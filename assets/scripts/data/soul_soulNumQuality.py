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
        "randomQuality": 1,
        "randomProp": 1000,
        "soulLevel": 1
    }),
    2: _tools.RODict({
        "ID": 2,
        "randomID": 1,
        "randomQuality": 2,
        "randomProp": 1000,
        "soulLevel": 2
    }),
    3: _tools.RODict({
        "ID": 3,
        "randomID": 1,
        "randomQuality": (1, 1),
        "randomProp": 1000,
        "soulLevel": 2
    }),
    4: _tools.RODict({
        "ID": 4,
        "randomID": 1,
        "randomQuality": (2, 1),
        "randomProp": 1000,
        "soulLevel": 3
    }),
    5: _tools.RODict({
        "ID": 5,
        "randomID": 1,
        "randomQuality": (1, 1, 1),
        "randomProp": 1000,
        "soulLevel": 3
    }),
    6: _tools.RODict({
        "ID": 6,
        "randomID": 1,
        "randomQuality": (2, 2),
        "randomProp": 1000,
        "soulLevel": 4
    }),
    7: _tools.RODict({
        "ID": 7,
        "randomID": 1,
        "randomQuality": (2, 1, 1),
        "randomProp": 1000,
        "soulLevel": 4
    }),
    8: _tools.RODict({
        "ID": 8,
        "randomID": 1,
        "randomQuality": 3,
        "randomProp": 1000,
        "soulLevel": 5
    }),
    9: _tools.RODict({
        "ID": 9,
        "randomID": 1,
        "randomQuality": (2, 2, 1),
        "randomProp": 1000,
        "soulLevel": 5
    }),
    10: _tools.RODict({
        "ID": 10,
        "randomID": 1,
        "randomQuality": (3, 1),
        "randomProp": 1000,
        "soulLevel": 6
    }),
    11: _tools.RODict({
        "ID": 11,
        "randomID": 1,
        "randomQuality": (2, 2, 2),
        "randomProp": 1000,
        "soulLevel": 6
    }),
    12: _tools.RODict({
        "ID": 12,
        "randomID": 1,
        "randomQuality": (3, 2),
        "randomProp": 1000,
        "soulLevel": 7
    }),
    13: _tools.RODict({
        "ID": 13,
        "randomID": 1,
        "randomQuality": (3, 1, 1),
        "randomProp": 1000,
        "soulLevel": 7
    }),
    14: _tools.RODict({
        "ID": 14,
        "randomID": 1,
        "randomQuality": 4,
        "randomProp": 1000,
        "soulLevel": 8
    }),
    15: _tools.RODict({
        "ID": 15,
        "randomID": 1,
        "randomQuality": (3, 2, 1),
        "randomProp": 1000,
        "soulLevel": 8
    }),
    16: _tools.RODict({
        "ID": 16,
        "randomID": 1,
        "randomQuality": (4, 1),
        "randomProp": 1000,
        "soulLevel": 9
    }),
    17: _tools.RODict({
        "ID": 17,
        "randomID": 1,
        "randomQuality": (3, 2, 2),
        "randomProp": 1000,
        "soulLevel": 9
    }),
    18: _tools.RODict({
        "ID": 18,
        "randomID": 1,
        "randomQuality": (4, 2),
        "randomProp": 1000,
        "soulLevel": 10
    }),
    19: _tools.RODict({
        "ID": 19,
        "randomID": 1,
        "randomQuality": (3, 3),
        "randomProp": 1000,
        "soulLevel": 10
    }),
    20: _tools.RODict({
        "ID": 20,
        "randomID": 1,
        "randomQuality": (4, 1, 1),
        "randomProp": 1000,
        "soulLevel": 10
    }),
    21: _tools.RODict({
        "ID": 21,
        "randomID": 1,
        "randomQuality": (4, 2, 1),
        "randomProp": 1000,
        "soulLevel": 11
    }),
    22: _tools.RODict({
        "ID": 22,
        "randomID": 1,
        "randomQuality": (3, 3, 1),
        "randomProp": 1000,
        "soulLevel": 11
    }),
    23: _tools.RODict({
        "ID": 23,
        "randomID": 1,
        "randomQuality": (4, 2, 2),
        "randomProp": 1000,
        "soulLevel": 12
    }),
    24: _tools.RODict({
        "ID": 24,
        "randomID": 1,
        "randomQuality": (3, 3, 2),
        "randomProp": 1000,
        "soulLevel": 12
    }),
    25: _tools.RODict({
        "ID": 25,
        "randomID": 1,
        "randomQuality": (4, 3),
        "randomProp": 1000,
        "soulLevel": 13
    }),
    26: _tools.RODict({
        "ID": 26,
        "randomID": 2,
        "randomQuality": 1,
        "randomProp": 1000,
        "soulLevel": 1
    }),
    27: _tools.RODict({
        "ID": 27,
        "randomID": 2,
        "randomQuality": 2,
        "randomProp": 1000,
        "soulLevel": 2
    }),
    28: _tools.RODict({
        "ID": 28,
        "randomID": 2,
        "randomQuality": (1, 1),
        "randomProp": 1000,
        "soulLevel": 2
    }),
    29: _tools.RODict({
        "ID": 29,
        "randomID": 2,
        "randomQuality": (2, 1),
        "randomProp": 1000,
        "soulLevel": 3
    }),
    30: _tools.RODict({
        "ID": 30,
        "randomID": 2,
        "randomQuality": (1, 1, 1),
        "randomProp": 1000,
        "soulLevel": 3
    }),
    31: _tools.RODict({
        "ID": 31,
        "randomID": 2,
        "randomQuality": (2, 2),
        "randomProp": 1000,
        "soulLevel": 4
    }),
    32: _tools.RODict({
        "ID": 32,
        "randomID": 2,
        "randomQuality": (2, 1, 1),
        "randomProp": 1000,
        "soulLevel": 4
    }),
    33: _tools.RODict({
        "ID": 33,
        "randomID": 2,
        "randomQuality": 3,
        "randomProp": 1000,
        "soulLevel": 5
    }),
    34: _tools.RODict({
        "ID": 34,
        "randomID": 2,
        "randomQuality": (2, 2, 1),
        "randomProp": 1000,
        "soulLevel": 5
    }),
    35: _tools.RODict({
        "ID": 35,
        "randomID": 2,
        "randomQuality": (3, 1),
        "randomProp": 1000,
        "soulLevel": 6
    }),
    36: _tools.RODict({
        "ID": 36,
        "randomID": 2,
        "randomQuality": (2, 2, 2),
        "randomProp": 1000,
        "soulLevel": 6
    }),
    37: _tools.RODict({
        "ID": 37,
        "randomID": 2,
        "randomQuality": (3, 2),
        "randomProp": 1000,
        "soulLevel": 7
    }),
    38: _tools.RODict({
        "ID": 38,
        "randomID": 2,
        "randomQuality": (3, 1, 1),
        "randomProp": 1000,
        "soulLevel": 7
    }),
    39: _tools.RODict({
        "ID": 39,
        "randomID": 2,
        "randomQuality": 4,
        "randomProp": 1000,
        "soulLevel": 8
    }),
    40: _tools.RODict({
        "ID": 40,
        "randomID": 2,
        "randomQuality": (3, 2, 1),
        "randomProp": 1000,
        "soulLevel": 8
    }),
    41: _tools.RODict({
        "ID": 41,
        "randomID": 2,
        "randomQuality": (4, 1),
        "randomProp": 1000,
        "soulLevel": 9
    }),
    42: _tools.RODict({
        "ID": 42,
        "randomID": 2,
        "randomQuality": (3, 2, 2),
        "randomProp": 1000,
        "soulLevel": 9
    }),
    43: _tools.RODict({
        "ID": 43,
        "randomID": 2,
        "randomQuality": (4, 2),
        "randomProp": 1000,
        "soulLevel": 10
    }),
    44: _tools.RODict({
        "ID": 44,
        "randomID": 2,
        "randomQuality": (3, 3),
        "randomProp": 1000,
        "soulLevel": 10
    }),
    45: _tools.RODict({
        "ID": 45,
        "randomID": 2,
        "randomQuality": (4, 1, 1),
        "randomProp": 1000,
        "soulLevel": 10
    }),
    46: _tools.RODict({
        "ID": 46,
        "randomID": 2,
        "randomQuality": (4, 2, 1),
        "randomProp": 1000,
        "soulLevel": 11
    }),
    47: _tools.RODict({
        "ID": 47,
        "randomID": 2,
        "randomQuality": (3, 3, 1),
        "randomProp": 1000,
        "soulLevel": 11
    }),
    48: _tools.RODict({
        "ID": 48,
        "randomID": 2,
        "randomQuality": (4, 2, 2),
        "randomProp": 1000,
        "soulLevel": 12
    }),
    49: _tools.RODict({
        "ID": 49,
        "randomID": 2,
        "randomQuality": (3, 3, 2),
        "randomProp": 1000,
        "soulLevel": 12
    }),
    50: _tools.RODict({
        "ID": 50,
        "randomID": 2,
        "randomQuality": (4, 3),
        "randomProp": 1000,
        "soulLevel": 13
    }),
    51: _tools.RODict({
        "ID": 51,
        "randomID": 2,
        "randomQuality": (4, 3, 1),
        "randomProp": 1000,
        "soulLevel": 14
    }),
    52: _tools.RODict({
        "ID": 52,
        "randomID": 2,
        "randomQuality": (4, 3, 2),
        "randomProp": 1000,
        "soulLevel": 15
    }),
    53: _tools.RODict({
        "ID": 53,
        "randomID": 2,
        "randomQuality": (3, 3, 3),
        "randomProp": 1000,
        "soulLevel": 15
    }),
    54: _tools.RODict({
        "ID": 54,
        "randomID": 2,
        "randomQuality": (4, 4),
        "randomProp": 1000,
        "soulLevel": 16
    }),
    55: _tools.RODict({
        "ID": 55,
        "randomID": 2,
        "randomQuality": (4, 4, 1),
        "randomProp": 1000,
        "soulLevel": 17
    }),
    56: _tools.RODict({
        "ID": 56,
        "randomID": 2,
        "randomQuality": (4, 4, 2),
        "randomProp": 1000,
        "soulLevel": 18
    }),
    57: _tools.RODict({
        "ID": 57,
        "randomID": 2,
        "randomQuality": (4, 3, 3),
        "randomProp": 1000,
        "soulLevel": 18
    }),
    58: _tools.RODict({
        "ID": 58,
        "randomID": 3,
        "randomQuality": 1,
        "randomProp": 1000,
        "soulLevel": 1
    }),
    59: _tools.RODict({
        "ID": 59,
        "randomID": 3,
        "randomQuality": 2,
        "randomProp": 1000,
        "soulLevel": 2
    }),
    60: _tools.RODict({
        "ID": 60,
        "randomID": 3,
        "randomQuality": (1, 1),
        "randomProp": 1000,
        "soulLevel": 2
    }),
    61: _tools.RODict({
        "ID": 61,
        "randomID": 3,
        "randomQuality": (2, 1),
        "randomProp": 1000,
        "soulLevel": 3
    }),
    62: _tools.RODict({
        "ID": 62,
        "randomID": 3,
        "randomQuality": (1, 1, 1),
        "randomProp": 1000,
        "soulLevel": 3
    }),
    63: _tools.RODict({
        "ID": 63,
        "randomID": 3,
        "randomQuality": (2, 2),
        "randomProp": 1000,
        "soulLevel": 4
    }),
    64: _tools.RODict({
        "ID": 64,
        "randomID": 3,
        "randomQuality": (2, 1, 1),
        "randomProp": 1000,
        "soulLevel": 4
    }),
    65: _tools.RODict({
        "ID": 65,
        "randomID": 3,
        "randomQuality": 3,
        "randomProp": 1000,
        "soulLevel": 5
    }),
    66: _tools.RODict({
        "ID": 66,
        "randomID": 3,
        "randomQuality": (2, 2, 1),
        "randomProp": 1000,
        "soulLevel": 5
    }),
    67: _tools.RODict({
        "ID": 67,
        "randomID": 3,
        "randomQuality": (3, 1),
        "randomProp": 1000,
        "soulLevel": 6
    }),
    68: _tools.RODict({
        "ID": 68,
        "randomID": 3,
        "randomQuality": (2, 2, 2),
        "randomProp": 1000,
        "soulLevel": 6
    }),
    69: _tools.RODict({
        "ID": 69,
        "randomID": 3,
        "randomQuality": (3, 2),
        "randomProp": 1000,
        "soulLevel": 7
    }),
    70: _tools.RODict({
        "ID": 70,
        "randomID": 3,
        "randomQuality": (3, 1, 1),
        "randomProp": 1000,
        "soulLevel": 7
    }),
    71: _tools.RODict({
        "ID": 71,
        "randomID": 3,
        "randomQuality": 4,
        "randomProp": 1000,
        "soulLevel": 8
    }),
    72: _tools.RODict({
        "ID": 72,
        "randomID": 3,
        "randomQuality": (3, 2, 1),
        "randomProp": 1000,
        "soulLevel": 8
    }),
    73: _tools.RODict({
        "ID": 73,
        "randomID": 3,
        "randomQuality": (4, 1),
        "randomProp": 1000,
        "soulLevel": 9
    }),
    74: _tools.RODict({
        "ID": 74,
        "randomID": 3,
        "randomQuality": (3, 2, 2),
        "randomProp": 1000,
        "soulLevel": 9
    }),
    75: _tools.RODict({
        "ID": 75,
        "randomID": 3,
        "randomQuality": (4, 2),
        "randomProp": 1000,
        "soulLevel": 10
    }),
    76: _tools.RODict({
        "ID": 76,
        "randomID": 3,
        "randomQuality": (3, 3),
        "randomProp": 1000,
        "soulLevel": 10
    }),
    77: _tools.RODict({
        "ID": 77,
        "randomID": 3,
        "randomQuality": (4, 1, 1),
        "randomProp": 1000,
        "soulLevel": 10
    }),
    78: _tools.RODict({
        "ID": 78,
        "randomID": 3,
        "randomQuality": (4, 2, 1),
        "randomProp": 1000,
        "soulLevel": 11
    }),
    79: _tools.RODict({
        "ID": 79,
        "randomID": 3,
        "randomQuality": (3, 3, 1),
        "randomProp": 1000,
        "soulLevel": 11
    }),
    80: _tools.RODict({
        "ID": 80,
        "randomID": 3,
        "randomQuality": (4, 2, 2),
        "randomProp": 1000,
        "soulLevel": 12
    }),
    81: _tools.RODict({
        "ID": 81,
        "randomID": 3,
        "randomQuality": (3, 3, 2),
        "randomProp": 1000,
        "soulLevel": 12
    }),
    82: _tools.RODict({
        "ID": 82,
        "randomID": 3,
        "randomQuality": (4, 3),
        "randomProp": 1000,
        "soulLevel": 13
    }),
    83: _tools.RODict({
        "ID": 83,
        "randomID": 3,
        "randomQuality": (4, 3, 1),
        "randomProp": 1000,
        "soulLevel": 14
    }),
    84: _tools.RODict({
        "ID": 84,
        "randomID": 3,
        "randomQuality": (4, 3, 2),
        "randomProp": 1000,
        "soulLevel": 15
    }),
    85: _tools.RODict({
        "ID": 85,
        "randomID": 3,
        "randomQuality": (3, 3, 3),
        "randomProp": 1000,
        "soulLevel": 15
    }),
    86: _tools.RODict({
        "ID": 86,
        "randomID": 3,
        "randomQuality": (4, 4),
        "randomProp": 1000,
        "soulLevel": 16
    }),
    87: _tools.RODict({
        "ID": 87,
        "randomID": 3,
        "randomQuality": (4, 4, 1),
        "randomProp": 1000,
        "soulLevel": 17
    }),
    88: _tools.RODict({
        "ID": 88,
        "randomID": 3,
        "randomQuality": (4, 4, 2),
        "randomProp": 1000,
        "soulLevel": 18
    }),
    89: _tools.RODict({
        "ID": 89,
        "randomID": 3,
        "randomQuality": (4, 3, 3),
        "randomProp": 1000,
        "soulLevel": 18
    }),
    90: _tools.RODict({
        "ID": 90,
        "randomID": 3,
        "randomQuality": (4, 4, 3),
        "randomProp": 1000,
        "soulLevel": 21
    }),
    91: _tools.RODict({
        "ID": 91,
        "randomID": 3,
        "randomQuality": (4, 4, 4),
        "randomProp": 1000,
        "soulLevel": 24
    }),
    92: _tools.RODict({
        "ID": 92,
        "randomID": 4,
        "randomQuality": 2,
        "randomProp": 1000,
        "soulLevel": 2
    }),
    93: _tools.RODict({
        "ID": 93,
        "randomID": 4,
        "randomQuality": 1,
        "randomProp": 1000,
        "soulLevel": 1
    }),
    94: _tools.RODict({
        "ID": 94,
        "randomID": 4,
        "randomQuality": 3,
        "randomProp": 1000,
        "soulLevel": 5
    })
})
minKey = 1
maxKey = 94

