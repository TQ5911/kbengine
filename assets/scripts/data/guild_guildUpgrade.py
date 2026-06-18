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
        "upgradeExp": 2500,
        "juYingGeLv": 1
    }),
    2: _tools.RODict({
        "ID": 2,
        "upgradeExp": 4000,
        "juYingGeLv": 1
    }),
    3: _tools.RODict({
        "ID": 3,
        "upgradeExp": 6500,
        "juYingGeLv": 1
    }),
    4: _tools.RODict({
        "ID": 4,
        "upgradeExp": 10000,
        "juYingGeLv": 1
    }),
    5: _tools.RODict({
        "ID": 5,
        "upgradeExp": 14000,
        "juYingGeLv": 1
    }),
    6: _tools.RODict({
        "ID": 6,
        "upgradeExp": 17500,
        "juYingGeLv": 1
    }),
    7: _tools.RODict({
        "ID": 7,
        "upgradeExp": 21000,
        "juYingGeLv": 1
    }),
    8: _tools.RODict({
        "ID": 8,
        "upgradeExp": 25000,
        "juYingGeLv": 1
    }),
    9: _tools.RODict({
        "ID": 9,
        "upgradeExp": 38000,
        "juYingGeLv": 1
    }),
    10: _tools.RODict({
        "ID": 10,
        "upgradeExp": 47000,
        "juYingGeLv": 2
    }),
    11: _tools.RODict({
        "ID": 11,
        "upgradeExp": 56000,
        "juYingGeLv": 2
    }),
    12: _tools.RODict({
        "ID": 12,
        "upgradeExp": 65000,
        "juYingGeLv": 2
    }),
    13: _tools.RODict({
        "ID": 13,
        "upgradeExp": 74000,
        "juYingGeLv": 2
    }),
    14: _tools.RODict({
        "ID": 14,
        "upgradeExp": 82000,
        "juYingGeLv": 2
    }),
    15: _tools.RODict({
        "ID": 15,
        "upgradeExp": 91000,
        "juYingGeLv": 2
    }),
    16: _tools.RODict({
        "ID": 16,
        "upgradeExp": 100000,
        "juYingGeLv": 2
    }),
    17: _tools.RODict({
        "ID": 17,
        "upgradeExp": 109000,
        "juYingGeLv": 2
    }),
    18: _tools.RODict({
        "ID": 18,
        "upgradeExp": 120000,
        "juYingGeLv": 2
    }),
    19: _tools.RODict({
        "ID": 19,
        "upgradeExp": 170000,
        "juYingGeLv": 2
    }),
    20: _tools.RODict({
        "ID": 20,
        "upgradeExp": 190000,
        "juYingGeLv": 3
    }),
    21: _tools.RODict({
        "ID": 21,
        "upgradeExp": 210000,
        "juYingGeLv": 3
    }),
    22: _tools.RODict({
        "ID": 22,
        "upgradeExp": 225000,
        "juYingGeLv": 3
    }),
    23: _tools.RODict({
        "ID": 23,
        "upgradeExp": 245000,
        "juYingGeLv": 3
    }),
    24: _tools.RODict({
        "ID": 24,
        "upgradeExp": 265000,
        "juYingGeLv": 3
    }),
    25: _tools.RODict({
        "ID": 25,
        "upgradeExp": 295000,
        "juYingGeLv": 3
    }),
    26: _tools.RODict({
        "ID": 26,
        "upgradeExp": 320000,
        "juYingGeLv": 3
    }),
    27: _tools.RODict({
        "ID": 27,
        "upgradeExp": 350000,
        "juYingGeLv": 3
    }),
    28: _tools.RODict({
        "ID": 28,
        "upgradeExp": 380000,
        "juYingGeLv": 3
    }),
    29: _tools.RODict({
        "ID": 29,
        "upgradeExp": 510000,
        "juYingGeLv": 3
    }),
    30: _tools.RODict({
        "ID": 30,
        "upgradeExp": 555000,
        "juYingGeLv": 4
    }),
    31: _tools.RODict({
        "ID": 31,
        "upgradeExp": 600000,
        "juYingGeLv": 4
    }),
    32: _tools.RODict({
        "ID": 32,
        "upgradeExp": 650000,
        "juYingGeLv": 4
    }),
    33: _tools.RODict({
        "ID": 33,
        "upgradeExp": 690000,
        "juYingGeLv": 4
    }),
    34: _tools.RODict({
        "ID": 34,
        "upgradeExp": 740000,
        "juYingGeLv": 4
    }),
    35: _tools.RODict({
        "ID": 35,
        "upgradeExp": 800000,
        "juYingGeLv": 4
    }),
    36: _tools.RODict({
        "ID": 36,
        "upgradeExp": 850000,
        "juYingGeLv": 4
    }),
    37: _tools.RODict({
        "ID": 37,
        "upgradeExp": 910000,
        "juYingGeLv": 4
    }),
    38: _tools.RODict({
        "ID": 38,
        "upgradeExp": 970000,
        "juYingGeLv": 4
    }),
    39: _tools.RODict({
        "ID": 39,
        "upgradeExp": 1230000,
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