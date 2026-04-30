# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *

import userType
import utils
import gameconst
import gametimer

class PlayerStatisticCacheVal(userType.UserSingleType):
    def __init__(self, gbId, playerBox, extraDic):
        self.gbId = gbId
        self.playerBox = playerBox
        self.name = extraDic.get('name')
        self.school = extraDic.get('school')
        self.dmg = 0
        self.hurt = 0
        self.heal = 0
        self.dead = 0
        self.petDmg = 0
        self.petHurt = 0
        self.petHeal = 0
        self.tStartTime = utils.curTS()
        self.allTime = 0
        self.statisticType = gameconst.StatisticType.STA_TYPE_DAMAGE
        self.lastVersion = 0
        self.isNeedBroadcast = False

    @property
    def isWithPet(self):
        return True if self.statisticType in gameconst.StatisticType.STA_TYPE_WITH_PET else False

    @property
    def dmgWithPet(self):
        return self.dmg + self.petDmg

    @property
    def hurtWithPet(self):
        return self.hurt + self.petHurt

    @property
    def healWithPet(self):
        return self.heal + self.petHeal

    @property
    def dmgPerSecond(self):
        if self.allTime:
            return int(self.dmg/self.allTime)
        return 0

    @property
    def dmgWithPetPerSecond(self):
        if self.allTime:
            return int(self.dmgWithPet/self.allTime)
        return 0

    @property
    def hurtPerSecond(self):
        if self.allTime:
            return int(self.hurt/self.allTime)
        return 0

    @property
    def hurtWithPetPerSecond(self):
        if self.allTime:
            return int(self.hurtWithPet/self.allTime)
        return 0

    @property
    def healPerSecond(self):
        if self.allTime:
            return int(self.heal/self.allTime)
        return 0

    @property
    def healWithPetPerSecond(self):
        if self.allTime:
            return int(self.healWithPet/self.allTime)
        return 0

    def updateStatistics(self, statisticDic):
        self.dmg += statisticDic.get('dmg', 0)
        self.hurt += statisticDic.get('hurt', 0)
        self.heal += statisticDic.get('heal', 0)
        self.dead += statisticDic.get('dead', 0)
        self.petDmg += statisticDic.get('petDmg', 0)
        self.petHurt += statisticDic.get('petHurt', 0)
        self.petHeal += statisticDic.get('petHeal', 0)
        self.allTime += (utils.curTS() - self.tStartTime)
        self.tStartTime = utils.curTS()

    def updateStartTime(self):
        self.tStartTime = utils.curTS()

    def startGetStatistics(self, statisticType, playerBox):
        # if self.isNeedBroadcast and self.statisticType == statisticType:
        #     return

        self.statisticType = statisticType
        self.playerBox = playerBox
        self.lastVersion = 0
        self.isNeedBroadcast = True
        LOG_IFO('startGetStatistics', self.gbId, statisticType)

    def stopGetStatistics(self):
        self.isNeedBroadcast = False
        self.playerBox = None

    def getClientData(self, statisticType):
        clientData = {
            'gbId': self.gbId,
            'name': self.name,
            'school': self.school
            }
        if statisticType == gameconst.StatisticType.STA_TYPE_DAMAGE:
            clientData['statisticsNum'] = self.dmg
        elif statisticType == gameconst.StatisticType.STA_TYPE_DAMAGE_WITH_PET:
            clientData['statisticsNum'] = self.dmgWithPet
            petPercent = int(self.petDmg/self.dmgWithPet * 100) if self.dmgWithPet else 0
            clientData['petPercent'] = petPercent
        elif statisticType == gameconst.StatisticType.STA_TYPE_HURT:
            clientData['statisticsNum'] = self.hurt
        elif statisticType == gameconst.StatisticType.STA_TYPE_HURT_WITH_PET:
            clientData['statisticsNum'] = self.hurtWithPet
            petPercent = int(self.petHurt/self.hurtWithPet * 100) if self.hurtWithPet else 0
            clientData['petPercent'] = petPercent
        elif statisticType == gameconst.StatisticType.STA_TYPE_HEAL:
            clientData['statisticsNum'] = self.heal
        elif statisticType == gameconst.StatisticType.STA_TYPE_HEAL_WITH_PET:
            clientData['statisticsNum'] = self.healWithPet
            petPercent = int(self.petHeal/self.healWithPet * 100) if self.healWithPet else 0
            clientData['petPercent'] = petPercent
        elif statisticType == gameconst.StatisticType.STA_TYPE_DAMAGE_PER_SECOND:
            clientData['statisticsNum'] = self.dmgPerSecond
        elif statisticType == gameconst.StatisticType.STA_TYPE_DAMAGE_WITH_PET_PER_SECOND:
            clientData['statisticsNum'] = self.dmgWithPetPerSecond
            petPercent = int((1 - self.dmgPerSecond/self.dmgWithPetPerSecond) * 100) if self.dmgWithPetPerSecond else 0
            clientData['petPercent'] = petPercent
        elif statisticType == gameconst.StatisticType.STA_TYPE_HURT_PER_SECOND:
            clientData['statisticsNum'] = self.hurtPerSecond
        elif statisticType == gameconst.StatisticType.STA_TYPE_HURT_WITH_PET_PER_SECOND:
            clientData['statisticsNum'] = self.hurtWithPetPerSecond
            petPercent = int((1 - self.hurtPerSecond/self.hurtWithPetPerSecond) * 100) if self.hurtWithPetPerSecond else 0
            clientData['petPercent'] = petPercent
        elif statisticType == gameconst.StatisticType.STA_TYPE_HEAL_PER_SECOND:
            clientData['statisticsNum'] = self.healPerSecond
        elif statisticType == gameconst.StatisticType.STA_TYPE_HEAL_WITH_PET_PER_SECOND:
            clientData['statisticsNum'] = self.healWithPetPerSecond
            petPercent = int((1 - self.healPerSecond/self.healWithPetPerSecond) * 100) if self.healWithPetPerSecond else 0
            clientData['petPercent'] = petPercent
        elif statisticType == gameconst.StatisticType.STA_TYPE_DEAD:
            clientData['statisticsNum'] = self.dead

        return clientData
    
    def getDungeonClientData(self, statisticTypes):
        clientData = {
            'gbId': self.gbId,
            'name': self.name,
            'school': self.school,
            'stDatas':{}
            }
        if utils.bhas(statisticTypes, gameconst.StatisticType.STA_TYPE_DAMAGE):
            clientData['stDatas']['dmg'] = self.dmg
        if utils.bhas(statisticTypes, gameconst.StatisticType.STA_TYPE_HURT):
            clientData['stDatas']['hurt'] = self.hurt
        if utils.bhas(statisticTypes, gameconst.StatisticType.STA_TYPE_HEAL):
            clientData['stDatas']['heal'] = self.heal
        if utils.bhas(statisticTypes, gameconst.StatisticType.STA_TYPE_DEAD):
            clientData['stDatas']['dead'] = self.dead

        return clientData

