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


class ImpTask(impTalk.ImpTalk):

    @gamedecorator.checkGameconfigEnable('task')
    @utils.isMyself
    @gamedecorator.limitcall(1)
    def reqUpdateTaskByTalkToNpc(self, exposed, opType, npcEntityId, taskId, dialogId):
        npcEnt = KBEngine.entities.get(npcEntityId)
        if not npcEnt or not npcEnt.IsNpc:
            WARNING_MSG('reqUpdateTaskByTalkToNpc, invalid npcEntityId:', npcEntityId)
            return

        if self.spaceNo != npcEnt.spaceNo:
            WARNING_MSG('reqUpdateTaskByTalkToNpc, diff spaceNo:', self.spaceNo, npcEnt.spaceNo)
            return

        dis = sMath.distance2D(self.position, npcEnt.position)
        if dis >= self.speed * 2:
            WARNING_MSG('reqUpdateTaskByTalkToNpc, not enough distance:', self.position, npcEnt.position)
            return

        npcId = npcEnt.npcId
        # 跟随npc校验
        taskData = dataUtils.getTaskData(taskId)
        if taskData and taskData.get('CheckFollowNPC', False) and taskData.get('TaskFollowNPC', []):
            for followInfo in taskData.get('TaskFollowNPC', []):
                if followInfo['NpcFollowID'] == npcId:
                    if not self._checkTaskFollowNPC(npcEntityId, taskId, npcId, dialogId):
                        return

        if opType == gameconst.TaskOpTypeByTalkToPNC.CLAIM_TASK:
            self.startClaimTask(taskId, taskCtx=actionContext.ClaimTaskCtx(claimSrc=gameconst.ClaimTaskSrc.NPC_DIALOG))
        elif opType == gameconst.TaskOpTypeByTalkToPNC.SUBMIT_TASK:
            self.cellCheckTaskSubmitCond(taskId, 0)
        elif opType == gameconst.TaskOpTypeByTalkToPNC.FAIL_TASK:
            self.base.startTaskFailed(taskId, gameconst.TaskNotSuccReason.NPC_DIALOG)
        elif opType == gameconst.TaskOpTypeByTalkToPNC.NPC_TALK_TARGET:
            self.base.onTaskStepUpdate(gameconst.TaskTargetType.TASK_TARGET_TALK_NPC, taskId, (npcId, dialogId))

    @gamedecorator.checkGameconfigEnable('task')
    @utils.isMyself
    def reqClaimTask(self, exposed, claimSrcType, taskId, paramStr):
        INFO_MSG('in reqClaimTask:', taskId)
        self.startClaimTask(taskId)
        return

    def startClaimTask(self, taskId, itemMethodName='', itemArgs=(), taskCtx=None):
        INFO_MSG('startClaimTask:', taskId)
        if not taskCtx:
            taskCtx = actionContext.ClaimTaskCtx()

        if not dataUtils.isRootTask(taskId):
            self.claimTaskFailed(taskId, taskCtx)
            return

        if itemMethodName:
            taskCBInfoDic = self.getTempMiscProp(gameconst.AvatarProps.callbackTmpInfo)
            if not taskCBInfoDic:
                taskCBInfoDic = {}
                self.setTempMiscProp(gameconst.AvatarProps.callbackTmpInfo, taskCBInfoDic)
            callbackUUID = KBEngine.genUUID64()
            taskCBInfoDic[callbackUUID] = (itemMethodName, itemArgs)
            taskCtx.callbackUUID = callbackUUID

        taskCtx.seed = random.randint(100, 10000)
        self._contClaimTask(taskId, taskCtx)

    def _contClaimTask(self, taskId, taskCtx):
        self._claimSingleTask(taskId, taskCtx)

    def _claimSingleTask(self, taskId, taskCtx):
        taskData = dataUtils.getRootTaskData(taskId)
        taskCondResult = self._checkPlayerClaimTaskCellCond(taskData)
        if not taskCondResult:
            self.claimTaskFailed(taskId, taskCtx, msgId=taskCondResult.msgId, msgArgs=taskCondResult.msgArgs)
            return
        pointsDic = self._getReachAreaPoints(taskId)
        if pointsDic:
            taskCtx.extra['pointsDic'] = pointsDic
        self.base.onCheckSingleTaskCellCondSucc(taskId, taskCtx)
        return

    def _checkPlayerClaimTaskCellCond(self, taskData):
        # 自动放弃任务不可接取
        if taskData.get('IsAutoQuit'):
            return gameclass.TaskCondResult(False, playerName=self.name)
        taskId = taskData.get("TaskId", 0)
        if not dataUtils.isTaskInOpenTime(taskId):
            return gameclass.TaskCondResult(False, playerName=self.name)
        # level condition
        levelCondResult = self._checkTaskPlayerLevelCond(taskData)
        if not levelCondResult:
            return levelCondResult

        # 职业
        # openCondCheckProfres 默认值可能是 字符串 "0"、空字符串、整数0
        openCondCheckProfres = dataUtils.taskFieldVal(taskData, 'OpenCondCheckProfres')
        if openCondCheckProfres:
            openCondCheckProfresList = openCondCheckProfres.split('|')
            if str(self.school) not in openCondCheckProfresList:
                WARNING_MSG('   _checkPlayerClaimTaskCellCond, OpenCondCheckProfres failed:', openCondCheckProfres, self.school)
                return gameclass.TaskCondResult(False, playerName=self.name)

        # 性别校验
        openCondCheckSex = dataUtils.taskFieldVal(taskData, 'OpenCondCheckSex')
        if openCondCheckSex and openCondCheckSex != self.sex:
            WARNING_MSG('   _checkPlayerClaimTaskCellCond, openCondCheckSex failed:', openCondCheckSex, self.sex)
            return gameclass.TaskCondResult(False, playerName=self.name)

        # 触发区域校验
        if taskData.get('OpenCondIsTriggerArea'):
            openCondTriggerArea = dataUtils.taskFieldVal(taskData, 'OpenCondTriggerArea')
            mapId = openCondTriggerArea.get('MapId', 0)
            posX = openCondTriggerArea.get('X', 0.0)
            posZ = openCondTriggerArea.get('Z', 0.0)
            width = openCondTriggerArea.get('Width', 0.0)
            length = openCondTriggerArea.get('Length', 0.0)
            triggerDis = openCondTriggerArea.get('TriggerDis', 0.0)
            dungeonNo = formula.getDungeonNoBySpaceNo(self.spaceNo)
            if mapId != dungeonNo:
                WARNING_MSG('   _checkPlayerClaimTaskCellCond, mapId failed:', taskData['TaskId'], self.spaceNo,
                            openCondTriggerArea)
                return gameclass.TaskCondResult(False, playerName=self.name)

            widthDelta = abs(self.position[0] - posX)
            lenthDelta = abs(self.position[2] - posZ)
            if triggerDis > 0:
                if math.pow(widthDelta, 2) + math.pow(lenthDelta, 2) > math.pow(triggerDis + 3, 2):
                    WARNING_MSG('   _checkPlayerClaimTaskCellCond, area cond failed:', taskData['TaskId'],
                                self.position, openCondTriggerArea)
                    return gameclass.TaskCondResult(False, playerName=self.name)
            else:
                if widthDelta > width / 2 + 3 or lenthDelta > length / 2 + 3:
                    WARNING_MSG('   _checkPlayerClaimTaskCellCond, area cond failed:', taskData['TaskId'],
                                self.position, openCondTriggerArea)
                    return gameclass.TaskCondResult(False, playerName=self.name)
        return gameclass.TaskCondResult(True)

    def _checkTaskPlayerLevelCond(self, taskData):
        ClaimCondLevelMin = dataUtils.taskFieldVal(taskData, 'ClaimCondLevelMin')
        ClaimCondLevelMax = dataUtils.taskFieldVal(taskData, 'ClaimCondLevelMax')
        if 0 == ClaimCondLevelMax:
            ClaimCondLevelMax = utils.getPlayerMaxLevel()
        if self.level < ClaimCondLevelMin or self.level > ClaimCondLevelMax:
            WARNING_MSG('in _checkTaskPlayerLevelCond, level check failed:', taskData['TaskId'])
            return gameclass.TaskCondResult(False, dataUtils.taskMsgId('taskClaimAlert_Team_LevelCheck'),
                                            msgArgs=(self.name,), playerName=self.name)
        return gameclass.TaskCondResult(True)

    def _getReachAreaPoints(self, taskId):
        randomPoints = {}
        randTargetTaskIds = dataUtils.getRandTargetPointTaskIds(taskId)
        for tid in randTargetTaskIds:
            taskData = dataUtils.getTaskData(tid)
            point = self._getTaskRandomPoint(taskData)
            if not point:
                continue
            randomPoints[taskData['TaskId']] = (point[0], point[1], point[2])
        return randomPoints

    def _getTaskRandomPoint(self, taskData):
        if not taskData:
            return None
        if not dataUtils.taskFieldVal(taskData, 'FinCondIsTriggerArea'):
            return None
        triggerDis = dataUtils.taskFieldVal(taskData, 'FinCondReachArea').get('TriggerDis', 0)
        if triggerDis > 0:
            areaData = dataUtils.taskFieldVal(taskData, 'FinCondReachArea')
            center = (areaData['X'], areaData['Y'], areaData['Z'])
            radi = min(areaData['Width'], areaData['Length'])
            for x in range(10):
                posList = self.getRandomPoints(center, radi, 3, 0)
                if not posList:
                    continue
                return posList[0]
        return None

    def claimTaskFailed(self, taskId, taskCtx, msgId=dataUtils.taskMsgId('taskClaimAlert_OtherFail'), msgArgs=None):
        INFO_MSG('in claimTaskFailed:', taskId, msgId)
        self._sendTaskFailedMsg(taskId, taskCtx, msgId, msgArgs)
        self._doTaskClaimCallback(False, taskId, taskCtx.callbackUUID)
        if taskCtx.claimSrc == gameconst.ClaimTaskSrc.REWARD_TASK:
            self.base.baseTaskClaimedFailed(taskCtx, taskId)

    def _sendTaskFailedMsg(self, taskId, taskCtx, msgId, msgArgs):
        taskData = dataUtils.getTaskData(taskId)
        if not taskData or dataUtils.taskFieldVal(taskData, 'DispHiddenTask') or dataUtils.taskFieldVal(taskData,
                                                                                                        'ClaimCondAutoTake'):
            return
        if msgArgs is None:
            msgArgs = []
        errMsgId = taskCtx.extra.get("errMsgId", 0)

        msgId > 0 and self.showMsg(msgId, msgArgs)
        # errMsgId 是额外需要展示的
        errMsgId > 0 and self.showMsg(errMsgId, [])
        return

    def claimTaskSuccCallback(self, taskId, callbackUUID):
        self._doTaskClaimCallback(True, taskId, callbackUUID)
        return

    def _doTaskClaimCallback(self, result, taskId, callbackUUID):
        taskCBInfoDic = self.getTempMiscProp(gameconst.AvatarProps.callbackTmpInfo)
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
        INFO_MSG('in taskFailedLeaveArea:', srcEntityID, taskId)
        taskData = dataUtils.getTaskData(taskId)
        if dataUtils.taskFieldVal(taskData, 'FailCondIsLeaveArea'):
            area = dataUtils.taskFieldVal(taskData, 'FailCondLeaveArea')
            deltaX = abs(area['X'] - self.position[0])
            deltaZ = abs(area['Z'] - self.position[2])
            if deltaX > area['Width'] / 2 or deltaZ > area['Length']:
                self.base.startTaskFailed(taskId, gameconst.TaskNotSuccReason.LEAVE_AREA)

    @gamedecorator.checkGameconfigEnable('task')
    @utils.isMyself
    def taskFailedEnterArea(self, srcEntityID, taskId):
        INFO_MSG('in taskFailedEnterArea:', srcEntityID, taskId)
        taskData = dataUtils.getTaskData(taskId)
        if dataUtils.taskFieldVal(taskData, 'FailCondIsEnterArea'):
            area = dataUtils.taskFieldVal(taskData, 'FailCondEnterArea')
            deltaX = abs(area['X'] - self.position[0])
            deltaZ = abs(area['Z'] - self.position[2])
            if deltaX < area['Width'] / 2 and deltaZ < area['Length']:
                self.base.startTaskFailed(taskId, gameconst.TaskNotSuccReason.ENTER_AREA)

    def checkTaskCompleteActionTarget(self, taskId, tgtType, tgtId):
        taskData = dataUtils.getTaskData(taskId)
        curDungonNo = formula.getDungeonNoBySpaceNo(self.spaceNo)
        result = False
        if dataUtils.taskFieldVal(taskData, 'FinCondIsTriggerAction'):
            for oneTgtData in dataUtils.taskFieldVal(taskData, 'FinCondTriggerAction'):
                actionId = oneTgtData.get('ActionId')
                if not actionId or actionId != tgtId:
                    continue
                cfgPos = (oneTgtData['X'], oneTgtData['Y'], oneTgtData['Z'])
                dis = sMath.distance2D(self.position, cfgPos)
                if oneTgtData['MapId'] == curDungonNo and dis < self.speed * 2:
                    result = True
                break
        self.base.onCheckTaskCompleteActionTargetCallback(result, taskId, tgtType, tgtId)


    ######################### 组任务相关 ###################################
    def _claimTeamTask(self, taskId, taskCtx):
        if not self.isCaptain():
            self.claimTaskFailed(taskId, taskCtx)
            return
        taskCtx.teamId = self.teamId
        self.checkTeamTaskCellCond(taskId, taskCtx)
        return

    def checkTeamTaskCellCond(self, taskId, taskCtx):
        if not self.isInTeam(self.gbId):
            self.claimTaskFailed(taskId, taskCtx)
            return
        if not self.isCaptain():
            self.claimTaskFailed(taskId, taskCtx, msgId=dataUtils.taskMsgId('taskClaimAlert_Team_LeaderCheck'))
            return
        rootTaskData = dataUtils.getRootTaskData(taskId)
        memberNumLimit = rootTaskData.get('ClaimCondCheckTeam', {}).get('TeamCountLimit', 0)
        if self.teamInfo.howManyMember() < memberNumLimit:
            self.claimTaskFailed(taskId, taskCtx, msgId=dataUtils.taskMsgId('taskClaimAlert_Team_PalNumCheck'),
                                 msgArgs=[str(memberNumLimit), ])
            return

        if dataUtils.isSHFSTask(taskId) and taskCtx.claimSrc != gameconst.ClaimTaskSrc.FROM_ACTION:
            #一条龙任务特殊处理，只有在 FROM_ACTION 时候才检查队员条件
            self.checkTeamTaskPlayerCondSuccess(taskId, taskCtx, [])
            return

        self.setTempMiscProp(gameconst.AvatarProps.teamTaskCondCheck, {})
        onlineTeamMemGBIds = self.teamInfo.onlineMembers()
        for memGbId in onlineTeamMemGBIds:
            teamPlayerVal = self.teamInfo.teamPlayerDic[memGbId]
            if memGbId == self.gbId:
                self.checkTeamTaskPlayerCond(taskId, self.base, self.position, taskCtx)
            else:
                teamPlayerVal.playerBox.cell.checkTeamTaskPlayerCond(taskId, self.base, self.position, taskCtx)

    def checkTeamTaskPlayerCond(self, taskId, captainBox, captainPos, taskCtx):
        # 任务领取条件只检查根任务
        taskData = dataUtils.getRootTaskData(taskId)
        cellCondResult = self._checkPlayerClaimTaskCellCond(taskData)
        if not cellCondResult:
            captainBox.cell.checkTeamTaskPlayerCondCB(taskId, cellCondResult, self.gbId, taskCtx)
            return

        needFollow = dataUtils.taskFieldVal(taskData, 'ClaimCondCheckTeam').get('NeedFollow', False)
        if needFollow and not self.isCaptain() and self.followCaptain == gameconst.TeamFollowState.Idle:
            WARNING_MSG('     in checkTeamTaskPlayerCond, bFollowCaptain is False')
            result = gameclass.TaskCondResult(False, dataUtils.taskMsgId('taskClaimAlert_Team_FollowCheck'), playerName=self.name)
            captainBox.cell.checkTeamTaskPlayerCondCB(taskId, result, self.gbId, taskCtx)
            return

        #队伍每个玩家都要检查base条件，包括物品条件
        self.base.checkTeamTaskBasePlayerCond(taskId, captainBox, taskCtx)
        return

    def checkTeamTaskPlayerCondCB(self, taskId, checkResult:gameclass.TaskCondResult, fromGbId, taskCtx):
        teamCheckDic = self.getTempMiscProp(gameconst.AvatarProps.teamTaskCondCheck, None)
        if teamCheckDic is None:
            WARNING_MSG('checkTeamTaskPlayerCondCB, no teamCheckDic')
            return
        teamCheckDic[fromGbId] = checkResult
        if len(teamCheckDic) < len(self.teamInfo.onlineMembers()):
            return
        self.popTempMiscProp(gameconst.AvatarProps.teamTaskCondCheck)
        specialFailedMsgIds = [dataUtils.taskMsgId('taskClaimAlert_Team_LevelCheck'),
                               dataUtils.taskMsgId('taskClaimAlert_Team_NearbyCheck'),
                               dataUtils.taskMsgId('taskClaimAlert_Team_FollowCheck'),
                               ]
        failedPlayerNames = ''
        failedMsgId = -1
        failedMsgArgs = ()
        condFailedGBIDs = []
        for gbid, checkResult in teamCheckDic.items():
            if checkResult:
                continue
            condFailedGBIDs.append(gbid)
            msgId = checkResult.msgId
            if msgId in specialFailedMsgIds:
                if failedMsgId not in specialFailedMsgIds:
                    failedMsgId = msgId
                    failedPlayerNames = checkResult.playerName
                    failedMsgArgs = (failedPlayerNames, )
                elif msgId == failedMsgId:
                    failedPlayerNames += ", "
                    failedPlayerNames += checkResult.playerName
                    failedMsgArgs = (failedPlayerNames, )
            else:
                failedMsgId = msgId
                failedMsgArgs = checkResult.msgArgs
        #单人支持的组队任务，可以只有部分队员领取成功
        if len(condFailedGBIDs)>0 and not dataUtils.isSingleSupportTeamTask(taskId):
            self.claimTaskFailed(taskId, taskCtx, failedMsgId, msgArgs=failedMsgArgs)
            return
        self.checkTeamTaskPlayerCondSuccess(taskId, taskCtx, condFailedGBIDs)
        return

    def checkTeamTaskPlayerCondSuccess(self, taskId, taskCtx, condFailedGBIDs):
        cbArgs = (taskId, taskCtx, condFailedGBIDs)
        gameengine.getTeamStub(self.teamInfo.teamId).getTeamMemberInfo(self, self.teamInfo.teamId,
                                                                        'teamTaskGetTeamMemberInfoCB', cbArgs)
        return

    def teamTaskGetTeamMemberInfoCB(self, teamBaseInfoDic, taskId, taskCtx, condFailedGBIDs):
        pointsDic = self._getReachAreaPoints(taskId)
        if pointsDic:
            taskCtx.extra['pointsDic'] = pointsDic
        taskCtx.isCaptain = True
        taskCtx.teamBaseInfoDic = teamBaseInfoDic
        self.base.onCheckTeamTaskAllCondSucc(taskId, taskCtx, condFailedGBIDs)
        return

    @gamedecorator.checkGameconfigEnable('task')
    @utils.isMyself
    def reqStartPlayCinema(self, srcEntityID, cinemaId):
        INFO_MSG('in startPlayCinema:', cinemaId)
        self.prepareStartPlayCinema(cinemaId)

    def prepareStartPlayCinema(self, cinemaId):
        INFO_MSG('in prepareStartPlayCinema:', cinemaId)
        self.client.onStartPlayCinema(cinemaId)
        self.afterPlayCinema(cinemaId)

    def afterPlayCinema(self, cinemaId):
        INFO_MSG('in afterPlayCinema:', cinemaId)
        self.resetAllTargetTypeCache()

    @gamedecorator.checkGameconfigEnable('task')
    @utils.isMyself
    def cinemaPlayEnd(self, srcEntityID, cinemaId):
        INFO_MSG('in cinemaPlayingEnd:', cinemaId)
        self.onCinemaPlayingEnd(cinemaId)

    def onCinemaPlayingEnd(self, cinemaId):
        self.flowCtrlPlayerCinemaPlayEnded(cinemaId)

    def startSyncTasksFromCaptain(self):
        if self.isCaptain():
            return
        captainSpaceNo = self.teamInfo.getCaptainSpaceNo()
        dungonNo = formula.getDungeonNoBySpaceNo(captainSpaceNo)
        if not gamePlay_gamePlay.datas.get(dungonNo, {}).get('isTaskShareScene', 1):
            WARNING_MSG('   in startSyncTasksFromCaptain, cant sync tasks, spaceNo not match:',
                        dungonNo, captainSpaceNo, self.spaceNo)
            return
        self.teamInfo.getCaptainBox().cell.captainSyncTasksToNewMem(self.teamId, self.gbId, self.base)

    def captainSyncTasksToNewMem(self, teamId, newMemGbId, newMemBox):
        INFO_MSG("captainSyncTasksToNewMem::", teamId, newMemGbId, newMemBox)
        captainInfoDic = {"captainSpaceNo": self.spaceNo,
                          "captainPosition": self.position}
        self.base.captainSyncTasksToNewMem(teamId, newMemGbId, newMemBox, captainInfoDic)

    def cellCheckTaskSubmitCond(self, taskId, popRewardUUID):
        self.base.onCheckCellSubmitCondSucc(taskId, self.isCaptain(), popRewardUUID)
        return True

    def captainSubmitTeamTask(self, taskId):
        # 队长发起提交组队任务
        if not self.isCaptain():
            WARNING_MSG('     in captainSyncTeamTask, not captain')
            return
        self.cellCheckTaskSubmitCond(taskId, 0)
        return

    def cellTaskCondCheckOnAddTeam(self, teamTaskList, captainInfoDic):
        INFO_MSG('in onCellTaskNewMemAddTeam:', [t.taskId for t in teamTaskList], captainInfoDic)
        rmIdxList = []
        for idx, task in enumerate(teamTaskList):
            taskData = dataUtils.getTaskData(task.taskId)
            if not self._checkTaskPlayerLevelCond(taskData):
                rmIdxList.append(idx)
                continue
            if not self._checkTaskGuildCond(taskData, captainInfoDic.get('captainGuildUUID', 0)):
                rmIdxList.append(idx)
        for rmIdx in reversed(rmIdxList):
            teamTaskList.pop(rmIdx)
        teamTaskList and self.base.baseTaskCondCheckOnAddTeam(teamTaskList, captainInfoDic)
        return

    ######################### 组任务相关 end ###################################
    def taskPreEnterSpace(self, taskId, dungeonNo, dstPos, dstDir):
        INFO_MSG("taskPreEnterSpace 1", taskId, dungeonNo, dstPos, dstDir)
        if not dstPos:
            #如果使用原位置传送，当前场景和目标场景只能是大世界或大世界副本
            if not formula.spaceInWorldLine(self.spaceNo) and not formula.isBigWorldNaviCostLikedSpace(self.spaceNo):
                ERROR_MSG('taskPreEnterSpace, use cur position tel, from space must be big world:', self.spaceNo)
                return
            if not formula.spaceInWorldLine(dungeonNo) and not formula.isBigWorldNaviCostLikedSpace(dungeonNo):
                ERROR_MSG('taskPreEnterSpace, use cur position tel, dst space must be big world:', dungeonNo)
                return
            dstPos = self.position
        if not dstDir:
            dstDir = self.direction

        if formula.isWorldLineType(dungeonNo):
            INFO_MSG("taskPreEnterSpace 2", taskId, dungeonNo, dstPos, dstDir)
            self.taskEnterWorldLine(taskId, dungeonNo, dstPos, dstDir)
            return
        if dungeonNo not in gamePlay_gamePlay.datas:
            INFO_MSG("taskPreEnterSpace 3", taskId, dungeonNo, dstPos, dstDir)
            return
        dungeonSpaceType = gamePlay_gamePlay.datas[dungeonNo]['type']
        dungeonEnterType = gamePlay_gamePlay.datas[dungeonNo]['enterType']
        INFO_MSG('in taskPreEnterSpace:', taskId, dungeonNo, dungeonSpaceType, dungeonEnterType, self.spaceNo, self.direction)
        if gameconst.DungeonType.isSingleDungeon(dungeonSpaceType, dungeonEnterType) or gameconst.DungeonType.isBothDungeon(dungeonSpaceType, dungeonEnterType):
            #单人任务才能进单人副本
            not dataUtils.isTeamTask(taskId) and self.taskSelfEnterSingleDungeon(dungeonNo, dstPos, dstDir)
        elif gameconst.DungeonType.isTeamDungeon(dungeonSpaceType, dungeonEnterType) or gameconst.DungeonType.isBothDungeon(dungeonSpaceType, dungeonEnterType):
            #组队任务才能进team dungeon
            dataUtils.isTeamTask(taskId) and self.taskSelfEnterTeamDungeon(taskId, dungeonNo)
        # elif gameconst.SpaceType.SpaceGuild == dungeonSpaceType:
        #     #帮会场景
        #     myDungeonNo = formula.getDungeonNoBySpaceNo(self.spaceNo)
        #     if dungeonNo == myDungeonNo:
        #         self.removeState(gameconst.State.Fishing)
        #         self.client.startTeleport(self.spaceNo, dstPos)
        #         self.telToPos(dstPos, dstDir)
        #     else:
        #         self.cellEnterGuildSpace(0, None)
        else:
            gameengine.reportCritical('in taskPreEnterSpace:', taskId, dungeonNo)
        return

    def taskEnterWorldLine(self, taskId, dungeonNo, dstPos, dstDir):
        INFO_MSG('in taskEnterWorldLine:', taskId, dstPos, dstDir, self.spaceNo, dungeonNo)
        if formula.spaceInWorldLine(self.spaceNo):
            self.onTelToMainCityWithCast(None, dungeonNo, dstPos, dstDir, None, None, None, None)
        else:
            self.doLeaveSingleDungeonWithDstPos(dungeonNo, dstPos, dstDir)

    def _onCheckLineAreaByTaskTeltoPos(self, checkCode, dstPos, dstDir):
        if checkCode == gameconst.EnterLineCode.CAN_ENTER:
            self.client.startTeleport(self.spaceNo, dstPos)
            self.telToPos(dstPos, dstDir)
        else:
            ERROR_MSG('_onCheckLineAreaByTaskTeltoPos failed, ', checkCode, dstPos)

    def taskSelfEnterSingleDungeon(self, dungeonNo, dstPos, dstDir):
        INFO_MSG('in taskSelfEnterSingleDungeon:', self.spaceNo, dungeonNo, dstPos, dstDir)
        # TODO(DUNGEON_SRC): use task src
        src = dungeonSrc.BasicDungeonSrc(srcId=gameconst.DungeonSrcEnum.FROM_TASK)
        myDungeonNo = formula.getDungeonNoBySpaceNo(self.spaceNo)
        if dungeonNo == myDungeonNo:
            # 相同單人副本之間的傳送到指定位置
            INFO_MSG('in taskSelfEnterSingleDungeon: do same dungeonNo telport, ', self.spaceNo, dungeonNo, dstPos, dstDir)
            self._resetTeleportCache(self.spaceNo, None, None)
            self.client.startTeleport(self.spaceNo, dstPos)
            self._stopCommonCast()
            self.beforeTeleport(self.spaceNo)
            self.telToPos(dstPos, dstDir)
            try:
                ret = self._onTeleportSuccess(None)
            except Exception as e:
                gameengine.reportCritical(f"taskSelfEnterSingleDungeon::raise exception, {e}")
                ret = False
            finally:
                if ret:
                    self.client.onTeleportDone(self.spaceNo, self.spaceNo)
                else:
                    ERROR_MSG("taskSelfEnterSingleDungeon:: failure handle method")
                    self._popTeleportCache(self.spaceNo)
            return

        else:
            extra = {'position':dstPos, 'direction':dstDir[2]*180/math.pi}
            self._enterSingleDungeon(dungeonNo, src, extra)
        return

    def taskSelfEnterTeamDungeon(self, taskId, dungeonNo):
        INFO_MSG('in taskSelfEnterTeamDungeon:', taskId, dungeonNo)
        if not self.isInTeam(self.gbId) or not self.isCaptain():
            return

        myDungeon = formula.getDungeonNoBySpaceNo(self.spaceNo)
        if myDungeon == dungeonNo:
            WARNING_MSG('cant enter same dungeon')
            return

        src = dungeonSrc.BasicDungeonSrc(srcId=gameconst.DungeonSrcEnum.FROM_TASK)
        self.selfEnterTeamDungeon(dungeonNo, src)
        return

    def onTaskRwdLeaveDungeon(self, taskId, dungeonNo, claimSrc):
        INFO_MSG('in onTaskRwdLeaveDungeon:', taskId, self.spaceNo, dungeonNo)
        if claimSrc==gameconst.ClaimTaskSrc.GM_FINISH_NEWBIE and dungeonNo and not formula.isDungeonSpace(self.spaceNo):
            return

        if dungeonNo != formula.getMapId(self.spaceNo):
            WARNING_MSG('   in onTaskRwdLeaveDungeon, not in dungeon:', dungeonNo, self.spaceNo)
            return

        if formula.isLineSpace(self.spaceNo):
            WARNING_MSG('   in onTaskRwdLeaveDungeon, player already in line space')
            return

        leaveDelay = dataUtils.taskFieldVal(dataUtils.getTaskData(taskId), 'FinRewardLevInsDelay')
        box = gameengine.getDungeonStubBySpaceNo(self.spaceNo)
        if box:
            if formula.isSingleDungeonSpace(self.spaceNo):
                box.completeSingleDungeon(self.spaceNo, self.gbId, True, leaveDelay)
            elif formula.isTeamDungeonSpace(self.spaceNo):
                box.completeTeamDungeon(self.spaceNo, self.teamId, True, leaveDelay, gameconst.DunegonCompleteReasonType.FINISHED)
            elif formula.isRaidDungeonSpace(self.spaceNo):
                box.completeRaidDungeon(self.spaceNo, self.raidUUID, True, leaveDelay, gameconst.DunegonCompleteReasonType.FINISHED)
        return

    def cellEnterTaskTargetDungeon(self, taskId, dungeonNo, extra):
        myDungeonNo = formula.getDungeonNoBySpaceNo(self.spaceNo)
        if myDungeonNo == dungeonNo:
            WARNING_MSG('   cellEnterTaskTargetDungeon, already in dungeon:', dungeonNo)
            return
        INFO_MSG('cellEnterTaskTargetDungeon:', taskId, dungeonNo, extra)
        src = dungeonSrc.BasicDungeonSrc(srcId=gameconst.DungeonSrcEnum.FROM_TASK,
                                         playerBox=self.base, playerGBID=self.gbId)
        if dataUtils.isTeamTask(taskId):
            if not (self.isCaptain() or dataUtils.isSingleSupportTeamTask(taskId) or extra.get('forceEnter')):
                WARNING_MSG('   cellEnterTaskTargetDungeon, is not captain:', taskId, dungeonNo)
                return
            self._enterTeamDungeon(dungeonNo, src, extra=extra)
        else:
            self._enterSingleDungeon(dungeonNo, src, extra=extra)
        return

    @gamedecorator.checkGameconfigEnable('task')
    @utils.isMyself
    def taskReachArea(self, srcEntityID, taskId):
        INFO_MSG('in taskReachArea:', taskId)
        # 到达指定区域任务目标由服务端检验
        dungeonNo = formula.getDungeonNoBySpaceNo(self.spaceNo)
        areaTaskInCurDun = self.getTempMiscProp(gameconst.AvatarProps.taskAreaTarget, {}).get(dungeonNo, {})
        _target = areaTaskInCurDun.get(taskId)
        if not _target:
            WARNING_MSG('   taskReachArea, target not found:', taskId, dungeonNo)
            return

        if _target.isInArea(self.position[0], self.position[2]):
            self._taskReachArea(taskId)

    def _taskReachArea(self, taskId):
        self.base.onTaskStepUpdate(gameconst.TaskTargetType.TASK_TARGET_REACH_AREA, taskId, (self.position[0],
                                                                                             self.position[2]))

    def onAreaTargetTaskAdd(self, taskId, target):
        areaTaskDic = self.getTempMiscProp(gameconst.AvatarProps.taskAreaTarget)
        if not areaTaskDic:
            areaTaskDic = {}
            self.setTempMiscProp(gameconst.AvatarProps.taskAreaTarget, areaTaskDic)
        areaTaskDic.setdefault(target.mapId, {})
        areaTaskDic[target.mapId][taskId] = target
        self.tryStartAreaTaskCheckTimer()
        return

    def refreshAreaTaskTimer(self):
        self.tryStartAreaTaskCheckTimer()
        return

    def tryStartAreaTaskCheckTimer(self):
        if self.checkAreaTgtTaskTimer:
            return
        dungeonNo = formula.getDungeonNoBySpaceNo(self.spaceNo)
        areaTaskInCurDun = self.getTempMiscProp(gameconst.AvatarProps.taskAreaTarget, {}).get(dungeonNo)
        if not areaTaskInCurDun:
            return
        self.checkAreaTgtTaskTimer = self._callback(1, '_checkAreaTaskTarget', (),
                                                    gametimer.TIMER_TAG_CHECK_AREA_TARGET_TASK, 'checkAreaTgtTaskTimer')
        return

    def _checkAreaTaskTarget(self):
        self.checkAreaTgtTaskTimer = 0
        dungeonNo = formula.getDungeonNoBySpaceNo(self.spaceNo)
        areaTaskInCurDun = self.getTempMiscProp(gameconst.AvatarProps.taskAreaTarget, {}).get(dungeonNo, {})
        for taskId, target in areaTaskInCurDun.items():
            if target.isInArea(self.position[0], self.position[2]):
                self._taskReachArea(taskId)
        self.tryStartAreaTaskCheckTimer()
        return

    def removeAreaTargetTask(self, taskId, dungeonNo):
        INFO_MSG('removeAreaTargetTask:', taskId, dungeonNo)
        areaTaskDic = self.getTempMiscProp(gameconst.AvatarProps.taskAreaTarget, None)
        if areaTaskDic is None:
            WARNING_MSG('removeAreaTargetTask, areaTaskDic is None')
            return
        areaTaskDicInCurDun = areaTaskDic.get(dungeonNo, None)
        if areaTaskDicInCurDun is None:
            WARNING_MSG('removeAreaTargetTask, areaTaskDicInCurDun is None')
            return
        areaTaskDicInCurDun.pop(taskId, None)
        if not areaTaskDicInCurDun:
            areaTaskDic.pop(dungeonNo, None)
        if not areaTaskDic:
            self.popTempMiscProp(gameconst.AvatarProps.taskAreaTarget, None)
        return

    def checkKillMonsterTrigger(self, monsterId, monsterUID):
        monsterTaskIds = TMD.datas.get(str(monsterId))
        itemSrcTaskIds = TISD.datas.get(str(monsterId))
        if monsterTaskIds or itemSrcTaskIds:
            self.base.onTaskStepUpdate(gameconst.TaskTargetType.TASK_TARGET_MONSTERS, 0, (self.spaceNo, monsterId, monsterUID))

    def checkSameMap(self, taskID):
        INFO_MSG("checkSameMap ", taskID)
        taskData = dataUtils.getTaskData(taskID)
        if not taskData:
            ERROR_MSG("checkSameMap, missing task cfg ", taskID)
            return
        if not dataUtils.taskFieldVal(taskData, 'ClaimCanTransIns'):
            INFO_MSG("checkSameMap, no ClaimCanTransIns ", taskID)
            return
        claimTransData = dataUtils.taskFieldVal(taskData, 'ClaimTransInstance')
        dungeonNo = claimTransData.get('MapId')
        if dungeonNo is None:
            WARNING_MSG('checkSameMap, map id is None', taskID, claimTransData)
            return
        ret = dungeonNo == formula.getMapId(self.spaceNo)
        self.base.onCheckSameMap(taskID, ret)
