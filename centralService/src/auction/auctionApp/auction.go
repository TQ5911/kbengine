package Auction

import (
	"bytes"
	"centralService/src/appLog"
	gameServerService "centralService/src/auction/auctionApp/gameServerService"
	"centralService/src/common"
	cmap "centralService/src/common/concurrent_map"
	"database/sql"
	"encoding/json"
	"errors"
	"fmt"
	"math/rand"
	"strconv"
	"sync"
	"time"

	"github.com/google/btree"
)

var itemDataPool = sync.Pool{
	New: func() interface{} {
		return &ItemData{}
	},
}

// === 2026-09-21 抢购迁移 v3:抽签桶结构与全局索引 ===

// SnatchReason 抢购退款原因 (与 proto SnatchRefundItem.reason 对应)
type SnatchReason uint32

const (
	SnatchReasonNotLucky SnatchReason = 1 // 未中签
	SnatchReasonTimeout  SnatchReason = 2 // 超时退款 (本期未使用)
	SnatchReasonOffline  SnatchReason = 3 // 微服务下线退款 (本期未使用)
)

// SnatchRec 单个玩家的抢购参与记录
type SnatchRec struct {
	PlayerGBID uint64
	RoleName   string
	OpUUID     int64
	InTime     int64
	ServerId   uint32
	// 2026-10-08 抢购权重快照(普通玩家=1000,推广者=1100);openSnatch 抽签时按此权重抽样
	SnatchWeight int64
	Extra        string
}

// SnatchBucket 每个拍卖物品的抢购参与桶
type SnatchBucket struct {
	AuctionItemUUID  uint64
	ItemId           uint32
	Price            uint64
	Number           uint32
	PublicityEndTime int64
	Opened           bool                  // 抽签是否已执行
	WinnerGBID       uint64                // 0 = 未抽或无人参与
	Records          map[uint64]*SnatchRec // gbID → 参与记录
	OpenTimer        *time.Timer           // 抽签调度 (用于崩溃重挂)
	mu               sync.Mutex
}

// snatchBuckets 全局桶索引 auctionItemUUID → bucket
var snatchBuckets = cmap.NewWithCustomShardingFunction[uint64, *SnatchBucket](DirectUInt64Sharding)

func (am *AuctionMgr) checkSnatchBucket(auctionItemUUID uint64) bool {
	if b, ok := snatchBuckets.Get(auctionItemUUID); ok && b != nil {
		b.mu.Lock()
		defer b.mu.Unlock()
		return len(b.Records) > 0
	}
	return false
}

func (am *AuctionMgr) checkSnatchPlayer(auctionItemUUID uint64, playerGbId uint64) bool {
	if b, ok := snatchBuckets.Get(auctionItemUUID); ok && b != nil {
		b.mu.Lock()
		defer b.mu.Unlock()
		if _, ok := b.Records[playerGbId]; ok {
			return true
		}
	}
	return false
}

// getOrCreateSnatchBucket 获取或创建桶
func (am *AuctionMgr) getOrCreateSnatchBucket(item *AuctionItem) (*SnatchBucket, int) {
	if b, ok := snatchBuckets.Get(item.AuctionItemUUID); ok && b != nil {
		b.mu.Lock()
		defer b.mu.Unlock()
		return b, len(b.Records)
	}
	b := &SnatchBucket{
		AuctionItemUUID:  item.AuctionItemUUID,
		ItemId:           item.ItemData.ItemId,
		Price:            item.Price,
		Number:           item.Number,
		PublicityEndTime: item.GetPublicityEndTime(),
		Records:          make(map[uint64]*SnatchRec),
	}
	res := snatchBuckets.Upsert(item.AuctionItemUUID, b, func(exist bool, valueInMap, newValue *SnatchBucket) *SnatchBucket {
		if exist {
			return valueInMap
		}
		return newValue
	})
	b.mu.Lock()
	defer b.mu.Unlock()
	return res, len(b.Records)
}

// getOrCreateSnatchBucket 获取或创建桶
func (am *AuctionMgr) popSnatchBucket(item *AuctionItem) (*SnatchBucket, int) {
	data, ok := snatchBuckets.Pop(item.AuctionItemUUID)
	if ok {
		return data, len(data.Records)
	}
	return nil, 0
}

// maybeRecordSnatchParticipation v3 拦截点:
// DoBuyItem 调用此函数检查是否在 SNATCH 期间.
// 是 → 在 bucket.Records 中登记,return true (DoBuyItem 伪成交返回)
// 否 → return false (DoBuyItem 走正常流)
// snatchWeight = 0 由 game server 兜底改成默认值 DEFAULT_SNATCH_WEIGHT(1000)
func (am *AuctionMgr) maybeRecordSnatchParticipation(auctionItem *AuctionItem, serverId uint32, playerGBID uint64, extra string, snatchWeight int64) bool {
	if !auctionItem.CheckInSnatch() {
		// 抢购时间过了
		return false
	}
	// 解析 extra:尽力取 role_name + opUUID(失败给空也无所谓,只影响退款文案)
	var m map[string]interface{}
	roleName := ""
	opUUID := int64(0)
	if json.Unmarshal([]byte(extra), &m) == nil {
		if tlogProps, ok := m["tlogProps"].(map[string]interface{}); ok {
			if rn, ok := tlogProps["role_name"].(string); ok {
				roleName = rn
			}
		}
		opUUID = int64(m["opUUID"].(float64))
	}

	bucket, _ := am.getOrCreateSnatchBucket(auctionItem)
	bucket.mu.Lock()
	defer bucket.mu.Unlock()
	if bucket.Opened {
		// 已开始了
		return false
	}
	_, exists := bucket.Records[playerGBID]
	if exists {
		// 已参与了
		return false
	}

	bucket.Records[playerGBID] = &SnatchRec{
		PlayerGBID:   playerGBID,
		RoleName:     roleName,
		OpUUID:       opUUID,
		InTime:       time.Now().Unix(),
		ServerId:     serverId,
		SnatchWeight: snatchWeight,
		Extra:        extra,
	}
	return true
}

//func getAuctionItemEndTime(itemId string) (uint32, error) {
//	categoryId, ok := ItemIdToCategoryConfig.Get(itemId).(string)
//	if !ok {
//		appLog.Error("getAuctionItemEndTime: ItemIdToCategoryConfig.Get error, itemId:", itemId)
//		return 0, errors.New("getAuctionItemEndTime: ItemIdToCategoryConfig.Get error, itemId:" + itemId)
//	}
//	categoryConfig := AuctionCategoryConfig.GetStringMap(categoryId)
//	if categoryConfig == nil {
//		appLog.Error("getAuctionItemEndTime: categoryConfig is nil, categoryId:", categoryId)
//		return 0, errors.New("getAuctionItemEndTime: categoryConfig is nil, categoryId:" + categoryId)
//	}
//
//	endTime, ok := categoryConfig["endtime"].(float64)
//	if !ok {
//		appLog.Debugw("getAuctionItemEndTime itemList value is nil", "categoryId", categoryId, "itemId", itemId)
//		return 0, nil
//	}
//	layout := "20060102150405"
//	t, err := time.ParseInLocation(layout, strconv.FormatUint(uint64(endTime), 10), time.Local)
//	if err != nil {
//		appLog.Error("getAuctionItemEndTime: time.ParseInLocation error:", err)
//		return 0, err
//	}
//
//	return uint32(t.Unix()), nil
//}

type AuctionItem struct {
	AuctionType           uint8                            `json:"auctionType"`      // 交易行类型
	AuctionItemUUID       uint64                           `json:"auctionItemUUID"`  // 上架物品唯一UUID
	AddTime               int64                            `json:"addTime"`          // 上架物品时间
	ItemData              *ItemData                        `json:"itemData"`         // 物品信息
	Price                 uint64                           `json:"price"`            // 总价
	Number                uint32                           `json:"number"`           // 物品数量
	BagType               uint8                            `json:"bagType"`          // 商家时的背包类型
	Source                uint8                            `json:"source"`           // 拍卖来源
	Status                uint8                            `json:"status"`           // 物品交易状态
	Locked                uint64                           `json:"locked"`           // 物品是否被锁
	ExtraInfo             string                           `json:"extraInfo"`        // 其他信息
	TCreate               uint32                           `json:"tCreate"`          // 创建时间
	FromPlayerGBID        uint64                           `json:"fromPlayerGBID"`   // 交易物品的玩家GBID
	ServerId              uint32                           `json:"serverId"`         // 服务器ID
	LockPlayerGBID        uint64                           `json:"lockPlayerGBID"`   // 锁定的玩家GBID
	LockTimer             *time.Timer                      `json:"lockTimer"`        // 锁定的定时器
	IsDestroyed           bool                             `json:"isDestroyed"`      // 是否已经销毁
	mu                    *sync.RWMutex                    `json:"-"`                // 读写锁
	IsInIndexMap          cmap.ConcurrentMap[string, bool] `json:"-"`                // 是否在索引中
	IsInPublicityIndexMap cmap.ConcurrentMap[string, bool] `json:"-"`                // 是否在公示索引中
	IsNeedRemove          bool                             `json:"-"`                // 是否需要从商品缓存列表中移除
	EachPrice             float32                          `json:"-"`                // 单价
	AddPublicityTime      uint32                           `json:"addPublicityTime"` // 公示时间
	EquipExtraCache       map[string]int32                 `json:"-"`                // 装备特殊的缓存数据
}

func NewAuctionItem(auctionType uint8, auctionItemUUID uint64, addTime int64, itemData *ItemData, price uint64, number uint32, bagType uint8, source uint8, status uint8, locked uint64, extraInfo string, fromPlayerGBID uint64, addPublicityTime uint32) *AuctionItem {
	auctionItem := &AuctionItem{
		AuctionType:      auctionType,
		AuctionItemUUID:  auctionItemUUID,
		AddTime:          addTime,
		ItemData:         itemData,
		Price:            price,
		Number:           number,
		BagType:          bagType,
		Source:           source,
		Status:           status,
		Locked:           locked,
		ExtraInfo:        extraInfo,
		TCreate:          uint32(time.Now().Unix()),
		FromPlayerGBID:   fromPlayerGBID,
		mu:               &sync.RWMutex{},
		AddPublicityTime: addPublicityTime,
		EquipExtraCache:  make(map[string]int32),
	}

	var m map[string]interface{}
	err := json.Unmarshal([]byte(extraInfo), &m)
	if err != nil {
		appLog.Error("NewAuctionItem: Unmarshal err", err)
		return nil
	}
	auctionItem.EquipExtraCache[EQUIP_GRADE_LEVEL] = int32(m[EQUIP_GRADE_LEVEL].(float64))
	auctionItem.EquipExtraCache[EQUIP_ENHANCE_LEVEL] = int32(m[EQUIP_ENHANCE_LEVEL].(float64))

	auctionItem.ServerId = uint32(m["serverId"].(float64))
	auctionItem.EachPrice = float32(auctionItem.Price) / float32(auctionItem.Number)
	auctionItem.init()
	return auctionItem
}

func (a *AuctionItem) init() bool {
	a.IsInIndexMap = cmap.New[bool]()
	for _, indexKey := range auctionIndexKeys {
		a.IsInIndexMap.Set(indexKey, false)
	}

	a.IsInPublicityIndexMap = cmap.New[bool]()
	for _, indexKey := range auctionIndexKeys {
		a.IsInPublicityIndexMap.Set(indexKey, false)
	}
	return true
}

func (a *AuctionItem) Less(other btree.Item) bool {
	if a.EachPrice == other.(*AuctionItem).EachPrice {
		if a.AddTime == other.(*AuctionItem).AddTime {
			return a.AuctionItemUUID < other.(*AuctionItem).AuctionItemUUID
		}
		return a.AddTime < other.(*AuctionItem).AddTime
	}
	return a.EachPrice < other.(*AuctionItem).EachPrice
}

func (a *AuctionItem) Compare(other *AuctionItem) bool {
	if a.EachPrice == other.EachPrice {
		if a.AddTime == other.AddTime {
			return a.AuctionItemUUID < other.AuctionItemUUID
		}
		return a.AddTime < other.AddTime
	}
	return a.EachPrice < other.EachPrice
}

func (a *AuctionItem) getServerId() uint32 {
	return a.ServerId
}

func (a *AuctionItem) getEachPrice() float32 {
	return float32(a.Price) / float32(a.Number)
}

