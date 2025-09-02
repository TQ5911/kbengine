# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: bagData/set
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "initCommonBagCapacity": _tools.RODict({
        "ID": "initCommonBagCapacity",
        "value": 200,
    }),
    "commonBagCapacity": _tools.RODict({
        "ID": "commonBagCapacity",
        "value": 250,
    }),
    "currencyBagCapacity": _tools.RODict({
        "ID": "currencyBagCapacity",
        "value": 30,
    }),
    "initBankCapacity": _tools.RODict({
        "ID": "initBankCapacity",
        "value": 100,
    }),
    "bankCapacity": _tools.RODict({
        "ID": "bankCapacity",
        "value": 150,
    }),
    "itemBatchUseUpLimit": _tools.RODict({
        "ID": "itemBatchUseUpLimit",
        "value": 99,
    }),
    "bagFullItemTips": _tools.RODict({
        "ID": "bagFullItemTips",
        "value": 54000010,
    }),
    "bagReorgCD": _tools.RODict({
        "ID": "bagReorgCD",
        "value": 10,
    }),
    "bagExpansionCoinUsageLimit_msgID": _tools.RODict({
        "ID": "bagExpansionCoinUsageLimit_msgID",
        "value": 54000025,
    }),
    "bagExpansionSuccess_msgID": _tools.RODict({
        "ID": "bagExpansionSuccess_msgID",
        "value": 54000026,
    }),
    "noCheckedConditions_msgID": _tools.RODict({
        "ID": "noCheckedConditions_msgID",
        "value": 54000034,
    }),
    "noEligibleItems_msgID": _tools.RODict({
        "ID": "noEligibleItems_msgID",
        "value": 54000035,
    }),
    "autoSelectSales": _tools.RODict({
        "ID": "autoSelectSales",
        "value": 20,
    }),
    "cantSelectToAutoSaleMsg": _tools.RODict({
        "ID": "cantSelectToAutoSaleMsg",
        "value": 54000138,
    }),
    "autoSelectQuality": _tools.RODict({
        "ID": "autoSelectQuality",
        "value": 2,
    }),
    "autoGearDisassembleQuality": _tools.RODict({
        "ID": "autoGearDisassembleQuality",
        "value": 2,
    }),
    "putInFail_bankFull_msg": _tools.RODict({
        "ID": "putInFail_bankFull_msg",
        "value": 54000164,
    }),
    "takeOutFail_bagFull_msg": _tools.RODict({
        "ID": "takeOutFail_bagFull_msg",
        "value": 54000165,
    }),
    "putInFail_itemLimited_msg": _tools.RODict({
        "ID": "putInFail_itemLimited_msg",
        "value": 54000166,
    }),
    "bankExpansionCoinUsageLimit_msgID": _tools.RODict({
        "ID": "bankExpansionCoinUsageLimit_msgID",
        "value": 54000198,
    }),
    "bankExpansionSuccess_msgID": _tools.RODict({
        "ID": "bankExpansionSuccess_msgID",
        "value": 54000199,
    }),
    "bagItemAuctionCD": _tools.RODict({
        "ID": "bagItemAuctionCD",
        "value": "交易冷却期：{0}",
    }),
    "bagItemLimitTimeCD": _tools.RODict({
        "ID": "bagItemLimitTimeCD",
        "value": "过期删除：{0}",
    })
})