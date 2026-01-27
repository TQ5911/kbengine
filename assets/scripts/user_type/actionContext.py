# -*- coding: utf-8 -*-
import KBEngine
import random

import gameconst
import gameconfig
import math
from KBEDebug import *
import time

import userType
import gameclass
import skill_skill as SSD
import mounts_set as MSD
import const_const as CONST

ACTION_UNKNOWN = 0
ACTION_USE_SKILL = 1
ACTION_PASSIVE_SKILL = 2
ACTION_CREATION_LOOP = 3
ACTION_CREATION_COMMON = 5

ACTION_HOME_BOSS_ABILITY = 6
ACTION_AUREOLE = 7
ACTION_BUFF_TICK = 9
ACTION_BUFF_END = 10
ACTION_BUFF_EFFECT = 11
ACTION_CHANGE_SKILL_SLOT = 12
ACTION_SKILL_COMMON = 13
ACTION_EVENT_EFFECT = 14
ACTION_USE_ITEM = 16
ACTION_DEAD = 17
ACTION_EQUIP = 18
ACTION_EQUIP_SET = 19
ACTION_FLOW_CONTROLLER_CALLED = 22
ACTION_CLAIM_TASK = 24
ACTION_USE_ITEM_HEAL = 29
ACTION_USE_BOX_TYPE_ITEM = 30
ACTION_AI_ACTION = 31

class ActionContext(userType.UserSoleType):
    actionType = ACTION_UNKNOWN

    def __init__(self, parentContext=None):
        self.parentContext = parentContext
        self.actionStage = 0
        self.customDict = {}

    def __str__(self):
        return '%s %s' % (self.actionType, str(vars(self)))

    def getSrcEntity(self):
        return None

    def setCustomVar(self, name, val):
        self.customDict[name] = val

    def getCustomVar(self, name):
        return self.customDict.get(name)

    def _lateReload(self):
        super(ActionContext, self)._lateReload()
        if self.parentContext:
            self.parentContext.reloadScript()

    def getCtxFromActionQueue(self, actionType):
        if self.actionType == actionType:
            return self

        if self.parentContext:
            return self.parentContext.getCtxFromActionQueue(actionType)

        return None
    
    def getTopCtxFromActionQueue(self, actionType):
        # 如果父节点，继续往上找
        if self.parentContext:
            parentContext = self.parentContext.getTopCtxFromActionQueue(actionType)
            if parentContext:
                # 如果父节点满足，返回父节点
                return parentContext
        # 检查当前节点，如果当前节点，满足，返回当前节点
        if self.actionType == actionType:
            return self
        return None

ACTION_CONTEXT_DEFAULT = ActionContext()

class UseSkillCtx(ActionContext):
    actionType = ACTION_USE_SKILL
    def __init__(self, casterEntId, skillId, skillArgs, useTargetId, effectedEntIds, skillObj, skillResult, castBySkill=0, isSucc=None, parentCtx=None,actionProgress=0,isLastActionStage=False):
        super(UseSkillCtx, self).__init__(parentCtx)
        self.casterEntId = casterEntId          #�ż��ܵ�entity id
        self.skillId = skillId                  #����id
        self.skillArgs = list(skillArgs)        #ʹ�ò��������꣬���򣬽Ƕȵ�
        self.useTargetId = useTargetId          #ʹ��Ŀ��
        self.effectedEntIds = effectedEntIds    #����Ŀ��
        self.castBySkill = castBySkill          #�ڱ�ļ���action���ͷŵ�
        self.skillObj = skillObj                #SkillAttack����
        self.skillResult = skillResult
        self.isSucc = isSucc
        self.duringBigWorldDuel = False
        self.actionProgress = actionProgress                 #���ܽ���
        self.isLastActionStage = isLastActionStage           #�Ƿ����һ��actionstage
        self.checkInRange = True

        if self.skillResult:
            self.skillResult.sourceType = self.getDmgSourceType()
            self.skillResult.sourceId = self.getDmgSourceId()

    def getDmgSourceType(self):
        return gameconst.SourceType.Skill

    def getDmgSourceId(self):
        return self.skillId

    def getCombatResult(self):
        return self.skillResult

    def getSrcEntity(self):
        return KBEngine.entities.get(self.casterEntId)

    def _lateReload(self):
        super(UseSkillCtx, self)._lateReload()

        if self.skillObj:
            self.skillObj.reloadScript()

        if self.skillResult:
            self.skillResult.reloadScript()

