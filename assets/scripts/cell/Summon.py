# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

import iTimer
import EventMgr
import iFubenSpace
import iMonsterGrp
import iMonsterDungeon
import iGameEntity
import iClient

import utils
import dataUtils
import aiController
import gametimer
import gameconst
import formula
import iAICombatUnit

import creep_base as C_BD
import const_const as C_CD
import creep_bornState as CBSD


class Summon(iAICombatUnit.IAICombatUnit, iTimer.ITimer,
             EventMgr.EventMgr, iFubenSpace.IFubenSpace,
             iMonsterGrp.IMonsterGrp, iMonsterDungeon.IMonsterDungeon,
             iGameEntity.IGameEntity, iClient.IClient,):
    IsSummon = True

    def __init__(self):
        if not self.level:
            self.level = gameconst.MIN_LEVEL
        elif self.level > utils.getMaxPlayerLevel():
            self.level = utils.getMaxPlayerLevel()

        iAICombatUnit.IAICombatUnit.__init__(self)
        EventMgr.EventMgr.__init__(self)
        iGameEntity.IGameEntity.__init__(self)
        self.name = C_BD.datas[self.summonId].get('name', '无名怪')
        _hostEnt = self.getHost()
        if _hostEnt and _hostEnt.IsAvatar:
            self.cellFlags = utils.bset(self.cellFlags, gameconst.CELL_FLAGS_IS_HOST_AVATAR)

        if not self.hostId or (_hostEnt and not _hostEnt.IsAvatar):
            self.isWitnessComplete = gameconst.WitnessTypeEnum.WITNESS_ENUM_IGNORE

        if not self.force:
            if _hostEnt:
                self.force = _hostEnt.force
            else:
                self.force = C_BD.datas[self.summonId].get('force', 0)

        self.baseDodge = 0
        self.bornPosition = tuple(self.position)

        self.initEntitySkills()

        self.initEntBornAction()

        self.onInitPropsCompleted()

        self.hp = self.fullHp
        self.mp = self.fullMp

        self.siegeWarCamp = _hostEnt.siegeWarCamp if _hostEnt else 0

        spaceMgr = self.spaceMgr
        if spaceMgr:
            gid = utils.parseGidFromGameEntityId(self.gameEntityId)
            if formula.inDungeonScene(self.spaceNo):
                spaceMgr.addEntity(
                    self.id, 
                    (
                        str(self.fbEntityId), 
                        'gid_{}'.format(gid), 
                        str(self.summonId),
                        self.__class__.__name__,
                    ),)
            else:
                if spaceMgr:
                    spaceMgr.addEntity(self.id, (str(self.summonId), self.__class__.__name__,) )

        self.triggeredFlowControllerRestNumIncreased()

        self.triggerAIEvent(self.id, gameconst.AI_EVENT_ENTITY_BORN, ())

        if not self.ttl:
            self.ttl = float(C_BD.datas[self.summonId].get('time', 0.0))

        if self.ttl:
            self.pyAddTimer(self.ttl, 0, gametimer.TIMER_ON_CELL_TTL_DESTROY)

    def _doInitBornState(self):
        ifBornState = C_BD.datas[self.summonId]['ifBornState']
        if ifBornState:
            self.setBornState(gameconst.BornStateEnum.invisible)
            self.addTimerCB(CBSD.datas[ifBornState]['refreshTime'], 'setBornState',
                           (gameconst.BornStateEnum.static, ), gametimer.TIMER_TAG_CHANGE_BORN_STATE)
        else:
            self.setBornState(gameconst.BornStateEnum.move)

    @property
    def creepbaseId(self):
        return self.summonId

    def initEntBornAction(self):
        bornAction = self.getBornAction()
        if bornAction:
            bornAction(self, self, self.createContext)

    def getHost(self):
        _ent = KBEngine.entities.get(self.hostId)

        return _ent

    def getBindedEntity(self):
        # 召唤物对特定对象召唤的话记录对象EntityID
        return KBEngine.entities.get(self.bindedEntityId)

    def getCreepData(self):
        monsterId = self.summonId
        return C_BD.datas.get(monsterId, {})

    def getConfigData(self):
        return C_BD.datas.get(self.summonId, {})

    def _onTtlDestroy(self):
        self.safeDestroy()

    def baseFullHpRatio(self):
        if self.inheritPropRatio:
            return C_BD.datas[self.creepbaseId].get('inheritFullHpRatio', 1.0)
        return super(Summon, self).baseFullHpRatio()

    def baseMagicArmorRatio(self):
        if self.inheritPropRatio:
            return C_BD.datas[self.creepbaseId].get('inheritMagicArmotRatio', 1.0)
        return super(Summon, self).baseMagicArmorRatio()

    def basePhysicalArmorRatio(self):
        if self.inheritPropRatio:
            return C_BD.datas[self.creepbaseId].get('inheritPhysicalArmotRatio', 1.0)
        return super(Summon, self).basePhysicalArmorRatio()

    def baseMaxAtkRatio(self):
        if self.inheritPropRatio:
            return C_BD.datas[self.creepbaseId].get('inheritMaxAtkRatio', 1.0)
        return super(Summon, self).baseMaxAtkRatio()

    def baseMinAtkRatio(self):
        if self.inheritPropRatio:
            return C_BD.datas[self.creepbaseId].get('inheritMinAtkRatio', 1.0)
        return super(Summon, self).baseMinAtkRatio()

    def doInitBaseProperties(self):
        owner = self.getHost()
        if owner:
            self.setProp('adjAtkBless', owner.getProp('adjAtkBless'))

        super().doInitBaseProperties()

    def onInitPropsCompleted(self):
        _owner = self.getHost()
        if self.inheritPropRatio>0 and _owner and not _owner.isDestroyed:
            self.setProp('baseFullHp', int(_owner.getProp('baseFullHp')*self.baseFullHpRatio()*self.inheritPropRatio), gameconst.SourceType.SrcTpInit)
            self.setProp('baseMinPhysicalArmor', int(_owner.getProp('baseMinPhysicalArmor')*self.basePhysicalArmorRatio()*self.inheritPropRatio), gameconst.SourceType.SrcTpInit)
            self.setProp('baseMinMagicArmor', int(_owner.getProp('baseMinMagicArmor')*self.baseMagicArmorRatio()*self.inheritPropRatio), gameconst.SourceType.SrcTpInit)
            self.setProp('baseMaxPhysicalArmor', int(_owner.getProp('baseMaxPhysicalArmor')*self.basePhysicalArmorRatio()*self.inheritPropRatio), gameconst.SourceType.SrcTpInit)
            self.setProp('baseMaxMagicArmor', int(_owner.getProp('baseMaxMagicArmor')*self.baseMagicArmorRatio()*self.inheritPropRatio), gameconst.SourceType.SrcTpInit)

            otherProps = [
                            'adjFullHp', 'adjFullHpAbs', 'mulFullHp', 'adjMinPhysicalAtk', 'adjMinPhysicalAtkAbs', 'adjMinMagicAtk', 'adjMinMagicAtkAbs', 
                            'adjMaxPhysicalAtk', 'adjMaxPhysicalAtkAbs', 'adjMaxMagicAtk', 'adjMaxMagicAtkAbs', 'baseHit', 'adjHit', 'baseDodge', 'adjDodge', 
                            'baseFatal', 'adjFatal', 'baseAntiFatal', 'adjAntiFatal', 'baseMortal', 'adjMortal', 'baseAntiMortal', 'adjAntiMortal',
                            'evasion', 'accuracy',
                        ]
            # 没有被定义和使用的属性,先移出来,不然报错
            # 'mulHit', 'mulDodge', 'baseDodgeDmg', 'adjDodgeDmg',
            # 'mulDodgeDmg', 'mulFatal', 'mulAntiFatal', 'mulMortal', 'mulAntiMortal'
            for propName in otherProps:
                propVal = _owner.getProp(propName)
                _tp = type(propVal)
                self.setProp(propName, _tp(propVal*self.inheritPropRatio), gameconst.SourceType.SrcTpInit)


    # --------------------------------------------------------------------------------------------
    #                              Callbacks
    # --------------------------------------------------------------------------------------------

    def onTimer(self, tid, userData):
        self._onTimerTrigger(tid, userData)
        if utils.isBelongTimerTag(userData):
            self._onTimerCallback(tid)

        elif userData == gametimer.COMBAT_UNIT_AI_THINK:
            self.aiTick()

        elif userData == gametimer.TIMER_CELL_DELAY_SAFE_DESTROY:
            self.onDelayTimerSafeDestroy()

        else:
            super(Summon, self).onTimer(tid, userData)

    def aiTick(self):
        if self.aiController:
            self.aiController.tickOnce()

    def _addTrap(self):
        _radii = self.getAlertDistance()
        if _radii<=0:
            return
        self.hateTrapId = self.addProximity(_radii, _radii, gameconst.AGGRO_TRIGGER_TRAP)
        leaveAoiRange = self.getLeaveAlertDistance()
        self.addProximity(leaveAoiRange, 0.0, gameconst.AOI_EXIT_TRAP)

    def onGetWitness(self):
        """
        KBEngine method.
        绑定了一个观察者(客户端)
        """
        LOG_DBG("Avatar::onGetWitness: %i." % self.id)

    def onLoseWitness(self):
        """
        KBEngine method.
        解绑定了一个观察者(客户端)
        """
        LOG_DBG("Avatar::onLoseWitness: %i." % self.id)

    def _preSafeDestory(self):
        """
        KBEngine method.
        entity销毁
        """
        LOG_DBG("summon::onDestroy: %i." % self.id)
        if self.aiController:
            self.aiController.inheritSourceHate(self.hostId)

        if self.spaceMgr:
            self.spaceMgr.removeEntById(self.id)

        super(Summon, self)._preSafeDestory()

        _mGrp = self.monsterGroup
        if _mGrp and _mGrp.canBeDestroy():
            _mGrp.safeDestroy()

        if self.getHost():
            self.getHost().removeSummonById(self.id)

    def setAI(self, aiName):
        if aiName:
            self.aiName=aiName
        else:
            self.aiName=self.getDefenderAIName()

        if self.aiName<=0:
            return

        self.aiController = aiController.AIControllerCls(self.id, self.aiName, self.checkActiveAttack())
        self.startThink()

    def onDead(self, killer, *args, **kwargs):
        LOG_DBG('Summon::onDead', killer)
        super(Summon, self).onDead(killer, hostId=self.hostId)
        self.doRemoveAllBuff()
        self.removeMoveController()
        self.destroySummonOnDead()
        if killer:
            self.allClients.onDead(killer.id)

        # 【【任务】副本编辑器中monsterID接入范围扩大为entityID】
        # killMonsterNum
        # 【【程序自主】【副本编辑器】服务流程编辑器怪物原型ID检测支持临时Entity(没有副本ID的Entity)】
        _h = self.getHost()
        if not (_h and _h.IsAvatar):
            self.addDungeonKillCount()

        self.triggeredFlowControllerRestNumDec()

        if _h:
            _h.removeSummonById(self.id)

        self.delaySafeDestroy(self.getDestroyDelay())

    def setBornState(self, newState):
        if newState == gameconst.BornStateEnum.static:
            ifBornState = C_BD.datas[self.summonId].get('ifBornState', 1)
            nextState = gameconst.BornStateEnum.move
            self.addTimerCB(CBSD.datas[ifBornState]['bornStateTime'], 'setBornState', (nextState, ), gametimer.TIMER_TAG_CHANGE_BORN_STATE)
        elif newState == gameconst.BornStateEnum.move:
            self.setAI(self.aiName)
            self.addTimerCB(1, '_addTrap', (), gametimer.TIMER_TAG_ADD_TRAP)
        elif newState == gameconst.BornStateEnum.reMove:
            newState = gameconst.BornStateEnum.move

        self.bornState = newState

    def addSkillByPlunderLingzhu(self, skillIds):
        for skillId in skillIds:
            self.addSkillInEntity(skillId, 1)

    def enterFightingState(self):
        super(Summon, self).enterFightingState()
        if self.isMoving():
            self.removeMoveController()
        self.setProp('adjSpeed', self.getProp('adjSpeed') + C_BD.datas[self.summonId].get('adjSpeed', 0),
                     gameconst.SourceType.SrcTpFight)

    def leaveFightingState(self):
        super(Summon, self).leaveFightingState()
        if self.isDie() or self.getProp('adjSpeed') == 0:
            return
        self.setProp('adjSpeed', self.getProp('adjSpeed') - C_BD.datas[self.summonId].get('adjSpeed', 0),
                     gameconst.SourceType.SrcTpFight)
        return

    def getAIParam(self):
        return dataUtils.getAIParameters(self.summonId)

    def checkCombatRangeY(self, target):
        if utils.bhas(self.cellFlags, gameconst.CELL_FLAGS_IS_HOST_AVATAR) and target.IsMonster:
            underAttackHeightLimit = C_BD.datas[target.monsterId]['underAttackHeightLimit']
            if underAttackHeightLimit:
                heightLimit = underAttackHeightLimit
            else:
                heightLimit = C_CD.datas['damageHeightLimit'].get('value')
        else:
            heightLimit = C_CD.datas['damageHeightLimit'].get('value')

        return abs(self.position[1] - target.position[1]) <= heightLimit



