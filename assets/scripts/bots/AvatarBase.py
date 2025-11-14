# -*- encoding:utf-8 -*-
# defined in */scripts/entity_defs/Avatar.def
# It is generated automatically, please do not modify manually
import KBEngine

class AvatarBase(KBEngine.Entity):
    def applyFollowTeamCaptainTransDirectlyNotify(self): pass
    def applyFollowTeamCaptainTransToTelNotify(self): pass
    def beNotifiedApplyJoinRaid(self, arg0, arg1, arg2): pass
    def biddingFailRedPointSync(self, arg0): pass
    def breakAwayStuckFailed(self): pass
    def changeDungeonRemainTime(self, arg0, arg1): pass
    def changeSelfCameraLookPos(self, arg0): pass
    def changeSelfCameraStatus(self, arg0): pass
    def cityRecentActivityResponse(self, arg0, arg1): pass
    def dragSkillChangeBuildSkills(self, arg0): pass
    def duelFlagIn(self): pass
    def duelFlagOut(self): pass
    def leaderBoardNotChanged(self, arg0, arg1, arg2): pass
    def notifyCastingSkill(self, arg0, arg1): pass
    def notifyClientSelfBigWorldLineCachedPos(self, arg0, arg1): pass
    def onAddAureole(self, arg0): pass
    def onAddAureoleFromOthers(self, arg0): pass
    def onAddBagItems(self, arg0, arg1, arg2, arg3, arg4, arg5): pass
    def onAddBuff(self, arg0): pass
    def onAddChallengeAvatar(self, arg0): pass
    def onAddCubeRoomRewardRecord(self, arg0): pass
    def onAddFirstBuyCredit(self, arg0): pass
    def onAddGatherRewardRecord(self, arg0): pass
    def onAddGuildRelationClient(self, arg0, arg1): pass
    def onAddLevelAwards(self, arg0): pass
    def onAddNewEquipDrop(self, arg0): pass
    def onAddNewRaidMember(self, arg0, arg1, arg2, arg3): pass
    def onAddPassiveSkill(self, arg0, arg1): pass
    def onAddRaidDungeonRewardRecord(self, arg0, arg1, arg2): pass
    def onAddSkill(self, arg0, arg1, arg2, arg3, arg4, arg5): pass
    def onAddStateRet(self, arg0, arg1, arg2, arg3): pass
    def onAddTeam(self, arg0): pass
    def onAddTeamDungeonRewardRecord(self, arg0, arg1, arg2): pass
    def onAddTeamMember(self, arg0): pass
    def onAddWonderLandRewardRecord(self, arg0): pass
    def onAffixWashingFailed(self): pass
    def onAllAliasIds(self, arg0): pass
    def onAllApplyGuildUnion(self, arg0): pass
    def onAnotherClientLogin(self): pass
    def onAppearanceOutfitUpdated(self, arg0, arg1): pass
    def onAppearanceUpdated(self, arg0, arg1): pass
    def onApplyBecomeCaptainMsg(self, arg0, arg1): pass
    def onApplyGather(self, arg0, arg1): pass
    def onApplyInviteTeamMsg(self, arg0, arg1, arg2, arg3, arg4, arg5, arg6): pass
    def onApplyJoinTeamFailed(self, arg0): pass
    def onApplyJoinTeamMsg(self, arg0, arg1, arg2, arg3, arg4, arg5): pass
    def onAskConfirmFollowCaptain(self): pass
    def onAvatarEquipSetChanged(self, arg0, arg1, arg2, arg3): pass
    def onAvatarLevelUp(self, arg0, arg1): pass
    def onAvatarTotalScoreInitCompleted(self): pass
    def onBackLogin(self): pass
    def onBackSelectCharacter(self): pass
    def onBagItemsDailyUpdate(self, arg0): pass
    def onBasePersistPropChanged(self, arg0, arg1): pass
    def onBeInvitedRaidByDeputy(self, arg0, arg1, arg2, arg3, arg4, arg5, arg6): pass
    def onBeInvitedRaidByLeader(self, arg0, arg1, arg2, arg3, arg4, arg5, arg6): pass
    def onBeInvitedRaidByMember(self, arg0, arg1, arg2, arg3, arg4, arg5, arg6): pass
    def onBeInvitedRaidByTeamCaptain(self, arg0, arg1, arg2, arg3, arg4, arg5, arg6): pass
    def onBindItemSucc(self, arg0, arg1): pass
    def onBlockAllRaidMemberMics(self, arg0, arg1): pass
    def onBlockAllTeamMemberMics(self, arg0, arg1): pass
    def onBodyEquipDailyUpdate(self, arg0): pass
    def onBreakCastingSkill(self, arg0, arg1, arg2): pass
    def onBreakChannelingSkill(self, arg0, arg1, arg2): pass
    def onBroadPlayAnimation(self, arg0, arg1): pass
    def onBuyCreditSuccess(self, arg0): pass
    def onBuyItemInCoinAuctionByAuctionItemUUID(self, arg0, arg1, arg2, arg3, arg4): pass
    def onBuyItemInCoinAuctionByAuctionItemUUIDFailed(self, arg0, arg1): pass
    def onBuyStoreItems(self, arg0, arg1, arg2, arg3): pass
    def onCancelChangeAppearance(self, arg0): pass
    def onCancelDigTreasure(self, arg0): pass
    def onCancelGather(self): pass
    def onCancelSaleCanStackedItemInCoinAuction(self, arg0, arg1, arg2, arg3): pass
    def onCancelSaleItemInCoinAuction(self, arg0, arg1, arg2): pass
    def onCancelSaleItemInCoinAuctionFail(self, arg0): pass
    def onCaptainCancleFollowTeam(self): pass
    def onCellPersistPropChanged(self, arg0, arg1): pass
    def onChangeCaptain(self, arg0): pass
    def onChangeCityMoneyToGuildMoneyResult(self, arg0, arg1): pass
    def onChangeRaidMark(self, arg0): pass
    def onChangeSkill(self, arg0, arg1): pass
    def onChangeTeamMark(self, arg0): pass
    def onChangeWonderLandRenewTimes(self, arg0): pass
    def onCheckUseHomeItemCond(self, arg0, arg1, arg2, arg3): pass
    def onCityBattleTokenChanged(self, arg0): pass
    def onCityDataResponse(self, arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13, arg14, arg15, arg16): pass
    def onClaimTask(self, arg0, arg1): pass
    def onClearRaidApplyJoinDic(self, arg0): pass
    def onClearRaidData(self): pass
    def onClearRaidDungeonInfo(self, arg0, arg1, arg2): pass
    def onClearSpeak(self, arg0): pass
    def onClientAuthState(self, arg0): pass
    def onClientDataSyncFinished(self): pass
    def onClientLaunchReward(self, arg0): pass
    def onCollectHolyArtifactFragment(self, arg0): pass
    def onCommonCastSuccess(self): pass
    def onCompoundRes(self, arg0, arg1, arg2, arg3): pass
    def onCreateRaid(self, arg0): pass
    def onCrossServerTokenResp(self, arg0, arg1, arg2): pass
    def onCsharpTest(self, arg0): pass
    def onCubeAutoRenewSwitch(self, arg0, arg1): pass
    def onCubeLoginData(self, arg0, arg1, arg2, arg3): pass
    def onCubeRoomEndTime(self, arg0): pass
    def onDead(self, arg0): pass
    def onDealAuthResult(self, arg0): pass
    def onDeathPenaltyExpChange(self, arg0): pass
    def onDeathPenaltyReward(self, arg0, arg1, arg2, arg3): pass
    def onDelAllMails(self): pass
    def onDelMails(self, arg0): pass
    def onDelRaidApplyJoinRecord(self, arg0, arg1): pass
    def onDelTeamMember(self, arg0): pass
    def onDigTreasureSucc(self, arg0): pass
    def onDisbandRaid(self, arg0): pass
    def onDoChangeAppearanceToMakeUpFace(self, arg0, arg1, arg2): pass
    def onDoChangeAppearanceToMakeUpSex(self, arg0, arg1, arg2, arg3): pass
    def onDressEquipment(self, arg0): pass
    def onDropAward(self, arg0, arg1, arg2): pass
    def onDropRuneIds(self, arg0, arg1, arg2): pass
    def onDuelFlagsChanged(self, arg0): pass
    def onDuelResult(self, arg0, arg1, arg2): pass
    def onDungeonCompleted(self, arg0, arg1, arg2, arg3): pass
    def onEnemyDatas(self, arg0): pass
    def onEnhanceMeridian(self, arg0): pass
    def onEnterSingleDungeon(self, arg0): pass
    def onEquipBackBlessSucc(self, arg0, arg1, arg2, arg3, arg4, arg5): pass
    def onEquipBaseAttrWashingSucc(self, arg0, arg1, arg2): pass
    def onEquipBindValueWashingFailed(self, arg0, arg1): pass
    def onEquipBindValueWashingSucc(self, arg0, arg1, arg2, arg3): pass
    def onEquipBlessSucc(self, arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7): pass
    def onEquipBroken(self, arg0, arg1): pass
    def onEquipDisassemble(self, arg0, arg1, arg2): pass
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
    def onFightPropsChanged(self): pass
    def onFirstUnlockEquipSet(self, arg0, arg1): pass
    def onFlashSkillZed(self, arg0): pass
    def onFollowCaptainChanged(self, arg0, arg1): pass
    def onFollowTeamCaptainAsk(self, arg0, arg1): pass
    def onFriendMsgChanged(self, arg0, arg1, arg2): pass
    def onFriendRequests(self, arg0): pass
    def onGameConfigChanged(self, arg0, arg1): pass
    def onGatherSucc(self, arg0): pass
    def onGetAllRaidList(self, arg0): pass
    def onGetAllTeamList(self, arg0): pass
    def onGetAureoleInfo(self, arg0, arg1): pass
    def onGetAvatarCoinBill(self, arg0, arg1, arg2, arg3, arg4): pass
    def onGetBuffIdInfo(self, arg0, arg1): pass
    def onGetBuffInfo(self, arg0, arg1): pass
    def onGetCaptainFollowInfo(self, arg0, arg1, arg2): pass
    def onGetCaptainPos(self, arg0, arg1, arg2): pass
    def onGetCoinAuctionPlayerInfo(self, arg0, arg1, arg2): pass
    def onGetCollectInfo(self, arg0): pass
    def onGetCurrentSaleItemInfoResp(self, arg0, arg1, arg2, arg3): pass
    def onGetDeathPenaltyExpLogin(self, arg0): pass
    def onGetDrawCardInfo(self, arg0): pass
    def onGetDunTimeFreezeFlag(self, arg0): pass
    def onGetEnemyFreshInfo(self, arg0): pass
    def onGetEnemyGuildInfosClient(self, arg0): pass
    def onGetFollowRideFlag(self, arg0): pass
    def onGetFriendMsgs(self, arg0, arg1, arg2): pass
    def onGetGuaranteedPetEgg(self, arg0, arg1, arg2): pass
    def onGetGuildData(self, arg0): pass
    def onGetGuildListData(self, arg0): pass
    def onGetGuildUnionApplySender(self, arg0): pass
    def onGetHolyArtifactsData(self, arg0): pass
    def onGetInterInfoClient(self, arg0): pass
    def onGetItemLastAndAvgPrice(self, arg0, arg1, arg2): pass
    def onGetItemNumByCategoryIdResp(self, arg0, arg1, arg2, arg3): pass
    def onGetLineInfo(self, arg0): pass
    def onGetLingShouBattleList(self, arg0): pass
    def onGetMailAttach(self, arg0): pass
    def onGetMailList(self, arg0): pass
    def onGetMeridianData(self, arg0, arg1, arg2): pass
    def onGetNewMail(self, arg0): pass
    def onGetOnlineRewardData(self, arg0, arg1): pass
    def onGetOnlineTimeReward(self, arg0): pass
    def onGetPlayerPayInfo(self, arg0, arg1, arg2): pass
    def onGetRaidAllMembersAttrs(self, arg0, arg1): pass
    def onGetRaidApplyJoinList(self, arg0, arg1): pass
    def onGetRaidData(self, arg0): pass
    def onGetRaidList(self, arg0, arg1, arg2): pass
    def onGetRedBagMyList(self, arg0): pass
    def onGetRedBagRankList(self, arg0): pass
    def onGetServerLevel(self, arg0): pass
    def onGetServerOpenTime(self, arg0): pass
    def onGetSpaceState(self, arg0): pass
    def onGetStoreLimitedItemList(self, arg0, arg1): pass
    def onGetStoreList(self, arg0): pass
    def onGetSynthesisUpgradeNum(self, arg0): pass
    def onGetTaskReward(self, arg0, arg1): pass
    def onGetTeamInfo(self, arg0): pass
    def onGetTeamList(self, arg0, arg1, arg2): pass
    def onGetVariableData(self, arg0, arg1): pass
    def onGetWelfareSignInInfo(self, arg0): pass
    def onGmCommandResult(self, arg0, arg1): pass
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
    def onInitAchieveData(self, arg0, arg1, arg2): pass
    def onInitEnemyRecord(self, arg0, arg1): pass
    def onInitEquipDropData(self, arg0): pass
    def onInteractStateChange(self, arg0): pass
    def onJoinRaid(self, arg0, arg1, arg2): pass
    def onJoinTeam(self, arg0, arg1, arg2): pass
    def onJunXuArchitectureChanged(self, arg0): pass
    def onKillAvatar(self, arg0): pass
    def onLeaderBoardAvatarLevel(self, arg0, arg1, arg2, arg3, arg4, arg5): pass
    def onLeaderBoardAvatarScore(self, arg0, arg1, arg2, arg3, arg4, arg5): pass
    def onLeaderBoardGuild(self, arg0, arg1, arg2, arg3, arg4): pass
    def onLeaveSingleDungeon(self, arg0): pass
    def onLeaveTeam(self): pass
    def onLeftFreeReliveTimesChanged(self, arg0): pass
    def onLeveUpMeridianPointTo(self, arg0, arg1, arg2): pass
    def onLockItemSucc(self, arg0, arg1, arg2, arg3): pass
    def onMessage(self, arg0, arg1): pass
    def onModifyNameResult(self, arg0, arg1): pass
    def onMultiAtkStage(self, arg0, arg1, arg2, arg3, arg4): pass
    def onMultiNumResourceChanged(self, arg0, arg1): pass
    def onNewApplyGuildUnion(self, arg0): pass
    def onNewBlazeId(self, arg0): pass
    def onNewEnemyRecord(self, arg0, arg1): pass
    def onNewGuildUnionApplySender(self, arg0): pass
    def onNewbieGuideId(self, arg0): pass
    def onNotifyApplyJoinInfo(self, arg0): pass
    def onNotiyNewAuctionCollection(self, arg0): pass
    def onNumResourceChanged(self, arg0, arg1): pass
    def onOfficialMessage(self, arg0, arg1, arg2, arg3, arg4): pass
    def onOthersSkillDamage(self, arg0, arg1): pass
    def onOutfitExpired(self, arg0): pass
    def onPickNewEquipDrop(self, arg0): pass
    def onPlayerAutoMatch(self): pass
    def onPlayerCoinAuctionItemBeSaled(self, arg0, arg1, arg2): pass
    def onPlayerGetExp(self, arg0, arg1, arg2, arg3): pass
    def onPlayerStopAutoMatch(self): pass
    def onPopDialog(self, arg0): pass
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
    def onRaidStartAutoMatch(self, arg0): pass
    def onRaidStopAutoMatch(self): pass
    def onRandomSummonPet(self, arg0): pass
    def onRandomSynthesis(self, arg0): pass
    def onReadOneMail(self, arg0): pass
    def onRecordFightProps(self): pass
    def onRecvAuthRoleClient(self, arg0, arg1): pass
    def onRecvAvatarChannelMsg(self, arg0, arg1, arg2): pass
    def onRecvDuelReq(self, arg0, arg1): pass
    def onRecvTrumpetMsg(self, arg0, arg1, arg2): pass
    def onRedBagPlayerInfo(self, arg0, arg1): pass
    def onReleaseRedBagMsg(self, arg0, arg1, arg2, arg3, arg4, arg5): pass
    def onRelive(self): pass
    def onReliveByOthers(self, arg0): pass
    def onRemoveApplyGuildUnion(self, arg0): pass
    def onRemoveApplyedGuilds(self, arg0): pass
    def onRemoveAureole(self, arg0): pass
    def onRemoveAureoleFromOthers(self, arg0): pass
    def onRemoveBlocks(self, arg0): pass
    def onRemoveBuff(self, arg0, arg1): pass
    def onRemoveChallengeAvatar(self, arg0): pass
    def onRemoveCompletePetWitness(self, arg0): pass
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
    def onRemoveRune(self, arg0, arg1): pass
    def onRemoveStrangers(self, arg0): pass
    def onReplyBecomeCaptain(self, arg0, arg1): pass
    def onReplyFollowTeamCaptain(self, arg0, arg1): pass
    def onReplyInviteTeam(self, arg0): pass
    def onReplyRaidStandbyChecker(self, arg0, arg1): pass
    def onReplyRaidStandbyCheckerBeforeEnterDungeon(self, arg0, arg1, arg2): pass
    def onRideMount(self, arg0, arg1): pass
    def onRideMountCast(self): pass
    def onSaleItemInCoinAuction(self, arg0, arg1, arg2): pass
    def onSceneState(self, arg0): pass
    def onSearchCoinAuctionItemsByItemId(self, arg0, arg1, arg2, arg3, arg4): pass
    def onSearchFriends(self, arg0, arg1): pass
    def onSelfInteractStateChange(self, arg0, arg1): pass
    def onSellItemSucc(self, arg0, arg1, arg2, arg3): pass
    def onSendCommonFlagCellInfo(self, arg0): pass
    def onSendForbidChat(self, arg0, arg1): pass
    def onSendForbidVoiceChat(self, arg0, arg1): pass
    def onSendHolidayPayInfo(self, arg0): pass
    def onSendLevelRewardInfo(self, arg0): pass
    def onSendRequiredVersion(self, arg0): pass
    def onSendtoRandomLineAndArea(self, arg0, arg1, arg2, arg3, arg4): pass
    def onServerUseSkill(self, arg0): pass
    def onSetAddSkillCd(self, arg0, arg1, arg2, arg3, arg4, arg5, arg6): pass
    def onSetChatCD(self, arg0, arg1): pass
    def onSetChiefDungeonAutoConfirmConfig(self, arg0): pass
    def onSetCrusadeDungeonAutoConfirmConfig(self, arg0): pass
    def onSetInstantPotionSlots(self, arg0): pass
    def onSetRaidDeputy(self, arg0, arg1): pass
    def onSetRaidDungeonInfo(self, arg0, arg1): pass
    def onSetRaidLeader(self, arg0, arg1): pass
    def onSetRaidTarget(self, arg0, arg1, arg2, arg3, arg4, arg5, arg6): pass
    def onSetRaidTeamCaptain(self, arg0, arg1, arg2): pass
    def onSetTeamTarget(self, arg0, arg1, arg2, arg3, arg4, arg5, arg6): pass
    def onShooterSkillCanUse(self, arg0, arg1, arg2): pass
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
    def onSkillTeleport(self, arg0, arg1): pass
    def onStartAutoCombat(self): pass
    def onStartPlayCinema(self, arg0): pass
    def onStopAutoCombat(self): pass
    def onSwitchRaidMicsMode(self, arg0, arg1, arg2, arg3): pass
    def onSwitchTeamMicsMode(self, arg0, arg1, arg2, arg3): pass
    def onSyncAllRaidMemberMiscStatus(self, arg0, arg1, arg2, arg3): pass
    def onSyncAllTeamMemberMiscStatus(self, arg0, arg1, arg2, arg3): pass
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
    def onTeleport(self): pass
    def onTeleportCasting(self, arg0, arg1): pass
    def onTeleportDone(self, arg0, arg1): pass
    def onTeleportFail(self): pass
    def onTryBeInvitedInRaid(self, arg0, arg1, arg2, arg3): pass
    def onTurnOffRaidMemberMics(self, arg0, arg1, arg2, arg3, arg4): pass
    def onTurnOffTeamMemberMics(self, arg0, arg1, arg2, arg3): pass
    def onTurnOnRaidMemberMics(self, arg0, arg1, arg2, arg3): pass
    def onTurnOnTeamMemberMics(self, arg0, arg1, arg2): pass
    def onUnblockAllRaidMemberMics(self, arg0, arg1): pass
    def onUnblockAllTeamMemberMics(self, arg0, arg1): pass
    def onUnblockRaidMemberMisc(self, arg0, arg1, arg2): pass
    def onUnblockTeamMemberMisc(self, arg0, arg1): pass
    def onUndressEquipment(self, arg0): pass
    def onUnlockGrids(self, arg0, arg1): pass
    def onUnlockSkills(self, arg0): pass
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
    def onUpdateLingShouScore(self, arg0, arg1): pass
    def onUpdateMemberAttr(self, arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7): pass
    def onUpdateOutfitData(self, arg0): pass
    def onUpdatePetBattleListName(self, arg0, arg1): pass
    def onUpdateRaidMemberHP(self, arg0, arg1, arg2): pass
    def onUpdateRaidMemberLevel(self, arg0, arg1): pass
    def onUpdateRaidMemberPos(self, arg0, arg1, arg2): pass
    def onUpdateRaidMemberScore(self, arg0, arg1): pass
    def onUpdateRecentData(self, arg0): pass
    def onUpdateSkillBuildInfo(self, arg0): pass
    def onUpdateSkillLevel(self, arg0, arg1): pass
    def onUpdateSkills(self, arg0): pass
    def onUpdateStandbyCheckData(self, arg0, arg1, arg2): pass
    def onUpdateStrangerData(self, arg0): pass
    def onUpdateSynthesisUpgradeNum(self, arg0): pass
    def onUpdateTeamMembeSex(self, arg0, arg1): pass
    def onUpdateTeamMemberHp(self, arg0, arg1, arg2): pass
    def onUpdateTeamMemberPos(self, arg0, arg1, arg2): pass
    def onUpdateTeamMemberScore(self, arg0, arg1): pass
    def onUpgradeSynthesis(self, arg0): pass
    def onUseCasting(self, arg0, arg1, arg2, arg3, arg4): pass
    def onUseChanneling(self, arg0, arg1, arg2, arg3, arg4, arg5): pass
    def onUseItemWithAnimation(self, arg0): pass
    def onUseMapCasting(self): pass
    def onUseSkill(self, arg0, arg1, arg2, arg3, arg4): pass
    def onUseStageSkill(self, arg0, arg1, arg2): pass
    def onVariableChanged(self, arg0, arg1): pass
    def onWarehouseInItems(self, arg0, arg1): pass
    def onWarehouseLockItemSucc(self, arg0, arg1, arg2): pass
    def onWarehouseOutItems(self, arg0, arg1): pass
    def onWonderLandBossInfo(self, arg0): pass
    def onWonderLandLeftTime(self, arg0): pass
    def onWonderLandLoginData(self, arg0, arg1, arg2, arg3): pass
    def onWonderLandSwitch(self, arg0, arg1): pass
    def onWorkshopMF(self, arg0, arg1, arg2, arg3): pass
    def onYuxiFlagChange(self, arg0): pass
    def popDialog(self, arg0): pass
    def popDialogWithSelfHead(self, arg0): pass
    def qureyAddTeamCaptainFriend(self, arg0): pass
    def raidEnterDungeonStandbyCheckNotify(self, arg0, arg1, arg2, arg3): pass
    def raidStandbyCheckNotify(self, arg0, arg1): pass
    def recvGetGuildDetailInfo(self, arg0): pass
    def revertSelfCameraStatus(self): pass
    def selfGuildNameChanged(self, arg0, arg1): pass
    def sendAllSkills(self, arg0): pass
    def sendEnemyPosInfoToClient(self, arg0, arg1, arg2): pass
    def sendPickedCollectoins(self, arg0, arg1): pass
    def sendSkillBuilds(self, arg0): pass
    def sendTeamStatisticData(self, arg0): pass
    def showCombatMsg(self, arg0, arg1): pass
    def showPopoverMsg(self, arg0): pass
    def showPopoverMsgWithArg(self, arg0, arg1): pass
    def skillTeleportBefore(self, arg0): pass
    def startCreateEquipTeam(self): pass
    def startCreateRandomTeam(self): pass
    def startLeaveTeam(self): pass
    def startTeleport(self, arg0, arg1): pass
    def stopOfficialMessage(self, arg0): pass
    def switchBuildChangeSkills(self, arg0): pass
    def syncGuildTaskInfo(self, arg0): pass
    def syncServerTime(self, arg0, arg1): pass
    def teleportCastingPreNotify(self, arg0, arg1): pass
    def triggerNewbieGuide(self, arg0): pass
    def updateSkillsExtraLevel(self, arg0, arg1, arg2): pass
