# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

import math

import gameengine
import gamebase
import gameconfig
import gameconst
import gameRedisAsync
import random
import utils
import formula
import gameglobal
import gametimer
import gmCommand
import gamesql
import iRouter
import json
import ResMgr
import copy
import iTimer
import iBaseNoCell
import asyncore
import iBroadcastEvent
import gzip
import iGameStart
import mailAssistor
import elasticUtils

from proto.interface_pb2 import BaseApp as BaseAppService
from proto.interface_pb2 import Void, Interface_Stub, ConfigVal, ListVal, IntVal

from rpc import RpcChannel


class InterfaceBaseappClient(BaseAppService):
    def __init__(self, baseapp, address):
        self.baseapp = baseapp
        self.channel = RpcChannel.RpcChannel(self)
        self.interfaceStub = Interface_Stub(self.channel)

        self.channel.connect(address)

    def on_connected(self):
        pass

    def on_disconnected(self):
        pass

    def activeTickCallback(self, rpc_controller, request, done):
        pass

    def reqSyncCacheConfigOnBaseapp(self, rpc_controller, request, done):
        nameStr, valueStr = gameconfig.packInterfaceDiffCache()
        if nameStr and valueStr:
            configVal = ConfigVal()
            configVal.name, configVal.val = nameStr, valueStr
            self.interfaceStub.syncCacheConfigOnBaseapp(None, configVal, None)