func (a *AuctionItem) getIndexVal(indexKey string) string {
	switch indexKey {
	case INDEX_KEY_ITEMID:
		return strconv.FormatUint(uint64(a.ItemData.ItemId), 10)
	case INDEX_KEY_PLAYERGBID:
		return strconv.FormatUint(a.FromPlayerGBID, 10)
	default:
		appLog.Error("getIndexVal unknow index key, indexKey:", indexKey)
		return ""
	}
}

func (a *AuctionItem) isItemExpired(cutTime int64) bool {
	if a.Status == AUCTION_STATUS_EXPIRED {
		return true
	}
	if a.ItemData.ExpireTime > 0 && cutTime >= a.ItemData.ExpireTime {
		return true
	}
	return a.itemExpiredTime() <= cutTime
}

func (a *AuctionItem) lock(timeout uint32, lockPlayerGbId uint64, app *AuctionApp, isRemoveIndex bool) bool {
	if a.isLocked(lockPlayerGbId) {
		return false
	}
	isPublicity := false
	if isRemoveIndex {
		a.IsNeedRemove = true
		// 正在公示
		if a.Status == AUCTION_STATUS_PUBLICITY {
			isPublicity = true
			app.auctionMgr.removeAuctionItemFromPublicityIndex(INDEX_KEY_ITEMID, a.getIndexVal(INDEX_KEY_ITEMID), a)
		} else {
			app.auctionMgr.removeAuctionItemFromIndex(INDEX_KEY_ITEMID, a.getIndexVal(INDEX_KEY_ITEMID), a)
		}
	}
	if !a.mu.TryLock() {
		if isRemoveIndex {
			a.IsNeedRemove = false
			if isPublicity {
				app.auctionMgr.addAuctionItemToPublicityIndex(INDEX_KEY_ITEMID, a.getIndexVal(INDEX_KEY_ITEMID), a)
			} else {
				app.auctionMgr.addAuctionItemToIndex(INDEX_KEY_ITEMID, a.getIndexVal(INDEX_KEY_ITEMID), a)
			}
		}
		return false
	}

	if a.LockPlayerGBID != 0 && a.LockPlayerGBID != SNATCH_LOCK_ID {
		a.mu.Unlock()
		return false
	}

	if a.IsDestroyed || a.Number == 0 {
		a.mu.Unlock()
		return false
	}

	a.Locked = 1
	a.LockPlayerGBID = lockPlayerGbId
	a.mu.Unlock()

	if a.LockTimer != nil {
		a.LockTimer.Stop()
		a.LockTimer = nil
	}

	timer := time.AfterFunc(time.Duration(timeout)*time.Second, func() {
		a.unLock()
	})
	a.LockTimer = timer
	return true
}

func (a *AuctionItem) unLock() {
	a.mu.Lock()
	defer a.mu.Unlock()
	a.Locked = 0
	a.LockPlayerGBID = 0
	if a.LockTimer != nil {
		a.LockTimer.Stop()
		a.LockTimer = nil
	}
}

func (a *AuctionItem) checkLockedId(lockedId uint64) bool {
	a.mu.RLock()
	defer a.mu.RUnlock()
	return a.Locked != 0 && a.LockPlayerGBID == lockedId
}

func (a *AuctionItem) isLocked(lockedId uint64) bool {
	a.mu.RLock()
	defer a.mu.RUnlock()
	if a.Locked != 0 {
		// 抢购的可以一起锁
		if a.LockPlayerGBID == lockedId {
			return false
		}
		return true
	}
	return false
}

func (a *AuctionItem) itemExpiredSecond() int64 {
	auctionCfg, ret := ConfigStore.cfgVipers.Get(CFG_TYPE_AUCTION_CONST)
	if !ret {
		appLog.Error("itemExpiredSecond missing cfg store ", CFG_TYPE_AUCTION_CONST)
		return 0
	}
	normalItemSalePeriod := auctionCfg.GetInt("auctionAutoUnlist")
	t := int64(normalItemSalePeriod * 3600)
	t += a.GetPublicityGap()
	return t
}

func (a *AuctionItem) getSnatchTime() int64 {
	auctionCfg, ret := ConfigStore.cfgVipers.Get(CFG_TYPE_AUCTION_CONST)
	if !ret {
		appLog.Error("getSnatchTime missing cfg store ", CFG_TYPE_AUCTION_CONST)
		return 0
	}
	snatchTime := auctionCfg.GetInt("auctionLuckyBuyTime")
	return int64(snatchTime)
}

func (a *AuctionItem) GetPublicityGap() int64 {
	return int64(a.AddPublicityTime)
}

func (a *AuctionItem) GetPublicityEndTime() int64 {
	return a.AddTime + int64(a.AddPublicityTime)
}

func (a *AuctionItem) CheckInSelling() bool {
	return a.Status == AUCTION_STATUS_SELLING
}

func (a *AuctionItem) CheckInSnatch() bool {
	curTime := time.Now().Unix()
	return a.GetPublicityEndTime()-a.getSnatchTime()-2 <= curTime && curTime <= a.GetPublicityEndTime()
}

func (a *AuctionItem) CheckInPublicity() bool {
	curTime := time.Now().Unix()
	return curTime < a.GetPublicityEndTime()-a.getSnatchTime()
}

func (a *AuctionItem) itemExpiredTime() int64 {
	return a.AddTime + a.itemExpiredSecond()
}

func (a *AuctionItem) setStatus(status uint8, db *sql.DB, isInit bool) error {
	if a.Status == status {
		return nil
	}

	a.Status = status
	// 初始化期间，直接插入db或者从db捞数据出来，无需进行再次插入，只有状态发生改变的才需要插入
	if isInit {
		if status == AUCTION_STATUS_SELLING || status == AUCTION_STATUS_PUBLICITY {
			return nil
		}
	} else {
		err := a.Update(db, []string{"status"}, []interface{}{a.Status})
		if err != nil {
			appLog.Error("setStatus Update err:", err)
			return err
		}
	}

	return nil
}

func (a *AuctionItem) Add(db *sql.DB, status uint8) error {
	sql := "INSERT INTO `auction_auctionItemData` (`serverId`, `auctionType`, `auctionItemUUID`, `addTime`, `itemData_itemId`, `itemData_itemNum`, `itemData_createTime`, `itemData_expireTime`, `itemData_uniqueId`, `itemData_bindType`, `itemData_attrJson`, `price`, `number`, `bagType`, `source`, `status`, `locked`, `extraInfo`, `tCreate`, `fromPlayerGBID`, `addPublicityTime`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
	_, err := db.Exec(sql, a.ServerId, a.AuctionType, a.AuctionItemUUID, a.AddTime, a.ItemData.ItemId, a.ItemData.ItemNum, a.ItemData.CreateTime, a.ItemData.ExpireTime, a.ItemData.UniqueId, a.ItemData.BindType, a.ItemData.AttrJson, a.Price, a.Number, a.BagType, a.Source, status, a.Locked, a.ExtraInfo, a.TCreate, a.FromPlayerGBID, a.AddPublicityTime)
	if err != nil {
		appLog.Error("Add AuctionItem Exec err:", err)
		return err
	}
	return nil
}

func (a *AuctionItem) Update(db *sql.DB, keys []string, values []interface{}) error {
	if len(keys) != len(values) {
		appLog.Error("Update AuctionItem err: keys and values must be same length")
		return errors.New("keys and values must be same length")
	}
	var query bytes.Buffer
	query.WriteString("UPDATE `auction_auctionItemData` SET ")
	params := make([]interface{}, len(keys)+1)
	for i := 0; i < len(keys); i++ {
		query.WriteString(fmt.Sprintf("`%s`=?,", keys[i]))
		params[i] = values[i]
	}
	query.Truncate(query.Len() - 1)
	query.WriteString(" WHERE `auctionItemUUID`=?")
	params[len(params)-1] = a.AuctionItemUUID
	_, err := db.Exec(query.String(), params...)
	if err != nil {
		appLog.Error("Update AuctionItem err:", err)
		return err
	}
	return nil
}

func (a *AuctionItem) Delete(db *sql.DB) error {
	_, err := db.Exec("DELETE FROM `auction_auctionItemData` WHERE `auctionItemUUID`=?", a.AuctionItemUUID)
	if err != nil {
		appLog.Error("Delete AuctionItem err:", err)
	}
	return err
}

type ItemData struct {
	ItemId     uint32 `json:"itemId"`     // 物品ID
	ItemNum    uint32 `json:"itemNum"`    // 物品数量
	UniqueId   uint64 `json:"uniqueId"`   // 物品唯一ID
	BindType   uint8  `json:"bindType"`   // 绑定类型
	CreateTime int64  `json:"createTime"` // 创建时间
	ExpireTime int64  `json:"expireTime"` // 过期时间
	AttrJson   string `json:"attrJson"`   // 属性数据
}

func NewItemData(srcItemData *ItemData, itemNum uint32) *ItemData {
	itemData := itemDataPool.Get().(*ItemData)
	itemData.ItemId = srcItemData.ItemId
	itemData.ItemNum = itemNum
	itemData.UniqueId = srcItemData.UniqueId
	itemData.BindType = srcItemData.BindType
	itemData.CreateTime = srcItemData.CreateTime
	itemData.ExpireTime = srcItemData.ExpireTime
	itemData.AttrJson = srcItemData.AttrJson

	return itemData
}

type DailyPrice struct {
	Date       string  `json:"date"`
	TotalPrice uint64  `json:"totalPrice"`
	Number     uint64  `json:"number"`
	AvgPrice   float32 `json:"avgPrice"`
}

type AuctionItemAvgRecord struct {
	serverId       uint32
	itemId         uint32
	totalPrice     uint64
	number         uint64
	avgPrice       float32
	lastUpdateTime int64
	recentPrices   []DailyPrice
}

func (a *AuctionItemAvgRecord) GetRecentAvgPrice(days int) float32 {
	if days <= 0 || len(a.recentPrices) == 0 {
		return 0
	}
	startIdx := len(a.recentPrices) - days
	if startIdx < 0 {
		startIdx = 0
	}
	var totalAllPrice uint64 = 0
	var totalAllNum uint64 = 0
	for i := startIdx; i < len(a.recentPrices); i++ {
		dp := a.recentPrices[i]
		totalAllPrice += dp.TotalPrice
		totalAllNum += dp.Number
	}
	if totalAllNum == 0 {
		return 0
	}
	avgPrice := float64(totalAllPrice) / float64(totalAllNum)
	return float32(avgPrice)
}

func (a *AuctionItemAvgRecord) Update(db *sql.DB, isDailyReset bool) error {
	jsonBytes, err := json.Marshal(a.recentPrices)
	if err != nil {
		appLog.Error("AuctionItemAvgRecord Update marshal recentPrices error: ", err.Error(), " itemId", a.itemId)
		return err
	}

	var buf bytes.Buffer
	if isDailyReset {
		buf.WriteString("UPDATE `auction_priceRecord_avgPrices` SET `tLastUpdateTime`=?, `totalPrice`=?, `number`=?, `avgPrice`=?, recentPrices=? WHERE `itemId`=? and `serverId`=?")
		query := buf.String()

		_, err = db.Exec(query, a.lastUpdateTime, a.totalPrice, a.number, a.avgPrice, string(jsonBytes), a.itemId, a.serverId)
	} else {
		buf.WriteString("UPDATE `auction_priceRecord_avgPrices` SET `totalPrice`=?, `number`=?, `avgPrice`=?, recentPrices=? WHERE `itemId`=? and `serverId`=?")
		query := buf.String()

		_, err = db.Exec(query, a.totalPrice, a.number, a.avgPrice, string(jsonBytes), a.itemId, a.serverId)
	}

	if err != nil {
		appLog.Error("AuctionItemAvgRecord Update error: ", err.Error(), " itemId", a.itemId)
		return err
	}

	return nil
}

func (a *AuctionItemAvgRecord) Insert(db *sql.DB) error {
	jsonBytes, err := json.Marshal(a.recentPrices)
	if err != nil {
		appLog.Error("AuctionItemAvgRecord Insert marshal recentPrices error: ", err.Error(), " itemId: ", a.itemId)
		return err
	}

	stmt, err := db.Prepare("INSERT INTO `auction_priceRecord_avgPrices` (`serverId`, `itemId`, `totalPrice`, `number`, `avgPrice`, `recentPrices`) VALUES (?, ?, ?, ?, ?, ?)")
	if err != nil {
		appLog.Error("AuctionItemAvgRecord Insert error: ", err.Error(), " itemId: ", a.itemId)
		return err
	}

	defer stmt.Close()

	_, err = stmt.Exec(a.serverId, a.itemId, a.totalPrice, a.number, a.avgPrice, string(jsonBytes))
	if err != nil {
		appLog.Error("AuctionItemAvgRecord Insert error: ", err.Error(), " itemId: ", a.itemId)
		return err
	}

	return nil
}

