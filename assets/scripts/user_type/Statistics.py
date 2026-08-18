# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *

import userType
import utils
import gameconst
import gametimer

class PlayerStatisticCacheVal(userType.UserSingleType):
    def __init__(self, gbId, playerBox, extraDic):
        self.playerBox = playerBox
        self.gbId = gbId
        self.name = extraDic.get('name')
        self.dmg = 0
        self.school = extraDic.get('school')
        self.hurt = 0
        self.dead = 0
        self.heal = 0
        self.allTime = 0
        self.tStartTime = utils.curTS()
        self.statisticType = gameconst.StatisticEnum.STA_TYPE_DAMAGE
        self.isNeedBroadcast = False
        self.lastVersion = 0

    def dmgPerSecond(self):
        if self.allTime:
            return int(self.dmg/self.allTime)
        return 0

    def hurtPerSecond(self):
        if self.allTime:
            return int(self.hurt/self.allTime)
        return 0

    def healPerSecond(self):
        if self.allTime:
            return int(self.heal/self.allTime)
        return 0

    def updateStatistics(self, statisticDic):
        self.dmg += statisticDic.get('dmg', 0)
        self.hurt += statisticDic.get('hurt', 0)
        self.heal += statisticDic.get('heal', 0)
        self.dead += statisticDic.get('dead', 0)
        self.allTime += (utils.curTS() - self.tStartTime)
        self.tStartTime = utils.curTS()

    def updateStartTime(self):
        self.tStartTime = utils.curTS()

    def startGetStatistics(self, statisticType, playerBox):
        self.playerBox = playerBox
        self.statisticType = statisticType
        self.lastVersion = 0
        self.isNeedBroadcast = True
        LOG_INFO('startGetStatistics', self.gbId, statisticType)

    def stopGetStatistics(self):
        self.playerBox = None
        self.isNeedBroadcast = False

    def getClientData(self, statisticType):
        clientData = {
            'name': self.name,
            'gbId': self.gbId,
            'school': self.school,
            }
        if statisticType == gameconst.StatisticEnum.STA_TYPE_DAMAGE:
            clientData['statisticsNum'] = self.dmg
        elif statisticType == gameconst.StatisticEnum.STA_TYPE_HURT:
            clientData['statisticsNum'] = self.hurt
        elif statisticType == gameconst.StatisticEnum.STA_TYPE_HEAL:
            clientData['statisticsNum'] = self.heal
        elif statisticType == gameconst.StatisticEnum.STA_TYPE_DAMAGE_PER_SECOND:
            clientData['statisticsNum'] = self.dmgPerSecond()
        elif statisticType == gameconst.StatisticEnum.STA_TYPE_HURT_PER_SECOND:
            clientData['statisticsNum'] = self.hurtPerSecond()
        elif statisticType == gameconst.StatisticEnum.STA_TYPE_HEAL_PER_SECOND:
            clientData['statisticsNum'] = self.healPerSecond()
        elif statisticType == gameconst.StatisticEnum.STA_TYPE_DEAD:
            clientData['statisticsNum'] = self.dead

        return clientData
    
    def getDungeonClientData(self, statisticTypes):
        clientData = {
            'gbId': self.gbId,
            'name': self.name,
            'school': self.school,
            'stDatas':{}
            }
        if utils.bhas(statisticTypes, gameconst.StatisticEnum.STA_TYPE_DAMAGE):
            clientData['stDatas']['dmg'] = self.dmg
        if utils.bhas(statisticTypes, gameconst.StatisticEnum.STA_TYPE_HURT):
            clientData['stDatas']['hurt'] = self.hurt
        if utils.bhas(statisticTypes, gameconst.StatisticEnum.STA_TYPE_HEAL):
            clientData['stDatas']['heal'] = self.heal
        if utils.bhas(statisticTypes, gameconst.StatisticEnum.STA_TYPE_DEAD):
            clientData['stDatas']['dead'] = self.dead

        return clientData

