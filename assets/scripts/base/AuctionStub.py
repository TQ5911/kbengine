# -*- coding: utf-8 -*-

import KBEngine

import utils
from KBEDebug import *
import gameengine
import iGlobal
import iBaseNoCell
import iTimer
import gametimer
import gameconfig
import auction
import itemFactory
import redisUtils
import iRouter

import auction_auctionConst as AUC_CONST

from rpc import RpcChannel, TcpClient
from proto.gameServerAuction_pb2 import (
    AuctionServer_Stub, GameServer, ServerInfoMessage, GetItemLastAndAvgPriceReq, Void,
    SaleItemReq, DoSaleItemReq, BuyItemReq, DoBuyItemReq, CancelSaleItemReq, DoCancelSaleItemReq,
    SearchItemsByItemIdReq, GetPlayerAuctionItemsReq, LoadPlayerAuctionItemReq, DoCommandReq,
    GetItemNumByCategoryIdReq, BuyItemByItemIdReq, DoBuyItemByItemIdReq, GetCurrentSaleItemInfoReq, 
    GetAuctionItemByAuctionIdsReq)

import gameglobal
import gameconst
import json
import LogTrackingMgr

class AuctionStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer):
    def __init__(self):
        iGlobal.IGlobal.__init__(self)
        iBaseNoCell.IBaseNoCell.__init__(self)
        iTimer.ITimer.__init__(self)

        self.auctionService = None

    def doNext(self):
        self._fullPrepare()

    def _fullPrepare(self):
        self.pyAddTimer(1, 1, gametimer.AUCTION_STUB_ASYNC_TICK)
        gameglobal.localBaseApp.initAysncore()
        self.pyAddTimer(gameconst.CENTRAL_SERVER_HEARTBEAT_INTERVAL, gameconst.CENTRAL_SERVER_HEARTBEAT_INTERVAL,
                        gametimer.AUCTION_STUB_ACTIVE_TICK)

    def onTimer(self, tid, userArg):
        self._onTimer(tid, userArg)
        if userArg == gametimer.AUCTION_STUB_ASYNC_TICK:
            self._connectAuctionCenter()
        elif userArg == gametimer.AUCTION_STUB_ACTIVE_TICK:
            self._checkAuctionCenterActive()

    def reloadScript(self):
        super(AuctionStub, self).reloadScript()

    def _connectAuctionCenter(self):
        if not gameconfig.enableAuction():
            return

        host = gameconfig.auctionServerHost()
        if not (self.auctionService and self.auctionService.channel.dispatcher):
            INFO_MSG('connect auctionCenter---------:', host)
            self.auctionService = AuctionStubService(self, host)

    def _checkAuctionCenterActive(self):
        if not gameconfig.enableAuction():
            return

        if self.auctionService and self.auctionService.channel.dispatcher:
            self.auctionService.serviceStub.activeTick(None, Void(), None)

    def isAuctionCenterActive(self, needCheck=True):
        if needCheck and not gameconfig.enableAuction():
            return False

        return self.auctionService and self.auctionService.channel.dispatcher

    def saleItem(self, playerGBID, itemDict, totalPrice, number, bagType, extra):
        if not self.isAuctionCenterActive():
            INFO_MSG("saleItem auctionCenter is not active")
            return

        request = SaleItemReq()
        request.playerGBID = playerGBID
        request.itemDict = itemDict
        request.totalPrice = totalPrice
        request.number = number
        request.bagType = bagType
        request.extra = json.dumps(extra)

        self.auctionService.serviceStub.saleItem(None, request, None)

    def doSaleItem(self, auctionItemUUID, playerGBID, extra, result):
        if not self.isAuctionCenterActive(False):
            INFO_MSG("doSaleItem auctionCenter is not active")
            return

        request = DoSaleItemReq()
        request.auctionItemUUID = auctionItemUUID
        request.playerGBID = playerGBID
        request.extra = json.dumps(extra)
        request.result = result

        self.auctionService.serviceStub.doSaleItem(None, request, None)

    def buyItem(self, playerGBID, auctionItemUUID, number, extra):
        if not self.isAuctionCenterActive():
            INFO_MSG("buyItem auctionCenter is not active")
            return

        request = BuyItemReq()
        request.playerGBID = playerGBID
        request.auctionItemUUID = auctionItemUUID
        request.number = number
        request.extra = json.dumps(extra)

        self.auctionService.serviceStub.buyItem(None, request, None)

    def doBuyItem(self, auctionItemUUID, playerGBID, errno, price, extra):
        if not self.isAuctionCenterActive():
            INFO_MSG("doBuyItem auctionCenter is not active")
            return

        request = DoBuyItemReq()
        request.auctionItemUUID = auctionItemUUID
        request.playerGBID = playerGBID
        request.errno = errno
        request.price = price
        request.extra = json.dumps(extra)

        self.auctionService.serviceStub.doBuyItem(None, request, None)

    def cancelSaleItem(self, playerGBID, auctionItemUUID, extra):
        if not self.isAuctionCenterActive():
            INFO_MSG("cancelSaleItem auctionCenter is not active")
            return

        request = CancelSaleItemReq()
        request.playerGBID = playerGBID
        request.auctionItemUUID = auctionItemUUID
        request.extra = json.dumps(extra)

        self.auctionService.serviceStub.cancelSaleItem(None, request, None)

    def doCancelSaleItem(self, auctionItemUUID, playerGBID, extra):
        if not self.isAuctionCenterActive(False):
            INFO_MSG("doCancelSaleItem auctionCenter is not active")
            return

        request = DoCancelSaleItemReq()
        request.auctionItemUUID = auctionItemUUID
        request.playerGBID = playerGBID
        request.extra = json.dumps(extra)

        self.auctionService.serviceStub.doCancelSaleItem(None, request, None)

    def searchItemsByItemId(self, playerGBID, itemIds, limit, offset, isPublicity, extra):
        if not self.isAuctionCenterActive():
            INFO_MSG("searchItemsByItemId auctionCenter is not active")
            return

        request = SearchItemsByItemIdReq()
        request.playerGBID = playerGBID
        for itemId in itemIds:
            request.itemIds.append(itemId)
        request.limit = limit
        request.offset = offset
        request.isPublicity = isPublicity
        request.extra = json.dumps(extra)

        self.auctionService.serviceStub.searchItemsByItemId(None, request, None)

    def getItemLastAndAvgPrice(self, playerGBID, itemId, extra):
        if not self.isAuctionCenterActive():
            INFO_MSG("getItemLastAndAvgPrice auctionCenter is not active")
            return

        request = GetItemLastAndAvgPriceReq()
        request.playerGBID = playerGBID
        request.itemId = itemId
        request.extra = json.dumps(extra)

        self.auctionService.serviceStub.getItemLastAndAvgPrice(None, request, None)

    def getCurrentSaleItemInfo(self, playerGBID, itemId, isPublicity, extra):
        if not self.isAuctionCenterActive():
            INFO_MSG("getCurrentSaleItemInfo auctionCenter is not active")
            return

        request = GetCurrentSaleItemInfoReq()
        request.playerGBID = playerGBID
        request.itemId = itemId
        request.isPublicity = isPublicity
        request.extra = json.dumps(extra)

        self.auctionService.serviceStub.getCurrentSaleItemInfo(None, request, None)

    def getPlayerAuctionItems(self, playerGBID, extra):
        if not self.isAuctionCenterActive():
            INFO_MSG("getPlayerAuctionItems auctionCenter is not active")
            return

        request = GetPlayerAuctionItemsReq()
        request.playerGBID = playerGBID
        request.extra = json.dumps(extra)

        self.auctionService.serviceStub.getPlayerAuctionItems(None, request, None)

    def loadPlayerAuctionItem(self, playerGBID, extra):
        if not self.isAuctionCenterActive():
            INFO_MSG("loadPlayerAuctionItem auctionCenter is not active")
            return

        request = LoadPlayerAuctionItemReq()
        request.playerGBID = playerGBID
        request.extra = json.dumps(extra)

        self.auctionService.serviceStub.loadPlayerAuctionItem(None, request, None)

    def doCommand(self, command, extra):
        if not self.isAuctionCenterActive():
            INFO_MSG("doCommand auctionCenter is not active")
            return

        request = DoCommandReq()
        request.command = command
        request.extra = json.dumps(extra)

        self.auctionService.serviceStub.doCommand(None, request, None)

    def getAuctionItemNumByCategoryId(self, playerGBID, categoryId, itemIdList, isPublicity):
        if not self.isAuctionCenterActive():
            INFO_MSG("getAuctionItemNumByCategoryId auctionCenter is not active")
            return

        request = GetItemNumByCategoryIdReq()
        request.playerGBID = playerGBID
        request.categoryId = categoryId
        for itemId in itemIdList:
            request.itemIds.append(itemId)
        request.isPublicity = isPublicity

        self.auctionService.serviceStub.getAuctionItemNumByCategoryId(None, request, None)

    def buyItemByItemId(self, playerGBID, itemId, number, price, extra):
        if not self.isAuctionCenterActive():
            INFO_MSG("buyItemByItemId auctionCenter is not active")
            return

        request = BuyItemByItemIdReq()
        request.itemId = itemId
        request.playerGBID = playerGBID
        request.number = number
        request.price = price
        request.extra = json.dumps(extra)

        self.auctionService.serviceStub.buyItemByItemId(None, request, None)

    def doBuyItemByItemId(self, playerGBID, errno, itemId, number, price, remainNum, auctionItemUUIDs, totalPrice,
                          extra):
        if not self.isAuctionCenterActive(False):
            INFO_MSG("doBuyItemByItemId auctionCenter is not active")
            return

        request = DoBuyItemByItemIdReq()
        request.playerGBID = playerGBID
        request.errno = errno
        request.itemId = itemId
        request.number = number
        request.price = price
        request.remainNum = remainNum
        request.totalPrice = totalPrice
        for auctionItemUUID in auctionItemUUIDs:
            request.auctionItemUUIDs.append(auctionItemUUID)
        request.extra = json.dumps(extra)

        self.auctionService.serviceStub.doBuyItemByItemId(None, request, None)

    def getAuctionItemsByAuctionIdList(self, playerGBID, categoryId, auctionIdList):
        if not self.isAuctionCenterActive():
            INFO_MSG("getAuctionItemsByAuctionIdList auctionCenter is not active")
            return

        request = GetAuctionItemByAuctionIdsReq()
        request.playerGBID = playerGBID
        request.categoryId = categoryId
        for auctionId in auctionIdList:
            request.auctionIds.append(auctionId)

        self.auctionService.serviceStub.getAuctionItemsByAuctionIds(None, request, None)

