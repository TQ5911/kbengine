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

	"github.com/garyburd/redigo/redis"
	_ "github.com/go-sql-driver/mysql"
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

	redisPool := &redis.Pool{
		MaxIdle:     16,  //最大空闲连接数
		MaxActive:   100, //与数据库的最大链接数，0表示没有限制
		IdleTimeout: 100, //最大空闲时间
		Dial: func() (redis.Conn, error) {
			c, err := redis.Dial("tcp", LoginConfig.RedisServer.Addr)
			if err != nil {
				fmt.Println("conn redis failed,", err)
				return nil, err
			}
			if LoginConfig.RedisServer.Passwd != "" {
				if _, err := c.Do("AUTH", LoginConfig.RedisServer.Passwd); err != nil {
					c.Close()
					return nil, err
				}
			}

			if LoginConfig.RedisServer.Db != "" {
				if _, err := c.Do("SELECT", LoginConfig.RedisServer.Db); err != nil {
					c.Close()
					return nil, err
				}
			}
			return c, nil
		},
	}

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
		appLog.Error("checkClientLogin failed: cannot find client", accountType, accountName)
		return false, 0, "", "{}"
	}

	if cs.loginResult == clientService.LoginReply_LOGIN_SUCCESS && token == cs.loginToken {
		return true, cs.channelId, cs.accountId, cs.otherJsonData
	} else {
		appLog.Error("checkClientLogin failed: ", cs.loginResult, cs.loginToken, token)
	}

	return false, 0, "", "{}"
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
