# coding: utf-8
import KBEngine
from KBEDebug import *
import utils
import heapq
import userType
import gametimer
import gameconst
import creep_base
import copy
import creep_timedRefresh as CTR

class TimedIntervalsEntityVal(userType.UserSoleType):
    def __init__(self, refreshTimedID, nextStartTime, interval, refreshDataList):
        self.refreshTimedID = refreshTimedID
        self.nextStartTime = nextStartTime
        self.interval = interval
        self.refreshDataList = refreshDataList
        self.srcRefreshDataList = copy.deepcopy(self.refreshDataList)

    def __lt__(self, other):
        return self.nextStartTime < other.nextStartTime

    def __str__(self):
        return f'TimedIntervalsEntityVal(refreshTimedID={self.refreshTimedID}, nextStartTime={self.nextStartTime}, interval={self.interval}, refreshDataList={self.refreshDataList}, srcRefreshDataList={self.srcRefreshDataList}, nextStartTimeStr={utils.getTimeStrFromTimeStamp(self.nextStartTime)})'

class TimeLimitedEntityVal(userType.UserSoleType):
    def __init__(self, refreshTimedID, stageType, nextStartTime, interval, refreshDataList):
        self.refreshTimedID = refreshTimedID
        self.stageType = stageType
        self.nextStartTime = nextStartTime
        self.interval = interval
        self.refreshDataList = refreshDataList
        self.srcRefreshDataList = copy.deepcopy(self.refreshDataList)

    def __lt__(self, other):
        return self.nextStartTime < other.nextStartTime

    def __str__(self):
        return f'TimeLimitedEntityVal(refreshTimedID={self.refreshTimedID}, stageType={self.stageType}, nextStartTime={self.nextStartTime}, interval={self.interval}, refreshDataList={self.refreshDataList}, srcRefreshDataList={self.srcRefreshDataList}, nextStartTimeStr={utils.getTimeStrFromTimeStamp(self.nextStartTime)})'

class ITimerEntityRefresh(object):
    def __init__(self):
        self.refreshEntityQueue = [[] for i in range(gameconst.TimerEntityRefreshType.SIZE)]
        self.refreshGID2TimerListMap = [{} for i in range(gameconst.TimerEntityRefreshType.SIZE)]
        self.timedIntervalsEntityTimerId = 0
        self.timeLimitedEntityTimerId = 0

    def initTimerEntities(self, space, readyTimerEntitiesMap):
        if not readyTimerEntitiesMap:
            return

        INFO_MSG("initTimerEntities readyTimerEntitiesMap", readyTimerEntitiesMap)
        now = utils.getNow()
        for refreshTimedID, refreshDataList in readyTimerEntitiesMap.items():
            refreshCfg = CTR.datas.get(refreshTimedID, {})
            if not refreshCfg:
                WARNING_MSG("initTimerEntities not refreshCfg")
                continue

            refreshType = refreshCfg['RefreshType']
            if refreshType == gameconst.TimerEntityRefreshType.TIMED_INTERVALS:
                self.initTimedIntervalsEntityVal(refreshCfg, now, refreshDataList)
            elif refreshType == gameconst.TimerEntityRefreshType.TIME_LIMITED:
                self.initTimeLimitedEntityVal(refreshCfg, now, refreshDataList)
            else:
                WARNING_MSG("initTimerEntities RefreshType error", refreshType)
                continue

            for refreshData in refreshDataList:
                (id_, entityType, extraData) = refreshData
                self.refreshGID2TimerListMap[refreshType][id_] = set()

        for refreshType, refreshQueue in enumerate(self.refreshEntityQueue):
            if not refreshQueue:
                continue

            heapq.heapify(refreshQueue)
            if refreshType == gameconst.TimerEntityRefreshType.TIMED_INTERVALS:
                self.startTimedIntervalsEntityRefreshTimer()
            elif refreshType == gameconst.TimerEntityRefreshType.TIME_LIMITED:
                self.startTimeLimitedEntityRefreshTimer()

