# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

import formula
import gameconst
import gameengine
import gameglobal
import kbeUtils

import iCell
import iTimer


class WaitMapSpace(iCell.ICell, iTimer.ITimer):
    def __init__(self):
        LOG_INFO("WaitMapSpace::__init__~", self.spaceNo, self.spaceID, KBEngine.getComponentGroupOrder())
        gameglobal.localSpaceNoMap[self.spaceNo] = self
        gameglobal.localSpaceIDMap[self.spaceID] = self
        super(WaitMapSpace, self).__init__()
        self.base.initCellField(self.spaceID)

        self.spaceMap = formula.getSpaceMap(self.spaceNo)
        if not self.spaceMap and self.spaceNo:
            LOG_ERR("WaitMapSpace map is empty! %s %s" % (self.spaceNo, self.spaceID))

        if self.spaceMap:
            kbeUtils.addSpaceGeometryMapping(self.spaceID, None, self.spaceMap)

    def onSpaceGone(self):
        gameglobal.localSpaceNoMap.pop(self.spaceNo, None)
        gameglobal.localSpaceIDMap.pop(self.spaceID, None)
        self.destroy()
        return

    def onDestroy(self):
        super(WaitMapSpace, self).onDestroy()
        gameglobal.localSpaceNoMap.pop(self.spaceNo, None)
        gameglobal.localSpaceIDMap.pop(self.spaceID, None)

    def destroyMySpace(self):
        self.destroySpace()
        return

    def onTimer(self, tid, userData):
        self._onTimerTrigger(tid, userData)
