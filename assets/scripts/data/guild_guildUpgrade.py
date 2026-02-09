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
        "upgradeExp": 3800,
        "juYingGeLv": 1
    }),
    2: _tools.RODict({
        "ID": 2,
        "upgradeExp": 5700,
        "juYingGeLv": 1
    }),
    3: _tools.RODict({
        "ID": 3,
        "upgradeExp": 7600,
        "juYingGeLv": 1
    }),
    4: _tools.RODict({
        "ID": 4,
        "upgradeExp": 9500,
        "juYingGeLv": 1
    }),
    5: _tools.RODict({
        "ID": 5,
        "upgradeExp": 13300,
        "juYingGeLv": 1
    }),
    6: _tools.RODict({
        "ID": 6,
        "upgradeExp": 17100,
        "juYingGeLv": 1
    }),
    7: _tools.RODict({
        "ID": 7,
        "upgradeExp": 20900,
        "juYingGeLv": 1
    }),
    8: _tools.RODict({
        "ID": 8,
        "upgradeExp": 24700,
        "juYingGeLv": 1
    }),
    9: _tools.RODict({
        "ID": 9,
        "upgradeExp": 39900,
        "juYingGeLv": 1
    }),
    10: _tools.RODict({
        "ID": 10,
        "upgradeExp": 47880,
        "juYingGeLv": 2
    }),
    11: _tools.RODict({
        "ID": 11,
        "upgradeExp": 55860,
        "juYingGeLv": 2
    }),
    12: _tools.RODict({
        "ID": 12,
        "upgradeExp": 63840,
        "juYingGeLv": 2
    }),
    13: _tools.RODict({
        "ID": 13,
        "upgradeExp": 71820,
        "juYingGeLv": 2
    }),
    14: _tools.RODict({
        "ID": 14,
        "upgradeExp": 79800,
        "juYingGeLv": 2
    }),
    15: _tools.RODict({
        "ID": 15,
        "upgradeExp": 90440,
        "juYingGeLv": 2
    }),
    16: _tools.RODict({
        "ID": 16,
        "upgradeExp": 101080,
        "juYingGeLv": 2
    }),
    17: _tools.RODict({
        "ID": 17,
        "upgradeExp": 111720,
        "juYingGeLv": 2
    }),
    18: _tools.RODict({
        "ID": 18,
        "upgradeExp": 122360,
        "juYingGeLv": 3
    }),
    19: _tools.RODict({
        "ID": 19,
        "upgradeExp": 171000,
        "juYingGeLv": 3
    }),
    20: _tools.RODict({
        "ID": 20,
        "upgradeExp": 188100,
        "juYingGeLv": 3
    }),
    21: _tools.RODict({
        "ID": 21,
        "upgradeExp": 205200,
        "juYingGeLv": 3
    }),
    22: _tools.RODict({
        "ID": 22,
        "upgradeExp": 222300,
        "juYingGeLv": 3
    }),
    23: _tools.RODict({
        "ID": 23,
        "upgradeExp": 239400,
        "juYingGeLv": 3
    }),
    24: _tools.RODict({
        "ID": 24,
        "upgradeExp": 256500,
        "juYingGeLv": 3
    }),
    25: _tools.RODict({
        "ID": 25,
        "upgradeExp": 282150,
        "juYingGeLv": 3
    }),
    26: _tools.RODict({
        "ID": 26,
        "upgradeExp": 307800,
        "juYingGeLv": 3
    }),
    27: _tools.RODict({
        "ID": 27,
        "upgradeExp": 333450,
        "juYingGeLv": 4
    }),
    28: _tools.RODict({
        "ID": 28,
        "upgradeExp": 359100,
        "juYingGeLv": 4
    }),
    29: _tools.RODict({
        "ID": 29,
        "upgradeExp": 470250,
        "juYingGeLv": 4
    }),
    30: _tools.RODict({
        "ID": 30,
        "upgradeExp": 512050,
        "juYingGeLv": 4
    }),
    31: _tools.RODict({
        "ID": 31,
        "upgradeExp": 553850,
        "juYingGeLv": 4
    }),
    32: _tools.RODict({
        "ID": 32,
        "upgradeExp": 595650,
        "juYingGeLv": 4
    }),
    33: _tools.RODict({
        "ID": 33,
        "upgradeExp": 637450,
        "juYingGeLv": 4
    }),
    34: _tools.RODict({
        "ID": 34,
        "upgradeExp": 679250,
        "juYingGeLv": 4
    }),
    35: _tools.RODict({
        "ID": 35,
        "upgradeExp": 721050,
        "juYingGeLv": 5
    }),
    36: _tools.RODict({
        "ID": 36,
        "upgradeExp": 762850,
        "juYingGeLv": 5
    }),
    37: _tools.RODict({
        "ID": 37,
        "upgradeExp": 804650,
        "juYingGeLv": 5
    }),
    38: _tools.RODict({
        "ID": 38,
        "upgradeExp": 846450,
        "juYingGeLv": 5
    }),
    39: _tools.RODict({
        "ID": 39,
        "upgradeExp": 1049750,
        "juYingGeLv": 5
    }),
    40: _tools.RODict({
        "ID": 40,
        "upgradeExp": 1253050,
        "juYingGeLv": 5
    })
})
minKey = 1
maxKey = 40