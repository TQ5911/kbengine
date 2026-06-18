package Auction

import (
	"centralService/src/appLog"
	gameServerService "centralService/src/auction/auctionApp/gameServerService"
	"centralService/src/trpc"
	"sync"
	"time"
)

// 给游戏服务器提供的接口
type GameServerService struct {
	*trpc.ServerEndPoint
	app       *AuctionApp
	serverId  uint32
	compId    uint32
	status    int8
	pushQueue chan *gameServerService.OnItemSalingInfo
}

func BuildGameServerService(endPoint *trpc.ServerEndPoint, app *AuctionApp) *GameServerService {
	gs := &GameServerService{
		ServerEndPoint: endPoint,
		app:            app,
		pushQueue:      make(chan *gameServerService.OnItemSalingInfo, 10000),
	}
	go gs.pushConsumer()
	return gs
}

var onItemSalingInfoPool = sync.Pool{
	New: func() interface{} {
		return &gameServerService.OnItemSalingInfo{}
	},
}

var protoAuctionItemPool = sync.Pool{
	New: func() interface{} {
		return &gameServerService.AuctionItem{}
	},
}

var protoItemDataPool = sync.Pool{
	New: func() interface{} {
		return &gameServerService.ItemData{}
	},
}

var searchItemsByItemIdRespPool = sync.Pool{
	New: func() interface{} {
		return &gameServerService.SearchItemsByItemIdResp{}
	},
}

var getItemLastAndAvgPriceRespPool = sync.Pool{
	New: func() interface{} {
		return &gameServerService.GetItemLastAndAvgPriceResp{}
	},
}

var getCurrentSaleItemInfoRespPool = sync.Pool{
	New: func() interface{} {
		return &gameServerService.GetCurrentSaleItemInfoResp{}
	},
}

var getPlayerAuctionItemsRespPool = sync.Pool{
	New: func() interface{} {
		return &gameServerService.GetPlayerAuctionItemsResp{}
	},
}

var doCancelSaleItemRespPool = sync.Pool{
	New: func() interface{} {
		return &gameServerService.DoCancelSaleItemResp{}
	},
}

var onItemBeSaledInfoPool = sync.Pool{
	New: func() interface{} {
		return &gameServerService.OnItemBeSaledInfo{}
	},
}

var doBuyItemRespPool = sync.Pool{
	New: func() interface{} {
		return &gameServerService.DoBuyItemResp{}
	},
}

var buyItemRespPool = sync.Pool{
	New: func() interface{} {
		return &gameServerService.BuyItemResp{}
	},
}

var loadPlayerAuctionItemRespPool = sync.Pool{
	New: func() interface{} {
		return &gameServerService.LoadPlayerAuctionItemResp{}
	},
}

var doSaleItemRespPool = sync.Pool{
	New: func() interface{} {
		return &gameServerService.DoSaleItemResp{}
	},
}

var saleItemRespPool = sync.Pool{
	New: func() interface{} {
		return &gameServerService.SaleItemResp{}
	},
}

var getItemNumByCategoryIdRespPool = sync.Pool{
	New: func() interface{} {
		return &gameServerService.GetItemNumByCategoryIdResp{}
	},
}

var buyItemByItemIdRespPool = sync.Pool{
	New: func() interface{} {
		return &gameServerService.BuyItemByItemIdResp{}
	},
}

var doBuyItemByItemIdRespPool = sync.Pool{
	New: func() interface{} {
		return &gameServerService.DoBuyItemByItemIdResp{}
	},
}

var getAuctionItemsByAuctionIdsRespPool = sync.Pool{
	New: func() interface{} {
		return &gameServerService.GetAuctionItemByAuctionIdsResp{}
	},
}

func (gs *GameServerService) newAuctionItem() *gameServerService.AuctionItem {
	item := protoAuctionItemPool.Get().(*gameServerService.AuctionItem)
	item.Reset()
	itemData := protoItemDataPool.Get().(*gameServerService.ItemData)
	itemData.Reset()
	item.ItemData = itemData

	return item
}

func (gs *GameServerService) putAuctionItem(auctionItem *gameServerService.AuctionItem) {
	protoItemDataPool.Put(auctionItem.ItemData)
	protoAuctionItemPool.Put(auctionItem)
}

func (gs *GameServerService) OnLoseConnection() {
	close(gs.pushQueue)
	gs.status = ServiceStatus_Disconnected
	gs.app.unRegisterServer(gs)
}

