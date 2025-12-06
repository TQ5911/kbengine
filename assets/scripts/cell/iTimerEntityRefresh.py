# coding: utf-8
import KBEngine
from KBEDebug import *
import utils
import heapq
import userType
import gametimer
import gameconst
import creep_base
import creep_timedRefresh as CTR

class TimerEntityVal(userType.UserSoleType):
    def __init__(self, refreshTimedID, nextStartTime, interval, refreshDataList):
        self.refreshTimedID = refreshTimedID
        self.nextStartTime = nextStartTime
        self.interval = interval
        self.refreshDataList = refreshDataList

    def __lt__(self, other):
        return self.nextStartTime < other.nextStartTime

    def __str__(self):
        return f'TimerEntityVal(refreshTimedID={self.refreshTimedID}, nextStartTime={self.nextStartTime}, interval={self.interval}, refreshDataList={self.refreshDataList}, nextStartTimeStr={utils.getTimeStrFromTimeStamp(self.nextStartTime)})'

class ITimerEntityRefresh(object):
    def __init__(self):
        self.refreshEntityQueue = []
        self.refreshEntityTimerId = 0

    def initTimerEntities(self, space, readyTimerEntitiesMap):
        if not readyTimerEntitiesMap:
            return

        DEBUG_MSG("initTimerEntities readyTimerEntitiesMap", readyTimerEntitiesMap)
        now = utils.getNow()
        for refreshTimedID, refreshDataList in readyTimerEntitiesMap.items():
            refreshCfg = CTR.datas.get(refreshTimedID, {})
            if not refreshCfg:
                WARNING_MSG("initTimerEntities not refreshCfg")
                continue

            startTimeCron, _ = utils.nextByTimeTupleList(refreshCfg['initialRefresh'])
            nextStartTime = now + startTimeCron
            interval = refreshCfg['refreshInterval'] * 60

            # 按天刷新的策略
            tmpNextStartTime = nextStartTime - 86400
            while tmpNextStartTime < now:
                if tmpNextStartTime + interval >= nextStartTime:
                    tmpNextStartTime = nextStartTime
                    break
                tmpNextStartTime += interval
            self.refreshEntityQueue.append(TimerEntityVal(refreshTimedID, tmpNextStartTime, interval, refreshDataList))

        if not self.refreshEntityQueue:
            return
        
        heapq.heapify(self.refreshEntityQueue)
        self.startEntityRefreshTimer()

    def startEntityRefreshTimer(self):
        if self.refreshEntityTimerId:
            self._cancelDatetimeCallback(self.refreshEntityTimerId, gametimer.TIMER_TAG_TIMER_ENTITY_REFRESH_TIMER)
            self.refreshEntityTimerId = 0

        if not self.refreshEntityQueue:
            return

        _val = heapq.nsmallest(1, self.refreshEntityQueue)[0]
        DEBUG_MSG('startEntityRefreshTimer ', _val)
        self.refreshEntityTimerId = self._datetimeCallback(_val.nextStartTime, 'onEntityRefreshTimerCallback', (), gametimer.TIMER_TAG_TIMER_ENTITY_REFRESH_TIMER, 'refreshEntityTimerId')

    def onEntityRefreshTimerCallback(self):
        if not self.refreshEntityQueue:
            return

        _val = heapq.heappop(self.refreshEntityQueue)
        DEBUG_MSG('onEntityRefreshTimerCallback', _val)
        self.doEntityRefresh(_val)
        now = utils.getNow()
        while _val.nextStartTime <= now:
            _val.nextStartTime += _val.interval

        heapq.heappush(self.refreshEntityQueue, _val)

        self.startEntityRefreshTimer()

    def doEntityRefresh(self, timerEntityVal):
        DEBUG_MSG('doEntityRefresh1', timerEntityVal)
        for refreshData in timerEntityVal.refreshDataList:
            (id_, entityType, entityID, count_) = refreshData
            ents = self.getEntitiesByTag('gid_{}'.format(id_))
            DEBUG_MSG('doEntityRefresh2', 'gid_{}'.format(id_), len(ents))
            if ents:
                continue

            if entityType == gameconst.EntityType.MONSTER and creep_base.datas.get(entityID, {}).get('type', 0) == gameconst.MonsterType.ADVANCE:
                func = getattr(self, 'doCreateWorldBoss', None)# onWorldBossRefresh 通过stub来创建->func(timerEntityVal.nextStartTime, 0)
                if not func:
                    ERROR_MSG("doEntityRefresh not WorldLineSpaceMgr", id_)
                else:
                    DEBUG_MSG("doEntityRefresh doCreateWorldBoss", id_, self.worldBossGid)
                    func()
            else:
                DEBUG_MSG("doEntityRefresh doLoadSpecifiedEntities", id_)
                self.getCurrentSpace().doLoadSpecifiedEntities([str(id_)], self.id)