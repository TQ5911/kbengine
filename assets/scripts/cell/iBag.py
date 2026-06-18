# -*- encoding:utf-8 -*-
from KBEDebug import *
import KBEngine
import math
import sMath
import utils
import gameconst
import gameengine
import gamedecorator
from collections.abc import Iterable

import itemData_itemData as ID_IDD
import message_Message_def as M_M_DD
import conflict_conflict_def as C_C_DD
import NPC_pickConst as NPCST
import const_const as C_CD
import NPC_Pick as NPD
import login_set as L_SD
import bagData_set as BD_SD
import gamePlay_gamePlay as GPGPD
import gamePlay_singleSceneData as GPSSDD
import gamePlay_set as GPSD
import PKData_PKData as PKD
import gearBase_gearBase as GBGBD
import LogTrackingMgr

import actionContext
import dataUtils
import formula
import gametimer
import random
import awardContext
import gameconfig


class IBag(object):

    @gamedecorator.checkGameconfigEnable('bag')
    @gamedecorator.crossServer
    @utils.isMyself
    def reqUseItems(self, exposed, bagType, gridId, itemId, targetId, useNum, argsList):
        LOG_INFO('ckz: reqUseItems', bagType, gridId, itemId, targetId, argsList, useNum)
        if useNum <= 0:
            return

        if not targetId:
            targetId = self.id

        if itemId not in ID_IDD.datas:
            LOG_ERR('ckz: item id %d is invalid' % itemId)
            return

        if not self.checkConflictState(C_C_DD.datas.useItem):
            LOG_WARN('   in reqUseItems, checkConflictState failed')
            return

        itemData = ID_IDD.datas[itemId]
        # 检查职业限定
        checkClass = itemData['class']
        if isinstance(checkClass, Iterable):
            if self.school not in checkClass:
                LOG_WARN('   in reqUseItems, class check failed')
                return
        else:
            if checkClass != 0 and checkClass != self.school:
                LOG_WARN('   in reqUseItems, class check failed')
                return

        if not itemData['use']:
            LOG_WARN('   in reqUseItems, item can not use')
            return

        if useNum > 1 and not itemData['batchUse']:
            LOG_WARN('   in reqUseItems, item can not batch use')
            return

        if useNum > BD_SD.datas['itemBatchUseUpLimit']['value']:
            LOG_WARN('in reqUseItems, use items num reach uplimit:', useNum)
            useNum = BD_SD.datas['itemBatchUseUpLimit']['value']

        _useItemCtx = actionContext.UseItemCtx(targetId, argsList)
        if itemData['subType'] in (gameconst.ItemSubType.Normal,):
            _useItemCtx = actionContext.UseBoxTypeItemCtx(targetId, argsList)

        #检查跨服是否可以使用
        if gameconfig.isCrossServer():
            if not itemData['ifCrossServer']:
                LOG_ERR('in reqUseItems, item can not use in cross server')
                return
            _useItemCtx.isCrossServerUseItem = True

        checkFunc = itemData['conditionCheckAction']
        if checkFunc:
            # 物品check函数只能返回三个值,其他值会报错：
            # gameconst.UseItemEnum.FALSE：   检查失败，使用过程将中断
            # gameconst.UseItemEnum.TRUE：    检查成功，将去base进程锁定背包扣除数量，再在cell进程执行物品action
            # gameconst.UseItemEnum.PENDING： 不能立即得出结果，即要异步检查，这个时候需要先调用setPendingCheckId再返回PENDING
            #                            调用setPendingCheckId会获得一个pendingId，等检查得出结果时，再调用cell部分的onPendingCheckItem
            #                            函数告知检查的结果，此时只能是TRUE/FALSE
            _checkResult = checkFunc(self, gridId, itemId, useNum, _useItemCtx)
            if _checkResult == gameconst.UseItemEnum.FALSE:
                return
            elif _checkResult == gameconst.UseItemEnum.TRUE:
                self.base.baseUseItems(gridId, itemId, useNum, _useItemCtx, False)
            elif _checkResult == gameconst.UseItemEnum.PENDING:
                LOG_INFO('pending check', bagType, gridId, itemId, targetId)
                if not _useItemCtx.pendingOpId:
                    LOG_ERR('pending check error', bagType, gridId, itemId)
                    return
            else:
                LOG_ERR('check function error', bagType, gridId, itemId)
        else:
            self.base.baseUseItems(gridId, itemId, useNum, _useItemCtx, False)

    def cachePendingCheckId(self, gridId, itemId, useNum, useItemCtx, isBaseAct=False):
        _pendingIdDict = self.getTempMiscProp(gameconst.EntityPropsEnum.pendingCheckUseItem, {})
        if _pendingIdDict:
            pid = max(_pendingIdDict.keys()) + 1
        else:
            pid = 1
            self.setTempMiscProp(gameconst.EntityPropsEnum.pendingCheckUseItem, _pendingIdDict)

        useItemCtx.pendingOpId = pid
        tid = self.addTimerCB(10, '_pendingCheckExpired', (pid,), gametimer.TIMER_TAG_PENDING_CHECK_EXPIRED)
        _pendingIdDict[pid] = [gridId, itemId, useNum, useItemCtx, isBaseAct, tid]

        return pid

    def _pendingCheckExpired(self, pid):
        _pendingIdDict = self.getTempMiscProp(gameconst.EntityPropsEnum.pendingCheckUseItem, {})
        gridId, itemId, useNum, useItemCtx, isBaseAct, tid = _pendingIdDict.pop(pid, (None, 0))
        LOG_ERR('pending check expired', gridId, itemId, useNum, isBaseAct, tid, useItemCtx)
        if not _pendingIdDict:
            self.popTempMiscProp(gameconst.EntityPropsEnum.pendingCheckUseItem)

    def onSetPendingCheckRewardAndMaxUseNum(self, pendingId, awardList, maxUseNum):
        LOG_INFO("onSetPendingCheckRewardAndMaxUseNum ", pendingId, awardList, maxUseNum)
        _pendingIdDict = self.getTempMiscProp(gameconst.EntityPropsEnum.pendingCheckUseItem, {})
        if pendingId not in _pendingIdDict:
            LOG_ERR('invalid pending set id', pendingId)
            return
        _pendingIdDict[pendingId][2] = maxUseNum
        _pendingIdDict[pendingId][3].awardList = awardList
        LOG_INFO('self.getTempMiscProp(gameconst.EntityPropsEnum.pendingCheckUseItem, {}) ',
                  self.getTempMiscProp(gameconst.EntityPropsEnum.pendingCheckUseItem, {}))

    def onPendingCheckItemFinished(self, pendingId, checkResult):
        _pendingIdDict = self.getTempMiscProp(gameconst.EntityPropsEnum.pendingCheckUseItem, {})
        if pendingId not in _pendingIdDict:
            LOG_ERR('invalid pending check id', pendingId, checkResult)
            return

        _gridId, _itemId, useNum, useItemCtx, isBaseAct, tid = _pendingIdDict.pop(pendingId)
        useItemCtx.pendingOpId = 0
        self.cancelTimerCB(tid, gametimer.TIMER_TAG_PENDING_CHECK_EXPIRED)
        if checkResult == gameconst.UseItemEnum.TRUE:
            self.base.baseUseItems(_gridId, _itemId, useNum, useItemCtx, isBaseAct)

    def checkUseTreasureBoxCond(self, costDic, rewardId, gridId, itemId, useNum, useItemCtx):
        LOG_INFO('in checkUseTreasureBoxCond:', costDic, rewardId)
        self.cachePendingCheckId(gridId, itemId, useNum, useItemCtx, True)
        self.base.checkBaseUseTreasureBoxCond(
            costDic, rewardId, gridId, itemId, useNum, useItemCtx.pendingOpId)
        return gameconst.UseItemEnum.PENDING

    def doAction(self, gridId, itemId, useNum, opUUID, useItemCtx):
        LOG_INFO('doAction', opUUID, itemId, useItemCtx.targetId)
        itemData = ID_IDD.datas[itemId]
        action = itemData['action']

        # 物品action函数只能返回三个值,其他值会报错：
        # gameconst.UseItemEnum.FALSE：   使用失败，消耗的物品将被反还
        # gameconst.UseItemEnum.TRUE：    使用成功，将去base做后续处理
        # gameconst.UseItemEnum.PENDING： 不能立即得出结果，有多个使用过程，这个时候需要先调用setPendingUseId再返回PENDING
        #                            调用setPendingUseId会获得一个pendingId，物品最终使用成功或失败都必须调用cell部分的onPendingUseItem
        #                            函数告知使用的结果，此时只能是TRUE/FALSE，确保物品的action的每个return的之前都调用过onPendingUseItem
        #                            否则15s后还没得到结果会报错
        result = action(self, gridId, itemId, useNum, opUUID, useItemCtx)
        if result == gameconst.UseItemEnum.FALSE:
            self.base.afterUseItemDone(False, opUUID, True)
        elif result == gameconst.UseItemEnum.TRUE:
            self.base.afterUseItemDone(True, opUUID, True)
        elif result == gameconst.UseItemEnum.PENDING:
            pass
        else:
            LOG_ERR('doAction error', opUUID, itemId)
            self.base.afterUseItemDone(True, opUUID, True)

    def setPendingUseId(self, opUUID, useItemCtx):
        LOG_INFO("setPendingUseId 1", opUUID, useItemCtx)
        _pendingIdDict = self.getTempMiscProp(gameconst.EntityPropsEnum.pendingUseItem, {})
        if _pendingIdDict:
            pid = max(_pendingIdDict.keys()) + 1
        else:
            pid = 1
            self.setTempMiscProp(gameconst.EntityPropsEnum.pendingUseItem, _pendingIdDict)

        useItemCtx.pendingOpId = pid
        tid = self.addTimerCB(15, '_pendingUseExpired', (pid,), gametimer.TIMER_TAG_PENDING_USE_EXPIRED)
        _pendingIdDict[pid] = (useItemCtx, opUUID, tid)
        LOG_INFO("setPendingUseId 2", opUUID, pid)
        return pid

    def _pendingUseExpired(self, pid):
        _pendingIdDict = self.getTempMiscProp(gameconst.EntityPropsEnum.pendingUseItem, {})
        useItemCtx, opUUID, tid = _pendingIdDict.pop(pid, (None, 0))
        LOG_ERR('_pendingUseExpired', useItemCtx, tid)

        if not _pendingIdDict:
            self.popTempMiscProp(gameconst.EntityPropsEnum.pendingUseItem)

    def onPendingUseItemFinished(self, pendingId, useResult):
        LOG_INFO("onPendingUseItemFinished", pendingId, type(pendingId), useResult)
        _pendingIdDict = self.getTempMiscProp(gameconst.EntityPropsEnum.pendingUseItem, {})
        if pendingId not in _pendingIdDict:
            LOG_ERR('invalid pending check id', pendingId)
            return

        useItemCtx, opUUID, tid = _pendingIdDict.pop(pendingId)
        self.cancelTimerCB(tid, gametimer.TIMER_TAG_PENDING_USE_EXPIRED)
        if useResult == gameconst.UseItemEnum.FALSE:
            self.base.afterUseItemDone(False, opUUID, False)
        elif useResult == gameconst.UseItemEnum.TRUE:
            self.base.afterUseItemDone(True, opUUID, False)

    def addSettlementExp(self, awardResults, entityID, expValue):
        awardResult = awardResults.get(entityID)
        if not awardResult:
            awardResult = {}
            awardResults[entityID] = awardResult
        awardResult["exp"] = awardResult.get("exp", 0) + expValue

    def addSettlementAward(self, awardResults, entityID, rewardID, rewardNum, rewardDisplayMode):
        awardResult = awardResults.get(entityID)
        if not awardResult:
            awardResult = {}
            awardResults[entityID] = awardResult
        k = "awards_{0}".format(rewardDisplayMode)
        data = awardResult.get(k)
        if not data:
            data = []
            awardResult[k] = data
        data.append([rewardID, rewardNum])

    def processKillMonsterExp(self, dropCtx, awardResults):
        LOG_DBG("iBag-> processKillMonsterExp 1 ", dropCtx, awardResults)
        monsterExp = dataUtils.getMonsterExp(dropCtx.monsterId, dropCtx.level)
        if monsterExp is None or monsterExp == 0:
            return
        # 组队
        if self.isInTeam(self.gbId):
            teammateNum = len(self.teammateEntIdInAoiSet)
            if teammateNum >= 1:
                # 组队加成系数列表
                teamNumBonus = C_CD.datas['killMonsterTeamExpBonus'].get("value")
                # 组队加成系数
                teamNumRatio = teamNumBonus[teammateNum]
                # 组队均分经验
                teamExp = int(teamNumRatio * monsterExp / (teammateNum + 1))
                # 按照个人调整
                for memEntId in self.teammateEntIdInAoiSet:
                    memVal = KBEngine.entities.get(memEntId)
                    if not memVal:
                        continue
                    memberExp = self._adjustKillMonsterExp(awardResults, teamExp, dropCtx.level, memVal.level)
                    self.addSettlementExp(awardResults, memEntId, memberExp)
                    LOG_DBG("iBag-> processKillMonsterExp 2 ", dropCtx, awardResults, teamExp, dropCtx.level, memVal.level)
                # 杀怪的个人调整
                LOG_DBG("iBag-> processKillMonsterExp 3 ", dropCtx, awardResults, teamExp, dropCtx.level, self.level)
                killerExp = self._adjustKillMonsterExp(awardResults, teamExp, dropCtx.level, self.level)
                self.addSettlementExp(awardResults, self.id, killerExp)
            else:
                killerExp = self._adjustKillMonsterExp(awardResults, monsterExp, dropCtx.level, self.level)
                self.addSettlementExp(awardResults, self.id, killerExp)
                LOG_DBG("iBag-> processKillMonsterExp 4 ", dropCtx, awardResults, monsterExp, dropCtx.level, self.level)
        # 团战
        elif self.inRaid():
            # 根据等级调整经验
            killerExp = self._adjustKillMonsterExp(awardResults, monsterExp, dropCtx.level, self.level)
            self.addSettlementExp(awardResults, self.id, killerExp)
            LOG_DBG("iBag-> processKillMonsterExp 5 ", dropCtx, awardResults, monsterExp, dropCtx.level, self.level)
        else:
            # 根据等级调整经验
            killerExp = self._adjustKillMonsterExp(awardResults, monsterExp, dropCtx.level, self.level)
            self.addSettlementExp(awardResults, self.id, killerExp)
            LOG_DBG("iBag-> processKillMonsterExp 6 ", dropCtx, awardResults, monsterExp, dropCtx.level, self.level)
        return

    def _adjustKillMonsterExp(self, awardResults, monsterExp, monsterLevel, playerLevel):
        LOG_DBG("iBag-> _adjustKillMonsterExp", awardResults, monsterExp, monsterLevel, playerLevel)
        # 根据等级调整经验
        config = formula.getKillMonsterRewardConfig(monsterLevel, playerLevel)
        realExp = int(monsterExp * config.get('expprop'))
        return realExp

    def preAwardOnKillMonster(self, dropCtx, dropRewardIds, shareRewards, displayModes):
        LOG_DBG("iBag->preAwardOnKillMonster ", dropCtx, dropRewardIds, shareRewards, displayModes)
        awardResults = {}
        self.processKillMonsterExp(dropCtx, awardResults)
        for idx in range(len(dropRewardIds)):
            dropRewardId = dropRewardIds[idx]
            shareReward = shareRewards[idx]
            displayMode = displayModes[idx]
            self.processKillMonsterAward(awardResults, dropRewardId, 1, shareReward, displayMode, dropCtx)

        for entityID, awardResult in awardResults.items():
            memVal = KBEngine.entities.get(entityID)
            if not memVal:
                LOG_ERR('iBag->preAwardOnKillMonster, entity is missing', entityID, awardResults)
                continue
            exp = awardResult.get("exp", 0)
            awards0 = awardResult.get("awards_0", [])
            awards1 = awardResult.get("awards_1", [])
            memVal.doKillMonsterAwards(dropCtx, exp, awards0, awards1)

    def doKillMonsterAwards(self, dropCtx, exp, awards0, awards1):
        dropCtx.addContextVar('additionProps', {'copper': self.getProp('copper')})
        LOG_DBG("iBag->doKillMonsterAwards ", dropCtx, exp, awards0, awards1)
        self.checkIncMoralValueOnKillMonster(dropCtx.level)
        if exp > 0:
            self.addExpByKill(exp, dropCtx.level, dropCtx.opUUID, dropCtx.srcType, dropCtx.detail, True)
        #dropCtx.detail and dropCtx.detail.__setstate__({'cellExpVal':exp})
        self.base.doAwardOnKillMonster(dropCtx, awards0, awards1)

    def processKillMonsterAward(self, awardResults, dropRewardId, rewardNum, shareReward, displayMode, dropCtx):
        LOG_DBG("iBag->processKillMonsterAward ", awardResults, dropRewardId, rewardNum, shareReward, displayMode, dropCtx)
        #首刀归属类奖励全部都会爆到地上，不进包，要做金币经验之类的，可以同时配(1,3)两种，3负责爆地上，1负责进包
        if shareReward == gameconst.DropShareRewardType.FIRST_BLOOD:
            return
        # 组队
        if self.isInTeam(self.gbId):
            teammateNum = len(self.teammateEntIdInAoiSet)
            if teammateNum >= 1:
                if shareReward == gameconst.DropShareRewardType.SELF:
                    self.addSettlementAward(awardResults, self.id, dropRewardId, rewardNum, displayMode)
                elif shareReward == gameconst.DropShareRewardType.ALL_TEAMMATE:
                    for memEntId in self.teammateEntIdInAoiSet:
                        memVal = KBEngine.entities.get(memEntId)
                        if not memVal:
                            continue
                        self.addSettlementAward(awardResults, memEntId, dropRewardId, rewardNum, displayMode)
                    self.addSettlementAward(awardResults, self.id, dropRewardId, rewardNum, displayMode)
                elif shareReward == gameconst.DropShareRewardType.RANDOM_ONE:
                    allRanEntId = list(self.teammateEntIdInAoiSet) + [self.id]
                    randChoiceEntId = random.choice(allRanEntId)
                    memVal = KBEngine.entities.get(randChoiceEntId)
                    if memVal:
                        self.addSettlementAward(awardResults, randChoiceEntId, dropRewardId, rewardNum, displayMode)
            else:
                self.addSettlementAward(awardResults, self.id, dropRewardId, rewardNum, displayMode)
        # 团战
        elif self.inRaid():
            raidmateNum = len(self.raidmateEntIdInAoiSet)
            if raidmateNum >= 1:
                if shareReward == gameconst.DropShareRewardType.SELF:
                    self.addSettlementAward(awardResults, self.id, dropRewardId, rewardNum, displayMode)
                elif shareReward == gameconst.DropShareRewardType.ALL_TEAMMATE:
                    # for _, _, memberVal in self.raidInfo.iterGetRaidMember():
                    #     if not memberVal.playerBox:
                    #         continue
                    for memEntId in self.raidmateEntIdInAoiSet:
                        memVal = KBEngine.entities.get(memEntId)
                        if not memVal:
                            continue
                        self.addSettlementAward(awardResults, memEntId, dropRewardId, rewardNum, displayMode)
                elif shareReward == gameconst.DropShareRewardType.RANDOM_ONE:
                    # memberVals = []
                    # for _, _, memberVal in self.raidInfo.iterGetRaidMember():
                    #     if not memberVal.playerBox:
                    #         continue
                    #     memberVals.append(memberVal)
                    # memberVal = random.choice(memberVals)
                    # memVal = KBEngine.entities.get(memberVal.playerBox.id)
                    allRanEntId = list(self.raidmateEntIdInAoiSet) + [self.id]
                    randChoiceEntId = random.choice(allRanEntId)
                    memVal = KBEngine.entities.get(randChoiceEntId)
                    if memVal:
                        self.addSettlementAward(awardResults, randChoiceEntId, dropRewardId, rewardNum, displayMode)
            else:
                self.addSettlementAward(awardResults, self.id, dropRewardId, rewardNum, displayMode)
        else:
            self.addSettlementAward(awardResults, self.id, dropRewardId, rewardNum, displayMode)

    def sendTeamMessage(self,messageId,messageArgs):
        if self.isInTeam(self.gbId):
            gameengine.getTeamStub(self.teamId).sendTeamMemberMsg(self.teamId,messageId,messageArgs)

