package DropApp

import (
	"centralService/src/appLog"
	"centralService/src/common"
	gameServerService "centralService/src/dropServer/dropApp/gameServerService"
	"centralService/src/trpc"
	"errors"
	"fmt"
	"slices"
)

type GameServerService struct {
	*trpc.ServerEndPoint
	app      *DropApp
	serverId uint32
}

const (
	TYPE_DROP                        = 1 // 掉落
	TYPE_TAKE                        = 2 // 拾取
	TYPE_TAKE_WAIT_DROP_GET          = 3 // 捡起来等待领取
	TYPE_REDEEM_WAIT_DROP_GET        = 4 // 赎回等待领取
	TYPE_GIVEUP_WAIT_DROP_GET        = 5 // 捡起掉落的人主动放弃, 待失主领取
	TYPE_REDEEM_EXPIRE_WAIT_TAKE_GET = 6 // 赎回倒计时结束，待拾取者领取
	TYPE_RETURN_WAIT                 = 7 // 等待返还
	TYPE_RETURN_GET                  = 8 // 待原主人领取
	TYPE_REWARD                      = 9 // 领取奖励
)

const (
	NOTIFY_SET_PRICE                        = -3 // 设置价格
	NOTIFY_REMOVE_TAKE                      = -2 // 移除拾取
	NOTIFY_REMOVE_DROP                      = -1 // 移除掉落
	NOTIFY_REMOVE_ALL                       = 0  // 移除所有
	NOTIFY_TYPE_DROP                        = 1  // 掉落
	NOTIFY_TYPE_TAKE                        = 2  // 拾取
	NOTIFY_TYPE_TAKE_WAIT_DROP_GET          = 3  // 捡起来等待领取
	NOTIFY_TYPE_REDEEM_WAIT_DROP_GET        = 4  // 赎回等待领取
	NOTIFY_TYPE_GIVEUP_WAIT_DROP_GET        = 5  // 捡起掉落的人主动放弃, 待失主领取
	NOTIFY_TYPE_REDEEM_EXPIRE_WAIT_TAKE_GET = 6  // 赎回倒计时结束，待拾取者领取
	NOTIFY_TYPE_RETURN_WAIT                 = 7  // 等待返还
	NOTIFY_TYPE_RETURN_GET                  = 8  // 待原主人领取
	NOTIFY_TYPE_REWARD                      = 9  // 领取奖励
)

func (gss *GameServerService) OnLoseConnection() {
	appLog.Info("on lose connection")
	gss.app.removeGameServer(gss)
}

func (gss *GameServerService) RegisterGameServer(in *gameServerService.RegisterGameServerRequest) (*gameServerService.Void, error) {
	appLog.Info("register game server:", in.ServerId)
	server := gss.app.getGameServer(in.ServerId)
	if server != nil {
		return nil, errors.New(fmt.Sprint("baseapp is already registered: ", in.ServerId))
	}

	if in.ServerId == 0 {
		return nil, errors.New(fmt.Sprint("invalid ServerId: ", in.ServerId))
	}

	gss.serverId = in.ServerId

	if !gss.app.CheckInited() {
		return nil, errors.New(fmt.Sprint("server is in init: ", in.ServerId))
	}

	gss.app.addGameServer(gss)

	return nil, nil
}

func (gss *GameServerService) Drop(in *gameServerService.DropRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		appLog.Info("on drop:", in.ServerId, in.UniqueId)
		returnTime := in.ReturnTime
		// 我自己的第一次掉
		if in.IsFirst {
			returnTime = 0
		}
		// 2026-10-08 改走 store (cache-aside + write-through): 写内存 + 同步 mysql.
		rec := &DropInfoRecord{
			ServerId:       in.ServerId,
			UniqueId:       in.UniqueId,
			DropGbId:       in.DropGbId,
			DropType:       TYPE_DROP,
			EndTime:        in.EndTime,
			EquipInfo:      in.EquipInfo,
			DropTime:       in.DropTime,
			TakerGbId:      0,
			TakerServerId:  0,
			CollExpireTime: in.CollExpireTime,
			Price:          in.Price,
			MaxPrice:       in.MaxPrice,
			ExtraInfo:      in.ExtraInfo,
			GiveUpTime:     0,
			CollectionId:   in.CollectionId,
			RedeemWaitTime: 0,
			HasRedeemPrice: 0,
			HasPayment:     0,
			ReturnTime:     returnTime,
			OwnerGbId:      in.OwnerId,
			OwnerServerId:  common.GetGameServerMergeRoot(in.OwnerServerId),
			ReturnTimeBack: in.ReturnTime,
		}
		err := gss.app.store.InsertDropInfo(rec)
		if err != nil {
			appLog.Error("Drop: insert drop info error: ", err.Error())
			gss.Client.(*gameServerService.GameServerClient).OnDrop(&gameServerService.DropResponse{
				UniqueId: in.UniqueId,
				Success:  false,
			})
			return
		}
		// 不是第一次掉，就放入待归还
		if !in.IsFirst {
			custodyRec := &CustodyInfoRecord{
				UniqueId:       in.UniqueId,
				DropType:       TYPE_RETURN_WAIT,
				EquipInfo:      in.EquipInfo,
				HolderGbId:     0,
				HolderServerId: 0,
				ReturnTime:     in.ReturnTime,
				OwnerGbId:      in.OwnerId,
				OwnerServerId:  in.OwnerServerId,
			}
			if err := gss.app.store.UpsertCustodyHolder(custodyRec); err != nil {
				appLog.Error("Drop: insert custody info error: ", err.Error())
				gss.Client.(*gameServerService.GameServerClient).OnDrop(&gameServerService.DropResponse{
					UniqueId: in.UniqueId,
					Success:  false,
				})
				return
			}
		}

		gss.Client.(*gameServerService.GameServerClient).OnDrop(&gameServerService.DropResponse{
			UniqueId: in.UniqueId,
			Success:  true,
		})
	})

	return nil, nil
}

func (gss *GameServerService) Custody(in *gameServerService.CustodyRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		appLog.Info("on custody:", in.UniqueId)
		// 2026-10-08 改走 store (memory + mysql 双写).
		custodyRec := &CustodyInfoRecord{
			UniqueId:       in.UniqueId,
			DropType:       TYPE_RETURN_WAIT,
			EquipInfo:      in.EquipInfo,
			HolderGbId:     0,
			HolderServerId: 0,
			ReturnTime:     in.ReturnTime,
			OwnerGbId:      in.OwnerId,
			OwnerServerId:  in.OwnerServerId,
		}
		if err := gss.app.store.UpsertCustodyHolder(custodyRec); err != nil {
			appLog.Error("Custody: insert custody info error: ", err.Error())
			gss.Client.(*gameServerService.GameServerClient).OnCustody(&gameServerService.CustodyResponse{
				UniqueId: in.UniqueId,
				Success:  false,
			})
			return
		}

		gss.Client.(*gameServerService.GameServerClient).OnCustody(&gameServerService.CustodyResponse{
			UniqueId: in.UniqueId,
			Success:  true,
		})
		// 通知拥有者更新状态
		gss._notifyCustodyEquip(in.OwnerServerId, in.OwnerId, in.UniqueId, uint32(in.DropType), in.EquipInfo, int64(in.ReturnTime))
	})
	return nil, nil
}

