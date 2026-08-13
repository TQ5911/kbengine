package DropApp

import (
	"centralService/src/appLog"
	"centralService/src/common"
	gameServerService "centralService/src/dropServer/dropApp/gameServerService"
	"sync"
	"time"
)

// dropExpireData 过期掉落的数据, 用于通知掉落者
type dropExpireData struct {
	serverId  uint32
	gbId      uint64
	equipInfo []byte
}

// startDropExpireTimer 全局定时器, 掉落过期与赎回过期分开独立检查, 每轮处理结束之后再进入下一轮
func (da *DropApp) startDropExpireTimer() {
	// 掉落过期检查循环
	go da.runDropExpireCheck()
	// 赎回过期检查循环
	go da.runRedeemExpireCheck()
}

// runDropExpireCheck 掉落过期检查循环: 每轮处理结束之后再等待进入下一轮
func (da *DropApp) runDropExpireCheck() {
	for {
		da.checkDropExpire()
		time.Sleep(time.Second * 2)
	}
}

// runRedeemExpireCheck 赎回过期检查循环: 每轮处理结束之后再等待进入下一轮
func (da *DropApp) runRedeemExpireCheck() {
	for {
		da.checkRedeemExpire()
		time.Sleep(time.Second * 2)
	}
}

// checkDropExpire 掉落过期: 删除 TYPE_DROP 已过期的掉落并通知掉落者
func (da *DropApp) checkDropExpire() {
	wg := sync.WaitGroup{}
	wg.Add(1)
	common.ExecuteConcurrently(func() {
		defer wg.Done()
		// 延迟几秒过期，防止临界问题
		limitTime := common.GetNowTime()
		sql := "SELECT uniqueId, serverId, dropGbId, endTime, equipInfo FROM drop_info WHERE dropType=? AND endTime < ? order by endTime asc limit 100"
		rows, err := da.db.Query(sql, TYPE_DROP, limitTime)
		if err != nil {
			appLog.Error("checkDropExpire: get drop info error: ", err.Error())
			return
		}
		defer rows.Close()

		expireDatas := make(map[uint64]*dropExpireData, 0)
		for rows.Next() {
			var uniqueId uint64
			var serverId uint32
			var dropGbId uint64
			var endTime int64
			var equipInfo []byte
			err = rows.Scan(&uniqueId, &serverId, &dropGbId, &endTime, &equipInfo)
			if err != nil {
				appLog.Error("checkDropExpire: scan drop info error: ", err.Error())
				continue
			}
			expireDatas[uniqueId] = &dropExpireData{
				serverId:  serverId,
				gbId:      dropGbId,
				equipInfo: equipInfo,
			}
		}
		rows.Close()

		if len(expireDatas) == 0 {
			return
		}

		// 删除过期数据并通知掉落者
		for uniqueId, expireData := range expireDatas {
			da.dropItemLock.Lock(uniqueId)
			_, err = da.db.Exec("DELETE FROM drop_info WHERE uniqueId=?", uniqueId)
			da.dropItemLock.Unlock(uniqueId)
			if err != nil {
				appLog.Error("checkDropExpire: delete drop info error: ", err.Error())
				continue
			}
			// 通知掉落者装备已过期
			da.notifyEquipExpired(expireData.serverId, expireData.gbId, expireData.equipInfo)
		}
	})
	wg.Wait()
}