################################## 采集 相关 ######################################
    @gamedecorator.crossServer
    @utils.isMyself
    @gamedecorator.limitcall(1)
    def applyGather(self, exposed, targetId):
        LOG_INFO('applyGather', targetId)
        if not self.checkConflictState(C_C_DD.datas.clientPick):
            LOG_WARN('applyGather, checkConflictState')
            return False

        target = KBEngine.entities.get(targetId, None)
        if not (target and target.IsCollection):
            LOG_WARN('applyGather, target')
            return False
        
        LOG_INFO('applyGather, createTime:', target.createTime)
        pickData = NPD.datas.get(target.collectionId, None)
        if not pickData:
            return False

        if sMath.distance2D(self.position, target.position) > pickData['pickDistance'] + 1:
            self.showMsg(M_M_DD.datas.targetIsOutOfRange, [])
            return False

        if pickData['precheckAction'] is not None:
            ctx = pickData['precheckAction'](self, target.collectionId)

            if not ctx.checkCell(self):
                LOG_WARN('applyGather, checkCell failed', self.id, target.collectionId)
                return False

        else:
            ctx = None

        # 检查采集物及base条件
        return target.checkAvatarGather(self.base, self.gbId, ctx, self.hasState(gameconst.StateEnum.clientPick))

    def onBaseAvatarGatherCheckSucc(self, targetId, ret):
        LOG_INFO('onBaseAvatarGatherCheckSucc', targetId, ret)
        if not (ret and self._prepareApplyGather(targetId)):
            if ret:
                LOG_WARN('_prepareApplyGather')
            self.endApplyGather(gameconst.CancelGatherReason.GatherCheck)

        return

    def _calPickTime(self, target):
        pickData = NPD.datas.get(target.collectionId, None)
        if not pickData:
            return 1

        pickTime = pickData['time']
        if target.type == gameconst.CollectionType.MINERAL:
            pickTime = pickTime * (1 - self.getProp('miningRate'))
        elif target.type == gameconst.CollectionType.ZHEN_QI:
            pickTime = pickTime * (1 - self.getProp('gatherRate'))
        elif target.type == gameconst.CollectionType.DECAY_BOX:
            # 计算衰减时间
            elapsedTime = utils.curTS() - target.createTime
            pickTimeDecay = NPCST.datas.get("pickTimeLessen", {}).get('value')
            if pickTimeDecay:
                lastDecayTime = 0
                lastDecayRate = 0
                for decayData in pickTimeDecay:
                    decayTime, decayRate = decayData
                    if elapsedTime > decayTime:
                        if decayTime >= lastDecayTime:
                            lastDecayTime = decayTime
                            lastDecayRate = decayRate
                if lastDecayRate > 0:
                    pickTime = math.ceil(pickTime * lastDecayRate)
        pickTime = pickTime if pickTime > 0 else 0
        LOG_INFO('_calPickTime', pickTime)
        return pickTime

    def _prepareApplyGather(self, targetId):
        LOG_INFO('_prepareApplyGather', targetId)
        gatherTime = utils.getTimestamp64()
        _target = KBEngine.entities.get(targetId, None)
        if not (_target and _target.IsCollection):
            return False

        if not self.checkConflictState(dataUtils.getStateEventId(gameconst.StateEnum.clientPick)):
            LOG_WARN('_prepareApplyGather, state conflict ')
            return False

        gatherTarget = self.getTempMiscProp(gameconst.EntityPropsEnum.gatherTarget, None)
        if gatherTarget:
            if targetId != gatherTarget['targetId']:
                LOG_ERR('_prepareApplyGather, continuous collection, not same', targetId, gatherTarget['targetId'])
                return False
            if 'timer' in gatherTarget:
                LOG_WARN('_prepareApplyGather, continuous collection, in picking ', targetId, gatherTarget['targetId'])
                return True
            LOG_INFO('_prepareApplyGather, continuous collection', targetId)
        elif not _target.canGather:
            self.showMsg(M_M_DD.datas.collectionWarning, [])
            LOG_WARN('_prepareApplyGather, _target can not gather', targetId, _target.collectionId)
            return False

        pickData = NPD.datas.get(_target.collectionId, None)
        if not pickData:
            return False

        self.setState(gameconst.StateEnum.clientPick)

        gatherTargetInfo = {'targetId': targetId, 'gatherTime': gatherTime, 'isUnstoppble': pickData['isUnstoppble'],
                            'collection': _target, 'collectionId': _target.collectionId,
                            'collectionType': _target.type, 'startTime': utils.curTS()}

        pickTime = self._calPickTime(_target)

        timer = None
        if pickData['pickType'] in gameconst.CollectionPickType.CountdownTypes:
            timer = self.addTimerCB(pickTime, '_finishApplyGather', (targetId,),
                                   gametimer.TIMER_TAG_FINISH_APPLY_GATHER)
        gatherTargetInfo['timer'] = timer
        self.suspendAutoCombat(gameconst.SuspendAutoCombatReasonEnum.ApplyGather)
        self.setTempMiscProp(gameconst.EntityPropsEnum.gatherTarget, gatherTargetInfo)
        applyAction = pickData['applyAction']
        if applyAction and callable(applyAction):
            applyAction(self, self, actionContext.ACTION_CONTEXT_DEFAULT)

        if pickData['isUnique']:
            _target.canGather = False

        self.allClients.onApplyGather(targetId, pickTime*1000)
        return True

    @gamedecorator.crossServer
    @utils.isMyself
    def cancelGather(self, exposed, infoId):
        LOG_INFO('cancelGather:', infoId)
        self.endApplyGather(gameconst.CancelGatherReason.Client, infoId)

    @gamedecorator.crossServer
    @utils.isMyself
    @gamedecorator.limitcall(1)
    def applyFinishGather(self, exposed, targetId):
        LOG_INFO('applyFinishGather:', targetId)
        target = KBEngine.entities.get(targetId)
        if not target:
            LOG_WARN('applyFinishGather, no target:', targetId)
            return
        _pickData = NPD.datas.get(target.collectionId)
        if not _pickData or _pickData['pickType'] not in gameconst.CollectionPickType.ClientJudgeTypes:
            gameengine.panicStack('applyFinishGather, not client judge pickType:', targetId, target.collectionId)
            return
        self._finishApplyGather(targetId)

    def _finishApplyGather(self, targetId):
        if not self._checkFinishApplyGather(targetId):
            LOG_WARN('_checkFinishApplyGather', targetId)
            self.endApplyGather(gameconst.CancelGatherReason.ApplyGatherCheck)
            return

    def _checkFinishApplyGather(self, targetId):
        LOG_INFO("_finishApplyGather  ", targetId)
        gatherTarget = self.getTempMiscProp(gameconst.EntityPropsEnum.gatherTarget, None)
        if not gatherTarget:
            return False
        if targetId and gatherTarget['targetId'] != targetId:
            return False
        target = KBEngine.entities.get(targetId)
        if not target:
            return False
        if 'timer' not in gatherTarget:
            return True

        gatherTarget.pop('timer', None)
        pickData = NPD.datas.get(target.collectionId, None)
        if target and pickData and pickData['isUnique']:
            target.canGather = True

        if target.type in gameconst.CollectionType.VALID_RANGE_CHECK:
            self.base.doApplyGatherPreCheck(
                target.collectionId, target.gameEntityId, targetId, False, self.spaceNo)
        else:
            LOG_ERR('un-known collection type', target.type)
            return False

        return True

    def onDoApplyGatherPreCheck(self, collectionId, gameEntityId, targetId, isCaptain, spaceNo, deductWealthVal, checkResult):
        LOG_INFO("onDoApplyGatherPreCheck::", collectionId, gameEntityId, targetId, isCaptain, spaceNo,
                  deductWealthVal, checkResult)
        if not (checkResult and self._doApplyGather(collectionId, gameEntityId, targetId, isCaptain, spaceNo, deductWealthVal)):
            if checkResult:
                LOG_WARN('_doApplyGather')
            self.endApplyGather(gameconst.CancelGatherReason.ApplyGather)
        return

    def _doApplyGather(self, collectionId, gameEntityId, targetId, isCaptain, spaceNo, deductWealthVal):

        target = KBEngine.entities.get(targetId)
        if not target:
            LOG_WARN("onDoApplyGatherPreCheck::target not found", self.gbId, targetId)
            self.client.onUpdateCollectionGatherFlag(targetId, 0)
            return False

        if target.gameEntityId != gameEntityId:
            LOG_ERR("onDoApplyGatherPreCheck::target not same", self.gbId, targetId, target.gameEntityId,
                      gameEntityId)
            self.client.onUpdateCollectionGatherFlag(targetId, 0)
            return False

        if not target._checkAvatarGather(self.base, self.gbId):
            LOG_WARN("onDoApplyGatherPreCheck::check avatar gather error", self.gbId, targetId)
            self.client.onUpdateCollectionGatherFlag(targetId, 0)
            return False

        opUUID = KBEngine.genUUID64()
        self.base.baseDoApplyGather(collectionId, gameEntityId, targetId, isCaptain, spaceNo, deductWealthVal, self._calPickTime(target), opUUID, target.awardContext)

        target.addGatherAvatar(self.id, self.gbId, collectionId)

        if target.dropEquipId:
            self.takeEquip(target.dropEquipId)

        gatherTarget = self.getTempMiscProp(gameconst.EntityPropsEnum.gatherTarget, None)
        if gatherTarget:
            LogTrackingMgr.LogTrackingMgr.Gather_Collection(
                self.gbId,
                self.clientDistinctIdCell,
                self.gbId,
                gatherTarget['collectionId'],
                gatherTarget['collectionType'],
                gatherTarget['startTime'],
                utils.curTS(),
                opUUID,
            )

        return self.applyGather(self.id, targetId)

    def endApplyGather(self, id, infoId=0):
        LOG_INFO('endApplyGather', id, infoId)
        self._removePickState(infoId)

    def _removePickState(self, infoId):
        if self.hasState(gameconst.StateEnum.clientPick):
            self.removeState(gameconst.StateEnum.clientPick, infoId)
        return

    def _onExitClientPick(self, byConflictState, removeReason):
        LOG_INFO("_onExitClientPick1", byConflictState, removeReason)
        gatherTarget = self.popTempMiscProp(gameconst.EntityPropsEnum.gatherTarget, None)
        pickData = NPD.datas.get(gatherTarget['collectionId'], None) if gatherTarget else None
        if gatherTarget and pickData:
            LOG_INFO("_onExitClientPick2")
            if 'timer' in gatherTarget:
                if gatherTarget['timer']:
                    self.cancelTimerCB(gatherTarget['timer'], gametimer.TIMER_TAG_FINISH_APPLY_GATHER)
                self.allClients.onCancelGather(removeReason)
            targetId = gatherTarget['targetId']
            target = KBEngine.entities.get(targetId)
            if target and pickData['isUnique']:
                target.canGather = True

        self.resumeAutoCombat(self.spaceNo, gameconst.SuspendAutoCombatReasonEnum.ApplyGather)
        if pickData:
            unApplyAction = pickData['unApplyAction']
            if unApplyAction and callable(unApplyAction):
                unApplyAction(self, self, actionContext.ACTION_CONTEXT_DEFAULT)
        return

    def giveGatherAwardCell(self, collectionId):
        _pickData = NPD.datas[collectionId]
        triggerPos = _pickData['triggerPos']
        if triggerPos:
            if self.checkConflictState(C_C_DD.datas.teleport):
                self.telToPos(triggerPos)
            # self.base.teleportByNo(self.spaceNo, triggerPos, self.direction, '', ())
            else:
                self.showMsg(NPCST.datas.get("pickFailedAlert_TransportFail", {}).get('value'), [_pickData['castDesc']])

        triggerAction = _pickData['triggerAction']
        if triggerAction and callable(triggerAction):
            triggerAction(self, collectionId)

    def checkCollectionGatherFlag(self, eid):
        collection = KBEngine.entities.get(eid)
        if not collection or collection.isDestroyed:
            LOG_INFO("checkCollectionGatherFlag wrong ", eid, collection)
            return
        collection.checkAvatarGatherFlag(self.base, self.gbId)
        collection.checkAvatarGatherPickTimes(self.base, self.gbId)

        if hasattr(collection, 'firstBloodTargetGbIds'):
            isTarget = self.gbId in collection.firstBloodTargetGbIds
            self.addTimerCB(0.5, '_doSyncIsFBTarget', (eid, isTarget, 0), gametimer.TIMER_TAG_DO_SYNC_IS_FB_TARGET)
        LOG_INFO("checkCollectionGatherFlag ", eid)

    def _doSyncIsFBTarget(self, eid, isTarget, times):
        targetClient = self.clientEntity(eid)
        LOG_INFO("_doSyncIsFBTarget", eid, isTarget, targetClient, isinstance(targetClient, (utils.Swallower,)))
        if targetClient and not isinstance(targetClient, (utils.Swallower,)):
            targetClient.syncIsFBTarget(isTarget)
        elif times < 5:
            self.addTimerCB(0.5, '_doSyncIsFBTarget', (eid, isTarget, times + 1), gametimer.TIMER_TAG_DO_SYNC_IS_FB_TARGET)
        else:
            LOG_ERR("_doSyncIsFBTarget repeat times >= 5", eid, isTarget, targetClient, times)

    ################################## 采集 end #########################################

    def useItemRandRewardPool(self, boxItemId, poolId, opUUID, ctx):
        pass

    ################################## item use check ###################################
    def checkHealHpOrMpItemCond(self, itemId):
        if self.hp == self.fullHp and self.mp == self.fullMp:
            self.showMsg(M_M_DD.datas.useMedicine_HPMPIsFull, [str(itemId)])
            return gameconst.UseItemEnum.FALSE

        return gameconst.UseItemEnum.TRUE

    def checkHealSalveItemCond(self, itemId):
        if self.hp == self.fullHp:
            self.showMsg(M_M_DD.datas.useMedicine_HPIsFull, [str(itemId)])
            return gameconst.UseItemEnum.FALSE

        return gameconst.UseItemEnum.TRUE

    def useHealSalveItem(self, itemId, addNum, addPct, *args):
        _delta = 0
        if addNum > 0:
            ret = self.healByNum(self, actionContext.UseItemHealContext(itemId, self.id), addNum, *args)
            if ret is not None:
                _delta += ret.healVal

        if addPct > 0:
            ret = self.healByPct(self, actionContext.UseItemHealContext(itemId, self.id), addPct, *args)
            if ret is not None:
                _delta += ret.healVal

        if _delta > 0:
            self.client.onHealItemResult(_delta, True)

        return gameconst.UseItemEnum.TRUE

    def checkUseAddMpItemCond(self, itemId):
        if self.mp == self.fullMp:
            self.showMsg(M_M_DD.datas.useMedicine_MPIsFull, [str(itemId)])
            return gameconst.UseItemEnum.FALSE

        return gameconst.UseItemEnum.TRUE

    def useAddMpItem(self, itemId, addNum, addPct, *args):
        if addNum > 0:
            self.addMp(self, actionContext.UseItemHealContext(itemId, self.id), addNum, *args)

        if addPct > 0:
            self.addMpByPct(self, actionContext.UseItemHealContext(itemId, self.id), addPct, *args)

        return gameconst.UseItemEnum.TRUE

    def useAddBuffByItem(self, itemId, *args):
        self.addBuffBySkill(self, actionContext.UseItemHealContext(itemId, self.id), *args)
        return gameconst.UseItemEnum.TRUE

    def useAddTargetBuffByItem(self, context, itemId, *args):
        _target = KBEngine.entities.get(context.targetId)
        if not _target:
            return gameconst.UseItemEnum.FALSE
        self.addBuffBySkill(_target, actionContext.UseItemHealContext(itemId, self.id), *args)
        return gameconst.UseItemEnum.TRUE

    def checkUseTelToNearestTeleportor(self, itemId, *args):
        if formula.inWorldLineScene(self.spaceNo):
            return gameconst.UseItemEnum.TRUE
        self.showMsg(C_CD.datas["teleportStoneInvalidMsg"]['value'], [])
        return gameconst.UseItemEnum.FALSE

    def onUseTelToNearestTeleportor(self, result, pendingUseId, toCell, spaceNo, dstPos, dstDir):
        # LOG_ERR("DEBUG::onUseTelToNearestTeleportor::", toCell, spaceNo, dstPos, dstDir)
        if result:
            self.onPendingUseItemFinished(pendingUseId, gameconst.UseItemEnum.TRUE)
        else:
            self.onPendingUseItemFinished(pendingUseId, gameconst.UseItemEnum.FALSE)

    ################################## item skill check ###################################

    # --------------------------------- 改帮会名--------------------------------
    def checkModifyGuildName(self, gridId, itemId, useNum, context):
        if not (context.argsList and isinstance(context.argsList[0], str)):
            return gameconst.UseItemEnum.FALSE

        newName = context.argsList[0]
        if not self.guildUUID:
            return gameconst.UseItemEnum.FALSE

        if not utils.checkGuildNameLength(newName):
            self.showMsg(L_SD.datas['avatarNameLengthOverLimit_msg']["value"], [])
            return gameconst.UseItemEnum.FALSE

        if not utils.checkGuildName(newName):
            self.showMsg(C_CD.datas['forbiddenContent']['value'], [])
            return gameconst.UseItemEnum.FALSE

        pendingCheckId = self.cachePendingCheckId(gridId, itemId, useNum, context)
        self.base.checkModifyGuildNameBase(newName, pendingCheckId)
        return gameconst.UseItemEnum.PENDING

    # -------------------------------- 改名 ----------------------------------
    def checkModifyName(self, gridId, itemId, useNum, ctx):
        LOG_INFO('checkModifyName:', ctx.argsList)
        if not (ctx.argsList and isinstance(ctx.argsList[0], str)):
            return gameconst.UseItemEnum.FALSE

        name = ctx.argsList[0]

        name = name.strip()
        if not utils.checkAvatarNameLength(name):
            self.showMsg(L_SD.datas['avatarNameLengthOverLimit_msg']["value"], [])
            return gameconst.UseItemEnum.FALSE

        if not utils.checkAvatarName(name):
            self.showMsg(M_M_DD.datas.forbiddenContent, [])
            return gameconst.UseItemEnum.FALSE

        if name.isdigit():
            self.showMsg(M_M_DD.datas.forbiddenContent, [])
            return gameconst.UseItemEnum.FALSE

        pendingCheckId = self.cachePendingCheckId(gridId, itemId, useNum, ctx)
        self.base.checkModifyNameBase(pendingCheckId, gridId, itemId, name)
        return gameconst.UseItemEnum.PENDING

    def checkGetRewardByBPLotteryBoxItem(self, actId, gridId, itemId, useNum, ctx):
        pendingCheckId = self.cachePendingCheckId(gridId, itemId, useNum, ctx, True)
        self.base.onCheckGetRewardByBPLotteryBoxItem(pendingCheckId, actId)
        return gameconst.UseItemEnum.PENDING

    def checkGetRewardByNBPLotteryBoxItem(self, actId, gridId, itemId, useNum, ctx):
        pendingCheckId = self.cachePendingCheckId(gridId, itemId, useNum, ctx, True)
        self.base.onCheckGetRewardByNBPLotteryBoxItem(pendingCheckId, actId)
        return gameconst.UseItemEnum.PENDING

    # --------------------------------- 自动吃药  begin ------------------------
    @gamedecorator.crossServer
    @utils.isMyself
    def setBAutoHeal(self, exposed, autoUse, isHp):
        # flag 定义位置 gameconst.AvatarFlagCell
        if isHp:
            _flag = gameconst.AvatarFlagCell.AUTO_HEAL_HP
        else:
            _flag = gameconst.AvatarFlagCell.AUTO_HEAL_MP

        self.updateCommonFlagCell(self.id, _flag, autoUse)

    @gamedecorator.crossServer
    @utils.isMyself
    def setHealRatio(self, exposed, ratio, isHp):
        if 0 <= ratio <= 100:
            if isHp:
                self.healHpRatio = ratio
            else:
                self.healMpRatio = ratio

    # --------------------------------- 自动吃药  end   ------------------------

    # 只能用于道具action
    def getReward(self, rewardId, level, gridId, itemId, useNum, opUUID, context):
        if level == -1:
            level = self.level
        context.withMailId = gameconst.MailConstEnum.REWARD_MAIL_ID
        self.setPendingUseId(opUUID, context)
        self.base.getRewardByIdBase(rewardId, level, gridId, itemId, useNum, opUUID, context)
        return gameconst.UseItemEnum.PENDING

    def checkPickedCollections(self):
        expired = []
        for cid, num in self.pickedCollections.items():
            pickData = NPD.datas.get(cid)
            if not pickData:
                expired.append(cid)
                continue

            if pickData.get('isInvalid', 0):
                expired.append(cid)

        for cid in expired:
            self.pickedCollections.pop(cid)

    def addPickedCollections(self, collectionEnt, maxPickTimes):
        collectionId = collectionEnt.collectionId
        if len(self.pickedCollections) >= 100 and collectionId not in self.pickedCollections:
            LOG_ERR('addPickedCollections: too many collections', collectionId)

        self.pickedCollections[collectionId] = self.pickedCollections.get(collectionId, 0) + 1

        if self.pickedCollections[collectionId] == maxPickTimes:
            self.pickedCollections[collectionId] = -1
            collectionEnt.setWitnessType(self.id, gameconst.WitnessTypeEnum.WITNESS_ENUM_HIDE)

    def getCollectionAlreadyPickTime(self, collectionId):
        return self.pickedCollections.get(collectionId, 0)

    def sendAllPickedCollections(self):
        collectionIds = []
        nums = []
        for cid, num in self.pickedCollections.items():
            if num < 0:
                continue
            collectionIds.append(cid)
            nums.append(num)

    def checkUseTelToMainCity(self, itemId, *args):
        mapId = formula.fetchMapId(self.spaceNo)
        canUseReturnScroll = GPGPD.datas[mapId]['canUseReturnScroll']
        if not canUseReturnScroll:
            msgId = GPSD.datas.get("msgId_cantUseReturnScroll").get('value')
            self.base.onMessagePre(msgId, [])
            LOG_INFO("DEBUG::checkUseTelToMainCity::", itemId, GPGPD.datas[mapId]['canUseReturnScroll'], self.getMoralEffectTransItem())
            return gameconst.UseItemEnum.FALSE

        canUseReturnScroll = self.getMoralEffectTransItem()
        if not canUseReturnScroll:
            msgId = PKD.datas.get("PK_cantUseTransItem_msgID").get('value')
            self.base.onMessagePre(msgId, [])
            LOG_INFO("DEBUG::checkUseTelToMainCity::", itemId, GPGPD.datas[mapId]['canUseReturnScroll'], self.getMoralEffectTransItem())
            return gameconst.UseItemEnum.FALSE

        returnMapID = GPGPD.datas[mapId]['returnMapID']
        if not returnMapID or not self.onCheckMapUnlocked(returnMapID):
            LOG_INFO("DEBUG::checkUseTelToMainCity::", itemId, GPGPD.datas[mapId]['returnMapID'])
            return gameconst.UseItemEnum.FALSE

        return gameconst.UseItemEnum.TRUE

    def useTelToMainCity(self, opUUID, context, castTime=-1, *args):
        LOG_INFO("DEBUG::useTelToMainCity::", context, castTime, args)
        mapId = formula.parseLineType(self.spaceNo)
        returnMapID = GPGPD.datas[mapId]['returnMapID']
        if not returnMapID:
            LOG_ERR('useTelToMainCity not found returnMapId', mapId)
            return gameconst.UseItemEnum.FALSE

        sceneRes = GPGPD.datas[returnMapID]['sceneRes']
        returnPosList = GPSSDD.datas[sceneRes]['returnPos']
        if not returnPosList:
            LOG_ERR('useTelToMainCity not config returnPos', mapId, returnMapID)
            return gameconst.UseItemEnum.FALSE

        returnPos = random.choice(returnPosList)

        pendingUseId = self.setPendingUseId(opUUID, context)
        spaceNo, dstPos, dstDir = returnMapID, returnPos, self.direction
        callback, callbackArgs = "onUseTelToMainCity", (True, pendingUseId, None, spaceNo, dstPos, dstDir)
        fCallback, fCallbackArgs = "onUseTelToMainCity", (False, pendingUseId, None, spaceNo, dstPos, dstDir)

        _extra = {'dstSpaceNo': spaceNo, 'dstPos': dstPos}
        self._commonNeedCast(C_C_DD.datas.teleportCast,
                             gameconst.StateEnum.Teleporting,
                             gameconst.CastType.teleportByUseItem,
                             'onTelToMainCityWithCast',
                             (None, spaceNo, dstPos, dstDir, callback, callbackArgs, fCallback, fCallbackArgs),
                             castTime=castTime,
                             failedFunc=fCallback,
                             failedArgs=fCallbackArgs,
                             extraProps=_extra)

        return gameconst.UseItemEnum.PENDING

    def onUseTelToMainCity(self, result, pendingUseId, toCell, spaceNo, dstPos, dstDir):
        LOG_INFO("DEBUG::onUseTelToMainCity::", toCell, spaceNo, dstPos, dstDir)
        if result:
            self.onPendingUseItemFinished(pendingUseId, gameconst.UseItemEnum.TRUE)
        else:
            self.onPendingUseItemFinished(pendingUseId, gameconst.UseItemEnum.FALSE)

    def checkModifyName(self, gridId, itemId, useNum, ctx):
        LOG_INFO('checkModifyName:', ctx.argsList)
        pendingCheckId = self.cachePendingCheckId(gridId, itemId, useNum, ctx)
        self.base.checkRenameBase(pendingCheckId, ctx.argsList[0])
        return gameconst.UseItemEnum.PENDING

    def modifyNameAction(self, opUUID, ctx):
        _newName = ctx.argsList[0]
        pendingUseId = self.setPendingUseId(opUUID, ctx)
        self.base.modifyNameBase(pendingUseId, _newName)
        return gameconst.UseItemEnum.PENDING

    def onPendingUseRenameItemResult(self, success, pendingUseId, newName):
        _oldName = self.name
        self.name = newName
        if success:
            self.onPendingUseItemFinished(pendingUseId, gameconst.UseItemEnum.TRUE)
        else:
            self.onPendingUseItemFinished(pendingUseId, gameconst.UseItemEnum.FALSE)

        self.base.delOldName(_oldName)
        self.pyWriteToDB()
        gameengine.getGlobalBase('PlayerStub').updateName(_oldName, newName, self, self.gbId)

        if self.isInTeam():
            gameengine.getTeamStub(self.teamId).modifyPlayerName(self.base, self.teamId, self.gbId, newName, _oldName)
        elif self.inRaid():
            gameengine.getRaidStub(self.raidUUID).modifyPlayerName(self.base, self.raidUUID, self.gbId, newName, _oldName)

    def bodyItemLock(self, equipIn, equipPos, itemId, uniqueId, lockStatus):
        LOG_INFO('in bodyItemLock::', equipIn, equipPos, itemId, uniqueId, lockStatus)
        if itemId not in GBGBD.datas:
            LOG_WARN("in bodyItemLock, wrong arg item Id 1", itemId)
            return

        if lockStatus not in gameconst.ItemLockStatus.VALID_STATUS:
            LOG_WARN("in bodyItemLock, wrong arg lockStatus", lockStatus)
            return

        equipItem = self.bodyEquipData.getEquipItem(equipPos)
        if equipItem.uniqueId != uniqueId:
            LOG_WARN("in bodyItemLock, wrong arg unique Id", equipItem.uniqueId, uniqueId)
            return

        if equipItem.itemId != itemId:
            LOG_WARN("in bodyItemLock, wrong arg item Id 2", equipItem.itemId, itemId)
            return

        if not equipItem.isGood(self.gbID):
            LOG_WARN("in bodyItemLock, equipment item is broken ", equipItem.itemId, itemId)
            return
        
        equipItem.setLockStatus(lockStatus)

        self.client.onLockItemSucc(equipIn, equipPos, itemId, lockStatus)

    def bagExpansion(self, gridNum, gridId, itemId, useNum, opUUID, context):
        pendingUseId = self.setPendingUseId(opUUID, context)
        self.base.bagExpansion(pendingUseId, gridNum, gridId, itemId, useNum, opUUID, context)
        return gameconst.UseItemEnum.PENDING

    def warehouseExpansion(self, gridNum, gridId, itemId, useNum, opUUID, context):
        pendingUseId = self.setPendingUseId(opUUID, context)
        self.base.warehouseExpansion(pendingUseId, gridNum, gridId, itemId, useNum, opUUID, context)
        return gameconst.UseItemEnum.PENDING

    def setTitleCell(self, titleId):
        self.title = titleId

    def getAvatarAwardCtxCell(self, awardId, awardCtx, mailId=0):
        awardCtx = awardCtx or awardContext.CommonContext(mailId)
        awardCtx.args.addArg('avatarLv', self.level)
        awardCtx.addContextVar('school', self.school)
        awardCtx.addContextVar('awardId', awardId)
        awardCtx.args.addArg('avatarSex', self.sex)
        awardCtx.addContextVar('avatarGbId', self.gbId)
        awardCtx.addContextVar('avatarId', self.id)
        awardCtx.addContextVar('isMonthCardExpired', self.isMonthCardExpiredCell())
        awardCtx.addContextVar('isBigMonthCardExpired', self.isBigMonthCardExpiredCell())
        awardCtx.addContextVar('avatarScoreRank', self.avatarScoreRankCell)
        awardCtx.addContextVar('isCrossServer', self.isCrossServer)
        return awardCtx