########################################################################################################
    def initTimedIntervalsEntityVal(self, refreshCfg, now, refreshDataList, subRefreshType=1):
        startTimeCron, _ = utils.nextByTimeTupleList(refreshCfg['initialRefresh'], now)
        nextStartTime = now + startTimeCron
        interval = refreshCfg['refreshInterval'] * 60
        tmpNextStartTime = nextStartTime

        if subRefreshType == 1:
            tmpNextStartTime = nextStartTime - 86400
            while tmpNextStartTime < now:
                if tmpNextStartTime + interval >= nextStartTime:
                    tmpNextStartTime = nextStartTime
                    break
                tmpNextStartTime += interval
        else:
            pass
        self.refreshEntityQueue[gameconst.TimerEntityRefreshType.TIMED_INTERVALS].append(TimedIntervalsEntityVal(refreshCfg['ID'], tmpNextStartTime, interval, refreshDataList))

    def startTimedIntervalsEntityRefreshTimer(self):
        if self.timedIntervalsEntityTimerId:
            self._cancelDatetimeCallback(self.timedIntervalsEntityTimerId, gametimer.TIMER_TAG_TIMED_INTERVALS_ENTITY_REFRESH_TIMER)
            self.timedIntervalsEntityTimerId = 0

        if not self.refreshEntityQueue[gameconst.TimerEntityRefreshType.TIMED_INTERVALS]:
            return

        _val = heapq.nsmallest(1, self.refreshEntityQueue[gameconst.TimerEntityRefreshType.TIMED_INTERVALS])[0]
        INFO_MSG('startTimedIntervalsEntityRefreshTimer ', _val)
        self.timedIntervalsEntityTimerId = self._datetimeCallback(_val.nextStartTime, 'onTimedIntervalsEntityRefreshTimerCallback', (), gametimer.TIMER_TAG_TIMED_INTERVALS_ENTITY_REFRESH_TIMER, 'timedIntervalsEntityTimerId')

    def onTimedIntervalsEntityRefreshTimerCallback(self):
        if not self.refreshEntityQueue[gameconst.TimerEntityRefreshType.TIMED_INTERVALS]:
            return

        _val = heapq.heappop(self.refreshEntityQueue[gameconst.TimerEntityRefreshType.TIMED_INTERVALS])
        INFO_MSG('onTimedIntervalsEntityRefreshTimerCallback', _val)
        self.doTimedIntervalsEntityRefresh(_val)
        now = utils.getNow()
        # 刷新策略
        while _val.nextStartTime <= now:
            _val.nextStartTime += _val.interval

        heapq.heappush(self.refreshEntityQueue[gameconst.TimerEntityRefreshType.TIMED_INTERVALS], _val)

        self.startTimedIntervalsEntityRefreshTimer()

    def doTimedIntervalsEntityRefresh(self, timedIntervalsEntityVal):
        INFO_MSG('doTimedIntervalsEntityRefresh1', timedIntervalsEntityVal)
        for refreshData in timedIntervalsEntityVal.refreshDataList:
            (id_, entityType, extraData) = refreshData
            ents = self.getEntitiesByTag('gid_{}'.format(id_))
            INFO_MSG('doTimedIntervalsEntityRefresh2', 'gid_{}'.format(id_), len(ents))
            if ents:
                continue

            self.onTimerEntityRefresh(refreshData)

    def doTimedIntervalsEntityDestroy(self, timedIntervalsEntityVal):
        DEBUG_MSG("doTimedIntervalsEntityDestroy1", timedIntervalsEntityVal)
        for refreshData in timedIntervalsEntityVal.refreshDataList:
            (id_, entityType, extraData) = refreshData
            entityID = extraData["EntityID"]
            ents = self.getEntitiesByTag('gid_{}'.format(id_))
            DEBUG_MSG('doTimedIntervalsEntityDestroy2', 'gid_{}'.format(id_), len(ents))

            self.onTimerEntityDestroy(ents, entityID)
