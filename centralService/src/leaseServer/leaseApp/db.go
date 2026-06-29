package LeaseApp

import (
	"centralService/src/appLog"
	"fmt"
	"time"
)

func (lm *LeaseMgr) dbLoadItems(cb func(*LeaseMarketItem) error) error {
	const batchSize = 1000
	var lastId uint64
	for {
		rows, err := lm.db.Query(`SELECT id, unique_id, item_id, return_owner_gbid,
			return_owner_server_id, return_time, return_reason, lease_days, lessor_gbid,
			lessor_server_id, lessee_gbid, lessee_server_id, price_per_day, lease_start_time,
			lease_end_time, lease_cost, lease_gold, lease_bind_gold, lease_tax, item_data,
			lease_status, create_time FROM lease_market WHERE lease_status IN (?, ?) AND id > ? LIMIT ?`,
			LEASE_STATUS_ON_SALE, LEASE_STATUS_EXPIRED, lastId, batchSize)
		if err != nil {
			return err
		}

		count := 0
		for rows.Next() {
			item := &LeaseMarketItem{}
			var id uint64
			var createTime uint32
			err := rows.Scan(&id, &item.UniqueId, &item.ItemId, &item.ReturnOwnerGbId, &item.ReturnOwnerServerId,
				&item.ReturnEndTime, &item.ReturnReason, &item.LeaseDay,
				&item.LessorGbId, &item.LessorServerId, &item.LesseeGbId, &item.LesseeServerId,
				&item.PricePerDay, &item.LeaseStartTime, &item.LeaseEndTime,
				&item.LeaseCost, &item.LeaseGold, &item.LeaseBindGold, &item.LeaseTax,
				&item.ItemData, &item.Status, &createTime)
			if err != nil {
				appLog.Error("load lease_market row error:", err.Error())
				continue
			}
			item.AddTime = int64(createTime)
			if err := cb(item); err != nil {
				rows.Close()
				return err
			}
			lastId = id
			count++
		}
		rows.Close()

		if count < batchSize {
			break
		}
	}
	return nil
}

func (lm *LeaseMgr) dbAddItemCommit(item *LeaseMarketItem) error {
	now := time.Now().Unix()

	_, err := lm.db.Exec(`INSERT INTO lease_market 
		(unique_id, item_id, return_owner_gbid, return_owner_server_id, return_time, return_reason, lease_days,
		lessor_gbid, lessor_server_id, lessee_gbid, lessee_server_id, 
		price_per_day, lease_start_time, lease_end_time, lease_cost, lease_gold, lease_bind_gold, lease_tax, item_data, lease_status, create_time, update_time)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
		ON DUPLICATE KEY UPDATE 
		item_id=VALUES(item_id),
		return_owner_gbid=VALUES(return_owner_gbid),
		return_owner_server_id=VALUES(return_owner_server_id),
		return_time=VALUES(return_time),
		return_reason=VALUES(return_reason),
		lease_days=VALUES(lease_days),
		lessor_gbid=VALUES(lessor_gbid),
		lessor_server_id=VALUES(lessor_server_id),
		lessee_gbid=VALUES(lessee_gbid),
		lessee_server_id=VALUES(lessee_server_id),
		price_per_day=VALUES(price_per_day),
		lease_start_time=VALUES(lease_start_time),
		lease_end_time=VALUES(lease_end_time),
		lease_cost=VALUES(lease_cost),
		lease_gold=VALUES(lease_gold),
		lease_bind_gold=VALUES(lease_bind_gold),
		lease_tax=VALUES(lease_tax),
		item_data=VALUES(item_data),
		lease_status=VALUES(lease_status),
		update_time=VALUES(update_time)`,
		item.UniqueId, item.ItemId, item.ReturnOwnerGbId, item.ReturnOwnerServerId, item.ReturnEndTime, item.ReturnReason, item.LeaseDay,
		item.LessorGbId, item.LessorServerId, item.LesseeGbId, item.LesseeServerId,
		item.PricePerDay, item.LeaseStartTime, item.LeaseEndTime, item.LeaseCost, item.LeaseGold, item.LeaseBindGold,
		item.LeaseTax, item.ItemData, item.Status, item.AddTime, now)
	return err
}

func (lm *LeaseMgr) dbLeaseItemCommit(item *LeaseMarketItem, now uint32) error {
	_, err := lm.db.Exec(`UPDATE lease_market SET lease_status=?, lessee_gbid=?,
	    lessee_server_id=?, lease_start_time=?, lease_cost=?, lease_gold=?,
		lease_bind_gold=?, lease_tax=?, update_time=? WHERE unique_id=?`,
		item.Status, item.LesseeGbId, item.LesseeServerId, item.LeaseStartTime,
		item.LeaseCost, item.LeaseGold, item.LeaseBindGold, item.LeaseTax, now, item.UniqueId)
	return err
}

func (lm *LeaseMgr) dbCancelItemCAS(item *LeaseMarketItem, now uint32, oldStatus uint8) error {
	result, err := lm.db.Exec(
		"UPDATE lease_market SET lease_status=?, update_time=? WHERE unique_id=? AND lease_status=?",
		item.Status, now, item.UniqueId, oldStatus,
	)
	if err != nil {
		return err
	}
	if affected, _ := result.RowsAffected(); affected == 0 {
		return fmt.Errorf("dbCancelItemCAS failed, uniqueId=%d, oldStatus=%d", item.UniqueId, oldStatus)
	}
	return nil
}

func (lm *LeaseMgr) dbSetItemExpiredCAS(item *LeaseMarketItem, now uint32) error {
	result, err := lm.db.Exec(
		"UPDATE lease_market SET lease_status=?, update_time=? WHERE unique_id=? AND lease_status=?",
		LEASE_STATUS_EXPIRED, now, item.UniqueId, LEASE_STATUS_ON_SALE,
	)
	if err != nil {
		return err
	}
	if affected, _ := result.RowsAffected(); affected == 0 {
		return fmt.Errorf("dbSetItemExpiredCAS failed, uniqueId=%d", item.UniqueId)
	}
	return nil
}
