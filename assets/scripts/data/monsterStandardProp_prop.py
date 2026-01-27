# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: monsterStandardProp/prop
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
        "normalExp": 15
    }),
    2: _tools.RODict({
        "ID": 2,
        "normalExp": 15
    }),
    3: _tools.RODict({
        "ID": 3,
        "normalExp": 16
    }),
    4: _tools.RODict({
        "ID": 4,
        "normalExp": 16
    }),
    5: _tools.RODict({
        "ID": 5,
        "normalExp": 17
    }),
    6: _tools.RODict({
        "ID": 6,
        "normalExp": 17
    }),
    7: _tools.RODict({
        "ID": 7,
        "normalExp": 18
    }),
    8: _tools.RODict({
        "ID": 8,
        "normalExp": 18
    }),
    9: _tools.RODict({
        "ID": 9,
        "normalExp": 19
    }),
    10: _tools.RODict({
        "ID": 10,
        "normalExp": 20
    }),
    11: _tools.RODict({
        "ID": 11,
        "normalExp": 20
    }),
    12: _tools.RODict({
        "ID": 12,
        "normalExp": 21
    }),
    13: _tools.RODict({
        "ID": 13,
        "normalExp": 21
    }),
    14: _tools.RODict({
        "ID": 14,
        "normalExp": 22
    }),
    15: _tools.RODict({
        "ID": 15,
        "normalExp": 24
    }),
    16: _tools.RODict({
        "ID": 16,
        "normalExp": 25
    }),
    17: _tools.RODict({
        "ID": 17,
        "normalExp": 27
    }),
    18: _tools.RODict({
        "ID": 18,
        "normalExp": 29
    }),
    19: _tools.RODict({
        "ID": 19,
        "normalExp": 31
    }),
    20: _tools.RODict({
        "ID": 20,
        "normalExp": 33
    }),
    21: _tools.RODict({
        "ID": 21,
        "normalExp": 35
    }),
    22: _tools.RODict({
        "ID": 22,
        "normalExp": 38
    }),
    23: _tools.RODict({
        "ID": 23,
        "normalExp": 40
    }),
    24: _tools.RODict({
        "ID": 24,
        "normalExp": 43
    }),
    25: _tools.RODict({
        "ID": 25,
        "normalExp": 46
    }),
    26: _tools.RODict({
        "ID": 26,
        "normalExp": 50
    }),
    27: _tools.RODict({
        "ID": 27,
        "normalExp": 53
    }),
    28: _tools.RODict({
        "ID": 28,
        "normalExp": 57
    }),
    29: _tools.RODict({
        "ID": 29,
        "normalExp": 61
    }),
    30: _tools.RODict({
        "ID": 30,
        "normalExp": 65
    }),
    31: _tools.RODict({
        "ID": 31,
        "normalExp": 70
    }),
    32: _tools.RODict({
        "ID": 32,
        "normalExp": 74
    }),
    33: _tools.RODict({
        "ID": 33,
        "normalExp": 80
    }),
    34: _tools.RODict({
        "ID": 34,
        "normalExp": 85
    }),
    35: _tools.RODict({
        "ID": 35,
        "normalExp": 91
    }),
    36: _tools.RODict({
        "ID": 36,
        "normalExp": 98
    }),
    37: _tools.RODict({
        "ID": 37,
        "normalExp": 104
    }),
    38: _tools.RODict({
        "ID": 38,
        "normalExp": 112
    }),
    39: _tools.RODict({
        "ID": 39,
        "normalExp": 120
    }),
    40: _tools.RODict({
        "ID": 40,
        "normalExp": 128
    }),
    41: _tools.RODict({
        "ID": 41,
        "normalExp": 137
    }),
    42: _tools.RODict({
        "ID": 42,
        "normalExp": 146
    }),
    43: _tools.RODict({
        "ID": 43,
        "normalExp": 157
    }),
    44: _tools.RODict({
        "ID": 44,
        "normalExp": 168
    }),
    45: _tools.RODict({
        "ID": 45,
        "normalExp": 179
    }),
    46: _tools.RODict({
        "ID": 46,
        "normalExp": 192
    }),
    47: _tools.RODict({
        "ID": 47,
        "normalExp": 205
    }),
    48: _tools.RODict({
        "ID": 48,
        "normalExp": 220
    }),
    49: _tools.RODict({
        "ID": 49,
        "normalExp": 235
    }),
    50: _tools.RODict({
        "ID": 50,
        "normalExp": 252
    }),
    51: _tools.RODict({
        "ID": 51,
        "normalExp": 269
    }),
    52: _tools.RODict({
        "ID": 52,
        "normalExp": 288
    }),
    53: _tools.RODict({
        "ID": 53,
        "normalExp": 308
    }),
    54: _tools.RODict({
        "ID": 54,
        "normalExp": 330
    }),
    55: _tools.RODict({
        "ID": 55,
        "normalExp": 353
    }),
    56: _tools.RODict({
        "ID": 56,
        "normalExp": 378
    }),
    57: _tools.RODict({
        "ID": 57,
        "normalExp": 404
    }),
    58: _tools.RODict({
        "ID": 58,
        "normalExp": 432
    }),
    59: _tools.RODict({
        "ID": 59,
        "normalExp": 463
    }),
    60: _tools.RODict({
        "ID": 60,
        "normalExp": 495
    }),
    61: _tools.RODict({
        "ID": 61,
        "normalExp": 530
    }),
    62: _tools.RODict({
        "ID": 62,
        "normalExp": 567
    }),
    63: _tools.RODict({
        "ID": 63,
        "normalExp": 606
    }),
    64: _tools.RODict({
        "ID": 64,
        "normalExp": 649
    }),
    65: _tools.RODict({
        "ID": 65,
        "normalExp": 694
    }),
    66: _tools.RODict({
        "ID": 66,
        "normalExp": 743
    }),
    67: _tools.RODict({
        "ID": 67,
        "normalExp": 795
    }),
    68: _tools.RODict({
        "ID": 68,
        "normalExp": 851
    }),
    69: _tools.RODict({
        "ID": 69,
        "normalExp": 910
    }),
    70: _tools.RODict({
        "ID": 70,
        "normalExp": 974
    }),
    71: _tools.RODict({
        "ID": 71,
        "normalExp": 1042
    }),
    72: _tools.RODict({
        "ID": 72,
        "normalExp": 1115
    }),
    73: _tools.RODict({
        "ID": 73,
        "normalExp": 1193
    }),
    74: _tools.RODict({
        "ID": 74,
        "normalExp": 1276
    }),
    75: _tools.RODict({
        "ID": 75,
        "normalExp": 1366
    }),
    76: _tools.RODict({
        "ID": 76,
        "normalExp": 1461
    }),
    77: _tools.RODict({
        "ID": 77,
        "normalExp": 1564
    }),
    78: _tools.RODict({
        "ID": 78,
        "normalExp": 1673
    }),
    79: _tools.RODict({
        "ID": 79,
        "normalExp": 1790
    }),
    80: _tools.RODict({
        "ID": 80,
        "normalExp": 1916
    }),
    81: _tools.RODict({
        "ID": 81,
        "normalExp": 2050
    }),
    82: _tools.RODict({
        "ID": 82,
        "normalExp": 2193
    }),
    83: _tools.RODict({
        "ID": 83,
        "normalExp": 2347
    }),
    84: _tools.RODict({
        "ID": 84,
        "normalExp": 2511
    }),
    85: _tools.RODict({
        "ID": 85,
        "normalExp": 2687
    }),
    86: _tools.RODict({
        "ID": 86,
        "normalExp": 2875
    }),
    87: _tools.RODict({
        "ID": 87,
        "normalExp": 3076
    }),
    88: _tools.RODict({
        "ID": 88,
        "normalExp": 3291
    }),
    89: _tools.RODict({
        "ID": 89,
        "normalExp": 3522
    }),
    90: _tools.RODict({
        "ID": 90,
        "normalExp": 3768
    }),
    91: _tools.RODict({
        "ID": 91,
        "normalExp": 4032
    }),
    92: _tools.RODict({
        "ID": 92,
        "normalExp": 4314
    }),
    93: _tools.RODict({
        "ID": 93,
        "normalExp": 4616
    }),
    94: _tools.RODict({
        "ID": 94,
        "normalExp": 4939
    }),
    95: _tools.RODict({
        "ID": 95,
        "normalExp": 5285
    }),
    96: _tools.RODict({
        "ID": 96,
        "normalExp": 5655
    }),
    97: _tools.RODict({
        "ID": 97,
        "normalExp": 6051
    }),
    98: _tools.RODict({
        "ID": 98,
        "normalExp": 6475
    }),
    99: _tools.RODict({
        "ID": 99,
        "normalExp": 6928
    }),
    100: _tools.RODict({
        "ID": 100,
        "normalExp": 7413
    })
})
minKey = 1
maxKey = 100