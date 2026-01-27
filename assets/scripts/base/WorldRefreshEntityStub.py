# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine

import gameengine
import utils

import iBaseNoCell
import iGlobal
import heapq
import gameconst
import iTimer
import userType
import gametimer
import gameglobal
import formula
import gameengine
import copy

import worldMonsterRefresh_entityRefresh as WMR_ER
import worldMonsterRefresh_entitykRefreshGroup as WMR_ERG
import creep_timedRefresh as CTR

class TimeLimitedGroupEntityVal(userType.UserSoleType):
    def __init__(self, refreshTimedID, stageType, nextStartTime, interval, refreshDataList):
        self.refreshTimedID = refreshTimedID
        self.stageType = stageType
        self.nextStartTime = nextStartTime
        self.interval = interval
        self.refreshDataList = refreshDataList

    def __lt__(self, other):
        return self.nextStartTime < other.nextStartTime

    def __str__(self):
        return f'TimeLimitedGroupEntityVal(refreshTimedID={self.refreshTimedID}, stageType={self.stageType}, nextStartTime={self.nextStartTime}, interval={self.interval}, refreshDataList={self.refreshDataList}, nextStartTimeStr={utils.getTimeStrFromTimeStamp(self.nextStartTime)})'

class WorldRefreshEntityStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer):

    def __init__(self):
        super(WorldRefreshEntityStub, self).__init__()
        self.groupRefreshInfo = {}
        self.groupEntityReady = {}
        self.gameEntityIdSet = {}

        self.refreshGroupEntityQueue = [[] for i in range(gameconst.TimerEntityRefreshType.SIZE)]
        self.timeLimitedGroupEntityTimerId = 0
        self.addDatetimeTimerTick()

    def doNext(self):
        gameglobal.localBaseApp.fullPrepare(self.classname())
        return

    def onTimer(self, timerID, userData):
        self._onTimer(timerID, userData)
        if utils.isBelongTimerTag(userData):
            self._onTimerCallback(timerID)
        elif userData == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()

    def checkAllGroupReady(self, box, callback, args):
        cbFunc = getattr(box, callback)
        for groupId, isReady in self.groupEntityReady.items():
            cbFunc(groupId, isReady, *args)

    def loadGroupEntities(self):
        INFO_MSG("WorldRefreshEntityStub::loadGroupEntities")

        for groupId, groupCfg in WMR_ERG.datas.items():
            if groupCfg.get('RefreshTimedID', 0):
                continue
            initInfo = self._initGroupEntities(groupId, groupCfg)
            self.groupRefreshInfo[groupId] = initInfo
            self.groupEntityReady[groupId] = True
            DEBUG_MSG("WorldRefreshEntityStub::loadGroupEntities group initInfo", initInfo)

        DEBUG_MSG("WorldRefreshEntityStub::loadGroupEntities end", self.groupRefreshInfo, self.groupEntityReady)

        tmpGroupRefreshInfo = copy.deepcopy(self.groupRefreshInfo)
        self.groupRefreshInfo.clear()
        for groupId, initInfo in tmpGroupRefreshInfo.items():
            for id, info in initInfo.items():
                self.onLoadGroupEntities(id, info)

        self.doLoadTimerGroupEntities()

    def _initGroupEntities(self, groupId, groupCfg, refreshType=0, refreshNum=0, excludeIds=[]):
        DEBUG_MSG("WorldRefreshEntityStub::_initGroupEntities")

        initInfo = {}
        refreshNum = refreshNum if refreshNum > 0 else groupCfg.get('refreshNum', 1)
        refreshTime = groupCfg.get('refreshTime', 0)
        DEBUG_MSG("WorldRefreshEntityStub::_initGroupEntities refreshNum, refreshTime", refreshNum, refreshTime)

        eidList, eidWeightList = self.getEIDWeightListByGroup(groupId, groupCfg)
        DEBUG_MSG("WorldRefreshEntityStub::_initGroupEntities eidList, eidWeightList", eidList, eidWeightList)
        idList, idWeightList = self.getIDWeightListByGroup(groupId, excludeIds)
        DEBUG_MSG("WorldRefreshEntityStub::_initGroupEntities idList, idweightList", idList, idWeightList)

        if len(eidList) <= 0 or len(idList) <= 0:
            WARNING_MSG("WorldRefreshEntityStub::_initGroupEntities eidList, idList", len(eidList), len(idList))
            return initInfo

        maxRefreshNum = min(refreshNum, len(idList))
        DEBUG_MSG("WorldRefreshEntityStub::_initGroupEntities maxRefreshNum", maxRefreshNum)
        for i in range(maxRefreshNum):
            if len(idList) <= 0:
                break

            idx = utils.randomByWeight(idWeightList)
            eIdx = utils.randomByWeight(eidWeightList)
            if idx == None or eIdx == None:
                WARNING_MSG("WorldRefreshEntityStub::_initGroupEntities idx, eIdx", idx, eIdx)
                continue

            id = idList[idx]
            eId = eidList[eIdx]
            info = {
                'gId': groupId,
                'id': id,
                'eId': eId,
                'cnt': 1,
                'refreshTime': refreshTime,
                'className' : 'Collection',
                'entityType': gameconst.className2EntityType['Collection'],
                'refreshType': refreshType,
                }
            initInfo[id] = info

            idWeightList.pop(idx)
            idList.pop(idx)

        return initInfo

    def getEIDWeightListByGroup(self, groupId, groupCfg=None):
        DEBUG_MSG("WorldRefreshEntityStub::getEIDWeightListByGroup")

        eidList = []
        eidWeightList = []
        groupCfg = groupCfg if groupCfg is not None else WMR_ERG.datas.get(groupId, None)
        if groupCfg:
            entityIDTups = groupCfg.get('entityID', ())
            if entityIDTups:
                for val in entityIDTups:
                    eid, weight = val
                    eidList.append(eid)
                    eidWeightList.append(weight)

        return eidList, eidWeightList

    def getIDWeightListByGroup(self, groupId, excludeIds):
        DEBUG_MSG("WorldRefreshEntityStub::getIDWeightListByGroup groupId, excludeIds", groupId, excludeIds)

        idList = []
        idWeightList = []
        for id, refreshData in WMR_ER.datas.items():
            isOpen = refreshData.get('isOpen', 0)
            refreshGroupID = refreshData.get('refreshGroupID', 0)
            refreshWeight = refreshData.get('refreshWeight', 0)
            if not isOpen or groupId != refreshGroupID:
                continue
            if id in excludeIds:
                continue

            idList.append(id)
            idWeightList.append(refreshWeight)

        return idList, idWeightList

    def onLoadGroupEntities(self, id, info):
        DEBUG_MSG("WorldRefreshEntityStub::onLoadGroupEntities id, info", id, info)

        if formula.spaceInWorldLine(id):
            gameengine.getLineStub(formula.getMapId(id)).onLoadGroupEntities(info)

        elif formula.isCubeSpace(id):
            gameengine.getCubeStubBySpaceNo(id).onLoadGroupEntities(info)

        elif formula.isWonderLandSpace(id):
            gameengine.getWonderLandStubBySpaceNo(id).onLoadGroupEntities(info)

    def onRefreshGroupEntities(self, id, info, pointData):
        DEBUG_MSG("WorldRefreshEntityStub::onRefreshGroupEntities id, info", id, info)

        self.onCancelGroupEntityRefreshTimer(info, pointData["refreshTimerId"])

        if formula.spaceInWorldLine(id):
            gameengine.getLineStub(formula.getMapId(id)).onRefreshGroupEntities(info)

        elif formula.isCubeSpace(id):
            gameengine.getCubeStubBySpaceNo(id).onRefreshGroupEntities(info)

        elif formula.isWonderLandSpace(id):
            gameengine.getWonderLandStubBySpaceNo(id).onRefreshGroupEntities(info)

    def onDestroyGroupEntities(self, id, info):
        DEBUG_MSG("WorldRefreshEntityStub::onDestroyGroupEntities id, info", id, info)

        if formula.spaceInWorldLine(id):
            gameengine.getLineStub(formula.getMapId(id)).onDestroyGroupEntities(info)

        elif formula.isCubeSpace(id):
            gameengine.getCubeStubBySpaceNo(id).onDestroyGroupEntities(info)

        elif formula.isWonderLandSpace(id):
            gameengine.getWonderLandStubBySpaceNo(id).onDestroyGroupEntities(info)

    def onLoadGroupEntitiesAck(self, info):
        lineNo = formula.getLineNo(info['spaceNo'])
        groupInfo = self.groupRefreshInfo.setdefault(info['gId'], {})
        lineInfo = groupInfo.setdefault(lineNo, {})
        curInfo = lineInfo.setdefault(info['id'], {})
        curInfo.update(info)
        DEBUG_MSG("WorldRefreshEntityStub::_onLoadGroupEntitiesAck info", curInfo)

    def onGroupEntityRefresh(self, spaceNo, gameEntityId, refreshTime):
        INFO_MSG("WorldRefreshEntityStub::onGroupEntityRefresh spaceNo, gameEntityId, refreshTime", spaceNo, gameEntityId, refreshTime)
        lineNo = formula.getLineNo(spaceNo)
        id = utils.getGidFromGameEntityId(gameEntityId)
        geIds = self.gameEntityIdSet.setdefault(id, set())
        geIds.add(gameEntityId)

        curInfo = None
        curLineInfo = None
        curGroupInfo = None
        entityRefreshCfg = WMR_ER.datas.get(id, None)
        if not entityRefreshCfg:
            WARNING_MSG("WorldRefreshEntityStub::onGroupEntityRefresh entityRefreshCfg", gameEntityId)
            return
        curGroupInfo = self.groupRefreshInfo.get(entityRefreshCfg['refreshGroupID'], None)
        if not curGroupInfo:
            WARNING_MSG("WorldRefreshEntityStub::onGroupEntityRefresh curGroupInfo", gameEntityId)
            return
        curLineInfo = curGroupInfo.get(lineNo, None)
        if not curLineInfo:
            WARNING_MSG("WorldRefreshEntityStub::onGroupEntityRefresh curLineInfo", gameEntityId)
            return
        curInfo = curLineInfo.get(id, None)
        if not curInfo:
            WARNING_MSG("WorldRefreshEntityStub::onGroupEntityRefresh curInfo", gameEntityId)
            return
        groupId = curInfo['gId']
        ids = list(curLineInfo.keys())
        curLineInfo.pop(id, None)

        groupCfg = WMR_ERG.datas.get(groupId, None)
        initInfo = self._initGroupEntities(groupId, groupCfg, curInfo['refreshType'], refreshNum=1, excludeIds=ids)
        if len(initInfo) != 1:
            WARNING_MSG("WorldRefreshEntityStub::onGroupEntityRefresh gameEntityId, excludeIds", gameEntityId, ids)
            return
        curLineInfo.update(initInfo)

        for newId, info in initInfo.items():
            info['lineNo'] = lineNo
            _geIdsSet = self.gameEntityIdSet.setdefault(newId, set())
            if len(_geIdsSet) > 0:
                _geids = []
                _geids.append(_geIdsSet.pop())
                info['geIds'] = _geids

            curRefreshTime = info.get('refreshTime', refreshTime)
            pointData = {}
            timerId = self._callback(curRefreshTime, 'onRefreshGroupEntities', (newId, info, pointData), gametimer.TIMER_TAG_LOAD_GROUP_ENTITIES_CALL_BACK)
            pointData["refreshTimerId"] = timerId
            self.onAddGroupEntityRefreshTimer(info, timerId)

        DEBUG_MSG("WorldRefreshEntityStub::onGroupEntityRefresh end", curLineInfo)
