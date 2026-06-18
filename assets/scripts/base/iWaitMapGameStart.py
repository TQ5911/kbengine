# -*- coding: utf-8 -*-
import formula
import KBEngine
import json
import random
import gameclass
from KBEDebug import *
import gametimer
import gameengine
import gameconfig
import gameconst
import gameglobal
import gamesql
import utils
import gamebase
import redisUtils


class IWaitMapGameStart(object):

    def __init__(self):
        super(IWaitMapGameStart, self).__init__()
        self.waitingCellapps = []
        self.waitMapPreparingEntTypes = []

    def waitMapAddInitedCellapp(self, groupOrder):
        if groupOrder in self.waitingCellapps:
            return
        LOG_INFO('addWaitingCellapp', groupOrder)
        self.waitingCellapps.append(groupOrder)
        self.waitingCellapps.sort()

    def waitMapFullPrepare(self, entType):
        LOG_INFO(entType, 'waitMapFullPrepare')
        if entType in self.waitMapPreparingEntTypes:
            self.waitMapPreparingEntTypes.remove(entType)
        else:
            self.waitMapPreparingEntTypes.append(entType)

    def onWaitMapTimer(self, tid, userArg):
        if userArg == gametimer.WAITMAP_TIMER_START:
            cellapps = self.waitingCellapps
            if len(cellapps) != gameconfig.cellAppCount():
                LOG_INFO('start waiting: waiting for cellapps start: %s/%s' % (cellapps, gameconfig.cellAppCount()))
                self.pyAddTimer(1, 0, gametimer.WAITMAP_TIMER_START)
                return

            comps = KBEngine.getComponents()
            if len(comps['baseapps']) + 1 != gameconfig.baseAppCount():
                LOG_INFO('start waiting: waiting for baseapps start: %s/%s' % (
                len(comps['baseapps']) + 1, gameconfig.baseAppCount()))
                self.pyAddTimer(1, 0, gametimer.WAITMAP_TIMER_START)
                return

            LOG_INFO('starting: components ready')
            self.pyAddTimer(1, 0, gametimer.WAITMAP_TIMER_CHECK_COMPONENTS)

        elif userArg == gametimer.WAITMAP_TIMER_CHECK_COMPONENTS:
            baseAppCnt = gameconfig.baseAppCount()
            howManyBaseApp = gameengine.howManyBaseApps()

            if howManyBaseApp < baseAppCnt:
                LOG_INFO('start waiting: waiting for creating all BaseApp Entity: %s/%s' % (howManyBaseApp, baseAppCnt))
                self.pyAddTimer(1, 0, gametimer.WAITMAP_TIMER_CHECK_COMPONENTS)
                return

            LOG_INFO('starting: successful to create all baseapps&cellapps, now create stubs')
            self.onGetAllBaseApps()
            self.createWaitMapLocalStubs()
            self.pyAddTimer(0.1, 0, gametimer.WAITMAP_TIMER_GET_ALL_SERVER_INFO)

        elif userArg == gametimer.WAITMAP_TIMER_GET_ALL_SERVER_INFO:
            _url = gameconfig.mapleAllServerUrl()
            if gameglobal.isBootstrap and _url:
                KBEngine.urlopenv2(_url, self._onWaitMapGetAllServerResult, method='GET')
                return

            self.pyAddTimer(0.1, 0, gametimer.WAITMAP_TIMER_WAIT_GET_ALL_SERVER_INFO)

        elif userArg == gametimer.WAITMAP_TIMER_WAIT_GET_ALL_SERVER_INFO:
            if not gameglobal.mapleServerInfo:
                LOG_WARN('still waiting for get mapleServerInfo')
                self.pyAddTimer(0.1, 0, gametimer.WAITMAP_TIMER_WAIT_GET_ALL_SERVER_INFO)
                return

            if gameglobal.mapleServerInfo[gameconfig.serverId()]['start_time'] != gameconfig.serverOpenTime():
                LOG_ERR(f'server startTime not match: {gameglobal.mapleServerInfo[gameconfig.serverId()]}, {gameconfig.serverOpenTime()}')
                self.pyAddTimer(1, 0, gametimer.WAITMAP_TIMER_WAIT_GET_ALL_SERVER_INFO)
                return
            
            if gameglobal.isBootstrap:
                key = gameconst.RedisKey.SERVER_OPEN_TIME + str(gameconfig.serverId())
                redisUtils.RedisUtils.cmdSet(key, str(gameconfig.serverOpenTime()), self._onWaitMapServerOpenTime)

                key = gameconst.RedisKey.SERVER_OPEN_STATE + str(gameconfig.serverId())
                redisUtils.RedisUtils.cmdSet(key, str(gameconfig.permitLogin()), self._onWaitMapServerOpenState)

            self.pyAddTimer(0.1, 0, gametimer.WAITMAP_TIMER_WAIT_LEADER_BOARD_STUB_READY)

        elif userArg == gametimer.WAITMAP_TIMER_WAIT_LEADER_BOARD_STUB_READY:
            if gameglobal.isBootstrap:
                self.createWaitMapGlobalStubs()

            self.pyAddTimer(0.1, 0, gametimer.WAITMAP_TIMER_WAIT_GLOBAL_STUBS_HALF_PREPARE)

        elif userArg == gametimer.WAITMAP_TIMER_WAIT_GLOBAL_STUBS_HALF_PREPARE:
            if not gameengine.getGlobalBase('WaitMapSpaceStub', reportErr=False):
                LOG_INFO('start waiting: still waiting for WaitMapSpaceStub')
                self.pyAddTimer(0.1, 0, gametimer.WAITMAP_TIMER_WAIT_GLOBAL_STUBS_HALF_PREPARE)
                return
            LOG_INFO('starting: waitmap server stubs ready')
            self.pyAddTimer(0.1, 0, gametimer.WAITMAP_TIMER_GLOBAL_STUBS_HALF_PREPARE)

        elif userArg == gametimer.WAITMAP_TIMER_GLOBAL_STUBS_HALF_PREPARE:
            gameglobal.localAdminStub.doNext()
            gameengine.getGlobalBase('WaitMapSpaceStub').doNext()
            LOG_INFO('starting: all stubs doNext')
            self.pyAddTimer(0.1, 0, gametimer.WAITMAP_TIMER_GLOBAL_STUBS_FULL_PREPARE)

        elif userArg == gametimer.WAITMAP_TIMER_GLOBAL_STUBS_FULL_PREPARE:
            if self.waitMapPreparingEntTypes:
                LOG_INFO('still wating for fullPrepare', self.waitMapPreparingEntTypes)
                self.pyAddTimer(0.5, 0, gametimer.WAITMAP_TIMER_GLOBAL_STUBS_FULL_PREPARE)
                return

            gameengine.getFirstBaseApp().setBaseAppLockState(self, gameconst.BASEAPP_STATE_LOCK_WAIT_FULL_PREPARE)

        elif userArg == gametimer.WAITMAP_TIMER_SET_SERVER_STATE:
            LOG_INFO('starting: line entities ready')
            if gameglobal.isBootstrap:
                import gmCommand
                import gmGroup
                import gmAdmin
                agent = gmCommand.GMAgent(gmAdmin.DUMMY_SU, '', None, gmGroup.MANAGER_GROUP_GOD)
                gmCommand.doCommandInside(agent, "$hotreload")
            gameglobal.localBaseApp.readhotfix()

            if not gameconfig.waitEntityLoading():
                gameengine.setGlobalData(gameconst.GLOBALDATA_KEY_BASEAPP_READY, KBEngine.getComponentGroupOrder())

            def _func(*args):
                LOG_DBG('set server start:', args)
            gamesql.setServerStateInfo('server_start_time', utils.curTS(), _func)
            gameengine.setGlobalData(gameconst.GLOBALDATA_KEY_BASEAPP_READY, KBEngine.getComponentGroupOrder())

            self.pyAddTimer(1, 0, gametimer.WAITMAP_TIMER_GAME_READY)

        elif userArg == gametimer.WAITMAP_TIMER_GAME_READY:
            if not gameglobal.isRelivedBaseapp and len(gameglobal.readyBaseappOrder) != gameconfig.baseAppCount():
                LOG_INFO('start waiting: waitting for all baseapps ready', gameglobal.isRelivedBaseapp, gameglobal.readyBaseappOrder)
                self.pyAddTimer(1, 0, gametimer.WAITMAP_TIMER_GAME_READY)
                return

            LOG_WARN('starting: all baseapp ready, set game ready')
            if gameglobal.isBootstrap:
                gameengine.setGlobalData(gameconst.GLOBALDATA_KEY_GAME_READY, True)
                import gmCommand
                import gmGroup
                import gmAdmin
                agent = gmCommand.GMAgent(gmAdmin.DUMMY_SU, '', None, gmGroup.MANAGER_GROUP_GOD)
                gmCommand.doCommandInside(agent, "$setcachecfg interfaceEnableLogin 1")

    def createWaitMapLocalStubs(self):
        idx = formula.fetchStubIndex()
        _createFunc = lambda name, props: gamebase.createGlobal(name, props, gameengine.buildIndexStubName(name, idx))
        gameglobal.localAdminStub = _createFunc('AdminStub', {'globalIdx': idx})

    def createWaitMapGlobalStubs(self):
        baseApps = gameengine.chooseGoodBaseApp()
        random.choice(baseApps).createUnarchiveStub('WaitMapSpaceStub', {}, '')

    def _onWaitMapGetAllServerResult(self, httpCode, data, headers, success, *args):
        if not (httpCode == 200 and success):
            LOG_ERR('_onWaitMapGetAllServerResult', httpCode)
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
        self.pyAddTimer(0.1, 0, gametimer.WAITMAP_TIMER_WAIT_GET_ALL_SERVER_INFO)

    def _onWaitMapServerOpenTime(self, ok, data):
        LOG_INFO("_onWaitMapServerOpenTime", ok, data)

    def _onWaitMapServerOpenState(self, ok, data):
        LOG_INFO("_onWaitMapServerOpenState", ok, data)
