# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: welfare/config
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "serverLoginDurationMinLevel": _tools.RODict({
        "ID": "serverLoginDurationMinLevel",
        "value": 10,
    }),
    "SevenSignInSubtitle": _tools.RODict({
        "ID": "SevenSignInSubtitle",
        "value": "您已累计登录 {0} 天！",
    }),
    "SevenSignInsRewardTips1": _tools.RODict({
        "ID": "SevenSignInsRewardTips1",
        "value": "累计登录<size=80>7</size>天",
    }),
    "SevenSignInsRewardTips2": _tools.RODict({
        "ID": "SevenSignInsRewardTips2",
        "value": "赠送<color=#739cc9><size=42>蘑菇巫师</size></color>",
    }),
    "SevenSignInsRewardCard": _tools.RODict({
        "ID": "SevenSignInsRewardCard",
        "value": "Assets/Res/ui/texturenp/activities_image/activity_sign_bigreward_img.png",
    }),
    "TenSignTitle": _tools.RODict({
        "ID": "TenSignTitle",
        "value": "超多元宝天天领",
    }),
    "TenSignSubtitle": _tools.RODict({
        "ID": "TenSignSubtitle",
        "value": "每日登录即可领取绑定元宝",
    }),
    "TenSignRewardCard": _tools.RODict({
        "ID": "TenSignRewardCard",
        "value": "Assets/Res/ui/texturenp/activities_image/activity_sign_bigreward_img.png",
    }),
    "AttentionMethod": _tools.RODict({
        "ID": "AttentionMethod",
        "value": "第一步：关注官方公众号，发送口令\n“烽烟破晓”，领取专属兑换码。\n第二步：点击【兑换礼包】使用兑换码。",
    }),
    "AttentionReward": _tools.RODict({
        "ID": "AttentionReward",
        "value": 40000154,
    }),
    "AttentionAccounts": _tools.RODict({
        "ID": "AttentionAccounts",
        "value": "烽烟",
    }),
    "AttentionCopyMsg": _tools.RODict({
        "ID": "AttentionCopyMsg",
        "value": 54000381,
    }),
    "AttentionAccountsPic": _tools.RODict({
        "ID": "AttentionAccountsPic",
        "value": "Assets/Res/ui/texturenp/activities_image/attention_qr_img.png",
    }),
    "LevelRankDeadLine": _tools.RODict({
        "ID": "LevelRankDeadLine",
        "value": "202603270500",
    }),
    "LevelNotEnough": _tools.RODict({
        "ID": "LevelNotEnough",
        "value": 54000389,
    }),
    "LevelRankLimit": _tools.RODict({
        "ID": "LevelRankLimit",
        "value": _tools.ROList([100, 3000]),
    }),
    "PcLoginReward": _tools.RODict({
        "ID": "PcLoginReward",
        "value": 40000153,
    }),
    "wechatFailedJump": _tools.RODict({
        "ID": "wechatFailedJump",
        "value": 54000390,
    }),
    "resourceRecoveryTimeDes": _tools.RODict({
        "ID": "resourceRecoveryTimeDes",
        "value": "可找回<color=#038304>{0}</color>天内未使用的免费次数",
    }),
    "recoveryCostFree": _tools.RODict({
        "ID": "recoveryCostFree",
        "value": "免费找回",
    }),
    "recoveryNumCountDes": _tools.RODict({
        "ID": "recoveryNumCountDes",
        "value": "找回次数：{0}",
    }),
    "refundRechargeSubtitle": _tools.RODict({
        "ID": "refundRechargeSubtitle",
        "value": "高额返利 等你来领",
    }),
    "refundRechargeTips1": _tools.RODict({
        "ID": "refundRechargeTips1",
        "value": "充值 0 - 50000 元，返还 100% <#itemId={0}>和 20% <#itemId={1}>\n充值 50000 元以上，返还 100% <#itemId={0}>",
    }),
    "refundRechargeTips2": _tools.RODict({
        "ID": "refundRechargeTips2",
        "value": "已累计充值",
    }),
    "refundRechargeTips3": _tools.RODict({
        "ID": "refundRechargeTips3",
        "value": "公测最终返还",
    }),
    "refundRechargeItem1": _tools.RODict({
        "ID": "refundRechargeItem1",
        "value": "30000001",
    }),
    "refundRechargeItem2": _tools.RODict({
        "ID": "refundRechargeItem2",
        "value": "30000021",
    })
})