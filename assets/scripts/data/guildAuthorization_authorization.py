# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: guildAuthorization/authorization
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
        "guildJob": "leader",
        "name": "帮主",
        "authorization": _tools.ROList([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]),
        "level": 1
    }),
    2: _tools.RODict({
        "ID": 2,
        "guildJob": "coleader",
        "name": "副帮主",
        "authorization": _tools.ROList([2, 4, 5, 6, 9, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30, 31]),
        "level": 2
    }),
    3: _tools.RODict({
        "ID": 3,
        "guildJob": "elders",
        "name": "长老",
        "authorization": _tools.ROList([5, 6, 11, 12, 24, 25, 28, 30, 31]),
        "level": 3
    }),
    4: _tools.RODict({
        "ID": 4,
        "guildJob": "member",
        "name": "帮众",
        "authorization": None,
        "level": 4
    })
})
minKey = 1
maxKey = 4

authorization2Job = _tools.RODict({
    0: _tools.ROList(['1']),
    1: _tools.ROList(['1']),
    2: _tools.ROList(['1', '2']),
    3: _tools.ROList(['1']),
    4: _tools.ROList(['1', '2']),
    5: _tools.ROList(['1', '2', '3']),
    6: _tools.ROList(['1', '2', '3']),
    7: _tools.ROList(['1']),
    8: _tools.ROList(['1']),
    9: _tools.ROList(['1', '2']),
    10: _tools.ROList(['1']),
    11: _tools.ROList(['1', '2', '3']),
    12: _tools.ROList(['1', '2', '3']),
    13: _tools.ROList(['1', '2']),
    14: _tools.ROList(['1']),
    15: _tools.ROList(['1', '2']),
    16: _tools.ROList(['1', '2']),
    17: _tools.ROList(['1', '2']),
    18: _tools.ROList(['1', '2']),
    19: _tools.ROList(['1', '2']),
    20: _tools.ROList(['1', '2']),
    21: _tools.ROList(['1', '2']),
    22: _tools.ROList(['1', '2']),
    23: _tools.ROList(['1', '2']),
    24: _tools.ROList(['1', '2', '3']),
    25: _tools.ROList(['1', '2', '3']),
    26: _tools.ROList(['1', '2']),
    27: _tools.ROList(['1', '2']),
    28: _tools.ROList(['1', '2', '3']),
    29: _tools.ROList(['1']),
    30: _tools.ROList(['1', '2', '3']),
    31: _tools.ROList(['1', '2', '3']),
})