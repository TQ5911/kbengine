# -*- coding: utf-8 -*-
import KBEngine
import random
import gameconst
from KBEDebug import *

import buff_buff as B_BD
import effect_basic as EBD
import effect_event as EED
import effect_timer as ETD

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

    callerType = UNKOWN

    def __init__(self, callerInfo):
        self.__dict__.update(callerInfo)

    def getEffectVal(self, owner, effectId, effectIndex):
        pass

    def getCaller(self, owner):
        pass

    def getEffectList(self, owner):
        pass

    def getFromEntId(self, owner):
        pass


class BuffCaller(EffectCaller):
    callerType = EffectCaller.BUFF

    def getCaller(self, owner):
        return owner.buffMgrDic.getBuffVal(self.buffId, self.buffKey)

    def getFromEntId(self, owner):
        _buffVal = self.getCaller(owner)
        return _buffVal.releaseRoleId

    def getEffectVal(self, owner, effectId, effectIndex):
        _buffVal = self.getCaller(owner)
        effectKey = utils.fetchBuffEffectKey(effectId, effectIndex)
        return _buffVal.effectDict.get(effectKey)

    def getEffectList(self, owner):
        _effectList = B_BD.datas.get(self.buffId, {}).get('effectList')
        return _effectList

    def getCallerKey(self, effectId, effectIndex):
        return 'effect_%s_%s_%s%s'%(self.buffId, self.buffKey, effectId, effectIndex)

    def getCallerSrc(self):
        return gameconst.SourceType.SrcTpBuff

