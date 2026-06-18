# -*- coding: utf-8 -*-
import dataUtils
import formula
import KBEngine
import json

import gameclass
from KBEDebug import *
import gametimer
import gameengine
import gameconfig
import gameconst
import gameglobal
import gamesql
import utils
import random
import gamebase
import dataUtils
import redisUtils

import gamePlay_gamePlay as DDL
import wonderLand_floor as WL_FD
import abyss_floor as AB_FD
import cube_floor as C_FD
import guildChallenge_basicInfo as GC_BI

class IGameStart(object):
    def __init__(self):
        super(IGameStart, self).__init__()
        self.initProcedures = {}
        self.lineReady = {}
        self.lineEntityReadyNum = {}
        self.worldRefreshEntityReady = {}
        self.preparingEntTypes = []
        self.initedCellapps = []

    def onTimer(self, tid, userArg):
        if userArg == gametimer.BASESTUB_TIMER_CHECK_COMPONENTS:
            cellapps = self.initedCellapps
            if len(cellapps) != gameconfig.cellAppCount():
                LOG_INFO('start waiting: waiting for cellapps start: %s/%s' % (cellapps, gameconfig.cellAppCount()))
                self.pyAddTimer(1, 0, gametimer.BASESTUB_TIMER_CHECK_COMPONENTS)
                return

            comps = KBEngine.getComponents()
            if len(comps['baseapps']) + 1 != gameconfig.baseAppCount():
                LOG_INFO('start waiting: waiting for baseapps start: %s/%s' % (
                len(comps['baseapps']) + 1, gameconfig.baseAppCount()))
                self.pyAddTimer(1, 0, gametimer.BASESTUB_TIMER_CHECK_COMPONENTS)
                return

            LOG_INFO('starting: components ready')

            self.pyAddTimer(1, 0, gametimer.BASESTUB_TIMER_BASEAPPS)

        elif userArg == gametimer.BASESTUB_TIMER_BASEAPPS:
            baseAppCnt = gameconfig.baseAppCount()
            howManyBaseApp = gameengine.howManyBaseApps()

            if howManyBaseApp < baseAppCnt:
                LOG_INFO('start waiting: waiting for creating all BaseApp Entity: %s/%s' % (howManyBaseApp, baseAppCnt))
                self.pyAddTimer(1, 0, gametimer.BASESTUB_TIMER_BASEAPPS)
                return

            LOG_INFO('starting: successful to create all baseapps&cellapps, now create stubs')
            self.onGetAllBaseApps()

            self.createLocalStubs()
            self.pyAddTimer(0.1, 0, gametimer.GET_ALL_SERVER_INFO)

        elif userArg == gametimer.GET_ALL_SERVER_INFO:
            _url = gameconfig.mapleAllServerUrl()
            if gameglobal.isBootstrap and _url:
                KBEngine.urlopenv2(_url, self._onGetAllServerResult, method='GET')
                return

            self.pyAddTimer(0.1, 0, gametimer.WAIT_GET_ALL_SERVER_INFO)

        elif userArg == gametimer.WAIT_GET_ALL_SERVER_INFO:
            if not gameglobal.mapleServerInfo:
                LOG_WARN('still waiting for get mapleServerInfo')
                self.pyAddTimer(0.1, 0, gametimer.WAIT_GET_ALL_SERVER_INFO)
                return

            if gameglobal.mapleServerInfo[gameconfig.serverId()]['start_time'] != gameconfig.serverOpenTime():
                LOG_ERR(f'server startTime not match: {gameglobal.mapleServerInfo[gameconfig.serverId()]}, {gameconfig.serverOpenTime()}')
                self.pyAddTimer(1, 0, gametimer.WAIT_GET_ALL_SERVER_INFO)
                return
            
            # 服务器开服时间和状态写redis
            if gameglobal.isBootstrap:
                key = gameconst.RedisKey.SERVER_OPEN_TIME + str(gameconfig.serverId())
                redisUtils.RedisUtils.cmdSet(key, str(gameconfig.serverOpenTime()), self._onServerOpenTime)

                key = gameconst.RedisKey.SERVER_OPEN_STATE + str(gameconfig.serverId())
                redisUtils.RedisUtils.cmdSet(key, str(gameconfig.permitLogin()), self._onServerOpenState)

            self.pyAddTimer(0.1, 0, gametimer.CREATE_LEADER_BOARD_STUB)

        elif userArg == gametimer.CREATE_LEADER_BOARD_STUB:
            if gameglobal.isBootstrap:
                self.createLeaderBoardStub()
            self.pyAddTimer(1, 0, gametimer.WAIT_LEADER_BOARD_STUB_READY)

        elif userArg == gametimer.WAIT_LEADER_BOARD_STUB_READY:
            for _lbType in gameconst.LeaderBoardType.ALL_KEYS:
                _stub = gameengine.getLeaderStub(_lbType, reportErr=False)
                if not _stub:
                    LOG_INFO('start waiting: waiting for leaderBoardStub ready', _lbType)
                    self.pyAddTimer(0.1, 0, gametimer.WAIT_LEADER_BOARD_STUB_READY)
                    return

            self.pyAddTimer(0.1, 0, gametimer.CREATE_GLOBAL_STUBS)

        elif userArg == gametimer.CREATE_GLOBAL_STUBS:
            if gameglobal.isBootstrap:
                self.createGlobalStubs()

            self.pyAddTimer(0.1, 0, gametimer.BASESTUB_TIMER_GLOBAL_WAIT_STUBS_HALF_PREPARE)

        elif userArg == gametimer.BASESTUB_TIMER_GLOBAL_WAIT_STUBS_HALF_PREPARE:
            for stubName in gameconst.GLOBAL_BASE_STUB_UNARCHIVE:
                globalName = stubName
                if not gameengine.getGlobalBase(globalName, reportErr=False):
                    LOG_INFO('start waiting: still waiting for stub:', globalName)
                    self.pyAddTimer(0.1, 0, gametimer.BASESTUB_TIMER_GLOBAL_WAIT_STUBS_HALF_PREPARE)
                    return

            for i in range(gameconst.TEAMSTUB_CONF_NUM):
                stubName = gameconst.GLOBAL_BASE_STUB_TEAMSTUB + str(i)
                if not KBEngine.globalData.get(stubName):
                    LOG_INFO('still waiting for team stub', stubName)
                    self.pyAddTimer(0.1, 0, gametimer.BASESTUB_TIMER_GLOBAL_WAIT_STUBS_HALF_PREPARE)
                    return False

            for i in range(gameconst.RAIDSTUB_CONFIG_NUM):
                stubName = gameconst.GLOBAL_BASE_STUB_RAIDSTUB + str(i)
                if not KBEngine.globalData.get(stubName):
                    LOG_INFO('still waiting for raid stub', stubName)
                    self.pyAddTimer(0.1, 0, gametimer.BASESTUB_TIMER_GLOBAL_WAIT_STUBS_HALF_PREPARE)
                    return False
                
            for i in range(gameconst.STATISTICSTUB_CONFIG_NUM):
                stubName = gameconst.GLOBAL_BASE_STUB_STATISTICSTUB + str(i)
                if not KBEngine.globalData.get(stubName):
                    LOG_INFO('still waiting for statistic stub', stubName)
                    self.pyAddTimer(0.1, 0, gametimer.BASESTUB_TIMER_GLOBAL_WAIT_STUBS_HALF_PREPARE)
                    return False

            for lineType in gameconst.lineStubMap().keys():
                globalName = gameengine.buildLineStubName(lineType)
                if not gameengine.getGlobalBase(globalName, reportErr=False):
                    LOG_INFO('start waiting: still waiting for line stub:', globalName)
                    self.pyAddTimer(0.1, 0, gametimer.BASESTUB_TIMER_GLOBAL_WAIT_STUBS_HALF_PREPARE)
                    return

            for stubName in gameconst.GLOBAL_BASE_STUB_ARCHIVE:
                if not gameengine.getGlobalBase(stubName, reportErr=False):
                    LOG_INFO('still waiting for archived stub', stubName)
                    self.pyAddTimer(0.1, 0, gametimer.BASESTUB_TIMER_GLOBAL_WAIT_STUBS_HALF_PREPARE)
                    return

            for dungeonNo, dVal in DDL.datas.items():
                if not dVal.get('type', 0):
                    LOG_WARN('skip dungeon stub in none dungeonType', dungeonNo)
                    continue

                if hasattr(self, '_skipInitDungeonStubs') and dungeonNo in self._skipInitDungeonStubs:
                    LOG_WARN('skip dungeon stub in err found', dungeonNo)
                    continue

                dungeonType = dVal['type']
                if dungeonType not in gameconst.DungeonSpaceTypeEnum.COLL_DUNGEON:
                    continue

                enterType = dVal['enterType']
                if enterType in gameconst.DungeonEnterTypeEnum.COLL_ALL:
                    stubName = formula.fetchDungeonStubGlobalName(dungeonNo, enterType)
                    if not KBEngine.globalData.get(stubName):
                        LOG_INFO('still waiting for dungeon stub', stubName)
                        self.pyAddTimer(0.1, 0, gametimer.BASESTUB_TIMER_GLOBAL_WAIT_STUBS_HALF_PREPARE)
                        return
                    continue

                if enterType == gameconst.DungeonEnterTypeEnum.BOTH:
                    for enterType in gameconst.DungeonEnterTypeEnum.COLL_BOTH:
                        stubName = formula.fetchDungeonStubGlobalName(dungeonNo, enterType)
                        if not KBEngine.globalData.get(stubName):
                            LOG_INFO('still waiting for dungeon stub', stubName)
                            self.pyAddTimer(0.1, 0, gametimer.BASESTUB_TIMER_GLOBAL_WAIT_STUBS_HALF_PREPARE)
                            return
                        continue

            else:
                if hasattr(self, '_skipInitDungeonStubs'):
                    del self._skipInitDungeonStubs


            for _floorNo in WL_FD.datas.keys():
                if not gameengine.getGlobalBase('WonderLandStub%d' % _floorNo, reportErr=False):
                    LOG_INFO('start waiting: waiting for wonderland stub', _floorNo)
                    self.pyAddTimer(0.1, 0, gametimer.BASESTUB_TIMER_GLOBAL_WAIT_STUBS_HALF_PREPARE)
                    return

            for _floorNo in AB_FD.datas.keys():
                if not gameengine.getGlobalBase('AbyssStub%d' % _floorNo, reportErr=False):
                    LOG_INFO('start waiting: waiting for abyss stub', _floorNo)
                    self.pyAddTimer(0.1, 0, gametimer.BASESTUB_TIMER_GLOBAL_WAIT_STUBS_HALF_PREPARE)
                    return

            for _floorNo in C_FD.datas.keys():
                if not gameengine.getGlobalBase('CubeStub%d' % _floorNo, reportErr=False):
                    LOG_INFO('start waiting: waiting for CubeStub stub', _floorNo)
                    self.pyAddTimer(0.1, 0, gametimer.BASESTUB_TIMER_GLOBAL_WAIT_STUBS_HALF_PREPARE)
                    return

            LOG_INFO('starting: all baseapp finished creating stubs')
            self.pyAddTimer(0.1, 0, gametimer.BASESTUB_TIMER_GLOBAL_STUBS_HALF_PREPARE)

        elif userArg == gametimer.BASESTUB_TIMER_GLOBAL_STUBS_HALF_PREPARE:
            # 所有stub都创建完成，执行doNext
            idx = formula.fetchStubIndex()

            gameglobal.localLoginStub.doNext()
            gameglobal.localAdminStub.doNext()
            gameglobal.localAuctionStub.doNext()
            gameglobal.localLeaseStub.doNext()
            gameglobal.localOrderStub.doNext()

            if gameglobal.isBootstrap:
                for lineType in gameconst.lineStubMap().keys():
                    stub = gameengine.getLineStub(lineType)
                    stub.doNext()

                for stubName in gameconst.GLOBAL_BASE_STUB_ARCHIVE:
                    gameengine.getGlobalBase(stubName).doNext()

                for stubName in gameconst.GLOBAL_BASE_STUB_UNARCHIVE:
                    gameengine.getGlobalBase(stubName).doNext()

                for i in range(gameconst.TEAMSTUB_CONF_NUM):
                    stubName = gameconst.GLOBAL_BASE_STUB_TEAMSTUB + str(i)
                    stub = gameengine.getGlobalBase(stubName)
                    stub.doNext()

                for i in range(gameconst.RAIDSTUB_CONFIG_NUM):
                    stubName = gameconst.GLOBAL_BASE_STUB_RAIDSTUB + str(i)
                    stub = gameengine.getGlobalBase(stubName)
                    stub.doNext()

                for i in range(gameconst.STATISTICSTUB_CONFIG_NUM):
                    stubName = gameconst.GLOBAL_BASE_STUB_STATISTICSTUB + str(i)
                    stub = gameengine.getGlobalBase(stubName)
                    stub.doNext()

                for dungeonNo, dVal in DDL.datas.items():

                    enterType = dVal['enterType']
                    dungeonType = dVal['type']

                    if dungeonType not in gameconst.DungeonSpaceTypeEnum.COLL_DUNGEON:
                        LOG_INFO("BaseStub::BASESTUB_TIMER_GLOBAL_STUBS_HALF_PREPARE:: skip dungeonNo in gamePlay table: ",
                                 dungeonNo, dungeonType)
                        continue

                    if dungeonType == gameconst.DungeonSpaceTypeEnum.UNKNOWN \
                            or enterType == gameconst.DungeonEnterTypeEnum.UNKNOWN:
                        continue

                    if enterType in gameconst.DungeonEnterTypeEnum.COLL_ALL:
                        stub = gameengine.getDungeonStubByDungeonNo(dungeonNo, enterType)
                        stub.doNext()
                        continue

                    if enterType == gameconst.DungeonEnterTypeEnum.BOTH:
                        for enterType in gameconst.DungeonEnterTypeEnum.COLL_BOTH:
                            stub = gameengine.getDungeonStubByDungeonNo(dungeonNo, enterType)
                            stub.doNext()
                            continue

                for _floorNo in WL_FD.datas.keys():
                    gameengine.getGlobalBase('WonderLandStub%d' % _floorNo).doNext()
                    
                for _floorNo in AB_FD.datas.keys():
                    gameengine.getGlobalBase('AbyssStub%d' % _floorNo).doNext()

                for _floorNo in C_FD.datas.keys():
                    gameengine.getGlobalBase('CubeStub%d' % _floorNo).doNext()

                gameengine.getGlobalBase('SiegeWarSpaceStub').doNext()

            LOG_INFO('starting: all stubs doNext')

            self.pyAddTimer(0.1, 0, gametimer.BASESTUB_TIMER_GLOBAL_STUBS_FULL_PREPARE)

        elif userArg == gametimer.BASESTUB_TIMER_GLOBAL_STUBS_FULL_PREPARE:
            if self.preparingEntTypes:
                LOG_INFO('still wating for fullPrepare', self.preparingEntTypes)
                self.pyAddTimer(0.5, 0, gametimer.BASESTUB_TIMER_GLOBAL_STUBS_FULL_PREPARE)
                return

            gameengine.getFirstBaseApp().setBaseAppLockState(self, gameconst.BASEAPP_STATE_LOCK_WAIT_FULL_PREPARE)
            #self.pyAddTimer(0.1, 0, gametimer.BASESTUB_TIMER_CHECK_LINE_READY)

        elif userArg == gametimer.BASESTUB_TIMER_CHECK_LINE_READY:
            # check world line ready
            if gameglobal.isBootstrap:
                for lineType, lineCfg in gameconst.lineStubMap().items():
                    stubName = lineCfg['stubName']
                    ready = self.lineReady.get(lineType, False)
                    if not ready:
                        LOG_INFO('start waiting: waiting for line space ready', stubName, lineType)
                        gameengine.getLineStub(lineType).checkAllLineSpaceReady(self, 'onLineReady', ())
                        self.pyAddTimer(0.1, 0, gametimer.BASESTUB_TIMER_CHECK_LINE_READY)
                        return

            if gameglobal.isBootstrap:
                import gmCommand
                import gmGroup
                import gmAdmin
                agent = gmCommand.GMAgent(gmAdmin.DUMMY_SU, '', None, gmGroup.MANAGER_GROUP_GOD)
                gmCommand.doCommandInside(agent, "$hotreload")

            gameglobal.localBaseApp.readhotfix()

            LOG_INFO('starting: line space ready', self.lineReady)

            if not gameconfig.waitEntityLoading():
                gameengine.setGlobalData(gameconst.GLOBALDATA_KEY_BASEAPP_READY, KBEngine.getComponentGroupOrder())

            self.pyAddTimer(0.1, 0, gametimer.BASESTUB_TIMER_CREATE_LINE_SPACE_ENTITIES)

        elif userArg == gametimer.BASESTUB_TIMER_CREATE_LINE_SPACE_ENTITIES:
            ready = self.isLineEntityReady()
            if not ready:
                LOG_INFO('start waiting: waiting for entities ready', ready.extra)
                self.pyAddTimer(1, 0, gametimer.BASESTUB_TIMER_CREATE_LINE_SPACE_ENTITIES)
                return

            LOG_INFO('starting: line entities ready')

            def _func(*args):
                LOG_DBG('set server start:', args)

            gamesql.setServerStateInfo('server_start_time', utils.curTS(), _func)
            gameengine.setGlobalData(gameconst.GLOBALDATA_KEY_BASEAPP_READY, KBEngine.getComponentGroupOrder())
            self.pyAddTimer(1, 0, gametimer.BASESTUB_TIMER_CREATE_WORLD_REFRESH_ENTITIES)

        elif userArg == gametimer.BASESTUB_TIMER_CREATE_WORLD_REFRESH_ENTITIES:
            if gameglobal.isBootstrap:
                gameengine.getGlobalBase('WorldRefreshEntityStub').loadGroupEntities()

            self.pyAddTimer(1, 0, gametimer.BASESTUB_TIMER_WAIT_WORLD_REFRESH_ENTITIES_READY)
        elif userArg == gametimer.BASESTUB_TIMER_WAIT_WORLD_REFRESH_ENTITIES_READY:
            if gameglobal.isBootstrap:
                ready = self.isWorldRefreshEntityReady()
                if not ready:
                   LOG_INFO('start waiting: waiting for world refresh entities ready', ready.extra)
                   gameengine.getGlobalBase('WorldRefreshEntityStub').checkAllGroupReady(self, 'onWorldRefreshEntityReady', ())
                   self.pyAddTimer(1, 0, gametimer.BASESTUB_TIMER_WAIT_WORLD_REFRESH_ENTITIES_READY)
                   return

            LOG_INFO('starting: world refresh entities ready')
            self.pyAddTimer(1, 0, gametimer.BASESTUB_TIMER_GAME_READY)

        elif userArg == gametimer.BASESTUB_TIMER_GAME_READY:
            if not gameglobal.isRelivedBaseapp and len(gameglobal.readyBaseappOrder) != gameconfig.baseAppCount():
                LOG_INFO('start waiting: waitting for all baseapps ready', gameglobal.isRelivedBaseapp, gameglobal.readyBaseappOrder)
                self.pyAddTimer(1, 0, gametimer.BASESTUB_TIMER_GAME_READY)
                return

            LOG_WARN('starting: all baseapp ready, set game ready')
            if gameglobal.isBootstrap:
                gameengine.setGlobalData(gameconst.GLOBALDATA_KEY_GAME_READY, True)
                import gmCommand
                import gmGroup
                import gmAdmin
                agent = gmCommand.GMAgent(gmAdmin.DUMMY_SU, '', None, gmGroup.MANAGER_GROUP_GOD)
                gmCommand.doCommandInside(agent, "$setcachecfg interfaceEnableLogin 1")
                gameengine.getGlobalBase('PlayerStub').syncOnlineNumToQueueServer()

    def _onServerOpenTime(self, ok, data):
        LOG_INFO("onServerOpenTime", ok, data)

    def _onServerOpenState(self, ok, data):
        LOG_INFO("onServerOpenState", ok, data)

    def createLocalStubs(self):
        idx = formula.fetchStubIndex()
        _createFunc = lambda name, props: gamebase.createGlobal(name, props, gameengine.buildIndexStubName(name, idx))
        gameglobal.localLoginStub = _createFunc('LoginStub', {'globalIdx': idx})
        gameglobal.localAdminStub = _createFunc('AdminStub', {'globalIdx': idx})
        gameglobal.localAuctionStub = _createFunc('AuctionStub', {'globalIdx':idx})
        gameglobal.localLeaseStub = _createFunc('LeaseStub', {'globalIdx':idx})
        gameglobal.localOrderStub = _createFunc('OrderStub', {'globalIdx':idx})
        gameglobal.localLoginStub.accountNumCounter.setSum(self, self.accountNum)

        self.localStubCreated = True

    def onLineReady(self, lineType, isReady):
        self.lineReady[lineType] = isReady

    def onLineEntityReady(self, spaceNo):
        lineType = formula.parseLineType(spaceNo)
        self.lineEntityReadyNum[lineType] = self.lineEntityReadyNum.get(lineType, 0) + 1
        LOG_DBG('onLineEntityReady:: lineType: {}, READY {} / {}'.format(
            lineType, self.lineEntityReadyNum.get(lineType, 0), utils.fetchLineMaxNumber(lineType)))

    def isLineEntityReady(self):
        for mapId, lineCfg in gameconst.lineStubMap().items():
            if not lineCfg.get('createAtStart', True):
                continue

            needNum = utils.fetchLineMaxNumber(mapId)

            readyNum = self.lineEntityReadyNum.get(mapId, 0)
            if readyNum < needNum:
                return gameclass.ResultBool(False, mapId)

        return gameclass.ResultBool(True, 0)

    def onWorldRefreshEntityReady(self, groupId, isReady):
        self.worldRefreshEntityReady[groupId] = isReady

    def isWorldRefreshEntityReady(self):
        '''
        for groupId, groupCfg in WMR_ERG.datas.items():
            isReady = self.worldRefreshEntityReady.get(groupId, False)
            if not isReady:
                return gameclass.ResultBool(False, groupId)
        '''
        return gameclass.ResultBool(True, 0)

    def addInitProcedure(self, name):
        LOG_INFO('start init', name)
        self.initProcedures[name] = 1

    def onInitProcedureDone(self, key):
        LOG_INFO('init done:', key)
        self.initProcedures.pop(key, None)

    def createGlobalStubs(self):
        baseApps = gameengine.chooseGoodBaseApp()
        for stubName in gameconst.GLOBAL_BASE_STUB_ARCHIVE:
            random.choice(baseApps).createArchiveStub(stubName, {}, '')

        for stubName in gameconst.GLOBAL_BASE_STUB_UNARCHIVE:
            random.choice(baseApps).createUnarchiveStub(stubName, {}, '')

        for i in range(gameconst.TEAMSTUB_CONF_NUM):
            stubName = gameconst.GLOBAL_BASE_STUB_TEAMSTUB + str(i)
            random.choice(baseApps).createUnarchiveStub(gameconst.GLOBAL_BASE_STUB_TEAMSTUB, {}, stubName)

        for i in range(gameconst.RAIDSTUB_CONFIG_NUM):
            stubName = gameconst.GLOBAL_BASE_STUB_RAIDSTUB + str(i)
            random.choice(baseApps).createUnarchiveStub(gameconst.GLOBAL_BASE_STUB_RAIDSTUB, {}, stubName)

        for i in range(gameconst.STATISTICSTUB_CONFIG_NUM):
            stubName = gameconst.GLOBAL_BASE_STUB_STATISTICSTUB + str(i)
            random.choice(baseApps).createUnarchiveStub(gameconst.GLOBAL_BASE_STUB_STATISTICSTUB, {}, stubName)

        # 每个地图一个stub,对应下面会创建 n个支线space
        for lineType, stubDic in gameconst.lineStubMap().items():
            random.choice(baseApps).createUnarchiveStub(stubDic['stubName'], {'lineType':lineType}, gameengine.buildLineStubName(lineType))

        # 每个副本地图一个stub,下面创建多个 副本space,用到才创建
        for dungeonNo, stubPrm in DDL.datas.items():
            dungeonSpaceType = stubPrm.get('type', 0)
            dungeonEnterType = stubPrm.get('enterType', 0)

            if dungeonSpaceType not in gameconst.DungeonSpaceTypeEnum.COLL_DUNGEON:
                LOG_INFO("BaseStub::_createGlobalStubs:: skip dungeonNo in gamePlay table: ",
                         dungeonNo, dungeonSpaceType)
                continue

            hasSpace = False
            if gameconst.DungeonTypeJudge.isTeamDungeon(dungeonSpaceType, dungeonEnterType):
                globalName = formula.fetchDungeonStubGlobalName(dungeonNo, gameconst.DungeonEnterTypeEnum.TEAM)
                random.choice(baseApps).createUnarchiveStub(
                    'TeamDungeonStub', {'dungeonNo': dungeonNo}, globalName, )
                hasSpace = True

            if gameconst.DungeonTypeJudge.isSingleDungeon(dungeonSpaceType, dungeonEnterType):
                globalName = formula.fetchDungeonStubGlobalName(dungeonNo, gameconst.DungeonEnterTypeEnum.SINGLE)
                random.choice(baseApps).createUnarchiveStub(
                    'SingleDungeonStub', {'dungeonNo': dungeonNo}, globalName, )
                hasSpace = True

            if gameconst.DungeonTypeJudge.isRaidDungeon(dungeonSpaceType, dungeonEnterType):
                globalName = formula.fetchDungeonStubGlobalName(dungeonNo, gameconst.DungeonEnterTypeEnum.RAID)
                random.choice(baseApps).createUnarchiveStub(
                    'RaidDungeonStub', {'dungeonNo': dungeonNo}, globalName, )
                hasSpace = True

            # 公会boss副本
            if gameconst.DungeonTypeJudge.isGuildBossDungeon(dungeonSpaceType, dungeonEnterType):
                globalName = formula.fetchDungeonStubGlobalName(dungeonNo, gameconst.DungeonEnterTypeEnum.GUILD)
                random.choice(baseApps).createUnarchiveStub(
                    'GuildBossDungeonStub', {'dungeonNo': dungeonNo}, globalName, )
                hasSpace = True

            if not hasSpace:
                LOG_WARN('_createGlobalStubs:: UN-KNOWN DungeonTypeJudge', dungeonNo, dungeonSpaceType, dungeonEnterType)
                if not hasattr(self, '_skipInitDungeonStubs'):
                    self._skipInitDungeonStubs = []
                self._skipInitDungeonStubs.append(dungeonNo)

        # 每层单独一个stub,一个space
        for _floorNo in WL_FD.datas.keys():
            random.choice(baseApps).createUnarchiveStub('WonderLandStub', {'floor': _floorNo}, 'WonderLandStub%d' % _floorNo)

        for _floorNo in AB_FD.datas.keys():
            random.choice(baseApps).createUnarchiveStub('AbyssStub', {'floor': _floorNo}, 'AbyssStub%d' % _floorNo)

        # 每层单独一个stub,一个space
        for _floorNo in C_FD.datas.keys():
            random.choice(baseApps).createUnarchiveStub('CubeStub', {'cubeNo': _floorNo}, 'CubeStub%d' % _floorNo)

        #todo读策划表
        random.choice(baseApps).createUnarchiveStub('SiegeWarSpaceStub', {}, 'SiegeWarSpaceStub')

    def fullPrepare(self, entType):
        LOG_INFO(entType, 'fullPrepare')
        if entType in self.preparingEntTypes:
            self.preparingEntTypes.remove(entType)

    def addInitedCellapp(self, groupOrder):
        if groupOrder in self.initedCellapps:
            return
        LOG_INFO('addInitedCellapp', groupOrder)
        self.initedCellapps.append(groupOrder)
        self.initedCellapps.sort()

    def createLeaderBoardStub(self):
        gamesql.loadLeaderBoardStubInfos(self._onGetLeaderBoardStubInfos)

    def _onGetLeaderBoardStubInfos(self, ret, num, insertId, err):
        LOG_INFO('LeaderBoardAvatarStub _onGetLeaderBoardStubInfos')
        if err:
            LOG_ERR('LeaderBoardAvatarStub _onGetLeaderBoardStubInfos', err)
            return

        _dic = {k: None for k in gameconst.LeaderBoardType.ALL_KEYS}

        for _lbType, _dbid in ret:
            _dbid = int(_dbid)
            _lbType = int(_lbType)

            _dic[_lbType] = _dbid

        for _lbType, _dbid in _dic.items():
            if _dbid is None:
                _props = {
                    'leaderBoardType': _lbType,
                }
                KBEngine.createEntityAnywhere(
                    'LeaderBoardStub',
                    _props,
                    self._onCreateLeaderBoardStub,
                )

            else:
                KBEngine.createEntityAnywhereFromDBID(
                    'LeaderBoardStub',
                    _dbid,
                    self._onCreateLeaderBoardStubFromDBID,
                )

    def _onCreateLeaderBoardStubFromDBID(self, ent, dbid, wasActive):
        pass

    def _onCreateLeaderBoardStub(self, lbStub):
        lbStub.onFirstCreate()

    def _onGetAllServerResult(self, httpCode, data, headers, success, *args):
        if not (httpCode == 200 and success):
            LOG_ERR('_onGetAllServerResult', httpCode)
            self.pyAddTimer(0.1, 0, gametimer.GET_ALL_SERVER_INFO)
            return

        _datas = json.loads(data)
        LOG_INFO('all server data', _datas)
        _dic = {}
        for _data in _datas['servers']:
            _dic[_data['id']] = _data

        _curServerInfo = _dic.get(gameconfig.serverId(), {})
        _alias = _curServerInfo.get('alias', '')
        _serverName = _curServerInfo.get('server_name', '')

        gameengine.callAllApps(
            'gameengine.setMapleServerInfo',
            (_dic, _alias, _serverName))

        self.setMapleServerInfo(json.dumps(_dic))
        self.pyAddTimer(0.1, 0, gametimer.WAIT_GET_ALL_SERVER_INFO)

