# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: experience/bindWorldLevel
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
        "groupID": 1,
        "levelGap": 6,
        "rewardBind": -0.3
    }),
    2: _tools.RODict({
        "ID": 2,
        "groupID": 1,
        "levelGap": 5,
        "rewardBind": -0.25
    }),
    3: _tools.RODict({
        "ID": 3,
        "groupID": 1,
        "levelGap": 4,
        "rewardBind": -0.2
    }),
    4: _tools.RODict({
        "ID": 4,
        "groupID": 1,
        "levelGap": 3,
        "rewardBind": -0.15
    }),
    5: _tools.RODict({
        "ID": 5,
        "groupID": 1,
        "levelGap": 2,
        "rewardBind": -0.1
    }),
    6: _tools.RODict({
        "ID": 6,
        "groupID": 1,
        "levelGap": 1,
        "rewardBind": -0.05
    }),
    7: _tools.RODict({
        "ID": 7,
        "groupID": 1,
        "levelGap": 0,
        "rewardBind": 0.0
    }),
    8: _tools.RODict({
        "ID": 8,
        "groupID": 1,
        "levelGap": -1,
        "rewardBind": 0.05
    }),
    9: _tools.RODict({
        "ID": 9,
        "groupID": 1,
        "levelGap": -2,
        "rewardBind": 0.1
    }),
    10: _tools.RODict({
        "ID": 10,
        "groupID": 1,
        "levelGap": -3,
        "rewardBind": 0.15
    }),
    11: _tools.RODict({
        "ID": 11,
        "groupID": 1,
        "levelGap": -4,
        "rewardBind": 0.2
    }),
    12: _tools.RODict({
        "ID": 12,
        "groupID": 1,
        "levelGap": -5,
        "rewardBind": 0.25
    }),
    13: _tools.RODict({
        "ID": 13,
        "groupID": 1,
        "levelGap": -6,
        "rewardBind": 0.3
    }),
    14: _tools.RODict({
        "ID": 14,
        "groupID": 1,
        "levelGap": -7,
        "rewardBind": 0.35
    }),
    15: _tools.RODict({
        "ID": 15,
        "groupID": 1,
        "levelGap": -8,
        "rewardBind": 0.4
    }),
    16: _tools.RODict({
        "ID": 16,
        "groupID": 1,
        "levelGap": -9,
        "rewardBind": 0.45
    }),
    17: _tools.RODict({
        "ID": 17,
        "groupID": 2,
        "levelGap": 6,
        "rewardBind": -0.3
    }),
    18: _tools.RODict({
        "ID": 18,
        "groupID": 2,
        "levelGap": 5,
        "rewardBind": -0.25
    }),
    19: _tools.RODict({
        "ID": 19,
        "groupID": 2,
        "levelGap": 4,
        "rewardBind": -0.2
    }),
    20: _tools.RODict({
        "ID": 20,
        "groupID": 2,
        "levelGap": 3,
        "rewardBind": -0.15
    }),
    21: _tools.RODict({
        "ID": 21,
        "groupID": 2,
        "levelGap": 2,
        "rewardBind": -0.1
    }),
    22: _tools.RODict({
        "ID": 22,
        "groupID": 2,
        "levelGap": 1,
        "rewardBind": -0.05
    }),
    23: _tools.RODict({
        "ID": 23,
        "groupID": 2,
        "levelGap": 0,
        "rewardBind": 0.0
    }),
    24: _tools.RODict({
        "ID": 24,
        "groupID": 2,
        "levelGap": -1,
        "rewardBind": 0.05
    }),
    25: _tools.RODict({
        "ID": 25,
        "groupID": 2,
        "levelGap": -2,
        "rewardBind": 0.1
    }),
    26: _tools.RODict({
        "ID": 26,
        "groupID": 2,
        "levelGap": -3,
        "rewardBind": 0.15
    }),
    27: _tools.RODict({
        "ID": 27,
        "groupID": 2,
        "levelGap": -4,
        "rewardBind": 0.2
    }),
    28: _tools.RODict({
        "ID": 28,
        "groupID": 2,
        "levelGap": -5,
        "rewardBind": 0.25
    }),
    29: _tools.RODict({
        "ID": 29,
        "groupID": 2,
        "levelGap": -6,
        "rewardBind": 0.3
    }),
    30: _tools.RODict({
        "ID": 30,
        "groupID": 2,
        "levelGap": -7,
        "rewardBind": 0.35
    }),
    31: _tools.RODict({
        "ID": 31,
        "groupID": 2,
        "levelGap": -8,
        "rewardBind": 0.4
    }),
    32: _tools.RODict({
        "ID": 32,
        "groupID": 2,
        "levelGap": -9,
        "rewardBind": 0.45
    }),
    33: _tools.RODict({
        "ID": 33,
        "groupID": 2,
        "levelGap": -10,
        "rewardBind": 0.5
    }),
    34: _tools.RODict({
        "ID": 34,
        "groupID": 2,
        "levelGap": -11,
        "rewardBind": 0.55
    }),
    35: _tools.RODict({
        "ID": 35,
        "groupID": 2,
        "levelGap": -12,
        "rewardBind": 0.6
    }),
    36: _tools.RODict({
        "ID": 36,
        "groupID": 2,
        "levelGap": -13,
        "rewardBind": 0.65
    }),
    37: _tools.RODict({
        "ID": 37,
        "groupID": 2,
        "levelGap": -14,
        "rewardBind": 0.7
    }),
    38: _tools.RODict({
        "ID": 38,
        "groupID": 2,
        "levelGap": -15,
        "rewardBind": 0.75
    }),
    39: _tools.RODict({
        "ID": 39,
        "groupID": 2,
        "levelGap": -16,
        "rewardBind": 0.8
    }),
    40: _tools.RODict({
        "ID": 40,
        "groupID": 2,
        "levelGap": -17,
        "rewardBind": 0.85
    }),
    41: _tools.RODict({
        "ID": 41,
        "groupID": 2,
        "levelGap": -18,
        "rewardBind": 0.9
    }),
    42: _tools.RODict({
        "ID": 42,
        "groupID": 2,
        "levelGap": -19,
        "rewardBind": 0.95
    }),
    43: _tools.RODict({
        "ID": 43,
        "groupID": 2,
        "levelGap": -20,
        "rewardBind": 1.0
    })
})
minKey = 1
maxKey = 43