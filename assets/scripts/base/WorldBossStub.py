# coding=utf-8

import KBEngine
from KBEDebug import *

import iGlobal
import gametimer
import iBaseNoCell
import iTimer
import gameengine
import formula


class WorldBossStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer):
    def __init__(self):
        self.addDatetimeTimerTick()

    def getBossCreateTime(self, spaceNo, spaceMgrBoxCell):
        _createTime = self.createBossTimeDic.get(spaceNo, 0)
        spaceMgrBoxCell.onGetCreateBossTime(_createTime)

    def doNext(self):
        super().doNext()

    def onTimer(self, tid, userArg):
        if userArg == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()
        else:
            self._onTimer(tid, userArg)

    def addCreateWorldBossTimer(self, spaceNo, createTime):
        self._datetimeCallback(
            createTime,
            '_notifyCreateWorldBoss',
            (spaceNo,),
            gametimer.TIMER_TAG_CREATE_WORLD_BOSS)

    def _notifyCreateWorldBoss(self, spaceNo):
        _mapId = formula.getMapId(spaceNo)
        gameengine.getLineStub(_mapId).notifyCreateWorldBoss(spaceNo)

    def onWorldBossDeadAddTimer(self, spaceNo, nextCreateTime):
        self.createBossTimeDic[spaceNo] = nextCreateTime
        self.addCreateWorldBossTimer(spaceNo, nextCreateTime)


