# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: guildChallenge/config
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "guildChallenge": _tools.RODict({
        "ID": "guildChallenge",
        "value": "帮会讨伐",
    }),
    "guildCoinOpen": _tools.RODict({
        "ID": "guildCoinOpen",
        "value": 1,
    }),
    "guildMoneyOpen": _tools.RODict({
        "ID": "guildMoneyOpen",
        "value": 1,
    }),
    "guildRewardTimes": _tools.RODict({
        "ID": "guildRewardTimes",
        "value": 2,
    }),
    "countdownOpen": _tools.RODict({
        "ID": "countdownOpen",
        "value": 300,
    }),
    "countdownPrepare": _tools.RODict({
        "ID": "countdownPrepare",
        "value": 120,
    }),
    "countdownStart": _tools.RODict({
        "ID": "countdownStart",
        "value": 10,
    }),
    "emailReservation": _tools.RODict({
        "ID": "emailReservation",
        "value": 37000017,
    }),
    "emailCountdown": _tools.RODict({
        "ID": "emailCountdown",
        "value": 37000018,
    }),
    "emailStart": _tools.RODict({
        "ID": "emailStart",
        "value": 37000019,
    }),
    "emailSettle": _tools.RODict({
        "ID": "emailSettle",
        "value": 37000020,
    }),
    "guildChallenge_win": _tools.RODict({
        "ID": "guildChallenge_win",
        "value": "帮会讨伐胜利",
    }),
    "guildChallenge_lose": _tools.RODict({
        "ID": "guildChallenge_lose",
        "value": "帮会讨伐失败",
    }),
    "guildChallenge_winTitle": _tools.RODict({
        "ID": "guildChallenge_winTitle",
        "value": "击败{0}",
    }),
    "guildChallenge_loseTitle": _tools.RODict({
        "ID": "guildChallenge_loseTitle",
        "value": "{0}挑战失败，提升战力后再来试试吧",
    }),
    "guildChallenge_rewardTitle": _tools.RODict({
        "ID": "guildChallenge_rewardTitle",
        "value": "胜利奖励",
    }),
    "guildChallenge_hurt": _tools.RODict({
        "ID": "guildChallenge_hurt",
        "value": "造成伤害：",
    }),
    "guildChallenge_rank": _tools.RODict({
        "ID": "guildChallenge_rank",
        "value": "伤害贡献排名：",
    }),
    "guildChallenge_grade": _tools.RODict({
        "ID": "guildChallenge_grade",
        "value": "伤害奖励档位：",
    }),
    "guildChallenge_noRank": _tools.RODict({
        "ID": "guildChallenge_noRank",
        "value": "无排名",
    }),
    "rewardParticipation": _tools.RODict({
        "ID": "rewardParticipation",
        "value": "参与奖励",
    }),
    "rewardParticipationID": _tools.RODict({
        "ID": "rewardParticipationID",
        "value": 40020541,
    }),
    "countDownMsg": _tools.RODict({
        "ID": "countDownMsg",
        "value": "{0}后，自动回到先前位置",
    }),
    "timeNotScheduledFront": _tools.RODict({
        "ID": "timeNotScheduledFront",
        "value": _tools.ROList([[[55], [3], [], [], [], []]]),
    }),
    "timeNotScheduledLater": _tools.RODict({
        "ID": "timeNotScheduledLater",
        "value": _tools.ROList([[[0], [5], [], [], [], []]]),
    }),
    "timeScheduledAhead": _tools.RODict({
        "ID": "timeScheduledAhead",
        "value": "1800",
    }),
    "guildChallengeResetTime": _tools.RODict({
        "ID": "guildChallengeResetTime",
        "value": _tools.ROList([[[0], [5], [], [], [1], []]]),
    }),
    "costInfoNoticeTxt": _tools.RODict({
        "ID": "costInfoNoticeTxt",
        "value": "消耗{0}预约开启帮会讨伐{1}，讨伐将于{2}开始",
    }),
    "guildOpenTimes": _tools.RODict({
        "ID": "guildOpenTimes",
        "value": 2,
    })
})