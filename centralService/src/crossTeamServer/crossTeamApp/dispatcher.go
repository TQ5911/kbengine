package crossTeamApp

import (
	"centralService/src/appLog"
	"centralService/src/common"
	pb "centralService/src/crossTeamServer/crossTeamApp/gameServerService"
	"sort"
	"sync"
	"time"
)

// teamTask 投递给队伍 worker 的任务，fn 在 worker goroutine 内执行并持有该 worker 的队伍数据
type teamTask struct {
	name string // 日志用
	fn   func(w *teamWorker)
}

// teamWorker 队伍 worker：持有 teamId % workerNum == idx 的全部队伍，
// 单 goroutine 串行消费 channel，队伍数据无需加锁。
type teamWorker struct {
	idx   int
	ch    chan teamTask
	teams map[uint64]*CrossTeamData
}

// TeamDispatcher 中心服并发模型：
// 请求按 teamId（无 teamId 的入口按 gbId/uuid）取模投入固定数量的 worker channel，
// 每个 channel 由单 goroutine 串行消费。
type TeamDispatcher struct {
	app     *CrossTeamApp
	workers []*teamWorker
}

func NewTeamDispatcher(app *CrossTeamApp, workerNum int) *TeamDispatcher {
	if workerNum <= 0 {
		workerNum = DEFAULT_WORKER_NUM
	}
	d := &TeamDispatcher{app: app, workers: make([]*teamWorker, workerNum)}
	for i := range d.workers {
		d.workers[i] = &teamWorker{idx: i, ch: make(chan teamTask, 1024), teams: make(map[uint64]*CrossTeamData)}
		w := d.workers[i]
		common.ExecuteConcurrently(func() { d.runWorker(w) })
	}
	return d
}

func (d *TeamDispatcher) runWorker(w *teamWorker) {
	sweepTicker := time.NewTicker(WORKER_SWEEP_SECONDS * time.Second)
	defer sweepTicker.Stop()
	for {
		select {
		case task := <-w.ch:
			// 逐任务 recover（比 ExecuteConcurrently 更细粒度：单个任务 panic 不杀死 worker 循环），
			// 外层 ExecuteConcurrently 仅作 worker 整体的兜底
			func() {
				defer func() {
					if r := recover(); r != nil {
						appLog.Errorf("team worker %d run task %s panic: %v", w.idx, task.name, r)
					}
				}()
				task.fn(w)
			}()
		case <-sweepTicker.C:
			d.sweep(w)
		}
	}
}

// sweep worker 周期扫描：申请超时清理、队长离线转让、空队伍解散
func (d *TeamDispatcher) sweep(w *teamWorker) {
	defer func() {
		if r := recover(); r != nil {
			appLog.Errorf("team worker %d sweep panic: %v", w.idx, r)
		}
	}()
	now := time.Now().Unix()
	for _, team := range w.teams {
		// 申请 60s 超时清理（瞬态数据）：移除后通知队长，客户端同步从申请列表剔除
		for gbId, apply := range team.Applicants {
			if now-apply.ApplyTS >= APPLY_TIMEOUT_SECONDS {
				delete(team.Applicants, gbId)
				if captain, ok := team.Members[team.CaptainGbId]; ok {
					d.app.notifyApplyRemove(captain.ServerId, team.TeamId, gbId, team.CaptainGbId)
				}
				appLog.Debugf("join apply timeout, teamId=%d gbId=%d", team.TeamId, gbId)
			}
		}
		// 讨伐检查/建空间超时
		if team.CrusadeState == CRUSADE_STATE_CHECKING && now >= team.CrusadeDeadline {
			d.app.crusadeAbort(w, team, CRUSADE_ABORT_CHECK_TIMEOUT)
		} else if team.CrusadeState == CRUSADE_STATE_SPACE_CREATING && now >= team.CrusadeDeadline {
			d.app.crusadeAbort(w, team, CRUSADE_ABORT_SPACE_FAILED)
		}
	}
}

