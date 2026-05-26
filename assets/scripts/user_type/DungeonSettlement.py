# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *

import userType
import awardContext
import gameconst
import dataUtils
import dropAward

import teamMatch_matchConfig as TMMCD
import guildChallenge_rankReward as GC_RR
import guildChallenge_basicInfo as GC_BI
import guildChallenge_config as GC_C
import raidBossChallenge_basicInfo as RBC_BI
import teamDunChallenge_basicInfo as TDC_BI
import teamMatch_pointsRanking as TM_PR

class DungeonExtraData(userType.UserSingleType):
    def __init__(self, gbId = 0, name = '', school = 0, level = 0, sex = 0, eId = 0):
        self.gbId = gbId
        self.name = name
        self.school = school
        self.level = level
        self.sex = sex
        self.eId = eId

    def toSavedDict(self):
        return {
            'gbId': self.gbId,
            'name': self.name,
            'school': self.school,
            'level': self.level,
            'sex': self.sex,
            'eId': self.eId,
        }

    def createObjFromDict(self, dataDict):
        obj = DungeonExtraData(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toSavedDict()

    def isSameType(self, obj):
        return type(obj) is DungeonExtraData
    
    def loadDatas(self, extra):
        self.gbId = extra.get('gbId')
        self.name = extra.get('name')
        self.school = extra.get('school')
        self.level = extra.get('level')
        self.sex = extra.get('sex')
        self.eId = extra.get('eId')

DungeonExtraDataInstance = DungeonExtraData()

class DungeonSettlementData(userType.UserSingleType):
    def __init__(self):
        self.gbId = 0
        self.name = ''
        self.win = 0
        self.rank = 0
        self.score = 0
        self.sex = 0
        self.level = 0
        self.school = 0
        self.dungeonRewards = []
        self.firstPassRewards = []
        self.goldPassRewards = []

    def toClientData(self):
        return {
            'gbId': self.gbId,
            'name': self.name,
            'rank': self.rank,
            'score': self.score,
            'sex': self.sex,
            'level': self.level,
            'school': self.school,
            'dungeonRewards': self.dungeonRewards,
            'firstPassRewards': self.firstPassRewards,
            'goldPassRewards': self.goldPassRewards,
        }
    
    def _calcGuildBossSettlement(self, box, rewardDatas, opUUId, uniqueId, entity, spaceNo, dungeonNo, dungeonExtraDatas, win, dungeonStatisticRecords):
        # 公会副本结算有排名奖励
        dmgRankData = dungeonStatisticRecords.get(gameconst.StatisticEnum.STA_TYPE_DAMAGE, {}).get(dungeonExtraDatas.gbId, None)
        if dmgRankData:
            extra = self._getDungeonExtraData(rewardDatas, dungeonExtraDatas, win, dmgRankData['rank'], dmgRankData['statisticsNum'])
        else:
            extra = self._getDungeonExtraData(rewardDatas, dungeonExtraDatas, win, 0, 0)

        entity.base.onDungeonSettlement(gameconst.DungeonPlayModeEnum.GUILD_BOSS, spaceNo, dungeonNo, opUUId, uniqueId, win, box, extra)

    def _calcCrusadeSettlement(self, box, rewardDatas, opUUId, uniqueId, entity, spaceNo, dungeonNo, dungeonExtraDatas, win, score, extra):
        datas = self._getDungeonExtraData(rewardDatas, dungeonExtraDatas, win, 0, score)
        extra.update(datas)
        entity.base.onDungeonSettlement(gameconst.DungeonPlayModeEnum.CRUSADE, spaceNo, dungeonNo, opUUId, uniqueId, win, box, extra)

    def _calcChiefSettlement(self, box, rewardDatas, opUUId, uniqueId, entity, spaceNo, dungeonNo, dungeonExtraDatas, win, score, extra):
        datas = self._getDungeonExtraData(rewardDatas, dungeonExtraDatas, win, 0, score)
        extra.update(datas)
        entity.base.onDungeonSettlement(gameconst.DungeonPlayModeEnum.CHIEF, spaceNo, dungeonNo, opUUId, uniqueId, win, box, extra)

    def _getDungeonExtraData(self, rewardDatas, dungeonExtraDatas, win, rank, score):
        extra = {}
        extra['win'] = win
        extra['rank'] = rank
        extra['score'] = score
        extra['gbId'] = dungeonExtraDatas.gbId
        extra['name'] = dungeonExtraDatas.name
        extra['sex'] = dungeonExtraDatas.sex
        extra['school'] = dungeonExtraDatas.school
        extra['level'] = dungeonExtraDatas.level

        rewardData = rewardDatas.setdefault(dungeonExtraDatas.gbId, {})
        rewardData['wait'] = True

        return extra
