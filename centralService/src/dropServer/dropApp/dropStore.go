package DropApp

import (
	"centralService/src/appLog"
	"centralService/src/common"
	"database/sql"
	"fmt"
	"strings"
	"sync"
)

// === 内存结构体 (与 mysql 表字段一对一) ===

// DropInfoRecord 对应 drop_info 表
type DropInfoRecord struct {
	Id             int64 // 2026-10-14 加 AUTO_INCREMENT id 列, 用于 keyset 分页加载 (替代 OFFSET)
	ServerId       uint32
	UniqueId       uint64
	DropGbId       uint64
	DropType       uint32
	EndTime        int64
	EquipInfo      []byte
	DropTime       int64
	TakerGbId      uint64
	TakerServerId  uint32
	CollExpireTime int64
	Price          uint32
	MaxPrice       uint32
	ExtraInfo      []byte
	GiveUpTime     int64
	CollectionId   uint32
	RedeemWaitTime int64
	HasRedeemPrice uint32
	HasPayment     uint32
	ReturnTime     int64
	OwnerGbId      uint64
	OwnerServerId  uint32
	ReturnTimeBack int64
}

// CustodyInfoRecord 对应 custody_info 表
type CustodyInfoRecord struct {
	Id             int64
	UniqueId       uint64
	DropType       uint32
	EquipInfo      []byte
	HolderGbId     uint64
	HolderServerId uint32
	ReturnTime     int64
	OwnerGbId      uint64
	OwnerServerId  uint32
}

// RewardInfoRecord 对应 reward_info 表
type RewardInfoRecord struct {
	Id        int64
	UniqueId  uint64
	GbId      uint64
	ServerId  uint32
	BindMoney uint32
	Money     uint32
	EquipInfo []byte
}

// === dropStore: cache-aside + write-through ===

// dropStore 三表内存仓库.
//   - 读: 先内存, miss 回退 mysql 并回填内存 (cache-aside).
//   - 写: 内存 + mysql 同步双写 (write-through). mysql 是 source of truth.
//   - 启动: 从 mysql 加载到内存 (恢复完整, 不会丢最近几分钟的数据).
type dropStore struct {
	db *sql.DB

	// drop_info (主键 uniqueId)
	dropMu      sync.RWMutex
	dropByUid   map[uint64]*DropInfoRecord
	dropByDrop  map[uint64]map[uint64]*DropInfoRecord // dropGbId -> {uniqueId -> rec}
	dropByTaker map[uint64]map[uint64]*DropInfoRecord // takerGbId -> {uniqueId -> rec}

	// custody_info (主键 uniqueId)
	custodyMu      sync.RWMutex
	custodyByUid   map[uint64]*CustodyInfoRecord
	custodyByOwner map[uint64]map[uint64]*CustodyInfoRecord // ownerGbId -> {uniqueId -> rec}

	// reward_info (主键 uniqueId, 副索引 gbId)
	rewardMu     sync.RWMutex
	rewardByUid  map[uint64]*RewardInfoRecord
	rewardByGbId map[uint64]map[uint64]*RewardInfoRecord // gbId -> {uniqueId -> rec}
}

func newDropStore(db *sql.DB) *dropStore {
	return &dropStore{
		db:             db,
		dropByUid:      make(map[uint64]*DropInfoRecord),
		dropByDrop:     make(map[uint64]map[uint64]*DropInfoRecord),
		dropByTaker:    make(map[uint64]map[uint64]*DropInfoRecord),
		custodyByUid:   make(map[uint64]*CustodyInfoRecord),
		custodyByOwner: make(map[uint64]map[uint64]*CustodyInfoRecord),
		rewardByUid:    make(map[uint64]*RewardInfoRecord),
		rewardByGbId:   make(map[uint64]map[uint64]*RewardInfoRecord),
	}
}

// ----- index helpers -----

