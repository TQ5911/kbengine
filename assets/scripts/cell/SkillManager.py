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
import NPC_Pick as NPD


class AureoleMixin(object):
    def addTAureoleTrap(self, aureoleId):
        _aureole = self.aureoleDic.get(aureoleId)

        if not _aureole:
            return

        _aureole.addAureoleTrap(self)

    def isWholeAreaAureole(self, aureoleId):
        return self.spaceMgr and AAD.datas[aureoleId].get('radium') == -1

    def removeAureola(self, aureoleId):
        self.aureoleDic.removeAureola(self, aureoleId)

    def clearAureole(self):
        for _aureoleId in list(self.aureoleDic.keys()):
            self.removeAureola(_aureoleId)

    def disableAureole(self, aureoleId=0):
        if aureoleId == 0:
            for aureoleId in list(self.aureoleDic.keys()):
                self.aureoleDic.disableAureole(self, aureoleId)
        else:
            self.aureoleDic.disableAureole(self, aureoleId)

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
                LOG_ERR('addAureoleEffect faileed', srcEntId, aureoleId)
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
            self.onEnterTrap(self, 0, 0, aVal.aureoleTrapId, gameconst.AURA_TRAP)

    def hasAureola(self, aureolaId):
        return aureolaId in self.aureoleDic

    def isValidAureoleTarget(self, aureolaId, target):
        if not self.hasAureola(aureolaId):
            return False

        _aureole = self.aureoleDic[aureolaId]
        if not utils.checkTargetTypeValid(_aureole.effectTarget, self, target):
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
        return self.getTempMiscProp(gameconst.EntityPropsEnum.statisticsDmgRecordTimerId, 0)

    @statisticsDmgRecordTimerId.setter
    def statisticsDmgRecordTimerId(self, newTimerId):
        self.setTempMiscProp(gameconst.EntityPropsEnum.statisticsDmgRecordTimerId, newTimerId)

    @statisticsDmgRecordTimerId.deleter
    def statisticsDmgRecordTimerId(self):
        self.popTempMiscProp(gameconst.EntityPropsEnum.statisticsDmgRecordTimerId)

    @property
    def maxRecordsTimeout(self):
        return 30

    @property
    def maxRecordsCount(self):
        return 100

    def stopStatisticsRecorded(self):
        LOG_DBG("stopStatisticsRecorded::", self.statisticsDmgRecordTimerId)
        if self.statisticsDmgRecordTimerId:
            self._stopStatisticsRecorded()

    def _stopStatisticsRecorded(self):
        self.cancelTimerCB(self.statisticsDmgRecordTimerId, gametimer.TIMER_TAG_IN_REFRESH_STATISTICS_RECORDS)
        del self.statisticsDmgRecordTimerId

    def startStatisticsRecorded(self):
        LOG_DBG("startStatisticsRecorded::")
        self._refreshStatisticsRecordsRegr()

    def _refreshStatisticsRecordsRegr(self):
        if self.statisticsDmgRecordTimerId:
            self._stopStatisticsRecorded()
        m_tid = self.addTimerCB(1, '_inRefreshStatisticsRecords', (),
                               gametimer.TIMER_TAG_IN_REFRESH_STATISTICS_RECORDS, 'statisticsDmgRecordTimerId')
        self.statisticsDmgRecordTimerId = m_tid

    def _inRefreshStatisticsRecords(self):
        self.refreshStatisticsRecords()
        self._refreshStatisticsRecordsRegr()

    def refreshStatisticsRecords(self):
        now = utils.curTS()
        lastTime = now - self.maxRecordsTimeout
        while True:
            if not self.statisticsDmgRecords:
                break

            d = self.statisticsDmgRecords[0]
            if d[-1] > lastTime:
                break
            else:
                self.statisticsDmgRecords.popleft()


