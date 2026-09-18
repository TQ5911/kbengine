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
    }),
    101: _tools.RODict({
        "grid": 101,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    102: _tools.RODict({
        "grid": 102,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    103: _tools.RODict({
        "grid": 103,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    104: _tools.RODict({
        "grid": 104,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    105: _tools.RODict({
        "grid": 105,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    106: _tools.RODict({
        "grid": 106,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    107: _tools.RODict({
        "grid": 107,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    108: _tools.RODict({
        "grid": 108,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    109: _tools.RODict({
        "grid": 109,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    110: _tools.RODict({
        "grid": 110,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    111: _tools.RODict({
        "grid": 111,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    112: _tools.RODict({
        "grid": 112,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    113: _tools.RODict({
        "grid": 113,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    114: _tools.RODict({
        "grid": 114,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    115: _tools.RODict({
        "grid": 115,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    116: _tools.RODict({
        "grid": 116,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    117: _tools.RODict({
        "grid": 117,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    118: _tools.RODict({
        "grid": 118,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    119: _tools.RODict({
        "grid": 119,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    120: _tools.RODict({
        "grid": 120,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    121: _tools.RODict({
        "grid": 121,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    122: _tools.RODict({
        "grid": 122,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    123: _tools.RODict({
        "grid": 123,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    124: _tools.RODict({
        "grid": 124,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    125: _tools.RODict({
        "grid": 125,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    126: _tools.RODict({
        "grid": 126,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    127: _tools.RODict({
        "grid": 127,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    128: _tools.RODict({
        "grid": 128,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    129: _tools.RODict({
        "grid": 129,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    130: _tools.RODict({
        "grid": 130,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    131: _tools.RODict({
        "grid": 131,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    132: _tools.RODict({
        "grid": 132,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    133: _tools.RODict({
        "grid": 133,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    134: _tools.RODict({
        "grid": 134,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    135: _tools.RODict({
        "grid": 135,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    136: _tools.RODict({
        "grid": 136,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    137: _tools.RODict({
        "grid": 137,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    138: _tools.RODict({
        "grid": 138,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    139: _tools.RODict({
        "grid": 139,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    140: _tools.RODict({
        "grid": 140,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    141: _tools.RODict({
        "grid": 141,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    142: _tools.RODict({
        "grid": 142,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    143: _tools.RODict({
        "grid": 143,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    144: _tools.RODict({
        "grid": 144,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    145: _tools.RODict({
        "grid": 145,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    146: _tools.RODict({
        "grid": 146,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    147: _tools.RODict({
        "grid": 147,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    148: _tools.RODict({
        "grid": 148,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    149: _tools.RODict({
        "grid": 149,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    150: _tools.RODict({
        "grid": 150,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    151: _tools.RODict({
        "grid": 151,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    152: _tools.RODict({
        "grid": 152,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    153: _tools.RODict({
        "grid": 153,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    154: _tools.RODict({
        "grid": 154,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    155: _tools.RODict({
        "grid": 155,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    156: _tools.RODict({
        "grid": 156,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    157: _tools.RODict({
        "grid": 157,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    158: _tools.RODict({
        "grid": 158,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    159: _tools.RODict({
        "grid": 159,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    160: _tools.RODict({
        "grid": 160,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    161: _tools.RODict({
        "grid": 161,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    162: _tools.RODict({
        "grid": 162,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    163: _tools.RODict({
        "grid": 163,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    164: _tools.RODict({
        "grid": 164,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    165: _tools.RODict({
        "grid": 165,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    166: _tools.RODict({
        "grid": 166,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    167: _tools.RODict({
        "grid": 167,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    168: _tools.RODict({
        "grid": 168,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    169: _tools.RODict({
        "grid": 169,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    170: _tools.RODict({
        "grid": 170,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    171: _tools.RODict({
        "grid": 171,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    172: _tools.RODict({
        "grid": 172,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    173: _tools.RODict({
        "grid": 173,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    174: _tools.RODict({
        "grid": 174,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    175: _tools.RODict({
        "grid": 175,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    176: _tools.RODict({
        "grid": 176,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    177: _tools.RODict({
        "grid": 177,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    178: _tools.RODict({
        "grid": 178,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    179: _tools.RODict({
        "grid": 179,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    180: _tools.RODict({
        "grid": 180,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    181: _tools.RODict({
        "grid": 181,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    182: _tools.RODict({
        "grid": 182,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    183: _tools.RODict({
        "grid": 183,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    184: _tools.RODict({
        "grid": 184,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    185: _tools.RODict({
        "grid": 185,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    186: _tools.RODict({
        "grid": 186,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    187: _tools.RODict({
        "grid": 187,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    188: _tools.RODict({
        "grid": 188,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    189: _tools.RODict({
        "grid": 189,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    190: _tools.RODict({
        "grid": 190,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    191: _tools.RODict({
        "grid": 191,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    192: _tools.RODict({
        "grid": 192,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    193: _tools.RODict({
        "grid": 193,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    194: _tools.RODict({
        "grid": 194,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    195: _tools.RODict({
        "grid": 195,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    196: _tools.RODict({
        "grid": 196,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    197: _tools.RODict({
        "grid": 197,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    198: _tools.RODict({
        "grid": 198,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    199: _tools.RODict({
        "grid": 199,
        "itemNeeded": 30000001,
        "itemNum": 25
    }),
    200: _tools.RODict({
        "grid": 200,
        "itemNeeded": 30000001,
        "itemNum": 25
    })
})
minKey = 1
maxKey = 200