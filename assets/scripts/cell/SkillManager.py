# -*- coding: utf-8 -*-
import KBEngine
import gameconst
from KBEDebug import *
import skill_skill as SSD
import conflict_conflict
import buff_buff
import time
import combatSkill
import buff
import random
import formula
import math, Math, sMath
import collections
import utils
import actionContext
import effectEventCtx
import iEventActions
import iCell
import gameengine
import gameclass
import gametimer
import gamemove
import gameconfig
import dataUtils
import gamedecorator
import iFlowController
import gameglobal
import fightProp_define as FDD
import message_Message as MSG
import conflict_status as CSD
import conflict_conflict_def as CCD
import creation_creation as CRD
import buff_buff as BBD
import const_const as CONST
import conflict_status_def as CCDD
import gamePlay_gamePlay as GPGPD
import gamePlay_set as GP_SD
import aureola_aureola as AAD
import aureole


class AureoleMixin(object):
    def addTAureoleTrap(self, aureoleId):
        _aureole = self.aureoleDic.get(aureoleId)

        if not _aureole:
            return

        _aureole.addAureoleTrap(self)

    def isWholeAreaAureole(self, aureoleId):
        return self.spaceMgr and AAD.datas[aureoleId].get('radium') == -1

    def removeAureole(self, aureoleId):
        self.aureoleDic.removeAureole(self, aureoleId)

    def clearAureole(self):
        for _aureoleId in list(self.aureoleDic.keys()):
            self.removeAureole(_aureoleId)

    def disableAureole(self, aureoleId=0):
        if aureoleId == 0:
            for aureoleId in list(self.aureoleDic.keys()):
                self.aureoleDic.disableAureole(self, aureoleId)
        else:
            self.aureoleDic.disableAureole(self, aureoleId)

    # 光环内单位与光环主人敌我关系变化检查，暂时先不查，玩家没光环
    def _checkAuroleTargetType(self):
        invalidAureoles = []
        for aid, aval in self.aureoleFormOtherDic.items():
            srcEnt = KBEngine.entities.get(aval.srcEntId)
            if not srcEnt or srcEnt.isDestroyed:
                self.removeAureoleEffect(aid, aval.srcEntId)
                continue

            if not srcEnt.isValidAureoleTarget(aid, self):
                invalidAureoles.append((aid, srcEnt))
                continue

        for aid, srcEnt in invalidAureoles:
            srcEnt.removeAureoleTarget(aid, self.id)

        if self.aureoleFormOtherDic:
            self._callback(10, '_checkAuroleTargetType', ())

    def addAureoleEffect(self, srcEntId, aureoleId, aureoleLv):
        curar = self.aureoleFormOtherDic.get(aureoleId, None)
        if curar:
            if curar.level >= aureoleLv:
                return False
            else:
                self.removeAureoleEffect(aureoleId, 0)

        startAction = AAD.datas[aureoleId].get('action')
        srcEnt = KBEngine.entities.get(srcEntId)
        if startAction and srcEnt:
            ret = self.doCombatActions(startAction, srcEnt, self, srcEntId,
                                       lambda result: actionContext.AureoleCtx(srcEntId, aureoleId, aureoleLv, result))
            if ret == False:
                ERROR_MSG('addAureoleEffect faileed', srcEntId, aureoleId)
                return False

        srcHostEntId = srcEnt.getHost().id if srcEnt.getHost() is not None else None
        self.aureoleFormOtherDic.applyAureole(aureoleId, aureoleLv, srcEntId, srcHostEntId)

        clientAr = aureole.ClientAureoleVal(aureoleId, aureoleLv)
        self.allClients.onAddAureoleFromOthers(clientAr.getClientData())
        return True

    # 作用目标移除光环效果
    def removeAureoleEffect(self, aureoleId, srcEntId):
        curar = self.aureoleFormOtherDic.get(aureoleId, None)
        if curar and (not srcEntId or curar.srcEntId == srcEntId):
            self.aureoleFormOtherDic.pop(aureoleId)
            # 移除可能在srcEnt的onDestroy里移除，这个时候虽然srcEnt还在，但是在KBEngine.entities里已经没有了
            # 所以这里执行action的主体先用self吧
            endAction = AAD.datas[aureoleId].get('endActionToEffectObject')
            if endAction:
                _srcEntId = curar.srcHostEntId if curar.srcHostEntId is not None else curar.srcEntId
                self.doCombatActions(endAction, self, self, curar.srcEntId,
                                     lambda r: actionContext.AureoleCtx(_srcEntId, aureoleId, curar.level, r))

            if self.isReal():
                self.allClients.onRemoveAureoleFromOthers(aureoleId)

        if self.hasAureola(aureoleId) and (srcEntId and srcEntId != self.id):
            aVal = self.aureoleDic[aureoleId]
            self.onEnterTrap(self, 0, 0, aVal.aureoleTrapId, gameconst.AUREOLE_TRAP)

    def hasAureola(self, aureolaId):
        return aureolaId in self.aureoleDic

    def isValidAureoleTarget(self, aureolaId, target):
        if not self.hasAureola(aureolaId):
            return False

        _aureole = self.aureoleDic[aureolaId]
        if not utils.checkTargetType(_aureole.effectTarget, self, target):
            return False

        return True

    # 光环主人移除目标
    def removeAureoleTarget(self, aureolaId, targetId):
        _aureole = self.aureoleDic[aureolaId]
        _aureole.onLeaveAureoleRnage(self, targetId)


class StatisticsRecordsMixin(object):
    def __init__(self):
        self.statisticsDmgRecords = collections.deque(maxlen=self.maxRecordsCount)

    @property
    def statisticsDmgRecordTimerId(self):
        return self.getTempMiscProp(gameconst.AvatarProps.statisticsDmgRecordTimerId, 0)

    @statisticsDmgRecordTimerId.setter
    def statisticsDmgRecordTimerId(self, newTimerId):
        self.setTempMiscProp(gameconst.AvatarProps.statisticsDmgRecordTimerId, newTimerId)

    @statisticsDmgRecordTimerId.deleter
    def statisticsDmgRecordTimerId(self):
        self.popTempMiscProp(gameconst.AvatarProps.statisticsDmgRecordTimerId)

    @property
    def maxRecordsTimeout(self):
        return 30

    @property
    def maxRecordsCount(self):
        return 100

    def stopStatisticsRecorded(self):
        DEBUG_MSG("stopStatisticsRecorded::", self.statisticsDmgRecordTimerId)
        if self.statisticsDmgRecordTimerId:
            self._stopStatisticsRecorded()

    def _stopStatisticsRecorded(self):
        self._cancelCallback(self.statisticsDmgRecordTimerId, gametimer.TIMER_TAG_IN_REFRESH_STATISTICS_RECORDS)
        del self.statisticsDmgRecordTimerId

    def startStatisticsRecorded(self):
        DEBUG_MSG("startStatisticsRecorded::")
        self._refreshStatisticsRecordsRegr()

    def _refreshStatisticsRecordsRegr(self):
        if self.statisticsDmgRecordTimerId:
            self._stopStatisticsRecorded()
        m_tid = self._callback(1, '_inRefreshStatisticsRecords', (),
                               gametimer.TIMER_TAG_IN_REFRESH_STATISTICS_RECORDS, 'statisticsDmgRecordTimerId')
        self.statisticsDmgRecordTimerId = m_tid

    def _inRefreshStatisticsRecords(self):
        self.refreshStatisticsRecords()
        self._refreshStatisticsRecordsRegr()

    def refreshStatisticsRecords(self):
        now = utils.getNow()
        lastTime = now - self.maxRecordsTimeout
        while True:
            if not self.statisticsDmgRecords:
                break

            d = self.statisticsDmgRecords[0]
            if d[-1] > lastTime:
                break
            else:
                self.statisticsDmgRecords.popleft()

    def recordStatisticsRecords(self, ent, cxtResult, srcIsSelf):
        # DEBUG_MSG('recordStatisticsRecords::', ent, cxtResult, srcIsSelf)
        data = (ent.id, ent.gbId, cxtResult, srcIsSelf, utils.getNow())
        self.statisticsDmgRecords.append(data)
        return data

    def iterGetLastXSecondsRecords(self, rTime=10):
        if rTime > self.maxRecordsTimeout:
            rTime = self.maxRecordsTimeout

        idx = -1
        now = utils.getNow()
        lastTime = now - rTime

        while True:
            if not self.statisticsDmgRecords:
                return

            if abs(idx) > len(self.statisticsDmgRecords):
                return

            data = self.statisticsDmgRecords[idx]
            if data[-1] < lastTime:
                return

            yield data
            idx -= 1

    def resetStatisticsRecords(self):
        self.statisticsDmgRecords.clear()


class StandStillBuffTriggerLoopMixin(object):

    @property
    def standStillBuffTriggerCacheDic(self) -> dict:
        """Type: Dict[buffId, Dict[buffId, maxOverlayLevel, upPreOverlaySec, downPreOverlaySec,
                      lastOverlayT, lastOverlayActionType, timerId, uuid]]"""
        if not self.hasTempMiscProp(gameconst.AvatarProps.standStillBuffTriggerCacheDic):
            self.setTempMiscProp(gameconst.AvatarProps.standStillBuffTriggerCacheDic, dict())
        return self.getTempMiscProp(gameconst.AvatarProps.standStillBuffTriggerCacheDic)

    def regrStandStillBuffTriggerCache(self, buffId, maxOverlayLevel, upPreOverlaySec, downPreOverlaySec,
                                       skipTick=True):
        INFO_MSG("regrStandStillBuffTriggerCache::", buffId, maxOverlayLevel, upPreOverlaySec, downPreOverlaySec)
        standStillBuffTriggerCacheDic = self.standStillBuffTriggerCacheDic
        if buffId in standStillBuffTriggerCacheDic:
            self.unregrStandStillBuffTriggerCache(buffId)

        _uuid = KBEngine.genUUID64()
        _gcd = sMath.gcd(upPreOverlaySec, downPreOverlaySec)
        _timerId = self._callback(_gcd, '_onStandStillBuffTriggerCallback', (buffId, _uuid, skipTick),
                                  gametimer.TIMER_TAG_STANDSTILL_BUFF_LOOP_TRIGGER)

        _data = dict(buffId=buffId,
                     maxOverlayLevel=maxOverlayLevel,
                     upPreOverlaySec=upPreOverlaySec,
                     downPreOverlaySec=downPreOverlaySec,
                     lastOverlayT=0,
                     lastOverlayActionType=gameconst.StandStillBuffLastOverlayActionType.NONE,
                     timerId=_timerId,
                     uuid=_uuid)
        standStillBuffTriggerCacheDic[buffId] = _data

    def _onStandStillBuffTriggerCallback(self, buffId, uuid, skipTick):
        DEBUG_MSG("_onStandStillBuffTriggerCallback::", buffId, uuid, skipTick)
        standStillBuffTriggerCacheDic = self.standStillBuffTriggerCacheDic
        if buffId not in standStillBuffTriggerCacheDic:
            WARNING_MSG("_onStandStillBuffTriggerCallback:: missing buffId", buffId, uuid)
            return

        if uuid != standStillBuffTriggerCacheDic[buffId]['uuid']:
            WARNING_MSG("_onStandStillBuffTriggerCallback:: uuid mismatch", buffId, uuid,
                        standStillBuffTriggerCacheDic[buffId])
            return

        _data = standStillBuffTriggerCacheDic[buffId]
        _now = utils.getNow()
        if self.hasState(gameconst.State.Moving):
            if _data["lastOverlayT"] + _data["downPreOverlaySec"] <= _now:
                if skipTick and _data["lastOverlayActionType"] == gameconst.StandStillBuffLastOverlayActionType.UP:
                    _data["lastOverlayActionType"] = gameconst.StandStillBuffLastOverlayActionType.NONE
                else:
                    self.changeBuffLevel(buffId, -1, self.id, duration=-1, levelLimit=_data["maxOverlayLevel"],
                                         autoHandleBuff=True)
                    _data["lastOverlayT"] = _now
                    _data["lastOverlayActionType"] = gameconst.StandStillBuffLastOverlayActionType.DOWN

        else:
            if _data["lastOverlayT"] + _data["upPreOverlaySec"] <= _now:
                if skipTick and _data["lastOverlayActionType"] == gameconst.StandStillBuffLastOverlayActionType.DOWN:
                    _data["lastOverlayActionType"] = gameconst.StandStillBuffLastOverlayActionType.NONE
                else:
                    self.changeBuffLevel(buffId, 1, self.id, duration=-1, levelLimit=_data["maxOverlayLevel"],
                                         autoHandleBuff=True)
                    _data["lastOverlayT"] = _now
                    _data["lastOverlayActionType"] = gameconst.StandStillBuffLastOverlayActionType.UP

        _gcd = sMath.gcd(_data["upPreOverlaySec"], _data["downPreOverlaySec"])
        _timerId = self._callback(_gcd, '_onStandStillBuffTriggerCallback', (buffId, uuid, skipTick),
                                  gametimer.TIMER_TAG_STANDSTILL_BUFF_LOOP_TRIGGER)
        _data["timerId"] = _timerId

    def unregrStandStillBuffTriggerCache(self, buffId):
        INFO_MSG("unregrStandStillBuffTriggerCache::", buffId)
        _data = self.standStillBuffTriggerCacheDic.pop(buffId, None)
        if not _data:
            return

        if _data['timerId']:
            self._cancelCallback(_data['timerId'], gametimer.TIMER_TAG_STANDSTILL_BUFF_LOOP_TRIGGER)

        _buffSrcKey = self._getBuffSrcKey(_data['buffId'], self.id)
        if _data['buffId'] and self.hasBuff(_data['buffId'], _buffSrcKey):
            self.removeBuff(_data['buffId'], _buffSrcKey)


handlerMap = {}


def propChangedHandler(changedBySrc, propName):
    def _f(f, *args):
        if type(propName) == str:
            propNames = (propName,)
        else:
            propNames = propName

        if type(changedBySrc) == int:
            srcList = (changedBySrc,)
        else:
            srcList = changedBySrc

        for name in propNames:
            handlerMap.setdefault(name, {})
            for src in srcList:
                handlerMap[name][src] = f
        return f

    return _f


