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


class EventTypeEnum(object):
    typeAmount = 5
    EVENT_NONE, EVENT_DAY, EVENT_WEEK, EVENT_MONTH, EVENT_HOUR = range(typeAmount)


class IBaseCycleEvent(object):
    """
    base cycle event class
    """
    eventType = EventTypeEnum.EVENT_NONE

    def __init__(self, owner, cbFunc, cbArg=(), cycleTime=gameconst.GENERAL_CYCLE_TIME):
        self.cbArg = cbArg
        self.cbFunc = cbFunc
        self.cycleTime = cycleTime
        self.tUpdateTime = self.getUpdateDict(owner).get(cbFunc, 0)
        if not self.tUpdateTime:
            self._calcNextCBTime()
            self.restoreUpdateDict(owner)

    def calcNextCBTime(self, owner):
        self._calcNextCBTime()
        self.restoreUpdateDict(owner)

    def getUpdateDict(self, owner):
        return None

    def __lt__(self, other):
        return self.tUpdateTime < other.tUpdateTime

    def restoreUpdateDict(self, owner):
        updateDict = self.getUpdateDict(owner)
        updateDict[self.cbFunc] = self.tUpdateTime


class CmpCycleEvent(IBaseCycleEvent):
    def __init__(self, updateTime):
        self.tUpdateTime = updateTime


class HourCycleEvent(IBaseCycleEvent):
    """
    hour cycle event class
    """
    eventType = EventTypeEnum.EVENT_HOUR

    def getUpdateDict(self, owner):
        return owner.tLastHourUpdateTimeDict

    def _calcNextCBTime(self):
        _tUpdate = utils.getCurHourTS(offsetSec=self.cycleTime)
        _tNow = time.time()
        if _tNow < _tUpdate:
            self.tUpdateTime = _tUpdate
        else:
            self.tUpdateTime = _tUpdate + gameconst.ONE_HOUR_COST_SECONDES


class DayCycleEvent(IBaseCycleEvent):
    """
    day cycle event class
    """
    eventType = EventTypeEnum.EVENT_DAY

    def getUpdateDict(self, owner):
        return owner.tLastDayUpdateTimeDict

    def _calcNextCBTime(self):
        tUpdate = utils.getCurDayTS(offsetSec=self.cycleTime)
        _tNow = time.time()
        if _tNow < tUpdate:
            self.tUpdateTime = tUpdate
        else:
            self.tUpdateTime = tUpdate + gameconst.ONE_DAY_COST_SECONDS


class WeekCycleEvent(IBaseCycleEvent):
    """
    week cycle event class
    """
    eventType = EventTypeEnum.EVENT_WEEK
    DEFAULT_REFRESH_WEEKDAY = 1

    def __init__(self, owner, cbFunc, cbArg=(),
                 cycleTime=gameconst.ONE_DAY_COST_SECONDS * (DEFAULT_REFRESH_WEEKDAY - 1) + gameconst.GENERAL_CYCLE_TIME):
        super(WeekCycleEvent, self).__init__(owner, cbFunc, cbArg, cycleTime)

    def _calcNextCBTime(self):
        tUpdate = utils.getCurWeekTS(offsetSec=self.cycleTime)
        _tNow = time.time()
        if _tNow < tUpdate:
            self.tUpdateTime = tUpdate
        else:
            self.tUpdateTime = tUpdate + gameconst.ONE_WEEK_COST_SECONDS

    def getUpdateDict(self, owner):
        return owner.tLastWeekUpdateTimeDict


class MonthCycleEvent(IBaseCycleEvent):
    """
    month cycle event class
    """
    eventType = EventTypeEnum.EVENT_MONTH

    def _calcNextCBTime(self):
        tUpdate = utils.getCurrentMonthTS() + self.cycleTime
        _tNow = time.time()
        if _tNow < tUpdate:
            self.tUpdateTime = tUpdate
        else:
            self.tUpdateTime = utils.getNextMonthTS(offsetSec=self.cycleTime)

    def getUpdateDict(self, owner):
        return owner.tLastMonthUpdateTimeDict