// Dispatch 按 key（teamId，无 teamId 时为 gbId/uuid）把任务投入对应 worker 串行执行
func (d *TeamDispatcher) Dispatch(key uint64, name string, fn func(w *teamWorker)) {
	idx := key % uint64(len(d.workers))
	d.workers[idx].ch <- teamTask{name, fn}
}

// getTeam 在调用方已是 worker 上下文时取队伍（仅 worker goroutine 内使用）
func (w *teamWorker) getTeam(teamId uint64) *CrossTeamData {
	return w.teams[teamId]
}

// collectTeamList 跨 worker 收集可入列表的队伍（按 target 过滤，
// 排除私密/InDungeon 队伍），按 createTS 升序排序后返回。
// 条目携带 isCross/dunServer 元数据：本服目标队伍仅对同服请求方可见，
// 过滤在 GetTeamList 按请求 serverId 进行（快照为全组共享，版本号语义不变）。
// 数据量 ≤8k 队，全量收集即可，无需索引结构。
// 调用方为 RPC goroutine，不得在 worker 任务内调用（会死锁）。
func (d *TeamDispatcher) collectTeamList(target int32) []*teamListEntry {
	type listEntry struct {
		entry    *teamListEntry
		createTS int64
	}
	var mu sync.Mutex
	var wg sync.WaitGroup
	all := make([]*listEntry, 0, 64)
	for _, w := range d.workers {
		wg.Add(1)
		w.ch <- teamTask{name: "collectTeamList", fn: func(w *teamWorker) {
			defer wg.Done()
			part := make([]*listEntry, 0, 16)
			for _, team := range w.teams {
				if team.Target != target || team.Password != "" || team.isInDungeon() {
					continue
				}
				part = append(part, &listEntry{
					entry: &teamListEntry{
						item:      team.toListItemPb(),
						isCross:   team.IsCross,
						dunServer: team.DunServer,
					},
					createTS: team.CreateTS,
				})
			}
			if len(part) > 0 {
				mu.Lock()
				all = append(all, part...)
				mu.Unlock()
			}
		}}
	}
	wg.Wait()
	sort.Slice(all, func(i, j int) bool {
		if all[i].createTS != all[j].createTS {
			return all[i].createTS < all[j].createTS
		}
		return all[i].entry.item.TeamId < all[j].entry.item.TeamId
	})
	out := make([]*teamListEntry, 0, len(all))
	for _, e := range all {
		out = append(out, e.entry)
	}
	return out
}

// filterTeamListByServer 按请求方本服 id 过滤本服目标队伍（D3-1：本服队伍仅同服可见，
// 跨服队伍不做限制）；版本号语义不变（版本对比先于过滤，快照本身为全组共享）
func filterTeamListByServer(entries []*teamListEntry, serverId uint32) []*pb.TeamListItem {
	out := make([]*pb.TeamListItem, 0, len(entries))
	for _, e := range entries {
		if !e.isCross && e.dunServer != serverId {
			continue
		}
		out = append(out, e.item)
	}
	return out
}

// foreachTeamOfServer 让各 worker 扫描自己持有的队伍，对含 serverId 成员的队伍执行 fn。
// 用于中心重启恢复后向重连的游戏服刷新队伍缓存。
func (d *TeamDispatcher) foreachTeamOfServer(serverId uint32, fn func(w *teamWorker, team *CrossTeamData)) {
	for _, w := range d.workers {
		w.ch <- teamTask{name: "foreachTeamOfServer", fn: func(w *teamWorker) {
			for _, team := range w.teams {
				for _, m := range team.Members {
					if m.ServerId == serverId {
						fn(w, team)
						break
					}
				}
			}
		}}
	}
}

// matchPoolOp 散人池操作：入池/取消/队伍摘要事件等所有变更都走 pool 所属 goroutine 的 channel
type matchPoolOp struct {
	name string
	fn   func(p *matchPool)
}

