package CentralLogin

import (
	"centralService/src/appLog"
	"centralService/src/common"
	"centralService/src/trpc"
	sqllib "database/sql"
	"errors"
	"fmt"
	"time"

	"github.com/garyburd/redigo/redis"

	gameServerService "centralService/src/centralLogin/centralLoginApp/gameServerService"
)

// 给游戏服务器提供的接口
type GameServerService struct {
	*trpc.ServerEndPoint
	app       *CentralLoginApp
	hostId    uint32
	onlineNum uint32
}

func (self *GameServerService) OnLoseConnection() {
	self.app.removeGameServer(self)
}

func (self *GameServerService) DoVerifyLogin(in *gameServerService.VerifyAccountRequest) gameServerService.VerifyAccountReply_VerifyResult {
	conn := self.app.redisPool.Get()
	defer conn.Close()

	isLock, err := redis.Int(conn.Do("get", self.LockLoginSwitchServerKey(in.AccountName)))

	if err != nil {
	} else {
		if isLock == 1 {
			appLog.Debug("VerifyLogin get lockLogin ret", isLock)
			return gameServerService.VerifyAccountReply_VERIFY_ACCOUNT_FAIL
		}
	}

	if in.HostId != ServerListCfg.GetUint32("auditServerId") {
		_, err := redis.String(conn.Do("set", common.LAST_SERVER_ID+in.AccountName, in.HostId))
		if err != nil {
			appLog.Error("VerifyLogin set lastServerId failed", in.AccountName, err.Error())
		}
	}

	value, err := redis.Int(conn.Do("setnx", "AccountLogin_"+in.AccountName, in.HostId))
	if err != nil {
		appLog.Error("VerifyLogin setnx failed", in.AccountName, err.Error())
	} else {
		if value == 0 {
			lastServerId, err := redis.Int(conn.Do("get", "AccountLogin_"+in.AccountName))
			if err != nil {
				appLog.Error("VerifyLogin get failed", in.AccountName, err.Error())
			} else {
				if lastServerId != 0 {
					accountType, err := redis.Int(conn.Do("get", "AccountLoginType_"+in.AccountName))
					if err != nil {
						appLog.Error("VerifyLogin get AccountLoginType_ failed", in.AccountName, err.Error())
						accountType = 0
					}
					if uint32(accountType) != in.AccountType || uint32(lastServerId) != in.HostId {
						gameServer := self.app.getGameServer(uint32(lastServerId))
						if gameServer != nil {
							kickAccountInfo := gameServerService.KickAccountVal{AccountType: uint32(accountType), AccountName: in.AccountName, KickReason: gameServerService.KickAccountVal_LOGIN_VERIFY_FAIL}
							_, err := gameServer.GetClientEndPoint().(gameServerService.IGameServerInterface).OnKickAccount(&kickAccountInfo)
							if err != nil {
								appLog.Error("VerifyLogin->OnKickAccount failed: ", accountType, in.AccountName, lastServerId, in.HostId)
							}
						} else {
							appLog.Error("VerifyLogin getGameServer failed", lastServerId)
						}

						_, err := redis.String(conn.Do("set", "AccountLogin_"+in.AccountName, in.HostId))
						if err != nil {
							appLog.Error("VerifyLogin set AccountLogin_ failed", in.AccountName)
						}
					}
				}
			}
		}
	}

	_, err = redis.String(conn.Do("set", "AccountLoginType_"+in.AccountName, in.AccountType))
	if err != nil {
		appLog.Error("VerifyLogin set AccountLoginType_ failed", in.AccountName)
	}

	return gameServerService.VerifyAccountReply_VERIFY_ACCOUNT_OK
}