// checkRedeemExpire 赎回过期: TYPE_TAKE 的赎回时间超时, 转移为等待领取/归还
func (da *DropApp) checkRedeemExpire() {
	wg := sync.WaitGroup{}
	wg.Add(1)
	common.ExecuteConcurrently(func() {
		defer wg.Done()
		// 延迟几秒过期，防止临界问题
		limitTime := common.GetNowTime()
		sql := "SELECT uniqueId, dropGbId, serverId, takerGbId, takerServerId, equipInfo, redeemWaitTime, returnTime, returnTimeBack, ownerGbId FROM drop_info WHERE dropType=? AND redeemWaitTime < ? order by redeemWaitTime asc limit 100"
		rows, err := da.db.Query(sql, TYPE_TAKE, limitTime)
		if err != nil {
			appLog.Error("checkRedeemExpire: get drop info error: ", err.Error())
			return
		}
		defer rows.Close()

		now := common.GetNowTime()
		for rows.Next() {
			var uniqueId uint64
			var dropGbId uint64
			var dropServerId uint32
			var takerGbId uint64
			var takerServerId uint32
			var equipInfo []byte
			var redeemWaitTime int64
			var returnTime int64
			var returnTimeBack int64
			var ownerGbId uint64
			err = rows.Scan(&uniqueId, &dropGbId, &dropServerId, &takerGbId, &takerServerId, &equipInfo,
				&redeemWaitTime, &returnTime, &returnTimeBack, &ownerGbId)
			if err != nil {
				appLog.Error("checkRedeemExpire: scan drop info error: ", err.Error())
				continue
			}
			// 超过返还时间，交给返还系统处理
			if returnTime > 0 && now >= returnTime {
				continue
			}
			// 检查下赎回时间，不到不处理
			if now < redeemWaitTime {
				continue
			}

			da.dropItemLock.Lock(uniqueId)
			_, err = da.db.Exec("UPDATE drop_info SET dropType=?, returnTime=? WHERE uniqueId=?", TYPE_REDEEM_EXPIRE_WAIT_TAKE_GET, returnTimeBack, uniqueId)
			if err != nil {
				appLog.Error("checkRedeemExpire: update drop info error: ", err.Error())
				da.dropItemLock.Unlock(uniqueId)
				continue
			}
			// 首次掉落的，需要处理下进入等待归还
			if returnTime == 0 {
				// 被人拾取了，处理下转移关系
				sql = `INSERT INTO custody_info 
					(uniqueId, dropType, equipInfo, holderGbId, holderServerId, returnTime, ownerGbId, ownerServerId) 
					VALUES (?, ?, ?, ?, ?, ?, ?, ?) on duplicate key update holderGbId=?, holderServerId=?`
				_, err = da.db.Exec(sql, uniqueId, TYPE_RETURN_WAIT, equipInfo, takerGbId, takerServerId,
					returnTimeBack, dropGbId, dropServerId, takerGbId, takerServerId)
				if err != nil {
					appLog.Error("checkRedeemExpire: insert custody info error: ", err.Error())
					da.dropItemLock.Unlock(uniqueId)
					continue
				}
			}
			da.dropItemLock.Unlock(uniqueId)

			// 通知拾取者更新状态
			da.notifyDropTypeChange(takerServerId, uniqueId, NOTIFY_TYPE_REDEEM_EXPIRE_WAIT_TAKE_GET,
				&gameServerService.DropNotifyArgs{Args: []int64{returnTime}}, takerGbId)
			if dropGbId == ownerGbId {
				// 通知拥有者更新状态
				da.notifyDropTypeChange(dropServerId, uniqueId, NOTIFY_TYPE_RETURN_WAIT,
					&gameServerService.DropNotifyArgs{Args: []int64{returnTime}}, dropGbId)
			} else {
				// 通知掉落者更新状态
				da.notifyDropTypeChange(dropServerId, uniqueId, NOTIFY_REMOVE_DROP,
					&gameServerService.DropNotifyArgs{Args: []int64{0}}, dropGbId)
			}
		}
	})
	wg.Wait()
}

// notifyDropTypeChange 通知指定服的指定玩家掉落状态改变
func (da *DropApp) notifyDropTypeChange(
	serverId uint32,
	uniqueId uint64,
	notifyType int32,
	notifyArgs *gameServerService.DropNotifyArgs,
	gbId uint64,
) {
	gameServer := da.getGameServer(serverId)
	if gameServer == nil {
		appLog.Error("notifyDropTypeChange: get game server error: ", serverId)
		return
	}

	gameServer.Client.(*gameServerService.GameServerClient).OnDropTypeChange(&gameServerService.DropTypeChangeNotify{
		UniqueIds:   []uint64{uniqueId},
		NotifyTypes: []int32{notifyType},
		NotifyArgs:  []*gameServerService.DropNotifyArgs{notifyArgs},
		GbId:        gbId,
	})
}

func (da *DropApp) notifyEquipExpired(
	serverId uint32,
	gbId uint64,
	equipInfo []byte,
) {
	gameServer := da.getGameServer(serverId)
	if gameServer == nil {
		appLog.Error("notifyEquipExpired: get game server error: ", serverId)
		return
	}

	gameServer.Client.(*gameServerService.GameServerClient).OnNotifyEquipExpired(&gameServerService.NotifyEquipExpired{
		GbId:  gbId,
		Equip: equipInfo,
	})
}
