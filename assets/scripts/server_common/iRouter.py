# -*- encoding:utf-8 -*-
from KBEDebug import *
import KBEngine
from rpc import RpcChannel
from proto.gameServerRouter_pb2 import GameServer, RouterServer_Stub,\
    BaseAppInfo, Void, OthersBaseRequest
import os
import gameconfig
import gameglobal
import pickle
import gameengine
import gameconst
import traceback

class RouterService(GameServer):
    def __init__(self, loginMgr, address, routerServerId):
        self.routerServerId = routerServerId
        self.loginMgr = loginMgr
        self.channel = RpcChannel.RpcChannel(self)
        self.routerServerStub = RouterServer_Stub(self.channel)

        self.channel.connect(address)

    def on_disconnected(self):
        self.loginMgr.onRouterServerDisonnected()

    def on_connected(self):
        self.loginMgr.onRouterServerConnected(self.routerServerId)

    def onRemoteCallFromOthersBase(self, rpc_controller, reply, done):
        LOG_DBG("onRemoteCallFromOthersBase", done)
        self.loginMgr.onRemoteCallFromOthersBase(
            reply.serverId, 
            reply.dstServerId, 
            reply.componentId, 
            reply.memoryStream)

    def activeTickCallback(self, rpc_controller, reply, done):
        return


class RouterServerInfo(object):
    def __init__(self, serverId, ip, port):
        self.serverId = serverId
        self.port = port
        self.ip = ip


class RemoteEntityCallMethod(object):
    def __init__(self, remoteServerEntityCall, funcName):
        self.funcName = funcName
        self.remoteServerEntityCall = remoteServerEntityCall

    def __call__(self, *arguments):
        if KBEngine.component == 'cellapp':
            order = KBEngine.getComponentGroupOrder()
            _baseapps = gameengine.getAllBaseApps()
            _baseapp = _baseapps[order%len(_baseapps)]
            _baseapp.doOnOthersBase(self.remoteServerEntityCall, self.funcName, arguments)
        else:
            gameglobal.localBaseApp.doOnOthersBase(
                self.remoteServerEntityCall, 
                self.funcName, 
                arguments)


class RemoteServerEntityCall(object):
    def __init__(self, dstServerId, stubNameOrBox):
        self.dstServerId = dstServerId
        self.serverId = gameconfig.serverId()
        self.stubNameOrBox = stubNameOrBox

    def __getattr__(self, funcName):
        return RemoteEntityCallMethod(self, funcName)

    def __setstate__(self, state):
        self.serverId, self.dstServerId, self.stubNameOrBox = state[:3]

    def __getstate__(self):
        return [self.serverId, self.dstServerId, self.stubNameOrBox]

# e.g.
# r = RemoteServerStubEntityCall(20202, "PlayerStub")
# r.gmAddFriendsGetGbIds(None, 1, 2)
class RemoteServerStubEntityCall(RemoteServerEntityCall):
    def __init__(self, dstServerId, stubName, *args):
        super(RemoteServerStubEntityCall, self).__init__(dstServerId, stubName)
        self.entityCallType = gameconst.RemoteSrvEntCallType.STUB_NAME

    def __setstate__(self, state):
        super().__setstate__(state)
        self.entityCallType = state[3]

    def __getstate__(self):
        attrList = super().__getstate__()
        attrList.append(self.entityCallType)
        return attrList

# e.g.
# box = avatar.base
# r = RemoteServerBoxEntityCall(20202, box)
# r.doBuyCredit(123)
class RemoteServerBoxEntityCall(RemoteServerEntityCall):
    def __init__(self, dstServerId, box, compoentType=gameconst.CrossServerCBComponent.ENUM_BASE, initOtherEntityCall=True):
        super(RemoteServerBoxEntityCall, self).__init__(dstServerId, box)
        self.entityCallType = gameconst.RemoteSrvEntCallType.BOX
        self.compoentType = compoentType
        self.client = self.cell = True
        if initOtherEntityCall:
            if box.cell:
                self.cell = self.__class__(
                    dstServerId, 
                    box, 
                    compoentType=gameconst.CrossServerCBComponent.ENUM_CELL, 
                    initOtherEntityCall=False)
            if box.client:
                self.client = self.__class__(
                    dstServerId, 
                    box, 
                    compoentType=gameconst.CrossServerCBComponent.ENUM_CLIENT, 
                    initOtherEntityCall=False)

    @property
    def id(self):
        return self.stubNameOrBox.id

    @id.setter
    def id(self, _):
        return

    def __getstate__(self):
        _attrList = super().__getstate__()
        _attrList.append(self.entityCallType)
        _attrList.append(self.compoentType)
        _attrList.append(self.client)
        _attrList.append(self.cell)
        return _attrList

    def __setstate__(self, state):
        super().__setstate__(state)
        self.cell = state[-1]
        self.client = state[-2]
        self.compoentType = state[-3]
        self.entityCallType = state[-4]


