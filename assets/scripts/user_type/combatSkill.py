# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine

import time
import random
import math
import gameconst
import sMath
import Math
import effectEventCtx
import actionContext
import utils
import userType
import gameengine
import weakref

import skill_skill as S_SD
import conflict_conflict_def as C_C_DD
import conflict_status as C_SD
import fx_fx as FF
import const_const as C_CD
import skillRelevant_skillConst as SRSC
import gameclass
import functools
import gametimer
import gameconst


class ServerSkills(userType.UserDictType):
    """SERVER_SKILLS"""

    def __init__(self):
        self.skillSwitches = {}

    def doAddSkill(self, owner, skillId, skillLv, **kwargs):
        if skillId in self:
            return self[skillId]

        _skillClass = fetchSkillClass(skillId)
        self[skillId] = _skillClass(skillId, skillLv, **kwargs)
        # 初始默认都是开启的
        if skillId not in self.skillSwitches:
            switchStatus = gameconst.SkillSwitchStatus.AUTO
            # 针对玩家的技能释放处理
            if owner.IsAvatar:
                # autoFightUseSkill设置1表示不会自动释放
                if S_SD.datas.get(skillId, {}).get("autoFightUseSkill", 0) == gameconst.SkillSwitchStatus.MANUAL:
                    switchStatus = gameconst.SkillSwitchStatus.MANUAL
                LOG_DBG("initial skill switch status 0 ", skillId, switchStatus)
            self.skillSwitches[skillId] = switchStatus

        return self[skillId]

    def doRemoveSkill(self, skillId):
        self.pop(skillId, None)

    def doGetSkill(self, skillId, reportErr=True):
        _skill = self.get(skillId, None)
        if not _skill and reportErr:
            gameengine.panicStack('doGetSkill with out skillId', skillId)
            return None

        return _skill

    def getClientData(self, owner):
        _skills = []
        _skillCDStatus = []
        for _skillId, skillInstance in self.items():
            skillDict = {
                'skillId': _skillId,
                'tNextCast': skillInstance.tNextCast,
                'skillCd': skillInstance.getCDDur(owner),
                'extraSkillLv': skillInstance.getExtraLevel(owner),
            }
            _skills.append(skillDict)
            # 技能CD状态
            cdStatus = skillInstance.getTempData(gameconst.SkillTempDataKey.CHANGE_SKILL_CD_STATUS, gameconst.SkillCDStatus.DEFAULT)
            if cdStatus != gameconst.SkillCDStatus.DEFAULT:
                skillCDStatu = {
                    'skillId': _skillId,
                    'cdStatus': cdStatus
                }
                _skillCDStatus.append(skillCDStatu)

        skillSwitches = []
        for _skillId, skillSwitch in self.skillSwitches.items():
            skillDict = {
                'skillId':_skillId,
                'switchStatus':skillSwitch
            }
            skillSwitches.append(skillDict)

        _clientData = {
            'skills': _skills,
            'skillSwitches': skillSwitches,
            'skillCDStatus': _skillCDStatus,
        }
        return _clientData

    def toDict(self):
        _skillDict = {'skills': []}
        for _skillId, sVal in self.items():
            sDict = {
                'skillId': _skillId,
                'skillLv': sVal.skillLv,
                'tNextCast': float(sVal.tNextCast),
                'cdDelta': float(sVal.cdDelta),
            }
            _skillDict['skills'].append(sDict)

        _skillDict['skillSwitches'] = self.skillSwitches
        return _skillDict

    def toReplicaSkillDict(self):
        _skillDict = {'skills': []}
        for _skillId, sVal in self.items():
            sDict = {
                'skillId': _skillId,
                'skillLv': sVal.skillLv,
                #'tNextCast': float(sVal.tNextCast),
                #'cdDelta': float(sVal.cdDelta),
            }
            _skillDict['skills'].append(sDict)
        return _skillDict
    
    def checkSkillSwitch(self, skillID, status):
        switchStatus = self.skillSwitches.get(skillID, None)
        if switchStatus is None:
            return False
        return switchStatus == status

    def getSkillSwitch(self, skillID):
        return self.skillSwitches.get(skillID, gameconst.SkillSwitchStatus.AUTO)

    def setSkillSwitch(self, owner, skillID, status):
        skillID, _ = owner.glyphEquipData.getInscriptionSrcSkillId(skillID)
        if not S_SD.datas.get(skillID, None):
            LOG_ERR("setSkillSwitch illeagal skill id", skillID, status)
            return
        if status not in gameconst.SkillSwitchStatus.VALID_STATUS:
            LOG_ERR("setSkillSwitch illeagal switch status", skillID, status)
            return
        self.skillSwitches[skillID] = status

    def _lateReload(self):
        super(ServerSkills, self)._lateReload()
        for _v in self.values():
            _v.reloadScript()


class SkillDamageVal(userType.UserSingleType):
    def __init__(self, targetId, hurt, hitType):
        self.hurt = int(hurt)
        self.targetId = targetId
        self.hitType = hitType


class SkillDamges(userType.UserSingleType):
    def __init__(self, casterId=0, sourceType=0, sourceId=0, damageInfo=None, **args):
        self.sourceId = sourceId
        self.casterId = casterId
        self.damageInfo = damageInfo or []
        self.sourceType = sourceType

    def _lateReload(self):
        super(SkillDamges, self)._lateReload()

        for _v in self.damageInfo:
            _v.reloadScript()


class DamageResult(userType.UserSingleType):
    def __init__(self, dmg=0, hpSuck=0, atkType=0, calcShield=True, hurtDmg=0, **kwargs):
        self.dmg = dmg  # 输出伤害
        self.atkType = atkType
        self.hpSuck = hpSuck
        self.calcShield = calcShield
        self.hurtDmg = hurtDmg  # 受伤害值，用于承伤统计，实际结算数值用dmg


class HealResult(userType.UserSingleType):
    def __init__(self, healVal=0, isCrit=False, doSkillHealCorrection=False):
        self.isCrit = isCrit
        self.healVal = healVal
        self.doSkillHealCorrection = doSkillHealCorrection


class AntiControlResult(userType.UserSingleType):
    RET_NOT_HIT = 0
    RET_HIT = 1
    RET_IMMUNE = 2
    RET_ANTI = 3

    def __init__(self, resultCode=RET_NOT_HIT, isDecay=False, controlState=-1, controlBuffId=0, controlDuration=0,
                 dispelBuffTag=0, antiDuration=20):
        self.controlState = controlState
        self.resultCode = resultCode
        self.controlBuffId = controlBuffId
        self.isDecay = isDecay
        self.controlDuration = controlDuration
        self.antiDuration = antiDuration
        self.dispelBuffTag = dispelBuffTag


class ControlState(userType.UserSingleType):
    def __init__(self, controlLevel, tStart):
        self.controlLevel = controlLevel
        self.tStart = tStart
        self.removeTimerId = 0

    def refreshAntiTimer(self, owner, antiCtrlState, antiDuration):
        if self.removeTimerId:
            owner.cancelTimerCB(self.removeTimerId, gametimer.TIMER_TAG_REMOVE_COMBAT_CONTROL_STATE)

        self.removeTimerId = owner.addTimerCB(antiDuration, 'removeCombatControlState', (antiCtrlState,),
                                             gametimer.TIMER_TAG_REMOVE_COMBAT_CONTROL_STATE)

    def addControlLv(self, val):
        self.controlLevel = int(self.controlLevel + val)

    def resetTimerId(self):
        self.removeTimerId = 0


class SkillBaseClass(userType.UserSingleType):
    def __init__(self, skillId, skillLv, tNextCast=0.0, cdDelta=0.0, parentSkill=0, targetIds=None, **kwargs):
        self.skillLv = int(skillLv)
        self.skillId = skillId
        self.tNextCast = tNextCast
        self.parentSkill = parentSkill
        self.cdDelta = cdDelta
        self.targetIds = targetIds or []
        self.tempData = {}
        self.isInSkill = False


    def _lateReload(self):
        super(SkillBaseClass, self)._lateReload()
        if not self.parentSkill:
            return

        self.parentSkill.reloadScript()

    @classmethod
    def clearAllCache(cls):
        cls.getTag.cache_clear()
        cls.getSkillCfg.cache_clear()
        cls.getAction.cache_clear()
        cls.getDeactivateAction.cache_clear()
        cls.getActivateAction.cache_clear()
        cls.getMaxTargetData.cache_clear()
        cls.getChannelTime.cache_clear()
        cls.getCastingtimeMax.cache_clear()
        cls.getInterruptByAttack.cache_clear()
        cls.getScope.cache_clear()
        cls.getScopeData.cache_clear()
        cls.getMpPerSec.cache_clear()
        cls.getCostMpData.cache_clear()
        cls.getRangeData.cache_clear()
        cls.getFxDelay.cache_clear()
        cls.getBulletFx.cache_clear()
        cls.getSkillTime.cache_clear()
        cls.getBulletFxTime.cache_clear()
        cls.isAttackSkill.cache_clear()
        cls.getSkillHateRatio.cache_clear()
        cls.getCategory.cache_clear()
        cls.getBulletTimeScale.cache_clear()
        cls.getSkillSchoolTag.cache_clear()
        cls.getSkillName.cache_clear()
        cls.getTarget.cache_clear()
        cls.getStartAction.cache_clear()
        cls.getEffectTargetType.cache_clear()
        cls.getEndAction.cache_clear()
        cls.isMovingSkill.cache_clear()
        cls.getPriority.cache_clear()
        cls.getSkillLvParam.cache_clear()
        cls.getSkillEvent.cache_clear()

    def getSkillId(self):
        return self.skillId

    def getLevel(self, owner):
        # NOTE(): 玩法如果涉及到增加技能等級時需要自行存儲管理增加的技能等級, 並按照如下步驟接入
        #  1. 在 AvatarCell.getExtraSkillLv 中增加涉及到自己的等級
        #  2. 在完成等級设置后通过如下接口下发给客户端 Avatar.client.updateSkillsExtraLevel
        #     2.1. API: updateSkillsExtraLevel 来源src 技能IDList(如果全局请填写: [gameconst.ClassSkillID, ]) 技能levelList(如果全局请填写: [exLvl, ])
        #  3. 在AvatarCell.initClientOnCell 中调用 Avatar.client.onGetSkillsExtraLevel 将等级数据下发给客户端
        #     3.1. 注意: 该调用必须在 Avatar.client.sendSkillBuilds 前调用
        return min(self.skillLv + self.getExtraLevel(owner), int(SRSC.datas['sp_skillMaxLevel']['valueCN']))

    def getExtraLevel(self, owner):
        if not owner.IsAvatar:
            return 0
        # 被动技能替换的技能需要从原技能中获取额外的技能等级
        _relatedSkills = S_SD.datas.get(self.skillId, {}).get('conflictSkill') or ()
        _maxExtraSkillLv = owner.getExtraSkillLv(self.skillId)
        for _sid in _relatedSkills:
            if _maxExtraSkillLv < owner.getExtraSkillLv(_sid):
                _maxExtraSkillLv = owner.getExtraSkillLv(_sid)
        return _maxExtraSkillLv

    def setSkillLevel(self, skillLevel):
        self.skillLv = int(skillLevel)

    @staticmethod
    @functools.lru_cache(1024)
    def getSkillCfg(skillId):
        return S_SD.datas[skillId]

    @staticmethod
    @functools.lru_cache(1024)
    def getSkillEvent(skillId):
        return SkillBaseClass.getSkillCfg(skillId).get('skillEvent', 0)

    @staticmethod
    @functools.lru_cache(1024)
    def getPriority(skillId):
        return SkillBaseClass.getSkillCfg(skillId).get('priority', 0)

    @staticmethod
    @functools.lru_cache(1024)
    def getTag(skillId):
        _tags = SkillBaseClass.getSkillCfg(skillId).get('tag')
        if not _tags:
            return ()
        elif type(_tags[0]) is tuple:
            return _tags[0]
        else:
            return _tags

    def getGlobalCD(self, owner):
        _gcd = self.getSkillCfg(self.skillId).get('globalCD', 0)
        return _gcd * (1 + owner.mulGCD)

    def getCDDur(self, owner):
        _cd = self.getSkillCfg(self.skillId).get('CD', 0)

        if isinstance(_cd, tuple) or isinstance(_cd, list):
            _lv = self.getLevel(owner) - 1
            if 0 <= _lv < len(_cd):
                cd = _cd[_lv]
            else:
                cd = _cd[-1]

        elif _cd is None:
            cd = 0

        else:
            cd = _cd

