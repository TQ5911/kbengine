package LeaseApp

import (
	"centralService/src/appLog"
	gameServerService "centralService/src/leaseServer/leaseApp/gameServerService"
	"centralService/src/trpc"
	"sync"

	"golang.org/x/time/rate"
)

// 给游戏服务器提供的接口
type GameServerService struct {
	*trpc.ServerEndPoint           // trpc 服务端端点基类
	app                  *LeaseApp // 所属 LeaseApp 实例
	serverId             uint32    // 游戏服 serverId
	compId               uint32    // 游戏服 compId（组件 ID）
	status               int8      // 连接状态：1=已连接 0=已断开
	limiter              *rate.Limiter
}

func newRateLimiter() *rate.Limiter {
	r := LeaseConfig.RateLimit.R
	b := LeaseConfig.RateLimit.B
	if r <= 0 {
		r = 50
	}
	if b <= 0 {
		b = 80
	}
	return rate.NewLimiter(rate.Limit(r), b)
}

const (
	_                          = iota
	ServiceStatus_Connected    // 与游戏服已建立连接
	ServiceStatus_Disconnected // 与游戏服连接已断开
)

var (
	replyAddItemPrepareRespPool = sync.Pool{
		New: func() interface{} { return &gameServerService.LeaseAddItemPrepareResp{} },
	}
	replyAddItemCommitRespPool = sync.Pool{
		New: func() interface{} { return &gameServerService.LeaseAddItemCommitResp{} },
	}
	replyLeaseItemPrepareRespPool = sync.Pool{
		New: func() interface{} { return &gameServerService.LeaseItemPrepareResp{} },
	}
	replyLeaseItemCommitRespPool = sync.Pool{
		New: func() interface{} { return &gameServerService.LeaseItemCommitResp{} },
	}
	replyCancelItemRespPool = sync.Pool{
		New: func() interface{} { return &gameServerService.LeaseCancelItemResp{} },
	}
	replyShopSummaryRespPool = sync.Pool{
		New: func() interface{} { return &gameServerService.LeaseShopSummaryResp{} },
	}
	replyShopItemsRespPool = sync.Pool{
		New: func() interface{} { return &gameServerService.LeaseShopItemsResp{} },
	}
	replyMySaleListRespPool = sync.Pool{
		New: func() interface{} { return &gameServerService.LeaseMySaleListResp{} },
	}
	leaseGiveItemReqPool = sync.Pool{
		New: func() interface{} { return &gameServerService.LeaseGiveItemReq{} },
	}

	leaseAddIncomeReqPool = sync.Pool{
		New: func() interface{} { return &gameServerService.LeaseAddIncomeReq{} },
	}
)

func (gs *GameServerService) OnLoseConnection() {
	gs.status = ServiceStatus_Disconnected
	gs.app.unRegisterServer(gs)
}

func (gs *GameServerService) ActiveTick(in *gameServerService.Void) (*gameServerService.Void, error) {
	return &gameServerService.Void{}, nil
}

func (gs *GameServerService) RegisterServer(in *gameServerService.ServerInfoMessage) (*gameServerService.Void, error) {
	err := gs.app.doRegisterServer(uint32(in.ServerId), uint32(in.CompId), in.ServerName, gs)
	if err != nil {
		return nil, err
	}
	gs.serverId = uint32(in.ServerId)
	gs.compId = uint32(in.CompId)
	return nil, nil
}

