# -*- encoding:utf-8 -*-

import KBEngine
from KBEDebug import *
import utils
import dataUtils
import random
import gameengine
import gameconst
import math

import actionContext
import userType
import dropAward
import awardContext

import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import itemFactory
import taskItemSrc as TISD
import taskRelate as TRD
import rewardTask_taskInfo as RRTID
import rewardTask_config as RRTIC
import gameclass
import gameglobal
import Task
import gamelog
import formula
import visible_visible as V_VD


class TaskCountLimitType(object):
    TASK_LIMIT_CLAIM_COUNT = 0  # 领取任务时检查领取次数限制
    TASK_LIMIT_SUBMIT_COUNT = 1  # 提交任务时检查提交次数限制


class TaskInfo(userType.UserSoleType):
    def __init__(self):
        self.tasks = {}
        self.taskRecordDic = {}
        self.sendUpdateTasks = {}

        self.taskId2ValidSec = {}
        self.taskId2expiredTime = {}
        self.areaTargetTaskDic = {}

        self.rewardTaskCacheDic = {}

        self.curTryEnterDunData = {}

        # 每周悬赏任务完成次数
        self.hookRewardTaskFnsNumWeekly = 0
        # 同时进行的悬赏任务个数
        self.hookRewardTaskNum = 0
        # 悬赏任务列表
        self.hookRewardTaskIdListWeekly = []
        self.hookRewardTaskIdListDaily = []
        # 附灵随机任务权重
        self.randomTaskWeights = {}

    def isTaskComplete(self, taskId):
        return self.getTaskCurrentState(taskId) == gameconst.TaskStat.TASK_STAT_SUBMITTED

    def isTaskRunning(self, taskId):
        return self.getTaskCurrentState(taskId) == gameconst.TaskStat.TASK_STAT_RUNNING

    def getTaskCurrentState(self, taskId):
        task = self.getTask(taskId)
        if task:
            return task.stat
        return self._taskStateNoTaskObj(taskId)

    def _taskStateNoTaskObj(self, taskId):
        # 任务不在当前任务列表里的情况
        taskData = dataUtils.getTaskData(taskId)
        if not taskData:
            ERROR_MSG('_taskStateNoTaskObj task not config', taskId)
            return self.taskRecordDic.get(taskId, gameconst.TaskStat.TASK_STAT_UNKNOWN)

        parentTaskId = dataUtils.taskFieldVal(taskData, 'FatherTaskId')
        if parentTaskId == 0:
            # taskId已经是根任务
            return self.taskRecordDic.get(taskId, gameconst.TaskStat.TASK_STAT_UNKNOWN)
        parentTask = self.getTask(parentTaskId)
        if parentTask:
            if parentTask.isInEndStat():
                return parentTask.stat
            else:
                return gameconst.TaskStat.TASK_STAT_UNKNOWN
        return self._taskStateNoTaskObj(parentTaskId)

    def isTaskInStat(self, taskId, state):
        return self.getTaskCurrentState(taskId) == state

    def _lateReload(self):
        super(TaskInfo, self)._lateReload()

        for v in self.tasks.values():
            v.reloadScript()

        for v in self.sendUpdateTasks.values():
            v.reloadScript()
        return

    def toTaskInfoSavedDict(self):
        self.dealEndTasks()
        dic = {'taskList': [], 'submitTaskIdList': [], 'quitTaskIdList': []}
        for taskId, task in self.tasks.items():
            dic['taskList'].append(task)
        for taskId, taskStat in self.taskRecordDic.items():
            if taskStat == gameconst.TaskStat.TASK_STAT_SUBMITTED:
                dic['submitTaskIdList'].append(taskId)
            elif taskStat == gameconst.TaskStat.TASK_STAT_QUIT:
                dic['quitTaskIdList'].append(taskId)

        if len(dic['taskList']) > 100:
            # blob最多存300+任务
            gameengine.reportCritical('attention!!! taskList num greater 100:', len(dic['taskList']))

        if len(dic['submitTaskIdList']) > 10000:
            # blob最多存 13000+ 任务
            gameengine.reportCritical('attention!!! submitTaskIdList num greater 10000:', len(dic['submitTaskIdList']))

        if len(dic['quitTaskIdList']) > 10000:
            # blob最多存 13000+ 任务
            gameengine.reportCritical('attention!!! quitTaskIdList num greater 10000:', len(dic['quitTaskIdList']))

        dic['rewardTaskCacheDic'] = self.rewardTaskCacheDic
        dic['hookRewardTaskFnsNumWeekly'] = self.hookRewardTaskFnsNumWeekly
        dic['hookRewardTaskNum'] = self.hookRewardTaskNum
        dic['hookRewardTaskIdListWeekly'] = self.hookRewardTaskIdListWeekly
        dic['hookRewardTaskIdListDaily'] = self.hookRewardTaskIdListDaily
        dic['randomTaskWeights'] = self.randomTaskWeights
        return dic

    def toTaskInfoClientDict(self):
        dic = {'taskList': [], 'submitTaskIdList': [], 'quitTaskIdList': []}
        for taskId, task in self.tasks.items():
            dic['taskList'].append(task.toTaskClientDict())
        for taskId, taskStat in self.taskRecordDic.items():
            if taskStat == gameconst.TaskStat.TASK_STAT_SUBMITTED:
                dic['submitTaskIdList'].append(taskId)
            elif taskStat == gameconst.TaskStat.TASK_STAT_QUIT:
                dic['quitTaskIdList'].append(taskId)
        dic['hookRewardTaskFnsNumWeekly'] = self.hookRewardTaskFnsNumWeekly
        dic['hookRewardTaskNum'] = self.hookRewardTaskNum
        dic['hookRewardTaskIdListWeekly'] = self.hookRewardTaskIdListWeekly
        dic['hookRewardTaskIdListDaily'] = self.hookRewardTaskIdListDaily
        return dic

    def fromSavedDict(self, dataDic):
        self.tasks = {}
        for task in dataDic['taskList']:
            if not task:
                WARNING_MSG('fromSavedDict, task is None')
                continue
            self.tasks[task.taskId] = task
            if task.parentTaskId != 0:
                continue

        for taskId in dataDic.get('submitTaskIdList', []):
            self.taskRecordDic[taskId] = gameconst.TaskStat.TASK_STAT_SUBMITTED
        for taskId in dataDic.get('quitTaskIdList', []):
            self.taskRecordDic[taskId] = gameconst.TaskStat.TASK_STAT_QUIT

        self.rewardTaskCacheDic = dataDic.get('rewardTaskCacheDic', {})
        self.hookRewardTaskFnsNumWeekly = dataDic.get('hookRewardTaskFnsNumWeekly', 0)
        self.hookRewardTaskNum = dataDic.get('hookRewardTaskNum', 0)
        self.hookRewardTaskIdListWeekly = dataDic.get('hookRewardTaskIdListWeekly', [])
        self.hookRewardTaskIdListDaily = dataDic.get('hookRewardTaskIdListDaily', [])
        self.randomTaskWeights = dataDic.get('randomTaskWeights', {})
        return

    @classmethod
    def _checkIgnores_(cls):
        # 角色登陆时候根据任务数据构建的数据
        return 'taskId2ValidSec', 'taskId2expiredTime', 'areaTargetTaskDic', 'curTryEnterDunData'

    def recordOnceTask(self, taskId, taskStat):
        self.taskRecordDic[taskId] = taskStat

    def dealEndTasks(self):
        endRootTaskIds = []
        for taskId, task in self.tasks.items():
            if task.parentTaskId != 0:
                continue
            if task.isInEndStat():
                endRootTaskIds.append(task.taskId)

        # 将已提交或已放弃的根任务的所有子任务移除列表
        for endTaskId in endRootTaskIds:
            self.remChildTask(endTaskId)

        # 处理已经完结（成功或者放弃）的任务
        removeTaskIds = []
        for taskId in endRootTaskIds:
            task = self.getTask(taskId)
            taskData = dataUtils.getTaskData(task.taskId)
            # 任务已经完结（成功或者放弃），清理任务列表的这部分数据并按需记录状态
            if gameconst.TaskCycleType.TASK_CYCLE_NONE == task.cycleType:
                # 非周期任务
                if task.isStat(gameconst.TaskStat.TASK_STAT_SUBMITTED):
                    if not dataUtils.taskFieldVal(taskData, 'OpenCondRepeatIfSucess'):
                        # 任务成功后不能重复开启, 记录任务状态
                        removeTaskIds.append(taskId)
                        self.recordOnceTask(taskId, task.stat)
                elif task.isStat(gameconst.TaskStat.TASK_STAT_QUIT):
                    if not dataUtils.taskFieldVal(taskData, 'OpenCondRepeatIfFail'):
                        # 任务放弃后不能重复开启, 记录任务状态
                        removeTaskIds.append(taskId)
                        self.recordOnceTask(taskId, task.stat)
            elif gameconst.TaskCycleType.TASK_CYCLE_ONCE == task.cycleType:
                # 单次开启的任务
                openCondTaskeState = dataUtils.taskFieldVal(taskData, 'OpenCondTaskeState')
                if openCondTaskeState == TaskCountLimitType.TASK_LIMIT_CLAIM_COUNT and task.limitCount != 0 and task.claimCount >= task.limitCount:
                    # 领取次数已满，移除任务并记录状态
                    removeTaskIds.append(taskId)
                    self.recordOnceTask(taskId, task.stat)
                elif openCondTaskeState == TaskCountLimitType.TASK_LIMIT_SUBMIT_COUNT and task.limitCount != 0 and task.alreadyCount >= task.limitCount:
                    # 提交次数已满，移除任务并记录状态
                    removeTaskIds.append(taskId)
                    self.recordOnceTask(taskId, task.stat)
        if removeTaskIds:
            INFO_MSG('in dealAlreadyFinTasks, removeTaskIds:', removeTaskIds)
        for remTaskId in removeTaskIds:
            self.remTask(remTaskId)
        return

    def _constructHookRewardTaskList(self, taskNum, taskSrcList, myLevel):
        exist_set = set()
        for taskId, task in self.tasks.items():
            if task.parentTaskId != 0:
                continue
            if task.taskType != gameconst.TaskType.TASK_TYPE_HOOK_REWARD:
                continue
            exist_set.add(taskId)
        result_list = []
        for taskId in taskSrcList:
            taskData = RRTID.datas.get(taskId)
            if not taskData:
                gameengine.reportCritical('getTaskData from RRTID, no taskdata:', taskId)
                continue
            ClaimCondLevelMin = taskData.get('minLevel', 0)
            ClaimCondLevelMax = taskData.get('maxLevel', 0)
            if myLevel < ClaimCondLevelMin or myLevel > ClaimCondLevelMax:
                continue
            if taskId not in exist_set:
                result_list.append(taskId)
        taskNum = min(taskNum, len(result_list))
        return random.sample(result_list, taskNum)

    def initNoviceHookRewardTask(self):
        hookRewardTaskNum = RRTIC.datas.get('dailyLimitNum', {}).get('value', 0)
        myLevel = 0
        self.hookRewardTaskIdListDaily = self._constructHookRewardTaskList(hookRewardTaskNum, RRTID.DailyTaskList, myLevel)
        hookRewardTaskNum = RRTIC.datas.get('weeklyLimitNum', {}).get('value', 0)
        self.hookRewardTaskIdListWeekly = self._constructHookRewardTaskList(hookRewardTaskNum, RRTID.WeeklyTaskList, myLevel)
        self.hookRewardTaskFnsNumWeekly = 0

    def refreshHookRewardTask(self, level):
        hookRewardTaskNum = RRTIC.datas.get('dailyLimitNum', {}).get('value', 0)
        self.hookRewardTaskIdListDaily = self._constructHookRewardTaskList(hookRewardTaskNum, RRTID.DailyTaskList, level)
        hookRewardTaskNum = RRTIC.datas.get('weeklyLimitNum', {}).get('value', 0)
        self.hookRewardTaskIdListWeekly = self._constructHookRewardTaskList(hookRewardTaskNum, RRTID.WeeklyTaskList, level)
        self.hookRewardTaskFnsNumWeekly = 0

    def _afterTaskUpdateRemoved(self, owner, removeTaskIds):
        DEBUG_MSG("_afterTaskUpdateRemoved", removeTaskIds)
        for taskId in removeTaskIds:
            owner.deleteTemporarySkillByTask(taskId)

    def doTaskDailyUpdate(self, owner, myLevel):
        finDailyTaskIds = []
        hookRewardTaskNum = RRTIC.datas.get('dailyLimitNum', {}).get('value', 0)
        self.hookRewardTaskIdListDaily = self._constructHookRewardTaskList(hookRewardTaskNum, RRTID.DailyTaskList, myLevel)
        removeTaskIds = []
        for taskId, task in self.tasks.items():
            if task.parentTaskId != 0:
                continue
            if gameconst.TaskCycleType.TASK_CYCLE_DAYLY != task.cycleType:
                continue
            if task.isInEndStat():
                finDailyTaskIds.append(taskId)
            else:
                task.claimCount = 0
                task.alreadyCount = 0
                task.taskRewardLimitDic.clear()
                self.addSendUpdatedTaskList([task, ])

        for remTaskId in finDailyTaskIds:
            if self.remTask(remTaskId):
                removeTaskIds.append(remTaskId)
            removeTaskIds.extend(self.remChildTask(remTaskId))
        DEBUG_MSG('in doTaskDailyUpdate, removeTaskIds:', removeTaskIds)
        self._afterTaskUpdateRemoved(owner, removeTaskIds)
        return removeTaskIds

    def doTaskWeeklyUpdate(self, owner, myLevel):
        finDailyTaskIds = []
        hookRewardTaskNum = RRTIC.datas.get('weeklyLimitNum', {}).get('value', 0)
        self.hookRewardTaskIdListWeekly = self._constructHookRewardTaskList(hookRewardTaskNum, RRTID.WeeklyTaskList, myLevel)
        self.hookRewardTaskFnsNumWeekly = 0
        for taskId, task in self.tasks.items():
            if task.parentTaskId != 0:
                continue
            if gameconst.TaskCycleType.TASK_CYCLE_WEEKLY != task.cycleType:
                continue
            if task.isInEndStat():
                finDailyTaskIds.append(taskId)
            else:
                task.claimCount = 0
                task.alreadyCount = 0
                task.taskRewardLimitDic.clear()
                self.addSendUpdatedTaskList([task, ])

        removeTaskIds = []
        for remTaskId in finDailyTaskIds:
            if self.remTask(remTaskId):
                removeTaskIds.append(remTaskId)
            removeTaskIds.extend(self.remChildTask(remTaskId))
        DEBUG_MSG('in doTaskWeeklyUpdate, removeTaskIds:', removeTaskIds)
        self._afterTaskUpdateRemoved(owner, removeTaskIds)
        return removeTaskIds

    def addSendUpdatedTaskList(self, tasksList):
        for task in tasksList:
            self.sendUpdateTasks[task.taskId] = task

    def resetUpdatedTaskList(self):
        self.sendUpdateTasks = {}

    def sendUpdatedTaskNow(self, owner, task):
        DEBUG_MSG('in sendUpdatedTaskNow:', task.taskId, task.stat)
        owner.client.onTaskUpdate([task.toTaskClientDict(), ])
        self.sendUpdateTasks.pop(task.taskId, None)

    def doSendUpdateTasksToClient(self, owner):
        if self.sendUpdateTasks:
            DEBUG_MSG('     in doSendUpdateTasksToClient:', [(t.taskId, t.stat) for t in self.sendUpdateTasks.values()])
            owner.client.onTaskUpdate([task.toTaskClientDict() for task in self.sendUpdateTasks.values()])
            self.sendUpdateTasks = {}

    def sendHookRewardTaskList(self, owner):
        DEBUG_MSG('     in sendHookRewardTaskList daily list: ', self.hookRewardTaskIdListDaily, ' weekly list: ', self.hookRewardTaskIdListWeekly)
        DEBUG_MSG('     in sendHookRewardTaskList self.hookRewardTaskFnsNumWeekly: ', self.hookRewardTaskFnsNumWeekly, 'self.hookRewardTaskNum', self.hookRewardTaskNum)
        owner.client.onHookRewardTaskRefresh(self.hookRewardTaskIdListWeekly + self.hookRewardTaskIdListDaily)
        owner.client.onHookRewardTaskWeeklyLimitRefresh(self.hookRewardTaskFnsNumWeekly)

    def doUpdateTaskTimeout(self, owner, passSec=1):
        expiredTaskIds = []
        for taskId in self.taskId2ValidSec.keys():
            task = self.getTask(taskId)
            if not task:
                continue
            task.validSec -= passSec
            if task.validSec <= 0:
                expiredTaskIds.append(taskId)
        for failedTaskId in expiredTaskIds:
            self.taskId2ValidSec.pop(failedTaskId, None)
            task = self.getTask(failedTaskId)
            not task.isInEndStat() and self.doTaskFailed(owner, failedTaskId, gameconst.TaskNotSuccReason.TIMEOUT)
        expiredTaskIds = []
        for taskId in self.taskId2expiredTime.keys():
            task = self.getTask(taskId)
            if not task:
                continue
            if task and task.isTaskExpired():
                expiredTaskIds.append(taskId)

        for failedTaskId in expiredTaskIds:
            self.taskId2expiredTime.pop(failedTaskId, None)
            INFO_MSG('in doUpdateTaskTimeout task expired:', failedTaskId)
            task = self.getTask(failedTaskId)
            not task.isInEndStat() and self.doTaskFailed(owner, failedTaskId, gameconst.TaskNotSuccReason.TIMEOUT)
        self.doSendUpdateTasksToClient(owner)
        return

    def checkExpiredTaskOnLogin(self, owner):
        self.taskId2ValidSec.clear()
        self.taskId2expiredTime.clear()
        now = utils.getNow()
        expiredTaskIds = []
        for taskId, task in self.tasks.items():
            if task.isInEndStat():
                continue
            if task.validSec > 0:
                self.addValidSecTask(taskId, task.validSec)
                continue
            if task.isTaskExpired():
                # is expired
                expiredTaskIds.append(taskId)
                continue
            if task.expiredTime > now:
                self.addExpiredTimeTask(taskId, task.expiredTime)
                continue

        for failedTaskId in expiredTaskIds:
            INFO_MSG('in checkExpiredTaskOnLogin, failedTaskId:', failedTaskId)
            self.doTaskFailed(owner, failedTaskId, gameconst.TaskNotSuccReason.TIMEOUT)

    def initTaskCacheOnLogin(self, owner):
        self.areaTargetTaskDic.clear()
        for taskId, task in self.tasks.items():
            if task.isInEndStat():
                continue
            targetList = task.getTgtsByType(gameconst.TaskTargetType.TASK_TARGET_REACH_AREA)
            for target in targetList:
                self.addReachAreaTargetTask(taskId, target)
                owner.cell.onAreaTargetTaskAdd(taskId, target)

    def checkRewardTaskCacheOnLogin(self, owner):
        if not self.rewardTaskCacheDic:
            return
        DEBUG_MSG('checkRewardTaskCacheOnLogin:', self.rewardTaskCacheDic)
        for taskId in self.rewardTaskCacheDic.keys():
            owner.cell.startClaimTask(taskId, '', (),
                                      actionContext.ClaimTaskCtx(claimSrc=gameconst.ClaimTaskSrc.REWARD_TASK))

    def removeRewardTaskCache(self, taskId):
        self.rewardTaskCacheDic.pop(taskId, None)

    def addValidSecTask(self, taskId, validSec):
        if validSec <= 0:
            return
        self.taskId2ValidSec[taskId] = validSec
        return

    def remValidSecTask(self, taskId):
        self.taskId2ValidSec.pop(taskId, None)

    def addExpiredTimeTask(self, taskId, expiredTime):
        if utils.getNow() > expiredTime:
            return
        self.taskId2expiredTime[taskId] = expiredTime

    def remExpiredTimeTask(self, taskId):
        self.taskId2expiredTime.pop(taskId, None)

    def addReachAreaTargetTask(self, taskId, target):
        self.areaTargetTaskDic[taskId] = target

    def remReachAreaTargetTask(self, owner, taskId):
        target = self.areaTargetTaskDic.pop(taskId, None)
        if target and owner.cell:
            owner.cell.removeAreaTargetTask(taskId, target.mapId)

    def removeTaskCache(self, taskId):
        self.remValidSecTask(taskId)
        self.remExpiredTimeTask(taskId)

    def getTask(self, taskId):
        return self.tasks.get(taskId, None)

    def remTask(self, taskId):
        self.removeTaskCache(taskId)
        return self.tasks.pop(taskId, None)

    def remChildTask(self, taskId):
        # 只清除子任务
        remTaskIds = []
        for childTaskId in self.getChildTaskIds(taskId):
            if self.remTask(childTaskId):
                remTaskIds.append(childTaskId)
        remTaskIds and INFO_MSG('cleanTask, remTaskIds:', taskId, remTaskIds)
        return remTaskIds

    def hasBagSpaceForClaimTask(self, owner, taskId):
        taskData = dataUtils.getTaskData(taskId)
        if dataUtils.taskFieldVal(taskData, 'ClaimCanRewardITems'):
            awardVal = dropAward.AwardVal()
            for rewardItems in dataUtils.taskFieldVal(taskData, 'ClaimRewardItems'):
                if not rewardItems['ItemId']:
                    continue
                # if dataUtils.isTaskItem(rewardItems['ItemId']):
                #     continue
                awardVal.addWealthByItemId(rewardItems['ItemId'], rewardItems['Count'])
            srcType = AAC_AACDD.datas.BONUS_SRC_CLAIM_TASK
            awardCtx = awardContext.CommonContext(0)
            if not owner.canAddWealthVal(srcType, awardVal, awardCtx):
                return False

        for childTaskId in dataUtils.taskFieldVal(taskData, 'ChildTaskIds'):
            if not self.hasBagSpaceForClaimTask(owner, childTaskId):
                return False
        return True

    @staticmethod
    def giveClaimTaskItems(owner, opUUID, taskData):
        if not dataUtils.taskFieldVal(taskData, 'ClaimCanRewardITems'):
            return
        ClaimRewardItems = dataUtils.taskFieldVal(taskData, 'ClaimRewardItems')
        validItems = {}
        for rewardItems in ClaimRewardItems:
            itemId = rewardItems['ItemId']
            itemNum = rewardItems['Count']
            if itemId == 0 or itemNum == 0:
                continue
            validItems[itemId] = itemNum

        if 0 == len(validItems):
            return
        rewardDic = {}
        ClaimRandomItems = dataUtils.taskFieldVal(taskData, 'ClaimRandomItems')
        if ClaimRandomItems:
            itemKeys = list(validItems.keys())
            rewardKey = random.choice(itemKeys)
            rewardDic[rewardKey] = validItems[rewardKey]
        else:
            rewardDic = validItems
        src = AAC_AACDD.datas.BONUS_SRC_CLAIM_TASK
        detail = gameclass.AwardDetail(taskId=[taskData['TaskId']])
        DEBUG_MSG('in giveClaimTaskItems, rewardDic:', rewardDic)
        wealthVal = dropAward.AwardVal()
        # itemList = []
        for itemId, itemNum in rewardDic.items():
            wealthVal.addWealthByItemId(itemId, itemNum, dataUtils.getItemDefaultBindType())
            # 出售获得的是货币，所以必定成功
        if owner.canAddWealthVal(src, wealthVal):
            owner.addWealth(src, wealthVal, opUUID, detail)
        else:
            return False
        # itemList and owner.addTaskItems(itemList, src, opUUID, detail)
        return

    @staticmethod
    def checkClaimTaskItemsCond(owner, taskId, taskData):
        if dataUtils.taskFieldVal(taskData, 'ClaimCondCheckItem'):
            ClaimCondCheckItemInfo = dataUtils.taskFieldVal(taskData, 'ClaimCondCheckItemInfo')
            # 至少有一个物品数量够
            hasAtLeastOneEnoughItem = False
            # 所有物品数量够
            hasAtAllEnoughItem = False
            lackItemInfo = {}
            deductVal = dropAward.DeductWealthVal()
            for oneInfo in ClaimCondCheckItemInfo['Items']:
                if oneInfo['ItemId'] > 0 and oneInfo['Count'] > 0:
                    deductVal.addWealthByItemId(oneInfo['ItemId'], oneInfo['Count'], dataUtils.getItemDefaultBindType())
                    if owner.getItemNum(oneInfo['ItemId']) >= oneInfo['Count']:
                        hasAtLeastOneEnoughItem = True
                    else:
                        lackItemInfo['itemId'] = oneInfo['ItemId']
                        lackItemInfo['itemNum'] = oneInfo['Count']

            if owner.canDeductWealth(deductVal, sendMsg=False):
                hasAtAllEnoughItem = True

            SatisfyOne = ClaimCondCheckItemInfo.get('SatisfyOne', False)
            NotOpenIfHas = ClaimCondCheckItemInfo.get('NotOpenIfHas', False)
            if NotOpenIfHas and SatisfyOne:
                # 有一个道具数量足够，就不能领取任务，返回False
                if hasAtLeastOneEnoughItem:
                    return gameclass.TaskCondResult(False)
            elif NotOpenIfHas and not SatisfyOne:
                # 所有道具数量都足够 ，不能领取任务，返回False
                if hasAtAllEnoughItem:
                    return gameclass.TaskCondResult(False)
            else:
                # 所有道具都满足，才能领取任务，否则返回False
                if not hasAtAllEnoughItem:
                    if lackItemInfo:
                        if dataUtils.isTeamTask(taskId):
                            playerName = owner.getRoleCacheAttr('name', '')
                            return gameclass.TaskCondResult(False, dataUtils.taskMsgId('taskClaimAlert_Team_ItemCheck'),
                                                            msgArgs=(playerName, str(lackItemInfo['itemId'])))
                        else:
                            return gameclass.TaskCondResult(False, dataUtils.taskMsgId('taskClaimAlert_ItemCheck'),
                                                            msgArgs=(
                                                                str(lackItemInfo['itemId']),
                                                                str(lackItemInfo['itemNum'])))
                    else:
                        return gameclass.TaskCondResult(False)
        return gameclass.TaskCondResult(True)

    @staticmethod
    def deductClaimTaskItems(owner, taskId, taskData):
        # 到这里说明任务可以领取
        if dataUtils.taskFieldVal(taskData, 'ClaimCondCheckItem'):
            ClaimCondCheckItemInfo = dataUtils.taskFieldVal(taskData, 'ClaimCondCheckItemInfo')
            OnlyCheck = ClaimCondCheckItemInfo.get('OnlyCheck', False)
            if OnlyCheck:
                return True
            deductWealthVal = dropAward.DeductWealthVal()
            for oneInfo in ClaimCondCheckItemInfo['Items']:
                if oneInfo['ItemId'] > 0 and oneInfo['Count'] > 0:
                    deductWealthVal.addWealthByItemId(oneInfo['ItemId'], oneInfo['Count'])

            DEBUG_MSG('in deductClaimTaskItems itemsDic:', deductWealthVal)
            if not owner.canDeductWealth(deductWealthVal):
                return False

            opUUID = KBEngine.genUUID64()
            srcType = AAC_AACDD.datas.BONUS_SRC_CLAIM_TASK
            detail = gameclass.AwardDetail(taskId=taskId)
            owner.deductWealth(srcType, deductWealthVal, opUUID, detail)
        return True

    def doClaimTask(self, owner, taskId, taskCtx):
        self.removeRewardTaskCache(taskId)
        taskData = dataUtils.getTaskData(taskId)
        # 这里根据配置扣除物品，如果出现错误，说明是之前检查逻辑有错
        if not self.deductClaimTaskItems(owner, taskId, taskData):
            gameengine.reportCritical('in doClaimTask, claim items deduct failed:', taskId)
            return

        remChildTaskIds = self.remChildTask(taskId)
        if len(remChildTaskIds) > 0:
            DEBUG_MSG('     in doClaimTask, remChildTaskIds:', remChildTaskIds)
            owner.client.onTasksRem(remChildTaskIds)

        # 子任务的 seed、enemyGuild信息、 teamId 要使用根任务的
        rootTask = self.getRootTask(taskId)
        if rootTask and rootTask.taskId != taskId:
            taskCtx.claimSrc = rootTask.claimSrc
            taskCtx.seed = rootTask.seed

        if 0 == taskCtx.seed:
            taskCtx.seed = random.randint(100, 10000)

        addTaskIds = self.addTask(owner, taskId, taskData, taskCtx)
        if not addTaskIds:
            gameengine.reportCritical('doClaimTask, addTaskIds:', addTaskIds)
            return
        self._afterTaskClaimed(owner, taskCtx, taskId, addTaskIds)
        owner.afterTaskClaimed(taskId)
        return addTaskIds

    def _afterTaskClaimed(self, owner, taskCtx, taskId, addTaskIds):
        client = []
        task = self.getTask(taskId)
        task.claimCount += 1
        opUUID = KBEngine.genUUID64()
        for addTaskId in addTaskIds:
            tmpTask = self.getTask(addTaskId)
            client.append(tmpTask.toTaskClientDict())
            owner.taskFlowLog(addTaskId, "TaskClaim", opUUID, claimSrc=taskCtx.claimSrc)

        owner.client.onClaimTask(taskId, client)
        # 先处理最下层子任务，最后处理根任务
        for addTaskId in reversed(addTaskIds):
            tmpTask = self.getTask(addTaskId)
            addTaskData = dataUtils.getTaskData(addTaskId)
            # 领取任务发放物品
            self.giveClaimTaskItems(owner, opUUID, addTaskData)

            DEBUG_MSG('in _afterTaskClaimed, addTaskId:', addTaskId, tmpTask.stat)
            # 播放剧情动画
            storyId = addTaskData.get('ClaimTriggerStoryID')
            if storyId:
                # 播放剧情动画
                owner.cell.prepareStartPlayCinema(storyId)
            if taskCtx.claimSrc!=gameconst.ClaimTaskSrc.GM_FINISH_NEWBIE:
                self._claimEnterDungeon(owner, addTaskData, tmpTask)

            # 领取任务事件处理
            owner.doTaskEvent(gameconst.EventActionSrc.SRC_CLAIM_TASK, addTaskId,
                              addTaskData.get('ClaimEventName', ''), addTaskData.get('ClaimEventParam', ''))


            # 如果是悬赏任务，则更新同时接取的限制状态
            if tmpTask.taskType == gameconst.TaskType.TASK_TYPE_HOOK_REWARD:
                if task.cycleType == gameconst.TaskCycleType.TASK_CYCLE_DAYLY \
                    or task.cycleType == gameconst.TaskCycleType.TASK_CYCLE_WEEKLY \
                    or task.cycleType == gameconst.TaskCycleType.TASK_CYCLE_ONCE:

                    self.hookRewardTaskNum += 1
            # 修改变量
            if addTaskData.get('ClaimCanVarMod'):
                varSrc = gameconst.VarChangeSrc.VAR_SRC_TASK_CLAIM
                for varData in addTaskData['ClaimVarModInfo']:
                    owner.taskSetVariable(addTaskId, opUUID, varSrc, varData['TargetVar'], varData['FormId'],
                                          varData['ParamVar'])
            if len(addTaskData.get('ChildTaskIds', [])) == 0:
                if tmpTask.isEmptyTarget():
                    # 没有目标的任务
                    if not addTaskData.get('FinCondNoLimit', False):
                        # 没有勾选"直接完成"，不需要 checkTaskFinished
                        continue
                    else:
                        # 勾选了"直接完成"
                        tmpTask.setStat(owner, gameconst.TaskStat.TASK_STAT_FINISHED)
                self.checkTaskFinished(owner, tmpTask)

            target = self.areaTargetTaskDic.get(addTaskId)
            target and owner.cell.onAreaTargetTaskAdd(addTaskId, target)
        self.doSendUpdateTasksToClient(owner)
        return

    def _claimEnterDungeon(self, owner, addTaskData, task):
        if dataUtils.taskFieldVal(addTaskData, 'ClaimCanTransIns'):
            claimTransData = dataUtils.taskFieldVal(addTaskData, 'ClaimTransInstance')
            needConfirm = claimTransData.get('NeedConfirm')
            # 需要弹窗二次确认的，检测是否非本地图，如果是本地图就直接过去，非本地图，就等玩家主动点击，走reqTaskEnterSpace主动进行进地图切换
            if needConfirm:
                DEBUG_MSG("_claimEnterDungeon, need confirm dialog to continue ", task)
                owner.cell.checkSameMap(task.taskId)
                return
            self._taskEnterSpace(owner, task.taskId, claimTransData)
        return

    def onCheckSameTaskResult(self, owner, task, isSame):
        DEBUG_MSG("onCheckSameTaskResult, chek result ", task, isSame)
        if not isSame:
            DEBUG_MSG("onCheckSameTaskResult, not same map, grant for client OP ", task)
            return
        taskCfg = dataUtils.getTaskData(task.taskId)
        # 如果是附灵任务, 则同地图, 不主动进行切换
        if dataUtils.taskFieldVal(taskCfg, 'TaskType') == gameconst.TaskType.TASK_TYPE_SPIRIT:
            DEBUG_MSG("onCheckSameTaskResult, stop spirit task telporting for same map~")
            return

        if not dataUtils.taskFieldVal(taskCfg, 'ClaimCanTransIns'):
            ERROR_MSG("onCheckSameTaskResult, wrong cfg ", taskCfg)
            return
        claimTransData = dataUtils.taskFieldVal(taskCfg, 'ClaimTransInstance')
        self._taskEnterSpace(owner, task.taskId, claimTransData)

    def _taskEnterSpace(self, owner, taskId, transData):
        dungeonNo = transData.get('MapId')
        useConfigPos = transData.get('UseConfigPos')
        dstPos = None
        dstDir = None
        if useConfigPos:
            dstPos = (transData['X'], transData['Y'], transData['Z'])
            dstDir = (0.0, 0.0, math.pi*transData.get('Dir', 0.0)/180)
        else:
            dstPos, dstDir = formula.whatSpaceBornPosAndDir(dungeonNo)

        owner.cell.taskPreEnterSpace(taskId, dungeonNo, dstPos, dstDir)
        self.curTryEnterDunData = {'dungeonNo':dungeonNo, 't':utils.getNow()}

    def getTaskItemIdList(self, taskId):
        itemIds = []
        taskData = dataUtils.getTaskData(taskId)
        gatherItemsInfo = dataUtils.taskFieldVal(taskData, 'FinCondGatherItems')
        for itemInfo in gatherItemsInfo:
            itemId = itemInfo['ItemId']
            if itemId > 0:
                itemIds.append(itemInfo['ItemId'])
        for childTaskId in dataUtils.taskFieldVal(taskData, 'ChildTaskIds'):
            childItemIds = self.getTaskItemIdList(childTaskId)
            itemIds.extend(childItemIds)
        return itemIds

    def taskSpaceNoChanged(self, spaceNo):
        dungeonNo = formula.getDungeonNoBySpaceNo(spaceNo)
        self.curTryEnterDunData.pop(dungeonNo, None)

    def isTaskTryingEnterDungeon(self, dungeonNo):
        curDungeonNo = self.curTryEnterDunData.get('dungeonNo')
        if curDungeonNo and curDungeonNo==dungeonNo and utils.getNow() - self.curTryEnterDunData['t'] <=1:
            # 任务已经触发进入副本，在此期间，客户端通过追踪面板进入副本要拦截住
            WARNING_MSG('task is trying enter dungeon')
            return True
        return False

    def canClaimTask(self, owner, taskId):
        taskData = dataUtils.getTaskData(taskId)
        if taskId in self.taskRecordDic:
            WARNING_MSG('       in canClaimTask, taskId in taskRecordDic')
            return gameclass.TaskCondResult(False)

        # 关联任务检查
        openRelTaskIdsStr = dataUtils.taskFieldVal(taskData, 'OpenCondRelateTaskId')
        if openRelTaskIdsStr and openRelTaskIdsStr != '0':
            # 编辑器导出的数据 openRelTaskIdsStr，有可能是 str类型'0', int 类型0，int类型任务id
            openRelTaskIdsStr = str(openRelTaskIdsStr)
            if openRelTaskIdsStr:
                relTaskIds = openRelTaskIdsStr.split('|')
                for relTaskId in relTaskIds:
                    if not relTaskId:
                        continue
                    if not self.isTaskInStat(int(relTaskId), dataUtils.taskFieldVal(taskData, 'OpenCondRelateTaskState')):
                        WARNING_MSG('     in canClaimTask, OpenCondRelateTask failed:', taskId)
                        return gameclass.TaskCondResult(False)

        # 校验物品
        itemCondResult = self.checkClaimTaskItemsCond(owner, taskId, taskData)
        if not itemCondResult:
            WARNING_MSG('       in canClaimTask, check items failed, taskId:', taskId)
            return itemCondResult

        # 领取任务后发放物品，检查背包空间是否足够
        if not self.hasBagSpaceForClaimTask(owner, taskId):
            WARNING_MSG('       in canClaimTask, space not enough')
            return gameclass.TaskCondResult(False, msgId=dataUtils.taskMsgId('taskClaimAlert_GetItem'))

        if dataUtils.taskFieldVal(taskData, 'TaskType') == gameconst.TaskType.TASK_TYPE_HOOK_REWARD:
            hookRewardTaskCheck = taskId in RRTID.DoOnceTaskList
            if hookRewardTaskCheck:
                data = RRTID.datas.get(taskId)
                if not data:
                    ERROR_MSG('       in canClaimTask, hookRewardTaskNum cfg not exist: ', taskId)
                    return gameclass.TaskCondResult(False)

                myLevel = owner.getAvatarLevel()
                ClaimCondLevelMin = data.get('minLevel', 0)
                if myLevel < ClaimCondLevelMin:
                    WARNING_MSG('       in canClaimTask, hookRewardTaskNum level limit, ', taskId, myLevel, ClaimCondLevelMin)
                    return gameclass.TaskCondResult(False)
            else:
                hookRewardTaskCheck |= taskId in self.hookRewardTaskIdListDaily
                hookRewardTaskCheck |= taskId in self.hookRewardTaskIdListWeekly

            if not hookRewardTaskCheck:
                WARNING_MSG('       in canClaimTask, hookRewardTaskId not in hookRewardTaskIdList, taskId is ', taskId, 'daily list is ', self.hookRewardTaskIdListDaily, 'weekly list is ', self.hookRewardTaskIdListWeekly, 'task count limit ', dataUtils.taskFieldVal(taskData, 'OpenCondCountLimit'))
                return gameclass.TaskCondResult(False)
            if self.hookRewardTaskFnsNumWeekly > RRTIC.datas.get('weeklyMaxNum', {}).get('value', 0) :
                WARNING_MSG('       in canClaimTask, hookRewardTaskFnsNumWeekly exceed at', self.hookRewardTaskFnsNumWeekly)
                return gameclass.TaskCondResult(False)
            if self.hookRewardTaskNum > RRTIC.datas.get('currentlyMaxNum', {}).get('value', 0) :
                WARNING_MSG('       in canClaimTask, hookRewardTaskNum exceed at', self.hookRewardTaskNum)
                return gameclass.TaskCondResult(False)

        # 开启变量检查
        fmlId = dataUtils.taskFieldVal(taskData, 'OpenCondVarCheckFormID')
        if fmlId and not dataUtils.checkVariableCond(owner, fmlId, dataUtils.taskFieldVal(taskData, 'OpenCondVarCheckParam')):
            WARNING_MSG('       in canClaimTask, open variable cond failed')
            return gameclass.TaskCondResult(False)

        # 领取变量条件
        fmlId = taskData.get('ClaimCondVarCheckFormID')
        if fmlId and not dataUtils.checkVariableCond(owner, fmlId, dataUtils.taskFieldVal(taskData, 'ClaimCondVarCheckParam')):
            WARNING_MSG('       in canClaimTask, claim variable cond failed')
            return gameclass.TaskCondResult(False)

        # # npc好感度条件校验
        # if dataUtils.taskFieldVal(taskData, 'OpenCondCheckFavor'):
        #     npcId = dataUtils.taskFieldVal(taskData, 'OpenCondFavorNpc')
        #     condFavorLevel = dataUtils.taskFieldVal(taskData, 'OpenCondFavorLevel')
        #     npcFavorLevel = owner.favorsInfo.getNpcFavorStep(npcId)
        #     if npcFavorLevel < condFavorLevel:
        #         return gameclass.TaskCondResult(False)

        task = self.getTask(taskId)
        if task is not None:
            # 以下条件，只校验根任务
            if task.parentTaskId != 0:
                return gameclass.TaskCondResult(True)

            if not task.isInEndStat():
                # 运行中或失败状态的任务不能重新领取
                WARNING_MSG('     in canClaimTask, task not in end state:', taskId)
                return gameclass.TaskCondResult(False)

            if task.cycleType == gameconst.TaskCycleType.TASK_CYCLE_NONE:
                # 成功后是否重复开启， 只对非周期任务有效
                if task.isStat(gameconst.TaskStat.TASK_STAT_SUBMITTED):
                    OpenCondRepeatIfSucess = dataUtils.taskFieldVal(taskData, 'OpenCondRepeatIfSucess')
                    if not OpenCondRepeatIfSucess:
                        # 成功后不允许再次开启
                        WARNING_MSG('     in canClaimTask, OpenCondRepeatIfSucess is False', taskId)
                        return gameclass.TaskCondResult(False)
                elif task.isStat(gameconst.TaskStat.TASK_STAT_QUIT):
                    OpenCondRepeatIfQuit = dataUtils.taskFieldVal(taskData, 'OpenCondRepeatIfFail')
                    if not OpenCondRepeatIfQuit:
                        # 任务放弃后不允许再次开启
                        WARNING_MSG('     in canClaimTask, OpenCondRepeatIfFail is False', taskId)
                        return gameclass.TaskCondResult(False)
            elif dataUtils.taskFieldVal(taskData, 'OpenCondTaskeState') == TaskCountLimitType.TASK_LIMIT_CLAIM_COUNT and task.limitCount != 0 and task.claimCount >= task.limitCount:
                # 领取任务领取次数已满，不能领取任务
                WARNING_MSG('     in canClaimTask, can not claim, task.claimCount >= task.limitCount:', task.claimCount, task.limitCount)
                return gameclass.TaskCondResult(False, dataUtils.taskMsgId('taskClaimAlert_TimesCheck'))

            elif dataUtils.taskFieldVal(taskData, 'OpenCondTaskeState') == TaskCountLimitType.TASK_LIMIT_SUBMIT_COUNT and task.limitCount != 0 and task.alreadyCount >= task.limitCount:
                # 提交次数已满，不能领取任务
                WARNING_MSG('     in canClaimTask, can not claim, task.alreadyCount >= task.limitCount:', task.alreadyCount, task.limitCount)
                return gameclass.TaskCondResult(False, dataUtils.taskMsgId('taskClaimAlert_TimesCheck'))

        return gameclass.TaskCondResult(True)

    def addTask(self, owner, taskId, taskData, taskCtx):
        addTaskIds = []
        oldTask = self.getTask(taskId)
        oldClaimCount = 0
        oldAlreadyCount = 0
        taskRewardLimitDic = {}
        if oldTask and oldTask.parentTaskId == 0:
            oldClaimCount = oldTask.claimCount
            oldAlreadyCount = oldTask.alreadyCount
            taskRewardLimitDic = oldTask.taskRewardLimitDic
        # 创建一个新任务对象
        task = Task.TaskFactory.createTask(owner, taskId, taskCtx, alreadyCount=oldAlreadyCount,
                                           claimCount=oldClaimCount,
                                           taskRewardLimitDic=taskRewardLimitDic)
        if not task:
            gameengine.reportCritical('     in addTask, create task error:', taskId)
            return
        self.tasks[taskId] = task
        addTaskIds.append(taskId)
        # childTasks
        childTaskIds = task.childTaskIds
        claimChildTaskIds = []
        if len(childTaskIds) > 0:
            if dataUtils.taskFieldVal(taskData, 'ChildDoInQueue'):
                # 顺序完成子任务
                claimChildTaskIds.append(childTaskIds[0])
            elif dataUtils.taskFieldVal(taskData, 'ChildDoInRandom'):
                if dataUtils.taskFieldVal(taskData, 'RandomWithWeight'):
                    taskId = self.calculateRandomTaskWithWeight(task, taskData)
                    claimChildTaskIds.append(taskId)
                    task.lastChildTaskId = taskId
                else:
                    # 随机完成子任务; 注意，连续两次随机到的任务不能是同一个，所以首先进行的子任务(位置0的子任务)
                    # 不能与 lastChildTaskId 相同
                    if oldTask and childTaskIds[0] == oldTask.lastChildTaskId and len(childTaskIds) > 1:
                        childTaskIds[0], childTaskIds[-1] = childTaskIds[-1], childTaskIds[0]
                    claimChildTaskIds.append(childTaskIds[0])
            elif dataUtils.taskFieldVal(taskData, 'ChildDoInSelection'):
                claimChildTaskIds = [ctid for ctid in childTaskIds]
            elif dataUtils.taskFieldVal(taskData, 'ChildDoInSameTime'):
                claimChildTaskIds = [ctid for ctid in childTaskIds]
            else:
                claimChildTaskIds = [ctid for ctid in childTaskIds]

        for childTaskId in claimChildTaskIds:
            childTaskData = dataUtils.getTaskData(childTaskId)
            addChildTaskIds = self.addTask(owner, childTaskId, childTaskData, taskCtx)
            if not addChildTaskIds:
                # 添加子任务失败，回溯父任务
                if oldTask:
                    self.tasks[taskId] = oldTask
                else:
                    self.remTask(taskId)
                gameengine.reportCritical('addTask error, addChildTaskIds:', addChildTaskIds)
                return None
            addTaskIds.extend(addChildTaskIds)
            task.lastChildTaskId = childTaskId
        return addTaskIds

    def calculateRandomTaskWithWeight(self, task, taskData):
        DEBUG_MSG("calculateRandomTaskWithWeight 0", task, taskData, self.randomTaskWeights)
        guaranteeCount = 0
        taskType = dataUtils.taskFieldVal(taskData, 'TaskType')
        if taskType == gameconst.TaskType.TASK_TYPE_SPIRIT:
            guaranteeCount = self.randomTaskWeights.get(task.taskId, 0) + 1
            self.randomTaskWeights[task.taskId] = guaranteeCount
            # 清理掉旧等级对应的权重数据
            allTaskIDs = list(self.randomTaskWeights)
            if len(allTaskIDs) > 1:
                for taskID in allTaskIDs:
                    if task.taskId == taskID:
                        continue
                    self.randomTaskWeights.pop(taskID, None)
        else:
            task.guaranteeCount += 1
            guaranteeCount = task.guaranteeCount

        DEBUG_MSG("calculateRandomTaskWithWeight 1", task, self.randomTaskWeights)
        # 到达指定次数，出保底
        if guaranteeCount >= dataUtils.taskFieldVal(taskData, 'GuaranteeCount'):
            guaranteeTaskId = dataUtils.taskFieldVal(taskData, 'GuaranteeTaskId')
            # 兼容不同版本的保底任务配置
            taskId = guaranteeTaskId
            if type(guaranteeTaskId) is list:
                taskId = random.choice(guaranteeTaskId)

            if taskType == gameconst.TaskType.TASK_TYPE_SPIRIT:
                self.randomTaskWeights.pop(task.taskId, 0)
            else:
                task.guaranteeCount = 0
            DEBUG_MSG("calculateRandomTaskWithWeight 2", task, taskId, self.randomTaskWeights)
            return taskId
        else:
            # 子任务对应的权重配置
            weights = dataUtils.taskFieldVal(taskData, 'ChildTaskWeights')
            # 抽取权重对应的索引位置
            randIdx = utils.randomByWeight(weights)
            # 根据索引位置取出子任务id
            taskId = task.childTaskIds[randIdx]
            DEBUG_MSG("calculateRandomTaskWithWeight 3", task, taskId, self.randomTaskWeights)
            # 抽到保底了，清零
            hasGuaranteeTaskId = False
            guaranteeTaskId = dataUtils.taskFieldVal(taskData, 'GuaranteeTaskId')
            # 兼容不同版本的保底任务配置
            if type(guaranteeTaskId) is list:
                if taskId in guaranteeTaskId:
                    hasGuaranteeTaskId = True
            elif taskId == guaranteeTaskId:
                hasGuaranteeTaskId = True

            if hasGuaranteeTaskId:
                if taskType == gameconst.TaskType.TASK_TYPE_SPIRIT:
                    self.randomTaskWeights.pop(task.taskId, 0)
                else:
                    task.guaranteeCount = 0
                DEBUG_MSG("calculateRandomTaskWithWeight 4", task, taskId, self.randomTaskWeights)
            return taskId

    def doRelateTaskReachStat(self, owner, relateTaskId, relateTaskStat):
        taskIds = TRD.datas.get(str(relateTaskId), {}).get(str(relateTaskStat))
        if not taskIds:
            return
        rmTasks = []
        for taskId in taskIds:
            task = self.getTask(taskId)
            if not task:
                continue
            if not task.isStat(gameconst.TaskStat.TASK_STAT_RUNNING):
                continue
            result = task.checkTgtRelateTaskStat(relateTaskId, relateTaskStat)
            if not result:
                continue
            INFO_MSG('     TaskInfo::doRelateTaskReachStat, taskId:', taskId, relateTaskId, relateTaskStat)
            rmTasks.append(task)
        for rmTask in rmTasks:
            self.checkTaskFinished(owner, rmTask)
            self.addSendUpdatedTaskList([rmTask, ])
        return

    def doAddTgtItemByRelateAction(self, owner, srcId, gameEntityId):
        if srcId <= 0:
            return
        taskIds = TISD.datas.get(str(srcId))
        if not taskIds:
            return
        wealthVal = dropAward.AwardVal()
        for taskId in taskIds:
            task = self.getTask(taskId)
            if task is None:
                continue
            if not task.isStat(gameconst.TaskStat.TASK_STAT_RUNNING):
                continue
            tgtList = task.getTgtsByType(gameconst.TaskTargetType.TASK_TARGET_ITEMS)
            for tgt in tgtList:
                DEBUG_MSG('     in doAddTgtItemByRelateAction, taskIds:', tgt.srcIdList, tgt.srcRatio)
                itemCount = owner.getItemNum(tgt.tgtId)
                if itemCount >= tgt.dstCnt:
                    continue
                if srcId not in tgt.srcIdList:
                    continue
                if tgt.srcRatio > 0:
                    rdDigit = random.randint(1, 100)
                    DEBUG_MSG('     in doAddTgtItemByRelateAction, random digit:', rdDigit)
                    if rdDigit > tgt.srcRatio:
                        continue
                    wealthVal.addWealthByItemId(tgt.tgtId, 1, dataUtils.getItemDefaultBindType())
        if not wealthVal.isEmpty():
            srcType = AAC_AACDD.datas.BONUS_SRC_ADD_TASK_ITEMS
            opUUID = KBEngine.genUUID64()
            detail = gameclass.AwardDetail(taskId=[taskIds[0] if taskIds else 0])
            awardCtx = awardContext.CommonContext(0)
            if not owner.canAddWealthVal(srcType, wealthVal, awardCtx):
                owner.onMessagePre(dataUtils.taskMsgId('taskSubmitAlert_BagCheck'), [])
                return
            owner.addWealth(srcType, wealthVal, opUUID, detail)

    def doTaskLeaveDungeon(self, owner, taskId):
        task = self.getTask(taskId)
        if not task:
            return
        if task.isInEndStat():
            return
        taskData = dataUtils.getTaskData(task.taskId)
        if dataUtils.taskFieldVal(taskData, 'FailCondFailIfQtInst'):
            # 离开副本任务失败
            DEBUG_MSG('     TaskInfo::doTaskLeaveDungeon, task failed:', taskId)
            self.doTaskFailed(owner, task.taskId, gameconst.TaskNotSuccReason.LEAVE_SPACE)

    def completeTargetAction(self, owner, taskId, actionId):
        task = self.getTask(taskId)
        if not task:
            return False, False
        if not task.isStat(gameconst.TaskStat.TASK_STAT_RUNNING):
            return False, False
        updated, tgtArrived = task.setActionTgtCompleted(actionId)
        if not updated:
            return updated, tgtArrived
        if tgtArrived:
            self.checkTaskFinished(owner, task)
        self.addSendUpdatedTaskList([task, ])
        return updated, tgtArrived

    def completeTaskNoTarget(self, owner, taskId):
        task = self.getTask(taskId)
        if not task:
            return
        self.checkTaskFinished(owner, task)
        return

    def doTaskVariableChanged(self, owner, taskId, varId):
        task = self.getTask(taskId)
        if not task or not task.isStat(gameconst.TaskStat.TASK_STAT_RUNNING):
            return

        DEBUG_MSG('doTaskVariableChanged:', task.taskId, varId)
        taskData = dataUtils.getTaskData(task.taskId)
        # 触发任务失败
        fmlId = dataUtils.taskFieldVal(taskData, 'FailCondVarCheckFormID')
        if fmlId and dataUtils.checkVariableCond(owner, fmlId,
                                                 dataUtils.taskFieldVal(taskData, 'FailCondVarCheckParam')):
            DEBUG_MSG('       doTaskVariableChanged, failed var is True')
            self.doTaskFailed(owner, task.taskId, gameconst.TaskNotSuccReason.VARIABLE)
            return

        # 触发任务目标完成
        fmlId = dataUtils.taskFieldVal(taskData, 'FinCondVarCheckFormID')
        if not fmlId:
            return
        tgts = task.getTgtsByType(gameconst.TaskTargetType.TASK_TARGET_VAR)
        for tgt in tgts:
            if tgt.checkVarCond(owner, fmlId, dataUtils.taskFieldVal(taskData, 'FinCondVarCheckParam')):
                self.checkTaskFinished(owner, task)
        return

    def checkTaskFinished(self, owner, task):
        # 任务可以设置为 TASK_STAT_FINISHED 的情况(李策)，在任务目标都已经完成的前提下，有以下3种情况：
        # 1.其下的某个子任务完成提交操作，并且设置了 FaterSuccIfChildSucc
        # 2.其下的所有子任务都已提交
        # 3.服务器使其完成
        if not task.checkAllTargetsReached():
            return False

        for childTaskId in task.childTaskIds:
            childTask = self.getTask(childTaskId)
            if not childTask:
                continue
            if not childTask.isStat(gameconst.TaskStat.TASK_STAT_SUBMITTED):
                return False
        self.onTaskFinished(owner, task)
        return True

    def onTaskFinished(self, owner, task):
        DEBUG_MSG('in TaskInfo::onTaskFinished, taskId:', task.taskId)
        taskData = dataUtils.getTaskData(task.taskId)
        task.setStat(owner, gameconst.TaskStat.TASK_STAT_FINISHED)
        self.addSendUpdatedTaskList([task, ])
        if dataUtils.taskFieldVal(taskData, 'DeliMetdNoLimit'):
            # 先校验一次base的提交条件，如果不满足，就不用去cell校验条件了
            if self.checkSubmitBaseCond(owner, task.taskId):
                # 任务自动提交
                owner.startSubmitTask(task.taskId)
        return

    def relateSubmitTaskList(self, taskId):
        taskIdList = [taskId]
        task = self.getTask(taskId)
        parentTask = self.getTask(task.parentTaskId)
        childTaskId = taskId
        while parentTask and parentTask.childTaskIds:
            childTaskData = dataUtils.getTaskData(childTaskId)
            if dataUtils.taskFieldVal(childTaskData, 'FaterSuccIfChildSucc') or taskId == parentTask.childTaskIds[-1]:
                taskIdList.append(parentTask.taskId)
                childTaskId = parentTask.taskId
                parentTask = self.getTask(parentTask.parentTaskId)
            else:
                break
        return taskIdList

    def checkTaskSubmitRewardCond(self, owner, task):
        if not dataUtils.isLeafTask(task.taskId):
            return True
        taskIdList = self.relateSubmitTaskList(task.taskId)
        for taskId in taskIdList:
            if not self._canSubmitTaskReward(owner, taskId):
                return False
        return True

    def _canSubmitTaskReward(self, owner, taskId):
        taskData = dataUtils.getTaskData(taskId)
        if not dataUtils.taskFieldVal(taskData, 'FinRewardID'):
            # 任务完成无 rewardId 奖励
            return True

        task = self.getTask(taskId)
        if task.isEmptyTarget() and dataUtils.taskFieldVal(taskData, 'DeliMetdNoLimit'):
            # 没有任务目标及自动提交的任务
            return True

        # if dataUtils.taskFieldVal(taskData, 'FinRewardID') in RDRDD.NoBagSpaceRewardIDSet:
        #     # 该奖励不发放背包道具
        #     return True

        # 挂机玩法任务奖励不受背包限制，背包满时，通过邮件发放奖励；
        if owner.bagData.isFull() and not dataUtils.taskFieldVal(taskData, 'IsAutoTask'):
            WARNING_MSG('_canSubmitTaskReward, bag full:', taskId)
            if not dataUtils.taskFieldVal(taskData, 'DispHiddenTask'):
                owner.onMessagePre(dataUtils.taskMsgId('taskSubmitAlert_BagCheck'), [])
            return False
        return True

    def checkSubmitBaseCond(self, owner, taskId):
        task = self.getTask(taskId)
        if not task or task.isInEndStat() or not task.isStat(gameconst.TaskStat.TASK_STAT_FINISHED):
            # 必须处于 TASK_STAT_FINISHED 状态，才允许提交任务
            WARNING_MSG('   checkSubmitBaseCond check failed, no task or task state error')
            return False

        if not self.checkTaskSubmitRewardCond(owner, task):
            WARNING_MSG('   checkSubmitBaseCond check failed, submit reward cond failed')
            return False

        for childTaskId in task.childTaskIds:
            childTask = self.getTask(childTaskId)
            if not childTask:
                # 任务提交条件，不需要所有子任务都已经领取
                continue
            if not childTask.isStat(gameconst.TaskStat.TASK_STAT_SUBMITTED):
                gameengine.reportCritical('   checkSubmitBaseCond check failed, child task state error:',
                                          childTaskId, childTask.stat)
                return False
        return True

    def deductTaskTgtItems(self, owner, taskId):
        task = self.getTask(taskId)
        if not task or task.isInEndStat() or task.isStat(gameconst.TaskStat.TASK_STAT_FINISHED):
            WARNING_MSG('in deductTaskTgtItems, task error:', task, taskId)
            return
        deductWealthVal = task.getTaskTgtItemsWealthVal()
        if not owner.canDeductWealth(deductWealthVal):
            task.updateTgtItemsCount(owner)
            task.setStat(owner, gameconst.TaskStat.TASK_STAT_RUNNING)
            self.sendUpdatedTaskNow(owner, task)
            return False

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_COMPLETE_TASK
        detail = gameclass.AwardDetail(taskId=taskId)
        owner.deductWealth(srcType, deductWealthVal, opUUID, detail)
        task.deductTaskTgtItemsSucc()
        self.checkTaskFinished(owner, task)
        self.addSendUpdatedTaskList([task, ])
        return True

    def doSubmitTask(self, owner, taskId, popRewardUUID=0, check=True):
        # do reward and submit task
        task = self.getTask(taskId)
        if not task:
            WARNING_MSG('in doSubmitTask, no task')
            return

        if check and not task.isStat(gameconst.TaskStat.TASK_STAT_FINISHED):
            WARNING_MSG('in doSubmitTask, task not in target finish state:', task.stat)
            return

        if task.isStat(gameconst.TaskStat.TASK_STAT_SUBMITTED):
            WARNING_MSG('in doSubmitTask, already submit :', task.stat)
            return

        task.setStat(owner, gameconst.TaskStat.TASK_STAT_SUBMITTED)
        owner.flowCtrlOnTaskComplete(taskId)
        # flow controller notify

        # 如果是悬赏任务，则更新同时接取的限制状态
        if task.taskType == gameconst.TaskType.TASK_TYPE_HOOK_REWARD:
            if task.cycleType == gameconst.TaskCycleType.TASK_CYCLE_DAYLY \
                or task.cycleType == gameconst.TaskCycleType.TASK_CYCLE_WEEKLY:

                self.hookRewardTaskFnsNumWeekly += 1
                owner.client.onHookRewardTaskWeeklyLimitRefresh(self.hookRewardTaskFnsNumWeekly)

            if task.cycleType == gameconst.TaskCycleType.TASK_CYCLE_DAYLY \
                or task.cycleType == gameconst.TaskCycleType.TASK_CYCLE_WEEKLY \
                or task.cycleType == gameconst.TaskCycleType.TASK_CYCLE_ONCE:

                self.hookRewardTaskNum = max(self.hookRewardTaskNum-1, 0)

        task.alreadyCount += 1
        self.sendUpdatedTaskNow(owner, task)
        self._afterTaskSubmitted(owner, task, popRewardUUID)
        return True

    def _afterTaskSubmitted(self, owner, task, popRewardUUID=0):
        DEBUG_MSG("_afterTaskSubmitted ", task, popRewardUUID)
        if task.taskId in V_VD.taskDic:
            owner.updateVisibleByList(V_VD.taskDic[task.taskId])

        owner.onTaskFinishedForNewbieStep(task.taskId)
        owner.checkUnlockBuildAndSkillByTask(True, task.taskId)
        owner.deleteTemporarySkillByTask(task.taskId)
        owner.checkAndUnlockWelfareSignIn(updateFlag = True)
        owner.checkUnlockBountyTask()

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_COMPLETE_TASK
        self.doSubmitReward(owner, task.taskId, opUUID, srcType, popRewardUUID)
        self._autoClaimRoundTask(owner, task)
        self.onTaskEnd(owner, task.taskId, opUUID, srcType)
        owner.afterTaskSubmitted(opUUID, task.taskId)
        ctx = actionContext.AchievementCtx(taskId=task.taskId)
        if task.taskType == gameconst.TaskType.TASK_TYPE_MAINLINE:
            owner.triggerAchievement(gameconst.AchieveType.MAIN_TASK, ctx)

        elif task.taskType == gameconst.TaskType.TASK_TYPE_SUBLINE:
            owner.triggerAchievement(gameconst.AchieveType.SUB_TASK, ctx)

        elif task.taskType == gameconst.TaskType.TASK_TYPE_HOOK_REWARD:
            _data = RRTID.datas[task.taskId]
            owner.achievementInfo.triggerAchieveByType(
                owner,
                gameconst.AchieveType.HOOK_TASK_REWARD,
                actionContext.AchievementCtx(mapId=_data['mapID']))

        if 0 != task.parentTaskId:
            DEBUG_MSG("_afterTaskSubmitted 1 ", task)
            self.onChildtaskSubmitted(owner, task)

        return

    def _autoClaimRoundTask(self, owner, task):
        taskData = dataUtils.getTaskData(task.taskId)
        roundVal, _, _, _ = dataUtils.getTaskRoundInfo(taskData)
        if roundVal > 0:
            if task.alreadyCount % roundVal != 0:
                DEBUG_MSG('in autoClaimRoundTask, auto claim new task:', task.taskId, roundVal, task.alreadyCount)
                owner.cell.startClaimTask(task.taskId, '', (),
                                          actionContext.ClaimTaskCtx(claimSrc=gameconst.ClaimTaskSrc.ROUND_AUTO_CLAIM))

    def forceCompleteTask(self, owner, taskId):
        task = self.getTask(taskId)
        if not task or task.isInEndStat():
            return False
        task.setAllTargetsReached(owner)
        for childTaskId in task.childTaskIds:
            childTask = self.getTask(childTaskId)
            if childTask and self.forceCompleteTask(owner, childTaskId):
                # 正常调用不会走到这里，对于非叶节点任务，状态直接设置为已提交
                WARNING_MSG('forceCompleteTask, childTask:', taskId, childTaskId)
                childTask.setStat(owner, gameconst.TaskStat.TASK_STAT_SUBMITTED)
                self.sendUpdatedTaskNow(owner, childTask)
        self.onTaskFinished(owner, task)
        return True

    def _rewardItemsOnTaskEnd(self, owner, taskId, rewardId, opUUID, srcType, popRewardUUID=0):
        if rewardId > 0:
            DEBUG_MSG('in _rewardItemsOnTaskEnd:', taskId, rewardId, popRewardUUID)
            awardCtx = awardContext.CommonContext(gameconst.MailConstID.REWARD_MAIL_ID)
            awardCtx = owner._getAvatarAwardCtx(rewardId, awardCtx)

            taskVal = self.getTask(taskId)
            if taskVal:
                rewardItemArgs = taskVal.extraAttr.getExtraAttr('rewardItemArgs', {})
                if rewardItemArgs:
                    awardCtx.itemArgs.update(rewardItemArgs)
            wealthVal = dropAward.getAward(rewardId, 1, awardCtx)

            if not wealthVal.isEmpty():
                detail = gameclass.AwardDetail(taskId=[taskId], popRewardUUID=popRewardUUID)
                owner.addWealth(srcType, wealthVal, opUUID, detail=detail, awardCtx=awardCtx, directly=(popRewardUUID==0))

    def doSubmitReward(self, owner, taskId, opUUID, srcType, popRewardUUID=0):
        # 检查发奖次数是否满足
        task = self.getTask(taskId)
        rootTask = self.getTask(task.rootTaskId)
        taskData = dataUtils.getTaskData(taskId)
        rewardId = dataUtils.taskFieldVal(taskData, 'FinRewardID')
        finRewardCountLimit = dataUtils.taskFieldVal(taskData, 'FinRewardCountLimit')
        finRewardCountLimit = finRewardCountLimit or 1
        if rewardId and rootTask.canAddRewardId(task.taskId, rewardId, finRewardCountLimit):
            # 道具和物品奖励
            rootTask.recordSubmitTaskRewardId(taskId, rewardId)
            self._rewardItemsOnTaskEnd(owner, taskId, rewardId, opUUID, srcType, popRewardUUID)

        roundVal, roundRwdList, roundActList, roundParamList = dataUtils.getTaskRoundInfo(taskData)
        if task.parentTaskId == 0 and roundVal > 0 and task.alreadyCount > 0 and task.alreadyCount % roundVal == 0 and roundRwdList:
            roundIdx = task.alreadyCount // roundVal - 1
            if roundIdx < len(roundRwdList):
                self._rewardItemsOnTaskEnd(owner, taskId, roundRwdList[roundIdx], opUUID, srcType, popRewardUUID)

            if roundActList and roundParamList and roundIdx < len(roundActList) and roundIdx < len(roundParamList):
                owner.doTaskEvent(gameconst.EventActionSrc.SRC_ROUND_TASK, taskId,
                                  roundActList[roundIdx], roundParamList[roundIdx])

        #奖励进入副本 与 奖励传出当前副本， 二者同时只能有一个生效
        if dataUtils.taskFieldVal(taskData, 'FinHasRewardInst'):
            if task.claimSrc!=gameconst.ClaimTaskSrc.GM_FINISH_NEWBIE:
            #如果是GM完成新手就不进出副本了，因为进去马上会出来，瞬间多次传送支持不了
                self._rewardEnterDungeon(owner, taskId, dataUtils.taskFieldVal(taskData, 'FinRewardInstance'))
        else:
            self._rewardLeaveDungeon(owner, taskData, taskId, task.claimSrc)
        #奖励发放任务
        self._rewardNewTask(owner, dataUtils.taskFieldVal(taskData, 'FinRewardTaskID'))
        # 检查是否有事件需要处理
        owner.doTaskEvent(gameconst.EventActionSrc.SRC_SUBMIT_TASK, taskId,
                          dataUtils.taskFieldVal(taskData, 'FinRewardEventName'),
                          dataUtils.taskFieldVal(taskData, 'FinRewardEventParam'))
        # 是否需要播放动画
        storyId = dataUtils.taskFieldVal(taskData, 'FinRewardTriggerStoryID')
        if storyId:
            # 播放剧情动画
            owner.client.onStartPlayCinema(storyId)
            # 回调cell做后续处理
            owner.cell.afterPlayCinema(storyId)

        # 修改变量
        if dataUtils.taskFieldVal(taskData, 'FinRewardCanVarMod'):
            varSrc = gameconst.VarChangeSrc.VAR_SRC_TASK_SUBMIT
            for varData in dataUtils.taskFieldVal(taskData, 'FinRewardVarModInfo'):
                owner.taskSetVariable(taskId, opUUID, varSrc, varData['TargetVar'], varData['FormId'],
                                      varData['ParamVar'])
        return

    def quitTaskReward(self, owner, taskId, opUUID, srcType):
        # DEBUG_MSG('in quitTaskReward:', taskId)
        # 检查发奖次数是否满足
        taskData = dataUtils.getTaskData(taskId)
        # 道具和物品奖励
        rewardId = taskData.get('AbanRewardID', 0)
        if rewardId > 0:
            rootTask = self.getRootTask(taskId)
            if rootTask.canAddRewardId(taskId, rewardId):
                self._rewardItemsOnTaskEnd(owner, taskId, rewardId, opUUID, srcType)
        # 进入副本的奖励
        if dataUtils.taskFieldVal(taskData, 'AbanHasRewardInst'):
            self._rewardEnterDungeon(owner, taskId, dataUtils.taskFieldVal(taskData, 'AbanRewardInstance'))
        #奖励发放任务
        self._rewardNewTask(owner, dataUtils.taskFieldVal(taskData, 'AbanRewardTaskID'))
        # 检查是否有事件需要处理
        owner.doTaskEvent(gameconst.EventActionSrc.SRC_QUIT_TASK, taskId,
                          dataUtils.taskFieldVal(taskData, 'AbanRewardEventName'),
                          dataUtils.taskFieldVal(taskData, 'AbanRewardEventParam'))
        return

    def _rewardEnterDungeon(self, owner, taskId, newDungeonData):
        DEBUG_MSG('in _rewardEnterDungeon:', taskId, newDungeonData)
        self._taskEnterSpace(owner, taskId, newDungeonData)
        return

    def _rewardLeaveDungeon(self, owner, taskData, taskId, claimSrc):
        if dataUtils.taskFieldVal(taskData, 'FinRewardLeaveInstance'):
            leaveDungeonNo = dataUtils.taskFieldVal(taskData, 'FinRewardLevInsID')
            if not leaveDungeonNo:
                WARNING_MSG('in _rewardLeaveDungeon, no leaveDungeonNo:', taskId, leaveDungeonNo)
                return
            DEBUG_MSG('_rewardLeaveDungeon, leave dungeonNo:', taskId)
            owner.cell.onTaskRwdLeaveDungeon(taskId, leaveDungeonNo, claimSrc)
        return

    def _rewardNewTask(self, owner, newtaskIdsStr):
        if not newtaskIdsStr:
            return
        newTaskIds = newtaskIdsStr.split('|')
        for newTaskId in newTaskIds:
            if not newTaskId.isdigit():
                continue
            newTaskId = int(newTaskId)
            if newTaskId <= 0:
                continue
            self.rewardTaskCacheDic[newTaskId] = utils.getNow()
            owner.cell.startClaimTask(newTaskId, '', (),
                                      actionContext.ClaimTaskCtx(claimSrc=gameconst.ClaimTaskSrc.REWARD_TASK))

    def onChildtaskSubmitted(self, owner, task):
        DEBUG_MSG("onChildtaskSubmitted ", task)
        parentTask = self.getTask(task.parentTaskId)
        if not parentTask:
            ERROR_MSG('child task[Id={}] config parent task[Id={}] but not found parent task on avatar body'.format(
                task.taskId, task.parentTaskId))
            return

        if gameconst.TaskStat.TASK_STAT_FINISHED == parentTask.stat:
            DEBUG_MSG("onChildtaskSubmitted 1 ", parentTask)
            owner.startSubmitTask(parentTask.taskId)
            return
        if gameconst.TaskStat.TASK_STAT_RUNNING != parentTask.stat:
            DEBUG_MSG("onChildtaskSubmitted 2 ", parentTask)
            return

        childTaskData = dataUtils.getTaskData(task.taskId)
        FaterSuccIfChildSucc = dataUtils.taskFieldVal(childTaskData, 'FaterSuccIfChildSucc')
        if FaterSuccIfChildSucc:
            DEBUG_MSG("onChildtaskSubmitted 3 ", parentTask)
            # 子任务成功，则父任务也成功
            self.onTaskFinished(owner, parentTask)
            return

        # 是否需要添加新的子任务
        if self.addNewChildTask(owner, task.taskId, parentTask):
            # 需要进行新的子任务（已经发放新的子任务，或者等待玩家选择新的子任务）
            return

        for childTaskId in parentTask.childTaskIds:
            childTask = self.getTask(childTaskId)
            if not childTask:
                # 尚有未领取的子任务
                return
            if childTask and not childTask.isStat(gameconst.TaskStat.TASK_STAT_SUBMITTED):
                return

        # 所有子任务都已经完成并提交了
        self.onTaskFinished(owner, parentTask)
        return

    def addNewChildTask(self, owner, childTaskId, parentTask):
        DEBUG_MSG("addNewChildTask 1", childTaskId, parentTask)
        # taskData['ChildDoInSameTime'] 领取父任务时候就领取了所有子任务，所以这里不需要做检查
        taskData = dataUtils.getTaskData(parentTask.taskId)
        if dataUtils.taskFieldVal(taskData, 'ChildDoInQueue') or dataUtils.taskFieldVal(taskData, 'ChildDoInRandom'):
            DEBUG_MSG("addNewChildTask 2", parentTask)
            taskId = -1
            if dataUtils.taskFieldVal(taskData, 'RandomWithWeight'):
                taskId = self.calculateRandomTaskWithWeight(parentTask, taskData)
                parentTask.lastChildTaskId = taskId
            else:
                idx = parentTask.childTaskIds.index(childTaskId)
                if idx != len(parentTask.childTaskIds) - 1:
                    # 发放新的子任务
                    idx += 1
                    taskId = parentTask.childTaskIds[idx]

            if taskId > 0:
                # 子任务无条件领取成功
                self.doClaimTask(owner, taskId, actionContext.ClaimTaskCtx())
                self.addSendUpdatedTaskList([parentTask, ])
                parentTask.lastChildTaskId = taskId
                return True
        elif dataUtils.taskFieldVal(taskData, 'ChildDoInSelection'):
            # 等待玩家重新选择子任务
            return True
        return False

    def doTaskFailed(self, owner, taskId, reason=gameconst.TaskNotSuccReason.AUTO_QUIT):
        uptaskList = []
        task = self.getTask(taskId)
        if not task:
            ERROR_MSG(' in doTaskFailed, task not exist:', taskId, reason)
            return

        if task.isInEndStat():
            return

        DEBUG_MSG('in TaskInfo::doTaskFailed taskId {} reason {}'.format(taskId, reason))
        task.setStat(owner, gameconst.TaskStat.TASK_STAT_FAILED)
        uptaskList.append(task)
        # set flow
        owner.flowCtrlOnTaskFailed(taskId)

        # 所有子任务也失败
        childTaskIds = self.getChildTaskIds(task.taskId)
        failedTaskIds = [taskId, ]
        for childTaskId in childTaskIds:
            childTask = self.getTask(childTaskId)
            if childTask is None:
                continue
            if childTask.isInEndStat():
                continue
            childTask.setStat(owner, gameconst.TaskStat.TASK_STAT_FAILED)
            failedTaskIds.append(childTaskId)
            uptaskList.append(childTask)
        self._afterTaskFailed(owner, failedTaskIds)
        self.addSendUpdatedTaskList(uptaskList)
        if task.parentTaskId != 0:
            self.onChildTaskFailed(owner, task)

        # 检查任务失败后是否自动放弃
        taskData = dataUtils.getTaskData(taskId)
        if dataUtils.taskFieldVal(taskData, 'FailCondQuitIfFail'):
            owner.startQuitTask(taskId, reason)
        return True

    def _afterTaskFailed(self, owner, quitTaskIds):
        self._afterTaskUpdateRemoved(owner, quitTaskIds)
        for taskId in quitTaskIds:
            task = self.getTask(taskId)
            taskData = dataUtils.getTaskData(taskId)
            if dataUtils.taskFieldVal(taskData, 'OpenCondIsFailNoCount') and not dataUtils.taskFieldVal(taskData,
                                                                                                        'OpenCondIsAbanNoCount'):
                # 任务失败不记录次数; 任务失败和放弃只能返还一次领取次数， 所以如果勾选了放弃不记录次数，这里不要返还次数；
                if dataUtils.taskFieldVal(taskData, 'OpenCondTaskeState') == TaskCountLimitType.TASK_LIMIT_CLAIM_COUNT:
                    task.claimCount = max(task.claimCount - 1, 0)

    def onChildTaskFailed(self, owner, childTask):
        childTaskData = dataUtils.getTaskData(childTask.taskId)
        if dataUtils.taskFieldVal(childTaskData, 'FatherFailIfChildFail'):
            DEBUG_MSG('onChildTaskFailed, FatherFailIfChildFail:', childTask.taskId, childTask.parentTaskId)
            self.doTaskFailed(owner, childTask.parentTaskId, gameconst.TaskNotSuccReason.CHILD_FAILED)
            return

    def doAvatarDead(self, owner):
        for taskId, task in self.tasks.items():
            if task.parentTaskId != 0:
                continue
            if not task.isStat(gameconst.TaskStat.TASK_STAT_RUNNING) and not task.isStat(gameconst.TaskStat.TASK_STAT_FINISHED):
                continue
            taskData = dataUtils.getTaskData(taskId)
            FailCondIfDie = dataUtils.taskFieldVal(taskData, 'FailCondIfDie')
            if FailCondIfDie:
                DEBUG_MSG('in doAvatarDead, doTaskFailed:', taskId)
                self.doTaskFailed(owner, taskId, gameconst.TaskNotSuccReason.AVATAR_DIE)

    def canQuitTaskManual(self, taskId):
        taskData = dataUtils.getTaskData(taskId)
        if dataUtils.taskFieldVal(taskData, 'FailCondCanGiveUp'):
            # 任何状态可以手动放弃该任务
            return True

        if dataUtils.taskFieldVal(taskData, 'FailCondCanQuitIfFail') and self.getTaskCurrentState(
                taskId) == gameconst.TaskStat.TASK_STAT_FAILED:
            # 仅失败状态可以手动放弃该任务
            return True

        INFO_MSG('canQuitTaskManual, task can not quit:', taskData['TaskId'])
        return False

    # 放弃任务
    def doQuitTask(self, owner, taskId, reason):
        task = self.getTask(taskId)
        if not task or task.isInEndStat():
            return
        rootTaskId = task.rootTaskId
        DEBUG_MSG('doQuitTask, taskId {} rootTaskId {}:'.format(taskId, rootTaskId))
        uptaskList = []
        rootTask = self.getTask(rootTaskId)
        if self.getTaskCurrentState(taskId) != gameconst.TaskStat.TASK_STAT_FAILED:
            owner.flowCtrlOnTaskFailed(taskId)

        if not rootTask:
            # 找不到根任务，这种情况只会出现在使用gm指令直接领取子任务的情况
            task.setStat(owner, gameconst.TaskStat.TASK_STAT_QUIT)
            self.addSendUpdatedTaskList([task])
            self._afterTaskQuit(owner, [taskId], reason)
            gameengine.reportCritical('in doQuitTask, no root task:', taskId, rootTaskId)
            return
        rootTask.setStat(owner, gameconst.TaskStat.TASK_STAT_QUIT)
        quitTaskIds = set()
        quitTaskIds.add(rootTaskId)
        uptaskList.append(rootTask)
        # 所有子任务也放弃
        childTaskIds = self.getChildTaskIds(rootTask.taskId)
        for childTaskId in childTaskIds:
            childTask = self.getTask(childTaskId)
            if childTask is None:
                continue
            if childTask.isStat(gameconst.TaskStat.TASK_STAT_QUIT):
                continue
            childTask.setStat(owner, gameconst.TaskStat.TASK_STAT_QUIT)
            uptaskList.append(childTask)
            quitTaskIds.add(childTaskId)


        # 如果是悬赏任务，则更新同时接取的限制状态
        if task.taskType == gameconst.TaskType.TASK_TYPE_HOOK_REWARD:
            if task.cycleType == gameconst.TaskCycleType.TASK_CYCLE_DAYLY \
                or task.cycleType == gameconst.TaskCycleType.TASK_CYCLE_WEEKLY \
                or task.cycleType == gameconst.TaskCycleType.TASK_CYCLE_ONCE:

                self.hookRewardTaskNum = max(self.hookRewardTaskNum-1, 0)
                DEBUG_MSG('do quit task, self.hookRewardTaskNum is ', self.hookRewardTaskNum)

        self.addSendUpdatedTaskList(uptaskList)
        self._afterTaskQuit(owner, quitTaskIds, reason)

        return len(quitTaskIds) > 0

    def _afterTaskQuit(self, owner, quitTaskIds, reason):
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_ABANDON_TASK
        self._afterTaskUpdateRemoved(owner, quitTaskIds)
        for taskId in quitTaskIds:
            # 任务放弃也可能有奖励
            self.quitTaskReward(owner, taskId, opUUID, srcType)

            task = self.getTask(taskId)
            taskData = dataUtils.getTaskData(taskId)

            if dataUtils.taskFieldVal(taskData, 'OpenCondIsAbanNoCount'):
                # 任务放弃不记录次数
                if dataUtils.taskFieldVal(taskData, 'OpenCondTaskeState') == TaskCountLimitType.TASK_LIMIT_CLAIM_COUNT:
                    task.claimCount = max(task.claimCount - 1, 0)

            # 修改变量
            if dataUtils.taskFieldVal(taskData, 'AbanRewardCanVarMod'):
                varSrc = gameconst.VarChangeSrc.VAR_SRC_TASK_QUIT
                for varData in dataUtils.taskFieldVal(taskData, 'AbanRewardVarModInfo'):
                    owner.taskSetVariable(taskId, opUUID, varSrc, varData['TargetVar'], varData['FormId'],
                                          varData['ParamVar'])

            self.onTaskEnd(owner, taskId, opUUID, srcType)

            owner.taskFlowLog(taskId, "TaskQuit", opUUID, reason=reason)
        return

    def onTaskEnd(self, owner, taskId, opUUID, srcType):
        taskData = dataUtils.getTaskData(taskId)
        if dataUtils.taskFieldVal(taskData, 'ClaimCanRewardITems'):
            # 回收任务物
            owner.remTaskItems(taskId, opUUID, srcType)
        self.remReachAreaTargetTask(owner, taskId)
        self.removeTaskCache(taskId)

    def getRootTask(self, taskId):
        # 理论上最多10层子任务，实际应该不会超出10层
        rootTaskId = dataUtils.getRootTaskId(taskId)
        return self.getTask(rootTaskId)

    def getLastChildTaskId(self, taskId, default=0):
        task = self.getTask(taskId)
        if not task:
            return default
        lastChildTaskId = task.lastChildTaskId
        while lastChildTaskId > 0:
            childTask = self.getTask(lastChildTaskId)
            if not childTask:
                return lastChildTaskId
            if childTask.lastChildTaskId == 0:
                break
            lastChildTaskId = childTask.lastChildTaskId
        return lastChildTaskId

    def getChildTaskIds(self, taskId, deep=0):
        if deep >= 5:
            gameengine.reportCritical('getChildTaskIds, deep>=5:', taskId)
            return []
        childTaskIds = []
        taskData = dataUtils.getTaskData(taskId)
        for tid in dataUtils.taskFieldVal(taskData, 'ChildTaskIds'):
            childTaskIds.append(tid)
            # childTask = self.getTask(tid)
            # if not childTask:
            #     continue
            tids = self.getChildTaskIds(tid, deep=deep + 1)
            tids and childTaskIds.extend(tids)
        return childTaskIds

    def _cleanOldChildTasks(self, owner, syncTaskIdList):
        remChildTaskIds = []
        for taskId in syncTaskIdList:
            task = self.getTask(taskId)
            if not task:
                continue
            if task.parentTaskId != 0:
                continue
            if dataUtils.isSingleSupportTeamTask(taskId) and not task.isInEndStat():
                # 如果有进行中的单人支持的组队任务，不能被队长的任务覆盖
                continue
            remChildTaskIds.extend(self.remChildTask(task.taskId))
        if len(remChildTaskIds) > 0:
            DEBUG_MSG('     in _cleanOldChildTasks, remChildTaskIds:', remChildTaskIds)
            owner.client.onTasksRem(remChildTaskIds)
        return

    def onTaskStepUpdate(self, owner, targetType, taskIds, args):
        INFO_MSG('TaskInfo::onTaskStepUpdate:', targetType, taskIds, args)
        if taskIds:
            if type(taskIds) not in (tuple, list):
                taskIds = (taskIds,)
        else:
            taskIds = self.tasks.keys()

        bUpdate = False
        for taskId in taskIds:

            task = self.getTask(taskId)
            if not task or not task.isStat(gameconst.TaskStat.TASK_STAT_RUNNING):
                continue

            targetList = task.getTgtsByType(targetType)
            if not targetList:
                continue

            if targetType == gameconst.TaskTargetType.TASK_TARGET_ITEMS:
                updated = task.updateTgtItemsCount(owner)
                if updated:
                    DEBUG_MSG('TaskInfo::onTaskStepUpdate items:', taskId, args)
                    self.addSendUpdatedTaskList([task, ])
                    bUpdate = True
            elif targetType == gameconst.TaskTargetType.TASK_TARGET_COLLECT:
                _, gameEntityId, _ = args
                if not task.addCollectNum(targetType, args):
                    continue
                tgtArrived = task.onTaskStepUpdate(targetType, args)
                self.addSendUpdatedTaskList([task, ])
                bUpdate = True
                if tgtArrived:
                    DEBUG_MSG('TaskInfo::onTaskStepUpdate:', args)
                    self.checkTaskFinished(owner, task)
            elif targetType == gameconst.TaskTargetType.TASK_TARGET_COUNTER:
                if not task.addCounterNum(targetType, args):
                    continue
                tgtArrived = task.onTaskStepUpdate(targetType, args)
                self.addSendUpdatedTaskList([task, ])
                bUpdate = True
                if tgtArrived:
                    DEBUG_MSG('TaskInfo::onTaskStepUpdate arrived:', args)
                    self.checkTaskFinished(owner, task)
            else:
                tgtArrived = task.onTaskStepUpdate(targetType, args)
                if tgtArrived:
                    DEBUG_MSG('TaskInfo::onTaskStepUpdate arrived:', args)
                    self.checkTaskFinished(owner, task)
                    self.addSendUpdatedTaskList([task, ])
                    bUpdate = True
        return bUpdate

    def taskEnterSpace(self, owner, task):
        taskInfo = dataUtils.getTaskData(task.taskId)
        # 随任务接取后自动进入的
        if not dataUtils.taskFieldVal(taskInfo, 'ClaimCanTransIns'):
            ERROR_MSG('taskEnterSpace illegal op 1', taskInfo)
            return False

        claimTransData = dataUtils.taskFieldVal(taskInfo, 'ClaimTransInstance')
        if not claimTransData:
            ERROR_MSG('taskEnterSpace wrong cfg', taskInfo)
            return False

        needConfirm = claimTransData.get('NeedConfirm')
        # 不需要二次确认弹窗，接取任务主动进入地图
        if not needConfirm:
            ERROR_MSG('taskEnterSpace illegal op 2', taskInfo)
            return False

        self._taskEnterSpace(owner, task.taskId, claimTransData)
        return True
