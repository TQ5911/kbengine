package CentralLogin

import (
	"centralService/src/appLog"
	clientService "centralService/src/centralLogin/centralLoginApp/clientService"
	"centralService/src/common"
	"centralService/src/trpc"
	"crypto/ecdsa"
	"crypto/hmac"
	"crypto/sha1"
	"encoding/base64"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"io/ioutil"
	"math"
	"math/rand"
	"net/http"
	"strconv"
	"strings"
	"time"

	"github.com/dgrijalva/jwt-go"
	"github.com/garyburd/redigo/redis"
)

const SERVER_RAND_STR_LEN int = 10
const LOGIN_TOKEN_LEN int = 15
const SECONDS_ONE_DAY = 86400

// 成功
const SUCCESS = 0

// 错误
const ERROR = 1

// 超时
const TIMEOUT = 2

// QPS限制
const QPSLIMIT = 3

// 给客户端保持在线时间
const CLIENT_ONLINE_TIME = 30

// 中心服向客户端提供的接口
type LoginClientService struct {
	*trpc.ServerEndPoint
	app              *CentralLoginApp
	accountName      string
	accountType      clientService.AccountType
	serverRandStr    string
	loginResult      clientService.LoginReply_LoginResult
	loginToken       string
	activeTickCnt    int
	isValid          bool
	channelId        uint32
	isReqLogin       bool
	serverId         string
	gsHost           string
	qsHost           string
	isCaptchaValid   bool
	captchaBeginTime int64
	tokenTimeout	 uint32
	userId      	 string
	otherJsonData	 string
}

type PayLoad struct {
	Exp    int64 `json:"exp"`
	UserId int64 `json:"userId"`
	Iat    int64 `json:"iat"`
}

type UserInfo struct {
	UserId   int64  `json:"userId"`
	NickName string `json:"nickname"`
	Avatar   string `json:"avatar"`
	Country  string `json:"country"`
	Province string `json:"province"`
	IsAudit  bool   `json:"isAudit"`
	DeviceId string `json:"deviceId"`
}

type ChannelInfo struct {
	Id   			uint32 `json:"id"`
}

type TapTapAccessToken struct {
	Kid   			string `json:"kid"`
	TokenType 		string `json:"token_type"`
	MacKey   		string `json:"mac_key"`
	MacAlgorithm  	string `json:"mac_algorithm"`
	ScopeSet 	    []string `json:"scopeSet"`
}

type TapTapResponseData struct {
	Code                 int    `json:"code"`
	Msg                  string `json:"msg"`
	Error                string `json:"error"`
	ErrorDescription     string `json:"error_description"`

	Avatar 		         string `json:"avatar"`
	Gender               string `json:"gender"`
	Name   			     string `json:"name"`
	OpenId   		     string `json:"openid"`
	UnionId  	         string `json:"unionid"`
}

type TapTapAccessTokenResponse  struct {
	Data    		TapTapResponseData    `json:"data"`
	Now     		int64                 `json:"now"`
	Success 		bool                  `json:"success"`
}

var tapTapErrorMap = map[string]clientService.LoginReply_LoginResult {
	"access_denied":        clientService.LoginReply_LOGIN_THIRD_TAPTAP_ACCESS_DENIED,
    "forbidden":            clientService.LoginReply_LOGIN_THIRD_TAPTAP_FORBIDDEN,
    "server_error":         clientService.LoginReply_LOGIN_THIRD_TAPTAP_SERVER_ERROR,
    "insufficient_scope":   clientService.LoginReply_LOGIN_THIRD_TAPTAP_INSUFFICIENT_SCOPE,
}

type OfficialAccessToken struct {
	Token 			string `json:"token"`
}

type OfficialResponseData struct {
	GameId					string 	`json:"gameId"`
	TokenRefreshed			bool 	`json:"tokenRefreshed"`
	UserGameId				string 	`json:"userGameId"`
	Phone               	string 	`json:"phone"`
	TokenValid				bool 	`json:"tokenValid"`
	TokenTimeout   			string 	`json:"tokenTimeout"`
	UserInfoId   		  	string 	`json:"userInfoId"`
	NewToken  	         	string 	`json:"token"`
	IsCertified				bool	`json:"isCertified"`
	Birthday				string	`json:"birthday"`
	Age						uint32	`json:"age"`
}

type OfficialAccessTokenResponse  struct {
	Success			bool					`json:"-"`
	Code			int32					`json:"code"`
	Message 		string                	`json:"message"`
	Data    		OfficialResponseData  	`json:"data"`
	Timestamp     	string                 	`json:"timestamp"`
}

var officialErrorMap = map[int32]clientService.LoginReply_LoginResult {
	401:        			clientService.LoginReply_LOGIN_THIRD_OFFICIAL_401,
    500:            		clientService.LoginReply_LOGIN_THIRD_OFFICIAL_500,
    1001:         			clientService.LoginReply_LOGIN_THIRD_OFFICIAL_1001,
}

func (self *LoginClientService) startCheckValidTimer() {
	time.AfterFunc(time.Duration(time.Second*CLIENT_ONLINE_TIME), func() {
		self.checkIsReqLogin()
	})
}

func (self *LoginClientService) checkIsReqLogin() {
	appLog.Debug("checkIsReqLogin", self.isReqLogin)
	if !self.isReqLogin {
		self.GetRpcChannel().Disconnect()
	} else {
		appLog.Debug("request get login key", self.isReqLogin)
	}
}

func (self *LoginClientService) OnLoseConnection() {
	appLog.Infof("OnLoseConnection from %v\n", self.GetRpcChannel().GetRemoteAddr())
	self.app.removeClient(self)
}

func (self *LoginClientService) encrptStr(content string) string {
	return content
}

func (self *LoginClientService) decryptStr(content string) string {
	return content
}

func (self *LoginClientService) checkAccountType(accountType clientService.AccountType) bool {
	if len(LoginConfig.AccountTypes) == 0 {
		return true
	}

	for _, tp := range LoginConfig.AccountTypes {
		if clientService.AccountType(tp) == accountType {
			return true
		}
	}

	return false
}

func (self *LoginClientService) GetLoginKey(r *clientService.LoginKeyRequest) (*clientService.Void, error) {
	appLog.Info("request get login key", r.RStr)
	self.serverRandStr = common.RandString(SERVER_RAND_STR_LEN)
	loginKey := clientService.LoginKeyResponse{RStr: r.RStr, SStr: self.serverRandStr}
	_, err := self.GetClientEndPoint().(clientService.IGameClientInterface).OnGetLoginKey(&loginKey)
	return nil, err
}

func (self *LoginClientService) onLoginSucess(accountType clientService.AccountType, accountName string) {
	appLog.Info("onLoginSucess", accountType, accountName)
	sql := "insert into account (accountType, accountName) value (?, ?) on duplicate key update id=id"
	appLog.Info("onLoginSucess app", self.app == nil, self.app.db == nil)
	_, err := self.app.db.Exec(sql, accountType, accountName)

	if err != nil {
		appLog.Error("write account err: ", accountType, accountName, err.Error())
	}
}

