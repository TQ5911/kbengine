# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: affix/affixCountWeight
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
        "gid": 2,
        "group": _tools.ROList([1]),
        "groupWeight": 4515000.0
    }),
    2: _tools.RODict({
        "ID": 2,
        "gid": 2,
        "group": _tools.ROList([2]),
        "groupWeight": 2100000.0
    }),
    3: _tools.RODict({
        "ID": 3,
        "gid": 2,
        "group": _tools.ROList([3]),
        "groupWeight": 350000.0
    }),
    4: _tools.RODict({
        "ID": 4,
        "gid": 2,
        "group": _tools.ROList([4]),
        "groupWeight": 35000.0
    }),
    5: _tools.RODict({
        "ID": 5,
        "gid": 2,
        "group": _tools.ROList([1, 1]),
        "groupWeight": 1248075.0
    }),
    6: _tools.RODict({
        "ID": 6,
        "gid": 2,
        "group": _tools.ROList([2, 1]),
        "groupWeight": 1161000.0
    }),
    7: _tools.RODict({
        "ID": 7,
        "gid": 2,
        "group": _tools.ROList([3, 1]),
        "groupWeight": 193500.0
    }),
    8: _tools.RODict({
        "ID": 8,
        "gid": 2,
        "group": _tools.ROList([2, 1]),
        "groupWeight": 19350.0
    }),
    9: _tools.RODict({
        "ID": 9,
        "gid": 2,
        "group": _tools.ROList([2, 2]),
        "groupWeight": 270000.0
    }),
    10: _tools.RODict({
        "ID": 10,
        "gid": 2,
        "group": _tools.ROList([3, 2]),
        "groupWeight": 90000.0
    }),
    11: _tools.RODict({
        "ID": 11,
        "gid": 2,
        "group": _tools.ROList([4, 2]),
        "groupWeight": 9000.0
    }),
    12: _tools.RODict({
        "ID": 12,
        "gid": 2,
        "group": _tools.ROList([3, 3]),
        "groupWeight": 7500.0
    }),
    13: _tools.RODict({
        "ID": 13,
        "gid": 2,
        "group": _tools.ROList([4, 3]),
        "groupWeight": 1500.0
    }),
    14: _tools.RODict({
        "ID": 14,
        "gid": 2,
        "group": _tools.ROList([4, 4]),
        "groupWeight": 75.0
    }),
    15: _tools.RODict({
        "ID": 15,
        "gid": 3,
        "group": _tools.ROList([1]),
        "groupWeight": 403125000.0
    }),
    16: _tools.RODict({
        "ID": 16,
        "gid": 3,
        "group": _tools.ROList([2]),
        "groupWeight": 187500000.0
    }),
    17: _tools.RODict({
        "ID": 17,
        "gid": 3,
        "group": _tools.ROList([3]),
        "groupWeight": 31250000.0
    }),
    18: _tools.RODict({
        "ID": 18,
        "gid": 3,
        "group": _tools.ROList([4]),
        "groupWeight": 3125000.0
    }),
    19: _tools.RODict({
        "ID": 19,
        "gid": 3,
        "group": _tools.ROList([1, 1]),
        "groupWeight": 124807500.0
    }),
    20: _tools.RODict({
        "ID": 20,
        "gid": 3,
        "group": _tools.ROList([2, 1]),
        "groupWeight": 116100000.0
    }),
    21: _tools.RODict({
        "ID": 21,
        "gid": 3,
        "group": _tools.ROList([3, 1]),
        "groupWeight": 19350000.0
    }),
    22: _tools.RODict({
        "ID": 22,
        "gid": 3,
        "group": _tools.ROList([2, 1]),
        "groupWeight": 1935000.0
    }),
    23: _tools.RODict({
        "ID": 23,
        "gid": 3,
        "group": _tools.ROList([2, 2]),
        "groupWeight": 27000000.0
    }),
    24: _tools.RODict({
        "ID": 24,
        "gid": 3,
        "group": _tools.ROList([3, 2]),
        "groupWeight": 9000000.0
    }),
    25: _tools.RODict({
        "ID": 25,
        "gid": 3,
        "group": _tools.ROList([4, 2]),
        "groupWeight": 900000.0
    }),
    26: _tools.RODict({
        "ID": 26,
        "gid": 3,
        "group": _tools.ROList([3, 3]),
        "groupWeight": 750000.0
    }),
    27: _tools.RODict({
        "ID": 27,
        "gid": 3,
        "group": _tools.ROList([4, 3]),
        "groupWeight": 150000.0
    }),
    28: _tools.RODict({
        "ID": 28,
        "gid": 3,
        "group": _tools.ROList([4, 4]),
        "groupWeight": 7500.0
    }),
    29: _tools.RODict({
        "ID": 29,
        "gid": 3,
        "group": _tools.ROList([1, 1, 1]),
        "groupWeight": 20125209.0
    }),
    30: _tools.RODict({
        "ID": 30,
        "gid": 3,
        "group": _tools.ROList([2, 1, 1]),
        "groupWeight": 28081688.0
    }),
    31: _tools.RODict({
        "ID": 31,
        "gid": 3,
        "group": _tools.ROList([3, 1, 1]),
        "groupWeight": 4680281.0
    }),
    32: _tools.RODict({
        "ID": 32,
        "gid": 3,
        "group": _tools.ROList([4, 1, 1]),
        "groupWeight": 468028.0
    }),
    33: _tools.RODict({
        "ID": 33,
        "gid": 3,
        "group": _tools.ROList([2, 2, 1]),
        "groupWeight": 13061250.0
    }),
    34: _tools.RODict({
        "ID": 34,
        "gid": 3,
        "group": _tools.ROList([3, 2, 1]),
        "groupWeight": 4353750.0
    }),
    35: _tools.RODict({
        "ID": 35,
        "gid": 3,
        "group": _tools.ROList([4, 2, 1]),
        "groupWeight": 435375.0
    }),
    36: _tools.RODict({
        "ID": 36,
        "gid": 3,
        "group": _tools.ROList([3, 3, 1]),
        "groupWeight": 362813.0
    }),
    37: _tools.RODict({
        "ID": 37,
        "gid": 3,
        "group": _tools.ROList([4, 3, 1]),
        "groupWeight": 72563.0
    }),
    38: _tools.RODict({
        "ID": 38,
        "gid": 3,
        "group": _tools.ROList([4, 4, 1]),
        "groupWeight": 3628.0
    }),
    39: _tools.RODict({
        "ID": 39,
        "gid": 3,
        "group": _tools.ROList([2, 2, 2]),
        "groupWeight": 2025000.0
    }),
    40: _tools.RODict({
        "ID": 40,
        "gid": 3,
        "group": _tools.ROList([3, 2, 2]),
        "groupWeight": 1012500.0
    }),
    41: _tools.RODict({
        "ID": 41,
        "gid": 3,
        "group": _tools.ROList([4, 2, 2]),
        "groupWeight": 101250.0
    }),
    42: _tools.RODict({
        "ID": 42,
        "gid": 3,
        "group": _tools.ROList([3, 3, 2]),
        "groupWeight": 168750.0
    }),
    43: _tools.RODict({
        "ID": 43,
        "gid": 3,
        "group": _tools.ROList([4, 3, 2]),
        "groupWeight": 33750.0
    }),
    44: _tools.RODict({
        "ID": 44,
        "gid": 3,
        "group": _tools.ROList([4, 4, 2]),
        "groupWeight": 1688.0
    }),
    45: _tools.RODict({
        "ID": 45,
        "gid": 3,
        "group": _tools.ROList([3, 3, 3]),
        "groupWeight": 9375.0
    }),
    46: _tools.RODict({
        "ID": 46,
        "gid": 3,
        "group": _tools.ROList([4, 3, 3]),
        "groupWeight": 2813.0
    }),
    47: _tools.RODict({
        "ID": 47,
        "gid": 3,
        "group": _tools.ROList([4, 4, 3]),
        "groupWeight": 281.0
    }),
    48: _tools.RODict({
        "ID": 48,
        "gid": 3,
        "group": _tools.ROList([4, 4, 4]),
        "groupWeight": 9.0
    }),
    49: _tools.RODict({
        "ID": 49,
        "gid": 4,
        "group": _tools.ROList([1]),
        "groupWeight": 338625000.0
    }),
    50: _tools.RODict({
        "ID": 50,
        "gid": 4,
        "group": _tools.ROList([2]),
        "groupWeight": 157500000.0
    }),
    51: _tools.RODict({
        "ID": 51,
        "gid": 4,
        "group": _tools.ROList([3]),
        "groupWeight": 26250000.0
    }),
    52: _tools.RODict({
        "ID": 52,
        "gid": 4,
        "group": _tools.ROList([4]),
        "groupWeight": 2625000.0
    }),
    53: _tools.RODict({
        "ID": 53,
        "gid": 4,
        "group": _tools.ROList([1, 1]),
        "groupWeight": 145608750.0
    }),
    54: _tools.RODict({
        "ID": 54,
        "gid": 4,
        "group": _tools.ROList([2, 1]),
        "groupWeight": 135450000.0
    }),
    55: _tools.RODict({
        "ID": 55,
        "gid": 4,
        "group": _tools.ROList([3, 1]),
        "groupWeight": 22575000.0
    }),
    56: _tools.RODict({
        "ID": 56,
        "gid": 4,
        "group": _tools.ROList([2, 1]),
        "groupWeight": 2257500.0
    }),
    57: _tools.RODict({
        "ID": 57,
        "gid": 4,
        "group": _tools.ROList([2, 2]),
        "groupWeight": 31500000.0
    }),
    58: _tools.RODict({
        "ID": 58,
        "gid": 4,
        "group": _tools.ROList([3, 2]),
        "groupWeight": 10500000.0
    }),
    59: _tools.RODict({
        "ID": 59,
        "gid": 4,
        "group": _tools.ROList([4, 2]),
        "groupWeight": 1050000.0
    }),
    60: _tools.RODict({
        "ID": 60,
        "gid": 4,
        "group": _tools.ROList([3, 3]),
        "groupWeight": 875000.0
    }),
    61: _tools.RODict({
        "ID": 61,
        "gid": 4,
        "group": _tools.ROList([4, 3]),
        "groupWeight": 175000.0
    }),
    62: _tools.RODict({
        "ID": 62,
        "gid": 4,
        "group": _tools.ROList([4, 4]),
        "groupWeight": 8750.0
    }),
    63: _tools.RODict({
        "ID": 63,
        "gid": 4,
        "group": _tools.ROList([1, 1, 1]),
        "groupWeight": 33542016.0
    }),
    64: _tools.RODict({
        "ID": 64,
        "gid": 4,
        "group": _tools.ROList([2, 1, 1]),
        "groupWeight": 46802813.0
    }),
    65: _tools.RODict({
        "ID": 65,
        "gid": 4,
        "group": _tools.ROList([3, 1, 1]),
        "groupWeight": 7800469.0
    }),
    66: _tools.RODict({
        "ID": 66,
        "gid": 4,
        "group": _tools.ROList([4, 1, 1]),
        "groupWeight": 780047.0
    }),
    67: _tools.RODict({
        "ID": 67,
        "gid": 4,
        "group": _tools.ROList([2, 2, 1]),
        "groupWeight": 21768750.0
    }),
    68: _tools.RODict({
        "ID": 68,
        "gid": 4,
        "group": _tools.ROList([3, 2, 1]),
        "groupWeight": 7256250.0
    }),
    69: _tools.RODict({
        "ID": 69,
        "gid": 4,
        "group": _tools.ROList([4, 2, 1]),
        "groupWeight": 725625.0
    }),
    70: _tools.RODict({
        "ID": 70,
        "gid": 4,
        "group": _tools.ROList([3, 3, 1]),
        "groupWeight": 604688.0
    }),
    71: _tools.RODict({
        "ID": 71,
        "gid": 4,
        "group": _tools.ROList([4, 3, 1]),
        "groupWeight": 120938.0
    }),
    72: _tools.RODict({
        "ID": 72,
        "gid": 4,
        "group": _tools.ROList([4, 4, 1]),
        "groupWeight": 6047.0
    }),
    73: _tools.RODict({
        "ID": 73,
        "gid": 4,
        "group": _tools.ROList([2, 2, 2]),
        "groupWeight": 3375000.0
    }),
    74: _tools.RODict({
        "ID": 74,
        "gid": 4,
        "group": _tools.ROList([3, 2, 2]),
        "groupWeight": 1687500.0
    }),
    75: _tools.RODict({
        "ID": 75,
        "gid": 4,
        "group": _tools.ROList([4, 2, 2]),
        "groupWeight": 168750.0
    }),
    76: _tools.RODict({
        "ID": 76,
        "gid": 4,
        "group": _tools.ROList([3, 3, 2]),
        "groupWeight": 281250.0
    }),
    77: _tools.RODict({
        "ID": 77,
        "gid": 4,
        "group": _tools.ROList([4, 3, 2]),
        "groupWeight": 56250.0
    }),
    78: _tools.RODict({
        "ID": 78,
        "gid": 4,
        "group": _tools.ROList([4, 4, 2]),
        "groupWeight": 2813.0
    }),
    79: _tools.RODict({
        "ID": 79,
        "gid": 4,
        "group": _tools.ROList([3, 3, 3]),
        "groupWeight": 15625.0
    }),
    80: _tools.RODict({
        "ID": 80,
        "gid": 4,
        "group": _tools.ROList([4, 3, 3]),
        "groupWeight": 4688.0
    }),
    81: _tools.RODict({
        "ID": 81,
        "gid": 4,
        "group": _tools.ROList([4, 4, 3]),
        "groupWeight": 469.0
    }),
    82: _tools.RODict({
        "ID": 82,
        "gid": 4,
        "group": _tools.ROList([4, 4, 4]),
        "groupWeight": 16.0
    })
})
minKey = 1
maxKey = 82

