# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
import utils

import iLineSpaceStub
import iLinePlayersStub


class ILineStubBase(iLineSpaceStub.ILineSpaceStub, iLinePlayersStub.ILinePlayersStub):
    def __init__(self, **kwargs):
        iLineSpaceStub.ILineSpaceStub.__init__(self)
        iLinePlayersStub.ILinePlayersStub.__init__(self)

    def onLineSpaceGone(self, spaceNo, groupOrderNum):
        iLinePlayersStub.ILinePlayersStub.onLineSpaceGone(self, spaceNo, groupOrderNum)
        iLineSpaceStub.ILineSpaceStub.onLineSpaceGone(self, spaceNo, groupOrderNum)

    def onSpaceLineReady(self, spaceNo):
        iLinePlayersStub.ILinePlayersStub.onSpaceLineReady(self, spaceNo)
        iLineSpaceStub.ILineSpaceStub.onSpaceLineReady(self, spaceNo)

    def handleCellappDeath(self, groupOrderNum):
        iLinePlayersStub.ILinePlayersStub.handleCellappDeath(self, groupOrderNum)
        iLineSpaceStub.ILineSpaceStub.handleCellappDeath(self, groupOrderNum)

    def onCellappRelive(self, groupOrderNum):
        iLinePlayersStub.ILinePlayersStub.onCellappRelive(self, groupOrderNum)
        iLineSpaceStub.ILineSpaceStub.onCellappRelive(self, groupOrderNum)

    def onTimer(self, tid, userArg):
        self._onTimerTrigger(tid, userArg)
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
