# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
import gameconfig
import utils
import gameconst
import gameglobal
import json

from rpc import RpcChannel, TcpServer
from proto.interface_pb2 import Interface, BaseApp_Stub, Void, SetAccountCompResult


def clearAccountCompIdCache(accountName):
    _cache = gameglobal.accountCompIdCache.get(accountName)
    if not _cache:
        return

    if _cache[0] < utils.getNow():
        gameglobal.accountCompIdCache.pop(accountName)


class Baseapp2InterfaceRpcService(Interface):
    def __init__(self, connMgr, tcpConn):
        self.tcpConn = tcpConn
        self.baseappStub = BaseApp_Stub(tcpConn.rpc_channel)
        self.tLastTick = utils.getNow()

    def on_connected(self):
        pass

    def on_disconnected(self):
        pass

    def gameConfigChangedOnBaseapp(self, rpc_controller, request, done):
        INFO_MSG('gameConfigChangedOnBaseapp: ', request.name, request.val)
        gameconfig.gmSetCutomConfig(request.name, request.val, False)

    def cacheConfigOnBaseapp(self, rpc_controller, request, done):
        INFO_MSG('cacheConfigOnBaseapp: ', request.name, request.val)
        gameconfig.setCacheConfig(request.name, request.val)

    def syncCacheConfigOnBaseapp(self, rpc_controller, request, done):
        INFO_MSG('syncCacheConfigOnBaseapp', request.name, request.val)
        names, values = gameconfig.unpackInterfaceDiffCache(request.name, request.val)
        for i in range(0, min(len(names), len(values))):
            gameconfig.setCacheConfig(names[i], values[i])

    def interfaceReload(self, rpc_controller, request, done):
        import importlib
        import hotReload
        importlib.reload(hotReload)
        hotReload.refreshInterface()

    def interfaceDataReload(self, rpc_controller, request, done):
        import gamerefresh
        args = list(request.vals)
        gamerefresh.refreshData(args)

    def syncRegisterCount(self, rpc_controller, request, done):
        INFO_MSG('sync register count from base:', request.value)
        gameglobal.registerCount = int(request.value)

    def activeTick(self, rpc_controller, request, done):
        self.tLastTick = utils.getNow()
        self.baseappStub.activeTickCallback(None, Void(), None)

    def setAccountComp(self, rpc_controller, request, done):
        INFO_MSG('setAccountComp:', request)
        _expire = utils.getNow() + gameconst.AUTH_AVATAR_LOGIN_EXPIRE_TIME
        gameglobal.accountCompIdCache[request.accountName] = (_expire, request.compID)

        # +5 是为了留点容错时间
        _delay = gameconst.AUTH_AVATAR_LOGIN_EXPIRE_TIME + 5
        KBEngine.addTimer(_delay, 0, lambda *args: clearAccountCompIdCache(request.accountName))

        _resp = SetAccountCompResult()
        _resp.result = 1
        _resp.entityID = request.entityID
        self.baseappStub.setAccountCompResult(None, _resp, None)

    def updateAntiAddictionData(self, rpc_controller, request, done):
        timeType = request.timeType
        timestamp = request.timestamp
        INFO_MSG('updateAntiAddictionData:', timeType, timestamp)
        gameglobal.antiAddictionData = [timeType, timestamp]

    def setMapleServerInfo(self, rpc_controller, request, done):
        gameglobal.mapleServerInfo = json.loads(request.data)
        INFO_MSG('setMapleServerInfo:', gameglobal.mapleServerInfo)

class BaseappClientMgr(object):
    def __init__(self):
        self.clients = {}
        self.syncFlag = False

    def handleNewConnection(self, tcpConn):
        INFO_MSG('handleNewConnection', tcpConn.peername)
        interfaceService = Baseapp2InterfaceRpcService(self, tcpConn)
        tcpConn.set_channel_interface_obj(interfaceService)
        self.clients[tcpConn.peername] = interfaceService

        if not self.syncFlag:
            self.syncFlag = True
            interfaceService.baseappStub.reqSyncCacheConfigOnBaseapp(None, Void(), None)

    def checkClicentsActive(self):
        invalidClients = []
        for name, service in self.clients.items():
            if utils.getNow() - service.tLastTick > 60:
                invalidClients.append(name)

        for name in invalidClients:
            INFO_MSG('checkClicentsActive: remove baseapp client', name)
            self.clients.pop(name)


tcpServer = None


def startRpcServer():
    global tcpServer
    connMgr = BaseappClientMgr()
    hostList = gameconfig.interfaceRpcHostList()
    for host in hostList:
        addr, port = host['addr'], int(host['port'])
        INFO_MSG('start rpc server on:', addr, port)
        try:
            tcpServer = TcpServer.TcpServer(addr, port, None, connMgr)
            KBEngine.addTimer(1, 60, lambda timerId: connMgr.checkClicentsActive())
            break
        except Exception as e:
            INFO_MSG('start rpc server on: %s, %s, fail: %s' % (addr, port, e))