class EffectBase(userType.UserSingleType):
    EFFECT_TYPE = gameconst.EffecType.ENUM_EFFECT_UNKNOW

    def __init__(self, owner, callerInfo, effectId, effectIndex, extraInfo):
        self.effectIndex = effectIndex
        self.effectId = effectId
        self.extraInfo = extraInfo
        self.isValid = True

    #buff_buff/CSCID里effect对应的配置dict
    def getEffectDict(self, owner, callerInfo):
        _effectList = callerInfo.getEffectList(owner)
        try:
            return _effectList[self.effectIndex]
        except:
            self.isValid = False
            return {}

    def setupEffect(self, owner, callerInfo):
        raise NotImplementedError()

    def getEffectData(self):
        raise NotImplementedError()

    def _getEffectEventKey(self, owner, callerInfo):
        return callerInfo.getCallerKey(self.effectId, self.effectIndex)

    def getActionArgs(self, owner, callerInfo):
        _effectDict = self.getEffectDict(owner, callerInfo)
        actionParam = _effectDict.get('ActionParam')
        extraInfo = self.extraInfo
        _args = {'self':owner}

        if callerInfo.callerType == EffectCaller.BUFF:
            buffVal = callerInfo.getCaller(owner)
            _args['Layer'] = buffVal.level

        actionParam = actionParam(_args) if callable(actionParam) else actionParam
        if actionParam:
            _args['ActionParam'] = actionParam

        if extraInfo:
            for k,v in extraInfo.items():
                _args[k] = v

        return _args

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
    def __init__(self, owner, callerInfo:EffectCaller, effectId, effectIndex, extraInfo, **kwargs):
        super(BasicEffect, self).__init__(owner, callerInfo, effectId, effectIndex, extraInfo)

    #effect的配表数据
    def getEffectData(self):
        return EBD.datas.get(self.effectId, {})

    def setupEffect(self, owner, callerInfo):
        effectData = self.getEffectData()
        _func = effectData.get('Func')
        if _func:
            getattr(self, _func)(owner, callerInfo)

    def getRealValue(self, owner, callerInfo, value):
        _args = self.getActionArgs(owner, callerInfo)

        if type(value) in (tuple, list):
            valueNew = [val(_args) if callable(val) else val for val in value]
            return  tuple(valueNew)
        elif callable(value):
            value = value(_args)
        return value

    def makeTuple(self, val):
        if type(val) in (tuple, list):
            return val
        return (val,)

    def addFightParam(self, owner, callerInfo):
        _effectDict = self.getEffectDict(owner, callerInfo)
        props = self.makeTuple(_effectDict.get('Prop'))
        _value = _effectDict.get('Value')
        _values = self.makeTuple(self.getRealValue(owner, callerInfo, _value))

        for idx, propName in enumerate(props):
            if not propName:
                continue

            owner.onEffectAddProp(propName, _values[idx], 
                                  callerInfo, self.effectId, self.effectIndex)

    def undoAddFightParam(self, owner, callerInfo, isOverleap):
        _effectDict = self.getEffectDict(owner, callerInfo)
        props = self.makeTuple(_effectDict.get('Prop'))
        _value = _effectDict.get('Value')
        values = self.makeTuple(self.getRealValue(owner, callerInfo, _value))

        for _idx, propName in enumerate(props):
            if not propName:
                continue

            owner.onEffectAddProp(propName, -values[_idx], callerInfo, self.effectId, self.effectIndex)

    def undoSetFightParam(self, owner, callerInfo, isOverleap):
        pass

    #应该不能直接set要计算的属性，否则计算公式里变量修改后重算就把set的值覆盖了
    def setFightParam(self, owner, callerInfo):
        pass

    def undoSetUnControl(self, owner, callerInfo, isOverleap):
        owner.onEffectUnsetProp('baseStateRate', callerInfo, self.effectId, self.effectIndex)

    def setUnControl(self, owner, callerData):
        owner.onEffectSetProp('baseStateRate', -1, callerData, self.effectId, self.effectIndex)

    def undoSetSkillUnBroken(self, owner, callerData, isOverleap):
        owner.onEffectUnsetProp('skillBroken', callerData, self.effectId, self.effectIndex)

    def setSkillUnBroken(self, owner, callerData):
        owner.onEffectSetProp('skillBroken', 0, callerData, self.effectId, self.effectIndex)

    def getStatus(self, owner, callerData):
        effectDict = self.getEffectDict(owner, callerData)
        return effectDict.get('Status')

    def setStatus(self, owner, callerInfo):
        status = self.getStatus(owner, callerInfo)
        if owner.checkConflictState(dataUtils.getStateEventId(status)):
            owner.setState(status)

    def checkEvent(self, owner, callerInfo):
        effectDict = self.getEffectDict(owner, callerInfo)
        eventId = effectDict.get('EventId')
        owner.checkConflictState(eventId, False, True)

    def undoSetStatus(self, owner, callerData, isOverleap):
        if not isOverleap:
            effectDict = self.getEffectDict(owner, callerData)
            status = effectDict.get('Status')
            owner.removeState(status)
        return 0

    def onAddSkill(self, owner, callerData, event, skillId):
        self.addSkillCd(owner, callerData, skillId)

    def addSkillCd(self, owner, callerInfo, toSkillId=0):
        _effectDict = self.getEffectDict(owner, callerInfo)
        skillIds = _effectDict.get('skillList')
        values = _effectDict.get('Value')
        values = self.getRealValue(owner, callerInfo, values)
        isMul = _effectDict.get('isMul',False)
        if len(skillIds)!=len(values):
            LOG_ERR('invalid addSkillCd args', callerInfo)
            return

        if isMul and any(value <= -1 for value in values):
            LOG_ERR('invalid addSkillCd args', values)
            return

        _eventKey = self._getEffectEventKey(owner, callerInfo)

        pendingSkills = []
        for _idx, skillId in enumerate(skillIds):
            if toSkillId and skillId!=toSkillId:
                continue

            skillVal = owner.skillDic.doGetSkill(skillId, reportErr=False)
            if skillVal:
                if isMul:
                    cd = skillVal.getSkillCfg(skillId).get('CD', 0)
                    cdDelta = cd * values[_idx]
                else :
                    cdDelta = values[_idx]
                owner.addSkillEffectCd(skillId, cdDelta)
            else:
                pendingSkills.append(skillId)

        if pendingSkills:
            owner.addListener(
                'onAddSkill', 
                _eventKey, 
                'notifyEffectAddSkill', 
                (callerInfo, self.effectId, self.effectIndex, pendingSkills,),
            )
        return

    def undoAddSkillCd(self, owner, callerInfo, isOverleap):
        _effectDict = self.getEffectDict(owner, callerInfo)
        skillIds = _effectDict.get('skillList')
        values = _effectDict.get('Value')
        values = self.getRealValue(owner, callerInfo, values)
        isMul = _effectDict.get('isMul', False)
        eventKey = self._getEffectEventKey(owner, callerInfo)
        for _idx, skillId in enumerate(skillIds):
            skillVal = owner.skillDic.doGetSkill(skillId, reportErr=False)
            if skillVal:
                if isMul:
                    cd = skillVal.getSkillCfg(skillId).get('CD', 0)
                    cdDelta = cd * -values[_idx]
                else :
                    cdDelta = -values[_idx]
                owner.addSkillEffectCd(skillId, cdDelta)

        owner.removeListener('onAddSkill', eventKey)
        return 0

    def addShield(self, owner, callerData):
        _effectDict = self.getEffectDict(owner, callerData)
        value = _effectDict.get('Value')
        value = self.getRealValue(owner, callerData, value)
        type = _effectDict.get('type')

        _shieldTypeAbsolute = 1
        _shieldTypeRatio = 2
        _shieldTypeHybrid = 3

        if type == _shieldTypeAbsolute:
            pass
        elif type == _shieldTypeRatio:
            value = owner.fullHp * value
        elif type == _shieldTypeHybrid:
            value = owner.fullHp * value[0] + value[1]

        if callerData.callerType in (EffectCaller.BUFF,):
            shieldId = callerData.buffId
        else:
            LOG_ERR('cannot get shieldId', callerData)
            return

        host = owner.getAvatar()
        if host:
            skillId = 0
            if callerData.callerType == EffectCaller.BUFF:
                buffVal = callerData.getCaller(owner)
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

    def cantUseSkillTag(self, owner, callerInfo):
        effectDict = self.getEffectDict(owner, callerInfo)
        value = effectDict.get('Value')
        tags = self.getRealValue(owner, callerInfo, value)
        LOG_DBG("cantUseSkillTag", value, tags, owner.id)
        owner.forbidSkillByTags(tags)

    def undoCantUseSkillTag(self, owner, callerInfo, isOverleap):
        effectDict = self.getEffectDict(owner, callerInfo)
        value = effectDict.get('Value')
        tags = self.getRealValue(owner, callerInfo, value)
        LOG_DBG("undoCantUseSkillTag", value, tags, owner.id)
        owner.unForbidSkillByTags(tags)

    def undoAddDefensiveShield(self, owner, callerInfo, isOverleap):
        owner.removeShield(callerInfo.buffId)
        return 0
    
    def undoAddShield(self, owner, callerData, isOverleap):
        owner.removeShield(callerData.buffId)
        return 0

    def removeEffect(self, owner, callerData, isOverleap=False):
        self.isValid = False

        effectData = self.getEffectData()
        _funcName = effectData.get('Func')
        if _funcName:
            undoFunc = 'undo'+_funcName[:1].upper()+_funcName[1:]
            getattr(self, undoFunc)(owner, callerData, isOverleap)


