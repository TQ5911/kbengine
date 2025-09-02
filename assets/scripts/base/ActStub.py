# coding: utf-8
import KBEngine
from KBEDebug import *
import iGlobal
import iBaseNoCell
import iTimer
import gametimer
import activityControl_activityData as AC_ADD
import utils
import gameengine
import heapq
import userType


class ActTimeType(object):
    OPEN = 1
    END = 2


class ActTimeVal(userType.UserSoleType):
    def __init__(self, actId, fireTime, fireType):
        self.actId = actId
        self.fireTime = fireTime
        self.fireType = fireType

    def __lt__(self, other):
        return self.fireTime < other.fireTime

    def __str__(self):
        return f'ActTimeVal(actId={self.actId}, fireTime={self.fireTime}, fireType={self.fireType})'


class ActStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer):
    def __init__(self):
        self.addDatetimeTimerTick()
        self._resetActData()

    def onTimer(self, tid, userArg):
        if userArg == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()
        else:
            self._onTimer(tid, userArg)

    def doNext(self):
        super().doNext()

    def _resetActData(self):
        now = utils.getNow()
        actGlobalData = {}
        self.actTimeQueue = []
        for actId, actData in AC_ADD.datas.items():
            if actData['isOpen'] == 0:
                continue

            openTimeCron = actData['openTimeCron']
            endTimeCron = actData['endTimeCron']

            nextOpenTime, _ = utils.nextByTimeTupleList(openTimeCron)
            nextEndTime, _ = utils.nextByTimeTupleList(endTimeCron)

            if not nextOpenTime and not nextEndTime:
                actGlobalData[actId] = 0
                continue

            nextOpenTime = now + nextOpenTime
            nextEndTime = now + nextEndTime

            DEBUG_MSG('init act data', actData['name'], nextOpenTime, nextEndTime)

            if nextOpenTime < nextEndTime:
                self.actTimeQueue.append(ActTimeVal(actId, nextOpenTime, ActTimeType.OPEN))
                continue

            actGlobalData[actId] = nextEndTime
            self.actTimeQueue.append(ActTimeVal(actId, nextEndTime, ActTimeType.END))

        gameengine.callAllApps('gameengine.resetGlobalActData', (actGlobalData,))

        heapq.heapify(self.actTimeQueue)
        self._startActTimer()

    def _startActTimer(self):
        if self.actTimerId:
            self._cancelDatetimeCallback(self.actTimerId, gametimer.TIMER_TAG_ACT_TIMER)
            self.actTimerId = 0

        if not self.actTimeQueue:
            return

        _val = heapq.nsmallest(1, self.actTimeQueue)[0]
        self.actTimerId = self._datetimeCallback(_val.fireTime, 'onActTimerCallback', (), gametimer.TIMER_TAG_ACT_TIMER, 'actTimerId')

    def _getActNextOpenTime(self, actId):
        actData = AC_ADD.datas.get(actId)
        if not actData:
            return 0

        openTimeCron = actData['openTimeCron']
        nextOpenTime, _ = utils.nextByTimeTupleList(openTimeCron)
        return utils.getNow() + nextOpenTime

    def _getActNextEndTime(self, actId):
        actData = AC_ADD.datas.get(actId)
        if not actData:
            return 0

        endTimeCron = actData['endTimeCron']
        nextEndTime, _ = utils.nextByTimeTupleList(endTimeCron)
        return utils.getNow() + nextEndTime

    def onActTimerCallback(self):
        if not self.actTimeQueue:
            return

        _val = heapq.heappop(self.actTimeQueue)
        DEBUG_MSG('onActTimerCallback', _val)
        if _val.fireType == ActTimeType.OPEN:
            _nextEndTime = self._getActNextEndTime(_val.actId)
            heapq.heappush(self.actTimeQueue, ActTimeVal(_val.actId, _nextEndTime, ActTimeType.END))
            gameengine.callAllApps('gameengine.modifyGlobalActData', (_val.actId, _nextEndTime))
        else:
            _nextOpenTime = self._getActNextOpenTime(_val.actId)
            heapq.heappush(self.actTimeQueue, ActTimeVal(_val.actId, _nextOpenTime, ActTimeType.OPEN))
            gameengine.callAllApps('gameengine.modifyGlobalActData', (_val.actId, 0))

        self._startActTimer()

