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
        "value": _tools.ROList([1028, 1123]),
    }),
    "mineBattle_miningSafeArea": _tools.RODict({
        "ID": "mineBattle_miningSafeArea",
        "value": "{1028:1024, 1123:1122}",
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
    "mineBattle_recoveryRatio": _tools.RODict({
        "ID": "mineBattle_recoveryRatio",
        "value": _tools.ROList([0.001, 0.005]),
    }),
    "mineBattle_coreInvincibleBuffID": _tools.RODict({
        "ID": "mineBattle_coreInvincibleBuffID",
        "value": 64007002,
    }),
    "mineBattle_coreRecoverBuffID": _tools.RODict({
        "ID": "mineBattle_coreRecoverBuffID",
        "value": 64007001,
    }),
    "mineBattle_flagRecoverBuffID": _tools.RODict({
        "ID": "mineBattle_flagRecoverBuffID",
        "value": 64007005,
    }),
    "mineBattle_damageScore": _tools.RODict({
        "ID": "mineBattle_damageScore",
        "value": 10000,
    }),
    "mineBattle_lastHitScore": _tools.RODict({
        "ID": "mineBattle_lastHitScore",
        "value": 2000,
    }),
    "mineBattle_killScore": _tools.RODict({
        "ID": "mineBattle_killScore",
        "value": _tools.ROList([50, 150]),
    }),
    "mineBattle_takePartScore": _tools.RODict({
        "ID": "mineBattle_takePartScore",
        "value": _tools.ROList([30, 5, 300]),
    }),
    "mineBattle_rankScoreThreshold": _tools.RODict({
        "ID": "mineBattle_rankScoreThreshold",
        "value": 300,
    }),
    "mineBattle_rewardThreshold": _tools.RODict({
        "ID": "mineBattle_rewardThreshold",
        "value": 300,
    }),
    "mineBattle_rewardParticipation": _tools.RODict({
        "ID": "mineBattle_rewardParticipation",
        "value": 30000542,
    }),
    "mineBattle_miningPersonalDuration": _tools.RODict({
        "ID": "mineBattle_miningPersonalDuration",
        "value": _tools.ROList([30, 60]),
    }),
    "mineBattle_incomeCoefficient": _tools.RODict({
        "ID": "mineBattle_incomeCoefficient",
        "value": 1.5,
    }),
    "mineBattle_MoneyID": _tools.RODict({
        "ID": "mineBattle_MoneyID",
        "value": 30000013,
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
        "value": _tools.ROList([3, 50]),
    }),
    "mineBatte_rankPersonNum": _tools.RODict({
        "ID": "mineBatte_rankPersonNum",
        "value": 50,
    }),
    "mineBatte_rankGuildNum": _tools.RODict({
        "ID": "mineBatte_rankGuildNum",
        "value": 20,
    }),
    "mineBattle_coreTempletId": _tools.RODict({
        "ID": "mineBattle_coreTempletId",
        "value": 11238019,
    }),
    "mineBattle_flagDropCollectionId": _tools.RODict({
        "ID": "mineBattle_flagDropCollectionId",
        "value": _tools.ROList([16006068]),
    }),
    "mineBatte_neutralMiningAreaCoreProp": _tools.RODict({
        "ID": "mineBatte_neutralMiningAreaCoreProp",
        "value": _tools.ROList([52004021, 52004021]),
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
    "mineBattle_rewardRankDesc": _tools.RODict({
        "ID": "mineBattle_rewardRankDesc",
        "value": "个人积分达到{0}可入榜",
    }),
    "mineBattle_rewardParticipationDesc": _tools.RODict({
        "ID": "mineBattle_rewardParticipationDesc",
        "value": "个人积分达到{0}可获得参与奖",
    }),
    "mineBattle_occupationTips": _tools.RODict({
        "ID": "mineBattle_occupationTips",
        "value": "成功占领{0}矿区",
    }),
    "mineBattle_occupationTimeText": _tools.RODict({
        "ID": "mineBattle_occupationTimeText",
        "value": "占领第{0}天",
    }),
    "mineBattle_occupyMsg": _tools.RODict({
        "ID": "mineBattle_occupyMsg",
        "value": "欢迎来到[{0}]的帮会领地",
    }),
    "mineBattle_guildRankDesc": _tools.RODict({
        "ID": "mineBattle_guildRankDesc",
        "value": "每占领30秒可获得1%的额外挖矿收益，最高上限50%，获得矿区归属权的帮会直接获得50%额外收益",
    }),
    "mineBattle_noGuildName": _tools.RODict({
        "ID": "mineBattle_noGuildName",
        "value": "无",
    }),
    "mineBattle_flagResPath": _tools.RODict({
        "ID": "mineBattle_flagResPath",
        "value": "2010_00_qizhi",
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
    "mineBattle_noDividend": _tools.RODict({
        "ID": "mineBattle_noDividend",
        "value": 54003208,
    }),
    "mineBattle_noEnoughTime": _tools.RODict({
        "ID": "mineBattle_noEnoughTime",
        "value": 54003209,
    }),
    "mineBattle_dividendSuccessMsg": _tools.RODict({
        "ID": "mineBattle_dividendSuccessMsg",
        "value": 54003210,
    }),
    "mineBattle_dividendSuccessMsg2": _tools.RODict({
        "ID": "mineBattle_dividendSuccessMsg2",
        "value": 54003211,
    }),
    "mineBattle_dividendInputMsg": _tools.RODict({
        "ID": "mineBattle_dividendInputMsg",
        "value": 54003212,
    }),
    "mineBattle_prohibitAttacksMsg": _tools.RODict({
        "ID": "mineBattle_prohibitAttacksMsg",
        "value": 54003213,
    }),
    "mineBattle_prohibitExit": _tools.RODict({
        "ID": "mineBattle_prohibitExit",
        "value": 54003214,
    })
})