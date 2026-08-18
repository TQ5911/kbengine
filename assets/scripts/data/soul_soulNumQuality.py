# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: soul/soulNumQuality
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
        "randomID": 1,
        "randomQuality": None,
        "randomProp": 0
    }),
    2: _tools.RODict({
        "ID": 2,
        "randomID": 1,
        "randomQuality": 1,
        "randomProp": 71725
    }),
    3: _tools.RODict({
        "ID": 3,
        "randomID": 1,
        "randomQuality": 2,
        "randomProp": 8333
    }),
    4: _tools.RODict({
        "ID": 4,
        "randomID": 1,
        "randomQuality": 3,
        "randomProp": 1000
    }),
    5: _tools.RODict({
        "ID": 5,
        "randomID": 1,
        "randomQuality": (1, 1),
        "randomProp": 15385
    }),
    6: _tools.RODict({
        "ID": 6,
        "randomID": 1,
        "randomQuality": (2, 1),
        "randomProp": 2857
    }),
    7: _tools.RODict({
        "ID": 7,
        "randomID": 1,
        "randomQuality": (3, 1),
        "randomProp": 250
    }),
    8: _tools.RODict({
        "ID": 8,
        "randomID": 1,
        "randomQuality": (2, 2),
        "randomProp": 250
    }),
    9: _tools.RODict({
        "ID": 9,
        "randomID": 1,
        "randomQuality": (3, 2),
        "randomProp": 133
    }),
    10: _tools.RODict({
        "ID": 10,
        "randomID": 1,
        "randomQuality": (3, 3),
        "randomProp": 67
    }),
    11: _tools.RODict({
        "ID": 11,
        "randomID": 2,
        "randomQuality": None,
        "randomProp": 0
    }),
    12: _tools.RODict({
        "ID": 12,
        "randomID": 2,
        "randomQuality": 1,
        "randomProp": 56511
    }),
    13: _tools.RODict({
        "ID": 13,
        "randomID": 2,
        "randomQuality": 2,
        "randomProp": 6250
    }),
    14: _tools.RODict({
        "ID": 14,
        "randomID": 2,
        "randomQuality": 3,
        "randomProp": 1250
    }),
    15: _tools.RODict({
        "ID": 15,
        "randomID": 2,
        "randomQuality": 4,
        "randomProp": 250
    }),
    16: _tools.RODict({
        "ID": 16,
        "randomID": 2,
        "randomQuality": (1, 1),
        "randomProp": 20000
    }),
    17: _tools.RODict({
        "ID": 17,
        "randomID": 2,
        "randomQuality": (2, 1),
        "randomProp": 5000
    }),
    18: _tools.RODict({
        "ID": 18,
        "randomID": 2,
        "randomQuality": (3, 1),
        "randomProp": 625
    }),
    19: _tools.RODict({
        "ID": 19,
        "randomID": 2,
        "randomQuality": (4, 1),
        "randomProp": 111
    }),
    20: _tools.RODict({
        "ID": 20,
        "randomID": 2,
        "randomQuality": (2, 2),
        "randomProp": 625
    }),
    21: _tools.RODict({
        "ID": 21,
        "randomID": 2,
        "randomQuality": (3, 2),
        "randomProp": 250
    }),
    22: _tools.RODict({
        "ID": 22,
        "randomID": 2,
        "randomQuality": (4, 2),
        "randomProp": 48
    }),
    23: _tools.RODict({
        "ID": 23,
        "randomID": 2,
        "randomQuality": (3, 3),
        "randomProp": 111
    }),
    24: _tools.RODict({
        "ID": 24,
        "randomID": 2,
        "randomQuality": (4, 3),
        "randomProp": 33
    }),
    25: _tools.RODict({
        "ID": 25,
        "randomID": 2,
        "randomQuality": (4, 4),
        "randomProp": 13
    }),
    26: _tools.RODict({
        "ID": 26,
        "randomID": 2,
        "randomQuality": (1, 1, 1),
        "randomProp": 6250
    }),
    27: _tools.RODict({
        "ID": 27,
        "randomID": 2,
        "randomQuality": (2, 1, 1),
        "randomProp": 1250
    }),
    28: _tools.RODict({
        "ID": 28,
        "randomID": 2,
        "randomQuality": (3, 1, 1),
        "randomProp": 357
    }),
    29: _tools.RODict({
        "ID": 29,
        "randomID": 2,
        "randomQuality": (4, 1, 1),
        "randomProp": 111
    }),
    30: _tools.RODict({
        "ID": 30,
        "randomID": 2,
        "randomQuality": (2, 2, 1),
        "randomProp": 357
    }),
    31: _tools.RODict({
        "ID": 31,
        "randomID": 2,
        "randomQuality": (3, 2, 1),
        "randomProp": 111
    }),
    32: _tools.RODict({
        "ID": 32,
        "randomID": 2,
        "randomQuality": (4, 2, 1),
        "randomProp": 100
    }),
    33: _tools.RODict({
        "ID": 33,
        "randomID": 2,
        "randomQuality": (3, 3, 1),
        "randomProp": 48
    }),
    34: _tools.RODict({
        "ID": 34,
        "randomID": 2,
        "randomQuality": (4, 3, 1),
        "randomProp": 25
    }),
    35: _tools.RODict({
        "ID": 35,
        "randomID": 2,
        "randomQuality": (4, 4, 1),
        "randomProp": 17
    }),
    36: _tools.RODict({
        "ID": 36,
        "randomID": 2,
        "randomQuality": (2, 2, 2),
        "randomProp": 111
    }),
    37: _tools.RODict({
        "ID": 37,
        "randomID": 2,
        "randomQuality": (3, 2, 2),
        "randomProp": 48
    }),
    38: _tools.RODict({
        "ID": 38,
        "randomID": 2,
        "randomQuality": (4, 2, 2),
        "randomProp": 25
    }),
    39: _tools.RODict({
        "ID": 39,
        "randomID": 2,
        "randomQuality": (3, 3, 2),
        "randomProp": 33
    }),
    40: _tools.RODict({
        "ID": 40,
        "randomID": 2,
        "randomQuality": (4, 3, 2),
        "randomProp": 13
    }),
    41: _tools.RODict({
        "ID": 41,
        "randomID": 2,
        "randomQuality": (4, 4, 2),
        "randomProp": 8
    }),
    42: _tools.RODict({
        "ID": 42,
        "randomID": 2,
        "randomQuality": (3, 3, 3),
        "randomProp": 36
    }),
    43: _tools.RODict({
        "ID": 43,
        "randomID": 2,
        "randomQuality": (4, 3, 3),
        "randomProp": 13
    }),
    44: _tools.RODict({
        "ID": 44,
        "randomID": 2,
        "randomQuality": (4, 4, 3),
        "randomProp": 6
    }),
    45: _tools.RODict({
        "ID": 45,
        "randomID": 2,
        "randomQuality": (4, 4, 4),
        "randomProp": 5
    }),
    46: _tools.RODict({
        "ID": 46,
        "randomID": 3,
        "randomQuality": 1,
        "randomProp": 28945
    }),
    47: _tools.RODict({
        "ID": 47,
        "randomID": 3,
        "randomQuality": 2,
        "randomProp": 10000
    }),
    48: _tools.RODict({
        "ID": 48,
        "randomID": 3,
        "randomQuality": 3,
        "randomProp": 2500
    }),
    49: _tools.RODict({
        "ID": 49,
        "randomID": 3,
        "randomQuality": 4,
        "randomProp": 500
    }),
    50: _tools.RODict({
        "ID": 50,
        "randomID": 3,
        "randomQuality": (1, 1),
        "randomProp": 28571
    }),
    51: _tools.RODict({
        "ID": 51,
        "randomID": 3,
        "randomQuality": (2, 1),
        "randomProp": 10000
    }),
    52: _tools.RODict({
        "ID": 52,
        "randomID": 3,
        "randomQuality": (3, 1),
        "randomProp": 1250
    }),
    53: _tools.RODict({
        "ID": 53,
        "randomID": 3,
        "randomQuality": (4, 1),
        "randomProp": 222
    }),
    54: _tools.RODict({
        "ID": 54,
        "randomID": 3,
        "randomQuality": (2, 2),
        "randomProp": 1250
    }),
    55: _tools.RODict({
        "ID": 55,
        "randomID": 3,
        "randomQuality": (3, 2),
        "randomProp": 500
    }),
    56: _tools.RODict({
        "ID": 56,
        "randomID": 3,
        "randomQuality": (4, 2),
        "randomProp": 111
    }),
    57: _tools.RODict({
        "ID": 57,
        "randomID": 3,
        "randomQuality": (3, 3),
        "randomProp": 250
    }),
    58: _tools.RODict({
        "ID": 58,
        "randomID": 3,
        "randomQuality": (4, 3),
        "randomProp": 100
    }),
    59: _tools.RODict({
        "ID": 59,
        "randomID": 3,
        "randomQuality": (4, 4),
        "randomProp": 50
    }),
    60: _tools.RODict({
        "ID": 60,
        "randomID": 3,
        "randomQuality": (1, 1, 1),
        "randomProp": 10000
    }),
    61: _tools.RODict({
        "ID": 61,
        "randomID": 3,
        "randomQuality": (2, 1, 1),
        "randomProp": 2500
    }),
    62: _tools.RODict({
        "ID": 62,
        "randomID": 3,
        "randomQuality": (3, 1, 1),
        "randomProp": 714
    }),
    63: _tools.RODict({
        "ID": 63,
        "randomID": 3,
        "randomQuality": (4, 1, 1),
        "randomProp": 250
    }),
    64: _tools.RODict({
        "ID": 64,
        "randomID": 3,
        "randomQuality": (2, 2, 1),
        "randomProp": 714
    }),
    65: _tools.RODict({
        "ID": 65,
        "randomID": 3,
        "randomQuality": (3, 2, 1),
        "randomProp": 222
    }),
    66: _tools.RODict({
        "ID": 66,
        "randomID": 3,
        "randomQuality": (4, 2, 1),
        "randomProp": 250
    }),
    67: _tools.RODict({
        "ID": 67,
        "randomID": 3,
        "randomQuality": (3, 3, 1),
        "randomProp": 111
    }),
    68: _tools.RODict({
        "ID": 68,
        "randomID": 3,
        "randomQuality": (4, 3, 1),
        "randomProp": 83
    }),
    69: _tools.RODict({
        "ID": 69,
        "randomID": 3,
        "randomQuality": (4, 4, 1),
        "randomProp": 67
    }),
    70: _tools.RODict({
        "ID": 70,
        "randomID": 3,
        "randomQuality": (2, 2, 2),
        "randomProp": 222
    }),
    71: _tools.RODict({
        "ID": 71,
        "randomID": 3,
        "randomQuality": (3, 2, 2),
        "randomProp": 111
    }),
    72: _tools.RODict({
        "ID": 72,
        "randomID": 3,
        "randomQuality": (4, 2, 2),
        "randomProp": 83
    }),
    73: _tools.RODict({
        "ID": 73,
        "randomID": 3,
        "randomQuality": (3, 3, 2),
        "randomProp": 100
    }),
    74: _tools.RODict({
        "ID": 74,
        "randomID": 3,
        "randomQuality": (4, 3, 2),
        "randomProp": 50
    }),
    75: _tools.RODict({
        "ID": 75,
        "randomID": 3,
        "randomQuality": (4, 4, 2),
        "randomProp": 33
    }),
    76: _tools.RODict({
        "ID": 76,
        "randomID": 3,
        "randomQuality": (3, 3, 3),
        "randomProp": 143
    }),
    77: _tools.RODict({
        "ID": 77,
        "randomID": 3,
        "randomQuality": (4, 3, 3),
        "randomProp": 50
    }),
    78: _tools.RODict({
        "ID": 78,
        "randomID": 3,
        "randomQuality": (4, 4, 3),
        "randomProp": 25
    }),
    79: _tools.RODict({
        "ID": 79,
        "randomID": 3,
        "randomQuality": (4, 4, 4),
        "randomProp": 20
    }),
    80: _tools.RODict({
        "ID": 80,
        "randomID": 4,
        "randomQuality": 1,
        "randomProp": 400000
    })
})
minKey = 1
maxKey = 80
randomID2qualityStr = {1: ['', '1', '2', '3', '1,1', '2,1', '3,1', '2,2', '3,2', '3,3'], 2: ['', '1', '2', '3', '4', '1,1', '2,1', '3,1', '4,1', '2,2', '3,2', '4,2', '3,3', '4,3', '4,4', '1,1,1', '2,1,1', '3,1,1', '4,1,1', '2,2,1', '3,2,1', '4,2,1', '3,3,1', '4,3,1', '4,4,1', '2,2,2', '3,2,2', '4,2,2', '3,3,2', '4,3,2', '4,4,2', '3,3,3', '4,3,3', '4,4,3', '4,4,4'], 3: ['1', '2', '3', '4', '1,1', '2,1', '3,1', '4,1', '2,2', '3,2', '4,2', '3,3', '4,3', '4,4', '1,1,1', '2,1,1', '3,1,1', '4,1,1', '2,2,1', '3,2,1', '4,2,1', '3,3,1', '4,3,1', '4,4,1', '2,2,2', '3,2,2', '4,2,2', '3,3,2', '4,3,2', '4,4,2', '3,3,3', '4,3,3', '4,4,3', '4,4,4'], 4: ['1']}

randomID2weight = {1: [0, 71725, 8333, 1000, 15385, 2857, 250, 250, 133, 67], 2: [0, 56511, 6250, 1250, 250, 20000, 5000, 625, 111, 625, 250, 48, 111, 33, 13, 6250, 1250, 357, 111, 357, 111, 100, 48, 25, 17, 111, 48, 25, 33, 13, 8, 36, 13, 6, 5], 3: [28945, 10000, 2500, 500, 28571, 10000, 1250, 222, 1250, 500, 111, 250, 100, 50, 10000, 2500, 714, 250, 714, 222, 250, 111, 83, 67, 222, 111, 83, 100, 50, 33, 143, 50, 25, 20], 4: [400000]}
