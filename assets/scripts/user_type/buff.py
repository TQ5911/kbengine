# -*- coding: utf-8 -*-
import KBEngine
import gameconst
from KBEDebug import *
import buff_buff
import time
import gametimer
import utils

import effect
import userType
import actionContext
import effectEventCtx
import functools
import gameengine
import struct


class ShieldVal(userType.UserSingleType):
    def __init__(self, buffId, shieldType, shieldMaxValue, shieldValue, shieldEffects = None):
        self.buffId = buffId
        self.shieldMaxValue = shieldMaxValue
        self.shieldValue = int(shieldValue)
        self.absorbedVal = 0
        if not shieldEffects:
            self.shieldEffects = {}
        else:
            self.shieldEffects = shieldEffects
        self.shieldType = shieldType

    def doAbsorbDmg(self, val):
        iVal = int(val)
        if iVal > self.shieldValue:
            iVal = self.shieldValue
        self.shieldValue -= iVal
        self.absorbedVal += iVal
        return iVal

    def getShieldValue(self):
        return self.shieldValue
    
    def getShieldMaxValue(self):
        return self.shieldMaxValue
    
    def addShieldValue(self, val):
        self.shieldValue += val
        self.shieldMaxValue += val
    
    def getShieldType(self):
        return self.shieldType
    
    def getShieldReduceDmgRatio(self):
        return self.shieldEffects and self.shieldEffects.get('reduceDmgRatio', 0)

class Shields(userType.UserDictType):
    def _lateReload(self):
        super(Shields, self)._lateReload()

        for _v in self.values():
            _v.reloadScript()


class ClientBuffVal(userType.UserSingleType):
    def __init__(self, buffId, level, srcKey, endTimeStamp, duration):
        self.buffId = buffId
        self.srcKey = srcKey
        self.level = level
        self.duration = duration
        self.endTimeStamp = endTimeStamp

    def getClientStream(self):
        return struct.pack('<IQIdf', self.buffId, self.srcKey, self.level,\
                           self.endTimeStamp, self.duration)


