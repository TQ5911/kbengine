package CentralLogin

import (
	"centralService/src/appLog"
	clientService "centralService/src/centralLogin/centralLoginApp/clientService"
	gameServerService "centralService/src/centralLogin/centralLoginApp/gameServerService"
	"centralService/src/common"
	"centralService/src/trpc"
	"database/sql"
	"errors"
	"fmt"
	"net"
	_ "net/http/pprof"
	"strconv"
	"strings"
	"sync"
	"syscall"
	"time"

	_ "github.com/go-sql-driver/mysql"
	"github.com/gomodule/redigo/redis"
	"github.com/google/uuid"
	"github.com/spf13/viper"
)

var LoginConfig = AppConfig{}
var ServerListCfg = viper.New()
var ConfMD5 = ""

const (
	_ = iota
	SERVICE_CLIENT_AUTH
	SERVICE_GAME_SERVER
)

type LoginAction func(*CentralLoginApp) error

type CentralLoginApp struct {
	common.App
	gameServers   map[uint32]*GameServerService
	channelToHost map[uuid.UUID]*GameServerService
	serversLock   *sync.RWMutex

	gameClients     map[string]*LoginClientService
	channelToClient map[uuid.UUID]*LoginClientService
	clientsLock     *sync.RWMutex

	actions    chan LoginAction
	httpServer *HttpService

	db        *sql.DB
	redisPool *redis.Pool
}

func NewCentralLoginApp() *CentralLoginApp {
	gameServers := make(map[uint32]*GameServerService)
	channelToHost := make(map[uuid.UUID]*GameServerService)
	gameClients := make(map[string]*LoginClientService)
	channelToClient := make(map[uuid.UUID]*LoginClientService)
	actions := make(chan LoginAction, 10)

	db, err := sql.Open("mysql", fmt.Sprintf("%s:%s@tcp(%s)/%s?charset=utf8",
		LoginConfig.Mysql.User, LoginConfig.Mysql.Passwd, LoginConfig.Mysql.Addr, LoginConfig.Mysql.Db))

	if err != nil {
		appLog.Error("open msyql error: ", err.Error())
		return nil
	}

	db.SetMaxIdleConns(50)
	db.SetConnMaxLifetime(time.Second * 290)
	db.SetMaxOpenConns(50)
	if err = db.Ping(); err != nil {
		appLog.Error("mysql connect err", err.Error())
		return nil
	}

	redisPool := common.NewRedisPool(common.RedisPoolOptions{
		ServerName:  "centralLogin",
		Addr:        LoginConfig.RedisServer.Addr,
		Username:    LoginConfig.RedisServer.Username,
		Password:    LoginConfig.RedisServer.Passwd,
		Db:          LoginConfig.RedisServer.Db,
		MaxIdle:     16,
		MaxActive:   500,
		IdleTimeout: 100,
	})

	app := CentralLoginApp{common.App{AppName: "CentralLoginApp"},
		gameServers, channelToHost, new(sync.RWMutex), gameClients, channelToClient, new(sync.RWMutex), actions, nil, db, redisPool}

	return &app
}

func (self *CentralLoginApp) GetServices() []*common.ServiceInfo {
	services := []*common.ServiceInfo{
		&common.ServiceInfo{SERVICE_CLIENT_AUTH, "客户端连接监听", LoginConfig.ClientServiceAddr},
		&common.ServiceInfo{SERVICE_GAME_SERVER, "游戏服连接监听", LoginConfig.GameServerServiceAddr},
	}
	return services
}

func (self *CentralLoginApp) Start() {
	self.App.Start()

	self.RegisterSignals(syscall.SIGINT, syscall.SIGKILL, syscall.SIGTERM)

	fmt.Printf("app starting: %+v\n", LoginConfig)

	go func() {
		<-self.SignalChan
		self.Stop()
	}()
	self.httpServer = &HttpService{self}
	go self.httpServer.startHttpServer(LoginConfig.IdipHttpServer)
}

func (self *CentralLoginApp) Stop() {
	self.db.Close()
}

