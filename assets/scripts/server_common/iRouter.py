# -*- encoding:utf-8 -*-
from KBEDebug import *
import KBEngine
from rpc import RpcChannel, TcpClient
from proto.gameServerRouter_pb2 import GameServer, GameServer_Stub, RouterServer_Stub, RouterServer, BaseAppInfo, Void, OthersBaseRequest
import os
import gameconfig
import gameglobal
import random
import pickle
import gameengine
import gameconst
import traceback

class RouterService(GameServer):
    def __init__(self, loginMgr, address, routerServerId):
        self.loginMgr = loginMgr
        self.routerServerId = routerServerId
        self.channel = RpcChannel.RpcChannel(self)
        self.routerServerStub = RouterServer_Stub(self.channel)

        self.channel.connect(address)

    def on_connected(self):
        self.loginMgr.onRouterServerConnected(self.routerServerId)

    def on_disconnected(self):
        self.loginMgr.onRouterServerDisonnected()

    def onRemoteCallFromOthersBase(self, rpc_controller, reply, done):
        LOG_DBG("onRemoteCallFromOthersBase", done)
        serverId = reply.serverId
        dstServerId = reply.dstServerId
        componentId = reply.componentId
        memoryStream = reply.memoryStream
        self.loginMgr.onRemoteCallFromOthersBase(serverId, dstServerId, componentId, memoryStream)

    def activeTickCallback(self, rpc_controller, reply, done):
        pass


class RouterServerInfo(object):
    def __init__(self, serverId, ip, port):
        self.serverId = serverId
        self.ip = ip
        self.port = port


class RemoteEntityCallMethod(object):
    def __init__(self, remoteServerEntityCall, funcName):
        self.remoteServerEntityCall = remoteServerEntityCall
        self.funcName = funcName

    def __call__(self, *args):
        if KBEngine.component == 'cellapp':
            order = KBEngine.getComponentGroupOrder()
            baseapps = gameengine.getAllBaseApps()
            baseapp = baseapps[order%len(baseapps)]
            baseapp.doOnOthersBase(self.remoteServerEntityCall, self.funcName, args)
        else:
            gameglobal.localBaseApp.doOnOthersBase(self.remoteServerEntityCall, self.funcName, args)


class RemoteServerEntityCall(object):
    def __init__(self, dstServerId, stubNameOrBox):
        self.serverId = gameconfig.serverId()
        self.dstServerId = dstServerId
        self.stubNameOrBox = stubNameOrBox

    def __getattr__(self, funcName):
        return RemoteEntityCallMethod(self, funcName)

    def __getstate__(self):
        return [self.serverId, self.dstServerId, self.stubNameOrBox]

    def __setstate__(self, state):
        self.serverId, self.dstServerId, self.stubNameOrBox = state[:3]

# e.g.
# r = RemoteServerStubEntityCall(20202, "PlayerStub")
# r.gmAddFriendsGetGbIds(None, 1, 2)
class RemoteServerStubEntityCall(RemoteServerEntityCall):
    def __init__(self, dstServerId, stubName):
        super(RemoteServerStubEntityCall, self).__init__(dstServerId, stubName)
        self.entityCallType = gameconst.RemoteServerEntityCallType.STUB_NAME

    def __getstate__(self):
        attrList = super().__getstate__()
        attrList.append(self.entityCallType)
        return attrList

    def __setstate__(self, state):
        super().__setstate__(state)
        self.entityCallType = state[3]

# e.g.
# box = avatar.base
# r = RemoteServerBoxEntityCall(20202, box)
# r.doBuyCredit(123)
class RemoteServerBoxEntityCall(RemoteServerEntityCall):
    def __init__(self, dstServerId, box, compoentType=gameconst.CrossServerCBComponent.ENUM_BASE, initOtherEntityCall=True):
        super(RemoteServerBoxEntityCall, self).__init__(dstServerId, box)
        self.entityCallType = gameconst.RemoteServerEntityCallType.BOX
        self.compoentType = compoentType
        self.client = self.cell = True
        if initOtherEntityCall:
            if box.client:
                self.client = self.__class__(
                    dstServerId, box, compoentType=gameconst.CrossServerCBComponent.ENUM_CLIENT, initOtherEntityCall=False)
            if box.cell:
                self.cell = self.__class__(
                    dstServerId, box, compoentType=gameconst.CrossServerCBComponent.ENUM_CELL, initOtherEntityCall=False)

    @property
    def id(self):
        return self.stubNameOrBox.id

    @id.setter
    def id(self, value):
        pass

    def __getstate__(self):
        attrList = super().__getstate__()
        attrList.append(self.entityCallType)
        attrList.append(self.compoentType)
        attrList.append(self.client)
        attrList.append(self.cell)
        return attrList

    def __setstate__(self, state):
        super().__setstate__(state)
        self.entityCallType = state[-4]
        self.compoentType = state[-3]
        self.client = state[-2]
        self.cell = state[-1]