func (gs *GameServerService) RegisterServer(in *gameServerService.ServerInfoMessage) (*gameServerService.Void, error) {
	err := gs.app.doRegisterServer(in.ServerId, in.CompId, in.ServerName, gs)
	if err != nil {
		return nil, err
	}
	gs.serverId = in.ServerId
	gs.compId = in.CompId
	return nil, nil
}

func (gs *GameServerService) ActiveTick(_ *gameServerService.Void) (*gameServerService.Void, error) {
	_, err := gs.GetClientEndPoint().(gameServerService.IGameServerInterface).ActiveTickCallback(&gameServerService.Void{})
	if err != nil {
		return nil, err
	}

	return nil, nil
}

func (gs *GameServerService) transAuctionItem(auctionItem *AuctionItem, dstAuctionItem *gameServerService.AuctionItem) *gameServerService.AuctionItem {
	if auctionItem == nil {
		return nil
	}
	dstAuctionItem.AuctionType = uint32(auctionItem.AuctionType)
	dstAuctionItem.AuctionItemUUID = auctionItem.AuctionItemUUID
	dstAuctionItem.AddTime = auctionItem.AddTime
	dstAuctionItem.ItemData.ItemId = auctionItem.ItemData.ItemId
	dstAuctionItem.ItemData.ItemNum = auctionItem.ItemData.ItemNum
	dstAuctionItem.ItemData.UniqueId = auctionItem.ItemData.UniqueId
	dstAuctionItem.ItemData.BindType = uint32(auctionItem.ItemData.BindType)
	dstAuctionItem.ItemData.CreateTime = auctionItem.ItemData.CreateTime
	dstAuctionItem.ItemData.ExpireTime = auctionItem.ItemData.ExpireTime
	dstAuctionItem.ItemData.AttrJson = auctionItem.ItemData.AttrJson
	dstAuctionItem.Price = auctionItem.Price
	dstAuctionItem.Number = auctionItem.Number
	dstAuctionItem.BagType = uint32(auctionItem.BagType)
	dstAuctionItem.Source = uint32(auctionItem.Source)
	dstAuctionItem.Status = uint32(auctionItem.Status)
	dstAuctionItem.Locked = auctionItem.Locked
	dstAuctionItem.ExtraInfo = auctionItem.ExtraInfo
	dstAuctionItem.TCreate = auctionItem.TCreate
	dstAuctionItem.FromPlayerGBID = auctionItem.FromPlayerGBID
	dstAuctionItem.AddPublicityTime = auctionItem.AddPublicityTime

	return dstAuctionItem
}

func (gs *GameServerService) transItemData(itemData *ItemData, dstItemData *gameServerService.ItemData) *gameServerService.ItemData {
	if itemData == nil {
		return nil
	}
	dstItemData.ItemId = itemData.ItemId
	dstItemData.ItemNum = itemData.ItemNum
	dstItemData.UniqueId = itemData.UniqueId
	dstItemData.BindType = uint32(itemData.BindType)
	dstItemData.CreateTime = itemData.CreateTime
	dstItemData.ExpireTime = itemData.ExpireTime
	dstItemData.AttrJson = itemData.AttrJson

	return dstItemData
}

func (gs *GameServerService) SaleItem(in *gameServerService.SaleItemReq) (*gameServerService.Void, error) {
	go func() {

		appLog.Infow("SaleItem", "PlayerGBID", in.PlayerGBID, "ItemDict", in.ItemDict, "EachPrice", in.TotalPrice, "Number", in.Number, "Extra", in.Extra, "addPublicityType", in.AddPublicityTime)
		auctionItem, extra, err := gs.app.SaleItem(in.PlayerGBID, in.ItemDict, in.TotalPrice, in.Number, uint8(in.BagType), in.Extra, in.AddPublicityTime)
		if err != nil || auctionItem == nil {
			appLog.Errorw("SaleItem", "err", err)
			return
		}

		dstAuctionItem := gs.newAuctionItem()
		defer gs.putAuctionItem(dstAuctionItem)
		response := saleItemRespPool.Get().(*gameServerService.SaleItemResp)
		response.PlayerGBID = in.PlayerGBID
		response.AuctionItem = gs.transAuctionItem(auctionItem, dstAuctionItem)
		response.Extra = extra

		_, err = gs.GetClientEndPoint().(gameServerService.IGameServerInterface).ReplySaleItem(response)
		if err != nil {
			appLog.Errorw("SaleItem", "err", err)
		}

		response.Reset()
		saleItemRespPool.Put(response)
	}()
	return nil, nil
}

