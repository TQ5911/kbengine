# -*- coding: utf-8 -*-
import KBEngine
import random
import gameconst
from KBEDebug import *

import buff_buff as B_BD
import effect_basic as EBD
import effect_event as EED
import effect_timer as ETD

import effect_basic
import effect_event
import effect_timer
import time
import actionContext
import effectEventCtx
import userType
import utils
import functools
import dataUtils
import gametimer
import gamedecorator

#effect的调用者
class EffectCaller(userType.UserSingleType):
    UNKOWN = 0
    BUFF = 1
    CRYSTAL = 2

    callerType = UNKOWN

    def __init__(self, callerInfo):
        self.__dict__.update(callerInfo)

    def getCaller(self, owner):
        pass

    def getEffectVal(self, owner, effectId, effectIndex):
        pass

    def getFromEntId(self, owner):
        pass

    def getEffectList(self, owner):
        pass


class BuffCaller(EffectCaller):
    callerType = EffectCaller.BUFF

    def getCaller(self, owner):
        return owner.buffMgrDic.getBuffVal(self.buffId, self.buffKey)

    def getFromEntId(self, owner):
        buffVal = self.getCaller(owner)
        return buffVal.releaseRoleId

    def getEffectVal(self, owner, effectId, effectIndex):
        buffVal = self.getCaller(owner)
        effectKey = utils.fetchBuffEffectKey(effectId, effectIndex)
        return buffVal.effectDic.get(effectKey)

    def getCallerKey(self, effectId, effectIndex):
        return 'effect_%s_%s_%s%s'%(self.buffId, self.buffKey, effectId, effectIndex)

    def getEffectList(self, owner):
        effectList = B_BD.datas.get(self.buffId, {}).get('effectList')
        return effectList

    def getCallerSrc(self):
        return gameconst.SourceType.SrcTpBuff

class EffectBase(userType.UserSingleType):
    EFFECT_TYPE = gameconst.EffecType.ENUM_EFFECT_UNKNOW

    def __init__(self, owner, callerInfo, effectId, effectIndex, extraInfo):
        self.effectId = effectId
        self.effectIndex = effectIndex
        self.isValid = True
        self.extraInfo = extraInfo

    #buff_buff/CSCID里effect对应的配置dict
    def getEffectDict(self, owner, callerInfo):
        effectList = callerInfo.getEffectList(owner)
        try:
            return effectList[self.effectIndex]
        except:
            self.isValid = False
            return {}

    def _getEffectEventKey(self, owner, callerInfo):
        return callerInfo.getCallerKey(self.effectId, self.effectIndex)

    def setupEffect(self, owner, callerInfo):
        raise NotImplementedError()

    def getEffectData(self):
        raise NotImplementedError()

    def getActionArgs(self, owner, callerInfo):
        effectDict = self.getEffectDict(owner, callerInfo)
        actionParam = effectDict.get('ActionParam')
        extraInfo = self.extraInfo
        args = {'self':owner}

        if callerInfo.callerType == EffectCaller.BUFF:
            buffVal = callerInfo.getCaller(owner)
            args['Layer'] = buffVal.level

        actionParam = actionParam(args) if callable(actionParam) else actionParam
        if actionParam:
            args['ActionParam'] = actionParam

        if extraInfo:
            for k,v in extraInfo.items():
                args[k] = v

        return args

    def onLoadedFromDB(self, callerInfo):
        pass

    def onOverlayBuff(self, owner, callerInfo):
        effectData = self.getEffectData()
        funcName = effectData.get('Func')
        if funcName == 'setStatus':
            owner.onOverlayStatus(self.getStatus(owner, callerInfo))

