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
import itemFactory
import redisUtils

from rpc import RpcChannel, TcpClient
from proto.gameServerLease_pb2 import (
    LeaseServer_Stub, GameServer, ServerInfoMessage, Void,
    LeaseAddItemPrepareReq, LeaseAddItemCommitReq, LeaseAddItemRollbackReq,
    LeaseItemPrepareReq, LeaseItemCommitReq, LeaseItemRollbackReq,
    LeaseCancelItemReq,
    LeaseShopSummaryReq, LeaseShopItemsReq, LeaseMySaleListReq)

import gameglobal
import gameconst
import json
import LogTrackingMgr


class LeaseStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer):
    def __init__(self, **kwargs):
        iGlobal.IGlobal.__init__(self)
        iBaseNoCell.IBaseNoCell.__init__(self)
        iTimer.ITimer.__init__(self)

        self.leaseService = None

    def doNext(self):
        self._fullPrepare()

    def _fullPrepare(self):
        self.pyAddTimer(1, 1, gametimer.LEASE_STUB_ASYNC_TICK)
        gameglobal.localBaseApp.initAysncore()
        self.pyAddTimer(gameconst.CENTRAL_SERVICE_HEARTBEAT_INTERVAL, gameconst.CENTRAL_SERVICE_HEARTBEAT_INTERVAL,
                        gametimer.LEASE_STUB_ACTIVE_TICK)

    def onTimer(self, tid, userArg):
        self._onTimerTrigger(tid, userArg)
        if userArg == gametimer.LEASE_STUB_ASYNC_TICK:
            self._connectLeaseCenter()
        elif userArg == gametimer.LEASE_STUB_ACTIVE_TICK:
            self._checkLeaseCenterActive()

    def reloadScript(self):
        super(LeaseStub, self).reloadScript()

    def _connectLeaseCenter(self):
        if not gameconfig.enableLease():
            return

        host = gameconfig.leaseServerAddress()
        if not (self.leaseService and self.leaseService.channel.dispatcher):
            LOG_INFO('connect leaseCenter---------:', host)
            self.leaseService = LeaseStubService(self, host)

    def _checkLeaseCenterActive(self):
        if not gameconfig.enableLease():
            return

        if self.leaseService and self.leaseService.channel.dispatcher:
            self.leaseService.serviceStub.activeTick(None, Void(), None)

    def isLeaseCenterActive(self, needCheck=True):
        if needCheck and not gameconfig.enableLease():
            return False

        return self.leaseService and self.leaseService.channel.dispatcher

    # ---------- 请求转发 ----------

    def addItemPrepare(self, playerGBID, uniqueId, itemId, itemData, pricePerDay, leaseDays, returnServer, returnOwner, returnTime, returnReason, opUUID):
        if not self.isLeaseCenterActive():
            LOG_ERR("addItemPrepare leaseCenter is not active")
            return

        request = LeaseAddItemPrepareReq()
        request.playerGBID = playerGBID
        request.uniqueId = uniqueId
        request.itemId = itemId
        request.itemData = itemData
        request.pricePerDay = pricePerDay
        request.leaseDays = leaseDays
        request.returnServer = returnServer
        request.returnOwner = returnOwner
        request.returnTime = returnTime
        request.returnReason = returnReason
        request.opUUID = opUUID

        self.leaseService.serviceStub.addItemPrepare(None, request, None)

    def addItemCommit(self, uniqueId, playerGBID, opUUID):
        if not self.isLeaseCenterActive(False):
            LOG_ERR("addItemCommit leaseCenter is not active")
            return

        request = LeaseAddItemCommitReq()
        request.uniqueId = uniqueId
        request.playerGBID = playerGBID
        request.opUUID = opUUID

        self.leaseService.serviceStub.addItemCommit(None, request, None)

    def addItemRollback(self, uniqueId, opUUID):
        if not self.isLeaseCenterActive(False):
            LOG_ERR("addItemRollback leaseCenter is not active")
            return

        request = LeaseAddItemRollbackReq()
        request.uniqueId = uniqueId
        request.opUUID = opUUID

        self.leaseService.serviceStub.addItemRollback(None, request, None)

    def leaseItemPrepare(self, uniqueId, buyerServerId, buyerGBID, opUUID, rentalProp01, rentalProp02):
        if not self.isLeaseCenterActive():
            LOG_ERR("leaseItemPrepare leaseCenter is not active")
            return

        request = LeaseItemPrepareReq()
        request.buyerServerId = buyerServerId
        request.buyerGBID = buyerGBID
        request.uniqueId = uniqueId
        request.opUUID = opUUID
        request.rentalProp01.extend(rentalProp01)
        request.rentalProp02.extend(rentalProp02)

        self.leaseService.serviceStub.leaseItemPrepare(None, request, None)

    def leaseItemCommit(self, uniqueId, playerGBID, opUUID):
        if not self.isLeaseCenterActive(False):
            LOG_ERR("leaseItemCommit leaseCenter is not active")
            return

        request = LeaseItemCommitReq()
        request.uniqueId = uniqueId
        request.playerGBID = playerGBID
        request.opUUID = opUUID

        self.leaseService.serviceStub.leaseItemCommit(None, request, None)

    def leaseItemRollback(self, uniqueId, opUUID=0):
        if not self.isLeaseCenterActive(False):
            LOG_ERR("leaseItemRollback leaseCenter is not active")
            return

        request = LeaseItemRollbackReq()
        request.uniqueId = uniqueId
        request.opUUID = opUUID

        self.leaseService.serviceStub.leaseItemRollback(None, request, None)

    def cancelItem(self, playerGBID, uniqueId):
        LOG_INFO("cancelItem", playerGBID, uniqueId)
        if not self.isLeaseCenterActive():
            LOG_ERR("cancelItem leaseCenter is not active")
            return

        request = LeaseCancelItemReq()
        request.playerGBID = playerGBID
        request.uniqueId = uniqueId

        self.leaseService.serviceStub.cancelItem(None, request, None)

    def getShopSummary(self, categoryId, itemIdList, playerGBID):
        if not self.isLeaseCenterActive():
            LOG_ERR("getShopSummary leaseCenter is not active")
            return

        request = LeaseShopSummaryReq()
        request.categoryId = categoryId
        for itemId in itemIdList:
            request.itemIds.append(itemId)
        request.playerGBID = playerGBID

        self.leaseService.serviceStub.getShopSummary(None, request, None)

    def getShopItems(self, itemId, page, pageSize, playerGBID):
        if not self.isLeaseCenterActive():
            LOG_ERR("getShopItems leaseCenter is not active")
            return

        request = LeaseShopItemsReq()
        request.itemId = itemId
        request.page = page
        request.pageSize = pageSize
        request.playerGBID = playerGBID

        self.leaseService.serviceStub.getShopItems(None, request, None)

    def getMySaleList(self, playerGBID):
        if not self.isLeaseCenterActive():
            LOG_ERR("getMySaleList leaseCenter is not active")
            return

        request = LeaseMySaleListReq()
        request.playerGBID = playerGBID

        self.leaseService.serviceStub.getMySaleList(None, request, None)

    def onReplyAddItemPrepareOffline(self, failGbIds, playerGBID, uniqueId, result, opUUID):
        LOG_WARN("onReplyAddItemPrepareOffline", failGbIds, playerGBID, uniqueId, result, opUUID)
        self.addItemRollback(uniqueId, opUUID)

    def onReplyLeaseItemPrepareOffline(self, failGbIds, playerGBID, uniqueId, totalPrice, result, opUUID):
        LOG_WARN("onReplyLeaseItemPrepareOffline", failGbIds, playerGBID, uniqueId, totalPrice, result, opUUID)
        self.leaseItemRollback(uniqueId, opUUID)


