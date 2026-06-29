# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *

import random

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
import AuctionSnatchRecords
import mailAssistor
import dropAward
import utils
import dataUtils

import auction_auctionConst as AUC_CONST
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import mall_coinPrice

from rpc import RpcChannel, TcpClient
from proto.gameServerAuction_pb2 import (
    AuctionServer_Stub, GameServer, ServerInfoMessage, GetItemLastAndAvgPriceReq, Void,
    SaleItemReq, DoSaleItemReq, BuyItemReq, DoBuyItemReq, CancelSaleItemReq, DoCancelSaleItemReq,
    SearchItemsByItemIdReq, GetPlayerAuctionItemsReq, LoadPlayerAuctionItemReq, DoCommandReq,
    GetItemNumByCategoryIdReq, BuyItemByItemIdReq, DoBuyItemByItemIdReq, GetCurrentSaleItemInfoReq, 
    GetAuctionItemByAuctionIdsReq, OnItemSalingInfo)

import gameglobal
import gameconst
import json
import LogTrackingMgr
import auction_onSaleChatting as ASC

class AuctionStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer):
    def __init__(self, **kwargs):
        iGlobal.IGlobal.__init__(self)
        iBaseNoCell.IBaseNoCell.__init__(self)
        iTimer.ITimer.__init__(self)

        self.auctionService = None
        self.SNATCH_LOCK_TTL = AUC_CONST.datas['auctionLuckyBuyTime']['value'] * 2
        self.SNATCH_LOCK_PREFIX = 'auction:snatch:lock:'

    def doNext(self):
        self._fullPrepare()

    def _fullPrepare(self):
        self.pyAddTimer(1, 1, gametimer.AUCTION_STUB_ASYNC_TICK)
        gameglobal.localBaseApp.initAysncore()
        self.pyAddTimer(gameconst.CENTRAL_SERVICE_HEARTBEAT_INTERVAL, gameconst.CENTRAL_SERVICE_HEARTBEAT_INTERVAL,
                        gametimer.AUCTION_STUB_ACTIVE_TICK)
        self.pyAddTimer(1, gameconst.ONE_MINUTE_COST_SECONDS, gametimer.AUCTION_STUB_AVG_PRICE_CACHE)
        self.pyAddTimer(1, 1, gametimer.AUCTION_SNATCH)
        gameglobal.mallItemPriceCache.update(self.mallItemPriceDict)
        gameglobal.mallItemLastUpdateTime.update(self.mallItemLastUpdateTime)

    def onTimer(self, tid, userArg):
        self._onTimerTrigger(tid, userArg)
        if userArg == gametimer.AUCTION_STUB_ASYNC_TICK:
            self._connectAuctionCenter()
        elif userArg == gametimer.AUCTION_STUB_ACTIVE_TICK:
            self._checkAuctionCenterActive()
        elif userArg == gametimer.AUCTION_STUB_AVG_PRICE_CACHE:
            self._cacheAvgPrice()
        elif userArg == gametimer.AUCTION_SNATCH:
            self.auctionSnatch()

    def reloadScript(self):
        super(AuctionStub, self).reloadScript()

    def _connectAuctionCenter(self):
        if not gameconfig.enableAuction():
            return

        host = gameconfig.auctionServerHost()
        if not (self.auctionService and self.auctionService.channel.dispatcher):
            LOG_INFO('connect auctionCenter---------:', host)
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

    def saleItem(self, playerGBID, itemDict, totalPrice, number, bagType, extra, addPublicityTime):
        if not self.isAuctionCenterActive():
            LOG_INFO("saleItem auctionCenter is not active")
            return

        request = SaleItemReq()
        request.playerGBID = playerGBID
        request.itemDict = itemDict
        request.totalPrice = totalPrice
        request.number = number
        request.bagType = bagType
        request.extra = json.dumps(extra)
        request.addPublicityTime = addPublicityTime

        self.auctionService.serviceStub.saleItem(None, request, None)

    def doSaleItem(self, auctionItemUUID, playerGBID, extra, result, addPublicityTime):
        if not self.isAuctionCenterActive(False):
            LOG_INFO("doSaleItem auctionCenter is not active")
            return

        request = DoSaleItemReq()
        request.auctionItemUUID = auctionItemUUID
        request.playerGBID = playerGBID
        request.extra = json.dumps(extra)
        request.result = result

        self.auctionService.serviceStub.doSaleItem(None, request, None)

    def buyItem(self, playerGBID, auctionItemUUID, number, extra):
        if not self.isAuctionCenterActive():
            LOG_INFO("buyItem auctionCenter is not active")
            return

        request = BuyItemReq()
        request.playerGBID = playerGBID
        request.auctionItemUUID = auctionItemUUID
        request.number = number
        request.extra = json.dumps(extra)

        self.auctionService.serviceStub.buyItem(None, request, None)

    def doBuyItem(self, auctionItemUUID, playerGBID, errno, price, publicityEndTime, buyType, extra):
        LOG_INFO("doBuyItem ", auctionItemUUID, playerGBID, errno, price, publicityEndTime, buyType, extra)    
        # 成功付钱
        if errno == 1:
            # 抢购
            if buyType == gameconst.AuctionBuyType.SNATCH:
                data = self.auctionSnatchRecords.get(auctionItemUUID, None)
                if not data:
                    data = AuctionSnatchRecords.AuctionSnatchRecords(auctionItemUUID, extra.get('auctionBuyItemId'), price, extra.get('number'), publicityEndTime)
                    self.auctionSnatchRecords[auctionItemUUID] = data
                # 已完成直接返还
                if data.isFinished():
                    self.doSnatchReturnBack(playerGBID, extra.get('tlogProps').get('role_name'), extra.get('opUUID'), extra.get('auctionBuyItemId'), price)
                    return
                data.addAuctionSnatchRecords(playerGBID, extra.get('tlogProps').get('role_name'), extra.get('opUUID'))
                # 发消息
                gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                                        [playerGBID, ], 'onMessagePre', (AUC_CONST.datas['auctionLuckyBuyCheck']['value'], []),
                                        None, '', ())
                return
            
        if not self.isAuctionCenterActive():
            LOG_INFO("doBuyItem auctionCenter is not active")
            return
        self.startDoBuyAction(auctionItemUUID, playerGBID, price, extra, errno)

    def startDoBuyAction(self, auctionItemUUID, playerGBID, price, extra, errno):
        request = DoBuyItemReq()
        request.auctionItemUUID = auctionItemUUID
        request.playerGBID = playerGBID
        request.errno = errno
        request.price = price
        request.extra = json.dumps(extra)

        self.auctionService.serviceStub.doBuyItem(None, request, None)

    def cancelSaleItem(self, playerGBID, auctionItemUUID, extra):
        if not self.isAuctionCenterActive():
            LOG_INFO("cancelSaleItem auctionCenter is not active")
            return

        request = CancelSaleItemReq()
        request.playerGBID = playerGBID
        request.auctionItemUUID = auctionItemUUID
        request.extra = json.dumps(extra)

        self.auctionService.serviceStub.cancelSaleItem(None, request, None)

    def doCancelSaleItem(self, auctionItemUUID, playerGBID, extra):
        if not self.isAuctionCenterActive(False):
            LOG_INFO("doCancelSaleItem auctionCenter is not active")
            return

        request = DoCancelSaleItemReq()
        request.auctionItemUUID = auctionItemUUID
        request.playerGBID = playerGBID
        request.extra = json.dumps(extra)

        self.auctionService.serviceStub.doCancelSaleItem(None, request, None)

    def searchItemsByItemId(self, playerGBID, itemIds, limit, offset, isPublicity, extra):
        if not self.isAuctionCenterActive():
            LOG_INFO("searchItemsByItemId auctionCenter is not active")
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
            LOG_INFO("getItemLastAndAvgPrice auctionCenter is not active")
            return

        request = GetItemLastAndAvgPriceReq()
        request.playerGBID = playerGBID
        request.itemId = itemId
        request.extra = json.dumps(extra)

        self.auctionService.serviceStub.getItemLastAndAvgPrice(None, request, None)

    def getCurrentSaleItemInfo(self, playerGBID, itemId, isPublicity, extra):
        if not self.isAuctionCenterActive():
            LOG_INFO("getCurrentSaleItemInfo auctionCenter is not active")
            return

        request = GetCurrentSaleItemInfoReq()
        request.playerGBID = playerGBID
        request.itemId = itemId
        request.isPublicity = isPublicity
        request.extra = json.dumps(extra)

        self.auctionService.serviceStub.getCurrentSaleItemInfo(None, request, None)

    def getPlayerAuctionItems(self, playerGBID, extra):
        if not self.isAuctionCenterActive():
            LOG_INFO("getPlayerAuctionItems auctionCenter is not active")
            return

        request = GetPlayerAuctionItemsReq()
        request.playerGBID = playerGBID
        request.extra = json.dumps(extra)

        self.auctionService.serviceStub.getPlayerAuctionItems(None, request, None)

    def loadPlayerAuctionItem(self, playerGBID, extra):
        if not self.isAuctionCenterActive():
            LOG_INFO("loadPlayerAuctionItem auctionCenter is not active")
            return

        request = LoadPlayerAuctionItemReq()
        request.playerGBID = playerGBID
        request.extra = json.dumps(extra)

        self.auctionService.serviceStub.loadPlayerAuctionItem(None, request, None)

    def doCommand(self, command, extra):
        if not self.isAuctionCenterActive():
            LOG_INFO("doCommand auctionCenter is not active")
            return

        request = DoCommandReq()
        request.command = command
        request.extra = json.dumps(extra)

        self.auctionService.serviceStub.doCommand(None, request, None)

    def getAuctionItemNumByCategoryId(self, playerGBID, categoryId, itemIdList, isPublicity):
        if not self.isAuctionCenterActive():
            LOG_INFO("getAuctionItemNumByCategoryId auctionCenter is not active")
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
            LOG_INFO("buyItemByItemId auctionCenter is not active")
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
            LOG_INFO("doBuyItemByItemId auctionCenter is not active")
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
            LOG_INFO("getAuctionItemsByAuctionIdList auctionCenter is not active")
            return

        request = GetAuctionItemByAuctionIdsReq()
        request.playerGBID = playerGBID
        request.categoryId = categoryId
        for auctionId in auctionIdList:
            request.auctionIds.append(auctionId)

        self.auctionService.serviceStub.getAuctionItemsByAuctionIds(None, request, None)

    def _cacheAvgPrice(self):
        if not utils.checkDiffDay(utils.curTS(), utils.curTS() - gameconst.ONE_MINUTE_COST_SECONDS, gameconst.GENERAL_CYCLE_TIME + gameconst.ONE_MINUTE_COST_SECONDS):
            return
        LOG_INFO("cacheAvgPrice")
        for mallID in mall_coinPrice.type2ID[gameconst.MallItemType.DYNAMIC_PRICE]:
            data = mall_coinPrice.datas[mallID]
            itemId = data['itemId']
            self.getItemLastAndAvgPrice(0, itemId, {})

    def _onLockResult(self, cid, err, result, auctionUUID, itemId, price, number, records):
        if err:
            LOG_ERR('snatch:: lock error', err)
            # redis报错，全部返还
            self.doBatchSnatchRetunBack(itemId, price, records.records)
            return

        if result != 'OK':
            LOG_INFO('snatch:: already in flight')
            # 没抢到锁，全部返还
            self.doBatchSnatchRetunBack(itemId, price, records.records)
            return
        # 开始抢购
        self.startSnatch(auctionUUID, itemId, price, number, records)

    def auctionSnatch(self):
        now = utils.curTS()
        for auctionSnatchRecord in self.auctionSnatchRecords.values():
            # 完成了，不处理
            if auctionSnatchRecord.isFinished():
                continue
            # 交易行关了，全部走返还
            if not self.isAuctionCenterActive():
                auctionSnatchRecord.setFinished()
                self.doBatchSnatchRetunBack(auctionSnatchRecord.itemId, auctionSnatchRecord.price, auctionSnatchRecord.records)
                LOG_INFO("auctionSnatch auctionCenter is not active")
                return
            if now >= auctionSnatchRecord.publicityEndTime:
                auctionSnatchRecord.setFinished()
                # 没人就不抢了
                if len(auctionSnatchRecord.records) == 0:
                    continue
                gameglobal.localBaseApp.getRedisClient().setnxex(
                    self.SNATCH_LOCK_PREFIX + str(auctionSnatchRecord.auctionUUID), 1,
                    self.SNATCH_LOCK_TTL,
                    lambda cid, err, result, 
                    auctionUUID=auctionSnatchRecord.auctionUUID, 
                    itemId=auctionSnatchRecord.itemId, 
                    price=auctionSnatchRecord.price,
                    number=auctionSnatchRecord.number,
                    rcd=auctionSnatchRecord:
                        self._onLockResult(cid, err, result, auctionUUID, itemId, price, number, rcd))    

    def startSnatch(self, auctionUUID, itemId, price, number, records):
        LOG_INFO('startSnatch ', auctionUUID, itemId, price, number)
        idx = random.randint(0, len(records.records) - 1)
        # 幸运儿随机
        record = records.records.pop(idx)
        # 其他人走返还
        self.doBatchSnatchRetunBack(itemId, price, records.records)
        # 清理本次数据
        records.records.clear()
        # 开启去买
        extra = {}
        extra['number'] = number
        extra['selectItemLocked'] = 1
        extra['auctionBuyItemNum'] = number
        extra['opUUID'] = record.opUUID
        props = {'role_name':record.name}
        extra['tlogProps'] = props
        self.startDoBuyAction(auctionUUID, record.gbId, price, extra, gameconst.AuctionErrno.ERR_AUCTION_OK.errno)

    def doBatchSnatchRetunBack(self, itemId, price, records):
        for record in records:
            self.doSnatchReturnBack(record.gbId, record.name, record.opUUID, itemId, price)

    def doSnatchReturnBack(self, gbId, name, opUUID, itemId, price):
        # 发消息
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                                [gbId, ], 'onMessagePre', (AUC_CONST.datas['auctionLuckyBuyFail']['value'], [name]),
                                None, '', ())
        # 退还消耗
        attachVal = dropAward.MailAttachVal()
        attachVal.addWealthByItemId(gameconst.ItemIdEnum.MONEY, price)
        mailAssistor.sendMailToPlayers([gbId], AUC_CONST.datas['auctionLuckyBuyMail']['value'], extraAttach=attachVal, opUUID=opUUID, 
                                       despArgs=(itemId, gbId), srcType=AAC_AACDD.datas.BONUS_SRC_AUCTION_SNATCH_FAIL)

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
        LOG_INFO("disconnected from auction service:", self.address)

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
                                          addPublicityTime=item.addPublicityTime,
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

    def replySaleItem(self, rpc_controller, request, done):
        playerGBID = request.playerGBID
        auctionItem = request.auctionItem
        extra = json.loads(request.extra)
        auctionItem = self.transAuctionItem(auctionItem)
        LOG_INFO("replySaleItem", playerGBID, auctionItem, extra)
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [playerGBID], "doSaleItemInCoinAuction", (auctionItem, extra),
            None, '', ())

    def replyDoSaleItem(self, rpc_controller, request, done):
        playerGBID = request.playerGBID
        auctionItem = self.transAuctionItem(request.auctionItem)
        extra = json.loads(request.extra)
        LOG_INFO("replyDoSaleItem", playerGBID, auctionItem, extra)
        if playerGBID:
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                [playerGBID], "onSaleItemInCoinAuction", (auctionItem, extra),
                None, '', ())

            LogTrackingMgr.LogTrackingMgr.auction_item_sale(playerGBID, '', playerGBID, extra.get('opUUID'), auctionItem.auctionItemUUID, auctionItem.itemId, \
                                                        dataUtils.getItemType(auctionItem.itemId), auctionItem.number, auctionItem.price, auctionItem.totalPrice, auctionItem.addPublicityTime > 0)

    def replyBuyItem(self, rpc_controller, request, done):
        playerGBID = request.playerGBID
        auctionItemUUID = request.auctionItemUUID
        price = request.price
        publicityEndTime = request.publicityEndTime
        buyType = request.buyType
        extra = json.loads(request.extra)
        extra['code'] = request.code
        LOG_INFO("replyBuyItem", playerGBID, auctionItemUUID, price, extra)

        if playerGBID != 0:
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                [playerGBID], "doBuyItemInCoinAuctionByAuctionItemUUID", (auctionItemUUID, price, publicityEndTime, buyType, extra),
                None, '', ())

    def replyDoBuyItem(self, rpc_controller, request, done):
        playerGBID = request.playerGBID
        extra = json.loads(request.extra)
        auctionItem = self.transAuctionItem(request.auctionItem)
        LOG_INFO("replyDoBuyItem", playerGBID, auctionItem, extra)
        isOK = extra.get('isOK')
        if not isOK:
            pass
        else:
            if playerGBID:
                number = extra.get('auctionBuyItemNum')
                opUUID = extra.get('opUUID')
                price = auctionItem.price
                if price > 0:
                    now = utils.curTS()
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
                LogTrackingMgr.LogTrackingMgr.Auction_ItemBuy(playerGBID, '', playerGBID, opUUID, auctionItem.auctionItemUUID, auctionItem.itemId, number, price)

    def replyCancelSaleItem(self, rpc_controller, request, done):
        playerGBID = request.playerGBID
        auctionItem = self.transAuctionItem(request.auctionItem)
        extra = json.loads(request.extra)
        LOG_INFO("replyCancelSaleItem", playerGBID, auctionItem, extra)
        gameengine.broadcastBaseapp('onSyncNewAuctionItemCache', (playerGBID, auctionItem.auctionItemUUID, auctionItem.itemData.itemId))
        if playerGBID != 0:
            errno = extra.get('errno')
            errno = gameconst.AuctionErrno._errno(errno)
            if not auctionItem or errno != gameconst.AuctionErrno.ERR_AUCTION_OK:
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
        LOG_INFO("replyDoCancelSaleItem", playerGBID, errno, auctionItem, extra)

        if playerGBID:
            retCode = gameconst.AuctionErrno._errno(errno)
            if not auctionItem or retCode != gameconst.AuctionErrno.ERR_AUCTION_OK:
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
            LogTrackingMgr.LogTrackingMgr.auction_item_cancel(playerGBID, '', playerGBID, auctionItem.auctionItemUUID, auctionItem.itemId, \
                                                        dataUtils.getItemType(auctionItem.itemId), auctionItem.number, auctionItem.price, auctionItem.totalPrice, \
                                                        auctionItem.addPublicityTime > 0, auctionItem.itemData.createTime, auctionItem.addTime, auctionItem.itemData.expireTime, auctionItem.status)
            
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
        LOG_INFO("replySearchItemsByItemId", playerGBID, itemIds, limit, offset, totalNum, extra, isPublicity)

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
        LOG_INFO("replyGetItemLastAndAvgPrice", playerGBID, itemId, lastPrice, avgPrice, extra)

        utils.updateMallItemPriceCache(self.auctionStub, itemId, avgPrice)

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
        LOG_INFO("replyGetPlayerAuctionItems", playerGBID, auctionItems, extra)

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
        LOG_INFO("replyLoadPlayerAuctionItem", playerGBID, auctionItemUUIDs, extra)

        if playerGBID != 0:
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                [playerGBID], "onLoadPlayerCoinAuctionData",
                (auctionItemUUIDs, extra),
                None, '', ())

    def replyDoCommand(self, rpc_controller, request, done):
        command = request.command
        extra = request.extra

        LOG_INFO("replyDoCommand", command, extra)

    def onItemBeSaled(self, rpc_controller, request, done):
        playerGBID = request.playerGBID
        auctionItem = self.transAuctionItem(request.auctionItem)
        number = request.number
        extra = json.loads(request.extra)
        LOG_INFO("onItemBeSaled", playerGBID, auctionItem, number, extra)

        now = utils.curTS()
        opUUID = extra.get('opUUID', 0)

        auctionExtra = auctionItem.extraInfo
        tlogProps = auctionExtra.get('tlogProps', {})
        roleName = tlogProps.get('role_name', '')
        roleAccount = tlogProps.get('role_account', '')
        totalPrice = extra.get('totalPrice')
        auctionTaxRate = AUC_CONST.datas['auctionTaxRate']['value']
        totalPriceTax = round(totalPrice * auctionTaxRate/100)
        totalPriceInDeductTax = totalPrice - totalPriceTax

        fromPlayerGBID = auctionItem.fromPlayerGBID
        if fromPlayerGBID:
            m_playerStub = gameengine.getGlobalBase('PlayerStub')
            redisUtils.PlayerCoinAuctionRecord.recordMessage(
                now, fromPlayerGBID, auctionItem.itemId, number, totalPriceInDeductTax,
                auctionItem.itemData.toItemSavedDict(), opUUID,
                auctionItem.auctionItemUUID, 0)

            m_playerStub.doOnOthersBase(
                [fromPlayerGBID], "onPlayerGlobalAuctionItemBeSaled",
                (auctionItem, number, auctionItem.price, now, totalPriceInDeductTax, extra),
                m_playerStub, 'recordOfflineCallback',
                (fromPlayerGBID, 'onPlayerGlobalAuctionItemBeSaledOffline',
                 (auctionItem, number, auctionItem.price, now, totalPriceInDeductTax, extra)))


        LogTrackingMgr.LogTrackingMgr.auction_item_deal(playerGBID, '', playerGBID, opUUID, auctionItem.auctionItemUUID, \
                                                       auctionItem.itemId, dataUtils.getItemType(auctionItem.itemId), auctionItem.addPublicityTime > 0, \
                                                       auctionItem.number, totalPrice, totalPriceInDeductTax, totalPriceTax, auctionItem.fromPlayerGBID, \
                                                       roleName, roleAccount)
        

        crossSiegeWarServerInfo = gameconfig.crossSiegeWarServerInfo()
        _stub = iRouter.RemoteServerStubEntityCall(crossSiegeWarServerInfo['crossServerId'], 'CrossSiegeWarStub')
        _stub.onCityAuctionTax(gameconfig.serverId(), totalPriceTax)

    def onItemSaling(self, rpc_controller, request, done):
        auctionItemUUID = request.auctionItemUUID
        itemId = request.itemId
        gbId = request.gbId

        gameengine.broadcastBaseapp('onBroadcastToAllClients',
                                         ('onAuctionSaleChatting',
                                          (auctionItemUUID, itemId), ()))

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
        LOG_INFO("replyGetAuctionItemNumByCategoryId", playerGBID, categoryId, itemIds, itemNums, prices, isPublicity)

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
        LOG_INFO("replyBuyItemByItemId", playerGBID, itemId, number, price, extra, remainNum, auctionItemUUIDs,
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
        LOG_INFO("replyDoBuyItemByItemId", playerGBID, errno, itemId, number, price, remainNum, itemData, totalPrice,
                  extra)
        if playerGBID != 0:
            if totalPrice > 0:
                now = utils.curTS()
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
        LOG_INFO("replyGetCurrentSaleItemInfo", playerGBID, itemId, lastPrice, avgPrice, extra, auctionItems)

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

        LOG_INFO("replyGetAuctionItemsByAuctionIds", playerGBID, categoryId, auctionItems)

        if playerGBID != 0:
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                [playerGBID], "onGetAuctionItemsByAuctionIdsResp",
                (categoryId, auctionItems),
                None, '', ())
