# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

import utils
import dataUtils
import gameglobal
import CommEventAction
import gameconst
import gameengine
import gametimer
import actionContext
import formula
import taskGetItems as TID
import taskCollect as TCD
import taskLeaveDungeon as TLDD
import taskCounter as TCTD
import json
import gzip
import taskAutoClaimRelatetask as TACRTD
import taskAutoClaimMinLevel as TACMLD
import taskAutoClaimCondItems as TACCID
import taskMonster as TMD
import gearEnhance_gearconst as GEGCD
import gearBase_gearConst as GBGCD
import value_value as VLVLD
import gamelog
import gameclass
import taskdata as TDD
import uiConfig_uiVisible as UC_UVD
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD


class TaskEvent(object):
    def doTaskEvent(self, eventActionSrc, taskId, eventStr, paramStr):
        if not eventStr:
            return
        DEBUG_MSG('in doTaskEvent, eventStr:', eventActionSrc, eventStr, paramStr)
        event_list = eventStr.split('|')
        param_list = paramStr.split('|')
        for eventName, eventParams in zip(event_list, param_list):
            if not eventName:
                continue

            eventActionInfo = CommEventAction.CommEventActionMap.get(eventName)
            if not eventActionInfo:
                continue
            actionType, actionFunc = eventActionInfo
            eventArgs, eventKwargs = utils.parseCommEventParams(eventParams)
            eventKwargs['_srcTaskId'] = taskId
            if actionType == CommEventAction.ActionType.BASE:
                actionFunc(self, eventActionSrc, *eventArgs, **eventKwargs)
            else:
                self.cell.doCellCommEvent(eventActionSrc, eventName, eventArgs, eventKwargs)
        return

    def doBaseCommEvent(self, eventActionSrc, eventName, eventArgs, eventKwargs):
        DEBUG_MSG('in doBaseCommEvent:', eventActionSrc, eventName, eventArgs, eventKwargs)
        actionType, actionFunc = CommEventAction.CommEventActionMap[eventName]
        if actionType != CommEventAction.ActionType.BASE:
            gameengine.reportCritical('doBaseCommEvent, actionType Error:', eventActionSrc, eventName, eventArgs,
                                      eventKwargs)
            return

        actionFunc(self, eventActionSrc, *eventArgs, **eventKwargs)
        self.sendUpdateTasksToClient()

    def _eventActionFnstalk(self, eventActionSrc, *args, **kwargs):
        # 与npc交谈是任务目标
        DEBUG_MSG('in _eventActionFnstalk:', kwargs)
        if len(args) > 0:
            taskId = int(args[0])
        else:
            taskId = kwargs['_srcTaskId']
        npcId = kwargs['_npcId']
        dialogId = kwargs['_dialogId']

        result = self.taskInfo.onTaskStepUpdate(self, gameconst.TaskTargetType.TASK_TARGET_TALK_NPC, taskId,
                                                (npcId, dialogId))

    def _eventActionFnstask(self, eventActionSrc, *args, **kwargs):
        if len(args) > 0:
            taskId = int(args[0])
        else:
            taskId = kwargs['_srcTaskId']
        if not self.taskInfo.checkSubmitBaseCond(self, taskId):
            WARNING_MSG('in _eventActionFnstask, Fnstask evt, task items not enough')
            return
        self.startSubmitTask(taskId)

    def _eventActionFailtask(self, eventActionSrc, *args, **kwargs):
        if len(args) > 0:
            taskId = int(args[0])
        else:
            taskId = kwargs['_srcTaskId']
        self.startTaskFailed(taskId, gameconst.TaskNotSuccReason.FAIL_ACTION)

    def _eventActionTaskRepeat(self, eventActionSrc, *args, **kwargs):
        taskId = int(args[0])
        errMsgId = 0 if len(args) <= 1 else int(args[1])
        taskCtx = actionContext.ClaimTaskCtx(extra={"errMsgId": errMsgId})
        self.cell.startClaimTask(taskId, '', (), taskCtx)
        return

    def _eventActionSetVariableNoCharProp(self, eventActionSrc, varId, fmlId, paramsStr, *args, **kwargs):
        DEBUG_MSG('_eventActionSetVariableNoCharProp:', eventActionSrc, varId, fmlId, paramsStr, args, kwargs)
        opUUID = KBEngine.genUUID64()
        self._innerSetVariable(gameconst.VarChangeSrc.VAR_SRC_COMM_ACTION, varId, fmlId, paramsStr, opUUID, '')
        return

    def _eventActionAddEquipWashAnima(self, eventActionSrc, addNum, *args, **kwargs):
        INFO_MSG('_eventActionAddEquipWashAnima:', addNum)
        gridID, itemObj = self.getAnimaItemObj()
        if gridID < 0 or not itemObj:
            equipAnimaGetExceptions = GBGCD.datas['equipAnimaGetExceptions']['value']
            self.onMessagePre(equipAnimaGetExceptions, [str(addNum)])
            return
        itemObj.addAnima(self, gridID, int(addNum))

