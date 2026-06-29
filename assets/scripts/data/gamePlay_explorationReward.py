# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: gamePlay/explorationReward
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
        "map": 1001,
        "acPoint": 65,
        "reward": 40000091,
    }),
    2: _tools.RODict({
        "ID": 2,
        "map": 1001,
        "acPoint": 140,
        "reward": 40000091,
    }),
    3: _tools.RODict({
        "ID": 3,
        "map": 1001,
        "acPoint": 215,
        "reward": 40000091,
    }),
    4: _tools.RODict({
        "ID": 4,
        "map": 1001,
        "acPoint": 290,
        "reward": 40000091,
    }),
    5: _tools.RODict({
        "ID": 5,
        "map": 1001,
        "acPoint": 365,
        "reward": 40000091,
    }),
    6: _tools.RODict({
        "ID": 6,
        "map": 1002,
        "acPoint": 65,
        "reward": 40000091,
    }),
    7: _tools.RODict({
        "ID": 7,
        "map": 1002,
        "acPoint": 140,
        "reward": 40000091,
    }),
    8: _tools.RODict({
        "ID": 8,
        "map": 1002,
        "acPoint": 215,
        "reward": 40000091,
    }),
    9: _tools.RODict({
        "ID": 9,
        "map": 1002,
        "acPoint": 290,
        "reward": 40000091,
    }),
    10: _tools.RODict({
        "ID": 10,
        "map": 1002,
        "acPoint": 365,
        "reward": 40000091,
    }),
    11: _tools.RODict({
        "ID": 11,
        "map": 1004,
        "acPoint": 65,
        "reward": 40000091,
    }),
    12: _tools.RODict({
        "ID": 12,
        "map": 1004,
        "acPoint": 140,
        "reward": 40000091,
    }),
    13: _tools.RODict({
        "ID": 13,
        "map": 1004,
        "acPoint": 215,
        "reward": 40000091,
    }),
    14: _tools.RODict({
        "ID": 14,
        "map": 1004,
        "acPoint": 290,
        "reward": 40000091,
    }),
    15: _tools.RODict({
        "ID": 15,
        "map": 1004,
        "acPoint": 365,
        "reward": 40000091,
    }),
    16: _tools.RODict({
        "ID": 16,
        "map": 1010,
        "acPoint": 35,
        "reward": 40000091,
    }),
    17: _tools.RODict({
        "ID": 17,
        "map": 1010,
        "acPoint": 80,
        "reward": 40000091,
    }),
    18: _tools.RODict({
        "ID": 18,
        "map": 1010,
        "acPoint": 125,
        "reward": 40000091,
    }),
    19: _tools.RODict({
        "ID": 19,
        "map": 1010,
        "acPoint": 170,
        "reward": 40000091,
    }),
    20: _tools.RODict({
        "ID": 20,
        "map": 1010,
        "acPoint": 215,
        "reward": 40000091,
    }),
    21: _tools.RODict({
        "ID": 21,
        "map": 1011,
        "acPoint": 55,
        "reward": 40000091,
    }),
    22: _tools.RODict({
        "ID": 22,
        "map": 1011,
        "acPoint": 120,
        "reward": 40000091,
    }),
    23: _tools.RODict({
        "ID": 23,
        "map": 1011,
        "acPoint": 185,
        "reward": 40000091,
    }),
    24: _tools.RODict({
        "ID": 24,
        "map": 1011,
        "acPoint": 250,
        "reward": 40000091,
    }),
    25: _tools.RODict({
        "ID": 25,
        "map": 1011,
        "acPoint": 315,
        "reward": 40000091,
    }),
    26: _tools.RODict({
        "ID": 26,
        "map": 1020,
        "acPoint": 65,
        "reward": 40000091,
    }),
    27: _tools.RODict({
        "ID": 27,
        "map": 1020,
        "acPoint": 140,
        "reward": 40000091,
    }),
    28: _tools.RODict({
        "ID": 28,
        "map": 1020,
        "acPoint": 215,
        "reward": 40000091,
    }),
    29: _tools.RODict({
        "ID": 29,
        "map": 1020,
        "acPoint": 290,
        "reward": 40000091,
    }),
    30: _tools.RODict({
        "ID": 30,
        "map": 1020,
        "acPoint": 365,
        "reward": 40000091,
    }),
    31: _tools.RODict({
        "ID": 31,
        "map": 1021,
        "acPoint": 35,
        "reward": 40000091,
    }),
    32: _tools.RODict({
        "ID": 32,
        "map": 1021,
        "acPoint": 80,
        "reward": 40000091,
    }),
    33: _tools.RODict({
        "ID": 33,
        "map": 1021,
        "acPoint": 125,
        "reward": 40000091,
    }),
    34: _tools.RODict({
        "ID": 34,
        "map": 1021,
        "acPoint": 170,
        "reward": 40000091,
    }),
    35: _tools.RODict({
        "ID": 35,
        "map": 1021,
        "acPoint": 215,
        "reward": 40000091,
    }),
    36: _tools.RODict({
        "ID": 36,
        "map": 1024,
        "acPoint": 35,
        "reward": 40000091,
    }),
    37: _tools.RODict({
        "ID": 37,
        "map": 1024,
        "acPoint": 80,
        "reward": 40000091,
    }),
    38: _tools.RODict({
        "ID": 38,
        "map": 1024,
        "acPoint": 125,
        "reward": 40000091,
    }),
    39: _tools.RODict({
        "ID": 39,
        "map": 1024,
        "acPoint": 170,
        "reward": 40000091,
    }),
    40: _tools.RODict({
        "ID": 40,
        "map": 1024,
        "acPoint": 215,
        "reward": 40000091,
    }),
    41: _tools.RODict({
        "ID": 41,
        "map": 1030,
        "acPoint": 75,
        "reward": 40000091,
    }),
    42: _tools.RODict({
        "ID": 42,
        "map": 1030,
        "acPoint": 160,
        "reward": 40000091,
    }),
    43: _tools.RODict({
        "ID": 43,
        "map": 1030,
        "acPoint": 245,
        "reward": 40000091,
    }),
    44: _tools.RODict({
        "ID": 44,
        "map": 1030,
        "acPoint": 330,
        "reward": 40000091,
    }),
    45: _tools.RODict({
        "ID": 45,
        "map": 1030,
        "acPoint": 415,
        "reward": 40000091,
    }),
    46: _tools.RODict({
        "ID": 46,
        "map": 1031,
        "acPoint": 35,
        "reward": 40000091,
    }),
    47: _tools.RODict({
        "ID": 47,
        "map": 1031,
        "acPoint": 80,
        "reward": 40000091,
    }),
    48: _tools.RODict({
        "ID": 48,
        "map": 1031,
        "acPoint": 125,
        "reward": 40000091,
    }),
    49: _tools.RODict({
        "ID": 49,
        "map": 1031,
        "acPoint": 170,
        "reward": 40000091,
    }),
    50: _tools.RODict({
        "ID": 50,
        "map": 1031,
        "acPoint": 215,
        "reward": 40000091,
    }),
    51: _tools.RODict({
        "ID": 51,
        "map": 1032,
        "acPoint": 35,
        "reward": 40000091,
    }),
    52: _tools.RODict({
        "ID": 52,
        "map": 1032,
        "acPoint": 80,
        "reward": 40000091,
    }),
    53: _tools.RODict({
        "ID": 53,
        "map": 1032,
        "acPoint": 125,
        "reward": 40000091,
    }),
    54: _tools.RODict({
        "ID": 54,
        "map": 1032,
        "acPoint": 170,
        "reward": 40000091,
    }),
    55: _tools.RODict({
        "ID": 55,
        "map": 1032,
        "acPoint": 215,
        "reward": 40000091,
    }),
    56: _tools.RODict({
        "ID": 56,
        "map": 1035,
        "acPoint": 35,
        "reward": 40000091,
    }),
    57: _tools.RODict({
        "ID": 57,
        "map": 1035,
        "acPoint": 80,
        "reward": 40000091,
    }),
    58: _tools.RODict({
        "ID": 58,
        "map": 1035,
        "acPoint": 125,
        "reward": 40000091,
    }),
    59: _tools.RODict({
        "ID": 59,
        "map": 1035,
        "acPoint": 170,
        "reward": 40000091,
    }),
    60: _tools.RODict({
        "ID": 60,
        "map": 1035,
        "acPoint": 215,
        "reward": 40000091,
    }),
    61: _tools.RODict({
        "ID": 61,
        "map": 1120,
        "acPoint": 45,
        "reward": 40000091,
    }),
    62: _tools.RODict({
        "ID": 62,
        "map": 1120,
        "acPoint": 100,
        "reward": 40000091,
    }),
    63: _tools.RODict({
        "ID": 63,
        "map": 1120,
        "acPoint": 155,
        "reward": 40000091,
    }),
    64: _tools.RODict({
        "ID": 64,
        "map": 1120,
        "acPoint": 210,
        "reward": 40000091,
    }),
    65: _tools.RODict({
        "ID": 65,
        "map": 1120,
        "acPoint": 265,
        "reward": 40000091,
    }),
    66: _tools.RODict({
        "ID": 66,
        "map": 1121,
        "acPoint": 40,
        "reward": 40000091,
    }),
    67: _tools.RODict({
        "ID": 67,
        "map": 1121,
        "acPoint": 90,
        "reward": 40000091,
    }),
    68: _tools.RODict({
        "ID": 68,
        "map": 1121,
        "acPoint": 140,
        "reward": 40000091,
    }),
    69: _tools.RODict({
        "ID": 69,
        "map": 1121,
        "acPoint": 190,
        "reward": 40000091,
    }),
    70: _tools.RODict({
        "ID": 70,
        "map": 1121,
        "acPoint": 240,
        "reward": 40000091,
    }),
    71: _tools.RODict({
        "ID": 71,
        "map": 1123,
        "acPoint": 25,
        "reward": 40000091,
    }),
    72: _tools.RODict({
        "ID": 72,
        "map": 1123,
        "acPoint": 60,
        "reward": 40000091,
    }),
    73: _tools.RODict({
        "ID": 73,
        "map": 1123,
        "acPoint": 95,
        "reward": 40000091,
    }),
    74: _tools.RODict({
        "ID": 74,
        "map": 1123,
        "acPoint": 130,
        "reward": 40000091,
    }),
    75: _tools.RODict({
        "ID": 75,
        "map": 1123,
        "acPoint": 165,
        "reward": 40000091,
    })
})
minKey = 1
maxKey = 75

