# -*- coding: utf-8 -*-

import KBEngine

from KBEDebug import *

import utils
import time
import random
import heapq
import gameconst
import gameengine
import gametimer


class EventType(object):
    typeAmount = 5
    EVENT_NONE, EVENT_DAY, EVENT_WEEK, EVENT_MONTH, EVENT_HOUR = range(typeAmount)


class IBaseCycleEvent(object):
    """
    base cycle event class
    """
    eventType = EventType.EVENT_NONE

    def __init__(self, owner, cbFunc, cbArg=(), cycleTime=gameconst.GENERAL_CYCLE_TIME):
        self.cbFunc = cbFunc
        self.cbArg = cbArg
        self.tUpdateTime = self.getUpdateDict(owner).get(cbFunc, 0)
        self.cycleTime = cycleTime
        if not self.tUpdateTime:
            self._calcNextCBTime()
            self.restoreUpdateDict(owner)

    def getUpdateDict(self, owner):
        return None

    def calcNextCBTime(self, owner):
        self._calcNextCBTime()
        self.restoreUpdateDict(owner)

    def restoreUpdateDict(self, owner):
        updateDict = self.getUpdateDict(owner)
        updateDict[self.cbFunc] = self.tUpdateTime

    def __lt__(self, other):
        return self.tUpdateTime < other.tUpdateTime


class CmpCycleEvent(IBaseCycleEvent):
    def __init__(self, updateTime):
        self.tUpdateTime = updateTime


class HourCycleEvent(IBaseCycleEvent):
    """
    hour cycle event class
    """
    eventType = EventType.EVENT_HOUR

    def getUpdateDict(self, owner):
        return owner.tLastHourUpdateTimeDict

    def _calcNextCBTime(self):
        tUpdate = utils.getCurHourTS(offsetSec=self.cycleTime)
        tNow = time.time()
        if tNow < tUpdate:
            self.tUpdateTime = tUpdate
        else:
            self.tUpdateTime = tUpdate + gameconst.ONE_HOUR_COST_SECONDES


class DayCycleEvent(IBaseCycleEvent):
    """
    day cycle event class
    """
    eventType = EventType.EVENT_DAY

    def getUpdateDict(self, owner):
        return owner.tLastDayUpdateTimeDict

    def _calcNextCBTime(self):
        tUpdate = utils.getCurDayTS(offsetSec=self.cycleTime)
        tNow = time.time()
        if tNow < tUpdate:
            self.tUpdateTime = tUpdate
        else:
            self.tUpdateTime = tUpdate + gameconst.ONE_DAY_COST_SECONDS


class WeekCycleEvent(IBaseCycleEvent):
    """
    week cycle event class
    """
    eventType = EventType.EVENT_WEEK
    DEFAULT_REFRESH_WEEKDAY = 1

    def __init__(self, owner, cbFunc, cbArg=(),
                 cycleTime=gameconst.ONE_DAY_COST_SECONDS * (DEFAULT_REFRESH_WEEKDAY - 1) + gameconst.GENERAL_CYCLE_TIME):
        super(WeekCycleEvent, self).__init__(owner, cbFunc, cbArg, cycleTime)

    def getUpdateDict(self, owner):
        return owner.tLastWeekUpdateTimeDict

    def _calcNextCBTime(self):
        tUpdate = utils.getCurWeekTS(offsetSec=self.cycleTime)
        tNow = time.time()
        if tNow < tUpdate:
            self.tUpdateTime = tUpdate
        else:
            self.tUpdateTime = tUpdate + gameconst.ONE_WEEK_COST_SECONDS


class MonthCycleEvent(IBaseCycleEvent):
    """
    month cycle event class
    """
    eventType = EventType.EVENT_MONTH

    def getUpdateDict(self, owner):
        return owner.tLastMonthUpdateTimeDict

    def _calcNextCBTime(self):
        tUpdate = utils.getCurrentMonthTS() + self.cycleTime
        tNow = time.time()
        if tNow < tUpdate:
            self.tUpdateTime = tUpdate
        else:
            self.tUpdateTime = utils.getNextMonthTS(offsetSec=self.cycleTime)


