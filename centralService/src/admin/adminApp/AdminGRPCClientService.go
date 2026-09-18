package adminApp

import (
	gsmanager "centralService/src/admin/adminProto/gsmanager"
	webService "centralService/src/admin/adminProto/webservice"
	"centralService/src/appLog"
	"context"
	"errors"
	"fmt"
	"time"

	"github.com/google/uuid"
)

// AdminApp给GPRC客户端提供的接口
type GRPCAPIService struct {
	app *AdminApp
}

func (self *GRPCAPIService) DoCommand(ctx context.Context, info *webService.CommandInfo) (*webService.CommandResult, error) {
	appLog.Debug("DoCommand:", info.Acount, info.ServerId, info.Command)
	resultChan := make(chan *webService.CommandResult, 1)
	cmdUUID := uuid.New()

	gameServer := self.app.GetGameServer(info.ServerId, 0)
	if gameServer != nil {
		cmd := &gsmanager.CommandInfo{Uuid: cmdUUID[:], Account: info.Acount, Command: info.Command}
		gameServer.AddPendingCommands(cmdUUID.String(), resultChan)

		_, err := gameServer.AdminService.GetClientEndPoint().(gsmanager.IGameServerInterface).DoCommand(cmd)
		if err != nil {
			return nil, err
		}
	} else {
		return nil, errors.New(fmt.Sprintf("server[%d] does not exist!", info.ServerId))
	}

	select {
	case result := <-resultChan:
		appLog.Debugf("user: %s, command:%s result:%s\n", info.Acount, info.Command, result.Desc)
		return result, nil
	case <-time.After(10 * time.Second):
		gameServer.RemovePendingCommands(cmdUUID.String())
		return nil, errors.New("do gm command timeout")
	}
}

func (self *GRPCAPIService) ListServers(ctx context.Context, void *webService.Void) (*webService.ServerList, error) {
	self.app.rwLockGameServers.RLock()
	defer self.app.rwLockGameServers.RUnlock()

	servers := make([]*webService.ServerInfo, 0, 20)
	for serverId, _ := range self.app.gameServers {
		gameServer := self.app.GetGameServer(serverId, 0)
		servers = append(servers, &webService.ServerInfo{ServerId: serverId, ServerName: gameServer.serverName})
	}
	appLog.Debug("ListServers: serverNum=", len(servers))

	return &webService.ServerList{Servers: servers}, nil
}

func (self *GRPCAPIService) ListComponents(ctx context.Context, req *webService.ListCompRequest) (*webService.ComponentList, error) {
	compListReply := make([]*webService.ComponentInfo, 0, 10)
	gameServer := self.app.GetGameServer(req.ServerId, 0)
	if gameServer != nil {
		gameServer.rwLockComps.RLock()
		defer gameServer.rwLockComps.RUnlock()
		for compType, compList := range *gameServer.comps {
			for _, compVal := range compList {
				compInfo := webService.ComponentInfo{
					CompType:   uint32(compType),
					GroupOrder: compVal.groupOrder,
				}
				compListReply = append(compListReply, &compInfo)
			}
		}
	}

	return &webService.ComponentList{Comps: compListReply}, nil
}

func (self *GRPCAPIService) Runscript(ctx context.Context, info *webService.ScriptInfo) (*webService.ScriptResultList, error) {
	appLog.Debug("Runscript")
	resultList := make([]*webService.ScriptResult, 0, 10)

	gameServer := self.app.GetGameServer(info.ServerId, 0)
	if gameServer != nil {
		gameServer.rwLockComps.RLock()
		defer gameServer.rwLockComps.RUnlock()
		_components := *gameServer.comps
		if compList, ok := _components[CompType(info.CompType)]; ok {
			for _, compVal := range compList {
				if info.CompGroupOrder == 0 || info.CompGroupOrder == compVal.groupOrder {
					result := runScript(compVal, info.Script)

					scripResult := webService.ScriptResult{
						CompInfo: &webService.ComponentInfo{
							CompType:   info.CompType,
							GroupOrder: compVal.groupOrder,
						},
						Result: result,
					}
					resultList = append(resultList, &scripResult)
				}
			}
		}
	}

	return &webService.ScriptResultList{Results: resultList}, nil
}