// matchPlayer 池内散人：EnterTS 由中心入池时记录（proto 无此字段），用于顺序撮合与超时清理
type matchPlayer struct {
	info    *pb.MatchPlayerInfo
	enterTS int64
	// timeoutSeconds 本次入池生效的匹配超时（秒）：
	// 决策 D5 由游戏服读配表 maxMatchTime 带入；<=0 时入池回落为中心配置 matchTimeoutSeconds
	timeoutSeconds int32
}

// teamSummary 队伍撮合摘要（per-target 队伍摘要索引）：
// 由 team worker 在队伍创建/解散/成员进出/目标门槛或 autoMatch 变更时以事件同步过来，
// pool goroutine 单线程应用，撮合时直接读本地摘要，不跨 worker 收集（所有权清晰、无锁）
type teamSummary struct {
	teamId    uint64
	target    int32
	minLevel  int32
	minScore  int32
	maxNum    int32
	memberCnt int32
	createTS  int64
	isCross   bool   // 队伍目标是否跨服：本服目标队伍仅撮合 dunServer 同服的散人（D3-1）
	dunServer uint32 // 副本创建目标服（同服约束基准）
	matchable bool   // 可参与撮合：公开（无密码）&& 开启自动匹配 && 不在跨服副本中
}

// matchPool 单个 target 的散人匹配池：
// per-target 单 goroutine 持有 pool map 与队伍摘要索引，从结构上消除锁；
// 撮合轮次是纯内存计算（先 drain 操作队列再撮合），撮合结果交异步通知协程发 RPC，
// worker 永远不做 IO，入池请求不会排在慢流程后面。
type matchPool struct {
	target  int32
	opChan  chan matchPoolOp
	players map[uint64]*matchPlayer
	teams   map[uint64]*teamSummary
	dirty   bool // 池级脏标记：有新人进池/出现可撮合队伍才触发下一轮撮合，否则空过
	app     *CrossTeamApp
}

func newMatchPool(target int32, app *CrossTeamApp) *matchPool {
	p := &matchPool{
		target:  target,
		opChan:  make(chan matchPoolOp, 1024),
		players: make(map[uint64]*matchPlayer),
		teams:   make(map[uint64]*teamSummary),
		app:     app,
	}
	common.ExecuteConcurrently(p.run)
	return p
}

func (p *matchPool) run() {
	ticker := time.NewTicker(MATCH_TICK_SECONDS * time.Second)
	defer ticker.Stop()
	for {
		select {
		case op := <-p.opChan:
			p.runOp(op)
		case <-ticker.C:
			p.drainOps()
			p.matchTick()
		}
	}
}

func (p *matchPool) runOp(op matchPoolOp) {
	defer func() {
		if r := recover(); r != nil {
			appLog.Errorf(
				"match pool %d run op %s panic: %v",
				p.target,
				op.name,
				r,
			)
		}
	}()
	op.fn(p)
}

// drainOps 撮合轮次开始前清空操作队列，保证撮合看到的是最新池状态
func (p *matchPool) drainOps() {
	for {
		select {
		case op := <-p.opChan:
			p.runOp(op)
		default:
			return
		}
	}
}

// freeSlots 队伍可撮合空位
func (p *matchPool) freeSlots(ts *teamSummary) int32 {
	return ts.maxNum - ts.memberCnt
}