randomID2qualityStr = {1: ['1', '2', '1,1', '2,1', '1,1,1', '2,2', '2,1,1', '3', '2,2,1', '3,1', '2,2,2', '3,2', '3,1,1', '4', '3,2,1', '4,1', '3,2,2', '4,2', '3,3', '4,1,1', '4,2,1', '3,3,1', '4,2,2', '3,3,2', '4,3'], 2: ['1', '2', '1,1', '2,1', '1,1,1', '2,2', '2,1,1', '3', '2,2,1', '3,1', '2,2,2', '3,2', '3,1,1', '4', '3,2,1', '4,1', '3,2,2', '4,2', '3,3', '4,1,1', '4,2,1', '3,3,1', '4,2,2', '3,3,2', '4,3', '4,3,1', '4,3,2', '3,3,3', '4,4', '4,4,1', '4,4,2', '4,3,3'], 3: ['1', '2', '1,1', '2,1', '1,1,1', '2,2', '2,1,1', '3', '2,2,1', '3,1', '2,2,2', '3,2', '3,1,1', '4', '3,2,1', '4,1', '3,2,2', '4,2', '3,3', '4,1,1', '4,2,1', '3,3,1', '4,2,2', '3,3,2', '4,3', '4,3,1', '4,3,2', '3,3,3', '4,4', '4,4,1', '4,4,2', '4,3,3', '4,4,3', '4,4,4'], 4: ['2', '1', '3']}


