# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: materialSale/quotaLevel
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
        "groupID": 1,
        "minLevel": 1,
        "maxLevel": 29,
        "lvBonus": 0
    }),
    2: _tools.RODict({
        "ID": 2,
        "groupID": 1,
        "minLevel": 30,
        "maxLevel": 39,
        "lvBonus": 2000
    }),
    3: _tools.RODict({
        "ID": 3,
        "groupID": 1,
        "minLevel": 40,
        "maxLevel": 49,
        "lvBonus": 4000
    }),
    4: _tools.RODict({
        "ID": 4,
        "groupID": 1,
        "minLevel": 50,
        "maxLevel": 59,
        "lvBonus": 7000
    }),
    5: _tools.RODict({
        "ID": 5,
        "groupID": 1,
        "minLevel": 60,
        "maxLevel": 69,
        "lvBonus": 9000
    }),
    6: _tools.RODict({
        "ID": 6,
        "groupID": 1,
        "minLevel": 70,
        "maxLevel": 79,
        "lvBonus": 11000
    }),
    7: _tools.RODict({
        "ID": 7,
        "groupID": 1,
        "minLevel": 80,
        "maxLevel": 200,
        "lvBonus": 14000
    }),
    8: _tools.RODict({
        "ID": 8,
        "groupID": 2,
        "minLevel": 1,
        "maxLevel": 29,
        "lvBonus": 0
    }),
    9: _tools.RODict({
        "ID": 9,
        "groupID": 2,
        "minLevel": 30,
        "maxLevel": 39,
        "lvBonus": 1500
    }),
    10: _tools.RODict({
        "ID": 10,
        "groupID": 2,
        "minLevel": 40,
        "maxLevel": 49,
        "lvBonus": 3000
    }),
    11: _tools.RODict({
        "ID": 11,
        "groupID": 2,
        "minLevel": 50,
        "maxLevel": 59,
        "lvBonus": 5000
    }),
    12: _tools.RODict({
        "ID": 12,
        "groupID": 2,
        "minLevel": 60,
        "maxLevel": 69,
        "lvBonus": 7000
    }),
    13: _tools.RODict({
        "ID": 13,
        "groupID": 2,
        "minLevel": 70,
        "maxLevel": 79,
        "lvBonus": 9000
    }),
    14: _tools.RODict({
        "ID": 14,
        "groupID": 2,
        "minLevel": 80,
        "maxLevel": 200,
        "lvBonus": 12000
    }),
    15: _tools.RODict({
        "ID": 15,
        "groupID": 3,
        "minLevel": 1,
        "maxLevel": 29,
        "lvBonus": 0
    }),
    16: _tools.RODict({
        "ID": 16,
        "groupID": 3,
        "minLevel": 30,
        "maxLevel": 39,
        "lvBonus": 1000
    }),
    17: _tools.RODict({
        "ID": 17,
        "groupID": 3,
        "minLevel": 40,
        "maxLevel": 49,
        "lvBonus": 2000
    }),
    18: _tools.RODict({
        "ID": 18,
        "groupID": 3,
        "minLevel": 50,
        "maxLevel": 59,
        "lvBonus": 3000
    }),
    19: _tools.RODict({
        "ID": 19,
        "groupID": 3,
        "minLevel": 60,
        "maxLevel": 69,
        "lvBonus": 4500
    }),
    20: _tools.RODict({
        "ID": 20,
        "groupID": 3,
        "minLevel": 70,
        "maxLevel": 79,
        "lvBonus": 6000
    }),
    21: _tools.RODict({
        "ID": 21,
        "groupID": 3,
        "minLevel": 80,
        "maxLevel": 200,
        "lvBonus": 8000
    })
})
minKey = 1
maxKey = 21

groupBonus = _tools.RODict({
    1: ((1, 29, 0), (30, 39, 2000), (40, 49, 4000), (50, 59, 7000), (60, 69, 9000), (70, 79, 11000), (80, 200, 14000)),
    2: ((1, 29, 0), (30, 39, 1500), (40, 49, 3000), (50, 59, 5000), (60, 69, 7000), (70, 79, 9000), (80, 200, 12000)),
    3: ((1, 29, 0), (30, 39, 1000), (40, 49, 2000), (50, 59, 3000), (60, 69, 4500), (70, 79, 6000), (80, 200, 8000)),
})

def getBonus(groupId, value):
    for minVal, maxVal, bonus in groupBonus.get(groupId, ()):
        if minVal <= value <= maxVal:
            return bonus
    return 0