class ICycleEvent(object):
    """ 服务器循环时间类, 如需要继承改类需要注意一下问题:

    1. 需要实现 onTimer方法, e.g.

        class A(ICycleEvent):
            def onTimer(self, tid, userArg):
                if userArg == gametimer.CYCLE_EVENT_TICK_TIMER:
                    self.onCycleEventTick()
                else:
                    super().onTimer(tid, userArg)
                    ...

    2. 需要在初测玩事件后调用 onDailyEvent方法进行commit, e.g.

        def regAll(self, ...):
            self.registerDailyEvent(...)
            self.registerWeekEvent(...)
            self.registerMonthEvent(...)

            # finally
            # DO NOT REGITST ANY NEW EVENT AFTER THIS METHOD.
            self.onDailyEvent()

            # DO NOT REG. HERE
            # self.registerDailyEvent(...)
            # ...

    """

    def __init__(self):
        self.initSchemeEvent()

    def initSchemeEvent(self):
        self.schemeEvent = []

    def _checkUpdateEvent(self):
        nowTime = utils.curTS()
        LOG_DBG('myh _checkUpdateEvent', nowTime, self.tLastUpdateTime)
        if self.tLastUpdateTime > 0:
            for eventObj in self.schemeEvent:
                bNeedUpdate = False
                if eventObj.eventType == EventType.EVENT_HOUR:
                    if utils.checkDiffHour(nowTime, self.tLastUpdateTime, eventObj.cycleTime):
                        bNeedUpdate = True
                elif eventObj.eventType == EventType.EVENT_DAY:
                    if utils.checkDiffDay(nowTime, self.tLastUpdateTime, eventObj.cycleTime):
                        bNeedUpdate = True
                elif eventObj.eventType == EventType.EVENT_WEEK:
                    if utils.checkDiffWeek(nowTime, self.tLastUpdateTime, eventObj.cycleTime):
                        bNeedUpdate = True
                elif eventObj.eventType == EventType.EVENT_MONTH:
                    if utils.checkDiffMonth(nowTime, self.tLastUpdateTime, eventObj.cycleTime):
                        bNeedUpdate = True
                if bNeedUpdate:
                    LOG_DBG('in _checkUpdateEvent', eventObj.eventType, eventObj.cbFunc)
                    try:
                        func = getattr(self, eventObj.cbFunc, None)
                        func and func(gameconst.CycleEventTriggerType.LOGIN, *eventObj.cbArg)
                    except Exception as e:
                        gameengine.panicStack("_checkUpdateEvent exception:", e, eventObj.cbFunc)

        self.tLastUpdateTime = nowTime

    # 此函数在上线的时候和计时器时间到的时候(5点)触发
    def onDailyEvent(self):
        self._checkUpdateEvent()
        self.pyAddTimer(1, 60, gametimer.CYCLE_EVENT_TICK_TIMER)

    def onCycleEventTick(self):
        nowTime = utils.curTS()
        cmpObj = CmpCycleEvent(nowTime)
        heapq.heappush(self.schemeEvent, cmpObj)
        isUpdate = False
        while self.schemeEvent:
            newObj = heapq.heappop(self.schemeEvent)
            if cmpObj.tUpdateTime < newObj.tUpdateTime:
                heapq.heappush(self.schemeEvent, newObj)
                break
            if newObj is not cmpObj:
                try:
                    getattr(self, newObj.cbFunc)(gameconst.CycleEventTriggerType.TIMED, *newObj.cbArg)
                except Exception as e:
                    gameengine.panicStack('onDailyEvent, exception:', e, newObj.cbFunc)
                newObj.calcNextCBTime(self)
                heapq.heappush(self.schemeEvent, newObj)
                isUpdate = True
        if isUpdate:
            self.tLastUpdateTime = nowTime

        if self.schemeEvent and not self.cycleEventCheckTimerId:
            retObj = heapq.nsmallest(1, self.schemeEvent)[0]
            remainTime = retObj.tUpdateTime - nowTime
            if remainTime < 60:
                LOG_DBG('cb time:', time.localtime(retObj.tUpdateTime), nowTime)
                self.cycleEventCheckTimerId = self.addTimerCB(remainTime + random.random() * 5, '_onCycleEventTick',
                                                             (), gametimer.TIMER_TAG_CYCLE_EVENT_CHECK,
                                                             'cycleEventCheckTimerId')

    def _onCycleEventTick(self):
        nowTime = utils.curTS()
        cmpObj = CmpCycleEvent(nowTime)
        heapq.heappush(self.schemeEvent, cmpObj)
        isUpdate = False
        while self.schemeEvent:
            newObj = heapq.heappop(self.schemeEvent)
            if cmpObj.tUpdateTime < newObj.tUpdateTime:
                heapq.heappush(self.schemeEvent, newObj)
                break

            if newObj is not cmpObj:
                try:
                    getattr(self, newObj.cbFunc)(gameconst.CycleEventTriggerType.TIMED, *newObj.cbArg)
                except Exception as e:
                    gameengine.panicStack('onDailyEvent, exception:', e, newObj.cbFunc)
                newObj.calcNextCBTime(self)
                heapq.heappush(self.schemeEvent, newObj)
                isUpdate = True
        if isUpdate:
            self.tLastUpdateTime = nowTime

        self.cycleEventCheckTimerId = 0
        if self.schemeEvent:
            retObj = heapq.nsmallest(1, self.schemeEvent)[0]
            remainTime = retObj.tUpdateTime - nowTime
            if remainTime < 60:
                LOG_DBG('cb time:', time.localtime(retObj.tUpdateTime), nowTime)
                self.cycleEventCheckTimerId = self.addTimerCB(remainTime + random.randint(1, 3), '_onCycleEventTick',
                                                             (), gametimer.TIMER_TAG_CYCLE_EVENT_CHECK,
                                                             'cycleEventCheckTimerId')

    def register_Event(self, eventType, cbFunc, cbArg=(), cycleTime=gameconst.GENERAL_CYCLE_TIME):
        if eventType == EventType.EVENT_HOUR:
            evetObj = HourCycleEvent(self, cbFunc, cbArg, cycleTime)
        elif eventType == EventType.EVENT_DAY:
            evetObj = DayCycleEvent(self, cbFunc, cbArg, cycleTime)
        elif eventType == EventType.EVENT_WEEK:
            evetObj = WeekCycleEvent(self, cbFunc, cbArg, cycleTime)
        elif eventType == EventType.EVENT_MONTH:
            evetObj = MonthCycleEvent(self, cbFunc, cbArg, cycleTime)
        else:
            return

        heapq.heappush(self.schemeEvent, evetObj)

    def registerHourlyEvent(self, cbFunc, cbArg=(), cycleTime=0):
        self.register_Event(EventType.EVENT_HOUR, cbFunc, cbArg, cycleTime)

    def registerDailyEvent(self, cbFunc, cbArg=(), cycleTime=gameconst.GENERAL_CYCLE_TIME):
        self.register_Event(EventType.EVENT_DAY, cbFunc, cbArg, cycleTime)

    # 默认周一的5点刷新
    def registerWeekEvent(self, cbFunc, cbArg=(), cycleTime=gameconst.ONE_DAY_COST_SECONDS * (
            WeekCycleEvent.DEFAULT_REFRESH_WEEKDAY - 1) + gameconst.GENERAL_CYCLE_TIME):
        self.register_Event(EventType.EVENT_WEEK, cbFunc, cbArg, cycleTime)

    def registerMonthEvent(self, cbFunc, cbArg=(), cycleTime=gameconst.GENERAL_CYCLE_TIME):
        self.register_Event(EventType.EVENT_MONTH, cbFunc, cbArg, cycleTime)
