package crossTeamApp

import (
	"centralService/src/appLog"
	"centralService/src/common"
	pb "centralService/src/crossTeamServer/crossTeamApp/gameServerService"
	"centralService/src/trpc"
	"fmt"
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
	serversLock sync.RWMutex
	gameServers map[string]map[uuid.UUID]*GameServerService // serverId -> {channelUUID -> service}
	// serverStubNums 各服 Stub 分片总数（注册时上报并维护最大值，避免每次发送遍历连接；
	// 断连不代表部署结构变化，拆除连接不改值，仅最后一条连接拆除时清条目）；
	// 与 gameServers 同在 serversLock 保护下读写
	serverStubNums map[uint32]uint32
	channelToHost  map[uuid.UUID]*GameServerService // channelUUID -> service（断连时快速定位）

	dispatcher *TeamDispatcher
	matchPools *MatchPoolMgr
	chatBuffer *ChatBuffer

	// playerTeam 全局 gbId -> teamId 索引（互斥兜底校验与登录恢复反查用）。
	// 队伍成员关系仍由 worker 持有，本索引只存映射，跨 worker 读写需加锁
	playersLock sync.RWMutex
	playerTeam  map[uint64]uint64

	// 讨伐限流：全局每秒兜底限速器（大值安全阀，见 CRUSADE_START_LIMIT_PER_SECOND）
	crusadeLimiter *rate.Limiter

	// 队伍列表快照：后台协程按 target 维护，查询只读快照
	teamListSnapshot   map[int32]*teamListSnapshotEntry
	teamListSnapshotMu sync.RWMutex
	teamListDirty      map[int32]bool
	teamListDirtyMu    sync.Mutex
}

// initCrusadeLimiter 初始化全局每秒兜底限速器（硬编码大值，仅作异常流量安全阀）。
func (cta *CrossTeamApp) initCrusadeLimiter() {
	cta.crusadeLimiter = rate.NewLimiter(
		rate.Limit(CRUSADE_START_LIMIT_PER_SECOND),
		CRUSADE_START_LIMIT_PER_SECOND,
	)
}

