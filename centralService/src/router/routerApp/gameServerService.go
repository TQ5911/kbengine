package Router

import (
	"centralService/src/appLog"
	"centralService/src/router/routerApp/gameServerService"
	"centralService/src/router/routerApp/routerCluster"
	"centralService/src/trpc"
	"errors"
	"fmt"
)

// 给游戏服务器提供的接口
type GameServerService struct {
	*trpc.ServerEndPoint
	app         *RouterApp
	serverId    uint32
	componentId uint32
}

func (self *GameServerService) OnLoseConnection() {
	remoteAddr := self.GetRpcChannel().GetRemoteAddr()
	appLog.Error("lose connection from:", remoteAddr.String(), "serverId:", self.serverId, "componentId:", self.componentId)
	self.app.removeGameServer(self)
}

func (self *GameServerService) RegisterBaseapp(in *gameServerService.BaseAppInfo) (*gameServerService.Void, error) {
	appLog.Info("register baseapp:", in.ServerId, in.ComponentId)
	server := self.app.getGameServer(in.ServerId, in.ComponentId)
	if server != nil {
		return nil, errors.New(fmt.Sprint("baseapp is already registered: ", in.ServerId, in.ComponentId))
	}

	if in.ServerId == 0 {
		return nil, errors.New(fmt.Sprint("invalid ServerId: ", in.ServerId))
	}

	if in.ComponentId == 0 {
		return nil, errors.New(fmt.Sprint("invalid ComponentId: ", in.ComponentId))
	}

	self.serverId = in.ServerId
	self.componentId = in.ComponentId

	self.app.addGameServer(self)
	return nil, nil
}

func (self *GameServerService) DoOnOthersBase(in *gameServerService.OthersBaseRequest) (*gameServerService.Void, error) {
	appLog.Debug("doOnOthersBase:", in.ServerId, in.DstServerId, in.ComponentId, in.MemoryStream)

	//记录流量统计：按来源服务器和目标服务器分别累加请求数和字节数
	self.app.recordTraffic(in.ServerId, in.DstServerId, uint64(len(in.MemoryStream)))

	// 1) 本地优先
	if otherBaseApp := self.app.getOtherBaseApp(in.DstServerId, in.ComponentId); otherBaseApp != nil {
		othersBaseRequest := gameServerService.OthersBaseRequest{
			ServerId:     in.ServerId,
			DstServerId:  in.DstServerId,
			ComponentId:  in.ComponentId,
			MemoryStream: in.MemoryStream,
		}
		otherBaseApp.GetClientEndPoint().(*gameServerService.GameServerClient).OnRemoteCallFromOthersBase(&othersBaseRequest)
		return nil, nil
	}

	// 2) 集群路由：查全局表，目标可能注册在另一个 router 上
	if rid, ok := self.app.lookupClusterRoute(in.DstServerId); ok && rid != RouterConfig.RouterId {
		req := &routerCluster.ClusterForwardRequest{
			DstServerId:    in.DstServerId,
			DstComponentId: in.ComponentId,
			SrcServerId:    in.ServerId,
			SrcComponentId: in.ComponentId,
			MemoryStream:   in.MemoryStream,
		}
		if err := self.app.forwardToRemoteRouter(rid, req); err != nil {
			appLog.Errorf("cluster forward to routerId=%d failed: %s", rid, err.Error())
		} else {
			return nil, nil
		}
	}

	appLog.Error("cannot find other baseapp", in.ServerId, in.ComponentId, in.DstServerId, in.ComponentId)
	return nil, nil
}

func (self *GameServerService) ActiveTick(in *gameServerService.Void) (*gameServerService.Void, error) {
	_, err := self.GetClientEndPoint().(*gameServerService.GameServerClient).ActiveTickCallback(&gameServerService.Void{})
	return nil, err
}

func (self *GameServerService) GetTrafficStats(in *gameServerService.Void) (*gameServerService.Void, error) {
	stats := self.app.getTrafficStatsSnapshot()
	_, err := self.GetClientEndPoint().(*gameServerService.GameServerClient).GetTrafficStatsCallback(stats)
	return nil, err
}

func (self *GameServerService) ResetTrafficStats(in *gameServerService.Void) (*gameServerService.Void, error) {
	self.app.resetTrafficStats()
	_, err := self.GetClientEndPoint().(*gameServerService.GameServerClient).ResetTrafficStatsCallback(&gameServerService.ResetTrafficStatsResult{Success: true})
	return nil, err
}
