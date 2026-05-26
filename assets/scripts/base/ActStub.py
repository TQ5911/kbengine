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
import gameconst
import activityControl_activityNotice as ACAN


class ActTimeType(object):
    OPEN = 1
    END = 2


class ActTimeVal(userType.UserSingleType):
    def __init__(self, actId, fireTime, fireType):
        self.actId = actId
        self.fireTime = fireTime
        self.fireType = fireType

    def __lt__(self, other):
        return self.fireTime < other.fireTime

    def __str__(self):
        return f'ActTimeVal(actId={self.actId}, fireTime={self.fireTime}, fireType={self.fireType})'

class AnnouncementVal(object):
    def __init__(self, aType, uaType, beginTime, endTime):
        self.aType = aType
        self.uaType = uaType
        self.beginTime = beginTime
        self.endTime = endTime
        self.beAnnouncement = False

    def needAnnouncement(self, now):
        return self.beginTime <= now < self.endTime

    def leftTime(self, now):
        return self.endTime - now
    
    def __str__(self):
        return f'AnnouncementVal(aType={self.aType}, uaType={self.uaType}, beginTime={self.beginTime}, endTime={self.endTime}, beAnnouncement={self.beAnnouncement})'


class ActStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer):
    def __init__(self):
        self.announcementDict = {}
        self.addDatetimeTimerTick()
        self._resetActData()

    def onTimer(self, tid, userArg):
        if userArg == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()
        elif userArg == gametimer.TIMER_CHECK_ANNOUNCEMENT:
            self.checkAnnouncement()
        else:
            self._onTimer(tid, userArg)

    def doNext(self):
        super().doNext()
        self.pyAddTimer(1, 2, gametimer.TIMER_CHECK_ANNOUNCEMENT)

    def _resetActData(self):
        now = utils.curTS()
        actGlobalData = {}
        self.actTimeQueue = []
        for actId, actData in AC_ADD.datas.items():
            if actData['isOpen'] == 0:
                continue

            openTimeCron = actData['openTimeCron']
            endTimeCron = actData['endTimeCron']

            nextOpenTime, _ = utils.nextByCronTupleList(openTimeCron)
            nextEndTime, _ = utils.nextByCronTupleList(endTimeCron)

            if not nextOpenTime and not nextEndTime:
                actGlobalData[actId] = 0
                continue

            nextOpenTime = now + nextOpenTime
            nextEndTime = now + nextEndTime

            LOG_DBG('init act data', actData['name'], nextOpenTime, nextEndTime)

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
        nextOpenTime, _ = utils.nextByCronTupleList(openTimeCron)
        return utils.curTS() + nextOpenTime

    def _getActNextEndTime(self, actId):
        actData = AC_ADD.datas.get(actId)
        if not actData:
            return 0

        endTimeCron = actData['endTimeCron']
        nextEndTime, _ = utils.nextByCronTupleList(endTimeCron)
        return utils.curTS() + nextEndTime

    def onActTimerCallback(self):
        if not self.actTimeQueue:
            return

        _val = heapq.heappop(self.actTimeQueue)
        LOG_DBG('onActTimerCallback', _val)
        if _val.fireType == ActTimeType.OPEN:
            _nextEndTime = self._getActNextEndTime(_val.actId)
            heapq.heappush(self.actTimeQueue, ActTimeVal(_val.actId, _nextEndTime, ActTimeType.END))
            gameengine.callAllApps('gameengine.modifyGlobalActData', (_val.actId, _nextEndTime))
        else:
            _nextOpenTime = self._getActNextOpenTime(_val.actId)
            heapq.heappush(self.actTimeQueue, ActTimeVal(_val.actId, _nextOpenTime, ActTimeType.OPEN))
            gameengine.callAllApps('gameengine.modifyGlobalActData', (_val.actId, 0))

        self._startActTimer()

    def updateAnnouncement(self, aType, uaType, triggerTime, endTime):
        now = utils.curTS()
        LOG_INFO('updateAnnouncement', now, aType, uaType, triggerTime, endTime)
        preShowTime = ACAN.datas.get(aType, {}).get('preShowTime', 0)

        advanceTime = 0
        if uaType in (gameconst.UpdateAnnouncementType.WORLD_BOSS1_UPCOMING, gameconst.UpdateAnnouncementType.WORLD_BOSS2_UPCOMING):
            advanceTime = gameconst.ONE_MINUTE_COST_SECONDS * preShowTime
        elif uaType in (gameconst.UpdateAnnouncementType.WORLD_BOSS1_ONGOING, gameconst.UpdateAnnouncementType.WORLD_BOSS2_ONGOING):
            advanceTime = gameconst.ONE_MINUTE_COST_SECONDS * preShowTime
            endTime += advanceTime
        elif uaType in (gameconst.UpdateAnnouncementType.MINE_WAR_UPCOMING, gameconst.UpdateAnnouncementType.MINE_WAR_ONGOING,
                        gameconst.UpdateAnnouncementType.SIEGE_WAR_BIDDING, gameconst.UpdateAnnouncementType.SIEGE_WAR_UPCOMING, gameconst.UpdateAnnouncementType.SIEGE_WAR_ONGOING):
            advanceTime = endTime - triggerTime
        else:
            LOG_ERR('updateAnnouncement unknown uaType', uaType)
            return
        announcementVal = AnnouncementVal(aType, uaType, endTime - advanceTime, endTime)
        self.announcementDict[uaType] = announcementVal
        LOG_DBG('updateAnnouncement val', announcementVal)

        if not announcementVal.needAnnouncement(now):
            return
        announcementVal.beAnnouncement = True
        LOG_DBG('updateAnnouncement send val', announcementVal)
        gameengine.broadcastBaseapp('onBroadcastToAllClients', ('onAnnouncement', (announcementVal.aType, announcementVal.uaType, announcementVal.endTime)))

    def checkAnnouncement(self):
        now = utils.curTS()
        for uaType, announcementVal in self.announcementDict.items():
            if announcementVal.beAnnouncement:
                continue
            if not announcementVal.needAnnouncement(now):
                continue
            announcementVal.beAnnouncement = True
            LOG_DBG('checkAnnouncement send val', announcementVal)
            gameengine.broadcastBaseapp('onBroadcastToAllClients', ('onAnnouncement', (announcementVal.aType, announcementVal.uaType, announcementVal.endTime)))

    def getAnnouncement(self, playerBox):
        now = utils.curTS()
        LOG_DBG('getAnnouncement', now)
        for uaType, announcementVal in self.announcementDict.items():
            self.sendAnnouncement(playerBox, announcementVal, now)

    def sendAnnouncement(self, playerBox, announcementVal, now):
        if not announcementVal.needAnnouncement(now):
            return
        LOG_DBG('sendAnnouncement val', announcementVal)
        playerBox.client.onAnnouncement(announcementVal.aType, announcementVal.uaType, announcementVal.endTime)

