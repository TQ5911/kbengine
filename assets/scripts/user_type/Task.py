# -*- encoding:utf-8 -*-

import KBEngine
from KBEDebug import *
import utils
import TaskTargetInfo
import dataUtils
import random
import gameengine
import gameconst
import userType
import dropAward
import json
import gameglobal
import LogTrackingMgr

import rewardTask_taskInfo as RRTID

class TaskExtraAttr(userType.UserSingleType):

    def __init__(self):
        self.gameEntityDict = {}

    def toTaskExtraAttrClientJson(self):
        dic = {}

        for k, v in vars(self).items():
            if v:
                dic[k] = v
        return json.dumps(dic)

    def toTaskExtraAttrSavedJson(self):
        dic = {}

        for k, v in vars(self).items():
            if v:
                dic[k] = v
        return json.dumps(dic)

    def fromTaskExtraAttrSavedJson(self, jsonStr):
        if not jsonStr:
            return
        dic = json.loads(jsonStr)
        self.__dict__.update(dic)
        return

    def updateTaskExtraAttrFromObj(self, attrObj):
        self.gameEntityDict = attrObj.gameEntityDict

    def updateFromDic(self, attrDic):
        for attrName, attrVal in attrDic.items():
            if hasattr(self, attrName):
                setattr(self, attrName, attrVal)

    def getExtraAttr(self, attrName, defaultVal, setDefault=True):
        if not hasattr(self, attrName):
            if setDefault:
                self.setExtraAttr(attrName, defaultVal)
            return defaultVal
        else:
            return getattr(self, attrName)

    def setExtraAttr(self, attrName, val):
        setattr(self, attrName, val)

    def clear(self):
        self.gameEntityDict = {}