func (s *dropStore) addDropIndex(rec *DropInfoRecord) {
	if rec.DropGbId != 0 {
		m, ok := s.dropByDrop[rec.DropGbId]
		if !ok {
			m = make(map[uint64]*DropInfoRecord)
			s.dropByDrop[rec.DropGbId] = m
		}
		m[rec.UniqueId] = rec
	}
	if rec.TakerGbId != 0 {
		m, ok := s.dropByTaker[rec.TakerGbId]
		if !ok {
			m = make(map[uint64]*DropInfoRecord)
			s.dropByTaker[rec.TakerGbId] = m
		}
		m[rec.UniqueId] = rec
	}
}

func (s *dropStore) removeDropIndex(rec *DropInfoRecord) {
	if rec.DropGbId != 0 {
		if m, ok := s.dropByDrop[rec.DropGbId]; ok {
			delete(m, rec.UniqueId)
			if len(m) == 0 {
				delete(s.dropByDrop, rec.DropGbId)
			}
		}
	}
	if rec.TakerGbId != 0 {
		if m, ok := s.dropByTaker[rec.TakerGbId]; ok {
			delete(m, rec.UniqueId)
			if len(m) == 0 {
				delete(s.dropByTaker, rec.TakerGbId)
			}
		}
	}
}

func (s *dropStore) addCustodyIndex(rec *CustodyInfoRecord) {
	if rec.OwnerGbId != 0 {
		m, ok := s.custodyByOwner[rec.OwnerGbId]
		if !ok {
			m = make(map[uint64]*CustodyInfoRecord)
			s.custodyByOwner[rec.OwnerGbId] = m
		}
		m[rec.UniqueId] = rec
	}
}

func (s *dropStore) removeCustodyIndex(rec *CustodyInfoRecord) {
	if rec.OwnerGbId != 0 {
		if m, ok := s.custodyByOwner[rec.OwnerGbId]; ok {
			delete(m, rec.UniqueId)
			if len(m) == 0 {
				delete(s.custodyByOwner, rec.OwnerGbId)
			}
		}
	}
}

func (s *dropStore) addRewardIndex(rec *RewardInfoRecord) {
	if rec.GbId != 0 {
		m, ok := s.rewardByGbId[rec.GbId]
		if !ok {
			m = make(map[uint64]*RewardInfoRecord)
			s.rewardByGbId[rec.GbId] = m
		}
		m[rec.UniqueId] = rec
	}
}

func (s *dropStore) removeRewardIndex(rec *RewardInfoRecord) {
	if rec.GbId != 0 {
		if m, ok := s.rewardByGbId[rec.GbId]; ok {
			delete(m, rec.UniqueId)
			if len(m) == 0 {
				delete(s.rewardByGbId, rec.GbId)
			}
		}
	}
}

// ----- Load from MySQL at boot -----

// LoadFromMySQL dropServer 启动时从 mysql 加载全部活跃数据到内存.
// 装载策略: 全量加载三表, 内存上限可接受 (22字段 * ~100w 行 ≈ 100MB).
func (s *dropStore) LoadFromMySQL() error {
	if err := s.loadDropInfos(); err != nil {
		return fmt.Errorf("loadDropInfos err: %w", err)
	}
	if err := s.loadCustodyInfos(); err != nil {
		return fmt.Errorf("loadCustodyInfos err: %w", err)
	}
	if err := s.loadRewardInfos(); err != nil {
		return fmt.Errorf("loadRewardInfos err: %w", err)
	}
	return nil
}

// loadBatchSize 启动加载每批行数 (避免单次查询结果集过大)
const loadBatchSize = 1000

