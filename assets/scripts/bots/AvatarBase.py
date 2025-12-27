# -*- encoding:utf-8 -*-
# defined in */scripts/entity_defs/Avatar.def
# It is generated automatically, please do not modify manually
import KBEngine

class AvatarBase(KBEngine.Entity):
    def beNotifiedApplyJoinRaid(self, arg0, arg1, arg2): pass
    def biddingFailRedPointSync(self, arg0): pass
    def bindPhoneReplay(self, arg0, arg1): pass
    def changeDungeonRemainTime(self, arg0, arg1): pass
    def changeSelfCameraLookPos(self, arg0): pass
    def changeSelfCameraStatus(self, arg0): pass
    def claimPcLoginRewardInfo(self, arg0, arg1): pass
    def dragSkillChangeBuildSkills(self, arg0): pass
    def duelFlagIn(self): pass
    def duelFlagOut(self): pass
    def leaderBoardNotChanged(self, arg0, arg1, arg2): pass
    def notifyCastingSkill(self, arg0, arg1): pass
    def onAddAureole(self, arg0): pass
    def onAddAureoleFromOthers(self, arg0): pass
    def onAddBagItems(self, arg0, arg1, arg2, arg3, arg4, arg5): pass
    def onAddBuff(self, arg0): pass
    def onAddChallengeAvatar(self, arg0): pass
    def onAddCubeRoomRewardRecord(self, arg0): pass
    def onAddFirstBuyCredit(self, arg0): pass
    def onAddGatherRewardRecord(self, arg0): pass
    def onAddGuildRelationClient(self, arg0, arg1): pass
    def onAddNewEquipDrop(self, arg0): pass
    def onAddNewRaidMember(self, arg0, arg1, arg2, arg3): pass
    def onAddPassiveSkill(self, arg0, arg1): pass
    def onAddSkill(self, arg0, arg1, arg2, arg3, arg4, arg5): pass
    def onAddTeam(self, arg0): pass
    def onAddTeamMember(self, arg0): pass
    def onAddWonderLandRewardRecord(self, arg0): pass
    def onAllAliasIds(self, arg0): pass
    def onAllApplyGuildUnion(self, arg0): pass
    def onAnotherClientLogin(self): pass
    def onAppearanceOutfitUpdated(self, arg0, arg1): pass
    def onAppearanceUpdated(self, arg0, arg1): pass
    def onApplyBecomeCaptainMsg(self, arg0, arg1): pass
    def onApplyGather(self, arg0, arg1): pass
    def onApplyInviteTeamMsg(self, arg0, arg1, arg2, arg3, arg4, arg5, arg6): pass
    def onApplyJoinRaidLonelyFailed(self, arg0, arg1, arg2, arg3, arg4): pass
    def onApplyJoinTeamFailed(self, arg0, arg1, arg2, arg3, arg4): pass
    def onApplyJoinTeamMsg(self, arg0, arg1, arg2, arg3, arg4, arg5): pass
    def onAvatarTotalScoreInitCompleted(self): pass
    def onBackSelectCharacter(self): pass
    def onBagItemsDailyUpdate(self, arg0): pass
    def onBeInvitedRaidByLeader(self, arg0, arg1, arg2, arg3, arg4, arg5, arg6): pass
    def onBeInvitedRaidByMember(self, arg0, arg1, arg2, arg3, arg4, arg5, arg6): pass
    def onBeInvitedRaidByTeamCaptain(self, arg0, arg1, arg2, arg3, arg4, arg5, arg6): pass
    def onBindItemSucc(self, arg0, arg1): pass
    def onBreakCastingSkill(self, arg0, arg1, arg2): pass
    def onBreakChannelingSkill(self, arg0, arg1, arg2): pass
    def onBuyCreditSuccess(self, arg0): pass
    def onBuyItemInCoinAuctionByAuctionItemUUID(self, arg0, arg1, arg2, arg3, arg4): pass
    def onBuyItemInCoinAuctionByAuctionItemUUIDFailed(self, arg0, arg1): pass
    def onBuyStoreItems(self, arg0, arg1, arg2, arg3, arg4): pass
    def onCancelAuthRole(self, arg0, arg1): pass
    def onCancelGather(self): pass
    def onCancelGuildDungeonOrder(self, arg0): pass
    def onCancelSaleCanStackedItemInCoinAuction(self, arg0, arg1, arg2, arg3): pass
    def onCancelSaleItemInCoinAuction(self, arg0, arg1, arg2): pass
    def onCancelSaleItemInCoinAuctionFail(self, arg0): pass
    def onChangeCaptain(self, arg0): pass
    def onChangeCityMoneyToGuildMoneyResult(self, arg0, arg1): pass
    def onChangeRaidMark(self, arg0): pass
    def onChangeSkill(self, arg0, arg1): pass
    def onChangeTeamMark(self, arg0): pass
    def onChangeWonderLandRenewTimes(self, arg0): pass
    def onCityBattleTokenChanged(self, arg0): pass
    def onCityDataResponse(self, arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13, arg14, arg15, arg16): pass
    def onClaimTask(self, arg0, arg1): pass
    def onClearRaidApplyJoinDic(self, arg0): pass
    def onClearRaidData(self): pass
    def onClientAuthState(self, arg0): pass
    def onClientDataSyncFinished(self): pass
    def onCreateRaid(self, arg0): pass
    def onCrossServerTokenResp(self, arg0, arg1, arg2): pass
    def onCubeAutoRenewSwitch(self, arg0, arg1): pass
    def onCubeLoginData(self, arg0, arg1, arg2, arg3): pass
    def onCubeRoomEndTime(self, arg0): pass
    def onCubeRoomLeftTime(self, arg0): pass
    def onDailyUseMoneyChanged(self, arg0): pass
    def onDead(self, arg0): pass
    def onDealAuthResult(self, arg0): pass
    def onDeathPenaltyExpChange(self, arg0): pass
    def onDeathPenaltyReward(self, arg0, arg1, arg2, arg3): pass
    def onDelMails(self, arg0): pass
    def onDelRaidApplyJoinRecord(self, arg0, arg1): pass
    def onDelTeamMember(self, arg0): pass
    def onDisbandRaid(self, arg0): pass
    def onDressEquipment(self, arg0): pass
    def onDropAward(self, arg0, arg1, arg2): pass
    def onDuelFlagsChanged(self, arg0): pass
    def onDuelResult(self, arg0, arg1, arg2): pass
    def onDungenFinishRewards(self, arg0, arg1, arg2, arg3, arg4): pass
    def onDungeonChallengeSettlement(self, arg0): pass
    def onDungeonCompleteDungeonData(self, arg0, arg1): pass
    def onDungeonCompleteSettlementData(self, arg0, arg1): pass
    def onDungeonCompleted(self, arg0, arg1, arg2, arg3): pass
    def onEnemyDatas(self, arg0): pass
    def onEnhanceMeridian(self, arg0): pass
    def onEnterGuildDungeon(self, arg0, arg1): pass
    def onEquipBackBlessSucc(self, arg0, arg1, arg2, arg3, arg4, arg5): pass
    def onEquipBindValueWashingFailed(self, arg0, arg1): pass
    def onEquipBindValueWashingSucc(self, arg0, arg1, arg2, arg3, arg4): pass
    def onEquipBlessSucc(self, arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7): pass
    def onEquipBroken(self, arg0, arg1): pass
    def onEquipDropStateChange(self, arg0, arg1): pass
    def onEquipEnhanceFailed(self, arg0, arg1): pass
    def onEquipEnhanceSucc(self, arg0, arg1, arg2, arg3, arg4, arg5): pass
    def onEquipGlyphApplySucc(self, arg0, arg1, arg2, arg3): pass
    def onEquipGlyphWashingSucc(self, arg0, arg1, arg2, arg3, arg4, arg5, arg6): pass
    def onEquipMakeFailed(self): pass
    def onEquipMakeSucc(self, arg0): pass
    def onEquipSpiritApplySucc(self, arg0, arg1, arg2, arg3): pass
    def onEquipSpiritWashingSucc(self, arg0, arg1, arg2, arg3, arg4, arg5, arg6): pass
    def onEquipUpgradeFailed(self, arg0, arg1): pass
    def onEquipUpgradeSucc(self, arg0, arg1, arg2, arg3, arg4, arg5): pass
    def onEventTips(self, arg0, arg1): pass
    def onExchangeRaidTeamMember(self, arg0, arg1, arg2, arg3, arg4): pass
    def onExitGuildClient(self): pass
    def onFollowTeamCaptainAsk(self, arg0, arg1): pass
    def onFriendMsgChanged(self, arg0, arg1, arg2): pass
    def onFriendRequests(self, arg0): pass
    def onGameConfigChanged(self, arg0, arg1): pass
    def onGatherSucc(self, arg0): pass
    def onGetAllRaidList(self, arg0): pass
    def onGetAllTeamList(self, arg0): pass
    def onGetAuctionItemsByAuctionIdsResp(self, arg0, arg1, arg2, arg3): pass
    def onGetAureoleInfo(self, arg0, arg1): pass
    def onGetBuffIdInfo(self, arg0, arg1): pass
    def onGetBuffInfo(self, arg0, arg1): pass
    def onGetChagllengeDataInfo(self, arg0): pass
    def onGetCoinAuctionPlayerInfo(self, arg0, arg1, arg2): pass
    def onGetCollectInfo(self, arg0): pass
    def onGetCurrentSaleItemInfoResp(self, arg0, arg1, arg2, arg3, arg4): pass
    def onGetDeathPenaltyExpLogin(self, arg0): pass
    def onGetDrawCardInfo(self, arg0): pass
    def onGetEnemyFreshInfo(self, arg0): pass
    def onGetEnemyGuildInfosClient(self, arg0): pass
    def onGetFriendMsgs(self, arg0, arg1, arg2): pass
    def onGetGuaranteedPetEgg(self, arg0, arg1, arg2): pass
    def onGetGuildBossHP(self, arg0, arg1, arg2): pass
    def onGetGuildData(self, arg0): pass
    def onGetGuildListData(self, arg0): pass
    def onGetGuildUnionApplySender(self, arg0): pass
    def onGetInterInfoClient(self, arg0): pass
    def onGetItemLastAndAvgPrice(self, arg0, arg1, arg2): pass
    def onGetItemNumByCategoryIdResp(self, arg0, arg1, arg2, arg3, arg4): pass
    def onGetLevelWelfareInfo(self, arg0, arg1): pass
    def onGetLineInfo(self, arg0): pass
    def onGetLingShouBattleList(self, arg0): pass
    def onGetMailAttach(self, arg0): pass
    def onGetMailList(self, arg0): pass
    def onGetMeridianData(self, arg0, arg1, arg2): pass
    def onGetMineWarCollectInfo(self, arg0, arg1): pass
    def onGetMineWarGuildMemberScore(self, arg0, arg1): pass
    def onGetNewMail(self, arg0): pass
    def onGetPlayerPayInfo(self, arg0, arg1, arg2): pass
    def onGetRaidAllMembersAttrs(self, arg0, arg1): pass
    def onGetRaidApplyJoinList(self, arg0, arg1): pass
    def onGetRaidData(self, arg0): pass
    def onGetRaidList(self, arg0, arg1, arg2): pass
    def onGetRedBagMyList(self, arg0): pass
    def onGetRedBagRankList(self, arg0): pass
    def onGetServerOpenTime(self, arg0): pass
    def onGetSettlementRankList(self, arg0, arg1, arg2, arg3, arg4): pass
    def onGetStatisticsClient(self, arg0, arg1): pass
    def onGetStatisticsDetailClient(self, arg0, arg1, arg2, arg3): pass
    def onGetStoreLimitedItemList(self, arg0, arg1): pass
    def onGetStoreList(self, arg0): pass
    def onGetSynthesisUpgradeNum(self, arg0): pass
    def onGetTeamList(self, arg0, arg1, arg2): pass
    def onGetVariableData(self, arg0, arg1): pass
    def onGetWelfareSignInInfo(self, arg0, arg1): pass
    def onGlyphReplacedSkillIdx(self, arg0, arg1): pass
    def onGobackServer(self, arg0): pass
    def onGuildApplyJoinList(self, arg0): pass
    def onGuildBuildingChanged(self, arg0): pass
    def onGuildDescChanged(self, arg0): pass
    def onGuildDispChanged(self, arg0): pass
    def onGuildEventLogs(self, arg0): pass
    def onGuildExpChanged(self, arg0): pass
    def onGuildFundChanged(self, arg0): pass
    def onGuildIconChanged(self, arg0): pass
    def onGuildInfoFromCrossData(self, arg0): pass
    def onGuildInfosByRelationType(self, arg0, arg1): pass
    def onGuildInvateToClient(self, arg0): pass
    def onGuildJobData(self, arg0): pass
    def onGuildJoinCondChanged(self, arg0): pass
    def onGuildLevelChanged(self, arg0): pass
    def onGuildMemberDatas(self, arg0): pass
    def onGuildMoneyChanged(self, arg0): pass
    def onGuildRelationAll(self, arg0): pass
    def onGuildTrainResetClient(self): pass
    def onGuildTrainsInit(self, arg0): pass
    def onHealItemResult(self, arg0, arg1): pass
    def onHolidayPayUpdate(self, arg0): pass
    def onHookRewardTaskRefresh(self, arg0): pass
    def onHookRewardTaskWeeklyLimitRefresh(self, arg0): pass
    def onHotfixVersion(self, arg0): pass
    def onInitEnemyRecord(self, arg0, arg1): pass
    def onInitEquipDropData(self, arg0): pass
    def onKillAvatar(self, arg0): pass
    def onLeaderBoardAvatarLevel(self, arg0, arg1, arg2, arg3, arg4, arg5): pass
    def onLeaderBoardAvatarLevelRushRank(self, arg0, arg1, arg2, arg3, arg4, arg5): pass
    def onLeaderBoardAvatarScore(self, arg0, arg1, arg2, arg3, arg4, arg5): pass
    def onLeaderBoardGuild(self, arg0, arg1, arg2, arg3, arg4): pass
    def onLeaveTeam(self): pass
    def onLeveUpMeridianPointTo(self, arg0, arg1, arg2): pass
    def onLightPillarUpdate(self, arg0, arg1): pass
    def onLockItemSucc(self, arg0, arg1, arg2, arg3): pass
    def onMapUnlockMessagePre(self, arg0): pass
    def onMessage(self, arg0, arg1): pass
    def onMineWarEndInfo(self, arg0, arg1, arg2, arg3): pass
    def onMineWarGuildOwnerRank(self, arg0, arg1): pass
    def onMineWarGuildPlayerRank(self, arg0, arg1): pass
    def onMineWarInfo(self, arg0): pass
    def onMineWarShareBonusResult(self, arg0): pass
    def onNewApplyGuildUnion(self, arg0): pass
    def onNewBlazeId(self, arg0): pass
    def onNewEnemyRecord(self, arg0, arg1): pass
    def onNewGuildUnionApplySender(self, arg0): pass
    def onNewbieGuideId(self, arg0): pass
    def onNotifyApplyJoinInfo(self, arg0): pass
    def onNotifyStartBattleCD(self, arg0, arg1): pass
    def onNotiyNewAuctionItemCollection(self, arg0): pass
    def onOfficialMessage(self, arg0, arg1, arg2, arg3, arg4): pass
    def onOfflineHangupData(self, arg0, arg1): pass
    def onOpenGuildDungeon(self, arg0, arg1, arg2): pass
    def onOthersSkillDamage(self, arg0, arg1): pass
    def onPickNewEquipDrop(self, arg0): pass
    def onPlayerCoinAuctionItemBeSaled(self, arg0, arg1, arg2): pass
    def onPlayerGetExp(self, arg0, arg1, arg2, arg3): pass
    def onPopRaidTeamMember(self, arg0, arg1, arg2): pass
    def onQixieChanged(self, arg0): pass
    def onQueryItemLink(self, arg0, arg1): pass
    def onQueryPlayerLink(self, arg0): pass
    def onQuerySiegeWarBiddingWinnerDataResult(self, arg0, arg1, arg2, arg3, arg4, arg5, arg6): pass
    def onQuerySiegeWarCityFundUseRecordResult(self, arg0): pass
    def onQuerySiegeWarDefenderAndOffensiveResult(self, arg0): pass
    def onQuerySiegeWarSignUped(self, arg0): pass
    def onRaidAvatarLogin(self, arg0, arg1, arg2): pass
    def onRaidAvatarOffline(self, arg0, arg1, arg2): pass
    def onRaidPlayerStartAutoMatch(self): pass
    def onRaidPlayerStopAutoMatch(self): pass
    def onRandomSummonPet(self, arg0): pass
    def onRandomSynthesis(self, arg0): pass
    def onReadOneMail(self, arg0): pass
    def onRecvAuthRoleClient(self, arg0, arg1): pass
    def onRecvAvatarChannelMsg(self, arg0, arg1, arg2): pass
    def onRecvDuelReq(self, arg0, arg1): pass
    def onRecvTrumpetMsg(self, arg0, arg1, arg2): pass
    def onRedBagPlayerInfo(self, arg0, arg1): pass
    def onReleaseRedBagMsg(self, arg0, arg1, arg2, arg3, arg4, arg5): pass
    def onRemoveApplyGuildUnion(self, arg0): pass
    def onRemoveApplyedGuilds(self, arg0): pass
    def onRemoveAureole(self, arg0): pass
    def onRemoveAureoleFromOthers(self, arg0): pass
    def onRemoveBlocks(self, arg0): pass
    def onRemoveBuff(self, arg0, arg1): pass
    def onRemoveChallengeAvatar(self, arg0): pass
    def onRemoveCompleteWitness(self, arg0): pass
    def onRemoveEnemy(self, arg0): pass
    def onRemoveEquipDrop(self, arg0): pass
    def onRemoveFriendRequests(self, arg0): pass
    def onRemoveFriends(self, arg0): pass
    def onRemoveFromApplyList(self, arg0): pass
    def onRemoveGuildApplys(self, arg0): pass
    def onRemoveGuildMember(self, arg0): pass
    def onRemoveGuildRelationClient(self, arg0): pass
    def onRemoveInstantPotionSlots(self, arg0): pass
    def onRemovePickEquipDrop(self, arg0): pass
    def onRemoveRecent(self, arg0): pass
    def onRemoveStrangers(self, arg0): pass
    def onReplyRaidStandbyChecker(self, arg0, arg1): pass
    def onSaleItemInCoinAuction(self, arg0, arg1, arg2): pass
    def onSceneState(self, arg0): pass
    def onSearchCoinAuctionItemsByItemId(self, arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7): pass
    def onSearchFriends(self, arg0, arg1): pass
    def onSellItemSucc(self, arg0, arg1, arg2, arg3): pass
    def onSendHolidayPayInfo(self, arg0): pass
    def onSetAddSkillCd(self, arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7): pass
    def onSetInstantPotionSlots(self, arg0): pass
    def onSetRaidDeputy(self, arg0, arg1): pass
    def onSetRaidDungeonInfo(self, arg0, arg1): pass
    def onSetRaidLeader(self, arg0, arg1): pass
    def onSetRaidTarget(self, arg0, arg1, arg2, arg3, arg4, arg5, arg6): pass
    def onSetRaidTeamCaptain(self, arg0, arg1, arg2): pass
    def onSetTeamTarget(self, arg0, arg1, arg2, arg3, arg4, arg5, arg6): pass
    def onShooterSkillCanUse(self, arg0, arg1, arg2): pass
    def onShowMineWarMonsterInfo(self, arg0, arg1, arg2, arg3, arg4, arg5): pass
    def onShowPopReward(self, arg0, arg1, arg2): pass
    def onShowRedBagInfo(self, arg0, arg1, arg2): pass
    def onSiegeWarBattleEnd(self, arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8): pass
    def onSiegeWarBiddingDataUpdate(self, arg0, arg1, arg2, arg3): pass
    def onSiegeWarDeclareWarResult(self, arg0, arg1): pass
    def onSiegeWarEnterDataUpdate(self, arg0, arg1, arg2): pass
    def onSiegeWarLoginDataChanged(self, arg0, arg1): pass
    def onSiegeWarMinimapInfoUpdate(self, arg0): pass
    def onSiegeWarMinimapSignalChange(self, arg0): pass
    def onSiegeWarScoreData(self, arg0, arg1, arg2): pass
    def onSiegeWarSearchTargetResult(self, arg0, arg1): pass
    def onSiegeWarSignUpBiddingResult(self, arg0): pass
    def onSkillDamage(self, arg0): pass
    def onStartAutoCombat(self): pass
    def onStartPlayCinema(self, arg0): pass
    def onStopAutoCombat(self): pass
    def onSyncCitySimpleData(self, arg0, arg1, arg2, arg3): pass
    def onTakeAchievementRewards(self, arg0, arg1): pass
    def onTaskUpdate(self, arg0): pass
    def onTasksRem(self, arg0): pass
    def onTeamAutoMatch(self, arg0): pass
    def onTeamDisband(self): pass
    def onTeamStopAutoMatch(self): pass
    def onTeammateConfirm(self, arg0): pass
    def onTeammateConfirmBroadcastStatus(self, arg0, arg1): pass
    def onTeammateConfirmCrusade(self, arg0, arg1): pass
    def onTeleportCasting(self, arg0, arg1): pass
    def onTeleportDone(self, arg0, arg1): pass
    def onTriggerGuide(self, arg0): pass
    def onTryBeInvitedInRaid(self, arg0, arg1, arg2, arg3): pass
    def onUnblockRaidMemberMisc(self, arg0, arg1, arg2): pass
    def onUnblockTeamMemberMisc(self, arg0, arg1): pass
    def onUndressEquipment(self, arg0): pass
    def onUnlockGrids(self, arg0, arg1): pass
    def onUnlockWarehouseGrids(self, arg0, arg1): pass
    def onUpdateAchieveDatas(self, arg0): pass
    def onUpdateApplyedGuilds(self, arg0): pass
    def onUpdateAureoles(self, arg0): pass
    def onUpdateAureolesFromOthers(self, arg0): pass
    def onUpdateBlocks(self, arg0): pass
    def onUpdateBuff(self, arg0): pass
    def onUpdateBuffs(self, arg0): pass
    def onUpdateCollectionGatherFlag(self, arg0, arg1): pass
    def onUpdateCollectionGatherPickTimes(self, arg0, arg1, arg2): pass
    def onUpdateCreditNum(self, arg0, arg1): pass
    def onUpdateDailyUseLimit(self, arg0, arg1): pass
    def onUpdateDrawCardInfo(self, arg0): pass
    def onUpdateFriendsDiff(self, arg0): pass
    def onUpdateFriendsFull(self, arg0): pass
    def onUpdateGridItemsExpireTime(self, arg0, arg1): pass
    def onUpdateGridItemsJson(self, arg0, arg1, arg2, arg3): pass
    def onUpdateGridItemsNum(self, arg0, arg1): pass
    def onUpdateGuildMemberDatas(self, arg0): pass
    def onUpdateGuildTrains(self, arg0): pass
    def onUpdateItemCD(self, arg0, arg1, arg2): pass
    def onUpdateLingShouBattleList(self, arg0, arg1, arg2): pass
    def onUpdateLingShouData(self, arg0): pass
    def onUpdateLingShouEquip(self, arg0, arg1, arg2): pass
    def onUpdateMemberAttr(self, arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7): pass
    def onUpdateOutfitData(self, arg0): pass
    def onUpdatePetBattleListName(self, arg0, arg1): pass
    def onUpdateRaidMemberHP(self, arg0, arg1, arg2): pass
    def onUpdateRaidMemberLevel(self, arg0, arg1): pass
    def onUpdateRaidMemberPos(self, arg0, arg1, arg2): pass
    def onUpdateRaidMemberScore(self, arg0, arg1): pass
    def onUpdateRecentData(self, arg0): pass
    def onUpdateSkillLevel(self, arg0, arg1): pass
    def onUpdateStrangerData(self, arg0): pass
    def onUpdateSynthesisUpgradeNum(self, arg0): pass
    def onUpdateTeamMemberHp(self, arg0, arg1, arg2): pass
    def onUpdateTeamMemberPos(self, arg0, arg1, arg2): pass
    def onUpdateTeamMemberScore(self, arg0, arg1): pass
    def onUpgradeSynthesis(self, arg0): pass
    def onUseCasting(self, arg0, arg1, arg2, arg3, arg4, arg5): pass
    def onUseChanneling(self, arg0, arg1, arg2, arg3, arg4, arg5, arg6): pass
    def onUseSkill(self, arg0, arg1, arg2, arg3, arg4, arg5): pass
    def onUseStageSkill(self, arg0, arg1, arg2): pass
    def onVariableChanged(self, arg0, arg1): pass
    def onWarehouseInItems(self, arg0, arg1): pass
    def onWarehouseLockItemSucc(self, arg0, arg1, arg2): pass
    def onWarehouseOutItems(self, arg0, arg1, arg2): pass
    def onWonderLandBossInfo(self, arg0): pass
    def onWonderLandLeftTime(self, arg0): pass
    def onWonderLandLoginData(self, arg0, arg1, arg2, arg3): pass
    def onWonderLandSwitch(self, arg0, arg1): pass
    def onWorkshopMF(self, arg0, arg1, arg2, arg3): pass
    def onYuxiFlagChange(self, arg0): pass
    def popDialog(self, arg0): pass
    def recvGetGuildDetailInfo(self, arg0): pass
    def revertSelfCameraStatus(self): pass
    def selfGuildNameChanged(self, arg0, arg1): pass
    def sendAllSkills(self, arg0): pass
    def sendEnemyPosInfoToClient(self, arg0, arg1, arg2): pass
    def sendSkillBuilds(self, arg0): pass
    def showMineWarEnd(self): pass
    def showMineWarPrepare(self, arg0, arg1): pass
    def showMineWarStart(self, arg0, arg1): pass
    def showPopoverMsg(self, arg0): pass
    def showPopoverMsgWithArg(self, arg0, arg1): pass
    def startTeleport(self, arg0, arg1): pass
    def stopOfficialMessage(self, arg0): pass
    def syncGuildTaskInfo(self, arg0): pass
    def syncServerTime(self, arg0, arg1): pass
    def updateSkillsExtraLevel(self, arg0, arg1, arg2): pass
