# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: wonderLand/config
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "dailyWonderLandNum": _tools.RODict({
        "ID": "dailyWonderLandNum",
        "value": 2,
    }),
    "wonderLandNumCoin": _tools.RODict({
        "ID": "wonderLandNumCoin",
        "value": 100,
    }),
    "wonderLandNumCoinCost": _tools.RODict({
        "ID": "wonderLandNumCoinCost",
        "value": ((1, 30000021, 100), (2, 30000001, 100)),
    }),
    "wonderLandNumCoinDailyLimit": _tools.RODict({
        "ID": "wonderLandNumCoinDailyLimit",
        "value": 2,
    }),
    "wonderLandNumItem": _tools.RODict({
        "ID": "wonderLandNumItem",
        "value": 30000304,
    }),
    "wonderLandNumItemLimit": _tools.RODict({
        "ID": "wonderLandNumItemLimit",
        "value": 14,
    }),
    "wonderLandActID": _tools.RODict({
        "ID": "wonderLandActID",
        "value": 32000003,
    }),
    "wonderLandNumTime": _tools.RODict({
        "ID": "wonderLandNumTime",
        "value": 30,
    }),
    "wonderLandCountdownPrompt": _tools.RODict({
        "ID": "wonderLandCountdownPrompt",
        "value": 60,
    }),
    "timeExplanation2": _tools.RODict({
        "ID": "timeExplanation2",
        "value": "每张入场门票可延长30分钟限定时间",
    }),
    "timeExplanation3": _tools.RODict({
        "ID": "timeExplanation3",
        "value": "使用元宝或背包中的入场券\n可以将限定时间延长30分钟。",
    }),
    "wonderLandUseGold": _tools.RODict({
        "ID": "wonderLandUseGold",
        "value": "使用元宝({0}/{1})",
    }),
    "wonderLandUseTicket": _tools.RODict({
        "ID": "wonderLandUseTicket",
        "value": "使用入场券({0}/{1})",
    }),
    "wonderLand_levelNotOpen": _tools.RODict({
        "ID": "wonderLand_levelNotOpen",
        "value": 54001933,
    }),
    "wonderLand_noEnterNum": _tools.RODict({
        "ID": "wonderLand_noEnterNum",
        "value": 54001934,
    }),
    "wonderLand_addEnterNumSuccess": _tools.RODict({
        "ID": "wonderLand_addEnterNumSuccess",
        "value": 54001935,
    }),
    "wonderLand_addEnterNumLimit": _tools.RODict({
        "ID": "wonderLand_addEnterNumLimit",
        "value": 54001936,
    }),
    "wonderLand_addEnterNumFailed": _tools.RODict({
        "ID": "wonderLand_addEnterNumFailed",
        "value": 54001937,
    }),
    "wonderLand_addEnterNumLimit2": _tools.RODict({
        "ID": "wonderLand_addEnterNumLimit2",
        "value": 54001938,
    }),
    "wonderLand_timeExtensionSuccess": _tools.RODict({
        "ID": "wonderLand_timeExtensionSuccess",
        "value": 54001939,
    }),
    "wonderLand_timeExtensionFailed1": _tools.RODict({
        "ID": "wonderLand_timeExtensionFailed1",
        "value": 54001940,
    }),
    "wonderLand_timeExtensionFailed2": _tools.RODict({
        "ID": "wonderLand_timeExtensionFailed2",
        "value": 54001941,
    }),
    "wonderLand_timeExtensionFailed3": _tools.RODict({
        "ID": "wonderLand_timeExtensionFailed3",
        "value": 54001942,
    }),
    "wonderLand_autoExpansionSuccess": _tools.RODict({
        "ID": "wonderLand_autoExpansionSuccess",
        "value": 54001943,
    }),
    "wonderLand_autoExpansionCanceled": _tools.RODict({
        "ID": "wonderLand_autoExpansionCanceled",
        "value": 54001944,
    }),
    "wonderLand_autoExpansionFailed": _tools.RODict({
        "ID": "wonderLand_autoExpansionFailed",
        "value": 54001945,
    }),
    "wonderLand_timeRemaining1": _tools.RODict({
        "ID": "wonderLand_timeRemaining1",
        "value": 54001946,
    }),
    "wonderLand_timeRemaining2": _tools.RODict({
        "ID": "wonderLand_timeRemaining2",
        "value": 54001947,
    }),
    "wonderLand_timeRemaining3": _tools.RODict({
        "ID": "wonderLand_timeRemaining3",
        "value": 54001948,
    }),
    "wonderLand_LeaveDungeonMsg": _tools.RODict({
        "ID": "wonderLand_LeaveDungeonMsg",
        "value": 54001949,
    }),
    "wonderLand_cannotMove": _tools.RODict({
        "ID": "wonderLand_cannotMove",
        "value": 54001950,
    }),
    "wonderLand_useItem": _tools.RODict({
        "ID": "wonderLand_useItem",
        "value": 54001951,
    }),
    "wonderLand_leaveSafetyArea": _tools.RODict({
        "ID": "wonderLand_leaveSafetyArea",
        "value": 54001952,
    }),
    "wonderLand_enterSafetyArea": _tools.RODict({
        "ID": "wonderLand_enterSafetyArea",
        "value": 54001953,
    }),
    "wonderLand_summoningFailed": _tools.RODict({
        "ID": "wonderLand_summoningFailed",
        "value": 54001954,
    }),
    "wonderLand_summoningProgress": _tools.RODict({
        "ID": "wonderLand_summoningProgress",
        "value": 54001955,
    }),
    "wonderLand_summoningSuccess": _tools.RODict({
        "ID": "wonderLand_summoningSuccess",
        "value": 54001956,
    }),
    "wonderLand_fixedBossAppear": _tools.RODict({
        "ID": "wonderLand_fixedBossAppear",
        "value": 54001957,
    }),
    "wonderLand_randomBossAppear": _tools.RODict({
        "ID": "wonderLand_randomBossAppear",
        "value": 54001958,
    }),
    "wonderLand_summoningFailed2": _tools.RODict({
        "ID": "wonderLand_summoningFailed2",
        "value": 54001961,
    }),
    "wonderLand_bossAlive": _tools.RODict({
        "ID": "wonderLand_bossAlive",
        "value": 54001977,
    }),
    "wonderLand_noGoldMsg": _tools.RODict({
        "ID": "wonderLand_noGoldMsg",
        "value": 54003080,
    }),
    "WonderLand_addEnterNumLimit3": _tools.RODict({
        "ID": "WonderLand_addEnterNumLimit3",
        "value": 54001979,
    }),
    "WonderLandExpansionTitle": _tools.RODict({
        "ID": "WonderLandExpansionTitle",
        "value": "限定时间：{0}",
    }),
    "AutoExpansionUseItemText": _tools.RODict({
        "ID": "AutoExpansionUseItemText",
        "value": "消耗{0}/{1}",
    }),
    "AutoExpansionTimeText": _tools.RODict({
        "ID": "AutoExpansionTimeText",
        "value": "{0}次",
    }),
    "WonderLand_ticketAutoLimitMsg": _tools.RODict({
        "ID": "WonderLand_ticketAutoLimitMsg",
        "value": 54003265,
    }),
    "WonderLand_ticketAutoLimit": _tools.RODict({
        "ID": "WonderLand_ticketAutoLimit",
        "value": 200,
    }),
    "WonderLand_fullyBooked": _tools.RODict({
        "ID": "WonderLand_fullyBooked",
        "value": 54003266,
    })
})