func (gs *GameServerService) AddItemPrepare(in *gameServerService.LeaseAddItemPrepareReq) (*gameServerService.Void, error) {
	if !gs.limiter.Allow() {
		appLog.Warnw("AddItemPrepare rate limited", "playerGBID", in.PlayerGBID, "uniqueId", in.UniqueId, "opUUID", in.OpUUID)
		resp := replyAddItemPrepareRespPool.Get().(*gameServerService.LeaseAddItemPrepareResp)
		resp.UniqueId = in.UniqueId
		resp.PlayerGBID = in.PlayerGBID
		resp.Result = int32(LEASE_RATE_LIMIT)
		resp.OpUUID = in.OpUUID
		_, err := gs.GetClientEndPoint().(*gameServerService.GameServerClient).ReplyAddItemPrepare(resp)
		if err != nil {
			appLog.Errorw("ReplyAddItemPrepare failed", "err", err, "opUUID", in.OpUUID)
		}
		resp.Reset()
		replyAddItemPrepareRespPool.Put(resp)
		return nil, nil
	}

	SafeGo(func() {
		appLog.Infow("AddItemPrepare", "playerGBID", in.PlayerGBID, "uniqueId", in.UniqueId, "itemId", in.ItemId, "opUUID", in.OpUUID)

		item := &LeaseMarketItem{
			UniqueId:            in.UniqueId,
			ItemId:              in.ItemId,
			LeaseDay:            in.LeaseDays,
			PricePerDay:         in.PricePerDay,
			ReturnOwnerGbId:     in.ReturnOwner,
			ReturnOwnerServerId: uint32(in.ReturnServer),
			ReturnEndTime:       in.ReturnTime,
			ReturnReason:        in.ReturnReason,
			LessorGbId:          in.PlayerGBID,
			LessorServerId:      gs.serverId,
			ItemData:            in.ItemData,
		}
		ret := gs.app.leaseMgr.addItemPrepare(item)

		resp := replyAddItemPrepareRespPool.Get().(*gameServerService.LeaseAddItemPrepareResp)
		resp.UniqueId = in.UniqueId
		resp.PlayerGBID = in.PlayerGBID
		resp.Result = int32(ret)
		resp.OpUUID = in.OpUUID
		_, err := gs.GetClientEndPoint().(*gameServerService.GameServerClient).ReplyAddItemPrepare(resp)
		if err != nil {
			appLog.Errorw("ReplyAddItemPrepare failed", "err", err, "opUUID", in.OpUUID)
		}

		resp.Reset()
		replyAddItemPrepareRespPool.Put(resp)
	})
	return nil, nil
}

func (gs *GameServerService) AddItemCommit(in *gameServerService.LeaseAddItemCommitReq) (*gameServerService.Void, error) {
	SafeGo(func() {
		appLog.Infow("AddItemCommit", "uniqueId", in.UniqueId, "opUUID", in.OpUUID)

		ret := gs.app.leaseMgr.addItemCommit(in.UniqueId)

		resp := replyAddItemCommitRespPool.Get().(*gameServerService.LeaseAddItemCommitResp)
		resp.UniqueId = in.UniqueId
		resp.PlayerGBID = in.PlayerGBID
		resp.Result = int32(ret)
		resp.OpUUID = in.OpUUID
		_, err := gs.GetClientEndPoint().(*gameServerService.GameServerClient).ReplyAddItemCommit(resp)
		if err != nil {
			appLog.Errorw("ReplyAddItemCommit failed", "err", err, "opUUID", in.OpUUID)
		}

		resp.Reset()
		replyAddItemCommitRespPool.Put(resp)
	})
	return nil, nil
}

func (gs *GameServerService) AddItemRollback(in *gameServerService.LeaseAddItemRollbackReq) (*gameServerService.Void, error) {
	SafeGo(func() {
		appLog.Infow("AddItemRollback", "uniqueId", in.UniqueId, "opUUID", in.OpUUID)
		gs.app.leaseMgr.addItemRollback(in.UniqueId)
	})
	return nil, nil
}

