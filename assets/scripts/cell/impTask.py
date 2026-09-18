# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
import sMath
import utils
import dataUtils
import gameconst
import formula
import impTalk
import actionContext
import random
import gameclass
import math
import gametimer
import gamedecorator
import gamePlay_gamePlay
import gameengine
import dungeonSrc

import taskItemSrc as TISD
import taskMonster as TMD
import gameconfig
import taskClass_taskTarget as TCCTD


class ImpTask(impTalk.ImpTalk):

    @gamedecorator.checkGameconfigEnable('task')
    @utils.isMyself
    @gamedecorator.limitcall(1)
    def reqUpdateTaskByTalkToNpc(self, exposed, opType, npcEntityId, taskId, dialogId):
        _npcEnt = KBEngine.entities.get(npcEntityId)
        if not _npcEnt or not _npcEnt.IsNpc:
            LOG_WARN('reqUpdateTaskByTalkToNpc, invalid npcEntityId:', npcEntityId)
            return

        if self.spaceNo != _npcEnt.spaceNo:
            LOG_WARN('reqUpdateTaskByTalkToNpc, diff spaceNo:', self.spaceNo, _npcEnt.spaceNo)
            return

        distance = sMath.distance2D(self.position, _npcEnt.position)
        curSpeed = self.calculateCurrentSpeed()
        if distance >= curSpeed * 2:
            LOG_WARN('reqUpdateTaskByTalkToNpc, not enough distance:', self.position, _npcEnt.position)
            return

        npcId = _npcEnt.npcId
        # 跟随npc校验
        _taskData = dataUtils.getTaskCfg(taskId)
        if _taskData and _taskData.get('CheckFollowNPC', False) and _taskData.get('TaskFollowNPC', []):
            for _followInfo in _taskData.get('TaskFollowNPC', []):
                if _followInfo['NpcFollowID'] == npcId:
                    if not self._checkTaskFollowNPC(npcEntityId, taskId, npcId, dialogId):
                        return

        if opType == gameconst.TaskTalkToPNCEnum.CLAIM_TASK:
            self.doStartClaimTask(taskId, taskCtx=actionContext.ClaimTaskCtx(claimSrc=gameconst.ClaimTaskSrcEnum.TASK_SRC_NPC_DIALOG))
        elif opType == gameconst.TaskTalkToPNCEnum.SUBMIT_TASK:
            self.cellCheckTaskSubmitCond(taskId, 0)
        elif opType == gameconst.TaskTalkToPNCEnum.FAIL_TASK:
            self.base.startTaskFailed(taskId, gameconst.TaskNotSuccReasonEnum.NPC_DIALOG)
        elif opType == gameconst.TaskTalkToPNCEnum.NPC_TALK_TARGET:
            self.base.onTaskStepUpdate(gameconst.TaskTargetEnum.TASK_TARGET_TALK_NPC, taskId, (npcId, dialogId))

    @gamedecorator.checkGameconfigEnable('task')
    @utils.isMyself
    def reqClaimTask(self, exposed, claimSrcType, taskId, paramStr):
        LOG_INFO('in reqClaimTask:', taskId)
        if paramStr == "reset":
            self.base.reqQuitTask(taskId)
        self.doStartClaimTask(taskId)
        return

    def doStartClaimTask(self, taskId, itemMethodName='', itemArgs=(), taskCtx=None):
        LOG_INFO('doStartClaimTask:', taskId)
        if not taskCtx:
            taskCtx = actionContext.ClaimTaskCtx()

        if not dataUtils.isRootTask(taskId):
            self.onClaimTaskFailed(taskId, taskCtx)
            return

        if itemMethodName:
            taskCBInfoDic = self.getTempMiscProp(gameconst.EntityPropsEnum.callbackTmpInfo)
            if not taskCBInfoDic:
                taskCBInfoDic = {}
                self.setTempMiscProp(gameconst.EntityPropsEnum.callbackTmpInfo, taskCBInfoDic)
            callbackUUID = KBEngine.genUUID64()
            taskCBInfoDic[callbackUUID] = (itemMethodName, itemArgs)
            taskCtx.callbackUUID = callbackUUID

        taskCtx.seed = random.randint(100, 10000)
        self._contClaimTask(taskId, taskCtx)

    def _contClaimTask(self, taskId, taskCtx):
        self._claimSingleTask(taskId, taskCtx)

    def _claimSingleTask(self, taskId, taskCtx):
        _taskData = dataUtils.getRootTaskData(taskId)
        _taskCondResult = self._checkPlayerClaimTaskCellCond(_taskData)
        if not _taskCondResult:
            self.onClaimTaskFailed(taskId, taskCtx, msgId=_taskCondResult.msgId, msgArgs=_taskCondResult.msgArgs)
            return
        _pointsDic = self._getReachAreaPoints(taskId)
        if _pointsDic:
            taskCtx.extra['_pointsDic'] = _pointsDic
        self.base.onCheckSingleTaskCellCondSucc(taskId, taskCtx)

    def _checkPlayerClaimTaskCellCond(self, taskData):
        # 自动放弃任务不可接取
        if taskData.get('IsAutoQuit'):
            return gameclass.TaskCondResultCls(False, playerName=self.name)
        taskId = taskData.get("TaskId", 0)
        if not dataUtils.isTaskInOpenTime(taskId):
            return gameclass.TaskCondResultCls(False, playerName=self.name)
        if not dataUtils.isTaskUnlockDayReached(taskData):
            LOG_WARN('   _checkPlayerClaimTaskCellCond, OpenCondUnlockDay not reached:', taskId)
            return gameclass.TaskCondResultCls(False, playerName=self.name)
        # level condition
        levelCondResult = self._checkTaskPlayerLevelCond(taskData)
        if not levelCondResult:
            return levelCondResult

        # guild level check
        _openCondCheckGuildLv = dataUtils.getTaskFieldVal(taskData, 'OpenCondCheckGuildLv')
        if _openCondCheckGuildLv and self.guildLevel < _openCondCheckGuildLv:
            return gameclass.TaskCondResultCls(
                False,
                playerName=self.name,
            )

        # 职业
        # openCondCheckProfres 默认值可能是 字符串 "0"、空字符串、整数0
        openCondCheckProfres = dataUtils.getTaskFieldVal(taskData, 'OpenCondCheckProfres')
        if openCondCheckProfres:
            openCondCheckProfresList = openCondCheckProfres.split('|')
            if str(self.school) not in openCondCheckProfresList:
                LOG_WARN('   _checkPlayerClaimTaskCellCond, OpenCondCheckProfres failed:', openCondCheckProfres, self.school)
                return gameclass.TaskCondResultCls(False, playerName=self.name)

        # 性别校验
        openCondCheckSex = dataUtils.getTaskFieldVal(taskData, 'OpenCondCheckSex')
        if openCondCheckSex and openCondCheckSex != self.sex:
            LOG_WARN('   _checkPlayerClaimTaskCellCond, openCondCheckSex failed:', openCondCheckSex, self.sex)
            return gameclass.TaskCondResultCls(False, playerName=self.name)

        # 触发区域校验
        if taskData.get('OpenCondIsTriggerArea'):
            openCondTriggerArea = dataUtils.getTaskFieldVal(taskData, 'OpenCondTriggerArea')
            posX = openCondTriggerArea.get('X', 0.0)
            posZ = openCondTriggerArea.get('Z', 0.0)
            mapId = openCondTriggerArea.get('MapId', 0)
            width = openCondTriggerArea.get('Width', 0.0)
            triggerDis = openCondTriggerArea.get('TriggerDis', 0.0)
            length = openCondTriggerArea.get('Length', 0.0)
            dungeonNo = formula.parseDungeonNoBySpaceNo(self.spaceNo)
            if mapId != dungeonNo:
                LOG_WARN('   _checkPlayerClaimTaskCellCond, mapId failed:', taskData['TaskId'], self.spaceNo,
                            openCondTriggerArea)
                return gameclass.TaskCondResultCls(False, playerName=self.name)

            _widthDelta = abs(self.position[0] - posX)
            _lenthDelta = abs(self.position[2] - posZ)
            if triggerDis > 0:
                if math.pow(_widthDelta, 2) + math.pow(_lenthDelta, 2) > math.pow(triggerDis + 3, 2):
                    LOG_WARN('   _checkPlayerClaimTaskCellCond, area cond failed:', taskData['TaskId'],
                                self.position, openCondTriggerArea)
                    return gameclass.TaskCondResultCls(False, playerName=self.name)
            else:
                if _widthDelta > width / 2 + 3 or _lenthDelta > length / 2 + 3:
                    LOG_WARN('   _checkPlayerClaimTaskCellCond, area cond failed:', taskData['TaskId'],
                                self.position, openCondTriggerArea)
                    return gameclass.TaskCondResultCls(False, playerName=self.name)
        return gameclass.TaskCondResultCls(True)

    def _checkTaskPlayerLevelCond(self, taskData):
        _claimCondLevelMin = dataUtils.getTaskFieldVal(taskData, 'ClaimCondLevelMin')
        _claimCondLevelMax = dataUtils.getTaskFieldVal(taskData, 'ClaimCondLevelMax')
        if 0 == _claimCondLevelMax:
            _claimCondLevelMax = utils.getMaxPlayerLevel()
        if self.level < _claimCondLevelMin or self.level > _claimCondLevelMax:
            LOG_WARN('in _checkTaskPlayerLevelCond, level check failed:', taskData['TaskId'])
            return gameclass.TaskCondResultCls(False, dataUtils.getTaskMsgId('taskClaimAlert_Team_LevelCheck'),
                                            msgArgs=(self.name,), playerName=self.name)
        return gameclass.TaskCondResultCls(True)

    def _getReachAreaPoints(self, taskId):
        _randomPoints = {}
        randTargetTaskIds = dataUtils.getRandTargetPointTaskIds(taskId)
        for tid in randTargetTaskIds:
            taskData = dataUtils.getTaskCfg(tid)
            point = self._getTaskRandomPoint(taskData)
            if not point:
                continue
            _randomPoints[taskData['TaskId']] = (point[0], point[1], point[2])
        return _randomPoints

    def _getTaskRandomPoint(self, taskData):
        if not taskData:
            return None
        if not dataUtils.getTaskFieldVal(taskData, 'FinCondIsTriggerArea'):
            return None
        triggerDis = dataUtils.getTaskFieldVal(taskData, 'FinCondReachArea').get('TriggerDis', 0)
        if triggerDis > 0:
            areaData = dataUtils.getTaskFieldVal(taskData, 'FinCondReachArea')
            _center = (areaData['X'], areaData['Y'], areaData['Z'])
            _radi = min(areaData['Width'], areaData['Length'])
            for _ in range(10):
                _posList = self.getRandomPoints(_center, _radi, 3, 0)
                if not _posList:
                    continue
                return _posList[0]
        return None

    def onClaimTaskFailed(self, taskId, taskCtx, msgId=dataUtils.getTaskMsgId('taskClaimAlert_OtherFail'), msgArgs=None):
        LOG_INFO('in onClaimTaskFailed:', taskId, msgId)
        self._sendTaskFailedMsg(taskId, taskCtx, msgId, msgArgs)
        self._onTaskClaimCallback(False, taskId, taskCtx.callbackUUID)
        if taskCtx.claimSrc == gameconst.ClaimTaskSrcEnum.TASK_SRC_REWARD_TASK:
            self.base.baseTaskClaimedFailed(taskCtx, taskId)

    def _sendTaskFailedMsg(self, taskId, taskCtx, msgId, msgArgs):
        taskData = dataUtils.getTaskCfg(taskId)
        if not taskData or dataUtils.getTaskFieldVal(taskData, 'DispHiddenTask') or dataUtils.getTaskFieldVal(taskData,
                                                                                                        'ClaimCondAutoTake'):
            return
        if msgArgs is None:
            msgArgs = []
        errMsgId = taskCtx.extra.get("errMsgId", 0)

        if msgId > 0:
            self.showMsg(msgId, msgArgs)
        # errMsgId 是额外需要展示的
        if errMsgId > 0:
            self.showMsg(errMsgId, [])

    def claimTaskSuccCallback(self, taskId, callbackUUID):
        self._onTaskClaimCallback(True, taskId, callbackUUID)
        return

    def _onTaskClaimCallback(self, result, taskId, callbackUUID):
        taskCBInfoDic = self.getTempMiscProp(gameconst.EntityPropsEnum.callbackTmpInfo)
        if not taskCBInfoDic:
            return
        callbackInfo = taskCBInfoDic.pop(callbackUUID, None)
        if not callbackInfo:
            return
        getattr(self, callbackInfo[0])(result, *callbackInfo[1])
        return

    @gamedecorator.checkGameconfigEnable('task')
    @utils.isMyself
    def taskFailedLeaveArea(self, srcEntityID, taskId):
        LOG_INFO('in taskFailedLeaveArea:', srcEntityID, taskId)
        taskData = dataUtils.getTaskCfg(taskId)
        if dataUtils.getTaskFieldVal(taskData, 'FailCondIsLeaveArea'):
            area = dataUtils.getTaskFieldVal(taskData, 'FailCondLeaveArea')
            _deltaX = abs(area['X'] - self.position[0])
            _deltaZ = abs(area['Z'] - self.position[2])
            if _deltaX > area['Width'] / 2 or _deltaZ > area['Length']:
                self.base.startTaskFailed(taskId, gameconst.TaskNotSuccReasonEnum.LEAVE_AREA)

    @gamedecorator.checkGameconfigEnable('task')
    @utils.isMyself
    def taskFailedEnterArea(self, srcEntityID, taskId):
        LOG_INFO('in taskFailedEnterArea:', srcEntityID, taskId)
        taskData = dataUtils.getTaskCfg(taskId)
        if dataUtils.getTaskFieldVal(taskData, 'FailCondIsEnterArea'):
            area = dataUtils.getTaskFieldVal(taskData, 'FailCondEnterArea')
            _deltaX = abs(area['X'] - self.position[0])
            _deltaZ = abs(area['Z'] - self.position[2])
            if _deltaX < area['Width'] / 2 and _deltaZ < area['Length']:
                self.base.startTaskFailed(taskId, gameconst.TaskNotSuccReasonEnum.ENTER_AREA)

    def checkTaskCompleteActionTarget(self, taskId, tgtType, tgtId):
        taskData = dataUtils.getTaskCfg(taskId)
        curDungonNo = formula.parseDungeonNoBySpaceNo(self.spaceNo)
        _result = False
        if dataUtils.getTaskFieldVal(taskData, 'FinCondIsTriggerAction'):
            curSpeed = self.calculateCurrentSpeed()
            for oneTgtData in dataUtils.getTaskFieldVal(taskData, 'FinCondTriggerAction'):
                actionId = oneTgtData.get('ActionId')
                if not actionId or actionId != tgtId:
                    continue
                cfgPos = (oneTgtData['X'], oneTgtData['Y'], oneTgtData['Z'])
                distance = sMath.distance2D(self.position, cfgPos)
                if oneTgtData['MapId'] == curDungonNo and distance < curSpeed * 2:
                    _result = True
                    break
        self.base.onCheckTaskCompleteActionTargetCallback(_result, taskId, tgtType, tgtId)


    ######################### 组任务相关 ###################################
    def _claimTeamTask(self, taskId, taskContext):
        if not self.isCaptain():
            self.onClaimTaskFailed(taskId, taskContext)
            return
        taskContext.teamId = self.teamId
        self.checkTeamTaskCellCond(taskId, taskContext)

    def checkTeamTaskCellCond(self, taskId, taskCtx):
        if not self.isInTeam(self.gbId):
            self.onClaimTaskFailed(taskId, taskCtx)
            return

        if not self.isCaptain():
            self.onClaimTaskFailed(taskId, taskCtx, msgId=dataUtils.getTaskMsgId('taskClaimAlert_Team_LeaderCheck'))
            return

        _rootTaskData = dataUtils.getRootTaskData(taskId)
        memberNumLimit = _rootTaskData.get('ClaimCondCheckTeam', {}).get('TeamCountLimit', 0)
        if self.teamInfo.howManyMember() < memberNumLimit:
            self.onClaimTaskFailed(taskId, taskCtx, msgId=dataUtils.getTaskMsgId('taskClaimAlert_Team_PalNumCheck'),
                                 msgArgs=[str(memberNumLimit), ])
            return

        if dataUtils.isSHFSTask(taskId) and taskCtx.claimSrc != gameconst.ClaimTaskSrcEnum.TASK_SRC_FROM_ACTION:
            #一条龙任务特殊处理，只有在 FROM_ACTION 时候才检查队员条件
            self.checkTeamTaskPlayerCondSuccess(taskId, taskCtx, [])
            return

        self.setTempMiscProp(gameconst.EntityPropsEnum.teamTaskCondCheck, {})
        onlineTeamMemGBIds = self.teamInfo.onlineMembers()
        for _memGbId in onlineTeamMemGBIds:
            teamPlayerVal = self.teamInfo.teamPlayerDict[_memGbId]
            if _memGbId == self.gbId:
                self.checkTeamTaskMemberCond(taskId, self.base, self.position, taskCtx)
            else:
                teamPlayerVal.playerBox.cell.checkTeamTaskMemberCond(
                    taskId, self.base, self.position, taskCtx)

    def checkTeamTaskMemberCond(self, taskId, captainBox, captainPos, taskCtx):
        # 任务领取条件只检查根任务
        _taskData = dataUtils.getRootTaskData(taskId)
        cellCondResult = self._checkPlayerClaimTaskCellCond(_taskData)
        if not cellCondResult:
            captainBox.cell.checkTeamTaskPlayerCondCB(taskId, cellCondResult, self.gbId, taskCtx)
            return

        #队伍每个玩家都要检查base条件，包括物品条件
        self.base.checkTeamTaskBasePlayerCond(taskId, captainBox, taskCtx)

    def checkTeamTaskPlayerCondCB(self, taskId, checkResult:gameclass.TaskCondResultCls, fromGbId, taskCtx):
        _teamCheckDic = self.getTempMiscProp(gameconst.EntityPropsEnum.teamTaskCondCheck, None)
        if _teamCheckDic is None:
            LOG_WARN('checkTeamTaskPlayerCondCB, no teamCheckDic')
            return
        _teamCheckDic[fromGbId] = checkResult
        if len(_teamCheckDic) < len(self.teamInfo.onlineMembers()):
            return
        self.popTempMiscProp(gameconst.EntityPropsEnum.teamTaskCondCheck)
        specialFailedMsgIds = [dataUtils.getTaskMsgId('taskClaimAlert_Team_LevelCheck'),
                               dataUtils.getTaskMsgId('taskClaimAlert_Team_NearbyCheck'),
                               dataUtils.getTaskMsgId('taskClaimAlert_Team_FollowCheck'),
                               ]
        failedPlayerNames = ''
        failedMsgId = -1
        failedMsgArgs = ()
        condFailedGBIDs = []
        for gbid, _checkResult in _teamCheckDic.items():
            if _checkResult:
                continue
            condFailedGBIDs.append(gbid)
            msgId = _checkResult.msgId
            if msgId in specialFailedMsgIds:
                if failedMsgId not in specialFailedMsgIds:
                    failedMsgId = msgId
                    failedPlayerNames = _checkResult.playerName
                    failedMsgArgs = (failedPlayerNames, )
                elif msgId == failedMsgId:
                    failedPlayerNames += ", "
                    failedPlayerNames += _checkResult.playerName
                    failedMsgArgs = (failedPlayerNames, )
            else:
                failedMsgId = msgId
                failedMsgArgs = _checkResult.msgArgs
        #单人支持的组队任务，可以只有部分队员领取成功
        if len(condFailedGBIDs)>0 and not dataUtils.isSingleSupportTeamTask(taskId):
            self.onClaimTaskFailed(taskId, taskCtx, failedMsgId, msgArgs=failedMsgArgs)
            return
        self.checkTeamTaskPlayerCondSuccess(taskId, taskCtx, condFailedGBIDs)

    def checkTeamTaskPlayerCondSuccess(self, taskId, taskCtx, condFailedGBIDs):
        _cbArgs = (taskId, taskCtx, condFailedGBIDs)
        gameengine.getTeamStub(self.teamInfo.teamId).fetchTeamMemberInfo(
            self, 
            self.teamInfo.teamId,
            'teamTaskGetTeamMemberInfoCB', 
            _cbArgs)

    def teamTaskGetTeamMemberInfoCB(self, teamBaseInfoDic, taskId, taskCtx, condFailedGBIDs):
        _pointsDic = self._getReachAreaPoints(taskId)
        if _pointsDic:
            taskCtx.extra['pointsDic'] = _pointsDic
        taskCtx.isCaptain = True
        taskCtx.teamBaseInfoDic = teamBaseInfoDic
        self.base.onCheckTeamTaskAllCondSucc(taskId, taskCtx, condFailedGBIDs)
        return

    @gamedecorator.checkGameconfigEnable('task')
    @utils.isMyself
    def reqStartPlayCinema(self, srcEntityID, cinemaId):
        LOG_INFO('in startPlayCinema:', cinemaId)
        self.prepareStartPlayCinema(cinemaId)

    def prepareStartPlayCinema(self, cinemaId):
        LOG_INFO('in prepareStartPlayCinema:', cinemaId)
        self.client.onStartPlayCinema(cinemaId)
        self.afterPlayCinema(cinemaId)

    def afterPlayCinema(self, cinemaId):
        LOG_INFO('in afterPlayCinema:', cinemaId)
        self.resetAllTargetTypeCache()

    @gamedecorator.checkGameconfigEnable('task')
    @utils.isMyself
    def cinemaPlayEnd(self, srcEntityID, cinemaId):
        LOG_INFO('in cinemaPlayingEnd:', cinemaId)
        self.onCinemaPlayingEnd(cinemaId)

    def startSyncTasksFromCaptain(self):
        if self.isCaptain():
            return
        _captainSpaceNo = self.teamInfo.getCaptainSpaceNo()
        dungonNo = formula.parseDungeonNoBySpaceNo(_captainSpaceNo)
        if not gamePlay_gamePlay.datas.get(dungonNo, {}).get('isTaskShareScene', 1):
            LOG_WARN('   in startSyncTasksFromCaptain, cant sync tasks, spaceNo not match:',
                        dungonNo, _captainSpaceNo, self.spaceNo)
            return
        self.teamInfo.fetchCaptainBox().cell.captainSyncTasksToNewMem(self.teamId, self.gbId, self.base)

    def onCinemaPlayingEnd(self, cinemaId):
        self.flowCtrlPlayerCinemaPlayEnded(cinemaId)
        # 推进「播放指定id剧情动画」计次任务目标
        if cinemaId:
            self.base.taskCheckCounterTarget(TCCTD.couterTargetDic['SkipSpecifiedTimeline'], (cinemaId,))

    def captainSyncTasksToNewMem(self, teamId, newMemGbId, newMemBox):
        LOG_INFO("captainSyncTasksToNewMem::", teamId, newMemGbId, newMemBox)
        _captainInfoDic = {"captainSpaceNo": self.spaceNo,
                          "captainPosition": self.position}
        self.base.captainSyncTasksToNewMem(teamId, newMemGbId, newMemBox, _captainInfoDic)

    def cellCheckTaskSubmitCond(self, taskId, popRewardUUID):
        self.base.onCheckCellSubmitCondSucc(taskId, self.isCaptain(), popRewardUUID)
        return True

    def captainSubmitTeamTask(self, taskId):
        # 队长发起提交组队任务
        if not self.isCaptain():
            LOG_WARN('     in captainSyncTeamTask, not captain')
            return
        self.cellCheckTaskSubmitCond(taskId, 0)
        return

    def cellTaskCondCheckOnAddTeam(self, teamTaskList, captainInfoDic):
        LOG_INFO('in onCellTaskNewMemAddTeam:', [_t.taskId for _t in teamTaskList], captainInfoDic)
        rmIdxList = []
        for _idx, task in enumerate(teamTaskList):
            taskData = dataUtils.getTaskCfg(task.taskId)
            if not self._checkTaskPlayerLevelCond(taskData):
                rmIdxList.append(_idx)
                continue
            if not self._checkTaskGuildCond(taskData, captainInfoDic.get('captainGuildUUID', 0)):
                rmIdxList.append(_idx)
        for rmIdx in reversed(rmIdxList):
            teamTaskList.pop(rmIdx)
        if teamTaskList:
            self.base.baseTaskCondCheckOnAddTeam(teamTaskList, captainInfoDic)

    ######################### 组任务相关 end ###################################
    def taskPreEnterSpace(self, taskId, dungeonNo, dstPos, dstDir):
        LOG_INFO("taskPreEnterSpace 1", taskId, dungeonNo, dstPos, dstDir)

        if not dstPos:
            #如果使用原位置传送，当前场景和目标场景只能是大世界或大世界副本
            if not formula.inWorldLineScene(self.spaceNo) and not formula.isBigWorldNaviCostLikedSpace(self.spaceNo):
                LOG_ERR('taskPreEnterSpace, use cur position tel, from space must be big world:', self.spaceNo)
                return
            if not formula.inWorldLineScene(dungeonNo) and not formula.isBigWorldNaviCostLikedSpace(dungeonNo):
                LOG_ERR('taskPreEnterSpace, use cur position tel, dst space must be big world:', dungeonNo)
                return
            dstPos = self.position
        if not dstDir:
            dstDir = self.direction

        if formula.checkWorldLineType(dungeonNo):
            LOG_INFO("taskPreEnterSpace 2", taskId, dungeonNo, dstPos, dstDir)
            self.taskEnterWorldLine(taskId, dungeonNo, dstPos, dstDir)
            return
        if dungeonNo not in gamePlay_gamePlay.datas:
            LOG_INFO("taskPreEnterSpace 3", taskId, dungeonNo, dstPos, dstDir)
            return
        dungeonSpaceType = gamePlay_gamePlay.datas[dungeonNo]['type']
        dungeonEnterType = gamePlay_gamePlay.datas[dungeonNo]['enterType']
        LOG_INFO('in taskPreEnterSpace:', taskId, dungeonNo, dungeonSpaceType, dungeonEnterType, self.spaceNo, self.direction)
        if gameconst.DungeonTypeJudge.isSingleDungeon(dungeonSpaceType, dungeonEnterType) or gameconst.DungeonTypeJudge.isBothDungeon(dungeonSpaceType, dungeonEnterType):
            #单人任务才能进单人副本
            not dataUtils.isTeamTask(taskId) and self.taskSelfEnterSingleDungeon(dungeonNo, dstPos, dstDir, taskId)
        elif gameconst.DungeonTypeJudge.isTeamDungeon(dungeonSpaceType, dungeonEnterType) or gameconst.DungeonTypeJudge.isBothDungeon(dungeonSpaceType, dungeonEnterType):
            #组队任务才能进team dungeon
            dataUtils.isTeamTask(taskId) and self.taskSelfEnterTeamDungeon(taskId, dungeonNo)
        # elif gameconst.SpaceType.SpaceGuild == dungeonSpaceType:
        #     #帮会场景
        #     myDungeonNo = formula.parseDungeonNoBySpaceNo(self.spaceNo)
        #     if dungeonNo == myDungeonNo:
        #         self.removeState(gameconst.StateEnum.Fishing)
        #         self.client.startTeleport(self.spaceNo, dstPos)
        #         self.telToPos(dstPos, dstDir)
        #     else:
        #         self.cellEnterGuildSpace(0, None)
        else:
            gameengine.panicStack('in taskPreEnterSpace:', taskId, dungeonNo)
        return

    def taskEnterWorldLine(self, taskId, dungeonNo, dstPos, dstDir):
        LOG_INFO('in taskEnterWorldLine:', taskId, dstPos, dstDir, self.spaceNo, dungeonNo)
        if formula.inWorldLineScene(self.spaceNo):
            self.onTelToMainCityWithCast(None, dungeonNo, dstPos, dstDir, None, None, None, None)
        else:
            self.doLeaveSingleDungeonWithDstPos(dungeonNo, dstPos, dstDir)

    def _onCheckLineAreaByTaskTeltoPos(self, checkCode, dstPos, dstDir):
        if checkCode == gameconst.EnterLineCodeEnum.ENTER_CHECK_SUCCESS:
            self.client.startTeleport(self.spaceNo, dstPos)
            self.telToPos(dstPos, dstDir)
        else:
            LOG_ERR('_onCheckLineAreaByTaskTeltoPos failed, ', checkCode, dstPos)

    def taskSelfEnterSingleDungeon(self, dungeonNo, dstPos, dstDir, taskId):
        LOG_INFO('in taskSelfEnterSingleDungeon:', self.spaceNo, dungeonNo, dstPos, dstDir, taskId)
        # TODO(DUNGEON_SRC): use task src
        finRewardInstance = dataUtils.getTaskFieldVal(dataUtils.getTaskCfg(taskId), 'FinRewardInstance')
        NeedPlayFx = finRewardInstance.get('NeedPlayFx', True)
        if NeedPlayFx:
            self.client.onNoNeedPlayFx()

        src = dungeonSrc.BasicDungeonSrc(srcId=gameconst.DunSrcEnum.FROM_TASK)
        myDungeonNo = formula.parseDungeonNoBySpaceNo(self.spaceNo)
        if dungeonNo == myDungeonNo:
            # 相同單人副本之間的傳送到指定位置
            LOG_INFO('in taskSelfEnterSingleDungeon: do same dungeonNo telport, ', self.spaceNo, dungeonNo, dstPos, dstDir)
            self._resetTeleportCache(self.spaceNo, None, None)
            self.client.startTeleport(self.spaceNo, dstPos)
            self._stopCommonCast()
            self.beforeTeleport(self.spaceNo)
            self.telToPos(dstPos, dstDir)
            try:
                ret = self._onTeleportSuccess(None)
            except Exception as e:
                gameengine.panicStack(f"taskSelfEnterSingleDungeon::raise exception, {e}")
                ret = False
            finally:
                if ret:
                    self.client.onTeleportDone(self.spaceNo, self.spaceNo)
                else:
                    LOG_ERR("taskSelfEnterSingleDungeon:: failure handle method")
                    self._popTeleportCache(self.spaceNo)
            return

        else:
            _extra = {'position':dstPos, 'direction':dstDir[2]*180/math.pi}
            self._enterSingleDungeon(dungeonNo, src, _extra)

    def taskSelfEnterTeamDungeon(self, taskId, dungeonNo):
        LOG_INFO('in taskSelfEnterTeamDungeon:', taskId, dungeonNo)
        if not self.isInTeam(self.gbId) or not self.isCaptain():
            return

        _myDungeon = formula.parseDungeonNoBySpaceNo(self.spaceNo)
        if _myDungeon == dungeonNo:
            LOG_WARN('cant enter same dungeon')
            return

        _src = dungeonSrc.BasicDungeonSrc(srcId=gameconst.DunSrcEnum.FROM_TASK)
        self.selfEnterTeamDungeon(dungeonNo, _src)

    def onTaskRwdLeaveDungeon(self, taskId, dungeonNo, claimSrc):
        LOG_INFO('in onTaskRwdLeaveDungeon:', taskId, self.spaceNo, dungeonNo)
        if claimSrc==gameconst.ClaimTaskSrcEnum.TASK_SRC_GM_FINISH_NEWBIE and dungeonNo and not formula.inDungeonScene(self.spaceNo):
            return

        if dungeonNo != formula.fetchMapId(self.spaceNo):
            LOG_WARN('   in onTaskRwdLeaveDungeon, not in dungeon:', dungeonNo, self.spaceNo)
            return

        if formula.inLineScene(self.spaceNo):
            LOG_WARN('   in onTaskRwdLeaveDungeon, player already in line space')
            return

        leaveDelay = dataUtils.getTaskFieldVal(dataUtils.getTaskCfg(taskId), 'FinRewardLevInsDelay')
        if claimSrc==gameconst.ClaimTaskSrcEnum.TASK_SRC_QUIT_TASK_REWARD_LEAVE_DUNGEON:
            leaveDelay = dataUtils.getTaskFieldVal(dataUtils.getTaskCfg(taskId), 'AbanRewardLevInsDelay')
        box = gameengine.getDungeonStubBySpaceNo(self.spaceNo)
        if box:
            if formula.inSingleDungeonScene(self.spaceNo):
                box.completeSingleDungeon(self.spaceNo, self.gbId, True, leaveDelay)
            elif formula.inTeamDungeonScene(self.spaceNo):
                box.completeTeamDungeon(self.spaceNo, self.teamId, True, leaveDelay, gameconst.DunegonCompleteReasonType.FINISHED)
            elif formula.inRaidDungeonScene(self.spaceNo):
                box.completeRaidDungeon(self.spaceNo, self.raidUUID, True, leaveDelay, gameconst.DunegonCompleteReasonType.FINISHED)
        return

    def cellEnterTaskTargetDungeon(self, taskId, dungeonNo, extra):
        myDungeonNo = formula.parseDungeonNoBySpaceNo(self.spaceNo)
        if myDungeonNo == dungeonNo:
            LOG_WARN('   cellEnterTaskTargetDungeon, already in dungeon:', dungeonNo)
            return
        LOG_INFO('cellEnterTaskTargetDungeon:', taskId, dungeonNo, extra)
        _src = dungeonSrc.BasicDungeonSrc(
            srcId=gameconst.DunSrcEnum.FROM_TASK,
            playerBox=self.base, playerGBID=self.gbId,
        )

        if dataUtils.isTeamTask(taskId):
            if not (self.isCaptain()\
                    or dataUtils.isSingleSupportTeamTask(taskId)\
                    or extra.get('forceEnter')):
                LOG_WARN('   cellEnterTaskTargetDungeon, is not captain:', taskId, dungeonNo)
                return
            self._enterTeamDungeon(dungeonNo, _src, extra=extra)
        else:
            self._enterSingleDungeon(dungeonNo, _src, extra=extra)

    @gamedecorator.checkGameconfigEnable('task')
    @utils.isMyself
    def taskReachArea(self, srcEntityID, taskId):
        LOG_INFO('in taskReachArea:', taskId)
        # 到达指定区域任务目标由服务端检验
        dungeonNo = formula.parseDungeonNoBySpaceNo(self.spaceNo)
        areaTaskInCurDun = self.getTempMiscProp(gameconst.EntityPropsEnum.taskAreaTarget, {}).get(dungeonNo, {})
        _target = areaTaskInCurDun.get(taskId)
        if not _target:
            LOG_WARN('   taskReachArea, target not found:', taskId, dungeonNo)
            return

        if _target.isInArea(self.position[0], self.position[2]):
            self._taskReachArea(taskId)

    def _taskReachArea(self, taskId):
        self.base.onTaskStepUpdate(gameconst.TaskTargetEnum.TASK_TARGET_REACH_AREA, taskId, (self.position[0],
                                                                                             self.position[2]))

    def onAreaTargetTaskAdd(self, taskId, target):
        _areaTaskDic = self.getTempMiscProp(gameconst.EntityPropsEnum.taskAreaTarget)
        if not _areaTaskDic:
            _areaTaskDic = {}
            self.setTempMiscProp(gameconst.EntityPropsEnum.taskAreaTarget, _areaTaskDic)
        _areaTaskDic.setdefault(target.mapId, {})
        _areaTaskDic[target.mapId][taskId] = target
        self.tryStartAreaTaskCheckTimer()

    def refreshAreaTaskTimer(self):
        self.tryStartAreaTaskCheckTimer()

    def tryStartAreaTaskCheckTimer(self):
        if self.checkAreaTgtTaskTimer:
            return
        dungeonNo = formula.parseDungeonNoBySpaceNo(self.spaceNo)
        areaTaskInCurDun = self.getTempMiscProp(gameconst.EntityPropsEnum.taskAreaTarget, {}).get(dungeonNo)
        if not areaTaskInCurDun:
            return
        self.checkAreaTgtTaskTimer = self.addTimerCB(1, '_checkAreaTaskTarget', (),
                                                    gametimer.TIMER_TAG_CHECK_AREA_TARGET_TASK, 'checkAreaTgtTaskTimer')

    def _checkAreaTaskTarget(self):
        self.checkAreaTgtTaskTimer = 0
        dungeonNo = formula.parseDungeonNoBySpaceNo(self.spaceNo)
        areaTaskInCurDun = self.getTempMiscProp(gameconst.EntityPropsEnum.taskAreaTarget, {}).get(dungeonNo, {})
        for _taskId, _target in areaTaskInCurDun.items():
            if _target.isInArea(self.position[0], self.position[2]):
                self._taskReachArea(_taskId)
        self.tryStartAreaTaskCheckTimer()

    def removeAreaTargetTask(self, taskId, dungeonNo):
        LOG_INFO('removeAreaTargetTask:', taskId, dungeonNo)
        areaTaskDic = self.getTempMiscProp(gameconst.EntityPropsEnum.taskAreaTarget, None)
        if areaTaskDic is None:
            LOG_WARN('removeAreaTargetTask, areaTaskDic is None')
            return
        _areaTaskDicInCurDun = areaTaskDic.get(dungeonNo, None)
        if _areaTaskDicInCurDun is None:
            LOG_WARN('removeAreaTargetTask, areaTaskDicInCurDun is None')
            return
        _areaTaskDicInCurDun.pop(taskId, None)
        if not _areaTaskDicInCurDun:
            areaTaskDic.pop(dungeonNo, None)
        if not areaTaskDic:
            self.popTempMiscProp(gameconst.EntityPropsEnum.taskAreaTarget, None)

    def checkKillMonsterTrigger(self, monsterId, monsterUID):
        _monsterTaskIds = TMD.datas.get(str(monsterId))
        itemSrcTaskIds = TISD.datas.get(str(monsterId))
        if _monsterTaskIds or itemSrcTaskIds:
            self.base.onTaskStepUpdate(
                gameconst.TaskTargetEnum.TASK_TARGET_MONSTERS, 
                0, 
                (self.spaceNo, monsterId, monsterUID))

    def checkSameMap(self, taskID):
        LOG_INFO("checkSameMap ", taskID)
        taskData = dataUtils.getTaskCfg(taskID)
        if not taskData:
            LOG_ERR("checkSameMap, missing task cfg ", taskID)
            return
        if not dataUtils.getTaskFieldVal(taskData, 'ClaimCanTransIns'):
            LOG_INFO("checkSameMap, no ClaimCanTransIns ", taskID)
            return
        claimTransData = dataUtils.getTaskFieldVal(taskData, 'ClaimTransInstance')
        dungeonNo = claimTransData.get('MapId')
        if dungeonNo is None:
            LOG_WARN('checkSameMap, map id is None', taskID, claimTransData)
            return
        ret = dungeonNo == formula.fetchMapId(self.spaceNo)
        self.base.onCheckSameMap(taskID, ret)

    def submitTaskCheck(self, taskId):
        LOG_INFO("submitTaskCheck ", taskId)
        if self.isInTeam():
            self.base.submitTaskCheckCB(taskId, gameconst.TeamType.TEAM)
            return
        if self.inRaid():
            self.base.submitTaskCheckCB(taskId, gameconst.TeamType.RAID)
            return
        self.base.submitTaskCheckCB(taskId, gameconst.TeamType.DEFAULT)