func (a *AuctionItemAvgRecord) GetAvgPrice() (float32, float32) {
	//cfgData := ItemConfig.GetStringMap(strconv.FormatUint(uint64(a.itemId), 10))
	//if cfgData == nil || len(cfgData) == 0 {
	//	appLog.Error("GetAvgPrice: cfgData == nil", a.itemId)
	//	return 0
	//}
	//bottomPrice, ok := cfgData["normalpricebottomlinecoin"].(float64)
	//if !ok {
	//	appLog.Error("GetAvgPrice: bottomPrice err", a.itemId)
	//	return 0
	//}
	//topPrice, ok := cfgData["normalpricetoplinecoin"].(float64)
	//if !ok {
	//	appLog.Error("GetAvgPrice: topPrice err", a.itemId)
	//	return 0
	//}
	//avgPrice = math.Min(math.Max(avgPrice, bottomPrice), topPrice)
	return a.avgPrice, a.GetRecentAvgPrice(7)
}

type AuctionItemLastRecord struct {
	serverId uint32
	itemId   uint32
	price    float32
}

func (a *AuctionItemLastRecord) Update(db *sql.DB) error {
	stmt, err := db.Prepare("UPDATE `auction_priceRecord_lastPrices` SET `price`=? WHERE `itemId`=? and `serverId`=?")
	if err != nil {
		appLog.Error("AuctionItemLastRecord Update error: ", err.Error(), " itemId: ", a.itemId)
		return err
	}

	defer stmt.Close()

	_, err = stmt.Exec(a.price, a.itemId, a.serverId)
	if err != nil {
		appLog.Error("AuctionItemLastRecord Update error: ", err.Error(), " itemId: ", a.itemId)
		return err
	}

	return nil
}

func (a *AuctionItemLastRecord) Insert(db *sql.DB) error {
	stmt, err := db.Prepare("INSERT INTO `auction_priceRecord_lastPrices` (`serverId`, `itemId`, `price`) VALUES (?, ?, ?)")
	if err != nil {
		appLog.Error("AuctionItemLastRecord Insert error: ", err.Error(), " itemId: ", a.itemId)
		return err
	}

	defer stmt.Close()

	_, err = stmt.Exec(a.serverId, a.itemId, a.price)
	if err != nil {
		appLog.Error("AuctionItemLastRecord Insert error: ", err.Error(), " itemId: ", a.itemId)
		return err
	}

	return nil
}

type AuctionPriceRecords struct {
	itemAvgPriceRecords map[string]*AuctionItemAvgRecord
	avgPriceLock        *sync.RWMutex
	itemLastPriceData   map[string]*AuctionItemLastRecord
	rcdPriceLock        *sync.RWMutex
}

func (a *AuctionPriceRecords) GetAllItemPriceInfos() []*gameServerService.ItemPriceInfo {
	avgPrices := make(map[uint32]float32, 0)
	recentPrices := make(map[uint32]float32, 0)
	priceCounts := make(map[uint32]float32, 0)
	for itemIdData, auctionItemRecord := range a.itemAvgPriceRecords {
		_, itemId := SpilitPriceItemKey(itemIdData)
		if itemId == 0 {
			continue
		}

		avgPrice, recentPrice := auctionItemRecord.GetAvgPrice()

		a, ok := avgPrices[itemId]
		if ok {
			a += avgPrice
		}
		avgPrices[itemId] = a

		b, ok := recentPrices[itemId]
		if ok {
			b += recentPrice
		}

		recentPrices[itemId] = b
		c, ok := priceCounts[itemId]
		if ok {
			c += 1
		}

		priceCounts[itemId] = c
	}

	var priceInfoList []*gameServerService.ItemPriceInfo
	for itemId, priceCount := range priceCounts {
		if priceCount == 0 {
			continue
		}
		avgPrice, _ := avgPrices[itemId]
		recentPrice, _ := recentPrices[itemId]
		priceInfoList = append(priceInfoList, &gameServerService.ItemPriceInfo{
			ItemId:    itemId,
			AvgPrice:  avgPrice / priceCount,
			AvgPrice7: recentPrice / priceCount,
		})
	}

	return priceInfoList
}

func (a *AuctionPriceRecords) GetItemAvgPrice(itemId uint32, serverIds []int) (float32, float32) {
	a.avgPriceLock.RLock()
	defer a.avgPriceLock.RUnlock()
	batchCount := 0
	totalAvgPrice := float32(0)
	totalRecentPrice := float32(0)
	for _, serverId := range serverIds {
		itemAvgPriceRecord, ok := a.itemAvgPriceRecords[GetPriceItemKey(uint32(serverId), itemId)]
		if !ok {
			continue
		}
		a, b := itemAvgPriceRecord.GetAvgPrice()
		totalAvgPrice += a
		totalRecentPrice += b
		batchCount++
	}
	if batchCount > 0 {
		totalAvgPrice /= float32(batchCount)
		totalRecentPrice /= float32(batchCount)
	}
	return totalAvgPrice, totalRecentPrice
}

func (a *AuctionPriceRecords) GetItemLastPrice(itemId uint32, serverIds []int) float32 {
	a.rcdPriceLock.RLock()
	defer a.rcdPriceLock.RUnlock()
	totalPrice := 0
	for _, serverId := range serverIds {
		d, ok := a.itemLastPriceData[GetPriceItemKey(uint32(serverId), itemId)]
		if ok {
			totalPrice += int(d.price)
		}
	}
	return float32(totalPrice)
}

func (a *AuctionPriceRecords) AddAvgPriceRecord(serverId uint32, itemId uint32, price uint64, number uint32, app *AuctionApp) {
	a.avgPriceLock.Lock()
	defer a.avgPriceLock.Unlock()
	dataKey := GetPriceItemKey(serverId, itemId)
	itemAvgPriceRecord, ok := a.itemAvgPriceRecords[dataKey]
	totalPrice := price
	if !ok {
		itemAvgPriceRecord = &AuctionItemAvgRecord{
			serverId:     serverId,
			itemId:       itemId,
			totalPrice:   totalPrice,
			number:       uint64(number),
			avgPrice:     0.0,
			recentPrices: make([]DailyPrice, 0),
		}
		a.itemAvgPriceRecords[dataKey] = itemAvgPriceRecord

		err := itemAvgPriceRecord.Insert(app.db)
		if err != nil {
			appLog.Error("AuctionPriceRecords AddAvgPriceRecord error: ", err.Error(), " itemId: ", itemId)
			return
		}

	} else {
		itemAvgPriceRecord.totalPrice += totalPrice
		itemAvgPriceRecord.number += uint64(number)
		itemIdStr := strconv.FormatUint(uint64(itemId), 10)
		if _, ok := app.auctionMgr.updateTimerMap.Get(itemIdStr); ok {
			appLog.Debug("AddAvgPriceRecord: timer already exist")
			return
		}
		timer := time.AfterFunc(10*time.Second, func() {
			_, ok := app.auctionMgr.updateTimerMap.Get(itemIdStr)
			if ok {
				app.auctionMgr.updateTimerMap.Remove(itemIdStr)
			}
			err := itemAvgPriceRecord.Update(app.db, false)
			if err != nil {
				appLog.Error("AuctionPriceRecords AddAvgPriceRecord error: ", err.Error(), " itemId: ", itemId)
				return
			}
		})
		app.auctionMgr.updateTimerMap.Set(itemIdStr, timer)
	}
}

func (a *AuctionPriceRecords) AddLastPriceRecord(serverId uint32, itemId uint32, price float32, db *sql.DB) {
	var oldPrice float32 = 0
	a.rcdPriceLock.Lock()
	defer a.rcdPriceLock.Unlock()
	dataKey := GetPriceItemKey(serverId, itemId)
	auctionItemRecord, ok := a.itemLastPriceData[dataKey]
	if !ok {
		auctionItemRecord = &AuctionItemLastRecord{serverId: serverId, itemId: itemId, price: price}
		a.itemLastPriceData[dataKey] = auctionItemRecord
		err := auctionItemRecord.Insert(db)
		if err != nil {
			appLog.Error("AuctionPriceRecords AddLastPriceRecord error: ", err.Error(), " itemId: ", itemId)
			return
		}
	} else {
		oldPrice = auctionItemRecord.price
		auctionItemRecord.price = price
		err := auctionItemRecord.Update(db)
		if err != nil {
			appLog.Error("AuctionPriceRecords AddLastPriceRecord error: ", err.Error(), " itemId: ", itemId)
			return
		}
	}
	appLog.Info("AddLastPriceRecord itemId: ", itemId, " oldPrice: ", oldPrice, " newPrice: ", price)
}

type LockedBTree struct {
	tree *btree.BTreeG[*AuctionItem]
	mu   *sync.RWMutex
}

func NewLockedBTree() *LockedBTree {
	btreeG := btree.NewG(32, func(a, b *AuctionItem) bool {
		return a.Less(b)
	})
	return &LockedBTree{tree: btreeG, mu: &sync.RWMutex{}}
}

type CacheItem struct {
	IndexKey    string
	IndexVal    string
	AuctionItem *AuctionItem
	IsInit      bool
}

type AuctionMgr struct {
	auctionItems              cmap.ConcurrentMap[string, *AuctionItem]
	db                        *sql.DB
	app                       *AuctionApp
	priceRecord               *AuctionPriceRecords
	isDBLoaded                bool
	auctionItemIndex          cmap.ConcurrentMap[string, cmap.ConcurrentMap[string, *LockedBTree]]
	auctionItemPublicityIndex cmap.ConcurrentMap[string, cmap.ConcurrentMap[string, *LockedBTree]]
	expiredTimerMap           cmap.ConcurrentMap[string, *time.Timer]
	endPublicityTimerMap      cmap.ConcurrentMap[string, *time.Timer]
	gmTimerMap                map[string]interface{}
	gmTimerLock               *sync.RWMutex
	blackList                 []uint64
	blackListLock             *sync.RWMutex
	updateTimerMap            cmap.ConcurrentMap[string, *time.Timer]
	addCh                     chan *CacheItem
}

func NewAuctionMgr(db *sql.DB, app *AuctionApp) *AuctionMgr {
	var priceRecord = &AuctionPriceRecords{
		itemAvgPriceRecords: make(map[string]*AuctionItemAvgRecord),
		avgPriceLock:        &sync.RWMutex{},
		itemLastPriceData:   make(map[string]*AuctionItemLastRecord),
		rcdPriceLock:        &sync.RWMutex{},
	}

	auctionMgr := &AuctionMgr{
		auctionItems:              cmap.New[*AuctionItem](),
		db:                        db,
		priceRecord:               priceRecord,
		app:                       app,
		expiredTimerMap:           cmap.New[*time.Timer](),
		endPublicityTimerMap:      cmap.New[*time.Timer](),
		gmTimerMap:                make(map[string]interface{}),
		gmTimerLock:               &sync.RWMutex{},
		auctionItemIndex:          cmap.New[cmap.ConcurrentMap[string, *LockedBTree]](),
		auctionItemPublicityIndex: cmap.New[cmap.ConcurrentMap[string, *LockedBTree]](),
		blackList:                 make([]uint64, 0),
		blackListLock:             &sync.RWMutex{},
		updateTimerMap:            cmap.New[*time.Timer](),
		addCh:                     make(chan *CacheItem, 1000000),
	}

	return auctionMgr
}

const loadSize = 1000

// Init 初始化拍卖行管理器
func (am *AuctionMgr) Init() {
	appLog.Info("start init auction data from db~")
	am.isDBLoaded = false
	go am.procAuctionItemIndex()
	am._loadAuctionAllItemData()
	am._loadAuctionLastPricesData()
	am._loadAuctionAvgPricesData()
	am._loadAuctionBlackListData()
	am.onInitAuctionFromDB()
	am.isDBLoaded = true
	am.app.initedMutex.Lock()
	defer am.app.initedMutex.Unlock()
	am.app.inited = true
}

func (am *AuctionMgr) procAuctionItemIndex() {
	for cacheItem := range am.addCh {
		am.addAuctionItemToIndex(cacheItem.IndexKey, cacheItem.IndexVal, cacheItem.AuctionItem)
	}
}