func (self *LoginClientService) _replyNeedCDKey() error {
	appLog.Debug("login need cdkey ", self.accountType, self.accountName, self.loginToken)
	reply := clientService.LoginReply{Result: clientService.LoginReply_LOGIN_NEED_CDKEY, Token: "", CentralServerId: LoginConfig.CentralServerId, ServerId: self.serverId, GameServerHost: self.gsHost, QueueServerHost: self.qsHost, TokenTimeout: self.tokenTimeout, Reserved: self.otherJsonData}
	_, err := self.GetClientEndPoint().(clientService.IGameClientInterface).OnLoginReply(&reply)
	return err
}

func (self *LoginClientService) _replyLoginSuccess() error {
	appLog.Info("login success ", self.accountType, self.accountName, self.loginToken, self.serverId, self.gsHost, self.qsHost, self.tokenTimeout, self.otherJsonData)
	reply := clientService.LoginReply{Result: clientService.LoginReply_LOGIN_SUCCESS, Token: self.loginToken, CentralServerId: LoginConfig.CentralServerId, ServerId: self.serverId, GameServerHost: self.gsHost, QueueServerHost: self.qsHost, TokenTimeout: self.tokenTimeout, Reserved: self.otherJsonData}
	_, err := self.GetClientEndPoint().(clientService.IGameClientInterface).OnLoginReply(&reply)
	return err
}

func (self *LoginClientService) _replyCheckCaptcha(needCaptcha bool, forbiddenDueTime int64, captchaType clientService.CaptchaType) error {
	appLog.Info("reply check captcha ", self.accountType, self.accountName)
	// 如果需要验证码，记录开始时间
	if needCaptcha {
		self.captchaBeginTime = time.Now().UnixMilli()
	}
	reply := clientService.CheckCaptchaNotify{CaptchaType: captchaType, NeedCaptcha: needCaptcha, ForbidExpireTime: forbiddenDueTime}
	_, err := self.GetClientEndPoint().(clientService.IGameClientInterface).OnCheckCaptcha(&reply)
	if err != nil {
		appLog.Error("reply check captcha error, ", self.accountType, self.accountName, err.Error())
	}
	return err
}

func (self *LoginClientService) CheckLockLogin(r *clientService.PasswordLogin) bool {
	conn := self.app.redisPool.Get()
	defer conn.Close()
	key := fmt.Sprintf("lockLogin_%v", r.AccountName)
	value, err := redis.Int(conn.Do("get", key))
	if err != nil && err.Error() != "redigo: nil returned" {
		appLog.Error("CheckLockLogin: get ttl failed", r.AccountName, err.Error())
		return false
	}

	if value > 0 {
		return true
	}

	return false
}

func (self *LoginClientService) LoginByPassword(r *clientService.PasswordLogin) (*clientService.Void, error) {
	self.isReqLogin = true
	if !self.checkAccountType(clientService.AccountType_ACCOUNT_PASSWD) {
		appLog.Error("LoginByPassword: accountType is forbidden")
		return nil, errors.New(fmt.Sprintf("LoginByPassword is forbidden"))
	}

	if self.CheckLockLogin(r) {
		appLog.Error("LoginByPassword: account is locked")
		return nil, errors.New(fmt.Sprintf("LoginByPassword is locked"))
	}

	self.accountName = r.AccountName
	self.accountType = clientService.AccountType_ACCOUNT_PASSWD
	self.userId = fmt.Sprintf("PWD:%d:%s", self.accountType, self.accountName)
	self.loginToken = common.RandString(LOGIN_TOKEN_LEN)
	self.app.addClient(self)

	self.onLoginSucess(self.accountType, self.accountName)

	appLog.Info("LoginByPassword: ", self.accountType, self.userId, self.accountName, self.loginToken)

	self.loginResult = clientService.LoginReply_LOGIN_SUCCESS
	err := self._replyLoginSuccess()

	if err != nil {
		self.app.removeClient(self)
		return nil, err
	}

	return nil, nil
}

func (self *LoginClientService) CheckCDkey(in *clientService.CheckCDKeyRequest) (*clientService.Void, error) {
	checkUrl := fmt.Sprintf("http://%s/checkCdkey?key=%s", "", in.Key)
	client := http.Client{Timeout: 3 * time.Second}
	resp, err := client.Get(checkUrl)
	if err != nil {
		appLog.Error("call http api error", err.Error())
		return nil, nil
	}

	if resp.StatusCode != 200 {
		appLog.Error("call http api status error", resp.StatusCode)
		return nil, nil
	}

	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)

	if err != nil {
		appLog.Error("read body error ", err.Error())
		return nil, nil
	}
	result, err := strconv.ParseInt(string(body), 10, 32)
	if err != nil {
		appLog.Error("parse body error ", err.Error())
		return nil, err
	}

	code := clientService.CheckCDKeyReply_CDKeyResult(result)
	appLog.Debugf(fmt.Sprintf("check CDKey: %s %s", in.Key, code))

	if code == clientService.CheckCDKeyReply_CDKEY_OK {
		sql := "update account set accountCDKey=? where accountType=? and accountName=?"
		res, err := self.app.db.Exec(sql, in.Key, self.accountType, self.accountName)
		if err != nil {
			appLog.Error("update cd key error", err.Error())
			return nil, nil
		}
		nEffected, err := res.RowsAffected()
		if err != nil {
			appLog.Error("update cd key effected row err:", err.Error())
			return nil, nil
		}

		if nEffected != 1 {
			appLog.Error("update cd key effected row not found:", nEffected)
			return nil, nil
		}
		self.loginResult = clientService.LoginReply_LOGIN_SUCCESS
	}

	checkReply := clientService.CheckCDKeyReply{Result: code}
	_, err = self.GetClientEndPoint().(clientService.IGameClientInterface).OnCheckCDKey(&checkReply)
	if err != nil {
		return nil, err
	}

	if self.loginResult == clientService.LoginReply_LOGIN_SUCCESS {
		reply := clientService.LoginReply{Result: clientService.LoginReply_LOGIN_SUCCESS, Token: self.loginToken, CentralServerId: LoginConfig.CentralServerId, ServerId: self.serverId, GameServerHost: self.gsHost, QueueServerHost: self.qsHost, TokenTimeout: self.tokenTimeout, Reserved: self.otherJsonData}
		_, err = self.GetClientEndPoint().(clientService.IGameClientInterface).OnLoginReply(&reply)
	}

	return nil, err
}

func (self *LoginClientService) ListServers(in *clientService.Void) (*clientService.Void, error) {
	if self.loginResult != clientService.LoginReply_LOGIN_SUCCESS {
		return nil, errors.New(fmt.Sprint("ListServers before login:", self.accountType, self.accountName, self.loginResult))
	}
	servers := clientService.ServerInfo{}
	servers.Servers = make([]*clientService.ServerInfoVal, 0, 10)

	self.app.serversLock.RLock()
	defer self.app.serversLock.RUnlock()

	for hostId, hs := range self.app.gameServers {
		var status clientService.ServerInfoVal_ServerStatus
		if hs.onlineNum >= 1000 {
			status = clientService.ServerInfoVal_ST_BAOMAN
		} else if hs.onlineNum >= 500 {
			status = clientService.ServerInfoVal_ST_YONGJI
		} else {
			status = clientService.ServerInfoVal_ST_LIUCHANG
		}
		servers.Servers = append(servers.Servers, &clientService.ServerInfoVal{HostId: hostId, Status: status})
	}

	appLog.Debug("listerServers")

	_, err := self.GetClientEndPoint().(clientService.IGameClientInterface).OnListServers(&servers)
	return nil, err
}

