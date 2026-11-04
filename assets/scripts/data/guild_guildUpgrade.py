# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: guild/guildUpgrade
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
        "upgradeExp": 1300,
        "juYingGeLv": 1
    }),
    2: _tools.RODict({
        "ID": 2,
        "upgradeExp": 2000,
        "juYingGeLv": 1
    }),
    3: _tools.RODict({
        "ID": 3,
        "upgradeExp": 3400,
        "juYingGeLv": 1
    }),
    4: _tools.RODict({
        "ID": 4,
        "upgradeExp": 5400,
        "juYingGeLv": 1
    }),
    5: _tools.RODict({
        "ID": 5,
        "upgradeExp": 7400,
        "juYingGeLv": 1
    }),
    6: _tools.RODict({
        "ID": 6,
        "upgradeExp": 9400,
        "juYingGeLv": 1
    }),
    7: _tools.RODict({
        "ID": 7,
        "upgradeExp": 11400,
        "juYingGeLv": 1
    }),
    8: _tools.RODict({
        "ID": 8,
        "upgradeExp": 13400,
        "juYingGeLv": 1
    }),
    9: _tools.RODict({
        "ID": 9,
        "upgradeExp": 19700,
        "juYingGeLv": 1
    }),
    10: _tools.RODict({
        "ID": 10,
        "upgradeExp": 24200,
        "juYingGeLv": 2
    }),
    11: _tools.RODict({
        "ID": 11,
        "upgradeExp": 28700,
        "juYingGeLv": 2
    }),
    12: _tools.RODict({
        "ID": 12,
        "upgradeExp": 33300,
        "juYingGeLv": 2
    }),
    13: _tools.RODict({
        "ID": 13,
        "upgradeExp": 37800,
        "juYingGeLv": 2
    }),
    14: _tools.RODict({
        "ID": 14,
        "upgradeExp": 42300,
        "juYingGeLv": 2
    }),
    15: _tools.RODict({
        "ID": 15,
        "upgradeExp": 46900,
        "juYingGeLv": 2
    }),
    16: _tools.RODict({
        "ID": 16,
        "upgradeExp": 51400,
        "juYingGeLv": 2
    }),
    17: _tools.RODict({
        "ID": 17,
        "upgradeExp": 55900,
        "juYingGeLv": 2
    }),
    18: _tools.RODict({
        "ID": 18,
        "upgradeExp": 60500,
        "juYingGeLv": 2
    }),
    19: _tools.RODict({
        "ID": 19,
        "upgradeExp": 75600,
        "juYingGeLv": 2
    }),
    20: _tools.RODict({
        "ID": 20,
        "upgradeExp": 84000,
        "juYingGeLv": 3
    }),
    21: _tools.RODict({
        "ID": 21,
        "upgradeExp": 92400,
        "juYingGeLv": 3
    }),
    22: _tools.RODict({
        "ID": 22,
        "upgradeExp": 100800,
        "juYingGeLv": 3
    }),
    23: _tools.RODict({
        "ID": 23,
        "upgradeExp": 109200,
        "juYingGeLv": 3
    }),
    24: _tools.RODict({
        "ID": 24,
        "upgradeExp": 117600,
        "juYingGeLv": 3
    }),
    25: _tools.RODict({
        "ID": 25,
        "upgradeExp": 130200,
        "juYingGeLv": 3
    }),
    26: _tools.RODict({
        "ID": 26,
        "upgradeExp": 142800,
        "juYingGeLv": 3
    }),
    27: _tools.RODict({
        "ID": 27,
        "upgradeExp": 155400,
        "juYingGeLv": 3
    }),
    28: _tools.RODict({
        "ID": 28,
        "upgradeExp": 168000,
        "juYingGeLv": 3
    }),
    29: _tools.RODict({
        "ID": 29,
        "upgradeExp": 203300,
        "juYingGeLv": 3
    }),
    30: _tools.RODict({
        "ID": 30,
        "upgradeExp": 221800,
        "juYingGeLv": 4
    }),
    31: _tools.RODict({
        "ID": 31,
        "upgradeExp": 240200,
        "juYingGeLv": 4
    }),
    32: _tools.RODict({
        "ID": 32,
        "upgradeExp": 258700,
        "juYingGeLv": 4
    }),
    33: _tools.RODict({
        "ID": 33,
        "upgradeExp": 277200,
        "juYingGeLv": 4
    }),
    34: _tools.RODict({
        "ID": 34,
        "upgradeExp": 295700,
        "juYingGeLv": 4
    }),
    35: _tools.RODict({
        "ID": 35,
        "upgradeExp": 318800,
        "juYingGeLv": 4
    }),
    36: _tools.RODict({
        "ID": 36,
        "upgradeExp": 341900,
        "juYingGeLv": 4
    }),
    37: _tools.RODict({
        "ID": 37,
        "upgradeExp": 365000,
        "juYingGeLv": 4
    }),
    38: _tools.RODict({
        "ID": 38,
        "upgradeExp": 388100,
        "juYingGeLv": 4
    }),
    39: _tools.RODict({
        "ID": 39,
        "upgradeExp": 453600,
        "juYingGeLv": 4
    }),
    40: _tools.RODict({
        "ID": 40,
        "upgradeExp": 1250000,
        "juYingGeLv": 5
    })
})
minKey = 1
maxKey = 40