class Task(userType.UserSingleType):
    def __init__(self, taskId, taskData=None):
        self.taskId = taskId
        taskData = taskData or dataUtils.getTaskData(taskId)
        self.taskType = dataUtils.taskFieldVal(taskData, 'TaskType')
        cycleEnable = dataUtils.taskFieldVal(taskData, 'OpenCondCheckTaskCount')
        if cycleEnable:
            self.cycleType = dataUtils.taskFieldVal(taskData, 'OpenCondCountCycle')
            self.limitCount = dataUtils.taskFieldVal(taskData, 'OpenCondCountLimit')
        else:
            self.cycleType = gameconst.TaskCycleType.CYCLE_TASK_ENUM_NONE
            self.limitCount = 0
        self.rootTaskId = dataUtils.getRootTaskId(taskId)
        self.parentTaskId = dataUtils.taskFieldVal(taskData, 'FatherTaskId')

        self.lastChildTaskId = 0
        self.stat = gameconst.TaskStat.TASK_STAT_DEFAULT
        # 领取任务次数
        self.claimCount = 0
        self.alreadyCount = 0
        self.teamId = 0
        self.claimSrc = gameconst.ClaimTaskSrcEnum.TASK_SRC_UNKNOWN
        self.seed = 0  # 计算随机子任务使用
        self.startTime = 0
        self.validSec = 0  # 只有在线时候才会计时的任务
        self.expiredTime = 0  # 下线时也要计时的任务
        self.extraAttr = TaskExtraAttr()
        self.pointsDic = {}
        self.childTaskIds = []
        self.targetDic = {}
        self.taskRewardLimitDic = {}
        self.guaranteeCount = 0

    def _lateReload(self):
        super(Task, self)._lateReload()
        for tgt in self.getAllTargets():
            tgt.reloadScript()

    def __getstate__(self):
        return self.toTaskSavedDict()

    def __setstate__(self, state):
        self.__init__(state['taskId'])
        self.fromSavedDict(state)

    def toTaskClientDict(self):
        expiredTime = 0
        if self.expiredTime > 0:
            expiredTime = self.expiredTime
        elif self.validSec > 0:
            expiredTime = utils.curTS() + self.validSec

        tgts = []
        for tgt in self.getAllTargets():
            tgts.append(tgt.toClientDict())
        return {
            'taskId': self.taskId,
            'taskType': self.taskType,
            'startTime': self.startTime,
            'stat': self.stat,
            'limitCount': self.limitCount,
            'alreadyCount': self.alreadyCount,
            'claimCount': self.claimCount,
            'expiredTime': expiredTime,
            'parentTaskId': self.parentTaskId,
            'targets': tgts,
            'extraJson': self.extraAttr.toTaskExtraAttrClientJson(),
        }

    def toTaskSavedDict(self):
        tgts = []

        for tgt in self.getAllTargets():
            tgts.append(tgt.toTgtSavedDict())

        return {
            'taskId': self.taskId,
            'claimSrc': self.claimSrc,
            'stat': self.stat,
            'limitCount': self.limitCount,
            'claimCount': self.claimCount,
            'alreadyCount': self.alreadyCount,
            'teamId': self.teamId,
            'startTime': self.startTime,
            'seed': self.seed,
            'validSec': self.validSec,
            'expiredTime': self.expiredTime,
            'lastChildTaskId': self.lastChildTaskId,

            'pointsDic': self.pointsDic,
            'taskRewardLimitDic': self.taskRewardLimitDic,
            'childTaskIds': self.childTaskIds,
            'targets': tgts,
            'extraJson': self.extraAttr.toTaskExtraAttrSavedJson(),
            'guaranteeCount': self.guaranteeCount,
        }

    def fromSavedDict(self, dataDic):
        self.taskId = dataDic['taskId']
        self.stat = dataDic['stat']
        self.limitCount = dataDic['limitCount']
        self.claimCount = dataDic.get('claimCount', 0)
        self.alreadyCount = dataDic['alreadyCount']
        self.teamId = dataDic.get('teamId', 0)
        self.startTime = dataDic['startTime']
        self.seed = dataDic.get('seed', 0)
        self.validSec = dataDic.get('validSec', 0)
        self.expiredTime = dataDic['expiredTime']
        self.lastChildTaskId = dataDic['lastChildTaskId']
        self.pointsDic = dataDic.get('pointsDic', {})
        self.taskRewardLimitDic = dataDic.get('taskRewardLimitDic', {})
        self.childTaskIds = list(dataDic['childTaskIds'])
        self.extraAttr = TaskExtraAttr()
        extraJson = dataDic.get('extraJson', '')
        self.extraAttr.fromTaskExtraAttrSavedJson(extraJson)
        self.claimSrc = dataDic.get('claimSrc', gameconst.ClaimTaskSrcEnum.TASK_SRC_UNKNOWN)
        self.guaranteeCount = dataDic.get('guaranteeCount', 0)

        self.resetTargetDic()
        for oneData in dataDic['targets']:
            tgt = TaskTargetInfo.TaskTgtFactory.createTargetBySavedDic(oneData)
            self.addNewTarget(tgt)

    def updateFromTaskObj(self, owner, task):
        LOG_DBG('in Task::updateFromTaskObj, taskId:', task.taskId)
        # if newTask:
        # #以下几个属性不要被覆盖
        #     self.limitCount = task.limitCount
        #     self.claimCount = task.claimCount
        #     self.alreadyCount = task.alreadyCount

        self.taskId = task.taskId
        self.claimSrc = task.claimSrc
        self.setStat(owner, task.stat)
        self.teamId = task.teamId
        self.startTime = task.startTime
        self.seed = task.seed
        self.validSec = task.validSec
        self.expiredTime = task.expiredTime

        self.pointsDic = {taskId: (pos[0], pos[1], pos[2]) for taskId, pos in task.pointsDic.items()}

        self.extraAttr.updateTaskExtraAttrFromObj(task.extraAttr)
        self.lastChildTaskId = task.lastChildTaskId
        self.childTaskIds = [tid for tid in task.childTaskIds]
        self.guaranteeCount = task.guaranteeCount
        self.targetDic = {}
        for tgtList in task.targetDic.values():
            for tgt in tgtList:
                newTgt = TaskTargetInfo.TaskTgtFactory.createTargetByObj(tgt)
                self.addNewTarget(newTgt)

    def resetTargetDic(self):
        self.targetDic = {}

    def addNewTarget(self, tgt):
        self.targetDic.setdefault(tgt.tgtType, []).append(tgt)

    def getTgtsByType(self, tgtType):
        return self.targetDic.get(tgtType, [])

    def findTargetByTypeAndId(self, tgtType, tgtId):
        targetList = self.getTgtsByType(tgtType)
        for target in targetList:
            if target.tgtId == tgtId:
                return target
        return None

    def getAllTargets(self):
        tgts = []
        for tgtList in self.targetDic.values():
            tgts.extend(tgtList)
        return tgts

    def getTargetDungeonList(self):
        dunList = []
        for tgt in self.getAllTargets():
            if tgt.dungeonNo > 1 and tgt.dungeonNo not in dunList:
                dunList.append(tgt.dungeonNo)
        return dunList

    @staticmethod
    def listShuffle(seed, srcList):
        gap = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
               31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
               73, 79, 83, 89, 97, 101, 103, 107, 109]
        result = []
        src_num = len(srcList)
        if 0 == src_num:
            return result
        gap_num = len(gap)
        dstIdx = seed % src_num
        gapIdx = seed % gap_num
        for idx in range(src_num):
            cnt = 0
            while srcList[dstIdx] in result and cnt <= src_num:
                cnt += 1
                dstIdx += 1
                if dstIdx >= src_num:
                    dstIdx = dstIdx % src_num
            result.append(srcList[dstIdx])
            gapIdx += 1
            if gapIdx >= gap_num:
                gapIdx = gapIdx % gap_num
            dstIdx = dstIdx + gap[gapIdx]
            if dstIdx >= src_num:
                dstIdx = dstIdx % src_num
        LOG_DBG('in listShuffle:', seed, srcList, result)
        return result

    def initTaskFromData(self, owner, taskId, taskCtx, alreadyCount=0, claimCount=0, taskRewardLimitDic=None):
        taskInfo = owner.taskInfo
        self.claimSrc = taskCtx.claimSrc
        self.seed = taskCtx.seed

        taskData = dataUtils.getTaskData(taskId)
        # LOG_DBG('in Task::initTaskFromData, taskId:', taskId, alreadyCount, claimCount, taskCtx.extra)
        self.setStat(owner, gameconst.TaskStat.TASK_STAT_RUNNING)
        self.claimCount = claimCount
        self.alreadyCount = alreadyCount
        self.taskRewardLimitDic = taskRewardLimitDic or {}
        self.startTime = utils.curTS()

        pointsDic = taskCtx.extra.get("pointsDic", {})
        self.pointsDic = {taskId: (pos[0], pos[1], pos[2]) for taskId, pos in pointsDic.items()}

        # childTasks
        cfgChildTaskIds = dataUtils.taskFieldVal(taskData, 'ChildTaskIds')
        if len(cfgChildTaskIds) > 0:
            checkLevel = 0
            if taskCtx.teamBaseInfoDic:
                teamLevels = taskCtx.teamBaseInfoDic.get('levels', [])
                if len(teamLevels) > 0:
                    checkLevel = sum(teamLevels) / len(teamLevels)

            checkLevel = checkLevel or gameglobal.roleCache.get(owner.id, {}).get('level', 1)
            checkLevel = int(checkLevel)
            childTaskIds = dataUtils.calcChildTaskIds(taskData, cfgChildTaskIds, checkLevel, seed=taskCtx.seed)
            if not childTaskIds:
                # 到这里说明配置错误(浮戏苍灵出现过)：父任务领取条件最低等级为0，但是所有子任务最低等级至少为20级，
                # 小于20级的玩家会出现没有可以领取的子任务的情况
                gameengine.panicStack('initTaskFromData, config error!!! no match child task:', taskId,
                                          cfgChildTaskIds)
                return False
            self.childTaskIds = childTaskIds

        self.teamId = taskCtx.teamId
        failedSec = dataUtils.taskFieldVal(taskData, 'FailCondTimeLimit')
        if failedSec > 0:
            failedSec = int(failedSec)
            if dataUtils.taskFieldVal(taskData, 'FailCondTimingOffline'):
                # 下线后依旧计时的任务
                self.expiredTime = utils.curTS() + failedSec
                taskInfo.addExpiredTimeTask(taskId, self.expiredTime)
            else:
                # 下线以后不再计时
                self.validSec = failedSec
                taskInfo.addValidSecTask(taskId, self.validSec)

        # 与活动关联的任务
        # failCondActId = dataUtils.taskFieldVal(taskData, 'FailCondActId')
        # if taskId in ACAD.taskId2actId and failCondActId:
        #     if failCondActId in gameconst.ACT_ID_CONST.FESTIVAL_ACTIVITY_IDS:
        #         festivalId = ACAD.datas[failCondActId]['cntFestival']
        #         self.expiredTime = min(gameglobal.globalOpenedActDic.get(int(failCondActId), 0),
        #                                gameglobal.globalOpenedFestivalDic.get(festivalId, 0))
        #     else:
        #         self.expiredTime = gameglobal.globalOpenedActDic.get(int(failCondActId), 0)

        # 计数任务
        checkValue = dataUtils.taskFieldVal(taskData, 'FinCondNeedCheckValue')
        if checkValue:
            values = dataUtils.taskFieldVal(taskData, 'FinCondCheckValue')
            for idx, valueData in enumerate(values):
                if valueData['Value'] <= 0:
                    continue
                tgt = TaskTargetInfo.TaskTgtFactory.createTarget(gameconst.TaskTargetType.TASK_TARGET_COUNT,
                                                                 idx, valueData['Value'], valueData['CompareType'])
                self.addNewTarget(tgt)

        # 杀怪任务
        hasKillMst = dataUtils.taskFieldVal(taskData, 'FinCondHasKillMon')
        if hasKillMst:
            tgtKillMonsters = dataUtils.taskFieldVal(taskData, 'FinCondKillMonster')
            killMonstersMode = dataUtils.taskFieldVal(taskData, 'FinCondKillMonsterMode')
            killMonstersTotalCount = dataUtils.taskFieldVal(taskData, 'FinCondKillMonsterNum')

            monsterIDs = set()

            for oneData in tgtKillMonsters:
                monsterId = oneData['MonsterId']
                if monsterId > 0:
                    monsterIDs.add(monsterId)

            for oneData in tgtKillMonsters:
                monsterId = oneData['MonsterId']
                dstCnt = oneData['Count']
                mapId = oneData['MapId']
                if killMonstersMode == 0:
                    if monsterId <= 0 or dstCnt <= 0:
                        continue
                elif killMonstersMode == 1:
                    if monsterId <= 0 or killMonstersTotalCount <= 0:
                        continue
                else:
                    LOG_ERR('in task, initTaskFromData, invalid arg 3:', killMonstersMode, monsterId, dstCnt)
                    continue

                tgt = TaskTargetInfo.TaskTgtFactory.createTarget(gameconst.TaskTargetType.TASK_TARGET_MONSTERS,
                                                                 monsterId, dstCnt, mapId, killMonstersMode, killMonstersTotalCount, monsterIDs)
                self.addNewTarget(tgt)

        # 收集物品任务
        hasGatherItems = dataUtils.taskFieldVal(taskData, 'FinCondHasGatherItems')
        if hasGatherItems:
            tgtItems = dataUtils.taskFieldVal(taskData, 'FinCondGatherItems')
            for oneData in tgtItems:
                itemId = oneData['ItemId']
                dstCnt = oneData['Count']
                if itemId <= 0 or dstCnt <= 0:
                    continue

                srcIdList = []
                srcIdStr = oneData.get("RelateMonster", '')
                if srcIdStr:
                    srcIdList.extend(srcIdStr.split('|'))
                srcIdStr = oneData.get("RelateCollect", '')
                if srcIdStr:
                    srcIdList.extend(srcIdStr.split('|'))
                srcRatio = oneData.get("Ratio", 0)
                itemCurNum = owner.getItemNum(itemId)
                tgt = TaskTargetInfo.TaskTgtFactory.createTarget(gameconst.TaskTargetType.TASK_TARGET_ITEMS,
                                                                 itemId, dstCnt, srcIdList, srcRatio,
                                                                 oneData.get("MapId", 0), itemCurNum)
                self.addNewTarget(tgt)

        # 交互采集任务
        hasInterCollect = dataUtils.taskFieldVal(taskData, 'FinCondHasInterCollect')
        if hasInterCollect:
            collData = dataUtils.taskFieldVal(taskData, 'FinCondInterCollect')
            for oneData in collData:
                collId = oneData['CollId']
                dstCnt = oneData['Count']
                mapId = oneData['MapId']
                if collId <= 0 or dstCnt <= 0:
                    continue
                tgt = TaskTargetInfo.TaskTgtFactory.createTarget(gameconst.TaskTargetType.TASK_TARGET_COLLECT,
                                                                 collId, dstCnt, mapId)

                self.addNewTarget(tgt)

        # 激活怪物图鉴任务
        if dataUtils.taskFieldVal(taskData, 'FinCondNeedActiveCard'):
            manualIdsStr = dataUtils.taskFieldVal(taskData, 'FinCondMonCardId')
            manualIds = manualIdsStr.split('|')
            for mid in manualIds:
                if not mid:
                    continue
                mid = int(mid)
                tgt = TaskTargetInfo.TaskTgtFactory.createTarget(gameconst.TaskTargetType.TASK_TARGET_MONSTER_CARD,
                                                                 mid, mid in owner.catchMonsterSet)
                self.addNewTarget(tgt)

        # 播放一个动作任务
        if dataUtils.taskFieldVal(taskData, 'FinCondIsTriggerAction'):
            for oneTgtData in dataUtils.taskFieldVal(taskData, 'FinCondTriggerAction'):
                actionId = oneTgtData.get('ActionId')
                if not actionId:
                    continue
                tgt = TaskTargetInfo.TaskTgtFactory.createTarget(gameconst.TaskTargetType.TASK_TARGET_ACTION,
                                                                 actionId, oneTgtData['MapId'])
                self.addNewTarget(tgt)

        # 与npc交谈任务
        tgtTalkToNpc = dataUtils.taskFieldVal(taskData, 'FinCondFinDialogs')
        for oneData in tgtTalkToNpc:
            npcIdStr = oneData['NPCId']
            dialogIdStr = oneData['DialogId']
            if not npcIdStr or not dialogIdStr:
                continue
            npcIdList = [int(npcId) for npcId in str(npcIdStr).split('|') if int(npcId) > 0]
            dialogIdList = [int(dialogId) for dialogId in str(dialogIdStr).split('|') if int(dialogId) > 0]
            if not npcIdList or not dialogIdList:
                continue
            tgt = TaskTargetInfo.TaskTgtFactory.createTarget(gameconst.TaskTargetType.TASK_TARGET_TALK_NPC,
                                                             npcIdList, dialogIdList, oneData['MapId'])
            self.addNewTarget(tgt)

        # 到达指定区域
        if dataUtils.taskFieldVal(taskData, 'FinCondIsTriggerArea'):
            if not pointsDic:
                rootTask = taskInfo.getRootTask(self.taskId)
                if rootTask:
                    pointsDic = rootTask.pointsDic
            rdPoint = None
            if pointsDic:
                rdPoint = pointsDic.get(self.taskId, None)
            tgt = TaskTargetInfo.TaskTgtFactory.createTarget(gameconst.TaskTargetType.TASK_TARGET_REACH_AREA,
                                                             dataUtils.taskFieldVal(taskData, 'FinCondReachArea'),
                                                             rdPoint)
            self.addNewTarget(tgt)
            taskInfo.addReachAreaTargetTask(taskId, tgt)

        # 到达某个等级
        dstLevel = dataUtils.taskFieldVal(taskData, 'FinCondToLevel')
        if dstLevel > 0:
            tgt = TaskTargetInfo.TaskTgtFactory.createTarget(gameconst.TaskTargetType.TASK_TARGET_LEVEL,
                                                             dstLevel)
            tgt.avatarLevelUp(owner.getAvatarLevel())
            self.addNewTarget(tgt)

        # 关联任务处于某个状态
        finRelateTaskIdsStr = dataUtils.taskFieldVal(taskData, 'FinCondRelateTaskId')
        # 注意这里，编辑器导出的 FinCondRelateTaskId 的数据还可能是: str类型的 '0', int 类型的 0, int 类型的 taskId
        finRelateTaskIdsStr = str(finRelateTaskIdsStr)
        if finRelateTaskIdsStr:
            relTaskIds = finRelateTaskIdsStr.split('|')
            for relTaskId in relTaskIds:
                # 编辑器导出后的数据，reltaskid可能为：'', '0'
                if not relTaskId:
                    continue
                relTaskId = int(relTaskId)
                if not relTaskId:
                    continue
                relTaskStat = owner.taskInfo.getTaskCurrentState(relTaskId)
                tgt = TaskTargetInfo.TaskTgtFactory.createTarget(gameconst.TaskTargetType.TASK_TARGET_RELATE_TASK,
                                                                 relTaskId, dataUtils.taskFieldVal(taskData,
                                                                                                   'FinCondRelateTaskState'),
                                                                 relTaskStat)
                self.addNewTarget(tgt)

        # 变量目标
        varFrmId = dataUtils.taskFieldVal(taskData, 'FinCondVarCheckFormID')
        if varFrmId:
            tgt = TaskTargetInfo.TaskTgtFactory.createTarget(gameconst.TaskTargetType.TASK_TARGET_VAR, varFrmId)
            tgt.checkVarCond(owner, varFrmId, dataUtils.taskFieldVal(taskData, 'FinCondVarCheckParam'))
            self.addNewTarget(tgt)

        # 计次目标
        counterId = dataUtils.taskFieldVal(taskData, 'FinCondCountID')
        dstCnt = dataUtils.taskFieldVal(taskData, 'FinCondCountTgt')
        counterParam = dataUtils.taskFieldVal(taskData, 'FinCondCountParam')
        if counterId and dstCnt:
            # if counterId == TCTTD.couterTargetDic['TaskCounterTargetXZKY']:
            #     curCnt = owner.achieveInfo.achieveScore
            # else:
            curCnt = 0
            tgt = TaskTargetInfo.TaskTgtFactory.createTarget(gameconst.TaskTargetType.TASK_TARGET_COUNTER, counterId,
                                                             dstCnt,
                                                             counterParam, curCnt)
            self.addNewTarget(tgt)
        return True

    def setStat(self, owner, stat):
        if self.stat != stat:
            LOG_IFO('Task::setStat, taskId {}, {} ==> {}'.format(self.taskId, self.stat, stat))

            self.stat = stat
            owner.onTaskStateChanged(self.taskId, stat)

            mapId = 0
            data = RRTID.datas.get(self.taskId, None)
            if data:
                mapId = data['mapID']
            
            LogTrackingMgr.LogTrackingMgr.Task_State_Change(owner.gbID, self.taskId, self.stat, self.taskType, mapId, owner.getRoleCacheAttr('level'))
        return

    def isStat(self, stat):
        return self.stat == stat

    def isInEndStat(self):
        # 任务是否处于最终状态
        return self.stat in [gameconst.TaskStat.TASK_STAT_SUBMITTED, gameconst.TaskStat.TASK_STAT_QUIT]

    def isTaskExpired(self):
        return 0 < self.expiredTime <= utils.curTS()

    def canAddRewardId(self, taskId, rewardId, rewardMaxNum=1):
        hasRewardTimes = self.taskRewardLimitDic.get(taskId, {}).get(rewardId, 0)
        if hasRewardTimes >= rewardMaxNum:
            LOG_IFO('in canAddRewardId, hasRewardTimes > rewardMaxNum:', taskId, rewardId, hasRewardTimes,
                      rewardMaxNum)
            return False
        else:
            return True

    def recordSubmitTaskRewardId(self, taskId, rewardId):
        self.taskRewardLimitDic.setdefault(taskId, {})
        self.taskRewardLimitDic[taskId][rewardId] = self.taskRewardLimitDic[taskId].get(rewardId, 0) + 1

    def updateTgtItemsCount(self, owner):
        LOG_DBG('in Task::updateItemsCount')
        update = False
        tgtList = self.getTgtsByType(gameconst.TaskTargetType.TASK_TARGET_ITEMS)
        for tgt in tgtList:
            itemCnt = owner.getItemNum(tgt.tgtId)
            if tgt.stepCnt == itemCnt:
                continue
            update = True
            tgt.stepCnt = min(itemCnt, tgt.dstCnt)
        return update

    def getTaskTgtItemsWealthVal(self):
        deductWealthVal = dropAward.DeductWealthVal()
        tgtList = self.getTgtsByType(gameconst.TaskTargetType.TASK_TARGET_ITEMS)
        for tgt in tgtList:
            deductWealthVal.addWealthByItemId(tgt.tgtId, tgt.dstCnt, dataUtils.getItemDefaultBindType())
        return deductWealthVal

    def deductTaskTgtItemsSucc(self):
        tgtList = self.getTgtsByType(gameconst.TaskTargetType.TASK_TARGET_ITEMS)
        for tgt in tgtList:
            tgt.deductItemsSucc()
        return

    def checkTgtRelateTaskStat(self, relateTaskId, relateTaskStat):
        target = self.findTargetByTypeAndId(gameconst.TaskTargetType.TASK_TARGET_RELATE_TASK, relateTaskId)
        return target and target.relateTaskReachStat(relateTaskId, relateTaskStat)

    def updateTaskTgtCnt(self, idx, timeList):
        LOG_DBG('in updateTaskTgtCnt:', idx, timeList)
        target = self.findTargetByTypeAndId(gameconst.TaskTargetType.TASK_TARGET_COUNT, idx)
        if target is None:
            LOG_WARN('       in updateTaskTgtCnt, no count target:', idx, timeList)
            return
        return target.addMultiCnt(idx, timeList)

    def updateCounterTarget(self, targetId, params):
        LOG_DBG('in updateTaskTgtCnt:', targetId, params)
        target = self.findTargetByTypeAndId(gameconst.TaskTargetType.TASK_TARGET_COUNTER, targetId)
        if target is None:
            LOG_WARN('       in updateCounterTarget, no counter target:', self.taskId, targetId)
            return
        return target.counter(targetId, params)

    def isEmptyTarget(self):
        return len(self.targetDic) == 0

    def checkAllTargetsReached(self):
        if self.isStat(gameconst.TaskStat.TASK_STAT_FINISHED):
            return True
        for tgt in self.getAllTargets():
            if not tgt.isTargetCompleted():
                return False
        return True

    def setActionTgtCompleted(self, actionId):
        actTgtList = self.getTgtsByType(gameconst.TaskTargetType.TASK_TARGET_ACTION)
        updated = False
        tgtArrived = False
        for tgt in actTgtList:
            if tgt.tgtId != actionId:
                continue
            if not tgt.isTargetCompleted():
                updated = True
            tgt.setTargetCompleted()
            tgtArrived = True
        return updated, tgtArrived

    def setAllTargetsReached(self, owner):
        LOG_IFO('in Task::setAllTargetsReached:', self.taskId)
        for tgt in self.getAllTargets():
            tgt.setTargetCompleted()

        self.setStat(owner, gameconst.TaskStat.TASK_STAT_FINISHED)
        return

    def addGameEntityIdRecord(self, gameEntityId):
        gameEntityId = str(gameEntityId)
        if gameEntityId not in self.extraAttr.gameEntityDict:
            self.extraAttr.gameEntityDict[gameEntityId] = 0
        self.extraAttr.gameEntityDict[gameEntityId] += 1

    def addCollectNum(self, targetType, args):
        isAdd = False
        if targetType == gameconst.TaskTargetType.TASK_TARGET_COLLECT:
            tgtList = self.getTgtsByType(targetType)
            if not tgtList:
                return False
            for tgt in tgtList:
                result = tgt.addCollectNum(*args)
                if result:
                    isAdd = True
            return isAdd

    def addCounterNum(self, targetType, args):
        isAdd = False
        if targetType == gameconst.TaskTargetType.TASK_TARGET_COUNTER:
            tgtList = self.getTgtsByType(targetType)
            if not tgtList:
                return False
            for tgt in tgtList:
                result = tgt.counter(*args)
                if result:
                    isAdd = True
            return isAdd

    def onTaskStepUpdate(self, targetTye, args):
        tgtList = self.getTgtsByType(targetTye)
        tgtArrived = False
        if not tgtList:
            return False
        for tgt in tgtList:
            result = tgt.checkTargetCompleted(*args)
            if not result:
                continue
            LOG_DBG('onTaskProgressUpdate', result, targetTye, self.taskId, args)
            tgtArrived = True
        return tgtArrived


