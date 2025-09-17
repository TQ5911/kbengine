# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: guild/guildConst
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "initGuildMemberLimit": _tools.RODict({
        "key": "initGuildMemberLimit",
        "value": 50,
    }),
    "maxGuildLevel": _tools.RODict({
        "key": "maxGuildLevel",
        "value": 30,
    }),
    "guildEstablishCost": _tools.RODict({
        "key": "guildEstablishCost",
        "value": ((30000001, 100), (30000236, 1)),
    }),
    "guildNameMinLength": _tools.RODict({
        "key": "guildNameMinLength",
        "value": 2,
    }),
    "guildNameMaxLength": _tools.RODict({
        "key": "guildNameMaxLength",
        "value": 7,
    }),
    "guildCreedMaxLength": _tools.RODict({
        "key": "guildCreedMaxLength",
        "value": 45,
    }),
    "guildApplyCountLimit": _tools.RODict({
        "key": "guildApplyCountLimit",
        "value": 50,
    }),
    "guildUnionCountLimit": _tools.RODict({
        "key": "guildUnionCountLimit",
        "value": 50,
    }),
    "guildRenameItemID": _tools.RODict({
        "key": "guildRenameItemID",
        "value": 30000238,
    }),
    "guildRenameCooldown": _tools.RODict({
        "key": "guildRenameCooldown",
        "value": 1,
    }),
    "guildCreateLevelRequire": _tools.RODict({
        "key": "guildCreateLevelRequire",
        "value": 17,
    }),
    "guildJoinLevelRequire": _tools.RODict({
        "key": "guildJoinLevelRequire",
        "value": 17,
    }),
    "guildMoneyToCoinRatio": _tools.RODict({
        "key": "guildMoneyToCoinRatio",
        "value": 100,
    }),
    "guild_coinLimitCantConvert_msg": _tools.RODict({
        "key": "guild_coinLimitCantConvert_msg",
        "value": 54000541,
    }),
    "InactiveDaysForGuildDisband": _tools.RODict({
        "key": "InactiveDaysForGuildDisband",
        "value": 30,
    }),
    "creatGuildMailId": _tools.RODict({
        "key": "creatGuildMailId",
        "value": 37000007,
    }),
    "JoinGuildMailId": _tools.RODict({
        "key": "JoinGuildMailId",
        "value": 37000004,
    }),
    "guildDisbandMailId": _tools.RODict({
        "key": "guildDisbandMailId",
        "value": 37000005,
    }),
    "guildKickMail": _tools.RODict({
        "key": "guildKickMail",
        "value": 37000006,
    }),
    "buildExpPerAssist": _tools.RODict({
        "key": "buildExpPerAssist",
        "value": 10,
    }),
    "maxAssistTimes": _tools.RODict({
        "key": "maxAssistTimes",
        "value": 24,
    }),
    "assistTimesRecIntvl": _tools.RODict({
        "key": "assistTimesRecIntvl",
        "value": 1800,
    }),
    "guildInviteCooldown": _tools.RODict({
        "key": "guildInviteCooldown",
        "value": 10,
    }),
    "guildRefusedInviteCooldown": _tools.RODict({
        "key": "guildRefusedInviteCooldown",
        "value": 300,
    }),
    "guildInviteCooldownMsg": _tools.RODict({
        "key": "guildInviteCooldownMsg",
        "value": 54000489,
    }),
    "guildSwitchCooldown": _tools.RODict({
        "key": "guildSwitchCooldown",
        "value": 2,
    }),
    "guildAutoApplyNum": _tools.RODict({
        "key": "guildAutoApplyNum",
        "value": 15,
    }),
    "guildTrainMaxLevel": _tools.RODict({
        "key": "guildTrainMaxLevel",
        "value": 60,
    }),
    "guildTitleId": _tools.RODict({
        "key": "guildTitleId",
        "value": 25000007,
    }),
    "guildEmblemId": _tools.RODict({
        "key": "guildEmblemId",
        "value": (0, 1),
    }),
    "guildJoinScoreLimit": _tools.RODict({
        "key": "guildJoinScoreLimit",
        "value": 999999,
    }),
    "guildTrain_levelUp_msg": _tools.RODict({
        "key": "guildTrain_levelUp_msg",
        "value": 54000255,
    }),
    "guildTrain_buildLevelLimited_msg": _tools.RODict({
        "key": "guildTrain_buildLevelLimited_msg",
        "value": 54000256,
    }),
    "guildTrain_lowRoleLevel_msg": _tools.RODict({
        "key": "guildTrain_lowRoleLevel_msg",
        "value": 54000257,
    }),
    "guildTrainResetFail_notTrained_msg": _tools.RODict({
        "key": "guildTrainResetFail_notTrained_msg",
        "value": 54000258,
    }),
    "guildTrainReset_check": _tools.RODict({
        "key": "guildTrainReset_check",
        "value": 54000259,
    }),
    "guildTrainResetFee": _tools.RODict({
        "key": "guildTrainResetFee",
        "value": (30000001, 100),
    }),
    "guildTrainResetFeeText": _tools.RODict({
        "key": "guildTrainResetFeeText",
        "value": "消耗{0}{1}",
    }),
    "guildAssistCost": _tools.RODict({
        "key": "guildAssistCost",
        "value": (30000002, 400),
    }),
    "guildAssistRewardID": _tools.RODict({
        "key": "guildAssistRewardID",
        "value": 40000019,
    }),
    "guildDonateCoinCopper": _tools.RODict({
        "key": "guildDonateCoinCopper",
        "value": 100,
    }),
    "guildDonateCoinToGuildCoin": _tools.RODict({
        "key": "guildDonateCoinToGuildCoin",
        "value": 1,
    }),
    "guildDonateCoinRewardID": _tools.RODict({
        "key": "guildDonateCoinRewardID",
        "value": 40000018,
    }),
    "guildDonateMoneyCopper": _tools.RODict({
        "key": "guildDonateMoneyCopper",
        "value": 1,
    }),
    "guildDonateMoneyToGuildMoney": _tools.RODict({
        "key": "guildDonateMoneyToGuildMoney",
        "value": 1,
    }),
    "guildDonateMoneyRewardID": _tools.RODict({
        "key": "guildDonateMoneyRewardID",
        "value": 40000020,
    }),
    "guildDonateTokenCopper": _tools.RODict({
        "key": "guildDonateTokenCopper",
        "value": 1,
    }),
    "guildDonateTokenToGuildMoney": _tools.RODict({
        "key": "guildDonateTokenToGuildMoney",
        "value": 1,
    }),
    "guildDonateTokenRewardID": _tools.RODict({
        "key": "guildDonateTokenRewardID",
        "value": 40000020,
    }),
    "guildTrainTypeName": _tools.RODict({
        "key": "guildTrainTypeName",
        "value": ('基础修炼', '攻击修炼', '防御修炼'),
    }),
    "guild_establishFail_inGuild_msg": _tools.RODict({
        "key": "guild_establishFail_inGuild_msg",
        "value": 54000490,
    }),
    "guildApply_applySent_msg": _tools.RODict({
        "key": "guildApply_applySent_msg",
        "value": 54000491,
    }),
    "guild_createCheck_check": _tools.RODict({
        "key": "guild_createCheck_check",
        "value": 54000492,
    }),
    "guild_notAuthorized_msg": _tools.RODict({
        "key": "guild_notAuthorized_msg",
        "value": 54000493,
    }),
    "guild_establishLevelLine_msg": _tools.RODict({
        "key": "guild_establishLevelLine_msg",
        "value": 54000494,
    }),
    "guild_blankGuildName_msg": _tools.RODict({
        "key": "guild_blankGuildName_msg",
        "value": 54000495,
    }),
    "guild_guildNameCountError_msg": _tools.RODict({
        "key": "guild_guildNameCountError_msg",
        "value": 54000496,
    }),
    "guild_guildNameOccupied_msg": _tools.RODict({
        "key": "guild_guildNameOccupied_msg",
        "value": 54000497,
    }),
    "guildApply_sentRedundant_msg": _tools.RODict({
        "key": "guildApply_sentRedundant_msg",
        "value": 54000498,
    }),
    "guild_selectNeeded_msg": _tools.RODict({
        "key": "guild_selectNeeded_msg",
        "value": 54000499,
    }),
    "guildApply_playerInOtherGuild_msg": _tools.RODict({
        "key": "guildApply_playerInOtherGuild_msg",
        "value": 54000500,
    }),
    "guildApply_guildFull_msg": _tools.RODict({
        "key": "guildApply_guildFull_msg",
        "value": 54000501,
    }),
    "guildApply_applyAccept_msg": _tools.RODict({
        "key": "guildApply_applyAccept_msg",
        "value": 54000502,
    }),
    "guild_established_msg": _tools.RODict({
        "key": "guild_established_msg",
        "value": 54000503,
    }),
    "guildAuth_appointment_msg": _tools.RODict({
        "key": "guildAuth_appointment_msg",
        "value": 54000504,
    }),
    "guildAuth_dismiss_msg": _tools.RODict({
        "key": "guildAuth_dismiss_msg",
        "value": 54000505,
    }),
    "guild_levelUp_msg": _tools.RODict({
        "key": "guild_levelUp_msg",
        "value": 54000506,
    }),
    "guildAuth_appointed_msg": _tools.RODict({
        "key": "guildAuth_appointed_msg",
        "value": 54000508,
    }),
    "guildAuth_dismissed_msg": _tools.RODict({
        "key": "guildAuth_dismissed_msg",
        "value": 54000509,
    }),
    "guildAuth_positionFull_msg": _tools.RODict({
        "key": "guildAuth_positionFull_msg",
        "value": 54000510,
    }),
    "guildAuth_samePosition_msg": _tools.RODict({
        "key": "guildAuth_samePosition_msg",
        "value": 54000511,
    }),
    "guild_kickMemberCheck_check": _tools.RODict({
        "key": "guild_kickMemberCheck_check",
        "value": 54000512,
    }),
    "guild_kicked_msg": _tools.RODict({
        "key": "guild_kicked_msg",
        "value": 54000513,
    }),
    "guild_presidentLeave_msg": _tools.RODict({
        "key": "guild_presidentLeave_msg",
        "value": 54000514,
    }),
    "guild_memberLeaveCheck_check": _tools.RODict({
        "key": "guild_memberLeaveCheck_check",
        "value": 54000515,
    }),
    "guild_memberLeaveNotice_msg": _tools.RODict({
        "key": "guild_memberLeaveNotice_msg",
        "value": 54000516,
    }),
    "guild_presidentLeaveCheck_msg": _tools.RODict({
        "key": "guild_presidentLeaveCheck_msg",
        "value": 54000520,
    }),
    "guild_memberFull_msg": _tools.RODict({
        "key": "guild_memberFull_msg",
        "value": 54000523,
    }),
    "guild_guildRenamed_msg": _tools.RODict({
        "key": "guild_guildRenamed_msg",
        "value": 54000530,
    }),
    "guild_renameCooldown_msg": _tools.RODict({
        "key": "guild_renameCooldown_msg",
        "value": 54000830,
    }),
    "guild_guildCreedRevised_msg": _tools.RODict({
        "key": "guild_guildCreedRevised_msg",
        "value": 54000531,
    }),
    "guild_authEditSaved_msg": _tools.RODict({
        "key": "guild_authEditSaved_msg",
        "value": 54000536,
    }),
    "guild_leftGuild_msg": _tools.RODict({
        "key": "guild_leftGuild_msg",
        "value": 54000538,
    }),
    "guild_failApplyFull_msg": _tools.RODict({
        "key": "guild_failApplyFull_msg",
        "value": 54000562,
    }),
    "guild_failUnionFull_msg": _tools.RODict({
        "key": "guild_failUnionFull_msg",
        "value": 54000563,
    }),
    "guild_inviteFail_inGuild_msg": _tools.RODict({
        "key": "guild_inviteFail_inGuild_msg",
        "value": 54000571,
    }),
    "guild_inviteCheck_check": _tools.RODict({
        "key": "guild_inviteCheck_check",
        "value": 54000572,
    }),
    "guild_estFail_levelNotEnough_msg": _tools.RODict({
        "key": "guild_estFail_levelNotEnough_msg",
        "value": 54000575,
    }),
    "guild_applyFail_levelNotEnough_msg": _tools.RODict({
        "key": "guild_applyFail_levelNotEnough_msg",
        "value": 54000576,
    }),
    "guild_quitCheck_check": _tools.RODict({
        "key": "guild_quitCheck_check",
        "value": 54000577,
    }),
    "guild_presidentAppointCheck_check": _tools.RODict({
        "key": "guild_presidentAppointCheck_check",
        "value": 54000578,
    }),
    "guildTrain_notInGuild_msg": _tools.RODict({
        "key": "guildTrain_notInGuild_msg",
        "value": 54000598,
    }),
    "guild_inviteFail_offline_msg": _tools.RODict({
        "key": "guild_inviteFail_offline_msg",
        "value": 54000606,
    }),
    "guild_switchCoolingDown_msg": _tools.RODict({
        "key": "guild_switchCoolingDown_msg",
        "value": 54000613,
    }),
    "guildTrain_unlockCondition_text": _tools.RODict({
        "key": "guildTrain_unlockCondition_text",
        "value": 54000619,
    }),
    "guildTrain_levelCurrentMax_text": _tools.RODict({
        "key": "guildTrain_levelCurrentMax_text",
        "value": 54000620,
    }),
    "guildTrain_levelMax_text": _tools.RODict({
        "key": "guildTrain_levelMax_text",
        "value": 54000621,
    }),
    "guildApply_conditionNotFit_msg": _tools.RODict({
        "key": "guildApply_conditionNotFit_msg",
        "value": 54000835,
    }),
    "guild_settingSaved_msg": _tools.RODict({
        "key": "guild_settingSaved_msg",
        "value": 54000880,
    }),
    "guild_settingUnchange_msg": _tools.RODict({
        "key": "guild_settingUnchange_msg",
        "value": 54000881,
    }),
    "guild_autoApplyNoFitGuild_msg": _tools.RODict({
        "key": "guild_autoApplyNoFitGuild_msg",
        "value": 54000898,
    }),
    "guild_join_msg": _tools.RODict({
        "key": "guild_join_msg",
        "value": 54000901,
    }),
    "guild_kickOfficer_msg": _tools.RODict({
        "key": "guild_kickOfficer_msg",
        "value": 54001077,
    }),
    "guildApply_guildDismissed_msg": _tools.RODict({
        "key": "guildApply_guildDismissed_msg",
        "value": 54001096,
    }),
    "guildTrainNotOpen_text": _tools.RODict({
        "key": "guildTrainNotOpen_text",
        "value": 54001200,
    }),
    "authNotChanged_msg": _tools.RODict({
        "key": "authNotChanged_msg",
        "value": 54000820,
    }),
    "guildOfficialResignCheck": _tools.RODict({
        "key": "guildOfficialResignCheck",
        "value": 54001441,
    }),
    "guildOfficialLeavingGuildMsg": _tools.RODict({
        "key": "guildOfficialLeavingGuildMsg",
        "value": 54001445,
    }),
    "guildApplyFail_inGuild_msg": _tools.RODict({
        "key": "guildApplyFail_inGuild_msg",
        "value": 54001446,
    }),
    "guildRenameFail_notGuildLeader_msg": _tools.RODict({
        "key": "guildRenameFail_notGuildLeader_msg",
        "value": 54001581,
    }),
    "guildRenameFail_notInGuild_msg": _tools.RODict({
        "key": "guildRenameFail_notInGuild_msg",
        "value": 54000598,
    }),
    "guildRenameCheck": _tools.RODict({
        "key": "guildRenameCheck",
        "value": 54001590,
    }),
    "guild_dissolved_msg": _tools.RODict({
        "key": "guild_dissolved_msg",
        "value": 54001713,
    }),
    "guildRecruitChatMsg": _tools.RODict({
        "key": "guildRecruitChatMsg",
        "value": 58000008,
    }),
    "guildRecruitChatSent": _tools.RODict({
        "key": "guildRecruitChatSent",
        "value": 54001773,
    }),
    "guildRecruitChatCooldown": _tools.RODict({
        "key": "guildRecruitChatCooldown",
        "value": 54001774,
    }),
    "guildRecruitBoradcastCooldown": _tools.RODict({
        "key": "guildRecruitBoradcastCooldown",
        "value": 120,
    }),
    "guild_officialResigned_chatMsg": _tools.RODict({
        "key": "guild_officialResigned_chatMsg",
        "value": 58000009,
    }),
    "guild_offcialAppointed_chatMsg": _tools.RODict({
        "key": "guild_offcialAppointed_chatMsg",
        "value": 58000010,
    }),
    "guild_offcialFired_chatMsg": _tools.RODict({
        "key": "guild_offcialFired_chatMsg",
        "value": 58000011,
    }),
    "guild_presidentTransferred_chatMsg": _tools.RODict({
        "key": "guild_presidentTransferred_chatMsg",
        "value": 58000012,
    }),
    "guild_join_chatMsg": _tools.RODict({
        "key": "guild_join_chatMsg",
        "value": 58000013,
    }),
    "guild_coreBuildingLvNotEnough_msg": _tools.RODict({
        "key": "guild_coreBuildingLvNotEnough_msg",
        "value": 54000831,
    }),
    "coreBuildingUpgradeCondText": _tools.RODict({
        "key": "coreBuildingUpgradeCondText",
        "value": "帮会等级达到{0}级",
    }),
    "nonCoreBuildingUpgradeCondText": _tools.RODict({
        "key": "nonCoreBuildingUpgradeCondText",
        "value": "聚义楼等级达到{0}级",
    }),
    "guild_noAssistTimes_msg": _tools.RODict({
        "key": "guild_noAssistTimes_msg",
        "value": 54000518,
    }),
    "coreBuildingCntUpgrade_msg": _tools.RODict({
        "key": "coreBuildingCntUpgrade_msg",
        "value": 54000532,
    }),
    "nonCoreBuildingCntUpgrade_msg": _tools.RODict({
        "key": "nonCoreBuildingCntUpgrade_msg",
        "value": 54000533,
    }),
    "guild_applySentLimit_msg": _tools.RODict({
        "key": "guild_applySentLimit_msg",
        "value": 54000534,
    }),
    "guild_guildCoinLimit_msg": _tools.RODict({
        "key": "guild_guildCoinLimit_msg",
        "value": 54000535,
    }),
    "guild_guildMoneyLimit_msg": _tools.RODict({
        "key": "guild_guildMoneyLimit_msg",
        "value": 54000537,
    }),
    "guild_guildTokenLimit_msg": _tools.RODict({
        "key": "guild_guildTokenLimit_msg",
        "value": 54000542,
    }),
    "guildTrain_yanWuGeLvNotEnough": _tools.RODict({
        "key": "guildTrain_yanWuGeLvNotEnough",
        "value": "演武场等级达到{0}级",
    }),
    "guildTrain_selfLvNotEnough": _tools.RODict({
        "key": "guildTrain_selfLvNotEnough",
        "value": "角色等级达到{0}级",
    }),
    "guild_dailyCoinLimit_msg": _tools.RODict({
        "key": "guild_dailyCoinLimit_msg",
        "value": 54000539,
    }),
    "guild_dailyMoneyLimit_msg": _tools.RODict({
        "key": "guild_dailyMoneyLimit_msg",
        "value": 54000540,
    }),
    "guildTrain_wuHuaGeLvNotEnough": _tools.RODict({
        "key": "guildTrain_wuHuaGeLvNotEnough",
        "value": "百宝阁等级达到{0}级",
    }),
    "guild_buildUpgraded_msg": _tools.RODict({
        "key": "guild_buildUpgraded_msg",
        "value": 58000014,
    }),
    "guild_unionNum": _tools.RODict({
        "key": "guild_unionNum",
        "value": 20,
    }),
    "guild_unionApplicationNum": _tools.RODict({
        "key": "guild_unionApplicationNum",
        "value": 50,
    }),
    "guild_unionDesc": _tools.RODict({
        "key": "guild_unionDesc",
        "value": "我帮与帮会{0}结为同盟",
    }),
    "guild_relieveUnionDes": _tools.RODict({
        "key": "guild_relieveUnionDes",
        "value": "我帮与帮会{0}解除同盟",
    }),
    "guild_enmityDesc1": _tools.RODict({
        "key": "guild_enmityDesc1",
        "value": "我帮向帮会{0}宣战",
    }),
    "guild_enmityDesc2": _tools.RODict({
        "key": "guild_enmityDesc2",
        "value": "{0}帮会向我帮宣战",
    }),
    "guild_unionNumDesc": _tools.RODict({
        "key": "guild_unionNumDesc",
        "value": "结盟帮会：{0}/{1}",
    }),
    "guild_commissariatLevel": _tools.RODict({
        "key": "guild_commissariatLevel",
        "value": "军需处等级达到{0}级",
    }),
    "guild_enmityCost": _tools.RODict({
        "key": "guild_enmityCost",
        "value": (30000007, 50000),
    }),
    "guild_relieveUnion": _tools.RODict({
        "key": "guild_relieveUnion",
        "value": 54003058,
    }),
    "guild_enmityConfirm": _tools.RODict({
        "key": "guild_enmityConfirm",
        "value": 54003059,
    }),
    "guild_crossServerJoin": _tools.RODict({
        "key": "guild_crossServerJoin",
        "value": 54003060,
    }),
    "guild_unionNumDes": _tools.RODict({
        "key": "guild_unionNumDes",
        "value": 54003061,
    }),
    "guild_enmityNumDes": _tools.RODict({
        "key": "guild_enmityNumDes",
        "value": 54003062,
    }),
    "guild_enmityFail": _tools.RODict({
        "key": "guild_enmityFail",
        "value": 54003063,
    }),
    "guild_enmityAlready": _tools.RODict({
        "key": "guild_enmityAlready",
        "value": 54003064,
    }),
    "guild_unionApplicationDes": _tools.RODict({
        "key": "guild_unionApplicationDes",
        "value": 54003069,
    }),
    "guild_unionApplicationDes2": _tools.RODict({
        "key": "guild_unionApplicationDes2",
        "value": 54003070,
    }),
    "guild_unionAppliedFor": _tools.RODict({
        "key": "guild_unionAppliedFor",
        "value": 54003074,
    }),
    "guild_dismissed": _tools.RODict({
        "key": "guild_dismissed",
        "value": 54003075,
    }),
    "guild_pkPrompt": _tools.RODict({
        "key": "guild_pkPrompt",
        "value": 58000033,
    }),
    "guild_pkPrompt2": _tools.RODict({
        "key": "guild_pkPrompt2",
        "value": 58000034,
    }),
    "guild_unionPrompt": _tools.RODict({
        "key": "guild_unionPrompt",
        "value": 54003076,
    }),
    "guild_alreadyEnmity": _tools.RODict({
        "key": "guild_alreadyEnmity",
        "value": 54003077,
    }),
    "guild_noCompletedTask": _tools.RODict({
        "key": "guild_noCompletedTask",
        "value": 54003081,
    }),
    "guild_noJoinGuild": _tools.RODict({
        "key": "guild_noJoinGuild",
        "value": 54003089,
    }),
    "guild_dailyTokenLimit": _tools.RODict({
        "key": "guild_dailyTokenLimit",
        "value": 54003103,
    }),
    "guild_commissariatLevelNotEnough": _tools.RODict({
        "key": "guild_commissariatLevelNotEnough",
        "value": 54000543,
    }),
    "equipmentMaxAssistTimes": _tools.RODict({
        "key": "equipmentMaxAssistTimes",
        "value": 24,
    }),
    "equipmentAssistTimesRecIntvl": _tools.RODict({
        "key": "equipmentAssistTimesRecIntvl",
        "value": 3600,
    }),
    "equipmentAssistRewardID": _tools.RODict({
        "key": "equipmentAssistRewardID",
        "value": 40000019,
    }),
    "guildCityBattleTokenID": _tools.RODict({
        "key": "guildCityBattleTokenID",
        "value": 30000014,
    }),
    "cityBattleTokenID": _tools.RODict({
        "key": "cityBattleTokenID",
        "value": 30000310,
    }),
    "guild_warEquipmentAssets": _tools.RODict({
        "key": "guild_warEquipmentAssets",
        "value": ('Assets/Res/ui/texturenp/guild/guild_department01_bg_img.png', 'Assets/Res/ui/texturenp/guild/guild_department02_bg_img.png', 'Assets/Res/ui/texturenp/guild/guild_department03_bg_img.png', 'Assets/Res/ui/texturenp/guild/guild_department05_bg_img.png', 'Assets/Res/ui/texturenp/guild/guild_department04_bg_img.png'),
    }),
    "guild_warEquipmentName": _tools.RODict({
        "key": "guild_warEquipmentName",
        "value": ('主城门', '副城门', '旗帜', '攻城兽', '守城弩'),
    }),
    "guild_unionApplicationTimeLimit": _tools.RODict({
        "key": "guild_unionApplicationTimeLimit",
        "value": 3,
    }),
    "guild_enmityTime": _tools.RODict({
        "key": "guild_enmityTime",
        "value": 21600,
    }),
    "guild_declareWar": _tools.RODict({
        "key": "guild_declareWar",
        "value": 58000032,
    }),
    "guild_guildLvNotEnough_msg": _tools.RODict({
        "key": "guild_guildLvNotEnough_msg",
        "value": 54990063,
    })
})