func (am *AuctionMgr) _loadAuctionAvgPricesData() {
	offset := 0
	am.priceRecord.avgPriceLock.Lock()
	defer am.priceRecord.avgPriceLock.Unlock()
	for {
		// 每次加载 1000 条数据
		auctionItemRecords, err := am.loadAuctionItemRecordsFromDB(offset)
		if err != nil {
			appLog.Error("loadAuctionItemRecordsFromDB err: ", err)
		}
		if len(auctionItemRecords) == 0 {
			// 加载的数据为空，说明数据已经加载完
			break
		}

		for _, auctionItemRecord := range auctionItemRecords {
			am.priceRecord.itemAvgPriceRecords[GetPriceItemKey(auctionItemRecord.serverId, auctionItemRecord.itemId)] = auctionItemRecord
		}
		offset += 1000
	}
}

func (am *AuctionMgr) _loadAuctionBlackListData() {
	offset := 0
	for {
		// 每次加载 1000 条数据
		auctionBlackLists, err := am.loadAuctionBlackListFromDB(offset)
		if err != nil {
			appLog.Error("loadAuctionBlackListFromDB err: ", err)
		}
		if len(auctionBlackLists) == 0 {
			// 加载的数据为空，说明数据已经加载完
			break
		}

		am.blackList = append(am.blackList, auctionBlackLists...)
		offset += 1000
	}
}

func (am *AuctionMgr) loadAuctionBlackListFromDB(offset int) ([]uint64, error) {
	stmt, err := am.db.Prepare("SELECT `playerGBId` FROM `auction_blackList` LIMIT ?, ?")
	if err != nil {
		appLog.Error("loadAuctionBlackListFromDB err: ", err)
		return nil, err
	}
	defer stmt.Close()

	rows, err := stmt.Query(offset, loadSize)
	if err != nil {
		appLog.Error("loadAuctionBlackListFromDB err: ", err)
		return nil, err
	}
	defer rows.Close()

	auctionBlackLists := make([]uint64, 0)
	for rows.Next() {
		var playerGbId uint64
		err = rows.Scan(&playerGbId)
		if err != nil {
			appLog.Error("loadAuctionBlackListFromDB err: ", err)
			continue
		}
		auctionBlackLists = append(auctionBlackLists, playerGbId)
	}
	return auctionBlackLists, nil
}

func (am *AuctionMgr) loadAuctionItemRecordsFromDB(offset int) ([]*AuctionItemAvgRecord, error) {
	stmt, err := am.db.Prepare("SELECT `serverId`, `itemId`, `totalPrice`, `number`, `avgPrice`, `recentPrices`, `tLastUpdateTime` FROM `auction_priceRecord_avgPrices` LIMIT ?, ?")
	if err != nil {
		appLog.Error("loadAuctionItemRecordsFromDB err: ", err)
		return nil, err
	}
	defer stmt.Close()

	rows, err := stmt.Query(offset, loadSize)
	if err != nil {
		appLog.Error("loadAuctionItemRecordsFromDB err: ", err)
		return nil, err
	}
	defer rows.Close()

	auctionItemRecords := make([]*AuctionItemAvgRecord, 0)
	for rows.Next() {
		auctionItemRecord := &AuctionItemAvgRecord{}
		var recentPricesJsonStr string
		err = rows.Scan(&auctionItemRecord.serverId, &auctionItemRecord.itemId, &auctionItemRecord.totalPrice, &auctionItemRecord.number, &auctionItemRecord.avgPrice, &recentPricesJsonStr, &auctionItemRecord.lastUpdateTime)
		if err != nil {
			return nil, err
		}

		// 这里先去查找兑换的合服信息
		serverId := common.GetGameServerMergeRoot(auctionItemRecord.serverId)
		// 不是本组的，过滤掉
		if !common.CheckServerIdInGroup(am.app.groupId, serverId) {
			continue
		}

		auctionItemRecord.serverId = uint32(serverId)

		if recentPricesJsonStr != "" {
			err = json.Unmarshal([]byte(recentPricesJsonStr), &auctionItemRecord.recentPrices)
			if err != nil {
				appLog.Errorw("loadAuctionItemRecordsFromDB unmarshal recentPrices failed", "itemId", auctionItemRecord.itemId, "err", err)
				auctionItemRecord.recentPrices = make([]DailyPrice, 0)
			}
		} else {
			auctionItemRecord.recentPrices = make([]DailyPrice, 0)
		}
		auctionItemRecords = append(auctionItemRecords, auctionItemRecord)
	}

	return auctionItemRecords, nil
}

func (am *AuctionMgr) _loadAuctionLastPricesData() {
	offset := 0
	am.priceRecord.rcdPriceLock.Lock()
	defer am.priceRecord.rcdPriceLock.Unlock()
	for {
		// 每次加载 1000 条数据
		auctionItemLastPriceRecords, err := am.loadAuctionItemLastRecordsFromDB(offset)
		if err != nil {
			appLog.Error("loadAuctionItemLastRecordsFromDB err: ", err)
			return
		}
		if len(auctionItemLastPriceRecords) == 0 {
			// 加载的数据为空，说明数据已经加载完
			break
		}
		for _, auctionItemLastRecord := range auctionItemLastPriceRecords {
			am.priceRecord.itemLastPriceData[GetPriceItemKey(auctionItemLastRecord.serverId, auctionItemLastRecord.itemId)] = auctionItemLastRecord
		}
		offset += 1000
	}
}

func (am *AuctionMgr) loadAuctionItemLastRecordsFromDB(offset int) ([]*AuctionItemLastRecord, error) {
	stmt, err := am.db.Prepare("SELECT `serverId`, `itemId`, `price` FROM `auction_priceRecord_lastPrices` LIMIT ?, ?")
	if err != nil {
		appLog.Error("loadAuctionItemLastRecordsFromDB err: ", err)
		return nil, err
	}
	defer stmt.Close()

	rows, err := stmt.Query(offset, loadSize)
	if err != nil {
		appLog.Error("loadAuctionItemLastRecordsFromDB err: ", err)
		return nil, err
	}
	defer rows.Close()

	auctionItemLastPriceRecords := make([]*AuctionItemLastRecord, 0)
	for rows.Next() {
		auctionIteLastPriceRecord := &AuctionItemLastRecord{}
		err = rows.Scan(&auctionIteLastPriceRecord.serverId, &auctionIteLastPriceRecord.itemId, &auctionIteLastPriceRecord.price)
		if err != nil {
			appLog.Error("loadAuctionItemLastRecordsFromDB err: ", err)
			return nil, err
		}
		// 这里先去查找兑换的合服信息
		serverId := common.GetGameServerMergeRoot(auctionIteLastPriceRecord.serverId)
		// 不是本组的，过滤掉
		if !common.CheckServerIdInGroup(am.app.groupId, serverId) {
			continue
		}
		auctionIteLastPriceRecord.serverId = uint32(serverId)

		auctionItemLastPriceRecords = append(auctionItemLastPriceRecords, auctionIteLastPriceRecord)
	}

	return auctionItemLastPriceRecords, nil
}

func (am *AuctionMgr) _loadAuctionAllItemData() error {
	fromId := 0
	for {
		auctionItems, lastId, err := am.loadAuctionItemsFromDB(fromId)
		fromId = lastId
		if err != nil {
			appLog.Error("loadAuctionItemsFromDB err: ", err)
			return err
		}
		if len(auctionItems) == 0 {
			// 加载的数据为空，说明数据已经加载完
			break
		}
		//offset += 10000
	}

	return nil
}

func (am *AuctionMgr) loadAuctionItemsFromDB(lastId int) ([]*AuctionItem, int, error) {
	var auctionItems []*AuctionItem
	query := fmt.Sprintf("SELECT id, serverId, auctionType, auctionItemUUID, addTime, itemData_itemId, itemData_itemNum, itemData_createTime, itemData_expireTime, itemData_uniqueId, itemData_bindType, itemData_attrJson, price, number, bagType, source, status, locked, extraInfo, tCreate, fromPlayerGBID, addPublicityTime FROM auction_auctionItemData where id > %d order by id asc LIMIT 10000 ", lastId)
	rows, err := am.db.Query(query)
	if err != nil {
		return auctionItems, lastId, err
	}
	defer rows.Close()

	for rows.Next() {
		var itemData = ItemData{}

		var ai = AuctionItem{ItemData: &itemData, mu: &sync.RWMutex{}, EquipExtraCache: make(map[string]int32)}
		err := rows.Scan(&lastId, &ai.ServerId, &ai.AuctionType, &ai.AuctionItemUUID, &ai.AddTime, &ai.ItemData.ItemId, &ai.ItemData.ItemNum, &ai.ItemData.CreateTime, &ai.ItemData.ExpireTime, &ai.ItemData.UniqueId, &ai.ItemData.BindType, &ai.ItemData.AttrJson, &ai.Price, &ai.Number, &ai.BagType, &ai.Source, &ai.Status, &ai.Locked, &ai.ExtraInfo, &ai.TCreate, &ai.FromPlayerGBID, &ai.AddPublicityTime)
		if err != nil {
			appLog.Error("loadAuctionItemsFromDB: Scan err", err)
			return auctionItems, lastId, err
		}

		// 这里先去查找兑换的合服信息
		serverId := common.GetGameServerMergeRoot(ai.ServerId)
		// 不是本组的，过滤掉
		if !common.CheckServerIdInGroup(am.app.groupId, serverId) {
			continue
		}
		ai.ServerId = uint32(serverId)

		ai.EachPrice = float32(ai.Price) / float32(ai.Number)
		var m map[string]interface{}
		err = json.Unmarshal([]byte(ai.ExtraInfo), &m)
		if err != nil {
			appLog.Error("loadAuctionItemsFromDB: Unmarshal err", err)
			return auctionItems, lastId, err
		}

		if v, ok := m[EQUIP_GRADE_LEVEL]; ok {
			ai.EquipExtraCache[EQUIP_GRADE_LEVEL] = int32(v.(float64))
		}
		if v, ok := m[EQUIP_ENHANCE_LEVEL]; ok {
			ai.EquipExtraCache[EQUIP_ENHANCE_LEVEL] = int32(v.(float64))
		}

		ai.init()
		am.auctionItems.Set(strconv.FormatUint(ai.AuctionItemUUID, 10), &ai)
		auctionItems = append(auctionItems, &ai)
	}

	return auctionItems, lastId, nil
}

func (am *AuctionMgr) onInitAuctionFromDB() {
	am.refreshAuctionIndexData()
	am.refreshDaily()
}

//func (am *AuctionMgr) refreshHourly() {
//	now := time.Now()
//	nextHour := time.Date(now.Year(), now.Month(), now.Day(), now.Hour()+1, 0, 0, 0, now.Location())
//	duration := nextHour.Sub(now)
//	ticker := time.NewTicker(duration)
//	go func() {
//		for {
//			<-ticker.C
//			appLog.Info("refreshHourly start")
//			am.refreshItemPriceData()
//			appLog.Info("refreshHourly end")
//			ticker.Reset(1 * time.Hour)
//		}
//	}()
//}

func isDiffDay(tLastUpdateTime, tNow time.Time) bool {
	curDay := time.Date(tNow.Year(), tNow.Month(), tNow.Day(), 5, 0, 0, 0, tNow.Location())
	//判断tNow是否小于curDay
	if tNow.Before(curDay) {
		yesterday := time.Date(tNow.Year(), tNow.Month(), tNow.Day()-1, 5, 0, 0, 0, tNow.Location())
		if tLastUpdateTime.Before(yesterday) {
			return true
		}
	} else {
		if tLastUpdateTime.Before(curDay) {
			return true
		}
	}

	return false
}

// 每天凌晨5点更新
func (am *AuctionMgr) refreshDaily() {
	tNow := time.Now()
	am.refreshItemPriceData(true)

	curDay := time.Date(tNow.Year(), tNow.Month(), tNow.Day(), 5, 0, 0, 0, tNow.Location())
	var duration time.Duration
	//判断tNow是否小于curDay
	if tNow.Before(curDay) {
		duration = curDay.Sub(tNow)
	} else {
		nextDay := time.Date(tNow.Year(), tNow.Month(), tNow.Day()+1, 5, 0, 0, 0, tNow.Location())
		duration = nextDay.Sub(tNow)
	}
	ticker := time.NewTicker(duration)
	go func() {
		for {
			<-ticker.C
			appLog.Info("refreshDaily start")
			am.refreshItemPriceData(false)
			am.app.broadcastAllItemsPriceInfoList()
			appLog.Info("refreshDaily end")
			ticker.Reset(24 * time.Hour)
		}
	}()
}