func (self *LoginClientService) GetCharaterInfo(*clientService.Void) (*clientService.Void, error) {
	if self.loginResult != clientService.LoginReply_LOGIN_SUCCESS {
		return nil, errors.New(fmt.Sprint("get character before login:", self.accountType, self.accountName, self.loginResult))
	}

	info := clientService.CharacterInfo{}
	info.Info = make([]*clientService.CharacterInfo_CharacterVal, 0, 1)
	appLog.Info("GetCharacterInfo", self.accountType, self.accountName)

	sql := "select AC.hostId, AC.name, AC.level, AC.school, AC.gbId, AC.sex, AC.tLastLogin, A.id, A.deleteTime from account_characters as AC, account as A where A.accountType=? and A.accountName=? and AC.parentID=A.id"
	rows, err := self.app.db.Query(sql, self.accountType, self.accountName)
	if err != nil {
		appLog.Error("get characters err: ", err.Error(), self.accountType, self.accountName)
		return nil, err
	} else {
		defer rows.Close()

		var hostId, level, school, sex, tLastLogin, deleteTime uint32 = 0, 0, 0, 0, 0, 0
		var gbId uint64 = 0
		var tblAccountId uint64 = 0
		name := ""

		for rows.Next() {
			if err = rows.Scan(&hostId, &name, &level, &school, &gbId, &sex, &tLastLogin, &tblAccountId, &deleteTime); err != nil {
				appLog.Error("read charachter info err: ", self.accountName, self.accountType, err.Error())
				continue
			}

			info.Info = append(info.Info, &clientService.CharacterInfo_CharacterVal{HostId: hostId, Name: name, School: school, Level: level, GbId: gbId, Sex: sex, TLastLogin: tLastLogin})
		}
		appLog.Infof(fmt.Sprintf("GetCharacterInfo %s %v", self.accountName, info.Info))
		_, err := self.GetClientEndPoint().(clientService.IGameClientInterface).OnGetCharacterInfo(&info)
		if err != nil {
			return nil, err
		}
	}
	return nil, nil
}

func (self *LoginClientService) ActiveTick(in *clientService.Void) (*clientService.Void, error) {
	self.activeTickCnt += 1
	if self.loginResult != clientService.LoginReply_LOGIN_SUCCESS && self.loginResult != clientService.LoginReply_LOGIN_NEED_CDKEY && self.activeTickCnt >= 3 {
		return nil, errors.New(fmt.Sprint("login fail for long time:", self.accountType, self.accountName, self.GetRpcChannel().GetRemoteAddr().String()))
	}

	if self.loginResult == clientService.LoginReply_LOGIN_NEED_CDKEY && self.activeTickCnt >= 30 {
		return nil, errors.New(fmt.Sprint("wait for cd key for long time:", self.accountType, self.accountName, self.GetRpcChannel().GetRemoteAddr().String()))
	}

	_, err := self.GetClientEndPoint().(clientService.IGameClientInterface).ActiveTickCallback(&clientService.Void{})
	return nil, err
}

func (self *LoginClientService) GetServerListDir(r *clientService.ServerListRequest) (*clientService.Void, error) {
	appLog.Info("GetServerListDir: request: ", r.ClientType, r.ClientVersion, r.IsMaple)
	if r.IsMaple {
		return nil, nil
	} else {
		return nil, nil
	}
	return nil, nil
}

func (self *LoginClientService) _getServerListInfo(province string, isAudit bool) (string, string, string) {
	if isAudit {
		bestServerId := ServerListCfg.GetString("auditServerId")
		gsHost := ServerListCfg.GetString(fmt.Sprintf("gameServerList.%s", bestServerId))
		qsHost := ServerListCfg.GetString(fmt.Sprintf("queueServerList.%s", bestServerId))
		return bestServerId, gsHost, qsHost
	}

	conn := self.app.redisPool.Get()
	defer conn.Close()
	lastServerId, err := redis.Int(conn.Do("get", common.LAST_SERVER_ID+self.accountName))
	if err != nil {
		appLog.Warn("_getServerListInfo get lastServerId failed", self.accountName, err.Error())
	} else {
		if lastServerId != 0 {
			gsHost := ServerListCfg.GetString(fmt.Sprintf("gameServerList.%s", strconv.Itoa(lastServerId)))
			qsHost := ServerListCfg.GetString(fmt.Sprintf("queueServerList.%s", strconv.Itoa(lastServerId)))
			return strconv.Itoa(lastServerId), gsHost, qsHost
		}
	}

	bestServerId := ""
	group := ServerListCfg.GetString(fmt.Sprintf("provinceServer.%s", province))
	serverIds := ServerListCfg.GetStringSlice(fmt.Sprintf("serverGroup.%s", group))
	if serverIds == nil || len(serverIds) <= 0 {
		appLog.Warn("_getServerListInfo cannot find any serverIds", province)
		var serverListMap = ServerListCfg.GetStringMapString("gameServerList")
		bestServerId = common.RandMapKey(serverListMap)
		gsHost := ServerListCfg.GetString(fmt.Sprintf("gameServerList.%s", bestServerId))
		qsHost := ServerListCfg.GetString(fmt.Sprintf("queueServerList.%s", bestServerId))
		return bestServerId, gsHost, qsHost
	}

	maxOnlineNum := ServerListCfg.GetUint32("maxOnlineNum")
	for _, serverId := range serverIds {
		curServerId, err := strconv.Atoi(serverId)
		if err != nil {
			appLog.Error("_getServerListInfo parse serverId error", err, serverId)
			continue
		}

		gameServer := self.app.getGameServer(uint32(curServerId))
		if gameServer == nil {
			continue
		}
		if gameServer.onlineNum <= maxOnlineNum {
			bestServerId = serverId
			break
		}
	}

	if bestServerId == "" {
		bestServerId = serverIds[rand.Intn(len(serverIds))]
	}

	gsHost := ServerListCfg.GetString(fmt.Sprintf("gameServerList.%s", bestServerId))
	qsHost := ServerListCfg.GetString(fmt.Sprintf("queueServerList.%s", bestServerId))
	return bestServerId, gsHost, qsHost
}

