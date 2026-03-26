# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: creep/timedRefresh
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
        "initialRefresh": _tools.ROList([[[0], [20], [], [], [], []]]),
        "refreshInterval": 360,
        "EndRefresh": None,
        "RefreshType": 1
    }),
    2: _tools.RODict({
        "ID": 2,
        "initialRefresh": _tools.ROList([[[0], [0], [], [], [], []]]),
        "refreshInterval": 60,
        "EndRefresh": None,
        "RefreshType": 1
    }),
    3: _tools.RODict({
        "ID": 3,
        "initialRefresh": _tools.ROList([[[0], [16], [], [], [], []]]),
        "refreshInterval": -1,
        "EndRefresh": _tools.ROList([[[0], [2], [], [], [], []]]),
        "RefreshType": 2
    }),
    4: _tools.RODict({
        "ID": 4,
        "initialRefresh": _tools.ROList([[[0], [0], [], [], [], []]]),
        "refreshInterval": 60,
        "EndRefresh": None,
        "RefreshType": 1
    }),
    5: _tools.RODict({
        "ID": 5,
        "initialRefresh": _tools.ROList([[[0], [0], [], [], [], []]]),
        "refreshInterval": 90,
        "EndRefresh": None,
        "RefreshType": 1
    }),
    6: _tools.RODict({
        "ID": 6,
        "initialRefresh": _tools.ROList([[[0], [0], [], [], [], []]]),
        "refreshInterval": 120,
        "EndRefresh": None,
        "RefreshType": 1
    })
})
minKey = 1
maxKey = 6