// matchTick 撮合轮次：
// 先超时扫描（每轮都跑），再按脏标记做空转抑制；
// 遍历本 target 未满的自动匹配队伍（按 createTS 升序，早建的先补人），
// 在 pool 内按入池顺序（EnterTS 排序快照）找满足门槛的散人，配对即从 map 删除
func (p *matchPool) matchTick() {
	now := time.Now().Unix()

	// 超时扫描：按各散人入池时生效的超时值判定，删除并下发 MatchTimeout，玩家需重新发起（无自动重试）
	for gbId, mp := range p.players {
		if now-mp.enterTS >= int64(mp.timeoutSeconds) {
			delete(p.players, gbId)
			p.app.matchPools.clearPlayer(gbId)
			p.notifyMatchTimeout(mp)
			appLog.Infof("match timeout, target=%d gbId=%d", p.target, gbId)
		}
	}

	if !p.dirty {
		return
	}
	p.dirty = false
	if len(p.players) == 0 {
		return
	}

	// 可撮合队伍：未满的自动匹配队伍，按 createTS 升序
	teams := make([]*teamSummary, 0, len(p.teams))
	for _, ts := range p.teams {
		if ts.matchable && p.freeSlots(ts) > 0 {
			teams = append(teams, ts)
		}
	}
	if len(teams) == 0 {
		return
	}
	sort.Slice(teams, func(i, j int) bool { return teams[i].createTS < teams[j].createTS })

	// 散人候选快照按 EnterTS 升序（入池顺序）
	candidates := make([]*matchPlayer, 0, len(p.players))
	for _, mp := range p.players {
		candidates = append(candidates, mp)
	}
	sort.Slice(candidates, func(i, j int) bool {
		if candidates[i].enterTS != candidates[j].enterTS {
			return candidates[i].enterTS < candidates[j].enterTS
		}
		return candidates[i].info.GbId < candidates[j].info.GbId
	})

	matched := make(map[uint64]bool) // 本轮已配对的散人
	// takenSlots 记录本轮撮合已经为每支队伍“占用”了多少空位，避免同一个 tick 内
	// 把多名散人匹配到同一个 slot。跨 tick 的 Settlement 由最终队满兜底。
	takenSlots := make(map[uint64]int32)
	for _, ts := range teams {
		for _, cand := range candidates {
			if p.freeSlots(ts)-takenSlots[ts.teamId] <= 0 {
				break
			}
			if matched[cand.info.GbId] {
				continue
			}
			if cand.info.Level < ts.minLevel || cand.info.Score < ts.minScore {
				continue
			}
			// 本服目标队伍仅撮合 dunServer 同服的散人（D3-1，散人 serverId 入池时已携带）
			if !ts.isCross && cand.info.ServerId != ts.dunServer {
				continue
			}
			// 配对：出池 + 异步通知散人所在服，MatchJoin 最终由队满兜底
			matched[cand.info.GbId] = true
			delete(p.players, cand.info.GbId)
			p.app.matchPools.clearPlayer(cand.info.GbId)
			takenSlots[ts.teamId]++
			p.notifyMatchSuccess(ts.teamId, cand)
			appLog.Infof(
				"match success, target=%d teamId=%d gbId=%d",
				p.target,
				ts.teamId,
				cand.info.GbId,
			)
		}
	}
}

// notifyMatchSuccess 撮合成功异步通知（两段式第一段）：向散人所在服发 MatchSuccess，
// 由其本服权威复检后发 MatchJoin 完成入队
func (p *matchPool) notifyMatchSuccess(teamId uint64, mp *matchPlayer) {
	app := p.app
	serverId := mp.info.ServerId
	gbId := mp.info.GbId
	target := p.target
	common.ExecuteConcurrently(func() {
		app.sendToServer(serverId, "matchSuccess", func(client *pb.GameServerClient) error {
			_, err := client.MatchSuccess(&pb.MatchSuccessMsg{TeamId: teamId, Target: target, GbId: gbId})
			return err
		})
	})
}

// notifyMatchTimeout 匹配超时异步通知
func (p *matchPool) notifyMatchTimeout(mp *matchPlayer) {
	app := p.app
	serverId := mp.info.ServerId
	gbId := mp.info.GbId
	target := p.target
	common.ExecuteConcurrently(func() {
		app.sendToServer(serverId, "matchTimeout", func(client *pb.GameServerClient) error {
			_, err := client.MatchTimeout(&pb.MatchTimeoutMsg{Target: target, GbId: gbId})
			return err
		})
	})
}