func (am *AuctionMgr) refreshItemPriceData(needDoubleCheck bool) {
	curTime := time.Now()
	am.priceRecord.avgPriceLock.Lock()
	defer am.priceRecord.avgPriceLock.Unlock()
	today := time.Now().Format("2006-01-02")
	for _, auctionItemRecord := range am.priceRecord.itemAvgPriceRecords {
		if needDoubleCheck {
			if !isDiffDay(time.Unix(auctionItemRecord.lastUpdateTime, 0), curTime) {
				continue
			}
		}
		if auctionItemRecord.number > 0 {
			auctionItemRecord.avgPrice = float32(auctionItemRecord.totalPrice) / float32(auctionItemRecord.number)
			daily := DailyPrice{
				Date:       today,
				TotalPrice: auctionItemRecord.totalPrice,
				Number:     auctionItemRecord.number,
				AvgPrice:   auctionItemRecord.avgPrice,
			}
			auctionItemRecord.totalPrice, auctionItemRecord.number = 0, 0
			auctionItemRecord.recentPrices = append(auctionItemRecord.recentPrices, daily)
			if len(auctionItemRecord.recentPrices) > 30 {
				auctionItemRecord.recentPrices = auctionItemRecord.recentPrices[1:]
			}
			auctionItemRecord.lastUpdateTime = time.Now().Unix()
			err := auctionItemRecord.Update(am.db, true)
			if err != nil {
				appLog.Error("refreshItemPriceData: Update err", err)
			}
		}
	}
}

func (am *AuctionMgr) getAllItemsPriceInfoList() []*gameServerService.ItemPriceInfo {
	am.priceRecord.avgPriceLock.Lock()
	defer am.priceRecord.avgPriceLock.Unlock()

	return am.priceRecord.GetAllItemPriceInfos()
}
func (am *AuctionMgr) refreshAuctionIndexData() {
	// 当前时间
	curTime := time.Now().Unix()
	// 公示时间
	appLog.Info("refreshAuctionIndexData: start ", am.auctionItems.Count())
	for item := range am.auctionItems.IterBuffered() {
		auctionItem := item.Val
		if auctionItem.Status == AUCTION_STATUS_PUBLICITY {
			// 检查是否在公示期
			if auctionItem.AddTime+auctionItem.GetPublicityGap() > curTime {
				auctionItemUUID := auctionItem.AuctionItemUUID
				auctionItemUUIDStr := strconv.FormatUint(auctionItemUUID, 10)
				if _, ok := am.endPublicityTimerMap.Get(auctionItemUUIDStr); ok {
					appLog.Error("refreshAuctionIndexData: publicity timer already exist:", auctionItemUUID)
					continue
				}
				// 加入公示索引
				for _, indexKey := range auctionIndexKeys {
					am.addAuctionItemToPublicityIndex(indexKey, auctionItem.getIndexVal(indexKey), auctionItem)
				}
				// 挂公示结束定时器
				curTime := time.Now().Unix()
				duration := auctionItem.AddTime + auctionItem.GetPublicityGap() - curTime
				if duration > 0 {
					timer := time.AfterFunc(time.Duration(duration)*time.Second, func() {
						am.setItemSelling(auctionItemUUID, true)
					})
					am.endPublicityTimerMap.Set(auctionItemUUIDStr, timer)
				} else {
					am.setItemSelling(auctionItemUUID, false)
				}

				continue
				// 处理正常公示期结束
			}
		}
		// 不管是否已过期公示期，出售期，都需要检查是否过期
		if auctionItem.Status == AUCTION_STATUS_SELLING || auctionItem.Status == AUCTION_STATUS_PUBLICITY {
			if auctionItem.isItemExpired(curTime) {
				am.setStatus(AUCTION_STATUS_EXPIRED, auctionItem, false)
				// 加入玩家队列
				am.addAuctionItemToIndex(INDEX_KEY_PLAYERGBID, auctionItem.getIndexVal(INDEX_KEY_PLAYERGBID), auctionItem)
			} else {
				// 未过期，公示期需要进入出售期
				am.setStatus(AUCTION_STATUS_SELLING, auctionItem, false)
				// 加入出售索引
				for _, indexKey := range auctionIndexKeys {
					am.addAuctionItemToIndex(indexKey, auctionItem.getIndexVal(indexKey), auctionItem)
				}
				// 挂出售期超时定期器
				auctionItemUUID := auctionItem.AuctionItemUUID
				auctionItemUUIDStr := strconv.FormatUint(auctionItemUUID, 10)
				if _, ok := am.expiredTimerMap.Get(auctionItemUUIDStr); ok {
					appLog.Error("refreshAuctionIndexData: expired timer already exist:", auctionItemUUID)
					continue
				}
				curTime := time.Now().Unix()
				duration := auctionItem.itemExpiredTime() - curTime
				timer := time.AfterFunc(time.Duration(duration)*time.Second, func() {
					am.setItemExpired(auctionItemUUID)
				})
				am.expiredTimerMap.Set(auctionItemUUIDStr, timer)
			}
			continue
		}
		// 其他的状态，一律放在玩家索引里
		am.addAuctionItemToIndex(INDEX_KEY_PLAYERGBID, auctionItem.getIndexVal(INDEX_KEY_PLAYERGBID), auctionItem)
	}
}

func (am *AuctionMgr) addAuctionItemToIndex(indexKey string, indexValue string, auctionItem *AuctionItem) {
	if auctionItem.IsDestroyed || auctionItem.Number == 0 {
		appLog.Debug("addAuctionItemToIndex: auctionItem is removed", auctionItem.AuctionItemUUID)
		return
	}

	isIn, ok := auctionItem.IsInIndexMap.Get(indexKey)
	if ok && isIn {
		appLog.Debugw("addAuctionItemToIndex: auctionItem is already in index", "auctionItemUUID", auctionItem.AuctionItemUUID, "indexKey", indexKey)
		return
	}

	innerMap, _ := am.auctionItemIndex.GetOrCreate(indexKey, func() cmap.ConcurrentMap[string, *LockedBTree] {
		return cmap.New[*LockedBTree]()
	})

	lockedBTree, _ := innerMap.GetOrCreate(indexValue, func() *LockedBTree {
		return NewLockedBTree()
	})

	lockedBTree.mu.Lock()
	defer lockedBTree.mu.Unlock()
	if auctionItem.IsDestroyed || auctionItem.Number == 0 || auctionItem.IsNeedRemove {
		appLog.Debugw("addAuctionItemToIndex: auctionItem is removed in lock", "auctionItemUUID", auctionItem.AuctionItemUUID)
		return
	}

	isIn, ok = auctionItem.IsInIndexMap.Get(indexKey)
	if ok && isIn {
		appLog.Debugw("addAuctionItemToIndex: auctionItem is already in index in lock", "auctionItemUUID", auctionItem.AuctionItemUUID, "indexKey", indexKey)
		return
	}
	auctionItem.IsInIndexMap.Set(indexKey, true)

	if indexKey == INDEX_KEY_ITEMID {
		if auctionItem.Status == AUCTION_STATUS_EXPIRED {
			appLog.Debugw("addAuctionItemToIndex: auctionItem is expired", "auctionItemUUID", auctionItem.AuctionItemUUID)
			return
		}
	}
	lockedBTree.tree.ReplaceOrInsert(auctionItem)
}

func (am *AuctionMgr) addAuctionItemToPublicityIndex(indexKey string, indexValue string, auctionItem *AuctionItem) {
	if auctionItem.IsDestroyed || auctionItem.Number == 0 {
		appLog.Debug("addAuctionItemToPublicityIndex: auctionItem is removed", auctionItem.AuctionItemUUID)
		return
	}

	isIn, ok := auctionItem.IsInPublicityIndexMap.Get(indexKey)
	if ok && isIn {
		appLog.Debugw("addAuctionItemToPublicityIndex: auctionItem is already in index", "auctionItemUUID", auctionItem.AuctionItemUUID, "indexKey", indexKey)
		return
	}

	innerMap, _ := am.auctionItemPublicityIndex.GetOrCreate(indexKey, func() cmap.ConcurrentMap[string, *LockedBTree] {
		return cmap.New[*LockedBTree]()
	})

	lockedBTree, _ := innerMap.GetOrCreate(indexValue, func() *LockedBTree {
		return NewLockedBTree()
	})

	lockedBTree.mu.Lock()
	defer lockedBTree.mu.Unlock()
	if auctionItem.IsDestroyed || auctionItem.Number == 0 || auctionItem.IsNeedRemove {
		appLog.Debugw("addAuctionItemToPublicityIndex: auctionItem is removed in lock", "auctionItemUUID", auctionItem.AuctionItemUUID)
		return
	}

	isIn, ok = auctionItem.IsInPublicityIndexMap.Get(indexKey)
	if ok && isIn {
		appLog.Debugw("addAuctionItemToPublicityIndex: auctionItem is already in index in lock", "auctionItemUUID", auctionItem.AuctionItemUUID, "indexKey", indexKey)
		return
	}
	auctionItem.IsInPublicityIndexMap.Set(indexKey, true)

	if indexKey == INDEX_KEY_ITEMID {
		if auctionItem.Status == AUCTION_STATUS_SELLING {
			appLog.Debugw("addAuctionItemToPublicityIndex: auctionItem is selling", "auctionItemUUID", auctionItem.AuctionItemUUID)
			return
		}
	}
	lockedBTree.tree.ReplaceOrInsert(auctionItem)
}

func (am *AuctionMgr) getAuctionItemIndex(indexKey string, indexValue string) *LockedBTree {
	innerMap, ok := am.auctionItemIndex.Get(indexKey)
	if !ok {
		return nil
	}
	lockedBtree, ok := innerMap.Get(indexValue)
	if !ok {
		return nil
	}

	return lockedBtree
}

func (am *AuctionMgr) getAuctionItemPublicityIndex(indexKey string, indexValue string) *LockedBTree {
	innerMap, ok := am.auctionItemPublicityIndex.Get(indexKey)
	if !ok {
		return nil
	}
	lockedBtree, ok := innerMap.Get(indexValue)
	if !ok {
		return nil
	}

	return lockedBtree
}

func (am *AuctionMgr) getAuctionItemIndexNum(indexKey string, indexValue string) uint32 {
	innerMap, ok := am.auctionItemIndex.Get(indexKey)
	if !ok {
		return 0
	}
	lockedBtree, ok := innerMap.Get(indexValue)
	if !ok {
		return 0
	}
	if lockedBtree == nil {
		return 0
	}

	if lockedBtree.tree == nil {
		return 0
	}

	return uint32(lockedBtree.tree.Len())
}

// 获取最低售价的物品
func (am *AuctionMgr) GetLowestPriceItem(indexKey string, indexValue string) float32 {
	lockedBtree := am.getAuctionItemIndex(indexKey, indexValue)
	if lockedBtree == nil {
		return 0
	}
	lockedBtree.mu.RLock()
	defer lockedBtree.mu.RUnlock()
	if lockedBtree.tree.Len() == 0 {
		return 0
	}
	auctionItem, ok := lockedBtree.tree.Min()
	if !ok {
		return 0
	}

	return auctionItem.EachPrice
}

func (am *AuctionMgr) getAuctionItemPublicityIndexNum(indexKey string, indexValue string) uint32 {
	innerMap, ok := am.auctionItemPublicityIndex.Get(indexKey)
	if !ok {
		return 0
	}
	lockedBtree, ok := innerMap.Get(indexValue)
	if !ok {
		return 0
	}
	if lockedBtree == nil {
		return 0
	}

	if lockedBtree.tree == nil {
		return 0
	}

	return uint32(lockedBtree.tree.Len())
}

// 获取最低售价的物品
func (am *AuctionMgr) GetLowestPricePublicityItem(indexKey string, indexValue string) float32 {
	lockedBtree := am.getAuctionItemPublicityIndex(indexKey, indexValue)
	if lockedBtree == nil {
		return 0
	}
	lockedBtree.mu.RLock()
	defer lockedBtree.mu.RUnlock()
	if lockedBtree.tree.Len() == 0 {
		return 0
	}
	auctionItem, ok := lockedBtree.tree.Min()
	if !ok {
		return 0
	}

	return auctionItem.EachPrice
}

