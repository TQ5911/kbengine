package DropApp

import (
	"centralService/src/appLog"
	"centralService/src/common"
	gameServerService "centralService/src/dropServer/dropApp/gameServerService"
	"centralService/src/trpc"
	"errors"
	"fmt"
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
	appLog.Info("on drop:", in.ServerId)
	sql := `INSERT INTO drop_info 
	(serverId, uniqueId, dropGbId, dropType, endTime, equipInfo, dropTime, takerGbId, takerServerId, collExpireTime, price, 
	extraInfo, giveUpTime, collectionId, redeemTime, hasRedeemPrice, hasPayment, returnTime, ownerGbId, ownerServerId) 
	VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`

	_, err := gss.app.db.Exec(sql, in.ServerId, in.UniqueId, in.DropGbId, TYPE_DROP, in.EndTime, in.EquipInfo, in.DropTime, 0, 0,
		in.CollExpireTime, in.Price, in.ExtraInfo, 0, in.CollectionId, 0, 0, 0, in.ReturnTime, in.OwnerId, in.OwnerServerId)
	if err != nil {
		appLog.Error("insert drop info error: ", err.Error())
		gss.Client.(*gameServerService.GameServerClient).OnDrop(&gameServerService.DropResponse{
			UniqueId: in.UniqueId,
			Success:  false,
		})
		return nil, nil
	}
	// 自己掉落的就不用做关联了
	if in.DropGbId != in.OwnerId {
		// 更新一下返还情况
		sql = `INSERT INTO custody_info 
		(uniqueId, dropType, equipInfo, holderGbId, holderServerId, returnTime, ownerGbId, ownerServerId) 
		VALUES (?, ?, ?, ?, ?, ?, ?, ?) on duplicate key update holderGbId=?, holderServerId=?`
		_, err = gss.app.db.Exec(sql, in.UniqueId, TYPE_RETURN_WAIT, in.EquipInfo, in.CollectionId, 0, 0,
			in.ReturnTime, in.OwnerId, in.OwnerServerId, in.DropGbId, in.ServerId)
		if err != nil {
			appLog.Error("insert custody info error: ", err.Error())
			gss.Client.(*gameServerService.GameServerClient).OnDrop(&gameServerService.DropResponse{
				UniqueId: in.UniqueId,
				Success:  false,
			})
			return nil, nil
		}
	}

	gss.Client.(*gameServerService.GameServerClient).OnDrop(&gameServerService.DropResponse{
		UniqueId: in.UniqueId,
		Success:  true,
	})
	return nil, nil
}

func (gss *GameServerService) Custody(in *gameServerService.CustodyRequest) (*gameServerService.Void, error) {
	appLog.Info("on custody:", in.OwnerId)
	// 查一下是否存在返还的情况
	sql := `INSERT INTO custody_info 
		(uniqueId, dropType, equipInfo, holderGbId, holderServerId, returnTime, ownerGbId, ownerServerId) 
		VALUES (?, ?, ?, ?, ?, ?, ?, ?) on duplicate key update holderGbId=?, holderServerId=?`
	_, err := gss.app.db.Exec(sql, in.UniqueId, TYPE_RETURN_WAIT, in.EquipInfo, 0, 0,
		in.ReturnTime, in.OwnerId, in.OwnerServerId, 0, 0)
	if err != nil {
		appLog.Error("insert custody info error: ", err.Error())
		gss.Client.(*gameServerService.GameServerClient).OnCustody(&gameServerService.CustodyResponse{
			UniqueId: in.UniqueId,
			Success:  false,
		})
		return nil, nil
	}

	gss.Client.(*gameServerService.GameServerClient).OnCustody(&gameServerService.CustodyResponse{
		UniqueId: in.UniqueId,
		Success:  true,
	})
	// 通知拥有者更新状态
	gss._notifyCustodyEquip(in.OwnerServerId, in.OwnerId, in.UniqueId, uint32(in.DropType), in.EquipInfo, int64(in.ReturnTime))
	return nil, nil
}

func (gss *GameServerService) Take(in *gameServerService.TakeRequest) (*gameServerService.Void, error) {
	appLog.Info("on take:", in.UniqueId, in.TakerGbId)

	sql := "SELECT dropGbId, takerGbId, dropType, equipInfo, collExpireTime, endTime, price, returnTime FROM drop_info WHERE uniqueId=?"

	row := gss.app.db.QueryRow(sql, in.UniqueId)
	var dropGbId uint64
	var takerGbId uint64
	var dropType uint32
	var equipInfo []byte
	var collExpireTime int64
	var endTime uint32
	var price uint32
	var returnTime int64
	err := row.Scan(&dropGbId, &takerGbId, &dropType, &equipInfo, &collExpireTime, &endTime, &price, &returnTime)
	if err != nil {
		appLog.Error("take drop info error: ", err.Error())
		gss.Client.(*gameServerService.GameServerClient).OnTake(&gameServerService.TakeResponse{
			UniqueId: in.UniqueId,
			DropGbId: dropGbId,
			Result:   gameServerService.DropResult_DropResult_NOT_FOUND,
		})
		return nil, nil
	}

	var now = common.GetNowTime()
	// 大于采集物时间了，不能获取，或者超过返还时间了
	if now >= collExpireTime || now >= returnTime {
		appLog.Info("drop expire:", in.UniqueId)
		gss.Client.(*gameServerService.GameServerClient).OnTake(&gameServerService.TakeResponse{
			UniqueId: in.UniqueId,
			DropGbId: dropGbId,
			Result:   gameServerService.DropResult_DropResult_EXPIRE,
		})
		return nil, nil
	}
	// 非掉落状态，不允许拾取
	if dropType != TYPE_DROP {
		gss.Client.(*gameServerService.GameServerClient).OnTake(&gameServerService.TakeResponse{
			UniqueId: in.UniqueId,
			DropGbId: dropGbId,
			Result:   gameServerService.DropResult_DropResult_HAS_TAKEN,
		})
		return nil, nil
	}

	// 捡起自己掉落的
	if dropGbId == in.TakerGbId {
		return gss._selfTake(in, dropGbId, equipInfo)
	}

	redeemTime := now + int64(in.RedeemWaitTime)
	if collExpireTime > 0 {
		redeemTime = collExpireTime + int64(in.RedeemWaitTime)
	}
	// 捡起别人掉落的
	return gss._otherTake(in, dropGbId, equipInfo, endTime, price, redeemTime)
}

func (gss *GameServerService) _selfTake(in *gameServerService.TakeRequest, dropGbId uint64, equipInfo []byte) (*gameServerService.Void, error) {
	sql := "UPDATE drop_info SET dropType=? WHERE uniqueId=? AND dropType=?"
	_, err := gss.app.db.Exec(sql, TYPE_TAKE_WAIT_DROP_GET, in.UniqueId, TYPE_DROP)
	if err != nil {
		appLog.Error("update drop info error: ", err.Error())
		gss.Client.(*gameServerService.GameServerClient).OnTake(&gameServerService.TakeResponse{
			UniqueId: in.UniqueId,
			DropGbId: in.TakerGbId,
			Result:   gameServerService.DropResult_DropResult_HAS_TAKEN,
		})
		return nil, nil
	}

	gss.Client.(*gameServerService.GameServerClient).OnTake(&gameServerService.TakeResponse{
		UniqueId: in.UniqueId,
		DropGbId: in.TakerGbId,
		Result:   gameServerService.DropResult_DropResult_SUCCESS,
	})
	return nil, nil
}