func (self *LoginClientService) LoginByToken(r *clientService.TokenLogin) (*clientService.Void, error) {
	appLog.Info("LoginByToken: verify request: ", r.Phone, r.Token, r.UserInfo)
	self.isReqLogin = true
	var err error

	var userInfo UserInfo
	err = json.Unmarshal([]byte(r.UserInfo), &userInfo)
	if err != nil {
		return nil, errors.New(fmt.Sprintf("fails to unmarshal userInfo: %s", r.UserInfo))
	}

	token := r.Token
	appLog.Info("LoginByToken: ", r.Phone, token)

	key, fileErr := ioutil.ReadFile("ec256-public.pem")
	if fileErr != nil {
		return nil, errors.New(fmt.Sprintf("cannot find public.pem file"))
	}

	var ecdsaKey *ecdsa.PublicKey
	if ecdsaKey, err = jwt.ParseECPublicKeyFromPEM(key); err != nil {
		appLog.Errorf(fmt.Sprintf("Unable to parse ECDSA public key: %v", err.Error()))
		return nil, errors.New(fmt.Sprintf("Unable to parse ECDSA public key: %v", err.Error()))
	}

	parts := strings.Split(token, ".")
	var cnt = 0
	var payLoadStr = ""
	var payLoad PayLoad
	for _, val := range parts {
		cnt++
		if cnt == 2 {
			e := base64.StdEncoding.WithPadding(base64.NoPadding)
			msg, _ := e.DecodeString(val)
			payLoadStr = string(msg)
			appLog.Debugf(fmt.Sprintf("payLoad: %s", payLoadStr))
			err = json.Unmarshal(msg, &payLoad)
			if err != nil {
				return nil, errors.New(fmt.Sprintf("fails to unmarshal json: %s", payLoadStr))
			}
			curTime := time.Now().Unix()
			if curTime > payLoad.Exp {
				reply := clientService.LoginReply{Result: clientService.LoginReply_LOGIN_TOKEN_ERROR, Token: self.loginToken, CentralServerId: LoginConfig.CentralServerId, ServerId: self.serverId, GameServerHost: self.gsHost, QueueServerHost: self.qsHost, TokenTimeout: self.tokenTimeout, Reserved: self.otherJsonData}
				self.GetClientEndPoint().(clientService.IGameClientInterface).OnLoginReply(&reply)
				appLog.Warn("LoginByToken: token expired", curTime, payLoad.Exp)
				return nil, nil
			}
			break
		}
	}

	if len(parts) < 3 {
		reply := clientService.LoginReply{Result: clientService.LoginReply_LOGIN_TOKEN_ERROR, Token: self.loginToken, CentralServerId: LoginConfig.CentralServerId, ServerId: self.serverId, GameServerHost: self.gsHost, QueueServerHost: self.qsHost, TokenTimeout: self.tokenTimeout, Reserved: self.otherJsonData}
		self.GetClientEndPoint().(clientService.IGameClientInterface).OnLoginReply(&reply)
		appLog.Warn("LoginByToken: token len err", r.Phone, r.Token)
		return nil, nil
	}

	method := jwt.GetSigningMethod("ES256")
	err = method.Verify(strings.Join(parts[0:2], "."), parts[2], ecdsaKey)
	if err != nil {
		reply := clientService.LoginReply{Result: clientService.LoginReply_LOGIN_TOKEN_ERROR, Token: self.loginToken, CentralServerId: LoginConfig.CentralServerId, ServerId: self.serverId, GameServerHost: self.gsHost, QueueServerHost: self.qsHost, TokenTimeout: self.tokenTimeout, Reserved: self.otherJsonData}
		self.GetClientEndPoint().(clientService.IGameClientInterface).OnLoginReply(&reply)
		appLog.Warn("LoginByToken: token err", r.Phone, r.Token)
		return nil, nil
	} else {
		conn := self.app.redisPool.Get()
		defer conn.Close()
		var deviceId = userInfo.DeviceId
		resMap, err := redis.Int64Map(conn.Do("HGETALL", common.DEVICE_ID+deviceId))
		if err != nil {
			return nil, errors.New(fmt.Sprintf("LoginByToken: HGETALL failed: %s", deviceId))
		}

		var accountNum = 0
		var accountName = strconv.FormatInt(payLoad.UserId, 10)
		var curTime = time.Now().Unix()
		var isExist = false
		for userId, lastLoginTime := range resMap {
			if curTime-lastLoginTime < SECONDS_ONE_DAY {
				accountNum += 1
				if userId == accountName {
					isExist = true
				}
			} else {
				_, err := redis.Int(conn.Do("HDEL", common.DEVICE_ID+deviceId, userId))
				if err != nil {
					appLog.Error("LoginByToken HDEL deviceId failed", deviceId, userId, err.Error())
				}
			}
		}

		maxAccountPerDevice := ServerListCfg.GetInt("maxAccountPerDevice")
		if accountNum < maxAccountPerDevice || isExist {
			_, err := redis.String(conn.Do("HMSET", common.DEVICE_ID+deviceId, accountName, curTime))
			if err != nil {
				appLog.Error("LoginByToken HMSET deviceId failed", deviceId, accountName, curTime, err.Error())
			}
		} else {
			reply := clientService.LoginReply{Result: clientService.LoginReply_LOGIN_DEVICE_LIMIT, Token: self.loginToken, CentralServerId: LoginConfig.CentralServerId, ServerId: self.serverId, GameServerHost: self.gsHost, QueueServerHost: self.qsHost, TokenTimeout: self.tokenTimeout, Reserved: self.otherJsonData}
			self.GetClientEndPoint().(clientService.IGameClientInterface).OnLoginReply(&reply)
			appLog.Warn("LoginByToken: device limit err", deviceId, accountNum, isExist)
			return nil, nil
		}

		self.accountName = accountName
		self.accountType = clientService.AccountType_ACCOUNT_TOKEN
		self.loginResult = clientService.LoginReply_LOGIN_SUCCESS
		self.loginToken = common.RandString(LOGIN_TOKEN_LEN)
		self.serverId, self.gsHost, self.qsHost = self._getServerListInfo(userInfo.Province, userInfo.IsAudit)
		self.app.addClient(self)

		self.onLoginSucess(self.accountType, self.accountName)

		err = self._replyLogin()

		if err != nil {
			self.app.removeClient(self)
			return nil, err
		}

		return nil, nil
	}
}

func (self *LoginClientService) resetThirdData() {
	self.accountType = clientService.AccountType_ACCOUNT_UNKNOW
	self.userId = ""
	self.accountName = ""
	self.loginToken = ""
	self.tokenTimeout = 0
	self.otherJsonData = "{}"
}

func (self *LoginClientService) _hmacSha1(valStr, keyStr string) (string) {
	key := []byte(keyStr)
	mac := hmac.New(sha1.New, key)
	mac.Write([]byte(valStr))

	return base64.StdEncoding.EncodeToString(mac.Sum(nil))
}

func (self *LoginClientService) _getTapTapLoginResultByErrorMsg(errorMsg string) (clientService.LoginReply_LoginResult) {
    if result, exists := tapTapErrorMap[errorMsg]; exists {
        return result
    }
    return clientService.LoginReply_LOGIN_THIRD_FAILED
}

