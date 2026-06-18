# -*- coding: utf-8 -*-
import functools
import KBEngine
from KBEDebug import *

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
import ResMgr
import copy
import iTimer
import iBaseNoCell
import asyncore
import iBroadcastEvent
import iGameStart
import iWaitMapGameStart
import elasticUtils

from proto.interface_pb2 import BaseApp as BaseAppService
from proto.interface_pb2 import Void, Interface_Stub, ConfigVal, ListVal, IntVal, SetAccountCompVal, AntiAddictionData, MapleServerInfo, PatchVersionData

from rpc import RpcChannel


class InterfaceBaseappClient(BaseAppService):
    def __init__(self, baseapp, address):
        self.channel = RpcChannel.RpcChannel(self)
        self.baseapp = baseapp
        self.interfaceStub = Interface_Stub(self.channel)

        self.channel.connect(address)

    def on_disconnected(self):
        pass

    def on_connected(self):
        pass

    def reqSyncCacheConfigOnBaseapp(self, rpc_controller, request, done):
        _nameStr, valueStr = gameconfig.packInterfaceDiffCache()
        if _nameStr and valueStr:
            configVal = ConfigVal()
            configVal.name, configVal.val = _nameStr, valueStr
            self.interfaceStub.syncCacheConfigOnBaseapp(None, configVal, None)

    def activeTickCallback(self, rpc_controller, request, done):
        pass

    def setAccountCompResult(self, rpc_controller, reply, done):
        if not reply.result:
            LOG_ERR('setAccountCompResult', reply.entityID)
            return

        _ent = KBEngine.entities.get(reply.entityID)
        if not _ent:
            LOG_ERR('setAccountCompResult', 'entity not found', reply.entityID)
            return

        _ent.onSetAccountCompSuccess()


