package LeaseApp

import (
	"centralService/src/appLog"
	"centralService/src/common"
	cmap "centralService/src/common/concurrent_map"
	gameServerService "centralService/src/leaseServer/leaseApp/gameServerService"
	"centralService/src/trpc"
	"container/heap"
	"database/sql"
	"fmt"
	"math"
	"net"
	"sync"
	"syscall"
	"time"

	_ "github.com/go-sql-driver/mysql"
	"github.com/google/btree"
	"github.com/google/uuid"
)

var LeaseConfig = AppConfig{}

const (
	_                   = iota
	SERVICE_GAME_SERVER // 游戏服务器服务类型标识
)

// ==================== 常量 ====================
const (
	_                     = iota
	LEASE_STATUS_PREPARE  // 预上架（临时状态）
	LEASE_STATUS_ON_SALE  // 上架中
	LEASE_STATUS_LEASED   // 已租出
	LEASE_STATUS_CANCELED // 已下架（下架后延迟删除）
	LEASE_STATUS_PRE_LOCK // 预锁定（临时状态）
	LEASE_STATUS_EXPIRED  // 已自动下架（等待取回）
)

const (
	LEASE_OK = iota
	LEASE_NOT_FOUND
	LEASE_ITEM_LOCKED
	LEASE_PARAM_ERROR
	LEASE_STATUS_ERROR
	LEASE_ALREADY_EXISTS
	LEASE_NOT_OWNER
	LEASE_TIMEOUT
	LEASE_IN_COOLDOWN
	LEASE_DB_ERROR
	LEASE_RATE_LIMIT
	LEASE_SELF_LEASE
	LEASE_SHELF_FULL
)

const (
	_            = iota
	RETURN_DROP  // 归还原因：爆装
	RETURN_LEASE // 归还原因：租赁
)

// ==================== 内存数据结构 ====================

// 有两种出租类型：
// 1. 爆来的装备按固定归还时间：由 ReturnXXX 几个字段计算时间
// 2. 玩家自己出租按租期：由 LeaseDay 字段计算时间
// 对于原主出租的装备不设置 ReturnXXX 值
type LeaseMarketItem struct {
	UniqueId            uint64 // 装备全局唯一 ID
	ItemId              uint32 // 装备配置 ID
	ReturnOwnerGbId     uint64 // 最终归还目标玩家 gbId（链条顶端原主人）
	ReturnOwnerServerId uint32 // 最终归还目标玩家所在服 ID
	ReturnEndTime       uint32 // 归还/到期截止时间
	ReturnReason        uint32 // 归还原因：0=未设置/不退回 1=爆装(RETURN_DROP) 2=租赁(RETURN_LEASE)
	LessorGbId          uint64 // 当前出租方玩家 gbId
	LessorServerId      uint32 // 当前出租方所在服 ID
	LesseeGbId          uint64 // 当前承租方玩家 gbId
	LesseeServerId      uint32 // 当前承租方所在服 ID
	PricePerDay         int64  // 每日租金（流通金）
	LeaseDay            uint32 // 租赁天数（自身装备使用）
	ItemData            string // 装备序列化 JSON 数据
	Status              uint8  // 订单状态：见 LEASE_STATUS_xxx 常量
	AddTime             int64  // 上架/记录创建时间

	// 出租预成交时计算以下参数
	LeaseStartTime uint32 // 本次租赁开始时间
	LeaseEndTime   uint32 // 本次租赁结束时间
	LeaseCost      int64  // leess 花费租金
	LeaseGold      int64  // lessor 获得租金
	LeaseBindGold  int64  // lessor 获得绑定金
	LeaseTax       int64  // 税金（从租金中扣除）

	PendingOpUUID uint64 // 当前中间状态（PREPARE/PRE_LOCK）所属流程的 opUUID，commit/rollback 必须携带相同值才生效；清扫器也用它识别脏条目

	mu sync.Mutex // 保护 Status 及相关字段的并发访问
}

func (a *LeaseMarketItem) Less(other btree.Item) bool {
	b := other.(*LeaseMarketItem)
	if a.PricePerDay != b.PricePerDay {
		return a.PricePerDay < b.PricePerDay
	}
	if a.AddTime != b.AddTime {
		return a.AddTime > b.AddTime
	}
	return a.UniqueId < b.UniqueId
}

// checkSetStatus 原子 check-and-set：当且仅当前状态为 from 时，才将其改为 to
func (a *LeaseMarketItem) checkSetStatus(from, to uint8) bool {
	a.mu.Lock()
	defer a.mu.Unlock()
	if a.Status != from {
		return false
	}
	a.Status = to
	return true
}

// checkSetStatusAny 原子 check-and-set：当状态为 from 列表中的任意一个时，才将其改为 to，并返回原状态
func (a *LeaseMarketItem) checkSetStatusAny(from []uint8, to uint8) (uint8, bool) {
	a.mu.Lock()
	defer a.mu.Unlock()
	for _, f := range from {
		if a.Status == f {
			old := a.Status
			a.Status = to
			return old, true
		}
	}
	return a.Status, false
}

