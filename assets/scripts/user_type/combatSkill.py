# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine

import time
import sys
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
import formula
import weakref

import skill_skill as SSD
import message_Message_def as MMD
import conflict_conflict_def as CCD
import conflict_status as CSD
import fx_fx as FF
import const_const as CONST
import skillRelevant_skillConst as SRSC
import dataUtils
import gameclass
import functools
import gametimer
import gameconst


class ServerSkills(userType.UserDictType):
    """SERVER_SKILLS"""

    def __init__(self):
        self.skillSwitches = {}

    def doAddSkill(self, owner, skillId, skillLv, **kwargs):
        if skillId not in self:
            skillClass = getSkillClass(skillId)
            self[skillId] = skillClass(skillId, skillLv, **kwargs)
            # 初始默认都是开启的
            if skillId not in self.skillSwitches:
                switchStatus = gameconst.SkillSwitchStatus.AUTO
                # 针对玩家的技能释放处理
                if owner.IsAvatar:
                    # autoFightUseSkill设置1表示不会自动释放
                    if SSD.datas.get(skillId, {}).get("autoFightUseSkill", 0) == gameconst.SkillSwitchStatus.MANUAL:
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
        skills = []
        skillCDStatus = []
        for skillId, skillInstance in self.items():
            skillDict = {
                'skillId': skillId,
                'tNextCast': skillInstance.tNextCast,
                'skillCd': skillInstance.getCD(owner),
                'extraSkillLv': skillInstance.getExtraLv(owner),
            }
            skills.append(skillDict)
            # 技能CD状态
            cdStatus = skillInstance.getTempData(gameconst.SkillTempDataKey.CHANGE_SKILL_CD_STATUS, gameconst.SkillCDStatus.DEFAULT)
            if cdStatus != gameconst.SkillCDStatus.DEFAULT:
                skillCDStatu = {
                    'skillId': skillId,
                    'cdStatus': cdStatus
                }
                skillCDStatus.append(skillCDStatu)

        skillSwitches = []
        for skillId, skillSwitch in self.skillSwitches.items():
            skillDict = {
                'skillId':skillId,
                'switchStatus':skillSwitch
            }
            skillSwitches.append(skillDict)

        clientData = {
            'skills': skills,
            'skillSwitches': skillSwitches,
            'skillCDStatus': skillCDStatus,
        }
        return clientData

    def toDict(self):
        skillDict = {'skills': []}
        for skillId, sVal in self.items():
            sDict = {
                'skillId': skillId,
                'skillLv': sVal.skillLv,
                'tNextCast': float(sVal.tNextCast),
                'cdDelta': float(sVal.cdDelta),
            }
            skillDict['skills'].append(sDict)
        skillDict['skillSwitches'] = self.skillSwitches
        return skillDict

    def checkSkillSwitch(self, skillID, status):
        switchStatus = self.skillSwitches.get(skillID, None)
        if switchStatus is None:
            return False
        return switchStatus == status

    def getSkillSwitch(self, skillID):
        return self.skillSwitches.get(skillID, gameconst.SkillSwitchStatus.AUTO)

    def setSkillSwitch(self, owner, skillID, status):
        skillID, _ = owner.glyphEquipData.getInscriptionSrcSkillId(skillID)
        if not SSD.datas.get(skillID, None):
            LOG_ERR("setSkillSwitch illeagal skill id", skillID, status)
            return
        if status not in gameconst.SkillSwitchStatus.VALID_STATUS:
            LOG_ERR("setSkillSwitch illeagal switch status", skillID, status)
            return
        self.skillSwitches[skillID] = status

    def _lateReload(self):
        super(ServerSkills, self)._lateReload()
        for v in self.values():
            v.reloadScript()

        return

class SkillDamageVal(userType.UserSingleType):
    def __init__(self, targetId, hurt, hitType):
        self.targetId = targetId
        self.hurt = int(hurt)
        self.hitType = hitType


class SkillDamges(userType.UserSingleType):
    def __init__(self, casterId=0, sourceType=0, sourceId=0, damageInfo=None):
        self.casterId = casterId
        self.sourceId = sourceId
        self.sourceType = sourceType
        self.damageInfo = damageInfo or []

    def _lateReload(self):
        super(SkillDamges, self)._lateReload()

        for v in self.damageInfo:
            v.reloadScript()

        return


class DamageResult(userType.UserSingleType):
    def __init__(self, dmg=0, hpSuck=0, atkType=0, calcShield=True, hurtDmg=0):
        self.dmg = dmg  # 输出伤害
        self.atkType = atkType
        self.hpSuck = hpSuck
        self.calcShield = calcShield
        self.hurtDmg = hurtDmg  # 受伤害值，用于承伤统计，实际结算数值用dmg


class HealResult(userType.UserSingleType):
    def __init__(self, healVal=0, isCrit=False, doSkillHealCorrection=False):
        self.healVal = healVal
        self.isCrit = isCrit
        self.doSkillHealCorrection = doSkillHealCorrection


class AntiControlResult(userType.UserSingleType):
    RES_NOT_HIT = 0
    RES_HIT = 1
    RES_IMMUNE = 2
    RES_ANTI = 3

    def __init__(self, resultCode=RES_NOT_HIT, isDecay=False, controlState=-1, controlBuffId=0, controlDuration=0,
                 dispelBuffTag=0, antiDuration=20):
        self.resultCode = resultCode
        self.controlState = controlState
        self.controlBuffId = controlBuffId
        self.controlDuration = controlDuration
        self.isDecay = isDecay
        self.dispelBuffTag = dispelBuffTag
        self.antiDuration = antiDuration


class ControlState(userType.UserSingleType):
    def __init__(self, controlLv, tStart):
        self.controlLv = controlLv
        self.tStart = tStart
        self.removeTimerId = 0

    def refreshAntiTimer(self, owner, antiControlState, antiDuration):
        if self.removeTimerId:
            owner.cancelTimerCB(self.removeTimerId, gametimer.TIMER_TAG_REMOVE_COMBAT_CONTROL_STATE)

        self.removeTimerId = owner.addTimerCB(antiDuration, 'removeCombatControlState', (antiControlState,),
                                             gametimer.TIMER_TAG_REMOVE_COMBAT_CONTROL_STATE)

    def addControlLv(self, val):
        self.controlLv = int(self.controlLv + val)

    def resetTimerId(self):
        self.removeTimerId = 0