func (gs *GameServerService) DoSaleItem(in *gameServerService.DoSaleItemReq) (*gameServerService.Void, error) {
	gs.app.funcChan <- func() {
		appLog.Infow("DoSaleItem", "AuctionItemUUID", in.AuctionItemUUID, "PlayerGBID", in.PlayerGBID, "Extra", in.Extra, "Result", in.Result)
		auctionItem, extra, err := gs.app.DoSaleItem(in.AuctionItemUUID, in.PlayerGBID, in.Extra, in.Result, gs)
		if err != nil || auctionItem == nil {
			appLog.Errorw("DoSaleItem", "err", err)
			return
		}

		dstAuctionItem := gs.newAuctionItem()
		defer gs.putAuctionItem(dstAuctionItem)

		response := doSaleItemRespPool.Get().(*gameServerService.DoSaleItemResp)
		response.PlayerGBID = in.PlayerGBID
		response.AuctionItem = gs.transAuctionItem(auctionItem, dstAuctionItem)
		response.Extra = extra

		_, err = gs.GetClientEndPoint().(gameServerService.IGameServerInterface).ReplyDoSaleItem(response)
		if err != nil {
			appLog.Errorw("DoSaleItem->ReplyDoSaleItem", "err", err)
		}

		response.Reset()
		doSaleItemRespPool.Put(response)
	}

	return nil, nil
}

func (gs *GameServerService) RefreshPlayerCoinAuctionData(playerGBID uint64, auctionItemUUIDs []uint64, extra string) (*gameServerService.Void, error) {
	go func() {
		appLog.Debugw("RefreshPlayerCoinAuctionData", "playerGBID", playerGBID, "auctionItemUUIDs", auctionItemUUIDs, "extra", extra)
		response := loadPlayerAuctionItemRespPool.Get().(*gameServerService.LoadPlayerAuctionItemResp)
		response.PlayerGBID = playerGBID
		response.AuctionItemUUIDs = auctionItemUUIDs
		response.Extra = extra

		_, err := gs.GetClientEndPoint().(*gameServerService.GameServerClient).ReplyLoadPlayerAuctionItem(response)
		if err != nil {
			appLog.Errorw("RefreshPlayerCoinAuctionData->ReplyLoadPlayerAuctionItem", "err", err)
		}

		response.Reset()
		loadPlayerAuctionItemRespPool.Put(response)
	}()
	return nil, nil
}

func (gs *GameServerService) BuyItem(in *gameServerService.BuyItemReq) (*gameServerService.Void, error) {
	go func() {
		appLog.Infow("BuyItem", "PlayerGBID", in.PlayerGBID, "AuctionItemUUID", in.AuctionItemUUID, "Number", in.Number, "Extra", in.Extra)
		auctionItemUUID, extra, price, publicityEndTime, code, buyType, err := gs.app.BuyItem(in.PlayerGBID, in.AuctionItemUUID, in.Number, in.Extra)
		if err != nil {
			appLog.Errorw("BuyItem", "err", err)
			return
		}

		response := buyItemRespPool.Get().(*gameServerService.BuyItemResp)
		response.PlayerGBID = in.PlayerGBID
		response.AuctionItemUUID = auctionItemUUID
		response.Price = price
		response.PublicityEndTime = publicityEndTime
		response.BuyType = buyType
		response.Extra = extra
		response.Code = code

		_, err = gs.GetClientEndPoint().(gameServerService.IGameServerInterface).ReplyBuyItem(response)
		if err != nil {
			appLog.Errorw("BuyItem->ReplyBuyItem failed", "err", err)
		}

		response.Reset()
		buyItemRespPool.Put(response)
	}()
	return nil, nil
}

func (gs *GameServerService) DoBuyItem(in *gameServerService.DoBuyItemReq) (*gameServerService.Void, error) {
	gs.app.funcChan <- func() {
		appLog.Infow("DoBuyItem", "AuctionItemUUID", in.AuctionItemUUID, "PlayerGBID", in.PlayerGBID, "Errno", in.Errno, "Price", in.Price, "Extra", in.Extra)
		auctionItem, extra, err := gs.app.DoBuyItem(in.AuctionItemUUID, in.PlayerGBID, in.Errno, in.Price, in.Extra, gs)
		if err != nil || auctionItem == nil {
			appLog.Errorw("DoBuyItem", "err", err)
			return
		}

		dstAuctionItem := gs.newAuctionItem()
		defer gs.putAuctionItem(dstAuctionItem)
		response := doBuyItemRespPool.Get().(*gameServerService.DoBuyItemResp)
		response.PlayerGBID = in.PlayerGBID
		response.AuctionItem = gs.transAuctionItem(auctionItem, dstAuctionItem)
		response.Extra = extra

		_, err = gs.GetClientEndPoint().(gameServerService.IGameServerInterface).ReplyDoBuyItem(response)
		if err != nil {
			appLog.Errorw("BuyItem->ReplyDoBuyItem failed", "err", err)
		}

		response.Reset()
		doBuyItemRespPool.Put(response)
	}
	return nil, nil
}

