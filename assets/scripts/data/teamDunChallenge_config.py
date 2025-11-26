# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: teamDunChallenge/config
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "dailyRewardNum": _tools.RODict({
        "ID": "dailyRewardNum",
        "value": 3,
    }),
    "rewardNumCoin": _tools.RODict({
        "ID": "rewardNumCoin",
        "value": 60,
    }),
    "rewardNumCoinDailyLimit": _tools.RODict({
        "ID": "rewardNumCoinDailyLimit",
        "value": 2,
    }),
    "rewardNumItem": _tools.RODict({
        "ID": "rewardNumItem",
        "value": 30000219,
    }),
    "rewardNumItemWeeklyLimit": _tools.RODict({
        "ID": "rewardNumItemWeeklyLimit",
        "value": 10,
    }),
    "teamDunChallengeActID": _tools.RODict({
        "ID": "teamDunChallengeActID",
        "value": 32000004,
    }),
    "enterRefusedMsg": _tools.RODict({
        "ID": "enterRefusedMsg",
        "value": 54000147,
    }),
    "slslAutoHelpInfo": _tools.RODict({
        "ID": "slslAutoHelpInfo",
        "value": 4,
    }),
    "continueEnterMsg": _tools.RODict({
        "ID": "continueEnterMsg",
        "value": 54000148,
    }),
    "raid_useUnbindItem": _tools.RODict({
        "ID": "raid_useUnbindItem",
        "value": 54000143,
    }),
    "raid_noRewardNum": _tools.RODict({
        "ID": "raid_noRewardNum",
        "value": 54000144,
    }),
    "raid_memberNoRewardNum": _tools.RODict({
        "ID": "raid_memberNoRewardNum",
        "value": 54000145,
    }),
    "sugMemberCnt": _tools.RODict({
        "ID": "sugMemberCnt",
        "value": 3,
    }),
    "raid_membersLow": _tools.RODict({
        "ID": "raid_membersLow",
        "value": 54000146,
    }),
    "dunReadyConfirm": _tools.RODict({
        "ID": "dunReadyConfirm",
        "value": 54000149,
    }),
    "useShanglingdingMsg": _tools.RODict({
        "ID": "useShanglingdingMsg",
        "value": "54001264",
    }),
    "raid_startCountdown": _tools.RODict({
        "ID": "raid_startCountdown",
        "value": 54000903,
    }),
    "raid_inTeamRecreate": _tools.RODict({
        "ID": "raid_inTeamRecreate",
        "value": 54000904,
    }),
    "raid_changeBossRecreate": _tools.RODict({
        "ID": "raid_changeBossRecreate",
        "value": 54000905,
    }),
    "raid_changeTeam": _tools.RODict({
        "ID": "raid_changeTeam",
        "value": 54000906,
    }),
    "raid_createTeam": _tools.RODict({
        "ID": "raid_createTeam",
        "value": 54000907,
    }),
    "raid_startAutoTeleport": _tools.RODict({
        "ID": "raid_startAutoTeleport",
        "value": 54000908,
    }),
    "raid_joinCityBattle": _tools.RODict({
        "ID": "raid_joinCityBattle",
        "value": 54000909,
    }),
    "raidStats_win": _tools.RODict({
        "ID": "raidStats_win",
        "value": "挑战胜利",
    }),
    "raidStats_lose": _tools.RODict({
        "ID": "raidStats_lose",
        "value": "挑战失败",
    }),
    "raidStats_winTitle": _tools.RODict({
        "ID": "raidStats_winTitle",
        "value": "{0}完成",
    }),
    "raidStats_loseTitle": _tools.RODict({
        "ID": "raidStats_loseTitle",
        "value": "{0}挑战失败，提升战力后再来试试吧",
    }),
    "raidStats_reward": _tools.RODict({
        "ID": "raidStats_reward",
        "value": "挑战奖励",
    }),
    "raidStats_score": _tools.RODict({
        "ID": "raidStats_score",
        "value": "挑战分数:",
    }),
    "raidStats_time": _tools.RODict({
        "ID": "raidStats_time",
        "value": "完成时间:",
    }),
    "raidStats_countdown": _tools.RODict({
        "ID": "raidStats_countdown",
        "value": "{0}后，自动回到先前位置",
    }),
    "raidStats_mine": _tools.RODict({
        "ID": "raidStats_mine",
        "value": "我的获得情况",
    }),
    "raidStats_other": _tools.RODict({
        "ID": "raidStats_other",
        "value": "队伍获得情况",
    }),
    "teamMembersNum": _tools.RODict({
        "ID": "teamMembersNum",
        "value": 5,
    }),
    "dunDailyTimesInfo": _tools.RODict({
        "ID": "dunDailyTimesInfo",
        "value": 36,
    }),
    "raidStats_rank1": _tools.RODict({
        "ID": "raidStats_rank1",
        "value": "S",
    }),
    "raidStats_rank2": _tools.RODict({
        "ID": "raidStats_rank2",
        "value": "A",
    }),
    "raidStats_rank3": _tools.RODict({
        "ID": "raidStats_rank3",
        "value": "B",
    }),
    "raidStats_rank4": _tools.RODict({
        "ID": "raidStats_rank4",
        "value": "C",
    }),
    "firstRewardText": _tools.RODict({
        "ID": "firstRewardText",
        "value": "首通",
    }),
    "addDunTimesTitle": _tools.RODict({
        "ID": "addDunTimesTitle",
        "value": "补充挑战次数",
    }),
    "dunTimesText": _tools.RODict({
        "ID": "dunTimesText",
        "value": "挑战次数({0}/{1})",
    }),
    "startRaidBtnText": _tools.RODict({
        "ID": "startRaidBtnText",
        "value": "开始挑战",
    })
})