# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine

import functools
import copy

import userType
import utils
import gameconst

import character_charData as C_C_DD
import skill_skill as SSD
import skillRelevant_skillConst as SRSC
import skillRelevant_skillUpgrade as SRSUD
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import dropAward
import gameclass

import gameglobal
import dataUtils
import LogTrackingMgr
import actionContext

class Build(userType.UserSingleType):
    """BUILD_INFO"""
    ACTIVE_SKILL_SLOTS_COUNT = 14

    ULTRA_SKILL_SLOT = ACTIVE_SKILL_SLOTS_COUNT - 1

    def __init__(self, otherBuild=None):
        if otherBuild:
            self.activeSkills = copy.copy(otherBuild.activeSkills)
            self.skillLevels = copy.copy(otherBuild.skillLevels)
        else:
            self.activeSkills = userType.UserListType([0] * Build.ACTIVE_SKILL_SLOTS_COUNT)
            self.skillLevels = userType.UserDictType()

    def getSlotId(self, skillId):
        slots = self.activeSkills
        try:
            return slots.index(skillId)
        except Exception:
            return None

    def getSlotSkillId(self, slotId):
        slots = self.activeSkills
        if slotId >= len(slots):
            return 0

        return slots[slotId]

    def isRightSlot(self, skillId, slotId):
        isUltraSkill = utils.hasSkillTagById(skillId, gameconst.SkillTag.UltraSkill)
        isGeneralSkill = utils.hasSkillTagById(skillId, gameconst.SkillTag.GeneralSkill)
        if slotId is None:
            return False
        if slotId == 0 and not isGeneralSkill:
            return False
        if slotId != 0 and isGeneralSkill:
            return False
        if slotId == Build.ULTRA_SKILL_SLOT and not isUltraSkill:
            return False
        if slotId != Build.ULTRA_SKILL_SLOT and isUltraSkill:
            return False

        return True

    def getSkillRecommendSlot(self, owner, skillId):
        if utils.hasSkillTagById(skillId, gameconst.SkillTag.UltraSkill):
            if not self.activeSkills[Build.ULTRA_SKILL_SLOT]:
                return Build.ULTRA_SKILL_SLOT
            else:
                return None

        charData = C_C_DD.datas.get(gameglobal.roleCache[owner.id]['school'])
        if not charData:
            return None

        recommendSkills = charData['build']
        recommendSlot = recommendSkills.index(skillId) if skillId in recommendSkills else None
        if recommendSlot is not None and not self.activeSkills[recommendSlot]:
            if not self.isRightSlot(skillId, recommendSlot):
                LOG_ERR('skill and slot mismatch', recommendSlot, skillId)
                return None
            return recommendSlot

        return None

    def containSkill(self, skillId):
        return skillId in self.activeSkills

    def getSkillCfg(self):
        slots = self.activeSkills
        return [{
            'skillId': skillId,
            'slotId': slotId,
        } for slotId, skillId in enumerate(slots)]

    def getLevelsData(self):
        return [{
            'skillId': skillId,
            'level': level
        } for skillId, level in self.skillLevels.items()]

    def getData(self, isNeedActive=True, isNeedLevel=True):
        return {
            'skills': self.getSkillCfg() if isNeedActive else [],
            'skillLevels': self.getLevelsData() if isNeedLevel else [],
        }

    def getSendBuildData(self):
        """
        获取发送给客户端的build数据
        这个数据里的skillLevels中会带有 conflictSkill 的技能等级
        """
        _skillLevels = {k: v for k, v in self.skillLevels.items()}

        _skillData = []
        for _slotId, _skillId in enumerate(self.activeSkills):
            _skillData.append({
                'skillId': _skillId,
                'slotId': _slotId,
            })

            if not _skillId:
                continue

            _conflictSkillIds = SSD.datas[_skillId].get('conflictSkill', ())
            if not _conflictSkillIds:
                continue

            _level = _skillLevels.get(_skillId, 1)

            for _conflictSkillId in _conflictSkillIds:
                _skillLevels[_conflictSkillId] = _level

        _levelsData = []
        for _skillId, _level in _skillLevels.items():
            _levelsData.append({
                'skillId': _skillId,
                'level': _level,
            })

        return {
            'skills': _skillData,
            'skillLevels': _levelsData,
        }

    def buildAddActiveSkill(self, owner, skillId, skillLv):
        self.skillLevels[skillId] = skillLv
        owner.updateSkillLevelSetSummonSlotIdx(skillId, skillLv)
        return True

    def doAddActiveSkill(self, owner, skillId, skillLv):
        self.skillLevels[skillId] = skillLv
        owner.updateSkillLevelSetSummonSlotIdx(skillId, skillLv)
        return True

    def buildRemoveActiveSkill(self, owner, skillId):
        self.skillLevels.pop(skillId, None)
        owner.removeSkillSetSummonSlotIdx([skillId])
        return True

    def changeSkillSlot(self, owner, skillId, fromSlotId, toSlotId, isFromDeleteTempSkill = False, fromSkillNextCastTime = 0):
        if fromSlotId is None and toSlotId is None:
            return

        if skillId not in self.skillLevels:
            return

        if fromSlotId is None:
            owner.cell.doActionOnChangeSlot(skillId, self.skillLevels[skillId], True, True, fromSkillNextCastTime)
        else:
            self.activeSkills[fromSlotId] = 0

        if toSlotId is None:
            owner.cell.doActionOnChangeSlot(skillId, self.skillLevels[skillId], False, False, fromSkillNextCastTime)
            owner.cell.removeSkill(skillId, isFromDeleteTempSkill)
        else:
            self.activeSkills[toSlotId] = skillId

    def getMaxLevel(self, owner, skillId, oldSkillId):
        cfgData = SRSUD.datas.get(skillId, None)
        if not cfgData:
            cfgData = SRSUD.datas.get(oldSkillId, None)
            if not cfgData:
                LOG_ERR('getMaxLevel cfgData is None', skillId, oldSkillId)
                return 1
        return len(cfgData.get('levelLimit')) + 1

    def canLevelUp(self, owner, skillId, delta):
        if skillId not in self.skillLevels:
            return False

        _morphBaseSkillId = dataUtils.getSkillIdByMorphState(skillId, gameconst.MORPH_BUILD_STATE)
        if delta > 0 and self.skillLevels[skillId] + delta > self.getMaxLevel(owner, _morphBaseSkillId, _morphBaseSkillId):
            LOG_DBG('skillLv reach max', owner.id, skillId, self.skillLevels)
            return False

        if delta < 0 and self.skillLevels[skillId] + delta < 1:
            LOG_DBG('skillLv reach min', owner.id, skillId, self.skillLevels)
            return False

        if not owner.hasSkill(skillId):
            LOG_DBG('skill does not unlocked')
            return False

        return True

    def levelUp(self, owner, skillId, oldSkillId, delta):
        if skillId not in self.skillLevels:
            return False

        if delta != 1:
            LOG_ERR('levelUp delta must be 1', skillId, delta)
            return

        _morphBaseSkillId = dataUtils.getSkillIdByMorphState(skillId, gameconst.MORPH_BUILD_STATE)
        if delta > 0 and self.skillLevels[skillId] >= self.getMaxLevel(owner, _morphBaseSkillId, oldSkillId):
            LOG_DBG('skillLv reach max', owner.id, skillId, self.skillLevels)
            return False

        if not owner.hasSkill(skillId):
            LOG_DBG('skill does not unlocked')
            return False

        oldLevel = self.skillLevels[skillId]

        cfgData = SRSUD.datas.get(_morphBaseSkillId, None)
        if not cfgData:
            cfgData = SRSUD.datas[oldSkillId]

        selfLevel = gameglobal.roleCache[owner.id]['level']
        levelLimit = cfgData.get('levelLimit')[oldLevel-1]
        if selfLevel < levelLimit:
            LOG_ERR('level limit:', selfLevel, levelLimit)
            return False

        costItemInfo = {}
        consumeItem = cfgData.get('consumeItem')[oldLevel-1]
        deductVal = dropAward.DeductWealthVal()
        for costItemId, itemNum in zip(consumeItem[::2], consumeItem[1::2]):
            deductVal.addWealthByItemId(costItemId, itemNum)
            costItemInfo[costItemId] = costItemInfo.get(costItemId, 0) + itemNum

        consumeMoney = cfgData.get('consumeMoney')[oldLevel-1]
        costItemId, itemNum = consumeMoney
        deductVal.addWealthByItemId(costItemId, itemNum)

        if not owner.canDeductWealth(deductVal, sendMsg=True):
            LOG_WARN('   in levelUp, canDeductWealth fail:', skillId, delta)
            return

        opUUID = KBEngine.genUUID64()
        src = AAC_AACDD.datas.BONUS_SRC_SKILL_UPGRADE
        detail = gameclass.AwardDetailCls(skillId=skillId)
        owner.deductWealth(src, deductVal, opUUID, detail)
        newLevel = int(min(oldLevel + delta, self.getMaxLevel(owner, _morphBaseSkillId, oldSkillId)))
        self.skillLevels[skillId] = newLevel
        self.skillLevels[oldSkillId] = newLevel
        owner.updateSkillLevelSetSummonSlotIdx(skillId, newLevel)

        # 被动技能替换的技能一并要升级
        relatedSkills = SSD.datas.get(skillId, {}).get('conflictSkill') or ()
        skillIdList = [skillId] + list(relatedSkills)
        for sid in relatedSkills:
            if sid in self.skillLevels:
                self.skillLevels[sid] = newLevel
                owner.updateSkillLevelSetSummonSlotIdx(sid, newLevel)

        owner.onChangeSkillLv(skillId, newLevel)
        owner.client.onUpdateSkillLevel(skillIdList, [newLevel] * len(skillIdList))
        #
        owner.achievementInfo.triggerAchieveByType(
            owner,
            gameconst.AchieveType.LEVEL_UP_SKILL,
            actionContext.AchievementCtx(oldLevel=oldLevel, newLevel=newLevel))
        LogTrackingMgr.LogTrackingMgr.Skill_Upgrade(owner.gbID, owner.accountEntity.clientDistinctId, owner.gbID, skillId, list(costItemInfo.keys()), list(costItemInfo.values()), consumeMoney[0], consumeMoney[1], newLevel, opUUID)
        return True

    def resetAllSkill(self, caster):
        totalSkillIdList = []
        for skillId in self.skillLevels:
            totalSkillIdList.append(skillId)
            self.skillLevels[skillId] = 1
            caster.updateSkillLevelSetSummonSlotIdx(skillId, 1)
            relatedSkills = SSD.datas.get(skillId, {}).get('conflictSkill') or ()
            for sid in relatedSkills:
                totalSkillIdList.append(sid)
                if sid in self.skillLevels:
                    self.skillLevels[sid] = 1
                    caster.updateSkillLevelSetSummonSlotIdx(sid, 1)
            caster.onChangeSkillLv(self.buildId, skillId, 1)

        caster.client.onUpdateSkillLevel(totalSkillIdList, [1] * len(totalSkillIdList))

    def getSkillIds(self):
        slots = self.activeSkills
        return slots

    def updateSkillLevel(self, owner, skillIdLevelList):
        for skillLevelInfo in skillIdLevelList:
            skillId, skillLevel = skillLevelInfo

            if skillId not in self.skillLevels:
                return False

            self.skillLevels[skillId] = skillLevel
            owner.updateSkillLevelSetSummonSlotIdx(skillId, skillLevel)

            # 被动技能替换的技能一并要升级
            relatedSkills = SSD.datas.get(skillId, {}).get('conflictSkill') or ()
            skillIdList = [skillId] + list(relatedSkills)
            for sid in relatedSkills:
                if sid in self.skillLevels:
                    self.skillLevels[sid] = skillLevel
                    owner.updateSkillLevelSetSummonSlotIdx(sid, skillLevel)

            owner.onChangeSkillLv(skillId, skillLevel)
            owner.client.onUpdateSkillLevel(skillIdList, [skillLevel] * len(skillIdList))

        return True

    def getSkillLevel(self, skillId):
        if skillId not in self.skillLevels:
            LOG_ERR("getSkillLevel not in self.skillLevels", skillId)
            return 0

        return self.skillLevels[skillId]


