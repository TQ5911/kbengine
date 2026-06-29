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

	"github.com/garyburd/redigo/redis"
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

func (a *LeaseMarketItem) LeftTime() uint32 {
	if a.ReturnEndTime == 0 {
		return a.LeaseDay * 86400
	} else {
		now := uint32(time.Now().Unix())
		return a.ReturnEndTime - now
	}
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

// resetLeaseStatus 将状态重置为 on_sale
func (a *LeaseMarketItem) resetLeaseStatus() {
	a.mu.Lock()
	defer a.mu.Unlock()

	a.Status = LEASE_STATUS_ON_SALE
	a.LesseeGbId = 0
	a.LesseeServerId = 0
	a.LeaseStartTime = 0
	a.LeaseEndTime = 0
	a.LeaseCost = 0
	a.LeaseGold = 0
	a.LeaseBindGold = 0
	a.LeaseTax = 0
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
	db        *sql.DB     // MySQL 连接
	redisPool *redis.Pool // Redis 连接池

	// 数据及索引
	items         cmap.ConcurrentMap[uint64, *LeaseMarketItem] // uniqueId -> 租赁物品主数据
	itemIdIndex   cmap.ConcurrentMap[uint32, *LockedBTree]     // itemId -> 按价格和上架时间排序的 BTree
	playerIdIndex cmap.ConcurrentMap[uint64, *LockedBTree]     // playerGbId -> 该玩家的出租物品 BTree

	// 配置映射 itemId -> type/subType
	cfgMu        sync.RWMutex
	gearBaseMap  map[uint32]*GearBaseItem // gearBase 配置，用于商店分类过滤
	auctionConst *AuctionConstConfig      // 拍卖行常量配置（租赁服务复用）

	// 过期调度器（集中式最小堆）
	expireHeap *expireHeap
	expireMu   sync.Mutex
	expireWake chan struct{}
}

func NewLeaseMgr(db *sql.DB, redisPool *redis.Pool, gearBaseMap map[uint32]*GearBaseItem, auctionConst *AuctionConstConfig) *LeaseMgr {
	h := &expireHeap{}
	heap.Init(h)
	return &LeaseMgr{
		db:            db,
		items:         cmap.NewWithCustomShardingFunction[uint64, *LeaseMarketItem](uint64Shard),
		itemIdIndex:   cmap.NewWithCustomShardingFunction[uint32, *LockedBTree](uint32Shard),
		playerIdIndex: cmap.NewWithCustomShardingFunction[uint64, *LockedBTree](uint64Shard),
		redisPool:     redisPool,
		gearBaseMap:   gearBaseMap,
		auctionConst:  auctionConst,
		expireHeap:    h,
		expireWake:    make(chan struct{}, 1),
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

func (lm *LeaseMgr) addItemPrepare(item *LeaseMarketItem) int {
	limit := int32(lm.auctionConst.RentalInitShelfNum)
	if lm.getPlayerOnSaleCount(item.LessorGbId) >= limit {
		return LEASE_SHELF_FULL
	}

	now := time.Now().Unix()
	item.AddTime = now
	item.Status = LEASE_STATUS_PREPARE
	if !lm.items.SetIfAbsent(item.UniqueId, item) {
		return LEASE_ALREADY_EXISTS
	}
	return LEASE_OK
}

func (lm *LeaseMgr) addItemCommit(uniqueId uint64) int {
	item, ok := lm.items.Get(uniqueId)
	if !ok {
		return LEASE_NOT_FOUND
	}
	if !item.checkSetStatus(LEASE_STATUS_PREPARE, LEASE_STATUS_ON_SALE) {
		return LEASE_STATUS_ERROR
	}

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

func (lm *LeaseMgr) addItemRollback(uniqueId uint64) int {
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

	lm.items.Remove(uniqueId)

	return LEASE_OK
}

func (lm *LeaseMgr) leaseItemPrepare(uniqueId uint64, buyerGbId uint64, buyerServerId uint32) (int64, int) {
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
	if item.ReturnEndTime > 0 && item.ReturnEndTime-now < uint32(lm.auctionConst.RentalTimelimit)*86400 {
		return 0, LEASE_TIMEOUT
	}

	item.Status = LEASE_STATUS_PRE_LOCK

	var goldRate float64
	var bindGoldRate float64

	item.LeaseStartTime = uint32(now)
	if item.ReturnReason > 0 {
		goldRate = lm.auctionConst.RentalProp02[2]
		bindGoldRate = lm.auctionConst.RentalProp02[1]
		item.LeaseEndTime = item.ReturnEndTime // 固定归还时间
	} else {
		goldRate = lm.auctionConst.RentalProp01[2]
		bindGoldRate = lm.auctionConst.RentalProp01[1]
		item.LeaseEndTime = item.LeaseStartTime + item.LeaseDay*86400 // 从此刻开始计算租期
	}

	pricePerMinute := float64(item.PricePerDay) / 24.0 / 60.0
	remainMinutes := (float64(item.LeaseEndTime) - float64(now)) / 60.0

	item.LeaseCost = int64(pricePerMinute*remainMinutes + 0.5)
	item.LeaseGold = int64(float64(item.LeaseCost)*goldRate + 0.5)
	item.LeaseBindGold = int64(float64(item.LeaseCost)*bindGoldRate + 0.5)
	item.LeaseTax = item.LeaseCost - item.LeaseGold - item.LeaseBindGold

	item.LesseeGbId = buyerGbId
	item.LesseeServerId = buyerServerId
	lm._removeFromItemIdIndex(item)
	lm._removeFromPlayerIdIndex(item)

	return item.LeaseCost, LEASE_OK
}

func (lm *LeaseMgr) leaseItemCommit(uniqueId uint64) (*LeaseMarketItem, int) {
	item, ok := lm.items.Get(uniqueId)
	if !ok {
		return nil, LEASE_NOT_FOUND
	}

	if !item.checkSetStatus(LEASE_STATUS_PRE_LOCK, LEASE_STATUS_LEASED) {
		return item, LEASE_STATUS_ERROR
	}

	now := uint32(time.Now().Unix())
	if err := lm.dbLeaseItemCommit(item, now); err != nil {
		appLog.Errorw("leaseItemCommit db error", "uniqueId", item.UniqueId, "err", err)

		// 写库失败，这里重新回滚到上架状态
		item.resetLeaseStatus()
		lm._addToItemIdIndex(item)
		lm._addToPlayerIdIndex(item)
		return item, LEASE_DB_ERROR
	}

	// 租赁成交后从内存中移除，由 Avatar 端管理到期归还
	lm.items.Remove(item.UniqueId)

	return item, LEASE_OK
}

func (lm *LeaseMgr) leaseItemRollback(uniqueId uint64) int {
	item, ok := lm.items.Get(uniqueId)
	if !ok {
		return LEASE_NOT_FOUND
	}
	item.mu.Lock()
	defer item.mu.Unlock()

	if item.Status != LEASE_STATUS_PRE_LOCK {
		return LEASE_STATUS_ERROR
	}

	// 回滚到上架状态
	item.Status = LEASE_STATUS_ON_SALE
	item.LesseeGbId = 0
	item.LesseeServerId = 0
	item.LeaseStartTime = 0
	item.LeaseEndTime = 0
	item.LeaseCost = 0
	item.LeaseGold = 0
	item.LeaseBindGold = 0
	item.LeaseTax = 0
	lm._addToItemIdIndex(item)
	lm._addToPlayerIdIndex(item)

	return LEASE_OK
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
			if item.ReturnEndTime > 0 && item.ReturnEndTime-now < uint32(lm.auctionConst.RentalTimelimit)*86400 {
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
		if item.ReturnEndTime > 0 && item.ReturnEndTime-now < uint32(lm.auctionConst.RentalTimelimit)*86400 {
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

	appLog.Info("create redis pool...")
	var redisPool *redis.Pool
	if LeaseConfig.RedisServer.Addr != "" {
		redisPool = common.NewRedisPool(common.RedisPoolOptions{
			ServerName:  "lease",
			Addr:        LeaseConfig.RedisServer.Addr,
			Username:    LeaseConfig.RedisServer.Username,
			Password:    LeaseConfig.RedisServer.Passwd,
			Db:          LeaseConfig.RedisServer.Db,
			MaxIdle:     16,
			MaxActive:   100,
			IdleTimeout: 100,
		})
	}

	appLog.Info("load config...")
	gearBaseMap, err := loadGearBaseMap("../data/gearBase.gearBase.txt")
	if err != nil {
		appLog.Errorw("load gearBase config failed", "err", err)
		return nil
	}
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
		leaseMgr:      NewLeaseMgr(db, redisPool, gearBaseMap, auctionConst),
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
