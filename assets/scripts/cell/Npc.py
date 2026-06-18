# coding: utf-8
import KBEngine
from KBEDebug import *

import NPC_NPC as NPC_DATA
import creep_base

import iCell
import iTimer
import EventMgr
import iAICombatUnit
import iFubenSpace
import iGameEntity
import iEntityRefresh
import iClient
import iMonsterDungeon
import iRoute

import gameconst
import gametimer
import utils
import sMath
import formula

import Dialog_Dialog as DDD


class Npc(iAICombatUnit.IAICombatUnit, iTimer.ITimer, EventMgr.EventMgr, iGameEntity.IGameEntity,
          iEntityRefresh.IEntityRefresh, iClient.IClient, iFubenSpace.IFubenSpace, iMonsterDungeon.IMonsterDungeon,
          iRoute.IRoute):
    IsNpc = True
    IsCombatUnit = False

    # ------------------------------------------------------------------
    # INIT
    def __init__(self):
        iGameEntity.IGameEntity.__init__(self)
        iEntityRefresh.IEntityRefresh.__init__(self)

        if self.IsCombatUnit:
            self.initCNpc()
        else:
            self.initNpc()
        LOG_INFO('on create', self.spaceNo, self.position, self.npcId)

    def initNpc(self):
        if not self.level:
            self.level = gameconst.MIN_LEVEL
        elif self.level > utils.getMaxPlayerLevel():
            self.level = utils.getMaxPlayerLevel()

        if not self.name:
            self.name = NPC_DATA.datas.get(self.npcId, {}).get('name', '无名NPC')

        self.hp = self.fullHp
        self.mp = self.fullMp
        self.speed = float(creep_base.datas.get(self.creepbaseId, {}).get('baseSpeed', 3.0))

        self.isNameDisplay = NPC_DATA.datas[self.npcId].get('isNameDisplay', 1)
        self.isSelectable = NPC_DATA.datas[self.npcId].get('isSelectable', 1)

        self.baseDodge = 0

        self.bornPosition = tuple(self.position)

        if self.force == 0:
            self.force = gameconst.ForceTypeEnum.NPC

        self.initEntBornAction()

        spaceMgr = self.spaceMgr

        if formula.inDungeonScene(self.spaceNo) and spaceMgr:
            gid = utils.parseGidFromGameEntityId(self.gameEntityId)
            spaceMgr.addEntity(self.id, (str(self.fbEntityId), str(self.npcId),
                                         'gid_{}'.format(gid), self.__class__.__name__,))
            if self.isBoss:
                spaceMgr.setBossEntity(self.id)

        elif formula.inWonderLandScene(self.spaceNo):
            spaceMgr.addEntity(self.id, (str(self.npcId),
                                         self.__class__.__name__,))
        else:
            if spaceMgr:
                spaceMgr.addEntity(self.id, (str(self.npcId),
                                         self.__class__.__name__,))

        self.triggeredFlowControllerRestNumIncreased()
        # if not self.IsCombatUnit and self.belongFestivalLoadId:
        #     dataUtils.allFestivalStubDo('festivalEntityLoad', (self.belongFestivalLoadId, self))
        self.addListener('onBeat', self.id, 'onBeAttacked', ())
        self.triggerAIEvent(self.id, gameconst.AI_EVENT_ENTITY_BORN, ())
        self.setBornState(gameconst.BornStateEnum.move)

    def initCNpc(self):
        iAICombatUnit.IAICombatUnit.__init__(self)
        iGameEntity.IGameEntity.__init__(self)

    # ------------------------------------------------------------------

    def onEnterTrap(self, entity, rangeXZ, rangeY, controllerId, userArg):
        super().onEnterTrap(entity, rangeXZ, rangeY, controllerId, userArg)
        if userArg == gameconst.ESCORT_ROUTE_TRAP:
            self.onPlayerEnterEscortTrap(entity, rangeXZ, rangeY, controllerId)

    def getPathId(self):
        return NPC_DATA.datas[self.npcId].get('pathID', 0)

    def faceToPlayer(self, captainPos):
        direction = sMath.vector3WithoutY(captainPos - self.position)
        yaw = sMath.getYawFromDirection(direction)
        self.direction = (0.0, 0.0, yaw)
        return

    def setBornState(self, state):
        if self.bornState >= state:
            LOG_ERR('setBornState failed:', self.bornState, state)
            return

        self.bornState = state
        if state == gameconst.BornStateEnum.move:
            pathId = self.getPathId()
            if pathId:
                self.addTimerCB(1, 'setRoute', (pathId, True if self.aiController else False),
                               gametimer.TIMER_TAG_SET_ROUTE)
        elif state == gameconst.BornStateEnum.reMove:
            self.bornState = gameconst.BornStateEnum.move
        elif state == gameconst.BornStateEnum.afterDialog:
            self.stopThink()
            self.interruptRouting()
            self.removeMoveController()
            self.killCastingSkill(gameconst.EndCasting.ECEnumCaptureMonster)
            self.killChannelingSkill(gameconst.ChannelingBreak.BREAK_TP_CAPTURE)
        elif state == gameconst.BornStateEnum.normal:
            self.addTimerCB(0.5, 'startThink', (), gametimer.TIMER_TAG_START_THINK)

    @property
    def creepbaseId(self):
        return NPC_DATA.datas[self.npcId].get('creepID', 0)

    def initEntBornAction(self):
        self.otherClients.onBornAction()

    def setAI(self, aiName):
        # no combat NPC doesn't need AI Controller
        pass

    def onTimer(self, tid, userData):
        self._onTimerTrigger(tid, userData)
        if utils.isBelongTimerTag(userData):
            self._onTimerCallback(tid)

        elif userData == gametimer.COMBAT_UNIT_AI_THINK:
            self.aiController and self.aiTick()

        elif userData == gametimer.TIMER_CELL_DELAY_SAFE_DESTROY:
            self.onDelayTimerSafeDestroy()

        elif userData == gametimer.GUIDE_WALK_TIMER:
            self.onTimerGuideWalk()
        else:
            super().onTimer(tid, userData)

    def aiTick(self):
        self.aiController and self.aiController.tickOnce()

    def _addTrap(self):
        radii = self.getAlertDistance()
        if radii<=0:
            return
        self.hateTrapId = self.addProximity(radii, radii, gameconst.AGGRO_TRIGGER_TRAP)
        leaveAoiRange = self.getLeaveAlertDistance()
        self.addProximity(leaveAoiRange, 0.0, gameconst.AOI_EXIT_TRAP)

    def onBeAttacked(self, arg):
        attackerId = arg.triggerRoleId
        self.triggerAIEvent(self.id, gameconst.AI_EVENT_ON_BE_ATTACKED, (attackerId,))

    def _preSafeDestory(self):
        super()._preSafeDestory()
        if self.spaceMgr:
            self.spaceMgr.removeEntById(self.id)

    def onDead(self, killer, *args, **kwargs):
        super().onDead(killer)
        self.removeAllBuff()
        self.removeMoveController()
        self.destroySummonOnDead()

        if killer:
            self.allClients.onDead(killer.id)

        # 【【任务】副本编辑器中monsterID接入范围扩大为entityID】
        # killMonsterNum
        # 【【程序自主】【副本编辑器】服务流程编辑器怪物原型ID检测支持临时Entity(没有副本ID的Entity)】
        self.addDungeonKillCount()

        self.triggeredFlowControllerRestNumDec()

        self.delaySafeDestroy(3)

    def _checkValidEnt(self, ent):
        if not ent or ent.isDestroyed:
            LOG_WARN('NPC._checkValidEnt: invalid entity')
            return False

        if not ent.IsAvatar:
            LOG_WARN('NPC._checkValidEnt: not Avatar')
            return False

        if ent.spaceNo != self.spaceNo:
            LOG_WARN('NPC._checkValidEnt: not in same space')
            return False

        if sMath.distance2D(self.position, ent.position) > 30:
            LOG_WARN('NPC._checkValidEnt: too faraway')
            return False

        return True

    def doDialogEvent(self, exposed, dialogId):
        pass

    def onEntityRefresh(self):
        super().onEntityRefresh(self.spaceNo, self.posIndex)

    def onDisappearTimerEnded(self):
        super().onDisappearTimerEnded()