class BaseApp(iBaseNoCell.IBaseNoCell, iTimer.ITimer, iBroadcastEvent.IBroadcastEvent, iWaitMapGameStart.IWaitMapGameStart, iGameStart.IGameStart, iRouter.IRouter):
    INITIAL_INIT = 0.1

    def __init__(self):
        super(BaseApp, self).__init__()
        self.initDatetimeTimerTick()

        self._loadEntityTypeToDBID()
        self.buildAreaData()
        self.redisAsyncClient = gameRedisAsync.AsyncRedisClient(
            gameconfig.redisServer(), gameconfig.redisPort(),
            gameconfig.redisPassword(), gameconfig.redisUsername())
        self.redisAsyncClient.onConnect()
        self.redisAttrsCache = {}
        self.lockDict = {}
        self.interfaceClient = {}
        self.gmCmdDic = {}
        self.initAysncore()
        self.accountNum = 0
        self.avatarNum = 0

        self.pyAddTimer(5, 1, gametimer.TIMER_REDIS_HEART_BEAT)
        self.pyAddTimer(1, 5, gametimer.TIMER_BASEAPP_CONN_INTERFACE)
        self.pyAddTimer(gameconst.CENTRAL_SERVICE_HEARTBEAT_INTERVAL, gameconst.CENTRAL_SERVICE_HEARTBEAT_INTERVAL,
                        gametimer.BASEAPP_INTERFACE_ACTIVE)

        self.pyAddTimer(1, 1, gametimer.TIMER_BASEAPP_ASYNC_TICK)

        self.pyAddTimer(gameconst.CENTRAL_SERVICE_HEARTBEAT_INTERVAL, gameconst.CENTRAL_SERVICE_HEARTBEAT_INTERVAL, gametimer.BASEAPP_ACTIVE_TICK)

        self.addTimerCB(30, '_handleCallQueue', (), gametimer.TIMER_TAG_HANDLE_CALL_QUEUE)

        self.pyAddTimer(self.INITIAL_INIT + random.random(), 0, gametimer.BASEAPP_TIMER_INIT)

        self.pyAddTimer(1, gameconst.AuctionIdCollection.CHECK_TIP_INTERVAL, gametimer.CHECK_TIP_PLAYER_AUCTION_ITEM_COLLECTION)

        self.pyAddTimer(1, gameconst.DrawCardPoolMacro.CHECK_TIME_LIMIT_INTERVAL, gametimer.CHECK_DRAW_CARD_POOL_TIME_LIMIT)

        if gameconfig.elasticServer() and gameglobal.isBootstrap:
            self.addTimerCB(1, 'initElastic', (), gametimer.TIMER_TAG_INIT_ELASTIC)

    def initElastic(self):
        elasticUtils.ElasticUtils.init(self._initElasitc)

    def _initElasitc(self, *args):
        LOG_INFO('init elastic', args)

    def setStartGbId(self, cursor, num):
        self.startGbId = cursor * ((1 << gameconst.SERVER_TIMESTAMP_BIT_SHIFT) // num)

    def getRedisClient(self):
        return self.redisAsyncClient

    def getStartGbId(self):
        return self.startGbId

    def initAysncore(self):
        if self.asyncTimer:
            return

        LOG_INFO('initAysncore')
        self.asyncTimer = self.pyAddTimer(1, 0.1, gametimer.TIMER_ASYNCORE_TICK)

    def preReloadScript(self):
        return

    def onTimer(self, timerID, userData):
        self._onTimerTrigger(timerID, userData)

        if userData == gametimer.BASEAPP_TIMER_INIT:
            if self.initProcedures:
                self.pyAddTimer(0.5, 0, gametimer.BASEAPP_TIMER_INIT)
                LOG_INFO('waitting for baseapp init:', list(self.initProcedures.keys()))
                return
            hostName = utils.getPythonAddr()
            stubIndex = formula.fetchStubIndex()
            gameengine.setGlobalData(gameconst.GLOBALDATA_KEY_BASEAPP + ':' + hostName, self)
            gameengine.setGlobalData(gameconst.GLOBALDATA_KEY_BASEAPP_IDX + ':' + str(stubIndex), self)
            self.setTempMiscProp(gameconst.GLOBALDATA_KEY_BASEAPP_IDX, stubIndex)
            # self.pyAddTimer(1, 10, gametimer.BASEAPP_TIMER_CREATE_SPACE_MARKER)
            if gameconfig.isWaitMapServer():
                self.pyAddTimer(1, 0, gametimer.WAITMAP_TIMER_START)
            else:
                self.pyAddTimer(1, 0, gametimer.BASESTUB_TIMER_CHECK_COMPONENTS)

        elif utils.isBelongTimerTag(userData):
            self._onTimerCallback(timerID)

        elif userData == gametimer.TIMER_ASYNCORE_TICK:
            asyncore.loop(0, True, None, 1)

        elif userData == gametimer.TIMER_REDIS_HEART_BEAT:
            self._onRedisHeartBeat()

        elif userData == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()

        elif userData == gametimer.BASEAPP_INTERFACE_ACTIVE:
            self._checkInterfaceActive()

        elif userData == gametimer.TIMER_BASEAPP_CONN_INTERFACE:
            self._connectInterfaceApp()

        elif userData == gametimer.BASEAPP_ACTIVE_TICK:
            if gameconfig.enableRouterServer():
                self.checkAllRouterServerActive()

        elif userData == gametimer.TIMER_BASEAPP_ASYNC_TICK:
            self.connectAllRouterServer()

        elif userData == gametimer.CHECK_TIP_PLAYER_AUCTION_ITEM_COLLECTION:
            self._checkTipPlayerAuctionItemCollection()

        elif userData == gametimer.CHECK_DRAW_CARD_POOL_TIME_LIMIT:
            self._checkDrawCardPoolTimeLimit()

        else:
            if gameconfig.isWaitMapServer():
                iWaitMapGameStart.IWaitMapGameStart.onWaitMapTimer(self, timerID, userData)
            else:
                iGameStart.IGameStart.onTimer(self, timerID, userData)

    def onRouterServerConnected(self, routerServerId):
        self.tryRegisterBaseApp(routerServerId)

    def tryRegisterBaseApp(self, routerServerId):
        if not KBEngine.globalData.get(gameconst.GLOBALDATA_KEY_GAME_READY):
            self.addTimerCB(5, 'tryRegisterBaseApp', (routerServerId,), gametimer.TIMER_TAG_TRY_REGISTER_BASEAPP)
        else:
            self.registerBaseApp(routerServerId)

    def _onRedisHeartBeat(self):
        if not self.redisAsyncClient.isConnect():
            LOG_ERR('the redis server is not connected')
            self.redisAsyncClient.disconnectRedis()
            self.redisAsyncClient.onConnect()

    def _checkInterfaceActive(self):
        for _client in self.interfaceClient.values():
            if _client and _client.channel.dispatcher:
                _client.interfaceStub.activeTick(None, Void(), None)

    def _connectInterfaceApp(self):
        _hostList = gameconfig.interfaceRpcHostList()
        for _host in _hostList:
            key = ':'.join(_host.values())
            _client = self.interfaceClient.get(key, None)
            if _client and _client.channel.dispatcher: continue

            _addr, _port = _host['addr'], int(_host['port'])
            LOG_INFO('connect interface', _addr, _port)
            self.interfaceClient[key] = InterfaceBaseappClient(self, (_addr, _port))

    def _callInterfaceApp(self, func, *args):
        for _client in self.interfaceClient.values():
            if _client and _client.channel.dispatcher:
                method = getattr(_client.interfaceStub, func)
                if method:
                    method(*args)

    def _checkTipPlayerAuctionItemCollection(self):
        newAuctionItemCache = gameglobal.newAuctionItemCache
        if not len(newAuctionItemCache):
            return

        copyNewAuctionItemCache = copy.deepcopy(newAuctionItemCache)
        self.broadcastToAllAvatar(gameconst.BASE, 'tipPlayerAuctionItemCollection', (copyNewAuctionItemCache,))
        newAuctionItemCache.clear()

    def _checkDrawCardPoolTimeLimit(self):
        curTimestamp = utils.curTS()
        lastTimestamp = self.lastCheckDrawCardPoolTimestamp
        self.lastCheckDrawCardPoolTimestamp = curTimestamp

        poolsInfo = utils.checkDrawCardPoolTimeLimit(curTimestamp, gameconst.DrawCardPoolMacro.CHECK_TIME_LIMIT_TYPE_TIMER)

        if len(poolsInfo):
            LOG_INFO('_checkDrawCardPoolTimeLimit', lastTimestamp, curTimestamp, poolsInfo)
            self.broadcastToAllAvatar(gameconst.BASE, 'triggerTimeLimitGuaranteedReward', (poolsInfo,))

    # 以归档模式创建base实体，首先查询数据库中是否存在该实体，若存在则调用createBaseLocallyFromDB来创建
    # 否则，使用gamebase.createGlobal的方式直接创建
    def createArchiveStub(self, clsName, properties, globalName):
        self.preparingEntTypes.append(clsName)
        _dbid = gameglobal.entityTypeToDBID.get(clsName)
        LOG_INFO('createArchiveStub', clsName, globalName, _dbid)
        if not _dbid:
            self._onArchiveStubLookup(clsName, 0, properties, globalName, False)
        else:
            KBEngine.lookUpEntityByDBID(
                clsName,
                _dbid,
                functools.partial(self._onArchiveStubLookup, clsName, _dbid, properties, globalName),
            )

    def _onArchiveStubLookup(self, clsName, dbid, props, globalName, box):
        LOG_INFO('_onArchiveStubLookup', clsName, dbid, box, globalName, props)
        if box == False:
            if dbid:
                # lookUpEntityByDBID的box参数只有两种情况会返回false
                # 1.数据库中tbl_className表中没有dbid对应的实体，但dbid在gameglobal.entityTypeToDBID中，所以应该是哪里出错了，这里停下来报错不让成功启动
                # 2.数据库kbe_entitylog表中entity对应的数据serverGroupID与当前服不匹配（因为kbengine允许多组服共用一个库）
                # 如果从数据库中找到对应dbid数据，box返回true
                # 如果对应dbid的实体已经创建则返回实体的entity_call
                LOG_ERR('_onArchiveStubLookup: lookup entity failed')
            else:
                gamebase.createArchiveStubGlobal(clsName, props, globalName)
        elif box == True:
            KBEngine.createEntityFromDBID(
                clsName,
                dbid,
                functools.partial(self._onArchiveStubLoad, clsName, globalName),
            )
        else:
            LOG_INFO('[%s %s] has been loaded' % (clsName, dbid,))

        return

    def _onArchiveStubLoad(self, clsName, globalName, ent, databaseID, wasActive):
        if ent:
            LOG_INFO('successful to load [%s %s] from database' % (clsName, databaseID,))
            # TODO:查下registerGlobally
            ent.onGlobalBase(True, globalName)
        else:
            LOG_ERR('Error:failed to load [%s %s] from database')

        return

    def createUnarchiveStub(self, clsName, props, globalName):
        self.preparingEntTypes.append(clsName)
        gamebase.createGlobal(clsName, props, globalName)

    def destroyMarker(self, spaceNo):
        sm = gamebase.getSpaceMarkerBaseByNo(spaceNo)
        if sm:
            sm.doEntireDestroy(False, False)

    def _loadEntityTypeToDBID(self):
        self.addInitProcedure(gameconst.BaseAppIniting.LOAD_ENTITY_DBID)
        _sql = 'SELECT entityType, entityDBID FROM game_entity_dbid'
        KBEngine.executeRawDatabaseCommand(
            _sql,
            self._onGetEntityDBIDFromDB,
        )

    def _onGetEntityDBIDFromDB(self, result, num, insertId, error):
        if isinstance(error, str):
            LOG_ERR('==========Error:failed to exec query base==========%s' % error)
            return

        gameglobal.entityTypeToDBID = {}
        self.onInitProcedureDone(gameconst.BaseAppIniting.LOAD_ENTITY_DBID)
        if not result:
            return

        for _entityType, dbid in result:
            _entityType = utils.bytesToString(_entityType)
            try:
                __import__(_entityType)
            except:
                gamesql.deleteEntityDBID(_entityType)
                continue
            gameglobal.entityTypeToDBID[_entityType] = int(dbid)

    def onGmFindAccount(self, result, accountName, idx, raw, uid):
        gmCommand.onFindAccount(result, accountName, idx, raw, uid)

    def onGmFindEntity(self, result, uid):
        gmCommand.onFindEntity(result, uid)

    def onGmLookUpAvatar(self, base, role, uid, idx, raw):
        gmCommand.onLookUpAvatar(base, role, uid, idx, raw)

    def onDoCmdSucc(self, uid):
        gmCommand.onBroadcastCmdSuccess(uid)

    def onDoCmdFail(self, uid):
        gmCommand.onBroadcastCmdFail(uid)

    def lockKey(self, key):
        timestamp = self.lockDict.get(key, 0)
        now = utils.curTS()
        if now - timestamp < 60:
            return False

        self.lockDict[key] = now
        return True

    def pushRedisAttrs(self, gbId, attrs):
        if gbId in self.redisAttrsCache:
            self.redisAttrsCache[gbId].update(attrs)
        else:
            self.redisAttrsCache[gbId] = attrs

    def unlockKey(self, key):
        self.lockDict.pop(key, None)

    def popRedisAttrs(self, gbId):
        return self.redisAttrsCache.pop(gbId, {})

    def notifyInterfaceConfigChanged(self, name, val):
        _configVal = ConfigVal()
        _configVal.name = name
        _configVal.val = val

        self._callInterfaceApp('gameConfigChangedOnBaseapp', None, _configVal, None)

    def notifyInterfaceCacheConfigChanged(self, name, val):
        _configVal = ConfigVal()
        _configVal.name = name
        _configVal.val = val

        self._callInterfaceApp('cacheConfigOnBaseapp', None, _configVal, None)

    def notifyInterfaceDataReload(self, args):
        _listVal = ListVal()
        for arg in args:
            _listVal.vals.append(arg)
        self._callInterfaceApp('interfaceDataReload', None, _listVal, None)

    def notifyInterfaceReload(self):
        self._callInterfaceApp('interfaceReload', None, Void(), None)

    def notifyInterfaceSyncRegisterCount(self, count):
        _intVal = IntVal()
        _intVal.value = count
        self._callInterfaceApp('syncRegisterCount', None, _intVal, None)

    def readhotfix(self):
        LOG_INFO('do hotfix')

    def _handleCallQueue(self):
        if not self.callObjQueue:
            self.addTimerCB(1, '_handleCallQueue', (), gametimer.TIMER_TAG_HANDLE_CALL_QUEUE)
            return

        _cnt = 50
        for callObj in self.callObjQueue[:_cnt]:
            try:
                callObj()
            except Exception as e:
                gameengine.panicStack('handleCallQueue error:', e, callObj)

        self.callObjQueue = self.callObjQueue[_cnt:]
        self.addTimerCB(0.2, '_handleCallQueue', (), gametimer.TIMER_TAG_HANDLE_CALL_QUEUE)

    def addToCallQueue(self, callableObj):
        self.callObjQueue.append(callableObj)

    def sendOfficialMessageForTest(self, gbId, content, registerChannel, seqId):
        channelList = registerChannel.split(',')
        playerStub = gameengine.getGlobalBase('PlayerStub')
        playerStub.doOnOthersClient([gbId, ], 'onOfficialMessage', (95, content, 1, channelList, seqId, '', 0), None, '', ())

    def sendOfficialMessage(self, beginTime, endTime, content, tick, registerChannel, seqId, priority=0, chatChannelList='', chatType=0):
        if seqId in self.officialMesTimerDict:
            LOG_ERR('official message is already exist', seqId)
            return

        if seqId in self.officialMesTickTimerDict:
            LOG_ERR('official message is already exist', seqId)
            return

        channelList = registerChannel.split(',')
        officialMesTimerId = self._datetimeCallback(beginTime, '_sendOfficialMessage',
                                                    (content, tick, channelList, seqId, endTime, priority, chatChannelList, chatType),
                                                    gametimer.TIMER_GM_OFFICIAL_MESSAGE)

        self.officialMesTimerDict[seqId] = officialMesTimerId
        if gameglobal.isBootstrap:
            value = ";".join((str(beginTime), str(endTime), content, str(tick), registerChannel))
            self.getRedisClient().hset(gameconst.RedisKey.IDIPMARQUEE_KEY, str(seqId), value)

    def _overOfficialMessage(self, seqId):
        if self.officialMesTickTimerDict.get(seqId, 0):
            self.cancelTimerCB(self.officialMesTickTimerDict.get(seqId), gametimer.TIMER_GM_OFFICIAL_MESSAGE)
        if self.officialMesTimerDict.get(seqId, 0):
            self._cancelDatetimeCallback(self.officialMesTimerDict.get(seqId), gametimer.TIMER_GM_OFFICIAL_MESSAGE)
        self.officialMesTimerDict.pop(seqId, None)
        self.officialMesTickTimerDict.pop(seqId, None)
        if gameglobal.isBootstrap:
            self.getRedisClient().hdel(gameconst.RedisKey.IDIPMARQUEE_KEY, str(seqId))

    def _sendOfficialMessage(self, content, tick, channelList, seqId, endTime=None, priority=0, chatChannelList='', chatType=0):
        self.officialMesTimerDict.pop(seqId, None)
        self.officialMesTickTimerDict.pop(seqId, None)
        self.onBroadcastToAllClients('onOfficialMessage', (95, content, 1, channelList, seqId, chatChannelList, chatType))
        if endTime is None or utils.curTS() > endTime or tick <= 0:
            return

        tick += priority / 100
        officialMesTickTimerId = self.addTimerCB(tick, '_sendOfficialMessage',
                                                (content, tick, channelList, seqId, endTime, priority, chatChannelList, chatType),
                                                gametimer.TIMER_GM_OFFICIAL_MESSAGE, )
        self.officialMesTickTimerDict[seqId] = officialMesTickTimerId

    def stopOfficialMessage(self, seqId):
        if self.officialMesTickTimerDict.get(seqId, 0):
            self.cancelTimerCB(self.officialMesTickTimerDict.get(seqId), gametimer.TIMER_GM_OFFICIAL_MESSAGE)
        if self.officialMesTimerDict.get(seqId, 0):
            self._cancelDatetimeCallback(self.officialMesTimerDict.get(seqId), gametimer.TIMER_GM_OFFICIAL_MESSAGE)
        self.officialMesTimerDict.pop(seqId, None)
        self.officialMesTickTimerDict.pop(seqId, None)
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
        LOG_DBG('onInc:', key, val)
        self.doBaseappDataCallback(key, val)

    def sendDataToRelivedBaseapp(self, fromHostName, fromGroupOrder, fromBaseapp, accountNum, avatarNum):
        LOG_INFO('sendDataToRelivedBaseapp', fromHostName, fromGroupOrder, fromBaseapp, accountNum, avatarNum)
        import game
        key = gameconst.GLOBALDATA_KEY_BASEAPP + ':' + fromHostName
        game.onGlobalData(key, fromBaseapp)

        key = gameconst.GLOBALDATA_KEY_BASEAPP_IDX + ':' + str(fromGroupOrder)
        game.onGlobalData(key, fromBaseapp)

        self.accountNum = accountNum
        self.avatarNum = avatarNum

        if gameglobal.localLoginStub:
            LOG_INFO('set account counter', self.avatarNum)
            gameglobal.localLoginStub.accountNumCounter.setSum(self.accountNum)

    def onCellappRelive(self, cellIndex):
        # 处理 plane space
        LOG_DBG('BaseApp onCellappRelive', cellIndex)

    def handleCellappDealth(self, dealthCellIndex):
        LOG_DBG("handleCellappDealth", dealthCellIndex)

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

    def setAccountCompIdToInterface(self, accountName, compId, entId):
        _req = SetAccountCompVal()
        _req.accountName = accountName
        _req.compID = compId
        _req.entityID = entId

        for _client in self.interfaceClient.values():
            if _client and _client.channel.dispatcher:
                _client.interfaceStub.setAccountComp(None, _req, None)

    def setBaseAppLockState(self, baseapp, state):
        LOG_DBG('setBaseAppLockState', baseapp.id, state)
        self.baseAppStateLock.setdefault(state, set()).add(baseapp.id)

        _allOk = len(self.baseAppStateLock[state]) == gameconfig.baseAppCount()
        baseapp.onSetBaseAppLockResult(_allOk, state)

    def onSetBaseAppLockResult(self, isOk, state):
        LOG_DBG('onSetBaseAppLockResult', isOk, state)
        if state == gameconst.BASEAPP_STATE_LOCK_WAIT_FULL_PREPARE:
            if isOk:
                if gameconfig.isWaitMapServer():
                    self.pyAddTimer(0.1, 0, gametimer.WAITMAP_TIMER_SET_SERVER_STATE)
                else:
                    self.pyAddTimer(0.1, 0, gametimer.BASESTUB_TIMER_CHECK_LINE_READY)
            else:
                LOG_INFO('still waiting for all stub full prepare in lock')
                if gameconfig.isWaitMapServer():
                    self.pyAddTimer(0.5, 0, gametimer.WAITMAP_TIMER_GLOBAL_STUBS_FULL_PREPARE)
                else:
                    self.pyAddTimer(0.5, 0, gametimer.BASESTUB_TIMER_GLOBAL_STUBS_FULL_PREPARE)

    def doAntiAddiction(self):
        antiAddictionData = gameglobal.antiAddictionData
        LOG_INFO("baseapp doAntiAddiction", antiAddictionData)
        if antiAddictionData[0] == gameconst.AntiAddictionTimeType.PERMIT:
            LOG_DBG("baseapp doAntiAddiction PERMIT", antiAddictionData[1])
        elif antiAddictionData[0] == gameconst.AntiAddictionTimeType.PROHIBIT:
            LOG_DBG("baseapp doAntiAddiction PROHIBIT", antiAddictionData[1])
            minorAccountCacheList = list(gameglobal.localMinorAccountCache.keys())
            self.kickAllMinorAccountBatchly(iter(minorAccountCacheList), 10, 0.1)

    def kickAllMinorAccountBatchly(self, accountIter, batchNum, interval):
        LOG_INFO("kickAllMinorAccountBatchly-----------", batchNum, interval)
        for i in range(batchNum):
            (minorAccountName) = next(accountIter, (""))
            if not minorAccountName:
                LOG_INFO("kickAllMinorAccountBatchly finish kick all minor account")
                return
            minorAccount = gameglobal.localMinorAccountCache.get(minorAccountName, None)
            if not minorAccount:
                LOG_INFO("kickAllMinorAccountBatchly minor account alerady logout")
                return
            LOG_INFO("kickAllMinorAccountBatchly account=%s" % (minorAccount.__ACCOUNT_NAME__))
            minorAccount.destroyAccount(gameconst.OFFLINE_REASON_ANIT_ADDICTION)
        self.addTimerCB(interval, 'kickAllMinorAccountBatchly', (accountIter, batchNum, interval), gametimer.TIMER_TAG_KICK_ALL_MINOR_ACCOUNT_TIMER)

    def updateAntiAddictionData(self, timeType, nextStartTime):
        _req = AntiAddictionData()
        _req.timeType = timeType
        _req.timestamp = nextStartTime

        for client in self.interfaceClient.values():
            if client and client.channel.dispatcher:
                client.interfaceStub.updateAntiAddictionData(None, _req, None)

    def setMapleServerInfo(self, data):
        LOG_DBG("setMapleServerInfo", data)
        _req = MapleServerInfo()
        _req.data = data

        for client in self.interfaceClient.values():
            if client and client.channel.dispatcher:
                client.interfaceStub.setMapleServerInfo(None, _req, None)

    def updateRequiredClientVersion(self, platId, patchVerStr):
        LOG_DBG("updateRequiredClientVersion", platId, patchVerStr)
        _req = PatchVersionData()
        _req.platId = platId
        _req.patchVerStr = patchVerStr

        for client in self.interfaceClient.values():
            if client and client.channel.dispatcher:
                client.interfaceStub.updatePatchVersionData(None, _req, None)

    def doUpdateFreeTicketNumConfig(self, subType, expandInfoList):
        now = utils.curTS()
        LOG_INFO("doUpdateFreeTicketNumConfig", now, subType, expandInfoList)
        self.broadcastToAllAvatar(gameconst.BASE, 'onUpdateFreeTicketNumConfig', (subType,))
