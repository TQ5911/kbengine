# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine

import gameconst
import gamedecorator
import dropAward
import utils
import json
import gameglobal
import actionContext
import gametimer

import skill_skill as SSD
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import skill_unlock as SUD
import fightProp_define as FPDD
import skillRelevant_summonUnlock as SRSU
import skillRelevant_skillConst as SRSC
import gamelog
import gameconfig
import gameclass
import gamePlay_set as GP_SD
import formula_generalFormula as F_GFD
import dataUtils
import taskClass_taskTarget as TCCTD


class AvatarBuildsMixin(object):
    def __init__(self):
        pass

    def initNoviceSkills(self):
        if gameglobal.roleCache[self.id]['school'] and gameglobal.roleCache[self.id]['level']:
            self.initSkillAfterHasSchool()

    def initSkillAfterHasSchool(self):
        self.initNoviceBuild()
        self.checkUnlockBuildAndSkillByLevel(False, gameglobal.roleCache[self.id]['level'])
        self.cell.unlockDodgeSkill(0, 1)
        self.sendCliSkillBuildInfo()
        self.updateSkillScore()

    def getSkillIdBySlotId(self, slotId):
        skillId = self.buildDic.getSlotSkillId(slotId)
        return skillId if skillId else None

    # 技能升级
    def baseLevelUpSkill(self, newSkillId, oldSkillId, levelDelta):
        LOG_IFO('baseLevelUpSkill', newSkillId, oldSkillId, levelDelta)
        _skillId = dataUtils.getSkillIdByMorphState(newSkillId, self.morphState)
        self._levelUpSkill(_skillId, oldSkillId, levelDelta)
        self.updateSkillScore()

    def _levelUpSkill(self, newSkillId, oldSkillId, levelDelta):
        LOG_IFO("_levelUpSkill", newSkillId, oldSkillId, levelDelta)
        if not self.buildDic.levelUp(self, newSkillId, oldSkillId, levelDelta):
            LOG_IFO('skill can not levelUp', newSkillId, oldSkillId)
            return False

        self.achievementInfo.triggerAchieveByType(
            self,
            gameconst.AchieveType.LEVEL_UP_SKILL,
            actionContext.AchievementCtx())
        return True

    def onChangeSkillLv(self, skillId, toLv):
        self.cell.onChangeSkillLv(skillId, toLv)

    def _isCanUnlockSkill(self, isActive, skillId, lv, mid):
        condStr = SSD.datas[skillId]['unlockCondition']

        if not condStr:
            return True

        res = self._isUIVisibleStr(condStr)
        return res

    def unlockSkill(self, isNotify, lv=0, mid=0):
        unlockedSkills = []
        school = gameglobal.roleCache[self.id]['school']
        if school in SUD.datas:
            activeSkills = SUD.datas[gameglobal.roleCache[self.id]['school']].get('data')
            for skillIds in activeSkills:
                for skillId in skillIds:
                    if not skillId:
                        continue
                    skillId = dataUtils.getSkillIdByMorphState(skillId, self.morphState)
                    if not self._isCanUnlockSkill(True, skillId, lv, mid):
                        continue

                    _buildSkillId = dataUtils.getSkillIdByMorphState(skillId, gameconst.MORPH_BUILD_STATE)
                    taskId = self.checkHasUnlockedTemporarySkill(_buildSkillId)
                    if taskId:
                       self.cannelTemporarySkill(taskId, _buildSkillId)
                    else:
                        if self.unlockActiveSkill(_buildSkillId, skillId, isNotify, lv, mid):
                            LOG_IFO('unlock skill', skillId)
                            unlockedSkills.append(skillId)

        if unlockedSkills:
            self.updateSkillScore()

    def unlockActiveSkill(self, _buildSkillId, skillId, isNotify, lv, mid):
        if self.hasSkill(skillId):
            return False

        skillLv = 1

        self.buildDic.buildAddActiveSkill(self, skillId, skillLv)

        recommendSlot = self.buildDic.getSkillRecommendSlot(self, _buildSkillId)
        if recommendSlot is not None:
            self.buildDic.changeSkillSlot(self, skillId, None, recommendSlot)

        return True

    def cannelTemporarySkill(self, taskId, skillId):
        unlockedSkills = self.tmpTaskSkillIds.get(taskId, [skillId])
        unlockedSkills.remove(skillId)

    def checkHasUnlockedTemporarySkill(self, skillId):
        for taskId, unlockedSkills in self.tmpTaskSkillIds.items():
            if skillId in unlockedSkills:
                return taskId
        return None

    def unlockTemporarySkill(self, _buildSkillId, _stateSkillId, skillLv):
        if self.hasSkill(_buildSkillId):
            return False

        self.buildDic.buildAddActiveSkill(self, _stateSkillId, skillLv)
        recommendSlot = self.buildDic.getSkillRecommendSlot(self, _buildSkillId)
        if recommendSlot is not None:
            self.buildDic.changeSkillSlot(self, _stateSkillId, None, recommendSlot)

        return True

    def deleteTemporarySkill(self, _buildSkillId, _stateSkillId):
        slotId = self.buildDic.getSlotId(_stateSkillId)
        if slotId is None:
            slotId = self.buildDic.getSlotId(_buildSkillId)
        self.buildDic.changeSkillSlot(self, _stateSkillId, slotId, None, True)
        if _buildSkillId != _stateSkillId:
            self.buildDic.changeSkillSlot(self, _buildSkillId, slotId, None, True)

        relatedSkills = SSD.datas.get(_buildSkillId, {}).get('conflictSkill') or ()
        skillIdList = [_buildSkillId] + list(relatedSkills)
        for skillId in skillIdList:
            if not self.hasSkill(skillId):
                continue
            self.buildDic.buildRemoveActiveSkill(self, skillId)

    def initNoviceBuild(self):
        pass

    def onChangeSkill(self, fromSkillId, toSkillId, fromSkillNextCastTime):
        skillIds = self.buildDic.getSkillIds()
        if toSkillId in skillIds:
            LOG_WARN("onChangeSkill toSkillId was in buildDic", fromSkillId, toSkillId, skillIds)

        slotId = self.buildDic.getSlotId(fromSkillId)
        if slotId is None:
            return

        buildVal = self.buildDic

        buildVal.changeSkillSlot(self, fromSkillId, slotId, None)
        buildVal.changeSkillSlot(self, toSkillId, None, slotId, fromSkillNextCastTime = fromSkillNextCastTime)

        self.client.onChangeSkill(fromSkillId, toSkillId)

    def buildAddActiveSkill(self, skillId, skillLv):
        self.buildDic.doAddActiveSkill(self, skillId, skillLv)
        self.client.onUpdateSkillLevel([skillId], [skillLv])

    def hasSkill(self, skillId):
        return skillId in self.buildDic.skillLevels

    # 拖技能到build
    @gamedecorator.crossServer
    def updateSkills(self, exposed, skillSlotInfos):
        LOG_IFO("updateSkills ", skillSlotInfos)
        self._updateSkills(skillSlotInfos, True, True)

    def _updateSkills(self, skillSlotInfos, bNotifyClient=False, isMessage=False):
        skillCheckList = []
        for skillSlotInfo in skillSlotInfos:
            skillId = skillSlotInfo['skillId']
            # 需要处理下冲突技能
            skillId = dataUtils.getSkillIdByMorphState(skillId, self.morphState)
            toSlotId = skillSlotInfo['slotId']
            if toSlotId < 0:
                toSlotId = None

            if not self.buildDic.isRightSlot(skillId, toSlotId):
                return

            toSkillId = self.getSkillIdBySlotId(toSlotId)
            skillCheckList.append((toSkillId, skillId, toSlotId))

        self.onCheckUpdateSkillRet(True, skillCheckList, bNotifyClient, isMessage)

    def onCheckUpdateSkillRet(self, bCanUpdate, skillSlotInfos, bNotifyClient=False, isMessage=False):
        updateResult = {}
        if bCanUpdate:
            for skillSlotInfo in skillSlotInfos:
                toSkillId, skillId, toSlotId = skillSlotInfo
                if toSlotId < 0:
                    toSlotId = None

                fromSlotId = self.buildDic.getSlotId(skillId)
                currentSkillId = self.getSkillIdBySlotId(toSlotId)

                buildVal = self.buildDic
                if currentSkillId:
                    buildVal.changeSkillSlot(self, currentSkillId, toSlotId, fromSlotId)
                    if len(skillSlotInfos) == 1:
                        currentSkillLevel = buildVal.skillLevels[currentSkillId]
                        skillLevel = buildVal.skillLevels[skillId]
                        skillLevelList = [(skillId, currentSkillLevel)]
                        skillLevelList.append((currentSkillId, skillLevel))
                        buildVal.updateSkillLevel(self, skillLevelList)

                buildVal.changeSkillSlot(self, skillId, fromSlotId, toSlotId)

                if fromSlotId is not None:
                    updateResult[fromSlotId] = buildVal.activeSkills[fromSlotId]
                if toSlotId is not None:
                    updateResult[toSlotId] = buildVal.activeSkills[toSlotId]

            if updateResult and bNotifyClient:
                self.client.dragSkillChangeBuildSkills(json.dumps(updateResult).encode('ascii'))

    def sendCliSkillBuildInfo(self):
        self.client.sendSkillBuilds(self.buildDic.getData())


