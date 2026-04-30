# -*- coding: utf-8 -*-
import formula
from KBEDebug import *
import random
import gameconst
import utils
import formula
from collections import defaultdict


def _defaultdict_list():
    return defaultdict(list)


class IMapRefresher(object):
    '''
    一张地图上的刷新位置，
    根据表格上的规则和已有数据去刷新
    '''

    def __init__(self):
        self.mapPosUsed = {}  # {spaceNo: [index,]]}
        self.collects = {}
        self.refreshTimers = {}
        self.groupCollects = defaultdict(_defaultdict_list)
        self.nonGroupCollects = _defaultdict_list()

    def startRrefreshTimer(self, spaceNo, policyIdsMap={}):
        pass

    def onRefreshEntity(self, spaceNo, entId):
        pass

    def getMapRefreshPolicyData(self, spaceNo):
        mapId = formula.fetchMapId(spaceNo)
        try:
            return __import__('mapRefresh_refresh%s' % mapId).datas
        except Exception as e:
            LOG_ERR('cannot get map refresh data for', spaceNo, mapId)
            return {}

    def getEntRefreshData(self, spaceNo):
        mapId = formula.fetchMapId(spaceNo)
        try:
            mapEntRefresh = __import__('map_entities_refresh_r%s' % mapId)
            return mapEntRefresh
        except Exception as e:
            LOG_WARN('cannot get entities refresh r data for', spaceNo, mapId)
            return None

    def calcValidPos(self, spaceNo, rId, posPool=[]):
        if spaceNo not in self.mapPosUsed:
            self.mapPosUsed[spaceNo] = []

        tmp = [formula.calcPosPoolIndex(rId, x) for x in range(len(posPool))]
        return [x for x in tmp if x not in self.mapPosUsed[spaceNo]]

    def addEntitysCache(self, spaceNo, entId, posIndex, rGid):
        if spaceNo not in self.collects:
            self.collects[spaceNo] = []

        self.collects[spaceNo].append((entId, posIndex))
        if rGid:
            self.groupCollects[spaceNo][rGid].append(entId)
        else:
            self.nonGroupCollects[spaceNo].append(entId)

    def getEntityBornPos(self, spaceNo, policyId):
        policyData = self.getMapRefreshPolicyData(spaceNo).get(policyId, {})
        num = policyData.get('num', 1)
        poolPos = policyData.get('position', [])
        posIndexList = self.allocEntityPos(spaceNo, policyId, poolPos, num)
        return [poolPos[formula.fetchPosPoolIndex(posIndex)] for posIndex in posIndexList], posIndexList

    def getEntityRefreshParams(self, spaceNo, policyId):
        policyData = self.getMapRefreshPolicyData(spaceNo).get(policyId, {})
        direction = (0, 0, policyData.get('direction', 0))
        refreshTime = gameconst.MapRefreshType.countSec(policyData.get('period')) if policyData.get('period') else 0
        return direction, refreshTime

    def getEntityDisappearTime(self, spaceNo, policyId):
        policyData = self.getMapRefreshPolicyData(spaceNo).get(policyId, {})
        try:
            _disappearTime = policyData.get('disappearTime', None)
            if _disappearTime:
                disappearTimeStr = str(_disappearTime)
                disappearTime = utils.getIntTimestamp(disappearTimeStr)
                return disappearTime
        except Exception:
            LOG_ERR("map refresh config for disappearTime error", spaceNo, policyId)
            return -1

    def preAllocEntityPos(self, spaceNo, policyId):
        policyData = self.getMapRefreshPolicyData(spaceNo).get(policyId, {})
        num = policyData.get('num', 1)
        poolPos = policyData.get('position', [])
        return self.allocEntityPos(spaceNo, policyId, poolPos, num)

    def allocEntityPos(self, spaceNo, policyId, poolPos, num):
        validPosPool = self.calcValidPos(spaceNo, policyId, poolPos)
        assert (len(validPosPool) >= num)
        posList = random.sample(validPosPool, num)
        if spaceNo not in self.mapPosUsed:
            self.mapPosUsed = []
        self.mapPosUsed[spaceNo].extend(posList)
        return posList

    def recycleEntityPos(self, spaceNo, entId, posIndex):
        # LOG_DBG("iMapRefresh recycleEntityPos ", spaceNo, entId, posIndex)
        entInfoLst = self.collects.get(spaceNo, [])
        if (entId, posIndex) in entInfoLst:
            self.collects[spaceNo].remove((entId, posIndex))
            self.mapPosUsed[spaceNo].remove(posIndex)
            for gId, gp in self.groupCollects[spaceNo].items():
                if entId in gp:
                    self.groupCollects[spaceNo][gId].remove(entId)
                    # LOG_DBG("recycle group entity pos success", entId, posIndex)
                    return True, gId

            if entId in self.nonGroupCollects[spaceNo]:
                self.nonGroupCollects[spaceNo].remove(entId)
                # LOG_DBG("recycle non group entity pos success", entId)
                return True, 0
            else:
                LOG_ERR("MpaRefresh recycle entity pos not in mananger", spaceNo, entId, posIndex)
                return False, 0

        LOG_ERR("recycleEntityPos failed", spaceNo, entId, posIndex)
        return False, 0

    def recycleSpacePos(self, spaceNo):
        self.mapPosUsed[spaceNo] = []
        self.collects[spaceNo] = []
        self.groupCollects[spaceNo] = _defaultdict_list()
        self.nonGroupCollects[spaceNo] = []

    def checkRefreshGroups(self, spaceNo, gId):
        # LOG_DBG("checkRefreshGroups", self.groupCollects, spaceNo)
        if gId not in self.groupCollects[spaceNo] or len(self.groupCollects[spaceNo][gId]) == 0:
            return True
        return False

    def checkRefreshSingle(self, spaceNo, entId):
        # LOG_DBG("checkRefreshSingle", spaceNo, entId)
        if entId not in self.nonGroupCollects[spaceNo]:
            return True
        return False
