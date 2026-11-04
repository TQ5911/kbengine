# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: abyss/floor
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
        "ID": 5201,
        "needScore": 35000,
        "needLv": 45,
        "serverLv": 40,
    }),
    2: _tools.RODict({
        "floor": 2,
        "ID": 5202,
        "needScore": 40000,
        "needLv": 50,
        "serverLv": 45,
    }),
    3: _tools.RODict({
        "floor": 3,
        "ID": 5203,
        "needScore": 47500,
        "needLv": 55,
        "serverLv": 50,
    }),
    4: _tools.RODict({
        "floor": 4,
        "ID": 5204,
        "needScore": 55000,
        "needLv": 60,
        "serverLv": 55,
    })
})
minKey = 1
maxKey = 4

id2floor = _tools.RODict({
    5201: 1,
    5202: 2,
    5203: 3,
    5204: 4,
})