#         【【战斗】技能冷却加速属性没生效】
# https://www.tapd.cn/tapd_fe/59721401/bug/detail/1159721401001004163
        #realCD = (cd + owner.adjCD) * (1 + owner.mulCD) + self.cdDelta'
        realCD = cd * (1 - owner.skillCD) + self.cdDelta
        realCD = sMath.limit(realCD, 0.1, 999999)
        gcd = self.getGlobalCD(owner)
        totalCD = max(realCD, gcd)
        host = owner.getAvatar()
        LOG_DBG("in getCDDur ", owner, self.skillId, owner.IsAvatar, host)
        if host:
            addValue = 0
            ret, datas = host.getInscriptionEffects(self.skillId, gameconst.InscriptionEffectType.MODIFY_CD)
            if ret:
                if len(datas) == 1:
                    addValue = datas[0]
                    LOG_DBG("in getCDDur, inscription effect is triggered, skill_id:{0}, effect_type{1}, effect_value{2}", self.skillId, gameconst.InscriptionEffectType.MODIFY_CD, datas)
            totalCD -= addValue
            if totalCD < 0:
                totalCD = 0
            if totalCD > 0:
                ret, datas = host.getInscriptionEffects(self.skillId, gameconst.InscriptionEffectType.REFRESH_CD)
                if ret:
                    if len(datas) == 1:
                        addValue = datas[0]
                        if random.uniform(0, 1) <= addValue:
                            totalCD = 0
                            LOG_DBG("in getCDDur, inscription effect is triggered, skill_id:{0}, effect_type{1}, effect_value{2}", self.skillId, gameconst.InscriptionEffectType.REFRESH_CD, datas)
        return totalCD

    # 修改cd时长
    def changeCD(self, owner, delta):
        owner.debugCombatMsg("SkillBaseClass changeCD: skillId:%s, delta:%s, inCDTime:%s", self.getSkillId(), delta, self.inCDTime())
        self.cdDelta += delta

        if not owner.IsAvatar:
            return

        owner.client.onSetAddSkillCd(
            self.skillId, 
            float(self.getCDDur(owner)), 
            float(self.tNextCast),
            False, 
            self.getTempData(gameconst.SkillTempDataKey.RELEASE_TIME, 0), 
            self.getTempData(gameconst.SkillTempDataKey.TOTAL_RELEASE_CNT, 0), 
            self.getTempData(gameconst.SkillTempDataKey.RELEASED_CNT, 0), 
            not self.isSkillCDStatusFrozen())
            
    # 修改本次cd的结束时间点
    def changeNextCast(self, owner, delta):
        self.tNextCast += delta
        realCD = self.tNextCast - time.time() if self.tNextCast > time.time() else self.getCDDur(owner)
        if owner.IsAvatar:
            owner.client.onSetAddSkillCd(
                self.skillId, 
                float(realCD), 
                float(self.tNextCast),
                False, 
                self.getTempData(gameconst.SkillTempDataKey.RELEASE_TIME, 0), 
                self.getTempData(gameconst.SkillTempDataKey.TOTAL_RELEASE_CNT, 0), 
                self.getTempData(gameconst.SkillTempDataKey.RELEASED_CNT, 0), 
                not self.isSkillCDStatusFrozen())

    def inCDTime(self):
        return True if time.time() < self.tNextCast else False

    def canRemoveFromBuild(self):
        return not self.inCDTime()

    def fetchLastCDTime(self):
        _t = time.time() 
        if _t < self.tNextCast:
            return self.tNextCast - _t
        else:
            return 0

    @staticmethod
    @functools.lru_cache(1024)
    def getAction(skillId):
        return SkillBaseClass.getSkillCfg(skillId).get('action', '')

    @staticmethod
    @functools.lru_cache(1024)
    def getActivateAction(skillId):
        return SkillBaseClass.getSkillCfg(skillId).get('activateAction')

    @staticmethod
    @functools.lru_cache(1024)
    def getDeactivateAction(skillId):
        return SkillBaseClass.getSkillCfg(skillId).get('deactivateAction')

    @staticmethod
    @functools.lru_cache(1024)
    def getCastingtimeMax(skillId):
        return float(SkillBaseClass.getSkillCfg(skillId).get('castingTime') or 0)

    @staticmethod
    @functools.lru_cache(1024)
    def getMaxTargetData(skillId):
        return SkillBaseClass.getSkillCfg(skillId).get('maxTargetNum', 0)

    def getMaxTargetNum(self, owner, skillId, context):
        defaultMaxTagretNum = self.getMaxTargetData(skillId)
        host = owner.getAvatar()
        #LOG_DBG("in getMaxTargetNum 1", owner, skillId, owner.IsAvatar, host, context)
        if host:
            ret, datas = host.getInscriptionEffects(skillId, gameconst.InscriptionEffectType.ATTACK_TARGET_ADD_VALUE)
            if ret:
                if len(datas) == 1:
                    addValue = datas[0]
                    defaultMaxTagretNum += addValue
                    LOG_DBG("in getMaxTargetNum 2, inscription effect is triggered, skill_id:{0}, effect_type{1}, effect_value{2}", skillId, gameconst.InscriptionEffectType.ATTACK_TARGET_ADD_VALUE, datas)
            else:
                if context:
                    ctx = context.getTopCtxFromActionQueue(actionContext.ACTION_USE_SKILL)
                    if ctx:
                        ret, datas = host.getInscriptionEffects(ctx.skillId, gameconst.InscriptionEffectType.ATTACK_TARGET_ADD_VALUE)
                        if ret:
                            if len(datas) == 1:
                                addValue = datas[0]
                                defaultMaxTagretNum += addValue
                                LOG_DBG("in getMaxTargetNum 3, inscription effect is triggered, skill_id:{0}, effect_type{1}, effect_value{2}", skillId, gameconst.InscriptionEffectType.ATTACK_TARGET_ADD_VALUE, datas)
        return defaultMaxTagretNum

    @staticmethod
    @functools.lru_cache(1024)
    def getChannelTime(skillId):
        return SkillBaseClass.getSkillCfg(skillId).get('channelTime', 0)

    @staticmethod
    @functools.lru_cache(1024)
    def getInterruptByAttack(skillId):
        return SkillBaseClass.getSkillCfg(skillId).get('interrupt', 0)

    @staticmethod
    @functools.lru_cache(1024)
    def getScope(skillId):
        return SkillBaseClass.getSkillCfg(skillId).get('scope') or 0

    @staticmethod
    @functools.lru_cache(1024)
    def getScopeData(skillId):
        return SkillBaseClass.getSkillCfg(skillId).get('scopeParam', '')

    def getScopeParam(self, owner, skillId, context):
        _scopeParam = self.getScopeData(skillId)
        if not _scopeParam:
            return None, None
        else:
            _scopeParam = eval(_scopeParam) if isinstance(_scopeParam, (str, bytes)) else _scopeParam
            if type(_scopeParam) not in (list, tuple):
                _scopeParam = (_scopeParam,)
            host = owner.getAvatar()
            LOG_DBG("in getScopeParam 1 ", owner, skillId, owner.IsAvatar, host)
            if host:
                ret, datas = host.getInscriptionEffects(skillId, gameconst.InscriptionEffectType.SKILL_RELEASE_RANGE_ADD_VALUE)
                if ret:
                    if len(datas) == 1:
                        LOG_DBG("in getScopeParam 2", owner, skillId, owner.IsAvatar, host, _scopeParam, datas)
                        return _scopeParam, datas[0]
                else:
                    if context:
                        ctx = context.getTopCtxFromActionQueue(actionContext.ACTION_USE_SKILL)
                        if ctx:
                            ret, datas = host.getInscriptionEffects(ctx.skillId, gameconst.InscriptionEffectType.SKILL_RELEASE_RANGE_ADD_VALUE)
                            if ret:
                                if len(datas) == 1:
                                    LOG_DBG("in getScopeParam 3", owner, skillId, owner.IsAvatar, host, _scopeParam, datas)
                                    return _scopeParam, datas[0]
            return _scopeParam, None

    @staticmethod
    @functools.lru_cache(1024)
    def getCostMpData(skillId):
        return SkillBaseClass.getSkillCfg(skillId).get('consumeMp') or 0

    def getCostMp(self, owner, skillId, factor):
        _mp = self.getCostMpData(skillId)
        if isinstance(_mp, tuple) or isinstance(_mp, list):
            _lv = self.getLevel(owner) - 1
            if 0 <= _lv < len(_mp):
                mp = _mp[_lv]
            else:
                mp = _mp[-1]
        elif _mp is None:
            mp = 0
        else:
            mp = _mp

        originalConsumeMP = mp
        host = owner.getAvatar()
        LOG_DBG("in getCostMp ", owner, skillId, owner.IsAvatar, host)
        if host:
            if originalConsumeMP > 0:
                ret, datas = host.getInscriptionEffects(skillId, gameconst.InscriptionEffectType.MANA_DECREASE_VALUE)
                if ret:
                    if len(datas) == 1:
                        addValue = datas[0]
                        if addValue >= originalConsumeMP:
                            originalConsumeMP = 0
                        else:
                            originalConsumeMP -= addValue
                        LOG_DBG("in getCostMp, inscription effect is triggered, skill_id:{0}, effect_type{1}, effect_value{2}", skillId, gameconst.InscriptionEffectType.MANA_DECREASE_VALUE, datas)
        return factor * float(originalConsumeMP)

    @staticmethod
    @functools.lru_cache(1024)
    def getMpPerSec(skillId):
        return SkillBaseClass.getSkillCfg(skillId).get('mpPerSec')

    @staticmethod
    @functools.lru_cache(1024)
    def getRangeData(skillId):
        # 兼容下老配置
        rangeData = SkillBaseClass.getSkillCfg(skillId).get('range')
        if isinstance(rangeData, (float, int)):
            return (rangeData,)
        if not rangeData:
            return (0,)
        return rangeData

    def getRange(self, owner, skillId, skillLv=1):
        rangeData = self.getRangeData(skillId)
        defaultRange = rangeData[-1] if skillLv > len(rangeData) else rangeData[skillLv - 1]
        host = owner.getAvatar()
        LOG_DBG("in getRange ", owner, skillId, owner.IsAvatar, host)
        if host:
            ret, datas = host.getInscriptionEffects(skillId, gameconst.InscriptionEffectType.SKILL_RELEASE_DISTANCE_ADD_VALUE)
            if ret:
                if len(datas) == 1:
                    addValue = datas[0]
                    defaultRange += addValue
                    LOG_DBG("in getRange, inscription effect is triggered, skill_id:{0}, effect_type{1}, effect_value{2}", self.skillId, gameconst.InscriptionEffectType.SKILL_RELEASE_DISTANCE_ADD_VALUE, datas)
        return defaultRange

    @staticmethod
    @functools.lru_cache(1024)
    def getEffectRangeData(skillId):
        # 兼容下老配置
        damageRangeData = SkillBaseClass.getSkillCfg(skillId).get('DamageRange')
        if isinstance(damageRangeData, (float,int)):
            return (damageRangeData,)
        if not damageRangeData:
            return (0,)
        return damageRangeData

    def getEffectRange(self, owner, skillId, skillLv=1):
        effectRangeData = self.getEffectRangeData(skillId)
        return effectRangeData[-1] if skillLv > len(effectRangeData) else effectRangeData[skillLv - 1]

    @staticmethod
    @functools.lru_cache(1024)
    def getFxDelay(skillId):
        fxDelay = SkillBaseClass.getSkillCfg(skillId).get('fxDelay') or 0
        if type(fxDelay) is tuple and fxDelay:
            _d = fxDelay[0]
        else:
            _d = fxDelay

        return float(_d)

    @staticmethod
    @functools.lru_cache(1024)
    def getBulletFx(skillId):
        return int(SkillBaseClass.getSkillCfg(skillId).get('bulletFx') or 0)

    @staticmethod
    @functools.lru_cache(1024)
    def getBulletFxTime(skillId):
        return float(SkillBaseClass.getSkillCfg(skillId).get('bulletFxTime') or 0)

    @staticmethod
    @functools.lru_cache(1024)
    def getSkillTime(skillId):
        _skillTime = SkillBaseClass.getSkillCfg(skillId).get('skillTime') or 0
        if type(_skillTime) is tuple and _skillTime:
            _st = 0
            for timeStage in _skillTime:
                _st += timeStage
        else:
            _st = _skillTime
        return float(_st)

    @staticmethod
    @functools.lru_cache(1024)
    def isAttackSkill(skillId):
        return True if SkillBaseClass.getSkillCfg(skillId).get('isAttackSkill') == 1 else False

    @staticmethod
    @functools.lru_cache(1024)
    def getSkillHateRatio(skillId):
        return SkillBaseClass\
            .getSkillCfg(skillId)\
            .get('skillHateRatio')

    @staticmethod
    @functools.lru_cache(1024)
    def getBulletTimeScale(skillId):
        return FF.datas\
            .get(SkillBaseClass.getBulletFx(skillId), {})\
            .get('bulletTimeScale', 1.0)

    @staticmethod
    @functools.lru_cache(1024)
    def getCategory(skillId):
        return SkillBaseClass.getSkillCfg(skillId).get('category', 0)

    @staticmethod
    @functools.lru_cache(1024)
    def getSkillSchoolTag(skillId):
        return SkillBaseClass.getSkillCfg(skillId).get('classTag', 0)

    @staticmethod
    @functools.lru_cache(1024)
    def getSkillName(skillId):
        return SkillBaseClass.getSkillCfg(skillId).get('name', '')

    @staticmethod
    @functools.lru_cache(1024)
    def getSkillLvParam(skillId):
        return SkillBaseClass.getSkillCfg(skillId).get('lvParam')

    def getClassTag(self, owner):
        _classTag = self.getSkillSchoolTag(self.skillId)
        if _classTag == -1 and owner.IsAICombatUnit:
            battleType = owner.getBattleType()
            if battleType == gameconst.BattleType.physics:
                _classTag = gameconst.SCHOOL_PHYSICAL
            elif battleType == gameconst.BattleType.magic:
                _classTag = gameconst.SCHOOL_MAGIC
        return _classTag

    def getServerEffectRange(self, owner):
        # 为了解决客户端打到，服务端判断出了范围加个延迟的范围值，只给客户端算的锁定技能加
        if self.needReleaseTarget():
            return self.getEffectRange(owner, self.skillId, self.skillLv) + 1
        return self.getEffectRange(owner, self.skillId, self.skillLv)

    def getServerEffectRangeWithTarget(self, owner, target):
        targetRadius = 0
        if target.IsMonster:
            targetRadius = target.getCreepData().get('attackDistanceCompensation')
        if self.needReleaseTarget():
            return self.getEffectRange(owner, self.skillId, self.skillLv) + targetRadius + 1
        return self.getEffectRange(owner, self.skillId, self.skillLv) + targetRadius

    def inEffectRange(self, src, target):
        pos1 = src.position
        pos2 = target.position
        if not src.checkCombatRangeY(target):
            return False
        if self.getEffectRange(src, self.skillId, self.skillLv) <= 0:
            return True
        # 为了解决客户端打到，服务端判断出了范围加个延迟的范围值
        if sMath.distance2DToCompareFrom3DPosition(pos1, pos2) < math.pow(self.getServerEffectRangeWithTarget(src, target), 2):
            return True

        return False

    def inRange(self, src, pos2, checkY, distanceCompensation):
        pos1 = src.position
        if not checkY:
            return False
        _skillRange = self.getRange(src, self.skillId, self.skillLv)
        if _skillRange <= 0:
            return True

        if self.needReleaseTarget():
            _dis = _skillRange + distanceCompensation + 1
        else:
            _dis = _skillRange + distanceCompensation + 1
        # 为了解决客户端打到，服务端判断出了范围加个延迟的范围值
        if sMath.distance2DToCompareFrom3DPosition(pos1, pos2) < math.pow(_dis, 2):
            return True

        return False

    def getServerScoperRange(self, target, range):
        # 为了解决客户端打到，服务端判断出了范围加个延迟的范围值，只给客户端算的锁定技能加
        if self.needReleaseTarget():
            return range + 1
        return range

    def needReleaseTarget(self):
        _targetType = self.getTarget(self.skillId)
        if not _targetType or _targetType == 'None':
            return False
        return True

    def isMultiCastSkill(self, owner, context):
        return self.hasSkillTag(gameconst.SkillTagEnum.Casting) and self.getMaxTargetNum(owner, self.skillId, context) > 1

    @staticmethod
    @functools.lru_cache(1024)
    def getEffectTargetType(skillId):
        LOG_DBG("getEffectTargetType", skillId)
        return SkillBaseClass.getSkillCfg(skillId).get('effectTarget', '')

    @staticmethod
    @functools.lru_cache(1024)
    def getTarget(skillId):
        return SkillBaseClass.getSkillCfg(skillId).get('target', '')

    @staticmethod
    @functools.lru_cache(1024)
    def getStartAction(skillId):
        return SkillBaseClass.getSkillCfg(skillId).get('startSkillAction', None)

    @staticmethod
    @functools.lru_cache(1024)
    def getEndAction(skillId):
        return SkillBaseClass.getSkillCfg(skillId).get('endSkillAction', None)

    @staticmethod
    @functools.lru_cache(1024)
    def getShiftDelay(skillId):
        return SkillBaseClass.getSkillCfg(skillId).get('shiftDelay', 0)

    @staticmethod
    @functools.lru_cache(1024)
    def getProtectRange(skillId):
        return SkillBaseClass.getSkillCfg(skillId).get('protectRange', 0)

    def hasTag(self, tag):
        """
        由于策划那边还保留有旧的接口，这个就作为兼容用吧
        """
        _tags = self.getTag(self.skillId)
        if not _tags:
            return False

        if tag in _tags:
            return True
        return False

    def hasSkillTag(self, tag):
        _tags = self.getTag(self.skillId)
        if not _tags:
            return False

        if tag in _tags:
            return True
        return False

    @staticmethod
    @functools.lru_cache(1024)
    def isMovingSkill(skillId):
        _isMoveSkill = SkillBaseClass.getSkillCfg(skillId).get('isMoveSkill', False)
        if type(_isMoveSkill) is tuple and _isMoveSkill:
            _isMoveSkillState = _isMoveSkill[0]
        else:
            _isMoveSkillState = _isMoveSkill
        return int(_isMoveSkillState)

    @staticmethod
    @functools.lru_cache(1024)
    def isChangePosSkill(skillId):
        _tags = SkillBaseClass.getTag(skillId)
        return gameconst.SkillTagEnum.ShiftSkill in _tags\
            or gameconst.SkillTagEnum.DodgeSkill in _tags\
            or gameconst.SkillTagEnum.Lunge in _tags\
            or gameconst.SkillTagEnum.Chongfeng in _tags\
            or gameconst.SkillTagEnum.TeleportSkill in _tags\
            or gameconst.SkillTagEnum.BlinkToTarget in _tags

    def clearCD(self, owner):
        _oldInCD = self.inCDTime()
        self.tNextCast = 0.0

        if _oldInCD and owner.IsAvatar:
            owner.client.onSetAddSkillCd(
                self.skillId, 
                float(self.getCDDur(owner)), 
                float(self.tNextCast), False, 
                self.getTempData(gameconst.SkillTempDataKey.RELEASE_TIME, 0), 
                self.getTempData(gameconst.SkillTempDataKey.TOTAL_RELEASE_CNT, 0), 
                self.getTempData(gameconst.SkillTempDataKey.RELEASED_CNT, 0), 
                not self.isSkillCDStatusFrozen())

    def getOneNearest(self, pos, targetsList):
        if not targetsList or len(targetsList) == 0:
            return
        _distance = 10000
        _minIndex = -1
        for _idx, target in enumerate(targetsList):
            curDis = sMath.distance2DToCompareFrom3DPosition(pos, target.position)
            if curDis < _distance:
                _minIndex = _idx
                _distance = curDis
        return targetsList[_minIndex]

    def getOneHPLowest(self, casterEnt):
        ###取队伍或小队百分比最低
        if not casterEnt.isInTeam() and not casterEnt.inRaid():
            return casterEnt

        _targetsList = []
        if casterEnt.isInTeam():
            for _member in casterEnt.teamInfo.teamPlayerDict.values():
                if not _member.playerBox:
                    continue

                player = KBEngine.entities.get(_member.playerBox.id, None)

                if not player:
                    continue
                if utils.checkTargetTypeValid(self.getEffectTargetType(self.skillId), casterEnt, player) and self.inEffectRange(
                        casterEnt, player):
                    _targetsList.append(player)

        elif casterEnt.inRaid():
            raidTeamCacheVal = casterEnt.raidInfo.raidTeamDic.get(casterEnt.raidInfo.raidTeamIDX, None)
            if raidTeamCacheVal:
                for _member in raidTeamCacheVal.teamPlayerDict.values():
                    if not _member.playerBox:
                        continue

                    player = KBEngine.entities.get(_member.playerBox.id, None)

                    if not player:
                        continue
                    if utils.checkTargetTypeValid(self.getEffectTargetType(self.skillId), casterEnt, player) and self.inEffectRange(
                            casterEnt, player):
                        _targetsList.append(player)

        if not _targetsList:
            return casterEnt

        hpPercent = _targetsList[0].hp / _targetsList[0].fullHp if _targetsList[0].fullHp else 1
        minIndex = 0
        for idx, target in enumerate(_targetsList):
            targetHpPercent = target.hp / target.fullHp if target.fullHp else 1
            if targetHpPercent < hpPercent:
                minIndex = idx
                hpPercent = targetHpPercent

        return _targetsList[minIndex]

    def isInAttackAnnularArea(self, target, center, minRadius, maxRadius):
        targetRadius = 0
        if target.IsMonster:
            targetRadius = target.getCreepData().get('attackDistanceCompensation', 0)

        distance2 = sMath.distance2DToCompareFrom3DPosition(target.position, center)
        _distance = math.sqrt(max(0, distance2))

        return (_distance + targetRadius >= minRadius) and (_distance - targetRadius <= maxRadius)

    def isInAttackLine(self, target, vCenter, direction, length, width):
        targetRadius = 0
        if target.IsMonster:
            targetRadius = target.getCreepData().get('attackDistanceCompensation', 0)

        if targetRadius:
            return utils.isInAttackLineWithRadius(target.position, vCenter, direction, length, width, targetRadius)
        else:
            return utils.isInAttackLine(target.position, vCenter, direction, length, width, True)

    def isInAttackRectAngle(self, target, vCenter, direction, length, width, radius):
        return utils.isAttackArea(target, vCenter, radius)\
            and self.isInAttackLine(target, vCenter, direction, length, width)

    def getAngle(self, vector_a, vector_b):
        _ab = vector_a.x * vector_b.x + vector_a.y * vector_b.y
        _a1 = math.sqrt(vector_a.x * vector_a.x + vector_a.y * vector_a.y)
        _b1 = math.sqrt(vector_b.x * vector_b.x + vector_b.y * vector_b.y)
        if _a1 * _b1 == 0:
            return 0
        else:
            _cosr = _ab / (_a1 * _b1)

        _cosr = max(-1.0, min(1.0, _cosr))
        _angle = math.acos(_cosr)
        _angle2 = _angle * 360 / 2 / math.pi

        return _angle2

    def isInAttackSector(self, target, center, dir, radius, angle):
        targetRadius = 0
        if target.IsMonster:
            targetRadius = target.getCreepData().get('attackDistanceCompensation', 0)

        if not targetRadius:
            _center2 = Math.Vector2(center.x, center.z)
            _dir2 = Math.Vector2(dir.x, dir.z)

            if sMath.distance2DToCompareFrom3DPosition(target.position, center) <= radius * radius:
                _curPos = Math.Vector2(target.position.x, target.position.z)
                temp = _curPos - _center2
                return self.getAngle(_dir2, temp) <= angle / 2
            return False
        else:
            _center2 = Math.Vector2(center.x, center.z)
            _dir2 = Math.Vector2(dir.x, dir.z)

            distance2 = sMath.distance2DToCompareFrom3DPosition(target.position, center)
            distance = math.sqrt(max(0, distance2))

            if distance > radius + targetRadius:
                return False

            if distance <= targetRadius:
                return True

            _curPos = Math.Vector2(target.position.x, target.position.z)
            vectorToTarget = _curPos - _center2

            targetAngle = self.getAngle(_dir2, vectorToTarget)
            halfAngle = angle / 2

            if targetAngle <= halfAngle:
                return True

            if targetAngle > 180:
                targetAngle = 360 - targetAngle

            halfAngleRad = halfAngle * math.pi / 180
            targetAngleRad = targetAngle * math.pi / 180

            distToEdge = distance * math.sin(math.fabs(targetAngleRad - halfAngleRad))

            if distance * math.cos(targetAngleRad) <= radius and distToEdge <= targetRadius:
                return True

            leftEdgeDir = sMath.clockwiseRotate(dir, -halfAngleRad)
            leftEdgeDir = Math.Vector2(leftEdgeDir.x, leftEdgeDir.z)
            rightEdgeDir = sMath.clockwiseRotate(dir, halfAngleRad)
            rightEdgeDir = Math.Vector2(rightEdgeDir.x, rightEdgeDir.z)

            distToLeftEdge = sMath.distancePointToLine(_curPos, _center2, _center2 + leftEdgeDir)
            distToRightEdge = sMath.distancePointToLine(_curPos, _center2, _center2 + rightEdgeDir)

            if distToLeftEdge <= targetRadius or distToRightEdge <= targetRadius:
                projOnLeft = sMath.projectPointOnLine(_curPos, _center2, _center2 + leftEdgeDir)
                projOnRight = sMath.projectPointOnLine(_curPos, _center2, _center2 + rightEdgeDir)

                leftVec = projOnLeft - _center2
                rightVec = projOnRight - _center2

                if (leftVec.dot(leftEdgeDir) >= 0 and distToLeftEdge <= targetRadius) or \
                   (rightVec.dot(rightEdgeDir) >= 0 and distToRightEdge <= targetRadius):
                    return True

            return False

    def isInMultiSectorAttack(self, target, center, baseDir, radius, angle, sectorNum, offsetAngles):
        for _i in range(sectorNum):
            offsetAngle = offsetAngles[_i] if _i < len(offsetAngles) else 0
            offsetRad = offsetAngle * math.pi / 180

            rotatedDir = sMath.clockwiseRotate(baseDir, offsetRad)
            rotatedDir3D = Math.Vector3(rotatedDir[0], 0, rotatedDir[2])

            if self.isInAttackSector(target, center, rotatedDir3D, radius, angle):
                return True

        return False

    def isInAttackMi(self, target, center, skillDir, length, width):
        for _i in range(8):
            _theta = math.pi * _i / 4
            _toDir = sMath.clockwiseRotate(skillDir, _theta)
            _toDir = Math.Vector3(_toDir)
            if self.isInAttackLine(target, center, _toDir, length, width):
                return True
        return False

    def isInAttackHalfMi(self, target, center, skillDir, length, width):
        for _i in (-1, 0, 1):
            _theta = math.pi * _i / 4
            _toDir = sMath.clockwiseRotate(skillDir, _theta)
            _toDir = Math.Vector3(_toDir)
            if self.isInAttackLine(target, center, _toDir, length, width):
                return True
        return False

    def getLinkedTargets(self, owner, target, dist, linkProp, count):
        if not target:
            return []

        _targetsList = owner.getTargets(target, target.id, self.getEffectTargetType(self.skillId), dist)

        _linkedTargets = [target.id]
        if len(_linkedTargets) >= count:
            return _linkedTargets

        random.shuffle(_targetsList)

        for _e in _targetsList:
            if _e.id in _linkedTargets:
                continue

            # 有概率闪电链不会传递
            if random.random() > linkProp:
                break

            _linkedTargets.append(_e.id)
            if len(_linkedTargets) >= count:
                return _linkedTargets

        return _linkedTargets

    def checkSkillArgs(self, owenr, args):
        _scopeType = self.getScope(self.skillId)
        if not _scopeType or _scopeType == gameconst.SkillScopeEnum.TARGET_AUTO:
            return True

        if _scopeType in (gameconst.SkillScopeEnum.CIRCLE_CENTER_SELF, gameconst.SkillScopeEnum.CIRCLE_CENTER_TARGET,
                         gameconst.SkillScopeEnum.TARGET_LINKED, gameconst.SkillScopeEnum.ANNULAR_CENTER_SELF):
            return True

        if not args:
            return False

        if _scopeType in (gameconst.SkillScopeEnum.SELF_TO_TARGET_RECTANGLE, gameconst.SkillScopeEnum.USER_DEFINED_SECTOR,
                         gameconst.SkillScopeEnum.USER_DEFINED_RECTANGLE, \
                         gameconst.SkillScopeEnum.MI_CENTER_SELF, gameconst.SkillScopeEnum.HALF_MI,
                         gameconst.SkillScopeEnum.CURRENT_DIRECTION_RECTANGLE):
            if self.isChangePosSkill(self.skillId):
                return len(args) >= 6
            return len(args) >= 3

        if _scopeType in (gameconst.SkillScopeEnum.USER_DEFINED_CIRCLE,):
            if self.isChangePosSkill(self.skillId):
                return len(args) >= 7
            return len(args) >= 4

        if _scopeType in (gameconst.SkillScopeEnum.COLOSSUS_CIRCLE, gameconst.SkillScopeEnum.COLOSSUS_RECTANGLE):
            if self.isChangePosSkill(self.skillId):
                return len(args) >= 9
            return len(args) == 6

        if _scopeType == gameconst.SkillScopeEnum.MULTI_SECTOR:
            return len(args) >= 3

        return False

    def getSkillPosAndDir(self, caster, target, arr):
        _position = None
        _direction = None
        _scopeType = self.getScope(self.skillId)

        if _scopeType in (gameconst.SkillScopeEnum.CIRCLE_CENTER_SELF, gameconst.SkillScopeEnum.ANNULAR_CENTER_SELF):
            pass

        elif _scopeType == gameconst.SkillScopeEnum.CIRCLE_CENTER_TARGET:
            _position = target.position if target else caster.position

        elif _scopeType == gameconst.SkillScopeEnum.SELF_TO_TARGET_RECTANGLE:
            if target and target is not caster:
                _direction = sMath.vector3WithoutY(target.position - caster.position) 
            elif len(arr) < 3:
                _direction = sMath.vector3WithoutY(target.position - caster.position) 
            else:
                _direction = Math.Vector3(arr[0], arr[1], arr[2])

            _direction.normalise()

        elif _scopeType == gameconst.SkillScopeEnum.USER_DEFINED_SECTOR:
            _direction = Math.Vector3(arr[0], arr[1], arr[2])
            _direction.normalise()

        elif _scopeType == gameconst.SkillScopeEnum.USER_DEFINED_RECTANGLE:
            _direction = Math.Vector3(arr[0], arr[1], arr[2])
            _direction.normalise()
            _position = caster.position

        elif _scopeType == gameconst.SkillScopeEnum.USER_DEFINED_CIRCLE:
            percent = arr[3]
            _direction = Math.Vector3(arr[0], arr[1], arr[2])
            _direction.normalise()
            _position = caster.position + _direction * percent * (self.getRange(caster, self.skillId, self.skillLv)+0.1) # 加0.1是为了容错，避免因为客户端和服务端距离计算误差导致明明在范围内却打不到的情况

        elif _scopeType == gameconst.SkillScopeEnum.MI_CENTER_SELF:
            _direction = Math.Vector3(arr[0], arr[1], arr[2])
            _direction.normalise()

        elif _scopeType == gameconst.SkillScopeEnum.HALF_MI:
            _direction = Math.Vector3(arr[0], arr[1], arr[2])
            _direction.normalise()

        elif _scopeType == gameconst.SkillScopeEnum.TARGET_LINKED:
            _position = target.position if target else caster.position

        elif _scopeType == gameconst.SkillScopeEnum.COLOSSUS_CIRCLE:
            _position = tuple(arr[:3])
            _direction = Math.Vector3(arr[3], arr[4], arr[5])
            _direction.normalise()

        elif _scopeType == gameconst.SkillScopeEnum.COLOSSUS_RECTANGLE:
            if arr:
                _position = tuple(arr[:3])
                _direction = Math.Vector3(arr[3], arr[4], arr[5])
                _direction.normalise()

        elif _scopeType == gameconst.SkillScopeEnum.CURRENT_DIRECTION_RECTANGLE:
            _direction = sMath.getDirFromYaw(caster._direction[2])
            _direction.normalise()
            _position = caster.position

        elif _scopeType == gameconst.SkillScopeEnum.MULTI_SECTOR:
            _direction = Math.Vector3(arr[0], arr[1], arr[2])
            _direction.normalise()

        if not _direction and self.needReleaseTarget() and target:
            _direction = Math.Vector3(target.position - caster.position)
            _direction.normalise()

        return _position, _direction

    def getSkillArr(self, caster, target, direction=None):
        _arr = []
        if not direction:
            direction = sMath.vector3WithoutY(target.position - caster.position)
            direction.normalise()
        _scopeType = self.getScope(self.skillId)

        if not _scopeType:
            _arr = list(direction)
        elif _scopeType == gameconst.SkillScopeEnum.SELF_TO_TARGET_RECTANGLE:
            _arr = list(direction)

        elif _scopeType == gameconst.SkillScopeEnum.USER_DEFINED_SECTOR:
            _arr = list(direction)

        elif _scopeType in (
                gameconst.SkillScopeEnum.USER_DEFINED_RECTANGLE, gameconst.SkillScopeEnum.CURRENT_DIRECTION_RECTANGLE):
            _arr = list(direction)

        elif _scopeType == gameconst.SkillScopeEnum.USER_DEFINED_CIRCLE:
            _arr = utils.transformPosesToSkillArgs(
                caster.position,
                target.position,
                self.getRange(caster, self.skillId, self.skillLv),
                direction
            )

        elif _scopeType == gameconst.SkillScopeEnum.MI_CENTER_SELF:
            _arr = list(direction)

        elif _scopeType == gameconst.SkillScopeEnum.HALF_MI:
            _arr = list(direction)

        elif _scopeType == gameconst.SkillScopeEnum.MULTI_SECTOR:
            _arr = list(direction)

        return _arr

    def getSkillDesPosition(self, caster, target, skillArgs):
        if self.hasSkillTag(gameconst.SkillTagEnum.TeleportSkill):
            distance = self.getRange(caster, self.skillId, self.skillLv)
            dstPosition = sMath.getForwardPos(caster.position, caster.direction[2], distance)
            skillPos, skillDir = self.getSkillPosAndDir(caster, target, skillArgs)
            # scope其他时取技能朝向，scope为6时取双摇杆选的坐标
            if self.getScope(self.skillId) == gameconst.SkillScopeEnum.USER_DEFINED_CIRCLE:
                dstPosition = skillPos
            else:
                dstPosition = caster.position + skillDir * distance

            dstPosition = utils.getSurfacePos(caster.spaceID, dstPosition)
            _realDstPos = utils.getRaycastPosition(caster.spaceID, caster.position, dstPosition)
            desPosition = list(_realDstPos)

        elif self.hasSkillTag(gameconst.SkillTagEnum.BlinkToTarget):
            offset = 2.0
            _yaw = sMath.getYawFromPoints(caster.position, target.position)
            targetPos = sMath.getForwardPos(target.position, _yaw, offset)

            targetPos = utils.getSurfacePos(caster.spaceID, targetPos)
            _realDstPos = utils.getRaycastPosition(caster.spaceID, caster.position, targetPos)
            desPosition = list(_realDstPos)
        elif self.hasSkillTag(gameconst.SkillTagEnum.Chongfeng):
            skillPos, skillDir = self.getSkillPosAndDir(caster, target, skillArgs)
            dstPosition = caster.position + skillDir * self.getRange(caster, self.skillId, self.skillLv)

            dstPosition = utils.getSurfacePos(caster.spaceID, dstPosition)
            dstPosition = utils.getRaycastPosition(caster.spaceID, caster.position, dstPosition)
            desPosition = list(dstPosition)
        elif self.hasSkillTag(gameconst.SkillTagEnum.Lunge):
            skillPos, skillDir = self.getSkillPosAndDir(caster, target, skillArgs)
            skillRange = self.getRange(caster, self.skillId, self.skillLv)
            # 根据target的碰撞距离处理
            if target:
                collisionDis = 2.0
                if hasattr(target, 'creepbaseId'):
                    collisionDis = utils.getCollisionDistance(target.creepbaseId, collisionDis)
                distance = sMath.distance2D(caster.position, target.position)
                # 距离超过碰撞距离，需要减去碰撞距离。否则原地不动
                distance = distance - collisionDis if distance > collisionDis else 0
                if skillRange > distance:
                    skillRange = distance

            dstPosition = caster.position + skillDir * skillRange
            dstPosition = utils.getSurfacePos(caster.spaceID, dstPosition)
            _realDstPos = utils.getRaycastPosition(caster.spaceID, caster.position, dstPosition)
            desPosition = list(_realDstPos)
        elif self.hasSkillTag(gameconst.SkillTagEnum.DodgeSkill) or self.hasSkillTag(gameconst.SkillTagEnum.ShiftSkill):
            skillPos, skillDir = self.getSkillPosAndDir(caster, target, skillArgs)
            dstPosition = caster.position + skillDir * self.getRange(caster, self.skillId, self.skillLv)
            dstPosition = utils.getSurfacePos(caster.spaceID, dstPosition)
            _realDstPos = utils.getRaycastPosition(caster.spaceID, caster.position, dstPosition)
            LOG_DBG('dodgeGetPos', caster.spaceID, caster.position, dstPosition, _realDstPos)
            desPosition = list(_realDstPos)

        return desPosition

    def getEffectTargets(self, caster, targetId, arr, forceTarget=False, positionSkillArgs=None, context = None):
        if not caster:
            return []
        if self.getTempData(gameconst.SkillTempDataKey.IS_CHANNELING_EMPTY, False):
            return []

        if self.targetIds:
            invalidIds = []
            for _i, tid in enumerate(self.targetIds):
                target = KBEngine.entities.get(tid)
                if not target:
                    invalidIds.append(_i)
                    continue

                if not utils.checkTargetTypeValid(
                        self.getEffectTargetType(self.skillId),
                        caster,
                        target):

                    invalidIds.append(_i)

            for _i in reversed(invalidIds):
                self.targetIds.pop(_i)

            return self.targetIds

        return self._internalGetEffectTargets(caster, targetId, arr, forceTarget, positionSkillArgs, context)

    def _internalGetEffectTargets(self, caster, targetId, arr, forceTarget, positionSkillArgs, context):
        # 客户端自动寻路攻击目标调用过来的时候，可能最新的position还没报告给服务端，所以这里按技能距离可能
        # 拿不到客户端选中的entity，这里加点offset偏差做容错

        target = KBEngine.entities.get(targetId)

        _skillPos, _skillDir = self.getSkillPosAndDir(caster, target, arr)
        scopes = self.getScope(self.skillId)
        _scopeParams, scopeAddRatio = self.getScopeParam(caster, self.skillId, context)

        LOG_DBG("in _internalGetEffectTargets ", scopes, self.skillId, _scopeParams, scopeAddRatio)

        if not scopes or scopes == gameconst.SkillScopeEnum.TARGET_AUTO:
            if self.hasSkillTag(gameconst.SkillTagEnum.SingleHeal)\
                    and hasattr(caster, 'commonFlagCell')\
                    and caster.getCommonFlagCell(gameconst.CommonFlagCellType.IsHealHPLow)\
                    and (
                        not target\
                        or targetId == caster.id\
                        or not utils.checkTargetTypeValid(self.getEffectTargetType(self.skillId), 
                                                          caster, target)):

                _targetNearest = self.getOneHPLowest(caster)

            else:
                if target\
                        and (caster.isVisible(target) or caster.hasBuffTag(gameconst.BuffTag.TagSeeHiddenEnt))\
                        and utils.checkTargetTypeValid(self.getEffectTargetType(self.skillId), caster, target):

                    if self.inEffectRange(caster, target):
                        return [target.id]
                    else:
                        return []

                if self.getEffectTargetType(self.skillId) == 'Friend':
                    return [caster.id]

                if not targetId:
                    return []

                if self.getTempData(gameconst.SkillTempDataKey.BEGIN_SKILL_POSITION):
                    targetsList = caster.getTargets(caster, targetId, self.getEffectTargetType(self.skillId),
                                                    self.getServerEffectRange(caster), forceTarget,
                                                    self.getTempData(gameconst.SkillTempDataKey.BEGIN_SKILL_POSITION))
                    _targetNearest = self.getOneNearest(self.getTempData(gameconst.SkillTempDataKey.BEGIN_SKILL_POSITION), targetsList)
                else:
                    targetsList = caster.getTargets(caster, targetId, self.getEffectTargetType(self.skillId),
                                                    self.getServerEffectRange(caster), forceTarget)
                    _targetNearest = self.getOneNearest(caster.position, targetsList)

            if _targetNearest and (caster.isVisible(_targetNearest) or caster.hasBuffTag(
                    gameconst.BuffTag.TagSeeHiddenEnt)) and self.inEffectRange(caster, _targetNearest):
                return [_targetNearest.id]
            else:
                return []

        elif scopes == gameconst.SkillScopeEnum.CIRCLE_CENTER_SELF:
            center = caster.position
            radius = float(_scopeParams[0])
            if scopeAddRatio:
                radius *= (1+scopeAddRatio)

            checkScopeFun = lambda target: utils.isAttackArea(target, center, radius)
            return caster.getTargetsWithNum(caster, targetId, self.getEffectTargetType(self.skillId), self.getServerEffectRange(caster),
                                            self.getMaxTargetNum(caster, self.skillId, context), checkScopeFun)

        elif scopes == gameconst.SkillScopeEnum.CIRCLE_CENTER_TARGET:
            if not target:
                return []

            radius = float(_scopeParams[0])
            if scopeAddRatio:
                radius *= (1+scopeAddRatio)

            checkScopeFun = lambda target: utils.isAttackArea(target, _skillPos, radius)
            return caster.getTargetsWithNum(target, targetId, self.getEffectTargetType(self.skillId),
                                            self.getEffectRange(caster, self.skillId, self.skillLv) + 0.8,
                                            self.getMaxTargetNum(caster, self.skillId, context), checkScopeFun)

        elif scopes == gameconst.SkillScopeEnum.SELF_TO_TARGET_RECTANGLE:
            length = float(_scopeParams[0])
            width = float(_scopeParams[1])
            if scopeAddRatio:
                length *= (1+scopeAddRatio)
                width *= (1+scopeAddRatio)

            length = self.getServerScoperRange(target, length)
            checkScopeFun = lambda target: self.isInAttackLine(target, caster.position, _skillDir, length, width)
            return caster.getTargetsWithNum(caster, targetId, self.getEffectTargetType(self.skillId), self.getServerEffectRange(caster),
                                            self.getMaxTargetNum(caster, self.skillId, context), checkScopeFun)

        elif scopes == gameconst.SkillScopeEnum.USER_DEFINED_SECTOR:
            skillSectorAngle = float(_scopeParams[0])
            radius = self.getServerEffectRange(caster)
            if scopeAddRatio:
                radius *= (1+scopeAddRatio)
                
            checkScopeFun = lambda target: self.isInAttackSector(target, caster.position, _skillDir,
                                                                 radius, skillSectorAngle * 2)
            return caster.getTargetsWithNum(caster, targetId, self.getEffectTargetType(self.skillId), self.getServerEffectRange(caster),
                                            self.getMaxTargetNum(caster, self.skillId, context), checkScopeFun)

        elif scopes in (gameconst.SkillScopeEnum.USER_DEFINED_RECTANGLE, gameconst.SkillScopeEnum.CURRENT_DIRECTION_RECTANGLE):
            length = self.getServerEffectRange(caster) + self.getProtectRange(self.skillId)
            width = float(_scopeParams[1])
            if scopeAddRatio:
                length *= (1+scopeAddRatio)
                width *= (1+scopeAddRatio)
            if positionSkillArgs:
                beginSkillPos = self.getTempData(gameconst.SkillTempDataKey.BEGIN_SKILL_POSITION) if self.getTempData(
                    gameconst.SkillTempDataKey.BEGIN_SKILL_POSITION) else caster.position
                distance = sMath.distance2D(beginSkillPos, positionSkillArgs)
                range = min(self.getEffectRange(caster, self.skillId, self.skillLv), distance + self.getProtectRange(self.skillId))
            else:
                range = self.getServerEffectRange(caster) + self.getProtectRange(self.skillId)
            if self.getTempData(gameconst.SkillTempDataKey.BEGIN_SKILL_POSITION):
                checkScopeFun = lambda target: self.isInAttackRectAngle(target, self.getTempData(gameconst.SkillTempDataKey.BEGIN_SKILL_POSITION),
                                                                        _skillDir, length, width, range)
                return caster.getTargetsWithNum(caster, targetId, self.getEffectTargetType(self.skillId), range,
                                                self.getMaxTargetNum(caster, self.skillId, context), checkScopeFun)
            else:
                checkScopeFun = lambda target: self.isInAttackRectAngle(target, caster.position, _skillDir, length,
                                                                        width, range)
                return caster.getTargetsWithNum(caster, targetId, self.getEffectTargetType(self.skillId), range,
                                                self.getMaxTargetNum(caster, self.skillId, context), checkScopeFun)

        elif scopes == gameconst.SkillScopeEnum.USER_DEFINED_CIRCLE:
            direction = Math.Vector3(arr[0], arr[1], arr[2])
            percent = arr[3]
            beginSkillPos = self.getTempData(gameconst.SkillTempDataKey.BEGIN_SKILL_POSITION) if self.getTempData(gameconst.SkillTempDataKey.BEGIN_SKILL_POSITION) else caster.position
            center = beginSkillPos + direction * percent * (self.getRange(caster, self.skillId, self.skillLv)+0.1) # 加0.1是为了容错，避免因为客户端和服务端距离计算误差导致明明在范围内却打不到的情况
            radius = float(_scopeParams[0])
            if scopeAddRatio:
                radius *= (1+scopeAddRatio)
            checkScopeFun = lambda target: utils.isAttackArea(target, center, radius)
            return caster.getTargetsWithNum(target, targetId, self.getEffectTargetType(self.skillId),
                                            self.getServerEffectRange(caster) + radius,
                                            self.getMaxTargetNum(caster, self.skillId, context), checkScopeFun)

        elif scopes == gameconst.SkillScopeEnum.MI_CENTER_SELF:
            length = float(_scopeParams[0])
            width = float(_scopeParams[1])

            checkScopeFun = lambda target: self.isInAttackMi(target, caster.position, _skillDir, length, width)
            return caster.getTargetsWithNum(target, targetId, self.getEffectTargetType(self.skillId), self.getServerEffectRange(caster),
                                            self.getMaxTargetNum(caster, self.skillId, context), checkScopeFun)

        elif scopes == gameconst.SkillScopeEnum.HALF_MI:
            length = float(_scopeParams[0])
            width = float(_scopeParams[1])

            checkScopeFun = lambda target: self.isInAttackHalfMi(target, caster.position, _skillDir, length, width)
            return caster.getTargetsWithNum(target, targetId, self.getEffectTargetType(self.skillId), self.getServerEffectRange(caster),
                                            self.getMaxTargetNum(caster, self.skillId, context), checkScopeFun)

        elif scopes == gameconst.SkillScopeEnum.TARGET_LINKED:
            dist, linkProp, count = float(_scopeParams[0]), float(_scopeParams[1]), float(_scopeParams[2])
            linkedTargets = self.getLinkedTargets(caster, target, dist, linkProp, count)
            return linkedTargets

        elif scopes == gameconst.SkillScopeEnum.COLOSSUS_CIRCLE:
            center = _skillPos
            radius = float(_scopeParams[0])

            checkScopeFun = lambda target: utils.isAttackArea(target, center, radius)
            return caster.getTargetsWithNum(target, targetId, self.getEffectTargetType(self.skillId),
                                            self.getServerEffectRange(caster) + radius,
                                            self.getMaxTargetNum(caster, self.skillId, context), checkScopeFun)

        elif scopes == gameconst.SkillScopeEnum.COLOSSUS_RECTANGLE:
            length = self.getServerEffectRange(caster)
            width = float(_scopeParams[1])

            if _skillPos:
                checkScopeFun = lambda target: self.isInAttackRectAngle(target, _skillPos, _skillDir, length, width,
                                                                        self.getServerEffectRange(caster))
                return caster.getTargetsWithNum(caster, targetId, self.getEffectTargetType(self.skillId),
                                                self.getServerEffectRange(caster),
                                                self.getMaxTargetNum(caster, self.skillId, context), checkScopeFun)
            else:
                return []
        elif scopes == gameconst.SkillScopeEnum.ANNULAR_CENTER_SELF:
            minRadius = float(_scopeParams[0])
            maxRadius = float(_scopeParams[1])
            center = caster.position
            checkScopeFun = lambda target: self.isInAttackAnnularArea(target, center, minRadius, maxRadius)
            return caster.getTargetsWithNum(target, targetId, self.getEffectTargetType(self.skillId), self.getServerEffectRange(caster),
                                            self.getMaxTargetNum(caster, self.skillId, context), checkScopeFun)
        elif scopes == gameconst.SkillScopeEnum.MULTI_SECTOR:
            sectorNum = int(_scopeParams[0])
            offsetAngles = _scopeParams[1]
            sectorAngle = float(_scopeParams[2])

            if not isinstance(offsetAngles, (list, tuple)):
                offsetAngles = []

            if len(offsetAngles) < sectorNum:
                caster.debugCombatMsg("_internalGetEffectTargets MULTI_SECTOR not enough offsetAngles: skillId:%s", self.skillId)

            checkScopeFun = lambda target: self.isInMultiSectorAttack(target, caster.position, _skillDir,
                                                self.getServerEffectRange(caster), sectorAngle * 2, sectorNum, offsetAngles)
            return caster.getTargetsWithNum(caster, targetId, self.getEffectTargetType(self.skillId), self.getServerEffectRange(caster),
                                            self.getMaxTargetNum(caster, self.skillId, context), checkScopeFun)

        return []

    def _checkUseSkillOwner(self, owner, targetId, ignoreReasons=0, checkInRange=True):
        LOG_DBG('_checkUseSkillOwner', self.skillId, targetId, ignoreReasons, checkInRange)
        code = gameconst.UseSkillCheck.USC_ENUM_FORBID
        if not code & ignoreReasons and owner.checkForbidSkill(self.getSkillId()):
            owner.debugCombatMsg('_checkUseSkillOwner forbid skill: skillId:%s', self.getSkillId())
            return code
        
        code = gameconst.UseSkillCheck.USC_ENUM_IN_CD
        if not code & ignoreReasons and self.inCDTime():
            owner.debugCombatMsg('_checkUseSkillOwner cannot use inCDTime: skillId:%s, tNextCast:%s, now:%s', self.getSkillId(), self.tNextCast, time.time())
            return code

        code = gameconst.UseSkillCheck.USC_ENUM_LACK_OF_MP
        if not code & ignoreReasons and owner.IsAvatar and owner.mp < self.getCostMp(owner, self.skillId, owner.mpCostRatio):
            owner.debugCombatMsg('_checkUseSkillOwner fail to use lack of mp: skillId:%s', self.skillId)
            return code

        code = gameconst.UseSkillCheck.USC_ENUM_INVALID_OWNER
        if not code & ignoreReasons and not owner:
            LOG_ERR('skill %s caster error' % (self.getSkillId()))
            return code

        code = gameconst.UseSkillCheck.USC_ENUM_SELF_DIE
        if not code & ignoreReasons and owner.isDie():
            return code

        if utils.hasSkillTagById(self.skillId, gameconst.SkillTagEnum.UltraSkill):
            code = gameconst.UseSkillCheck.USC_ENUM_ULTRA_SKILL_POWER_NOT_ENOUGH
            if not code & ignoreReasons and not owner.isUltraSkillPowerMax():
                owner.debugCombatMsg('_checkUseSkillOwner fail to use ultra skill power not enough: skillId:%s', self.getSkillId())
                return code

        code = gameconst.UseSkillCheck.USC_ENUM_STATE_CONFLICT
        if not code & ignoreReasons:
            _extraEventId = self.getSkillEvent(self.skillId)
            if _extraEventId:
                if not owner.checkConflictState(_extraEventId):
                    owner.debugCombatMsg('_checkUseSkillOwner fail to use skill conflict state _extraEventId: skillId:%s, _extraEventId:%s', self.getSkillId(), _extraEventId)
                    return code
            else:
                if not owner.checkConflictState(C_C_DD.datas.useSkill):
                    owner.debugCombatMsg('_checkUseSkillOwner fail to use skill conflict state useSkill: skillId:%s', self.getSkillId())
                    return code

                if utils.hasSkillTagById(self.skillId, gameconst.SkillTagEnum.GeneralSkill) and not owner.checkConflictState(
                        C_C_DD.datas.useGeneralSkill, False):
                    return code

                _skillState = self.getSkillState()
                eventId = C_SD.datas[_skillState].get('event')
                if eventId and not owner.checkConflictState(eventId):
                    owner.debugCombatMsg('_checkUseSkillOwner fail to use skil conflict state eventId: skillId:%s, eventId:%s', self.getSkillId(), eventId)
                    return code

        return gameconst.UseSkillCheck.USC_ENUM_CHEKC_OK

    def _checkUseSkillTarget(self, owner, targetId, ignoreReasons=0, checkInRange=True):
        needReleaseTarget = self.needReleaseTarget()
        LOG_DBG('_checkUseSkillTarget', self.skillId, targetId, needReleaseTarget)
        owner.debugCombatMsg('_checkUseSkillTarget: skillId:%s, targetId:%s, needReleaseTarget:%s', self.skillId, targetId, needReleaseTarget)
        if self.hasSkillTag(gameconst.SkillTagEnum.SingleHeal):
            target = KBEngine.entities.get(targetId)
            if not target:
                return gameconst.UseSkillCheck.USC_ENUM_CHEKC_OK
            if not utils.checkTargetTypeValid(self.getEffectTargetType(self.skillId), owner, target):
                return gameconst.UseSkillCheck.USC_ENUM_CHEKC_OK
            if checkInRange:
                res = self.inRange(
                    owner, 
                    target.position, 
                    owner.checkCombatRangeY(target), 
                    target.fetchAttackDistanceCompensation())

            else:
                res = self.inEffectRange(owner, target)
            if not res:
                if self.hasSkillTag(gameconst.SkillTagEnum.Channel) or self.hasSkillTag(gameconst.SkillTagEnum.Casting):
                    owner.showMsg(C_CD.datas['targetIsOutOfRange_butCasted']['value'], [])
                else:
                    owner.showMsg(C_CD.datas['targetIsOutOfRange']['value'], [])
                    return gameconst.UseSkillCheck.USC_ENUM_SINGLE_HEAL_OUT_OF_RANGE
        if needReleaseTarget:
            target = KBEngine.entities.get(targetId)
            if not target:
                if ignoreReasons & gameconst.UseSkillCheck.USC_ENUM_TARGET_NOT_FOUND:
                    return gameconst.UseSkillCheck.USC_ENUM_CHEKC_OK

                else:
                    return gameconst.UseSkillCheck.USC_ENUM_TARGET_NOT_FOUND

            code = gameconst.UseSkillCheck.USC_ENUM_INVALID_TARGET
            if not code & ignoreReasons and not utils.checkTargetTypeValid(self.getTarget(self.skillId), owner, target):
                owner.debugCombatMsg('_checkUseSkillTarget skill cannot use because checkTargetTypeValid fail: skillId:%s, targetType:%s, targetId:%s', self.skillId, self.getTarget(self.skillId),
                                     target.id)
                return code

            code = gameconst.UseSkillCheck.USC_ENUM_INVISIBLE_TARGET
            if not code & ignoreReasons and not owner.isVisible(target) and not owner.hasBuffTag(
                    gameconst.BuffTag.TagSeeHiddenEnt):
                owner.debugCombatMsg('_checkUseSkillTarget skill cannot use because target is invisible: skillId:%s, targetId:%s', self.skillId, target.id)
                return code

            code = gameconst.UseSkillCheck.USC_ENUM_CROSS_SPACE
            if not code & ignoreReasons and target.spaceNo != owner.spaceNo:
                owner.debugCombatMsg('_checkUseSkillTarget skill cannot use because cross space: skillId:%s, targetSpaceNo:%s, ownerSpaceNo:%s', self.skillId, target.spaceNo, owner.spaceNo)
                return code

            code = gameconst.UseSkillCheck.USC_ENUM_OUT_OF_RANGE
            if not code & ignoreReasons:
                if not self.inRange(
                    owner, 
                    target.position, 
                    owner.checkCombatRangeY(target), 
                    target.fetchAttackDistanceCompensation()
                ):

                    owner.debugCombatMsg('_checkUseSkillTarget skill cannot use because needReleaseTarget and not inRange: skillId:%s, targetPosition:%s, ownerPosition:%s, distance:%s',
                                        self.getSkillId(), target.position, owner.position, sMath.distance2D(owner.position, target.position))
                    return code

        return gameconst.UseSkillCheck.USC_ENUM_CHEKC_OK

    def checkUseSkill(self, owner, targetId, ignoreReasons=0, checkInRange=True):
        code = self._checkUseSkillOwner(owner, targetId, ignoreReasons, checkInRange)
        if code != gameconst.UseSkillCheck.USC_ENUM_CHEKC_OK:
            return code

        return self._checkUseSkillTarget(owner, targetId, ignoreReasons, checkInRange)

    # 延迟结算时间
    def getSkillResultDelay(self, owner, targetId,  compensateTime):
        _delayTime = self.getFxDelay(self.skillId) - (compensateTime / 1000.0)
        if self.hasSkillTag(gameconst.SkillTagEnum.Channel):
            return sMath.limit(_delayTime, 0.0, 9999.0)
        if self.getBulletFx(self.skillId):
            _timeEx = self.calBulletTime(owner, targetId)

            _delayTime += _timeEx
        _delayTime = sMath.limit(_delayTime, 0.0, 9999.0)
        return _delayTime

    def getSkillState(self):
        raise NotImplementedError()

    def doEnterCDTime(self, owner, delayCd=0):
        LOG_DBG('doEnterCDTime 1', self.skillId, self.tNextCast, delayCd)
        addCD = 0
        if delayCd > 0:
            addCD = delayCd
            self.tNextCast = time.time() + delayCd
        else:
            addCD = self.getCDDur(owner)
            self.tNextCast = time.time() + addCD - 0.1
        LOG_DBG('doEnterCDTime 2', self.skillId, self.tNextCast, addCD, delayCd)

    def onInvalidateRefreshCD(self, owner, doReset=True, notifyClient=True):
        owner.debugCombatMsg('onInvalidateRefreshCD: skillId:%s, tempData:%s', self.skillId, self.tempData)
        self.tNextCast = self.getTempData('tNextCast', time.time())
        self.popTempData(gameconst.SkillTempDataKey.RESTORE_CD_TIMER)

        if notifyClient:
            owner.client.onSetAddSkillCd(
                self.skillId, 
                float(self.getCDDur(owner)), 
                float(self.tNextCast),
                False, 
                self.getTempData(gameconst.SkillTempDataKey.RELEASE_TIME, 0), 
                self.getTempData(gameconst.SkillTempDataKey.TOTAL_RELEASE_CNT, 0), 
                self.getTempData(gameconst.SkillTempDataKey.RELEASED_CNT, 0), 
                not self.isSkillCDStatusFrozen())

        doReset and self.resetSkill(owner, gameconst.ResetSkillReason.ReasonTimeRefreshDone)

    # 支持callAfterDelay配出来的分阶段action
    def setupMulAttackAction(self, owner, context, delay, firstStageCalcDelay, duration):
        context.actionStage += 1
        if context.actionStage >= 50:
            gameengine.panicStack('skill action stage reach max', context.actionStage, self.skillId)

        self.setTempData(owner, gameconst.SkillTempDataKey.DURATION, duration)
        if delay <= 0:
            owner.doSkillAction(self.skillId, context, firstStageCalcDelay, True,
                                gameconst.UseSkillCheck.USC_MUL_ATTACK_CHECK_IGNORES, duration)
        else:
            tid = owner.addTimerCB(delay, 'doSkillAction', (self.skillId, context, firstStageCalcDelay, True,
                                                           gameconst.UseSkillCheck.USC_MUL_ATTACK_CHECK_IGNORES, duration),
                                  gametimer.TIMER_TAG_DO_SKILL_ACTION)

            self._cancelTempTimer(owner, gameconst.SkillTempDataKey.MUL_ATTACK_ACT_TIMER, gametimer.TIMER_TAG_DO_SKILL_ACTION)
            self.setTimerTempData(owner, gameconst.SkillTempDataKey.MUL_ATTACK_ACT_TIMER, tid)

    def applySkillEffect(self, owner, targetId, skillArgs, actionCtx, calcDelay, doRemoveState=True):
        _realSkillArgs = skillArgs
        _positionSkillArgs = None
        if self.isChangePosSkill(self.skillId):
            _realSkillArgs = list(skillArgs)[:-3]
            _positionSkillArgs = list(skillArgs)[-3:]

        hitChooseAgain = S_SD.datas[self.skillId].get('HitChooseAgain')
        if hitChooseAgain:
            self.targetIds = []

        effectedEntIds = self.getEffectTargets(owner, targetId, _realSkillArgs, positionSkillArgs=_positionSkillArgs)
        actionCtx.effectedEntIds = effectedEntIds

        skillEventContext = effectEventCtx.SkillEventCtx(owner.id, self.skillId, _realSkillArgs, targetId,
                                                         effectedEntIds, self)
        owner.onEffectEventCall('onSkill', owner.id, targetId, skillEventContext)
        owner.onEffectEventCall('onSpecSkill', owner.id, targetId, skillEventContext)

        try:
            _actResult = owner.doSkillAction(self.skillId, actionCtx, calcDelay, doRemoveState=doRemoveState)
        except Exception as e:
            _actResult = gameclass.ResultBool(False)
            gameengine.panicStack('applySkillEffect error:', owner.id, self.skillId, targetId, str(e))

        self.targetIds = []
        owner.debugCombatMsg('applySkillEffect: skillId:%s, targetId:%s, skillArgs:%s, effectedEntIds:%s, _actResult:%s', self.skillId, targetId, skillArgs, effectedEntIds, _actResult)
        return _actResult

    def onSkillActionFinished(self, owner, targetId, skillArgs, ctx, calcDelay, actionDuration, doRemoveState=True):
        # 技能分为若干个阶段：1.客户端请求施法 2.计算子弹飞行，挥刀等延迟结算 3.结算技能数值
        # 4.结算完等整个技能时间结束(等待客户端收刀等后摇动作)

        # 引导技能在引导结束后再执行skillDone，其他技能结算完就可以skillDone了
        if not self.isInSkill:
            return
        if not self.hasSkillTag(
                gameconst.SkillTagEnum.Channel) and ctx.actionProgress == gameconst.ActionProgressEnum.actionDone:

            _remainTime = self.getSkillTime(self.skillId) - calcDelay - actionDuration
            if _remainTime <= 0:
                self.useSkillDone(owner, targetId, skillArgs, doRemoveState=doRemoveState)
            else:
                tid = owner.addTimerCB(_remainTime, '_onSkillCallback',
                                      (self, 'useSkillDone', (targetId, skillArgs, True, False, doRemoveState)),
                                      gametimer.TIMER_TAG_SKILL_DONE)

                self._cancelTempTimer(owner, gameconst.SkillTempDataKey.SKILL_DONE_TIMER, gametimer.TIMER_TAG_SKILL_DONE)
                self.setTimerTempData(owner, gameconst.SkillTempDataKey.SKILL_DONE_TIMER, tid)

    def useSkillDone(self, owner, targetId, skillArgs, isSucc=True, startActionFail=False, doRemoveState=True, forceResetSkill=False):
        self._cancelTempTimer(owner, gameconst.SkillTempDataKey.SKILL_DONE_TIMER, gametimer.TIMER_TAG_SKILL_DONE)
        owner.debugCombatMsg('useSkillDone: skillId:%s, targetId:%s, isSucc:%s', self.skillId, targetId, isSucc)
        if doRemoveState:
            skillState = self.getSkillState()
            owner.removeState(skillState, removeReason=gameconst.RemoveStateReason.SKILL_DONE)

        if self.hasTempData(gameconst.SkillTempDataKey.BEGIN_SKILL_POSITION):
            self.popTempData(gameconst.SkillTempDataKey.BEGIN_SKILL_POSITION)

        if self.hasTempData(gameconst.SkillTempDataKey.SKILL_ARGS):
            self.popTempData(gameconst.SkillTempDataKey.SKILL_ARGS)

        if self.needResetOnSkillDone(owner) or forceResetSkill:
            self.resetSkill(owner, gameconst.ResetSkillReason.ReasonSkillDone, doRemoveState)
        else:
            self.isInSkill = False
            self.targetIds = []

        owner.onUseSkillFinish(self.skillId)

        target = KBEngine.entities.get(targetId)
        endAction = self.getSkillCfg(self.skillId).get('endSkillAction', None)
        # startAction释放成功了才执行endAction，目前只有位移技能的startAction有返回值可能返回失败
        if endAction and not startActionFail and isSucc:
            _realSkillArgs = skillArgs
            if self.isChangePosSkill(self.skillId):
                _realSkillArgs = skillArgs[:-3]
            _effectedEntIds = self.getEffectTargets(owner, targetId, _realSkillArgs)
            _ctx = actionContext.UseSkillCtx(
                owner.id, 
                self.skillId, 
                skillArgs, 
                targetId, 
                _effectedEntIds, 
                self,
                None, 
                isSucc=isSucc)
            endAction(owner, target, _ctx)

        # 在aiController的useSkillDone里面会把当前这个skillId pop掉，改为放在最后把
        owner.IsAICombatUnit and owner.aiController and owner.aiController.useSkillDone(self.skillId)

    def getRealSkillVal(self, owner):
        # 目前只有StageSkill实现了这个方法
        return self, False

    def doActionOnChangeSlot(self, owner, bActive):
        if bActive:
            _action = self.getActivateAction(self.skillId)
        else:
            _action = self.getDeactivateAction(self.skillId)

        if _action:
            _action(owner, owner, actionContext.ChangeSkillSlotCtx(self.skillId))

    def onChangedFromSkill(self, fromSkillObj):
        self.tNextCast = fromSkillObj.tNextCast
        self.skillLv = fromSkillObj.skillLv

    def onTimerCallback(self, owner, callbackName, args):
        getattr(self, callbackName)(owner, *args)

    def onChangedSkillBegin(self, owner):
        if self.hasTempData(gameconst.SkillTempDataKey.RESTORE_CD_TIMER):
            self._cancelTempTimer(owner, gameconst.SkillTempDataKey.RESTORE_CD_TIMER, gametimer.TIMER_TAG_RESTORE_CD)
            self.onInvalidateRefreshCD(owner, doReset=False, notifyClient=False)

        self.doEnterCDTime(owner)
        owner.client.onSetAddSkillCd(
            self.skillId, 
            float(self.getCDDur(owner)), 
            float(self.tNextCast), 
            False, 
            self.getTempData(gameconst.SkillTempDataKey.RELEASE_TIME, 0), 
            self.getTempData(gameconst.SkillTempDataKey.TOTAL_RELEASE_CNT, 0), 
            self.getTempData(gameconst.SkillTempDataKey.RELEASED_CNT, 0), 
            not self.isSkillCDStatusFrozen())

    def isSkillCDStatusFrozen(self):
        return self.getTempData(gameconst.SkillTempDataKey.CHANGE_SKILL_CD_STATUS, gameconst.SkillCDStatus.DEFAULT) == gameconst.SkillCDStatus.DISABLED

    def getTempData(self, name, defalut=None):
        return self.tempData.get(name, defalut)

    def hasTempData(self, name):
        return name in self.tempData

    def popTempData(self, name, default=None):
        return self.tempData.pop(name, default)

    def setTempData(self, owner, name, val):
        self.tempData[name] = val

    def setTimerTempData(self, owner, name, val):
        if owner.IsAvatar:
            owner.skillTimerLogQueue.addSkillTimerLog(
                id(self),
                val,
                gameconst.SKILL_LOG_OPR_SET_TIMER,
                name,
                self.skillId,
            )

        owner.skillTimerDic[val] = name
        self.tempData[name] = val
    
    def _cancelTempTimer(self, owner, timerName, timerTag=''):
        tid = self.popTempData(timerName, 0)
        if owner.IsAvatar:
            owner.skillTimerLogQueue.addSkillTimerLog(
                id(self), 
                tid, 
                gameconst.SKILL_LOG_OPR_REMOVE_TIMER, 
                timerName,
                self.skillId
            )

        if tid:
            if owner.cancelTimerCB(tid, timerTag) == gameconst.TIMER_CANCEL_RET_MISMATCH and owner.IsAvatar:
                owner.skillTimerLogQueue.errReportLogQueue()
            owner.skillTimerDic.pop(tid, None)
            return True
        return False

    def clearTempData(self):
        changeSkillCDStatus = self.tempData.get(gameconst.SkillTempDataKey.CHANGE_SKILL_CD_STATUS, None)
        self.tempData.clear()
        if changeSkillCDStatus and changeSkillCDStatus in gameconst.SkillCDStatus.VALID:
            self.tempData[gameconst.SkillTempDataKey.CHANGE_SKILL_CD_STATUS] = changeSkillCDStatus

    def needResetOnSkillDone(self, owner):
        # 如果是限时刷新技能先不reset，等超时没使用或刷新的技能用完了再reset

        if self.hasTempData(gameconst.SkillTempDataKey.RESTORE_CD_TIMER):
            return False
        return True

    def resetSkill(self, owner, reason=gameconst.ResetSkillReason.ReasonDefault, doRemoveState=True):
        owner.debugCombatMsg('resetSkill: skillId:%s, resetSkillReason:%s, doRemoveState:%s', self.skillId, reason, doRemoveState)
        self.isInSkill = False
        owner.removeUsingSkillRecord(self.skillId)
        _skillState = self.getSkillState()
        if owner.hasState(_skillState) and doRemoveState:
            owner.removeState(_skillState)

        if self.hasSkillTag(gameconst.SkillTagEnum.Channel):
            owner.removeState(gameconst.StateEnum.UsingSkill)

        if self._cancelTempTimer(owner, gameconst.SkillTempDataKey.RESTORE_CD_TIMER, gametimer.TIMER_TAG_RESTORE_CD):
            self.onInvalidateRefreshCD(owner, doReset=False)

        self._cancelTempTimer(owner, gameconst.SkillTempDataKey.DELAY_CALC_TIMER, gametimer.TIMER_TAG_SKILL_DELAY_CALC)
        self._cancelTempTimer(owner, gameconst.SkillTempDataKey.SKILL_DONE_TIMER, gametimer.TIMER_TAG_SKILL_DONE)
        self._cancelTempTimer(owner, gameconst.SkillTempDataKey.MUL_ATTACK_ACT_TIMER, gametimer.TIMER_TAG_DO_SKILL_ACTION)
        self.clearTempData()
        self.targetIds = []

    def childSkills(self):
        return ()

