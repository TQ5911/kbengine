# coding: utf-8
from KBEDebug import *

import gameconst
import gameengine
import formula
import gameconfig

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
        if not self.checkDungeonVisibleConfigEnabled(dungeonPlayMode):
            return
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

    def checkDungeonVisibleConfigEnabled(self, dungeonPlayMode):
        INFO_MSG('IDungeonSettlement::checkDungeonVisibleConfigEnabled: begin ', dungeonPlayMode)
        ret = True
        if dungeonPlayMode == gameconst.DungeonPlayModeEnum.CRUSADE:
            if not gameconfig.visibleConfigEable('teamDungeon'):
                ret = False
        elif dungeonPlayMode == gameconst.DungeonPlayModeEnum.CHIEF:
            if not gameconfig.visibleConfigEable('raidDungeon'):
                ret = False
        elif dungeonPlayMode == gameconst.DungeonPlayModeEnum.GUILD_BOSS:
            if not gameconfig.visibleConfigEable('guildBossChallenge'):
                ret = False

        INFO_MSG('IDungeonSettlement::checkDungeonVisibleConfigEnabled: end ', dungeonPlayMode, ret)
        return ret