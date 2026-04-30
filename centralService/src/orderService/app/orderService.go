package app

import (
	service "centralService/src/orderService/service"
	"centralService/src/trpc"
)

// 给游戏服务器提供的接口
type OrderService struct {
	*trpc.ServerEndPoint
	app      *OrderApp
	serverId uint32
	compId   uint32
	status   int8
}

func (gs *OrderService) OnLoseConnection() {
	gs.status = ServiceStatus_Disconnected
	gs.app.unRegisterServer(gs)
}

func (gs *OrderService) RegisterServer(in *service.ServerInfoMessage) (*service.Void, error) {
	err := gs.app.doRegisterServer(in.ServerId, in.CompId, in.ServerName, gs)
	if err != nil {
		return nil, err
	}
	gs.serverId = in.ServerId
	gs.compId = in.CompId
	return nil, nil
}

func (gs *OrderService) ActiveTick(_ *service.Void) (*service.Void, error) {
	_, err := gs.GetClientEndPoint().(service.IGameServerInterface).ActiveTickCallback(&service.Void{})
	if err != nil {
		return nil, err
	}

	return nil, nil
}

func (gs *OrderService) FinishOrder(in *service.OrderResponse) (*service.Void, error) {
	gs.app.NotifyOrder(in.OutTradeNo)
	return nil, nil
}
