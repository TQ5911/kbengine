# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: raid/raidConst
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "raidMemberLimit": _tools.RODict({
        "ID": "raidMemberLimit",
        "value": 15,
    }),
    "raidTeamLimit": _tools.RODict({
        "ID": "raidTeamLimit",
        "value": 3,
    }),
    "raidApplyLimit": _tools.RODict({
        "ID": "raidApplyLimit",
        "value": 50,
    }),
    "raidUnlcokLevel": _tools.RODict({
        "ID": "raidUnlcokLevel",
        "value": 10,
    }),
    "teamUIVisibleId": _tools.RODict({
        "ID": "teamUIVisibleId",
        "value": "Team",
    }),
    "raidUIVisibleId": _tools.RODict({
        "ID": "raidUIVisibleId",
        "value": "Raid",
    }),
    "teamDungeonUIVisibleId": _tools.RODict({
        "ID": "teamDungeonUIVisibleId",
        "value": "UITeamDunPanel",
    }),
    "raidDungeonUIVisibleId": _tools.RODict({
        "ID": "raidDungeonUIVisibleId",
        "value": "UICrusadeSystemPanel",
    }),
    "raidInvDeniedMsg": _tools.RODict({
        "ID": "raidInvDeniedMsg",
        "value": 54000111,
    }),
    "raidApplyDuration": _tools.RODict({
        "ID": "raidApplyDuration",
        "value": 10,
    }),
    "raidPressTime": _tools.RODict({
        "ID": "raidPressTime",
        "value": 1.0,
    }),
    "raid_applyFail_raidFull_msg": _tools.RODict({
        "ID": "raid_applyFail_raidFull_msg",
        "value": 54000608,
    }),
    "raid_applyAcceptFail_raidFull_msg": _tools.RODict({
        "ID": "raid_applyAcceptFail_raidFull_msg",
        "value": 54000609,
    }),
    "raid_invitationCheck_check": _tools.RODict({
        "ID": "raid_invitationCheck_check",
        "value": 54000616,
    }),
    "raid_joinFail_spaceless_msg": _tools.RODict({
        "ID": "raid_joinFail_spaceless_msg",
        "value": 54000618,
    }),
    "raid_kickCheck_check": _tools.RODict({
        "ID": "raid_kickCheck_check",
        "value": 54000719,
    }),
    "raid_kicked_msg": _tools.RODict({
        "ID": "raid_kicked_msg",
        "value": 54000720,
    }),
    "raid_kickDone_msg": _tools.RODict({
        "ID": "raid_kickDone_msg",
        "value": 54000721,
    }),
    "raid_appointCheckRL_check": _tools.RODict({
        "ID": "raid_appointCheckRL_check",
        "value": 54000722,
    }),
    "raid_appointedRL_msg": _tools.RODict({
        "ID": "raid_appointedRL_msg",
        "value": 54000723,
    }),
    "raid_appointRLDone_msg": _tools.RODict({
        "ID": "raid_appointRLDone_msg",
        "value": 54000724,
    }),
    "raid_appointedRDL_msg": _tools.RODict({
        "ID": "raid_appointedRDL_msg",
        "value": 54000780,
    }),
    "raid_appointRDLDone_msg": _tools.RODict({
        "ID": "raid_appointRDLDone_msg",
        "value": 54000781,
    }),
    "raid_applyCheckPL_check": _tools.RODict({
        "ID": "raid_applyCheckPL_check",
        "value": 54000728,
    }),
    "raidInviteFail_alreadyInRaid_msg": _tools.RODict({
        "ID": "raidInviteFail_alreadyInRaid_msg",
        "value": 54000763,
    }),
    "raidInviteFail_alreadyInTeam_msg": _tools.RODict({
        "ID": "raidInviteFail_alreadyInTeam_msg",
        "value": 54000764,
    }),
    "raid_join_msg": _tools.RODict({
        "ID": "raid_join_msg",
        "value": 54000776,
    }),
    "raid_leaveCheck_check": _tools.RODict({
        "ID": "raid_leaveCheck_check",
        "value": 54000777,
    }),
    "raid_applySent_msg": _tools.RODict({
        "ID": "raid_applySent_msg",
        "value": 54000779,
    }),
    "raid_inviteFail_raidFull_msg": _tools.RODict({
        "ID": "raid_inviteFail_raidFull_msg",
        "value": 54000778,
    }),
    "raid_applyFull_msg": _tools.RODict({
        "ID": "raid_applyFull_msg",
        "value": 54000804,
    }),
    "raid_inviteSuccess_msg": _tools.RODict({
        "ID": "raid_inviteSuccess_msg",
        "value": 54000829,
    }),
    "raid_selectOutOfRange_msg": _tools.RODict({
        "ID": "raid_selectOutOfRange_msg",
        "value": 54000869,
    }),
    "raid_readyCheckUndergoing_msg": _tools.RODict({
        "ID": "raid_readyCheckUndergoing_msg",
        "value": 54001080,
    }),
    "raidInviteCooldown": _tools.RODict({
        "ID": "raidInviteCooldown",
        "value": 10,
    }),
    "raid_inviteFail_cooldown_msg": _tools.RODict({
        "ID": "raid_inviteFail_cooldown_msg",
        "value": 54001737,
    }),
    "raidDismissedMsg": _tools.RODict({
        "ID": "raidDismissedMsg",
        "value": 54001738,
    }),
    "raidCreated_chatMsg": _tools.RODict({
        "ID": "raidCreated_chatMsg",
        "value": 58000026,
    }),
    "raidCreated_msg": _tools.RODict({
        "ID": "raidCreated_msg",
        "value": 54000180,
    }),
    "raidFollow_pop": _tools.RODict({
        "ID": "raidFollow_pop",
        "value": 54001974,
    }),
    "raid_readyCheck_check": _tools.RODict({
        "ID": "raid_readyCheck_check",
        "value": 54000729,
    }),
    "raid_readyCheck2": _tools.RODict({
        "ID": "raid_readyCheck2",
        "value": 54000730,
    }),
    "raid_ready_msg": _tools.RODict({
        "ID": "raid_ready_msg",
        "value": 54000732,
    }),
    "raid_unready_msg": _tools.RODict({
        "ID": "raid_unready_msg",
        "value": 58000027,
    }),
    "raidAssembleMembersCD": _tools.RODict({
        "ID": "raidAssembleMembersCD",
        "value": 20,
    }),
    "goToTheRaidCaptainCD": _tools.RODict({
        "ID": "goToTheRaidCaptainCD",
        "value": 20,
    }),
    "raid_captainSummonDone_msg": _tools.RODict({
        "ID": "raid_captainSummonDone_msg",
        "value": 54000785,
    }),
    "raid_captainSummonmsg": _tools.RODict({
        "ID": "raid_captainSummonmsg",
        "value": 54000782,
    }),
    "raid_raidMembersSummonmsg": _tools.RODict({
        "ID": "raid_raidMembersSummonmsg",
        "value": 54000783,
    }),
    "raid_cantMoveRL_msg": _tools.RODict({
        "ID": "raid_cantMoveRL_msg",
        "value": 54000784,
    }),
    "raid_applyRefused_msg": _tools.RODict({
        "ID": "raid_applyRefused_msg",
        "value": 54000786,
    }),
    "raid_RDLDownGrade_msg": _tools.RODict({
        "ID": "raid_RDLDownGrade_msg",
        "value": 54000787,
    }),
    "raid_disbandConfirm": _tools.RODict({
        "ID": "raid_disbandConfirm",
        "value": 54000788,
    }),
    "raid_RLDownGradeOfflineTime": _tools.RODict({
        "ID": "raid_RLDownGradeOfflineTime",
        "value": 300,
    }),
    "raidInvite_inPartyCheck": _tools.RODict({
        "ID": "raidInvite_inPartyCheck",
        "value": 54001918,
    }),
    "raidTeamTitle": _tools.RODict({
        "ID": "raidTeamTitle",
        "value": ('小队一', '小队二', '小队三'),
    }),
    "raid_memberOffline": _tools.RODict({
        "ID": "raid_memberOffline",
        "value": 54001980,
    }),
    "raidStatusDisplay": _tools.RODict({
        "ID": "raidStatusDisplay",
        "value": "团队：{0}/{1}",
    }),
    "raidPartyInivte_underLevel_msg": _tools.RODict({
        "ID": "raidPartyInivte_underLevel_msg",
        "value": 54000725,
    }),
    "raidPartyApply_underLevel_msg": _tools.RODict({
        "ID": "raidPartyApply_underLevel_msg",
        "value": 54000726,
    }),
    "raid_notInRaid_msg": _tools.RODict({
        "ID": "raid_notInRaid_msg",
        "value": 54000607,
    }),
    "raidJoinCheck_inParty": _tools.RODict({
        "ID": "raidJoinCheck_inParty",
        "value": 54001939,
    }),
    "raid_teamInvitationCheck_check": _tools.RODict({
        "ID": "raid_teamInvitationCheck_check",
        "value": 54000617,
    }),
    "raidInviteFail_partyFull": _tools.RODict({
        "ID": "raidInviteFail_partyFull",
        "value": 54001575,
    }),
    "raid_transportBanned_msg": _tools.RODict({
        "ID": "raid_transportBanned_msg",
        "value": 54001577,
    }),
    "raidInviteFail_memberInviteTeam_msg": _tools.RODict({
        "ID": "raidInviteFail_memberInviteTeam_msg",
        "value": 54001407,
    }),
    "raid_appointedPL_msg": _tools.RODict({
        "ID": "raid_appointedPL_msg",
        "value": 54000726,
    }),
    "raid_appointPLDone_msg": _tools.RODict({
        "ID": "raid_appointPLDone_msg",
        "value": 54000727,
    }),
    "raid_playerLeft_msg": _tools.RODict({
        "ID": "raid_playerLeft_msg",
        "value": 58000030,
    }),
    "raid_playerKicked_msg": _tools.RODict({
        "ID": "raid_playerKicked_msg",
        "value": 58000031,
    }),
    "raidTeamNotExist": _tools.RODict({
        "ID": "raidTeamNotExist",
        "value": 54000649,
    })
})