// checkSetStatusWithOp 原子 check-and-set：状态为 from 且 PendingOpUUID 匹配时，才将其改为 to
// 用于拒绝上一流程迟到（如超时清扫恢复之后）的 commit 消息
func (a *LeaseMarketItem) checkSetStatusWithOp(from, to uint8, opUUID uint64) bool {
	a.mu.Lock()
	defer a.mu.Unlock()
	if a.Status != from || a.PendingOpUUID != opUUID {
		return false
	}
	a.Status = to
	return true
}

// LockedBTree 带锁的 BTree，用于高并发索引
type LockedBTree struct {
	tree *btree.BTreeG[*LeaseMarketItem]
	mu   *sync.RWMutex
}

func NewLockedBTree() *LockedBTree {
	return &LockedBTree{
		tree: btree.NewG(32, func(a, b *LeaseMarketItem) bool { return a.Less(b) }),
		mu:   &sync.RWMutex{},
	}
}

func uint32Shard(key uint32) uint32 {
	return key
}

func uint64Shard(key uint64) uint32 {
	return uint32(key) ^ uint32(key>>32)
}

// ==================== 过期调度器 ====================

// expireEntry 过期调度条目
type expireEntry struct {
	uniqueId uint64
	expireAt int64
}

// expireHeap 按过期时间排序的最小堆
type expireHeap []expireEntry

func (h expireHeap) Len() int           { return len(h) }
func (h expireHeap) Less(i, j int) bool { return h[i].expireAt < h[j].expireAt }
func (h expireHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }

func (h *expireHeap) Push(x interface{}) {
	*h = append(*h, x.(expireEntry))
}

func (h *expireHeap) Pop() interface{} {
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[:n-1]
	return x
}

// ==================== LeaseMgr ====================

// LeaseMgr 租赁市场内存管理器
type LeaseMgr struct {
	db *sql.DB // MySQL 连接

	// 数据及索引
	items         cmap.ConcurrentMap[uint64, *LeaseMarketItem] // uniqueId -> 租赁物品主数据
	itemIdIndex   cmap.ConcurrentMap[uint32, *LockedBTree]     // itemId -> 按价格和上架时间排序的 BTree
	playerIdIndex cmap.ConcurrentMap[uint64, *LockedBTree]     // playerGbId -> 该玩家的出租物品 BTree

	auctionConst *AuctionConstConfig // 拍卖行常量配置（租赁服务复用）

	// 过期调度器（集中式最小堆）
	expireHeap *expireHeap
	expireMu   sync.Mutex
	expireWake chan struct{}

	// 中间状态清扫事件（add/del）传递通道，由清扫 goroutine 单向消费，生产侧无锁
	pendingCh chan pendingOp
}

func NewLeaseMgr(db *sql.DB, auctionConst *AuctionConstConfig) *LeaseMgr {
	h := &expireHeap{}
	heap.Init(h)
	return &LeaseMgr{
		db:            db,
		items:         cmap.NewWithCustomShardingFunction[uint64, *LeaseMarketItem](uint64Shard),
		itemIdIndex:   cmap.NewWithCustomShardingFunction[uint32, *LockedBTree](uint32Shard),
		playerIdIndex: cmap.NewWithCustomShardingFunction[uint64, *LockedBTree](uint64Shard),
		auctionConst:  auctionConst,
		expireHeap:    h,
		expireWake:    make(chan struct{}, 1),
		pendingCh:     make(chan pendingOp, pendingChanBuf),
	}
}

func (lm *LeaseMgr) loadFromDB() error {
	return lm.dbLoadItems(func(item *LeaseMarketItem) error {
		switch item.Status {
		case LEASE_STATUS_ON_SALE:
			lm.items.Set(item.UniqueId, item)
			lm._addToPlayerIdIndex(item)

			expireAt := item.AddTime + int64(lm.auctionConst.RentalAutoUnlist)*3600
			if expireAt <= time.Now().Unix() {
				// 已经过期，直接置为 EXPIRED
				if item.checkSetStatus(LEASE_STATUS_ON_SALE, LEASE_STATUS_EXPIRED) {
					lm._removeFromItemIdIndex(item)
					if err := lm.dbSetItemExpiredCAS(item, uint32(time.Now().Unix())); err != nil {
						appLog.Errorw("loadFromDB set expired failed", "uniqueId", item.UniqueId, "err", err)
					}
				}
			} else {
				lm._addToItemIdIndex(item)
				lm.pushExpire(item.UniqueId, expireAt)
			}
		case LEASE_STATUS_EXPIRED:
			// 已过期未取回，保留在玩家索引中
			lm.items.Set(item.UniqueId, item)
			lm._addToPlayerIdIndex(item)
		}
		// 租出状态不再加载到内存，由 Avatar 端自行管理到期
		return nil
	})
}

// ==================== 玩家上架数量 ====================

// getPlayerOnSaleCount 通过 playerIdIndex 统计玩家当前上架中（ON_SALE）和自动下架待取回（EXPIRED）的物品数量
func (lm *LeaseMgr) getPlayerOnSaleCount(playerGbId uint64) int32 {
	t, ok := lm.playerIdIndex.Get(playerGbId)
	if !ok {
		return 0
	}

	t.mu.RLock()
	count := int32(t.tree.Len())
	t.mu.RUnlock()
	return count
}

// ==================== 过期调度器 ====================