const onSaleChatPushPerSec int = 300 // 每秒每个serverId最大推送数量

func (gs *GameServerService) pushConsumer() {
	ticker := time.NewTicker(time.Second)
	defer ticker.Stop()
	for range ticker.C {
		// 每个周期内批量处理多条
		for i := 0; i < onSaleChatPushPerSec; i++ {
			isEnd := false
			select {
			case info, ok := <-gs.pushQueue:
				if !ok {
					appLog.Errorw("OnItemSaling channel is closed")
					return
				}
				_, err := gs.GetClientEndPoint().(*gameServerService.GameServerClient).OnItemSaling(info)
				if err != nil {
					appLog.Errorw("OnItemSaling send failed", "err", err)
				}
				info.Reset()
				onItemSalingInfoPool.Put(info)
			default:
				isEnd = true
				// channel 为空，提前结束本批次
				break // 跳出内层 for 循环
			}
			if isEnd {
				break
			}
		}
	}
}

func (gs *GameServerService) OnItemSaling(auctionItemUUID uint64, itemId uint32, gbId uint64) {
	info := onItemSalingInfoPool.Get().(*gameServerService.OnItemSalingInfo)
	info.AuctionItemUUID = auctionItemUUID
	info.ItemId = itemId
	info.GbId = gbId

	gs.pushQueue <- info
}

func (gs *GameServerService) OnItemBeSaled(playerGBID uint64, auctionItem *AuctionItem, number uint32, extra string) (*gameServerService.Void, error) {
	go func() {
		appLog.Debugw("OnItemBeSaled", "playerGBID", playerGBID, "auctionItemUUID", auctionItem.AuctionItemUUID, "number", number, "extra", extra)
		dstAuctionItem := gs.newAuctionItem()
		defer gs.putAuctionItem(dstAuctionItem)
		response := onItemBeSaledInfoPool.Get().(*gameServerService.OnItemBeSaledInfo)
		response.PlayerGBID = playerGBID
		response.AuctionItem = gs.transAuctionItem(auctionItem, dstAuctionItem)
		response.Number = number
		response.Extra = extra

		_, err := gs.GetClientEndPoint().(*gameServerService.GameServerClient).OnItemBeSaled(response)
		if err != nil {
			appLog.Errorw("OnItemBeSaled send to client", "err", err)
		}
		response.Reset()
		onItemBeSaledInfoPool.Put(response)
	}()
	return nil, nil
}

func (gs *GameServerService) CancelSaleItem(in *gameServerService.CancelSaleItemReq) (*gameServerService.Void, error) {
	gs.app.funcChan <- func() {
		appLog.Infow("CancelSaleItem", "PlayerGBID", in.PlayerGBID, "AuctionItemUUID", in.AuctionItemUUID, "Extra", in.Extra)
		auctionItem, extra, retCode, err := gs.app.CancelSaleItem(in.PlayerGBID, in.AuctionItemUUID, in.Extra)
		if err != nil {
			appLog.Errorw("CancelSaleItem", "err", err)
			return
		}
		if retCode != AUCTION_OK {
			dstAuctionItem := gs.newAuctionItem()
			defer gs.putAuctionItem(dstAuctionItem)
			response := doCancelSaleItemRespPool.Get().(*gameServerService.DoCancelSaleItemResp)
			response.PlayerGBID = in.PlayerGBID
			response.Errno = retCode
			response.AuctionItem = gs.transAuctionItem(auctionItem, dstAuctionItem)
			response.Extra = extra
			_, err := gs.GetClientEndPoint().(gameServerService.IGameServerInterface).ReplyDoCancelSaleItem(response)
			if err != nil {
				appLog.Errorw("CancelSaleItem->ReplyDoCancelSaleItem failed", "err", err)
			}

			response.Reset()
			doCancelSaleItemRespPool.Put(response)
		} else {
			auctionItem, extra, errno := gs.app.DoCancelSaleItem(in.AuctionItemUUID, in.PlayerGBID, extra, gs)
			if auctionItem == nil {
				appLog.Warnw("DoCancelSaleItem", "errno", errno, "AuctionItemUUID", in.AuctionItemUUID, "PlayerGBID", in.PlayerGBID, "Extra", in.Extra)
				return
			}

			dstAuctionItem := gs.newAuctionItem()
			defer gs.putAuctionItem(dstAuctionItem)
			response := doCancelSaleItemRespPool.Get().(*gameServerService.DoCancelSaleItemResp)
			response.PlayerGBID = in.PlayerGBID
			response.Errno = errno
			response.AuctionItem = gs.transAuctionItem(auctionItem, dstAuctionItem)
			response.Extra = extra
			_, err := gs.GetClientEndPoint().(gameServerService.IGameServerInterface).ReplyDoCancelSaleItem(response)
			if err != nil {
				appLog.Errorw("CancelSaleItem->ReplyDoCancelSaleItem failed", "err", err)
			}

			response.Reset()
			doCancelSaleItemRespPool.Put(response)
		}
	}

	return nil, nil
}