func (s *dropStore) loadDropInfos() error {
	// 2026-10-14 keyset 分批加载: 每次 WHERE id > lastId ORDER BY id LIMIT 1000.
	// 性能: 索引 seek (O(log n)) + 顺序 scan (O(batch)), 与翻页深度无关. 优于 OFFSET.
	// 假设: 启动期间停服, 无新写入. 若改热启动需评估漏读风险.
	s.dropMu.Lock()
	defer s.dropMu.Unlock()

	const selectFields = `id, serverId, uniqueId, dropGbId, dropType, endTime, equipInfo, dropTime, takerGbId, takerServerId,
		       collExpireTime, price, maxPrice, extraInfo, giveUpTime, collectionId, redeemWaitTime,
		       hasRedeemPrice, hasPayment, returnTime, ownerGbId, ownerServerId, returnTimeBack`
	query := fmt.Sprintf("SELECT %s FROM drop_info WHERE id > ? ORDER BY id LIMIT ?", selectFields)

	count := 0
	lastId := int64(0)
	for {
		rows, err := s.db.Query(query, lastId, loadBatchSize)
		if err != nil {
			return err
		}
		batchCount := 0
		var maxId int64
		for rows.Next() {
			rec := &DropInfoRecord{}
			if err := rows.Scan(
				&rec.Id, &rec.ServerId, &rec.UniqueId, &rec.DropGbId, &rec.DropType, &rec.EndTime, &rec.EquipInfo,
				&rec.DropTime, &rec.TakerGbId, &rec.TakerServerId, &rec.CollExpireTime, &rec.Price,
				&rec.MaxPrice, &rec.ExtraInfo, &rec.GiveUpTime, &rec.CollectionId, &rec.RedeemWaitTime,
				&rec.HasRedeemPrice, &rec.HasPayment, &rec.ReturnTime, &rec.OwnerGbId,
				&rec.OwnerServerId, &rec.ReturnTimeBack,
			); err != nil {
				rows.Close()
				return err
			}

			rec.ServerId = common.GetGameServerMergeRoot(rec.ServerId)
			rec.TakerServerId = common.GetGameServerMergeRoot(rec.TakerServerId)
			rec.OwnerServerId = common.GetGameServerMergeRoot(rec.OwnerServerId)

			s.dropByUid[rec.UniqueId] = rec
			s.addDropIndex(rec)
			if rec.Id > maxId {
				maxId = rec.Id
			}
			batchCount++
		}
		rows.Close()
		count += batchCount
		lastId = maxId
		if batchCount < loadBatchSize {
			break
		}
	}
	appLog.Infof("dropStore.loadDropInfos loaded %d rows (batch=%d, keyset=id)", count, loadBatchSize)
	return nil
}

func (s *dropStore) loadCustodyInfos() error {
	// 2026-10-14 keyset 分批加载: 每次 WHERE id > lastId ORDER BY id LIMIT 1000
	s.custodyMu.Lock()
	defer s.custodyMu.Unlock()

	const selectFields = `id, uniqueId, dropType, equipInfo, holderGbId, holderServerId, returnTime, ownerGbId, ownerServerId`
	query := fmt.Sprintf("SELECT %s FROM custody_info WHERE id > ? ORDER BY id LIMIT ?", selectFields)

	count := 0
	lastId := int64(0)
	for {
		rows, err := s.db.Query(query, lastId, loadBatchSize)
		if err != nil {
			return err
		}
		batchCount := 0
		var maxId int64
		for rows.Next() {
			rec := &CustodyInfoRecord{}
			if err := rows.Scan(
				&rec.Id, &rec.UniqueId, &rec.DropType, &rec.EquipInfo, &rec.HolderGbId, &rec.HolderServerId,
				&rec.ReturnTime, &rec.OwnerGbId, &rec.OwnerServerId,
			); err != nil {
				rows.Close()
				return err
			}
			rec.HolderServerId = common.GetGameServerMergeRoot(rec.HolderServerId)
			rec.OwnerServerId = common.GetGameServerMergeRoot(rec.OwnerServerId)
			s.custodyByUid[rec.UniqueId] = rec
			s.addCustodyIndex(rec)
			if rec.Id > maxId {
				maxId = rec.Id
			}
			batchCount++
		}
		rows.Close()
		count += batchCount
		lastId = maxId
		if batchCount < loadBatchSize {
			break
		}
	}
	appLog.Infof("dropStore.loadCustodyInfos loaded %d rows (batch=%d, keyset=id)", count, loadBatchSize)
	return nil
}

