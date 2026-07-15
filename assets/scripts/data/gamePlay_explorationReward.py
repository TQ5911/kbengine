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
        "acPoint": 70,
        "reward": 40042001,
    }),
    2: _tools.RODict({
        "ID": 2,
        "map": 1001,
        "acPoint": 150,
        "reward": 40042002,
    }),
    3: _tools.RODict({
        "ID": 3,
        "map": 1001,
        "acPoint": 230,
        "reward": 40042003,
    }),
    4: _tools.RODict({
        "ID": 4,
        "map": 1001,
        "acPoint": 310,
        "reward": 40042006,
    }),
    5: _tools.RODict({
        "ID": 5,
        "map": 1001,
        "acPoint": 390,
        "reward": 40042005,
    }),
    6: _tools.RODict({
        "ID": 6,
        "map": 1002,
        "acPoint": 70,
        "reward": 40042001,
    }),
    7: _tools.RODict({
        "ID": 7,
        "map": 1002,
        "acPoint": 150,
        "reward": 40042002,
    }),
    8: _tools.RODict({
        "ID": 8,
        "map": 1002,
        "acPoint": 230,
        "reward": 40042003,
    }),
    9: _tools.RODict({
        "ID": 9,
        "map": 1002,
        "acPoint": 310,
        "reward": 40042007,
    }),
    10: _tools.RODict({
        "ID": 10,
        "map": 1002,
        "acPoint": 390,
        "reward": 40042005,
    }),
    11: _tools.RODict({
        "ID": 11,
        "map": 1004,
        "acPoint": 70,
        "reward": 40042001,
    }),
    12: _tools.RODict({
        "ID": 12,
        "map": 1004,
        "acPoint": 150,
        "reward": 40042002,
    }),
    13: _tools.RODict({
        "ID": 13,
        "map": 1004,
        "acPoint": 230,
        "reward": 40042003,
    }),
    14: _tools.RODict({
        "ID": 14,
        "map": 1004,
        "acPoint": 310,
        "reward": 40042008,
    }),
    15: _tools.RODict({
        "ID": 15,
        "map": 1004,
        "acPoint": 390,
        "reward": 40042005,
    }),
    16: _tools.RODict({
        "ID": 16,
        "map": 1010,
        "acPoint": 40,
        "reward": 40042001,
    }),
    17: _tools.RODict({
        "ID": 17,
        "map": 1010,
        "acPoint": 90,
        "reward": 40042002,
    }),
    18: _tools.RODict({
        "ID": 18,
        "map": 1010,
        "acPoint": 140,
        "reward": 40042003,
    }),
    19: _tools.RODict({
        "ID": 19,
        "map": 1010,
        "acPoint": 190,
        "reward": 40042004,
    }),
    20: _tools.RODict({
        "ID": 20,
        "map": 1010,
        "acPoint": 240,
        "reward": 40042005,
    }),
    21: _tools.RODict({
        "ID": 21,
        "map": 1011,
        "acPoint": 60,
        "reward": 40042001,
    }),
    22: _tools.RODict({
        "ID": 22,
        "map": 1011,
        "acPoint": 130,
        "reward": 40042002,
    }),
    23: _tools.RODict({
        "ID": 23,
        "map": 1011,
        "acPoint": 200,
        "reward": 40042003,
    }),
    24: _tools.RODict({
        "ID": 24,
        "map": 1011,
        "acPoint": 270,
        "reward": 40042004,
    }),
    25: _tools.RODict({
        "ID": 25,
        "map": 1011,
        "acPoint": 340,
        "reward": 40042005,
    }),
    26: _tools.RODict({
        "ID": 26,
        "map": 1020,
        "acPoint": 70,
        "reward": 40042001,
    }),
    27: _tools.RODict({
        "ID": 27,
        "map": 1020,
        "acPoint": 150,
        "reward": 40042002,
    }),
    28: _tools.RODict({
        "ID": 28,
        "map": 1020,
        "acPoint": 230,
        "reward": 40042003,
    }),
    29: _tools.RODict({
        "ID": 29,
        "map": 1020,
        "acPoint": 310,
        "reward": 40042004,
    }),
    30: _tools.RODict({
        "ID": 30,
        "map": 1020,
        "acPoint": 390,
        "reward": 40042005,
    }),
    31: _tools.RODict({
        "ID": 31,
        "map": 1021,
        "acPoint": 40,
        "reward": 40042001,
    }),
    32: _tools.RODict({
        "ID": 32,
        "map": 1021,
        "acPoint": 90,
        "reward": 40042002,
    }),
    33: _tools.RODict({
        "ID": 33,
        "map": 1021,
        "acPoint": 140,
        "reward": 40042003,
    }),
    34: _tools.RODict({
        "ID": 34,
        "map": 1021,
        "acPoint": 190,
        "reward": 40042004,
    }),
    35: _tools.RODict({
        "ID": 35,
        "map": 1021,
        "acPoint": 240,
        "reward": 40042005,
    }),
    36: _tools.RODict({
        "ID": 36,
        "map": 1024,
        "acPoint": 40,
        "reward": 40042001,
    }),
    37: _tools.RODict({
        "ID": 37,
        "map": 1024,
        "acPoint": 90,
        "reward": 40042002,
    }),
    38: _tools.RODict({
        "ID": 38,
        "map": 1024,
        "acPoint": 140,
        "reward": 40042003,
    }),
    39: _tools.RODict({
        "ID": 39,
        "map": 1024,
        "acPoint": 190,
        "reward": 40042004,
    }),
    40: _tools.RODict({
        "ID": 40,
        "map": 1024,
        "acPoint": 240,
        "reward": 40042005,
    }),
    41: _tools.RODict({
        "ID": 41,
        "map": 1030,
        "acPoint": 80,
        "reward": 40042001,
    }),
    42: _tools.RODict({
        "ID": 42,
        "map": 1030,
        "acPoint": 170,
        "reward": 40042002,
    }),
    43: _tools.RODict({
        "ID": 43,
        "map": 1030,
        "acPoint": 260,
        "reward": 40042003,
    }),
    44: _tools.RODict({
        "ID": 44,
        "map": 1030,
        "acPoint": 350,
        "reward": 40042004,
    }),
    45: _tools.RODict({
        "ID": 45,
        "map": 1030,
        "acPoint": 440,
        "reward": 40042005,
    }),
    46: _tools.RODict({
        "ID": 46,
        "map": 1031,
        "acPoint": 40,
        "reward": 40042001,
    }),
    47: _tools.RODict({
        "ID": 47,
        "map": 1031,
        "acPoint": 90,
        "reward": 40042002,
    }),
    48: _tools.RODict({
        "ID": 48,
        "map": 1031,
        "acPoint": 140,
        "reward": 40042003,
    }),
    49: _tools.RODict({
        "ID": 49,
        "map": 1031,
        "acPoint": 190,
        "reward": 40042004,
    }),
    50: _tools.RODict({
        "ID": 50,
        "map": 1031,
        "acPoint": 240,
        "reward": 40042005,
    }),
    51: _tools.RODict({
        "ID": 51,
        "map": 1032,
        "acPoint": 40,
        "reward": 40042001,
    }),
    52: _tools.RODict({
        "ID": 52,
        "map": 1032,
        "acPoint": 90,
        "reward": 40042002,
    }),
    53: _tools.RODict({
        "ID": 53,
        "map": 1032,
        "acPoint": 140,
        "reward": 40042003,
    }),
    54: _tools.RODict({
        "ID": 54,
        "map": 1032,
        "acPoint": 190,
        "reward": 40042004,
    }),
    55: _tools.RODict({
        "ID": 55,
        "map": 1032,
        "acPoint": 240,
        "reward": 40042005,
    }),
    56: _tools.RODict({
        "ID": 56,
        "map": 1035,
        "acPoint": 40,
        "reward": 40042001,
    }),
    57: _tools.RODict({
        "ID": 57,
        "map": 1035,
        "acPoint": 90,
        "reward": 40042002,
    }),
    58: _tools.RODict({
        "ID": 58,
        "map": 1035,
        "acPoint": 140,
        "reward": 40042003,
    }),
    59: _tools.RODict({
        "ID": 59,
        "map": 1035,
        "acPoint": 190,
        "reward": 40042004,
    }),
    60: _tools.RODict({
        "ID": 60,
        "map": 1035,
        "acPoint": 240,
        "reward": 40042005,
    }),
    61: _tools.RODict({
        "ID": 61,
        "map": 1120,
        "acPoint": 50,
        "reward": 40042001,
    }),
    62: _tools.RODict({
        "ID": 62,
        "map": 1120,
        "acPoint": 110,
        "reward": 40042002,
    }),
    63: _tools.RODict({
        "ID": 63,
        "map": 1120,
        "acPoint": 170,
        "reward": 40042003,
    }),
    64: _tools.RODict({
        "ID": 64,
        "map": 1120,
        "acPoint": 230,
        "reward": 40042004,
    }),
    65: _tools.RODict({
        "ID": 65,
        "map": 1120,
        "acPoint": 290,
        "reward": 40042005,
    }),
    66: _tools.RODict({
        "ID": 66,
        "map": 1121,
        "acPoint": 45,
        "reward": 40042001,
    }),
    67: _tools.RODict({
        "ID": 67,
        "map": 1121,
        "acPoint": 100,
        "reward": 40042002,
    }),
    68: _tools.RODict({
        "ID": 68,
        "map": 1121,
        "acPoint": 155,
        "reward": 40042003,
    }),
    69: _tools.RODict({
        "ID": 69,
        "map": 1121,
        "acPoint": 210,
        "reward": 40042004,
    }),
    70: _tools.RODict({
        "ID": 70,
        "map": 1121,
        "acPoint": 265,
        "reward": 40042005,
    }),
    71: _tools.RODict({
        "ID": 71,
        "map": 1123,
        "acPoint": 45,
        "reward": 40042001,
    }),
    72: _tools.RODict({
        "ID": 72,
        "map": 1123,
        "acPoint": 100,
        "reward": 40042002,
    }),
    73: _tools.RODict({
        "ID": 73,
        "map": 1123,
        "acPoint": 155,
        "reward": 40042003,
    }),
    74: _tools.RODict({
        "ID": 74,
        "map": 1123,
        "acPoint": 210,
        "reward": 40042004,
    }),
    75: _tools.RODict({
        "ID": 75,
        "map": 1123,
        "acPoint": 265,
        "reward": 40042005,
    })
})
minKey = 1
maxKey = 75