func (am *AuctionMgr) removeAuctionItemFromIndex(indexKey string, indexVal string, dstAuctionItem *AuctionItem) *AuctionItem {
	isIn, ok := dstAuctionItem.IsInIndexMap.Get(indexKey)
	if !ok || !isIn {
		appLog.Debugw("removeAuctionItemFromIndex: auctionItem is not in index", "auctionItemUUID", dstAuctionItem.AuctionItemUUID, "indexKey", indexKey)
		return nil
	}
	dstAuctionItem.IsInIndexMap.Set(indexKey, false)

	innerMap, ok := am.auctionItemIndex.Get(indexKey)
	if !ok {
		appLog.Errorw("removeAuctionItemFromIndex: auctionItem is not in index", "auctionItemUUID", dstAuctionItem.AuctionItemUUID, "indexKey", indexKey)
		return nil
	}
	lockedBtree, ok := innerMap.Get(indexVal)
	if !ok {
		appLog.Errorw("removeAuctionItemFromIndex: auctionItem is not in index", "auctionItemUUID", dstAuctionItem.AuctionItemUUID, "indexKey", indexKey)
		return nil
	}

	lockedBtree.mu.Lock()
	defer lockedBtree.mu.Unlock()
	lockedBtree.tree.Delete(dstAuctionItem)

	return nil
}

func (am *AuctionMgr) removeAuctionItemFromPublicityIndex(indexKey string, indexVal string, dstAuctionItem *AuctionItem) *AuctionItem {
	isIn, ok := dstAuctionItem.IsInPublicityIndexMap.Get(indexKey)
	if !ok || !isIn {
		appLog.Debugw("removeAuctionItemFromPublicityIndex: auctionItem is not in index", "auctionItemUUID", dstAuctionItem.AuctionItemUUID, "indexKey", indexKey)
		return nil
	}
	dstAuctionItem.IsInPublicityIndexMap.Set(indexKey, false)

	innerMap, ok := am.auctionItemPublicityIndex.Get(indexKey)
	if !ok {
		appLog.Errorw("removeAuctionItemFromPublicityIndex: auctionItem is not in index", "auctionItemUUID", dstAuctionItem.AuctionItemUUID, "indexKey", indexKey)
		return nil
	}
	lockedBtree, ok := innerMap.Get(indexVal)
	if !ok {
		appLog.Errorw("removeAuctionItemFromPublicityIndex: auctionItem is not in index", "auctionItemUUID", dstAuctionItem.AuctionItemUUID, "indexKey", indexKey)
		return nil
	}

	lockedBtree.mu.Lock()
	defer lockedBtree.mu.Unlock()
	lockedBtree.tree.Delete(dstAuctionItem)

	return nil
}

func (am *AuctionMgr) removeAuctionItemsFromIndex(indexKey string, indexVal string, dstAuctionItems []*AuctionItem) error {
	innerMap, ok := am.auctionItemIndex.Get(indexKey)
	if !ok {
		appLog.Errorw("removeAuctionItemsFromIndex: auctionItem is not in index", "indexKey", indexKey, "indexVal", indexVal)
		return errors.New("removeAuctionItemsFromIndex not found")
	}
	lockedBtree, ok := innerMap.Get(indexVal)
	if !ok {
		appLog.Errorw("removeAuctionItemsFromIndex: auctionItem is not in index", "indexKey", indexKey, "indexVal", indexVal)
		return errors.New("removeAuctionItemsFromIndex not found")
	}

	for _, dstAuctionItem := range dstAuctionItems {
		isIn, ok := dstAuctionItem.IsInIndexMap.Get(indexKey)
		if !ok || !isIn {
			appLog.Debugw("removeAuctionItemsFromIndex: auctionItem is not in index", "auctionItemUUID", dstAuctionItem.AuctionItemUUID, "indexKey", indexKey)
			continue
		}
		dstAuctionItem.IsInIndexMap.Set(indexKey, false)
		lockedBtree.tree.Delete(dstAuctionItem)
	}

	return nil
}

func (am *AuctionMgr) AddAuctionItem(auctionType uint8, auctionItemUUID uint64, addTime int64, itemData *ItemData, price uint64, number uint32, bagType uint8, source uint8, status uint8, locked uint64, extraInfo string, fromPlayerGBID uint64, addPublicityTime uint32) (*AuctionItem, error) {
	auctionItem := NewAuctionItem(auctionType, auctionItemUUID, addTime, itemData, price, number, bagType, source, status, locked, extraInfo, fromPlayerGBID, addPublicityTime)

	_, err := am.GetAuctionItem(auctionItem.AuctionItemUUID)
	if err == nil {
		appLog.Errorw("auction item already exists", "auctionItemUUID", auctionItem.AuctionItemUUID)
		return nil, errors.New(fmt.Sprint("auction item already exists", auctionItem.AuctionItemUUID))
	}

	am.auctionItems.Set(strconv.FormatUint(auctionItemUUID, 10), auctionItem)

	return auctionItem, nil
}

func (am *AuctionMgr) DeleteAuctionItem(auctionItemUUID uint64) error {
	auctionItem, err := am.GetAuctionItem(auctionItemUUID)
	if err != nil {
		return fmt.Errorf("auction item not found")
	}

	err = auctionItem.Delete(am.db)
	if err != nil {
		appLog.Errorw("auction item delete failed", "auctionItemUUID", auctionItemUUID, "err", err)
		return err
	}

	am.auctionItems.Remove(strconv.FormatUint(auctionItemUUID, 10))

	auctionItemUUIDStr := strconv.FormatUint(auctionItemUUID, 10)
	timer, ok := am.expiredTimerMap.Get(auctionItemUUIDStr)
	if ok {
		if timer != nil {
			timer.Stop()
		}
		am.expiredTimerMap.Remove(auctionItemUUIDStr)
	}

	timer, ok = am.endPublicityTimerMap.Get(auctionItemUUIDStr)
	if ok {
		if timer != nil {
			timer.Stop()
		}
		am.endPublicityTimerMap.Remove(auctionItemUUIDStr)
	}

	auctionItem.IsDestroyed = true
	for _, indexKey := range auctionIndexKeys {
		am.removeAuctionItemFromIndex(indexKey, auctionItem.getIndexVal(indexKey), auctionItem)
		am.removeAuctionItemFromPublicityIndex(indexKey, auctionItem.getIndexVal(indexKey), auctionItem)
	}

	if auctionItem.FromPlayerGBID != 0 {
		gameServer := am.app.GetGameServer(auctionItem.ServerId, 0)
		if gameServer == nil {
			appLog.Errorw("DeleteAuctionItem: gameServer == nil", "uuid", auctionItem.AuctionItemUUID, "playerGBID", auctionItem.FromPlayerGBID, "serverId", auctionItem.ServerId)
		} else {
			am.app.RefreshPlayerCoinAuctionData(auctionItem.FromPlayerGBID, gameServer.AuctionService.(*GameServerService))
		}
	}

	return nil
}

func (am *AuctionMgr) GetAuctionItem(auctionItemUUID uint64) (*AuctionItem, error) {
	auctionItem, ok := am.auctionItems.Get(strconv.FormatUint(auctionItemUUID, 10))
	if !ok {
		return nil, fmt.Errorf("auction item not found: %d", auctionItemUUID)
	}

	return auctionItem, nil
}

func (am *AuctionMgr) GetItemLastPrice(itemId uint32) float32 {
	var price = float32(0)
	price = am.priceRecord.GetItemLastPrice(itemId, common.GetGameGroupServerIdMap(am.app.groupId))

	return price
}

func (am *AuctionMgr) GetItemAvgPrice(itemId uint32) (float32, float32) {
	var price = float32(0)
	var price7 = float32(0)
	price, price7 = am.priceRecord.GetItemAvgPrice(itemId, common.GetGameGroupServerIdMap(am.app.groupId))

	return price, price7
}

func (am *AuctionMgr) CheckBuyItem(auctionItemUUID uint64, buyerGbId uint64, buyNumber uint32) (*AuctionItem, int) {
	auctionItem, err := am.GetAuctionItem(auctionItemUUID)
	if err != nil {
		return auctionItem, AUCTION_NOT_IN_AUCTION
	}

	if auctionItem.FromPlayerGBID == buyerGbId {
		return auctionItem, AUCTION_ITEM_IS_SELF_SALE
	}

	if auctionItem.Status == AUCTION_STATUS_EXPIRED {
		return auctionItem, AUCTION_IS_EXPIRED
	}

	if auctionItem.Number != buyNumber {
		return auctionItem, AUCTION_BUY_ITEM_NOT_ENOUGH
	}

	if !auctionItem.CheckInSnatch() {
		if auctionItem.CheckInPublicity() {
			return auctionItem, AUCTION_ITEM_IS_IN_PUBLICITY
		}
		if auctionItem.isLocked(0) {
			return auctionItem, AUCTION_ITEM_IS_LOCKED
		}
	}

	return auctionItem, AUCTION_OK
}

func (am *AuctionMgr) CheckBuyItems(auctionItemUUID uint64, buyerGbId uint64, buyNumber uint32) (*AuctionItem, int) {
	auctionItem, err := am.GetAuctionItem(auctionItemUUID)
	if err != nil {
		return auctionItem, AUCTION_NOT_IN_AUCTION
	}

	if auctionItem.FromPlayerGBID == buyerGbId {
		return auctionItem, AUCTION_ITEM_IS_SELF_SALE
	}

	if auctionItem.Status == AUCTION_STATUS_EXPIRED {
		return auctionItem, AUCTION_IS_EXPIRED
	}

	if auctionItem.Number != buyNumber {
		return auctionItem, AUCTION_BUY_ITEM_NOT_ENOUGH
	}

	if !auctionItem.CheckInSelling() {
		return auctionItem, AUCTION_ITEM_IS_NOT_IN_SELLING
	}

	return auctionItem, AUCTION_OK
}

func (am *AuctionMgr) doBuyItem(auctionItem *AuctionItem, buyNum uint32, fromPlayerGBID uint64, extra map[string]interface{}) (map[string]interface{}, error) {
	if buyNum > auctionItem.Number {
		appLog.Errorw("auction buy item num is more than auction item number", "buyNum", buyNum, "auctionItemNumber", auctionItem.Number, "auctionItemUUID", auctionItem.AuctionItemUUID)
		return extra, errors.New(fmt.Sprint("auction buy item num is more than auction item number", auctionItem.AuctionItemUUID))
	}
	if buyNum == auctionItem.Number {
		err := am.DeleteAuctionItem(auctionItem.AuctionItemUUID)
		if err != nil {
			appLog.Errorw("auction delete item error", "auctionItemUUID", auctionItem.AuctionItemUUID, "err", err)
			return extra, err
		}
	} else {
		auctionItem.Number -= buyNum
		err := auctionItem.Update(am.db, []string{"number"}, []interface{}{auctionItem.Number})
		if err != nil {
			appLog.Errorw("auction update item error", "auctionItemUUID", auctionItem.AuctionItemUUID, "err", err)
			return extra, err
		}
		indexKey := INDEX_KEY_ITEMID
		auctionItem.unLock()
		cacheItem := &CacheItem{
			IndexKey:    indexKey,
			IndexVal:    auctionItem.getIndexVal(indexKey),
			AuctionItem: auctionItem,
			IsInit:      false,
		}
		am.addCh <- cacheItem
	}

	am.onPlayerAuctionItemBeSaled(auctionItem, buyNum, extra, fromPlayerGBID)

	return extra, nil
}

func (am *AuctionMgr) onPlayerAuctionItemBeSaled(auctionItem *AuctionItem, buyNumber uint32, extra map[string]interface{}, fromPlayerGBID uint64) {
	totalPrice := auctionItem.Price
	extra["totalPrice"] = totalPrice

	if auctionItem.getServerId() != 0 {
		extraB, err := json.Marshal(extra)
		if err != nil {
			appLog.Errorw("BuyItem: Marshal err", "err", err)
			return
		}
		am.app.onItemBeSaled(auctionItem, buyNumber, string(extraB), fromPlayerGBID)
	} else {
		appLog.Infow("auction item from player serverId is 0", "auctionItemUUID", auctionItem.AuctionItemUUID, "extra", extra, "fromPlayerGBID", fromPlayerGBID)
	}
}

