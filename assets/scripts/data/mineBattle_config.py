# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: mineBattle/config
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "mineBattle_miningArea": _tools.RODict({
        "ID": "mineBattle_miningArea",
        "value": ([1022, 1024, 1026], [1121, 1122, 1123]),
    }),
    "mineBattle_miningBattleArea": _tools.RODict({
        "ID": "mineBattle_miningBattleArea",
        "value": _tools.ROList([1026, 1123]),
    }),
    "mineBattle_miningSafeArea": _tools.RODict({
        "ID": "mineBattle_miningSafeArea",
        "value": "{1026:1024, 1123:1122}",
    }),
    "mineBattle_miningTime": _tools.RODict({
        "ID": "mineBattle_miningTime",
        "value": _tools.ROList([1600, 200]),
    }),
    "mineBattle_startTime": _tools.RODict({
        "ID": "mineBattle_startTime",
        "value": _tools.ROList([3, 2000, 2100]),
    }),
    "mineBattle_interfacePromptTime": _tools.RODict({
        "ID": "mineBattle_interfacePromptTime",
        "value": 10,
    }),
    "mineBattle_transferPersonnelTime": _tools.RODict({
        "ID": "mineBattle_transferPersonnelTime",
        "value": 1,
    }),
    "mineBattle_invincibleTime": _tools.RODict({
        "ID": "mineBattle_invincibleTime",
        "value": 1,
    }),
    "mineBattle_recoverRange": _tools.RODict({
        "ID": "mineBattle_recoverRange",
        "value": 3,
    }),
    "mineBattle_recoveryRatio": _tools.RODict({
        "ID": "mineBattle_recoveryRatio",
        "value": _tools.ROList([0.1, 0.5]),
    }),
    "mineBattle_damageScore": _tools.RODict({
        "ID": "mineBattle_damageScore",
        "value": 10000,
    }),
    "mineBattle_lastHitScore": _tools.RODict({
        "ID": "mineBattle_lastHitScore",
        "value": 100,
    }),
    "mineBattle_killScore": _tools.RODict({
        "ID": "mineBattle_killScore",
        "value": _tools.ROList([5, 15]),
    }),
    "mineBattle_takePartScore": _tools.RODict({
        "ID": "mineBattle_takePartScore",
        "value": _tools.ROList([30, 5, 300]),
    }),
    "mineBattle_rankScoreThreshold": _tools.RODict({
        "ID": "mineBattle_rankScoreThreshold",
        "value": 500,
    }),
    "mineBattle_rewardThreshold": _tools.RODict({
        "ID": "mineBattle_rewardThreshold",
        "value": 200,
    }),
    "mineBattle_miningPersonalDuration": _tools.RODict({
        "ID": "mineBattle_miningPersonalDuration",
        "value": _tools.ROList([30, 60]),
    }),
    "mineBattle_incomeCoefficient": _tools.RODict({
        "ID": "mineBattle_incomeCoefficient",
        "value": 1.5,
    }),
    "mineBattle_extraIncome": _tools.RODict({
        "ID": "mineBattle_extraIncome",
        "value": 5,
    }),
    "mineBattle_bonusIncome": _tools.RODict({
        "ID": "mineBattle_bonusIncome",
        "value": _tools.ROList([30, 1, 50]),
    }),
    "mineBattle_flagReset": _tools.RODict({
        "ID": "mineBattle_flagReset",
        "value": 5,
    }),
    "mineBattle_flagDamageEffect": _tools.RODict({
        "ID": "mineBattle_flagDamageEffect",
        "value": _tools.ROList([3, 5]),
    }),
    "mineBattle_InterfaceButtonText": _tools.RODict({
        "ID": "mineBattle_InterfaceButtonText",
        "value": "争夺中",
    }),
    "mineBattle_InterfaceCoreText1": _tools.RODict({
        "ID": "mineBattle_InterfaceCoreText1",
        "value": "保护中",
    }),
    "mineBattle_InterfaceCoreText2": _tools.RODict({
        "ID": "mineBattle_InterfaceCoreText2",
        "value": "战斗中",
    }),
    "mineBattle_InterfaceFlagText1": _tools.RODict({
        "ID": "mineBattle_InterfaceFlagText1",
        "value": "恢复中",
    }),
    "mineBattle_InterfaceCoreText3": _tools.RODict({
        "ID": "mineBattle_InterfaceCoreText3",
        "value": "下一占领战： {0}",
    }),
    "mineBattle_InterfaceCoreText4": _tools.RODict({
        "ID": "mineBattle_InterfaceCoreText4",
        "value": "占领倒计时： {0}",
    }),
    "mineBattle_InterfaceFlagText2": _tools.RODict({
        "ID": "mineBattle_InterfaceFlagText2",
        "value": "恢复倒计时： {0}",
    }),
    "mineBattle_dividendText": _tools.RODict({
        "ID": "mineBattle_dividendText",
        "value": "再次分红",
    }),
    "mineBattle_damageImmunityMsg": _tools.RODict({
        "ID": "mineBattle_damageImmunityMsg",
        "value": 54003201,
    }),
    "mineBattle_forbidTeleportMsg": _tools.RODict({
        "ID": "mineBattle_forbidTeleportMsg",
        "value": 54003202,
    }),
    "mineBattle_teleportSafeZoneMsg": _tools.RODict({
        "ID": "mineBattle_teleportSafeZoneMsg",
        "value": 54003203,
    }),
    "mineBattle_coreHpInsufficientMsg": _tools.RODict({
        "ID": "mineBattle_coreHpInsufficientMsg",
        "value": 54003204,
    }),
    "mineBattle_notAffiliationMsg": _tools.RODict({
        "ID": "mineBattle_notAffiliationMsg",
        "value": 54003205,
    }),
    "mineBattle_notPickableMsg": _tools.RODict({
        "ID": "mineBattle_notPickableMsg",
        "value": 54003206,
    }),
    "mineBattle_notEnoughStock": _tools.RODict({
        "ID": "mineBattle_notEnoughStock",
        "value": 54003207,
    }),
    "mineBatte_chatChannelMsg1": _tools.RODict({
        "ID": "mineBatte_chatChannelMsg1",
        "value": 58000201,
    }),
    "mineBatte_chatChannelMsg2": _tools.RODict({
        "ID": "mineBatte_chatChannelMsg2",
        "value": 58000202,
    }),
    "mineBatte_chatChannelMsg3": _tools.RODict({
        "ID": "mineBatte_chatChannelMsg3",
        "value": 58000203,
    }),
    "mineBatte_chatChannelMsg4": _tools.RODict({
        "ID": "mineBatte_chatChannelMsg4",
        "value": 58000204,
    }),
    "mineBatte_chatChannelMsg5": _tools.RODict({
        "ID": "mineBatte_chatChannelMsg5",
        "value": 58000205,
    }),
    "mineBatte_chatChannelMsg6": _tools.RODict({
        "ID": "mineBatte_chatChannelMsg6",
        "value": 58000206,
    }),
    "mineBatte_chatChannelMsg7": _tools.RODict({
        "ID": "mineBatte_chatChannelMsg7",
        "value": 58000207,
    }),
    "mineBatte_startMail": _tools.RODict({
        "ID": "mineBatte_startMail",
        "value": 37001017,
    }),
    "mineBatte_dividendMail": _tools.RODict({
        "ID": "mineBatte_dividendMail",
        "value": 37001018,
    }),
    "mineBatte_occupyMail": _tools.RODict({
        "ID": "mineBatte_occupyMail",
        "value": 37001019,
    }),
    "mineBatte_scoreRankMail": _tools.RODict({
        "ID": "mineBatte_scoreRankMail",
        "value": 37001020,
    })
})