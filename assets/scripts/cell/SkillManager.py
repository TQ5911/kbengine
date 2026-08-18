# -*- coding: utf-8 -*-
import KBEngine
import gameconst
from KBEDebug import *
import skill_skill as SSD
import conflict_conflict
import time
import buff_buff
import combatSkill
import random
import buff
import formula
import collections
import math, Math, sMath
import utils
import actionContext
import effectEventCtx
import iEventActions
import gameengine
import iCell
import gameclass
import gametimer
import gamemove
import gameconfig
import dataUtils
import gamedecorator
import iFlowController
import gameglobal
import fightProp_define as FP_DD
import message_Message as M_MD
import conflict_status as C_SD
import conflict_conflict_def as C_C_DD
import creation_creation as CRD
import buff_buff as B_BD
import const_const as CONST
import conflict_status_def as CCDD
import gamePlay_gamePlay as GPGPD
import gamePlay_set as GP_SD
import aureola_aureola as AAD
import aureole
import NPC_Pick as NPD
import skillRelevant_summonUnlock as SRSU
import combatSkill


class AureoleMixin(object):
    def addTAureoleTrap(self, auraId):
        _aureoleInfo = self.auraDic.get(auraId)

        if not _aureoleInfo:
            return

        _aureoleInfo.addAureoleTrap(self)

    def isWholeAreaAura(self, auraId):
        return AAD.datas[auraId].get('radium') == -1 and self.spaceMgr 

    def removeAureolaById(self, auraId):
        self.auraDic.removeAureola(self, auraId)

    def clearAura(self):
        for _auraId in list(self.auraDic.keys()):
            self.removeAureolaById(_auraId)

    def disableAura(self, auraId=0):
        if auraId == 0:
            for auraId in list(self.auraDic.keys()):
                self.auraDic.doDisableAura(self, auraId)
        else:
            self.auraDic.doDisableAura(self, auraId)

    def addAureoleEffect(self, srcEntId, auraId, aureoleLv):
        curar = self.aureoleFormOtherDic.get(auraId, None)
        if curar:
            if curar.level >= aureoleLv:
                return False
            else:
                self.removeAureoleEffect(auraId, 0)

        startAction = AAD.datas[auraId].get('action')
        _srcEnt = KBEngine.entities.get(srcEntId)
        if startAction and _srcEnt:
            _ret = self.doCombatActions(startAction, _srcEnt, self, srcEntId,
                                       lambda result: actionContext.AureoleCtx(srcEntId, auraId, aureoleLv, result))
            if _ret == False:
                LOG_ERR('addAureoleEffect faileed', srcEntId, auraId)
                return False

        srcHostEntId = _srcEnt.getHost().id if _srcEnt.getHost() is not None else None
        self.aureoleFormOtherDic.applyAureole(auraId, aureoleLv, srcEntId, srcHostEntId)

        clientAr = aureole.ClientAureoleVal(auraId, aureoleLv)
        self.allClients.onAddAureoleFromOthers(clientAr.getClientData())
        return True

    # 作用目标移除光环效果
    def removeAureoleEffect(self, auraId, srcEntId):
        curar = self.aureoleFormOtherDic.get(auraId, None)
        if curar and (not srcEntId or curar.srcEntId == srcEntId):
            self.aureoleFormOtherDic.pop(auraId)
            # 移除可能在_srcEnt的onDestroy里移除，这个时候虽然_srcEnt还在，但是在KBEngine.entities里已经没有了
            # 所以这里执行action的主体先用self吧
            endAction = AAD.datas[auraId].get('endActionToEffectObject')
            if endAction:
                _srcEntId = curar.srcHostEntId if curar.srcHostEntId is not None else curar.srcEntId
                self.doCombatActions(endAction, self, self, curar.srcEntId,
                                     lambda r: actionContext.AureoleCtx(_srcEntId, auraId, curar.level, r))

            if self.isReal():
                self.allClients.onRemoveAureoleFromOthers(auraId)

        if self.hasAureola(auraId) and (srcEntId and srcEntId != self.id):
            aVal = self.auraDic[auraId]
            self.onEnterTrap(self, 0, 0, aVal.aureoleTrapId, gameconst.AURA_TRAP)

    def hasAureola(self, auraId):
        return auraId in self.auraDic

    def isValidAureoleTarget(self, auraId, target):
        if not self.hasAureola(auraId):
            return False

        _aura = self.auraDic[auraId]
        if not utils.checkTargetTypeValid(_aura.effectTarget, self, target):
            return False

        return True

    # 光环主人移除目标
    def removeAureoleTarget(self, auraId, targetId):
        _aura = self.auraDic[auraId]
        _aura.onLeaveAureoleRnage(self, targetId)


handlerMap = {}


def propChangedHandler(changedBySrc, propName):
    def _func(func, *args):
        if type(propName) == str:
            _propNames = (propName,)
        else:
            _propNames = propName

        if type(changedBySrc) == int:
            srcList = (changedBySrc,)
        else:
            srcList = changedBySrc

        for name in _propNames:
            handlerMap.setdefault(name, {})
            for src in srcList:
                handlerMap[name][src] = func
        return func

    return _func