// notifyMatchStart 入池成功异步通知：客户端匹配 UI 开始倒计时（enterTS 为入池时间，
// timeoutSeconds 为本次入池生效的超时，客户端主读配表，此处冗余校准）
func (p *matchPool) notifyMatchStart(mp *matchPlayer) {
	app := p.app
	serverId := mp.info.ServerId
	gbId := mp.info.GbId
	target := p.target
	enterTS := mp.enterTS
	timeoutSeconds := mp.timeoutSeconds
	common.ExecuteConcurrently(func() {
		app.sendToServer(serverId, "matchStart", func(client *pb.GameServerClient) error {
			_, err := client.MatchStart(&pb.MatchStartMsg{
				Target:         target,
				GbId:           gbId,
				EnterTS:        enterTS,
				TimeoutSeconds: timeoutSeconds,
			})
			return err
		})
	})
}

// notifyMatchStop 取消匹配确认异步通知（撮合成功/超时分别走 MatchSuccess/MatchTimeout，不走这里）
func (p *matchPool) notifyMatchStop(mp *matchPlayer) {
	app := p.app
	serverId := mp.info.ServerId
	gbId := mp.info.GbId
	target := p.target
	common.ExecuteConcurrently(func() {
		app.sendToServer(serverId, "matchStop", func(client *pb.GameServerClient) error {
			_, err := client.MatchStop(&pb.MatchStopMsg{Target: target, GbId: gbId})
			return err
		})
	})
}

// MatchPoolMgr 按 target 分池管理，pool 惰性创建
type MatchPoolMgr struct {
	mu    sync.Mutex
	pools map[int32]*matchPool
	app   *CrossTeamApp
	// playerTarget 记录 gbId -> target 反查表（玩家同一时刻只能处于一个匹配中），
	// 供 LeaveMatchPool（不带 target）定位所属池；仅在本 mgr 锁内读写
	playerTarget map[uint64]int32
}

func NewMatchPoolMgr(app *CrossTeamApp) *MatchPoolMgr {
	return &MatchPoolMgr{
		pools:        make(map[int32]*matchPool),
		app:          app,
		playerTarget: make(map[uint64]int32),
	}
}

// EnterPool 散人入池：登记反查表后把变更投递到 target 对应 pool 的 goroutine。
// timeoutSeconds 为游戏服读配表带入的本次匹配超时，<=0 时回落中心配置 matchTimeoutSeconds
func (m *MatchPoolMgr) EnterPool(player *pb.MatchPlayerInfo, target int32, timeoutSeconds int32) {
	if timeoutSeconds <= 0 {
		timeoutSeconds = int32(matchTimeoutSeconds)
	}
	m.mu.Lock()
	m.playerTarget[player.GbId] = target
	m.mu.Unlock()

	m.do(target, "EnterMatchPool", func(p *matchPool) {
		if _, ok := p.players[player.GbId]; ok {
			// 中心 pool map 查重兜底（第一道拦截在玩家本服匹配状态）
			appLog.Warnf(
				"enter match pool duplicated, target=%d gbId=%d",
				target,
				player.GbId,
			)
			return
		}
		mp := &matchPlayer{info: player, enterTS: time.Now().Unix(), timeoutSeconds: timeoutSeconds}
		p.players[player.GbId] = mp
		p.dirty = true
		// 入池成功通知：客户端匹配 UI 开始倒计时
		p.notifyMatchStart(mp)
		appLog.Infof(
			"enter match pool, target=%d gbId=%d serverId=%d timeout=%ds",
			target,
			player.GbId,
			player.ServerId,
			timeoutSeconds,
		)
	})
}

// LeavePool 散人取消匹配：按反查表定位池并移除，确认取消后推 MatchStop
func (m *MatchPoolMgr) LeavePool(gbId uint64) {
	m.mu.Lock()
	target, ok := m.playerTarget[gbId]
	if ok {
		delete(m.playerTarget, gbId)
	}
	m.mu.Unlock()
	if !ok {
		appLog.Warnf(
			"leave match pool but not in pool, gbId=%d",
			gbId,
		)
		return
	}

	m.do(target, "LeaveMatchPool", func(p *matchPool) {
		mp, ok := p.players[gbId]
		if !ok {
			return
		}
		delete(p.players, gbId)
		p.notifyMatchStop(mp)
		appLog.Infof(
			"leave match pool, target=%d gbId=%d",
			target,
			gbId,
		)
	})
}

