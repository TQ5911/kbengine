# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: bagData/commonBagCapacity
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    1: _tools.RODict({
        "grid": 1,
        "itemNeeded": 30000001,
        "itemNum": 5
    }),
    2: _tools.RODict({
        "grid": 2,
        "itemNeeded": 30000001,
        "itemNum": 5
    }),
    3: _tools.RODict({
        "grid": 3,
        "itemNeeded": 30000001,
        "itemNum": 5
    }),
    4: _tools.RODict({
        "grid": 4,
        "itemNeeded": 30000001,
        "itemNum": 5
    }),
    5: _tools.RODict({
        "grid": 5,
        "itemNeeded": 30000001,
        "itemNum": 5
    }),
    6: _tools.RODict({
        "grid": 6,
        "itemNeeded": 30000001,
        "itemNum": 7
    }),
    7: _tools.RODict({
        "grid": 7,
        "itemNeeded": 30000001,
        "itemNum": 7
    }),
    8: _tools.RODict({
        "grid": 8,
        "itemNeeded": 30000001,
        "itemNum": 7
    }),
    9: _tools.RODict({
        "grid": 9,
        "itemNeeded": 30000001,
        "itemNum": 7
    }),
    10: _tools.RODict({
        "grid": 10,
        "itemNeeded": 30000001,
        "itemNum": 7
    }),
    11: _tools.RODict({
        "grid": 11,
        "itemNeeded": 30000001,
        "itemNum": 9
    }),
    12: _tools.RODict({
        "grid": 12,
        "itemNeeded": 30000001,
        "itemNum": 9
    }),
    13: _tools.RODict({
        "grid": 13,
        "itemNeeded": 30000001,
        "itemNum": 9
    }),
    14: _tools.RODict({
        "grid": 14,
        "itemNeeded": 30000001,
        "itemNum": 9
    }),
    15: _tools.RODict({
        "grid": 15,
        "itemNeeded": 30000001,
        "itemNum": 9
    }),
    16: _tools.RODict({
        "grid": 16,
        "itemNeeded": 30000001,
        "itemNum": 11
    }),
    17: _tools.RODict({
        "grid": 17,
        "itemNeeded": 30000001,
        "itemNum": 11
    }),
    18: _tools.RODict({
        "grid": 18,
        "itemNeeded": 30000001,
        "itemNum": 11
    }),
    19: _tools.RODict({
        "grid": 19,
        "itemNeeded": 30000001,
        "itemNum": 11
    }),
    20: _tools.RODict({
        "grid": 20,
        "itemNeeded": 30000001,
        "itemNum": 11
    }),
    21: _tools.RODict({
        "grid": 21,
        "itemNeeded": 30000001,
        "itemNum": 13
    }),
    22: _tools.RODict({
        "grid": 22,
        "itemNeeded": 30000001,
        "itemNum": 13
    }),
    23: _tools.RODict({
        "grid": 23,
        "itemNeeded": 30000001,
        "itemNum": 13
    }),
    24: _tools.RODict({
        "grid": 24,
        "itemNeeded": 30000001,
        "itemNum": 13
    }),
    25: _tools.RODict({
        "grid": 25,
        "itemNeeded": 30000001,
        "itemNum": 13
    }),
    26: _tools.RODict({
        "grid": 26,
        "itemNeeded": 30000001,
        "itemNum": 15
    }),
    27: _tools.RODict({
        "grid": 27,
        "itemNeeded": 30000001,
        "itemNum": 15
    }),
    28: _tools.RODict({
        "grid": 28,
        "itemNeeded": 30000001,
        "itemNum": 15
    }),
    29: _tools.RODict({
        "grid": 29,
        "itemNeeded": 30000001,
        "itemNum": 15
    }),
    30: _tools.RODict({
        "grid": 30,
        "itemNeeded": 30000001,
        "itemNum": 15
    }),
    31: _tools.RODict({
        "grid": 31,
        "itemNeeded": 30000001,
        "itemNum": 17
    }),
    32: _tools.RODict({
        "grid": 32,
        "itemNeeded": 30000001,
        "itemNum": 17
    }),
    33: _tools.RODict({
        "grid": 33,
        "itemNeeded": 30000001,
        "itemNum": 17
    }),
    34: _tools.RODict({
        "grid": 34,
        "itemNeeded": 30000001,
        "itemNum": 17
    }),
    35: _tools.RODict({
        "grid": 35,
        "itemNeeded": 30000001,
        "itemNum": 17
    }),
    36: _tools.RODict({
        "grid": 36,
        "itemNeeded": 30000001,
        "itemNum": 19
    }),
    37: _tools.RODict({
        "grid": 37,
        "itemNeeded": 30000001,
        "itemNum": 19
    }),
    38: _tools.RODict({
        "grid": 38,
        "itemNeeded": 30000001,
        "itemNum": 19
    }),
    39: _tools.RODict({
        "grid": 39,
        "itemNeeded": 30000001,
        "itemNum": 19
    }),
    40: _tools.RODict({
        "grid": 40,
        "itemNeeded": 30000001,
        "itemNum": 19
    }),
    41: _tools.RODict({
        "grid": 41,
        "itemNeeded": 30000001,
        "itemNum": 21
    }),
    42: _tools.RODict({
        "grid": 42,
        "itemNeeded": 30000001,
        "itemNum": 21
    }),
    43: _tools.RODict({
        "grid": 43,
        "itemNeeded": 30000001,
        "itemNum": 21
    }),
    44: _tools.RODict({
        "grid": 44,
        "itemNeeded": 30000001,
        "itemNum": 21
    }),
    45: _tools.RODict({
        "grid": 45,
        "itemNeeded": 30000001,
        "itemNum": 21
    }),
    46: _tools.RODict({
        "grid": 46,
        "itemNeeded": 30000001,
        "itemNum": 23
    }),
    47: _tools.RODict({
        "grid": 47,
        "itemNeeded": 30000001,
        "itemNum": 23
    }),
    48: _tools.RODict({
        "grid": 48,
        "itemNeeded": 30000001,
        "itemNum": 23
    }),
    49: _tools.RODict({
        "grid": 49,
        "itemNeeded": 30000001,
        "itemNum": 23
    }),
    50: _tools.RODict({
        "grid": 50,
        "itemNeeded": 30000001,
        "itemNum": 23
    })
})
minKey = 1
maxKey = 50