class SkillBase(userType.UserSingleType):
    def __init__(self, skillId, skillLv, tNextCast=0.0, cdDelta=0.0, parentSkill=0, targetIds=None):
        self.skillId = skillId
        self.skillLv = int(skillLv)
        self.tNextCast = tNextCast
        self.cdDelta = cdDelta
        self.parentSkill = parentSkill
        self.targetIds = targetIds or []
        self.isInSkill = False
        self.tempData = {}


    def _lateReload(self):
        super(SkillBase, self)._lateReload()
        if self.parentSkill:
            self.parentSkill.reloadScript()

    @classmethod
    def clearAllCache(cls):
        cls.getSkillData.cache_clear()
        cls.getTag.cache_clear()
        cls.getAction.cache_clear()
        cls.getActivateAction.cache_clear()
        cls.getDeactivateAction.cache_clear()
        cls.getChargetimeMax.cache_clear()
        cls.getCastingtimeMax.cache_clear()
        cls.getMaxTargetData.cache_clear()
        cls.getChannelTime.cache_clear()
        cls.getInterruptByAttack.cache_clear()
        cls.getScope.cache_clear()
        cls.getScopeData.cache_clear()
        cls.getCostMpData.cache_clear()
        cls.getMpPerSec.cache_clear()
        cls.getRangeData.cache_clear()
        cls.getFxDelay.cache_clear()
        cls.getBulletFx.cache_clear()
        cls.getBulletFxTime.cache_clear()
        cls.getSkillTime.cache_clear()
        cls.isAttackSkill.cache_clear()
        cls.getSkillHateRatio.cache_clear()
        cls.getBulletTimeScale.cache_clear()
        cls.getCategory.cache_clear()
        cls.getSkillSchoolTag.cache_clear()
        cls.getSkillName.cache_clear()
        cls.getEffectTarget.cache_clear()
        cls.getTarget.cache_clear()
        cls.getStartAction.cache_clear()
        cls.getEndAction.cache_clear()
        cls.isMovingSkill.cache_clear()
        cls.getPriority.cache_clear()
        cls.getSkillEvent.cache_clear()
        cls.getSkillLvParam.cache_clear()

    def getSkillId(self):
        return self.skillId

    def getLevel(self, owner):
        # NOTE(): 玩法如果涉及到增加技能等級時需要自行存儲管理增加的技能等級, 並按照如下步驟接入
        #  1. 在 AvatarCell.getExtraSkillLv 中增加涉及到自己的等級
        #  2. 在完成等級设置后通过如下接口下发给客户端 Avatar.client.updateSkillsExtraLevel
        #     2.1. API: updateSkillsExtraLevel 来源src 技能IDList(如果全局请填写: [gameconst.ClassSkillID, ]) 技能levelList(如果全局请填写: [exLvl, ])
        #  3. 在AvatarCell.initClientOnCell 中调用 Avatar.client.onGetSkillsExtraLevel 将等级数据下发给客户端
        #     3.1. 注意: 该调用必须在 Avatar.client.sendSkillBuilds 前调用
        return min(self.skillLv + self.getExtraLv(owner), int(SRSC.datas['sp_skillMaxLevel']['valueCN']))

    def getExtraLv(self, owner):
        if owner.IsAvatar:
            # 被动技能替换的技能需要从原技能中获取额外的技能等级
            relatedSkills = SSD.datas.get(self.skillId, {}).get('conflictSkill') or ()
            maxExtraSkillLv = owner.getExtraSkillLv(self.skillId)
            for sid in relatedSkills:
                if maxExtraSkillLv < owner.getExtraSkillLv(sid):
                    maxExtraSkillLv = owner.getExtraSkillLv(sid)
            return maxExtraSkillLv

        return 0

    def setLevel(self, owner, skillLv):
        self.skillLv = int(skillLv)

    @staticmethod
    @functools.lru_cache(1024)
    def getSkillData(skillId):
        return SSD.datas[skillId]

    @staticmethod
    @functools.lru_cache(1024)
    def getSkillEvent(skillId):
        return SkillBase.getSkillData(skillId).get('skillEvent', 0)

    @staticmethod
    @functools.lru_cache(1024)
    def getPriority(skillId):
        return SkillBase.getSkillData(skillId).get('priority', 0)

    @staticmethod
    @functools.lru_cache(1024)
    def getTag(skillId):
        tags = SkillBase.getSkillData(skillId).get('tag')
        if not tags:
            return ()
        elif type(tags[0]) is tuple:
            return tags[0]
        else:
            return tags

    def getGlobalCD(self, owner):
        gcd = self.getSkillData(self.skillId).get('globalCD', 0)
        return gcd * (1 + owner.mulGCD)

    def getCD(self, owner):
        _cd = self.getSkillData(self.skillId).get('CD', 0)

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
        LOG_DBG("in getCD ", owner, self.skillId, owner.IsAvatar, host)
        if host:
            addValue = 0
            ret, datas = host.getInscriptionEffects(self.skillId, gameconst.InscriptionEffectType.MODIFY_CD)
            if ret:
                if len(datas) == 1:
                    addValue = datas[0]
                    LOG_DBG("in getCD, inscription effect is triggered, skill_id:{0}, effect_type{1}, effect_value{2}", self.skillId, gameconst.InscriptionEffectType.MODIFY_CD, datas)
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
                            LOG_DBG("in getCD, inscription effect is triggered, skill_id:{0}, effect_type{1}, effect_value{2}", self.skillId, gameconst.InscriptionEffectType.REFRESH_CD, datas)
        return totalCD

    # 修改cd时长
    def changeCD(self, owner, delta):
        owner.combatDebugMsg("SkillBase changeCD: skillId:%s, delta:%s, inCDTime:%s", self.getSkillId(), delta, self.inCDTime())
        self.cdDelta += delta

        owner.IsAvatar and owner.client.onSetAddSkillCd(self.skillId, float(self.getCD(owner)), float(self.tNextCast),
                                                        False, self.getTempData(gameconst.SkillTempDataKey.RELEASE_TIME, 0), self.getTempData(gameconst.SkillTempDataKey.TOTAL_RELEASE_CNT, 0), self.getTempData(gameconst.SkillTempDataKey.RELEASED_CNT, 0), not self.isSkillCDStatusFrozen())
    # 修改本次cd的结束时间点
    def changeNextCast(self, owner, delta):
        self.tNextCast += delta
        realCD = self.tNextCast - time.time() if self.tNextCast > time.time() else self.getCD(owner)
        owner.IsAvatar and owner.client.onSetAddSkillCd(self.skillId, float(realCD), float(self.tNextCast),
                                                        False, self.getTempData(gameconst.SkillTempDataKey.RELEASE_TIME, 0), self.getTempData(gameconst.SkillTempDataKey.TOTAL_RELEASE_CNT, 0), self.getTempData(gameconst.SkillTempDataKey.RELEASED_CNT, 0), not self.isSkillCDStatusFrozen())

    def inCDTime(self):
        if time.time() < self.tNextCast:
            return True
        else:
            return False

    def canRemoveFromBuild(self):
        return not self.inCDTime()

    def getLastCDTime(self):
        if time.time() < self.tNextCast:
            return self.tNextCast - time.time()
        else:
            return 0

    @staticmethod
    @functools.lru_cache(1024)
    def getAction(skillId):
        return SkillBase.getSkillData(skillId).get('action', '')

    @staticmethod
    @functools.lru_cache(1024)
    def getActivateAction(skillId):
        return SkillBase.getSkillData(skillId).get('activateAction')

    @staticmethod
    @functools.lru_cache(1024)
    def getDeactivateAction(skillId):
        return SkillBase.getSkillData(skillId).get('deactivateAction')

    def getChargetimeMin(self):
        if self.getChargetimeMax(self.skillId) > 1:
            return 1
        else:
            return 0

    @staticmethod
    @functools.lru_cache(1024)
    def getChargetimeMax(skillId):
        return float(SkillBase.getSkillData(skillId).get('accumulating') or 0)

    @staticmethod
    @functools.lru_cache(1024)
    def getCastingtimeMax(skillId):
        return float(SkillBase.getSkillData(skillId).get('castingTime') or 0)

    @staticmethod
    @functools.lru_cache(1024)
    def getMaxTargetData(skillId):
        return SkillBase.getSkillData(skillId).get('maxTargetNum', 0)

    def getMaxTargetNum(self, owner, skillId, context):
        defaultMaxTagretNum = self.getMaxTargetData(skillId)
        host = owner.getAvatar()
        LOG_DBG("in getMaxTargetNum 1", owner, skillId, owner.IsAvatar, host, context)
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
        return SkillBase.getSkillData(skillId).get('channelTime', 0)

    @staticmethod
    @functools.lru_cache(1024)
    def getInterruptByAttack(skillId):
        return SkillBase.getSkillData(skillId).get('interrupt', 0)

    @staticmethod
    @functools.lru_cache(1024)
    def getScope(skillId):
        return SkillBase.getSkillData(skillId).get('scope') or 0

    @staticmethod
    @functools.lru_cache(1024)
    def getScopeData(skillId):
        return SkillBase.getSkillData(skillId).get('scopeParam', '')

    def getScopeParam(self, owner, skillId, context):
        scopeParam = self.getScopeData(skillId)
        if not scopeParam:
            return None, None
        else:
            scopeParam = eval(scopeParam) if isinstance(scopeParam, (str, bytes)) else scopeParam
            if type(scopeParam) not in (list, tuple):
                scopeParam = (scopeParam,)
            host = owner.getAvatar()
            LOG_DBG("in getScopeParam 1 ", owner, skillId, owner.IsAvatar, host)
            if host:
                ret, datas = host.getInscriptionEffects(skillId, gameconst.InscriptionEffectType.SKILL_RELEASE_RANGE_ADD_VALUE)
                if ret:
                    if len(datas) == 1:
                        LOG_DBG("in getScopeParam 2", owner, skillId, owner.IsAvatar, host, scopeParam, datas)
                        return scopeParam, datas[0]
                else:
                    if context:
                        ctx = context.getTopCtxFromActionQueue(actionContext.ACTION_USE_SKILL)
                        if ctx:
                            ret, datas = host.getInscriptionEffects(ctx.skillId, gameconst.InscriptionEffectType.SKILL_RELEASE_RANGE_ADD_VALUE)
                            if ret:
                                if len(datas) == 1:
                                    LOG_DBG("in getScopeParam 3", owner, skillId, owner.IsAvatar, host, scopeParam, datas)
                                    return scopeParam, datas[0]
            return scopeParam, None

    @staticmethod
    @functools.lru_cache(1024)
    def getCostMpData(skillId):
        return SkillBase.getSkillData(skillId).get('consumeMp') or 0

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
        return SkillBase.getSkillData(skillId).get('mpPerSec')

    @staticmethod
    @functools.lru_cache(1024)
    def getRangeData(skillId):
        # 兼容下老配置
        rangeData = SkillBase.getSkillData(skillId).get('range')
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
        damageRangeData = SkillBase.getSkillData(skillId).get('DamageRange')
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
        fxDelay = SkillBase.getSkillData(skillId).get('fxDelay') or 0
        if type(fxDelay) is tuple and fxDelay:
            d = fxDelay[0]
        else:
            d = fxDelay

        return float(d)

    @staticmethod
    @functools.lru_cache(1024)
    def getBulletFx(skillId):
        return int(SkillBase.getSkillData(skillId).get('bulletFx') or 0)

    @staticmethod
    @functools.lru_cache(1024)
    def getBulletFxTime(skillId):
        return float(SkillBase.getSkillData(skillId).get('bulletFxTime') or 0)

    @staticmethod
    @functools.lru_cache(1024)
    def getSkillTime(skillId):
        skillTime = SkillBase.getSkillData(skillId).get('skillTime') or 0
        if type(skillTime) is tuple and skillTime:
            st = 0
            for timeStage in skillTime:
                st += timeStage
        else:
            st = skillTime
        return float(st)

    @staticmethod
    @functools.lru_cache(1024)
    def isAttackSkill(skillId):
        return True if SkillBase.getSkillData(skillId).get('isAttackSkill') == 1 else False

    @staticmethod
    @functools.lru_cache(1024)
    def getSkillHateRatio(skillId):
        return SkillBase.getSkillData(skillId).get('skillHateRatio')

    @staticmethod
    @functools.lru_cache(1024)
    def getBulletTimeScale(skillId):
        return FF.datas.get(SkillBase.getBulletFx(skillId), {}).get('bulletTimeScale', 1.0)

    @staticmethod
    @functools.lru_cache(1024)
    def getCategory(skillId):
        return SkillBase.getSkillData(skillId).get('category', 0)

    @staticmethod
    @functools.lru_cache(1024)
    def getSkillSchoolTag(skillId):
        return SkillBase.getSkillData(skillId).get('classTag', 0)

    @staticmethod
    @functools.lru_cache(1024)
    def getSkillName(skillId):
        return SkillBase.getSkillData(skillId).get('name', '')

    @staticmethod
    @functools.lru_cache(1024)
    def getSkillLvParam(skillId):
        return SkillBase.getSkillData(skillId).get('lvParam')

    def getClassTag(self, owner):
        classTag = self.getSkillSchoolTag(self.skillId)
        if classTag == -1 and owner.IsAICombatUnit:
            battleType = owner.getBattleType()
            if battleType == gameconst.BattleType.physics:
                classTag = gameconst.SCHOOL_PHYSICAL
            elif battleType == gameconst.BattleType.magic:
                classTag = gameconst.SCHOOL_MAGIC
        return classTag

    def getServerEffectRange(self, owner):
        # 为了解决客户端打到，服务端判断出了范围加个延迟的范围值，只给客户端算的锁定技能加
        if self.needReleaseTarget():
            return self.getEffectRange(owner, self.skillId, self.skillLv) + 1
        return self.getEffectRange(owner, self.skillId, self.skillLv)

    def getServerEffectRangeWithTarget(self, owner, target):
        targetRadius = 0
        if target.IsMonster:
            targetRadius = target.getConfigData().get('attackDistanceCompensation')
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

    def getServerRangeWithTarget(self, owner, target):
        targetRadius = 0
        if target.IsMonster:
            targetRadius = target.getConfigData().get('attackDistanceCompensation')
        if self.needReleaseTarget():
            return self.getRange(owner, self.skillId, self.skillLv) + targetRadius + 1
        return self.getRange(owner, self.skillId, self.skillLv) + targetRadius

    def inRange(self, src, target):
        pos1 = src.position
        pos2 = target.position
        if not src.checkCombatRangeY(target):
            return False
        if self.getRange(src, self.skillId, self.skillLv) <= 0:
            return True
        # 为了解决客户端打到，服务端判断出了范围加个延迟的范围值
        if sMath.distance2DToCompareFrom3DPosition(pos1, pos2) < math.pow(self.getServerRangeWithTarget(src, target), 2):
            return True

        return False

    def getServerScoperRange(self, target, range):
        # 为了解决客户端打到，服务端判断出了范围加个延迟的范围值，只给客户端算的锁定技能加
        if self.needReleaseTarget():
            return range + 1
        return range

    def needReleaseTarget(self):
        targetType = self.getTarget(self.skillId)
        if not targetType or targetType == 'None':
            return False
        return True

    def isMultiCastSkill(self, owner, context):
        return self.hasSkillTag(gameconst.SkillTag.Casting) and self.getMaxTargetNum(owner, self.skillId, context) > 1

    def needCharge(self):
        return self.getChargetimeMin() > 0 and self.getChargetimeMax(self.skillId) > 0

    def needCast(self):
        return self.getCastingtimeMax(self.skillId) > 0

    @staticmethod
    @functools.lru_cache(1024)
    def getEffectTarget(skillId):
        LOG_DBG("getEffectTarget", skillId)
        return SkillBase.getSkillData(skillId).get('effectTarget', '')

    @staticmethod
    @functools.lru_cache(1024)
    def getTarget(skillId):
        return SkillBase.getSkillData(skillId).get('target', '')

    @staticmethod
    @functools.lru_cache(1024)
    def getStartAction(skillId):
        return SkillBase.getSkillData(skillId).get('startSkillAction', None)

    @staticmethod
    @functools.lru_cache(1024)
    def getEndAction(skillId):
        return SkillBase.getSkillData(skillId).get('endSkillAction', None)

    @staticmethod
    @functools.lru_cache(1024)
    def getShiftDelay(skillId):
        return SkillBase.getSkillData(skillId).get('shiftDelay', 0)

    @staticmethod
    @functools.lru_cache(1024)
    def getProtectRange(skillId):
        return SkillBase.getSkillData(skillId).get('protectRange', 0)

    def hasTag(self, tag):
        """
        由于策划那边还保留有旧的接口，这个就作为兼容用吧
        """
        tags = self.getTag(self.skillId)
        if not tags:
            return False

        if tag in tags:
            return True
        return False

    def hasSkillTag(self, tag):
        tags = self.getTag(self.skillId)
        if not tags:
            return False

        if tag in tags:
            return True
        return False

    @staticmethod
    @functools.lru_cache(1024)
    def isMovingSkill(skillId):
        isMoveSkill = SkillBase.getSkillData(skillId).get('isMoveSkill', False)
        if type(isMoveSkill) is tuple and isMoveSkill:
            isMoveSkillState = isMoveSkill[0]
        else:
            isMoveSkillState = isMoveSkill
        return int(isMoveSkillState)

    @staticmethod
    @functools.lru_cache(1024)
    def isChangePositionSkill(skillId):
        tags = SkillBase.getTag(skillId)
        return gameconst.SkillTag.ShiftSkill in tags or gameconst.SkillTag.DodgeSkill in tags or gameconst.SkillTag.Lunge in tags or gameconst.SkillTag.Chongfeng in tags or gameconst.SkillTag.TeleportSkill in tags or gameconst.SkillTag.BlinkToTarget in tags

    def clearCD(self, owner):
        oldInCD = self.inCDTime()
        self.tNextCast = 0.0

        if oldInCD and owner.IsAvatar:
            owner.client.onSetAddSkillCd(self.skillId, float(self.getCD(owner)), float(self.tNextCast), False, self.getTempData(gameconst.SkillTempDataKey.RELEASE_TIME, 0), self.getTempData(gameconst.SkillTempDataKey.TOTAL_RELEASE_CNT, 0), self.getTempData(gameconst.SkillTempDataKey.RELEASED_CNT, 0), not self.isSkillCDStatusFrozen())

    def getOneNearest(self, pos, targetsList):
        if not targetsList or len(targetsList) == 0:
            return
        distance = 10000
        minIndex = -1
        for idx, target in enumerate(targetsList):
            curDis = sMath.distance2DToCompareFrom3DPosition(pos, target.position)
            if curDis < distance:
                minIndex = idx
                distance = curDis
        return targetsList[minIndex]

    def getOneHPLowest(self, caster):
        ###取队伍或小队百分比最低
        if not caster.isInTeam() and not caster.isInRaid():
            return caster

        targetsList = []
        if caster.isInTeam():
            for member in caster.teamInfo.teamPlayerDic.values():
                if not member.playerBox:
                    continue

                player = KBEngine.entities.get(member.playerBox.id, None)

                if not player:
                    continue
                if utils.checkTargetTypeValid(self.getEffectTarget(self.skillId), caster, player) and self.inEffectRange(
                        caster, player):
                    targetsList.append(player)

        elif caster.isInRaid():
            raidTeamCacheVal = caster.raidInfo.raidTeamDic.get(caster.raidInfo.raidTeamIDX, None)
            if raidTeamCacheVal:
                for member in raidTeamCacheVal.teamPlayerDic.values():
                    if not member.playerBox:
                        continue

                    player = KBEngine.entities.get(member.playerBox.id, None)

                    if not player:
                        continue
                    if utils.checkTargetTypeValid(self.getEffectTarget(self.skillId), caster, player) and self.inEffectRange(
                            caster, player):
                        targetsList.append(player)

        if not targetsList:
            return caster

        hpPercent = targetsList[0].hp / targetsList[0].fullHp if targetsList[0].fullHp else 1
        minIndex = 0
        for idx, target in enumerate(targetsList):
            targetHpPercent = target.hp / target.fullHp if target.fullHp else 1
            if targetHpPercent < hpPercent:
                minIndex = idx
                hpPercent = targetHpPercent

        return targetsList[minIndex]

    def isInAttackAnnularArea(self, target, center, minRadius, maxRadius):
        targetRadius = 0
        if target.IsMonster:
            targetRadius = target.getConfigData().get('attackDistanceCompensation', 0)

        distance2 = sMath.distance2DToCompareFrom3DPosition(target.position, center)
        distance = math.sqrt(max(0, distance2))

        return (distance + targetRadius >= minRadius) and (distance - targetRadius <= maxRadius)

    def isInAttackLine(self, target, vCenter, direction, length, width):
        targetRadius = 0
        if target.IsMonster:
            targetRadius = target.getConfigData().get('attackDistanceCompensation', 0)

        if targetRadius:
            return utils.isInAttackLineWithRadius(target.position, vCenter, direction, length, width, targetRadius)
        else:
            return utils.isInAttackLine(target.position, vCenter, direction, length, width, True)

    def isInAttackRectAngle(self, target, vCenter, direction, length, width, radius):
        return utils.isInAttackArea(target, vCenter, radius) and self.isInAttackLine(target, vCenter, direction, length,
                                                                                    width)

    def getAngle(self, vector_a, vector_b):
        ab = vector_a.x * vector_b.x + vector_a.y * vector_b.y
        a1 = math.sqrt(vector_a.x * vector_a.x + vector_a.y * vector_a.y)
        b1 = math.sqrt(vector_b.x * vector_b.x + vector_b.y * vector_b.y)
        if a1 * b1 == 0:
            return 0
        else:
            cosr = ab / (a1 * b1)

        cosr = max(-1.0, min(1.0, cosr))
        angle = math.acos(cosr)
        angle2 = angle * 360 / 2 / math.pi

        return angle2

    def isInAttackSector(self, target, center, dir, radius, angle):
        targetRadius = 0
        if target.IsMonster:
            targetRadius = target.getConfigData().get('attackDistanceCompensation', 0)

        if not targetRadius:
            center2 = Math.Vector2(center.x, center.z)
            dir2 = Math.Vector2(dir.x, dir.z)

            if sMath.distance2DToCompareFrom3DPosition(target.position, center) <= radius * radius:
                curPos = Math.Vector2(target.position.x, target.position.z)
                temp = curPos - center2
                return self.getAngle(dir2, temp) <= angle / 2
            return False
        else:
            center2 = Math.Vector2(center.x, center.z)
            dir2 = Math.Vector2(dir.x, dir.z)

            distance2 = sMath.distance2DToCompareFrom3DPosition(target.position, center)
            distance = math.sqrt(max(0, distance2))

            if distance > radius + targetRadius:
                return False

            if distance <= targetRadius:
                return True

            curPos = Math.Vector2(target.position.x, target.position.z)
            vectorToTarget = curPos - center2

            targetAngle = self.getAngle(dir2, vectorToTarget)
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

            distToLeftEdge = sMath.distancePointToLine(curPos, center2, center2 + leftEdgeDir)
            distToRightEdge = sMath.distancePointToLine(curPos, center2, center2 + rightEdgeDir)

            if distToLeftEdge <= targetRadius or distToRightEdge <= targetRadius:
                projOnLeft = sMath.projectPointOnLine(curPos, center2, center2 + leftEdgeDir)
                projOnRight = sMath.projectPointOnLine(curPos, center2, center2 + rightEdgeDir)

                leftVec = projOnLeft - center2
                rightVec = projOnRight - center2

                if (leftVec.dot(leftEdgeDir) >= 0 and distToLeftEdge <= targetRadius) or \
                   (rightVec.dot(rightEdgeDir) >= 0 and distToRightEdge <= targetRadius):
                    return True

            return False

    def isInMultiSectorAttack(self, target, center, baseDir, radius, angle, sectorNum, offsetAngles):
        for i in range(sectorNum):
            offsetAngle = offsetAngles[i] if i < len(offsetAngles) else 0
            offsetRad = offsetAngle * math.pi / 180

            rotatedDir = sMath.clockwiseRotate(baseDir, offsetRad)
            rotatedDir3D = Math.Vector3(rotatedDir[0], 0, rotatedDir[2])

            if self.isInAttackSector(target, center, rotatedDir3D, radius, angle):
                return True

        return False

    def isInAttackMi(self, target, center, skillDir, length, width):
        for i in range(8):
            theta = math.pi * i / 4
            toDir = sMath.clockwiseRotate(skillDir, theta)
            toDir = Math.Vector3(toDir)
            if self.isInAttackLine(target, center, toDir, length, width):
                return True
        return False

    def isInAttackHalfMi(self, target, center, skillDir, length, width):
        for i in (-1, 0, 1):
            theta = math.pi * i / 4
            toDir = sMath.clockwiseRotate(skillDir, theta)
            toDir = Math.Vector3(toDir)
            if self.isInAttackLine(target, center, toDir, length, width):
                return True
        return False

    def getLinkedTargets(self, owner, target, dist, linkProp, count):
        if not target:
            return []

        targetsList = owner.getTargets(target, target.id, self.getEffectTarget(self.skillId), dist)

        linkedTargets = [target.id]
        if len(linkedTargets) >= count:
            return linkedTargets

        random.shuffle(targetsList)

        for e in targetsList:
            if e.id in linkedTargets:
                continue

            # 有概率闪电链不会传递
            if random.random() > linkProp:
                break

            linkedTargets.append(e.id)
            if len(linkedTargets) >= count:
                return linkedTargets

        return linkedTargets

    def checkSkillArgs(self, args):
        scopeType = self.getScope(self.skillId)
        if not scopeType or scopeType == gameconst.SkillScope.TARGET_AUTO:
            return True

        if scopeType in (gameconst.SkillScope.CIRCLE_CENTER_SELF, gameconst.SkillScope.CIRCLE_CENTER_TARGET,
                         gameconst.SkillScope.TARGET_LINKED, gameconst.SkillScope.ANNULAR_CENTER_SELF):
            return True

        if not args:
            return False

        if scopeType in (gameconst.SkillScope.SELF_TO_TARGET_RECTANGLE, gameconst.SkillScope.USER_DEFINED_SECTOR,
                         gameconst.SkillScope.USER_DEFINED_RECTANGLE, \
                         gameconst.SkillScope.MI_CENTER_SELF, gameconst.SkillScope.HALF_MI,
                         gameconst.SkillScope.CURRENT_DIRECTION_RECTANGLE):
            if self.isChangePositionSkill(self.skillId):
                return len(args) >= 6
            return len(args) >= 3

        if scopeType in (gameconst.SkillScope.USER_DEFINED_CIRCLE,):
            if self.isChangePositionSkill(self.skillId):
                return len(args) >= 7
            return len(args) >= 4

        if scopeType in (gameconst.SkillScope.COLOSSUS_CIRCLE, gameconst.SkillScope.COLOSSUS_RECTANGLE):
            if self.isChangePositionSkill(self.skillId):
                return len(args) >= 9
            return len(args) == 6

        if scopeType == gameconst.SkillScope.MULTI_SECTOR:
            return len(args) >= 3

        return False

    def getSkillPosAndDir(self, caster, target, arr):
        position = None
        direction = None
        scopeType = self.getScope(self.skillId)

        if scopeType in (gameconst.SkillScope.CIRCLE_CENTER_SELF, gameconst.SkillScope.ANNULAR_CENTER_SELF):
            pass

        elif scopeType == gameconst.SkillScope.CIRCLE_CENTER_TARGET:
            position = target.position if target else caster.position

        elif scopeType == gameconst.SkillScope.SELF_TO_TARGET_RECTANGLE:
            direction = sMath.vector3WithoutY(target.position - caster.position) if target else Math.Vector3(arr[0],
                                                                                                             arr[1],
                                                                                                             arr[2])
            direction.normalise()

        elif scopeType == gameconst.SkillScope.USER_DEFINED_SECTOR:
            direction = Math.Vector3(arr[0], arr[1], arr[2])
            direction.normalise()

        elif scopeType == gameconst.SkillScope.USER_DEFINED_RECTANGLE:
            direction = Math.Vector3(arr[0], arr[1], arr[2])
            direction.normalise()
            position = caster.position

        elif scopeType == gameconst.SkillScope.USER_DEFINED_CIRCLE:
            percent = arr[3]
            direction = Math.Vector3(arr[0], arr[1], arr[2])
            direction.normalise()
            position = caster.position + direction * percent * (self.getRange(caster, self.skillId, self.skillLv)+0.1) # 加0.1是为了容错，避免因为客户端和服务端距离计算误差导致明明在范围内却打不到的情况
        elif scopeType == gameconst.SkillScope.MI_CENTER_SELF:
            direction = Math.Vector3(arr[0], arr[1], arr[2])
            direction.normalise()
        elif scopeType == gameconst.SkillScope.HALF_MI:
            direction = Math.Vector3(arr[0], arr[1], arr[2])
            direction.normalise()
        elif scopeType == gameconst.SkillScope.TARGET_LINKED:
            position = target.position if target else caster.position

        elif scopeType == gameconst.SkillScope.COLOSSUS_CIRCLE:
            position = tuple(arr[:3])
            direction = Math.Vector3(arr[3], arr[4], arr[5])
            direction.normalise()
        elif scopeType == gameconst.SkillScope.COLOSSUS_RECTANGLE:
            if arr:
                position = tuple(arr[:3])
                direction = Math.Vector3(arr[3], arr[4], arr[5])
                direction.normalise()
        elif scopeType == gameconst.SkillScope.CURRENT_DIRECTION_RECTANGLE:
            direction = sMath.getDirFromYaw(caster.direction[2])
            direction.normalise()
            position = caster.position

        elif scopeType == gameconst.SkillScope.MULTI_SECTOR:
            direction = Math.Vector3(arr[0], arr[1], arr[2])
            direction.normalise()

        if not direction and self.needReleaseTarget() and target:
            direction = Math.Vector3(target.position - caster.position)
            direction.normalise()

        return position, direction

    def getSkillArr(self, caster, target, direction=None):
        arr = []
        if not direction:
            direction = sMath.vector3WithoutY(target.position - caster.position)
            direction.normalise()
        scopeType = self.getScope(self.skillId)

        if not scopeType:
            arr = list(direction)
        elif scopeType == gameconst.SkillScope.SELF_TO_TARGET_RECTANGLE:
            arr = list(direction)

        elif scopeType == gameconst.SkillScope.USER_DEFINED_SECTOR:
            arr = list(direction)

        elif scopeType in (
                gameconst.SkillScope.USER_DEFINED_RECTANGLE, gameconst.SkillScope.CURRENT_DIRECTION_RECTANGLE):
            arr = list(direction)

        elif scopeType == gameconst.SkillScope.USER_DEFINED_CIRCLE:
            arr = utils.transformPosesToSkillArgs(
                caster.position,
                target.position,
                self.getRange(caster, self.skillId, self.skillLv),
                direction
            )

        elif scopeType == gameconst.SkillScope.MI_CENTER_SELF:
            arr = list(direction)

        elif scopeType == gameconst.SkillScope.HALF_MI:
            arr = list(direction)

        elif scopeType == gameconst.SkillScope.MULTI_SECTOR:
            arr = list(direction)

        return arr

    def getSkillDesPosition(self, caster, target, skillArgs):
        if self.hasSkillTag(gameconst.SkillTag.TeleportSkill):
            distance = self.getRange(caster, self.skillId, self.skillLv)
            dstPosition = sMath.getForwardPos(caster.position, caster.direction[2], distance)
            skillPos, skillDir = self.getSkillPosAndDir(caster, target, skillArgs)
            # scope其他时取技能朝向，scope为6时取双摇杆选的坐标
            if self.getScope(self.skillId) == gameconst.SkillScope.USER_DEFINED_CIRCLE:
                dstPosition = skillPos
            else:
                dstPosition = caster.position + skillDir * distance

            dstPosition = utils.getSurfacePos(caster.spaceID, dstPosition)
            realDstPos = utils.getRaycastPosition(caster.spaceID, caster.position, dstPosition)
            desPosition = list(realDstPos)

        elif self.hasSkillTag(gameconst.SkillTag.BlinkToTarget):
            offset = 2.0
            yaw = sMath.getYawFromPoints(caster.position, target.position)
            targetPos = sMath.getForwardPos(target.position, yaw, offset)

            targetPos = utils.getSurfacePos(caster.spaceID, targetPos)
            realDstPos = utils.getRaycastPosition(caster.spaceID, caster.position, targetPos)
            desPosition = list(realDstPos)
        elif self.hasSkillTag(gameconst.SkillTag.Chongfeng):
            distance = 2.0
            if target and hasattr(target, 'creepBaseId'):
                distance = utils.getCollisionDistance(target.creepBaseId, distance)

            if sMath.inRange2D(distance, caster.position, target.position):
                dstPosition = caster.position
            else:
                offset = distance
                yaw = sMath.getYawFromPoints(caster.position, target.position)
                dstPosition = sMath.getForwardPos(target.position, yaw, offset)

            dstPosition = utils.getSurfacePos(caster.spaceID, dstPosition)
            dstPosition = utils.getRaycastPosition(caster.spaceID, caster.position, dstPosition)
            desPosition = list(dstPosition)
        elif self.hasSkillTag(gameconst.SkillTag.Lunge):
            skillPos, skillDir = self.getSkillPosAndDir(caster, target, skillArgs)
            skillRange = self.getRange(caster, self.skillId, self.skillLv)
            # 根据target的碰撞距离处理
            if target:
                collisionDis = 2.0
                if hasattr(target, 'creepBaseId'):
                    collisionDis = utils.getCollisionDistance(target.creepBaseId, collisionDis)
                distance = sMath.distance2D(caster.position, target.position)
                # 距离超过碰撞距离，需要减去碰撞距离。否则原地不动
                distance = distance - collisionDis if distance > collisionDis else 0
                if skillRange > distance:
                    skillRange = distance

            dstPosition = caster.position + skillDir * skillRange
            dstPosition = utils.getSurfacePos(caster.spaceID, dstPosition)
            realDstPos = utils.getRaycastPosition(caster.spaceID, caster.position, dstPosition)
            desPosition = list(realDstPos)
        elif self.hasSkillTag(gameconst.SkillTag.DodgeSkill) or self.hasSkillTag(gameconst.SkillTag.ShiftSkill):
            skillPos, skillDir = self.getSkillPosAndDir(caster, target, skillArgs)
            dstPosition = caster.position + skillDir * self.getRange(caster, self.skillId, self.skillLv)
            dstPosition = utils.getSurfacePos(caster.spaceID, dstPosition)
            realDstPos = utils.getRaycastPosition(caster.spaceID, caster.position, dstPosition)
            LOG_DBG('dodgeGetPos', caster.spaceID, caster.position, dstPosition, realDstPos)
            desPosition = list(realDstPos)

        return desPosition

    def getEffectTargets(self, caster, targetId, arr, forceTarget=False, positionSkillArgs=None, context = None):
        if not caster:
            return []
        if self.getTempData(gameconst.SkillTempDataKey.IS_CHANNELING_EMPTY, False):
            return []

        if self.targetIds:
            invalidIds = []
            for i, tid in enumerate(self.targetIds):
                target = KBEngine.entities.get(tid)
                if not target:
                    invalidIds.append(i)
                    continue

                if not utils.checkTargetTypeValid(
                        self.getEffectTarget(self.skillId),
                        caster,
                        target):

                    invalidIds.append(i)

            for i in reversed(invalidIds):
                self.targetIds.pop(i)

            return self.targetIds

        return self._internalGetEffectTargets(caster, targetId, arr, forceTarget, positionSkillArgs, context)

    def _internalGetEffectTargets(self, caster, targetId, arr, forceTarget, positionSkillArgs, context):
        # 客户端自动寻路攻击目标调用过来的时候，可能最新的position还没报告给服务端，所以这里按技能距离可能
        # 拿不到客户端选中的entity，这里加点offset偏差做容错

        target = KBEngine.entities.get(targetId)

        skillPos, skillDir = self.getSkillPosAndDir(caster, target, arr)
        scopes = self.getScope(self.skillId)
        scopeParams, scopeAddRatio = self.getScopeParam(caster, self.skillId, context)

        LOG_DBG("in _internalGetEffectTargets ", scopes, self.skillId, scopeParams, scopeAddRatio)

        if not scopes or scopes == gameconst.SkillScope.TARGET_AUTO:
            if self.hasSkillTag(gameconst.SkillTag.SingleHeal) and hasattr(caster,
                                                                      'commonFlagCell') and caster.getCommonFlagCell(
                gameconst.CommonFlagCellType.IsHealHPLow) and (
                    not target or targetId == caster.id or not utils.checkTargetTypeValid(self.getEffectTarget(self.skillId),
                                                                                     caster, target)):
                targetNearest = self.getOneHPLowest(caster)
            else:
                if target and (caster.isVisible(target) or caster.hasBuffTag(
                        gameconst.BuffTag.TagSeeHiddenEnt)) and utils.checkTargetTypeValid(self.getEffectTarget(self.skillId),
                                                                                   caster, target):
                    if self.inEffectRange(caster, target):
                        return [target.id]
                    else:
                        return []

                if self.getEffectTarget(self.skillId) == 'Friend':
                    return [caster.id]

                if not targetId:
                    return []

                if self.getTempData(gameconst.SkillTempDataKey.BEGIN_SKILL_POSITION):
                    targetsList = caster.getTargets(caster, targetId, self.getEffectTarget(self.skillId),
                                                    self.getServerEffectRange(caster), forceTarget,
                                                    self.getTempData(gameconst.SkillTempDataKey.BEGIN_SKILL_POSITION))
                    targetNearest = self.getOneNearest(self.getTempData(gameconst.SkillTempDataKey.BEGIN_SKILL_POSITION), targetsList)
                else:
                    targetsList = caster.getTargets(caster, targetId, self.getEffectTarget(self.skillId),
                                                    self.getServerEffectRange(caster), forceTarget)
                    targetNearest = self.getOneNearest(caster.position, targetsList)
            if targetNearest and (caster.isVisible(targetNearest) or caster.hasBuffTag(
                    gameconst.BuffTag.TagSeeHiddenEnt)) and self.inEffectRange(caster, targetNearest):
                return [targetNearest.id]
            else:
                return []

        elif scopes == gameconst.SkillScope.CIRCLE_CENTER_SELF:
            center = caster.position
            radius = float(scopeParams[0])
            if scopeAddRatio:
                radius *= (1+scopeAddRatio)

            checkScopeFun = lambda target: utils.isInAttackArea(target, center, radius)
            return caster.getTargetsWithNum(caster, targetId, self.getEffectTarget(self.skillId), self.getServerEffectRange(caster),
                                            self.getMaxTargetNum(caster, self.skillId, context), checkScopeFun)

        elif scopes == gameconst.SkillScope.CIRCLE_CENTER_TARGET:
            if not target:
                return []

            radius = float(scopeParams[0])
            if scopeAddRatio:
                radius *= (1+scopeAddRatio)

            checkScopeFun = lambda target: utils.isInAttackArea(target, skillPos, radius)
            return caster.getTargetsWithNum(target, targetId, self.getEffectTarget(self.skillId),
                                            self.getEffectRange(caster, self.skillId, self.skillLv) + 0.8,
                                            self.getMaxTargetNum(caster, self.skillId, context), checkScopeFun)

        elif scopes == gameconst.SkillScope.SELF_TO_TARGET_RECTANGLE:
            length = float(scopeParams[0])
            width = float(scopeParams[1])
            if scopeAddRatio:
                length *= (1+scopeAddRatio)
                width *= (1+scopeAddRatio)

            length = self.getServerScoperRange(target, length)
            checkScopeFun = lambda target: self.isInAttackLine(target, caster.position, skillDir, length, width)
            return caster.getTargetsWithNum(caster, targetId, self.getEffectTarget(self.skillId), self.getServerEffectRange(caster),
                                            self.getMaxTargetNum(caster, self.skillId, context), checkScopeFun)

        elif scopes == gameconst.SkillScope.USER_DEFINED_SECTOR:
            skillSectorAngle = float(scopeParams[0])
            radius = self.getServerEffectRange(caster)
            if scopeAddRatio:
                radius *= (1+scopeAddRatio)
                
            checkScopeFun = lambda target: self.isInAttackSector(target, caster.position, skillDir,
                                                                 radius, skillSectorAngle * 2)
            return caster.getTargetsWithNum(caster, targetId, self.getEffectTarget(self.skillId), self.getServerEffectRange(caster),
                                            self.getMaxTargetNum(caster, self.skillId, context), checkScopeFun)

        elif scopes in (gameconst.SkillScope.USER_DEFINED_RECTANGLE, gameconst.SkillScope.CURRENT_DIRECTION_RECTANGLE):
            length = self.getServerEffectRange(caster) + self.getProtectRange(self.skillId)
            width = float(scopeParams[1])
            if scopeAddRatio:
                length *= (1+scopeAddRatio)
                width *= (1+scopeAddRatio)
            if positionSkillArgs:
                beginSkillPosition = self.getTempData(gameconst.SkillTempDataKey.BEGIN_SKILL_POSITION) if self.getTempData(
                    gameconst.SkillTempDataKey.BEGIN_SKILL_POSITION) else caster.position
                distance = sMath.distance2D(beginSkillPosition, positionSkillArgs)
                range = min(self.getEffectRange(caster, self.skillId, self.skillLv), distance + self.getProtectRange(self.skillId))
            else:
                range = self.getServerEffectRange(caster) + self.getProtectRange(self.skillId)
            if self.getTempData(gameconst.SkillTempDataKey.BEGIN_SKILL_POSITION):
                checkScopeFun = lambda target: self.isInAttackRectAngle(target, self.getTempData(gameconst.SkillTempDataKey.BEGIN_SKILL_POSITION),
                                                                        skillDir, length, width, range)
                return caster.getTargetsWithNum(caster, targetId, self.getEffectTarget(self.skillId), range,
                                                self.getMaxTargetNum(caster, self.skillId, context), checkScopeFun)
            else:
                checkScopeFun = lambda target: self.isInAttackRectAngle(target, caster.position, skillDir, length,
                                                                        width, range)
                return caster.getTargetsWithNum(caster, targetId, self.getEffectTarget(self.skillId), range,
                                                self.getMaxTargetNum(caster, self.skillId, context), checkScopeFun)

        elif scopes == gameconst.SkillScope.USER_DEFINED_CIRCLE:
            direction = Math.Vector3(arr[0], arr[1], arr[2])
            percent = arr[3]
            beginSkillPosition = self.getTempData(gameconst.SkillTempDataKey.BEGIN_SKILL_POSITION) if self.getTempData(gameconst.SkillTempDataKey.BEGIN_SKILL_POSITION) else caster.position
            center = beginSkillPosition + direction * percent * (self.getRange(caster, self.skillId, self.skillLv)+0.1) # 加0.1是为了容错，避免因为客户端和服务端距离计算误差导致明明在范围内却打不到的情况
            radius = float(scopeParams[0])
            if scopeAddRatio:
                radius *= (1+scopeAddRatio)
            checkScopeFun = lambda target: utils.isInAttackArea(target, center, radius)
            return caster.getTargetsWithNum(target, targetId, self.getEffectTarget(self.skillId),
                                            self.getServerEffectRange(caster) + radius,
                                            self.getMaxTargetNum(caster, self.skillId, context), checkScopeFun)

        elif scopes == gameconst.SkillScope.MI_CENTER_SELF:
            length = float(scopeParams[0])
            width = float(scopeParams[1])

            checkScopeFun = lambda target: self.isInAttackMi(target, caster.position, skillDir, length, width)
            return caster.getTargetsWithNum(target, targetId, self.getEffectTarget(self.skillId), self.getServerEffectRange(caster),
                                            self.getMaxTargetNum(caster, self.skillId, context), checkScopeFun)

        elif scopes == gameconst.SkillScope.HALF_MI:
            length = float(scopeParams[0])
            width = float(scopeParams[1])

            checkScopeFun = lambda target: self.isInAttackHalfMi(target, caster.position, skillDir, length, width)
            return caster.getTargetsWithNum(target, targetId, self.getEffectTarget(self.skillId), self.getServerEffectRange(caster),
                                            self.getMaxTargetNum(caster, self.skillId, context), checkScopeFun)

        elif scopes == gameconst.SkillScope.TARGET_LINKED:
            dist, linkProp, count = float(scopeParams[0]), float(scopeParams[1]), float(scopeParams[2])
            linkedTargets = self.getLinkedTargets(caster, target, dist, linkProp, count)
            return linkedTargets

        elif scopes == gameconst.SkillScope.COLOSSUS_CIRCLE:
            center = skillPos
            radius = float(scopeParams[0])

            checkScopeFun = lambda target: utils.isInAttackArea(target, center, radius)
            return caster.getTargetsWithNum(target, targetId, self.getEffectTarget(self.skillId),
                                            self.getServerEffectRange(caster) + radius,
                                            self.getMaxTargetNum(caster, self.skillId, context), checkScopeFun)

        elif scopes == gameconst.SkillScope.COLOSSUS_RECTANGLE:
            length = self.getServerEffectRange(caster)
            width = float(scopeParams[1])

            if skillPos:
                checkScopeFun = lambda target: self.isInAttackRectAngle(target, skillPos, skillDir, length, width,
                                                                        self.getServerEffectRange(caster))
                return caster.getTargetsWithNum(caster, targetId, self.getEffectTarget(self.skillId),
                                                self.getServerEffectRange(caster),
                                                self.getMaxTargetNum(caster, self.skillId, context), checkScopeFun)
            else:
                return []
        elif scopes == gameconst.SkillScope.ANNULAR_CENTER_SELF:
            minRadius = float(scopeParams[0])
            maxRadius = float(scopeParams[1])
            center = caster.position
            checkScopeFun = lambda target: self.isInAttackAnnularArea(target, center, minRadius, maxRadius)
            return caster.getTargetsWithNum(target, targetId, self.getEffectTarget(self.skillId), self.getServerEffectRange(caster),
                                            self.getMaxTargetNum(caster, self.skillId, context), checkScopeFun)
        elif scopes == gameconst.SkillScope.MULTI_SECTOR:
            sectorNum = int(scopeParams[0])
            offsetAngles = scopeParams[1]
            sectorAngle = float(scopeParams[2])

            if not isinstance(offsetAngles, (list, tuple)):
                offsetAngles = []

            if len(offsetAngles) < sectorNum:
                caster.combatDebugMsg("_internalGetEffectTargets MULTI_SECTOR not enough offsetAngles: skillId:%s", self.skillId)

            checkScopeFun = lambda target: self.isInMultiSectorAttack(target, caster.position, skillDir,
                                                self.getServerEffectRange(caster), sectorAngle * 2, sectorNum, offsetAngles)
            return caster.getTargetsWithNum(caster, targetId, self.getEffectTarget(self.skillId), self.getServerEffectRange(caster),
                                            self.getMaxTargetNum(caster, self.skillId, context), checkScopeFun)

        return []

    def _checkUseSkillOwner(self, owner, targetId, ignoreReasons=0, checkInRange=True):
        LOG_DBG('_checkUseSkillOwner', self.skillId, targetId, ignoreReasons, checkInRange)
        code = gameconst.UseSkillCheck.USC_ENUM_IN_CD
        if not code & ignoreReasons and self.inCDTime():
            owner.combatDebugMsg('_checkUseSkillOwner cannot use inCDTime: skillId:%s, tNextCast:%s, now:%s', self.getSkillId(), self.tNextCast, time.time())
            return code

        code = gameconst.UseSkillCheck.USC_ENUM_LACK_OF_MP
        if not code & ignoreReasons and owner.IsAvatar and owner.mp < self.getCostMp(owner, self.skillId, owner.mpCostRatio):
            owner.combatDebugMsg('_checkUseSkillOwner fail to use lack of mp: skillId:%s', self.skillId)
            return code

        code = gameconst.UseSkillCheck.USC_ENUM_INVALID_OWNER
        if not code & ignoreReasons and not owner:
            LOG_ERR('skill %s caster error' % (self.getSkillId()))
            return code

        code = gameconst.UseSkillCheck.USC_ENUM_SELF_DIE
        if not code & ignoreReasons and owner.isDie():
            return code

        if utils.hasSkillTagById(self.skillId, gameconst.SkillTag.UltraSkill):
            code = gameconst.UseSkillCheck.USC_ENUM_ULTRA_SKILL_POWER_NOT_ENOUGH
            if not code & ignoreReasons and not owner.isUltraSkillPowerMax():
                owner.combatDebugMsg('_checkUseSkillOwner fail to use ultra skill power not enough: skillId:%s', self.getSkillId())
                return code

        code = gameconst.UseSkillCheck.USC_ENUM_STATE_CONFLICT
        if not code & ignoreReasons:
            extraEventId = self.getSkillEvent(self.skillId)
            if extraEventId:
                if not owner.checkConflictState(extraEventId):
                    owner.combatDebugMsg('_checkUseSkillOwner fail to use skill conflict state extraEventId: skillId:%s, extraEventId:%s', self.getSkillId(), extraEventId)
                    return code
            else:
                if not owner.checkConflictState(CCD.datas.useSkill):
                    owner.combatDebugMsg('_checkUseSkillOwner fail to use skill conflict state useSkill: skillId:%s', self.getSkillId())
                    return code

                if utils.hasSkillTagById(self.skillId, gameconst.SkillTag.GeneralSkill) and not owner.checkConflictState(
                        CCD.datas.useGeneralSkill, False):
                    return code

                skillState = self.getSkillState()
                eventId = CSD.datas[skillState].get('event')
                if eventId and not owner.checkConflictState(eventId):
                    owner.combatDebugMsg('_checkUseSkillOwner fail to use skil conflict state eventId: skillId:%s, eventId:%s', self.getSkillId(), eventId)
                    return code

        return gameconst.UseSkillCheck.USC_ENUM_CHEKC_OK

    def _checkUseSkillTarget(self, owner, targetId, ignoreReasons=0, checkInRange=True):
        needReleaseTarget = self.needReleaseTarget()
        LOG_DBG('_checkUseSkillTarget', self.skillId, targetId, needReleaseTarget)
        owner.combatDebugMsg('_checkUseSkillTarget: skillId:%s, targetId:%s, needReleaseTarget:%s', self.skillId, targetId, needReleaseTarget)
        if self.hasSkillTag(gameconst.SkillTag.SingleHeal):
            target = KBEngine.entities.get(targetId)
            if not target:
                return gameconst.UseSkillCheck.USC_ENUM_CHEKC_OK
            if not utils.checkTargetTypeValid(self.getEffectTarget(self.skillId), owner, target):
                return gameconst.UseSkillCheck.USC_ENUM_CHEKC_OK
            if checkInRange:
                res = self.inRange(owner, target)
            else:
                res = self.inEffectRange(owner, target)
            if not res:
                if self.hasSkillTag(gameconst.SkillTag.Channel) or self.hasSkillTag(gameconst.SkillTag.Casting):
                    owner.showMsg(CONST.datas['targetIsOutOfRange_butCasted']['value'], [])
                else:
                    owner.showMsg(CONST.datas['targetIsOutOfRange']['value'], [])
                    return gameconst.UseSkillCheck.USC_ENUM_SINGLE_HEAL_OUT_OF_RANGE
        if needReleaseTarget:
            target = KBEngine.entities.get(targetId)
            if not target:
                if ignoreReasons & gameconst.UseSkillCheck.USC_ENUM_INVALID_TARGET:
                    return gameconst.UseSkillCheck.USC_ENUM_CHEKC_OK

                else:
                    return gameconst.UseSkillCheck.USC_ENUM_INVALID_TARGET

            code = gameconst.UseSkillCheck.USC_ENUM_INVALID_TARGET
            if not code & ignoreReasons and not utils.checkTargetTypeValid(self.getTarget(self.skillId), owner, target):
                owner.combatDebugMsg('_checkUseSkillTarget skill cannot use because checkTargetTypeValid fail: skillId:%s, targetType:%s, targetId:%s', self.skillId, self.getTarget(self.skillId),
                                     target.id)
                return code

            code = gameconst.UseSkillCheck.USC_ENUM_INVISIBLE_TARGET
            if not code & ignoreReasons and not owner.isVisible(target) and not owner.hasBuffTag(
                    gameconst.BuffTag.TagSeeHiddenEnt):
                owner.combatDebugMsg('_checkUseSkillTarget skill cannot use because target is invisible: skillId:%s, targetId:%s', self.skillId, target.id)
                return code

            code = gameconst.UseSkillCheck.USC_ENUM_CROSS_SPACE
            if not code & ignoreReasons and target.spaceNo != owner.spaceNo:
                owner.combatDebugMsg('_checkUseSkillTarget skill cannot use because cross space: skillId:%s, targetSpaceNo:%s, ownerSpaceNo:%s', self.skillId, target.spaceNo, owner.spaceNo)
                return code

            code = gameconst.UseSkillCheck.USC_ENUM_OUT_OF_RANGE
            if not code & ignoreReasons and not self.inRange(owner, target):
                owner.combatDebugMsg('_checkUseSkillTarget skill cannot use because needReleaseTarget and not inRange: skillId:%s, ownerPosition:%s, targetPosition:%s, distance:%s',
                                     self.getSkillId(), owner.position, target.position, sMath.distance2D(owner.position, target.position))
                return code

        return gameconst.UseSkillCheck.USC_ENUM_CHEKC_OK

    def checkUseSkill(self, owner, targetId, ignoreReasons=0, checkInRange=True):
        code = self._checkUseSkillOwner(owner, targetId, ignoreReasons, checkInRange)
        if code != gameconst.UseSkillCheck.USC_ENUM_CHEKC_OK:
            return code

        return self._checkUseSkillTarget(owner, targetId, ignoreReasons, checkInRange)

    # 延迟结算时间
    def getSkillResultDelay(self, owner, targetId, skillArgs, compensateTime):
        delayTime = self.getFxDelay(self.skillId) - (compensateTime / 1000.0)
        if self.hasSkillTag(gameconst.SkillTag.Channel):
            return sMath.limit(delayTime, 0.0, 9999.0)
        if self.getBulletFx(self.skillId):
            timeEx = self.calBulletTime(owner, targetId)

            delayTime += timeEx
        delayTime = sMath.limit(delayTime, 0.0, 9999.0)
        return delayTime

    def getSkillState(self):
        raise NotImplementedError()

    def enterCDTime(self, owner, delayCd=0):
        LOG_DBG('enterCDTime 1', self.skillId, self.tNextCast, delayCd)
        addCD = 0
        if delayCd > 0:
            addCD = delayCd
            self.tNextCast = time.time() + delayCd
        else:
            addCD = self.getCD(owner)
            self.tNextCast = time.time() + addCD - 0.1
        LOG_DBG('enterCDTime 2', self.skillId, self.tNextCast, addCD, delayCd)

    def refreshSkillCD(self, owner, duration):
        owner.combatDebugMsg('refreshSkillCD: skillId:%s, duration:%s', self.skillId, duration)
        self._cancelTempTimer(owner, gameconst.SkillTempDataKey.RESTORE_CD_TIMER, gametimer.TIMER_TAG_RESTORE_CD)

        if not self.hasTempData(gameconst.SkillTempDataKey.NEXT_CAST):
            self.setTempData(owner, gameconst.SkillTempDataKey.NEXT_CAST, self.tNextCast)
        self.tNextCast = time.time() - 0.1
        owner.client.onSetAddSkillCd(self.skillId, float(self.getCD(owner)), float(self.tNextCast), True, self.getTempData(gameconst.SkillTempDataKey.RELEASE_TIME, 0), self.getTempData(gameconst.SkillTempDataKey.TOTAL_RELEASE_CNT, 0), self.getTempData(gameconst.SkillTempDataKey.RELEASED_CNT, 0), not self.isSkillCDStatusFrozen())
        tid = owner.addTimerCB(duration, '_onSkillCallback', (self, 'invalidateRefreshCD', ()),
                              gametimer.TIMER_TAG_RESTORE_CD)
        self.setTimerTempData(owner, gameconst.SkillTempDataKey.RESTORE_CD_TIMER, tid)

    def invalidateRefreshCD(self, owner, doReset=True, notifyClient=True):
        owner.combatDebugMsg('invalidateRefreshCD: skillId:%s, tempData:%s', self.skillId, self.tempData)
        self.tNextCast = self.getTempData('tNextCast', time.time())
        self.popTempData(gameconst.SkillTempDataKey.RESTORE_CD_TIMER)

        notifyClient and owner.client.onSetAddSkillCd(self.skillId, float(self.getCD(owner)), float(self.tNextCast),
                                                      False, self.getTempData(gameconst.SkillTempDataKey.RELEASE_TIME, 0), self.getTempData(gameconst.SkillTempDataKey.TOTAL_RELEASE_CNT, 0), self.getTempData(gameconst.SkillTempDataKey.RELEASED_CNT, 0), not self.isSkillCDStatusFrozen())
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
        realSkillArgs = skillArgs
        positionSkillArgs = None
        if self.isChangePositionSkill(self.skillId):
            realSkillArgs = list(skillArgs)[:-3]
            positionSkillArgs = list(skillArgs)[-3:]

        hitChooseAgain = SSD.datas[self.skillId].get('HitChooseAgain')
        if hitChooseAgain:
            self.targetIds = []
        effectedEntIds = self.getEffectTargets(owner, targetId, realSkillArgs, positionSkillArgs=positionSkillArgs)
        actionCtx.effectedEntIds = effectedEntIds

        skillEventContext = effectEventCtx.SkillEventCtx(owner.id, self.skillId, realSkillArgs, targetId,
                                                         effectedEntIds, self)
        owner.onEffectEvent('onSkill', owner.id, targetId, skillEventContext)
        owner.onEffectEvent('onSpecSkill', owner.id, targetId, skillEventContext)

        try:
            actResult = owner.doSkillAction(self.skillId, actionCtx, calcDelay, doRemoveState=doRemoveState)
        except Exception as e:
            actResult = gameclass.BoolResult(False)
            gameengine.panicStack('applySkillEffect error:', owner.id, self.skillId, targetId, str(e))

        self.targetIds = []
        owner.combatDebugMsg('applySkillEffect: skillId:%s, targetId:%s, skillArgs:%s, effectedEntIds:%s, actResult:%s', self.skillId, targetId, skillArgs, effectedEntIds, actResult)
        return actResult

    def onSkillActionFinished(self, owner, targetId, skillArgs, context, calcDelay, actionDuration, doRemoveState=True):
        # 技能分为若干个阶段：1.客户端请求施法 2.计算子弹飞行，挥刀等延迟结算 3.结算技能数值
        # 4.结算完等整个技能时间结束(等待客户端收刀等后摇动作)

        # 引导技能在引导结束后再执行skillDone，其他技能结算完就可以skillDone了
        if not self.isInSkill:
            return
        if not self.hasSkillTag(
                gameconst.SkillTag.Channel) and context.actionProgress == gameconst.ActionProgressEnum.actionDone:
            remainTime = self.getSkillTime(self.skillId) - calcDelay - actionDuration
            if remainTime <= 0:
                self.useSkillDone(owner, targetId, skillArgs, doRemoveState=doRemoveState)
            else:
                tid = owner.addTimerCB(remainTime, '_onSkillCallback',
                                      (self, 'useSkillDone', (targetId, skillArgs, True, False, doRemoveState)),
                                      gametimer.TIMER_TAG_SKILL_DONE)

                self._cancelTempTimer(owner, gameconst.SkillTempDataKey.SKILL_DONE_TIMER, gametimer.TIMER_TAG_SKILL_DONE)
                self.setTimerTempData(owner, gameconst.SkillTempDataKey.SKILL_DONE_TIMER, tid)

    def useSkillDone(self, owner, targetId, skillArgs, isSucc=True, startActionFail=False, doRemoveState=True, forceResetSkill=False):
        self._cancelTempTimer(owner, gameconst.SkillTempDataKey.SKILL_DONE_TIMER, gametimer.TIMER_TAG_SKILL_DONE)
        owner.combatDebugMsg('useSkillDone: skillId:%s, targetId:%s, isSucc:%s', self.skillId, targetId, isSucc)
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

        owner.useSkillFinish(self.skillId)

        target = KBEngine.entities.get(targetId)
        endAction = self.getSkillData(self.skillId).get('endSkillAction', None)
        # startAction释放成功了才执行endAction，目前只有位移技能的startAction有返回值可能返回失败
        if endAction and not startActionFail and isSucc:
            realSkillArgs = skillArgs
            if self.isChangePositionSkill(self.skillId):
                realSkillArgs = skillArgs[:-3]
            effectedEntIds = self.getEffectTargets(owner, targetId, realSkillArgs)
            actionCtx = actionContext.UseSkillCtx(
                owner.id, 
                self.skillId, 
                skillArgs, 
                targetId, 
                effectedEntIds, 
                self,
                None, 
                isSucc=isSucc)
            endAction(owner, target, actionCtx)

        # 在aiController的useSkillDone里面会把当前这个skillId pop掉，改为放在最后把
        owner.IsAICombatUnit and owner.aiController and owner.aiController.useSkillDone(self.skillId)

    def getRealSkillVal(self, owner):
        # 目前只有StageSkill实现了这个方法
        return self, False

    def doActionOnChangeSlot(self, owner, bActive):
        if bActive:
            action = self.getActivateAction(self.skillId)
        else:
            action = self.getDeactivateAction(self.skillId)

        action and action(owner, owner, actionContext.ChangeSkillSlotCtx(self.skillId))

    def onChangedFromSkill(self, fromSkillVal):
        self.tNextCast = fromSkillVal.tNextCast
        self.skillLv = fromSkillVal.skillLv

    def onTimerCallback(self, owner, callbackName, args):
        getattr(self, callbackName)(owner, *args)

    def getSavedDict(self):
        return {}

    def loadSavedDict(self, data):
        pass

    def onChangedSkillBegin(self, owner):
        if self.hasTempData(gameconst.SkillTempDataKey.RESTORE_CD_TIMER):
            self._cancelTempTimer(owner, gameconst.SkillTempDataKey.RESTORE_CD_TIMER, gametimer.TIMER_TAG_RESTORE_CD)
            self.invalidateRefreshCD(owner, doReset=False, notifyClient=False)
        self.enterCDTime(owner)
        owner.client.onSetAddSkillCd(self.skillId, float(self.getCD(owner)), float(self.tNextCast), False, self.getTempData(gameconst.SkillTempDataKey.RELEASE_TIME, 0), self.getTempData(gameconst.SkillTempDataKey.TOTAL_RELEASE_CNT, 0), self.getTempData(gameconst.SkillTempDataKey.RELEASED_CNT, 0), not self.isSkillCDStatusFrozen())

    def isSkillCDStatusFrozen(self):
        return self.getTempData(gameconst.SkillTempDataKey.CHANGE_SKILL_CD_STATUS, gameconst.SkillCDStatus.DEFAULT) == gameconst.SkillCDStatus.DISABLED

    def hasTempData(self, name):
        return name in self.tempData

    def getTempData(self, name, defalut=None):
        return self.tempData.get(name, defalut)

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
        owner.combatDebugMsg('resetSkill: skillId:%s, resetSkillReason:%s, doRemoveState:%s', self.skillId, reason, doRemoveState)
        self.isInSkill = False
        owner.removeUseSkillRecord(self.skillId)
        skillState = self.getSkillState()
        if owner.hasState(skillState) and doRemoveState:
            owner.removeState(skillState)

        if self.hasSkillTag(gameconst.SkillTag.Channel):
            owner.removeState(gameconst.StateEnum.UsingSkill)

        if self._cancelTempTimer(owner, gameconst.SkillTempDataKey.RESTORE_CD_TIMER, gametimer.TIMER_TAG_RESTORE_CD):
            self.invalidateRefreshCD(owner, doReset=False)

        self._cancelTempTimer(owner, gameconst.SkillTempDataKey.DELAY_CALC_TIMER, gametimer.TIMER_TAG_SKILL_DELAY_CALC)
        self._cancelTempTimer(owner, gameconst.SkillTempDataKey.SKILL_DONE_TIMER, gametimer.TIMER_TAG_SKILL_DONE)
        self._cancelTempTimer(owner, gameconst.SkillTempDataKey.MUL_ATTACK_ACT_TIMER, gametimer.TIMER_TAG_DO_SKILL_ACTION)
        self.clearTempData()
        self.targetIds = []

    def childSkills(self):
        return ()

