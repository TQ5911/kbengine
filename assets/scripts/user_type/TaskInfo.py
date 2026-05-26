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
import gameclass
import Task
import formula

import taskRelate as TRD
import taskItemSrc as TISD

import visible_visible as V_VD
import rewardTask_config as RRTIC
import rewardTask_taskInfo as RRTID
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD

class TaskCountLimitType(object):
    TASK_LIMIT_CLAIM_COUNT = 0  # 领取任务时检查领取次数限制
    TASK_LIMIT_SUBMIT_COUNT = 1  # 提交任务时检查提交次数限制


class TaskInfo(userType.UserSingleType):
    def __init__(self):
        self.tasks = {}
        self.sendUpdateTasks = {}
        self.taskRecordDic = {}

        self.taskId2ValidSecDic = {}
        self.areaTargetTaskDic = {}
        self.taskId2expiredTimeDic = {}

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
        return self.getTaskCurrentState(taskId) == gameconst.TaskStatEnum.TASK_STAT_SUBMITTED

    def isTaskRunning(self, taskId):
        return self.getTaskCurrentState(taskId) == gameconst.TaskStatEnum.TASK_STAT_RUNNING

    def getTaskCurrentState(self, taskId):
        _task = self.getTaskObj(taskId)
        if _task:
            return _task.stat
        return self._taskStateNoTaskObj(taskId)

    def _taskStateNoTaskObj(self, taskId):
        # 任务不在当前任务列表里的情况
        taskData = dataUtils.getTaskCfg(taskId)
        if not taskData:
            LOG_ERR('_taskStateNoTaskObj task not config', taskId)
            return self.taskRecordDic.get(taskId, gameconst.TaskStatEnum.TASK_STAT_UNKNOWN)

        parentTaskId = dataUtils.getTaskFieldVal(taskData, 'FatherTaskId')
        if parentTaskId == 0:
            # taskId已经是根任务
            return self.taskRecordDic.get(taskId, gameconst.TaskStatEnum.TASK_STAT_UNKNOWN)
        parentTask = self.getTaskObj(parentTaskId)
        if parentTask:
            if parentTask.isInEndStat():
                return parentTask.stat
            else:
                return gameconst.TaskStatEnum.TASK_STAT_UNKNOWN
        return self._taskStateNoTaskObj(parentTaskId)

    def isTaskInStat(self, taskId, stat):
        return self.getTaskCurrentState(taskId) == stat

    def _lateReload(self):
        super(TaskInfo, self)._lateReload()

        for _v in self.tasks.values():
            _v.reloadScript()

        for _v in self.sendUpdateTasks.values():
            _v.reloadScript()
        return

    def toTaskInfoSavedDict(self):
        self.dealEndTasks()
        _dic = {
            'taskList': [], 
            'quitTaskIdList': [],
            'submitTaskIdList': [], 
        }

        for taskId, task in self.tasks.items():
            _dic['taskList'].append(task)
        for taskId, taskStat in self.taskRecordDic.items():
            if taskStat == gameconst.TaskStatEnum.TASK_STAT_SUBMITTED:
                _dic['submitTaskIdList'].append(taskId)
            elif taskStat == gameconst.TaskStatEnum.TASK_STAT_QUIT:
                _dic['quitTaskIdList'].append(taskId)

        if len(_dic['taskList']) > 100:
            # blob最多存300+任务
            gameengine.panicStack('attention!!! taskList num greater 100:', len(_dic['taskList']))

        if len(_dic['submitTaskIdList']) > 10000:
            # blob最多存 13000+ 任务
            gameengine.panicStack('attention!!! submitTaskIdList num greater 10000:', len(_dic['submitTaskIdList']))

        if len(_dic['quitTaskIdList']) > 10000:
            # blob最多存 13000+ 任务
            gameengine.panicStack('attention!!! quitTaskIdList num greater 10000:', len(_dic['quitTaskIdList']))

        _dic['rewardTaskCacheDic'] = self.rewardTaskCacheDic
        _dic['hookRewardTaskFnsNumWeekly'] = self.hookRewardTaskFnsNumWeekly
        _dic['hookRewardTaskNum'] = self.hookRewardTaskNum
        _dic['hookRewardTaskIdListWeekly'] = self.hookRewardTaskIdListWeekly
        _dic['hookRewardTaskIdListDaily'] = self.hookRewardTaskIdListDaily
        _dic['randomTaskWeights'] = self.randomTaskWeights
        return _dic

    def toTaskInfoClientDict(self):
        _dic = {
            'taskList': [], 
            'quitTaskIdList': [],
            'submitTaskIdList': [], 
        }

        for _taskId, _task in self.tasks.items():
            _dic['taskList'].append(_task.toTaskClientDict())

        for _taskId, _taskStat in self.taskRecordDic.items():
            if _taskStat == gameconst.TaskStatEnum.TASK_STAT_SUBMITTED:
                _dic['submitTaskIdList'].append(_taskId)
            elif _taskStat == gameconst.TaskStatEnum.TASK_STAT_QUIT:
                _dic['quitTaskIdList'].append(_taskId)

        _dic['hookRewardTaskFnsNumWeekly'] = self.hookRewardTaskFnsNumWeekly
        _dic['hookRewardTaskNum'] = self.hookRewardTaskNum
        _dic['hookRewardTaskIdListWeekly'] = self.hookRewardTaskIdListWeekly
        _dic['hookRewardTaskIdListDaily'] = self.hookRewardTaskIdListDaily
        return _dic

    def fromSavedDict(self, dataDic):
        self.tasks = {}
        for _task in dataDic['taskList']:
            if not _task:
                LOG_WARN('fromSavedDict, _task is None')
                continue
            self.tasks[_task.taskId] = _task
            if _task.parentTaskId != 0:
                continue

        for taskId in dataDic.get('submitTaskIdList', []):
            self.taskRecordDic[taskId] = gameconst.TaskStatEnum.TASK_STAT_SUBMITTED
        for taskId in dataDic.get('quitTaskIdList', []):
            self.taskRecordDic[taskId] = gameconst.TaskStatEnum.TASK_STAT_QUIT

        self.rewardTaskCacheDic = dataDic.get('rewardTaskCacheDic', {})
        self.hookRewardTaskFnsNumWeekly = dataDic.get('hookRewardTaskFnsNumWeekly', 0)
        self.hookRewardTaskNum = dataDic.get('hookRewardTaskNum', 0)
        self.hookRewardTaskIdListWeekly = dataDic.get('hookRewardTaskIdListWeekly', [])
        self.hookRewardTaskIdListDaily = dataDic.get('hookRewardTaskIdListDaily', [])
        self.randomTaskWeights = dataDic.get('randomTaskWeights', {})

    @classmethod
    def _checkIgnores_(cls):
        # 角色登陆时候根据任务数据构建的数据
        return ('taskId2ValidSecDic', 'taskId2expiredTimeDic', 'areaTargetTaskDic', 'curTryEnterDunData')

    def recordTaskOnce(self, taskId, taskStat):
        self.taskRecordDic[taskId] = taskStat

    def dealEndTasks(self):
        _endRootTaskIds = []
        for taskId, _task in self.tasks.items():
            if _task.parentTaskId != 0:
                continue
            if _task.isInEndStat():
                _endRootTaskIds.append(_task.taskId)

        # 将已提交或已放弃的根任务的所有子任务移除列表
        for endTaskId in _endRootTaskIds:
            self.remChildTask(endTaskId)

        # 处理已经完结（成功或者放弃）的任务
        removeTaskIds = []
        for taskId in _endRootTaskIds:
            _task = self.getTaskObj(taskId)
            taskData = dataUtils.getTaskCfg(_task.taskId)
            # 任务已经完结（成功或者放弃），清理任务列表的这部分数据并按需记录状态
            if gameconst.TaskCycleType.CYCLE_TASK_ENUM_NONE == _task.cycleType:
                # 非周期任务
                if _task.isStat(gameconst.TaskStatEnum.TASK_STAT_SUBMITTED):
                    if not dataUtils.getTaskFieldVal(taskData, 'OpenCondRepeatIfSucess'):
                        # 任务成功后不能重复开启, 记录任务状态
                        removeTaskIds.append(taskId)
                        self.recordTaskOnce(taskId, _task.stat)
                elif _task.isStat(gameconst.TaskStatEnum.TASK_STAT_QUIT):
                    if not dataUtils.getTaskFieldVal(taskData, 'OpenCondRepeatIfFail'):
                        # 任务放弃后不能重复开启, 记录任务状态
                        removeTaskIds.append(taskId)
                        self.recordTaskOnce(taskId, _task.stat)
            elif gameconst.TaskCycleType.CYCLE_TASK_ENUM_ONCE == _task.cycleType:
                # 单次开启的任务
                _openCondTaskeState = dataUtils.getTaskFieldVal(taskData, 'OpenCondTaskeState')
                if _openCondTaskeState == TaskCountLimitType.TASK_LIMIT_CLAIM_COUNT and _task.limitCount != 0 and _task.claimCount >= _task.limitCount:
                    # 领取次数已满，移除任务并记录状态
                    removeTaskIds.append(taskId)
                    self.recordTaskOnce(taskId, _task.stat)
                elif _openCondTaskeState == TaskCountLimitType.TASK_LIMIT_SUBMIT_COUNT and _task.limitCount != 0 and _task.alreadyCount >= _task.limitCount:
                    # 提交次数已满，移除任务并记录状态
                    removeTaskIds.append(taskId)
                    self.recordTaskOnce(taskId, _task.stat)
        if removeTaskIds:
            LOG_INFO('in dealAlreadyFinTasks, removeTaskIds:', removeTaskIds)
        for remTaskId in removeTaskIds:
            self.remTask(remTaskId)
        return

    def _constructHookRewardTaskListWeekly(self, taskNum, taskSrcList, myLevel):
        exist_set = set()
        for taskId, task in self.tasks.items():
            if task.parentTaskId != 0:
                continue
            # 悬赏任务类型
            if task.taskType != gameconst.TaskType.TASK_TYPE_HOOK_REWARD:
                continue
            # 周刷新类型
            if task.cycleType != gameconst.TaskCycleType.CYCLE_TASK_ENUM_WEEKLY:
                continue

            exist_set.add(taskId)
        result_list = []
        for taskId in taskSrcList:
            taskData = RRTID.datas.get(taskId)
            if not taskData:
                gameengine.panicStack('getTaskCfg from RRTID, no taskdata:', taskId)
                continue
            ClaimCondLevelMin = taskData.get('minLevel', 0)
            ClaimCondLevelMax = taskData.get('maxLevel', 0)
            if myLevel < ClaimCondLevelMin or myLevel > ClaimCondLevelMax:
                continue
            if taskId not in exist_set:
                result_list.append(taskId)
        taskNum = min(taskNum, len(result_list))
        result_list = random.sample(result_list, taskNum)
        result_list.extend(exist_set)
        return result_list
    
    def _constructHookRewardTaskListDaily(self, taskNum, taskSrcList, myLevel):
        result_list = []
        exist_set = set()
        mapTaskIds = {}
        for taskId, task in self.tasks.items():
            if taskId in exist_set:
                continue

            if task.parentTaskId != 0:
                continue
            # 悬赏任务类型
            if task.taskType != gameconst.TaskType.TASK_TYPE_HOOK_REWARD:
                continue
            # 日刷新类型
            if task.cycleType != gameconst.TaskCycleType.CYCLE_TASK_ENUM_DAYLY:
                continue

            taskData = RRTID.datas.get(taskId)
            if not taskData:
                gameengine.panicStack('getTaskCfg from RRTID, no taskdata:', taskId)
                continue
            mapId = taskData.get('mapID', 0)
            if mapId <= 0:
                continue
        
            exist_set.add(taskId)
            taskIds = mapTaskIds.get(mapId, None)
            if not taskIds:
                taskIds = []
                mapTaskIds[mapId] = taskIds
            taskIds.append(taskId)

        for taskId in taskSrcList:
            if taskId in exist_set:
                continue

            taskData = RRTID.datas.get(taskId)
            if not taskData:
                gameengine.panicStack('getTaskCfg from RRTID, no taskdata:', taskId)
                continue
            ClaimCondLevelMin = taskData.get('minLevel', 0)
            ClaimCondLevelMax = taskData.get('maxLevel', 0)
            if myLevel < ClaimCondLevelMin or myLevel > ClaimCondLevelMax:
                continue
            
            mapId = taskData.get('mapID', 0)
            if mapId <= 0:
                continue
            
            exist_set.add(taskId)
            taskIds = mapTaskIds.get(mapId, None)
            if not taskIds:
                taskIds = []
                mapTaskIds[mapId] = taskIds
            taskIds.append(taskId)
        
        # 按照地图取taskNum个任务
        for _, taskIds in mapTaskIds.items():
            taskCount = min(taskNum, len(taskIds))
            taskIds = random.sample(taskIds, taskCount)
            result_list.extend(taskIds)
        # 重新打乱一遍
        result_list = random.sample(result_list, len(result_list))
        return result_list

    def initNoviceHookRewardTask(self):
        hookRewardTaskNum = RRTIC.datas.get('dailyLimitNum', {}).get('value', 0)
        myLevel = 0
        self.hookRewardTaskIdListDaily = self._constructHookRewardTaskListDaily(hookRewardTaskNum, RRTID.DailyTaskList, myLevel)
        hookRewardTaskNum = RRTIC.datas.get('weeklyLimitNum', {}).get('value', 0)
        self.hookRewardTaskIdListWeekly = self._constructHookRewardTaskListWeekly(hookRewardTaskNum, RRTID.WeeklyTaskList, myLevel)
        self.hookRewardTaskFnsNumWeekly = 0

    def refreshHookRewardTask(self, level):
        hookRewardTaskNum = RRTIC.datas.get('dailyLimitNum', {}).get('value', 0)
        self.hookRewardTaskIdListDaily = self._constructHookRewardTaskListDaily(hookRewardTaskNum, RRTID.DailyTaskList, level)
        hookRewardTaskNum = RRTIC.datas.get('weeklyLimitNum', {}).get('value', 0)
        self.hookRewardTaskIdListWeekly = self._constructHookRewardTaskListWeekly(hookRewardTaskNum, RRTID.WeeklyTaskList, level)
        self.hookRewardTaskFnsNumWeekly = 0

    def _afterTaskUpdateRemoved(self, owner, removeTaskIds):
        LOG_INFO("_afterTaskUpdateRemoved", removeTaskIds)
        for taskId in removeTaskIds:
            owner.deleteTemporarySkillByTask(taskId)

    def doTaskDailyUpdate(self, owner, myLevel):
        finDailyTaskIds = []
        hookRewardTaskNum = RRTIC.datas.get('dailyLimitNum', {}).get('value', 0)
        self.hookRewardTaskIdListDaily = self._constructHookRewardTaskListDaily(hookRewardTaskNum, RRTID.DailyTaskList, myLevel)
        removeTaskIds = []
        for taskId, _task in self.tasks.items():
            if _task.parentTaskId != 0:
                continue
            if gameconst.TaskCycleType.CYCLE_TASK_ENUM_DAYLY != _task.cycleType:
                continue
            if _task.isInEndStat():
                finDailyTaskIds.append(taskId)
            else:
                _task.claimCount = 0
                _task.alreadyCount = 0
                _task.taskRewardLimitDic.clear()
                self.addSendUpdatedTaskList([_task, ])

        for _remTaskId in finDailyTaskIds:
            if self.remTask(_remTaskId):
                removeTaskIds.append(_remTaskId)
            removeTaskIds.extend(self.remChildTask(_remTaskId))
        LOG_INFO('in doTaskDailyUpdate, removeTaskIds:', removeTaskIds)
        self._afterTaskUpdateRemoved(owner, removeTaskIds)
        return removeTaskIds

    def doTaskWeeklyUpdate(self, owner, myLevel):
        finDailyTaskIds = []
        hookRewardTaskNum = RRTIC.datas.get('weeklyLimitNum', {}).get('value', 0)
        self.hookRewardTaskIdListWeekly = self._constructHookRewardTaskListWeekly(hookRewardTaskNum, RRTID.WeeklyTaskList, myLevel)
        self.hookRewardTaskFnsNumWeekly = 0
        for taskId, _task in self.tasks.items():
            if _task.parentTaskId != 0:
                continue
            if gameconst.TaskCycleType.CYCLE_TASK_ENUM_WEEKLY != _task.cycleType:
                continue
            if _task.isInEndStat():
                finDailyTaskIds.append(taskId)
            else:
                _task.claimCount = 0
                _task.alreadyCount = 0
                _task.taskRewardLimitDic.clear()
                self.addSendUpdatedTaskList([_task, ])

        _removeTaskIds = []
        for remTaskId in finDailyTaskIds:
            if self.remTask(remTaskId):
                _removeTaskIds.append(remTaskId)
            _removeTaskIds.extend(self.remChildTask(remTaskId))
        LOG_INFO('in doTaskWeeklyUpdate, _removeTaskIds:', _removeTaskIds)
        self._afterTaskUpdateRemoved(owner, _removeTaskIds)
        return _removeTaskIds

    def addSendUpdatedTaskList(self, tasksList):
        for _task in tasksList:
            self.sendUpdateTasks[_task.taskId] = _task

    def resetUpdatedTaskList(self):
        self.sendUpdateTasks = {}

    def sendUpdatedTaskNow(self, owner, taskObj):
        LOG_INFO('in sendUpdatedTaskNow:', taskObj.taskId, taskObj.stat)
        owner.client.onTaskUpdate([taskObj.toTaskClientDict(), ])
        self.sendUpdateTasks.pop(taskObj.taskId, None)

    def doSendUpdateTasksToClient(self, owner):
        if self.sendUpdateTasks:
            LOG_INFO('     in doSendUpdateTasksToClient:', [(_t.taskId, _t.stat) for _t in self.sendUpdateTasks.values()])
            owner.client.onTaskUpdate([_t.toTaskClientDict() for _t in self.sendUpdateTasks.values()])
            self.sendUpdateTasks = {}

    def sendHookRewardTaskList(self, owner):
        LOG_INFO('     in sendHookRewardTaskList daily list: ', self.hookRewardTaskIdListDaily, ' weekly list: ', self.hookRewardTaskIdListWeekly)
        LOG_INFO('     in sendHookRewardTaskList self.hookRewardTaskFnsNumWeekly: ', self.hookRewardTaskFnsNumWeekly, 'self.hookRewardTaskNum', self.hookRewardTaskNum)
        owner.client.onHookRewardTaskRefresh(self.hookRewardTaskIdListWeekly + self.hookRewardTaskIdListDaily)
        owner.client.onHookRewardTaskWeeklyLimitRefresh(self.hookRewardTaskFnsNumWeekly)

    def doUpdateTaskTimeout(self, owner, passSec=1):
        expiredTaskIds = []
        for _taskId in self.taskId2ValidSecDic.keys():
            _task = self.getTaskObj(_taskId)
            if not _task:
                continue
            _task.validSec -= passSec
            if _task.validSec <= 0:
                expiredTaskIds.append(_taskId)
        for failedTaskId in expiredTaskIds:
            self.taskId2ValidSecDic.pop(failedTaskId, None)
            _task = self.getTaskObj(failedTaskId)
            not _task.isInEndStat() and self.doTaskFailed(owner, failedTaskId, gameconst.TaskNotSuccReasonEnum.TIMEOUT)
        expiredTaskIds = []
        for _taskId in self.taskId2expiredTimeDic.keys():
            _task = self.getTaskObj(_taskId)
            if not _task:
                continue
            if _task and _task.isTaskExpired():
                expiredTaskIds.append(_taskId)

        for failedTaskId in expiredTaskIds:
            self.taskId2expiredTimeDic.pop(failedTaskId, None)
            LOG_INFO('in doUpdateTaskTimeout _task expired:', failedTaskId)
            _task = self.getTaskObj(failedTaskId)
            not _task.isInEndStat() and self.doTaskFailed(owner, failedTaskId, gameconst.TaskNotSuccReasonEnum.TIMEOUT)
        self.doSendUpdateTasksToClient(owner)

    def checkExpiredTaskOnLogin(self, owner):
        self.taskId2expiredTimeDic.clear()
        self.taskId2ValidSecDic.clear()
        now = utils.curTS()
        expiredTaskIds = []
        for _taskId, _task in self.tasks.items():
            if _task.isInEndStat():
                continue
            if _task.validSec > 0:
                self.addValidSecTask(_taskId, _task.validSec)
                continue
            if _task.isTaskExpired():
                # is expired
                expiredTaskIds.append(_taskId)
                continue
            if _task.expiredTime > now:
                self.addExpiredTimeTask(_taskId, _task.expiredTime)
                continue

        for failedTaskId in expiredTaskIds:
            LOG_INFO('in checkExpiredTaskOnLogin, failedTaskId:', failedTaskId)
            self.doTaskFailed(owner, failedTaskId, gameconst.TaskNotSuccReasonEnum.TIMEOUT)

    def initTaskCacheOnLogin(self, owner):
        self.areaTargetTaskDic.clear()
        for _taskId, _task in self.tasks.items():
            if _task.isInEndStat():
                continue
            targetList = _task.getTgtsByType(gameconst.TaskTargetType.TASK_TARGET_REACH_AREA)
            for target in targetList:
                self.addReachAreaTargetTask(_taskId, target)
                owner.cell.onAreaTargetTaskAdd(_taskId, target)

    def checkRewardTaskCacheOnLogin(self, owner):
        if not self.rewardTaskCacheDic:
            return
        LOG_INFO('checkRewardTaskCacheOnLogin:', self.rewardTaskCacheDic)
        for _taskId in self.rewardTaskCacheDic.keys():
            owner.cell.startClaimTask(_taskId, '', (),
                                      actionContext.ClaimTaskCtx(claimSrc=gameconst.ClaimTaskSrcEnum.TASK_SRC_REWARD_TASK))

    def removeRewardTaskCache(self, taskId):
        self.rewardTaskCacheDic.pop(taskId, None)

    def addValidSecTask(self, taskId, validSec):
        if validSec <= 0:
            return
        self.taskId2ValidSecDic[taskId] = validSec
        return

    def addExpiredTimeTask(self, taskId, expiredTime):
        if utils.curTS() > expiredTime:
            return
        self.taskId2expiredTimeDic[taskId] = expiredTime

    def remValidSecTask(self, taskId):
        self.taskId2ValidSecDic.pop(taskId, None)

    def remExpiredTimeTask(self, taskId):
        self.taskId2expiredTimeDic.pop(taskId, None)

    def addReachAreaTargetTask(self, taskId, target):
        self.areaTargetTaskDic[taskId] = target

    def removeTaskInCache(self, taskId):
        self.remValidSecTask(taskId)
        self.remExpiredTimeTask(taskId)

    def remReachAreaTargetTask(self, owner, taskId):
        _target = self.areaTargetTaskDic.pop(taskId, None)
        if _target and owner.cell:
            owner.cell.removeAreaTargetTask(taskId, _target.mapId)

    def getTaskObj(self, taskId):
        return self.tasks.get(taskId, None)

    def remTask(self, taskId):
        self.removeTaskInCache(taskId)
        return self.tasks.pop(taskId, None)

    def remChildTask(self, taskId):
        # 只清除子任务
        _remTaskIds = []
        for childTaskId in self.getChildTaskIds(taskId):
            if self.remTask(childTaskId):
                _remTaskIds.append(childTaskId)

        if _remTaskIds:
            LOG_INFO('cleanTask, _remTaskIds:', taskId, _remTaskIds)

        return _remTaskIds

    def hasBagSpaceForClaimTask(self, owner, taskId):
        taskData = dataUtils.getTaskCfg(taskId)
        if dataUtils.getTaskFieldVal(taskData, 'ClaimCanRewardITems'):
            _awardVal = dropAward.AwardVal()
            for _rewardItems in dataUtils.getTaskFieldVal(taskData, 'ClaimRewardItems'):
                if not _rewardItems['ItemId']:
                    continue

                _awardVal.addWealthByItemId(_rewardItems['ItemId'], _rewardItems['Count'])

            srcType = AAC_AACDD.datas.BONUS_SRC_CLAIM_TASK
            _awardCtx = awardContext.CommonContext(0)
            if not owner.canAddWealthVal(srcType, _awardVal, _awardCtx):
                return False

        for _childTaskId in dataUtils.getTaskFieldVal(taskData, 'ChildTaskIds'):
            if not self.hasBagSpaceForClaimTask(owner, _childTaskId):
                return False
        return True

    @staticmethod
    def giveClaimTaskItems(owner, opUUID, taskData):
        if not dataUtils.getTaskFieldVal(taskData, 'ClaimCanRewardITems'):
            return

        ClaimRewardItems = dataUtils.getTaskFieldVal(taskData, 'ClaimRewardItems')
        _validItems = {}
        for _rewardItems in ClaimRewardItems:
            itemId = _rewardItems['ItemId']
            itemNum = _rewardItems['Count']
            if itemId == 0 or itemNum == 0:
                continue
            _validItems[itemId] = itemNum

        if 0 == len(_validItems):
            return
        rewardDic = {}
        ClaimRandomItems = dataUtils.getTaskFieldVal(taskData, 'ClaimRandomItems')
        if ClaimRandomItems:
            itemKeys = list(_validItems.keys())
            rewardKey = random.choice(itemKeys)
            rewardDic[rewardKey] = _validItems[rewardKey]
        else:
            rewardDic = _validItems
        src = AAC_AACDD.datas.BONUS_SRC_CLAIM_TASK
        detail = gameclass.AwardDetail(taskId=[taskData['TaskId']])
        LOG_INFO('in giveClaimTaskItems, rewardDic:', rewardDic)
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
        if not dataUtils.getTaskFieldVal(taskData, 'ClaimCondCheckItem'):
            return gameclass.TaskCondResultCls(True)

        ClaimCondCheckItemInfo = dataUtils.getTaskFieldVal(taskData, 'ClaimCondCheckItemInfo')
        # 至少有一个物品数量够
        hasAtLeastOneEnoughItem = False
        # 所有物品数量够
        _hasAtAllEnoughItem = False
        _lackItemInfo = {}
        _deductVal = dropAward.DeductWealthVal()
        for oneInfo in ClaimCondCheckItemInfo['Items']:
            if oneInfo['ItemId'] <= 0 or oneInfo['Count'] <= 0:
                continue

            _deductVal.addWealthByItemId(oneInfo['ItemId'], oneInfo['Count'], dataUtils.getItemDefaultBindType())
            if owner.getItemNum(oneInfo['ItemId']) >= oneInfo['Count']:
                hasAtLeastOneEnoughItem = True
            else:
                _lackItemInfo['itemId'] = oneInfo['ItemId']
                _lackItemInfo['itemNum'] = oneInfo['Count']

        if owner.canDeductWealth(_deductVal, sendMsg=False):
            _hasAtAllEnoughItem = True

        SatisfyOne = ClaimCondCheckItemInfo.get('SatisfyOne', False)
        NotOpenIfHas = ClaimCondCheckItemInfo.get('NotOpenIfHas', False)
        if NotOpenIfHas and SatisfyOne:
            # 有一个道具数量足够，就不能领取任务，返回False
            if hasAtLeastOneEnoughItem:
                return gameclass.TaskCondResultCls(False)
            else:
                return gameclass.TaskCondResultCls(True)

        if NotOpenIfHas and not SatisfyOne:
            # 所有道具数量都足够 ，不能领取任务，返回False
            if _hasAtAllEnoughItem:
                return gameclass.TaskCondResultCls(False)
            else:
                return gameclass.TaskCondResultCls(True)

            # 所有道具都满足，才能领取任务，否则返回False
        if _hasAtAllEnoughItem:
            return gameclass.TaskCondResultCls(True)

        if not _lackItemInfo:
            return gameclass.TaskCondResultCls(False)

        if dataUtils.isTeamTask(taskId):
            _playerName = owner.getRoleCacheAttr('name', '')
            return gameclass.TaskCondResultCls(
                False, 
                dataUtils.getTaskMsgId('taskClaimAlert_Team_ItemCheck'),
                msgArgs=(_playerName, str(_lackItemInfo['itemId']))
            )

        else:
            return gameclass.TaskCondResultCls(
                False, 
                dataUtils.getTaskMsgId('taskClaimAlert_ItemCheck'),
                msgArgs=(str(_lackItemInfo['itemId']), str(_lackItemInfo['itemNum']))
            )

    @staticmethod
    def deductClaimTaskItems(owner, taskId, taskData):
        # 到这里说明任务可以领取
        if dataUtils.getTaskFieldVal(taskData, 'ClaimCondCheckItem'):
            ClaimCondCheckItemInfo = dataUtils.getTaskFieldVal(taskData, 'ClaimCondCheckItemInfo')
            _onlyCheck = ClaimCondCheckItemInfo.get('OnlyCheck', False)
            if _onlyCheck:
                return True
            _deductWealthVal = dropAward.DeductWealthVal()
            for oneInfo in ClaimCondCheckItemInfo['Items']:
                if oneInfo['ItemId'] > 0 and oneInfo['Count'] > 0:
                    _deductWealthVal.addWealthByItemId(oneInfo['ItemId'], oneInfo['Count'])

            LOG_INFO('in deductClaimTaskItems itemsDic:', _deductWealthVal)
            if not owner.canDeductWealth(_deductWealthVal):
                return False

            _opUUID = KBEngine.genUUID64()
            _srcType = AAC_AACDD.datas.BONUS_SRC_CLAIM_TASK
            _detail = gameclass.AwardDetail(taskId=taskId)
            owner.deductWealth(_srcType, _deductWealthVal, _opUUID, _detail)
        return True

    def doClaimTask(self, owner, taskId, taskCtx):
        self.removeRewardTaskCache(taskId)
        taskData = dataUtils.getTaskCfg(taskId)
        # 这里根据配置扣除物品，如果出现错误，说明是之前检查逻辑有错
        if not self.deductClaimTaskItems(owner, taskId, taskData):
            gameengine.panicStack('in doClaimTask, claim items deduct failed:', taskId)
            return

        remChildTaskIds = self.remChildTask(taskId)
        if len(remChildTaskIds) > 0:
            LOG_INFO('     in doClaimTask, remChildTaskIds:', remChildTaskIds)
            owner.client.onTasksRem(remChildTaskIds)

        # 子任务的 seed、enemyGuild信息、 teamId 要使用根任务的
        _rootTask = self.getRootTask(taskId)
        if _rootTask and _rootTask.taskId != taskId:
            taskCtx.claimSrc = _rootTask.claimSrc
            taskCtx.seed = _rootTask.seed

        if 0 == taskCtx.seed:
            taskCtx.seed = random.randint(100, 10000)

        _addTaskIds = self.addTask(owner, taskId, taskData, taskCtx)
        if not _addTaskIds:
            gameengine.panicStack('doClaimTask, addTaskIds:', _addTaskIds)
            return
        self._afterTaskClaimed(owner, taskCtx, taskId, _addTaskIds)
        owner.afterTaskClaimed(taskId)
        return _addTaskIds

    def _afterTaskClaimed(self, owner, taskCtx, taskId, addTaskIds):
        client = []
        _task = self.getTaskObj(taskId)
        _task.claimCount += 1
        opUUID = KBEngine.genUUID64()
        for _addTaskId in addTaskIds:
            _tmpTask = self.getTaskObj(_addTaskId)
            client.append(_tmpTask.toTaskClientDict())

        owner.client.onClaimTask(taskId, client)
        # 先处理最下层子任务，最后处理根任务
        for _addTaskId in reversed(addTaskIds):
            _tmpTask = self.getTaskObj(_addTaskId)
            addTaskData = dataUtils.getTaskCfg(_addTaskId)
            # 领取任务发放物品
            self.giveClaimTaskItems(owner, opUUID, addTaskData)

            LOG_DBG('in _afterTaskClaimed, addTaskId:', _addTaskId, _tmpTask.stat)
            # 播放剧情动画
            storyId = addTaskData.get('ClaimTriggerStoryID')
            if storyId:
                # 播放剧情动画
                owner.cell.prepareStartPlayCinema(storyId)
            if taskCtx.claimSrc!=gameconst.ClaimTaskSrcEnum.TASK_SRC_GM_FINISH_NEWBIE:
                self._claimEnterDungeon(owner, addTaskData, _tmpTask)

            # 领取任务事件处理
            owner.doTaskEvent(
                gameconst.EventActionSrc.SRC_CLAIM_TASK, 
                _addTaskId,
                addTaskData.get('ClaimEventName', ''), 
                addTaskData.get('ClaimEventParam', '')
            )

            # 如果是悬赏任务，则更新同时接取的限制状态
            if _tmpTask.taskType == gameconst.TaskType.TASK_TYPE_HOOK_REWARD:
                if _task.cycleType == gameconst.TaskCycleType.CYCLE_TASK_ENUM_DAYLY \
                    or _task.cycleType == gameconst.TaskCycleType.CYCLE_TASK_ENUM_WEEKLY \
                    or _task.cycleType == gameconst.TaskCycleType.CYCLE_TASK_ENUM_ONCE:

                    self.hookRewardTaskNum += 1
            # 修改变量
            if addTaskData.get('ClaimCanVarMod'):
                varSrc = gameconst.VarChangeSrcEnum.VAR_SRC_TASK_CLAIM
                for _varData in addTaskData['ClaimVarModInfo']:
                    owner.taskSetVar(
                        _addTaskId, 
                        opUUID, 
                        varSrc, 
                        _varData['TargetVar'], 
                        _varData['FormId'],
                        _varData['ParamVar']
                    )

            if len(addTaskData.get('ChildTaskIds', [])) == 0:
                if _tmpTask.isEmptyTarget():
                    # 没有目标的任务
                    if not addTaskData.get('FinCondNoLimit', False):
                        # 没有勾选"直接完成"，不需要 checkTaskFinished
                        continue
                    else:
                        # 勾选了"直接完成"
                        _tmpTask.setStat(owner, gameconst.TaskStatEnum.TASK_STAT_FINISHED)
                self.checkTaskFinished(owner, _tmpTask)

            target = self.areaTargetTaskDic.get(_addTaskId)
            if target:
                owner.cell.onAreaTargetTaskAdd(_addTaskId, target)
        self.doSendUpdateTasksToClient(owner)
        return

    def _claimEnterDungeon(self, owner, addTaskData, task):
        if dataUtils.getTaskFieldVal(addTaskData, 'ClaimCanTransIns'):
            claimTransData = dataUtils.getTaskFieldVal(addTaskData, 'ClaimTransInstance')
            needConfirm = claimTransData.get('NeedConfirm')
            # 需要弹窗二次确认的，检测是否非本地图，如果是本地图就直接过去，非本地图，就等玩家主动点击，走reqTaskEnterSpace主动进行进地图切换
            if needConfirm:
                LOG_INFO("_claimEnterDungeon, need confirm dialog to continue ", task)
                owner.cell.checkSameMap(task.taskId)
                return
            self._taskEnterSpace(owner, task.taskId, claimTransData)
        return

    def onCheckSameTaskResult(self, owner, task, isSame):
        LOG_INFO("onCheckSameTaskResult, chek result ", task, isSame)
        if not isSame:
            LOG_INFO("onCheckSameTaskResult, not same map, grant for client OP ", task)
            return
        taskCfg = dataUtils.getTaskCfg(task.taskId)
        # 如果是附灵任务, 则同地图, 不主动进行切换
        if dataUtils.getTaskFieldVal(taskCfg, 'TaskType') == gameconst.TaskType.TASK_TYPE_SPIRIT:
            LOG_INFO("onCheckSameTaskResult, stop spirit task telporting for same map~")
            return

        if not dataUtils.getTaskFieldVal(taskCfg, 'ClaimCanTransIns'):
            LOG_ERR("onCheckSameTaskResult, wrong cfg ", taskCfg)
            return
        claimTransData = dataUtils.getTaskFieldVal(taskCfg, 'ClaimTransInstance')
        self._taskEnterSpace(owner, task.taskId, claimTransData)

    def _taskEnterSpace(self, owner, taskId, transData):
        _dungeonNo = transData.get('MapId')
        _useConfigPos = transData.get('UseConfigPos')
        _dstPos = None
        _dstDir = None
        if _useConfigPos:
            _dstPos = (transData['X'], transData['Y'], transData['Z'])
            _dstDir = (0.0, 0.0, math.pi*transData.get('Dir', 0.0)/180)
        else:
            _dstPos, _dstDir = formula.getSpaceBornPosAndDir(_dungeonNo)

        owner.cell.taskPreEnterSpace(taskId, _dungeonNo, _dstPos, _dstDir)
        self.curTryEnterDunData = {'dungeonNo':_dungeonNo, 't':utils.curTS()}

    def getTaskItemIdList(self, taskId):
        itemIds = []
        taskData = dataUtils.getTaskCfg(taskId)
        gatherItemsInfo = dataUtils.getTaskFieldVal(taskData, 'FinCondGatherItems')
        for _itemInfo in gatherItemsInfo:
            itemId = _itemInfo['ItemId']
            if itemId > 0:
                itemIds.append(_itemInfo['ItemId'])
        for _childTaskId in dataUtils.getTaskFieldVal(taskData, 'ChildTaskIds'):
            childItemIds = self.getTaskItemIdList(_childTaskId)
            itemIds.extend(childItemIds)
        return itemIds

    def taskSpaceNoChanged(self, spaceNo):
        dungeonNo = formula.parseDungeonNoBySpaceNo(spaceNo)
        self.curTryEnterDunData.pop(dungeonNo, None)

    def isTaskTryingEnterDungeon(self, dungeonNo):
        _curDungeonNo = self.curTryEnterDunData.get('dungeonNo')
        if _curDungeonNo and _curDungeonNo==dungeonNo and utils.curTS() - self.curTryEnterDunData['t'] <=1:
            # 任务已经触发进入副本，在此期间，客户端通过追踪面板进入副本要拦截住
            LOG_WARN('task is trying enter dungeon')
            return True
        return False

    def canClaimTask(self, owner, taskId):
        taskData = dataUtils.getTaskCfg(taskId)
        if taskId in self.taskRecordDic:
            LOG_WARN('       in canClaimTask, taskId in taskRecordDic')
            return gameclass.TaskCondResultCls(False)

        # 关联任务检查
        _openRelTaskIdsStr = dataUtils.getTaskFieldVal(taskData, 'OpenCondRelateTaskId')
        if _openRelTaskIdsStr and _openRelTaskIdsStr != '0':
            # 编辑器导出的数据 openRelTaskIdsStr，有可能是 str类型'0', int 类型0，int类型任务id
            _openRelTaskIdsStr = str(_openRelTaskIdsStr)
            if _openRelTaskIdsStr:
                relTaskIds = _openRelTaskIdsStr.split('|')
                for relTaskId in relTaskIds:
                    if not relTaskId:
                        continue
                    if not self.isTaskInStat(int(relTaskId), dataUtils.getTaskFieldVal(taskData, 'OpenCondRelateTaskState')):
                        LOG_WARN('     in canClaimTask, OpenCondRelateTask failed:', taskId)
                        return gameclass.TaskCondResultCls(False)

        # 校验物品
        itemCondResult = self.checkClaimTaskItemsCond(owner, taskId, taskData)
        if not itemCondResult:
            LOG_WARN('       in canClaimTask, check items failed, taskId:', taskId)
            return itemCondResult

        # 领取任务后发放物品，检查背包空间是否足够
        if not self.hasBagSpaceForClaimTask(owner, taskId):
            LOG_WARN('       in canClaimTask, space not enough')
            return gameclass.TaskCondResultCls(False, msgId=dataUtils.getTaskMsgId('taskClaimAlert_GetItem'))

        if dataUtils.getTaskFieldVal(taskData, 'TaskType') == gameconst.TaskType.TASK_TYPE_HOOK_REWARD:
            hookRewardTaskCheck = taskId in RRTID.DoOnceTaskList
            if hookRewardTaskCheck:
                data = RRTID.datas.get(taskId)
                if not data:
                    LOG_ERR('       in canClaimTask, hookRewardTaskNum cfg not exist: ', taskId)
                    return gameclass.TaskCondResultCls(False)

                myLevel = owner.getAvatarLevel()
                ClaimCondLevelMin = data.get('minLevel', 0)
                if myLevel < ClaimCondLevelMin:
                    LOG_WARN('       in canClaimTask, hookRewardTaskNum level limit, ', taskId, myLevel, ClaimCondLevelMin)
                    return gameclass.TaskCondResultCls(False)
            else:
                hookRewardTaskCheck |= taskId in self.hookRewardTaskIdListDaily
                hookRewardTaskCheck |= taskId in self.hookRewardTaskIdListWeekly

            if not hookRewardTaskCheck:
                LOG_WARN('       in canClaimTask, hookRewardTaskId not in hookRewardTaskIdList, taskId is ', taskId, 'daily list is ', self.hookRewardTaskIdListDaily, 'weekly list is ', self.hookRewardTaskIdListWeekly, 'task count limit ', dataUtils.getTaskFieldVal(taskData, 'OpenCondCountLimit'))
                return gameclass.TaskCondResultCls(False)
            if self.hookRewardTaskFnsNumWeekly > RRTIC.datas.get('weeklyMaxNum', {}).get('value', 0) :
                LOG_WARN('       in canClaimTask, hookRewardTaskFnsNumWeekly exceed at', self.hookRewardTaskFnsNumWeekly)
                return gameclass.TaskCondResultCls(False)
            if self.hookRewardTaskNum > RRTIC.datas.get('currentlyMaxNum', {}).get('value', 0) :
                LOG_WARN('       in canClaimTask, hookRewardTaskNum exceed at', self.hookRewardTaskNum)
                return gameclass.TaskCondResultCls(False)

        # 开启变量检查
        _fmlId = dataUtils.getTaskFieldVal(taskData, 'OpenCondVarCheckFormID')
        if _fmlId and not dataUtils.checkVariableCond(owner, _fmlId, dataUtils.getTaskFieldVal(taskData, 'OpenCondVarCheckParam')):
            LOG_WARN('       in canClaimTask, open variable cond failed')
            return gameclass.TaskCondResultCls(False)

        # 领取变量条件
        _fmlId = taskData.get('ClaimCondVarCheckFormID')
        if _fmlId and not dataUtils.checkVariableCond(owner, _fmlId, dataUtils.getTaskFieldVal(taskData, 'ClaimCondVarCheckParam')):
            LOG_WARN('       in canClaimTask, claim variable cond failed')
            return gameclass.TaskCondResultCls(False)

        task = self.getTaskObj(taskId)
        if task is not None:
            # 以下条件，只校验根任务
            if task.parentTaskId != 0:
                return gameclass.TaskCondResultCls(True)

            if not task.isInEndStat():
                # 运行中或失败状态的任务不能重新领取
                LOG_WARN('     in canClaimTask, task not in end state:', taskId)
                return gameclass.TaskCondResultCls(False)

            if task.cycleType == gameconst.TaskCycleType.CYCLE_TASK_ENUM_NONE:
                # 成功后是否重复开启， 只对非周期任务有效
                if task.isStat(gameconst.TaskStatEnum.TASK_STAT_SUBMITTED):
                    OpenCondRepeatIfSucess = dataUtils.getTaskFieldVal(taskData, 'OpenCondRepeatIfSucess')
                    if not OpenCondRepeatIfSucess:
                        # 成功后不允许再次开启
                        LOG_WARN('     in canClaimTask, OpenCondRepeatIfSucess is False', taskId)
                        return gameclass.TaskCondResultCls(False)
                elif task.isStat(gameconst.TaskStatEnum.TASK_STAT_QUIT):
                    OpenCondRepeatIfQuit = dataUtils.getTaskFieldVal(taskData, 'OpenCondRepeatIfFail')
                    if not OpenCondRepeatIfQuit:
                        # 任务放弃后不允许再次开启
                        LOG_WARN('     in canClaimTask, OpenCondRepeatIfFail is False', taskId)
                        return gameclass.TaskCondResultCls(False)
            elif dataUtils.getTaskFieldVal(taskData, 'OpenCondTaskeState') == TaskCountLimitType.TASK_LIMIT_CLAIM_COUNT and task.limitCount != 0 and task.claimCount >= task.limitCount:
                # 领取任务领取次数已满，不能领取任务
                LOG_WARN('     in canClaimTask, can not claim, task.claimCount >= task.limitCount:', task.claimCount, task.limitCount)
                return gameclass.TaskCondResultCls(False, dataUtils.getTaskMsgId('taskClaimAlert_TimesCheck'))

            elif dataUtils.getTaskFieldVal(taskData, 'OpenCondTaskeState') == TaskCountLimitType.TASK_LIMIT_SUBMIT_COUNT and task.limitCount != 0 and task.alreadyCount >= task.limitCount:
                # 提交次数已满，不能领取任务
                LOG_WARN('     in canClaimTask, can not claim, task.alreadyCount >= task.limitCount:', task.alreadyCount, task.limitCount)
                return gameclass.TaskCondResultCls(False, dataUtils.getTaskMsgId('taskClaimAlert_TimesCheck'))

        return gameclass.TaskCondResultCls(True)

    def addTask(self, owner, taskId, taskData, taskCtx):
        addTaskIds = []
        _oldTask = self.getTaskObj(taskId)
        oldClaimCount = 0
        oldAlreadyCount = 0
        taskRewardLimitDic = {}
        if _oldTask and _oldTask.parentTaskId == 0:
            oldClaimCount = _oldTask.claimCount
            oldAlreadyCount = _oldTask.alreadyCount
            taskRewardLimitDic = _oldTask.taskRewardLimitDic
        # 创建一个新任务对象
        _task = Task.TaskFactory.createTask(owner, taskId, taskCtx, alreadyCount=oldAlreadyCount,
                                           claimCount=oldClaimCount,
                                           taskRewardLimitDic=taskRewardLimitDic)
        if not _task:
            gameengine.panicStack('     in addTask, create _task error:', taskId)
            return
        self.tasks[taskId] = _task
        addTaskIds.append(taskId)
        # childTasks
        _childTaskIds = _task.childTaskIds
        claimChildTaskIds = []
        if len(_childTaskIds) > 0:
            if dataUtils.getTaskFieldVal(taskData, 'ChildDoInQueue'):
                # 顺序完成子任务
                claimChildTaskIds.append(_childTaskIds[0])
            elif dataUtils.getTaskFieldVal(taskData, 'ChildDoInRandom'):
                if dataUtils.getTaskFieldVal(taskData, 'RandomWithWeight'):
                    taskId = self.calculateRandomTaskWithWeight(_task, taskData)
                    claimChildTaskIds.append(taskId)
                    _task.lastChildTaskId = taskId
                else:
                    # 随机完成子任务; 注意，连续两次随机到的任务不能是同一个，所以首先进行的子任务(位置0的子任务)
                    # 不能与 lastChildTaskId 相同
                    if _oldTask and _childTaskIds[0] == _oldTask.lastChildTaskId and len(_childTaskIds) > 1:
                        _childTaskIds[0], _childTaskIds[-1] = _childTaskIds[-1], _childTaskIds[0]
                    claimChildTaskIds.append(_childTaskIds[0])
            elif dataUtils.getTaskFieldVal(taskData, 'ChildDoInSelection'):
                claimChildTaskIds = [ctid for ctid in _childTaskIds]
            elif dataUtils.getTaskFieldVal(taskData, 'ChildDoInSameTime'):
                claimChildTaskIds = [ctid for ctid in _childTaskIds]
            else:
                claimChildTaskIds = [ctid for ctid in _childTaskIds]

        for childTaskId in claimChildTaskIds:
            childTaskData = dataUtils.getTaskCfg(childTaskId)
            addChildTaskIds = self.addTask(owner, childTaskId, childTaskData, taskCtx)
            if not addChildTaskIds:
                # 添加子任务失败，回溯父任务
                if _oldTask:
                    self.tasks[taskId] = _oldTask
                else:
                    self.remTask(taskId)
                gameengine.panicStack('addTask error, addChildTaskIds:', addChildTaskIds)
                return None
            addTaskIds.extend(addChildTaskIds)
            _task.lastChildTaskId = childTaskId
        return addTaskIds

    def calculateRandomTaskWithWeight(self, task, taskData):
        LOG_INFO("calculateRandomTaskWithWeight 0", task, taskData, self.randomTaskWeights)
        guaranteeCount = 0
        taskType = dataUtils.getTaskFieldVal(taskData, 'TaskType')
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

        LOG_INFO("calculateRandomTaskWithWeight 1", task, self.randomTaskWeights)
        # 到达指定次数，出保底
        if guaranteeCount >= dataUtils.getTaskFieldVal(taskData, 'GuaranteeCount'):
            guaranteeTaskId = dataUtils.getTaskFieldVal(taskData, 'GuaranteeTaskId')
            # 兼容不同版本的保底任务配置
            taskId = guaranteeTaskId
            if type(guaranteeTaskId) is list:
                taskId = random.choice(guaranteeTaskId)

            if taskType == gameconst.TaskType.TASK_TYPE_SPIRIT:
                self.randomTaskWeights.pop(task.taskId, 0)
            else:
                task.guaranteeCount = 0
            LOG_INFO("calculateRandomTaskWithWeight 2", task, taskId, self.randomTaskWeights)
            return taskId
        else:
            # 子任务对应的权重配置
            weights = dataUtils.getTaskFieldVal(taskData, 'ChildTaskWeights')
            # 抽取权重对应的索引位置
            randIdx = utils.randomByWeight(weights)
            # 根据索引位置取出子任务id
            taskId = task.childTaskIds[randIdx]
            LOG_INFO("calculateRandomTaskWithWeight 3", task, taskId, self.randomTaskWeights)
            # 抽到保底了，清零
            hasGuaranteeTaskId = False
            guaranteeTaskId = dataUtils.getTaskFieldVal(taskData, 'GuaranteeTaskId')
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
                LOG_INFO("calculateRandomTaskWithWeight 4", task, taskId, self.randomTaskWeights)
            return taskId

    def doRelateTaskReachStat(self, owner, relateTaskId, relateTaskStat):
        _taskIds = TRD.datas.get(str(relateTaskId), {}).get(str(relateTaskStat))
        if not _taskIds:
            return
        _rmTasks = []
        for taskId in _taskIds:
            task = self.getTaskObj(taskId)
            if not task:
                continue
            if not task.isStat(gameconst.TaskStatEnum.TASK_STAT_RUNNING):
                continue
            result = task.checkTgtRelateTaskStat(relateTaskId, relateTaskStat)
            if not result:
                continue
            LOG_INFO('     TaskInfo::doRelateTaskReachStat, taskId:', taskId, relateTaskId, relateTaskStat)
            _rmTasks.append(task)
        for rmTask in _rmTasks:
            self.checkTaskFinished(owner, rmTask)
            self.addSendUpdatedTaskList([rmTask, ])
        return

    def doAddTgtItemByRelateAction(self, owner, srcId, gameEntityId):
        if srcId <= 0:
            return
        _taskIds = TISD.datas.get(str(srcId))
        if not _taskIds:
            return
        wealthVal = dropAward.AwardVal()
        for taskId in _taskIds:
            task = self.getTaskObj(taskId)
            if task is None:
                continue
            if not task.isStat(gameconst.TaskStatEnum.TASK_STAT_RUNNING):
                continue
            tgtList = task.getTgtsByType(gameconst.TaskTargetType.TASK_TARGET_ITEMS)
            for _tgt in tgtList:
                LOG_DBG('     in doAddTgtItemByRelateAction, _taskIds:', _tgt.srcIdList, _tgt.srcRatio)
                _itemCount = owner.getItemNum(_tgt.tgtId)
                if _itemCount >= _tgt.dstCnt:
                    continue
                if srcId not in _tgt.srcIdList:
                    continue
                if _tgt.srcRatio > 0:
                    rdDigit = random.randint(1, 100)
                    LOG_DBG('     in doAddTgtItemByRelateAction, random digit:', rdDigit)
                    if rdDigit > _tgt.srcRatio:
                        continue
                    wealthVal.addWealthByItemId(_tgt.tgtId, 1, dataUtils.getItemDefaultBindType())

        if not wealthVal.isEmpty():
            _srcType = AAC_AACDD.datas.BONUS_SRC_ADD_TASK_ITEMS
            _opUUID = KBEngine.genUUID64()
            _detail = gameclass.AwardDetail(taskId=[_taskIds[0] if _taskIds else 0])
            _awardCtx = awardContext.CommonContext(0)
            if not owner.canAddWealthVal(_srcType, wealthVal, _awardCtx):
                owner.onMessagePre(dataUtils.getTaskMsgId('taskSubmitAlert_BagCheck'), [])
                return
            owner.addWealth(_srcType, wealthVal, _opUUID, _detail)

    def doTaskLeaveDungeon(self, owner, taskId):
        task = self.getTaskObj(taskId)
        if not task:
            return
        if task.isInEndStat():
            return
        taskData = dataUtils.getTaskCfg(task.taskId)
        if dataUtils.getTaskFieldVal(taskData, 'FailCondFailIfQtInst'):
            # 离开副本任务失败
            LOG_INFO('     TaskInfo::doTaskLeaveDungeon, task failed:', taskId)
            self.doTaskFailed(owner, task.taskId, gameconst.TaskNotSuccReasonEnum.LEAVE_SPACE)

    def completeTargetAction(self, owner, taskId, actionId):
        _task = self.getTaskObj(taskId)
        if not _task:
            return False, False
        if not _task.isStat(gameconst.TaskStatEnum.TASK_STAT_RUNNING):
            return False, False
        updated, tgtArrived = _task.setActionTgtCompleted(actionId)
        if not updated:
            return updated, tgtArrived
        if tgtArrived:
            self.checkTaskFinished(owner, _task)
        self.addSendUpdatedTaskList([_task, ])
        return updated, tgtArrived

    def completeTaskNoTarget(self, owner, taskId):
        _task = self.getTaskObj(taskId)
        if not _task:
            return
        self.checkTaskFinished(owner, _task)
        return

    def doTaskVariableChanged(self, owner, taskId, varId):
        _task = self.getTaskObj(taskId)
        if not _task or not _task.isStat(gameconst.TaskStatEnum.TASK_STAT_RUNNING):
            return

        LOG_INFO('doTaskVariableChanged:', _task.taskId, varId)
        taskData = dataUtils.getTaskCfg(_task.taskId)
        # 触发任务失败
        _fmlId = dataUtils.getTaskFieldVal(taskData, 'FailCondVarCheckFormID')
        if _fmlId and dataUtils.checkVariableCond(owner, _fmlId,
                                                 dataUtils.getTaskFieldVal(taskData, 'FailCondVarCheckParam')):
            LOG_INFO('       doTaskVariableChanged, failed var is True')
            self.doTaskFailed(owner, _task.taskId, gameconst.TaskNotSuccReasonEnum.VARIABLE)
            return

        # 触发任务目标完成
        _fmlId = dataUtils.getTaskFieldVal(taskData, 'FinCondVarCheckFormID')
        if not _fmlId:
            return
        tgts = _task.getTgtsByType(gameconst.TaskTargetType.TASK_TARGET_VAR)
        for tgt in tgts:
            if tgt.checkVarCond(owner, _fmlId, dataUtils.getTaskFieldVal(taskData, 'FinCondVarCheckParam')):
                self.checkTaskFinished(owner, _task)
        return

    def checkTaskFinished(self, owner, task):
        # 任务可以设置为 TASK_STAT_FINISHED 的情况(李策)，在任务目标都已经完成的前提下，有以下3种情况：
        # 1.其下的某个子任务完成提交操作，并且设置了 FaterSuccIfChildSucc
        # 2.其下的所有子任务都已提交
        # 3.服务器使其完成
        if not task.checkAllTargetsReached():
            return False

        for _childTaskId in task.childTaskIds:
            childTask = self.getTaskObj(_childTaskId)
            if not childTask:
                continue
            if not childTask.isStat(gameconst.TaskStatEnum.TASK_STAT_SUBMITTED):
                return False
        self.onTaskFinished(owner, task)
        return True

    def onTaskFinished(self, owner, task):
        LOG_INFO('in TaskInfo::onTaskFinished, taskId:', task.taskId)
        taskData = dataUtils.getTaskCfg(task.taskId)
        task.setStat(owner, gameconst.TaskStatEnum.TASK_STAT_FINISHED)
        self.addSendUpdatedTaskList([task, ])
        if dataUtils.getTaskFieldVal(taskData, 'DeliMetdNoLimit'):
            # 先校验一次base的提交条件，如果不满足，就不用去cell校验条件了
            if self.checkSubmitBaseCond(owner, task.taskId):
                # 任务自动提交
                owner.startSubmitTask(task.taskId)
        return

    def relateSubmitTaskList(self, taskId):
        _taskIdList = [taskId]
        task = self.getTaskObj(taskId)
        parentTask = self.getTaskObj(task.parentTaskId)
        _childTaskId = taskId
        while parentTask and parentTask.childTaskIds:
            childTaskData = dataUtils.getTaskCfg(_childTaskId)
            if dataUtils.getTaskFieldVal(childTaskData, 'FaterSuccIfChildSucc') or taskId == parentTask.childTaskIds[-1]:
                _taskIdList.append(parentTask.taskId)
                _childTaskId = parentTask.taskId
                parentTask = self.getTaskObj(parentTask.parentTaskId)
            else:
                break
        return _taskIdList

    def checkTaskSubmitRewardCond(self, owner, task):
        if not dataUtils.isLeafTask(task.taskId):
            return True
        _taskIdList = self.relateSubmitTaskList(task.taskId)
        for taskId in _taskIdList:
            if not self._canSubmitTaskReward(owner, taskId):
                return False
        return True

    def _canSubmitTaskReward(self, owner, taskId):
        _taskData = dataUtils.getTaskCfg(taskId)
        if not dataUtils.getTaskFieldVal(_taskData, 'FinRewardID'):
            # 任务完成无 rewardId 奖励
            return True

        task = self.getTaskObj(taskId)
        if task.isEmptyTarget() and dataUtils.getTaskFieldVal(_taskData, 'DeliMetdNoLimit'):
            # 没有任务目标及自动提交的任务
            return True

        # 挂机玩法任务奖励不受背包限制，背包满时，通过邮件发放奖励；
        if owner.bagData.isFull() and not dataUtils.getTaskFieldVal(_taskData, 'IsAutoTask'):
            LOG_WARN('_canSubmitTaskReward, bag full:', taskId)
            if not dataUtils.getTaskFieldVal(_taskData, 'DispHiddenTask'):
                owner.onMessagePre(dataUtils.getTaskMsgId('taskSubmitAlert_BagCheck'), [])
            return False
        return True

    def checkSubmitBaseCond(self, owner, taskId):
        _task = self.getTaskObj(taskId)
        if not _task or _task.isInEndStat() or not _task.isStat(gameconst.TaskStatEnum.TASK_STAT_FINISHED):
            # 必须处于 TASK_STAT_FINISHED 状态，才允许提交任务
            LOG_WARN('   checkSubmitBaseCond check failed, no _task or _task state error')
            return False

        if not self.checkTaskSubmitRewardCond(owner, _task):
            LOG_WARN('   checkSubmitBaseCond check failed, submit reward cond failed')
            return False

        for _childTaskId in _task.childTaskIds:
            childTask = self.getTaskObj(_childTaskId)
            if not childTask:
                # 任务提交条件，不需要所有子任务都已经领取
                continue
            if not childTask.isStat(gameconst.TaskStatEnum.TASK_STAT_SUBMITTED):
                gameengine.panicStack('   checkSubmitBaseCond check failed, child _task state error:',
                                          _childTaskId, childTask.stat)
                return False
        return True

    def deductTaskTgtItems(self, owner, taskId):
        _task = self.getTaskObj(taskId)
        if not _task or _task.isInEndStat() or _task.isStat(gameconst.TaskStatEnum.TASK_STAT_FINISHED):
            LOG_WARN('in deductTaskTgtItems, _task error:', _task, taskId)
            return
        deductWealthVal = _task.getTaskTgtItemsWealthVal()
        if not owner.canDeductWealth(deductWealthVal):
            _task.updateTgtItemsCount(owner)
            _task.setStat(owner, gameconst.TaskStatEnum.TASK_STAT_RUNNING)
            self.sendUpdatedTaskNow(owner, _task)
            return False

        _opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_COMPLETE_TASK
        _detail = gameclass.AwardDetail(taskId=taskId)
        owner.deductWealth(srcType, deductWealthVal, _opUUID, _detail)
        _task.deductTaskTgtItemsSucc()
        self.checkTaskFinished(owner, _task)
        self.addSendUpdatedTaskList([_task, ])
        return True

    def doSubmitTask(self, owner, taskId, popRewardUUID=0, check=True):
        # do reward and submit _task
        _task = self.getTaskObj(taskId)
        if not _task:
            LOG_WARN('in doSubmitTask, no _task')
            return

        if check and not _task.isStat(gameconst.TaskStatEnum.TASK_STAT_FINISHED):
            LOG_WARN('in doSubmitTask, _task not in target finish state:', _task.stat)
            return

        if _task.isStat(gameconst.TaskStatEnum.TASK_STAT_SUBMITTED):
            LOG_WARN('in doSubmitTask, already submit :', _task.stat)
            return

        _task.setStat(owner, gameconst.TaskStatEnum.TASK_STAT_SUBMITTED)
        owner.flowCtrlOnTaskComplete(taskId)
        # flow controller notify

        # 如果是悬赏任务，则更新同时接取的限制状态
        if _task.taskType == gameconst.TaskType.TASK_TYPE_HOOK_REWARD:
            if _task.cycleType == gameconst.TaskCycleType.CYCLE_TASK_ENUM_DAYLY \
                or _task.cycleType == gameconst.TaskCycleType.CYCLE_TASK_ENUM_WEEKLY:

                self.hookRewardTaskFnsNumWeekly += 1
                owner.client.onHookRewardTaskWeeklyLimitRefresh(self.hookRewardTaskFnsNumWeekly)

            if _task.cycleType == gameconst.TaskCycleType.CYCLE_TASK_ENUM_DAYLY \
                or _task.cycleType == gameconst.TaskCycleType.CYCLE_TASK_ENUM_WEEKLY \
                or _task.cycleType == gameconst.TaskCycleType.CYCLE_TASK_ENUM_ONCE:

                self.hookRewardTaskNum = max(self.hookRewardTaskNum-1, 0)

        _task.alreadyCount += 1
        self.sendUpdatedTaskNow(owner, _task)
        self._afterTaskSubmitted(owner, _task, popRewardUUID)
        return True

    def _afterTaskSubmitted(self, owner, task, popRewardUUID=0):
        LOG_INFO("_afterTaskSubmitted ", task, popRewardUUID)
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
            LOG_INFO("_afterTaskSubmitted 1 ", task)
            self.onChildtaskSubmitted(owner, task)

        return

    def _autoClaimRoundTask(self, owner, task):
        taskData = dataUtils.getTaskCfg(task.taskId)
        _roundVal, _, _, _ = dataUtils.getTaskRoundInfo(taskData)
        if _roundVal > 0:
            if task.alreadyCount % _roundVal != 0:
                LOG_INFO('in autoClaimRoundTask, auto claim new task:', task.taskId, _roundVal, task.alreadyCount)
                owner.cell.startClaimTask(
                    task.taskId, 
                    '', 
                    (),
                    actionContext.ClaimTaskCtx(claimSrc=gameconst.ClaimTaskSrcEnum.TASK_SRC_ROUND_AUTO_CLAIM))

    def forceCompleteTask(self, owner, taskId):
        _task = self.getTaskObj(taskId)
        if not _task or _task.isInEndStat():
            return False
        _task.setAllTargetsReached(owner)
        for childTaskId in _task.childTaskIds:
            childTask = self.getTaskObj(childTaskId)
            if childTask and self.forceCompleteTask(owner, childTaskId):
                # 正常调用不会走到这里，对于非叶节点任务，状态直接设置为已提交
                LOG_WARN('forceCompleteTask, childTask:', taskId, childTaskId)
                childTask.setStat(owner, gameconst.TaskStatEnum.TASK_STAT_SUBMITTED)
                self.sendUpdatedTaskNow(owner, childTask)
        self.onTaskFinished(owner, _task)
        return True

    def _rewardItemsOnTaskEnd(self, owner, taskId, rewardId, opUUID, srcType, popRewardUUID=0):
        if rewardId > 0:
            LOG_INFO('in _rewardItemsOnTaskEnd:', taskId, rewardId, popRewardUUID)
            awardCtx = awardContext.CommonContext(gameconst.MailConstID.REWARD_MAIL_ID)
            awardCtx = owner._getAvatarAwardCtx(rewardId, awardCtx)

            taskVal = self.getTaskObj(taskId)
            if taskVal:
                rewardItemArgs = taskVal.extraAttr.getExtraAttr('rewardItemArgs', {})
                if rewardItemArgs:
                    awardCtx.itemArgs.update(rewardItemArgs)
            wealthVal = dropAward.getAward(rewardId, 1, awardCtx)

            if not wealthVal.isEmpty():
                directly = True
                taskData = dataUtils.getTaskCfg(taskId)
                detail = gameclass.AwardDetail(taskId=[taskId], popRewardUUID=popRewardUUID)
                owner.addWealth(srcType, wealthVal, opUUID, detail=detail, awardCtx=awardCtx, directly=directly)

    def doSubmitReward(self, owner, taskId, opUUID, srcType, popRewardUUID=0):
        # 检查发奖次数是否满足
        task = self.getTaskObj(taskId)
        _rootTask = self.getTaskObj(task.rootTaskId)
        _taskData = dataUtils.getTaskCfg(taskId)
        rewardId = dataUtils.getTaskFieldVal(_taskData, 'FinRewardID')
        finRewardCountLimit = dataUtils.getTaskFieldVal(_taskData, 'FinRewardCountLimit')
        finRewardCountLimit = finRewardCountLimit or 1
        if rewardId and _rootTask.canAddRewardId(task.taskId, rewardId, finRewardCountLimit):
            # 道具和物品奖励
            _rootTask.recordSubmitTaskRewardId(taskId, rewardId)
            self._rewardItemsOnTaskEnd(owner, taskId, rewardId, opUUID, srcType, popRewardUUID)

        _roundVal, roundRwdList, _roundActList, roundParamList = dataUtils.getTaskRoundInfo(_taskData)
        if task.parentTaskId == 0 and _roundVal > 0 and task.alreadyCount > 0 and task.alreadyCount % _roundVal == 0 and roundRwdList:
            roundIdx = task.alreadyCount // _roundVal - 1
            if roundIdx < len(roundRwdList):
                self._rewardItemsOnTaskEnd(owner, taskId, roundRwdList[roundIdx], opUUID, srcType, popRewardUUID)

            if _roundActList and roundParamList and roundIdx < len(_roundActList) and roundIdx < len(roundParamList):
                owner.doTaskEvent(gameconst.EventActionSrc.SRC_ROUND_TASK, taskId,
                                  _roundActList[roundIdx], roundParamList[roundIdx])

        #奖励进入副本 与 奖励传出当前副本， 二者同时只能有一个生效
        if dataUtils.getTaskFieldVal(_taskData, 'FinHasRewardInst'):
            if task.claimSrc!=gameconst.ClaimTaskSrcEnum.TASK_SRC_GM_FINISH_NEWBIE:
            #如果是GM完成新手就不进出副本了，因为进去马上会出来，瞬间多次传送支持不了
                self._rewardEnterDungeon(owner, taskId, dataUtils.getTaskFieldVal(_taskData, 'FinRewardInstance'))
        else:
            self._rewardLeaveDungeon(owner, _taskData, taskId, task.claimSrc)
        #奖励发放任务
        self._rewardNewTask(owner, dataUtils.getTaskFieldVal(_taskData, 'FinRewardTaskID'))
        # 检查是否有事件需要处理
        owner.doTaskEvent(gameconst.EventActionSrc.SRC_SUBMIT_TASK, taskId,
                          dataUtils.getTaskFieldVal(_taskData, 'FinRewardEventName'),
                          dataUtils.getTaskFieldVal(_taskData, 'FinRewardEventParam'))
        # 是否需要播放动画
        storyId = dataUtils.getTaskFieldVal(_taskData, 'FinRewardTriggerStoryID')
        if storyId:
            # 播放剧情动画
            owner.client.onStartPlayCinema(storyId)
            # 回调cell做后续处理
            owner.cell.afterPlayCinema(storyId)

        # 修改变量
        if dataUtils.getTaskFieldVal(_taskData, 'FinRewardCanVarMod'):
            varSrc = gameconst.VarChangeSrcEnum.VAR_SRC_TASK_SUBMIT
            for varData in dataUtils.getTaskFieldVal(_taskData, 'FinRewardVarModInfo'):
                owner.taskSetVar(taskId, opUUID, varSrc, varData['TargetVar'], varData['FormId'],
                                      varData['ParamVar'])

    def quitTaskReward(self, owner, taskId, opUUID, srcType):
        # LOG_INFO('in quitTaskReward:', taskId)
        # 检查发奖次数是否满足
        taskData = dataUtils.getTaskCfg(taskId)
        # 道具和物品奖励
        rewardId = taskData.get('AbanRewardID', 0)
        if rewardId > 0:
            _rootTask = self.getRootTask(taskId)
            if _rootTask.canAddRewardId(taskId, rewardId):
                self._rewardItemsOnTaskEnd(owner, taskId, rewardId, opUUID, srcType)
        # 进入副本的奖励
        if dataUtils.getTaskFieldVal(taskData, 'AbanHasRewardInst'):
            self._rewardEnterDungeon(owner, taskId, dataUtils.getTaskFieldVal(taskData, 'AbanRewardInstance'))
        #奖励发放任务
        self._rewardNewTask(owner, dataUtils.getTaskFieldVal(taskData, 'AbanRewardTaskID'))
        # 检查是否有事件需要处理
        owner.doTaskEvent(gameconst.EventActionSrc.SRC_QUIT_TASK, taskId,
                          dataUtils.getTaskFieldVal(taskData, 'AbanRewardEventName'),
                          dataUtils.getTaskFieldVal(taskData, 'AbanRewardEventParam'))

    def _rewardLeaveDungeon(self, owner, taskData, taskId, claimSrc):
        if dataUtils.getTaskFieldVal(taskData, 'FinRewardLeaveInstance'):
            leaveDungeonNo = dataUtils.getTaskFieldVal(taskData, 'FinRewardLevInsID')
            if not leaveDungeonNo:
                LOG_WARN('in _rewardLeaveDungeon, no leaveDungeonNo:', taskId, leaveDungeonNo)
                return
            LOG_INFO('_rewardLeaveDungeon, leave dungeonNo:', taskId)
            owner.cell.onTaskRwdLeaveDungeon(taskId, leaveDungeonNo, claimSrc)

    def _rewardEnterDungeon(self, owner, taskId, newDungeonData):
        LOG_INFO('in _rewardEnterDungeon:', taskId, newDungeonData)
        self._taskEnterSpace(owner, taskId, newDungeonData)

    def _rewardNewTask(self, owner, newtaskIdsStr):
        if not newtaskIdsStr:
            return
        _newTaskIds = newtaskIdsStr.split('|')
        for _newTaskId in _newTaskIds:
            if not _newTaskId.isdigit():
                continue
            _newTaskId = int(_newTaskId)
            if _newTaskId <= 0:
                continue
            self.rewardTaskCacheDic[_newTaskId] = utils.curTS()
            owner.cell.startClaimTask(_newTaskId, '', (),
                                      actionContext.ClaimTaskCtx(claimSrc=gameconst.ClaimTaskSrcEnum.TASK_SRC_REWARD_TASK))

    def onChildtaskSubmitted(self, owner, task):
        LOG_INFO("onChildtaskSubmitted ", task)
        parentTask = self.getTaskObj(task.parentTaskId)
        if not parentTask:
            LOG_ERR('child task[Id={}] config parent task[Id={}] but not found parent task on avatar body'.format(
                task.taskId, task.parentTaskId))
            return

        if gameconst.TaskStatEnum.TASK_STAT_FINISHED == parentTask.stat:
            LOG_INFO("onChildtaskSubmitted 1 ", parentTask)
            owner.startSubmitTask(parentTask.taskId)
            return
        if gameconst.TaskStatEnum.TASK_STAT_RUNNING != parentTask.stat:
            LOG_INFO("onChildtaskSubmitted 2 ", parentTask)
            return

        childTaskData = dataUtils.getTaskCfg(task.taskId)
        FaterSuccIfChildSucc = dataUtils.getTaskFieldVal(childTaskData, 'FaterSuccIfChildSucc')
        if FaterSuccIfChildSucc:
            LOG_INFO("onChildtaskSubmitted 3 ", parentTask)
            # 子任务成功，则父任务也成功
            self.onTaskFinished(owner, parentTask)
            return

        # 是否需要添加新的子任务
        if self.addNewChildTask(owner, task.taskId, parentTask):
            # 需要进行新的子任务（已经发放新的子任务，或者等待玩家选择新的子任务）
            return

        for childTaskId in parentTask.childTaskIds:
            childTask = self.getTaskObj(childTaskId)
            if not childTask:
                # 尚有未领取的子任务
                return
            if childTask and not childTask.isStat(gameconst.TaskStatEnum.TASK_STAT_SUBMITTED):
                return

        # 所有子任务都已经完成并提交了
        self.onTaskFinished(owner, parentTask)
        return

    def addNewChildTask(self, owner, childTaskId, parentTask):
        LOG_INFO("addNewChildTask 1", childTaskId, parentTask)
        # taskData['ChildDoInSameTime'] 领取父任务时候就领取了所有子任务，所以这里不需要做检查
        taskData = dataUtils.getTaskCfg(parentTask.taskId)
        if dataUtils.getTaskFieldVal(taskData, 'ChildDoInQueue') or dataUtils.getTaskFieldVal(taskData, 'ChildDoInRandom'):
            LOG_INFO("addNewChildTask 2", parentTask)
            taskId = -1
            if dataUtils.getTaskFieldVal(taskData, 'RandomWithWeight'):
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
        elif dataUtils.getTaskFieldVal(taskData, 'ChildDoInSelection'):
            # 等待玩家重新选择子任务
            return True
        return False

    def doTaskFailed(self, owner, taskId, reason=gameconst.TaskNotSuccReasonEnum.AUTO_QUIT):
        uptaskList = []
        task = self.getTaskObj(taskId)
        if not task:
            LOG_ERR(' in doTaskFailed, task not exist:', taskId, reason)
            return

        if task.isInEndStat():
            return

        LOG_INFO('in TaskInfo::doTaskFailed taskId {} reason {}'.format(taskId, reason))
        task.setStat(owner, gameconst.TaskStatEnum.TASK_STAT_FAILED)
        uptaskList.append(task)
        # set flow
        owner.flowCtrlOnTaskFailed(taskId)

        # 所有子任务也失败
        childTaskIds = self.getChildTaskIds(task.taskId)
        failedTaskIds = [taskId, ]
        for childTaskId in childTaskIds:
            childTask = self.getTaskObj(childTaskId)
            if childTask is None:
                continue
            if childTask.isInEndStat():
                continue
            childTask.setStat(owner, gameconst.TaskStatEnum.TASK_STAT_FAILED)
            failedTaskIds.append(childTaskId)
            uptaskList.append(childTask)
        self._afterTaskFailed(owner, failedTaskIds)
        self.addSendUpdatedTaskList(uptaskList)
        if task.parentTaskId != 0:
            self.onChildTaskFailed(owner, task)

        # 检查任务失败后是否自动放弃
        taskData = dataUtils.getTaskCfg(taskId)
        if dataUtils.getTaskFieldVal(taskData, 'FailCondQuitIfFail'):
            owner.startQuitTask(taskId, reason)
        return True

    def _afterTaskFailed(self, owner, quitTaskIds):
        self._afterTaskUpdateRemoved(owner, quitTaskIds)
        for taskId in quitTaskIds:
            task = self.getTaskObj(taskId)
            taskData = dataUtils.getTaskCfg(taskId)
            if dataUtils.getTaskFieldVal(taskData, 'OpenCondIsFailNoCount') and not dataUtils.getTaskFieldVal(taskData,
                                                                                                        'OpenCondIsAbanNoCount'):
                # 任务失败不记录次数; 任务失败和放弃只能返还一次领取次数， 所以如果勾选了放弃不记录次数，这里不要返还次数；
                if dataUtils.getTaskFieldVal(taskData, 'OpenCondTaskeState') == TaskCountLimitType.TASK_LIMIT_CLAIM_COUNT:
                    task.claimCount = max(0, task.claimCount - 1)

    def onChildTaskFailed(self, owner, childTask):
        childTaskData = dataUtils.getTaskCfg(childTask.taskId)
        if dataUtils.getTaskFieldVal(childTaskData, 'FatherFailIfChildFail'):
            LOG_INFO('onChildTaskFailed, FatherFailIfChildFail:', childTask.taskId, childTask.parentTaskId)
            self.doTaskFailed(owner, childTask.parentTaskId, gameconst.TaskNotSuccReasonEnum.CHILD_FAILED)

    def doAvatarDead(self, owner):
        for _taskId, task in self.tasks.items():
            if task.parentTaskId != 0:
                continue
            if not task.isStat(gameconst.TaskStatEnum.TASK_STAT_RUNNING) and not task.isStat(gameconst.TaskStatEnum.TASK_STAT_FINISHED):
                continue
            taskData = dataUtils.getTaskCfg(_taskId)
            FailCondIfDie = dataUtils.getTaskFieldVal(taskData, 'FailCondIfDie')
            if FailCondIfDie:
                LOG_INFO('in doAvatarDead, doTaskFailed:', _taskId)
                self.doTaskFailed(owner, _taskId, gameconst.TaskNotSuccReasonEnum.AVATAR_DIE)

    def canQuitTaskManual(self, taskId):
        taskData = dataUtils.getTaskCfg(taskId)
        if dataUtils.getTaskFieldVal(taskData, 'FailCondCanGiveUp'):
            # 任何状态可以手动放弃该任务
            return True

        if dataUtils.getTaskFieldVal(taskData, 'FailCondCanQuitIfFail') and self.getTaskCurrentState(
                taskId) == gameconst.TaskStatEnum.TASK_STAT_FAILED:
            # 仅失败状态可以手动放弃该任务
            return True

        LOG_INFO('canQuitTaskManual, task can not quit:', taskData['TaskId'])
        return False

    # 放弃任务
    def doQuitTask(self, owner, taskId, reason):
        task = self.getTaskObj(taskId)
        if not task or task.isInEndStat():
            return
        rootTaskId = task.rootTaskId
        LOG_INFO('doQuitTask, taskId {} rootTaskId {}:'.format(taskId, rootTaskId))
        _uptaskList = []
        _rootTask = self.getTaskObj(rootTaskId)
        if self.getTaskCurrentState(taskId) != gameconst.TaskStatEnum.TASK_STAT_FAILED:
            owner.flowCtrlOnTaskFailed(taskId)

        if not _rootTask:
            # 找不到根任务，这种情况只会出现在使用gm指令直接领取子任务的情况
            task.setStat(owner, gameconst.TaskStatEnum.TASK_STAT_QUIT)
            self.addSendUpdatedTaskList([task])
            self._afterTaskQuit(owner, [taskId], reason)
            gameengine.panicStack('in doQuitTask, no root task:', taskId, rootTaskId)
            return
        _rootTask.setStat(owner, gameconst.TaskStatEnum.TASK_STAT_QUIT)
        _quitTaskIds = set()
        _quitTaskIds.add(rootTaskId)
        _uptaskList.append(_rootTask)
        # 所有子任务也放弃
        childTaskIds = self.getChildTaskIds(_rootTask.taskId)
        for childTaskId in childTaskIds:
            childTask = self.getTaskObj(childTaskId)
            if childTask is None:
                continue
            if childTask.isStat(gameconst.TaskStatEnum.TASK_STAT_QUIT):
                continue
            childTask.setStat(owner, gameconst.TaskStatEnum.TASK_STAT_QUIT)
            _uptaskList.append(childTask)
            _quitTaskIds.add(childTaskId)


        # 如果是悬赏任务，则更新同时接取的限制状态
        if task.taskType == gameconst.TaskType.TASK_TYPE_HOOK_REWARD:
            if task.cycleType == gameconst.TaskCycleType.CYCLE_TASK_ENUM_DAYLY \
                or task.cycleType == gameconst.TaskCycleType.CYCLE_TASK_ENUM_WEEKLY \
                or task.cycleType == gameconst.TaskCycleType.CYCLE_TASK_ENUM_ONCE:

                self.hookRewardTaskNum = max(self.hookRewardTaskNum-1, 0)
                LOG_INFO('do quit task, self.hookRewardTaskNum is ', self.hookRewardTaskNum)

        self.addSendUpdatedTaskList(_uptaskList)
        self._afterTaskQuit(owner, _quitTaskIds, reason)

        return len(_quitTaskIds) > 0

    def _afterTaskQuit(self, owner, quitTaskIds, reason):
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_ABANDON_TASK
        self._afterTaskUpdateRemoved(owner, quitTaskIds)
        for taskId in quitTaskIds:
            # 任务放弃也可能有奖励
            self.quitTaskReward(owner, taskId, opUUID, srcType)

            task = self.getTaskObj(taskId)
            taskData = dataUtils.getTaskCfg(taskId)

            if dataUtils.getTaskFieldVal(taskData, 'OpenCondIsAbanNoCount'):
                # 任务放弃不记录次数
                if dataUtils.getTaskFieldVal(taskData, 'OpenCondTaskeState') == TaskCountLimitType.TASK_LIMIT_CLAIM_COUNT:
                    task.claimCount = max(task.claimCount - 1, 0)

            # 修改变量
            if dataUtils.getTaskFieldVal(taskData, 'AbanRewardCanVarMod'):
                varSrc = gameconst.VarChangeSrcEnum.VAR_SRC_TASK_QUIT
                for _varData in dataUtils.getTaskFieldVal(taskData, 'AbanRewardVarModInfo'):
                    owner.taskSetVar(taskId, opUUID, varSrc, _varData['TargetVar'], _varData['FormId'],
                                          _varData['ParamVar'])

            self.onTaskEnd(owner, taskId, opUUID, srcType)
        return

    def onTaskEnd(self, owner, taskId, opUUID, srcType):
        taskData = dataUtils.getTaskCfg(taskId)
        if dataUtils.getTaskFieldVal(taskData, 'ClaimCanRewardITems'):
            # 回收任务物
            owner.remTaskItems(taskId, opUUID, srcType)
        # 放弃任务时，需要处理掉背包里指定的任务道具
        if srcType == AAC_AACDD.datas.BONUS_SRC_ABANDON_TASK:
            owner.abandonTaskItems(taskId, opUUID, srcType)

        self.remReachAreaTargetTask(owner, taskId)
        self.removeTaskInCache(taskId)    

    def getRootTask(self, taskId):
        # 理论上最多10层子任务，实际应该不会超出10层
        rootTaskId = dataUtils.getRootTaskId(taskId)
        return self.getTaskObj(rootTaskId)

    def getLastChildTaskId(self, taskId, default=0):
        task = self.getTaskObj(taskId)
        if not task:
            return default
        lastChildTaskId = task.lastChildTaskId
        while lastChildTaskId > 0:
            _childTask = self.getTaskObj(lastChildTaskId)
            if not _childTask:
                return lastChildTaskId
            if _childTask.lastChildTaskId == 0:
                break
            lastChildTaskId = _childTask.lastChildTaskId
        return lastChildTaskId

    def getChildTaskIds(self, taskId, deep=0):
        if deep >= 5:
            gameengine.panicStack('getChildTaskIds, deep>=5:', taskId)
            return []
        childTaskIds = []
        taskData = dataUtils.getTaskCfg(taskId)
        for tid in dataUtils.getTaskFieldVal(taskData, 'ChildTaskIds'):
            childTaskIds.append(tid)
            tids = self.getChildTaskIds(tid, deep=deep + 1)
            tids and childTaskIds.extend(tids)
        return childTaskIds

    def _cleanOldChildTasks(self, owner, syncTaskIdList):
        remChildTaskIds = []
        for taskId in syncTaskIdList:
            _task = self.getTaskObj(taskId)
            if not _task:
                continue
            if _task.parentTaskId != 0:
                continue
            if dataUtils.isSingleSupportTeamTask(taskId) and not _task.isInEndStat():
                # 如果有进行中的单人支持的组队任务，不能被队长的任务覆盖
                continue
            remChildTaskIds.extend(self.remChildTask(_task.taskId))
        if len(remChildTaskIds) > 0:
            LOG_INFO('     in _cleanOldChildTasks, remChildTaskIds:', remChildTaskIds)
            owner.client.onTasksRem(remChildTaskIds)
        return

    def onTaskStepUpdate(self, owner, targetType, taskIds, args):
        LOG_DBG('TaskInfo::onTaskStepUpdate:', targetType, taskIds, args)
        if taskIds:
            if type(taskIds) not in (tuple, list):
                taskIds = (taskIds,)
        else:
            taskIds = self.tasks.keys()

        bUpdate = False
        for taskId in taskIds:

            task = self.getTaskObj(taskId)
            if not task or not task.isStat(gameconst.TaskStatEnum.TASK_STAT_RUNNING):
                continue

            targetList = task.getTgtsByType(targetType)
            if not targetList:
                continue

            if targetType == gameconst.TaskTargetType.TASK_TARGET_ITEMS:
                updated = task.updateTgtItemsCount(owner)
                if updated:
                    LOG_INFO('TaskInfo::onTaskStepUpdate items:', taskId, args)
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
                    LOG_INFO('TaskInfo::onTaskStepUpdate:', args)
                    self.checkTaskFinished(owner, task)
            elif targetType == gameconst.TaskTargetType.TASK_TARGET_COUNTER:
                if not task.addCounterNum(targetType, args):
                    continue
                tgtArrived = task.onTaskStepUpdate(targetType, args)
                self.addSendUpdatedTaskList([task, ])
                bUpdate = True
                if tgtArrived:
                    LOG_INFO('TaskInfo::onTaskStepUpdate arrived:', args)
                    self.checkTaskFinished(owner, task)
            else:
                tgtArrived = task.onTaskStepUpdate(targetType, args)
                if tgtArrived:
                    LOG_INFO('TaskInfo::onTaskStepUpdate arrived:', args)
                    self.checkTaskFinished(owner, task)
                    self.addSendUpdatedTaskList([task, ])
                    bUpdate = True
        return bUpdate

    def taskEnterSpace(self, owner, task):
        taskInfo = dataUtils.getTaskCfg(task.taskId)
        # 随任务接取后自动进入的
        if not dataUtils.getTaskFieldVal(taskInfo, 'ClaimCanTransIns'):
            LOG_ERR('taskEnterSpace illegal op 1', taskInfo)
            return False

        claimTransData = dataUtils.getTaskFieldVal(taskInfo, 'ClaimTransInstance')
        if not claimTransData:
            LOG_ERR('taskEnterSpace wrong cfg', taskInfo)
            return False

        needConfirm = claimTransData.get('NeedConfirm')
        # 不需要二次确认弹窗，接取任务主动进入地图
        if not needConfirm:
            LOG_ERR('taskEnterSpace illegal op 2', taskInfo)
            return False

        self._taskEnterSpace(owner, task.taskId, claimTransData)
        return True
