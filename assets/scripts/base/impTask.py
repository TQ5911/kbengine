# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

import json
import gzip

import utils
import dataUtils
import CommEventAction
import gameconst
import gameengine
import gametimer
import actionContext
import formula
import gamedecorator
import gameclass

import taskGetItems as TID
import taskCollect as TCD
import taskLeaveDungeon as TLDD
import taskCounter as TCTD
import taskAutoClaimRelatetask as TACRTD
import taskAutoClaimMinLevel as TACMLD
import taskAutoClaimCondItems as TACCID
import taskMonster as TMD
import taskdata as TDD
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import visible_visible as V_VD
import itemData_itemData as ITEM_DATA

class TaskEvent(object):
    def doTaskEvent(self, eventActionSrc, taskId, eventStr, paramStr):
        if not eventStr:
            return
        LOG_INFO('in doTaskEvent, eventStr:', eventActionSrc, eventStr, paramStr)
        _eventList = eventStr.split('|')
        _paramList = paramStr.split('|')
        for eventName, eventParams in zip(_eventList, _paramList):
            if not eventName:
                continue

            _eventActionInfo = CommEventAction.CommEventActionMap.get(eventName)
            if not _eventActionInfo:
                continue
            _actionType, _actionFunc = _eventActionInfo
            _eventArgs, eventKwargs = utils.parseCommEventParams(eventParams)
            eventKwargs['_srcTaskId'] = taskId
            if _actionType == CommEventAction.ActionType.BASE:
                _actionFunc(self, eventActionSrc, *_eventArgs, **eventKwargs)
            else:
                self.cell.doCellCommEvent(eventActionSrc, eventName, _eventArgs, eventKwargs)

    def doBaseCommEvent(self, eventActionSrc, eventName, eventArgs, eventKwargs):
        LOG_INFO('in doBaseCommEvent:', eventActionSrc, eventName, eventArgs, eventKwargs)
        _actionType, _actionFunc = CommEventAction.CommEventActionMap[eventName]
        if _actionType != CommEventAction.ActionType.BASE:
            gameengine.panicStack('doBaseCommEvent, actionType Error:', eventActionSrc, eventName, eventArgs,
                                      eventKwargs)
            return

        _actionFunc(self, eventActionSrc, *eventArgs, **eventKwargs)
        self.sendUpdateTasksToClient()

    def _eventActionFnstalk(self, _, *args, **kwargs):
        # 与npc交谈是任务目标
        LOG_INFO('in _eventActionFnstalk:', kwargs)
        if len(args) > 0:
            _taskId = int(args[0])
        else:
            _taskId = kwargs['_srcTaskId']
        npcId = kwargs['_npcId']
        dialogId = kwargs['_dialogId']

        self.taskInfo.onTaskStepUpdate(self, gameconst.TaskTargetEnum.TASK_TARGET_TALK_NPC, _taskId,
                                                (npcId, dialogId))

    def _eventActionFnstask(self, _, *args, **kwargs):
        if len(args) > 0:
            _taskId = int(args[0])
        else:
            _taskId = kwargs['_srcTaskId']
        if not self.taskInfo.checkSubmitBaseCond(self, _taskId):
            LOG_WARN('in _eventActionFnstask, Fnstask evt, task items not enough')
            return
        self.startSubmitTask(_taskId)

    def _eventActionFailtask(self, eventActionSrc, *args, **kwargs):
        if len(args) > 0:
            _taskId = int(args[0])
        else:
            _taskId = kwargs['_srcTaskId']
        self.startTaskFailed(_taskId, gameconst.TaskNotSuccReasonEnum.FAIL_ACTION)

    def _eventActionTaskRepeat(self, eventActionSrc, *args, **kwargs):
        _taskId = int(args[0])
        _errMsgId = 0 if len(args) <= 1 else int(args[1])
        taskCtx = actionContext.ClaimTaskCtx(extra={"errMsgId": _errMsgId})
        self.cell.doStartClaimTask(_taskId, '', (), taskCtx)
        return

    def _eventActionSetVariableNoCharProp(self, eventActionSrc, varId, fmlId, paramsStr, *args, **kwargs):
        LOG_INFO('_eventActionSetVariableNoCharProp:', eventActionSrc, varId, fmlId, paramsStr, args, kwargs)
        opUUID = KBEngine.genUUID64()
        self._innerSetVariable(gameconst.VarChangeSrcEnum.VAR_SRC_COMM_ACTION, varId, fmlId, paramsStr, opUUID, '')
        return

    def _eventActionTemporarySkill(self, eventActionSrc, *args, **kwargs):
        LOG_INFO('_eventActionTemporarySkill:', eventActionSrc, args, kwargs)

        _taskId = kwargs['_srcTaskId']
        school = self.getRoleCacheAttr('school')
        skillList =  kwargs[str(school)]
        self.unlockTemporarySkillByTask(_taskId, skillList)