class IRouter(object):
    def __init__(self):
        LOG_INFO("IRouter init")
        super().__init__()
        self.componentId = int(os.getenv('KBE_COMPONENTID'))
        self.routerClientDic = {}
        self.routerServerDic = {}
        self.initRouterServers()

    def connectAllRouterServer(self):
        for routerServerId, _ in self.routerServerDic.items():
            self.connectRouterServer(routerServerId)

    def initRouterServers(self):
        if gameconfig.isReady() and not gameconfig.enableRouterServer():
            return

        if not gameconfig.serverId():
            return

        routerServersInfo = gameconfig.routerServersInfo()
        for _serverInfo in routerServersInfo:
            routerServerId = int(_serverInfo.get("routerServerId"))
            ip = _serverInfo.get("ip")
            port = int(_serverInfo.get("port"))
            self.routerServerDic[routerServerId] = RouterServerInfo(routerServerId, ip, port)
            self.connectRouterServer(routerServerId)

    def connectRouterServer(self, routerServerId):
        if not (gameconfig.isReady() and gameconfig.enableRouterServer()):
            return

        if routerServerId not in self.routerServerDic:
            LOG_ERR("connectRouterServer routerServerId not in routerServerDic", routerServerId,
                      self.routerServerDic)
            return

        _routerClient = self.routerClientDic.get(routerServerId, None)
        if _routerClient and _routerClient.channel.dispatcher:
            return

        serverId = gameconfig.serverId()
        if not serverId:
            return

        _rsInfo = self.routerServerDic.get(routerServerId)
        LOG_DBG('IRouter connecting router server:', _rsInfo.ip, _rsInfo.port, _rsInfo.serverId)
        self.routerClientDic[routerServerId] = RouterService(self, (_rsInfo.ip, _rsInfo.port), _rsInfo.serverId)

    def onRouterServerDisonnected(self):
        pass

    def onRouterServerConnected(self, routerServerId):
        pass

    def registerBaseApp(self, routerServerId):
        _serverId = gameconfig.serverId()
        if not _serverId:
            return

        _baseappInfo = BaseAppInfo()
        _baseappInfo.serverId = _serverId
        _baseappInfo.componentId = self.componentId

        routerClient = self.routerClientDic.get(routerServerId)
        routerClient.routerServerStub.registerBaseapp(None, _baseappInfo, None)

    def doOnOthersBase(self, remoteServerEntityCall:RemoteServerEntityCall, funcName, args):
        _serverId = gameconfig.serverId()
        if not _serverId:
            return

        if len(self.routerClientDic) <=0:
            LOG_ERR("doOnOthersBase has no routerClientDic")
            return

        otherBaseRequest = OthersBaseRequest()
        otherBaseRequest.serverId = _serverId
        otherBaseRequest.dstServerId = remoteServerEntityCall.dstServerId
        otherBaseRequest.componentId = self.componentId
        otherBaseRequest.memoryStream = pickle.dumps((remoteServerEntityCall.entityCallType,
                                                      remoteServerEntityCall.stubNameOrBox,
                                                      remoteServerEntityCall.compoentType,
                                                      funcName, args))

        _order = KBEngine.getComponentGroupOrder()
        routerIds = sorted(self.routerClientDic.keys())
        routerServerId = routerIds[_order%len(routerIds)]
        _routerClient = self.routerClientDic.get(routerServerId)
        _routerClient.routerServerStub.doOnOthersBase(None, otherBaseRequest, None)

    def checkRouterServerActive(self, routerServerId):
        if gameconfig.enableRouterServer():
            _routerClient = self.routerClientDic.get(routerServerId)
            _routerClient.routerServerStub.activeTick(None, Void(), None)

    def checkAllRouterServerActive(self):
        if gameconfig.enableRouterServer():
            for _routerServerId, _ in self.routerServerDic.items():
                self.checkRouterServerActive(_routerServerId)

    def onRemoteCallFromOthersBase(self, serverId, dstServerId, componentId, memoryStream):
        _curServerId = gameconfig.serverId()
        if not _curServerId:
            return

        if _curServerId != dstServerId:
            LOG_ERR("onRemoteCallFromOthersBase serverId error",  _curServerId, dstServerId)
            return

        entityCallType, stubNameOrBox, compoentType, funcName, args = pickle.loads(memoryStream)
        LOG_INFO("onRemoteCallFromOthersBase", entityCallType, stubNameOrBox, compoentType, funcName, args)
        try:
            if entityCallType == gameconst.RemoteSrvEntCallType.STUB_NAME:
                _func = getattr(gameengine.getGlobalBase(stubNameOrBox), funcName)
                _func(*args)
            elif entityCallType == gameconst.RemoteSrvEntCallType.BOX:
                if compoentType == gameconst.CrossServerCBComponent.ENUM_BASE:
                    _func = getattr(stubNameOrBox, funcName)
                elif compoentType == gameconst.CrossServerCBComponent.ENUM_CELL:
                    _func = getattr(stubNameOrBox.cell, funcName)
                elif compoentType == gameconst.CrossServerCBComponent.ENUM_CLIENT:
                    _func = getattr(stubNameOrBox.client, funcName)
                else:
                    raise RuntimeError("onRemoteCallFromOthersBase:: compoentType err, {}".format(compoentType))
                _func(*args)
        except Exception as e:
            LOG_ERR('onRemoteCallFromOthersBase failed:', e, entityCallType, stubNameOrBox, funcName, args, traceback.format_exc())