affixWeightDic = _tools.RODict({ 
        2:[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], [4515000.0, 2100000.0, 350000.0, 35000.0, 1248075.0, 1161000.0, 193500.0, 19350.0, 270000.0, 90000.0, 9000.0, 7500.0, 1500.0, 75.0]],
        3:[[15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48], [403125000.0, 187500000.0, 31250000.0, 3125000.0, 124807500.0, 116100000.0, 19350000.0, 1935000.0, 27000000.0, 9000000.0, 900000.0, 750000.0, 150000.0, 7500.0, 20125209.0, 28081688.0, 4680281.0, 468028.0, 13061250.0, 4353750.0, 435375.0, 362813.0, 72563.0, 3628.0, 2025000.0, 1012500.0, 101250.0, 168750.0, 33750.0, 1688.0, 9375.0, 2813.0, 281.0, 9.0]],
        4:[[49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82], [338625000.0, 157500000.0, 26250000.0, 2625000.0, 145608750.0, 135450000.0, 22575000.0, 2257500.0, 31500000.0, 10500000.0, 1050000.0, 875000.0, 175000.0, 8750.0, 33542016.0, 46802813.0, 7800469.0, 780047.0, 21768750.0, 7256250.0, 725625.0, 604688.0, 120938.0, 6047.0, 3375000.0, 1687500.0, 168750.0, 281250.0, 56250.0, 2813.0, 15625.0, 4688.0, 469.0, 16.0]],
})
