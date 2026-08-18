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
        "upgradeContributionCost": 400,
        "upgradeCoinCost": 10000,
        "yanWuGeLvReq": 1,
        "charLevelReq": 18
    }),
    2: _tools.RODict({
        "ID": 2,
        "upgradeContributionCost": 450,
        "upgradeCoinCost": 15000,
        "yanWuGeLvReq": 1,
        "charLevelReq": 18
    }),
    3: _tools.RODict({
        "ID": 3,
        "upgradeContributionCost": 500,
        "upgradeCoinCost": 20000,
        "yanWuGeLvReq": 1,
        "charLevelReq": 18
    }),
    4: _tools.RODict({
        "ID": 4,
        "upgradeContributionCost": 550,
        "upgradeCoinCost": 25000,
        "yanWuGeLvReq": 1,
        "charLevelReq": 20
    }),
    5: _tools.RODict({
        "ID": 5,
        "upgradeContributionCost": 600,
        "upgradeCoinCost": 30000,
        "yanWuGeLvReq": 1,
        "charLevelReq": 25
    }),
    6: _tools.RODict({
        "ID": 6,
        "upgradeContributionCost": 1000,
        "upgradeCoinCost": 40000,
        "yanWuGeLvReq": 1,
        "charLevelReq": 30
    }),
    7: _tools.RODict({
        "ID": 7,
        "upgradeContributionCost": 1500,
        "upgradeCoinCost": 60000,
        "yanWuGeLvReq": 1,
        "charLevelReq": 33
    }),
    8: _tools.RODict({
        "ID": 8,
        "upgradeContributionCost": 2000,
        "upgradeCoinCost": 100000,
        "yanWuGeLvReq": 1,
        "charLevelReq": 36
    }),
    9: _tools.RODict({
        "ID": 9,
        "upgradeContributionCost": 2500,
        "upgradeCoinCost": 200000,
        "yanWuGeLvReq": 1,
        "charLevelReq": 39
    }),
    10: _tools.RODict({
        "ID": 10,
        "upgradeContributionCost": 3000,
        "upgradeCoinCost": 300000,
        "yanWuGeLvReq": 1,
        "charLevelReq": 42
    }),
    11: _tools.RODict({
        "ID": 11,
        "upgradeContributionCost": 3500,
        "upgradeCoinCost": 400000,
        "yanWuGeLvReq": 2,
        "charLevelReq": 45
    }),
    12: _tools.RODict({
        "ID": 12,
        "upgradeContributionCost": 4000,
        "upgradeCoinCost": 500000,
        "yanWuGeLvReq": 2,
        "charLevelReq": 48
    }),
    13: _tools.RODict({
        "ID": 13,
        "upgradeContributionCost": 4500,
        "upgradeCoinCost": 600000,
        "yanWuGeLvReq": 2,
        "charLevelReq": 50
    }),
    14: _tools.RODict({
        "ID": 14,
        "upgradeContributionCost": 5000,
        "upgradeCoinCost": 700000,
        "yanWuGeLvReq": 2,
        "charLevelReq": 52
    }),
    15: _tools.RODict({
        "ID": 15,
        "upgradeContributionCost": 5750,
        "upgradeCoinCost": 800000,
        "yanWuGeLvReq": 2,
        "charLevelReq": 54
    }),
    16: _tools.RODict({
        "ID": 16,
        "upgradeContributionCost": 6500,
        "upgradeCoinCost": 900000,
        "yanWuGeLvReq": 2,
        "charLevelReq": 56
    }),
    17: _tools.RODict({
        "ID": 17,
        "upgradeContributionCost": 7250,
        "upgradeCoinCost": 1000000,
        "yanWuGeLvReq": 2,
        "charLevelReq": 58
    }),
    18: _tools.RODict({
        "ID": 18,
        "upgradeContributionCost": 8000,
        "upgradeCoinCost": 1100000,
        "yanWuGeLvReq": 2,
        "charLevelReq": 60
    }),
    19: _tools.RODict({
        "ID": 19,
        "upgradeContributionCost": 8750,
        "upgradeCoinCost": 1200000,
        "yanWuGeLvReq": 2,
        "charLevelReq": 62
    }),
    20: _tools.RODict({
        "ID": 20,
        "upgradeContributionCost": 9500,
        "upgradeCoinCost": 1300000,
        "yanWuGeLvReq": 2,
        "charLevelReq": 64
    }),
    21: _tools.RODict({
        "ID": 21,
        "upgradeContributionCost": 10250,
        "upgradeCoinCost": 1400000,
        "yanWuGeLvReq": 3,
        "charLevelReq": 66
    }),
    22: _tools.RODict({
        "ID": 22,
        "upgradeContributionCost": 11000,
        "upgradeCoinCost": 1500000,
        "yanWuGeLvReq": 3,
        "charLevelReq": 68
    }),
    23: _tools.RODict({
        "ID": 23,
        "upgradeContributionCost": 11750,
        "upgradeCoinCost": 1600000,
        "yanWuGeLvReq": 3,
        "charLevelReq": 70
    }),
    24: _tools.RODict({
        "ID": 24,
        "upgradeContributionCost": 12500,
        "upgradeCoinCost": 1750000,
        "yanWuGeLvReq": 3,
        "charLevelReq": 71
    }),
    25: _tools.RODict({
        "ID": 25,
        "upgradeContributionCost": 13250,
        "upgradeCoinCost": 1900000,
        "yanWuGeLvReq": 3,
        "charLevelReq": 72
    }),
    26: _tools.RODict({
        "ID": 26,
        "upgradeContributionCost": 14000,
        "upgradeCoinCost": 2050000,
        "yanWuGeLvReq": 3,
        "charLevelReq": 73
    }),
    27: _tools.RODict({
        "ID": 27,
        "upgradeContributionCost": 14750,
        "upgradeCoinCost": 2200000,
        "yanWuGeLvReq": 3,
        "charLevelReq": 74
    }),
    28: _tools.RODict({
        "ID": 28,
        "upgradeContributionCost": 15500,
        "upgradeCoinCost": 2350000,
        "yanWuGeLvReq": 3,
        "charLevelReq": 75
    }),
    29: _tools.RODict({
        "ID": 29,
        "upgradeContributionCost": 16250,
        "upgradeCoinCost": 2500000,
        "yanWuGeLvReq": 3,
        "charLevelReq": 76
    }),
    30: _tools.RODict({
        "ID": 30,
        "upgradeContributionCost": 17000,
        "upgradeCoinCost": 2650000,
        "yanWuGeLvReq": 3,
        "charLevelReq": 77
    }),
    31: _tools.RODict({
        "ID": 31,
        "upgradeContributionCost": 18000,
        "upgradeCoinCost": 2800000,
        "yanWuGeLvReq": 4,
        "charLevelReq": 78
    }),
    32: _tools.RODict({
        "ID": 32,
        "upgradeContributionCost": 19000,
        "upgradeCoinCost": 2950000,
        "yanWuGeLvReq": 4,
        "charLevelReq": 79
    }),
    33: _tools.RODict({
        "ID": 33,
        "upgradeContributionCost": 20000,
        "upgradeCoinCost": 3100000,
        "yanWuGeLvReq": 4,
        "charLevelReq": 80
    }),
    34: _tools.RODict({
        "ID": 34,
        "upgradeContributionCost": 21500,
        "upgradeCoinCost": 3250000,
        "yanWuGeLvReq": 4,
        "charLevelReq": 81
    }),
    35: _tools.RODict({
        "ID": 35,
        "upgradeContributionCost": 23000,
        "upgradeCoinCost": 3400000,
        "yanWuGeLvReq": 4,
        "charLevelReq": 82
    }),
    36: _tools.RODict({
        "ID": 36,
        "upgradeContributionCost": 24500,
        "upgradeCoinCost": 3600000,
        "yanWuGeLvReq": 5,
        "charLevelReq": 83
    }),
    37: _tools.RODict({
        "ID": 37,
        "upgradeContributionCost": 26000,
        "upgradeCoinCost": 3800000,
        "yanWuGeLvReq": 5,
        "charLevelReq": 84
    }),
    38: _tools.RODict({
        "ID": 38,
        "upgradeContributionCost": 27500,
        "upgradeCoinCost": 4000000,
        "yanWuGeLvReq": 5,
        "charLevelReq": 85
    }),
    39: _tools.RODict({
        "ID": 39,
        "upgradeContributionCost": 29000,
        "upgradeCoinCost": 4500000,
        "yanWuGeLvReq": 5,
        "charLevelReq": 86
    }),
    40: _tools.RODict({
        "ID": 40,
        "upgradeContributionCost": 32000,
        "upgradeCoinCost": 5000000,
        "yanWuGeLvReq": 5,
        "charLevelReq": 87
    })
})
minKey = 1
maxKey = 40