class StatisticsCacheVal(userType.UserSingleType):
    def __init__(self, spaceNo, owner):
        self.owner = owner
        self.spaceNo = spaceNo
        self.statisticPlayerDic = {}  # type:{int: PlayerStatisticCacheVal}
        self.versionDic = {
            gameconst.StatisticEnum.STA_TYPE_HURT: 0,
            gameconst.StatisticEnum.STA_TYPE_DAMAGE: 0,
            gameconst.StatisticEnum.STA_TYPE_HEAL: 0,
            gameconst.StatisticEnum.STA_TYPE_DAMAGE_PER_SECOND: 0,
            gameconst.StatisticEnum.STA_TYPE_HURT_PER_SECOND: 0,
            gameconst.StatisticEnum.STA_TYPE_HEAL_PER_SECOND: 0,
            gameconst.StatisticEnum.STA_TYPE_DEAD: 0,
        }
        self.dmgRankList = []
        self.hurtRankList = []
        self.healRankList = []
        self.deadRankList = []

        self.dmgPSRankList = []
        
        self.hurtPSRankList = []
        
        self.healPSRankList = []

    def addMemberForSta(self, gbId, playerBox, extraDic):
        if gbId in self.statisticPlayerDic:
            _pVal = self.statisticPlayerDic.get(gbId)
            _pVal.updateStartTime()
        else:
            _pVal = PlayerStatisticCacheVal(gbId, playerBox, extraDic)
            self.statisticPlayerDic[gbId] = _pVal

    def delMember(self, gbId):
        self.statisticPlayerDic.pop(gbId, None)
        self.resortRank()

    def updateStatistics(self, gbId, statisticDic):
        pVal = self.statisticPlayerDic.get(gbId)
        if not pVal:
            return
        pVal.updateStatistics(statisticDic)

        if statisticDic.get('dmg'):
            self.addStatisticVersion(gameconst.StatisticEnum.STA_TYPE_DAMAGE)

        if statisticDic.get('hurt'):
            self.addStatisticVersion(gameconst.StatisticEnum.STA_TYPE_HURT)

        if statisticDic.get('heal'):
            self.addStatisticVersion(gameconst.StatisticEnum.STA_TYPE_HEAL)

        if statisticDic.get('dead'):
            self.addStatisticVersion(gameconst.StatisticEnum.STA_TYPE_DEAD)

    def addStatisticVersion(self, statisticType):
        _curVersion = self.versionDic[statisticType]
        if _curVersion == sys.maxsize:
            self.versionDic[statisticType] = 0
        else:
            self.versionDic[statisticType] =  _curVersion + 1

    def showData(self):
        for gbId, pVal in self.statisticPlayerDic.items():
            LOG_INFO('showData', self.spaceNo, gbId, pVal.getClientData(0))

    def startGetStatistics(self, gbId, playerBox, statisticType, extraDic):
        if gbId in self.statisticPlayerDic:
            _pVal = self.statisticPlayerDic.get(gbId)
        else:
            _pVal = PlayerStatisticCacheVal(gbId, playerBox, extraDic)
            self.statisticPlayerDic[gbId] = _pVal

        _pVal.startGetStatistics(statisticType, playerBox)

    def stopGetStatistics(self, gbId):
        if gbId not in self.statisticPlayerDic:
            return

        LOG_INFO('stopGetStatistics', self.spaceNo, gbId)
        _pVal = self.statisticPlayerDic.get(gbId)
        _pVal.stopGetStatistics()

    def resortRank(self):
        _statisticList = list(self.statisticPlayerDic.values())
        self.dmgRankList = sorted(_statisticList, key=lambda pVal: pVal.dmg, reverse=True)
        self.hurtRankList = sorted(_statisticList, key=lambda pVal: pVal.hurt, reverse=True)
        self.healRankList = sorted(_statisticList, key=lambda pVal: pVal.heal, reverse=True)
        self.deadRankList = sorted(_statisticList, key=lambda pVal: pVal.dead, reverse=True)

    def updateTick(self):
        self.resortRank()

        self.owner.batchlyCall(self._sendStatistics(), 30)

    def _sendStatistics(self):
        maxRankCount = 5
        gbIds = list(self.statisticPlayerDic.keys())
        for gbId in gbIds:
            pVal = self.statisticPlayerDic.get(gbId)
            if not pVal or not pVal.playerBox or not pVal.isNeedBroadcast:
                continue

            if utils.checkBoxOffline(pVal.playerBox):
                pVal.stopGetStatistics()
                continue

            if self.versionDic[pVal.statisticType] == 0 or (pVal.lastVersion and pVal.lastVersion == self.versionDic[pVal.statisticType]):
                continue
            rankList = self.getRankList(pVal.statisticType)
            selfRank = 0
            sData = []
            for i, rankVal in enumerate(rankList):
                if rankVal.gbId == pVal.gbId:
                    selfRank = i + 1
                if len(sData) < maxRankCount:
                    cVal = rankVal.getClientData(pVal.statisticType)
                    cVal['rank'] = i + 1
                    sData.append(cVal)
                elif selfRank > 0:
                    break

            if selfRank > len(sData):
                selfData = pVal.getClientData(pVal.statisticType)
                selfData['rank'] = selfRank
                sData[-1] = selfData

            pVal.lastVersion = self.versionDic[pVal.statisticType]

            yield lambda: pVal.playerBox.onGetStatistics(pVal.statisticType, sData)

    def getRankList(self, statisticType):
        if statisticType == gameconst.StatisticEnum.STA_TYPE_DAMAGE:
            return self.dmgRankList
        elif statisticType == gameconst.StatisticEnum.STA_TYPE_HURT:
            return self.hurtRankList
        elif statisticType == gameconst.StatisticEnum.STA_TYPE_HEAL:
            return self.healRankList
        elif statisticType == gameconst.StatisticEnum.STA_TYPE_DAMAGE_PER_SECOND:
            return self.dmgPSRankList
        elif statisticType == gameconst.StatisticEnum.STA_TYPE_HURT_PER_SECOND:
            return self.hurtPSRankList
        elif statisticType == gameconst.StatisticEnum.STA_TYPE_HEAL_PER_SECOND:
            return self.healPSRankList
        elif statisticType == gameconst.StatisticEnum.STA_TYPE_DEAD:
            return self.deadRankList

    def _lateReload(self):
        super(StatisticsCacheVal, self)._lateReload()

        for _v in self.statisticPlayerDic.values():
            _v.reloadScript()

    def getStatisticsDetail(self, gbId, playerBox, statisticType, extraDic):
        self.detailRankList = self.getRankList(statisticType)
        if not self.detailRankList:
            return
        
        batchCount = extraDic.get('batchCount', 10)
        allCount = extraDic.get('allCount', len(self.detailRankList))
        allCount = min(allCount, len(self.detailRankList))
        self.detailRankList = self.detailRankList[:allCount]
        cache = extraDic.get('cache', False)
        self.owner.batchlyCall(self._sendStatisticsDetail(gbId, playerBox, statisticType, cache, batchCount, allCount), 2)
        
    def _sendStatisticsDetail(self, gbId, playerBox, statisticType, cache, batchCount, allCount):
        batchSize = (allCount + batchCount -1)//batchCount

        for i in range(0, allCount, batchCount):
            batch = self.detailRankList[i:i+batchCount]
            sData = []
            for j, val in enumerate(batch):
                valData = val.getClientData(statisticType)
                valData['rank'] = i + j + 1
                sData.append(valData)

            yield lambda : playerBox.onGetStatisticsDetail(cache, statisticType, batchSize, i//batchCount+1, sData)

    def getDungeonStatisticData(self, uuid, box, statisticType):
        self.detailRankList = self.getRankList(statisticType)
        self.owner.batchlyCall(self.doDisptachStatisticDatas(uuid, statisticType, self.detailRankList, 20, box), 1, 0.1)
        LOG_INFO('getDungeonStatisticData', self.spaceNo, uuid, statisticType)

    def doDisptachStatisticDatas(self, uuid, statisticType, allDatas, batchSize, box):
        if not allDatas:
            box.onDungeonStatisticData(0, 0, self.spaceNo, uuid, statisticType, [])
            return
        
        allCount = len(allDatas)
        if allCount > batchSize:
            batchCount = allCount // batchSize
            if allCount > batchCount * batchSize:
                batchCount += 1
            totalBatchCount = batchCount
        else:
            batchSize = allCount
            totalBatchCount = 1
        batchIdx = 0
        for idx in range(0, allCount, batchSize):
            batch = allDatas[idx:idx+batchSize]
            datas = []
            for j, val in enumerate(batch):
                data = val.getClientData(statisticType)
                data['rank'] = idx + j + 1
                datas.append(data)
            batchIdx += 1
            LOG_DBG('_sendRank', allCount, totalBatchCount, batchIdx, batchSize, self.spaceNo, uuid, statisticType, datas)
            yield lambda : box.onDungeonStatisticData(totalBatchCount, batchIdx, self.spaceNo, uuid, statisticType, datas)