# 普通技能
class CommonSkillVal(SkillBase):
    def getSkillState(self):
        if self.hasSkillTag(gameconst.SkillTag.Channel):
            if self.isMovingSkill(self.skillId):
                return gameconst.StateEnum.moveChannel

            return gameconst.StateEnum.Channeling
        elif self.hasSkillTag(gameconst.SkillTag.GeneralSkill):
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
        rootSkill = self
        while rootSkill.parentSkill:
            rootSkill = rootSkill.parentSkill
        return rootSkill

    def getNotifyClientSkillId(self):
        return self.skillId, self.skillLv

    def beginUseSkill(self, owner, targetId, skillArgs, compensateTime, doSetState=True, enterCD=True, parentCtx=None):
        isSucc = self.doBeginUseSkill(
            owner, 
            targetId, 
            skillArgs,
            compensateTime,
            doSetState, 
            enterCD, 
            parentCtx)

        if not isSucc:
            owner.client.onUseSkill(False, self.skillId, targetId, [], [], [])

        return isSucc

    def beginUseSkillStartAction(self, owner, targetId, skillArgs, compensateTime, doSetState=True, enterCD=True, parentCtx=None):
        self.isInSkill = True
        self.setTempData(owner, gameconst.SkillTempDataKey.SKILL_ARGS, skillArgs)
        owner.combatDebugMsg('SkillBase.beginUseSkillStartAction: skillId:%s, targetId:%s, skillArgs:%s', self.skillId, targetId, skillArgs)
        target = KBEngine.entities.get(targetId)
        startAction = self.getStartAction(self.skillId)
        startActionFail = False
        startActionResult = gameconst.StartActionResult.Success

        if self.hasTempData(gameconst.SkillTempDataKey.RESTORE_CD_TIMER):
            self._cancelTempTimer(owner, gameconst.SkillTempDataKey.RESTORE_CD_TIMER, gametimer.TIMER_TAG_RESTORE_CD)
            self.invalidateRefreshCD(owner, doReset=False)

        extraEventId = self.getSkillEvent(self.skillId)
        if extraEventId:
            owner.checkConflictState(extraEventId, remConflctState=True)

        if doSetState:
            skillState = self.getSkillState()
            owner.setState(skillState)

        realSkillArgs = skillArgs
        positionSkillArgs = None
        if self.isChangePositionSkill(self.skillId):
            realSkillArgs = list(skillArgs)[:-3]
            positionSkillArgs = tuple(skillArgs[-3:])

        effectedEntIds = self.getEffectTargets(owner, targetId, realSkillArgs, positionSkillArgs=positionSkillArgs, context = parentCtx)
        skillResult = SkillDamges(owner.id)
        actionCtx = actionContext.UseSkillCtx(
            owner.id, 
            self.skillId, 
            skillArgs, 
            targetId, 
            effectedEntIds, 
            self,
            skillResult, 
            parentCtx=parentCtx)

        actionCtx.actionProgress = gameconst.ActionProgressEnum.startActionDone
        if startAction:
            # start action先不给传effectedEntIds，因为可能还没开始结算
            # start action里加的buff什么的不能依赖在技能action里解除,技能可能在延迟后不能执行action
            # 例如旋风斩开始加的无敌需要在end action去删除
            ctxFunc = lambda r: actionCtx
            if owner.doCombatActions(startAction, owner, target, owner.id, ctxFunc) is False:
                startActionFail = True
                startActionResult = gameconst.StartActionResult.Fail

        if startActionFail:
            owner.combatDebugMsg('SkillBase.beginUseSkillStartAction do startAction fail: skillId:%s, targetId:%s, ownerPosition:%s', self.skillId, targetId, owner.position)
            self.useSkillDone(owner, targetId, skillArgs, isSucc=False, startActionFail=startActionFail)
            return startActionResult, None, None
        elif utils.hasSkillTagById(self.skillId, gameconst.SkillTag.UltraSkill):
            owner.ultraSkillPower = 0

        if (not owner.IsAvatar or owner.gmModeCell != gameconst.GmModeEnum.GM_NO_SKILLCD) and enterCD and not self.hasSkillTag(
                gameconst.SkillTag.Channel):
            host = owner.getAvatar()
            LOG_DBG("in beginUseSkillStartAction ", owner, self.skillId, owner.IsAvatar, host, targetId, skillArgs)
            if host:
                addValue = 0
                ret, datas = host.getInscriptionEffects(self.skillId, gameconst.InscriptionEffectType.SKILL_RELEASE_ADD_COUNT)
                if ret:
                    if len(datas) == 1:
                        addValue = datas[0]
                        LOG_IFO("in beginUseSkillStartAction, inscription effect is triggered, skill_id:{0}, effect_type{1}, effect_value{2}", self.skillId, gameconst.InscriptionEffectType.SKILL_RELEASE_ADD_COUNT, datas)

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
            self.enterCDTime(owner)
            owner.client.onSetAddSkillCd(self.skillId, float(self.getCD(owner)), float(self.tNextCast), False, self.getTempData(gameconst.SkillTempDataKey.RELEASE_TIME, 0), self.getTempData(gameconst.SkillTempDataKey.TOTAL_RELEASE_CNT, 0), self.getTempData(gameconst.SkillTempDataKey.RELEASED_CNT, 0), not self.isSkillCDStatusFrozen())

        owner.IsAvatar and owner.modifyMP(-self.getCostMp(owner, self.skillId, owner.mpCostRatio))

        # startAction里可能会攻击别人然后被反噬死。。
        if owner.isDie():
            owner.combatDebugMsg('SkillBase.beginUseSkillStartAction die after startAction: skillId:%s, ownerId:%s, targetId:%s, ownerPosition:%s', self.skillId, owner.id, targetId,
                                 owner.position)
            self.useSkillDone(owner, targetId, skillArgs, isSucc=False, startActionFail=startActionFail)
            return gameconst.StartActionResult.Fail, None, None

        return startActionResult, actionCtx, effectedEntIds

    def doBeginUseSkill(self, owner, targetId, skillArgs, compensateTime, doSetState=True, enterCD=True, parentCtx=None):
        isSucc, actionCtx, effectTargetIds = self.beginUseSkillStartAction(
            owner, 
            targetId, 
            skillArgs,
            compensateTime,
            doSetState, 
            enterCD, 
            parentCtx)

        skillId, skillLv = self.getNotifyClientSkillId()
        skillArgsExtra = [self.getRange(owner, skillId, skillLv), self.getEffectRange(owner, skillId, skillLv)]
        if not isSucc:
            owner.client.onUseSkill(False, skillId, targetId, [], [], [])
            return isSucc

        if self.isChangePositionSkill(self.skillId):
            if len(skillArgs) <= 3:
                target = KBEngine.entities.get(targetId)
                positionArgs = self.getSkillDesPosition(owner, target, skillArgs)
                skillArgs = skillArgs + positionArgs

        calcDelay = self.getSkillResultDelay(owner, targetId, skillArgs, compensateTime)
        # ChannelingSkillVal废除，因为吟唱后也需要可以引导，所以把引导合并到CommonSkillVal
        if self.hasSkillTag(gameconst.SkillTag.Channel):
            owner.setTempMiscProp(gameconst.EntityPropsEnum.currentChannelSkill, self)

            owner.combatDebugMsg('CommonSkillVal.doBeginUseSkill channel skill: skillId:%s, targetId:%s, skillArgs:%s, compensateTime:%s, calcDelay:%s, ownerPosition:%s', self.skillId, targetId, skillArgs, compensateTime, calcDelay, owner.position)
            self.startChanneling(owner, targetId, skillArgs, calcDelay, actionCtx)
            owner.allClients.onUseSkill(isSucc, skillId, targetId, skillArgs, effectTargetIds, skillArgsExtra)
        else:
            owner.combatDebugMsg('CommonSkillVal.doBeginUseSkill: skillId:%s, targetId:%s, skillArgs:%s, compensateTime:%s, calcDelay:%s', self.skillId, targetId, skillArgs, compensateTime, calcDelay)

            if actionCtx.actionProgress == gameconst.ActionProgressEnum.startActionDone:
                if calcDelay > 0:
                    if self.needReleaseTarget() and not (owner.IsMonster and self.isMultiCastSkill(owner, actionCtx)):
                        self.targetIds = effectTargetIds

                    self.setTimerTempData(owner, 
                        gameconst.SkillTempDataKey.DELAY_CALC_TIMER,
                        owner.addTimerCB(
                            calcDelay + 0.1,
                            'delayCalcSkill',
                            (
                                self, targetId,
                                skillArgs,
                                actionCtx,
                                calcDelay,
                                doSetState),
                            gametimer.TIMER_TAG_SKILL_DELAY_CALC))

                    owner.allClients.onUseSkill(True, skillId, targetId, skillArgs,
                                                effectTargetIds, skillArgsExtra)
                else:
                    # 保证onUseSkill在_doUseSkill前
                    self.targetIds = effectTargetIds
                    if owner.isReal():
                        owner.allClients.onUseSkill(True, skillId, targetId, skillArgs,
                                                    effectTargetIds, skillArgsExtra)
                    owner._doUseSkill(self, targetId, skillArgs, actionCtx, calcDelay, doSetState)

        return isSucc

    def startChanneling(self, caster, targetID, arr, delayTime, actionCtx):
        self.channelCount = 0
        timerId = caster.addTimerCB(delayTime, 'channelingSkillTick',
                                   (self, targetID, arr, tuple(caster.position), actionCtx),
                                   gametimer.TIMER_TAG_CHANNELING_CALC)
        self.setTimerTempData(caster, gameconst.SkillTempDataKey.CHANNELING_CALC_TIMER, timerId)
        self.setTempData(caster, gameconst.SkillTempDataKey.T_CHANNELING_START, time.time() + delayTime)

    def calBulletTime(self, owner, targetId):
        target = KBEngine.entities.get(targetId)
        if target:
            bulletTimeScale = self.getBulletTimeScale(self.skillId)
            timeEx = self.getBulletFxTime(self.skillId) * (
                    1 - bulletTimeScale + bulletTimeScale * sMath.distance2D(owner.position,
                                                                             target.position) / self.getRange(owner, self.skillId, self.skillLv))
        else:
            timeEx = self.getBulletFxTime(self.skillId) if self.getBulletFxTime(self.skillId) else 0.5
        return timeEx

    def onChannelingEnd(self, owner, isFinished):
        owner._endChannelingSkill(isFinished)
        self.useSkillDone(owner, 0, self.popTempData(gameconst.SkillTempDataKey.SKILL_ARGS, []))

    def onChannlingEffectEnd(self, owner):
        postSkillTime = self.getSkillTime(self.skillId)
        owner.removeState(self.getSkillState(), removeReason=gameconst.ChannelingBreak.BREAK_TP_NORMAR_END)
        self.enterCDTime(owner)
        owner.client.onSetAddSkillCd(self.skillId, float(self.getCD(owner)), float(self.tNextCast), False, self.getTempData(gameconst.SkillTempDataKey.RELEASE_TIME, 0), self.getTempData(gameconst.SkillTempDataKey.TOTAL_RELEASE_CNT, 0), self.getTempData(gameconst.SkillTempDataKey.RELEASED_CNT, 0), not self.isSkillCDStatusFrozen())
        if postSkillTime > 0:
            owner.setState(gameconst.StateEnum.UsingSkill)
            endTimer = owner.addTimerCB(postSkillTime, '_onSkillCallback', (self, 'onChannelingEnd', (True,)),
                                       gametimer.TIMER_TAG_ON_CHANNELING_END)
            self.setTimerTempData(owner, gameconst.SkillTempDataKey.CHANNELING_END_TIMER, endTimer)
        else:
            self.onChannelingEnd(owner, True)

    def resetSkill(self, owner, reason=gameconst.ResetSkillReason.ReasonDefault, doRemoveState=True):
        if self.hasSkillTag(gameconst.SkillTag.Channel):
            self._cancelTempTimer(owner, gameconst.SkillTempDataKey.CHANNELING_CALC_TIMER, gametimer.TIMER_TAG_CHANNELING_CALC)
            self._cancelTempTimer(owner, gameconst.SkillTempDataKey.CHANNELING_BULLET_TIMER, gametimer.TIMER_TAG_CHANNELING_SKILL_EFFECT)
            self._cancelTempTimer(owner, gameconst.SkillTempDataKey.CHANNELING_END_TIMER, gametimer.TIMER_TAG_ON_CHANNELING_END)
            self.popTempData(gameconst.SkillTempDataKey.IS_CHANNELING_EMPTY, False)
            self.channelCount = 0
        if self.hasSkillTag(gameconst.SkillTag.Lunge) and owner.hasState(gameconst.StateEnum.Shifting):
            owner.endLunge(self, 0, [])
        super(CommonSkillVal, self).resetSkill(owner, reason, doRemoveState)