def buildCheck(fn):
    @functools.wraps(fn)
    def wrapfn(self, *args, **kwargs):
        if args[0] >= len(self):
            LOG_ERR(fn.__name__, 'builds has no buildId', args[0])
            return

        return fn(self, *args, **kwargs)

    return wrapfn


class ServerBuilds(userType.UserListType):
    def __init__(self):
        pass

    def getSlotId(self, buildId, skillId, isActive=True):
        if buildId >= len(self):
            LOG_ERR('getSlotId builds has no buildId', buildId)
            return None

        return self[buildId].getSlotId(skillId, isActive)

    @buildCheck
    def getSkillIdBySlotId(self, buildId, slotId, isActive=True):
        return self[buildId].getSlotSkillId(slotId, isActive)

    @buildCheck
    def getBuildMirrorInfo(self, buildId):
        return {'builds': [self[buildId].getData()]}

    @buildCheck
    def getBuildClientData(self, buildId):
        return self[buildId].getData()

    @buildCheck
    def getClientData(self, buildId):
        return self[buildId].getData()

    def toClientData(self):
        builds = []
        for i, buildVal in enumerate(self):
            if not self.isBuildUnLocked(i):
                continue

            builds.append(self.getBuildClientData(i))

        return {'builds': builds}

    def getDBData(self):
        builds = []
        for i, buildVal in enumerate(self):
            builds.append(self.getBuildClientData(i))

        return {'builds': builds}

    @buildCheck
    def getPassiveSkillClientData(self, buildId):
        passiveData = self[buildId].getData(isNeedActive=False, isNeedLevel=False)
        passiveData.pop('skills')
        passiveData.pop('skillLevels')
        passiveData.pop('pSkillLevels')
        return passiveData

    def initBuild(self, buildId, buildName, copyFromBuildVal=None):
        self[buildId] = Build(buildId, buildName, copyFromBuildVal)
        return self[buildId]

    def isBuildUnLocked(self, buildId):
        return self[buildId].buildName

    def buildAddActiveSkill(self, owner, skillId, skillLv):
        for buildVal in self:
            if not buildVal:
                continue
            buildVal.doAddActiveSkill(owner, skillId, skillLv)

    def setBuildSkillLv(self, owner, skillId, skillLv):
        for buildVal in self:
            if not buildVal:
                continue

            if skillId not in buildVal.skillLevels:
                continue

            buildVal.skillLevels[skillId] = skillLv
        owner.onChangeSkillLv(owner.buildId, skillId, skillLv)

    @buildCheck
    def getSkills(self, buildId, isActive=True):
        return self[buildId].getSkillIds(isActive)

    def _lateReload(self):
        super(ServerBuilds, self)._lateReload()

        for i, buildVal in enumerate(self):
            buildVal.reloadScript()

        return
