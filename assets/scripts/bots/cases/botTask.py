import os
import sys
import threading
import random
import time
# sys.path.append('./scripts/common')
# sys.path.append('./scripts/common/Lib')
# sys.path.append('./scripts/server_common')

# import sMath

import BotClient
import botBase

import gameconst

import message_Message as MSGD
import taskdata as TD
import tasknpc as TND
import map_entities1 as MED
import mapRefresh_refresh1 as MRRD

# 86000001 
# [{'taskId': 86000001, 'taskType': 6, 'startTime': 1671869049, 'stat': 3, 'limitCount': 0, 'claimCount': 1, 'alreadyCount': 0, 'expiredTime': 0, 'parentTaskId': 0, 'extraJson': '{}', 'targets': []}, 
# {'taskId': 86000002, 'taskType': 6, 'startTime': 1671869049, 'stat': 3, 'limitCount': 0, 'claimCount': 0, 'alreadyCount': 0, 'expiredTime': 0, 'parentTaskId': 86000001, 'extraJson': '{}', 'targets': [
# {'tgtType': 3, 'tgtId': 18100044, 'stepCnt': 0, 'dstCnt': 1, 'cliExtra': ''}]
# }]


BOT_CONFIG = botBase.initBotConfig(__file__)

TGT_TYPE_NPC = "Npc"
TGT_TYPE_COLLECTION = "Collection"

ENTITY_TYPE_2_ID_KEY = {
    "Npc": "npcId",
    "Collection": "collectionId",
}

WORK_MODE_IDLE = 0
WORK_MODE_WALK = 1
WORK_MODE_DOING = 2


