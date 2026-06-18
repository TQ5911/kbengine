# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
import formula
import gameengine
import iStaticSpaceMgr
import abyss_config as WL_CD
import creep_base as CBD
import utils
import random
import math
import gametimer
import iTimer
import gameconst
import branchData_set as BDS

class AbyssSpaceMgr(iStaticSpaceMgr.IStaticSpaceMgr):
    def __init__(self):
        LOG_INFO("AbyssSpaceMgr __init__")
        iStaticSpaceMgr.IStaticSpaceMgr.__init__(self)
        gameengine.getAbyssStubBySpaceNo(self.spaceNo).onSpaceMgrReady(self.spaceNo, self)
        self.fightingPlayersCnt = 0

    def onTimer(self, tid, userArg):
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        elif userArg == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()
        else:
            self._onTimerTrigger(tid, userArg)

    def initStaticSpace(self):
        super().initStaticSpace()

    def addEntity(self, entId, tags):
        entity = KBEngine.entities.get(entId, None)
        super(AbyssSpaceMgr, self).addEntity(entId, tags)

    def removeEntById(self, entId):
        super(AbyssSpaceMgr, self).removeEntById(entId)

    def onPlayerRelogin(self, box, playerGbId):
        super().onPlayerRelogin(box, playerGbId)

    def onPlayerEnter(self, pid):
        super(AbyssSpaceMgr, self).onPlayerEnter(pid)
        _ent = KBEngine.entities.get(pid)
        if not _ent:
            LOG_ERR("onPlayerEnter: _ent is None", pid)
            return

    def _statisticFightingCount(self):
        now = utils.curTS()
        lastCnt = self.fightingPlayersCnt
        self.fightingPlayersCnt = 0
        dt = BDS.datas["Branch_activePlayer"]["value"] * 60
        for pid in self.players:
            ent = KBEngine.entities.get(pid)
            if not ent:
                continue
            #5分钟内有进入过战斗视为"活跃用户"
            if now - ent.lastFightTime < dt:
                self.fightingPlayersCnt += 1

        if lastCnt != self.fightingPlayersCnt:
            gameengine.getAbyssStubBySpaceNo(self.spaceNo).onFightingPlayersCntSync(self.spaceNo, self.fightingPlayersCnt)
