# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: gacha/gachaSet
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "gatchaTypeReward": _tools.RODict({
        "ID": "gatchaTypeReward",
        "value": ((1, 1), (10, 11), (100, 110)),
    }),
    "firstPetGachaID": _tools.RODict({
        "ID": "firstPetGachaID",
        "value": 15000001,
    }),
    "rollDailyLimitTips": _tools.RODict({
        "ID": "rollDailyLimitTips",
        "value": "今日剩余召唤次数：{0}",
    }),
    "rollLimitNotEnough": _tools.RODict({
        "ID": "rollLimitNotEnough",
        "value": 54000950,
    }),
    "rollTicketNotEnough": _tools.RODict({
        "ID": "rollTicketNotEnough",
        "value": 54000951,
    }),
    "guaranteeMaxFull": _tools.RODict({
        "ID": "guaranteeMaxFull",
        "value": 54000956,
    }),
    "inProgressStop": _tools.RODict({
        "ID": "inProgressStop",
        "value": 54000957,
    }),
    "rollStop": _tools.RODict({
        "ID": "rollStop",
        "value": 54000958,
    }),
    "pityCounter": _tools.RODict({
        "ID": "pityCounter",
        "value": "{0}/{1}",
    }),
    "pityCounterTips": _tools.RODict({
        "ID": "pityCounterTips",
        "value": "距离下次获得{0}，还剩{1}次召唤\n赠送次数不含在统计内",
    }),
    "countdownTips": _tools.RODict({
        "ID": "countdownTips",
        "value": "倒计时：{0}天{1}小时",
    }),
    "quality3Broadcast": _tools.RODict({
        "ID": "quality3Broadcast",
        "value": 58000006,
    }),
    "quality4Broadcast": _tools.RODict({
        "ID": "quality4Broadcast",
        "value": 58000007,
    }),
    "pullInfoText": _tools.RODict({
        "ID": "pullInfoText",
        "value": "概率详情",
    }),
    "pullRecordText": _tools.RODict({
        "ID": "pullRecordText",
        "value": "历史记录",
    }),
    "upItemText": _tools.RODict({
        "ID": "upItemText",
        "value": "2倍概率",
    }),
    "1rollText": _tools.RODict({
        "ID": "1rollText",
        "value": "召唤1次",
    }),
    "10rollText": _tools.RODict({
        "ID": "10rollText",
        "value": "召唤10次",
    }),
    "100rollText": _tools.RODict({
        "ID": "100rollText",
        "value": "召唤100次",
    }),
    "maxStack": _tools.RODict({
        "ID": "maxStack",
        "value": 1000,
    }),
    "100rollCounter": _tools.RODict({
        "ID": "100rollCounter",
        "value": "剩余 {0}/{1}",
    }),
    "100rollShowText": _tools.RODict({
        "ID": "100rollShowText",
        "value": "{0}秒后进入下一轮召唤，将自动跳过动画",
    }),
    "100rollGapTime": _tools.RODict({
        "ID": "100rollGapTime",
        "value": 3,
    }),
    "poolEndMsg": _tools.RODict({
        "ID": "poolEndMsg",
        "value": 54000959,
    }),
    "PoolEndMailID": _tools.RODict({
        "ID": "PoolEndMailID",
        "value": 37000015,
    })
})