# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: commonTextConfig/config
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "formatOfLevels": _tools.RODict({
        "ID": "formatOfLevels",
        "value": "{0}级",
        "Type": "string"
    }),
    "gearGradeText": _tools.RODict({
        "ID": "gearGradeText",
        "value": "{0}阶",
        "Type": "string"
    }),
    "physicalAtk": _tools.RODict({
        "ID": "physicalAtk",
        "value": "物理攻击",
        "Type": "string"
    }),
    "magicAtk": _tools.RODict({
        "ID": "magicAtk",
        "value": "法术攻击",
        "Type": "string"
    }),
    "physicalArmor": _tools.RODict({
        "ID": "physicalArmor",
        "value": "物理防御",
        "Type": "string"
    }),
    "magicArmor": _tools.RODict({
        "ID": "magicArmor",
        "value": "法术防御",
        "Type": "string"
    }),
    "second": _tools.RODict({
        "ID": "second",
        "value": "{0}秒",
        "Type": "string"
    }),
    "skillConsumeMp": _tools.RODict({
        "ID": "skillConsumeMp",
        "value": "{0}能量",
        "Type": "string"
    }),
    "skillRange": _tools.RODict({
        "ID": "skillRange",
        "value": "{0}米",
        "Type": "string"
    }),
    "day": _tools.RODict({
        "ID": "day",
        "value": "{0}天",
        "Type": "string"
    }),
    "hourDoubleDigits": _tools.RODict({
        "ID": "hourDoubleDigits",
        "value": "{0:00}小时",
        "Type": "string"
    }),
    "minuteDoubleDigits": _tools.RODict({
        "ID": "minuteDoubleDigits",
        "value": "{0:00}分",
        "Type": "string"
    }),
    "secondDoubleDigits": _tools.RODict({
        "ID": "secondDoubleDigits",
        "value": "{0:00}秒",
        "Type": "string"
    }),
    "expirationTips": _tools.RODict({
        "ID": "expirationTips",
        "value": "{0}后下架",
        "Type": "string"
    }),
    "expiredTips": _tools.RODict({
        "ID": "expiredTips",
        "value": "已过期",
        "Type": "string"
    }),
    "dailyRemainNum": _tools.RODict({
        "ID": "dailyRemainNum",
        "value": "本日剩余次数：{0}/{1}",
        "Type": "string"
    }),
    "weeklyRemainNum": _tools.RODict({
        "ID": "weeklyRemainNum",
        "value": "本周剩余次数：{0}/{1}",
        "Type": "string"
    }),
    "enterNum": _tools.RODict({
        "ID": "enterNum",
        "value": "入场次数：{0}/{1}",
        "Type": "string"
    }),
    "refresh": _tools.RODict({
        "ID": "refresh",
        "value": "刷新",
        "Type": "string"
    }),
    "levelRangeText": _tools.RODict({
        "ID": "levelRangeText",
        "value": "{0}-{1}级",
        "Type": "string"
    }),
    "branchText": _tools.RODict({
        "ID": "branchText",
        "value": "{0}线",
        "Type": "string"
    }),
    "onLineStateText": _tools.RODict({
        "ID": "onLineStateText",
        "value": "在线",
        "Type": "string"
    }),
    "upgradeText": _tools.RODict({
        "ID": "upgradeText",
        "value": "升阶概率：{0}%",
        "Type": "string"
    }),
    "guildText": _tools.RODict({
        "ID": "guildText",
        "value": "帮会：{0}",
        "Type": "string"
    }),
    "nullText": _tools.RODict({
        "ID": "nullText",
        "value": "无",
        "Type": "string"
    }),
    "uiVisibleLvLimitText": _tools.RODict({
        "ID": "uiVisibleLvLimitText",
        "value": "等级达到<color=#c60c0c>{0}</color>级解锁",
        "Type": "string"
    }),
    "uiVisibleTaskLimitText": _tools.RODict({
        "ID": "uiVisibleTaskLimitText",
        "value": "完成<color=#c60c0c>任务：{0}</color>解锁",
        "Type": "string"
    }),
    "dayDateFormatText": _tools.RODict({
        "ID": "dayDateFormatText",
        "value": "第{0}天",
        "Type": "string"
    }),
    "autoShutdownCountTime": _tools.RODict({
        "ID": "autoShutdownCountTime",
        "value": "{0}后自动关闭",
        "Type": "string"
    }),
    "AtkMulImprove": _tools.RODict({
        "ID": "AtkMulImprove",
        "value": "增幅",
        "Type": "string"
    }),
    "selectedMonsterLv": _tools.RODict({
        "ID": "selectedMonsterLv",
        "value": "等级：{0}",
        "Type": "string"
    }),
    "TapTapLoginText": _tools.RODict({
        "ID": "TapTapLoginText",
        "value": "TapTap登录",
        "Type": "string"
    }),
    "YXGNumberLoginText": _tools.RODict({
        "ID": "YXGNumberLoginText",
        "value": "一键登录",
        "Type": "string"
    }),
    "YXGSMSLoginText": _tools.RODict({
        "ID": "YXGSMSLoginText",
        "value": "短信登录",
        "Type": "string"
    })
})