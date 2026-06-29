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

BUFF_ACTIONS = (ACTION_BUFF_TICK, ACTION_BUFF_END, ACTION_BUFF_EFFECT)

class ActionContext(userType.UserSingleType):
    actionType = ACTION_UNKNOWN

    def __init__(self, parentContext=None):
        self.actionStage = 0
        self.parentContext = parentContext
        self.customDict = {}

    def getSrcEntity(self):
        return None

    def __str__(self):
        return '%s %s' % (self.actionType, str(vars(self)))

    def setCustomVar(self, name, val):
        self.customDict[name] = val

    def _lateReload(self):
        super(ActionContext, self)._lateReload()
        if self.parentContext:
            self.parentContext.reloadScript()

    def getCustomVar(self, name):
        return self.customDict.get(name)

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
    def __init__(self, casterEntId, skillId, skillArgs, useTargetId, 
                 effectedEntIds=None, skillObj=None, skillResult=None, 
                 castBySkill=0, isSucc=None, parentCtx=None, actionProgress=0,
                 isLastActionStage=False, isClient=False, checkInRange=True):

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
        self.actionProgress = actionProgress                 #���ܽ���
        self.isLastActionStage = isLastActionStage           #�Ƿ����һ��actionstage
        self.checkInRange = checkInRange
        self.isClient = isClient
        self.lastBlinkPos = None

        if self.skillResult:
            self.skillResult.sourceType = self.getDmgSourceType()
            self.skillResult.sourceId = self.getDmgSourceId()
    
    def isClientSkill(self, maxTimes=4):
        if maxTimes == 0:
            return False

        if self.isClient:
            return True

        if self.parentContext and self.parentContext.actionType == ACTION_USE_SKILL:
            return self.parentContext.isClientSkill(maxTimes - 1)

        return False

    def getDmgSourceType(self):
        return gameconst.SourceType.SrcTpSkill

    def getCombatResult(self):
        return self.skillResult

    def getDmgSourceId(self):
        return self.skillId

    def _lateReload(self):
        super(UseSkillCtx, self)._lateReload()

        if self.skillResult:
            self.skillResult.reloadScript()

        if self.skillObj:
            self.skillObj.reloadScript()

    def getSrcEntity(self):
        return KBEngine.entities.get(self.casterEntId)


class SkillCommonCtx(ActionContext):
    actionType = ACTION_SKILL_COMMON
    def __init__(self, skillId, parentCtx=None, **kwargs):
        super(SkillCommonCtx, self).__init__(parentCtx)
        self.skillId = skillId                  #����id


class CreationCombatCtx(ActionContext):
    actionType = ACTION_CREATION_LOOP
    def __init__(self, creationEntId, effectedEntIds, creationResult, parentCtx=None, loopTimes=0, context=None):
        super(CreationCombatCtx, self).__init__(parentCtx)
        self.creationEntId = creationEntId      #����entity id
        self.effectedEntIds = effectedEntIds    #��������Ŀ��
        self.creationResult = creationResult
        self.loopTimes = loopTimes
        self.parentContext = context

        if self.creationResult:
            self.creationResult.sourceId = self.getDmgSourceId()
            self.creationResult.sourceType = self.getDmgSourceType()

    def _lateReload(self):
        super(CreationCombatCtx, self)._lateReload()

        if self.creationResult:
            self.creationResult.reloadScript()

    def getDmgSourceType(self):
        return gameconst.SourceType.SrcTpCreation

    @property
    def creationId(self):
        return self.getDmgSourceId()

    def getDmgSourceId(self):
        e = KBEngine.entities.get(self.creationEntId)
        return e.creationId if e else 0

    def getSrcEntity(self):
        return KBEngine.entities.get(self.creationEntId)

    def getCombatResult(self):
        return self.creationResult