class EventEffect(EffectBase):
    EFFECT_TYPE = gameconst.EffecType.ENUM_EFFECT_BY_EVENT

    def __init__(self, owner, callerData, effectId, effectIndex, extraInfo):
        super(EventEffect, self).__init__(owner, callerData, effectId, effectIndex, extraInfo)
        effectData = self.getEffectData()
        triggerTime = 0
        if effectData.get('EventSourceType', 0) and effectData.get('EventCD', 0):
            triggerTime = owner.getEffectEventCDInfo(self.effectId)
        else:
            # 默认需求:不持久化的，即便CD非0也重置
            pass
        self.tNextTime = triggerTime
        #LOG_DBG('init EventEffect', self.effectId, self.tNextTime, utils.getNowTimeStr(self.tNextTime))

    def setupEffect(self, owner, callerInfo):
        _effectData = self.getEffectData()
        action = _effectData.get('Action')
        if not action:
            return

        _eventName = _effectData.get('Event')
        if not _eventName:
            return

        self.isValid = True

        eventKey =self._getEffectEventKey(owner, callerInfo)
        owner.addListener(_eventName, eventKey, 'notifyEffectActionEvent', (callerInfo, self.effectId, self.effectIndex))

    def getEffectData(self):
        return EED.datas.get(self.effectId, {})

    def _removeEventListener(self, owner, callerInfo):
        effectData = self.getEffectData()
        _eventName = effectData.get('Event')
        if not _eventName:
            return

        eventKey = self._getEffectEventKey(owner, callerInfo)
        owner.removeListener(_eventName, eventKey)

    @gamedecorator.prevent_instance_reentry
    def onActionEvent(self, owner, callerInfo, event):
        LOG_DBG('onActionEvent: the event context -', event)

        if not self.isValid:
            return

        _effectData = self.getEffectData()
        _effectDict = self.getEffectDict(owner, callerInfo)
        if not _effectData or not _effectDict:
            return

        if owner.isDie() and 'onDeadLater' != event.name:
            return

        if self.tNextTime and time.time() < self.tNextTime:
            return

        _prob = _effectDict.get('Probability')
        caller = callerInfo.getCaller(owner)
        if _prob:
            env = {'value':getattr(caller, 'randomValue', 0)}
            probVal = _prob(env) if callable(_prob) else _prob
            if random.uniform(0, 1) > probVal:
                return

        if event.name == 'onSpecSkill' and _effectDict.get('skillId') != event.eventContext.skillId:
            return

        elif event.name == 'onSelfBuff' and _effectDict.get('BuffId') != event.eventContext.buffId:
            LOG_DBG('onActionEvent - "onSelfBuff" not trigger', _effectDict, event.eventContext.buffId)
            return

        target = None
        _targetType = _effectData.get('Target')

        if _targetType == 'self':
            target = owner
        elif _targetType == 'other':
            #自己触发的事件ohter就是targetRoleId,别人触发的事件就是triggerRoleId
            _otherId = event.targetRoleId if event.triggerRoleId==owner.id else event.triggerRoleId
            target = KBEngine.entities.get(_otherId)
        elif _targetType == 'buffReleaser':
            releaseRole = KBEngine.entities.get(event.triggerRoleId)
            if not (releaseRole and releaseRole.IsCombatUnit):
                return
            target = releaseRole

        #有可能不是combatUnit触发的事件，比如Creation
        _ret = None
        if (target and target.IsCombatUnit) or _targetType=='None':
            _argsDict = self.getActionArgs(owner, callerInfo)
            if event.eventContext is not effectEventCtx.EE_DEFAULT_CONTEXT:
                _argsDict.update(vars(event.eventContext))

            _action = _effectData.get('Action')
            if _action:
                if callerInfo.callerType in (EffectCaller.BUFF, ):
                    _bufVal = callerInfo.getCaller(owner)
                    _ctxBuilder = lambda r:actionContext.EventEffectCtx(
                        callerInfo.getFromEntId(owner), 
                        owner.id, 
                        callerInfo.buffId, 
                        _bufVal.level, 
                        _bufVal.srcKey, 
                        self.effectId, 
                        _argsDict, 
                        event.eventContext, 
                        r, 
                        _bufVal.rootContext)

                else:
                    LOG_ERR('unsupported effect caller', callerInfo, self)
                    return
                _ret = owner.doCombatActions(_action, owner, target, callerInfo.getFromEntId(owner), _ctxBuilder)

        if _ret is None or _ret:
            self.tNextTime = time.time() + _effectData.get('EventCD', 0)
            if _effectData.get('EventSourceType', 0) and _effectData.get('EventCD', 0):
                owner.updateEffectEventCDInfo(self.effectId, self.tNextTime)

    def removeEffect(self, owner, callerData, isOverleap=False):
        self.isValid = False
        self._removeEventListener(owner, callerData)

