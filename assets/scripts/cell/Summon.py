# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

import iCell
import SkillManager
import iTimer
import EventMgr
import iFubenSpace
import iMonsterGrp
import iMonsterDungeon
import iGameEntity
import iClient
import actionContext

import utils
import dataUtils
import aiController
import gametimer
import gameconst
import formula
import iAICombatUnit

import creep_base as CBD
import creep_bornState as CBSD


class Summon(iAICombatUnit.IAICombatUnit, iTimer.ITimer,
             EventMgr.EventMgr, iFubenSpace.IFubenSpace,
             iMonsterGrp.IMonsterGrp, iMonsterDungeon.IMonsterDungeon,
             iGameEntity.IGameEntity, iClient.IClient):
    IsSummon = True

    MOVE_METHOD_NAV = 1
    MOVE_METHOD_MOVE = 2

    def __init__(self):
        if not self.level:
            self.level = gameconst.MIN_LEVEL
        elif self.level > utils.getPlayerMaxLevel():
            self.level = utils.getPlayerMaxLevel()

        iAICombatUnit.IAICombatUnit.__init__(self)
        EventMgr.EventMgr.__init__(self)
        iGameEntity.IGameEntity.__init__(self)
        self.name = CBD.datas[self.summonId].get('name', '无名怪')
        hostEnt = self.getHost()
        if not self.hostId or (hostEnt and not hostEnt.IsAvatar and not hostEnt.isBot()):
            self.isWitnessComplete = gameconst.WitnessType.WITNESS_TYPE_IGNORE

        if not self.force:
            if hostEnt:
                self.force = hostEnt.force
            else:
                self.force = CBD.datas[self.summonId].get('force', 0)

        self.baseDodge = 0
        self.bornPosition = tuple(self.position)

        self.initEntitySkills()

        self.initBornAction()

        self.onInitPropsCompleted()

        self.hp = self.fullHp
        self.mp = self.fullMp

        self.siegeWarCamp = hostEnt.siegeWarCamp if hostEnt else 0

        # self.aiController = None

        spaceMgr = self.spaceMgr
        if spaceMgr:
            gid = utils.getGidFromGameEntityId(self.gameEntityId)
            if formula.isDungeonSpace(self.spaceNo):
                spaceMgr.addEntity(self.id, (str(self.fbEntityId), str(self.summonId),
                                             'gid_{}'.format(gid), self.__class__.__name__,))
            else:
                if spaceMgr:
                    spaceMgr.addEntity(self.id, (str(self.summonId), self.__class__.__name__) )

        self.triggeredFlowControllerRestNumIncreased()

        self.aiTriggerEvent(self.id, gameconst.AI_EVENT_ENTITY_BORN, ())

        if not self.ttl:
            self.ttl = float(CBD.datas[self.summonId].get('time', 0))

        if self.ttl:
            self.pyAddTimer(self.ttl, 0, gametimer.TIMER_CELL_TTL_DESTROY)

    def _initBornState(self):
        ifBornState = CBD.datas[self.summonId]['ifBornState']
        if ifBornState:
            self.changeBornState(gameconst.BornStateType.invisible)
            self._callback(CBSD.datas[ifBornState]['refreshTime'], 'changeBornState',
                           (gameconst.BornStateType.static, ), gametimer.TIMER_TAG_CHANGE_BORN_STATE)
        else:
            self.changeBornState(gameconst.BornStateType.move)

    @property
    def creepBaseId(self):
        return self.summonId

    def initBornAction(self):
        bornAction = self.getBornAction()
        if bornAction:
            bornAction(self, self, actionContext.ACTION_CONTEXT_DEFAULT)

    def getHost(self):
        en = KBEngine.entities.get(self.hostId)

        return en

    def getBindedEntity(self):
        # 召唤物对特定对象召唤的话记录对象EntityID
        return KBEngine.entities.get(self.bindedEntityId)

    def getConfigData(self):
        monsterId = self.summonId
        return CBD.datas.get(monsterId, {})

    def _ttlDestroy(self):
        self.safeDestroy()

    def baseFullHpRatio(self):
        if self.inheritPropRatio:
            return CBD.datas[self.creepBaseId].get('inheritFullHpRatio', 1.0)
        return super(Summon, self).baseFullHpRatio()

    def basePhysicalArmorRatio(self):
        if self.inheritPropRatio:
            return CBD.datas[self.creepBaseId].get('inheritPhysicalArmotRatio', 1.0)
        return super(Summon, self).basePhysicalArmorRatio()

    def baseMagicArmorRatio(self):
        if self.inheritPropRatio:
            return CBD.datas[self.creepBaseId].get('inheritMagicArmotRatio', 1.0)
        return super(Summon, self).baseMagicArmorRatio()

    def baseMinAtkRatio(self):
        if self.inheritPropRatio:
            return CBD.datas[self.creepBaseId].get('inheritMinAtkRatio', 1.0)
        return super(Summon, self).baseMinAtkRatio()

    def baseMaxAtkRatio(self):
        if self.inheritPropRatio:
            return CBD.datas[self.creepBaseId].get('inheritMaxAtkRatio', 1.0)
        return super(Summon, self).baseMaxAtkRatio()

    def initBaseProperties(self):
        owner = self.getHost()
        if owner:
            self.setProp('adjAtkBless', owner.getProp('adjAtkBless'))

        super().initBaseProperties()

    def onInitPropsCompleted(self):
        owner = self.getHost()
        if self.inheritPropRatio>0 and owner and not owner.isDestroyed:
            self.setProp('baseFullHp', int(owner.getProp('baseFullHp')*self.baseFullHpRatio()*self.inheritPropRatio), gameconst.SourceType.Init)
            self.setProp('baseMinPhysicalArmor', int(owner.getProp('baseMinPhysicalArmor')*self.basePhysicalArmorRatio()*self.inheritPropRatio), gameconst.SourceType.Init)
            self.setProp('baseMinMagicArmor', int(owner.getProp('baseMinMagicArmor')*self.baseMagicArmorRatio()*self.inheritPropRatio), gameconst.SourceType.Init)
            self.setProp('baseMaxPhysicalArmor', int(owner.getProp('baseMaxPhysicalArmor')*self.basePhysicalArmorRatio()*self.inheritPropRatio), gameconst.SourceType.Init)
            self.setProp('baseMaxMagicArmor', int(owner.getProp('baseMaxMagicArmor')*self.baseMagicArmorRatio()*self.inheritPropRatio), gameconst.SourceType.Init)

            otherProps = ['adjFullHp', 'adjFullHpAbs', 'mulFullHp', 'adjMinPhysicalAtk', 'adjMinPhysicalAtkAbs',
                        'adjMinMagicAtk', 'adjMinMagicAtkAbs', 'adjMaxPhysicalAtk', 'adjMaxPhysicalAtkAbs', 'adjMaxMagicAtk',
                        'adjMaxMagicAtkAbs',
                        'baseHit', 'adjHit', 'baseDodge', 'adjDodge', 
                       'baseFatal', 'adjFatal', 'baseAntiFatal',
                       'adjAntiFatal', 'baseMortal', 'adjMortal', 'baseAntiMortal', 'adjAntiMortal',
                       ]
            # 没有被定义和使用的属性,先移出来,不然报错
            # 'mulHit', 'mulDodge', 'baseDodgeDmg', 'adjDodgeDmg', 
            # 'mulDodgeDmg', 'mulFatal', 'mulAntiFatal', 'mulMortal', 'mulAntiMortal'
            for propName in otherProps:
                propVal = owner.getProp(propName)
                tp = type(propVal)
                self.setProp(propName, tp(propVal*self.inheritPropRatio), gameconst.SourceType.Init)


    # --------------------------------------------------------------------------------------------
    #                              Callbacks
    # --------------------------------------------------------------------------------------------

    def onTimer(self, tid, userData):
        self._onTimer(tid, userData)
        if utils.isBelongTimerTag(userData):
            self._onTimerCallback(tid)

        elif userData == gametimer.MONSTER_AI_THINK:
            self.tickAI()

        elif userData == gametimer.TIMER_CELL_SAFE_DESTROY:
            self.onDelayTimerSafeDestroy()

        else:
            super(Summon, self).onTimer(tid, userData)

    def tickAI(self):
        self.aiController and self.aiController.tickOnce()

    def _addTrap(self):
        radii = self.getAlertDistance()
        if radii<=0:
            return
        self.hateTrapId = self.addProximity(radii, radii, gameconst.HATE_TRAP)
        leaveAoiRange = self.getLeaveAlertDistance()
        self.addProximity(leaveAoiRange, 0.0, gameconst.LEAVE_AOI_TRAP)

    def onGetWitness(self):
        """
        KBEngine method.
        绑定了一个观察者(客户端)
        """
        DEBUG_MSG("Avatar::onGetWitness: %i." % self.id)

    def onLoseWitness(self):
        """
        KBEngine method.
        解绑定了一个观察者(客户端)
        """
        DEBUG_MSG("Avatar::onLoseWitness: %i." % self.id)

    def _preSafeDestory(self):
        """
        KBEngine method.
        entity销毁
        """
        DEBUG_MSG("summon::onDestroy: %i." % self.id)
        self.aiController and self.aiController.inheritSourceHate(self.hostId)
        if self.spaceMgr :
            self.spaceMgr.removeEntityById(self.id)
        super(Summon, self)._preSafeDestory()

        mGrp = self.monsterGroup
        if mGrp and mGrp.canBeDestroy():
            mGrp.safeDestroy()

        if self.getHost():
            self.getHost().removeSummon(self.id)

    def onModifyShieldVal(self, val, releaseRoleId, srcType, srcId):
        pass

    def onDead(self, killer, *args, **kwargs):
        DEBUG_MSG('Summon::onDead', killer)
        super(Summon, self).onDead(killer, hostId=self.hostId)
        self.removeAllBuff()
        self.cancelMoveController()
        self.destroySummonOnDead()
        if killer:
            self.allClients.onDead(killer.id)

        # 【【任务】副本编辑器中monsterID接入范围扩大为entityID】
        # killMonsterNum
        # 【【程序自主】【副本编辑器】服务流程编辑器怪物原型ID检测支持临时Entity(没有副本ID的Entity)】
        h = self.getHost()
        if not (h and h.IsAvatar):
            self.addDungeonKillCount()

        self.triggeredFlowControllerRestNumDecreased()

        if self.getHost():
            self.getHost().removeSummon(self.id)
        self.delaySafeDestroy(self.getDestroyDelay())

    def setAI(self, aiName):
        if not aiName:
            self.aiName=self.getDefenderAI()
        else:
            self.aiName=aiName

        if self.aiName<=0:
            return

        self.aiController = aiController.AIController(self.id, self.aiName, self.isActiveAttack())
        self.startThink()

    def changeBornState(self, newState):
        if newState == gameconst.BornStateType.static:
            ifBornState = CBD.datas[self.summonId].get('ifBornState', 1)
            nextState = gameconst.BornStateType.move
            self._callback(CBSD.datas[ifBornState]['bornStateTime'], 'changeBornState', (nextState, ), gametimer.TIMER_TAG_CHANGE_BORN_STATE)
        elif newState == gameconst.BornStateType.move:
            self.setAI(self.aiName)
            self._callback(1, '_addTrap', (), gametimer.TIMER_TAG_ADD_TRAP)
        elif newState == gameconst.BornStateType.reMove:
            newState = gameconst.BornStateType.move

        self.bornState = newState

    def addSkillByPlunderLingzhu(self, skillIds):
        for skillId in skillIds:
            self.addSkill(skillId, 1)

    def enterFightingState(self):
        super(Summon, self).enterFightingState()
        if self.isMoving():
            self.cancelMoveController()
        self.setProp('adjSpeed', self.getProp('adjSpeed') + CBD.datas[self.summonId].get('adjSpeed', 0),
                     gameconst.SourceType.Fight)

    def leaveFightingState(self):
        super(Summon, self).leaveFightingState()
        if self.isDie() or self.getProp('adjSpeed') == 0:
            return
        self.setProp('adjSpeed', self.getProp('adjSpeed') - CBD.datas[self.summonId].get('adjSpeed', 0),
                     gameconst.SourceType.Fight)
        return

    def getAIParam(self):
        return dataUtils.getAIParameters(self.summonId)