class BasicEffect(EffectBase):
    EFFECT_TYPE = gameconst.EffecType.ENUM_EFFECT_BASIC

    #effect不能独立存在，必须是被其他模块调用的，暂时只要buff，所以这里的callerinfo都是buffCaller
    def __init__(self, owner, callerInfo:EffectCaller, effectId, effectIndex, extraInfo):
        super(BasicEffect, self).__init__(owner, callerInfo, effectId, effectIndex, extraInfo)

    def setupEffect(self, owner, callerInfo):
        effectData = self.getEffectData()
        func = effectData.get('Func')
        func and getattr(self, func)(owner, callerInfo)

    #effect的配表数据
    def getEffectData(self):
        return EBD.datas.get(self.effectId, {})

    def makeTuple(self, val):
        if type(val) in (tuple, list):
            return val
        return (val,)

    def getRealValue(self, owner, callerInfo, value):
        args = self.getActionArgs(owner, callerInfo)

        if type(value) in (tuple, list):
            valueNew = [val(args) if callable(val) else val for val in value]
            return  tuple(valueNew)
        elif callable(value):
            value = value(args)
        return value

    def addFightParam(self, owner, callerInfo):
        effectDict = self.getEffectDict(owner, callerInfo)
        props = self.makeTuple(effectDict.get('Prop'))
        value = effectDict.get('Value')
        values = self.makeTuple(self.getRealValue(owner, callerInfo, value))

        for idx, propName in enumerate(props):
            if not propName:
                continue

            owner.onEffectAddProp(propName, values[idx], callerInfo, self.effectId, self.effectIndex)

    def undoAddFightParam(self, owner, callerInfo, isOverleap):
        effectDict = self.getEffectDict(owner, callerInfo)
        props = self.makeTuple(effectDict.get('Prop'))
        value = effectDict.get('Value')
        values = self.makeTuple(self.getRealValue(owner, callerInfo, value))

        for idx, propName in enumerate(props):
            if not propName:
                continue

            owner.onEffectAddProp(propName, -values[idx], callerInfo, self.effectId, self.effectIndex)

    #应该不能直接set要计算的属性，否则计算公式里变量修改后重算就把set的值覆盖了
    def setFightParam(self, owner, callerInfo):
        pass

    def undoSetFightParam(self, owner, callerInfo, isOverleap):
        pass

    def setUnControl(self, owner, callerInfo):
        owner.onEffectSetProp('baseStateRate', -1, callerInfo, self.effectId, self.effectIndex)

    def undoSetUnControl(self, owner, callerInfo, isOverleap):
        owner.onEffectUnsetProp('baseStateRate', callerInfo, self.effectId, self.effectIndex)

    def setSkillUnBroken(self, owner, callerInfo):
        owner.onEffectSetProp('skillBroken', 0, callerInfo, self.effectId, self.effectIndex)

    def undoSetSkillUnBroken(self, owner, callerInfo, isOverleap):
        owner.onEffectUnsetProp('skillBroken', callerInfo, self.effectId, self.effectIndex)

    def getStatus(self, owner, callerInfo):
        effectDict = self.getEffectDict(owner, callerInfo)
        return effectDict.get('Status')

    def setStatus(self, owner, callerInfo):
        status = self.getStatus(owner, callerInfo)
        if owner.checkConflictState(dataUtils.getStateEventId(status)):
            owner.setState(status)

    def checkEvent(self, owner, callerInfo):
        effectDict = self.getEffectDict(owner, callerInfo)
        eventId = effectDict.get('EventId')
        owner.checkConflictState(eventId, False, True)

    def undoSetStatus(self, owner, callerInfo, isOverleap):
        if not isOverleap:
            effectDict = self.getEffectDict(owner, callerInfo)
            status = effectDict.get('Status')
            owner.removeState(status)
        return 0

    def onAddSkill(self, owner, callerInfo, event, skillId):
        self.addSkillCd(owner, callerInfo, skillId)

    def addSkillCd(self, owner, callerInfo, toSkillId=0):
        effectDict = self.getEffectDict(owner, callerInfo)
        skillIds = effectDict.get('skillList')
        values = effectDict.get('Value')
        values = self.getRealValue(owner, callerInfo, values)
        isMul = effectDict.get('isMul',False)
        if len(skillIds)!=len(values):
            LOG_ERR('invalid addSkillCd args', callerInfo)
            return

        if isMul and any(value <= -1 for value in values):
            LOG_ERR('invalid addSkillCd args', values)
            return

        eventKey = self._getEffectEventKey(owner, callerInfo)

        pendingSkills = []
        for idx, skillId in enumerate(skillIds):
            if toSkillId and skillId!=toSkillId:
                continue

            skillVal = owner.skillDic.doGetSkill(skillId, reportErr=False)
            if skillVal:
                if isMul:
                    cd = skillVal.getSkillCfg(skillId).get('CD', 0)
                    cdDelta = cd * values[idx]
                else :
                    cdDelta = values[idx]
                owner.addSkillEffectCd(skillId, cdDelta)
            else:
                pendingSkills.append(skillId)

        if pendingSkills:
            owner.addListener('onAddSkill', eventKey, 'notifyEffectAddSkill', (callerInfo, self.effectId, self.effectIndex, pendingSkills))
        return

    def undoAddSkillCd(self, owner, callerInfo, isOverleap):
        effectDict = self.getEffectDict(owner, callerInfo)
        skillIds = effectDict.get('skillList')
        values = effectDict.get('Value')
        values = self.getRealValue(owner, callerInfo, values)
        isMul = effectDict.get('isMul', False)
        eventKey = self._getEffectEventKey(owner, callerInfo)
        for idx, skillId in enumerate(skillIds):
            skillVal = owner.skillDic.doGetSkill(skillId, reportErr=False)
            if skillVal:
                if isMul:
                    cd = skillVal.getSkillCfg(skillId).get('CD', 0)
                    cdDelta = cd * -values[idx]
                else :
                    cdDelta = -values[idx]
                owner.addSkillEffectCd(skillId, cdDelta)

        owner.removeListener('onAddSkill', eventKey)
        return 0

    def addShield(self, owner, callerInfo):
        effectDict = self.getEffectDict(owner, callerInfo)
        value = effectDict.get('Value')
        value = self.getRealValue(owner, callerInfo, value)
        type = effectDict.get('type')

        shieldTypeAbsolute = 1
        shieldTypeRatio = 2
        shieldTypeHybrid = 3

        if type == shieldTypeAbsolute:
            pass
        elif type == shieldTypeRatio:
            value = owner.fullHp * value
        elif type == shieldTypeHybrid:
            value = owner.fullHp * value[0] + value[1]

        if callerInfo.callerType in (EffectCaller.BUFF,):
            shieldId = callerInfo.buffId
        else:
            LOG_ERR('cannot get shieldId', callerInfo)
            return

        host = owner.getAvatar()
        if host:
            skillId = 0
            if callerInfo.callerType == EffectCaller.BUFF:
                buffVal = callerInfo.getCaller(owner)
                if buffVal and buffVal.rootContext:
                    if hasattr(buffVal.rootContext, 'skillId'):
                        skillId = buffVal.rootContext.skillId
            if skillId > 0:
                totalAddValue = 0
                ret, datas = host.getInscriptionEffects(skillId, gameconst.InscriptionEffectType.SHIELD_INCREASE_RATIO)
                if ret:
                    if len(datas) == 1:
                        addValue = datas[0]
                        totalAddValue = value * addValue
                        LOG_DBG("in addShield, inscription effect is triggered, skill_id:{0}, effect_type{1}, effect_value{2}", skillId, gameconst.InscriptionEffectType.SHIELD_INCREASE_RATIO, datas)

                ret, datas = host.getInscriptionEffects(skillId, gameconst.InscriptionEffectType.SHIELD_INCREASE_VALUE)
                if ret:
                    if len(datas) == 1:
                        addValue = datas[0]
                        totalAddValue = addValue
                        LOG_DBG("in addShield, inscription effect is triggered, skill_id:{0}, effect_type{1}, effect_value{2}", skillId, gameconst.InscriptionEffectType.SHIELD_INCREASE_VALUE, datas)


                value += totalAddValue

        owner.addShield(shieldId, gameconst.ShieldType.LIFE, value)
        return
    
    def addDefensiveShield(self, owner, callerInfo):
        effectDict = self.getEffectDict(owner, callerInfo)
        value = effectDict.get('hpValue')
        hpValue = self.getRealValue(owner, callerInfo, value)
        value = effectDict.get('reduceDmgRatio')
        reduceDmgRatio = self.getRealValue(owner, callerInfo, value)

        if callerInfo.callerType in (EffectCaller.BUFF,):
            shieldId = callerInfo.buffId
        else:
            LOG_ERR('cannot get shieldId', callerInfo)
            return

        host = owner.getAvatar()
        if host:
            skillId = 0
            if callerInfo.callerType == EffectCaller.BUFF:
                buffVal = callerInfo.getCaller(owner)
                if buffVal and buffVal.rootContext:
                    if hasattr(buffVal.rootContext, 'skillId'):
                        skillId = buffVal.rootContext.skillId
            if skillId > 0:
                totalAddValue = 0
                ret, datas = host.getInscriptionEffects(skillId, gameconst.InscriptionEffectType.SHIELD_INCREASE_RATIO)
                if ret:
                    if len(datas) == 1:
                        addValue = datas[0]
                        totalAddValue = hpValue * addValue
                        LOG_DBG("in addDefensiveShield, inscription effect is triggered, skill_id:{0}, effect_type{1}, effect_value{2}", skillId, gameconst.InscriptionEffectType.SHIELD_INCREASE_RATIO, datas)

                ret, datas = host.getInscriptionEffects(skillId, gameconst.InscriptionEffectType.SHIELD_INCREASE_VALUE)
                if ret:
                    if len(datas) == 1:
                        addValue = datas[0]
                        totalAddValue = addValue
                        LOG_DBG("in addDefensiveShield, inscription effect is triggered, skill_id:{0}, effect_type{1}, effect_value{2}", skillId, gameconst.InscriptionEffectType.SHIELD_INCREASE_VALUE, datas)


                hpValue += totalAddValue

        owner.addShield(shieldId, gameconst.ShieldType.REDUCE_DMG, hpValue, {'reduceDmgRatio':reduceDmgRatio})
        return

    def undoAddDefensiveShield(self, owner, callerInfo, isOverleap):
        owner.removeShield(callerInfo.buffId)
        return 0
    
    def undoAddShield(self, owner, callerInfo, isOverleap):
        owner.removeShield(callerInfo.buffId)
        return 0

    def removeEffect(self, owner, callerInfo, isOverleap=False):
        self.isValid = False

        effectData = self.getEffectData()
        funcName = effectData.get('Func')
        if funcName:
            undoFunc = 'undo'+funcName[:1].upper()+funcName[1:]
            getattr(self, undoFunc)(owner, callerInfo, isOverleap)