class SkillCommonCtx(ActionContext):
    actionType = ACTION_SKILL_COMMON
    def __init__(self, skillId, parentCtx=None):
        super(SkillCommonCtx, self).__init__(parentCtx)
        self.skillId = skillId                  #����id
class CreationCtx(ActionContext):
    actionType = ACTION_CREATION_LOOP
    def __init__(self, creationEntId, effectedEntIds, creationResult, parentCtx=None, loopTimes=0, context=None):
        super(CreationCtx, self).__init__(parentCtx)
        self.creationEntId = creationEntId      #����entity id
        self.effectedEntIds = effectedEntIds    #��������Ŀ��
        self.creationResult = creationResult
        self.loopTimes = loopTimes
        self.parentContext = context

        if self.creationResult:
            self.creationResult.sourceType = self.getDmgSourceType()
            self.creationResult.sourceId = self.getDmgSourceId()

    def _lateReload(self):
        super(CreationCtx, self)._lateReload()

        if self.creationResult:
            self.creationResult.reloadScript()

    @property
    def creationId(self):
        return self.getDmgSourceId()

    def getDmgSourceType(self):
        return gameconst.SourceType.Creation

    def getDmgSourceId(self):
        e = KBEngine.entities.get(self.creationEntId)
        return e.creationId if e else 0

    def getCombatResult(self):
        return self.creationResult

    def getSrcEntity(self):
        return KBEngine.entities.get(self.creationEntId)
class BuffRefreshCtx(ActionContext):
    actionType = ACTION_BUFF_TICK
    def __init__(self, srcEntId, ownerEntId, buffId, buffLevel, srcKey, buffResult, parentCtx=None):
        super(BuffRefreshCtx, self).__init__(parentCtx)
        self.srcEntId = srcEntId
        self.ownerEntId = ownerEntId
        self.buffId = buffId
        self.srcKey = srcKey
        self.buffLevel = buffLevel
        self.buffResult = buffResult

        if self.buffResult:
            self.buffResult.sourceType = self.getDmgSourceType()
            self.buffResult.sourceId = self.getDmgSourceId()

    def _lateReload(self):
        super(BuffRefreshCtx, self)._lateReload()

        if self.buffResult:
            self.buffResult.reloadScript()

    def getDmgSourceType(self):
        return gameconst.SourceType.Buff

    def getDmgSourceId(self):
        return self.buffId

    def getCombatResult(self):
        return self.buffResult

    def getSrcEntity(self):
        return KBEngine.entities.get(self.srcEntId)

    def getOwnerEntity(self):
        return KBEngine.entities.get(self.ownerEntId)

    def getBuffObj(self):
        owner = self.getOwnerEntity()
        if not owner:
            return None

        return owner.getBuffByBuffId(self.buffId, self.srcKey)

class BuffEndCtx(ActionContext):
    actionType = ACTION_BUFF_END
    def __init__(self, srcEntId, ownerEntId, buffId, buffLevel, srcKey, removeType, buffResult, parentCtx=None):
        super(BuffEndCtx, self).__init__(parentCtx)
        self.srcEntId = srcEntId
        self.ownerEntId = ownerEntId
        self.buffId = buffId
        self.srcKey = srcKey
        self.buffLevel = buffLevel
        self.removeType = removeType
        self.buffResult = buffResult

        if self.buffResult:
            self.buffResult.sourceType = self.getDmgSourceType()
            self.buffResult.sourceId = self.getDmgSourceId()

    def _lateReload(self):
        super(BuffEndCtx, self)._lateReload()

        if self.buffResult:
            self.buffResult.reloadScript()

    def getDmgSourceType(self):
        return gameconst.SourceType.Buff

    def getDmgSourceId(self):
        return self.buffId

    def getCombatResult(self):
        return self.buffResult

    def getSrcEntity(self):
        return KBEngine.entities.get(self.srcEntId)

    def getOwnerEntity(self):
        return KBEngine.entities.get(self.ownerEntId)

    def getBuffObj(self):
        owner = self.getOwnerEntity()
        if not owner:
            return None

        return owner.getBuffByBuffId(self.buffId, self.srcKey)