class AuctionStubService(GameServer):
    # auctionStub: callback obj
    # address: tuple of (ip, port)
    def __init__(self, auctionStub, address):
        self.address = address
        self.auctionStub = auctionStub
        self.channel = RpcChannel.RpcChannel(self)
        self.serviceStub = AuctionServer_Stub(self.channel)
        address = address.split(':')
        self.channel.connect((address[0], int(address[1])))

    def on_connected(self):
        self._reportServerId()

    def on_disconnected(self):
        INFO_MSG("disconnected from auction service:", self.address)

    def _reportServerId(self):
        request = ServerInfoMessage()
        request.serverId = gameconfig.serverId()
        request.compId = KBEngine.getComponentGroupOrder()
        request.serverName = gameglobal.curServerName

        self.serviceStub.registerServer(None, request, None)

    def activeTickCallback(self, rpc_controller, request, done):
        pass

    def transAuctionItem(self, item):
        if not item or item.auctionItemUUID == 0:
            return
        itemDict = {
            "itemId": item.itemData.itemId,
            "itemNum": item.itemData.itemNum,
            "uniqueId": item.itemData.uniqueId,
            "bindType": item.itemData.bindType,
            "createTime": item.itemData.createTime,
            "expireTime": item.itemData.expireTime,
            "attrJson": item.itemData.attrJson,
        }
        itemData = itemFactory.ItemFactory.createItemWithSavedDict(itemDict)

        extraInfo = json.loads(item.extraInfo)
        auctionItem = auction.AuctionItem(auctionType=item.auctionType,
                                          auctionItemUUID=item.auctionItemUUID,
                                          addTime=item.addTime,
                                          itemData=itemData,
                                          price=item.price,
                                          number=item.number,
                                          bagType=item.bagType,
                                          source=item.source,
                                          status=item.status,
                                          locked=item.locked,
                                          extraInfo=extraInfo,
                                          tCreate=item.tCreate)
        auctionItem.fromPlayerGBID = item.fromPlayerGBID
        return auctionItem

    def transItemData(self, itemData):
        if not itemData or itemData.itemId == 0:
            return
        itemDict = {
            "itemId": itemData.itemId,
            "itemNum": itemData.itemNum,
            "uniqueId": itemData.uniqueId,
            "bindType": itemData.bindType,
            "createTime": itemData.createTime,
            "expireTime": itemData.expireTime,
            "attrJson": itemData.attrJson,
        }
        return itemDict

    def transAuctionClientInfo(self, item):
        if not item or item.auctionItemUUID == 0:
            return
        m_resultData = {
            "auctionType": item.auctionType,
            "auctionItemUUID": item.auctionItemUUID,
            "addTime": item.addTime,
            "itemId": item.itemId,
            "uniqueId": item.uniqueId,
            "price": item.price,
            "number": item.number,
            "status": item.status,
            "createTime": item.tCreate,
            "extra": json.dumps({"attrJson": {}})
        }

        return m_resultData

    def replySaleItem(self, rpc_controller, request, done):
        playerGBID = request.playerGBID
        auctionItem = request.auctionItem
        extra = json.loads(request.extra)
        auctionItem = self.transAuctionItem(auctionItem)
        INFO_MSG("replySaleItem", playerGBID, auctionItem, extra)
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [playerGBID], "doSaleItemInCoinAuction", (auctionItem, extra),
            None, '', ())

    def replyDoSaleItem(self, rpc_controller, request, done):
        playerGBID = request.playerGBID
        auctionItem = self.transAuctionItem(request.auctionItem)
        extra = json.loads(request.extra)
        INFO_MSG("replyDoSaleItem", playerGBID, auctionItem, extra)
        if playerGBID:
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                [playerGBID], "onSaleItemInCoinAuction", (auctionItem, extra),
                None, '', ())

            LogTrackingMgr.LogTrackingMgr.Auction_ItemSale(playerGBID, extra.get('opUUID'), auctionItem.auctionItemUUID, auctionItem.itemId, \
                                                        auctionItem.number, auctionItem.price, auctionItem.totalPrice, extra.get('isPublicity'))

    def replyBuyItem(self, rpc_controller, request, done):
        playerGBID = request.playerGBID
        auctionItemUUID = request.auctionItemUUID
        price = request.price
        extra = json.loads(request.extra)
        extra['code'] = request.code
        INFO_MSG("replyBuyItem", playerGBID, auctionItemUUID, price, extra)
        if playerGBID != 0:
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                [playerGBID], "doBuyItemInCoinAuctionByAuctionItemUUID", (auctionItemUUID, price, extra),
                None, '', ())

    def replyDoBuyItem(self, rpc_controller, request, done):
        playerGBID = request.playerGBID
        extra = json.loads(request.extra)
        auctionItem = self.transAuctionItem(request.auctionItem)
        INFO_MSG("replyDoBuyItem", playerGBID, auctionItem, extra)
        isOK = extra.get('isOK')
        if not isOK:
            pass
        else:
            if playerGBID:
                number = extra.get('auctionBuyItemNum')
                opUUID = extra.get('opUUID')
                price = auctionItem.price
                if price > 0:
                    now = utils.getNow()
                    redisUtils.PlayerBuyAuctionItemRecord.recordMessage(
                        now, playerGBID, auctionItem.itemId, number, price,
                        auctionItem.itemData.toItemSavedDict(), opUUID)
                stub = gameengine.getGlobalBase('PlayerStub')
                stub.doOnOthersBase(
                    [playerGBID, ],
                    "onBuyItemInCoinAuctionByAuctionItemUUID",
                    (auctionItem, price, extra),
                    stub, 'recordOfflineCallback',
                    (playerGBID, 'onBuyItemInCoinAuctionByAuctionItemUUIDOffline', (auctionItem, price, extra)))
                LogTrackingMgr.LogTrackingMgr.Auction_ItemBuy(playerGBID, opUUID, auctionItem.auctionItemUUID, auctionItem.itemId, number, price)

    def replyCancelSaleItem(self, rpc_controller, request, done):
        playerGBID = request.playerGBID
        auctionItem = self.transAuctionItem(request.auctionItem)
        extra = json.loads(request.extra)
        INFO_MSG("replyCancelSaleItem", playerGBID, auctionItem, extra)
        gameengine.broadcastBaseapp('onSyncNewAuctionItemCache', (playerGBID, auctionItem.auctionItemUUID, auctionItem.itemData.itemId))
        if playerGBID != 0:
            errno = extra.get('errno')
            errno = gameconst.AuctionErrno._errno(errno)
            if not auctionItem or errno != gameconst.AuctionErrno.AUCTION_OK:
                auctionItemUUID = extra.get('auctionItemUUID', -1)
                gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                    [playerGBID], "onCancelSaleItemInCoinAuctionFail", (errno.errno, auctionItemUUID, extra),
                    None, '', ())
                return
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                [playerGBID], "cancelSaleItemInCoinAuctionCallback", (auctionItem, extra),
                None, '', ())

    def replyDoCancelSaleItem(self, rpc_controller, request, done):
        playerGBID = request.playerGBID
        errno = request.errno
        auctionItem = self.transAuctionItem(request.auctionItem)
        extra = json.loads(request.extra)
        INFO_MSG("replyDoCancelSaleItem", playerGBID, errno, auctionItem, extra)

        if playerGBID:
            retCode = gameconst.AuctionErrno._errno(errno)
            if not auctionItem or retCode != gameconst.AuctionErrno.AUCTION_OK:
                auctionItemUUID = extra.get('auctionItemUUID', -1)
                m_playerStub = gameengine.getGlobalBase('PlayerStub')
                m_playerStub.doOnOthersBase(
                    [playerGBID], "onCancelSaleItemInCoinAuctionFail", (errno, auctionItemUUID, extra),
                    None, '', ())
                return
            m_playerStub = gameengine.getGlobalBase('PlayerStub')
            m_playerStub.doOnOthersBase(
                [playerGBID], "doCancelSaleItemInCoinAuction", (errno, auctionItem, extra),
                m_playerStub, 'recordOfflineCallback',
                (playerGBID, 'doCancelSaleItemInCoinAuction', (errno, auctionItem, extra)))
            LogTrackingMgr.LogTrackingMgr.Auction_ItemCancel(playerGBID, auctionItem.auctionItemUUID, auctionItem.itemId, \
                                                        auctionItem.number, auctionItem.price, auctionItem.totalPrice, \
                                                        auctionItem.itemData.createTime, auctionItem.addTime, auctionItem.itemData.expireTime, auctionItem.status)
            
    def replySearchItemsByItemId(self, rpc_controller, request, done):
        playerGBID = request.playerGBID
        itemIds = []
        for itemId in request.itemIds:
            itemIds.append(itemId)

        limit = request.limit
        offset = request.offset
        auctionItems = request.auctionItems
        totalNum = request.totalNum
        extra = json.loads(request.extra)
        searchResults = []
        for item in auctionItems:
            searchResults.append(self.transAuctionItem(item))
        isPublicity = request.isPublicity
        INFO_MSG("replySearchItemsByItemId", playerGBID, itemIds, limit, offset, totalNum, extra, isPublicity)

        if playerGBID != 0:
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                [playerGBID], "onSearchCoinAuctionItemsByItemId",
                (itemIds, limit, offset, searchResults, totalNum, extra, isPublicity),
                None, '', ())

    def replyGetItemLastAndAvgPrice(self, rpc_controller, request, done):
        playerGBID = request.playerGBID
        itemId = request.itemId
        lastPrice = request.lastPrice
        avgPrice = request.avgPrice
        extra = json.loads(request.extra)
        INFO_MSG("replyGetItemLastAndAvgPrice", playerGBID, itemId, lastPrice, avgPrice, extra)

        if playerGBID != 0:
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                [playerGBID], "onGetItemLastAndAvgPrice",
                (itemId, None, lastPrice, avgPrice, extra),
                None, '', ())

    def replyGetPlayerAuctionItems(self, rpc_controller, request, done):
        playerGBID = request.playerGBID
        auctionItems = []
        for item in request.auctionItems:
            auctionItems.append(self.transAuctionItem(item))

        extra = json.loads(request.extra)
        INFO_MSG("replyGetPlayerAuctionItems", playerGBID, auctionItems, extra)

        if playerGBID != 0:
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                [playerGBID], "onGetCoinAuctionPlayerInfo",
                (auctionItems, extra),
                None, '', ())

    def replyLoadPlayerAuctionItem(self, rpc_controller, request, done):
        playerGBID = request.playerGBID
        auctionItemUUIDs = []
        for auctionItemUUID in request.auctionItemUUIDs:
            auctionItemUUIDs.append(auctionItemUUID)
        extra = json.loads(request.extra)
        INFO_MSG("replyLoadPlayerAuctionItem", playerGBID, auctionItemUUIDs, extra)

        if playerGBID != 0:
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                [playerGBID], "onLoadPlayerCoinAuctionData",
                (auctionItemUUIDs, extra),
                None, '', ())

    def replyDoCommand(self, rpc_controller, request, done):
        command = request.command
        extra = request.extra

        INFO_MSG("replyDoCommand", command, extra)

    def onItemBeSaled(self, rpc_controller, request, done):
        playerGBID = request.playerGBID
        auctionItem = self.transAuctionItem(request.auctionItem)
        number = request.number
        extra = json.loads(request.extra)
        INFO_MSG("onItemBeSaled", playerGBID, auctionItem, number, extra)

        now = utils.getNow()
        opUUID = extra.get('opUUID', 0)

        totalPrice = extra.get('totalPrice')
        auctionTaxRate = AUC_CONST.datas['auctionTaxRate']['value']
        totalPriceTax = round(totalPrice * auctionTaxRate/100)
        totalPriceInDeductTax = totalPrice - totalPriceTax

        fromPlayerGBID = auctionItem.fromPlayerGBID
        if fromPlayerGBID:
            m_playerStub = gameengine.getGlobalBase('PlayerStub')
            redisUtils.PlayerCoinAuctionRecord.recordMessage(
                now, fromPlayerGBID, auctionItem.itemId, number, totalPriceInDeductTax,
                auctionItem.itemData.toItemSavedDict(), opUUID)

            m_playerStub.doOnOthersBase(
                [fromPlayerGBID], "onPlayerGlobalAuctionItemBeSaled",
                (auctionItem, number, auctionItem.price, now, totalPriceInDeductTax, extra),
                m_playerStub, 'recordOfflineCallback',
                (fromPlayerGBID, 'onPlayerGlobalAuctionItemBeSaledOffline',
                 (auctionItem, number, auctionItem.price, now, totalPriceInDeductTax, extra)))


        crossSiegeWarServerInfo = gameconfig.crossSiegeWarServerInfo()
        _stub = iRouter.RemoteServerStubEntityCall(crossSiegeWarServerInfo['crossServerId'], 'CrossSiegeWarStub')
        _stub.onCityAuctionTax(gameconfig.serverId(), totalPriceTax)

        LogTrackingMgr.LogTrackingMgr.Auction_ItemDeal(playerGBID, auctionItem.fromPlayerGBID, opUUID, auctionItem.auctionItemUUID, \
                                                       auctionItem.itemId, auctionItem.number, totalPrice, totalPriceInDeductTax, totalPriceTax)

    def replyGetAuctionItemNumByCategoryId(self, rpc_controller, request, done):
        playerGBID = request.playerGBID
        categoryId = request.categoryId
        itemIds = []
        for itemId in request.itemIds:
            itemIds.append(itemId)
        itemNums = []
        for itemNum in request.itemNums:
            itemNums.append(itemNum)
        prices = []
        for price in request.prices:
            prices.append(price)
        isPublicity = request.isPublicity
        INFO_MSG("replyGetAuctionItemNumByCategoryId", playerGBID, categoryId, itemIds, itemNums, prices, isPublicity)

        if playerGBID != 0:
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                [playerGBID], "onGetItemNumByCategoryIdResp",
                (categoryId, itemIds, itemNums, prices, isPublicity),
                None, '', ())

    def replyBuyItemByItemId(self, rpc_controller, request, done):
        playerGBID = request.playerGBID
        itemId = request.itemId
        number = request.number
        price = request.price
        extra = json.loads(request.extra)
        remainNum = request.remainNum
        auctionItemUUIDs = []
        for auctionItemUUID in request.auctionItemUUIDs:
            auctionItemUUIDs.append(auctionItemUUID)
        totalPrice = request.totalPrice
        INFO_MSG("replyBuyItemByItemId", playerGBID, itemId, number, price, extra, remainNum, auctionItemUUIDs,
                  totalPrice)

        if playerGBID != 0:
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                [playerGBID], "onBuyItemByItemIdResp",
                (itemId, number, price, remainNum, auctionItemUUIDs, totalPrice, extra),
                None, '', ())

    def replyDoBuyItemByItemId(self, rpc_controller, request, done):
        playerGBID = request.playerGBID
        errno = request.errno
        itemId = request.itemId
        number = request.number
        price = request.price
        remainNum = request.remainNum
        itemData = self.transItemData(request.itemData)
        totalPrice = request.totalPrice
        extra = json.loads(request.extra)
        INFO_MSG("replyDoBuyItemByItemId", playerGBID, errno, itemId, number, price, remainNum, itemData, totalPrice,
                  extra)
        if playerGBID != 0:
            if totalPrice > 0:
                now = utils.getNow()
                opUUID = extra.get('opUUID')
                buyNum = number - remainNum
                redisUtils.PlayerBuyAuctionItemRecord.recordMessage(
                    now, playerGBID, itemId, number, totalPrice,
                    itemData.toItemSavedDict(), opUUID)
            m_playerStub = gameengine.getGlobalBase('PlayerStub')
            m_playerStub.doOnOthersBase(
                [playerGBID], "onDoBuyItemByItemIdResp",
                (errno, itemId, number, price, remainNum, itemData, totalPrice, extra),
                m_playerStub, 'recordOfflineCallback',
                (playerGBID, 'onDoBuyItemByItemIdResp',
                 (errno, itemId, number, price, remainNum, itemData, totalPrice, extra)))

    def replyGetCurrentSaleItemInfo(self, rpc_controller, request, done):
        playerGBID = request.playerGBID
        itemId = request.itemId
        lastPrice = request.lastPrice
        avgPrice = request.avgPrice
        isPublicity = request.isPublicity
        extra = json.loads(request.extra)
        auctionItems = []
        for item in request.auctionItems:
            auctionItems.append(self.transAuctionItem(item))
        INFO_MSG("replyGetCurrentSaleItemInfo", playerGBID, itemId, lastPrice, avgPrice, extra, auctionItems)

        if playerGBID != 0:
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                [playerGBID], "onGetCurrentSaleItemInfoResp",
                (itemId, lastPrice, avgPrice, extra, auctionItems, isPublicity),
                None, '', ())

    def replyGetAuctionItemsByAuctionIds(self, rpc_controller, request, done):
        playerGBID = request.playerGBID
        categoryId = request.categoryId
        auctionItems = []
        for item in request.auctionItems:
            auctionItems.append(self.transAuctionItem(item))

        INFO_MSG("replyGetAuctionItemsByAuctionIds", playerGBID, categoryId, auctionItems)

        if playerGBID != 0:
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                [playerGBID], "onGetAuctionItemsByAuctionIdsResp",
                (categoryId, auctionItems),
                None, '', ())


