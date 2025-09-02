# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine

import gameconst
import gamedecorator
import dropAward
import utils
import json
import ServerBuilds
import gameglobal
import gametlog
import time
import actionContext
import gametimer

import skill_skill as SSD
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import skill_unlock as SUD
import fightProp_define as FPDD
import const_const as CONST
import skillRelevant_summonUnlock as SRSU
import skillRelevant_skillConst as SRSC
import gamelog
import gameconfig
import gameclass
import gamePlay_set as GP_SD
import formula_generalFormula as F_GFD
import dataUtils
import itemData_itemData as ID_IDD
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
    def levelUpSkill(self, skillId, levelDelta):
        INFO_MSG('levelUpSkill', skillId, levelDelta)
        _skillId = dataUtils.getSkillIdByMorphState(skillId, self.morphState)
        self._levelUpSkill(_skillId, levelDelta)
        self.updateSkillScore()

    def _levelUpSkill(self, skillId, levelDelta):
        DEBUG_MSG("_levelUpSkill", skillId, levelDelta)
        if not self.buildDic.levelUp(self, skillId, levelDelta):
            INFO_MSG('skill can not levelUp', skillId)
            return False

        self.makeSkillTlog(1 if levelDelta > 0 else 2, skillId, self.buildDic.skillLevels[skillId])
        self.achievementInfo.triggerAchieveByType(
            self,
            gameconst.AchieveType.LEVEL_UP_SKILL,
            actionContext.AchievementCtx())
        return True

    def makeSkillTlog(self, skillChangeType, skillId, skillLevel):
        tlogProps = {
            'GameSvrId': None,
            'dtEventTime': None,
            'vGameAppid': None,
            'skillChangeType': skillChangeType,
            'skillId': skillId,
            'skillLevel': skillLevel,
        }
        # tlogProps.update(self.getTLogCommonParams())
        # gametlog.build(gameconst.GameLog.LOG_AVATAR_SKILL, **tlogProps).init().commit()

    def onChangeSkillLv(self, skillId, toLv):
        self.cell.onChangeSkillLv(skillId, toLv)

    def _isCanUnlockSkill(self, isActive, skillId, lv, mid):
        condStr = SSD.datas[skillId]['unlockCondition']

        if not condStr:
            return True

        return self.isUIVisible(condStr)

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

                    if self.unlockActiveSkill(skillId, isNotify, lv, mid):
                        DEBUG_MSG('unlock skill', skillId)
                        unlockedSkills.append(skillId)

        if unlockedSkills:
            self.client.onUnlockSkills(unlockedSkills)
            self.updateSkillScore()

    def unlockActiveSkill(self, skillId, isNotify, lv, mid):
        if self.hasSkill(skillId):
            return False

        if not self._isCanUnlockSkill(True, skillId, lv, mid):
            return False

        skillLv = 1

        self.buildDic.buildAddActiveSkill(self, skillId, skillLv)

        _buildSkillId = dataUtils.getSkillIdByMorphState(skillId, gameconst.MORPH_BUILD_STATE)
        recommendSlot = self.buildDic.getSkillRecommendSlot(self, _buildSkillId)
        if recommendSlot is not None:
            self.buildDic.changeSkillSlot(self, skillId, None, recommendSlot)

        return True

    def initNoviceBuild(self):
        pass

    def onChangeSkill(self, fromSkillId, toSkillId):
        skillIds = self.buildDic.getSkillIds()
        if toSkillId in skillIds:
            WARNING_MSG("onChangeSkill toSkillId was in buildDic", fromSkillId, toSkillId, skillIds)

        slotId = self.buildDic.getSlotId(fromSkillId)
        if slotId is None:
            return

        buildVal = self.buildDic

        buildVal.changeSkillSlot(self, fromSkillId, slotId, None)
        buildVal.changeSkillSlot(self, toSkillId, None, slotId)

        self.client.onChangeSkill(fromSkillId, toSkillId)

    def buildAddActiveSkill(self, skillId, skillLv):
        self.buildDic.doAddActiveSkill(self, skillId, skillLv)
        self.client.onUpdateSkillLevel([skillId], [skillLv])

    def hasSkill(self, skillId):
        return skillId in self.buildDic.skillLevels

    # 拖技能到build
    @gamedecorator.crossServer
    def updateSkills(self, skillSlotInfos):
        INFO_MSG("updateSkills ", skillSlotInfos)
        self._updateSkills(skillSlotInfos, True, True)

    def _updateSkills(self, skillSlotInfos, bNotifyClient=False, isMessage=False):

        skillCheckList = []
        for skillSlotInfo in skillSlotInfos:
            skillId = skillSlotInfo['skillId']
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
    def onReliveDirectly(self, needBindCoin, resId):
        if resId == gameconst.ItemId.BINDING_MONEY:
            deductWealthVal = dropAward.DeductWealthVal(bindingMoney=needBindCoin)
        else:
            deductWealthVal = dropAward.DeductWealthVal(bindingCoin=needBindCoin)

        if not self.canDeductWealth(deductWealthVal, sendMsg=True):
            return

        reliveType = gameconst.RELIVE_TYPE_DIRECTLY
        opUUID = KBEngine.genUUID64()
        src = AAC_AACDD.datas.BONUS_SRC_RELIVE
        detail = gameclass.AwardDetail(reliveType=reliveType)
        self.deductWealth(src, deductWealthVal, opUUID, detail)
        self.cell.doRelive(reliveType)

    def addDeathPenaltyVal(self, expChange, coinChange, killerGbId, killerName, opUUID, killerData):
        _showList = []
        if coinChange:
            _src = AAC_AACDD.datas.BONUS_SRC_DEAD_PENALTY # TODO: DEAD_PENALTY
            _coin = min(coinChange, self.coin)
            _deductVal = dropAward.DeductWealthVal(coin=_coin) # TODO: DEAD_PENALTY
            _detail = gameclass.AwardDetail()
            self.deductWealth(_src, _deductVal, opUUID, _detail)
            _showList = _deductVal.toShowList()

        if expChange:
            _toClientData = self.deathPenaltyData.addDeathPenaltyExp(expChange)
            if _toClientData:
                self.client.onDeathPenaltyExpChange(_toClientData)

            _showList.append({'itemId': gameconst.ItemId.EXP, 'itemNum': expChange})

        self.client.onDeathPenaltyReward(killerGbId, killerName, _showList, killerData)

    def refreshFreeRecoverDeathPenaltyTimes(self):
        self.freeRecoverDeathPenaltyTimes = GP_SD.datas['freeExpRecCount']['value']

    def recoverDeathPenaltyExp(self, expireTime, itemId):
        INFO_MSG('recoverDeathPenaltyExp:', expireTime, itemId)
        if expireTime < utils.getNow():
            ERROR_MSG('recoverDeathPenaltyExp expireTime invalid:', expireTime, self.gbID)
            return

        _exp = self.deathPenaltyData.getDeathPenaltyExp(expireTime)
        if not _exp:
            ERROR_MSG('recoverDeathPenaltyExp not found:', expireTime, self.gbID)
            return

        _opUUID = KBEngine.genUUID64()
        _ratio = 1
        if itemId == 0:
            if self.freeRecoverDeathPenaltyTimes <= 0:
                ERROR_MSG('recoverDeathPenaltyExp freeRecoverDeathPenaltyTimes:', self.gbID)
                return

            self.freeRecoverDeathPenaltyTimes -= 1
            _ratio = GP_SD.datas['freeExpRecPct']['value']
        else:
            if itemId == gameconst.ItemId.COIN:
                _formulaId = GP_SD.datas['normalExpRecCost']['value']
                _num = F_GFD.datas[_formulaId]['serverFormula'](_exp)
                _ratio = GP_SD.datas['normalExpRecPct']['value']
            elif itemId == gameconst.ItemId.MONEY:
                _formulaId = GP_SD.datas['advancedExpRecCost']['value']
                _num = F_GFD.datas[_formulaId]['serverFormula'](_exp)
                _ratio = GP_SD.datas['advancedExpRecPct']['value']
            else:
                ERROR_MSG('recoverDeathPenaltyExp itemId invalid:', itemId, self.gbID)
                return

            _src = AAC_AACDD.datas.BONUS_SRC_RECOVER_DEAD_PENALTY_DEDUCT
            _deductVal = dropAward.DeductWealthVal()
            _deductVal.addWealthByItemId(itemId, _num)
            if not self.canDeductWealth(_deductVal, sendMsg=True):
                ERROR_MSG('recoverDeathPenaltyExp canDeductWealth failed:', self.gbID)
                return

            self.deductWealth(_src, _deductVal, _opUUID, gameclass.AwardDetail())

        self.deathPenaltyData.removeDeathPenaltyVal(expireTime)

        _src = AAC_AACDD.datas.BONUS_SRC_RECOVER_DEAD_PENALTY
        _awardVal = dropAward.AwardVal(exp=int(_exp * _ratio))
        self.addWealth(_src, _awardVal, _opUUID, gameclass.AwardDetail())

        self.client.onDeathPenaltyExpChange([{"expireTime": expireTime, "exp": 0}])

    def removeDeathPenaltyExp(self, expireTime):
        INFO_MSG('removeDeathPenaltyExp:', expireTime)
        if self.deathPenaltyData.removeDeathPenaltyVal(expireTime):
            self.client.onDeathPenaltyExpChange([{"expireTime": expireTime, "exp": 0}])

    # ------------------- dead and relive end -------------------

    def onAvatarLevelUpBase(self, oldLv, newLv):
        self.onTaskAvatarLvUp(oldLv, newLv)
        # self._modifyRedisAttr({'level': newLv})
        self.accountEntity.updateCharacterLevel(self.gbID, newLv, self.tLoginBase)

        self.checkUnlockBuildAndSkillByLevel(True, newLv)

        self.lastLevelupTime = utils.getNow()
        self._modifyRedisAttr({'level': newLv})

        self.guildBox and self.guildBox.onGuildMemberPropUpdate(self.gbID, 'level', newLv)
        self.propChangedTimes[gameconst.LeaderBoardType.AVATAR_LEVEL] = utils.getNow()

        self.achievementInfo.onLvUpAchievement(oldLv, newLv, self)
        self.checkAndUnlockWelfareSignIn()
        self.checkUnlockBountyTask()

    def playerDeadTlog(self, tlogProps):
        pass
        # tlogProps.update(self.getTLogCommonParams())
        # gametlog.build(gameconst.GameLog.LOG_AVATAR_DEAD, **tlogProps).init().commit()

    def playerReliveTlog(self, tlogProps):
        pass
        # tlogProps.update(self.getTLogCommonParams())
        # gametlog.build(gameconst.GameLog.LOG_AVATAR_RELIVE, **tlogProps).init().commit()

    def addAwardFightProps(self, fightProps, srcType, awardId, opUUID, detail):
        syncPropList = []
        logStrs = []
        for propName, val in fightProps:
            fpData = FPDD.datas.get(propName)
            if not fpData:
                ERROR_MSG('addAwardFightProps name invalid:', propName, val)
                continue

            if fpData['formulaPlayer']:
                ERROR_MSG('addAwardFightProps prop be rely on:', propName, val)
                continue

            self.awardFightPropDic[propName] = self.awardFightPropDic.get(propName, 0) + val
            syncPropList.append((propName, val))
            # relatedKey = fpData['relatedKey']
            # relatedName = FPDD.datas[relatedKey]['name']
            # if fpData['isPercent']:
            #     valStr = f'{int(val * 100)}%'
            # else:
            #     valStr = str(val)
            #
            # logStrs.append('{}:{}'.format(propName, val))
            #
            # self.onMessagePre(WYS_CD.datas['msgId_tuJian_getFightProp']['value'], [relatedName, valStr])

        self.cell.addAwardFightPropsCell(syncPropList)
        # gamelog.makeAddAwardFightPropsLog(self, srcType, awardId, opUUID, str(detail), ','.join(logStrs))

    def sendServerLevel(self, serverLevel=0):
        serverLevel = serverLevel or utils.getServerLevel()
        self.client.onGetServerLevel(serverLevel)

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
            'iTime': utils.getNow() - self.lastLevelupTime if oldLevel != newLevel else 0,
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

    def onKillOtherAvatar(self, gbId, spaceNo):
        if gbId == self.gbID:
            return

        self.enemyMgr.onKillOtherAvatarRecord(self, gbId, spaceNo)

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

    def setInstantPotionSlots(self, potion):
        INFO_MSG('setInstantPotionSlots', potion)
        _oldAutoHealHp = self.instantPotionSlots._hasAutoHealHp()
        _oldAutoHealMp = self.instantPotionSlots._hasAutoHealMp()
        if not self.instantPotionSlots.updateSlot(self, potion):
            ERROR_MSG('setInstantPotionSlots failed', self.gbID)
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

    def unsetInstantPotionSlots(self, slotId):
        INFO_MSG('unsetInstantPotionSlots', slotId)
        self.instantPotionSlots.unsetSlot(slotId)

        self.client.onRemoveInstantPotionSlots(slotId)

    def autoHealHp(self):
        for potion in self.instantPotionSlots.slots:
            if not potion.isHp():
                continue

            if not utils.hasBit(potion.potionState, gameconst.PotionState.AUTO):
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

            if not utils.hasBit(potion.potionState, gameconst.PotionState.AUTO):
                continue

            if self.useItemWithActionInternal(
                    gameconst.BagType.BAG_TYPE_NORMAL,
                    potion.itemId,
                    self.id):
                break

    # 快捷吃药 end ---------------------------------

    def initSummonSlotIdx(self):
        INFO_MSG('initSummonSlotIdx', self.summonSlotIdxBase)
        self.cell.setSummonSlotIdx(self.summonSlotIdxBase)

    def setSummonSlotIdx(self, slotIdx):
        if slotIdx == self.summonSlotIdxBase:
            INFO_MSG('base setSummonSlotIdx same idx', slotIdx)
            return

        school = gameglobal.roleCache[self.id]['school']
        summonSkillId = SRSC.datas['summonSkillId'].get('valueCN', 0)
        summonSchool = SRSC.datas['usePlayerForSummon'].get('valueCN', 0)
        skillLevel = self.buildDic.getSkillLevel(summonSkillId)
        INFO_MSG('base setSummonSlotIdx', slotIdx, self.summonSlotIdxBase, school, skillLevel)
        if school != summonSchool:
            ERROR_MSG('base setSummonSlotIdx school error', school, summonSchool)
            return
        if slotIdx <= 0 or slotIdx > SRSU.maxKey:
            ERROR_MSG('base setSummonSlotIdx slotIdx error', slotIdx)
            return
        if skillLevel < SRSU.datas[slotIdx].get('UnlockLevel', 0):
            ERROR_MSG('base setSummonSlotIdx unlock', skillLevel, SRSU.datas[slotIdx])
            return

        self.cell.setSummonSlotIdx(slotIdx)

    def updateSkillLevelSetSummonSlotIdx(self, skillId, skillLevel):
        school = gameglobal.roleCache[self.id]['school']
        summonSkillId = SRSC.datas['summonSkillId'].get('valueCN', 0)
        summonSchool = SRSC.datas['usePlayerForSummon'].get('valueCN', 0)
        if school != summonSchool or skillId != summonSkillId:
            return

        if self.summonSlotIdxBase == 0:
            INFO_MSG('base updateSkillLevelSetSummonSlotIdx1', skillId, skillLevel)
            self.setSummonSlotIdx(SRSU.minKey)
            return

        slotIdx = 0
        for idx in range(self.summonSlotIdxBase, 0, -1):
            if skillLevel >= SRSU.datas[idx].get('UnlockLevel', 0):
                slotIdx = idx
                break

        if slotIdx == self.summonSlotIdxBase:
            return

        INFO_MSG('base updateSkillLevelSetSummonSlotIdx2', self.summonSlotIdxBase, slotIdx, skillId, skillLevel)
        self.cell.setSummonSlotIdx(slotIdx)

    def setSummonSlotIdxAck(self, slotIdx):
        INFO_MSG('base setSummonSlotIdxAck', self.summonSlotIdxBase, slotIdx)
        self.summonSlotIdxBase = slotIdx