# 普通技能
class CommonSkillVal(SkillBaseClass):
    def getSkillState(self):
        if self.hasSkillTag(gameconst.SkillTagEnum.Channel):
            if self.isMovingSkill(self.skillId):
                return gameconst.StateEnum.moveChannel

            return gameconst.StateEnum.Channeling
        elif self.hasSkillTag(gameconst.SkillTagEnum.GeneralSkill):
            return gameconst.StateEnum.GeneralAttack
        else:
            if self.isMovingSkill(self.skillId):
                return gameconst.StateEnum.moveSkill

            return gameconst.StateEnum.UsingSkill

    # 获得最底层的skill，也就是存在skillDic里的技能对象
    # parentSkill指向：
    # 有劫：self<-enhancedSkill<-next stage of enhancedSkill, self.enhancedSkill上stageIndex表示段数，self.stageIndex没用
    # 没有劫：self<-next state of self， self.stageIndex表示段数
    def getRootSkillVal(self):
        _rootSkill = self
        while _rootSkill.parentSkill:
            _rootSkill = _rootSkill.parentSkill
        return _rootSkill

    def getNotifyClientSkillId(self):
        return self.skillId, self.skillLv

    def beginUseSkill(self, owner, targetId, skillArgs, compensateTime, isSetState=True, enterCD=True, parentCtx=None, isRecord=False):
        if not isRecord:
            owner.recordUsingSkill(self, parentCtx.useTargetId)
    
        _isSucc = self.doBeginUseSkill(
            owner, 
            targetId, 
            skillArgs,
            compensateTime,
            isSetState, 
            enterCD, 
            parentCtx)

        if not _isSucc:
            owner.client.onUseSkill(False, self.skillId, targetId, [], [], [])

        return _isSucc

    def beginUseSkillStartAction(self, owner, targetId, skillArgs, isSetState=True, enterCD=True, parentCtx=None):
        self.isInSkill = True
        self.setTempData(owner, gameconst.SkillTempDataKey.SKILL_ARGS, skillArgs)
        owner.debugCombatMsg('SkillBaseClass.beginUseSkillStartAction: skillId:%s, targetId:%s, skillArgs:%s', self.skillId, targetId, skillArgs)
        _target = KBEngine.entities.get(targetId)
        _startAction = self.getStartAction(self.skillId)
        _startActionFail = False
        startActionResult = gameconst.StartActionResult.Success

        if self.hasTempData(gameconst.SkillTempDataKey.RESTORE_CD_TIMER):
            self._cancelTempTimer(owner, gameconst.SkillTempDataKey.RESTORE_CD_TIMER, gametimer.TIMER_TAG_RESTORE_CD)
            self.onInvalidateRefreshCD(owner, doReset=False)

        _extraEventId = self.getSkillEvent(self.skillId)
        if _extraEventId:
            owner.checkConflictState(_extraEventId, remConflctState=True)

        if isSetState:
            _skillState = self.getSkillState()
            owner.setState(_skillState)

        _realSkillArgs = skillArgs
        _positionSkillArgs = None
        if self.isChangePosSkill(self.skillId):
            _realSkillArgs = list(skillArgs)[:-3]
            _positionSkillArgs = tuple(skillArgs[-3:])

        effectedEntIds = self.getEffectTargets(owner, targetId, _realSkillArgs, positionSkillArgs=_positionSkillArgs, context = parentCtx)
        _skillResult = SkillDamges(owner.id)
        actionCtx = actionContext.UseSkillCtx(
            owner.id, 
            self.skillId, 
            skillArgs, 
            targetId, 
            effectedEntIds, 
            self,
            _skillResult, 
            parentCtx=parentCtx)

        actionCtx.actionProgress = gameconst.ActionProgressEnum.startActionDone
        if _startAction:
            # start action先不给传effectedEntIds，因为可能还没开始结算
            # start action里加的buff什么的不能依赖在技能action里解除,技能可能在延迟后不能执行action
            # 例如旋风斩开始加的无敌需要在end action去删除
            ctxFunc = lambda r: actionCtx
            if owner.doCombatActions(_startAction, owner, _target, owner.id, ctxFunc) is False:
                _startActionFail = True
                startActionResult = gameconst.StartActionResult.Fail

        if _startActionFail:
            owner.debugCombatMsg('SkillBaseClass.beginUseSkillStartAction do _startAction fail: skillId:%s, targetId:%s, ownerPosition:%s', self.skillId, targetId, owner.position)
            self.useSkillDone(owner, targetId, skillArgs, isSucc=False, startActionFail=_startActionFail)
            return startActionResult, None, None
        elif utils.hasSkillTagById(self.skillId, gameconst.SkillTagEnum.UltraSkill):
            owner.ultraSkillPower = 0

        if (not owner.IsAvatar or owner.gmModeCell != gameconst.GmModeEnum.GM_NO_SKILLCD) and enterCD and not self.hasSkillTag(
                gameconst.SkillTagEnum.Channel):
            host = owner.getAvatar()
            LOG_DBG("in beginUseSkillStartAction ", owner, self.skillId, owner.IsAvatar, host, targetId, skillArgs)
            if host:
                addValue = 0
                ret, datas = host.getInscriptionEffects(self.skillId, gameconst.InscriptionEffectType.SKILL_RELEASE_ADD_COUNT)
                if ret:
                    if len(datas) == 1:
                        addValue = datas[0]
                        LOG_INFO("in beginUseSkillStartAction, inscription effect is triggered, skill_id:{0}, effect_type{1}, effect_value{2}", self.skillId, gameconst.InscriptionEffectType.SKILL_RELEASE_ADD_COUNT, datas)

                releasedCount = self.getTempData(gameconst.SkillTempDataKey.RELEASED_CNT, 0)
                totalReleaseCount = self.getTempData(gameconst.SkillTempDataKey.TOTAL_RELEASE_CNT, 0)
                # 激活条件
                if releasedCount == 0 or releasedCount != totalReleaseCount:
                    self.setTempData(owner, gameconst.SkillTempDataKey.RELEASED_CNT, addValue + 1)
                    self.setTempData(owner, gameconst.SkillTempDataKey.TOTAL_RELEASE_CNT, addValue + 1)
                    self.setTempData(owner, gameconst.SkillTempDataKey.RELEASE_TIME, time.time())
                # 消耗一次
                if releasedCount > 0:
                    self.setTempData(owner, gameconst.SkillTempDataKey.RELEASED_CNT, releasedCount - 1)
            self.doEnterCDTime(owner)
            owner.client.onSetAddSkillCd(self.skillId, float(self.getCDDur(owner)), float(self.tNextCast), False, self.getTempData(gameconst.SkillTempDataKey.RELEASE_TIME, 0), self.getTempData(gameconst.SkillTempDataKey.TOTAL_RELEASE_CNT, 0), self.getTempData(gameconst.SkillTempDataKey.RELEASED_CNT, 0), not self.isSkillCDStatusFrozen())

        owner.IsAvatar and owner.modifyMP(-self.getCostMp(owner, self.skillId, owner.mpCostRatio))

        # _startAction里可能会攻击别人然后被反噬死。。
        if owner.isDie():
            owner.debugCombatMsg('SkillBaseClass.beginUseSkillStartAction die after _startAction: skillId:%s, ownerId:%s, targetId:%s, ownerPosition:%s', self.skillId, owner.id, targetId,
                                 owner.position)
            self.useSkillDone(owner, targetId, skillArgs, isSucc=False, startActionFail=_startActionFail)
            return gameconst.StartActionResult.Fail, None, None

        return startActionResult, actionCtx, effectedEntIds

    def doBeginUseSkill(self, owner, targetId, skillArgs, compensateTime, isSetState=True, enterCD=True, parentCtx=None):
        _isSucc, _actionCtx, effectTargetIds = self.beginUseSkillStartAction(
            owner, 
            targetId, 
            skillArgs,
            isSetState, 
            enterCD, 
            parentCtx)

        skillId, skillLv = self.getNotifyClientSkillId()
        skillArgsExtra = [self.getRange(owner, skillId, skillLv), self.getEffectRange(owner, skillId, skillLv)]
        if not _isSucc:
            owner.client.onUseSkill(False, skillId, targetId, [], [], [])
            return _isSucc

        if self.isChangePosSkill(self.skillId):
            if len(skillArgs) <= 3:
                _target = KBEngine.entities.get(targetId)
                positionArgs = self.getSkillDesPosition(owner, _target, skillArgs)
                skillArgs = skillArgs + positionArgs

        calcDelay = self.getSkillResultDelay(owner, targetId, compensateTime)
        # ChannelingSkillVal废除，因为吟唱后也需要可以引导，所以把引导合并到CommonSkillVal
        if self.hasSkillTag(gameconst.SkillTagEnum.Channel):
            owner.setTempMiscProp(gameconst.EntityPropsEnum.currentChannelSkill, self)

            owner.debugCombatMsg('CommonSkillVal.doBeginUseSkill channel skill: skillId:%s, targetId:%s, skillArgs:%s, compensateTime:%s, ownerPosition:%s, calcDelay:%s', 
                                 self.skillId, targetId, skillArgs, compensateTime, owner.position, calcDelay)
            self.startChanneling(owner, targetId, skillArgs, calcDelay, _actionCtx)
            owner.allClients.onUseSkill(_isSucc, skillId, targetId, skillArgs, effectTargetIds, skillArgsExtra)
        else:
            owner.debugCombatMsg('CommonSkillVal.doBeginUseSkill: skillId:%s, targetId:%s, skillArgs:%s, compensateTime:%s, calcDelay:%s', self.skillId, targetId, skillArgs, compensateTime, calcDelay)

            if _actionCtx.actionProgress == gameconst.ActionProgressEnum.startActionDone:
                if calcDelay > 0:
                    if self.needReleaseTarget() and not (owner.IsMonster and self.isMultiCastSkill(owner, _actionCtx)):
                        self.targetIds = effectTargetIds

                    self.setTimerTempData(owner, 
                        gameconst.SkillTempDataKey.DELAY_CALC_TIMER,
                        owner.addTimerCB(
                            calcDelay + 0.1,
                            'delayCalcSkill',
                            (
                                self, targetId,
                                skillArgs,
                                _actionCtx,
                                calcDelay,
                                isSetState),
                            gametimer.TIMER_TAG_SKILL_DELAY_CALC))

                    owner.allClients.onUseSkill(True, skillId, targetId, skillArgs,
                                                effectTargetIds, skillArgsExtra)
                else:
                    # 保证onUseSkill在_doUseSkill前
                    self.targetIds = effectTargetIds
                    if owner.isReal():
                        owner.allClients.onUseSkill(True, skillId, targetId, skillArgs,
                                                    effectTargetIds, skillArgsExtra)
                    owner._doUseSkill(self, targetId, skillArgs, _actionCtx, calcDelay, isSetState)

        return _isSucc

    def startChanneling(self, caster, targetID, arr, delayTime, actionCtx):
        self.channelCount = 0
        timerId = caster.addTimerCB(delayTime, 'channelingSkillTick',
                                   (self, targetID, arr, tuple(caster.position), actionCtx),
                                   gametimer.TIMER_TAG_CHANNELING_CALC)
        self.setTimerTempData(caster, gameconst.SkillTempDataKey.CHANNELING_CALC_TIMER, timerId)
        self.setTempData(caster, gameconst.SkillTempDataKey.T_CHANNELING_START, time.time() + delayTime)

    def calBulletTime(self, owner, targetId):
        _target = KBEngine.entities.get(targetId)
        if _target:
            _bulletTimeScale = self.getBulletTimeScale(self.skillId)
            _timeEx = self.getBulletFxTime(self.skillId) * (
                    1 - _bulletTimeScale + _bulletTimeScale * sMath.distance2D(owner.position,
                                                                             _target.position) / self.getRange(owner, self.skillId, self.skillLv))
        else:
            _timeEx = self.getBulletFxTime(self.skillId) if self.getBulletFxTime(self.skillId) else 0.5
        return _timeEx

    def onChannelingEnd(self, owner, isFinished):
        owner._endChannelingSkill()
        self.useSkillDone(owner, 0, self.popTempData(gameconst.SkillTempDataKey.SKILL_ARGS, []))

    def onChannlingEffectEnd(self, owner):
        _postSkillTime = self.getSkillTime(self.skillId)
        owner.removeState(self.getSkillState(), removeReason=gameconst.ChannelingBreak.BREAK_TP_NORMAR_END)
        self.doEnterCDTime(owner)
        owner.client.onSetAddSkillCd(self.skillId, float(self.getCDDur(owner)), float(self.tNextCast), False, self.getTempData(gameconst.SkillTempDataKey.RELEASE_TIME, 0), self.getTempData(gameconst.SkillTempDataKey.TOTAL_RELEASE_CNT, 0), self.getTempData(gameconst.SkillTempDataKey.RELEASED_CNT, 0), not self.isSkillCDStatusFrozen())
        if _postSkillTime > 0:
            owner.setState(gameconst.StateEnum.UsingSkill)
            endTimer = owner.addTimerCB(_postSkillTime, '_onSkillCallback', (self, 'onChannelingEnd', (True,)),
                                       gametimer.TIMER_TAG_ON_CHANNELING_END)
            self.setTimerTempData(owner, gameconst.SkillTempDataKey.CHANNELING_END_TIMER, endTimer)
        else:
            self.onChannelingEnd(owner, True)

    def resetSkill(self, owner, reason=gameconst.ResetSkillReason.ReasonDefault, doRemoveState=True):
        if self.hasSkillTag(gameconst.SkillTagEnum.Channel):
            self._cancelTempTimer(owner, gameconst.SkillTempDataKey.CHANNELING_CALC_TIMER, gametimer.TIMER_TAG_CHANNELING_CALC)
            self._cancelTempTimer(owner, gameconst.SkillTempDataKey.CHANNELING_BULLET_TIMER, gametimer.TIMER_TAG_CHANNELING_SKILL_EFFECT)
            self._cancelTempTimer(owner, gameconst.SkillTempDataKey.CHANNELING_END_TIMER, gametimer.TIMER_TAG_ON_CHANNELING_END)
            self.popTempData(gameconst.SkillTempDataKey.IS_CHANNELING_EMPTY, False)
            self.channelCount = 0

        if self.hasSkillTag(gameconst.SkillTagEnum.Lunge) and owner.hasState(gameconst.StateEnum.Shifting):
            owner.onEndLunge(self, 0, [])

        super(CommonSkillVal, self).resetSkill(owner, reason, doRemoveState)


