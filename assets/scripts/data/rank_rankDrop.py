# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: rank/rankDrop
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    1: _tools.RODict({
        "id": 1,
        "rankID": 2,
        "rankRange": _tools.ROList([1, 3]),
        "bindWeightRank": 2000
    }),
    2: _tools.RODict({
        "id": 2,
        "rankID": 2,
        "rankRange": _tools.ROList([4, 10]),
        "bindWeightRank": 1500
    }),
    3: _tools.RODict({
        "id": 3,
        "rankID": 2,
        "rankRange": _tools.ROList([11, 30]),
        "bindWeightRank": 1000
    }),
    4: _tools.RODict({
        "id": 4,
        "rankID": 2,
        "rankRange": _tools.ROList([31, 100]),
        "bindWeightRank": 500
    })
})
minKey = 1
maxKey = 4