func (gss *GameServerService) Take(in *gameServerService.TakeRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		appLog.Info("on take:", in.UniqueId, in.TakerGbId)
		gss.app.dropItemLock.Lock(in.UniqueId)
		defer gss.app.dropItemLock.Unlock(in.UniqueId)

		// 2026-10-08 改走 store: 内存直接读
		rec := gss.app.store.GetDropInfoByUniqueId(in.UniqueId)
		if rec == nil {
			appLog.Error("Take: drop not found in cache:", in.UniqueId)
			gss.Client.(*gameServerService.GameServerClient).OnTake(&gameServerService.TakeResponse{
				UniqueId: in.UniqueId,
				Result:   gameServerService.DropResult_DropResult_NOT_FOUND,
			})
			return
		}
		dropGbId := rec.DropGbId
		_ = rec.TakerGbId
		dropType := rec.DropType
		equipInfo := rec.EquipInfo
		collExpireTime := rec.CollExpireTime
		endTime := rec.EndTime
		price := rec.Price
		maxPrice := rec.MaxPrice
		returnTime := rec.ReturnTime
		redeemWaitTime := rec.RedeemWaitTime
		ownerGbId := rec.OwnerGbId
		ownerServerId := rec.OwnerServerId

		var now = common.GetNowTime()
		// 大于采集物时间了，不能获取，或者超过返还时间了
		if now >= collExpireTime || (returnTime > 0 && now >= returnTime) {
			appLog.Info("Take: drop expire:", in.UniqueId)
			gss.Client.(*gameServerService.GameServerClient).OnTake(&gameServerService.TakeResponse{
				UniqueId:       in.UniqueId,
				DropGbId:       dropGbId,
				EquipInfo:      equipInfo,
				EndTime:        endTime,
				Price:          price,
				MaxPrice:       maxPrice,
				RedeemWaitTime: redeemWaitTime,
				ReturnTime:     returnTime,
				Result:         gameServerService.DropResult_DropResult_EXPIRE,
			})
			return
		}
		// 非掉落状态，不允许拾取
		if dropType != TYPE_DROP {
			gss.Client.(*gameServerService.GameServerClient).OnTake(&gameServerService.TakeResponse{
				UniqueId:       in.UniqueId,
				DropGbId:       dropGbId,
				EquipInfo:      equipInfo,
				EndTime:        endTime,
				Price:          price,
				MaxPrice:       maxPrice,
				RedeemWaitTime: redeemWaitTime,
				ReturnTime:     returnTime,
				Result:         gameServerService.DropResult_DropResult_HAS_TAKEN,
			})
			return
		}

		// 原先的returnTime等于0是首次掉落，等赎回期结束后，放入待归还
		if returnTime > 0 {
			// 被人拾取了，处理下转移关系
			custodyRec := &CustodyInfoRecord{
				UniqueId:       in.UniqueId,
				DropType:       TYPE_RETURN_WAIT,
				EquipInfo:      equipInfo,
				HolderGbId:     in.TakerGbId,
				HolderServerId: in.ServerId,
				ReturnTime:     returnTime,
				OwnerGbId:      ownerGbId,
				OwnerServerId:  ownerServerId,
			}
			if err := gss.app.store.UpsertCustodyHolder(custodyRec); err != nil {
				gss.Client.(*gameServerService.GameServerClient).OnTake(&gameServerService.TakeResponse{
					UniqueId:       in.UniqueId,
					DropGbId:       dropGbId,
					EquipInfo:      equipInfo,
					EndTime:        endTime,
					Price:          price,
					MaxPrice:       maxPrice,
					RedeemWaitTime: redeemWaitTime,
					ReturnTime:     returnTime,
					Result:         gameServerService.DropResult_DropResult_STATE_ERROR,
				})
				return
			}
		}

		// 捡起自己掉落的
		if dropGbId == in.TakerGbId {
			gss._selfTake(in, equipInfo, endTime, maxPrice, price, redeemWaitTime, redeemWaitTime)
			return
		}

		redeemWaitTime = now + int64(in.RedeemWaitTime)
		// 捡起别人掉落的
		gss._otherTake(in, dropGbId, equipInfo, endTime, maxPrice, price, redeemWaitTime, returnTime, ownerGbId, ownerServerId)
	})
	return nil, nil
}

func (gss *GameServerService) _selfTake(in *gameServerService.TakeRequest, equipInfo []byte, endTime int64, maxPrice uint32, price uint32, redeemWaitTime int64, returnTime int64) (*gameServerService.Void, error) {
	// 2026-10-08 改走 store: 条件 update (dropType 必须为 TYPE_DROP).
	_, err := gss.app.store.ConditionalUpdateDropDropType(in.UniqueId, TYPE_DROP, TYPE_TAKE_WAIT_DROP_GET)
	if err != nil {
		appLog.Error("_selfTake: drop info update error: ", err.Error())
		gss.Client.(*gameServerService.GameServerClient).OnTake(&gameServerService.TakeResponse{
			UniqueId:       in.UniqueId,
			DropGbId:       in.TakerGbId,
			EquipInfo:      equipInfo,
			EndTime:        endTime,
			Price:          price,
			MaxPrice:       maxPrice,
			RedeemWaitTime: redeemWaitTime,
			ReturnTime:     returnTime,
			Result:         gameServerService.DropResult_DropResult_HAS_TAKEN,
		})
		return nil, nil
	}

	gss.Client.(*gameServerService.GameServerClient).OnTake(&gameServerService.TakeResponse{
		UniqueId:       in.UniqueId,
		DropGbId:       in.TakerGbId,
		EquipInfo:      equipInfo,
		EndTime:        endTime,
		Price:          price,
		MaxPrice:       maxPrice,
		RedeemWaitTime: redeemWaitTime,
		ReturnTime:     returnTime,
		Result:         gameServerService.DropResult_DropResult_SUCCESS,
	})
	return nil, nil
}

func (gss *GameServerService) _otherTake(in *gameServerService.TakeRequest, dropGbId uint64, equipInfo []byte, endTime int64, maxPrice uint32, price uint32, redeemWaitTime int64, returnTime int64, ownerId uint64, ownerServerId uint32) (*gameServerService.Void, error) {
	// 2026-10-08 改走 store.
	_, err := gss.app.store.UpdateTakerFields(in.UniqueId, in.TakerGbId, in.ServerId, TYPE_TAKE, redeemWaitTime)
	if err != nil {
		appLog.Error("_otherTake: update drop info error: ", err.Error())
		gss.Client.(*gameServerService.GameServerClient).OnTake(&gameServerService.TakeResponse{
			UniqueId:       in.UniqueId,
			DropGbId:       dropGbId,
			EquipInfo:      equipInfo,
			EndTime:        endTime,
			Price:          price,
			MaxPrice:       maxPrice,
			RedeemWaitTime: redeemWaitTime,
			ReturnTime:     returnTime,
			Result:         gameServerService.DropResult_DropResult_HAS_TAKEN,
		})
		return nil, nil
	}

	notifyArgs := &gameServerService.DropNotifyArgs{
		Args: []int64{int64(in.TakerGbId), redeemWaitTime},
	}
	gss._notifyDropTypeChange(gss.serverId, in.UniqueId, NOTIFY_TYPE_TAKE, notifyArgs, dropGbId)

	gss.Client.(*gameServerService.GameServerClient).OnTake(&gameServerService.TakeResponse{
		UniqueId:       in.UniqueId,
		DropGbId:       dropGbId,
		EquipInfo:      equipInfo,
		EndTime:        endTime,
		Price:          price,
		MaxPrice:       maxPrice,
		RedeemWaitTime: redeemWaitTime,
		ReturnTime:     returnTime,
		Result:         gameServerService.DropResult_DropResult_SUCCESS,
	})

	return nil, nil
}

