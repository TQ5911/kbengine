package DropApp

import (
	"centralService/src/appLog"
	"centralService/src/common"
	gameServerService "centralService/src/dropServer/dropApp/gameServerService"
	"centralService/src/trpc"
	dtSQL "database/sql"
	"errors"
	"fmt"
	"slices"
	"strings"
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
		sql := `INSERT INTO drop_info 
		(serverId, uniqueId, dropGbId, dropType, endTime, equipInfo, dropTime, takerGbId, takerServerId, collExpireTime, price, 
		extraInfo, giveUpTime, collectionId, redeemWaitTime, hasRedeemPrice, hasPayment, returnTime, ownerGbId, ownerServerId, returnTimeBack) 
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`

		_, err := gss.app.db.Exec(sql, in.ServerId, in.UniqueId, in.DropGbId, TYPE_DROP, in.EndTime, in.EquipInfo, in.DropTime, 0, 0,
			in.CollExpireTime, in.Price, in.ExtraInfo, 0, in.CollectionId, 0, 0, 0, returnTime, in.OwnerId, in.OwnerServerId, in.ReturnTime)
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
			// 更新一下返还情况
			sql = `INSERT INTO custody_info 
				(uniqueId, dropType, equipInfo, holderGbId, holderServerId, returnTime, ownerGbId, ownerServerId) 
				VALUES (?, ?, ?, ?, ?, ?, ?, ?) on duplicate key update holderGbId=?, holderServerId=?`
			_, err = gss.app.db.Exec(sql, in.UniqueId, TYPE_RETURN_WAIT, in.EquipInfo, 0, 0,
				in.ReturnTime, in.OwnerId, in.OwnerServerId, 0, 0)
			if err != nil {
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
		// 查一下是否存在返还的情况
		sql := `INSERT INTO custody_info 
		(uniqueId, dropType, equipInfo, holderGbId, holderServerId, returnTime, ownerGbId, ownerServerId) 
		VALUES (?, ?, ?, ?, ?, ?, ?, ?) on duplicate key update holderGbId=?, holderServerId=?`
		_, err := gss.app.db.Exec(sql, in.UniqueId, TYPE_RETURN_WAIT, in.EquipInfo, 0, 0,
			in.ReturnTime, in.OwnerId, in.OwnerServerId, 0, 0)
		if err != nil {
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

		sql := "SELECT dropGbId, takerGbId, dropType, equipInfo, collExpireTime, endTime, price, returnTime, redeemWaitTime, ownerGbId, ownerServerId FROM drop_info WHERE uniqueId=?"

		row := gss.app.db.QueryRow(sql, in.UniqueId)
		var dropGbId uint64
		var takerGbId uint64
		var dropType uint32
		var equipInfo []byte
		var collExpireTime int64
		var endTime int64
		var price uint32
		var returnTime int64
		var redeemWaitTime int64
		var ownerGbId uint64
		var ownerServerId uint32
		err := row.Scan(&dropGbId, &takerGbId, &dropType, &equipInfo, &collExpireTime, &endTime, &price, &returnTime, &redeemWaitTime, &ownerGbId, &ownerServerId)
		if err != nil {
			appLog.Error("Take: take drop info error: ", err.Error())
			gss.Client.(*gameServerService.GameServerClient).OnTake(&gameServerService.TakeResponse{
				UniqueId:       in.UniqueId,
				DropGbId:       dropGbId,
				EquipInfo:      equipInfo,
				EndTime:        endTime,
				Price:          price,
				RedeemWaitTime: redeemWaitTime,
				ReturnTime:     returnTime,
				Result:         gameServerService.DropResult_DropResult_NOT_FOUND,
			})
			return
		}

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
				RedeemWaitTime: redeemWaitTime,
				ReturnTime:     returnTime,
				Result:         gameServerService.DropResult_DropResult_HAS_TAKEN,
			})
			return
		}

		// 原先的returnTime等于0是首次掉落，等赎回期结束后，放入待归还
		if returnTime > 0 {
			// 被人拾取了，处理下转移关系
			sql = `INSERT INTO custody_info 
			(uniqueId, dropType, equipInfo, holderGbId, holderServerId, returnTime, ownerGbId, ownerServerId) 
			VALUES (?, ?, ?, ?, ?, ?, ?, ?) on duplicate key update holderGbId=?, holderServerId=?`
			_, err = gss.app.db.Exec(sql, in.UniqueId, TYPE_RETURN_WAIT, equipInfo, in.TakerGbId, in.ServerId,
				returnTime, ownerGbId, ownerServerId, in.TakerGbId, in.ServerId)
			if err != nil {
				gss.Client.(*gameServerService.GameServerClient).OnTake(&gameServerService.TakeResponse{
					UniqueId:       in.UniqueId,
					DropGbId:       dropGbId,
					EquipInfo:      equipInfo,
					EndTime:        endTime,
					Price:          price,
					RedeemWaitTime: redeemWaitTime,
					ReturnTime:     returnTime,
					Result:         gameServerService.DropResult_DropResult_STATE_ERROR,
				})
				return
			}
		}

		// 捡起自己掉落的
		if dropGbId == in.TakerGbId {
			gss._selfTake(in, equipInfo, endTime, price, redeemWaitTime, redeemWaitTime)
			return
		}

		redeemWaitTime = now + int64(in.RedeemWaitTime)
		// 捡起别人掉落的
		gss._otherTake(in, dropGbId, equipInfo, endTime, price, redeemWaitTime, returnTime, ownerGbId, ownerServerId)
	})
	return nil, nil
}

