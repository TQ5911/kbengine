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

    def add(self, owner, skillId, skillLv, **kwargs):
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
                    DEBUG_MSG("initial skill switch status 0 ", skillId, switchStatus)
                self.skillSwitches[skillId] = switchStatus
        return self[skillId]

    def getClientData(self, owner):
        skills = []
        for skillId, skillInstance in self.items():
            skillDict = {
                'skillId': skillId,
                'tNextCast': skillInstance.tNextCast,
                'skillCd': skillInstance.getCD(owner),
                'extraSkillLv': skillInstance.getExtraLv(owner),
            }
            skills.append(skillDict)

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
        }
        INFO_MSG("getClientData  ", clientData)
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
    
    def setSkillSwitch(self, skillID, status):
        if not SSD.datas.get(skillID, None):
            ERROR_MSG("setSkillSwitch illeagal skill id", skillID, status)
            return
        if status not in gameconst.SkillSwitchStatus.VALID_STATUS:
            ERROR_MSG("setSkillSwitch illeagal switch status", skillID, status)
            return    
        self.skillSwitches[skillID] = status

    def _lateReload(self):
        super(ServerSkills, self)._lateReload()
        for v in self.values():
            v.reloadScript()

        return

class SkillDamageVal(userType.UserSoleType):
    def __init__(self, targetId, hurt, hitType):
        self.targetId = targetId
        self.hurt = int(hurt)
        self.hitType = hitType


class SkillDamges(userType.UserSoleType):
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


class RuneVal(userType.UserSoleType):
    def __init__(self, runeIndex, runeIdList, position, spaceNo):
        self.runeIndex = runeIndex
        self.runeIdList = runeIdList
        self.position = position
        self.spaceNo = spaceNo


class Runes(userType.UserSoleType):
    def __init__(self):
        self.runes = []

    def _lateReload(self):
        super(Runes, self)._lateReload()

        for v in self.runes:
            v.reloadScript()

        return


class DamageResult(userType.UserSoleType):
    def __init__(self, dmg=0, hpSuck=0, atkType=0, calcShield=True, hurtDmg=0):
        self.dmg = dmg  # 输出伤害
        self.atkType = atkType
        self.hpSuck = hpSuck
        self.calcShield = calcShield
        self.hurtDmg = hurtDmg  # 受伤害值，用于承伤统计，实际结算数值用dmg


class HealResult(userType.UserSoleType):
    def __init__(self, healVal=0, isCrit=False, doSkillHealCorrection=False):
        self.healVal = healVal
        self.isCrit = isCrit
        self.doSkillHealCorrection = doSkillHealCorrection


class AntiControlResult(userType.UserSoleType):
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


class ControlState(userType.UserSoleType):
    def __init__(self, controlLv, tStart):
        self.controlLv = controlLv
        self.tStart = tStart
        self.removeTimerId = 0

    def refreshAntiTimer(self, owner, antiControlState, antiDuration):
        if self.removeTimerId:
            owner._cancelCallback(self.removeTimerId, gametimer.TIMER_TAG_REMOVE_COMBAT_CONTROL_STATE)

        self.removeTimerId = owner._callback(antiDuration, 'removeCombatControlState', (antiControlState,),
                                             gametimer.TIMER_TAG_REMOVE_COMBAT_CONTROL_STATE)

    def addControlLv(self, val):
        self.controlLv = int(self.controlLv + val)

    def resetTimerId(self):
        self.removeTimerId = 0


class SkillBase(userType.UserSoleType):
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
        cls.getMaxTargetNum.cache_clear()
        cls.getChannelTime.cache_clear()
        cls.getInterruptByAttack.cache_clear()
        cls.getScope.cache_clear()
        cls.getScopeParam.cache_clear()
        cls.getCostMp.cache_clear()
        cls.getMpPerSec.cache_clear()
        cls.getRange.cache_clear()
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
        cd = self.getSkillData(self.skillId).get('CD', 0)
