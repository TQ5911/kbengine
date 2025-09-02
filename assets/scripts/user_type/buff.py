# -*- coding: utf-8 -*-
import KBEngine
import random
import gameconst
from KBEDebug import *
import buff_buff
import time
import utils
import gametimer

import effect
import userType
import actionContext
import effectEventCtx
import gameengine
import functools
import struct

import formula

class ShieldVal(userType.UserSoleType):
    def __init__(self, buffId, shieldValue):
        self.buffId = buffId
        self.shieldValue = int(shieldValue)
        self.absorbedVal = 0

    def doAbsorbDmg(self, val):
        val = int(val)
        if val>self.shieldValue:
            val = self.shieldValue
        self.shieldValue -= val
        self.absorbedVal += val
        return val


class Shields(userType.UserDictType):
    def _lateReload(self):
        super(Shields, self)._lateReload()

        for v in self.values():
            v.reloadScript()

        return


class ClientBuffVal(userType.UserSoleType):
    def __init__(self, id, level, srcKey, endTimeStamp, duration):
        self.buffId = id
        self.srcKey = srcKey
        self.level = level
        self.endTimeStamp = endTimeStamp
        self.duration = duration

    def getClientStream(self):
        return struct.pack('<IQIdf', self.buffId, self.srcKey, self.level, self.endTimeStamp, self.duration)


class ClientBuffs(userType.UserDictType):
    def _lateReload(self):
        super(ClientBuffs, self)._lateReload()

        for buffMap in self.values():
            for v in buffMap.values():
                v.reloadScript()

        return


