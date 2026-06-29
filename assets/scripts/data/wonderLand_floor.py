# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: wonderLand/floor
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
        "ID": 5100,
        "needScore": 10000,
        "needLv": 23,
    }),
    2: _tools.RODict({
        "floor": 2,
        "ID": 5101,
        "needScore": 20000,
        "needLv": 35,
    }),
    3: _tools.RODict({
        "floor": 3,
        "ID": 5102,
        "needScore": 30000,
        "needLv": 45,
    }),
    4: _tools.RODict({
        "floor": 4,
        "ID": 5103,
        "needScore": 45000,
        "needLv": 55,
    })
})
minKey = 1
maxKey = 4

id2floor = _tools.RODict({
    5100: 1,
    5101: 2,
    5102: 3,
    5103: 4,
})