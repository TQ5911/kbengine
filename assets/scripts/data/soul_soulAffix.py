# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: soul/soulAffix
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
        "randomID": 1001,
        "randomNum": 78004009,
        "randomWeight": 600
    }),
    2: _tools.RODict({
        "ID": 2,
        "randomID": 1001,
        "randomNum": 78004010,
        "randomWeight": 400
    }),
    3: _tools.RODict({
        "ID": 3,
        "randomID": 1001,
        "randomNum": 78004011,
        "randomWeight": 600
    }),
    4: _tools.RODict({
        "ID": 4,
        "randomID": 1001,
        "randomNum": 78004012,
        "randomWeight": 400
    }),
    5: _tools.RODict({
        "ID": 5,
        "randomID": 1002,
        "randomNum": 78004046,
        "randomWeight": 600
    }),
    6: _tools.RODict({
        "ID": 6,
        "randomID": 1002,
        "randomNum": 78004047,
        "randomWeight": 400
    }),
    7: _tools.RODict({
        "ID": 7,
        "randomID": 1002,
        "randomNum": 78004048,
        "randomWeight": 600
    }),
    8: _tools.RODict({
        "ID": 8,
        "randomID": 1002,
        "randomNum": 78004049,
        "randomWeight": 400
    }),
    9: _tools.RODict({
        "ID": 9,
        "randomID": 1003,
        "randomNum": 78004040,
        "randomWeight": 600
    }),
    10: _tools.RODict({
        "ID": 10,
        "randomID": 1003,
        "randomNum": 78004041,
        "randomWeight": 400
    }),
    11: _tools.RODict({
        "ID": 11,
        "randomID": 1003,
        "randomNum": 78004042,
        "randomWeight": 600
    }),
    12: _tools.RODict({
        "ID": 12,
        "randomID": 1003,
        "randomNum": 78004043,
        "randomWeight": 400
    }),
    13: _tools.RODict({
        "ID": 13,
        "randomID": 1004,
        "randomNum": 78004055,
        "randomWeight": 600
    }),
    14: _tools.RODict({
        "ID": 14,
        "randomID": 1004,
        "randomNum": 78004056,
        "randomWeight": 400
    }),
    15: _tools.RODict({
        "ID": 15,
        "randomID": 1004,
        "randomNum": 78004057,
        "randomWeight": 600
    }),
    16: _tools.RODict({
        "ID": 16,
        "randomID": 1004,
        "randomNum": 78004058,
        "randomWeight": 400
    }),
    17: _tools.RODict({
        "ID": 17,
        "randomID": 1005,
        "randomNum": 78004001,
        "randomWeight": 240
    }),
    18: _tools.RODict({
        "ID": 18,
        "randomID": 1005,
        "randomNum": 78004002,
        "randomWeight": 160
    }),
    19: _tools.RODict({
        "ID": 19,
        "randomID": 1005,
        "randomNum": 78004003,
        "randomWeight": 240
    }),
    20: _tools.RODict({
        "ID": 20,
        "randomID": 1005,
        "randomNum": 78004004,
        "randomWeight": 160
    }),
    21: _tools.RODict({
        "ID": 21,
        "randomID": 1005,
        "randomNum": 78004005,
        "randomWeight": 120
    }),
    22: _tools.RODict({
        "ID": 22,
        "randomID": 1005,
        "randomNum": 78004006,
        "randomWeight": 80
    }),
    23: _tools.RODict({
        "ID": 23,
        "randomID": 1006,
        "randomNum": 78004016,
        "randomWeight": 240
    }),
    24: _tools.RODict({
        "ID": 24,
        "randomID": 1006,
        "randomNum": 78004017,
        "randomWeight": 160
    }),
    25: _tools.RODict({
        "ID": 25,
        "randomID": 1006,
        "randomNum": 78004018,
        "randomWeight": 240
    }),
    26: _tools.RODict({
        "ID": 26,
        "randomID": 1006,
        "randomNum": 78004019,
        "randomWeight": 160
    }),
    27: _tools.RODict({
        "ID": 27,
        "randomID": 1006,
        "randomNum": 78004020,
        "randomWeight": 120
    }),
    28: _tools.RODict({
        "ID": 28,
        "randomID": 1006,
        "randomNum": 78004021,
        "randomWeight": 80
    }),
    29: _tools.RODict({
        "ID": 29,
        "randomID": 1007,
        "randomNum": 78004032,
        "randomWeight": 240
    }),
    30: _tools.RODict({
        "ID": 30,
        "randomID": 1007,
        "randomNum": 78004033,
        "randomWeight": 160
    }),
    31: _tools.RODict({
        "ID": 31,
        "randomID": 1007,
        "randomNum": 78004034,
        "randomWeight": 240
    }),
    32: _tools.RODict({
        "ID": 32,
        "randomID": 1007,
        "randomNum": 78004035,
        "randomWeight": 160
    }),
    33: _tools.RODict({
        "ID": 33,
        "randomID": 1007,
        "randomNum": 78004036,
        "randomWeight": 120
    }),
    34: _tools.RODict({
        "ID": 34,
        "randomID": 1007,
        "randomNum": 78004037,
        "randomWeight": 80
    }),
    35: _tools.RODict({
        "ID": 35,
        "randomID": 1008,
        "randomNum": 78004024,
        "randomWeight": 240
    }),
    36: _tools.RODict({
        "ID": 36,
        "randomID": 1008,
        "randomNum": 78004025,
        "randomWeight": 160
    }),
    37: _tools.RODict({
        "ID": 37,
        "randomID": 1008,
        "randomNum": 78004026,
        "randomWeight": 240
    }),
    38: _tools.RODict({
        "ID": 38,
        "randomID": 1008,
        "randomNum": 78004027,
        "randomWeight": 160
    }),
    39: _tools.RODict({
        "ID": 39,
        "randomID": 1008,
        "randomNum": 78004028,
        "randomWeight": 120
    }),
    40: _tools.RODict({
        "ID": 40,
        "randomID": 1008,
        "randomNum": 78004029,
        "randomWeight": 80
    }),
    41: _tools.RODict({
        "ID": 41,
        "randomID": 2001,
        "randomNum": 78004007,
        "randomWeight": 100
    }),
    42: _tools.RODict({
        "ID": 42,
        "randomID": 3001,
        "randomNum": 78004008,
        "randomWeight": 100
    }),
    43: _tools.RODict({
        "ID": 43,
        "randomID": 2002,
        "randomNum": 78004013,
        "randomWeight": 100
    }),
    44: _tools.RODict({
        "ID": 44,
        "randomID": 3002,
        "randomNum": 78004014,
        "randomWeight": 100
    }),
    45: _tools.RODict({
        "ID": 45,
        "randomID": 3002,
        "randomNum": 78004015,
        "randomWeight": 100
    }),
    46: _tools.RODict({
        "ID": 46,
        "randomID": 2003,
        "randomNum": 78004022,
        "randomWeight": 100
    }),
    47: _tools.RODict({
        "ID": 47,
        "randomID": 3003,
        "randomNum": 78004023,
        "randomWeight": 100
    }),
    48: _tools.RODict({
        "ID": 48,
        "randomID": 2004,
        "randomNum": 78004030,
        "randomWeight": 100
    }),
    49: _tools.RODict({
        "ID": 49,
        "randomID": 3004,
        "randomNum": 78004031,
        "randomWeight": 100
    }),
    50: _tools.RODict({
        "ID": 50,
        "randomID": 2005,
        "randomNum": 78004038,
        "randomWeight": 100
    }),
    51: _tools.RODict({
        "ID": 51,
        "randomID": 3005,
        "randomNum": 78004039,
        "randomWeight": 100
    }),
    52: _tools.RODict({
        "ID": 52,
        "randomID": 2006,
        "randomNum": 78004044,
        "randomWeight": 100
    }),
    53: _tools.RODict({
        "ID": 53,
        "randomID": 3006,
        "randomNum": 78004045,
        "randomWeight": 100
    }),
    54: _tools.RODict({
        "ID": 54,
        "randomID": 2007,
        "randomNum": 78004050,
        "randomWeight": 100
    }),
    55: _tools.RODict({
        "ID": 55,
        "randomID": 3007,
        "randomNum": 78004051,
        "randomWeight": 100
    }),
    56: _tools.RODict({
        "ID": 56,
        "randomID": 3007,
        "randomNum": 78004052,
        "randomWeight": 100
    }),
    57: _tools.RODict({
        "ID": 57,
        "randomID": 2008,
        "randomNum": 78004059,
        "randomWeight": 100
    }),
    58: _tools.RODict({
        "ID": 58,
        "randomID": 3008,
        "randomNum": 78004060,
        "randomWeight": 100
    }),
    59: _tools.RODict({
        "ID": 59,
        "randomID": 3008,
        "randomNum": 78004061,
        "randomWeight": 100
    }),
    60: _tools.RODict({
        "ID": 60,
        "randomID": 1010,
        "randomNum": 78004000,
        "randomWeight": 100
    })
})
minKey = 1
maxKey = 60
randomID2affixID = {1001: [78004009, 78004010, 78004011, 78004012], 1002: [78004046, 78004047, 78004048, 78004049], 1003: [78004040, 78004041, 78004042, 78004043], 1004: [78004055, 78004056, 78004057, 78004058], 1005: [78004001, 78004002, 78004003, 78004004, 78004005, 78004006], 1006: [78004016, 78004017, 78004018, 78004019, 78004020, 78004021], 1007: [78004032, 78004033, 78004034, 78004035, 78004036, 78004037], 1008: [78004024, 78004025, 78004026, 78004027, 78004028, 78004029], 2001: [78004007], 3001: [78004008], 2002: [78004013], 3002: [78004014, 78004015], 2003: [78004022], 3003: [78004023], 2004: [78004030], 3004: [78004031], 2005: [78004038], 3005: [78004039], 2006: [78004044], 3006: [78004045], 2007: [78004050], 3007: [78004051, 78004052], 2008: [78004059], 3008: [78004060, 78004061], 1010: [78004000]}

randomID2weight = {1001: [600, 400, 600, 400], 1002: [600, 400, 600, 400], 1003: [600, 400, 600, 400], 1004: [600, 400, 600, 400], 1005: [240, 160, 240, 160, 120, 80], 1006: [240, 160, 240, 160, 120, 80], 1007: [240, 160, 240, 160, 120, 80], 1008: [240, 160, 240, 160, 120, 80], 2001: [100], 3001: [100], 2002: [100], 3002: [100, 100], 2003: [100], 3003: [100], 2004: [100], 3004: [100], 2005: [100], 3005: [100], 2006: [100], 3006: [100], 2007: [100], 3007: [100, 100], 2008: [100], 3008: [100, 100], 1010: [100]}