class BuffRefreshCtx(ActionContext):
    actionType = ACTION_BUFF_TICK
    def __init__(self, srcEntId, ownerEntId, buffId, buffLevel, srcKey, 
                 buffResult, parentCtx=None, **kwargs):
        super(BuffRefreshCtx, self).__init__(parentCtx)
        self.ownerEntId = ownerEntId
        self.srcEntId = srcEntId
        self.buffId = buffId
        self.srcKey = srcKey
        self.buffResult = buffResult
        self.buffLevel = buffLevel

        if self.buffResult:
            self.buffResult.sourceId = self.getDmgSourceId()
            self.buffResult.sourceType = self.getDmgSourceType()

    def _lateReload(self):
        super(BuffRefreshCtx, self)._lateReload()

        if not self.buffResult:
            return

        self.buffResult.reloadScript()

    def getDmgSourceId(self):
        return self.buffId

    def getDmgSourceType(self):
        return gameconst.SourceType.SrcTpBuff

    def getCombatResult(self):
        return self.buffResult

    def getSrcEntity(self):
        return KBEngine.entities.get(self.srcEntId)

    def getBuffObject(self):
        _owner = self.getOwnerEntity()
        if not _owner:
            return None

        return _owner.getBuffByBuffId(self.buffId, self.srcKey)

    def getOwnerEntity(self):
        return KBEngine.entities.get(self.ownerEntId)


class BuffEndContext(ActionContext):
    actionType = ACTION_BUFF_END
    def __init__(self, srcEntId, ownerEntId, buffId, buffLevel, srcKey, removeType, buffResult, parentCtx=None):
        super(BuffEndContext, self).__init__(parentCtx)
        self.ownerEntId = ownerEntId
        self.srcEntId = srcEntId
        self.buffId = buffId
        self.srcKey = srcKey
        self.buffLevel = buffLevel
        self.buffResult = buffResult
        self.removeType = removeType

        if self.buffResult:
            self.buffResult.sourceId = self.getDmgSourceId()
            self.buffResult.sourceType = self.getDmgSourceType()

    def _lateReload(self):
        super(BuffEndContext, self)._lateReload()

        if not self.buffResult:
            return

        self.buffResult.reloadScript()

    def getDmgSourceType(self):
        return gameconst.SourceType.SrcTpBuff

    def getCombatResult(self):
        return self.buffResult

    def getDmgSourceId(self):
        return self.buffId

    def getOwnerEntity(self):
        return KBEngine.entities.get(self.ownerEntId)

    def getBuffObject(self):
        _owner = self.getOwnerEntity()
        if not _owner:
            return None

        return _owner.getBuffByBuffId(self.buffId, self.srcKey)

    def getSrcEntity(self):
        return KBEngine.entities.get(self.srcEntId)


class BuffEffectCtx(ActionContext):
    actionType = ACTION_BUFF_EFFECT
    def __init__(self, srcEntId, ownerEntId, buffId, buffLevel, srcKey,\
                 effectId, args, effectResult, parentCtx=None, **kwargs):
        super(BuffEffectCtx, self).__init__(parentCtx)
        self.ownerEntId = ownerEntId
        self.srcEntId = srcEntId
        self.buffId = buffId
        self.srcKey = srcKey
        self.buffLevel = buffLevel
        self.effectId = effectId
        self.effectResult = effectResult
        self.args = gameclass.DummyObject(**args)

        if self.effectResult:
            self.effectResult.sourceId = self.getDmgSourceId()
            self.effectResult.sourceType = self.getDmgSourceType()

    def _lateReload(self):
        super(BuffEffectCtx, self)._lateReload()

        self.args.reloadScript()

        if self.effectResult:
            self.effectResult.reloadScript()

    def getDmgSourceId(self):
        return self.buffId

    def getDmgSourceType(self):
        return gameconst.SourceType.SrcTpBuff

    def getCombatResult(self):
        return self.effectResult

    def getOwnerEntity(self):
        return KBEngine.entities.get(self.ownerEntId)

    def getSrcEntity(self):
        return KBEngine.entities.get(self.srcEntId)

    def getBuffObject(self):
        _owner = self.getOwnerEntity()
        if not _owner:
            return None

        return _owner.getBuffByBuffId(self.buffId, self.srcKey)


#�¼�������effect��������
class EventEffectCtx(BuffEffectCtx):
    actionType = ACTION_EVENT_EFFECT
    def __init__(self, srcEntId, ownerEntId, buffId, buffLv, srcKey, effectId,\
                 args, eventContext, effectResult, parentCtx=None, **kwargs):

        super(EventEffectCtx, self).__init__(
            srcEntId, ownerEntId, buffId, 
            buffLv, srcKey, effectId, args, effectResult, parentCtx,)
        self.eventContext = eventContext

    def _lateReload(self):
        super(EventEffectCtx, self)._lateReload()

        if self.eventContext:
            self.eventContext.reloadScript()

    def getSrcEntity(self):
        return KBEngine.entities.get(self.srcEntId)


