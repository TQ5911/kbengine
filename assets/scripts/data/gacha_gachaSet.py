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
        "value": "召唤{1}次得礼包\n<color=#9e9886>赠送不在统计内</color>",
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
        "value": "概率",
    }),
    "pullRecordText": _tools.RODict({
        "ID": "pullRecordText",
        "value": "记录",
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
        "value": 1,
    }),
    "100rollQualityGapTime": _tools.RODict({
        "ID": "100rollQualityGapTime",
        "value": 0.5,
    }),
    "poolEndMsg": _tools.RODict({
        "ID": "poolEndMsg",
        "value": 54000959,
    }),
    "PoolEndMailID": _tools.RODict({
        "ID": "PoolEndMailID",
        "value": 37000015,
    }),
    "petFxScale": _tools.RODict({
        "ID": "petFxScale",
        "value": 0.6,
    }),
    "petFxOffset": _tools.RODict({
        "ID": "petFxOffset",
        "value": -1.7,
    }),
    "gachaPageTitle": _tools.RODict({
        "ID": "gachaPageTitle",
        "value": "召唤",
    }),
    "pullInfoTitle": _tools.RODict({
        "ID": "pullInfoTitle",
        "value": "概率详情",
    }),
    "progressSound": _tools.RODict({
        "ID": "progressSound",
        "value": 85601031,
    }),
    "dropSound": _tools.RODict({
        "ID": "dropSound",
        "value": 85601032,
    }),
    "openSound": _tools.RODict({
        "ID": "openSound",
        "value": 85601033,
    }),
    "rollStopTips": _tools.RODict({
        "ID": "rollStopTips",
        "value": 54000949,
    }),
    "rerollHelpInfo": _tools.RODict({
        "ID": "rerollHelpInfo",
        "value": 67,
    }),
    "rerollEmptyTips": _tools.RODict({
        "ID": "rerollEmptyTips",
        "value": "右侧选择精灵石",
    }),
    "rerollFailTips": _tools.RODict({
        "ID": "rerollFailTips",
        "value": 54000969,
    }),
    "highQualityStandard": _tools.RODict({
        "ID": "highQualityStandard",
        "value": 2,
    }),
    "highQualityPetScale": _tools.RODict({
        "ID": "highQualityPetScale",
        "value": 1.8,
    }),
    "highQualityPetOffset": _tools.RODict({
        "ID": "highQualityPetOffset",
        "value": -1.0,
    }),
    "rerollItemTips": _tools.RODict({
        "ID": "rerollItemTips",
        "value": 166,
    }),
    "dailyCoinRollTime": _tools.RODict({
        "ID": "dailyCoinRollTime",
        "value": 1,
    }),
    "firstMountsGachaID": _tools.RODict({
        "ID": "firstMountsGachaID",
        "value": 15000001,
    }),
    "mountsRollDailyLimitTips": _tools.RODict({
        "ID": "mountsRollDailyLimitTips",
        "value": "今日剩余召唤次数：{0}",
    }),
    "mountsRollLimitNotEnough": _tools.RODict({
        "ID": "mountsRollLimitNotEnough",
        "value": 54000950,
    }),
    "mountsRollTicketNotEnough": _tools.RODict({
        "ID": "mountsRollTicketNotEnough",
        "value": 54000951,
    }),
    "mountsGuaranteeMaxFull": _tools.RODict({
        "ID": "mountsGuaranteeMaxFull",
        "value": 54000956,
    }),
    "mountsInProgressStop": _tools.RODict({
        "ID": "mountsInProgressStop",
        "value": 54000957,
    }),
    "mountsRollStop": _tools.RODict({
        "ID": "mountsRollStop",
        "value": 54000958,
    }),
    "mountsPityCounter": _tools.RODict({
        "ID": "mountsPityCounter",
        "value": "{0}/{1}",
    }),
    "mountsPityCounterTips": _tools.RODict({
        "ID": "mountsPityCounterTips",
        "value": "召唤{1}次得礼包\n<color=#9e9886>赠送不在统计内</color>",
    }),
    "mountsCountdownTips": _tools.RODict({
        "ID": "mountsCountdownTips",
        "value": "倒计时：{0}天{1}小时",
    }),
    "mountsQuality3Broadcast": _tools.RODict({
        "ID": "mountsQuality3Broadcast",
        "value": 58000229,
    }),
    "mountsQuality4Broadcast": _tools.RODict({
        "ID": "mountsQuality4Broadcast",
        "value": 58000230,
    }),
    "mountsPullInfoText": _tools.RODict({
        "ID": "mountsPullInfoText",
        "value": "概率",
    }),
    "mountspPullRecordText": _tools.RODict({
        "ID": "mountspPullRecordText",
        "value": "记录",
    }),
    "mountsUpItemText": _tools.RODict({
        "ID": "mountsUpItemText",
        "value": "2倍概率",
    }),
    "mounts1rollText": _tools.RODict({
        "ID": "mounts1rollText",
        "value": "召唤1次",
    }),
    "mounts10rollText": _tools.RODict({
        "ID": "mounts10rollText",
        "value": "召唤10次",
    }),
    "mounts100rollText": _tools.RODict({
        "ID": "mounts100rollText",
        "value": "召唤100次",
    }),
    "mountsMaxStack": _tools.RODict({
        "ID": "mountsMaxStack",
        "value": 1000,
    }),
    "mounts100rollCounter": _tools.RODict({
        "ID": "mounts100rollCounter",
        "value": "剩余 {0}/{1}",
    }),
    "mounts100rollShowText": _tools.RODict({
        "ID": "mounts100rollShowText",
        "value": "{0}秒后进入下一轮召唤，将自动跳过动画",
    }),
    "mounts100rollGapTime": _tools.RODict({
        "ID": "mounts100rollGapTime",
        "value": 1,
    }),
    "mounts100rollQualityGapTime": _tools.RODict({
        "ID": "mounts100rollQualityGapTime",
        "value": 0.5,
    }),
    "mountVideoGoldPath": _tools.RODict({
        "ID": "mountVideoGoldPath",
        "value": "drawmount_gold_video.mp4",
    }),
    "mountVideoGoldPathMobile": _tools.RODict({
        "ID": "mountVideoGoldPathMobile",
        "value": "drawmount_gold_video_mobile.mp4",
    }),
    "mountVideoPurplePath": _tools.RODict({
        "ID": "mountVideoPurplePath",
        "value": "drawmount_purple_video.mp4",
    }),
    "mountVideoPurplePathMobile": _tools.RODict({
        "ID": "mountVideoPurplePathMobile",
        "value": "drawmount_purple_video_mobile.mp4",
    })
})