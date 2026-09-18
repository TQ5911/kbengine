package Router

import (
	"centralService/src/appLog"
	"centralService/src/router/routerApp/routerCluster"
	"sync"
	"time"

	"github.com/gomodule/redigo/redis"
)

// globalServerEntry: 全局游戏服注册表中的一条记录
// componentId 不进入全局表——同一 serverId 的所有 componentId 必须在同一 router 上
// （业务约束），转发到目标 router 后由其本地 getGameServer(sid, cid) 解析。
type globalServerEntry struct {
	ServerId uint32
	RouterId uint32
}

// ClusterSyncTick: 5s 一次的周期任务
//   1) 把本节点 meta (clusterAddr + gameServerIds + lastTickMs) 写入 Redis 唯一 hash;
//   2) HGETALL 拉取所有 router 的 meta;
//   3) 推导 gameServerId → routerId，写入 app.globalServerTable;
//   4) 通知 ClusterTopology 根据最新 meta 调整到其他 router 的连接。
type ClusterSyncTick struct {
	app      *RouterApp
	pool     *redis.Pool
	ticker   *time.Ticker
	stopChan chan struct{}
	stopOnce sync.Once
	tickMu   sync.Mutex
	stopped  bool
}

func newClusterSyncTick(app *RouterApp, pool *redis.Pool) *ClusterSyncTick {
	return &ClusterSyncTick{
		app:      app,
		pool:     pool,
		ticker:   time.NewTicker(clusterSyncTickInterval),
		stopChan: make(chan struct{}),
	}
}

func (t *ClusterSyncTick) Start() {
	go t.run()
}

func (t *ClusterSyncTick) Stop() {
	t.stopOnce.Do(func() {
		close(t.stopChan)
		t.ticker.Stop()
	})
}

func (t *ClusterSyncTick) run() {
	t.safeTickOnce()
	for {
		select {
		case <-t.stopChan:
			return
		case <-t.ticker.C:
			t.safeTickOnce()
		}
	}
}

func (t *ClusterSyncTick) safeTickOnce() {
	t.tickMu.Lock()
	defer t.tickMu.Unlock()
	if t.stopped {
		return
	}
	if err := t.tickOnce(); err != nil {
		appLog.Errorf("routerCluster: sync tick failed: %s", err.Error())
	}
}

func (t *ClusterSyncTick) tickOnce() error {
	ids := t.collectLocalServerIds()
	nowMs := time.Now().UnixMilli()
	payload, err := buildMyMetaJSON(RouterConfig.ClusterAdvertiseAddr(), ids, nowMs)
	if err != nil {
		return err
	}
	if err := writeAllRouters(t.pool, RouterConfig.RouterId, payload); err != nil {
		return err
	}

	all, rerr := readAllRouters(t.pool)
	if rerr != nil {
		appLog.Warnf("routerCluster: read all routers failed: %s", rerr.Error())
		return nil
	}

	metas := convertPayloadsToMeta(all)
	t.applyServerRoute(metas)
	t.app.clusterTopology.Reconcile(metas)
	// 5) 本端作为 small ID 的连接, 主动 ping 一次, 维持链路活性
	//    (RpcChannel.Process 读超时为 20s, 5s 一次的 tick 写入足以刷掉对端读超时)
	t.pingSmallIdPeers()
	return nil
}

func (t *ClusterSyncTick) collectLocalServerIds() []uint32 {
	t.app.serversLock.RLock()
	defer t.app.serversLock.RUnlock()
	idSet := make(map[uint32]struct{}, len(t.app.gameServers))
	for _, gs := range t.app.gameServers {
		if gs == nil {
			continue
		}
		idSet[gs.serverId] = struct{}{}
	}
	out := make([]uint32, 0, len(idSet))
	for id := range idSet {
		out = append(out, id)
	}
	return out
}

