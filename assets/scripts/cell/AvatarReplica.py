# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

import utils
import aiController

import iTimer
import iFubenSpace
import iAICombatUnit
import iFubenSpace
import EventMgr
import iGameEntity
import iMonsterGrp
import formula
import math
import dataUtils
import gameclass
import SkillManager

import appearance
import gameconst
import gametimer
import creep_base as CBD
import creep_bornState as CBSD
import fightProp_define as FP_DD
import const_const as CONST
import awardContext
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import character_charData as CHD
import skill_skill as SSD

class AvatarReplica(iAICombatUnit.IAICombatUnit, iTimer.ITimer, 
                    iGameEntity.IGameEntity, EventMgr.EventMgr, iFubenSpace.IFubenSpace,
                    iMonsterGrp.IMonsterGrp):
    IsAvatarReplica = True

    def __init__(self):
        LOG_DBG("AvatarReplica::__init__")
        self.init()

    def init(self):
        LOG_DBG("AvatarReplica::init")
        iAICombatUnit.IAICombatUnit.__init__(self)
        EventMgr.EventMgr.__init__(self)
        iGameEntity.IGameEntity.__init__(self)
        dataCfg = self.getCreepData()
        self.collidable = dataCfg.get('collisionDiameter', True)
        if self.force == 0:
            self.force = dataCfg.get('force', gameconst.ForceTypeEnum.Monster)       
        self.bornPosition = tuple(self.position)
        self.initPosition()
        self.initEntitySkills()
        self.initEntityGrowthData()
        self.onInitPropsCompleted()
        self.initEntBornAction()
        spaceMgr = self.spaceMgr
        gid = utils.parseGidFromGameEntityId(self.gameEntityId)
        if formula.inDungeonScene(self.spaceNo):
            if spaceMgr:
                spaceMgr.addEntity(self.id, (str(self.fbEntityId), str(self.creepbaseId),
                                             'gid_{}'.format(gid), self.__class__.__name__))
                self.isBoss and spaceMgr.setBossEntity(self.id)
        else:
            if spaceMgr:
                spaceMgr.addEntity(self.id, (str(self.creepbaseId), 'gid_{}'.format(gid), self.__class__.__name__))
                self.isBoss and spaceMgr.setBossEntity(self.id)
        self.triggeredFlowControllerRestNumIncreased()
        self.triggerAIEvent(self.id, gameconst.AI_EVENT_ENTITY_BORN, ())
        if self.ttl:
            self.pyAddTimer(self.ttl, 0, gametimer.TIMER_ON_CELL_TTL_DESTROY)
        self.overwriteProps()

    def onTimer(self, tid, userData):
        LOG_DBG("AvatarReplica::onTimer")
        self._onTimerTrigger(tid, userData)
        if utils.isBelongTimerTag(userData):
            self._onTimerCallback(tid)
        elif userData == gametimer.COMBAT_UNIT_AI_THINK:
            self.aiTick()
        elif userData == gametimer.TIMER_CELL_DELAY_SAFE_DESTROY:
            self.onDelayTimerSafeDestroy()
        else:
            super(AvatarReplica, self).onTimer(tid, userData)

    def doInitBaseProperties(self):
        super().doInitBaseProperties()
    
    def isBornDoNothing(self):
        return self.bornState in gameconst.BornStateEnum.bornDoNothing

    def _doInitBornState(self):
        LOG_DBG("AvatarReplica::_doInitBornState")
        monData = CBD.datas[self.creepbaseId]
        ifBornState = monData['ifBornState']
        if self.isBornDoNothing():
            pass
        if ifBornState:
            self.setBornState(gameconst.BornStateEnum.invisible)
            self.addTimerCB(CBSD.datas[ifBornState]['refreshTime'], 'setBornState',
                           (gameconst.BornStateEnum.static,), gametimer.TIMER_TAG_CHANGE_BORN_STATE)
        else:
            self.setBornState(gameconst.BornStateEnum.move)

    def setBornState(self, newState):
        LOG_DBG("AvatarReplica::setBornState", self.bornState, newState, self.aiName)
        if newState == gameconst.BornStateEnum.static:
            ifBornState = CBD.datas[self.creepbaseId].get('ifBornState', 1)
            nextState = gameconst.BornStateEnum.move
            self.addTimerCB(CBSD.datas[ifBornState]['bornStateTime'], 'setBornState', (nextState,),
                           gametimer.TIMER_TAG_CHANGE_BORN_STATE)
        elif newState == gameconst.BornStateEnum.move:
            if self.bornState in gameconst.BornStateEnum.bornDoNothing:
                self.initEntBornAction()
            self.setAI(self.aiName)
            self.addTimerCB(1, '_addTrap', (), gametimer.TIMER_TAG_ADD_TRAP)
        elif newState == gameconst.BornStateEnum.reMove:
            newState = gameconst.BornStateEnum.move
        elif newState == gameconst.BornStateEnum.reMove:
            newState = gameconst.BornStateEnum.move

        self.bornState = newState

    def setAI(self, aiName):
        LOG_DBG("AvatarReplica::setAI", self.aiName, self.getDefenderAI(), self.checkActiveAttack())
        if not aiName:
            self.aiName = self.getDefenderAI()
        else:
            self.aiName = aiName

        if self.aiName <= 0:
            return

        self.aiController = aiController.AIController(self.id, self.aiName, self.checkActiveAttack())
        if not self.aiController:
            return

        if self.aiController.needTickOnce():
            self.startThink()

    def initEntitySkills(self, creepData=None):
        self.skillPropInfo = None
        _skillList = []
        skillPropList = []

        skills = self.skills['skills']
        for skill in skills:
            skillId = skill['skillId']
            skillLv = skill['skillLv']
            #tNextCast = skill['tNextCast']
            #cdDelta = skill['cdDelta']

            wight, switch = (SSD.datas[skillId].get('autoBattleWeight', 10), 1)
            if utils.hasSkillTagById(skillId, gameconst.SkillTag.DodgeSkill):
                wight, switch = (0, 0)
            #elif utils.hasSkillTagById(skillId, gameconst.SkillTag.GeneralSkill):
            #    wight, switch = (10, 1)
                
            _skillList.append(skillId)
            skillPropList.append(wight)
            self.addSkillInEntity(skillId, skillLv)
            self.skillDic.setSkillSwitch(self, skillId, switch)
        if _skillList:
            self.skillPropInfo = (_skillList, skillPropList)
        else:
            self.skillPropInfo = None
        
        LOG_DBG("AvatarReplica::initEntitySkills1", self.skillPropInfo)
        LOG_DBG("AvatarReplica::initEntitySkills2", self.skillDic.toDict())

    def getBuffData(self):
        buffData = {'buffs': []}
        buffList = buffData['buffs']
        for buffId, buffMap in self.buffMgrDic.items():
            for buffSrcKey, buffVal in buffMap.items():
                data = {
                    'tStartTime': buffVal.tStartTime,
                    'attNum': buffVal.attNum,
                    'skillNum': buffVal.skillNum,
                    'beatNum': buffVal.beatNum
                }
                buffInfo = {
                    'buffId': buffId,
                    'buffSrcKey': buffSrcKey,
                    'level': buffVal.level,
                    'releaseId': 0,
                    'data': data
                }
                buffList.append(buffInfo)
        return buffData

    def initEntityGrowthData(self):
        LOG_DBG("AvatarReplica::initEntityGrowthData1", self.buffs)
        buffs = self.buffs['buffs']
        for buffInfo in buffs:
            buffId = buffInfo['buffId']
            level = buffInfo['level']
            #buffSrcKey = buffInfo['buffSrcKey']
            #releaseId = buffInfo['releaseId']
            #data = buffInfo['data']
            self.addBuff(buffId, level, self.id)
        LOG_DBG("AvatarReplica::initEntityGrowthData2", self.getBuffData())

    def onInitPropsCompleted(self):
        avatar = self.getReplicaAvatar()
        if not avatar:
            LOG_ERR("AvatarReplica::onInitPropsCompleted no avatar", self.avatarId)
            return
        LOG_DBG("AvatarReplica::onInitPropsCompleted avatar", self.avatarId, self.avatarGbId, avatar.id)
        propValDic = avatar.getFightProps()
        for prop in sorted(propValDic.keys()):
            setattr(self, prop, propValDic[prop])
            #LOG_DBG("AvatarReplica::onInitPropsCompleted self/avatar prop/value", prop, avatar.getProp(prop), getattr(self, prop))

    def overwriteProps(self):
        LOG_DBG("AvatarReplica::overwriteProps")
        overwriteProps = self.tmpProps.pop('overwriteProps', {})
        initHpMult = overwriteProps.get('hpMult', 1.0)
        initMpMult = overwriteProps.get('mpMult', 1.0)
        LOG_DBG("AvatarReplica::overwriteProps self overwriteProps, hpMult, mpMult", overwriteProps, initHpMult, initMpMult)
        if initHpMult > 0:
            self.fullHp = max(1, math.ceil(self.fullHp * initHpMult))
            self.hp = self.fullHp
        if initMpMult > 0:
            self.fullMp = max(1, math.ceil(self.fullMp * initMpMult))
            self.mp = self.fullMp
        LOG_DBG("AvatarReplica::overwriteProps self hp/fullHp", self.hp, self.fullHp)
        LOG_DBG("AvatarReplica::overwriteProps self mp/fullMp", self.mp, self.fullMp)

    def getCreepData(self):
        return CBD.datas.get(self.creepbaseId, {})
    
    def getConfigData(self):
        return CBD.datas.get(self.creepbaseId, {})

    def getReplicaAvatar(self):
        en = KBEngine.entities.get(self.avatarId)
        return en

    def _onTtlDestroy(self):
        self.safeDestroy()

    def aiTick(self):
        self.aiController and self.aiController.tickOnce()

    def _addTrap(self):
        radii = self.getAlertDistance()
        if radii <= 0:
            return
        self.hateTrapId = self.addProximity(radii, radii, gameconst.AGGRO_TRIGGER_TRAP)
        leaveAoiRange = self.getLeaveAlertDistance()
        self.addProximity(leaveAoiRange, 0.0, gameconst.AOI_EXIT_TRAP)

    def onGetWitness(self):
        LOG_DBG("AvatarReplica::onGetWitness: %i." % self.id)

    def onLoseWitness(self):
        LOG_DBG("AvatarReplica::onLoseWitness: %i." % self.id)

    def onWitnessed(self, isWitnessed):
        LOG_DBG("AvatarReplica::onWitnessed", isWitnessed)
        if self.aiController and self.aiController.needTickOnce():
            self.startThink()

        if not self.aiController or not self.aiController.needTickOnce():
            self.stopThink()

        if not isWitnessed and self.aiController:
            self.aiController.onLoseWitnessed()

    def _preSafeDestory(self):
        LOG_DBG("AvatarReplica::_preSafeDestory: %i." % self.id)
        super(AvatarReplica, self)._preSafeDestory()
        spaceMgr = self.spaceMgr
        if spaceMgr:
            spaceMgr.removeEntById(self.id)

    def _postSafeDestory(self):
        pass

    def enterFightingState(self):
        super(AvatarReplica, self).enterFightingState()
        if self.isMoving():
            self.removeMoveController()
        self.setProp('adjSpeed', self.getProp('adjSpeed') + CBD.datas[self.creepbaseId].get('adjSpeed', 0),
                     gameconst.SourceType.SrcTpFight)

    def leaveFightingState(self):
        super(AvatarReplica, self).leaveFightingState()
        if self.isDie() or self.getProp('adjSpeed') == 0:
            return
        self.setProp('adjSpeed', self.getProp('adjSpeed') - CBD.datas[self.creepbaseId].get('adjSpeed', 0),
                     gameconst.SourceType.SrcTpFight)

    def getAIParam(self):
        return dataUtils.getAIParameters(self.creepbaseId)
    
    def checkCombatRangeY(self, target):
        attackHeightLimit = CBD.datas[self.creepbaseId]['attackHeightLimit']
        if attackHeightLimit:
            heightLimit = attackHeightLimit
        else:
            heightLimit = CONST.datas['damageHeightLimit'].get('value')

        return abs(self.position[1] - target.position[1]) <= heightLimit

    def onDead(self, killer, *args, **kwargs):
        delay = self.getDestroyDelay()
        kwargs['delay'] = delay
        LOG_DBG("AvatarReplica::onDead", killer, args, kwargs)
        super(AvatarReplica, self).onDead(killer, *args, **kwargs)
        self.removeAllBuff()
        self.removeMoveController()
        self.destroySummonOnDead()
        #self.cancelRouting()
        self.triggeredFlowControllerRestNumDec()
        self.delaySafeDestroy(delay)

        if killer:
            self.allClients.onDead(killer.id)
            self.triggerAIEvent(self.id, gameconst.AI_EVENT_DEAD, (killer.id,))
        '''
            opUUID = KBEngine.genUUID64()
            srcType = AAC_AACDD.datas.BONUS_SRC_KILL_MONSTER
            detail = gameclass.AwardDetailCls(replicaId=self.creepbaseId, spaceNo=self.spaceNo)
            rewardIDList, shareRewardIDList, displayModeList = self.getDeathDrop()
        
            dropCtx = awardContext.DropAwardCtx(self.id,
                                                self.level,
                                                {'lv': self.level, 'factor': 1},
                                                eventTipId=self.creepbaseId,
                                                monsterSpaceNo=self.spaceNo)
            dropCtx.addContextVar('srcType', srcType)
            dropCtx.addContextVar('opUUID', opUUID)
            dropCtx.addContextVar('detail', detail)
            self.doDispatchAward(killer, rewardIDList, shareRewardIDList, displayModeList, dropCtx)

        host = utils.getHostEntity(killer)
        if host and host.IsAvatar:
            host.base.triggerAchievement(gameconst.AchieveType.KILL_MONSTER)
            host.base.triggerAchievementWithCtx(gameconst.AchieveType.KILL_TAR_SUFFIX_MONSTER, {'suffixId': self.getCreepData().get('nameSuffixID', 0)})
            host.base.triggerAchievementWithCtx(gameconst.AchieveType.KILL_TAR_MONSTER, {'monsterId': self.creepbaseId})
        '''

    @property
    def creepbaseId(self):
        return self.replicaId

    def addUltraSkillPower(self, addVal, context = None):
        if addVal <= 0:
            return

        _ultSkillId = CHD.datas[self.school]['ult']
        ''''''
        if not self.hasSkill(_ultSkillId):
            return

        ultimatePowerMax = CONST.datas['ultimatePowerMax'].get('value')
        self.ultraSkillPower = min(ultimatePowerMax, self.ultraSkillPower + addVal)

    def getInscriptionEffects(self, skillID, effectType):
        return self.glyphEquipData.getInscriptionEffects(skillID, effectType)
    
    def changeMorphStateCell(self, morphState):
        if self.skillPropInfo:
            for _idx, _skillId in enumerate(self.skillPropInfo[0]):
                _modId = SSD.skillToModDic.get(_skillId)
                if not _modId:
                    continue
                _newSkillId = SSD.modDic[_modId][morphState]
                if _newSkillId == _skillId:
                    continue

                self.removeSkill(_skillId)
                self.skillPropInfo[0][_idx] = _newSkillId