class IRouter(object):
    def __init__(self):
        LOG_INFO("IRouter init")
        super().__init__()
        self.componentId = int(os.getenv('KBE_COMPONENTID'))
        self.routerServerDic = {}
        self.routerClientDic = {}
        self.initRouterServers()

    def initRouterServers(self):
        if gameconfig.isReady() and not gameconfig.enableRouterServer():
            return

        serverId = gameconfig.serverId()
        if not serverId:
            return

        routerServersInfo = gameconfig.routerServersInfo()
        for serverInfo in routerServersInfo:
            routerServerId = int(serverInfo.get("routerServerId"))
            ip = serverInfo.get("ip")
            port = int(serverInfo.get("port"))
            self.routerServerDic[routerServerId] = RouterServerInfo(routerServerId, ip, port)
            self.connectRouterServer(routerServerId)

    def connectAllRouterServer(self):
        for routerServerId, _ in self.routerServerDic.items():
            self.connectRouterServer(routerServerId)

    def connectRouterServer(self, routerServerId):
        if gameconfig.isReady() and not gameconfig.enableRouterServer():
            return

        if routerServerId not in self.routerServerDic:
            LOG_ERR("connectRouterServer routerServerId not in routerServerDic", routerServerId,
                      self.routerServerDic)
            return

        routerClient = self.routerClientDic.get(routerServerId, None)
        if routerClient and routerClient.channel.dispatcher:
            return

        serverId = gameconfig.serverId()
        if not serverId:
            return

        rsInfo = self.routerServerDic.get(routerServerId)
        LOG_DBG('IRouter connecting router server:', rsInfo.ip, rsInfo.port, rsInfo.serverId)
        self.routerClientDic[routerServerId] = RouterService(self, (rsInfo.ip, rsInfo.port), rsInfo.serverId)


    def onRouterServerConnected(self, routerServerId):
        pass

    def onRouterServerDisonnected(self):
        pass

    def registerBaseApp(self, routerServerId):
        serverId = gameconfig.serverId()
        if not serverId:
            return

        baseappInfo = BaseAppInfo()
        baseappInfo.serverId = serverId
        baseappInfo.componentId = self.componentId

        routerClient = self.routerClientDic.get(routerServerId)
        routerClient.routerServerStub.registerBaseapp(None, baseappInfo, None)

    def doOnOthersBase(self, remoteServerEntityCall:RemoteServerEntityCall, funcName, args):
        serverId = gameconfig.serverId()
        if not serverId:
            return

        if len(self.routerClientDic) <=0:
            LOG_ERR("doOnOthersBase has no routerClientDic")
            return

        otherBaseRequest = OthersBaseRequest()
        otherBaseRequest.serverId = serverId
        otherBaseRequest.dstServerId = remoteServerEntityCall.dstServerId
        otherBaseRequest.componentId = self.componentId
        stubNameOrBox = None
        otherBaseRequest.memoryStream = pickle.dumps((remoteServerEntityCall.entityCallType,
                                                      remoteServerEntityCall.stubNameOrBox,
                                                      remoteServerEntityCall.compoentType,
                                                      funcName, args))

        order = KBEngine.getComponentGroupOrder()
        routerIds = sorted(self.routerClientDic.keys())
        routerServerId = routerIds[order%len(routerIds)]
        routerClient = self.routerClientDic.get(routerServerId)
        routerClient.routerServerStub.doOnOthersBase(None, otherBaseRequest, None)

    def checkRouterServerActive(self, routerServerId):
        if gameconfig.enableRouterServer():
            routerClient = self.routerClientDic.get(routerServerId)
            routerClient.routerServerStub.activeTick(None, Void(), None)

    def checkAllRouterServerActive(self):
        if gameconfig.enableRouterServer():
            for routerServerId, _ in self.routerServerDic.items():
                self.checkRouterServerActive(routerServerId)

    def onRemoteCallFromOthersBase(self, serverId, dstServerId, componentId, memoryStream):
        curServerId = gameconfig.serverId()
        if not curServerId:
            return

        if curServerId != dstServerId:
            LOG_ERR("onRemoteCallFromOthersBase serverId error",  curServerId, dstServerId)
            return

        entityCallType, stubNameOrBox, compoentType, funcName, args = pickle.loads(memoryStream)
        LOG_INFO("onRemoteCallFromOthersBase", entityCallType, stubNameOrBox, compoentType, funcName, args)
        try:
            if entityCallType == gameconst.RemoteServerEntityCallType.STUB_NAME:
                func = getattr(gameengine.getGlobalBase(stubNameOrBox), funcName)
                func(*args)
            elif entityCallType == gameconst.RemoteServerEntityCallType.BOX:
                if compoentType == gameconst.CrossServerCBComponent.ENUM_BASE:
                    func = getattr(stubNameOrBox, funcName)
                elif compoentType == gameconst.CrossServerCBComponent.ENUM_CELL:
                    func = getattr(stubNameOrBox.cell, funcName)
                elif compoentType == gameconst.CrossServerCBComponent.ENUM_CLIENT:
                    func = getattr(stubNameOrBox.client, funcName)
                else:
                    raise RuntimeError("onRemoteCallFromOthersBase:: compoentType err, {}".format(compoentType))
                func(*args)
        except Exception as e:
            LOG_ERR('onRemoteCallFromOthersBase failed:', e, entityCallType, stubNameOrBox, funcName, args, traceback.format_exc())
