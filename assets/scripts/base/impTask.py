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

import dropAward
import taskGetItems as TID
import taskCollect as TCD
import taskLeaveDungeon as TLDD
import taskCounter as TCTD
import taskAutoClaimRelatetask as TACRTD
import taskAutoClaimMinLevel as TACMLD
import taskAutoClaimCondItems as TACCID
import taskMonster as TMD
import taskdata as TDD
import taskDesc_taskChapter as TTCD
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

            _eventActionInfo = CommEventAction.CommEventActionDic.get(eventName)
            if not _eventActionInfo:
                continue
            _actionType, _actionFunc = _eventActionInfo
            _eventArgs, eventKwargs = utils.parseCommEventParams(eventParams)
            eventKwargs['_srcTaskId'] = taskId
            if _actionType == CommEventAction.CommEvEnum.BASE:
                _actionFunc(self, eventActionSrc, *_eventArgs, **eventKwargs)
            else:
                self.cell.doCellCommEvent(eventActionSrc, eventName, _eventArgs, eventKwargs)

    def doBaseCommEvent(self, eventActionSrc, eventName, eventArgs, eventKwargs):
        LOG_INFO('in doBaseCommEvent:', eventActionSrc, eventName, eventArgs, eventKwargs)
        _actionType, _actionFunc = CommEventAction.CommEventActionDic[eventName]
        if _actionType != CommEventAction.CommEvEnum.BASE:
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
            for _oneData in tgtItems:
                itemId = _oneData['ItemId']
                dstCnt = _oneData['Count']
                if itemId <= 0 or dstCnt <= 0:
                    continue
                srcIdList = []
                srcIdStr = _oneData.get("RelateMonster", '')
                if srcIdStr:
                    srcIdList.extend(srcIdStr.split('|'))
                srcIdStr = _oneData.get("RelateCollect", '')
                if srcIdStr:
                    srcIdList.extend(srcIdStr.split('|'))
                srcRatio = _oneData.get("Ratio", 0)
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
            self.triggerAutoClaimTask(dataUtils.getUnlockDayAutoClaimTaskIds(utils.getSvrOpenDays()))
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
        self.triggerAutoClaimTask(dataUtils.getUnlockDayAutoClaimTaskIds(utils.getSvrOpenDays()))

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
                or itemDataCfg['type'] != gameconst.ItemEnum.Normal \
                or itemDataCfg['subType'] != gameconst.ItemSubEnum.TASK:
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
        self.updateSpecialVisibleBySpace(self.baseSpaceNo)
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

    def _gmForceSubmitOneTask(self, taskId, claimSrc=gameconst.ClaimTaskSrcEnum.TASK_SRC_GM):
        # 只完成当前任务本身，不递归子任务。调用方按顺序逐个完成。
        task = self.taskInfo.getTaskObj(taskId)
        if task and task.isStat(gameconst.TaskStatEnum.TASK_STAT_SUBMITTED):
            return True
        if not task and self.taskInfo.taskRecordDic.get(taskId) == gameconst.TaskStatEnum.TASK_STAT_SUBMITTED:
            return True
        if not task:
            self.baseTaskClaim(
                taskId,
                actionContext.ClaimTaskCtx(claimSrc=claimSrc),
                needCheck=False)
            task = self.taskInfo.getTaskObj(taskId)
            if not task:
                LOG_WARN('_gmForceSubmitOneTask, claim failed:', taskId)
                return False
            if task.isStat(gameconst.TaskStatEnum.TASK_STAT_SUBMITTED):
                return True
        task.setAllTargetsReached(self)
        if not task.isStat(gameconst.TaskStatEnum.TASK_STAT_SUBMITTED):
            self.taskInfo.doTaskSubmit(self, taskId)
        return task.isStat(gameconst.TaskStatEnum.TASK_STAT_SUBMITTED)

    def _gmParseRelateTaskIds(self, taskData):
        raw = dataUtils.getTaskFieldVal(taskData, 'OpenCondRelateTaskId')
        if raw is None:
            return []
        text = str(raw).strip()
        if not text or text == '0':
            return []
        relateIds = []
        for part in text.split('|'):
            part = part.strip()
            if not part.isdigit():
                continue
            relateId = int(part)
            if relateId > 0:
                relateIds.append(relateId)
        return relateIds

    def _collectGmTaskLine(self, taskId):
        # 从目标任务倒着收集：父任务、开启关联任务、子任务，直到没有更早的任务。
        # 再补上这些任务带出的解锁任务（日常任务，且开启条件都落在这条链上）。
        if str(taskId) not in TDD.datas:
            LOG_WARN('gmForceSubmitTaskLine, no task data:', taskId)
            return None
        collected = set()
        stack = [taskId]
        while stack:
            curId = stack.pop()
            if curId in collected:
                continue
            if str(curId) not in TDD.datas:
                LOG_WARN('gmForceSubmitTaskLine, missing task:', taskId, curId)
                return None
            if len(collected) >= 300:
                LOG_WARN('gmForceSubmitTaskLine, task line too long:', taskId)
                return None
            collected.add(curId)
            taskData = dataUtils.getTaskCfg(curId)
            fatherId = dataUtils.getTaskFieldVal(taskData, 'FatherTaskId') or 0
            if fatherId:
                stack.append(int(fatherId))
            for relateId in self._gmParseRelateTaskIds(taskData):
                stack.append(relateId)
            for childId in dataUtils.getTaskFieldVal(taskData, 'ChildTaskIds') or []:
                stack.append(int(childId))

        extraStack = []
        for taskKey, taskData in TDD.datas.items():
            if dataUtils.getTaskFieldVal(taskData, 'TaskType') != gameconst.TaskType.TASK_TYPE_DAYLY:
                continue
            unlockId = int(taskKey)
            if unlockId in collected:
                continue
            relateIds = self._gmParseRelateTaskIds(taskData)
            if relateIds and all(relateId in collected for relateId in relateIds):
                extraStack.append(unlockId)
        while extraStack:
            curId = extraStack.pop()
            if curId in collected:
                continue
            if str(curId) not in TDD.datas:
                LOG_WARN('gmForceSubmitTaskLine, missing unlock task:', taskId, curId)
                return None
            if len(collected) >= 300:
                LOG_WARN('gmForceSubmitTaskLine, task line too long:', taskId)
                return None
            collected.add(curId)
            taskData = dataUtils.getTaskCfg(curId)
            fatherId = dataUtils.getTaskFieldVal(taskData, 'FatherTaskId') or 0
            if fatherId:
                extraStack.append(int(fatherId))
            for childId in dataUtils.getTaskFieldVal(taskData, 'ChildTaskIds') or []:
                extraStack.append(int(childId))
        for grantTaskId in self._collectDungeonGrantTasks(collected):
            if grantTaskId in collected:
                continue
            if len(collected) >= 300:
                LOG_WARN('gmForceSubmitTaskLine, task line too long:', taskId)
                return None
            collected.add(grantTaskId)
        return collected

    def _flowNodeNextIds(self, node):
        nextIds = []
        transition = node.get('transition') or {}
        for target in transition.values():
            if isinstance(target, (list, tuple)):
                nextIds.extend(str(nodeId) for nodeId in target)
            elif isinstance(target, dict):
                for inner in target.values():
                    if isinstance(inner, (list, tuple)):
                        nextIds.extend(str(nodeId) for nodeId in inner)
        return nextIds

    def _collectDungeonGrantTasks(self, collected):
        # 副本流程里，完成主线后才会接取的任务没有父任务和关联任务，主线链扫不到。
        # 自动战斗 86030032 就是新手副本完成 86060075 之后接取的。
        import tutorConst_newbieStep as TCNSD
        grantTaskIds = set()
        lockDuns = set()
        for stepData in TCNSD.datas.values():
            lockDun = int(stepData.get('lockDun') or 0)
            if lockDun > 0:
                lockDuns.add(lockDun)
        for dunNo in lockDuns:
            if not utils.checkDunFlowModuleDataExist(dunNo):
                continue
            flow = utils.getDunFLowModuleData(dunNo) or {}
            startNodes = set()
            for nodeId, node in flow.items():
                if not isinstance(node, dict) or node.get('type') != 'taskFinished':
                    continue
                if int(node.get('taskID') or 0) in collected:
                    startNodes.add(str(nodeId))
            seen = set()
            stack = list(startNodes)
            while stack:
                nodeId = stack.pop()
                if nodeId in seen or nodeId not in flow:
                    continue
                seen.add(nodeId)
                node = flow[nodeId]
                if not isinstance(node, dict):
                    continue
                nodeType = node.get('type')
                taskInNode = int(node.get('taskID') or 0)
                if nodeType == 'taskFinished' and nodeId not in startNodes and taskInNode not in collected:
                    continue
                if nodeType == 'taskUndertake' and taskInNode and str(taskInNode) in TDD.datas:
                    grantTaskIds.add(taskInNode)
                stack.extend(self._flowNodeNextIds(node))
        return grantTaskIds

    def _sortGmTaskLine(self, collected):
        # 先完成开启条件关联的任务和父任务，再完成依赖它们的任务。
        preds = {tid: set() for tid in collected}
        succs = {tid: set() for tid in collected}

        def addEdge(beforeId, afterId):
            if beforeId not in collected or afterId not in collected or beforeId == afterId:
                return
            if beforeId in preds[afterId]:
                return
            preds[afterId].add(beforeId)
            succs[beforeId].add(afterId)

        for tid in collected:
            taskData = dataUtils.getTaskCfg(tid)
            fatherId = dataUtils.getTaskFieldVal(taskData, 'FatherTaskId') or 0
            if fatherId:
                addEdge(int(fatherId), tid)
            for relateId in self._gmParseRelateTaskIds(taskData):
                addEdge(relateId, tid)

        ready = sorted([tid for tid, preSet in preds.items() if not preSet])
        ordered = []
        while ready:
            tid = ready.pop(0)
            ordered.append(tid)
            newly = []
            for nxt in succs[tid]:
                preds[nxt].discard(tid)
                if not preds[nxt]:
                    newly.append(nxt)
            if newly:
                ready.extend(newly)
                ready.sort()
        if len(ordered) != len(collected):
            LOG_WARN('gmForceSubmitTaskLine, task line cycle:', ordered)
            return None
        return ordered

    def gmForceSubmitTaskLine(self, taskId):
        # 非gm指令不要调用该接口。从最早的任务开始，完成目标任务之前的主线、子任务和解锁任务。
        collected = self._collectGmTaskLine(taskId)
        if not collected:
            return False, '执行失败, 任务ID错误或任务链异常'
        ordered = self._sortGmTaskLine(collected)
        if not ordered:
            return False, '执行失败, 任务链存在循环'
        LOG_INFO('gmForceSubmitTaskLine:', taskId, ordered)
        claimSrc = gameconst.ClaimTaskSrcEnum.TASK_SRC_GM_FINISH_NEWBIE
        for tid in ordered:
            if not self._gmForceSubmitOneTask(tid, claimSrc):
                return False, '执行失败, 任务完成失败:%s' % tid
        self.sendUpdateTasksToClient()
        return True, 'command success, tasks:' + ','.join([str(tid) for tid in ordered])

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

    @gamedecorator.checkGameconfigEnable('task')
    def reqSwitchPosition(self, exposed, taskId):
        # 数据辅助任务触发 SwitchPosition。坐标只读任务配置，不接受客户端上传。
        LOG_INFO('reqSwitchPosition:', taskId)
        task = self.taskInfo.getTaskObj(taskId)
        if not task:
            LOG_WARN('reqSwitchPosition, missing task:', taskId)
            return
        if task.isInEndStat():
            LOG_WARN('reqSwitchPosition, task is end:', taskId, task.stat)
            return
        taskData = dataUtils.getTaskCfg(taskId)
        if not taskData:
            return
        if taskData.get('DataAidedTaskClientEvent') != 'SwitchPosition':
            LOG_WARN('reqSwitchPosition, event mismatch:', taskId, taskData.get('DataAidedTaskClientEvent'))
            return
        stateStr = taskData.get('DataAidedTaskEventState') or ''
        if stateStr:
            if str(task.stat) not in stateStr.split('|'):
                LOG_WARN('reqSwitchPosition, state mismatch:', taskId, task.stat, stateStr)
                return
        elif task.stat != gameconst.TaskStatEnum.TASK_STAT_RUNNING:
            LOG_WARN('reqSwitchPosition, task not running:', taskId, task.stat)
            return
        paramStr = taskData.get('DataAidedTaskEventParam') or ''
        eventArgs, _ = utils.parseCommEventParams(paramStr)
        if len(eventArgs) < 4:
            LOG_WARN('reqSwitchPosition, bad param:', taskId, paramStr)
            return
        mapId = int(float(eventArgs[0]))
        dstX = float(eventArgs[1])
        dstY = float(eventArgs[2])
        dstZ = float(eventArgs[3])
        self.cell.startSwitchPosition(mapId, dstX, dstY, dstZ)

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

    def sendTaskChapterRewards(self):
        if not self.client:
            return
        self.client.onTaskChapterRewardRecord(self.claimedTaskChapterRewards)

    @gamedecorator.checkGameconfigEnable('task')
    def reqClaimTaskChapterReward(self, exposed, chapterId):
        # RewardTasks 已提交后，领取 ChapterReward
        LOG_INFO('reqClaimTaskChapterReward', self.gbID, chapterId)
        cfg = TTCD.datas.get(chapterId)
        if not cfg:
            LOG_WARN('reqClaimTaskChapterReward invalid chapter', self.gbID, chapterId)
            return
        rewardId = int(cfg.get('ChapterReward') or 0)
        if rewardId <= 0:
            LOG_WARN('reqClaimTaskChapterReward no reward', self.gbID, chapterId)
            return
        if chapterId in self.claimedTaskChapterRewards:
            LOG_WARN('reqClaimTaskChapterReward already claimed', self.gbID, chapterId)
            return
        taskId = int(cfg.get('RewardTasks') or 0)
        if taskId <= 0 or not self.taskInfo.isTaskComplete(taskId):
            LOG_WARN('reqClaimTaskChapterReward task not complete', self.gbID, chapterId, taskId)
            return

        srcType = AAC_AACDD.datas.BONUS_SRC_COMPLETE_TASK
        ctx = self.getAvatarAwardCtx(rewardId, None)
        wealthVal = dropAward.getAwardOne(rewardId, ctx)
        if wealthVal.isEmpty():
            LOG_WARN('reqClaimTaskChapterReward empty award', self.gbID, chapterId, rewardId)
            return
        if not self.canAddWealthVal(srcType, wealthVal, ctx, bMsg=True):
            LOG_WARN('reqClaimTaskChapterReward bag', self.gbID, chapterId, rewardId)
            return

        self.claimedTaskChapterRewards.append(chapterId)
        opUUID = KBEngine.genUUID64()
        detail = gameclass.AwardDetailCls(chapterId=chapterId)
        self.addWealth(srcType, wealthVal, opUUID, detail, ctx)
        if self.client:
            self.client.onClaimTaskChapterReward(chapterId)
        LOG_INFO('reqClaimTaskChapterReward ok', self.gbID, chapterId, rewardId, taskId)

