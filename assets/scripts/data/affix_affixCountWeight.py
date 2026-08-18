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
        "groupWeight": 764067.0
    }),
    2: _tools.RODict({
        "ID": 2,
        "gid": 2,
        "group": _tools.ROList([2]),
        "groupWeight": 100000.0
    }),
    3: _tools.RODict({
        "ID": 3,
        "gid": 2,
        "group": _tools.ROList([3]),
        "groupWeight": 10000.0
    }),
    4: _tools.RODict({
        "ID": 4,
        "gid": 2,
        "group": _tools.ROList([4]),
        "groupWeight": 2000.0
    }),
    5: _tools.RODict({
        "ID": 5,
        "gid": 2,
        "group": _tools.ROList([1, 1]),
        "groupWeight": 100000.0
    }),
    6: _tools.RODict({
        "ID": 6,
        "gid": 2,
        "group": _tools.ROList([2, 1]),
        "groupWeight": 10000.0
    }),
    7: _tools.RODict({
        "ID": 7,
        "gid": 2,
        "group": _tools.ROList([3, 1]),
        "groupWeight": 4167.0
    }),
    8: _tools.RODict({
        "ID": 8,
        "gid": 2,
        "group": _tools.ROList([4, 1]),
        "groupWeight": 1000.0
    }),
    9: _tools.RODict({
        "ID": 9,
        "gid": 2,
        "group": _tools.ROList([2, 2]),
        "groupWeight": 4167.0
    }),
    10: _tools.RODict({
        "ID": 10,
        "gid": 2,
        "group": _tools.ROList([3, 2]),
        "groupWeight": 2000.0
    }),
    11: _tools.RODict({
        "ID": 11,
        "gid": 2,
        "group": _tools.ROList([4, 2]),
        "groupWeight": 1000.0
    }),
    12: _tools.RODict({
        "ID": 12,
        "gid": 2,
        "group": _tools.ROList([3, 3]),
        "groupWeight": 1000.0
    }),
    13: _tools.RODict({
        "ID": 13,
        "gid": 2,
        "group": _tools.ROList([4, 3]),
        "groupWeight": 400.0
    }),
    14: _tools.RODict({
        "ID": 14,
        "gid": 2,
        "group": _tools.ROList([4, 4]),
        "groupWeight": 200.0
    }),
    15: _tools.RODict({
        "ID": 15,
        "gid": 3,
        "group": _tools.ROList([1]),
        "groupWeight": 629887.0
    }),
    16: _tools.RODict({
        "ID": 16,
        "gid": 3,
        "group": _tools.ROList([2]),
        "groupWeight": 151515.0
    }),
    17: _tools.RODict({
        "ID": 17,
        "gid": 3,
        "group": _tools.ROList([3]),
        "groupWeight": 11111.0
    }),
    18: _tools.RODict({
        "ID": 18,
        "gid": 3,
        "group": _tools.ROList([4]),
        "groupWeight": 1667.0
    }),
    19: _tools.RODict({
        "ID": 19,
        "gid": 3,
        "group": _tools.ROList([1, 1]),
        "groupWeight": 151515.0
    }),
    20: _tools.RODict({
        "ID": 20,
        "gid": 3,
        "group": _tools.ROList([2, 1]),
        "groupWeight": 11111.0
    }),
    21: _tools.RODict({
        "ID": 21,
        "gid": 3,
        "group": _tools.ROList([3, 1]),
        "groupWeight": 6667.0
    }),
    22: _tools.RODict({
        "ID": 22,
        "gid": 3,
        "group": _tools.ROList([4, 1]),
        "groupWeight": 833.0
    }),
    23: _tools.RODict({
        "ID": 23,
        "gid": 3,
        "group": _tools.ROList([2, 2]),
        "groupWeight": 6667.0
    }),
    24: _tools.RODict({
        "ID": 24,
        "gid": 3,
        "group": _tools.ROList([3, 2]),
        "groupWeight": 1667.0
    }),
    25: _tools.RODict({
        "ID": 25,
        "gid": 3,
        "group": _tools.ROList([4, 2]),
        "groupWeight": 417.0
    }),
    26: _tools.RODict({
        "ID": 26,
        "gid": 3,
        "group": _tools.ROList([3, 3]),
        "groupWeight": 833.0
    }),
    27: _tools.RODict({
        "ID": 27,
        "gid": 3,
        "group": _tools.ROList([4, 3]),
        "groupWeight": 278.0
    }),
    28: _tools.RODict({
        "ID": 28,
        "gid": 3,
        "group": _tools.ROList([4, 4]),
        "groupWeight": 143.0
    }),
    29: _tools.RODict({
        "ID": 29,
        "gid": 3,
        "group": _tools.ROList([1, 1, 1]),
        "groupWeight": 11111.0
    }),
    30: _tools.RODict({
        "ID": 30,
        "gid": 3,
        "group": _tools.ROList([2, 1, 1]),
        "groupWeight": 6667.0
    }),
    31: _tools.RODict({
        "ID": 31,
        "gid": 3,
        "group": _tools.ROList([3, 1, 1]),
        "groupWeight": 1667.0
    }),
    32: _tools.RODict({
        "ID": 32,
        "gid": 3,
        "group": _tools.ROList([4, 1, 1]),
        "groupWeight": 417.0
    }),
    33: _tools.RODict({
        "ID": 33,
        "gid": 3,
        "group": _tools.ROList([2, 2, 1]),
        "groupWeight": 1667.0
    }),
    34: _tools.RODict({
        "ID": 34,
        "gid": 3,
        "group": _tools.ROList([3, 2, 1]),
        "groupWeight": 833.0
    }),
    35: _tools.RODict({
        "ID": 35,
        "gid": 3,
        "group": _tools.ROList([4, 2, 1]),
        "groupWeight": 278.0
    }),
    36: _tools.RODict({
        "ID": 36,
        "gid": 3,
        "group": _tools.ROList([3, 3, 1]),
        "groupWeight": 417.0
    }),
    37: _tools.RODict({
        "ID": 37,
        "gid": 3,
        "group": _tools.ROList([4, 3, 1]),
        "groupWeight": 152.0
    }),
    38: _tools.RODict({
        "ID": 38,
        "gid": 3,
        "group": _tools.ROList([4, 4, 1]),
        "groupWeight": 100.0
    }),
    39: _tools.RODict({
        "ID": 39,
        "gid": 3,
        "group": _tools.ROList([2, 2, 2]),
        "groupWeight": 833.0
    }),
    40: _tools.RODict({
        "ID": 40,
        "gid": 3,
        "group": _tools.ROList([3, 2, 2]),
        "groupWeight": 417.0
    }),
    41: _tools.RODict({
        "ID": 41,
        "gid": 3,
        "group": _tools.ROList([4, 2, 2]),
        "groupWeight": 152.0
    }),
    42: _tools.RODict({
        "ID": 42,
        "gid": 3,
        "group": _tools.ROList([3, 3, 2]),
        "groupWeight": 278.0
    }),
    43: _tools.RODict({
        "ID": 43,
        "gid": 3,
        "group": _tools.ROList([4, 3, 2]),
        "groupWeight": 143.0
    }),
    44: _tools.RODict({
        "ID": 44,
        "gid": 3,
        "group": _tools.ROList([4, 4, 2]),
        "groupWeight": 143.0
    }),
    45: _tools.RODict({
        "ID": 45,
        "gid": 3,
        "group": _tools.ROList([3, 3, 3]),
        "groupWeight": 152.0
    }),
    46: _tools.RODict({
        "ID": 46,
        "gid": 3,
        "group": _tools.ROList([4, 3, 3]),
        "groupWeight": 100.0
    }),
    47: _tools.RODict({
        "ID": 47,
        "gid": 3,
        "group": _tools.ROList([4, 4, 3]),
        "groupWeight": 100.0
    }),
    48: _tools.RODict({
        "ID": 48,
        "gid": 3,
        "group": _tools.ROList([4, 4, 4]),
        "groupWeight": 0.0
    }),
    49: _tools.RODict({
        "ID": 49,
        "gid": 4,
        "group": _tools.ROList([1]),
        "groupWeight": 465834.0
    }),
    50: _tools.RODict({
        "ID": 50,
        "gid": 4,
        "group": _tools.ROList([2]),
        "groupWeight": 200000.0
    }),
    51: _tools.RODict({
        "ID": 51,
        "gid": 4,
        "group": _tools.ROList([3]),
        "groupWeight": 22222.0
    }),
    52: _tools.RODict({
        "ID": 52,
        "gid": 4,
        "group": _tools.ROList([4]),
        "groupWeight": 3333.0
    }),
    53: _tools.RODict({
        "ID": 53,
        "gid": 4,
        "group": _tools.ROList([1, 1]),
        "groupWeight": 200000.0
    }),
    54: _tools.RODict({
        "ID": 54,
        "gid": 4,
        "group": _tools.ROList([2, 1]),
        "groupWeight": 22222.0
    }),
    55: _tools.RODict({
        "ID": 55,
        "gid": 4,
        "group": _tools.ROList([3, 1]),
        "groupWeight": 13333.0
    }),
    56: _tools.RODict({
        "ID": 56,
        "gid": 4,
        "group": _tools.ROList([4, 1]),
        "groupWeight": 1667.0
    }),
    57: _tools.RODict({
        "ID": 57,
        "gid": 4,
        "group": _tools.ROList([2, 2]),
        "groupWeight": 13333.0
    }),
    58: _tools.RODict({
        "ID": 58,
        "gid": 4,
        "group": _tools.ROList([3, 2]),
        "groupWeight": 3333.0
    }),
    59: _tools.RODict({
        "ID": 59,
        "gid": 4,
        "group": _tools.ROList([4, 2]),
        "groupWeight": 833.0
    }),
    60: _tools.RODict({
        "ID": 60,
        "gid": 4,
        "group": _tools.ROList([3, 3]),
        "groupWeight": 1667.0
    }),
    61: _tools.RODict({
        "ID": 61,
        "gid": 4,
        "group": _tools.ROList([4, 3]),
        "groupWeight": 556.0
    }),
    62: _tools.RODict({
        "ID": 62,
        "gid": 4,
        "group": _tools.ROList([4, 4]),
        "groupWeight": 286.0
    }),
    63: _tools.RODict({
        "ID": 63,
        "gid": 4,
        "group": _tools.ROList([1, 1, 1]),
        "groupWeight": 22222.0
    }),
    64: _tools.RODict({
        "ID": 64,
        "gid": 4,
        "group": _tools.ROList([2, 1, 1]),
        "groupWeight": 13333.0
    }),
    65: _tools.RODict({
        "ID": 65,
        "gid": 4,
        "group": _tools.ROList([3, 1, 1]),
        "groupWeight": 3333.0
    }),
    66: _tools.RODict({
        "ID": 66,
        "gid": 4,
        "group": _tools.ROList([4, 1, 1]),
        "groupWeight": 833.0
    }),
    67: _tools.RODict({
        "ID": 67,
        "gid": 4,
        "group": _tools.ROList([2, 2, 1]),
        "groupWeight": 3333.0
    }),
    68: _tools.RODict({
        "ID": 68,
        "gid": 4,
        "group": _tools.ROList([3, 2, 1]),
        "groupWeight": 1667.0
    }),
    69: _tools.RODict({
        "ID": 69,
        "gid": 4,
        "group": _tools.ROList([4, 2, 1]),
        "groupWeight": 556.0
    }),
    70: _tools.RODict({
        "ID": 70,
        "gid": 4,
        "group": _tools.ROList([3, 3, 1]),
        "groupWeight": 833.0
    }),
    71: _tools.RODict({
        "ID": 71,
        "gid": 4,
        "group": _tools.ROList([4, 3, 1]),
        "groupWeight": 303.0
    }),
    72: _tools.RODict({
        "ID": 72,
        "gid": 4,
        "group": _tools.ROList([4, 4, 1]),
        "groupWeight": 200.0
    }),
    73: _tools.RODict({
        "ID": 73,
        "gid": 4,
        "group": _tools.ROList([2, 2, 2]),
        "groupWeight": 1667.0
    }),
    74: _tools.RODict({
        "ID": 74,
        "gid": 4,
        "group": _tools.ROList([3, 2, 2]),
        "groupWeight": 833.0
    }),
    75: _tools.RODict({
        "ID": 75,
        "gid": 4,
        "group": _tools.ROList([4, 2, 2]),
        "groupWeight": 303.0
    }),
    76: _tools.RODict({
        "ID": 76,
        "gid": 4,
        "group": _tools.ROList([3, 3, 2]),
        "groupWeight": 556.0
    }),
    77: _tools.RODict({
        "ID": 77,
        "gid": 4,
        "group": _tools.ROList([4, 3, 2]),
        "groupWeight": 286.0
    }),
    78: _tools.RODict({
        "ID": 78,
        "gid": 4,
        "group": _tools.ROList([4, 4, 2]),
        "groupWeight": 286.0
    }),
    79: _tools.RODict({
        "ID": 79,
        "gid": 4,
        "group": _tools.ROList([3, 3, 3]),
        "groupWeight": 303.0
    }),
    80: _tools.RODict({
        "ID": 80,
        "gid": 4,
        "group": _tools.ROList([4, 3, 3]),
        "groupWeight": 200.0
    }),
    81: _tools.RODict({
        "ID": 81,
        "gid": 4,
        "group": _tools.ROList([4, 4, 3]),
        "groupWeight": 200.0
    }),
    82: _tools.RODict({
        "ID": 82,
        "gid": 4,
        "group": _tools.ROList([4, 4, 4]),
        "groupWeight": 133.0
    })
})
minKey = 1
maxKey = 82

affixWeightDic = _tools.RODict({ 
        2:[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], [764067.0, 100000.0, 10000.0, 2000.0, 100000.0, 10000.0, 4167.0, 1000.0, 4167.0, 2000.0, 1000.0, 1000.0, 400.0, 200.0]],
        3:[[15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48], [629887.0, 151515.0, 11111.0, 1667.0, 151515.0, 11111.0, 6667.0, 833.0, 6667.0, 1667.0, 417.0, 833.0, 278.0, 143.0, 11111.0, 6667.0, 1667.0, 417.0, 1667.0, 833.0, 278.0, 417.0, 152.0, 100.0, 833.0, 417.0, 152.0, 278.0, 143.0, 143.0, 152.0, 100.0, 100.0, 0.0]],
        4:[[49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82], [465834.0, 200000.0, 22222.0, 3333.0, 200000.0, 22222.0, 13333.0, 1667.0, 13333.0, 3333.0, 833.0, 1667.0, 556.0, 286.0, 22222.0, 13333.0, 3333.0, 833.0, 3333.0, 1667.0, 556.0, 833.0, 303.0, 200.0, 1667.0, 833.0, 303.0, 556.0, 286.0, 286.0, 303.0, 200.0, 200.0, 133.0]],
})