class ChongfengSkillVal(CommonSkillVal):
    def getSkillState(self):
        if self.isMovingSkill(self.skillId):
            return gameconst.StateEnum.moveSkill

        return gameconst.StateEnum.UsingSkill

    def resetSkill(self, owner, reason=gameconst.ResetSkillReason.ReasonDefault, doRemoveState=True):
        if owner.hasState(gameconst.StateEnum.Shifting):
            owner.onEndChongfeng(self, 0, [])
        super(ChongfengSkillVal, self).resetSkill(owner, reason, doRemoveState)


# 刺客突进技能
class LungeSkillVal(CommonSkillVal):
    def getSkillState(self):
        if self.isMovingSkill(self.skillId):
            return gameconst.StateEnum.moveSkill

        return gameconst.StateEnum.UsingSkill

    def resetSkill(self, owner, reason=gameconst.ResetSkillReason.ReasonDefault, doRemoveState=True):
        if owner.hasState(gameconst.StateEnum.Shifting):
            owner.onEndLunge(self, 0, [])
        super(LungeSkillVal, self).resetSkill(owner, reason, doRemoveState)

    def checkSkillArgs(self, owner, args):
        _scopeType = self.getScope(self.skillId)
        if _scopeType:
            return super(LungeSkillVal, self).checkSkillArgs(owner, args)

        _dstPos = args[-3:]
        return self.inRange(owner, _dstPos, True, 0)