class StandStillBuffTriggerLoopMixin(object):

    @property
    def standStillBuffTriggerCacheDic(self) -> dict:
        """Type: Dict[buffId, Dict[buffId, maxOverlayLevel, upPreOverlaySec, downPreOverlaySec,
                      lastOverlayT, lastOverlayActionType, timerId, uuid]]"""
        if not self.hasTempMiscProp(gameconst.EntityPropsEnum.standStillBuffTriggerCacheDic):
            self.setTempMiscProp(gameconst.EntityPropsEnum.standStillBuffTriggerCacheDic, dict())
        return self.getTempMiscProp(gameconst.EntityPropsEnum.standStillBuffTriggerCacheDic)

    def regrStandStillBuffTriggerCache(self, buffId, maxOverlayLevel, upPreOverlaySec, downPreOverlaySec,
                                       skipTick=True):
        LOG_IFO("regrStandStillBuffTriggerCache::", buffId, maxOverlayLevel, upPreOverlaySec, downPreOverlaySec)
        standStillBuffTriggerCacheDic = self.standStillBuffTriggerCacheDic
        if buffId in standStillBuffTriggerCacheDic:
            self.unregrStandStillBuffTriggerCache(buffId)

        _uuid = KBEngine.genUUID64()
        _gcd = sMath.gcd(upPreOverlaySec, downPreOverlaySec)
        _timerId = self.addTimerCB(_gcd, '_onStandStillBuffTriggerCallback', (buffId, _uuid, skipTick),
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
        LOG_DBG("_onStandStillBuffTriggerCallback::", buffId, uuid, skipTick)
        standStillBuffTriggerCacheDic = self.standStillBuffTriggerCacheDic
        if buffId not in standStillBuffTriggerCacheDic:
            LOG_WARN("_onStandStillBuffTriggerCallback:: missing buffId", buffId, uuid)
            return

        if uuid != standStillBuffTriggerCacheDic[buffId]['uuid']:
            LOG_WARN("_onStandStillBuffTriggerCallback:: uuid mismatch", buffId, uuid,
                        standStillBuffTriggerCacheDic[buffId])
            return

        _data = standStillBuffTriggerCacheDic[buffId]
        _now = utils.curTS()
        if self.hasState(gameconst.StateEnum.Moving):
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
        _timerId = self.addTimerCB(_gcd, '_onStandStillBuffTriggerCallback', (buffId, uuid, skipTick),
                                  gametimer.TIMER_TAG_STANDSTILL_BUFF_LOOP_TRIGGER)
        _data["timerId"] = _timerId

    def unregrStandStillBuffTriggerCache(self, buffId):
        LOG_IFO("unregrStandStillBuffTriggerCache::", buffId)
        _data = self.standStillBuffTriggerCacheDic.pop(buffId, None)
        if not _data:
            return

        if _data['timerId']:
            self.cancelTimerCB(_data['timerId'], gametimer.TIMER_TAG_STANDSTILL_BUFF_LOOP_TRIGGER)

        _buffSrcKey = self.getBuffSrcKey(_data['buffId'], self.id)
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
        self.doInitBaseProperties()
        self.initCombatProps(hpPercent, mpPercent)
        self.checkEffectEventCDInfoExpired()
        self.isWitnessComplete = gameconst.WitnessTypeEnum.WITNESS_ENUM_ALL
        self.stateList = formula.getInt64ListOnIndexes(self.getStateBitVector())

        # 缓存下是否矿战场景
        if formula.inMineWarScene(self.spaceNo):
            self.cellFlags = utils.bset(self.cellFlags, gameconst.CELL_FLAGS_IS_MINE_WAR_SPACE)

    def isAttackable(self, src):
        return utils.isJoinCombat(self, src)

    def doInitBaseProperties(self):
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
            self.checkOnUpdateProp(propName, gameconst.SourceType.SrcTpInit, checkedPropSet)

        # 上面不会重算hp,mp这种存数据库的属性，这里重设下处理数值被离线修改的情况
        self.hp = math.ceil(self.fullHp * hpPercent)
        self.mp = math.ceil(self.fullMp * mpPercent)

        LOG_DBG("initCombatProps", self.hp, self.fullHp, self.mp, self.fullMp)

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
        isInit = (src == gameconst.SourceType.SrcTpInit)
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
                LOG_ERR('Error: failed to call func in checkOnUpdateProp:  %s, reason:%s.' % (affectedProp, repr(e)))

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
                        '__init__', 'checkOnUpdateProp', 'doInitBaseProperties', 'inheritProps'):
                    return

                lastFrame = f
                f = f.f_back

            if lastFrame.f_code.co_name in ('onScriptSetAttr',):
                return

            gameengine.panicStack('cannot set %s directly to %s' % (key, value))

    def addProp(self, propName, delta, src=gameconst.SourceType.SrcTpDefault):
        if KBEngine.publish() == 0:
            curVal = self.getProp(propName)
            if type(curVal) is int and type(curVal) != type(delta):
                gameengine.panicStack('addProp type error', propName, curVal, delta)

        oldVal = getattr(self, propName)
        newVal = type(oldVal)(oldVal + delta)
        self.setProp(propName, newVal, src)

        for changedSrc in (src, gameconst.SourceType.SrcTpAll):
            if propName in handlerMap and changedSrc in handlerMap[propName]:
                handlerMap[propName][changedSrc](src, oldVal)

    def setProp(self, propName, value, src=gameconst.SourceType.SrcTpDefault):
        if KBEngine.publish() == 0:
            curVal = self.getProp(propName)
            if type(curVal) is int and type(curVal) != type(value):
                gameengine.panicStack('setProp type error', propName, curVal, value)
            # 初始化的日志太多了
            if src != gameconst.SourceType.SrcTpInit:
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

        for changedSrc in (src, gameconst.SourceType.SrcTpAll):
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
    @propChangedHandler(gameconst.SourceType.SrcTpAll, ('adjCD', 'mulCD'))
    def onCDPropChanged(self, srcType, oldVal):
        # CD发生了变化,需要同步客户端
        for skillVal in self.skillDic.values():
            skillVal.changeCD(self, 0.0)
    @propChangedHandler((gameconst.SourceType.SrcTpAll, ), ('drugsQuantity',))
    def onDrugsQuantityChanged(self, srcType, oldVal):
        LOG_DBG('onDrugsQuantityChanged', srcType, oldVal)
        self.base.onDrugsQuantitySync(self.drugsQuantity)

    @propChangedHandler((gameconst.SourceType.SrcTpAll, ), ('speed',))
    def onSpeedChanged(self, srcType, oldVal):
        LOG_DBG('onSpeedChanged', srcType, oldVal)
        if self.IsAvatar:
            self.speedChanged(self.speed, oldVal)

    def onEffectAddProp(self, propName, delta, callerInfo, effectId, effectIdx):
        propsByEffect = self.getTempMiscProp(gameconst.EntityPropsEnum.effectSetProps)
        if propsByEffect and propName in propsByEffect:
            LOG_ERR('onEffectAddProp error: cannot modify prop set by another effect')
            return

        curVal = self.getProp(propName)
        delta = type(curVal)(delta)

        newVal = curVal + delta
        self.setProp(propName, newVal, gameconst.SourceType.SrcTpBuff)

    def onEffectSetProp(self, propName, newVal, callerInfo, effectId, effectIdx):
        if not self.hasTempMiscProp(gameconst.EntityPropsEnum.effectSetProps):
            self.setTempMiscProp(gameconst.EntityPropsEnum.effectSetProps, {})

        propsByEffect = self.getTempMiscProp(gameconst.EntityPropsEnum.effectSetProps)
        newCallerKey = callerInfo.getCallerKey(effectId, effectIdx)
        if propName in propsByEffect:
            oldVal, setCnt, oldCallerKey = propsByEffect[propName]
        else:
            oldVal = self.getProp(propName)
            setCnt = 0

        propsByEffect[propName] = (oldVal, setCnt + 1, newCallerKey)
        self.setProp(propName, newVal, callerInfo.getCallerSrc())

    def onEffectUnsetProp(self, propName, callerInfo, effectId, effectIdx):
        propsByEffect = self.getTempMiscProp(gameconst.EntityPropsEnum.effectSetProps)
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
                self.popTempMiscProp(gameconst.EntityPropsEnum.effectSetProps)
        else:
            gameengine.panicStack('onEffectUnsetProp: prop missing %s %s' % (propName, callerSrcKey))
            return

    def isDie(self):
        return self.hasState(gameconst.StateEnum.Death)

    def hasSkill(self, skillId):
        if skillId <= 0:
            return False

        skill = self.skillDic.doGetSkill(skillId, False)
        if not skill:
            return False

        return True

    def safePopSkill(self, skillId):
        if skillId <= 0:
            return

        _skill = self.skillDic.doGetSkill(skillId)
        if _skill:
            _skill.resetSkill(self)

        return self.removeSkill(skillId)

    def addSkillInEntity(self, skillId, skillLv, tNextCast=0):
        if skillId not in SSD.datas:
            LOG_ERR('addSkillInEntity skillID not in configTable', skillId)
            return

        if skillId not in self.skillDic:
            skill = self.skillDic.doAddSkill(self, skillId, skillLv, tNextCast=tNextCast)
            self.onEffectEvent('onAddSkill', self.id, self.id, effectEventCtx.AddSkillEventCtx(skillId))
            return skill

        return

    def setAllSkillLv(self, skillLv):
        for sVal in self.skillDic.values():
            sVal.setLevel(self, skillLv)

    def getSkillByCategory(self, skillId, level):
        category = SSD.datas[skillId].get('category', 0)
        if category in (
                gameconst.SkillCategory.CATEGORY_CAST_SKILL_WITH_ACTION, gameconst.SkillCategory.CATEGORY_CAST_SKILL_WITHOUT_ACTION):
            skill = combatSkill.getSkillClass(skillId)(skillId, level)
        elif category == gameconst.SkillCategory.CATEGORY_GENERAL_SKILL:
            skill = self.skillDic.doGetSkill(skillId)
        else:
            skill = None

        return skill

    def getBuffSrcKey(self, buffId, srcEntId=None):
        bd = BBD.datas.get(buffId, {})
        if bd.get('isCover', 1):
            return 0

        # addBuff里releaseRole会转成host，所以这里也要转一下，否则会出现creation加的buff自己无法找到，因为srcKey算到主人去了
        if (self.IsCreation or self.IsSummon) and self.getHost():
            return self.getHost().getBuffSrcKey(buffId, srcEntId)

        return srcEntId if srcEntId is not None else self.id

    def getBuffByBuffId(self, buffId, buffSrcKey=None):
        buffMap = self.buffDic.get(buffId, {})
        if buffSrcKey is None:
            buffSrcKey = self.getBuffSrcKey(buffId)

        return buffMap.get(buffSrcKey)

    def checkRemoveBuffOnTargetTypeChanged(self):
        rmBuffs = []
        for buffId, buffMap in self.buffDic.items():
            for buffSrcKey, buffVal in buffMap.items():
                srcEnt = buffVal.releaseRole
                if not srcEnt or srcEnt.id == self.id:
                    continue
                if buff.Buff.getKind(buffId) < 0 and utils.checkTargetTypeValid('Friend', srcEnt, self):
                    rmBuffs.append((buffId, buffSrcKey))
                elif buff.Buff.getKind(buffId) >= 0 and utils.checkTargetTypeValid('Enemy', srcEnt, self):
                    rmBuffs.append((buffId, buffSrcKey))

        for buffId, buffSrcKey in rmBuffs:
            self.removeBuff(buffId, buffSrcKey)

    def removeAllBuff(self):
        for buffId in list(self.buffDic.keys()):
            self.removeBuff(buffId)

    def removeBuff(self, buffId, buffSrcKeys=None, isFinished=False, removeType=gameconst.RemoveType.RTEnumDefault):
        if not buffId in self.buffDic:
            return
        LOG_DBG('removeBuff', buffId, buffSrcKeys, removeType)
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

    def removeBuffBySkillId(self, skill):
        skillId = skill.skillId
        LOG_IFO('removeBuffBySkillId 1 ', skillId)
        buffIds = list(self.buffDic.keys())
        for buffId in buffIds:
            bufData = self.buffDic.get(buffId)
            if not bufData:
                continue
            buffSrcKeys = list(bufData.keys())
            for buffSrcKey in buffSrcKeys:
                buffVal = bufData.get(buffSrcKey)
                if not buffVal:
                    continue
                ctx = buffVal.getContext()
                if not ctx:
                    continue
                
                ctx = ctx.getTopCtxFromActionQueue(actionContext.ACTION_USE_SKILL)
                if ctx:
                    if ctx.skillId == skillId:
                        LOG_IFO('removeBuffBySkillId 2 ', skillId, buffId)
                        self.removeBuff(buffId)
                    else:
                        if self.school == gameconst.CharacterType.Taoist:
                            if ctx.skillId == dataUtils.getSkillIdByMorphState(skillId, gameconst.MORPH_BUILD_STATE):
                                LOG_IFO('removeBuffBySkillId 3 ', skillId, buffId)
                                self.removeBuff(buffId)

    def removeBuffWithoutCalc(self, buffId, srcKeys):
        self.buffDic.removeWithoutCalc(self, buffId, srcKeys)

    def broadcastAddBuffEvent(self, buffID, srcKeys):
        self.allClientsOnAddBuff(buffID, srcKeys)

    def broadcastRemoveBuffEvent(self, buffID):
        pass

    def addBuff(self, buffId, level, releaseRoleId, duration=-1, rootContext=None, kwargs=None):
        LOG_DBG("addBuff ", buffId, level, releaseRoleId, duration, kwargs)
        if buffId not in buff_buff.datas:
            LOG_ERR('addBuff buffId not in configTable', buffId)
            return

        if self.isDie() and not buff.Buff.getDeadDontRemove(buffId):
            return

        if len(self.buffDic) >= gameconst.MAX_BUFF_COUNT:
            LOG_WARN('buff num reaches max, ignore', buffId)
            return

        releaseRole = KBEngine.entities.get(releaseRoleId)

        if not releaseRole:
            LOG_WARN('addBuff fail: invalid src entity', buffId, level, releaseRoleId, rootContext)
            return

        buffSrcKey = releaseRole.getBuffSrcKey(buffId)
        if self.hasBuff(buffId, buffSrcKey):
            self.removeBuff(buffId, buffSrcKey)

        if releaseRole.IsAvatar:
            releaseRoleGbId = releaseRole.gbId
        else:
            releaseRoleGbId = None
        self.buffDic.doAddBuff(self, buffId, level, duration, releaseRoleId, releaseRole.name, releaseRoleGbId,
                               gameconst.BuffSrcTypeEnum.Combat, buffSrcKey, rootContext, kwargs)

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
        LOG_DBG('changeBuffLevel::', buffId, changeLevel, releaseRoleId, duration, levelLimit, autoHandleBuff)
        if buffId not in buff_buff.datas:
            LOG_ERR('changeBuffLevel:: buffId not in configTable', buffId)
            return False

        if self.isDie():
            return False

        _buffSrcKey = self.getBuffSrcKey(buffId, releaseRoleId)
        _buff = self.getBuffByBuffId(buffId, _buffSrcKey)

        # case1: 没有buff
        if not _buff:
            if not autoHandleBuff:
                LOG_ERR('changeBuffLevel:: can\'t changeBuffLevel if buff not exist', buffId, changeLevel)
                return False

            if changeLevel <= 0:
                # Nothing to do here
                return True

            else:
                if levelLimit and levelLimit < changeLevel:
                    LOG_WARN('changeBuffLevel:: 1 over level limit, reset level to limit', changeLevel, levelLimit)
                    changeLevel = levelLimit
                self.addBuff(buffId, changeLevel, releaseRoleId, duration, rootContext)
                return True

        buffLevel = _buff.level
        buffNewLevel = max(0, buffLevel + changeLevel)

        # case2: 新的buff层数<=0
        if buffNewLevel <= 0:
            if not autoHandleBuff:
                LOG_ERR('changeBuffLevel:: can\'t changeBuffLevel if new buff level <= 0', changeLevel, buffNewLevel)
                return False
            self.removeBuff(buffId, _buffSrcKey)
            return True

        # default: 更新buff层数
        if levelLimit and levelLimit < buffNewLevel:
            LOG_DBG('changeBuffLevel:: 2 over level limit, reset level to limit', buffNewLevel, levelLimit)
            buffNewLevel = levelLimit
        _buff.overlayBuff(self, buffNewLevel, duration)
        self.allClientsOnUpdateBuff(buffId, _buff.getClientStream())
        return True

    def changeBuffDuration(self, buffId, duration, releaseRoleId, rootContext=None, autoHandleBuff=True):
        """修改buffDuration"""
        LOG_DBG('changeBuffDuration::', buffId, duration, releaseRoleId, rootContext, autoHandleBuff)
        if buffId not in buff_buff.datas:
            LOG_ERR('changeBuffDuration:: buffId not in configTable', buffId)
            return False

        if self.isDie():
            return False

        _buffSrcKey = self.getBuffSrcKey(buffId, releaseRoleId)
        _buff = self.getBuffByBuffId(buffId, _buffSrcKey)

        # case1: 没有buff
        if not _buff:
            if not autoHandleBuff:
                LOG_ERR('changeBuffDuration:: can\'t changeBuffDuration if buff not exist', buffId, duration)
                return False

            if duration <= 0:
                # Nothing to do here
                return True
            else:
                self.addBuff(buffId, 1, releaseRoleId, duration, rootContext)
                return True

        # case2: 新的buff duration<=0
        if duration <= 0:
            if not autoHandleBuff:
                LOG_ERR('changeBuffDuration:: can\'t changeBuffDuration if new buff level <= 0', duration)
                return False
            self.removeBuff(buffId, _buffSrcKey)
            return True

        # default: 更新buff duration
        _buff.overlayBuff(self, _buff.level, duration)
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
        buffSrcKey = srcEnt.getBuffSrcKey(buffId)
        if buffSrcKey in buffMap:
            buffLv = buffMap[buffSrcKey].level
        return buffLv

    def killSelf(self, sourceType):
        self.modifyHP(-self.hp, self.id, sourceType, 0)

    def goDie(self, killer, srcType, srcId, forceDead=False, context=None):
        LOG_WARN('goDie', killer.id, srcType, srcId, forceDead, context)
        if self.isDie():
            LOG_WARN("goDie:: already dead", killer, srcType, srcId)
            return

        self.onEffectEvent('onDead', killer.id, self.id, effectEventCtx.EE_DEFAULT_CONTEXT)
        if not killer.IsCreation:
            killer.onEffectEvent('onKill', self.id, killer.id, effectEventCtx.EE_DEFAULT_CONTEXT)

        # : 防止时间触发时isDie()返回还未死亡
        self.setState(gameconst.StateEnum.Death)
        self.killChannelingSkill(gameconst.ChannelingBreak.BREAK_TP_SELF_DIE)
        self.killCastingSkill(gameconst.EndCasting.ECEnumDead)
        self.onDead(killer, srcType, srcId)

        if killer.IsAICombatUnit:
            killer.removeHate(self.id)

    def modifyHP(self, hpVal, releaseRoleId, srcType, srcId, forceDead=False, context=None):
        if srcType == gameconst.SourceType.SrcTpItem:
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
        lInfo = self.getTempMiscProp(gameconst.EntityPropsEnum.lockMinHp)
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
                    utils.parseGidFromGameEntityId(self.gameEntityId), int(oldHp), int(curHp), self.fullHp)
                pass

        if curHp <= 0 and self.IsAvatar and self.duelAttr.inFight():
            if self.duelAttr.isDuelEnemy(realReleaseRole) or realReleaseRole.id == self.id:
                self.hp = int(self.getDuelDeathHp(oldHp))
                LOG_IFO('modifyHP:: duel death, hp: ', oldHp, self.hp)
                duelFlag = self.duelAttr.duelFlagEnt()
                if duelFlag:
                    duelFlag.onAvatarDuelFailed(self.id)
                else:
                    LOG_ERR('modifyHP:: duelFlagEntity not found', self.id)

        # 矿战怪物免死
        if formula.inMineWarScene(self.spaceNo) and curHp <= 0 and self.IsMonster:
            self.hp = curHp = self.mineWarMonsterImmuneDeath(releaseRole, srcType, srcId, curHp)

        hpDelta = self.hp - oldHp
        if hpDelta < 0 and realReleaseRole.IsAvatar:
            realReleaseRole.addDamageSetInFighting(self)

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
                self.killChannelingSkill(gameconst.ChannelingBreak.BREAK_TP_BE_ATK)
            elif interruptType == 2:  # 必定打断
                self.killChannelingSkill(gameconst.ChannelingBreak.BREAK_TP_BE_ATK)

        castingSkillVal = self.getCastingSkillInfo()
        # 吟唱技能需要额外判断是否在吟唱状态，skillVal在吟唱+施法过程中都存在
        if castingSkillVal and self.hasState(gameconst.StateEnum.Casting):
            # 吟唱时收到伤害
            interruptType = castingSkillVal.getInterruptByAttack(castingSkillVal.skillId)
            if interruptType == 0:  # 不能打断
                pass
            elif interruptType == 1 and random.uniform(0, 1) <= self.skillBroken:  # 按概率打断
                self.killCastingSkill(gameconst.EndCasting.ECEnumBeAttacked)
            elif interruptType == 2:  # 必定打断
                self.killCastingSkill(gameconst.EndCasting.ECEnumBeAttacked)

    def modifyMP(self, mpVal, context=None):
        if context:
            srcType = context.getDmgSourceType()
            if srcType == gameconst.SourceType.SrcTpBuff and context.parentContext:
                srcType = context.parentContext.getDmgSourceType()
            if srcType == gameconst.SourceType.SrcTpItem:
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

    def removeSkill(self, skillID, isFromDeleteTempSkill = False):
        LOG_DBG('removeSkill ', skillID, isFromDeleteTempSkill)
        skill = self.skillDic.doGetSkill(skillID, False)
        if skill:
            if isFromDeleteTempSkill:
                self.removeBuffBySkillId(skill)
            self.skillDic.doRemoveSkill(skillID)
        return skill
    
    def doActionOnChangeSlot(self, skillId, skillLv, bActive, bTakeSkill, fromSkillNextCastTime):
        LOG_DBG('doActionOnChangeSlot ', skillId, skillLv, bActive, bTakeSkill, fromSkillNextCastTime)
        if bTakeSkill:
            skill = self.takeSkill(skillId, skillLv, tNextCast = fromSkillNextCastTime)
        else:
            skill = self.skillDic.doGetSkill(skillId, False)

        if not skill:
            return
        skill.doActionOnChangeSlot(self, bActive)

    @utils.isMyself
    def cancelChargeSkill(self, exposed, skillId):
        LOG_ERR('cancelChargeSkill not implemented')

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
    
    def enterFlyingState(self):
        pass
    def leaveFlyingState(self):
        pass

    def setStateBitVector(self, stateVec):
        isSetState = False
        if self.state != stateVec[0]:
            self.state = stateVec[0]
            isSetState = True
        if self.state2 != stateVec[1]:
            self.state2 = stateVec[1]
            isSetState = True
        if isSetState:
            self.stateList = formula.getInt64ListOnIndexes(stateVec)

    def setState(self, state, reportErr=True, isInit=False):
        if state < 0:
            reportErr and LOG_ERR("states is error:", state)
            return False
        """return True if state is exist"""
        if self.hasState(state) and not isInit:
            if state == gameconst.StateEnum.Fighting and self.IsAvatar:
                self.enterFightingState()
            return True

        eventId = CSD.datas[state].get('event')
        conflictRes = self.checkConflictState(eventId, remConflctState=False, isInit=isInit)
        if eventId and not conflictRes:
            # 现在设置状态前没有判断与当前状态是否冲突，可能会设置失败，这里打个trace检查这种情况
            reportErr and gameengine.panicStack('setState fail', eventId, state, conflictRes.extra)

            return False

        if state == gameconst.StateEnum.Fighting:
            if not self.hasState(gameconst.StateEnum.Fighting):
                self.enterFightingState()
            else:
                return True

        elif state == gameconst.StateEnum.Sprinting:
            if not self.hasState(gameconst.StateEnum.Sprinting):
                self.enterSprintingState()
            else:
                return True

        elif state in gameconst.StateEnum.breakSkillStates:
            self.breakSkillByState()

        elif state == gameconst.StateEnum.Flying:
            self.enterFlyingState()

        stateVec = self.getStateBitVector()
        formula.setInt64ListBit(stateVec, state)

        rmStates = []
        stateBitsList = self.stateList
        stateBitsList.append(state)
        if eventId:
            for st in stateBitsList:
                if st != state:
                    val = conflict_conflict.datas[eventId].get(str(st))
                    if val == 0:
                        reportErr and LOG_ERR("checkConflict false", eventId, state, st, self.state, stateBitsList)
                    elif val == 2:
                        formula.setInt64ListBit(stateVec, st, on=False)
                        rmStates.append(st)

        self._onRemovedStateBefore(rmStates, state)
        self.setStateBitVector(stateVec)
        self._onRemovedState(rmStates, state)

        if state == CCDD.datas.MImmortal:
            self.removeBuffByKind(gameconst.BuffKind.KindMagicalDoT)
        elif state == CCDD.datas.PImmortal:
            self.removeBuffByKind(gameconst.BuffKind.KindPhysicalDoT)

        if self.IsAvatar and state == gameconst.StateEnum.autoFight:
            if formula.inTeamDungeonScene(self.spaceNo) or formula.inRaidDungeonScene(self.spaceNo):
                self.setTempMiscProp(gameconst.EntityPropsEnum.autoCombatStartTimestamp, utils.curTS())
        
        return True

    def removeState(self, state, removeReason=0):
        if state < 0:
            LOG_ERR("states is error:", state)
            return
        if not self.hasState(state):
            return

        stateVec = self.getStateBitVector()
        formula.setInt64ListBit(stateVec, state, on=False)

        self._onRemovedStateBefore([state], state, removeReason=removeReason)
        self.setStateBitVector(stateVec)
        self._onRemovedState([state], state, removeReason=removeReason)
        self.doRemoveState(state)

    def removeStates(self, rmStates, byConflictState=-1, removeReason=0):
        stateVec = self.getStateBitVector()

        for state in rmStates:
            formula.setInt64ListBit(stateVec, state, on=False)
            self.doRemoveState(state)
        self._onRemovedStateBefore(rmStates, byConflictState)
        self.setStateBitVector(stateVec)
        self._onRemovedState(rmStates, byConflictState, removeReason)

    def doRemoveState(self, state):
        if self.IsAvatar and state == gameconst.StateEnum.autoFight:
            if formula.inTeamDungeonScene(self.spaceNo) or formula.inRaidDungeonScene(self.spaceNo):
                lastTimestammp = self.popTempMiscProp(gameconst.EntityPropsEnum.autoCombatStartTimestamp, 0)
                if lastTimestammp > 0:
                    autoFightTimes = utils.curTS() - lastTimestammp
                    if autoFightTimes > 0:
                        self.spaceMgr and self.spaceMgr.recordAutoFightTimes(self.gbId, state, autoFightTimes)

    def hasState(self, state):
        if state < 0:
            LOG_ERR("states is error:", state)
            return False
        if state >= 64:
            return (self.state2 >> (state - 64)) & 1 > 0
        else:
            return (self.state >> state) & 1 > 0

    def _onRemovedStateBefore(self, states, byConflictState=-1, removeReason=0):
        pass

    def _onRemovedState(self, states, byConflictState=-1, removeReason=0):
        for state in states:
            if state == gameconst.StateEnum.Fighting:
                self.leaveFightingState()

            elif state == gameconst.StateEnum.autoFight:
                self._stopAutoCombat()

            elif state == gameconst.StateEnum.Moving and hasattr(self, 'removeMoveController'):
                self.removeMoveController()

            elif state == gameconst.StateEnum.Channeling or state == gameconst.StateEnum.moveChannel:
                LOG_DBG("removeState  killChannelingSkill ")
                if removeReason:
                    self.killChannelingSkill(removeReason)
                else:
                    self.killChannelingSkill(gameconst.ChannelingBreak.BREAK_TP_CONFLICT_STATE)

            elif state == gameconst.StateEnum.Casting:
                LOG_DBG("removeState  killCastingSkill ", byConflictState)
                if byConflictState >= 0 and byConflictState in (gameconst.StateEnum.Moving, gameconst.StateEnum.Idle):
                    self.killCastingSkill(gameconst.EndCasting.ECEnumMove)
                elif byConflictState == gameconst.StateEnum.Death:
                    self.killCastingSkill(gameconst.EndCasting.ECEnumDead)
                elif byConflictState == gameconst.StateEnum.clientPick:
                    self.killCastingSkill(gameconst.EndCasting.ECEnumclientPick)
                else:
                    self.killCastingSkill(gameconst.EndCasting.ECEnumConflictState)

            elif state == gameconst.StateEnum.riding:
                self._onExitRiding(byConflictState)

            elif state == gameconst.StateEnum.clientPick:
                self._onExitClientPick(byConflictState, removeReason)

            elif state == gameconst.StateEnum.posture:
                self.exitPlayEmote(byConflictState, removeReason)

            elif state == gameconst.StateEnum.GeneralAttack:
                if removeReason != gameconst.RemoveStateReason.SKILL_DONE:
                    self._breakGeneralSkill()

            elif state == gameconst.StateEnum.Shifting or state == gameconst.StateEnum.Dodging:
                self.endMovement()
                if removeReason == gameconst.RemoveStateReason.CONFLICT:
                    LOG_DBG('[exitShift] by conflict')
                    self.allClients.onExitShiftByConflict(self.position)

            elif state == gameconst.StateEnum.Sprinting:
                self.leaveSprintingState()
            elif state == gameconst.StateEnum.Flying:
                if byConflictState not in (gameconst.StateEnum.Fall, gameconst.StateEnum.speedFall):
                    self.setState(gameconst.StateEnum.Fall)
                self.addTimerCB(1, '_onRemoveFlyingState', (), gametimer.TIMER_TAG_ON_REMOVE_FLY_STATE)

                self.leaveFlyingState()

            elif state == CCDD.datas.duel:
                self.leaveDuelState()
            elif state == CCDD.datas.blazing:
                self.leaveBlazeState()

            buffTag = CSD.datas[state].get('buffTag')
            if buffTag:
                self.removeBuffByTag(buffTag)

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
                bMsg and LOG_WARN("has conflict eventId=[{}] state=[{}] val=[0]".format(eventId, state))
                return gameclass.BoolResult(False, state)
            elif val == 2 and remConflctState:
                remState.append(state)
            elif val == 3:
                bMsg and LOG_WARN("has conflict eventId=[{}] state=[{}] val=[3]".format(eventId, state))
                return gameclass.BoolResult(False, state)
            elif MSG.datas.get(val, None):
                bMsg and LOG_WARN("has conflict eventId=[{}] state=[{}] val=[{}]".format(eventId, state, val))
                return gameclass.BoolResult(False, state)

        # todo remove conflict state, new state continue gooooo
        if len(remState) > 0:
            self.removeStates(remState, removeReason=gameconst.RemoveStateReason.CONFLICT)

        return gameclass.BoolResult(True, -1)

    def getRandomPosition(self, center, radii):
        posList = self.getRandomPoints(center, radii, 1, 0)
        if not posList:
            return None

        return posList[0]

    def getRandomPositionByBoxRadius(self, center, radii, boxRadii, num):
        if num <= 10:
            maxNum = num*3
        else:
            maxNum = num*2
        _posList = self.getRandomPoints(center, radii, maxNum, 0)
        if not _posList:
            return [center]*num
        if len(_posList) <= num:
            _posList.extend([center]*(num-len(_posList)))
            return _posList

        selected = utils.select_positions(_posList, num, boxRadii)
        return selected

    def recordUseSkill(self, skillVal, targetId):
        pass

    def removeUseSkillRecord(self, skillId):
        pass

    def useSkillFinish(self, skillId):
        if self.IsAvatar and self.autoCombat == gameconst.AutoCombatState.Fighting:
            self.autoCombatCheckUseSkill(skillId)

    def _castSkillByServer(self):
        return False

    def doUseSkill(self, skill, actionCtx, compensateTime=0, doSetState=True, fixDir=None, ignoreReasons=0):
        LOG_DBG("doUseSkill ", skill.skillId, actionCtx.useTargetId, actionCtx.skillArgs, actionCtx.isClient, compensateTime)
        if skill.hasSkillTag(gameconst.SkillTag.changeCDStatusSkill) \
            and skill.getTempData(gameconst.SkillTempDataKey.CHANGE_SKILL_CD_STATUS, gameconst.SkillCDStatus.DEFAULT) == gameconst.SkillCDStatus.DISABLED:
            return False

        if skill.hasSkillTag(gameconst.SkillTag.Casting):
            return self._castingSkillObjInternal(skill, actionCtx)
        else:
            return self._useSkillBySkillObj(skill, actionCtx, compensateTime, doSetState=doSetState, fixDir=fixDir, ignoreReasons=ignoreReasons)

    def _breakGeneralSkill(self):
        usingSkills = self.getTempMiscProp(gameconst.EntityPropsEnum.currentUseSkill, default={})
        for sid in list(usingSkills.keys()):
            if sid not in usingSkills:
                continue

            sVal, tid = usingSkills[sid]
            if sVal.hasSkillTag(gameconst.SkillTag.GeneralSkill):
                sVal.useSkillDone(self, 0, [], isSucc=False, doRemoveState=True, forceResetSkill=True)

    def _useSkillBySkillObj(self, skill, actionCtx, compensateTime=0, doSetState=True, fixDir=None, ignoreReasons=0):
        skillId = skill.skillId
        LOG_IFO('_useSkillBySkillObj: skill:{}, tgt:{}, arr:{}, {}'.format(skillId, actionCtx.useTargetId, actionCtx.skillArgs, actionCtx.isClient))
        # 走到这里如果不是Avatar，则一定是吟唱成功，如果是Avatar暂且认为吟唱过程成功，在canUse里会做校验
        castingSkillVal = self.getCastingSkillInfo()
        if castingSkillVal and self.hasState(gameconst.StateEnum.Casting):
            if castingSkillVal.skillId == skillId and castingSkillVal.isCastingSucc(delta=0.2):
                endReason = gameconst.EndCasting.ECEnumFinished
            else:
                endReason = gameconst.EndCasting.ECEnumOtherSkill

            self._endCastingSkill(endReason)

        realSkill, replaceSkill = skill.getRealSkillVal(self)
        if actionCtx.isClient:
            ignoreReasons |= gameconst.UseSkillCheck.USC_ENUM_INVALID_TARGET

        ret = realSkill.checkUseSkill(self, actionCtx.useTargetId, ignoreReasons, checkInRange=actionCtx.checkInRange)

        if ret != gameconst.UseSkillCheck.USC_ENUM_CHEKC_OK:
            target = KBEngine.entities.get(actionCtx.useTargetId)
            if not (target and target.isDie()):
                LOG_WARN("Spell::doUseSkill(%i):skillID=%i ret=%i tNextCast=%i" % (self.state, skillId, ret, skill.tNextCast))

            self.combatDebugMsg('_useSkillBySkillObj doUseSkill fail: targetId:%s, ret:%s, skillArgs:%s', actionCtx.useTargetId, ret, actionCtx.skillArgs)
            self.client.onUseSkill(False, skillId, actionCtx.useTargetId, [], [], [])
            return ret

        # 多段技能check时按当前段check，但是replaceSkill是false，表示使用时还调用第一段的使用
        # 因为后面段是第一段的子技能，子技能只能通过父技能使用
        if actionCtx.isClient and not realSkill.checkSkillArgs(actionCtx.skillArgs):
            LOG_ERR("doUseSkill: invalid skill args", realSkill.skillId, actionCtx.useTargetId, actionCtx.skillArgs)
            if realSkill.isChangePositionSkill(realSkill.skillId):
                self.client.onUseSkill(False, skillId, actionCtx.useTargetId, [], [], [])
            return None

        if utils.hasSkillTagById(skillId, gameconst.SkillTag.UltraSkill):
            self.resetUsingSkills(gameconst.ResetSkillReason.ReasonUltraSkill)

        if fixDir is not None:
            self.direction = fixDir

        if replaceSkill:
            self.recordUseSkill(realSkill, actionCtx.useTargetId)
            isSucc = realSkill.beginUseSkill(self, actionCtx.useTargetId, actionCtx.skillArgs, compensateTime, doSetState=doSetState, parentCtx=actionCtx)
            isGeneral = realSkill.hasSkillTag(gameconst.SkillTag.GeneralSkill)
        else:
            self.recordUseSkill(skill, actionCtx.useTargetId)
            isSucc = skill.beginUseSkill(self, actionCtx.useTargetId, actionCtx.skillArgs, compensateTime, doSetState=doSetState, parentCtx=actionCtx)
            isGeneral = skill.hasSkillTag(gameconst.SkillTag.GeneralSkill)

        if isSucc and not isGeneral:
            self._breakGeneralSkill()

        return None

    def delayCalcSkill(self, skillVal, targetId, arr, actionCtx, calcDelay, doRemoveState=True):
        # delay过程中如果有传送，skillVal不是skillDic里的值，这里重拿一次
        skill = self.skillDic.doGetSkill(skillVal.skillId, reportErr=False)
        # 如果getSkill没拿到，说明这种技能不是skillDic里的技能，就用iTimer里存的即可

        skill = skill or skillVal
        actionCtx.skillObj = skill
        if not skill:
            LOG_ERR('delayCalcSkill: cannot get skill', skill.skillId, targetId)
            return

        skill._cancelTempTimer(self, gameconst.SkillTempDataKey.DELAY_CALC_TIMER, gametimer.TIMER_TAG_SKILL_DELAY_CALC)
        ignoreReasons = gameconst.UseSkillCheck.USC_DELAY_CHECK_IGNORES

        if skill.checkUseSkill(self, targetId, ignoreReasons=ignoreReasons) != gameconst.UseSkillCheck.USC_ENUM_CHEKC_OK:
            skill.useSkillDone(self, targetId, arr, False, doRemoveState)
            return

        self._doUseSkill(skill, targetId, arr, actionCtx, calcDelay, doRemoveState)

    def _doUseSkill(self, skill, targetId, arr, actionCtx, calcDelay, doRemoveState=True):
        skill.applySkillEffect(self, targetId, arr, actionCtx, calcDelay, doRemoveState)

    def _onSkillCallback(self, skillVal, callbackName, args):
        skillVal.onTimerCallback(self, callbackName, args)

    def _castingSkillObjInternal(self, skillObj, actionCtx):
        self.combatDebugMsg("_castingSkillObjInternal:%s %s %s", skillObj.skillId, actionCtx.useTargetId, actionCtx.skillArgs)
        if self.hasState(gameconst.StateEnum.Casting):
            return None

        if not self.checkConflictState(CCD.datas.cast):
            LOG_IFO('skill %d cannot use: checkConflict: %d' % (skillObj.skillId, CCD.datas.cast))
            return None

        skillID = skillObj.skillId
        skillLv = skillObj.skillLv
        realSkillVal, replaceSkill = skillObj.getRealSkillVal(self)
        if replaceSkill:
            ret = self._useSkillBySkillObj(realSkillVal, actionCtx)
            return ret

        ignoreReasons = gameconst.UseSkillCheck.USC_ENUM_STATE_CONFLICT | gameconst.UseSkillCheck.USC_ENUM_NEED_CAST
        if actionCtx.isClient:
            ignoreReasons |= gameconst.UseSkillCheck.USC_ENUM_INVALID_TARGET

        ret = skillObj.checkUseSkill(self, actionCtx.useTargetId, ignoreReasons=ignoreReasons)
        if ret != gameconst.UseSkillCheck.USC_ENUM_CHEKC_OK:
            LOG_IFO("Spell::castingSkill(%i): cannot spell skillID=%i, targetID=%i, code=%i" % (
                self.id, skillID, actionCtx.useTargetId, ret))
            return ret

        self.removeState(gameconst.StateEnum.Moving)
        self.setState(gameconst.StateEnum.Casting)
        skillArgsExtra = [skillObj.getRange(self, skillID, skillLv), skillObj.getEffectRange(self, skillID, skillLv)]
        self.client and self.client.onUseCasting(self.id, skillID, actionCtx.useTargetId, actionCtx.skillArgs, [], skillArgsExtra)
        self.otherClients.onUseCasting(self.id, skillID, actionCtx.useTargetId, actionCtx.skillArgs, [], skillArgsExtra)
        self.setTempMiscProp(gameconst.EntityPropsEnum.currentCastingSkill, skillObj)
        skillObj.startCasting(self, actionCtx)
        
        return ret

    def castingSkillCheck(self, targetID, arr, castPos):
        skillObj = self.getCastingSkillInfo()
        skillObj._cancelTempTimer(self, gameconst.SkillTempDataKey.CASTING_CHECK_TIMER, gametimer.TIMER_TAG_CASTING_CHECK)

        if sMath.distance2DToCompareFrom3DPosition(castPos, self.position) > 1:
            self.killCastingSkill(gameconst.EndCasting.ECEnumMove)
            return

        # 如果客户端出错或者其他原因，吟唱时间到了后长时间没有调用spellTarget真正放吟唱技能，这里做容错结束吟唱
        # 对于服务器控制的实体，不会走到这里
        if time.time() - skillObj.castingStartTime > skillObj.getCastingtimeMax(skillObj.skillId) + 1:
            self._endCastingSkill(gameconst.EndCasting.ECEnumFinished)
            return

        timerId = self.addTimerCB(1, 'castingSkillCheck', (targetID, arr, castPos), gametimer.TIMER_TAG_CASTING_CHECK)
        skillObj.setTimerTempData(self, gameconst.SkillTempDataKey.CASTING_CHECK_TIMER, timerId)
        return

    def getCastingSkillInfo(self):
        curSkillInfo = self.getTempMiscProp(gameconst.EntityPropsEnum.currentCastingSkill)

        return curSkillInfo

    def getChannelingSkillInfo(self):
        curSkillInfo = self.getTempMiscProp(gameconst.EntityPropsEnum.currentChannelSkill)

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

        if reason != gameconst.EndCasting.ECEnumFinished:
            castingSkillVal.onCastingInterrupted(self, reason)

        self.popTempMiscProp(gameconst.EntityPropsEnum.currentCastingSkill)
        self.removeState(gameconst.StateEnum.Casting)

        castingSkillVal.resetSkill(self, gameconst.ResetSkillReason.ReasonEndCasting)

    def channelingSkillTick(self, skillObj, targetID, arr, channelPos, actionCtx):
        skillId = skillObj.skillId
        skillLv = skillObj.skillLv
        self.popTempMiscProp(gameconst.EntityPropsEnum.channelSkillTimer)
        skillObj.popTempData(gameconst.SkillTempDataKey.CHANNELING_CALC_TIMER)
        cfgData = SSD.datas[skillId]

        isMoveSkill = skillObj.isMovingSkill(skillId)
        if sMath.distance2DToCompareFrom3DPosition(self.position, channelPos) > 1.0 and not isMoveSkill:
            self.combatDebugMsg('channelingSkillTick move: position:%s, channelPos:%s', self.position, channelPos)
            self.killChannelingSkill(gameconst.ChannelingBreak.BREAK_TP_MOVE)
            return

        target = KBEngine.entities.get(targetID)
        if skillObj.needReleaseTarget() and ((target and target.isDie()) or (targetID > 0 and not target)):
            self.combatDebugMsg('channelingSkillTick target is invalid: targetId:%s', targetID)
            self.killChannelingSkill(gameconst.ChannelingBreak.BREAK_TP_TARGET_DIE)
            return

        if self.isDie():
            self.killChannelingSkill(gameconst.ChannelingBreak.BREAK_TP_SELF_DIE)
            return

        effectTargetIds = skillObj.getEffectTargets(self, targetID, arr)
        skillObj.targetIds = effectTargetIds
        scopes = skillObj.getScope(skillObj.skillId)
        if not effectTargetIds:
            if not scopes or scopes == gameconst.SkillScope.TARGET_AUTO:
                if skillObj.channelCount == 0 and self.IsAvatar:
                    skillObj.setTempData(self, gameconst.SkillTempDataKey.IS_CHANNELING_EMPTY, True)
                if not skillObj.getTempData(gameconst.SkillTempDataKey.IS_CHANNELING_EMPTY, False):
                    self.killChannelingSkill(gameconst.EndCasting.ECEnumMissingTarget)
                    return

        skillObj.channelCount += 1
        skillArgsExtra = [skillObj.getRange(self, skillId, skillLv), skillObj.getEffectRange(self, skillId, skillLv)]
        self.allClients.onUseChanneling(self.id, skillId, targetID, arr, effectTargetIds,
                                        skillObj.channelCount, skillArgsExtra)

        isFinished = skillObj.channelCount >= skillObj.getChannelTime(skillObj.skillId)

        bulletTime = skillObj.calBulletTime(self, targetID)
        bulletTimer = self.addTimerCB(bulletTime, "channelingSkillEffect", (skillObj, targetID, arr, actionCtx, 0,
                                                                           channelPos),
                                     gametimer.TIMER_TAG_CHANNELING_SKILL_EFFECT)
        skillObj.setTimerTempData(self, gameconst.SkillTempDataKey.CHANNELING_BULLET_TIMER, bulletTimer)

        channelInterval = max(cfgData.get('channelInterval') or 1, 0.3)
        if not isFinished:
            timerId = self.addTimerCB(channelInterval, 'channelingSkillTick', (skillObj, targetID, arr, channelPos,
                                                                              actionCtx),
                                     gametimer.TIMER_TAG_CHANNELING_CALC)
            skillObj.setTimerTempData(self, gameconst.SkillTempDataKey.CHANNELING_CALC_TIMER, timerId)
        self.combatDebugMsg('channelingSkillTick done: skillId:%s, state:%s, targetId:%s, channelCount:%s, channelInterval:%s, isFinished:%s',
                            skillId, self.state, targetID, skillObj.channelCount, channelInterval, isFinished)
        return

    def channelingSkillEffect(self, skillObj, targetId, skillArgs, actionCtx, calcDelay, channelPos):
        skillObj.applySkillEffect(self, targetId, skillArgs, actionCtx, calcDelay)
        skillObj.popTempData(gameconst.SkillTempDataKey.CHANNELING_BULLET_TIMER)
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
        self.client.onSetAddSkillCd(skillVal.skillId, float(skillVal.getCD(self)), float(skillVal.tNextCast), False, skillVal.getTempData(gameconst.SkillTempDataKey.RELEASE_TIME, 0), skillVal.getTempData(gameconst.SkillTempDataKey.TOTAL_RELEASE_CNT, 0), skillVal.getTempData(gameconst.SkillTempDataKey.RELEASED_CNT, 0), not skillVal.isSkillCDStatusFrozen())
        if reason != gameconst.ChannelingBreak.BREAK_TP_NORMAR_END:
            skillVal.onChannelingEnd(self, isFinished)
        notifyClient and self.allClients.onBreakChannelingSkill(self.id, skillVal.skillId, reason)

    def _endChannelingSkill(self, isFinished):
        skillVal = self.getChannelingSkillInfo()
        if not skillVal:
            return

        self.combatDebugMsg('_endChannelingSkill: skillId:%s', skillVal.skillId)
        self.popTempMiscProp(gameconst.EntityPropsEnum.currentChannelSkill)

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
            gameengine.panicStack('_executeSkillAction error:', self.id, skillId, str(e), context)

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
                context.actionProgress = gameconst.ActionProgressEnum.actionDoing
                actionFinished = False
            else:
                if context.actionProgress == gameconst.ActionProgressEnum.actionDoing:
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
        doActionTogether = skill.hasSkillTag(gameconst.SkillTag.DoActionTogether)
        skillDamges.damageInfo = []

        skill._cancelTempTimer(self, gameconst.SkillTempDataKey.MUL_ATTACK_ACT_TIMER, gametimer.TIMER_TAG_DO_SKILL_ACTION)

        context.actionProgress = gameconst.ActionProgressEnum.actionDone
        context.checkInRange = False
        if skill.getEffectTarget(skill.skillId) == 'None':
            actionFinished = self._executeSkillAction(skillId, context, calcDelay, actionFunc, None, duration)
        else:
            doActionTargets = []

            if needUseCheck:
                if effectedTargets:
                    for target in effectedTargets:
                        checkCode = skill.checkUseSkill(self, target.id, ignoreReasons=checkIgnoreReasons, checkInRange=context.checkInRange)
                        if checkCode == gameconst.UseSkillCheck.USC_ENUM_CHEKC_OK:
                            break
                    else:
                        skill.onSkillActionFinished(self, context.useTargetId, skillArgs, context, calcDelay, duration)
                        return actionFinished

            isAttackSkill = skill.isAttackSkill(skill.skillId)
            for target in effectedTargets:
                if target.isDestroyed:
                    continue

                if isAttackSkill and not target.hasState(gameconst.StateEnum.Fighting) and utils.isEnemy(self, target):
                    if target.IsAICombatUnit and target.aiController.canEnterFighting():
                        target.setState(gameconst.StateEnum.Fighting)

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

    def onBeforeAttackAction(self, target, context, ignoreType=False):
        if not target or target.isDie():
            LOG_DBG('attack miss target', context)
            return False

        if not ignoreType:
            attackSrcEnt = context.getSrcEntity()
            if attackSrcEnt is None:
                LOG_WARN("onBeforeAttackAction has no src entity")
                return False

            if not utils.checkTargetTypeValid("Enemy", attackSrcEnt, target):
                LOG_WARN("onBeforeAttackAction checkTargetTypeValid error", attackSrcEnt.id, target.id)
                return False

        dmgSchoolType = 0
        ignoreImmortal = False
        if context.actionType == actionContext.ACTION_USE_SKILL:
            skill = self._getSkillByActionContext(context)
            dmgSchoolType = skill.getClassTag(self)
            ignoreImmortal = skill.hasSkillTag(gameconst.SkillTag.IgnoreImmortal)

        elif context.actionType in (actionContext.ACTION_CREATION_LOOP, actionContext.ACTION_CREATION_COMMON):
            dmgSchoolType = CRD.datas.get(context.creationId, {}).get('classTag', 0)

        elif context.actionType in (actionContext.ACTION_AUREOLE,):
            dmgSchoolType = AAD.datas.get(context.aureoleId, {}).get('classTag', 0)

        elif context.actionType in (actionContext.ACTION_BUFF_TICK, actionContext.ACTION_BUFF_END,
                                    actionContext.ACTION_BUFF_EFFECT) and context.getBuffObject():
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

        if self.IsCreation or self.IsSummon or self.IsAvatarMirror:
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

    def calcBeHurtStats(self, target, context, damageResult, realDmgVal):
        if not damageResult.hurtDmg:
            return

        if self.IsSummon:
            host = self.getHost()
            host and host.IsAvatar and host.calcBeHurtStats(target, context, damageResult, realDmgVal)


    def calcHealStats(self, target, context, hpDelta):
        if not hpDelta:
            return

        if self.IsAvatarMirror or self.IsSummon or self.IsCreation:
            host = self.getHost()
            host and host.IsAvatar and host.calcHealStats(target, context, hpDelta)

    def applyDamageResult(self, target, context, damageResult):
        self.combatDebugMsg('applyDamageResult: sourceId:%s, targetId:%s, context:%s, damageResult:%s', context.getDmgSourceId(), target.id, context, damageResult)
        skillDamges = context.getCombatResult()
        if not skillDamges:
            LOG_ERR('unexpected heal action context', context)
            skillDamges = combatSkill.SkillDamges(self.id, context.getDmgSourceType(), context.getDmgSourceId())

        # 是否命中
        damageResult.dmg = int(damageResult.dmg)
        damageResult.hurtDmg = int(damageResult.hurtDmg)
        damageResult.hpSuck = int(damageResult.hpSuck)
        damageResult.dmgType = int(damageResult.dmgType)
        damageResult.atkType = int(damageResult.atkType)
        LOG_DBG("applyDamageResult", damageResult.dmg, damageResult.hurtDmg, damageResult.hpSuck, damageResult.dmgType, damageResult.atkType, damageResult.calcShield)
        # 如果血量被锁定了，就不分摊伤害吸血什么的，也不跳数字了
        if target.getTempMiscProp(gameconst.EntityPropsEnum.isHpLocked, False):
            return 0

        if target.isDie():
            return 0

        dmg = realDmgVal = damageResult.dmg
        absorbDamageDetail = {}

        dmgSrcEnt = context.getSrcEntity() or self
        # AvatarMirror,Pet，召唤物都算自己的，创生算主人的
        if dmgSrcEnt.IsCreation:
            dmgSrcEnt = dmgSrcEnt.getHost() or dmgSrcEnt

        dmgAfterTransfer = realDmgVal

        # 护盾吸收
        shieldAbsorbVal = 0
        if damageResult.calcShield:
            target.onEffectEvent('onBeatShield', self.id, target.id, effectEventCtx.HpEventCtx(dmgAfterTransfer))
            realDmgVal, absorbDamageDetail = target.absorbShieldWithDetails(dmgAfterTransfer)
            shieldAbsorbVal = dmgAfterTransfer - realDmgVal
            if realDmgVal == 0 and shieldAbsorbVal:
                # 全被吸收
                skillDamges.damageInfo.append(combatSkill.SkillDamageVal(target.id, shieldAbsorbVal, gameconst.HitType.Absorb))
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
                        and context.getDmgSourceType() == gameconst.SourceType.SrcTpSkill:
                    host.setState(gameconst.StateEnum.Fighting)
                    if not (targetHost.isDie() or targetHost.hasState(CCDD.datas.relive)):
                        targetHost.setState(gameconst.StateEnum.Fighting)

            if damageResult.atkType == gameconst.SkillAttackType.ATTACK_NORMAL:
                # 普通伤害
                if realDmgVal:
                    if hasattr(context, 'isCombo'):
                        skillDamges.damageInfo.append(combatSkill.SkillDamageVal(target.id, realDmgVal, gameconst.HitType.ComboHit))
                    else:
                        skillDamges.damageInfo.append(combatSkill.SkillDamageVal(target.id, realDmgVal, gameconst.HitType.Hit))

            elif damageResult.atkType == gameconst.SkillAttackType.ATTACK_DODGE:
                # 被部分闪避
                target.onEffectEvent('onDodge', self.id, target.id, effectEventCtx.EE_DEFAULT_CONTEXT)
                skillDamges.damageInfo.append(
                    combatSkill.SkillDamageVal(target.id, realDmgVal, gameconst.HitType.Miss))

            elif damageResult.atkType == gameconst.SkillAttackType.ATTACK_CRIT:
                # 暴击伤害
                self.onEffectEvent('onFatal', self.id, target.id, effectEventCtx.EE_DEFAULT_CONTEXT)
                if realDmgVal:
                    if hasattr(context, 'isCombo'):
                        skillDamges.damageInfo.append(combatSkill.SkillDamageVal(target.id, realDmgVal, gameconst.HitType.ComboCrit))
                    else:
                        skillDamges.damageInfo.append(combatSkill.SkillDamageVal(target.id, realDmgVal, gameconst.HitType.Crit))

            else:
                LOG_ERR('unknow attack type', target.id, context, damageResult)

            if damageResult.hpSuck:
                # 吸血
                suckHpVal = dmgSrcEnt.modifyHP(damageResult.hpSuck, dmgSrcEnt.id, context.getDmgSourceType(),
                                               context.getDmgSourceId())
                dmgSrcEnt.onEffectEvent('onBloodSuck', dmgSrcEnt.id, target.id,
                                        effectEventCtx.HpEventCtx(damageResult.hpSuck))
                if damageResult.hpSuck:
                    skillDamges.damageInfo.append(
                        combatSkill.SkillDamageVal(dmgSrcEnt.id, damageResult.hpSuck, gameconst.HitType.HPRecover))

            # effect里造成的血量伤害不触发onHit，否则攻击附带xxx效果会死循环
            if context.actionType not in (actionContext.ACTION_BUFF_EFFECT, actionContext.ACTION_EVENT_EFFECT):
                dmgSrcEnt.onEffectEvent('onHit', self.id, target.id,
                                        effectEventCtx.HpEventCtx(realDmgVal, damageResult.dmgType))
                if not target.IsCreation:
                    target.onEffectEvent('onBeat', self.id, target.id, effectEventCtx.HpEventCtx(realDmgVal))

        target.onBeDamaged(dmgSrcEnt.id, realDmgVal, shieldAbsorbVal, context.getDmgSourceType(),
                           context.getDmgSourceId())

        sDmgSrcEnt = context.getSrcEntity()
        _srcIsSelf = True if sDmgSrcEnt and (sDmgSrcEnt.IsAvatar or sDmgSrcEnt.isBot()) else False
        sDmgSrcEnt = sDmgSrcEnt or self
        if sDmgSrcEnt.IsCreation or sDmgSrcEnt.IsSummon or sDmgSrcEnt.IsAvatarMirror:
            sDmgSrcEnt = sDmgSrcEnt.getFirstHost() or sDmgSrcEnt

        if sDmgSrcEnt.IsAvatar or sDmgSrcEnt.isBot():
            recordDmgVal += shieldAbsorbVal
            if recordDmgVal < 0:
                recordDmgVal = 0
            # report to battleFieldDungeon

        target.calcBeHurtStats(dmgSrcEnt, context, damageResult, realDmgVal)
        dmgSrcEnt.calcAtkStats(target, context, realDmgVal)
        dmgSrcEnt.calcHealStats(dmgSrcEnt, context, suckHpVal)

        self.sendDmgMsgs(target, context, damageResult, absorbDamageDetail, realDmgVal)

        # 策划需求返回真实伤害，方便后面做一些吸血之类的操作
        return recordDmgVal

    def sendDmgMsgs(self, target, context, damageResult, absorbDamageDetail, realDmgVal):
        ctx = context or context.parentContext
        self.combatDebugMsg('sendDmgMsg: sourceId:%s, targetId:%s, context:%s, damageResult:%s, absorbDamageDetail:%s, realDmgVal:%s',
                            context.getDmgSourceId(), target.id, ctx, damageResult, absorbDamageDetail, realDmgVal)

    def _healActionBefore(self, target, context, ignoreType=False):
        if not ignoreType:
            if not target or target.isDie() or target.hp <= 0: # 触发事件时，目标的状态可能还没改为Death
                LOG_WARN('target miss ', context)
                return False
            healSrcEnt = context.getSrcEntity()
            if healSrcEnt is None:
                LOG_WARN("_healActionBefore has no src entity")
                return False

            if target and not utils.checkTargetTypeValid("Friend", healSrcEnt, target):
                LOG_WARN("_healActionBefore checkTargetTypeValid error", healSrcEnt.id, target.id)
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
            hateRecord = target.getTempMiscProp(gameconst.EntityPropsEnum.hateRecord, {})
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
        if target.getTempMiscProp(gameconst.EntityPropsEnum.isHpLocked, False):
            return

        healSrcEnt = context.getSrcEntity() or self
        _srcIsSelf = True if healSrcEnt and (healSrcEnt.IsAvatar or healSrcEnt.isBot()) else False
        if healSrcEnt.IsCreation or healSrcEnt.IsSummon or healSrcEnt.IsAvatarMirror:
            healSrcEnt = healSrcEnt.getFirstHost() or healSrcEnt

        oldHp = target.hp
        hpDelta = 0
        if healResult.healVal > 0:
            if target:
                mapData = GPGPD.datas.get(formula.fetchMapId((self.spaceNo)), {})
                ratio = 1

                healResult.healVal = int(healResult.healVal * ratio)
                srcType = context.getDmgSourceType()
                if srcType == gameconst.SourceType.SrcTpBuff and context.parentContext:
                    srcType = context.parentContext.getDmgSourceType()
                hpDelta = target.modifyHP(healResult.healVal, self.id, srcType,
                                          context.getDmgSourceId())
                if hpDelta:
                    if healSrcEnt and healSrcEnt.IsAvatar and context.getDmgSourceType() == gameconst.SourceType.SrcTpSkill:
                        healSrcEnt.setState(gameconst.StateEnum.Fighting)

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

    def calcFrameTime(self, distance, speed):
        _speed = speed / gameconst.gameUpdateHertz
        return max(1, math.ceil(distance / _speed))

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

        _frames = self.calcFrameTime(realDist, speed)
        # 算出真实的每秒速度
        _realSpeed = realDist * gameconst.gameUpdateHertz / _frames

        self.bePushedSpeed = _realSpeed
        if self.hasState(gameconst.StateEnum.bePushed):
            self.cancelTimerCB(self._displaceTimer, gametimer.TIMER_TAG_DISPLACED_BY_SKILL_DONE)
        self.setState(gameconst.StateEnum.bePushed)
        self.controlledBy = None
        self.moveToPoint(pos, _realSpeed, 0, (), False, 0)

        # 不能完全依赖onMoveOver恢复，过程中可能传送或者被别的打断，如果没恢复过来客户端就完全操作不了了
        if realDist <= 0 or _realSpeed <= 0:
            pushTime = timeEx
        else:
            pushTime = realDist / _realSpeed + timeEx
        self._displaceTimer = self.addTimerCB(pushTime, '_displacedBySkillDone', (srcEntityId, oldCollidable),
                                             gametimer.TIMER_TAG_DISPLACED_BY_SKILL_DONE, '_displaceTimer')
        return True

    def _displacedBySkillDone(self, srcEntityId, oldCollidable):

        self.controlledBy = self.base
        self.collidable = oldCollidable
        self.removeState(gameconst.StateEnum.bePushed)

    def getCreationCombatProps(self):
        props = {}

        inheritList = ['baseMinPhysicalAtk', 'adjMinPhysicalAtk', 'adjMinPhysicalAtkAbs', 'baseMaxPhysicalAtk',
                       'adjMaxPhysicalAtk', 'adjMaxPhysicalAtkAbs','baseMinMagicAtk', 'adjMinMagicAtk', 'adjMinMagicAtkAbs',
                       'baseMaxMagicAtk', 'adjMaxMagicAtk', 'adjMaxMagicAtkAbs', 'baseHit', 'adjHit', 'baseFatal',
                       'adjFatal', 'baseMortal', 'adjMortal', 'baseStunEnh',
                       'adjStunEnh', 'baseSilentEnh', 'adjSilentEnh', 'baseKnockEnh', 'adjKnockEnh', 'baseFrozenEnh', 'adjFrozenEnh'
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
        if self.isDestroyed:
            return set()
        if not self.useTargetTypeCacheFlag:
            viewRadius = self.getTargetByViewRadius()
            for e in self.entitiesInRange(viewRadius):
                if e.IsCombatUnit:
                    utils.isEnemy(self, e)
                    utils.isFriend(self, e)
            self.useTargetTypeCacheFlag = True
            self.stopCacheTargetTypeTimeId = self.addTimerCB(30, 'resetTargetTypeCacheFlag', (),
                                                            gametimer.TIMER_TAG_SET_TARGET_TYPE_CACHE_FLAG,
                                                            'stopCacheTargetTypeTimeId')
            if not self.checkTargetTypeTimeId:
                self.checkTargetTypeTimeId = self.pyAddTimer(5, 5, gametimer.CHECK_TARGET_TYPE_TIMER)
        else:
            if self.stopCacheTargetTypeTimeId:
                self.cancelTimerCB(self.stopCacheTargetTypeTimeId, gametimer.TIMER_TAG_SET_TARGET_TYPE_CACHE_FLAG)
                self.stopCacheTargetTypeTimeId = self.addTimerCB(30, 'resetTargetTypeCacheFlag', (),
                                                                gametimer.TIMER_TAG_SET_TARGET_TYPE_CACHE_FLAG,
                                                                'stopCacheTargetTypeTimeId')

        if targetString == "None":
            return self.enemyCacheSet.union(self.notEnemyCacheSet, {self.id})

        elif targetString == "PlayerExTarget":
            if self.IsMonster and self.aiController and self.aiController.hateDict:
                maxHateTargetId, _ = self.aiController.hateDict.getFirstVisibleHateTarget()
            if maxHateTargetId:
                targetSet = set(self.enemyCacheSet)
                targetSet.discard(maxHateTargetId)
                return targetSet
            else:
                return set(self.enemyCacheSet)

        else:
            _set = None
            _value = utils.getFightTargetTypeFromCfgData(targetString)
            if not _value:
                LOG_ERR('getTargetIdsByTargetType: targetString={} not found'.format(targetString))
                return set()

            for _tp in _value[2]:
                if _tp == gameconst.CampType.All:
                    _set = self.enemyCacheSet.union(self.notEnemyCacheSet, {self.id})
                    break

                elif _tp == gameconst.CampType.Enemy:
                    if _set is None:
                        _set = set(self.enemyCacheSet)

                    else:
                        _set = _set.union(self.enemyCacheSet)

                elif _tp == gameconst.CampType.Friend:
                    if _set is None:
                        _set = set(self.friendCacheSet)

                    else:
                        _set = _set.union(self.friendCacheSet)

                elif _tp == gameconst.CampType.Self:
                    if _set is None:
                        _set = {self.id}

                    else:
                        _set = _set.union({self.id})

                elif _tp == gameconst.CampType.EnemyExTarget:
                    if _set is None:
                        _set = set(self.enemyCacheSet)

                    else:
                        _set = _set.union(self.enemyCacheSet)

            if len(_value) > 3 and self.IsAvatar:
                temp_set = set()
                for _tp in _value[3]:
                    if _tp == gameconst.TeamType.TEAM and self.isInTeam():
                        teamList = []
                        for playerBaseVal in self.teamInfo.teamPlayerDic.values():
                            if playerBaseVal.playerBox:
                                teamList.append(playerBaseVal.playerBox.id)
 
                        temp_set = temp_set.union(teamList)
                    elif _tp == gameconst.TeamType.RAID and self.isInRaid():
                        raidList = []
                        for teamVal in self.raidInfo.raidTeamDic.values():
                            for playerInfo in teamVal.teamPlayerDic.values():
                                if playerInfo.playerBox:
                                    raidList.append(playerInfo.playerBox.id)

                        temp_set = temp_set.union(raidList)
                if temp_set and _set:
                    for entId in _set.copy():
                        ent = KBEngine.entities.get(entId)
                        src = utils.getEntityRealEntity(ent)
                        if src.id not in temp_set:
                            _set.discard(entId)

            if _set is None:
                return set()

            else:
                return _set

    def getTargets(self, centerEnt, targetId, targetString, targetRange=20, forceTarget=False, beginSkillPosition=None):
        targetsList = []
        entityIdList = self.getTargetIdsByTargetType(targetString)

        target = KBEngine.entities.get(targetId)

        if forceTarget and target:
            entityIdList.add(targetId)

        for eId in entityIdList:
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

            if not self.checkCombatRangeY(entity):
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

        if not self.checkCombatRangeY(entity):
            return False

        if not utils.checkCachedTargetType(targetString, self, entity, target):
            return False

        return checkFun(entity)

    def getTargetsWithNum(self, centerEnt, targetId, targetString, targetRange, targetNum, checkScopeFun,
                          beginSkillPosition=None):
        targetIdsList = []
        entityIdList = self.getTargetIdsByTargetType(targetString)
        target = KBEngine.entities.get(targetId)

        if targetNum > 1:
            if targetString == "Friend" or targetString == "FriendExGB":
                entityIdList.discard(self.id)
                if self.isTarget(target, self.id, targetString, targetRange, checkScopeFun, beginSkillPosition):
                    targetIdsList.append(self.id)
                if targetId in entityIdList:
                    entityIdList.discard(targetId)
                    if self.isTarget(target, targetId, targetString, targetRange, checkScopeFun, beginSkillPosition):
                        targetIdsList.append(targetId)
            elif targetString == "Enemy" or targetString == "EnemyExTarget":
                if targetId in entityIdList:
                    entityIdList.discard(targetId)
                    if self.isTarget(target, targetId, targetString, targetRange, checkScopeFun, beginSkillPosition):
                        targetIdsList.append(targetId)

        if len(targetIdsList) >= targetNum:
            return targetIdsList

        if KBEngine.getAverageLoad() < 0.6:
            entityIdList = list(entityIdList)
            random.shuffle(entityIdList)

        for eId in entityIdList:
            entity = KBEngine.entities.get(eId)
            if self.isTarget(entity, eId, targetString, targetRange, checkScopeFun, beginSkillPosition):
                targetIdsList.append(eId)
            if len(targetIdsList) >= targetNum:
                break

        return targetIdsList

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
        
        props['createContext'] = actionContext.CreateSummonCtx(summonLv, skillLv)
        
        summonProps and props.update(summonProps)

        summon = KBEngine.createEntity('Summon', self.spaceID, pos, direction, props)
        if not summon:
            LOG_ERR('addSummon Error', id, pos, hostId)
            return False

        if buffId and buffLv:
            summon.addBuff(buffId, buffLv, self.id)

        if skillLv:
            summon.setAllSkillLv(skillLv)

        self.petList.append(summon.id)

    def resetStateOnline(self):
        stList = list(self.stateList)
        removedSt = []
        LOG_IFO('resetStateOnline', stList)
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
                if i == gameconst.StateEnum.Moving and not self.isCleanMove(oldSpaceNo):
                    continue

                val = CSD.datas[i].get('clearTeleport', 0)
                if val == 1:
                    self.removeState(i)
                    LOG_IFO("resetStateTeleport", self.id, i)

    def addSkillEffectCd(self, skillID, cdDelta):
        skill = self.skillDic.doGetSkill(skillID)
        if skill is None:
            LOG_ERR("Spell::addSkillEffectCd(%i):skillID=%i not found" % (self.id, skillID))
            return False

        skill.changeCD(self, cdDelta)
        return True

    def addShield(self, buffId, shieldType, shieldVal, shieldEffects = None):
        shield = buff.ShieldVal(buffId, shieldType, shieldVal, shieldVal, shieldEffects)
        # 减伤盾如果存在直接替换
        if shield.getShieldType() == gameconst.ShieldType.REDUCE_DMG:
            self.shieldDic[buffId] = shield
        else:
            if buffId in self.shieldDic:
                self.shieldDic[buffId].addShieldValue(shield.getShieldValue())
            else:
                self.shieldDic[buffId] = shield

    def removeShield(self, buffId):
        if buffId in self.shieldDic:
            self.shieldDic.pop(buffId)

    def absorbShieldWithDetails(self, nHpModify):
        if nHpModify <= 0:
            return

        remainHp = nHpModify
        rmShelds = []
        details = {}
        # 盾会自动移除
        buffIds = list(self.shieldDic.keys())
        # 先使用生命盾,再用减伤盾
        remainHp = self.doAbsorbDmg(buffIds, gameconst.ShieldType.LIFE, remainHp, details, rmShelds)
        if remainHp > 0:
            remainHp = self.doAbsorbDmg(buffIds, gameconst.ShieldType.REDUCE_DMG, remainHp, details, rmShelds)
        # 移除
        for buffId in rmShelds:
            self.removeBuff(buffId, isFinished=True, removeType=gameconst.RemoveType.RTEnumEndByBeat)

        return remainHp, details

    def doAbsorbDmg(self, buffIds, useShieldType, nHpModify, details, rmShelds):
        remainHp = nHpModify
        for buffId in buffIds:
            shieldVal = self.shieldDic.get(buffId, None)
            if not shieldVal:
                continue
            if shieldVal.getShieldType() != useShieldType:
                continue
            # 盾能尝试吸收的最大伤害
            realShieldVal = remainHp
            # 减伤盾按百分比吸收
            if useShieldType == gameconst.ShieldType.REDUCE_DMG:
                realShieldVal = shieldVal.getShieldReduceDmgRatio() * remainHp

            absorbedVal = shieldVal.doAbsorbDmg(realShieldVal)
            LOG_DBG('absorbShieldWithDetails 1', useShieldType, nHpModify, remainHp, realShieldVal, absorbedVal, shieldVal.shieldValue)
            details[buffId] = absorbedVal
            remainHp -= absorbedVal
            # 盾生命值没了,需要移除
            if shieldVal.getShieldValue() <= 0:
                rmShelds.append(buffId)
                LOG_DBG('absorbShieldWithDetails 2', useShieldType, nHpModify, remainHp, absorbedVal, shieldVal.shieldValue)
            # 吸完了,结束
            if remainHp <= 0:
                LOG_DBG('absorbShieldWithDetails 3', useShieldType, nHpModify, remainHp, absorbedVal, shieldVal.shieldValue)
                break
            # 减伤盾刷新时间
            if useShieldType == gameconst.ShieldType.REDUCE_DMG:
                # 刷新reduce dmg shield duration
                buffSrcKey = self.getBuffSrcKey(buffId, self.id)
                buff = self.getBuffByBuffId(buffId, buffSrcKey)
                if buff:
                    remainTime = buff.getBuffRemainTime()
                    duration = remainTime * (1 - absorbedVal/shieldVal.getShieldMaxValue())
                    self.changeBuffDuration(buffId, duration, self.id)
                    LOG_DBG('absorbShieldWithDetails 4', useShieldType, nHpModify, remainHp, absorbedVal, shieldVal.shieldValue, duration)
        return remainHp
    
    def removeCreation(self, cid):
        if cid in self.creationList:
            self.creationList.remove(cid)

    def destoryAllCreation(self):
        for cid in list(self.creationList):
            creation = KBEngine.entities.get(cid)
            if creation:
                creation.safeDestroy()
            else:
                LOG_ERR('destoryAllCreation: cannot find creation', cid)
        self.creationList.clear()

    def removeSummon(self, summonId):
        if summonId not in self.petList:
            return

        self.petList.remove(summonId)

        if not self.getTempMiscProp(gameconst.EntityPropsEnum.spawnSummonByAI, False):
            return

        _aiData = self.getAIParam()
        if not _aiData:
            return

        _list = self.getTempMiscProp(gameconst.EntityPropsEnum.spawnSummonList, [])
        _list.append({
            'ts': utils.curTS() + _aiData['summonCD'],
            'summonId': _aiData['summonID'],
        })

        self.setTempMiscProp(gameconst.EntityPropsEnum.spawnSummonList, _list)

    def getSpawnSummonList(self):
        return self.getTempMiscProp(gameconst.EntityPropsEnum.spawnSummonList, [])

    def setSpawnSummonList(self, spawnSummonList):
        self.setTempMiscProp(gameconst.EntityPropsEnum.spawnSummonList, spawnSummonList)

    def enableSpawnSummonByAI(self):
        self.setTempMiscProp(gameconst.EntityPropsEnum.spawnSummonByAI, True)

    def initAISpawnSummon(self):
        _aiData = self.getAIParam()
        if not _aiData:
            return

        _list = []
        for i in range(_aiData['summonLimit']):
            _list.append({
                'ts': utils.curTS() + _aiData['summonCD'] * i,
                'summonId': _aiData['summonID'],
            })

        self.setTempMiscProp(gameconst.EntityPropsEnum.spawnSummonList, _list)

    def destroyAllSummon(self):
        if self.petList and self.IsAvatar:
            self.changeMorphState(None, None, 3)

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

    def getOwnedSummons(self, sid=0):
        ret = []
        for s in self.petList:
            ent = KBEngine.entities.get(s)
            if ent and (not sid or ent.creepBaseId == sid):
                ret.append(ent)
        return ret

    def endChongfeng(self, skillVal, targetId, skillArgs):
        self.removeState(gameconst.StateEnum.Shifting)

    def endLunge(self, skillVal, targetId, skillArgs):
        self.removeState(gameconst.StateEnum.Shifting)

    def endDodge(self, skillVal, targetId, skillArgs):
        self.removeState(gameconst.StateEnum.Dodging)

    def endMovement(self):
        if self.getNeedUpdateWitnessPosDir() == 0:
            self.cancelController('Movement')

    def endUpdateWitnessPosDir(self):
        LOG_DBG("endUpdateWitnessPosDir")
        self.setNeedUpdateWitnessPosDir(1)
        if self.IsAvatar:
            self.leaveShiftOrDodgeState()

    def resetShiftOrDodgeTimer(self):
        self.popTempMiscProp(gameconst.EntityPropsEnum.shiftOrDodgeTimer, 0)

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
            self.removeState(gameconst.StateEnum.Moving)

    def onChongfengMoveOver(self, isSucc):
        self.setNeedUpdateWitnessPosDir(1)
        self.topSpeed = gameconst.TopSpeedType.NormalTopSpeed
        # shiftOrDodgeTimer = self.popTempMiscProp(gameconst.EntityPropsEnum.shiftOrDodgeTimer, 0)
        # if shiftOrDodgeTimer > 0:
        #     self.cancelTimerCB(shiftOrDodgeTimer, gametimer.TIMER_TAG_SKILL_CHANGE_POS)
        chongfengData = self.popTempMiscProp(gameconst.EntityPropsEnum.chongfengData)
        if not chongfengData:
            LOG_ERR('chongfeng err: move failed', isSucc)
            self.endChongfeng(None, 0, [])
            return

        context, calcDelay = chongfengData

        skill = self._getSkillByActionContext(context)

        if not skill:
            LOG_ERR('onChongfengMoveOver: cannot get skill', skill.skillId, context)
            self.endChongfeng(None, 0, [])
            return

        targetId = context.useTargetId
        self.endChongfeng(skill, targetId, context.skillArgs)
        if skill.checkUseSkill(self, targetId,
                               ignoreReasons=gameconst.UseSkillCheck.USC_DELAY_CHECK_IGNORES) != gameconst.UseSkillCheck.USC_ENUM_CHEKC_OK:
            skill.useSkillDone(self, targetId, context.skillArgs, False)
            return

        if context.actionProgress == gameconst.ActionProgressEnum.startActionDoing:
            context.actionProgress = gameconst.ActionProgressEnum.startActionDone
            if isSucc:
                skillId, skillLv = skill.getNotifyClientSkillId()
                skillArgsExtra = [skill.getRange(self, skillId, skillLv), skill.getEffectRange(self, skillId, skillLv)]
                self.allClients.onUseSkill(True, skillId, targetId, context.skillArgs,
                                           context.effectedEntIds, skillArgsExtra)
            self._doUseSkill(skill, targetId, context.skillArgs, context, calcDelay)
        elif context.actionProgress == gameconst.ActionProgressEnum.actionDoing and context.isLastActionStage:
            if skill.hasTempData(gameconst.SkillTempDataKey.DURATION):
                duration = skill.popTempData(gameconst.SkillTempDataKey.DURATION)
            else:
                duration = 0
            remainTime = skill.getSkillTime(skill.skillId) - calcDelay - duration
            context.actionProgress = gameconst.ActionProgressEnum.actionDone
            if remainTime <= 0:
                skill.useSkillDone(self, targetId, context.skillArgs)
            else:
                skill._cancelTempTimer(self, gameconst.SkillTempDataKey.SKILL_DONE_TIMER, gametimer.TIMER_TAG_SKILL_DONE)
                tid = self.addTimerCB(remainTime, '_onSkillCallback',
                                     (skill, 'useSkillDone', (targetId, context.skillArgs, True, False, True)),
                                     gametimer.TIMER_TAG_SKILL_DONE)
                skill.setTimerTempData(self, gameconst.SkillTempDataKey.SKILL_DONE_TIMER, tid)

    def onLungeMoveOver(self, isSucc):
        LOG_DBG("###onLungeMoveOver")
        self.setNeedUpdateWitnessPosDir(1)
        self.topSpeed = gameconst.TopSpeedType.NormalTopSpeed
        # shiftOrDodgeTimer = self.popTempMiscProp(gameconst.EntityPropsEnum.shiftOrDodgeTimer, 0)
        # if shiftOrDodgeTimer > 0:
        #     self.cancelTimerCB(shiftOrDodgeTimer, gametimer.TIMER_TAG_SKILL_CHANGE_POS)
        lungeData = self.popTempMiscProp(gameconst.EntityPropsEnum.lungeSkillData)
        if not lungeData:
            LOG_ERR('lunge err: move failed', isSucc)
            self.endLunge(None, 0, [])
            return

        context, calcDelay = lungeData

        skill = self._getSkillByActionContext(context)

        if not skill:
            LOG_ERR('onLungeMoveOver: cannot get skill', skill.skillId, context)
            self.endLunge(None, 0, [])
            return

        targetId = context.useTargetId
        self.endLunge(skill, targetId, context.skillArgs)
        if skill.checkUseSkill(self, targetId,
                               ignoreReasons=gameconst.UseSkillCheck.USC_DELAY_CHECK_IGNORES) != gameconst.UseSkillCheck.USC_ENUM_CHEKC_OK:
            skill.useSkillDone(self, targetId, context.skillArgs, False)
            return

        if context.actionProgress == gameconst.ActionProgressEnum.startActionDoing:
            context.actionProgress = gameconst.ActionProgressEnum.startActionDone
            if isSucc:
                skillId, skillLv = skill.getNotifyClientSkillId()
                skillArgsExtra = [skill.getRange(self, skillId, skillLv), skill.getEffectRange(self, skillId, skillLv)]
                self.allClients.onUseSkill(True, skillId, targetId, context.skillArgs,
                                           context.effectedEntIds, skillArgsExtra)
            self._doUseSkill(skill, targetId, context.skillArgs, context, calcDelay)
        elif context.actionProgress == gameconst.ActionProgressEnum.actionDoing and context.isLastActionStage:
            if skill.hasTempData(gameconst.SkillTempDataKey.DURATION):
                duration = skill.popTempData(gameconst.SkillTempDataKey.DURATION)
            else:
                duration = 0
            remainTime = skill.getSkillTime(skill.skillId) - calcDelay - duration
            context.actionProgress = gameconst.ActionProgressEnum.actionDone
            if remainTime <= 0:
                skill.useSkillDone(self, targetId, context.skillArgs)
            else:
                tid = self.addTimerCB(remainTime, '_onSkillCallback',
                                     (skill, 'useSkillDone', (targetId, context.skillArgs, True, False, True)),
                                     gametimer.TIMER_TAG_SKILL_DONE)
                skill.setTimerTempData(self, gameconst.SkillTempDataKey.SKILL_DONE_TIMER, tid)

    def onDodgeMoveOver(self, isSucc):
        self.setNeedUpdateWitnessPosDir(1)
        self.topSpeed = gameconst.TopSpeedType.NormalTopSpeed
        # shiftOrDodgeTimer = self.popTempMiscProp(gameconst.EntityPropsEnum.shiftOrDodgeTimer, 0)
        # if shiftOrDodgeTimer > 0:
        #     self.cancelTimerCB(shiftOrDodgeTimer, gametimer.TIMER_TAG_SKILL_CHANGE_POS)
        dodgeData = self.popTempMiscProp(gameconst.EntityPropsEnum.dodgeSkillData)
        if not dodgeData:
            LOG_ERR('dodge err: move failed', isSucc)
            self.endDodge(None, 0, [])
            return

        context, calcDelay = dodgeData

        skill = self._getSkillByActionContext(context)

        if not skill:
            LOG_ERR('onDodgeMoveOver: cannot get skill', skill.skillId, context)
            self.endDodge(None, 0, [])
            return

        targetId = context.useTargetId
        self.endDodge(skill, 0, context.skillArgs)
        if skill.checkUseSkill(self, targetId,
                               ignoreReasons=gameconst.UseSkillCheck.USC_DELAY_CHECK_IGNORES) != gameconst.UseSkillCheck.USC_ENUM_CHEKC_OK:
            skill.useSkillDone(self, targetId, context.skillArgs, False)
            return

        if context.actionProgress == gameconst.ActionProgressEnum.startActionDoing:
            context.actionProgress = gameconst.ActionProgressEnum.startActionDone
            if isSucc:
                skillId, skillLv = skill.getNotifyClientSkillId()
                skillArgsExtra = [skill.getRange(self, skillId, skillLv), skill.getEffectRange(self, skillId, skillLv)]
                self.allClients.onUseSkill(True, skillId, targetId, context.skillArgs,
                                           context.effectedEntIds, skillArgsExtra)
            self._doUseSkill(skill, targetId, context.skillArgs, context, calcDelay)
        elif context.actionProgress == gameconst.ActionProgressEnum.actionDoing and context.isLastActionStage:
            if skill.hasTempData(gameconst.SkillTempDataKey.DURATION):
                duration = skill.popTempData(gameconst.SkillTempDataKey.DURATION)
            else:
                duration = 0
            remainTime = skill.getSkillTime(skill.skillId) - calcDelay - duration
            context.actionProgress = gameconst.ActionProgressEnum.actionDone
            if remainTime <= 0:
                skill.useSkillDone(self, targetId, context.skillArgs)
            else:
                tid = self.addTimerCB(remainTime, '_onSkillCallback',
                                     (skill, 'useSkillDone', (targetId, context.skillArgs, True, False, True)),
                                     gametimer.TIMER_TAG_SKILL_DONE)
                skill.setTimerTempData(self, gameconst.SkillTempDataKey.SKILL_DONE_TIMER, tid)

    def onEnterTrap(self, entity, rangeXZ, rangeY, controllerId, userArg):
        if hasattr(super(), 'onEnterTrap'):
            super().onEnterTrap(entity, rangeXZ, rangeY, controllerId, userArg)
        if not entity or entity.isDestroyed:
            return

        if userArg == gameconst.AURA_TRAP:
            if not entity.IsCombatUnit:
                return

            self.aureoleDic.addCtrlInPending(controllerId)

            _aureole = self.aureoleDic.getByCtrlId(controllerId)
            _entityId = entity.id

            if not _aureole:
                return

            if not utils.checkTargetTypeValid(_aureole.effectTarget, self, entity):
                return

            _aureole.addAureoleTarget(self, _entityId)

    def onLeaveTrap(self, entity, rangeXZ, rangeY, controllerId, userArg):
        if hasattr(super(), 'onLeaveTrap'):
            super().onLeaveTrap(entity, rangeXZ, rangeY, controllerId, userArg)
        if not entity:
            return

        if userArg == gameconst.AURA_TRAP:
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
            if _aureole and utils.checkTargetTypeValid(_aureole.effectTarget, self, entity):
                _aureole.addAureoleTarget(self, _entityId)

    def onLeaveWholeAureole(self, entity):
        if not entity:
            return

        for aureoleId in self.aureoleDic._wholeAreaAureoleList:
            _aureole = self.aureoleDic.get(aureoleId)
            _entityId = entity.id
            if _aureole and utils.checkTargetTypeValid(_aureole.effectTarget, self, entity):
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
            LOG_ERR('unexpected anti control context', context)
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
                return
            skillDamges.damageInfo.append(combatSkill.SkillDamageVal(target.id, 0, hitType))

    def dispelBuffByTag(self, target, context, tag):
        buffIdList = []
        for buffId in target.buffDic.keys():
            buff = target.getBuffByBuffId(buffId)
            if buff and buff.hasBuffTag(tag):
                buffIdList.append(buffId)

        for buffId in buffIdList:
            target.removeBuff(buffId)

    def isImmuneToControl(self):
        return self.baseStateRate == -1

    def setTargetHateRecord(self, targetId):
        target = KBEngine.entities.get(targetId)
        target and target.setHateRecord(self.id)

    def unsetTargetHateRecord(self, targetId):
        target = KBEngine.entities.get(targetId)
        target and target.unsetHateRecord(self.id)

    def clearHateRecord(self, removeFightingState=True):
        hateRecord = self.getTempMiscProp(gameconst.EntityPropsEnum.hateRecord)
        if hateRecord:
            self.popTempMiscProp(gameconst.EntityPropsEnum.hateRecord)
        # if removeFightingState and self.IsAvatar and not self.isDie():
        #     self.removeState(gameconst.StateEnum.Fighting)

    def setHateRecord(self, targetId):
        if not self.hasTempMiscProp(gameconst.EntityPropsEnum.hateRecord):
            self.setTempMiscProp(gameconst.EntityPropsEnum.hateRecord, {})
        hateRecord = self.getTempMiscProp(gameconst.EntityPropsEnum.hateRecord)
        hateRecord[targetId] = int(time.time())
        # self.IsAvatar and not self.isDie() and self.setState(gameconst.StateEnum.Fighting)

    def unsetHateRecord(self, targetId):
        hateRecord = self.getTempMiscProp(gameconst.EntityPropsEnum.hateRecord)
        if not hateRecord:
            return
        if targetId in hateRecord:
            hateRecord.pop(targetId)

        if not hateRecord:
            self.clearHateRecord()

    def unsetAllHateRecord(self, unsetReason):
        hateRecord = self.getTempMiscProp(gameconst.EntityPropsEnum.hateRecord)
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
        self.removeState(gameconst.StateEnum.Fighting)

    def checkRemoveFightingState(self):
        hateRecord = self.getTempMiscProp(gameconst.EntityPropsEnum.hateRecord)
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
        if not self.checkCombatRangeY(target):
            return False
        # return not target.hasState(gameconst.StateEnum.Invisible)
        return True

    # 为了让日志更可读以及减少字符拼接开销，必须以 'skillId:%s', skillId 这种形式传入
    def combatDebugMsg(self, *args):
        if gameconfig.enableCombatDebugLog():
            if len(args) <= 1:
                msg = args[0]
            else:
                msg = args[0] % args[1:]
            msg = '[%s][combatDebug] ' % getattr(self, 'name', '') + msg
            LOG_IFO(msg)

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
        self.modifyHP(newHp, self.id, gameconst.SourceType.SrcTpDefault, self.id)
        if pos:
            self.telToPos(pos, toDir)
        self._trapInViews()

        if self.IsAvatar:
            spaceMgr = self.spaceMgr
            spaceMgr and spaceMgr.onPlayerRelive(self.base, self.gbId)
            self.setState(CCDD.datas.relive)
            self.addTimerCB(CONST.datas['reliveTime']['value'], 'removeState', (CCDD.datas.relive,), gametimer.TIMER_TAG_REMOVE_RELIVE_STATE)

        self.popTempMiscProp(gameconst.EntityPropsEnum.isLightningArea)

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

        if skillDamges.sourceType == gameconst.SourceType.SrcTpSkill:
            targetIdList = [sVal.targetId for sVal in skillDamges.damageInfo if
                            not gameconst.HitType.checkInClientIgnoreList(sVal.hitType)]
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

    def resetAllTargetTypeCache(self, updateImmediately=True):
        if self.IsAvatar:
            self.guildRelationVersion = gameglobal.guildRelationVersion

        cacheIds = self.enemyCacheSet.union(self.notEnemyCacheSet, self.friendCacheSet, self.notFriendCacheSet)
        self.enemyCacheSet.clear()
        self.notEnemyCacheSet.clear()
        self.friendCacheSet.clear()
        self.notFriendCacheSet.clear()

        if updateImmediately:
            for eId in cacheIds:
                target = KBEngine.entities.get(eId)
                if not target:
                    LOG_WARN("resetAllTargetTypeCache target is None")
                    continue

                utils.isEnemy(self, target)
                utils.isFriend(self, target)

            for eId in list(self.cacheSelfSet):
                target = KBEngine.entities.get(eId)
                if not target:
                    LOG_WARN("resetAllTargetTypeCache cacheSelfSet target is None", eId)
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
                LOG_WARN("checkCacheTargetType  error1", eId)
                self.enemyCacheSet.remove(eId)
            elif not utils._isEnemy(self, target):
                LOG_WARN("checkCacheTargetType enemy cache error", eId)
                needRefreshList.append(target)

        for eId in list(self.notEnemyCacheSet):
            target = KBEngine.entities.get(eId)
            if not target:
                LOG_WARN("checkCacheTargetType  error2", eId)
                self.notEnemyCacheSet.remove(eId)
            elif utils._isEnemy(self, target):
                LOG_WARN("checkCacheTargetType not enemy cache error", eId)
                needRefreshList.append(target)

        for eId in list(self.friendCacheSet):
            target = KBEngine.entities.get(eId)
            if not target:
                LOG_WARN("checkCacheTargetType  error3", eId)
                self.friendCacheSet.remove(eId)
            elif not utils._isFriend(self, target):
                LOG_WARN("checkCacheTargetType friend cache error", eId)
                needRefreshList.append(target)

        for eId in list(self.notFriendCacheSet):
            target = KBEngine.entities.get(eId)
            if not target:
                LOG_WARN("checkCacheTargetType  error4", eId)
                self.notFriendCacheSet.remove(eId)
            elif utils._isFriend(self, target):
                LOG_WARN("checkCacheTargetType not friend cache error", eId)
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
                LOG_WARN("clearAllTargetTypeCache target is None in allCacheSet", eId)
                continue
            target.cacheSelfSet.remove(self.id)

        if bClearOthersCache:
            for eId in list(self.cacheSelfSet):
                target = KBEngine.entities.get(eId)
                if not target:
                    LOG_WARN("clearAllTargetTypeCache target is None in cacheSelfSet", eId)
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

    def tagDispelAll(self, tag):
        self.removeBuffByTag(tag)

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

        boxRadius = 0
        for weight, collectionId in collectionIdProb:
            boxRadius = max(boxRadius, NPD.datas.get(collectionId, {}).get('chestRadius', 0))
        createNum = utils.weightChoices(numList, numWeightList)[0][0]
        if createNum == 1:
            posList = [self.position]
        else:
            posList = self.getRandomPositionByBoxRadius(self.position, radius, boxRadius, createNum)

        for i in range(createNum):
            collectionIdList = []
            collectionIdWeightList = []
            for weight, collectionId in collectionIdProb:
                collectionIdList.append(collectionId)
                collectionIdWeightList.append(weight)

            collectionId = utils.weightChoices(collectionIdList, collectionIdWeightList)[0][0]
            _pos = posList[i] if i < len(posList) else self.position

            props = {
                'collectionId': collectionId,
                'spaceNo': self.spaceNo,
                'position': _pos,
                'direction': self.direction,
                'disappearTime': utils.curTS() + disappearTime
            }
            if self.spaceMgr:
                props['spaceMgrId'] = self.spaceMgr.id
                props['spaceMgrBox'] = self.spaceMgr.base

            KBEngine.createEntity('Collection', self.spaceID, _pos, self.direction, props)

    def deathCreateCollectionByList(self, radius, collectionIdProb, disappearTime):
        createNum = 0
        boxRadius = 0
        for (num, collectionId) in collectionIdProb:
            createNum += num
            boxRadius = max(boxRadius, NPD.datas.get(collectionId, {}).get('chestRadius', 0))
            
        posList = self.getRandomPositionByBoxRadius(self.position, radius, boxRadius, createNum)

        idx = 0
        for (num, collectionId) in collectionIdProb:
            for i in range(num):
                _pos = posList[idx] if i < len(posList) else self.position
                idx += 1
                props = {
                    'collectionId': collectionId,
                    'spaceNo': self.spaceNo,
                    'position': _pos,
                    'direction': self.direction,
                    'disappearTime': utils.curTS() + disappearTime
                }
                if self.spaceMgr:
                    props['spaceMgrId'] = self.spaceMgr.id
                    props['spaceMgrBox'] = self.spaceMgr.base

                KBEngine.createEntity('Collection', self.spaceID, _pos, self.direction, props)

    def breakSkillByState(self):
        usingSkills = self.getTempMiscProp(gameconst.EntityPropsEnum.currentUseSkill, default={})
        for sid in list(usingSkills.keys()):
            if sid not in usingSkills:
                continue
            
            sVal, tid = usingSkills[sid]
            sVal.useSkillDone(self, 0, [], isSucc=False, doRemoveState=True, forceResetSkill=True)

    def getAvatar(self):
        _host = utils.getHostEntity(self)
        if _host and _host.IsAvatar:
            return _host
        return None

    def updateEffectEventCDInfo(self, effectId, triggerTime):
        self.effectEventCDInfo[effectId] = triggerTime
        #LOG_DBG('update EventEffect', effectId, triggerTime, utils.getNowTimeStr(triggerTime))

    def getEffectEventCDInfo(self, effectId):
        triggerTime = self.effectEventCDInfo.get(effectId, 0)
        #LOG_DBG('get EventEffect', effectId, triggerTime, utils.getNowTimeStr(triggerTime))
        return triggerTime

    def removeEffectEventCDInfo(self, effectId):
        triggerTime = self.effectEventCDInfo.pop(effectId, None)
        #LOG_DBG('remove EventEffect', effectId, triggerTime)

    def checkEffectEventCDInfoExpired(self):
        now = time.time()
        effectIdList = list(self.effectEventCDInfo.keys())
        LOG_DBG('check EventEffect', self.effectEventCDInfo)
        for effectId in effectIdList:
            if self.getEffectEventCDInfo(effectId) <= now:
                self.removeEffectEventCDInfo(effectId)