func (lm *LeaseMgr) pushExpire(uniqueId uint64, expireAt int64) {
	lm.expireMu.Lock()
	heap.Push(lm.expireHeap, expireEntry{uniqueId: uniqueId, expireAt: expireAt})
	lm.expireMu.Unlock()

	select {
	case lm.expireWake <- struct{}{}:
	default:
	}
}

func (lm *LeaseMgr) startExpireScheduler() {
	for {
		lm.expireMu.Lock()
		now := time.Now().Unix()

		for lm.expireHeap.Len() > 0 {
			top := (*lm.expireHeap)[0]
			if top.expireAt > now {
				break
			}
			heap.Pop(lm.expireHeap)
			lm.expireMu.Unlock()
			lm.processExpire(top.uniqueId)
			lm.expireMu.Lock()
		}

		var wait time.Duration
		if lm.expireHeap.Len() > 0 {
			wait = time.Duration((*lm.expireHeap)[0].expireAt-now) * time.Second
			if wait < 0 {
				wait = 0
			}
		} else {
			wait = time.Hour
		}
		lm.expireMu.Unlock()

		timer := time.NewTimer(wait)
		select {
		case <-timer.C:
		case <-lm.expireWake:
			// stop-and-drain：等待被新条目打断时安全清理旧定时器。
			// 注意：此写法仅在 go.mod 声明 go < 1.23（异步缓冲定时器语义）下正确且必需；
			// Go 1.23 起定时器 channel 改为同步语义，Stop 会撤回未配对的旧发送，
			// 若升级 go.mod 到 1.23+，此处必须改为裸的 timer.Stop()，否则 drain 将永久阻塞。
			if !timer.Stop() {
				<-timer.C
			}
		}
	}
}

func (lm *LeaseMgr) processExpire(uniqueId uint64) {
	appLog.Infow("processExpire", "uniqueId", uniqueId)
	item, ok := lm.items.Get(uniqueId)
	if !ok {
		return
	}

	if !item.checkSetStatus(LEASE_STATUS_ON_SALE, LEASE_STATUS_EXPIRED) {
		return
	}

	lm._removeFromItemIdIndex(item)

	now := uint32(time.Now().Unix())
	if err := lm.dbSetItemExpiredCAS(item, now); err != nil {
		appLog.Errorw("processExpire db failed", "uniqueId", uniqueId, "err", err)
	}
}

// ==================== 中间状态超时清扫 ====================

// stuckSweepInterval 中间状态清扫间隔
const stuckSweepInterval = 10 * time.Second

// pendingChanBuf 清扫事件通道缓冲，按清扫间隔内的 prepare 峰值估算
// add/del 事件缓冲满时均直接丢弃（主流程稳定优先，代价见 _sendPendingAdd 注释）
const pendingChanBuf = 65536

// pendingEntry 中间状态待清扫条目，进入 PREPARE / PRE_LOCK 时生成
type pendingEntry struct {
	uniqueId uint64
	status   uint8  // 进入的中间状态：LEASE_STATUS_PREPARE / LEASE_STATUS_PRE_LOCK
	opUUID   uint64 // 该中间状态所属流程
	enterAt  int64  // 进入时间戳（秒）
}

// pendingOp 清扫事件：add=进入中间状态，del=流程已正常流转（可从待清扫集合移除）
type pendingOp struct {
	entry pendingEntry
	del   bool
}

// _sendPendingAdd 上报进入中间状态。缓冲满时直接丢弃，绝不阻塞主流程：
// 代价是这部分中间状态若卡住将无法被清扫（退化为优化前的行为），可接受
func (lm *LeaseMgr) _sendPendingAdd(uniqueId uint64, status uint8, opUUID uint64) {
	op := pendingOp{entry: pendingEntry{
		uniqueId: uniqueId,
		status:   status,
		opUUID:   opUUID,
		enterAt:  time.Now().Unix(),
	}}
	select {
	case lm.pendingCh <- op:
	default:
		appLog.Errorw("pending channel full, add event dropped", "uniqueId", uniqueId)
	}
}

// _sendPendingDel 上报中间状态流程已结束。丢失安全：
// 对应 add 条目超时后会因 状态/opUUID 不匹配 被清扫器跳过
// 携带 opUUID：跨 goroutine 下 del 可能排到同一物品新流程的 add 之后，
// 清扫器仅当 opUUID 匹配时才删除，避免误删新流程的条目
func (lm *LeaseMgr) _sendPendingDel(uniqueId uint64, opUUID uint64) {
	op := pendingOp{del: true}
	op.entry.uniqueId = uniqueId
	op.entry.opUUID = opUUID
	select {
	case lm.pendingCh <- op:
	default:
	}
}