class PlayerDelegate(object):
    @property
    def player(self): return self.robot.player()
    @property
    def base(self): return self.player.base
    @property
    def cell(self): return self.player.cell
    @property
    def position(self): return self.player.position


    def __init__(self, robot, botCLient):
        self.robot = robot
        self.botClient = botCLient
        self.workMode = WORK_MODE_IDLE
        self.curTaskId = 0
        self.taskInfo = {}
        self.posData = self.initPosData()

    def update(self):
        print("update")

    def initPosData(self):
        posData = {}
        for _, data in MED.datas.items():
            entityType = data.get("entityType", "Npc")
            props = data.get("props", {})
            entityId = props.get(ENTITY_TYPE_2_ID_KEY.get(entityType, ""),  0)
            refreshGroup = data.get("refreshGroup", 0)
            refreshPolicyId = data.get("refreshPolicyId", 0)
            if refreshGroup:
                mrrd = MRRD.datas.get(refreshGroup, {})
            else:
                mrrd = MRRD.datas.get(refreshPolicyId, {})
            position = mrrd.get("position", [])
            if entityType not in posData:
                posData[entityType] = {}
            posData[entityType][entityId] = position
        return posData

    def onBecomePlayer(self):
        print('onBecomePlayer')

    def onTeleportDone(self, *args):
        print('onTeleportDone')

    def onGetStreamData(self, dataTypeId, jsonData):
        if dataTypeId == gameconst.StreamStringID.TASK_LIST_DATA:
            taskList = jsonData.get("taskList", [])
            self._updateTask(taskList)
        

    def onMessage(self, *args):
        print('onMessage', args)

    def getTargetPos(self, tgtType, tgtId):
        tgtPoss = self.posData.get(tgtType, {}).get(tgtId, None)
        if not tgtPoss:
            print("error not find tgtPos %s %s" % (tgtType, tgtId))
            tgtPos = self.position
        else:
            tgtPos = random.choice(tgtPoss)
        print("getTargetPos ", tgtType, tgtId, tgtPos)
        return tgtPos

    def moveTo(self, position):
        print('moveTo', position)
        if self._checkNearBy(position, 1):
            return
        self.workMode = WORK_MODE_WALK
        self.cell.botMoveTo(position)
    
    def onMoveOver(self, *args):
        self.workMode = WORK_MODE_IDLE

    def moveToEveTarget(self, tgtType, tgtId):
        tgtPos = self.getTargetPos(tgtType, tgtId)
        self.moveTo(tgtPos)
        return tgtPos

    def _checkNearBy(self, targetPos, dstDis=3):
        return self.player._checkNearBy(targetPos, dstDis)

    def _isRootTask(self, taskVal):
        parentTaskId = taskVal.get("parentTaskId", 0)
        return parentTaskId == 0

    def _updateTask(self, taskList):
        for taskVal in taskList:
            taskId = taskVal.get("taskId", 0)
            self.taskInfo[taskId] = taskVal

    #获得下一个未完成的任务目标
    def _getNextTaskTarget(self, taskVal):
        targets = taskVal.get("targets", [])
        if targets:
            for target in targets:
                stepCnt = target.get("stepCnt", 0)
                dstCnt = target.get("dstCnt", 0)
                if stepCnt < dstCnt:
                    return target
        return None


    def _getTaskState(self, taskVal):
        state =  taskVal.get("stat", 0)
        return state

    def _getNextTask(self):
        for taskVal in self.taskInfo:
            state = self._getTaskState(taskVal)
            if state in (gameconst.TaskStat.TASK_STAT_RUNNING,):
                self.curTaskId = taskVal.get('taskId', 0)
                return
        self.curTaskId = 0
    
    def _getConFinDialogId(self, taskId, npcId):
        td = TD.datas.get(str(taskId), {})
        FinCondFinDialogs = td.get("FinCondFinDialogs", {})
        DialogId = 0
        for condFinDialog in FinCondFinDialogs:
            NPCId = int(condFinDialog.get("NPCId", 0))
            if NPCId == npcId:
                DialogId = int(condFinDialog.get("DialogId", 0)) * 1000
                break
        return DialogId

    def getEntityByClass(self, entityType, tgtId):
        key = ENTITY_TYPE_2_ID_KEY.get(entityType, "")
        for e in self.robot.entities.values():
            if e.className == entityType and getattr(e, key) == tgtId:
                return e.id, e
        return 0, None

    def talkToNpc(self, npcEntityId, taskId, dialogId, idx):
        self.cell.talkToNpc(npcEntityId, taskId, dialogId, idx)

    def reqUpdateTaskByTalkToNpc(self, opType, npcEntityId, taskId, dialogId):
        self.cell.reqUpdateTaskByTalkToNpc(opType, npcEntityId, taskId, dialogId)

    def updateCurTask(self):
        # if not self._isRootTask(taskVal) and not self.curTaskId:
        #         self.curTaskId = taskId
        # if self.curTaskId:
        #     self.doTask()
        pass

    def doTask(self):
        taskId = self.curTaskId
        if not taskId:
            self.workMode = WORK_MODE_IDLE
            return
        taskVal = self.taskInfo.get(taskId, {})
        target = self._getNextTaskTarget(taskVal)
        tgtType = target.get("tgtType", 0)
        tgtId = target.get("tgtId", 0)
        stepCnt = target.get("stepCnt", 0)
        dstCnt = target.get("dstCnt", 0)
        if tgtType == gameconst.TaskTargetType.TASK_TARGET_ITEMS:
            pass
        elif tgtType == gameconst.TaskTargetType.TASK_TARGET_TALK_NPC:
            tgtPos = self.moveToEveTarget(TGT_TYPE_NPC, tgtId)
            if self._checkNearBy(tgtPos):
                opType = gameconst.TaskOpTypeByTalkToPNC.NPC_TALK_TARGET
                npcEntityId, _ = self.getEntityByClass(TGT_TYPE_NPC, tgtId)
                dialogId = self._getConFinDialogId(taskId, tgtId)
                self.reqUpdateTaskByTalkToNpc(opType, npcEntityId, taskId, dialogId)
        elif tgtType == gameconst.TaskTargetType.TASK_TARGET_REACH_AREA:
            pass
        elif tgtType == gameconst.TaskTargetType.TASK_TARGET_COLLECT:
            pass

    def onTaskUpdate(self, taskVals):
        print("onTaskUpdate ", taskVals)
        self._updateTask(taskVals)
        

    def onClaimTask(self, taskId, taskVals):
        print("onClaimTask ", taskId, taskVals)
        self._updateTask(taskVals)

        
    def onTasksRem(self, taskIds):
        for taskId in taskIds:
            self.taskInfo.pop(taskId, None)
        print("onTasksRem ", taskIds)


DELEGATE_CLS=PlayerDelegate







def botLogin():
    client = BotClient.BotClient('testBot1')
    robot = client.login()
    robot.setPlayerDelegate(PlayerDelegate(robot, client))
    return robot, client, robot.getPlayerDelegate()