func (gs *GameServerService) DoCancelSaleItem(in *gameServerService.DoCancelSaleItemReq) (*gameServerService.Void, error) {
	//appLog.Infow("DoCancelSaleItem", "AuctionItemUUID", in.AuctionItemUUID, "PlayerGBID", in.PlayerGBID, "Extra", in.Extra)
	//auctionItem, extra, errno := gs.app.DoCancelSaleItem(in.AuctionItemUUID, in.PlayerGBID, in.Extra, gs)
	//if auctionItem == nil {
	//	appLog.Warnw("DoCancelSaleItem", "errno", errno, "AuctionItemUUID", in.AuctionItemUUID, "PlayerGBID", in.PlayerGBID, "Extra", in.Extra)
	//	return nil, nil
	//}
	//
	//dstAuctionItem := gs.newAuctionItem()
	//defer gs.putAuctionItem(dstAuctionItem)
	//response := doCancelSaleItemRespPool.Get().(*gameServerService.DoCancelSaleItemResp)
	//response.PlayerGBID = in.PlayerGBID
	//response.Errno = errno
	//response.AuctionItem = gs.transAuctionItem(auctionItem, dstAuctionItem)
	//response.Extra = extra
	//_, err := gs.GetClientEndPoint().(gameServerService.IGameServerInterface).ReplyDoCancelSaleItem(response)
	//if err != nil {
	//	appLog.Errorw("CancelSaleItem->ReplyDoCancelSaleItem failed", "err", err)
	//}
	//
	//response.Reset()
	//doCancelSaleItemRespPool.Put(response)

	return nil, nil
}

func (gs *GameServerService) SearchItemsByItemId(in *gameServerService.SearchItemsByItemIdReq) (*gameServerService.Void, error) {
	go func() {

		appLog.Debugw("SearchItemsByItemId", "PlayerGBID", in.PlayerGBID, "ItemIds", in.ItemIds, "Limit", in.Limit, "Offset", in.Offset, "IsPublicity", in.IsPublicity, "Extra", in.Extra)
		auctionItems, allCount, err := gs.app.SearchItemsByItemId(in.PlayerGBID, in.ItemIds, in.Limit, in.Offset, in.IsPublicity, in.Extra)
		if err != nil {
			appLog.Errorw("SearchItemsByItemId", "err", err)
			return
		}
		var dstAuctionItems []*gameServerService.AuctionItem
		for _, auctionItem := range auctionItems {
			dstAuctionItem := gs.newAuctionItem()
			gs.transAuctionItem(auctionItem, dstAuctionItem)
			dstAuctionItems = append(dstAuctionItems, dstAuctionItem)
		}

		response := searchItemsByItemIdRespPool.Get().(*gameServerService.SearchItemsByItemIdResp)
		response.PlayerGBID = in.PlayerGBID
		response.ItemIds = in.ItemIds
		response.Limit = in.Limit
		response.Offset = in.Offset
		response.AuctionItems = dstAuctionItems
		response.TotalNum = allCount
		response.Extra = in.Extra
		response.IsPublicity = in.IsPublicity

		_, err = gs.GetClientEndPoint().(gameServerService.IGameServerInterface).ReplySearchItemsByItemId(response)
		if err != nil {
			appLog.Errorw("SearchItemsByItemId -> ReplySearchItemsByItemId", "err", err)
		}

		for _, dstAuctionItem := range dstAuctionItems {
			gs.putAuctionItem(dstAuctionItem)
		}

		response.Reset()
		searchItemsByItemIdRespPool.Put(response)
	}()

	return nil, nil
}

