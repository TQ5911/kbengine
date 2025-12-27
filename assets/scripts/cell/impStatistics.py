# -*- coding: utf-8 -*-

from KBEDebug import *

import KBEngine

import time
import gameconst
import gameengine
import utils
import formula
import sMath
import gamedecorator

class IStatistics(object):
    def __init__(self):
        self.currStatisticSpaceNo = 0

    def startReportStatistics(self):
        """
        开始统计数据
        """
        if not utils.getCrtMapNeedStatisticFlag(self.spaceNo):
            return

        if self.currStatisticSpaceNo == self.spaceNo:
            return
        self.currStatisticSpaceNo = self.spaceNo
        INFO_MSG('IStatistics::startReportStatistics: entityID={}'.format(self.id))

        stub = gameengine.getStatisticStub(self.spaceNo)
        stub.startReportStatistics(self.gbId, self.base, self.spaceNo, {'name': self.name, 'school': self.school})

    def stopReportStatistics(self):
        """
        停止统计数据并上报
        """
        INFO_MSG('IStatistics::stopReportStatistics: entityID={}'.format(self.id))
        
    # 上报统计数据
    def recordStatistic(self, key, value):
        """
        记录一项统计数据
        """
        if not utils.getCrtMapNeedStatisticFlag(self.spaceNo):
            return

        INFO_MSG('IStatistics::recordStatistic: entityID={}, key={}, value={}'.format(self.id, key, value))
        stub = gameengine.getStatisticStub(self.spaceNo)
        stub.reportStatistics(self.gbId, self.spaceNo, {key: value})

    # @utils.isMyself
    def reqStartGetStatistics(self, exposed, statisticType):
        """
        请求获取统计数据
        """
        if not utils.getCrtMapNeedStatisticFlag(self.spaceNo):
            return

        stub = gameengine.getStatisticStub(self.spaceNo)
        stub.startGetStatistics(self.gbId, self.base, self.spaceNo, statisticType, {'name': self.name, 'school': self.school})

        # self.reqGetStatisticsDetail(exposed, statisticType)

    # @utils.isMyself
    def reqStopGetStatistics(self, exposed):
        """
        请求停止获取统计数据
        """

        stub = gameengine.getStatisticStub(self.spaceNo)
        stub.stopGetStatistics(self.gbId, self.spaceNo)

    # @utils.isMyself
    @gamedecorator.limitcall(3)
    def reqGetStatisticsDetail(self, exposed, statisticType):
        """
        请求获取统计数据详情
        """
        if not utils.getCrtMapNeedStatisticFlag(self.spaceNo):
            return

        stub = gameengine.getStatisticStub(self.spaceNo)
        stub.getStatisticsDetail(self.gbId, self.base, self.spaceNo, statisticType, {'batchCount': 10, 'allCount': 80})

    # @utils.isMyself
    @gamedecorator.limitcall(3)
    def reqClearStatistics(self, exposed, statisticType):
        """
        请求清除统计数据
        """
        if not utils.getCrtMapNeedStatisticFlag(self.spaceNo):
            return

        stub = gameengine.getStatisticStub(self.spaceNo)
        stub.getStatisticsDetail(self.gbId, self.base, self.spaceNo, statisticType, {'batchCount': 10, 'allCount': 80, 'cache': True})