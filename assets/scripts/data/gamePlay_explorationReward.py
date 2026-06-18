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
        "map": 1002,
        "acPoint": 10,
        "reward": 40000091,
    }),
    2: _tools.RODict({
        "ID": 2,
        "map": 1002,
        "acPoint": 30,
        "reward": 40000091,
    }),
    3: _tools.RODict({
        "ID": 3,
        "map": 1002,
        "acPoint": 60,
        "reward": 40000091,
    }),
    4: _tools.RODict({
        "ID": 4,
        "map": 1002,
        "acPoint": 100,
        "reward": 40000091,
    }),
    5: _tools.RODict({
        "ID": 5,
        "map": 1002,
        "acPoint": 150,
        "reward": 40000091,
    }),
    6: _tools.RODict({
        "ID": 6,
        "map": 1001,
        "acPoint": 10,
        "reward": 40000091,
    }),
    7: _tools.RODict({
        "ID": 7,
        "map": 1001,
        "acPoint": 30,
        "reward": 40000091,
    }),
    8: _tools.RODict({
        "ID": 8,
        "map": 1001,
        "acPoint": 60,
        "reward": 40000091,
    }),
    9: _tools.RODict({
        "ID": 9,
        "map": 1001,
        "acPoint": 100,
        "reward": 40000091,
    }),
    10: _tools.RODict({
        "ID": 10,
        "map": 1001,
        "acPoint": 150,
        "reward": 40000091,
    }),
    11: _tools.RODict({
        "ID": 11,
        "map": 1030,
        "acPoint": 10,
        "reward": 40000091,
    }),
    12: _tools.RODict({
        "ID": 12,
        "map": 1030,
        "acPoint": 30,
        "reward": 40000091,
    }),
    13: _tools.RODict({
        "ID": 13,
        "map": 1030,
        "acPoint": 60,
        "reward": 40000091,
    }),
    14: _tools.RODict({
        "ID": 14,
        "map": 1030,
        "acPoint": 100,
        "reward": 40000091,
    }),
    15: _tools.RODict({
        "ID": 15,
        "map": 1030,
        "acPoint": 150,
        "reward": 40000091,
    }),
    16: _tools.RODict({
        "ID": 16,
        "map": 1031,
        "acPoint": 10,
        "reward": 40000091,
    }),
    17: _tools.RODict({
        "ID": 17,
        "map": 1031,
        "acPoint": 30,
        "reward": 40000091,
    }),
    18: _tools.RODict({
        "ID": 18,
        "map": 1031,
        "acPoint": 60,
        "reward": 40000091,
    }),
    19: _tools.RODict({
        "ID": 19,
        "map": 1031,
        "acPoint": 100,
        "reward": 40000091,
    }),
    20: _tools.RODict({
        "ID": 20,
        "map": 1031,
        "acPoint": 150,
        "reward": 40000091,
    }),
    21: _tools.RODict({
        "ID": 21,
        "map": 1032,
        "acPoint": 10,
        "reward": 40000091,
    }),
    22: _tools.RODict({
        "ID": 22,
        "map": 1032,
        "acPoint": 30,
        "reward": 40000091,
    }),
    23: _tools.RODict({
        "ID": 23,
        "map": 1032,
        "acPoint": 60,
        "reward": 40000091,
    }),
    24: _tools.RODict({
        "ID": 24,
        "map": 1032,
        "acPoint": 100,
        "reward": 40000091,
    }),
    25: _tools.RODict({
        "ID": 25,
        "map": 1032,
        "acPoint": 150,
        "reward": 40000091,
    }),
    26: _tools.RODict({
        "ID": 26,
        "map": 1035,
        "acPoint": 10,
        "reward": 40000091,
    }),
    27: _tools.RODict({
        "ID": 27,
        "map": 1035,
        "acPoint": 30,
        "reward": 40000091,
    }),
    28: _tools.RODict({
        "ID": 28,
        "map": 1035,
        "acPoint": 60,
        "reward": 40000091,
    }),
    29: _tools.RODict({
        "ID": 29,
        "map": 1035,
        "acPoint": 100,
        "reward": 40000091,
    }),
    30: _tools.RODict({
        "ID": 30,
        "map": 1035,
        "acPoint": 150,
        "reward": 40000091,
    }),
    31: _tools.RODict({
        "ID": 31,
        "map": 1036,
        "acPoint": 10,
        "reward": 40000091,
    }),
    32: _tools.RODict({
        "ID": 32,
        "map": 1036,
        "acPoint": 30,
        "reward": 40000091,
    }),
    33: _tools.RODict({
        "ID": 33,
        "map": 1036,
        "acPoint": 60,
        "reward": 40000091,
    }),
    34: _tools.RODict({
        "ID": 34,
        "map": 1036,
        "acPoint": 100,
        "reward": 40000091,
    }),
    35: _tools.RODict({
        "ID": 35,
        "map": 1036,
        "acPoint": 150,
        "reward": 40000091,
    })
})
minKey = 1
maxKey = 35

mapId2Ids = {1002: [1, 2, 3, 4, 5], 1001: [6, 7, 8, 9, 10], 1030: [11, 12, 13, 14, 15], 1031: [16, 17, 18, 19, 20], 1032: [21, 22, 23, 24, 25], 1035: [26, 27, 28, 29, 30], 1036: [31, 32, 33, 34, 35]}


mapId2Reward = {1002: [(10, 40000091), (30, 40000091), (60, 40000091), (100, 40000091), (150, 40000091)], 1001: [(10, 40000091), (30, 40000091), (60, 40000091), (100, 40000091), (150, 40000091)], 1030: [(10, 40000091), (30, 40000091), (60, 40000091), (100, 40000091), (150, 40000091)], 1031: [(10, 40000091), (30, 40000091), (60, 40000091), (100, 40000091), (150, 40000091)], 1032: [(10, 40000091), (30, 40000091), (60, 40000091), (100, 40000091), (150, 40000091)], 1035: [(10, 40000091), (30, 40000091), (60, 40000091), (100, 40000091), (150, 40000091)], 1036: [(10, 40000091), (30, 40000091), (60, 40000091), (100, 40000091), (150, 40000091)]}