#         【【战斗】技能冷却加速属性没生效】
# https://www.tapd.cn/tapd_fe/59721401/bug/detail/1159721401001004163
        #realCD = (cd + owner.adjCD) * (1 + owner.mulCD) + self.cdDelta'
        realCD = cd * (1 - owner.skillCD) + self.cdDelta
        realCD = sMath.limit(realCD, 0.1, 999999)
        gcd = self.getGlobalCD(owner)
        return max(realCD, gcd)

    def changeCD(self, owner, delta):
        owner.combatDebugMsg("setCdByEffect ", self.getSkillId(), delta, self.inCDTime())
        self.cdDelta += delta

        owner.IsAvatar and owner.client.onSetAddSkillCd(self.skillId, float(self.getCD(owner)), float(self.tNextCast),
                                                        False)

    def changeNextCast(self, owner, delta):
        self.tNextCast += delta
        owner.IsAvatar and owner.client.onSetAddSkillCd(self.skillId, float(self.getCD(owner)), float(self.tNextCast),
                                                        False)

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
    def getMaxTargetNum(skillId):
        return SkillBase.getSkillData(skillId).get('maxTargetNum', 0)

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
    def getScopeParam(skillId):
        scopeParam = SkillBase.getSkillData(skillId).get('scopeParam', '')
        if not scopeParam:
            return ()
        else:
            scopeParam = eval(scopeParam) if isinstance(scopeParam, (str, bytes)) else scopeParam
            if type(scopeParam) not in (list, tuple):
                scopeParam = (scopeParam,)
            return scopeParam

    @staticmethod
    @functools.lru_cache(1024)
    def getCostMp(skillId, factor):
        return factor * float(SkillBase.getSkillData(skillId).get('consumeMp') or 0)

    @staticmethod
    @functools.lru_cache(1024)
    def getMpPerSec(skillId):
        return SkillBase.getSkillData(skillId).get('mpPerSec')

    @staticmethod
    @functools.lru_cache(1024)
    def getRange(skillId):
        return float(SkillBase.getSkillData(skillId).get('range') or 0)

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

    def getServerRange(self):
        # 为了解决客户端打到，服务端判断出了范围加个延迟的范围值，只给客户端算的锁定技能加
        if self.needReleaseTarget():
            return self.getRange(self.skillId) + 1
        return self.getRange(self.skillId)

    def getServerRangeWithTarget(self, target):
        targetRadius = 0
        if target.IsMonster:
            targetRadius = target.getConfigData().get('attackDistanceCompensation')
        if self.needReleaseTarget():
            return self.getRange(self.skillId) + targetRadius + 1
        return self.getRange(self.skillId) + targetRadius

    def inRange(self, src, target):
        pos1 = src.position
        pos2 = target.position
        if not utils.checkCombatRangeY(src, target):
            return False
        if self.getRange(self.skillId) <= 0:
            return True
        # 为了解决客户端打到，服务端判断出了范围加个延迟的范围值
        if sMath.distance2DToCompareFrom3DPosition(pos1, pos2) < math.pow(self.getServerRangeWithTarget(target), 2):
            return True

        return False

    def needReleaseTarget(self):
        targetType = self.getTarget(self.skillId)
        if not targetType or targetType == 'None':
            return False
        return True

    def isMultiCastSkill(self):
        return self.hasTag(gameconst.SkillTag.Casting) and self.getMaxTargetNum(self.skillId) > 1

    def needCharge(self):
        return self.getChargetimeMin() > 0 and self.getChargetimeMax(self.skillId) > 0

    def needCast(self):
        return self.getCastingtimeMax(self.skillId) > 0

    @staticmethod
    @functools.lru_cache(1024)
    def getEffectTarget(skillId):
        DEBUG_MSG("getEffectTarget", skillId)
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
        return gameconst.SkillTag.DodgeSkill in tags or gameconst.SkillTag.Lunge in tags or gameconst.SkillTag.Chongfeng in tags or gameconst.SkillTag.TeleportSkill in tags or gameconst.SkillTag.BlinkToTarget in tags or gameconst.SkillTag.EndTimebackSkill in tags

    def clearCD(self, owner):
        oldInCD = self.inCDTime()
        self.tNextCast = 0.0

        if oldInCD and owner.IsAvatar:
            owner.client.onSetAddSkillCd(self.skillId, float(self.getCD(owner)), float(self.tNextCast), False)

    def getOneNearest(self, pos, targetsList):
        if not targetsList or len(targetsList) == 0:
            return
        dis = 10000
        minIndex = -1
        for idx, target in enumerate(targetsList):
            curDis = sMath.distance2DToCompareFrom3DPosition(pos, target.position)
            if curDis < dis:
                minIndex = idx
                dis = curDis
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
                if utils.checkTargetType(self.getEffectTarget(self.skillId), caster, player) and self.inRange(
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
                    if utils.checkTargetType(self.getEffectTarget(self.skillId), caster, player) and self.inRange(
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

    def isInAttackArea(self, target, center, radius):
        if target.IsMonster:
            radius += target.getConfigData().get('attackDistanceCompensation', 0)

        dis = sMath.distance2DToCompareFrom3DPosition(target.position, center)
        return dis <= radius * radius

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

        if not targetRadius:
            direction.normalise()
            h = Math.Vector2(length / 2, width / 2)
            dstPosition = vCenter + direction * (length / 2)
            c = Math.Vector2(dstPosition.x, dstPosition.z)
            c = sMath.getRotatePos((c.x, c.y), (direction[0], direction[2]))
            c = Math.Vector2(c[0], c[1])
            p = Math.Vector2(target.position.x, target.position.z)
            p = sMath.getRotatePos((p.x, p.y), (direction[0], direction[2]))
            p = Math.Vector2(p[0], p[1])
            return sMath.isAabbDiskIntersect(c, h, p)
        else:
            dirMagnitude = math.sqrt(direction.x * direction.x + direction.z * direction.z)
            if dirMagnitude == 0:
                return False

            unitDirX = direction.x / dirMagnitude
            unitDirZ = direction.z / dirMagnitude

            targetVec = target.position - vCenter

            dotProduct = targetVec.x * unitDirX + targetVec.z * unitDirZ

            projPointX = vCenter.x + unitDirX * dotProduct
            projPointZ = vCenter.z + unitDirZ * dotProduct

            perpDistance = math.sqrt(max(0, (target.position.x - projPointX)**2 + (target.position.z - projPointZ)**2))

            closestX = dotProduct
            if closestX < 0:
                closestX = 0
            elif closestX > length:
                closestX = length

            closestZ = perpDistance
            if closestZ > width/2:
                closestZ = width/2

            if 0 <= dotProduct <= length:
                distance = max(0, perpDistance - width/2)
            else:
                endX = 0 if dotProduct < 0 else length
                endPointX = vCenter.x + unitDirX * endX
                endPointZ = vCenter.z + unitDirZ * endX

                dx = target.position.x - endPointX
                dz = target.position.z - endPointZ
                distance = math.sqrt(dx*dx + dz*dz) - width/2
                distance = max(0, distance)

            return distance <= targetRadius

    def isInAttackRectAngle(self, target, vCenter, direction, length, width, radius):
        return self.isInAttackArea(target, vCenter, radius) and self.isInAttackLine(target, vCenter, direction, length,
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
            position = caster.position + direction * percent * self.getRange(self.skillId)
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
                self.getRange(self.skillId),
                direction
            )

        elif scopeType == gameconst.SkillScope.MI_CENTER_SELF:
            arr = list(direction)

        elif scopeType == gameconst.SkillScope.HALF_MI:
            arr = list(direction)

        elif scopeType == gameconst.SkillScope.MULTI_SECTOR:
            arr = list(direction)

        elif scopeType == gameconst.SkillScope.COLOSSUS_CIRCLE or \
                scopeType == gameconst.SkillScope.COLOSSUS_RECTANGLE:
            return self.getPlunderLingzhuSkillArr(caster, target, caster.spaceNo)

        return arr

    def getSkillDesPosition(self, caster, target, skillArgs):
        if self.hasTag(gameconst.SkillTag.TeleportSkill):
            dis = self.getRange(self.skillId)
            dstPosition = sMath.getForwardPos(caster.position, caster.direction[2], dis)
            skillPos, skillDir = self.getSkillPosAndDir(caster, target, skillArgs)
            # scope其他时取技能朝向，scope为6时取双摇杆选的坐标
            if self.getScope(self.skillId) == gameconst.SkillScope.USER_DEFINED_CIRCLE:
                dstPosition = skillPos
            else:
                dstPosition = caster.position + skillDir * dis

            dstPosition = utils.getSurfacePos(caster.spaceID, dstPosition)
            realDstPos = utils.getRaycastPos(caster.spaceID, caster.position, dstPosition)
            desPosition = list(realDstPos)

        elif self.hasTag(gameconst.SkillTag.BlinkToTarget):
            offset = 2.0
            yaw = sMath.getYawFromPoints(caster.position, target.position)
            targetPos = sMath.getForwardPos(target.position, yaw, offset)

            targetPos = utils.getSurfacePos(caster.spaceID, targetPos)
            realDstPos = utils.getRaycastPos(caster.spaceID, caster.position, targetPos)
            desPosition = list(realDstPos)
        elif self.hasTag(gameconst.SkillTag.Chongfeng):
            dis = 2.0
            if target and hasattr(target, 'creepBaseId'):
                dis = utils.getCollisionDistance(target.creepBaseId, dis)

            if sMath.inRange2D(dis, caster.position, target.position):
                dstPosition = caster.position
            else:
                offset = dis
                yaw = sMath.getYawFromPoints(caster.position, target.position)
                dstPosition = sMath.getForwardPos(target.position, yaw, offset)

            dstPosition = utils.getSurfacePos(caster.spaceID, dstPosition)
            dstPosition = utils.getRaycastPos(caster.spaceID, caster.position, dstPosition)
            desPosition = list(dstPosition)
        elif self.hasTag(gameconst.SkillTag.Lunge):
            skillPos, skillDir = self.getSkillPosAndDir(caster, target, skillArgs)
            skillRange = self.getRange(self.skillId)
            # 根据target的碰撞距离处理
            if target and hasattr(target, 'creepBaseId'):
                collisionDis = utils.getCollisionDistance(target.creepBaseId, 2.0)
                dis = sMath.distance2D(caster.position, target.position)
                # 距离超过碰撞距离，需要减去碰撞距离。否则原地不动
                dis = dis - collisionDis if dis > collisionDis else 0
                if skillRange > dis:
                    skillRange = dis
            
            dstPosition = caster.position + skillDir * skillRange
            dstPosition = utils.getSurfacePos(caster.spaceID, dstPosition)
            realDstPos = utils.getRaycastPos(caster.spaceID, caster.position, dstPosition)
            desPosition = list(realDstPos)
        elif self.hasTag(gameconst.SkillTag.DodgeSkill):
            skillPos, skillDir = self.getSkillPosAndDir(caster, target, skillArgs)
            dstPosition = caster.position + skillDir * self.getRange(self.skillId)
            dstPosition = utils.getSurfacePos(caster.spaceID, dstPosition)
            realDstPos = utils.getRaycastPos(caster.spaceID, caster.position, dstPosition)
            desPosition = list(realDstPos)

        return desPosition

    def getPlunderLingzhuSkillArr(self, owner, target, spaceNo):
        arr = []
        pos = []
        dire = []
        ent = None

        lingzhuPosCustonKey = SSD.datas[self.skillId]['lingzhuSkillPos_customID']
        dunNo = formula.getMapId(spaceNo)
        dataList = list(utils.getDunStructureModuleData(dunNo)[lingzhuPosCustonKey].values())
        if dataList:
            data = dataList[0]
            pos = (data['PosX'], data['PosY'], data['PosZ'])
            dire = sMath.getDirFromYaw(data['Dir'] / 180 * math.pi)

        targetType = self.getTarget(self.skillId)
        if targetType != 'None':
            targetIds = owner.getTargetIdsByTargetType(targetType)
            if targetIds:
                targetId = random.choice(targetIds)
                ent = KBEngine.entities.get(targetId)
        else:
            ent = target

        scopeType = self.getScope(self.skillId)
        if scopeType == gameconst.SkillScope.COLOSSUS_CIRCLE:
            if ent:
                arr.extend(ent.position)
            else:
                arr.extend(pos)

            arr.extend(dire)

        elif scopeType == gameconst.SkillScope.COLOSSUS_RECTANGLE:
            if ent:
                dire = sMath.vector3WithoutY(ent.position - pos)
                arr.extend(pos)
                arr.extend(list(dire))

        return arr

    def getEffectTargets(self, caster, targetId, arr, forceTarget=False, positionSkillArgs=None):
        if not caster:
            return []
        if self.getTempData('isChannelingEmpty', False):
            return []

        if self.targetIds:
            invalidIds = []
            for i, tid in enumerate(self.targetIds):
                target = KBEngine.entities.get(tid)
                if not target:
                    invalidIds.append(i)
                    continue

                if not utils.checkTargetType(
                        self.getEffectTarget(self.skillId), 
                        caster, 
                        target):

                    invalidIds.append(i)

            for i in reversed(invalidIds):
                self.targetIds.pop(i)

            return self.targetIds

        return self._internalGetEffectTargets(caster, targetId, arr, forceTarget, positionSkillArgs)

    def _internalGetEffectTargets(self, caster, targetId, arr, forceTarget, positionSkillArgs):
        # 客户端自动寻路攻击目标调用过来的时候，可能最新的position还没报告给服务端，所以这里按技能距离可能
        # 拿不到客户端选中的entity，这里加点offset偏差做容错

        target = KBEngine.entities.get(targetId)

        skillPos, skillDir = self.getSkillPosAndDir(caster, target, arr)
        scopes = self.getScope(self.skillId)
        scopeParams = self.getScopeParam(self.skillId)

        if not scopes or scopes == gameconst.SkillScope.TARGET_AUTO:
            if self.hasTag(gameconst.SkillTag.SingleHeal) and hasattr(caster,
                                                                      'commonFlagCell') and caster.getCommonFlagCell(
                gameconst.CommonFlagCellType.IsHealHPLow) and (
                    not target or targetId == caster.id or not utils.checkTargetType(self.getEffectTarget(self.skillId),
                                                                                     caster, target)):
                targetNearest = self.getOneHPLowest(caster)
            else:
                if target and (caster.isVisible(target) or caster.hasBuffTag(
                        gameconst.BuffTag.SeeHiddenEnt)) and utils.checkTargetType(self.getEffectTarget(self.skillId),
                                                                                   caster, target):
                    if self.inRange(caster, target):
                        return [target.id]
                    else:
                        return []

                if self.getEffectTarget(self.skillId) == 'Friend':
                    return [caster.id]

                if not targetId:
                    return []

                if self.getTempData('beginSkillPosition'):
                    targetsList = caster.getTargets(caster, targetId, self.getEffectTarget(self.skillId),
                                                    self.getServerRange(), forceTarget,
                                                    self.getTempData('beginSkillPosition'))
                    targetNearest = self.getOneNearest(self.getTempData('beginSkillPosition'), targetsList)
                else:
                    targetsList = caster.getTargets(caster, targetId, self.getEffectTarget(self.skillId),
                                                    self.getServerRange(), forceTarget)
                    targetNearest = self.getOneNearest(caster.position, targetsList)
            if targetNearest and (caster.isVisible(targetNearest) or caster.hasBuffTag(
                    gameconst.BuffTag.SeeHiddenEnt)) and self.inRange(caster, targetNearest):
                return [targetNearest.id]
            else:
                return []

        elif scopes == gameconst.SkillScope.CIRCLE_CENTER_SELF:
            if len(scopeParams) < 1:
                caster.combatDebugMsg("GetEffectTargets skill scopeParams error")
            center = caster.position
            radius = float(scopeParams[0])

            checkScopeFun = lambda target: self.isInAttackArea(target, center, radius)
            return caster.getTargetsWithNum(caster, targetId, self.getEffectTarget(self.skillId), self.getServerRange(),
                                            self.getMaxTargetNum(self.skillId), checkScopeFun)

        elif scopes == gameconst.SkillScope.CIRCLE_CENTER_TARGET:
            if len(scopeParams) < 1:
                caster.combatDebugMsg("GetEffectTargets skill scopeParams error")
            if not target:
                return []

            radius = float(scopeParams[0])

            checkScopeFun = lambda target: self.isInAttackArea(target, skillPos, radius)
            return caster.getTargetsWithNum(target, targetId, self.getEffectTarget(self.skillId),
                                            self.getRange(self.skillId) + 0.8,
                                            self.getMaxTargetNum(self.skillId), checkScopeFun)

        elif scopes == gameconst.SkillScope.SELF_TO_TARGET_RECTANGLE:
            if len(scopeParams) < 2:
                caster.combatDebugMsg("GetEffectTargets skill scopeParams error")
            length = float(scopeParams[0])
            width = float(scopeParams[1])

            checkScopeFun = lambda target: self.isInAttackLine(target, caster.position, skillDir, length, width)
            return caster.getTargetsWithNum(caster, targetId, self.getEffectTarget(self.skillId), self.getServerRange(),
                                            self.getMaxTargetNum(self.skillId), checkScopeFun)

        elif scopes == gameconst.SkillScope.USER_DEFINED_SECTOR:
            if len(scopeParams) < 1:
                caster.combatDebugMsg("GetEffectTargets skill scopeParams error")
            skillSectorAngle = float(scopeParams[0])

            checkScopeFun = lambda target: self.isInAttackSector(target, caster.position, skillDir,
                                                                 self.getServerRange(), skillSectorAngle * 2)
            return caster.getTargetsWithNum(caster, targetId, self.getEffectTarget(self.skillId), self.getServerRange(),
                                            self.getMaxTargetNum(self.skillId), checkScopeFun)

        elif scopes in (gameconst.SkillScope.USER_DEFINED_RECTANGLE, gameconst.SkillScope.CURRENT_DIRECTION_RECTANGLE):
            if len(scopeParams) < 1:
                caster.combatDebugMsg("GetEffectTargets skill scopeParams error")
            length = self.getServerRange() + self.getProtectRange(self.skillId)
            width = float(scopeParams[1])

            if positionSkillArgs:
                beginSkillPosition = self.getTempData('beginSkillPosition') if self.getTempData(
                    'beginSkillPosition') else caster.position
                distance = sMath.distance2D(beginSkillPosition, positionSkillArgs)
                range = min(self.getRange(self.skillId), distance + self.getProtectRange(self.skillId))
            else:
                range = self.getServerRange() + self.getProtectRange(self.skillId)
            if self.getTempData('beginSkillPosition'):
                checkScopeFun = lambda target: self.isInAttackRectAngle(target, self.getTempData('beginSkillPosition'),
                                                                        skillDir, length, width, range)
                return caster.getTargetsWithNum(caster, targetId, self.getEffectTarget(self.skillId), range,
                                                self.getMaxTargetNum(self.skillId), checkScopeFun)
            else:
                checkScopeFun = lambda target: self.isInAttackRectAngle(target, caster.position, skillDir, length,
                                                                        width, range)
                return caster.getTargetsWithNum(caster, targetId, self.getEffectTarget(self.skillId), range,
                                                self.getMaxTargetNum(self.skillId), checkScopeFun)

        elif scopes == gameconst.SkillScope.USER_DEFINED_CIRCLE:
            if len(scopeParams) < 1:
                caster.combatDebugMsg("GetEffectTargets skill scopeParams error")
            direction = Math.Vector3(arr[0], arr[1], arr[2])
            percent = arr[3]
            beginSkillPosition = self.getTempData('beginSkillPosition') if self.getTempData('beginSkillPosition') else caster.position
            center = beginSkillPosition + direction * percent * self.getRange(self.skillId)
            radius = float(scopeParams[0])

            checkScopeFun = lambda target: self.isInAttackArea(target, center, radius)
            return caster.getTargetsWithNum(target, targetId, self.getEffectTarget(self.skillId),
                                            self.getServerRange() + radius,
                                            self.getMaxTargetNum(self.skillId), checkScopeFun)

        elif scopes == gameconst.SkillScope.MI_CENTER_SELF:
            length = float(scopeParams[0])
            width = float(scopeParams[1])

            checkScopeFun = lambda target: self.isInAttackMi(target, caster.position, skillDir, length, width)
            return caster.getTargetsWithNum(target, targetId, self.getEffectTarget(self.skillId), self.getServerRange(),
                                            self.getMaxTargetNum(self.skillId), checkScopeFun)

        elif scopes == gameconst.SkillScope.HALF_MI:
            length = float(scopeParams[0])
            width = float(scopeParams[1])

            checkScopeFun = lambda target: self.isInAttackHalfMi(target, caster.position, skillDir, length, width)
            return caster.getTargetsWithNum(target, targetId, self.getEffectTarget(self.skillId), self.getServerRange(),
                                            self.getMaxTargetNum(self.skillId), checkScopeFun)

        elif scopes == gameconst.SkillScope.TARGET_LINKED:
            dist, linkProp, count = float(scopeParams[0]), float(scopeParams[1]), float(scopeParams[2])
            linkedTargets = self.getLinkedTargets(caster, target, dist, linkProp, count)
            return linkedTargets

        elif scopes == gameconst.SkillScope.COLOSSUS_CIRCLE:
            center = skillPos
            radius = float(scopeParams[0])

            checkScopeFun = lambda target: self.isInAttackArea(target, center, radius)
            return caster.getTargetsWithNum(target, targetId, self.getEffectTarget(self.skillId),
                                            self.getServerRange() + radius,
                                            self.getMaxTargetNum(self.skillId), checkScopeFun)

        elif scopes == gameconst.SkillScope.COLOSSUS_RECTANGLE:
            if len(scopeParams) < 1:
                caster.combatDebugMsg("GetEffectTargets skill scopeParams error")
            length = self.getServerRange()
            width = float(scopeParams[1])

            if skillPos:
                checkScopeFun = lambda target: self.isInAttackRectAngle(target, skillPos, skillDir, length, width,
                                                                        self.getServerRange())
                return caster.getTargetsWithNum(caster, targetId, self.getEffectTarget(self.skillId),
                                                self.getServerRange(),
                                                self.getMaxTargetNum(self.skillId), checkScopeFun)
            else:
                return []
        elif scopes == gameconst.SkillScope.ANNULAR_CENTER_SELF:
            minRadius = float(scopeParams[0])
            maxRadius = float(scopeParams[1])
            center = caster.position
            checkScopeFun = lambda target: self.isInAttackAnnularArea(target, center, minRadius, maxRadius)
            return caster.getTargetsWithNum(target, targetId, self.getEffectTarget(self.skillId), self.getServerRange(),
                                            self.getMaxTargetNum(self.skillId), checkScopeFun)
        elif scopes == gameconst.SkillScope.MULTI_SECTOR:
            if len(scopeParams) < 3:
                caster.combatDebugMsg("GetEffectTargets MULTI_SECTOR skill scopeParams error")
                
            sectorNum = int(scopeParams[0])
            offsetAngles = scopeParams[1]
            sectorAngle = float(scopeParams[2])
            
            if not isinstance(offsetAngles, (list, tuple)):
                offsetAngles = []
                
            if len(offsetAngles) < sectorNum:
                caster.combatDebugMsg("GetEffectTargets MULTI_SECTOR not enough offsetAngles")
                
            checkScopeFun = lambda target: self.isInMultiSectorAttack(target, caster.position, skillDir, 
                                                self.getServerRange(), sectorAngle * 2, sectorNum, offsetAngles)
            return caster.getTargetsWithNum(caster, targetId, self.getEffectTarget(self.skillId), self.getServerRange(),
                                            self.getMaxTargetNum(self.skillId), checkScopeFun)

        return []

    def _checkUseSkillOwner(self, owner, targetId, ignoreReasons=0):
        code = gameconst.UseSkillCheck.IN_CD
        if not code & ignoreReasons and self.inCDTime():
            owner.combatDebugMsg('skill %d cannot use: inCDTime' % (self.getSkillId()), self.tNextCast, time.time())
            return code

        code = gameconst.UseSkillCheck.LACK_OF_MP
        if not code & ignoreReasons and owner.IsAvatar and owner.mp < self.getCostMp(self.skillId, owner.mpCostRatio):
            owner.combatDebugMsg('fail to use skill: lack of mp', self.skillId)
            return code

        code = gameconst.UseSkillCheck.INVALID_OWNER
        if not code & ignoreReasons and not owner:
            ERROR_MSG('skill %s caster error' % (self.getSkillId()))
            return code

        code = gameconst.UseSkillCheck.SELF_DIE
        if not code & ignoreReasons and owner.isDie():
            return code

        if utils.hasSkillTag(self.skillId, gameconst.SkillTag.UltraSkill):
            code = gameconst.UseSkillCheck.ULTRA_SKILL_POWER_NOT_ENOUGH
            if not code & ignoreReasons and not owner.isUltraSkillPowerMax():
                owner.combatDebugMsg('fail to use ultra skill: power not enough', self.getSkillId())
                return code

        code = gameconst.UseSkillCheck.STATE_CONFLICT
        if not code & ignoreReasons:
            extraEventId = self.getSkillEvent(self.skillId)
            if extraEventId:
                if not owner.checkConflictState(extraEventId):
                    owner.combatDebugMsg('fail to use skill2: curentState=useSkill', self.getSkillId(), extraEventId)
                    return code
            else:
                if not owner.checkConflictState(CCD.datas.useSkill):
                    owner.combatDebugMsg('fail to use skill2: curentState=useSkill', self.getSkillId(), extraEventId)
                    return code

                if utils.hasSkillTag(self.skillId, gameconst.SkillTag.GeneralSkill) and not owner.checkConflictState(
                        CCD.datas.useGeneralSkill, False):
                    return code

                skillState = self.getSkillState()
                eventId = CSD.datas[skillState].get('event')
                if eventId and not owner.checkConflictState(eventId):
                    owner.combatDebugMsg('fail to use skill3: curentState=useSkill', self.getSkillId(), eventId)
                    return code

        return gameconst.UseSkillCheck.CHEKC_OK

    def _checkUseSkillTarget(self, owner, targetId, ignoreReasons=0):
        DEBUG_MSG('_checkUseSkillTarget', self.skillId, targetId, self.needReleaseTarget())
        if self.hasTag(gameconst.SkillTag.SingleHeal):
            target = KBEngine.entities.get(targetId)
            if not target:
                return gameconst.UseSkillCheck.CHEKC_OK
            if not utils.checkTargetType(self.getEffectTarget(self.skillId), owner, target):
                return gameconst.UseSkillCheck.CHEKC_OK
            if not self.inRange(owner, target):
                if self.hasTag(gameconst.SkillTag.Channel) or self.hasTag(gameconst.SkillTag.Casting):
                    owner.showMsg(CONST.datas['targetIsOutOfRange_butCasted']['value'], [])
                else:
                    owner.showMsg(CONST.datas['targetIsOutOfRange']['value'], [])
                    return gameconst.UseSkillCheck.SINGLE_HEAL_OUT_OF_RANGE
        if self.needReleaseTarget():
            target = KBEngine.entities.get(targetId)
            if not target:
                return gameconst.UseSkillCheck.CHEKC_OK

            code = gameconst.UseSkillCheck.INVALID_TARGET
            if not code & ignoreReasons and not utils.checkTargetType(self.getTarget(self.skillId), owner, target):
                owner.combatDebugMsg('skill cannot use: checkTargetType:', self.skillId, self.getTarget(self.skillId),
                                     target)
                return code

            code = gameconst.UseSkillCheck.INVISIBLE_TARGET
            if not code & ignoreReasons and not owner.isVisible(target) and not owner.hasBuffTag(
                    gameconst.BuffTag.SeeHiddenEnt):
                owner.combatDebugMsg('skill cannot use: target is invisible:', self.skillId,
                                     self.getTarget(self.skillId), target.id)
                return code

            code = gameconst.UseSkillCheck.CROSS_SPACE
            if not code & ignoreReasons and target.spaceNo != owner.spaceNo:
                owner.combatDebugMsg('fail to use skill', target.spaceNo, owner.spaceNo)
                return code

            code = gameconst.UseSkillCheck.OUT_OF_RANGE
            if not code & ignoreReasons and not self.inRange(owner, target):
                owner.combatDebugMsg('skill cannot use: needReleaseTarget and not inRange', self.getSkillId(),
                                     owner.position, target.position, sMath.distance2D(owner.position, target.position))
                return code

        return gameconst.UseSkillCheck.CHEKC_OK

    def checkUseSkill(self, owner, targetId, ignoreReasons=0):
        code = self._checkUseSkillOwner(owner, targetId, ignoreReasons)
        if code != gameconst.UseSkillCheck.CHEKC_OK:
            return code

        return self._checkUseSkillTarget(owner, targetId, ignoreReasons)

    # 延迟结算时间
    def getSkillResultDelay(self, owner, targetId, skillArgs, compensateTime):
        delayTime = self.getFxDelay(self.skillId) - (compensateTime / 1000.0)
        if self.hasTag(gameconst.SkillTag.Channel):
            return sMath.limit(delayTime, 0.0, 9999.0)
        if self.getBulletFx(self.skillId):
            timeEx = self.calBulletTime(owner, targetId)

            delayTime += timeEx
        delayTime = sMath.limit(delayTime, 0.0, 9999.0)
        return delayTime

    def getSkillState(self):
        raise NotImplementedError()

    def enterCDTime(self, owner, delayCd=0):
        if delayCd:
            self.tNextCast = time.time() + delayCd
        else:   
            self.tNextCast = time.time() + self.getCD(owner) - 0.1

    def _cancelTempTimer(self, owner, timerName, timerTag=''):
        tid = self.popTempData(timerName, 0)
        if tid:
            owner._cancelCallback(tid, timerTag)
            return True
        return False

    def refreshSkillCD(self, owner, duration):
        owner.combatDebugMsg('refreshSkillCD', owner.id, self.skillId, duration)
        self._cancelTempTimer(owner, 'restoreCDTimer', gametimer.TIMER_TAG_RESTORE_CD)

        if self.hasTempData('changeToSkill'):
            owner.IsAvatar and owner.client.onUseStageSkill(self.skillId, 1, time.time())

        if not self.hasTempData('tNextCast'):
            self.setTempData('tNextCast', self.tNextCast)
        self.tNextCast = time.time() - 0.1
        owner.client.onSetAddSkillCd(self.skillId, float(self.getCD(owner)), float(self.tNextCast), True)
        tid = owner._callback(duration, '_onSkillCallback', (self, 'invalidateRefreshCD', ()),
                              gametimer.TIMER_TAG_RESTORE_CD)
        self.setTempData('restoreCDTimer', tid)

    def invalidateRefreshCD(self, owner, doReset=True, notifyClient=True):
        owner.combatDebugMsg('invalidateRefreshCD', self.skillId, self.tempData)
        self.tNextCast = self.getTempData('tNextCast', time.time())
        self.popTempData('restoreCDTimer')

        notifyClient and owner.client.onSetAddSkillCd(self.skillId, float(self.getCD(owner)), float(self.tNextCast),
                                                      False)
        doReset and self.resetSkill(owner, gameconst.ResetSkillReason.TimeRefreshDone)

    def beginUseSkill(self, owner, targetId, skillArgs, compensateTime, doSetState=True, enterCD=True, parentCtx=None):
        self.isInSkill = True
        self.setTempData('skillArgs', skillArgs)
        owner.combatDebugMsg('beginUseSkill', targetId, self.skillId, skillArgs)
        target = KBEngine.entities.get(targetId)
        startAction = self.getStartAction(self.skillId)
        startActionFail = False
        startActionResult = gameconst.StartActionResult.Success

        if self.hasTempData('restoreCDTimer'):
            self._cancelTempTimer(owner, 'restoreCDTimer', gametimer.TIMER_TAG_RESTORE_CD)
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

        effectedEntIds = self.getEffectTargets(owner, targetId, realSkillArgs, positionSkillArgs=positionSkillArgs)
        skillResult = SkillDamges(owner.id)
        actionCtx = actionContext.UseSkillCtx(owner.id, self.skillId, skillArgs, targetId, effectedEntIds, self,
                                              skillResult, parentCtx=parentCtx)

        actionCtx.actionProgress = gameconst.ActionProgressType.startActionDone
        if startAction:
            # start action先不给传effectedEntIds，因为可能还没开始结算
            # start action里加的buff什么的不能依赖在技能action里解除,技能可能在延迟后不能执行action
            # 例如旋风斩开始加的无敌需要在end action去删除
            ctxFunc = lambda r: actionCtx
            if owner.doCombatActions(startAction, owner, target, owner.id, ctxFunc) is False:
                startActionFail = True
                startActionResult = gameconst.StartActionResult.Fail

        if startActionFail:
            owner.combatDebugMsg('do startAction fail:', owner.id, targetId, self.skillId, owner.position)
            self.useSkillDone(owner, targetId, skillArgs, isSucc=False, startActionFail=startActionFail)
            return startActionResult, None, None
        elif utils.hasSkillTag(self.skillId, gameconst.SkillTag.UltraSkill):
            owner.ultraSkillPower = 0

        if (not owner.IsAvatar or owner.gmModeCell != gameconst.GmMode.GM_NO_SKILLCD) and enterCD and not self.hasTag(
                gameconst.SkillTag.Channel):
            self.enterCDTime(owner)
            owner.client.onSetAddSkillCd(self.skillId, float(self.getCD(owner)), float(self.tNextCast), False)

        owner.IsAvatar and owner.modifyMP(-self.getCostMp(self.skillId, owner.mpCostRatio))

        # if self.needReleaseTarget():
        #   target and owner.sendCombatMsg(MBD.datas.releaseSkillToTarget,
        #                                    [target.name, self.getSkillName(self.skillId)])
        # else:
        #   owner.sendCombatMsg(MBD.datas.releaseSkill, [self.getSkillName(self.skillId)])

        if self.hasTempData('changedFromSkill'):
            skillVal = owner.getSkill(self.getTempData('changedFromSkill'))
            skillVal.onChangedSkillBegin(owner)

        # startAction里可能会攻击别人然后被反噬死。。
        if owner.isDie():
            owner.combatDebugMsg('beginUseSkill die after startAction:', owner.id, targetId, self.skillId,
                                 owner.position)
            self.useSkillDone(owner, targetId, skillArgs, isSucc=False, startActionFail=startActionFail)
            return gameconst.StartActionResult.Fail, None, None

        return startActionResult, actionCtx, effectedEntIds

    # 支持callAfterDelay配出来的分阶段action
    def setupMulAttackAction(self, owner, context, delay, firstStageCalcDelay, duration):
        context.actionStage += 1
        self.setTempData('duration', duration)
        if delay <= 0:
            owner.doSkillAction(self.skillId, context, firstStageCalcDelay, True,
                                gameconst.UseSkillCheck.MUL_ATTACK_CHECK_IGNORES, duration)
        else:
            tid = owner._callback(delay, 'doSkillAction', (self.skillId, context, firstStageCalcDelay, True,
                                                           gameconst.UseSkillCheck.MUL_ATTACK_CHECK_IGNORES, duration),
                                  gametimer.TIMER_TAG_DO_SKILL_ACTION)

            self._cancelTempTimer(owner, 'mulAttackActionTimer', gametimer.TIMER_TAG_DO_SKILL_ACTION)
            self.setTempData('mulAttackActionTimer', tid)

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
            gameengine.reportCritical('applySkillEffect error:', owner.id, self.skillId, targetId, str(e))

        self.targetIds = []
        owner.combatDebugMsg('applySkillEffect', owner.id, targetId, skillArgs, effectedEntIds, actResult)
        return actResult

    def onSkillActionFinished(self, owner, targetId, skillArgs, context, calcDelay, actionDuration, doRemoveState=True):
        # 技能分为若干个阶段：1.客户端请求施法 2.计算子弹飞行，挥刀等延迟结算 3.结算技能数值
        # 4.结算完等整个技能时间结束(等待客户端收刀等后摇动作)

        # 引导技能在引导结束后再执行skillDone，其他技能结算完就可以skillDone了
        if not self.isInSkill:
            return
        if not self.hasTag(
                gameconst.SkillTag.Channel) and context.actionProgress == gameconst.ActionProgressType.actionDone:
            remainTime = self.getSkillTime(self.skillId) - calcDelay - actionDuration
            if remainTime <= 0:
                self.useSkillDone(owner, targetId, skillArgs, doRemoveState=doRemoveState)
            else:
                tid = owner._callback(remainTime, '_onSkillCallback',
                                      (self, 'useSkillDone', (targetId, skillArgs, True, False, doRemoveState)),
                                      gametimer.TIMER_TAG_SKILL_DONE)

                self._cancelTempTimer(owner, 'skillDoneTimer', gametimer.TIMER_TAG_SKILL_DONE)
                self.setTempData('skillDoneTimer', tid)

    def useSkillDone(self, owner, targetId, skillArgs, isSucc=True, startActionFail=False, doRemoveState=True):
        self._cancelTempTimer(owner, 'skillDoneTimer', gametimer.TIMER_TAG_SKILL_DONE)
        owner.combatDebugMsg('useSkillDone', self.skillId, isSucc)
        if doRemoveState:
            self._cancelTempTimer(owner, 'removeSkillStateTimer', gametimer.TIMER_TAG_REMOVE_SKILL_STATE)
            skillState = self.getSkillState()
            owner.removeState(skillState)

        if self.hasTempData('changedFromSkill'):
            fromSkillId = self.getTempData('changedFromSkill')
            owner.IsAvatar and owner.allClients.onUseStageSkill(fromSkillId, 0, time.time())

        if self.hasTempData('beginSkillPosition'):
            self.popTempData('beginSkillPosition')

        if self.hasTempData('skillArgs'):
            self.popTempData('skillArgs')

        if self.needResetOnSkillDone(owner):
            self.resetSkill(owner, gameconst.ResetSkillReason.SkillDone, doRemoveState)
        else:
            self.targetIds = []

        owner.useSkillFinish(self.skillId)
        owner.IsAICombatUnit and owner.aiController and owner.aiController.useSkillDone(self.skillId)

        target = KBEngine.entities.get(targetId)
        endAction = self.getSkillData(self.skillId).get('endSkillAction', None)
        # startAction释放成功了才执行endAction，目前只有位移技能的startAction有返回值可能返回失败
        if endAction and not startActionFail and isSucc:
            realSkillArgs = skillArgs
            if self.isChangePositionSkill(self.skillId):
                realSkillArgs = skillArgs[:-3]
            effectedEntIds = self.getEffectTargets(owner, targetId, realSkillArgs)
            actionCtx = actionContext.UseSkillCtx(owner.id, self.skillId, skillArgs, targetId, effectedEntIds, self,
                                                  None, isSucc=isSucc)
            endAction(owner, target, actionCtx)

    def getRealSkillVal(self, owner):
        if self.hasTempData('changeToSkill'):
            toSkillId = self.getTempData('changeToSkill')
            skillVal = owner.getSkillByCategory(toSkillId, self.getLevel(owner))
            skillVal.setTempData('changedFromSkill', self.skillId)
            return skillVal, True
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

    def changeToSkill(self, toSkillId):
        self.setTempData('changeToSkill', toSkillId)

    def onChangedSkillBegin(self, owner):
        if self.hasTempData('restoreCDTimer'):
            self._cancelTempTimer(owner, 'restoreCDTimer', gametimer.TIMER_TAG_RESTORE_CD)
            self.invalidateRefreshCD(owner, doReset=False, notifyClient=False)
        self.enterCDTime(owner)
        owner.client.onSetAddSkillCd(self.skillId, float(self.getCD(owner)), float(self.tNextCast), False)

    def setTempData(self, name, val):
        if self.tempData.get(name) and name.endswith('Timer'):
            gameengine.reportCritical('setTempData cover timer', name, val)

        self.tempData[name] = val

    def hasTempData(self, name):
        return name in self.tempData

    def getTempData(self, name, defalut=None):
        return self.tempData.get(name, defalut)

    def popTempData(self, name, default=None):
        return self.tempData.pop(name, default)

    def needResetOnSkillDone(self, owner):
        # 如果是限时刷新技能先不reset，等超时没使用或刷新的技能用完了再reset

        if self.hasTempData('restoreCDTimer'):
            return False
        return True

    def resetSkill(self, owner, reason=gameconst.ResetSkillReason.Default, doRemoveState=True):
        self.isInSkill = False
        owner.removeUseSkillRecord(self.skillId)
        skillState = self.getSkillState()
        if owner.hasState(skillState) and doRemoveState:
            owner.removeState(skillState)

        if self.hasTag(gameconst.SkillTag.Channel):
            owner.removeState(gameconst.State.UsingSkill)

        if self._cancelTempTimer(owner, 'restoreCDTimer', gametimer.TIMER_TAG_RESTORE_CD):
            self.invalidateRefreshCD(owner, doReset=False)

        self._cancelTempTimer(owner, 'delayCalcTimer', gametimer.TIMER_TAG_SKILL_DELAY_CALC)
        self._cancelTempTimer(owner, 'removeSkillStateTimer', gametimer.TIMER_TAG_REMOVE_SKILL_STATE)
        self._cancelTempTimer(owner, 'skillDoneTimer', gametimer.TIMER_TAG_SKILL_DONE)
        self._cancelTempTimer(owner, 'mulAttackActionTimer', gametimer.TIMER_TAG_DO_SKILL_ACTION)
        changeFromSkillId = 0 if not self.hasTempData('changedFromSkill') else self.getTempData('changedFromSkill')
        self.tempData.clear()

        self.targetIds = []

        if changeFromSkillId:
            skillVal = owner.getSkill(changeFromSkillId)
            if skillVal:
                skillVal.resetSkill(owner, reason, doRemoveState)

# 普通技能
class CommonSkillVal(SkillBase):
    def getSkillState(self):
        if self.hasTag(gameconst.SkillTag.Channel):
            if self.isMovingSkill(self.skillId):
                return gameconst.State.moveChannel

            return gameconst.State.Channeling
        elif self.hasTag(gameconst.SkillTag.GeneralSkill):
            return gameconst.State.GeneralAttack
        else:
            if self.isMovingSkill(self.skillId):
                return gameconst.State.moveSkill

            return gameconst.State.UsingSkill

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
        return self.skillId

    def beginUseSkill(self, owner, targetId, skillArgs, compensateTime, doSetState=True, enterCD=True, parentCtx=None):
        isSucc, actionCtx, effectTargetIds = super(CommonSkillVal, self).beginUseSkill(owner, targetId, skillArgs,
                                                                                       compensateTime,
                                                                                       doSetState, enterCD, parentCtx)
        if not isSucc:
            owner.client.onUseSkill(False, self.getNotifyClientSkillId(), targetId, [], [])
            return isSucc, None, effectTargetIds

        if self.isChangePositionSkill(self.skillId):
            if len(skillArgs) <= 3:
                target = KBEngine.entities.get(targetId)
                positionArgs = self.getSkillDesPosition(owner, target, skillArgs)
                skillArgs = skillArgs + positionArgs

        calcDelay = self.getSkillResultDelay(owner, targetId, skillArgs, compensateTime)
        # ChannelingSkillVal废除，因为吟唱后也需要可以引导，所以把引导合并到CommonSkillVal
        if self.hasTag(gameconst.SkillTag.Channel):
            owner.setTempMiscProp(gameconst.AvatarProps.currentChannelSkill, self)

            owner.combatDebugMsg('beginUseSkill channel sksill', self.skillId, targetId, skillArgs, compensateTime,
                                 calcDelay, owner.position)
            self.startChanneling(owner, targetId, skillArgs, calcDelay, actionCtx)
            owner.allClients.onUseSkill(isSucc, self.getNotifyClientSkillId(), targetId, skillArgs, effectTargetIds)
        else:
            owner.combatDebugMsg('beginUseSkill', self.skillId, targetId, skillArgs, compensateTime, calcDelay)
            skillStateDuration = self.getSkillTime(self.skillId)
            if not gameconst.SkillTag.GeneralSkill in self.getTag(self.skillId):
                if doSetState:
                    self._cancelTempTimer(owner, 'removeSkillStateTimer', gametimer.TIMER_TAG_REMOVE_SKILL_STATE)
                    self.setTempData(
                        'removeSkillStateTimer',
                        owner._callback(
                            skillStateDuration,
                            'removeSkillState',
                            (self,),
                            gametimer.TIMER_TAG_REMOVE_SKILL_STATE
                        )
                    )

            if actionCtx.actionProgress == gameconst.ActionProgressType.startActionDone:
                if calcDelay > 0:
                    if self.needReleaseTarget() and not (owner.IsMonster and self.isMultiCastSkill()):
                        self.targetIds = effectTargetIds

                    if self.hasTag(gameconst.SkillTag.EndTimebackSkill):
                        bkData = owner.getTempMiscProp(gameconst.AvatarProps.timebackSkillData)
                        if bkData:
                            skillArgs.extend(list(bkData.position))
                    self.setTempData(
                        'delayCalcTimer',
                        owner._callback(
                            calcDelay + 0.1, 
                            'delayCalcSkill', 
                            (
                                self, targetId,
                                skillArgs,
                                actionCtx,
                                calcDelay,
                                doSetState),
                            gametimer.TIMER_TAG_SKILL_DELAY_CALC))

                    owner.allClients.onUseSkill(True, self.getNotifyClientSkillId(), targetId, skillArgs,
                                                effectTargetIds)
                else:
                    # 保证onUseSkill在_doUseSkill前
                    self.targetIds = effectTargetIds
                    if self.hasTag(gameconst.SkillTag.EndTimebackSkill):
                        bkData = owner.getTempMiscProp(gameconst.AvatarProps.timebackSkillData)
                        if bkData:
                            skillArgs.extend(list(bkData.position))
                    if owner.isReal():
                        owner.allClients.onUseSkill(True, self.getNotifyClientSkillId(), targetId, skillArgs,
                                                    effectTargetIds)
                    owner._doUseSkill(self, targetId, skillArgs, actionCtx, calcDelay, doSetState)

        return isSucc, actionCtx, effectTargetIds

    def startChanneling(self, caster, targetID, arr, delayTime, actionCtx):
        self.channelCount = 0
        timerId = caster._callback(delayTime, 'channelingSkillTick',
                                   (self, targetID, arr, tuple(caster.position), actionCtx),
                                   gametimer.TIMER_TAG_CHANNELING_CALC)
        self.setTempData('channelingCalcTimer', timerId)
        self.setTempData('tChannelingStart', time.time() + delayTime)

    def calBulletTime(self, owner, targetId):
        target = KBEngine.entities.get(targetId)
        if target:
            bulletTimeScale = self.getBulletTimeScale(self.skillId)
            timeEx = self.getBulletFxTime(self.skillId) * (
                    1 - bulletTimeScale + bulletTimeScale * sMath.distance2D(owner.position,
                                                                             target.position) / self.getRange(
                self.skillId))
        else:
            timeEx = self.getBulletFxTime(self.skillId) if self.getBulletFxTime(self.skillId) else 0.5
        return timeEx

    def onChannelingEnd(self, owner, isFinished):
        owner._endChannelingSkill(isFinished)
        self.useSkillDone(owner, 0, self.popTempData('skillArgs', []))

    def onChannlingEffectEnd(self, owner):
        postSkillTime = self.getSkillTime(self.skillId)
        owner.removeState(self.getSkillState(), removeReason=gameconst.ChannelingBreak.NORMAR_END)
        self.enterCDTime(owner)
        owner.client.onSetAddSkillCd(self.skillId, float(self.getCD(owner)), float(self.tNextCast), False)
        if postSkillTime > 0:
            owner.setState(gameconst.State.UsingSkill)
            endTimer = owner._callback(postSkillTime, '_onSkillCallback', (self, 'onChannelingEnd', (True,)),
                                       gametimer.TIMER_TAG_ON_CHANNELING_END)
            self.setTempData('channelingEndTimer', endTimer)
        else:
            self.onChannelingEnd(owner, True)

    def resetSkill(self, owner, reason=gameconst.ResetSkillReason.Default, doRemoveState=True):
        if self.hasTag(gameconst.SkillTag.Channel):
            self._cancelTempTimer(owner, 'channelingCalcTimer', gametimer.TIMER_TAG_CHANNELING_CALC)
            self._cancelTempTimer(owner, 'channelingBulletTimer', gametimer.TIMER_TAG_CHANNELING_SKILL_EFFECT)
            self._cancelTempTimer(owner, 'channelingEndTimer', gametimer.TIMER_TAG_ON_CHANNELING_END)
            self.popTempData('isChannelingEmpty', False)
            self.channelCount = 0
        if self.hasTag(gameconst.SkillTag.Lunge) and owner.hasState(gameconst.State.Shifting):
            owner.endLunge(self, 0, [])
        super(CommonSkillVal, self).resetSkill(owner, reason, doRemoveState)

    def triggerRefreshSkillCD(self, owner):
        linkedSkillInfo = self.getSkillData(self.skillId).get('refreshSkillAndTime')
        WARNING_MSG('triggerRefreshSkillCD', owner.id, self.skillId, linkedSkillInfo)
        if not linkedSkillInfo:
            return

        linkedSkillId, duration = eval(linkedSkillInfo)
        owner.limitRefreshSkill(None, None, self.skillId, duration, linkedSkillId)


class ChongfengSkillVal(CommonSkillVal):
    def getSkillState(self):
        if self.isMovingSkill(self.skillId):
            return gameconst.State.moveSkill

        return gameconst.State.UsingSkill

    def beginUseSkill(self, owner, targetId, skillArgs, compensateTime, doSetState=True, enterCD=True, parentCtx=None):
        isSucc, actionCtx, effectTargetIds = super(ChongfengSkillVal, self).beginUseSkill(owner, targetId, skillArgs,
                                                                                          compensateTime,
                                                                                          doSetState, enterCD,
                                                                                          parentCtx)
        if not isSucc:
            owner.client.onUseSkill(False, self.skillId, targetId, [], [])

        return isSucc, actionCtx, effectTargetIds

    def resetSkill(self, owner, reason=gameconst.ResetSkillReason.Default, doRemoveState=True):
        if owner.hasState(gameconst.State.Shifting):
            owner.endChongfeng(self, 0, [])
        super(ChongfengSkillVal, self).resetSkill(owner, reason, doRemoveState)


# 刺客突进技能
class LungeSkillVal(CommonSkillVal):
    def getSkillState(self):
        if self.isMovingSkill(self.skillId):
            return gameconst.State.moveSkill

        return gameconst.State.UsingSkill

    def beginUseSkill(self, owner, targetId, skillArgs, compensateTime, doSetState=True, enterCD=True, parentCtx=None):
        isSucc, actionCtx, effectTargetIds = super(LungeSkillVal, self).beginUseSkill(owner, targetId, skillArgs,
                                                                                      compensateTime,
                                                                                      doSetState, enterCD, parentCtx)
        if not isSucc:
            owner.client.onUseSkill(False, self.skillId, targetId, [], [])

        return isSucc, actionCtx, effectTargetIds

    def resetSkill(self, owner, reason=gameconst.ResetSkillReason.Default, doRemoveState=True):
        if owner.hasState(gameconst.State.Shifting):
            owner.endLunge(self, 0, [])
        super(LungeSkillVal, self).resetSkill(owner, reason, doRemoveState)


# 闪避技能
class DodgeSkillVal(CommonSkillVal):
    def getSkillState(self):
        return gameconst.State.Dodging

    def beginUseSkill(self, owner, targetId, skillArgs, compensateTime, doSetState=True, enterCD=True, parentCtx=None):
        owner.resetUsingSkills(gameconst.ResetSkillReason.DodgeSkill)
        isSucc, actionCtx, effectTargetIds = super(DodgeSkillVal, self).beginUseSkill(owner, targetId, skillArgs,
                                                                                      compensateTime,
                                                                                      doSetState, enterCD, parentCtx)
        if not isSucc:
            owner.client.onUseSkill(False, self.skillId, targetId, [], [])

        return isSucc, None, effectTargetIds

    def resetSkill(self, owner, reason=gameconst.ResetSkillReason.Default, doRemoveState=True):
        if owner.hasState(gameconst.State.Dodging):
            owner.endDodge(self, 0, [])
        super(DodgeSkillVal, self).resetSkill(owner, reason, doRemoveState)

    def checkUseSkill(self, owner, targetId, ignoreReasons=0):
        return super(DodgeSkillVal, self).checkUseSkill(owner, targetId, ignoreReasons)


# 吟唱技能:多一个吟唱的普通技能
class CastingSkillVal(CommonSkillVal):
    def __init__(self, skillId, skillLv, tNextCast=0.0, cdDelta=0.0, parentSkill=0):
        super(CastingSkillVal, self).__init__(skillId, skillLv, tNextCast, cdDelta, parentSkill)
        self.castingStartTime = 0

    def onChangedFromSkill(self, fromSkillVal):
        super(CastingSkillVal, self).onChangedFromSkill(fromSkillVal)
        if fromSkillVal.hasTag(gameconst.SkillTag.Casting):
            self.castingStartTime = fromSkillVal.castingStartTime

    def checkUseSkill(self, owner, targetID, ignoreReasons=0):
        realSkillVal, _ = self.getRealSkillVal(owner)
        if realSkillVal != self:
            ret = super(CastingSkillVal, self).checkUseSkill(owner, targetID, ignoreReasons)
        else:
            castingSucc = self.isCastingSucc()
            if castingSucc:
                ignoreReasons |= gameconst.UseSkillCheck.OUT_OF_RANGE

            ret = super(CastingSkillVal, self).checkUseSkill(owner, targetID, ignoreReasons)

            if not castingSucc:
                code = gameconst.UseSkillCheck.NEED_CAST
                if not code & ignoreReasons:
                    DEBUG_MSG('use casting skill before finishing casting', self.skillId, time.time(),
                              self.castingStartTime, self.getCastingtimeMax(self.skillId))
                    return code | ret

            elif ret == gameconst.UseSkillCheck.CHEKC_OK:
                target = KBEngine.entities.get(targetID)
                if target and self.needReleaseTarget() and not sMath.inRange2D(gameconst.DEFAULT_AOI, owner.position,
                                                                               target.position):
                    code = gameconst.UseSkillCheck.OUT_OF_RANGE
                    if not code & ignoreReasons:
                        return code

        return ret

    def getEffectTargets(self, caster, targetId, arr, forceTarget=False, positionSkillArgs=None):
        target = KBEngine.entities.get(targetId)
        if (targetId > 0 and not target) or not caster:
            targetId = 0

        forceTarget = self.needReleaseTarget()

        targetIds = super(CastingSkillVal, self).getEffectTargets(caster, targetId, arr, forceTarget)

        return targetIds

    def startCasting(self, caster, targetID, arr):
        if caster.IsAvatar and caster.mp < self.getCostMp(self.skillId, caster.mpCostRatio):
            return

        self.castingStartTime = time.time()

        tid = caster._callback(1, 'castingSkillCheck', (targetID, arr, tuple(caster.position)),
                               gametimer.TIMER_TAG_CASTING_CHECK)
        self.setTempData('castingCheckTimer', tid)
        # caster.setTempMiscProp(gameconst.AvatarProps.castingCheckTimer, checkTimer)

        # #主角由客户端发起释放，其他实体服务器自动放
        # if not caster.IsAvatar or caster._castSkillByServer():
        # 可能是action里cast的技能，直接用技能对象放
        castingTime = self.getCastingtimeMax(self.skillId)
        useTimer = caster._callback(castingTime, '_useSkillBySkillObj', (self, targetID, arr),
                                    gametimer.TIMER_TAG_CASTING_SKILL)
        self.setTempData('castingSkillTimer', useTimer)

        castingAction = self.getSkillData(self.skillId).get('castingAction')
        if castingAction:
            target = KBEngine.entities.get(targetID)
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
                    gameconst.EndCasting.Move, gameconst.EndCasting.ClientCancel, gameconst.EndCasting.MissingTarget,
                    gameconst.EndCasting.Dead, gameconst.EndCasting.Teleporting, gameconst.EndCasting.clientPick):
                needCd = True
        elif cdType == gameconst.CastingSkillCDType.EnterCD:
            needCd = True
        elif cdType == gameconst.CastingSkillCDType.NotEnterCD:
            pass

        if needCd:
            self.tNextCast = time.time() + self.getCD(owner) - 0.1
            owner.client.onSetAddSkillCd(self.skillId, float(self.getCD(owner)), float(self.tNextCast), False)

        owner.IsAICombatUnit and owner.aiController and owner.aiController.onCastingInterrupted(self.skillId)

    def useSkillDone(self, owner, targetId, skillArgs, isSucc=True, startActionFail=False, doRemoveState=True):
        super(CastingSkillVal, self).useSkillDone(owner, targetId, skillArgs, isSucc, startActionFail)
        self.castingStartTime = 0

    def resetSkill(self, owner, reason=gameconst.ResetSkillReason.Default, doRemoveState=True):
        if reason != gameconst.ResetSkillReason.EndCasting:
            castingSkillVal = owner.getCastingSkillInfo()
            if castingSkillVal and castingSkillVal.skillId == self.skillId:
                owner.removeState(gameconst.State.Casting)
        self._cancelTempTimer(owner, 'removeSkillStateTimer', gametimer.TIMER_TAG_REMOVE_SKILL_STATE)
        self._cancelTempTimer(owner, 'castingCheckTimer', gametimer.TIMER_TAG_CASTING_CHECK)
        self._cancelTempTimer(owner, 'castingSkillTimer', gametimer.TIMER_TAG_CASTING_SKILL)
        # self.castingStartTime = 0      #这个只能在startCasting时重置或使用成功后重置
        super(CastingSkillVal, self).resetSkill(owner, reason, doRemoveState)


# 刺客技能:有zedPoint时可能使用的是一个加强版的技能
class ZedSkillVal(CommonSkillVal):
    def __init__(self, skillId, skillLv, tNextCast=0.0, cdDelta=0.0, parentSkill=0):
        super(ZedSkillVal, self).__init__(skillId, skillLv, tNextCast, cdDelta, parentSkill)
        self.enhanceZedSkill = None

    def _lateReload(self):
        super(ZedSkillVal, self)._lateReload()
        if self.enhanceZedSkill:
            self.enhanceZedSkill.reloadScript()

    # 劫强化技能客户端要求onUseSkill里发未强化的技能id
    # A技能被强化为B技能，onUseSkill里总是发A技能id
    def getNotifyClientSkillId(self):
        rootSkillVal = self.getRootSkillVal()
        return rootSkillVal.skillId

    def enhancedZedSkillId(self, owner):
        sd = self.getSkillData(self.skillId)
        if owner.zedPoint >= sd.get('zedBuffNum', 0) and sd.get('zedBuffSkillID'):
            return sd['zedBuffSkillID']
        return 0

    def getEnhancedZedSkill(self, owner):
        if self.enhanceZedSkill:
            return self.enhanceZedSkill
        enhanceSkillId = self.enhancedZedSkillId(owner)
        if enhanceSkillId:
            enhanceZedSkill = self.__class__(enhanceSkillId, self.skillLv, parentSkill=self)
            owner.combatDebugMsg('getEnhancedZedSkill', id(self), id(self.enhanceZedSkill), str(self.enhanceZedSkill),
                                 enhanceSkillId)
            return enhanceZedSkill
        return None

    def checkUseSkill(self, owner, targetId, ignoreReasons=0):
        realSkillVal, _ = self.getRealSkillVal(owner)
        if realSkillVal != self:
            if self.inCDTime():
                code = super(ZedSkillVal, self).checkUseSkill(owner, targetId, ignoreReasons)
                if code != gameconst.UseSkillCheck.CHEKC_OK:
                    return code
            return realSkillVal.checkUseSkill(owner, targetId, ignoreReasons)
        else:
            return super(ZedSkillVal, self).checkUseSkill(owner, targetId, ignoreReasons)

    def beginUseSkill(self, owner, targetId, skillArgs, compensateTime, doSetState=True, enterCD=True, parentCtx=None):
        enhancedSkill = self.getEnhancedZedSkill(owner)
        if enhancedSkill:
            self.enhanceZedSkill = enhancedSkill
            return self.enhanceZedSkill.beginUseSkill(owner, targetId, skillArgs, compensateTime, doSetState, enterCD,
                                                      parentCtx)
        else:
            return super(ZedSkillVal, self).beginUseSkill(owner, targetId, skillArgs, compensateTime, doSetState,
                                                          enterCD, parentCtx)

    def enterCDTime(self, owner, delayCd=0):
        if self.parentSkill:
            self.parentSkill.enterCDTime(owner, delayCd)
        super(ZedSkillVal, self).enterCDTime(owner, delayCd)

    def resetSkill(self, owner, reason=gameconst.ResetSkillReason.Default, doRemoveState=True):
        self.enhanceZedSkill = None
        if self.parentSkill:
            self.parentSkill.enhanceZedSkill = None
            self.parentSkill.resetSkill(owner, reason, doRemoveState)
        super(ZedSkillVal, self).resetSkill(owner, reason, doRemoveState)

    def getRealSkillVal(self, owner):
        enhancedSkill = self.getEnhancedZedSkill(owner)
        if enhancedSkill:
            return enhancedSkill, False
        return self, False


class ZedCastingSkillVal(ZedSkillVal, CastingSkillVal):
    def getEnhancedZedSkill(self, owner):
        enhancedSkill = super(ZedCastingSkillVal, self).getEnhancedZedSkill(owner)

        if enhancedSkill and enhancedSkill.hasTag(gameconst.SkillTag.Casting):
            enhancedSkill.castingStartTime = self.castingStartTime

        return enhancedSkill


class ResetCDZedSkillVal(ZedSkillVal):

    def triggerRefreshSkillCD(self, owner):
        super(ResetCDZedSkillVal, self).triggerRefreshSkillCD(owner)


class StagedSkill(ZedSkillVal):
    def __init__(self, skillId, skillLv, tNextCast=0.0, cdDelta=0.0, parentSkill=0):
        super(StagedSkill, self).__init__(skillId, skillLv, tNextCast, cdDelta, parentSkill)
        self.stageIndex = 0

    def canRemoveFromBuild(self):
        return self.stageIndex == 0 and super(StagedSkill, self).canRemoveFromBuild()

    # 劫强化技能客户端要求onUseSkill里发未强化的技能id
    # A技能被强化为B技能，下发的skillId可能为：
    # A->A1->A2
    # A->B1->B2
    def getNotifyClientSkillId(self):
        rootSkillVal = self.getRootSkillVal()
        if rootSkillVal.enhanceZedSkill and rootSkillVal.stageIndex == 0:
            return rootSkillVal.skillId
        return self.skillId

    def checkUseSkill(self, owner, targetId, ignoreReasons=0):
        realSkillVal, _ = self.getRealSkillVal(owner)
        if realSkillVal == self:
            return super(StagedSkill, self).checkUseSkill(owner, targetId, ignoreReasons)

        return realSkillVal.checkUseSkill(owner, targetId, ignoreReasons)

    def getRealSkillVal(self, owner):
        enhancedSkill = self.getEnhancedZedSkill(owner)
        if enhancedSkill:
            return enhancedSkill.getRealSkillVal(owner)

        if self.stageIndex == 0:
            return self, False
        else:
            curStageSkillId = self.getSkillIdForStage(self.stageIndex)
            if not curStageSkillId:
                return self, False
            curStageSKill = StagedSkill(curStageSkillId, self.skillLv, parentSkill=self)
            return curStageSKill, False

    def getSkillIdForStage(self, stageIndex):
        if stageIndex == 0:
            return self.skillId
        stageSkillIds = self.getSkillData(self.skillId).get('mulSkillID')
        if stageSkillIds and len(stageSkillIds) >= stageIndex:
            return stageSkillIds[stageIndex - 1]
        return 0

    def beginUseSkill(self, owner, targetId, skillArgs, compensateTime, doSetState=True, enterCD=True, parentCtx=None):
        enhancedSkill = self.getEnhancedZedSkill(owner)
        rootSkillVal = self.getRootSkillVal()
        owner.combatDebugMsg('StageSkill.beginUseSkill', id(self), self.skillId, self.stageIndex, targetId, skillArgs,
                             doSetState, owner.zedPoint, getattr(enhancedSkill, 'skillId', 0))
        if enhancedSkill:
            self.enhanceZedSkill = enhancedSkill
            if self is rootSkillVal:
                self.gotoNextStage(owner)

            isSucc, actionCtx, effectTargetIds = self.enhanceZedSkill.beginUseSkill(owner, targetId, skillArgs,
                                                                                    compensateTime, doSetState, enterCD,
                                                                                    parentCtx)

            if self is rootSkillVal:
                self.enhanceZedSkill.gotoNextStage(owner)
            return isSucc, actionCtx, effectTargetIds
        else:
            isEnhancedStage = bool(rootSkillVal.enhanceZedSkill)

            nextStageSkillId = self.getSkillIdForStage(self.stageIndex + 1)
            owner.combatDebugMsg('useStageSkill', self.stageIndex, rootSkillVal.skillId, self.skillId, nextStageSkillId,
                                 isEnhancedStage)

            # 如果有下一段就不进入cd
            enterCD = (nextStageSkillId == 0)
            if self.stageIndex == 0:
                self is rootSkillVal and self.gotoNextStage(owner)
                isSucc, actionCtx, effectTargetIds = super(StagedSkill, self).beginUseSkill(owner, targetId, skillArgs,
                                                                                            compensateTime, doSetState,
                                                                                            enterCD, parentCtx)
            else:
                curStageSkillId = self.getSkillIdForStage(self.stageIndex)
                curStageSKill = StagedSkill(curStageSkillId, self.skillLv, parentSkill=self)
                self is rootSkillVal and self.gotoNextStage(owner)
                isSucc, actionCtx, effectTargetIds = curStageSKill.beginUseSkill(owner, targetId, skillArgs,
                                                                                 compensateTime, doSetState, enterCD,
                                                                                 parentCtx)

            if isSucc:
                if self.hasTempData('stageCDTimer'):
                    self._cancelTempTimer(owner, 'stageCDTimer', gametimer.TIMER_TAG_ON_STAGE_END)
                    self.popTempData('stageCDTimer')
            else:
                return gameconst.StartActionResult.Fail, None, effectTargetIds

            if nextStageSkillId:
                stageDuration = SSD.datas[nextStageSkillId]['mulSkillCD']
                cdTimer = owner._callback(stageDuration, '_onSkillCallback', (self, 'onStageEnd', (True,)),
                                          gametimer.TIMER_TAG_ON_STAGE_END)
                self.setTempData('stageCDTimer', cdTimer)

                clientStageIdx = self.stageIndex
                if isEnhancedStage and nextStageSkillId:
                    stageSkillIds = SSD.datas[rootSkillVal.skillId].get('mulSkillID')
                    clientStageIdx += len(stageSkillIds)
            else:
                clientStageIdx = 0

            ##阶段技能只有普通技能的第一段以及强化后的第一段可以给客户端提交相关数据
            stageSkillIds = self.getSkillData(self.skillId).get('mulSkillID')
            curTime = time.time()
            stageSkillIds and owner.IsAvatar and owner.allClients.onUseStageSkill(rootSkillVal.skillId, clientStageIdx,
                                                                                  curTime)

            return isSucc, actionCtx, effectTargetIds

    def gotoNextStage(self, owner):
        self.stageIndex += 1
        if self.isLastStage(owner):
            self.onStageEnd(owner)

    def isLastStage(self, owner):
        # stageIndex是下次释放技能的stage
        return not self.getSkillIdForStage(self.stageIndex)

    # 超时或放完最后一段结束多段技能
    def onStageEnd(self, owner, endByTimeout=False):
        self._cancelTempTimer(owner, 'stageCDTimer', gametimer.TIMER_TAG_ON_STAGE_END)
        rootSkillVal = self.getRootSkillVal()
        owner.combatDebugMsg('endStage', self.skillId, rootSkillVal.skillId, rootSkillVal.enhanceZedSkill,
                             rootSkillVal.stageIndex)
        rootSkillVal.enterCDTime(owner)
        owner.client.onSetAddSkillCd(rootSkillVal.skillId, float(rootSkillVal.getCD(owner)),
                                     float(rootSkillVal.tNextCast), False)

        if endByTimeout:
            self.resetSkill(owner)
            rootSkillVal.resetSkill(owner)

    def useSkillDone(self, owner, targetId, skillArgs, isSucc=True, startActionFail=False, doRemoveState=True):
        rootSkillVal = self.getRootSkillVal()
        rootSkillVal.onStageSkillDone(owner)

        CommonSkillVal.useSkillDone(self, owner, targetId, skillArgs, isSucc, startActionFail)
        # 多段技能结束，通知父技能Done
        if self is not rootSkillVal and rootSkillVal.isLastStage(owner):
            rootSkillVal.useSkillDone(owner, targetId, skillArgs, isSucc, startActionFail)

    def onStageSkillDone(self, owner):
        pass

    def needResetOnSkillDone(self, owner):
        # 如果技能使用成功且还有下一段就先不reset，否则被reset到第一段了,等着onStageEnd里去reset
        if self.isLastStage(owner):
            return True
        return False

    def resetSkill(self, owner, reason=gameconst.ResetSkillReason.Default, doRemoveState=True):
        if reason == gameconst.ResetSkillReason.Teleport or reason == gameconst.ResetSkillReason.Transform or reason == gameconst.ResetSkillReason.DuelComplete:
            if self.stageIndex > 0:
                self.enterCDTime(owner)
                owner.client.onSetAddSkillCd(self.skillId, float(self.getCD(owner)), float(self.tNextCast), False)
                rootSkillVal = self.getRootSkillVal()
                owner.IsAvatar and owner.client.onUseStageSkill(rootSkillVal.skillId, 0, time.time())

        self.stageIndex = 0
        self.enhanceZedSkill = None
        self._cancelTempTimer(owner, 'stageCDTimer', gametimer.TIMER_TAG_ON_STAGE_END)

        super(StagedSkill, self).resetSkill(owner, reason, doRemoveState)


# 射手特殊技能
class ShooterSkillVal(CommonSkillVal):
    def __init__(self, skillId, skillLv, tNextCast=0.0, cdDelta=0.0, parentSkill=0):
        super(ShooterSkillVal, self).__init__(skillId, skillLv, tNextCast, cdDelta, parentSkill)
        self.tCanUseEndTime = 0
        self.canUseAllTime = 0

    def beginUseSkill(self, owner, targetId, skillArgs, compensateTime, doSetState=True, enterCD=True, parentCtx=None):
        isSucc, actionCtx, effectTargetIds = super(ShooterSkillVal, self).beginUseSkill(owner, targetId, skillArgs,
                                                                                        compensateTime,
                                                                                        doSetState, enterCD, parentCtx)
        if not isSucc:
            owner.client.onUseSkill(False, self.skillId, targetId, [], [])

        endTime = self.tCanUseEndTime - time.time()
        cdTimer = owner._callback(endTime, '_onSkillCallback', (self, 'resetSkill', (owner,)),
                                  gametimer.TIMER_TAG_SHOOTER_SKILL_END)
        self.setTempData('shooterCDTimer', cdTimer)

        return isSucc, None, effectTargetIds

    def resetSkill(self, owner, reason=gameconst.ResetSkillReason.Default, doRemoveState=True):
        self._cancelTempTimer(owner, 'shooterCDTimer', gametimer.TIMER_TAG_SHOOTER_SKILL_END)
        super(ShooterSkillVal, self).resetSkill(owner, reason, doRemoveState)

    def enterCanUseState(self, owner, canUseAllTime=0):
        DEBUG_MSG("enterCanUseState", canUseAllTime)
        if not owner.hasBuff(SRSC.datas['tag95SkillCheckBuff']['valueCN']):
            return

        if time.time() <= self.tCanUseEndTime:
            return

        if not canUseAllTime:
            canUseAllTime = SRSC.datas['tag95DefaultTime'].get('valueCN')

        self.tCanUseEndTime = time.time() + canUseAllTime
        self.canUseAllTime = canUseAllTime
        owner.addBuff(SRSC.datas['tag95SkillAddBuff']['valueCN'], 1, owner.id, canUseAllTime)
        DEBUG_MSG("enterCanUseState2", self.tCanUseEndTime, self.canUseAllTime)
        owner.client.onShooterSkillCanUse(self.skillId, self.tCanUseEndTime, self.canUseAllTime)

    def checkCanUse(self):
        return time.time() < self.tCanUseEndTime

    def checkUseSkill(self, owner, targetId, ignoreReasons=0):
        code = gameconst.UseSkillCheck.SHOOTER_SKILL_CANNOT_USE
        if not code & ignoreReasons and not self.checkCanUse():
            owner.combatDebugMsg('checkUseSkill skill %d cannot use' % (self.getSkillId()), self.tNextCast, time.time())
            return code

        return super(ShooterSkillVal, self).checkUseSkill(owner, targetId, ignoreReasons)


# 超级技能
class UltraSkillVal(CommonSkillVal):
    def beginUseSkill(self, owner, targetId, skillArgs, compensateTime, doSetState=True, enterCD=True, parentCtx=None):
        isSucc, actionCtx, effectTargetIds = super(UltraSkillVal, self).beginUseSkill(owner, targetId, skillArgs,
                                                                                      compensateTime,
                                                                                      doSetState, enterCD, parentCtx)
        if not isSucc:
            owner.client.onUseSkill(False, self.skillId, targetId, [], [])


        return isSucc, actionCtx, effectTargetIds

    def getSkillState(self):
        return gameconst.State.speicalSkill

    def checkUseSkill(self, owner, targetId, ignoreReasons=0):
        return super(UltraSkillVal, self).checkUseSkill(owner, targetId, ignoreReasons)


def getSkillClass(skillId):
    skillData = SkillBase.getSkillData(skillId)
    if not skillData:
        return
    tags = SkillBase.getTag(skillId)

    if gameconst.SkillTag.Casting in tags and gameconst.SkillTag.ZedSkill in tags:
        return ZedCastingSkillVal
    elif gameconst.SkillTag.Casting in tags:
        return CastingSkillVal
    elif gameconst.SkillTag.ResetCDZedSkill in tags:
        return ResetCDZedSkillVal
    elif gameconst.SkillTag.ZedSkill in tags:
        return ZedSkillVal
    elif gameconst.SkillTag.MulStageSkill in tags:
        return StagedSkill
    elif gameconst.SkillTag.Chongfeng in tags:
        return ChongfengSkillVal
    elif gameconst.SkillTag.Lunge in tags:
        return LungeSkillVal
    elif gameconst.SkillTag.DodgeSkill in tags:
        return DodgeSkillVal
    elif gameconst.SkillTag.lzSpecialSkill in tags:
        return ShooterSkillVal
    elif gameconst.SkillTag.UltraSkill in tags:
        return UltraSkillVal
    else:
        return CommonSkillVal
