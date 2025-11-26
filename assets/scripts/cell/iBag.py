# -*- encoding:utf-8 -*-
from KBEDebug import *
import KBEngine

import sMath
import utils
import gameconst
import gameengine
import gamedecorator
from collections.abc import Iterable
import itemData_itemData as IDID
import message_Message_def as MMD
import conflict_conflict_def as CCD
import NPC_pickConst as NPCST
import const_const as CONST
import NPC_Pick as NPD
import itemData_set as IDS
import login_set as LGS
import bagData_set as BDSD
import creep_base as CBD
import gamePlay_gamePlay as GPGPD
import gamePlay_singleSceneData as GPSSDD
import gamePlay_set as GPSD
import taskClass_taskTarget as TCCTD
import PKData_PKData as PKD
import gearBase_gearBase as GBGBD

import actionContext
import dataUtils
import formula
import gametimer
import random



class IBag(object):
    @gamedecorator.crossServer
    @utils.isMyself
    def reqUseItems(self, exposed, bagType, gridId, itemId, targetId, useNum, argsList):
        INFO_MSG('ckz: reqUseItems', bagType, gridId, itemId, targetId, useNum, argsList)
        if useNum <= 0:
            return
        if not targetId:
            targetId = self.id

        if itemId not in IDID.datas:
            ERROR_MSG('ckz: item id %d is invalid' % itemId)
            return

        if not self.checkConflictState(CCD.datas.useItem):
            WARNING_MSG('   in reqUseItems, checkConflictState failed')
            return

        itemData = IDID.datas[itemId]
        # 检查职业限定
        checkClass = itemData['class']
        if isinstance(checkClass, Iterable):
            if self.school not in checkClass:
                WARNING_MSG('   in reqUseItems, class check failed')
                return
        else:
            if checkClass != 0 and checkClass != self.school:
                WARNING_MSG('   in reqUseItems, class check failed')
                return

        if not itemData['use']:
            WARNING_MSG('   in reqUseItems, item can not use')
            return

        if useNum > 1 and not itemData['batchUse']:
            WARNING_MSG('   in reqUseItems, item can not batch use')
            return

        if useNum > BDSD.datas['itemBatchUseUpLimit']['value']:
            WARNING_MSG('in reqUseItems, use items num reach uplimit:', useNum)
            useNum = BDSD.datas['itemBatchUseUpLimit']['value']

        useItemCtx = actionContext.UseItemCtx(targetId, argsList)
        if itemData['subType'] in (gameconst.ItemSubType.Normal,):
            useItemCtx = actionContext.UseBoxTypeItemCtx(targetId, argsList)

        if not self.isSwitchOpen(itemId):
            return

        checkFunc = itemData['conditionCheckAction']
        if checkFunc:
            # 物品check函数只能返回三个值,其他值会报错：
            # gameconst.UseItem.FALSE：   检查失败，使用过程将中断
            # gameconst.UseItem.TRUE：    检查成功，将去base进程锁定背包扣除数量，再在cell进程执行物品action
            # gameconst.UseItem.PENDING： 不能立即得出结果，即要异步检查，这个时候需要先调用setPendingCheckId再返回PENDING
            #                            调用setPendingCheckId会获得一个pendingId，等检查得出结果时，再调用cell部分的onPendingCheckItem
            #                            函数告知检查的结果，此时只能是TRUE/FALSE
            checkResult = checkFunc(self, gridId, itemId, useNum, useItemCtx)
            if checkResult == gameconst.UseItem.FALSE:
                return
            elif checkResult == gameconst.UseItem.TRUE:
                self.base.baseUseItems(gridId, itemId, useNum, useItemCtx, False)
            elif checkResult == gameconst.UseItem.PENDING:
                DEBUG_MSG('pending check', bagType, gridId, itemId, targetId)
                if not useItemCtx.pendingOpId:
                    ERROR_MSG('pending check error', bagType, gridId, itemId)
                    return
            else:
                ERROR_MSG('check function error', bagType, gridId, itemId)
        #            checkFunc(self, useItemCtx)
        else:
            self.base.baseUseItems(gridId, itemId, useNum, useItemCtx, False)

    def isSwitchOpen(self, itemId):
        # if itemId == int(IDS.datas.get("changeNameCard").get('value')) and not gameconfig.enableModifyName():
        #     return False
        return True

    def setPendingCheckId(self, gridId, itemId, useNum, useItemCtx, isBaseAct=False):
        pendingIdDict = self.getTempMiscProp(gameconst.AvatarProps.pendingCheckUseItem, {})
        if pendingIdDict:
            pid = max(pendingIdDict.keys()) + 1
        else:
            pid = 1
            self.setTempMiscProp(gameconst.AvatarProps.pendingCheckUseItem, pendingIdDict)

        useItemCtx.pendingOpId = pid
        tid = self._callback(10, '_pendingCheckExpired', (pid,), gametimer.TIMER_TAG_PENDING_CHECK_EXPIRED)
        pendingIdDict[pid] = [gridId, itemId, useNum, useItemCtx, isBaseAct, tid]

        return pid

    def _pendingCheckExpired(self, pid):
        pendingIdDict = self.getTempMiscProp(gameconst.AvatarProps.pendingCheckUseItem, {})
        gridId, itemId, useNum, useItemCtx, isBaseAct, tid = pendingIdDict.pop(pid, (None, 0))
        ERROR_MSG('pending check expired', gridId, itemId, useNum, isBaseAct, tid, useItemCtx)
        if not pendingIdDict:
            self.popTempMiscProp(gameconst.AvatarProps.pendingCheckUseItem)

    def onSetPendingCheckRewardAndMaxUseNum(self, pendingId, awardList, maxUseNum):
        DEBUG_MSG("onSetPendingCheckRewardAndMaxUseNum ", pendingId, awardList, maxUseNum)
        pendingIdDict = self.getTempMiscProp(gameconst.AvatarProps.pendingCheckUseItem, {})
        if pendingId not in pendingIdDict:
            ERROR_MSG('invalid pending set id', pendingId)
            return
        pendingIdDict[pendingId][2] = maxUseNum
        pendingIdDict[pendingId][3].awardList = awardList
        DEBUG_MSG('self.getTempMiscProp(gameconst.AvatarProps.pendingCheckUseItem, {}) ',
                  self.getTempMiscProp(gameconst.AvatarProps.pendingCheckUseItem, {}))

    def onPendingCheckItem(self, pendingId, checkResult):
        pendingIdDict = self.getTempMiscProp(gameconst.AvatarProps.pendingCheckUseItem, {})
        if pendingId not in pendingIdDict:
            ERROR_MSG('invalid pending check id', pendingId, checkResult)
            return

        gridId, itemId, useNum, useItemCtx, isBaseAct, tid = pendingIdDict.pop(pendingId)
        useItemCtx.pendingOpId = 0
        self._cancelCallback(tid, gametimer.TIMER_TAG_PENDING_CHECK_EXPIRED)
        if checkResult == gameconst.UseItem.FALSE:
            return
        elif checkResult == gameconst.UseItem.TRUE:
            self.base.baseUseItems(gridId, itemId, useNum, useItemCtx, isBaseAct)

    def checkUseTreasureBoxCond(self, costDic, rewardId, gridId, itemId, useNum, useItemCtx):
        DEBUG_MSG('in checkUseTreasureBoxCond:', costDic, rewardId)
        self.setPendingCheckId(gridId, itemId, useNum, useItemCtx, True)
        self.base.checkBaseUseTreasureBoxCond(costDic, rewardId, gridId, itemId, useNum, useItemCtx.pendingOpId)
        return gameconst.UseItem.PENDING

    def checkRefreshTaskByItemCond(self, gridId, itemId, taskId, useItemCtx):
        self.setPendingCheckId(gridId, itemId, 1, useItemCtx, True)
        self.base.checkRefrshTaskByItemBaseCond(useItemCtx.pendingOpId, taskId)
        return gameconst.UseItem.PENDING

    def bagCapacityCheck(self, gridId, itemId, useNum, ctx, rewardId, level):
        if level == -1:
            level = self.level

        self.setPendingCheckId(gridId, itemId, useNum, ctx)
        self.base.openRewardCheckBase(gameconst.BagType.BAG_TYPE_NORMAL, useNum, ctx, rewardId)
        return gameconst.UseItem.PENDING

    def checkUseAuditValueItemCond(self, gridId, itemId, useNum, ctx):
        self.setPendingCheckId(gridId, itemId, useNum, ctx, True)
        self.base.useAuditValueItemCheckBase(ctx.pendingOpId, gridId, itemId)
        return gameconst.UseItem.PENDING

    def doAction(self, gridId, itemId, useNum, opUUID, useItemCtx):
        INFO_MSG('doAction', opUUID, itemId, useItemCtx.targetId)
        itemData = IDID.datas[itemId]
        action = itemData['action']

        # 物品action函数只能返回三个值,其他值会报错：
        # gameconst.UseItem.FALSE：   使用失败，消耗的物品将被反还
        # gameconst.UseItem.TRUE：    使用成功，将去base做后续处理
        # gameconst.UseItem.PENDING： 不能立即得出结果，有多个使用过程，这个时候需要先调用setPendingUseId再返回PENDING
        #                            调用setPendingUseId会获得一个pendingId，物品最终使用成功或失败都必须调用cell部分的onPendingUseItem
        #                            函数告知使用的结果，此时只能是TRUE/FALSE，确保物品的action的每个return的之前都调用过onPendingUseItem
        #                            否则15s后还没得到结果会报错
        result = action(self, gridId, itemId, useNum, opUUID, useItemCtx)
        if result == gameconst.UseItem.FALSE:
            self.base.useItemDone(False, opUUID)
        elif result == gameconst.UseItem.TRUE:
            self.base.useItemDone(True, opUUID)
        elif result == gameconst.UseItem.PENDING:
            pass
        else:
            ERROR_MSG('doAction error', opUUID, itemId)
            self.base.useItemDone(True, opUUID)

    def setPendingUseId(self, opUUID, useItemCtx):
        DEBUG_MSG("setPendingUseId 1", opUUID, useItemCtx)
        pendingIdDict = self.getTempMiscProp(gameconst.AvatarProps.pendingUseItem, {})
        if pendingIdDict:
            pid = max(pendingIdDict.keys()) + 1
        else:
            pid = 1
            self.setTempMiscProp(gameconst.AvatarProps.pendingUseItem, pendingIdDict)

        useItemCtx.pendingOpId = pid
        tid = self._callback(15, '_pendingUseExpired', (pid,), gametimer.TIMER_TAG_PENDING_USE_EXPIRED)
        pendingIdDict[pid] = (useItemCtx, opUUID, tid)
        DEBUG_MSG("setPendingUseId 2", opUUID, pid)
        return pid

    def _pendingUseExpired(self, pid):
        pendingIdDict = self.getTempMiscProp(gameconst.AvatarProps.pendingUseItem, {})
        useItemCtx, opUUID, tid = pendingIdDict.pop(pid, (None, 0))
        ERROR_MSG('_pendingUseExpired', useItemCtx, tid)

        if not pendingIdDict:
            self.popTempMiscProp(gameconst.AvatarProps.pendingUseItem)

    def onPendingUseItem(self, pendingId, useResult):
        DEBUG_MSG("onPendingUseItem", pendingId, type(pendingId), useResult)
        pendingIdDict = self.getTempMiscProp(gameconst.AvatarProps.pendingUseItem, {})
        if pendingId not in pendingIdDict:
            ERROR_MSG('invalid pending check id', pendingId)
            return

        useItemCtx, opUUID, tid = pendingIdDict.pop(pendingId)
        self._cancelCallback(tid, gametimer.TIMER_TAG_PENDING_USE_EXPIRED)
        if useResult == gameconst.UseItem.FALSE:
            self.base.useItemDone(False, opUUID)
        elif useResult == gameconst.UseItem.TRUE:
            self.base.useItemDone(True, opUUID)

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
        DEBUG_MSG("iBag-> processKillMonsterExp 1 ", dropCtx, awardResults)
        exp = dataUtils.getMonsterExp(dropCtx.monsterId, dropCtx.level)
        if exp is None or exp == 0:
            return
        DEBUG_MSG("iBag-> processKillMonsterExp 2 ", dropCtx, awardResults, exp)
        # 组队
        if self.isInTeam(self.gbId):
            teammateNum = len(self.teammateEntIdInAoiSet)
            if teammateNum >= 1:
                teamNumBonus = CONST.datas['killMonsterTeamExpBonus'].get("value")
                teamLevelAll = self.level
                for memEntId in self.teammateEntIdInAoiSet:
                    memVal = KBEngine.entities.get(memEntId)
                    if memVal:
                        teamLevelAll += memVal.level

                teamNumCoeff = teamNumBonus[teammateNum]
                for memEntId in self.teammateEntIdInAoiSet:
                    memVal = KBEngine.entities.get(memEntId)
                    if not memVal:
                        continue
                    teamMemExp = dataUtils.getExpByLevel(memVal.level, dropCtx.level,exp)
                    realExp = round(teamMemExp * teamNumCoeff * ((memVal.level + 2) / (teamLevelAll + 2 * (teammateNum + 1))))

                    self.addSettlementExp(awardResults, memEntId, realExp)

                #个人等级杀怪经验修正
                myexp = dataUtils.getExpByLevel(self.level, dropCtx.level,exp)
                realExp = round(myexp * teamNumCoeff * ((self.level + 2) / (teamLevelAll + 2 * (teammateNum + 1))))

                self.addSettlementExp(awardResults, self.id, realExp)
            else:
                self.addSettlementExp(awardResults, self.id, exp)
        # 团战
        elif self.isInRaid():
            self.addSettlementExp(awardResults, self.id, exp)
        else:
            self.addSettlementExp(awardResults, self.id, exp)
        return

    def preAwardOnKillMonster(self, dropCtx, dropRewardIds, shareRewards, displayModes):
        DEBUG_MSG("iBag->preAwardOnKillMonster ", dropCtx, dropRewardIds, shareRewards, displayModes)
        awardResults = {}
        self.processKillMonsterExp(dropCtx, awardResults)
        for idx in range(len(dropRewardIds)):
            dropRewardId = dropRewardIds[idx]
            shareReward = shareRewards[idx]
            displayMode = displayModes[idx]
            self.processKillMonsterAward(awardResults, dropRewardId, 1, shareReward, displayMode)

        for entityID, awardResult in awardResults.items():
            memVal = KBEngine.entities.get(entityID)
            if not memVal:
                ERROR_MSG('iBag->preAwardOnKillMonster, entity is missing', entityID, awardResults)
                continue
            exp = awardResult.get("exp", 0)
            awards0 = awardResult.get("awards_0", [])
            awards1 = awardResult.get("awards_1", [])
            memVal.doKillMonsterAwards(dropCtx, exp, awards0, awards1)

    def doKillMonsterAwards(self, dropCtx, exp, awards0, awards1):
        dropCtx.addContextVar('additionProps', {'copper': self.getProp('copper')})
        DEBUG_MSG("iBag->doKillMonsterAwards ", dropCtx, exp, awards0, awards1)
        self.checkIncMoralValueOnKillMonster(dropCtx.level)
        if exp > 0:
            self.addExpByKill(exp, dropCtx.level, dropCtx.opUUID, dropCtx.srcType, dropCtx.detail, True)
        #dropCtx.detail and dropCtx.detail.__setstate__({'cellExpVal':exp})
        self.base.doAwardOnKillMonster(dropCtx, awards0, awards1)

    def processKillMonsterAward(self, awardResults, dropRewardId, rewardNum, shareReward, displayMode):
        DEBUG_MSG("iBag->processKillMonsterAward ", awardResults, dropRewardId, rewardNum, shareReward, displayMode)
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
        elif self.isInRaid():
            if shareReward == gameconst.DropShareRewardType.SELF:
                self.addSettlementAward(awardResults, self.id, dropRewardId, rewardNum, displayMode)
            elif shareReward == gameconst.DropShareRewardType.ALL_TEAMMATE:
                for _, _, memberVal in self.raidInfo.iterGetRaidMember():
                    if not memberVal.playerBox:
                        continue
                    memVal = KBEngine.entities.get(memberVal.playerBox.id)
                    if not memVal:
                        continue
                    self.addSettlementAward(awardResults, memberVal.playerBox.id, dropRewardId, rewardNum, displayMode)
            elif shareReward == gameconst.DropShareRewardType.RANDOM_ONE:
                memberVals = []
                for _, _, memberVal in self.raidInfo.iterGetRaidMember():
                    if not memberVal.playerBox:
                        continue
                    memberVals.append(memberVal)
                memberVal = random.choice(memberVals)
                memVal = KBEngine.entities.get(memberVal.playerBox.id)
                if memVal:
                    self.addSettlementAward(awardResults, memberVal.playerBox.id, dropRewardId, rewardNum, displayMode)
        else:
            self.addSettlementAward(awardResults, self.id, dropRewardId, rewardNum, displayMode)

    def sendTeamMessage(self,messageId,messageArgs):
        if self.isInTeam(self.gbId):
            gameengine.getTeamStub(self.teamId).sendTeamMemberMessage(self.teamId,messageId,messageArgs)