# 闪避技能
class DodgeSkillVal(CommonSkillVal):
    def getSkillState(self):
        return gameconst.StateEnum.Dodging

    def getLastBlinkBeginPos(self, owner):
        usingSkills = owner.getTempMiscProp(gameconst.EntityPropsEnum.currentUseSkill, default={})
        for sid, (_skillVal, _tid) in usingSkills.items():
            if not _skillVal.isChangePosSkill(sid):
                continue

            _pos = _skillVal.getTempData(gameconst.SkillTempDataKey.BEGIN_SKILL_POSITION)
            # 如果是None说明真正的移动还没开始
            if _pos is None:
                return owner.position
            else:
                return _pos
        
        return None

    def beginUseSkill(self, owner, targetId, skillArgs, compensateTime, isSetState=True, enterCD=True, parentCtx=None, isRecord=False):
        # owner.resetUsingSkills(gameconst.ResetSkillReason.ReasonDodgeSkill)
        _pos = self.getLastBlinkBeginPos(owner)
        if _pos:
            parentCtx.lastBlinkPos = _pos
        LOG_DBG("beginUseSkill ", _pos, parentCtx.lastBlinkPos, targetId, skillArgs)
        owner.breakSkillByState()
        owner.recordUsingSkill(self, parentCtx.useTargetId)
        return super(DodgeSkillVal, self).beginUseSkill(
            owner, 
            targetId, 
            skillArgs,
            compensateTime,
            isSetState, 
            enterCD, 
            parentCtx,
            isRecord=True
            )

    def resetSkill(self, owner, reason=gameconst.ResetSkillReason.ReasonDefault, doRemoveState=True):
        if owner.hasState(gameconst.StateEnum.Dodging):
            owner.endDodge(self, 0, [])
        super(DodgeSkillVal, self).resetSkill(owner, reason, doRemoveState)


