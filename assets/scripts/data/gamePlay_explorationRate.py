# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: gamePlay/explorationRate
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
        "map": 1002,
        "targetType": 26,
        "targetParam": (11, 1002),
        "point": 10
    }),
    5: _tools.RODict({
        "ID": 5,
        "map": 1001,
        "targetType": 26,
        "targetParam": (11, 1001),
        "point": 10
    }),
    9: _tools.RODict({
        "ID": 9,
        "map": 1030,
        "targetType": 26,
        "targetParam": (7, 1030),
        "point": 10
    }),
    13: _tools.RODict({
        "ID": 13,
        "map": 1031,
        "targetType": 26,
        "targetParam": (7, 1031),
        "point": 10
    }),
    14: _tools.RODict({
        "ID": 14,
        "map": 1032,
        "targetType": 26,
        "targetParam": (7, 1032),
        "point": 10
    }),
    15: _tools.RODict({
        "ID": 15,
        "map": 1035,
        "targetType": 26,
        "targetParam": (7, 1035),
        "point": 10
    }),
    16: _tools.RODict({
        "ID": 16,
        "map": 1036,
        "targetType": 26,
        "targetParam": (7, 1036),
        "point": 10
    }),
    3: _tools.RODict({
        "ID": 3,
        "map": 1002,
        "targetType": 22,
        "targetParam": (10, 1002),
        "point": 10
    }),
    11: _tools.RODict({
        "ID": 11,
        "map": 1030,
        "targetType": 22,
        "targetParam": (10, 1030),
        "point": 10
    }),
    17: _tools.RODict({
        "ID": 17,
        "map": 1031,
        "targetType": 22,
        "targetParam": (10, 1031),
        "point": 10
    }),
    18: _tools.RODict({
        "ID": 18,
        "map": 1032,
        "targetType": 22,
        "targetParam": (10, 1032),
        "point": 10
    }),
    19: _tools.RODict({
        "ID": 19,
        "map": 1035,
        "targetType": 22,
        "targetParam": (10, 1035),
        "point": 10
    }),
    20: _tools.RODict({
        "ID": 20,
        "map": 1036,
        "targetType": 22,
        "targetParam": (10, 1036),
        "point": 10
    }),
    4: _tools.RODict({
        "ID": 4,
        "map": 1002,
        "targetType": 48,
        "targetParam": (10, 1002),
        "point": 10
    }),
    8: _tools.RODict({
        "ID": 8,
        "map": 1001,
        "targetType": 48,
        "targetParam": (10, 1001),
        "point": 10
    }),
    12: _tools.RODict({
        "ID": 12,
        "map": 1030,
        "targetType": 48,
        "targetParam": (5, 1030),
        "point": 10
    }),
    21: _tools.RODict({
        "ID": 21,
        "map": 1031,
        "targetType": 48,
        "targetParam": (5, 1031),
        "point": 10
    }),
    22: _tools.RODict({
        "ID": 22,
        "map": 1032,
        "targetType": 48,
        "targetParam": (5, 1032),
        "point": 10
    }),
    23: _tools.RODict({
        "ID": 23,
        "map": 1035,
        "targetType": 48,
        "targetParam": (5, 1035),
        "point": 10
    }),
    24: _tools.RODict({
        "ID": 24,
        "map": 1036,
        "targetType": 48,
        "targetParam": (5, 1036),
        "point": 10
    })
})
minKey = 1
maxKey = 24

mapId2Ids = {1002: [1, 3, 4], 1001: [5, 8], 1030: [9, 11, 12], 1031: [13, 17, 21], 1032: [14, 18, 22], 1035: [15, 19, 23], 1036: [16, 20, 24]}


mapId2Point = {1002: {26: 10, 22: 10, 48: 10}, 1001: {26: 10, 48: 10}, 1030: {26: 10, 22: 10, 48: 10}, 1031: {26: 10, 22: 10, 48: 10}, 1032: {26: 10, 22: 10, 48: 10}, 1035: {26: 10, 22: 10, 48: 10}, 1036: {26: 10, 22: 10, 48: 10}}
