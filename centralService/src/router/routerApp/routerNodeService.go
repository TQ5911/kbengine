package Router

import (
	"centralService/src/appLog"
	"centralService/src/router/routerApp/gameServerService"
	"centralService/src/router/routerApp/routerCluster"
	"centralService/src/trpc"
	"time"
)

type routerNodeService struct {
	*trpc.ServerEndPoint
	app           *RouterApp
	incomingState *RouterNodeState
}

func (self *routerNodeService) OnLoseConnection() {
	if self.app == nil {
		return
	}
	addr := self.GetRpcChannel().GetRemoteAddr().String()
	appLog.Warnf("routerCluster: lose connection from %s", addr)
	if self.app.clusterTopology != nil {
		self.app.clusterTopology.RemoveByAddr(addr)
	}
}

// ForwardToGameServer: 其他 router 节点把跨节点消息转发过来，要求本节点转交给
// (dstServerId, dstComponentId) 对应的游戏服
// 注: trpc 框架不把 handler 返回值真正回写到对端, 这里所有"未投递"原因改记日志, 返回 Void。
func (self *routerNodeService) ForwardToGameServer(in *routerCluster.ClusterForwardRequest) (*routerCluster.Void, error) {
	appLog.Debug("ForwardToGameServer:", in.SrcServerId, in.DstServerId, in.DstComponentId, in.MemoryStream)
	if self.app == nil {
		appLog.Warn("routerCluster: forwardToGameServer: app nil")
		return &routerCluster.Void{}, nil
	}
	if in == nil {
		appLog.Warn("routerCluster: forwardToGameServer: nil request")
		return &routerCluster.Void{}, nil
	}

	dst := self.app.getOtherBaseApp(in.DstServerId, in.DstComponentId)
	if dst == nil {
		appLog.Errorf("routerCluster: cluster forward miss, dst sid=%d cid=%d from src sid=%d cid=%d",
			in.DstServerId, in.DstComponentId, in.SrcServerId, in.SrcComponentId)
		return &routerCluster.Void{}, nil
	}

	gameClient := dst.GetClientEndPoint().(*gameServerService.GameServerClient)
	othersReq := &gameServerService.OthersBaseRequest{
		ServerId:     in.SrcServerId,
		DstServerId:  in.DstServerId,
		ComponentId:  in.DstComponentId,
		MemoryStream: in.MemoryStream,
	}
	if _, err := gameClient.OnRemoteCallFromOthersBase(othersReq); err != nil {
		appLog.Errorf("routerCluster: forward to game server failed, sid=%d cid=%d err=%s",
			in.DstServerId, in.DstComponentId, err.Error())
		return &routerCluster.Void{}, nil
	}
	return &routerCluster.Void{}, nil
}

// Ping: 链路活性探测。
// - 由小 ID 端发起；附带 fromRouterId 让大 ID 端登记对端节点
// - 大 ID 端收到后调用 topology.RegisterByPing 把对端加入 addr 表
// - 大 ID 端再以 request 方式 (client.Pong) 回一帧 pong, 让对端 (小 ID)
//   RpcChannel 读循环收到一帧后重置 20s 读超时
func (self *routerNodeService) Ping(in *routerCluster.ClusterPing) (*routerCluster.Void, error) {
	if self.app != nil && self.app.clusterTopology != nil && in != nil && in.FromRouterId != 0 {
		addr := self.GetRpcChannel().GetRemoteAddr().String()
		self.app.clusterTopology.RegisterByPing(in.FromRouterId, addr)
		if self.incomingState != nil && self.incomingState.client != nil {
			if _, perr := self.incomingState.client.Pong(&routerCluster.ClusterPong{
				FromRouterId: RouterConfig.RouterId,
				Timestamp:    uint64(time.Now().UnixMilli()),
			}); perr != nil {
				appLog.Warnf("routerCluster: pong-back to routerId=%d failed: %s", in.FromRouterId, perr.Error())
			}
		}
	}
	return &routerCluster.Void{}, nil
}

// Pong: 对端 (大 ID) 回过来的链路活性帧。
//   - 这一帧的到达本身已经把本端 (小 ID) RpcChannel 读循环的 20s deadline 刷新过;
//   - handler 不再回写, 避免形成 ping<->pong 的无限循环;
//   - 内容仅用于诊断, 不做拓扑变更 (小 ID 端的 app == nil, RegisterByPing 也不会跑)。
func (self *routerNodeService) Pong(in *routerCluster.ClusterPong) (*routerCluster.Void, error) {
	if in != nil {
		appLog.Debugf("routerCluster: pong received from routerId=%d ts=%d", in.FromRouterId, in.Timestamp)
	}
	return &routerCluster.Void{}, nil
}