func (am *AuctionMgr) CheckCancelSaleItem(auctionItemUUID uint64, fromPlayerGBID uint64) (*AuctionItem, uint32) {
	auctionItem, err := am.GetAuctionItem(auctionItemUUID)
	if err != nil {
		return auctionItem, AUCTION_CANCEL_SALE_ITEM_NOT_FOUND
	}

	if auctionItem.Status != AUCTION_STATUS_INIT && auctionItem.Status != AUCTION_STATUS_SELLING && auctionItem.Status != AUCTION_STATUS_EXPIRED && auctionItem.Status != AUCTION_STATUS_PUBLICITY {
		return auctionItem, AUCTION_ITEM_CANNOT_CANCEL_SALE
	}

	if fromPlayerGBID != auctionItem.FromPlayerGBID {
		return auctionItem, AUCTION_CANCEL_SALE_GBID_NOT_MATCH
	}

	if auctionItem.CheckInSnatch() || auctionItem.checkLockedId(SNATCH_LOCK_ID) {
		return auctionItem, AUCTION_ITEM_IS_IN_SNATCH
	}

	if auctionItem.isLocked(0) {
		return auctionItem, AUCTION_ITEM_IS_LOCKED
	}

	return auctionItem, AUCTION_OK
}

func (am *AuctionMgr) doCancelSaleItemCheck(auctionItemUUID uint64, fromPlayerGBID uint64) (*AuctionItem, uint32) {
	auctionItem, err := am.GetAuctionItem(auctionItemUUID)
	if err != nil {
		return auctionItem, AUCTION_CANCEL_SALE_ITEM_NOT_FOUND
	}

	if auctionItem.Status != AUCTION_STATUS_INIT && auctionItem.Status != AUCTION_STATUS_SELLING && auctionItem.Status != AUCTION_STATUS_EXPIRED && auctionItem.Status != AUCTION_STATUS_PUBLICITY {
		return auctionItem, AUCTION_ITEM_CANNOT_CANCEL_SALE
	}

	if fromPlayerGBID != auctionItem.FromPlayerGBID {
		return auctionItem, AUCTION_CANCEL_SALE_GBID_NOT_MATCH
	}

	return auctionItem, AUCTION_OK
}

func (am *AuctionMgr) doCancelSaleItem(auctionItem *AuctionItem) error {
	err := am.DeleteAuctionItem(auctionItem.AuctionItemUUID)
	if err != nil {
		appLog.Errorw("auction delete item error", "auctionItemUUID", auctionItem.AuctionItemUUID, "err", err)
		return err
	}
	return nil
}

func (am *AuctionMgr) SearchItemByItemIds(itemIds []uint32, gradeLevels []int32, enhanceLevels []int32, fromPlayerGBID uint64, limit uint32, offset uint32, isPublicity uint32) ([]*AuctionItem, uint32) {
	var auctionItems []*AuctionItem
	var count uint32
	var allCount uint32
	hasGradeLevelFilter := false
	hasEnhanceLevelFilter := false
	if len(itemIds) == len(gradeLevels) {
		hasGradeLevelFilter = true
	}
	if len(itemIds) == len(enhanceLevels) {
		hasEnhanceLevelFilter = true
	}
	if isPublicity == 1 {
		for pos, itemId := range itemIds {
			innerMap, ok := am.auctionItemPublicityIndex.Get(INDEX_KEY_ITEMID)
			if !ok {
				continue
			}
			lockedBtree, ok := innerMap.Get(strconv.FormatUint(uint64(itemId), 10))
			if !ok {
				continue
			}

			if lockedBtree == nil {
				continue
			}
			idx := uint32(0)
			lockedBtree.mu.RLock()
			lockedBtree.tree.Ascend(func(auctionItem *AuctionItem) bool {
				if hasGradeLevelFilter {
					if gradeLevels[pos] != EQUIP_DEFAULT_VALUE {
						v, ok := auctionItem.EquipExtraCache[EQUIP_GRADE_LEVEL]
						if !ok || v != gradeLevels[pos] {
							return true
						}
					}
				}
				if hasEnhanceLevelFilter {
					if enhanceLevels[pos] != EQUIP_DEFAULT_VALUE {
						v, ok := auctionItem.EquipExtraCache[EQUIP_ENHANCE_LEVEL]
						if !ok || v != enhanceLevels[pos] {
							return true
						}
					}
				}
				if auctionItem.Status != AUCTION_STATUS_PUBLICITY {
					return true
				}
				if idx < offset {
					idx++
					return true
				}

				auctionItems = append(auctionItems, auctionItem)
				idx++
				count++

				return count < limit
			})
			allCount += uint32(lockedBtree.tree.Len())
			lockedBtree.mu.RUnlock()
		}
	} else {
		for pos, itemId := range itemIds {
			innerMap, ok := am.auctionItemIndex.Get(INDEX_KEY_ITEMID)
			if !ok {
				continue
			}
			lockedBtree, ok := innerMap.Get(strconv.FormatUint(uint64(itemId), 10))
			if !ok {
				continue
			}

			if lockedBtree == nil {
				continue
			}
			idx := uint32(0)
			lockedBtree.mu.RLock()
			lockedBtree.tree.Ascend(func(auctionItem *AuctionItem) bool {
				if hasGradeLevelFilter {
					if gradeLevels[pos] != EQUIP_DEFAULT_VALUE {
						v, ok := auctionItem.EquipExtraCache[EQUIP_GRADE_LEVEL]
						if !ok || v != gradeLevels[pos] {
							return true
						}
					}
				}
				if hasEnhanceLevelFilter {
					if enhanceLevels[pos] != EQUIP_DEFAULT_VALUE {
						v, ok := auctionItem.EquipExtraCache[EQUIP_ENHANCE_LEVEL]
						if !ok || v != enhanceLevels[pos] {
							return true
						}
					}
				}
				if auctionItem.Status != AUCTION_STATUS_SELLING {
					return true
				}

				if idx < offset {
					idx++
					return true
				}

				auctionItems = append(auctionItems, auctionItem)
				idx++
				count++

				return count < limit
			})
			allCount += uint32(lockedBtree.tree.Len())
			lockedBtree.mu.RUnlock()
		}
	}
	return auctionItems, allCount
}

func (am *AuctionMgr) GetPlayerAuctionItemsByPlayerGBID(playerGBID uint64) []*AuctionItem {
	var auctionItems []*AuctionItem
	lockedBtree := am.getAuctionItemIndex(INDEX_KEY_PLAYERGBID, strconv.FormatUint(playerGBID, 10))
	if lockedBtree != nil {
		lockedBtree.mu.RLock()
		defer lockedBtree.mu.RUnlock()
		lockedBtree.tree.Ascend(func(item *AuctionItem) bool {
			auctionItems = append(auctionItems, item)
			return true
		})
	}

	lockedBtree = am.getAuctionItemPublicityIndex(INDEX_KEY_PLAYERGBID, strconv.FormatUint(playerGBID, 10))
	if lockedBtree != nil {
		lockedBtree.mu.RLock()
		defer lockedBtree.mu.RUnlock()
		lockedBtree.tree.Ascend(func(item *AuctionItem) bool {
			auctionItems = append(auctionItems, item)
			return true
		})
	}
	return auctionItems
}

func (am *AuctionMgr) LoadPlayerAuctionItemUUIDs(playerGBID uint64) []uint64 {
	var auctionItemUUIDs = make([]uint64, 0)
	// 出售的数据
	lockedBtree := am.getAuctionItemIndex(INDEX_KEY_PLAYERGBID, strconv.FormatUint(playerGBID, 10)) // from auction item index
	if lockedBtree != nil {
		lockedBtree.mu.RLock()
		defer lockedBtree.mu.RUnlock()
		lockedBtree.tree.Ascend(func(item *AuctionItem) bool {
			auctionItemUUIDs = append(auctionItemUUIDs, item.AuctionItemUUID)
			return true
		})
	}

	// 公示的数据
	lockedBtree = am.getAuctionItemPublicityIndex(INDEX_KEY_PLAYERGBID, strconv.FormatUint(playerGBID, 10)) // from auction item index
	if lockedBtree != nil {
		lockedBtree.mu.RLock()
		defer lockedBtree.mu.RUnlock()
		lockedBtree.tree.Ascend(func(item *AuctionItem) bool {
			auctionItemUUIDs = append(auctionItemUUIDs, item.AuctionItemUUID)
			return true
		})
	}

	return auctionItemUUIDs
}

func (am *AuctionMgr) setStatus(status uint8, auctionItem *AuctionItem, isInit bool) {
	if status == auctionItem.Status {
		return
	}
	oldStatus := auctionItem.Status
	err := auctionItem.setStatus(status, am.db, isInit)
	if err != nil {
		appLog.Errorw("setStatus error", "err", err)
		return
	}

	if status == AUCTION_STATUS_SELLING {
		// 如果是从公示期过来的，需要移除公示期数据
		if oldStatus == AUCTION_STATUS_PUBLICITY {
			for _, indexKey := range auctionIndexKeys {
				am.removeAuctionItemFromPublicityIndex(indexKey, auctionItem.getIndexVal(indexKey), auctionItem)
			}
		}
		// 加入出售索引
		for _, indexKey := range auctionIndexKeys {
			am.addAuctionItemToIndex(indexKey, auctionItem.getIndexVal(indexKey), auctionItem)
		}
	} else if status == AUCTION_STATUS_EXPIRED {
		// 过期移除物品索引
		am.removeAuctionItemFromIndex(INDEX_KEY_ITEMID, auctionItem.getIndexVal(INDEX_KEY_ITEMID), auctionItem)
	} else if status == AUCTION_STATUS_PUBLICITY {
		// 加入公示期索引
		for _, indexKey := range auctionIndexKeys {
			am.addAuctionItemToPublicityIndex(indexKey, auctionItem.getIndexVal(indexKey), auctionItem)
		}
	}
}

func (am *AuctionMgr) gmSaleAuctionItem(itemId uint32, itemNum uint32, price uint64, num uint32, startTime uint32, endTime uint32) (string, error) {
	// if time.Now().Unix() < int64(startTime) || (time.Now().Unix() > int64(endTime) && endTime != 0) {
	// 	appLog.Errorw("gmSaleAuctionItem: time err", "now", time.Now().Unix(), "startTime", startTime, "endTime", endTime)
	// 	return "", nil
	// }

	// for i := 0; i < int(num); i++ {
	// 	var curTime = time.Now().Unix()
	// 	var item = &ItemData{
	// 		ItemId:     itemId,
	// 		ItemNum:    itemNum,
	// 		BindType:   1,
	// 		CreateTime: curTime,
	// 	}

	// 	auctionItemUUID := am.app.GenUUID()
	// 	extraMap := make(map[string]interface{})
	// 	extraMap["opUUID"] = am.app.GenUUID()
	// 	extraMap["serverId"] = AuctionAppConfig.GmLogServerId
	// 	tlogPropsMap := make(map[string]interface{})
	// 	tlogPropsMap["role_name"] = "GM"
	// 	extraMap["tlogProps"] = tlogPropsMap
	// 	extraInfo, err := json.Marshal(extraMap)
	// 	if err != nil {
	// 		appLog.Errorw("gmSaleAuctionItem: Marshal err", "err", err)
	// 		return "", err
	// 	}

	// 	auctionItem, err := am.AddAuctionItem(AUCTION_TYPE_COIN, auctionItemUUID, curTime, item, price, itemNum, BAG_TYPE_NORMAL, AUCTION_SOURCE_PLAYER, AUCTION_STATUS_INIT, 0, string(extraInfo), 0)
	// 	if err != nil {
	// 		appLog.Errorw("gmSaleAuctionItem: AddAuctionItem err", "err", err)
	// 		return "", err
	// 	}

	// 	am.app.DoSaleItem(auctionItem.AuctionItemUUID, 0, string(extraInfo), true, nil)
	// }

	return "", nil
}

func (am *AuctionMgr) setGmTimer(timerName string, timer interface{}) {
	am.gmTimerLock.Lock()
	defer am.gmTimerLock.Unlock()
	am.gmTimerMap[timerName] = timer
}

func (am *AuctionMgr) cancelGmTimer(timerName string) {
	am.gmTimerLock.Lock()
	defer am.gmTimerLock.Unlock()
	if v, ok := am.gmTimerMap[timerName]; ok {
		switch t := v.(type) {
		case *time.Ticker:
			t.Stop()
		case *time.Timer:
			t.Stop()
		case chan struct{}:
			t <- struct{}{}
		}
	}
	am.gmTimerMap[timerName] = nil
}

func (am *AuctionMgr) setItemExpired(auctionItemUUID uint64) {
	auctionItem, err := am.GetAuctionItem(auctionItemUUID)
	if err != nil {
		appLog.Errorw("setItemExpired: GetAuctionItem err", "err", err)
		return
	}
	am.setStatus(AUCTION_STATUS_EXPIRED, auctionItem, false)

	auctionItemUUIDStr := strconv.FormatUint(auctionItemUUID, 10)
	if timer, ok := am.expiredTimerMap.Get(auctionItemUUIDStr); ok {
		if timer != nil {
			timer.Stop()
		}
		am.expiredTimerMap.Remove(auctionItemUUIDStr)
	}
}

