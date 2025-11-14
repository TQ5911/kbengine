# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: creep/countRefresh
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
        "mapID": 3103,
        "combatAreaID": 31038004,
        "refreshMonsterID": _tools.ROList([31030088]),
        "countLimit": 33,
        "countMonsterID": _tools.ROList([11011004, 11011005, 11011006]),
        "countResetTime": 60
    }),
    2: _tools.RODict({
        "ID": 2,
        "mapID": 3103,
        "combatAreaID": 31038005,
        "refreshMonsterID": _tools.ROList([31030129]),
        "countLimit": 33,
        "countMonsterID": _tools.ROList([11011004, 11011005, 11011006]),
        "countResetTime": 60
    }),
    3: _tools.RODict({
        "ID": 3,
        "mapID": 3103,
        "combatAreaID": 31038006,
        "refreshMonsterID": _tools.ROList([31030170]),
        "countLimit": 33,
        "countMonsterID": _tools.ROList([11011004, 11011005, 11011006]),
        "countResetTime": 60
    })
})
minKey = 1
maxKey = 3

refreshMonsterIDIndex = {310331030088: 1, 310331030129: 2, 310331030170: 3}


mapIDIndex = {3103: [1, 2, 3]}