func (gs *GameServerService) GetItemLastAndAvgPrice(in *gameServerService.GetItemLastAndAvgPriceReq) (*gameServerService.Void, error) {
	go func() {
		appLog.Debugw("GetItemLastAndAvgPrice", "ItemId", in.ItemId, "PlayerGBID", in.PlayerGBID, "Extra", in.Extra)
		lastPrice, err := gs.app.GetItemLastPrice(in.ItemId)
		if err != nil {
			appLog.Errorw("GetItemLastAndAvgPrice", "err", err)
			return
		}
		avgPrice, err := gs.app.GetItemAvgPrice(in.ItemId)
		if err != nil {
			appLog.Errorw("GetItemLastAndAvgPrice", "err", err)
			return
		}
		response := getItemLastAndAvgPriceRespPool.Get().(*gameServerService.GetItemLastAndAvgPriceResp)
		response.PlayerGBID = in.PlayerGBID
		response.ItemId = in.ItemId
		response.LastPrice = lastPrice
		response.AvgPrice = avgPrice
		response.Extra = in.Extra

		_, err = gs.GetClientEndPoint().(*gameServerService.GameServerClient).ReplyGetItemLastAndAvgPrice(response)
		if err != nil {
			appLog.Errorw("GetItemLastAndAvgPrice", "err", err)
		}

		response.Reset()
		getItemLastAndAvgPriceRespPool.Put(response)
	}()
	return nil, nil
}

// getCurrentSaleItemInfo
func (gs *GameServerService) GetCurrentSaleItemInfo(in *gameServerService.GetCurrentSaleItemInfoReq) (*gameServerService.Void, error) {
	go func() {

		appLog.Debugw("GetCurrentSaleItemInfo", "ItemId", in.ItemId, "PlayerGBID", in.PlayerGBID, "Extra", in.Extra, "IsPublicity", in.IsPublicity)
		auctionItems, _, err := gs.app.GetCurrentSaleItemInfo(in.ItemId, in.PlayerGBID, in.IsPublicity)
		if err != nil {
			appLog.Errorw("GetCurrentSaleItemInfo", "err", err)
			return
		}
		var dstAuctionItems []*gameServerService.AuctionItem
		for _, auctionItem := range auctionItems {
			dstAuctionItem := gs.newAuctionItem()
			gs.transAuctionItem(auctionItem, dstAuctionItem)
			dstAuctionItems = append(dstAuctionItems, dstAuctionItem)
		}

		lastPrice, _ := gs.app.GetItemLastPrice(in.ItemId)
		avgPrice, _ := gs.app.GetItemAvgPrice(in.ItemId)
		response := getCurrentSaleItemInfoRespPool.Get().(*gameServerService.GetCurrentSaleItemInfoResp)
		response.PlayerGBID = in.PlayerGBID
		response.ItemId = in.ItemId
		response.AuctionItems = dstAuctionItems
		response.Extra = in.Extra
		response.LastPrice = lastPrice
		response.AvgPrice = avgPrice
		response.IsPublicity = in.IsPublicity

		_, err = gs.GetClientEndPoint().(*gameServerService.GameServerClient).ReplyGetCurrentSaleItemInfo(response)
		if err != nil {
			appLog.Errorw("GetCurrentSaleItemInfo->ReplyGetCurrentSaleItemInfo", "err", err)
		}

		for _, dstAuctionItem := range dstAuctionItems {
			gs.putAuctionItem(dstAuctionItem)
		}

		response.Reset()
		getCurrentSaleItemInfoRespPool.Put(response)
	}()

	return nil, nil
}

func (gs *GameServerService) GetPlayerAuctionItems(in *gameServerService.GetPlayerAuctionItemsReq) (*gameServerService.Void, error) {
	go func() {
		var dstAuctionItems []*gameServerService.AuctionItem
		auctionItems := gs.app.GetPlayerAuctionItems(in.PlayerGBID)
		for _, auctionItem := range auctionItems {
			dstAuctionItem := gs.newAuctionItem()
			gs.transAuctionItem(auctionItem, dstAuctionItem)
			dstAuctionItems = append(dstAuctionItems, dstAuctionItem)
		}

		response := getPlayerAuctionItemsRespPool.Get().(*gameServerService.GetPlayerAuctionItemsResp)
		response.PlayerGBID = in.PlayerGBID
		response.AuctionItems = dstAuctionItems
		response.Extra = in.Extra

		_, err := gs.GetClientEndPoint().(*gameServerService.GameServerClient).ReplyGetPlayerAuctionItems(response)
		if err != nil {
			appLog.Errorw("GetPlayerAuctionItems", "err", err)
		}

		for _, dstAuctionItem := range dstAuctionItems {
			gs.putAuctionItem(dstAuctionItem)
		}

		response.Reset()
		getPlayerAuctionItemsRespPool.Put(response)
	}()

	return nil, nil
}