class ServerBuffs(userType.UserDictType):
    def __init__(self):
        super(ServerBuffs, self).__init__()
        self.buffTagSet = set()

    def getClientData(self, owner, buffIds=None):
        buffsDict = {'buffs':[]}
        buffIds = buffIds or self.keys()
        for buffId in buffIds:
            buffMap = self[buffId]
            for buffKey, buffVal in buffMap.items():
                buffsDict['buffs'].append(buffVal.getClientStream())
        return buffsDict

    def getClientBuffIds(self):
        buffIdsList = []
        for buffId in self.keys():
            buffMap = self[buffId]
            buffIdVal = {
                "buffId": buffId,
                "srcKeys": list(buffMap.keys())
            }
            buffIdsList.append(buffIdVal)
        return buffIdsList

    def getBuffVal(self, buffId, buffSrcKey):
        if buffId not in self:
            return

        return self[buffId].get(buffSrcKey)

    def doAddBuff(self, owner, buffId, level, duration, releaseRoleId,releaseRoleName,releaseRoleGbId, srcType, srcKey, rootContext,kwargs):
        DEBUG_MSG("trace doAddBuff ", buffId, level, duration, releaseRoleId,releaseRoleName,releaseRoleGbId, srcType, srcKey, rootContext,kwargs)
        self.setdefault(buffId, {})
        isAddBySelf = True if releaseRoleId == owner.id else False
        buffVal = Buff(buffId, level, duration, releaseRoleId, srcType, srcKey, rootContext,
                       releaseRoleName=releaseRoleName,releaseRoleGbId = releaseRoleGbId, isAddBySelf=isAddBySelf)
        self[buffId][srcKey] = buffVal
        if not kwargs :
            buffVal.initBuff(owner)
        else :
            buffVal.initBuff(owner,**kwargs)
        self.buffTagSet = buffVal.addBuffTags(self.buffTagSet)
        DEBUG_MSG('added buff', buffVal)
        return buffVal

    def hasBuffTag(self, tag):
        return tag in self.buffTagSet

    #暂时仅用于上线时移除过期buff，这时buff还未加在身上，不需要执行移除action
    def removeWithoutCalc(self, owner, buffId, srcKeys):
        if buffId not in self:
            return

        for buffKey in srcKeys:
            self[buffId].pop(buffKey)

        if not self[buffId]:
            self.pop(buffId, None)

        self.buffTagSet.clear()
        for buffMap in self.values():
            for buff in buffMap.values():
                self.buffTagSet = buff.addBuffTags(self.buffTagSet)

    def removeBuff(self, owner, buffId, buffSrcKeys, isFinished, removeType):
        if buffId not in self:
            return
        DEBUG_MSG("trace removeBuff ", buffId, buffSrcKeys, isFinished, removeType)
        buffSrcKeys = buffSrcKeys or list(self[buffId].keys())
        if type(buffSrcKeys) not in (tuple, list):
            buffSrcKeys = (buffSrcKeys,)
        removedKeys = []
        isModify = False
        for buffKey in buffSrcKeys:
            #buff action中可能会移除这个buffKey
            if buffKey not in self[buffId]:
                if removeType!=gameconst.RemoveType.EndByAction:
                    ERROR_MSG('cannot find buffKey', buffKey)
                    import traceback
                    traceback.print_stack()
                continue

            buffVal = self[buffId][buffKey]
            if buffVal.isRemoving:
                continue

            if removeType==gameconst.RemoveType.EndByTime and not buffVal.isBuffTimeEnd(owner):
                buffVal.delayRemoveBuff(owner, isFinished, removeType)
                continue

            isModify = True
            buffVal.isRemoving = True
            buffVal.onBuffRemove(owner, isFinished, removeType)

            #onBuffRemove里可能会触发别的action，会移除这个buff，这里需要再判一次
            if buffId in self:
                self[buffId].pop(buffKey, None)

            removedKeys.append(buffKey)

            # fromEnt = KBEngine.entities.get(buffVal.releaseRoleId)
            # if fromEnt and fromEnt.id != owner.id:
            #     fromEnt.sendCombatMsg(MBD.datas.targetLoseBuff, [buffVal.level, buffVal.getBuffName(buffVal.buffId),
            #                                                      owner.name])
            # owner.sendCombatMsg(MBD.datas.loseBuff, [buffVal.level, buffVal.getBuffName(buffVal.buffId)])

        if not isModify:
            return

        #onBuffRemove里可能会触发别的action，会移除这个buff，这里需要再判一次
        if buffId in self:
            #如果srcKeys还不为空
            if self[buffId]:
                not owner.isDestroyed and owner.allClientsOnRemoveBuff(buffId, removedKeys)
            else:
                self.pop(buffId)
                not owner.isDestroyed and owner.allClientsOnRemoveBuff(buffId, [])

        self.buffTagSet.clear()
        for buffMap in self.values():
            for buff in buffMap.values():
                self.buffTagSet = buff.addBuffTags(self.buffTagSet)

        owner.broadcastRemoveBuffEvent(buffId)

    def checkValidOnLogin(self, owner,tLastOffline):
        rmBuffs = {}
        for buffId, buffMap in self.items():
            invalidKeys = []
            buffSrcKey = owner._getBuffSrcKey(buffId)
            for buffKey, buffVal in buffMap.items():
                if buffVal.getBuffDuration()>0 :
                    if buffVal.getBuffRemainTimeOffline(owner,tLastOffline) <= 0:
                        invalidKeys.append(buffKey)
                    else:
                        buffVal.duration=buffVal.getBuffRemainTimeOffline(owner,tLastOffline)
                        buffVal.tStartTime=time.time()
                if buffSrcKey and buffKey==buffSrcKey:
                    buffVal.releaseRoleId = owner.id

            if invalidKeys:
                rmBuffs[buffId] = invalidKeys

        for buffId, srcKeys in rmBuffs.items():
            owner.removeBuffWithoutCalc(buffId, srcKeys)

    def _lateReload(self):
        super(ServerBuffs, self)._lateReload()

        for buffMap in self.values():
            for v in buffMap.values():
                v.reloadScript()

        return