randomID2weight = {1: [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000], 2: [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000], 3: [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000], 4: [1000, 1000, 1000]}


randomID2levelQuality = {1: {1: [[(1,)], [1000]], 2: [[(2,), (1, 1)], [1000, 1000]], 3: [[(2, 1), (1, 1, 1)], [1000, 1000]], 4: [[(2, 2), (2, 1, 1)], [1000, 1000]], 5: [[(3,), (2, 2, 1)], [1000, 1000]], 6: [[(3, 1), (2, 2, 2)], [1000, 1000]], 7: [[(3, 2), (3, 1, 1)], [1000, 1000]], 8: [[(4,), (3, 2, 1)], [1000, 1000]], 9: [[(4, 1), (3, 2, 2)], [1000, 1000]], 10: [[(4, 2), (3, 3), (4, 1, 1)], [1000, 1000, 1000]], 11: [[(4, 2, 1), (3, 3, 1)], [1000, 1000]], 12: [[(4, 2, 2), (3, 3, 2)], [1000, 1000]], 13: [[(4, 3)], [1000]]}, 2: {1: [[(1,)], [1000]], 2: [[(2,), (1, 1)], [1000, 1000]], 3: [[(2, 1), (1, 1, 1)], [1000, 1000]], 4: [[(2, 2), (2, 1, 1)], [1000, 1000]], 5: [[(3,), (2, 2, 1)], [1000, 1000]], 6: [[(3, 1), (2, 2, 2)], [1000, 1000]], 7: [[(3, 2), (3, 1, 1)], [1000, 1000]], 8: [[(4,), (3, 2, 1)], [1000, 1000]], 9: [[(4, 1), (3, 2, 2)], [1000, 1000]], 10: [[(4, 2), (3, 3), (4, 1, 1)], [1000, 1000, 1000]], 11: [[(4, 2, 1), (3, 3, 1)], [1000, 1000]], 12: [[(4, 2, 2), (3, 3, 2)], [1000, 1000]], 13: [[(4, 3)], [1000]], 14: [[(4, 3, 1)], [1000]], 15: [[(4, 3, 2), (3, 3, 3)], [1000, 1000]], 16: [[(4, 4)], [1000]], 17: [[(4, 4, 1)], [1000]], 18: [[(4, 4, 2), (4, 3, 3)], [1000, 1000]]}, 3: {1: [[(1,)], [1000]], 2: [[(2,), (1, 1)], [1000, 1000]], 3: [[(2, 1), (1, 1, 1)], [1000, 1000]], 4: [[(2, 2), (2, 1, 1)], [1000, 1000]], 5: [[(3,), (2, 2, 1)], [1000, 1000]], 6: [[(3, 1), (2, 2, 2)], [1000, 1000]], 7: [[(3, 2), (3, 1, 1)], [1000, 1000]], 8: [[(4,), (3, 2, 1)], [1000, 1000]], 9: [[(4, 1), (3, 2, 2)], [1000, 1000]], 10: [[(4, 2), (3, 3), (4, 1, 1)], [1000, 1000, 1000]], 11: [[(4, 2, 1), (3, 3, 1)], [1000, 1000]], 12: [[(4, 2, 2), (3, 3, 2)], [1000, 1000]], 13: [[(4, 3)], [1000]], 14: [[(4, 3, 1)], [1000]], 15: [[(4, 3, 2), (3, 3, 3)], [1000, 1000]], 16: [[(4, 4)], [1000]], 17: [[(4, 4, 1)], [1000]], 18: [[(4, 4, 2), (4, 3, 3)], [1000, 1000]], 21: [[(4, 4, 3)], [1000]], 24: [[(4, 4, 4)], [1000]]}, 4: {2: [[(2,)], [1000]], 1: [[(1,)], [1000]], 5: [[(3,)], [1000]]}}


