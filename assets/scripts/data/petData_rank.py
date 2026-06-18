# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: petData/rank
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
        "gearNum": 1,
        "levelExp": (200, 400),
        "consumeItem": ((1, 1, 1), (1, 1, 2), (1, 1, 3), (1, 1, 4)),
    }),
    2: _tools.RODict({
        "ID": 2,
        "gearNum": 2,
        "levelExp": (1200, 2400, 4800),
        "consumeItem": ((1, 1, 1), (1, 1, 2), (1, 1, 3), (1, 1, 4)),
    }),
    3: _tools.RODict({
        "ID": 3,
        "gearNum": 3,
        "levelExp": (6000, 12000, 24000, 48000),
        "consumeItem": ((1, 1, 1), (1, 1, 2), (1, 1, 3), (1, 1, 4)),
    }),
    4: _tools.RODict({
        "ID": 4,
        "gearNum": 4,
        "levelExp": (50000, 100000, 200000, 400000),
        "consumeItem": ((1, 1, 1), (1, 1, 2), (1, 1, 3), (1, 1, 4)),
    }),
    5: _tools.RODict({
        "ID": 5,
        "gearNum": 5,
        "levelExp": (50000, 100000, 200000, 400000),
        "consumeItem": ((1, 1, 1), (1, 1, 2), (1, 1, 3), (1, 1, 4)),
    })
})
minKey = 1
maxKey = 5