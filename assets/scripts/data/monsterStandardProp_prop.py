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
        "normalExp": 10
    }),
    2: _tools.RODict({
        "ID": 2,
        "normalExp": 10
    }),
    3: _tools.RODict({
        "ID": 3,
        "normalExp": 10
    }),
    4: _tools.RODict({
        "ID": 4,
        "normalExp": 10
    }),
    5: _tools.RODict({
        "ID": 5,
        "normalExp": 10
    }),
    6: _tools.RODict({
        "ID": 6,
        "normalExp": 12
    }),
    7: _tools.RODict({
        "ID": 7,
        "normalExp": 14
    }),
    8: _tools.RODict({
        "ID": 8,
        "normalExp": 16
    }),
    9: _tools.RODict({
        "ID": 9,
        "normalExp": 18
    }),
    10: _tools.RODict({
        "ID": 10,
        "normalExp": 20
    }),
    11: _tools.RODict({
        "ID": 11,
        "normalExp": 22
    }),
    12: _tools.RODict({
        "ID": 12,
        "normalExp": 24
    }),
    13: _tools.RODict({
        "ID": 13,
        "normalExp": 26
    }),
    14: _tools.RODict({
        "ID": 14,
        "normalExp": 28
    }),
    15: _tools.RODict({
        "ID": 15,
        "normalExp": 31
    }),
    16: _tools.RODict({
        "ID": 16,
        "normalExp": 34
    }),
    17: _tools.RODict({
        "ID": 17,
        "normalExp": 37
    }),
    18: _tools.RODict({
        "ID": 18,
        "normalExp": 40
    }),
    19: _tools.RODict({
        "ID": 19,
        "normalExp": 44
    }),
    20: _tools.RODict({
        "ID": 20,
        "normalExp": 48
    }),
    21: _tools.RODict({
        "ID": 21,
        "normalExp": 52
    }),
    22: _tools.RODict({
        "ID": 22,
        "normalExp": 57
    }),
    23: _tools.RODict({
        "ID": 23,
        "normalExp": 62
    }),
    24: _tools.RODict({
        "ID": 24,
        "normalExp": 68
    }),
    25: _tools.RODict({
        "ID": 25,
        "normalExp": 74
    }),
    26: _tools.RODict({
        "ID": 26,
        "normalExp": 81
    }),
    27: _tools.RODict({
        "ID": 27,
        "normalExp": 88
    }),
    28: _tools.RODict({
        "ID": 28,
        "normalExp": 96
    }),
    29: _tools.RODict({
        "ID": 29,
        "normalExp": 105
    }),
    30: _tools.RODict({
        "ID": 30,
        "normalExp": 114
    }),
    31: _tools.RODict({
        "ID": 31,
        "normalExp": 124
    }),
    32: _tools.RODict({
        "ID": 32,
        "normalExp": 135
    }),
    33: _tools.RODict({
        "ID": 33,
        "normalExp": 147
    }),
    34: _tools.RODict({
        "ID": 34,
        "normalExp": 160
    }),
    35: _tools.RODict({
        "ID": 35,
        "normalExp": 174
    }),
    36: _tools.RODict({
        "ID": 36,
        "normalExp": 190
    }),
    37: _tools.RODict({
        "ID": 37,
        "normalExp": 207
    }),
    38: _tools.RODict({
        "ID": 38,
        "normalExp": 226
    }),
    39: _tools.RODict({
        "ID": 39,
        "normalExp": 246
    }),
    40: _tools.RODict({
        "ID": 40,
        "normalExp": 268
    }),
    41: _tools.RODict({
        "ID": 41,
        "normalExp": 292
    }),
    42: _tools.RODict({
        "ID": 42,
        "normalExp": 318
    }),
    43: _tools.RODict({
        "ID": 43,
        "normalExp": 347
    }),
    44: _tools.RODict({
        "ID": 44,
        "normalExp": 378
    }),
    45: _tools.RODict({
        "ID": 45,
        "normalExp": 412
    }),
    46: _tools.RODict({
        "ID": 46,
        "normalExp": 449
    }),
    47: _tools.RODict({
        "ID": 47,
        "normalExp": 489
    }),
    48: _tools.RODict({
        "ID": 48,
        "normalExp": 533
    }),
    49: _tools.RODict({
        "ID": 49,
        "normalExp": 581
    }),
    50: _tools.RODict({
        "ID": 50,
        "normalExp": 633
    }),
    51: _tools.RODict({
        "ID": 51,
        "normalExp": 690
    }),
    52: _tools.RODict({
        "ID": 52,
        "normalExp": 752
    }),
    53: _tools.RODict({
        "ID": 53,
        "normalExp": 820
    }),
    54: _tools.RODict({
        "ID": 54,
        "normalExp": 894
    }),
    55: _tools.RODict({
        "ID": 55,
        "normalExp": 974
    }),
    56: _tools.RODict({
        "ID": 56,
        "normalExp": 1062
    }),
    57: _tools.RODict({
        "ID": 57,
        "normalExp": 1158
    }),
    58: _tools.RODict({
        "ID": 58,
        "normalExp": 1262
    }),
    59: _tools.RODict({
        "ID": 59,
        "normalExp": 1376
    }),
    60: _tools.RODict({
        "ID": 60,
        "normalExp": 1500
    }),
    61: _tools.RODict({
        "ID": 61,
        "normalExp": 1635
    }),
    62: _tools.RODict({
        "ID": 62,
        "normalExp": 1782
    }),
    63: _tools.RODict({
        "ID": 63,
        "normalExp": 1942
    }),
    64: _tools.RODict({
        "ID": 64,
        "normalExp": 2117
    }),
    65: _tools.RODict({
        "ID": 65,
        "normalExp": 2308
    }),
    66: _tools.RODict({
        "ID": 66,
        "normalExp": 2516
    }),
    67: _tools.RODict({
        "ID": 67,
        "normalExp": 2742
    }),
    68: _tools.RODict({
        "ID": 68,
        "normalExp": 2989
    }),
    69: _tools.RODict({
        "ID": 69,
        "normalExp": 3258
    }),
    70: _tools.RODict({
        "ID": 70,
        "normalExp": 3551
    }),
    71: _tools.RODict({
        "ID": 71,
        "normalExp": 3871
    }),
    72: _tools.RODict({
        "ID": 72,
        "normalExp": 4219
    }),
    73: _tools.RODict({
        "ID": 73,
        "normalExp": 4599
    }),
    74: _tools.RODict({
        "ID": 74,
        "normalExp": 5013
    }),
    75: _tools.RODict({
        "ID": 75,
        "normalExp": 5464
    }),
    76: _tools.RODict({
        "ID": 76,
        "normalExp": 5956
    }),
    77: _tools.RODict({
        "ID": 77,
        "normalExp": 6492
    }),
    78: _tools.RODict({
        "ID": 78,
        "normalExp": 7076
    }),
    79: _tools.RODict({
        "ID": 79,
        "normalExp": 7713
    }),
    80: _tools.RODict({
        "ID": 80,
        "normalExp": 8407
    }),
    81: _tools.RODict({
        "ID": 81,
        "normalExp": 9164
    }),
    82: _tools.RODict({
        "ID": 82,
        "normalExp": 9989
    }),
    83: _tools.RODict({
        "ID": 83,
        "normalExp": 10888
    }),
    84: _tools.RODict({
        "ID": 84,
        "normalExp": 11868
    }),
    85: _tools.RODict({
        "ID": 85,
        "normalExp": 12936
    }),
    86: _tools.RODict({
        "ID": 86,
        "normalExp": 14100
    }),
    87: _tools.RODict({
        "ID": 87,
        "normalExp": 15369
    }),
    88: _tools.RODict({
        "ID": 88,
        "normalExp": 16752
    }),
    89: _tools.RODict({
        "ID": 89,
        "normalExp": 18260
    }),
    90: _tools.RODict({
        "ID": 90,
        "normalExp": 19903
    })
})
minKey = 1
maxKey = 90