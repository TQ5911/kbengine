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
		// 2026-10-08 改走 store: 内存里遍历找过期 drop
		recs := da.store.FindExpiredDrops(limitTime, 100)
		if len(recs) == 0 {
			return
		}

		expireDatas := make(map[uint64]*dropExpireData, 0)
		for _, rec := range recs {
			expireDatas[rec.UniqueId] = &dropExpireData{
				serverId:  rec.ServerId,
				gbId:      rec.DropGbId,
				equipInfo: rec.EquipInfo,
			}
		}

		// 删除过期数据并通知掉落者 (mysql + 内存联动)
		for uniqueId, expireData := range expireDatas {
			da.dropItemLock.Lock(uniqueId)
			err := da.store.DeleteDropInfo(uniqueId)
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
		// 2026-10-08 改走 store: 内存里遍历找过期 redeem
		recs := da.store.FindExpiredRedeems(limitTime, 100)
		if len(recs) == 0 {
			return
		}

		now := common.GetNowTime()
		for _, rec := range recs {
			uniqueId := rec.UniqueId
			dropGbId := rec.DropGbId
			dropServerId := rec.ServerId
			takerGbId := rec.TakerGbId
			takerServerId := rec.TakerServerId
			equipInfo := rec.EquipInfo
			redeemWaitTime := rec.RedeemWaitTime
			returnTime := rec.ReturnTime
			returnTimeBack := rec.ReturnTimeBack
			ownerGbId := rec.OwnerGbId

			// 超过返还时间，交给返还系统处理
			if returnTime > 0 && now >= returnTime {
				continue
			}
			// 检查下赎回时间，不到不处理
			if now < redeemWaitTime {
				continue
			}

			da.dropItemLock.Lock(uniqueId)
			if err := da.store.UpdateDropDropTypeAndReturnTime(uniqueId, TYPE_REDEEM_EXPIRE_WAIT_TAKE_GET, returnTimeBack); err != nil {
				appLog.Error("checkRedeemExpire: update drop info error: ", err.Error())
				da.dropItemLock.Unlock(uniqueId)
				continue
			}
			// 首次掉落的，需要处理下进入等待归还
			if returnTime == 0 {
				custodyRec := &CustodyInfoRecord{
					UniqueId:       uniqueId,
					DropType:       TYPE_RETURN_WAIT,
					EquipInfo:      equipInfo,
					HolderGbId:     takerGbId,
					HolderServerId: takerServerId,
					ReturnTime:     returnTimeBack,
					OwnerGbId:      dropGbId,
					OwnerServerId:  dropServerId,
				}
				if err := da.store.UpsertCustodyHolder(custodyRec); err != nil {
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