func (self *LoginClientService) _attemptTapTapRequest(reqURL, authorization string, loginResult *clientService.LoginReply_LoginResult) bool {
	client := http.Client{Timeout: 5 * time.Second}
	req, err := http.NewRequest(http.MethodGet, reqURL, nil)
	if err != nil {
		appLog.Warn(fmt.Sprintf("_attemptTapTapRequest NewRequest: %s", err.Error()))
		return false
	}

	req.Header.Add("Authorization", authorization)
	resp, err := client.Do(req)
	if err != nil {
		appLog.Warn(fmt.Sprintf("_attemptTapTapRequest DoRequest: %s", err.Error()))
		return false
	}
	defer resp.Body.Close()

	respBody, err := io.ReadAll(resp.Body)
	if err != nil {
		appLog.Warn(fmt.Sprintf("_attemptTapTapRequest ReadAll: %s", err.Error()))
		return false
	}

	appLog.Info(fmt.Sprintf("_attemptTapTapRequest respBody: %s ", string(respBody)))

	var tapTapAccessTokenResponse TapTapAccessTokenResponse
	err = json.Unmarshal([]byte(respBody), &tapTapAccessTokenResponse)
	if err != nil {
		appLog.Warn(fmt.Sprintf("_attemptTapTapRequest fails to unmarshal err: %s", err.Error()))
	   	return false
	}
	self.resetThirdData()
	if !tapTapAccessTokenResponse.Success {
		appLog.Warn(fmt.Sprintf("_attemptTapTapRequest respBody false: %d, %s, %s, %s", tapTapAccessTokenResponse.Data.Code, tapTapAccessTokenResponse.Data.Msg,
		tapTapAccessTokenResponse.Data.Error, tapTapAccessTokenResponse.Data.ErrorDescription))
		*loginResult = self._getTapTapLoginResultByErrorMsg(tapTapAccessTokenResponse.Data.Error)
	} else {
		appLog.Info(fmt.Sprintf("_attemptTapTapRequest respBody true: %s, %s, %s, %s, %s", tapTapAccessTokenResponse.Data.Avatar, tapTapAccessTokenResponse.Data.Gender,
		tapTapAccessTokenResponse.Data.Name, tapTapAccessTokenResponse.Data.OpenId, tapTapAccessTokenResponse.Data.UnionId))
		self.accountType = clientService.AccountType_ACCOUNT_TAPTAP
		self.userId = tapTapAccessTokenResponse.Data.UnionId
		self.accountName = tapTapAccessTokenResponse.Data.OpenId
		self.loginToken = common.RandString(LOGIN_TOKEN_LEN)
	}
	return tapTapAccessTokenResponse.Success
}

func (self *LoginClientService) _loginByTapTap(channelInfo *ChannelInfo, tapTapAccessToken *TapTapAccessToken, loginResult *clientService.LoginReply_LoginResult) (bool) {
	appLog.Info("_loginByTapTap: verify request")

	var clientId string
	if value, ok := LoginConfig.TapTap["clientid"]; ok {
		clientId = value.(string)
	} else {
		appLog.Error("_loginByTapTap LoginConfig.TapTap[clientId]")
		return false
	}

	kid := tapTapAccessToken.Kid

	macKey := tapTapAccessToken.MacKey

	var nonce string
	if value, ok := LoginConfig.TapTap["nonce"]; ok {
		nonce = value.(string)
	} else {
		appLog.Error("_loginByTapTap LoginConfig.TapTap[nonce]")
		return false
	}

	timestamp := strconv.FormatInt(time.Now().Unix(), 10)

	var reqHost string
	if value, ok := LoginConfig.TapTap["reqhost"]; ok {
		reqHost = value.(string)
	} else {
		appLog.Error("_loginByTapTap LoginConfig.TapTap[reqHost]")
		return false
	}

	var reqURI string
	if value, ok := LoginConfig.TapTap["requri"]; ok {
		reqURI = value.(string) + clientId
	} else {
		appLog.Error("_loginByTapTap LoginConfig.TapTap[reqURI]")
		return false
	}

	reqURL := "https://" + reqHost + reqURI

	macStr := timestamp + "\n" + nonce + "\n" + "GET" + "\n" + reqURI + "\n" + reqHost + "\n" + "443" + "\n\n"

	mac := self._hmacSha1(macStr, macKey)

	authorization := "MAC id=" + "\"" + kid + "\"" + "," + "ts=" + "\"" + timestamp + "\"" + "," + "nonce=" + "\"" + nonce + "\"" + "," + "mac=" + "\"" + mac + "\""

	appLog.Info(fmt.Sprintf("_loginByTapTap authorization: %s", authorization))

	return self._attemptTapTapRequest(reqURL, authorization, loginResult)
}

func (self *LoginClientService) _getOfficialLoginResultByErrorMsg(errorCode int32) (clientService.LoginReply_LoginResult) {
    if result, exists := officialErrorMap[errorCode]; exists {
        return result
    }
    return clientService.LoginReply_LOGIN_THIRD_FAILED
}

func (self *LoginClientService) _attemptOfficialRequest(reqURL, token string, loginResult *clientService.LoginReply_LoginResult) bool {
	client := http.Client{Timeout: 5 * time.Second}
	req, err := http.NewRequest(http.MethodPost, reqURL, nil)
	if err != nil {
		appLog.Warn(fmt.Sprintf("_attemptOfficialRequest NewRequest: %s", err.Error()))
		return false
	}

	req.Header.Add("satoken", token)
	resp, err := client.Do(req)
	if err != nil {
		appLog.Warn(fmt.Sprintf("_attemptOfficialRequest DoRequest: %s", err.Error()))
		return false
	}
	defer resp.Body.Close()

	respBody, err := io.ReadAll(resp.Body)
	if err != nil {
		appLog.Warn(fmt.Sprintf("_attemptOfficialRequest ReadAll: %s", err.Error()))
		return false
	}

	appLog.Info(fmt.Sprintf("_attemptOfficialRequest respBody: %s ", string(respBody)))

	var officialAccessTokenResponse OfficialAccessTokenResponse
	err = json.Unmarshal([]byte(respBody), &officialAccessTokenResponse)
	if err != nil {
		appLog.Warn(fmt.Sprintf("_attemptOfficialRequest fails to unmarshal err: %s", err.Error()))
	   	return false
	}
	self.resetThirdData()
	if officialAccessTokenResponse.Code != 200 {
		appLog.Warn(fmt.Sprintf("_attemptOfficialRequest respBody false: %d, %s", officialAccessTokenResponse.Code, officialAccessTokenResponse.Message))
		*loginResult = self._getOfficialLoginResultByErrorMsg(officialAccessTokenResponse.Code)
		officialAccessTokenResponse.Success = false
	} else {
		appLog.Info(fmt.Sprintf("_attemptOfficialRequest respBody true: %s, %t, %s, %s, %t, %s, %s, %s, %t, %s, %d", officialAccessTokenResponse.Data.GameId, officialAccessTokenResponse.Data.TokenRefreshed,
		officialAccessTokenResponse.Data.UserGameId, officialAccessTokenResponse.Data.Phone, officialAccessTokenResponse.Data.TokenValid,
		officialAccessTokenResponse.Data.TokenTimeout, officialAccessTokenResponse.Data.UserInfoId, officialAccessTokenResponse.Data.NewToken,
		officialAccessTokenResponse.Data.IsCertified, officialAccessTokenResponse.Data.Birthday, officialAccessTokenResponse.Data.Age))

		tokenTimeout, err1 := strconv.ParseUint(officialAccessTokenResponse.Data.TokenTimeout, 10, 32)
		phone, err2 := strconv.ParseUint(officialAccessTokenResponse.Data.Phone, 10, 64)
		//birthday, err2 := strconv.ParseUint(officialAccessTokenResponse.Data.Birthday, 10, 32)
		//isCertified := officialAccessTokenResponse.Data.IsCertified
		age := officialAccessTokenResponse.Data.Age
		if err1 != nil {
			appLog.Warn("_attemptOfficialRequest respBody tokenTimeout error", err1)
			*loginResult = clientService.LoginReply_LOGIN_THIRD_FAILED
			officialAccessTokenResponse.Success = false
		} else if err2 != nil{
			appLog.Warn("_attemptOfficialRequest respBody phone error", err2)
			*loginResult = clientService.LoginReply_LOGIN_THIRD_FAILED
			officialAccessTokenResponse.Success = false
		} else {
			data := map[string]interface{} {
				"age":      	uint32(age),
				"phone":		uint64(phone),
				//"birthday": 	uint32(birthday),
				//"isCertified": 	bool(isCertified),
			}
			otherJsonData, _err := json.Marshal(data)
			if _err != nil {
				appLog.Warn("_attemptOfficialRequest otherJsonData marshalIndent error", _err)
				*loginResult = clientService.LoginReply_LOGIN_THIRD_FAILED
				officialAccessTokenResponse.Success = false
			} else {
				self.accountType = clientService.AccountType_ACCOUNT_OFFICIAL
				self.userId = officialAccessTokenResponse.Data.UserInfoId
				self.accountName = officialAccessTokenResponse.Data.UserGameId
				self.loginToken = officialAccessTokenResponse.Data.NewToken
				self.tokenTimeout = uint32(tokenTimeout)
				self.otherJsonData = string(otherJsonData)
				officialAccessTokenResponse.Success = true
			}
		}
	}
	return officialAccessTokenResponse.Success
}

