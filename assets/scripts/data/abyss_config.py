# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: abyss/config
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "abyssDailyNum": _tools.RODict({
        "ID": "abyssDailyNum",
        "value": 1,
    }),
    "abyssNumCoin": _tools.RODict({
        "ID": "abyssNumCoin",
        "value": 100,
    }),
    "abyssNumCoinCost": _tools.RODict({
        "ID": "abyssNumCoinCost",
        "value": ((1, 30000021, 100), (2, 30000001, 100)),
    }),
    "abyssNumCoinDailyLimit": _tools.RODict({
        "ID": "abyssNumCoinDailyLimit",
        "value": 2,
    }),
    "abyssNumItem": _tools.RODict({
        "ID": "abyssNumItem",
        "value": 30000314,
    }),
    "abyssActID": _tools.RODict({
        "ID": "abyssActID",
        "value": 32000005,
    }),
    "abyssNumTime": _tools.RODict({
        "ID": "abyssNumTime",
        "value": 30,
    }),
    "abyssCountdownPrompt": _tools.RODict({
        "ID": "abyssCountdownPrompt",
        "value": 60,
    }),
    "abyss_ticketAutoLimit": _tools.RODict({
        "ID": "abyss_ticketAutoLimit",
        "value": 200,
    }),
    "timeExplanation2": _tools.RODict({
        "ID": "timeExplanation2",
        "value": "每张入场门票可延长30分钟限定时间",
    }),
    "timeExplanation3": _tools.RODict({
        "ID": "timeExplanation3",
        "value": "使用元宝或背包中的入场券\n可以将限定时间延长30分钟。",
    }),
    "abyssUseGold": _tools.RODict({
        "ID": "abyssUseGold",
        "value": "使用元宝({0}/{1})",
    }),
    "abyssUseTicket": _tools.RODict({
        "ID": "abyssUseTicket",
        "value": "使用入场券({0}/{1})",
    }),
    "abyssExpansionTitle": _tools.RODict({
        "ID": "abyssExpansionTitle",
        "value": "限定时间：{0}",
    }),
    "autoExpansionUseItemText": _tools.RODict({
        "ID": "autoExpansionUseItemText",
        "value": "消耗{0}/{1}",
    }),
    "autoExpansionTimeText": _tools.RODict({
        "ID": "autoExpansionTimeText",
        "value": "{0}次",
    }),
    "abyss_levelNotOpen": _tools.RODict({
        "ID": "abyss_levelNotOpen",
        "value": 54003400,
    }),
    "abyss_noEnterNum": _tools.RODict({
        "ID": "abyss_noEnterNum",
        "value": 54003401,
    }),
    "abyss_addEnterNumSuccess": _tools.RODict({
        "ID": "abyss_addEnterNumSuccess",
        "value": 54003402,
    }),
    "abyss_addEnterNumLimit": _tools.RODict({
        "ID": "abyss_addEnterNumLimit",
        "value": 54003403,
    }),
    "abyss_addEnterNumFailed": _tools.RODict({
        "ID": "abyss_addEnterNumFailed",
        "value": 54003404,
    }),
    "abyss_addEnterNumLimit2": _tools.RODict({
        "ID": "abyss_addEnterNumLimit2",
        "value": 54003405,
    }),
    "abyss_timeExtensionSuccess": _tools.RODict({
        "ID": "abyss_timeExtensionSuccess",
        "value": 54003406,
    }),
    "abyss_timeExtensionFailed1": _tools.RODict({
        "ID": "abyss_timeExtensionFailed1",
        "value": 54003407,
    }),
    "abyss_timeExtensionFailed2": _tools.RODict({
        "ID": "abyss_timeExtensionFailed2",
        "value": 54003408,
    }),
    "abyss_timeExtensionFailed3": _tools.RODict({
        "ID": "abyss_timeExtensionFailed3",
        "value": 54003409,
    }),
    "abyss_autoExpansionSuccess": _tools.RODict({
        "ID": "abyss_autoExpansionSuccess",
        "value": 54003410,
    }),
    "abyss_autoExpansionCanceled": _tools.RODict({
        "ID": "abyss_autoExpansionCanceled",
        "value": 54003411,
    }),
    "abyss_autoExpansionFailed": _tools.RODict({
        "ID": "abyss_autoExpansionFailed",
        "value": 54003412,
    }),
    "abyss_timeRemaining1": _tools.RODict({
        "ID": "abyss_timeRemaining1",
        "value": 54003413,
    }),
    "abyss_timeRemaining2": _tools.RODict({
        "ID": "abyss_timeRemaining2",
        "value": 54003414,
    }),
    "abyss_timeRemaining3": _tools.RODict({
        "ID": "abyss_timeRemaining3",
        "value": 54003415,
    }),
    "abyss_LeaveDungeonMsg": _tools.RODict({
        "ID": "abyss_LeaveDungeonMsg",
        "value": 54003416,
    }),
    "abyss_cannotMove": _tools.RODict({
        "ID": "abyss_cannotMove",
        "value": 54003417,
    }),
    "abyss_useItem": _tools.RODict({
        "ID": "abyss_useItem",
        "value": 54003418,
    }),
    "abyss_leaveSafetyArea": _tools.RODict({
        "ID": "abyss_leaveSafetyArea",
        "value": 54003419,
    }),
    "abyss_enterSafetyArea": _tools.RODict({
        "ID": "abyss_enterSafetyArea",
        "value": 54003420,
    }),
    "abyss_noGoldMsg": _tools.RODict({
        "ID": "abyss_noGoldMsg",
        "value": 54003421,
    }),
    "abyss_addEnterNumLimit3": _tools.RODict({
        "ID": "abyss_addEnterNumLimit3",
        "value": 54003422,
    }),
    "abyss_ticketAutoLimitMsg": _tools.RODict({
        "ID": "abyss_ticketAutoLimitMsg",
        "value": 54003423,
    }),
    "abyss_fullyBooked": _tools.RODict({
        "ID": "abyss_fullyBooked",
        "value": 54003424,
    })
})