class ChongfengSkillVal(CommonSkillVal):
    def getSkillState(self):
        if self.isMovingSkill(self.skillId):
            return gameconst.StateEnum.moveSkill

        return gameconst.StateEnum.UsingSkill

    def resetSkill(self, owner, reason=gameconst.ResetSkillReason.ReasonDefault, doRemoveState=True):
        if owner.hasState(gameconst.StateEnum.Shifting):
            owner.endChongfeng(self, 0, [])
        super(ChongfengSkillVal, self).resetSkill(owner, reason, doRemoveState)


# 刺客突进技能
class LungeSkillVal(CommonSkillVal):
    def getSkillState(self):
        if self.isMovingSkill(self.skillId):
            return gameconst.StateEnum.moveSkill

        return gameconst.StateEnum.UsingSkill

    def resetSkill(self, owner, reason=gameconst.ResetSkillReason.ReasonDefault, doRemoveState=True):
        if owner.hasState(gameconst.StateEnum.Shifting):
            owner.endLunge(self, 0, [])
        super(LungeSkillVal, self).resetSkill(owner, reason, doRemoveState)


# 闪避技能
class DodgeSkillVal(CommonSkillVal):
    def getSkillState(self):
        return gameconst.StateEnum.Dodging

    def beginUseSkill(self, owner, targetId, skillArgs, compensateTime, doSetState=True, enterCD=True, parentCtx=None):
        owner.resetUsingSkills(gameconst.ResetSkillReason.ReasonDodgeSkill)
        return super(DodgeSkillVal, self).beginUseSkill(owner, targetId, skillArgs,
                                                                                      compensateTime,
                                                                                      doSetState, enterCD, parentCtx)

    def resetSkill(self, owner, reason=gameconst.ResetSkillReason.ReasonDefault, doRemoveState=True):
        if owner.hasState(gameconst.StateEnum.Dodging):
            owner.endDodge(self, 0, [])
        super(DodgeSkillVal, self).resetSkill(owner, reason, doRemoveState)

    def checkUseSkill(self, owner, targetId, ignoreReasons=0, checkInRange=True):
        return super(DodgeSkillVal, self).checkUseSkill(owner, targetId, ignoreReasons, checkInRange)