func (gss *GameServerService) _notifyDropTypeChange(
	serverId uint32,
	uniqueId uint64,
	notifyType int32,
	notifyArgs *gameServerService.DropNotifyArgs,
	gbId uint64,
) (*gameServerService.Void, error) {
	gameServer := gss.app.getGameServer(serverId)
	if gameServer == nil {
		appLog.Error("_notifyDropTypeChange: get game server error: ", serverId)
		return nil, nil
	}

	gameServer.Client.(*gameServerService.GameServerClient).OnDropTypeChange(&gameServerService.DropTypeChangeNotify{
		UniqueIds:   []uint64{uniqueId},
		NotifyTypes: []int32{notifyType},
		NotifyArgs:  []*gameServerService.DropNotifyArgs{notifyArgs},
		GbId:        gbId,
	})
	return nil, nil
}

func (gss *GameServerService) _notifyDropTypeChanges(
	serverId uint32,
	uniqueIds []uint64,
	notifyTypes []int32,
	notifyArgs []*gameServerService.DropNotifyArgs,
	gbId uint64,
) (*gameServerService.Void, error) {
	gameServer := gss.app.getGameServer(serverId)
	if gameServer == nil {
		appLog.Error("_notifyDropTypeChanges: get game server error: ", serverId)
		return nil, nil
	}

	gameServer.Client.(*gameServerService.GameServerClient).OnDropTypeChange(&gameServerService.DropTypeChangeNotify{
		UniqueIds:   uniqueIds,
		NotifyTypes: notifyTypes,
		NotifyArgs:  notifyArgs,
		GbId:        gbId,
	})
	return nil, nil
}

func (gss *GameServerService) _notifyCustodyEquip(
	serverId uint32,
	gbId uint64,
	uniqueId uint64,
	dropType uint32,
	equip []byte,
	returnTime int64,
) (*gameServerService.Void, error) {
	gameServer := gss.app.getGameServer(serverId)
	if gameServer == nil {
		appLog.Error("_notifyCustodyEquip: get game server error: ", serverId)
		return nil, nil
	}

	gameServer.Client.(*gameServerService.GameServerClient).OnNotifyCustodyEquip(&gameServerService.NotifyCustodyEquip{
		UniqueId:   uniqueId,
		GbId:       gbId,
		Equip:      equip,
		DropType:   dropType,
		ReturnTime: returnTime,
	})
	return nil, nil
}

func (gss *GameServerService) _notifyCleanCollections(
	serverId uint32,
	collectionIds []uint32,
	uniqueIds []uint64,
	collExpireTimes []int64) (*gameServerService.Void, error) {
	gameServer := gss.app.getGameServer(serverId)
	if gameServer == nil {
		appLog.Error("_notifyCleanCollections: get game server error: ", serverId)
		return nil, nil
	}

	gameServer.Client.(*gameServerService.GameServerClient).OnNotifyCleanCollection(&gameServerService.NotifyCleanCollections{
		CollectionIds:   collectionIds,
		UniqueIds:       uniqueIds,
		CollExpireTimes: collExpireTimes,
	})
	return nil, nil
}

func (gss *GameServerService) _notifyRemoveEquip(
	serverId uint32,
	gbId uint64,
	uniqueIds []uint64) (*gameServerService.Void, error) {
	gameServer := gss.app.getGameServer(serverId)
	if gameServer == nil {
		appLog.Error("_notifyRemoveEquip: get game server error: ", serverId)
		return nil, nil
	}

	gameServer.Client.(*gameServerService.GameServerClient).OnNotifyRemoveEquip(&gameServerService.NotifyRemoveEquip{
		GbId:      gbId,
		UniqueIds: uniqueIds,
	})
	return nil, nil
}

func (gss *GameServerService) GiveUp(in *gameServerService.GiveUpRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		appLog.Info("on give up:", in.UniqueId)
		gss.app.dropItemLock.Lock(in.UniqueId)
		defer gss.app.dropItemLock.Unlock(in.UniqueId)
		// 2026-10-08 改走 store: 内存直接读
		rec := gss.app.store.GetDropInfoByUniqueId(in.UniqueId)
		if rec == nil {
			appLog.Error("GiveUp: drop not found in cache:", in.UniqueId)
			gss.Client.(*gameServerService.GameServerClient).OnGiveUp(&gameServerService.GiveUpResponse{
				UniqueId: in.UniqueId,
				Result:   gameServerService.DropResult_DropResult_NOT_FOUND,
				Uuid:     in.Uuid,
			})
			return
		}
		serverId := rec.ServerId
		uniqueId := rec.UniqueId
		dropGbId := rec.DropGbId
		takerGbId := rec.TakerGbId
		dropType := rec.DropType
		redeemWaitTime := rec.RedeemWaitTime
		returnTime := rec.ReturnTime

		var now = common.GetNowTime()
		// 检查是否大于赎回时间
		if now >= redeemWaitTime || (returnTime > 0 && now >= returnTime) {
			gss.Client.(*gameServerService.GameServerClient).OnGiveUp(&gameServerService.GiveUpResponse{
				UniqueId: in.UniqueId,
				Result:   gameServerService.DropResult_DropResult_EXPIRE,
				Uuid:     in.Uuid,
			})
			return
		}

		if dropType != TYPE_TAKE {
			gss.Client.(*gameServerService.GameServerClient).OnGiveUp(&gameServerService.GiveUpResponse{
				UniqueId: in.UniqueId,
				Result:   gameServerService.DropResult_DropResult_STATE_ERROR,
				Uuid:     in.Uuid,
			})
			return
		}

		if takerGbId != in.TakerGbId {
			gss.Client.(*gameServerService.GameServerClient).OnGiveUp(&gameServerService.GiveUpResponse{
				UniqueId: in.UniqueId,
				Result:   gameServerService.DropResult_DropResult_NOT_TAKER,
				Uuid:     in.Uuid,
			})
			return
		}

		// 2026-10-08 改走 store: 给一个 dropInfo 整行替换 (dropType = TYPE_GIVEUP_WAIT_DROP_GET, giveUpTime = now)
		rec.DropType = TYPE_GIVEUP_WAIT_DROP_GET
		rec.GiveUpTime = now
		if err := gss.app.store.UpdateDropInfo(rec); err != nil {
			appLog.Error("GiveUp: update drop info error: ", err.Error())
			gss.Client.(*gameServerService.GameServerClient).OnGiveUp(&gameServerService.GiveUpResponse{
				UniqueId: in.UniqueId,
				Result:   gameServerService.DropResult_DropResult_STATE_ERROR,
				Uuid:     in.Uuid,
			})
			return
		}

		gss._notifyDropTypeChange(serverId, uniqueId, NOTIFY_TYPE_GIVEUP_WAIT_DROP_GET, &gameServerService.DropNotifyArgs{Args: []int64{0}}, dropGbId)

		gss.Client.(*gameServerService.GameServerClient).OnGiveUp(&gameServerService.GiveUpResponse{
			UniqueId: in.UniqueId,
			Result:   gameServerService.DropResult_DropResult_SUCCESS,
			Uuid:     in.Uuid,
			DropGbId: dropGbId,
		})

		if err := gss.app.store.UpdateCustodyHolderGiveUp(in.UniqueId, dropGbId, serverId); err != nil {
			appLog.Error("GiveUp: update custody info error: ", err.Error())
			return
		}
	})
	return nil, nil
}