func convertPayloadsToMeta(all map[uint32]*routerMetaPayload) map[uint32]*RouterNodeMeta {
	out := make(map[uint32]*RouterNodeMeta, len(all))
	for id, p := range all {
		out[id] = &RouterNodeMeta{
			RouterId:      id,
			ClusterAddr:   p.ClusterAddr,
			GameServerIds: p.GameServerIds,
			LastTickMs:    p.LastTickMs,
		}
	}
	return out
}

// applyServerRoute 用最新 router metas 刷新 app.globalServerTable。
// 流程：
//   1) 锁外计算新路由表 newTable；
//   2) 加读锁对比新旧表，无变化则直接返回（避免无效写）；
//   3) 有变化才升级为写锁并替换。
func (t *ClusterSyncTick) applyServerRoute(metas map[uint32]*RouterNodeMeta) {
	newTable := computeServerRoute(metas)
	if !t.serverRouteChanged(newTable) {
		return
	}
	t.app.globalTableLock.Lock()
	defer t.app.globalTableLock.Unlock()
	for sid, rid := range newTable {
		key := t.app.getServiceKey(sid, 0)
		t.app.globalServerTable[key] = &globalServerEntry{
			ServerId: sid,
			RouterId: rid,
		}
	}
	for k, entry := range t.app.globalServerTable {
		if _, ok := newTable[entry.ServerId]; !ok {
			delete(t.app.globalServerTable, k)
		}
	}
}

// computeServerRoute 锁外计算 serverId → routerId 映射
func computeServerRoute(metas map[uint32]*RouterNodeMeta) map[uint32]uint32 {
	out := make(map[uint32]uint32)
	for rid, meta := range metas {
		if rid == RouterConfig.RouterId {
			continue
		}
		if !isRouterOnline(meta) {
			continue
		}
		for _, sid := range meta.GameServerIds {
			if existing, ok := out[sid]; ok {
				appLog.Warnf("routerCluster: serverId=%d registered on both routerId=%d and routerId=%d, keeping the latter", sid, existing, rid)
				continue
			}
			out[sid] = rid
		}
	}
	return out
}

// serverRouteChanged 在读锁下对比新旧表是否等价
func (t *ClusterSyncTick) serverRouteChanged(newTable map[uint32]uint32) bool {
	t.app.globalTableLock.RLock()
	defer t.app.globalTableLock.RUnlock()

	// 把 globalServerTable 投影成 serverId -> routerId 临时视图
	current := make(map[uint32]uint32, len(t.app.globalServerTable))
	for _, entry := range t.app.globalServerTable {
		current[entry.ServerId] = entry.RouterId
	}
	if len(current) != len(newTable) {
		return true
	}
	for sid, rid := range newTable {
		if cur, ok := current[sid]; !ok || cur != rid {
			return true
		}
	}
	return false
}

// pingSmallIdPeers: 对本端是 small ID 的所有连接, 周期性发 ping。
//   - 写帧会到达大 ID 端, 触发大 ID 端 Ping handler 调用 RegisterByPing, 顺带刷新对端 topology;
//   - 同时也防止大 ID 端 RpcChannel 因长时间无入帧触发 20s 读超时而断连。
//   - 写入失败 (对端已挂 / 本端连接已断) 直接 MarkBroken, 下一次 Reconcile 会重拨。
func (t *ClusterSyncTick) pingSmallIdPeers() {
	myId := RouterConfig.RouterId
	peerIds := t.app.clusterTopology.PeersToPing(myId)
	for _, rid := range peerIds {
		state := t.app.clusterTopology.Get(rid)
		if state == nil || state.client == nil {
			continue
		}
		if _, err := state.client.Ping(&routerCluster.ClusterPing{
			FromRouterId: myId,
			Timestamp:    uint64(time.Now().UnixMilli()),
		}); err != nil {
			appLog.Warnf("routerCluster: ping to routerId=%d failed: %s", rid, err.Error())
			t.app.clusterTopology.MarkBroken(rid)
		}
	}
}

func isRouterOnline(meta *RouterNodeMeta) bool {
	if meta.LastTickMs <= 0 {
		return true
	}
	age := time.Now().UnixMilli() - meta.LastTickMs
	return age <= int64(routerMetaStaleTTL/time.Millisecond)
}
