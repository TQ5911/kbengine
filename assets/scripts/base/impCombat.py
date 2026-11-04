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
import skill_unlock as S_UD
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
        LOG_INFO('baseLevelUpSkill', newSkillId, oldSkillId, levelDelta)
        _skillId = dataUtils.getSkillIdByMorphState(newSkillId, self.morphState)
        ret, opUUID = self._levelUpSkill(_skillId, oldSkillId, levelDelta)
        self.updateSkillScore(opUUID)
        if ret:
            self.syncMethodCallToCrossServerBase('onLocalServerLevelUpSkill', (_skillId, oldSkillId, levelDelta))

    def _levelUpSkill(self, newSkillId, oldSkillId, levelDelta):
        LOG_INFO("_levelUpSkill", newSkillId, oldSkillId, levelDelta)
        ret, opUUID = self.buildDic.levelUp(self, newSkillId, oldSkillId, levelDelta)
        if not ret:
            LOG_INFO('skill can not levelUp', newSkillId, oldSkillId)
            return False, opUUID
        return True, opUUID

    #本服升完，跨服也会重走升级技能接口
    def onLocalServerLevelUpSkill(self, _skillId, oldSkillId, levelDelta):
        LOG_INFO('onLocalServerLevelUpSkill', _skillId, oldSkillId, levelDelta)
        self._levelUpSkill(_skillId, oldSkillId, levelDelta)
        self.updateSkillScore()

    def onChangeSkillLv(self, skillId, toLv):
        LOG_INFO('onChangeSkillLv, base, ', skillId, toLv)
        self.cell.onChangeSkillLv(skillId, toLv)

    def gmSetSkillLevel(self, skillId, targetLevel):
        """GM设置技能等级(免消耗直设, 支持回退, 不返还消耗); 铭文替换技能需传原技能ID"""
        LOG_INFO("gmSetSkillLevel", skillId, targetLevel)
        utils.traceSkill(self, 'gmSetSkillLevel.in', (skillId,),
                         'skillId=', skillId, 'targetLevel=', targetLevel,
                         'slotId=', self.buildDic.getSlotId(skillId),
                         'inLevels=', skillId in self.buildDic.skillLevels,
                         'slots=', tuple(self.buildDic.activeSkills))
        if skillId not in SSD.datas:
            LOG_ERR("gmSetSkillLevel skillId not exist", skillId)
            return False, 0, 0, 'skillId not exist'
        _skillId = dataUtils.getSkillIdByMorphState(skillId, self.morphState)
        if _skillId not in self.buildDic.skillLevels:
            LOG_ERR("gmSetSkillLevel skill not unlocked", skillId, _skillId)
            return False, 0, 0, 'skill not unlocked'
        oldLevel = self.buildDic.skillLevels[_skillId]
        maxLevel = self.buildDic.getMaxLevel(self, _skillId, _skillId)
        if targetLevel < 1 or targetLevel > maxLevel:
            LOG_ERR("gmSetSkillLevel targetLevel invalid", _skillId, targetLevel, maxLevel)
            return False, 0, 0, 'targetLevel invalid, range 1~%d' % maxLevel
        if targetLevel == oldLevel:
            return True, oldLevel, targetLevel, ''

        # 免消耗直设, 内含conflictSkill同步/召唤槽更新/onChangeSkillLv/客户端同步
        self.buildDic.updateSkillLevel(self, [(_skillId, targetLevel)])
        self.updateSkillScore()

        # 刷新新手历程技能等级缓存(与levelUp同口径)
        skillLvDatas = {}
        for skillLv in self.buildDic.skillLevels.values():
            skillLvDatas[skillLv] = skillLvDatas.get(skillLv, 0) + 1
        self.clearBeginnerJourneyBehaviorStatusEx([gameconst.BjTaskType.BJ_TASK_TYPE_SKILL_LEVEL])
        for skillLv, count in skillLvDatas.items():
            self.beginnerJourney_onTaskEvent(
                gameconst.BjTaskType.BJ_TASK_TYPE_SKILL_LEVEL,
                delta=count,
                level=skillLv)
        return True, oldLevel, targetLevel, ''

    def _isCanUnlockSkill(self, isActive, skillId, lv, mid):
        condStr = SSD.datas[skillId]['unlockCondition']

        if not condStr:
            return True

        res = self._isUIVisibleStr(condStr)
        return res

    def unlockSkill(self, isNotify, lv=0, mid=0):
        unlockedSkills = []
        _school = gameglobal.roleCache[self.id]['school']
        if _school in S_UD.datas:
            activeSkills = S_UD.datas[gameglobal.roleCache[self.id]['school']].get('data')
            for _skillIds in activeSkills:
                for skillId in _skillIds:
                    if not skillId:
                        continue
                    skillId = dataUtils.getSkillIdByMorphState(skillId, self.morphState)
                    if not self._isCanUnlockSkill(True, skillId, lv, mid):
                        utils.traceSkill(self, 'unlockSkill.conditionNotMet', (skillId,),
                                         'skillId=', skillId, 'morphState=', self.morphState,
                                         'lv=', lv, 'mid=', mid)
                        continue

                    _buildSkillId = dataUtils.getSkillIdByMorphState(skillId, gameconst.MORPH_BUILD_STATE)
                    taskId = self.checkHasUnlockedTemporarySkill(_buildSkillId)
                    if taskId:
                       self.cannelTemporarySkill(taskId, _buildSkillId)
                    else:
                        utils.traceSkill(self, 'unlockSkill.tryUnlock', (skillId,),
                                         'skillId=', skillId, 'buildSkillId=', _buildSkillId,
                                         'hasSkill=', self.hasSkill(skillId),
                                         'slots=', tuple(self.buildDic.activeSkills))
                        if self.unlockActiveSkill(_buildSkillId, skillId, isNotify, lv, mid):
                            LOG_INFO('unlock skill', skillId)
                            unlockedSkills.append(skillId)
                            utils.traceSkill(self, 'unlockSkill.unlocked', (skillId,),
                                             'skillId=', skillId,
                                             'slotId=', self.buildDic.getSlotId(skillId),
                                             'slotsAfter=', tuple(self.buildDic.activeSkills))

        if unlockedSkills:
            self.updateSkillScore()

    def unlockActiveSkill(self, _buildSkillId, skillId, isNotify, lv, mid):
        if self.hasSkill(skillId):
            # 已解锁就再也不处理槽位: 若此刻技能不在 activeSkills 里, 之后也不会被这里补上
            utils.traceSkill(self, 'unlockActiveSkill.alreadyUnlocked', (skillId, _buildSkillId),
                             'skillId=', skillId, 'buildSkillId=', _buildSkillId,
                             'slotId=', self.buildDic.getSlotId(skillId),
                             'slots=', tuple(self.buildDic.activeSkills),
                             'levels=', tuple(self.buildDic.skillLevels.keys()))
            return False

        skillLv = 1

        self.buildDic.buildAddActiveSkill(self, skillId, skillLv)

        recommendSlot = self.buildDic.getSkillRecommendSlot(self, _buildSkillId)
        if recommendSlot is not None:
            self.buildDic.changeSkillSlot(self, skillId, None, recommendSlot, reason=gameconst.CHANGE_SKILL_REASON_UNLOCK)
            utils.traceSkill(self, 'unlockActiveSkill.placed', (skillId, _buildSkillId),
                             'skillId=', skillId, 'recommendSlot=', recommendSlot,
                             'slotsAfter=', tuple(self.buildDic.activeSkills))
        else:
            utils.traceSkill(self, 'unlockActiveSkill.levelOnlyNoSlot', (skillId, _buildSkillId),
                             'skillId=', skillId, 'buildSkillId=', _buildSkillId,
                             'slots=', tuple(self.buildDic.activeSkills))

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

        utils.traceSkill(self, 'unlockTemporarySkill', (_buildSkillId, _stateSkillId),
                         'buildSkillId=', _buildSkillId, 'stateSkillId=', _stateSkillId,
                         'skillLv=', skillLv, 'slots=', tuple(self.buildDic.activeSkills))
        self.buildDic.buildAddActiveSkill(self, _stateSkillId, skillLv)
        recommendSlot = self.buildDic.getSkillRecommendSlot(self, _buildSkillId)
        if recommendSlot is not None:
            self.buildDic.changeSkillSlot(self, _stateSkillId, None, recommendSlot)

        return True

    def deleteTemporarySkill(self, _buildSkillId, _stateSkillId):
        utils.traceSkill(self, 'deleteTemporarySkill.in', (_buildSkillId, _stateSkillId),
                         'buildSkillId=', _buildSkillId, 'stateSkillId=', _stateSkillId,
                         'morphState=', self.morphState,
                         'slotOfState=', self.buildDic.getSlotId(_stateSkillId),
                         'slotOfBuild=', self.buildDic.getSlotId(_buildSkillId),
                         'slotsBefore=', tuple(self.buildDic.activeSkills))
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

        utils.traceSkill(self, 'deleteTemporarySkill.done', (_buildSkillId, _stateSkillId),
                         'buildSkillId=', _buildSkillId, 'stateSkillId=', _stateSkillId,
                         'slotsAfter=', tuple(self.buildDic.activeSkills),
                         'levelsAfter=', tuple(self.buildDic.skillLevels.keys()))

    def initNoviceBuild(self):
        pass

    def onChangeSkill(self, fromSkillId, toSkillId, fromSkillNextCastTime):
        utils.traceSkill(self, 'onChangeSkill.in', (fromSkillId, toSkillId),
                         'fromSkillId=', fromSkillId, 'toSkillId=', toSkillId,
                         'fromInLevels=', fromSkillId in self.buildDic.skillLevels,
                         'toInLevels=', toSkillId in self.buildDic.skillLevels,
                         'slotsBefore=', tuple(self.buildDic.activeSkills))
        skillIds = self.buildDic.getSkillIds()
        if toSkillId in skillIds:
            LOG_WARN("onChangeSkill toSkillId was in buildDic", fromSkillId, toSkillId, skillIds)

        slotId = self.buildDic.getSlotId(fromSkillId)
        if slotId is None:
            utils.traceSkill(self, 'onChangeSkill.fromNotInBuild', (fromSkillId, toSkillId),
                             'fromSkillId=', fromSkillId, 'toSkillId=', toSkillId)
            return

        buildVal = self.buildDic

        buildVal.changeSkillSlot(self, fromSkillId, slotId, None)
        buildVal.changeSkillSlot(self, toSkillId, None, slotId, fromSkillNextCastTime = fromSkillNextCastTime)

        self.client.onChangeSkill(fromSkillId, toSkillId)
        utils.traceSkill(self, 'onChangeSkill.done', (fromSkillId, toSkillId),
                         'fromSkillId=', fromSkillId, 'toSkillId=', toSkillId,
                         'slotId=', slotId, 'slotsAfter=', tuple(self.buildDic.activeSkills))

    def buildAddActiveSkill(self, skillId, skillLv):
        if skillId in self.buildDic.skillLevels:
            skillLv = self.buildDic.skillLevels[skillId]
        utils.traceSkill(self, 'buildAddActiveSkill', (skillId,),
                         'skillId=', skillId, 'skillLv=', skillLv,
                         'slotId=', self.buildDic.getSlotId(skillId),
                         'slots=', tuple(self.buildDic.activeSkills))
        self.buildDic.doAddActiveSkill(self, skillId, skillLv)
        self.client.onUpdateSkillLevel([skillId], [skillLv])

    def hasSkill(self, skillId):
        return skillId in self.buildDic.skillLevels

    # 拖技能到build
    @gamedecorator.crossServer
    def updateSkills(self, exposed, skillSlotInfos):
        LOG_INFO("updateSkills ", skillSlotInfos)
        self._updateSkills(skillSlotInfos, True, True)
        self.syncMethodCallToLocalServerBase('onCrossServerUpdateSkills', (skillSlotInfos,))

    def onCrossServerUpdateSkills(self, skillSlotInfos):
        LOG_INFO('onCrossServerUpdateSkills', skillSlotInfos)
        self._updateSkills(skillSlotInfos, True, True)

    def _updateSkills(self, skillSlotInfos, bNotifyClient=False, isMessage=False):
        # 客户端拖拽原始请求: 这里能看到客户端到底发了什么 skillId/slotId, 是定位数据脱钩的源头
        _reqSkillIds = []
        for _slotInfo in skillSlotInfos or ():
            try:
                _reqSkillIds.append(_slotInfo.get('skillId'))
            except Exception:
                pass
        utils.traceSkill(self, '_updateSkills.request', _reqSkillIds,
                         'raw=', skillSlotInfos, 'morphState=', self.morphState,
                         'slotsBefore=', tuple(self.buildDic.activeSkills),
                         'levels=', tuple(self.buildDic.skillLevels.keys()))

        skillCheckList = []
        for skillSlotInfo in skillSlotInfos:
            skillId = skillSlotInfo['skillId']
            # 需要处理下冲突技能
            skillId = dataUtils.getSkillIdByMorphState(skillId, self.morphState)
            toSlotId = skillSlotInfo['slotId']
            if toSlotId < 0:
                toSlotId = None

            utils.traceSkill(self, '_updateSkills.item', (_reqSkillIds[0] if _reqSkillIds else skillId, skillId),
                             'rawSkillId=', skillSlotInfo.get('skillId'), 'skillId=', skillId,
                             'toSlot=', toSlotId, 'morphState=', self.morphState,
                             'inLevels=', skillId in self.buildDic.skillLevels,
                             'isRightSlot=', self.buildDic.isRightSlot(skillId, toSlotId))

            if not self.buildDic.isRightSlot(skillId, toSlotId):
                utils.traceSkill(self, '_updateSkills.isRightSlotFail', (skillId,),
                                 'skillId=', skillId, 'toSlot=', toSlotId,
                                 'slots=', tuple(self.buildDic.activeSkills))
                return

            toSkillId = self.getSkillIdBySlotId(toSlotId)
            skillCheckList.append((toSkillId, skillId, toSlotId))

        self.onCheckUpdateSkillRet(True, skillCheckList, bNotifyClient, isMessage)

    def onCheckUpdateSkillRet(self, bCanUpdate, skillSlotInfos, bNotifyClient=False, isMessage=False):
        updateResult = {}
        if bCanUpdate:
            for skillSlotInfo in skillSlotInfos:
                _, skillId, toSlotId = skillSlotInfo
                if toSlotId < 0:
                    toSlotId = None

                fromSlotId = self.buildDic.getSlotId(skillId)
                currentSkillId = self.getSkillIdBySlotId(toSlotId)

                _buildVal = self.buildDic
                # 注意 inLevels 二元组: (目标槽现有技能是否在等级表, 要拖入的技能是否在等级表)。
                # 第二个为 False 时, 下面 skillLevels[skillId] 会抛 KeyError,
                # 而此时 changeSkillSlot(current->to) 已经执行过, 会留下空槽。
                utils.traceSkill(self, 'onCheckUpdateSkillRet.item', (skillId, currentSkillId),
                                 'skillId=', skillId, 'currentSkillId=', currentSkillId,
                                 'fromSlot=', fromSlotId, 'toSlot=', toSlotId,
                                 'inLevels=', (currentSkillId in _buildVal.skillLevels, skillId in _buildVal.skillLevels),
                                 'slotsBefore=', tuple(_buildVal.activeSkills))

                if currentSkillId:
                    _buildVal.changeSkillSlot(self, currentSkillId, toSlotId, fromSlotId)
                    if len(skillSlotInfos) == 1:
                        currentSkillLevel = _buildVal.skillLevels[currentSkillId]
                        skillLevel = _buildVal.skillLevels[skillId]
                        skillLevelList = [(skillId, currentSkillLevel)]
                        skillLevelList.append((currentSkillId, skillLevel))
                        _buildVal.updateSkillLevel(self, skillLevelList)

                _buildVal.changeSkillSlot(self, skillId, fromSlotId, toSlotId)

                if fromSlotId is not None:
                    updateResult[fromSlotId] = _buildVal.activeSkills[fromSlotId]
                if toSlotId is not None:
                    updateResult[toSlotId] = _buildVal.activeSkills[toSlotId]

                utils.traceSkill(self, 'onCheckUpdateSkillRet.done', (skillId, currentSkillId),
                                 'skillId=', skillId, 'currentSkillId=', currentSkillId,
                                 'slotsAfter=', tuple(_buildVal.activeSkills))

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
            _detail = gameclass.AwardDetailCls()
            self.deductWealth(_src, _deductVal, opUUID, _detail)
            _showList = _deductVal.toBriefList()
        now = 0
        if expChange:
            _toClientData, now = self.deathPenaltyData.addDeathPenaltyExp(expChange)
            if _toClientData:
                self.client.onDeathPenaltyExpChange(_toClientData)

            _showList.append({'itemId': gameconst.ItemIdEnum.EXP, 'itemNum': expChange, 'bindType': gameconst.ItemBindType.BIND})

        self.client.onDeathPenaltyReward(killerGbId, killerName, _showList, killerData)
        self.syncMethodCallToCrossServerBase('_addDeathPenaltyVal', (expChange, coinChange, killerGbId, killerName, opUUID, killerData, now))

    def _addDeathPenaltyVal(self, expChange, coinChange, killerGbId, killerName, opUUID, killerData, timestamp):
        _showList = []
        if coinChange:
            _src = AAC_AACDD.datas.BONUS_SRC_DEAD_PENALTY # TODO: DEAD_PENALTY
            _coin = min(coinChange, self.coin)
            _deductVal = dropAward.DeductWealthVal(coin=_coin) # TODO: DEAD_PENALTY
            _detail = gameclass.AwardDetailCls()
            self.deductWealth(_src, _deductVal, opUUID, _detail)
            _showList = _deductVal.toBriefList()

        if expChange:
            _toClientData, now = self.deathPenaltyData.addDeathPenaltyExp(expChange, timestamp)
            if _toClientData:
                self.client.onDeathPenaltyExpChange(_toClientData)

            _showList.append({'itemId': gameconst.ItemIdEnum.EXP, 'itemNum': expChange, 'bindType': gameconst.ItemBindType.BIND})

        self.client.onDeathPenaltyReward(killerGbId, killerName, _showList, killerData)

    def refreshFreeRecoverDeathPenaltyTimes(self, *args):
        self.freeRecoverDeathPenaltyTimes = GP_SD.datas['freeExpRecCount']['value']

    @gamedecorator.crossServer
    def recoverDeathPenaltyExp(self, exposed, expireTime, itemId, isExchange=False):
        if gameconfig.isCrossServer():
            self.syncMethodCallToLocalServerBase('_recoverDeathPenaltyExp', (expireTime, itemId, isExchange))
        else:
            self._recoverDeathPenaltyExp(expireTime, itemId, isExchange=isExchange)

    def _recoverDeathPenaltyExp(self, expireTime, itemId, isExchange=False):
        LOG_INFO('recoverDeathPenaltyExp:', expireTime, itemId)
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
            if itemId == gameconst.ItemIdEnum.COIN:
                _formulaId = GP_SD.datas['normalExpRecCost']['value']
                _num = F_GFD.datas[_formulaId]['serverFormula'](_exp)
                _ratio = GP_SD.datas['normalExpRecPct']['value']
            elif itemId == gameconst.ItemIdEnum.BIND_MONEY:
                _formulaId = GP_SD.datas['advancedExpRecCost']['value']
                _num = F_GFD.datas[_formulaId]['serverFormula'](_exp)
                _ratio = GP_SD.datas['advancedExpRecPct']['value']
            else:
                LOG_ERR('recoverDeathPenaltyExp itemId invalid:', itemId, self.gbID)
                return

            _src = AAC_AACDD.datas.BONUS_SRC_RECOVER_DEAD_PENALTY_DEDUCT
            _deductVal = dropAward.DeductWealthVal()
            _deductVal.addWealthByItemId(itemId, _num)
            res = self.canDeductWealth(_deductVal, sendMsg=True, allowMoneyCoverBindMoney=isExchange)
            if not res:
                LOG_WARN('recoverDeathPenaltyExp canDeductWealth failed:', self.gbID, res())
                return

            self.deductWealth(_src, _deductVal, _opUUID, gameclass.AwardDetailCls(), allowMoneyCoverBindMoney=isExchange)

        self.deathPenaltyData.removeDeathPenaltyVal(expireTime)

        _src = AAC_AACDD.datas.BONUS_SRC_RECOVER_DEAD_PENALTY
        _awardVal = dropAward.AwardVal(exp=int(_exp * _ratio))
        self.addWealth(_src, _awardVal, _opUUID, gameclass.AwardDetailCls())

        self.client.onDeathPenaltyExpChange([{"expireTime": expireTime, "exp": 0}])
        self.syncMethodCallToCrossServerBase('_recoverDeathPenaltyExp', (expireTime, itemId))

    @gamedecorator.crossServer
    def removeDeathPenaltyExp(self, exposed, expireTime):
        if gameconfig.isCrossServer():
            self.syncMethodCallToLocalServerBase('_removeDeathPenaltyExp', (expireTime,))
        else:
            self._removeDeathPenaltyExp(expireTime)

    def _removeDeathPenaltyExp(self, expireTime):
        LOG_INFO('removeDeathPenaltyExp:', expireTime)
        if self.deathPenaltyData.removeDeathPenaltyVal(expireTime):
            self.client.onDeathPenaltyExpChange([{"expireTime": expireTime, "exp": 0}])
            self.syncMethodCallToCrossServerBase('_removeDeathPenaltyExp', (expireTime,))

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
        self.onUpdateUseCoinTimesTicketInfo(newLv)

    def playerDeadTlog(self, tlogProps):
        pass

    def playerReliveTlog(self, tlogProps):
        pass

    def addAwardFightProps(self, fightProps, srcType, awardId, opUUID, detail):
        _syncPropList = []
        for propName, val in fightProps:
            fpData = FPDD.datas.get(propName)
            if not fpData:
                LOG_ERR('addAwardFightProps name invalid:', propName, val)
                continue

            if fpData['formulaPlayer']:
                LOG_ERR('addAwardFightProps prop be rely on:', propName, val)
                continue

            self.awardFightPropDic[propName] = self.awardFightPropDic.get(propName, 0) + val
            _syncPropList.append((propName, val))

        self.cell.addAwardFightPropsCell(_syncPropList, opUUID)

    def sendServerLevel(self, serverLevel=0):
        serverLevel = serverLevel or utils.getServerLevel()

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
        if unlockedSkills:
            self.updateSkillScore()

        self.sendCliSkillBuildInfo()

    def initRemoveTemporarySkill(self):
        removeTaskIds = list(self.tmpTaskSkillIds.keys())
        for taskId in removeTaskIds:
            self.deleteTemporarySkillByTask(taskId)

    # 变身状态 start ---------------------------------

    def changeMorphStateBase(self, morphState):
        if morphState == self.morphState:
            # base 侧形态已是目标值就直接返回: 若槽里残留的是另一形态的技能, 这里不会修正
            utils.traceSkill(self, 'changeMorphStateBase.sameState',
                             tuple(self.buildDic.activeSkills) + tuple(self.buildDic.skillLevels.keys()),
                             'morphState=', morphState,
                             'slots=', tuple(self.buildDic.activeSkills))
            return

        utils.traceSkill(self, 'changeMorphStateBase.in',
                         tuple(self.buildDic.activeSkills) + tuple(self.buildDic.skillLevels.keys()),
                         'from=', self.morphState, 'to=', morphState,
                         'slotsBefore=', tuple(self.buildDic.activeSkills),
                         'levels=', tuple(self.buildDic.skillLevels.keys()))

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

            utils.traceSkill(self, 'changeMorphStateBase.swapSlot', (_skillId, _newSkillId),
                             'slotId=', _slotId, 'oldSkillId=', _skillId, 'newSkillId=', _newSkillId,
                             'oldInLevels=', _skillId in self.buildDic.skillLevels,
                             'newInLevels=', _newSkillId in self.buildDic.skillLevels)

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

        utils.traceSkill(self, 'changeMorphStateBase.done',
                         tuple(self.buildDic.activeSkills) + tuple(self.buildDic.skillLevels.keys()),
                         'morphState=', morphState,
                         'slotsAfter=', tuple(self.buildDic.activeSkills),
                         'levelsAfter=', tuple(self.buildDic.skillLevels.keys()))

    # 变身状态 end ---------------------------------

    # 快捷吃药 start ---------------------------------

    @gamedecorator.checkGameconfigEnable('quickSettings')
    @gamedecorator.crossServer
    def setInstantPotionSlots(self, exposed, potion):
        self._setInstantPotionSlots(potion)
        self.syncMethodCallToLocalServerBase('_setInstantPotionSlots', (potion,))


    def _setInstantPotionSlots(self, potion):
        LOG_INFO('setInstantPotionSlots', potion)
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
    @gamedecorator.crossServer
    def unsetInstantPotionSlots(self, exposed, slotId):
        if gameconfig.isCrossServer():
            self.syncMethodCallToLocalServerBase('_unsetInstantPotionSlots', (slotId,))
        self._unsetInstantPotionSlots(slotId)

    def _unsetInstantPotionSlots(self, slotId):
        LOG_INFO('unsetInstantPotionSlots', slotId)
        self.instantPotionSlots.unsetSlot(slotId)

        self.client.onRemoveInstantPotionSlots(slotId)

    def autoHealHp(self):
        for potion in self.instantPotionSlots.slots:
            if not potion.isHp():
                continue

            if not utils.bhas(potion.potionState, gameconst.PotionState.AUTO):
                continue

            if self.useItemWithActionInternal(
                    gameconst.BagTypeEnum.BAG_TYPE_NORMAL,
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
                    gameconst.BagTypeEnum.BAG_TYPE_NORMAL,
                    potion.itemId,
                    self.id):
                break

    # 快捷吃药 end ---------------------------------

    def initSummonSlotIdx(self):
        LOG_INFO('initSummonSlotIdx', self.summonSlotIdxBase)
        self.cell.setSummonSlotIdx(self.summonSlotIdxBase)

    @gamedecorator.crossServer
    def setSummonSlotIdx(self, exposed, slotIdx):
        self._setSummonSlotIdx(slotIdx)
        self.syncMethodCallToLocalServerBase('_setSummonSlotIdx', (slotIdx,))

    def _setSummonSlotIdx(self, slotIdx):
        if slotIdx == self.summonSlotIdxBase:
            LOG_INFO('base setSummonSlotIdx same idx', slotIdx)
            return

        school = gameglobal.roleCache[self.id]['school']
        summonSkillIds = SRSC.datas['summonSkillId'].get('valueCN', (0,))
        summonSchool = SRSC.datas['usePlayerForSummon'].get('valueCN', 0)
        skillLevel = 0
        for summonSkillId in summonSkillIds:
            skillLevel = max(skillLevel, self.buildDic.getSkillLevel(summonSkillId))
        LOG_INFO('base setSummonSlotIdx', slotIdx, self.summonSlotIdxBase, school, skillLevel)
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
        LOG_DBG("updateSkillLevelSetSummonSlotIdx", skillId, skillLevel)
        school = gameglobal.roleCache[self.id]['school']
        summonSkillIds = SRSC.datas['summonSkillId'].get('valueCN', (0,))
        summonSchool = SRSC.datas['usePlayerForSummon'].get('valueCN', 0)
        if school != summonSchool or skillId not in summonSkillIds:
            return

        if self.summonSlotIdxBase == 0:
            LOG_INFO('base updateSkillLevelSetSummonSlotIdx1', skillId, skillLevel)
            self._setSummonSlotIdx(SRSU.minKey)
            return

        slotIdx = 0
        for idx in range(self.summonSlotIdxBase, 0, -1):
            if skillLevel >= SRSU.datas[idx].get('UnlockLevel', 0):
                slotIdx = idx
                break

        if slotIdx == self.summonSlotIdxBase:
            return

        LOG_INFO('base updateSkillLevelSetSummonSlotIdx2', self.summonSlotIdxBase, slotIdx, skillId, skillLevel)
        self.cell.setSummonSlotIdx(slotIdx)

    def setSummonSlotIdxAck(self, slotIdx):
        LOG_INFO('base setSummonSlotIdxAck', self.summonSlotIdxBase, slotIdx)
        self.summonSlotIdxBase = slotIdx

    def removeSkillSetSummonSlotIdx(self, removedSkills):
        school = gameglobal.roleCache[self.id]['school']
        summonSkillIds = SRSC.datas['summonSkillId'].get('valueCN', (0,))
        summonSchool = SRSC.datas['usePlayerForSummon'].get('valueCN', 0)
        if school != summonSchool or set(removedSkills).isdisjoint(set(summonSkillIds)):
            return

        LOG_INFO('base removeSkillSetSummonSlotIdx ', self.summonSlotIdxBase, removedSkills)
        self.summonSlotIdxBase = 0
        self.cell.setSummonSlotIdx(0)

    def removeSkillChangeMorphState(self, removedSkills):
        school = gameglobal.roleCache[self.id]['school']
        summonSkillIds = SRSC.datas['summonSkillId'].get('valueCN', (0,))
        summonSchool = SRSC.datas['usePlayerForSummon'].get('valueCN', 0)
        if school != summonSchool or set(removedSkills).isdisjoint(set(summonSkillIds)):
            return
        if self.morphState == gameconst.MORPH_BUILD_STATE:
            return

        LOG_INFO('base removeSkillChangeMorphState ', summonSkillIds, removedSkills, self.morphState)
        self.cell.changeMorphPreAddSkill(gameconst.MORPH_BUILD_STATE)