func (self *GameServerService) VerifyLogin(in *gameServerService.VerifyAccountRequest) (*gameServerService.Void, error) {
	res := gameServerService.VerifyAccountReply_VERIFY_ACCOUNT_UNKNOWN
	isLogin, channelId := self.app.checkClientLogin(self, in.AccountType, in.AccountName, in.Token)
	if !isLogin {
		res = gameServerService.VerifyAccountReply_VERIFY_ACCOUNT_FAIL
		appLog.Error("verifyLogin failed: ", in.AccountType, in.AccountName, in.Token)
	} else {
		res = self.DoVerifyLogin(in)
	}

	var banAccountTime int64 = 0
	var banPostTime int64 = 0
	var banAccountReason = ""
	var banPostReason = ""
	if res == gameServerService.VerifyAccountReply_VERIFY_ACCOUNT_OK {
		sql := "select banAccountTime, banAccountReason, banPostTime, banPostReason from account where accountType=? and accountName=?"
		row := self.app.db.QueryRow(sql, in.AccountType, in.AccountName)
		err := row.Scan(&banAccountTime, &banAccountReason, &banPostTime, &banPostReason)

		if err == sqllib.ErrNoRows {
			appLog.Error("verifyLogin ErrNoRows: ", in.AccountType, in.AccountName, in.Token)
		} else if err != nil {
			appLog.Error("verifyLogin scan banAccountTime  banPostTime error: ", in.AccountType, in.AccountName, err)
		}
	}

	appLog.Info(fmt.Sprintf("verifyLogin: res=%d, AccountType=%d, AccountName=%s, Token=%s, channelId=%d", res, in.AccountType, in.AccountName, in.Token, channelId))
	result := gameServerService.VerifyAccountReply{
		Result: res, AccountName: in.AccountName,
		AccountType:      in.AccountType,
		ChannelId:        channelId,
		BanAccountTime:   banAccountTime,
		BanPostTime:      banPostTime,
		BanAccountReason: banAccountReason,
		BanPostReason:    banPostReason}
	self.Client.(*gameServerService.GameServerClient).OnVerifyLogin(&result)

	return nil, nil
}

func (self *GameServerService) RegisterServer(in *gameServerService.GameServerInfo) (*gameServerService.Void, error) {
	appLog.Debug("register server:", in.HostId)

	server := self.app.getGameServer(in.HostId)
	if server != nil {
		return nil, errors.New(fmt.Sprint("server is already registered: ", in.HostId))
	}

	if in.HostId == 0 {
		return nil, errors.New(fmt.Sprint("invalid hostId: ", in.HostId))
	}

	self.hostId = in.HostId
	self.onlineNum = in.OnlineNum

	self.app.addGameServer(self)
	return nil, nil
}

func (self *GameServerService) UpdateServerInfo(in *gameServerService.GameServerInfo) (*gameServerService.Void, error) {
	self.app.serversLock.Lock()
	defer self.app.serversLock.Unlock()
	self.onlineNum = in.OnlineNum
	return nil, nil
}

func (self *GameServerService) OnCreateCharacter(in *gameServerService.NewCharacterInfo) (*gameServerService.Void, error) {
	appLog.Info("create character:", in.AccountType, in.AccountName, in.Name, in.HostId)
	parentIdSql := "select id from account where accountType=? and accountName=?"
	row := self.app.db.QueryRow(parentIdSql, in.AccountType, in.AccountName)

	var parentID uint64
	err := row.Scan(&parentID)
	if err != nil {
		appLog.Error("get parentID err: ", in.AccountName, in.AccountType, in.GbId, in.Name, err.Error())
		return nil, nil
	}

	sql := "insert into account_characters (parentID, hostId, gbId, name, level, school, gens, sex, tLastLogin) value (?, ?, ?, ?, ?, ?, ?, ?, ?)"
	_, err = self.app.db.Exec(sql, parentID, in.HostId, in.GbId, in.Name, in.Level, in.School, in.Gens, in.Sex, uint32(time.Now().Unix()))
	if err != nil {
		appLog.Error("write character err: ", in.AccountName, in.AccountType, in.GbId, in.Name, err.Error())
		return nil, nil
	}
	return nil, nil
}

