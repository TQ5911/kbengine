# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
import gameengine
import gameconfig
import gameglobal
import gameconst
import formula
import utils
import gametimer

import iLineSpaceStub
import iLinePlayersStub


class ILineStubBase(iLineSpaceStub.ILineSpaceStub, iLinePlayersStub.ILinePlayersStub):
    def __init__(self):
        iLineSpaceStub.ILineSpaceStub.__init__(self)
        iLinePlayersStub.ILinePlayersStub.__init__(self)

    def onLineSpaceReady(self, spaceNo):
        iLinePlayersStub.ILinePlayersStub.onLineSpaceReady(self, spaceNo)
        iLineSpaceStub.ILineSpaceStub.onLineSpaceReady(self, spaceNo)

    def onLineSpaceGone(self, spaceNo, groupOrder):
        iLinePlayersStub.ILinePlayersStub.onLineSpaceGone(self, spaceNo, groupOrder)
        iLineSpaceStub.ILineSpaceStub.onLineSpaceGone(self, spaceNo, groupOrder)

    def onCellappRelive(self, groupOrder):
        iLinePlayersStub.ILinePlayersStub.onCellappRelive(self, groupOrder)
        iLineSpaceStub.ILineSpaceStub.onCellappRelive(self, groupOrder)

    def handleCellappDeath(self, groupOrder):
        iLinePlayersStub.ILinePlayersStub.handleCellappDeath(self, groupOrder)
        iLineSpaceStub.ILineSpaceStub.handleCellappDeath(self, groupOrder)

    def onTimer(self, tid, userArg):
        self._onTimerTrigger(tid, userArg)
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