class EventEffect(EffectBase):
    EFFECT_TYPE = gameconst.EffecType.ENUM_EFFECT_BY_EVENT

    def __init__(self, owner, callerInfo, effectId, effectIndex, extraInfo):
        super(EventEffect, self).__init__(owner, callerInfo, effectId, effectIndex, extraInfo)
        effectData = self.getEffectData()
        triggerTime = 0
        if effectData.get('EventSourceType', 0) and effectData.get('EventCD', 0):
            triggerTime = owner.getEffectEventCDInfo(self.effectId)
        else:
            # 默认需求:不持久化的，即便CD非0也重置
            pass
        self.tNextTime = triggerTime
        #LOG_DBG('init EventEffect', self.effectId, self.tNextTime, utils.getNowTimeStr(self.tNextTime))

    def getEffectData(self):
        return EED.datas.get(self.effectId, {})

    def setupEffect(self, owner, callerInfo):
        effectData = self.getEffectData()
        action = effectData.get('Action')
        if not action:
            return

        eventName = effectData.get('Event')
        if not eventName:
            return

        self.isValid = True

        eventKey =self._getEffectEventKey(owner, callerInfo)
        owner.addListener(eventName, eventKey, 'notifyEffectActionEvent', (callerInfo, self.effectId, self.effectIndex))

    def _removeEventListener(self, owner, callerInfo):
        effectData = self.getEffectData()
        eventName = effectData.get('Event')
        if not eventName:
            return

        eventKey = self._getEffectEventKey(owner, callerInfo)
        owner.removeListener(eventName, eventKey)

    @gamedecorator.prevent_instance_reentry
    def onActionEvent(self, owner, callerInfo, event):
        LOG_DBG('onActionEvent: the event context -', event)

        if not self.isValid:
            return

        effectData = self.getEffectData()
        effectDict = self.getEffectDict(owner, callerInfo)
        if not effectData or not effectDict:
            return

        if owner.isDie() and 'onDeadLater' != event.name:
            return

        if self.tNextTime and time.time() < self.tNextTime:
            return

        prob = effectDict.get('Probability')
        caller = callerInfo.getCaller(owner)
        if prob:
            env = {'value':getattr(caller, 'randomValue', 0)}
            probVal = prob(env) if callable(prob) else prob
            if random.uniform(0, 1) > probVal:
                return

        if event.name == 'onSpecSkill' and effectDict.get('skillId') != event.eventContext.skillId:
            return
        elif event.name == 'onSelfBuff' and effectDict.get('BuffId') != event.eventContext.buffId:
            LOG_DBG('onActionEvent - "onSelfBuff" not trigger', effectDict, event.eventContext.buffId)
            return

        target = None
        targetType = effectData.get('Target')

        if targetType == 'self':
            target = owner
        elif targetType == 'other':
            #自己触发的事件ohter就是targetRoleId,别人触发的事件就是triggerRoleId
            otherId = event.targetRoleId if event.triggerRoleId==owner.id else event.triggerRoleId
            target = KBEngine.entities.get(otherId)
        elif targetType == 'buffReleaser':
            releaseRole = KBEngine.entities.get(event.triggerRoleId)
            if not (releaseRole and releaseRole.IsCombatUnit):
                return
            target = releaseRole

        #有可能不是combatUnit触发的事件，比如Creation
        _ret = None
        if (target and target.IsCombatUnit) or targetType=='None':
            argsDict = self.getActionArgs(owner, callerInfo)
            if event.eventContext is not effectEventCtx.EE_DEFAULT_CONTEXT:
                argsDict.update(vars(event.eventContext))

            action = effectData.get('Action')
            if action:
                if callerInfo.callerType in (EffectCaller.BUFF, ):
                    bufVal = callerInfo.getCaller(owner)
                    ctxBuilder = lambda r:actionContext.EventEffectCtx(callerInfo.getFromEntId(owner), owner.id, callerInfo.buffId, bufVal.level, bufVal.srcKey, self.effectId, argsDict, event.eventContext, r, bufVal.rootContext)
                else:
                    LOG_ERR('unsupported effect caller', callerInfo, self)
                    return
                _ret = owner.doCombatActions(action, owner, target, callerInfo.getFromEntId(owner), ctxBuilder)

        if _ret is None or _ret:
            self.tNextTime = time.time() + effectData.get('EventCD', 0)
            if effectData.get('EventSourceType', 0) and effectData.get('EventCD', 0):
                owner.updateEffectEventCDInfo(self.effectId, self.tNextTime)

    def removeEffect(self, owner, callerInfo, isOverleap=False):
        self.isValid = False
        self._removeEventListener(owner, callerInfo)