// startStuckSweeper 清扫卡在 PREPARE / PRE_LOCK 中间状态的物品
// 正常流程 prepare -> commit 秒级完成，超时未完成说明游戏服流程已中断（进程异常等）：
//   - PREPARE：物品只在内存，墓碑化后直接从主数据删除，uniqueId 释放
//   - PRE_LOCK：恢复为上架状态（DB 本来就是 ON_SALE，无需写库）
//
// 单 goroutine 同时消费 add/del 事件与 tick：事件即时处理（缓冲不积压），
// tick 被事件流抢占时顺延到下一个即可（清扫不要求准时）。
// 待清扫集合 pending 由本 goroutine 独占（正常流转的条目经 del 事件移除，
// 常态只剩极少数在途条目），无需任何锁
func (lm *LeaseMgr) startStuckSweeper(timeoutSec int64) {
	pending := make(map[uint64]pendingEntry)
	ticker := time.NewTicker(stuckSweepInterval)
	defer ticker.Stop()
	for {
		select {
		case op := <-lm.pendingCh:
			if op.del {
				// 仅删除本流程自己的条目，防止乱序 del 误删新流程的 add
				if e, ok := pending[op.entry.uniqueId]; ok && e.opUUID == op.entry.opUUID {
					delete(pending, op.entry.uniqueId)
				}
			} else {
				// 覆盖一定是以新换旧，无需校验时间：同一 uniqueId 的新流程只能在旧物品
				// 离开中间状态后发起，而旧流程的 add 在进入中间状态时已发送，
				// happens-before 于任何恢复/删除动作，故旧 add 不可能晚于新 add 到达
				pending[op.entry.uniqueId] = op.entry
			}
		case t := <-ticker.C:
			appLog.Debugw("tick stuck sweeper.")
			now := t.Unix()
			for uniqueId, e := range pending {
				if now-e.enterAt < timeoutSec {
					continue
				}
				delete(pending, uniqueId)
				lm._processPendingEntry(e, now)
			}
		}
	}
}

// _processPendingEntry 处理一个已超时的中间状态条目
// 脏条目（del 丢失、或 add/del 乱序留下的）会因 状态/opUUID 不匹配 被直接跳过
func (lm *LeaseMgr) _processPendingEntry(e pendingEntry, now int64) {
	item, ok := lm.items.Get(e.uniqueId)
	if !ok {
		return
	}
	item.mu.Lock()
	defer item.mu.Unlock()

	if item.Status != e.status || item.PendingOpUUID != e.opUUID {
		return
	}

	switch e.status {
	case LEASE_STATUS_PREPARE:
		// 墓碑化：使并发（迟到）的 addItemCommit CAS 必失败，走游戏服返还流程
		item.Status = LEASE_STATUS_CANCELED
		item.PendingOpUUID = 0
		lm.items.Remove(item.UniqueId)
		appLog.Warnw("sweep stuck PREPARE item", "uniqueId", e.uniqueId, "lessor", item.LessorGbId, "itemId", item.ItemId, "stuckSec", now-e.enterAt)
	case LEASE_STATUS_PRE_LOCK:
		appLog.Warnw("sweep stuck PRE_LOCK item", "uniqueId", e.uniqueId, "lessor", item.LessorGbId, "lessee", item.LesseeGbId, "itemId", item.ItemId, "stuckSec", now-e.enterAt)
		lm._restoreToOnSaleLocked(item)
	}
}

// ==================== 数据库历史数据清理 ====================

// dbCleanBatchInterval 批量删除的批间隔，避免长时间占用影响在线读写
const dbCleanBatchInterval = 500 * time.Millisecond

// startDBCleaner 周期清理 lease_market 中的历史数据（只触碰终态行，与主流程不相交）：
//   - CANCELED 行：下架流程结束即为历史，宽限期后删除
//     （CANCELED 行是下架回包丢失时装备的唯一副本，宽限期即人工补救窗口）
//   - LEASED 行：租约结束（lease_end_time）后即为历史，宽限期后删除
func (lm *LeaseMgr) startDBCleaner(intervalHours, batchSize, graceDays int) {
	ticker := time.NewTicker(time.Duration(intervalHours) * time.Hour)
	defer ticker.Stop()
	for range ticker.C {
		graceBefore := uint32(time.Now().Unix() - int64(graceDays)*86400)
		lm._cleanLoop("canceled", batchSize, func() (int64, error) {
			return lm.dbCleanCanceledBatch(batchSize, graceBefore)
		})
		lm._cleanLoop("leased", batchSize, func() (int64, error) {
			return lm.dbCleanLeasedBatch(batchSize, graceBefore)
		})
	}
}

// _cleanLoop 小批量循环删除：每批 batchSize 行，批间停顿，删不足一批即结束；出错只记日志等下轮
func (lm *LeaseMgr) _cleanLoop(name string, batchSize int, doBatch func() (int64, error)) {
	var total int64
	for {
		affected, err := doBatch()
		if err != nil {
			appLog.Errorw("db clean batch failed", "type", name, "err", err)
			return
		}
		total += affected
		if affected < int64(batchSize) {
			break
		}
		time.Sleep(dbCleanBatchInterval)
	}
	if total > 0 {
		appLog.Infow("db clean done", "type", name, "rows", total)
	}
}

func (lm *LeaseMgr) _getItemIdBtree(itemId uint32) *LockedBTree {
	t, _ := lm.itemIdIndex.GetOrCreate(itemId, func() *LockedBTree {
		return NewLockedBTree()
	})
	return t
}

func (lm *LeaseMgr) _getPlayerIdBtree(playerGbId uint64) *LockedBTree {
	t, _ := lm.playerIdIndex.GetOrCreate(playerGbId, func() *LockedBTree {
		return NewLockedBTree()
	})
	return t
}

func (lm *LeaseMgr) _addToItemIdIndex(item *LeaseMarketItem) {
	t := lm._getItemIdBtree(item.ItemId)
	t.mu.Lock()
	t.tree.ReplaceOrInsert(item)
	t.mu.Unlock()
}