randomID2levels = {1: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], 2: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18], 3: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 21, 24], 4: [1, 2, 5]}


randomID2qualityLevel = {1: {'1': 1, '2': 2, '1,1': 2, '2,1': 3, '1,1,1': 3, '2,2': 4, '2,1,1': 4, '3': 5, '2,2,1': 5, '3,1': 6, '2,2,2': 6, '3,2': 7, '3,1,1': 7, '4': 8, '3,2,1': 8, '4,1': 9, '3,2,2': 9, '4,2': 10, '3,3': 10, '4,1,1': 10, '4,2,1': 11, '3,3,1': 11, '4,2,2': 12, '3,3,2': 12, '4,3': 13}, 2: {'1': 1, '2': 2, '1,1': 2, '2,1': 3, '1,1,1': 3, '2,2': 4, '2,1,1': 4, '3': 5, '2,2,1': 5, '3,1': 6, '2,2,2': 6, '3,2': 7, '3,1,1': 7, '4': 8, '3,2,1': 8, '4,1': 9, '3,2,2': 9, '4,2': 10, '3,3': 10, '4,1,1': 10, '4,2,1': 11, '3,3,1': 11, '4,2,2': 12, '3,3,2': 12, '4,3': 13, '4,3,1': 14, '4,3,2': 15, '3,3,3': 15, '4,4': 16, '4,4,1': 17, '4,4,2': 18, '4,3,3': 18}, 3: {'1': 1, '2': 2, '1,1': 2, '2,1': 3, '1,1,1': 3, '2,2': 4, '2,1,1': 4, '3': 5, '2,2,1': 5, '3,1': 6, '2,2,2': 6, '3,2': 7, '3,1,1': 7, '4': 8, '3,2,1': 8, '4,1': 9, '3,2,2': 9, '4,2': 10, '3,3': 10, '4,1,1': 10, '4,2,1': 11, '3,3,1': 11, '4,2,2': 12, '3,3,2': 12, '4,3': 13, '4,3,1': 14, '4,3,2': 15, '3,3,3': 15, '4,4': 16, '4,4,1': 17, '4,4,2': 18, '4,3,3': 18, '4,4,3': 21, '4,4,4': 24}, 4: {'2': 2, '1': 1, '3': 5}}