class TaskProgress(object):
    def onTaskAvatarDie(self, spaceNo):
        # 角色死亡，对应任务可能会直接失败
        self.taskInfo.doAvatarDead(self)
        self.sendUpdateTasksToClient()

    def _offlineInTask(self):
        self.onTaskLeaveSpace(self.baseSpaceNo)

    def onTaskLeaveSpace(self, spaceNo):
        # 离开副本，任务可能失败
        dungeonNo = formula.getDungeonNoBySpaceNo(spaceNo)
        taskIds = TLDD.datas.get(str(dungeonNo))
        if not taskIds:
            return
        DEBUG_MSG('in onTaskLeaveSpace:', spaceNo)
        for taskId in taskIds:
            self.taskInfo.doTaskLeaveDungeon(self, taskId)
        self.sendUpdateTasksToClient()

    def onTaskAvatarLvUp(self, oldLv, newLv):
        # 角色升级，更新相应任务进度
        self.taskInfo.onTaskStepUpdate(self, gameconst.TaskTargetType.TASK_TARGET_LEVEL, None, (newLv,))
        self.sendUpdateTasksToClient()
        # 角色升级，可能触发领取新任务
        for lv in range(oldLv + 1, newLv + 1):
            taskList = TACMLD.datas.get(str(newLv), [])
            taskList and self.triggerAutoClaimTask(taskList)

    def taskCheckCounterTarget(self, counterTargetId, params=()):
        taskIds = TCTD.datas.get(str(counterTargetId))
        if not taskIds:
            return
        for taskId in taskIds:
            self.taskInfo.onTaskStepUpdate(self, gameconst.TaskTargetType.TASK_TARGET_COUNTER, taskId,
                                           (counterTargetId, params))
        self.sendUpdateTasksToClient()

    def onTaskStepUpdate(self, taskType, taskId, args):
        DEBUG_MSG("onTaskStepUpdate", taskType, taskId, args)
        if type(args) not in (tuple, list):
            args = (args,)
        if taskType == gameconst.TaskTargetType.TASK_TARGET_ITEMS:
            itemIdList = args[0]
            # 物品数量有变化，更新对应任务进度；任务目标不共享；
            for itemId in itemIdList:
                taskIds = TID.datas.get(str(itemId))
                if not taskIds:
                    continue
                self.taskInfo.onTaskStepUpdate(self, taskType, taskIds, (itemId,))
                self.triggerAutoClaimTask(TACCID.datas.get(str(itemId), []))
        elif taskType == gameconst.TaskTargetType.TASK_TARGET_COLLECT:
            # 采集完成，更新对应任务进度
            # 采集作为 物品搜集任务目标 的来源
            collectId, gameEntityId, spaceNo = args
            self.taskInfo.doAddTgtItemByRelateAction(self, collectId, gameEntityId)
            # 采集是组队任务目标；任务目标可以共享
            taskIds = TCD.datas.get(str(collectId))
            if not taskIds:
                return
            self.taskInfo.onTaskStepUpdate(self, taskType, taskIds, args)
        elif taskType == gameconst.TaskTargetType.TASK_TARGET_MONSTERS:
            monsterId = args[1]
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
        self.setTempMiscProp(gameconst.AvatarProps.reqSubmitTaskList, {})

    def fixTaskTargetInfo(self):
        for taskId, task in self.taskInfo.tasks.items():
            if not task.isStat(gameconst.TaskStat.TASK_STAT_RUNNING):
                continue
            taskData = dataUtils.getTaskData(taskId)
            hasGatherItems = dataUtils.taskFieldVal(taskData, 'FinCondHasGatherItems')
            if not hasGatherItems:
                continue
            tgtList = task.getTgtsByType(gameconst.TaskTargetType.TASK_TARGET_ITEMS)
            tgtItems = dataUtils.taskFieldVal(taskData, 'FinCondGatherItems')
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

    def reqSubmitTask(self, taskIds):
        # 提交任务
        popRewardUUID = KBEngine.genUUID64()
        taskIdSet = set()
        DEBUG_MSG('in reqSubmitTask1:', taskIds)
        for taskId in taskIds:
            if self.startSubmitTask(taskId, popRewardUUID):
                taskIdSet.add(taskId)
        if len(taskIdSet):
            taskIdsDicts = self.getTempMiscProp(gameconst.AvatarProps.reqSubmitTaskList, {})
            taskIdsInfo = taskIdsDicts.setdefault(popRewardUUID, [taskIdSet, list(taskIdSet)])
            DEBUG_MSG('in reqSubmitTask2:', popRewardUUID, taskIdsInfo)
        return

    def reqDeductTaskTargetItems(self, taskId):
        DEBUG_MSG('in reqDeductTaskTargetItems:', taskId)
        if self.taskInfo.deductTaskTgtItems(self, taskId):
            self.sendUpdateTasksToClient()

    def initNoviceHookRewardTask(self):
        self.taskInfo.initNoviceHookRewardTask()

    def reqQuitTask(self, taskId):
        DEBUG_MSG('in reqQuitTask:', taskId)
        if not self.taskInfo.canQuitTaskManual(taskId):
            WARNING_MSG('   in reqQuitTask, cant quit taskId:', taskId)
            return
        self.startQuitTask(taskId, gameconst.TaskNotSuccReason.MANUAL_QUIT)

    def getTask(self, taskId):
        return self.taskInfo.getTask(taskId)

    def isTaskComplete(self, taskId, cbBox=None, cbFn='', cbArgs=None):
        isComplete = self.taskInfo.isTaskComplete(taskId)
        if cbBox:
            getattr(cbBox, cbFn, utils.Swallower())(isComplete, *cbArgs)

        return isComplete

    def getTaskCurrentState(self, taskId, cbBox=None, cbFn='', cbArgs=None):
        state = self.taskInfo.getTaskCurrentState(taskId)
        if cbBox:
            getattr(cbBox, cbFn, utils.Swallower())(state, *cbArgs)

        return state

    def sendTaskList(self):
        dic = self.taskInfo.toTaskInfoClientDict()
        jsonStr = json.dumps(dic).encode('ascii')
        zStr = gzip.compress(jsonStr)
        self.streamStringProxy(zStr, '', gameconst.StreamStringID.TASK_LIST_DATA)
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
            gameengine.reportCritical('in taskOnLogin exception:', e)
            return

    def startTaskTimer(self):
        self.pyAddTimer(1, 1, gametimer.TASK_UPDATE_TIMER)

    def taskTick(self):
        self.taskInfo.doUpdateTaskTimeout(self, 1)

    def onTaskDailyUpdate(self, *args):
        DEBUG_MSG('onTaskDailyUpdate:', args)
        myLevel = self.getAvatarLevel()
        removeTaskIds = self.taskInfo.doTaskDailyUpdate(myLevel)
        self.client.onTasksRem(removeTaskIds)
        self.sendUpdateTasksToClient()
        self.taskInfo.sendHookRewardTaskList(self)

    def onTaskWeeklyUpdate(self, *args):
        DEBUG_MSG('onTaskWeeklyUpdate:', args)
        myLevel = self.getAvatarLevel()
        removeTaskIds = self.taskInfo.doTaskWeeklyUpdate(myLevel)
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
        if needCheck:
            checkResult = self.taskInfo.canClaimTask(self, taskId)
            if not checkResult:
                self.cell.claimTaskFailed(taskId, taskCtx, checkResult.msgId, checkResult.msgArgs)
                return
        addTaskIds = self.taskInfo.doClaimTask(self, taskId, taskCtx)
        self.sendUpdateTasksToClient()

        taskCtx.callbackUUID and self.cell.claimTaskSuccCallback(taskId, taskCtx.callbackUUID)

        return addTaskIds

    def shouldSyncTaskData(self, taskId):
        return dataUtils.isTeamTask(taskId)

    def addTaskItems(self, itemsList, srcType, opUUID, detail):
        if not itemsList:
            return True

        if self.taskBagData.isFull() or self.taskBagData.isLocked():
            gameengine.reportCritical('add task items err: databag full or locked')
            return False

        planOp, planDic, leftItems = self.taskBagData.calcAddItemsPlan(itemsList)
        if planOp != gameconst.BagOpPlan.BAG_OP_OK:
            gameengine.reportCritical('add task items err:', planOp)
            return False

        opStat, _ = self.taskBagData.addItemsWithPlan(self, itemsList, opUUID, srcType, detail, planDict=planDic)
        if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
            gameengine.reportCritical('add task items err:', self.id, planDic, len(itemsList))
            return False
        return True

    def remTaskItems(self, taskId, opUUID, srcType):
        # 目前任务道具最多发放3个
        # ClaimRewardItems
        taskData = dataUtils.getTaskData(taskId)

        bindType = dataUtils.getItemDefaultBindType()
        rmTaskItemDic = {}
        if dataUtils.taskFieldVal(taskData, 'ClaimCanRewardITems'):
            for rewardItems in dataUtils.taskFieldVal(taskData, 'ClaimRewardItems'):
                itemId = rewardItems['ItemId']
                if itemId not in rmTaskItemDic:
                    rmTaskItemDic[itemId] = {}
                itemInfo = rmTaskItemDic[itemId]
                itemInfo[bindType] = itemInfo.get(bindType, 0) + rewardItems['Count']
        detail = gameclass.AwardDetail(taskId=taskId)
        opStat, _ = self.bagData.deductItemsWithPlan(self, rmTaskItemDic, None, opUUID, srcType, detail, None, True)
        if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
            WARNING_MSG('rem task items err:', rmTaskItemDic)

    def reqDropTaskItem(self, gridId, itemId):
        gridObj = self.taskBagData.getItemObjByGridId(gridId)
        if not gridObj or gridObj.itemId != itemId:
            gameengine.reportCritical('in reqDropTaskItem, no task item:', gridId)
            return
        # 直接放弃任务，不需要做条件检查，任务放弃后会清理任务物品
        self.doTaskQuitNoCond(gridObj.uniqueId, gameconst.TaskNotSuccReason.DROP_TASK_ITEMS)

    def onTaskStateChanged(self, taskId, taskState):
        # 任务状态可能是其他任务的目标
        self.taskInfo.doRelateTaskReachStat(self, taskId, taskState)
        # 任务状态改变可能触发任务领取
        claimTaskList = TACRTD.datas.get(str(taskId), {}).get(str(taskState), [])
        claimTaskList and self.triggerAutoClaimTask(claimTaskList)
        return

    def taskFlowLog(self, taskId, logName, opUUID=None, reason='', claimSrc=None):
        task = self.getTask(taskId)
        if not task:
            return

        roleInfo = gameglobal.roleCache.get(self.id)
        if not roleInfo:
            return
        taskType = "unkown"
        if task.taskType == gameconst.TaskType.TASK_TYPE_MAINLINE:
            taskType = "mainline"
        elif task.taskType == gameconst.TaskType.TASK_TYPE_HOOK_REWARD:
            taskType = "hookReward"
        else:
            taskType = "subline"

        logDataDic = {}
        if logName == "TaskClaim":
            logDataDic = {
                "role_id": self.gbID,
                "role_name": self.getRoleCacheAttr('name', ''),
                "op_nuid": opUUID if opUUID else 0,
                "taskIds": taskId,
                "claim_source": claimSrc if claimSrc else taskType,
            }
        elif logName == "TaskSubmit":
            logDataDic = {
                "role_id": self.gbID,
                "role_name": self.getRoleCacheAttr('name', ''),
                "op_nuid": opUUID if opUUID else 0,
                "taskIds": taskId,
                "claim_source": taskType,
            }
        elif logName == "TaskQuit":
            logDataDic = {
                "role_id": self.gbID,
                "role_name": self.getRoleCacheAttr('name', ''),
                "op_nuid": opUUID if opUUID else 0,
                "taskIds": taskId,
                "reason": reason
            }
        gamelog.makeWLog(logName, logDataDic)

    # 自动领取任务
    def triggerAutoClaimTask(self, taskList):
        if not taskList:
            return
        for taskId in taskList:
            taskData = dataUtils.getTaskData(taskId)
            if not dataUtils.taskFieldVal(taskData, 'ClaimCondAutoTake'):
                continue
            if dataUtils.taskFieldVal(taskData, 'FatherTaskId') != 0:
                continue
            if not self.taskInfo.canClaimTask(self, taskId):
                continue
            self.cell.startClaimTask(taskId, '', (), None)
        return

    def onTaskAvatarDie(self, spaceNo):
        # 角色死亡，对应任务可能会直接失败
        self.taskInfo.doAvatarDead(self)
        self.sendUpdateTasksToClient()

    def taskLeaveTeam(self):
        # 角色离开队伍，对应任务可能会直接失败
        self.taskInfo.doLeaveTeam(self)
        self.sendUpdateTasksToClient()

    def _offlineInTask(self):
        self.onTaskLeaveSpace(self.baseSpaceNo)

    def onTaskLeaveSpace(self, spaceNo):
        # 离开副本，任务可能失败
        dungeonNo = formula.getDungeonNoBySpaceNo(spaceNo)
        taskIds = TLDD.datas.get(str(dungeonNo))
        if not taskIds:
            return
        DEBUG_MSG('in onTaskLeaveSpace:', spaceNo)
        for taskId in taskIds:
            self.taskInfo.doTaskLeaveDungeon(self, taskId)
        self.sendUpdateTasksToClient()
    # ------------------- 其他更新任务进度或状态的接口 -------------------------------------------------
    def reqCompleteTaskNoTarget(self, taskId):
        DEBUG_MSG('in reqCompleteTaskNoTarget:', taskId)
        self.doCompleteTaskNoTarget(taskId)

    def doCompleteTaskNoTarget(self, taskId):
        self.taskInfo.completeTaskNoTarget(self, taskId)
        return

    def reqTaskCompleteTarget(self, taskId, tgtType, tgtId):
        # 客户端检测的任务目标完成接口；目前有两种任务目标：完成一个行为(目前只有使用技能行为)目标 和 完成播放剧情任务目标
        # 完成播放剧情任务目标 已经废弃
        DEBUG_MSG('in reqTaskCompleteTarget:', taskId, tgtType, tgtId)
        if tgtType == gameconst.TaskTargetType.TASK_TARGET_ACTION:
            task = self.getTask(taskId)
            if not task:
                WARNING_MSG('in reqTaskCompleteTarget, not task:', taskId, tgtType, tgtId)
                return
            if task.isInEndStat():
                WARNING_MSG('in reqTaskCompleteTarget, task in end state:', taskId, tgtType, tgtId)
                return
            tgtList = task.getTgtsByType(tgtType)
            if not tgtList:
                WARNING_MSG('in reqTaskCompleteTarget, no this target:', taskId, tgtType, tgtId, tgtList)
                return

            self.cell.checkTaskCompleteActionTarget(taskId, tgtType, tgtId)
        else:
            gameengine.reportCritical('in reqTaskCompleteTarget, param error:', taskId, tgtType, tgtId)

    def onCheckTaskCompleteActionTargetCallback(self, result, taskId, tgtType, tgtId):
        if not result:
            ERROR_MSG('onCheckTaskCompleteActionTargetCallback, check failed:', result, taskId, tgtType, tgtId)
            return
        self.taskInfo.completeTargetAction(self, taskId, tgtId)

    def forceCompleteTaskNoCond(self, taskId):
        # 强制完成并提交任务，不做任何校验; 对于没有目标的任务，调用 doCompleteTaskNoTarget
        DEBUG_MSG('in forceCompleteTaskNoCond:', taskId)
        self._doCompleteTaskTarget(taskId)
        return

    def gmResetTask(self, taskId):
        # 非gm指令不要调用该接口
        self.taskInfo.taskRecordDic.pop(taskId, None)
        task = self.getTask(taskId)
        if not task:
            return
        rootTaskId = task.rootTaskId
        self.taskInfo.remChildTask(task.rootTaskId)
        self.taskInfo.remTask(rootTaskId)
        self.sendTaskList()

    def gmSetTaskState(self, taskId, state, childState):
        INFO_MSG('gmSetTaskState', taskId, state)
        task = self.getTask(taskId)
        if not task:
            return

        rootTaskId = task.rootTaskId
        if taskId == rootTaskId and childState:
            for childTaskId in self.taskInfo.getChildTaskIds(taskId):
                childTask = self.getTask(childTaskId)
                if childTask:
                    childTask.setStat(self, childState)

        task.setStat(self, state)

    def _doCompleteTaskTarget(self, taskId):
        DEBUG_MSG('     in _doCompleteTaskTarget:', taskId)
        if self.taskInfo.forceCompleteTask(self, taskId):
            self.taskInfo.doSubmitTask(self, taskId)
        self.sendUpdateTasksToClient()

    def startSubmitTask(self, taskId, popRewardUUID=0):
        # 提交任务的入口
        DEBUG_MSG('in startSubmitTask:', taskId, popRewardUUID)
        task = self.getTask(taskId)
        if not task or task.isStat(gameconst.TaskStat.TASK_STAT_SUBMITTED):
            WARNING_MSG('startSubmitTask, no task or already submit:', taskId)
            return False
        # taskList = self.taskInfo.relateSubmitTaskList(taskId)
        if not self.shouldSyncTaskData(taskId) or dataUtils.isSingleSupportTeamTask(taskId):
            self.cell.cellCheckTaskSubmitCond(taskId, popRewardUUID)
            return True
        return False

    def onCheckCellSubmitCondSucc(self, taskId, isCaptain, popRewardUUID):
        DEBUG_MSG('in onCheckCellSubmitCondSucc, taskId:', taskId, isCaptain, popRewardUUID)
        self._baseTaskSubmit(taskId, popRewardUUID)
        if popRewardUUID:
            taskIdsDicts = self.getTempMiscProp(gameconst.AvatarProps.reqSubmitTaskList, {})
            taskIdsInfo = taskIdsDicts.get(popRewardUUID, [{taskId}, [taskId]])
            DEBUG_MSG('in onCheckCellSubmitCondSucc, taskId:', taskId, popRewardUUID, taskIdsInfo)
            taskIdsInfo[0].discard(taskId)
            if not len(taskIdsInfo[0]):
                self._showPopReward(AAC_AACDD.datas.BONUS_SRC_COMPLETE_TASK, popRewardUUID, gameclass.AwardDetail(taskId=taskIdsInfo[1]))
                taskIdsDicts.pop(popRewardUUID, {})
        return

    def _baseTaskSubmit(self, taskId, popRewardUUID=0, check=True):
        DEBUG_MSG('in _baseTaskSubmit, taskId:', taskId, popRewardUUID)
        if check and not self.taskInfo.checkSubmitBaseCond(self, taskId):
            return
        self.taskInfo.doSubmitTask(self, taskId, popRewardUUID, check)
        self.sendUpdateTasksToClient()

        return True

    def startTaskFailed(self, taskId, reason=gameconst.TaskNotSuccReason.UNKNOWN):
        DEBUG_MSG('in startTaskFailed:', taskId, reason)
        if not self.shouldSyncTaskData(taskId) or dataUtils.isSingleSupportTeamTask(taskId):
            # 单人任务以及单人支持的组队任务，不需要同步任务失败
            self.baseTaskFailed(taskId, reason)

    def baseTaskFailed(self, taskId, reason):
        DEBUG_MSG('in baseTaskFailed:', taskId)
        self.taskInfo.doTaskFailed(self, taskId, reason)
        self.sendUpdateTasksToClient()

    def autoQuitTask(self):
        # 登录时自动放弃任务
        reson = gameconst.TaskNotSuccReason.LOGIN_AUTO_QUIT
        for taskId, task in self.taskInfo.tasks.items():
            if task.isInEndStat():
                continue
            if task.parentTaskId != 0:
                continue
            taskData = dataUtils.getTaskData(taskId)
            needQuit = False
            if dataUtils.taskFieldVal(taskData, 'IsAutoQuit'):
                reson = gameconst.TaskNotSuccReason.LOGIN_AUTO_QUIT
                needQuit = True
            elif not dataUtils.isTaskInOpenTime(taskId):
                reson = gameconst.TaskNotSuccReason.GROUP_TIMEOUT_QUIT
                needQuit = True
            if needQuit:
                self.doTaskQuitNoCond(taskId, reson)

    def startQuitTask(self, taskId, reason=gameconst.TaskNotSuccReason.UNKNOWN):
        DEBUG_MSG('in startQuitTask:', taskId)
        # 放弃任务入口
        if not self.shouldSyncTaskData(taskId) or dataUtils.isSingleSupportTeamTask(taskId):
            # 单人任务以及单人支持的组队任务，不需要同步任务放弃
            self.doTaskQuitNoCond(taskId, reason)
        return

    def doTaskQuitNoCond(self, taskId, reason):
        # 任务必定放弃成功
        DEBUG_MSG('in doTaskQuitNoCond, taskId:', taskId, reason)
        result = self.taskInfo.doQuitTask(self, taskId, reason)
        self.sendUpdateTasksToClient()

        return result

    def doRefreshSingleTask(self, taskId):
        # 刷新单人任务
        actId = dataUtils.getTaskRelateActId(taskId)
        if actId:
            task = self.getTask(taskId)
            if not task.isInEndStat():
                self.doTaskQuitNoCond(taskId, gameconst.TaskNotSuccReason.REFRESH)
        return self.baseTaskClaim(taskId, needCheck=False)

    def baseTaskClaimedFailed(self, taskCtx, taskId):
        INFO_MSG('baseTaskClaimedFailed:', taskId)
        if taskCtx.claimSrc == gameconst.ClaimTaskSrc.REWARD_TASK:
            self.taskInfo.removeRewardTaskCache(taskId)

    def reqEnterTaskTargetDungeon(self, taskId, dungeonNo):
        DEBUG_MSG('reqEnterTaskTargetDungeon:', taskId, dungeonNo)
        if self.taskInfo.isTaskTryingEnterDungeon(dungeonNo):
            return

        self.preEnterTaskTargetDungeonCond(taskId, dungeonNo)

    def preEnterTaskTargetDungeonCond(self, taskId, dungeonNo):
        task = self.getTask(taskId)
        if not task or task.isInEndStat():
            WARNING_MSG('preEnterTaskTargetDungeonCond, no running task, client task data expired:', taskId, dungeonNo)
            return
        self.doPreEnterTaskTargetDungeonCond(taskId, dungeonNo, {})

    def doPreEnterTaskTargetDungeonCond(self, taskId, dungeonNo, extra):
        task = self.getTask(taskId)
        if not task:
            WARNING_MSG('doPreEnterTaskTargetDungeonCond, no task, client task data expired:', taskId, dungeonNo)
            return
        taskData = dataUtils.getTaskData(taskId)
        for tgt in task.getAllTargets():
            if tgt.dungeonNo == dungeonNo:
                self.cell.cellEnterTaskTargetDungeon(taskId, dungeonNo, extra)
                break
            elif tgt.tgtType == gameconst.TaskTargetType.TASK_TARGET_ACTION:
                self.cell.cellEnterTaskTargetDungeon(taskId, dungeonNo, extra)
                break
            elif tgt.tgtType == gameconst.TaskTargetType.TASK_TARGET_TALK_NPC:
                for oneData in dataUtils.taskFieldVal(taskData, 'FinCondFinDialogs'):
                    if oneData['MapId'] == dungeonNo:
                        self.cell.cellEnterTaskTargetDungeon(taskId, dungeonNo, extra)
                    break
        else:
            WARNING_MSG('preEnterTaskTargetDungeonCond, no task target dungeon:', taskId, dungeonNo)
        return

    def checkTaskSetInteractState(self, state, interactId, taskId):
        task = self.getTask(taskId)
        if not task or task.isInEndStat():
            WARNING_MSG('checkTaskSetInteractState, no running task, client task data expired:', taskId)
            return
        self.cell.onCheckTaskSetInteractStateSucc(state, interactId, taskId)

    def taskSetVariable(self, taskId, opUUID, varSrc, varId, fmlId, paramsStr):
        desc = 'taskSetVariable taskId:{}'.format(taskId)
        self._innerSetVariable(varSrc, varId, fmlId, paramsStr, opUUID, desc)
        return

    def _innerSetVariable(self, varSrc, varId, fmlId, paramsStr, opUUID, desc):
        if not varId or not fmlId:
            return
        DEBUG_MSG('_innerSetVariable:', varSrc, varId, fmlId, paramsStr)
        varId = int(varId)
        fmlId = int(fmlId)
        paramsStr = paramsStr.strip(' ')
        paramVarIdList = [int(paramValId) for paramValId in paramsStr.split('|')] if paramsStr else []

        if dataUtils.isRelateCharPropVar(varId):
            WARNING_MSG('_innerSetVariable, can not set charprop variable')
            return

        if dataUtils.isAvatarVar(varId):
            paramVarList = [self.getVariable(paramVarId) for paramVarId in paramVarIdList]
            newVal = utils.calcFormulaValue(f'formula:{fmlId}', paramVarList)
            self.setAvatarVariable(varId, newVal, opUUID, varSrc, desc)
        elif dataUtils.isSpaceVar(varId):
            # 设置spacevar
            avatarVarDic = {}
            for paramVarId in paramVarIdList:
                if dataUtils.isAvatarVar(paramVarId):
                    avatarVarDic[paramVarId] = self.getVariable(paramVarId)

    def onTaskVarChanged(self, taskId, varId):
        self.taskInfo.doTaskVariableChanged(self, taskId, varId)
        self.sendUpdateTasksToClient()
        return

    def setBaseSpaceNo(self, spaceNo):
        INFO_MSG('setBaseSpaceNo {} ==> {}'.format(self.baseSpaceNo, spaceNo))
        self.baseSpaceNo = spaceNo
        self.taskInfo.taskSpaceNoChanged(spaceNo)

    def gmClaimTaskRec(self, taskId):
        _taskData = dataUtils.getTaskData(taskId)
        _parentId = dataUtils.taskFieldVal(_taskData, 'FatherTaskId')
        if _parentId:
            self.gmClaimTaskRec(_parentId)

        _task = self.taskInfo.getTask(taskId)
        if not _task:
            self.baseTaskClaim(
                taskId,
                actionContext.ClaimTaskCtx(
                    claimSrc=gameconst.ClaimTaskSrc.GM),
                needCheck=False)

    def gmForceSubmitTask(self, taskId):
        # 非gm指令不要调用该接口
        if str(taskId) not in TDD.datas:
            WARNING_MSG('gmForceSubmitTask, no task data:', taskId)
            return

        task = self.taskInfo.getTask(taskId)
        if not task:
            # 首先领取该任务
            self.gmClaimTaskRec(taskId)

        self.forceCompleteTaskNoCond(taskId)

    def afterTaskClaimed(self, taskId):
        return True, [(taskId, 1)]

    def afterTaskSubmitted(self, opUUID, taskId):
        self.taskFlowLog(taskId, "TaskSubmit", opUUID=opUUID)
        return True, [(taskId, 1)]

    def reqTaskEnterSpace(self, taskId):
        DEBUG_MSG('reqTaskEnterSpace:', taskId)
        task = self.taskInfo.getTask(taskId)
        if not task:
            WARNING_MSG('reqTaskEnterSpace, missing task, task id:', taskId)
            return
        if task.isInEndStat():
            WARNING_MSG('reqTaskEnterSpace, task is end:', taskId)
            return
        self.taskInfo.taskEnterSpace(self, task)

    def onCheckSameMap(self, taskID, isSame):
        task = self.taskInfo.getTask(taskID)
        if not task:
            WARNING_MSG('onCheckSameMap, missing task, task id:', taskID)
            return
        self.taskInfo.onCheckSameTaskResult(self, task, isSame)

    def checkUnlockBountyTask(self):
        if self.getPersistentMiscProp(gameconst.AvatarProps.unlockBountyTaskFlag, 0):
            return

        if not self.isUIVisible(gameconst.BOUNTY_TASK_UI_ID):
            return

        self.setPersistentMiscProp(gameconst.AvatarProps.unlockBountyTaskFlag, 1)

        self.taskInfo.refreshHookRewardTask(self.getAvatarLevel())
        self.taskInfo.sendHookRewardTaskList(self)