########################################################################################################
    def initTimeLimitedEntityVal(self, refreshCfg, now, refreshDataList, subRefreshType=1):
        startTimeCron, _ = utils.nextByTimeTupleList(refreshCfg['initialRefresh'], now)
        endTimeCron, _ = utils.nextByTimeTupleList(refreshCfg['EndRefresh'], now)
        nextStartTime = now + startTimeCron
        nextEndTime = now + endTimeCron
        tmpNextStartTime = nextStartTime

        if subRefreshType == 1:
            while nextEndTime <= nextStartTime:
                nextEndTime += 86400
        else:
            pass
        self.refreshEntityQueue[gameconst.TimerEntityRefreshType.TIME_LIMITED].append(TimeLimitedEntityVal(refreshCfg['ID'], gameconst.TimeLimitedStageType.START, tmpNextStartTime, 86400, refreshDataList))

    def startTimeLimitedEntityRefreshTimer(self):
        if self.timeLimitedEntityTimerId:
            self._cancelDatetimeCallback(self.timeLimitedEntityTimerId, gametimer.TIMER_TAG_TIME_LIMITED_ENTITY_REFRESH_TIMER)
            self.timeLimitedEntityTimerId = 0

        if not self.refreshEntityQueue[gameconst.TimerEntityRefreshType.TIME_LIMITED]:
            return

        _val = heapq.nsmallest(1, self.refreshEntityQueue[gameconst.TimerEntityRefreshType.TIME_LIMITED])[0]
        INFO_MSG('startTimeLimitedEntityRefreshTimer ', _val)
        self.timeLimitedEntityTimerId = self._datetimeCallback(_val.nextStartTime, 'onTimeLimitedEntityRefreshTimerCallback', (), gametimer.TIMER_TAG_TIME_LIMITED_ENTITY_REFRESH_TIMER, 'timeLimitedEntityTimerId')

    def onTimeLimitedEntityRefreshTimerCallback(self):
        if not self.refreshEntityQueue[gameconst.TimerEntityRefreshType.TIME_LIMITED]:
            return

        _val = heapq.heappop(self.refreshEntityQueue[gameconst.TimerEntityRefreshType.TIME_LIMITED])
        INFO_MSG('onTimeLimitedEntityRefreshTimerCallback', _val)
        now = utils.getNow()
        # 刷新策略
        refreshCfg = CTR.datas.get(_val.refreshTimedID, {})
        if not refreshCfg:
            WARNING_MSG("onTimeLimitedEntityRefreshTimerCallback not refreshCfg")
            return
        if _val.stageType == gameconst.TimeLimitedStageType.START:
            self.doTimeLimitedEntityRefresh(_val)
            endTimeCron, _ = utils.nextByTimeTupleList(refreshCfg['EndRefresh'], now)
            _val.nextStartTime = now + endTimeCron
            _val.stageType = gameconst.TimeLimitedStageType.END
        elif _val.stageType == gameconst.TimeLimitedStageType.END:
            self.doTimeLimitedEntityDestroy(_val)
            startTimeCron, _ = utils.nextByTimeTupleList(refreshCfg['initialRefresh'], now)
            _val.nextStartTime = now + startTimeCron
            _val.stageType = gameconst.TimeLimitedStageType.START

        heapq.heappush(self.refreshEntityQueue[gameconst.TimerEntityRefreshType.TIME_LIMITED], _val)

        self.startTimeLimitedEntityRefreshTimer()

    def doTimeLimitedEntityRefresh(self, timeLimitedEntityVal):
        INFO_MSG("doTimeLimitedEntityRefresh", timeLimitedEntityVal)
        for refreshData in timeLimitedEntityVal.refreshDataList:
            (id_, entityType, extraData) = refreshData
            ents = self.getEntitiesByTag('gid_{}'.format(id_))
            INFO_MSG('doTimeLimitedEntityRefresh2', 'gid_{}'.format(id_), len(ents))
            if ents:
                continue

            self.onTimerEntityRefresh(refreshData)

    def doTimeLimitedEntityDestroy(self, timeLimitedEntityVal):
        DEBUG_MSG("doTimeLimitedEntityDestroy1", timeLimitedEntityVal)
        for refreshData in timeLimitedEntityVal.refreshDataList:
            (id_, entityType, extraData) = refreshData
            entityID = extraData["EntityID"]
            count_ = extraData["RefreshNum"]
            ents = self.getEntitiesByTag('gid_{}'.format(id_))
            DEBUG_MSG('doTimeLimitedEntityDestroy2', 'gid_{}'.format(id_), entityID, len(ents))

            self.onTimerEntityDestroy(ents, entityID)

            self.onCancelEntityRefreshTimer(id_)

    def doTimeLimitedGroupEntityDestroy(self, info):
        DEBUG_MSG("doTimeLimitedGroupEntityDestroy1", info)
        id_ = info['id']
        entityID = info["eId"]
        ents = self.getEntitiesByTag('gid_{}'.format(id_))
        DEBUG_MSG('doTimeLimitedGroupEntityDestroy2', 'gid_{}'.format(id_), entityID, len(ents))

        self.onTimerEntityDestroy(ents, entityID)

