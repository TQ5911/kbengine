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
    }),
    51: _tools.RODict({
        "grid": 51,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    52: _tools.RODict({
        "grid": 52,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    53: _tools.RODict({
        "grid": 53,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    54: _tools.RODict({
        "grid": 54,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    55: _tools.RODict({
        "grid": 55,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    56: _tools.RODict({
        "grid": 56,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    57: _tools.RODict({
        "grid": 57,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    58: _tools.RODict({
        "grid": 58,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    59: _tools.RODict({
        "grid": 59,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    60: _tools.RODict({
        "grid": 60,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    61: _tools.RODict({
        "grid": 61,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    62: _tools.RODict({
        "grid": 62,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    63: _tools.RODict({
        "grid": 63,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    64: _tools.RODict({
        "grid": 64,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    65: _tools.RODict({
        "grid": 65,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    66: _tools.RODict({
        "grid": 66,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    67: _tools.RODict({
        "grid": 67,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    68: _tools.RODict({
        "grid": 68,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    69: _tools.RODict({
        "grid": 69,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    70: _tools.RODict({
        "grid": 70,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    71: _tools.RODict({
        "grid": 71,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    72: _tools.RODict({
        "grid": 72,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    73: _tools.RODict({
        "grid": 73,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    74: _tools.RODict({
        "grid": 74,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    75: _tools.RODict({
        "grid": 75,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    76: _tools.RODict({
        "grid": 76,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    77: _tools.RODict({
        "grid": 77,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    78: _tools.RODict({
        "grid": 78,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    79: _tools.RODict({
        "grid": 79,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    80: _tools.RODict({
        "grid": 80,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    81: _tools.RODict({
        "grid": 81,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    82: _tools.RODict({
        "grid": 82,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    83: _tools.RODict({
        "grid": 83,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    84: _tools.RODict({
        "grid": 84,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    85: _tools.RODict({
        "grid": 85,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    86: _tools.RODict({
        "grid": 86,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    87: _tools.RODict({
        "grid": 87,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    88: _tools.RODict({
        "grid": 88,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    89: _tools.RODict({
        "grid": 89,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    90: _tools.RODict({
        "grid": 90,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    91: _tools.RODict({
        "grid": 91,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    92: _tools.RODict({
        "grid": 92,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    93: _tools.RODict({
        "grid": 93,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    94: _tools.RODict({
        "grid": 94,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    95: _tools.RODict({
        "grid": 95,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    96: _tools.RODict({
        "grid": 96,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    97: _tools.RODict({
        "grid": 97,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    98: _tools.RODict({
        "grid": 98,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    99: _tools.RODict({
        "grid": 99,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    100: _tools.RODict({
        "grid": 100,
        "itemNeeded": 30000001,
        "itemNum": 25
    })
})
minKey = 1
maxKey = 100