func (lm *LeaseMgr) _removeFromItemIdIndex(item *LeaseMarketItem) {
	t, ok := lm.itemIdIndex.Get(item.ItemId)
	if !ok {
		return
	}
	t.mu.Lock()
	t.tree.Delete(item)
	t.mu.Unlock()
}

func (lm *LeaseMgr) _addToPlayerIdIndex(item *LeaseMarketItem) {
	t := lm._getPlayerIdBtree(item.LessorGbId)
	t.mu.Lock()
	t.tree.ReplaceOrInsert(item)
	t.mu.Unlock()
}

func (lm *LeaseMgr) _removeFromPlayerIdIndex(item *LeaseMarketItem) {
	t, ok := lm.playerIdIndex.Get(item.LessorGbId)
	if !ok {
		return
	}
	t.mu.Lock()
	t.tree.Delete(item)
	t.mu.Unlock()
}

// ==================== 核心操作 ====================

func (lm *LeaseMgr) addItemPrepare(item *LeaseMarketItem, opUUID uint64) int {
	limit := int32(lm.auctionConst.RentalInitShelfNum)
	if lm.getPlayerOnSaleCount(item.LessorGbId) >= limit {
		return LEASE_SHELF_FULL
	}

	now := time.Now().Unix()
	item.AddTime = now
	item.Status = LEASE_STATUS_PREPARE
	item.PendingOpUUID = opUUID
	if !lm.items.SetIfAbsent(item.UniqueId, item) {
		return LEASE_ALREADY_EXISTS
	}
	lm._sendPendingAdd(item.UniqueId, LEASE_STATUS_PREPARE, opUUID)
	return LEASE_OK
}

func (lm *LeaseMgr) addItemCommit(uniqueId uint64, opUUID uint64) int {
	item, ok := lm.items.Get(uniqueId)
	if !ok {
		return LEASE_NOT_FOUND
	}
	if !item.checkSetStatusWithOp(LEASE_STATUS_PREPARE, LEASE_STATUS_ON_SALE, opUUID) {
		return LEASE_STATUS_ERROR
	}
	lm._sendPendingDel(uniqueId, opUUID)

	// 入库
	if err := lm.dbAddItemCommit(item); err != nil {
		appLog.Errorw("addItemCommit db error", "uniqueId", item.UniqueId, "err", err)
		lm.items.Remove(uniqueId)
		return LEASE_DB_ERROR
	}

	lm._addToItemIdIndex(item)
	lm._addToPlayerIdIndex(item)

	expireAt := item.AddTime + int64(lm.auctionConst.RentalAutoUnlist)*3600
	appLog.Debugw("addItemCommit expireAt", "uniqueId", item.UniqueId, "expireAt", expireAt)
	lm.pushExpire(item.UniqueId, expireAt)

	return LEASE_OK
}

func (lm *LeaseMgr) addItemRollback(uniqueId uint64, opUUID uint64) int {
	item, ok := lm.items.Get(uniqueId)
	if !ok {
		return LEASE_OK
	}
	item.mu.Lock()
	defer item.mu.Unlock()

	if item.Status != LEASE_STATUS_PREPARE {
		appLog.Error("addItemRollback status err", uniqueId, item.Status)
		return LEASE_STATUS_ERROR
	}

	// 迟到（如超时清扫之后）的 rollback，忽略
	if item.PendingOpUUID != opUUID {
		appLog.Warnw("addItemRollback opUUID mismatch, ignored", "uniqueId", uniqueId, "opUUID", opUUID, "pendingOpUUID", item.PendingOpUUID)
		return LEASE_STATUS_ERROR
	}

	lm.items.Remove(uniqueId)
	lm._sendPendingDel(uniqueId, opUUID)

	return LEASE_OK
}

func (lm *LeaseMgr) leaseItemPrepare(uniqueId uint64, buyerGbId uint64, buyerServerId uint32, opUUID uint64, rentalProp01, rentalProp02 []float64) (int64, int) {
	item, ok := lm.items.Get(uniqueId)
	if !ok {
		return 0, LEASE_NOT_FOUND
	}
	item.mu.Lock()
	defer item.mu.Unlock()

	if item.Status != LEASE_STATUS_ON_SALE {
		return 0, LEASE_STATUS_ERROR
	}

	if item.LessorGbId == buyerGbId {
		return 0, LEASE_SELF_LEASE
	}

	now := uint32(time.Now().Unix())
	if item.ReturnEndTime > 0 && item.ReturnEndTime < now+uint32(lm.auctionConst.RentalTimelimit)*86400 {
		return 0, LEASE_TIMEOUT
	}

	// 费率由游戏服透传（游戏服支持热更配置）：[0]=税率 [2]=流通金比例，按装备类型选取
	prop := rentalProp01
	if item.ReturnReason > 0 {
		prop = rentalProp02
	}
	if len(prop) < 3 {
		return 0, LEASE_PARAM_ERROR
	}
	taxRate := prop[0]
	goldRate := prop[2]

	item.Status = LEASE_STATUS_PRE_LOCK
	item.PendingOpUUID = opUUID
	lm._sendPendingAdd(uniqueId, LEASE_STATUS_PRE_LOCK, opUUID)

	item.LeaseStartTime = uint32(now)
	if item.ReturnReason > 0 {
		item.LeaseEndTime = item.ReturnEndTime // 固定归还时间
	} else {
		item.LeaseEndTime = item.LeaseStartTime + item.LeaseDay*86400 // 从此刻开始计算租期
	}

	pricePerMinute := float64(item.PricePerDay) / 24.0 / 60.0
	remainMinutes := (float64(item.LeaseEndTime) - float64(now)) / 60.0

	item.LeaseCost = int64(math.Round(pricePerMinute * remainMinutes))
	item.LeaseTax = int64(math.Ceil(float64(item.LeaseCost) * taxRate))
	item.LeaseGold = int64(math.Ceil(float64(item.LeaseCost) * goldRate))
	item.LeaseBindGold = item.LeaseCost - item.LeaseTax - item.LeaseGold
	if item.LeaseBindGold < 0 {
		// 防御：taxRate+goldRate 配置接近 1 且租金很小时，双重 Ceil 可能把绑定金算成负数
		item.LeaseBindGold = 0
	}

	item.LesseeGbId = buyerGbId
	item.LesseeServerId = buyerServerId
	lm._removeFromItemIdIndex(item)
	lm._removeFromPlayerIdIndex(item)

	return item.LeaseCost, LEASE_OK
}

