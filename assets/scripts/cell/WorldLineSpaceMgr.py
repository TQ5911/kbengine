# coding:utf-8
from KBEDebug import *
import iSpaceMgr
import iCell
import gametimer
import utils
import gameengine
import gameconst
import iTimer
import formula
import creep_base
import const_const as CONST
import gameglobal
import iMineWarSpaceMgr
import branchData_set as BDS

class WorldLineSpaceMgr(iCell.ICell, iTimer.ITimer, iSpaceMgr.ISpaceMgr, iMineWarSpaceMgr.IMineWarSpaceMgr):
    def __init__(self):
        LOG_INFO('WorldLineSpaceMgr init', self.spaceNo, self.spaceID)

        iMineWarSpaceMgr.IMineWarSpaceMgr.__init__(self)
        iSpaceMgr.ISpaceMgr.__init__(self)
        if formula.inWolrdBossScene(self.spaceNo):
            # 初始化世界boss 由 ITimerEntityRefresh 处理
            if CONST.datas['bossRefreshSystem']['value'] != gameconst.WorldBossRefreshType.TIMED_INTERVALS_TIMER:
                self._initCreateBoss(0)

            self._initWorldBossGid()
            self.setSceneStates([
                gameconst.WorldLineSceneState.LEI_JI
            ])
        stubName = 'WorldLineStub{}'.format(formula.fetchMapId(self.spaceNo))
        gameengine.getGlobalBase(stubName).onSpaceMgrReady(self.spaceNo, self)
        LOG_INFO('WorldLineSpaceMgr init done', self.spaceNo, self.spaceID, stubName)

        # 矿战另外处理
        if not formula.inMineWarScene(self.spaceNo):
            self.addTimerCB(0.1, '_loadEntities', (), gametimer.TIMER_TAG_WORLD_LINE_LOAD_ENTITIES)
        self.addDatetimeTimerTick()

        #每分钟统计一次当前line活跃人数(5分钟内进入过战斗状态)
        self.pyAddTimer(1, 60, gametimer.STATISTIC_FIGHTING_COUNT)
        self.fightingPlayersCnt = 0

    def _loadEntities(self):
        _space = gameglobal.localSpaceIDMap[self.spaceID]
        _space.doLoadEntities(self.id)

    def _initWorldBossGid(self):
        _mapId = formula.fetchMapId(self.spaceNo)
        _dunData = utils.getDunStructModData(_mapId)
        _bossDatas = _dunData['InitEntities']['Monster']
        for _data in _bossDatas.values():
            _monsterId = _data['EntityID']
            _creepData = creep_base.datas[_monsterId]
            if _creepData['type'] != gameconst.MonsterType.ADVANCE:
                continue

            for i in utils.genGameEntityId(_data['ID'], 1):
                self.worldBossGid = i #10360001xxx
            break

    def _initCreateBoss(self, times):
        _stub = gameengine.getGlobalBase('WorldBossStub')
        if not _stub:
            self.addTimerCB(1, '_initCreateBoss', (times + 1,), gametimer.TIMER_TAG_INIT_CREATE_BOSS)
            if times > 60:
                LOG_ERR('WorldBossStub create boss retry meet max times', times)
            return

        _stub.getBossCreateTime(self.spaceNo, self)

    def doCreateWorldBoss(self):
        self._createWorldBoss()

    def _createWorldBoss(self):
        _entityProps = []
        utils.loadLineReadyEntities(self.spaceNo, [self.worldBossGid], _entityProps, True)
        for _, _, _className, _, _pos, _dir, _params, _ in _entityProps:
            _params['spaceMgrId'] = self.id

            self.getCurrentSpace().createCellLocally(_className, _pos, _dir, _params)

        if self.afterDeadSetSceneTimer:
            self.cancelTimerCB(self.afterDeadSetSceneTimer, gametimer.TIMER_TAG_BOSS_DEAD_SET_SCENE_STATE)
            self.afterDeadSetSceneTimer = 0

        self.setSceneStates([
            gameconst.WorldLineSceneState.THUNDER
        ])

    def onGetCreateBossTime(self, _createTime):
        _now = utils.curTS()
        if _createTime <= _now:
            self._createWorldBoss()
        else:
            gameengine.getGlobalBase('WorldBossStub').addCreateWorldBossTimer(
                self.spaceNo, _createTime
            )

    def onTimer(self, tid, userArg):
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        elif userArg == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()
        elif userArg == gametimer.STATISTIC_FIGHTING_COUNT:
            self._statisticFightingCount()
        elif userArg == gametimer.TIMER_MINE_WAR_SPACE_TICK:
            self._onMineWarSpaceTick()
        else:
            self._onTimer(tid, userArg)

    def setSceneStates(self, states):
        _state = 0
        for i in states:
            _state = _state | (1 << i)

        self.worldLineSceneState = _state
        LOG_DBG('setSceneStates', self.spaceNo, states, self.worldLineSceneState)
        self.syncPlayer(lambda box: box.onSceneStateChange(self.worldLineSceneState))

    def onPlayerEnter(self, eid):
        iSpaceMgr.ISpaceMgr.onPlayerEnter(self, eid)
        iMineWarSpaceMgr.IMineWarSpaceMgr.onPlayerEnter(self, eid)
        if not formula.inWolrdBossScene(self.spaceNo):
            return

        ent = self.getEntityById(eid)
        LOG_DBG('onPlayerEnter', self.spaceNo, self.worldLineSceneState)
        ent and ent.client.onSceneState(self.worldLineSceneState)

    def onPlayerLeave(self, gbId, playerId, box):
        iSpaceMgr.ISpaceMgr.onPlayerLeave(self, gbId, playerId, box)
        iMineWarSpaceMgr.IMineWarSpaceMgr.onPlayerLeave(self, gbId, playerId, box)

    def onPlayerRelogin(self, player, gbId):
        super().onPlayerRelogin(player, gbId)
        if not formula.inWolrdBossScene(self.spaceNo):
            return

        LOG_DBG('onPlayerEnter', self.spaceNo, self.worldLineSceneState)
        player.client.onSceneState(self.worldLineSceneState)

    def hasSceneState(self, st):
        return (self.worldLineSceneState & (1 << st)) > 0

    def onWorldBossDead(self, refreshTime):
        LOG_DBG('onWorldBossDead', self.spaceNo, refreshTime, CONST.datas['bossRefreshSystem']['value'])
        self.setSceneStates([gameconst.WorldLineSceneState.THUNDER])
        _delay = CONST.datas['messageDelayAfterDeath']['value']
        self.afterDeadSetSceneTimer = self.addTimerCB(
            _delay, 
            'setSceneStates', 
            ([gameconst.WorldLineSceneState.LEI_JI],), 
            gametimer.TIMER_TAG_BOSS_DEAD_SET_SCENE_STATE,
            'afterDeadSetSceneTimer'
        )

        # 不通知刷新了,由 ITimerEntityRefresh 控制下次刷新
        if CONST.datas['bossRefreshSystem']['value'] == gameconst.WorldBossRefreshType.TIMED_INTERVALS_TIMER:
            LOG_DBG('onWorldBossDead2', self.spaceNo, refreshTime)
            return

        self.onWorldBossRefresh(utils.curTS(), refreshTime, 0)

    def onWorldBossRefresh(self, _now, refreshTime, times):
        LOG_DBG('onWorldBossRefresh', self.spaceNo, _now, refreshTime, times)
        _stub = gameengine.getGlobalBase('WorldBossStub')
        if not _stub:
            self.addTimerCB(1, 'onWorldBossRefresh', (_now, refreshTime, times + 1,), gametimer.TIMER_TAG_REFRESH_CREATE_BOSS_TIMER)
            if times > 60:
                LOG_ERR('onWorldBossRefresh WorldBossStub create boss retry meet max times', times)
            return

        _nextCreateTime = _now + refreshTime
        _stub.onWorldBossDeadAddTimer(self.spaceNo, _nextCreateTime)

    def _statisticFightingCount(self):
        now = utils.curTS()
        lastCnt = self.fightingPlayersCnt
        self.fightingPlayersCnt = 0
        dt = BDS.datas["Branch_activePlayer"]["value"] * 60
        for pid in self.players:
            ent = KBEngine.entities.get(pid)
            if not ent:
                continue
            #5分钟内有进入过战斗视为"活跃用户"
            if now - ent.lastFightTime < dt:
                self.fightingPlayersCnt += 1

        if lastCnt != self.fightingPlayersCnt:
            stubName = 'WorldLineStub{}'.format(formula.fetchMapId(self.spaceNo))
            gameengine.getGlobalBase(stubName).onFightingPlayersCntSync(self.spaceNo, self.fightingPlayersCnt)
