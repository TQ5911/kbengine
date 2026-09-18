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
        "value": 100,
    }),
    "commonBagCapacity": _tools.RODict({
        "ID": "commonBagCapacity",
        "value": 300,
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
        "value": 200,
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
    "bagExpansionOverflow_msgID": _tools.RODict({
        "ID": "bagExpansionOverflow_msgID",
        "value": 54000382,
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
    "autoResolveOn": _tools.RODict({
        "ID": "autoResolveOn",
        "value": 54001100,
    }),
    "autoResolveOff": _tools.RODict({
        "ID": "autoResolveOff",
        "value": 54001102,
    }),
    "autoResolveDefault": _tools.RODict({
        "ID": "autoResolveDefault",
        "value": 54001103,
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
    "bankExpansionOverflow_msgID": _tools.RODict({
        "ID": "bankExpansionOverflow_msgID",
        "value": 54000383,
    }),
    "bagItemLimitTimeCD": _tools.RODict({
        "ID": "bagItemLimitTimeCD",
        "value": "过期删除：{0}",
    }),
    "autoSelectQualityList": _tools.RODict({
        "ID": "autoSelectQualityList",
        "value": _tools.ROList([1, 2]),
    }),
    "autoGearDisassembleQualityList": _tools.RODict({
        "ID": "autoGearDisassembleQualityList",
        "value": _tools.ROList([1, 2]),
    }),
    "bagToStorage": _tools.RODict({
        "ID": "bagToStorage",
        "value": "放入仓库",
    }),
    "storageToBag": _tools.RODict({
        "ID": "storageToBag",
        "value": "放入背包",
    }),
    "storageInteract1": _tools.RODict({
        "ID": "storageInteract1",
        "value": "点击全部移动",
    }),
    "storageInteract2": _tools.RODict({
        "ID": "storageInteract2",
        "value": "点击单个移动",
    }),
    "storageInteract3": _tools.RODict({
        "ID": "storageInteract3",
        "value": "点击预览",
    }),
    "bankForbiddenList": _tools.RODict({
        "ID": "bankForbiddenList",
        "value": (30010022, 30990151, 30990158, 30990159, 30990169, 30990170, 30990189, 30990160, 30990161, 30990166, 30990167, 30990168, 30990172),
    })
})