class BaseApp(iBaseNoCell.IBaseNoCell, iTimer.ITimer, iBroadcastEvent.IBroadcastEvent, iGameStart.IGameStart, iRouter.IRouter):
    INITIAL_INIT = 0.1
    INITIAL_MARKER = 1
    INTERVAL_MARKER = 10

    def __init__(self):
        super(BaseApp, self).__init__()
        self.addDatetimeTimerTick()

        self._loadEntityTypeToDBID()
        self.buildAreaData()
        self.redisAsyncClient = gameRedisAsync.RedisAsyncClient(gameconfig.redisServer(), gameconfig.redisPort(),
                                                                gameconfig.redisPassword())
        self.redisAsyncClient.onConnect()
        self.lockDict = {}
        self.redisAttrs = {}
        self.interfaceClient = {}
        self.gmCmdDic = {}
        self.initAysncore()
        self.accountNum = 0
        self.avatarNum = 0

        # self.ssClient = None
        # self._addLoopTimer()
        self.pyAddTimer(5, 1, gametimer.REDIS_HEART_BEAT)
        self.pyAddTimer(1, 5, gametimer.BASEAPP_CONN_INTERFACE)
        self.pyAddTimer(gameconst.CENTRAL_SERVER_HEARTBEAT_INTERVAL, gameconst.CENTRAL_SERVER_HEARTBEAT_INTERVAL,
                        gametimer.BASEAPP_INTERFACE_ACTIVE)

        self.pyAddTimer(1, 1, gametimer.BASEAPP_ASYNC_TICK)

        self.pyAddTimer(gameconst.CENTRAL_SERVER_HEARTBEAT_INTERVAL, gameconst.CENTRAL_SERVER_HEARTBEAT_INTERVAL, gametimer.BASEAPP_ACTIVE_TICK)

        self._callback(30, '_handleCallQueue', (), gametimer.TIMER_TAG_HANDLE_CALL_QUEUE)

        self.pyAddTimer(self.INITIAL_INIT + random.random(), 0, gametimer.BASEAPP_TIMER_INIT)

        #self.pyAddTimer(1, gameconst.AuctionCollection.CHECK_TIP_INTERVAL, gametimer.CHECK_TIP_PLAYER_AUCTION_COLLECTION)

        if gameconfig.elasticServer() and gameglobal.isBootstrap:
            self._callback(1, 'initElastic', (), gametimer.TIMER_TAG_INIT_ELASTIC)

        _url = gameconfig.mapleAllServerUrl()
        if gameglobal.isBootstrap and _url:
            KBEngine.urlopenv2(_url, self._onGetAllServerResult, method='GET')

        return

    def _onGetAllServerResult(self, httpCode, data, headers, success, *args):
        if not (httpCode == 200 and success):
            ERROR_MSG('_onGetAllServerResult', httpCode)
            return

        _datas = json.loads(data)
        _alias = ''
        for _data in _datas:
            if _data['id'] != gameconfig.serverId():
                continue

            _alias = _data['alias']
            break

        if not _alias:
            INFO_MSG('_onGetAllServerResult: no alias found')
            return

        gameengine.callAllApps(
            'gameengine.setServerAlias',
            (_alias,))

    def initElastic(self):
        elasticUtils.ElasticUtils.init(self._initElasitc)

    def _initElasitc(self, *args):
        INFO_MSG('init elastic', args)

    def setStartGbId(self, cursor, num):
        self.startGbId = cursor * ((1 << gameconst.GLOBAL_TIME_SHIFT) // num)

    def getStartGbId(self):
        return self.startGbId

    def getRedisClient(self):
        return self.redisAsyncClient

    def preReloadScript(self):
        return

    def initAysncore(self):
        if not self.asyncTimer:
            INFO_MSG('initAysncore')
            self.asyncTimer = self.pyAddTimer(1, 0.1, gametimer.ASYNCORE_TICK)

    def onTimer(self, timerID, userData):
        self._onTimer(timerID, userData)

        if userData == gametimer.BASEAPP_TIMER_INIT:
            if self.initProcedures:
                self.pyAddTimer(0.5, 0, gametimer.BASEAPP_TIMER_INIT)
                INFO_MSG('waitting for baseapp init:', list(self.initProcedures.keys()))
                return
            hostName = utils.getPythonServer()
            stubIndex = formula.getStubIndex()
            gameengine.setGlobalData(gameconst.GLOBALDATA_KEY_BASEAPP + ':' + hostName, self)
            gameengine.setGlobalData(gameconst.GLOBALDATA_KEY_BASEAPP_IDX + ':' + str(stubIndex), self)
            self.setTempMiscProp(gameconst.GLOBALDATA_KEY_BASEAPP_IDX, stubIndex)
            # self.pyAddTimer(1, 10, gametimer.BASEAPP_TIMER_CREATE_SPACE_MARKER)
            self.pyAddTimer(1, 0, gametimer.BASESTUB_TIMER_CHECK_COMPONENTS)

        elif utils.isBelongTimerTag(userData):
            self._onTimerCallback(timerID)

        elif userData == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()

        elif userData == gametimer.ASYNCORE_TICK:
            asyncore.loop(0, True, None, 1)

        elif userData == gametimer.REDIS_HEART_BEAT:
            self._onRedisHeartBeat()

        elif userData == gametimer.BASEAPP_INTERFACE_ACTIVE:
            self._checkInterfaceActive()

        elif userData == gametimer.BASEAPP_CONN_INTERFACE:
            self._connectInterfaceApp()

        elif userData == gametimer.BASEAPP_ACTIVE_TICK:
            if gameconfig.enableRouterServer():
                self.checkAllRouterServerActive()

        elif userData == gametimer.BASEAPP_ASYNC_TICK:
            self.connectAllRouterServer()

        elif userData == gametimer.CHECK_TIP_PLAYER_AUCTION_COLLECTION:
            self._checkTipPlayerAuctionCollection()

        else:
            iGameStart.IGameStart.onTimer(self, timerID, userData)

    def onRouterServerConnected(self, routerServerId):
        self.tryRegisterBaseApp(routerServerId)

    def tryRegisterBaseApp(self, routerServerId):
        if not KBEngine.globalData.get(gameconst.GLOBALDATA_KEY_GAME_READY):
            self._callback(5, 'tryRegisterBaseApp', (routerServerId,), gametimer.TIMER_TAG_TRY_REGISTER_BASEAPP)
        else:
            self.registerBaseApp(routerServerId)

    def _onRedisHeartBeat(self):
        if not self.redisAsyncClient.isConnect():
            ERROR_MSG('the redis server is not connected')
            self.redisAsyncClient.disconnectRedis()
            self.redisAsyncClient.onConnect()

    def _checkInterfaceActive(self):
        for client in self.interfaceClient.values():
            if client and client.channel.dispatcher:
                client.interfaceStub.activeTick(None, Void(), None)

    def _connectInterfaceApp(self):
        hostList = gameconfig.interfaceRpcHostList()
        for host in hostList:
            key = ':'.join(host.values())
            client = self.interfaceClient.get(key, None)
            if client and client.channel.dispatcher: continue

            addr, port = host['addr'], int(host['port'])
            INFO_MSG('connect interface', addr, port)
            self.interfaceClient[key] = InterfaceBaseappClient(self, (addr, port))

    def _callInterfaceApp(self, func, *args):
        for client in self.interfaceClient.values():
            if client and client.channel.dispatcher:
                method = getattr(client.interfaceStub, func)
                if method:
                    method(*args)

    def _checkTipPlayerAuctionCollection(self):
        newAuctionCache = gameglobal.newAuctionCache
        if not len(newAuctionCache):
            return

        copyNewAuctionCache = copy.deepcopy(newAuctionCache)
        self.broadcastToAllAvatar(gameconst.BASE, 'tipPlayerAuctionCollection', (copyNewAuctionCache,))
        newAuctionCache.clear()

    # 以归档模式创建base实体，首先查询数据库中是否存在该实体，若存在则调用createBaseLocallyFromDB来创建
    # 否则，使用gamebase.createGlobal的方式直接创建
    def createArchiveStub(self, clsName, properties, globalName):
        self.preparingEntTypes.append(clsName)
        dbid = gameglobal.entityTypeToDBID.get(clsName)
        INFO_MSG('createArchiveStub', clsName, globalName, dbid)
        if not dbid:
            self._onArchiveStubLookup(clsName, 0, False, properties, globalName)
        else:
            KBEngine.lookUpEntityByDBID(
                clsName,
                dbid,
                lambda box,
                       clsName=clsName,
                       dbid=dbid,
                       globalName=globalName: self._onArchiveStubLookup(clsName, dbid, box, properties, globalName)
            )

        return

    def _onArchiveStubLookup(self, clsName, dbid, box, properties, globalName):
        INFO_MSG('_onArchiveStubLookup', clsName, dbid, box, globalName, properties)
        if box == False:
            if dbid:
                # lookUpEntityByDBID的box参数只有两种情况会返回false
                # 1.数据库中tbl_className表中没有dbid对应的实体，但dbid在gameglobal.entityTypeToDBID中，所以应该是哪里出错了，这里停下来报错不让成功启动
                # 2.数据库kbe_entitylog表中entity对应的数据serverGroupID与当前服不匹配（因为kbengine允许多组服共用一个库）
                # 如果从数据库中找到对应dbid数据，box返回true
                # 如果对应dbid的实体已经创建则返回实体的entity_call
                ERROR_MSG('_onArchiveStubLookup: lookup entity failed')
            else:
                gamebase.createArchiveStubGlobal(clsName, properties, globalName)
        elif box == True:
            KBEngine.createEntityFromDBID(
                clsName,
                dbid,
                lambda ent,
                       databaseID,
                       wasActive,
                       clsName=clsName,
                       dbid=dbid,
                       globalName=globalName: self._onArchiveStubLoad(clsName, ent, databaseID, wasActive, globalName)
            )
        else:
            INFO_MSG('[%s %s] has been loaded' % (clsName, dbid,))

        return

    def _onArchiveStubLoad(self, clsName, ent, databaseID, wasActive, globalName):
        if ent:
            INFO_MSG('successful to load [%s %s] from database' % (clsName, databaseID,))
            # TODO:查下registerGlobally
            ent.onGlobalBase(True, globalName)
        else:
            ERROR_MSG('Error:failed to load [%s %s] from database')

        return

    def createUnarchiveStub(self, clsName, props, globalName):
        self.preparingEntTypes.append(clsName)
        gamebase.createGlobal(clsName, props, globalName)
        return

    def destroyMarker(self, spaceNo):
        sm = gamebase.getSpaceMarkerBaseByNo(spaceNo)
        if sm:
            sm.entireDestroy(False, False)

        return

    def _loadEntityTypeToDBID(self):
        self.addInitProcedure(gameconst.BaseAppIniting.LOAD_ENTITY_DBID)
        sql = 'SELECT entityType, entityDBID FROM game_entity_dbid'
        KBEngine.executeRawDatabaseCommand(
            sql,
            lambda ret, num, insertId, err: self._onGetEntityDBIDFromDB(ret, num, insertId, err)
        )

    def _onGetEntityDBIDFromDB(self, result, num, insertId, error):
        if isinstance(error, str):
            ERROR_MSG('==========Error:failed to exec query base==========%s' % error)
            return

        gameglobal.entityTypeToDBID = {}
        self.onInitProcedureDone(gameconst.BaseAppIniting.LOAD_ENTITY_DBID)
        if not result:
            return

        for entityType, dbid in result:
            entityType = utils.getStringFromBytes(entityType)
            try:
                __import__(entityType)
            except:
                gamesql.deleteEntityDBID(entityType)
                continue
            gameglobal.entityTypeToDBID[entityType] = int(dbid)

    def onGmFindEntity(self, result, uid):
        gmCommand.onFindEntity(result, uid)

    def onGmFindAccount(self, result, accountName, index, raw, uid):
        gmCommand.onFindAccount(result, accountName, index, raw, uid)

    def onGmLookUpAvatar(self, base, role, uid, index, raw):
        gmCommand.onLookUpAvatar(base, role, uid, index, raw)

    def onDoCmdSucc(self, uid):
        gmCommand.onBroadcastCmdSucc(uid)

    def onDoCmdFail(self, uid):
        gmCommand.onBroadcastCmdFail(uid)

    def lockKey(self, key):
        timestamp = self.lockDict.get(key, 0)
        now = utils.getNow()
        if now - timestamp < 60:
            return False

        self.lockDict[key] = now
        return True

    def unlockKey(self, key):
        self.lockDict.pop(key, None)

    def pushRedisAttrs(self, gbId, attrs):
        if gbId in self.redisAttrs:
            self.redisAttrs[gbId].update(attrs)
        else:
            self.redisAttrs[gbId] = attrs

    def popRedisAttrs(self, gbId):
        return self.redisAttrs.pop(gbId, {})

    def notifyInterfaceConfigChanged(self, name, val):
        configVal = ConfigVal()
        configVal.name = name
        configVal.val = val

        self._callInterfaceApp('gameConfigChangedOnBaseapp', None, configVal, None)

    def notifyInterfaceCacheConfigChanged(self, name, val):
        configVal = ConfigVal()
        configVal.name = name
        configVal.val = val

        self._callInterfaceApp('cacheConfigOnBaseapp', None, configVal, None)

    def notifyInterfaceReload(self):
        self._callInterfaceApp('interfaceReload', None, Void(), None)

    def notifyInterfaceDataReload(self, args):
        listVal = ListVal()
        for arg in args:
            listVal.vals.append(arg)
        self._callInterfaceApp('interfaceDataReload', None, listVal, None)

    def notifyInterfaceSyncRegisterCount(self, count):
        intVal = IntVal()
        intVal.value = count
        self._callInterfaceApp('syncRegisterCount', None, intVal, None)

    def readhotfix(self):
        INFO_MSG('do hotfix')
        # hotfix = ''
        # with open(gameconst.HOTFIX_PATH, 'r', encoding='utf-8') as f:
        #     hotfix = f.read()
        #
        # dic = {'hotfix': hotfix}
        # jsonStr = json.dumps(dic).encode('utf-8')
        # zStr = gzip.compress(jsonStr)
        # gameglobal.hotfix = zStr
        # self.broadcastToAllAccountHotfix()

    def _handleCallQueue(self):
        if not self.callObjQueue:
            self._callback(1, '_handleCallQueue', (), gametimer.TIMER_TAG_HANDLE_CALL_QUEUE)
            return

        cnt = 50
        for callObj in self.callObjQueue[:cnt]:
            try:
                callObj()
            except Exception as e:
                gameengine.reportCritical('handleCallQueue error:', e, callObj)

        self.callObjQueue = self.callObjQueue[cnt:]
        self._callback(0.2, '_handleCallQueue', (), gametimer.TIMER_TAG_HANDLE_CALL_QUEUE)

    def addCallQueue(self, callableObj):
        self.callObjQueue.append(callableObj)

    # def _checkGlobalStubsHalfPrepared(self):
    #     for lineType, stubName in gameconst.lineStubMap.items():
    #         if not KBEngine.globalData.get(gameengine.makeLineStubKey(lineType)):
    #             INFO_MSG('still waiting for archived stub', stubName)
    #             return False
    #     for stubName in gameconst.GLOBAL_BASE_STUB_ARCHIVE:
    #         if not KBEngine.globalData.get(stubName):
    #             INFO_MSG('still waiting for archived stub', stubName)
    #             return False
    #
    #     for stubName in gameconst.GLOBAL_BASE_STUB_UNARCHIVE:
    #         if not KBEngine.globalData.get(stubName):
    #             INFO_MSG('still waiting for stub', stubName)
    #             return False
    #     for i in range(gameconst.TEAMSTUB_CONFIG_NUM):
    #         stubName = gameconst.GLOBAL_BASE_STUB_TEAMSTUB + str(i)
    #         if not KBEngine.globalData.get(stubName):
    #             INFO_MSG('still waiting for stub', stubName)
    #             return False
    #
    #     for dungeonNo, dVal in DDL.datas.items():
    #         if not dVal.get('type', 0):
    #             WARNING_MSG('skip dungeon stub in none dungeonType', dungeonNo)
    #             continue
    #
    #         if hasattr(self, '_skipInitDungeonStubs') and dungeonNo in self._skipInitDungeonStubs:
    #             WARNING_MSG('skip dungeon stub in err found', dungeonNo)
    #             continue
    #
    #         dungeonType = dVal['type']
    #         if dungeonType not in gameconst.DungeonSpaceType.COLL_DUNGEON:
    #             continue
    #
    #         enterType = dVal['enterType']
    #         if enterType in gameconst.DungeonEnterType.COLL_ALL:
    #             stubName = formula.getDungeonStubGlobalName(dungeonNo, enterType)
    #             if not KBEngine.globalData.get(stubName):
    #                 INFO_MSG('still waiting for dungeon stub', stubName)
    #                 return False
    #             continue
    #
    #         if enterType == gameconst.DungeonEnterType.BOTH:
    #             for enterType in gameconst.DungeonEnterType.COLL_BOTH:
    #                 stubName = formula.getDungeonStubGlobalName(dungeonNo, enterType)
    #                 if not KBEngine.globalData.get(stubName):
    #                     INFO_MSG('still waiting for dungeon stub', stubName)
    #                     return False
    #                 continue
    #
    #     else:
    #         if hasattr(self, '_skipInitDungeonStubs'):
    #             del self._skipInitDungeonStubs
    #     return self.localStubCreated

    def sendOfficialMessageForTest(self, gbId, content, registerChannel, seqId):
        channelList = registerChannel.split(',')
        playerStub = gameengine.getGlobalBase('PlayerStub')
        playerStub.doOnOthersClient([gbId, ], 'onOfficialMessage', (95, content, 1, channelList, seqId), None, '', ())

    def sendOfficialMessage(self, beginTime, endTime, content, tick, registerChannel, seqId, priority=0):
        channelList = registerChannel.split(',')
        officialMesTimerId = self._datetimeCallback(beginTime, '_sendOfficialMessage',
                                                    (content, tick, channelList, seqId, endTime, priority),
                                                    gametimer.TIMER_GM_OFFICIAL_MESSAGE)

        self.officialMesTimerDic[seqId] = officialMesTimerId
        self.officialMesOverTimer = self._datetimeCallback(endTime, '_overOfficialMessage',
                                                           (seqId,), gametimer.TIMER_GM_OFFICIAL_MESSAGE)
        if gameglobal.isBootstrap:
            value = ";".join((str(beginTime), str(endTime), content, str(tick), registerChannel))
            self.getRedisClient().hset(gameconst.RedisKey.IDIPMARQUEE_KEY, str(seqId), value)

    def _overOfficialMessage(self, seqId):
        if self.officialMesTickTimerDic.get(seqId, 0):
            self._cancelCallback(self.officialMesTickTimerDic.get(seqId), gametimer.TIMER_GM_OFFICIAL_MESSAGE)
        if self.officialMesTimerDic.get(seqId, 0):
            self._cancelDatetimeCallback(self.officialMesTimerDic.get(seqId), gametimer.TIMER_GM_OFFICIAL_MESSAGE)
        self.officialMesOverTimer = 0
        self.officialMesTimerDic.pop(seqId, None)
        self.officialMesTickTimerDic.pop(seqId, None)
        if gameglobal.isBootstrap:
            self.getRedisClient().hdel(gameconst.RedisKey.IDIPMARQUEE_KEY, str(seqId))

    def _sendOfficialMessage(self, content, tick, channelList, seqId, endTime=None, priority=0):
        self.officialMesTimerDic.pop(seqId, None)
        self.officialMesTickTimerDic.pop(seqId, None)
        self.onBroadcastToAllClients('onOfficialMessage', (95, content, 1, channelList, seqId))
        if endTime is None or utils.getNow() > endTime or tick <= 0:
            return

        tick += priority / 100
        officialMesTickTimerId = self._callback(tick, '_sendOfficialMessage',
                                                (content, tick, channelList, seqId, endTime),
                                                gametimer.TIMER_GM_OFFICIAL_MESSAGE, )
        self.officialMesTickTimerDic[seqId] = officialMesTickTimerId

    def stopOfficialMessage(self, seqId):
        self._cancelDatetimeCallback(self.officialMesOverTimer, gametimer.TIMER_GM_OFFICIAL_MESSAGE)
        if self.officialMesTickTimerDic.get(seqId, 0):
            self._cancelCallback(self.officialMesTickTimerDic.get(seqId), gametimer.TIMER_GM_OFFICIAL_MESSAGE)
        if self.officialMesTimerDic.get(seqId, 0):
            self._cancelDatetimeCallback(self.officialMesTimerDic.get(seqId), gametimer.TIMER_GM_OFFICIAL_MESSAGE)
        self.officialMesOverTimer = 0
        self.officialMesTimerDic.pop(seqId, None)
        self.officialMesTickTimerDic.pop(seqId, None)
        self.onBroadcastToAllClients('stopOfficialMessage', (seqId,))

        self.getRedisClient().hdel(gameconst.RedisKey.IDIPMARQUEE_KEY, str(seqId))

    def doRONECommand(self, cmdArgs):
        gmCommand.realDoCommand(*cmdArgs)

    def registerBaseappDataCallback(self, key, callback):
        self.baseappDataListener[key] = callback

    def doBaseappDataCallback(self, key, val):
        if key in self.baseappDataListener:
            self.baseappDataListener[key](val)

    def registerGlobalDataCallback(self, key, callback):
        self.globalDataListener[key] = callback

    def doGlobalDataCallback(self, key, val):
        if key in self.globalDataListener:
            self.globalDataListener[key](val)

    def forwardAttrMethodCall(self, attrName, method, args):
        attr = getattr(self, attrName, None)
        if attr is None:
            return

        func = getattr(attr, method, None)
        if not func:
            return

        func(*args)

    def onGetAllBaseApps(self):
        pass

    def onBaseappSumIncrement(self, key, val):
        DEBUG_MSG('onInc:', key, val)
        self.doBaseappDataCallback(key, val)

    def sendDataToRelivedBaseapp(self, fromHostName, fromGroupOrder, fromBaseapp, accountNum, avatarNum):
        INFO_MSG('sendDataToRelivedBaseapp', fromHostName, fromGroupOrder, fromBaseapp, accountNum, avatarNum)
        import game
        key = gameconst.GLOBALDATA_KEY_BASEAPP + ':' + fromHostName
        game.onGlobalData(key, fromBaseapp)

        key = gameconst.GLOBALDATA_KEY_BASEAPP_IDX + ':' + str(fromGroupOrder)
        game.onGlobalData(key, fromBaseapp)

        self.accountNum = accountNum
        self.avatarNum = avatarNum

        if gameglobal.localLoginStub:
            INFO_MSG('set account counter', self.avatarNum)
            gameglobal.localLoginStub.accountNumCounter.setSum(self.accountNum)

    def onCellappRelive(self, cellIndex):
        # 处理 plane space
        DEBUG_MSG('BaseApp onCellappRelive', cellIndex)

    def handleCellappDealth(self, dealthCellIndex):
        DEBUG_MSG("handleCellappDealth", dealthCellIndex)

    def onGetAllPlayer(self, su, data):
        if not hasattr(self, 'allPlayerInfo'):
            self.allPlayerInfo = {}
        allData = self.allPlayerInfo
        allData.update(data)
        if len(allData) == gameconfig.baseAppCount():
            result = []
            for info in allData.values():
                result += info
            self.allPlayerInfo = {}
            su.onCommandResult(0, '', {'data': result})

    def recordOfflinePlayerMailLog(self, toGBIDList, mailId, mailGBID, title, cont, attachStr, srcType, srcSubType, opUUID, desc, idipSource):
        mailAssistor.doRecordOfflinePlayerMailLog(toGBIDList[0], mailId, mailGBID, title, cont, attachStr, srcType, srcSubType,
                                                  opUUID, desc, idipSource)

    def buildAreaData(self):
        if gameglobal.areaData is not None:
            return

        gameglobal.areaData = ResMgr.loadAreaData()

    def replyHttpCommand(self, box, tag, cmdUUID, result, retErrMsg, bodyBytes, cmdStr):
        allResult = self.gmCmdDic.get(cmdUUID, [])
        allResult.append((result, retErrMsg, bodyBytes))
        cmd = gameglobal.GM_CMDS.get(cmdStr)
        if cmd.component == gameconst.BASE:
            allCount = gameconfig.baseAppCount()
        elif cmd.component == gameconst.CELL:
            allCount = gameconfig.cellAppCount()
        else:
            allCount = gameconfig.baseAppCount() + gameconfig.cellAppCount()
        if len(allResult) == allCount:
            allResult_dict = {"allResult": allResult}
            box.replyHttpCommand(tag, cmdUUID, result, retErrMsg, allResult_dict)
            self.gmCmdDic.pop(cmdUUID)
        else:
            self.gmCmdDic[cmdUUID] = allResult
