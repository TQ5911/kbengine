package Router

import (
	"centralService/src/appLog"
	"centralService/src/common"
	"centralService/src/router/routerApp/gameServerService"
	"centralService/src/router/routerApp/routerCluster"
	_ "github.com/go-sql-driver/mysql"
	"github.com/gomodule/redigo/redis"
	"github.com/google/uuid"
	"net"
	"strconv"
	"sync"
	"sync/atomic"
	"syscall"
	"centralService/src/trpc"
)

var RouterConfig = AppConfig{}

const (
	_ = iota
	SERVICE_GAME_SERVER
	SERVICE_ROUTER_NODE
)

type LoginAction func(*RouterApp) error

//单个服务器维度的流量统计（无锁：字段均通过 sync/atomic 访问）
type serverTrafficStat struct {
	requestCount uint64
	byteCount    uint64
}

type RouterApp struct {
	common.App
	gameServers     map[string]*GameServerService
	channelToHost   map[uuid.UUID]*GameServerService
	serversLock     *sync.RWMutex
	actions         chan LoginAction
	gameBaseAppsList map[uint32][]uint32

	//集群化相关
	redisPool         *redis.Pool
	clusterTopology   *ClusterTopology
	clusterSyncTick   *ClusterSyncTick
	globalServerTable map[string]*globalServerEntry
	globalTableLock   *sync.RWMutex

	//流量统计（无锁）：用 sync.Map 持有按 serverId 的计数器，total 用 atomic
	sourceTraffic sync.Map // map[uint32]*serverTrafficStat
	destTraffic   sync.Map // map[uint32]*serverTrafficStat
	totalRequests uint64
	totalBytes    uint64
}

func NewRouterApp() *RouterApp {
	gameServers := make(map[string]*GameServerService)
	channelToHost := make(map[uuid.UUID]*GameServerService)
	actions := make(chan LoginAction, 10)
	gameBaseAppsList := make(map[uint32][]uint32)
	globalServerTable := make(map[string]*globalServerEntry)
	app := &RouterApp{
		App:               common.App{AppName: "RouterApp"},
		gameServers:       gameServers,
		channelToHost:     channelToHost,
		serversLock:       new(sync.RWMutex),
		actions:           actions,
		gameBaseAppsList:  gameBaseAppsList,
		globalServerTable: globalServerTable,
		globalTableLock:   new(sync.RWMutex),
	}

	// redis 连接池
	app.redisPool = common.NewRedisPool(common.RedisPoolOptions{
		ServerName:  "router",
		Addr:        RouterConfig.RedisServer.Addr,
		Username:    RouterConfig.RedisServer.Username,
		Password:    RouterConfig.RedisServer.Passwd,
		Db:          RouterConfig.RedisServer.Db,
		MaxIdle:     RouterConfig.RedisServer.MaxIdle,
		MaxActive:   RouterConfig.RedisServer.MaxActive,
		IdleTimeout: RouterConfig.RedisServer.IdleTimeout,
	})

	app.clusterTopology = newClusterTopology(app)
	app.clusterSyncTick = newClusterSyncTick(app, app.redisPool)
	return app
}

func (self *RouterApp) GetServices() []*common.ServiceInfo {
	services := []*common.ServiceInfo{
		{ServiceType: SERVICE_GAME_SERVER, ServiceName: "游戏服连接监听", ServiceListenAddr: RouterConfig.GameServerServiceAddr},
	}
	if RouterConfig.RouterClusterAddr != "" {
		services = append(services, &common.ServiceInfo{
			ServiceType:       SERVICE_ROUTER_NODE,
			ServiceName:       "router 集群节点监听",
			ServiceListenAddr: RouterConfig.RouterClusterAddr,
		})
	}
	return services
}

func (self *RouterApp) Start() {
	self.App.Start()

	if RouterConfig.RouterId == 0 {
		appLog.Error("routerCluster: routerId is 0, must be configured")
	} else if RouterConfig.RouterClusterAddr == "" {
		appLog.Error("routerCluster: routerClusterAddr is empty, must be configured for cluster mode")
	}

	self.RegisterSignals(syscall.SIGINT, syscall.SIGKILL, syscall.SIGTERM)

	go func() {
		<-self.SignalChan
		self.Stop()
	}()
	go self.StartDebugService(RouterConfig.AddressForDebug)

	if self.clusterSyncTick != nil {
		self.clusterSyncTick.Start()
	}
}

