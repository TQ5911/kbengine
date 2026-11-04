# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: guildTrain/guildTrainUpgrade
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    1: _tools.RODict({
        "ID": 1,
        "upgradeContributionCost": 300,
        "upgradeCoinCost": 10000,
        "yanWuGeLvReq": 1,
        "charLevelReq": 18
    }),
    2: _tools.RODict({
        "ID": 2,
        "upgradeContributionCost": 400,
        "upgradeCoinCost": 15000,
        "yanWuGeLvReq": 1,
        "charLevelReq": 18
    }),
    3: _tools.RODict({
        "ID": 3,
        "upgradeContributionCost": 550,
        "upgradeCoinCost": 20000,
        "yanWuGeLvReq": 1,
        "charLevelReq": 18
    }),
    4: _tools.RODict({
        "ID": 4,
        "upgradeContributionCost": 750,
        "upgradeCoinCost": 25000,
        "yanWuGeLvReq": 1,
        "charLevelReq": 20
    }),
    5: _tools.RODict({
        "ID": 5,
        "upgradeContributionCost": 1000,
        "upgradeCoinCost": 35000,
        "yanWuGeLvReq": 1,
        "charLevelReq": 24
    }),
    6: _tools.RODict({
        "ID": 6,
        "upgradeContributionCost": 1500,
        "upgradeCoinCost": 45000,
        "yanWuGeLvReq": 1,
        "charLevelReq": 28
    }),
    7: _tools.RODict({
        "ID": 7,
        "upgradeContributionCost": 2000,
        "upgradeCoinCost": 70000,
        "yanWuGeLvReq": 1,
        "charLevelReq": 32
    }),
    8: _tools.RODict({
        "ID": 8,
        "upgradeContributionCost": 2500,
        "upgradeCoinCost": 120000,
        "yanWuGeLvReq": 1,
        "charLevelReq": 34
    }),
    9: _tools.RODict({
        "ID": 9,
        "upgradeContributionCost": 3000,
        "upgradeCoinCost": 200000,
        "yanWuGeLvReq": 1,
        "charLevelReq": 36
    }),
    10: _tools.RODict({
        "ID": 10,
        "upgradeContributionCost": 3500,
        "upgradeCoinCost": 300000,
        "yanWuGeLvReq": 1,
        "charLevelReq": 38
    }),
    11: _tools.RODict({
        "ID": 11,
        "upgradeContributionCost": 4000,
        "upgradeCoinCost": 400000,
        "yanWuGeLvReq": 2,
        "charLevelReq": 40
    }),
    12: _tools.RODict({
        "ID": 12,
        "upgradeContributionCost": 4500,
        "upgradeCoinCost": 500000,
        "yanWuGeLvReq": 2,
        "charLevelReq": 42
    }),
    13: _tools.RODict({
        "ID": 13,
        "upgradeContributionCost": 5000,
        "upgradeCoinCost": 600000,
        "yanWuGeLvReq": 2,
        "charLevelReq": 44
    }),
    14: _tools.RODict({
        "ID": 14,
        "upgradeContributionCost": 5500,
        "upgradeCoinCost": 750000,
        "yanWuGeLvReq": 2,
        "charLevelReq": 46
    }),
    15: _tools.RODict({
        "ID": 15,
        "upgradeContributionCost": 6000,
        "upgradeCoinCost": 900000,
        "yanWuGeLvReq": 2,
        "charLevelReq": 48
    }),
    16: _tools.RODict({
        "ID": 16,
        "upgradeContributionCost": 6500,
        "upgradeCoinCost": 1050000,
        "yanWuGeLvReq": 2,
        "charLevelReq": 50
    }),
    17: _tools.RODict({
        "ID": 17,
        "upgradeContributionCost": 7000,
        "upgradeCoinCost": 1200000,
        "yanWuGeLvReq": 2,
        "charLevelReq": 52
    }),
    18: _tools.RODict({
        "ID": 18,
        "upgradeContributionCost": 7500,
        "upgradeCoinCost": 1350000,
        "yanWuGeLvReq": 2,
        "charLevelReq": 53
    }),
    19: _tools.RODict({
        "ID": 19,
        "upgradeContributionCost": 8000,
        "upgradeCoinCost": 1500000,
        "yanWuGeLvReq": 2,
        "charLevelReq": 54
    }),
    20: _tools.RODict({
        "ID": 20,
        "upgradeContributionCost": 8500,
        "upgradeCoinCost": 1650000,
        "yanWuGeLvReq": 2,
        "charLevelReq": 55
    }),
    21: _tools.RODict({
        "ID": 21,
        "upgradeContributionCost": 9000,
        "upgradeCoinCost": 1800000,
        "yanWuGeLvReq": 3,
        "charLevelReq": 56
    }),
    22: _tools.RODict({
        "ID": 22,
        "upgradeContributionCost": 9500,
        "upgradeCoinCost": 2000000,
        "yanWuGeLvReq": 3,
        "charLevelReq": 57
    }),
    23: _tools.RODict({
        "ID": 23,
        "upgradeContributionCost": 10000,
        "upgradeCoinCost": 2200000,
        "yanWuGeLvReq": 3,
        "charLevelReq": 58
    }),
    24: _tools.RODict({
        "ID": 24,
        "upgradeContributionCost": 10500,
        "upgradeCoinCost": 2400000,
        "yanWuGeLvReq": 3,
        "charLevelReq": 59
    }),
    25: _tools.RODict({
        "ID": 25,
        "upgradeContributionCost": 11000,
        "upgradeCoinCost": 2600000,
        "yanWuGeLvReq": 3,
        "charLevelReq": 60
    }),
    26: _tools.RODict({
        "ID": 26,
        "upgradeContributionCost": 11500,
        "upgradeCoinCost": 2800000,
        "yanWuGeLvReq": 3,
        "charLevelReq": 61
    }),
    27: _tools.RODict({
        "ID": 27,
        "upgradeContributionCost": 12000,
        "upgradeCoinCost": 3000000,
        "yanWuGeLvReq": 3,
        "charLevelReq": 62
    }),
    28: _tools.RODict({
        "ID": 28,
        "upgradeContributionCost": 12500,
        "upgradeCoinCost": 3200000,
        "yanWuGeLvReq": 3,
        "charLevelReq": 63
    }),
    29: _tools.RODict({
        "ID": 29,
        "upgradeContributionCost": 13000,
        "upgradeCoinCost": 3400000,
        "yanWuGeLvReq": 3,
        "charLevelReq": 64
    }),
    30: _tools.RODict({
        "ID": 30,
        "upgradeContributionCost": 13500,
        "upgradeCoinCost": 3600000,
        "yanWuGeLvReq": 3,
        "charLevelReq": 65
    }),
    31: _tools.RODict({
        "ID": 31,
        "upgradeContributionCost": 14000,
        "upgradeCoinCost": 3800000,
        "yanWuGeLvReq": 4,
        "charLevelReq": 66
    }),
    32: _tools.RODict({
        "ID": 32,
        "upgradeContributionCost": 14500,
        "upgradeCoinCost": 4000000,
        "yanWuGeLvReq": 4,
        "charLevelReq": 67
    }),
    33: _tools.RODict({
        "ID": 33,
        "upgradeContributionCost": 15000,
        "upgradeCoinCost": 4200000,
        "yanWuGeLvReq": 4,
        "charLevelReq": 68
    }),
    34: _tools.RODict({
        "ID": 34,
        "upgradeContributionCost": 15750,
        "upgradeCoinCost": 4400000,
        "yanWuGeLvReq": 4,
        "charLevelReq": 69
    }),
    35: _tools.RODict({
        "ID": 35,
        "upgradeContributionCost": 16500,
        "upgradeCoinCost": 4600000,
        "yanWuGeLvReq": 4,
        "charLevelReq": 70
    }),
    36: _tools.RODict({
        "ID": 36,
        "upgradeContributionCost": 17250,
        "upgradeCoinCost": 4800000,
        "yanWuGeLvReq": 5,
        "charLevelReq": 71
    }),
    37: _tools.RODict({
        "ID": 37,
        "upgradeContributionCost": 18000,
        "upgradeCoinCost": 5000000,
        "yanWuGeLvReq": 5,
        "charLevelReq": 72
    }),
    38: _tools.RODict({
        "ID": 38,
        "upgradeContributionCost": 18750,
        "upgradeCoinCost": 5500000,
        "yanWuGeLvReq": 5,
        "charLevelReq": 73
    }),
    39: _tools.RODict({
        "ID": 39,
        "upgradeContributionCost": 19500,
        "upgradeCoinCost": 6000000,
        "yanWuGeLvReq": 5,
        "charLevelReq": 74
    }),
    40: _tools.RODict({
        "ID": 40,
        "upgradeContributionCost": 20250,
        "upgradeCoinCost": 6500000,
        "yanWuGeLvReq": 5,
        "charLevelReq": 75
    })
})
minKey = 1
maxKey = 40