mapId2Ids = {1001: [1, 2, 3, 4, 5], 1002: [6, 7, 8, 9, 10], 1004: [11, 12, 13, 14, 15], 1010: [16, 17, 18, 19, 20], 1011: [21, 22, 23, 24, 25], 1020: [26, 27, 28, 29, 30], 1021: [31, 32, 33, 34, 35], 1024: [36, 37, 38, 39, 40], 1030: [41, 42, 43, 44, 45], 1031: [46, 47, 48, 49, 50], 1032: [51, 52, 53, 54, 55], 1035: [56, 57, 58, 59, 60], 1120: [61, 62, 63, 64, 65], 1121: [66, 67, 68, 69, 70], 1123: [71, 72, 73, 74, 75]}


mapId2Reward = {1001: [(70, 40042001), (150, 40042002), (230, 40042003), (310, 40042006), (390, 40042005)], 1002: [(70, 40042001), (150, 40042002), (230, 40042003), (310, 40042007), (390, 40042005)], 1004: [(70, 40042001), (150, 40042002), (230, 40042003), (310, 40042008), (390, 40042005)], 1010: [(40, 40042001), (90, 40042002), (140, 40042003), (190, 40042004), (240, 40042005)], 1011: [(60, 40042001), (130, 40042002), (200, 40042003), (270, 40042004), (340, 40042005)], 1020: [(70, 40042001), (150, 40042002), (230, 40042003), (310, 40042004), (390, 40042005)], 1021: [(40, 40042001), (90, 40042002), (140, 40042003), (190, 40042004), (240, 40042005)], 1024: [(40, 40042001), (90, 40042002), (140, 40042003), (190, 40042004), (240, 40042005)], 1030: [(80, 40042001), (170, 40042002), (260, 40042003), (350, 40042004), (440, 40042005)], 1031: [(40, 40042001), (90, 40042002), (140, 40042003), (190, 40042004), (240, 40042005)], 1032: [(40, 40042001), (90, 40042002), (140, 40042003), (190, 40042004), (240, 40042005)], 1035: [(40, 40042001), (90, 40042002), (140, 40042003), (190, 40042004), (240, 40042005)], 1120: [(50, 40042001), (110, 40042002), (170, 40042003), (230, 40042004), (290, 40042005)], 1121: [(45, 40042001), (100, 40042002), (155, 40042003), (210, 40042004), (265, 40042005)], 1123: [(45, 40042001), (100, 40042002), (155, 40042003), (210, 40042004), (265, 40042005)]}