func (self *LoginClientService) _loginByOfficial(channelInfo *ChannelInfo, officialAccessToken *OfficialAccessToken, loginResult *clientService.LoginReply_LoginResult) (bool) {
	appLog.Info("_loginByOfficial: verify request")

	token := officialAccessToken.Token

	var reqHost string
	if value, ok := LoginConfig.Official["reqhost"]; ok {
		reqHost = value.(string)
	} else {
		appLog.Error("_loginByOfficial LoginConfig.Official[reqHost]")
		return false
	}

	var reqURI string
	if value, ok := LoginConfig.Official["requri"]; ok {
		reqURI = value.(string)
	} else {
		appLog.Error("_loginByOfficial LoginConfig.Official[reqURI]")
		return false
	}

	reqURL := reqHost + reqURI

	appLog.Info(fmt.Sprintf("_loginByOfficial reqURL: %s, token: %s", reqURL, token))

	return self._attemptOfficialRequest(reqURL, token, loginResult)
}

func (self *LoginClientService) LoginByThird(r *clientService.ThirdLogin) (*clientService.Void, error) {
	appLog.Info(fmt.Sprintf("LoginByThird: verify request: %s, %s", r.ChannelInfo, r.AccessToken))
	self.isReqLogin = true
	var err error

	var channelInfo ChannelInfo
	err = json.Unmarshal([]byte(r.ChannelInfo), &channelInfo)
	if err != nil {
		appLog.Warn(fmt.Sprintf("fails to unmarshal channelInfo: %s, err: %s", r.ChannelInfo, err.Error()))
		return nil, errors.New(fmt.Sprintf("fails to unmarshal channelInfo: %s", r.ChannelInfo))
	}

	var res bool = false
	var loginResult clientService.LoginReply_LoginResult = clientService.LoginReply_LOGIN_THIRD_FAILED
	if channelInfo.Id == uint32(clientService.ThirdLoginType_THIRD_LOGIN_TAPTAP) {
		var tapTapAccessToken TapTapAccessToken
		err := json.Unmarshal([]byte(r.AccessToken), &tapTapAccessToken)
		if err != nil {
			appLog.Warn(fmt.Sprintf("fails to unmarshal tapTapAccessToken: %s, err: %s", r.AccessToken, err.Error()))
			return nil, errors.New(fmt.Sprintf("fails to unmarshal tapTapAccessToken: %s", r.AccessToken))
		}
		res = self._loginByTapTap(&channelInfo, &tapTapAccessToken, &loginResult)
	} else if channelInfo.Id == uint32(clientService.ThirdLoginType_THIRD_LOGIN_OFFICIAL) {
		var officialAccessToken OfficialAccessToken
		err := json.Unmarshal([]byte(r.AccessToken), &officialAccessToken)
		if err != nil {
			appLog.Warn(fmt.Sprintf("fails to unmarshal officialAccessToken: %s, err: %s", r.AccessToken, err.Error()))
			return nil, errors.New(fmt.Sprintf("fails to unmarshal officialAccessToken: %s", r.AccessToken))
		}
		res = self._loginByOfficial(&channelInfo, &officialAccessToken, &loginResult)
	} else {
		appLog.Warn(fmt.Sprintf("unsupported channel id: %d", channelInfo.Id))
		return nil, errors.New(fmt.Sprintf("unsupported channel id: %d", channelInfo.Id))
	}

	if !res {
		reply := clientService.LoginReply{Result: loginResult, Token: self.loginToken, CentralServerId: LoginConfig.CentralServerId, ServerId: self.serverId, GameServerHost: self.gsHost, QueueServerHost: self.qsHost, TokenTimeout: self.tokenTimeout, Reserved: self.otherJsonData}
		self.GetClientEndPoint().(clientService.IGameClientInterface).OnLoginReply(&reply)
		appLog.Warn(fmt.Sprintf("loginByThird verify failed res : %d", loginResult))
		return nil, nil
	}
	appLog.Info(fmt.Sprintf("LoginByThird: verify success, accountType: %d, userId: %s, accountName: %s", self.accountType, self.userId, self.accountName))

	self.loginResult = clientService.LoginReply_LOGIN_SUCCESS
	self.channelId = channelInfo.Id
	self.app.addClient(self)

	self.onLoginSucess(self.accountType, self.accountName)

	err = self._replyLogin()

	if err != nil {
		self.app.removeClient(self)
		return nil, err
	}

	return nil, nil
}

// 回复登录
func (self *LoginClientService) _replyLogin() error {
	self.loginResult = clientService.LoginReply_LOGIN_SUCCESS
	err := self._replyLoginSuccess()
	return err
}

// 检查是否需要走验证码
func (self *LoginClientService) _checkNeedCaptcha() (error, bool) {
	if !self.isCaptchaValid {
		needCaptcha, forbidExpireTime := self._securityCheck()
		if needCaptcha || forbidExpireTime > 0 {
			err := self._replyCheckCaptcha(needCaptcha, forbidExpireTime, clientService.CaptchaType_CT_Login)
			return err, true
		}
	}
	return nil, false
}