# 吟唱技能:多一个吟唱的普通技能
class CastingSkillVal(CommonSkillVal):
    def __init__(self, skillId, skillLv, tNextCast=0.0, cdDelta=0.0, parentSkill=0, **kwargs):
        super(CastingSkillVal, self).__init__(skillId, skillLv, tNextCast, cdDelta, parentSkill)
        self.castingStartTime = 0

    def checkUseSkill(self, owner, targetID, ignoreReasons=0, checkInRange=True):
        _realSkillVal, _ = self.getRealSkillVal(owner)
        if _realSkillVal != self:
            ret = super(CastingSkillVal, self).checkUseSkill(owner, targetID, ignoreReasons, checkInRange)
        else:
            castingSucc = self.isCastingSucc()
            if castingSucc:
                ignoreReasons |= gameconst.UseSkillCheck.USC_ENUM_OUT_OF_RANGE

            ret = super(CastingSkillVal, self).checkUseSkill(owner, targetID, ignoreReasons, checkInRange)

            if not castingSucc:
                code = gameconst.UseSkillCheck.USC_ENUM_NEED_CAST
                if not code & ignoreReasons:
                    LOG_INFO('use casting skill before finishing casting', self.skillId, time.time(),
                              self.getCastingtimeMax(self.skillId), self.castingStartTime)
                    return code | ret

            elif ret == gameconst.UseSkillCheck.USC_ENUM_CHEKC_OK:
                _target = KBEngine.entities.get(targetID)
                if _target and self.needReleaseTarget() and not sMath.inRange2D(gameconst.DEFAULT_AOI, owner.position,
                                                                               _target.position):
                    code = gameconst.UseSkillCheck.USC_ENUM_OUT_OF_RANGE
                    if not code & ignoreReasons:
                        return code

        return ret

    def onChangedFromSkill(self, fromSkillVal):
        super(CastingSkillVal, self).onChangedFromSkill(fromSkillVal)
        if fromSkillVal.hasSkillTag(gameconst.SkillTagEnum.Casting):
            self.castingStartTime = fromSkillVal.castingStartTime

    def getEffectTargets(self, caster, targetId, arr, forceTarget=False, positionSkillArgs=None, context=None):
        _target = KBEngine.entities.get(targetId)
        if (targetId > 0 and not _target) or not caster:
            targetId = 0

        forceTarget = self.needReleaseTarget()

        _targetIds = super(CastingSkillVal, self).getEffectTargets(caster, targetId, arr, forceTarget, positionSkillArgs, context)

        return _targetIds

    def startCasting(self, caster, actionCtx):
        if caster.IsAvatar and caster.mp < self.getCostMp(caster, self.skillId, caster.mpCostRatio):
            return

        self.castingStartTime = time.time()

        tid = caster.addTimerCB(1, 'castingSkillCheck', (actionCtx.useTargetId, actionCtx.skillArgs, tuple(caster.position)),
                               gametimer.TIMER_TAG_CASTING_CHECK)
        self.setTimerTempData(caster, gameconst.SkillTempDataKey.CASTING_CHECK_TIMER, tid)
        # caster.setTempMiscProp(gameconst.EntityPropsEnum.castingCheckTimer, checkTimer)

        # #主角由客户端发起释放，其他实体服务器自动放
        # 可能是action里cast的技能，直接用技能对象放
        castingTime = self.getCastingtimeMax(self.skillId)
        useTimer = caster.addTimerCB(castingTime, '_useSkillBySkillObj', (self, actionCtx),
                                    gametimer.TIMER_TAG_CASTING_SKILL)
        self.setTimerTempData(caster, gameconst.SkillTempDataKey.CASTING_SKILL_TIMER, useTimer)

        castingAction = self.getSkillCfg(self.skillId).get('castingAction')
        if castingAction:
            _target = KBEngine.entities.get(actionCtx.useTargetId)
            castingAction(caster, _target, actionContext.SkillCommonCtx(self.skillId))

    def onCastingInterrupted(self, owner, reason):
        self.castingStartTime = 0
        cdType = self.getSkillCfg(self.skillId).get('CDAfterInterrupt', 0)

        _needCd = False
        if cdType == gameconst.CastingSkillCDType.IgnoreMove:
            if reason not in (
                    gameconst.EndCasting.ECEnumMove, gameconst.EndCasting.ECEnumClientCancel, gameconst.EndCasting.ECEnumMissingTarget,
                    gameconst.EndCasting.ECEnumDead, gameconst.EndCasting.ECEnumTeleporting, gameconst.EndCasting.ECEnumclientPick):
                _needCd = True
        elif cdType == gameconst.CastingSkillCDType.EnterCD:
            _needCd = True
        elif cdType == gameconst.CastingSkillCDType.NotEnterCD:
            pass

        if _needCd:
            super(CastingSkillVal, self).doEnterCDTime(owner)
            owner.client.onSetAddSkillCd(self.skillId, float(self.getCDDur(owner)), float(self.tNextCast), False, self.getTempData(gameconst.SkillTempDataKey.RELEASE_TIME, 0), self.getTempData(gameconst.SkillTempDataKey.TOTAL_RELEASE_CNT, 0), self.getTempData(gameconst.SkillTempDataKey.RELEASED_CNT, 0), not self.isSkillCDStatusFrozen())

        owner.IsAICombatUnit and owner.aiController and owner.aiController.onCastingInterrupted(self.skillId)

    def isCastingSucc(self, delta=0.5):
        if not self.castingStartTime:
            return False
        else:
            return time.time() - self.castingStartTime >= self.getCastingtimeMax(self.skillId) - delta

    def useSkillDone(self, owner, targetId, skillArgs, isSucc=True, startActionFail=False, doRemoveState=True, forceResetSkill=False):
        super(CastingSkillVal, self).useSkillDone(owner, targetId, skillArgs, isSucc, startActionFail, forceResetSkill=forceResetSkill)
        self.castingStartTime = 0

    def resetSkill(self, owner, reason=gameconst.ResetSkillReason.ReasonDefault, doRemoveState=True):
        if reason != gameconst.ResetSkillReason.ReasonEndCasting:
            castingSkillVal = owner.getCastingSkillInfo()
            if castingSkillVal and castingSkillVal.skillId == self.skillId:
                owner.removeState(gameconst.StateEnum.Casting)
        self._cancelTempTimer(owner, gameconst.SkillTempDataKey.CASTING_CHECK_TIMER, gametimer.TIMER_TAG_CASTING_CHECK)
        self._cancelTempTimer(owner, gameconst.SkillTempDataKey.CASTING_SKILL_TIMER, gametimer.TIMER_TAG_CASTING_SKILL)
        # self.castingStartTime = 0      #这个只能在startCasting时重置或使用成功后重置
        super(CastingSkillVal, self).resetSkill(owner, reason, doRemoveState)