########################################################################################################
    def doLoadTimerGroupEntities(self):
        INFO_MSG("WorldRefreshEntityStub::oLoadTimerGroupEntities")

        readyTimerGroupEntitiesMap = {}
        self.loadTimerGroupEntities(readyTimerGroupEntitiesMap)
        self.initTimerEntities(readyTimerGroupEntitiesMap)

    def loadTimerGroupEntities(self, readyTimerGroupEntitiesMap):
        INFO_MSG("WorldRefreshEntityStub::loadTimerGroupEntities")
        for groupId, groupCfg in WMR_ERG.datas.items():
            refreshTimedID = groupCfg.get('RefreshTimedID', 0)
            if not refreshTimedID:
                continue

            refreshData = (groupId,)
            readyTimerGroupEntitiesMap.setdefault(refreshTimedID, []).append(refreshData)
            DEBUG_MSG("WorldRefreshEntityStub::loadTimerGroupEntities", groupId, refreshTimedID, refreshData)

    def initTimerEntities(self, readyTimerGroupEntitiesMap):
        if not readyTimerGroupEntitiesMap:
            return

        INFO_MSG("WorldRefreshEntityStub::initTimerEntities", readyTimerGroupEntitiesMap)
        now = utils.getNow()
        for refreshTimedID, refreshDataList in readyTimerGroupEntitiesMap.items():
            refreshCfg = CTR.datas.get(refreshTimedID, {})
            if not refreshCfg:
                WARNING_MSG("WorldRefreshEntityStub::initTimerEntities not refreshCfg")
                continue

            refreshType = refreshCfg['RefreshType']
            if refreshType == gameconst.TimerEntityRefreshType.TIMED_INTERVALS:
                ERROR_MSG("WorldRefreshEntityStub::initTimerEntities TIMED_INTERVALS error", refreshType)
                continue
            elif refreshType == gameconst.TimerEntityRefreshType.TIME_LIMITED:
                self.initTimeLimitedGroupEntityVal(refreshCfg, now, refreshDataList)
            else:
                ERROR_MSG("WorldRefreshEntityStub::initTimerEntities RefreshType error", refreshType)
                continue

        for refreshType, refreshQueue in enumerate(self.refreshGroupEntityQueue):
            if not refreshQueue:
                continue

            heapq.heapify(refreshQueue)
            if refreshType == gameconst.TimerEntityRefreshType.TIMED_INTERVALS:
                ERROR_MSG("WorldRefreshEntityStub::initTimerEntities TIMED_INTERVALS error", refreshType)
                continue
            elif refreshType == gameconst.TimerEntityRefreshType.TIME_LIMITED:
                self.startTimeLimitedGroupEntityRefreshTimer()