func (gss *GameServerService) Redeem(in *gameServerService.RedeemRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		appLog.Info("on redeem:", in.UniqueId, in.RedeemerGbId)
		gss.app.dropItemLock.Lock(in.UniqueId)
		defer gss.app.dropItemLock.Unlock(in.UniqueId)
		// 2026-10-08 改走 store
		rec := gss.app.store.GetDropInfoByUniqueId(in.UniqueId)
		if rec == nil {
			appLog.Error("Redeem: drop not found in cache:", in.UniqueId)
			gss.Client.(*gameServerService.GameServerClient).OnRedeem(&gameServerService.RedeemResponse{
				UniqueId: in.UniqueId,
				Result:   gameServerService.DropResult_DropResult_NOT_FOUND,
				Uuid:     in.Uuid,
			})
			return
		}
		_ = rec.DropGbId
		_ = rec.ServerId
		_ = rec.TakerGbId
		dropType := rec.DropType
		collExpireTime := rec.CollExpireTime
		equipInfo := rec.EquipInfo
		endTime := rec.EndTime
		_ = rec.TakerServerId
		_ = rec.HasRedeemPrice
		_ = rec.RedeemWaitTime
		returnTime := rec.ReturnTime
		ownerGbId := rec.OwnerGbId
		ownerServerId := rec.OwnerServerId

		var now = common.GetNowTime()
		// 采集消失后，返还结束前，损毁之前
		if now < collExpireTime || (returnTime > 0 && now >= returnTime) || now >= endTime {
			gss.Client.(*gameServerService.GameServerClient).OnRedeem(&gameServerService.RedeemResponse{
				UniqueId: in.UniqueId,
				Result:   gameServerService.DropResult_DropResult_REDEEM_TIME_EXPIRED,
				Uuid:     in.Uuid,
			})
			return
		}

		if dropType != TYPE_DROP {
			appLog.Error("Redeem: drop type is not drop or take: ", dropType)
			gss.Client.(*gameServerService.GameServerClient).OnRedeem(&gameServerService.RedeemResponse{
				UniqueId: in.UniqueId,
				Result:   gameServerService.DropResult_DropResult_STATE_ERROR,
				Uuid:     in.Uuid,
			})
			return
		}

		// 2026-10-08 改走 store: 条件 update (dropType 必须为当前 dropType, 通常是 TYPE_DROP)
		_, err := gss.app.store.ConditionalUpdateDropDropType(in.UniqueId, dropType, TYPE_REDEEM_WAIT_DROP_GET)
		if err != nil {
			appLog.Error("Redeem: update drop info error: ", err.Error())
			gss.Client.(*gameServerService.GameServerClient).OnRedeem(&gameServerService.RedeemResponse{
				UniqueId: in.UniqueId,
				Result:   gameServerService.DropResult_DropResult_STATE_ERROR,
				Uuid:     in.Uuid,
			})
			return
		}

		if returnTime > 0 {
			// 被人赎回了，处理下转移关系
			custodyRec := &CustodyInfoRecord{
				UniqueId:       in.UniqueId,
				DropType:       TYPE_RETURN_WAIT,
				EquipInfo:      equipInfo,
				HolderGbId:     in.RedeemerGbId,
				HolderServerId: in.ServerId,
				ReturnTime:     returnTime,
				OwnerGbId:      ownerGbId,
				OwnerServerId:  ownerServerId,
			}
			if err := gss.app.store.UpsertCustodyHolder(custodyRec); err != nil {
				appLog.Error("Redeem: insert custody info error: ", err.Error())
				gss.Client.(*gameServerService.GameServerClient).OnRedeem(&gameServerService.RedeemResponse{
					UniqueId: in.UniqueId,
					Result:   gameServerService.DropResult_DropResult_STATE_ERROR,
					Uuid:     in.Uuid,
				})
				return
			}
		}

		result := gameServerService.RedeemResponse{
			UniqueId: in.UniqueId,
			Result:   gameServerService.DropResult_DropResult_SUCCESS,
			Uuid:     in.Uuid,
		}
		gss.Client.(*gameServerService.GameServerClient).OnRedeem(&result)
	})
	return nil, nil
}

func (gss *GameServerService) ActiveTick(in *gameServerService.Void) (*gameServerService.Void, error) {
	_, err := gss.GetClientEndPoint().(*gameServerService.GameServerClient).ActiveTickCallback(&gameServerService.Void{})
	return nil, err
}

func (gss *GameServerService) GetTakeReward(in *gameServerService.GetTakeRewardRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		appLog.Info("on get take reward:", in.UniqueId, in.TakerGbId)
		// 2026-10-08 改走 store: 内存直接读
		rec := gss.app.store.GetRewardByUniqueId(in.UniqueId)
		if rec == nil {
			appLog.Error("GetTakeReward: reward not found in cache:", in.UniqueId)
			gss.Client.(*gameServerService.GameServerClient).OnGetTakeReward(&gameServerService.GetTakeRewardResponse{
				UniqueId: in.UniqueId,
				Result:   gameServerService.DropResult_DropResult_NOT_FOUND,
				Uuid:     in.Uuid,
			})
			return
		}
		bindMoney := rec.BindMoney
		money := rec.Money

		if err := gss.app.store.DeleteRewardByUniqueId(in.UniqueId); err != nil {
			appLog.Error("GetTakeReward: delete reward info error: ", err.Error())
			gss.Client.(*gameServerService.GameServerClient).OnGetTakeReward(&gameServerService.GetTakeRewardResponse{
				UniqueId: in.UniqueId,
				Result:   gameServerService.DropResult_DropResult_STATE_ERROR,
				Uuid:     in.Uuid,
			})
			return
		}

		gss.Client.(*gameServerService.GameServerClient).OnGetTakeReward(&gameServerService.GetTakeRewardResponse{
			UniqueId:  in.UniqueId,
			Result:    gameServerService.DropResult_DropResult_SUCCESS,
			BindMoney: bindMoney,
			Money:     money,
			Uuid:      in.Uuid,
		})
	})
	return nil, nil
}

