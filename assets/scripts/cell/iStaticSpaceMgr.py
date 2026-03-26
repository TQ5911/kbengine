# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

import gametimer
import gameglobal
import iCell
import iTimer
import iSpaceMgr
import gameengine
import formula


class IStaticSpaceMgr(iCell.ICell, iTimer.ITimer, iSpaceMgr.ISpaceMgr):
    def __init__(self):
        INFO_MSG('IStaticSpaceMgr.__init__', self.spaceNo)
        iCell.ICell.__init__(self)
        iSpaceMgr.ISpaceMgr.__init__(self)
        self.addDatetimeTimerTick()

    def onTimer(self, tid, userData):
        if userData == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()
        else:
            self._onTimer(tid, userData)

    def initStaticSpace(self):
        _space = gameglobal.localSpaceIDMap[self.spaceID]
        _space.doLoadEntities(self.id)