################################## 采集 相关 ######################################

    @gamedecorator.crossServer
    @utils.isMyself
    @gamedecorator.limitcall(1)
    def applyGather(self, exposed, targetId):
        DEBUG_MSG('applyGather', targetId)
        if not self.checkConflictState(CCD.datas.clientPick):
            WARNING_MSG('applyGather, checkConflictState')
            return False

        target = KBEngine.entities.get(targetId, None)
        if not (target and target.IsCollection):
            return False
        pickData = NPD.datas.get(target.collectionId, None)
        if not pickData:
            return False

        if sMath.distance2D(self.position, target.position) > pickData['pickDistance'] + 1:
            self.showMsg(MMD.datas.targetIsOutOfRange, [])
            return False

        if pickData['precheckAction'] is not None:
            ctx = pickData['precheckAction'](self, target.collectionId)

            if not ctx.checkCell(self):
                WARNING_MSG('applyGather, checkCell failed', self.id, target.collectionId)
                return False

        else:
            ctx = None

        # 检查采集物及base条件
        return target.checkAvatarGather(self.base, self.gbId, ctx)

    def onBaseAvatarGatherCheckSucc(self, targetId, ret):
        DEBUG_MSG('onBaseAvatarGatherCheckSucc', targetId, ret)
        if not (ret and self._prepareApplyGather(targetId)):
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
        pickTime = pickTime if pickTime > 0 else 0
        return pickTime

    def _prepareApplyGather(self, targetId):
        DEBUG_MSG('_prepareApplyGather', targetId)
        gatherTime = utils.getTimestamp64()
        target = KBEngine.entities.get(targetId, None)
        if not (target and target.IsCollection):
            return False

        if not self.checkConflictState(dataUtils.getStateEventId(gameconst.State.clientPick)):
            WARNING_MSG('_prepareApplyGather, state conflict ')
            return False

        gatherTarget = self.getTempMiscProp(gameconst.AvatarProps.gatherTarget, None)
        if gatherTarget:
            if targetId != gatherTarget['targetId']:
                ERROR_MSG('_prepareApplyGather, continuous collection, not same', targetId, gatherTarget['targetId'])
                return False
            if 'timer' in gatherTarget:
                ERROR_MSG('_prepareApplyGather, continuous collection, in picking ', targetId, gatherTarget['targetId'])
                return False
            DEBUG_MSG('_prepareApplyGather, continuous collection', targetId)
        elif not target.canGather:
            self.showMsg(MMD.datas.collectionWarning, [])
            WARNING_MSG('_prepareApplyGather, target can not gather', targetId, target.collectionId)
            return False

        pickData = NPD.datas.get(target.collectionId, None)
        if not pickData:
            return False

        self.setState(gameconst.State.clientPick)

        gatherTargetInfo = {'targetId': targetId, 'gatherTime': gatherTime, 'isUnstoppble': pickData['isUnstoppble'],
                            'collection': target, 'collectionId': target.collectionId}

        pickTime = self._calPickTime(target)

        timer = None
        if pickData['pickType'] in gameconst.CollectionPickType.CountdownTypes:
            timer = self._callback(pickTime, '_finishApplyGather', (targetId,),
                                   gametimer.TIMER_TAG_FINISH_APPLY_GATHER)
        gatherTargetInfo['timer'] = timer
        self.suspendFollow(gameconst.SuspendFollowReason.ApplyGather)
        self.suspendAutoCombat(gameconst.SuspendAutoCombatReason.ApplyGather)
        self.setTempMiscProp(gameconst.AvatarProps.gatherTarget, gatherTargetInfo)
        applyAction = pickData['applyAction']
        if applyAction and callable(applyAction):
            applyAction(self, self, actionContext.ACTION_CONTEXT_DEFAULT)

        if pickData['isUnique']:
            target.canGather = False

        self.allClients.onApplyGather(targetId, pickTime*1000)
        targetClient = self.clientEntity(targetId)
        targetClient and targetClient.onEnterCollect()
        return True

    @gamedecorator.crossServer
    @utils.isMyself
    def cancelGather(self, exposed):
        self.endApplyGather(gameconst.CancelGatherReason.Client)

    @gamedecorator.crossServer
    @utils.isMyself
    @gamedecorator.limitcall(1)
    def applyFinishGather(self, exposed, targetId):
        DEBUG_MSG('applyFinishGather:', targetId)
        target = KBEngine.entities.get(targetId)
        if not target:
            WARNING_MSG('applyFinishGather, no target:', targetId)
            return
        pickData = NPD.datas.get(target.collectionId)
        if not pickData or pickData['pickType'] not in gameconst.CollectionPickType.ClientJudgeTypes:
            gameengine.reportCritical('applyFinishGather, not client judge pickType:', targetId, target.collectionId)
            return
        self._finishApplyGather(targetId)
        return

    def _finishApplyGather(self, targetId):
        if not self._checkFinishApplyGather(targetId):
            WARNING_MSG('_checkFinishApplyGather', targetId)
            self.endApplyGather(gameconst.CancelGatherReason.ApplyGatherCheck)
            return

    def _checkFinishApplyGather(self, targetId):
        DEBUG_MSG("_finishApplyGather  ", targetId)
        gatherTarget = self.getTempMiscProp(gameconst.AvatarProps.gatherTarget, None)
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
            # self.base.doApplyGatherPreCheck(
            #     target.collectionId, target.gameEntityId, targetId, self.isCaptain(), self.spaceNo)
            self.base.doApplyGatherPreCheck(
                target.collectionId, target.gameEntityId, targetId, False, self.spaceNo)
        else:
            ERROR_MSG('un-known collection type', target.type)
            return False

        return True

    def onDoApplyGatherPreCheck(self, collectionId, gameEntityId, targetId, isCaptain, spaceNo, deductWealthVal, checkResult):
        DEBUG_MSG("onDoApplyGatherPreCheck::", collectionId, gameEntityId, targetId, isCaptain, spaceNo,
                  deductWealthVal, checkResult)
        if not (checkResult and self._doApplyGather(collectionId, gameEntityId, targetId, isCaptain, spaceNo, deductWealthVal)):
            WARNING_MSG('onDoApplyGatherPreCheck err')
            self.endApplyGather(gameconst.CancelGatherReason.ApplyGather)
        return

    def _doApplyGather(self, collectionId, gameEntityId, targetId, isCaptain, spaceNo, deductWealthVal):

        target = KBEngine.entities.get(targetId)
        if not target:
            WARNING_MSG("onDoApplyGatherPreCheck::target not found", self.gbId, targetId)
            self.client.onUpdateCollectionGatherFlag(targetId, 0)
            return False

        if target.gameEntityId != gameEntityId:
            ERROR_MSG("onDoApplyGatherPreCheck::target not same", self.gbId, targetId, target.gameEntityId,
                      gameEntityId)
            self.client.onUpdateCollectionGatherFlag(targetId, 0)
            return False

        if not target._checkAvatarGather(self.base, self.gbId):
            WARNING_MSG("onDoApplyGatherPreCheck::check avatar gather error", self.gbId, targetId)
            self.client.onUpdateCollectionGatherFlag(targetId, 0)
            return False

        self.base.baseDoApplyGather(collectionId, gameEntityId, targetId, isCaptain, spaceNo, deductWealthVal, self._calPickTime(target))

        target.addGatherAvatar(self.id, self.gbId, collectionId)
        targetClient = self.clientEntity(targetId)
        targetClient and targetClient.onAfterCollect()

        if target.dropEquipId:
            self.takeEquip(target.dropEquipId)

        return self.applyGather(self.id, targetId)

    def endApplyGather(self, id):
        DEBUG_MSG('endApplyGather', id)
        self._removePickState()

    def _removePickState(self):
        if self.hasState(gameconst.State.clientPick):
            self.removeState(gameconst.State.clientPick)
        return

    def _onExitClientPick(self):
        DEBUG_MSG("_onExitClientPick1")
        gatherTarget = self.popTempMiscProp(gameconst.AvatarProps.gatherTarget, None)
        pickData = NPD.datas.get(gatherTarget['collectionId'], None) if gatherTarget else None
        if gatherTarget and pickData:
            DEBUG_MSG("_onExitClientPick2")
            if 'timer' in gatherTarget:
                if gatherTarget['timer']:
                    self._cancelCallback(gatherTarget['timer'], gametimer.TIMER_TAG_FINISH_APPLY_GATHER)
                self.allClients.onCancelGather()
            targetId = gatherTarget['targetId']
            targetClient = self.clientEntity(targetId)
            targetClient and targetClient.onCancelCollect()
            target = KBEngine.entities.get(targetId)
            if target and pickData['isUnique']:
                target.canGather = True

        self.recoverFollow(self.spaceNo, gameconst.SuspendFollowReason.ApplyGather)
        self.recoverAutoCombat(self.spaceNo, gameconst.SuspendAutoCombatReason.ApplyGather)
        unApplyAction = pickData['unApplyAction']
        if unApplyAction and callable(unApplyAction):
           unApplyAction(self, self, actionContext.ACTION_CONTEXT_DEFAULT)
        return

    def giveGatherAwardCell(self, collectionId):
        pickData = NPD.datas[collectionId]
        triggerPos = pickData['triggerPos']
        if triggerPos:
            if self.checkConflictState(CCD.datas.teleport):
                self.telToPos(triggerPos)
            # self.base.teleportByNo(self.spaceNo, triggerPos, self.direction, '', ())
            else:
                self.showMsg(NPCST.datas.get("pickFailedAlert_TransportFail", {}).get('value'), [pickData['castDesc']])

        triggerAction = pickData['triggerAction']
        if triggerAction and callable(triggerAction):
            triggerAction(self, collectionId)

    def checkCollectionGatherFlag(self, eid):
        collection = KBEngine.entities.get(eid)
        if not collection or collection.isDestroyed:
            DEBUG_MSG("checkCollectionGatherFlag wrong ", eid, collection)
            return
        collection.checkAvatarGatherFlag(self.base, self.gbId)
        collection.checkAvatarGatherPickTimes(self.base, self.gbId)
        DEBUG_MSG("checkCollectionGatherFlag ", eid)

    ################################## 采集 end #########################################

    def useItemRandRewardPool(self, boxItemId, poolId, opUUID, ctx):
        pass

    ################################## item use check ###################################
    def checkHealHpOrMpItemCond(self, itemId):
        if self.hp == self.fullHp and self.mp == self.fullMp:
            self.showMsg(MMD.datas.useMedicine_HPMPIsFull, [str(itemId)])
            return gameconst.UseItem.FALSE

        return gameconst.UseItem.TRUE

    def checkHealSalveItemCond(self, itemId):
        if self.hp == self.fullHp:
            self.showMsg(MMD.datas.useMedicine_HPIsFull, [str(itemId)])
            return gameconst.UseItem.FALSE

        return gameconst.UseItem.TRUE

    def useHealSalveItem(self, itemId, addNum, addPct, *args):
        _delta = 0
        if addNum > 0:
            ret = self.healByNum(self, actionContext.UseItemHealCtx(itemId, self.id), addNum, *args)
            if ret is not None:
                _delta += ret.healVal

        if addPct > 0:
            ret = self.healByPct(self, actionContext.UseItemHealCtx(itemId, self.id), addPct, *args)
            if ret is not None:
                _delta += ret.healVal

        if _delta > 0:
            self.client.onHealItemResult(_delta, True)

        return gameconst.UseItem.TRUE

    def checkUseAddMpItemCond(self, itemId):
        if self.mp == self.fullMp:
            self.showMsg(MMD.datas.useMedicine_MPIsFull, [str(itemId)])
            return gameconst.UseItem.FALSE

        return gameconst.UseItem.TRUE

    def useAddMpItem(self, itemId, addNum, addPct, *args):
        _oldMp = self.mp
        _delta = 0
        if addNum > 0:
            self.addMp(self, actionContext.UseItemHealCtx(itemId, self.id), addNum, *args)

        if addPct > 0:
            self.addMpByPct(self, actionContext.UseItemHealCtx(itemId, self.id), addPct, *args)

        return gameconst.UseItem.TRUE

    def useAddBuffByItem(self, itemId, *args):
        self.addBuffBySkill(self, actionContext.UseItemHealCtx(itemId, self.id), *args)
        return gameconst.UseItem.TRUE

    def useAddTargetBuffByItem(self, context, itemId, *args):
        target = KBEngine.entities.get(context.targetId)
        if not target:
            return gameconst.UseItem.FALSE
        self.addBuffBySkill(target, actionContext.UseItemHealCtx(itemId, self.id), *args)
        return gameconst.UseItem.TRUE

    def checkUseTelToNearestTeleportor(self, itemId, *args):
        if formula.spaceInWorldLine(self.spaceNo):
            return gameconst.UseItem.TRUE
        self.showMsg(CONST.datas["teleportStoneInvalidMsg"]['value'], [])
        return gameconst.UseItem.FALSE

    def onUseTelToNearestTeleportor(self, result, pendingUseId, toCell, spaceNo, dstPos, dstDir):
        # ERROR_MSG("DEBUG::onUseTelToNearestTeleportor::", toCell, spaceNo, dstPos, dstDir)
        if result:
            self.onPendingUseItem(pendingUseId, gameconst.UseItem.TRUE)
        else:
            self.onPendingUseItem(pendingUseId, gameconst.UseItem.FALSE)

    ################################## item skill check ###################################

    # --------------------------------- 改帮会名--------------------------------
    def checkModifyGuildName(self, gridId, itemId, useNum, ctx):
        if not (ctx.argsList and isinstance(ctx.argsList[0], str)):
            return gameconst.UseItem.FALSE

        newName = ctx.argsList[0]
        if not self.guildUUID:
            return gameconst.UseItem.FALSE

        if not utils.checkGuildNameLength(newName):
            self.showMsg(LGS.datas['avatarNameLengthOverLimit_msg']["value"], [])
            return gameconst.UseItem.FALSE

        if not utils.checkGuildName(newName):
            self.showMsg(CONST.datas['forbiddenContent']['value'], [])
            return gameconst.UseItem.FALSE

        pendingCheckId = self.setPendingCheckId(gridId, itemId, useNum, ctx)
        self.base.checkModifyGuildNameBase(newName, pendingCheckId)
        return gameconst.UseItem.PENDING

    def modifyGuildName(self, opUUID, ctx):
        if not len(ctx.argsList):
            return gameconst.UseItem.FALSE

        newName = ctx.argsList[0]

        if not self.guildUUID:
            return gameconst.UseItem.FALSE

        pendingUseId = self.setPendingUseId(opUUID, ctx)
        gameengine.getGlobalBase('GuildStub').doModifyGuildName(self.gbId, self.base, self.guildUUID, newName,
                                                                pendingUseId)
        return gameconst.UseItem.PENDING

    # -------------------------------- 改名 ----------------------------------
    def checkModifyName(self, gridId, itemId, useNum, ctx):
        DEBUG_MSG('checkModifyName:', ctx.argsList)
        if not (ctx.argsList and isinstance(ctx.argsList[0], str)):
            return gameconst.UseItem.FALSE

        name = ctx.argsList[0]

        name = name.strip()
        if not utils.checkAvatarNameLength(name):
            self.showMsg(LGS.datas['avatarNameLengthOverLimit_msg']["value"], [])
            return gameconst.UseItem.FALSE

        if not utils.checkAvatarName(name):
            self.showMsg(MMD.datas.forbiddenContent, [])
            return gameconst.UseItem.FALSE

        if name.isdigit():
            self.showMsg(MMD.datas.forbiddenContent, [])
            return gameconst.UseItem.FALSE

        pendingCheckId = self.setPendingCheckId(gridId, itemId, useNum, ctx)
        self.base.checkModifyNameBase(pendingCheckId, gridId, itemId, name)
        return gameconst.UseItem.PENDING

    def checkGetRewardByBPLotteryBoxItem(self, actId, gridId, itemId, useNum, ctx):
        pendingCheckId = self.setPendingCheckId(gridId, itemId, useNum, ctx, True)
        self.base.onCheckGetRewardByBPLotteryBoxItem(pendingCheckId, actId)
        return gameconst.UseItem.PENDING

    def checkGetRewardByNBPLotteryBoxItem(self, actId, gridId, itemId, useNum, ctx):
        pendingCheckId = self.setPendingCheckId(gridId, itemId, useNum, ctx, True)
        self.base.onCheckGetRewardByNBPLotteryBoxItem(pendingCheckId, actId)
        return gameconst.UseItem.PENDING

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
        # self.syncMethodCallToLocalServerCell("setHealHpRatio", (ratio, ))

    # --------------------------------- 自动吃药  end   ------------------------

    # 只能用于道具action
    def getReward(self, rewardId, level, gridId, itemId, useNum, opUUID, ctx):
        if level == -1:
            level = self.level
        ctx.withMailId = gameconst.MailConstID.REWARD_MAIL_ID
        self.setPendingUseId(opUUID, ctx)
        self.base.getRewardByIdBase(rewardId, level, gridId, itemId, useNum, opUUID, ctx)
        return gameconst.UseItem.PENDING

    def onCellBagDailyUpdate(self):
        pass

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
            ERROR_MSG('addPickedCollections: too many collections', collectionId)

        self.pickedCollections[collectionId] = self.pickedCollections.get(collectionId, 0) + 1

        if self.pickedCollections[collectionId] == maxPickTimes:
            self.pickedCollections[collectionId] = -1
            collectionEnt.setWitnessType(self.id, gameconst.WitnessType.WITNESS_TYPE_HIDE)

        if self.pickedCollections[collectionId] > 0:
            self.client.sendPickedCollectoins([collectionId], [self.pickedCollections[collectionId]])

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

        self.client.sendPickedCollectoins(collectionIds, nums)

    def checkUseTelToMainCity(self, itemId, *args):
        mapId = formula.getMapId(self.spaceNo)
        canUseReturnScroll = GPGPD.datas[mapId]['canUseReturnScroll']
        if not canUseReturnScroll:
            msgId = GPSD.datas.get("msgId_cantUseReturnScroll").get('value')
            self.base.onMessagePre(msgId, [])
            DEBUG_MSG("DEBUG::checkUseTelToMainCity::", itemId, GPGPD.datas[mapId]['canUseReturnScroll'], self.getMoralEffectTransItem())
            return gameconst.UseItem.FALSE

        canUseReturnScroll = self.getMoralEffectTransItem()
        if not canUseReturnScroll:
            msgId = PKD.datas.get("PK_cantUseTransItem_msgID").get('value')
            self.base.onMessagePre(msgId, [])
            DEBUG_MSG("DEBUG::checkUseTelToMainCity::", itemId, GPGPD.datas[mapId]['canUseReturnScroll'], self.getMoralEffectTransItem())
            return gameconst.UseItem.FALSE

        returnMapID = GPGPD.datas[mapId]['returnMapID']
        if not returnMapID or not self.onCheckMapUnlocked(returnMapID):
            DEBUG_MSG("DEBUG::checkUseTelToMainCity::", itemId, GPGPD.datas[mapId]['returnMapID'])
            return gameconst.UseItem.FALSE

        return gameconst.UseItem.TRUE

    def useTelToMainCity(self, opUUID, context, castTime=-1, *args):
        DEBUG_MSG("DEBUG::useTelToMainCity::", context, castTime, args)
        mapId = formula.getLineType(self.spaceNo)
        returnMapID = GPGPD.datas[mapId]['returnMapID']
        if not returnMapID:
            ERROR_MSG('useTelToMainCity not found returnMapId', mapId)
            return gameconst.UseItem.FALSE

        sceneRes = GPGPD.datas[returnMapID]['sceneRes']
        returnPosList = GPSSDD.datas[sceneRes]['returnPos']
        if not returnPosList:
            ERROR_MSG('useTelToMainCity not config returnPos', mapId, returnMapID)
            return gameconst.UseItem.FALSE

        returnPos = random.choice(returnPosList)

        pendingUseId = self.setPendingUseId(opUUID, context)
        spaceNo, dstPos, dstDir = returnMapID, returnPos, self.direction
        callback, callbackArgs = "onUseTelToMainCity", (True, pendingUseId, None, spaceNo, dstPos, dstDir)
        fCallback, fCallbackArgs = "onUseTelToMainCity", (False, pendingUseId, None, spaceNo, dstPos, dstDir)

        _extra = {'dstSpaceNo': spaceNo, 'dstPos': dstPos}
        self._commonNeedCast(CCD.datas.teleportCast,
                             gameconst.State.Teleporting,
                             gameconst.CastType.teleportByUseItem,
                             'onTelToMainCityWithCast',
                             (None, spaceNo, dstPos, dstDir, callback, callbackArgs, fCallback, fCallbackArgs),
                             castTime=castTime,
                             failedFunc=fCallback,
                             failedArgs=fCallbackArgs,
                             extraProps=_extra)

        return gameconst.UseItem.PENDING

    def onUseTelToMainCity(self, result, pendingUseId, toCell, spaceNo, dstPos, dstDir):
        DEBUG_MSG("DEBUG::onUseTelToMainCity::", toCell, spaceNo, dstPos, dstDir)
        if result:
            self.onPendingUseItem(pendingUseId, gameconst.UseItem.TRUE)
        else:
            self.onPendingUseItem(pendingUseId, gameconst.UseItem.FALSE)

    def checkModifyName(self, gridId, itemId, useNum, ctx):
        DEBUG_MSG('checkModifyName:', ctx.argsList)
        pendingCheckId = self.setPendingCheckId(gridId, itemId, useNum, ctx)
        self.base.checkRenameBase(pendingCheckId, ctx.argsList[0])
        return gameconst.UseItem.PENDING

    def modifyNameAction(self, opUUID, ctx):
        _newName = ctx.argsList[0]
        pendingUseId = self.setPendingUseId(opUUID, ctx)
        self.base.modifyNameBase(pendingUseId, _newName)
        return gameconst.UseItem.PENDING

    def onPendingUseRenameItemResult(self, success, pendingUseId, newName):
        _oldName = self.name
        self.name = newName
        if success:
            self.onPendingUseItem(pendingUseId, gameconst.UseItem.TRUE)
        else:
            self.onPendingUseItem(pendingUseId, gameconst.UseItem.FALSE)

        self.base.delOldName(_oldName)
        self.pyWriteToDB()

    def bodyItemLock(self, equipIn, equipPos, itemId, uniqueId, lockStatus):
        INFO_MSG('in bodyItemLock::', equipIn, equipPos, itemId, uniqueId, lockStatus)
        if itemId not in GBGBD.datas:
            WARNING_MSG("in bodyItemLock, wrong arg item Id 1", itemId)
            return

        if lockStatus not in gameconst.ItemLockStatus.VALID_STATUS:
            WARNING_MSG("in bodyItemLock, wrong arg lockStatus", lockStatus)
            return

        equipItem = self.bodyEquipData.getEquipItem(equipPos)
        if equipItem.uniqueId != uniqueId:
            WARNING_MSG("in bodyItemLock, wrong arg unique Id", equipItem.uniqueId, uniqueId)
            return

        if equipItem.itemId != itemId:
            WARNING_MSG("in bodyItemLock, wrong arg item Id 2", equipItem.itemId, itemId)
            return

        equipItem.setLockStatus(lockStatus)

        self.client.onLockItemSucc(equipIn, equipPos, itemId, lockStatus)

    def bagExpansion(self, gridNum, gridId, itemId, useNum, opUUID, context):
        pendingUseId = self.setPendingUseId(opUUID, context)
        self.base.bagExpansion(pendingUseId, gridNum, gridId, itemId, useNum, opUUID, context)
        return gameconst.UseItem.PENDING

    def warehouseExpansion(self, gridNum, gridId, itemId, useNum, opUUID, context):
        pendingUseId = self.setPendingUseId(opUUID, context)
        self.base.warehouseExpansion(pendingUseId, gridNum, gridId, itemId, useNum, opUUID, context)
        return gameconst.UseItem.PENDING
