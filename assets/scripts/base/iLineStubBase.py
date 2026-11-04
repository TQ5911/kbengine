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

    def onLineSpaceGone(self, spaceNo):
        iLinePlayersStub.ILinePlayersStub.onLineSpaceGone(self, spaceNo)
        iLineSpaceStub.ILineSpaceStub.onLineSpaceGone(self, spaceNo)

    def onSpaceLineReady(self, spaceNo):
        iLinePlayersStub.ILinePlayersStub.onSpaceLineReady(self, spaceNo)
        iLineSpaceStub.ILineSpaceStub.onSpaceLineReady(self, spaceNo)

    def handleCellappDeath(self, cellId):
        iLinePlayersStub.ILinePlayersStub.handleCellappDeath(self, cellId)
        iLineSpaceStub.ILineSpaceStub.handleCellappDeath(self, cellId)

    def onCellappRelive(self, cellId):
        iLinePlayersStub.ILinePlayersStub.onCellappRelive(self, cellId)
        iLineSpaceStub.ILineSpaceStub.onCellappRelive(self, cellId)

    def onTimer(self, tid, userArg):
        self._onTimerTrigger(tid, userArg)
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
