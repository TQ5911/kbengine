# coding: utf-8
import gameglobal
from KBEDebug import *
import KBEngine

import random
import json

import gameengine
import gameconst
import gameconfig
import gametimer
import formula
import dataUtils
import utils

class IStatistics(object):

    def checkStatisticRecordSpace(self):
        """
        检查统计记录的场景是否变化，变化则重置记录
        """
        recordSpaceNo = self.getTempMiscProp(gameconst.AvatarProps.statisticDataRecordSpaceNo, 0)
        if recordSpaceNo != self.baseSpaceNo:
            self.setTempMiscProp(gameconst.AvatarProps.statisticDataRecord, {})
            self.setTempMiscProp(gameconst.AvatarProps.statisticDataRecordSpaceNo, self.baseSpaceNo)

    def onLeaveStatisticSpace(self, fromSpaceNo):
        """
        离开场景回调
        """
        # 缓存清除
        self.setTempMiscProp(gameconst.AvatarProps.statisticDataRecord, {})
        recordSpaceNo = self.getTempMiscProp(gameconst.AvatarProps.statisticDataRecordSpaceNo, 0)
        if recordSpaceNo != 0:
            self.setTempMiscProp(gameconst.AvatarProps.statisticDataRecordSpaceNo, 0)
            stub = gameengine.getStatisticStub(recordSpaceNo)
            stub.stopGetStatistics(self.gbID, recordSpaceNo)

    def onGetStatistics(self, statisticType, data):
        """
        统计数据回调
        """
        self.checkStatisticRecordSpace()

        dataRecord = self.getTempMiscProp(gameconst.AvatarProps.statisticDataRecord, {})
        for i, val in enumerate(data):
            gbId = val.get('gbId', 0)
            if gbId == 0:
                continue
            # val['rank'] = i + 1
            val['statisticsNum'] -= dataRecord.get(statisticType, {}).get(gbId, 0)

        INFO_MSG('IStatistics::onGetStatistics: entityID={}, statisticType={}, data={}'.format(self.id, statisticType, data))
        self.client.onGetStatisticsClient(statisticType, data)
    
    def onGetStatisticsDetail(self, cache, statisticType, batchSize, batchNo, data):
        """
        统计数据详情回调
        """
        # IStatistics::onGetStatisticsDetail: entityID=6272, batchSize=1, batchNo=1, data=[{'gbId': 5700768059476672513, 'name': '郑槿言', 'school': 1001, 'statisticsNum': 348, 'rank': 1}]
        INFO_MSG('IStatistics::onGetStatisticsDetail: entityID={}, cache={}, statisticType={}, batchSize={}, batchNo={}, dataSize={}'.format(self.id, cache, statisticType, batchSize, batchNo, len(data)))
        self.checkStatisticRecordSpace()

        dataRecord = self.getTempMiscProp(gameconst.AvatarProps.statisticDataRecord, {})
        # 本次是拉取缓存
        if cache:
            for val in data:
                gbId = val.get('gbId', 0)
                if gbId == 0:
                    continue
                if statisticType not in dataRecord:
                    dataRecord[statisticType] = {}
                dataRecord[statisticType][gbId] = val.get('statisticsNum', 0)
            self.setTempMiscProp(gameconst.AvatarProps.statisticDataRecord, dataRecord)
            return

        for val in data:
            gbId = val.get('gbId', 0)
            if gbId == 0:
                continue
            val['statisticsNum'] -= dataRecord.get(statisticType, {}).get(gbId, 0)

        self.client.onGetStatisticsDetailClient(statisticType, batchSize, batchNo, data)