class TaskProgress(object):
    def onTaskLeaveSpace(self, spaceNo):
        # 离开副本，任务可能失败
        dungeonNo = formula.parseDungeonNoBySpaceNo(spaceNo)
        taskIds = TLDD.datas.get(str(dungeonNo))
        if not taskIds:
            return
        LOG_INFO('in onTaskLeaveSpace:', spaceNo)
        for _taskId in taskIds:
            self.taskInfo.doTaskLeaveDungeon(self, _taskId)
        self.sendUpdateTasksToClient()

    def _offlineInTask(self):
        self.onTaskLeaveSpace(self.baseSpaceNo)

    def onTaskAvatarLvUp(self, oldLv, newLv):
        # 角色升级，更新相应任务进度
        self.taskInfo.onTaskStepUpdate(self, gameconst.TaskTargetEnum.TASK_TARGET_LEVEL, None, (newLv,))
        self.sendUpdateTasksToClient()
        # 角色升级，可能触发领取新任务
        for _ in range(oldLv + 1, newLv + 1):
            taskList = TACMLD.datas.get(str(newLv), [])
            if taskList:
                self.triggerAutoClaimTask(taskList)

    def taskCheckCounterTarget(self, counterTargetId, params=()):
        taskIds = TCTD.datas.get(str(counterTargetId))
        if not taskIds:
            return
        for _taskId in taskIds:
            self.taskInfo.onTaskStepUpdate(self, gameconst.TaskTargetEnum.TASK_TARGET_COUNTER, _taskId,
                                           (counterTargetId, params))
        self.sendUpdateTasksToClient()

    def onTaskStepUpdate(self, taskType, taskId, args):
        LOG_DBG("onTaskStepUpdate", taskType, taskId, args)
        

        
        if type(args) not in (tuple, list):
            args = (args,)
        if taskType == gameconst.TaskTargetEnum.TASK_TARGET_ITEMS:
            itemIdList = args[0]
            # 物品数量有变化，更新对应任务进度；任务目标不共享；
            for itemId in itemIdList:
                taskIds = TID.datas.get(str(itemId))
                if not taskIds:
                    continue
                self.taskInfo.onTaskStepUpdate(self, taskType, taskIds, (itemId,))
                self.triggerAutoClaimTask(TACCID.datas.get(str(itemId), []))
        elif taskType == gameconst.TaskTargetEnum.TASK_TARGET_COLLECT:
            # 采集完成，更新对应任务进度
            # 采集作为 物品搜集任务目标 的来源
            collectId, gameEntityId, spaceNo = args
            self.taskInfo.doAddTgtItemByRelateAction(self, collectId, gameEntityId)
            # 采集是组队任务目标；任务目标可以共享
            taskIds = TCD.datas.get(str(collectId))
            if not taskIds:
                return
            self.taskInfo.onTaskStepUpdate(self, taskType, taskIds, args)
        elif taskType == gameconst.TaskTargetEnum.TASK_TARGET_MONSTERS:
            _, monsterId, _ = args
            self.taskInfo.doAddTgtItemByRelateAction(self, monsterId, 0)
            taskIds = TMD.datas.get(str(monsterId))
            if not taskIds:
                return
            for taskId in taskIds:
                self.taskInfo.onTaskStepUpdate(self, taskType, taskId, args)
        else:
            self.taskInfo.onTaskStepUpdate(self, taskType, taskId, args)
        self.sendUpdateTasksToClient()


