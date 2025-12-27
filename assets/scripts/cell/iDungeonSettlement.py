# coding: utf-8
from KBEDebug import *
import KBEngine

import gameconst
import dataUtils
import dropAward
import gameclass
import mailAssistor
import gamedecorator
import gameengine
import formula

import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import raidBossChallenge_config as RBC_CFG
import raidBossChallenge_basicInfo as RBC_BI
import teamDunChallenge_basicInfo as TDC_BI
import guildChallenge_basicInfo as GC_BI
import guildChallenge_config as GC_C

class IDungeonSettlement(object):
    def __init__(self):
        pass
    
    def _calcDungeonEnterType(self, dungeonNo, dungeonPlayMode):
        if dungeonNo == formula.getDungeonNoBySpaceNo(self.spaceNo):
            if dungeonPlayMode == gameconst.DungeonPlayModeEnum.CRUSADE:
                if formula.isTeamDungeonSpace(self.spaceNo):
                    return dungeonNo, gameconst.DungeonEnterType.TEAM
            elif dungeonPlayMode == gameconst.DungeonPlayModeEnum.CHIEF:
                if formula.isRaidDungeonSpace(self.spaceNo):
                    return dungeonNo, gameconst.DungeonEnterType.RAID
            elif dungeonPlayMode == gameconst.DungeonPlayModeEnum.GUILD_BOSS:
                if formula.isGuildBossDungeonSpace(self.spaceNo):
                    return dungeonNo, gameconst.DungeonEnterType.GUILD
        return None, None

    def getSettlementRankList(self, exposed, rankType, dungeonNo, dungeonPlayMode, idx, offset):
        INFO_MSG('IDungeonSettlement::getSettlementRankList:', exposed, rankType, dungeonNo, dungeonPlayMode, idx, offset)
        if rankType not in gameconst.StatisticType.DUNGEON_VALID_TYPES:
            ERROR_MSG('IDungeonSettlement::getSettlementRankList, wrong args 0:', exposed, rankType, dungeonNo, dungeonPlayMode, idx, offset)
            return
        dungeonNo, dungeonEnterType = self._calcDungeonEnterType(dungeonNo, dungeonPlayMode)
        if dungeonNo and dungeonEnterType:    
            dungeonStub = gameengine.getDungeonStubByDungeonNo(dungeonNo, dungeonEnterType)
            dungeonStub.getSettlementRankList(rankType, self.spaceNo, self.guildUUID, self.base, self.gbId, idx, offset)
        else:
            ERROR_MSG('IDungeonSettlement::getSettlementRankList, wrong args 1:', exposed, rankType, dungeonNo, dungeonPlayMode, idx, offset)  