class TimerEffect(EffectBase):
    EFFECT_TYPE = gameconst.EffecType.ENUM_EFFECT_BY_TIMER

    def __init__(self, owner, callerData, effectId, effectIndex, extraInfo):
        self.effectTimer = 0
        self.tickCount = 0

        super(TimerEffect, self).__init__(owner,  callerData, effectId, effectIndex, extraInfo)

    def setupEffect(self, owner, callerData):
        effectDict = self.getEffectDict(owner, callerData)
        if 'Count' not in effectDict or 'Interval' not in effectDict:
            LOG_ERR('TimerEffect needs Count and Interval',  callerData, self.effectId, effectDict)
            caller = callerData.getCaller(owner)
            caller.onSetupEffectError(owner)
            return

        self.tickCount = 0
        self.isValid = True

        self.updateEffect(owner, callerData)
        LOG_DBG('setupEffect', self)

    def getEffectData(self):
        return ETD.datas.get(self.effectId, {})

    def updateEffect(self, owner, callerData):
        self.effectTimer = 0
        if not self.isValid:
            return

        effectDict = self.getEffectDict(owner, callerData)

        interval = effectDict['Interval']
        self._doTickAction(owner, callerData)

        if self.isValid and interval > 0:
            if self.effectTimer:
                # 之所以会走到这里，大概率是因为_doTickAction里面调用了类似
                #overlaybuff的接口,导致里面 已经添加了timer
                return
            self.effectTimer = owner.addTimerCB(interval, 'updateTimeEffect', (callerData, self.effectId, self.effectIndex),

                                               gametimer.TIMER_TAG_UPDATE_TIME_EFFECT)

    def _doTickAction(self, owner, callerInfo):
        _effectData = self.getEffectData()
        act = _effectData.get('Action')
        if not act:
            return
        args = self.getActionArgs(owner, callerInfo)

        self.tickCount += 1
        args['tickCount'] = self.tickCount
        _fromEntId = callerInfo.getFromEntId(owner)
        if callerInfo.callerType in (EffectCaller.BUFF,):
            _bufVal = callerInfo.getCaller(owner)
            ctxBuilder = lambda r:actionContext.BuffEffectCtx(
                _fromEntId, 
                owner.id, 
                _bufVal.buffId, 
                _bufVal.level, 
                _bufVal.srcKey, 
                self.effectId, 
                args, 
                r, 
                _bufVal.rootContext)
        else:
            LOG_ERR('unsupported effect caller', callerInfo, self.effectId)
            return

        owner.doCombatActions(act, owner, owner, _fromEntId, ctxBuilder)

        _effectDict = self.getEffectDict(owner, callerInfo)
        if _effectDict['Count']>=0 and self.tickCount>=_effectDict['Count']:
            self.isValid = False

    def removeEffect(self, owner, callerData, isOverleap=False):
        self.isValid = False

        if self.effectTimer > 0:
            owner.cancelTimerCB(self.effectTimer, gametimer.TIMER_TAG_UPDATE_TIME_EFFECT)
            self.effectTimer = 0

    def onOverlayBuff(self, owner, callerInfo):
        self.tickCount = 0
        self.isValid = True
        if not self.effectTimer:
            self.updateEffect(owner, callerInfo)

    def resetTimerId(self):
        self.effectTimer = 0

    def onLoadedFromDB(self, callerInfo):
        self.effectTimer = 0

def createEffect(owner, callerData, effectId, effectIndex, extraInfo):
    if effectId in EBD.datas:
        return BasicEffect(owner, callerData, effectId, effectIndex, extraInfo)
    elif effectId in EED.datas:
        return EventEffect(owner, callerData, effectId, effectIndex, extraInfo)
    elif effectId in ETD.datas:
        return TimerEffect(owner, callerData, effectId, effectIndex, extraInfo)
    else:
        raise Exception('invliad effect id %s %s %s %s'%(owner.id, callerData, effectId, effectIndex,))