class TimerEffect(EffectBase):
    EFFECT_TYPE = gameconst.EffecType.ENUM_EFFECT_BY_TIMER

    def __init__(self, owner, callerInfo, effectId, effectIndex, extraInfo):
        self.effectTimer = 0
        self.tickCount = 0

        super(TimerEffect, self).__init__(owner,  callerInfo, effectId, effectIndex, extraInfo)

    def getEffectData(self):
        return ETD.datas.get(self.effectId, {})

    def setupEffect(self, owner, callerInfo):
        effectDict = self.getEffectDict(owner, callerInfo)
        if 'Count' not in effectDict or 'Interval' not in effectDict:
            LOG_ERR('TimerEffect needs Count and Interval',  callerInfo, self.effectId, effectDict)
            caller = callerInfo.getCaller(owner)
            caller.onSetupEffectError(callerInfo, self.effectId)
            return

        self.tickCount = 0
        self.isValid = True

        self.updateEffect(owner, callerInfo)
        LOG_DBG('setupEffect', self)

    def updateEffect(self, owner, callerInfo):
        self.effectTimer = 0
        if not self.isValid:
            return

        effectDict = self.getEffectDict(owner, callerInfo)

        interval = effectDict['Interval']
        self._doTickAction(owner, callerInfo)

        if self.isValid and interval > 0:
            if self.effectTimer:
                # 之所以会走到这里，大概率是因为_doTickAction里面调用了类似
                #overlaybuff的接口,导致里面 已经添加了timer
                return
            self.effectTimer = owner.addTimerCB(interval, 'updateTimeEffect', (callerInfo, self.effectId, self.effectIndex),

                                               gametimer.TIMER_TAG_UPDATE_TIME_EFFECT)

    def _doTickAction(self, owner, callerInfo):
        effectData = self.getEffectData()
        act = effectData.get('Action')
        if not act:
            return
        args = self.getActionArgs(owner, callerInfo)

        self.tickCount += 1
        args['tickCount'] = self.tickCount
        fromEntId = callerInfo.getFromEntId(owner)
        if callerInfo.callerType in (EffectCaller.BUFF,):
            bufVal = callerInfo.getCaller(owner)
            ctxBuilder = lambda r:actionContext.BuffEffectCtx(fromEntId, owner.id, bufVal.buffId, bufVal.level, bufVal.srcKey, self.effectId, args, r, bufVal.rootContext)
        else:
            LOG_ERR('unsupported effect caller', callerInfo, self.effectId)
            return

        owner.doCombatActions(act, owner, owner, fromEntId, ctxBuilder)

        effectDict = self.getEffectDict(owner, callerInfo)
        if effectDict['Count']>=0 and self.tickCount>=effectDict['Count']:
            self.isValid = False

    def removeEffect(self, owner, callerInfo, isOverleap=False):
        self.isValid = False

        if self.effectTimer > 0:
            owner.cancelTimerCB(self.effectTimer, gametimer.TIMER_TAG_UPDATE_TIME_EFFECT)
            self.effectTimer = 0

    def onLoadedFromDB(self, callerInfo):
        self.effectTimer = 0

    def onOverlayBuff(self, owner, callerInfo):
        self.tickCount = 0
        self.isValid = True
        if not self.effectTimer:
            self.updateEffect(owner, callerInfo)

    def resetTimerId(self):
        self.effectTimer = 0

def createEffect(owner, callerInfo, effectId, effectIndex, extraInfo):
    if effectId in EBD.datas:
        return BasicEffect(owner, callerInfo, effectId, effectIndex, extraInfo)
    elif effectId in EED.datas:
        return EventEffect(owner, callerInfo, effectId, effectIndex, extraInfo)
    elif effectId in ETD.datas:
        return TimerEffect(owner, callerInfo, effectId, effectIndex, extraInfo)
    else:
        raise Exception('invliad effect id %s %s %s %s'%(owner.id, callerInfo, effectId, effectIndex,))