func (gss *GameServerService) GetDropInfo(in *gameServerService.GetDropInfoRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		appLog.Info("on get drop info:", in.GbId)
		// 2026-10-08 改走 store: 4 段全部走内存
		inDrop := make(map[uint64]bool)

		dropInfoList := make([]*gameServerService.DropInfo, 0)
		for _, rec := range gss.app.store.GetDropInfosByDropGbId(in.GbId) {
			// 进入赎回超时等待返还了，掉落列表就不用显示了
			if rec.DropType == TYPE_REDEEM_EXPIRE_WAIT_TAKE_GET {
				continue
			}
			dropInfoList = append(dropInfoList, &gameServerService.DropInfo{
				UniqueId:       rec.UniqueId,
				DropType:       rec.DropType,
				EndTime:        rec.EndTime,
				CollExpireTime: rec.CollExpireTime,
				ExtraInfo:      rec.ExtraInfo,
				EquipInfo:      rec.EquipInfo,
				Price:          rec.Price,
				DropTime:       rec.DropTime,
				HasPrice:       rec.HasRedeemPrice != 0,
				ReturnTime:     rec.ReturnTime,
				RedeemWaitTime: rec.RedeemWaitTime,
				TakerGbId:      rec.TakerGbId,
			})
			inDrop[rec.UniqueId] = true
		}

		takerInfoList := make([]*gameServerService.TakerInfo, 0)
		for _, rec := range gss.app.store.GetDropInfosByTakerGbId(in.GbId) {
			// 掉落中，放弃等待领取，赎回等待领取的就不用显示了
			if rec.DropType == TYPE_DROP || rec.DropType == TYPE_GIVEUP_WAIT_DROP_GET || rec.DropType == TYPE_REDEEM_WAIT_DROP_GET {
				continue
			}
			takerInfoList = append(takerInfoList, &gameServerService.TakerInfo{
				UniqueId:       rec.UniqueId,
				Price:          rec.Price,
				EndTime:        rec.EndTime,
				DropType:       rec.DropType,
				EquipInfo:      rec.EquipInfo,
				RedeemWaitTime: rec.RedeemWaitTime,
				HasPrice:       rec.HasRedeemPrice != 0,
				ReturnTime:     rec.ReturnTime,
				MaxPrice:       rec.MaxPrice,
			})
		}

		rewardInfoList := make([]*gameServerService.RewardInfo, 0)
		for _, rec := range gss.app.store.GetRewardListByGbId(in.GbId) {
			rewardInfoList = append(rewardInfoList, &gameServerService.RewardInfo{
				UniqueId:  rec.UniqueId,
				EquipInfo: rec.EquipInfo,
				BindMoney: uint64(rec.BindMoney),
				Money:     uint64(rec.Money),
			})
		}

		returnInfoList := make([]*gameServerService.ReturnInfo, 0)
		for _, rec := range gss.app.store.GetCustodyInfosByOwnerGbId(in.GbId) {
			uniqueId := rec.UniqueId
			if _, ok := inDrop[uniqueId]; ok {
				continue
			}
			returnInfoList = append(returnInfoList, &gameServerService.ReturnInfo{
				UniqueId:   uniqueId,
				EquipInfo:  rec.EquipInfo,
				DropType:   rec.DropType,
				ReturnTime: rec.ReturnTime,
			})
		}

		gss.Client.(*gameServerService.GameServerClient).OnGetDropInfo(&gameServerService.GetDropInfoResponse{
			DropInfos:   dropInfoList,
			TakerInfos:  takerInfoList,
			ReturnInfos: returnInfoList,
			RewardInfos: rewardInfoList,
			Uuid:        in.Uuid,
		})
	})
	return nil, nil
}

func (gss *GameServerService) SendRepairDropMail(in *gameServerService.SendRepairDropMailRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		appLog.Info("on send repair drop mail:", in.UniqueId)
		// 2026-10-08 改走 store
		rec := gss.app.store.GetDropInfoByUniqueId(in.UniqueId)
		if rec == nil {
			appLog.Error("SendRepairDropMail: drop not found in cache:", in.UniqueId)
			return
		}
		dropGbId := rec.DropGbId
		dropType := rec.DropType
		serverId := rec.ServerId
		equipInfo := rec.EquipInfo
		endTime := rec.EndTime

		gameServer := gss.app.getGameServer(serverId)
		if gameServer == nil {
			appLog.Error("SendRepairDropMail: get game server error: ", serverId)
			return
		}

		if dropType != TYPE_DROP {
			appLog.Error("SendRepairDropMail: drop type error: ", dropType)
			return
		}

		gameServer.Client.(*gameServerService.GameServerClient).OnSendRepairDropMail(&gameServerService.SendRepairDropMailResponse{
			UniqueId:  in.UniqueId,
			GbId:      dropGbId,
			EquipInfo: equipInfo,
			EndTime:   endTime,
		})
	})
	return nil, nil
}

func (gss *GameServerService) UpdateCollEndTime(in *gameServerService.UpdateCollEndTimeRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		appLog.Info("on update coll end time:", in.UniqueId, in.CollEndTime)
		gss.app.dropItemLock.Lock(in.UniqueId)
		defer gss.app.dropItemLock.Unlock(in.UniqueId)

		// 2026-10-08 改走 store
		if err := gss.app.store.UpdateCollExpireTime(in.UniqueId, in.CollEndTime); err != nil {
			appLog.Error("UpdateCollEndTime: update coll end time error: ", err.Error())
			return
		}
	})
	return nil, nil
}

func (gss *GameServerService) SetTakeEquipRedeemPrice(in *gameServerService.SetTakeEquipRedeemPriceRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		appLog.Info("set take equip redeem price:", in.UniqueId, in.GbId)
		gss.app.dropItemLock.Lock(in.UniqueId)
		defer gss.app.dropItemLock.Unlock(in.UniqueId)
		// 2026-10-08 改走 store
		rec := gss.app.store.GetDropInfoByUniqueId(in.UniqueId)
		if rec == nil {
			appLog.Error("SetTakeEquipRedeemPrice: not found in cache:", in.UniqueId)
			gss.Client.(*gameServerService.GameServerClient).OnSetTakeEquipRedeemPrice(&gameServerService.SetTakeEquipRedeemPriceResponse{
				Uuid:     in.Uuid,
				GbId:     in.GbId,
				UniqueId: in.UniqueId,
				Price:    in.Price,
				Result:   gameServerService.DropResult_DropResult_NOT_FOUND,
			})
			return
		}
		dropGbId := rec.DropGbId
		dropType := rec.DropType
		dropServerId := rec.ServerId
		redeemWaitTime := rec.RedeemWaitTime
		returnTime := rec.ReturnTime

		if dropType != TYPE_TAKE {
			gss.Client.(*gameServerService.GameServerClient).OnSetTakeEquipRedeemPrice(&gameServerService.SetTakeEquipRedeemPriceResponse{
				Uuid:     in.Uuid,
				GbId:     in.GbId,
				UniqueId: in.UniqueId,
				Price:    in.Price,
				Result:   gameServerService.DropResult_DropResult_STATE_ERROR,
			})
			return
		}

		now := common.GetNowTime()
		if now >= redeemWaitTime || (returnTime > 0 && now >= returnTime) {
			gss.Client.(*gameServerService.GameServerClient).OnSetTakeEquipRedeemPrice(&gameServerService.SetTakeEquipRedeemPriceResponse{
				Uuid:     in.Uuid,
				GbId:     in.GbId,
				UniqueId: in.UniqueId,
				Price:    in.Price,
				Result:   gameServerService.DropResult_DropResult_SET_REDEEM_PRICE_EXPIRE,
			})
			return
		}

		_, err := gss.app.store.UpdateDropPrice(in.UniqueId, in.Price, TYPE_TAKE)
		if err != nil {
			appLog.Error("SetTakeEquipRedeemPrice: update drop info error: ", err.Error())
			gss.Client.(*gameServerService.GameServerClient).OnSetTakeEquipRedeemPrice(&gameServerService.SetTakeEquipRedeemPriceResponse{
				Uuid:     in.Uuid,
				GbId:     in.GbId,
				UniqueId: in.UniqueId,
				Price:    in.Price,
				Result:   gameServerService.DropResult_DropResult_OTHER_REDEEM,
			})
			return
		}

		gss.Client.(*gameServerService.GameServerClient).OnSetTakeEquipRedeemPrice(&gameServerService.SetTakeEquipRedeemPriceResponse{
			Uuid:     in.Uuid,
			GbId:     in.GbId,
			UniqueId: in.UniqueId,
			Price:    in.Price,
			Result:   gameServerService.DropResult_DropResult_SUCCESS,
		})

		gss._notifyDropTypeChange(dropServerId, in.UniqueId, NOTIFY_SET_PRICE, &gameServerService.DropNotifyArgs{Args: []int64{int64(in.Price)}}, dropGbId)
	})
	return nil, nil
}

