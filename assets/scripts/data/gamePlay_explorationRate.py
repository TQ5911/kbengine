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
    1001: _tools.RODict({
        "ID": 1001,
        "map": 1001,
        "targetType": 26,
        "targetParam": (7, 1001),
        "point": 15
    }),
    3001: _tools.RODict({
        "ID": 3001,
        "map": 1001,
        "targetType": 48,
        "targetParam": (15, 1001),
        "point": 20
    }),
    4001: _tools.RODict({
        "ID": 4001,
        "map": 1001,
        "targetType": 27,
        "targetParam": (3, 1001),
        "point": 10
    }),
    1002: _tools.RODict({
        "ID": 1002,
        "map": 1002,
        "targetType": 26,
        "targetParam": (7, 1002),
        "point": 15
    }),
    2001: _tools.RODict({
        "ID": 2001,
        "map": 1002,
        "targetType": 22,
        "targetParam": (10, 1002),
        "point": 10
    }),
    3002: _tools.RODict({
        "ID": 3002,
        "map": 1002,
        "targetType": 48,
        "targetParam": (10, 1002),
        "point": 20
    }),
    4002: _tools.RODict({
        "ID": 4002,
        "map": 1002,
        "targetType": 27,
        "targetParam": (3, 1002),
        "point": 10
    }),
    1003: _tools.RODict({
        "ID": 1003,
        "map": 1004,
        "targetType": 26,
        "targetParam": (7, 1004),
        "point": 15
    }),
    3003: _tools.RODict({
        "ID": 3003,
        "map": 1004,
        "targetType": 48,
        "targetParam": (15, 1004),
        "point": 20
    }),
    4003: _tools.RODict({
        "ID": 4003,
        "map": 1004,
        "targetType": 27,
        "targetParam": (3, 1004),
        "point": 10
    }),
    1006: _tools.RODict({
        "ID": 1006,
        "map": 1010,
        "targetType": 26,
        "targetParam": (7, 1010),
        "point": 15
    }),
    2005: _tools.RODict({
        "ID": 2005,
        "map": 1010,
        "targetType": 22,
        "targetParam": (15, 1010),
        "point": 10
    }),
    4004: _tools.RODict({
        "ID": 4004,
        "map": 1010,
        "targetType": 27,
        "targetParam": (3, 1010),
        "point": 10
    }),
    1007: _tools.RODict({
        "ID": 1007,
        "map": 1011,
        "targetType": 26,
        "targetParam": (7, 1011),
        "point": 15
    }),
    2006: _tools.RODict({
        "ID": 2006,
        "map": 1011,
        "targetType": 22,
        "targetParam": (10, 1011),
        "point": 10
    }),
    3007: _tools.RODict({
        "ID": 3007,
        "map": 1011,
        "targetType": 48,
        "targetParam": (8, 1011),
        "point": 20
    }),
    4005: _tools.RODict({
        "ID": 4005,
        "map": 1011,
        "targetType": 27,
        "targetParam": (3, 1011),
        "point": 10
    }),
    1008: _tools.RODict({
        "ID": 1008,
        "map": 1020,
        "targetType": 26,
        "targetParam": (7, 1020),
        "point": 15
    }),
    2007: _tools.RODict({
        "ID": 2007,
        "map": 1020,
        "targetType": 22,
        "targetParam": (10, 1020),
        "point": 10
    }),
    3008: _tools.RODict({
        "ID": 3008,
        "map": 1020,
        "targetType": 48,
        "targetParam": (10, 1020),
        "point": 20
    }),
    4006: _tools.RODict({
        "ID": 4006,
        "map": 1020,
        "targetType": 27,
        "targetParam": (3, 1020),
        "point": 10
    }),
    1009: _tools.RODict({
        "ID": 1009,
        "map": 1021,
        "targetType": 26,
        "targetParam": (7, 1021),
        "point": 15
    }),
    2008: _tools.RODict({
        "ID": 2008,
        "map": 1021,
        "targetType": 22,
        "targetParam": (15, 1021),
        "point": 10
    }),
    4007: _tools.RODict({
        "ID": 4007,
        "map": 1021,
        "targetType": 27,
        "targetParam": (3, 1021),
        "point": 10
    }),
    1010: _tools.RODict({
        "ID": 1010,
        "map": 1024,
        "targetType": 26,
        "targetParam": (7, 1024),
        "point": 15
    }),
    2009: _tools.RODict({
        "ID": 2009,
        "map": 1024,
        "targetType": 22,
        "targetParam": (15, 1024),
        "point": 10
    }),
    4008: _tools.RODict({
        "ID": 4008,
        "map": 1024,
        "targetType": 27,
        "targetParam": (3, 1024),
        "point": 10
    }),
    1013: _tools.RODict({
        "ID": 1013,
        "map": 1030,
        "targetType": 26,
        "targetParam": (7, 1030),
        "point": 15
    }),
    2012: _tools.RODict({
        "ID": 2012,
        "map": 1030,
        "targetType": 22,
        "targetParam": (10, 1030),
        "point": 10
    }),
    3013: _tools.RODict({
        "ID": 3013,
        "map": 1030,
        "targetType": 48,
        "targetParam": (12, 1030),
        "point": 20
    }),
    4009: _tools.RODict({
        "ID": 4009,
        "map": 1030,
        "targetType": 27,
        "targetParam": (3, 1030),
        "point": 10
    }),
    1014: _tools.RODict({
        "ID": 1014,
        "map": 1031,
        "targetType": 26,
        "targetParam": (7, 1031),
        "point": 15
    }),
    2013: _tools.RODict({
        "ID": 2013,
        "map": 1031,
        "targetType": 22,
        "targetParam": (15, 1031),
        "point": 10
    }),
    4010: _tools.RODict({
        "ID": 4010,
        "map": 1031,
        "targetType": 27,
        "targetParam": (3, 1031),
        "point": 10
    }),
    1015: _tools.RODict({
        "ID": 1015,
        "map": 1032,
        "targetType": 26,
        "targetParam": (7, 1032),
        "point": 15
    }),
    2014: _tools.RODict({
        "ID": 2014,
        "map": 1032,
        "targetType": 22,
        "targetParam": (15, 1032),
        "point": 10
    }),
    4011: _tools.RODict({
        "ID": 4011,
        "map": 1032,
        "targetType": 27,
        "targetParam": (3, 1032),
        "point": 10
    }),
    1016: _tools.RODict({
        "ID": 1016,
        "map": 1035,
        "targetType": 26,
        "targetParam": (7, 1035),
        "point": 15
    }),
    2015: _tools.RODict({
        "ID": 2015,
        "map": 1035,
        "targetType": 22,
        "targetParam": (15, 1035),
        "point": 10
    }),
    4012: _tools.RODict({
        "ID": 4012,
        "map": 1035,
        "targetType": 27,
        "targetParam": (3, 1035),
        "point": 10
    }),
    1023: _tools.RODict({
        "ID": 1023,
        "map": 1120,
        "targetType": 26,
        "targetParam": (7, 1120),
        "point": 15
    }),
    2022: _tools.RODict({
        "ID": 2022,
        "map": 1120,
        "targetType": 22,
        "targetParam": (15, 1120),
        "point": 10
    }),
    3023: _tools.RODict({
        "ID": 3023,
        "map": 1120,
        "targetType": 48,
        "targetParam": (3, 1120),
        "point": 20
    }),
    4013: _tools.RODict({
        "ID": 4013,
        "map": 1120,
        "targetType": 27,
        "targetParam": (3, 1120),
        "point": 10
    }),
    1024: _tools.RODict({
        "ID": 1024,
        "map": 1121,
        "targetType": 26,
        "targetParam": (7, 1121),
        "point": 15
    }),
    2023: _tools.RODict({
        "ID": 2023,
        "map": 1121,
        "targetType": 22,
        "targetParam": (15, 1121),
        "point": 10
    }),
    3024: _tools.RODict({
        "ID": 3024,
        "map": 1121,
        "targetType": 48,
        "targetParam": (1, 1121),
        "point": 20
    }),
    4014: _tools.RODict({
        "ID": 4014,
        "map": 1121,
        "targetType": 27,
        "targetParam": (3, 1121),
        "point": 10
    }),
    1025: _tools.RODict({
        "ID": 1025,
        "map": 1123,
        "targetType": 26,
        "targetParam": (7, 1123),
        "point": 15
    }),
    2024: _tools.RODict({
        "ID": 2024,
        "map": 1123,
        "targetType": 22,
        "targetParam": (15, 1123),
        "point": 10
    }),
    3025: _tools.RODict({
        "ID": 3025,
        "map": 1123,
        "targetType": 48,
        "targetParam": (2, 1123),
        "point": 20
    }),
    4015: _tools.RODict({
        "ID": 4015,
        "map": 1123,
        "targetType": 27,
        "targetParam": (3, 1123),
        "point": 10
    })
})
minKey = 1001
maxKey = 4015

