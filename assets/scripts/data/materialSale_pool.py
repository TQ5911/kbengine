# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: materialSale/pool
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    1001: _tools.RODict({
        "ID": 1001,
        "itemId": (30000224, 1),
        "groupID": 1,
        "discount": 8500,
        "weekQuota": 640,
        "isBind": 1,
        "floorPrice": 10,
        "minServerDay": 1,
        "status": 1,
        "guidePrice": 80,
        "dynamicStartDay": 4,
        "minLevel": 1,
    }),
    1002: _tools.RODict({
        "ID": 1002,
        "itemId": (30000227, 1),
        "groupID": 1,
        "discount": 8500,
        "weekQuota": 640,
        "isBind": 1,
        "floorPrice": 10,
        "minServerDay": 2,
        "status": 1,
        "guidePrice": 80,
        "dynamicStartDay": 5,
        "minLevel": 1,
    }),
    1003: _tools.RODict({
        "ID": 1003,
        "itemId": (30000231, 1),
        "groupID": 1,
        "discount": 8700,
        "weekQuota": 900,
        "isBind": 1,
        "floorPrice": 20,
        "minServerDay": 8,
        "status": 1,
        "guidePrice": 150,
        "dynamicStartDay": 11,
        "minLevel": 20,
    }),
    1004: _tools.RODict({
        "ID": 1004,
        "itemId": (30000280, 1),
        "groupID": 1,
        "discount": 8400,
        "weekQuota": 750,
        "isBind": 1,
        "floorPrice": 20,
        "minServerDay": 8,
        "status": 1,
        "guidePrice": 150,
        "dynamicStartDay": 11,
        "minLevel": 30,
    }),
    1005: _tools.RODict({
        "ID": 1005,
        "itemId": (30000225, 1),
        "groupID": 2,
        "discount": 7800,
        "weekQuota": 1400,
        "isBind": 1,
        "floorPrice": 30,
        "minServerDay": 8,
        "status": 1,
        "guidePrice": 350,
        "dynamicStartDay": 11,
        "minLevel": 30,
    }),
    1006: _tools.RODict({
        "ID": 1006,
        "itemId": (30000267, 1),
        "groupID": 2,
        "discount": 8000,
        "weekQuota": 300,
        "isBind": 1,
        "floorPrice": 10,
        "minServerDay": 8,
        "status": 1,
        "guidePrice": 30,
        "dynamicStartDay": 11,
        "minLevel": 35,
    }),
    1007: _tools.RODict({
        "ID": 1007,
        "itemId": (30000287, 1),
        "groupID": 2,
        "discount": 7800,
        "weekQuota": 400,
        "isBind": 1,
        "floorPrice": 10,
        "minServerDay": 15,
        "status": 1,
        "guidePrice": 50,
        "dynamicStartDay": 18,
        "minLevel": 40,
    }),
    1008: _tools.RODict({
        "ID": 1008,
        "itemId": (30000281, 1),
        "groupID": 2,
        "discount": 7600,
        "weekQuota": 3000,
        "isBind": 1,
        "floorPrice": 100,
        "minServerDay": 15,
        "status": 1,
        "guidePrice": 1000,
        "dynamicStartDay": 18,
        "minLevel": 45,
    }),
    1009: _tools.RODict({
        "ID": 1009,
        "itemId": (30000226, 1),
        "groupID": 3,
        "discount": 7200,
        "weekQuota": 1600,
        "isBind": 1,
        "floorPrice": 80,
        "minServerDay": 31,
        "status": 1,
        "guidePrice": 800,
        "dynamicStartDay": 34,
        "minLevel": 50,
    }),
    1010: _tools.RODict({
        "ID": 1010,
        "itemId": (30000271, 1),
        "groupID": 3,
        "discount": 7400,
        "weekQuota": 600,
        "isBind": 1,
        "floorPrice": 20,
        "minServerDay": 31,
        "status": 1,
        "guidePrice": 150,
        "dynamicStartDay": 34,
        "minLevel": 55,
    }),
    1011: _tools.RODict({
        "ID": 1011,
        "itemId": (30000291, 1),
        "groupID": 3,
        "discount": 7200,
        "weekQuota": 1350,
        "isBind": 1,
        "floorPrice": 40,
        "minServerDay": 31,
        "status": 1,
        "guidePrice": 450,
        "dynamicStartDay": 34,
        "minLevel": 55,
    }),
    1012: _tools.RODict({
        "ID": 1012,
        "itemId": (30000282, 1),
        "groupID": 3,
        "discount": 7000,
        "weekQuota": 3000,
        "isBind": 1,
        "floorPrice": 300,
        "minServerDay": 61,
        "status": 1,
        "guidePrice": 3000,
        "dynamicStartDay": 64,
        "minLevel": 65,
    })
})
minKey = 1001
maxKey = 1012

import materialSale_const as _MSC
import materialSale_quotaDate as _MSQD
import materialSale_quotaLevel as _MSQL

_RATE_BASE = 10000

def maxQuota(cfg, level, serverDay, cardRate):
    rate = _RATE_BASE + _MSQD.getBonus(cfg['groupID'], serverDay) + _MSQL.getBonus(cfg['groupID'], level) + cardRate
    return int(math.ceil(cfg['weekQuota'] * rate / float(_RATE_BASE)))

def unitPrice(cfg, avgPrice, lastPrice, serverDay):
    # 未到 dynamicStartDay 用指导价。到了以后用拍卖行昨日均价 * discount，
    # 不低于 floorPrice，且相对上一次售价的涨幅不超过 upLimitRate、跌幅不低于 downLimitRate。
    guide = int(cfg['guidePrice'])
    if serverDay < cfg['dynamicStartDay']:
        return guide

    discount = cfg['discount'] or _MSC.datas['defaultDiscount']['value']
    if avgPrice:
        price = int(math.ceil(float(avgPrice) * discount / float(_RATE_BASE)))
    else:
        price = guide
    floorPrice = int(cfg['floorPrice'])
    if price < floorPrice:
        price = floorPrice

    base = int(lastPrice) if lastPrice else guide
    if base > 0:
        upLimit = int(base * _MSC.datas['upLimitRate']['value'] / float(_RATE_BASE))
        downLimit = int(math.ceil(base * _MSC.datas['downLimitRate']['value'] / float(_RATE_BASE)))
        if price > upLimit:
            price = upLimit
        elif price < downLimit:
            price = downLimit
    if price < floorPrice:
        price = floorPrice
    return int(price)