class BuffEffectCtx(ActionContext):
    actionType = ACTION_BUFF_EFFECT
    def __init__(self, srcEntId, ownerEntId, buffId, buffLevel, srcKey, effectId, args, effectResult, parentCtx=None):
        super(BuffEffectCtx, self).__init__(parentCtx)
        self.srcEntId = srcEntId
        self.ownerEntId = ownerEntId
        self.buffId = buffId
        self.srcKey = srcKey
        self.buffLevel = buffLevel
        self.effectId = effectId
        self.args = gameclass.DummyObject(**args)
        self.effectResult = effectResult

        if self.effectResult:
            self.effectResult.sourceType = self.getDmgSourceType()
            self.effectResult.sourceId = self.getDmgSourceId()

    def _lateReload(self):
        super(BuffEffectCtx, self)._lateReload()

        if self.effectResult:
            self.effectResult.reloadScript()

        self.args.reloadScript()

    def getDmgSourceType(self):
        return gameconst.SourceType.Buff

    def getDmgSourceId(self):
        return self.buffId

    def getCombatResult(self):
        return self.effectResult

    def getSrcEntity(self):
        return KBEngine.entities.get(self.srcEntId)

    def getOwnerEntity(self):
        return KBEngine.entities.get(self.ownerEntId)

    def getBuffObj(self):
        owner = self.getOwnerEntity()
        if not owner:
            return None

        return owner.getBuffByBuffId(self.buffId, self.srcKey)


#�¼�������effect��������
class EventEffectCtx(BuffEffectCtx):
    actionType = ACTION_EVENT_EFFECT
    def __init__(self, srcEntId, ownerEntId, buffId, buffLv, srcKey, effectId, args, eventContext, effectResult, parentCtx=None):
        super(EventEffectCtx, self).__init__(srcEntId, ownerEntId, buffId, buffLv, srcKey, effectId, args, effectResult, parentCtx)
        self.eventContext = eventContext

    def getSrcEntity(self):
        return KBEngine.entities.get(self.srcEntId)

    def _lateReload(self):
        super(EventEffectCtx, self)._lateReload()

        if self.eventContext:
            self.eventContext.reloadScript()

class ChangeSkillSlotCtx(ActionContext):
    actionType = ACTION_CHANGE_SKILL_SLOT
    def __init__(self, skillId, parentCtx=None):
        super(ChangeSkillSlotCtx, self).__init__(parentCtx)
        self.skillId = skillId                  #����id

class AiActionCtx(ActionContext):
    actionType = ACTION_AI_ACTION
    def __init__(self, creepBaseId, parentCtx=None):
        super(AiActionCtx, self).__init__(parentCtx)
        self.creepBaseId = creepBaseId

class PlunderRewardCtx(object):
    def __init__(self, lingqiPointLv=0, lingStone=0, hunStone=0, completion=0):
        self.lingqiPointLv = lingqiPointLv
        self.lingStone = lingStone
        self.hunStone = hunStone
        self.completion = completion
class UseItemCtx(object):
    actionType = ACTION_USE_ITEM

    def __init__(self, targetId=0, argsList=None, withMailId=0, bindType=gameconst.ItemBindType.BINDTYPE_NOT_SPECIFIED,
                 itemObj=None):
        self.targetId = targetId
        self.argsList = [] if argsList is None else argsList
        self.pendingOpId = 0
        self.withMailId = withMailId
        self.bindType = bindType
        self.itemObj = itemObj

    def _lateReload(self):
        super(UseItemCtx, self)._lateReload()


