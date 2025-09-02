# -*- coding: utf-8 -*-

from KBEDebug import *

import gameengine
import gamebase
import gametimer

import iBaseNoCell
import iGlobal
import iTimer


class SpaceMapStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer):

    def __init__(self):
        super(SpaceMapStub, self).__init__()
        self.pyAddTimer(1, 0, gametimer.SPACE_MAP_STUB_READY)
        return

    def doNext(self):

        return

    def onTimer(self, timerID, userData):
        self._onTimer(timerID, userData)
        if userData == gametimer.SPACE_MAP_STUB_READY:
            self._doReady()
        return

    def _doReady(self):
        gameengine.setGlobalData(self.classname(), self)

    def regSpace(self, spaceID, mailbox):
        INFO_MSG('SpaceMapStub.regSpace: %s %s' % (spaceID, mailbox))
        self.spaceMap[spaceID] = mailbox

        if spaceID in self.loadedSet:
            INFO_MSG('SpaceMapStub.regSpace: loaded before regSpace: %s %s' % (spaceID, mailbox))
            self.spaceMap[spaceID].entireConstruct(spaceID)

    def unRegSpace(self, spaceID, mailbox):
        INFO_MSG('SpaceMapStub.unRegSpace %s %s' % (spaceID, mailbox))

        self.spaceMap.pop(spaceID, None)
        self.loadedSet.discard(spaceID)

    def entireConstruct(self, spaceID):
        INFO_MSG('SpaceMapStub.entireConstruct: %s' % spaceID)

        self.loadedSet.add(spaceID)
        s = self.spaceMap.get(spaceID)
        if s:
            s.entireConstruct(spaceID)
        else:
            INFO_MSG('SpaceMapStub.entireConstruct: loaded before regSpace %s' % spaceID)