func (gss *GameServerService) _otherTake(in *gameServerService.TakeRequest, dropGbId uint64, equipInfo []byte, endTime uint32, price uint32, redeemTime int64) (*gameServerService.Void, error) {
	sql := "UPDATE drop_info SET takerGbId=?, takerServerId=?, dropType=?, redeemTime=? WHERE uniqueId=? AND dropType=?"
	_, err := gss.app.db.Exec(sql, in.TakerGbId, in.ServerId, TYPE_TAKE, redeemTime, in.UniqueId, TYPE_DROP)
	if err != nil {
		appLog.Error("update drop info error: ", err.Error())
		gss.Client.(*gameServerService.GameServerClient).OnTake(&gameServerService.TakeResponse{
			UniqueId: in.UniqueId,
			DropGbId: dropGbId,
			Result:   gameServerService.DropResult_DropResult_HAS_TAKEN,
		})
		return nil, nil
	}

	gss._notifyDropTypeChange(gss.serverId, in.UniqueId, NOTIFY_TYPE_TAKE, dropGbId)

	gss.Client.(*gameServerService.GameServerClient).OnTake(&gameServerService.TakeResponse{
		UniqueId:       in.UniqueId,
		DropGbId:       dropGbId,
		Result:         gameServerService.DropResult_DropResult_SUCCESS,
		EquipInfo:      equipInfo,
		EndTime:        endTime,
		Price:          price,
		RedeemWaitTime: in.RedeemWaitTime,
	})

	return nil, nil
}

func (gss *GameServerService) _notifyDropTypeChange(
	serverId uint32,
	uniqueId uint64,
	dropType int32,
	gbId uint64,
) (*gameServerService.Void, error) {
	gameServer := gss.app.getGameServer(serverId)
	if gameServer == nil {
		appLog.Error("get game server error: ", serverId)
		return nil, nil
	}

	gameServer.Client.(*gameServerService.GameServerClient).OnDropTypeChange(&gameServerService.DropTypeChangeNotify{
		UniqueId:   []uint64{uniqueId},
		NotifyType: []int32{dropType},
		GbId:       gbId,
	})
	return nil, nil
}

