# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: buyCredit/buyCredit
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    68000001: _tools.RODict({
        "ID": 68000001,
        "name": "购买60金币",
        "type": 1,
        "subType": 0,
        "price": 6,
        "priceID": 0,
        "quantity": 0,
        "VIPPoint": 6,
        "productID": "",
        "amount": 0,
        "credit": 60,
        "firstBuyExRewardType": 30000001,
        "firstBuyExReward": 60,
        "normalBuyExRewardType": 30000001,
        "normalBuyExReward": 6,
        "reward": None
    }),
    68000002: _tools.RODict({
        "ID": 68000002,
        "name": "购买300金币",
        "type": 1,
        "subType": 0,
        "price": 30,
        "priceID": 0,
        "quantity": 0,
        "VIPPoint": 30,
        "productID": "",
        "amount": 0,
        "credit": 300,
        "firstBuyExRewardType": 30000001,
        "firstBuyExReward": 300,
        "normalBuyExRewardType": 30000001,
        "normalBuyExReward": 33,
        "reward": None
    }),
    68000003: _tools.RODict({
        "ID": 68000003,
        "name": "购买680金币",
        "type": 1,
        "subType": 0,
        "price": 68,
        "priceID": 0,
        "quantity": 0,
        "VIPPoint": 68,
        "productID": "",
        "amount": 0,
        "credit": 680,
        "firstBuyExRewardType": 30000001,
        "firstBuyExReward": 680,
        "normalBuyExRewardType": 30000001,
        "normalBuyExReward": 78,
        "reward": None
    }),
    68000004: _tools.RODict({
        "ID": 68000004,
        "name": "购买1280金币",
        "type": 1,
        "subType": 0,
        "price": 128,
        "priceID": 0,
        "quantity": 0,
        "VIPPoint": 128,
        "productID": "",
        "amount": 0,
        "credit": 1280,
        "firstBuyExRewardType": 30000001,
        "firstBuyExReward": 1280,
        "normalBuyExRewardType": 30000001,
        "normalBuyExReward": 178,
        "reward": None
    }),
    68000005: _tools.RODict({
        "ID": 68000005,
        "name": "购买3280金币",
        "type": 1,
        "subType": 0,
        "price": 328,
        "priceID": 0,
        "quantity": 0,
        "VIPPoint": 328,
        "productID": "",
        "amount": 0,
        "credit": 3280,
        "firstBuyExRewardType": 30000001,
        "firstBuyExReward": 3280,
        "normalBuyExRewardType": 30000001,
        "normalBuyExReward": 518,
        "reward": None
    }),
    68000006: _tools.RODict({
        "ID": 68000006,
        "name": "购买6480金币",
        "type": 1,
        "subType": 0,
        "price": 648,
        "priceID": 0,
        "quantity": 0,
        "VIPPoint": 648,
        "productID": "",
        "amount": 0,
        "credit": 6480,
        "firstBuyExRewardType": 30000001,
        "firstBuyExReward": 6480,
        "normalBuyExRewardType": 30000001,
        "normalBuyExReward": 1288,
        "reward": None
    }),
    68000100: _tools.RODict({
        "ID": 68000100,
        "name": "初见之礼",
        "type": 8,
        "subType": 0,
        "price": 0,
        "priceID": 0,
        "quantity": 0,
        "VIPPoint": 0,
        "productID": "",
        "amount": 1,
        "credit": 0,
        "firstBuyExRewardType": 0,
        "firstBuyExReward": 0,
        "normalBuyExRewardType": 0,
        "normalBuyExReward": 0,
        "reward": _tools.ROList([40000012])
    }),
    68000101: _tools.RODict({
        "ID": 68000101,
        "name": "推荐礼包1",
        "type": 7,
        "subType": 0,
        "price": 6,
        "priceID": 0,
        "quantity": 0,
        "VIPPoint": 6,
        "productID": "",
        "amount": 1,
        "credit": 0,
        "firstBuyExRewardType": 0,
        "firstBuyExReward": 0,
        "normalBuyExRewardType": 0,
        "normalBuyExReward": 0,
        "reward": _tools.ROList([40000013])
    }),
    68000102: _tools.RODict({
        "ID": 68000102,
        "name": "推荐礼包2",
        "type": 7,
        "subType": 0,
        "price": 30,
        "priceID": 0,
        "quantity": 0,
        "VIPPoint": 30,
        "productID": "",
        "amount": 1,
        "credit": 0,
        "firstBuyExRewardType": 0,
        "firstBuyExReward": 0,
        "normalBuyExRewardType": 0,
        "normalBuyExReward": 0,
        "reward": _tools.ROList([40000014])
    }),
    68000200: _tools.RODict({
        "ID": 68000200,
        "name": "节日礼包1",
        "type": 10,
        "subType": 0,
        "price": 68,
        "priceID": 0,
        "quantity": 0,
        "VIPPoint": 68,
        "productID": "",
        "amount": 3,
        "credit": 0,
        "firstBuyExRewardType": 0,
        "firstBuyExReward": 0,
        "normalBuyExRewardType": 0,
        "normalBuyExReward": 0,
        "reward": _tools.ROList([40000015])
    }),
    68000201: _tools.RODict({
        "ID": 68000201,
        "name": "节日礼包2",
        "type": 10,
        "subType": 0,
        "price": 128,
        "priceID": 0,
        "quantity": 0,
        "VIPPoint": 128,
        "productID": "",
        "amount": 3,
        "credit": 0,
        "firstBuyExRewardType": 0,
        "firstBuyExReward": 0,
        "normalBuyExRewardType": 0,
        "normalBuyExReward": 0,
        "reward": _tools.ROList([40000016])
    }),
    68000202: _tools.RODict({
        "ID": 68000202,
        "name": "节日礼包3",
        "type": 10,
        "subType": 0,
        "price": 328,
        "priceID": 0,
        "quantity": 0,
        "VIPPoint": 328,
        "productID": "",
        "amount": 3,
        "credit": 0,
        "firstBuyExRewardType": 0,
        "firstBuyExReward": 0,
        "normalBuyExRewardType": 0,
        "normalBuyExReward": 0,
        "reward": _tools.ROList([40000017])
    }),
    68000300: _tools.RODict({
        "ID": 68000300,
        "name": "月卡1",
        "type": 2,
        "subType": 2,
        "price": 98,
        "priceID": 0,
        "quantity": 0,
        "VIPPoint": 98,
        "productID": "",
        "amount": 0,
        "credit": 0,
        "firstBuyExRewardType": 0,
        "firstBuyExReward": 0,
        "normalBuyExRewardType": 0,
        "normalBuyExReward": 0,
        "reward": _tools.ROList([40000015])
    }),
    68000301: _tools.RODict({
        "ID": 68000301,
        "name": "月卡1",
        "type": 2,
        "subType": 2,
        "price": 0,
        "priceID": 30000001,
        "quantity": 980,
        "VIPPoint": 0,
        "productID": "",
        "amount": 0,
        "credit": 0,
        "firstBuyExRewardType": 0,
        "firstBuyExReward": 0,
        "normalBuyExRewardType": 0,
        "normalBuyExReward": 0,
        "reward": _tools.ROList([40000015])
    })
})
minKey = 68000001
maxKey = 68000301

ProductIdDic = _tools.RODict({ 
})


BuyCreditMainTypeDic = _tools.RODict({ 
        1:[68000001, 68000002, 68000003, 68000004, 68000005, 68000006],
        2:[68000300, 68000301],
        7:[68000101, 68000102],
        8:[68000100],
        10:[68000200, 68000201, 68000202],
})


BuyCreditAllTypeDic = _tools.RODict({ 
        100:[68000001, 68000002, 68000003, 68000004, 68000005, 68000006],
        202:[68000300, 68000301],
        700:[68000101, 68000102],
        800:[68000100],
        1000:[68000200, 68000201, 68000202],
})


TiyanMonthCardBuyCreditId = 0


JingdianMonthCardBuyCreditId = 68000301


DianCangMonthCardBuyCreditId = 0


LimitGiftMoneyList = _tools.ROList([])