func (gs *GameServerService) LeaseItemPrepare(in *gameServerService.LeaseItemPrepareReq) (*gameServerService.Void, error) {
	if !gs.limiter.Allow() {
		appLog.Warnw("LeaseItemPrepare rate limited", "buyerGBID", in.BuyerGBID, "uniqueId", in.UniqueId, "opUUID", in.OpUUID)
		resp := replyLeaseItemPrepareRespPool.Get().(*gameServerService.LeaseItemPrepareResp)
		resp.PlayerGBID = in.BuyerGBID
		resp.UniqueId = in.UniqueId
		resp.Result = int32(LEASE_RATE_LIMIT)
		resp.OpUUID = in.OpUUID
		_, err := gs.GetClientEndPoint().(*gameServerService.GameServerClient).ReplyLeaseItemPrepare(resp)
		if err != nil {
			appLog.Errorw("ReplyLeaseItemPrepare failed", "err", err, "opUUID", in.OpUUID)
		}
		resp.Reset()
		replyLeaseItemPrepareRespPool.Put(resp)
		return nil, nil
	}

	SafeGo(func() {
		appLog.Infow("LeaseItemPrepare", "buyerGBID", in.BuyerGBID, "uniqueId", in.UniqueId, "opUUID", in.OpUUID)

		totalPrice, ret := gs.app.leaseMgr.leaseItemPrepare(in.UniqueId, in.BuyerGBID, in.BuyerServerId)

		resp := replyLeaseItemPrepareRespPool.Get().(*gameServerService.LeaseItemPrepareResp)
		resp.PlayerGBID = in.BuyerGBID
		resp.UniqueId = in.UniqueId
		resp.Result = int32(ret)
		resp.OpUUID = in.OpUUID
		if ret == LEASE_OK {
			resp.PlayerGBID = in.BuyerGBID
			resp.TotalPrice = totalPrice
		}

		_, err := gs.GetClientEndPoint().(*gameServerService.GameServerClient).ReplyLeaseItemPrepare(resp)
		if err != nil {
			appLog.Errorw("ReplyLeaseItemPrepare failed", "err", err, "opUUID", in.OpUUID)
		}
		resp.Reset()
		replyLeaseItemPrepareRespPool.Put(resp)
	})
	return nil, nil
}

func (gs *GameServerService) LeaseItemCommit(in *gameServerService.LeaseItemCommitReq) (*gameServerService.Void, error) {
	SafeGo(func() {
		appLog.Infow("LeaseItemCommit", "uniqueId", in.UniqueId, "opUUID", in.OpUUID, "playerGBID", in.PlayerGBID)

		item, ret := gs.app.leaseMgr.leaseItemCommit(in.UniqueId)

		resp := replyLeaseItemCommitRespPool.Get().(*gameServerService.LeaseItemCommitResp)
		resp.PlayerGBID = in.PlayerGBID
		resp.UniqueId = in.UniqueId
		resp.Result = int32(ret)
		resp.OpUUID = in.OpUUID
		if ret == LEASE_OK {
			resp.PlayerGBID = item.LesseeGbId
			resp.LeaseStartTime = item.LeaseStartTime
			resp.LeaseEndTime = item.LeaseEndTime
			resp.LeaseCost = item.LeaseCost
			resp.LeaseGold = item.LeaseGold
			resp.LeaseBindGold = item.LeaseBindGold
			resp.LeaseTax = item.LeaseTax
			resp.LessorGBID = item.LessorGbId
			resp.OwnerGBID = item.ReturnOwnerGbId
			resp.ItemData = item.ItemData
			// 出租自己的装备时，没有设置 ReturnOwnerGbId，直接用 LessorGbId 作为 OwnerGBID
			if resp.OwnerGBID == 0 {
				resp.OwnerGBID = item.LessorGbId
			}
		}

		_, err := gs.GetClientEndPoint().(*gameServerService.GameServerClient).ReplyLeaseItemCommit(resp)
		if err != nil {
			appLog.Errorw("ReplyLeaseItemCommit failed", "err", err, "opUUID", in.OpUUID)
		}
		resp.Reset()
		replyLeaseItemCommitRespPool.Put(resp)

		// 成交后：给出租方增加收入，给承租方发放装备
		if ret == LEASE_OK {
			gs.onLeaseSuccess(item, in.OpUUID)
		}
	})
	return nil, nil
}

