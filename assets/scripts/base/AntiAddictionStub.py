# coding: utf-8
import KBEngine
from KBEDebug import *
import iGlobal
import iBaseNoCell
import iTimer
import gametimer
import utils
import gameengine
import heapq
import gameconst
import userType
import gameglobal
import antiAddictionSystem_config as AASC
import antiAddictionSystem_holiday as AASCH
import antiAddictionSystem_workday as AASCW

class AntiAddictionTimeVal(userType.UserSingleType):
    def __init__(self):
        self.dateType = gameconst.AntiAddictionDateType.WORKDAY
        self.timeType = gameconst.AntiAddictionTimeType.PROHIBIT
        self.nextStartTime = 0

    def __str__(self):
        return f'AntiAddictionTimeVal(dateType={self.dateType}, timeType={self.timeType}, nextStartTime={self.nextStartTime}, nextStartTimeStr={utils.getNowTimeStr(self.nextStartTime)})'

class AntiAddictionStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer):
    def __init__(self):
        self.permitTimeLimitList = [[[], []], [[], []]]
        self.antiAddictionTimeVal = AntiAddictionTimeVal()
        self.switchTimeTypeTimerId = 0
        self.initDatetimeTimerTick()
        self.initAntiAddictionData(utils.curTS())

    def onTimer(self, tid, userArg):
        if userArg == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()
        else:
            self._onTimerTrigger(tid, userArg)

    def doNext(self):
        super().doNext()

    def initAntiAddictionData(self, now):
        LOG_INFO("_resetAntiAddictionData")

        self.permitTimeLimitList = [[[], []], [[], []]]
        for id, holidayData in AASCH.datas.items():
            timeDateStart = holidayData['timeDateStart']
            timeDateEnd = holidayData['timeDateEnd']
            for data in timeDateStart:
                self.permitTimeLimitList[gameconst.AntiAddictionDateType.HOLIDAY][gameconst.AntiAddictionTimeType.PERMIT].append(data)
            for data in timeDateEnd:
                self.permitTimeLimitList[gameconst.AntiAddictionDateType.HOLIDAY][gameconst.AntiAddictionTimeType.PROHIBIT].append(data)

        allowedPeriodDayStart = AASC.datas.get('allowedPeriodDayStart', {}).get('value')
        allowedPeriodDayEnd = AASC.datas.get('allowedPeriodDayEnd', {}).get('value')
        for data in allowedPeriodDayStart:
            self.permitTimeLimitList[gameconst.AntiAddictionDateType.WEEKEND][gameconst.AntiAddictionTimeType.PERMIT].append(data)
        for data in allowedPeriodDayEnd:
            self.permitTimeLimitList[gameconst.AntiAddictionDateType.WEEKEND][gameconst.AntiAddictionTimeType.PROHIBIT].append(data)

        permitDateType, startPermitTimeCron, nextStartPermitTime = self.getNextTime(gameconst.AntiAddictionTimeType.PERMIT, now)
        prohibitDateType, startProhibitTimeCron, nextStartProhibitTime = self.getNextTime(gameconst.AntiAddictionTimeType.PROHIBIT, now)
        if nextStartPermitTime < nextStartProhibitTime:
            self.antiAddictionTimeVal.dateType = permitDateType
            self.antiAddictionTimeVal.timeType = gameconst.AntiAddictionTimeType.PROHIBIT
            self.antiAddictionTimeVal.nextStartTime = nextStartPermitTime
        else:
            self.antiAddictionTimeVal.dateType = prohibitDateType
            self.antiAddictionTimeVal.timeType = gameconst.AntiAddictionTimeType.PERMIT
            self.antiAddictionTimeVal.nextStartTime = nextStartProhibitTime

        gameglobal.localBaseApp.updateAntiAddictionData(self.antiAddictionTimeVal.timeType, int(self.antiAddictionTimeVal.nextStartTime))
        gameengine.callAllApps('gameengine.updateAntiAddictionData', (self.antiAddictionTimeVal.timeType, int(self.antiAddictionTimeVal.nextStartTime)))
        self.startSwitchTimeTypeTimer()

    def getNextTime(self, timeType, now):
        holidayTimeCron = sys.maxsize
        if self.permitTimeLimitList[gameconst.AntiAddictionDateType.HOLIDAY][timeType]:
            holidayTimeCron, _ = utils.nextByCronTupleList(self.permitTimeLimitList[gameconst.AntiAddictionDateType.HOLIDAY][timeType], now)
        nextStartHolidayTime = now + holidayTimeCron

        weekendTimeCron = sys.maxsize
        nextStartWeekendTime = now
        if self.permitTimeLimitList[gameconst.AntiAddictionDateType.WEEKEND][timeType]:
            cycCnt = int(len(AASCW.datas))
            curCnt = 1
            while True and curCnt <= cycCnt:
                curCnt += 1
                weekendTimeCron, _ = utils.nextByCronTupleList(self.permitTimeLimitList[gameconst.AntiAddictionDateType.WEEKEND][timeType], nextStartWeekendTime)
                nextStartWeekendTime = nextStartWeekendTime + weekendTimeCron
                if not AntiAddictionStub.isWorkDay(nextStartWeekendTime):
                    break

        if holidayTimeCron <= weekendTimeCron:
            return gameconst.AntiAddictionDateType.HOLIDAY, holidayTimeCron, nextStartHolidayTime
        return  gameconst.AntiAddictionDateType.WEEKEND, weekendTimeCron, nextStartWeekendTime
    
    def startSwitchTimeTypeTimer(self):
        if self.switchTimeTypeTimerId:
            self._cancelDatetimeCallback(self.switchTimeTypeTimerId, gametimer.TIMER_TAG_SWITCH_ANIT_ADDICTION_TIME_TYPE_TIMER)
            self.switchTimeTypeTimerId = 0

        LOG_INFO("startSwitchTimeTypeTimer", self.antiAddictionTimeVal)
        self.switchTimeTypeTimerId = self._datetimeCallback(self.antiAddictionTimeVal.nextStartTime, 'onSwitchTimeTypeTimerCallback', (), gametimer.TIMER_TAG_SWITCH_ANIT_ADDICTION_TIME_TYPE_TIMER, 'switchTimeTypeTimerId')

    def onSwitchTimeTypeTimerCallback(self):
        LOG_INFO("onSwitchTimeTypeTimerCallback", self.antiAddictionTimeVal)
        now = utils.curTS()
        if self.antiAddictionTimeVal.timeType == gameconst.AntiAddictionTimeType.PERMIT:
            permitDateType, startPermitTimeCron, nextStartPermitTime = self.getNextTime(gameconst.AntiAddictionTimeType.PERMIT, now)
            self.antiAddictionTimeVal.dateType = permitDateType
            self.antiAddictionTimeVal.timeType = gameconst.AntiAddictionTimeType.PROHIBIT
            self.antiAddictionTimeVal.nextStartTime = nextStartPermitTime
        elif self.antiAddictionTimeVal.timeType == gameconst.AntiAddictionTimeType.PROHIBIT:
            prohibitDateType, startProhibitTimeCron, nextStartProhibitTime = self.getNextTime(gameconst.AntiAddictionTimeType.PROHIBIT, now)
            self.antiAddictionTimeVal.dateType = prohibitDateType
            self.antiAddictionTimeVal.timeType = gameconst.AntiAddictionTimeType.PERMIT
            self.antiAddictionTimeVal.nextStartTime = nextStartProhibitTime

        gameglobal.localBaseApp.updateAntiAddictionData(self.antiAddictionTimeVal.timeType, int(self.antiAddictionTimeVal.nextStartTime))
        gameengine.callAllApps('gameengine.updateAntiAddictionData', (self.antiAddictionTimeVal.timeType, int(self.antiAddictionTimeVal.nextStartTime)))
        self.startSwitchTimeTypeTimer()

    @staticmethod
    def isWorkDay(timestamp):
        dateStr = utils.getCommonTimeStrFromTimeStamp(timestamp)
        date = int(dateStr[:8])
        LOG_DBG("isWorkDay timestamp=%d, dateStr=%s, date=%d" % (timestamp, dateStr, date))
        return date in AASCW.datas