func NewCrossTeamApp() *CrossTeamApp {
	app := &CrossTeamApp{
		App:              common.App{AppName: "CrossTeamApp"},
		gameServers:      make(map[string]map[uuid.UUID]*GameServerService),
		serverStubNums:   make(map[uint32]uint32),
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
	// stubNum 注册后不再变化，新增连接只会持平或抬高该服最大值
	if service.stubNum > cta.serverStubNums[service.serverId] {
		cta.serverStubNums[service.serverId] = service.stubNum
	}
}

func (cta *CrossTeamApp) removeGameServer(service *GameServerService) {
	cta.serversLock.Lock()
	defer cta.serversLock.Unlock()

	serviceKey := cta.getServiceKey(service.serverId)
	if m, ok := cta.gameServers[serviceKey]; ok {
		delete(m, service.GetRpcChannel().ChannelUUID)
		if len(m) == 0 {
			delete(cta.gameServers, serviceKey)
			// 最后一条连接拆除：顺手清掉 stubNum 条目，避免永不回归的服残留；
			// 断连不代表部署结构（stubNum）变化，其他情况不动 serverStubNums，
			// 重连时 addGameServer 会重写同值
			delete(cta.serverStubNums, service.serverId)
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

// pickShardConn 按分片 key 从连接集合中选择目标连接：分片下标 = shardKey % stubNum，
// stubNum 为该服注册时记录的分片总数（与游戏服 Stub 的 _isMyTeam/_isMyGbId 过滤口径一致，
// key 按消息类型取 teamId 或 gbId）。
// 返回 nil 表示无法路由（stubNum=0/目标分片不在线），调用方回退广播。
func pickShardConn(servers []*GameServerService, shardKey uint64, stubNum uint32) *GameServerService {
	if len(servers) == 1 {
		return servers[0]
	}
	// 滚动更新期新旧版本并存时，路由不到目标分片的消息走回退广播，
	// 仍由 Stub 过滤兜底，不会丢
	if stubNum == 0 {
		return nil
	}
	targetIdx := uint32(shardKey % uint64(stubNum))
	for _, gs := range servers {
		if gs.stubNum == stubNum && gs.stubIdx == targetIdx {
			return gs
		}
	}
	return nil
}

// serverStubNum 查该服注册时记录的最大 stubNum（注册时在 serversLock 下维护，
// 路由口径同 pickShardConn），0 表示无连接或连接均未上报分片信息
func (cta *CrossTeamApp) serverStubNum(serverId uint32) uint32 {
	cta.serversLock.RLock()
	defer cta.serversLock.RUnlock()
	return cta.serverStubNums[serverId]
}

// sendToServer 按 serverId + 分片 key 路由推送：命中分片连接则单发，不再向同服全部
// Stub 分片广播；无法路由时回退广播（行为与旧版一致，游戏服 Stub 过滤兜底）。
// shardKey 必须与游戏服侧该消息的过滤 key 一致（按 teamId 过滤的消息传 teamId，
// 按 gbId 过滤的传 gbId）
func (cta *CrossTeamApp) sendToServer(serverId uint32, shardKey uint64, what string, send func(client *pb.GameServerClient) error) {
	servers := cta.getGameServers(serverId)
	if len(servers) == 0 {
		appLog.Warnf("send %s failed, game server %d not connected", what, serverId)
		return
	}
	if gs := pickShardConn(servers, shardKey, cta.serverStubNum(serverId)); gs != nil {
		if err := send(gs.GetClientEndPoint().(*pb.GameServerClient)); err != nil {
			appLog.Errorf("send %s to server %d channel %s failed: %v", what, serverId, gs.GetRpcChannel().ChannelUUID, err)
		}
		return
	}
	for _, gs := range servers {
		if err := send(gs.GetClientEndPoint().(*pb.GameServerClient)); err != nil {
			appLog.Errorf("send %s to server %d channel %s failed: %v", what, serverId, gs.GetRpcChannel().ChannelUUID, err)
		}
	}
}

// pushStateBucketKey 成员状态推送分桶 key：目标服 + stub 分片下标。
// 目标连接必须满足 teamId % stubNum == stubIdx（与游戏服 Stub 过滤口径一致，
// stubNum 取该服注册信息），同（服、分片）的多队合一包发送；
// 该服连接均未上报分片信息（stubNum=0）时统一落 stubIdx=0 桶，发送时按现有回退策略广播
type pushStateBucketKey struct {
	serverId uint32
	stubIdx  uint32
}

// pushTeamMemberStates 成员状态推送分发（推送模型，供 worker 推送分支调用）：
// 把各队全量快照 item 按成员当前实际所在服（MemberState.routeServerId）+ stub 分片
// 分桶聚合，经 sendToServer 下行；发送失败由 sendToServer 一处打日志（what 携带
// teamId 定位），不重试——脏集合在 worker 侧取出即视为消费完毕
func (cta *CrossTeamApp) pushTeamMemberStates(items []*pb.TeamMemberStatePushItem) {
	if len(items) == 0 {
		return
	}

	buckets := make(map[pushStateBucketKey]*pb.TeamMemberStatesPushMsg)
	shardKeys := make(map[pushStateBucketKey]uint64) // 每桶的代表 teamId（满足 teamId % stubNum == stubIdx）
	for _, item := range items {
		// 目标服集合：该队所有成员的 RouteServerId（成员当前实际所在服）去重
		routed := make(map[uint32]bool)
		for _, m := range item.Members {
			if routed[m.RouteServerId] {
				continue
			}
			routed[m.RouteServerId] = true
			stubNum := cta.serverStubNum(m.RouteServerId)
			stubIdx := uint32(0)
			if stubNum > 0 {
				stubIdx = uint32(item.TeamId % uint64(stubNum))
			}
			key := pushStateBucketKey{serverId: m.RouteServerId, stubIdx: stubIdx}
			msg, ok := buckets[key]
			if !ok {
				msg = &pb.TeamMemberStatesPushMsg{}
				buckets[key] = msg
				shardKeys[key] = item.TeamId
			}
			msg.Teams = append(msg.Teams, item)
		}
	}

	for key, msg := range buckets {
		teamIds := make([]uint64, 0, len(msg.Teams))
		for _, item := range msg.Teams {
			teamIds = append(teamIds, item.TeamId)
		}
		cta.sendToServer(
			key.serverId,
			shardKeys[key],
			fmt.Sprintf("teamMemberStatesPush teams=%v", teamIds),
			func(client *pb.GameServerClient) error {
				_, err := client.TeamMemberStatesPush(msg)
				return err
			},
		)
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

		// debug：打印本 target 快照中的队伍列表，便于测试观测
		for _, e := range items {
			appLog.Debugf(
				"team list snapshot, target=%d teamId=%d members=%d/%d isCross=%v",
				target,
				e.item.TeamId,
				e.item.MemberCnt,
				e.item.MaxNum,
				e.isCross,
			)
		}
	}
}

// ---------------------------------------------------------------------------
// playerTeam 全局索引（gbId -> teamId）：互斥兜底校验与 QueryTeam 反查用
// ---------------------------------------------------------------------------

// compareAndSetPlayerTeam 互斥最终闸门：单次写锁内完成"无队检查 + 落索引"。
// 队伍按 teamId%workerNum 分桶并发处理，查（RLock）与写（Lock）分步进行时锁会释放，
// 两个 worker 可同时通过 ==0 检查后各自写索引（后写覆盖先写，造成"一人在两队"）；
// 所有落索引路径（入队/建队/转换登记）必须经本函数，已在队返回 false
func (cta *CrossTeamApp) compareAndSetPlayerTeam(gbId uint64, teamId uint64) bool {
	cta.playersLock.Lock()
	defer cta.playersLock.Unlock()
	if cta.playerTeam[gbId] != 0 {
		return false
	}
	cta.playerTeam[gbId] = teamId
	return true
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