class UseBoxTypeItemCtx(object):
    actionType = ACTION_USE_BOX_TYPE_ITEM

    def __init__(self, targetId=0, argsList=None, withMailId=0, awardVal=None,
                 bindType=gameconst.ItemBindType.BINDTYPE_NOT_SPECIFIED):
        self.targetId = targetId
        self.argsList = [] if argsList is None else argsList
        self.pendingOpId = 0
        self.withMailId = withMailId
        self.bindType = bindType
        self.awardVal = awardVal

    def _lateReload(self):
        super(UseBoxTypeItemCtx, self)._lateReload()


class UseItemHealCtx(ActionContext):
    actionType = ACTION_USE_ITEM_HEAL

    def __init__(self, itemId, srcEntId=0, itemResult=None, parentCtx=None):
        super(UseItemHealCtx, self).__init__(parentCtx)
        self.itemId = itemId
        self.srcEntId = srcEntId
        self.itemResult = itemResult
        if self.itemResult:
            self.itemResult.sourceType = self.getDmgSourceType()
            self.itemResult.sourceId = self.getDmgSourceId()

    def getDmgSourceType(self):
        return gameconst.SourceType.Item

    def getDmgSourceId(self):
        return self.itemId

    def getSrcEntity(self):
        return KBEngine.entities.get(self.srcEntId)

    def getCombatResult(self):
        return self.itemResult

class DeadActCtx(ActionContext):
    actionType = ACTION_DEAD
    def __init__(self, killerEntId, actResult, parentCtx=None):
        super(DeadActCtx, self).__init__(parentCtx)
        self.killerEntId = killerEntId

        if self.actResult:
            self.actResult.sourceType = self.getDmgSourceType()
            self.actResult.sourceId = self.getDmgSourceId()

    def getDmgSourceType(self):
        return gameconst.SourceType.Default

    def getDmgSourceId(self):
        return self.killerEntId

    def getCombatResult(self):
        return self.actResult

class FlowControllerCtx(ActionContext):
    actionType = ACTION_FLOW_CONTROLLER_CALLED

    __defaults__ = {'rawGameEntityId': 0,
                    'number': 0, 'radius': 0}

    def __init__(self, parentContext=None, **customProps):
        super(FlowControllerCtx, self).__init__(parentContext)
        if customProps:
            self.customDict.update(customProps)

    def __getattr__(self, item):
        try:
            return self.customDict[item]
        except KeyError:
            if item in self.__defaults__:
                return self.__defaults__[item]
            raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__.__name__, item))


class ClaimTaskCtx(object):
    actionType = ACTION_CLAIM_TASK

    def __init__(self, claimSrc=gameconst.ClaimTaskSrc.NORMAL, callbackUUID=0, teamId=0, teamBaseInfoDic=None,
                 seed=0, extra=None):
        super(ClaimTaskCtx, self).__init__()
        self.teamId = teamId
        self.teamBaseInfoDic = teamBaseInfoDic if teamBaseInfoDic else {}
        self.claimSrc = claimSrc
        self.seed = seed
        self.callbackUUID = callbackUUID
        self.extra = {} if not extra else extra

class CastCommonCtx(object):
    def __init__(self, castState, startTime, castTime, failedFunc='', failedArgs=None):
        self.castState = castState
        self.startTime = startTime
        self.castTime = castTime
        self.failedFunc = failedFunc
        self.failedArgs = failedArgs
        self.timer = 0

    def setCastTimer(self, timer):
        self.timer = timer

    def getCastTime(self, castType):
        if self.castTime > 0:
            return self.castTime
        else:
            return CONST.datas["teleportCastTime"]["value"]

    def callFailedFunc(self, owner):
        if self.failedFunc:
            getattr(owner, self.failedFunc)(*self.failedArgs)

    def notifyClient(self, box, castType, extraProps=None):
        extraProps = extraProps or {}
        if castType == gameconst.CastType.ride:
            pass
        elif castType == gameconst.CastType.teleportClientDelay:
            pass
        else:
            box.client.onTeleportCasting(castType, self.getCastTime(castType), self.startTime + self.getCastTime(castType))

    def clearTimerId(self):
        self.timer = 0

