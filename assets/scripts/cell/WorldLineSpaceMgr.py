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

class WorldLineSpaceMgr(iCell.ICell, iTimer.ITimer, iSpaceMgr.ISpaceMgr):
    def __init__(self):
        INFO_MSG('WorldLineSpaceMgr init', self.spaceNo, self.spaceID)
        if formula.isWolrdBossSpace(self.spaceNo):
            self._initCreateBoss(0)
            self._initWorldBossGid()

            self.setSceneStates([
                gameconst.WorldLineSceneState.LEI_JI
            ])

    def _initWorldBossGid(self):
        _mapId = formula.getMapId(self.spaceNo)
        _dunData = utils.getDunStructureModuleData(_mapId)
        _bossDatas = _dunData['InitEntities']['Monster']
        for _data in _bossDatas.values():
            _monsterId = _data['EntityID']
            _creepData = creep_base.datas[_monsterId]
            if _creepData['type'] != gameconst.MonsterType.ADVANCE:
                continue

            for i in utils.generateGameEntityId(_data['ID'], 1):
                self.worldBossGid = i #10360001xxx
            break

    def _initCreateBoss(self, times):
        _stub = gameengine.getGlobalBase('WorldBossStub')
        if not _stub:
            self._callback(1, '_initCreateBoss', (times + 1,), gametimer.TIMER_TAG_INIT_CREATE_BOSS)
            if times > 60:
                ERROR_MSG('WorldBossStub create boss retry meet max times', times)
            return

        _stub.getBossCreateTime(self.spaceNo, self)

    def doCreateWorldBoss(self):
        self._createWorldBoss()

    def _createWorldBoss(self):
        _entityProps = []
        utils.loadLineReadyEntities(self.spaceNo, [self.worldBossGid], _entityProps)
        for _, _, _className, _, _pos, _dir, _params, _ in _entityProps:
            _params['spaceMgrId'] = self.id

            self.getCurrentSpace().createCellLocally(_className, _pos, _dir, _params)

        self.setSceneStates([
            gameconst.WorldLineSceneState.THUNDER
        ])

    def onGetCreateBossTime(self, _createTime):
        _now = utils.getNow()
        if _createTime <= _now:
            self._createWorldBoss()
        else:
            gameengine.getGlobalBase('WorldBossStub').addCreateWorldBossTimer(
                self.spaceNo, _createTime
            )

    def onTimer(self, tid, userArg):
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        else:
            self._onTimer(tid, userArg)

    def setSceneStates(self, states):
        _state = 0
        for i in states:
            _state = _state | (1 << i)

        self.worldLineSceneState = _state
        DEBUG_MSG('setSceneStates', self.spaceNo, states, self.worldLineSceneState)
        self.syncPlayer(lambda box: box.client.onSceneState(self.worldLineSceneState))

    def onPlayerEnter(self, eid):
        super(WorldLineSpaceMgr, self).onPlayerEnter(eid)
        if not formula.isWolrdBossSpace(self.spaceNo):
            return

        ent = self.getEntityById(eid)
        DEBUG_MSG('onPlayerEnter', self.spaceNo, self.worldLineSceneState)
        ent and ent.client.onSceneState(self.worldLineSceneState)

    def onPlayerRelogin(self, player, gbId):
        if not formula.isWolrdBossSpace(self.spaceNo):
            return

        DEBUG_MSG('onPlayerEnter', self.spaceNo, self.worldLineSceneState)
        player.client.onSceneState(self.worldLineSceneState)

    def hasSceneState(self, st):
        return (self.worldLineSceneState & (1 << st)) > 0

    def onWorldBossDead(self, refreshTime):
        DEBUG_MSG('onWorldBossDead', self.spaceNo, refreshTime)
        _nextCreateTime = utils.getNow() + refreshTime
        gameengine.getGlobalBase('WorldBossStub').onWorldBossDeadAddTimer(self.spaceNo, _nextCreateTime)

        _delay = CONST.datas['messageDelayAfterDeath']['value']
        self._callback(_delay, 'setSceneStates', ([gameconst.WorldLineSceneState.LEI_JI],), gametimer.TIMER_TAG_BOSS_DEAD_SET_SCENE_STATE)