func (s *dropStore) loadRewardInfos() error {
	// 2026-10-14 keyset 分批加载: 每次 WHERE id > lastId ORDER BY id LIMIT 1000
	s.rewardMu.Lock()
	defer s.rewardMu.Unlock()

	const selectFields = `id, uniqueId, gbId, serverId, bindMoney, money, equipInfo`
	query := fmt.Sprintf("SELECT %s FROM reward_info WHERE id > ? ORDER BY id LIMIT ?", selectFields)

	count := 0
	lastId := int64(0)
	for {
		rows, err := s.db.Query(query, lastId, loadBatchSize)
		if err != nil {
			return err
		}
		batchCount := 0
		var maxId int64
		for rows.Next() {
			rec := &RewardInfoRecord{}
			if err := rows.Scan(
				&rec.Id, &rec.UniqueId, &rec.GbId, &rec.ServerId, &rec.BindMoney, &rec.Money, &rec.EquipInfo,
			); err != nil {
				rows.Close()
				return err
			}
			rec.ServerId = common.GetGameServerMergeRoot(rec.ServerId)
			s.rewardByUid[rec.UniqueId] = rec
			s.addRewardIndex(rec)
			if rec.Id > maxId {
				maxId = rec.Id
			}
			batchCount++
		}
		rows.Close()
		count += batchCount
		lastId = maxId
		if batchCount < loadBatchSize {
			break
		}
	}
	appLog.Infof("dropStore.loadRewardInfos loaded %d rows (batch=%d, keyset=id)", count, loadBatchSize)
	return nil
}

// =========================================================================
// drop_info DAO
// =========================================================================

