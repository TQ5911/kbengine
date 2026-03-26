# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: cube/config
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "dailyCubeNum": _tools.RODict({
        "ID": "dailyCubeNum",
        "value": 2,
    }),
    "cubeNumCoin": _tools.RODict({
        "ID": "cubeNumCoin",
        "value": 100,
    }),
    "cubeNumCoinDailyLimit": _tools.RODict({
        "ID": "cubeNumCoinDailyLimit",
        "value": 1,
    }),
    "cubeNumItem": _tools.RODict({
        "ID": "cubeNumItem",
        "value": 30000222,
    }),
    "cubeNumItemWeeklyLimit": _tools.RODict({
        "ID": "cubeNumItemWeeklyLimit",
        "value": 7,
    }),
    "cubeActID": _tools.RODict({
        "ID": "cubeActID",
        "value": 32000002,
    }),
    "cubeNumTime": _tools.RODict({
        "ID": "cubeNumTime",
        "value": 30,
    }),
    "cubeSwitchScenesCD": _tools.RODict({
        "ID": "cubeSwitchScenesCD",
        "value": 5,
    }),
    "cubeCountdownPrompt": _tools.RODict({
        "ID": "cubeCountdownPrompt",
        "value": 60,
    }),
    "timeExplanation": _tools.RODict({
        "ID": "timeExplanation",
        "value": "【混沌回廊入场时间】\n进入混沌回廊须消耗入场门票，每次入场时间30分钟。",
    }),
    "numExplanation": _tools.RODict({
        "ID": "numExplanation",
        "value": "【混沌回廊入场门票】\n可使用每日免费入场门票进入混沌回廊。免费入场门票于每日5:00重置。\n用完免费入场门票时，可通过兑换的方式进入混沌回廊。",
    }),
    "timeExtensionExplanation": _tools.RODict({
        "ID": "timeExtensionExplanation",
        "value": "【延长限定时间】\n限定时间小于30分钟时，可以消耗1次入场门票延长限定时间30分钟。\n可以使用元宝或通行牌补充入场门票。\n限定每日2次使用元宝补充入场门票。",
    }),
    "autoExpansionExplanation": _tools.RODict({
        "ID": "autoExpansionExplanation",
        "value": "【自动延长】\n自动延长可以指定延长次数，一次设置可指定最多20次自动延长。\n若已设置为自动延长，则当限定时间不足1分钟时，会自动延长限定时间。\n自动延长会以入场门票>通行牌>元宝的顺序使用。\n限定每日2次使用元宝自动延长，需在元宝使用选项开启后才能使用。\n若角色死亡或退出混沌回廊，则取消自动延长。",
    }),
    "timeExplanation2": _tools.RODict({
        "ID": "timeExplanation2",
        "value": "每张入场门票可延长30分钟限定时间",
    }),
    "timeExplanation3": _tools.RODict({
        "ID": "timeExplanation3",
        "value": "使用元宝或背包中的通行牌\n可以将限定时间延长30分钟。",
    }),
    "cubeUseGold": _tools.RODict({
        "ID": "cubeUseGold",
        "value": "使用元宝({0}/{1})",
    }),
    "cubeUseTicket": _tools.RODict({
        "ID": "cubeUseTicket",
        "value": "使用通行牌({0}/{1})",
    }),
    "cubeExpansionTitle": _tools.RODict({
        "ID": "cubeExpansionTitle",
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
    "cube_levelNotOpen": _tools.RODict({
        "ID": "cube_levelNotOpen",
        "value": 54001900,
    }),
    "cube_noEnterNum": _tools.RODict({
        "ID": "cube_noEnterNum",
        "value": 54001901,
    }),
    "cube_addEnterNumSuccess": _tools.RODict({
        "ID": "cube_addEnterNumSuccess",
        "value": 54001902,
    }),
    "cube_addEnterNumLimit": _tools.RODict({
        "ID": "cube_addEnterNumLimit",
        "value": 54001903,
    }),
    "cube_addEnterNumFailed": _tools.RODict({
        "ID": "cube_addEnterNumFailed",
        "value": 54001904,
    }),
    "cube_addEnterNumLimit2": _tools.RODict({
        "ID": "cube_addEnterNumLimit2",
        "value": 54001905,
    }),
    "cube_addEnterNumLimit3": _tools.RODict({
        "ID": "cube_addEnterNumLimit3",
        "value": 54001960,
    }),
    "cube_countdownNotEnd": _tools.RODict({
        "ID": "cube_countdownNotEnd",
        "value": 54001906,
    }),
    "cube_timeExtensionSuccess": _tools.RODict({
        "ID": "cube_timeExtensionSuccess",
        "value": 54001907,
    }),
    "cube_timeExtensionFailed1": _tools.RODict({
        "ID": "cube_timeExtensionFailed1",
        "value": 54001908,
    }),
    "cube_timeExtensionFailed2": _tools.RODict({
        "ID": "cube_timeExtensionFailed2",
        "value": 54001909,
    }),
    "cube_timeExtensionFailed3": _tools.RODict({
        "ID": "cube_timeExtensionFailed3",
        "value": 54001910,
    }),
    "cube_autoExpansionSuccess": _tools.RODict({
        "ID": "cube_autoExpansionSuccess",
        "value": 54001911,
    }),
    "cube_autoExpansionCanceled": _tools.RODict({
        "ID": "cube_autoExpansionCanceled",
        "value": 54001912,
    }),
    "cube_autoExpansionFailed": _tools.RODict({
        "ID": "cube_autoExpansionFailed",
        "value": 54001913,
    }),
    "cube_timeRemaining1": _tools.RODict({
        "ID": "cube_timeRemaining1",
        "value": 54001914,
    }),
    "cube_timeRemaining2": _tools.RODict({
        "ID": "cube_timeRemaining2",
        "value": 54001915,
    }),
    "cube_timeRemaining3": _tools.RODict({
        "ID": "cube_timeRemaining3",
        "value": 54001916,
    }),
    "cube_LeaveDungeonMsg": _tools.RODict({
        "ID": "cube_LeaveDungeonMsg",
        "value": 54001917,
    }),
    "cube_cannotMove": _tools.RODict({
        "ID": "cube_cannotMove",
        "value": 54001918,
    }),
    "cube_useItem": _tools.RODict({
        "ID": "cube_useItem",
        "value": 54001919,
    }),
    "cube_prayConfirm1": _tools.RODict({
        "ID": "cube_prayConfirm1",
        "value": 54003250,
    }),
    "cube_prayConfirm2": _tools.RODict({
        "ID": "cube_prayConfirm2",
        "value": 54003251,
    }),
    "cube_prayNoTimes": _tools.RODict({
        "ID": "cube_prayNoTimes",
        "value": 54003252,
    }),
    "cube_chapmanLeave": _tools.RODict({
        "ID": "cube_chapmanLeave",
        "value": 54003253,
    }),
    "cube_floorJudge": _tools.RODict({
        "ID": "cube_floorJudge",
        "value": 54003111,
    }),
    "cube_passNotEnough": _tools.RODict({
        "ID": "cube_passNotEnough",
        "value": 54003112,
    }),
    "cube_cowRoomConfirm": _tools.RODict({
        "ID": "cube_cowRoomConfirm",
        "value": 54003113,
    }),
    "cube_cowRoomTimeMsg": _tools.RODict({
        "ID": "cube_cowRoomTimeMsg",
        "value": 54003114,
    }),
    "cube_levelConfirm": _tools.RODict({
        "ID": "cube_levelConfirm",
        "value": 54003254,
    }),
    "cube_levelLocked": _tools.RODict({
        "ID": "cube_levelLocked",
        "value": 54003255,
    }),
    "cube_crazyRoomTimeMsg": _tools.RODict({
        "ID": "cube_crazyRoomTimeMsg",
        "value": 54003263,
    }),
    "cube_ringDefenderPresence": _tools.RODict({
        "ID": "cube_ringDefenderPresence",
        "value": 54003258,
    }),
    "cube_ringDefenderPresence2": _tools.RODict({
        "ID": "cube_ringDefenderPresence2",
        "value": 54003264,
    }),
    "cube_ticketAutoLimitMsg": _tools.RODict({
        "ID": "cube_ticketAutoLimitMsg",
        "value": 54003265,
    }),
    "cube_ticketAutoLimit": _tools.RODict({
        "ID": "cube_ticketAutoLimit",
        "value": 200,
    }),
    "cube_cowRoomEntranceNum": _tools.RODict({
        "ID": "cube_cowRoomEntranceNum",
        "value": _tools.ROList([4, 6]),
    }),
    "cube_cowRoomEntranceTime": _tools.RODict({
        "ID": "cube_cowRoomEntranceTime",
        "value": 3,
    }),
    "cube_cowRoomEntranceIntervalTime": _tools.RODict({
        "ID": "cube_cowRoomEntranceIntervalTime",
        "value": _tools.ROList([5, 15]),
    }),
    "cube_cowRoomEntrancePersonalTime": _tools.RODict({
        "ID": "cube_cowRoomEntrancePersonalTime",
        "value": 30,
    }),
    "cube_hall": _tools.RODict({
        "ID": "cube_hall",
        "value": 3100,
    }),
    "cube_prayTimesEveryDay": _tools.RODict({
        "ID": "cube_prayTimesEveryDay",
        "value": 1,
    }),
    "cube_chapmanRefreshInterval": _tools.RODict({
        "ID": "cube_chapmanRefreshInterval",
        "value": 10,
    }),
    "cube_prayCostItem": _tools.RODict({
        "ID": "cube_prayCostItem",
        "value": 30000314,
    }),
    "cube_prayCostCurrency": _tools.RODict({
        "ID": "cube_prayCostCurrency",
        "value": _tools.ROList([30000021, 30]),
    }),
    "cube_eachRoomTime": _tools.RODict({
        "ID": "cube_eachRoomTime",
        "value": ([2, 30], [4, 30]),
    }),
    "cube_transportProtection": _tools.RODict({
        "ID": "cube_transportProtection",
        "value": 3,
    })
})