func (lm *LeaseMgr) leaseItemCommit(uniqueId uint64, opUUID uint64) (*LeaseMarketItem, int) {
	item, ok := lm.items.Get(uniqueId)
	if !ok {
		return nil, LEASE_NOT_FOUND
	}

	if !item.checkSetStatusWithOp(LEASE_STATUS_PRE_LOCK, LEASE_STATUS_LEASED, opUUID) {
		return item, LEASE_STATUS_ERROR
	}
	lm._sendPendingDel(uniqueId, opUUID)

	now := uint32(time.Now().Unix())
	if err := lm.dbLeaseItemCommitCAS(item, now, LEASE_STATUS_ON_SALE); err != nil {
		appLog.Errorw("leaseItemCommit db error", "uniqueId", item.UniqueId, "err", err)

		// 写库失败，这里重新回滚到上架状态
		item.mu.Lock()
		lm._restoreToOnSaleLocked(item)
		item.mu.Unlock()
		return item, LEASE_DB_ERROR
	}

	// 租赁成交后从内存中移除，由 Avatar 端管理到期归还
	lm.items.Remove(item.UniqueId)

	return item, LEASE_OK
}

func (lm *LeaseMgr) leaseItemRollback(uniqueId uint64, opUUID uint64) int {
	item, ok := lm.items.Get(uniqueId)
	if !ok {
		return LEASE_NOT_FOUND
	}
	item.mu.Lock()
	defer item.mu.Unlock()

	if item.Status != LEASE_STATUS_PRE_LOCK {
		return LEASE_STATUS_ERROR
	}

	// 迟到（如超时清扫恢复之后）的 rollback，忽略，避免误回滚新流程的 PRE_LOCK
	if item.PendingOpUUID != opUUID {
		appLog.Warnw("leaseItemRollback opUUID mismatch, ignored", "uniqueId", uniqueId, "opUUID", opUUID, "pendingOpUUID", item.PendingOpUUID)
		return LEASE_STATUS_ERROR
	}

	lm._restoreToOnSaleLocked(item)
	lm._sendPendingDel(uniqueId, opUUID)

	return LEASE_OK
}

// _restoreToOnSaleLocked 将 PRE_LOCK 物品恢复为上架状态：重置租赁字段、加回索引、重新调度自动下架
// 调用方必须持有 item.mu，保证状态变更与索引操作的原子性
func (lm *LeaseMgr) _restoreToOnSaleLocked(item *LeaseMarketItem) {
	item.Status = LEASE_STATUS_ON_SALE
	item.LesseeGbId = 0
	item.LesseeServerId = 0
	item.LeaseStartTime = 0
	item.LeaseEndTime = 0
	item.LeaseCost = 0
	item.LeaseGold = 0
	item.LeaseBindGold = 0
	item.LeaseTax = 0
	item.PendingOpUUID = 0
	lm._addToItemIdIndex(item)
	lm._addToPlayerIdIndex(item)

	// 重新调度自动下架：PRE_LOCK 期间原调度条目可能已触发并被丢弃
	expireAt := item.AddTime + int64(lm.auctionConst.RentalAutoUnlist)*3600
	lm.pushExpire(item.UniqueId, expireAt)
}

func (lm *LeaseMgr) cancelItem(uniqueId uint64, playerGBID uint64) (*LeaseMarketItem, int) {
	item, ok := lm.items.Get(uniqueId)
	if !ok {
		return nil, LEASE_NOT_FOUND
	}

	// lessor 不会变，先判断 owner，不需要加锁
	if item.LessorGbId != playerGBID {
		return item, LEASE_NOT_OWNER
	}

	oldStatus, ok := item.checkSetStatusAny(
		[]uint8{LEASE_STATUS_ON_SALE, LEASE_STATUS_EXPIRED},
		LEASE_STATUS_CANCELED,
	)
	if !ok {
		return item, LEASE_STATUS_ERROR
	}

	now := uint32(time.Now().Unix())
	if err := lm.dbCancelItemCAS(item, now, oldStatus); err != nil {
		appLog.Errorw("cancelItem db error", "uniqueId", item.UniqueId, "err", err)
		// 写库失败，回滚到原来的状态
		item.mu.Lock()
		item.Status = oldStatus
		item.mu.Unlock()
		return item, LEASE_DB_ERROR
	}

	lm._removeFromItemIdIndex(item)
	lm._removeFromPlayerIdIndex(item)
	lm.items.Remove(uniqueId)

	return item, LEASE_OK
}