class SkillManager(iCell.ICell, iEventActions.IEventActions, iFlowController.IFlowController,
                   AureoleMixin):
    def __init__(self):
        self.shieldDic = buff.Shields()

        _hpPercent = self.hp / self.fullHp if self.fullHp else 1
        _mpPercent = self.mp / self.fullMp if self.fullMp else 1
        self.doInitBaseProperties()
        self.initEntityCombatProps(_hpPercent, _mpPercent)
        self.checkEffectEventCDInfoExpired()
        self.isWitnessComplete = gameconst.WitnessTypeEnum.WITNESS_ENUM_ALL
        self.stateList = formula.getInt64ListOnIndexes(self.getStateBitVector())

        # 缓存下是否矿战场景
        if formula.inMineWarScene(self.spaceNo):
            self.cellFlags = utils.bset(self.cellFlags, gameconst.CELL_FLAGS_IS_MINE_WAR_SPACE)

    def canAttackable(self, src):
        return utils.isJoinCombat(self, src)

    def doInitBaseProperties(self):
        pass

    def _preSafeDestory(self):
        super(SkillManager, self)._preSafeDestory()
        self.destroyAllSummon()
        self.disableAura()

    def _onDestroy(self):
        self.clearAura()
        self.doClearAllTargetTypeCache(True)

    def overwriteProps(self):
        """初始化时覆盖一些属性, 需要再子类中显示调用, 一般在放在__init__完成后"""

    def onInitPropsCompleted(self):
        return

    def initEntityCombatProps(self, hpPercent, mpPercent):
        checkedPropSet = set()
        for _propName in FP_DD.datas.keys():
            if not hasattr(self, _propName):
                continue

            # 虽然没设置属性，但上线时也需要重新计算下
            # 因为有些属性时存数据库的，所以要计算它影响的属性
            self.checkOnUpdateProp(_propName, gameconst.SourceType.SrcTpInit, checkedPropSet)

        # 上面不会重算hp,mp这种存数据库的属性，这里重设下处理数值被离线修改的情况
        self.hp = math.ceil(self.fullHp * hpPercent)
        self.mp = math.ceil(self.fullMp * mpPercent)

        LOG_DBG("initEntityCombatProps", self.hp ,self.mp, self.fullHp, self.fullMp)

    def checkOnUpdateProp(self, propName, src, checkedPropSet=None):
        _propData = FP_DD.datas.get(propName)
        if not _propData:
            return

        _changeAffactProps = _propData.get('changeAffactProp')
        if not _changeAffactProps:
            return

        _affectProps = _changeAffactProps.split(';')
        if self.IsAvatar:
            formulaStr = 'formulaPlayer'
        else:
            formulaStr = 'formulaMonster'

        propFormulaFunc = _propData.get(formulaStr)
        isInit = (src == gameconst.SourceType.SrcTpInit)
        for _affectedProp in _affectProps:
            # hp,mp等存数据库的属性，在初始化时不参与计算，因为这里propName对应的属性可能不是最终值，会把这类属性算成错的
            if (isInit) and _affectedProp in ('hp', 'mp'):
                continue

            if isInit and not propFormulaFunc and checkedPropSet and _affectedProp in checkedPropSet:
                continue

            elif not _affectedProp or not hasattr(self, _affectedProp):
                continue

            _affectedPropData = FP_DD.datas.get(_affectedProp)
            if not _affectedPropData:
                continue

            _func = _affectedPropData.get(formulaStr)
            if not _func:
                continue

            try:
                _value = _func(self)
                if _value != gameconst.scriptNone:
                    self.setProp(_affectedProp, _value, src)
                    if checkedPropSet is not None:
                        checkedPropSet.add(_affectedProp)
            except Exception as e:
                LOG_ERR('Error: failed to call _func in checkOnUpdateProp:  %s, reason:%s.' % (_affectedProp, repr(e)))

    # FOR DEBUG ONLY. called if KBEngine.publish()==0
    def onScriptSetAttr(self, keyName, value, isInit):
        if keyName not in FP_DD.datas:
            return

        if keyName in ('hp', 'mp'):
            return

        if isInit:
            return
        if keyName == 'speed':
            if self.hasTempMiscProp(gameconst.EntityPropsEnum.idleChangeSpeed):
                return

        if self.IsAvatar:
            _formulaStr = 'formulaPlayer'
        else:
            _formulaStr = 'formulaMonster'

        if FP_DD.datas[keyName][_formulaStr]:
            _nDepth = 10
            _f = sys._getframe()
            lastFrame = None
            for _ in range(_nDepth):
                if not _f:
                    break

                if _f.f_code.co_name in (
                        '__init__', 'checkOnUpdateProp', 'doInitBaseProperties', 'inheritProps'):
                    return

                lastFrame = _f
                _f = _f.f_back

            if lastFrame.f_code.co_name in ('onScriptSetAttr',):
                return

            gameengine.panicStack('cannot set %s directly to %s' % (keyName, value))

    def addProp(self, propName, delta, src=gameconst.SourceType.SrcTpDefault):
        if KBEngine.publish() == 0:
            _curVal = self.getProp(propName)
            if type(_curVal) is int and type(_curVal) != type(delta):
                gameengine.panicStack('addProp type error', propName, _curVal, delta)

        _oldVal = getattr(self, propName)
        _newVal = type(_oldVal)(_oldVal + delta)
        self.setProp(propName, _newVal, src)

        for changedSrc in (src, gameconst.SourceType.SrcTpAll):
            if propName in handlerMap and changedSrc in handlerMap[propName]:
                handlerMap[propName][changedSrc](self, src, _oldVal)

    def setProp(self, propName, value, src=gameconst.SourceType.SrcTpDefault):
        if KBEngine.publish() == 0:
            _curVal = self.getProp(propName)
            if type(_curVal) is int and type(_curVal) != type(value):
                gameengine.panicStack('setProp type error', propName, _curVal, value)
            # 初始化的日志太多了
            if src != gameconst.SourceType.SrcTpInit:
                self.debugCombatMsg('setProp: propName:%s, oldValue:%s, value:%s, sourceType:%s', propName, _curVal, value, src)
        # hasattr判断先拿掉，好像有点慢
        _oldVal = getattr(self, propName)
        _func = type(_oldVal)
        setattr(self, propName, type(_oldVal)(value))

        if _func is int:
            if _oldVal == int(value):
                return
        elif _func is float:
            if math.isclose(_oldVal, float(value)):
                return

        self.checkOnUpdateProp(propName, src)

        for _changedSrc in (src, gameconst.SourceType.SrcTpAll):
            if propName in handlerMap and _changedSrc in handlerMap[propName]:
                handlerMap[propName][_changedSrc](self, src, _oldVal)

    def getProp(self, propName):
        return getattr(self, propName)

    def getFightProps(self):
        _propValDic = {}
        for _propName, _ in FP_DD.datas.items():
            _val = getattr(self, _propName, None)
            if _val is None:
                continue
            _propValDic[_propName] = _val
        return _propValDic

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
        _propsByEffect = self.getTempMiscProp(gameconst.EntityPropsEnum.effectSetProps)
        if _propsByEffect and propName in _propsByEffect:
            LOG_ERR('onEffectAddProp error: cannot modify prop set by another effect')
            return

        _curVal = self.getProp(propName)
        delta = type(_curVal)(delta)

        _newVal = _curVal + delta
        self.setProp(propName, _newVal, gameconst.SourceType.SrcTpBuff)

    def onEffectSetProp(self, propName, newVal, callerInfo, effectId, effectIdx):
        if not self.hasTempMiscProp(gameconst.EntityPropsEnum.effectSetProps):
            self.setTempMiscProp(gameconst.EntityPropsEnum.effectSetProps, {})

        _propsByEffect = self.getTempMiscProp(gameconst.EntityPropsEnum.effectSetProps)
        _newCallerKey = callerInfo.getCallerKey(effectId, effectIdx)
        if propName in _propsByEffect:
            oldVal, setCnt, _ = _propsByEffect[propName]
        else:
            oldVal = self.getProp(propName)
            setCnt = 0

        _propsByEffect[propName] = (oldVal, setCnt + 1, _newCallerKey)
        self.setProp(propName, newVal, callerInfo.getCallerSrc())

    def onEffectUnsetProp(self, propName, callerInfo, effectId, effectIdx):
        _propsByEffect = self.getTempMiscProp(gameconst.EntityPropsEnum.effectSetProps)
        callerSrcKey = callerInfo.getCallerKey(effectId, effectIdx)
        if propName in _propsByEffect:
            oldVal, setCnt, curCallerKey = _propsByEffect[propName]

            setCnt -= 1
            if setCnt <= 0:
                _propsByEffect.pop(propName)
                self.setProp(propName, oldVal, callerInfo.getCallerSrc())
            else:
                _propsByEffect[propName] = (oldVal, setCnt, curCallerKey)

            if not _propsByEffect:
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

        if skillId in self.skillDic:
            return

        skill = self.skillDic.doAddSkill(self, skillId, skillLv, tNextCast=tNextCast)
        self.onEffectEventCall('onAddSkill', self.id, self.id, effectEventCtx.AddSkillEventCtx(skillId))
        return skill

    def setAllSkillLv(self, skillLv):
        for _sVal in self.skillDic.values():
            _sVal.setSkillLevel(skillLv)

    def getSkillByCategory(self, skillId, level):
        _category = SSD.datas[skillId].get('category', 0)
        if _category in (
                gameconst.SkillCategory.CATEGORY_CAST_SKILL_WITH_ACTION, gameconst.SkillCategory.CATEGORY_CAST_SKILL_WITHOUT_ACTION):
            skill = combatSkill.fetchSkillClass(skillId)(skillId, level)
        elif _category == gameconst.SkillCategory.CATEGORY_GENERAL_SKILL:
            skill = self.skillDic.doGetSkill(skillId)
        else:
            skill = None

        return skill

    def removeBuffsByTag(self,  tag):
        for buffId in list(self.buffMgrDic.keys()):
            if buffId not in self.buffMgrDic:
                continue

            if B_BD.datas[buffId][tag]:
                self.removeBuff(buffId)

    def getBuffSrcKey(self, buffId, srcEntId=None):
        bd = B_BD.datas.get(buffId, {})
        if bd.get('isCover', 1):
            return 0

        # addBuff里releaseRole会转成host，所以这里也要转一下，否则会出现creation加的buff自己无法找到，因为srcKey算到主人去了
        if (self.IsCreation or self.IsSummon) and self.getHost():
            return self.getHost().getBuffSrcKey(buffId, srcEntId)

        return srcEntId if srcEntId is not None else self.id

    def getBuffByBuffId(self, buffId, buffSrcKey=None):
        _buffMap = self.buffMgrDic.get(buffId, {})
        if buffSrcKey is None:
            buffSrcKey = self.getBuffSrcKey(buffId)

        return _buffMap.get(buffSrcKey)

    def checkRemoveBuffAfterTargetTypeChanged(self):
        _rmBuffs = []
        for _buffId, buffMap in self.buffMgrDic.items():
            for buffSrcKey, buffVal in buffMap.items():
                _srcEnt = buffVal.releaseRole
                if not _srcEnt or _srcEnt.id == self.id:
                    continue
                if buff.Buff.getKind(_buffId) < 0 and utils.checkTargetTypeValid('Friend', _srcEnt, self):
                    _rmBuffs.append((_buffId, buffSrcKey))
                elif buff.Buff.getKind(_buffId) >= 0 and utils.checkTargetTypeValid('Enemy', _srcEnt, self):
                    _rmBuffs.append((_buffId, buffSrcKey))

        for _buffId, buffSrcKey in _rmBuffs:
            self.removeBuff(_buffId, buffSrcKey)

    def doRemoveAllBuff(self):
        for _buffId in list(self.buffMgrDic.keys()):
            self.removeBuff(_buffId)

    def removeBuff(self, buffId, buffSrcKeys=None, isFinished=False, removeType=gameconst.RemoveTypeEnum.RTEnumDefault):
        if not buffId in self.buffMgrDic:
            return
        LOG_DBG('removeBuff', buffId, buffSrcKeys, removeType)
        self.buffMgrDic.removeBuff(self, buffId, buffSrcKeys, isFinished, removeType)

    def removeBuffByKind(self, buffKind):
        for _buffId in list(self.buffMgrDic.keys()):
            if buff.Buff.getKind(_buffId) != buffKind:
                continue

            self.removeBuff(_buffId)

    def removeBuffByTag(self, buffTag):
        for _buffId in list(self.buffMgrDic.keys()):
            tagList = buff.Buff.getTag(_buffId)
            if not (tagList and buffTag in tagList):
                continue

            self.removeBuff(_buffId)

    def removeBuffBySkillId(self, skill):
        skillId = skill.skillId
        LOG_INFO('removeBuffBySkillId 1 ', skillId)
        buffIds = list(self.buffMgrDic.keys())
        for buffId in buffIds:
            bufData = self.buffMgrDic.get(buffId)
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
                        LOG_INFO('removeBuffBySkillId 2 ', skillId, buffId)
                        self.removeBuff(buffId)
                    else:
                        if self.school == gameconst.CharacterType.Taoist:
                            if ctx.skillId == dataUtils.getSkillIdByMorphState(skillId, gameconst.MORPH_BUILD_STATE):
                                LOG_INFO('removeBuffBySkillId 3 ', skillId, buffId)
                                self.removeBuff(buffId)

    def broadcastAddBuffEvent(self, buffID, srcKeys):
        self.allClientsOnAddBuff(buffID, srcKeys)

    def removeBuffWithoutCalc(self, buffId, srcKeys):
        self.buffMgrDic.removeWithoutCalc(buffId, srcKeys)

    def addBuff(self, buffId, level, releaseRoleId, duration=-1, rootContext=None, kwargs=None):
        LOG_DBG("addBuff ", buffId, level, releaseRoleId, duration, kwargs)
        if buffId not in buff_buff.datas:
            LOG_ERR('addBuff buffId not in configTable', buffId)
            return

        if self.isDie() and not buff.Buff.fetchDeadDontRemove(buffId):
            return

        if len(self.buffMgrDic) >= gameconst.MAX_BUFF_COUNT:
            LOG_WARN('buff num reaches max, ignore', buffId)
            return

        _releaseRole = KBEngine.entities.get(releaseRoleId)

        if not _releaseRole:
            LOG_WARN('addBuff fail: invalid src entity', buffId, level, releaseRoleId, rootContext)
            return

        buffSrcKey = _releaseRole.getBuffSrcKey(buffId)
        if self.hasBuff(buffId, buffSrcKey):
            self.removeBuff(buffId, buffSrcKey)

        if _releaseRole.IsAvatar:
            _releaseRoleGbId = _releaseRole.gbId
        else:
            _releaseRoleGbId = None
        self.buffMgrDic.doAddBuff(self, buffId, level, duration, releaseRoleId, _releaseRole.name, _releaseRoleGbId,
                               gameconst.BuffSrcTypeEnum.Combat, buffSrcKey, rootContext, kwargs)

        # 这里取一遍，因为addBuff里面会去结算，可能又触发删除buff的逻辑
        _buffVal = self.getBuffByBuffId(buffId, buffSrcKey)
        if _buffVal:
            self.onEffectEventCall('onSelfBuff', releaseRoleId, self.id, effectEventCtx.BuffEventContext(buffId))

            _buffVal = self.getBuffByBuffId(buffId, buffSrcKey)
            if _buffVal:
                # 再取一遍，因为 onSelfbuff里面也可能删除buff
                self.broadcastAddBuffEvent(buffId, _buffVal.getClientStream())

    def changeBuffLevel(self, buffId, changeLv, releaseRoleId, duration=-1, rootContext=None, levelLimit=0,
                        autoHandleBuff=True):
        """修改buff层数"""
        LOG_DBG('changeBuffLevel::', buffId, changeLv, releaseRoleId, duration, levelLimit, autoHandleBuff)
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
                LOG_ERR('changeBuffLevel:: can\'t changeBuffLevel if buff not exist', buffId, changeLv)
                return False

            if changeLv <= 0:
                # Nothing to do here
                return True

            else:
                if levelLimit and levelLimit < changeLv:
                    LOG_WARN('changeBuffLevel:: over level limit, reset level to limit', changeLv, levelLimit)
                    changeLv = levelLimit
                self.addBuff(buffId, changeLv, releaseRoleId, duration, rootContext)
                return True

        buffLevel = _buff.level
        _buffNewLevel = max(0, buffLevel + changeLv)

        # case2: 新的buff层数<=0
        if _buffNewLevel <= 0:
            if not autoHandleBuff:
                LOG_ERR('changeBuffLevel:: can\'t changeBuffLevel if new buff level <= 0', changeLv, _buffNewLevel)
                return False
            self.removeBuff(buffId, _buffSrcKey)
            return True

        # default: 更新buff层数
        if levelLimit and levelLimit < _buffNewLevel:
            LOG_DBG('changeBuffLevel:: 2 over level limit, reset level to limit', _buffNewLevel, levelLimit)
            _buffNewLevel = levelLimit
        _buff.overlayBuff(self, _buffNewLevel, duration)
        self.allClientsCallOnUpdateBuff(buffId, _buff.getClientStream())
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
        self.allClientsCallOnUpdateBuff(buffId, _buff.getClientStream())
        return True
    
    def hasBuff(self, buffId, buffSrcKey=None):
        if buffId in self.buffMgrDic and self.buffMgrDic[buffId]:
            if buffSrcKey is None or buffSrcKey in self.buffMgrDic[buffId]:
                return True
        return False

    def hasBuffTag(self, tag):
        return self.buffMgrDic.hasBuffTag(tag)

    def getBuffLv(self, buffId, srcEnt=None):
        buffMap = self.buffMgrDic.get(buffId, {})
        buffLv = 0
        srcEnt = srcEnt or self
        buffSrcKey = srcEnt.getBuffSrcKey(buffId)
        if buffSrcKey in buffMap:
            buffLv = buffMap[buffSrcKey].level
        return buffLv

    def killSelf(self, sourceType):
        self.modifyHP(-self.hp, self.id, sourceType, 0)

    def goDie(self, killer, srcType, srcId, forceDead=False, context=None):
        LOG_WARN('goDie', killer.id, srcType, srcId, forceDead)
        if self.isDie():
            LOG_WARN("goDie:: already dead", killer, srcType, srcId)
            return

        self.onEffectEventCall('onDead', killer.id, self.id, effectEventCtx.EE_DEFAULT_CTX)
        if not killer.IsCreation:
            killer.onEffectEventCall('onKill', self.id, killer.id, effectEventCtx.EE_DEFAULT_CTX)

        # : 防止时间触发时isDie()返回还未死亡
        self.setState(gameconst.StateEnum.Death)
        self.killChannelingSkill(gameconst.ChannelingBreak.BREAK_TP_SELF_DIE)
        self.killCastingSkill(gameconst.EndCasting.ECEnumDead)
        self.onDead(killer, srcType, srcId)

        if killer.IsAICombatUnit:
            killer.removeHate(self.id)

    def modifyHP(self, hpValue, releaseRoleId, srcType, srcId, forceDead=False, context=None):
        if srcType == gameconst.SourceType.SrcTpItem:
            hpValue = hpValue * self.getMoralEffectItemPercent()
        hpValue = int(hpValue)
        if self.isDie():
            return 0

        _releaseRole = KBEngine.entities.get(releaseRoleId)
        # 自己可能传送到其他场景了，找不到来源entity正常的
        if not _releaseRole:
            return 0

        if (hpValue > 0 and self.hp < self.fullHp) or (hpValue < 0 and self.hp > 0):
            self.onEffectEventCall('onHPModify', releaseRoleId, self.id, effectEventCtx.HpEventCtx(hpValue))

        oldHp = self.hp
        _curHp = self.hp + hpValue

        # 免死事件触发：当伤害足以致死时，通知效果系统进行锁血
        if _curHp <= 0 and hpValue < 0:
            # 没有生效中的锁血效果，才会触发噬天
            if not self.getTempMiscProp(gameconst.EntityPropsEnum.lockMinHp) and srcType != gameconst.SourceType.SrcTpDropDeath:
                self.onEffectEventCall('onImmuneDie', releaseRoleId, self.id, effectEventCtx.EE_DEFAULT_CTX)

        # 【【任务】支持boss濒死】
        # 锁血相关, 需要将self.hp 修改提前到最先
        if _curHp > self.fullHp:
            self.hp = _curHp = self.fullHp
        elif _curHp < 0:
            self.hp = _curHp = 0
        else:
            self.hp = _curHp

        realReleaseRole = utils.getEntityRealEntity(_releaseRole)
        _lInfo = self.getTempMiscProp(gameconst.EntityPropsEnum.lockMinHp)
        if _lInfo and _lInfo.isValid():
            if self.hp < _lInfo.minHp:
                _lInfo.effectTimes += 1
                self.hp = _curHp = _lInfo.minHp

        if hpValue:
            if self.IsAvatar:
                pass
                # self.flowCtrlDunAnyPlayerHpMonitorTrigger(int(oldHp), int(_curHp), self.fullHp)
            elif hasattr(self, 'gameEntityId'):
                # 【【任务】新手剧情-新手村部分-NPC 添加buff】
                # 包括怪物/CNPC等可战斗实体都需要支持该节点
                self.flowCtrlMonsterHpMonitorTrigger(
                    utils.parseGidFromGameEntityId(self.gameEntityId), int(oldHp), int(_curHp), self.fullHp)
                pass

        if _curHp <= 0 and self.IsAvatar and self.duelAttr.inFight():
            if self.duelAttr.isDuelEnemy(realReleaseRole) or realReleaseRole.id == self.id:
                self.hp = int(self.getDuelDeathHp(oldHp))
                LOG_INFO('modifyHP:: duel death, hp: ', oldHp, self.hp)
                duelFlag = self.duelAttr.duelFlagEnt()
                if duelFlag:
                    duelFlag.onAvatarDuelFailed(self.id)
                else:
                    LOG_ERR('modifyHP:: duelFlagEntity not found', self.id)

        # 矿战怪物免死
        if formula.inMineWarScene(self.spaceNo) and _curHp <= 0 and self.IsMonster:
            self.hp = _curHp = self.mineWarMonsterImmuneDeath(_releaseRole, srcType, srcId, _curHp)

        hpDelta = self.hp - oldHp
        if hpDelta < 0 and realReleaseRole.IsAvatar:
            realReleaseRole.addDamageSetInFighting(self)

        if self.hp <= 0:
            self.goDie(_releaseRole, srcType, srcId, forceDead, context)

        if self.IsAICombatUnit and self.aiController and self.hp == self.fullHp:
            self.aiController.onHpFull()

        return hpDelta

    def onDoDamage(self, destEntId):
        host = utils.getHostEntity(self)
        _targetHost = utils.getHostEntity(KBEngine.entities.get(destEntId))
        if _targetHost and host.IsAvatar and _targetHost.IsAvatar and host.id != _targetHost.id:
            host.checkPKWithAvatar(_targetHost)
            _targetHost.checkBeAttackByAvatarPK(host)
            host.setHateRecord(_targetHost.id)

    def onBeDamaged(self, dmgSrcEntityId, damageVal, absorbVal, srcType, srcId):
        _srcTargetHost = utils.getHostEntity(KBEngine.entities.get(dmgSrcEntityId))
        host = utils.getHostEntity(self)
        if _srcTargetHost and host and host.IsAvatar and _srcTargetHost.IsAvatar and host.id != _srcTargetHost.id:
            host.setHateRecord(_srcTargetHost.id)

        _channelingSkillVal = self.getChannelingSkillInfo()
        if _channelingSkillVal:  # 引导时收到伤害
            interruptType = _channelingSkillVal.getInterruptByAttack(_channelingSkillVal.skillId)
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

    def modifyMP(self, mpValue, context=None):
        if context:
            srcType = context.getDmgSourceType()
            if srcType == gameconst.SourceType.SrcTpBuff and context.parentContext:
                srcType = context.parentContext.getDmgSourceType()
            if srcType == gameconst.SourceType.SrcTpItem:
                mpValue = mpValue * self.getMoralEffectItemPercent()
        mpValue = int(mpValue)
        if not mpValue:
            return

        _curMp = self.mp + mpValue
        if _curMp > self.fullMp:
            self.mp = self.fullMp
        elif _curMp < 0:
            self.mp = 0
        else:
            self.mp = _curMp

    def removeSkill(self, skillID, isFromDeleteTempSkill = False):
        LOG_DBG('removeSkill ', skillID, isFromDeleteTempSkill)
        skill = self.skillDic.doGetSkill(skillID, False)
        if skill:
            if isFromDeleteTempSkill:
                self.removeBuffBySkillId(skill)
            self.skillDic.doRemoveSkill(skillID)
        return skill
    
    def doActionOnChangeSlot(self, skillId, skillLv, bActive, bTakeSkill, fromSkillNextCastTime, reason):
        LOG_DBG('doActionOnChangeSlot ', skillId, skillLv, bActive, bTakeSkill, fromSkillNextCastTime, reason)
        if bTakeSkill:
            skill = self.takeSkill(skillId, skillLv, tNextCast = fromSkillNextCastTime)
        else:
            skill = self.skillDic.doGetSkill(skillId, False)

        if not skill:
            return
        skill.skillDoActionOnChangeSlot(self, bActive)

        if reason != gameconst.CHANGE_SKILL_REASON_UNLOCK:
            return

        # 解锁技能走到了这里,解锁技能需要解锁被铭文升级后的技能
        newSkillId, oldSkillId = self.glyphEquipData.getInscriptionSrcSkillId(skillId)
        if newSkillId == skillId:
            return

        # 这里走eventactions的接口来替换
        self.changeSkill(None, None, skillId, newSkillId)

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
        _isSetState = False
        if self.state != stateVec[0]:
            self.state = stateVec[0]
            _isSetState = True
        if self.state2 != stateVec[1]:
            self.state2 = stateVec[1]
            _isSetState = True
        if _isSetState:
            self.stateList = formula.getInt64ListOnIndexes(stateVec)

    def setStateByCounter(self, state):
        _cnt = self.stateCounters.get(state, 0)
        self.stateCounters[state] = _cnt  + 1
        LOG_DBG('setStateByCounter', _cnt)
        if _cnt == 0:
            self.setState(state)
    
    def removeStateByCounter(self, state):
        _cnt = self.stateCounters.get(state, 0)
        LOG_DBG('removeStateByCounter', _cnt)
        if _cnt <= 1:
            self.stateCounters.pop(state, None)
            self.removeState(state)
        else:
            self.stateCounters[state] = _cnt - 1

    def onOverlayStatus(self, state):
        if state == CCDD.datas.Down:
            # 这个协议作用是如果当前已经在这个状态时候重入给客户端发事件
            self.allClients.onStateChangedForce(state)

    def setState(self, state, reportErr=True, isInit=False):
        if state < 0:
            reportErr and LOG_ERR("states is error:", state)
            return False
        """return True if state is exist"""
        if self.hasState(state) and not isInit:
            if state == gameconst.StateEnum.Fighting and self.IsAvatar:
                self.enterFightingState()
            return True

        eventId = C_SD.datas[state].get('event')
        _conflictRes = self.checkConflictState(eventId, remConflctState=False, isInit=isInit)
        if eventId and not _conflictRes:
            # 现在设置状态前没有判断与当前状态是否冲突，可能会设置失败，这里打个trace检查这种情况
            reportErr and gameengine.panicStack('setState fail', eventId, state, _conflictRes.extra)

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
            self.breakSkillByState(gameconst.SkillTagEnum.antiBreak)

        elif state == gameconst.StateEnum.Flying:
            self.enterFlyingState()
        elif state == CCDD.datas.blazing:
            self.enterBlazeState()

        _stateVec = self.getStateBitVector()
        formula.setInt64ListBit(_stateVec, state)

        _rmStates = []
        _stateBitsList = self.stateList
        _stateBitsList.append(state)
        if eventId:
            for st in _stateBitsList:
                if st != state:
                    val = conflict_conflict.datas[eventId].get(str(st))
                    if val == 0:
                        reportErr and LOG_ERR("checkConflict false", eventId, state, st, self.state, _stateBitsList)
                    elif val == 2:
                        formula.setInt64ListBit(_stateVec, st, on=False)
                        _rmStates.append(st)

        self.setStateBitVector(_stateVec)
        self._onRemovedState(_rmStates, state)

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

        self.setStateBitVector(stateVec)
        self._onRemovedState([state], state, removeReason=removeReason)
        self.doRemoveState(state)

    def removeStates(self, rmStates, byConflictState=-1, removeReason=0):
        stateVec = self.getStateBitVector()

        for state in rmStates:
            formula.setInt64ListBit(stateVec, state, on=False)
            self.doRemoveState(state)
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

    def hasState(self, status):
        if status < 0:
            LOG_ERR("states is error:", status)
            return False
        if status >= 64:
            return (self.state2 >> (status - 64)) & 1 > 0
        else:
            return (self.state >> status) & 1 > 0

    def _onRemovedState(self, states, byConflictState=-1, removeReason=0):
        for _state in states:
            if _state == gameconst.StateEnum.Fighting:
                self.leaveFightingState()

            elif _state == gameconst.StateEnum.autoFight:
                self._stopAutoCombat()

            elif _state == gameconst.StateEnum.Moving and hasattr(self, 'removeMoveController'):
                self.removeMoveController()

            elif _state == gameconst.StateEnum.Channeling or _state == gameconst.StateEnum.moveChannel:
                LOG_DBG("removeState  killChannelingSkill ")
                if removeReason:
                    self.killChannelingSkill(removeReason)
                else:
                    self.killChannelingSkill(gameconst.ChannelingBreak.BREAK_TP_CONFLICT_STATE)

            elif _state == gameconst.StateEnum.Casting:
                LOG_DBG("removeState  killCastingSkill ", byConflictState)
                if byConflictState >= 0 and byConflictState in (gameconst.StateEnum.Moving, gameconst.StateEnum.Idle):
                    self.killCastingSkill(gameconst.EndCasting.ECEnumMove)
                elif byConflictState == gameconst.StateEnum.Death:
                    self.killCastingSkill(gameconst.EndCasting.ECEnumDead)
                elif byConflictState == gameconst.StateEnum.clientPick:
                    self.killCastingSkill(gameconst.EndCasting.ECEnumclientPick)
                else:
                    self.killCastingSkill(gameconst.EndCasting.ECEnumConflictState)

            elif _state == gameconst.StateEnum.riding:
                self._onExitRiding(byConflictState)

            elif _state == gameconst.StateEnum.clientPick:
                self._onExitClientPick(byConflictState, removeReason)

            elif _state == gameconst.StateEnum.posture:
                self.exitPlayEmote(byConflictState, removeReason)

            elif _state == gameconst.StateEnum.GeneralAttack:
                if removeReason != gameconst.RemoveStateReason.SKILL_DONE:
                    self._breakGeneralSkill()

            elif _state == gameconst.StateEnum.Shifting or _state == gameconst.StateEnum.Dodging:
                self.endMovement()
                if removeReason == gameconst.RemoveStateReason.CONFLICT:
                    LOG_DBG('[exitShift] by conflict')
                    self.allClients.onExitShiftByConflict(self.position)

            elif _state == gameconst.StateEnum.Sprinting:
                self.leaveSprintingState()
            elif _state == gameconst.StateEnum.Flying:
                if byConflictState not in (gameconst.StateEnum.Fall, gameconst.StateEnum.speedFall):
                    self.setState(gameconst.StateEnum.Fall)
                self.addTimerCB(1, '_onRemoveFlyingState', (), gametimer.TIMER_TAG_ON_REMOVE_FLY_STATE)

                self.leaveFlyingState()

            elif _state == CCDD.datas.duel:
                self.leaveDuelState()
            elif _state == CCDD.datas.blazing:
                self.leaveBlazeState()

            buffTag = C_SD.datas[_state].get('buffTag')
            if buffTag:
                self.removeBuffByTag(buffTag)

    def _onRemoveFlyingState(self):
        self.topSpeed = gameconst.TopSpeedType.NormalTopSpeed
                
    @classmethod
    def clearAllCache(cls):
        cls._fetchConflictEventName.cache_clear()
        cls.fetchConflictEventCfgData.cache_clear()
        cls._fetchConflictStatusName.cache_clear()
        cls.getConflictStatus.cache_clear()

    @staticmethod
    @functools.lru_cache(64)
    def _fetchConflictStatusName(stateId):
        return C_SD.datas.get(stateId, {}).get('statusName', '')

    @staticmethod
    @functools.lru_cache(64)
    def _fetchConflictEventName(eventId):
        return conflict_conflict.datas[eventId]['eventName']

    @staticmethod
    @functools.lru_cache(64)
    def _getConflictPopupIndex(stateId):
        return C_SD.datas.get(stateId, {}).get('popupIndex', 0)

    @staticmethod
    @functools.lru_cache(64)
    def fetchConflictEventCfgData(eventId):
        return conflict_conflict.datas[eventId]
    
    @staticmethod
    @functools.lru_cache(64)
    def getConflictStatus(eventId):
        allStatus = SkillManager.fetchConflictEventCfgData(eventId)
        status = 0
        for k, v in allStatus.items():
            if k.isnumeric() and (v == 2 or v == 3):
                status |= 1 << int(k)
        return status

    def checkConflictState(self, evId, bMsg=True, remConflctState=False, isInit=False):
        if not evId:
            return gameclass.ResultBool(True, -1)

        remState = []
        cfgData = self.fetchConflictEventCfgData(evId)
        for _state in self.stateList:
            val = cfgData.get(str(_state))
            if val == 1:
                continue
            elif val == 0:
                bMsg and LOG_WARN("has conflict evId=[{}] _state=[{}] val=[0]".format(evId, _state))
                return gameclass.ResultBool(False, _state)
            elif val == 2 and remConflctState:
                remState.append(_state)
            elif val == 3:
                bMsg and LOG_WARN("has conflict evId=[{}] _state=[{}] val=[3]".format(evId, _state))
                return gameclass.ResultBool(False, _state)
            elif M_MD.datas.get(val, None):
                bMsg and LOG_WARN("has conflict evId=[{}] _state=[{}] val=[{}]".format(evId, _state, val))
                return gameclass.ResultBool(False, _state)

        if len(remState) > 0:
            self.removeStates(remState, removeReason=gameconst.RemoveStateReason.CONFLICT)

        return gameclass.ResultBool(True, -1)

    def getRandomPosition(self, center, radii):
        _posList = self.getRandomPoints(center, radii, 1, 0)
        if not _posList:
            return None

        return _posList[0]

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

    def recordUsingSkill(self, skillVal, targetId):
        pass

    def removeUsingSkillRecord(self, skillId):
        pass

    def onUseSkillFinish(self, skillId):
        if self.IsAvatar and self.autoCombat == gameconst.AutoCombatStatus.Fighting:
            self.doAutoCombatCheckUseSkill(skillId)

    def doUseSkill(self, skill, actionCtx, compensateTime=0, isSetState=True, fixDir=None, ignoreReasons=0):
        LOG_DBG("doUseSkill ", skill.skillId, actionCtx.useTargetId, actionCtx.skillArgs, actionCtx.isClient, compensateTime)
        if skill.hasSkillTag(gameconst.SkillTagEnum.changeCDStatusSkill) \
            and skill.getTempData(gameconst.SkillTempDataKey.CHANGE_SKILL_CD_STATUS, gameconst.SkillCDStatus.DEFAULT) == gameconst.SkillCDStatus.DISABLED:
            return gameconst.UseSkillCheck.USC_ENUM_IN_CD_STATUS

        if skill.hasSkillTag(gameconst.SkillTagEnum.Casting):
            return self._castingSkillObjInternal(skill, actionCtx)
        else:
            return self._useSkillBySkillObj(skill, actionCtx, compensateTime, isSetState=isSetState, fixDir=fixDir, ignoreReasons=ignoreReasons)

    def _breakGeneralSkill(self):
        usingSkills = self.getTempMiscProp(gameconst.EntityPropsEnum.currentUseSkill, default={})
        for sid in list(usingSkills.keys()):
            if sid not in usingSkills:
                continue

            sVal, tid = usingSkills[sid]
            if sVal.hasSkillTag(gameconst.SkillTagEnum.GeneralSkill):
                sVal.useSkillDone(self, 0, [], isSucc=False, doRemoveState=True, forceResetSkill=True)

    def _useSkillBySkillObj(self, skill, actionCtx, compensateTime=0, isSetState=True, fixDir=None, ignoreReasons=0):
        skillId = skill.skillId
        LOG_INFO('_useSkillBySkillObj: skill:{}, tgt:{}, arr:{}, {}'.format(skillId, actionCtx.useTargetId, actionCtx.skillArgs, actionCtx.isClient))
        # 走到这里如果不是Avatar，则一定是吟唱成功，如果是Avatar暂且认为吟唱过程成功，在canUse里会做校验
        castingSkillVal = self.getCastingSkillInfo()
        if castingSkillVal and self.hasState(gameconst.StateEnum.Casting):
            if castingSkillVal.skillId == skillId and castingSkillVal.isCastingSucc(delta=0.2):
                endReason = gameconst.EndCasting.ECEnumFinished
            else:
                endReason = gameconst.EndCasting.ECEnumOtherSkill

            self._onEndCastingSkill(endReason)

        realSkill, replaceSkill = skill.getRealSkillVal(self)
        if actionCtx.isClient:
            ignoreReasons |= gameconst.UseSkillCheck.USC_ENUM_TARGET_NOT_FOUND

        _ret = realSkill.checkUseSkill(
            self, 
            actionCtx.useTargetId, 
            ignoreReasons, 
            checkInRange=actionCtx.checkInRange,
            checkStage=gameconst.CHECK_SKILL_STAGE_BEFORE_BEGIN,
        )

        if _ret != gameconst.UseSkillCheck.USC_ENUM_CHEKC_OK:
            target = KBEngine.entities.get(actionCtx.useTargetId)
            if not (target and target.isDie()):
                LOG_WARN("Spell::doUseSkill(%i):skillID=%i _ret=%i tNextCast=%i" % (self.state, skillId, _ret, skill.tNextCast))

            self.debugCombatMsg('_useSkillBySkillObj doUseSkill fail: targetId:%s, _ret:%s, skillArgs:%s', actionCtx.useTargetId, _ret, actionCtx.skillArgs)
            self.client.onUseSkill(False, skillId, actionCtx.useTargetId, [], [], [])
            return _ret

        # 多段技能check时按当前段check，但是replaceSkill是false，表示使用时还调用第一段的使用
        # 因为后面段是第一段的子技能，子技能只能通过父技能使用
        if actionCtx.isClient and not realSkill.checkSkillArgs(self, actionCtx.skillArgs):
            LOG_WARN("doUseSkill: invalid skill args", realSkill.skillId, actionCtx.useTargetId, actionCtx.skillArgs)
            if realSkill.isChangePosSkill(realSkill.skillId):
                self.client.onUseSkill(False, skillId, actionCtx.useTargetId, [], [], [])
            return None

        if utils.hasSkillTagById(skillId, gameconst.SkillTagEnum.UltraSkill):
            self.resetUsingSkills(gameconst.ResetSkillReason.ReasonUltraSkill)

        if fixDir is not None:
            self.direction = fixDir

        if replaceSkill:
            isSucc = realSkill.beginUseSkill(self, actionCtx.useTargetId, actionCtx.skillArgs, compensateTime, isSetState=isSetState, parentCtx=actionCtx)
            isGeneral = realSkill.hasSkillTag(gameconst.SkillTagEnum.GeneralSkill)
        else:
            isSucc = skill.beginUseSkill(self, actionCtx.useTargetId, actionCtx.skillArgs, compensateTime, isSetState=isSetState, parentCtx=actionCtx)
            isGeneral = skill.hasSkillTag(gameconst.SkillTagEnum.GeneralSkill)

        if isSucc and not isGeneral:
            self._breakGeneralSkill()

        return None

    def delayCalcSkill(self, skillVal, targetId, arr, actionCtx, calcDelay, doRemoveState=True):
        # delay过程中如果有传送，skillVal不是skillDic里的值，这里重拿一次
        _skill = self.skillDic.doGetSkill(skillVal.skillId, reportErr=False)
        # 如果getSkill没拿到，说明这种技能不是skillDic里的技能，就用iTimer里存的即可

        _skill = _skill or skillVal
        actionCtx.skillObj = _skill
        if not _skill:
            LOG_ERR('delayCalcSkill: cannot get _skill', _skill.skillId, targetId)
            return

        _skill._cancelTempTimer(self, gameconst.SkillTempDataKey.DELAY_CALC_TIMER, gametimer.TIMER_TAG_SKILL_DELAY_CALC)
        ignoreReasons = gameconst.UseSkillCheck.USC_DELAY_CHECK_IGNORES
        if actionCtx.isClientSkill():
            ignoreReasons |= gameconst.UseSkillCheck.USC_ENUM_TARGET_NOT_FOUND

        _ret = _skill.checkUseSkill(self, targetId, ignoreReasons=ignoreReasons)
        if _ret != gameconst.UseSkillCheck.USC_ENUM_CHEKC_OK:
            _skill.useSkillDone(self, targetId, arr, False, doRemoveState)
            return

        self._doUseSkill(_skill, targetId, arr, actionCtx, calcDelay, doRemoveState)

    def _doUseSkill(self, skill, tgtId, arr, actionCtx, calcDelay, doRemoveState=True):
        skill.applySkillEffect(self, tgtId, arr, actionCtx, calcDelay, doRemoveState)

    def _onSkillCallback(self, skill, callbackName, args):
        skill.onTimerCallback(self, callbackName, args)

    def _castingSkillObjInternal(self, skillObj, actionCtx):
        self.debugCombatMsg("_castingSkillObjInternal:%s %s %s", skillObj.skillId, actionCtx.useTargetId, actionCtx.skillArgs)
        if self.hasState(gameconst.StateEnum.Casting):
            return None

        if not self.checkConflictState(C_C_DD.datas.cast):
            LOG_INFO('skill %d cannot use: checkConflict: %d' % (skillObj.skillId, C_C_DD.datas.cast))
            return None

        skillID = skillObj.skillId
        skillLv = skillObj.skillLv
        realSkillVal, replaceSkill = skillObj.getRealSkillVal(self)
        if replaceSkill:
            ret = self._useSkillBySkillObj(realSkillVal, actionCtx)
            return ret

        ignoreReasons = gameconst.UseSkillCheck.USC_ENUM_STATE_CONFLICT | gameconst.UseSkillCheck.USC_ENUM_NEED_CAST
        if actionCtx.isClient:
            ignoreReasons |= gameconst.UseSkillCheck.USC_ENUM_TARGET_NOT_FOUND

        ret = skillObj.checkUseSkill(self, actionCtx.useTargetId, ignoreReasons=ignoreReasons)
        if ret != gameconst.UseSkillCheck.USC_ENUM_CHEKC_OK:
            LOG_INFO("Spell::castingSkill(%i): cannot spell skillID=%i, targetID=%i, code=%i" % (
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

    def fetchAttackDistanceCompensation(self):
        return 0

    def castingSkillCheck(self, targetID, arr, castPos):
        skillObj = self.getCastingSkillInfo()
        skillObj._cancelTempTimer(self, gameconst.SkillTempDataKey.CASTING_CHECK_TIMER, gametimer.TIMER_TAG_CASTING_CHECK)

        if sMath.distance2DToCompareFrom3DPosition(castPos, self.position) > 1:
            self.killCastingSkill(gameconst.EndCasting.ECEnumMove)
            return

        # 如果客户端出错或者其他原因，吟唱时间到了后长时间没有调用spellTarget真正放吟唱技能，这里做容错结束吟唱
        # 对于服务器控制的实体，不会走到这里
        if time.time() - skillObj.castingStartTime > skillObj.getCastingtimeMax(skillObj.skillId) + 1:
            self._onEndCastingSkill(gameconst.EndCasting.ECEnumFinished)
            return

        timerId = self.addTimerCB(1, 'castingSkillCheck', (targetID, arr, castPos), gametimer.TIMER_TAG_CASTING_CHECK)
        skillObj.setTimerTempData(self, gameconst.SkillTempDataKey.CASTING_CHECK_TIMER, timerId)
        return

    def getCastingSkillInfo(self):
        curSkillInfo = self.getTempMiscProp(gameconst.EntityPropsEnum.currentCastingSkill)

        return curSkillInfo

    def getChannelingSkillInfo(self):
        _curSkillInfo = self.getTempMiscProp(gameconst.EntityPropsEnum.currentChannelSkill)

        return _curSkillInfo

    def killCastingSkill(self, reason):
        skillVal = self.getCastingSkillInfo()
        if not skillVal:
            return
        self._onEndCastingSkill(reason)
        self.allClients.onBreakCastingSkill(self.id, skillVal.skillId, 1)

    def _onEndCastingSkill(self, reason):
        castingSkillVal = self.getCastingSkillInfo()
        if not castingSkillVal:
            return

        if reason != gameconst.EndCasting.ECEnumFinished:
            castingSkillVal.onCastingInterrupted(self, reason)

        self.popTempMiscProp(gameconst.EntityPropsEnum.currentCastingSkill)
        self.removeState(gameconst.StateEnum.Casting)

        castingSkillVal.resetSkill(self, gameconst.ResetSkillReason.ReasonEndCasting)

    def channelingSkillTick(self, skillVal, targetID, arr, channelPos, actionCtx):
        skillId = skillVal.skillId
        skillLv = skillVal.skillLv
        self.popTempMiscProp(gameconst.EntityPropsEnum.channelSkillTimer)
        skillVal.popTempData(gameconst.SkillTempDataKey.CHANNELING_CALC_TIMER)
        cfgData = SSD.datas[skillId]

        isMoveSkill = skillVal.isMovingSkill(skillId)
        if sMath.distance2DToCompareFrom3DPosition(self.position, channelPos) > 1.0 and not isMoveSkill:
            self.debugCombatMsg('channelingSkillTick move: position:%s, channelPos:%s', self.position, channelPos)
            self.killChannelingSkill(gameconst.ChannelingBreak.BREAK_TP_MOVE)
            return

        target = KBEngine.entities.get(targetID)
        if skillVal.needReleaseTarget() and ((target and target.isDie()) or (targetID > 0 and not target)):
            self.debugCombatMsg('channelingSkillTick target is invalid: targetId:%s', targetID)
            self.killChannelingSkill(gameconst.ChannelingBreak.BREAK_TP_TARGET_DIE)
            return

        if self.isDie():
            self.killChannelingSkill(gameconst.ChannelingBreak.BREAK_TP_SELF_DIE)
            return

        effectTargetIds = skillVal.getEffectTargets(self, targetID, arr)
        skillVal.targetIds = effectTargetIds
        scopes = skillVal.getScope(skillVal.skillId)
        if not effectTargetIds:
            if not scopes or scopes == gameconst.SkillScopeEnum.TARGET_AUTO:
                if skillVal.channelCount == 0 and self.IsAvatar:
                    skillVal.setTempData(self, gameconst.SkillTempDataKey.IS_CHANNELING_EMPTY, True)
                if not skillVal.getTempData(gameconst.SkillTempDataKey.IS_CHANNELING_EMPTY, False):
                    self.killChannelingSkill(gameconst.EndCasting.ECEnumMissingTarget)
                    return

        skillVal.channelCount += 1
        skillArgsExtra = [skillVal.getRange(self, skillId, skillLv), skillVal.getEffectRange(self, skillId, skillLv)]
        self.allClients.onUseChanneling(self.id, skillId, targetID, arr, effectTargetIds,
                                        skillVal.channelCount, skillArgsExtra)

        isFinished = skillVal.channelCount >= skillVal.getChannelTime(skillVal.skillId)

        bulletTime = skillVal.calBulletTime(self, targetID)
        bulletTimer = self.addTimerCB(bulletTime, "channelingSkillEffect", (skillVal, targetID, arr, actionCtx, 0,
                                                                           channelPos),
                                     gametimer.TIMER_TAG_CHANNELING_SKILL_EFFECT)
        skillVal.setTimerTempData(self, gameconst.SkillTempDataKey.CHANNELING_BULLET_TIMER, bulletTimer)

        channelInterval = max(cfgData.get('channelInterval') or 1, 0.3)
        if not isFinished:
            timerId = self.addTimerCB(channelInterval, 'channelingSkillTick', (skillVal, targetID, arr, channelPos,
                                                                              actionCtx),
                                     gametimer.TIMER_TAG_CHANNELING_CALC)
            skillVal.setTimerTempData(self, gameconst.SkillTempDataKey.CHANNELING_CALC_TIMER, timerId)
        self.debugCombatMsg('channelingSkillTick done: skillId:%s, state:%s, targetId:%s, channelCount:%s, channelInterval:%s, isFinished:%s',
                            skillId, self.state, targetID, skillVal.channelCount, channelInterval, isFinished)
        return

    def channelingSkillEffect(self, skillVal, targetId, skillArgs, actionCtx, calcDelay, channelPos):
        skillVal.applySkillEffect(self, targetId, skillArgs, actionCtx, calcDelay)
        skillVal.popTempData(gameconst.SkillTempDataKey.CHANNELING_BULLET_TIMER)
        isFinished = skillVal.channelCount >= skillVal.getChannelTime(skillVal.skillId)

        if isFinished:
            self.debugCombatMsg('channelingSkillEffect end: channelCount:%s, channelTime:%s',
                                skillVal.channelCount, skillVal.getChannelTime(skillVal.skillId))
            skillVal.onChannlingEffectEnd(self)
            return

    def killChannelingSkill(self, reason, isFinished=False, notifyClient=True):
        _skillVal = self.getChannelingSkillInfo()
        if not _skillVal:
            return

        _skillVal.doEnterCDTime(self)
        self.client.onSetAddSkillCd(
            _skillVal.skillId, 
            float(_skillVal.getCDDur(self)), 
            float(_skillVal.tNextCast), 
            False, 
            _skillVal.getTempData(gameconst.SkillTempDataKey.RELEASE_TIME, 0), 
            _skillVal.getTempData(gameconst.SkillTempDataKey.TOTAL_RELEASE_CNT, 0), 
            _skillVal.getTempData(gameconst.SkillTempDataKey.RELEASED_CNT, 0), 
            not _skillVal.isSkillCDStatusFrozen()
        )

        if reason != gameconst.ChannelingBreak.BREAK_TP_NORMAR_END:
            _skillVal.onChannelingEnd(self, isFinished)

        if notifyClient:
            self.allClients.onBreakChannelingSkill(self.id, _skillVal.skillId, reason)

    def _endChannelingSkill(self):
        skillVal = self.getChannelingSkillInfo()
        if not skillVal:
            return

        self.debugCombatMsg('_endChannelingSkill: skillId:%s', skillVal.skillId)
        self.popTempMiscProp(gameconst.EntityPropsEnum.currentChannelSkill)

    def _executeSkillAction(self, skillId, context, calcDelay, actionFunction, target, duration=0):
        if not actionFunction:
            return True

        _ret = None
        try:
            if not target or (target and target.isReal()):
                if target:
                    target.onEffectEventCall('onFlashBeat', self.id, target.id, effectEventCtx.EE_DEFAULT_CTX)
                _ret = actionFunction(self, target, context)
        except Exception as e:
            gameengine.panicStack('_executeSkillAction error:', self.id, skillId, str(e), context)

        _actionFinished = True
        if _ret is not None:
            _actType, args = _ret
            if _actType == gameconst.SkillActionType.StagedAct:
                _delay, = args
                context.skillObj.setupMulAttackAction(self, context, _delay, calcDelay, duration + _delay)
                context.actionProgress = gameconst.ActionProgressEnum.actionDoing
                _actionFinished = False
            else:
                if context.actionProgress == gameconst.ActionProgressEnum.actionDoing:
                    _actionFinished = False
                context.isLastActionStage = True
        else:
            context.isLastActionStage = True

        return _actionFinished

    def doSkillAction(self, skillId, ctx, calcDelay, needUseCheck=False, checkIgnoreReasons=0, duration=0,
                      doRemoveState=True):
        skill = ctx.skillObj
        actionFunc = skill.getAction(skill.skillId)
        skillArgs = ctx.skillArgs
        if ctx.actionStage > 0:
            #多段技能重新随目标
            realSkillArgs = skillArgs
            positionSkillArgs = None
            if ctx.skillObj.isChangePosSkill(skillId):
                realSkillArgs = list(skillArgs)[:-3]
                positionSkillArgs = tuple(skillArgs[-3:])

            effectedEntIds = ctx.skillObj.getEffectTargets(self, ctx.useTargetId, realSkillArgs,
                                                               positionSkillArgs=positionSkillArgs)
            ctx.effectedEntIds = effectedEntIds
        effectedEntIds = ctx.effectedEntIds
        effectedTargets = utils.getEntitiesByIds(effectedEntIds)
        actionFinished = True

        skillDamges = ctx.getCombatResult()
        doActionTogether = skill.hasSkillTag(gameconst.SkillTagEnum.DoActionTogether)
        skillDamges.damageInfo = []

        skill._cancelTempTimer(self, gameconst.SkillTempDataKey.MUL_ATTACK_ACT_TIMER, gametimer.TIMER_TAG_DO_SKILL_ACTION)

        ctx.actionProgress = gameconst.ActionProgressEnum.actionDone
        ctx.checkInRange = False
        if skill.getEffectTargetType(skill.skillId) == 'None':
            actionFinished = self._executeSkillAction(skillId, ctx, calcDelay, actionFunc, None, duration)
        else:
            doActionTargets = []

            if needUseCheck:
                if effectedTargets:
                    for target in effectedTargets:
                        checkCode = skill.checkUseSkill(self, target.id, ignoreReasons=checkIgnoreReasons, checkInRange=ctx.checkInRange)
                        if checkCode == gameconst.UseSkillCheck.USC_ENUM_CHEKC_OK:
                            break
                    else:
                        skill.onSkillActionFinished(self, ctx.useTargetId, skillArgs, ctx, calcDelay, duration)
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
                    actionFinished = self._executeSkillAction(skillId, ctx, calcDelay, actionFunc, target, duration)

            if doActionTogether:
                ctx.effectedEntIds = [e.id for e in doActionTargets]
                _actionTarget = doActionTargets[0] if doActionTargets else None
                actionFinished = self._executeSkillAction(skillId, ctx, calcDelay, actionFunc, _actionTarget,
                                                          duration)
            else:
                if not effectedTargets:
                    actionFinished = self._executeSkillAction(skillId, ctx, calcDelay, actionFunc, None, duration)

        if skillDamges.damageInfo and not self.isDestroyed:
            self.sendSkillDamage(skillDamges)
            skillDamges.damageInfo = []

        if actionFinished:
            skill.onSkillActionFinished(self, ctx.useTargetId, skillArgs, ctx, calcDelay, duration,
                                        doRemoveState)

        return actionFinished

    def _getAtkSkillDmgType(self, schoolType):
        _eventId, _hitType = 0, 0
        if schoolType == gameconst.SCHOOL_PHYSICAL:
            _eventId = C_C_DD.datas.pBeat
            _hitType = gameconst.HitType.ImmuneDmg

        elif schoolType == gameconst.SCHOOL_MAGIC:
            _eventId = C_C_DD.datas.mBeat
            _hitType = gameconst.HitType.ImmuneDmg

        return _eventId, _hitType

    def onBeforeAttackAction(self, target, ctx, ignoreType=False):
        if not target or target.isDie():
            LOG_DBG('attack miss target', ctx)
            return False

        if not ignoreType:
            attackSrcEnt = ctx.getSrcEntity()
            if attackSrcEnt is None:
                LOG_WARN("onBeforeAttackAction has no src entity")
                return False

            if not utils.checkTargetTypeValid("Enemy", attackSrcEnt, target):
                LOG_WARN("onBeforeAttackAction checkTargetTypeValid error", attackSrcEnt.id, target.id)
                return False

        _dmgSchoolType = 0
        ignoreImmortal = False
        if ctx.actionType == actionContext.ACTION_USE_SKILL:
            skill = self._getSkillByActionContext(ctx)
            _dmgSchoolType = skill.getClassTag(self)
            ignoreImmortal = skill.hasSkillTag(gameconst.SkillTagEnum.IgnoreImmortal)

        elif ctx.actionType in (actionContext.ACTION_CREATION_LOOP, actionContext.ACTION_CREATION_COMMON):
            _dmgSchoolType = CRD.datas.get(ctx.creationId, {}).get('classTag', 0)

        elif ctx.actionType in (actionContext.ACTION_AUREOLE,):
            _dmgSchoolType = AAD.datas.get(ctx.aureoleId, {}).get('classTag', 0)

        elif ctx.actionType in (actionContext.ACTION_BUFF_TICK, actionContext.ACTION_BUFF_END,
                                    actionContext.ACTION_BUFF_EFFECT) and ctx.getBuffObject():
            _dmgSchoolType = B_BD.datas.get(ctx.buffId, {}).get('classTag', 0)

        if _dmgSchoolType:
            skillDamges = ctx.getCombatResult()
            _eventId, hitType = self._getAtkSkillDmgType(_dmgSchoolType)

            if _eventId:
                _conflictResult = target.checkConflictState(_eventId, bMsg=False, remConflctState=True)
                if not _conflictResult and _conflictResult.extra in (
                        CCDD.datas.PImmortal, CCDD.datas.MImmortal) and not ignoreImmortal:
                    if hitType not in gameconst.HitType.zeroFilter:
                        skillDamges.damageInfo.append(combatSkill.SkillDamageVal(target.id, 0, hitType))
                    return False

        return True

    def getHost(self):
        return None

    def getFirstHost(self, num=1):
        if num >= 3:
            return self

        if self.IsCreation or self.IsSummon:
            _host = self.getHost()
            if _host:
                return _host.getFirstHost(num + 1)

        return self

    def calcAtkStats(self, target, context, dmg):
        if not dmg:
            return

        if self.IsSummon or self.IsCreation:
            _host = self.getHost()
            _host and _host.IsAvatar and _host.calcAtkStats(target, context, dmg)

    def calcBeHurtStats(self, target, context, damageResult, realDmgVal):
        if not damageResult.hurtDmg:
            return

        if self.IsSummon:
            _host = self.getHost()
            _host and _host.IsAvatar and _host.calcBeHurtStats(target, context, damageResult, realDmgVal)


    def calcHealStats(self, target, context, hpDelta):
        if not hpDelta:
            return

        if self.IsSummon or self.IsCreation:
            _host = self.getHost()
            _host and _host.IsAvatar and _host.calcHealStats(target, context, hpDelta)

    def applyDamageResult(self, target, context, damageResult):
        self.debugCombatMsg('applyDamageResult: sourceId:%s, targetId:%s, context:%s, damageResult:%s', context.getDmgSourceId(), target.id, context, damageResult)
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

        _realDmgVal = damageResult.dmg
        absorbDamageDetail = {}

        dmgSrcEnt = context.getSrcEntity() or self
        # AvatarMirror,Pet，召唤物都算自己的，创生算主人的
        if dmgSrcEnt.IsCreation:
            dmgSrcEnt = dmgSrcEnt.getHost() or dmgSrcEnt

        dmgAfterTransfer = _realDmgVal

        # 护盾吸收
        shieldAbsorbVal = 0
        if damageResult.calcShield:
            target.onEffectEventCall('onBeatShield', self.id, target.id, effectEventCtx.HpEventCtx(dmgAfterTransfer))
            _realDmgVal, absorbDamageDetail = target.absorbShieldWithDetails(dmgAfterTransfer)
            shieldAbsorbVal = dmgAfterTransfer - _realDmgVal
            if _realDmgVal == 0 and shieldAbsorbVal:
                # 全被吸收
                skillDamges.damageInfo.append(combatSkill.SkillDamageVal(target.id, shieldAbsorbVal, gameconst.HitType.Absorb))

        # 增加焚心值, 由于modifyHp的时候会造成切磋状态改变，所以要放在modifyHp之前
        self.onDoDamage(target.id)

        # 真实扣血
        recordDmgVal = 0
        suckHpVal = 0
        if _realDmgVal >= 0:
            _realHpDelta = target.modifyHP(-_realDmgVal, dmgSrcEnt.id, context.getDmgSourceType(), context.getDmgSourceId(),
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
                if _realDmgVal:
                    if hasattr(context, 'isCombo'):
                        skillDamges.damageInfo.append(combatSkill.SkillDamageVal(target.id, _realDmgVal, gameconst.HitType.ComboHit))
                    else:
                        skillDamges.damageInfo.append(combatSkill.SkillDamageVal(target.id, _realDmgVal, gameconst.HitType.Hit))

            elif damageResult.atkType == gameconst.SkillAttackType.ATTACK_DODGE:
                # 被部分闪避
                target.onEffectEventCall('onDodge', self.id, target.id, effectEventCtx.EE_DEFAULT_CTX)
                skillDamges.damageInfo.append(
                    combatSkill.SkillDamageVal(target.id, _realDmgVal, gameconst.HitType.Miss))

            elif damageResult.atkType == gameconst.SkillAttackType.ATTACK_CRIT:
                # 暴击伤害
                self.onEffectEventCall('onFatal', self.id, target.id, effectEventCtx.EE_DEFAULT_CTX)
                # 受到玩家伤害
                if self.IsAvatar:
                    target.onEffectEventCall('onFatalBeat', self.id, target.id, effectEventCtx.EE_DEFAULT_CTX)
                    
                if _realDmgVal:
                    if hasattr(context, 'isCombo'):
                        skillDamges.damageInfo.append(combatSkill.SkillDamageVal(target.id, _realDmgVal, gameconst.HitType.ComboCrit))
                    else:
                        skillDamges.damageInfo.append(combatSkill.SkillDamageVal(target.id, _realDmgVal, gameconst.HitType.Crit))

            else:
                LOG_ERR('unknow attack type', target.id, context, damageResult)

            if damageResult.hpSuck:
                # 吸血
                suckHpVal = dmgSrcEnt.modifyHP(damageResult.hpSuck, dmgSrcEnt.id, context.getDmgSourceType(),
                                               context.getDmgSourceId())
                dmgSrcEnt.onEffectEventCall('onBloodSuck', dmgSrcEnt.id, target.id,
                                        effectEventCtx.HpEventCtx(damageResult.hpSuck))
                if damageResult.hpSuck:
                    skillDamges.damageInfo.append(
                        combatSkill.SkillDamageVal(dmgSrcEnt.id, damageResult.hpSuck, gameconst.HitType.HPRecover))

            # effect里造成的血量伤害不触发onHit，否则攻击附带xxx效果会死循环
            if context.actionType not in (actionContext.ACTION_BUFF_EFFECT, actionContext.ACTION_EVENT_EFFECT):
                dmgSrcEnt.onEffectEventCall('onHit', self.id, target.id,
                                        effectEventCtx.HpEventCtx(_realDmgVal, damageResult.dmgType))
                if not target.IsCreation:
                    target.onEffectEventCall('onBeat', self.id, target.id, effectEventCtx.HpEventCtx(_realDmgVal))

        target.onBeDamaged(dmgSrcEnt.id, _realDmgVal, shieldAbsorbVal, context.getDmgSourceType(),
                           context.getDmgSourceId())

        _sDmgSrcEnt = context.getSrcEntity()
        _sDmgSrcEnt = _sDmgSrcEnt or self
        if _sDmgSrcEnt.IsCreation or _sDmgSrcEnt.IsSummon:
            _sDmgSrcEnt = _sDmgSrcEnt.getFirstHost() or _sDmgSrcEnt

        if _sDmgSrcEnt.IsAvatar:
            recordDmgVal += shieldAbsorbVal
            if recordDmgVal < 0:
                recordDmgVal = 0

        target.calcBeHurtStats(dmgSrcEnt, context, damageResult, _realDmgVal)
        dmgSrcEnt.calcAtkStats(target, context, _realDmgVal)
        dmgSrcEnt.calcHealStats(dmgSrcEnt, context, suckHpVal)

        self.sendDmgMsgs(target, context, damageResult, absorbDamageDetail, _realDmgVal)

        # 策划需求返回真实伤害，方便后面做一些吸血之类的操作
        return recordDmgVal

    def sendDmgMsgs(self, target, context, damageResult, absorbDamageDetail, realDmgVal):
        ctx = context or context.parentContext
        self.debugCombatMsg('sendDmgMsg: sourceId:%s, targetId:%s, context:%s, damageResult:%s, absorbDamageDetail:%s, realDmgVal:%s',
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
        _skillId = 0
        if context.actionType in (actionContext.ACTION_USE_SKILL,):
            _skillId = context.skillId
        elif context.parentContext and context.parentContext.actionType in (actionContext.ACTION_USE_SKILL,):
            _skillId = context.parentContext.skillId
        else:
            return

        if not _skillId:
            return

        if hpDelta > 0 and self.id != target.id and not self.isDie() and self.spaceNo == target.spaceNo:
            _hateRecord = target.getTempMiscProp(gameconst.EntityPropsEnum.hateRecord, {})
            for _mEid in list(_hateRecord.keys()):
                _ent = KBEngine.entities.get(_mEid)
                if not _ent:
                    continue
                if not _ent.isDie() and _ent.spaceNo == self.spaceNo and hasattr(_ent, 'aiController'):
                    skillHateRatio = SSD.datas[_skillId].get('skillHateRatio', 0.1)
                    if _ent.aiController:
                        _ent.aiController.doIncreaseHate(self.id, hpDelta * skillHateRatio)

    def applyHealActionResult(self, tgt, context, healResult: combatSkill.HealResult):
        if not tgt:
            return

        _skillDamges = context.getCombatResult()
        if not _skillDamges:
            _skillDamges = combatSkill.SkillDamges(self.id, context.getDmgSourceType(), context.getDmgSourceId())

        # 如果血量被锁定了，就不分摊伤害吸血什么的，也不跳数字了
        if tgt.getTempMiscProp(gameconst.EntityPropsEnum.isHpLocked, False):
            return

        healSrcEnt = context.getSrcEntity() or self
        if healSrcEnt.IsCreation or healSrcEnt.IsSummon:
            healSrcEnt = healSrcEnt.getFirstHost() or healSrcEnt

        hpDelta = 0
        if healResult.healVal > 0:
            if tgt:
                ratio = 1

                healResult.healVal = int(healResult.healVal * ratio)
                srcType = context.getDmgSourceType()
                if srcType == gameconst.SourceType.SrcTpBuff and context.parentContext:
                    srcType = context.parentContext.getDmgSourceType()
                hpDelta = tgt.modifyHP(healResult.healVal, self.id, srcType,
                                          context.getDmgSourceId())
                if hpDelta:
                    if healSrcEnt and healSrcEnt.IsAvatar and context.getDmgSourceType() == gameconst.SourceType.SrcTpSkill:
                        healSrcEnt.setState(gameconst.StateEnum.Fighting)

                self.addHealHate(hpDelta, tgt, context)

                healResult.healVal = hpDelta

            if hpDelta:
                if healResult.isCrit:
                    _skillDamges.damageInfo.append(
                        combatSkill.SkillDamageVal(tgt.id, hpDelta, gameconst.HitType.HealCrit))
                else:
                    _skillDamges.damageInfo.append(
                        combatSkill.SkillDamageVal(tgt.id, hpDelta, gameconst.HitType.HPRecover))

        self.calcHealStats(tgt, context, hpDelta)

    def calcFrameTime(self, distance, speed):
        _speed = speed / gameconst.gameUpdateHertz
        return max(1, math.ceil(distance / _speed))

    def displacedBySkill(self, srcEntityId, pos, speed, timeEx, context=None):
        src = KBEngine.entities.get(srcEntityId)
        if not src:
            return False

        _ret = self.checkConflictState(C_C_DD.datas.bePushed, True)
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

        _realDist = sMath.distance2D(self.position, pos)
        _yaw = sMath.getYawFromDirection(Math.Vector3(src.position) - Math.Vector3(pos))

        _oldCollidable = self.collidable
        self.collidable = False
        self.direction = (0.0, 0.0, _yaw)

        _frames = self.calcFrameTime(_realDist, speed)
        # 算出真实的每秒速度
        _realSpeed = _realDist * gameconst.gameUpdateHertz / _frames

        self.bePushedSpeed = _realSpeed
        if self.hasState(gameconst.StateEnum.bePushed):
            self.cancelTimerCB(self._displaceTimer, gametimer.TIMER_TAG_DISPLACED_BY_SKILL_DONE)
        self.setState(gameconst.StateEnum.bePushed)
        self.controlledBy = None
        self.moveToPoint(pos, _realSpeed, 0, (), False, 0)

        # 不能完全依赖onMoveOver恢复，过程中可能传送或者被别的打断，如果没恢复过来客户端就完全操作不了了
        if _realDist <= 0 or _realSpeed <= 0:
            pushTime = timeEx
        else:
            pushTime = _realDist / _realSpeed + timeEx
        self._displaceTimer = self.addTimerCB(pushTime, '_displacedBySkillDone', (srcEntityId, _oldCollidable),
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

        for _propName in inheritList:
            props[_propName] = self.getProp(_propName)

        return props

    def getSummonCloneCombatProps(self):
        _props = {}

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
            _props[propName] = self.getProp(propName)

        return _props

    def getTargetByViewRadius(self):
        if self.IsAvatar:
            return self.getViewRadius()
        return gameconst.DEFAULT_AOI

    def getTargetIdsByTargetType(self, targetString):
        if self.isDestroyed:
            return set()
        if not self.useTargetTypeCacheFlag:
            viewRadius = self.getTargetByViewRadius()
            for _e in self.entitiesInRange(viewRadius):
                if _e.IsCombatUnit:
                    utils.isEnemy(self, _e)
                    utils.isFriend(self, _e)
            self.useTargetTypeCacheFlag = True
            self.stopCacheTargetTypeTimerId = self.addTimerCB(30, 'resetTargetTypeCacheFlag', (),
                                                            gametimer.TIMER_TAG_SET_TARGET_TYPE_CACHE_FLAG,
                                                            'stopCacheTargetTypeTimerId')
            if not self.checkTargetTypeTimerId:
                self.checkTargetTypeTimerId = self.pyAddTimer(5, 5, gametimer.CHECK_TARGET_TYPE_TIMER)
        else:
            if self.stopCacheTargetTypeTimerId:
                self.cancelTimerCB(self.stopCacheTargetTypeTimerId, gametimer.TIMER_TAG_SET_TARGET_TYPE_CACHE_FLAG)
                self.stopCacheTargetTypeTimerId = self.addTimerCB(30, 'resetTargetTypeCacheFlag', (),
                                                                gametimer.TIMER_TAG_SET_TARGET_TYPE_CACHE_FLAG,
                                                                'stopCacheTargetTypeTimerId')

        if targetString == "None":
            return self.enemiesCacheSet.union(self.notEnemiesCacheSet, {self.id})

        elif targetString == "PlayerExTarget":
            if self.IsMonster and self.aiController and self.aiController.hateDic:
                maxHateTargetId, _ = self.aiController.hateDic.getFirstVisibleHateTarget()
            if maxHateTargetId:
                targetSet = set(self.enemiesCacheSet)
                targetSet.discard(maxHateTargetId)
                return targetSet
            else:
                return set(self.enemiesCacheSet)

        else:
            _set = None
            _value = utils.getFightTargetTypeFromCfgData(targetString)
            if not _value:
                LOG_ERR('getTargetIdsByTargetType: targetString={} not found'.format(targetString))
                return set()

            for _tp in _value[2]:
                if _tp == gameconst.CampType.All:
                    _set = self.enemiesCacheSet.union(self.notEnemiesCacheSet, {self.id})
                    break

                elif _tp == gameconst.CampType.Enemy:
                    if _set is None:
                        _set = set(self.enemiesCacheSet)

                    else:
                        _set = _set.union(self.enemiesCacheSet)

                elif _tp == gameconst.CampType.Friend:
                    if _set is None:
                        _set = set(self.friendsCacheSet)

                    else:
                        _set = _set.union(self.friendsCacheSet)

                elif _tp == gameconst.CampType.Self:
                    if _set is None:
                        _set = {self.id}

                    else:
                        _set = _set.union({self.id})

                elif _tp == gameconst.CampType.EnemyExTarget:
                    if _set is None:
                        _set = set(self.enemiesCacheSet)

                    else:
                        _set = _set.union(self.enemiesCacheSet)

            if len(_value) > 3 and self.IsAvatar:
                temp_set = set()
                for _tp in _value[3]:
                    if _tp == gameconst.TeamType.TEAM and self.isInTeam():
                        teamList = []
                        for playerBaseVal in self.teamInfo.teamPlayerDict.values():
                            if playerBaseVal.playerBox:
                                teamList.append(playerBaseVal.playerBox.id)
 
                        temp_set = temp_set.union(teamList)
                    elif _tp == gameconst.TeamType.RAID and self.inRaid():
                        raidList = []
                        for teamVal in self.raidInfo.raidTeamDic.values():
                            for playerInfo in teamVal.teamPlayerDict.values():
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

    def getTargets(self, centerEnt, targetId, targetString, targetRange=20, forceTarget=False, beginSkillPos=None):
        targetsList = []
        entityIdList = self.getTargetIdsByTargetType(targetString)

        target = KBEngine.entities.get(targetId)

        if forceTarget and target:
            entityIdList.add(targetId)

        for eId in entityIdList:
            _entity = KBEngine.entities.get(eId)
            if not _entity:
                continue

            if _entity.isDestroyed:
                continue

            if not _entity.IsCombatUnit:
                continue

            if _entity.IsMonster:
                _targetRange = targetRange + _entity.getCreepData().get('attackDistanceCompensation')

            else:
                _targetRange = targetRange

            if beginSkillPos:
                if not sMath.inRectRange2D(_targetRange, _entity.position, beginSkillPos):
                    continue
            else:
                if not sMath.inRectRange2D(_targetRange, _entity.position, self.position):
                    continue

            if not self.checkCombatRangeY(_entity):
                continue

            if utils.checkCachedTargetType(targetString, self, _entity, target):
                targetsList.append(_entity)

        return targetsList

    def isTarget(self, target, eId, targetString, targetRange, checkFun, beginSkillPos=None):
        _entity = KBEngine.entities.get(eId)
        if not _entity or _entity.isDestroyed or not _entity.IsCombatUnit:
            return False

        if _entity.IsMonster:
            targetRange += _entity.getCreepData().get('attackDistanceCompensation')

        if beginSkillPos:
            if not sMath.inRectRange2D(targetRange, _entity.position, beginSkillPos):
                return False
        else:
            if not sMath.inRectRange2D(targetRange, _entity.position, self.position):
                return False

        if not self.checkCombatRangeY(_entity):
            return False

        if not utils.checkCachedTargetType(targetString, self, _entity, target):
            return False

        return checkFun(_entity)

    def getTargetsWithNum(self, centerEnt, targetId, targetString, targetRange, targetNum, checkScopeFun,
                          beginSkillPos=None):
        targetIdsList = []
        entityIdList = self.getTargetIdsByTargetType(targetString)
        _target = KBEngine.entities.get(targetId)

        if targetNum > 1:
            if targetString == "Friend" or targetString == "FriendExGB":
                entityIdList.discard(self.id)
                if self.isTarget(_target, self.id, targetString, targetRange, checkScopeFun, beginSkillPos):
                    targetIdsList.append(self.id)
                if targetId in entityIdList:
                    entityIdList.discard(targetId)
                    if self.isTarget(_target, targetId, targetString, targetRange, checkScopeFun, beginSkillPos):
                        targetIdsList.append(targetId)
            elif targetString == "Enemy" or targetString == "EnemyExTarget":
                if targetId in entityIdList:
                    entityIdList.discard(targetId)
                    if self.isTarget(_target, targetId, targetString, targetRange, checkScopeFun, beginSkillPos):
                        targetIdsList.append(targetId)

        if len(targetIdsList) >= targetNum:
            return targetIdsList

        if KBEngine.getAverageLoad() < 0.6:
            entityIdList = list(entityIdList)
            random.shuffle(entityIdList)

        for eId in entityIdList:
            _entity = KBEngine.entities.get(eId)
            if self.isTarget(_entity, eId, targetString, targetRange, checkScopeFun, beginSkillPos):
                targetIdsList.append(eId)
            if len(targetIdsList) >= targetNum:
                break

        return targetIdsList

    def updateTimeEffect(self, effectCaller, effectId, effectIndex):
        _effectVal = effectCaller.getEffectVal(self, effectId, effectIndex)
        if not _effectVal:
            return

        _effectVal.updateEffect(self, effectCaller)

    def addSummon(self, id, pos, direction, hostId, skillLv, bDieWithHost, ttl,
                  summonLevel, buffId, buffLv, inheritPropRatio=1.0,
                  summonProps=None):
        _props = {
            'summonId': id, 
            'hostId': self.id, 
            'spaceNo': self.spaceNo, 
            'dieWithHost': bDieWithHost,
            'spaceMgrId': self.spaceMgrId, 
            'force': self.force, 
            'ttl': ttl, 
            'level': summonLevel,
            'inheritPropRatio': inheritPropRatio}
        
        _props['createContext'] = actionContext.CreateSummonCtx(summonLevel, skillLv)
        
        summonProps and _props.update(summonProps)

        _summon = KBEngine.createEntity('Summon', self.spaceID, pos, direction, _props)
        if not _summon:
            LOG_ERR('addSummon Error', id, pos, hostId)
            return False

        if buffId and buffLv:
            _summon.addBuff(buffId, buffLv, self.id)

        if skillLv:
            _summon.setAllSkillLv(skillLv)

        self.petList.append(_summon.id)

    def resetStateOnline(self):
        stList = list(self.stateList)
        _removedSt = []
        LOG_INFO('resetStateOnline', stList)
        for st in stList:
            if C_SD.datas[st].get('clearOnline', 0) or C_SD.datas[st].get('buffTag', 0):
                _removedSt.append(st)
                self.removeState(st)

        for st in stList:
            if st not in _removedSt:
                self.setState(st, isInit=True)

    def resetStateTeleport(self, oldSpaceNo):
        for i in self.stateList:
            if not self.hasState(i):
                continue

            if i == gameconst.StateEnum.Moving and not self.isCleanMove(oldSpaceNo):
                continue

            val = C_SD.datas[i].get('clearTeleport', 0)
            if val == 1:
                self.removeState(i)
                LOG_INFO("resetStateTeleport", self.id, i)

    def addSkillEffectCd(self, skillID, cdDelta):
        _skill = self.skillDic.doGetSkill(skillID)
        if _skill is None:
            LOG_ERR("Spell::addSkillEffectCd(%i):skillID=%i not found" % (self.id, skillID))
            return False

        _skill.changeCD(self, cdDelta)
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

        if self.checkShieldTimerId > 0:
            self.pyDelTimer(self.checkShieldTimerId, gametimer.TIMER_CHECK_SHIELD)
        self.checkShieldTimerId = self.pyAddTimer(0, 1, gametimer.TIMER_CHECK_SHIELD)

    def removeShield(self, buffID):
        if buffID in self.shieldDic:
            self.shieldDic.pop(buffID)
        if len(self.shieldDic) == 0:
            if self.checkShieldTimerId > 0:
                self.pyDelTimer(self.checkShieldTimerId, gametimer.TIMER_CHECK_SHIELD)
                self.checkShieldTimerId = 0

    def checkShield(self):
        self.onEffectEventCall('onShield', self.id, 0, effectEventCtx.EE_DEFAULT_CTX)

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
            self.removeBuff(buffId, isFinished=True, removeType=gameconst.RemoveTypeEnum.RTEnumEndByBeat)

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
                    # 增加除0保护
                    if shieldVal.getShieldMaxValue() < 1e-6:
                        _rate = 1
                    else:
                        _rate = (1 - absorbedVal/shieldVal.getShieldMaxValue())
                    duration = remainTime * _rate
                    self.changeBuffDuration(buffId, duration, self.id)
                    LOG_DBG('absorbShieldWithDetails 4', useShieldType, nHpModify, remainHp, absorbedVal, shieldVal.shieldValue, duration)
        return remainHp
    
    def removeCreation(self, creationId):
        if creationId in self.creationList:
            self.creationList.remove(creationId)

    def destoryAllCreation(self):
        for _creationId in list(self.creationList):
            creation = KBEngine.entities.get(_creationId)
            if not creation:
                LOG_WARN('destoryAllCreation: cannot find creation', _creationId)
                continue
            if not creation.isDestroyed:
                creation.safeDestroy()
        self.creationList.clear()

    def removeSummonById(self, summonId):
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

        for _summonId in list(self.petList):
            summon = KBEngine.entities.get(_summonId)
            if summon:
                summon.safeDestroy()
        self.petList.clear()

    def destroySummonOnDead(self):
        for _summonId in list(self.petList):
            summon = KBEngine.entities.get(_summonId)
            if summon and summon.dieWithHost:
                summon.delaySafeDestroy()
                self.petList.remove(_summonId)

        for _cloneId in list(self.cloneList):
            clone = KBEngine.entities.get(_cloneId)
            if clone and clone.dieWithHost:
                clone.delaySafeDestroy()
                self.cloneList.remove(_cloneId)

    def removeBuffOnDead(self):
        for buffId in list(self.buffMgrDic.keys()):
            # 前面的buff的endAction可能把后面的buff删掉
            if buffId not in self.buffMgrDic:
                continue

            for _buffVal in self.buffMgrDic[buffId].values():
                if _buffVal.isRemoveOnDead():
                    self.removeBuff(buffId)
                    break

    @gamedecorator.crossServer
    @utils.isMyself
    def getBuffInfo(self, exposed, entityId):
        _target = KBEngine.entities.get(entityId)
        if _target and _target.buffMgrDic:
            self.client.onGetBuffInfo(entityId, _target.buffMgrDic.getClientData(_target))

    # 客户端entity创建好后来服务器取一把光环信息，因为aureoleDic这个属性只有部分数据
    # 需要发给客户端，所以不能做成ALL_CLIENTS,只能在进入AOI时再发一次或者让客户端再取一次
    # 服务器的onEnterView接口里取self.clientEntity可能客户端实体还没创建好，所以暂时只能让客户端来拿
    @gamedecorator.crossServer
    def getAureoleInfo(self, exposed, entityId):
        if not self._isMyself(exposed):
            return

        _target = KBEngine.entities.get(entityId)
        if _target and _target.auraDic:
            self.client.onGetAureoleInfo(entityId, _target.auraDic.getClientData())

    def onCloneInitMoveover(self):
        return

    def onCloneDestroy(self, cloneID):
        if cloneID in self.cloneList:
            self.cloneList.remove(cloneID)

    def getOwnedCreations(self, cid=0):
        _ret = []
        for _c in self.creationList:
            _ent = KBEngine.entities.get(_c)
            if _ent and (not cid or _ent.creationId == cid):
                _ret.append(_ent)
        return _ret

    def getOwnedSummons(self, sid=0):
        _ret = []
        for s in self.petList:
            ent = KBEngine.entities.get(s)
            if ent and (not sid or ent.creepbaseId == sid):
                _ret.append(ent)
        return _ret

    def onEndChongfeng(self, skillVal, targetId, skillArgs):
        self.removeState(gameconst.StateEnum.Shifting)

    def onEndLunge(self, skillVal, targetId, skillArgs):
        self.removeState(gameconst.StateEnum.Shifting)

    def endDodge(self, skillVal, targetId, skillArgs):
        self.removeState(gameconst.StateEnum.Dodging)

    def endMovement(self):
        if self.getNeedUpdateWitnessPosDir() == 0:
            self.cancelController('Movement')

    def endUpdateWitnessPosDir(self):
        LOG_DBG("endUpdateWitnessPosDir")
        self.setNeedUpdateWitnessPosDir(1)

    def resetShiftOrDodgeTimer(self):
        self.popTempMiscProp(gameconst.EntityPropsEnum.shiftOrDodgeTimer, 0)

    def onMoveOver(self, controllerId, userData):
        if userData == gamemove.LUNGE_MOVE_OVER:
            self.onLungeMoveOver(True)
        elif userData == gamemove.CHONGFENG_MOVE_OVER:
            self.onChongfengMoveOver(True)
        elif userData == gamemove.DODGE_MOVE_OVER:
            LOG_DBG("onMoveOver --------------------- ", self.position)
            self.onDodgeMoveOver(True)

    def onMoveFailure(self, controllerId, userData):
        if userData == gamemove.LUNGE_MOVE_OVER:
            self.onLungeMoveOver(False)
        elif userData == gamemove.CHONGFENG_MOVE_OVER:
            self.onChongfengMoveOver(False)
        elif userData == gamemove.DODGE_MOVE_OVER:
            LOG_DBG("onMoveFailure --------------------- ", self.position)
            self.onDodgeMoveOver(False)

    def onMoveBreak(self, controllerId, userData):
        if userData == gamemove.LUNGE_MOVE_OVER:
            self.onLungeMoveOver(False)
        elif userData == gamemove.CHONGFENG_MOVE_OVER:
            self.onChongfengMoveOver(False)
        elif userData == gamemove.DODGE_MOVE_OVER:
            LOG_DBG("onMoveBreak --------------------- ", self.position)
            self.onDodgeMoveOver(False)
        elif not userData:
            self.removeState(gameconst.StateEnum.Moving)

    def onMove(self, controllerId, userData):
        if self.IsAvatar:
            LOG_DBG("onMove --------------------- ", userData, self.position)


    def onChongfengMoveOver(self, isSucc):
        self.setNeedUpdateWitnessPosDir(1)
        self.topSpeed = gameconst.TopSpeedType.NormalTopSpeed
        chongfengData = self.popTempMiscProp(gameconst.EntityPropsEnum.chongfengData)
        if not chongfengData:
            LOG_ERR('chongfeng err: move failed', isSucc)
            self.onEndChongfeng(None, 0, [])
            return

        _context, calcDelay = chongfengData

        skill = self._getSkillByActionContext(_context)

        if not skill:
            LOG_ERR('onChongfengMoveOver: cannot get skill', skill.skillId, _context)
            self.onEndChongfeng(None, 0, [])
            return

        targetId = _context.useTargetId
        self.onEndChongfeng(skill, targetId, _context.skillArgs)
        if skill.checkUseSkill(self, targetId,
                               ignoreReasons=gameconst.UseSkillCheck.USC_DELAY_CHECK_IGNORES) != gameconst.UseSkillCheck.USC_ENUM_CHEKC_OK:
            skill.useSkillDone(self, targetId, _context.skillArgs, False)
            return

        if _context.actionProgress == gameconst.ActionProgressEnum.startActionDoing:
            _context.actionProgress = gameconst.ActionProgressEnum.startActionDone
            if isSucc:
                skillId, skillLv = skill.getNotifyClientSkillId()
                skillArgsExtra = [skill.getRange(self, skillId, skillLv), skill.getEffectRange(self, skillId, skillLv)]
                self.allClients.onUseSkill(True, skillId, targetId, _context.skillArgs,
                                           _context.effectedEntIds, skillArgsExtra)
            self._doUseSkill(skill, targetId, _context.skillArgs, _context, calcDelay)
        elif _context.actionProgress == gameconst.ActionProgressEnum.actionDoing and _context.isLastActionStage:
            if skill.hasTempData(gameconst.SkillTempDataKey.DURATION):
                duration = skill.popTempData(gameconst.SkillTempDataKey.DURATION)
            else:
                duration = 0
            remainTime = skill.getSkillTime(skill.skillId) - calcDelay - duration
            _context.actionProgress = gameconst.ActionProgressEnum.actionDone
            if remainTime <= 0:
                skill.useSkillDone(self, targetId, _context.skillArgs)
            else:
                skill._cancelTempTimer(self, gameconst.SkillTempDataKey.SKILL_DONE_TIMER, gametimer.TIMER_TAG_SKILL_DONE)
                tid = self.addTimerCB(remainTime, '_onSkillCallback',
                                     (skill, 'useSkillDone', (targetId, _context.skillArgs, True, False, True)),
                                     gametimer.TIMER_TAG_SKILL_DONE)
                skill.setTimerTempData(self, gameconst.SkillTempDataKey.SKILL_DONE_TIMER, tid)

    def onLungeMoveOver(self, isSucc):
        LOG_DBG("###onLungeMoveOver")
        self.setNeedUpdateWitnessPosDir(1)
        self.topSpeed = gameconst.TopSpeedType.NormalTopSpeed
        lungeData = self.popTempMiscProp(gameconst.EntityPropsEnum.lungeSkillData)
        if not lungeData:
            LOG_ERR('lunge err: move failed', isSucc)
            self.onEndLunge(None, 0, [])
            return

        _context, calcDelay = lungeData

        skill = self._getSkillByActionContext(_context)

        if not skill:
            LOG_ERR('onLungeMoveOver: cannot get skill', skill.skillId, _context)
            self.onEndLunge(None, 0, [])
            return

        targetId = _context.useTargetId
        self.onEndLunge(skill, targetId, _context.skillArgs)
        _ignore = gameconst.UseSkillCheck.USC_DELAY_CHECK_IGNORES
        _ignore |= gameconst.UseSkillCheck.USC_ENUM_TARGET_NOT_FOUND

        if  skill.checkUseSkill(self, targetId,
                               ignoreReasons=_ignore) != gameconst.UseSkillCheck.USC_ENUM_CHEKC_OK:
            skill.useSkillDone(self, targetId, _context.skillArgs, False)
            return

        if _context.actionProgress == gameconst.ActionProgressEnum.startActionDoing:
            _context.actionProgress = gameconst.ActionProgressEnum.startActionDone
            if isSucc:
                skillId, skillLv = skill.getNotifyClientSkillId()
                skillArgsExtra = [skill.getRange(self, skillId, skillLv), skill.getEffectRange(self, skillId, skillLv)]
                self.allClients.onUseSkill(True, skillId, targetId, _context.skillArgs,
                                           _context.effectedEntIds, skillArgsExtra)
            self._doUseSkill(skill, targetId, _context.skillArgs, _context, calcDelay)
        elif _context.actionProgress == gameconst.ActionProgressEnum.actionDoing and _context.isLastActionStage:
            if skill.hasTempData(gameconst.SkillTempDataKey.DURATION):
                duration = skill.popTempData(gameconst.SkillTempDataKey.DURATION)
            else:
                duration = 0
            remainTime = skill.getSkillTime(skill.skillId) - calcDelay - duration
            _context.actionProgress = gameconst.ActionProgressEnum.actionDone
            if remainTime <= 0:
                skill.useSkillDone(self, targetId, _context.skillArgs)
            else:
                tid = self.addTimerCB(remainTime, '_onSkillCallback',
                                     (skill, 'useSkillDone', (targetId, _context.skillArgs, True, False, True)),
                                     gametimer.TIMER_TAG_SKILL_DONE)
                skill.setTimerTempData(self, gameconst.SkillTempDataKey.SKILL_DONE_TIMER, tid)

    def onDodgeMoveOver(self, isSucc):
        self.setNeedUpdateWitnessPosDir(1)
        self.topSpeed = gameconst.TopSpeedType.NormalTopSpeed
        dodgeData = self.popTempMiscProp(gameconst.EntityPropsEnum.dodgeSkillData)
        if not dodgeData:
            LOG_ERR('dodge err: move failed', isSucc)
            self.endDodge(None, 0, [])
            return

        _context, calcDelay = dodgeData

        skill = self._getSkillByActionContext(_context)

        if not skill:
            LOG_ERR('onDodgeMoveOver: cannot get skill', skill.skillId, _context)
            self.endDodge(None, 0, [])
            return

        targetId = _context.useTargetId
        self.endDodge(skill, 0, _context.skillArgs)
        if skill.checkUseSkill(self, targetId,
                               ignoreReasons=gameconst.UseSkillCheck.USC_DELAY_CHECK_IGNORES) != gameconst.UseSkillCheck.USC_ENUM_CHEKC_OK:
            skill.useSkillDone(self, targetId, _context.skillArgs, False)
            return

        if _context.actionProgress == gameconst.ActionProgressEnum.startActionDoing:
            _context.actionProgress = gameconst.ActionProgressEnum.startActionDone
            if isSucc:
                skillId, skillLv = skill.getNotifyClientSkillId()
                skillArgsExtra = [skill.getRange(self, skillId, skillLv), skill.getEffectRange(self, skillId, skillLv)]
                self.allClients.onUseSkill(True, skillId, targetId, _context.skillArgs,
                                           _context.effectedEntIds, skillArgsExtra)
            self._doUseSkill(skill, targetId, _context.skillArgs, _context, calcDelay)
        elif _context.actionProgress == gameconst.ActionProgressEnum.actionDoing and _context.isLastActionStage:
            if skill.hasTempData(gameconst.SkillTempDataKey.DURATION):
                duration = skill.popTempData(gameconst.SkillTempDataKey.DURATION)
            else:
                duration = 0
            remainTime = skill.getSkillTime(skill.skillId) - calcDelay - duration
            _context.actionProgress = gameconst.ActionProgressEnum.actionDone
            if remainTime <= 0:
                skill.useSkillDone(self, targetId, _context.skillArgs)
            else:
                tid = self.addTimerCB(remainTime, '_onSkillCallback',
                                     (skill, 'useSkillDone', (targetId, _context.skillArgs, True, False, True)),
                                     gametimer.TIMER_TAG_SKILL_DONE)
                skill.setTimerTempData(self, gameconst.SkillTempDataKey.SKILL_DONE_TIMER, tid)

    def onEnterTrap(self, otherEntity, rangeXZ, rangeY, controllerId, userArg):
        if hasattr(super(), 'onEnterTrap'):
            super().onEnterTrap(otherEntity, rangeXZ, rangeY, controllerId, userArg)

        if not otherEntity or otherEntity.isDestroyed:
            return

        if userArg == gameconst.AURA_TRAP:
            if not otherEntity.IsCombatUnit:
                return

            self.auraDic.addCtrlInPending(controllerId)

            _aura = self.auraDic.getByCtrlId(controllerId)
            _entityId = otherEntity.id

            if not _aura:
                return

            if not utils.checkTargetTypeValid(_aura.effectTarget, self, otherEntity):
                return

            _aura.addAureoleTarget(self, _entityId)

    def onLeaveTrap(self, otherEntity, rangeXZ, rangeY, controllerId, userArg):
        if hasattr(super(), 'onLeaveTrap'):
            super().onLeaveTrap(otherEntity, rangeXZ, rangeY, controllerId, userArg)
        if not otherEntity:
            return

        if userArg == gameconst.AURA_TRAP:
            _aura = self.auraDic.getByCtrlId(controllerId)
            _entityId = otherEntity.id

            if not _aura:
                return

            _aura.onLeaveAureoleRnage(self, _entityId)

    def onEnterWholeAureole(self, otherEntity):
        if not otherEntity:
            return

        if not otherEntity.IsCombatUnit:
            return

        for aureoleId in self.auraDic._wholeAreaAuraList:
            _aura = self.auraDic.get(aureoleId)
            _entityId = otherEntity.id
            if _aura and utils.checkTargetTypeValid(_aura.effectTarget, self, otherEntity):
                _aura.addAureoleTarget(self, _entityId)

    def onLeaveWholeAureole(self, otherEntity):
        if not otherEntity:
            return

        for aureoleId in self.auraDic._wholeAreaAuraList:
            _aura = self.auraDic.get(aureoleId)
            _entityId = otherEntity.id
            if _aura and utils.checkTargetTypeValid(_aura.effectTarget, self, otherEntity):
                _aura.onLeaveAureoleRnage(self, _entityId)

    def setCombatControlState(self, ctrlState, antiDuration, controlLevel=1):
        if ctrlState not in self.controlledStates:
            csVal = combatSkill.ControlState(controlLevel, time.time())
            csVal.refreshAntiTimer(self, ctrlState, antiDuration)
            self.controlledStates[ctrlState] = csVal
        else:
            csVal = self.controlledStates[ctrlState]
            csVal.refreshAntiTimer(self, ctrlState, antiDuration)

        return csVal

    def getControllLv(self, ctrlState):
        if ctrlState not in self.controlledStates:
            return 0

        return self.controlledStates[ctrlState].controlLevel

    def removeCombatControlState(self, ctrlState):
        self.controlledStates.pop(ctrlState)

    def calcAntiControl(self, target, context, antiRet):
        if target.isDie() or target.isDestroyed:
            return
        # 如果概率没命中，就不干虾米了
        if antiRet.resultCode == antiRet.RET_NOT_HIT:
            return

        buffLv = 1
        controlStateId = antiRet.controlState
        hitType = self._getConflictPopupIndex(controlStateId)

        skillDamges = context.getCombatResult()
        if not skillDamges:
            LOG_ERR('unexpected anti control context', context)
            skillDamges = combatSkill.SkillDamges(self.id, context.getDmgSourceType(), context.getDmgSourceId())

        # 免疫控制状态 or 控制状态被抵抗
        if (antiRet.resultCode == antiRet.RET_IMMUNE and not target.IsMonster) or antiRet.resultCode == antiRet.RET_ANTI:
            if hitType == gameconst.HitType.Silence:
                skillDamges.damageInfo.append(combatSkill.SkillDamageVal(target.id, 0, gameconst.HitType.AntiSilence))
            else:
                skillDamges.damageInfo.append(combatSkill.SkillDamageVal(target.id, 0, gameconst.HitType.AntiControl))

        # 命中，如果衰减的话要增加控制等级，刷新衰减时间
        elif antiRet.resultCode == antiRet.RET_HIT:
            csVal = self.setCombatControlState(controlStateId, antiRet.antiDuration)
            if antiRet.isDecay:
                csVal.addControlLv(math.ceil(antiRet.controlDuration))
                csVal.refreshAntiTimer(self, controlStateId, antiRet.antiDuration)

            self.addBuffBySkill(target, context, antiRet.controlBuffId, buffLv, 1.0, antiRet.controlDuration)
            if antiRet.dispelBuffTag:
                self.dispelBuffByTag(target, antiRet.dispelBuffTag)

            if hitType == 0:
                return
            skillDamges.damageInfo.append(combatSkill.SkillDamageVal(target.id, 0, hitType))
            # 自己造成控制
            self.onEffectEventCall('onControl', self.id, target.id, effectEventCtx.EE_DEFAULT_CTX)
            # 目标受到控制
            target.onEffectEventCall('onControlBeat', self.id, target.id, effectEventCtx.EE_DEFAULT_CTX)

    def dispelBuffByTag(self, target, tag):
        _buffIdList = []
        for buffId in target.buffMgrDic.keys():
            _buff = target.getBuffByBuffId(buffId)
            if _buff and _buff.hasBuffTag(tag):
                _buffIdList.append(buffId)

        for _buffId in _buffIdList:
            target.removeBuff(_buffId)

    def setTargetHateRecord(self, targetId):
        target = KBEngine.entities.get(targetId)
        if target:
            target.setHateRecord(self.id)

    def unsetTargetHateRecord(self, targetId):
        target = KBEngine.entities.get(targetId)
        if target:
            target.unsetHateRecord(self.id)

    def clearHateRecord(self):
        hateRecord = self.getTempMiscProp(gameconst.EntityPropsEnum.hateRecord)
        if hateRecord:
            self.popTempMiscProp(gameconst.EntityPropsEnum.hateRecord)

    def setHateRecord(self, targetId):
        if not self.hasTempMiscProp(gameconst.EntityPropsEnum.hateRecord):
            self.setTempMiscProp(gameconst.EntityPropsEnum.hateRecord, {})
        hateRecord = self.getTempMiscProp(gameconst.EntityPropsEnum.hateRecord)
        hateRecord[targetId] = int(time.time())
        # self.IsAvatar and not self.isDie() and self.setState(gameconst.StateEnum.Fighting)

    def unsetHateRecord(self, targetId):
        _hateRecord = self.getTempMiscProp(gameconst.EntityPropsEnum.hateRecord)
        if not _hateRecord:
            return
        if targetId in _hateRecord:
            _hateRecord.pop(targetId)

        if not _hateRecord:
            self.clearHateRecord()

    def unsetAllHateRecord(self, unsetReason):
        _hateRecord = self.getTempMiscProp(gameconst.EntityPropsEnum.hateRecord)
        if not _hateRecord:
            return
        for targetId in list(_hateRecord.keys()):
            _target = KBEngine.entities.get(targetId)
            if _target and _target.IsAvatar:
                _target.unsetHateRecord(self.id)

    def removeFightingState(self):
        self.rmFightStateTimeId = 0
        self.removeState(gameconst.StateEnum.Fighting)

    def checkRemoveFightingState(self):
        _hateRecord = self.getTempMiscProp(gameconst.EntityPropsEnum.hateRecord)
        if not _hateRecord:
            return True

        _removeTime = CONST.datas.get('leaveFightStateTime', {}).get('value')
        for _targetId in list(_hateRecord.keys()):
            target = KBEngine.entities.get(_targetId)
            if target and target.IsAvatar and _hateRecord[_targetId] + _removeTime < int(time.time()):
                _hateRecord.pop(_targetId, None)
                target.unsetHateRecord(self.id)

        if not _hateRecord:
            self.clearHateRecord()
            return True

        return False

    def isVisible(self, target):
        if not self.checkCombatRangeY(target):
            return False

        return True

    # 为了让日志更可读以及减少字符拼接开销，必须以 'skillId:%s', skillId 这种形式传入
    def debugCombatMsg(self, *args):
        if gameconfig.enableCombatDebugLog():
            if len(args) <= 1:
                msg = args[0]
            else:
                msg = args[0] % args[1:]
            msg = '[%s][combatDebug] ' % getattr(self, 'name', '') + msg
            LOG_INFO(msg)

    def reliveToPos(self, pos, toDir, hp, context):
        """在指定位置复活

        Arguments:
            pos {position or None} -- 复活位置, 如果为None则在原地位置复活
            hp {int} -- 复活血量, 如果 =0则默认复活, 如果<0则满血复活, 其他情况按血量设置复活
        """
        self._relive()
        self.addBuff(GP_SD.datas["resurrectProtectBuffID"]["value"], 1, self.id)
        _newHp = hp
        if hp == 0:
            _newHp = self.getDefaultReliveHP()
        elif hp < 0 or hp > self.fullHp:
            _newHp = self.fullHp
        self.modifyHP(_newHp, self.id, gameconst.SourceType.SrcTpDefault, self.id)
        if pos:
            self.telToPos(pos, toDir)
        self._trapInViews()

        if self.IsAvatar:
            spaceMgr = self.spaceMgr
            spaceMgr and spaceMgr.onPlayerRelive(self.base, self.gbId)
            self.setState(CCDD.datas.relive)
            self.addTimerCB(CONST.datas['reliveTime']['value'], 'removeState', (CCDD.datas.relive,), gametimer.TIMER_TAG_REMOVE_RELIVE_STATE)

        self.popTempMiscProp(gameconst.EntityPropsEnum.isLightningArea)

    def getDefaultReliveHP(self):
        return max(min(round(1 * 0.01 * self.fullHp), self.fullHp), 1)

    def sendSkillDamage(self, skillDamges):
        _broadcastIdList = []

        for _sVal in skillDamges.damageInfo:
            target = KBEngine.entities.get(_sVal.targetId)
            if target:
                target = utils.getEntityRealEntity(target)
                if target and target.IsAvatar and target.id not in _broadcastIdList:
                    _broadcastIdList.append(target.id)
                    target.client.onSkillDamage(skillDamges)

        _src = KBEngine.entities.get(skillDamges.casterId)
        if _src:
            _src = utils.getEntityRealEntity(_src)
            if _src and _src.IsAvatar and _src.id not in _broadcastIdList:
                _src.client.onSkillDamage(skillDamges)

        if skillDamges.sourceType == gameconst.SourceType.SrcTpSkill:
            _targetIdList = [_sVal.targetId for _sVal in skillDamges.damageInfo if
                            not gameconst.HitType.checkInClientIgnoreList(_sVal.hitType)]
            if len(_targetIdList) > 0:
                _avatarList = [_e for _e in self.getWitnesses() if _e.id not in _broadcastIdList]
                _num = min(20, len(_avatarList))
                _sourceId = skillDamges.sourceId
                for _avatar in random.sample(_avatarList, _num):
                    _avatar.client.onOthersSkillDamage(_sourceId, _targetIdList)

    def pySetWitnessType(self, eId, witnessType):
        self.setWitnessType(eId, witnessType)

    def allClientsCallOnUpdateBuff(self, buffId, buffClientData):
        _ifSend = buff.Buff.getIfSend(buffId)
        if _ifSend:
            self.allClients.onUpdateBuff(buffClientData)
            return

        if self.IsMonster and self.isBoss:
            self.allClients.onUpdateBuff(buffClientData)
            return

        if self.IsAvatar:
            self.client.onUpdateBuff(buffClientData)

        for _e in self.getWitnessesWithName():
            if not (_e and _e.IsAvatar and _e.selectedTargetId == self.id):
                continue

            clientEnt = _e.clientEntity(self.id)
            if not clientEnt:
                continue

            clientEnt.onUpdateBuff(buffClientData)

    def allClientsOnAddBuff(self, buffId, buffClientData):
        _ifSend = buff.Buff.getIfSend(buffId)
        if _ifSend:
            self.allClients.onAddBuff(buffClientData)
            return

        if self.IsMonster and self.isBoss:
            self.allClients.onAddBuff(buffClientData)
            return

        if self.IsAvatar:
            self.client.onAddBuff(buffClientData)

        for _e in self.getWitnessesWithName():
            if not (_e and _e.IsAvatar and _e.selectedTargetId == self.id):
                continue

            clientEnt = _e.clientEntity(self.id)
            if not clientEnt:
                continue

            clientEnt.onAddBuff(buffClientData)

    def allClientsOnRemoveBuff(self, buffId, removedKeys):
        _ifSend = buff.Buff.getIfSend(buffId)
        if _ifSend:
            self.allClients.onRemoveBuff(buffId, removedKeys)
            return

        if self.IsMonster and self.isBoss:
            self.allClients.onRemoveBuff(buffId, removedKeys)
            return

        if self.IsAvatar:
            self.client.onRemoveBuff(buffId, removedKeys)

        for _e in self.getWitnessesWithName():
            if not (_e and _e.IsAvatar and _e.selectedTargetId == self.id):
                continue

            clientEnt = _e.clientEntity(self.id)
            if not clientEnt:
                continue

            clientEnt.onRemoveBuff(buffId, removedKeys)

    def resetTargetTypeCache(self, entities):
        for _target in entities:
            self.removeTargetTypeCache(_target)
            utils.isEnemy(self, _target)
            utils.isFriend(self, _target)

            if _target.id not in list(self.cacheSelfSet):
                continue

            _target.removeTargetTypeCache(self)
            utils.isEnemy(_target, self)
            utils.isFriend(_target, self)

        self.checkRemoveBuffAfterTargetTypeChanged()
        self.allChildrenResetTargetTypeCache(entities)

    def resetAllTargetTypeCache(self, updateImmediately=True):
        if self.IsAvatar:
            self.guildRelationVersion = gameglobal.guildRelationVersion

        cacheIds = self.enemiesCacheSet.union(self.notEnemiesCacheSet, self.friendsCacheSet, self.notFriendsCacheSet)
        self.enemiesCacheSet.clear()
        self.notEnemiesCacheSet.clear()
        self.friendsCacheSet.clear()
        self.notFriendsCacheSet.clear()

        if updateImmediately:
            for _eid in cacheIds:
                target = KBEngine.entities.get(_eid)
                if not target:
                    LOG_WARN("resetAllTargetTypeCache target is None", _eid)
                    continue

                utils.isEnemy(self, target)
                utils.isFriend(self, target)

            for _eid in list(self.cacheSelfSet):
                target = KBEngine.entities.get(_eid)
                if not target:
                    LOG_WARN("resetAllTargetTypeCache cacheSelfSet target is None", _eid)
                    continue

                target.removeTargetTypeCache(self)
                utils.isEnemy(target, self)
                utils.isFriend(target, self)

        self.checkRemoveBuffAfterTargetTypeChanged()
        self.allChildrenResetAllTargetTypeCache()

    def checkCacheTargetType(self):
        _allCacheSetLen = len(self.enemiesCacheSet) + len(self.notEnemiesCacheSet)
        if _allCacheSetLen > 30:
            return
        _needRefreshList = []
        for eId in list(self.enemiesCacheSet):
            target = KBEngine.entities.get(eId)
            if not target:
                LOG_WARN("checkCacheTargetType  error1", eId)
                self.enemiesCacheSet.remove(eId)
            elif not utils._isEnemy(self, target):
                LOG_WARN("checkCacheTargetType enemy cache error", eId)
                _needRefreshList.append(target)

        for eId in list(self.notEnemiesCacheSet):
            target = KBEngine.entities.get(eId)
            if not target:
                LOG_WARN("checkCacheTargetType  error2", eId)
                self.notEnemiesCacheSet.remove(eId)
            elif utils._isEnemy(self, target):
                LOG_WARN("checkCacheTargetType not enemy cache error", eId)
                _needRefreshList.append(target)

        for eId in list(self.friendsCacheSet):
            target = KBEngine.entities.get(eId)
            if not target:
                LOG_WARN("checkCacheTargetType  error3", eId)
                self.friendsCacheSet.remove(eId)
            elif not utils._isFriend(self, target):
                LOG_WARN("checkCacheTargetType friend cache error", eId)
                _needRefreshList.append(target)

        for eId in list(self.notFriendsCacheSet):
            target = KBEngine.entities.get(eId)
            if not target:
                LOG_WARN("checkCacheTargetType  error4", eId)
                self.notFriendsCacheSet.remove(eId)
            elif utils._isFriend(self, target):
                LOG_WARN("checkCacheTargetType not friend cache error", eId)
                _needRefreshList.append(target)

        if len(_needRefreshList) > 0:
            self.resetTargetTypeCache(_needRefreshList)

    def resetTargetTypeCacheFlag(self):
        self.stopCacheTargetTypeTimerId = 0
        self.useTargetTypeCacheFlag = False
        self.doClearAllTargetTypeCache()

    def doClearAllTargetTypeCache(self, bClearOthersCache=False):
        allCacheSet = self.enemiesCacheSet.union(self.notEnemiesCacheSet, self.friendsCacheSet, self.notFriendsCacheSet)
        self.enemiesCacheSet.clear()
        self.notEnemiesCacheSet.clear()
        self.friendsCacheSet.clear()
        self.notFriendsCacheSet.clear()
        for eId in allCacheSet:
            target = KBEngine.entities.get(eId)
            if not target:
                LOG_WARN("doClearAllTargetTypeCache target is None in allCacheSet", eId)
                continue
            target.cacheSelfSet.remove(self.id)

        if not bClearOthersCache:
            return

        for _eid in list(self.cacheSelfSet):
            _target = KBEngine.entities.get(_eid)
            if not _target:
                LOG_WARN("doClearAllTargetTypeCache _target is None in cacheSelfSet", _eid)
                self.cacheSelfSet.remove(_eid)
                continue

            _target.removeTargetTypeCache(self)

    def removeTargetTypeCache(self, target):
        self.enemiesCacheSet.discard(target.id)
        self.notEnemiesCacheSet.discard(target.id)
        self.friendsCacheSet.discard(target.id)
        self.notFriendsCacheSet.discard(target.id)
        target.cacheSelfSet.discard(self.id)

    def allChildrenResetAllTargetTypeCache(self):
        for _summonId in self.petList:
            summon = KBEngine.entities.get(_summonId)
            if not summon:
                continue

            summon.resetAllTargetTypeCache()

        for _cid in self.cloneList:
            c = KBEngine.entities.get(_cid)
            if not c:
                continue

            c.resetAllTargetTypeCache()

        for _cid in self.creationList:
            creation = KBEngine.entities.get(_cid)
            if not creation:
                continue

            creation.resetAllTargetTypeCache()

    def allChildrenResetTargetTypeCache(self, entities):
        for _summonId in self.petList:
            summon = KBEngine.entities.get(_summonId)
            if not summon:
                continue
            
            summon.resetTargetTypeCache(entities)

        for _cid in self.cloneList:
            c = KBEngine.entities.get(_cid)
            if not c:
                continue

            c.resetTargetTypeCache(entities)

        for _cid in self.creationList:
            creation = KBEngine.entities.get(_cid)
            if not creation:
                continue

            creation.resetTargetTypeCache(entities)

    def tagDispelAll(self, tag):
        self.removeBuffByTag(tag)

    def onTimer(self, tid, userData):
        self._onTimerTrigger(tid, userData)
        if userData == gametimer.TIMER_AURA_LOOP:
            self.auraDic._onLoop(self, tid)
            return

        if userData == gametimer.CHECK_TARGET_TYPE_TIMER:
            self.checkCacheTargetType()
            return
        
        if userData == gametimer.TIMER_CHECK_SHIELD:
            self.checkShield()
            return

        super(SkillManager, self).onTimer(tid, userData)

    def deathCreateCollection(self, radius, numProb, collectionIdProb, disappearTime, extra=None):
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
        
        if self.IsMonster and self.isFirstBloodMonster:
            posList = [extra.get('FBPos', self.position)]

        for i in range(createNum):
            collectionIdList = []
            collectionIdWeightList = []
            for weight, collectionId in collectionIdProb:
                collectionIdList.append(collectionId)
                collectionIdWeightList.append(weight)

            collectionId = utils.weightChoices(collectionIdList, collectionIdWeightList)[0][0]
            _pos = posList[i] if i < len(posList) else self.position
            

            _props = {
                'collectionId': collectionId,
                'spaceNo': self.spaceNo,
                'position': _pos,
                'direction': self.direction,
                'disappearTime': utils.curTS() + disappearTime
            }
            if self.spaceMgr:
                _props['spaceMgrId'] = self.spaceMgr.id
                _props['spaceMgrBox'] = self.spaceMgr.base

            if extra:
                _props.update(extra)
                if self.IsMonster:
                    if self.isFirstBloodMonster:
                        if _props.get('needFBTarget'):
                            FBtar = KBEngine.entities.get(self.FirstBloodTargetId)
                            if FBtar:
                                FBMembers = FBtar.getAllTeamMemberGbIdSet()
                                FBMembers.update(FBtar.getAllRaidMemberGbIdSet())
                                FBMembers.add(FBtar.gbId)
                                _props['firstBloodTargetGbIds'] = FBMembers
                                _props['fBItemId'] = extra.get('FBItemId', 0)
                                _props['fromMonsterId'] = extra.get('fromMonsterId', 0)

            LOG_INFO("deathCreateCollection", _props)
            KBEngine.createEntity('Collection', self.spaceID, _pos, self.direction, _props)

    def deathCreateCollectionByList(
            self, radius, collectionIdProb, 
            disappearTime, posType=gameconst.DEATH_COLL_POS_TYPE_SELF_POS, 
            fixedPos=None):

        createNum = 0
        boxRadius = 0
        for (num, collectionId) in collectionIdProb:
            createNum += num
            boxRadius = max(boxRadius, NPD.datas.get(collectionId, {}).get('chestRadius', 0))

        if posType == gameconst.DEATH_COLL_POS_TYPE_SELF_POS:
            _targetPos = self.position
        elif posType == gameconst.DEATH_COLL_POS_TYPE_FIXED_POS:
            _targetPos = fixedPos
        else:
            LOG_ERR('invalid pos type', posType)
            return

        posList = self.getRandomPositionByBoxRadius(_targetPos, radius, boxRadius, createNum)

        idx = 0
        for (num, collectionId) in collectionIdProb:
            for i in range(num):
                _pos = posList[idx] if i < len(posList) else self.position
                idx += 1
                _props = {
                    'collectionId': collectionId,
                    'spaceNo': self.spaceNo,
                    'position': _pos,
                    'direction': self.direction,
                    'disappearTime': utils.curTS() + disappearTime
                }
                if self.spaceMgr:
                    _props['spaceMgrId'] = self.spaceMgr.id
                    _props['spaceMgrBox'] = self.spaceMgr.base

                KBEngine.createEntity('Collection', self.spaceID, _pos, self.direction, _props)

    def breakSkillByState(self, ignoreTag=0):
        usingSkills = self.getTempMiscProp(gameconst.EntityPropsEnum.currentUseSkill, default={})
        for sid in list(usingSkills.keys()):
            if sid not in usingSkills:
                continue

            if ignoreTag and utils.hasSkillTagById(sid, ignoreTag):
                continue
            
            sVal, tid = usingSkills[sid]
            sVal.useSkillDone(self, 0, [], isSucc=False, doRemoveState=True, forceResetSkill=True)

    def getAvatar(self):
        _host = utils.getHostEntity(self)
        if _host and (_host.IsAvatar or _host.IsAvatarReplica):
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

    def forbidSkillByTags(self, tags):
        LOG_DBG("forbidSkillByTags1", tags, self.skillForbidTagDic)
        beUpdate = False
        for tag in tags:
            if tag not in self.skillForbidTagDic:
                self.skillForbidTagDic.setdefault(tag, 0)
                beUpdate = True
            self.skillForbidTagDic[tag] += 1

        LOG_DBG("forbidSkillByTags2", tags, self.skillForbidTagDic)
        self.notifyUpdateForbidSkills(beUpdate)

    def unForbidSkillByTags(self, tags):
        LOG_DBG("unForbidSkillByTags1", tags, self.skillForbidTagDic)
        beUpdate = False
        for tag in tags:
            if tag not in self.skillForbidTagDic:
                continue
            self.skillForbidTagDic[tag] -= 1
            if self.skillForbidTagDic[tag] > 0:
                continue
            self.skillForbidTagDic.pop(tag, None)
            beUpdate = True

        LOG_DBG("unForbidSkillByTags2", tags, self.skillForbidTagDic)
        self.notifyUpdateForbidSkills(beUpdate)

    def notifyUpdateForbidSkills(self, beUpdate):
        if not self.IsAvatar:
            return
        if not beUpdate:
            return

        forbidTags = list(self.skillForbidTagDic.keys())
        LOG_DBG("notifyUpdateForbidSkills", forbidTags)
        self.client.updateForbidSkillTags(forbidTags)

    def checkForbidSkill(self, skillId):
        tags = combatSkill.SkillBaseClass.getTag(skillId)
        for tag in tags:
            if tag not in self.skillForbidTagDic:
                continue
            return True
        return False 

    def addDamageRatioLimit(self, limitInfo):
        infoDict = self.getTempMiscProp(gameconst.EntityPropsEnum.damageRatioLimit, {})
        LOG_DBG("addDamageRatioLimit", limitInfo, infoDict)
        for (_type, _ratio) in limitInfo:
            if _type not in gameconst.EntityType.VALID_ENTITY_TYPE:
                continue
            if _ratio < 0 or type(_ratio) is not int:
                LOG_ERR("addDamageRatioLimit error", limitInfo)
                continue

            limitList = infoDict.setdefault(_type, [])
            limitList.append(_ratio)
            limitList.sort()

        self.setTempMiscProp(gameconst.EntityPropsEnum.damageRatioLimit, infoDict)
        LOG_DBG("addDamageRatioLimit", infoDict)

    def removeDamageRatioLimit(self, limitInfo):
        infoDict = self.getTempMiscProp(gameconst.EntityPropsEnum.damageRatioLimit, {})
        LOG_DBG("removeDamageRatioLimit", limitInfo, infoDict)
        for (_type, _ratio) in limitInfo:
            if _type not in gameconst.EntityType.VALID_ENTITY_TYPE:
                continue
            if _ratio < 0 or type(_ratio) is not int:
                LOG_ERR("removeDamageRatioLimit error", limitInfo)
                continue

            limitList = infoDict.setdefault(_type, [])
            if _ratio not in limitList:
                continue
            limitList.remove(_ratio)

        self.setTempMiscProp(gameconst.EntityPropsEnum.damageRatioLimit, infoDict)
        LOG_DBG("removeDamageRatioLimit", infoDict)

    def getEntityDamageRatioLimit(self, eType):
        infoDict = self.getTempMiscProp(gameconst.EntityPropsEnum.damageRatioLimit, {})
        LOG_DBG("getEntityDamageRatioLimit", eType, infoDict)
        if eType not in gameconst.EntityType.VALID_ENTITY_TYPE:
            return False, 0

        limitList = infoDict.setdefault(eType, [])
        beLimit = len(limitList) > 0
        return beLimit, limitList[0] if beLimit else 0
