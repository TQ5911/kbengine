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
import json
import LogTrackingMgr

class OrderStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer):
    def __init__(self):
        iGlobal.IGlobal.__init__(self)
        iBaseNoCell.IBaseNoCell.__init__(self)
        iTimer.ITimer.__init__(self)

        self.orderService = None

    def doNext(self):
        self._fullPrepare()

    def _fullPrepare(self):
        self.pyAddTimer(1, 1, gametimer.ORDER_STUB_ASYNC_TICK)
        gameglobal.localBaseApp.initAysncore()
        self.pyAddTimer(gameconst.CENTRAL_SERVER_HEARTBEAT_INTERVAL, gameconst.CENTRAL_SERVER_HEARTBEAT_INTERVAL, gametimer.ORDER_STUB_ACTIVE_TICK)

    def onTimer(self, tid, userArg):
        self._onTimer(tid, userArg)
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
        gbId = request.gbId
        itemId = request.itemId
        itemCount = request.itemCount
        LOG_INFO("notifyOrder:", serverId, outTradeNo, gbId, itemId, itemCount)

        resp = OrderResponse()
        resp.outTradeNo = outTradeNo
        resp.result = OrderService.SUCCESS

        self.serviceStub.finishOrder(None, resp, None)
