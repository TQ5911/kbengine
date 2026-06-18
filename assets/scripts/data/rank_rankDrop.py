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
        "rankRange": _tools.ROList([1, 100]),
        "bindWeightRank": 1000,
        "isMonthCard": 1,
        "isCrossServer": 1,
        "bigBindWeightRank": 1000
    }),
    2: _tools.RODict({
        "id": 2,
        "rankID": 2,
        "rankRange": _tools.ROList([101, 200]),
        "bindWeightRank": 1000,
        "isMonthCard": 1,
        "isCrossServer": 1,
        "bigBindWeightRank": 1000
    }),
    3: _tools.RODict({
        "id": 3,
        "rankID": 2,
        "rankRange": _tools.ROList([201, 500]),
        "bindWeightRank": 1000,
        "isMonthCard": 1,
        "isCrossServer": 1,
        "bigBindWeightRank": 1000
    }),
    4: _tools.RODict({
        "id": 4,
        "rankID": 2,
        "rankRange": _tools.ROList([501, 1000]),
        "bindWeightRank": 1000,
        "isMonthCard": 1,
        "isCrossServer": 1,
        "bigBindWeightRank": 1000
    }),
    5: _tools.RODict({
        "id": 5,
        "rankID": 2,
        "rankRange": _tools.ROList([1001, 2000]),
        "bindWeightRank": 1000,
        "isMonthCard": 1,
        "isCrossServer": 0,
        "bigBindWeightRank": 1000
    }),
    6: _tools.RODict({
        "id": 6,
        "rankID": 2,
        "rankRange": _tools.ROList([2001, 3000]),
        "bindWeightRank": 1000,
        "isMonthCard": 1,
        "isCrossServer": 0,
        "bigBindWeightRank": 1000
    })
})
minKey = 1
maxKey = 6