class TaskFactory(object):

    @classmethod
    def createTask(cls, owner, taskId, taskCtx, alreadyCount=0, claimCount=0, taskRewardLimitDic=None):
        if not taskId:
            gameengine.panicStack('invalid taskId:', taskId)
            return
        taskData = dataUtils.getTaskData(taskId)
        if not taskData:
            gameengine.panicStack('no taskdata:', taskId)
            return
        task = Task(taskId)
        task.initTaskFromData(owner, taskId, taskCtx, alreadyCount=alreadyCount, claimCount=claimCount,
                              taskRewardLimitDic=taskRewardLimitDic)
        return task

    @classmethod
    def createTaskBySavedDict(cls, savedDict):
        taskData = dataUtils.getTaskData(savedDict['taskId'])
        if not taskData:
            gameengine.panicStack('invalid taskId:', savedDict['taskId'])
            return
        task = Task(savedDict['taskId'], taskData=taskData)
        task.fromSavedDict(savedDict)
        return task

    @classmethod
    def createTaskByTaskObj(cls, owner, taskObj):
        taskData = dataUtils.getTaskData(taskObj.taskId)
        if not taskData:
            gameengine.panicStack('invalid taskId:', taskObj.taskId)
            return
        task = Task(taskObj.taskId)
        task.updateFromTaskObj(owner, taskObj)
        return task