func (gs *GameServerService) onLeaseSuccess(item *LeaseMarketItem, opUUID uint64) {
	appLog.Infow("onLeaseSuccess", "lessor", item.LessorGbId, "lessee", item.LesseeGbId, "item", item.ItemId, "opUUID", opUUID)
	// 增加出租方收入
	ownerServer := gs.app.GetGameServer(item.LessorServerId, 0)
	if ownerServer != nil {
		req := leaseAddIncomeReqPool.Get().(*gameServerService.LeaseAddIncomeReq)
		req.UniqueId = item.UniqueId
		req.ItemId = item.ItemId
		req.PlayerGBID = item.LessorGbId
		req.BindGold = item.LeaseBindGold
		req.Gold = item.LeaseGold
		req.ReturnEndTime = item.LeaseEndTime
		req.OpUUID = opUUID
		req.ItemData = item.ItemData
		_, err := ownerServer.LeaseService.(*GameServerService).addIncomeToOwner(req, opUUID)
		if err != nil {
			appLog.Errorw("addIncomeToOwner failed", "err", err, "opUUID", opUUID)
		}
		req.Reset()
		leaseAddIncomeReqPool.Put(req)
	}

	// 给承租方发放装备
	lesseeServer := gs.app.GetGameServer(item.LesseeServerId, 0)
	if lesseeServer != nil {
		req := leaseGiveItemReqPool.Get().(*gameServerService.LeaseGiveItemReq)
		req.PlayerGBID = item.LesseeGbId
		req.ItemData = item.ItemData
		req.UniqueId = item.UniqueId
		req.ReturnEndTime = item.LeaseEndTime
		req.ReturnOwnerGbId = item.LessorGbId
		req.ReturnOwnerServerId = item.LessorServerId
		req.OpUUID = opUUID

		_, err := lesseeServer.LeaseService.(*GameServerService).giveItemToPlayer(req, opUUID)
		if err != nil {
			appLog.Errorw("giveItemToPlayer failed", "err", err, "opUUID", opUUID)
		}
		req.Reset()
		leaseGiveItemReqPool.Put(req)
	}

}

func (gs *GameServerService) LeaseItemRollback(in *gameServerService.LeaseItemRollbackReq) (*gameServerService.Void, error) {
	SafeGo(func() {
		appLog.Infow("LeaseItemRollback", "uniqueId", in.UniqueId, "opUUID", in.OpUUID)
		gs.app.leaseMgr.leaseItemRollback(in.UniqueId)
	})
	return nil, nil
}

func (gs *GameServerService) CancelItem(in *gameServerService.LeaseCancelItemReq) (*gameServerService.Void, error) {
	if !gs.limiter.Allow() {
		appLog.Warnw("CancelItem rate limited", "playerGBID", in.PlayerGBID, "uniqueId", in.UniqueId)
		resp := replyCancelItemRespPool.Get().(*gameServerService.LeaseCancelItemResp)
		resp.UniqueId = in.UniqueId
		resp.PlayerGBID = in.PlayerGBID
		resp.Result = int32(LEASE_RATE_LIMIT)
		_, err := gs.GetClientEndPoint().(*gameServerService.GameServerClient).ReplyCancelItem(resp)
		if err != nil {
			appLog.Errorw("ReplyCancelItem failed", "err", err)
		}
		resp.Reset()
		replyCancelItemRespPool.Put(resp)
		return nil, nil
	}

	SafeGo(func() {
		appLog.Infow("CancelItem", "playerGBID", in.PlayerGBID, "uniqueId", in.UniqueId)

		item, ret := gs.app.leaseMgr.cancelItem(in.UniqueId, in.PlayerGBID)

		resp := replyCancelItemRespPool.Get().(*gameServerService.LeaseCancelItemResp)
		resp.UniqueId = in.UniqueId
		resp.PlayerGBID = in.PlayerGBID
		resp.Result = int32(ret)
		if ret == LEASE_OK && item != nil {
			resp.ItemData = item.ItemData
		}

		_, err := gs.GetClientEndPoint().(*gameServerService.GameServerClient).ReplyCancelItem(resp)
		if err != nil {
			appLog.Errorw("ReplyCancelItem failed", "err", err, "opUUID")
		}
		resp.Reset()
		replyCancelItemRespPool.Put(resp)
	})
	return nil, nil
}