func (gss *GameServerService) CheckDropReturnExpire(in *gameServerService.CheckDropReturnExpireRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		// 2026-10-08 改走 store: 内存里遍历 custody_info 找过期 return
		curTime := common.GetNowTime()
		limitTime := curTime + 5

		custodyRecs := gss.app.store.FindExpiringCustodyReturns(in.ServerId, limitTime, 200)
		if len(custodyRecs) == 0 {
			return
		}

		holderReturnCacheDatas := make(map[uint64]*gameServerService.NotifyRemoveEquipCacheData, 0)
		ownerReturnCacheDatas := make(map[uint64]*gameServerService.NotifyDropCacheData, 0)
		returnUniqueIds := make([]uint64, 0)

		// 1. 从 memory 里读取 custody 记录 (代替原来对 custody_info 的 SELECT)
		for _, rec := range custodyRecs {
			uniqueId := rec.UniqueId
			holderGbId := rec.HolderGbId
			holderServerId := rec.HolderServerId
			ownerGbId := rec.OwnerGbId
			ownerServerId := rec.OwnerServerId
			_ = rec.ReturnTime

			returnUniqueIds = append(returnUniqueIds, uniqueId)
			if ownerGbId > 0 {
				ownerReturnCacheData, ok := ownerReturnCacheDatas[ownerGbId]
				if !ok {
					ownerReturnCacheData = &gameServerService.NotifyDropCacheData{
						UniqueIds: make([]uint64, 0),
						DropTypes: make([]int32, 0),
					}
					ownerReturnCacheDatas[ownerGbId] = ownerReturnCacheData
				}
				ownerReturnCacheData.ServerId = ownerServerId
				ownerReturnCacheData.UniqueIds = append(ownerReturnCacheData.UniqueIds, uniqueId)
				ownerReturnCacheData.DropTypes = append(ownerReturnCacheData.DropTypes, NOTIFY_TYPE_RETURN_GET)
			}

			if holderGbId > 0 {
				holderReturnCacheData, ok := holderReturnCacheDatas[holderGbId]
				if !ok {
					holderReturnCacheData = &gameServerService.NotifyRemoveEquipCacheData{
						UniqueIds: make([]uint64, 0),
					}
					holderReturnCacheDatas[holderGbId] = holderReturnCacheData
				}
				holderReturnCacheData.ServerId = holderServerId
				holderReturnCacheData.UniqueIds = append(holderReturnCacheData.UniqueIds, uniqueId)
			}
		}

		// 2. 走 store 读 drop_info records (按 uniqueId)
		dropDatas := make(map[uint64]*gameServerService.NotifyDropCacheData)
		takerDatas := make(map[uint64]*gameServerService.NotifyDropCacheData)
		collectionDatas := make(map[uint32]*gameServerService.NotifyCollectionCacheData)
		for _, uniqueId := range returnUniqueIds {
			dropRec := gss.app.store.GetDropInfoByUniqueId(uniqueId)
			if dropRec == nil {
				continue
			}
			dropServerId := dropRec.ServerId
			dropGbId := dropRec.DropGbId
			takerServerId := dropRec.TakerServerId
			takerGbId := dropRec.TakerGbId
			collExpireTime := dropRec.CollExpireTime
			collectionId := dropRec.CollectionId

			ownerReturnCacheData, ok := ownerReturnCacheDatas[dropGbId]
			if !ok || !slices.Contains(ownerReturnCacheData.UniqueIds, uniqueId) {
				dropData, ok := dropDatas[dropGbId]
				if !ok {
					dropData = &gameServerService.NotifyDropCacheData{
						UniqueIds: make([]uint64, 0),
						DropTypes: make([]int32, 0),
					}
					dropDatas[dropGbId] = dropData
				}
				dropData.ServerId = dropServerId
				dropData.UniqueIds = append(dropData.UniqueIds, uniqueId)
				dropData.DropTypes = append(dropData.DropTypes, NOTIFY_REMOVE_ALL)
			}

			ownerReturnCacheData, ok = ownerReturnCacheDatas[takerGbId]
			if !ok || !slices.Contains(ownerReturnCacheData.UniqueIds, uniqueId) {
				takerData, ok := takerDatas[takerGbId]
				if !ok {
					takerData = &gameServerService.NotifyDropCacheData{
						UniqueIds: make([]uint64, 0),
						DropTypes: make([]int32, 0),
					}
					takerDatas[takerGbId] = takerData
				}

				takerData.ServerId = takerServerId
				takerData.UniqueIds = append(takerData.UniqueIds, uniqueId)
				takerData.DropTypes = append(takerData.DropTypes, NOTIFY_REMOVE_ALL)
			}

			if curTime < collExpireTime {
				collectionData, ok := collectionDatas[dropServerId]
				if !ok {
					collectionData = &gameServerService.NotifyCollectionCacheData{
						CollectionIds: make([]uint32, 0),
						UniqueIds:     make([]uint64, 0),
					}
					collectionDatas[dropServerId] = collectionData
				}
				collectionData.CollectionIds = append(collectionData.CollectionIds, collectionId)
				collectionData.UniqueIds = append(collectionData.UniqueIds, uniqueId)
				collectionData.CollExpireTimes = append(collectionData.CollExpireTimes, collExpireTime)
			}
		}

		// 3. 批量删除 drop_info (DB + 内存)
		if err := gss.app.store.DeleteDropInfos(returnUniqueIds); err != nil {
			appLog.Error("CheckDropReturnExpire: delete drop info error: ", err.Error())
			return
		}

		// 4. 批量更新 custody_info: dropType=TYPE_RETURN_GET (DB + 内存)
		if err := gss.app.store.BatchUpdateCustodyDropType(returnUniqueIds, TYPE_RETURN_GET); err != nil {
			appLog.Error("CheckDropReturnExpire: update custody info error: ", err.Error())
			return
		}

		// 5.给掉落者发送移除所有数据
		for gbId, data := range dropDatas {
			gss._notifyDropTypeChanges(data.ServerId, data.UniqueIds, data.DropTypes, nil, gbId)
		}
		// 6.给拾取者发送移除所有数据
		for gbId, data := range takerDatas {
			gss._notifyDropTypeChanges(data.ServerId, data.UniqueIds, data.DropTypes, nil, gbId)
		}
		// 7.给持有人发送移除装备
		for gbId, data := range holderReturnCacheDatas {
			gss._notifyRemoveEquip(data.ServerId, gbId, data.UniqueIds)
		}
		// 8.给原主人发送装备变更数据
		for gbId, data := range ownerReturnCacheDatas {
			gss._notifyDropTypeChanges(data.ServerId, data.UniqueIds, data.DropTypes, nil, gbId)
		}
		// 9.广播指定服, 清理创生物
		for serverId, collectionData := range collectionDatas {
			gss._notifyCleanCollections(serverId, collectionData.CollectionIds, collectionData.UniqueIds, collectionData.CollExpireTimes)
		}
	})

	gss.Client.(*gameServerService.GameServerClient).OnCheckDropReturnExpire(&gameServerService.CheckDropReturnExpireResponse{
		Uuid:     in.Uuid,
		ServerId: in.ServerId,
	})
	return nil, nil
}