func (lm *LeaseMgr) getShopSummary(itemIds []uint32) []*gameServerService.LeaseShopSummaryItem {
	result := make([]*gameServerService.LeaseShopSummaryItem, 0)
	for _, itemId := range itemIds {
		lockedBTree, ok := lm.itemIdIndex.Get(itemId)
		if !ok {
			continue
		}

		now := uint32(time.Now().Unix())

		onSaleCount := uint32(0)
		minPrice := int64(math.MaxInt64)
		lockedBTree.mu.RLock()
		lockedBTree.tree.Ascend(func(item *LeaseMarketItem) bool {
			if item.Status != LEASE_STATUS_ON_SALE {
				return true
			}
			if item.ReturnEndTime > 0 && item.ReturnEndTime < now+uint32(lm.auctionConst.RentalTimelimit)*86400 {
				return true
			}

			onSaleCount++
			if item.PricePerDay < minPrice {
				minPrice = item.PricePerDay
			}
			return true
		})
		lockedBTree.mu.RUnlock()

		if onSaleCount > 0 {
			result = append(result, &gameServerService.LeaseShopSummaryItem{
				ItemId:      itemId,
				OnSaleCount: onSaleCount,
				MinPrice:    minPrice,
			})
		}
	}
	return result
}

func (lm *LeaseMgr) getShopItems(itemId uint32, page uint32, pageSize uint32) []*LeaseMarketItem {
	t, ok := lm.itemIdIndex.Get(itemId)
	if !ok {
		return nil
	}

	skip := int(page * pageSize)
	need := int(pageSize)

	items := make([]*LeaseMarketItem, 0, need)
	skipped := 0
	now := uint32(time.Now().Unix())

	t.mu.RLock()
	t.tree.Ascend(func(item *LeaseMarketItem) bool {
		if item.Status != LEASE_STATUS_ON_SALE {
			return true
		}
		if item.ReturnEndTime > 0 && item.ReturnEndTime < now+uint32(lm.auctionConst.RentalTimelimit)*86400 {
			return true
		}

		if skipped < skip {
			skipped++
			return true
		}

		items = append(items, item)
		if len(items) >= need {
			return false
		}
		return true
	})
	t.mu.RUnlock()

	if len(items) == 0 {
		return nil
	}
	return items
}

func (lm *LeaseMgr) getMySaleList(playerGBID uint64) []*LeaseMarketItem {
	t, ok := lm.playerIdIndex.Get(playerGBID)
	if !ok {
		return nil
	}

	t.mu.RLock()
	items := make([]*LeaseMarketItem, 0, t.tree.Len())
	t.tree.Ascend(func(item *LeaseMarketItem) bool {
		if item.Status != LEASE_STATUS_ON_SALE && item.Status != LEASE_STATUS_EXPIRED {
			return true
		}
		items = append(items, item)
		return true
	})
	t.mu.RUnlock()
	return items
}

// ==================== LeaseApp ====================

// GameServerInfo 已注册游戏服的信息
type GameServerInfo struct {
	serverName   string               // 游戏服名称
	LeaseService trpc.IServerEndPoint // 租赁服务 RPC 端点
	rwLock       *sync.RWMutex        // 该游戏服信息读写锁
}

// LeaseApp 租赁服务主应用
type LeaseApp struct {
	common.App
	gameServers   map[uint32]map[uint32]*GameServerInfo // serverId -> compId -> GameServerInfo
	channelToHost map[uuid.UUID]uint32                  // RPC Channel UUID -> serverId
	serversMutex  *sync.RWMutex                         // gameServers 和 channelToHost 的读写锁
	db            *sql.DB                               // MySQL 连接
	leaseMgr      *LeaseMgr                             // 租赁市场内存管理器
}

func NewLeaseApp() *LeaseApp {
	appLog.Info("create db connection...")
	db, err := sql.Open("mysql", fmt.Sprintf("%s:%s@tcp(%s)/%s?charset=utf8",
		LeaseConfig.Mysql.User, LeaseConfig.Mysql.Passwd, LeaseConfig.Mysql.Addr, LeaseConfig.Mysql.Db))
	if err != nil {
		appLog.Error("open mysql error: ", err.Error())
		return nil
	}
	db.SetMaxIdleConns(200)
	db.SetConnMaxLifetime(time.Hour * 5)
	db.SetMaxOpenConns(200)
	if err = db.Ping(); err != nil {
		appLog.Error("mysql connect err", err.Error())
		return nil
	}

	appLog.Info("load config...")
	auctionConst, err := loadAuctionConst("../data/auction.auctionConst.txt")
	if err != nil {
		appLog.Errorw("load auction const failed", "err", err)
		return nil
	}

	app := &LeaseApp{
		App:           common.App{AppName: "LeaseApp"},
		gameServers:   make(map[uint32]map[uint32]*GameServerInfo),
		channelToHost: make(map[uuid.UUID]uint32),
		serversMutex:  &sync.RWMutex{},
		db:            db,
		leaseMgr:      NewLeaseMgr(db, auctionConst),
	}

	appLog.Info("load lease data from db...")
	if err := app.leaseMgr.loadFromDB(); err != nil {
		appLog.Error("load lease db error:", err.Error())
		return nil
	}

	return app
}