func (gss *GameServerService) _selfTake(in *gameServerService.TakeRequest, equipInfo []byte, endTime int64, price uint32, redeemWaitTime int64, returnTime int64) (*gameServerService.Void, error) {
	sql := "UPDATE drop_info set dropType=? WHERE uniqueId=? AND dropType=?"
	_, err := gss.app.db.Exec(sql, TYPE_TAKE_WAIT_DROP_GET, in.UniqueId, TYPE_DROP)
	if err != nil {
		appLog.Error("_selfTake: delete drop info error: ", err.Error())
		gss.Client.(*gameServerService.GameServerClient).OnTake(&gameServerService.TakeResponse{
			UniqueId:       in.UniqueId,
			DropGbId:       in.TakerGbId,
			EquipInfo:      equipInfo,
			EndTime:        endTime,
			Price:          price,
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
		RedeemWaitTime: redeemWaitTime,
		ReturnTime:     returnTime,
		Result:         gameServerService.DropResult_DropResult_SUCCESS,
	})
	return nil, nil
}

func (gss *GameServerService) _otherTake(in *gameServerService.TakeRequest, dropGbId uint64, equipInfo []byte, endTime int64, price uint32, redeemWaitTime int64, returnTime int64, ownerId uint64, ownerServerId uint32) (*gameServerService.Void, error) {
	sql := "UPDATE drop_info SET takerGbId=?, takerServerId=?, dropType=?, redeemWaitTime=? WHERE uniqueId=? AND dropType=?"
	_, err := gss.app.db.Exec(sql, in.TakerGbId, in.ServerId, TYPE_TAKE, redeemWaitTime, in.UniqueId, TYPE_DROP)
	if err != nil {
		appLog.Error("_otherTake: update drop info error: ", err.Error())
		gss.Client.(*gameServerService.GameServerClient).OnTake(&gameServerService.TakeResponse{
			UniqueId:       in.UniqueId,
			DropGbId:       dropGbId,
			EquipInfo:      equipInfo,
			EndTime:        endTime,
			Price:          price,
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
		sql := "SELECT serverId, uniqueId, dropGbId, takerGbId, takerServerId, dropType, endTime, returnTime, redeemWaitTime FROM drop_info WHERE uniqueId=?"
		row := gss.app.db.QueryRow(sql, in.UniqueId)
		var serverId uint32
		var uniqueId uint64
		var dropGbId uint64
		var takerGbId uint64
		var takerServerId uint32
		var dropType uint32
		var endTime int64
		var redeemWaitTime int64
		var returnTime int64
		err := row.Scan(&serverId, &uniqueId, &dropGbId, &takerGbId, &takerServerId, &dropType, &endTime, &returnTime, &redeemWaitTime)
		if err != nil {
			appLog.Error("GiveUp: give up drop info error: ", err.Error())
			gss.Client.(*gameServerService.GameServerClient).OnGiveUp(&gameServerService.GiveUpResponse{
				UniqueId: in.UniqueId,
				Result:   gameServerService.DropResult_DropResult_NOT_FOUND,
				Uuid:     in.Uuid,
			})
			return
		}

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

		sql = "UPDATE drop_info SET dropType=?, giveUpTime=? WHERE uniqueId=? AND dropType=?"
		_, err = gss.app.db.Exec(sql, TYPE_GIVEUP_WAIT_DROP_GET, now, in.UniqueId, TYPE_TAKE)
		if err != nil {
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

		sql = "UPDATE custody_info SET holderGbId=?, holderServerId=? WHERE uniqueId=?"
		_, err = gss.app.db.Exec(sql, dropGbId, serverId, in.UniqueId)
		if err != nil {
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
		sql := "SELECT dropGbId, serverId, takerGbId, dropType, collExpireTime, equipInfo, endTime, takerServerId, hasRedeemPrice, redeemWaitTime, returnTime, ownerGbId, ownerServerId FROM drop_info WHERE uniqueId=?"
		row := gss.app.db.QueryRow(sql, in.UniqueId)
		var dropGbId uint64
		var dropServerId uint32
		var takerGbId uint64
		var dropType uint32
		var collExpireTime int64
		var equipInfo []byte
		var endTime int64
		var takerServerId uint32
		var hasPrice bool
		var redeemWaitTime int64
		var returnTime int64
		var ownerGbId uint64
		var ownerServerId uint32
		err := row.Scan(&dropGbId, &dropServerId, &takerGbId, &dropType, &collExpireTime, &equipInfo, &endTime, &takerServerId, &hasPrice, &redeemWaitTime, &returnTime, &ownerGbId, &ownerServerId)
		if err != nil {
			appLog.Error("Redeem: drop info error: ", err.Error())
			gss.Client.(*gameServerService.GameServerClient).OnRedeem(&gameServerService.RedeemResponse{
				UniqueId: in.UniqueId,
				Result:   gameServerService.DropResult_DropResult_NOT_FOUND,
				Uuid:     in.Uuid,
			})
			return
		}

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

		sql = "UPDATE drop_info SET dropType=? WHERE uniqueId=? AND dropType=?"
		_, err = gss.app.db.Exec(sql, TYPE_REDEEM_WAIT_DROP_GET, in.UniqueId, dropType)
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
			sql = `INSERT INTO custody_info 
					(uniqueId, dropType, equipInfo, holderGbId, holderServerId, returnTime, ownerGbId, ownerServerId) 
					VALUES (?, ?, ?, ?, ?, ?, ?, ?) on duplicate key update holderGbId=?, holderServerId=?`
			_, err = gss.app.db.Exec(sql, in.UniqueId, TYPE_RETURN_WAIT, equipInfo, in.RedeemerGbId, in.ServerId,
				returnTime, ownerGbId, ownerServerId, in.RedeemerGbId, in.ServerId)
			if err != nil {
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
		sql := "SELECT bindMoney, money FROM reward_info WHERE uniqueId=?"
		row := gss.app.db.QueryRow(sql, in.UniqueId)
		var bindMoney uint32
		var money uint32
		err := row.Scan(&bindMoney, &money)
		if err != nil {
			appLog.Error("GetTakeReward: get take reward drop info error: ", err.Error())
			gss.Client.(*gameServerService.GameServerClient).OnGetTakeReward(&gameServerService.GetTakeRewardResponse{
				UniqueId: in.UniqueId,
				Result:   gameServerService.DropResult_DropResult_NOT_FOUND,
				Uuid:     in.Uuid,
			})
			return
		}

		sql = "DELETE FROM reward_info WHERE uniqueId=?"
		_, err = gss.app.db.Exec(sql, in.UniqueId)
		if err != nil {
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
		sql := "SELECT uniqueId, returnTime, takerGbId, dropType, endTime, collExpireTime, extraInfo, equipInfo, price, dropTime, redeemWaitTime, hasRedeemPrice FROM drop_info WHERE dropGbId=?"
		rows, err := gss.app.db.Query(sql, in.GbId)
		if err != nil {
			appLog.Error("GetDropInfo: get drop info error: ", err.Error())
			return
		}
		defer rows.Close()

		inDrop := make(map[uint64]bool)

		dropInfoList := make([]*gameServerService.DropInfo, 0)
		for rows.Next() {
			var uniqueId uint64
			var returnTime int64
			var takerGbId uint64
			var dropType uint32
			var endTime int64
			var collExpireTime int64
			var extraInfo []byte
			var equipInfo []byte
			var price uint32
			var dropTime int64
			var redeemWaitTime int64
			var hasPrice bool
			err = rows.Scan(&uniqueId, &returnTime, &takerGbId, &dropType, &endTime, &collExpireTime, &extraInfo, &equipInfo, &price, &dropTime, &redeemWaitTime, &hasPrice)
			if err != nil {
				appLog.Error("GetDropInfo: scan drop info error: ", err.Error())
				continue
			}
			// 进入赎回超时等待返还了，掉落列表就不用显示了
			if dropType == TYPE_REDEEM_EXPIRE_WAIT_TAKE_GET {
				continue
			}

			dropInfoList = append(dropInfoList, &gameServerService.DropInfo{
				UniqueId:       uniqueId,
				DropType:       dropType,
				EndTime:        endTime,
				CollExpireTime: collExpireTime,
				ExtraInfo:      extraInfo,
				EquipInfo:      equipInfo,
				Price:          price,
				DropTime:       dropTime,
				HasPrice:       hasPrice,
				ReturnTime:     returnTime,
				RedeemWaitTime: redeemWaitTime,
				TakerGbId:      takerGbId,
			})

			inDrop[uniqueId] = true
		}

		// go gss._deleteDropInfo(deleteDropInfoList)

		takerInfoList := make([]*gameServerService.TakerInfo, 0)
		sql = "SELECT uniqueId, dropGbId, price, endTime, dropType, equipInfo, redeemWaitTime, hasRedeemPrice, returnTime FROM drop_info WHERE takerGbId=?"
		rows, err = gss.app.db.Query(sql, in.GbId)
		if err != nil {
			appLog.Error("GetDropInfo: query taker info error: ", err.Error())
			return
		}
		defer rows.Close()

		// deleteTakerInfoList := make([][2]uint64, 0)

		for rows.Next() {
			var uniqueId uint64
			var dropGbId uint64
			var price uint32
			var endTime int64
			var dropType uint32
			var equipInfo []byte
			var redeemWaitTime int64
			var hasPrice bool
			var returnTime int64
			err = rows.Scan(&uniqueId, &dropGbId, &price, &endTime, &dropType, &equipInfo, &redeemWaitTime, &hasPrice, &returnTime)
			if err != nil {
				appLog.Error("GetDropInfo: scan taker info error: ", err.Error())
				continue
			}
			// 掉落中，放弃等待领取，赎回等待领取的就不用显示了
			if dropType == TYPE_DROP || dropType == TYPE_GIVEUP_WAIT_DROP_GET || dropType == TYPE_REDEEM_WAIT_DROP_GET {
				// 已经放弃的掉落信息就不发给玩家了
				continue
			}

			takerInfoList = append(takerInfoList, &gameServerService.TakerInfo{
				UniqueId:       uniqueId,
				Price:          price,
				EndTime:        endTime,
				DropType:       dropType,
				EquipInfo:      equipInfo,
				RedeemWaitTime: redeemWaitTime,
				HasPrice:       hasPrice,
				ReturnTime:     returnTime,
			})
		}

		rewardInfoList := make([]*gameServerService.RewardInfo, 0)
		sql = "SELECT uniqueId, equipInfo, bindMoney, money FROM reward_info WHERE gbId=?"
		rows, err = gss.app.db.Query(sql, in.GbId)
		if err != nil {
			appLog.Error("GetDropInfo: query reward info error: ", err.Error())
			return
		}
		defer rows.Close()

		for rows.Next() {
			var uniqueId uint64
			var equipInfo []byte
			var bindMoney uint64
			var money uint64
			err = rows.Scan(&uniqueId, &equipInfo, &bindMoney, &money)
			if err != nil {
				appLog.Error("GetDropInfo: scan reward info error: ", err.Error())
				continue
			}

			rewardInfoList = append(rewardInfoList, &gameServerService.RewardInfo{
				UniqueId:  uniqueId,
				EquipInfo: equipInfo,
				BindMoney: bindMoney,
				Money:     money,
			})
		}

		returnInfoList := make([]*gameServerService.ReturnInfo, 0)
		sql = "SELECT uniqueId, equipInfo, dropType, returnTime FROM custody_info WHERE ownerGbId=?"
		rows, err = gss.app.db.Query(sql, in.GbId)
		if err != nil {
			appLog.Error("GetDropInfo: query return info error: ", err.Error())
			return
		}
		defer rows.Close()

		for rows.Next() {
			var uniqueId uint64
			var equipInfo []byte
			var dropType uint32
			var returnTime int64
			err = rows.Scan(&uniqueId, &equipInfo, &dropType, &returnTime)
			if err != nil {
				appLog.Error("GetDropInfo: scan return info error: ", err.Error())
				continue
			}

			// 还在掉落中先不管
			if _, ok := inDrop[uniqueId]; ok {
				continue
			}

			returnInfoList = append(returnInfoList, &gameServerService.ReturnInfo{
				UniqueId:   uniqueId,
				EquipInfo:  equipInfo,
				DropType:   dropType,
				ReturnTime: returnTime,
			})
		}
		// go gss._deleteDropInfo(deleteTakerInfoList)

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
		sql := "SELECT dropGbId, dropType, serverId, equipInfo, endTime FROM drop_info WHERE uniqueId=?"
		row := gss.app.db.QueryRow(sql, in.UniqueId)
		var dropGbId uint64
		var dropType uint32
		var serverId uint32
		var equipInfo []byte
		var endTime int64
		err := row.Scan(&dropGbId, &dropType, &serverId, &equipInfo, &endTime)
		if err != nil {
			appLog.Error("SendRepairDropMail: send repair drop mail error: ", err.Error())
			return
		}

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

		sql := "UPDATE drop_info SET collExpireTime=? WHERE uniqueId=?"
		_, err := gss.app.db.Exec(sql, in.CollEndTime, in.UniqueId)
		if err != nil {
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
		sql := "SELECT dropGbId, dropType, serverId, redeemWaitTime, returnTime FROM drop_info WHERE uniqueId=?"
		row := gss.app.db.QueryRow(sql, in.UniqueId)
		var dropGbId uint64
		var dropType uint32
		var dropServerId uint32
		var redeemWaitTime int64
		var returnTime int64
		err := row.Scan(&dropGbId, &dropType, &dropServerId, &redeemWaitTime, &returnTime)
		if err != nil {
			appLog.Error("SetTakeEquipRedeemPrice: set task equip redeem price error: ", err.Error())
			gss.Client.(*gameServerService.GameServerClient).OnSetTakeEquipRedeemPrice(&gameServerService.SetTakeEquipRedeemPriceResponse{
				Uuid:     in.Uuid,
				GbId:     in.GbId,
				UniqueId: in.UniqueId,
				Price:    in.Price,
				Result:   gameServerService.DropResult_DropResult_NOT_FOUND,
			})
			return
		}

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

		sql = "UPDATE drop_info SET price=?, hasRedeemPrice=? WHERE uniqueId=? AND dropType=?"
		_, err = gss.app.db.Exec(sql, in.Price, 1, in.UniqueId, TYPE_TAKE)
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
		//appLog.Info("on checkDropReturnExpire:", in.Uuid, in.ServerId)
		sql := "SELECT uniqueId, holderGbId, holderServerId, ownerGbId, ownerServerId, returnTime FROM custody_info WHERE ownerServerId=? and dropType=? and returnTime < ? limit 200"
		// 延迟几秒过期，防止临界问题
		curTime := common.GetNowTime()
		limitTime := curTime + 5
		rows, err := gss.app.db.Query(sql, in.ServerId, TYPE_RETURN_WAIT, limitTime)
		if err != nil {
			appLog.Error("CheckDropReturnExpire: get custody info error: ", err.Error())
			return
		}
		defer rows.Close()

		holderReturnCacheDatas := make(map[uint64]*gameServerService.NotifyRemoveEquipCacheData, 0)
		ownerReturnCacheDatas := make(map[uint64]*gameServerService.NotifyDropCacheData, 0)
		returnUniqueIds := make([]uint64, 0)

		for rows.Next() {
			var uniqueId uint64
			var holderGbId uint64
			var holderServerId uint32
			var ownerGbId uint64
			var ownerServerId uint32
			var returnTime int64
			err = rows.Scan(&uniqueId, &holderGbId, &holderServerId, &ownerGbId, &ownerServerId, &returnTime)
			if err != nil {
				appLog.Error("CheckDropReturnExpire: scan custody info error: ", err.Error())
				continue
			}
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

		// 分批次处理
		if len(returnUniqueIds) > 0 {
			placeholders := strings.Repeat(",?", len(returnUniqueIds))[1:]
			query := fmt.Sprintf("select uniqueId, serverId, dropGbId, takerServerId, takerGbId, collExpireTime, collectionId from drop_info WHERE uniqueId IN (%s)", placeholders)

			args := make([]interface{}, 0, len(returnUniqueIds))
			for _, id := range returnUniqueIds {
				args = append(args, id)
			}

			rows, err := gss.app.db.Query(query, args...)
			if err != nil {
				appLog.Error("CheckDropReturnExpire: get drop info error: ", err.Error())
				return
			}
			defer rows.Close()
			// 1.先收集数据
			dropDatas := make(map[uint64]*gameServerService.NotifyDropCacheData)
			takerDatas := make(map[uint64]*gameServerService.NotifyDropCacheData)
			collectionDatas := make(map[uint32]*gameServerService.NotifyCollectionCacheData)
			for rows.Next() {
				var uniqueId uint64
				var dropServerId uint32
				var dropGbId uint64
				var takerServerId uint32
				var takerGbId uint64
				var collExpireTime int64
				var collectionId uint32
				err = rows.Scan(&uniqueId, &dropServerId, &dropGbId, &takerServerId, &takerGbId, &collExpireTime, &collectionId)
				if err != nil {
					appLog.Error("CheckDropReturnExpire: scan drop info error: ", err.Error())
					continue
				}

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

			// 2.删除数据
			query = fmt.Sprintf("DELETE from drop_info WHERE uniqueId IN (%s)", placeholders)

			args = make([]interface{}, 0, len(returnUniqueIds))
			for _, id := range returnUniqueIds {
				args = append(args, id)
			}

			if _, err := gss.app.db.Exec(query, args...); err != nil {
				appLog.Error("CheckDropReturnExpire: delete drop info error: ", err.Error())
				return
			}
			// 3.更新原主人的记录状态
			for i := 0; i < len(returnUniqueIds); i += 500 {
				end := i + 500
				if end > len(returnUniqueIds) {
					end = len(returnUniqueIds)
				}
				batch := returnUniqueIds[i:end]

				placeholders := strings.Repeat(",?", len(batch))[1:]
				query := fmt.Sprintf("UPDATE custody_info SET dropType = ? WHERE uniqueId IN (%s)", placeholders)

				args := make([]interface{}, 0, len(batch)+1)
				args = append(args, TYPE_RETURN_GET)
				for _, id := range batch {
					args = append(args, id)
				}

				if _, err := gss.app.db.Exec(query, args...); err != nil {
					appLog.Error("CheckDropReturnExpire: get update custody info error: ", err.Error())
					return
				}
			}

			// 4.给掉落者发送移除所有数据
			for gbId, data := range dropDatas {
				gss._notifyDropTypeChanges(data.ServerId, data.UniqueIds, data.DropTypes, nil, gbId)
			}
			// 5.给拾取者发送移除所有数据
			for gbId, data := range takerDatas {
				gss._notifyDropTypeChanges(data.ServerId, data.UniqueIds, data.DropTypes, nil, gbId)
			}
			// 6.给持有人发送移除装备
			for gbId, data := range holderReturnCacheDatas {
				gss._notifyRemoveEquip(data.ServerId, gbId, data.UniqueIds)
			}
			// 7.给原主人发送装备变更数据
			for gbId, data := range ownerReturnCacheDatas {
				gss._notifyDropTypeChanges(data.ServerId, data.UniqueIds, data.DropTypes, nil, gbId)
			}

			// 8.广播指定服, 清理创生物
			for serverId, collectionData := range collectionDatas {
				gss._notifyCleanCollections(serverId, collectionData.CollectionIds, collectionData.UniqueIds, collectionData.CollExpireTimes)
			}
		}

		gss.Client.(*gameServerService.GameServerClient).OnCheckDropReturnExpire(&gameServerService.CheckDropReturnExpireResponse{
			Uuid:     in.Uuid,
			ServerId: in.ServerId,
		})
	})
	return nil, nil
}

func (gss *GameServerService) GetBackEquip(in *gameServerService.GetBackEquipRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		appLog.Info("on get back equip:", in.UniqueId, in.GbId)
		gss.app.dropItemLock.Lock(in.UniqueId)
		defer gss.app.dropItemLock.Unlock(in.UniqueId)
		if in.DropType == TYPE_TAKE_WAIT_DROP_GET || in.DropType == TYPE_REDEEM_WAIT_DROP_GET || in.DropType == TYPE_GIVEUP_WAIT_DROP_GET {
			sql := "SELECT dropGbId, serverId, takerGbId, takerServerId, dropType, uniqueId, equipInfo, redeemWaitTime, returnTime, endTime FROM drop_info WHERE uniqueId=? and dropGbId=? and dropType=?"
			row := gss.app.db.QueryRow(sql, in.UniqueId, in.GbId, in.DropType)
			var dropGbId uint64
			var dropServerId uint32
			var takerGbId uint64
			var takerServerId uint32
			var dropType uint32
			var uniqueId uint64
			var equipInfo []byte
			var redeemWaitTime int64
			var returnTime int64
			var endTime int64

			err := row.Scan(&dropGbId, &dropServerId, &takerGbId, &takerServerId, &dropType, &uniqueId, &equipInfo, &redeemWaitTime, &returnTime, &endTime)
			if err != nil {
				appLog.Error("GetBackEquip: get back equip error: ", err.Error())
				gss.Client.(*gameServerService.GameServerClient).OnGetBackEquip(&gameServerService.GetBackEquipResponse{
					UniqueId:   in.UniqueId,
					DropType:   in.DropType,
					GbId:       in.GbId,
					EquipInfo:  equipInfo,
					ReturnTime: returnTime,
					Result:     gameServerService.DropResult_DropResult_NOT_FOUND,
				})
				return
			}

			now := common.GetNowTime()
			// 超过返还时间
			if returnTime > 0 && now >= returnTime {
				// 操作成功
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
			sql = "DELETE FROM drop_info WHERE uniqueId=? AND dropGbId=? AND dropType=?"
			_, err = gss.app.db.Exec(sql, in.UniqueId, in.GbId, in.DropType)
			if err != nil {
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
			sql := "SELECT dropGbId, serverId, takerGbId, takerServerId, dropType, uniqueId, equipInfo, redeemWaitTime, returnTime, endTime FROM drop_info WHERE uniqueId=? and takerGbId=? and dropType=?"
			row := gss.app.db.QueryRow(sql, in.UniqueId, in.GbId, in.DropType)
			var dropGbId uint64
			var dropServerId uint32
			var takerGbId uint64
			var takerServerId uint32
			var dropType uint32
			var uniqueId uint64
			var equipInfo []byte
			var redeemWaitTime int64
			var returnTime int64
			var endTime int64

			err := row.Scan(&dropGbId, &dropServerId, &takerGbId, &takerServerId, &dropType, &uniqueId, &equipInfo, &redeemWaitTime, &returnTime, &endTime)
			if err != nil {
				appLog.Error("GetBackEquip: get back equip error: ", err.Error())
				gss.Client.(*gameServerService.GameServerClient).OnGetBackEquip(&gameServerService.GetBackEquipResponse{
					UniqueId:   in.UniqueId,
					DropType:   in.DropType,
					GbId:       in.GbId,
					EquipInfo:  equipInfo,
					ReturnTime: returnTime,
					Result:     gameServerService.DropResult_DropResult_NOT_FOUND,
				})
				return
			}

			now := common.GetNowTime()
			// 超过返还时间
			if now >= returnTime {
				// 操作成功
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
			sql = "DELETE FROM drop_info WHERE uniqueId=? AND takerGbId=? AND dropType=?"
			_, err = gss.app.db.Exec(sql, in.UniqueId, in.GbId, in.DropType)
			if err != nil {
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
			sql := "select uniqueId, equipInfo FROM custody_info WHERE uniqueId=? and ownerGbId=? and dropType=?"
			row := gss.app.db.QueryRow(sql, in.UniqueId, in.GbId, in.DropType)
			var uniqueId uint64
			var equipInfo []byte

			err := row.Scan(&uniqueId, &equipInfo)
			if err != nil {
				appLog.Error("GetBackEquip: select custody info error: ", err.Error())
				gss.Client.(*gameServerService.GameServerClient).OnGetBackEquip(&gameServerService.GetBackEquipResponse{
					UniqueId:   in.UniqueId,
					DropType:   in.DropType,
					GbId:       in.GbId,
					EquipInfo:  equipInfo,
					ReturnTime: 0,
					Result:     gameServerService.DropResult_DropResult_NOT_FOUND,
				})
				return
			}

			sql = "DELETE FROM custody_info WHERE uniqueId=? AND ownerGbId=? AND dropType=?"
			_, err = gss.app.db.Exec(sql, in.UniqueId, in.GbId, in.DropType)
			if err != nil {
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
		sql := "SELECT dropGbId, takerGbId, takerServerId, dropType, serverId, redeemWaitTime, returnTime, price, equipInfo FROM drop_info WHERE uniqueId=?"
		row := gss.app.db.QueryRow(sql, in.UniqueId)
		var dropGbId uint64
		var takeGbId uint64
		var takerServerId uint32
		var dropType uint32
		var dropServerId uint32
		var redeemWaitTime int64
		var returnTime int64
		var price int64
		var equipInfo []byte
		err := row.Scan(&dropGbId, &takeGbId, &takerServerId, &dropType, &dropServerId, &redeemWaitTime, &returnTime, &price, &equipInfo)
		if err != nil {
			appLog.Error("SetDropEquipPayPrice: set drop equip pay price error: ", err.Error())
			gss.Client.(*gameServerService.GameServerClient).OnSetDropEquipPayPrice(&gameServerService.SetDropEquipPayPriceResponse{
				Uuid:     in.Uuid,
				GbId:     in.GbId,
				UniqueId: in.UniqueId,
				Price:    in.Price,
				Result:   gameServerService.DropResult_DropResult_NOT_FOUND,
			})
			return
		}

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
		sql = "UPDATE drop_info SET hasPayment=?, dropType=? WHERE uniqueId=? AND dropType=?"
		_, err = gss.app.db.Exec(sql, 1, TYPE_REDEEM_WAIT_DROP_GET, in.UniqueId, TYPE_TAKE)
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

		sql = "SELECT bindMoney, money FROM reward_info WHERE uniqueId=?"
		row = gss.app.db.QueryRow(sql, in.UniqueId)
		var oldBindMoney int64
		var oldMoney int64
		err = row.Scan(&oldBindMoney, &oldMoney)
		if err != nil {
			if err != dtSQL.ErrNoRows {
				appLog.Error("SetDropEquipPayPrice: get take reward drop info error: ", err.Error())
				gss.Client.(*gameServerService.GameServerClient).OnSetDropEquipPayPrice(&gameServerService.SetDropEquipPayPriceResponse{
					Uuid:     in.Uuid,
					GbId:     in.GbId,
					UniqueId: in.UniqueId,
					Price:    in.Price,
					Result:   gameServerService.DropResult_DropResult_STATE_ERROR,
				})
				return
			}
		}

		bindMoney := oldBindMoney + int64(in.BindMoney)
		money := oldMoney + int64(in.Money)
		if bindMoney > 0 || money > 0 {
			sql = `INSERT INTO reward_info (uniqueId, gbId, serverId, bindMoney, money, equipInfo) VALUES (?, ?, ?, ?, ?, ?) on duplicate key update bindMoney=?,money=?`
			_, err = gss.app.db.Exec(sql, in.UniqueId, takeGbId, takerServerId, bindMoney, money, equipInfo, bindMoney, money)
			if err != nil {
				appLog.Error("SetDropEquipPayPrice: insert take reward drop info error: ", err.Error())
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
