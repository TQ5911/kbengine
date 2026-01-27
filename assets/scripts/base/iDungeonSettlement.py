# coding: utf-8
from KBEDebug import *
import KBEngine

import gameconst
import dataUtils
import dropAward
import gameclass
import mailAssistor
import gameconfig
import LogTrackingMgr

import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import raidBossChallenge_basicInfo as RBC_BI
import teamDunChallenge_basicInfo as TDC_BI
import guildChallenge_basicInfo as GC_BI
import guildChallenge_config as GC_C
import guildChallenge_rankReward as GC_RR

class IDungeonSettlement(object):
    def __init__(self):
        pass

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

    def checkDungeonPlayModeOpen(self, playMode):
        ret = True
        if playMode == gameconst.DungeonPlayModeEnum.CRUSADE:
            if not gameconfig.visibleConfigEable('teamDungeon'):
                ret = False
        elif playMode == gameconst.DungeonPlayModeEnum.CHIEF:
            if not gameconfig.visibleConfigEable('raidDungeon'):
                ret = False
        elif playMode == gameconst.DungeonPlayModeEnum.GUILD_BOSS:
            if not gameconfig.visibleConfigEable('guildBossChallenge'):
                ret = False
        else:
            ret = False
        return ret

    def onDungeonSettlement(self, playMode, spaceNo, dungeonNo, opUUId, uniqueId, win, box, extra):
        INFO_MSG('onDungeonSettlement:: 1', playMode, spaceNo, dungeonNo, opUUId, uniqueId, win, box, extra)
        if not self.checkDungeonPlayModeOpen(playMode):
            box.cell.onNotifySettlementResult(self, playMode, spaceNo, dungeonNo, opUUId, uniqueId, win, extra, [], [], [])
            INFO_MSG('onDungeonSettlement:: 2, play mode id closed, no reward ', playMode, spaceNo, dungeonNo, opUUId, uniqueId, win, box, extra)
            return
        
        if playMode == gameconst.DungeonPlayModeEnum.CRUSADE:
            self._doCrusadeSettlement(spaceNo, dungeonNo, opUUId, uniqueId, win, box, extra) 
        elif playMode == gameconst.DungeonPlayModeEnum.CHIEF:
            self._doChiefSettlement(spaceNo, dungeonNo, opUUId, uniqueId, win, box, extra) 
        elif playMode == gameconst.DungeonPlayModeEnum.GUILD_BOSS:
            self._doGuildBossChallengeSettlement(spaceNo, dungeonNo, opUUId, uniqueId, win, box, extra) 
        else:
            ERROR_MSG('in onDungeonSettlement:: unknow play mod', playMode, spaceNo, dungeonNo, opUUId, uniqueId, win, extra)

    def _doChiefSettlement(self, spaceNo, dungeonNo, opUUId, uniqueId, win, box, extra):
        firstPassRewards = None
        goldPassRewards = None
        dungeonRewards = None
        if win:
            dungeonRewardId = RBC_BI.clearPassRewardDic.get(dungeonNo, 0)
            if dungeonRewardId > 0:
                ctx = self._getAvatarAwardCtx(dungeonRewardId, None)
                dungeonRewards = dropAward.getAwardOne(dungeonRewardId, ctx).toBriefList()
                INFO_MSG('in _doChiefSettlement:: record dungeon reward', spaceNo, dungeonNo, opUUId, uniqueId, win, extra)
                self._doAddWealthVal(opUUId, gameconst.DungeonPlayModeEnum.CHIEF, dungeonNo, win, 0, uniqueId, AAC_AACDD.datas.BONUS_SRC_RAID_CLEAR_PASS_REWARD, dungeonRewardId, dungeonRewards, 0)

            if self.chiefInfo.checkUsedTicketType(gameconst.DungeonTicketType.GOLD):
                goldRewardId = RBC_BI.goldPassRewardDic.get(dungeonNo, 0)
                if goldRewardId > 0:
                    ctx = self._getAvatarAwardCtx(goldRewardId, None)
                    goldPassRewards = dropAward.getAwardOne(goldRewardId, ctx).toBriefList()
                    INFO_MSG('in _doChiefSettlement:: record gold reward', spaceNo, dungeonNo, opUUId, uniqueId, win, extra)
                    self._doAddWealthVal(opUUId, gameconst.DungeonPlayModeEnum.CHIEF, dungeonNo, win, 0, uniqueId, AAC_AACDD.datas.BONUS_SRC_RAID_GOLD_PASS_REWARD, goldRewardId, goldPassRewards, 0)
            entryId = RBC_BI.dungeonIdxDic.get(dungeonNo)
            if self.chiefPassRecords.checkEntryStatus(entryId):
                firstRewardId = RBC_BI.fistPassRewardDic.get(dungeonNo, 0)
                if firstRewardId > 0:
                    self.chiefPassRecords.finishEntryStatus(entryId)
                    self.chiefPassRecords = self.chiefPassRecords
                    ctx = self._getAvatarAwardCtx(firstRewardId, None)
                    firstPassRewards = dropAward.getAwardOne(firstRewardId, ctx).toBriefList()
                    INFO_MSG('in _doChiefSettlement:: record first reward', spaceNo, dungeonNo, opUUId, uniqueId, win, extra)
                    self._doAddWealthVal(opUUId, gameconst.DungeonPlayModeEnum.CHIEF, dungeonNo, win, 0, uniqueId, AAC_AACDD.datas.BONUS_SRC_RAID_FIRST_PASS_REWARD, firstRewardId, firstPassRewards, 0)
        box.cell.onNotifySettlementResult(self, gameconst.DungeonPlayModeEnum.CHIEF, spaceNo, dungeonNo, opUUId, uniqueId, win, extra, firstPassRewards if firstPassRewards else [], goldPassRewards if goldPassRewards else [], dungeonRewards if dungeonRewards else [])
        
        LogTrackingMgr.LogTrackingMgr.Dungeon_Settlement(extra['uniqueID'], gameconst.DungeonPlayModeEnum.CHIEF, dungeonNo, extra['spaceUUID'], spaceNo, self.gbID, \
                                                        True if dungeonRewards else False, True if firstPassRewards else False, extra['elaspedTime'], win, extra['completedReasonType'], extra['playerCount'], 
                                                        extra['deadCount'], firstPassRewards if firstPassRewards else {}, dungeonRewards if dungeonRewards else {}, \
                                                        goldPassRewards if goldPassRewards else {}, extra['autoCombatTimes'], self.getTotalScore(), self.getRoleCacheAttr('level'))
        
    def _doCrusadeSettlement(self, spaceNo, dungeonNo, opUUId, uniqueId, win, box, extra):
        firstPassRewards = None
        goldPassRewards = None
        dungeonRewards = None
        if win:
            dungeonRewardId = TDC_BI.clearPassRewardDic.get(dungeonNo, 0)
            if dungeonRewardId > 0:
                ctx = self._getAvatarAwardCtx(dungeonRewardId, None)
                dungeonRewards = dropAward.getAwardOne(dungeonRewardId, ctx).toBriefList()
                INFO_MSG('in _doCrusadeSettlement:: record dungeon reward', spaceNo, dungeonNo, opUUId, uniqueId, win, extra)
                self._doAddWealthVal(opUUId, gameconst.DungeonPlayModeEnum.CRUSADE, dungeonNo, win, 0, uniqueId, AAC_AACDD.datas.BONUS_SRC_TEAM_CLEAR_PASS_REWARD, dungeonRewardId, dungeonRewards, 0)

            if self.crusadeInfo.checkUsedTicketType(gameconst.DungeonTicketType.GOLD):
                goldRewardId = TDC_BI.goldPassRewardDic.get(dungeonNo, 0)
                if goldRewardId > 0:
                    ctx = self._getAvatarAwardCtx(goldRewardId, None)
                    goldPassRewards = dropAward.getAwardOne(goldRewardId, ctx).toBriefList()
                    INFO_MSG('in _doCrusadeSettlement:: record gold reward', spaceNo, dungeonNo, opUUId, uniqueId, win, extra)
                    self._doAddWealthVal(opUUId, gameconst.DungeonPlayModeEnum.CRUSADE, dungeonNo, win, 0, uniqueId, AAC_AACDD.datas.BONUS_SRC_TEAM_FIRST_PASS_REWARD, goldRewardId, goldPassRewards, 0)
            entryId = TDC_BI.dungeonIdxDic.get(dungeonNo)
            if self.crusadePassRecords.checkEntryStatus(entryId):
                firstRewardId = TDC_BI.fistPassRewardDic.get(dungeonNo, 0)
                if firstRewardId > 0:
                    self.crusadePassRecords.finishEntryStatus(entryId)
                    self.crusadePassRecords = self.crusadePassRecords
                    ctx = self._getAvatarAwardCtx(firstRewardId, None)
                    firstPassRewards = dropAward.getAwardOne(firstRewardId, ctx).toBriefList()
                    INFO_MSG('in _doCrusadeSettlement:: record first reward', spaceNo, dungeonNo, opUUId, uniqueId, win, extra)
                    self._doAddWealthVal(opUUId, gameconst.DungeonPlayModeEnum.CRUSADE, dungeonNo, win, 0, uniqueId, AAC_AACDD.datas.BONUS_SRC_TEAM_GOLD_PASS_REWARD, firstRewardId, firstPassRewards, 0)
        box.cell.onNotifySettlementResult(self, gameconst.DungeonPlayModeEnum.CRUSADE, spaceNo, dungeonNo, opUUId, uniqueId, win, extra, firstPassRewards if firstPassRewards else [], goldPassRewards if goldPassRewards else [], dungeonRewards if dungeonRewards else [])
        
        LogTrackingMgr.LogTrackingMgr.Dungeon_Settlement(extra['uniqueID'], gameconst.DungeonPlayModeEnum.CRUSADE, dungeonNo, extra['spaceUUID'], spaceNo, self.gbID, \
                                                         True if dungeonRewards else False, True if firstPassRewards else False, extra['elaspedTime'], win, extra['completedReasonType'], extra['playerCount'], 
                                                         extra['deadCount'], firstPassRewards if firstPassRewards else {}, dungeonRewards if dungeonRewards else {}, \
                                                         goldPassRewards if goldPassRewards else {}, extra['autoCombatTimes'], self.getTotalScore(), self.getRoleCacheAttr('level'))

    def _doGuildBossChallengeSettlement(self, spaceNo, dungeonNo, opUUId, uniqueId, win, box, extra):
        # 没次数或者没有造成伤害，不给奖励
        if not self.checkGuildBossRewardRemainTimes(dungeonNo):
            box.cell.onNotifySettlementResult(self, gameconst.DungeonPlayModeEnum.GUILD_BOSS, spaceNo, dungeonNo, opUUId, uniqueId, win, extra, [], [], [])
            WARNING_MSG('in _doGuildBossChallengeSettlement:: no reward', spaceNo, dungeonNo, opUUId, uniqueId, win, box, extra)
            return
        
        self.guildBossRewardWeeklyCount = self.guildBossRewardWeeklyCount + 1
        
        dungeonRewards = None
        firstPassRewards = None
        isFirstPass = False
        rank = extra['rank']
        score = extra['score']
        if win and score > 0:
            settlementMailID = int(GC_C.datas['emailSettle']['value'])
            dataKey = dataUtils.getGuildBossRankRewardKey(dungeonNo, rank)
            dungeonRewardId = GC_RR.rankRewardDic.get(dataKey, 0)
            if dungeonRewardId > 0:
                ctx = self._getAvatarAwardCtx(dungeonRewardId, None)
                dungeonRewards = dropAward.getAwardOne(dungeonRewardId, ctx).toBriefList()
                INFO_MSG('in _doGuildBossChallengeSettlement:: record dungeon reward', spaceNo, dungeonNo, opUUId, uniqueId, win, extra)
                self._doAddWealthVal(opUUId, gameconst.DungeonPlayModeEnum.GUILD_BOSS, dungeonNo, win, rank, uniqueId, AAC_AACDD.datas.BONUS_SRC_GULID_DUNGEON_CLEAR_REWARD, dungeonRewardId, dungeonRewards, settlementMailID)

        # 首通奖励
            entryId = GC_BI.dungeonIdxDic.get(dungeonNo)
            if self.guildBossPassRecords.checkEntryStatus(entryId):
                firstRewardId = GC_BI.fistPassRewardDic.get(dungeonNo, 0)
                if firstRewardId > 0:
                    isFirstPass = True
                    self.guildBossPassRecords.finishEntryStatus(entryId)
                    self.guildBossPassRecords = self.guildBossPassRecords
                    ctx = self._getAvatarAwardCtx(firstRewardId, None)
                    firstPassRewards = dropAward.getAwardOne(firstRewardId, ctx).toBriefList()
                    INFO_MSG('in _doGuildBossChallengeSettlement:: record first pass reward', spaceNo, dungeonNo, opUUId, uniqueId, win, extra)
                    self._doAddWealthVal(opUUId, gameconst.DungeonPlayModeEnum.GUILD_BOSS, dungeonNo, win, rank, uniqueId, AAC_AACDD.datas.BONUS_SRC_GULID_DUNGEON_FIRST_REWARD, firstRewardId, firstPassRewards, settlementMailID)
        
        LogTrackingMgr.LogTrackingMgr.Guild_BossChallenge_Settlement(opUUId, self.gbID, win, score, rank, isFirstPass, firstPassRewards if firstPassRewards else [], dungeonRewards if dungeonRewards else [])
        
        box.cell.onNotifySettlementResult(self, gameconst.DungeonPlayModeEnum.GUILD_BOSS, spaceNo, dungeonNo, opUUId, uniqueId, win, extra, firstPassRewards if firstPassRewards else [], [], dungeonRewards if dungeonRewards else [])

    def _doAddWealthVal(self, opUUID, playMode, dungeonNo, win, rank, uniqueId, src, rewardId, rewards, rewardMailId):
        addWealthVal = dropAward.AwardVal()
        for reward in rewards:
            addWealthVal.addWealthByItemId(reward['itemId'], reward['itemNum'], reward['bindType'])
        srcType = src
        awardCtx = self._getAvatarAwardCtx(rewardId, None, rewardMailId)
        detail = gameclass.AwardDetail(awardIds = rewardId, playMode = playMode, dungeonNo = dungeonNo, win=win, rank=rank, uniqueId=uniqueId)
        self.addWealth(srcType, addWealthVal, opUUID, detail, awardCtx)
        
    def checkGuildBossRewardRemainTimes(self, dungeonNo):
        return self.guildBossRewardWeeklyCount < int(GC_C.datas['guildRewardTimes']['value'])
    
    def dungeonSettlementWeeklyReset(self):
        self.guildBossRewardWeeklyCount = 0
    
    def _sendMail(self, opUUID, gbIDs, mailID, mailArgs):
        mailAssistor.sendMailToPlayers(gbIDs, mailID, opUUID=opUUID, despArgs=mailArgs)
