package adminApp

import (
	gsmanager "centralService/src/adminServer/adminProto/gsmanager"
	webService "centralService/src/adminServer/adminProto/webservice"
	"centralService/src/appLog"
	"centralService/src/trpc"
	"errors"
	"fmt"

	"github.com/google/uuid"
)

// AdminApp给游戏服提供的接口
type GameServerService struct {
	*trpc.ServerEndPoint
	app      *AdminApp
	serverId uint32
	compId   uint32
	status   int8
}

func (self *GameServerService) RegisterServer(in *gsmanager.ServerInfoMessage) (*gsmanager.Void, error) {
	err := self.app.doRegisterServer(in.ServerId, in.CompId, in.ServerName, self)
	if err != nil {
		return nil, err
	}
	self.serverId = in.ServerId
	self.compId = in.CompId
	return nil, nil
}

func (self *GameServerService) ReplyCommand(result *gsmanager.CommandResult) (*gsmanager.Void, error) {
	cmdUUID, err := uuid.FromBytes(result.Uuid)
	if err != nil {
		appLog.Errorf("decode uuid error: %v\n", err)
		return nil, err
	}

	gameServer := self.app.GetGameServer(self.serverId, self.compId)
	if gameServer != nil {
		gameServer.rwLockCommand.Lock()
		defer gameServer.rwLockCommand.Unlock()
		if resultChan, ok := gameServer.PendingCommands[cmdUUID.String()]; ok {
			resultChan <- &webService.CommandResult{ResultCode: result.ResultCode, Desc: result.Result}
			delete(gameServer.PendingCommands, cmdUUID.String())
		} else {
			return nil, errors.New(fmt.Sprintf("invalid command uuid: %v %s %s %d", cmdUUID, result.Account, result.Result, result.ResultCode))
		}
	}

	return &(gsmanager.Void{}), nil
}

func (self *GameServerService) ReplyHttpCommand(resp *gsmanager.HttpAPICommandResponse) (*gsmanager.Void, error) {
	gameServer := self.app.GetGameServer(self.serverId, self.compId)
	if gameServer != nil {
		cmdUUIDStr := resp.Uuid
		appLog.Debugf("ReplyIDIPCommand uuid: %s\n", cmdUUIDStr)

		var ok2 bool
		gameServer.rwLockHttpCommand.RLock()
		defer gameServer.rwLockHttpCommand.RUnlock()
		responseChan, ok := gameServer.PendingHttpCommands[cmdUUIDStr]
		if ok {
			if len(responseChan) > 0 {
				appLog.Errorf("write to blocked channel: %s %d %d\n", cmdUUIDStr, self.serverId, self.compId)
				return &(gsmanager.Void{}), nil
			}
			responseChan <- resp
		} else {
			gameServer.rwLockAllHtpCmds.RLock()
			defer gameServer.rwLockAllHtpCmds.RUnlock()
			responseChan, ok2 = gameServer.PendingAllHttpCmds[cmdUUIDStr]
			if ok2 {
				responseChan <- resp
			}
		}
		self.app.rwLockPendingAccountCommands.RLock()
		defer self.app.rwLockPendingAccountCommands.RUnlock()
		responseChan, ok1 := self.app.PendingAccountCommands[cmdUUIDStr]
		if ok1 {
			if resp.Result == HTTP_CMD_OK {
				if len(responseChan) > 0 {
					appLog.Errorf("write to blocked channel: %d\n", self.serverId)
					return &(gsmanager.Void{}), nil
				}
				responseChan <- resp
			}

		}

		if !(ok || ok1 || ok2) {
			appLog.Errorf("ReplyIDIPCommand invalid seqId %d %s\n", self.serverId, cmdUUIDStr)
			return &(gsmanager.Void{}), nil
		}
	}
	return &(gsmanager.Void{}), nil
}

func (self *GameServerService) ActiveTick(in *gsmanager.Void) (*gsmanager.Void, error) {
	gameServer := self.app.GetGameServer(self.serverId, self.compId)

	if gameServer != nil {
		_, err := gameServer.AdminService.GetClientEndPoint().(gsmanager.IGameServerInterface).ActiveTickCallback(&gsmanager.Void{})
		if err != nil {
			return nil, err
		}
	}
	return nil, nil
}

func (self *GameServerService) OnLoseConnection() {
	appLog.Info("OnLoseConnection", self.serverId)
	self.status = AdminServiceStatus_Disconnected
	self.app.unRegisterServer(self)
}
