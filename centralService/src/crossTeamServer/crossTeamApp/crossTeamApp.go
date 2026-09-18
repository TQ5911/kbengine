package crossTeamApp

import (
	"centralService/src/appLog"
	"centralService/src/common"
	pb "centralService/src/crossTeamServer/crossTeamApp/gameServerService"
	"centralService/src/trpc"
	"net"
	"strconv"
	"sync"
	"syscall"
	"time"

	"github.com/google/uuid"
	"golang.org/x/time/rate"
)

var CrossTeamConfig = AppConfig{}

type CrossTeamApp struct {
	common.App
	serversLock   sync.RWMutex
	gameServers   map[string]map[uuid.UUID]*GameServerService // serverId -> {channelUUID -> service}
	channelToHost map[uuid.UUID]*GameServerService            // channelUUID -> service（断连时快速定位）

	dispatcher *TeamDispatcher
	matchPools *MatchPoolMgr
	chatBuffer *ChatBuffer

	// playerTeam 全局 gbId -> teamId 索引（互斥兜底校验与登录恢复反查用）。
	// 队伍成员关系仍由 worker 持有，本索引只存映射，跨 worker 读写需加锁
	playersLock sync.RWMutex
	playerTeam  map[uint64]uint64

	// 讨伐限流：进行中计数（原子）+ 全局每秒限速器
	crusadeOngoing int64
	crusadeLimiter *rate.Limiter

	// 队伍列表快照：后台协程按 target 维护，查询只读快照
	teamListSnapshot   map[int32]*teamListSnapshotEntry
	teamListSnapshotMu sync.RWMutex
	teamListDirty      map[int32]bool
	teamListDirtyMu    sync.Mutex
}

// initCrusadeLimiter 根据当前配置初始化全局每秒限速器。
func (cta *CrossTeamApp) initCrusadeLimiter() {
	limitPerSecond := CrossTeamConfig.CrusadeStartLimitPerSecond
	if limitPerSecond > 0 {
		cta.crusadeLimiter = rate.NewLimiter(rate.Limit(limitPerSecond), limitPerSecond)
	} else {
		cta.crusadeLimiter = nil
	}
}

func NewCrossTeamApp() *CrossTeamApp {
	app := &CrossTeamApp{
		App:              common.App{AppName: "CrossTeamApp"},
		gameServers:      make(map[string]map[uuid.UUID]*GameServerService),
		channelToHost:    make(map[uuid.UUID]*GameServerService),
		playerTeam:       make(map[uint64]uint64),
		teamListSnapshot: make(map[int32]*teamListSnapshotEntry),
		teamListDirty:    make(map[int32]bool),
	}
	app.matchPools = NewMatchPoolMgr(app)
	app.dispatcher = NewTeamDispatcher(app, CrossTeamConfig.WorkerNum)
	if CrossTeamConfig.MatchTimeoutSeconds > 0 {
		matchTimeoutSeconds = CrossTeamConfig.MatchTimeoutSeconds
	}
	app.chatBuffer = NewChatBuffer(app.dispatcher)
	app.initCrusadeLimiter()
	return app
}

func (cta *CrossTeamApp) GetServices() []*common.ServiceInfo {
	return []*common.ServiceInfo{
		{
			ServiceType:       SERVICE_CROSS_TEAM,
			ServiceName:       cta.AppName,
			ServiceListenAddr: CrossTeamConfig.CrossTeamServerAddr,
		},
	}
}

func (cta *CrossTeamApp) NewService(conn net.Conn, serviceType uint8) trpc.IServerEndPoint {
	var service trpc.IServerEndPoint = nil
	if serviceType == SERVICE_CROSS_TEAM {
		rpcUUID := uuid.New()
		channel := trpc.NewRpcChannel(rpcUUID, conn)
		service = &GameServerService{
			ServerEndPoint: pb.NewCrossTeamServerService(pb.NewGameServerClient(channel)), app: cta}
		channel.SetEndPoint(service)
	}
	return service
}

// Start implements common.IApp.
func (cta *CrossTeamApp) Start() {
	appLog.Info("cross team app start, groupId:", CrossTeamConfig.GroupId)
	cta.App.Start()

	cta.RegisterSignals(syscall.SIGINT, syscall.SIGKILL, syscall.SIGTERM)
	common.ExecuteConcurrently(func() {
		<-cta.SignalChan
		cta.Stop()
	})
	common.ExecuteConcurrently(cta.runTeamListSnapshotRefresh)
	common.ExecuteConcurrently(func() {
		cta.StartDebugService(CrossTeamConfig.AddressForDebug)
	})
}

// Stop implements common.IApp.
func (cta *CrossTeamApp) Stop() {
}

func (cta *CrossTeamApp) addGameServer(service *GameServerService) {
	cta.serversLock.Lock()
	defer cta.serversLock.Unlock()

	serviceKey := cta.getServiceKey(service.serverId)
	if cta.gameServers[serviceKey] == nil {
		cta.gameServers[serviceKey] = make(map[uuid.UUID]*GameServerService)
	}
	cta.gameServers[serviceKey][service.GetRpcChannel().ChannelUUID] = service
	cta.channelToHost[service.GetRpcChannel().ChannelUUID] = service
}

