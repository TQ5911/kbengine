# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

import iBase
import formula
import gameconst
import gameengine


class WaitMapSpace(iBase.IBase):
    def __init__(self):
        super(WaitMapSpace, self).__init__()
        self.spacetype = formula.getSpaceType(self.spaceno)
        self.cellData['spaceType'] = self.spacetype

        self.createCellEntityInNewSpace(self.cellappIndex, 10)
        LOG_INFO('WaitMapSpace.__init__:', self.spaceno)

    def onGetCell(self):
        LOG_INFO('WaitMapSpace.onGetCell', self.spaceno, self.spacetype)
        if self.alreadyTrunk:
            self.onSpaceCellReady()

    def onLoseCell(self, reason=gameconst.OnLoseCellReasonEnum.DEFAULT):
        LOG_INFO("WaitMapSpace.onLoseCell:", self.spaceno, reason)
        if self.isDestroyed:
            return
        if reason:
            self.onLoseCellReason = reason
        stub = gameengine.getGlobalBase('WaitMapSpaceStub', reportErr=False)
        if stub:
            stub.onWaitMapSpaceGone(self.spaceno)
        self.doEntireDestroy(False, False)

    def onCreateCellFailure(self):
        LOG_ERR('WaitMapSpace.onCreateCellFailure~')
        self.destroy(deleteFromDB=False, writeToDB=False)

    def initCellField(self, spaceID):
        self.spaceid = spaceID

    def entireConstruct(self, spaceID):
        LOG_INFO('WaitMapSpace.entireConstruct', self.spaceno, spaceID)
        self.spaceid = spaceID
        if self.alreadyTrunk:
            return
        self.alreadyTrunk = True
        if self.cell:
            self.onSpaceCellReady()

    def onSpaceCellReady(self):
        if self.isNotifiedSpaceReady:
            return
        self.isNotifiedSpaceReady = True
        stub = gameengine.getGlobalBase('WaitMapSpaceStub', reportErr=False)
        if stub:
            stub.onWaitMapSpaceReady(self.spaceno)

    def doEntireDestroy(self, deleteFromDB, writeToDB):
        LOG_INFO("WaitMapSpace.doEntireDestroy ", self.spaceno)
        if self.isDestroyed:
            return
        if hasattr(self, 'cell') and self.cell:
            self.isDelFromDB = deleteFromDB
            self.isWriteToDB = writeToDB
            self.onLoseCellReason = gameconst.OnLoseCellReasonEnum.ENTIRE_DESTROY
            self.cell.destroyMySpace()
        else:
            self.destroy(deleteFromDB=deleteFromDB, writeToDB=writeToDB)

    def onTimer(self, tid, userData):
        self._onTimerTrigger(tid, userData)
