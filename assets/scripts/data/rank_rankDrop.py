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
        "rankRange": _tools.ROList([1, 1]),
        "bindWeightRank": 9000,
        "isMonthCard": 1,
        "isCrossServer": 1,
        "bigBindWeightRank": 500
    }),
    2: _tools.RODict({
        "id": 2,
        "rankID": 2,
        "rankRange": _tools.ROList([2, 2]),
        "bindWeightRank": 7000,
        "isMonthCard": 1,
        "isCrossServer": 1,
        "bigBindWeightRank": 500
    }),
    3: _tools.RODict({
        "id": 3,
        "rankID": 2,
        "rankRange": _tools.ROList([3, 3]),
        "bindWeightRank": 6000,
        "isMonthCard": 1,
        "isCrossServer": 1,
        "bigBindWeightRank": 500
    }),
    4: _tools.RODict({
        "id": 4,
        "rankID": 2,
        "rankRange": _tools.ROList([4, 10]),
        "bindWeightRank": 5000,
        "isMonthCard": 1,
        "isCrossServer": 1,
        "bigBindWeightRank": 500
    }),
    5: _tools.RODict({
        "id": 5,
        "rankID": 2,
        "rankRange": _tools.ROList([11, 50]),
        "bindWeightRank": 4500,
        "isMonthCard": 1,
        "isCrossServer": 1,
        "bigBindWeightRank": 500
    }),
    6: _tools.RODict({
        "id": 6,
        "rankID": 2,
        "rankRange": _tools.ROList([51, 100]),
        "bindWeightRank": 4000,
        "isMonthCard": 1,
        "isCrossServer": 1,
        "bigBindWeightRank": 500
    }),
    7: _tools.RODict({
        "id": 7,
        "rankID": 2,
        "rankRange": _tools.ROList([101, 200]),
        "bindWeightRank": 3500,
        "isMonthCard": 1,
        "isCrossServer": 1,
        "bigBindWeightRank": 500
    }),
    8: _tools.RODict({
        "id": 8,
        "rankID": 2,
        "rankRange": _tools.ROList([201, 500]),
        "bindWeightRank": 3000,
        "isMonthCard": 1,
        "isCrossServer": 1,
        "bigBindWeightRank": 500
    }),
    9: _tools.RODict({
        "id": 9,
        "rankID": 2,
        "rankRange": _tools.ROList([501, 1000]),
        "bindWeightRank": 2500,
        "isMonthCard": 1,
        "isCrossServer": 1,
        "bigBindWeightRank": 500
    }),
    10: _tools.RODict({
        "id": 10,
        "rankID": 2,
        "rankRange": _tools.ROList([1001, 2000]),
        "bindWeightRank": 1500,
        "isMonthCard": 1,
        "isCrossServer": 0,
        "bigBindWeightRank": 500
    }),
    11: _tools.RODict({
        "id": 11,
        "rankID": 2,
        "rankRange": _tools.ROList([2001, 3000]),
        "bindWeightRank": 500,
        "isMonthCard": 1,
        "isCrossServer": 0,
        "bigBindWeightRank": 500
    })
})
minKey = 1
maxKey = 11