mapId2Ids = {1001: [1001, 3001, 4001], 1002: [1002, 2001, 3002, 4002], 1004: [1003, 3003, 4003], 1010: [1006, 2005, 4004], 1011: [1007, 2006, 3007, 4005], 1020: [1008, 2007, 3008, 4006], 1021: [1009, 2008, 4007], 1024: [1010, 2009, 4008], 1030: [1013, 2012, 3013, 4009], 1031: [1014, 2013, 4010], 1032: [1015, 2014, 4011], 1035: [1016, 2015, 4012], 1120: [1023, 2022, 3023, 4013], 1121: [1024, 2023, 3024, 4014], 1123: [1025, 2024, 3025, 4015]}


mapId2Point = {1001: {26: 15, 48: 20, 27: 10}, 1002: {26: 15, 22: 10, 48: 20, 27: 10}, 1004: {26: 15, 48: 20, 27: 10}, 1010: {26: 15, 22: 10, 27: 10}, 1011: {26: 15, 22: 10, 48: 20, 27: 10}, 1020: {26: 15, 22: 10, 48: 20, 27: 10}, 1021: {26: 15, 22: 10, 27: 10}, 1024: {26: 15, 22: 10, 27: 10}, 1030: {26: 15, 22: 10, 48: 20, 27: 10}, 1031: {26: 15, 22: 10, 27: 10}, 1032: {26: 15, 22: 10, 27: 10}, 1035: {26: 15, 22: 10, 27: 10}, 1120: {26: 15, 22: 10, 48: 20, 27: 10}, 1121: {26: 15, 22: 10, 48: 20, 27: 10}, 1123: {26: 15, 22: 10, 48: 20, 27: 10}}
