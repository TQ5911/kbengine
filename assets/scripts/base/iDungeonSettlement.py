# coding: utf-8
from KBEDebug import *
import KBEngine

import gameconst
import dataUtils
import dropAward
import gameclass
import gameconfig
import LogTrackingMgr
import formula
import actionContext
import mailAssistor

import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import raidBossChallenge_basicInfo as RBC_BI
import teamDunChallenge_basicInfo as TDC_BI
import guildChallenge_basicInfo as GC_BI
import guildChallenge_config as GC_C
import guildChallenge_rankReward as GC_RR
import teamDunChallenge_config as TDC_CFG
import cube_innerDemon as CID
import taskClass_taskTarget as TCCTD


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

        detail = gameclass.AwardDetailCls(awardIds = rewardIds, dungeonType = dungeonType, dungeonNo = dungeonNo)
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
            if not gameconfig.visibleConfigEnabled('teamDungeon'):
                ret = False
        elif playMode == gameconst.DungeonPlayModeEnum.CHIEF:
            if not gameconfig.visibleConfigEnabled('raidDungeon'):
                ret = False
        elif playMode == gameconst.DungeonPlayModeEnum.GUILD_BOSS:
            if not gameconfig.visibleConfigEnabled('guildBossChallenge'):
                ret = False
        elif playMode == gameconst.DungeonPlayModeEnum.INNER_DEMON:
            pass
        else:
            ret = False
        return ret

    def onDungeonSettlement(self, playMode, spaceNo, dungeonNo, opUUId, uniqueId, win, box, extra):
        LOG_INFO('onDungeonSettlement:: 1', playMode, spaceNo, dungeonNo, opUUId, uniqueId, win, box, extra)
        # 跨服 playMode（CROSS_CRUSADE/CROSS_CHIEF）只出现在跨服服（问题记录#6，D3-2 修订后
        # 本服模式空间 playMode 直接落 CRUSADE/CHIEF，走下方本服结算链路，无需分发）：
        # - 本机跨服服（跨服服上的镜像 Avatar 走到这里）：结算计算/展示标记/弹窗聚合在跨服本地闭环，
        #   不再整体透传本服再等结果回传（任一成员本服结算异常会卡住全员结算面板）；
        #   次数扣减/奖励发放等持久化副作用打包异步落本服（fire-and-forget，失败仅报错）
        if playMode in gameconst.DungeonPlayModeEnum.COLL_CROSS:
            if gameconfig.isCrossServer():
                self._doCrossTeamDungeonSettlement(playMode, spaceNo, dungeonNo, opUUId, uniqueId, win, box, extra)
            else:
                LOG_ERR('onDungeonSettlement:: cross play mode on local server', playMode, spaceNo, dungeonNo)
            return

        if not self.checkDungeonPlayModeOpen(playMode):
            box.cell.onNotifySettlementResult(self, playMode, spaceNo, dungeonNo, opUUId, uniqueId, win, extra, [], [], [])
            LOG_INFO('onDungeonSettlement:: 2, play mode id closed, no reward ', playMode, spaceNo, dungeonNo, opUUId, uniqueId, win, box, extra)
            return
        
        if playMode == gameconst.DungeonPlayModeEnum.CRUSADE:
            self._doCrusadeSettlement(spaceNo, dungeonNo, opUUId, uniqueId, win, box, extra) 
        elif playMode == gameconst.DungeonPlayModeEnum.CHIEF:
            self._doChiefSettlement(spaceNo, dungeonNo, opUUId, uniqueId, win, box, extra) 
        elif playMode == gameconst.DungeonPlayModeEnum.GUILD_BOSS:
            self._doGuildBossChallengeSettlement(spaceNo, dungeonNo, opUUId, uniqueId, win, box, extra) 
        elif playMode == gameconst.DungeonPlayModeEnum.INNER_DEMON:
            self._doInnerDemonChallengeSettlement(spaceNo, dungeonNo, opUUId, uniqueId, win, box, extra) 
        else:
            LOG_ERR('in onDungeonSettlement:: unknow play mod', playMode, spaceNo, dungeonNo, opUUId, uniqueId, win, extra)

    def onLocalServerCrossCrusadeSettlementApply(self, pack):
        # 跨服讨伐发奖包落地（跨服服镜像完成结算计算与展示后异步送达，fire-and-forget）：
        playMode = pack['playMode']
        dungeonNo = pack['dungeonNo']
        win = pack['win']
        extra = pack['extra']
        dungeonRewards = pack.get('dungeonRewards') or []
        goldPassRewards = pack.get('goldPassRewards') or []
        firstPassRewards = pack.get('firstPassRewards') or []
        LOG_INFO('onLocalServerCrossCrusadeSettlementApply::', self.gbID, playMode, dungeonNo, win)
        try:
            if win:
                if playMode == gameconst.DungeonPlayModeEnum.CROSS_CRUSADE:
                    # 扣次数
                    self.crusadeInfo.deductRewardNum()
                    self.crusadeInfo = self.crusadeInfo

                    # 发奖励
                    for src, rewardId, rewards in pack['rewardList']:
                        self._doAddWealthVal(pack['opUUId'], playMode, dungeonNo, win, 0, pack['uniqueId'], src, rewardId, rewards)

                    # 首通
                    if pack.get('firstPassEntryId', 0):
                        self.crusadePassRecords.finishEntryStatus(firstPassEntryId)
                        self.crusadePassRecords = self.crusadePassRecords

                    # 成就
                    self.achievementInfo.triggerAchieveByType(
                        self,
                        gameconst.AchieveType.CRUSADE,
                        actionContext.AchievementCtx(dungeonNo=dungeonNo)
                    )

                elif playMode == gameconst.DungeonPlayModeEnum.CROSS_CHIEF:
                    # 扣次数
                    self.chiefInfo.deductRewardNum()
                    self.chiefInfo = self.chiefInfo

                    # 发奖励
                    for src, rewardId, rewards in pack['rewardList']:
                        self._doAddWealthVal(pack['opUUId'], playMode, dungeonNo, win, 0, pack['uniqueId'], src, rewardId, rewards)

                    # 首通
                    if pack.get('firstPassEntryId', 0):
                        self.chiefPassRecords.finishEntryStatus(firstPassEntryId)
                        self.chiefPassRecords = self.chiefPassRecords

                    # 成就
                    self.achievementInfo.triggerAchieveByType(
                        self,
                        gameconst.AchieveType.CHIEF,
                        actionContext.AchievementCtx(dungeonNo=dungeonNo)
                    )

                else:
                    LOG_ERR('onLocalServerCrossCrusadeSettlementApply playMode err:', playMode)

                # 任务
                self.taskCheckCounterTarget(TCCTD.couterTargetDic['CompleteACertainInstance'], (dungeonNo,))

            self.sendDungeonFinishedMail(playMode, dungeonNo, pack['opUUId'], extra['gbId'], win)
            LogTrackingMgr.LogTrackingMgr.Dungeon_Settlement(
                self.gbID,
                self.accountEntity.clientDistinctId,
                extra['uniqueID'],
                playMode,
                dungeonNo,
                extra['spaceUUID'],
                pack['spaceNo'],
                self.gbID,
                True if dungeonRewards else False,
                True if firstPassRewards else False,
                extra['elaspedTime'],
                win,
                extra['completedReasonType'],
                extra['playerCount'],
                extra['deadCount'],
                firstPassRewards if firstPassRewards else {},
                dungeonRewards if dungeonRewards else {},
                goldPassRewards if goldPassRewards else {},
                extra['autoCombatTimes'],
                self.getTotalScore(),
                self.getRoleCacheAttr('level'),
                extra['score']
            )
        except Exception:
            import traceback
            traceback.print_exc()
            LOG_ERR('onLocalServerCrossCrusadeSettlementApply error::', self.gbID, pack)

    # 跨服副本奖励等结算数据计算后传回本服落地
    def _doCrossTeamDungeonSettlement(self, playMode, spaceNo, dungeonNo, opUUId, uniqueId, win, box, extra):
        if playMode == gameconst.DungeonPlayModeEnum.CROSS_CRUSADE:
            dungeonInfo = self.crusadeInfo
            passRecords = self.crusadePassRecords
            biData = TDC_BI
            srcDungeon = AAC_AACDD.datas.BONUS_SRC_TEAM_CLEAR_PASS_REWARD
            srcGold = AAC_AACDD.datas.BONUS_SRC_TEAM_GOLD_PASS_REWARD
            srcFirst = AAC_AACDD.datas.BONUS_SRC_TEAM_FIRST_PASS_REWARD
        elif playMode == gameconst.DungeonPlayModeEnum.CROSS_CHIEF:
            dungeonInfo = self.chiefInfo
            passRecords = self.chiefPassRecords
            biData = RBC_BI
            srcDungeon = AAC_AACDD.datas.BONUS_SRC_RAID_CLEAR_PASS_REWARD
            srcGold = AAC_AACDD.datas.BONUS_SRC_RAID_GOLD_PASS_REWARD
            srcFirst = AAC_AACDD.datas.BONUS_SRC_RAID_FIRST_PASS_REWARD
        else:
            LOG_ERR('_doCrossTeamDungeonSettlement playerMode err:', playMode)
            return

        firstPassRewards = None
        goldPassRewards = None
        dungeonRewards = None
        rewardList = []
        firstPassEntryId = 0
        try:
            if win:
                dungeonInfo.deductRewardNum()

                dungeonRewardId = biData.clearPassRewardDic.get(dungeonNo, 0)
                if dungeonRewardId > 0:
                    ctx = self.getAvatarAwardCtx(dungeonRewardId, None)
                    dungeonRewards = dropAward.getAwardOne(dungeonRewardId, ctx).toBriefList()
                    LOG_INFO('in _doCrossTeamDungeonSettlement:: record dungeon reward', spaceNo, dungeonNo, opUUId, uniqueId, win, extra)
                    rewardList.append((srcDungeon, dungeonRewardId, dungeonRewards))

                if dungeonInfo.checkUsedTicketType(gameconst.DungeonTicketType.GOLD):
                    goldRewardId = biData.goldPassRewardDic.get(dungeonNo, 0)
                    if goldRewardId > 0:
                        ctx = self.getAvatarAwardCtx(goldRewardId, None)
                        goldPassRewards = dropAward.getAwardOne(goldRewardId, ctx).toBriefList()
                        LOG_INFO('in _doCrossTeamDungeonSettlement:: record gold reward', spaceNo, dungeonNo, opUUId, uniqueId, win, extra)
                        rewardList.append((srcGold, goldRewardId, goldPassRewards))

                entryId = biData.dungeonIdxDic.get(dungeonNo)
                if passRecords.checkEntryStatus(entryId):
                    firstRewardId = biData.fistPassRewardDic.get(dungeonNo, 0)
                    if firstRewardId > 0:
                        firstPassEntryId = entryId
                        ctx = self.getAvatarAwardCtx(firstRewardId, None)
                        firstPassRewards = dropAward.getAwardOne(firstRewardId, ctx).toBriefList()
                        LOG_INFO('in _doCrossTeamDungeonSettlement:: record first reward', spaceNo, dungeonNo, opUUId, uniqueId, win, extra)
                        rewardList.append((srcFirst, firstRewardId, firstPassRewards))
        except Exception:
            import traceback
            traceback.print_exc()
            LOG_ERR('_doCrossTeamDungeonSettlement error::', self.gbID, playMode, spaceNo, dungeonNo, opUUId, uniqueId, win, extra)
            # 兜底：单成员结算异常也回填空结果清 wait 标记，不阻塞全员结算面板；
            # 发奖包不再发送，本服无次数扣减/奖励发放等副作用
            box.cell.onNotifySettlementResult(self, playMode, spaceNo, dungeonNo, opUUId, uniqueId, win, extra, [], [], [])
            return

        box.cell.onNotifySettlementResult(self, playMode, spaceNo, dungeonNo, opUUId, uniqueId, win, extra, firstPassRewards if firstPassRewards else [], goldPassRewards if goldPassRewards else [], dungeonRewards if dungeonRewards else [])

        _pack = {
            'playMode': playMode,
            'spaceNo': spaceNo,
            'dungeonNo': dungeonNo,
            'opUUId': opUUId,
            'uniqueId': uniqueId,
            'win': win,
            'extra': extra,
            'rewardList': rewardList,
            'firstPassEntryId': firstPassEntryId,
            'dungeonRewards': dungeonRewards if dungeonRewards else [],
            'goldPassRewards': goldPassRewards if goldPassRewards else [],
            'firstPassRewards': firstPassRewards if firstPassRewards else [],
        }
        self.syncMethodCallToLocalServerBase('onLocalServerCrossCrusadeSettlementApply', (_pack,))

    def _doChiefSettlement(self, spaceNo, dungeonNo, opUUId, uniqueId, win, box, extra):
        firstPassRewards = None
        goldPassRewards = None
        dungeonRewards = None
        if win: 
            self.chiefInfo.deductRewardNum()
            self.chiefInfo = self.chiefInfo
            dungeonRewardId = RBC_BI.clearPassRewardDic.get(dungeonNo, 0)
            if dungeonRewardId > 0:
                ctx = self.getAvatarAwardCtx(dungeonRewardId, None)
                dungeonRewards = dropAward.getAwardOne(dungeonRewardId, ctx).toBriefList()
                LOG_INFO('in _doChiefSettlement:: record dungeon reward', spaceNo, dungeonNo, opUUId, uniqueId, win, extra)
                self._doAddWealthVal(opUUId, gameconst.DungeonPlayModeEnum.CHIEF, dungeonNo, win, 0, uniqueId, AAC_AACDD.datas.BONUS_SRC_RAID_CLEAR_PASS_REWARD, dungeonRewardId, dungeonRewards)

            if self.chiefInfo.checkUsedTicketType(gameconst.DungeonTicketType.GOLD):
                goldRewardId = RBC_BI.goldPassRewardDic.get(dungeonNo, 0)
                if goldRewardId > 0:
                    ctx = self.getAvatarAwardCtx(goldRewardId, None)
                    goldPassRewards = dropAward.getAwardOne(goldRewardId, ctx).toBriefList()
                    LOG_INFO('in _doChiefSettlement:: record gold reward', spaceNo, dungeonNo, opUUId, uniqueId, win, extra)
                    self._doAddWealthVal(opUUId, gameconst.DungeonPlayModeEnum.CHIEF, dungeonNo, win, 0, uniqueId, AAC_AACDD.datas.BONUS_SRC_RAID_GOLD_PASS_REWARD, goldRewardId, goldPassRewards)
            entryId = RBC_BI.dungeonIdxDic.get(dungeonNo)
            if self.chiefPassRecords.checkEntryStatus(entryId):
                firstRewardId = RBC_BI.fistPassRewardDic.get(dungeonNo, 0)
                if firstRewardId > 0:
                    self.chiefPassRecords.finishEntryStatus(entryId)
                    self.chiefPassRecords = self.chiefPassRecords
                    ctx = self.getAvatarAwardCtx(firstRewardId, None)
                    firstPassRewards = dropAward.getAwardOne(firstRewardId, ctx).toBriefList()
                    LOG_INFO('in _doChiefSettlement:: record first reward', spaceNo, dungeonNo, opUUId, uniqueId, win, extra)
                    self._doAddWealthVal(opUUId, gameconst.DungeonPlayModeEnum.CHIEF, dungeonNo, win, 0, uniqueId, AAC_AACDD.datas.BONUS_SRC_RAID_FIRST_PASS_REWARD, firstRewardId, firstPassRewards)
            self.achievementInfo.triggerAchieveByType(
                self,
                gameconst.AchieveType.CHIEF,
                actionContext.AchievementCtx(dungeonNo=dungeonNo)
            )
            self.taskCheckCounterTarget(TCCTD.couterTargetDic['CompleteACertainInstance'], (dungeonNo,))
        box.cell.onNotifySettlementResult(self, gameconst.DungeonPlayModeEnum.CHIEF, spaceNo, dungeonNo, opUUId, uniqueId, win, extra, firstPassRewards if firstPassRewards else [], goldPassRewards if goldPassRewards else [], dungeonRewards if dungeonRewards else [])
        self.sendDungeonFinishedMail(gameconst.DungeonPlayModeEnum.CHIEF, dungeonNo, opUUId, extra['gbId'], win)
        LogTrackingMgr.LogTrackingMgr.Dungeon_Settlement(self.gbID, self.accountEntity.clientDistinctId, extra['uniqueID'], gameconst.DungeonPlayModeEnum.CHIEF, dungeonNo, extra['spaceUUID'], spaceNo, self.gbID, \
                                                        True if dungeonRewards else False, True if firstPassRewards else False, extra['elaspedTime'], win, extra['completedReasonType'], extra['playerCount'], 
                                                        extra['deadCount'], firstPassRewards if firstPassRewards else {}, dungeonRewards if dungeonRewards else {}, \
                                                        goldPassRewards if goldPassRewards else {}, extra['autoCombatTimes'], self.getTotalScore(), self.getRoleCacheAttr('level'), extra['score'])
        
    def _doCrusadeSettlement(self, spaceNo, dungeonNo, opUUId, uniqueId, win, box, extra):
        firstPassRewards = None
        goldPassRewards = None
        dungeonRewards = None
        if win:
            self.crusadeInfo.deductRewardNum()
            self.crusadeInfo = self.crusadeInfo

            dungeonRewardId = TDC_BI.clearPassRewardDic.get(dungeonNo, 0)
            if dungeonRewardId > 0:
                ctx = self.getAvatarAwardCtx(dungeonRewardId, None)
                dungeonRewards = dropAward.getAwardOne(dungeonRewardId, ctx).toBriefList()
                LOG_INFO('in _doCrusadeSettlement:: record dungeon reward', spaceNo, dungeonNo, opUUId, uniqueId, win, extra)
                self._doAddWealthVal(opUUId, gameconst.DungeonPlayModeEnum.CRUSADE, dungeonNo, win, 0, uniqueId, AAC_AACDD.datas.BONUS_SRC_TEAM_CLEAR_PASS_REWARD, dungeonRewardId, dungeonRewards)

            if self.crusadeInfo.checkUsedTicketType(gameconst.DungeonTicketType.GOLD):
                goldRewardId = TDC_BI.goldPassRewardDic.get(dungeonNo, 0)
                if goldRewardId > 0:
                    ctx = self.getAvatarAwardCtx(goldRewardId, None)
                    goldPassRewards = dropAward.getAwardOne(goldRewardId, ctx).toBriefList()
                    LOG_INFO('in _doCrusadeSettlement:: record gold reward', spaceNo, dungeonNo, opUUId, uniqueId, win, extra)
                    self._doAddWealthVal(opUUId, gameconst.DungeonPlayModeEnum.CRUSADE, dungeonNo, win, 0, uniqueId, AAC_AACDD.datas.BONUS_SRC_TEAM_FIRST_PASS_REWARD, goldRewardId, goldPassRewards)
            entryId = TDC_BI.dungeonIdxDic.get(dungeonNo)
            if self.crusadePassRecords.checkEntryStatus(entryId):
                firstRewardId = TDC_BI.fistPassRewardDic.get(dungeonNo, 0)
                if firstRewardId > 0:
                    self.crusadePassRecords.finishEntryStatus(entryId)
                    self.crusadePassRecords = self.crusadePassRecords
                    ctx = self.getAvatarAwardCtx(firstRewardId, None)
                    firstPassRewards = dropAward.getAwardOne(firstRewardId, ctx).toBriefList()
                    LOG_INFO('in _doCrusadeSettlement:: record first reward', spaceNo, dungeonNo, opUUId, uniqueId, win, extra)
                    self._doAddWealthVal(opUUId, gameconst.DungeonPlayModeEnum.CRUSADE, dungeonNo, win, 0, uniqueId, AAC_AACDD.datas.BONUS_SRC_TEAM_GOLD_PASS_REWARD, firstRewardId, firstPassRewards)
            self.achievementInfo.triggerAchieveByType(
                self,
                gameconst.AchieveType.CRUSADE,
                actionContext.AchievementCtx(dungeonNo=dungeonNo)
            )
            self.taskCheckCounterTarget(TCCTD.couterTargetDic['CompleteACertainInstance'], (dungeonNo,))

        box.cell.onNotifySettlementResult(self, gameconst.DungeonPlayModeEnum.CRUSADE, spaceNo, dungeonNo, opUUId, uniqueId, win, extra, firstPassRewards if firstPassRewards else [], goldPassRewards if goldPassRewards else [], dungeonRewards if dungeonRewards else [])
        self.sendDungeonFinishedMail(gameconst.DungeonPlayModeEnum.CRUSADE, dungeonNo, opUUId, extra['gbId'], win)
        LogTrackingMgr.LogTrackingMgr.Dungeon_Settlement(self.gbID, self.accountEntity.clientDistinctId, extra['uniqueID'], gameconst.DungeonPlayModeEnum.CRUSADE, dungeonNo, extra['spaceUUID'], spaceNo, self.gbID, \
                                                         True if dungeonRewards else False, True if firstPassRewards else False, extra['elaspedTime'], win, extra['completedReasonType'], extra['playerCount'], 
                                                         extra['deadCount'], firstPassRewards if firstPassRewards else {}, dungeonRewards if dungeonRewards else {}, \
                                                         goldPassRewards if goldPassRewards else {}, extra['autoCombatTimes'], self.getTotalScore(), self.getRoleCacheAttr('level'), extra['score'])

    def _doGuildBossChallengeSettlement(self, spaceNo, dungeonNo, opUUId, uniqueId, win, box, extra):
        # 没次数或者没有造成伤害，不给奖励
        if not self.checkGuildBossRewardRemainTimes(dungeonNo):
            box.cell.onNotifySettlementResult(self, gameconst.DungeonPlayModeEnum.GUILD_BOSS, spaceNo, dungeonNo, opUUId, uniqueId, win, extra, [], [], [])
            LOG_WARN('in _doGuildBossChallengeSettlement:: no reward', spaceNo, dungeonNo, opUUId, uniqueId, win, box, extra)
            return
        
        self.guildBossRewardWeeklyCount = self.guildBossRewardWeeklyCount + 1
        
        dungeonRewards = None
        firstPassRewards = None
        isFirstPass = False
        rank = extra['rank']
        score = extra['score']
        if win and score > 0:
            dataKey = dataUtils.getGuildBossRankRewardKey(dungeonNo, rank)
            dungeonRewardId = GC_RR.rankRewardDic.get(dataKey, 0)
            if dungeonRewardId > 0:
                ctx = self.getAvatarAwardCtx(dungeonRewardId, None)
                dungeonRewards = dropAward.getAwardOne(dungeonRewardId, ctx).toBriefList()
                LOG_INFO('in _doGuildBossChallengeSettlement:: record dungeon reward', spaceNo, dungeonNo, opUUId, uniqueId, win, extra)
                self._doAddWealthVal(opUUId, gameconst.DungeonPlayModeEnum.GUILD_BOSS, dungeonNo, win, rank, uniqueId, AAC_AACDD.datas.BONUS_SRC_GULID_DUNGEON_CLEAR_REWARD, dungeonRewardId, dungeonRewards)

            # 首通奖励
            entryId = GC_BI.dungeonIdxDic.get(dungeonNo)
            if self.guildBossPassRecords.checkEntryStatus(entryId):
                firstRewardId = GC_BI.fistPassRewardDic.get(dungeonNo, 0)
                if firstRewardId > 0:
                    isFirstPass = True
                    self.guildBossPassRecords.finishEntryStatus(entryId)
                    self.guildBossPassRecords = self.guildBossPassRecords
                    ctx = self.getAvatarAwardCtx(firstRewardId, None)
                    firstPassRewards = dropAward.getAwardOne(firstRewardId, ctx).toBriefList()
                    LOG_INFO('in _doGuildBossChallengeSettlement:: record first pass reward', spaceNo, dungeonNo, opUUId, uniqueId, win, extra)
                    self._doAddWealthVal(opUUId, gameconst.DungeonPlayModeEnum.GUILD_BOSS, dungeonNo, win, rank, uniqueId, AAC_AACDD.datas.BONUS_SRC_GULID_DUNGEON_FIRST_REWARD, firstRewardId, firstPassRewards)
        
        LogTrackingMgr.LogTrackingMgr.Guild_BossChallenge_Settlement(self.gbID, self.accountEntity.clientDistinctId, opUUId, self.gbID, win, score, rank, isFirstPass, firstPassRewards if firstPassRewards else [], dungeonRewards if dungeonRewards else [])
        box.cell.onNotifySettlementResult(self, gameconst.DungeonPlayModeEnum.GUILD_BOSS, spaceNo, dungeonNo, opUUId, uniqueId, win, extra, firstPassRewards if firstPassRewards else [], [], dungeonRewards if dungeonRewards else [])
        self.triggerAchievementWithCtx(gameconst.AchieveType.GUILD_ACTIVITY, actionContext.AchievementCtx(activityType=gameconst.AchieveGuildActivityType.BOSS))

    def _doInnerDemonChallengeSettlement(self, spaceNo, dungeonNo, opUUId, uniqueId, win, box, extra) :
        firstPassRewards = None
        goldPassRewards = None
        dungeonRewards = None

        score = extra['score']
        level = extra['level']
        LOG_INFO('_doInnerDemonChallengeSettlement::win, score',win, score, level)
        if win:
            dungeonRewardIdList = CID.datas.get(CID.maxKey, {}).get('rewardList', [])
            for data in CID.datas.values():
                if score >= data['time']:
                    dungeonRewardIdList = data['rewardList']
                    break
            LOG_INFO('_doInnerDemonChallengeSettlement::dungeonRewardIdList',dungeonRewardIdList)
            if len(dungeonRewardIdList) > 0:
                dungeonRewardId = 0
                for rewardIdInfo in dungeonRewardIdList:
                    if rewardIdInfo[0] > level:
                        continue
                    dungeonRewardId = rewardIdInfo[1]
                    break
                ctx = self.getAvatarAwardCtx(dungeonRewardId, None)
                dungeonRewards = dropAward.getAwardOne(dungeonRewardId, ctx).toBriefList()
                LOG_INFO('in _doInnerDemonChallengeSettlement:: record dungeon reward', dungeonRewardId, spaceNo, dungeonNo, opUUId, uniqueId, win, extra)
                self._doAddWealthVal(opUUId, gameconst.DungeonPlayModeEnum.INNER_DEMON, dungeonNo, win, 0, uniqueId, AAC_AACDD.datas.BONUS_SRC_INNER_DEMON_PASS_REWARD, dungeonRewardId, dungeonRewards)
            self.updateInnerDemonRewardCnt()

        box.cell.onNotifySettlementResult(self, gameconst.DungeonPlayModeEnum.INNER_DEMON, spaceNo, dungeonNo, opUUId, uniqueId, win, extra, firstPassRewards if firstPassRewards else [], goldPassRewards if goldPassRewards else [], dungeonRewards if dungeonRewards else [])

    def _doAddWealthVal(self, opUUID, playMode, dungeonNo, win, rank, uniqueId, src, rewardId, rewards):
        addWealthVal = dropAward.AwardVal()
        for reward in rewards:
            addWealthVal.addWealthByItemId(reward['itemId'], reward['itemNum'], reward['bindType'])
        srcType = src
        awardCtx = self.getAvatarAwardCtx(rewardId, None)
        awardCtx.addContextVar('eventTipId', dungeonNo)
        detail = gameclass.AwardDetailCls(awardIds = rewardId, playMode = playMode, dungeonNo = dungeonNo, win=win, rank=rank, uniqueId=uniqueId)
        self.addWealth(srcType, addWealthVal, opUUID, detail, awardCtx)

    def checkGuildBossRewardRemainTimes(self, dungeonNo):
        return self.guildBossRewardWeeklyCount < int(GC_C.datas['guildRewardTimes']['value'])
    
    def dungeonSettlementWeeklyReset(self, *args):
        self.guildBossRewardWeeklyCount = 0

    def sendDungeonFinishedMail(self, dungeonType, dungeonNo, opUUID, gbId, isWin):
        dungeonName = None
        if dungeonType in (gameconst.DungeonPlayModeEnum.CHIEF, gameconst.DungeonPlayModeEnum.CROSS_CHIEF):
            entryId = RBC_BI.dungeonIdxDic.get(dungeonNo)
            dungeonName = RBC_BI.datas[entryId]['name']
        elif dungeonType in (gameconst.DungeonPlayModeEnum.CRUSADE, gameconst.DungeonPlayModeEnum.CROSS_CRUSADE):
            entryId = TDC_BI.dungeonIdxDic.get(dungeonNo)
            dungeonName = TDC_BI.datas[entryId]['name']
        else:
            return
        
        if not isWin:
            mailAssistor.sendMailToPlayers([gbId], int(TDC_CFG.datas['raid_mailFailure']['value']), opUUID=opUUID, 
                                        despArgs=(dungeonName,), srcType=AAC_AACDD.datas.BONUS_SRC_DUNGEON_FINISHED)
            
