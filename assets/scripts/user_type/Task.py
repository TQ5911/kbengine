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
        _dic = json.loads(jsonStr)
        self.__dict__.update(_dic)

    def updateFromDic(self, attrDic):
        for _attrName, attrVal in attrDic.items():
            if hasattr(self, _attrName):
                setattr(self, _attrName, attrVal)

    def updateTaskExtraAttrFromObj(self, attrObj):
        self.gameEntityDict = attrObj.gameEntityDict

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
        taskData = taskData or dataUtils.getTaskCfg(taskId)
        self.taskType = dataUtils.getTaskFieldVal(taskData, 'TaskType')
        cycleEnable = dataUtils.getTaskFieldVal(taskData, 'OpenCondCheckTaskCount')
        if cycleEnable:
            self.cycleType = dataUtils.getTaskFieldVal(taskData, 'OpenCondCountCycle')
            self.limitCount = dataUtils.getTaskFieldVal(taskData, 'OpenCondCountLimit')
        else:
            self.cycleType = gameconst.TaskCycleType.CYCLE_TASK_ENUM_NONE
            self.limitCount = 0
        self.rootTaskId = dataUtils.getRootTaskId(taskId)
        self.parentTaskId = dataUtils.getTaskFieldVal(taskData, 'FatherTaskId')

        self.lastChildTaskId = 0
        self.stat = gameconst.TaskStatEnum.TASK_STAT_DEFAULT
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
        self.childTaskIds = []
        self.pointsDic = {}
        self.targetDic = {}
        self.taskRewardLimitDic = {}
        self.guaranteeCount = 0

    def _lateReload(self):
        super(Task, self)._lateReload()
        for _tgt in self.getAllTargets():
            _tgt.reloadScript()

    def __setstate__(self, state):
        self.__init__(state['taskId'])
        self.fromSavedDict(state)

    def __getstate__(self):
        return self.toTaskSavedDict()

    def toTaskClientDict(self):
        _expiredTime = 0
        if self.expiredTime > 0:
            _expiredTime = self.expiredTime
        elif self.validSec > 0:
            _expiredTime = utils.curTS() + self.validSec

        _tgts = []
        for tgt in self.getAllTargets():
            _tgts.append(tgt.toClientDict())
        return {
            'taskType': self.taskType,
            'taskId': self.taskId,
            'startTime': self.startTime,
            'stat': self.stat,
            'limitCount': self.limitCount,
            'alreadyCount': self.alreadyCount,
            'expiredTime': _expiredTime,
            'claimCount': self.claimCount,
            'parentTaskId': self.parentTaskId,
            'extraJson': self.extraAttr.toTaskExtraAttrClientJson(),
            'targets': _tgts,
        }

    def toTaskSavedDict(self):
        tgts = []

        for tgt in self.getAllTargets():
            tgts.append(tgt.toTargetSavedDict())

        return {
            'claimSrc': self.claimSrc,
            'taskId': self.taskId,
            'stat': self.stat,
            'limitCount': self.limitCount,
            'claimCount': self.claimCount,
            'alreadyCount': self.alreadyCount,
            'startTime': self.startTime,
            'teamId': self.teamId,
            'validSec': self.validSec,
            'seed': self.seed,
            'expiredTime': self.expiredTime,
            'lastChildTaskId': self.lastChildTaskId,
            'taskRewardLimitDic': self.taskRewardLimitDic,
            'pointsDic': self.pointsDic,
            'childTaskIds': self.childTaskIds,
            'targets': tgts,
            'guaranteeCount': self.guaranteeCount,
            'extraJson': self.extraAttr.toTaskExtraAttrSavedJson(),
        }

    def fromSavedDict(self, dataDic):
        self.stat = dataDic['stat']
        self.taskId = dataDic['taskId']
        self.limitCount = dataDic['limitCount']
        self.claimCount = dataDic.get('claimCount', 0)
        self.teamId = dataDic.get('teamId', 0)
        self.alreadyCount = dataDic['alreadyCount']
        self.startTime = dataDic['startTime']
        self.validSec = dataDic.get('validSec', 0)
        self.seed = dataDic.get('seed', 0)
        self.expiredTime = dataDic['expiredTime']
        self.pointsDic = dataDic.get('pointsDic', {})
        self.lastChildTaskId = dataDic['lastChildTaskId']
        self.childTaskIds = list(dataDic['childTaskIds'])
        self.taskRewardLimitDic = dataDic.get('taskRewardLimitDic', {})
        self.extraAttr = TaskExtraAttr()
        _extraJson = dataDic.get('extraJson', '')
        self.extraAttr.fromTaskExtraAttrSavedJson(_extraJson)
        self.claimSrc = dataDic.get('claimSrc', gameconst.ClaimTaskSrcEnum.TASK_SRC_UNKNOWN)
        self.guaranteeCount = dataDic.get('guaranteeCount', 0)

        self.resetTargetDic()
        for _oneData in dataDic['targets']:
            tgt = TaskTargetInfo.TaskTgtFactory.createTargetBySavedDic(_oneData)
            self.addNewTarget(tgt)

    def updateFromTaskObj(self, owner, task):
        LOG_DBG('in Task::updateFromTaskObj, taskId:', task.taskId)
        # if newTask:
        # #以下几个属性不要被覆盖
        #     self.limitCount = task.limitCount
        #     self.claimCount = task.claimCount
        #     self.alreadyCount = task.alreadyCount

        self.claimSrc = task.claimSrc
        self.taskId = task.taskId
        self.setStat(owner, task.stat)
        self.teamId = task.teamId
        self.seed = task.seed
        self.startTime = task.startTime
        self.expiredTime = task.expiredTime
        self.validSec = task.validSec

        self.pointsDic = {taskId: (_pos[0], _pos[1], _pos[2]) for taskId, _pos in task.pointsDic.items()}

        self.extraAttr.updateTaskExtraAttrFromObj(task.extraAttr)
        self.childTaskIds = [tid for tid in task.childTaskIds]
        self.lastChildTaskId = task.lastChildTaskId
        self.guaranteeCount = task.guaranteeCount
        self.targetDic = {}
        for _tgtList in task.targetDic.values():
            for _tgt in _tgtList:
                _newTgt = TaskTargetInfo.TaskTgtFactory.createTargetByObj(_tgt)
                self.addNewTarget(_newTgt)

    def addNewTarget(self, tgt):
        self.targetDic.setdefault(tgt.tgtType, []).append(tgt)

    def resetTargetDic(self):
        self.targetDic = {}

    def findTargetByTypeAndId(self, tgtType, tgtId):
        _targetList = self.getTgtsByType(tgtType)
        for target in _targetList:
            if target.tgtId == tgtId:
                return target
        return None

    def getTgtsByType(self, tgtType):
        return self.targetDic.get(tgtType, [])

    def getAllTargets(self):
        _tgts = []
        for tgtList in self.targetDic.values():
            _tgts.extend(tgtList)
        return _tgts

    def getTargetDungeonList(self):
        _dunList = []
        for tgt in self.getAllTargets():
            if tgt.dungeonNo > 1 and tgt.dungeonNo not in _dunList:
                _dunList.append(tgt.dungeonNo)
        return _dunList

    @staticmethod
    def listShuffle(seed, srcList):
        _gap = [
            2, 3, 5, 7, 11, 13, 17, 19, 23, 29,\
            31, 37, 41, 43, 47, 53, 59, 61, 67, 71,\
            73, 79, 83, 89, 97, 101, 103, 107, 109,
        ]
        _result = []
        src_num = len(srcList)
        if 0 == src_num:
            return _result
        gap_num = len(_gap)
        dstIdx = seed % src_num
        gapIdx = seed % gap_num
        for _ in range(src_num):
            cnt = 0
            while srcList[dstIdx] in _result and cnt <= src_num:
                cnt += 1
                dstIdx += 1
                if dstIdx >= src_num:
                    dstIdx = dstIdx % src_num
            _result.append(srcList[dstIdx])
            gapIdx += 1
            if gapIdx >= gap_num:
                gapIdx = gapIdx % gap_num
            dstIdx = dstIdx + _gap[gapIdx]
            if dstIdx >= src_num:
                dstIdx = dstIdx % src_num
        LOG_DBG('in listShuffle:', seed, srcList, _result)
        return _result

    def initTaskFromData(self, owner, taskId, taskCtx, alreadyCount=0, 
                         claimCount=0, taskRewardLimitDic=None):
        _taskInfo = owner.taskInfo
        self.claimSrc = taskCtx.claimSrc
        self.seed = taskCtx.seed

        _taskData = dataUtils.getTaskCfg(taskId)
        # LOG_DBG('in Task::initTaskFromData, taskId:', taskId, alreadyCount, claimCount, taskCtx.extra)
        self.setStat(owner, gameconst.TaskStatEnum.TASK_STAT_RUNNING)
        self.claimCount = claimCount
        self.alreadyCount = alreadyCount
        self.taskRewardLimitDic = taskRewardLimitDic or {}
        self.startTime = utils.curTS()

        _pointsDic = taskCtx.extra.get("pointsDic", {})
        self.pointsDic = {taskId: (_pos[0], _pos[1], _pos[2]) for taskId, _pos in _pointsDic.items()}

        # childTasks
        cfgChildTaskIds = dataUtils.getTaskFieldVal(_taskData, 'ChildTaskIds')
        if len(cfgChildTaskIds) > 0:
            _checkLevel = 0
            if taskCtx.teamBaseInfoDic:
                teamLevels = taskCtx.teamBaseInfoDic.get('levels', [])
                if len(teamLevels) > 0:
                    _checkLevel = sum(teamLevels) / len(teamLevels)

            _checkLevel = _checkLevel or gameglobal.roleCache.get(owner.id, {}).get('level', 1)
            _checkLevel = int(_checkLevel)
            childTaskIds = dataUtils.calcChildTaskIds(_taskData, cfgChildTaskIds, _checkLevel, seed=taskCtx.seed)
            if not childTaskIds:
                # 到这里说明配置错误(浮戏苍灵出现过)：父任务领取条件最低等级为0，但是所有子任务最低等级至少为20级，
                # 小于20级的玩家会出现没有可以领取的子任务的情况
                gameengine.panicStack('initTaskFromData, config error!!! no match child task:', taskId,
                                          cfgChildTaskIds)
                return False
            self.childTaskIds = childTaskIds

        self.teamId = taskCtx.teamId
        failedSec = dataUtils.getTaskFieldVal(_taskData, 'FailCondTimeLimit')
        if failedSec > 0:
            failedSec = int(failedSec)
            if dataUtils.getTaskFieldVal(_taskData, 'FailCondTimingOffline'):
                # 下线后依旧计时的任务
                self.expiredTime = utils.curTS() + failedSec
                _taskInfo.addExpiredTimeTask(taskId, self.expiredTime)
            else:
                # 下线以后不再计时
                self.validSec = failedSec
                _taskInfo.addValidSecTask(taskId, self.validSec)

        # 计数任务
        checkValue = dataUtils.getTaskFieldVal(_taskData, 'FinCondNeedCheckValue')
        if checkValue:
            values = dataUtils.getTaskFieldVal(_taskData, 'FinCondCheckValue')
            for _idx, _valueData in enumerate(values):
                if _valueData['Value'] <= 0:
                    continue
                tgt = TaskTargetInfo.TaskTgtFactory.createTarget(gameconst.TaskTargetEnum.TASK_TARGET_COUNT,
                                                                 _idx, _valueData['Value'], _valueData['CompareType'])
                self.addNewTarget(tgt)

        # 杀怪任务
        hasKillMst = dataUtils.getTaskFieldVal(_taskData, 'FinCondHasKillMon')
        if hasKillMst:
            tgtKillMonsters = dataUtils.getTaskFieldVal(_taskData, 'FinCondKillMonster')
            killMonstersMode = dataUtils.getTaskFieldVal(_taskData, 'FinCondKillMonsterMode')
            killMonstersTotalCount = dataUtils.getTaskFieldVal(_taskData, 'FinCondKillMonsterNum')

            monsterIDs = set()
            _tgts = []

            for oneData in tgtKillMonsters:
                monsterId = oneData['MonsterId']
                if monsterId > 0:
                    if monsterId in monsterIDs:
                        LOG_ERR('策划一个任务配置了两个相同的monsterId', monsterId, oneData)
                        continue

                    monsterIDs.add(monsterId)

                _tgts.append(oneData)

            for oneData in _tgts:
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

                tgt = TaskTargetInfo.TaskTgtFactory.createTarget(gameconst.TaskTargetEnum.TASK_TARGET_MONSTERS,
                                                                 monsterId, dstCnt, mapId, killMonstersMode, killMonstersTotalCount, monsterIDs)
                self.addNewTarget(tgt)

        # 收集物品任务
        hasGatherItems = dataUtils.getTaskFieldVal(_taskData, 'FinCondHasGatherItems')
        if hasGatherItems:
            tgtItems = dataUtils.getTaskFieldVal(_taskData, 'FinCondGatherItems')
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
                itemCurNum = owner.getItemNum(itemId, ignoreCheck=True)
                tgt = TaskTargetInfo.TaskTgtFactory.createTarget(gameconst.TaskTargetEnum.TASK_TARGET_ITEMS,
                                                                 itemId, dstCnt, srcIdList, srcRatio,
                                                                 _oneData.get("MapId", 0), itemCurNum)
                self.addNewTarget(tgt)

        # 交互采集任务
        hasInterCollect = dataUtils.getTaskFieldVal(_taskData, 'FinCondHasInterCollect')
        if hasInterCollect:
            collData = dataUtils.getTaskFieldVal(_taskData, 'FinCondInterCollect')
            for _oneData in collData:
                collId = _oneData['CollId']
                dstCnt = _oneData['Count']
                mapId = _oneData['MapId']
                if collId <= 0 or dstCnt <= 0:
                    continue
                tgt = TaskTargetInfo.TaskTgtFactory.createTarget(gameconst.TaskTargetEnum.TASK_TARGET_COLLECT,
                                                                 collId, dstCnt, mapId)

                self.addNewTarget(tgt)

        # 播放一个动作任务
        if dataUtils.getTaskFieldVal(_taskData, 'FinCondIsTriggerAction'):
            for oneTgtData in dataUtils.getTaskFieldVal(_taskData, 'FinCondTriggerAction'):
                actionId = oneTgtData.get('ActionId')
                if not actionId:
                    continue
                tgt = TaskTargetInfo.TaskTgtFactory.createTarget(gameconst.TaskTargetEnum.TASK_TARGET_ACTION,
                                                                 actionId, oneTgtData['MapId'])
                self.addNewTarget(tgt)

        # 与npc交谈任务
        tgtTalkToNpc = dataUtils.getTaskFieldVal(_taskData, 'FinCondFinDialogs')
        for _oneData in tgtTalkToNpc:
            npcIdStr = _oneData['NPCId']
            dialogIdStr = _oneData['DialogId']
            if not npcIdStr or not dialogIdStr:
                continue
            _npcIdList = [int(_npcId) for _npcId in str(npcIdStr).split('|') if int(_npcId) > 0]
            dialogIdList = [int(_dialogId) for _dialogId in str(dialogIdStr).split('|') if int(_dialogId) > 0]
            if not _npcIdList or not dialogIdList:
                continue
            tgt = TaskTargetInfo.TaskTgtFactory.createTarget(gameconst.TaskTargetEnum.TASK_TARGET_TALK_NPC,
                                                             _npcIdList, dialogIdList, _oneData['MapId'])
            self.addNewTarget(tgt)

        # 到达指定区域
        if dataUtils.getTaskFieldVal(_taskData, 'FinCondIsTriggerArea'):
            if not _pointsDic:
                rootTask = _taskInfo.getRootTask(self.taskId)
                if rootTask:
                    _pointsDic = rootTask.pointsDic
            rdPoint = None
            if _pointsDic:
                rdPoint = _pointsDic.get(self.taskId, None)
            tgt = TaskTargetInfo.TaskTgtFactory.createTarget(gameconst.TaskTargetEnum.TASK_TARGET_REACH_AREA,
                                                             dataUtils.getTaskFieldVal(_taskData, 'FinCondReachArea'),
                                                             rdPoint)
            self.addNewTarget(tgt)
            _taskInfo.addReachAreaTargetTask(taskId, tgt)

        # 到达某个等级
        dstLevel = dataUtils.getTaskFieldVal(_taskData, 'FinCondToLevel')
        if dstLevel > 0:
            tgt = TaskTargetInfo.TaskTgtFactory.createTarget(gameconst.TaskTargetEnum.TASK_TARGET_LEVEL,
                                                             dstLevel)
            tgt.avatarLevelUp(owner.getAvatarLevel())
            self.addNewTarget(tgt)

        # 关联任务处于某个状态
        _finRelateTaskIdsStr = dataUtils.getTaskFieldVal(_taskData, 'FinCondRelateTaskId')
        # 注意这里，编辑器导出的 FinCondRelateTaskId 的数据还可能是: str类型的 '0', int 类型的 0, int 类型的 taskId
        _finRelateTaskIdsStr = str(_finRelateTaskIdsStr)
        if _finRelateTaskIdsStr:
            relTaskIds = _finRelateTaskIdsStr.split('|')
            for _relTaskId in relTaskIds:
                # 编辑器导出后的数据，reltaskid可能为：'', '0'
                if not _relTaskId:
                    continue
                _relTaskId = int(_relTaskId)
                if not _relTaskId:
                    continue
                relTaskStat = owner.taskInfo.getTaskCurrentState(_relTaskId)
                tgt = TaskTargetInfo.TaskTgtFactory.createTarget(gameconst.TaskTargetEnum.TASK_TARGET_RELATE_TASK,
                                                                 _relTaskId, dataUtils.getTaskFieldVal(_taskData,
                                                                                                   'FinCondRelateTaskState'),
                                                                 relTaskStat)
                self.addNewTarget(tgt)

        # 变量目标
        varFrmId = dataUtils.getTaskFieldVal(_taskData, 'FinCondVarCheckFormID')
        if varFrmId:
            tgt = TaskTargetInfo.TaskTgtFactory.createTarget(gameconst.TaskTargetEnum.TASK_TARGET_VAR, varFrmId)
            tgt.checkVarCond(owner, varFrmId, dataUtils.getTaskFieldVal(_taskData, 'FinCondVarCheckParam'))
            self.addNewTarget(tgt)

        # 计次目标
        counterId = dataUtils.getTaskFieldVal(_taskData, 'FinCondCountID')
        dstCnt = dataUtils.getTaskFieldVal(_taskData, 'FinCondCountTgt')
        counterParam = dataUtils.getTaskFieldVal(_taskData, 'FinCondCountParam')
        if counterId and dstCnt:
            curCnt = 0
            tgt = TaskTargetInfo.TaskTgtFactory.createTarget(gameconst.TaskTargetEnum.TASK_TARGET_COUNTER, counterId,
                                                             dstCnt,
                                                             counterParam, curCnt)
            self.addNewTarget(tgt)
        return True

    def isStat(self, stat):
        return self.stat == stat

    def setStat(self, owner, stat, opUUID=0):
        if self.stat == stat:
            return

        LOG_INFO('Task::setStat, taskId {}, new:{} ==> cur:{}'.format(self.taskId, stat, self.stat))

        self.stat = stat
        owner.onTaskStateChanged(self.taskId, stat)

        mapId = 0
        data = RRTID.datas.get(self.taskId, None)
        if data:
            mapId = data['mapID']

        if not opUUID:
            opUUID = KBEngine.genUUID64()
        LogTrackingMgr.LogTrackingMgr.Task_State_Change(owner.gbID, owner.accountEntity.clientDistinctId, owner.gbID, self.taskId, self.stat, self.taskType, mapId, owner.getRoleCacheAttr('level'), opUUID)

    def isInEndStat(self):
        # 任务是否处于最终状态
        return self.stat in [gameconst.TaskStatEnum.TASK_STAT_SUBMITTED, gameconst.TaskStatEnum.TASK_STAT_QUIT]

    def isTaskExpired(self):
        return 0 < self.expiredTime <= utils.curTS()

    def canAddRewardId(self, taskId, rewardId, rewardMaxNum=1):
        _hasRewardTimes = self.taskRewardLimitDic.get(taskId, {}).get(rewardId, 0)
        if _hasRewardTimes >= rewardMaxNum:
            LOG_INFO('in canAddRewardId, hasRewardTimes > rewardMaxNum:', taskId, rewardId, _hasRewardTimes,
                      rewardMaxNum)
            return False
        else:
            return True

    def updateTgtItemsCount(self, owner):
        LOG_DBG('in Task::updateItemsCount')
        update = False
        _tgtList = self.getTgtsByType(gameconst.TaskTargetEnum.TASK_TARGET_ITEMS)
        for _tgt in _tgtList:
            itemCnt = owner.getItemNum(_tgt.tgtId, ignoreCheck=True)
            if _tgt.stepCnt == itemCnt:
                continue
            update = True
            _tgt.stepCnt = min(itemCnt, _tgt.dstCnt)
        return update

    def recordSubmitTaskRewardId(self, taskId, rewardId):
        _dic = self.taskRewardLimitDic.setdefault(taskId, {})
        _dic[rewardId] = _dic.get(rewardId, 0) + 1

    def getTaskTgtItemsWealthVal(self):
        deductWealthVal = dropAward.DeductWealthVal()
        tgtList = self.getTgtsByType(gameconst.TaskTargetEnum.TASK_TARGET_ITEMS)
        for tgt in tgtList:
            deductWealthVal.addWealthByItemId(tgt.tgtId, tgt.dstCnt, dataUtils.getItemDefaultBindType())
        return deductWealthVal

    def deductTaskTgtItemsSucc(self):
        tgtList = self.getTgtsByType(gameconst.TaskTargetEnum.TASK_TARGET_ITEMS)
        for tgt in tgtList:
            tgt.deductItemsSucc()
        return

    def checkTgtRelateTaskStat(self, relateTaskId, relateTaskStat):
        target = self.findTargetByTypeAndId(gameconst.TaskTargetEnum.TASK_TARGET_RELATE_TASK, relateTaskId)
        return target and target.relateTaskReachStat(relateTaskId, relateTaskStat)

    def updateTaskTgtCnt(self, idx, timeList):
        LOG_DBG('in updateTaskTgtCnt:', idx, timeList)
        target = self.findTargetByTypeAndId(gameconst.TaskTargetEnum.TASK_TARGET_COUNT, idx)
        if target is None:
            LOG_WARN('       in updateTaskTgtCnt, no count target:', idx, timeList)
            return
        return target.addMultiCnt(idx, timeList)

    def updateCounterTarget(self, targetId, params):
        LOG_DBG('in updateTaskTgtCnt:', targetId, params)
        target = self.findTargetByTypeAndId(gameconst.TaskTargetEnum.TASK_TARGET_COUNTER, targetId)
        if target is None:
            LOG_WARN('       in updateCounterTarget, no counter target:', self.taskId, targetId)
            return
        return target.counter(targetId, params)

    def checkAllTargetsReached(self):
        if self.isStat(gameconst.TaskStatEnum.TASK_STAT_FINISHED):
            return True
        for tgt in self.getAllTargets():
            if not tgt.isTaskTargetCompleted():
                return False
        return True

    def isEmptyTarget(self):
        return len(self.targetDic) == 0

    def setActionTgtCompleted(self, actionId):
        actTgtList = self.getTgtsByType(gameconst.TaskTargetEnum.TASK_TARGET_ACTION)
        updated = False
        tgtArrived = False
        for tgt in actTgtList:
            if tgt.tgtId != actionId:
                continue
            if not tgt.isTaskTargetCompleted():
                updated = True
            tgt.setTaskTargetCompleted()
            tgtArrived = True
        return updated, tgtArrived

    def setAllTargetsReached(self, owner):
        LOG_INFO('in Task::setAllTargetsReached:', self.taskId)
        for tgt in self.getAllTargets():
            tgt.setTaskTargetCompleted()

        self.setStat(owner, gameconst.TaskStatEnum.TASK_STAT_FINISHED)
        return

    def addGameEntityIdRecord(self, gameEntityId):
        gameEntityId = str(gameEntityId)
        _dic = self.extraAttr.gameEntityDict
        _dic[gameEntityId] = _dic.get(gameEntityId, 0) + 1

    def addCollectNum(self, targetType, args):
        isAdd = False
        if targetType == gameconst.TaskTargetEnum.TASK_TARGET_COLLECT:
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
        if targetType == gameconst.TaskTargetEnum.TASK_TARGET_COUNTER:
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
    def createTaskBySavedDict(cls, savedDict):
        taskData = dataUtils.getTaskCfg(savedDict['taskId'])
        if not taskData:
            gameengine.panicStack('invalid taskId:', savedDict['taskId'])
            return
        _task = Task(savedDict['taskId'], taskData=taskData)
        _task.fromSavedDict(savedDict)
        return _task

    @classmethod
    def createTask(cls, owner, taskId, taskContext, alreadyCount=0, claimCount=0, 
                   taskRewardLimitDic=None):
        if not taskId:
            gameengine.panicStack('invalid taskId:', taskId)
            return
        taskData = dataUtils.getTaskCfg(taskId)
        if not taskData:
            gameengine.panicStack('no taskdata:', taskId)
            return
        task = Task(taskId)
        task.initTaskFromData(owner, taskId, taskContext, alreadyCount=alreadyCount, claimCount=claimCount,
                              taskRewardLimitDic=taskRewardLimitDic)
        return task

    @classmethod
    def createTaskByTaskObj(cls, owner, taskObj):
        taskData = dataUtils.getTaskCfg(taskObj.taskId)
        if not taskData:
            gameengine.panicStack('invalid taskId:', taskObj.taskId)
            return
        task = Task(taskObj.taskId)
        task.updateFromTaskObj(owner, taskObj)
        return task