class ChangeSkillSlotCtx(ActionContext):
    actionType = ACTION_CHANGE_SKILL_SLOT
    def __init__(self, skillId, parentCtx=None, **kwargs):
        super(ChangeSkillSlotCtx, self).__init__(parentCtx)
        self.skillId = skillId                  #����id

class AiActionCtx(ActionContext):
    actionType = ACTION_AI_ACTION
    def __init__(self, creepbaseId, parentCtx=None):
        super(AiActionCtx, self).__init__(parentCtx)
        self.creepbaseId = creepbaseId


class UseItemCtx(object):
    actionType = ACTION_USE_ITEM

    def __init__(self, targetId=0, argsList=None, withMailId=0,\
                 bindType=gameconst.ItemBindType.BINDTYPE_NOT_SPECIFIED,
                 itemObj=None):
        self.targetId = targetId
        if argsList is None:
            self.argsList = []
        else:
            self.argsList = argsList

        self.pendingOpId = 0
        self.withMailId = withMailId
        self.bindType = bindType
        self.itemObj = itemObj

    def _lateReload(self):
        super(UseItemCtx, self)._lateReload()
        return


class UseBoxTypeItemCtx(object):
    actionType = ACTION_USE_BOX_TYPE_ITEM

    def __init__(self, targetId=0, argsList=(), withMailId=0, awardVal=None,\
                 bindType=gameconst.ItemBindType.BINDTYPE_NOT_SPECIFIED, **kwargs):
        self.targetId = targetId
        if argsList:
            self.argsList = argsList
        else:
            self.argsList = []

        self.pendingOpId = 0
        self.withMailId = withMailId
        self.awardVal = awardVal
        self.bindType = bindType

    def _lateReload(self):
        super(UseBoxTypeItemCtx, self)._lateReload()
        return


class UseItemHealContext(ActionContext):
    actionType = ACTION_USE_ITEM_HEAL

    def __init__(self, itemId, srcEntId=0, itemResult=None, parentCtx=None, **kwargs):
        super(UseItemHealContext, self).__init__(parentCtx)
        self.srcEntId = srcEntId
        self.itemId = itemId
        self.itemResult = itemResult
        if self.itemResult:
            self.itemResult.sourceId = self.getDmgSourceId()
            self.itemResult.sourceType = self.getDmgSourceType()

    def getDmgSourceType(self):
        return gameconst.SourceType.SrcTpItem

    def getSrcEntity(self):
        return KBEngine.entities.get(self.srcEntId)

    def getCombatResult(self):
        return self.itemResult

    def getDmgSourceId(self):
        return self.itemId


class FlowCtrlCtx(ActionContext):
    actionType = ACTION_FLOW_CONTROLLER_CALLED

    __defaults__ = {
        'rawGameEntityId': 0,
        'number': 0, 
        'radius': 0,
    }

    def __init__(self, parentContext=None, **kwargs):
        super(FlowCtrlCtx, self).__init__(parentContext)
        if kwargs:
            self.customDict.update(kwargs)

    def __getattr__(self, itemProp):
        try:
            return self.customDict[itemProp]
        except KeyError:
            if itemProp in self.__defaults__:
                return self.__defaults__[itemProp]
            raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__.__name__, itemProp))


class ClaimTaskCtx(object):
    actionType = ACTION_CLAIM_TASK

    def __init__(self, claimSrc=gameconst.ClaimTaskSrcEnum.TASK_SRC_NORMAL, callbackUUID=0, teamId=0, teamBaseInfoDic=None,
                 seed=0, extra=None, **kwargs):
        super(ClaimTaskCtx, self).__init__()
        if teamBaseInfoDic:
            self.teamBaseInfoDic = teamBaseInfoDic
        else:
            self.teamBaseInfoDic = {}
        self.teamId = teamId

        self.claimSrc = claimSrc
        self.seed = seed
        self.callbackUUID = callbackUUID
        self.extra = {} if not extra else extra


