# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: buyCredit/buyCreditConst
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "buyCredit_fail_msg": _tools.RODict({
        "ID": "buyCredit_fail_msg",
        "value": 54001698,
    }),
    "buyCredit_package_success": _tools.RODict({
        "ID": "buyCredit_package_success",
        "value": 54001701,
    }),
    "buyCredit_package_fail": _tools.RODict({
        "ID": "buyCredit_package_fail",
        "value": 54001702,
    }),
    "buyCredit_payTooBusy": _tools.RODict({
        "ID": "buyCredit_payTooBusy",
        "value": 54001703,
    }),
    "holidayGift_overdue_msgID": _tools.RODict({
        "ID": "holidayGift_overdue_msgID",
        "value": 54001699,
    }),
    "holidayGift_overLimitBuyTime_msgID": _tools.RODict({
        "ID": "holidayGift_overLimitBuyTime_msgID",
        "value": 54001700,
    }),
    "recommendGiftConfig": _tools.RODict({
        "ID": "recommendGiftConfig",
        "value": (68000101, 68000102, 68000103, 68000104, 68000105, 68000106, 68000107, 68000108),
    }),
    "singlePurchaseLimit3_msg": _tools.RODict({
        "ID": "singlePurchaseLimit3_msg",
        "value": 54000157,
    }),
    "monthlyLimit3_msg": _tools.RODict({
        "ID": "monthlyLimit3_msg",
        "value": 54000158,
    }),
    "buyCredit_success_msg": _tools.RODict({
        "ID": "buyCredit_success_msg",
        "value": 54000038,
    }),
    "buyGiftConfirm_msg": _tools.RODict({
        "ID": "buyGiftConfirm_msg",
        "value": 54000098,
    }),
    "buyGiftSuccess_msg": _tools.RODict({
        "ID": "buyGiftSuccess_msg",
        "value": 54000122,
    }),
    "amountFormat": _tools.RODict({
        "ID": "amountFormat",
        "value": "限购{0}/{1}",
    }),
    "moreFormat": _tools.RODict({
        "ID": "moreFormat",
        "value": "超值{0}%",
    }),
    "rmbFirstFormat": _tools.RODict({
        "ID": "rmbFirstFormat",
        "value": "x{0}",
    }),
    "rmbNextFormat": _tools.RODict({
        "ID": "rmbNextFormat",
        "value": "x{0}",
    }),
    "rmbFormat": _tools.RODict({
        "ID": "rmbFormat",
        "value": "￥{0}",
    }),
    "itemActivate": _tools.RODict({
        "ID": "itemActivate",
        "value": 30000312,
    }),
    "durationHours": _tools.RODict({
        "ID": "durationHours",
        "value": 720,
    }),
    "durationHoursLimit": _tools.RODict({
        "ID": "durationHoursLimit",
        "value": 4297,
    }),
    "durationHoursLimitMsg": _tools.RODict({
        "ID": "durationHoursLimitMsg",
        "value": 54001697,
    }),
    "dailyRewards": _tools.RODict({
        "ID": "dailyRewards",
        "value": 40000157,
    }),
    "dailyBaseTime": _tools.RODict({
        "ID": "dailyBaseTime",
        "value": 480,
    }),
    "offlineTimeLimit": _tools.RODict({
        "ID": "offlineTimeLimit",
        "value": 5,
    }),
    "coinActivate": _tools.RODict({
        "ID": "coinActivate",
        "value": 54001704,
    }),
    "monthCard": _tools.RODict({
        "ID": "monthCard",
        "value": "MonthCard",
    }),
    "limitText": _tools.RODict({
        "ID": "limitText",
        "value": ('终生限购', '日限购', '周限购', '月限购'),
    }),
    "rmbSwitch": _tools.RODict({
        "ID": "rmbSwitch",
        "value": 1,
    }),
    "rmbSymbol": _tools.RODict({
        "ID": "rmbSymbol",
        "value": "Assets/Res/ui/texture/common/com_money_icon.png",
    }),
    "limitedTime": _tools.RODict({
        "ID": "limitedTime",
        "value": "限时上架至{0}",
    }),
    "webTopUp": _tools.RODict({
        "ID": "webTopUp",
        "value": 54000270,
    }),
    "monthCardFailedMail": _tools.RODict({
        "ID": "monthCardFailedMail",
        "value": 37000031,
    }),
    "monthCardDailyMail": _tools.RODict({
        "ID": "monthCardDailyMail",
        "value": 37000032,
    }),
    "miniMonthlyPassPerks": _tools.RODict({
        "ID": "miniMonthlyPassPerks",
        "value": ('开通月卡解锁可交易道具获取资格，及交易行上架资格', '可交易道具掉落额外增加战力排行加成', '周礼包专享绑元购买 及 史诗精灵召唤券绑元购买'),
    }),
    "premiumMonthlyPassPerks": _tools.RODict({
        "ID": "premiumMonthlyPassPerks",
        "value": ('挂机时长8小时增加到16小时，并可获得道具奖励', '可交易道具掉落概率+10% (购买赤铜月卡后生效)', '材料特供专享绑元购买，且购买次数增加 '),
    }),
    "monthCardRenew": _tools.RODict({
        "ID": "monthCardRenew",
        "value": "续购",
    }),
    "monthCardActive": _tools.RODict({
        "ID": "monthCardActive",
        "value": "激活",
    }),
    "rechargeSuccess": _tools.RODict({
        "ID": "rechargeSuccess",
        "value": 54002400,
    }),
    "cancelPayment": _tools.RODict({
        "ID": "cancelPayment",
        "value": 54002401,
    }),
    "paymentTimeout": _tools.RODict({
        "ID": "paymentTimeout",
        "value": 54002402,
    }),
    "paySendLimit": _tools.RODict({
        "ID": "paySendLimit",
        "value": 54002403,
    }),
    "iOSNotOpenYet": _tools.RODict({
        "ID": "iOSNotOpenYet",
        "value": 54002404,
    }),
    "monthlyExclusive": _tools.RODict({
        "ID": "monthlyExclusive",
        "value": 54002405,
    }),
    "itemOffShelf": _tools.RODict({
        "ID": "itemOffShelf",
        "value": 54002406,
    }),
    "buyLimitReached": _tools.RODict({
        "ID": "buyLimitReached",
        "value": 54002407,
    }),
    "createOrderError": _tools.RODict({
        "ID": "createOrderError",
        "value": 54002408,
    }),
    "paymentFailed": _tools.RODict({
        "ID": "paymentFailed",
        "value": 54002409,
    }),
    "paymentFailedKefu": _tools.RODict({
        "ID": "paymentFailedKefu",
        "value": 54002410,
    }),
    "paymentFailedClose": _tools.RODict({
        "ID": "paymentFailedClose",
        "value": 54002411,
    })
})