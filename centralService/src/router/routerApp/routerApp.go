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

//单个服务器维度的流量统计（无锁：字段均通过 sync/atomic 访问）
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

	//流量统计（无锁）：用 sync.Map 持有按 serverId 的计数器，total 用 atomic
	sourceTraffic sync.Map // map[uint32]*serverTrafficStat
	destTraffic   sync.Map // map[uint32]*serverTrafficStat
	totalRequests uint64
	totalBytes    uint64
}

func NewRouterApp() *RouterApp{
	gameServers := make(map[string] *GameServerService)
	channelToHost := make(map[uuid.UUID] *GameServerService)
	actions := make(chan LoginAction, 10)
	gameBaseAppsList :=make(map[uint32] []uint32)

	app := RouterApp{common.App{AppName:"RouterApp"},
		gameServers, channelToHost,  new(sync.RWMutex), actions, gameBaseAppsList,
		sync.Map{}, sync.Map{}, 0, 0}

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
		appLog.Error("getOtherBaseApp failed by serverId:", serverId)
		return nil
	}

	index := componentId % length
	dstCId := self.gameBaseAppsList[serverId][index]

	serviceKey := self.getServiceKey(serverId, dstCId)
	if gs, ok := self.gameServers[serviceKey]; ok{
		return gs
	}
	appLog.Error("getOtherBaseApp failed by serviceKey:", serverId, ",", componentId)
	return nil
}

//获取或创建某个 serverId 对应的统计计数器（首次插入走 sync.Map 内部锁，热点键后续为 lock-free）
func getOrCreateTrafficStat(m *sync.Map, serverId uint32) *serverTrafficStat {
	if v, ok := m.Load(serverId); ok {
		return v.(*serverTrafficStat)
	}
	newStat := &serverTrafficStat{}
	actual, _ := m.LoadOrStore(serverId, newStat)
	return actual.(*serverTrafficStat)
}

//记录一次转发的流量统计（无锁）
func (self *RouterApp) recordTraffic(sourceServerId uint32, destServerId uint32, byteCount uint64) {
	atomic.AddUint64(&self.totalRequests, 1)
	atomic.AddUint64(&self.totalBytes, byteCount)

	srcStat := getOrCreateTrafficStat(&self.sourceTraffic, sourceServerId)
	atomic.AddUint64(&srcStat.requestCount, 1)
	atomic.AddUint64(&srcStat.byteCount, byteCount)

	dstStat := getOrCreateTrafficStat(&self.destTraffic, destServerId)
	atomic.AddUint64(&dstStat.requestCount, 1)
	atomic.AddUint64(&dstStat.byteCount, byteCount)
}

//获取当前流量统计的快照（无锁：sync.Map.Range 内部无锁，per-counter 读取走 atomic）
func (self *RouterApp) getTrafficStatsSnapshot() *gameServerService.TrafficStats {
	stats := &gameServerService.TrafficStats{
		SourceTraffic: []*gameServerService.ServerTrafficEntry{},
		DestTraffic:   []*gameServerService.ServerTrafficEntry{},
		TotalRequests: atomic.LoadUint64(&self.totalRequests),
		TotalBytes:    atomic.LoadUint64(&self.totalBytes),
	}

	self.sourceTraffic.Range(func(key, value interface{}) bool {
		serverId, _ := key.(uint32)
		stat, _ := value.(*serverTrafficStat)
		stats.SourceTraffic = append(stats.SourceTraffic, &gameServerService.ServerTrafficEntry{
			ServerId:     serverId,
			RequestCount: atomic.LoadUint64(&stat.requestCount),
			ByteCount:    atomic.LoadUint64(&stat.byteCount),
		})
		return true
	})

	self.destTraffic.Range(func(key, value interface{}) bool {
		serverId, _ := key.(uint32)
		stat, _ := value.(*serverTrafficStat)
		stats.DestTraffic = append(stats.DestTraffic, &gameServerService.ServerTrafficEntry{
			ServerId:     serverId,
			RequestCount: atomic.LoadUint64(&stat.requestCount),
			ByteCount:    atomic.LoadUint64(&stat.byteCount),
		})
		return true
	})

	return stats
}

//重置所有流量统计（无锁：逐个 Delete 即可）
func (self *RouterApp) resetTrafficStats() {
	self.sourceTraffic.Range(func(key, value interface{}) bool {
		self.sourceTraffic.Delete(key)
		return true
	})
	self.destTraffic.Range(func(key, value interface{}) bool {
		self.destTraffic.Delete(key)
		return true
	})
	atomic.StoreUint64(&self.totalRequests, 0)
	atomic.StoreUint64(&self.totalBytes, 0)

	appLog.Info("router traffic stats reset")
}