func (self *CentralLoginApp) NewService(conn net.Conn, serviceType uint8) trpc.IServerEndPoint {
	var service trpc.IServerEndPoint = nil
	if serviceType == SERVICE_GAME_SERVER {
		rpcUUID := uuid.New()
		channel := trpc.NewRpcChannel(rpcUUID, conn)
		service = &GameServerService{ServerEndPoint: gameServerService.NewCentralServerService(gameServerService.NewGameServerClient(channel)), app: self}
		channel.SetEndPoint(service)

	} else if serviceType == SERVICE_CLIENT_AUTH {
		rpcUUID := uuid.New()
		channel := trpc.NewRpcChannel(rpcUUID, conn)
		service = &LoginClientService{
			ServerEndPoint:   clientService.NewCentralServerService(clientService.NewGameClientClient(channel)),
			app:              self,
			activeTickCnt:    0,
			loginResult:      clientService.LoginReply_LOGIN_NOT_LOGIN,
			isReqLogin:       false,
			isValid:          true,
			isCaptchaValid:   false,
			captchaBeginTime: 0,
		}
		channel.SetEndPoint(service)
		service.(*LoginClientService).resetThirdData()
		service.(*LoginClientService).startCheckValidTimer()
	}

	return service
}

func (self *CentralLoginApp) buildClientKey(accountType uint32, accountName string) string {
	return common.JoinToStr(accountType, "-", accountName)
}

func (self *CentralLoginApp) addClient(service *LoginClientService) {
	keyName := self.buildClientKey(uint32(service.accountType), service.accountName)
	//如果有老的，先把老的删了，否则客户端不断开快速连过来时，上一个连接超时会把当前的删掉
	self.clientsLock.Lock()
	defer self.clientsLock.Unlock()

	oldClient, ok := self.gameClients[keyName]

	if ok {
		self.removeClient(oldClient, false)
	}

	self.gameClients[keyName] = service
	self.channelToClient[service.GetRpcChannel().ChannelUUID] = service
}

func (self *CentralLoginApp) removeClient(service *LoginClientService, optional ...bool) {
	if !service.isValid {
		return
	}
	needLock := true
	if len(optional) == 1 {
		needLock = optional[0]
	}

	if needLock {
		self.clientsLock.Lock()
		defer self.clientsLock.Unlock()
	}

	service.isValid = false
	keyName := self.buildClientKey(uint32(service.accountType), service.accountName)
	delete(self.gameClients, keyName)
	delete(self.channelToClient, service.GetRpcChannel().ChannelUUID)
}

func (self *CentralLoginApp) getClient(accountType uint32, accountName string) *LoginClientService {
	self.clientsLock.RLock()
	defer self.clientsLock.RUnlock()
	keyName := self.buildClientKey(accountType, accountName)
	if clientSvc, ok := self.gameClients[keyName]; ok {
		return clientSvc
	}
	return nil
}

func (self *CentralLoginApp) checkClientLogin(gs *GameServerService, accountType uint32, accountName string, token string) (bool, uint32, string, string) {
	cs := self.getClient(accountType, accountName)
	if cs == nil {
		return self.checkClientLoginFromRedis(accountType, accountName, token)
	}

	if !cs.checkAccountType(clientService.AccountType(accountType)) {
		appLog.Error("checkClientLogin failed: unsupported accountType", LoginConfig.AccountTypes, accountType)
		return false, 0, "", "{}"
	}
	if cs.loginResult == clientService.LoginReply_LOGIN_SUCCESS && token == cs.loginToken {
		return true, cs.channelId, cs.userId, cs.otherJsonData
	} else {
		appLog.Error("checkClientLogin failed: ", cs.loginResult, cs.loginToken, token)
	}

	return false, 0, "", "{}"
}

// AccountLoginInfo 持久化在 Redis 中的客户端登录态。Key = login:accountinfo:{type}:{name}，Hash 字段见下。
type AccountLoginInfo struct {
	AccountType   uint32
	AccountName   string
	Token         string `redis:"token"`
	ChannelId     uint32 `redis:"channelId"`
	UserId        string `redis:"userId"`
	OtherJsonData string `redis:"otherJsonData"`
}

// accountLoginInfoTTL 是 hash 条目的 TTL（秒），覆盖常见 token 失效窗口。
const accountLoginInfoTTL = 3600

