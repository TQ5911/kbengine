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
        "randomNum": 78004007,
        "randomWeight": 240
    }),
    2: _tools.RODict({
        "ID": 2,
        "randomID": 1001,
        "randomNum": 78004008,
        "randomWeight": 360
    }),
    3: _tools.RODict({
        "ID": 3,
        "randomID": 1001,
        "randomNum": 78004009,
        "randomWeight": 240
    }),
    4: _tools.RODict({
        "ID": 4,
        "randomID": 1001,
        "randomNum": 78004010,
        "randomWeight": 360
    }),
    5: _tools.RODict({
        "ID": 5,
        "randomID": 1001,
        "randomNum": 78004011,
        "randomWeight": 200
    }),
    6: _tools.RODict({
        "ID": 6,
        "randomID": 1001,
        "randomNum": 78004012,
        "randomWeight": 200
    }),
    7: _tools.RODict({
        "ID": 7,
        "randomID": 1002,
        "randomNum": 78004033,
        "randomWeight": 240
    }),
    8: _tools.RODict({
        "ID": 8,
        "randomID": 1002,
        "randomNum": 78004034,
        "randomWeight": 360
    }),
    9: _tools.RODict({
        "ID": 9,
        "randomID": 1002,
        "randomNum": 78004035,
        "randomWeight": 240
    }),
    10: _tools.RODict({
        "ID": 10,
        "randomID": 1002,
        "randomNum": 78004036,
        "randomWeight": 360
    }),
    11: _tools.RODict({
        "ID": 11,
        "randomID": 1002,
        "randomNum": 78004037,
        "randomWeight": 400
    }),
    12: _tools.RODict({
        "ID": 12,
        "randomID": 1003,
        "randomNum": 78004028,
        "randomWeight": 240
    }),
    13: _tools.RODict({
        "ID": 13,
        "randomID": 1003,
        "randomNum": 78004029,
        "randomWeight": 360
    }),
    14: _tools.RODict({
        "ID": 14,
        "randomID": 1003,
        "randomNum": 78004030,
        "randomWeight": 240
    }),
    15: _tools.RODict({
        "ID": 15,
        "randomID": 1003,
        "randomNum": 78004031,
        "randomWeight": 360
    }),
    16: _tools.RODict({
        "ID": 16,
        "randomID": 1003,
        "randomNum": 78004032,
        "randomWeight": 400
    }),
    17: _tools.RODict({
        "ID": 17,
        "randomID": 1004,
        "randomNum": 78004039,
        "randomWeight": 240
    }),
    18: _tools.RODict({
        "ID": 18,
        "randomID": 1004,
        "randomNum": 78004040,
        "randomWeight": 360
    }),
    19: _tools.RODict({
        "ID": 19,
        "randomID": 1004,
        "randomNum": 78004041,
        "randomWeight": 240
    }),
    20: _tools.RODict({
        "ID": 20,
        "randomID": 1004,
        "randomNum": 78004042,
        "randomWeight": 360
    }),
    21: _tools.RODict({
        "ID": 21,
        "randomID": 1004,
        "randomNum": 78004043,
        "randomWeight": 400
    }),
    22: _tools.RODict({
        "ID": 22,
        "randomID": 1005,
        "randomNum": 78004001,
        "randomWeight": 120
    }),
    23: _tools.RODict({
        "ID": 23,
        "randomID": 1005,
        "randomNum": 78004002,
        "randomWeight": 180
    }),
    24: _tools.RODict({
        "ID": 24,
        "randomID": 1005,
        "randomNum": 78004003,
        "randomWeight": 120
    }),
    25: _tools.RODict({
        "ID": 25,
        "randomID": 1005,
        "randomNum": 78004004,
        "randomWeight": 180
    }),
    26: _tools.RODict({
        "ID": 26,
        "randomID": 1005,
        "randomNum": 78004005,
        "randomWeight": 200
    }),
    27: _tools.RODict({
        "ID": 27,
        "randomID": 1005,
        "randomNum": 78004006,
        "randomWeight": 200
    }),
    28: _tools.RODict({
        "ID": 28,
        "randomID": 1006,
        "randomNum": 78004013,
        "randomWeight": 120
    }),
    29: _tools.RODict({
        "ID": 29,
        "randomID": 1006,
        "randomNum": 78004014,
        "randomWeight": 180
    }),
    30: _tools.RODict({
        "ID": 30,
        "randomID": 1006,
        "randomNum": 78004015,
        "randomWeight": 120
    }),
    31: _tools.RODict({
        "ID": 31,
        "randomID": 1006,
        "randomNum": 78004016,
        "randomWeight": 180
    }),
    32: _tools.RODict({
        "ID": 32,
        "randomID": 1006,
        "randomNum": 78004017,
        "randomWeight": 400
    }),
    33: _tools.RODict({
        "ID": 33,
        "randomID": 1007,
        "randomNum": 78004023,
        "randomWeight": 120
    }),
    34: _tools.RODict({
        "ID": 34,
        "randomID": 1007,
        "randomNum": 78004024,
        "randomWeight": 180
    }),
    35: _tools.RODict({
        "ID": 35,
        "randomID": 1007,
        "randomNum": 78004025,
        "randomWeight": 120
    }),
    36: _tools.RODict({
        "ID": 36,
        "randomID": 1007,
        "randomNum": 78004026,
        "randomWeight": 180
    }),
    37: _tools.RODict({
        "ID": 37,
        "randomID": 1007,
        "randomNum": 78004027,
        "randomWeight": 400
    }),
    38: _tools.RODict({
        "ID": 38,
        "randomID": 1008,
        "randomNum": 78004018,
        "randomWeight": 120
    }),
    39: _tools.RODict({
        "ID": 39,
        "randomID": 1008,
        "randomNum": 78004019,
        "randomWeight": 180
    }),
    40: _tools.RODict({
        "ID": 40,
        "randomID": 1008,
        "randomNum": 78004020,
        "randomWeight": 120
    }),
    41: _tools.RODict({
        "ID": 41,
        "randomID": 1008,
        "randomNum": 78004021,
        "randomWeight": 180
    }),
    42: _tools.RODict({
        "ID": 42,
        "randomID": 1008,
        "randomNum": 78004022,
        "randomWeight": 400
    }),
    43: _tools.RODict({
        "ID": 43,
        "randomID": 1009,
        "randomNum": 78004033,
        "randomWeight": 240
    }),
    44: _tools.RODict({
        "ID": 44,
        "randomID": 1009,
        "randomNum": 78004034,
        "randomWeight": 360
    }),
    45: _tools.RODict({
        "ID": 45,
        "randomID": 1009,
        "randomNum": 78004035,
        "randomWeight": 240
    }),
    46: _tools.RODict({
        "ID": 46,
        "randomID": 1009,
        "randomNum": 78004036,
        "randomWeight": 360
    }),
    47: _tools.RODict({
        "ID": 47,
        "randomID": 1009,
        "randomNum": 78004037,
        "randomWeight": 400
    }),
    48: _tools.RODict({
        "ID": 48,
        "randomID": 1009,
        "randomNum": 78004038,
        "randomWeight": 1000
    }),
    49: _tools.RODict({
        "ID": 49,
        "randomID": 1010,
        "randomNum": 78004000,
        "randomWeight": 1000
    })
})
minKey = 1
maxKey = 49
randomID2affixID = {1001: [78004007, 78004008, 78004009, 78004010, 78004011, 78004012], 1002: [78004033, 78004034, 78004035, 78004036, 78004037], 1003: [78004028, 78004029, 78004030, 78004031, 78004032], 1004: [78004039, 78004040, 78004041, 78004042, 78004043], 1005: [78004001, 78004002, 78004003, 78004004, 78004005, 78004006], 1006: [78004013, 78004014, 78004015, 78004016, 78004017], 1007: [78004023, 78004024, 78004025, 78004026, 78004027], 1008: [78004018, 78004019, 78004020, 78004021, 78004022], 1009: [78004033, 78004034, 78004035, 78004036, 78004037, 78004038], 1010: [78004000]}

randomID2weight = {1001: [240, 360, 240, 360, 200, 200], 1002: [240, 360, 240, 360, 400], 1003: [240, 360, 240, 360, 400], 1004: [240, 360, 240, 360, 400], 1005: [120, 180, 120, 180, 200, 200], 1006: [120, 180, 120, 180, 400], 1007: [120, 180, 120, 180, 400], 1008: [120, 180, 120, 180, 400], 1009: [240, 360, 240, 360, 400, 1000], 1010: [1000]}
