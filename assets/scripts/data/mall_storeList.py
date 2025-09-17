# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: mall/storeList
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
        "name": "药铺",
        "isTimeLimit": 0,
        "openTime": None,
        "closeTime": None,
        "goodsList": (111, 1, 2, 3, 4, 5, 6, 39, 40),
        "groupId": (1, 2),
        "numberWeight": ((5000, 3000, 2000), (5000, 3000, 2000)),
        "groupRefreshTime": 4,
    }),
    2: _tools.RODict({
        "ID": 2,
        "name": "杂货铺",
        "isTimeLimit": 0,
        "openTime": None,
        "closeTime": None,
        "goodsList": (91, 41, 42, 43, 44, 48, 49, 45, 46, 47, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 50, 51, 38),
        "groupId": None,
        "numberWeight": None,
        "groupRefreshTime": 0,
    }),
    3: _tools.RODict({
        "ID": 3,
        "name": "秘境商店",
        "isTimeLimit": 1,
        "openTime": _tools.ROList([[[0], [0], [5], [11], [], [2022]]]),
        "closeTime": _tools.ROList([[[0], [0], [7], [7], [], [2099]]]),
        "goodsList": (16, 17, 18, 19),
        "groupId": None,
        "numberWeight": None,
        "groupRefreshTime": 0,
    }),
    4: _tools.RODict({
        "ID": 4,
        "name": "帮会商店",
        "isTimeLimit": 0,
        "openTime": None,
        "closeTime": None,
        "goodsList": (62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90),
        "groupId": None,
        "numberWeight": None,
        "groupRefreshTime": 0,
    }),
    5: _tools.RODict({
        "ID": 5,
        "name": "铁匠铺",
        "isTimeLimit": 0,
        "openTime": None,
        "closeTime": None,
        "goodsList": (28, 29, 30, 31, 32, 33),
        "groupId": None,
        "numberWeight": None,
        "groupRefreshTime": 0,
    }),
    6: _tools.RODict({
        "ID": 6,
        "name": "交易盒兑换",
        "isTimeLimit": 0,
        "openTime": None,
        "closeTime": None,
        "goodsList": (92, 93),
        "groupId": None,
        "numberWeight": None,
        "groupRefreshTime": 0,
    }),
    7: _tools.RODict({
        "ID": 7,
        "name": "服装店",
        "isTimeLimit": 0,
        "openTime": None,
        "closeTime": None,
        "goodsList": (97, 98, 99, 100, 101, 102, 103, 104, 105),
        "groupId": None,
        "numberWeight": None,
        "groupRefreshTime": 0,
    }),
    8: _tools.RODict({
        "ID": 8,
        "name": "首饰店",
        "isTimeLimit": 0,
        "openTime": None,
        "closeTime": None,
        "goodsList": (106, 107, 108, 109, 110),
        "groupId": None,
        "numberWeight": None,
        "groupRefreshTime": 0,
    }),
    9: _tools.RODict({
        "ID": 9,
        "name": "武器店",
        "isTimeLimit": 0,
        "openTime": None,
        "closeTime": None,
        "goodsList": (94, 95, 96),
        "groupId": None,
        "numberWeight": None,
        "groupRefreshTime": 0,
    }),
    10: _tools.RODict({
        "ID": 10,
        "name": "测试-兑换类型1",
        "isTimeLimit": 0,
        "openTime": None,
        "closeTime": None,
        "goodsList": (112, 113, 114, 115, 116, 117),
        "groupId": None,
        "numberWeight": None,
        "groupRefreshTime": 0,
    }),
    11: _tools.RODict({
        "ID": 11,
        "name": "测试-兑换类型2",
        "isTimeLimit": 0,
        "openTime": None,
        "closeTime": None,
        "goodsList": (118, 119, 120, 121, 122, 123),
        "groupId": None,
        "numberWeight": None,
        "groupRefreshTime": 0,
    })
})
minKey = 1
maxKey = 11