func (cta *CrossTeamApp) removeGameServer(service *GameServerService) {
	cta.serversLock.Lock()
	defer cta.serversLock.Unlock()

	serviceKey := cta.getServiceKey(service.serverId)
	if m, ok := cta.gameServers[serviceKey]; ok {
		delete(m, service.GetRpcChannel().ChannelUUID)
		if len(m) == 0 {
			delete(cta.gameServers, serviceKey)
		}
	}
	delete(cta.channelToHost, service.GetRpcChannel().ChannelUUID)
}

func (cta *CrossTeamApp) getServiceKey(serverId uint32) string {
	return strconv.Itoa(int(serverId))
}

// getGameServers 返回指定 serverId 下的全部连接（快照，调用方只读使用）
func (cta *CrossTeamApp) getGameServers(serverId uint32) []*GameServerService {
	cta.serversLock.RLock()
	defer cta.serversLock.RUnlock()

	serviceKey := cta.getServiceKey(serverId)
	m, ok := cta.gameServers[serviceKey]
	if !ok || len(m) == 0 {
		return nil
	}
	out := make([]*GameServerService, 0, len(m))
	for _, service := range m {
		out = append(out, service)
	}
	return out
}

// sendToServer 按 serverId 路由推送：同服多个 Stub 分片连接时广播到该服全部连接
func (cta *CrossTeamApp) sendToServer(serverId uint32, what string, send func(client *pb.GameServerClient) error) {
	servers := cta.getGameServers(serverId)
	if len(servers) == 0 {
		appLog.Warnf("send %s failed, game server %d not connected", what, serverId)
		return
	}
	for _, gs := range servers {
		if err := send(gs.GetClientEndPoint().(*pb.GameServerClient)); err != nil {
			appLog.Errorf("send %s to server %d channel %s failed: %v", what, serverId, gs.GetRpcChannel().ChannelUUID, err)
		}
	}
}

// ---------------------------------------------------------------------------
// 队伍列表快照：后台协程周期性按 target 聚合，查询只读快照 + 版本号对比省流量
// ---------------------------------------------------------------------------

// teamListEntry 队伍列表快照条目：item 为下发数据，isCross/dunServer 为本服过滤元数据。
// 本服目标队伍仅对 dunServer 同服的请求方可见（D3-1），过滤在 GetTeamList 按请求
// serverId 进行（快照全组共享）；TeamListItem 协议本身不携带这两字段
type teamListEntry struct {
	item      *pb.TeamListItem
	isCross   bool
	dunServer uint32
}

// teamListSnapshotEntry 单个 target 的队伍列表快照（调用方读 snapshot 时只读 items，不修改）
type teamListSnapshotEntry struct {
	items []*teamListEntry
}

// runTeamListSnapshotRefresh 后台定时刷新协程入口
func (cta *CrossTeamApp) runTeamListSnapshotRefresh() {
	ticker := time.NewTicker(TEAM_LIST_REFRESH_SECONDS * time.Second)
	defer ticker.Stop()
	for range ticker.C {
		cta.refreshTeamListSnapshot()
	}
}

// markTeamListDirty 在队伍数据发生变更时标记对应 target 需要重建快照
func (cta *CrossTeamApp) markTeamListDirty(target int32) {
	cta.teamListDirtyMu.Lock()
	cta.teamListDirty[target] = true
	cta.teamListDirtyMu.Unlock()
}

// refreshTeamListSnapshot 刷新所有脏 target 的快照。
// 先清空脏标记再聚合，聚合期间产生的新变更会再次把 target 标脏，下一轮自然重建。
func (cta *CrossTeamApp) refreshTeamListSnapshot() {
	cta.teamListDirtyMu.Lock()
	targets := make([]int32, 0, len(cta.teamListDirty))
	for target, dirty := range cta.teamListDirty {
		if dirty {
			targets = append(targets, target)
			cta.teamListDirty[target] = false
		}
	}
	cta.teamListDirtyMu.Unlock()

	for _, target := range targets {
		items := cta.dispatcher.collectTeamList(target)
		cta.teamListSnapshotMu.Lock()
		entry := cta.teamListSnapshot[target]
		if entry == nil {
			entry = &teamListSnapshotEntry{}
			cta.teamListSnapshot[target] = entry
		}
		entry.items = items
		cta.teamListSnapshotMu.Unlock()
	}
}

// ---------------------------------------------------------------------------
// playerTeam 全局索引（gbId -> teamId）：互斥兜底校验与 QueryTeam 反查用
// ---------------------------------------------------------------------------

func (cta *CrossTeamApp) setPlayerTeam(gbId uint64, teamId uint64) {
	cta.playersLock.Lock()
	defer cta.playersLock.Unlock()
	cta.playerTeam[gbId] = teamId
}

func (cta *CrossTeamApp) removePlayerTeam(gbId uint64) {
	cta.playersLock.Lock()
	defer cta.playersLock.Unlock()
	delete(cta.playerTeam, gbId)
}

func (cta *CrossTeamApp) getPlayerTeam(gbId uint64) uint64 {
	cta.playersLock.RLock()
	defer cta.playersLock.RUnlock()
	return cta.playerTeam[gbId]
}