mapId2Ids = {1001: [1, 2, 3, 4, 5], 1002: [6, 7, 8, 9, 10], 1004: [11, 12, 13, 14, 15], 1010: [16, 17, 18, 19, 20], 1011: [21, 22, 23, 24, 25], 1020: [26, 27, 28, 29, 30], 1021: [31, 32, 33, 34, 35], 1024: [36, 37, 38, 39, 40], 1030: [41, 42, 43, 44, 45], 1031: [46, 47, 48, 49, 50], 1032: [51, 52, 53, 54, 55], 1035: [56, 57, 58, 59, 60], 1120: [61, 62, 63, 64, 65], 1121: [66, 67, 68, 69, 70], 1123: [71, 72, 73, 74, 75]}


mapId2Reward = {1001: [(65, 40000091), (140, 40000091), (215, 40000091), (290, 40000091), (365, 40000091)], 1002: [(65, 40000091), (140, 40000091), (215, 40000091), (290, 40000091), (365, 40000091)], 1004: [(65, 40000091), (140, 40000091), (215, 40000091), (290, 40000091), (365, 40000091)], 1010: [(35, 40000091), (80, 40000091), (125, 40000091), (170, 40000091), (215, 40000091)], 1011: [(55, 40000091), (120, 40000091), (185, 40000091), (250, 40000091), (315, 40000091)], 1020: [(65, 40000091), (140, 40000091), (215, 40000091), (290, 40000091), (365, 40000091)], 1021: [(35, 40000091), (80, 40000091), (125, 40000091), (170, 40000091), (215, 40000091)], 1024: [(35, 40000091), (80, 40000091), (125, 40000091), (170, 40000091), (215, 40000091)], 1030: [(75, 40000091), (160, 40000091), (245, 40000091), (330, 40000091), (415, 40000091)], 1031: [(35, 40000091), (80, 40000091), (125, 40000091), (170, 40000091), (215, 40000091)], 1032: [(35, 40000091), (80, 40000091), (125, 40000091), (170, 40000091), (215, 40000091)], 1035: [(35, 40000091), (80, 40000091), (125, 40000091), (170, 40000091), (215, 40000091)], 1120: [(45, 40000091), (100, 40000091), (155, 40000091), (210, 40000091), (265, 40000091)], 1121: [(40, 40000091), (90, 40000091), (140, 40000091), (190, 40000091), (240, 40000091)], 1123: [(25, 40000091), (60, 40000091), (95, 40000091), (130, 40000091), (165, 40000091)]}
