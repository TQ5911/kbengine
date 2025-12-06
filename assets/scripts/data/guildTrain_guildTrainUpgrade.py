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
        "upgradeCoinCost": 1600,
        "yanWuGeLvReq": 1,
        "charLevelReq": 1
    }),
    2: _tools.RODict({
        "ID": 2,
        "upgradeContributionCost": 440,
        "upgradeCoinCost": 1760,
        "yanWuGeLvReq": 1,
        "charLevelReq": 2
    }),
    3: _tools.RODict({
        "ID": 3,
        "upgradeContributionCost": 484,
        "upgradeCoinCost": 1920,
        "yanWuGeLvReq": 1,
        "charLevelReq": 3
    }),
    4: _tools.RODict({
        "ID": 4,
        "upgradeContributionCost": 532,
        "upgradeCoinCost": 2120,
        "yanWuGeLvReq": 1,
        "charLevelReq": 4
    }),
    5: _tools.RODict({
        "ID": 5,
        "upgradeContributionCost": 585,
        "upgradeCoinCost": 2320,
        "yanWuGeLvReq": 1,
        "charLevelReq": 5
    }),
    6: _tools.RODict({
        "ID": 6,
        "upgradeContributionCost": 644,
        "upgradeCoinCost": 2560,
        "yanWuGeLvReq": 1,
        "charLevelReq": 6
    }),
    7: _tools.RODict({
        "ID": 7,
        "upgradeContributionCost": 708,
        "upgradeCoinCost": 2800,
        "yanWuGeLvReq": 1,
        "charLevelReq": 7
    }),
    8: _tools.RODict({
        "ID": 8,
        "upgradeContributionCost": 779,
        "upgradeCoinCost": 3080,
        "yanWuGeLvReq": 1,
        "charLevelReq": 8
    }),
    9: _tools.RODict({
        "ID": 9,
        "upgradeContributionCost": 857,
        "upgradeCoinCost": 3400,
        "yanWuGeLvReq": 1,
        "charLevelReq": 9
    }),
    10: _tools.RODict({
        "ID": 10,
        "upgradeContributionCost": 943,
        "upgradeCoinCost": 3760,
        "yanWuGeLvReq": 2,
        "charLevelReq": 10
    }),
    11: _tools.RODict({
        "ID": 11,
        "upgradeContributionCost": 1037,
        "upgradeCoinCost": 4120,
        "yanWuGeLvReq": 2,
        "charLevelReq": 12
    }),
    12: _tools.RODict({
        "ID": 12,
        "upgradeContributionCost": 1141,
        "upgradeCoinCost": 4520,
        "yanWuGeLvReq": 2,
        "charLevelReq": 14
    }),
    13: _tools.RODict({
        "ID": 13,
        "upgradeContributionCost": 1255,
        "upgradeCoinCost": 4960,
        "yanWuGeLvReq": 2,
        "charLevelReq": 16
    }),
    14: _tools.RODict({
        "ID": 14,
        "upgradeContributionCost": 1381,
        "upgradeCoinCost": 5440,
        "yanWuGeLvReq": 2,
        "charLevelReq": 18
    }),
    15: _tools.RODict({
        "ID": 15,
        "upgradeContributionCost": 1519,
        "upgradeCoinCost": 6000,
        "yanWuGeLvReq": 2,
        "charLevelReq": 20
    }),
    16: _tools.RODict({
        "ID": 16,
        "upgradeContributionCost": 1671,
        "upgradeCoinCost": 6600,
        "yanWuGeLvReq": 2,
        "charLevelReq": 22
    }),
    17: _tools.RODict({
        "ID": 17,
        "upgradeContributionCost": 1838,
        "upgradeCoinCost": 7280,
        "yanWuGeLvReq": 2,
        "charLevelReq": 24
    }),
    18: _tools.RODict({
        "ID": 18,
        "upgradeContributionCost": 2022,
        "upgradeCoinCost": 8000,
        "yanWuGeLvReq": 3,
        "charLevelReq": 26
    }),
    19: _tools.RODict({
        "ID": 19,
        "upgradeContributionCost": 2224,
        "upgradeCoinCost": 8800,
        "yanWuGeLvReq": 3,
        "charLevelReq": 28
    }),
    20: _tools.RODict({
        "ID": 20,
        "upgradeContributionCost": 2446,
        "upgradeCoinCost": 9680,
        "yanWuGeLvReq": 3,
        "charLevelReq": 30
    }),
    21: _tools.RODict({
        "ID": 21,
        "upgradeContributionCost": 2691,
        "upgradeCoinCost": 10640,
        "yanWuGeLvReq": 3,
        "charLevelReq": 32
    }),
    22: _tools.RODict({
        "ID": 22,
        "upgradeContributionCost": 2960,
        "upgradeCoinCost": 11720,
        "yanWuGeLvReq": 3,
        "charLevelReq": 34
    }),
    23: _tools.RODict({
        "ID": 23,
        "upgradeContributionCost": 3256,
        "upgradeCoinCost": 12880,
        "yanWuGeLvReq": 3,
        "charLevelReq": 36
    }),
    24: _tools.RODict({
        "ID": 24,
        "upgradeContributionCost": 3582,
        "upgradeCoinCost": 14160,
        "yanWuGeLvReq": 3,
        "charLevelReq": 38
    }),
    25: _tools.RODict({
        "ID": 25,
        "upgradeContributionCost": 3940,
        "upgradeCoinCost": 15560,
        "yanWuGeLvReq": 3,
        "charLevelReq": 40
    }),
    26: _tools.RODict({
        "ID": 26,
        "upgradeContributionCost": 4334,
        "upgradeCoinCost": 17120,
        "yanWuGeLvReq": 4,
        "charLevelReq": 42
    }),
    27: _tools.RODict({
        "ID": 27,
        "upgradeContributionCost": 4767,
        "upgradeCoinCost": 18840,
        "yanWuGeLvReq": 4,
        "charLevelReq": 44
    }),
    28: _tools.RODict({
        "ID": 28,
        "upgradeContributionCost": 5244,
        "upgradeCoinCost": 20720,
        "yanWuGeLvReq": 4,
        "charLevelReq": 46
    }),
    29: _tools.RODict({
        "ID": 29,
        "upgradeContributionCost": 5768,
        "upgradeCoinCost": 22800,
        "yanWuGeLvReq": 4,
        "charLevelReq": 48
    }),
    30: _tools.RODict({
        "ID": 30,
        "upgradeContributionCost": 6345,
        "upgradeCoinCost": 25080,
        "yanWuGeLvReq": 4,
        "charLevelReq": 50
    }),
    31: _tools.RODict({
        "ID": 31,
        "upgradeContributionCost": 6980,
        "upgradeCoinCost": 27600,
        "yanWuGeLvReq": 4,
        "charLevelReq": 53
    }),
    32: _tools.RODict({
        "ID": 32,
        "upgradeContributionCost": 7678,
        "upgradeCoinCost": 30360,
        "yanWuGeLvReq": 4,
        "charLevelReq": 56
    }),
    33: _tools.RODict({
        "ID": 33,
        "upgradeContributionCost": 8446,
        "upgradeCoinCost": 33400,
        "yanWuGeLvReq": 4,
        "charLevelReq": 59
    }),
    34: _tools.RODict({
        "ID": 34,
        "upgradeContributionCost": 9291,
        "upgradeCoinCost": 36760,
        "yanWuGeLvReq": 5,
        "charLevelReq": 62
    }),
    35: _tools.RODict({
        "ID": 35,
        "upgradeContributionCost": 10220,
        "upgradeCoinCost": 40440,
        "yanWuGeLvReq": 5,
        "charLevelReq": 65
    }),
    36: _tools.RODict({
        "ID": 36,
        "upgradeContributionCost": 11242,
        "upgradeCoinCost": 44480,
        "yanWuGeLvReq": 5,
        "charLevelReq": 68
    }),
    37: _tools.RODict({
        "ID": 37,
        "upgradeContributionCost": 12366,
        "upgradeCoinCost": 48920,
        "yanWuGeLvReq": 5,
        "charLevelReq": 71
    }),
    38: _tools.RODict({
        "ID": 38,
        "upgradeContributionCost": 13603,
        "upgradeCoinCost": 53800,
        "yanWuGeLvReq": 5,
        "charLevelReq": 74
    }),
    39: _tools.RODict({
        "ID": 39,
        "upgradeContributionCost": 14963,
        "upgradeCoinCost": 59200,
        "yanWuGeLvReq": 5,
        "charLevelReq": 77
    }),
    40: _tools.RODict({
        "ID": 40,
        "upgradeContributionCost": 16459,
        "upgradeCoinCost": 65120,
        "yanWuGeLvReq": 5,
        "charLevelReq": 80
    })
})
minKey = 1
maxKey = 40