// AccountLoginInfoKey 返回 AccountLoginInfo 在 Redis 中的统一 key。
func AccountLoginInfoKey(accountType uint32, accountName string) string {
	return fmt.Sprintf("login:accountinfo:%d:%s", accountType, accountName)
}

// SaveAccountLoginInfo 把登录态写入 Redis hash 并设置 TTL。
func (self *CentralLoginApp) SaveAccountLoginInfo(info *AccountLoginInfo) error {
	key := AccountLoginInfoKey(info.AccountType, info.AccountName)
	conn, err := common.GetRedisConn(self.redisPool, "login.SaveAccountLoginInfo")
	if err != nil {
		return err
	}
	defer conn.Close()
	if _, err := conn.Do("HMSET", key,
		"token", info.Token,
		"channelId", info.ChannelId,
		"userId", info.UserId,
		"otherJsonData", info.OtherJsonData); err != nil {
		return err
	}
	_, err = conn.Do("EXPIRE", key, accountLoginInfoTTL)
	return err
}

// LoadAccountLoginInfo 从 Redis 读回登录态。key 不存在时返回 (info, nil)，其中 info.Token == ""。
func (self *CentralLoginApp) LoadAccountLoginInfo(accountType uint32, accountName string) (*AccountLoginInfo, error) {
	key := AccountLoginInfoKey(accountType, accountName)
	conn, err := common.GetRedisConn(self.redisPool, "login.LoadAccountLoginInfo")
	if err != nil {
		return nil, err
	}
	defer conn.Close()
	values, err := redis.Values(conn.Do("HGETALL", key))
	if err != nil {
		return nil, err
	}
	info := &AccountLoginInfo{
		AccountType: accountType,
		AccountName: accountName,
	}
	if err := redis.ScanStruct(values, info); err != nil {
		return nil, err
	}
	return info, nil
}

// DeleteAccountLoginInfo 删除某账号的登录态 hash（踢人 / 登出时使用）。
func (self *CentralLoginApp) DeleteAccountLoginInfo(accountType uint32, accountName string) error {
	key := AccountLoginInfoKey(accountType, accountName)
	conn, err := common.GetRedisConn(self.redisPool, "login.DeleteAccountLoginInfo")
	if err != nil {
		return err
	}
	defer conn.Close()
	_, err = conn.Do("del", key)
	return err
}

func (self *CentralLoginApp) checkClientLoginFromRedis(accountType uint32, accountName string, token string) (bool, uint32, string, string) {
	info, err := self.LoadAccountLoginInfo(accountType, accountName)
	if err != nil {
		appLog.Error("checkClientLoginFromRedis load failed", accountType, accountName, err.Error())
		return false, 0, "", "{}"
	}

	if info.Token == "" {
		appLog.Info("checkClientLoginFromRedis failed: cannot get token:", accountType, accountName)
		return false, 0, "", "{}"
	}

	if info.Token != token {
		appLog.Error("checkClientLoginFromRedis failed: token mismatch", info.Token, token)
		return false, 0, "", "{}"
	}

	return true, info.ChannelId, info.UserId, info.OtherJsonData
}

// KickAccountClient 把指定账号的客户端踢下线，并让后续 VerifyLogin 的 checkClientLogin 必失败：
//  1. 断开该客户端的 RPC 连接；
//  2. 从 gameClients 中移除（让 getClient 返回 nil）；
//  3. 清理 Redis 中保存的 login token（否则 checkClientLogin 会回退到 checkClientLoginFromRedis 并被旧 token 命中）。
func (self *CentralLoginApp) KickAccountClient(accountType uint32, accountName string) {
	if cs := self.getClient(accountType, accountName); cs != nil {
		self.removeClient(cs)
		cs.GetRpcChannel().Disconnect()
	}

	if err := self.DeleteAccountLoginInfo(accountType, accountName); err != nil {
		appLog.Error("KickAccountClient del failed", accountType, accountName, err.Error())
	}
	appLog.Info("KickAccountClient ok,", accountType, ",", accountName)
}

func (self *CentralLoginApp) addGameServer(service *GameServerService) {
	self.serversLock.Lock()
	defer self.serversLock.Unlock()

	self.gameServers[service.hostId] = service
	self.channelToHost[service.GetRpcChannel().ChannelUUID] = service
}

