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
        if dungeonNo == formula.parseDungeonNoBySpaceNo(self.spaceNo):
            if dungeonPlayMode == gameconst.DungeonPlayModeEnum.CRUSADE:
                if formula.inTeamDungeonScene(self.spaceNo):
                    return dungeonNo, gameconst.DungeonEnterTypeEnum.TEAM
            elif dungeonPlayMode == gameconst.DungeonPlayModeEnum.CHIEF:
                if formula.inRaidDungeonScene(self.spaceNo):
                    return dungeonNo, gameconst.DungeonEnterTypeEnum.RAID
            elif dungeonPlayMode == gameconst.DungeonPlayModeEnum.GUILD_BOSS:
                if formula.inGuildBossDungeonScene(self.spaceNo):
                    return dungeonNo, gameconst.DungeonEnterTypeEnum.GUILD
        return None, None

    def getSettlementRankList(self, exposed, rankType, dungeonNo, dungeonPlayMode, idx, offset):
        if not self.checkDungeonVisibleConfigEnabled(dungeonPlayMode):
            return
        LOG_IFO('IDungeonSettlement::getSettlementRankList:', exposed, rankType, dungeonNo, dungeonPlayMode, idx, offset)
        if rankType not in gameconst.StatisticType.DUNGEON_VALID_TYPES:
            LOG_ERR('IDungeonSettlement::getSettlementRankList, wrong args 0:', exposed, rankType, dungeonNo, dungeonPlayMode, idx, offset)
            return
        dungeonNo, dungeonEnterType = self._calcDungeonEnterType(dungeonNo, dungeonPlayMode)
        if dungeonNo and dungeonEnterType:    
            dungeonStub = gameengine.getDungeonStubByDungeonNo(dungeonNo, dungeonEnterType)
            dungeonStub.getSettlementRankList(rankType, self.spaceNo, self.guildUUID, self.base, self.gbId, idx, offset)
        else:
            LOG_ERR('IDungeonSettlement::getSettlementRankList, wrong args 1:', exposed, rankType, dungeonNo, dungeonPlayMode, idx, offset)

    def checkDungeonVisibleConfigEnabled(self, dungeonPlayMode):
        LOG_IFO('IDungeonSettlement::checkDungeonVisibleConfigEnabled: begin ', dungeonPlayMode)
        ret = True
        if dungeonPlayMode == gameconst.DungeonPlayModeEnum.CRUSADE:
            if not gameconfig.visibleConfigEnabled('teamDungeon'):
                ret = False
        elif dungeonPlayMode == gameconst.DungeonPlayModeEnum.CHIEF:
            if not gameconfig.visibleConfigEnabled('raidDungeon'):
                ret = False
        elif dungeonPlayMode == gameconst.DungeonPlayModeEnum.GUILD_BOSS:
            if not gameconfig.visibleConfigEnabled('guildBossChallenge'):
                ret = False

        LOG_IFO('IDungeonSettlement::checkDungeonVisibleConfigEnabled: end ', dungeonPlayMode, ret)
        return ret