func (gs *GameServerService) LoadPlayerAuctionItem(in *gameServerService.LoadPlayerAuctionItemReq) (*gameServerService.Void, error) {
	go func() {
		appLog.Debugw("LoadPlayerAuctionItem", "PlayerGBID", in.PlayerGBID, "Extra", in.Extra)
		auctionItemUUIDs, extra, err := gs.app.LoadPlayerAuctionItem(in.PlayerGBID, in.Extra)
		if err != nil {
			appLog.Errorw("LoadPlayerAuctionItem", "err", err)
			return
		}

		response := loadPlayerAuctionItemRespPool.Get().(*gameServerService.LoadPlayerAuctionItemResp)
		response.PlayerGBID = in.PlayerGBID
		response.AuctionItemUUIDs = auctionItemUUIDs
		response.Extra = extra

		_, err = gs.GetClientEndPoint().(*gameServerService.GameServerClient).ReplyLoadPlayerAuctionItem(response)
		if err != nil {
			appLog.Errorw("LoadPlayerAuctionItem->ReplyLoadPlayerAuctionItem", "err", err)
		}

		response.Reset()
		loadPlayerAuctionItemRespPool.Put(response)
	}()
	return nil, nil
}

func (gs *GameServerService) DoCommand(in *gameServerService.DoCommandReq) (*gameServerService.Void, error) {
	appLog.Infow("DoCommand", "Command", in.Command, "Extra", in.Extra)
	extra, err := gs.app.DoCommand(in.Command, in.Extra)
	if err != nil {
		appLog.Errorw("DoCommand", "err", err)
		return nil, nil
	}
	response := gameServerService.DoCommandResp{
		Command: in.Command,
		Extra:   extra,
	}
	_, err = gs.GetClientEndPoint().(*gameServerService.GameServerClient).ReplyDoCommand(&response)
	if err != nil {
		appLog.Errorw("DoCommand->ReplyDoCommand", "err", err)

	}
	return nil, nil
}

func (gs *GameServerService) GetAuctionItemNumByCategoryId(in *gameServerService.GetItemNumByCategoryIdReq) (*gameServerService.Void, error) {
	go func() {
		appLog.Debugw("GetAuctionItemNumByCategoryId", "PlayerGBID", in.PlayerGBID, "CategoryId", in.CategoryId, "itemIds", in.ItemIds, "isPublicity", in.IsPublicity)
		itemIds, itemNums, eachPrices, err := gs.app.getAuctionItemNumByCategoryId(in.ItemIds, in.IsPublicity)
		if err != nil {
			appLog.Errorw("GetAuctionItemNumByCategoryId", "err", err)
			return
		}

		response := getItemNumByCategoryIdRespPool.Get().(*gameServerService.GetItemNumByCategoryIdResp)
		response.PlayerGBID = in.PlayerGBID
		response.CategoryId = in.CategoryId
		response.ItemIds = itemIds
		response.ItemNums = itemNums
		response.Prices = eachPrices
		response.IsPublicity = in.IsPublicity
		_, err = gs.GetClientEndPoint().(*gameServerService.GameServerClient).ReplyGetAuctionItemNumByCategoryId(response)
		if err != nil {
			appLog.Errorw("GetAuctionItemNumByCategoryId->ReplyGetItemNumByCategoryId", "err", err)
		}

		response.Reset()
		getItemNumByCategoryIdRespPool.Put(response)
	}()
	return nil, nil
}

func (gs *GameServerService) BuyItemByItemId(in *gameServerService.BuyItemByItemIdReq) (*gameServerService.Void, error) {
	go func() {
		appLog.Infow("BuyItemByItemId", "PlayerGBID", in.PlayerGBID, "ItemId", in.ItemId, "Number", in.Number, "Price", in.Price, "Extra", in.Extra)
		auctionItemUUIDs, remainNum, totalPrice, err := gs.app.buyItemByItemId(in.PlayerGBID, in.ItemId, in.Number, in.Price)
		if err != nil {
			appLog.Errorw("BuyItemByItemId", "err", err)
			return
		}

		response := buyItemByItemIdRespPool.Get().(*gameServerService.BuyItemByItemIdResp)
		response.PlayerGBID = in.PlayerGBID
		response.ItemId = in.ItemId
		response.Number = in.Number
		response.Price = in.Price
		response.Extra = in.Extra
		response.RemainNum = remainNum
		response.AuctionItemUUIDs = auctionItemUUIDs
		response.TotalPrice = totalPrice

		_, err = gs.GetClientEndPoint().(*gameServerService.GameServerClient).ReplyBuyItemByItemId(response)
		if err != nil {
			appLog.Errorw("BuyItemByItemId->ReplyBuyItemByItemId", "err", err)
		}

		response.Reset()
		buyItemByItemIdRespPool.Put(response)
	}()

	return nil, nil
}

