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
        "normalExp": 16
    }),
    3: _tools.RODict({
        "ID": 3,
        "normalExp": 17
    }),
    4: _tools.RODict({
        "ID": 4,
        "normalExp": 17
    }),
    5: _tools.RODict({
        "ID": 5,
        "normalExp": 18
    }),
    6: _tools.RODict({
        "ID": 6,
        "normalExp": 19
    }),
    7: _tools.RODict({
        "ID": 7,
        "normalExp": 20
    }),
    8: _tools.RODict({
        "ID": 8,
        "normalExp": 21
    }),
    9: _tools.RODict({
        "ID": 9,
        "normalExp": 22
    }),
    10: _tools.RODict({
        "ID": 10,
        "normalExp": 23
    }),
    11: _tools.RODict({
        "ID": 11,
        "normalExp": 24
    }),
    12: _tools.RODict({
        "ID": 12,
        "normalExp": 26
    }),
    13: _tools.RODict({
        "ID": 13,
        "normalExp": 27
    }),
    14: _tools.RODict({
        "ID": 14,
        "normalExp": 28
    }),
    15: _tools.RODict({
        "ID": 15,
        "normalExp": 30
    }),
    16: _tools.RODict({
        "ID": 16,
        "normalExp": 31
    }),
    17: _tools.RODict({
        "ID": 17,
        "normalExp": 33
    }),
    18: _tools.RODict({
        "ID": 18,
        "normalExp": 34
    }),
    19: _tools.RODict({
        "ID": 19,
        "normalExp": 36
    }),
    20: _tools.RODict({
        "ID": 20,
        "normalExp": 38
    }),
    21: _tools.RODict({
        "ID": 21,
        "normalExp": 40
    }),
    22: _tools.RODict({
        "ID": 22,
        "normalExp": 42
    }),
    23: _tools.RODict({
        "ID": 23,
        "normalExp": 44
    }),
    24: _tools.RODict({
        "ID": 24,
        "normalExp": 46
    }),
    25: _tools.RODict({
        "ID": 25,
        "normalExp": 48
    }),
    26: _tools.RODict({
        "ID": 26,
        "normalExp": 51
    }),
    27: _tools.RODict({
        "ID": 27,
        "normalExp": 53
    }),
    28: _tools.RODict({
        "ID": 28,
        "normalExp": 56
    }),
    29: _tools.RODict({
        "ID": 29,
        "normalExp": 59
    }),
    30: _tools.RODict({
        "ID": 30,
        "normalExp": 62
    }),
    31: _tools.RODict({
        "ID": 31,
        "normalExp": 65
    }),
    32: _tools.RODict({
        "ID": 32,
        "normalExp": 68
    }),
    33: _tools.RODict({
        "ID": 33,
        "normalExp": 71
    }),
    34: _tools.RODict({
        "ID": 34,
        "normalExp": 75
    }),
    35: _tools.RODict({
        "ID": 35,
        "normalExp": 79
    }),
    36: _tools.RODict({
        "ID": 36,
        "normalExp": 83
    }),
    37: _tools.RODict({
        "ID": 37,
        "normalExp": 87
    }),
    38: _tools.RODict({
        "ID": 38,
        "normalExp": 91
    }),
    39: _tools.RODict({
        "ID": 39,
        "normalExp": 96
    }),
    40: _tools.RODict({
        "ID": 40,
        "normalExp": 101
    }),
    41: _tools.RODict({
        "ID": 41,
        "normalExp": 106
    }),
    42: _tools.RODict({
        "ID": 42,
        "normalExp": 111
    }),
    43: _tools.RODict({
        "ID": 43,
        "normalExp": 116
    }),
    44: _tools.RODict({
        "ID": 44,
        "normalExp": 122
    }),
    45: _tools.RODict({
        "ID": 45,
        "normalExp": 128
    }),
    46: _tools.RODict({
        "ID": 46,
        "normalExp": 135
    }),
    47: _tools.RODict({
        "ID": 47,
        "normalExp": 142
    }),
    48: _tools.RODict({
        "ID": 48,
        "normalExp": 149
    }),
    49: _tools.RODict({
        "ID": 49,
        "normalExp": 156
    }),
    50: _tools.RODict({
        "ID": 50,
        "normalExp": 164
    }),
    51: _tools.RODict({
        "ID": 51,
        "normalExp": 172
    }),
    52: _tools.RODict({
        "ID": 52,
        "normalExp": 181
    }),
    53: _tools.RODict({
        "ID": 53,
        "normalExp": 190
    }),
    54: _tools.RODict({
        "ID": 54,
        "normalExp": 199
    }),
    55: _tools.RODict({
        "ID": 55,
        "normalExp": 209
    }),
    56: _tools.RODict({
        "ID": 56,
        "normalExp": 220
    }),
    57: _tools.RODict({
        "ID": 57,
        "normalExp": 231
    }),
    58: _tools.RODict({
        "ID": 58,
        "normalExp": 242
    }),
    59: _tools.RODict({
        "ID": 59,
        "normalExp": 254
    }),
    60: _tools.RODict({
        "ID": 60,
        "normalExp": 267
    }),
    61: _tools.RODict({
        "ID": 61,
        "normalExp": 280
    }),
    62: _tools.RODict({
        "ID": 62,
        "normalExp": 294
    }),
    63: _tools.RODict({
        "ID": 63,
        "normalExp": 309
    }),
    64: _tools.RODict({
        "ID": 64,
        "normalExp": 324
    }),
    65: _tools.RODict({
        "ID": 65,
        "normalExp": 341
    }),
    66: _tools.RODict({
        "ID": 66,
        "normalExp": 358
    }),
    67: _tools.RODict({
        "ID": 67,
        "normalExp": 375
    }),
    68: _tools.RODict({
        "ID": 68,
        "normalExp": 394
    }),
    69: _tools.RODict({
        "ID": 69,
        "normalExp": 414
    }),
    70: _tools.RODict({
        "ID": 70,
        "normalExp": 435
    }),
    71: _tools.RODict({
        "ID": 71,
        "normalExp": 456
    }),
    72: _tools.RODict({
        "ID": 72,
        "normalExp": 479
    }),
    73: _tools.RODict({
        "ID": 73,
        "normalExp": 503
    }),
    74: _tools.RODict({
        "ID": 74,
        "normalExp": 528
    }),
    75: _tools.RODict({
        "ID": 75,
        "normalExp": 555
    }),
    76: _tools.RODict({
        "ID": 76,
        "normalExp": 582
    }),
    77: _tools.RODict({
        "ID": 77,
        "normalExp": 612
    }),
    78: _tools.RODict({
        "ID": 78,
        "normalExp": 642
    }),
    79: _tools.RODict({
        "ID": 79,
        "normalExp": 674
    }),
    80: _tools.RODict({
        "ID": 80,
        "normalExp": 708
    }),
    81: _tools.RODict({
        "ID": 81,
        "normalExp": 743
    }),
    82: _tools.RODict({
        "ID": 82,
        "normalExp": 781
    }),
    83: _tools.RODict({
        "ID": 83,
        "normalExp": 820
    }),
    84: _tools.RODict({
        "ID": 84,
        "normalExp": 861
    }),
    85: _tools.RODict({
        "ID": 85,
        "normalExp": 904
    }),
    86: _tools.RODict({
        "ID": 86,
        "normalExp": 949
    }),
    87: _tools.RODict({
        "ID": 87,
        "normalExp": 996
    }),
    88: _tools.RODict({
        "ID": 88,
        "normalExp": 1046
    }),
    89: _tools.RODict({
        "ID": 89,
        "normalExp": 1098
    }),
    90: _tools.RODict({
        "ID": 90,
        "normalExp": 1153
    }),
    91: _tools.RODict({
        "ID": 91,
        "normalExp": 1211
    }),
    92: _tools.RODict({
        "ID": 92,
        "normalExp": 1272
    }),
    93: _tools.RODict({
        "ID": 93,
        "normalExp": 1335
    }),
    94: _tools.RODict({
        "ID": 94,
        "normalExp": 1402
    }),
    95: _tools.RODict({
        "ID": 95,
        "normalExp": 1472
    }),
    96: _tools.RODict({
        "ID": 96,
        "normalExp": 1546
    }),
    97: _tools.RODict({
        "ID": 97,
        "normalExp": 1623
    }),
    98: _tools.RODict({
        "ID": 98,
        "normalExp": 1704
    }),
    99: _tools.RODict({
        "ID": 99,
        "normalExp": 1789
    }),
    100: _tools.RODict({
        "ID": 100,
        "normalExp": 1879
    })
})
minKey = 1
maxKey = 100