func (gss *GameServerService) GetBackEquip(in *gameServerService.GetBackEquipRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		appLog.Info("on get back equip:", in.UniqueId, in.GbId)
		gss.app.dropItemLock.Lock(in.UniqueId)
		defer gss.app.dropItemLock.Unlock(in.UniqueId)
		// 2026-10-08 改走 store
		if in.DropType == TYPE_TAKE_WAIT_DROP_GET || in.DropType == TYPE_REDEEM_WAIT_DROP_GET || in.DropType == TYPE_GIVEUP_WAIT_DROP_GET {
			rec := gss.app.store.GetDropInfoByUniqueId(in.UniqueId)
			if rec == nil || rec.DropGbId != in.GbId || rec.DropType != in.DropType {
				appLog.Error("GetBackEquip: drop not found or mismatch:", in.UniqueId)
				gss.Client.(*gameServerService.GameServerClient).OnGetBackEquip(&gameServerService.GetBackEquipResponse{
					UniqueId: in.UniqueId,
					DropType: in.DropType,
					GbId:     in.GbId,
					Result:   gameServerService.DropResult_DropResult_NOT_FOUND,
				})
				return
			}
			_ = rec.DropGbId
			equipInfo := rec.EquipInfo
			returnTime := rec.ReturnTime

			now := common.GetNowTime()
			if returnTime > 0 && now >= returnTime {
				gss.Client.(*gameServerService.GameServerClient).OnGetBackEquip(&gameServerService.GetBackEquipResponse{
					UniqueId:   in.UniqueId,
					DropType:   in.DropType,
					GbId:       in.GbId,
					EquipInfo:  equipInfo,
					ReturnTime: returnTime,
					Result:     gameServerService.DropResult_DropResult_GET_BACK_EXPIRED,
				})
				return
			}
			if err := gss.app.store.DeleteDropInfo(in.UniqueId); err != nil {
				appLog.Error("GetBackEquip: delete drop info error: ", err.Error())
				gss.Client.(*gameServerService.GameServerClient).OnGetBackEquip(&gameServerService.GetBackEquipResponse{
					UniqueId:   in.UniqueId,
					DropType:   in.DropType,
					GbId:       in.GbId,
					EquipInfo:  equipInfo,
					ReturnTime: returnTime,
					Result:     gameServerService.DropResult_DropResult_GET_BACK_EXPIRED,
				})
				return
			}
			gss.Client.(*gameServerService.GameServerClient).OnGetBackEquip(&gameServerService.GetBackEquipResponse{
				UniqueId:   in.UniqueId,
				DropType:   in.DropType,
				EquipInfo:  equipInfo,
				GbId:       in.GbId,
				ReturnTime: returnTime,
				Result:     gameServerService.DropResult_DropResult_SUCCESS,
			})
		} else if in.DropType == TYPE_REDEEM_EXPIRE_WAIT_TAKE_GET {
			rec := gss.app.store.GetDropInfoByUniqueId(in.UniqueId)
			if rec == nil || rec.TakerGbId != in.GbId || rec.DropType != in.DropType {
				appLog.Error("GetBackEquip: drop not found or mismatch:", in.UniqueId)
				gss.Client.(*gameServerService.GameServerClient).OnGetBackEquip(&gameServerService.GetBackEquipResponse{
					UniqueId: in.UniqueId,
					DropType: in.DropType,
					GbId:     in.GbId,
					Result:   gameServerService.DropResult_DropResult_NOT_FOUND,
				})
				return
			}
			equipInfo := rec.EquipInfo
			returnTime := rec.ReturnTime
			now := common.GetNowTime()
			if now >= returnTime {
				gss.Client.(*gameServerService.GameServerClient).OnGetBackEquip(&gameServerService.GetBackEquipResponse{
					UniqueId:   in.UniqueId,
					DropType:   in.DropType,
					GbId:       in.GbId,
					EquipInfo:  equipInfo,
					ReturnTime: returnTime,
					Result:     gameServerService.DropResult_DropResult_GET_BACK_EXPIRED,
				})
				return
			}
			if err := gss.app.store.DeleteDropInfo(in.UniqueId); err != nil {
				appLog.Error("GetBackEquip: delete drop info error: ", err.Error())
				gss.Client.(*gameServerService.GameServerClient).OnGetBackEquip(&gameServerService.GetBackEquipResponse{
					UniqueId:   in.UniqueId,
					DropType:   in.DropType,
					GbId:       in.GbId,
					EquipInfo:  equipInfo,
					ReturnTime: returnTime,
					Result:     gameServerService.DropResult_DropResult_GET_BACK_EXPIRED,
				})
				return
			}
			gss.Client.(*gameServerService.GameServerClient).OnGetBackEquip(&gameServerService.GetBackEquipResponse{
				UniqueId:   in.UniqueId,
				DropType:   in.DropType,
				EquipInfo:  equipInfo,
				GbId:       in.GbId,
				ReturnTime: returnTime,
				Result:     gameServerService.DropResult_DropResult_SUCCESS,
			})
		} else if in.DropType == TYPE_RETURN_GET {
			rec := gss.app.store.GetCustodyInfoByUniqueId(in.UniqueId)
			if rec == nil || rec.OwnerGbId != in.GbId || rec.DropType != in.DropType {
				appLog.Error("GetBackEquip: custody not found or mismatch:", in.UniqueId)
				gss.Client.(*gameServerService.GameServerClient).OnGetBackEquip(&gameServerService.GetBackEquipResponse{
					UniqueId:   in.UniqueId,
					DropType:   in.DropType,
					GbId:       in.GbId,
					ReturnTime: 0,
					Result:     gameServerService.DropResult_DropResult_NOT_FOUND,
				})
				return
			}
			equipInfo := rec.EquipInfo
			if err := gss.app.store.DeleteCustodyInfo(in.UniqueId); err != nil {
				appLog.Error("GetBackEquip: delete custody info error: ", err.Error())
				gss.Client.(*gameServerService.GameServerClient).OnGetBackEquip(&gameServerService.GetBackEquipResponse{
					UniqueId:  in.UniqueId,
					DropType:  in.DropType,
					GbId:      in.GbId,
					EquipInfo: equipInfo,
					Result:    gameServerService.DropResult_DropResult_STATE_ERROR,
				})
				return
			}
			gss.Client.(*gameServerService.GameServerClient).OnGetBackEquip(&gameServerService.GetBackEquipResponse{
				UniqueId:   in.UniqueId,
				DropType:   in.DropType,
				EquipInfo:  equipInfo,
				GbId:       in.GbId,
				ReturnTime: 0,
				Result:     gameServerService.DropResult_DropResult_SUCCESS,
			})
		} else {
			appLog.Error("GetBackEquip: get back equip drop type error: ", in.DropType, in.GbId, in.DropType)
			gss.Client.(*gameServerService.GameServerClient).OnGetBackEquip(&gameServerService.GetBackEquipResponse{
				UniqueId:   in.UniqueId,
				DropType:   in.DropType,
				GbId:       in.GbId,
				ReturnTime: 0,
				Result:     gameServerService.DropResult_DropResult_GET_BACK_TYPE_ERROR,
			})
			return
		}
	})
	return nil, nil
}

