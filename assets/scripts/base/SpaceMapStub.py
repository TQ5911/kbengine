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
        self._onTimerTrigger(timerID, userData)
        if userData == gametimer.SPACE_MAP_STUB_READY:
            self._doReady()
        return

    def _doReady(self):
        gameengine.setGlobalData(self.classname(), self)

    def regSpace(self, spaceID, mailbox):
        LOG_INFO('SpaceMapStub.regSpace: %s %s' % (spaceID, mailbox))
        self.spaceMap[spaceID] = mailbox

        if spaceID in self.loadedSet:
            LOG_INFO('SpaceMapStub.regSpace: loaded before regSpace: %s %s' % (spaceID, mailbox))
            self.spaceMap[spaceID].entireConstruct(spaceID)

    def unRegSpace(self, spaceID, mailbox):
        LOG_INFO('SpaceMapStub.unRegSpace %s %s' % (spaceID, mailbox))

        self.spaceMap.pop(spaceID, None)
        self.loadedSet.discard(spaceID)

    def entireConstruct(self, spaceID):
        LOG_INFO('SpaceMapStub.entireConstruct: %s' % spaceID)

        self.loadedSet.add(spaceID)
        s = self.spaceMap.get(spaceID)
        if s:
            s.entireConstruct(spaceID)
        else:
            LOG_INFO('SpaceMapStub.entireConstruct: loaded before regSpace %s' % spaceID)
