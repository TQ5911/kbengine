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

    def __init__(self, **kwargs):
        super(StatisticStub, self).__init__()
        LOG_INFO("StatisticStub  __init__", self.classname())
        self.statisticDic = {}

    def postReloadScript(self):
        super(StatisticStub, self).postReloadScript()
        for _v in self.statisticDic.values():
            _v.reloadScript()

    def doNext(self):
        gameglobal.localBaseApp.fullPrepare(self.classname())
        self.pyAddTimer(1, 1, gametimer.STATISTIC_STUB_UPDATE)

    def onTimer(self, tid, userArg):
        self._onTimerTrigger(tid, userArg)
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        elif userArg == gametimer.STATISTIC_STUB_UPDATE:
            self._updateTick()

    def _updateTick(self):
        for sVal in self.statisticDic.values():
            sVal.updateTick()

    def startReportStatistics(self, gbId, playerBox, spaceNo, extraDic):
        LOG_INFO("startReportStatistics", gbId, spaceNo, extraDic)
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
        LOG_INFO("startReportStatistics", gbId, spaceNo)
        sVal = self.statisticDic.get(spaceNo, None)
        if sVal:
            sVal.delMember(gbId)

    def reportStatistics(self, gbId, spaceNo, statisticDic):
        LOG_INFO("reportStatistics", gbId, spaceNo, statisticDic)
        if not utils.getCrtMapNeedStatisticFlag(spaceNo):
            LOG_ERR("reportStatistics space cannot statistic", gbId, spaceNo)
            return

        if spaceNo not in self.statisticDic:
            LOG_ERR("reportStatistics spaceNo not in self.statisticDic", spaceNo)
            return

        _sVal = self.statisticDic.get(spaceNo)
        _sVal.updateStatistics(gbId, statisticDic)

    def startGetStatistics(self, gbId, playerBox, spaceNo, statisticType, extraDic):
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
            LOG_INFO("stopGetStatistics space cannot statistic", gbId, spaceNo)
            return

        if spaceNo not in self.statisticDic:
            return

        _sVal = self.statisticDic.get(spaceNo)
        _sVal.stopGetStatistics(gbId)

    def onSpaceGone(self, spaceNo):
        if not utils.getCrtMapNeedStatisticFlag(spaceNo):
            LOG_INFO("onSpaceGone space cannot statistic", spaceNo)
            return

        if spaceNo in self.statisticDic:
            LOG_INFO("onSpaceGone", spaceNo)
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
