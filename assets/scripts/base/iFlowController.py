# coding: utf-8
from KBEDebug import *
import KBEngine


class IFlowController(object):

    def flowCtrlOnTaskComplete(self, taskId):
        self.cell.flowCtrlOnTaskComplete(taskId)

    def flowCtrlOnTaskFailed(self, taskId):
        self.cell.flowCtrlOnTaskFailed(taskId)

    def flowCtrlOnTaskInProgress(self, taskId):
        self.cell.flowCtrlOnTaskInProgress(taskId)

    def flowCtrlDungeonMonsterReleaseComplete(self, monsterGIDs):
        self.cell.flowCtrlDungeonMonsterReleaseComplete(monsterGIDs)

    def flowCtrlDungeonMonsterKillNumIncreased(self, monsterGID, newNumber, newTotalNumber):
        self.cell.flowCtrlDungeonMonsterKillNumIncreased(monsterGID, newNumber, newTotalNumber)

    def flowCtrlDungeonMonsterKillNumIncreasedByCreepbaseId(self, monsterId, newNumber, newTotalNumber):
        self.cell.flowCtrlDungeonMonsterKillNumIncreasedByCreepbaseId(monsterId, newNumber, newTotalNumber)