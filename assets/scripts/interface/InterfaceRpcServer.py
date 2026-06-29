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

    if _cache[0] < utils.curTS():
        gameglobal.accountCompIdCache.pop(accountName)


class Baseapp2InterfaceRpcService(Interface):
    def __init__(self, _, tcpConn):
        self.tcpConn = tcpConn
        self.baseappStub = BaseApp_Stub(tcpConn.rpc_channel)
        self.tLastTick = utils.curTS()

    def on_connected(self):
        pass

    def on_disconnected(self):
        pass

    def gameConfigChangedOnBaseapp(self, _, request, done):
        LOG_INFO('gameConfigChangedOnBaseapp: ', request.val, request.name)
        gameconfig.gmSetCutomConfig(request.name, request.val, False)

    def cacheConfigOnBaseapp(self, _, request, done):
        LOG_INFO('cacheConfigOnBaseapp: ', request.name, request.val)
        gameconfig.setCacheConfig(request.name, request.val)

    def syncCacheConfigOnBaseapp(self, _, request, done):
        LOG_INFO('syncCacheConfigOnBaseapp', request.name, request.val)
        _names, values = gameconfig.unpackInterfaceDiffCache(request.name, request.val)
        for i in range(0, min(len(_names), len(values))):
            gameconfig.setCacheConfig(_names[i], values[i])

    def interfaceReload(self, rpc_controller, request, done):
        import hotReload
        import importlib
        importlib.reload(hotReload)
        hotReload.refreshInterface()

    def syncRegisterCount(self, rpc_controller, request, done):
        LOG_INFO('sync register count from base:', request.value)
        gameglobal.registerCount = int(request.value)

    def interfaceDataReload(self, _, request, done):
        import gamerefresh
        _args = list(request.vals)
        gamerefresh.refreshData(_args)

    def activeTick(self, rpc_controller, request, done):
        self.tLastTick = utils.curTS()
        self.baseappStub.activeTickCallback(None, Void(), None)

    def setAccountComp(self, rpc_controller, request, done):
        LOG_INFO('setAccountComp:', request)
        _expire = utils.curTS() + gameconst.AUTH_AVATAR_LOGIN_EXPIRE_TIME
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
        LOG_INFO('updateAntiAddictionData:', timeType, timestamp)
        gameglobal.antiAddictionData = [timeType, timestamp]

    def setMapleServerInfo(self, rpc_controller, request, done):
        gameglobal.mapleServerInfo = json.loads(request.data)
        LOG_INFO('setMapleServerInfo:', gameglobal.mapleServerInfo)

    def updatePatchVersionData(self, rpc_controller, request, done):
        platId = request.platId
        patchVerStr = request.patchVerStr
        LOG_INFO('updatePatchVersionData:', platId, patchVerStr)
        gameglobal.requiredClientVersion[platId] = patchVerStr

class BaseappClientMgr(object):
    def __init__(self):
        self.syncFlag = False
        self.clients = {}

    def handleNewConnection(self, tcpConn):
        LOG_INFO('handleNewConnection', tcpConn.peername)
        _interfaceService = Baseapp2InterfaceRpcService(self, tcpConn)
        tcpConn.set_channel_interface_obj(_interfaceService)
        self.clients[tcpConn.peername] = _interfaceService

        if not self.syncFlag:
            self.syncFlag = True
            _interfaceService.baseappStub.reqSyncCacheConfigOnBaseapp(None, Void(), None)

    def checkClicentsActive(self):
        invalidClients = []
        for name, _service in self.clients.items():
            if utils.curTS() - _service.tLastTick > 60:
                invalidClients.append(name)

        for _name in invalidClients:
            LOG_INFO('checkClicentsActive: remove baseapp client', _name)
            self.clients.pop(_name)


tcpServer = None


def startRpcServer():
    global tcpServer
    _connMgr = BaseappClientMgr()
    hostList = gameconfig.interfaceRpcHostList()
    for _host in hostList:
        addr, port = _host['addr'], int(_host['port'])
        LOG_INFO('start rpc server on:', addr, port)
        try:
            tcpServer = TcpServer.TcpServer(addr, port, None, _connMgr)
            KBEngine.addTimer(1, 60, lambda timerId: _connMgr.checkClicentsActive())
            break
        except Exception as e:
            LOG_INFO('start rpc server on: %s, %s, fail: %s' % (addr, port, e))