func (self *GameServerService) UpdateCharacter(in *gameServerService.UpdateCharacterInfo) (*gameServerService.Void, error) {
	appLog.Debug("update character:", in.Delete, in.GbId, in.Name, in.Sex)
	if in.Delete {
		sql := "delete from account_characters where gbId=?"
		_, err := self.app.db.Exec(sql, in.GbId)
		if err != nil {
			appLog.Error("delete characters err: ", in.GbId, err.Error())
		}
	} else {
		sql := "update account_characters set name=?, level=?, school=?, sex=?, tLastLogin=? where gbId=?"
		_, err := self.app.db.Exec(sql, in.Name, in.Level, in.School, in.Sex, in.TLastLogin, in.GbId)
		if err != nil {
			appLog.Error("update characters err: ", in.GbId, in.Name, err.Error())
		}
	}

	return nil, nil
}

func (self *GameServerService) OnLoginComplete(in *gameServerService.AccountVal) (*gameServerService.Void, error) {
	client := self.app.getClient(in.AccountType, in.AccountName)
	if client != nil {
		appLog.Debug("login complete, close connectoin:", in.AccountType, in.AccountName, client.loginResult)
		client.GetRpcChannel().Disconnect()
	}
	return nil, nil
}

func (self *GameServerService) OnAccountOffline(in *gameServerService.AccountOfflineVal) (*gameServerService.Void, error) {
	appLog.Info("OnAccountOffline:", in.AccountName, in.AccountType, in.HostId)
	conn := self.app.redisPool.Get()
	defer conn.Close()
	lastServerId, err := redis.Int(conn.Do("get", "AccountLogin_"+in.AccountName))
	if err != nil {
		appLog.Error("OnAccountOffline get failed", in.AccountName, err.Error())
	} else {
		if lastServerId == int(in.HostId) {
			accountType, err := redis.Int(conn.Do("get", "AccountLoginType_"+in.AccountName))
			if err != nil {
				appLog.Error("OnAccountOffline get AccountLoginType_ failed", in.AccountName, err.Error())
			} else {
				if accountType == int(in.AccountType) {
					ret, err := redis.Int(conn.Do("del", "AccountLogin_"+in.AccountName))
					if err != nil || ret != 1 {
						appLog.Error("OnAccountOffline del AccountLogin_ failed", in.AccountName)
					}

					ret, err = redis.Int(conn.Do("del", "AccountLoginType_"+in.AccountName))
					if err != nil || ret != 1 {
						appLog.Error("OnAccountOffline del AccountLoginType_ failed", in.AccountName)
					}
				}
			}
		}
	}

	return nil, nil
}

func (self *GameServerService) ActiveTick(in *gameServerService.Void) (*gameServerService.Void, error) {
	_, err := self.GetClientEndPoint().(*gameServerService.GameServerClient).ActiveTickCallback(&gameServerService.Void{})
	return nil, err
}

func (self *GameServerService) LockLoginSwitchServerKey(accountName string) string {
	return "lockLogin_" + accountName
}

func (self *GameServerService) LockLoginSwitchServer(in *gameServerService.LockLoginSwitchServerVal) (*gameServerService.Void, error) {
	conn := self.app.redisPool.Get()
	defer conn.Close()
	_, err := conn.Do("set", self.LockLoginSwitchServerKey(in.AccountName), 1)
	if err != nil {
		appLog.Error("LockLoginSwitchServer set failed", in.AccountName, err.Error())
		return nil, err
	}

	self.Client.(*gameServerService.GameServerClient).OnLockedLogin(in)

	return nil, nil
}

func (self *GameServerService) UnlockLoginSwitchServer(in *gameServerService.UnlockLoginSwitchServerVal) (*gameServerService.Void, error) {
	conn := self.app.redisPool.Get()
	defer conn.Close()
	_, err := conn.Do("del", self.LockLoginSwitchServerKey(in.AccountName))
	if err != nil {
		appLog.Error("UnlockLoginSwitchServer del failed", in.AccountName, err.Error())
		return nil, err
	}

	return nil, nil
}