class StagedSkill(CommonSkillVal):
    def __init__(self, skillId, skillLv, tNextCast=0.0, cdDelta=0.0, parentSkill=0, **kwargs):
        super(StagedSkill, self).__init__(skillId, skillLv, tNextCast, cdDelta, parentSkill)
        self.stageIndex = 0

    def checkUseSkill(self, owner, targetId, ignoreReasons=0, checkInRange=True):
        _realSkillVal, _ = self.getRealSkillVal(owner)
        if _realSkillVal == self:
            return super(StagedSkill, self).checkUseSkill(owner, targetId, ignoreReasons, checkInRange)

        return _realSkillVal.checkUseSkill(owner, targetId, ignoreReasons, checkInRange)

    def canRemoveFromBuild(self):
        return self.stageIndex == 0 and super(StagedSkill, self).canRemoveFromBuild()

    def childSkills(self):
        _dic = self.getTempData(gameconst.SkillTempDataKey.STAGE_CHILD, {})
        _retList = []
        for _skill in _dic.values():
            _retList.append(_skill)

        return _retList

    def getRealSkillVal(self, owner):
        if self.stageIndex == 0:
            return self, False
        else:
            _curStageSkillId = self.getSkillIdForStage(self.stageIndex)
            if not _curStageSkillId:
                return self, False

            childDic = self.getTempData(gameconst.SkillTempDataKey.STAGE_CHILD, {})
            if _curStageSkillId in childDic:
                return childDic[_curStageSkillId], False

            curStageSkill = StagedSkill(_curStageSkillId, self.skillLv, parentSkill=self)
            childDic[_curStageSkillId] = curStageSkill

            self.setTempData(owner, gameconst.SkillTempDataKey.STAGE_CHILD, childDic)
            return curStageSkill, False

    def getSkillIdForStage(self, stageIndex):
        if stageIndex == 0:
            return self.skillId
        _stageSkillIds = self.getSkillCfg(self.skillId).get('mulSkillID')
        if _stageSkillIds and len(_stageSkillIds) >= stageIndex:
            return _stageSkillIds[stageIndex - 1]
        return 0

    def beginUseSkill(self, owner, targetId, skillArgs, compensateTime, isSetState=True, enterCD=True, parentCtx=None, isRecord=False):
        rootSkillVal = self.getRootSkillVal()
        owner.debugCombatMsg('StageSkill.beginUseSkill: skillId:%s, stageIndex:%s, targetId:%s, skillArgs:%s, isSetState:%s, rootSkillId:%s',
                             self.skillId, self.stageIndex, targetId, skillArgs,
                             isSetState, rootSkillVal.skillId)
        nextStageSkillId = self.getSkillIdForStage(self.stageIndex + 1)
        owner.recordUsingSkill(self, parentCtx.useTargetId)
        # 如果有下一段就不进入cd
        enterCD = (nextStageSkillId == 0)
        if self.stageIndex == 0:
            if self is rootSkillVal:
                self.gotoNextStage(owner)

            isSucc = self.doBeginUseSkill(
                owner, 
                targetId, 
                skillArgs,
                compensateTime, 
                isSetState,
                enterCD, 
                parentCtx)
        else:
            curStageSkill, _ = self.getRealSkillVal(owner)
            if curStageSkill is self:
                raise Exception('ckz curStageSkill is self', self.skillId, self.stageIndex, owner.gbId)

            if self is rootSkillVal:
                self.gotoNextStage(owner)

            isSucc = curStageSkill.beginUseSkill(
                owner, targetId, skillArgs,
                compensateTime, isSetState, enterCD,
                parentCtx, isRecord=True)

        if isSucc:
            if self.hasTempData(gameconst.SkillTempDataKey.STAGE_CD_TIMER):
                self._cancelTempTimer(owner, gameconst.SkillTempDataKey.STAGE_CD_TIMER, gametimer.TIMER_TAG_ON_STAGE_END)
                self.popTempData(gameconst.SkillTempDataKey.STAGE_CD_TIMER)
        else:
            return gameconst.StartActionResult.Fail

        if nextStageSkillId:
            # 只有root技能才能走到这里，子技能是走不到的，所以onStageEnd是只有root才会调用
            stageDuration = S_SD.datas[nextStageSkillId]['mulSkillCD']
            cdTimer = owner.addTimerCB(stageDuration, '_onSkillCallback', (self, 'onStageEnd', (True,)),
                                        gametimer.TIMER_TAG_ON_STAGE_END)
            self.setTimerTempData(owner, gameconst.SkillTempDataKey.STAGE_CD_TIMER, cdTimer)

            clientStageIdx = self.stageIndex
        else:
            clientStageIdx = 0

        ##阶段技能只有普通技能的第一段以及强化后的第一段可以给客户端提交相关数据
        stageSkillIds = self.getSkillCfg(self.skillId).get('mulSkillID')
        curTime = time.time()
        stageSkillIds and owner.IsAvatar and owner.allClients.onUseStageSkill(rootSkillVal.skillId, clientStageIdx,
                                                                                curTime)

        return isSucc

    def gotoNextStage(self, owner):
        self.stageIndex += 1
        if self.checkLastStage(owner):
            self.onStageEnd(owner)

    def checkLastStage(self, owner):
        # stageIndex是下次释放技能的stage
        return not self.getSkillIdForStage(self.stageIndex)

    # 超时或放完最后一段结束多段技能
    def onStageEnd(self, owner, endByTimeout=False):
        # 目前只有root才会走到这里
        self._cancelTempTimer(owner, gameconst.SkillTempDataKey.STAGE_CD_TIMER, gametimer.TIMER_TAG_ON_STAGE_END)
        rootSkillVal = self.getRootSkillVal()
        owner.debugCombatMsg('StageSkill.onStageEnd: skillId:%s, rootSkillId:%s, rootSkillStageIndex:%s',
                             self.skillId, rootSkillVal.skillId, rootSkillVal.stageIndex)
        rootSkillVal.doEnterCDTime(owner)
        owner.client.onSetAddSkillCd(rootSkillVal.skillId, float(rootSkillVal.getCDDur(owner)),
                                     float(rootSkillVal.tNextCast), False, rootSkillVal.getTempData(gameconst.SkillTempDataKey.RELEASE_TIME, 0), rootSkillVal.getTempData(gameconst.SkillTempDataKey.TOTAL_RELEASE_CNT, 0), rootSkillVal.getTempData(gameconst.SkillTempDataKey.RELEASED_CNT, 0), not rootSkillVal.isSkillCDStatusFrozen())

        if endByTimeout:
            self.resetSkill(owner)

    def useSkillDone(self, owner, targetId, skillArgs, isSucc=True, startActionFail=False, doRemoveState=True, forceResetSkill=False):
        rootSkillVal = self.getRootSkillVal()
        # 获取子技能列表一定要放前面，因为reset之后 tempData就变成空的了
        _children = self.childSkills()
        CommonSkillVal.useSkillDone(self, owner, targetId, skillArgs, isSucc, startActionFail, forceResetSkill=forceResetSkill)
        if forceResetSkill:
            # 如果是force情况下，一定是自上而下的
            if self is rootSkillVal:
                for _child in _children:
                    _child.useSkillDone(owner, targetId, skillArgs, isSucc, startActionFail, forceResetSkill=forceResetSkill)

        else:
            if self is not rootSkillVal and rootSkillVal.checkLastStage(owner):
            # 多段技能结束，通知父技能Done, 多段的技能不能设置force，不然可能会无限循环
                rootSkillVal.useSkillDone(owner, targetId, skillArgs, isSucc, startActionFail, forceResetSkill=False)

    def needResetOnSkillDone(self, owner):
        # 如果技能使用成功且还有下一段就先不reset，否则被reset到第一段了,等着onStageEnd里去reset
        rootSkillVal = self.getRootSkillVal()
        if self.checkLastStage(owner):
            return True

        if self is rootSkillVal:
            return False

        return True

    def resetSkill(self, owner, reason=gameconst.ResetSkillReason.ReasonDefault, doRemoveState=True):
        if reason == gameconst.ResetSkillReason.ReasonTeleport or reason == gameconst.ResetSkillReason.ReasonTransform or reason == gameconst.ResetSkillReason.ReasonDuelComplete:
            if self.stageIndex > 0:
                self.doEnterCDTime(owner)
                owner.client.onSetAddSkillCd(
                    self.skillId, 
                    float(self.getCDDur(owner)), 
                    float(self.tNextCast), 
                    False, 
                    self.getTempData(gameconst.SkillTempDataKey.RELEASE_TIME, 0), 
                    self.getTempData(gameconst.SkillTempDataKey.TOTAL_RELEASE_CNT, 0), 
                    self.getTempData(gameconst.SkillTempDataKey.RELEASED_CNT, 0), 
                    not self.isSkillCDStatusFrozen())

                _rootSkillVal = self.getRootSkillVal()
                if owner.IsAvatar:
                    owner.client.onUseStageSkill(_rootSkillVal.skillId, 0, time.time())

        self.stageIndex = 0
        self._cancelTempTimer(owner, gameconst.SkillTempDataKey.STAGE_CD_TIMER, gametimer.TIMER_TAG_ON_STAGE_END)

        super(StagedSkill, self).resetSkill(owner, reason, doRemoveState)


# 超级技能
class UltraSkillVal(CommonSkillVal):
    def getSkillState(self):
        return gameconst.StateEnum.speicalSkill


def fetchSkillClass(skillId):
    skillData = SkillBaseClass.getSkillCfg(skillId)
    if not skillData:
        return
    tags = SkillBaseClass.getTag(skillId)

    if gameconst.SkillTagEnum.Casting in tags:
        return CastingSkillVal
    elif gameconst.SkillTagEnum.Chongfeng in tags:
        return ChongfengSkillVal
    elif gameconst.SkillTagEnum.Lunge in tags:
        return LungeSkillVal
    elif gameconst.SkillTagEnum.MulStageSkill in tags:
        return StagedSkill
    elif gameconst.SkillTagEnum.DodgeSkill in tags:
        return DodgeSkillVal
    elif gameconst.SkillTagEnum.UltraSkill in tags:
        return UltraSkillVal
    else:
        return CommonSkillVal