// RemovePlayer 玩家入队/离线等情况下的强制出池（不告警），供队伍 worker 调用
func (m *MatchPoolMgr) RemovePlayer(gbId uint64) {
	m.mu.Lock()
	target, ok := m.playerTarget[gbId]
	if ok {
		delete(m.playerTarget, gbId)
	}
	m.mu.Unlock()
	if !ok {
		return
	}
	m.do(target, "RemovePlayer", func(p *matchPool) {
		delete(p.players, gbId)
	})
}

// clearPlayer 仅清反查表（配对/超时时散人已不在 pool map 中，由 pool goroutine 调用）
func (m *MatchPoolMgr) clearPlayer(gbId uint64) {
	m.mu.Lock()
	delete(m.playerTarget, gbId)
	m.mu.Unlock()
}

// UpsertTeamSummary 队伍摘要事件同步（team worker 调用）：
// 队伍创建/成员进出/目标门槛或 autoMatch 变更时投到对应 target 的 pool goroutine
func (m *MatchPoolMgr) UpsertTeamSummary(ts *teamSummary) {
	m.do(ts.target, "UpsertTeamSummary", func(p *matchPool) {
		p.teams[ts.teamId] = ts
		// 出现可撮合的空位队伍也视为撮合触发源（池内可能已有等待的散人）
		if ts.matchable && p.freeSlots(ts) > 0 {
			p.dirty = true
		}
	})
}

// RemoveTeamSummary 队伍解散/目标改走/InDungeon 时摘除摘要
func (m *MatchPoolMgr) RemoveTeamSummary(teamId uint64, target int32) {
	m.do(target, "RemoveTeamSummary", func(p *matchPool) {
		delete(p.teams, teamId)
	})
}

// do 把操作投递到 target 对应 pool 的 goroutine（pool 不存在则惰性创建）
func (m *MatchPoolMgr) do(target int32, name string, fn func(p *matchPool)) {
	m.mu.Lock()
	pool, ok := m.pools[target]
	if !ok {
		pool = newMatchPool(target, m.app)
		m.pools[target] = pool
	}
	m.mu.Unlock()
	pool.opChan <- matchPoolOp{name, fn}
}

// chatItem 上行的一条队伍聊天消息
type chatItem struct {
	teamId uint64
	msg    *pb.ChatMsg
}

// ChatBuffer 聊天聚合缓冲：map[teamId] -> []ChatMsg，
// 由独立 goroutine 持有，0.5s 定时 flush。
// flush 时按 teamId 把批量消息投回该队伍所属 worker，由 worker 读成员表
// 按所在服分组推送 TeamChatBatch（队伍数据只有 worker 能碰）。
// 中心只做转发，敏感词检查在发送方本服完成。
type ChatBuffer struct {
	dispatcher *TeamDispatcher
	addChan    chan chatItem
}

func NewChatBuffer(dispatcher *TeamDispatcher) *ChatBuffer {
	b := &ChatBuffer{dispatcher: dispatcher, addChan: make(chan chatItem, 4096)}
	common.ExecuteConcurrently(b.run)
	return b
}

func (b *ChatBuffer) Add(teamId uint64, msg *pb.ChatMsg) {
	b.addChan <- chatItem{teamId, msg}
}

func (b *ChatBuffer) run() {
	buf := make(map[uint64][]*pb.ChatMsg)
	ticker := time.NewTicker(CHAT_FLUSH_MS * time.Millisecond)
	defer ticker.Stop()
	for {
		select {
		case item := <-b.addChan:
			buf[item.teamId] = append(buf[item.teamId], item.msg)
		case <-ticker.C:
			for teamId, msgs := range buf {
				if len(msgs) == 0 {
					delete(buf, teamId)
					continue
				}
				batch := msgs
				b.dispatcher.Dispatch(teamId, "ChatFlush", func(w *teamWorker) {
					b.dispatcher.app.flushTeamChat(w, teamId, batch)
				})
				delete(buf, teamId)
			}
		}
	}
}