class Buff(userType.UserSoleType):
    def __init__(self, buffId, level, duration, releaseRoleId, srcType, srcKey, rootContext, randomValue=0,
                 removeTimerId=0,releaseRoleName="",releaseRoleGbId="", isAddBySelf=False):
        self.buffId = buffId
        self.level = int(level)
        self.tStartTime = time.time()
        self.releaseRoleId = releaseRoleId
        self.srcType = srcType
        self.srcKey = srcKey
        self.rootContext = rootContext              #最终来源上下文
        self.effectDic = {}
        self.removeTimerId = removeTimerId
        self.skillNum = 0
        self.beatNum = 0
        self.attNum = 0
        self.duration = duration
        self.usrDefineDic = {}
        self.randomValue = randomValue
        self.releaseRoleName=releaseRoleName
        self.releaseRoleGbId=releaseRoleGbId
        self.isRemoving = False
        self.isPause = False
        self.isAddBySelf = isAddBySelf

    def _lateReload(self):
        super(Buff, self)._lateReload()

        if self.rootContext:
            self.rootContext.reloadScript()

        for v in self.effectDic.values():
            v.reloadScript()

        return

    @classmethod
    def clearAllCache(cls):
        cls.getBuffData.cache_clear()
        cls.getBuffEffectList.cache_clear()
        cls.getKind.cache_clear()
        cls.getDeadDontRemove.cache_clear()
        cls.getEndByTime.cache_clear()
        cls.getEndBySkill.cache_clear()
        cls.getEndByBeat.cache_clear()
        cls.getEndByAtt.cache_clear()
        cls.getEndAction.cache_clear()
        cls.getEndByBeatAction.cache_clear()
        cls.getEndByDieRemoveAction.cache_clear()
        cls.getEndByTimeAction.cache_clear()
        cls.getRefreshAction.cache_clear()
        cls.getTag.cache_clear()
        cls.getOffLineLast.cache_clear()
        cls.getBuffName.cache_clear()
        cls.getOfflineKeep.cache_clear()
        cls.getIfSend.cache_clear()
        cls.getSchoolTag.cache_clear()

    @property
    def releaseRole(self):
        return KBEngine.entities.get(self.releaseRoleId)

    def getBuffRemainTime(self):
        duration = self.getBuffDuration()
        if duration<=0:
            return float('inf')

        endTime = duration + self.tStartTime

        return endTime-time.time() if endTime>time.time() else 0.0

    def getBuffRemainTimeOffline(self,owner,tLastOffline):
        if not owner.IsAvatar:
            tLastOffline = 0

        duration = self.getBuffDuration()
        if duration <= 0:
            return float('inf')

        endTime = duration + self.tStartTime
        if endTime < tLastOffline:
            return 0.0

        if self.isOffLineLast():
            return endTime - time.time() if endTime > time.time() else 0.0
        else:
            return endTime - tLastOffline

    def getBuffEndTime(self, owner):
        if self.getBuffDuration()<=0:
            return 0

        return time.time()+self.getBuffRemainTime()

    def _getBuffEventKey(self):
        return 'buff_%s_%s'%(self.buffId, self.srcKey)

    def initBuff(self, owner, **extraInfo):
        eventKey = self._getBuffEventKey()
        if self.getEndBySkill(self.buffId):
            owner.addListener('onSkill', eventKey, 'onEventSkill', (self.buffId, self.srcKey))
        if self.getEndByBeat(self.buffId):
            owner.addListener('onBeat', eventKey, 'onEventBeat', (self.buffId, self.srcKey))
        if self.getEndByAtt(self.buffId):
            owner.addListener('onHit', eventKey, 'onEventHit', (self.buffId, self.srcKey))

        self.getEffectList(owner, **extraInfo)

        duration = self.getBuffDuration()
        if duration > 0:
            remainTime = self.getBuffRemainTime()
            if remainTime>0:
                self.removeTimerId = owner._callback(remainTime, 'removeBuff', (self.buffId, (self.srcKey,), True,
                                                                                gameconst.RemoveType.EndByTime),
                                                                                gametimer.TIMER_TAG_REMOVE_BUFF)
            else:
                ERROR_MSG('initBuff error', duration, remainTime, self.tStartTime, self.buffId)
                owner.removeBuff(self.buffId, (self.srcKey,), False, gameconst.RemoveType.Default)
                return

    def _getEffectCaller(self):
        if self.srcType==gameconst.BuffSrcType.Combat:
            return effect.BuffCaller({'buffId':self.buffId, 'buffKey':self.srcKey,})

    def getEffectList(self, owner, **extraInfo):
        if self.srcType==gameconst.BuffSrcType.Combat:
            effectList = self.getBuffEffectList(self.buffId)
        else:
            gameengine.reportCritical('invalid buff src:', self.srcType, self.buffId)
            return

        if not effectList:
            return

        buffCaller = self._getEffectCaller()
        for i, effectDict in enumerate(effectList):
            effectId = effectDict['EffectId']
            effectKey = utils.getBuffEffectKey(effectId, i)
            self.effectDic[effectKey] = effect.createEffect(owner, buffCaller, effectId, i, extraInfo)
            self.effectDic[effectKey].setupEffect(owner, buffCaller)

            #effect可能把owner打死了，buff没有了，不再加别的effect
            if not buffCaller.getCaller(owner):
                break


    def onSetupEffectError(self, owner, callerInfo, effectId):
        owner.removeBuff(self.buffId, (self.srcKey,))

    #duration: 0:永久 >0:duration <0:读表
    def getBuffDuration(self):
        if self.duration >= 0:
            return self.duration
        else:
            return float(self.getEndByTime(self.buffId) or 0)

    @staticmethod
    @functools.lru_cache(1024)
    def getBuffData(buffId):
        return buff_buff.datas[buffId]

    @staticmethod
    @functools.lru_cache(1024)
    def getBuffEffectList(buffId):
        return Buff.getBuffData(buffId).get('effectList', ())

    @staticmethod
    @functools.lru_cache(1024)
    def getKind(buffId):
        return Buff.getBuffData(buffId).get('kind')

    @staticmethod
    @functools.lru_cache(1024)
    def getDeadDontRemove(buffId):
        return Buff.getBuffData(buffId).get('deadDontRemove')

    @staticmethod
    @functools.lru_cache(1024)
    def getEndByTime(buffId):
        return Buff.getBuffData(buffId).get('endByTime')

    @staticmethod
    @functools.lru_cache(1024)
    def getEndBySkill(buffId):
        return Buff.getBuffData(buffId).get('endBySkill')

    @staticmethod
    @functools.lru_cache(1024)
    def getEndByBeat(buffId):
        return Buff.getBuffData(buffId).get('endByBeat')

    @staticmethod
    @functools.lru_cache(1024)
    def getEndByAtt(buffId):
        return Buff.getBuffData(buffId).get('endByAtt')

    @staticmethod
    @functools.lru_cache(1024)
    def getEndAction(buffId):
        return Buff.getBuffData(buffId).get('endAction')

    @staticmethod
    @functools.lru_cache(1024)
    def getEndByBeatAction(buffId):
        return Buff.getBuffData(buffId).get('endByBeatAction')

    @staticmethod
    @functools.lru_cache(1024)
    def getEndByDieRemoveAction(buffId):
        return Buff.getBuffData(buffId).get('endByDieRemoveAction')

    @staticmethod
    @functools.lru_cache(1024)
    def getEndByTimeAction(buffId):
        return Buff.getBuffData(buffId).get('endByTimeAction')

    @staticmethod
    @functools.lru_cache(1024)
    def getRefreshAction(buffId):
        return Buff.getBuffData(buffId).get('refreshAction')

    @staticmethod
    @functools.lru_cache(1024)
    def getTag(buffId):
        return Buff.getBuffData(buffId).get('tag')

    @staticmethod
    @functools.lru_cache(1024)
    def getOffLineLast(buffId):
        return Buff.getBuffData(buffId).get('offLineLast')

    @staticmethod
    @functools.lru_cache(1024)
    def getBuffName(buffId):
        return Buff.getBuffData(buffId).get('name', '')

    def getEffect(self, effectKey):
        return self.effectDic.get(effectKey, None)

    @staticmethod
    @functools.lru_cache(1024)
    def getOfflineKeep(buffId):
        return Buff.getBuffData(buffId).get('offLineKeep', False)

    @staticmethod
    @functools.lru_cache(1024)
    def getIfSend(buffId):
        return Buff.getBuffData(buffId).get('ifSend', False)

    @staticmethod
    @functools.lru_cache(1024)
    def getSchoolTag(buffId):
        return Buff.getBuffData(buffId).get('classTag', 0)

    def addBuffTags(self, buffTagSet):
        tags = Buff.getTag(self.buffId)
        if tags:
            for tag in tags:
                buffTagSet.add(tag)
        return buffTagSet

    def hasTag(self, tag):
        tags = self.getTag(self.buffId)
        if tags and tag in tags:
            return True
        return False

    def overlayBuff(self, owner, toLevel, duration):
        DEBUG_MSG("trace overlayBuff 1")
        oldLevel = self.level

        if oldLevel == toLevel:
            remainTime = self.getBuffRemainTime()
            newDura = duration
            if duration < 0:
                newDura = float(self.getEndByTime(self.buffId) or 0)

            if newDura <= 0:
                newDura = float('inf')

            if newDura < remainTime :
                return
            DEBUG_MSG("trace overlayBuff 2 ", remainTime, self)

        self.tStartTime = time.time()
        self.skillNum = 0
        self.beatNum = 0
        self.attNum = 0

        if self.removeTimerId > 0:
            owner._cancelCallback(self.removeTimerId, gametimer.TIMER_TAG_REMOVE_BUFF)
            self.removeTimerId = 0

        self.duration = duration

        duration = self.getBuffDuration()
        if duration > 0:
            DEBUG_MSG("trace overlayBuff 3")
            buffCaller = self._getEffectCaller()
            for effectVal in self.effectDic.values():
                effectVal.onOverlayBuff(owner, buffCaller)

            self.removeTimerId = owner._callback(duration, 'removeBuff', (self.buffId, (self.srcKey,), True,
                                                                        gameconst.RemoveType.EndByTime),
                                                                        gametimer.TIMER_TAG_REMOVE_BUFF)

        if oldLevel != toLevel:
            DEBUG_MSG("trace overlayBuff 4")
            buffCaller = self._getEffectCaller()

            for effectVal in self.effectDic.values():

                if effectVal.EFFECT_TYPE == gameconst.EffecType.EFFECT_BASIC:
                    #先按旧的等级移除effect
                    effectVal.removeEffect(owner, buffCaller, isOverleap=True)

                elif effectVal.EFFECT_TYPE == gameconst.EffecType.EFFECT_BY_EVENT:
                    pass

                elif effectVal.EFFECT_TYPE == gameconst.EffecType.EFFECT_BY_TIMER:
                    effectVal.removeEffect(owner, buffCaller, isOverleap=True)

            self.level = int(toLevel)

            #按新等级添加effect
            for effectKey in list(self.effectDic.keys()):
                #setupEffect可能kill目标导致移除buff，清空effectDic
                effectVal = self.effectDic.get(effectKey)
                if not effectVal:
                    continue

                if effectVal.EFFECT_TYPE == gameconst.EffecType.EFFECT_BASIC:
                    effectVal.setupEffect(owner, buffCaller)

                elif effectVal.EFFECT_TYPE == gameconst.EffecType.EFFECT_BY_EVENT:
                    pass

                elif effectVal.EFFECT_TYPE == gameconst.EffecType.EFFECT_BY_TIMER:
                    effectVal.setupEffect(owner, buffCaller)

            refreshAction = self.getRefreshAction(self.buffId)
            if refreshAction:
                ctxFunc = lambda r:actionContext.BuffRefreshCtx(self.releaseRoleId, owner.id, self.buffId, self.level, self.srcKey, r, self.rootContext)
                owner.doCombatActions(refreshAction, owner, owner, owner.id, ctxFunc)
            DEBUG_MSG("trace overlayBuff ", self)

    def isBuffTimeEnd(self, owner):
        buffCaller = self._getEffectCaller()
        for effectVal in self.effectDic.values():
            if isinstance(effectVal, effect.TimerEffect):
                effectDict = effectVal.getEffectDict(owner, buffCaller)
                if effectDict['Count']>=0 and effectVal.isValid:
                    DEBUG_MSG('cannot remove buff by time now, will remove later', effectVal)
                    return False
        return True

    #有TimerEffect的buff必须保证effect tick的次数到达配置次数后才可以销毁，否则延迟移除
    def delayRemoveBuff(self, owner, isFinished, removeType):
        if self.removeTimerId > 0:
            owner._cancelCallback(self.removeTimerId, gametimer.TIMER_TAG_REMOVE_BUFF)

        self.removeTimerId = owner._callback(0.3, 'removeBuff', (self.buffId, (self.srcKey,), isFinished, removeType),
                                             gametimer.TIMER_TAG_REMOVE_BUFF)

    def onBuffRemove(self, owner, isFinished, removeType):
        #一定要放在最开始cancel，否则在action后cancel可能会把action加上去的timer退出了
        #因为这里保存的id已经是无效的了，可能被引擎重用
        if self.removeTimerId > 0:
            owner._cancelCallback(self.removeTimerId, gametimer.TIMER_TAG_REMOVE_BUFF)
            self.removeTimerId = 0

        eventKey = self._getBuffEventKey()
        if self.getEndBySkill(self.buffId):
            owner.removeListener('onSkill', eventKey)
        if self.getEndByBeat(self.buffId):
            owner.removeListener('onBeat', eventKey)
        if self.getEndByAtt(self.buffId):
            owner.removeListener('onHit', eventKey)

        if isFinished:
            owner.onEffectEvent('onBuffEnd', owner.id, owner.id, effectEventCtx.BuffEventCtx(self.buffId,
                                                                                             self.getTag(self.buffId),
                                                                                             removeType))

        eventAction = None
        endAction = self.getEndAction(self.buffId)
        if removeType == gameconst.RemoveType.EndByBeat and self.getEndByBeatAction(self.buffId):
            eventAction = self.getEndByBeatAction(self.buffId)
        elif removeType == gameconst.RemoveType.EndByDead and self.getEndByDieRemoveAction(self.buffId):
            eventAction = self.getEndByDieRemoveAction(self.buffId)
        elif removeType == gameconst.RemoveType.EndByTime:
            eventAction = self.getEndByTimeAction(self.buffId)

        ctxFunc = lambda r:actionContext.BuffEndCtx(self.releaseRoleId, owner.id, self.buffId, self.level, self.srcKey, removeType, r, self.rootContext)
        actFunc = lambda actionOwner, target, ctx: (eventAction and eventAction(owner, owner, ctx), endAction and endAction(owner, owner, ctx))

        owner.doCombatActions(actFunc, owner, owner, owner.id, ctxFunc)

        buffCaller = self._getEffectCaller()
        for effectId, effect in self.effectDic.items():
            DEBUG_MSG("remove effect ", effect)
            effect.removeEffect(owner, buffCaller)
        self.effectDic.clear()

    def onEventSkill(self, owner, event, buffId):
        if buffId != self.buffId:
            return
        self.skillNum += 1
        if self.getEndBySkill(self.buffId) > 0 and self.skillNum >= self.getEndBySkill(self.buffId):
            owner.removeListener('onSkill', self._getBuffEventKey())
            owner.removeBuff(self.buffId, (self.srcKey,), True, gameconst.RemoveType.EndBySkill)

    def onEventBeat(self, owner, event, buffId):
        if buffId != self.buffId:
            return
        self.beatNum += 1
        if self.getEndByBeat(self.buffId) > 0 and self.beatNum >= self.getEndByBeat(self.buffId):
            owner.removeListener('onBeat', self._getBuffEventKey())
            owner.removeBuff(self.buffId, (self.srcKey,), True, gameconst.RemoveType.EndByBeat)

    def onEventHit(self, owner, event, buffId):
        if buffId != self.buffId:
            return
        self.attNum += 1
        if self.attNum >= self.getEndByAtt(self.buffId) > 0:
            owner.removeListener('onHit', self._getBuffEventKey())
            owner.removeBuff(self.buffId, (self.srcKey,), True, gameconst.RemoveType.EndByAtt)

    def isRemoveOnDead(self):
        if self.getDeadDontRemove(self.buffId):
            return False
        return True

    def isOffLineLast(self):
        if self.getOffLineLast(self.buffId):
            return True
        return False

    def pauseEffects(self, owner):
        if self.isPause:
            WARNING_MSG("pauseEffects has already paused", self.buffId)
            return

        self.isPause = True
        buffCaller = self._getEffectCaller()
        for effectId in list(self.effectDic.keys()):
            effect = self.effectDic.get(effectId)
            DEBUG_MSG("pauseEffects effect ", effect)
            effect and effect.pauseEffect(owner, buffCaller)

    def restartEffects(self, owner):
        if not self.isPause:
            WARNING_MSG("restartEffects has not paused", self.buffId)
            return

        self.isPause = False
        buffCaller = self._getEffectCaller()
        for effectId in list(self.effectDic.keys()):
            effect = self.effectDic.get(effectId)
            DEBUG_MSG("restartEffects effect ", effect)
            effect and effect.restartEffect(owner, buffCaller)

    def resetTimerId(self):
        self.removeTimerId = 0

    def getClassTag(self, owner):
        classTag = self.getSchoolTag(self.buffId)
        if classTag == -1 and owner.IsAICombatUnit:
            battleType = owner.getBattleType()
            if battleType == gameconst.BattleType.physics:
                classTag = gameconst.SCHOOL_PHYSICAL
            elif battleType == gameconst.BattleType.magic:
                classTag = gameconst.SCHOOL_MAGIC
        return classTag

    def onRestored(self, owner):
        if self.isAddBySelf:
            self.releaseRoleId = owner.id

    def getClientVal(self, owner):
        return ClientBuffVal(self.buffId, self.level, self.srcKey, self.getBuffEndTime(None), self.getBuffDuration())

    def getClientData(self, owner):
        return {
            'buffId':self.buffId,
            'srcKey':self.srcKey,
            'level':self.level,
            'endTimeStamp': self.getBuffEndTime(owner),
            'duration': self.getBuffDuration()
        }

    def getClientStream(self):
        return struct.pack('<IQIdf', self.buffId, self.srcKey, self.level, self.getBuffEndTime(None), self.getBuffDuration())

    def getSavedDict(self):
        return {'tStartTime': self.tStartTime,
                'skillNum': self.skillNum,
                'beatNum': self.beatNum,
                'attNum': self.attNum,
                'duration': self.duration,
                'effectDic': self.effectDic,
                'randomValue' : self.randomValue,
                'rootContext': self.rootContext,
                'isAddBySelf': self.isAddBySelf,
                }

    def loadSavedDict(self, data):
        if 'tStartTime' in data:
            self.tStartTime = data['tStartTime']
        if 'skillNum' in data:
            self.skillNum = data['skillNum']
        if 'beatNum' in data:
            self.beatNum = data['beatNum']
        if 'attNum' in data:
            self.attNum = data['attNum']
        if 'duration' in data:
            self.duration = data['duration']
        if 'effectDic' in data:
            self.effectDic = data['effectDic']
        if 'randomValue' in data:
            self.randomValue = data['randomValue']
        if 'rootContext' in data:
            self.rootContext = data['rootContext']
        if 'isAddBySelf' in data:
            self.isAddBySelf = data['isAddBySelf']


