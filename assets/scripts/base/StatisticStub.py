# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *

import gameengine
import gametimer
import Statistics
import iBaseNoCell
import iGlobal
import iTimer
import utils
import gameconfig
import gameglobal



class StatisticStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer):

    def __init__(self):
        super(StatisticStub, self).__init__()
        LOG_IFO("StatisticStub  __init__", self.classname())
        self.statisticDic = {}
        return

    def postReloadScript(self):
        super(StatisticStub, self).postReloadScript()
        for v in self.statisticDic.values():
            v.reloadScript()

    def doNext(self):
        gameglobal.localBaseApp.fullPrepare(self.classname())

        self.pyAddTimer(1, 1, gametimer.STATISTIC_STUB_UPDATE)
        return

    def onTimer(self, tid, userArg):
        self._onTimer(tid, userArg)
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        elif userArg == gametimer.STATISTIC_STUB_UPDATE:
            self._updateTick()

    def _updateTick(self):
        # if not gameconfig.enableStatistic():
        #     return

        for spaceNo, sVal in self.statisticDic.items():
            sVal.updateTick()


    def startReportStatistics(self, gbId, playerBox, spaceNo, extraDic):
        LOG_IFO("startReportStatistics", gbId, spaceNo, extraDic)
        if not utils.getCrtMapNeedStatisticFlag(spaceNo):
            LOG_ERR("startReportStatistics space cannot statistic", gbId, spaceNo)
            return

        if spaceNo not in self.statisticDic:
            sVal = Statistics.StatisticsCacheVal(spaceNo, self)
            self.statisticDic[spaceNo] = sVal
        else:
            sVal = self.statisticDic.get(spaceNo)
        sVal.addMemberForSta(gbId, playerBox, extraDic)

    def stopReportStatistics(self, gbId, playBox, spaceNo):
        LOG_IFO("startReportStatistics", gbId, spaceNo)
        sVal = self.statisticDic.get(spaceNo, None)
        if sVal:
            sVal.delMember(gbId)

    def reportStatistics(self, gbId, spaceNo, statisticDic):
        LOG_IFO("reportStatistics", gbId, spaceNo, statisticDic)
        if not utils.getCrtMapNeedStatisticFlag(spaceNo):
            LOG_ERR("reportStatistics space cannot statistic", gbId, spaceNo)
            return

        if spaceNo not in self.statisticDic:
            LOG_ERR("reportStatistics spaceNo not in self.statisticDic", spaceNo)
            return

        sVal = self.statisticDic.get(spaceNo)
        sVal.updateStatistics(gbId, statisticDic)

    def startGetStatistics(self, gbId, playerBox, spaceNo, statisticType, extraDic):
        # LOG_IFO("startGetStatistics", statisticType)
        if not utils.getCrtMapNeedStatisticFlag(spaceNo):
            LOG_ERR("startGetStatistics space cannot statistic", gbId, spaceNo)
            return

        if spaceNo not in self.statisticDic:
            sVal = Statistics.StatisticsCacheVal(spaceNo, self)
            self.statisticDic[spaceNo] = sVal
        else:
            sVal = self.statisticDic.get(spaceNo)

        sVal.startGetStatistics(gbId, playerBox, statisticType, extraDic)

    def stopGetStatistics(self, gbId, spaceNo):
        if not utils.getCrtMapNeedStatisticFlag(spaceNo):
            LOG_IFO("stopGetStatistics space cannot statistic", gbId, spaceNo)
            return

        if spaceNo not in self.statisticDic:
            return

        sVal = self.statisticDic.get(spaceNo)
        sVal.stopGetStatistics(gbId)

    def onSpaceGone(self, spaceNo):
        if not utils.getCrtMapNeedStatisticFlag(spaceNo):
            LOG_IFO("onSpaceGone space cannot statistic", spaceNo)
            return

        if spaceNo in self.statisticDic:
            LOG_IFO("onSpaceGone", spaceNo)
            self.statisticDic.pop(spaceNo)

    def showData(self):
        for spaceNo, sVal in self.statisticDic.items():
            sVal.showData()

    def getStatisticsDetail(self, gbId, playerBox, spaceNo, statisticType, extraDic):
        if not utils.getCrtMapNeedStatisticFlag(spaceNo):
            LOG_ERR("getStatisticsDetail space cannot statistic", gbId, spaceNo)
            return []

        if spaceNo not in self.statisticDic:
            LOG_ERR("getStatisticsDetail spaceNo not in self.statisticDic", spaceNo)
            return []

        sVal = self.statisticDic.get(spaceNo)
        return sVal.getStatisticsDetail(gbId, playerBox, statisticType, extraDic)

    def getDungeonStatisticData(self, spaceNo, uuid, box, statisticType):
        if not utils.getCrtMapNeedStatisticFlag(spaceNo):
            LOG_ERR("getDungeonStatisticData space cannot statistic", spaceNo)
            return {}

        if spaceNo not in self.statisticDic:
            LOG_ERR("getDungeonStatisticData spaceNo not in self.statisticDic", spaceNo)
            return {}

        sVal = self.statisticDic.get(spaceNo)
        return sVal.getDungeonStatisticData(uuid, box, statisticType)
    
    # def getStatisticDetailDatas(self, spaceNo, uuid, box):