// InsertDropInfo 落库 + 写内存 (write-through). mysql 失败会让函数返回 error, 调用方决定要不要回滚内存.
func (s *dropStore) InsertDropInfo(rec *DropInfoRecord) error {
	_, err := s.db.Exec(`INSERT INTO drop_info
		(serverId, uniqueId, dropGbId, dropType, endTime, equipInfo, dropTime, takerGbId, takerServerId,
		 collExpireTime, price, maxPrice, extraInfo, giveUpTime, collectionId, redeemWaitTime,
		 hasRedeemPrice, hasPayment, returnTime, ownerGbId, ownerServerId, returnTimeBack)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
		rec.ServerId, rec.UniqueId, rec.DropGbId, rec.DropType, rec.EndTime, rec.EquipInfo, rec.DropTime,
		rec.TakerGbId, rec.TakerServerId, rec.CollExpireTime, rec.Price, rec.MaxPrice, rec.ExtraInfo,
		rec.GiveUpTime, rec.CollectionId, rec.RedeemWaitTime, rec.HasRedeemPrice, rec.HasPayment,
		rec.ReturnTime, rec.OwnerGbId, rec.OwnerServerId, rec.ReturnTimeBack)
	if err != nil {
		return err
	}

	s.dropMu.Lock()
	defer s.dropMu.Unlock()
	if old, ok := s.dropByUid[rec.UniqueId]; ok {
		s.removeDropIndex(old)
	}
	cp := *rec
	s.dropByUid[rec.UniqueId] = &cp
	s.addDropIndex(&cp)
	return nil
}

// UpdateDropInfo 整行替换, 同时写 mysql + 内存. 期望 rec.UniqueId 已在内存.
func (s *dropStore) UpdateDropInfo(rec *DropInfoRecord) error {
	_, err := s.db.Exec(`UPDATE drop_info SET
		serverId=?, dropGbId=?, dropType=?, endTime=?, equipInfo=?, dropTime=?, takerGbId=?, takerServerId=?,
		collExpireTime=?, price=?, maxPrice=?, extraInfo=?, giveUpTime=?, collectionId=?, redeemWaitTime=?,
		hasRedeemPrice=?, hasPayment=?, returnTime=?, ownerGbId=?, ownerServerId=?, returnTimeBack=?
		WHERE uniqueId=?`,
		rec.ServerId, rec.DropGbId, rec.DropType, rec.EndTime, rec.EquipInfo, rec.DropTime,
		rec.TakerGbId, rec.TakerServerId, rec.CollExpireTime, rec.Price, rec.MaxPrice, rec.ExtraInfo,
		rec.GiveUpTime, rec.CollectionId, rec.RedeemWaitTime, rec.HasRedeemPrice, rec.HasPayment,
		rec.ReturnTime, rec.OwnerGbId, rec.OwnerServerId, rec.ReturnTimeBack, rec.UniqueId)
	if err != nil {
		return err
	}

	s.dropMu.Lock()
	defer s.dropMu.Unlock()
	old, ok := s.dropByUid[rec.UniqueId]
	if ok {
		s.removeDropIndex(old)
	}
	cp := *rec
	s.dropByUid[rec.UniqueId] = &cp
	s.addDropIndex(&cp)
	return nil
}

// ConditionalUpdateDropDropType 条件 update: 当 dropType==expect 才改, 防并发.
func (s *dropStore) ConditionalUpdateDropDropType(uniqueId uint64, expectDropType uint32, newDropType uint32) (bool, error) {
	res, err := s.db.Exec(`UPDATE drop_info SET dropType=? WHERE uniqueId=? AND dropType=?`,
		newDropType, uniqueId, expectDropType)
	if err != nil {
		return false, err
	}
	rows, _ := res.RowsAffected()
	if rows == 0 {
		return false, nil
	}

	s.dropMu.Lock()
	defer s.dropMu.Unlock()
	if rec, ok := s.dropByUid[uniqueId]; ok {
		rec.DropType = newDropType
	}
	return true, nil
}

// UpdateDropDropTypeAndReturnTime 给 checkRedeemExpire 用 (dropType + returnTime 同时改)
func (s *dropStore) UpdateDropDropTypeAndReturnTime(uniqueId uint64, newDropType uint32, returnTime int64) error {
	_, err := s.db.Exec(`UPDATE drop_info SET dropType=?, returnTime=? WHERE uniqueId=?`,
		newDropType, returnTime, uniqueId)
	if err != nil {
		return err
	}
	s.dropMu.Lock()
	defer s.dropMu.Unlock()
	if rec, ok := s.dropByUid[uniqueId]; ok {
		rec.DropType = newDropType
		rec.ReturnTime = returnTime
	}
	return nil
}

// UpdateTakerFields _otherTake 用 (takerGbId, takerServerId, dropType, redeemWaitTime)
func (s *dropStore) UpdateTakerFields(uniqueId uint64, takerGbId uint64, takerServerId uint32, newDropType uint32, redeemWaitTime int64) (bool, error) {
	res, err := s.db.Exec(`UPDATE drop_info SET takerGbId=?, takerServerId=?, dropType=?, redeemWaitTime=? WHERE uniqueId=? AND dropType=?`,
		takerGbId, takerServerId, newDropType, redeemWaitTime, uniqueId, TYPE_DROP)
	if err != nil {
		return false, err
	}
	rows, _ := res.RowsAffected()
	if rows == 0 {
		return false, nil
	}
	s.dropMu.Lock()
	defer s.dropMu.Unlock()
	if rec, ok := s.dropByUid[uniqueId]; ok {
		s.removeDropIndex(rec)
		rec.TakerGbId = takerGbId
		rec.TakerServerId = takerServerId
		rec.DropType = newDropType
		rec.RedeemWaitTime = redeemWaitTime
		s.addDropIndex(rec)
	}
	return true, nil
}

// UpdateCollExpireTime UpdateCollEndTime 用
func (s *dropStore) UpdateCollExpireTime(uniqueId uint64, collEndTime int64) error {
	_, err := s.db.Exec(`UPDATE drop_info SET collExpireTime=? WHERE uniqueId=?`, collEndTime, uniqueId)
	if err != nil {
		return err
	}
	s.dropMu.Lock()
	defer s.dropMu.Unlock()
	if rec, ok := s.dropByUid[uniqueId]; ok {
		rec.CollExpireTime = collEndTime
	}
	return nil
}

// UpdateDropPrice SetTakeEquipRedeemPrice 用 (price, hasRedeemPrice, only when dropType=TYPE_TAKE)
func (s *dropStore) UpdateDropPrice(uniqueId uint64, price uint32, newDropType uint32) (bool, error) {
	res, err := s.db.Exec(`UPDATE drop_info SET price=?, hasRedeemPrice=? WHERE uniqueId=? AND dropType=?`,
		price, 1, uniqueId, newDropType)
	if err != nil {
		return false, err
	}
	rows, _ := res.RowsAffected()
	if rows == 0 {
		return false, nil
	}
	s.dropMu.Lock()
	defer s.dropMu.Unlock()
	if rec, ok := s.dropByUid[uniqueId]; ok {
		rec.Price = price
		rec.HasRedeemPrice = 1
	}
	return true, nil
}

// DeleteDropInfo 物理删除 (只用于 expire 真正的清理)
func (s *dropStore) DeleteDropInfo(uniqueId uint64) error {
	_, err := s.db.Exec(`DELETE FROM drop_info WHERE uniqueId=?`, uniqueId)
	if err != nil {
		return err
	}
	s.dropMu.Lock()
	defer s.dropMu.Unlock()
	if rec, ok := s.dropByUid[uniqueId]; ok {
		s.removeDropIndex(rec)
		delete(s.dropByUid, uniqueId)
	}
	return nil
}

// DeleteDropInfos 批量删除 (CheckDropReturnExpire 用)
func (s *dropStore) DeleteDropInfos(uniqueIds []uint64) error {
	if len(uniqueIds) == 0 {
		return nil
	}
	placeholders := strings.Repeat(",?", len(uniqueIds))[1:]
	query := fmt.Sprintf("DELETE FROM drop_info WHERE uniqueId IN (%s)", placeholders)
	args := make([]interface{}, 0, len(uniqueIds))
	for _, id := range uniqueIds {
		args = append(args, id)
	}
	if _, err := s.db.Exec(query, args...); err != nil {
		return err
	}

	s.dropMu.Lock()
	defer s.dropMu.Unlock()
	for _, id := range uniqueIds {
		if rec, ok := s.dropByUid[id]; ok {
			s.removeDropIndex(rec)
			delete(s.dropByUid, id)
		}
	}
	return nil
}

// FindExpiringCustodyReturns CheckDropReturnExpire 用:
// 找 ownerServerId == serverId AND dropType == TYPE_RETURN_WAIT AND returnTime < limitTime 的 record
func (s *dropStore) FindExpiringCustodyReturns(serverId uint32, limitTime int64, limit int) []*CustodyInfoRecord {
	s.custodyMu.RLock()
	defer s.custodyMu.RUnlock()
	out := make([]*CustodyInfoRecord, 0)
	for _, rec := range s.custodyByUid {
		if rec.DropType != TYPE_RETURN_WAIT {
			continue
		}
		if rec.OwnerServerId != serverId {
			continue
		}
		if rec.ReturnTime >= limitTime {
			continue
		}
		cp := *rec
		out = append(out, &cp)
		if len(out) >= limit {
			break
		}
	}
	return out
}

// BatchUpdateCustodyDropType 批量更新 custody_info.dropType (CheckDropReturnExpire 用, 改 TYPE_RETURN_WAIT -> TYPE_RETURN_GET)
func (s *dropStore) BatchUpdateCustodyDropType(uniqueIds []uint64, newDropType uint32) error {
	if len(uniqueIds) == 0 {
		return nil
	}
	placeholders := strings.Repeat(",?", len(uniqueIds))[1:]
	query := fmt.Sprintf("UPDATE custody_info SET dropType=? WHERE uniqueId IN (%s)", placeholders)
	args := make([]interface{}, 0, len(uniqueIds)+1)
	args = append(args, newDropType)
	for _, id := range uniqueIds {
		args = append(args, id)
	}
	if _, err := s.db.Exec(query, args...); err != nil {
		return err
	}

	s.custodyMu.Lock()
	defer s.custodyMu.Unlock()
	for _, id := range uniqueIds {
		if rec, ok := s.custodyByUid[id]; ok {
			s.removeCustodyIndex(rec)
			rec.DropType = newDropType
			s.addCustodyIndex(rec)
		}
	}
	return nil
}

// GetDropInfoByUniqueId 直接命中内存
func (s *dropStore) GetDropInfoByUniqueId(uniqueId uint64) *DropInfoRecord {
	s.dropMu.RLock()
	defer s.dropMu.RUnlock()
	if rec, ok := s.dropByUid[uniqueId]; ok {
		cp := *rec
		return &cp
	}
	return nil
}

// GetDropInfosByDropGbId GetDropInfo 的 dropInfo 部分
func (s *dropStore) GetDropInfosByDropGbId(gbId uint64) []*DropInfoRecord {
	s.dropMu.RLock()
	defer s.dropMu.RUnlock()
	m, ok := s.dropByDrop[gbId]
	if !ok {
		return nil
	}
	out := make([]*DropInfoRecord, 0, len(m))
	for _, rec := range m {
		cp := *rec
		out = append(out, &cp)
	}
	return out
}

// GetDropInfosByTakerGbId GetDropInfo 的 takerInfo 部分
func (s *dropStore) GetDropInfosByTakerGbId(gbId uint64) []*DropInfoRecord {
	s.dropMu.RLock()
	defer s.dropMu.RUnlock()
	m, ok := s.dropByTaker[gbId]
	if !ok {
		return nil
	}
	out := make([]*DropInfoRecord, 0, len(m))
	for _, rec := range m {
		cp := *rec
		out = append(out, &cp)
	}
	return out
}

// FindExpiredDrops 用于 checkDropExpire: dropType=TYPE_DROP AND endTime<limitTime
func (s *dropStore) FindExpiredDrops(limitTime int64, limit int) []*DropInfoRecord {
	s.dropMu.RLock()
	defer s.dropMu.RUnlock()
	out := make([]*DropInfoRecord, 0)
	for _, rec := range s.dropByUid {
		if rec.DropType != TYPE_DROP {
			continue
		}
		if rec.EndTime >= limitTime {
			continue
		}
		cp := *rec
		out = append(out, &cp)
		if len(out) >= limit {
			break
		}
	}
	return out
}

// FindExpiredRedeems 用于 checkRedeemExpire: dropType=TYPE_TAKE AND redeemWaitTime<limitTime
func (s *dropStore) FindExpiredRedeems(limitTime int64, limit int) []*DropInfoRecord {
	s.dropMu.RLock()
	defer s.dropMu.RUnlock()
	out := make([]*DropInfoRecord, 0)
	for _, rec := range s.dropByUid {
		if rec.DropType != TYPE_TAKE {
			continue
		}
		if rec.RedeemWaitTime >= limitTime {
			continue
		}
		cp := *rec
		out = append(out, &cp)
		if len(out) >= limit {
			break
		}
	}
	return out
}

// =========================================================================
// custody_info DAO
// =========================================================================

// UpsertCustodyHolder 兼容性: INSERT ... on duplicate key update holderGbId, holderServerId.
// 等价于原 `INSERT INTO custody_info (uniqueId, dropType, equipInfo, holderGbId, holderServerId, returnTime, ownerGbId, ownerServerId) VALUES (...) on duplicate key update holderGbId=?, holderServerId=?`.
func (s *dropStore) UpsertCustodyHolder(rec *CustodyInfoRecord) error {
	_, err := s.db.Exec(`INSERT INTO custody_info
		(uniqueId, dropType, equipInfo, holderGbId, holderServerId, returnTime, ownerGbId, ownerServerId)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?) on duplicate key update holderGbId=?, holderServerId=?`,
		rec.UniqueId, rec.DropType, rec.EquipInfo, rec.HolderGbId, rec.HolderServerId,
		rec.ReturnTime, rec.OwnerGbId, rec.OwnerServerId, rec.HolderGbId, rec.HolderServerId)
	if err != nil {
		return err
	}

	s.custodyMu.Lock()
	defer s.custodyMu.Unlock()
	old, ok := s.custodyByUid[rec.UniqueId]
	if ok {
		s.removeCustodyIndex(old)
	}
	cp := *rec
	s.custodyByUid[rec.UniqueId] = &cp
	s.addCustodyIndex(&cp)
	return nil
}

// UpdateCustodyHolderGiveUp 兼容原 `UPDATE custody_info SET holderGbId=?, holderServerId=? WHERE uniqueId=?`
func (s *dropStore) UpdateCustodyHolderGiveUp(uniqueId uint64, holderGbId uint64, holderServerId uint32) error {
	_, err := s.db.Exec(`UPDATE custody_info SET holderGbId=?, holderServerId=? WHERE uniqueId=?`,
		holderGbId, holderServerId, uniqueId)
	if err != nil {
		return err
	}
	s.custodyMu.Lock()
	defer s.custodyMu.Unlock()
	if rec, ok := s.custodyByUid[uniqueId]; ok {
		s.removeCustodyIndex(rec)
		rec.HolderGbId = holderGbId
		rec.HolderServerId = holderServerId
		s.addCustodyIndex(rec)
	}
	return nil
}

func (s *dropStore) GetCustodyInfoByUniqueId(uniqueId uint64) *CustodyInfoRecord {
	s.custodyMu.RLock()
	defer s.custodyMu.RUnlock()
	if rec, ok := s.custodyByUid[uniqueId]; ok {
		cp := *rec
		return &cp
	}
	return nil
}

func (s *dropStore) GetCustodyInfosByOwnerGbId(gbId uint64) []*CustodyInfoRecord {
	s.custodyMu.RLock()
	defer s.custodyMu.RUnlock()
	m, ok := s.custodyByOwner[gbId]
	if !ok {
		return nil
	}
	out := make([]*CustodyInfoRecord, 0, len(m))
	for _, rec := range m {
		cp := *rec
		out = append(out, &cp)
	}
	return out
}

// DeleteCustodyInfo GetBackEquip 用
func (s *dropStore) DeleteCustodyInfo(uniqueId uint64) error {
	_, err := s.db.Exec(`DELETE FROM custody_info WHERE uniqueId=?`, uniqueId)
	if err != nil {
		return err
	}
	s.custodyMu.Lock()
	defer s.custodyMu.Unlock()
	if rec, ok := s.custodyByUid[uniqueId]; ok {
		s.removeCustodyIndex(rec)
		delete(s.custodyByUid, uniqueId)
	}
	return nil
}

// =========================================================================
// reward_info DAO
// =========================================================================

// UpsertReward SetDropEquipPayPrice 用: 增量 bindMoney/money
// 返回更新后的 (bindMoney, money).
func (s *dropStore) UpsertReward(rec *RewardInfoRecord) error {
	_, err := s.db.Exec(`INSERT INTO reward_info
		(uniqueId, gbId, serverId, bindMoney, money, equipInfo)
		VALUES (?, ?, ?, ?, ?, ?) on duplicate key update bindMoney=?, money=?`,
		rec.UniqueId, rec.GbId, rec.ServerId, rec.BindMoney, rec.Money, rec.EquipInfo,
		rec.BindMoney, rec.Money)
	if err != nil {
		return err
	}

	s.rewardMu.Lock()
	defer s.rewardMu.Unlock()
	old, ok := s.rewardByUid[rec.UniqueId]
	if ok {
		s.removeRewardIndex(old)
	}
	cp := *rec
	s.rewardByUid[rec.UniqueId] = &cp
	s.addRewardIndex(&cp)
	return nil
}

func (s *dropStore) GetRewardByUniqueId(uniqueId uint64) *RewardInfoRecord {
	s.rewardMu.RLock()
	defer s.rewardMu.RUnlock()
	if rec, ok := s.rewardByUid[uniqueId]; ok {
		cp := *rec
		return &cp
	}
	return nil
}

func (s *dropStore) GetRewardListByGbId(gbId uint64) []*RewardInfoRecord {
	s.rewardMu.RLock()
	defer s.rewardMu.RUnlock()
	m, ok := s.rewardByGbId[gbId]
	if !ok {
		return nil
	}
	out := make([]*RewardInfoRecord, 0, len(m))
	for _, rec := range m {
		cp := *rec
		out = append(out, &cp)
	}
	return out
}

func (s *dropStore) DeleteRewardByUniqueId(uniqueId uint64) error {
	_, err := s.db.Exec(`DELETE FROM reward_info WHERE uniqueId=?`, uniqueId)
	if err != nil {
		return err
	}
	s.rewardMu.Lock()
	defer s.rewardMu.Unlock()
	if rec, ok := s.rewardByUid[uniqueId]; ok {
		s.removeRewardIndex(rec)
		delete(s.rewardByUid, uniqueId)
	}
	return nil
}