func (gs *GameServerService) DoBuyItemByItemId(in *gameServerService.DoBuyItemByItemIdReq) (*gameServerService.Void, error) {
	gs.app.funcChan <- func() {
		appLog.Infow("DoBuyItemByItemId", "PlayerGBID", in.PlayerGBID, "Errno", in.Errno, "ItemId", in.ItemId, "Number", in.Number, "Price", in.Price, "RemainNum", in.RemainNum, "AuctionItemUUIDs", in.AuctionItemUUIDs, "TotalPrice", in.TotalPrice, "Extra", in.Extra)
		itemData, extra, err := gs.app.doBuyItemByItemId(in.PlayerGBID, in.Errno, in.ItemId, in.Number, in.Price, in.RemainNum, in.AuctionItemUUIDs, in.TotalPrice, in.Extra)
		if err != nil || itemData == nil {
			appLog.Errorw("DoBuyItemByItemId", "err", err, "PlayerGBID", in.PlayerGBID, "Errno", in.Errno, "ItemId", in.ItemId, "Number", in.Number, "Price", in.Price, "RemainNum", in.RemainNum, "AuctionItemUUIDs", in.AuctionItemUUIDs, "TotalPrice", in.TotalPrice, "Extra", in.Extra)
			return
		}

		response := doBuyItemByItemIdRespPool.Get().(*gameServerService.DoBuyItemByItemIdResp)
		response.PlayerGBID = in.PlayerGBID
		response.Errno = in.Errno
		response.ItemId = in.ItemId
		response.Number = in.Number
		response.Price = in.Price
		response.RemainNum = in.RemainNum
		response.TotalPrice = in.TotalPrice
		response.Extra = extra
		itemDataEx := protoItemDataPool.Get().(*gameServerService.ItemData)
		response.ItemData = gs.transItemData(itemData, itemDataEx)

		_, err = gs.GetClientEndPoint().(*gameServerService.GameServerClient).ReplyDoBuyItemByItemId(response)
		if err != nil {
			appLog.Errorw("DoBuyItemByItemId->ReplyDoBuyItemByItemId", "err", err)
		}

		itemDataEx.Reset()
		protoItemDataPool.Put(itemDataEx)

		response.Reset()
		doBuyItemByItemIdRespPool.Put(response)
	}

	return nil, nil
}

func (gs *GameServerService) GetAuctionItemsByAuctionIds(in *gameServerService.GetAuctionItemByAuctionIdsReq) (*gameServerService.Void, error) {
	go func() {
		appLog.Debugw("getAuctionItemsByAuctionIds", "PlayerGBID", in.PlayerGBID, "CategoryId", in.CategoryId, "itemIds", in.AuctionIds)
		auctionItems, err := gs.app.getAuctionItemsByAuctionIds(in.AuctionIds)
		if err != nil {
			appLog.Errorw("getAuctionItemsByAuctionIds", "err", err)
			return
		}

		var dstAuctionItems []*gameServerService.AuctionItem
		for _, auctionItem := range auctionItems {
			dstAuctionItem := gs.newAuctionItem()
			gs.transAuctionItem(auctionItem, dstAuctionItem)
			dstAuctionItems = append(dstAuctionItems, dstAuctionItem)
		}

		response := getAuctionItemsByAuctionIdsRespPool.Get().(*gameServerService.GetAuctionItemByAuctionIdsResp)
		response.PlayerGBID = in.PlayerGBID
		response.CategoryId = in.CategoryId
		response.AuctionItems = dstAuctionItems

		_, err = gs.GetClientEndPoint().(*gameServerService.GameServerClient).ReplyGetAuctionItemsByAuctionIds(response)
		if err != nil {
			appLog.Errorw("getAuctionItemsByAuctionIds->ReplyGetItemNumByCategoryId", "err", err)
		}

		for _, dstAuctionItem := range dstAuctionItems {
			gs.putAuctionItem(dstAuctionItem)
		}
		response.Reset()
		getAuctionItemsByAuctionIdsRespPool.Put(response)
	}()
	return nil, nil
}