func (gs *GameServerService) GetShopSummary(in *gameServerService.LeaseShopSummaryReq) (*gameServerService.Void, error) {
	SafeGo(func() {
		appLog.Debugw("GetShopSummary", "categoryId", in.CategoryId, "itemIds", in.ItemIds)

		items := gs.app.leaseMgr.getShopSummary(in.ItemIds)

		resp := replyShopSummaryRespPool.Get().(*gameServerService.LeaseShopSummaryResp)
		resp.Items = items
		resp.PlayerGBID = in.PlayerGBID
		resp.CategoryId = in.CategoryId
		_, err := gs.GetClientEndPoint().(*gameServerService.GameServerClient).ReplyShopSummary(resp)
		if err != nil {
			appLog.Errorw("ReplyShopSummary failed", "err", err)
		}
		resp.Reset()
		replyShopSummaryRespPool.Put(resp)
	})
	return nil, nil
}

func (gs *GameServerService) GetShopItems(in *gameServerService.LeaseShopItemsReq) (*gameServerService.Void, error) {
	SafeGo(func() {
		appLog.Debugw("GetShopItems", "itemId", in.ItemId, "page", in.Page, "pageSize", in.PageSize)

		items := gs.app.leaseMgr.getShopItems(in.ItemId, in.Page, in.PageSize)

		resp := replyShopItemsRespPool.Get().(*gameServerService.LeaseShopItemsResp)
		resp.ItemId = in.ItemId
		resp.PlayerGBID = in.PlayerGBID
		resp.Page = in.Page
		resp.PageSize = in.PageSize
		for _, item := range items {
			resp.Items = append(resp.Items, &gameServerService.LeaseShopItem{
				UniqueId:       item.UniqueId,
				ItemId:         item.ItemId,
				LessorGbId:     item.LessorGbId,
				LessorServerId: item.LessorServerId,
				PricePerDay:    item.PricePerDay,
				LeaseDay:       item.LeaseDay,
				ReturnEndTime:  item.ReturnEndTime,
				ItemData:       item.ItemData,
			})
		}
		_, err := gs.GetClientEndPoint().(*gameServerService.GameServerClient).ReplyShopItems(resp)
		if err != nil {
			appLog.Errorw("ReplyShopItems failed", "err", err)
		}
		resp.Reset()
		replyShopItemsRespPool.Put(resp)
	})
	return nil, nil
}

func (gs *GameServerService) GetMySaleList(in *gameServerService.LeaseMySaleListReq) (*gameServerService.Void, error) {
	SafeGo(func() {
		appLog.Debugw("GetMySaleList", "playerGBID", in.PlayerGBID)

		items := gs.app.leaseMgr.getMySaleList(in.PlayerGBID)

		resp := replyMySaleListRespPool.Get().(*gameServerService.LeaseMySaleListResp)
		resp.PlayerGBID = in.PlayerGBID
		for _, item := range items {
			resp.Items = append(resp.Items, &gameServerService.LeaseMySaleItem{
				UniqueId:      item.UniqueId,
				ItemId:        item.ItemId,
				PricePerDay:   item.PricePerDay,
				LeaseDay:      item.LeaseDay,
				ReturnEndTime: item.ReturnEndTime,
				ItemData:      item.ItemData,
			})
		}
		_, err := gs.GetClientEndPoint().(*gameServerService.GameServerClient).ReplyMySaleList(resp)
		if err != nil {
			appLog.Errorw("ReplyMySaleList failed", "err", err)
		}
		resp.Reset()
		replyMySaleListRespPool.Put(resp)
	})
	return nil, nil
}

// ==================== 主动向游戏服发送的回调 ====================

func (gs *GameServerService) addIncomeToOwner(in *gameServerService.LeaseAddIncomeReq, opUUID uint64) (*gameServerService.Void, error) {
	appLog.Infow("addIncomeToOwner", "playerGBID", in.PlayerGBID, "uniqueId", in.UniqueId, "opUUID", opUUID)
	_, err := gs.GetClientEndPoint().(*gameServerService.GameServerClient).AddIncomeToOwner(in)
	return nil, err
}

func (gs *GameServerService) giveItemToPlayer(in *gameServerService.LeaseGiveItemReq, opUUID uint64) (*gameServerService.Void, error) {
	appLog.Infow("giveItemToPlayer", "playerGBID", in.PlayerGBID, "uniqueId", in.UniqueId, "opUUID", opUUID)
	in.OpUUID = opUUID
	_, err := gs.GetClientEndPoint().(*gameServerService.GameServerClient).GiveItemToPlayer(in)
	return nil, err
}