func (gss *GameServerService) SetDropEquipPayPrice(in *gameServerService.SetDropEquipPayPriceRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		appLog.Info("set drop equip pay price:", in.UniqueId, in.GbId)
		gss.app.dropItemLock.Lock(in.UniqueId)
		defer gss.app.dropItemLock.Unlock(in.UniqueId)
		// 2026-10-08 改走 store
		rec := gss.app.store.GetDropInfoByUniqueId(in.UniqueId)
		if rec == nil {
			appLog.Error("SetDropEquipPayPrice: not found in cache:", in.UniqueId)
			gss.Client.(*gameServerService.GameServerClient).OnSetDropEquipPayPrice(&gameServerService.SetDropEquipPayPriceResponse{
				Uuid:     in.Uuid,
				GbId:     in.GbId,
				UniqueId: in.UniqueId,
				Price:    in.Price,
				Result:   gameServerService.DropResult_DropResult_NOT_FOUND,
			})
			return
		}
		dropGbId := rec.DropGbId
		takeGbId := rec.TakerGbId
		takerServerId := rec.TakerServerId
		dropType := rec.DropType
		dropServerId := rec.ServerId
		redeemWaitTime := rec.RedeemWaitTime
		returnTime := rec.ReturnTime
		price := int64(rec.Price)
		equipInfo := rec.EquipInfo

		if dropType != TYPE_TAKE {
			gss.Client.(*gameServerService.GameServerClient).OnSetDropEquipPayPrice(&gameServerService.SetDropEquipPayPriceResponse{
				Uuid:     in.Uuid,
				GbId:     in.GbId,
				UniqueId: in.UniqueId,
				Price:    in.Price,
				Result:   gameServerService.DropResult_DropResult_STATE_ERROR,
			})
			return
		}

		now := common.GetNowTime()
		if now >= redeemWaitTime || (returnTime > 0 && now >= returnTime) {
			gss.Client.(*gameServerService.GameServerClient).OnSetDropEquipPayPrice(&gameServerService.SetDropEquipPayPriceResponse{
				Uuid:     in.Uuid,
				GbId:     in.GbId,
				UniqueId: in.UniqueId,
				Price:    in.Price,
				Result:   gameServerService.DropResult_DropResult_SET_PAY_PRICE_EXPIRE,
			})
			return
		}

		if in.Price != uint32(price) {
			gss.Client.(*gameServerService.GameServerClient).OnSetDropEquipPayPrice(&gameServerService.SetDropEquipPayPriceResponse{
				Uuid:     in.Uuid,
				GbId:     in.GbId,
				UniqueId: in.UniqueId,
				Price:    in.Price,
				Result:   gameServerService.DropResult_DropResult_SET_PAY_PRICE_NOT_SAME,
			})
			return
		}
		// 条件 update: dropType 必须为 TYPE_TAKE 才改, 防并发.
		_, err := gss.app.store.ConditionalUpdateDropDropType(in.UniqueId, TYPE_TAKE, TYPE_REDEEM_WAIT_DROP_GET)
		if err != nil {
			appLog.Error("SetDropEquipPayPrice: update drop info error: ", err.Error())
			gss.Client.(*gameServerService.GameServerClient).OnSetDropEquipPayPrice(&gameServerService.SetDropEquipPayPriceResponse{
				Uuid:     in.Uuid,
				GbId:     in.GbId,
				UniqueId: in.UniqueId,
				Price:    in.Price,
				Result:   gameServerService.DropResult_DropResult_OTHER_REDEEM,
			})
			return
		}
		// 同步设置 hasPayment (走 UpdateDropInfo + 直接改 rec 字段)
		rec2 := gss.app.store.GetDropInfoByUniqueId(in.UniqueId)
		if rec2 != nil {
			rec2.HasPayment = 1
			if err := gss.app.store.UpdateDropInfo(rec2); err != nil {
				appLog.Error("SetDropEquipPayPrice: set hasPayment error: ", err.Error())
			}
		}

		// 从 store 取当前 reward_info (允许不存在 — 历史数据里可能没)
		var oldBindMoney int64
		var oldMoney int64
		if rewardRec := gss.app.store.GetRewardByUniqueId(in.UniqueId); rewardRec != nil {
			oldBindMoney = int64(rewardRec.BindMoney)
			oldMoney = int64(rewardRec.Money)
		}

		bindMoney := oldBindMoney + int64(in.BindMoney)
		money := oldMoney + int64(in.Money)
		if bindMoney > 0 || money > 0 {
			rewardRec := &RewardInfoRecord{
				UniqueId:  in.UniqueId,
				GbId:      takeGbId,
				ServerId:  takerServerId,
				BindMoney: uint32(bindMoney),
				Money:     uint32(money),
				EquipInfo: equipInfo,
			}
			if err := gss.app.store.UpsertReward(rewardRec); err != nil {
				appLog.Error("SetDropEquipPayPrice: upsert reward error: ", err.Error())
				gss.Client.(*gameServerService.GameServerClient).OnSetDropEquipPayPrice(&gameServerService.SetDropEquipPayPriceResponse{
					Uuid:     in.Uuid,
					GbId:     in.GbId,
					UniqueId: in.UniqueId,
					Price:    in.Price,
					Result:   gameServerService.DropResult_DropResult_STATE_ERROR,
				})
				return
			}
			gss._notifyDropTypeChange(takerServerId, in.UniqueId, NOTIFY_TYPE_REWARD, &gameServerService.DropNotifyArgs{Args: []int64{bindMoney, money}}, takeGbId)
		} else {
			gss._notifyDropTypeChange(takerServerId, in.UniqueId, NOTIFY_REMOVE_TAKE, &gameServerService.DropNotifyArgs{Args: []int64{0}}, takeGbId)
		}

		gss._notifyDropTypeChange(dropServerId, in.UniqueId, NOTIFY_TYPE_REDEEM_WAIT_DROP_GET, &gameServerService.DropNotifyArgs{Args: []int64{0}}, dropGbId)

		gss.Client.(*gameServerService.GameServerClient).OnSetDropEquipPayPrice(&gameServerService.SetDropEquipPayPriceResponse{
			Uuid:     in.Uuid,
			GbId:     in.GbId,
			UniqueId: in.UniqueId,
			Price:    in.Price,
			Result:   gameServerService.DropResult_DropResult_SUCCESS,
		})
	})
	return nil, nil
}
