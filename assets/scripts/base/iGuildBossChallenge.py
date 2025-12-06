#coding: utf-8

from KBEDebug import *

import gamedecorator
import utils
import gameconst
import AuthClsWraper
import agent_agentFunction as A_AFD
import guildChallenge_basicInfo as GCBI
import guildChallenge_config as GCC
import gamePlay_gamePlay as GP_GP

class IGuildBossChallenge(object):
    def __init__(self):        
        pass

    @gamedecorator.checkGameconfigEnable('guild')
    @AuthClsWraper.authWithPermission(A_AFD.Guild)
    @gamedecorator.limitcall(1)
    def openGuildDungeon(self, exposed, openTime, openType, openID):
        INFO_MSG('IGuild::openGuildDungeon:', exposed, openTime, openType, openID)
        if not self.guildInitStatus:
            return
        
        if not self.guildUUIDBase:
            return

        if not self.guildBox:
            return
        
        if openType not in gameconst.GuildChallengeDungeonOpenType.VALID_TYPE:
            WARNING_MSG('IGuild::openGuildDungeon: wrong opened type', exposed, openType, openID)
            return
        
        cfg = GCBI.datas.get(openID, None)
        if not cfg:
            WARNING_MSG('IGuild::openGuildDungeon: wrong opened id', exposed, openType, openID)
            return
        
        dungeonID = cfg['dunID']
        if not GP_GP.datas.get(dungeonID, None):
            WARNING_MSG('IGuild::openGuildDungeon: wrong gameplay dungeon cfg', exposed, openType, openID)
            return
        
        guildChallengeCfgID = GCBI.dungeonIdxDic.get(dungeonID, None)
        if not guildChallengeCfgID:
            WARNING_MSG('IGuild::openGuildDungeon: wrong dungeon id', exposed, openType, dungeonID)
            return
        
        currentScore = self.getTotalScore()
        # 检查战力
        needScore = GCBI.datas[guildChallengeCfgID]['minScore']
        if currentScore < needScore:
            self.client.onOpenGuildDungeon(gameconst.GuildChallengeOpenDungeonResult.NO_ENOUGH_SCORE, openType, openID)
            WARNING_MSG('IGuild::openGuildDungeon: score is not enough', exposed, openType, dungeonID, currentScore, needScore)
            return
        
        # 检查是否可以预约
        now = utils.getNow()
        frontTime, _ = utils.nextByTimeTupleList(GCC.datas['timeNotScheduledFront']['value'])
        laterTime, _ = utils.nextByTimeTupleList(GCC.datas['timeNotScheduledLater']['value'])

        # 预约开启
        if openType == gameconst.GuildChallengeDungeonOpenType.APPOINT:
            # 计算下一个开启时间点
            # 1.后退时间
            backTime = int(GCC.datas['timeScheduledAhead']['value'])
            # 2.找到下一个半个整点
            nextHalfTime = utils.getNextHoursTimestamp(openTime, backTime, 0.5)
            # 3.检查是否比现在时间还要靠前
            if nextHalfTime <= now:
                WARNING_MSG('IGuild::openGuildDungeon: not in time range 2', exposed, openType, openID)
                self.client.onOpenGuildDungeon(gameconst.GuildChallengeOpenDungeonResult.NOT_VALID_TIME, openType, openID)
                return
            # 跨周期不可预约
            if openTime >= frontTime:
                WARNING_MSG('IGuild::openGuildDungeon: not in time range 1', exposed, openType, openID)
                self.client.onOpenGuildDungeon(gameconst.GuildChallengeOpenDungeonResult.NOT_VALID_TIME, openType, openID)
                return
            openTime = nextHalfTime
        # 直接开启
        else:
            # 开始大于结束时间了，或者，在两个时间段内，说明进入了限制时间段
            if frontTime > laterTime or (openTime >= frontTime and openTime <= laterTime):
                WARNING_MSG('IGuild::openGuildDungeon: not in time range 3', exposed, openType, openID)
                self.client.onOpenGuildDungeon(gameconst.GuildChallengeOpenDungeonResult.NOT_VALID_TIME, openType, openID)
                return

        self.guildBox.openGuildChallenge(self.gbID, self, openType, openID, openTime)

    @gamedecorator.checkGameconfigEnable('guild')
    @AuthClsWraper.authWithPermission(A_AFD.Guild)
    @gamedecorator.limitcall(1)
    def getChangllengeDataInfo(self, exposed):
        INFO_MSG('IGuild::getChangllengeDataInfo:', exposed)
        if not self.guildInitStatus:
            return
        
        if not self.guildUUIDBase:
            return

        if not self.guildBox:
            return

        self.guildBox.getChangllengeDataInfo(self.gbID, self)

    @gamedecorator.checkGameconfigEnable('guild')
    @AuthClsWraper.authWithPermission(A_AFD.Guild)
    @gamedecorator.limitcall(1)
    def cancalGuildDungeonOrder(self, exposed):
        INFO_MSG('IGuild::cancalGuildDungeonOrder:', exposed)
        if not self.guildInitStatus:
            return
        
        if not self.guildUUIDBase:
            return

        if not self.guildBox:
            return
        
        self.guildBox.cancalGuildDungeonOrder(self.gbID, self)

    @gamedecorator.checkGameconfigEnable('guild')
    @AuthClsWraper.authWithPermission(A_AFD.Guild)
    @gamedecorator.limitcall(1)
    def enterBossChallengeDungeon(self, exposed):
        INFO_MSG('IGuild::enterBossChallengeDungeon:', exposed)
        if not self.guildInitStatus:
            return
        
        if not self.guildUUIDBase:
            return

        if not self.guildBox:
            return
        
        extra = {}
        extra['playerName'] = self.characterName
        self.guildBox.enterBossChallengeDungeon(self.gbID, self, extra)

    @gamedecorator.checkGameconfigEnable('guild')
    @AuthClsWraper.authWithPermission(A_AFD.Guild)
    @gamedecorator.limitcall(1)
    def leaveBossChallengeDungeon(self, exposed):
        INFO_MSG('IGuild::leaveBossChallengeDungeon:', exposed)
        if not self.guildInitStatus:
            return
        
        if not self.guildUUIDBase:
            return

        if not self.guildBox:
            return
        
        self.guildBox.leaveBossChallengeDungeon(self.gbID, self)

    @gamedecorator.checkGameconfigEnable('guild')
    @AuthClsWraper.authWithPermission(A_AFD.Guild)
    @gamedecorator.limitcall(1)
    def getSettlementRankList(self, exposed, idx, offset):
        INFO_MSG('IGuild::getSettlementRankList:', exposed, idx, offset)
        if not self.guildInitStatus:
            return
        
        if not self.guildUUIDBase:
            return

        if not self.guildBox:
            return
        
        self.guildBox.getSettlementRankList(self.gbID, self, idx, offset)

        