class TeleportInfoContext(object):
    def __init__(self, position, spaceNo, callback, args, startTime):
        self.position = position
        self.spaceNo = spaceNo
        self.callback = callback
        self.args = args
        self.startTime = startTime

    @property
    def endTime(self):
        return self.startTime + 120

    def getTeleportInfoCache(self):
        return self.position, self.spaceNo, self.callback, self.args

    def __str__(self):
        return f'pos:{self.position}, spaceNo:{self.spaceNo}, cb:{self.callback}, args:{self.args}, now:{self.startTime}, end:{self.endTime}'

class AddLingShouCtx(object):
    def __init__(self, reason, extra=None):
        self.pet = None
        self.reason = reason
        self.extra = {} if not extra else extra

    def setPet(self, pet):
        self.pet = pet

class PassiveSkillCtx(ActionContext):
    actionType = ACTION_PASSIVE_SKILL
    def __init__(self, objId, pSkillId, parentCtx=None):
        super(PassiveSkillCtx, self).__init__(parentCtx)
        self.objId = objId
        self.skillId = pSkillId                  #技能id

    def getDmgSourceType(self):
        return gameconst.SourceType.PassiveSkill

    def getDmgSourceId(self):
        return self.skillId

class BaseAffixActionCtx(ActionContext):
    actionType = ACTION_UNKNOWN
    def __init__(self, itemObj, affixVals, affixLv, lvGap=5, isLogin=False):
        super(BaseAffixActionCtx, self).__init__()
        self.affixItem = itemObj
        self.affixVals = affixVals
        self.affixLv = affixLv
        self.affixLevelGap = lvGap
        self.isLogin = isLogin

class EquipActionCtx(BaseAffixActionCtx):
    actionType = ACTION_EQUIP
    def __init__(self, equipItem, affixVals, affixLv, lvGap=5, isLogin=False):
        super(EquipActionCtx, self).__init__(equipItem, affixVals, affixLv, lvGap, isLogin)
        return

class AchievementCtx(object):
    def __init__(self, addNum=0, **kwargs):
        self.addNum = addNum
        for k, v in kwargs.items():
            setattr(self, k, v)


class DropEquipCtx(object):
    def __init__(self, score=0, quality=0, grade=0):
        self.score = score
        self.quality = quality
        self.grade = grade

class AureoleCtx(ActionContext):
    actionType = ACTION_AUREOLE
    def __init__(self, srcEntId, aureoleId, aureoleLevel, aureoleResult, parentCtx=None):
        super(AureoleCtx, self).__init__(parentCtx)
        self.aureoleId = aureoleId
        self.aureoleResult = aureoleResult
        self.srcEntId = srcEntId
        self.aureoleLevel = aureoleLevel

        if self.aureoleResult:
            self.aureoleResult.sourceType = self.getDmgSourceType()
            self.aureoleResult.sourceId = self.getDmgSourceId()

    def _lateReload(self):
        super(AureoleCtx, self)._lateReload()

        if self.aureoleResult:
            self.aureoleResult.reloadScript()

    def getDmgSourceType(self):
        return gameconst.SourceType.Aureole

    def getDmgSourceId(self):
        return self.aureoleId

    def getCombatResult(self):
        return self.aureoleResult

    @property
    def effectedEntIds(self):
        owner = KBEngine.entities.get(self.srcEntId)
        if not owner:
            return []

        aureoleVal = owner.aureoleDic.get(self.aureoleId)
        if aureoleVal:
            return aureoleVal.aureoleTargetIds

        return []


class CubeDurCtx(object):
    def __init__(self, avatarBase, failedLeaveCube=False):
        self.avatarBase = avatarBase
        self.failedLeaveCube = failedLeaveCube

    def done(self, isSuccess):
        if not isSuccess:
            if self.failedLeaveCube:
                self.avatarBase.cell.leaveCubeInternal(gameconst.DungeonSrcEnum.FROM_TIME_OUT)


