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
        "needScore": 8000,
        "cowPassBuffID": 64000107,
        "defenderBuff": _tools.ROList([(0, 64000107), (5, 64000108)]),
        "challengerBuff": 64000109,
        "chapmanID": 18000738,
        "position": _tools.ROList([(3111, 180.6146, 527.7224, 109.7814, -88.299), (3121, -26.67728, 0, 50.70382, 167.021)])
    }),
    2: _tools.RODict({
        "floor": 2,
        "ID": 3200,
        "needScore": 24000,
        "cowPassBuffID": 64000108,
        "defenderBuff": _tools.ROList([(0, 64000108), (5, 64000109)]),
        "challengerBuff": 64000107,
        "chapmanID": 18000739,
        "position": _tools.ROList([(3211, 180.6146, 527.7224, 109.7814, -88.299), (3221, -26.67728, 0, 50.70382, 167.021)])
    }),
    3: _tools.RODict({
        "floor": 3,
        "ID": 3300,
        "needScore": 36000,
        "cowPassBuffID": 64000109,
        "defenderBuff": _tools.ROList([(0, 64000109), (5, 64000110)]),
        "challengerBuff": 64000108,
        "chapmanID": 18000740,
        "position": _tools.ROList([(3311, 180.6146, 527.7224, 109.7814, -88.299), (3321, -26.67728, 0, 50.70382, 167.021)])
    })
})
minKey = 1
maxKey = 3