class ImpTask(TaskProgress, TaskEvent):
    def __init__(self):
        super(ImpTask, self).__init__()
        self.setTempMiscProp(gameconst.EntityPropsEnum.reqSubmitTaskList, {})

    def fixTaskTargetInfo(self):
        for taskId, task in self.taskInfo.tasks.items():
            if not task.isStat(gameconst.TaskStatEnum.TASK_STAT_RUNNING):
                continue
            taskData = dataUtils.getTaskCfg(taskId)
            hasGatherItems = dataUtils.getTaskFieldVal(taskData, 'FinCondHasGatherItems')
            if not hasGatherItems:
                continue
            tgtList = task.getTgtsByType(gameconst.TaskTargetEnum.TASK_TARGET_ITEMS)
            tgtItems = dataUtils.getTaskFieldVal(taskData, 'FinCondGatherItems')
            tmpData = {}
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
                tmpData[itemId] = {"srcIdList": srcIdList, "srcRatio": srcRatio}

            for tgt in tgtList:
                if tgt.stepCnt >= tgt.dstCnt:
                    continue
                srcInfo = tmpData.get(tgt.tgtId, {})
                srcIdList = srcInfo.get("srcIdList", [])
                srcRatio = srcInfo.get("srcRatio", 0)
                tgt.srcIdList = [int(srcId) for srcId in srcIdList]
                tgt.srcRatio = int(100 * srcRatio)
                tgt.state = 0

    @gamedecorator.checkGameconfigEnable('task')
    def reqSubmitTask(self, exposed, taskIds):
        # 提交任务
        popRewardUUID = KBEngine.genUUID64()
        taskIdSet = set()
        LOG_INFO('in reqSubmitTask1:', taskIds)
        for taskId in taskIds:
            if self.startSubmitTask(taskId, popRewardUUID):
                taskIdSet.add(taskId)
        if len(taskIdSet):
            taskIdsDicts = self.getTempMiscProp(gameconst.EntityPropsEnum.reqSubmitTaskList, {})
            taskIdsInfo = taskIdsDicts.setdefault(popRewardUUID, [taskIdSet, list(taskIdSet)])
            LOG_INFO('in reqSubmitTask2:', popRewardUUID, taskIdsInfo)
        return

    @gamedecorator.checkGameconfigEnable('task')
    def reqDeductTaskTargetItems(self, exposed, taskId):
        LOG_INFO('in reqDeductTaskTargetItems:', taskId)
        if self.taskInfo.deductTaskTgtItems(self, taskId):
            self.sendUpdateTasksToClient()

    def initNoviceHookRewardTask(self):
        self.taskInfo.initNoviceHookRewardTask()

    @gamedecorator.checkGameconfigEnable('task')
    def reqQuitTask(self, exposed, taskId):
        LOG_INFO('in reqQuitTask:', taskId)
        if not self.taskInfo.canQuitTaskManual(taskId):
            LOG_WARN('   in reqQuitTask, cant quit taskId:', taskId)
            return
        self.startQuitTask(taskId, gameconst.TaskNotSuccReasonEnum.MANUAL_QUIT)

    def getTaskObj(self, taskId):
        return self.taskInfo.getTaskObj(taskId)

    def isTaskComplete(self, taskId, cbBox=None, cbFn='', cbArgs=None):
        _isComplete = self.taskInfo.isTaskComplete(taskId)
        if cbBox:
            getattr(cbBox, cbFn, utils.Swallower())(_isComplete, *cbArgs)

        return _isComplete

    def getTaskCurrentState(self, taskId, cbBox=None, cbFn='', cbArgs=None):
        _state = self.taskInfo.getTaskCurrentState(taskId)
        if cbBox:
            getattr(cbBox, cbFn, utils.Swallower())(_state, *cbArgs)

        return _state

    def sendTaskList(self):
        _dic = self.taskInfo.toTaskInfoClientDict()
        jsonStr = json.dumps(_dic).encode('ascii')
        _zStr = gzip.compress(jsonStr)
        self.streamStringProxy(_zStr, '', gameconst.StreamStringID.TASK_LIST_DATA)
        self.taskInfo.resetUpdatedTaskList()
        self.taskInfo.sendHookRewardTaskList(self)

    def taskOnLogin(self):
        try:
            # self.taskInfo.dealEndTasks()
            self.taskInfo.checkExpiredTaskOnLogin(self)
            self.taskInfo.initTaskCacheOnLogin(self)
            self.taskInfo.checkRewardTaskCacheOnLogin(self)
            self.startTaskTimer()
            self.autoQuitTask()
            self.fixTaskTargetInfo()
            self.taskInfo.sendHookRewardTaskList(self)
        except Exception as e:
            gameengine.panicStack('in taskOnLogin exception:', e)
            return

    def taskTick(self):
        self.taskInfo.doUpdateTaskTimeout(self, 1)

    def startTaskTimer(self):
        self.pyAddTimer(1, 1, gametimer.TASK_UPDATE_TIMER)

    def onTaskDailyUpdate(self, *args):
        LOG_INFO('onTaskDailyUpdate:', args)
        myLevel = self.getAvatarLevel()
        removeTaskIds = self.taskInfo.doTaskDailyUpdate(self, myLevel)
        self.client.onTasksRem(removeTaskIds)
        self.sendUpdateTasksToClient()
        self.taskInfo.sendHookRewardTaskList(self)

    def onTaskWeeklyUpdate(self, *args):
        LOG_INFO('onTaskWeeklyUpdate:', args)
        myLevel = self.getAvatarLevel()
        removeTaskIds = self.taskInfo.doTaskWeeklyUpdate(self, myLevel)
        self.client.onTasksRem(removeTaskIds)
        self.sendUpdateTasksToClient()
        self.taskInfo.sendHookRewardTaskList(self)

    def sendUpdateTasksToClient(self):
        self.taskInfo.doSendUpdateTasksToClient(self)

    def onCheckSingleTaskCellCondSucc(self, taskId, taskCtx):
        # 对于单人任务，base领取任务的条件还没有检查
        self.baseTaskClaim(taskId, taskCtx)
        return

    def baseTaskClaim(self, taskId, taskCtx=None, needCheck=True):
        if not taskCtx:
            taskCtx = actionContext.ClaimTaskCtx()
        if gameengine.checkForbiddenTaskId(taskId):
            LOG_WARN('baseTaskClaim, task is forbidden !!! ', taskId)
            checkResult = gameclass.TaskCondResultCls(False)
            self.cell.onClaimTaskFailed(taskId, taskCtx, checkResult.msgId, checkResult.msgArgs)
            return
        if needCheck:
            checkResult = self.taskInfo.canClaimTask(self, taskId)
            if not checkResult:
                self.cell.onClaimTaskFailed(taskId, taskCtx, checkResult.msgId, checkResult.msgArgs)
                return
        _addTaskIds = self.taskInfo.doClaimTask(self, taskId, taskCtx)
        self.sendUpdateTasksToClient()

        if taskCtx.callbackUUID:
            self.cell.claimTaskSuccCallback(taskId, taskCtx.callbackUUID)

        return _addTaskIds

    def shouldSyncTaskData(self, taskId):
        return dataUtils.isTeamTask(taskId)

    def remTaskItems(self, taskId, opUUID, srcType):
        # 目前任务道具最多发放3个
        # ClaimRewardItems
        taskData = dataUtils.getTaskCfg(taskId)
        bindType = dataUtils.getItemDefaultBindType()
        rmTaskItemDic = {}
        if dataUtils.getTaskFieldVal(taskData, 'ClaimCanRewardITems'):
            for rewardItems in dataUtils.getTaskFieldVal(taskData, 'ClaimRewardItems'):
                itemId = rewardItems['ItemId']
                if itemId not in rmTaskItemDic:
                    rmTaskItemDic[itemId] = {}
                itemInfo = rmTaskItemDic[itemId]
                itemInfo[bindType] = itemInfo.get(bindType, 0) + rewardItems['Count']
        
        detail = gameclass.AwardDetailCls(taskId=taskId)
        opStat, _ = self.bagData.deductItemsWithPlan(self, rmTaskItemDic, None, opUUID, srcType, detail, None, True)
        if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
            LOG_WARN('rem task items err:', rmTaskItemDic)

    def abandonTaskItems(self, taskId, opUUID, srcType):
        taskData = dataUtils.getTaskCfg(taskId)
        if not dataUtils.getTaskFieldVal(taskData, 'AbanCanRemoveItems'):
            return
        abanRemoveItemIds = dataUtils.getTaskFieldVal(taskData, 'AbanRemoveItems')
        if not abanRemoveItemIds:
            return
        abandonedItems = {}
        for abanRemoveItemId in abanRemoveItemIds:
            itemDataCfg = ITEM_DATA.datas.get(abanRemoveItemId)
            if not itemDataCfg \
                or itemDataCfg['type'] != gameconst.ItemType.Normal \
                or itemDataCfg['subType'] != gameconst.ItemSubType.TASK:
                LOG_WARN('abandonTaskItems, rem task items err, wrong item cfg:', abanRemoveItemId)
                continue

            ret = self.bagData.getGridIdsByItemId(abanRemoveItemId)
            if ret:
                gridIds = abandonedItems.get(abanRemoveItemId)
                if not gridIds:
                    gridIds = []
                    abandonedItems[abanRemoveItemId] = gridIds
                gridIds.extend(ret)

        if not abandonedItems:
            return
        detail = gameclass.AwardDetailCls(taskId=taskId)
        for itemId, gridIds in abandonedItems.items():
            LOG_DBG('abandonTaskItems, rem task items:', itemId, gridIds, opUUID, srcType, detail)
            for gridId in gridIds:
                self.bagData.cleanGridByGridId(self, gridId, itemId, opUUID, srcType, detail)

    @gamedecorator.checkGameconfigEnable('task')
    def reqDropTaskItem(self, exposed, gridId, itemId):
        gridObj = self.taskBagData.getItemObjByGridId(gridId)
        if not gridObj or gridObj.itemId != itemId:
            gameengine.panicStack('in reqDropTaskItem, no task item:', gridId)
            return
        # 直接放弃任务，不需要做条件检查，任务放弃后会清理任务物品
        self.doTaskQuitNoCond(gridObj.uniqueId, gameconst.TaskNotSuccReasonEnum.DROP_TASK_ITEMS)

    def onTaskStateChanged(self, taskId, taskState):
        # 任务状态可能是其他任务的目标
        self.taskInfo.doRelateTaskReachStat(self, taskId, taskState)
        # 任务状态改变可能触发任务领取
        _claimTaskList = TACRTD.datas.get(str(taskId), {}).get(str(taskState), [])
        if _claimTaskList:
            self.triggerAutoClaimTask(_claimTaskList)

    # 自动领取任务
    def triggerAutoClaimTask(self, taskList):
        if not taskList:
            return
        for taskId in taskList:
            taskData = dataUtils.getTaskCfg(taskId)
            if not dataUtils.getTaskFieldVal(taskData, 'ClaimCondAutoTake'):
                continue
            if dataUtils.getTaskFieldVal(taskData, 'FatherTaskId') != 0:
                continue
            if not self.taskInfo.canClaimTask(self, taskId):
                continue
            self.cell.doStartClaimTask(taskId, '', (), None)

    def _offlineInTask(self):
        self.onTaskLeaveSpace(self.baseSpaceNo)

    def taskLeaveTeam(self):
        # 角色离开队伍，对应任务可能会直接失败
        self.taskInfo.doLeaveTeam(self)
        self.sendUpdateTasksToClient()

    def onTaskLeaveSpace(self, spaceNo):
        # 离开副本，任务可能失败
        dungeonNo = formula.parseDungeonNoBySpaceNo(spaceNo)
        taskIds = TLDD.datas.get(str(dungeonNo))
        if not taskIds:
            return
        LOG_INFO('in onTaskLeaveSpace:', spaceNo)
        for taskId in taskIds:
            self.taskInfo.doTaskLeaveDungeon(self, taskId)
        self.sendUpdateTasksToClient()
    # ------------------- 其他更新任务进度或状态的接口 -------------------------------------------------
    @gamedecorator.checkGameconfigEnable('task')
    def reqCompleteTaskNoTarget(self, exposed, taskId):
        LOG_INFO('in reqCompleteTaskNoTarget:', taskId)
        self.doCompleteTaskNoTarget(taskId)

    def doCompleteTaskNoTarget(self, taskId):
        self.taskInfo.completeTaskNoTarget(self, taskId)
        return

    @gamedecorator.checkGameconfigEnable('task')
    def reqTaskCompleteTarget(self, exposed, taskId, tgtType, tgtId):
        # 客户端检测的任务目标完成接口；目前有两种任务目标：完成一个行为(目前只有使用技能行为)目标 和 完成播放剧情任务目标
        # 完成播放剧情任务目标 已经废弃
        LOG_INFO('in reqTaskCompleteTarget:', taskId, tgtType, tgtId)
        if tgtType == gameconst.TaskTargetEnum.TASK_TARGET_ACTION:
            task = self.getTaskObj(taskId)
            if not task:
                LOG_WARN('in reqTaskCompleteTarget, not task:', taskId, tgtType, tgtId)
                return
            if task.isInEndStat():
                LOG_WARN('in reqTaskCompleteTarget, task in end state:', taskId, tgtType, tgtId)
                return
            tgtList = task.getTgtsByType(tgtType)
            if not tgtList:
                LOG_WARN('in reqTaskCompleteTarget, no this target:', taskId, tgtType, tgtId, tgtList)
                return

            self.cell.checkTaskCompleteActionTarget(taskId, tgtType, tgtId)
        else:
            gameengine.panicStack('in reqTaskCompleteTarget, param error:', taskId, tgtType, tgtId)

    def onCheckTaskCompleteActionTargetCallback(self, result, taskId, tgtType, tgtId):
        if not result:
            LOG_ERR('onCheckTaskCompleteActionTargetCallback, check failed:', result, taskId, tgtType, tgtId)
            return
        self.taskInfo.completeTargetAction(self, taskId, tgtId)

    def forceCompleteTaskNoCond(self, taskId):
        # 强制完成并提交任务，不做任何校验; 对于没有目标的任务，调用 doCompleteTaskNoTarget
        LOG_INFO('in forceCompleteTaskNoCond:', taskId)
        self._doCompleteTaskTarget(taskId)
        return

    def gmResetTask(self, taskId):
        # 非gm指令不要调用该接口
        self.taskInfo.taskRecordDic.pop(taskId, None)
        _task = self.getTaskObj(taskId)
        if not _task:
            return
        rootTaskId = _task.rootTaskId
        self.taskInfo.remChildTask(_task.rootTaskId)
        self.taskInfo.remTask(rootTaskId)
        self.sendTaskList()

    def gmSetTaskState(self, taskId, state, childState):
        LOG_INFO('gmSetTaskState', taskId, state)
        _task = self.getTaskObj(taskId)
        if not _task:
            return

        rootTaskId = _task.rootTaskId
        if taskId == rootTaskId and childState:
            for childTaskId in self.taskInfo.getChildTaskIds(taskId):
                childTask = self.getTaskObj(childTaskId)
                if childTask:
                    childTask.setStat(self, childState)

        _task.setStat(self, state)

    def _doCompleteTaskTarget(self, taskId):
        LOG_INFO('     in _doCompleteTaskTarget:', taskId)
        if self.taskInfo.forceCompleteTask(self, taskId):
            self.taskInfo.doTaskSubmit(self, taskId)
        self.sendUpdateTasksToClient()

    def startSubmitTask(self, taskId, popRewardUUID=0):
        LOG_INFO('in startSubmitTask:', taskId, popRewardUUID)
        # 提交任务的入口
        LOG_INFO('in doStartSubmitTask:', taskId, popRewardUUID)
        if gameengine.checkForbiddenTaskId(taskId):
            LOG_WARN('doStartSubmitTask, task is forbidden!!! ', taskId)
            return False
        task = self.getTaskObj(taskId)
        if not task or task.isStat(gameconst.TaskStatEnum.TASK_STAT_SUBMITTED):
            LOG_WARN('doStartSubmitTask, no task or already submit:', taskId)
            return False
        # taskList = self.taskInfo.relateSubmitTaskList(taskId)
        if not self.shouldSyncTaskData(taskId) or dataUtils.isSingleSupportTeamTask(taskId):
            self.cell.cellCheckTaskSubmitCond(taskId, popRewardUUID)
            return True
        return False

    def submitTaskCheckCB(self, taskId, teamType):
        LOG_INFO('in submitTaskCheckCB 1:', taskId, teamType)
        if teamType != gameconst.TeamType.DEFAULT:
            LOG_INFO('in submitTaskCheckCB 2:', taskId, teamType)
            self.client.onSubmitCheckResult(taskId, teamType)
            return
        task = self.getTaskObj(taskId)
        self.taskInfo.doTaskFinished(self, task)

    def onCheckCellSubmitCondSucc(self, taskId, isCaptain, popRewardUUID):
        LOG_INFO('in onCheckCellSubmitCondSucc, taskId:', taskId, isCaptain, popRewardUUID)
        self._baseTaskSubmit(taskId, popRewardUUID)
        if popRewardUUID:
            taskIdsDicts = self.getTempMiscProp(gameconst.EntityPropsEnum.reqSubmitTaskList, {})
            taskIdsInfo = taskIdsDicts.get(popRewardUUID, [{taskId}, [taskId]])
            LOG_INFO('in onCheckCellSubmitCondSucc, taskId:', taskId, popRewardUUID, taskIdsInfo)
            taskIdsInfo[0].discard(taskId)
            if not len(taskIdsInfo[0]):
                taskData = dataUtils.getTaskCfg(taskId)
                self._showPopReward(AAC_AACDD.datas.BONUS_SRC_COMPLETE_TASK, popRewardUUID, gameclass.AwardDetailCls(taskId=taskIdsInfo[1]))
                taskIdsDicts.pop(popRewardUUID, {})
        return

    def _baseTaskSubmit(self, taskId, popRewardUUID=0, check=True):
        LOG_INFO('in _baseTaskSubmit, taskId:', taskId, popRewardUUID)
        if check and not self.taskInfo.checkSubmitBaseCond(self, taskId):
            return
        self.taskInfo.doTaskSubmit(self, taskId, popRewardUUID, check)
        self.sendUpdateTasksToClient()

        return True

    def startTaskFailed(self, taskId, reason=gameconst.TaskNotSuccReasonEnum.UNKNOWN):
        LOG_INFO('in startTaskFailed:', taskId, reason)
        if not self.shouldSyncTaskData(taskId)\
                or dataUtils.isSingleSupportTeamTask(taskId):
            # 单人任务以及单人支持的组队任务，不需要同步任务失败
            self.baseTaskFailed(taskId, reason)

    def baseTaskFailed(self, taskId, reason):
        LOG_INFO('in baseTaskFailed:', taskId)
        self.taskInfo.doTaskFailed(self, taskId, reason)
        self.sendUpdateTasksToClient()

    def autoQuitTask(self):
        # 登录时自动放弃任务
        reson = gameconst.TaskNotSuccReasonEnum.LOGIN_AUTO_QUIT
        for taskId, task in self.taskInfo.tasks.items():
            if task.isInEndStat():
                continue
            if task.parentTaskId != 0:
                continue
            taskData = dataUtils.getTaskCfg(taskId)
            needQuit = False
            if dataUtils.getTaskFieldVal(taskData, 'IsAutoQuit'):
                reson = gameconst.TaskNotSuccReasonEnum.LOGIN_AUTO_QUIT
                needQuit = True
            elif not dataUtils.isTaskInOpenTime(taskId):
                reson = gameconst.TaskNotSuccReasonEnum.GROUP_TIMEOUT_QUIT
                needQuit = True
            if needQuit:
                self.doTaskQuitNoCond(taskId, reson)

    def startQuitTask(self, taskId, reason=gameconst.TaskNotSuccReasonEnum.UNKNOWN):
        LOG_INFO('in startQuitTask:', taskId)
        # 放弃任务入口
        if not self.shouldSyncTaskData(taskId)\
                or dataUtils.isSingleSupportTeamTask(taskId):
            # 单人任务以及单人支持的组队任务，不需要同步任务放弃
            self.doTaskQuitNoCond(taskId, reason)

    def doTaskQuitNoCond(self, taskId, reason):
        # 任务必定放弃成功
        LOG_INFO('in doTaskQuitNoCond, taskId:', taskId, reason)
        result = self.taskInfo.doQuitTask(self, taskId, reason)
        self.sendUpdateTasksToClient()

        return result

    def doRefreshSingleTask(self, taskId):
        # 刷新单人任务
        actId = dataUtils.getTaskRelateActId(taskId)
        if actId:
            task = self.getTaskObj(taskId)
            if not task.isInEndStat():
                self.doTaskQuitNoCond(taskId, gameconst.TaskNotSuccReasonEnum.REFRESH)
        return self.baseTaskClaim(taskId, needCheck=False)

    def baseTaskClaimedFailed(self, taskCtx, taskId):
        LOG_INFO('baseTaskClaimedFailed:', taskId)
        if taskCtx.claimSrc == gameconst.ClaimTaskSrcEnum.TASK_SRC_REWARD_TASK:
            self.taskInfo.removeRewardTaskCache(taskId)

    def preEnterTaskTargetDungeonCond(self, taskId, dungeonNo):
        task = self.getTaskObj(taskId)
        if not task or task.isInEndStat():
            LOG_WARN('preEnterTaskTargetDungeonCond, no running task, client task data expired:', taskId, dungeonNo)
            return
        self.doPreEnterTaskTargetDungeonCond(taskId, dungeonNo, {})

    @gamedecorator.checkGameconfigEnable('task')
    def reqEnterTaskTargetDungeon(self, exposed, taskId, dungeonNo):
        LOG_INFO('reqEnterTaskTargetDungeon:', taskId, dungeonNo)
        if self.taskInfo.isTaskTryingEnterDungeon(dungeonNo):
            return

        self.preEnterTaskTargetDungeonCond(taskId, dungeonNo)

    def doPreEnterTaskTargetDungeonCond(self, taskId, dungeonNo, extra):
        task = self.getTaskObj(taskId)
        if not task:
            LOG_WARN('doPreEnterTaskTargetDungeonCond, no task, client task data expired:', taskId, dungeonNo)
            return
        taskData = dataUtils.getTaskCfg(taskId)
        for _tgt in task.getAllTargets():
            if _tgt.dungeonNo == dungeonNo:
                self.cell.cellEnterTaskTargetDungeon(taskId, dungeonNo, extra)
                break
            elif _tgt.tgtType == gameconst.TaskTargetEnum.TASK_TARGET_ACTION:
                self.cell.cellEnterTaskTargetDungeon(taskId, dungeonNo, extra)
                break
            elif _tgt.tgtType == gameconst.TaskTargetEnum.TASK_TARGET_TALK_NPC:
                for oneData in dataUtils.getTaskFieldVal(taskData, 'FinCondFinDialogs'):
                    if oneData['MapId'] == dungeonNo:
                        self.cell.cellEnterTaskTargetDungeon(taskId, dungeonNo, extra)
                    break
        else:
            LOG_WARN('preEnterTaskTargetDungeonCond, no task target dungeon:', taskId, dungeonNo)

    def taskSetVar(self, taskId, opUUID, varSrc, varId, fmlId, paramsStr):
        desc = 'taskSetVar taskId:{}'.format(taskId)
        self._innerSetVariable(varSrc, varId, fmlId, paramsStr, opUUID, desc)

    def _innerSetVariable(self, varSrc, varId, fmlId, paramsStr, opUUID, desc):
        if not varId or not fmlId:
            return
        LOG_INFO('_innerSetVariable:', varSrc, varId, fmlId, paramsStr)
        varId = int(varId)
        fmlId = int(fmlId)
        _paramsStr = paramsStr.strip(' ')
        paramVarIdList = [int(paramValId) for paramValId in _paramsStr.split('|')] if _paramsStr else []

        if dataUtils.isRelateCharPropVar(varId):
            LOG_WARN('_innerSetVariable, can not set charprop variable')
            return

        if dataUtils.isAvatarVar(varId):
            _paramVarList = [self.getVariable(paramVarId) for paramVarId in paramVarIdList]
            newVal = utils.calcFormulaValue(fmlId, _paramVarList)
            self.setAvatarVariable(varId, newVal, opUUID, varSrc, desc)
        elif dataUtils.isSpaceVar(varId):
            # 设置spacevar
            avatarVarDict = {}
            for paramVarId in paramVarIdList:
                if dataUtils.isAvatarVar(paramVarId):
                    avatarVarDict[paramVarId] = self.getVariable(paramVarId)

    def onTaskVarChanged(self, taskId, varId):
        self.taskInfo.doTaskVariableChanged(self, taskId, varId)
        self.sendUpdateTasksToClient()

    def setBaseSpaceNo(self, spaceNo):
        LOG_INFO('setBaseSpaceNo {} ==> {}'.format(self.baseSpaceNo, spaceNo))
        self.baseSpaceNo = spaceNo
        self.taskInfo.taskSpaceNoChanged(spaceNo)

    def gmClaimTaskRec(self, taskId):
        _taskData = dataUtils.getTaskCfg(taskId)
        _parentId = dataUtils.getTaskFieldVal(_taskData, 'FatherTaskId')
        if _parentId:
            self.gmClaimTaskRec(_parentId)

        _task = self.taskInfo.getTaskObj(taskId)
        if not _task:
            self.baseTaskClaim(
                taskId,
                actionContext.ClaimTaskCtx(
                    claimSrc=gameconst.ClaimTaskSrcEnum.TASK_SRC_GM),
                needCheck=False)

    def gmForceSubmitTask(self, taskId):
        # 非gm指令不要调用该接口
        if str(taskId) not in TDD.datas:
            LOG_WARN('gmForceSubmitTask, no task data:', taskId)
            return

        task = self.taskInfo.getTaskObj(taskId)
        if not task:
            # 首先领取该任务
            self.gmClaimTaskRec(taskId)

        self.forceCompleteTaskNoCond(taskId)

    def afterTaskClaimed(self, taskId):
        return True, [(taskId, 1)]

    @gamedecorator.checkGameconfigEnable('task')
    def reqTaskEnterSpace(self, exposed, taskId):
        LOG_INFO('reqTaskEnterSpace:', taskId)
        task = self.taskInfo.getTaskObj(taskId)
        if not task:
            LOG_WARN('reqTaskEnterSpace, missing task, task id:', taskId)
            return
        if task.isInEndStat():
            LOG_WARN('reqTaskEnterSpace, task is end:', taskId)
            return
        self.taskInfo.taskEnterSpace(self, task)

    def onCheckSameMap(self, taskID, isSame):
        task = self.taskInfo.getTaskObj(taskID)
        if not task:
            LOG_WARN('onCheckSameMap, missing task, task id:', taskID)
            return
        self.taskInfo.onCheckSameTaskResult(self, task, isSame)

    def checkUnlockBountyTask(self):
        res = self._isUIVisible(V_VD.UIRewardTaskPanel)
        if not res:
            return

        self.taskInfo.refreshHookRewardTask(self.getAvatarLevel())
        self.taskInfo.sendHookRewardTaskList(self)

