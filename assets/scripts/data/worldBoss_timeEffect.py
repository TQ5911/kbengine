# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: worldBoss/timeEffect
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
        "startTimeCron": _tools.ROList([[[0], [2], [], [], [], []]]),
        "endTimeCron": _tools.ROList([[[0], [8], [], [], [], []]]),
        "chestSpawnRate": 0.5,
        "lightSpawnRate": 0.5
    }),
    2: _tools.RODict({
        "ID": 2,
        "startTimeCron": _tools.ROList([[[0], [8], [], [], [], []]]),
        "endTimeCron": _tools.ROList([[[0], [14], [], [], [], []]]),
        "chestSpawnRate": 0.5,
        "lightSpawnRate": 0.5
    }),
    3: _tools.RODict({
        "ID": 3,
        "startTimeCron": _tools.ROList([[[0], [14], [], [], [], []]]),
        "endTimeCron": _tools.ROList([[[0], [20], [], [], [], []]]),
        "chestSpawnRate": 0.7,
        "lightSpawnRate": 0.7
    }),
    4: _tools.RODict({
        "ID": 4,
        "startTimeCron": _tools.ROList([[[0], [20], [], [], [], []]]),
        "endTimeCron": _tools.ROList([[[0], [2], [], [], [], []]]),
        "chestSpawnRate": 1.0,
        "lightSpawnRate": 1.0
    })
})
minKey = 1
maxKey = 4