class SkillManager(iCell.ICell, iEventActions.IEventActions, iFlowController.IFlowController,
                   AureoleMixin, StatisticsRecordsMixin, StandStillBuffTriggerLoopMixin):
    def __init__(self):

        StatisticsRecordsMixin.__init__(self)
        self.shieldDic = buff.Shields()

        hpPercent = self.hp / self.fullHp if self.fullHp else 1
        mpPercent = self.mp / self.fullMp if self.fullMp else 1
        self.initBaseProperties()
        self.initCombatProps(hpPercent, mpPercent)
        self.isWitnessComplete = gameconst.WitnessType.WITNESS_TYPE_ALL
        self.stateList = formula.getInt64VectorOnIndexes(self.getStateBitVector())

    def isAttackable(self, src):
        return utils.isJoinCombat(self, src)

    def initBaseProperties(self):
        pass

    def _preSafeDestory(self):
        super(SkillManager, self)._preSafeDestory()
        self.destroyAllSummon()
        self.disableAureole()

    def _onDestroy(self):
        self.clearAureole()
        self.clearAllTargetTypeCache(True)

    def overwriteProps(self):
        """初始化时覆盖一些属性, 需要再子类中显示调用, 一般在放在__init__完成后"""

    def onInitPropsCompleted(self):
        # if self.hp > self.fullHp:
        #     self.hp = self.fullHp
        # if self.mp > self.fullMp:
        #     self.mp = self.fullMp
        pass

    def initCombatProps(self, hpPercent, mpPercent):
        checkedPropSet = set()
        for propName, propData in FDD.datas.items():

            if not hasattr(self, propName):
                continue

            # 虽然没设置属性，但上线时也需要重新计算下
            # 因为有些属性时存数据库的，所以要计算它影响的属性
            self.checkOnUpdateProp(propName, gameconst.SourceType.Init, checkedPropSet)

        # 上面不会重算hp,mp这种存数据库的属性，这里重设下处理数值被离线修改的情况
        self.hp = math.ceil(self.fullHp * hpPercent)
        self.mp = math.ceil(self.fullMp * mpPercent)

        DEBUG_MSG("initCombatProps", self.hp, self.fullHp, self.mp, self.fullMp)

    def checkOnUpdateProp(self, propName, src, checkedPropSet=None):
        propData = FDD.datas.get(propName)
        if not propData:
            return

        changeAffactProps = propData.get('changeAffactProp')
        if not changeAffactProps:
            return

        affectProps = changeAffactProps.split(';')
        if self.IsAvatar:
            formulaStr = 'formulaPlayer'
        else:
            formulaStr = 'formulaMonster'

        propFormulaFunc = propData.get(formulaStr)
        isInit = (src == gameconst.SourceType.Init)
        for affectedProp in affectProps:
            # hp,mp等存数据库的属性，在初始化时不参与计算，因为这里propName对应的属性可能不是最终值，会把这类属性算成错的
            if (isInit) and affectedProp in ('hp', 'mp'):
                continue

            if isInit and not propFormulaFunc and checkedPropSet and affectedProp in checkedPropSet:
                continue

            elif not affectedProp or not hasattr(self, affectedProp):
                continue

            affectedPropData = FDD.datas.get(affectedProp)
            if not affectedPropData:
                continue

            func = affectedPropData.get(formulaStr)
            if not func:
                continue

            try:
                value = func(self)
                if value != gameconst.scriptNone:
                    self.setProp(affectedProp, value, src)
                    if checkedPropSet is not None:
                        checkedPropSet.add(affectedProp)
            except Exception as e:
                ERROR_MSG('Error: failed to call func in checkOnUpdateProp:  %s, reason:%s.' % (affectedProp, repr(e)))

    # FOR DEBUG ONLY. called if KBEngine.publish()==0
    def onScriptSetAttr(self, key, value, isInit):
        if key not in FDD.datas:
            return

        if key in ('hp', 'mp'):
            return

        if isInit:
            return

        if self.IsAvatar:
            formulaStr = 'formulaPlayer'
        else:
            formulaStr = 'formulaMonster'

        if FDD.datas[key][formulaStr]:
            nDepth = 10
            f = sys._getframe()
            lastFrame = None
            for i in range(nDepth):
                if not f:
                    break

                if f.f_code.co_name in (
                        '__init__', 'checkOnUpdateProp', 'initBaseProperties', 'inheritProps'):
                    return

                lastFrame = f
                f = f.f_back

            if lastFrame.f_code.co_name in ('onScriptSetAttr',):
                return

            gameengine.reportCritical('cannot set %s directly to %s' % (key, value))

    def addProp(self, propName, delta, src=gameconst.SourceType.Default):
        if KBEngine.publish() == 0:
            curVal = self.getProp(propName)
            if type(curVal) is int and type(curVal) != type(delta):
                gameengine.reportCritical('addProp type error', propName, curVal, delta)

        oldVal = getattr(self, propName)
        newVal = type(oldVal)(oldVal + delta)
        self.setProp(propName, newVal, src)

        for changedSrc in (src, gameconst.SourceType.All):
            if propName in handlerMap and changedSrc in handlerMap[propName]:
                handlerMap[propName][changedSrc](src, oldVal)

    def setProp(self, propName, value, src=gameconst.SourceType.Default):
        if KBEngine.publish() == 0:
            curVal = self.getProp(propName)
            if type(curVal) is int and type(curVal) != type(value):
                gameengine.reportCritical('setProp type error', propName, curVal, value)
            # 初始化的日志太多了
            if src != gameconst.SourceType.Init:
                self.combatDebugMsg('setProp: propName:%s, oldValue:%s, value:%s, sourceType:%s', propName, curVal, value, src)
        # hasattr判断先拿掉，好像有点慢
        oldVal = getattr(self, propName)
        func = type(oldVal)
        setattr(self, propName, type(oldVal)(value))

        if func is int:
            if oldVal == int(value):
                return
        elif func is float:
            if math.isclose(oldVal, float(value)):
                return

        self.checkOnUpdateProp(propName, src)

        for changedSrc in (src, gameconst.SourceType.All):
            if propName in handlerMap and changedSrc in handlerMap[propName]:
                handlerMap[propName][changedSrc](self, src, oldVal)

    def getProp(self, propName):
        return getattr(self, propName)

    def getFightProps(self):
        propValDic = {}
        for propName, _ in FDD.datas.items():
            val = getattr(self, propName, None)
            if val is None:
                continue
            propValDic[propName] = val
        return propValDic

    # 这几个函数子类重写没用，要继承需要先改装饰器
    @propChangedHandler(gameconst.SourceType.All, ('adjCD', 'mulCD'))
    def onCDPropChanged(self, srcType, oldVal):
        # CD发生了变化,需要同步客户端
        for skillVal in self.getSkillDic().values():
            skillVal.changeCD(self, 0.0)

    @propChangedHandler((gameconst.SourceType.Equip, ), ('fullHp',))
    def onFullHpChanged(self, srcType, oldVal):
        DEBUG_MSG('onFullHpChanged', srcType, oldVal)
        # hpPercent = self.hp / oldVal if oldVal else 1
        # newHp = self.fullHp * hpPercent
        # self.modifyHP(newHp - self.hp, self.id, srcType, 0)

    @propChangedHandler((gameconst.SourceType.Equip, ), ('fullMp',))
    def onFullMpChanged(self, srcType, oldVal):
        DEBUG_MSG('onFullMpChanged', srcType, oldVal)
        # mpPercent = self.mp / oldVal if oldVal else 1
        # newMp = self.fullMp * mpPercent
        # self.modifyMP(newMp - self.mp)

    @propChangedHandler((gameconst.SourceType.All, ), ('drugsQuantity',))
    def onDrugsQuantityChanged(self, srcType, oldVal):
        DEBUG_MSG('onDrugsQuantityChanged', srcType, oldVal)
        self.base.onDrugsQuantitySync(self.drugsQuantity)

    def rateInDungeon(self, rate):
        self.hp = self.fullHp

    def onEffectAddProp(self, propName, delta, callerInfo, effectId, effectIdx):
        propsByEffect = self.getTempMiscProp(gameconst.AvatarProps.effectSetProps)
        if propsByEffect and propName in propsByEffect:
            ERROR_MSG('onEffectAddProp error: cannot modify prop set by another effect')
            return

        curVal = self.getProp(propName)
        delta = type(curVal)(delta)

        newVal = curVal + delta
        self.setProp(propName, newVal, gameconst.SourceType.Buff)
        # oldVal, oldCallerKey = propsByEffect[propName]
        # propsByEffect[propName] = (oldVal+delta, oldCallerKey)

    def onEffectSetProp(self, propName, newVal, callerInfo, effectId, effectIdx):
        if not self.hasTempMiscProp(gameconst.AvatarProps.effectSetProps):
            self.setTempMiscProp(gameconst.AvatarProps.effectSetProps, {})

        propsByEffect = self.getTempMiscProp(gameconst.AvatarProps.effectSetProps)
        newCallerKey = callerInfo.getCallerKey(effectId, effectIdx)
        if propName in propsByEffect:
            oldVal, setCnt, oldCallerKey = propsByEffect[propName]
        else:
            oldVal = self.getProp(propName)
            setCnt = 0

        propsByEffect[propName] = (oldVal, setCnt + 1, newCallerKey)
        self.setProp(propName, newVal, callerInfo.getCallerSrc())

    def onEffectUnsetProp(self, propName, callerInfo, effectId, effectIdx):
        propsByEffect = self.getTempMiscProp(gameconst.AvatarProps.effectSetProps)
        callerSrcKey = callerInfo.getCallerKey(effectId, effectIdx)
        if propName in propsByEffect:
            oldVal, setCnt, curCallerKey = propsByEffect[propName]

            setCnt -= 1
            if setCnt <= 0:
                propsByEffect.pop(propName)
                self.setProp(propName, oldVal, callerInfo.getCallerSrc())
            else:
                propsByEffect[propName] = (oldVal, setCnt, curCallerKey)

            if not propsByEffect:
                self.popTempMiscProp(gameconst.AvatarProps.effectSetProps)
        else:
            gameengine.reportCritical('onEffectUnsetProp: prop missing %s %s' % (propName, callerSrcKey))
            return

    def onAdjPropByDailyDraw(self, adjProp, duration):
        name, delta = adjProp
        oldVal = self.getProp(name)
        newVal = oldVal + delta
        self.setProp(name, newVal, gameconst.SourceType.DailyDraw)
        self._datetimeCallback(duration, 'onAdjPropByDailyDrawExpired', (adjProp,),
                               gametimer.TIMER_TAG_DAILYDRAW_ADJ_PROP)

    def onAdjPropByDailyDrawExpired(self, adjProp):
        name, delta = adjProp
        oldVal = self.getProp(name)
        newVal = oldVal - delta
        self.setProp(name, newVal, gameconst.SourceType.DailyDraw)

    def isDie(self):
        return self.hasState(gameconst.State.Death)

    def hasSkill(self, skillId):
        if skillId <= 0:
            return False

        skill = self.getSkillDic().get(skillId, None)
        if not skill:
            return False

        return True

    def hasPassiveSkill(self, skillId):
        if skillId <= 0:
            return False

        skill = self.passiveSkillDic.get(skillId, None)
        if not skill:
            return False

        return True

    def getSkill(self, skillId, reportError=True, forceBuildSkill=False):
        if skillId <= 0:
            return

        if forceBuildSkill:
            skill = self.skillDic.get(skillId, None)
        else:
            skill = self.getSkillDic().get(skillId, None)
        if not skill and reportError:
            import traceback
            traceback.print_stack()
            ERROR_MSG('getSkill no skillId', skillId)
            return None

        return skill

    def popSkill(self, skillId, reportError=True):
        if skillId <= 0:
            return

        skill = self.getSkillDic().pop(skillId, None)
        if not skill and reportError:
            import traceback
            traceback.print_stack()
            ERROR_MSG('popSkill no skillId', skillId)
            return None

        return skill

    def safePopSkill(self, skillId):
        if skillId <= 0:
            return

        _skill = self.getSkill(skillId)
        if _skill:
            _skill.resetSkill(self)

        return self.popSkill(skillId)

    def addSkill(self, skillId, skillLv, tNextCast=0):
        if skillId not in SSD.datas:
            ERROR_MSG('addSkill skillID not in configTable', skillId)
            return

        if skillId not in self.skillDic:
            skill = self.skillDic.add(self, skillId, skillLv, tNextCast=tNextCast)
            self.onEffectEvent('onAddSkill', self.id, self.id, effectEventCtx.AddSkillEventCtx(skillId))
            return skill

        return

    def setAllSkillLv(self, skillLv):
        for sVal in self.getSkillDic().values():
            sVal.setLevel(self, skillLv)

    def addPassiveSkill(self, pSkillId, pskillLv):
        if pSkillId in self.passiveSkillDic:
            return False

        self.passiveSkillDic.addPSkill(pSkillId, pskillLv)

        self.client.onAddPassiveSkill(pSkillId, pskillLv)
        return True

    def getSkillByCategory(self, skillId, level):
        category = SSD.datas[skillId].get('category', 0)
        if category in (
                gameconst.SkillCategory.CAST_SKILL_WITH_ACTION, gameconst.SkillCategory.CAST_SKILL_WITHOUT_ACTION):
            skill = combatSkill.getSkillClass(skillId)(skillId, level)
        elif category == gameconst.SkillCategory.GENERAL_SKILL:
            skill = self.getSkill(skillId)
        else:
            skill = None

        return skill

    def _getBuffSrcKey(self, buffId, srcEntId=None):
        bd = BBD.datas.get(buffId, {})
        if bd.get('isCover', 1):
            return 0

        # addBuff里releaseRole会转成host，所以这里也要转一下，否则会出现creation加的buff自己无法找到，因为srcKey算到主人去了
        if (self.IsCreation or self.IsPet or self.IsSummon) and self.getHost():
            return self.getHost()._getBuffSrcKey(buffId, srcEntId)

        return srcEntId if srcEntId is not None else self.id

    def getBuffByBuffId(self, buffId, buffSrcKey=None):
        buffMap = self.buffDic.get(buffId, {})
        if buffSrcKey is None:
            buffSrcKey = self._getBuffSrcKey(buffId)

        return buffMap.get(buffSrcKey)

    def getBuffMap(self, buffId):
        return self.buffDic.get(buffId, {})

    def checkRemoveBuffOnTargetTypeChanged(self):
        rmBuffs = []
        for buffId, buffMap in self.buffDic.items():
            for buffSrcKey, buffVal in buffMap.items():
                srcEnt = buffVal.releaseRole
                if not srcEnt or srcEnt.id == self.id:
                    continue
                if buff.Buff.getKind(buffId) < 0 and utils.checkTargetType('Friend', srcEnt, self):
                    rmBuffs.append((buffId, buffSrcKey))
                elif buff.Buff.getKind(buffId) >= 0 and utils.checkTargetType('Enemy', srcEnt, self):
                    rmBuffs.append((buffId, buffSrcKey))

        for buffId, buffSrcKey in rmBuffs:
            self.removeBuff(buffId, buffSrcKey)

    def clearBuffWhenLeaveHome(self):
        rmBuffs = []
        for buffId, buffMap in self.buffDic.items():
            for buffSrcKey, buffVal in buffMap.items():
                if buffVal.hasTag(gameconst.BuffTag.Home):
                    rmBuffs.append((buffId, buffSrcKey))

        for buffId, buffSrcKey in rmBuffs:
            self.removeBuff(buffId, buffSrcKey)

    def removeAllBuff(self):
        for buffId in list(self.buffDic.keys()):
            self.removeBuff(buffId)

    def removeAllNegativeBuff(self):
        for buffId in list(self.buffDic.keys()):
            if buff.Buff.getKind(buffId) < 0:
                self.removeBuff(buffId)

    def removeBuff(self, buffId, buffSrcKeys=None, isFinished=False, removeType=gameconst.RemoveType.Default):
        if not buffId in self.buffDic:
            return
        DEBUG_MSG('removeBuff', buffId, buffSrcKeys, removeType)
        self.buffDic.removeBuff(self, buffId, buffSrcKeys, isFinished, removeType)

    def removeBuffByKind(self, buffKind):
        for buffId in list(self.buffDic.keys()):
            if buff.Buff.getKind(buffId) == buffKind:
                self.removeBuff(buffId)

    def removeBuffByTag(self, buffTag):
        for buffId in list(self.buffDic.keys()):
            tagList = buff.Buff.getTag(buffId)
            if tagList and buffTag in tagList:
                self.removeBuff(buffId)

    def removeBuffWithoutCalc(self, buffId, srcKeys):
        self.buffDic.removeWithoutCalc(self, buffId, srcKeys)

    def broadcastAddBuffEvent(self, buffID, srcKeys):
        self.allClientsOnAddBuff(buffID, srcKeys)

    def broadcastRemoveBuffEvent(self, buffID):
        pass

    def addBuff(self, buffId, level, releaseRoleId, duration=-1, rootContext=None, kwargs=None):
        DEBUG_MSG("addBuff ", buffId, level, releaseRoleId, duration, kwargs)
        if buffId not in buff_buff.datas:
            ERROR_MSG('addBuff buffId not in configTable', buffId)
            return

        if self.isDie() and not buff.Buff.getDeadDontRemove(buffId):
            return

        if len(self.buffDic) >= gameconst.MAX_BUFF_COUNT:
            WARNING_MSG('buff num reaches max, ignore', buffId)
            return

        releaseRole = KBEngine.entities.get(releaseRoleId)

        if not releaseRole:
            WARNING_MSG('addBuff fail: invalid src entity', buffId, level, releaseRoleId, rootContext)
            return

        buffSrcKey = releaseRole._getBuffSrcKey(buffId)
        if self.hasBuff(buffId, buffSrcKey):
            self.removeBuff(buffId, buffSrcKey)

        if releaseRole.IsAvatar:
            releaseRoleGbId = releaseRole.gbId
        else:
            releaseRoleGbId = None
        self.buffDic.doAddBuff(self, buffId, level, duration, releaseRoleId, releaseRole.name, releaseRoleGbId,
                               gameconst.BuffSrcType.Combat, buffSrcKey, rootContext, kwargs)

        # 这里取一遍，因为addBuff里面会去结算，可能又触发删除buff的逻辑
        buffVal = self.getBuffByBuffId(buffId, buffSrcKey)
        if buffVal:
            self.onEffectEvent('onSelfBuff', releaseRoleId, self.id, effectEventCtx.BuffEventCtx(buffId))

            # if releaseRole:
                # self.sendCombatMsg(MBD.datas.getBuff, [buffVal.level, buffVal.getBuffName(buffVal.buffId)])
                # releaseRole.id != self.id and releaseRole.sendCombatMsg(MBD.datas.targetGetBuff,
                #                                                         [self.name, buffVal.level,
                #                                                          buffVal.getBuffName(buffVal.buffId)])

            buffVal = self.getBuffByBuffId(buffId, buffSrcKey)
            if buffVal:
                # 再取一遍，因为 onSelfbuff里面也可能删除buff
                self.broadcastAddBuffEvent(buffId, buffVal.getClientStream())

    def changeBuffLevel(self, buffId, changeLevel, releaseRoleId, duration=-1, rootContext=None, levelLimit=0,
                        autoHandleBuff=True):
        """修改buff层数"""
        DEBUG_MSG('changeBuffLevel::', buffId, changeLevel, releaseRoleId, duration, levelLimit, autoHandleBuff)
        if buffId not in buff_buff.datas:
            ERROR_MSG('changeBuffLevel:: buffId not in configTable', buffId)
            return False

        if self.isDie():
            return False

        _buffSrcKey = self._getBuffSrcKey(buffId, releaseRoleId)
        _buff = self.getBuffByBuffId(buffId, _buffSrcKey)

        # case1: 没有buff
        if not _buff:
            if not autoHandleBuff:
                ERROR_MSG('changeBuffLevel:: can\'t changeBuffLevel if buff not exist', buffId, changeLevel)
                return False

            if changeLevel <= 0:
                # Nothing to do here
                return True

            else:
                if levelLimit and levelLimit < changeLevel:
                    WARNING_MSG('changeBuffLevel:: 1 over level limit, reset level to limit', changeLevel, levelLimit)
                    changeLevel = levelLimit
                self.addBuff(buffId, changeLevel, releaseRoleId, duration, rootContext)
                return True

        buffLevel = _buff.level
        buffNewLevel = max(0, buffLevel + changeLevel)

        # case2: 新的buff层数<=0
        if buffNewLevel <= 0:
            if not autoHandleBuff:
                ERROR_MSG('changeBuffLevel:: can\'t changeBuffLevel if new buff level <= 0', changeLevel, buffNewLevel)
                return False
            self.removeBuff(buffId, _buffSrcKey)
            return True

        # default: 更新buff层数
        if levelLimit and levelLimit < buffNewLevel:
            DEBUG_MSG('changeBuffLevel:: 2 over level limit, reset level to limit', buffNewLevel, levelLimit)
            buffNewLevel = levelLimit
        _buff.overlayBuff(self, buffNewLevel, duration)
        self.allClientsOnUpdateBuff(buffId, _buff.getClientStream())
        return True

    def hasBuff(self, buffId, buffSrcKey=None):
        if buffId in self.buffDic and self.buffDic[buffId]:
            if buffSrcKey is None or buffSrcKey in self.buffDic[buffId]:
                return True
        return False

    def hasBuffTag(self, tag):
        return self.buffDic.hasBuffTag(tag)

    def getBuffLv(self, buffId, srcEnt=None):
        buffMap = self.buffDic.get(buffId, {})
        buffLv = 0
        srcEnt = srcEnt or self
        buffSrcKey = srcEnt._getBuffSrcKey(buffId)
        if buffSrcKey in buffMap:
            buffLv = buffMap[buffSrcKey].level
        return buffLv

    def _immuneDeathFinished(self, srcEntId, context):
        iInfo = self.getTempMiscProp(gameconst.AvatarProps.immuneDeath)
        if not iInfo:
            return
        if iInfo.immuneDeathFinishTimerId:
            iInfo.immuneDeathFinishTimerId = 0

        if iInfo.deadFuture:
            self.popTempMiscProp(gameconst.AvatarProps.immuneDeath)

        if iInfo.deadAfterImmunning:
            iInfo.status = gameconst.ImmuneDeathState.IMMUNE_FINISHED

            self.modifyHP(-self.hp, srcEntId, iInfo.srcType, iInfo.srcId, True, context)
        else:
            iInfo.status = gameconst.ImmuneDeathState.IMMUNE_VALID

        self._endBigWorldDuel(self)

    def cancelImmuneDeath(self):
        iInfo = self.getTempMiscProp(gameconst.AvatarProps.immuneDeath)
        if not iInfo:
            return
        if iInfo.immuneDeathFinishTimerId:
            self._cancelCallback(iInfo.immuneDeathFinishTimerId, gametimer.TIMER_TAG_IMMUNE_DEATH_FINISHED)
            iInfo.immuneDeathFinishTimerId = 0
        iInfo.status = gameconst.ImmuneDeathState.IMMUNE_VALID

    def isImmuneDeath(self):
        iInfo = self.getTempMiscProp(gameconst.AvatarProps.immuneDeath)
        if not iInfo:
            return False
        return bool(iInfo.status == gameconst.ImmuneDeathState.IMMUNE_DURING)

    def killSelf(self, sourceType):
        iInfo = self.getTempMiscProp(gameconst.AvatarProps.immuneDeath)
        if iInfo:
            iInfo.status = gameconst.ImmuneDeathState.IMMUNE_FINISHED
        self.modifyHP(-self.hp, self.id, sourceType, 0)
        self._endBigWorldDuel(self)

    def goDie(self, killer, srcType, srcId, forceDead=False, context=None):
        WARNING_MSG('goDie', killer.id, srcType, srcId, forceDead, context)
        if self.isDie():
            WARNING_MSG("goDie:: already dead", killer, srcType, srcId)
            return

        self.onEffectEvent('onDead', killer.id, self.id, effectEventCtx.EE_DEFAULT_CONTEXT)
        if not killer.IsCreation:
            killer.onEffectEvent('onKill', self.id, killer.id, effectEventCtx.EE_DEFAULT_CONTEXT)

        if srcType == gameconst.SourceType.Skill and killer.IsAvatar and srcId:
            killedBySkill = SSD.datas[srcId].get('zedNormalSkillID') or srcId
            skillVal = killer.getSkill(killedBySkill, reportError=False)
            if skillVal:
                skillVal.triggerRefreshSkillCD(killer)

        # : 防止时间触发时isDie()返回还未死亡
        self.setState(gameconst.State.Death)
        self.killChannelingSkill(gameconst.ChannelingBreak.SELF_DIE)
        self.killCastingSkill(gameconst.EndCasting.Dead)
        self.onDead(killer, srcType, srcId)

        iInfo = self.getTempMiscProp(gameconst.AvatarProps.immuneDeath)
        if iInfo:
            iInfo.status = gameconst.ImmuneDeathState.IMMUNE_VALID

        if killer.IsAICombatUnit:
            killer.removeHate(self.id)

    def modifyHP(self, hpVal, releaseRoleId, srcType, srcId, forceDead=False, context=None):
        if srcType == gameconst.SourceType.Item:
            hpVal = hpVal * self.getMoralEffectItemPercent()
        hpVal = int(hpVal)
        if self.isDie():
            return 0

        releaseRole = KBEngine.entities.get(releaseRoleId)
        # 自己可能传送到其他场景了，找不到来源entity正常的
        if not releaseRole:
            return 0

        if (hpVal > 0 and self.hp < self.fullHp) or (hpVal < 0 and self.hp > 0):
            self.onEffectEvent('onHPModify', releaseRoleId, self.id, effectEventCtx.HpEventCtx(hpVal))

        oldHp = self.hp
        curHp = self.hp + hpVal

        # 【【任务】支持boss濒死】
        # 锁血相关, 需要将self.hp 修改提前到最先
        if curHp > self.fullHp:
            self.hp = curHp = self.fullHp
        elif curHp < 0:
            self.hp = curHp = 0
        else:
            self.hp = curHp

        realReleaseRole = utils.getEntityRealEntity(releaseRole)
        lInfo = self.getTempMiscProp(gameconst.AvatarProps.lockMinHp)
        if lInfo and lInfo.isValid():
            if self.hp < lInfo.minHp:
                lInfo.effectTimes += 1
                self.hp = curHp = lInfo.minHp

        if hpVal:
            if self.IsAvatar:
                pass
                # self.flowCtrlDunAnyPlayerHpMonitorTrigger(int(oldHp), int(curHp), self.fullHp)
            elif hasattr(self, 'gameEntityId'):
                # 【【任务】新手剧情-新手村部分-NPC 添加buff】
                # 包括怪物/CNPC等可战斗实体都需要支持该节点
                self.flowCtrlMonsterHpMonitorTrigger(
                    utils.getGidFromGameEntityId(self.gameEntityId), int(oldHp), int(curHp), self.fullHp)
                pass

        iInfo = self.getTempMiscProp(gameconst.AvatarProps.immuneDeath)
        if iInfo:
            # 【【任务】支持boss濒死】
            # 修改curHp: 兼容原代码逻辑; 修改self.hp: 锁血相关, 需要将self.hp 修改提前到最先, 这里需求强制再赋值
            if not forceDead and curHp <= 0 and iInfo.status == gameconst.ImmuneDeathState.IMMUNE_VALID:
                self.hp = curHp = 1
                iInfo.status = gameconst.ImmuneDeathState.IMMUNE_DURING
                iInfo.srcType = srcType
                iInfo.srcId = srcId

                if releaseRoleId != self.id:
                    iInfo.lastEnemyId = releaseRoleId

                if iInfo.duration > 0:
                    if iInfo.immuneDeathFinishTimerId:
                        self._cancelCallback(iInfo.immuneDeathFinishTimerId, gametimer.TIMER_TAG_IMMUNE_DEATH_FINISHED)
                    iInfo.immuneDeathFinishTimerId = self._callback(iInfo.duration, '_immuneDeathFinished',
                                                                    (releaseRoleId, context),
                                                                    gametimer.TIMER_TAG_IMMUNE_DEATH_FINISHED)
                if not self.IsAvatar:
                    self.flowCtrlDunEntityimmuneDeathTrigger(utils.getGidFromGameEntityId(self.gameEntityId))
                if self.IsAvatar and realReleaseRole.IsAvatar and not self.hasTempMiscProp(gameconst.AvatarProps.isMoralValueChanged):
                    self.setTempMiscProp(gameconst.AvatarProps.isMoralValueChanged, realReleaseRole.isMoralValueChanged(self))

            elif iInfo.status == gameconst.ImmuneDeathState.IMMUNE_DURING:
                self.hp = curHp = 1
                if self.IsAvatar and realReleaseRole.IsAvatar and not self.hasTempMiscProp(gameconst.AvatarProps.isMoralValueChanged):
                    self.setTempMiscProp(gameconst.AvatarProps.isMoralValueChanged, realReleaseRole.isMoralValueChanged(self))

        if curHp <= 0 and self.IsAvatar and self.duelAttr.inFight():
            if self.duelAttr.isDuelEnemy(realReleaseRole) or realReleaseRole.id == self.id:
                self.hp = int(self.getDuelDeathHp(oldHp))
                duelFlag = self.duelAttr.duelFlagEnt()
                if duelFlag:
                    duelFlag.onAvatarDuelFailed(self.id)
                else:
                    ERROR_MSG('modifyHP:: duelFlagEntity not found', self.id)

        hpDelta = self.hp - oldHp

        if self.hp <= 0:
            self.goDie(releaseRole, srcType, srcId, forceDead, context)

        if self.IsAICombatUnit and self.aiController and self.hp == self.fullHp:
            self.aiController.onHpFull()

        return hpDelta

    def onDoDamage(self, destEntId, damageVal, absorbVal, srcType, srcId):
        host = utils.getHostEntity(self)
        targetHost = utils.getHostEntity(KBEngine.entities.get(destEntId))
        if targetHost and host.IsAvatar and targetHost.IsAvatar and host.id != targetHost.id:
            host.checkPKWithAvatar(targetHost)
            targetHost.checkBeAttackByAvatarPK(host)
            host.setHateRecord(targetHost.id)

    def onBeDamaged(self, dmgSrcEntityId, damageVal, absorbVal, srcType, srcId):
        srcTargetHost = utils.getHostEntity(KBEngine.entities.get(dmgSrcEntityId))
        host = utils.getHostEntity(self)
        if srcTargetHost and host and host.IsAvatar and srcTargetHost.IsAvatar and host.id != srcTargetHost.id:
            host.setHateRecord(srcTargetHost.id)

        channelingSkillVal = self.getChannelingSkillInfo()
        if channelingSkillVal:  # 引导时收到伤害
            interruptType = channelingSkillVal.getInterruptByAttack(channelingSkillVal.skillId)
            if interruptType == 0:  # 不能打断
                pass
            elif interruptType == 1 and random.uniform(0, 1) <= self.skillBroken:  # 按概率打断
                self.killChannelingSkill(gameconst.ChannelingBreak.BE_ATK)
            elif interruptType == 2:  # 必定打断
                self.killChannelingSkill(gameconst.ChannelingBreak.BE_ATK)

        castingSkillVal = self.getCastingSkillInfo()
        # 吟唱技能需要额外判断是否在吟唱状态，skillVal在吟唱+施法过程中都存在
        if castingSkillVal and self.hasState(gameconst.State.Casting):
            # 吟唱时收到伤害
            interruptType = castingSkillVal.getInterruptByAttack(castingSkillVal.skillId)
            if interruptType == 0:  # 不能打断
                pass
            elif interruptType == 1 and random.uniform(0, 1) <= self.skillBroken:  # 按概率打断
                self.killCastingSkill(gameconst.EndCasting.BeAttacked)
            elif interruptType == 2:  # 必定打断
                self.killCastingSkill(gameconst.EndCasting.BeAttacked)

    def modifyMP(self, mpVal, context=None):
        if context:
            srcType = context.getDmgSourceType()
            if srcType == gameconst.SourceType.Buff and context.parentContext:
                srcType = context.parentContext.getDmgSourceType()
            if srcType == gameconst.SourceType.Item:
                mpVal = mpVal * self.getMoralEffectItemPercent()
        mpVal = int(mpVal)
        if not mpVal:
            return

        curMp = self.mp + mpVal
        if curMp > self.fullMp:
            self.mp = self.fullMp
        elif curMp < 0:
            self.mp = 0
        else:
            self.mp = curMp

    def removeSkill(self, skillID):
        return self.skillDic.pop(skillID, None)

    def doActionOnChangeSlot(self, skillId, skillLv, bActive, bTakeSkill):
        if bTakeSkill:
            skill = self.takeSkill(skillId, skillLv)
        else:
            skill = self.getSkill(skillId, False, True)

        if not skill:
            return
        skill.doActionOnChangeSlot(self, bActive)

    def pressChargeSkill(self, srcEntityID, skillID):
        ERROR_MSG('pressChargeSkill not implemented')

    @utils.isMyself
    def cancelChargeSkill(self, exposed, skillId):
        ERROR_MSG('cancelChargeSkill not implemented')

    def enterFightingState(self):
        pass

    def leaveFightingState(self):
        pass

    def enterSprintingState(self):
        pass

    def leaveSprintingState(self):
        pass

    def getStateBitVector(self):
        return [self.state, self.state2]

    def setStateBitVector(self, stateVec):
        isSetState = False
        if self.state != stateVec[0]:
            self.state = stateVec[0]
            isSetState = True
        if self.state2 != stateVec[1]:
            self.state2 = stateVec[1]
            isSetState = True
        if isSetState:
            self.stateList = formula.getInt64VectorOnIndexes(self.getStateBitVector())

    def setState(self, state, reportErr=True, isInit=False):
        if state < 0:
            reportErr and ERROR_MSG("states is error:", state)
            return False

        """return True if state is exist"""
        if self.hasState(state) and not isInit:
            if state == gameconst.State.Fighting and self.IsAvatar:
                self.enterFightingState()
            return True

        eventId = CSD.datas[state].get('event')
        conflictRes = self.checkConflictState(eventId, remConflctState=False, isInit=isInit)
        if eventId and not conflictRes:
            # 现在设置状态前没有判断与当前状态是否冲突，可能会设置失败，这里打个trace检查这种情况
            reportErr and gameengine.reportCritical('setState fail', eventId, state, conflictRes.extra)

            return False

        if state == gameconst.State.Fighting:
            if not self.hasState(gameconst.State.Fighting):
                self.enterFightingState()
            else:
                return True

        elif state == gameconst.State.Sprinting:
            if not self.hasState(gameconst.State.Sprinting):
                self.enterSprintingState()
            else:
                return True

        elif state in gameconst.State.breakSkillStates:
            self.breakSkillByState()

        stateVec = self.getStateBitVector()
        formula.setInt64VectorBit(stateVec, state)

        rmStates = []
        stateBitsList = self.stateList
        stateBitsList.append(state)
        if eventId:
            for st in stateBitsList:
                if st != state:
                    val = conflict_conflict.datas[eventId].get(str(st))
                    if val == 0:
                        reportErr and ERROR_MSG("checkConflict false", eventId, state, st, self.state, stateBitsList)
                    elif val == 2:
                        formula.setInt64VectorBit(stateVec, st, on=False)
                        rmStates.append(st)

        self._onRemovedStateBefore(rmStates, state)
        self.setStateBitVector(stateVec)
        self._onRemovedState(rmStates, state)

        if state == CCDD.datas.MImmortal:
            self.removeBuffByKind(gameconst.BuffKind.MagicalDoT)
        elif state == CCDD.datas.PImmortal:
            self.removeBuffByKind(gameconst.BuffKind.PhysicalDoT)

        return True

    def removeState(self, state, removeReason=0):
        if state < 0:
            ERROR_MSG("states is error:", state)
            return

        if not self.hasState(state):
            return

        stateVec = self.getStateBitVector()
        formula.setInt64VectorBit(stateVec, state, on=False)

        self._onRemovedStateBefore([state], state, removeReason=removeReason)
        self.setStateBitVector(stateVec)
        self._onRemovedState([state], state, removeReason=removeReason)

    def removeStates(self, rmStates, byConflictState=-1):
        stateVec = self.getStateBitVector()

        for state in rmStates:
            formula.setInt64VectorBit(stateVec, state, on=False)

        self._onRemovedStateBefore(rmStates, byConflictState)
        self.setStateBitVector(stateVec)
        self._onRemovedState(rmStates, byConflictState)

    def hasState(self, state):
        if state < 0:
            ERROR_MSG("states is error:", state)
            return False
        if state >= 64:
            return (self.state2 >> (state - 64)) & 1 > 0
        else:
            return (self.state >> state) & 1 > 0

    def _onRemovedStateBefore(self, states, byConflictState=-1, removeReason=0):
        pass
        # for state in states:
        #     if state == gameconst.State.Moving:
        #         if self.IsAvatar:
        #             self.position = self.position

    def _onRemovedState(self, states, byConflictState=-1, removeReason=0):
        for state in states:
            if state == gameconst.State.Fighting:
                self.leaveFightingState()

            elif state == gameconst.State.autoFight:
                self._stopAutoCombat()

            elif state == gameconst.State.Moving and hasattr(self, 'removeMoveController'):
                self.removeMoveController()

            elif state == gameconst.State.Channeling or state == gameconst.State.moveChannel:
                DEBUG_MSG("removeState  killChannelingSkill ")
                if removeReason:
                    self.killChannelingSkill(removeReason)
                else:
                    self.killChannelingSkill(gameconst.ChannelingBreak.CONFLICT_STATE)

            elif state == gameconst.State.Casting:
                DEBUG_MSG("removeState  killCastingSkill ", byConflictState)
                if byConflictState >= 0 and byConflictState in (gameconst.State.Moving, gameconst.State.Idle):
                    self.killCastingSkill(gameconst.EndCasting.Move)
                elif byConflictState == gameconst.State.Death:
                    self.killCastingSkill(gameconst.EndCasting.Dead)
                # elif byConflictState == gameconst.State.Teleporting:
                #     self.killCastingSkill(gameconst.EndCasting.Teleporting)
                elif byConflictState == gameconst.State.clientPick:
                    self.killCastingSkill(gameconst.EndCasting.clientPick)
                else:
                    self.killCastingSkill(gameconst.EndCasting.ConflictState)

            elif state == gameconst.State.riding:
                self._onExitRiding(byConflictState)

            elif state == gameconst.State.clientPick:
                self._onExitClientPick()

            elif state == gameconst.State.GeneralAttack:
                if removeReason != gameconst.RemoveStateReason.SKILL_DONE:
                    self._breakGeneralSkill()

            elif state == gameconst.State.Shifting or state == gameconst.State.Dodging:
                self.endMovement()
            elif state == gameconst.State.Sprinting:
                self.leaveSprintingState()
            # elif self.IsAvatar and state == gameconst.State.UsingSkill:
            #     self.resetUsingSkills(gameconst.ResetSkillReason.SkillStateRemove)
            elif state == gameconst.State.Flying:
                self._callback(1, '_onRemoveFlyingState', (), gametimer.TIMER_TAG_ON_REMOVE_FLY_STATE)

            elif state == CCDD.datas.duel:
                self.leaveDuelState()

            buffTag = CSD.datas[state].get('buffTag')
            if buffTag:
                self.removeBuffByTag(buffTag)

    def _onRemoveCinemaPlaying(self, byConflictState):
        pass

    def _onRemoveFlyingState(self):
        self.topSpeed = gameconst.TopSpeedType.NormalTopSpeed

    @classmethod
    def clearAllCache(cls):
        cls._getConflictStatusName.cache_clear()
        cls._getConflictEventName.cache_clear()
        cls.getConflictEventCfgData.cache_clear()

    @staticmethod
    @functools.lru_cache(64)
    def _getConflictStatusName(stateId):
        return CSD.datas.get(stateId, {}).get('statusName', '')

    @staticmethod
    @functools.lru_cache(64)
    def _getConflictEventName(eventId):
        return conflict_conflict.datas[eventId]['eventName']

    @staticmethod
    @functools.lru_cache(64)
    def _getConflictPopupIndex(stateId):
        return CSD.datas.get(stateId, {}).get('popupIndex', 0)

    @staticmethod
    @functools.lru_cache(64)
    def getConflictEventCfgData(eventId):
        return conflict_conflict.datas[eventId]

    def checkConflictState(self, eventId, bMsg=True, remConflctState=False, isInit=False):
        if not eventId:
            return gameclass.BoolResult(True, -1)

        remState = []
        cfgData = self.getConflictEventCfgData(eventId)
        for state in self.stateList:
            val = cfgData.get(str(state))
            if val == 1:
                continue
            elif val == 0:
                bMsg and WARNING_MSG("has conflict eventId=[{}] state=[{}] val=[0]".format(eventId, state))
                return gameclass.BoolResult(False, state)
            elif val == 2 and remConflctState:
                remState.append(state)
            elif val == 3:
                bMsg and WARNING_MSG("has conflict eventId=[{}] state=[{}] val=[3]".format(eventId, state))
                return gameclass.BoolResult(False, state)
            elif MSG.datas.get(val, None):
                bMsg and WARNING_MSG("has conflict eventId=[{}] state=[{}] val=[{}]".format(eventId, state, val))
                return gameclass.BoolResult(False, state)

        # todo remove conflict state, new state continue gooooo
        if len(remState) > 0:
            self.removeStates(remState)

        return gameclass.BoolResult(True, -1)

    def getRandomPosition(self, center, radii):
        posList = self.getRandomPoints(center, radii, 1, 0)
        if not posList:
            return None

        return posList[0]

    def recordUseSkill(self, skillVal, targetId):
        pass

    def removeUseSkillRecord(self, skillId):
        pass

    def useSkillFinish(self, skillId):
        if self.IsAvatar and self.autoCombat == gameconst.AutoCombatState.Fighting:
            self.autoCombatCheckUseSkill(skillId)

    def _castSkillByServer(self):
        return False

    def doUseSkill(self, skillID, targetID, arr, isClient=False, compensateTime=0):
        DEBUG_MSG("doUseSkill ", skillID, targetID, arr, isClient, compensateTime)
        skill = self.getSkill(skillID)

        if skill is None:
            ERROR_MSG("Spell::doUseSkill(%i):skillID=%i not found" % (self.id, skillID))
            return False

        return self._useSkillBySkillObj(skill, targetID, arr, isClient, compensateTime)

    def _breakGeneralSkill(self):
        usingSkills = self.getTempMiscProp(gameconst.AvatarProps.currentUseSkill, default={})
        for sid in list(usingSkills.keys()):
            if sid not in usingSkills:
                continue

            sVal, tid = usingSkills[sid]
            if sVal.hasTag(gameconst.SkillTag.GeneralSkill):
                if sVal.isInSkill:
                    sVal.useSkillDone(self, 0, [], isSucc=False, doRemoveState=True)

                _child = sVal.childSkill()
                if _child and _child.isInSkill:
                    _child.useSkillDone(self, 0, [], isSucc=False, doRemoveState=True)

    def _useSkillBySkillObj(self, skill, targetID, arr, isClient=False, compensateTime=0):
        skillId = skill.skillId
        self.combatDebugMsg('_useSkillBySkillObj: skillId:%s, targetId:%s, skillArgs:%s', skillId, targetID, arr)
        # 走到这里如果不是Avatar，则一定是吟唱成功，如果是Avatar暂且认为吟唱过程成功，在canUse里会做校验
        castingSkillVal = self.getCastingSkillInfo()
        if castingSkillVal and self.hasState(gameconst.State.Casting):
            if castingSkillVal.skillId == skillId and castingSkillVal.isCastingSucc(delta=0.2):
                endReason = gameconst.EndCasting.Finished
            else:
                endReason = gameconst.EndCasting.OtherSkill

            self._endCastingSkill(endReason)

        realSkill, replaceSkill = skill.getRealSkillVal(self)
        ret = realSkill.checkUseSkill(self, targetID)

        if ret != gameconst.UseSkillCheck.CHEKC_OK:
            target = KBEngine.entities.get(targetID)
            if not (target and target.isDie()):
                WARNING_MSG("Spell::doUseSkill(%i):skillID=%i ret=%i tNextCast=%i" % (self.id, skillId, ret, skill.tNextCast))
            if ret & gameconst.UseSkillCheck.INVALID_TARGET and isClient:
                targetID = 0
            else:
                self.combatDebugMsg('_useSkillBySkillObj doUseSkill fail: targetId:%s, ret:%s, skillArgs:%s', targetID, ret, arr)
                self.client.onUseSkill(False, skillId, targetID, [], [])
                return False

        # 多段技能check时按当前段check，但是replaceSkill是false，表示使用时还调用第一段的使用
        # 因为后面段是第一段的子技能，子技能只能通过父技能使用
        if isClient and not realSkill.checkSkillArgs(arr):
            ERROR_MSG("doUseSkill: invalid skill args", realSkill.skillId, targetID, arr)
            if realSkill.isChangePositionSkill(realSkill.skillId):
                self.client.onUseSkill(False, skillId, targetID, [], [])
            return False

        if utils.hasSkillTag(skillId, gameconst.SkillTag.UltraSkill):
            self.resetUsingSkills(gameconst.ResetSkillReason.UltraSkill)

        if replaceSkill:
            self.recordUseSkill(realSkill, targetID)
            isSucc, actionCtx, effectedEntIds = realSkill.beginUseSkill(self, targetID, arr, compensateTime)
            isGeneral = realSkill.hasTag(gameconst.SkillTag.GeneralSkill)
        else:
            self.recordUseSkill(skill, targetID)
            isSucc, actionCtx, effectedEntIds = skill.beginUseSkill(self, targetID, arr, compensateTime)
            isGeneral = skill.hasTag(gameconst.SkillTag.GeneralSkill)

        if isSucc and not isGeneral:
            self._breakGeneralSkill()

        return isSucc

    def removeSkillState(self, skillVal):
        DEBUG_MSG("removeSkillState ", skillVal)
        skillVal._cancelTempTimer(self, 'removeSkillStateTimer', gametimer.TIMER_TAG_REMOVE_SKILL_STATE)
        skillState = skillVal.getSkillState()
        self.removeState(skillState)

    def delayCalcSkill(self, skillVal, targetId, arr, actionCtx, calcDelay, doRemoveState=True):
        # delay过程中如果有传送，skillVal不是skillDic里的值，这里重拿一次
        skill = self.getSkill(skillVal.skillId, reportError=False)
        # 如果getSkill没拿到，说明这种技能不是skillDic里的技能，就用iTimer里存的即可
        skill = skill or skillVal
        actionCtx.skillObj = skill
        if not skill:
            ERROR_MSG('delayCalcSkill: cannot get skill', skill.skillId, targetId)
            return

        skill._cancelTempTimer(self, 'delayCalcTimer', gametimer.TIMER_TAG_SKILL_DELAY_CALC)
        ignoreReasons = gameconst.UseSkillCheck.DELAY_CHECK_IGNORES
        if actionCtx.duringBigWorldDuel:
            ignoreReasons = gameconst.UseSkillCheck.BIGWORLD_DUEL_DELAY_CHECK_IGNORES

        if skill.checkUseSkill(self, targetId, ignoreReasons=ignoreReasons) != gameconst.UseSkillCheck.CHEKC_OK:
            skill.useSkillDone(self, targetId, arr, False, doRemoveState)
            return

        self._doUseSkill(skill, targetId, arr, actionCtx, calcDelay, doRemoveState)

    def _doUseSkill(self, skill, targetId, arr, actionCtx, calcDelay, doRemoveState=True):
        skill.applySkillEffect(self, targetId, arr, actionCtx, calcDelay, doRemoveState)

    def _onSkillCallback(self, skillVal, callbackName, args):
        skillVal.onTimerCallback(self, callbackName, args)

    def castingSkillInternal(self, skillID, targetID, arr, isClient=False):
        skill = self.getSkill(skillID, reportError=not isClient)

        self._castingSkillObjInternal(skill, targetID, arr, isClient)

    def _castingSkillObjInternal(self, skillObj, targetID, arr, isClient=False):
        if skillObj is None and not isClient:
            ERROR_MSG("_castingSkillObjInternal: invalid skill")
            return

        self.combatDebugMsg("_castingSkillObjInternal: skillId:%s, targetId:%s, skillArgs:%s", skillObj.skillId, targetID, arr)

        if self.hasState(gameconst.State.Casting):
            return

        if not self.checkConflictState(CCD.datas.cast):
            INFO_MSG('skill %d cannot use: checkConflict: %d' % (skillObj.skillId, CCD.datas.cast))
            return

        skillID = skillObj.skillId
        realSkillVal, replaceSkill = skillObj.getRealSkillVal(self)
        if replaceSkill:
            self._useSkillBySkillObj(realSkillVal, targetID, arr, isClient)
            return

        ignoreReasons = gameconst.UseSkillCheck.STATE_CONFLICT | gameconst.UseSkillCheck.NEED_CAST
        ret = skillObj.checkUseSkill(self, targetID, ignoreReasons=ignoreReasons)
        if ret != gameconst.UseSkillCheck.CHEKC_OK:
            if ret & gameconst.UseSkillCheck.INVALID_TARGET and isClient:
                targetID = 0
            else:
                INFO_MSG("Spell::castingSkill(%i): cannot spell skillID=%i, targetID=%i, code=%i" % (
                    self.id, skillID, targetID, ret))
                return

        self.removeState(gameconst.State.Moving)
        self.setState(gameconst.State.Casting)
        self.client and self.client.onUseCasting(self.id, skillID, targetID, arr, [])
        self.otherClients.onUseCasting(self.id, skillID, targetID, arr, [])
        self.setTempMiscProp(gameconst.AvatarProps.currentCastingSkill, skillObj)
        skillObj.startCasting(self, targetID, arr)

    def castingSkillCheck(self, targetID, arr, castPos):
        skillObj = self.getCastingSkillInfo()
        skillObj._cancelTempTimer(self, 'castingCheckTimer', gametimer.TIMER_TAG_CASTING_CHECK)

        if sMath.distance2DToCompareFrom3DPosition(castPos, self.position) > 1:
            self.killCastingSkill(gameconst.EndCasting.Move)
            return

        # 如果客户端出错或者其他原因，吟唱时间到了后长时间没有调用spellTarget真正放吟唱技能，这里做容错结束吟唱
        # 对于服务器控制的实体，不会走到这里
        if time.time() - skillObj.castingStartTime > skillObj.getCastingtimeMax(skillObj.skillId) + 1:
            self._endCastingSkill(gameconst.EndCasting.Finished)
            return

        timerId = self._callback(1, 'castingSkillCheck', (targetID, arr, castPos), gametimer.TIMER_TAG_CASTING_CHECK)
        skillObj.setTempData('castingCheckTimer', timerId)
        return

    def getCastingSkillInfo(self):
        curSkillInfo = self.getTempMiscProp(gameconst.AvatarProps.currentCastingSkill)

        return curSkillInfo

    def getChannelingSkillInfo(self):
        curSkillInfo = self.getTempMiscProp(gameconst.AvatarProps.currentChannelSkill)

        return curSkillInfo

    def killCastingSkill(self, reason):
        skillVal = self.getCastingSkillInfo()
        if not skillVal:
            return
        self._endCastingSkill(reason)
        self.allClients.onBreakCastingSkill(self.id, skillVal.skillId, 1)

    def _endCastingSkill(self, reason):
        castingSkillVal = self.getCastingSkillInfo()
        if not castingSkillVal:
            return

        if reason != gameconst.EndCasting.Finished:
            castingSkillVal.onCastingInterrupted(self, reason)

        self.popTempMiscProp(gameconst.AvatarProps.currentCastingSkill)
        self.removeState(gameconst.State.Casting)

        castingSkillVal.resetSkill(self, gameconst.ResetSkillReason.EndCasting)

    def channelingSkillTick(self, skillObj, targetID, arr, channelPos, actionCtx):
        skillId = skillObj.skillId
        self.popTempMiscProp(gameconst.AvatarProps.channelSkillTimer)
        skillObj.popTempData('channelingCalcTimer')
        cfgData = SSD.datas[skillId]

        isMoveSkill = skillObj.isMovingSkill(skillId)
        if sMath.distance2DToCompareFrom3DPosition(self.position, channelPos) > 1.0 and not isMoveSkill:
            self.combatDebugMsg('channelingSkillTick move: position:%s, channelPos:%s', self.position, channelPos)
            self.killChannelingSkill(gameconst.ChannelingBreak.MOVE)
            return

        target = KBEngine.entities.get(targetID)
        if skillObj.needReleaseTarget() and ((target and target.isDie()) or (targetID > 0 and not target)):
            self.combatDebugMsg('channelingSkillTick target is invalid: targetId:%s', targetID)
            self.killChannelingSkill(gameconst.ChannelingBreak.TARGET_DIE)
            return

        if self.isDie():
            self.killChannelingSkill(gameconst.ChannelingBreak.SELF_DIE)
            return

        effectTargetIds = skillObj.getEffectTargets(self, targetID, arr)
        skillObj.targetIds = effectTargetIds
        scopes = skillObj.getScope(skillObj.skillId)
        if not effectTargetIds:
            if not scopes or scopes == gameconst.SkillScope.TARGET_AUTO:
                if skillObj.channelCount == 0 and self.IsAvatar:
                    skillObj.setTempData('isChannelingEmpty', True)
                if not skillObj.getTempData('isChannelingEmpty', False):
                    self.killChannelingSkill(gameconst.EndCasting.MissingTarget)
                    return

        skillObj.channelCount += 1
        self.allClients.onUseChanneling(self.id, skillId, targetID, arr, effectTargetIds,
                                        skillObj.channelCount)

        isFinished = skillObj.channelCount >= skillObj.getChannelTime(skillObj.skillId)

        bulletTime = skillObj.calBulletTime(self, targetID)
        bulletTimer = self._callback(bulletTime, "channelingSkillEffect", (skillObj, targetID, arr, actionCtx, 0,
                                                                           channelPos),
                                     gametimer.TIMER_TAG_CHANNELING_SKILL_EFFECT)
        skillObj.setTempData('channelingBulletTimer', bulletTimer)

        channelInterval = max(cfgData.get('channelInterval') or 1, 0.3)
        if not isFinished:
            timerId = self._callback(channelInterval, 'channelingSkillTick', (skillObj, targetID, arr, channelPos,
                                                                              actionCtx),
                                     gametimer.TIMER_TAG_CHANNELING_CALC)
            skillObj.setTempData('channelingCalcTimer', timerId)
        self.combatDebugMsg('channelingSkillTick done: skillId:%s, state:%s, targetId:%s, channelCount:%s, channelInterval:%s, isFinished:%s',
                            skillId, self.state, targetID, skillObj.channelCount, channelInterval, isFinished)
        return

    def channelingSkillEffect(self, skillObj, targetId, skillArgs, actionCtx, calcDelay, channelPos):
        skillObj.applySkillEffect(self, targetId, skillArgs, actionCtx, calcDelay)
        skillObj.popTempData('channelingBulletTimer')
        isFinished = skillObj.channelCount >= skillObj.getChannelTime(skillObj.skillId)

        if isFinished:
            self.combatDebugMsg('channelingSkillEffect end: channelCount:%s, channelTime:%s',
                                skillObj.channelCount, skillObj.getChannelTime(skillObj.skillId))
            skillObj.onChannlingEffectEnd(self)
            return

    def killChannelingSkill(self, reason, isFinished=False, notifyClient=True):
        skillVal = self.getChannelingSkillInfo()
        if not skillVal:
            return

        skillVal.enterCDTime(self)
        self.client.onSetAddSkillCd(skillVal.skillId, float(skillVal.getCD(self)), float(skillVal.tNextCast), False, skillVal.getTempData('releaseTime', 0), skillVal.getTempData('totalReleaseCount', 0), skillVal.getTempData('releasedCount', 0))
        if reason != gameconst.ChannelingBreak.NORMAR_END:
            skillVal.onChannelingEnd(self, isFinished)
        notifyClient and self.allClients.onBreakChannelingSkill(self.id, skillVal.skillId, reason)

    def _endChannelingSkill(self, isFinished):
        skillVal = self.getChannelingSkillInfo()
        if not skillVal:
            return

        self.combatDebugMsg('_endChannelingSkill: skillId:%s', skillVal.skillId)
        self.popTempMiscProp(gameconst.AvatarProps.currentChannelSkill)

    def _executeSkillAction(self, skillId, context, calcDelay, actionFunc, target, duration=0):
        if not actionFunc:
            return True

        ret = None
        try:
            if not target or (target and target.isReal()):
                if target:
                    target.onEffectEvent('onFlashBeat', self.id, target.id, effectEventCtx.EE_DEFAULT_CONTEXT)
                ret = actionFunc(self, target, context)
        except Exception as e:
            gameengine.reportCritical('_executeSkillAction error:', self.id, skillId, str(e), context)

        actionFinished = True
        if ret is not None:
            actType, args = ret
            if actType == gameconst.SkillActionType.StagedAct:
                delay, = args
                hitChooseAgain = SSD.datas[skillId].get('HitChooseAgain')
                if hitChooseAgain:
                    context.skillObj.targetIds = []
                    skillArgs = context.skillArgs
                    realSkillArgs = skillArgs
                    positionSkillArgs = None
                    if context.skillObj.isChangePositionSkill(skillId):
                        realSkillArgs = list(skillArgs)[:-3]
                        positionSkillArgs = tuple(skillArgs[-3:])

                    effectedEntIds = context.skillObj.getEffectTargets(self, context.useTargetId, realSkillArgs,
                                                           positionSkillArgs=positionSkillArgs)
                    context.effectedEntIds = effectedEntIds
                context.skillObj.setupMulAttackAction(self, context, delay, calcDelay, duration + delay)
                context.actionProgress = gameconst.ActionProgressType.actionDoing
                actionFinished = False
            else:
                if context.actionProgress == gameconst.ActionProgressType.actionDoing:
                    actionFinished = False
                context.isLastActionStage = True
        else:
            context.isLastActionStage = True

        return actionFinished

    def doSkillAction(self, skillId, context, calcDelay, needUseCheck=False, checkIgnoreReasons=0, duration=0,
                      doRemoveState=True):
        skill = context.skillObj
        actionFunc = skill.getAction(skill.skillId)
        skillArgs = context.skillArgs
        if context.actionStage > 0:
            #多段技能重新随目标
            realSkillArgs = skillArgs
            positionSkillArgs = None
            if context.skillObj.isChangePositionSkill(skillId):
                realSkillArgs = list(skillArgs)[:-3]
                positionSkillArgs = tuple(skillArgs[-3:])

            effectedEntIds = context.skillObj.getEffectTargets(self, context.useTargetId, realSkillArgs,
                                                               positionSkillArgs=positionSkillArgs)
            context.effectedEntIds = effectedEntIds
        effectedEntIds = context.effectedEntIds
        effectedTargets = utils.getEntitiesByIds(effectedEntIds)
        actionFinished = True

        skillDamges = context.getCombatResult()
        ignoreImmortal = skill.hasTag(gameconst.SkillTag.IgnoreImmortal)
        doActionTogether = skill.hasTag(gameconst.SkillTag.DoActionTogether)
        skillDamges.damageInfo = []

        skill._cancelTempTimer(self, 'mulAttackActionTimer', gametimer.TIMER_TAG_DO_SKILL_ACTION)

        context.actionProgress = gameconst.ActionProgressType.actionDone
        if skill.getEffectTarget(skill.skillId) == 'None':
            actionFinished = self._executeSkillAction(skillId, context, calcDelay, actionFunc, None, duration)
        else:
            doActionTargets = []

            host = utils.getHostEntity(self)

            if needUseCheck:
                if effectedTargets:
                    for target in effectedTargets:
                        checkCode = skill.checkUseSkill(self, target.id, ignoreReasons=checkIgnoreReasons)
                        if checkCode == gameconst.UseSkillCheck.CHEKC_OK:
                            break
                    else:
                        skill.onSkillActionFinished(self, context.useTargetId, skillArgs, context, calcDelay, duration)
                        return actionFinished

            isAttackSkill = skill.isAttackSkill(skill.skillId)
            for target in effectedTargets:
                if target.isDestroyed:
                    continue

                if isAttackSkill and not target.hasState(gameconst.State.Fighting) and utils.isEnemy(self, target):
                    if target.IsAICombatUnit and target.aiController.canEnterFighting():
                        target.setState(gameconst.State.Fighting)

                if doActionTogether:
                    # 先不执行action，后面一起执行
                    doActionTargets.append(target)
                else:
                    actionFinished = self._executeSkillAction(skillId, context, calcDelay, actionFunc, target, duration)

            if doActionTogether:
                context.effectedEntIds = [e.id for e in doActionTargets]
                actionTarget = doActionTargets[0] if doActionTargets else None
                actionFinished = self._executeSkillAction(skillId, context, calcDelay, actionFunc, actionTarget,
                                                          duration)
            else:
                if not effectedTargets:
                    actionFinished = self._executeSkillAction(skillId, context, calcDelay, actionFunc, None, duration)

        if skillDamges.damageInfo and not self.isDestroyed:
            self.sendSkillDamage(skillDamges)
            skillDamges.damageInfo = []

        if actionFinished:
            skill.onSkillActionFinished(self, context.useTargetId, skillArgs, context, calcDelay, duration,
                                        doRemoveState)

        return actionFinished

    def _getAtkSkillDmgType(self, schoolType):
        eventId, hitType = 0, 0
        if schoolType == gameconst.SCHOOL_PHYSICAL:
            eventId = CCD.datas.pBeat
            hitType = gameconst.HitType.ImmuneDmg

        elif schoolType == gameconst.SCHOOL_MAGIC:
            eventId = CCD.datas.mBeat
            hitType = gameconst.HitType.ImmuneDmg

        # elif schoolType == gameconst.SCHOOL_ASSISTANT:
        #     eventId = CCD.datas.hBeat
        #     hitType = gameconst.HitType.ImmuneAssistantDmg

        return eventId, hitType

    def _attackActionBefore(self, target, context, ignoreType=False):
        if not target or target.isDie():
            DEBUG_MSG('attack miss target', context)
            return False

        if not ignoreType:
            attackSrcEnt = context.getSrcEntity()
            if attackSrcEnt is None:
                WARNING_MSG("_attackActionBefore has no src entity")
                return False

            if not utils.checkTargetType("Enemy", attackSrcEnt, target):
                WARNING_MSG("_attackActionBefore checkTargetType error", attackSrcEnt.id, target.id)
                return False

        dmgSchoolType = 0
        ignoreImmortal = False
        if context.actionType == actionContext.ACTION_USE_SKILL:
            skill = self._getSkillByActionContext(context)
            dmgSchoolType = skill.getClassTag(self)
            ignoreImmortal = skill.hasTag(gameconst.SkillTag.IgnoreImmortal)

        elif context.actionType in (actionContext.ACTION_CREATION_LOOP, actionContext.ACTION_CREATION_COMMON):
            dmgSchoolType = CRD.datas.get(context.creationId, {}).get('classTag', 0)

        elif context.actionType in (actionContext.ACTION_AUREOLE,):
            dmgSchoolType = AAD.datas.get(context.aureoleId, {}).get('classTag', 0)

        elif context.actionType in (actionContext.ACTION_BUFF_TICK, actionContext.ACTION_BUFF_END,
                                    actionContext.ACTION_BUFF_EFFECT) and context.getBuffObj():
            dmgSchoolType = BBD.datas.get(context.buffId, {}).get('classTag', 0)

        if dmgSchoolType:
            skillDamges = context.getCombatResult()
            eventId, hitType = self._getAtkSkillDmgType(dmgSchoolType)

            if eventId:
                conflictResult = target.checkConflictState(eventId, bMsg=False, remConflctState=True)
                if not conflictResult and conflictResult.extra in (
                        CCDD.datas.PImmortal, CCDD.datas.MImmortal) and not ignoreImmortal:
                    if hitType not in gameconst.HitType.zeroFilter:
                        skillDamges.damageInfo.append(combatSkill.SkillDamageVal(target.id, 0, hitType))
                    return False

        return True

    def onModifyShieldVal(self, val, releaseRoleId, srcType, srcId):
        pass

    def getHost(self):
        return None

    def getFirstHost(self, num=1):
        if num == 3:
            return self

        if self.IsCreation or self.IsSummon or self.IsPet or self.IsAvatarMirror:
            host = self.getHost()
            if host:
                return host.getFirstHost(num + 1)

        return self

    def calcAtkStats(self, target, context, dmg):
        if not dmg:
            return

        if self.IsAvatarMirror or self.IsSummon or self.IsCreation:
            host = self.getHost()
            host and host.IsAvatar and host.calcAtkStats(target, context, dmg)
        elif self.IsPet:
            host = self.getHost()
            host and host.IsAvatar and host.calcPetAtkStats(dmg)

    def calcBeHurtStats(self, target, context, dmgResult):
        if not dmgResult.hurtDmg:
            return

        if self.IsSummon:
            host = self.getHost()
            host and host.IsAvatar and host.calcBeHurtStats(target, context, dmgResult)


    def calcHealStats(self, target, context, hpDelta):
        if not hpDelta:
            return

        if self.IsAvatarMirror or self.IsSummon or self.IsCreation:
            host = self.getHost()
            host and host.IsAvatar and host.calcHealStats(target, context, hpDelta)

    def _transferHostDmg(self, dmgSrcEnt, toEnt, context, totalDmg):
        if not toEnt or not toEnt.IsCombatUnit:
            return 0

        transferDmg = int(toEnt.shareMasterDmg * totalDmg)
        if transferDmg > 0:
            transferDmg = -toEnt.modifyHP(-transferDmg, dmgSrcEnt.id, context.getDmgSourceType(),
                                          context.getDmgSourceId())

        return transferDmg

    def applyDmgActionResult(self, target, context, dmgResult):
        self.combatDebugMsg('applyDmgActionResult: sourceId:%s, targetId:%s, context:%s, dmgResult:%s', context.getDmgSourceId(), target.id, context, dmgResult)
        skillDamges = context.getCombatResult()
        if not skillDamges:
            ERROR_MSG('unexpected heal action context', context)
            skillDamges = combatSkill.SkillDamges(self.id, context.getDmgSourceType(), context.getDmgSourceId())

        # 是否命中
        dmgResult.dmg = int(dmgResult.dmg)
        dmgResult.hurtDmg = int(dmgResult.hurtDmg)
        dmgResult.hpSuck = int(dmgResult.hpSuck)
        dmgResult.dmgType = int(dmgResult.dmgType)
        dmgResult.atkType = int(dmgResult.atkType)
        DEBUG_MSG("applyDmgActionResult", dmgResult.dmg, dmgResult.hurtDmg, dmgResult.hpSuck, dmgResult.dmgType, dmgResult.atkType, dmgResult.calcShield)
        # 如果血量被锁定了，就不分摊伤害吸血什么的，也不跳数字了
        if target.getTempMiscProp(gameconst.AvatarProps.isHpLocked, False):
            return

        if target.isDie():
            return

        dmg = realDmgVal = dmgResult.dmg
        absorbDamageDetail = {}

        dmgSrcEnt = context.getSrcEntity() or self
        # AvatarMirror,Pet，召唤物都算自己的，创生算主人的
        if dmgSrcEnt.IsCreation:
            dmgSrcEnt = dmgSrcEnt.getHost() or dmgSrcEnt

        # 分摊伤害
        # transferedSum = 0
        # transferToTgts = target.cloneList + target.petList
        # if target.IsAvatar:
        #     transferToTgts.append(target.lingShouId)

        # for tid in transferToTgts:
        #     t = KBEngine.entities.get(tid)
        #     if realDmgVal > 0:
        #         transferedDmg = target._transferHostDmg(dmgSrcEnt, t, context, dmg)
        #         realDmgVal = max(realDmgVal - transferedDmg, 0)
        #         transferedSum += transferedDmg
        #     else:
        #         break
        #
        # transferedSum and skillDamges.damageInfo.append(
        #     combatSkill.SkillDamageVal(target.id, transferedSum, gameconst.HitType.ShareDmg))

        dmgAfterTransfer = realDmgVal

        # 护盾吸收
        shieldAbsorbVal = 0
        if dmgResult.calcShield:
            target.onEffectEvent('onBeatShield', self.id, target.id, effectEventCtx.HpEventCtx(dmgAfterTransfer))
            realDmgVal, absorbDamageDetail = target.absorbShieldWithDetails(dmgAfterTransfer)
            shieldAbsorbVal = dmgAfterTransfer - realDmgVal
            if realDmgVal == 0 and shieldAbsorbVal:
                # 全被吸收
                skillDamges.damageInfo.append(
                    combatSkill.SkillDamageVal(target.id, shieldAbsorbVal, gameconst.HitType.Absorb))
            if shieldAbsorbVal > 0:
                target.onModifyShieldVal(shieldAbsorbVal, dmgSrcEnt.id, context.getDmgSourceType(),
                                         context.getDmgSourceId())

        # 增加焚心值, 由于modifyHp的时候会造成切磋状态改变，所以要放在modifyHp之前
        self.onDoDamage(target.id, realDmgVal, shieldAbsorbVal, context.getDmgSourceType(), context.getDmgSourceId())

        # 真实扣血
        recordDmgVal = 0
        suckHpVal = 0
        if realDmgVal >= 0:
            _realHpDelta = target.modifyHP(-realDmgVal, dmgSrcEnt.id, context.getDmgSourceType(), context.getDmgSourceId(),
                                context=context)
            recordDmgVal = abs(_realHpDelta)

            if _realHpDelta < 0:
                host = utils.getHostEntity(self)
                targetHost = utils.getHostEntity(target)
                if targetHost \
                        and not host.isDie() \
                        and not host.hasState(CCDD.datas.relive) \
                        and host.id != targetHost.id \
                        and context.getDmgSourceType() == gameconst.SourceType.Skill:
                    host.setState(gameconst.State.Fighting)
                    if not (targetHost.isDie() or targetHost.hasState(CCDD.datas.relive)):
                        targetHost.setState(gameconst.State.Fighting)

            if dmgResult.atkType == gameconst.SkillAttackType.ATTACK_NORMAL:
                # 普通伤害
                if realDmgVal:
                    if hasattr(context, 'isCombo'):
                        skillDamges.damageInfo.append(combatSkill.SkillDamageVal(target.id, realDmgVal, gameconst.HitType.ComboHit))
                    else:
                        skillDamges.damageInfo.append(combatSkill.SkillDamageVal(target.id, realDmgVal, gameconst.HitType.Hit))

            elif dmgResult.atkType == gameconst.SkillAttackType.ATTACK_DODGE:
                # 被部分闪避
                target.onEffectEvent('onDodge', self.id, target.id, effectEventCtx.EE_DEFAULT_CONTEXT)
                skillDamges.damageInfo.append(
                    combatSkill.SkillDamageVal(target.id, realDmgVal, gameconst.HitType.Miss))

            elif dmgResult.atkType == gameconst.SkillAttackType.ATTACK_CRIT:
                # 暴击伤害
                self.onEffectEvent('onFatal', self.id, target.id, effectEventCtx.EE_DEFAULT_CONTEXT)
                if realDmgVal:
                    if hasattr(context, 'isCombo'):
                        skillDamges.damageInfo.append(combatSkill.SkillDamageVal(target.id, realDmgVal, gameconst.HitType.ComboCrit))
                    else:
                        skillDamges.damageInfo.append(combatSkill.SkillDamageVal(target.id, realDmgVal, gameconst.HitType.Crit))

            else:
                ERROR_MSG('unknow attack type', target.id, context, dmgResult)

            if dmgResult.hpSuck:
                # 吸血
                suckHpVal = dmgSrcEnt.modifyHP(dmgResult.hpSuck, dmgSrcEnt.id, context.getDmgSourceType(),
                                               context.getDmgSourceId())
                dmgSrcEnt.onEffectEvent('onBloodSuck', dmgSrcEnt.id, target.id,
                                        effectEventCtx.HpEventCtx(dmgResult.hpSuck))
                if dmgResult.hpSuck:
                    skillDamges.damageInfo.append(
                        combatSkill.SkillDamageVal(dmgSrcEnt.id, dmgResult.hpSuck, gameconst.HitType.HPRecover))

            # effect里造成的血量伤害不触发onHit，否则攻击附带xxx效果会死循环
            if context.actionType not in (actionContext.ACTION_BUFF_EFFECT, actionContext.ACTION_EVENT_EFFECT):
                dmgSrcEnt.onEffectEvent('onHit', self.id, target.id,
                                        effectEventCtx.HpEventCtx(realDmgVal, dmgResult.dmgType))
                if not target.IsCreation:
                    target.onEffectEvent('onBeat', self.id, target.id, effectEventCtx.HpEventCtx(realDmgVal))

        target.onBeDamaged(dmgSrcEnt.id, realDmgVal, shieldAbsorbVal, context.getDmgSourceType(),
                           context.getDmgSourceId())

        sDmgSrcEnt = context.getSrcEntity()
        _srcIsSelf = True if sDmgSrcEnt and (sDmgSrcEnt.IsAvatar or sDmgSrcEnt.isBot()) else False
        sDmgSrcEnt = sDmgSrcEnt or self
        if sDmgSrcEnt.IsCreation or sDmgSrcEnt.IsSummon or sDmgSrcEnt.IsPet or sDmgSrcEnt.IsAvatarMirror:
            sDmgSrcEnt = sDmgSrcEnt.getFirstHost() or sDmgSrcEnt

        if sDmgSrcEnt.IsAvatar or sDmgSrcEnt.isBot():
            recordDmgVal += shieldAbsorbVal
            if recordDmgVal < 0:
                recordDmgVal = 0
            # report to battleFieldDungeon

        target.calcBeHurtStats(dmgSrcEnt, context, dmgResult)
        dmgSrcEnt.calcAtkStats(target, context, dmg)
        dmgSrcEnt.calcHealStats(dmgSrcEnt, context, suckHpVal)

        self.sendDmgMsgs(target, context, dmgResult, absorbDamageDetail, realDmgVal)

        # 【切磋会把对方打死】
        # 需要再技能Action后在清理切磋
        # self._endBigWorldDuel(target)

    def _endBigWorldDuel(self, target):
        pass
        # tbInfo = target.bigWorldDuelCacheInfo if target.IsAvatar else None
        # if tbInfo and tbInfo.duelStatus == gameconst.BigWorldDuelStatus.END:
        #     duelFlagEntId = target.getTempMiscProp(gameconst.AvatarProps.bigWorldDuelTempCacheVal).duelFlagEntId
        #     duelFlagEnt = KBEngine.entities.get(duelFlagEntId)
        #     if not duelFlagEnt:
        #         gameengine.reportCritical("FATAL when end big world duel", target.gbId, self.gbId)
        #     else:
        #         duelFlagEnt.onAvatarFailedInBigWorldDuel(target.id, tbInfo.duelSide)

    def sendDmgMsgs(self, target, context, dmgResult, absorbDamageDetail, realDmgVal):
        ctx = context or context.parentContext
        dmgDesc = gameconst.SKILL_DMG_DESC[dmgResult.dmgType]

        self.combatDebugMsg('sendDmgMsg: sourceId:%s, targetId:%s, context:%s, dmgResult:%s, absorbDamageDetail:%s, realDmgVal:%s',
                            context.getDmgSourceId(), target.id, ctx, dmgResult, absorbDamageDetail, realDmgVal)

        if ctx.actionType == actionContext.ACTION_USE_SKILL:
            skillName = context.skillObj.getSkillName(context.skillObj.skillId)
            dmgSrcEnt = KBEngine.entities.get(ctx.casterEntId)
            if not dmgSrcEnt:
                return

            # for buffId, offsetVal in absorbDamageDetail.items():
            #     dmgSrcEnt.sendCombatMsg(MBD.datas.beAbsorbed,
            #                             [skillName, offsetVal, target.name, buff.Buff.getBuffName(buffId)])
            #     target.sendCombatMsg(MBD.datas.absorb,
            #                          [dmgSrcEnt.name, skillName, offsetVal, buff.Buff.getBuffName(buffId)])

            if realDmgVal <= 0:
                return

            if dmgResult.hpSuck:
                # if dmgResult.atkType == gameconst.SkillAttackType.ATTACK_NORMAL:
                #     # 普通伤害
                #     dmgSrcEnt.sendCombatMsg(MBD.datas.bloodsuck,
                #                             [skillName, target.name, realDmgVal, dmgDesc, dmgResult.hpSuck])
                #     target.sendCombatMsg(MBD.datas.targetBloodsuck,
                #                          [dmgSrcEnt.name, skillName, realDmgVal, dmgDesc, dmgResult.hpSuck])
                #
                # elif dmgResult.atkType == gameconst.SkillAttackType.ATTACK_DODGE:
                #     # 被部分闪避
                #     self.sendCombatMsg(MBD.datas.beDodgedBloodsuck,
                #                        [skillName, target.name, realDmgVal, dmgDesc, dmgResult.hpSuck])
                #     target.sendCombatMsg(MBD.datas.dodgeBloodsuck,
                #                          [self.name, skillName, realDmgVal, dmgDesc, dmgResult.hpSuck])
                #     pass
                #
                # elif dmgResult.atkType == gameconst.SkillAttackType.ATTACK_CRIT:
                #     dmgSrcEnt.sendCombatMsg(MBD.datas.fatalBloodsuck,
                #                             [skillName, target.name, realDmgVal, dmgDesc, dmgResult.hpSuck])
                #     target.sendCombatMsg(MBD.datas.targetFatalBloodsuck,
                #                          [dmgSrcEnt.name, skillName, realDmgVal, dmgDesc, dmgResult.hpSuck])
                pass
            else:
                # if dmgResult.atkType == gameconst.SkillAttackType.ATTACK_NORMAL:
                #     # 普通伤害
                #     dmgSrcEnt.sendCombatMsg(MBD.datas.hit, [skillName, target.name, realDmgVal, dmgDesc])
                #
                #     target.sendCombatMsg(MBD.datas.targetHit, [dmgSrcEnt.name, skillName, realDmgVal, dmgDesc])
                # elif dmgResult.atkType == gameconst.SkillAttackType.ATTACK_DODGE:
                #     # 被部分闪避
                #     self.sendCombatMsg(MBD.datas.beDodged, [skillName, target.name, realDmgVal, dmgDesc])
                #     target.sendCombatMsg(MBD.datas.dodge, [self.name, skillName, realDmgVal, dmgDesc])
                #     pass
                #
                # elif dmgResult.atkType == gameconst.SkillAttackType.ATTACK_CRIT:
                #     dmgSrcEnt.sendCombatMsg(MBD.datas.fatal, [skillName, target.name, realDmgVal, dmgDesc])
                #     target.sendCombatMsg(MBD.datas.targetFatal, [dmgSrcEnt.name, skillName, realDmgVal, dmgDesc])
                pass

        elif ctx.actionType in (
                actionContext.ACTION_BUFF_END, actionContext.ACTION_BUFF_TICK, actionContext.ACTION_BUFF_EFFECT):
            buffName = buff.Buff.getBuffName(ctx.buffId)
            dmgSrcEnt = KBEngine.entities.get(ctx.srcEntId)

            # if dmgResult.atkType == gameconst.SkillAttackType.ATTACK_NORMAL:
            #     # 普通伤害
            #     dmgSrcEnt and dmgSrcEnt.sendCombatMsg(MBD.datas.targetGetBuffDamage,
            #                                           [ctx.buffLevel, buffName, target.name, realDmgVal, dmgDesc])
            #     target.sendCombatMsg(MBD.datas.getBuffDamage, [ctx.buffLevel, buffName, realDmgVal, dmgDesc])
            #
            # elif dmgResult.atkType == gameconst.SkillAttackType.ATTACK_DODGE:
            #     # 被部分闪避
            #     dmgSrcEnt and dmgSrcEnt.sendCombatMsg(MBD.datas.targetGetBuffDodgeDamage,
            #                                           [ctx.buffLevel, buffName, target.name, realDmgVal, dmgDesc])
            #     target.sendCombatMsg(MBD.datas.getBuffDodgeDamage, [ctx.buffLevel, buffName, realDmgVal, dmgDesc])
            #     pass
            #
            # elif dmgResult.atkType == gameconst.SkillAttackType.ATTACK_CRIT:
            #     dmgSrcEnt and dmgSrcEnt.sendCombatMsg(MBD.datas.targetGetBuffFatalDamage,
            #                                           [ctx.buffLevel, buffName, target.name, realDmgVal, dmgDesc])
            #     target.sendCombatMsg(MBD.datas.getBuffFatalDamage, [ctx.buffLevel, buffName, realDmgVal, dmgDesc])

    def _healActionBefore(self, target, context, ignoreType=False):
        if not ignoreType:
            if not target or target.isDie():
                WARNING_MSG('target miss ', context)
                return False
            healSrcEnt = context.getSrcEntity()
            if healSrcEnt is None:
                WARNING_MSG("_healActionBefore has no src entity")
                return False

            if target and not utils.checkTargetType("Friend", healSrcEnt, target):
                WARNING_MSG("_healActionBefore checkTargetType error", healSrcEnt.id, target.id)
                return False
        # 有益的action目前改为必定能加，无视魔免
        return True

    def addHealHate(self, hpDelta, target, context):
        skillId = 0
        if context.actionType in (actionContext.ACTION_USE_SKILL,):
            skillId = context.skillId
        elif context.parentContext and context.parentContext.actionType in (actionContext.ACTION_USE_SKILL,):
            skill = self._getSkillByActionContext(context.parentContext)
            skillId = context.parentContext.skillId
        else:
            return

        if skillId > 0 and hpDelta > 0 and self.id != target.id and not self.isDie() and self.spaceNo == target.spaceNo:
            hateRecord = target.getTempMiscProp(gameconst.AvatarProps.hateRecord, {})
            for mEid in list(hateRecord.keys()):
                ent = KBEngine.entities.get(mEid)
                if not ent:
                    continue
                if not ent.isDie() and ent.spaceNo == self.spaceNo and hasattr(ent, 'aiController'):
                    skillHateRatio = SSD.datas[skillId].get('skillHateRatio', 0.1)
                    ent.aiController and ent.aiController.increaseHate(self.id, hpDelta * skillHateRatio)

    def applyHealActionResult(self, target, context, healResult: combatSkill.HealResult):
        if not target:
            return

        skillDamges = context.getCombatResult()
        if not skillDamges:
            skillDamges = combatSkill.SkillDamges(self.id, context.getDmgSourceType(), context.getDmgSourceId())

        # 如果血量被锁定了，就不分摊伤害吸血什么的，也不跳数字了
        if target.getTempMiscProp(gameconst.AvatarProps.isHpLocked, False):
            return

        healSrcEnt = context.getSrcEntity() or self
        _srcIsSelf = True if healSrcEnt and (healSrcEnt.IsAvatar or healSrcEnt.isBot()) else False
        if healSrcEnt.IsCreation or healSrcEnt.IsSummon or healSrcEnt.IsAvatarMirror or healSrcEnt.IsPet:
            healSrcEnt = healSrcEnt.getFirstHost() or healSrcEnt

        oldHp = target.hp
        hpDelta = 0
        if healResult.healVal > 0:
            if target:
                mapData = GPGPD.datas.get(formula.getMapId((self.spaceNo)), {})
                ratio = 1

                healResult.healVal = int(healResult.healVal * ratio)
                srcType = context.getDmgSourceType()
                if srcType == gameconst.SourceType.Buff and context.parentContext:
                    srcType = context.parentContext.getDmgSourceType()
                hpDelta = target.modifyHP(healResult.healVal, self.id, srcType,
                                          context.getDmgSourceId())
                if hpDelta:
                    if healSrcEnt and healSrcEnt.IsAvatar and context.getDmgSourceType() == gameconst.SourceType.Skill:
                        healSrcEnt.setState(gameconst.State.Fighting)

                self.addHealHate(hpDelta, target, context)

                healResult.healVal = hpDelta

            if hpDelta:
                if healResult.isCrit:
                    skillDamges.damageInfo.append(
                        combatSkill.SkillDamageVal(target.id, hpDelta, gameconst.HitType.HealCrit))
                else:
                    skillDamges.damageInfo.append(
                        combatSkill.SkillDamageVal(target.id, hpDelta, gameconst.HitType.HPRecover))

        self.calcHealStats(target, context, hpDelta)

    def displacedBySkill(self, srcEntityId, pos, speed, timeEx, context=None):
        src = KBEngine.entities.get(srcEntityId)
        if not src:
            return False

        _ret = self.checkConflictState(CCD.datas.bePushed, True)
        if not _ret:
            if _ret.extra == CCDD.datas.Bating and not self.IsMonster:
                skillDamges = context.getCombatResult()
                if skillDamges:
                    skillDamges.damageInfo.append(
                        combatSkill.SkillDamageVal(
                            self.id,
                            0,
                            gameconst.HitType.ImmuneDisplacement))
            return False

        realDist = sMath.distance2D(self.position, pos)
        yaw = sMath.getYawFromDirection(Math.Vector3(src.position) - Math.Vector3(pos))

        oldCollidable = self.collidable
        self.collidable = False
        self.direction = (0.0, 0.0, yaw)

        self.bePushedSpeed = speed
        if self.hasState(gameconst.State.bePushed):
            self._cancelCallback(self._displaceTimer, gametimer.TIMER_TAG_DISPLACED_BY_SKILL_DONE)
        self.setState(gameconst.State.bePushed)
        self.controlledBy = None
        self.moveToPoint(pos, speed, 0, (), False, 0)

        # 不能完全依赖onMoveOver恢复，过程中可能传送或者被别的打断，如果没恢复过来客户端就完全操作不了了
        if realDist <= 0 or speed <= 0:
            pushTime = timeEx
        else:
            pushTime = realDist / speed + timeEx
        self._displaceTimer = self._callback(pushTime, '_displacedBySkillDone', (srcEntityId, oldCollidable),
                                             gametimer.TIMER_TAG_DISPLACED_BY_SKILL_DONE, '_displaceTimer')
        return True

    def _displacedBySkillDone(self, srcEntityId, oldCollidable):

        self.controlledBy = self.base
        self.collidable = oldCollidable
        self.removeState(gameconst.State.bePushed)

    # def setControl(self, controller):
    #     if self.controlledBy != controller:
    #         self.controlledBy = controller
    #     self.topSpeed = 50.0

    def getCreationCombatProps(self):
        props = {}

        inheritList = ['baseMinPhysicalAtk', 'adjMinPhysicalAtk', 'adjMinPhysicalAtkAbs', 'baseMaxPhysicalAtk',
                       'adjMaxPhysicalAtk', 'adjMaxPhysicalAtkAbs','baseMinMagicAtk', 'adjMinMagicAtk', 'adjMinMagicAtkAbs',
                       'baseMaxMagicAtk', 'adjMaxMagicAtk', 'adjMaxMagicAtkAbs', 'baseHit', 'adjHit', 'baseFatal',
                       'adjFatal', 'baseMortal', 'adjMortal', 'baseStunEnh',
                       'adjStunEnh', 'baseSilentEnh', 'adjSilentEnh', 'baseKnockEnh', 'adjKnockEnh', 'baseDebilityEnh',
                       'adjDebilityEnh', 'baseFrozenEnh', 'adjFrozenEnh'
                       ]

        for propName in inheritList:
            props[propName] = self.getProp(propName)

        return props

    def getSummonCloneCombatProps(self):
        props = {}

        inheritList = ['baseFullHp', 'adjFullHp', 'adjFullHpAbs', 'mulFullHp', 'minPhysicalAtk', 'baseMinPhysicalAtk',
                       'adjMinPhysicalAtk', 'adjMinPhysicalAtkAbs', 'maxPhysicalAtk', 'baseMaxPhysicalAtk', 'adjMaxPhysicalAtk',
                       'adjMaxPhysicalAtkAbs', 'minMagicAtk', 'baseMinMagicAtk', 'adjMinMagicAtk', 'adjMinMagicAtkAbs',
                       'maxMagicAtk', 'baseMaxMagicAtk', 'adjMaxMagicAtk', 'adjMaxMagicAtkAbs',
                       'adjFatal',
                       'baseAntiFatal',
                       'adjAntiFatal', 'baseMortal', 'adjMortal', 'baseAntiMortal',
                       'adjAntiMortal',
                       ]
        # 没有被定义和使用的属性,先移出来,不然报错
        # 'mulHit', 'mulDodge', 'baseDodgeDmg', 'adjDodgeDmg',
        # 'mulDodgeDmg', 'mulAntiFatal', 'mulMortal', 'mulAntiMortal'

        for propName in inheritList:
            props[propName] = self.getProp(propName)

        return props

    def getTargetByViewRadius(self):
        if self.IsAvatar:
            return self.getViewRadius()
        return gameconst.DEFAULT_AOI

    def getTargetIdsByTargetType(self, targetString):
        entityIds = []
        if self.isDestroyed:
            return entityIds
        if not self.useTargetTypeCacheFlag:
            viewRadius = self.getTargetByViewRadius()
            for e in self.entitiesInRange(viewRadius):
                if e.IsCombatUnit:
                    utils.isEnemy(self, e)
                    utils.isFriend(self, e)
            self.useTargetTypeCacheFlag = True
            self.stopCacheTargetTypeTimeId = self._callback(30, 'resetTargetTypeCacheFlag', (),
                                                            gametimer.TIMER_TAG_SET_TARGET_TYPE_CACHE_FLAG,
                                                            'stopCacheTargetTypeTimeId')
            if not self.checkTargetTypeTimeId:
                self.checkTargetTypeTimeId = self.pyAddTimer(5, 5, gametimer.CHECK_TARGET_TYPE_TIMER)
        else:
            if self.stopCacheTargetTypeTimeId:
                self._cancelCallback(self.stopCacheTargetTypeTimeId, gametimer.TIMER_TAG_SET_TARGET_TYPE_CACHE_FLAG)
                self.stopCacheTargetTypeTimeId = self._callback(30, 'resetTargetTypeCacheFlag', (),
                                                                gametimer.TIMER_TAG_SET_TARGET_TYPE_CACHE_FLAG,
                                                                'stopCacheTargetTypeTimeId')

        if targetString == "None":
            entityIds = list(self.enemyCacheSet.union(self.notEnemyCacheSet, {self.id}))

        elif targetString == "PlayerExTarget":
            if self.IsMonster and self.aiController and self.aiController.hateDict:
                maxHateTargetId, maxHateTargetHate = self.aiController.hateDict.getFirstVisibleHateTarget()
            if maxHateTargetId:
                targetSet = list(self.enemyCacheSet)
                if maxHateTargetId in targetSet:
                    targetSet.remove(maxHateTargetId)
                entityIds = targetSet
            else:
                entityIds = list(self.enemyCacheSet)

        else:
            _set = None
            _value = utils.getFightTargetTypeCfgData(targetString)
            if not _value:
                ERROR_MSG('getTargetIdsByTargetType: targetString={} not found'.format(targetString))
                return []

            for _tp in _value[2]:
                if _tp == gameconst.CampType.All:
                    _set = self.enemyCacheSet.union(self.notEnemyCacheSet, {self.id})

                elif _tp == gameconst.CampType.Enemy:
                    if _set is None:
                        _set = self.enemyCacheSet

                    else:
                        _set = _set.union(self.enemyCacheSet)

                elif _tp == gameconst.CampType.Friend:
                    if _set is None:
                        _set = self.friendCacheSet

                    else:
                        _set = _set.union(self.friendCacheSet)

                elif _tp == gameconst.CampType.Self:
                    if _set is None:
                        _set = {self.id}

                    else:
                        _set = _set.union({self.id})

                elif _tp == gameconst.CampType.EnemyExTarget:
                    if _set is None:
                        _set = self.enemyCacheSet

                    else:
                        _set = _set.union(self.enemyCacheSet)

            if _set is None:
                return []

            else:
                return list(_set)

        return entityIds

    def getTargets(self, centerEnt, targetId, targetString, targetRange=20, forceTarget=False, beginSkillPosition=None):
        targetsList = []
        entityIds = self.getTargetIdsByTargetType(targetString)

        target = KBEngine.entities.get(targetId)

        if forceTarget and target:
            entityIds.append(targetId)

        for eId in entityIds:
            entity = KBEngine.entities.get(eId)
            if not entity:
                continue

            if entity.isDestroyed:
                continue

            if not entity.IsCombatUnit:
                continue

            if entity.IsMonster:
                targetRange += entity.getConfigData().get('attackDistanceCompensation')

            if beginSkillPosition:
                if not sMath.inRectRange2D(targetRange, entity.position, beginSkillPosition):
                    continue
            else:
                if not sMath.inRectRange2D(targetRange, entity.position, self.position):
                    continue

            if not utils.checkCombatRangeY(self, entity):
                continue

            if utils.checkCachedTargetType(targetString, self, entity, target):
                targetsList.append(entity)

        return targetsList

    def isTarget(self, target, eId, targetString, targetRange, checkFun, beginSkillPosition=None):
        entity = KBEngine.entities.get(eId)
        if not entity or entity.isDestroyed or not entity.IsCombatUnit:
            return False

        if entity.IsMonster:
            targetRange += entity.getConfigData().get('attackDistanceCompensation')

        if beginSkillPosition:
            if not sMath.inRectRange2D(targetRange, entity.position, beginSkillPosition):
                return False
        else:
            if not sMath.inRectRange2D(targetRange, entity.position, self.position):
                return False

        if not utils.checkCombatRangeY(self, entity):
            return False

        if not utils.checkCachedTargetType(targetString, self, entity, target):
            return False

        return checkFun(entity)

    def getTargetsWithNum(self, centerEnt, targetId, targetString, targetRange, targetNum, checkScopeFun,
                          beginSkillPosition=None):
        targetIdsList = []
        entityIds = self.getTargetIdsByTargetType(targetString)
        target = KBEngine.entities.get(targetId)

        if targetNum > 1:
            if targetString == "Friend" or targetString == "FriendExGB":
                entityIds.remove(self.id)
                if self.isTarget(target, self.id, targetString, targetRange, checkScopeFun, beginSkillPosition):
                    targetIdsList.append(self.id)
                if targetId in entityIds:
                    entityIds.remove(targetId)
                    if self.isTarget(target, targetId, targetString, targetRange, checkScopeFun, beginSkillPosition):
                        targetIdsList.append(targetId)
            elif targetString == "Enemy" or targetString == "EnemyExTarget":
                if targetId in entityIds:
                    entityIds.remove(targetId)
                    if self.isTarget(target, targetId, targetString, targetRange, checkScopeFun, beginSkillPosition):
                        targetIdsList.append(targetId)

        if len(targetIdsList) >= targetNum:
            return targetIdsList

        random.shuffle(entityIds)
        for eId in entityIds:
            entity = KBEngine.entities.get(eId)
            if self.isTarget(entity, eId, targetString, targetRange, checkScopeFun, beginSkillPosition):
                targetIdsList.append(eId)
            if len(targetIdsList) >= targetNum:
                break

        return targetIdsList

    def iterGetTargets(self, targetString):
        entities = self.entitiesInRange(20)

        for entity in entities:
            if not entity.IsCombatUnit:
                continue

            if utils.checkTargetType(targetString, self, entity):
                yield entity

    def updateTimeEffect(self, effectCaller, effectId, effectIndex):
        effectVal = effectCaller.getEffectVal(self, effectId, effectIndex)
        if not effectVal:
            return

        effectVal.updateEffect(self, effectCaller)

    def addSummon(self, id, pos, direction, hostId, skillLv, bDieWithHost, ttl,
                  summonLv, buffId, buffLv, inheritPropRatio=1.0,
                  summonProps=None):
        props = {'summonId': id, 'spaceNo': self.spaceNo, 'hostId': self.id, 'dieWithHost': bDieWithHost, \
                 'force': self.force, 'spaceMgrId': self.spaceMgrId, 'ttl': ttl, 'level': summonLv,
                 'inheritPropRatio': inheritPropRatio}

        summonProps and props.update(summonProps)
        if self.IsAvatar:
            props.update({'hostTeamId': self.teamId})

        summon = KBEngine.createEntity('Summon', self.spaceID, pos, direction, props)
        if not summon:
            ERROR_MSG('addSummon Error', id, pos, hostId)
            return False

        if buffId and buffLv:
            summon.addBuff(buffId, buffLv, self.id)

        if skillLv:
            summon.setAllSkillLv(skillLv)

        self.petList.append(summon.id)

    def checkCanUseSkill(self, skillID):
        skill = self.getSkill(skillID)
        if skill is None:
            ERROR_MSG("checkCanUseSkill(%i):skillID=%i not found" % (self.id, skillID))
            return False

        skillState = skill.getSkillState()
        eventId = CSD.datas[skillState].get('event')
        if eventId and not self.checkConflictState(eventId):
            return

        if utils.hasSkillTag(skillID, gameconst.SkillTag.lzSpecialSkill):
            if not skill.checkCanUse():
                return

        return not skill.inCDTime()

    def resetStateOnline(self):
        stList = list(self.stateList)
        removedSt = []
        INFO_MSG('resetStateOnline', stList)
        for st in stList:
            if CSD.datas[st].get('clearOnline', 0) or CSD.datas[st].get('buffTag', 0):
                removedSt.append(st)
                self.removeState(st)

        for st in stList:
            if st not in removedSt:
                self.setState(st, isInit=True)

    def resetStateTeleport(self, oldSpaceNo):
        for i in self.stateList:
            if self.hasState(i):
                if i == gameconst.State.Moving and not self.isCleanMove(oldSpaceNo):
                    continue

                val = CSD.datas[i].get('clearTeleport', 0)
                if val == 1:
                    self.removeState(i)
                    INFO_MSG("resetStateTeleport", self.id, i)

    def addSkillEffectCd(self, skillID, cdDelta):
        skill = self.getSkill(skillID)
        if skill is None:
            ERROR_MSG("Spell::addSkillEffectCd(%i):skillID=%i not found" % (self.id, skillID))
            return False

        skill.changeCD(self, cdDelta)
        return True

    def addShield(self, buffId, shieldVal):
        if buffId in self.shieldDic:
            self.shieldDic[buffId].shieldValue += shieldVal
        else:
            self.shieldDic[buffId] = buff.ShieldVal(buffId, shieldVal)

    def removeShield(self, buffId):
        if buffId in self.shieldDic:
            self.shieldDic.pop(buffId)

    def absorbShieldWithDetails(self, nHpModify):
        remainHp = nHpModify
        rmShelds = []
        details = {}

        for buffId, shieldVal in self.shieldDic.items():
            if shieldVal.shieldValue > remainHp:
                shieldVal.doAbsorbDmg(remainHp)
                details[buffId] = remainHp
                remainHp = 0
                break
            else:
                absorbedVal = shieldVal.doAbsorbDmg(remainHp)
                remainHp -= absorbedVal
                rmShelds.append(buffId)
                details[buffId] = absorbedVal

        for buffId in rmShelds:
            self.removeBuff(buffId, isFinished=True, removeType=gameconst.RemoveType.EndByBeat)

        return remainHp, details

    def removeCreation(self, cid):
        if cid in self.creationList:
            self.creationList.remove(cid)

    def destoryAllCreation(self):
        for cid in list(self.creationList):
            creation = KBEngine.entities.get(cid)
            if creation:
                creation.safeDestroy()
            else:
                ERROR_MSG('destoryAllCreation: cannot find creation', cid)
        self.creationList.clear()

    def removeSummon(self, summonId):
        if summonId not in self.petList:
            return

        self.petList.remove(summonId)

        if not self.getTempMiscProp(gameconst.AvatarProps.spawnSummonByAI, False):
            return

        _aiData = self.getAIParam()
        if not _aiData:
            return

        _list = self.getTempMiscProp(gameconst.AvatarProps.spawnSummonList, [])
        _list.append({
            'ts': utils.getNow() + _aiData['summonCD'],
            'summonId': _aiData['summonID'],
        })

        self.setTempMiscProp(gameconst.AvatarProps.spawnSummonList, _list)

    def getSpawnSummonList(self):
        return self.getTempMiscProp(gameconst.AvatarProps.spawnSummonList, [])

    def setSpawnSummonList(self, spawnSummonList):
        self.setTempMiscProp(gameconst.AvatarProps.spawnSummonList, spawnSummonList)

    def enableSpawnSummonByAI(self):
        self.setTempMiscProp(gameconst.AvatarProps.spawnSummonByAI, True)

    def initAISpawnSummon(self):
        _aiData = self.getAIParam()
        if not _aiData:
            return

        _list = []
        for i in range(_aiData['summonLimit']):
            _list.append({
                'ts': utils.getNow() + _aiData['summonCD'] * i,
                'summonId': _aiData['summonID'],
            })

        self.setTempMiscProp(gameconst.AvatarProps.spawnSummonList, _list)

    def destroyAllSummon(self):
        for summonId in list(self.petList):
            summom = KBEngine.entities.get(summonId)
            if summom:
                summom.safeDestroy()
        self.petList.clear()

    def destroySummonOnDead(self):
        for summonId in list(self.petList):
            summom = KBEngine.entities.get(summonId)
            if summom and summom.dieWithHost:
                summom.delaySafeDestroy()
                self.petList.remove(summonId)

        for cloneId in list(self.cloneList):
            clone = KBEngine.entities.get(cloneId)
            if clone and clone.dieWithHost:
                clone.delaySafeDestroy()
                self.cloneList.remove(cloneId)

    def removeBuffOnDead(self):
        for buffId in list(self.buffDic.keys()):
            # 前面的buff的endAction可能把后面的buff删掉
            if buffId not in self.buffDic:
                continue
            for buffVal in self.buffDic[buffId].values():
                if buffVal.isRemoveOnDead():
                    self.removeBuff(buffId)
                    break

    @gamedecorator.crossServer
    def getBuffInfo(self, exposed, entityId):
        if not self._isMyself(exposed):
            return

        target = KBEngine.entities.get(entityId)
        if target and target.buffDic:
            self.client.onGetBuffInfo(entityId, target.buffDic.getClientData(target))

    # 客户端entity创建好后来服务器取一把光环信息，因为aureoleDic这个属性只有部分数据
    # 需要发给客户端，所以不能做成ALL_CLIENTS,只能在进入AOI时再发一次或者让客户端再取一次
    # 服务器的onEnterView接口里取self.clientEntity可能客户端实体还没创建好，所以暂时只能让客户端来拿
    @gamedecorator.crossServer
    def getAureoleInfo(self, exposed, entityId):
        if not self._isMyself(exposed):
            return

        target = KBEngine.entities.get(entityId)
        if target and target.aureoleDic:
            self.client.onGetAureoleInfo(entityId, target.aureoleDic.getClientData())

    def sendCombatMsg(self, msgId, args):
        pass

    def onCloneInitMoveover(self):
        pass

    def onCloneDestroy(self, cloneId):
        if cloneId in self.cloneList:
            self.cloneList.remove(cloneId)

    def getOwnedCreations(self, cid=0):
        ret = []
        for c in self.creationList:
            ent = KBEngine.entities.get(c)
            if ent and (not cid or ent.creationId == cid):
                ret.append(ent)
        return ret

    def getOwnedClones(self, cid=0):
        ret = []
        for c in self.cloneList:
            ent = KBEngine.entities.get(c)
            if ent and (not cid or ent.creepBaseId == cid):
                ret.append(ent)
        return ret

    def getOwnedSummons(self, sid=0):
        ret = []
        for s in self.petList:
            ent = KBEngine.entities.get(s)
            if ent and (not sid or ent.creepBaseId == sid):
                ret.append(ent)
        return ret

    def endChongfeng(self, skillVal, targetId, skillArgs):
        self.removeState(gameconst.State.Shifting)

    def endLunge(self, skillVal, targetId, skillArgs):
        self.removeState(gameconst.State.Shifting)

    def endDodge(self, skillVal, targetId, skillArgs):
        self.removeState(gameconst.State.Dodging)

    def endMovement(self):
        if self.getNeedUpdateWitnessPosDir() == 0:
            self.cancelController('Movement')

    def endUpdateWitnessPosDir(self):
        self.setNeedUpdateWitnessPosDir(1)

    def resetShiftOrDodgeTimer(self):
        shiftOrDodgeTimer = self.popTempMiscProp(gameconst.AvatarProps.shiftOrDodgeTimer, 0)

    def onMoveOver(self, controllerID, userData):
        if userData == gamemove.CHONGFENG_MOVE_OVER:
            self.onChongfengMoveOver(True)
        elif userData == gamemove.LUNGE_MOVE_OVER:
            self.onLungeMoveOver(True)
        elif userData == gamemove.DODGE_MOVE_OVER:
            self.onDodgeMoveOver(True)
        elif userData == gamemove.CLONE_INIT_MOVE_OVER:
            self.onCloneInitMoveover()

    def onMoveFailure(self, controllerID, userData):
        if userData == gamemove.CHONGFENG_MOVE_OVER:
            self.onChongfengMoveOver(False)
        elif userData == gamemove.LUNGE_MOVE_OVER:
            self.onLungeMoveOver(False)
        elif userData == gamemove.DODGE_MOVE_OVER:
            self.onDodgeMoveOver(False)
        elif userData == gamemove.CLONE_INIT_MOVE_OVER:
            self.onCloneInitMoveover()

    def onMoveBreak(self, controllerID, userData):
        if userData == gamemove.CHONGFENG_MOVE_OVER:
            self.onChongfengMoveOver(False)
        elif userData == gamemove.LUNGE_MOVE_OVER:
            self.onLungeMoveOver(False)
        elif userData == gamemove.DODGE_MOVE_OVER:
            self.onDodgeMoveOver(False)
        elif userData == gamemove.CLONE_INIT_MOVE_OVER:
            self.onCloneInitMoveover()
        elif not userData:
            self.removeState(gameconst.State.Moving)

    def onChongfengMoveOver(self, isSucc):
        self.setNeedUpdateWitnessPosDir(1)
        self.topSpeed = gameconst.TopSpeedType.NormalTopSpeed
        shiftOrDodgeTimer = self.popTempMiscProp(gameconst.AvatarProps.shiftOrDodgeTimer, 0)
        if shiftOrDodgeTimer > 0:
            self._cancelCallback(shiftOrDodgeTimer, gametimer.TIMER_TAG_SKILL_CHANGE_POS)
        chongfengData = self.popTempMiscProp(gameconst.AvatarProps.chongfengData)
        if not chongfengData:
            ERROR_MSG('chongfeng err: move failed', isSucc)
            self.endChongfeng(None, 0, [])
            return

        context, calcDelay = chongfengData

        skill = self._getSkillByActionContext(context)

        if not skill:
            ERROR_MSG('onChongfengMoveOver: cannot get skill', skill.skillId, context)
            self.endChongfeng(None, 0, [])
            return

        targetId = context.useTargetId
        self.endChongfeng(skill, targetId, context.skillArgs)
        if skill.checkUseSkill(self, targetId,
                               ignoreReasons=gameconst.UseSkillCheck.DELAY_CHECK_IGNORES) != gameconst.UseSkillCheck.CHEKC_OK:
            skill.useSkillDone(self, targetId, context.skillArgs, False)
            return

        if context.actionProgress == gameconst.ActionProgressType.startActionDoing:
            context.actionProgress = gameconst.ActionProgressType.startActionDone
            if isSucc:
                self.allClients.onUseSkill(True, skill.getNotifyClientSkillId(), targetId, context.skillArgs,
                                           context.effectedEntIds)
            self._doUseSkill(skill, targetId, context.skillArgs, context, calcDelay)
        elif context.actionProgress == gameconst.ActionProgressType.actionDoing and context.isLastActionStage:
            if skill.hasTempData('duration'):
                duration = skill.popTempData('duration')
            else:
                duration = 0
            remainTime = skill.getSkillTime(skill.skillId) - calcDelay - duration
            context.actionProgress = gameconst.ActionProgressType.actionDone
            if remainTime <= 0:
                skill.useSkillDone(self, targetId, context.skillArgs)
            else:
                skill._cancelTempTimer(self, 'skillDoneTimer', gametimer.TIMER_TAG_SKILL_DONE)
                tid = self._callback(remainTime, '_onSkillCallback',
                                     (skill, 'useSkillDone', (targetId, context.skillArgs, True, False, True)),
                                     gametimer.TIMER_TAG_SKILL_DONE)
                skill.setTempData('skillDoneTimer', tid)

    def onLungeMoveOver(self, isSucc):
        DEBUG_MSG("###onLungeMoveOver")
        self.setNeedUpdateWitnessPosDir(1)
        self.topSpeed = gameconst.TopSpeedType.NormalTopSpeed
        shiftOrDodgeTimer = self.popTempMiscProp(gameconst.AvatarProps.shiftOrDodgeTimer, 0)
        if shiftOrDodgeTimer > 0:
            self._cancelCallback(shiftOrDodgeTimer, gametimer.TIMER_TAG_SKILL_CHANGE_POS)
        lungeData = self.popTempMiscProp(gameconst.AvatarProps.lungeSkillData)
        if not lungeData:
            ERROR_MSG('lunge err: move failed', isSucc)
            self.endLunge(None, 0, [])
            return

        context, calcDelay = lungeData

        skill = self._getSkillByActionContext(context)

        if not skill:
            ERROR_MSG('onLungeMoveOver: cannot get skill', skill.skillId, context)
            self.endLunge(None, 0, [])
            return

        targetId = context.useTargetId
        self.endLunge(skill, targetId, context.skillArgs)
        if skill.checkUseSkill(self, targetId,
                               ignoreReasons=gameconst.UseSkillCheck.DELAY_CHECK_IGNORES) != gameconst.UseSkillCheck.CHEKC_OK:
            skill.useSkillDone(self, targetId, context.skillArgs, False)
            return

        if context.actionProgress == gameconst.ActionProgressType.startActionDoing:
            context.actionProgress = gameconst.ActionProgressType.startActionDone
            if isSucc:
                self.allClients.onUseSkill(True, skill.getNotifyClientSkillId(), targetId, context.skillArgs,
                                           context.effectedEntIds)
            self._doUseSkill(skill, targetId, context.skillArgs, context, calcDelay)
        elif context.actionProgress == gameconst.ActionProgressType.actionDoing and context.isLastActionStage:
            if skill.hasTempData('duration'):
                duration = skill.popTempData('duration')
            else:
                duration = 0
            remainTime = skill.getSkillTime(skill.skillId) - calcDelay - duration
            context.actionProgress = gameconst.ActionProgressType.actionDone
            if remainTime <= 0:
                skill.useSkillDone(self, targetId, context.skillArgs)
            else:
                tid = self._callback(remainTime, '_onSkillCallback',
                                     (skill, 'useSkillDone', (targetId, context.skillArgs, True, False, True)),
                                     gametimer.TIMER_TAG_SKILL_DONE)
                skill.setTempData('skillDoneTimer', tid)

    def onDodgeMoveOver(self, isSucc):
        self.setNeedUpdateWitnessPosDir(1)
        self.topSpeed = gameconst.TopSpeedType.NormalTopSpeed
        shiftOrDodgeTimer = self.popTempMiscProp(gameconst.AvatarProps.shiftOrDodgeTimer, 0)
        if shiftOrDodgeTimer > 0:
            self._cancelCallback(shiftOrDodgeTimer, gametimer.TIMER_TAG_SKILL_CHANGE_POS)
        dodgeData = self.popTempMiscProp(gameconst.AvatarProps.dodgeSkillData)
        if not dodgeData:
            ERROR_MSG('dodge err: move failed', isSucc)
            self.endDodge(None, 0, [])
            return

        context, calcDelay = dodgeData

        skill = self._getSkillByActionContext(context)

        if not skill:
            ERROR_MSG('onDodgeMoveOver: cannot get skill', skill.skillId, context)
            self.endDodge(None, 0, [])
            return

        targetId = context.useTargetId
        self.endDodge(skill, 0, context.skillArgs)
        if skill.checkUseSkill(self, targetId,
                               ignoreReasons=gameconst.UseSkillCheck.DELAY_CHECK_IGNORES) != gameconst.UseSkillCheck.CHEKC_OK:
            skill.useSkillDone(self, targetId, context.skillArgs, False)
            return

        if context.actionProgress == gameconst.ActionProgressType.startActionDoing:
            context.actionProgress = gameconst.ActionProgressType.startActionDone
            if isSucc:
                self.allClients.onUseSkill(True, skill.getNotifyClientSkillId(), targetId, context.skillArgs,
                                           context.effectedEntIds)
            self._doUseSkill(skill, targetId, context.skillArgs, context, calcDelay)
        elif context.actionProgress == gameconst.ActionProgressType.actionDoing and context.isLastActionStage:
            if skill.hasTempData('duration'):
                duration = skill.popTempData('duration')
            else:
                duration = 0
            remainTime = skill.getSkillTime(skill.skillId) - calcDelay - duration
            context.actionProgress = gameconst.ActionProgressType.actionDone
            if remainTime <= 0:
                skill.useSkillDone(self, targetId, context.skillArgs)
            else:
                tid = self._callback(remainTime, '_onSkillCallback',
                                     (skill, 'useSkillDone', (targetId, context.skillArgs, True, False, True)),
                                     gametimer.TIMER_TAG_SKILL_DONE)
                skill.setTempData('skillDoneTimer', tid)

    def onKillTarget(self, spaceNo, targetId, targetUID, belongOwnerGbId=0, belongTeamId=0):
        pass
        # hostKiller, isKillerBot = utils.getRealAvatarEnt(self)
        # # if hostKiller and hostKiller.IsAvatarMirror and hostKiller.teamRobotHostId > 0 and hostKiller.teamId > 0:
        # #     teamRobotHost = KBEngine.entities.get(hostKiller.teamRobotHostId)
        # #     if teamRobotHost:
        # #         teamRobotHost.checkKillMonsterTrigger(targetId, targetUID)
        # #     else:
        # #         gameengine.getTeamStub(hostKiller.teamId).teamRobotKillMonster(hostKiller.teamId, spaceNo, targetId,
        # #                                                                        targetUID,
        # #                                                                        hostKiller.gbId)
        # #     return
        #
        # if isKillerBot:
        #     WARNING_MSG('in onKillTarget, killer is killerbot')
        #     return
        # if hostKiller and hostKiller.IsAvatar:
        #     if not belongTeamId and not belongOwnerGbId:
        #         # 没有归属信息，默认归属hostkiller
        #         hostKiller.checkKillMonsterTrigger(targetId, targetUID)
        #     else:
        #     #     # 归属于某个队伍和归属指定玩家可以同时存在（尚羽之争帮主镜像）
        #     #     # 归属于队伍
        #     #     if belongTeamId:
        #     #         gameengine.getTeamStub(belongTeamId).killMonster(belongTeamId, spaceNo, targetId, targetUID,
        #     #                                                          hostKiller.gbId)
        #     #     # 归属于指定玩家
        #         if belongOwnerGbId:
        #             if belongOwnerGbId != hostKiller.gbId:
        #                 # belongTeamId 需要设置为0，否则会再次进入 gameengine.getTeamStub(belongTeamId).killMonster 逻辑
        #                 belongTeamId = 0
        #                 gameengine.getGlobalBase('PlayerStub').doOnOthersCell([belongOwnerGbId], 'onKillTarget', (
        #                     spaceNo, targetId, targetUID, belongOwnerGbId, belongTeamId), None, '', ())
        #             else:
        #                 hostKiller.checkKillMonsterTrigger(targetId, targetUID)
            # hostKiller.monsterDeadAddFriendDegree()

    def onEnterTrap(self, entity, rangeXZ, rangeY, controllerId, userArg):
        if hasattr(super(), 'onEnterTrap'):
            super().onEnterTrap(entity, rangeXZ, rangeY, controllerId, userArg)
        if not entity or entity.isDestroyed:
            return

        if userArg == gameconst.AUREOLE_TRAP:
            if not entity.IsCombatUnit:
                return

            self.aureoleDic.addCtrlInPending(controllerId)

            _aureole = self.aureoleDic.getByCtrlId(controllerId)
            _entityId = entity.id

            if not _aureole:
                return

            if not utils.checkTargetType(_aureole.effectTarget, self, entity):
                return

            _aureole.addAureoleTarget(self, _entityId)

    def onLeaveTrap(self, entity, rangeXZ, rangeY, controllerId, userArg):
        if hasattr(super(), 'onLeaveTrap'):
            super().onLeaveTrap(entity, rangeXZ, rangeY, controllerId, userArg)
        if not entity:
            return

        if userArg == gameconst.AUREOLE_TRAP:
            _aureole = self.aureoleDic.getByCtrlId(controllerId)
            _entityId = entity.id

            if not _aureole:
                return

            _aureole.onLeaveAureoleRnage(self, _entityId)

    def onEnterWholeAureole(self, entity):
        if not entity:
            return

        if not entity.IsCombatUnit:
            return

        for aureoleId in self.aureoleDic._wholeAreaAureoleList:
            _aureole = self.aureoleDic.get(aureoleId)
            _entityId = entity.id
            if _aureole and utils.checkTargetType(_aureole.effectTarget, self, entity):
                _aureole.addAureoleTarget(self, _entityId)

    def onLeaveWholeAureole(self, entity):
        if not entity:
            return

        for aureoleId in self.aureoleDic._wholeAreaAureoleList:
            _aureole = self.aureoleDic.get(aureoleId)
            _entityId = entity.id
            if _aureole and utils.checkTargetType(_aureole.effectTarget, self, entity):
                _aureole.onLeaveAureoleRnage(self, _entityId)

    def setCombatControlState(self, controlState, antiDuration, controlLv=1):
        if controlState not in self.controlledStates:
            csVal = combatSkill.ControlState(controlLv, time.time())
            csVal.refreshAntiTimer(self, controlState, antiDuration)
            self.controlledStates[controlState] = csVal
        else:
            csVal = self.controlledStates[controlState]
            csVal.refreshAntiTimer(self, controlState, antiDuration)

        return csVal

    def getControllLv(self, controlState):
        if controlState not in self.controlledStates:
            return 0

        return self.controlledStates[controlState].controlLv

    def removeCombatControlState(self, controlState):
        self.controlledStates.pop(controlState)

    def calcAntiControl(self, target, context, antiRes):
        if target.isDie() or target.isDestroyed:
            return
        # 如果概率没命中，就不干虾米了
        if antiRes.resultCode == antiRes.RES_NOT_HIT:
            return

        buffLv = 1
        controlStateId = antiRes.controlState
        stateName = self._getConflictStatusName(controlStateId)
        buffName = buff.Buff.getBuffName(antiRes.controlBuffId)
        hitType = self._getConflictPopupIndex(controlStateId)

        skillDamges = context.getCombatResult()
        if not skillDamges:
            ERROR_MSG('unexpected anti control context', context)
            skillDamges = combatSkill.SkillDamges(self.id, context.getDmgSourceType(), context.getDmgSourceId())

        # 免疫控制状态 or 控制状态被抵抗
        if (antiRes.resultCode == antiRes.RES_IMMUNE and not target.IsMonster) or antiRes.resultCode == antiRes.RES_ANTI:
            if hitType == gameconst.HitType.Silence:
                skillDamges.damageInfo.append(combatSkill.SkillDamageVal(target.id, 0, gameconst.HitType.AntiSilence))
            else:
                skillDamges.damageInfo.append(combatSkill.SkillDamageVal(target.id, 0, gameconst.HitType.AntiControl))

        # 命中，如果衰减的话要增加控制等级，刷新衰减时间
        elif antiRes.resultCode == antiRes.RES_HIT:

            csVal = self.setCombatControlState(controlStateId, antiRes.antiDuration)
            if antiRes.isDecay:
                csVal.addControlLv(math.ceil(antiRes.controlDuration))
                csVal.refreshAntiTimer(self, controlStateId, antiRes.antiDuration)

            self.addBuffBySkill(target, context, antiRes.controlBuffId, buffLv, 1.0, antiRes.controlDuration)
            antiRes.dispelBuffTag and self.dispelBuffByTag(target, context, antiRes.dispelBuffTag)

            if hitType == 0:
                ERROR_MSG('unexpected anti control hitType', hitType)
                return
            skillDamges.damageInfo.append(combatSkill.SkillDamageVal(target.id, 0, hitType))

    def dispelBuffByTag(self, target, context, tag):
        buffIdList = []
        for buffId in target.buffDic.keys():
            buff = target.getBuffByBuffId(buffId)
            if buff and buff.hasTag(tag):
                buffIdList.append(buffId)

        for buffId in buffIdList:
            target.removeBuff(buffId)

    def isImmuneToControl(self):
        return self.baseStateRate == -1

    def getArbitrarySkill(self):
        return next(iter(self.getSkillDic().values()), None)

    def changeWeather(self, weatherType, duration):
        DEBUG_MSG('skill change weather:', weatherType, duration)
        if duration <= 0:
            strongerTime = -1
        else:
            strongerTime = utils.getNow() + duration

        weatherVal = weather.WeatherBase.getWeatherVal(weatherType, self.id, strongerTime)

        spaceMgr = self.spaceMgr
        if not spaceMgr:
            DEBUG_MSG('changeWeather: spaceMgr not found')
            return

        spaceMgr.changeWeather(weatherVal)

    def resetWeather(self):
        DEBUG_MSG('skill reset:')
        spaceMgr = self.spaceMgr
        if not spaceMgr:
            DEBUG_MSG('changeWeather: spaceMgr not found')
            return

        spaceMgr.resetWeather()

    def getCurWeather(self):
        spaceMgr = self.spaceMgr
        if not spaceMgr:
            DEBUG_MSG('getCurWeather: spaceMgr not in home or dun:', self.spaceNo)
            return 0, 1

        wVal = spaceMgr.spaceWeather
        return wVal.WEATHER_TYPE, wVal.level

    def setTargetHateRecord(self, targetId):
        target = KBEngine.entities.get(targetId)
        target and target.setHateRecord(self.id)

    def unsetTargetHateRecord(self, targetId):
        target = KBEngine.entities.get(targetId)
        target and target.unsetHateRecord(self.id)

    def clearHateRecord(self, removeFightingState=True):
        hateRecord = self.getTempMiscProp(gameconst.AvatarProps.hateRecord)
        if hateRecord:
            self.popTempMiscProp(gameconst.AvatarProps.hateRecord)
        # if removeFightingState and self.IsAvatar and not self.isDie():
        #     self.removeState(gameconst.State.Fighting)

    def setHateRecord(self, targetId):
        if not self.hasTempMiscProp(gameconst.AvatarProps.hateRecord):
            self.setTempMiscProp(gameconst.AvatarProps.hateRecord, {})
        hateRecord = self.getTempMiscProp(gameconst.AvatarProps.hateRecord)
        hateRecord[targetId] = int(time.time())
        # self.IsAvatar and not self.isDie() and self.setState(gameconst.State.Fighting)

    def unsetHateRecord(self, targetId):
        hateRecord = self.getTempMiscProp(gameconst.AvatarProps.hateRecord)
        if not hateRecord:
            return
        if targetId in hateRecord:
            hateRecord.pop(targetId)

        if not hateRecord:
            self.clearHateRecord()

    def unsetAllHateRecord(self, unsetReason):
        hateRecord = self.getTempMiscProp(gameconst.AvatarProps.hateRecord)
        if not hateRecord:
            return
        for targetId in list(hateRecord.keys()):
            target = KBEngine.entities.get(targetId)
            target and target.IsAvatar and target.unsetHateRecord(self.id)
            if unsetReason in (gameconst.UnsetAllHateReason.dead, gameconst.UnsetAllHateReason.leaveFightingState,
                               gameconst.UnsetAllHateReason.destory):
                pass
                # target and target.removeHate(self.id)
        self.clearHateRecord()

    def removeFightingState(self):
        # if not self.checkRemoveFightingState():
        #     return
        self.rmFightStateTimeId = 0
        self.removeState(gameconst.State.Fighting)

    def checkRemoveFightingState(self):
        hateRecord = self.getTempMiscProp(gameconst.AvatarProps.hateRecord)
        if not hateRecord:
            return True
        removeTime = CONST.datas.get('leaveFightStateTime', {}).get('value')
        for targetId in list(hateRecord.keys()):
            target = KBEngine.entities.get(targetId)
            if target and target.IsAvatar and hateRecord[targetId] + removeTime < int(time.time()):
                hateRecord.pop(targetId, None)
                target.unsetHateRecord(self.id)
        if not hateRecord:
            self.clearHateRecord(removeFightingState=False)
            return True
        return False

    def isVisible(self, target):
        if target.hasBuffTag(gameconst.BuffTag.DisableSelfHiddenTag):
            return True

        if not utils.checkCombatRangeY(self, target):
            return False
        # return not target.hasState(gameconst.State.Invisible)
        return True

    def _onRemoveInvisible(self, byConfilictState):
        self._trapInViews()

    # 为了让日志更可读以及减少字符拼接开销，必须以 'skillId:%s', skillId 这种形式传入
    def combatDebugMsg(self, *args):
        if gameconfig.enableCombatDebugLog():
            if len(args) <= 1:
                msg = args[0]
            else:
                msg = args[0] % args[1:]
            msg = '[%s][combatDebug] ' % getattr(self, 'name', '') + msg
            INFO_MSG(msg)

    def reliveToPos(self, pos, toDir, hp, context):
        """在指定位置复活

        Arguments:
            pos {position or None} -- 复活位置, 如果为None则在原地位置复活
            hp {int} -- 复活血量, 如果 =0则默认复活, 如果<0则满血复活, 其他情况按血量设置复活
        """
        self._relive()
        self.addBuff(GP_SD.datas["resurrectProtectBuffID"]["value"], 1, self.id)
        newHp = hp
        if hp == 0:
            newHp = self.getDefaultReliveHp()
        elif hp < 0 or hp > self.fullHp:
            newHp = self.fullHp
        self.modifyHP(newHp, self.id, gameconst.SourceType.Default, self.id)
        if pos:
            self.telToPos(pos, toDir)
        self._trapInViews()

        if context is not None:
            srcEntId = None
            if hasattr(context, 'casterEntId'):
                srcEntId = context.casterEntId
            elif hasattr(context, 'srcEntId'):
                srcEntId = context.srcEntId
            if srcEntId:
                self.client.onReliveByOthers(srcEntId)

        if self.IsAvatar:
            spaceMgr = self.spaceMgr
            spaceMgr and spaceMgr.onPlayerRelive(self.base, self.gbId)
            self.setState(CCDD.datas.relive)
            self._callback(CONST.datas['reliveTime']['value'], 'removeState', (CCDD.datas.relive,), gametimer.TIMER_TAG_REMOVE_RELIVE_STATE)

        self.popTempMiscProp(gameconst.AvatarProps.isLightningArea)

    def getDefaultReliveHp(self):
        return max(min(round(1 * 0.01 * self.fullHp), self.fullHp), 1)

    def sendSkillDamage(self, skillDamges):
        broadcastIdList = []

        for sVal in skillDamges.damageInfo:
            target = KBEngine.entities.get(sVal.targetId)
            if target:
                target = utils.getEntityRealEntity(target)
                if target and target.IsAvatar and target.id not in broadcastIdList:
                    broadcastIdList.append(target.id)
                    target.client.onSkillDamage(skillDamges)

        src = KBEngine.entities.get(skillDamges.casterId)
        if src:
            src = utils.getEntityRealEntity(src)
            src and src.IsAvatar and src.id not in broadcastIdList and src.client.onSkillDamage(skillDamges)

        if skillDamges.sourceType == gameconst.SourceType.Skill:
            targetIdList = [sVal.targetId for sVal in skillDamges.damageInfo if
                            not gameconst.HitType.isInClientIgnoreList(sVal.hitType)]
            if len(targetIdList) > 0:
                avatarList = [e for e in self.getWitnesses() if e.id not in broadcastIdList]
                num = min(20, len(avatarList))
                sourceId = skillDamges.sourceId
                for avatar in random.sample(avatarList, num):
                    avatar.client.onOthersSkillDamage(sourceId, targetIdList)

    def pySetWitnessType(self, eId, witnessType):
        self.setWitnessType(eId, witnessType)

    def allClientsOnUpdateBuff(self, buffId, buffClientData):
        ifSend = buff.Buff.getIfSend(buffId)
        if ifSend:
            self.allClients.onUpdateBuff(buffClientData)
        else:
            if self.IsMonster and self.isBoss:
                self.allClients.onUpdateBuff(buffClientData)
            else:
                self.IsAvatar and self.client.onUpdateBuff(buffClientData)
                for e in self.getWitnessesWithName():
                    if e and e.IsAvatar and e.selectedTargetId == self.id:
                        clientEnt = e.clientEntity(self.id)
                        clientEnt and clientEnt.onUpdateBuff(buffClientData)

    def allClientsOnAddBuff(self, buffId, buffClientData):
        ifSend = buff.Buff.getIfSend(buffId)
        if ifSend:
            self.allClients.onAddBuff(buffClientData)
        else:
            if self.IsMonster and self.isBoss:
                self.allClients.onAddBuff(buffClientData)
            else:
                self.IsAvatar and self.client.onAddBuff(buffClientData)
                for e in self.getWitnessesWithName():
                    if e and e.IsAvatar and e.selectedTargetId == self.id:
                        clientEnt = e.clientEntity(self.id)
                        clientEnt and clientEnt.onAddBuff(buffClientData)

    def allClientsOnRemoveBuff(self, buffId, removedKeys):
        ifSend = buff.Buff.getIfSend(buffId)
        if ifSend:
            self.allClients.onRemoveBuff(buffId, removedKeys)
        else:
            if self.IsMonster and self.isBoss:
                self.allClients.onRemoveBuff(buffId, removedKeys)
            else:
                self.IsAvatar and self.client.onRemoveBuff(buffId, removedKeys)
                for e in self.getWitnessesWithName():
                    if e and e.IsAvatar and e.selectedTargetId == self.id:
                        clientEnt = e.clientEntity(self.id)
                        clientEnt and clientEnt.onRemoveBuff(buffId, removedKeys)

    def printDebugMap(self, fromPos, toPos, markPosList=(), layer=1):
        fromPos = (int(fromPos[0]), int(fromPos[2]))
        toPos = (int(toPos[0]), int(toPos[2]))
        s = (min(fromPos[0], toPos[0]), min(fromPos[1], toPos[1]))
        t = (max(fromPos[0], toPos[0]), max(fromPos[1], toPos[1]))

        print('spaceNo:%s from: %s to %s' % (self.spaceNo, fromPos, toPos))
        print('range: %s  %s' % (s, t))

        monsterPos = []
        avatarPos = []
        for e in self.entitiesInRange(80):
            if not e.IsCombatUnit:
                continue

            if e.IsAvatar:
                avatarPos.append(sMath.postion3DTo2DCell(e.position))
            else:
                monsterPos.append(sMath.postion3DTo2DCell(e.position))

        result = ''
        for i in range(t[1] + 1, s[1] - 2, -1):
            line = ''
            for j in range(s[0] - 2, t[0] + 2):
                if (j, i) == fromPos:
                    line += 'F'
                elif (j, i) == toPos:
                    line += 'T'
                elif (j, i) == s:
                    line += '*'
                elif (j, i) == t:
                    line += '-'
                elif (j, i) in markPosList:
                    line += '#'
                elif (j, i) in avatarPos:
                    line += 'a'
                elif (j, i) == sMath.postion3DTo2DCell(self.position):
                    line += 'M'
                elif (j, i) in monsterPos:
                    line += 'm'
                else:
                    line += str(KBEngine.getMapTileNavCost(self.spaceID, j, i, layer))
                line += ' '
            result += line + '\n'
            DEBUG_MSG(line)

        # print(result)

    def resetTargetTypeCache(self, entities):
        for target in entities:
            self.removeTargetTypeCache(target)
            utils.isEnemy(self, target)
            utils.isFriend(self, target)

            if target.id in list(self.cacheSelfSet):
                target.removeTargetTypeCache(self)
                utils.isEnemy(target, self)
                utils.isFriend(target, self)

        self.checkRemoveBuffOnTargetTypeChanged()
        self.allChildrenResetTargetTypeCache(entities)

    def resetAllTargetTypeCache(self):
        if self.IsAvatar:
            self.guildRelationVersion = gameglobal.guildRelationVersion

        cacheIds = self.enemyCacheSet.union(self.notEnemyCacheSet, self.friendCacheSet, self.notFriendCacheSet)
        self.enemyCacheSet.clear()
        self.notEnemyCacheSet.clear()
        self.friendCacheSet.clear()
        self.notFriendCacheSet.clear()

        for eId in cacheIds:
            target = KBEngine.entities.get(eId)
            if not target:
                ERROR_MSG("resetAllTargetTypeCache target is None")
                continue

            utils.isEnemy(self, target)
            utils.isFriend(self, target)

        for eId in list(self.cacheSelfSet):
            target = KBEngine.entities.get(eId)
            if not target:
                ERROR_MSG("resetAllTargetTypeCache cacheSelfSet target is None", eId)
                continue

            target.removeTargetTypeCache(self)
            utils.isEnemy(target, self)
            utils.isFriend(target, self)

        self.checkRemoveBuffOnTargetTypeChanged()
        self.allChildrenResetAllTargetTypeCache()

    def checkCacheTargetType(self):
        allCacheSetLen = len(self.enemyCacheSet) + len(self.notEnemyCacheSet)
        if allCacheSetLen > 30:
            return
        needRefreshList = []
        for eId in list(self.enemyCacheSet):
            target = KBEngine.entities.get(eId)
            if not target:
                ERROR_MSG("checkCacheTargetType  error1", eId)
                self.enemyCacheSet.remove(eId)
            elif not utils._isEnemy(self, target):
                ERROR_MSG("checkCacheTargetType enemy cache error", eId)
                needRefreshList.append(target)

        for eId in list(self.notEnemyCacheSet):
            target = KBEngine.entities.get(eId)
            if not target:
                ERROR_MSG("checkCacheTargetType  error2", eId)
                self.notEnemyCacheSet.remove(eId)
            elif utils._isEnemy(self, target):
                ERROR_MSG("checkCacheTargetType not enemy cache error", eId)
                needRefreshList.append(target)

        for eId in list(self.friendCacheSet):
            target = KBEngine.entities.get(eId)
            if not target:
                ERROR_MSG("checkCacheTargetType  error3", eId)
                self.friendCacheSet.remove(eId)
            elif not utils._isFriend(self, target):
                ERROR_MSG("checkCacheTargetType friend cache error", eId)
                needRefreshList.append(target)

        for eId in list(self.notFriendCacheSet):
            target = KBEngine.entities.get(eId)
            if not target:
                ERROR_MSG("checkCacheTargetType  error4", eId)
                self.notFriendCacheSet.remove(eId)
            elif utils._isFriend(self, target):
                ERROR_MSG("checkCacheTargetType not friend cache error", eId)
                needRefreshList.append(target)

        if len(needRefreshList) > 0:
            self.resetTargetTypeCache(needRefreshList)

    def resetTargetTypeCacheFlag(self):
        self.stopCacheTargetTypeTimeId = 0
        self.useTargetTypeCacheFlag = False
        self.clearAllTargetTypeCache()

    def clearAllTargetTypeCache(self, bClearOthersCache=False):
        allCacheSet = self.enemyCacheSet.union(self.notEnemyCacheSet, self.friendCacheSet, self.notFriendCacheSet)
        self.enemyCacheSet.clear()
        self.notEnemyCacheSet.clear()
        self.friendCacheSet.clear()
        self.notFriendCacheSet.clear()
        for eId in allCacheSet:
            target = KBEngine.entities.get(eId)
            if not target:
                ERROR_MSG("clearAllTargetTypeCache target is None in allCacheSet", eId)
                continue
            target.cacheSelfSet.remove(self.id)

        if bClearOthersCache:
            for eId in list(self.cacheSelfSet):
                target = KBEngine.entities.get(eId)
                if not target:
                    ERROR_MSG("clearAllTargetTypeCache target is None in cacheSelfSet", eId)
                    self.cacheSelfSet.remove(eId)
                    continue
                target.removeTargetTypeCache(self)

    def removeTargetTypeCache(self, target):
        self.enemyCacheSet.discard(target.id)
        self.notEnemyCacheSet.discard(target.id)
        self.friendCacheSet.discard(target.id)
        self.notFriendCacheSet.discard(target.id)
        target.cacheSelfSet.discard(self.id)

    def allChildrenResetAllTargetTypeCache(self):
        for summonId in self.petList:
            summom = KBEngine.entities.get(summonId)
            summom and summom.resetAllTargetTypeCache()

        for cid in self.cloneList:
            c = KBEngine.entities.get(cid)
            c and c.resetAllTargetTypeCache()

        for cid in self.creationList:
            creation = KBEngine.entities.get(cid)
            creation and creation.resetAllTargetTypeCache()

    def allChildrenResetTargetTypeCache(self, entities):
        for summonId in self.petList:
            summom = KBEngine.entities.get(summonId)
            summom and summom.resetTargetTypeCache(entities)

        for cid in self.cloneList:
            c = KBEngine.entities.get(cid)
            c and c.resetTargetTypeCache(entities)

        for cid in self.creationList:
            creation = KBEngine.entities.get(cid)
            creation and creation.resetTargetTypeCache(entities)

    def getSkillDic(self):
        return self.skillDic

    def tagDispel(self, tag):
        buffIdList = []
        for buffId in self.buffDic.keys():
            buffMap = self.buffDic.get(buffId)
            if not buffMap:
                continue
            for buffSrcKey in buffMap.keys():
                buff = buffMap.get(buffSrcKey)
                if buff and buff.hasTag(tag):
                    buffIdList.append(buffId)
                break
        if len(buffIdList) >= 1:
            ranBuffId = random.sample(buffIdList, 1)
            self.removeBuff(ranBuffId[0])

    def tagDispelAll(self, tag):
        self.removeBuffByTag(tag)

    def hasPropTransformState(self):
        return False

    def onTimer(self, tid, userData):
        self._onTimer(tid, userData)
        if userData == gametimer.AUREOLE_LOOP:
            self.aureoleDic._onLoop(self, tid)
        if userData == gametimer.FIGHTING_STATE_TICK:
            self.removeFightingState()
        if userData == gametimer.CHECK_TARGET_TYPE_TIMER:
            self.checkCacheTargetType()
        else:
            super(SkillManager, self).onTimer(tid, userData)

    def deathCreateCollection(self, radius, numProb, collectionIdProb, disappearTime):
        numList = []
        numWeightList = []
        for weight, num in numProb:
            numList.append(num)
            numWeightList.append(weight)

        createNum = utils.weightChoice(numList, numWeightList)[0][0]
        for i in range(createNum):
            collectionIdList = []
            collectionIdWeightList = []
            for weight, collectionId in collectionIdProb:
                collectionIdList.append(collectionId)
                collectionIdWeightList.append(weight)

            collectionId = utils.weightChoice(collectionIdList, collectionIdWeightList)[0][0]
            pos_ = self.getRandomPosition(self.position, radius) or self.position

            props = {
                'collectionId': collectionId,
                'spaceNo': self.spaceNo,
                'position': pos_,
                'direction': self.direction,
                'disappearTime': utils.getNow() + disappearTime
            }
            if self.spaceMgr:
                props['spaceMgrId'] = self.spaceMgr.id
                props['spaceMgrBox'] = self.spaceMgr.base

            KBEngine.createEntity('Collection', self.spaceID, pos_, self.direction, props)

    def setShooterSkillCanUse(self, skillId, canUseAllTime):
        DEBUG_MSG("setShooterSkillCanUse", skillId, canUseAllTime)
        if not self.hasSkill(skillId):
            return

        if not utils.hasSkillTag(skillId, gameconst.SkillTag.lzSpecialSkill):
            return

        skillVal = self.getSkill(skillId)
        skillVal and skillVal.enterCanUseState(self, canUseAllTime)

    def breakSkillByState(self):
        for skillId in list(self.getSkillDic()):
            skillVal = self.getSkill(skillId)
            if not skillVal:
                continue

            if skillVal.isInSkill:
                skillVal.useSkillDone(self, 0, [], isSucc=False, doRemoveState=True)

            _child = skillVal.childSkill()
            if _child and _child.isInSkill:
                _child.useSkillDone(self, 0, [], isSucc=False, doRemoveState=True)

    def getAvatar(self):
        if self.IsAvatar:
            return self
        if self.IsCreation or self.IsSummon:
            entity = self.getHost()
            if entity.IsAvatar:
                return entity
        return None
