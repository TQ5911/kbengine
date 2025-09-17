# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: gamePlay/set
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "ifActivityGoto_0": _tools.RODict({
        "ID": "ifActivityGoto_0",
        "value": 54000816,
    }),
    "ifCrossSceneRouting_0": _tools.RODict({
        "ID": "ifCrossSceneRouting_0",
        "value": 54000817,
    }),
    "ifCrossSceneRouting_2": _tools.RODict({
        "ID": "ifCrossSceneRouting_2",
        "value": 54000818,
    }),
    "ifEnterDun_0": _tools.RODict({
        "ID": "ifEnterDun_0",
        "value": 54000816,
    }),
    "ifEnterDun_2": _tools.RODict({
        "ID": "ifEnterDun_2",
        "value": 54000818,
    }),
    "gotoTheSameGamePlayID": _tools.RODict({
        "ID": "gotoTheSameGamePlayID",
        "value": 54000932,
    }),
    "enterDunFailTeammateInDun": _tools.RODict({
        "ID": "enterDunFailTeammateInDun",
        "value": 54001274,
    }),
    "arverageLevelFormularID": _tools.RODict({
        "ID": "arverageLevelFormularID",
        "value": 34000001,
    }),
    "leaveDungeonConfirmMsg": _tools.RODict({
        "ID": "leaveDungeonConfirmMsg",
        "value": 54000319,
    }),
    "soundId_reliveSuccess": _tools.RODict({
        "ID": "soundId_reliveSuccess",
        "value": 85002025,
    }),
    "leaveDunVisibleID": _tools.RODict({
        "ID": "leaveDunVisibleID",
        "value": 5,
    }),
    "resurrectTime": _tools.RODict({
        "ID": "resurrectTime",
        "value": 90,
    }),
    "resurrectHP": _tools.RODict({
        "ID": "resurrectHP",
        "value": 20,
    }),
    "resurrectProtectBuffID": _tools.RODict({
        "ID": "resurrectProtectBuffID",
        "value": 64000902,
    }),
    "deadNameColorID": _tools.RODict({
        "ID": "deadNameColorID",
        "value": 32,
    }),
    "expDropOnDeath": _tools.RODict({
        "ID": "expDropOnDeath",
        "value": 34000005,
    }),
    "coinDropOnDeath": _tools.RODict({
        "ID": "coinDropOnDeath",
        "value": 34000006,
    }),
    "beInjuredBuffID": _tools.RODict({
        "ID": "beInjuredBuffID",
        "value": 64000009,
    }),
    "beInjuredBuffLevel": _tools.RODict({
        "ID": "beInjuredBuffLevel",
        "value": 3,
    }),
    "beInjuredBuffLimit": _tools.RODict({
        "ID": "beInjuredBuffLimit",
        "value": 10,
    }),
    "beCritInjuredBuffID": _tools.RODict({
        "ID": "beCritInjuredBuffID",
        "value": 64000010,
    }),
    "resWaitResetTime": _tools.RODict({
        "ID": "resWaitResetTime",
        "value": 600,
    }),
    "resurrectCD": _tools.RODict({
        "ID": "resurrectCD",
        "value": 34000007,
    }),
    "resurrectCDMSG": _tools.RODict({
        "ID": "resurrectCDMSG",
        "value": 54000075,
    }),
    "punishmentKillerTips": _tools.RODict({
        "ID": "punishmentKillerTips",
        "value": "{0}",
    }),
    "killerTips": _tools.RODict({
        "ID": "killerTips",
        "value": "击杀者：<color=#d35a66>{0}</color>",
    }),
    "dropsCloseTimeout": _tools.RODict({
        "ID": "dropsCloseTimeout",
        "value": 15,
    }),
    "cantResAtNearestTips": _tools.RODict({
        "ID": "cantResAtNearestTips",
        "value": "当前状态无法进行据点复活",
    }),
    "maxExpRecTime": _tools.RODict({
        "ID": "maxExpRecTime",
        "value": 86400,
    }),
    "maxExpRecSlots": _tools.RODict({
        "ID": "maxExpRecSlots",
        "value": 10,
    }),
    "removeExpConfirm": _tools.RODict({
        "ID": "removeExpConfirm",
        "value": 54000061,
    }),
    "expRecPctTips": _tools.RODict({
        "ID": "expRecPctTips",
        "value": "恢复率{0}%",
    }),
    "freeExpRecBtnText": _tools.RODict({
        "ID": "freeExpRecBtnText",
        "value": "免费恢复({0}）",
    }),
    "freeExpRecCount": _tools.RODict({
        "ID": "freeExpRecCount",
        "value": 3,
    }),
    "freeExpRecConfirm": _tools.RODict({
        "ID": "freeExpRecConfirm",
        "value": 54000062,
    }),
    "freeExpRecPct": _tools.RODict({
        "ID": "freeExpRecPct",
        "value": 1.0,
    }),
    "normalExpRecPct": _tools.RODict({
        "ID": "normalExpRecPct",
        "value": 0.75,
    }),
    "advancedExpRecPct": _tools.RODict({
        "ID": "advancedExpRecPct",
        "value": 1.0,
    }),
    "expRecConfirm": _tools.RODict({
        "ID": "expRecConfirm",
        "value": 54000063,
    }),
    "normalExpRecCost": _tools.RODict({
        "ID": "normalExpRecCost",
        "value": 34000008,
    }),
    "advancedExpRecCost": _tools.RODict({
        "ID": "advancedExpRecCost",
        "value": 34000009,
    }),
    "msgId_cantUseReturnScroll": _tools.RODict({
        "ID": "msgId_cantUseReturnScroll",
        "value": 54000029,
    }),
    "safeAndUnsafeAreaBgColor": _tools.RODict({
        "ID": "safeAndUnsafeAreaBgColor",
        "value": (33, 34),
    }),
    "mapCollectionListFullMsg": _tools.RODict({
        "ID": "mapCollectionListFullMsg",
        "value": 54000037,
    }),
    "dropExpTab": _tools.RODict({
        "ID": "dropExpTab",
        "value": "经验（{0}/{1}）",
    }),
    "dropGearTab": _tools.RODict({
        "ID": "dropGearTab",
        "value": "装备（{0}/{1}）",
    }),
    "clearDebuffID": _tools.RODict({
        "ID": "clearDebuffID",
        "value": _tools.ROList([64000009, 64000010]),
    }),
    "HealingWoundsCost": _tools.RODict({
        "ID": "HealingWoundsCost",
        "value": _tools.ROList([0, 180]),
    }),
    "HealingWoundsCostCurrency": _tools.RODict({
        "ID": "HealingWoundsCostCurrency",
        "value": 30000001,
    }),
    "HealingWoundsMsg1": _tools.RODict({
        "ID": "HealingWoundsMsg1",
        "value": 54003121,
    }),
    "HealingWoundsMsg2": _tools.RODict({
        "ID": "HealingWoundsMsg2",
        "value": 54003122,
    }),
    "HealingWoundsConfirm": _tools.RODict({
        "ID": "HealingWoundsConfirm",
        "value": 54003123,
    }),
    "HealingWoundsConfirm2": _tools.RODict({
        "ID": "HealingWoundsConfirm2",
        "value": 54003124,
    })
})