func (self *RouterApp) Stop() {
	if self.clusterSyncTick != nil {
		self.clusterSyncTick.Stop()
	}
	if self.clusterTopology != nil {
		self.clusterTopology.CloseAll()
	}
}

func (self *RouterApp) NewService(conn net.Conn, serviceType uint8) trpc.IServerEndPoint {
	var service trpc.IServerEndPoint = nil
	switch serviceType {
	case SERVICE_GAME_SERVER:
		rpcUUID := uuid.New()
		channel := trpc.NewRpcChannel(rpcUUID, conn)
		service = &GameServerService{
			ServerEndPoint: gameServerService.NewRouterServerService(gameServerService.NewGameServerClient(channel)),
			app:            self,
		}
		channel.SetEndPoint(service)
	case SERVICE_ROUTER_NODE:
		// 来自其他 router 节点的连接（大 ID 端被小 ID 端连过来）
		state := newRouterNodeStateAsServer(conn, self)
		self.clusterTopology.RegisterIncomingConn(state)
		service = state
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
	self.gameBaseAppsList[service.serverId] = append(self.gameBaseAppsList[service.serverId], service.componentId)
}

func (self *RouterApp) removeGameServer(service *GameServerService) {
	self.serversLock.Lock()
	serviceKey := self.getServiceKey(service.serverId, service.componentId)
	if _, ok := self.gameServers[serviceKey]; ok {
		delete(self.gameServers, serviceKey)
		delete(self.channelToHost, service.GetRpcChannel().ChannelUUID)
		self.gameBaseAppsList[service.serverId] = remove(self.gameBaseAppsList[service.serverId], service.componentId)
	}
	self.serversLock.Unlock()
}

func (self *RouterApp) getGameServer(serverId uint32, componentId uint32) *GameServerService {
	self.serversLock.RLock()
	defer self.serversLock.RUnlock()

	serviceKey := self.getServiceKey(serverId, componentId)
	if gs, ok := self.gameServers[serviceKey]; ok {
		return gs
	}
	return nil
}

func (self *RouterApp) getOtherBaseApp(serverId uint32, componentId uint32) *GameServerService {
	self.serversLock.RLock()
	defer self.serversLock.RUnlock()

	length := uint32(len(self.gameBaseAppsList[serverId]))
	if length <= 0 {
		//appLog.Error("getOtherBaseApp failed by serverId:", serverId)
		return nil
	}

	index := componentId % length
	dstCId := self.gameBaseAppsList[serverId][index]

	serviceKey := self.getServiceKey(serverId, dstCId)
	if gs, ok := self.gameServers[serviceKey]; ok {
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

// lookupClusterRoute: 查询全局路由表，得到目标 serverId 所在 routerId
// 全局表只按 serverId 索引，不关心 componentId：业务约束下同一 serverId 的所有
// componentId 必须注册在同一 router 上。
func (self *RouterApp) lookupClusterRoute(serverId uint32) (uint32, bool) {
	key := self.getServiceKey(serverId, 0)
	self.globalTableLock.RLock()
	defer self.globalTableLock.RUnlock()
	if entry, ok := self.globalServerTable[key]; ok {
		return entry.RouterId, true
	}
	return 0, false
}

// forwardToRemoteRouter: 跨节点转发 payload 到目标 router
// 返回 err：写失败（连接已 closed / broken pipe 等）时主动摘除该 routerId 的连接，
// 下个 tick 会按 meta 重建，避免后续请求继续走死连接。
// 注: handler 返回值当前不被回写, 因此本函数无法判断对端是否"已成功投递到游戏服"，
// err == nil 仅代表帧已写到 socket。
func (self *RouterApp) forwardToRemoteRouter(targetRouterId uint32, req *routerCluster.ClusterForwardRequest) error {
	conn := self.clusterTopology.Get(targetRouterId)
	if conn == nil {
		return nil
	}
	client := conn.Client()
	if client == nil {
		return nil
	}
	if _, err := client.ForwardToGameServer(req); err != nil {
		appLog.Warnf("routerCluster: forward to routerId=%d failed, mark broken: %s", targetRouterId, err.Error())
		self.clusterTopology.MarkBroken(targetRouterId)
		return err
	}
	return nil
}
