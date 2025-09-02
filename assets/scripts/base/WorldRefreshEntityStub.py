# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine

import gameengine
import utils

import iBaseNoCell
import iGlobal
import gameconst
import iTimer
import gametimer
import gameglobal
import formula
import gameengine
import copy

import worldMonsterRefresh_entityRefresh as WMR_ER
import worldMonsterRefresh_entitykRefreshGroup as WMR_ERG

class WorldRefreshEntityStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer):

    def __init__(self):
        super(WorldRefreshEntityStub, self).__init__()
        self.groupRefreshInfo = {}
        self.groupEntityReady = {}
        self.gameEntityIdSet = {}
        return

    def doNext(self):
        gameglobal.localBaseApp.fullPrepare(self.classname())
        return

    def onTimer(self, timerID, userData):
        self._onTimer(timerID, userData)
        if utils.isBelongTimerTag(userData):
            self._onTimerCallback(timerID)
        return

    def checkAllGroupReady(self, box, callback, args):
        cbFunc = getattr(box, callback)
        for groupId, isReady in self.groupEntityReady.items():
            cbFunc(groupId, isReady, *args)

    def loadGroupEntities(self):
        DEBUG_MSG("WorldRefreshEntityStub::loadGroupEntities")

        for groupId, groupCfg in WMR_ERG.datas.items():
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

    def _initGroupEntities(self, groupId, groupCfg, refreshNum=0, excludeIds=[]):
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

    def onLoadGroupEntities(self, spaceNo, info):
        DEBUG_MSG("WorldRefreshEntityStub::_onLoadGroupEntities id, info", id, info)

        if formula.spaceInWorldLine(spaceNo):
            gameengine.getLineStub(formula.getMapId(spaceNo)).onLoadGroupEntities(info)

        elif formula.isCubeSpace(spaceNo):
            gameengine.getGlobalBase('CubeStub').onLoadGroupEntities(info)

        elif formula.isWonderLandSpace(spaceNo):
            gameengine.getWonderLandStubBySpaceNo(spaceNo).onLoadGroupEntities(info)

    def onRefreshGroupEntities(self, id, info):
        DEBUG_MSG("WorldRefreshEntityStub::onRefreshGroupEntities id, info", id, info)

        if formula.spaceInWorldLine(id):
            gameengine.getLineStub(formula.getMapId(id)).onRefreshGroupEntities(info)

        elif formula.isCubeSpace(id):
            gameengine.getGlobalBase('CubeStub').onRefreshGroupEntities(info)

        elif formula.isWonderLandSpace(id):
            gameengine.getWonderLandStubBySpaceNo(id).onRefreshGroupEntities(info)

    def onLoadGroupEntitiesAck(self, info):
        lineNo = formula.getLineNo(info['spaceNo'])
        groupInfo = self.groupRefreshInfo.setdefault(info['gId'], {})
        lineInfo = groupInfo.setdefault(lineNo, {})
        curInfo = lineInfo.setdefault(info['id'], {})
        curInfo.update(info)
        DEBUG_MSG("WorldRefreshEntityStub::_onLoadGroupEntitiesAck info", curInfo)

    def onGroupEntityRefresh(self, spaceNo, gameEntityId, refreshTime):
        DEBUG_MSG("WorldRefreshEntityStub::onGroupEntityRefresh spaceNo, gameEntityId, refreshTime", spaceNo, gameEntityId, refreshTime)
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
        initInfo = self._initGroupEntities(groupId, groupCfg, refreshNum=1, excludeIds=ids)
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

            self.onRefreshGroupEntities(newId, info)

        DEBUG_MSG("WorldRefreshEntityStub::onGroupEntityRefresh end", curLineInfo)