class CastCommonCtx(object):
    def __init__(self, castState, startTime, castTime, failedFunc='', failedArgs=None):
        self.startTime = startTime
        self.castState = castState
        self.castTime = castTime
        self.failedFunc = failedFunc
        self.timer = 0
        self.failedArgs = failedArgs

    def getCastTime(self, castType):
        if self.castTime > 0:
            return self.castTime
        else:
            return CONST.datas["teleportCastTime"]["value"]

    def setCastTimer(self, timer):
        self.timer = timer

    def callFailedFunc(self, owner):
        if not self.failedFunc:
            return

        getattr(owner, self.failedFunc)(*self.failedArgs)

    def clearTimerId(self):
        self.timer = 0

    def notifyClient(self, box, castType, extraProps=None):
        if castType == gameconst.CastEnum.ride:
            pass
        elif castType == gameconst.CastEnum.teleportClientDelay:
            pass
        else:
            box.client.onTeleportCasting(castType, self.getCastTime(castType), self.startTime + self.getCastTime(castType))


class TeleportInfoContext(object):
    def __init__(self, position, spaceNo, callback, args, startTime):
        self.spaceNo = spaceNo
        self.position = position
        self.callback = callback
        self.startTime = startTime
        self.args = args

    def getTeleportInfoCache(self):
        return self.position, self.spaceNo, self.callback, self.args

    @property
    def endTime(self):
        return self.startTime + 120

    def __str__(self):
        return f'pos:{self.position}, spaceNo:{self.spaceNo}, cb:{self.callback}, args:{self.args}, now:{self.startTime}, end:{self.endTime}'

class AddLingShouCtx(object):
    def __init__(self, reason, extra=None):
        self.reason = reason
        self.pet = None
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
        return gameconst.SourceType.SrcTpPassiveSkill

    def getDmgSourceId(self):
        return self.skillId

class BaseAffixActionCtx(ActionContext):
    actionType = ACTION_UNKNOWN
    def __init__(self, itemObj, affixVals, affixLv, lvGap=5, isLogin=False, **kwargs):
        super(BaseAffixActionCtx, self).__init__()
        self.affixVals = affixVals
        self.affixItem = itemObj
        self.affixLv = affixLv
        self.isLogin = isLogin
        self.affixLevelGap = lvGap

class EquipActionCtx(BaseAffixActionCtx):
    actionType = ACTION_EQUIP
    def __init__(self, equipItem, affixVals, affixLv, lvGap=5, isLogin=False, **kwargs):
        super(EquipActionCtx, self).__init__(equipItem, affixVals, affixLv, lvGap, isLogin)

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
    def __init__(self, srcEntId, aureoleId, aureoleLevel, aureoleResult, 
                 parentCtx=None, **kwargs):
        super(AureoleCtx, self).__init__(parentCtx)
        self.aureoleResult = aureoleResult
        self.aureoleId = aureoleId
        self.srcEntId = srcEntId
        self.aureoleLevel = aureoleLevel

        if self.aureoleResult:
            self.aureoleResult.sourceId = self.getDmgSourceId()
            self.aureoleResult.sourceType = self.getDmgSourceType()

    def _lateReload(self):
        super(AureoleCtx, self)._lateReload()

        if not self.aureoleResult:
            return

        self.aureoleResult.reloadScript()

    def getDmgSourceId(self):
        return self.aureoleId

    def getDmgSourceType(self):
        return gameconst.SourceType.SrcTpAureole

    @property
    def effectedEntIds(self):
        _owner = KBEngine.entities.get(self.srcEntId)
        if not _owner:
            return []

        aureoleVal = _owner.auraDic.get(self.aureoleId)
        if aureoleVal:
            return aureoleVal.aureoleTargetIds

        return []

    def getCombatResult(self):
        return self.aureoleResult


class CubeDurCtx(object):
    def __init__(self, avatarBase, failedLeaveCube=False):
        self.avatarBase = avatarBase
        self.failedLeaveCube = failedLeaveCube

    def done(self, isSuccess):
        if not isSuccess:
            if self.failedLeaveCube:
                self.avatarBase.cell.leaveCubeInternal(gameconst.DunSrcEnum.FROM_TIME_OUT, True)

class CreateSummonCtx(ActionContext):
    actionType = ACTION_UNKNOWN
    def __init__(self, summonLv, skillLv, parentCtx=None):
        super(CreateSummonCtx, self).__init__(parentCtx)
        self.summonLv = summonLv
        self.skillLv = skillLv

