package Router

import (
	"centralService/src/common"
	_ "github.com/go-sql-driver/mysql"
	"github.com/google/uuid"
	"net"
	gameServerService "centralService/src/router/routerApp/gameServerService"
	"strconv"
	"sync"
	"syscall"
	"centralService/src/trpc"
)

var RouterConfig = AppConfig{}

const(
	_=iota
	//SERVICE_CLIENT_AUTH
	SERVICE_GAME_SERVER
)

type LoginAction func (*RouterApp) error

type RouterApp struct
{
	common.App
	gameServers map[string] *GameServerService
	channelToHost map[uuid.UUID] *GameServerService
	serversLock *sync.RWMutex
	actions chan LoginAction
	gameBaseAppsList map[uint32] []uint32
}

func NewRouterApp() *RouterApp{
	gameServers := make(map[string] *GameServerService)
	channelToHost := make(map[uuid.UUID] *GameServerService)
	actions := make(chan LoginAction, 10)
	gameBaseAppsList :=make(map[uint32] []uint32)

	app := RouterApp{common.App{AppName:"RouterApp"},
		gameServers, channelToHost,  new(sync.RWMutex), actions, gameBaseAppsList}

	return  &app
}

func (self *RouterApp) GetServices() []*common.ServiceInfo{
	services := []*common.ServiceInfo {
		&common.ServiceInfo{SERVICE_GAME_SERVER, "游戏服连接监听", RouterConfig.GameServerServiceAddr},
	}
	return services
}

func (self *RouterApp) Start(){
	self.App.Start()

	self.RegisterSignals(syscall.SIGINT, syscall.SIGKILL, syscall.SIGTERM)

	go func() {
		<-self.SignalChan
		self.Stop()
	}()
	go self.StartDebugService(RouterConfig.AddressForDebug)
}

func (self *RouterApp) Stop(){

}

func (self *RouterApp) NewService(conn net.Conn, serviceType uint8) trpc.IServerEndPoint {
	var service trpc.IServerEndPoint = nil
	if(serviceType==SERVICE_GAME_SERVER){
		rpcUUID := uuid.New()
		channel := trpc.NewRpcChannel(rpcUUID, conn)
		service = &GameServerService{ServerEndPoint: gameServerService.NewRouterServerService(gameServerService.NewGameServerClient(channel)), app:self}
		channel.SetEndPoint(service)
	}

	return service
}

func remove(slice []uint32, elem uint32) []uint32 {
	for i := range slice {
		if slice[i] == elem {
			slice = append(slice[:i], slice[i+1:]...)
			return slice
		}
	}
	return slice
}

func (self *RouterApp) getServiceKey(serverId uint32, componentId uint32) string {
	return strconv.Itoa(int(serverId)) + strconv.Itoa(int(componentId))
}

func (self *RouterApp) addGameServer(service *GameServerService) {
	self.serversLock.Lock()
	defer self.serversLock.Unlock()

	serviceKey := self.getServiceKey(service.serverId, service.componentId)
	self.gameServers[serviceKey] = service
	self.channelToHost[service.GetRpcChannel().ChannelUUID] = service
	self.gameBaseAppsList[service.serverId]= append(self.gameBaseAppsList[service.serverId], service.componentId)
}

func (self *RouterApp) removeGameServer(service *GameServerService) {
	self.serversLock.Lock()
	defer self.serversLock.Unlock()

	serviceKey := self.getServiceKey(service.serverId, service.componentId)
	delete(self.gameServers, serviceKey)
	delete(self.channelToHost, service.GetRpcChannel().ChannelUUID)
	self.gameBaseAppsList[service.serverId] = remove(self.gameBaseAppsList[service.serverId], service.componentId)
}

func (self *RouterApp) getGameServer(serverId uint32, componentId uint32) *GameServerService {
	self.serversLock.RLock()
	defer self.serversLock.RUnlock()

	serviceKey := self.getServiceKey(serverId, componentId)
	if gs, ok := self.gameServers[serviceKey]; ok{
		return gs
	}
	return nil
}

func (self *RouterApp) getOtherBaseApp(serverId uint32, componentId uint32) *GameServerService {
	self.serversLock.RLock()
	defer self.serversLock.RUnlock()

	length := uint32(len(self.gameBaseAppsList[serverId]))
	if length <= 0{
		return nil
	}

	index := componentId % length
	dstCId := self.gameBaseAppsList[serverId][index]

	serviceKey := self.getServiceKey(serverId, dstCId)
	if gs, ok := self.gameServers[serviceKey]; ok{
		return gs
	}
	return nil
}