func (self *CentralLoginApp) removeGameServer(service *GameServerService) {
	self.serversLock.Lock()
	defer self.serversLock.Unlock()

	delete(self.gameServers, service.hostId)
	delete(self.channelToHost, service.GetRpcChannel().ChannelUUID)
}

func (self *CentralLoginApp) getGameServer(hostId uint32) *GameServerService {
	self.serversLock.RLock()
	defer self.serversLock.RUnlock()

	if gs, ok := self.gameServers[hostId]; ok {
		return gs
	}
	return nil
}

func (self *CentralLoginApp) delAccountByGOpenID(accountType int, accountGOpenID string) (uint8, error) {
	tx, err := self.db.Begin()
	if err != nil {
		appLog.Error("delAccountByGOpenID: fail to start transaction", accountGOpenID, err.Error())
		return 2, err
	}
	defer tx.Commit()
	var id int = 0
	err = tx.QueryRow("select id from account where accountType=? and accountName=?", accountType, accountGOpenID).Scan(&id)

	if err == sql.ErrNoRows {
		return 1, errors.New("account does not exist")
	} else if err != nil {
		appLog.Error("delAccountByGOpenID query account id error:", err.Error())
		return 3, errors.New(fmt.Sprint("delAccountByGOpenID query account id error:", err.Error()))
	}

	tx.Exec("update account set deleteTime=? where id=?", time.Now().Add(time.Duration(15*24*time.Hour)).Unix(), id)
	appLog.Info("deleteAccount:", accountGOpenID, id)

	return 0, nil
}

func (self *CentralLoginApp) queryAccountLastLogin(accountType int, accountGOpenID string) (uint8, uint32, error) {
	var id int = 0
	err := self.db.QueryRow("select id from account where accountType=? and accountName=?", accountType, accountGOpenID).Scan(&id)
	if err == sql.ErrNoRows {
		return 1, 0, errors.New("account does not exist")
	} else if err != nil {
		appLog.Error("queryAccountLastLogin: query account id error:", err.Error())
		return 3, 0, errors.New(fmt.Sprint("queryAccountLastLogin: query account id error:", err.Error()))
	}

	var tLastLogin uint32 = 0
	err = self.db.QueryRow("select max(tLastLogin) from account_characters where parentID=?", id).Scan(&tLastLogin)
	if err == sql.ErrNoRows {
		return 0, 0, nil
	} else if err != nil {
		appLog.Error("queryAccountLastLogin query max lastLogin error:", err.Error())
		return 3, 0, errors.New(fmt.Sprint("queryAccountLastLogin query max lastLogin error:", err.Error()))
	}
	appLog.Info("queryAccountLastLogin:", accountGOpenID, id, tLastLogin)
	return 0, tLastLogin, nil
}

func (self *CentralLoginApp) queryAccountServers(accountType int, accountGOpenID string) (uint8, string, error) {
	var id int = 0
	err := self.db.QueryRow("select id from account where accountType=? and accountName=?", accountType, accountGOpenID).Scan(&id)

	if err == sql.ErrNoRows {
		return 1, "", errors.New("account does not exist")
	} else if err != nil {
		appLog.Error("queryAccountServers query account error:", err.Error())
		return 3, "", errors.New(fmt.Sprint("queryAccountServers query account error:", err.Error()))
	}

	var hostIdList [1000]string

	rows, err := self.db.Query("select distinct(hostId) from account_characters where parentID=?", id)
	if err != nil {
		appLog.Error("get servers err: ", err.Error(), accountType, accountGOpenID)
		return 3, "", err
	} else {
		defer rows.Close()

		var hostId int = 0
		idx := 0
		for rows.Next() {
			if err = rows.Scan(&hostId); err != nil {
				appLog.Error("read character info err: ", accountType, accountGOpenID, err.Error())
				continue
			}
			hostIdList[idx] = strconv.Itoa(hostId)
			idx++
		}

		result := strings.Join(hostIdList[:idx], "|")
		appLog.Info("queryAccountServers:", accountGOpenID, id, result)
		return 0, result, nil
	}
}
