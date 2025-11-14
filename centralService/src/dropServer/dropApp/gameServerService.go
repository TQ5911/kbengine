package DropApp

import (
	"centralService/src/appLog"
	"centralService/src/common"
	gameServerService "centralService/src/dropServer/dropApp/gameServerService"
	"centralService/src/trpc"
	"errors"
	"fmt"
)

type GameServerService struct {
	*trpc.ServerEndPoint
	app      *DropApp
	serverId uint32
}

const (
	TYPE_DROP   = 1 // 掉落
	TYPE_TAKE   = 2 // 有人捡起了这个掉落
	TYPE_REDEEM = 3 // 主人赎回
	TYPE_GIVEUP = 4 // 捡起掉落的人主动放弃
)

const (
	NOTIFY_DROP_EXPIRE = 1 // 你掉落的装备过期了
	NOTIFY_TAKE_EXPIRE = 2 // 你捡起的装备过期了
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
	(serverId, uniqueId, dropGbId, dropType, endTime, equipInfo, dropTime, takerGbId, collExpireTime, price, extraInfo, giveUpTime, collectionId) 
	VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`

	_, err := gss.app.db.Exec(sql, in.ServerId, in.UniqueId, in.DropGbId, TYPE_DROP, in.EndTime, in.EquipInfo, in.DropTime, 0, in.CollExpireTime, in.Price, in.ExtraInfo, 0, in.CollectionId)
	if err != nil {
		appLog.Error("insert drop info error: ", err.Error())
		gss.Client.(*gameServerService.GameServerClient).OnDrop(&gameServerService.DropResponse{
			UniqueId: in.UniqueId,
			Success:  false,
		})
		return nil, nil
	}

	gss.Client.(*gameServerService.GameServerClient).OnDrop(&gameServerService.DropResponse{
		UniqueId: in.UniqueId,
		Success:  true,
	})
	return nil, nil
}

func (gss *GameServerService) _selfTake(in *gameServerService.TakeRequest, equipInfo []byte) (*gameServerService.Void, error) {
	sql := "DELETE FROM drop_info WHERE uniqueId=? AND dropType=?"
	_, err := gss.app.db.Exec(sql, in.UniqueId, TYPE_DROP)
	if err != nil {
		appLog.Error("delete drop info error: ", err.Error())
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

	gss.Client.(*gameServerService.GameServerClient).OnGetBackEquip(&gameServerService.GetBackEquipResponse{
		UniqueId:   in.UniqueId,
		DropGbId:   in.TakerGbId,
		EquipInfo:  equipInfo,
		IsSelfTake: true,
	})
	return nil, nil
}

func (gss *GameServerService) _otherTake(in *gameServerService.TakeRequest, dropGbId uint64, equipInfo []byte, endTime uint32, price uint32) (*gameServerService.Void, error) {
	sql := "UPDATE drop_info SET takerGbId=?, dropType=? WHERE uniqueId=? AND dropType=?"
	_, err := gss.app.db.Exec(sql, in.TakerGbId, TYPE_TAKE, in.UniqueId, TYPE_DROP)
	if err != nil {
		appLog.Error("update drop info error: ", err.Error())
		gss.Client.(*gameServerService.GameServerClient).OnTake(&gameServerService.TakeResponse{
			UniqueId: in.UniqueId,
			DropGbId: dropGbId,
			Result:   gameServerService.DropResult_DropResult_HAS_TAKEN,
		})
		return nil, nil
	}

	gss._notifyDropTypeChange(gss.serverId, in.UniqueId, TYPE_TAKE, dropGbId)

	gss.Client.(*gameServerService.GameServerClient).OnTake(&gameServerService.TakeResponse{
		UniqueId:  in.UniqueId,
		DropGbId:  dropGbId,
		Result:    gameServerService.DropResult_DropResult_SUCCESS,
		EquipInfo: equipInfo,
		EndTime:   endTime,
		Price:     price,
	})
	return nil, nil
}

func (gss *GameServerService) _notifyDropTypeChange(
	serverId uint32,
	uniqueId uint64,
	dropType uint32,
	gbId uint64,
) (*gameServerService.Void, error) {
	gameServer := gss.app.getGameServer(serverId)
	if gameServer == nil {
		appLog.Error("get game server error: ", serverId)
		return nil, nil
	}

	gameServer.Client.(*gameServerService.GameServerClient).OnDropTypeChange(&gameServerService.DropTypeChangeRequest{
		UniqueId: uniqueId,
		DropType: dropType,
		GbId:     gbId,
	})
	return nil, nil
}

func (gss *GameServerService) GiveUp(in *gameServerService.GiveUpRequest) (*gameServerService.Void, error) {
	appLog.Info("on give up:", in.UniqueId)
	sql := "SELECT serverId, uniqueId, dropGbId, takerGbId, dropType, endTime FROM drop_info WHERE uniqueId=?"
	row := gss.app.db.QueryRow(sql, in.UniqueId)
	var serverId uint32
	var uniqueId uint64
	var dropGbId uint64
	var takerGbId uint64
	var dropType uint32
	var endTime uint32
	err := row.Scan(&serverId, &uniqueId, &dropGbId, &takerGbId, &dropType, &endTime)
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
	if now > endTime {
		gss._removeDropInfo(in.UniqueId, TYPE_TAKE)
		gss.Client.(*gameServerService.GameServerClient).OnGiveUp(&gameServerService.GiveUpResponse{
			UniqueId: in.UniqueId,
			Result:   gameServerService.DropResult_DropResult_EXPIRE,
			Uuid:     in.Uuid,
		})
		return nil, nil
	}

	if dropType == TYPE_REDEEM {
		gss.Client.(*gameServerService.GameServerClient).OnGiveUp(&gameServerService.GiveUpResponse{
			UniqueId: in.UniqueId,
			Result:   gameServerService.DropResult_DropResult_OTHER_REDEEM,
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
	_, err = gss.app.db.Exec(sql, TYPE_GIVEUP, now, in.UniqueId, TYPE_TAKE)
	if err != nil {
		appLog.Error("update drop info error: ", err.Error())
		gss.Client.(*gameServerService.GameServerClient).OnGiveUp(&gameServerService.GiveUpResponse{
			UniqueId: in.UniqueId,
			Result:   gameServerService.DropResult_DropResult_STATE_ERROR,
			Uuid:     in.Uuid,
		})
		return nil, nil
	}

	gss._notifyDropTypeChange(serverId, uniqueId, TYPE_GIVEUP, dropGbId)

	gss.Client.(*gameServerService.GameServerClient).OnGiveUp(&gameServerService.GiveUpResponse{
		UniqueId: in.UniqueId,
		Result:   gameServerService.DropResult_DropResult_SUCCESS,
		Uuid:     in.Uuid,
		DropGbId: dropGbId,
	})

	return nil, nil
}

func (gss *GameServerService) Take(in *gameServerService.TakeRequest) (*gameServerService.Void, error) {
	appLog.Info("on take:", in.UniqueId, in.TakerGbId)

	sql := "SELECT dropGbId, takerGbId, dropType, equipInfo, collExpireTime, endTime, price FROM drop_info WHERE uniqueId=?"

	row := gss.app.db.QueryRow(sql, in.UniqueId)
	var dropGbId uint64
	var takerGbId uint64
	var dropType uint32
	var equipInfo []byte
	var collExpireTime uint32
	var endTime uint32
	var price uint32
	err := row.Scan(&dropGbId, &takerGbId, &dropType, &equipInfo, &collExpireTime, &endTime, &price)
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

	if now > collExpireTime {
		appLog.Info("drop expire:", in.UniqueId)
		gss.Client.(*gameServerService.GameServerClient).OnTake(&gameServerService.TakeResponse{
			UniqueId: in.UniqueId,
			DropGbId: dropGbId,
			Result:   gameServerService.DropResult_DropResult_EXPIRE,
		})
		return nil, nil
	}

	if dropType != TYPE_DROP {
		gss.Client.(*gameServerService.GameServerClient).OnTake(&gameServerService.TakeResponse{
			UniqueId: in.UniqueId,
			DropGbId: dropGbId,
			Result:   gameServerService.DropResult_DropResult_HAS_TAKEN,
		})
		return nil, nil
	}

	if dropGbId == in.TakerGbId {
		return gss._selfTake(in, equipInfo)
	}

	return gss._otherTake(in, dropGbId, equipInfo, endTime, price)
}

func (gss *GameServerService) Redeem(in *gameServerService.RedeemRequest) (*gameServerService.Void, error) {
	appLog.Info("on redeem:", in.UniqueId, in.RedeemerGbId)
	sql := "SELECT dropGbId, takerGbId, dropType, collExpireTime, equipInfo, endTime, serverId FROM drop_info WHERE uniqueId=?"
	row := gss.app.db.QueryRow(sql, in.UniqueId)
	var dropGbId uint64
	var takerGbId uint64
	var dropType uint32
	var collExpireTime uint32
	var equipInfo []byte
	var endTime uint32
	var serverId uint32
	err := row.Scan(&dropGbId, &takerGbId, &dropType, &collExpireTime, &equipInfo, &endTime, &serverId)
	if err != nil {
		appLog.Error("redeem drop info error: ", err.Error())
		gss.Client.(*gameServerService.GameServerClient).OnRedeem(&gameServerService.RedeemResponse{
			UniqueId: in.UniqueId,
			Result:   gameServerService.DropResult_DropResult_NOT_FOUND,
			Uuid:     in.Uuid,
		})
		return nil, nil
	}

	var now = common.GetNowTime()

	if now > endTime {
		gss._removeDropInfo(in.UniqueId, TYPE_DROP)
		gss.Client.(*gameServerService.GameServerClient).OnRedeem(&gameServerService.RedeemResponse{
			UniqueId: in.UniqueId,
			Result:   gameServerService.DropResult_DropResult_EXPIRE,
			Uuid:     in.Uuid,
		})
		return nil, nil
	}

	if dropType == TYPE_DROP && now > collExpireTime {
		sql = "DELETE FROM drop_info WHERE uniqueId=? AND dropType=?"
		_, err = gss.app.db.Exec(sql, in.UniqueId, dropType)
		if err != nil {
			appLog.Error("delete drop info error: ", err.Error())
			gss.Client.(*gameServerService.GameServerClient).OnRedeem(&gameServerService.RedeemResponse{
				UniqueId: in.UniqueId,
				Result:   gameServerService.DropResult_DropResult_STATE_ERROR,
				Uuid:     in.Uuid,
			})
			return nil, nil
		}
	} else if dropType == TYPE_TAKE {
		sql = "UPDATE drop_info SET dropType=? WHERE uniqueId=? AND dropType=?"
		_, err = gss.app.db.Exec(sql, TYPE_REDEEM, in.UniqueId, dropType)
		if err != nil {
			appLog.Error("update drop info error: ", err.Error())
			gss.Client.(*gameServerService.GameServerClient).OnRedeem(&gameServerService.RedeemResponse{
				UniqueId: in.UniqueId,
				Result:   gameServerService.DropResult_DropResult_STATE_ERROR,
				Uuid:     in.Uuid,
			})
			return nil, nil
		}

		// 通知接单者
		if takerGbId != 0 {
			gss._notifyDropTypeChange(serverId, in.UniqueId, TYPE_REDEEM, takerGbId)
		}
	} else if dropType == TYPE_GIVEUP {
		gss.Client.(*gameServerService.GameServerClient).OnRedeem(&gameServerService.RedeemResponse{
			UniqueId: in.UniqueId,
			Result:   gameServerService.DropResult_DropResult_OTHER_GIVEUP,
			Uuid:     in.Uuid,
		})
	} else {
		appLog.Error("drop type is not drop or take: ", dropType)
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

	gss.Client.(*gameServerService.GameServerClient).OnGetBackEquip(&gameServerService.GetBackEquipResponse{
		UniqueId:   in.UniqueId,
		DropGbId:   dropGbId,
		EquipInfo:  equipInfo,
		IsSelfTake: false,
	})

	return nil, nil
}

func (gss *GameServerService) ActiveTick(in *gameServerService.Void) (*gameServerService.Void, error) {
	_, err := gss.GetClientEndPoint().(*gameServerService.GameServerClient).ActiveTickCallback(&gameServerService.Void{})
	return nil, err
}

func (gss *GameServerService) GetTakeReward(in *gameServerService.GetTakeRewardRequest) (*gameServerService.Void, error) {
	appLog.Info("on get take reward:", in.UniqueId, in.TakerGbId)
	sql := "SELECT takerGbId, dropType, price FROM drop_info WHERE uniqueId=?"
	row := gss.app.db.QueryRow(sql, in.UniqueId)
	var takerGbId uint64
	var dropType uint32
	var price uint32
	err := row.Scan(&takerGbId, &dropType, &price)
	if err != nil {
		appLog.Error("get take reward drop info error: ", err.Error())
		gss.Client.(*gameServerService.GameServerClient).OnGetTakeReward(&gameServerService.GetTakeRewardResponse{
			UniqueId: in.UniqueId,
			Result:   gameServerService.DropResult_DropResult_NOT_FOUND,
			Uuid:     in.Uuid,
		})
		return nil, nil
	}

	if takerGbId != in.TakerGbId {
		gss.Client.(*gameServerService.GameServerClient).OnGetTakeReward(&gameServerService.GetTakeRewardResponse{
			UniqueId: in.UniqueId,
			Result:   gameServerService.DropResult_DropResult_NOT_TAKER,
			Uuid:     in.Uuid,
		})
		return nil, nil
	}

	if dropType != TYPE_REDEEM {
		gss.Client.(*gameServerService.GameServerClient).OnGetTakeReward(&gameServerService.GetTakeRewardResponse{
			UniqueId: in.UniqueId,
			Result:   gameServerService.DropResult_DropResult_STATE_ERROR,
			Uuid:     in.Uuid,
		})
		return nil, nil
	}

	sql = "DELETE FROM drop_info WHERE uniqueId=? AND dropType=?"
	_, err = gss.app.db.Exec(sql, in.UniqueId, dropType)
	if err != nil {
		appLog.Error("delete drop info error: ", err.Error())
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
	appLog.Info("on fetch drop equip:", in.UniqueId, in.GbId)
	sql := "SELECT equipInfo, endTime, dropGbId, dropType, giveUpTime FROM drop_info WHERE uniqueId=?"
	row := gss.app.db.QueryRow(sql, in.UniqueId)
	var equipInfo []byte
	var endTime uint32
	var dropGbId uint64
	var dropType uint32
	var giveUpTime uint32
	err := row.Scan(&equipInfo, &endTime, &dropGbId, &dropType, &giveUpTime)
	if err != nil {
		appLog.Error("fetch drop info error: ", err.Error())
		gss.Client.(*gameServerService.GameServerClient).OnFetchDropEquip(&gameServerService.FetchDropEquipResponse{
			UniqueId: in.UniqueId,
			Result:   gameServerService.DropResult_DropResult_NOT_FOUND,
			Uuid:     in.Uuid,
		})
		return nil, nil
	}

	if dropGbId != in.GbId {
		gss.Client.(*gameServerService.GameServerClient).OnFetchDropEquip(&gameServerService.FetchDropEquipResponse{
			UniqueId: in.UniqueId,
			Result:   gameServerService.DropResult_DropResult_NOT_OWNER,
			Uuid:     in.Uuid,
		})
		return nil, nil
	}

	var now = common.GetNowTime()

	if dropType != TYPE_GIVEUP {
		if now > endTime {
			gss._removeDropInfo(in.UniqueId, dropType)
			gss.Client.(*gameServerService.GameServerClient).OnFetchDropEquip(&gameServerService.FetchDropEquipResponse{
				UniqueId: in.UniqueId,
				Result:   gameServerService.DropResult_DropResult_EXPIRE,
				Uuid:     in.Uuid,
			})
		} else {
			gss.Client.(*gameServerService.GameServerClient).OnFetchDropEquip(&gameServerService.FetchDropEquipResponse{
				UniqueId: in.UniqueId,
				Result:   gameServerService.DropResult_DropResult_STATE_ERROR,
				Uuid:     in.Uuid,
			})
		}
		return nil, nil
	}

	gss._removeDropInfo(in.UniqueId, dropType)
	gss.Client.(*gameServerService.GameServerClient).OnFetchDropEquip(&gameServerService.FetchDropEquipResponse{
		UniqueId:   in.UniqueId,
		Result:     gameServerService.DropResult_DropResult_SUCCESS,
		EquipInfo:  equipInfo,
		GiveUpTime: giveUpTime,
		Uuid:       in.Uuid,
	})
	return nil, nil
}

func (gss *GameServerService) _deleteDropInfo(deleteDropInfoList [][2]uint64) {
	sql := "DELETE FROM drop_info WHERE uniqueId=? AND dropType=?"
	for _, dropInfo := range deleteDropInfoList {
		_, err := gss.app.db.Exec(sql, dropInfo[0], dropInfo[1])
		if err != nil {
			appLog.Error("delete drop info error: ", err.Error())
		}
	}
}

func (gss *GameServerService) GetDropInfo(in *gameServerService.GetDropInfoRequest) (*gameServerService.Void, error) {
	appLog.Info("on get drop info:", in.GbId)
	sql := "SELECT uniqueId, takerGbId, dropType, endTime, collExpireTime, extraInfo, equipInfo, price FROM drop_info WHERE dropGbId=?"
	rows, err := gss.app.db.Query(sql, in.GbId)
	if err != nil {
		appLog.Error("get drop info error: ", err.Error())
		return nil, nil
	}
	defer rows.Close()

	// now := common.GetNowTime()

	// deleteDropInfoList := make([][2]uint64, 0)

	dropInfoList := make([]*gameServerService.DropInfo, 0)
	for rows.Next() {
		var uniqueId uint64
		var takerGbId uint64
		var dropType uint32
		var endTime uint32
		var collExpireTime uint32
		var extraInfo []byte
		var equipInfo []byte
		var price uint32
		err = rows.Scan(&uniqueId, &takerGbId, &dropType, &endTime, &collExpireTime, &extraInfo, &equipInfo, &price)
		if err != nil {
			appLog.Error("scan drop info error: ", err.Error())
			continue
		}

		if dropType == TYPE_REDEEM {
			// 已经赎回的掉落信息就不发给玩家了
			continue
		}

		// if now > endTime {
		// 	if dropType == TYPE_DROP || dropType == TYPE_TAKE {
		// 		// 过期并且是掉落或者被捡起的掉落，需要删除
		// 		deleteDropInfoList = append(deleteDropInfoList, [2]uint64{uniqueId, uint64(dropType)})
		// 	}
		// }

		dropInfoList = append(dropInfoList, &gameServerService.DropInfo{
			UniqueId:       uniqueId,
			TakerGbId:      takerGbId,
			DropType:       dropType,
			EndTime:        endTime,
			CollExpireTime: collExpireTime,
			ExtraInfo:      extraInfo,
			EquipInfo:      equipInfo,
			Price:          price,
		})
	}

	// go gss._deleteDropInfo(deleteDropInfoList)

	takerInfoList := make([]*gameServerService.TakerInfo, 0)
	sql = "SELECT uniqueId, dropGbId, price, endTime, dropType, equipInfo FROM drop_info WHERE takerGbId=?"
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
		err = rows.Scan(&uniqueId, &dropGbId, &price, &endTime, &dropType, &equipInfo)
		if err != nil {
			appLog.Error("scan taker info error: ", err.Error())
			continue
		}

		if dropType == TYPE_GIVEUP {
			// 已经放弃的掉落信息就不发给玩家了
			continue
		}

		// if now > endTime {
		// 	if dropType == TYPE_DROP || dropType == TYPE_TAKE {
		// 		// 过期并且是掉落或者被捡起的掉落，需要删除
		// 		deleteTakerInfoList = append(deleteTakerInfoList, [2]uint64{uniqueId, uint64(dropType)})
		// 	}
		// }

		takerInfoList = append(takerInfoList, &gameServerService.TakerInfo{
			UniqueId:  uniqueId,
			DropGbId:  dropGbId,
			Price:     price,
			EndTime:   endTime,
			DropType:  dropType,
			EquipInfo: equipInfo,
		})
	}

	// go gss._deleteDropInfo(deleteTakerInfoList)

	gss.Client.(*gameServerService.GameServerClient).OnGetDropInfo(&gameServerService.GetDropInfoResponse{
		DropInfo:  dropInfoList,
		TakerInfo: takerInfoList,
		Uuid:      in.Uuid,
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

	if dropType != TYPE_DROP && dropType != TYPE_TAKE {
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

	if dropType != TYPE_DROP && dropType != TYPE_TAKE {
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

func (gss *GameServerService) _addDropNotify(notifyType uint32, gbId uint64, notifyTime uint32, equipInfo []byte, serverId uint32, uniqueId uint64) {
	sql := "INSERT INTO drop_notify (notifyType, gbId, notifyTime, equipInfo, uniqueId) VALUES (?, ?, ?, ?, ?)"
	_, err := gss.app.db.Exec(sql, notifyType, gbId, notifyTime, equipInfo, uniqueId)
	if err != nil {
		appLog.Error("add drop notify error: ", err.Error())
	}

	gameServer := gss.app.getGameServer(serverId)
	if gameServer == nil {
		appLog.Error("get game server error: ", serverId)
		return
	}

	gameServer.Client.(*gameServerService.GameServerClient).OnAddDropNotify(&gameServerService.AddDropNotify{
		GbId: gbId,
	})
}

func (gss *GameServerService) CheckDropExpire(in *gameServerService.CheckDropExpireRequest) (*gameServerService.Void, error) {
	appLog.Info("on check drop expire:", in.UniqueId, in.GbId)
	sql := "SELECT dropGbId, takerGbId, dropType, serverId, equipInfo, endTime FROM drop_info WHERE uniqueId=?"
	row := gss.app.db.QueryRow(sql, in.UniqueId)
	var dropGbId uint64
	var takerGbId uint64
	var dropType uint32
	var serverId uint32
	var equipInfo []byte
	var endTime uint32
	err := row.Scan(&dropGbId, &takerGbId, &dropType, &serverId, &equipInfo, &endTime)
	if err != nil {
		appLog.Error("check drop expire error: ", err.Error())
		gss.Client.(*gameServerService.GameServerClient).OnCheckDropExpire(&gameServerService.CheckDropExpireResponse{
			UniqueId: in.UniqueId,
			Uuid:     in.Uuid,
			Result:   gameServerService.DropResult_DropResult_NOT_FOUND,
		})
		return nil, nil
	}

	if !(dropType == TYPE_DROP || dropType == TYPE_TAKE) {
		gss.Client.(*gameServerService.GameServerClient).OnCheckDropExpire(&gameServerService.CheckDropExpireResponse{
			UniqueId: in.UniqueId,
			Uuid:     in.Uuid,
			Result:   gameServerService.DropResult_DropResult_STATE_ERROR,
		})
		return nil, nil
	}

	now := common.GetNowTime()
	if now < endTime {
		gss.Client.(*gameServerService.GameServerClient).OnCheckDropExpire(&gameServerService.CheckDropExpireResponse{
			UniqueId: in.UniqueId,
			Uuid:     in.Uuid,
			Result:   gameServerService.DropResult_DropResult_NOT_EXPIRE,
		})
		return nil, nil
	}

	sql = "DELETE FROM drop_info WHERE uniqueId=? AND dropType=?"
	_, err = gss.app.db.Exec(sql, in.UniqueId, dropType)
	if err != nil {
		appLog.Error("delete drop info error: ", err.Error())
		gss.Client.(*gameServerService.GameServerClient).OnCheckDropExpire(&gameServerService.CheckDropExpireResponse{
			UniqueId: in.UniqueId,
			Uuid:     in.Uuid,
			Result:   gameServerService.DropResult_DropResult_STATE_ERROR,
		})
		return nil, nil
	}

	if dropGbId == in.GbId {
		if takerGbId != 0 {
			gss._addDropNotify(NOTIFY_TAKE_EXPIRE, takerGbId, now, equipInfo, serverId, in.UniqueId)
		}
	} else if takerGbId == in.GbId {
		if dropGbId != 0 {
			gss._addDropNotify(NOTIFY_DROP_EXPIRE, dropGbId, now, equipInfo, serverId, in.UniqueId)
		}
	}

	gss.Client.(*gameServerService.GameServerClient).OnCheckDropExpire(&gameServerService.CheckDropExpireResponse{
		UniqueId: in.UniqueId,
		Uuid:     in.Uuid,
		Result:   gameServerService.DropResult_DropResult_SUCCESS,
	})
	return nil, nil
}

func (gss *GameServerService) GetDropNotifyList(in *gameServerService.GetDropNotifyListRequest) (*gameServerService.Void, error) {
	sql := "SELECT notifyType, notifyTime, equipInfo, uniqueId FROM drop_notify WHERE gbId=?"
	rows, err := gss.app.db.Query(sql, in.GbId)
	if err != nil {
		appLog.Error("query drop notify error: ", err.Error())
		gss.Client.(*gameServerService.GameServerClient).OnGetDropNotifyList(&gameServerService.GetDropNotifyListResponse{
			DropNotify: nil,
			Uuid:       in.Uuid,
		})
		return nil, nil
	}

	defer rows.Close()

	dropNotifyList := make([]*gameServerService.DropNotify, 0)
	maxNotifyTime := uint32(0)
	for rows.Next() {
		var notifyType uint32
		var notifyTime uint32
		var equipInfo []byte
		var uniqueId uint64
		err = rows.Scan(&notifyType, &notifyTime, &equipInfo, &uniqueId)
		if err != nil {
			appLog.Error("scan drop notify error: ", err.Error())
			continue
		}

		if notifyTime > maxNotifyTime {
			maxNotifyTime = notifyTime
		}

		dropNotifyList = append(dropNotifyList, &gameServerService.DropNotify{
			NotifyType: notifyType,
			NotifyTime: notifyTime,
			EquipInfo:  equipInfo,
			UniqueId:   uniqueId,
		})
	}

	if maxNotifyTime > 0 {
		sql = "DELETE FROM drop_notify WHERE gbId=? AND notifyTime<=?"
		_, err = gss.app.db.Exec(sql, in.GbId, maxNotifyTime)
		if err != nil {
			appLog.Error("delete drop notify error: ", err.Error())
		}
	}

	gss.Client.(*gameServerService.GameServerClient).OnGetDropNotifyList(&gameServerService.GetDropNotifyListResponse{
		DropNotify: dropNotifyList,
		Uuid:       in.Uuid,
	})

	return nil, nil
}
