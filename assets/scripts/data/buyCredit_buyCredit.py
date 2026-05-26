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
        "name": "购买60元宝",
        "type": 1,
        "subType": 0,
        "price": 6,
        "priceID": 0,
        "quantity": 0,
        "VIPPoint": 6,
        "productID": "",
        "limitType": 0,
        "limitNumber": 0,
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
        "name": "购买300元宝",
        "type": 1,
        "subType": 0,
        "price": 30,
        "priceID": 0,
        "quantity": 0,
        "VIPPoint": 30,
        "productID": "",
        "limitType": 0,
        "limitNumber": 0,
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
        "name": "购买680元宝",
        "type": 1,
        "subType": 0,
        "price": 68,
        "priceID": 0,
        "quantity": 0,
        "VIPPoint": 68,
        "productID": "",
        "limitType": 0,
        "limitNumber": 0,
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
        "name": "购买1280元宝",
        "type": 1,
        "subType": 0,
        "price": 128,
        "priceID": 0,
        "quantity": 0,
        "VIPPoint": 128,
        "productID": "",
        "limitType": 0,
        "limitNumber": 0,
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
        "name": "购买3280元宝",
        "type": 1,
        "subType": 0,
        "price": 328,
        "priceID": 0,
        "quantity": 0,
        "VIPPoint": 328,
        "productID": "",
        "limitType": 0,
        "limitNumber": 0,
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
        "name": "购买6480元宝",
        "type": 1,
        "subType": 0,
        "price": 648,
        "priceID": 0,
        "quantity": 0,
        "VIPPoint": 648,
        "productID": "",
        "limitType": 0,
        "limitNumber": 0,
        "amount": 0,
        "credit": 6480,
        "firstBuyExRewardType": 30000001,
        "firstBuyExReward": 6480,
        "normalBuyExRewardType": 30000001,
        "normalBuyExReward": 1288,
        "reward": None
    }),
    68000101: _tools.RODict({
        "ID": 68000101,
        "name": "强化石礼包",
        "type": 7,
        "subType": 0,
        "price": 0,
        "priceID": 30000021,
        "quantity": 980,
        "VIPPoint": 0,
        "productID": "",
        "limitType": 3,
        "limitNumber": 1,
        "amount": 1,
        "credit": 0,
        "firstBuyExRewardType": 0,
        "firstBuyExReward": 0,
        "normalBuyExRewardType": 0,
        "normalBuyExReward": 0,
        "reward": _tools.ROList([40000158])
    }),
    68000102: _tools.RODict({
        "ID": 68000102,
        "name": "洗练石礼包",
        "type": 7,
        "subType": 0,
        "price": 0,
        "priceID": 30000021,
        "quantity": 980,
        "VIPPoint": 0,
        "productID": "",
        "limitType": 3,
        "limitNumber": 1,
        "amount": 1,
        "credit": 0,
        "firstBuyExRewardType": 0,
        "firstBuyExReward": 0,
        "normalBuyExRewardType": 0,
        "normalBuyExReward": 0,
        "reward": _tools.ROList([40000159])
    }),
    68000103: _tools.RODict({
        "ID": 68000103,
        "name": "铭文石礼包",
        "type": 7,
        "subType": 0,
        "price": 0,
        "priceID": 30000021,
        "quantity": 980,
        "VIPPoint": 0,
        "productID": "",
        "limitType": 3,
        "limitNumber": 1,
        "amount": 1,
        "credit": 0,
        "firstBuyExRewardType": 0,
        "firstBuyExReward": 0,
        "normalBuyExRewardType": 0,
        "normalBuyExReward": 0,
        "reward": _tools.ROList([40000160])
    }),
    68000104: _tools.RODict({
        "ID": 68000104,
        "name": "普通精灵礼包",
        "type": 7,
        "subType": 0,
        "price": 0,
        "priceID": 30000021,
        "quantity": 980,
        "VIPPoint": 0,
        "productID": "",
        "limitType": 3,
        "limitNumber": 1,
        "amount": 1,
        "credit": 0,
        "firstBuyExRewardType": 0,
        "firstBuyExReward": 0,
        "normalBuyExRewardType": 0,
        "normalBuyExReward": 0,
        "reward": _tools.ROList([40000161])
    }),
    68000105: _tools.RODict({
        "ID": 68000105,
        "name": "豪华精灵礼包",
        "type": 7,
        "subType": 0,
        "price": 0,
        "priceID": 30000021,
        "quantity": 1980,
        "VIPPoint": 0,
        "productID": "",
        "limitType": 3,
        "limitNumber": 1,
        "amount": 1,
        "credit": 0,
        "firstBuyExRewardType": 0,
        "firstBuyExReward": 0,
        "normalBuyExRewardType": 0,
        "normalBuyExReward": 0,
        "reward": _tools.ROList([40000162])
    }),
    68000106: _tools.RODict({
        "ID": 68000106,
        "name": "至尊精灵礼包",
        "type": 7,
        "subType": 0,
        "price": 0,
        "priceID": 30000021,
        "quantity": 2980,
        "VIPPoint": 0,
        "productID": "",
        "limitType": 3,
        "limitNumber": 1,
        "amount": 1,
        "credit": 0,
        "firstBuyExRewardType": 0,
        "firstBuyExReward": 0,
        "normalBuyExRewardType": 0,
        "normalBuyExReward": 0,
        "reward": _tools.ROList([40000163])
    }),
    68000107: _tools.RODict({
        "ID": 68000107,
        "name": "魔物征讨礼包",
        "type": 7,
        "subType": 0,
        "price": 0,
        "priceID": 30000021,
        "quantity": 980,
        "VIPPoint": 0,
        "productID": "",
        "limitType": 3,
        "limitNumber": 1,
        "amount": 1,
        "credit": 0,
        "firstBuyExRewardType": 0,
        "firstBuyExReward": 0,
        "normalBuyExRewardType": 0,
        "normalBuyExReward": 0,
        "reward": _tools.ROList([40000164])
    }),
    68000108: _tools.RODict({
        "ID": 68000108,
        "name": "时空之门礼包",
        "type": 7,
        "subType": 0,
        "price": 0,
        "priceID": 30000021,
        "quantity": 980,
        "VIPPoint": 0,
        "productID": "",
        "limitType": 3,
        "limitNumber": 1,
        "amount": 1,
        "credit": 0,
        "firstBuyExRewardType": 0,
        "firstBuyExReward": 0,
        "normalBuyExRewardType": 0,
        "normalBuyExReward": 0,
        "reward": _tools.ROList([40000165])
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
        "limitType": 0,
        "limitNumber": 0,
        "amount": 0,
        "credit": 0,
        "firstBuyExRewardType": 0,
        "firstBuyExReward": 0,
        "normalBuyExRewardType": 0,
        "normalBuyExReward": 0,
        "reward": _tools.ROList([40000156])
    }),
    68000301: _tools.RODict({
        "ID": 68000301,
        "name": "月卡1",
        "type": 2,
        "subType": 2,
        "price": 0,
        "priceID": 30000021,
        "quantity": 980,
        "VIPPoint": 0,
        "productID": "",
        "limitType": 0,
        "limitNumber": 0,
        "amount": 0,
        "credit": 0,
        "firstBuyExRewardType": 0,
        "firstBuyExReward": 0,
        "normalBuyExRewardType": 0,
        "normalBuyExReward": 0,
        "reward": _tools.ROList([40000156])
    })
})
minKey = 68000001
maxKey = 68000301

ProductIdDic = _tools.RODict({ 
})


BuyCreditMainTypeDic = _tools.RODict({ 
        1:[68000001, 68000002, 68000003, 68000004, 68000005, 68000006],
        2:[68000300, 68000301],
        7:[68000101, 68000102, 68000103, 68000104, 68000105, 68000106, 68000107, 68000108],
})


BuyCreditAllTypeDic = _tools.RODict({ 
        100:[68000001, 68000002, 68000003, 68000004, 68000005, 68000006],
        202:[68000300, 68000301],
        700:[68000101, 68000102, 68000103, 68000104, 68000105, 68000106, 68000107, 68000108],
})


TiyanMonthCardBuyCreditId = 0


JingdianMonthCardBuyCreditId = 68000301


DianCangMonthCardBuyCreditId = 0


LimitGiftMoneyList = _tools.ROList([])