class LeaseStubService(GameServer):
    def __init__(self, leaseStub, address):
        self.address = address
        self.leaseStub = leaseStub
        self.channel = RpcChannel.RpcChannel(self)
        self.serviceStub = LeaseServer_Stub(self.channel)
        address = address.split(':')
        self.channel.connect((address[0], int(address[1])))

    def on_connected(self):
        LOG_INFO("connect to lease service: ", self.address)
        self._reportServerId()

    def on_disconnected(self):
        LOG_INFO("disconnected from lease service:", self.address)

    def _reportServerId(self):
        request = ServerInfoMessage()
        request.serverId = gameconfig.serverId()
        request.compId = KBEngine.getComponentGroupOrder()
        request.serverName = gameglobal.curServerName

        self.serviceStub.registerServer(None, request, None)

    def activeTickCallback(self, rpc_controller, request, done):
        pass

    # ---------- 辅助方法 ----------

    def _transLeaseShopSummary(self, item):
        if not item:
            return None
        return {
            'itemId': item.itemId,
            'onSaleCount': item.onSaleCount,
            'minPrice': item.minPrice,
        }

    def _transLeaseShopItem(self, item):
        if not item:
            return None
        return {
            'uniqueId': item.uniqueId,
            'itemId': item.itemId,
            'lessorGbId': item.lessorGbId,
            'lessorServerId': item.lessorServerId,
            'pricePerDay': item.pricePerDay,
            'leaseDay': item.leaseDay,
            'returnEndTime': item.returnEndTime,
            'itemData': item.itemData,
        }

    def _transLeaseMySaleItem(self, item):
        if not item:
            return None
        return {
            'uniqueId': item.uniqueId,
            'itemId': item.itemId,
            'pricePerDay': item.pricePerDay,
            'leaseDay': item.leaseDay,
            'returnEndTime': item.returnEndTime,
            'itemData': item.itemData,
            'status': item.status,
            'saleEndTime': item.saleEndTime,
        }

    # ---------- 接收 LeaseServer 回调 ----------

    def replyAddItemPrepare(self, rpc_controller, request, done):
        playerGBID = request.playerGBID
        uniqueId = request.uniqueId
        result = request.result
        opUUID = request.opUUID
        LOG_INFO("replyAddItemPrepare", playerGBID, uniqueId, result, opUUID)

        if playerGBID == 0:
            LOG_ERR("replyAddItemPrepare no gbid:", opUUID)
            return

        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [playerGBID], "onReplyAddItemPrepare",
            (uniqueId, result, opUUID),
            self.leaseStub, 'onReplyAddItemPrepareOffline',
            (playerGBID, uniqueId, result, opUUID)
        )

    def replyAddItemCommit(self, rpc_controller, request, done):
        playerGBID = request.playerGBID
        uniqueId = request.uniqueId
        result = request.result
        opUUID = request.opUUID
        LOG_INFO("replyAddItemCommit", playerGBID, uniqueId, result, opUUID)

        if playerGBID == 0:
            LOG_ERR("replyAddItemCommit no gbid:", opUUID)
            return

        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [playerGBID], "onReplyAddItemCommit",
            (uniqueId, result, opUUID),
            None, '', ()
        )

    def replyLeaseItemPrepare(self, rpc_controller, request, done):
        playerGBID = request.playerGBID
        uniqueId = request.uniqueId
        result = request.result
        totalPrice = request.totalPrice
        opUUID = request.opUUID
        LOG_INFO("replyLeaseItemPrepare", playerGBID, uniqueId, result, totalPrice, opUUID)

        if playerGBID == 0:
            LOG_ERR("replyLeaseItemPrepare no gbid:", opUUID)
            return

        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [playerGBID], "onReplyLeaseItemPrepare",
            (uniqueId, totalPrice, result, opUUID),
            self.leaseStub, 'onReplyLeaseItemPrepareOffline',
            (playerGBID, uniqueId, totalPrice, result, opUUID)
        )

    def replyLeaseItemCommit(self, rpc_controller, request, done):
        playerGBID = request.playerGBID
        uniqueId = request.uniqueId
        result = request.result
        opUUID = request.opUUID
        leaseStartTime = request.leaseStartTime
        leaseEndTime = request.leaseEndTime
        lessorGBID = request.lessorGBID
        ownerGBID = request.ownerGBID
        leaseGold = request.leaseGold
        leaseBindGold = request.leaseBindGold
        leaseCost = request.leaseCost
        itemData = request.itemData
        LOG_INFO("replyLeaseItemCommit", opUUID, result, playerGBID, lessorGBID, uniqueId, ownerGBID)

        if playerGBID == 0:
            LOG_ERR("replyLeaseItemCommit no gbid:", opUUID)
            return

        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [playerGBID], "onReplyLeaseItemCommit",
            (opUUID, uniqueId, result, leaseStartTime, leaseEndTime, lessorGBID, ownerGBID, leaseGold, leaseBindGold, leaseCost, itemData),
            None, '', ()
        )

    def replyCancelItem(self, rpc_controller, request, done):
        playerGBID = request.playerGBID
        uniqueId = request.uniqueId
        itemData = request.itemData
        result = request.result
        LOG_INFO("replyCancelItem", playerGBID, uniqueId, result)

        if playerGBID == 0:
            LOG_ERR("replyCancelItem no gbid:", uniqueId)
            return

        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [playerGBID], "onReplyCancelItemInLease",
            (uniqueId, result, itemData),
            None, '', ()
        )

    def replyShopSummary(self, rpc_controller, request, done):
        playerGBID = request.playerGBID
        categoryId = request.categoryId
        items = []
        for item in request.items:
            items.append(self._transLeaseShopSummary(item))
        LOG_DBG("replyShopSummary", playerGBID, categoryId, len(items))

        if playerGBID == 0:
            LOG_ERR("replyShopSummary no gbid:")
            return

        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [playerGBID], "onLeaseShopSummaryResp",
            (categoryId, items),
            None, '', ()
        )

    def replyShopItems(self, rpc_controller, request, done):
        playerGBID = request.playerGBID
        itemId = request.itemId
        page = request.page
        pageSize = request.pageSize
        items = []
        for item in request.items:
            items.append(self._transLeaseShopItem(item))
        LOG_DBG("replyShopItems", playerGBID, itemId, page, pageSize, len(items))

        if playerGBID == 0:
            LOG_ERR("replyShopItems no gbid:")
            return

        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [playerGBID], "onLeaseShopItemsResp",
            (itemId, page, pageSize, items),
            None, '', ()
        )

    def replyMySaleList(self, rpc_controller, request, done):
        playerGBID = request.playerGBID
        items = []
        for item in request.items:
            items.append(self._transLeaseMySaleItem(item))
        LOG_DBG("replyMySaleList", playerGBID, len(items))

        if playerGBID == 0:
            LOG_ERR("replyMySaleList no gbid:")
            return

        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [playerGBID], "onMyLeaseSaleInfo",
            (items, ),
            None, '', ()
        )

    def giveItemToPlayer(self, rpc_controller, request, done):
        ownerServer = request.returnOwnerServerId
        playerGBID = request.playerGBID
        uniqueId = request.uniqueId
        itemData = request.itemData
        opUUID = request.opUUID
        ownerGBID = request.returnOwnerGbId
        returnTime = request.returnEndTime
        LOG_INFO("giveItemToPlayer", opUUID, playerGBID, uniqueId, ownerServer, ownerGBID, returnTime)

        if playerGBID == 0:
            LOG_ERR("giveItemToPlayer no gbid:", opUUID)
            return

        callbackArgs = (opUUID, uniqueId, itemData, ownerServer, ownerGBID, returnTime)
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [playerGBID], "onGiveLeaseItem",
            callbackArgs,
            gameengine.getGlobalBase('PlayerStub'), 'recordOfflineCallback',
            (playerGBID, 'onGiveLeaseItem', callbackArgs)
        )
            
    def addIncomeToOwner(self, rpc_controller, request, done):
        uniqueId = request.uniqueId
        playerGBID = request.playerGBID
        bindGold = request.bindGold
        gold = request.gold
        itemId = request.itemId
        opUUID = request.opUUID
        returnTime = request.returnEndTime
        itemData = request.itemData
        LOG_INFO("addIncomeToOwner", opUUID, uniqueId, playerGBID, bindGold, gold, itemId, returnTime, itemData)

        if playerGBID == 0:
            LOG_ERR("addIncomeToOwner no gbid:", opUUID)
            return

        callbackArgs = (uniqueId, itemId, bindGold, gold, opUUID, returnTime, itemData)
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [playerGBID], "onAddLeaseIncome",
            callbackArgs,
            gameengine.getGlobalBase('PlayerStub'), 'recordOfflineCallback',
            (playerGBID, 'onAddLeaseIncome', callbackArgs)
        )