########################################################################################################
    def initTimeLimitedGroupEntityVal(self, refreshCfg, now, refreshDataList, subRefreshType=1):
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
        self.refreshGroupEntityQueue[gameconst.TimerEntityRefreshType.TIME_LIMITED].append(TimeLimitedGroupEntityVal(refreshCfg['ID'], gameconst.TimeLimitedStageType.START, tmpNextStartTime, 86400, refreshDataList))
        INFO_MSG("WorldRefreshEntityStub::initTimeLimitedGroupEntityVal ", self.refreshGroupEntityQueue[gameconst.TimerEntityRefreshType.TIME_LIMITED][-1])

    def startTimeLimitedGroupEntityRefreshTimer(self):
        if self.timeLimitedGroupEntityTimerId:
            self._cancelDatetimeCallback(self.timeLimitedGroupEntityTimerId, gametimer.TIMER_TAG_TIME_LIMITED_GROUP_ENTITY_REFRESH_TIMER)
            self.timeLimitedGroupEntityTimerId = 0

        if not self.refreshGroupEntityQueue[gameconst.TimerEntityRefreshType.TIME_LIMITED]:
            return

        _val = heapq.nsmallest(1, self.refreshGroupEntityQueue[gameconst.TimerEntityRefreshType.TIME_LIMITED])[0]
        INFO_MSG('WorldRefreshEntityStub::startTimeLimitedGroupEntityRefreshTimer ', _val)
        self.timeLimitedGroupEntityTimerId = self._datetimeCallback(_val.nextStartTime, 'onTimeLimitedGroupEntityRefreshTimerCallback', (), gametimer.TIMER_TAG_TIME_LIMITED_GROUP_ENTITY_REFRESH_TIMER, 'timeLimitedGroupEntityTimerId')

    def onTimeLimitedGroupEntityRefreshTimerCallback(self):
        if not self.refreshGroupEntityQueue[gameconst.TimerEntityRefreshType.TIME_LIMITED]:
            return

        _val = heapq.heappop(self.refreshGroupEntityQueue[gameconst.TimerEntityRefreshType.TIME_LIMITED])
        INFO_MSG('WorldRefreshEntityStub::onTimeLimitedGroupEntityRefreshTimerCallback', _val)
        now = utils.getNow()
        # 刷新策略
        refreshCfg = CTR.datas.get(_val.refreshTimedID, {})
        if not refreshCfg:
            WARNING_MSG("WorldRefreshEntityStub::onTimeLimitedGroupEntityRefreshTimerCallback not refreshCfg")
            return
        if _val.stageType == gameconst.TimeLimitedStageType.START:
            self.doTimeLimitedGroupEntityRefresh(_val)
            endTimeCron, _ = utils.nextByTimeTupleList(refreshCfg['EndRefresh'], now)
            _val.nextStartTime = now + endTimeCron
            _val.stageType = gameconst.TimeLimitedStageType.END
        elif _val.stageType == gameconst.TimeLimitedStageType.END:
            self.doTimeLimitedGroupEntityDestroy(_val)
            startTimeCron, _ = utils.nextByTimeTupleList(refreshCfg['initialRefresh'], now)
            _val.nextStartTime = now + startTimeCron
            _val.stageType = gameconst.TimeLimitedStageType.START

        heapq.heappush(self.refreshGroupEntityQueue[gameconst.TimerEntityRefreshType.TIME_LIMITED], _val)

        self.startTimeLimitedGroupEntityRefreshTimer()

    def doTimeLimitedGroupEntityRefresh(self, timeLimitedGroupEntityVal):
        INFO_MSG("WorldRefreshEntityStub::doTimeLimitedGroupEntityRefresh", timeLimitedGroupEntityVal)
        for refreshData in timeLimitedGroupEntityVal.refreshDataList:
            (groupId, ) = refreshData
            groupCfg = WMR_ERG.datas[groupId]
            initInfo = self._initGroupEntities(groupId, groupCfg, gameconst.TimerEntityRefreshType.TIME_LIMITED)
            for id, info in initInfo.items():
                self.onLoadGroupEntities(id, info)

    def doTimeLimitedGroupEntityDestroy(self, timeLimitedGroupEntityVal):
        INFO_MSG("WorldRefreshEntityStub::doTimeLimitedGroupEntityDestroy", timeLimitedGroupEntityVal)
        for refreshData in timeLimitedGroupEntityVal.refreshDataList:
            (groupId, ) = refreshData
            curGroupInfo = self.groupRefreshInfo.get(groupId, None)
            if not curGroupInfo:
                WARNING_MSG("WorldRefreshEntityStub::doTimeLimitedGroupEntityDestroy not curGroupInfo", groupId)
                continue
            DEBUG_MSG('WorldRefreshEntityStub::doTimeLimitedGroupEntityDestroy curGroupInfo', curGroupInfo)
            for lineNo, curLineInfo in curGroupInfo.items():
                for id in list(curLineInfo.keys()):
                    info = curLineInfo.pop(id, {})
                    _geids = info.get('geIds', None)
                    if _geids:
                        geIdsSet = self.gameEntityIdSet.setdefault(id, set())
                        geIdsSet.update(_geids)
                    self.onCancelGroupEntityRefreshTimer(info)
                    self.onDestroyGroupEntities(id, info)