class ImpCombat(AvatarBuildsMixin):
    # ------------------- dead and relive start -------------------

    def addDeathPenaltyVal(self, expChange, coinChange, killerGbId, killerName, opUUID, killerData):
        _showList = []
        if coinChange:
            _src = AAC_AACDD.datas.BONUS_SRC_DEAD_PENALTY # TODO: DEAD_PENALTY
            _coin = min(coinChange, self.coin)
            _deductVal = dropAward.DeductWealthVal(coin=_coin) # TODO: DEAD_PENALTY
            _detail = gameclass.AwardDetail()
            self.deductWealth(_src, _deductVal, opUUID, _detail)
            _showList = _deductVal.toBriefList()

        if expChange:
            _toClientData = self.deathPenaltyData.addDeathPenaltyExp(expChange)
            if _toClientData:
                self.client.onDeathPenaltyExpChange(_toClientData)

            _showList.append({'itemId': gameconst.ItemId.EXP, 'itemNum': expChange, 'bindType': gameconst.ItemBindType.BIND})

        self.client.onDeathPenaltyReward(killerGbId, killerName, _showList, killerData)

    def refreshFreeRecoverDeathPenaltyTimes(self):
        self.freeRecoverDeathPenaltyTimes = GP_SD.datas['freeExpRecCount']['value']

    def recoverDeathPenaltyExp(self, exposed, expireTime, itemId):
        LOG_IFO('recoverDeathPenaltyExp:', expireTime, itemId)
        if expireTime < utils.curTS():
            LOG_ERR('recoverDeathPenaltyExp expireTime invalid:', expireTime, self.gbID)
            return

        _exp = self.deathPenaltyData.getDeathPenaltyExp(expireTime)
        if not _exp:
            LOG_ERR('recoverDeathPenaltyExp not found:', expireTime, self.gbID)
            return

        _opUUID = KBEngine.genUUID64()
        _ratio = 1
        if itemId == 0:
            if self.freeRecoverDeathPenaltyTimes <= 0:
                LOG_ERR('recoverDeathPenaltyExp freeRecoverDeathPenaltyTimes:', self.gbID)
                return

            self.freeRecoverDeathPenaltyTimes -= 1
            _ratio = GP_SD.datas['freeExpRecPct']['value']
        else:
            if itemId == gameconst.ItemId.COIN:
                _formulaId = GP_SD.datas['normalExpRecCost']['value']
                _num = F_GFD.datas[_formulaId]['serverFormula'](_exp)
                _ratio = GP_SD.datas['normalExpRecPct']['value']
            elif itemId == gameconst.ItemId.BIND_MONEY:
                _formulaId = GP_SD.datas['advancedExpRecCost']['value']
                _num = F_GFD.datas[_formulaId]['serverFormula'](_exp)
                _ratio = GP_SD.datas['advancedExpRecPct']['value']
            else:
                LOG_ERR('recoverDeathPenaltyExp itemId invalid:', itemId, self.gbID)
                return

            _src = AAC_AACDD.datas.BONUS_SRC_RECOVER_DEAD_PENALTY_DEDUCT
            _deductVal = dropAward.DeductWealthVal()
            _deductVal.addWealthByItemId(itemId, _num)
            if not self.canDeductWealth(_deductVal, sendMsg=True):
                LOG_ERR('recoverDeathPenaltyExp canDeductWealth failed:', self.gbID)
                return

            self.deductWealth(_src, _deductVal, _opUUID, gameclass.AwardDetail())

        self.deathPenaltyData.removeDeathPenaltyVal(expireTime)

        _src = AAC_AACDD.datas.BONUS_SRC_RECOVER_DEAD_PENALTY
        _awardVal = dropAward.AwardVal(exp=int(_exp * _ratio))
        self.addWealth(_src, _awardVal, _opUUID, gameclass.AwardDetail())

        self.client.onDeathPenaltyExpChange([{"expireTime": expireTime, "exp": 0}])

    def removeDeathPenaltyExp(self, exposed, expireTime):
        LOG_IFO('removeDeathPenaltyExp:', expireTime)
        if self.deathPenaltyData.removeDeathPenaltyVal(expireTime):
            self.client.onDeathPenaltyExpChange([{"expireTime": expireTime, "exp": 0}])

    # ------------------- dead and relive end -------------------

    def onAvatarLevelUpBase(self, oldLv, newLv):
        self._onLvUpVisible(oldLv, newLv)
        self.onTaskAvatarLvUp(oldLv, newLv)
        # self._modifyRedisAttr({'level': newLv})
        self.accountEntity.updateCharacterLevel(self.gbID, newLv, self.tLoginBase)
        if self.subAccount:
            self.subAccount.updateCharacterLevel(self.gbID, newLv, self.tLoginBase)

        self.checkUnlockBuildAndSkillByLevel(True, newLv)

        self.lastLevelupTime = utils.curTS()
        self._modifyRedisAttr({'level': newLv})

        self.guildBox and self.guildBox.onGuildMemberPropUpdate(self.gbID, 'level', newLv)
        self.propChangedTimes[gameconst.LeaderBoardType.AVATAR_LEVEL] = utils.curTS()

        self.achievementInfo.onLvUpAchievement(oldLv, newLv, self)
        self.checkAndUnlockWelfareSignIn()
        self.checkUnlockBountyTask()
        self._updateLeaderBoardAvatar()

    def playerDeadTlog(self, tlogProps):
        pass

    def playerReliveTlog(self, tlogProps):
        pass

    def addAwardFightProps(self, fightProps, srcType, awardId, opUUID, detail):
        syncPropList = []
        for propName, val in fightProps:
            fpData = FPDD.datas.get(propName)
            if not fpData:
                LOG_ERR('addAwardFightProps name invalid:', propName, val)
                continue

            if fpData['formulaPlayer']:
                LOG_ERR('addAwardFightProps prop be rely on:', propName, val)
                continue

            self.awardFightPropDic[propName] = self.awardFightPropDic.get(propName, 0) + val
            syncPropList.append((propName, val))

        self.cell.addAwardFightPropsCell(syncPropList)
        # gamelog.makeAddAwardFightPropsLog(self, srcType, awardId, opUUID, str(detail), ','.join(logStrs))

    def sendServerLevel(self, serverLevel=0):
        serverLevel = serverLevel or utils.getServerLevel()

    def playerExpFlowLog(self, expChange, oldLevel, newLevel, iTime, srcType, srcSubType=0, detail=None, idipSource=0):
        roleInfo = gameglobal.roleCache.get(self.id)
        logDataDic = {
            'vGameAppid': utils.getGameAppId(self.accountEntity.channelId),
            'PlatID': self.accountEntity.devicePlatId,
            'iZoneAreaID': gameconfig.serverId(),
            'vOpenID': self.accountEntity.accountName,
            'vRoleID': str(self.gbID),
            'vRoleName': roleInfo['name'],
            'iLevel': roleInfo['level'],
            'iVipLevel': 0,
            'iRoleCE': roleInfo.get('battlePoint', 0),
            'ExpChange': expChange,
            'BeforeLevel': oldLevel,
            'AfterLevel': newLevel,
            'iTime': utils.curTS() - self.lastLevelupTime if oldLevel != newLevel else 0,
            'Reason': srcType,
            'SubReason': srcSubType,
            'Detail': str(detail),
            'IDIPSource': idipSource,
        }
        gamelog.makePlayerExpFlowLog(logDataDic)

    def checkUnlockBuildAndSkillByLevel(self, isNotify, newLv):
        self.unlockSkill(isNotify, newLv, 0)
        self.sendCliSkillBuildInfo()


    def checkUnlockBuildAndSkillByTask(self, isNotify, messionId):
        self.unlockSkill(isNotify, 0, messionId)
        self.sendCliSkillBuildInfo()

    
    def onKillOtherAvatar(self, gbId, spaceNo, name, school, level, sex):
        if gbId == self.gbID:
            return

        self.enemyMgr.onKillOtherAvatarRecord(self, gbId, spaceNo, name, school, level, sex)

    def unlockTemporarySkillByTask(self, taskId, skillList):
        unlockedSkills = []
        for skillId in skillList:
            _stateSkillId = dataUtils.getSkillIdByMorphState(skillId, self.morphState)
            _buildSkillId = dataUtils.getSkillIdByMorphState(skillId, gameconst.MORPH_BUILD_STATE)
            if not self.unlockTemporarySkill(_buildSkillId, _stateSkillId, 1):
                continue
            unlockedSkills.append(_buildSkillId)

        if unlockedSkills:
            self.tmpTaskSkillIds[taskId] = unlockedSkills
            self.updateSkillScore()
        self.sendCliSkillBuildInfo()

    def deleteTemporarySkillByTask(self, taskId):
        if taskId not in self.tmpTaskSkillIds:
            return

        unlockedSkills = self.tmpTaskSkillIds.pop(taskId, [])
        for _buildSkillId in unlockedSkills:
            _stateSkillId = dataUtils.getSkillIdByMorphState(_buildSkillId, self.morphState)
            self.deleteTemporarySkill(_buildSkillId, _stateSkillId)
        self.removeSkillChangeMorphState(unlockedSkills)

        self.sendCliSkillBuildInfo()

    def initRemoveTemporarySkill(self):
        removeTaskIds = list(self.tmpTaskSkillIds.keys())
        for taskId in removeTaskIds:
            self.deleteTemporarySkillByTask(taskId)

    # 变身状态 start ---------------------------------

    def changeMorphStateBase(self, morphState):
        if morphState == self.morphState:
            return

        self.morphState = morphState

        _skillLevelList = []
        updateResult = {}
        for _slotId, _skillId in list(enumerate(self.buildDic.activeSkills)):
            _modId = SSD.skillToModDic.get(_skillId)
            if not _modId:
                continue

            _newSkillId = SSD.modDic[_modId][morphState]
            if _newSkillId == _skillId:
                continue

            self.buildDic.changeSkillSlot(self, _skillId, _slotId, None)
            _skillLevel = self.buildDic.skillLevels[_skillId]
            self.buildDic.doAddActiveSkill(self, _newSkillId, _skillLevel)
            self.buildDic.changeSkillSlot(self, _newSkillId, None, _slotId)

            _skillLevelList.append((_newSkillId, _skillLevel))
            updateResult[_slotId] = _newSkillId

        if _skillLevelList:
            self.buildDic.updateSkillLevel(self, _skillLevelList)

        if updateResult:
            self.client.dragSkillChangeBuildSkills(json.dumps(updateResult).encode('ascii'))

    # 变身状态 end ---------------------------------

    # 快捷吃药 start ---------------------------------

    @gamedecorator.checkGameconfigEnable('quickSettings')
    def setInstantPotionSlots(self, exposed, potion):
        LOG_IFO('setInstantPotionSlots', potion)
        _oldAutoHealHp = self.instantPotionSlots._hasAutoHealHp()
        _oldAutoHealMp = self.instantPotionSlots._hasAutoHealMp()
        if not self.instantPotionSlots.updateSlot(self, potion):
            LOG_ERR('setInstantPotionSlots failed', self.gbID)
            return

        self.taskCheckCounterTarget(TCCTD.couterTargetDic['TaskCounterTargetSetHp'], ())

        self.client.onSetInstantPotionSlots(potion)

        _newAutoHealHp = self.instantPotionSlots._hasAutoHealHp()
        _newAutoHealMp = self.instantPotionSlots._hasAutoHealMp()

        if _oldAutoHealHp != _newAutoHealHp:
            self.cell.updateCommonFlagCell(
                gameconst.AvatarFlagCell.AUTO_HEAL_HP,
                _newAutoHealHp)

        if _oldAutoHealMp != _newAutoHealMp:
            self.cell.updateCommonFlagCell(
                gameconst.AvatarFlagCell.AUTO_HEAL_MP,
                _newAutoHealMp)

        if self.instantPotionSlots._needAutoDrinkBase():
            self._startAutoDrinkPotionTimer()
        else:
            self._stopAutoDrinkPotionTimer()

    def _onAutoDrinkPotionTimer(self):
        self.instantPotionSlots.drinkAll(self)

    def _startAutoDrinkPotionTimer(self):
        if self.autoDrinkPotionTimerId:
            return

        self.autoDrinkPotionTimerId = self.pyAddTimer(5, 5, gametimer.AUTO_DRINK_POTION_TIMER)

    def _stopAutoDrinkPotionTimer(self):
        if not self.autoDrinkPotionTimerId:
            return

        self.pyDelTimer(self.autoDrinkPotionTimerId, gametimer.AUTO_DRINK_POTION_TIMER)
        self.autoDrinkPotionTimerId = 0

    @gamedecorator.checkGameconfigEnable('quickSettings')
    def unsetInstantPotionSlots(self, exposed, slotId):
        LOG_IFO('unsetInstantPotionSlots', slotId)
        self.instantPotionSlots.unsetSlot(slotId)

        self.client.onRemoveInstantPotionSlots(slotId)

    def autoHealHp(self):
        for potion in self.instantPotionSlots.slots:
            if not potion.isHp():
                continue

            if not utils.bhas(potion.potionState, gameconst.PotionState.AUTO):
                continue

            if self.useItemWithActionInternal(
                    gameconst.BagType.BAG_TYPE_NORMAL,
                    potion.itemId,
                    self.id):
                break

    def autoHealMp(self):
        for potion in self.instantPotionSlots.slots:
            if not potion.isMp():
                continue

            if not utils.bhas(potion.potionState, gameconst.PotionState.AUTO):
                continue

            if self.useItemWithActionInternal(
                    gameconst.BagType.BAG_TYPE_NORMAL,
                    potion.itemId,
                    self.id):
                break

    # 快捷吃药 end ---------------------------------

    def initSummonSlotIdx(self):
        LOG_IFO('initSummonSlotIdx', self.summonSlotIdxBase)
        self.cell.setSummonSlotIdx(self.summonSlotIdxBase)

    def setSummonSlotIdx(self, exposed, slotIdx):
        self._setSummonSlotIdx(slotIdx)

    def _setSummonSlotIdx(self, slotIdx):
        if slotIdx == self.summonSlotIdxBase:
            LOG_IFO('base setSummonSlotIdx same idx', slotIdx)
            return

        school = gameglobal.roleCache[self.id]['school']
        summonSkillId = SRSC.datas['summonSkillId'].get('valueCN', 0)
        summonSchool = SRSC.datas['usePlayerForSummon'].get('valueCN', 0)
        skillLevel = self.buildDic.getSkillLevel(summonSkillId)
        LOG_IFO('base setSummonSlotIdx', slotIdx, self.summonSlotIdxBase, school, skillLevel)
        if school != summonSchool:
            LOG_ERR('base setSummonSlotIdx school error', school, summonSchool)
            return
        if slotIdx <= 0 or slotIdx > SRSU.maxKey:
            LOG_ERR('base setSummonSlotIdx slotIdx error', slotIdx)
            return
        if skillLevel < SRSU.datas[slotIdx].get('UnlockLevel', 0):
            LOG_ERR('base setSummonSlotIdx unlock', skillLevel, SRSU.datas[slotIdx])
            return

        self.cell.setSummonSlotIdx(slotIdx)

    def updateSkillLevelSetSummonSlotIdx(self, skillId, skillLevel):
        school = gameglobal.roleCache[self.id]['school']
        summonSkillId = SRSC.datas['summonSkillId'].get('valueCN', 0)
        summonSchool = SRSC.datas['usePlayerForSummon'].get('valueCN', 0)
        if school != summonSchool or skillId != summonSkillId:
            return

        if self.summonSlotIdxBase == 0:
            LOG_IFO('base updateSkillLevelSetSummonSlotIdx1', skillId, skillLevel)
            self._setSummonSlotIdx(SRSU.minKey)
            return

        slotIdx = 0
        for idx in range(self.summonSlotIdxBase, 0, -1):
            if skillLevel >= SRSU.datas[idx].get('UnlockLevel', 0):
                slotIdx = idx
                break

        if slotIdx == self.summonSlotIdxBase:
            return

        LOG_IFO('base updateSkillLevelSetSummonSlotIdx2', self.summonSlotIdxBase, slotIdx, skillId, skillLevel)
        self.cell.setSummonSlotIdx(slotIdx)

    def setSummonSlotIdxAck(self, slotIdx):
        LOG_IFO('base setSummonSlotIdxAck', self.summonSlotIdxBase, slotIdx)
        self.summonSlotIdxBase = slotIdx

    def removeSkillSetSummonSlotIdx(self, removedSkills):
        school = gameglobal.roleCache[self.id]['school']
        summonSkillId = SRSC.datas['summonSkillId'].get('valueCN', 0)
        summonSchool = SRSC.datas['usePlayerForSummon'].get('valueCN', 0)
        if school != summonSchool or summonSkillId not in removedSkills:
            return

        LOG_IFO('base removeSkillSetSummonSlotIdx ', self.summonSlotIdxBase, removedSkills)
        self.summonSlotIdxBase = 0
        self.cell.setSummonSlotIdx(0)

    def removeSkillChangeMorphState(self, removedSkills):
        school = gameglobal.roleCache[self.id]['school']
        summonSkillId = SRSC.datas['summonSkillId'].get('valueCN', 0)
        summonSchool = SRSC.datas['usePlayerForSummon'].get('valueCN', 0)
        if school != summonSchool or summonSkillId not in removedSkills:
            return
        if self.morphState == gameconst.MORPH_BUILD_STATE:
            return

        LOG_IFO('base removeSkillChangeMorphState ', summonSkillId, removedSkills, self.morphState)
        self.cell.changeMorphPreAddSkill(gameconst.MORPH_BUILD_STATE)