func (am *AuctionMgr) setItemSelling(auctionItemUUID uint64, isBroadCast bool) {
	auctionItem, err := am.GetAuctionItem(auctionItemUUID)
	if err != nil {
		appLog.Errorw("setItemSelling: GetAuctionItem err", "err", err)
		return
	}

	// === 2026-09-21 v3 抢购迁移:挂抽签调度 (0 秒 timer,公示期结束立即异步抽签) ===

	bucket, participateCount := am.popSnatchBucket(auctionItem)
	if nil != bucket && participateCount > 0 {
		if bucket.OpenTimer != nil {
			bucket.OpenTimer.Stop()
		}
		bucket.OpenTimer = time.AfterFunc(0, func() { am.openSnatch(auctionItemUUID, bucket) })
		return
	}

	// 置成出售状态
	am.setStatus(AUCTION_STATUS_SELLING, auctionItem, false)
	// 移除公示结束定时器
	auctionItemUUIDStr := strconv.FormatUint(auctionItemUUID, 10)
	if timer, ok := am.endPublicityTimerMap.Get(auctionItemUUIDStr); ok {
		if timer != nil {
			timer.Stop()
		}
		am.endPublicityTimerMap.Remove(auctionItemUUIDStr)
	}
	// 挂出售过期定时器
	curTime := time.Now().Unix()
	duration := auctionItem.itemExpiredTime() - curTime
	timer := time.AfterFunc(time.Duration(duration)*time.Second, func() {
		am.setItemExpired(auctionItemUUID)
	})
	am.expiredTimerMap.Set(auctionItemUUIDStr, timer)
	// 推送公示结束消息到交易频道（全量推送，频率由GameServerService限流）
	if isBroadCast {
		auctionOnSaleChattingCfg, ret := ConfigStore.cfgVipers.Get(CFG_TYPE_AUCTION_ONSALECHATTING)
		if !ret || nil == auctionOnSaleChattingCfg {
			appLog.Error("setItemSelling missing cfg store ", CFG_TYPE_AUCTION_ONSALECHATTING)
			return
		}
		flag := auctionOnSaleChattingCfg.GetInt(strconv.FormatUint(uint64(auctionItem.ItemData.ItemId), 10))
		if flag == 1 {
			go am.app.broadcastOnItemSaling(auctionItemUUID, auctionItem.ItemData.ItemId, auctionItem.FromPlayerGBID)
		}
	}
}

// openSnatch 抽签:v3 行为 —
//   - 无人:物品继续按 SELLING 正常卖,不需要 winner
//   - 有人:按 Σ snatchWeight 加权随机选 winner,winner 走 executeSnatchWinnerDoBuyItem 发物品;其余参与者走 notifySnatchRefund 退款
//
// 加权抽样算法: 总权重 totalWeight = Σ rec.SnatchWeight(2026-10-08 之前的老桶记录里 SnatchWeight 默认为 0,
// 函数开头兜底为 DEFAULT_SNATCH_WEIGHT 1000,保持和老逻辑的等概率语义)
// 取 rand ∈ [0, totalWeight),按 Records 顺序累计,首个累计 ≥ rand 的就是 winner.
// 时间复杂度 O(n),Records map 顺序本来就不确定,语义上等价于"按权重加权后随机抽样".
func (am *AuctionMgr) openSnatch(auctionItemUUID uint64, bucket *SnatchBucket) {
	if bucket == nil {
		appLog.Warnw("openSnatch: bucket missing", "uuid", auctionItemUUID)
		return
	}
	bucket.mu.Lock()
	defer bucket.mu.Unlock()
	if bucket.Opened {

		return
	}
	bucket.Opened = true

	if len(bucket.Records) == 0 {
		appLog.Infow("openSnatch: no participants, item stays SELLING", "uuid", auctionItemUUID)
		return
	}

	// === 2026-10-08 按权重加权抽样 ===
	// 1) 计算总权重 + 给老记录(无 SnatchWeight)兜底
	var totalWeight uint64 = 0
	weights := make(map[uint64]uint64, len(bucket.Records))
	for gbID, rec := range bucket.Records {
		w := uint64(rec.SnatchWeight)
		weights[gbID] = w
		totalWeight += w
	}

	// 2) 防御:totalWeight 应该 >0,否则退化为随机等概率抽样
	if totalWeight == 0 {
		appLog.Warnw("openSnatch: totalWeight==0, fall back to uniform random", "uuid", auctionItemUUID)
		gbs := make([]uint64, 0, len(bucket.Records))
		for gbID := range bucket.Records {
			gbs = append(gbs, gbID)
		}
		bucket.WinnerGBID = gbs[rand.Intn(len(gbs))]
	} else {
		// 3) 抽 [0, totalWeight) 区间随机点,按顺序累计求 winner
		pickPoint := rand.Uint64() % totalWeight
		var accWeight uint64 = 0
		var winnerGBID uint64
		var winnerWeight uint64
		for gbID, w := range weights {
			accWeight += w
			if accWeight >= pickPoint {
				winnerGBID = gbID
				winnerWeight = w
				break
			}
		}
		bucket.WinnerGBID = winnerGBID
		appLog.Infow("openSnatch: weighted draw", "uuid", auctionItemUUID,
			"winner", winnerGBID, "winnerWeight", winnerWeight,
			"totalWeight", totalWeight, "participants", len(bucket.Records),
			"pickPoint", pickPoint)
	}

	winnerGBID := bucket.WinnerGBID
	rec := bucket.Records[winnerGBID]

	auctionItem, err := am.GetAuctionItem(auctionItemUUID)
	if err != nil {
		appLog.Errorw("openSnatch: GetAuctionItem err", "err", err, "uuid", auctionItemUUID)
		return
	}

	// winner 走完整成交路径 (doBuyItem + 发物品 + 通知卖家)
	if err := am.app.executeSnatchWinnerDoBuyItem(auctionItem, winnerGBID, rec); err != nil {
		appLog.Errorw("openSnatch: winner doBuyItem failed", "err", err,
			"uuid", auctionItemUUID, "winner", winnerGBID)
	}

	// 其余参与者退款 (异步,不阻塞)
	go am.notifySnatchRefund(bucket)
}

// notifySnatchRefund 把 winner 之外的参与者通过 SnatchRefundReq RPC 推到 game server
// 当前实现:单一来源服推送 (auctionItem.ServerId);跨服玩家通过 game server 端按 playerGBID 路由
func (am *AuctionMgr) notifySnatchRefund(bucket *SnatchBucket) {
	if am.app == nil {
		appLog.Errorw("notifySnatchRefund: app nil", "uuid", bucket.AuctionItemUUID)
		return
	}
	bucket.mu.Lock()
	defer bucket.mu.Unlock()
	for gbID, rec := range bucket.Records {
		if gbID == bucket.WinnerGBID {
			continue
		}

		req := &gameServerService.SnatchRefundReq{
			AuctionItemUUID: bucket.AuctionItemUUID,
			ItemId:          bucket.ItemId,
			Price:           bucket.Price,
			Number:          bucket.Number,
			PlayerGBID:      gbID,
			OpUUID:          rec.OpUUID,
			Reason:          uint32(SnatchReasonNotLucky),
			PublicEndTime:   bucket.PublicityEndTime,
		}
		gs := am.app.GetGameServer(rec.ServerId, 0)
		if gs == nil {
			appLog.Errorw("notifySnatchRefund: gameServer is nil",
				"uuid", bucket.AuctionItemUUID, "serverId", rec.ServerId)
			return
		}
		gss, ok := gs.AuctionService.(*GameServerService)
		if !ok {
			appLog.Errorw("notifySnatchRefund: cast AuctionService failed", "serverId", rec.ServerId)
			return
		}
		if _, err := gss.GetClientEndPoint().(*gameServerService.GameServerClient).ReplySnatchRefund(req); err != nil {
			appLog.Errorw("notifySnatchRefund: RPC failed",
				"err", err, "uuid", bucket.AuctionItemUUID, "serverId", rec.ServerId)
			return
		}
		appLog.Infow("notifySnatchRefund: dispatched", "uuid", bucket.AuctionItemUUID, "serverId", rec.ServerId)
	}
}

func (am *AuctionMgr) gmBuyAuctionItem(itemId uint32, buyNum uint32, price uint64, startTime uint32) (string, uint32, error) {
	realBuyNum := buyNum
	curTime := time.Now().Unix()
	if curTime < int64(startTime) {
		appLog.Errorw("gmBuyAuctionItem: time err", "now", curTime, "startTime", startTime)
		return "", 0, nil
	}

	auctionItemUUIDs, remainNum, totalPrice, err := am.app.buyItemByItemId(0, itemId, buyNum, uint32(price))
	if err != nil {
		appLog.Errorw("gmBuyAuctionItem: buyItemByItemId err", "err", err)
		return "", 0, err
	}

	m := make(map[string]interface{})
	m["auctionBuyItemId"] = itemId
	m["auctionBuyItemNum"] = buyNum
	tlogProps := make(map[string]interface{})
	tlogProps["role_name"] = "GM"
	m["tlogProps"] = tlogProps
	extraB, err := json.Marshal(m)
	if err != nil {
		appLog.Errorw("gmBuyAuctionItem: Marshal err", "err", err)
		return "", 0, err
	}

	_, _, err = am.app.doBuyItemByItemId(0, AUCTION_OK, itemId, buyNum, uint32(price), remainNum, auctionItemUUIDs, totalPrice, string(extraB))
	if err != nil {
		appLog.Errorw("gmBuyAuctionItem: doBuyItemByItemId err", "err", err)
		return "", 0, err
	}

	realBuyNum = buyNum - remainNum
	return "", realBuyNum, nil
}

func (am *AuctionMgr) addAuctionBlackList(playerGbId uint64) {
	if playerGbId == 0 {
		return
	}

	am.blackListLock.Lock()
	defer am.blackListLock.Unlock()
	for _, v := range am.blackList {
		if v == playerGbId {
			return
		}
	}

	am.blackList = append(am.blackList, playerGbId)
	err := am.insertBlackListToDB(playerGbId)
	if err != nil {
		return
	}
}

func (am *AuctionMgr) insertBlackListToDB(playerGbId uint64) error {
	stmt, err := am.db.Prepare("INSERT INTO auction_blackList (playerGBID) VALUES (?)")
	if err != nil {
		appLog.Errorw("insertBlackListToDB: Prepare err", "err", err, "playerGbId", playerGbId)
		return err
	}

	defer stmt.Close()

	_, err = stmt.Exec(playerGbId)
	if err != nil {
		appLog.Errorw("insertBlackListToDB: Exec err", "err", err, "playerGbId", playerGbId)
		return nil
	}

	return nil
}

func (am *AuctionMgr) removeAuctionBlackList(playerGbId uint64) {
	if playerGbId == 0 {
		return
	}

	am.blackListLock.Lock()
	defer am.blackListLock.Unlock()
	for i, v := range am.blackList {
		if v == playerGbId {
			am.blackList = append(am.blackList[:i], am.blackList[i+1:]...)
			break
		}
	}

	err := am.deleteBlackListFromDB(playerGbId)
	if err != nil {
		appLog.Errorw("removeAuctionBlackList: deleteBlackListFromDB err", "err", err, "playerGbId", playerGbId)
	}
}

func (am *AuctionMgr) deleteBlackListFromDB(playerGbId uint64) error {
	stmt, err := am.db.Prepare("DELETE FROM `auction_blackList` WHERE `playerGBID` = ?")
	if err != nil {
		appLog.Errorw("deleteBlackListFromDB: Prepare err", "err", err, "playerGbId", playerGbId)
		return err
	}

	defer stmt.Close()

	_, err = stmt.Exec(playerGbId)
	if err != nil {
		appLog.Errorw("deleteBlackListFromDB: Exec err", "err", err, "playerGbId", playerGbId)
		return err
	}

	return nil
}

func (am *AuctionMgr) checkIsInBlackList(playerGbId uint64) bool {
	if playerGbId == 0 {
		return false
	}

	am.blackListLock.RLock()
	defer am.blackListLock.RUnlock()
	for _, v := range am.blackList {
		if v == playerGbId {
			return true
		}
	}

	return false
}