class ServerBuffs(userType.UserDictType):
    """
    SERVER_BUFFS
    Skillmanager.buffMgrDic
    """
    def __init__(self):
        super(ServerBuffs, self).__init__()
        self.buffTagsSet = set()

    def getClientData(self, null, buffIds=None):
        _buffsDict = {'buffs':[]}
        buffIds = buffIds or self.keys()
        for buffId in buffIds:
            buffMap = self[buffId]
            for _, buffVal in buffMap.items():
                _buffsDict['buffs'].append(buffVal.getClientStream())
        return _buffsDict

    def getClientBuffIds(self):
        _buffIdsList = []
        for _buffId in self.keys():
            buffMap = self[_buffId]
            _endTime = None
            for _buffVal in buffMap.values():
                _curBuffEndTime = _buffVal.getBuffEndTime()
                if _endTime is None:
                    _endTime = _curBuffEndTime
                elif _endTime < _curBuffEndTime:
                    _endTime = _curBuffEndTime

            buffIdVal = {
                "buffId": _buffId,
                "endTimeStamp": _endTime,
            }
            _buffIdsList.append(buffIdVal)
        return _buffIdsList

    def getBuffVal(self, buffId, buffSrcKey):
        if buffId not in self:
            return None

        return self[buffId].get(buffSrcKey)

    def doAddBuff(self, owner, buffId, buffLevel, duration, releaseRoleId, 
                  releaseRoleName, releaseRoleGbId, srcType, srcKey, rootContext,kwargs):

        owner.debugCombatMsg('doAddBuff: buffId:%s, buffLevel:%s, duration:%s, releaseRoleId:%s, releaseRoleName:%s, buffSrcType:%s, srcKey:%s, rootContext:%s',
                                     buffId, buffLevel, duration, releaseRoleId, releaseRoleName, srcType, srcKey, rootContext)
        self.setdefault(buffId, {})
        isAddBySelf = True if releaseRoleId == owner.id else False
        _buffVal = Buff(buffId, buffLevel, duration, releaseRoleId, srcType, srcKey, rootContext,
                       releaseRoleName=releaseRoleName,releaseRoleGbId = releaseRoleGbId, isAddBySelf=isAddBySelf)
        self[buffId][srcKey] = _buffVal
        if not kwargs :
            _buffVal.initBuff(owner)
        else :
            _buffVal.initBuff(owner,**kwargs)
        self.buffTagsSet = _buffVal.addBuffTags(self.buffTagsSet)

        return _buffVal

    def hasBuffTag(self, tag):
        return tag in self.buffTagsSet

    #暂时仅用于上线时移除过期buff，这时buff还未加在身上，不需要执行移除action
    def removeWithoutCalc(self, buffId, srcKeys):
        if buffId not in self:
            return

        for _buffKey in srcKeys:
            self[buffId].pop(_buffKey)

        if not self[buffId]:
            self.pop(buffId, None)

        self.buffTagsSet.clear()
        for _buffMap in self.values():
            for buff in _buffMap.values():
                self.buffTagsSet = buff.addBuffTags(self.buffTagsSet)

    def removeBuff(self, owner, buffId, buffSrcKeys, isFinished, removeType):
        if buffId not in self:
            return

        LOG_DBG("trace removeBuff ", buffId, buffSrcKeys, isFinished, removeType)
        owner.debugCombatMsg('removeBuff: buffId:%s, buffSrcKeys:%s, isFinished:%s, removeType:%s',
                                     buffId, buffSrcKeys, isFinished, removeType)
        if not buffSrcKeys:
            buffSrcKeys = list(self[buffId].keys())

        if not isinstance(buffSrcKeys, (list, tuple)):
            buffSrcKeys = (buffSrcKeys,)

        _removedKeys = []
        _isModify = False
        for buffKey in buffSrcKeys:
            #buff action中可能会移除这个buffKey
            if buffKey not in self[buffId]:
                if removeType!=gameconst.RemoveTypeEnum.RTEnumEndByAction:
                    gameengine.panicStack('cannot find buffKey', buffKey)
                continue

            _buffVal = self[buffId][buffKey]
            if _buffVal.isRemoving:
                continue

            if removeType==gameconst.RemoveTypeEnum.RTEnumEndByTime and not _buffVal.isBuffTimeEnd(owner):
                _buffVal.delayRemoveBuff(owner, isFinished, removeType)
                continue

            _isModify = True
            _buffVal.isRemoving = True
            _buffVal.onBuffRemove(owner, isFinished, removeType)

            #onBuffRemove里可能会触发别的action，会移除这个buff，这里需要再判一次
            if buffId in self:
                self[buffId].pop(buffKey, None)

            _removedKeys.append(buffKey)

        if not _isModify:
            return

        #onBuffRemove里可能会触发别的action，会移除这个buff，这里需要再判一次
        if buffId in self:
            #如果srcKeys还不为空
            if self[buffId]:
                not owner.isDestroyed and owner.allClientsOnRemoveBuff(buffId, _removedKeys)
            else:
                self.pop(buffId)
                not owner.isDestroyed and owner.allClientsOnRemoveBuff(buffId, [])

        self.buffTagsSet.clear()
        for buffMap in self.values():
            for buff in buffMap.values():
                self.buffTagsSet = buff.addBuffTags(self.buffTagsSet)

    def checkValidOnLogin(self, owner,tsLastOffline):
        rmBuffs = {}
        for buffId, buffMap in self.items():
            _invalidKeys = []
            _buffSrcKey = owner.getBuffSrcKey(buffId)
            for _buffKey, _buffVal in buffMap.items():
                if _buffVal.getBuffDuration()>0 :
                    if _buffVal.getBuffRemainTimeOffline(owner,tsLastOffline) <= 0:
                        _invalidKeys.append(_buffKey)
                    else:
                        _buffVal.duration=_buffVal.getBuffRemainTimeOffline(owner,tsLastOffline)
                        _buffVal.tStartTime=time.time()

                if _buffSrcKey and _buffKey == _buffSrcKey:
                    _buffVal.releaseRoleId = owner.id

            if _invalidKeys:
                rmBuffs[buffId] = _invalidKeys

        for _buffId, _srcKeys in rmBuffs.items():
            owner.removeBuffWithoutCalc(_buffId, _srcKeys)

    def _lateReload(self):
        super(ServerBuffs, self)._lateReload()

        for buffMap in self.values():
            for _v in buffMap.values():
                _v.reloadScript()

        return


