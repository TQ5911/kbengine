# coding: utf-8
from KBEDebug import *


class IFlowController(object):

    def flowCtrlOnTaskFailed(self, taskId):
        self.cell.flowCtrlOnTaskFailed(taskId)

    def flowCtrlOnTaskComplete(self, taskId):
        self.cell.flowCtrlOnTaskComplete(taskId)

    def flowCtrlDunMonsterReleaseComplete(self, monsterGIDs):
        self.cell.flowCtrlDunMonsterReleaseComplete(monsterGIDs)

    def flowCtrlOnTaskInProgress(self, taskId):
        self.cell.flowCtrlOnTaskInProgress(taskId)

    def flowCtrlDunMonsterKillNumIncByMonsterId(self, monsterId, newNumber, newTotalNumber):
        self.cell.flowCtrlDunMonsterKillNumIncByMonsterId(monsterId, newNumber, newTotalNumber)

    def flowCtrlDunMonsterKillNumInc(self, monsterGID, newNumber, newTotalNumber):
        self.cell.flowCtrlDunMonsterKillNumInc(monsterGID, newNumber, newTotalNumber)