########################################################################################################
    def onAddGroupEntityRefreshTimer(self, info, timerId):
        id = info['id']
        refreshType = info['refreshType']
        INFO_MSG("WorldRefreshEntityStub::onAddGroupEntityRefreshTimer", info, timerId)

        if refreshType == gameconst.TimerEntityRefreshType.TIMED_INTERVALS:
            ERROR_MSG("WorldRefreshEntityStub::onAddGroupEntityRefreshTimer error")

        if refreshType == gameconst.TimerEntityRefreshType.TIME_LIMITED:
            timerSet = info.setdefault('timerSet', set())
            timerSet.add(timerId)

    def onCancelGroupEntityRefreshTimer(self, info, timerId=0):
        id = info['id']
        refreshType = info['refreshType']
        INFO_MSG("WorldRefreshEntityStub::onCancelGroupEntityRefreshTimer", info, timerId)

        if refreshType == gameconst.TimerEntityRefreshType.TIMED_INTERVALS:
            ERROR_MSG("WorldRefreshEntityStub::onCancelGroupEntityRefreshTimer error")

        if refreshType == gameconst.TimerEntityRefreshType.TIME_LIMITED:
            timerSet = info.setdefault('timerSet', set())
            if timerId and timerId in timerSet:
                timerSet.discard(timerId)
            else:
                for tId in timerSet:
                    self._cancelCallback(tId, gametimer.TIMER_TAG_LOAD_GROUP_ENTITIES_CALL_BACK)
                info.pop('timerSet', set())