class ICycleEventMixin(object):
    """ 服务器循环时间类, 如需要继承改类需要注意一下问题:

    1. 需要实现 onTimer方法, e.g.

        class A(ICycleEventMixin):
            def onTimer(self, tid, userArg):
                if userArg == gametimer.TIMER_CYCLE_EVENT_TICK_TIMER:
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

    def _checkUpdateEvent(self):
        _nowTime = utils.curTS()
        LOG_DBG('myh _checkUpdateEvent', _nowTime, self.tLastUpdateTime)
        if self.tLastUpdateTime > 0:
            for eventObj in self.schemeEvent:
                bNeedUpdate = False
                if eventObj.eventType == EventTypeEnum.EVENT_HOUR:
                    if utils.checkDiffHour(_nowTime, self.tLastUpdateTime, eventObj.cycleTime):
                        bNeedUpdate = True
                elif eventObj.eventType == EventTypeEnum.EVENT_DAY:
                    if utils.checkDiffDay(_nowTime, self.tLastUpdateTime, eventObj.cycleTime):
                        bNeedUpdate = True
                elif eventObj.eventType == EventTypeEnum.EVENT_WEEK:
                    if utils.checkDiffWeek(_nowTime, self.tLastUpdateTime, eventObj.cycleTime):
                        bNeedUpdate = True
                elif eventObj.eventType == EventTypeEnum.EVENT_MONTH:
                    if utils.checkDiffMonth(_nowTime, self.tLastUpdateTime, eventObj.cycleTime):
                        bNeedUpdate = True
                if bNeedUpdate:
                    LOG_DBG('in _checkUpdateEvent', eventObj.eventType, eventObj.cbFunc)
                    try:
                        func = getattr(self, eventObj.cbFunc, None)
                        if func:
                            func(gameconst.CycleEventTriggerType.LOGIN, *eventObj.cbArg)
                    except Exception as e:
                        gameengine.panicStack("_checkUpdateEvent exception:", e, eventObj.cbFunc)

        self.tLastUpdateTime = _nowTime

    def initSchemeEvent(self):
        self.schemeEvent = []

    # 此函数在上线的时候和计时器时间到的时候(5点)触发
    def onDailyEvent(self):
        self._checkUpdateEvent()
        self.pyAddTimer(1, 60, gametimer.TIMER_CYCLE_EVENT_TICK_TIMER)

    def onCycleEventTick(self):
        _nowTime = utils.curTS()
        _cmpObj = CmpCycleEvent(_nowTime)
        heapq.heappush(self.schemeEvent, _cmpObj)
        isUpdate = False
        while self.schemeEvent:
            _newObj = heapq.heappop(self.schemeEvent)
            if _cmpObj.tUpdateTime < _newObj.tUpdateTime:
                heapq.heappush(self.schemeEvent, _newObj)
                break
            if _newObj is not _cmpObj:
                try:
                    getattr(self, _newObj.cbFunc)(gameconst.CycleEventTriggerType.TIMED, *_newObj.cbArg)
                except Exception as e:
                    gameengine.panicStack('onDailyEvent, exception:', e, _newObj.cbFunc)
                _newObj.calcNextCBTime(self)
                heapq.heappush(self.schemeEvent, _newObj)
                isUpdate = True
        if isUpdate:
            self.tLastUpdateTime = _nowTime

        if self.schemeEvent and not self.cycleEventCheckTimerId:
            _retObj = heapq.nsmallest(1, self.schemeEvent)[0]
            _remainTime = _retObj.tUpdateTime - _nowTime
            if _remainTime < 60:
                LOG_DBG('cb time:', time.localtime(_retObj.tUpdateTime), _nowTime)
                self.cycleEventCheckTimerId = self.addTimerCB(
                    _remainTime + random.random() * 5, 
                    '_onCycleEventTick',
                    (), 
                    gametimer.TIMER_TAG_CHECK_CYCLE_EVENT,
                    'cycleEventCheckTimerId')

    def _onCycleEventTick(self):
        _nowTime = utils.curTS()
        _cmpObj = CmpCycleEvent(_nowTime)
        heapq.heappush(self.schemeEvent, _cmpObj)
        isUpdate = False
        while self.schemeEvent:
            _newObj = heapq.heappop(self.schemeEvent)
            if _cmpObj.tUpdateTime < _newObj.tUpdateTime:
                heapq.heappush(self.schemeEvent, _newObj)
                break

            if _newObj is not _cmpObj:
                try:
                    getattr(self, _newObj.cbFunc)(gameconst.CycleEventTriggerType.TIMED, *_newObj.cbArg)
                except Exception as e:
                    gameengine.panicStack('onDailyEvent, exception:', e, _newObj.cbFunc)
                _newObj.calcNextCBTime(self)
                heapq.heappush(self.schemeEvent, _newObj)
                isUpdate = True
        if isUpdate:
            self.tLastUpdateTime = _nowTime

        self.cycleEventCheckTimerId = 0
        if self.schemeEvent:
            _retObj = heapq.nsmallest(1, self.schemeEvent)[0]
            remainTime = _retObj.tUpdateTime - _nowTime
            if remainTime < 60:
                LOG_DBG('cb time:', time.localtime(_retObj.tUpdateTime), _nowTime)
                self.cycleEventCheckTimerId = self.addTimerCB(remainTime + random.randint(1, 3), '_onCycleEventTick',
                                                             (), gametimer.TIMER_TAG_CHECK_CYCLE_EVENT,
                                                             'cycleEventCheckTimerId')

    def register_Event(self, eventType, cbFunc, cbArg=(), cycleTime=gameconst.GENERAL_CYCLE_TIME):
        if eventType == EventTypeEnum.EVENT_HOUR:
            evetObj = HourCycleEvent(self, cbFunc, cbArg, cycleTime)
        elif eventType == EventTypeEnum.EVENT_DAY:
            evetObj = DayCycleEvent(self, cbFunc, cbArg, cycleTime)
        elif eventType == EventTypeEnum.EVENT_WEEK:
            evetObj = WeekCycleEvent(self, cbFunc, cbArg, cycleTime)
        elif eventType == EventTypeEnum.EVENT_MONTH:
            evetObj = MonthCycleEvent(self, cbFunc, cbArg, cycleTime)
        else:
            return

        heapq.heappush(self.schemeEvent, evetObj)

    def registerHourlyEvent(self, cbFunc, cbArg=(), cycleTime=0):
        self.register_Event(EventTypeEnum.EVENT_HOUR, cbFunc, cbArg, cycleTime)

    def registerDailyEvent(self, cbFunc, cbArg=(), cycleTime=gameconst.GENERAL_CYCLE_TIME):
        self.register_Event(EventTypeEnum.EVENT_DAY, cbFunc, cbArg, cycleTime)

    # 默认周一的5点刷新
    def registerWeekEvent(self, cbFunc, cbArg=(), cycleTime=gameconst.ONE_DAY_COST_SECONDS * (
            WeekCycleEvent.DEFAULT_REFRESH_WEEKDAY - 1) + gameconst.GENERAL_CYCLE_TIME):
        self.register_Event(EventTypeEnum.EVENT_WEEK, cbFunc, cbArg, cycleTime)

    def registerMonthEvent(self, cbFunc, cbArg=(), cycleTime=gameconst.GENERAL_CYCLE_TIME):
        self.register_Event(EventTypeEnum.EVENT_MONTH, cbFunc, cbArg, cycleTime)
