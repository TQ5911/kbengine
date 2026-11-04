# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: soul/rareSoulNumQuality
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
        "soulLevel": 1,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 82400
    }),
    2: _tools.RODict({
        "ID": 2,
        "randomID": 1,
        "soulLevel": 1,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 10000
    }),
    3: _tools.RODict({
        "ID": 3,
        "randomID": 1,
        "soulLevel": 1,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 6000
    }),
    4: _tools.RODict({
        "ID": 4,
        "randomID": 1,
        "soulLevel": 1,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 1000
    }),
    5: _tools.RODict({
        "ID": 5,
        "randomID": 1,
        "soulLevel": 1,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 600
    }),
    6: _tools.RODict({
        "ID": 6,
        "randomID": 1,
        "soulLevel": 2,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 74000
    }),
    7: _tools.RODict({
        "ID": 7,
        "randomID": 1,
        "soulLevel": 2,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 15000
    }),
    8: _tools.RODict({
        "ID": 8,
        "randomID": 1,
        "soulLevel": 2,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 9000
    }),
    9: _tools.RODict({
        "ID": 9,
        "randomID": 1,
        "soulLevel": 2,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 1250
    }),
    10: _tools.RODict({
        "ID": 10,
        "randomID": 1,
        "soulLevel": 2,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 750
    }),
    11: _tools.RODict({
        "ID": 11,
        "randomID": 1,
        "soulLevel": 3,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 65600
    }),
    12: _tools.RODict({
        "ID": 12,
        "randomID": 1,
        "soulLevel": 3,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 20000
    }),
    13: _tools.RODict({
        "ID": 13,
        "randomID": 1,
        "soulLevel": 3,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 12000
    }),
    14: _tools.RODict({
        "ID": 14,
        "randomID": 1,
        "soulLevel": 3,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 1500
    }),
    15: _tools.RODict({
        "ID": 15,
        "randomID": 1,
        "soulLevel": 3,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 900
    }),
    16: _tools.RODict({
        "ID": 16,
        "randomID": 1,
        "soulLevel": 4,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 57200
    }),
    17: _tools.RODict({
        "ID": 17,
        "randomID": 1,
        "soulLevel": 4,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 25000
    }),
    18: _tools.RODict({
        "ID": 18,
        "randomID": 1,
        "soulLevel": 4,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 15000
    }),
    19: _tools.RODict({
        "ID": 19,
        "randomID": 1,
        "soulLevel": 4,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 1750
    }),
    20: _tools.RODict({
        "ID": 20,
        "randomID": 1,
        "soulLevel": 4,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 1050
    }),
    21: _tools.RODict({
        "ID": 21,
        "randomID": 1,
        "soulLevel": 5,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 48800
    }),
    22: _tools.RODict({
        "ID": 22,
        "randomID": 1,
        "soulLevel": 5,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 30000
    }),
    23: _tools.RODict({
        "ID": 23,
        "randomID": 1,
        "soulLevel": 5,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 18000
    }),
    24: _tools.RODict({
        "ID": 24,
        "randomID": 1,
        "soulLevel": 5,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 2000
    }),
    25: _tools.RODict({
        "ID": 25,
        "randomID": 1,
        "soulLevel": 5,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 1200
    }),
    26: _tools.RODict({
        "ID": 26,
        "randomID": 1,
        "soulLevel": 6,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 39712
    }),
    27: _tools.RODict({
        "ID": 27,
        "randomID": 1,
        "soulLevel": 6,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 35000
    }),
    28: _tools.RODict({
        "ID": 28,
        "randomID": 1,
        "soulLevel": 6,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 21000
    }),
    29: _tools.RODict({
        "ID": 29,
        "randomID": 1,
        "soulLevel": 6,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 2250
    }),
    30: _tools.RODict({
        "ID": 30,
        "randomID": 1,
        "soulLevel": 6,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 1350
    }),
    31: _tools.RODict({
        "ID": 31,
        "randomID": 1,
        "soulLevel": 6,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 430
    }),
    32: _tools.RODict({
        "ID": 32,
        "randomID": 1,
        "soulLevel": 6,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 258
    }),
    33: _tools.RODict({
        "ID": 33,
        "randomID": 1,
        "soulLevel": 7,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 31232
    }),
    34: _tools.RODict({
        "ID": 34,
        "randomID": 1,
        "soulLevel": 7,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 40000
    }),
    35: _tools.RODict({
        "ID": 35,
        "randomID": 1,
        "soulLevel": 7,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 24000
    }),
    36: _tools.RODict({
        "ID": 36,
        "randomID": 1,
        "soulLevel": 7,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 2500
    }),
    37: _tools.RODict({
        "ID": 37,
        "randomID": 1,
        "soulLevel": 7,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 1500
    }),
    38: _tools.RODict({
        "ID": 38,
        "randomID": 1,
        "soulLevel": 7,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 480
    }),
    39: _tools.RODict({
        "ID": 39,
        "randomID": 1,
        "soulLevel": 7,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 288
    }),
    40: _tools.RODict({
        "ID": 40,
        "randomID": 1,
        "soulLevel": 8,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 22752
    }),
    41: _tools.RODict({
        "ID": 41,
        "randomID": 1,
        "soulLevel": 8,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 45000
    }),
    42: _tools.RODict({
        "ID": 42,
        "randomID": 1,
        "soulLevel": 8,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 27000
    }),
    43: _tools.RODict({
        "ID": 43,
        "randomID": 1,
        "soulLevel": 8,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 2750
    }),
    44: _tools.RODict({
        "ID": 44,
        "randomID": 1,
        "soulLevel": 8,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 1650
    }),
    45: _tools.RODict({
        "ID": 45,
        "randomID": 1,
        "soulLevel": 8,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 530
    }),
    46: _tools.RODict({
        "ID": 46,
        "randomID": 1,
        "soulLevel": 8,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 318
    }),
    47: _tools.RODict({
        "ID": 47,
        "randomID": 1,
        "soulLevel": 9,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 41030
    }),
    48: _tools.RODict({
        "ID": 48,
        "randomID": 1,
        "soulLevel": 9,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 24618
    }),
    49: _tools.RODict({
        "ID": 49,
        "randomID": 1,
        "soulLevel": 9,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 16950
    }),
    50: _tools.RODict({
        "ID": 50,
        "randomID": 1,
        "soulLevel": 9,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 10170
    }),
    51: _tools.RODict({
        "ID": 51,
        "randomID": 1,
        "soulLevel": 9,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 3390
    }),
    52: _tools.RODict({
        "ID": 52,
        "randomID": 1,
        "soulLevel": 9,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 2034
    }),
    53: _tools.RODict({
        "ID": 53,
        "randomID": 1,
        "soulLevel": 9,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 1130
    }),
    54: _tools.RODict({
        "ID": 54,
        "randomID": 1,
        "soulLevel": 9,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 678
    }),
    55: _tools.RODict({
        "ID": 55,
        "randomID": 1,
        "soulLevel": 10,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 28680
    }),
    56: _tools.RODict({
        "ID": 56,
        "randomID": 1,
        "soulLevel": 10,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 17208
    }),
    57: _tools.RODict({
        "ID": 57,
        "randomID": 1,
        "soulLevel": 10,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 26700
    }),
    58: _tools.RODict({
        "ID": 58,
        "randomID": 1,
        "soulLevel": 10,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 16020
    }),
    59: _tools.RODict({
        "ID": 59,
        "randomID": 1,
        "soulLevel": 10,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 5340
    }),
    60: _tools.RODict({
        "ID": 60,
        "randomID": 1,
        "soulLevel": 10,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 3204
    }),
    61: _tools.RODict({
        "ID": 61,
        "randomID": 1,
        "soulLevel": 10,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 1780
    }),
    62: _tools.RODict({
        "ID": 62,
        "randomID": 1,
        "soulLevel": 10,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 1068
    }),
    63: _tools.RODict({
        "ID": 63,
        "randomID": 1,
        "soulLevel": 11,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 16330
    }),
    64: _tools.RODict({
        "ID": 64,
        "randomID": 1,
        "soulLevel": 11,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 9798
    }),
    65: _tools.RODict({
        "ID": 65,
        "randomID": 1,
        "soulLevel": 11,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 36450
    }),
    66: _tools.RODict({
        "ID": 66,
        "randomID": 1,
        "soulLevel": 11,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 21870
    }),
    67: _tools.RODict({
        "ID": 67,
        "randomID": 1,
        "soulLevel": 11,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 7290
    }),
    68: _tools.RODict({
        "ID": 68,
        "randomID": 1,
        "soulLevel": 11,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 4374
    }),
    69: _tools.RODict({
        "ID": 69,
        "randomID": 1,
        "soulLevel": 11,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 2430
    }),
    70: _tools.RODict({
        "ID": 70,
        "randomID": 1,
        "soulLevel": 11,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 1458
    }),
    71: _tools.RODict({
        "ID": 71,
        "randomID": 1,
        "soulLevel": 12,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 3980
    }),
    72: _tools.RODict({
        "ID": 72,
        "randomID": 1,
        "soulLevel": 12,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 2388
    }),
    73: _tools.RODict({
        "ID": 73,
        "randomID": 1,
        "soulLevel": 12,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 46200
    }),
    74: _tools.RODict({
        "ID": 74,
        "randomID": 1,
        "soulLevel": 12,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 27720
    }),
    75: _tools.RODict({
        "ID": 75,
        "randomID": 1,
        "soulLevel": 12,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 9240
    }),
    76: _tools.RODict({
        "ID": 76,
        "randomID": 1,
        "soulLevel": 12,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 5544
    }),
    77: _tools.RODict({
        "ID": 77,
        "randomID": 1,
        "soulLevel": 12,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 3080
    }),
    78: _tools.RODict({
        "ID": 78,
        "randomID": 1,
        "soulLevel": 12,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 1848
    }),
    79: _tools.RODict({
        "ID": 79,
        "randomID": 1,
        "soulLevel": 13,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 47580
    }),
    80: _tools.RODict({
        "ID": 80,
        "randomID": 1,
        "soulLevel": 13,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 28548
    }),
    81: _tools.RODict({
        "ID": 81,
        "randomID": 1,
        "soulLevel": 13,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 11190
    }),
    82: _tools.RODict({
        "ID": 82,
        "randomID": 1,
        "soulLevel": 13,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 6714
    }),
    83: _tools.RODict({
        "ID": 83,
        "randomID": 1,
        "soulLevel": 13,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 3730
    }),
    84: _tools.RODict({
        "ID": 84,
        "randomID": 1,
        "soulLevel": 13,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 2238
    }),
    85: _tools.RODict({
        "ID": 85,
        "randomID": 1,
        "soulLevel": 14,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 33700
    }),
    86: _tools.RODict({
        "ID": 86,
        "randomID": 1,
        "soulLevel": 14,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 20220
    }),
    87: _tools.RODict({
        "ID": 87,
        "randomID": 1,
        "soulLevel": 14,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 21600
    }),
    88: _tools.RODict({
        "ID": 88,
        "randomID": 1,
        "soulLevel": 14,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 12960
    }),
    89: _tools.RODict({
        "ID": 89,
        "randomID": 1,
        "soulLevel": 14,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 7200
    }),
    90: _tools.RODict({
        "ID": 90,
        "randomID": 1,
        "soulLevel": 14,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 4320
    }),
    91: _tools.RODict({
        "ID": 91,
        "randomID": 1,
        "soulLevel": 15,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 23700
    }),
    92: _tools.RODict({
        "ID": 92,
        "randomID": 1,
        "soulLevel": 15,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 14220
    }),
    93: _tools.RODict({
        "ID": 93,
        "randomID": 1,
        "soulLevel": 15,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 29100
    }),
    94: _tools.RODict({
        "ID": 94,
        "randomID": 1,
        "soulLevel": 15,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 17460
    }),
    95: _tools.RODict({
        "ID": 95,
        "randomID": 1,
        "soulLevel": 15,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 9700
    }),
    96: _tools.RODict({
        "ID": 96,
        "randomID": 1,
        "soulLevel": 15,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 5820
    }),
    97: _tools.RODict({
        "ID": 97,
        "randomID": 1,
        "soulLevel": 16,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 13700
    }),
    98: _tools.RODict({
        "ID": 98,
        "randomID": 1,
        "soulLevel": 16,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 8220
    }),
    99: _tools.RODict({
        "ID": 99,
        "randomID": 1,
        "soulLevel": 16,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 36600
    }),
    100: _tools.RODict({
        "ID": 100,
        "randomID": 1,
        "soulLevel": 16,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 21960
    }),
    101: _tools.RODict({
        "ID": 101,
        "randomID": 1,
        "soulLevel": 16,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 12200
    }),
    102: _tools.RODict({
        "ID": 102,
        "randomID": 1,
        "soulLevel": 16,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 7320
    }),
    103: _tools.RODict({
        "ID": 103,
        "randomID": 1,
        "soulLevel": 17,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 3700
    }),
    104: _tools.RODict({
        "ID": 104,
        "randomID": 1,
        "soulLevel": 17,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 2220
    }),
    105: _tools.RODict({
        "ID": 105,
        "randomID": 1,
        "soulLevel": 17,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 44100
    }),
    106: _tools.RODict({
        "ID": 106,
        "randomID": 1,
        "soulLevel": 17,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 26460
    }),
    107: _tools.RODict({
        "ID": 107,
        "randomID": 1,
        "soulLevel": 17,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 14700
    }),
    108: _tools.RODict({
        "ID": 108,
        "randomID": 1,
        "soulLevel": 17,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 8820
    }),
    109: _tools.RODict({
        "ID": 109,
        "randomID": 1,
        "soulLevel": 18,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 45300
    }),
    110: _tools.RODict({
        "ID": 110,
        "randomID": 1,
        "soulLevel": 18,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 27180
    }),
    111: _tools.RODict({
        "ID": 111,
        "randomID": 1,
        "soulLevel": 18,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 17200
    }),
    112: _tools.RODict({
        "ID": 112,
        "randomID": 1,
        "soulLevel": 18,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 10320
    }),
    113: _tools.RODict({
        "ID": 113,
        "randomID": 1,
        "soulLevel": 19,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 4500
    }),
    114: _tools.RODict({
        "ID": 114,
        "randomID": 1,
        "soulLevel": 19,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 2700
    }),
    115: _tools.RODict({
        "ID": 115,
        "randomID": 1,
        "soulLevel": 19,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 58000
    }),
    116: _tools.RODict({
        "ID": 116,
        "randomID": 1,
        "soulLevel": 19,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 34800
    }),
    117: _tools.RODict({
        "ID": 117,
        "randomID": 1,
        "soulLevel": 20,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 4500
    }),
    118: _tools.RODict({
        "ID": 118,
        "randomID": 1,
        "soulLevel": 20,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 2700
    }),
    119: _tools.RODict({
        "ID": 119,
        "randomID": 1,
        "soulLevel": 20,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 58000
    }),
    120: _tools.RODict({
        "ID": 120,
        "randomID": 1,
        "soulLevel": 20,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 34800
    }),
    121: _tools.RODict({
        "ID": 121,
        "randomID": 1,
        "soulLevel": 21,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 4500
    }),
    122: _tools.RODict({
        "ID": 122,
        "randomID": 1,
        "soulLevel": 21,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 2700
    }),
    123: _tools.RODict({
        "ID": 123,
        "randomID": 1,
        "soulLevel": 21,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 58000
    }),
    124: _tools.RODict({
        "ID": 124,
        "randomID": 1,
        "soulLevel": 21,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 34800
    }),
    125: _tools.RODict({
        "ID": 125,
        "randomID": 1,
        "soulLevel": 22,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 4500
    }),
    126: _tools.RODict({
        "ID": 126,
        "randomID": 1,
        "soulLevel": 22,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 2700
    }),
    127: _tools.RODict({
        "ID": 127,
        "randomID": 1,
        "soulLevel": 22,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 58000
    }),
    128: _tools.RODict({
        "ID": 128,
        "randomID": 1,
        "soulLevel": 22,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 34800
    }),
    129: _tools.RODict({
        "ID": 129,
        "randomID": 1,
        "soulLevel": 23,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 4500
    }),
    130: _tools.RODict({
        "ID": 130,
        "randomID": 1,
        "soulLevel": 23,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 2700
    }),
    131: _tools.RODict({
        "ID": 131,
        "randomID": 1,
        "soulLevel": 23,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 58000
    }),
    132: _tools.RODict({
        "ID": 132,
        "randomID": 1,
        "soulLevel": 23,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 34800
    }),
    133: _tools.RODict({
        "ID": 133,
        "randomID": 1,
        "soulLevel": 24,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 62500
    }),
    134: _tools.RODict({
        "ID": 134,
        "randomID": 1,
        "soulLevel": 24,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 37500
    }),
    135: _tools.RODict({
        "ID": 135,
        "randomID": 2,
        "soulLevel": 1,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 82400
    }),
    136: _tools.RODict({
        "ID": 136,
        "randomID": 2,
        "soulLevel": 1,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 10000
    }),
    137: _tools.RODict({
        "ID": 137,
        "randomID": 2,
        "soulLevel": 1,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 6000
    }),
    138: _tools.RODict({
        "ID": 138,
        "randomID": 2,
        "soulLevel": 1,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 1000
    }),
    139: _tools.RODict({
        "ID": 139,
        "randomID": 2,
        "soulLevel": 1,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 600
    }),
    140: _tools.RODict({
        "ID": 140,
        "randomID": 2,
        "soulLevel": 2,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 74000
    }),
    141: _tools.RODict({
        "ID": 141,
        "randomID": 2,
        "soulLevel": 2,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 15000
    }),
    142: _tools.RODict({
        "ID": 142,
        "randomID": 2,
        "soulLevel": 2,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 9000
    }),
    143: _tools.RODict({
        "ID": 143,
        "randomID": 2,
        "soulLevel": 2,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 1250
    }),
    144: _tools.RODict({
        "ID": 144,
        "randomID": 2,
        "soulLevel": 2,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 750
    }),
    145: _tools.RODict({
        "ID": 145,
        "randomID": 2,
        "soulLevel": 3,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 65600
    }),
    146: _tools.RODict({
        "ID": 146,
        "randomID": 2,
        "soulLevel": 3,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 20000
    }),
    147: _tools.RODict({
        "ID": 147,
        "randomID": 2,
        "soulLevel": 3,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 12000
    }),
    148: _tools.RODict({
        "ID": 148,
        "randomID": 2,
        "soulLevel": 3,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 1500
    }),
    149: _tools.RODict({
        "ID": 149,
        "randomID": 2,
        "soulLevel": 3,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 900
    }),
    150: _tools.RODict({
        "ID": 150,
        "randomID": 2,
        "soulLevel": 4,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 57200
    }),
    151: _tools.RODict({
        "ID": 151,
        "randomID": 2,
        "soulLevel": 4,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 25000
    }),
    152: _tools.RODict({
        "ID": 152,
        "randomID": 2,
        "soulLevel": 4,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 15000
    }),
    153: _tools.RODict({
        "ID": 153,
        "randomID": 2,
        "soulLevel": 4,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 1750
    }),
    154: _tools.RODict({
        "ID": 154,
        "randomID": 2,
        "soulLevel": 4,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 1050
    }),
    155: _tools.RODict({
        "ID": 155,
        "randomID": 2,
        "soulLevel": 5,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 48800
    }),
    156: _tools.RODict({
        "ID": 156,
        "randomID": 2,
        "soulLevel": 5,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 30000
    }),
    157: _tools.RODict({
        "ID": 157,
        "randomID": 2,
        "soulLevel": 5,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 18000
    }),
    158: _tools.RODict({
        "ID": 158,
        "randomID": 2,
        "soulLevel": 5,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 2000
    }),
    159: _tools.RODict({
        "ID": 159,
        "randomID": 2,
        "soulLevel": 5,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 1200
    }),
    160: _tools.RODict({
        "ID": 160,
        "randomID": 2,
        "soulLevel": 6,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 39712
    }),
    161: _tools.RODict({
        "ID": 161,
        "randomID": 2,
        "soulLevel": 6,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 35000
    }),
    162: _tools.RODict({
        "ID": 162,
        "randomID": 2,
        "soulLevel": 6,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 21000
    }),
    163: _tools.RODict({
        "ID": 163,
        "randomID": 2,
        "soulLevel": 6,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 2250
    }),
    164: _tools.RODict({
        "ID": 164,
        "randomID": 2,
        "soulLevel": 6,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 1350
    }),
    165: _tools.RODict({
        "ID": 165,
        "randomID": 2,
        "soulLevel": 6,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 430
    }),
    166: _tools.RODict({
        "ID": 166,
        "randomID": 2,
        "soulLevel": 6,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 258
    }),
    167: _tools.RODict({
        "ID": 167,
        "randomID": 2,
        "soulLevel": 7,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 31232
    }),
    168: _tools.RODict({
        "ID": 168,
        "randomID": 2,
        "soulLevel": 7,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 40000
    }),
    169: _tools.RODict({
        "ID": 169,
        "randomID": 2,
        "soulLevel": 7,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 24000
    }),
    170: _tools.RODict({
        "ID": 170,
        "randomID": 2,
        "soulLevel": 7,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 2500
    }),
    171: _tools.RODict({
        "ID": 171,
        "randomID": 2,
        "soulLevel": 7,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 1500
    }),
    172: _tools.RODict({
        "ID": 172,
        "randomID": 2,
        "soulLevel": 7,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 480
    }),
    173: _tools.RODict({
        "ID": 173,
        "randomID": 2,
        "soulLevel": 7,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 288
    }),
    174: _tools.RODict({
        "ID": 174,
        "randomID": 2,
        "soulLevel": 8,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 22752
    }),
    175: _tools.RODict({
        "ID": 175,
        "randomID": 2,
        "soulLevel": 8,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 45000
    }),
    176: _tools.RODict({
        "ID": 176,
        "randomID": 2,
        "soulLevel": 8,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 27000
    }),
    177: _tools.RODict({
        "ID": 177,
        "randomID": 2,
        "soulLevel": 8,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 2750
    }),
    178: _tools.RODict({
        "ID": 178,
        "randomID": 2,
        "soulLevel": 8,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 1650
    }),
    179: _tools.RODict({
        "ID": 179,
        "randomID": 2,
        "soulLevel": 8,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 530
    }),
    180: _tools.RODict({
        "ID": 180,
        "randomID": 2,
        "soulLevel": 8,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 318
    }),
    181: _tools.RODict({
        "ID": 181,
        "randomID": 2,
        "soulLevel": 9,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 41030
    }),
    182: _tools.RODict({
        "ID": 182,
        "randomID": 2,
        "soulLevel": 9,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 24618
    }),
    183: _tools.RODict({
        "ID": 183,
        "randomID": 2,
        "soulLevel": 9,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 16950
    }),
    184: _tools.RODict({
        "ID": 184,
        "randomID": 2,
        "soulLevel": 9,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 10170
    }),
    185: _tools.RODict({
        "ID": 185,
        "randomID": 2,
        "soulLevel": 9,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 3390
    }),
    186: _tools.RODict({
        "ID": 186,
        "randomID": 2,
        "soulLevel": 9,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 2034
    }),
    187: _tools.RODict({
        "ID": 187,
        "randomID": 2,
        "soulLevel": 9,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 1130
    }),
    188: _tools.RODict({
        "ID": 188,
        "randomID": 2,
        "soulLevel": 9,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 678
    }),
    189: _tools.RODict({
        "ID": 189,
        "randomID": 2,
        "soulLevel": 10,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 28680
    }),
    190: _tools.RODict({
        "ID": 190,
        "randomID": 2,
        "soulLevel": 10,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 17208
    }),
    191: _tools.RODict({
        "ID": 191,
        "randomID": 2,
        "soulLevel": 10,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 26700
    }),
    192: _tools.RODict({
        "ID": 192,
        "randomID": 2,
        "soulLevel": 10,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 16020
    }),
    193: _tools.RODict({
        "ID": 193,
        "randomID": 2,
        "soulLevel": 10,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 5340
    }),
    194: _tools.RODict({
        "ID": 194,
        "randomID": 2,
        "soulLevel": 10,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 3204
    }),
    195: _tools.RODict({
        "ID": 195,
        "randomID": 2,
        "soulLevel": 10,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 1780
    }),
    196: _tools.RODict({
        "ID": 196,
        "randomID": 2,
        "soulLevel": 10,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 1068
    }),
    197: _tools.RODict({
        "ID": 197,
        "randomID": 2,
        "soulLevel": 11,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 16330
    }),
    198: _tools.RODict({
        "ID": 198,
        "randomID": 2,
        "soulLevel": 11,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 9798
    }),
    199: _tools.RODict({
        "ID": 199,
        "randomID": 2,
        "soulLevel": 11,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 36450
    }),
    200: _tools.RODict({
        "ID": 200,
        "randomID": 2,
        "soulLevel": 11,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 21870
    }),
    201: _tools.RODict({
        "ID": 201,
        "randomID": 2,
        "soulLevel": 11,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 7290
    }),
    202: _tools.RODict({
        "ID": 202,
        "randomID": 2,
        "soulLevel": 11,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 4374
    }),
    203: _tools.RODict({
        "ID": 203,
        "randomID": 2,
        "soulLevel": 11,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 2430
    }),
    204: _tools.RODict({
        "ID": 204,
        "randomID": 2,
        "soulLevel": 11,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 1458
    }),
    205: _tools.RODict({
        "ID": 205,
        "randomID": 2,
        "soulLevel": 12,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 3980
    }),
    206: _tools.RODict({
        "ID": 206,
        "randomID": 2,
        "soulLevel": 12,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 2388
    }),
    207: _tools.RODict({
        "ID": 207,
        "randomID": 2,
        "soulLevel": 12,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 46200
    }),
    208: _tools.RODict({
        "ID": 208,
        "randomID": 2,
        "soulLevel": 12,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 27720
    }),
    209: _tools.RODict({
        "ID": 209,
        "randomID": 2,
        "soulLevel": 12,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 9240
    }),
    210: _tools.RODict({
        "ID": 210,
        "randomID": 2,
        "soulLevel": 12,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 5544
    }),
    211: _tools.RODict({
        "ID": 211,
        "randomID": 2,
        "soulLevel": 12,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 3080
    }),
    212: _tools.RODict({
        "ID": 212,
        "randomID": 2,
        "soulLevel": 12,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 1848
    }),
    213: _tools.RODict({
        "ID": 213,
        "randomID": 2,
        "soulLevel": 13,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 47580
    }),
    214: _tools.RODict({
        "ID": 214,
        "randomID": 2,
        "soulLevel": 13,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 28548
    }),
    215: _tools.RODict({
        "ID": 215,
        "randomID": 2,
        "soulLevel": 13,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 11190
    }),
    216: _tools.RODict({
        "ID": 216,
        "randomID": 2,
        "soulLevel": 13,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 6714
    }),
    217: _tools.RODict({
        "ID": 217,
        "randomID": 2,
        "soulLevel": 13,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 3730
    }),
    218: _tools.RODict({
        "ID": 218,
        "randomID": 2,
        "soulLevel": 13,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 2238
    }),
    219: _tools.RODict({
        "ID": 219,
        "randomID": 2,
        "soulLevel": 14,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 33700
    }),
    220: _tools.RODict({
        "ID": 220,
        "randomID": 2,
        "soulLevel": 14,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 20220
    }),
    221: _tools.RODict({
        "ID": 221,
        "randomID": 2,
        "soulLevel": 14,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 21600
    }),
    222: _tools.RODict({
        "ID": 222,
        "randomID": 2,
        "soulLevel": 14,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 12960
    }),
    223: _tools.RODict({
        "ID": 223,
        "randomID": 2,
        "soulLevel": 14,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 7200
    }),
    224: _tools.RODict({
        "ID": 224,
        "randomID": 2,
        "soulLevel": 14,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 4320
    }),
    225: _tools.RODict({
        "ID": 225,
        "randomID": 2,
        "soulLevel": 15,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 23700
    }),
    226: _tools.RODict({
        "ID": 226,
        "randomID": 2,
        "soulLevel": 15,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 14220
    }),
    227: _tools.RODict({
        "ID": 227,
        "randomID": 2,
        "soulLevel": 15,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 29100
    }),
    228: _tools.RODict({
        "ID": 228,
        "randomID": 2,
        "soulLevel": 15,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 17460
    }),
    229: _tools.RODict({
        "ID": 229,
        "randomID": 2,
        "soulLevel": 15,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 9700
    }),
    230: _tools.RODict({
        "ID": 230,
        "randomID": 2,
        "soulLevel": 15,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 5820
    }),
    231: _tools.RODict({
        "ID": 231,
        "randomID": 2,
        "soulLevel": 16,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 13700
    }),
    232: _tools.RODict({
        "ID": 232,
        "randomID": 2,
        "soulLevel": 16,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 8220
    }),
    233: _tools.RODict({
        "ID": 233,
        "randomID": 2,
        "soulLevel": 16,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 36600
    }),
    234: _tools.RODict({
        "ID": 234,
        "randomID": 2,
        "soulLevel": 16,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 21960
    }),
    235: _tools.RODict({
        "ID": 235,
        "randomID": 2,
        "soulLevel": 16,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 12200
    }),
    236: _tools.RODict({
        "ID": 236,
        "randomID": 2,
        "soulLevel": 16,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 7320
    }),
    237: _tools.RODict({
        "ID": 237,
        "randomID": 2,
        "soulLevel": 17,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 3700
    }),
    238: _tools.RODict({
        "ID": 238,
        "randomID": 2,
        "soulLevel": 17,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 2220
    }),
    239: _tools.RODict({
        "ID": 239,
        "randomID": 2,
        "soulLevel": 17,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 44100
    }),
    240: _tools.RODict({
        "ID": 240,
        "randomID": 2,
        "soulLevel": 17,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 26460
    }),
    241: _tools.RODict({
        "ID": 241,
        "randomID": 2,
        "soulLevel": 17,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 14700
    }),
    242: _tools.RODict({
        "ID": 242,
        "randomID": 2,
        "soulLevel": 17,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 8820
    }),
    243: _tools.RODict({
        "ID": 243,
        "randomID": 2,
        "soulLevel": 18,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 45300
    }),
    244: _tools.RODict({
        "ID": 244,
        "randomID": 2,
        "soulLevel": 18,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 27180
    }),
    245: _tools.RODict({
        "ID": 245,
        "randomID": 2,
        "soulLevel": 18,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 17200
    }),
    246: _tools.RODict({
        "ID": 246,
        "randomID": 2,
        "soulLevel": 18,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 10320
    }),
    247: _tools.RODict({
        "ID": 247,
        "randomID": 2,
        "soulLevel": 19,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 4500
    }),
    248: _tools.RODict({
        "ID": 248,
        "randomID": 2,
        "soulLevel": 19,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 2700
    }),
    249: _tools.RODict({
        "ID": 249,
        "randomID": 2,
        "soulLevel": 19,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 58000
    }),
    250: _tools.RODict({
        "ID": 250,
        "randomID": 2,
        "soulLevel": 19,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 34800
    }),
    251: _tools.RODict({
        "ID": 251,
        "randomID": 2,
        "soulLevel": 20,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 4500
    }),
    252: _tools.RODict({
        "ID": 252,
        "randomID": 2,
        "soulLevel": 20,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 2700
    }),
    253: _tools.RODict({
        "ID": 253,
        "randomID": 2,
        "soulLevel": 20,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 58000
    }),
    254: _tools.RODict({
        "ID": 254,
        "randomID": 2,
        "soulLevel": 20,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 34800
    }),
    255: _tools.RODict({
        "ID": 255,
        "randomID": 2,
        "soulLevel": 21,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 4500
    }),
    256: _tools.RODict({
        "ID": 256,
        "randomID": 2,
        "soulLevel": 21,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 2700
    }),
    257: _tools.RODict({
        "ID": 257,
        "randomID": 2,
        "soulLevel": 21,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 58000
    }),
    258: _tools.RODict({
        "ID": 258,
        "randomID": 2,
        "soulLevel": 21,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 34800
    }),
    259: _tools.RODict({
        "ID": 259,
        "randomID": 2,
        "soulLevel": 22,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 4500
    }),
    260: _tools.RODict({
        "ID": 260,
        "randomID": 2,
        "soulLevel": 22,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 2700
    }),
    261: _tools.RODict({
        "ID": 261,
        "randomID": 2,
        "soulLevel": 22,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 58000
    }),
    262: _tools.RODict({
        "ID": 262,
        "randomID": 2,
        "soulLevel": 22,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 34800
    }),
    263: _tools.RODict({
        "ID": 263,
        "randomID": 2,
        "soulLevel": 23,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 4500
    }),
    264: _tools.RODict({
        "ID": 264,
        "randomID": 2,
        "soulLevel": 23,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 2700
    }),
    265: _tools.RODict({
        "ID": 265,
        "randomID": 2,
        "soulLevel": 23,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 58000
    }),
    266: _tools.RODict({
        "ID": 266,
        "randomID": 2,
        "soulLevel": 23,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 34800
    }),
    267: _tools.RODict({
        "ID": 267,
        "randomID": 2,
        "soulLevel": 24,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 62500
    }),
    268: _tools.RODict({
        "ID": 268,
        "randomID": 2,
        "soulLevel": 24,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 37500
    }),
    269: _tools.RODict({
        "ID": 269,
        "randomID": 3,
        "soulLevel": 1,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 82400
    }),
    270: _tools.RODict({
        "ID": 270,
        "randomID": 3,
        "soulLevel": 1,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 10000
    }),
    271: _tools.RODict({
        "ID": 271,
        "randomID": 3,
        "soulLevel": 1,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 6000
    }),
    272: _tools.RODict({
        "ID": 272,
        "randomID": 3,
        "soulLevel": 1,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 1000
    }),
    273: _tools.RODict({
        "ID": 273,
        "randomID": 3,
        "soulLevel": 1,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 600
    }),
    274: _tools.RODict({
        "ID": 274,
        "randomID": 3,
        "soulLevel": 2,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 74000
    }),
    275: _tools.RODict({
        "ID": 275,
        "randomID": 3,
        "soulLevel": 2,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 15000
    }),
    276: _tools.RODict({
        "ID": 276,
        "randomID": 3,
        "soulLevel": 2,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 9000
    }),
    277: _tools.RODict({
        "ID": 277,
        "randomID": 3,
        "soulLevel": 2,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 1250
    }),
    278: _tools.RODict({
        "ID": 278,
        "randomID": 3,
        "soulLevel": 2,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 750
    }),
    279: _tools.RODict({
        "ID": 279,
        "randomID": 3,
        "soulLevel": 3,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 65600
    }),
    280: _tools.RODict({
        "ID": 280,
        "randomID": 3,
        "soulLevel": 3,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 20000
    }),
    281: _tools.RODict({
        "ID": 281,
        "randomID": 3,
        "soulLevel": 3,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 12000
    }),
    282: _tools.RODict({
        "ID": 282,
        "randomID": 3,
        "soulLevel": 3,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 1500
    }),
    283: _tools.RODict({
        "ID": 283,
        "randomID": 3,
        "soulLevel": 3,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 900
    }),
    284: _tools.RODict({
        "ID": 284,
        "randomID": 3,
        "soulLevel": 4,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 57200
    }),
    285: _tools.RODict({
        "ID": 285,
        "randomID": 3,
        "soulLevel": 4,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 25000
    }),
    286: _tools.RODict({
        "ID": 286,
        "randomID": 3,
        "soulLevel": 4,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 15000
    }),
    287: _tools.RODict({
        "ID": 287,
        "randomID": 3,
        "soulLevel": 4,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 1750
    }),
    288: _tools.RODict({
        "ID": 288,
        "randomID": 3,
        "soulLevel": 4,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 1050
    }),
    289: _tools.RODict({
        "ID": 289,
        "randomID": 3,
        "soulLevel": 5,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 48800
    }),
    290: _tools.RODict({
        "ID": 290,
        "randomID": 3,
        "soulLevel": 5,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 30000
    }),
    291: _tools.RODict({
        "ID": 291,
        "randomID": 3,
        "soulLevel": 5,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 18000
    }),
    292: _tools.RODict({
        "ID": 292,
        "randomID": 3,
        "soulLevel": 5,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 2000
    }),
    293: _tools.RODict({
        "ID": 293,
        "randomID": 3,
        "soulLevel": 5,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 1200
    }),
    294: _tools.RODict({
        "ID": 294,
        "randomID": 3,
        "soulLevel": 6,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 39712
    }),
    295: _tools.RODict({
        "ID": 295,
        "randomID": 3,
        "soulLevel": 6,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 35000
    }),
    296: _tools.RODict({
        "ID": 296,
        "randomID": 3,
        "soulLevel": 6,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 21000
    }),
    297: _tools.RODict({
        "ID": 297,
        "randomID": 3,
        "soulLevel": 6,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 2250
    }),
    298: _tools.RODict({
        "ID": 298,
        "randomID": 3,
        "soulLevel": 6,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 1350
    }),
    299: _tools.RODict({
        "ID": 299,
        "randomID": 3,
        "soulLevel": 6,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 430
    }),
    300: _tools.RODict({
        "ID": 300,
        "randomID": 3,
        "soulLevel": 6,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 258
    }),
    301: _tools.RODict({
        "ID": 301,
        "randomID": 3,
        "soulLevel": 7,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 31232
    }),
    302: _tools.RODict({
        "ID": 302,
        "randomID": 3,
        "soulLevel": 7,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 40000
    }),
    303: _tools.RODict({
        "ID": 303,
        "randomID": 3,
        "soulLevel": 7,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 24000
    }),
    304: _tools.RODict({
        "ID": 304,
        "randomID": 3,
        "soulLevel": 7,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 2500
    }),
    305: _tools.RODict({
        "ID": 305,
        "randomID": 3,
        "soulLevel": 7,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 1500
    }),
    306: _tools.RODict({
        "ID": 306,
        "randomID": 3,
        "soulLevel": 7,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 480
    }),
    307: _tools.RODict({
        "ID": 307,
        "randomID": 3,
        "soulLevel": 7,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 288
    }),
    308: _tools.RODict({
        "ID": 308,
        "randomID": 3,
        "soulLevel": 8,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 22752
    }),
    309: _tools.RODict({
        "ID": 309,
        "randomID": 3,
        "soulLevel": 8,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 45000
    }),
    310: _tools.RODict({
        "ID": 310,
        "randomID": 3,
        "soulLevel": 8,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 27000
    }),
    311: _tools.RODict({
        "ID": 311,
        "randomID": 3,
        "soulLevel": 8,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 2750
    }),
    312: _tools.RODict({
        "ID": 312,
        "randomID": 3,
        "soulLevel": 8,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 1650
    }),
    313: _tools.RODict({
        "ID": 313,
        "randomID": 3,
        "soulLevel": 8,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 530
    }),
    314: _tools.RODict({
        "ID": 314,
        "randomID": 3,
        "soulLevel": 8,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 318
    }),
    315: _tools.RODict({
        "ID": 315,
        "randomID": 3,
        "soulLevel": 9,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 41030
    }),
    316: _tools.RODict({
        "ID": 316,
        "randomID": 3,
        "soulLevel": 9,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 24618
    }),
    317: _tools.RODict({
        "ID": 317,
        "randomID": 3,
        "soulLevel": 9,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 16950
    }),
    318: _tools.RODict({
        "ID": 318,
        "randomID": 3,
        "soulLevel": 9,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 10170
    }),
    319: _tools.RODict({
        "ID": 319,
        "randomID": 3,
        "soulLevel": 9,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 3390
    }),
    320: _tools.RODict({
        "ID": 320,
        "randomID": 3,
        "soulLevel": 9,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 2034
    }),
    321: _tools.RODict({
        "ID": 321,
        "randomID": 3,
        "soulLevel": 9,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 1130
    }),
    322: _tools.RODict({
        "ID": 322,
        "randomID": 3,
        "soulLevel": 9,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 678
    }),
    323: _tools.RODict({
        "ID": 323,
        "randomID": 3,
        "soulLevel": 10,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 28680
    }),
    324: _tools.RODict({
        "ID": 324,
        "randomID": 3,
        "soulLevel": 10,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 17208
    }),
    325: _tools.RODict({
        "ID": 325,
        "randomID": 3,
        "soulLevel": 10,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 26700
    }),
    326: _tools.RODict({
        "ID": 326,
        "randomID": 3,
        "soulLevel": 10,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 16020
    }),
    327: _tools.RODict({
        "ID": 327,
        "randomID": 3,
        "soulLevel": 10,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 5340
    }),
    328: _tools.RODict({
        "ID": 328,
        "randomID": 3,
        "soulLevel": 10,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 3204
    }),
    329: _tools.RODict({
        "ID": 329,
        "randomID": 3,
        "soulLevel": 10,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 1780
    }),
    330: _tools.RODict({
        "ID": 330,
        "randomID": 3,
        "soulLevel": 10,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 1068
    }),
    331: _tools.RODict({
        "ID": 331,
        "randomID": 3,
        "soulLevel": 11,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 16330
    }),
    332: _tools.RODict({
        "ID": 332,
        "randomID": 3,
        "soulLevel": 11,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 9798
    }),
    333: _tools.RODict({
        "ID": 333,
        "randomID": 3,
        "soulLevel": 11,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 36450
    }),
    334: _tools.RODict({
        "ID": 334,
        "randomID": 3,
        "soulLevel": 11,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 21870
    }),
    335: _tools.RODict({
        "ID": 335,
        "randomID": 3,
        "soulLevel": 11,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 7290
    }),
    336: _tools.RODict({
        "ID": 336,
        "randomID": 3,
        "soulLevel": 11,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 4374
    }),
    337: _tools.RODict({
        "ID": 337,
        "randomID": 3,
        "soulLevel": 11,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 2430
    }),
    338: _tools.RODict({
        "ID": 338,
        "randomID": 3,
        "soulLevel": 11,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 1458
    }),
    339: _tools.RODict({
        "ID": 339,
        "randomID": 3,
        "soulLevel": 12,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 3980
    }),
    340: _tools.RODict({
        "ID": 340,
        "randomID": 3,
        "soulLevel": 12,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 2388
    }),
    341: _tools.RODict({
        "ID": 341,
        "randomID": 3,
        "soulLevel": 12,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 46200
    }),
    342: _tools.RODict({
        "ID": 342,
        "randomID": 3,
        "soulLevel": 12,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 27720
    }),
    343: _tools.RODict({
        "ID": 343,
        "randomID": 3,
        "soulLevel": 12,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 9240
    }),
    344: _tools.RODict({
        "ID": 344,
        "randomID": 3,
        "soulLevel": 12,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 5544
    }),
    345: _tools.RODict({
        "ID": 345,
        "randomID": 3,
        "soulLevel": 12,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 3080
    }),
    346: _tools.RODict({
        "ID": 346,
        "randomID": 3,
        "soulLevel": 12,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 1848
    }),
    347: _tools.RODict({
        "ID": 347,
        "randomID": 3,
        "soulLevel": 13,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 47580
    }),
    348: _tools.RODict({
        "ID": 348,
        "randomID": 3,
        "soulLevel": 13,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 28548
    }),
    349: _tools.RODict({
        "ID": 349,
        "randomID": 3,
        "soulLevel": 13,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 11190
    }),
    350: _tools.RODict({
        "ID": 350,
        "randomID": 3,
        "soulLevel": 13,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 6714
    }),
    351: _tools.RODict({
        "ID": 351,
        "randomID": 3,
        "soulLevel": 13,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 3730
    }),
    352: _tools.RODict({
        "ID": 352,
        "randomID": 3,
        "soulLevel": 13,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 2238
    }),
    353: _tools.RODict({
        "ID": 353,
        "randomID": 3,
        "soulLevel": 14,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 33700
    }),
    354: _tools.RODict({
        "ID": 354,
        "randomID": 3,
        "soulLevel": 14,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 20220
    }),
    355: _tools.RODict({
        "ID": 355,
        "randomID": 3,
        "soulLevel": 14,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 21600
    }),
    356: _tools.RODict({
        "ID": 356,
        "randomID": 3,
        "soulLevel": 14,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 12960
    }),
    357: _tools.RODict({
        "ID": 357,
        "randomID": 3,
        "soulLevel": 14,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 7200
    }),
    358: _tools.RODict({
        "ID": 358,
        "randomID": 3,
        "soulLevel": 14,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 4320
    }),
    359: _tools.RODict({
        "ID": 359,
        "randomID": 3,
        "soulLevel": 15,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 23700
    }),
    360: _tools.RODict({
        "ID": 360,
        "randomID": 3,
        "soulLevel": 15,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 14220
    }),
    361: _tools.RODict({
        "ID": 361,
        "randomID": 3,
        "soulLevel": 15,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 29100
    }),
    362: _tools.RODict({
        "ID": 362,
        "randomID": 3,
        "soulLevel": 15,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 17460
    }),
    363: _tools.RODict({
        "ID": 363,
        "randomID": 3,
        "soulLevel": 15,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 9700
    }),
    364: _tools.RODict({
        "ID": 364,
        "randomID": 3,
        "soulLevel": 15,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 5820
    }),
    365: _tools.RODict({
        "ID": 365,
        "randomID": 3,
        "soulLevel": 16,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 13700
    }),
    366: _tools.RODict({
        "ID": 366,
        "randomID": 3,
        "soulLevel": 16,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 8220
    }),
    367: _tools.RODict({
        "ID": 367,
        "randomID": 3,
        "soulLevel": 16,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 36600
    }),
    368: _tools.RODict({
        "ID": 368,
        "randomID": 3,
        "soulLevel": 16,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 21960
    }),
    369: _tools.RODict({
        "ID": 369,
        "randomID": 3,
        "soulLevel": 16,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 12200
    }),
    370: _tools.RODict({
        "ID": 370,
        "randomID": 3,
        "soulLevel": 16,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 7320
    }),
    371: _tools.RODict({
        "ID": 371,
        "randomID": 3,
        "soulLevel": 17,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 3700
    }),
    372: _tools.RODict({
        "ID": 372,
        "randomID": 3,
        "soulLevel": 17,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 2220
    }),
    373: _tools.RODict({
        "ID": 373,
        "randomID": 3,
        "soulLevel": 17,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 44100
    }),
    374: _tools.RODict({
        "ID": 374,
        "randomID": 3,
        "soulLevel": 17,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 26460
    }),
    375: _tools.RODict({
        "ID": 375,
        "randomID": 3,
        "soulLevel": 17,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 14700
    }),
    376: _tools.RODict({
        "ID": 376,
        "randomID": 3,
        "soulLevel": 17,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 8820
    }),
    377: _tools.RODict({
        "ID": 377,
        "randomID": 3,
        "soulLevel": 18,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 45300
    }),
    378: _tools.RODict({
        "ID": 378,
        "randomID": 3,
        "soulLevel": 18,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 27180
    }),
    379: _tools.RODict({
        "ID": 379,
        "randomID": 3,
        "soulLevel": 18,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 17200
    }),
    380: _tools.RODict({
        "ID": 380,
        "randomID": 3,
        "soulLevel": 18,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 10320
    }),
    381: _tools.RODict({
        "ID": 381,
        "randomID": 3,
        "soulLevel": 19,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 4500
    }),
    382: _tools.RODict({
        "ID": 382,
        "randomID": 3,
        "soulLevel": 19,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 2700
    }),
    383: _tools.RODict({
        "ID": 383,
        "randomID": 3,
        "soulLevel": 19,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 58000
    }),
    384: _tools.RODict({
        "ID": 384,
        "randomID": 3,
        "soulLevel": 19,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 34800
    }),
    385: _tools.RODict({
        "ID": 385,
        "randomID": 3,
        "soulLevel": 20,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 4500
    }),
    386: _tools.RODict({
        "ID": 386,
        "randomID": 3,
        "soulLevel": 20,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 2700
    }),
    387: _tools.RODict({
        "ID": 387,
        "randomID": 3,
        "soulLevel": 20,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 58000
    }),
    388: _tools.RODict({
        "ID": 388,
        "randomID": 3,
        "soulLevel": 20,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 34800
    }),
    389: _tools.RODict({
        "ID": 389,
        "randomID": 3,
        "soulLevel": 21,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 4500
    }),
    390: _tools.RODict({
        "ID": 390,
        "randomID": 3,
        "soulLevel": 21,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 2700
    }),
    391: _tools.RODict({
        "ID": 391,
        "randomID": 3,
        "soulLevel": 21,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 58000
    }),
    392: _tools.RODict({
        "ID": 392,
        "randomID": 3,
        "soulLevel": 21,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 34800
    }),
    393: _tools.RODict({
        "ID": 393,
        "randomID": 3,
        "soulLevel": 22,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 4500
    }),
    394: _tools.RODict({
        "ID": 394,
        "randomID": 3,
        "soulLevel": 22,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 2700
    }),
    395: _tools.RODict({
        "ID": 395,
        "randomID": 3,
        "soulLevel": 22,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 58000
    }),
    396: _tools.RODict({
        "ID": 396,
        "randomID": 3,
        "soulLevel": 22,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 34800
    }),
    397: _tools.RODict({
        "ID": 397,
        "randomID": 3,
        "soulLevel": 23,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 4500
    }),
    398: _tools.RODict({
        "ID": 398,
        "randomID": 3,
        "soulLevel": 23,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 2700
    }),
    399: _tools.RODict({
        "ID": 399,
        "randomID": 3,
        "soulLevel": 23,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 58000
    }),
    400: _tools.RODict({
        "ID": 400,
        "randomID": 3,
        "soulLevel": 23,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 34800
    }),
    401: _tools.RODict({
        "ID": 401,
        "randomID": 3,
        "soulLevel": 24,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 62500
    }),
    402: _tools.RODict({
        "ID": 402,
        "randomID": 3,
        "soulLevel": 24,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 37500
    }),
    403: _tools.RODict({
        "ID": 403,
        "randomID": 4,
        "soulLevel": 1,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 82400
    }),
    404: _tools.RODict({
        "ID": 404,
        "randomID": 4,
        "soulLevel": 1,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 10000
    }),
    405: _tools.RODict({
        "ID": 405,
        "randomID": 4,
        "soulLevel": 1,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 6000
    }),
    406: _tools.RODict({
        "ID": 406,
        "randomID": 4,
        "soulLevel": 1,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 1000
    }),
    407: _tools.RODict({
        "ID": 407,
        "randomID": 4,
        "soulLevel": 1,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 600
    }),
    408: _tools.RODict({
        "ID": 408,
        "randomID": 4,
        "soulLevel": 2,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 74000
    }),
    409: _tools.RODict({
        "ID": 409,
        "randomID": 4,
        "soulLevel": 2,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 15000
    }),
    410: _tools.RODict({
        "ID": 410,
        "randomID": 4,
        "soulLevel": 2,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 9000
    }),
    411: _tools.RODict({
        "ID": 411,
        "randomID": 4,
        "soulLevel": 2,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 1250
    }),
    412: _tools.RODict({
        "ID": 412,
        "randomID": 4,
        "soulLevel": 2,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 750
    }),
    413: _tools.RODict({
        "ID": 413,
        "randomID": 4,
        "soulLevel": 3,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 65600
    }),
    414: _tools.RODict({
        "ID": 414,
        "randomID": 4,
        "soulLevel": 3,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 20000
    }),
    415: _tools.RODict({
        "ID": 415,
        "randomID": 4,
        "soulLevel": 3,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 12000
    }),
    416: _tools.RODict({
        "ID": 416,
        "randomID": 4,
        "soulLevel": 3,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 1500
    }),
    417: _tools.RODict({
        "ID": 417,
        "randomID": 4,
        "soulLevel": 3,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 900
    }),
    418: _tools.RODict({
        "ID": 418,
        "randomID": 4,
        "soulLevel": 4,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 57200
    }),
    419: _tools.RODict({
        "ID": 419,
        "randomID": 4,
        "soulLevel": 4,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 25000
    }),
    420: _tools.RODict({
        "ID": 420,
        "randomID": 4,
        "soulLevel": 4,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 15000
    }),
    421: _tools.RODict({
        "ID": 421,
        "randomID": 4,
        "soulLevel": 4,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 1750
    }),
    422: _tools.RODict({
        "ID": 422,
        "randomID": 4,
        "soulLevel": 4,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 1050
    }),
    423: _tools.RODict({
        "ID": 423,
        "randomID": 4,
        "soulLevel": 5,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 48800
    }),
    424: _tools.RODict({
        "ID": 424,
        "randomID": 4,
        "soulLevel": 5,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 30000
    }),
    425: _tools.RODict({
        "ID": 425,
        "randomID": 4,
        "soulLevel": 5,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 18000
    }),
    426: _tools.RODict({
        "ID": 426,
        "randomID": 4,
        "soulLevel": 5,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 2000
    }),
    427: _tools.RODict({
        "ID": 427,
        "randomID": 4,
        "soulLevel": 5,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 1200
    }),
    428: _tools.RODict({
        "ID": 428,
        "randomID": 4,
        "soulLevel": 6,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 39712
    }),
    429: _tools.RODict({
        "ID": 429,
        "randomID": 4,
        "soulLevel": 6,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 35000
    }),
    430: _tools.RODict({
        "ID": 430,
        "randomID": 4,
        "soulLevel": 6,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 21000
    }),
    431: _tools.RODict({
        "ID": 431,
        "randomID": 4,
        "soulLevel": 6,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 2250
    }),
    432: _tools.RODict({
        "ID": 432,
        "randomID": 4,
        "soulLevel": 6,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 1350
    }),
    433: _tools.RODict({
        "ID": 433,
        "randomID": 4,
        "soulLevel": 6,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 430
    }),
    434: _tools.RODict({
        "ID": 434,
        "randomID": 4,
        "soulLevel": 6,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 258
    }),
    435: _tools.RODict({
        "ID": 435,
        "randomID": 4,
        "soulLevel": 7,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 31232
    }),
    436: _tools.RODict({
        "ID": 436,
        "randomID": 4,
        "soulLevel": 7,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 40000
    }),
    437: _tools.RODict({
        "ID": 437,
        "randomID": 4,
        "soulLevel": 7,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 24000
    }),
    438: _tools.RODict({
        "ID": 438,
        "randomID": 4,
        "soulLevel": 7,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 2500
    }),
    439: _tools.RODict({
        "ID": 439,
        "randomID": 4,
        "soulLevel": 7,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 1500
    }),
    440: _tools.RODict({
        "ID": 440,
        "randomID": 4,
        "soulLevel": 7,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 480
    }),
    441: _tools.RODict({
        "ID": 441,
        "randomID": 4,
        "soulLevel": 7,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 288
    }),
    442: _tools.RODict({
        "ID": 442,
        "randomID": 4,
        "soulLevel": 8,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 22752
    }),
    443: _tools.RODict({
        "ID": 443,
        "randomID": 4,
        "soulLevel": 8,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 45000
    }),
    444: _tools.RODict({
        "ID": 444,
        "randomID": 4,
        "soulLevel": 8,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 27000
    }),
    445: _tools.RODict({
        "ID": 445,
        "randomID": 4,
        "soulLevel": 8,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 2750
    }),
    446: _tools.RODict({
        "ID": 446,
        "randomID": 4,
        "soulLevel": 8,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 1650
    }),
    447: _tools.RODict({
        "ID": 447,
        "randomID": 4,
        "soulLevel": 8,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 530
    }),
    448: _tools.RODict({
        "ID": 448,
        "randomID": 4,
        "soulLevel": 8,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 318
    }),
    449: _tools.RODict({
        "ID": 449,
        "randomID": 4,
        "soulLevel": 9,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 41030
    }),
    450: _tools.RODict({
        "ID": 450,
        "randomID": 4,
        "soulLevel": 9,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 24618
    }),
    451: _tools.RODict({
        "ID": 451,
        "randomID": 4,
        "soulLevel": 9,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 16950
    }),
    452: _tools.RODict({
        "ID": 452,
        "randomID": 4,
        "soulLevel": 9,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 10170
    }),
    453: _tools.RODict({
        "ID": 453,
        "randomID": 4,
        "soulLevel": 9,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 3390
    }),
    454: _tools.RODict({
        "ID": 454,
        "randomID": 4,
        "soulLevel": 9,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 2034
    }),
    455: _tools.RODict({
        "ID": 455,
        "randomID": 4,
        "soulLevel": 9,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 1130
    }),
    456: _tools.RODict({
        "ID": 456,
        "randomID": 4,
        "soulLevel": 9,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 678
    }),
    457: _tools.RODict({
        "ID": 457,
        "randomID": 4,
        "soulLevel": 10,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 28680
    }),
    458: _tools.RODict({
        "ID": 458,
        "randomID": 4,
        "soulLevel": 10,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 17208
    }),
    459: _tools.RODict({
        "ID": 459,
        "randomID": 4,
        "soulLevel": 10,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 26700
    }),
    460: _tools.RODict({
        "ID": 460,
        "randomID": 4,
        "soulLevel": 10,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 16020
    }),
    461: _tools.RODict({
        "ID": 461,
        "randomID": 4,
        "soulLevel": 10,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 5340
    }),
    462: _tools.RODict({
        "ID": 462,
        "randomID": 4,
        "soulLevel": 10,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 3204
    }),
    463: _tools.RODict({
        "ID": 463,
        "randomID": 4,
        "soulLevel": 10,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 1780
    }),
    464: _tools.RODict({
        "ID": 464,
        "randomID": 4,
        "soulLevel": 10,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 1068
    }),
    465: _tools.RODict({
        "ID": 465,
        "randomID": 4,
        "soulLevel": 11,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 16330
    }),
    466: _tools.RODict({
        "ID": 466,
        "randomID": 4,
        "soulLevel": 11,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 9798
    }),
    467: _tools.RODict({
        "ID": 467,
        "randomID": 4,
        "soulLevel": 11,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 36450
    }),
    468: _tools.RODict({
        "ID": 468,
        "randomID": 4,
        "soulLevel": 11,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 21870
    }),
    469: _tools.RODict({
        "ID": 469,
        "randomID": 4,
        "soulLevel": 11,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 7290
    }),
    470: _tools.RODict({
        "ID": 470,
        "randomID": 4,
        "soulLevel": 11,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 4374
    }),
    471: _tools.RODict({
        "ID": 471,
        "randomID": 4,
        "soulLevel": 11,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 2430
    }),
    472: _tools.RODict({
        "ID": 472,
        "randomID": 4,
        "soulLevel": 11,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 1458
    }),
    473: _tools.RODict({
        "ID": 473,
        "randomID": 4,
        "soulLevel": 12,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 3980
    }),
    474: _tools.RODict({
        "ID": 474,
        "randomID": 4,
        "soulLevel": 12,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 2388
    }),
    475: _tools.RODict({
        "ID": 475,
        "randomID": 4,
        "soulLevel": 12,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 46200
    }),
    476: _tools.RODict({
        "ID": 476,
        "randomID": 4,
        "soulLevel": 12,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 27720
    }),
    477: _tools.RODict({
        "ID": 477,
        "randomID": 4,
        "soulLevel": 12,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 9240
    }),
    478: _tools.RODict({
        "ID": 478,
        "randomID": 4,
        "soulLevel": 12,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 5544
    }),
    479: _tools.RODict({
        "ID": 479,
        "randomID": 4,
        "soulLevel": 12,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 3080
    }),
    480: _tools.RODict({
        "ID": 480,
        "randomID": 4,
        "soulLevel": 12,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 1848
    }),
    481: _tools.RODict({
        "ID": 481,
        "randomID": 4,
        "soulLevel": 13,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 47580
    }),
    482: _tools.RODict({
        "ID": 482,
        "randomID": 4,
        "soulLevel": 13,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 28548
    }),
    483: _tools.RODict({
        "ID": 483,
        "randomID": 4,
        "soulLevel": 13,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 11190
    }),
    484: _tools.RODict({
        "ID": 484,
        "randomID": 4,
        "soulLevel": 13,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 6714
    }),
    485: _tools.RODict({
        "ID": 485,
        "randomID": 4,
        "soulLevel": 13,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 3730
    }),
    486: _tools.RODict({
        "ID": 486,
        "randomID": 4,
        "soulLevel": 13,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 2238
    }),
    487: _tools.RODict({
        "ID": 487,
        "randomID": 4,
        "soulLevel": 14,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 33700
    }),
    488: _tools.RODict({
        "ID": 488,
        "randomID": 4,
        "soulLevel": 14,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 20220
    }),
    489: _tools.RODict({
        "ID": 489,
        "randomID": 4,
        "soulLevel": 14,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 21600
    }),
    490: _tools.RODict({
        "ID": 490,
        "randomID": 4,
        "soulLevel": 14,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 12960
    }),
    491: _tools.RODict({
        "ID": 491,
        "randomID": 4,
        "soulLevel": 14,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 7200
    }),
    492: _tools.RODict({
        "ID": 492,
        "randomID": 4,
        "soulLevel": 14,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 4320
    }),
    493: _tools.RODict({
        "ID": 493,
        "randomID": 4,
        "soulLevel": 15,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 23700
    }),
    494: _tools.RODict({
        "ID": 494,
        "randomID": 4,
        "soulLevel": 15,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 14220
    }),
    495: _tools.RODict({
        "ID": 495,
        "randomID": 4,
        "soulLevel": 15,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 29100
    }),
    496: _tools.RODict({
        "ID": 496,
        "randomID": 4,
        "soulLevel": 15,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 17460
    }),
    497: _tools.RODict({
        "ID": 497,
        "randomID": 4,
        "soulLevel": 15,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 9700
    }),
    498: _tools.RODict({
        "ID": 498,
        "randomID": 4,
        "soulLevel": 15,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 5820
    }),
    499: _tools.RODict({
        "ID": 499,
        "randomID": 4,
        "soulLevel": 16,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 13700
    }),
    500: _tools.RODict({
        "ID": 500,
        "randomID": 4,
        "soulLevel": 16,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 8220
    }),
    501: _tools.RODict({
        "ID": 501,
        "randomID": 4,
        "soulLevel": 16,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 36600
    }),
    502: _tools.RODict({
        "ID": 502,
        "randomID": 4,
        "soulLevel": 16,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 21960
    }),
    503: _tools.RODict({
        "ID": 503,
        "randomID": 4,
        "soulLevel": 16,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 12200
    }),
    504: _tools.RODict({
        "ID": 504,
        "randomID": 4,
        "soulLevel": 16,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 7320
    }),
    505: _tools.RODict({
        "ID": 505,
        "randomID": 4,
        "soulLevel": 17,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 3700
    }),
    506: _tools.RODict({
        "ID": 506,
        "randomID": 4,
        "soulLevel": 17,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 2220
    }),
    507: _tools.RODict({
        "ID": 507,
        "randomID": 4,
        "soulLevel": 17,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 44100
    }),
    508: _tools.RODict({
        "ID": 508,
        "randomID": 4,
        "soulLevel": 17,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 26460
    }),
    509: _tools.RODict({
        "ID": 509,
        "randomID": 4,
        "soulLevel": 17,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 14700
    }),
    510: _tools.RODict({
        "ID": 510,
        "randomID": 4,
        "soulLevel": 17,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 8820
    }),
    511: _tools.RODict({
        "ID": 511,
        "randomID": 4,
        "soulLevel": 18,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 45300
    }),
    512: _tools.RODict({
        "ID": 512,
        "randomID": 4,
        "soulLevel": 18,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 27180
    }),
    513: _tools.RODict({
        "ID": 513,
        "randomID": 4,
        "soulLevel": 18,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 17200
    }),
    514: _tools.RODict({
        "ID": 514,
        "randomID": 4,
        "soulLevel": 18,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 10320
    }),
    515: _tools.RODict({
        "ID": 515,
        "randomID": 4,
        "soulLevel": 19,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 4500
    }),
    516: _tools.RODict({
        "ID": 516,
        "randomID": 4,
        "soulLevel": 19,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 2700
    }),
    517: _tools.RODict({
        "ID": 517,
        "randomID": 4,
        "soulLevel": 19,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 58000
    }),
    518: _tools.RODict({
        "ID": 518,
        "randomID": 4,
        "soulLevel": 19,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 34800
    }),
    519: _tools.RODict({
        "ID": 519,
        "randomID": 4,
        "soulLevel": 20,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 4500
    }),
    520: _tools.RODict({
        "ID": 520,
        "randomID": 4,
        "soulLevel": 20,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 2700
    }),
    521: _tools.RODict({
        "ID": 521,
        "randomID": 4,
        "soulLevel": 20,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 58000
    }),
    522: _tools.RODict({
        "ID": 522,
        "randomID": 4,
        "soulLevel": 20,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 34800
    }),
    523: _tools.RODict({
        "ID": 523,
        "randomID": 4,
        "soulLevel": 21,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 4500
    }),
    524: _tools.RODict({
        "ID": 524,
        "randomID": 4,
        "soulLevel": 21,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 2700
    }),
    525: _tools.RODict({
        "ID": 525,
        "randomID": 4,
        "soulLevel": 21,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 58000
    }),
    526: _tools.RODict({
        "ID": 526,
        "randomID": 4,
        "soulLevel": 21,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 34800
    }),
    527: _tools.RODict({
        "ID": 527,
        "randomID": 4,
        "soulLevel": 22,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 4500
    }),
    528: _tools.RODict({
        "ID": 528,
        "randomID": 4,
        "soulLevel": 22,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 2700
    }),
    529: _tools.RODict({
        "ID": 529,
        "randomID": 4,
        "soulLevel": 22,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 58000
    }),
    530: _tools.RODict({
        "ID": 530,
        "randomID": 4,
        "soulLevel": 22,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 34800
    }),
    531: _tools.RODict({
        "ID": 531,
        "randomID": 4,
        "soulLevel": 23,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 4500
    }),
    532: _tools.RODict({
        "ID": 532,
        "randomID": 4,
        "soulLevel": 23,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 2700
    }),
    533: _tools.RODict({
        "ID": 533,
        "randomID": 4,
        "soulLevel": 23,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 58000
    }),
    534: _tools.RODict({
        "ID": 534,
        "randomID": 4,
        "soulLevel": 23,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 34800
    }),
    535: _tools.RODict({
        "ID": 535,
        "randomID": 4,
        "soulLevel": 24,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 62500
    }),
    536: _tools.RODict({
        "ID": 536,
        "randomID": 4,
        "soulLevel": 24,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 37500
    }),
    537: _tools.RODict({
        "ID": 537,
        "randomID": 5,
        "soulLevel": 1,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 82400
    }),
    538: _tools.RODict({
        "ID": 538,
        "randomID": 5,
        "soulLevel": 1,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 10000
    }),
    539: _tools.RODict({
        "ID": 539,
        "randomID": 5,
        "soulLevel": 1,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 6000
    }),
    540: _tools.RODict({
        "ID": 540,
        "randomID": 5,
        "soulLevel": 1,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 1000
    }),
    541: _tools.RODict({
        "ID": 541,
        "randomID": 5,
        "soulLevel": 1,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 600
    }),
    542: _tools.RODict({
        "ID": 542,
        "randomID": 5,
        "soulLevel": 2,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 74000
    }),
    543: _tools.RODict({
        "ID": 543,
        "randomID": 5,
        "soulLevel": 2,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 15000
    }),
    544: _tools.RODict({
        "ID": 544,
        "randomID": 5,
        "soulLevel": 2,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 9000
    }),
    545: _tools.RODict({
        "ID": 545,
        "randomID": 5,
        "soulLevel": 2,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 1250
    }),
    546: _tools.RODict({
        "ID": 546,
        "randomID": 5,
        "soulLevel": 2,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 750
    }),
    547: _tools.RODict({
        "ID": 547,
        "randomID": 5,
        "soulLevel": 3,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 65600
    }),
    548: _tools.RODict({
        "ID": 548,
        "randomID": 5,
        "soulLevel": 3,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 20000
    }),
    549: _tools.RODict({
        "ID": 549,
        "randomID": 5,
        "soulLevel": 3,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 12000
    }),
    550: _tools.RODict({
        "ID": 550,
        "randomID": 5,
        "soulLevel": 3,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 1500
    }),
    551: _tools.RODict({
        "ID": 551,
        "randomID": 5,
        "soulLevel": 3,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 900
    }),
    552: _tools.RODict({
        "ID": 552,
        "randomID": 5,
        "soulLevel": 4,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 57200
    }),
    553: _tools.RODict({
        "ID": 553,
        "randomID": 5,
        "soulLevel": 4,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 25000
    }),
    554: _tools.RODict({
        "ID": 554,
        "randomID": 5,
        "soulLevel": 4,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 15000
    }),
    555: _tools.RODict({
        "ID": 555,
        "randomID": 5,
        "soulLevel": 4,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 1750
    }),
    556: _tools.RODict({
        "ID": 556,
        "randomID": 5,
        "soulLevel": 4,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 1050
    }),
    557: _tools.RODict({
        "ID": 557,
        "randomID": 5,
        "soulLevel": 5,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 48800
    }),
    558: _tools.RODict({
        "ID": 558,
        "randomID": 5,
        "soulLevel": 5,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 30000
    }),
    559: _tools.RODict({
        "ID": 559,
        "randomID": 5,
        "soulLevel": 5,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 18000
    }),
    560: _tools.RODict({
        "ID": 560,
        "randomID": 5,
        "soulLevel": 5,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 2000
    }),
    561: _tools.RODict({
        "ID": 561,
        "randomID": 5,
        "soulLevel": 5,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 1200
    }),
    562: _tools.RODict({
        "ID": 562,
        "randomID": 5,
        "soulLevel": 6,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 39712
    }),
    563: _tools.RODict({
        "ID": 563,
        "randomID": 5,
        "soulLevel": 6,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 35000
    }),
    564: _tools.RODict({
        "ID": 564,
        "randomID": 5,
        "soulLevel": 6,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 21000
    }),
    565: _tools.RODict({
        "ID": 565,
        "randomID": 5,
        "soulLevel": 6,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 2250
    }),
    566: _tools.RODict({
        "ID": 566,
        "randomID": 5,
        "soulLevel": 6,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 1350
    }),
    567: _tools.RODict({
        "ID": 567,
        "randomID": 5,
        "soulLevel": 6,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 430
    }),
    568: _tools.RODict({
        "ID": 568,
        "randomID": 5,
        "soulLevel": 6,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 258
    }),
    569: _tools.RODict({
        "ID": 569,
        "randomID": 5,
        "soulLevel": 7,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 31232
    }),
    570: _tools.RODict({
        "ID": 570,
        "randomID": 5,
        "soulLevel": 7,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 40000
    }),
    571: _tools.RODict({
        "ID": 571,
        "randomID": 5,
        "soulLevel": 7,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 24000
    }),
    572: _tools.RODict({
        "ID": 572,
        "randomID": 5,
        "soulLevel": 7,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 2500
    }),
    573: _tools.RODict({
        "ID": 573,
        "randomID": 5,
        "soulLevel": 7,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 1500
    }),
    574: _tools.RODict({
        "ID": 574,
        "randomID": 5,
        "soulLevel": 7,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 480
    }),
    575: _tools.RODict({
        "ID": 575,
        "randomID": 5,
        "soulLevel": 7,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 288
    }),
    576: _tools.RODict({
        "ID": 576,
        "randomID": 5,
        "soulLevel": 8,
        "randomQuality": 0,
        "randomQuality2": 0,
        "randomProp": 22752
    }),
    577: _tools.RODict({
        "ID": 577,
        "randomID": 5,
        "soulLevel": 8,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 45000
    }),
    578: _tools.RODict({
        "ID": 578,
        "randomID": 5,
        "soulLevel": 8,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 27000
    }),
    579: _tools.RODict({
        "ID": 579,
        "randomID": 5,
        "soulLevel": 8,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 2750
    }),
    580: _tools.RODict({
        "ID": 580,
        "randomID": 5,
        "soulLevel": 8,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 1650
    }),
    581: _tools.RODict({
        "ID": 581,
        "randomID": 5,
        "soulLevel": 8,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 530
    }),
    582: _tools.RODict({
        "ID": 582,
        "randomID": 5,
        "soulLevel": 8,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 318
    }),
    583: _tools.RODict({
        "ID": 583,
        "randomID": 5,
        "soulLevel": 9,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 41030
    }),
    584: _tools.RODict({
        "ID": 584,
        "randomID": 5,
        "soulLevel": 9,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 24618
    }),
    585: _tools.RODict({
        "ID": 585,
        "randomID": 5,
        "soulLevel": 9,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 16950
    }),
    586: _tools.RODict({
        "ID": 586,
        "randomID": 5,
        "soulLevel": 9,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 10170
    }),
    587: _tools.RODict({
        "ID": 587,
        "randomID": 5,
        "soulLevel": 9,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 3390
    }),
    588: _tools.RODict({
        "ID": 588,
        "randomID": 5,
        "soulLevel": 9,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 2034
    }),
    589: _tools.RODict({
        "ID": 589,
        "randomID": 5,
        "soulLevel": 9,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 1130
    }),
    590: _tools.RODict({
        "ID": 590,
        "randomID": 5,
        "soulLevel": 9,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 678
    }),
    591: _tools.RODict({
        "ID": 591,
        "randomID": 5,
        "soulLevel": 10,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 28680
    }),
    592: _tools.RODict({
        "ID": 592,
        "randomID": 5,
        "soulLevel": 10,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 17208
    }),
    593: _tools.RODict({
        "ID": 593,
        "randomID": 5,
        "soulLevel": 10,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 26700
    }),
    594: _tools.RODict({
        "ID": 594,
        "randomID": 5,
        "soulLevel": 10,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 16020
    }),
    595: _tools.RODict({
        "ID": 595,
        "randomID": 5,
        "soulLevel": 10,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 5340
    }),
    596: _tools.RODict({
        "ID": 596,
        "randomID": 5,
        "soulLevel": 10,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 3204
    }),
    597: _tools.RODict({
        "ID": 597,
        "randomID": 5,
        "soulLevel": 10,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 1780
    }),
    598: _tools.RODict({
        "ID": 598,
        "randomID": 5,
        "soulLevel": 10,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 1068
    }),
    599: _tools.RODict({
        "ID": 599,
        "randomID": 5,
        "soulLevel": 11,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 16330
    }),
    600: _tools.RODict({
        "ID": 600,
        "randomID": 5,
        "soulLevel": 11,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 9798
    }),
    601: _tools.RODict({
        "ID": 601,
        "randomID": 5,
        "soulLevel": 11,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 36450
    }),
    602: _tools.RODict({
        "ID": 602,
        "randomID": 5,
        "soulLevel": 11,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 21870
    }),
    603: _tools.RODict({
        "ID": 603,
        "randomID": 5,
        "soulLevel": 11,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 7290
    }),
    604: _tools.RODict({
        "ID": 604,
        "randomID": 5,
        "soulLevel": 11,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 4374
    }),
    605: _tools.RODict({
        "ID": 605,
        "randomID": 5,
        "soulLevel": 11,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 2430
    }),
    606: _tools.RODict({
        "ID": 606,
        "randomID": 5,
        "soulLevel": 11,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 1458
    }),
    607: _tools.RODict({
        "ID": 607,
        "randomID": 5,
        "soulLevel": 12,
        "randomQuality": 1,
        "randomQuality2": 0,
        "randomProp": 3980
    }),
    608: _tools.RODict({
        "ID": 608,
        "randomID": 5,
        "soulLevel": 12,
        "randomQuality": 1,
        "randomQuality2": 1,
        "randomProp": 2388
    }),
    609: _tools.RODict({
        "ID": 609,
        "randomID": 5,
        "soulLevel": 12,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 46200
    }),
    610: _tools.RODict({
        "ID": 610,
        "randomID": 5,
        "soulLevel": 12,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 27720
    }),
    611: _tools.RODict({
        "ID": 611,
        "randomID": 5,
        "soulLevel": 12,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 9240
    }),
    612: _tools.RODict({
        "ID": 612,
        "randomID": 5,
        "soulLevel": 12,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 5544
    }),
    613: _tools.RODict({
        "ID": 613,
        "randomID": 5,
        "soulLevel": 12,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 3080
    }),
    614: _tools.RODict({
        "ID": 614,
        "randomID": 5,
        "soulLevel": 12,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 1848
    }),
    615: _tools.RODict({
        "ID": 615,
        "randomID": 5,
        "soulLevel": 13,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 47580
    }),
    616: _tools.RODict({
        "ID": 616,
        "randomID": 5,
        "soulLevel": 13,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 28548
    }),
    617: _tools.RODict({
        "ID": 617,
        "randomID": 5,
        "soulLevel": 13,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 11190
    }),
    618: _tools.RODict({
        "ID": 618,
        "randomID": 5,
        "soulLevel": 13,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 6714
    }),
    619: _tools.RODict({
        "ID": 619,
        "randomID": 5,
        "soulLevel": 13,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 3730
    }),
    620: _tools.RODict({
        "ID": 620,
        "randomID": 5,
        "soulLevel": 13,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 2238
    }),
    621: _tools.RODict({
        "ID": 621,
        "randomID": 5,
        "soulLevel": 14,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 33700
    }),
    622: _tools.RODict({
        "ID": 622,
        "randomID": 5,
        "soulLevel": 14,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 20220
    }),
    623: _tools.RODict({
        "ID": 623,
        "randomID": 5,
        "soulLevel": 14,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 21600
    }),
    624: _tools.RODict({
        "ID": 624,
        "randomID": 5,
        "soulLevel": 14,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 12960
    }),
    625: _tools.RODict({
        "ID": 625,
        "randomID": 5,
        "soulLevel": 14,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 7200
    }),
    626: _tools.RODict({
        "ID": 626,
        "randomID": 5,
        "soulLevel": 14,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 4320
    }),
    627: _tools.RODict({
        "ID": 627,
        "randomID": 5,
        "soulLevel": 15,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 23700
    }),
    628: _tools.RODict({
        "ID": 628,
        "randomID": 5,
        "soulLevel": 15,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 14220
    }),
    629: _tools.RODict({
        "ID": 629,
        "randomID": 5,
        "soulLevel": 15,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 29100
    }),
    630: _tools.RODict({
        "ID": 630,
        "randomID": 5,
        "soulLevel": 15,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 17460
    }),
    631: _tools.RODict({
        "ID": 631,
        "randomID": 5,
        "soulLevel": 15,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 9700
    }),
    632: _tools.RODict({
        "ID": 632,
        "randomID": 5,
        "soulLevel": 15,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 5820
    }),
    633: _tools.RODict({
        "ID": 633,
        "randomID": 5,
        "soulLevel": 16,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 13700
    }),
    634: _tools.RODict({
        "ID": 634,
        "randomID": 5,
        "soulLevel": 16,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 8220
    }),
    635: _tools.RODict({
        "ID": 635,
        "randomID": 5,
        "soulLevel": 16,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 36600
    }),
    636: _tools.RODict({
        "ID": 636,
        "randomID": 5,
        "soulLevel": 16,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 21960
    }),
    637: _tools.RODict({
        "ID": 637,
        "randomID": 5,
        "soulLevel": 16,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 12200
    }),
    638: _tools.RODict({
        "ID": 638,
        "randomID": 5,
        "soulLevel": 16,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 7320
    }),
    639: _tools.RODict({
        "ID": 639,
        "randomID": 5,
        "soulLevel": 17,
        "randomQuality": 2,
        "randomQuality2": 0,
        "randomProp": 3700
    }),
    640: _tools.RODict({
        "ID": 640,
        "randomID": 5,
        "soulLevel": 17,
        "randomQuality": 2,
        "randomQuality2": 2,
        "randomProp": 2220
    }),
    641: _tools.RODict({
        "ID": 641,
        "randomID": 5,
        "soulLevel": 17,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 44100
    }),
    642: _tools.RODict({
        "ID": 642,
        "randomID": 5,
        "soulLevel": 17,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 26460
    }),
    643: _tools.RODict({
        "ID": 643,
        "randomID": 5,
        "soulLevel": 17,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 14700
    }),
    644: _tools.RODict({
        "ID": 644,
        "randomID": 5,
        "soulLevel": 17,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 8820
    }),
    645: _tools.RODict({
        "ID": 645,
        "randomID": 5,
        "soulLevel": 18,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 45300
    }),
    646: _tools.RODict({
        "ID": 646,
        "randomID": 5,
        "soulLevel": 18,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 27180
    }),
    647: _tools.RODict({
        "ID": 647,
        "randomID": 5,
        "soulLevel": 18,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 17200
    }),
    648: _tools.RODict({
        "ID": 648,
        "randomID": 5,
        "soulLevel": 18,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 10320
    }),
    649: _tools.RODict({
        "ID": 649,
        "randomID": 5,
        "soulLevel": 19,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 4500
    }),
    650: _tools.RODict({
        "ID": 650,
        "randomID": 5,
        "soulLevel": 19,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 2700
    }),
    651: _tools.RODict({
        "ID": 651,
        "randomID": 5,
        "soulLevel": 19,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 58000
    }),
    652: _tools.RODict({
        "ID": 652,
        "randomID": 5,
        "soulLevel": 19,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 34800
    }),
    653: _tools.RODict({
        "ID": 653,
        "randomID": 5,
        "soulLevel": 20,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 4500
    }),
    654: _tools.RODict({
        "ID": 654,
        "randomID": 5,
        "soulLevel": 20,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 2700
    }),
    655: _tools.RODict({
        "ID": 655,
        "randomID": 5,
        "soulLevel": 20,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 58000
    }),
    656: _tools.RODict({
        "ID": 656,
        "randomID": 5,
        "soulLevel": 20,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 34800
    }),
    657: _tools.RODict({
        "ID": 657,
        "randomID": 5,
        "soulLevel": 21,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 4500
    }),
    658: _tools.RODict({
        "ID": 658,
        "randomID": 5,
        "soulLevel": 21,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 2700
    }),
    659: _tools.RODict({
        "ID": 659,
        "randomID": 5,
        "soulLevel": 21,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 58000
    }),
    660: _tools.RODict({
        "ID": 660,
        "randomID": 5,
        "soulLevel": 21,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 34800
    }),
    661: _tools.RODict({
        "ID": 661,
        "randomID": 5,
        "soulLevel": 22,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 4500
    }),
    662: _tools.RODict({
        "ID": 662,
        "randomID": 5,
        "soulLevel": 22,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 2700
    }),
    663: _tools.RODict({
        "ID": 663,
        "randomID": 5,
        "soulLevel": 22,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 58000
    }),
    664: _tools.RODict({
        "ID": 664,
        "randomID": 5,
        "soulLevel": 22,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 34800
    }),
    665: _tools.RODict({
        "ID": 665,
        "randomID": 5,
        "soulLevel": 23,
        "randomQuality": 3,
        "randomQuality2": 0,
        "randomProp": 4500
    }),
    666: _tools.RODict({
        "ID": 666,
        "randomID": 5,
        "soulLevel": 23,
        "randomQuality": 3,
        "randomQuality2": 3,
        "randomProp": 2700
    }),
    667: _tools.RODict({
        "ID": 667,
        "randomID": 5,
        "soulLevel": 23,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 58000
    }),
    668: _tools.RODict({
        "ID": 668,
        "randomID": 5,
        "soulLevel": 23,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 34800
    }),
    669: _tools.RODict({
        "ID": 669,
        "randomID": 5,
        "soulLevel": 24,
        "randomQuality": 4,
        "randomQuality2": 0,
        "randomProp": 62500
    }),
    670: _tools.RODict({
        "ID": 670,
        "randomID": 5,
        "soulLevel": 24,
        "randomQuality": 4,
        "randomQuality2": 4,
        "randomProp": 37500
    })
})
minKey = 1
maxKey = 670