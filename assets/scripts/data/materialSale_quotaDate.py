# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: materialSale/quotaDate
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
        "minServerDay": 1,
        "maxServerDay": 7,
        "quotaRate": 0
    }),
    2: _tools.RODict({
        "ID": 2,
        "groupID": 1,
        "minServerDay": 8,
        "maxServerDay": 14,
        "quotaRate": 3000
    }),
    3: _tools.RODict({
        "ID": 3,
        "groupID": 1,
        "minServerDay": 15,
        "maxServerDay": 30,
        "quotaRate": 6000
    }),
    4: _tools.RODict({
        "ID": 4,
        "groupID": 1,
        "minServerDay": 31,
        "maxServerDay": 60,
        "quotaRate": 9000
    }),
    5: _tools.RODict({
        "ID": 5,
        "groupID": 1,
        "minServerDay": 61,
        "maxServerDay": 90,
        "quotaRate": 11000
    }),
    6: _tools.RODict({
        "ID": 6,
        "groupID": 1,
        "minServerDay": 91,
        "maxServerDay": 180,
        "quotaRate": 13000
    }),
    7: _tools.RODict({
        "ID": 7,
        "groupID": 1,
        "minServerDay": 181,
        "maxServerDay": 9999,
        "quotaRate": 15000
    }),
    8: _tools.RODict({
        "ID": 8,
        "groupID": 2,
        "minServerDay": 1,
        "maxServerDay": 7,
        "quotaRate": 0
    }),
    9: _tools.RODict({
        "ID": 9,
        "groupID": 2,
        "minServerDay": 8,
        "maxServerDay": 14,
        "quotaRate": 2000
    }),
    10: _tools.RODict({
        "ID": 10,
        "groupID": 2,
        "minServerDay": 15,
        "maxServerDay": 30,
        "quotaRate": 4000
    }),
    11: _tools.RODict({
        "ID": 11,
        "groupID": 2,
        "minServerDay": 31,
        "maxServerDay": 60,
        "quotaRate": 6000
    }),
    12: _tools.RODict({
        "ID": 12,
        "groupID": 2,
        "minServerDay": 61,
        "maxServerDay": 90,
        "quotaRate": 7500
    }),
    13: _tools.RODict({
        "ID": 13,
        "groupID": 2,
        "minServerDay": 91,
        "maxServerDay": 180,
        "quotaRate": 9000
    }),
    14: _tools.RODict({
        "ID": 14,
        "groupID": 2,
        "minServerDay": 181,
        "maxServerDay": 9999,
        "quotaRate": 10000
    }),
    15: _tools.RODict({
        "ID": 15,
        "groupID": 3,
        "minServerDay": 1,
        "maxServerDay": 7,
        "quotaRate": 0
    }),
    16: _tools.RODict({
        "ID": 16,
        "groupID": 3,
        "minServerDay": 8,
        "maxServerDay": 14,
        "quotaRate": 1000
    }),
    17: _tools.RODict({
        "ID": 17,
        "groupID": 3,
        "minServerDay": 15,
        "maxServerDay": 30,
        "quotaRate": 2000
    }),
    18: _tools.RODict({
        "ID": 18,
        "groupID": 3,
        "minServerDay": 31,
        "maxServerDay": 60,
        "quotaRate": 3000
    }),
    19: _tools.RODict({
        "ID": 19,
        "groupID": 3,
        "minServerDay": 61,
        "maxServerDay": 90,
        "quotaRate": 4000
    }),
    20: _tools.RODict({
        "ID": 20,
        "groupID": 3,
        "minServerDay": 91,
        "maxServerDay": 180,
        "quotaRate": 5000
    }),
    21: _tools.RODict({
        "ID": 21,
        "groupID": 3,
        "minServerDay": 181,
        "maxServerDay": 9999,
        "quotaRate": 6000
    })
})
minKey = 1
maxKey = 21

groupBonus = _tools.RODict({
    1: ((1, 7, 0), (8, 14, 3000), (15, 30, 6000), (31, 60, 9000), (61, 90, 11000), (91, 180, 13000), (181, 9999, 15000)),
    2: ((1, 7, 0), (8, 14, 2000), (15, 30, 4000), (31, 60, 6000), (61, 90, 7500), (91, 180, 9000), (181, 9999, 10000)),
    3: ((1, 7, 0), (8, 14, 1000), (15, 30, 2000), (31, 60, 3000), (61, 90, 4000), (91, 180, 5000), (181, 9999, 6000)),
})

def getBonus(groupId, value):
    for minVal, maxVal, bonus in groupBonus.get(groupId, ()):
        if minVal <= value <= maxVal:
            return bonus
    return 0
