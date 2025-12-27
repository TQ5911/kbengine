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
        "upgradeContributionCost": 500,
        "upgradeCoinCost": 3000,
        "yanWuGeLvReq": 1,
        "charLevelReq": 15
    }),
    2: _tools.RODict({
        "ID": 2,
        "upgradeContributionCost": 550,
        "upgradeCoinCost": 4000,
        "yanWuGeLvReq": 1,
        "charLevelReq": 15
    }),
    3: _tools.RODict({
        "ID": 3,
        "upgradeContributionCost": 600,
        "upgradeCoinCost": 5000,
        "yanWuGeLvReq": 1,
        "charLevelReq": 15
    }),
    4: _tools.RODict({
        "ID": 4,
        "upgradeContributionCost": 650,
        "upgradeCoinCost": 7500,
        "yanWuGeLvReq": 1,
        "charLevelReq": 20
    }),
    5: _tools.RODict({
        "ID": 5,
        "upgradeContributionCost": 700,
        "upgradeCoinCost": 10000,
        "yanWuGeLvReq": 1,
        "charLevelReq": 25
    }),
    6: _tools.RODict({
        "ID": 6,
        "upgradeContributionCost": 750,
        "upgradeCoinCost": 30000,
        "yanWuGeLvReq": 1,
        "charLevelReq": 29
    }),
    7: _tools.RODict({
        "ID": 7,
        "upgradeContributionCost": 800,
        "upgradeCoinCost": 50000,
        "yanWuGeLvReq": 1,
        "charLevelReq": 32
    }),
    8: _tools.RODict({
        "ID": 8,
        "upgradeContributionCost": 900,
        "upgradeCoinCost": 100000,
        "yanWuGeLvReq": 1,
        "charLevelReq": 35
    }),
    9: _tools.RODict({
        "ID": 9,
        "upgradeContributionCost": 1200,
        "upgradeCoinCost": 150000,
        "yanWuGeLvReq": 1,
        "charLevelReq": 38
    }),
    10: _tools.RODict({
        "ID": 10,
        "upgradeContributionCost": 2000,
        "upgradeCoinCost": 200000,
        "yanWuGeLvReq": 1,
        "charLevelReq": 41
    }),
    11: _tools.RODict({
        "ID": 11,
        "upgradeContributionCost": 2500,
        "upgradeCoinCost": 250000,
        "yanWuGeLvReq": 1,
        "charLevelReq": 43
    }),
    12: _tools.RODict({
        "ID": 12,
        "upgradeContributionCost": 3000,
        "upgradeCoinCost": 300000,
        "yanWuGeLvReq": 1,
        "charLevelReq": 45
    }),
    13: _tools.RODict({
        "ID": 13,
        "upgradeContributionCost": 3500,
        "upgradeCoinCost": 400000,
        "yanWuGeLvReq": 2,
        "charLevelReq": 47
    }),
    14: _tools.RODict({
        "ID": 14,
        "upgradeContributionCost": 4000,
        "upgradeCoinCost": 500000,
        "yanWuGeLvReq": 2,
        "charLevelReq": 49
    }),
    15: _tools.RODict({
        "ID": 15,
        "upgradeContributionCost": 4500,
        "upgradeCoinCost": 600000,
        "yanWuGeLvReq": 2,
        "charLevelReq": 51
    }),
    16: _tools.RODict({
        "ID": 16,
        "upgradeContributionCost": 5000,
        "upgradeCoinCost": 700000,
        "yanWuGeLvReq": 2,
        "charLevelReq": 53
    }),
    17: _tools.RODict({
        "ID": 17,
        "upgradeContributionCost": 5500,
        "upgradeCoinCost": 800000,
        "yanWuGeLvReq": 2,
        "charLevelReq": 55
    }),
    18: _tools.RODict({
        "ID": 18,
        "upgradeContributionCost": 6000,
        "upgradeCoinCost": 900000,
        "yanWuGeLvReq": 2,
        "charLevelReq": 57
    }),
    19: _tools.RODict({
        "ID": 19,
        "upgradeContributionCost": 6500,
        "upgradeCoinCost": 1000000,
        "yanWuGeLvReq": 2,
        "charLevelReq": 59
    }),
    20: _tools.RODict({
        "ID": 20,
        "upgradeContributionCost": 7000,
        "upgradeCoinCost": 1100000,
        "yanWuGeLvReq": 2,
        "charLevelReq": 61
    }),
    21: _tools.RODict({
        "ID": 21,
        "upgradeContributionCost": 7500,
        "upgradeCoinCost": 1200000,
        "yanWuGeLvReq": 3,
        "charLevelReq": 63
    }),
    22: _tools.RODict({
        "ID": 22,
        "upgradeContributionCost": 8000,
        "upgradeCoinCost": 1300000,
        "yanWuGeLvReq": 3,
        "charLevelReq": 65
    }),
    23: _tools.RODict({
        "ID": 23,
        "upgradeContributionCost": 8500,
        "upgradeCoinCost": 1400000,
        "yanWuGeLvReq": 3,
        "charLevelReq": 67
    }),
    24: _tools.RODict({
        "ID": 24,
        "upgradeContributionCost": 9000,
        "upgradeCoinCost": 1500000,
        "yanWuGeLvReq": 3,
        "charLevelReq": 69
    }),
    25: _tools.RODict({
        "ID": 25,
        "upgradeContributionCost": 9500,
        "upgradeCoinCost": 1600000,
        "yanWuGeLvReq": 3,
        "charLevelReq": 71
    }),
    26: _tools.RODict({
        "ID": 26,
        "upgradeContributionCost": 10000,
        "upgradeCoinCost": 1700000,
        "yanWuGeLvReq": 3,
        "charLevelReq": 73
    }),
    27: _tools.RODict({
        "ID": 27,
        "upgradeContributionCost": 10500,
        "upgradeCoinCost": 1800000,
        "yanWuGeLvReq": 3,
        "charLevelReq": 75
    }),
    28: _tools.RODict({
        "ID": 28,
        "upgradeContributionCost": 11000,
        "upgradeCoinCost": 1900000,
        "yanWuGeLvReq": 3,
        "charLevelReq": 77
    }),
    29: _tools.RODict({
        "ID": 29,
        "upgradeContributionCost": 11500,
        "upgradeCoinCost": 2000000,
        "yanWuGeLvReq": 3,
        "charLevelReq": 79
    }),
    30: _tools.RODict({
        "ID": 30,
        "upgradeContributionCost": 12000,
        "upgradeCoinCost": 2100000,
        "yanWuGeLvReq": 3,
        "charLevelReq": 80
    }),
    31: _tools.RODict({
        "ID": 31,
        "upgradeContributionCost": 12500,
        "upgradeCoinCost": 2200000,
        "yanWuGeLvReq": 4,
        "charLevelReq": 81
    }),
    32: _tools.RODict({
        "ID": 32,
        "upgradeContributionCost": 13000,
        "upgradeCoinCost": 2400000,
        "yanWuGeLvReq": 4,
        "charLevelReq": 82
    }),
    33: _tools.RODict({
        "ID": 33,
        "upgradeContributionCost": 13500,
        "upgradeCoinCost": 2600000,
        "yanWuGeLvReq": 4,
        "charLevelReq": 83
    }),
    34: _tools.RODict({
        "ID": 34,
        "upgradeContributionCost": 14000,
        "upgradeCoinCost": 2800000,
        "yanWuGeLvReq": 4,
        "charLevelReq": 84
    }),
    35: _tools.RODict({
        "ID": 35,
        "upgradeContributionCost": 14500,
        "upgradeCoinCost": 3000000,
        "yanWuGeLvReq": 4,
        "charLevelReq": 85
    }),
    36: _tools.RODict({
        "ID": 36,
        "upgradeContributionCost": 15000,
        "upgradeCoinCost": 3200000,
        "yanWuGeLvReq": 5,
        "charLevelReq": 86
    }),
    37: _tools.RODict({
        "ID": 37,
        "upgradeContributionCost": 15500,
        "upgradeCoinCost": 3400000,
        "yanWuGeLvReq": 5,
        "charLevelReq": 87
    }),
    38: _tools.RODict({
        "ID": 38,
        "upgradeContributionCost": 16000,
        "upgradeCoinCost": 3600000,
        "yanWuGeLvReq": 5,
        "charLevelReq": 88
    }),
    39: _tools.RODict({
        "ID": 39,
        "upgradeContributionCost": 16500,
        "upgradeCoinCost": 3800000,
        "yanWuGeLvReq": 5,
        "charLevelReq": 89
    }),
    40: _tools.RODict({
        "ID": 40,
        "upgradeContributionCost": 17000,
        "upgradeCoinCost": 4000000,
        "yanWuGeLvReq": 5,
        "charLevelReq": 90
    })
})
minKey = 1
maxKey = 40