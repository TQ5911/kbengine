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

import proto.orderService_pb2 as OrderService
from rpc import RpcChannel, TcpClient
from proto.orderService_pb2 import (
    OrderService_Stub, GameServer, ServerInfoMessage, Void, OrderResponse, ERRCODE)

import gameglobal
import gameconst
import gamesql
import json
import LogTrackingMgr
import itemData_itemData as ITEM_DATA

class OrderStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer):
    def __init__(self, **kwargs):
        iGlobal.IGlobal.__init__(self)
        iBaseNoCell.IBaseNoCell.__init__(self)
        iTimer.ITimer.__init__(self)

        self.orderService = None
        self.ORDER_LOCK_TTL = 30
        self.ORDER_LOCK_PREFIX = 'order:lock:'

    def doNext(self):
        self._fullPrepare()

    def _fullPrepare(self):
        self.pyAddTimer(1, 1, gametimer.ORDER_STUB_ASYNC_TICK)
        gameglobal.localBaseApp.initAysncore()
        self.pyAddTimer(gameconst.CENTRAL_SERVICE_HEARTBEAT_INTERVAL, gameconst.CENTRAL_SERVICE_HEARTBEAT_INTERVAL, gametimer.ORDER_STUB_ACTIVE_TICK)

    def onTimer(self, tid, userArg):
        self._onTimerTrigger(tid, userArg)
        if userArg == gametimer.ORDER_STUB_ASYNC_TICK:
            self._connectOrderService()
        elif userArg == gametimer.ORDER_STUB_ACTIVE_TICK:
            self._checkOrderServiceActive()

    def reloadScript(self):
        super(OrderStub, self).reloadScript()

    def _connectOrderService(self):
        if not gameconfig.enableOrderService():
            return

        host = gameconfig.orderServerHost()
        if not (self.orderService and self.orderService.channel.dispatcher):
            LOG_INFO('connect orderService---------:', host)
            self.orderService = OrderStubService(self, host)

    def _checkOrderServiceActive(self):
        if not gameconfig.enableOrderService():
            return

        if self.orderService and self.orderService.channel.dispatcher:
            self.orderService.serviceStub.activeTick(None, Void(), None)

    def isOrderServiceActive(self, needCheck=True):
        if needCheck and not gameconfig.enableOrderService():
            return False

        return self.orderService and self.orderService.channel.dispatcher

    def _releaseOrderLock(self, outTradeNo):
        gameglobal.localBaseApp.getRedisClient().deleteTable(self.ORDER_LOCK_PREFIX + outTradeNo)

    def _processNotifyOrder(self, outTradeNo, createTime, gbId, itemId, itemCount, itemPrice, addToSafe, roleName, serverId, payTime):
        cfgData = ITEM_DATA.datas.get(itemId)
        if not cfgData:
            LOG_ERR('_processNotifyOrder:: config not found', itemId, outTradeNo)
            self._sendOrderAck(outTradeNo, gameconst.OrderError.ITEM_CFG_MISSING)
            self._releaseOrderLock(outTradeNo)
            return

        playerStub = gameengine.getGlobalBase('PlayerStub')

        playerStub.doOnOthersBase(
                [gbId], "processPurchaseOrder",
                (outTradeNo, payTime, itemId, itemCount, itemPrice, addToSafe),
                playerStub, 'recordOfflineCallback',
                (gbId, 'processPurchaseOrder',
                (outTradeNo, payTime, itemId, itemCount, itemPrice, addToSafe)))
        LogTrackingMgr.LogTrackingMgr.item_issuance(gbId,
			                                        '',
                                                    outTradeNo,
                                                    gbId,
                                                    roleName,
                                                    serverId,
                                                    itemId,
                                                    addToSafe, 
                                                    createTime, 
                                                    payTime)

        self._sendOrderAck(outTradeNo, gameconst.OrderError.SUCCESS)
        self._releaseOrderLock(outTradeNo)

    def _sendOrderAck(self, outTradeNo, result):
        if not (self.orderService and self.orderService.channel.dispatcher):
            LOG_WARN('_sendOrderAck:: order service not connected', outTradeNo)
            return
        resp = OrderResponse()
        resp.outTradeNo = outTradeNo
        resp.result = result
        self.orderService.serviceStub.finishOrder(None, resp, None)

    def _onLockAcquired(self, outTradeNo, createTime, gbId, itemId, itemCount, itemPrice, addToSafe, roleName, serverId, payTime):
        gamesql.checkOrderExists(
            outTradeNo,
            lambda ret, num, insertId, err, otn=outTradeNo, ct=createTime, pid=gbId, iid=itemId, ic=itemCount, ip=itemPrice, ad=addToSafe, rn=roleName, si=serverId, pt=payTime:
                self._onNotifyOrderIdempotency(ret, num, insertId, err, otn, ct, pid, iid, ic, ip, ad, rn, si, pt))

    def _onNotifyOrderIdempotency(self, ret, num, insertId, err, outTradeNo, createTime, gbId, itemId, itemCount, itemPrice, addToSafe, roleName, serverId, payTime):
        if err:
            LOG_ERR('notifyOrder:: idempotency check failed', outTradeNo, err)
            self._sendOrderAck(outTradeNo, gameconst.OrderError.MYSQL_ERROR)
            self._releaseOrderLock(outTradeNo)
            return
        if ret:
            LOG_INFO('notifyOrder:: order already processed', outTradeNo)
            self._sendOrderAck(outTradeNo, gameconst.OrderError.SUCCESS)
            self._releaseOrderLock(outTradeNo)
            return
        # 记录幂等信息
        gamesql.recordOrderId(outTradeNo, lambda ret, num, insertId, err, otn=outTradeNo, ct=createTime, pid=gbId, iid=itemId, ic=itemCount, ip=itemPrice, ad=addToSafe, rn=roleName, si=serverId, pt=payTime:
                self._onRecordOrderId(ret, num, insertId, err, otn, ct, pid, iid, ic, ip, ad, rn, si, pt))

    def _onRecordOrderId(self, ret, num, insertId, err, outTradeNo, createTime, gbId, itemId, itemCount, itemPrice, addToSafe, roleName, serverId, payTime):
        if err:
            LOG_ERR('_onRecordOrderId:: record id add failed', err, outTradeNo)
            self._sendOrderAck(outTradeNo, gameconst.OrderError.MYSQL_ERROR)
            self._releaseOrderLock(outTradeNo)
            return
        self._processNotifyOrder(outTradeNo, createTime, gbId, itemId, itemCount, itemPrice, addToSafe, roleName, serverId, payTime)