func (gss *GameServerService) _notifyDropTypeChanges(
	serverId uint32,
	uniqueId []uint64,
	dropType []int32,
	gbId uint64,
) (*gameServerService.Void, error) {
	gameServer := gss.app.getGameServer(serverId)
	if gameServer == nil {
		appLog.Error("get game server error: ", serverId)
		return nil, nil
	}

	gameServer.Client.(*gameServerService.GameServerClient).OnDropTypeChange(&gameServerService.DropTypeChangeNotify{
		UniqueId:   uniqueId,
		NotifyType: dropType,
		GbId:       gbId,
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
		appLog.Error("get game server error: ", serverId)
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
		appLog.Error("get game server error: ", serverId)
		return nil, nil
	}

	gameServer.Client.(*gameServerService.GameServerClient).OnNotifyCleanCollection(&gameServerService.NotifyCleanCollections{
		CollectionIds:   collectionIds,
		UniqueIds:       uniqueIds,
		CollExpireTimes: collExpireTimes,
	})
	return nil, nil
}

func (gss *GameServerService) GiveUp(in *gameServerService.GiveUpRequest) (*gameServerService.Void, error) {
	appLog.Info("on give up:", in.UniqueId)
	sql := "SELECT serverId, uniqueId, dropGbId, takerGbId, takerServerId, dropType, endTime, returnTime, redeemTime FROM drop_info WHERE uniqueId=?"
	row := gss.app.db.QueryRow(sql, in.UniqueId)
	var serverId uint32
	var uniqueId uint64
	var dropGbId uint64
	var takerGbId uint64
	var takerServerId uint32
	var dropType uint32
	var endTime int64
	var redeemTime int64
	var returnTime int64
	err := row.Scan(&serverId, &uniqueId, &dropGbId, &takerGbId, &takerServerId, &dropType, &endTime, &returnTime, &redeemTime)
	if err != nil {
		appLog.Error("give up drop info error: ", err.Error())
		gss.Client.(*gameServerService.GameServerClient).OnGiveUp(&gameServerService.GiveUpResponse{
			UniqueId: in.UniqueId,
			Result:   gameServerService.DropResult_DropResult_NOT_FOUND,
			Uuid:     in.Uuid,
		})
		return nil, nil
	}

	var now = common.GetNowTime()
	// 检查是否大于赎回时间
	if now >= redeemTime || now >= returnTime {
		gss.Client.(*gameServerService.GameServerClient).OnGiveUp(&gameServerService.GiveUpResponse{
			UniqueId: in.UniqueId,
			Result:   gameServerService.DropResult_DropResult_EXPIRE,
			Uuid:     in.Uuid,
		})
		return nil, nil
	}

	if dropType != TYPE_TAKE {
		gss.Client.(*gameServerService.GameServerClient).OnGiveUp(&gameServerService.GiveUpResponse{
			UniqueId: in.UniqueId,
			Result:   gameServerService.DropResult_DropResult_STATE_ERROR,
			Uuid:     in.Uuid,
		})
		return nil, nil
	}

	if takerGbId != in.TakerGbId {
		gss.Client.(*gameServerService.GameServerClient).OnGiveUp(&gameServerService.GiveUpResponse{
			UniqueId: in.UniqueId,
			Result:   gameServerService.DropResult_DropResult_NOT_TAKER,
			Uuid:     in.Uuid,
		})
		return nil, nil
	}

	sql = "UPDATE drop_info SET dropType=?, giveUpTime=? WHERE uniqueId=? AND dropType=?"
	_, err = gss.app.db.Exec(sql, TYPE_GIVEUP_WAIT_DROP_GET, now, in.UniqueId, TYPE_TAKE_WAIT_DROP_GET)
	if err != nil {
		appLog.Error("update drop info error: ", err.Error())
		gss.Client.(*gameServerService.GameServerClient).OnGiveUp(&gameServerService.GiveUpResponse{
			UniqueId: in.UniqueId,
			Result:   gameServerService.DropResult_DropResult_STATE_ERROR,
			Uuid:     in.Uuid,
		})
		return nil, nil
	}

	gss._notifyDropTypeChange(serverId, uniqueId, NOTIFY_TYPE_GIVEUP_WAIT_DROP_GET, dropGbId)

	gss.Client.(*gameServerService.GameServerClient).OnGiveUp(&gameServerService.GiveUpResponse{
		UniqueId: in.UniqueId,
		Result:   gameServerService.DropResult_DropResult_SUCCESS,
		Uuid:     in.Uuid,
		DropGbId: dropGbId,
	})

	sql = "UPDATE custody_info SET holderGbId=?, holderServerId=? WHERE uniqueId=?"
	_, err = gss.app.db.Exec(sql, dropGbId, serverId, in.UniqueId)
	if err != nil {
		appLog.Error("update custody info error: ", err.Error())
		return nil, nil
	}
	return nil, nil
}

func (gss *GameServerService) Redeem(in *gameServerService.RedeemRequest) (*gameServerService.Void, error) {
	appLog.Info("on redeem:", in.UniqueId, in.RedeemerGbId)
	sql := "SELECT dropGbId, serverId, takerGbId, dropType, collExpireTime, equipInfo, endTime, takerServerId, hasRedeemPrice, redeemTime, returnTime FROM drop_info WHERE uniqueId=?"
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
	var redeemTime int64
	var returnTime int64
	err := row.Scan(&dropGbId, &dropServerId, &takerGbId, &dropType, &collExpireTime, &equipInfo, &endTime, &takerServerId, &hasPrice, &redeemTime, &returnTime)
	if err != nil {
		appLog.Error("redeem drop info error: ", err.Error())
		gss.Client.(*gameServerService.GameServerClient).OnRedeem(&gameServerService.RedeemResponse{
			UniqueId: in.UniqueId,
			Result:   gameServerService.DropResult_DropResult_NOT_FOUND,
			Uuid:     in.Uuid,
		})
		return nil, nil
	}
	// 检查是否设置过价格
	if !hasPrice {
		gss.Client.(*gameServerService.GameServerClient).OnRedeem(&gameServerService.RedeemResponse{
			UniqueId: in.UniqueId,
			Result:   gameServerService.DropResult_DropResult_REDEEM_NOT_SET_PRICE,
			Uuid:     in.Uuid,
		})
		return nil, nil
	}

	var now = common.GetNowTime()
	// 是否还在赎回期内, 在返还时间内
	if now >= redeemTime || now >= returnTime {
		gss.Client.(*gameServerService.GameServerClient).OnRedeem(&gameServerService.RedeemResponse{
			UniqueId: in.UniqueId,
			Result:   gameServerService.DropResult_DropResult_REDEEM_TIME_EXPIRED,
			Uuid:     in.Uuid,
		})
		return nil, nil
	}

	if !(dropType == TYPE_TAKE_WAIT_DROP_GET || dropType == TYPE_DROP) {
		appLog.Error("drop type is not drop or take: ", dropType)
		gss.Client.(*gameServerService.GameServerClient).OnRedeem(&gameServerService.RedeemResponse{
			UniqueId: in.UniqueId,
			Result:   gameServerService.DropResult_DropResult_STATE_ERROR,
			Uuid:     in.Uuid,
		})
		return nil, nil
	}
	sql = "UPDATE drop_info SET dropType=? WHERE uniqueId=? AND dropType=?"
	_, err = gss.app.db.Exec(sql, TYPE_REDEEM_WAIT_DROP_GET, in.UniqueId, dropType)
	if err != nil {
		appLog.Error("update drop info error: ", err.Error())
		gss.Client.(*gameServerService.GameServerClient).OnRedeem(&gameServerService.RedeemResponse{
			UniqueId: in.UniqueId,
			Result:   gameServerService.DropResult_DropResult_STATE_ERROR,
			Uuid:     in.Uuid,
		})
		return nil, nil
	}

	result := gameServerService.RedeemResponse{
		UniqueId: in.UniqueId,
		Result:   gameServerService.DropResult_DropResult_SUCCESS,
		Uuid:     in.Uuid,
	}
	gss.Client.(*gameServerService.GameServerClient).OnRedeem(&result)

	// 通知拾取者
	gss._notifyDropTypeChange(takerServerId, in.UniqueId, NOTIFY_REMOVE_TAKE, takerGbId)

	// 查一下是否存在返还的情况
	var count uint32
	sql = `select count(1) from custody_info where uniqueId = ?`
	row = gss.app.db.QueryRow(sql, in.UniqueId)
	err = row.Scan(&count)
	if err != nil {
		appLog.Error("query custody info error: ", err.Error())
		return nil, nil
	}
	// 更新一下持有者
	if count > 0 {
		sql := "UPDATE custody_info SET holderGbId=?, holderServerId=? WHERE uniqueId=?"
		_, err := gss.app.db.Exec(sql, dropGbId, dropServerId, in.UniqueId)
		if err != nil {
			appLog.Error("update custody info error: ", err.Error())
			return nil, nil
		}
	}
	return nil, nil
}

func (gss *GameServerService) ActiveTick(in *gameServerService.Void) (*gameServerService.Void, error) {
	_, err := gss.GetClientEndPoint().(*gameServerService.GameServerClient).ActiveTickCallback(&gameServerService.Void{})
	return nil, err
}

func (gss *GameServerService) GetTakeReward(in *gameServerService.GetTakeRewardRequest) (*gameServerService.Void, error) {
	appLog.Info("on get take reward:", in.UniqueId, in.TakerGbId)
	sql := "SELECT price FROM reward_info WHERE uniqueId=?"
	row := gss.app.db.QueryRow(sql, in.UniqueId)
	var price uint32
	err := row.Scan(&price)
	if err != nil {
		appLog.Error("get take reward drop info error: ", err.Error())
		gss.Client.(*gameServerService.GameServerClient).OnGetTakeReward(&gameServerService.GetTakeRewardResponse{
			UniqueId: in.UniqueId,
			Result:   gameServerService.DropResult_DropResult_NOT_FOUND,
			Uuid:     in.Uuid,
		})
		return nil, nil
	}

	sql = "DELETE FROM reward_info WHERE uniqueId=?"
	_, err = gss.app.db.Exec(sql, in.UniqueId)
	if err != nil {
		appLog.Error("delete reward info error: ", err.Error())
		gss.Client.(*gameServerService.GameServerClient).OnGetTakeReward(&gameServerService.GetTakeRewardResponse{
			UniqueId: in.UniqueId,
			Result:   gameServerService.DropResult_DropResult_STATE_ERROR,
			Uuid:     in.Uuid,
		})
		return nil, nil
	}

	gss.Client.(*gameServerService.GameServerClient).OnGetTakeReward(&gameServerService.GetTakeRewardResponse{
		UniqueId: in.UniqueId,
		Result:   gameServerService.DropResult_DropResult_SUCCESS,
		Price:    price,
		Uuid:     in.Uuid,
	})

	return nil, nil
}

func (gss *GameServerService) _removeDropInfo(uniqueId uint64, dropType uint32) {
	sql := "DELETE FROM drop_info WHERE uniqueId=? AND dropType=?"
	_, err := gss.app.db.Exec(sql, uniqueId, dropType)
	if err != nil {
		appLog.Error("delete drop info error: ", err.Error())
	}
}

// 取回别人放弃的我的装备
func (gss *GameServerService) FetchDropEquip(in *gameServerService.FetchDropEquipRequest) (*gameServerService.Void, error) {
	return nil, nil
}

func (gss *GameServerService) GetDropInfo(in *gameServerService.GetDropInfoRequest) (*gameServerService.Void, error) {
	appLog.Info("on get drop info:", in.GbId)
	sql := "SELECT uniqueId, returnTime, takerGbId, dropType, endTime, collExpireTime, extraInfo, equipInfo, price, dropTime, redeemTime FROM drop_info WHERE dropGbId=?"
	rows, err := gss.app.db.Query(sql, in.GbId)
	if err != nil {
		appLog.Error("get drop info error: ", err.Error())
		return nil, nil
	}
	defer rows.Close()

	dropInfoList := make([]*gameServerService.DropInfo, 0)
	for rows.Next() {
		var uniqueId uint64
		var returnTime int64
		var takerGbId uint64
		var dropType uint32
		var endTime uint32
		var collExpireTime uint32
		var extraInfo []byte
		var equipInfo []byte
		var price uint32
		var dropTime uint32
		var redeemTime int64
		err = rows.Scan(&uniqueId, &returnTime, &takerGbId, &dropType, &endTime, &collExpireTime, &extraInfo, &equipInfo, &price, &dropTime, &redeemTime)
		if err != nil {
			appLog.Error("scan drop info error: ", err.Error())
			continue
		}
		// 进入赎回超时等待返还了，掉落列表就不用显示了
		if dropType == TYPE_REDEEM_EXPIRE_WAIT_TAKE_GET {
			continue
		}

		dropInfoList = append(dropInfoList, &gameServerService.DropInfo{
			UniqueId:       uniqueId,
			TakerGbId:      takerGbId,
			DropType:       dropType,
			EndTime:        endTime,
			CollExpireTime: collExpireTime,
			ExtraInfo:      extraInfo,
			EquipInfo:      equipInfo,
			Price:          price,
			DropTime:       dropTime,
		})
	}

	// go gss._deleteDropInfo(deleteDropInfoList)

	takerInfoList := make([]*gameServerService.TakerInfo, 0)
	sql = "SELECT uniqueId, dropGbId, price, endTime, dropType, equipInfo, redeemTime, hasRedeemPrice FROM drop_info WHERE takerGbId=?"
	rows, err = gss.app.db.Query(sql, in.GbId)
	if err != nil {
		appLog.Error("query taker info error: ", err.Error())
		return nil, nil
	}
	defer rows.Close()

	// deleteTakerInfoList := make([][2]uint64, 0)

	for rows.Next() {
		var uniqueId uint64
		var dropGbId uint64
		var price uint32
		var endTime uint32
		var dropType uint32
		var equipInfo []byte
		var redeemTime uint64
		var hasPrice bool
		err = rows.Scan(&uniqueId, &dropGbId, &price, &endTime, &dropType, &equipInfo, &redeemTime, &hasPrice)
		if err != nil {
			appLog.Error("scan taker info error: ", err.Error())
			continue
		}
		// 掉落中，放弃等待领取，赎回等待领取的就不用显示了
		if dropType == TYPE_DROP || dropType == TYPE_GIVEUP_WAIT_DROP_GET || dropType == TYPE_REDEEM_WAIT_DROP_GET {
			// 已经放弃的掉落信息就不发给玩家了
			continue
		}

		takerInfoList = append(takerInfoList, &gameServerService.TakerInfo{
			UniqueId:       uniqueId,
			DropGbId:       dropGbId,
			Price:          price,
			EndTime:        endTime,
			DropType:       dropType,
			EquipInfo:      equipInfo,
			RedeemWaitTime: redeemTime,
			HasPrice:       hasPrice,
		})
	}

	rewardInfoList := make([]*gameServerService.RewardInfo, 0)
	sql = "SELECT uniqueId, equipInfo, price FROM reward_info WHERE gbId=?"
	rows, err = gss.app.db.Query(sql, in.GbId)
	if err != nil {
		appLog.Error("query reward info error: ", err.Error())
		return nil, nil
	}
	defer rows.Close()

	for rows.Next() {
		var uniqueId uint64
		var equipInfo []byte
		var price uint64
		err = rows.Scan(&uniqueId, &equipInfo, &price)
		if err != nil {
			appLog.Error("scan reward info error: ", err.Error())
			continue
		}

		rewardInfoList = append(rewardInfoList, &gameServerService.RewardInfo{
			UniqueId:  uniqueId,
			EquipInfo: equipInfo,
			Price:     price,
		})
	}

	returnInfoList := make([]*gameServerService.ReturnInfo, 0)
	sql = "SELECT uniqueId, equipInfo, returnTime FROM custody_info WHERE ownerGbId=?"
	rows, err = gss.app.db.Query(sql, in.GbId)
	if err != nil {
		appLog.Error("query return info error: ", err.Error())
		return nil, nil
	}
	defer rows.Close()

	for rows.Next() {
		var uniqueId uint64
		var equipInfo []byte
		var returnTime uint64
		err = rows.Scan(&uniqueId, &equipInfo, &returnTime)
		if err != nil {
			appLog.Error("scan return info error: ", err.Error())
			continue
		}

		returnInfoList = append(returnInfoList, &gameServerService.ReturnInfo{
			UniqueId:   uniqueId,
			EquipInfo:  equipInfo,
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
	return nil, nil
}

func (gss *GameServerService) _removeDropInfoNotifyTaker(
	serverId uint32,
	uniqueId uint64,
	gbId uint64,
) (*gameServerService.Void, error) {
	gameServer := gss.app.getGameServer(serverId)
	if gameServer == nil {
		appLog.Error("get game server error: ", serverId)
		return nil, nil
	}

	gameServer.Client.(*gameServerService.GameServerClient).OnRemoveDropInfoNotifyTaker(&gameServerService.RemoveDropInfoNotifyTaker{
		UniqueId: uniqueId,
		GbId:     gbId,
	})
	return nil, nil
}

func (gss *GameServerService) RemoveDropInfo(in *gameServerService.RemoveDropInfoRequest) (*gameServerService.Void, error) {
	appLog.Info("on remove drop info:", in.UniqueId, in.GbId)
	sql := "SELECT dropGbId, takerGbId, dropType, serverId, collectionId FROM drop_info WHERE uniqueId=?"
	row := gss.app.db.QueryRow(sql, in.UniqueId)
	var dropGbId uint64
	var takerGbId uint64
	var dropType uint32
	var serverId uint32
	var collectionId uint32
	err := row.Scan(&dropGbId, &takerGbId, &dropType, &serverId, &collectionId)
	if err != nil {
		appLog.Error("remove drop info error: ", err.Error())
		gss.Client.(*gameServerService.GameServerClient).OnRemoveDropInfo(&gameServerService.RemoveDropInfoResponse{
			UniqueId:     in.UniqueId,
			Result:       gameServerService.DropResult_DropResult_NOT_FOUND,
			Uuid:         in.Uuid,
			CollectionId: collectionId,
		})
		return nil, nil
	}

	if dropGbId != in.GbId {
		gss.Client.(*gameServerService.GameServerClient).OnRemoveDropInfo(&gameServerService.RemoveDropInfoResponse{
			UniqueId:     in.UniqueId,
			Result:       gameServerService.DropResult_DropResult_NOT_OWNER,
			Uuid:         in.Uuid,
			CollectionId: collectionId,
		})
		return nil, nil
	}

	if dropType != TYPE_DROP && dropType != TYPE_TAKE_WAIT_DROP_GET {
		gss.Client.(*gameServerService.GameServerClient).OnRemoveDropInfo(&gameServerService.RemoveDropInfoResponse{
			UniqueId:     in.UniqueId,
			Result:       gameServerService.DropResult_DropResult_STATE_ERROR,
			Uuid:         in.Uuid,
			CollectionId: collectionId,
		})
		return nil, nil
	}

	gss._removeDropInfo(in.UniqueId, dropType)

	if takerGbId != 0 {
		gss._removeDropInfoNotifyTaker(serverId, in.UniqueId, takerGbId)
	}

	gss.Client.(*gameServerService.GameServerClient).OnRemoveDropInfo(&gameServerService.RemoveDropInfoResponse{
		UniqueId:     in.UniqueId,
		Result:       gameServerService.DropResult_DropResult_SUCCESS,
		Uuid:         in.Uuid,
		CollectionId: collectionId,
	})

	return nil, nil
}

func (gss *GameServerService) SendRepairDropMail(in *gameServerService.SendRepairDropMailRequest) (*gameServerService.Void, error) {
	appLog.Info("on send repair drop mail:", in.UniqueId)
	sql := "SELECT dropGbId, dropType, serverId, equipInfo, endTime FROM drop_info WHERE uniqueId=?"
	row := gss.app.db.QueryRow(sql, in.UniqueId)
	var dropGbId uint64
	var dropType uint32
	var serverId uint32
	var equipInfo []byte
	var endTime uint32
	err := row.Scan(&dropGbId, &dropType, &serverId, &equipInfo, &endTime)
	if err != nil {
		appLog.Error("send repair drop mail error: ", err.Error())
		return nil, nil
	}

	gameServer := gss.app.getGameServer(serverId)
	if gameServer == nil {
		appLog.Error("get game server error: ", serverId)
		return nil, nil
	}

	if dropType != TYPE_DROP && dropType != TYPE_TAKE_WAIT_DROP_GET {
		appLog.Error("drop type error: ", dropType)
		return nil, nil
	}

	gameServer.Client.(*gameServerService.GameServerClient).OnSendRepairDropMail(&gameServerService.SendRepairDropMailResponse{
		UniqueId:  in.UniqueId,
		GbId:      dropGbId,
		EquipInfo: equipInfo,
		EndTime:   endTime,
	})
	return nil, nil
}

func (gss *GameServerService) UpdateCollEndTime(in *gameServerService.UpdateCollEndTimeRequest) (*gameServerService.Void, error) {
	appLog.Info("on update coll end time:", in.UniqueId, in.CollEndTime)
	sql := "UPDATE drop_info SET collExpireTime=? WHERE uniqueId=?"
	_, err := gss.app.db.Exec(sql, in.CollEndTime, in.UniqueId)
	if err != nil {
		appLog.Error("update coll end time error: ", err.Error())
		return nil, nil
	}
	return nil, nil
}

func (gss *GameServerService) CheckDropExpire(in *gameServerService.CheckDropExpireRequest) (*gameServerService.Void, error) {
	appLog.Info("on check drop expire:", in.UniqueId, in.GbId)
	sql := "SELECT uniqueId, ownerServerId, ownerGbId, serverId, dropGbId, takerGbId, dropType, equipInfo, endTime, returnTime FROM drop_info WHERE uniqueId=?"
	row := gss.app.db.QueryRow(sql, in.UniqueId)
	var uniqueId uint64
	var ownerServerId uint32
	var ownerGbId uint64
	var dropServerId uint32
	var dropGbId uint64
	var takerGbId uint64
	var dropType uint32
	var equipInfo []byte
	var endTime int64
	var returnTime int64
	err := row.Scan(&uniqueId, &ownerServerId, &ownerGbId, &dropServerId, &dropGbId, &takerGbId, &dropType, &equipInfo, &endTime, &returnTime)
	if err != nil {
		appLog.Error("check drop expire error: ", err.Error())
		gss.Client.(*gameServerService.GameServerClient).OnCheckDropExpire(&gameServerService.CheckDropExpireResponse{
			UniqueId: in.UniqueId,
			Uuid:     in.Uuid,
			Result:   gameServerService.DropResult_DropResult_NOT_FOUND,
		})
		return nil, nil
	}

	// 掉落状态
	if dropType != TYPE_DROP {
		gss.Client.(*gameServerService.GameServerClient).OnCheckDropExpire(&gameServerService.CheckDropExpireResponse{
			UniqueId: in.UniqueId,
			Uuid:     in.Uuid,
			Result:   gameServerService.DropResult_DropResult_STATE_ERROR,
		})
		return nil, nil
	}

	now := common.GetNowTime()
	// 超过返还时间，更新下状态
	if now < endTime {
		gss.Client.(*gameServerService.GameServerClient).OnCheckDropExpire(&gameServerService.CheckDropExpireResponse{
			UniqueId: in.UniqueId,
			Uuid:     in.Uuid,
			Result:   gameServerService.DropResult_DropResult_NOT_EXPIRE,
		})
		return nil, nil
	}
	sql = "DELETE FROM drop_info WHERE uniqueId=? AND dropType=?"
	_, err = gss.app.db.Exec(sql, TYPE_RETURN_GET, in.UniqueId, TYPE_TAKE_WAIT_DROP_GET)
	if err != nil {
		appLog.Error("delete drop info error: ", err.Error())
		gss.Client.(*gameServerService.GameServerClient).OnCheckDropExpire(&gameServerService.CheckDropExpireResponse{
			UniqueId: in.UniqueId,
			Uuid:     in.Uuid,
			Result:   gameServerService.DropResult_DropResult_STATE_ERROR,
		})
		return nil, nil
	}
	gss.Client.(*gameServerService.GameServerClient).OnCheckDropExpire(&gameServerService.CheckDropExpireResponse{
		Uuid:     in.Uuid,
		UniqueId: in.UniqueId,
		Result:   gameServerService.DropResult_DropResult_SUCCESS,
	})
	// 通知掉落者移除
	gss._notifyDropTypeChange(dropServerId, uniqueId, NOTIFY_REMOVE_DROP, dropGbId)
	return nil, nil
}

func (gss *GameServerService) SetTakeEquipRedeemPrice(in *gameServerService.SetTakeEquipRedeemPriceRequest) (*gameServerService.Void, error) {
	sql := "SELECT dropGbId, dropType, serverId, redeemTime, returnTime FROM drop_info WHERE uniqueId=?"
	row := gss.app.db.QueryRow(sql, in.UniqueId)
	var dropGbId uint64
	var dropType uint32
	var serverId uint32
	var redeemTime int64
	var returnTime int64
	err := row.Scan(&dropGbId, &dropType, &serverId, &redeemTime)
	if err != nil {
		appLog.Error("SetTakeEquipRedeemPrice, set task equip redeem price error: ", err.Error())
		gss.Client.(*gameServerService.GameServerClient).OnSetTakeEquipRedeemPrice(&gameServerService.SetTakeEquipRedeemPriceResponse{
			Uuid:     in.Uuid,
			GbId:     in.GbId,
			UniqueId: in.UniqueId,
			Price:    in.Price,
			Result:   gameServerService.DropResult_DropResult_NOT_FOUND,
		})
		return nil, nil
	}

	if dropType != TYPE_TAKE_WAIT_DROP_GET {
		gss.Client.(*gameServerService.GameServerClient).OnSetTakeEquipRedeemPrice(&gameServerService.SetTakeEquipRedeemPriceResponse{
			Uuid:     in.Uuid,
			GbId:     in.GbId,
			UniqueId: in.UniqueId,
			Price:    in.Price,
			Result:   gameServerService.DropResult_DropResult_STATE_ERROR,
		})
		return nil, nil
	}

	now := common.GetNowTime()
	if now >= redeemTime || now >= returnTime {
		gss.Client.(*gameServerService.GameServerClient).OnSetTakeEquipRedeemPrice(&gameServerService.SetTakeEquipRedeemPriceResponse{
			Uuid:     in.Uuid,
			GbId:     in.GbId,
			UniqueId: in.UniqueId,
			Price:    in.Price,
			Result:   gameServerService.DropResult_DropResult_SET_REDEEM_PRICE_EXPIRE,
		})
		return nil, nil
	}

	sql = "UPDATE drop_info SET price=?, hasRedeemPrice=? WHERE uniqueId=? AND dropType=?"
	_, err = gss.app.db.Exec(sql, in.Price, 1, in.UniqueId, TYPE_TAKE_WAIT_DROP_GET)
	if err != nil {
		appLog.Error("SetTakeEquipRedeemPrice, update drop info error: ", err.Error())
		gss.Client.(*gameServerService.GameServerClient).OnSetTakeEquipRedeemPrice(&gameServerService.SetTakeEquipRedeemPriceResponse{
			Uuid:     in.Uuid,
			GbId:     in.GbId,
			UniqueId: in.UniqueId,
			Price:    in.Price,
			Result:   gameServerService.DropResult_DropResult_OTHER_REDEEM,
		})
		return nil, nil
	}

	gss.Client.(*gameServerService.GameServerClient).OnSetTakeEquipRedeemPrice(&gameServerService.SetTakeEquipRedeemPriceResponse{
		Uuid:     in.Uuid,
		GbId:     in.GbId,
		UniqueId: in.UniqueId,
		Price:    in.Price,
		Result:   gameServerService.DropResult_DropResult_SUCCESS,
	})

	return nil, nil
}

func (gss *GameServerService) CheckRedeemExpire(in *gameServerService.CheckRedeemExpireRequest) (*gameServerService.Void, error) {
	appLog.Info("on check redeem expire:", in.UniqueId, in.GbId)
	sql := "SELECT dropGbId, serverId, takerGbId, takerServerId, dropType, uniqueId, equipInfo, redeemTime, returnTime, endTime FROM drop_info WHERE uniqueId=?"
	row := gss.app.db.QueryRow(sql, in.UniqueId)
	var ownerServerId uint32
	var ownerGbId uint64
	var dropGbId uint64
	var dropServerId uint32
	var takerGbId uint64
	var takerServerId uint32
	var dropType uint32
	var uniqueId uint64
	var equipInfo []byte
	var redeemTime int64
	var returnTime int64
	var endTime uint32

	err := row.Scan(&ownerServerId, &ownerGbId, &dropGbId, &dropServerId, &takerGbId, &takerServerId, &dropType, &uniqueId, &equipInfo, &redeemTime, &returnTime, &endTime)
	if err != nil {
		appLog.Error("check redeem expire error: ", err.Error())
		gss.Client.(*gameServerService.GameServerClient).OnCheckRedeemExpire(&gameServerService.CheckRedeemExpireResponse{
			Uuid:     in.Uuid,
			UniqueId: in.UniqueId,
			Result:   gameServerService.DropResult_DropResult_NOT_FOUND,
		})
		return nil, nil
	}
	// 不在拾取状态
	if dropType != TYPE_TAKE_WAIT_DROP_GET {
		gss.Client.(*gameServerService.GameServerClient).OnCheckRedeemExpire(&gameServerService.CheckRedeemExpireResponse{
			UniqueId: in.UniqueId,
			Uuid:     in.Uuid,
			Result:   gameServerService.DropResult_DropResult_STATE_ERROR,
		})
		return nil, nil
	}

	now := common.GetNowTime()
	// 超过返还时间
	if now >= returnTime {
		// 操作成功
		gss.Client.(*gameServerService.GameServerClient).OnCheckRedeemExpire(&gameServerService.CheckRedeemExpireResponse{
			UniqueId: in.UniqueId,
			Uuid:     in.Uuid,
			Result:   gameServerService.DropResult_DropResult_SUCCESS,
		})
		return nil, nil
	}
	// 检查下赎回时间，不到不处理
	if now < redeemTime {
		gss.Client.(*gameServerService.GameServerClient).OnCheckRedeemExpire(&gameServerService.CheckRedeemExpireResponse{
			UniqueId: in.UniqueId,
			Uuid:     in.Uuid,
			Result:   gameServerService.DropResult_DropResult_REDEEM_TIME_NOT_EXPIRED,
		})
		return nil, nil
	}
	// 合法的赎回超时
	if dropType != TYPE_REDEEM_EXPIRE_WAIT_TAKE_GET {
		sql = "UPDATE drop_info SET dropType=? WHERE uniqueId=?"
		_, err = gss.app.db.Exec(sql, TYPE_REDEEM_EXPIRE_WAIT_TAKE_GET, in.UniqueId)
		if err != nil {
			appLog.Error("update drop info error: ", err.Error())
			gss.Client.(*gameServerService.GameServerClient).OnCheckRedeemExpire(&gameServerService.CheckRedeemExpireResponse{
				UniqueId: in.UniqueId,
				Uuid:     in.Uuid,
				Result:   gameServerService.DropResult_DropResult_STATE_ERROR,
			})
			return nil, nil
		}
		gss.Client.(*gameServerService.GameServerClient).OnCheckRedeemExpire(&gameServerService.CheckRedeemExpireResponse{
			Uuid:     in.Uuid,
			UniqueId: in.UniqueId,
			Result:   gameServerService.DropResult_DropResult_SUCCESS,
		})
		// 通知拾取者更新状态
		gss._notifyDropTypeChange(takerServerId, uniqueId, NOTIFY_TYPE_REDEEM_EXPIRE_WAIT_TAKE_GET, takerGbId)
		// 通知掉落者更新状态
		gss._notifyDropTypeChange(dropServerId, uniqueId, NOTIFY_REMOVE_DROP, dropGbId)
		return nil, nil
	}

	return nil, nil
}

func (gss *GameServerService) CheckDropReturnExpire(in *gameServerService.CheckDropReturnExpireRequest) (*gameServerService.Void, error) {
	appLog.Info("on checkDropReturnExpire:", in.Uuid, in.ServerId)
	sql := "SELECT uniqueId, holderGbId, holderServerId, ownerGbId, ownerServerId, returnTime FROM custody_info WHERE ownerServerId=? and dropType=? and returnTime > ? limit 500"
	// 延迟几秒过期，防止临界问题
	curTime := common.GetNowTime()
	limitTime := curTime + 3
	rows, err := gss.app.db.Query(sql, in.ServerId, TYPE_RETURN_WAIT, limitTime)
	if err != nil {
		appLog.Error("get custody info error: ", err.Error())
		return nil, nil
	}
	defer rows.Close()
	holderReturnCacheDatas := make(map[uint64]*gameServerService.NotifyDropCacheData, 0)
	ownerReturnCacheDatas := make(map[uint64]*gameServerService.NotifyDropCacheData, 0)
	dropUniqueIds := make([]uint64, 0)
	for rows.Next() {
		var uniqueId uint64
		var holderGbId uint64
		var holderServerId uint32
		var ownerGbId uint64
		var ownerServerId uint32
		var returnTime int64
		err = rows.Scan(&uniqueId, &holderGbId, &holderServerId, &ownerGbId, &ownerServerId, &returnTime)
		if err != nil {
			appLog.Error("scan custody info error: ", err.Error())
			continue
		}
		dropUniqueIds = append(dropUniqueIds, uniqueId)
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

		holderReturnCacheData, ok := holderReturnCacheDatas[ownerGbId]
		if !ok {
			holderReturnCacheData = &gameServerService.NotifyDropCacheData{
				UniqueIds: make([]uint64, 0),
				DropTypes: make([]int32, 0),
			}
			holderReturnCacheDatas[ownerGbId] = holderReturnCacheData
		}
		holderReturnCacheData.ServerId = ownerServerId
		holderReturnCacheData.UniqueIds = append(holderReturnCacheData.UniqueIds, uniqueId)
		holderReturnCacheData.DropTypes = append(holderReturnCacheData.DropTypes, NOTIFY_TYPE_RETURN_GET)
	}

	// 分批次处理
	if len(dropUniqueIds) > 0 {
		placeholders := strings.Repeat(",?", len(dropUniqueIds))[1:]
		query := fmt.Sprintf("select uniqueId, serverId, dropGbId, takerServerId, takerGbId, collExpireTime, collectionId from drop_info WHERE uniqueId IN (%s)", placeholders)

		args := make([]interface{}, 0, len(dropUniqueIds))
		for _, id := range dropUniqueIds {
			args = append(args, id)
		}

		rows, err := gss.app.db.Query(query, args...)
		if err != nil {
			appLog.Error("get drop info error: ", err.Error())
			return nil, nil
		}
		defer rows.Close()
		// 1.先收集数据
		datas := make(map[uint64]*gameServerService.NotifyDropCacheData)
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
				appLog.Error("scan drop info error: ", err.Error())
				continue
			}
			data, ok := datas[dropGbId]
			if !ok {
				data = &gameServerService.NotifyDropCacheData{
					UniqueIds: make([]uint64, 0),
					DropTypes: make([]int32, 0),
				}
				datas[dropGbId] = data
			}
			data.ServerId = dropServerId
			data.UniqueIds = append(data.UniqueIds, uniqueId)
			data.DropTypes = append(data.DropTypes, NOTIFY_REMOVE_ALL)

			data, ok = datas[takerGbId]
			if !ok {
				data = &gameServerService.NotifyDropCacheData{
					UniqueIds: make([]uint64, 0),
					DropTypes: make([]int32, 0),
				}
				datas[dropGbId] = data
			}
			data.ServerId = takerServerId
			data.UniqueIds = append(data.UniqueIds, uniqueId)
			data.DropTypes = append(data.DropTypes, NOTIFY_REMOVE_ALL)

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

		args = make([]interface{}, 0, len(dropUniqueIds))
		for _, id := range dropUniqueIds {
			args = append(args, id)
		}

		if _, err := gss.app.db.Exec(query, args...); err != nil {
			appLog.Error("delete drop info error: ", err.Error())
			return nil, nil
		}
		// 3.更新原主人的记录状态
		for i := 0; i < len(dropUniqueIds); i += 500 {
			end := i + 500
			if end > len(dropUniqueIds) {
				end = len(dropUniqueIds)
			}
			batch := dropUniqueIds[i:end]

			placeholders := strings.Repeat(",?", len(batch))[1:]
			query := fmt.Sprintf("UPDATE custody_info SET dropType = ? WHERE uniqueId IN (%s)", placeholders)

			args := make([]interface{}, 0, len(batch)+1)
			args = append(args, TYPE_RETURN_GET)
			for _, id := range batch {
				args = append(args, id)
			}

			if _, err := gss.app.db.Exec(query, args...); err != nil {
				appLog.Error("get update custody info error: ", err.Error())
				return nil, nil
			}
		}

		// 4.给掉落者和拾取者发送数据
		for gbId, data := range datas {
			gss._notifyDropTypeChanges(data.ServerId, data.UniqueIds, data.DropTypes, gbId)
		}
		// 5.给原主人发送数据
		for gbId, data := range ownerReturnCacheDatas {
			gss._notifyDropTypeChanges(data.ServerId, data.UniqueIds, data.DropTypes, gbId)
		}
		// 6.给持有人发送数据
		for gbId, data := range holderReturnCacheDatas {
			gss._notifyDropTypeChanges(data.ServerId, data.UniqueIds, data.DropTypes, gbId)
		}

		// 7.广播指定服, 清理创生物
		for serverId, collectionData := range collectionDatas {
			gss._notifyCleanCollections(serverId, collectionData.CollectionIds, collectionData.UniqueIds, collectionData.CollExpireTimes)
		}
	}

	gss.Client.(*gameServerService.GameServerClient).OnCheckDropReturnExpire(&gameServerService.CheckDropReturnExpireResponse{
		Uuid:     in.Uuid,
		ServerId: in.ServerId,
	})

	return nil, nil
}

func (gss *GameServerService) GetBackEquip(in *gameServerService.GetBackEquipRequest) (*gameServerService.Void, error) {
	appLog.Info("on get back equip:", in.UniqueId, in.GbId)
	var equipInfo []byte
	if in.DropType == TYPE_TAKE_WAIT_DROP_GET || in.DropType == TYPE_REDEEM_WAIT_DROP_GET || in.DropType == TYPE_GIVEUP_WAIT_DROP_GET {
		sql := "SELECT dropGbId, serverId, takerGbId, takerServerId, dropType, uniqueId, equipInfo, redeemTime, returnTime, endTime FROM drop_info WHERE uniqueId=? and dropGbId=? and dropType=?"
		row := gss.app.db.QueryRow(sql, in.UniqueId, in.GbId, in.DropType)
		var ownerServerId uint32
		var ownerGbId uint64
		var dropGbId uint64
		var dropServerId uint32
		var takerGbId uint64
		var takerServerId uint32
		var dropType uint32
		var uniqueId uint64
		var equipInfo []byte
		var redeemTime int64
		var returnTime int64
		var endTime int64

		err := row.Scan(&ownerServerId, &ownerGbId, &dropGbId, &dropServerId, &takerGbId, &takerServerId, &dropType, &uniqueId, &equipInfo, &redeemTime, &returnTime, &endTime)
		if err != nil {
			appLog.Error("get back equip error: ", err.Error())
			gss.Client.(*gameServerService.GameServerClient).OnGetBackEquip(&gameServerService.GetBackEquipResponse{
				UniqueId:  in.UniqueId,
				DropType:  in.DropType,
				GbId:      in.GbId,
				EquipInfo: equipInfo,
				Result:    gameServerService.DropResult_DropResult_NOT_FOUND,
			})
			return nil, nil
		}

		now := common.GetNowTime()
		// 超过返还时间
		if now >= returnTime || now >= endTime {
			// 操作成功
			gss.Client.(*gameServerService.GameServerClient).OnGetBackEquip(&gameServerService.GetBackEquipResponse{
				UniqueId:  in.UniqueId,
				DropType:  in.DropType,
				GbId:      in.GbId,
				EquipInfo: equipInfo,
				Result:    gameServerService.DropResult_DropResult_GET_BACK_EXPIRED,
			})
			return nil, nil
		}
		sql = "DELETE FROM drop_info WHERE uniqueId=? AND dropGbId=? AND dropType=?"
		_, err = gss.app.db.Exec(sql, TYPE_RETURN_GET, in.UniqueId, in.GbId, in.DropType)
		if err != nil {
			appLog.Error("delete drop info error: ", err.Error())
			gss.Client.(*gameServerService.GameServerClient).OnGetBackEquip(&gameServerService.GetBackEquipResponse{
				UniqueId:  in.UniqueId,
				DropType:  in.DropType,
				GbId:      in.GbId,
				EquipInfo: equipInfo,
				Result:    gameServerService.DropResult_DropResult_GET_BACK_EXPIRED,
			})
			return nil, nil
		}
		gss.Client.(*gameServerService.GameServerClient).OnGetBackEquip(&gameServerService.GetBackEquipResponse{
			UniqueId:  in.UniqueId,
			DropType:  in.DropType,
			EquipInfo: equipInfo,
			GbId:      in.GbId,
			Result:    gameServerService.DropResult_DropResult_SUCCESS,
		})
	} else if in.DropType == TYPE_REDEEM_EXPIRE_WAIT_TAKE_GET {
		sql := "SELECT dropGbId, serverId, takerGbId, takerServerId, dropType, uniqueId, equipInfo, redeemTime, returnTime, endTime FROM drop_info WHERE uniqueId=? and takerGbId=? and dropType=?"
		row := gss.app.db.QueryRow(sql, in.UniqueId, in.GbId, in.DropType)
		var ownerServerId uint32
		var ownerGbId uint64
		var dropGbId uint64
		var dropServerId uint32
		var takerGbId uint64
		var takerServerId uint32
		var dropType uint32
		var uniqueId uint64
		var equipInfo []byte
		var redeemTime int64
		var returnTime int64
		var endTime int64

		err := row.Scan(&ownerServerId, &ownerGbId, &dropGbId, &dropServerId, &takerGbId, &takerServerId, &dropType, &uniqueId, &equipInfo, &redeemTime, &returnTime, &endTime)
		if err != nil {
			appLog.Error("get back equip error: ", err.Error())
			gss.Client.(*gameServerService.GameServerClient).OnGetBackEquip(&gameServerService.GetBackEquipResponse{
				UniqueId:  in.UniqueId,
				DropType:  in.DropType,
				GbId:      in.GbId,
				EquipInfo: equipInfo,
				Result:    gameServerService.DropResult_DropResult_NOT_FOUND,
			})
			return nil, nil
		}

		now := common.GetNowTime()
		// 超过返还时间
		if now >= returnTime || now >= endTime {
			// 操作成功
			gss.Client.(*gameServerService.GameServerClient).OnGetBackEquip(&gameServerService.GetBackEquipResponse{
				UniqueId:  in.UniqueId,
				DropType:  in.DropType,
				GbId:      in.GbId,
				EquipInfo: equipInfo,
				Result:    gameServerService.DropResult_DropResult_GET_BACK_EXPIRED,
			})
			return nil, nil
		}
		sql = "DELETE FROM drop_info WHERE uniqueId=? AND takerGbId=? AND dropType=?"
		_, err = gss.app.db.Exec(sql, TYPE_RETURN_GET, in.UniqueId, in.GbId, in.DropType)
		if err != nil {
			appLog.Error("delete drop info error: ", err.Error())
			gss.Client.(*gameServerService.GameServerClient).OnGetBackEquip(&gameServerService.GetBackEquipResponse{
				UniqueId:  in.UniqueId,
				DropType:  in.DropType,
				GbId:      in.GbId,
				EquipInfo: equipInfo,
				Result:    gameServerService.DropResult_DropResult_GET_BACK_EXPIRED,
			})
			return nil, nil
		}
		gss.Client.(*gameServerService.GameServerClient).OnGetBackEquip(&gameServerService.GetBackEquipResponse{
			UniqueId:  in.UniqueId,
			DropType:  in.DropType,
			EquipInfo: equipInfo,
			GbId:      in.GbId,
			Result:    gameServerService.DropResult_DropResult_SUCCESS,
		})
	} else if in.DropType == TYPE_RETURN_GET {
		sql := "SELECT uniqueId, serverId, takerGbId, takerServerId, dropType, uniqueId, equipInfo, redeemTime, returnTime, endTime FROM drop_info WHERE uniqueId=? and dropGbId=? and dropType=?"
		row := gss.app.db.QueryRow(sql, in.UniqueId, in.GbId, in.DropType)
		var ownerServerId uint32
		var ownerGbId uint64
		var dropGbId uint64
		var dropServerId uint32
		var takerGbId uint64
		var takerServerId uint32
		var dropType uint32
		var uniqueId uint64
		var equipInfo []byte
		var redeemTime int64
		var returnTime int64
		var endTime int64

		err := row.Scan(&ownerServerId, &ownerGbId, &dropGbId, &dropServerId, &takerGbId, &takerServerId, &dropType, &uniqueId, &equipInfo, &redeemTime, &returnTime, &endTime)
		if err != nil {
			appLog.Error("get back equip error: ", err.Error())
			gss.Client.(*gameServerService.GameServerClient).OnGetBackEquip(&gameServerService.GetBackEquipResponse{
				UniqueId:  in.UniqueId,
				DropType:  in.DropType,
				GbId:      in.GbId,
				EquipInfo: equipInfo,
				Result:    gameServerService.DropResult_DropResult_NOT_FOUND,
			})
			return nil, nil
		}
		sql = "DELETE FROM drop_info WHERE uniqueId=? AND takerGbId=? AND dropType=?"
		_, err = gss.app.db.Exec(sql, TYPE_RETURN_GET, in.UniqueId, in.GbId, in.DropType)
		if err != nil {
			appLog.Error("delete drop info error: ", err.Error())
			gss.Client.(*gameServerService.GameServerClient).OnGetBackEquip(&gameServerService.GetBackEquipResponse{
				UniqueId:  in.UniqueId,
				DropType:  in.DropType,
				GbId:      in.GbId,
				EquipInfo: equipInfo,
				Result:    gameServerService.DropResult_DropResult_GET_BACK_EXPIRED,
			})
			return nil, nil
		}

		sql = "SELECT equipInfo, holderGbId, holderServerId FROM custody_info WHERE uniqueId=? and ownerServerId=? and dropType=?"
		row = gss.app.db.QueryRow(sql, in.UniqueId, in.ServerId, in.DropType)
		var returnBackEquip []byte
		var holderGbId uint64
		var holderServerId uint32
		err = row.Scan(&equipInfo, &returnBackEquip, &holderGbId, &holderServerId)
		if err != nil {
			appLog.Error("get back equip error: ", err.Error())
			gss.Client.(*gameServerService.GameServerClient).OnGetBackEquip(&gameServerService.GetBackEquipResponse{
				UniqueId:  in.UniqueId,
				DropType:  in.DropType,
				GbId:      in.GbId,
				EquipInfo: equipInfo,
				Result:    gameServerService.DropResult_DropResult_NOT_FOUND,
			})
			return nil, nil
		}
		sql = "DELETE FROM custody_info WHERE uniqueId=? AND ownerGbId=? AND dropType=?"
		_, err = gss.app.db.Exec(sql, in.UniqueId, in.GbId, in.DropType)
		if err != nil {
			appLog.Error("delete drop info error: ", err.Error())
			gss.Client.(*gameServerService.GameServerClient).OnGetBackEquip(&gameServerService.GetBackEquipResponse{
				UniqueId:  in.UniqueId,
				DropType:  in.DropType,
				GbId:      in.GbId,
				EquipInfo: equipInfo,
				Result:    gameServerService.DropResult_DropResult_GET_BACK_EXPIRED,
			})
			return nil, nil
		}
		gss.Client.(*gameServerService.GameServerClient).OnGetBackEquip(&gameServerService.GetBackEquipResponse{
			UniqueId:  in.UniqueId,
			DropType:  in.DropType,
			EquipInfo: equipInfo,
			GbId:      in.GbId,
			Result:    gameServerService.DropResult_DropResult_SUCCESS,
		})
	} else {
		appLog.Error("get back equip drop type error: ", in.DropType, in.GbId, in.DropType)
		gss.Client.(*gameServerService.GameServerClient).OnGetBackEquip(&gameServerService.GetBackEquipResponse{
			UniqueId:  in.UniqueId,
			DropType:  in.DropType,
			EquipInfo: equipInfo,
			GbId:      in.GbId,
			Result:    gameServerService.DropResult_DropResult_GET_BACK_TYPE_ERROR,
		})
		return nil, nil
	}
	return nil, nil
}

func (gss *GameServerService) SetDropEquipPayPrice(in *gameServerService.SetDropEquipPayPriceRequest) (*gameServerService.Void, error) {
	sql := "SELECT dropGbId, dropType, serverId, redeemTime, returnTime FROM drop_info WHERE uniqueId=?"
	row := gss.app.db.QueryRow(sql, in.UniqueId)
	var dropGbId uint64
	var dropType uint32
	var serverId uint32
	var redeemTime int64
	var returnTime int64
	err := row.Scan(&dropGbId, &dropType, &serverId, &redeemTime)
	if err != nil {
		appLog.Error("SetDropEquipPayPrice, set drop equip pay price error: ", err.Error())
		gss.Client.(*gameServerService.GameServerClient).OnSetDropEquipPayPrice(&gameServerService.SetDropEquipPayPriceResponse{
			Uuid:     in.Uuid,
			GbId:     in.GbId,
			UniqueId: in.UniqueId,
			Price:    in.Price,
			Result:   gameServerService.DropResult_DropResult_NOT_FOUND,
		})
		return nil, nil
	}

	if dropType != TYPE_TAKE_WAIT_DROP_GET {
		gss.Client.(*gameServerService.GameServerClient).OnSetDropEquipPayPrice(&gameServerService.SetDropEquipPayPriceResponse{
			Uuid:     in.Uuid,
			GbId:     in.GbId,
			UniqueId: in.UniqueId,
			Price:    in.Price,
			Result:   gameServerService.DropResult_DropResult_STATE_ERROR,
		})
		return nil, nil
	}

	now := common.GetNowTime()
	if now >= redeemTime || now >= returnTime {
		gss.Client.(*gameServerService.GameServerClient).OnSetDropEquipPayPrice(&gameServerService.SetDropEquipPayPriceResponse{
			Uuid:     in.Uuid,
			GbId:     in.GbId,
			UniqueId: in.UniqueId,
			Price:    in.Price,
			Result:   gameServerService.DropResult_DropResult_SET_REDEEM_PRICE_EXPIRE,
		})
		return nil, nil
	}

	sql = "UPDATE drop_info SET hasPayment=? WHERE uniqueId=? AND dropType=?"
	_, err = gss.app.db.Exec(sql, 1, in.UniqueId, TYPE_TAKE_WAIT_DROP_GET)
	if err != nil {
		appLog.Error("SetDropEquipPayPrice, update drop info error: ", err.Error())
		gss.Client.(*gameServerService.GameServerClient).OnSetDropEquipPayPrice(&gameServerService.SetDropEquipPayPriceResponse{
			Uuid:     in.Uuid,
			GbId:     in.GbId,
			UniqueId: in.UniqueId,
			Price:    in.Price,
			Result:   gameServerService.DropResult_DropResult_OTHER_REDEEM,
		})
		return nil, nil
	}

	gss.Client.(*gameServerService.GameServerClient).OnSetDropEquipPayPrice(&gameServerService.SetDropEquipPayPriceResponse{
		Uuid:     in.Uuid,
		GbId:     in.GbId,
		UniqueId: in.UniqueId,
		Price:    in.Price,
		Result:   gameServerService.DropResult_DropResult_SUCCESS,
	})

	return nil, nil
}