class StatisticsCacheVal(userType.UserSingleType):
    def __init__(self, spaceNo, owner):
        self.spaceNo = spaceNo
        self.owner = owner
        self.statisticPlayerDic = {}  # type:{int: PlayerStatisticCacheVal}
        self.versionDic = {
            gameconst.StatisticType.STA_TYPE_DAMAGE: 0,
            gameconst.StatisticType.STA_TYPE_DAMAGE_WITH_PET: 0,
            gameconst.StatisticType.STA_TYPE_HURT: 0,
            gameconst.StatisticType.STA_TYPE_HURT_WITH_PET: 0,
            gameconst.StatisticType.STA_TYPE_HEAL: 0,
            gameconst.StatisticType.STA_TYPE_HEAL_WITH_PET: 0,
            gameconst.StatisticType.STA_TYPE_DAMAGE_PER_SECOND: 0,
            gameconst.StatisticType.STA_TYPE_DAMAGE_WITH_PET_PER_SECOND: 0,
            gameconst.StatisticType.STA_TYPE_HURT_PER_SECOND: 0,
            gameconst.StatisticType.STA_TYPE_HURT_WITH_PET_PER_SECOND: 0,
            gameconst.StatisticType.STA_TYPE_HEAL_PER_SECOND: 0,
            gameconst.StatisticType.STA_TYPE_HEAL_WITH_PET_PER_SECOND: 0,
            gameconst.StatisticType.STA_TYPE_DEAD: 0,
        }
        self.dmgRankList = []
        self.hurtRankList = []
        self.healRankList = []
        self.deadRankList = []

        self.dmgWithPetRankList = []
        self.dmgPSRankList = []
        self.dmgWithPetPSRankList = []
        
        self.hurtWithPetRankList = []
        self.hurtPSRankList = []
        self.hurtWithPetPSRankList = []
        
        self.healWithPetRankList = []
        self.healPSRankList = []
        self.healWithPetPSRankList = []

    def addMemberForSta(self, gbId, playerBox, extraDic):
        if gbId in self.statisticPlayerDic:
            pVal = self.statisticPlayerDic.get(gbId)
            pVal.updateStartTime()
        else:
            pVal = PlayerStatisticCacheVal(gbId, playerBox, extraDic)
            self.statisticPlayerDic[gbId] = pVal

    def delMember(self, gbId):
        self.statisticPlayerDic.pop(gbId, None)
        self.resortRank()

    def updateStatistics(self, gbId, statisticDic):
        pVal = self.statisticPlayerDic.get(gbId)
        if not pVal:
            return
        pVal.updateStatistics(statisticDic)

        if statisticDic.get('dmg') or statisticDic.get('petDmg'):
            # self.addStatisticVersion(gameconst.StatisticType.STA_TYPE_DAMAGE_WITH_PET)
            if statisticDic.get('dmg'):
                self.addStatisticVersion(gameconst.StatisticType.STA_TYPE_DAMAGE)
        if statisticDic.get('hurt') or statisticDic.get('petHurt'):
            # self.addStatisticVersion(gameconst.StatisticType.STA_TYPE_HURT_WITH_PET)
            if statisticDic.get('hurt'):
                self.addStatisticVersion(gameconst.StatisticType.STA_TYPE_HURT)
        if statisticDic.get('heal') or statisticDic.get('petHeal'):
            # self.addStatisticVersion(gameconst.StatisticType.STA_TYPE_HEAL_WITH_PET)
            if statisticDic.get('heal'):
                self.addStatisticVersion(gameconst.StatisticType.STA_TYPE_HEAL)
        if statisticDic.get('dead'):
            self.addStatisticVersion(gameconst.StatisticType.STA_TYPE_DEAD)

        # for statisticType in (gameconst.StatisticType.STA_TYPE_DAMAGE_PER_SECOND,
        #                       gameconst.StatisticType.STA_TYPE_DAMAGE_WITH_PET_PER_SECOND,
        #                       gameconst.StatisticType.STA_TYPE_HURT_PER_SECOND,
        #                       gameconst.StatisticType.STA_TYPE_HURT_WITH_PET_PER_SECOND,
        #                       gameconst.StatisticType.STA_TYPE_HEAL_PER_SECOND,
        #                       gameconst.StatisticType.STA_TYPE_HEAL_WITH_PET_PER_SECOND):
        #     self.addStatisticVersion(statisticType)

    def addStatisticVersion(self, statisticType):
        curVersion = self.versionDic[statisticType]
        if curVersion == sys.maxsize:
            self.versionDic[statisticType] = 0
        else:
            self.versionDic[statisticType] =  curVersion + 1

    def showData(self):
        for gbId, pVal in self.statisticPlayerDic.items():
            LOG_IFO('showData', self.spaceNo, gbId, pVal.getClientData(0))

    def startGetStatistics(self, gbId, playerBox, statisticType, extraDic):
        if gbId in self.statisticPlayerDic:
            pVal = self.statisticPlayerDic.get(gbId)
        else:
            pVal = PlayerStatisticCacheVal(gbId, playerBox, extraDic)
            self.statisticPlayerDic[gbId] = pVal

        pVal.startGetStatistics(statisticType, playerBox)

    def stopGetStatistics(self, gbId):
        if gbId not in self.statisticPlayerDic:
            return

        LOG_IFO('stopGetStatistics', self.spaceNo, gbId)
        pVal = self.statisticPlayerDic.get(gbId)
        pVal.stopGetStatistics()

    def resortRank(self):
        statisticList = list(self.statisticPlayerDic.values())
        self.dmgRankList = sorted(statisticList, key=lambda pVal: pVal.dmg, reverse=True)
        # self.dmgWithPetRankList = sorted(statisticList, key=lambda pVal: pVal.dmgWithPet, reverse=True)
        # self.dmgPSRankList = sorted(statisticList, key=lambda pVal: pVal.dmgPerSecond, reverse=True)
        # self.dmgWithPetPSRankList = sorted(statisticList, key=lambda pVal: pVal.dmgWithPetPerSecond, reverse=True)
        self.hurtRankList = sorted(statisticList, key=lambda pVal: pVal.hurt, reverse=True)
        # self.hurtWithPetRankList = sorted(statisticList, key=lambda pVal: pVal.hurtWithPet, reverse=True)
        # self.hurtPSRankList = sorted(statisticList, key=lambda pVal: pVal.hurtPerSecond, reverse=True)
        # self.hurtWithPetPSRankList = sorted(statisticList, key=lambda pVal: pVal.hurtWithPetPerSecond, reverse=True)
        self.healRankList = sorted(statisticList, key=lambda pVal: pVal.heal, reverse=True)
        # self.healWithPetRankList = sorted(statisticList, key=lambda pVal: pVal.healWithPet, reverse=True)
        # self.healPSRankList = sorted(statisticList, key=lambda pVal: pVal.healPerSecond, reverse=True)
        # self.healWithPetPSRankList = sorted(statisticList, key=lambda pVal: pVal.healWithPetPerSecond, reverse=True)
        self.deadRankList = sorted(statisticList, key=lambda pVal: pVal.dead, reverse=True)

    def updateTick(self):
        self.resortRank()

        self.owner.batchlyCall(self._sendStatistics(), 30)

    def _sendStatistics(self):
        maxRankCount = 5
        for gbId, pVal in self.statisticPlayerDic.items():
            if not pVal.playerBox or not pVal.isNeedBroadcast:
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

            # LOG_IFO("_sendStatistics: ", gbId, sData)

            yield lambda: pVal.playerBox.onGetStatistics(pVal.statisticType, sData)

    def getRankList(self, statisticType):
        if statisticType == gameconst.StatisticType.STA_TYPE_DAMAGE:
            return self.dmgRankList
        elif statisticType == gameconst.StatisticType.STA_TYPE_DAMAGE_WITH_PET:
            return self.dmgWithPetRankList
        elif statisticType == gameconst.StatisticType.STA_TYPE_HURT:
            return self.hurtRankList
        elif statisticType == gameconst.StatisticType.STA_TYPE_HURT_WITH_PET:
            return self.hurtWithPetRankList
        elif statisticType == gameconst.StatisticType.STA_TYPE_HEAL:
            return self.healRankList
        elif statisticType == gameconst.StatisticType.STA_TYPE_HEAL_WITH_PET:
            return self.healWithPetRankList
        elif statisticType == gameconst.StatisticType.STA_TYPE_DAMAGE_PER_SECOND:
            return self.dmgPSRankList
        elif statisticType == gameconst.StatisticType.STA_TYPE_DAMAGE_WITH_PET_PER_SECOND:
            return self.dmgWithPetPSRankList
        elif statisticType == gameconst.StatisticType.STA_TYPE_HURT_PER_SECOND:
            return self.hurtPSRankList
        elif statisticType == gameconst.StatisticType.STA_TYPE_HURT_WITH_PET_PER_SECOND:
            return self.hurtWithPetPSRankList
        elif statisticType == gameconst.StatisticType.STA_TYPE_HEAL_PER_SECOND:
            return self.healPSRankList
        elif statisticType == gameconst.StatisticType.STA_TYPE_HEAL_WITH_PET_PER_SECOND:
            return self.healWithPetPSRankList
        elif statisticType == gameconst.StatisticType.STA_TYPE_DEAD:
            return self.deadRankList

    def _lateReload(self):
        super(StatisticsCacheVal, self)._lateReload()

        for v in self.statisticPlayerDic.values():
            v.reloadScript()

        return

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
        LOG_IFO('getDungeonStatisticData', self.spaceNo, uuid, statisticType)

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