func (la *LeaseApp) GetServices() []*common.ServiceInfo {
	return []*common.ServiceInfo{
		{
			ServiceType:       SERVICE_GAME_SERVER,
			ServiceName:       "LeaseServer",
			ServiceListenAddr: LeaseConfig.GameServerServiceAddr,
		},
	}
}

func (la *LeaseApp) Start() {
	la.App.Start()
	la.RegisterSignals(syscall.SIGINT, syscall.SIGKILL, syscall.SIGTERM)
	SafeGo(func() {
		<-la.SignalChan
		la.Stop()
	})

	SafeGo(func() {
		la.StartDebugService(LeaseConfig.AddressForDebug)
	})

	// 启动上架过期调度器（租赁到期归还仍由 Avatar 端处理）
	SafeGo(la.leaseMgr.startExpireScheduler)

	// 启动中间状态（PREPARE/PRE_LOCK）超时清扫器
	pendingTimeout := int64(LeaseConfig.PendingStatusTimeout)
	if pendingTimeout <= 0 {
		pendingTimeout = 60
	}
	SafeGo(func() {
		la.leaseMgr.startStuckSweeper(pendingTimeout)
	})

	// 启动数据库历史数据清理器（CANCELED / 已结束 LEASED 行）
	cleanInterval := LeaseConfig.CleanIntervalHours
	if cleanInterval <= 0 {
		cleanInterval = 6
	}
	cleanBatch := LeaseConfig.CleanBatchSize
	if cleanBatch <= 0 {
		cleanBatch = 100
	}
	cleanGrace := LeaseConfig.CleanGraceDays
	if cleanGrace <= 0 {
		cleanGrace = 14
	}
	SafeGo(func() {
		la.leaseMgr.startDBCleaner(cleanInterval, cleanBatch, cleanGrace)
	})
}

func (la *LeaseApp) Stop() {
	appLog.Info("lease app stopping...")
}

func (la *LeaseApp) NewService(conn net.Conn, serviceType uint8) trpc.IServerEndPoint {
	var service trpc.IServerEndPoint = nil
	if serviceType == SERVICE_GAME_SERVER {
		rpcUUID := uuid.New()
		channel := trpc.NewRpcChannel(rpcUUID, conn)
		service = &GameServerService{
			ServerEndPoint: gameServerService.NewLeaseServerService(gameServerService.NewGameServerClient(channel)),
			app:            la,
			status:         ServiceStatus_Connected,
			limiter:        newRateLimiter(),
		}
		channel.SetEndPoint(service)
	}
	return service
}

func (la *LeaseApp) doRegisterServer(hostId uint32, compId uint32, hostName string, service trpc.IServerEndPoint) error {
	appLog.Infow("register server", "hostId", hostId, "compId", compId, "hostName", hostName)
	if hostId == 0 {
		return fmt.Errorf("register server err: invalid hostId: %d", hostId)
	}
	la.serversMutex.Lock()
	defer la.serversMutex.Unlock()
	if _, ok := la.gameServers[hostId]; !ok {
		la.gameServers[hostId] = make(map[uint32]*GameServerInfo)
	}
	la.gameServers[hostId][compId] = &GameServerInfo{
		serverName:   hostName,
		LeaseService: service,
		rwLock:       &sync.RWMutex{},
	}
	la.channelToHost[service.GetRpcChannel().ChannelUUID] = hostId
	return nil
}

func (la *LeaseApp) unRegisterServer(service *GameServerService) {
	appLog.Infow("unRegisterServer", "serverId", service.serverId, "compId", service.compId)
	la.serversMutex.Lock()
	defer la.serversMutex.Unlock()
	if gameServerMap, ok := la.gameServers[service.serverId]; ok {
		if gameServer, ok := gameServerMap[service.compId]; ok {
			delete(gameServerMap, service.compId)
			delete(la.channelToHost, gameServer.LeaseService.GetRpcChannel().ChannelUUID)
		}
		if len(gameServerMap) == 0 {
			delete(la.gameServers, service.serverId)
		}
	}
}

func (la *LeaseApp) GetGameServer(serverId uint32, compId uint32) *GameServerInfo {
	la.serversMutex.RLock()
	defer la.serversMutex.RUnlock()
	if gameServerMap, ok := la.gameServers[serverId]; ok {
		if len(gameServerMap) == 0 {
			return nil
		}
		if compId == 0 {
			for _, gameServer := range gameServerMap {
				gameServ := gameServer.LeaseService.(*GameServerService)
				if gameServ.status != 1 {
					continue
				}
				return gameServer
			}
		} else if gameServer, okk := gameServerMap[compId]; okk {
			gameServ := gameServer.LeaseService.(*GameServerService)
			if gameServ.status != 1 {
				return nil
			}
			return gameServer
		}
	}
	return nil
}

// 租赁到期归还逻辑已下放到 Avatar 端，Go 服不再维护定时器与到期队列
