# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: experience/revenue
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
        "levelgap": 15,
        "boundprop": 1,
        "expprop": 0.05,
        "rewardprop": 0.05
    }),
    2: _tools.RODict({
        "ID": 2,
        "levelgap": 14,
        "boundprop": 1,
        "expprop": 0.05,
        "rewardprop": 0.05
    }),
    3: _tools.RODict({
        "ID": 3,
        "levelgap": 13,
        "boundprop": 1,
        "expprop": 0.05,
        "rewardprop": 0.05
    }),
    4: _tools.RODict({
        "ID": 4,
        "levelgap": 12,
        "boundprop": 1,
        "expprop": 0.2,
        "rewardprop": 0.2
    }),
    5: _tools.RODict({
        "ID": 5,
        "levelgap": 11,
        "boundprop": 1,
        "expprop": 0.4,
        "rewardprop": 0.4
    }),
    6: _tools.RODict({
        "ID": 6,
        "levelgap": 10,
        "boundprop": 1,
        "expprop": 0.6,
        "rewardprop": 0.6
    }),
    7: _tools.RODict({
        "ID": 7,
        "levelgap": 9,
        "boundprop": 1,
        "expprop": 0.8,
        "rewardprop": 0.8
    }),
    8: _tools.RODict({
        "ID": 8,
        "levelgap": 8,
        "boundprop": 1,
        "expprop": 1.0,
        "rewardprop": 1.0
    }),
    9: _tools.RODict({
        "ID": 9,
        "levelgap": 7,
        "boundprop": 1,
        "expprop": 1.0,
        "rewardprop": 1.0
    }),
    10: _tools.RODict({
        "ID": 10,
        "levelgap": 6,
        "boundprop": 1,
        "expprop": 1.0,
        "rewardprop": 1.0
    }),
    11: _tools.RODict({
        "ID": 11,
        "levelgap": 5,
        "boundprop": 0,
        "expprop": 1.0,
        "rewardprop": 1.0
    }),
    12: _tools.RODict({
        "ID": 12,
        "levelgap": 4,
        "boundprop": 0,
        "expprop": 1.0,
        "rewardprop": 1.0
    }),
    13: _tools.RODict({
        "ID": 13,
        "levelgap": 3,
        "boundprop": 0,
        "expprop": 1.0,
        "rewardprop": 1.0
    }),
    14: _tools.RODict({
        "ID": 14,
        "levelgap": 2,
        "boundprop": 0,
        "expprop": 1.0,
        "rewardprop": 1.0
    }),
    15: _tools.RODict({
        "ID": 15,
        "levelgap": 1,
        "boundprop": 0,
        "expprop": 1.0,
        "rewardprop": 1.0
    }),
    16: _tools.RODict({
        "ID": 16,
        "levelgap": 0,
        "boundprop": 0,
        "expprop": 1.0,
        "rewardprop": 1.0
    }),
    17: _tools.RODict({
        "ID": 17,
        "levelgap": -1,
        "boundprop": 0,
        "expprop": 1.0,
        "rewardprop": 1.0
    }),
    18: _tools.RODict({
        "ID": 18,
        "levelgap": -2,
        "boundprop": 0,
        "expprop": 1.0,
        "rewardprop": 1.0
    }),
    19: _tools.RODict({
        "ID": 19,
        "levelgap": -3,
        "boundprop": 0,
        "expprop": 1.0,
        "rewardprop": 1.0
    }),
    20: _tools.RODict({
        "ID": 20,
        "levelgap": -4,
        "boundprop": 0,
        "expprop": 1.0,
        "rewardprop": 1.0
    }),
    21: _tools.RODict({
        "ID": 21,
        "levelgap": -5,
        "boundprop": 0,
        "expprop": 1.0,
        "rewardprop": 1.0
    }),
    22: _tools.RODict({
        "ID": 22,
        "levelgap": -6,
        "boundprop": 1,
        "expprop": 0.8,
        "rewardprop": 0.8
    }),
    23: _tools.RODict({
        "ID": 23,
        "levelgap": -7,
        "boundprop": 1,
        "expprop": 0.6,
        "rewardprop": 0.6
    }),
    24: _tools.RODict({
        "ID": 24,
        "levelgap": -8,
        "boundprop": 1,
        "expprop": 0.4,
        "rewardprop": 0.4
    }),
    25: _tools.RODict({
        "ID": 25,
        "levelgap": -9,
        "boundprop": 1,
        "expprop": 0.2,
        "rewardprop": 0.2
    }),
    26: _tools.RODict({
        "ID": 26,
        "levelgap": -10,
        "boundprop": 1,
        "expprop": 0.05,
        "rewardprop": 0.05
    }),
    27: _tools.RODict({
        "ID": 27,
        "levelgap": -11,
        "boundprop": 1,
        "expprop": 0.05,
        "rewardprop": 0.05
    }),
    28: _tools.RODict({
        "ID": 28,
        "levelgap": -12,
        "boundprop": 1,
        "expprop": 0.05,
        "rewardprop": 0.05
    }),
    29: _tools.RODict({
        "ID": 29,
        "levelgap": -13,
        "boundprop": 1,
        "expprop": 0.05,
        "rewardprop": 0.05
    }),
    30: _tools.RODict({
        "ID": 30,
        "levelgap": -14,
        "boundprop": 1,
        "expprop": 0.05,
        "rewardprop": 0.05
    }),
    31: _tools.RODict({
        "ID": 31,
        "levelgap": -15,
        "boundprop": 1,
        "expprop": 0.05,
        "rewardprop": 0.05
    })
})
minKey = 1
maxKey = 31

