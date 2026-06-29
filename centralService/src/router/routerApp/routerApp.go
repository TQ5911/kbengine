package Router

import (
	"centralService/src/appLog"
	"centralService/src/common"
	_ "github.com/go-sql-driver/mysql"
	"github.com/google/uuid"
	"net"
	gameServerService "centralService/src/router/routerApp/gameServerService"
	"strconv"
	"sync"
	"sync/atomic"
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

//单个服务器维度的流量统计
type serverTrafficStat struct {
	requestCount uint64
	byteCount    uint64
}

type RouterApp struct
{
	common.App
	gameServers map[string] *GameServerService
	channelToHost map[uuid.UUID] *GameServerService
	serversLock *sync.RWMutex
	actions chan LoginAction
	gameBaseAppsList map[uint32] []uint32

	//流量统计：分别按来源服务器和目标服务器统计
	sourceTraffic map[uint32] *serverTrafficStat
	destTraffic   map[uint32] *serverTrafficStat
	trafficLock   *sync.RWMutex
	totalRequests uint64
	totalBytes    uint64
}

func NewRouterApp() *RouterApp{
	gameServers := make(map[string] *GameServerService)
	channelToHost := make(map[uuid.UUID] *GameServerService)
	actions := make(chan LoginAction, 10)
	gameBaseAppsList :=make(map[uint32] []uint32)
	sourceTraffic := make(map[uint32] *serverTrafficStat)
	destTraffic := make(map[uint32] *serverTrafficStat)

	app := RouterApp{common.App{AppName:"RouterApp"},
		gameServers, channelToHost,  new(sync.RWMutex), actions, gameBaseAppsList,
		sourceTraffic, destTraffic, new(sync.RWMutex), 0, 0}

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

//记录一次转发的流量统计
func (self *RouterApp) recordTraffic(sourceServerId uint32, destServerId uint32, byteCount uint64) {
	atomic.AddUint64(&self.totalRequests, 1)
	atomic.AddUint64(&self.totalBytes, byteCount)

	self.trafficLock.Lock()
	defer self.trafficLock.Unlock()

	srcStat, ok := self.sourceTraffic[sourceServerId]
	if !ok {
		srcStat = &serverTrafficStat{}
		self.sourceTraffic[sourceServerId] = srcStat
	}
	srcStat.requestCount++
	srcStat.byteCount += byteCount

	dstStat, ok := self.destTraffic[destServerId]
	if !ok {
		dstStat = &serverTrafficStat{}
		self.destTraffic[destServerId] = dstStat
	}
	dstStat.requestCount++
	dstStat.byteCount += byteCount
}

//获取当前流量统计的快照
func (self *RouterApp) getTrafficStatsSnapshot() *gameServerService.TrafficStats {
	self.trafficLock.RLock()
	defer self.trafficLock.RUnlock()

	stats := &gameServerService.TrafficStats{
		SourceTraffic: make([]*gameServerService.ServerTrafficEntry, 0, len(self.sourceTraffic)),
		DestTraffic:   make([]*gameServerService.ServerTrafficEntry, 0, len(self.destTraffic)),
		TotalRequests: atomic.LoadUint64(&self.totalRequests),
		TotalBytes:    atomic.LoadUint64(&self.totalBytes),
	}

	for serverId, st := range self.sourceTraffic {
		stats.SourceTraffic = append(stats.SourceTraffic, &gameServerService.ServerTrafficEntry{
			ServerId:     serverId,
			RequestCount: st.requestCount,
			ByteCount:    st.byteCount,
		})
	}

	for serverId, st := range self.destTraffic {
		stats.DestTraffic = append(stats.DestTraffic, &gameServerService.ServerTrafficEntry{
			ServerId:     serverId,
			RequestCount: st.requestCount,
			ByteCount:    st.byteCount,
		})
	}

	return stats
}

//重置所有流量统计
func (self *RouterApp) resetTrafficStats() {
	self.trafficLock.Lock()
	defer self.trafficLock.Unlock()

	self.sourceTraffic = make(map[uint32] *serverTrafficStat)
	self.destTraffic = make(map[uint32] *serverTrafficStat)
	atomic.StoreUint64(&self.totalRequests, 0)
	atomic.StoreUint64(&self.totalBytes, 0)

	appLog.Info("router traffic stats reset")
}