class OrderStubService(GameServer):
    # orderStub: callback obj
    # address: tuple of (ip, port)
    def __init__(self, orderStub, address):
        self.address = address
        self.orderStub = orderStub
        self.channel = RpcChannel.RpcChannel(self)
        self.serviceStub = OrderService_Stub(self.channel)
        address = address.split(':')
        self.channel.connect((address[0], int(address[1])))

    def on_connected(self):
        LOG_INFO("connected from order service:", self.address)
        self._reportServerId()

    def on_disconnected(self):
        LOG_INFO("disconnected from order service:", self.address)

    def _reportServerId(self):
        request = ServerInfoMessage()
        request.serverId = gameconfig.serverId()
        request.compId = KBEngine.getComponentGroupOrder()
        request.serverName = gameglobal.curServerName

        self.serviceStub.registerServer(None, request, None)

    def activeTickCallback(self, rpc_controller, request, done):
        pass

    def notifyOrder(self, rpc_controller, request, done):
        serverId = request.serverId
        outTradeNo = request.outTradeNo
        createTime = request.createTime
        gbId = request.gbId
        itemId = request.itemId
        itemCount = request.itemCount
        itemPrice = request.price
        addToSafe = request.addToSafe
        roleName = request.roleName
        payTime = request.payTime
        LOG_INFO("notifyOrder:", serverId, outTradeNo, createTime, gbId, itemId, itemCount, itemPrice, addToSafe, roleName, payTime)

        gameglobal.localBaseApp.getRedisClient().setnxex(
            self.orderStub.ORDER_LOCK_PREFIX + outTradeNo, 1,
            self.orderStub.ORDER_LOCK_TTL,
            lambda cid, err, result, otn=outTradeNo, ct=createTime, pid=gbId, iid=itemId, ic=itemCount, ip=itemPrice, ad=addToSafe, rn=roleName, si=serverId, pt=payTime:
                self._onLockResult(cid, err, result, otn, ct, pid, iid, ic, ip, ad, rn, si, pt))

    def _onLockResult(self, cid, err, result, outTradeNo, createTime, gbId, itemId, itemCount, itemPrice, addToSafe, roleName, serverId, payTime):
        if err:
            LOG_ERR('notifyOrder:: lock error', outTradeNo, err)
            self.orderStub._sendOrderAck(outTradeNo, gameconst.OrderError.REDIS_ERROR)
            return

        if result != 'OK':
            LOG_INFO('notifyOrder:: already in flight', outTradeNo)
            self.orderStub._sendOrderAck(outTradeNo, gameconst.OrderError.IN_PROCESSING)
            return

        self.orderStub._onLockAcquired(outTradeNo, createTime, gbId, itemId, itemCount, itemPrice, addToSafe, roleName, serverId, payTime)