revenueLevelGapDic = {15: {'ID': 1, 'levelgap': 15, 'boundprop': 1, 'expprop': 0.05, 'rewardprop': 0.05}, 14: {'ID': 2, 'levelgap': 14, 'boundprop': 1, 'expprop': 0.05, 'rewardprop': 0.05}, 13: {'ID': 3, 'levelgap': 13, 'boundprop': 1, 'expprop': 0.05, 'rewardprop': 0.05}, 12: {'ID': 4, 'levelgap': 12, 'boundprop': 1, 'expprop': 0.2, 'rewardprop': 0.2}, 11: {'ID': 5, 'levelgap': 11, 'boundprop': 1, 'expprop': 0.4, 'rewardprop': 0.4}, 10: {'ID': 6, 'levelgap': 10, 'boundprop': 1, 'expprop': 0.6, 'rewardprop': 0.6}, 9: {'ID': 7, 'levelgap': 9, 'boundprop': 1, 'expprop': 0.8, 'rewardprop': 0.8}, 8: {'ID': 8, 'levelgap': 8, 'boundprop': 1, 'expprop': 1.0, 'rewardprop': 1.0}, 7: {'ID': 9, 'levelgap': 7, 'boundprop': 1, 'expprop': 1.0, 'rewardprop': 1.0}, 6: {'ID': 10, 'levelgap': 6, 'boundprop': 1, 'expprop': 1.0, 'rewardprop': 1.0}, 5: {'ID': 11, 'levelgap': 5, 'boundprop': 0, 'expprop': 1.0, 'rewardprop': 1.0}, 4: {'ID': 12, 'levelgap': 4, 'boundprop': 0, 'expprop': 1.0, 'rewardprop': 1.0}, 3: {'ID': 13, 'levelgap': 3, 'boundprop': 0, 'expprop': 1.0, 'rewardprop': 1.0}, 2: {'ID': 14, 'levelgap': 2, 'boundprop': 0, 'expprop': 1.0, 'rewardprop': 1.0}, 1: {'ID': 15, 'levelgap': 1, 'boundprop': 0, 'expprop': 1.0, 'rewardprop': 1.0}, 0: {'ID': 16, 'levelgap': 0, 'boundprop': 0, 'expprop': 1.0, 'rewardprop': 1.0}, -1: {'ID': 17, 'levelgap': -1, 'boundprop': 0, 'expprop': 1.0, 'rewardprop': 1.0}, -2: {'ID': 18, 'levelgap': -2, 'boundprop': 0, 'expprop': 1.0, 'rewardprop': 1.0}, -3: {'ID': 19, 'levelgap': -3, 'boundprop': 0, 'expprop': 1.0, 'rewardprop': 1.0}, -4: {'ID': 20, 'levelgap': -4, 'boundprop': 0, 'expprop': 1.0, 'rewardprop': 1.0}, -5: {'ID': 21, 'levelgap': -5, 'boundprop': 0, 'expprop': 1.0, 'rewardprop': 1.0}, -6: {'ID': 22, 'levelgap': -6, 'boundprop': 1, 'expprop': 0.8, 'rewardprop': 0.8}, -7: {'ID': 23, 'levelgap': -7, 'boundprop': 1, 'expprop': 0.6, 'rewardprop': 0.6}, -8: {'ID': 24, 'levelgap': -8, 'boundprop': 1, 'expprop': 0.4, 'rewardprop': 0.4}, -9: {'ID': 25, 'levelgap': -9, 'boundprop': 1, 'expprop': 0.2, 'rewardprop': 0.2}, -10: {'ID': 26, 'levelgap': -10, 'boundprop': 1, 'expprop': 0.05, 'rewardprop': 0.05}, -11: {'ID': 27, 'levelgap': -11, 'boundprop': 1, 'expprop': 0.05, 'rewardprop': 0.05}, -12: {'ID': 28, 'levelgap': -12, 'boundprop': 1, 'expprop': 0.05, 'rewardprop': 0.05}, -13: {'ID': 29, 'levelgap': -13, 'boundprop': 1, 'expprop': 0.05, 'rewardprop': 0.05}, -14: {'ID': 30, 'levelgap': -14, 'boundprop': 1, 'expprop': 0.05, 'rewardprop': 0.05}, -15: {'ID': 31, 'levelgap': -15, 'boundprop': 1, 'expprop': 0.05, 'rewardprop': 0.05}}
