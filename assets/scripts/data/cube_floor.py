# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: cube/floor
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    1: _tools.RODict({
        "floor": 1,
        "ID": 3100,
        "needScore": 5000,
        "cowPassBuffID": 64000107,
        "defenderBuff": _tools.ROList([(0, 64000120), (5, 64000121), (10, 64000122)]),
        "challengerBuff": 64000117
    }),
    2: _tools.RODict({
        "floor": 2,
        "ID": 3200,
        "needScore": 20000,
        "cowPassBuffID": 64000108,
        "defenderBuff": _tools.ROList([(0, 64000123), (5, 64000124), (10, 64000125)]),
        "challengerBuff": 64000118
    }),
    3: _tools.RODict({
        "floor": 3,
        "ID": 3300,
        "needScore": 34000,
        "cowPassBuffID": 64000109,
        "defenderBuff": _tools.ROList([(0, 64000127), (5, 64000128), (10, 64000129)]),
        "challengerBuff": 64000119
    })
})
minKey = 1
maxKey = 3