class Buff(userType.UserSingleType):
    def __init__(self, buffId, level, duration, releaseRoleId, srcType,\
                 srcKey, rootContext, randomValue=0, removeTimerId=0,\
                 releaseRoleName="",releaseRoleGbId="", isAddBySelf=False):

        self.level = int(level)
        self.buffId = buffId
        self.tStartTime = time.time()
        self.releaseRoleId = releaseRoleId
        self.srcType = srcType
        self.srcKey = srcKey
        self.effectDict = {}
        self.rootContext = rootContext              #最终来源上下文
        self.removeTimerId = removeTimerId
        self.beatNum = 0
        self.skillNum = 0
        self.attNum = 0
        self.usrDefineDic = {}
        self.duration = duration
        self.randomValue = randomValue
        self.releaseRoleName = releaseRoleName
        self.releaseRoleGbId = releaseRoleGbId
        self.isPause = False
        self.isRemoving = False
        self.isAddBySelf = isAddBySelf

    def _lateReload(self):
        super(Buff, self)._lateReload()

        if self.rootContext:
            self.rootContext.reloadScript()

        for _v in self.effectDict.values():
            _v.reloadScript()

        return

    @classmethod
    def clearAllCache(cls):
        cls.getBuffEffectList.cache_clear()
        cls.getBuffCfg.cache_clear()
        cls.getKind.cache_clear()
        cls.fetchDeadDontRemove.cache_clear()
        cls.getEndBySkill.cache_clear()
        cls.getEndByTime.cache_clear()
        cls.getEndNumByBeat.cache_clear()
        cls.getEndByAtt.cache_clear()
        cls.getEndByBeatAction.cache_clear()
        cls.getEndAction.cache_clear()
        cls.getEndByDieRemoveAction.cache_clear()
        cls.getEndByTimeAction.cache_clear()
        cls.getTag.cache_clear()
        cls.getRefreshAction.cache_clear()
        cls.getOffLineLast.cache_clear()
        cls.getBuffName.cache_clear()
        cls.getIfSend.cache_clear()
        cls.getSchoolTag.cache_clear()
        cls.getOfflineKeep.cache_clear()

    @property
    def releaseRole(self):
        return KBEngine.entities.get(self.releaseRoleId)

    def getContext(self):
        return self.rootContext
    
    def getBuffRemainTime(self):
        _duration = self.getBuffDuration()
        if _duration<=0:
            return float('inf')

        endTime = _duration + self.tStartTime

        if endTime > time.time():
            return endTime - time.time() 
        else:
            return 0.0

    def getBuffRemainTimeOffline(self,owner,tsLastOffline):
        if not owner.IsAvatar:
            tsLastOffline = 0

        duration = self.getBuffDuration()
        if duration <= 0:
            return float('inf')

        _endTime = duration + self.tStartTime
        if _endTime < tsLastOffline:
            return 0.0

        if self.isOffLineLast():
            return _endTime - time.time() if _endTime > time.time() else 0.0
        else:
            return _endTime - tsLastOffline

    def getBuffEndTime(self):
        if self.getBuffDuration() > 0:
            return time.time() + self.getBuffRemainTime()

        return 0

    def _getBufferEventKey(self):
        return 'buff_%s_%s'%(self.buffId, self.srcKey)

    def initBuff(self, owner, **extraInfo):
        _eventKey = self._getBufferEventKey()
        if self.getEndBySkill(self.buffId):
            owner.addListener('onSkill', _eventKey, 'onEventSkill', (self.buffId, self.srcKey))
        if self.getEndNumByBeat(self.buffId):
            owner.addListener('onBeat', _eventKey, 'onEventBeat', (self.buffId, self.srcKey))
        if self.getEndByAtt(self.buffId):
            owner.addListener('onHit', _eventKey, 'onEventHit', (self.buffId, self.srcKey))

        self.getEffectList(owner, **extraInfo)

        _duration = self.getBuffDuration()
        if _duration <= 0:
            return

        _remainTime = self.getBuffRemainTime()
        if _remainTime > 0:
            self.removeTimerId = owner.addTimerCB(
                _remainTime, 
                'removeBuff', 
                (self.buffId, (self.srcKey,), True, gameconst.RemoveTypeEnum.RTEnumEndByTime),
                gametimer.TIMER_TAG_DELAY_REMOVE_BUFF)

        else:
            LOG_ERR('initBuff error', _duration, _remainTime, self.tStartTime, self.buffId)
            owner.removeBuff(self.buffId, (self.srcKey,), False, gameconst.RemoveTypeEnum.RTEnumDefault)

    def _getEffectCaller(self):
        if self.srcType == gameconst.BuffSrcTypeEnum.Combat:
            return effect.BuffCaller({
                'buffKey':self.srcKey,
                'buffId':self.buffId, 
            })

    def getEffectList(self, owner, **extraInfo):
        if self.srcType == gameconst.BuffSrcTypeEnum.Combat:
            effectList = self.getBuffEffectList(self.buffId)
        else:
            gameengine.panicStack('invalid buff src:', self.srcType, self.buffId)
            return

        if not effectList:
            return

        _buffCaller = self._getEffectCaller()
        for i, effectDict in enumerate(effectList):
            effectId = effectDict['EffectId']
            effectKey = utils.fetchBuffEffectKey(effectId, i)
            self.effectDict[effectKey] = effect.createEffect(owner, _buffCaller, effectId, i, extraInfo)
            self.effectDict[effectKey].setupEffect(owner, _buffCaller)

            #effect可能把owner打死了，buff没有了，不再加别的effect
            if not _buffCaller.getCaller(owner):
                break

    #duration: 0:永久 >0:duration <0:读表
    def getBuffDuration(self):
        if self.duration < 0:
            return float(self.getEndByTime(self.buffId) or 0)
        else:
            return self.duration

    def onSetupEffectError(self, owner):
        owner.removeBuff(self.buffId, (self.srcKey,))

    @staticmethod
    @functools.lru_cache(1024)
    def getBuffEffectList(buffId):
        return Buff.getBuffCfg(buffId).get('effectList', ())

    @staticmethod
    @functools.lru_cache(1024)
    def getBuffCfg(buffId):
        return buff_buff.datas[buffId]

    @staticmethod
    @functools.lru_cache(1024)
    def getKind(buffId):
        return Buff.getBuffCfg(buffId).get('kind')

    @staticmethod
    @functools.lru_cache(1024)
    def fetchDeadDontRemove(buffId):
        return Buff.getBuffCfg(buffId).get('deadDontRemove')

    @staticmethod
    @functools.lru_cache(1024)
    def getEndByTime(buffId):
        return Buff.getBuffCfg(buffId).get('endByTime')

    @staticmethod
    @functools.lru_cache(1024)
    def getEndBySkill(buffId):
        return Buff.getBuffCfg(buffId).get('endBySkill')

    @staticmethod
    @functools.lru_cache(1024)
    def getEndNumByBeat(buffId):
        return Buff.getBuffCfg(buffId).get('endByBeat')

    @staticmethod
    @functools.lru_cache(1024)
    def getEndByAtt(buffId):
        return Buff.getBuffCfg(buffId).get('endByAtt')

    @staticmethod
    @functools.lru_cache(1024)
    def getEndAction(buffId):
        return Buff.getBuffCfg(buffId).get('endAction')

    @staticmethod
    @functools.lru_cache(1024)
    def getEndByBeatAction(buffId):
        return Buff.getBuffCfg(buffId).get('endByBeatAction')

    @staticmethod
    @functools.lru_cache(1024)
    def getEndByDieRemoveAction(buffId):
        return Buff.getBuffCfg(buffId).get('endByDieRemoveAction')

    @staticmethod
    @functools.lru_cache(1024)
    def getEndByTimeAction(buffId):
        return Buff.getBuffCfg(buffId).get('endByTimeAction')

    @staticmethod
    @functools.lru_cache(1024)
    def getRefreshAction(buffId):
        return Buff.getBuffCfg(buffId).get('refreshAction')

    @staticmethod
    @functools.lru_cache(1024)
    def getTag(buffId):
        return Buff.getBuffCfg(buffId).get('tag')

    @staticmethod
    @functools.lru_cache(1024)
    def getOffLineLast(buffId):
        return Buff.getBuffCfg(buffId).get('offLineLast')

    @staticmethod
    @functools.lru_cache(1024)
    def getBuffName(buffId):
        return Buff.getBuffCfg(buffId).get('name', '')

    def getEffect(self, effectKey):
        return self.effectDict.get(effectKey, None)

    @staticmethod
    @functools.lru_cache(1024)
    def getOfflineKeep(buffId):
        return Buff.getBuffCfg(buffId).get('offLineKeep', False)

    @staticmethod
    @functools.lru_cache(1024)
    def getIfSend(buffId):
        return Buff.getBuffCfg(buffId).get('ifSend', False)

    @staticmethod
    @functools.lru_cache(1024)
    def getSchoolTag(buffId):
        return Buff.getBuffCfg(buffId).get('classTag', 0)

    def addBuffTags(self, buffTagsSet):
        tags = Buff.getTag(self.buffId)
        if tags:
            for tag in tags:
                buffTagsSet.add(tag)
        return buffTagsSet

    def hasBuffTag(self, tag):
        _tags = self.getTag(self.buffId)
        if _tags and tag in _tags:
            return True
        return False

    def overlayBuff(self, owner, toLevel, duration):
        LOG_DBG("trace overlayBuff 1")
        _oldLevel = self.level

        if _oldLevel == toLevel:
            remainTime = self.getBuffRemainTime()
            _newDura = duration
            if duration < 0:
                _newDura = float(self.getEndByTime(self.buffId) or 0)

            if _newDura <= 0:
                _newDura = float('inf')

            LOG_DBG("trace overlayBuff 2 ", _newDura, remainTime, self)

        self.tStartTime = time.time()
        self.beatNum = 0
        self.skillNum = 0
        self.attNum = 0

        if self.removeTimerId > 0:
            owner.cancelTimerCB(self.removeTimerId, gametimer.TIMER_TAG_DELAY_REMOVE_BUFF)
            self.removeTimerId = 0

        self.duration, duration = duration, self.getBuffDuration()

        if duration > 0:
            LOG_DBG("trace overlayBuff 3")
            buffCaller = self._getEffectCaller()
            effectValues = list(self.effectDict.values())
            for _effectVal in effectValues:
                _effectVal.onOverlayBuff(owner, buffCaller)

            self.removeTimerId = owner.addTimerCB(duration, 'removeBuff', (self.buffId, (self.srcKey,), True,
                                                                        gameconst.RemoveTypeEnum.RTEnumEndByTime),
                                                                        gametimer.TIMER_TAG_DELAY_REMOVE_BUFF)

        if _oldLevel != toLevel:
            LOG_DBG("trace overlayBuff 4")
            buffCaller = self._getEffectCaller()
            effectValues = list(self.effectDict.values())
            for _effectVal in effectValues:

                if _effectVal.EFFECT_TYPE == gameconst.EffecType.ENUM_EFFECT_BASIC:
                    #先按旧的等级移除effect
                    _effectVal.removeEffect(owner, buffCaller, isOverleap=True)

                elif _effectVal.EFFECT_TYPE == gameconst.EffecType.ENUM_EFFECT_BY_EVENT:
                    pass

                elif _effectVal.EFFECT_TYPE == gameconst.EffecType.ENUM_EFFECT_BY_TIMER:
                    _effectVal.removeEffect(owner, buffCaller, isOverleap=True)

            self.level = int(toLevel)

            #按新等级添加effect
            effectKeys = list(self.effectDict.keys())
            for effectKey in effectKeys:
                #setupEffect可能kill目标导致移除buff，清空effectDic
                _effectVal = self.effectDict.get(effectKey)
                if not _effectVal:
                    continue

                if _effectVal.EFFECT_TYPE == gameconst.EffecType.ENUM_EFFECT_BASIC:
                    _effectVal.setupEffect(owner, buffCaller)

                elif _effectVal.EFFECT_TYPE == gameconst.EffecType.ENUM_EFFECT_BY_EVENT:
                    pass

                elif _effectVal.EFFECT_TYPE == gameconst.EffecType.ENUM_EFFECT_BY_TIMER:
                    _effectVal.setupEffect(owner, buffCaller)

            _refreshAction = self.getRefreshAction(self.buffId)
            if _refreshAction:
                _ctxFunc = lambda r:actionContext.BuffRefreshCtx(
                    self.releaseRoleId, owner.id, self.buffId, self.level,\
                    self.srcKey, r, self.rootContext)

                owner.doCombatActions(_refreshAction, owner, owner, owner.id, _ctxFunc)
            LOG_DBG("trace overlayBuff ", self)

    def isBuffTimeEnd(self, owner):
        buffCaller = self._getEffectCaller()
        for _effectVal in self.effectDict.values():
            if not isinstance(_effectVal, effect.TimerEffect):
                continue

            effectDict = _effectVal.getEffectDict(owner, buffCaller)
            if effectDict['Count'] >= 0 and _effectVal.isValid:
                LOG_DBG('cannot remove buff by time now, will remove later', _effectVal)
                return False

        return True

    #有TimerEffect的buff必须保证effect tick的次数到达配置次数后才可以销毁，否则延迟移除
    def delayRemoveBuff(self, owner, isFinished, removeType):
        if self.removeTimerId > 0:
            owner.cancelTimerCB(self.removeTimerId, gametimer.TIMER_TAG_DELAY_REMOVE_BUFF)

        self.removeTimerId = owner.addTimerCB(
            0.3, 
            'removeBuff', 
            (self.buffId, (self.srcKey,), isFinished, removeType),
            gametimer.TIMER_TAG_DELAY_REMOVE_BUFF)

    def onBuffRemove(self, owner, isFinished, removeType):
        #一定要放在最开始cancel，否则在action后cancel可能会把action加上去的timer退出了
        #因为这里保存的id已经是无效的了，可能被引擎重用
        if self.removeTimerId > 0:
            owner.cancelTimerCB(self.removeTimerId, gametimer.TIMER_TAG_DELAY_REMOVE_BUFF)
            self.removeTimerId = 0

        _eventKey = self._getBufferEventKey()
        if self.getEndBySkill(self.buffId):
            owner.removeListener('onSkill', _eventKey)
        if self.getEndNumByBeat(self.buffId):
            owner.removeListener('onBeat', _eventKey)
        if self.getEndByAtt(self.buffId):
            owner.removeListener('onHit', _eventKey)

        if isFinished:
            owner.onEffectEventCall(
                'onBuffEnd', 
                owner.id, 
                owner.id, 
                effectEventCtx.BuffEventContext(self.buffId, self.getTag(self.buffId), removeType))

        _eventAction = None
        _endAction = self.getEndAction(self.buffId)
        if removeType == gameconst.RemoveTypeEnum.RTEnumEndByBeat and self.getEndByBeatAction(self.buffId):
            _eventAction = self.getEndByBeatAction(self.buffId)
        elif removeType == gameconst.RemoveTypeEnum.RTEnumEndByDead and self.getEndByDieRemoveAction(self.buffId):
            _eventAction = self.getEndByDieRemoveAction(self.buffId)
        elif removeType == gameconst.RemoveTypeEnum.RTEnumEndByTime:
            _eventAction = self.getEndByTimeAction(self.buffId)

        _ctxFunc = lambda r:actionContext.BuffEndContext(self.releaseRoleId, owner.id, self.buffId, self.level, self.srcKey, removeType, r, self.rootContext)
        _actFunc = lambda actionOwner, target, ctx: (_eventAction and _eventAction(owner, owner, ctx), _endAction and _endAction(owner, owner, ctx))

        owner.doCombatActions(_actFunc, owner, owner, owner.id, _ctxFunc)

        buffCaller = self._getEffectCaller()
        for effectId, effect in self.effectDict.items():
            LOG_DBG("remove effect ", effect)
            effect.removeEffect(owner, buffCaller)
        self.effectDict.clear()

    def onEventSkill(self, owner, event, buffId):
        if buffId != self.buffId:
            return

        self.skillNum = self.skillNum + 1
        if self.getEndBySkill(self.buffId) > 0\
                and self.skillNum >= self.getEndBySkill(self.buffId):
            owner.removeListener('onSkill', self._getBufferEventKey())
            owner.removeBuff(self.buffId, (self.srcKey,), True, gameconst.RemoveTypeEnum.RTEnumEndBySkill)

    def onEventBeat(self, owner, event, buffId):
        if buffId != self.buffId:
            return

        self.beatNum += 1
        if self.getEndNumByBeat(self.buffId) > 0 and self.beatNum >= self.getEndNumByBeat(self.buffId):
            owner.removeListener('onBeat', self._getBufferEventKey())
            owner.removeBuff(self.buffId, (self.srcKey,), True, gameconst.RemoveTypeEnum.RTEnumEndByBeat)

    def onEventHit(self, owner, event, buffId):
        if buffId != self.buffId:
            return

        self.attNum = self.attNum + 1
        if self.attNum >= self.getEndByAtt(self.buffId) > 0:
            owner.removeListener('onHit', self._getBufferEventKey())
            owner.removeBuff(self.buffId, (self.srcKey,), True, gameconst.RemoveTypeEnum.RTEnumEndByAtt)

    def isRemoveOnDead(self):
        if self.fetchDeadDontRemove(self.buffId):
            return False
        return True

    def resetTimerId(self):
        self.removeTimerId = 0

    def isOffLineLast(self):
        if self.getOffLineLast(self.buffId):
            return True
        return False

    def getClassTag(self, owner):
        _classTag = self.getSchoolTag(self.buffId)
        if _classTag == -1 and owner.IsAICombatUnit:
            battleType = owner.getBattleType()
            if battleType == gameconst.BattleType.physics:
                _classTag = gameconst.SCHOOL_PHYSICAL
            elif battleType == gameconst.BattleType.magic:
                _classTag = gameconst.SCHOOL_MAGIC
        return _classTag

    def onRestored(self, owner):
        if self.isAddBySelf:
            self.releaseRoleId = owner.id

    def getClientVal(self, owner):
        return ClientBuffVal(self.buffId, self.level, self.srcKey, self.getBuffEndTime(), self.getBuffDuration())

    def getClientData(self, owner):
        return {
            'srcKey':self.srcKey,
            'buffId':self.buffId,
            'level':self.level,
            'duration': self.getBuffDuration(),
            'endTimeStamp': self.getBuffEndTime(),
        }

    def getClientStream(self):
        return struct.pack('<IQIdf', self.buffId, self.srcKey, self.level,\
                           self.getBuffEndTime(), self.getBuffDuration())

    def getSavedDict(self):
        return {
            'skillNum': self.skillNum,
            'tStartTime': self.tStartTime,
            'beatNum': self.beatNum,
            'duration': self.duration,
            'attNum': self.attNum,
            'effectDict': self.effectDict,
            'randomValue' : self.randomValue,
            'isAddBySelf': self.isAddBySelf,
            'rootContext': self.rootContext,
        }

    def loadSavedDict(self, data):
        if 'skillNum' in data:
            self.skillNum = data['skillNum']
        if 'tStartTime' in data:
            self.tStartTime = data['tStartTime']
        if 'beatNum' in data:
            self.beatNum = data['beatNum']
        if 'duration' in data:
            self.duration = data['duration']
        if 'attNum' in data:
            self.attNum = data['attNum']
        if 'effectDict' in data:
            self.effectDict = data['effectDict']
        if 'randomValue' in data:
            self.randomValue = data['randomValue']
        if 'rootContext' in data:
            self.rootContext = data['rootContext']
        if 'isAddBySelf' in data:
            self.isAddBySelf = data['isAddBySelf']


