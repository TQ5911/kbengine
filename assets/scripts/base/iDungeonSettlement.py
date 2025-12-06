# coding: utf-8
from KBEDebug import *
import KBEngine

import gameconst
import dataUtils
import dropAward
import gameclass
import mailAssistor

import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import raidBossChallenge_config as RBC_CFG
import raidBossChallenge_basicInfo as RBC_BI
import teamDunChallenge_basicInfo as TDC_BI
import guildChallenge_basicInfo as GC_BI
import guildChallenge_config as GC_C

class IDungeonSettlement(object):
    def __init__(self):
        pass

    def queryFirstPassRewardStatus(self, exposed, dungeonType, dungeonNo):
        DEBUG_MSG('in queryFirstPassRewardStatus::', exposed, dungeonType, dungeonNo)
        if dungeonType == gameconst.DungeonPlayModeEnum.CRUSADE:
            ret = self.chiefFirstPassRecords.get(dungeonNo, 0)
            self.onQueryFirstPassRewardStatus(dungeonType, dungeonNo, ret)
        elif dungeonType == gameconst.DungeonPlayModeEnum.CHIEF:
            ret = self.crusadeFirstPassRecords.get(dungeonNo, 0)
            self.onQueryFirstPassRewardStatus(dungeonType, dungeonNo, ret)
        elif dungeonType == gameconst.DungeonPlayModeEnum.GUILD_BOSS:
            ret = self.guildBossFirstPassRecords.get(dungeonNo, 0)
            self.onQueryFirstPassRewardStatus(dungeonType, dungeonNo, ret)
        else:
            ERROR_MSG('in queryFirstPassRewardStatus:: unknow dungeon type', exposed, dungeonType, dungeonNo)

    def onDungeonFinished(self, isWin, dungeonType, dungeonNo, rank):
        DEBUG_MSG('in onDungeonFinished::', isWin, dungeonType, dungeonNo, rank)
        # 五人讨伐
        if dungeonType == gameconst.DungeonPlayModeEnum.CRUSADE:
            self.doCrusadeSettlement(isWin, dungeonType, dungeonNo, rank)
        # 首领征战
        elif dungeonType == gameconst.DungeonPlayModeEnum.CHIEF:
            self.doChiefSettlement(isWin, dungeonType, dungeonNo, rank)
        # # 公会boss
        # elif dungeonType == gameconst.DungeonPlayModeEnum.GUILD_BOSS:
        #     self.doGuildBossSettlement(isWin, dungeonType, dungeonNo, rank)

    def doCrusadeSettlement(self, isWin, dungeonType, dungeonNo, rank):
        opUUID = None
        firstPassWealth = None
        clearPassWealth = None
        if isWin:
            ret = self.crusadeFirstPassRecords.get(dungeonNo, 0)
            if not ret:
                self.crusadeFirstPassRecords[dungeonNo] = 1
                rewardId = TDC_BI.fistPassRewardDic.get(dungeonNo, 0)
                if rewardId > 0:
                    if not opUUID:
                        opUUID = KBEngine.genUUID64()
                    firstPassWealth = self.calculateDunegonReward(dungeonType, dungeonNo, AAC_AACDD.datas.BONUS_SRC_TEAM_FIRST_PASS_REWARD, opUUID, [rewardId])
            rewardId = TDC_BI.clearPassRewardDic.get(dungeonNo, 0)
            if rewardId > 0:
                if not opUUID:
                    opUUID = KBEngine.genUUID64()
                clearPassWealth = self.calculateDunegonReward(dungeonType, dungeonNo, AAC_AACDD.datas.BONUS_SRC_TEAM_CLEAR_PASS_REWARD, opUUID, [rewardId])
            self.notifyDungeonInfoToClient(dungeonType, dungeonNo, firstPassWealth, clearPassWealth, rank)

    def doChiefSettlement(self, isWin, dungeonType, dungeonNo, rank):
        opUUID = None
        firstPassWealth = None
        clearPassWealth = None
        if isWin:
            ret = self.chiefFirstPassRecords.get(dungeonNo, 0)
            if not ret:
                self.chiefFirstPassRecords[dungeonNo] = 1
                rewardId = RBC_BI.fistPassRewardDic.get(dungeonNo, 0)
                if rewardId > 0:
                    if not opUUID:
                        opUUID = KBEngine.genUUID64()
                    firstPassWealth = self.calculateDunegonReward(dungeonType, dungeonNo, AAC_AACDD.datas.BONUS_SRC_RAID_FIRST_PASS_REWARD, opUUID, [rewardId])
            rewardId = RBC_BI.clearPassRewardDic.get(dungeonNo, 0)
            if rewardId > 0:
                if not opUUID:
                    opUUID = KBEngine.genUUID64()
                clearPassWealth = self.calculateDunegonReward(dungeonType, dungeonNo, AAC_AACDD.datas.BONUS_SRC_RAID_CLEAR_PASS_REWARD, opUUID, [rewardId])
            self.notifyDungeonInfoToClient(dungeonType, dungeonNo, firstPassWealth, clearPassWealth, rank)

    def doGuildBossSettlement(self, isWin, dungeonType, dungeonNo, rank):
        opUUID = None
        firstPassWealth = None
        clearPassWealth = None
        if isWin:
            ret = self.guildBossFirstPassRecords.get(dungeonNo, 0)
            if not ret:
                self.guildBossFirstPassRecords[dungeonNo] = 1
                rewardId = GC_BI.fistPassRewardDic.get(dungeonNo, 0)
                if rewardId > 0:
                    if not opUUID:
                        opUUID = KBEngine.genUUID64()
                    firstPassWealth = self.calculateDunegonReward(dungeonType, dungeonNo, AAC_AACDD.datas.BONUS_SRC_GULID_DUNGEON_FIRST_REWARD, opUUID, [rewardId])
            rewardId = RBC_BI.clearPassRewardDic.get(dungeonNo, 0)
            if rewardId > 0:
                if not opUUID:
                    opUUID = KBEngine.genUUID64()
                clearPassWealth = self.calculateDunegonReward(dungeonType, dungeonNo, AAC_AACDD.datas.BONUS_SRC_GULID_DUNGEON_CLEAR_REWARD, opUUID, [rewardId])
            self.notifyDungeonInfoToClient(dungeonType, dungeonNo, firstPassWealth, clearPassWealth, rank)

    def calculateDunegonReward(self, dungeonType, dungeonNo, src, opUUID, rewardIds):
        if not rewardIds or len(rewardIds) == 0:
            return None

        addWealthVal = dropAward.AwardVal()
        ctx = self._getAvatarAwardsCtx(rewardIds, None)
        for rewardId in rewardIds:
            addWealthVal += dropAward.getAwardOne(rewardId, ctx)

        detail = gameclass.AwardDetail(awardIds = rewardIds, dungeonType = dungeonType, dungeonNo = dungeonNo)
        self.addWealth(src, addWealthVal, opUUID, detail)
        return addWealthVal

    def notifyDungeonInfoToClient(self, dungeonType, dungeonNo, firstPassWealth, clearPassWealth, rank):
        firstPassBriefReward = []
        clearPassBriefReward = []
        if firstPassWealth and not firstPassWealth.isEmpty():
            firstPassBriefReward = firstPassWealth.toBriefList()
        if clearPassWealth and not clearPassWealth.isEmpty():
            clearPassBriefReward = clearPassWealth.toBriefList()
        if firstPassBriefReward or clearPassBriefReward:
            self.client.onDungenFinishRewards(dungeonType, dungeonNo, firstPassBriefReward, clearPassBriefReward, rank)

    def onDungeonSettlement(self, dungeonType, dungeonNo, opUUID, guildUUID, settlementData):
        win = settlementData['win']
        rank = settlementData['rank']
        dungeonRewardID = settlementData['dungeonRewardsID']
        dungeonRewards = settlementData['dungeonRewards']
        firstPassRewardID = settlementData['firstPassRewardsID']
        firstPassRewards = settlementData['firstPassRewards']
        INFO_MSG('onDungeonSettlement:: ', opUUID, guildUUID, dungeonNo, dungeonType, win, rank, dungeonRewardID, dungeonRewards, firstPassRewardID, firstPassRewards)
        if dungeonType == gameconst.DungeonPlayModeEnum.CRUSADE:
            pass
        elif dungeonType == gameconst.DungeonPlayModeEnum.CHIEF:
            pass
        elif dungeonType == gameconst.DungeonPlayModeEnum.GUILD_BOSS:
            self._doGuildBossChallengeSettlement(self, opUUID, guildUUID, dungeonNo, dungeonType, win, dungeonRewardID, dungeonRewards, firstPassRewardID, firstPassRewards) 
        else:
            ERROR_MSG('in onDungeonSettlement:: unknow dungeon type', dungeonType)

    def _doGuildBossChallengeSettlement(self, opUUID, guildUUID, dungeonNo, dungeonType, win, rankdID, dungeonRewardID, dungeonRewards, firstPassRewardID, firstPassRewards):
        settlementMailID = int(GC_C.datas['emailSettle']['value'])
        if dungeonRewardID > 0:
            addWealthVal = dropAward.AwardVal()
            for reward in dungeonRewards:
                addWealthVal.addWealthByItemId(reward['itemId'], reward['itemNum'], reward['bindType'])
            srcType = AAC_AACDD.datas.BONUS_SRC_GULID_DUNGEON_CLEAR_REWARD
            awardCtx = self._getAvatarAwardCtx(dungeonRewardID, None, settlementMailID)
            detail = gameclass.AwardDetail(awardIds = dungeonRewardID, dungeonType = dungeonType, dungeonNo = dungeonNo, isWin=isWin, rankdID=rankdID, guildUUID=guildUUID)
            self.addWealth(srcType, addWealthVal, opUUID, detail, awardCtx)
        if win and not self.guildBossFirstPassRecords.get(dungeonNo, 0):
            if firstPassRewardID > 0:
                addWealthVal = dropAward.AwardVal()
                for reward in firstPassRewards:
                    addWealthVal.addWealthByItemId(reward['itemId'], reward['itemNum'], reward['bindType'])
                srcType = AAC_AACDD.datas.BONUS_SRC_GULID_DUNGEON_FIRST_REWARD
                awardCtx = self._getAvatarAwardCtx(firstPassRewardID, None, settlementMailID)
                detail = gameclass.AwardDetail(awardIds = firstPassRewardID, dungeonType = dungeonType, dungeonNo = dungeonNo, isWin=isWin, rankdID=rankdID, guildUUID=guildUUID)
                self.addWealth(srcType, addWealthVal, opUUID, detail, awardCtx)
                # 记录结算状态
                self.guildBossFirstPassRecords[dungeonNo] = 1

        _mailId = int(GC_C.datas['emailSettle']['value'])
        openID = GC_BI.dungeonIdxDic[dungeonNo]
        _mailArgs = [GC_BI.datas[openID]['name']]
        self._sendMail(opUUID, [self.gbId], _mailId, _mailArgs)

    def _sendMail(self, opUUID, gbIDs, mailID, mailArgs):
        mailAssistor.sendMailToPlayers(gbIDs, mailID, opUUID=opUUID, despArgs=mailArgs)