// 检查是否需要验证码以及lock down cd time
func (self *LoginClientService) _securityCheck() (bool, int64) {
	//先看下是否有封禁
	appLog.Info("_securityCheck: check request, account name: ", self.accountName, ", account type: ", self.accountType)
	conn := self.app.redisPool.Get()
	defer conn.Close()
	captchaForbidKey := fmt.Sprintf("sclb_%v_%v", self.accountName, int32(self.accountType))
	value, err := redis.Int(conn.Do("ttl", captchaForbidKey))
	if err != nil {
		log := fmt.Sprintf("_securityCheck: Error in get ttl forbidden time, accountName: %v, accountType: %v", self.accountName, self.accountType)
		appLog.Error(log)
	}

	if value > 0 {
		//还在封禁时间内，不走验证码
		return false, int64(value)
	}

	//查下是否在验证成功cd有效期内
	captchaDataValidKey := fmt.Sprintf("sclv_%v_%v_%v", self.accountName, int32(self.accountType), int32(clientService.CaptchaType_CT_Login))
	value, err = redis.Int(conn.Do("get", captchaDataValidKey))
	//这里的error包含是redis没有数据的情况，这种就让玩家走验证好了
	if err != nil {
		//如果不是由于值为空返回的错误，那就是redis有问题了，放过玩家
		if err.Error() != "redigo: nil returned" {
			appLog.Errorf(fmt.Sprintf("_securityCheck: account name: %v, account type: %v, captcha type: %v, err: %v", self.accountName, self.accountType, clientService.CaptchaType_CT_Login, err.Error()))
			return false, 0
		}
	} else {
		//还在成功验证的cd有效期内, 不需要验证
		if value == 1 {
			return false, 0
		}
	}

	//检查上次是否有记录
	dataRecorddKey := fmt.Sprintf("sclr_%v_%v_%v", self.accountName, int32(self.accountType), int32(clientService.CaptchaType_CT_Login))
	_, err = redis.Int(conn.Do("get", dataRecorddKey))
	if err != nil {
		if err.Error() != "redigo: nil returned" {
			appLog.Errorf(fmt.Sprintf("_securityCheck: get data record key: %v, accountName: %v, accountType: %v, err: %v", dataRecorddKey, self.accountName, self.accountType, err.Error()))
		}
	} else {
		//上次有记录，让玩家继续验证
		return true, 0
	}

	//如果历史没有验证码记录, 检查是否需要验证码
	gameActionRateKey := fmt.Sprintf("%d", int32(clientService.CaptchaType_CT_Login))
	gameActionRateConfig, result := ConfigService.GetString("checkGameActionRate" + gameActionRateKey)
	if !result {
		appLog.Info("missing config checkGameActionRate")
		return false, 0
	}

	//解析数据
	data := make(map[string]int)
	err = json.Unmarshal([]byte(gameActionRateConfig), &data)
	if err != nil {
		//配置有问题，不验证，放过
		appLog.Info("unmarshal risk level data error: ", err.Error(), gameActionRateConfig)
		return false, 0
	}
	//当前没法取到中心服玩家的风险等级，给默认值0
	riskLevel := "0"
	riskLevelRate, ok := data[riskLevel]
	if !ok {
		//配置有问题，不验证，放过
		appLog.Info("get risk level rate data error: ", gameActionRateConfig)
		return false, 0
	}

	//小于100的需要随机下是否需要触发，等于100的必触发，等于0的不触发
	if riskLevelRate == 0 {
		return false, 0
	} else if riskLevelRate == 100 {
		//记录玩家的验证码策略
		_, err = redis.String(conn.Do("set", dataRecorddKey, 1))
		if err != nil {
			appLog.Errorf(fmt.Sprintf("_securityCheck: set data record key: %v, accountName: %v, accountType: %v, error: %v", dataRecorddKey, self.accountName, self.accountType, err.Error()))
		}
		return true, 0
	}

	rand.Seed(time.Now().UnixNano())
	randomValue := rand.Intn(riskLevelRate)
	if randomValue <= riskLevelRate {
		_, err = redis.String(conn.Do("set", dataRecorddKey, 1))
		if err != nil {
			appLog.Errorf(fmt.Sprintf("_securityCheck: set data record key: %v, accountName: %v, accountType: %v, error: %v", dataRecorddKey, self.accountName, self.accountType, err.Error()))
		}
		return true, 0
	}
	return false, 0
}

func (self *LoginClientService) _replyCaptchaValidate(isSuccess bool, captchaType clientService.CaptchaType) {
	reply := clientService.CaptchaValidateResponse{Success: isSuccess, CaptchaType: captchaType}
	_, err := self.GetClientEndPoint().(clientService.IGameClientInterface).OnCaptchaValidate(&reply)
	if err != nil {
		appLog.Error("_replyCaptchaValidate: reply captcha validate error, ", self.accountType, self.accountName, err.Error())
	}
}

func (self *LoginClientService) _calculateRecordType(isSuccess, isTimeout, isQPSLimit bool) int {
	if isQPSLimit {
		return QPSLIMIT
	}
	if isTimeout {
		return TIMEOUT
	}
	if isSuccess {
		return SUCCESS
	}
	return ERROR
}

func (self *LoginClientService) CaptchaValidate(r *clientService.CaptchaValidateRequest) (*clientService.Void, error) {
	appLog.Infof(fmt.Sprintf("CaptchaValidate: check request: %v, accountName: %v, accountType: %v ", r.CaptchaData, self.accountName, self.accountType))
	return nil, nil
}