# 吟唱技能:多一个吟唱的普通技能
class CastingSkillVal(CommonSkillVal):
    def __init__(self, skillId, skillLv, tNextCast=0.0, cdDelta=0.0, parentSkill=0):
        super(CastingSkillVal, self).__init__(skillId, skillLv, tNextCast, cdDelta, parentSkill)
        self.castingStartTime = 0

    def onChangedFromSkill(self, fromSkillVal):
        super(CastingSkillVal, self).onChangedFromSkill(fromSkillVal)
        if fromSkillVal.hasSkillTag(gameconst.SkillTag.Casting):
            self.castingStartTime = fromSkillVal.castingStartTime

    def checkUseSkill(self, owner, targetID, ignoreReasons=0, checkInRange=True):
        realSkillVal, _ = self.getRealSkillVal(owner)
        if realSkillVal != self:
            ret = super(CastingSkillVal, self).checkUseSkill(owner, targetID, ignoreReasons, checkInRange)
        else:
            castingSucc = self.isCastingSucc()
            if castingSucc:
                ignoreReasons |= gameconst.UseSkillCheck.USC_ENUM_OUT_OF_RANGE

            ret = super(CastingSkillVal, self).checkUseSkill(owner, targetID, ignoreReasons, checkInRange)

            if not castingSucc:
                code = gameconst.UseSkillCheck.USC_ENUM_NEED_CAST
                if not code & ignoreReasons:
                    LOG_IFO('use casting skill before finishing casting', self.skillId, time.time(),
                              self.castingStartTime, self.getCastingtimeMax(self.skillId))
                    return code | ret

            elif ret == gameconst.UseSkillCheck.USC_ENUM_CHEKC_OK:
                target = KBEngine.entities.get(targetID)
                if target and self.needReleaseTarget() and not sMath.inRange2D(gameconst.DEFAULT_AOI, owner.position,
                                                                               target.position):
                    code = gameconst.UseSkillCheck.USC_ENUM_OUT_OF_RANGE
                    if not code & ignoreReasons:
                        return code

        return ret

    def getEffectTargets(self, caster, targetId, arr, forceTarget=False, positionSkillArgs=None, context=None):
        target = KBEngine.entities.get(targetId)
        if (targetId > 0 and not target) or not caster:
            targetId = 0

        forceTarget = self.needReleaseTarget()

        targetIds = super(CastingSkillVal, self).getEffectTargets(caster, targetId, arr, forceTarget, positionSkillArgs, context)

        return targetIds

    def startCasting(self, caster, actionCtx):
        if caster.IsAvatar and caster.mp < self.getCostMp(caster, self.skillId, caster.mpCostRatio):
            return

        self.castingStartTime = time.time()

        tid = caster.addTimerCB(1, 'castingSkillCheck', (actionCtx.useTargetId, actionCtx.skillArgs, tuple(caster.position)),
                               gametimer.TIMER_TAG_CASTING_CHECK)
        self.setTimerTempData(caster, gameconst.SkillTempDataKey.CASTING_CHECK_TIMER, tid)
        # caster.setTempMiscProp(gameconst.EntityPropsEnum.castingCheckTimer, checkTimer)

        # #主角由客户端发起释放，其他实体服务器自动放
        # if not caster.IsAvatar or caster._castSkillByServer():
        # 可能是action里cast的技能，直接用技能对象放
        castingTime = self.getCastingtimeMax(self.skillId)
        useTimer = caster.addTimerCB(castingTime, '_useSkillBySkillObj', (self, actionCtx),
                                    gametimer.TIMER_TAG_CASTING_SKILL)
        self.setTimerTempData(caster, gameconst.SkillTempDataKey.CASTING_SKILL_TIMER, useTimer)

        castingAction = self.getSkillData(self.skillId).get('castingAction')
        if castingAction:
            target = KBEngine.entities.get(actionCtx.useTargetId)
            castingAction(caster, target, actionContext.SkillCommonCtx(self.skillId))

    def isCastingSucc(self, delta=0.5):
        if not self.castingStartTime:
            return False
        return time.time() - self.castingStartTime >= self.getCastingtimeMax(self.skillId) - delta

    def onCastingInterrupted(self, owner, reason):
        self.castingStartTime = 0
        cdType = self.getSkillData(self.skillId).get('CDAfterInterrupt', 0)

        needCd = False
        if cdType == gameconst.CastingSkillCDType.IgnoreMove:
            if reason not in (
                    gameconst.EndCasting.ECEnumMove, gameconst.EndCasting.ECEnumClientCancel, gameconst.EndCasting.ECEnumMissingTarget,
                    gameconst.EndCasting.ECEnumDead, gameconst.EndCasting.ECEnumTeleporting, gameconst.EndCasting.ECEnumclientPick):
                needCd = True
        elif cdType == gameconst.CastingSkillCDType.EnterCD:
            needCd = True
        elif cdType == gameconst.CastingSkillCDType.NotEnterCD:
            pass

        if needCd:
            super(CastingSkillVal, self).enterCDTime(owner)
            owner.client.onSetAddSkillCd(self.skillId, float(self.getCD(owner)), float(self.tNextCast), False, self.getTempData(gameconst.SkillTempDataKey.RELEASE_TIME, 0), self.getTempData(gameconst.SkillTempDataKey.TOTAL_RELEASE_CNT, 0), self.getTempData(gameconst.SkillTempDataKey.RELEASED_CNT, 0), not self.isSkillCDStatusFrozen())

        owner.IsAICombatUnit and owner.aiController and owner.aiController.onCastingInterrupted(self.skillId)

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
    def __init__(self, skillId, skillLv, tNextCast=0.0, cdDelta=0.0, parentSkill=0):
        super(StagedSkill, self).__init__(skillId, skillLv, tNextCast, cdDelta, parentSkill)
        self.stageIndex = 0

    def canRemoveFromBuild(self):
        return self.stageIndex == 0 and super(StagedSkill, self).canRemoveFromBuild()

    def checkUseSkill(self, owner, targetId, ignoreReasons=0, checkInRange=True):
        realSkillVal, _ = self.getRealSkillVal(owner)
        if realSkillVal == self:
            return super(StagedSkill, self).checkUseSkill(owner, targetId, ignoreReasons, checkInRange)

        return realSkillVal.checkUseSkill(owner, targetId, ignoreReasons, checkInRange)

    def childSkills(self):
        _dic = self.getTempData(gameconst.SkillTempDataKey.STAGE_CHILD, {})
        _retList = []
        for _skill in _dic.values():
            if not _skill():
                continue

            _retList.append(_skill())

        return _retList

    def getRealSkillVal(self, owner):
        if self.stageIndex == 0:
            return self, False
        else:
            curStageSkillId = self.getSkillIdForStage(self.stageIndex)
            if not curStageSkillId:
                return self, False

            childDic = self.getTempData(gameconst.SkillTempDataKey.STAGE_CHILD, {})
            if curStageSkillId in childDic and childDic[curStageSkillId]():
                return childDic[curStageSkillId](), False

            curStageSkill = StagedSkill(curStageSkillId, self.skillLv, parentSkill=self)
            childDic[curStageSkillId] = weakref.ref(curStageSkill)

            self.setTempData(owner, gameconst.SkillTempDataKey.STAGE_CHILD, childDic)
            return curStageSkill, False

    def getSkillIdForStage(self, stageIndex):
        if stageIndex == 0:
            return self.skillId
        stageSkillIds = self.getSkillData(self.skillId).get('mulSkillID')
        if stageSkillIds and len(stageSkillIds) >= stageIndex:
            return stageSkillIds[stageIndex - 1]
        return 0

    def beginUseSkill(self, owner, targetId, skillArgs, compensateTime, doSetState=True, enterCD=True, parentCtx=None):
        rootSkillVal = self.getRootSkillVal()
        owner.combatDebugMsg('StageSkill.beginUseSkill: skillId:%s, stageIndex:%s, targetId:%s, skillArgs:%s, doSetState:%s, rootSkillId:%s',
                             self.skillId, self.stageIndex, targetId, skillArgs,
                             doSetState, rootSkillVal.skillId)
        nextStageSkillId = self.getSkillIdForStage(self.stageIndex + 1)

        # 如果有下一段就不进入cd
        enterCD = (nextStageSkillId == 0)
        if self.stageIndex == 0:
            self is rootSkillVal and self.gotoNextStage(owner)
            isSucc = self.doBeginUseSkill(
                owner, 
                targetId, 
                skillArgs,
                compensateTime, 
                doSetState,
                enterCD, 
                parentCtx)
        else:
            curStageSkill, _ = self.getRealSkillVal(owner)
            if curStageSkill is self:
                raise Exception('ckz curStageSkill is self', self.skillId, self.stageIndex, owner.gbId)

            self is rootSkillVal and self.gotoNextStage(owner)
            isSucc = curStageSkill.beginUseSkill(owner, targetId, skillArgs,
                                                                                compensateTime, doSetState, enterCD,
                                                                                parentCtx)

        if isSucc:
            if self.hasTempData(gameconst.SkillTempDataKey.STAGE_CD_TIMER):
                self._cancelTempTimer(owner, gameconst.SkillTempDataKey.STAGE_CD_TIMER, gametimer.TIMER_TAG_ON_STAGE_END)
                self.popTempData(gameconst.SkillTempDataKey.STAGE_CD_TIMER)
        else:
            return gameconst.StartActionResult.Fail

        if nextStageSkillId:
            # 只有root技能才能走到这里，子技能是走不到的，所以onStageEnd是只有root才会调用
            stageDuration = SSD.datas[nextStageSkillId]['mulSkillCD']
            cdTimer = owner.addTimerCB(stageDuration, '_onSkillCallback', (self, 'onStageEnd', (True,)),
                                        gametimer.TIMER_TAG_ON_STAGE_END)
            self.setTimerTempData(owner, gameconst.SkillTempDataKey.STAGE_CD_TIMER, cdTimer)

            clientStageIdx = self.stageIndex
        else:
            clientStageIdx = 0

        ##阶段技能只有普通技能的第一段以及强化后的第一段可以给客户端提交相关数据
        stageSkillIds = self.getSkillData(self.skillId).get('mulSkillID')
        curTime = time.time()
        stageSkillIds and owner.IsAvatar and owner.allClients.onUseStageSkill(rootSkillVal.skillId, clientStageIdx,
                                                                                curTime)

        return isSucc

    def gotoNextStage(self, owner):
        self.stageIndex += 1
        if self.isLastStage(owner):
            self.onStageEnd(owner)

    def isLastStage(self, owner):
        # stageIndex是下次释放技能的stage
        return not self.getSkillIdForStage(self.stageIndex)

    # 超时或放完最后一段结束多段技能
    def onStageEnd(self, owner, endByTimeout=False):
        # 目前只有root才会走到这里
        self._cancelTempTimer(owner, gameconst.SkillTempDataKey.STAGE_CD_TIMER, gametimer.TIMER_TAG_ON_STAGE_END)
        rootSkillVal = self.getRootSkillVal()
        owner.combatDebugMsg('StageSkill.onStageEnd: skillId:%s, rootSkillId:%s, rootSkillStageIndex:%s',
                             self.skillId, rootSkillVal.skillId, rootSkillVal.stageIndex)
        rootSkillVal.enterCDTime(owner)
        owner.client.onSetAddSkillCd(rootSkillVal.skillId, float(rootSkillVal.getCD(owner)),
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
            if self is not rootSkillVal and rootSkillVal.isLastStage(owner):
            # 多段技能结束，通知父技能Done, 多段的技能不能设置force，不然可能会无限循环
                rootSkillVal.useSkillDone(owner, targetId, skillArgs, isSucc, startActionFail, forceResetSkill=False)

    def needResetOnSkillDone(self, owner):
        # 如果技能使用成功且还有下一段就先不reset，否则被reset到第一段了,等着onStageEnd里去reset
        rootSkillVal = self.getRootSkillVal()
        if self.isLastStage(owner):
            return True

        if self is rootSkillVal:
            return False

        return True

    def resetSkill(self, owner, reason=gameconst.ResetSkillReason.ReasonDefault, doRemoveState=True):
        if reason == gameconst.ResetSkillReason.ReasonTeleport or reason == gameconst.ResetSkillReason.ReasonTransform or reason == gameconst.ResetSkillReason.ReasonDuelComplete:
            if self.stageIndex > 0:
                self.enterCDTime(owner)
                owner.client.onSetAddSkillCd(self.skillId, float(self.getCD(owner)), float(self.tNextCast), False, self.getTempData(gameconst.SkillTempDataKey.RELEASE_TIME, 0), self.getTempData(gameconst.SkillTempDataKey.TOTAL_RELEASE_CNT, 0), self.getTempData(gameconst.SkillTempDataKey.RELEASED_CNT, 0), not self.isSkillCDStatusFrozen())
                rootSkillVal = self.getRootSkillVal()
                owner.IsAvatar and owner.client.onUseStageSkill(rootSkillVal.skillId, 0, time.time())

        self.stageIndex = 0
        self._cancelTempTimer(owner, gameconst.SkillTempDataKey.STAGE_CD_TIMER, gametimer.TIMER_TAG_ON_STAGE_END)

        super(StagedSkill, self).resetSkill(owner, reason, doRemoveState)


# 超级技能
class UltraSkillVal(CommonSkillVal):
    def getSkillState(self):
        return gameconst.StateEnum.speicalSkill

    def checkUseSkill(self, owner, targetId, ignoreReasons=0, checkInRange=True):
        return super(UltraSkillVal, self).checkUseSkill(owner, targetId, ignoreReasons, checkInRange)


def getSkillClass(skillId):
    skillData = SkillBase.getSkillData(skillId)
    if not skillData:
        return
    tags = SkillBase.getTag(skillId)

    if gameconst.SkillTag.Casting in tags:
        return CastingSkillVal
    elif gameconst.SkillTag.MulStageSkill in tags:
        return StagedSkill
    elif gameconst.SkillTag.Chongfeng in tags:
        return ChongfengSkillVal
    elif gameconst.SkillTag.Lunge in tags:
        return LungeSkillVal
    elif gameconst.SkillTag.DodgeSkill in tags:
        return DodgeSkillVal
    elif gameconst.SkillTag.UltraSkill in tags:
        return UltraSkillVal
    else:
        return CommonSkillVal
