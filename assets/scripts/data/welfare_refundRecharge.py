# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: welfare/refundRecharge
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
        "rechargeRange": _tools.ROList([1, 5000]),
        "goldRate": 100,
        "boundGoldRate": 30
    }),
    2: _tools.RODict({
        "ID": 2,
        "rechargeRange": _tools.ROList([5001, 50000]),
        "goldRate": 100,
        "boundGoldRate": 20
    }),
    3: _tools.RODict({
        "ID": 3,
        "rechargeRange": _tools.ROList([50001]),
        "goldRate": 100,
        "boundGoldRate": 10
    })
})
minKey = 1
maxKey = 3