########################################################################################################
    def onTemporaryDestroyTimerEntities(self, entityTypes):
        INFO_MSG("onAddTemporaryDestroyTimerEntities", entityTypes)
        for refreshType, refreshQueue in enumerate(self.refreshEntityQueue):
            if not refreshQueue:
                continue
            for val in refreshQueue:
                INFO_MSG("onAddTemporaryDestroyTimerEntities", val)
                tmpVal = copy.deepcopy(val)
                tmpVal.refreshDataList = []
                for refreshData in tmpVal.srcRefreshDataList:
                    (id_, entityType, extraData) = refreshData
                    if entityType not in entityTypes:
                        continue

                    if refreshData in val.refreshDataList:
                        val.refreshDataList.remove(refreshData)
                    tmpVal.refreshDataList.append(refreshData)

                if refreshType == gameconst.TimerEntityRefreshType.TIMED_INTERVALS:
                    self.doTimedIntervalsEntityDestroy(tmpVal)
                elif refreshType == gameconst.TimerEntityRefreshType.TIME_LIMITED:
                    self.doTimeLimitedEntityDestroy(tmpVal)

    def onRestoreTemporaryDestroyTimerEntities(self):
        INFO_MSG("onRestoreTemporaryDestroyTimerEntities")
        for refreshType, refreshQueue in enumerate(self.refreshEntityQueue):
            if not refreshQueue:
                continue
            for val in refreshQueue:
                INFO_MSG("onRestoreTemporaryDestroyTimerEntities", val)
                val.refreshDataList = copy.deepcopy(val.srcRefreshDataList)

                if refreshType == gameconst.TimerEntityRefreshType.TIMED_INTERVALS:
                    #self.doTimedIntervalsEntityRefresh(val)
                    # 走定时
                    pass
                elif refreshType == gameconst.TimerEntityRefreshType.TIME_LIMITED:
                    if val.stageType == gameconst.TimeLimitedStageType.END:
                        INFO_MSG("onRestoreTemporaryDestroyTimerEntities END")
                        self.doTimeLimitedEntityRefresh(val)
                    elif val.stageType == gameconst.TimeLimitedStageType.START:
                        INFO_MSG("onRestoreTemporaryDestroyTimerEntities START")
                        pass

    def onDestroyGroupEntities(self, info):
        refreshType = info['refreshType']
        if refreshType == gameconst.TimerEntityRefreshType.TIMED_INTERVALS:
            ERROR_MSG("onDestroyGroupEntities error")

        if refreshType == gameconst.TimerEntityRefreshType.TIME_LIMITED:
            self.doTimeLimitedGroupEntityDestroy(info)

    def onTimerEntityDestroy(self, ents, entityID):
        for ent in ents:
            if ent.IsMonster:
                if creep_base.datas.get(entityID, {}).get('type', 0) == gameconst.MonsterType.ADVANCE:
                    self.onWorldBossDead(ent.refreshTime)
                elif ent.isNeedRefresh():
                    ent.onEntityRefresh()
                ent.safeDestroy()
                #ent.killSelf(gameconst.SourceType.Default)
            elif ent.IsCollection:
                ent.safeDestroy()

    def onTimerEntityRefresh(self, refreshData):
        (id_, entityType, extraData) = refreshData
        entityID = extraData["EntityID"]
        count_ = extraData["RefreshNum"]

        if entityType == gameconst.EntityType.MONSTER and creep_base.datas.get(entityID, {}).get('type', 0) == gameconst.MonsterType.ADVANCE:
            func = getattr(self, 'doCreateWorldBoss', None)
            if not func:
                ERROR_MSG("doTimedIntervalsEntityRefresh not WorldLineSpaceMgr", id_)
            else:
                func()
        else:
            self.getCurrentSpace().doLoadSpecifiedEntities([str(id_)], self.id)

    def onAddEntityRefreshTimer(self, gid, timerId):
        INFO_MSG("onAddEntityRefreshTimer", gid, timerId)
        if gid in self.refreshGID2TimerListMap[gameconst.TimerEntityRefreshType.TIMED_INTERVALS]:
            WARNING_MSG("onAddTimerEntityRefresh gid cfg, refreshTime not 0")

        if gid in self.refreshGID2TimerListMap[gameconst.TimerEntityRefreshType.TIME_LIMITED]:
            self.refreshGID2TimerListMap[gameconst.TimerEntityRefreshType.TIME_LIMITED][gid].add(timerId)

    def onCancelEntityRefreshTimer(self, gid, timerId=0):
        INFO_MSG("onCancelEntityRefreshTimer", gid, timerId)
        if gid in self.refreshGID2TimerListMap[gameconst.TimerEntityRefreshType.TIMED_INTERVALS]:
            WARNING_MSG("onCancelTimerEntityRefresh gid cfg, refreshTime not 0")

        if gid in self.refreshGID2TimerListMap[gameconst.TimerEntityRefreshType.TIME_LIMITED]:
            if timerId and timerId in self.refreshGID2TimerListMap[gameconst.TimerEntityRefreshType.TIME_LIMITED][gid]:
                self.refreshGID2TimerListMap[gameconst.TimerEntityRefreshType.TIME_LIMITED][gid].discard(timerId)
            else:
                for tId in self.refreshGID2TimerListMap[gameconst.TimerEntityRefreshType.TIME_LIMITED][gid]:
                    self.getCurrentSpace()._cancelCallback(tId, gametimer.TIMER_TAG_SPACE_DO_REFRESH)
                self.refreshGID2TimerListMap[gameconst.TimerEntityRefreshType.TIME_LIMITED][gid].clear()