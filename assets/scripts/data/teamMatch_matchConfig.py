# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: teamMatch/matchConfig
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "maxMatchTime": _tools.RODict({
        "ID": "maxMatchTime",
        "value": 3600,
    }),
    "captainActiveTime": _tools.RODict({
        "ID": "captainActiveTime",
        "value": 180,
    }),
    "teamChannel_applyTeamMsg": _tools.RODict({
        "ID": "teamChannel_applyTeamMsg",
        "value": 58000028,
    }),
    "teamChannel_applyRaidMsg": _tools.RODict({
        "ID": "teamChannel_applyRaidMsg",
        "value": 58000029,
    }),
    "guildChannelCD": _tools.RODict({
        "ID": "guildChannelCD",
        "value": 60,
    }),
    "zhaomuChannelCD": _tools.RODict({
        "ID": "zhaomuChannelCD",
        "value": 30,
    }),
    "applyCaptionCountdown": _tools.RODict({
        "ID": "applyCaptionCountdown",
        "value": 6,
    }),
    "teamFollowBigworldDunMsg": _tools.RODict({
        "ID": "teamFollowBigworldDunMsg",
        "value": 54001284,
    }),
    "teamFollowCantAccessMsg": _tools.RODict({
        "ID": "teamFollowCantAccessMsg",
        "value": 54000197,
    }),
    "teamFollowCantAccessMsgCD": _tools.RODict({
        "ID": "teamFollowCantAccessMsgCD",
        "value": 10,
    }),
    "targetAgreeMsg": _tools.RODict({
        "ID": "targetAgreeMsg",
        "value": 54000100,
    }),
    "targetJoinMsg": _tools.RODict({
        "ID": "targetJoinMsg",
        "value": 54000101,
    }),
    "inTeamMsg": _tools.RODict({
        "ID": "inTeamMsg",
        "value": 54000102,
    }),
    "isAppliedMsg": _tools.RODict({
        "ID": "isAppliedMsg",
        "value": 54000103,
    }),
    "teamFullMsg": _tools.RODict({
        "ID": "teamFullMsg",
        "value": 54000104,
    }),
    "applyFullMsg": _tools.RODict({
        "ID": "applyFullMsg",
        "value": 54000105,
    }),
    "applySentMsg": _tools.RODict({
        "ID": "applySentMsg",
        "value": 54000106,
    }),
    "targetInOtherTeamMsg": _tools.RODict({
        "ID": "targetInOtherTeamMsg",
        "value": 54000107,
    }),
    "inviteToTeamMsg": _tools.RODict({
        "ID": "inviteToTeamMsg",
        "value": 54000109,
    }),
    "inviteSentMsg": _tools.RODict({
        "ID": "inviteSentMsg",
        "value": 54000110,
    }),
    "inviteDeniedMsg": _tools.RODict({
        "ID": "inviteDeniedMsg",
        "value": 54000111,
    }),
    "teamDisbandMsg": _tools.RODict({
        "ID": "teamDisbandMsg",
        "value": 54000112,
    }),
    "enterTheTeamMsg": _tools.RODict({
        "ID": "enterTheTeamMsg",
        "value": 54000125,
    }),
    "tianyan_targfetOffLine": _tools.RODict({
        "ID": "tianyan_targfetOffLine",
        "value": 54000124,
    }),
    "applyCaptainMsg": _tools.RODict({
        "ID": "applyCaptainMsg",
        "value": 54000113,
    }),
    "beCaptainMsg": _tools.RODict({
        "ID": "beCaptainMsg",
        "value": 54000114,
    }),
    "applyCaptainDeniedMsg": _tools.RODict({
        "ID": "applyCaptainDeniedMsg",
        "value": 54000115,
    }),
    "transferCaptainMsg": _tools.RODict({
        "ID": "transferCaptainMsg",
        "value": 54000117,
    }),
    "kickFromTeamMsg": _tools.RODict({
        "ID": "kickFromTeamMsg",
        "value": 54000118,
    }),
    "teamFollowMsg": _tools.RODict({
        "ID": "teamFollowMsg",
        "value": 54000126,
    }),
    "teamMatch_noGoalMsg": _tools.RODict({
        "ID": "teamMatch_noGoalMsg",
        "value": 54000579,
    }),
    "teamMatch_fullMsg": _tools.RODict({
        "ID": "teamMatch_fullMsg",
        "value": 54000580,
    }),
    "teamMatch_raidFullMsg": _tools.RODict({
        "ID": "teamMatch_raidFullMsg",
        "value": 54000087,
    }),
    "leaveMatch_timeOverMsg": _tools.RODict({
        "ID": "leaveMatch_timeOverMsg",
        "value": 54000582,
    }),
    "teamMatch_inTeamQuitMsg": _tools.RODict({
        "ID": "teamMatch_inTeamQuitMsg",
        "value": 54000603,
    }),
    "teamMatch_inRaidQuitMsg": _tools.RODict({
        "ID": "teamMatch_inRaidQuitMsg",
        "value": 54000604,
    }),
    "teamChannel_enterTeamMsg": _tools.RODict({
        "ID": "teamChannel_enterTeamMsg",
        "value": 58000018,
    }),
    "teamChannel_initiativeLeaveTeamMsg": _tools.RODict({
        "ID": "teamChannel_initiativeLeaveTeamMsg",
        "value": 58000019,
    }),
    "teamChannel_kickedMsg": _tools.RODict({
        "ID": "teamChannel_kickedMsg",
        "value": 58000020,
    }),
    "teamChannel_applyCaptainMsg": _tools.RODict({
        "ID": "teamChannel_applyCaptainMsg",
        "value": 58000021,
    }),
    "teamChannel_becomeCaptainMsg": _tools.RODict({
        "ID": "teamChannel_becomeCaptainMsg",
        "value": 58000022,
    }),
    "teamChannel_createTeamMsg": _tools.RODict({
        "ID": "teamChannel_createTeamMsg",
        "value": 58000060,
    }),
    "team_createTeamMsg": _tools.RODict({
        "ID": "team_createTeamMsg",
        "value": 54000155,
    }),
    "playerApplyTeamPopMsg": _tools.RODict({
        "ID": "playerApplyTeamPopMsg",
        "value": 54001126,
    }),
    "teamApplyGroupPopMsg": _tools.RODict({
        "ID": "teamApplyGroupPopMsg",
        "value": 54001128,
    }),
    "teamMinLevel": _tools.RODict({
        "ID": "teamMinLevel",
        "value": 1,
    }),
    "teamMinLevelMsg": _tools.RODict({
        "ID": "teamMinLevelMsg",
        "value": 54001336,
    }),
    "teamInviteScoreMsg": _tools.RODict({
        "ID": "teamInviteScoreMsg",
        "value": 54001471,
    }),
    "teamInviteLevelMsg": _tools.RODict({
        "ID": "teamInviteLevelMsg",
        "value": 54001472,
    }),
    "teamInviteQuestMsg": _tools.RODict({
        "ID": "teamInviteQuestMsg",
        "value": 54001473,
    }),
    "createTeamCD": _tools.RODict({
        "ID": "createTeamCD",
        "value": 3,
    }),
    "createTeamCDMsg": _tools.RODict({
        "ID": "createTeamCDMsg",
        "value": 54001620,
    }),
    "inviteCD": _tools.RODict({
        "ID": "inviteCD",
        "value": 5,
    }),
    "startAutomatch": _tools.RODict({
        "ID": "startAutomatch",
        "value": 54001789,
    }),
    "teamExperienceBonus": _tools.RODict({
        "ID": "teamExperienceBonus",
        "value": _tools.ROList([10, 20, 30, 40]),
    }),
    "zhaomuMessageCD": _tools.RODict({
        "ID": "zhaomuMessageCD",
        "value": 54000623,
    }),
    "recruitSent": _tools.RODict({
        "ID": "recruitSent",
        "value": 54000644,
    }),
    "zhaomuGuildSent": _tools.RODict({
        "ID": "zhaomuGuildSent",
        "value": 54000645,
    }),
    "zhaomuBattleFieldSent": _tools.RODict({
        "ID": "zhaomuBattleFieldSent",
        "value": 54000647,
    }),
    "assembleTeammatesCD": _tools.RODict({
        "ID": "assembleTeammatesCD",
        "value": 20,
    }),
    "goToTheCaptainCD": _tools.RODict({
        "ID": "goToTheCaptainCD",
        "value": 20,
    }),
    "leaveTheTeamConfirmation": _tools.RODict({
        "ID": "leaveTheTeamConfirmation",
        "value": 54001127,
    }),
    "insufficientConditions": _tools.RODict({
        "ID": "insufficientConditions",
        "value": 54001125,
    }),
    "recruitmentRefreshCd": _tools.RODict({
        "ID": "recruitmentRefreshCd",
        "value": 5,
    }),
    "maxNumberFb": _tools.RODict({
        "ID": "maxNumberFb",
        "value": 20,
    }),
    "maxNumberHh": _tools.RODict({
        "ID": "maxNumberHh",
        "value": 30,
    }),
    "captainSummonmsg": _tools.RODict({
        "ID": "captainSummonmsg",
        "value": 54000127,
    }),
    "teamMembersSummonmsg": _tools.RODict({
        "ID": "teamMembersSummonmsg",
        "value": 54000128,
    }),
    "cancelApplication": _tools.RODict({
        "ID": "cancelApplication",
        "value": 54000130,
    }),
    "teamMatchConfirm": _tools.RODict({
        "ID": "teamMatchConfirm",
        "value": 54000044,
    }),
    "team_notTeamLeader": _tools.RODict({
        "ID": "team_notTeamLeader",
        "value": 54000139,
    }),
    "team_scoreNotEnough": _tools.RODict({
        "ID": "team_scoreNotEnough",
        "value": 54000045,
    }),
    "teamMatchGuildActivityLeaveGuildMsg": _tools.RODict({
        "ID": "teamMatchGuildActivityLeaveGuildMsg",
        "value": 54001580,
    }),
    "targetInRaidMsg": _tools.RODict({
        "ID": "targetInRaidMsg",
        "value": 54000646,
    }),
    "raid_applicantOffline": _tools.RODict({
        "ID": "raid_applicantOffline",
        "value": 54000108,
    }),
    "teamMatch_needCancleMatchMsg": _tools.RODict({
        "ID": "teamMatch_needCancleMatchMsg",
        "value": 54000601,
    }),
    "teamMatch_needTeamMsg": _tools.RODict({
        "ID": "teamMatch_needTeamMsg",
        "value": 54000192,
    }),
    "teamMatch_needRaidMsg": _tools.RODict({
        "ID": "teamMatch_needRaidMsg",
        "value": 54000193,
    }),
    "leaveMatch_teamCapNotActiveMsg": _tools.RODict({
        "ID": "leaveMatch_teamCapNotActiveMsg",
        "value": 54000581,
    }),
    "leaveMatch_raidCapNotActiveMsg": _tools.RODict({
        "ID": "leaveMatch_raidCapNotActiveMsg",
        "value": 54000583,
    }),
    "leaveMatch_teamCapOfflineMsg": _tools.RODict({
        "ID": "leaveMatch_teamCapOfflineMsg",
        "value": 54000584,
    }),
    "leaveMatch_raidCapOfflineMsg": _tools.RODict({
        "ID": "leaveMatch_raidCapOfflineMsg",
        "value": 54000585,
    }),
    "leaveMatch_teamCapCancleMatchMsg": _tools.RODict({
        "ID": "leaveMatch_teamCapCancleMatchMsg",
        "value": 54000586,
    }),
    "leaveMatch_raidCapCancleMatchMsg": _tools.RODict({
        "ID": "leaveMatch_raidCapCancleMatchMsg",
        "value": 54000587,
    }),
    "team_TLDownGradeOfflineTime": _tools.RODict({
        "ID": "team_TLDownGradeOfflineTime",
        "value": 60,
    }),
    "leaveMatch_disbandConfirm": _tools.RODict({
        "ID": "leaveMatch_disbandConfirm",
        "value": 54000588,
    }),
    "teamMatch_TargetUnchanged": _tools.RODict({
        "ID": "teamMatch_TargetUnchanged",
        "value": 54001739,
    }),
    "team_TargetCondition": _tools.RODict({
        "ID": "team_TargetCondition",
        "value": 54001740,
    }),
    "team_inCopyScene": _tools.RODict({
        "ID": "team_inCopyScene",
        "value": 54001741,
    }),
    "team_lackCombatEffectiveness": _tools.RODict({
        "ID": "team_lackCombatEffectiveness",
        "value": 54001742,
    }),
    "team_unready": _tools.RODict({
        "ID": "team_unready",
        "value": 54001743,
    }),
    "team_lackChallengNums": _tools.RODict({
        "ID": "team_lackChallengNums",
        "value": 54001744,
    }),
    "team_leave": _tools.RODict({
        "ID": "team_leave",
        "value": 54000902,
    }),
    "teamSettingChange": _tools.RODict({
        "ID": "teamSettingChange",
        "value": 54000910,
    }),
    "onlyPublicTeamCanMatch": _tools.RODict({
        "ID": "onlyPublicTeamCanMatch",
        "value": 54000911,
    }),
    "teamMatch_differentFactions": _tools.RODict({
        "ID": "teamMatch_differentFactions",
        "value": 54003128,
    }),
    "in_dungeon_cant_operate": _tools.RODict({
        "ID": "in_dungeon_cant_operate",
        "value": 54000648,
    }),
    "raidTeamNotExist": _tools.RODict({
        "ID": "raidTeamNotExist",
        "value": 54000649,
    }),
    "raidTeamTitleDes": _tools.RODict({
        "ID": "raidTeamTitleDes",
        "value": "队伍招募中，欢迎加入！",
    }),
    "teamMatch_notFollow": _tools.RODict({
        "ID": "teamMatch_notFollow",
        "value": 54000650,
    }),
    "teamMatch_notConvene": _tools.RODict({
        "ID": "teamMatch_notConvene",
        "value": 54000651,
    }),
    "teamMatch_dataChange": _tools.RODict({
        "ID": "teamMatch_dataChange",
        "value": 54000652,
    }),
    "teamMatch_enterPassword": _tools.RODict({
        "ID": "teamMatch_enterPassword",
        "value": 54000653,
    }),
    "teamMatch_existingTeam": _tools.RODict({
        "ID": "teamMatch_existingTeam",
        "value": 54000654,
    }),
    "teamMatch_applicationFailed": _tools.RODict({
        "ID": "teamMatch_applicationFailed",
        "value": 54000655,
    }),
    "teamMatch_invitationFailed": _tools.RODict({
        "ID": "teamMatch_invitationFailed",
        "value": 54000656,
    }),
    "teamMatch_joinFailed": _tools.RODict({
        "ID": "teamMatch_joinFailed",
        "value": 54000657,
    }),
    "teamMatch_settlementInterval": _tools.RODict({
        "ID": "teamMatch_settlementInterval",
        "value": 3.5,
    }),
    "team_color_self": _tools.RODict({
        "ID": "team_color_self",
        "value": 57,
    }),
    "teamMatch_pwLen": _tools.RODict({
        "ID": "teamMatch_pwLen",
        "value": 4,
    }),
    "teamGoal_1": _tools.RODict({
        "ID": "teamGoal_1",
        "value": "巢穴副本",
    }),
    "teamGoal_2": _tools.RODict({
        "ID": "teamGoal_2",
        "value": "自设目标",
    }),
    "teamFullAutoStart": _tools.RODict({
        "ID": "teamFullAutoStart",
        "value": "满员自动开始挑战（同队伍仅首次挑战生效）",
    }),
    "copySettlementInterval": _tools.RODict({
        "ID": "copySettlementInterval",
        "value": 5,
    }),
    "needPassword": _tools.RODict({
        "ID": "needPassword",
        "value": "请输入密码",
    }),
    "errorPassword": _tools.RODict({
        "ID": "errorPassword",
        "value": "<color=red>密码错误</color>",
    }),
    "teamMatch_guildInvitation": _tools.RODict({
        "ID": "teamMatch_guildInvitation",
        "value": 54000630,
    }),
    "teamMatch_allInvitationSend": _tools.RODict({
        "ID": "teamMatch_allInvitationSend",
        "value": 54000631,
    }),
    "teamMatch_invitationCd": _tools.RODict({
        "ID": "teamMatch_invitationCd",
        "value": 54000632,
    }),
    "teamMatch_guildListEmpty": _tools.RODict({
        "ID": "teamMatch_guildListEmpty",
        "value": 54000635,
    }),
    "teamMatch_guildInvitationCd": _tools.RODict({
        "ID": "teamMatch_guildInvitationCd",
        "value": 60,
    }),
    "teamMatch_oneInvitationCd": _tools.RODict({
        "ID": "teamMatch_oneInvitationCd",
        "value": 10,
    }),
    "teamInviteMapMsg": _tools.RODict({
        "ID": "teamInviteMapMsg",
        "value": 54000634,
    }),
    "teammateChangeNameMsg": _tools.RODict({
        "ID": "teammateChangeNameMsg",
        "value": 54000636,
    }),
    "teamAnimFade": _tools.RODict({
        "ID": "teamAnimFade",
        "value": (0.1, 0.2, 18, 0.45, 30, 0.15, 3),
    }),
    "crossServerFollowMsg": _tools.RODict({
        "ID": "crossServerFollowMsg",
        "value": 54003520,
    }),
    "crossServerSummonMsg": _tools.RODict({
        "ID": "crossServerSummonMsg",
        "value": 54003521,
    })
})