func (self *LoginClientService) captchaLoginValidate(verifyResult, isTimeOut, isQPSLimit bool) {
	dataFailedKey := fmt.Sprintf("sclf_%v_%v_%v", self.accountName, int32(self.accountType), int32(clientService.CaptchaType_CT_Login))
	dataSuccessKey := fmt.Sprintf("scls_%v_%v_%v", self.accountName, int32(self.accountType), int32(clientService.CaptchaType_CT_Login))
	captchaDataValidKey := fmt.Sprintf("sclv_%v_%v_%v", self.accountName, int32(self.accountType), int32(clientService.CaptchaType_CT_Login))
	captchaForbidKey := fmt.Sprintf("sclb_%v_%v", self.accountName, int32(self.accountType))
	recordType := self._calculateRecordType(verifyResult, isTimeOut, isQPSLimit)
	conn := self.app.redisPool.Get()
	defer conn.Close()
	if verifyResult {
		appLog.Infof(fmt.Sprintf("captchaLoginValidate: Success in login captchaValidate, accountName: %v, accountType: %v", self.accountName, self.accountType))
		//成功了，删除记录
		dataRecorddKey := fmt.Sprintf("sclr_%v_%v_%v", self.accountName, int32(self.accountType), int32(clientService.CaptchaType_CT_Login))
		conn := self.app.redisPool.Get()
		defer conn.Close()
		_, err := conn.Do("del", dataRecorddKey)
		if err != nil {
			appLog.Errorf(fmt.Sprintf("CaptchaValidate: del data record key: %v, accountName: %v, accountType: %v", dataRecorddKey, self.accountName, self.accountType))
		}

		//验证成功清理掉次数
		_, err = conn.Do("del", dataFailedKey)
		if err != nil {
			appLog.Errorf(fmt.Sprintf("captchaLoginValidate: Error in captcha login validate 1, del failed count key: %v, accountName: %v, accountType: %v", dataFailedKey, self.accountName, self.accountType))
		}
		//增加验证成功的次数
		successCount := -1
		successCount, err = redis.Int(conn.Do("incr", dataSuccessKey))
		if err != nil {
			//服务器redis不行了，让玩家过去吧
			appLog.Errorf(fmt.Sprintf("captchaLoginValidate: Error in increasing login success count key: %v, accountName: %v, accountType: %v", dataSuccessKey, self.accountName, self.accountType))
		}
		//只记录有效数据
		if successCount > 0 {
			self.recordValidateLog("", self.accountName, int(self.accountType), -1, int(clientService.CaptchaType_CT_Login), 1, successCount, 0, recordType)
		}
		//设置玩家的成功cd时间
		captchaSuccessCDTime, ret := ConfigService.GetInt32("checkLoginCoolDown")
		if !ret {
			//配置读取失败，让玩家过去吧
			self._replyCaptchaResult(clientService.CaptchaType_CT_Login, true, 0, isTimeOut)
			appLog.Errorf(fmt.Sprintf("captchaLoginValidate: Error in reading checkLoginCoolDown config, accountName: %v, accountType: %v", self.accountName, self.accountType))
		}
		//记录玩家一段时间不用验证的状态
		expireCDTme := int64(captchaSuccessCDTime) * 60
		_, err = conn.Do("setex", captchaDataValidKey, expireCDTme, 1)
		if err != nil {
			appLog.Errorf(fmt.Sprintf("captchaAwardValidate: Error in captcha login validate, set expire time failed 1, accountName: %v, accountType: %v", self.accountName, self.accountType))
		}

		self._replyCaptchaResult(clientService.CaptchaType_CT_Login, true, 0, isTimeOut)
		return
	}

	//验证失败清理累计成功次数
	_, err := conn.Do("del", dataSuccessKey)
	if err != nil {
		appLog.Errorf(fmt.Sprintf("captchaLoginValidate: Error in captcha login validate 1, del login success count key: %v, accountName: %v, accountType: %v", dataSuccessKey, self.accountName, self.accountType))
	}

	//累计连续失败次数
	failedCount, err := redis.Int(conn.Do("incr", dataFailedKey))
	if err != nil {
		//服务器redis不行了，让玩家过去吧
		self._replyCaptchaResult(clientService.CaptchaType_CT_Login, true, 0, isTimeOut)
		appLog.Errorf(fmt.Sprintf("captchaLoginValidate: Error in increasing login failed count key: %v, accountName: %v, accountType: %v", dataFailedKey, self.accountName, self.accountType))
		return
	}
	loginAllowNum, ret := ConfigService.GetInt32("checkNoPunishmentNum")
	if !ret {
		//配置读取失败，让玩家过去吧
		self._replyCaptchaResult(clientService.CaptchaType_CT_Login, true, 0, isTimeOut)
		appLog.Errorf(fmt.Sprintf("captchaLoginValidate: Error in reading checkNoPunishmentNum config, accountName: %v, accountType: %v", self.accountName, self.accountType))
		return
	}

	loginForbidenTime, ret := ConfigService.GetInt32("checkFailLoginForbiddenTime")
	if !ret {
		//配置读取失败，让玩家过去吧
		self._replyCaptchaResult(clientService.CaptchaType_CT_Login, true, 0, isTimeOut)
		appLog.Errorf(fmt.Sprintf("captchaLoginValidate: Error in reading checkFailLoginForbiddenTime config, accountName: %v, accountType: %v", self.accountName, self.accountType))
		return
	}

	forbidLimitTime, ret := ConfigService.GetInt32("checkLoginForbiddenTimeLimit")
	if !ret {
		//配置读取失败，让玩家过去吧
		self._replyCaptchaResult(clientService.CaptchaType_CT_Login, true, 0, isTimeOut)
		appLog.Errorf(fmt.Sprintf("captchaLoginValidate: Error in reading checkLoginForbiddenTimeLimit config, accountName: %v, accountType: %v", self.accountName, self.accountType))
		return
	}

	//超过配置的登录验证失败次数了
	if int32(failedCount) > loginAllowNum {
		//根据公式计算封禁截止时间
		forbidSeconds := int64(float64(loginForbidenTime) * 60 * math.Pow(2, float64(failedCount-int(loginForbidenTime))))
		//这里有最大的禁止时间限制, 一旦超出，用限制的时间
		forbidLimitTimeSeconds := int64(forbidLimitTime) * 60
		if forbidSeconds > forbidLimitTimeSeconds {
			forbidSeconds = forbidLimitTimeSeconds
		}

		//开启玩家验证码封禁
		_, err = conn.Do("setex", captchaForbidKey, forbidSeconds, 1)
		if err != nil {
			appLog.Errorf(fmt.Sprintf("captchaLoginValidate: Error in captcha login validate, set expire time failed 0, accountName: %v, accountType: %v", self.accountName, self.accountType))
		}

		//记录失败封禁后次数
		self.recordValidateLog("", self.accountName, int(self.accountType), -1, int(clientService.CaptchaType_CT_Login), 0, 0, failedCount, recordType)
		self._replyCaptchaResult(clientService.CaptchaType_CT_Login, false, forbidSeconds, isTimeOut)
		return
	}
	self.recordValidateLog("", self.accountName, int(self.accountType), -1, int(clientService.CaptchaType_CT_Login), 0, 0, failedCount, recordType)
	//还在允许验证失败的时机，继续弹
	self._replyCaptchaResult(clientService.CaptchaType_CT_Login, false, 0, isTimeOut)
}

func (self *LoginClientService) _replyCaptchaResult(captchaType clientService.CaptchaType, isValid bool, forbiddenTime int64, isTimeout bool) {
	self.isCaptchaValid = isValid
	self._replyCaptchaValidate(isValid, captchaType)
	//验证码有效
	if isValid {
		self.loginResult = clientService.LoginReply_LOGIN_SUCCESS
		self._replyLoginSuccess()
	} else {
		// 如果是超时，仅仅只是记录数据，不做再次弹出的验证
		if isTimeout {
			return
		}
		//验证码无效，看是否封禁时间
		if forbiddenTime > 0 {
			//有封禁时间，不弹验证码，给封禁时间
			self._replyCheckCaptcha(false, forbiddenTime, captchaType)
		} else {
			//没有封禁时间，弹验证码
			self._replyCheckCaptcha(true, 0, captchaType)
		}
	}
}

func (self *LoginClientService) recordValidateLog(name string, accountName string, accountType, riskLevel, checkType, checkResult, successTimes, failureTimes, recordType int) {
	elpasedTime := time.Now().UnixMilli() - self.captchaBeginTime
	appLog.Infof(fmt.Sprintf("yidun_captcha_check_log: clientService: %v, %v, %v, %v, %v, %v, %v, %v, %v, %v", name, accountName, accountType, riskLevel, checkType, checkResult, successTimes, failureTimes, recordType, elpasedTime))
	//上抛日志
	data := make(map[string]interface{})
	data["server"] = self.serverId
	data["log_id"] = "yidun_captcha_check_log"
	data["log_timestamp"] = time.Now().Unix()
	data["role_id"] = -1
	data["user_name"] = ""
	data["account_name"] = accountName
	data["account_type"] = accountType
	data["risk_level"] = -1
	data["captcha_type"] = checkType
	data["check_result"] = checkResult
	data["success_times"] = successTimes
	data["failure_times"] = failureTimes
	data["reason_type"] = recordType
	data["elapsed_time"] = elpasedTime

	_, err := json.Marshal(&data)
	if err != nil {
		appLog.Errorf(fmt.Sprintf("recordValidateLog: marshal json data failed, accountName: %v, accountType: %v, error: %v", self.accountName, self.accountType, err.Error()))
	} else {
		//记录到syslog
		//logrus.Infoln(string(d))
	}
}
