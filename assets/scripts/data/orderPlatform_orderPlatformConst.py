# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: orderPlatform/orderPlatformConst
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "orderPlatformTaxRate": _tools.RODict({
        "key": "orderPlatformTaxRate",
        "value": "10",
        "type": "int"
    }),
    "taxRateTip": _tools.RODict({
        "key": "taxRateTip",
        "value": "已扣除手续费{0}%",
        "type": "string"
    }),
    "tradeRecordRetention": _tools.RODict({
        "key": "tradeRecordRetention",
        "value": "100",
        "type": "int"
    }),
    "purchaseConfirm": _tools.RODict({
        "key": "purchaseConfirm",
        "value": "54000235",
        "type": "uint"
    }),
    "buyItemSuccessMsg": _tools.RODict({
        "key": "buyItemSuccessMsg",
        "value": "54000241",
        "type": "uint"
    }),
    "putawayConfirm": _tools.RODict({
        "key": "putawayConfirm",
        "value": "54000190",
        "type": "uint"
    }),
    "subscriptionSuccessful": _tools.RODict({
        "key": "subscriptionSuccessful",
        "value": "54000316",
        "type": "uint"
    }),
    "partialMatchSuccess": _tools.RODict({
        "key": "partialMatchSuccess",
        "value": "54000317",
        "type": "uint"
    }),
    "subscriptionFailed": _tools.RODict({
        "key": "subscriptionFailed",
        "value": "54000318",
        "type": "uint"
    }),
    "dynamicPriceStatCount": _tools.RODict({
        "key": "dynamicPriceStatCount",
        "value": "200",
        "type": "uint"
    }),
    "dynamicPriceBaseValue": _tools.RODict({
        "key": "dynamicPriceBaseValue",
        "value": "50",
        "type": "uint"
    }),
    "priceRefreshInterval": _tools.RODict({
        "key": "priceRefreshInterval",
        "value": "60",
        "type": "uint"
    }),
    "priceRefreshTip": _tools.RODict({
        "key": "priceRefreshTip",
        "value": "交易行成交量不足，无法更新当前价格",
        "type": "string"
    }),
    "limitText": _tools.RODict({
        "key": "limitText",
        "value": "\"终生限购\",\"日限购\",\"周限购\",\"月限购\",\"\",\"限购\"",
        "type": "stringlist"
    }),
    "subscription": _tools.RODict({
        "key": "subscription",
        "value": "认购",
        "type": "string"
    }),
    "confirmSubscription": _tools.RODict({
        "key": "confirmSubscription",
        "value": "确定认购",
        "type": "string"
    }),
    "subscriptionStatus": _tools.RODict({
        "key": "subscriptionStatus",
        "value": "\"可认购\",\"已认购\"",
        "type": "stringlist"
    })
})