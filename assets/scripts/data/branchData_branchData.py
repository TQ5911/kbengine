# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: branchData/branchData
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    1001: _tools.RODict({
        "ID": 1001,
        "name": "新元城",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1002: _tools.RODict({
        "ID": 1002,
        "name": "同心谷",
        "subType": 1,
        "num": 2,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1003: _tools.RODict({
        "ID": 1003,
        "name": "占坑大世界场景",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1004: _tools.RODict({
        "ID": 1004,
        "name": "飞沙要塞",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1005: _tools.RODict({
        "ID": 1005,
        "name": "精灵之村",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1006: _tools.RODict({
        "ID": 1006,
        "name": "精灵宝殿",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1010: _tools.RODict({
        "ID": 1010,
        "name": "石窟走廊",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1011: _tools.RODict({
        "ID": 1011,
        "name": "新元城郊",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1020: _tools.RODict({
        "ID": 1020,
        "name": "祖珂地堡一层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1021: _tools.RODict({
        "ID": 1021,
        "name": "祖珂地堡二层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1024: _tools.RODict({
        "ID": 1024,
        "name": "祖珂地堡三层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1027: _tools.RODict({
        "ID": 1027,
        "name": "祖珂地堡四层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1028: _tools.RODict({
        "ID": 1028,
        "name": "祖珂地堡五层",
        "subType": 2,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1026: _tools.RODict({
        "ID": 1026,
        "name": "祖珂地堡六层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1030: _tools.RODict({
        "ID": 1030,
        "name": "月光海港一层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1031: _tools.RODict({
        "ID": 1031,
        "name": "月光海港二层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1032: _tools.RODict({
        "ID": 1032,
        "name": "月光海港三层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1035: _tools.RODict({
        "ID": 1035,
        "name": "月光海港四层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1036: _tools.RODict({
        "ID": 1036,
        "name": "月光海港五层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1101: _tools.RODict({
        "ID": 1101,
        "name": "杜格教廷一层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1102: _tools.RODict({
        "ID": 1102,
        "name": "杜格教廷二层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1103: _tools.RODict({
        "ID": 1103,
        "name": "杜格教廷三层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1110: _tools.RODict({
        "ID": 1110,
        "name": "流沙故城一层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1111: _tools.RODict({
        "ID": 1111,
        "name": "流沙故城二层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1112: _tools.RODict({
        "ID": 1112,
        "name": "流沙故城三层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1120: _tools.RODict({
        "ID": 1120,
        "name": "五毒石窟一层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1121: _tools.RODict({
        "ID": 1121,
        "name": "五毒石窟二层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1123: _tools.RODict({
        "ID": 1123,
        "name": "五毒石窟三层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1124: _tools.RODict({
        "ID": 1124,
        "name": "五毒石窟四层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1125: _tools.RODict({
        "ID": 1125,
        "name": "五毒石窟五层",
        "subType": 2,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1126: _tools.RODict({
        "ID": 1126,
        "name": "五毒石窟六层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1901: _tools.RODict({
        "ID": 1901,
        "name": "石窟走廊(精英）",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1902: _tools.RODict({
        "ID": 1902,
        "name": "新元城郊(精英）",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1903: _tools.RODict({
        "ID": 1903,
        "name": "月光海港一层(精英）",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1904: _tools.RODict({
        "ID": 1904,
        "name": "月光海港二层(精英）",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1905: _tools.RODict({
        "ID": 1905,
        "name": "月光海港三层(精英）",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1906: _tools.RODict({
        "ID": 1906,
        "name": "月光海港四层(精英）",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1907: _tools.RODict({
        "ID": 1907,
        "name": "祖珂地堡一层(精英）",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1908: _tools.RODict({
        "ID": 1908,
        "name": "祖珂地堡二层(精英）",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1909: _tools.RODict({
        "ID": 1909,
        "name": "祖珂地堡三层(精英）",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1910: _tools.RODict({
        "ID": 1910,
        "name": "祖珂地堡四层(精英）",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1911: _tools.RODict({
        "ID": 1911,
        "name": "祖珂地堡五层(精英）",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1912: _tools.RODict({
        "ID": 1912,
        "name": "五毒石窟一层(精英）",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1913: _tools.RODict({
        "ID": 1913,
        "name": "五毒石窟二层(精英）",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1914: _tools.RODict({
        "ID": 1914,
        "name": "五毒石窟三层(精英）",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1915: _tools.RODict({
        "ID": 1915,
        "name": "五毒石窟四层(精英）",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    1916: _tools.RODict({
        "ID": 1916,
        "name": "五毒石窟五层(精英）",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    7000: _tools.RODict({
        "ID": 7000,
        "name": "演武场",
        "subType": 2,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    3100: _tools.RODict({
        "ID": 3100,
        "name": "回廊大厅",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    }),
    3101: _tools.RODict({
        "ID": 3101,
        "name": "回廊一层-修行Ⅰ",
        "subType": 1,
        "num": 1,
        "N1": 200,
        "N2": 180,
        "N3": 170,
        "AddRequired": 50,
        "MergeRequired": 20
    }),
    3102: _tools.RODict({
        "ID": 3102,
        "name": "回廊一层-修行Ⅱ",
        "subType": 1,
        "num": 1,
        "N1": 200,
        "N2": 180,
        "N3": 170,
        "AddRequired": 50,
        "MergeRequired": 20
    }),
    3103: _tools.RODict({
        "ID": 3103,
        "name": "回廊一层-历战Ⅰ",
        "subType": 1,
        "num": 1,
        "N1": 200,
        "N2": 180,
        "N3": 170,
        "AddRequired": 50,
        "MergeRequired": 20
    }),
    3104: _tools.RODict({
        "ID": 3104,
        "name": "回廊一层-历战Ⅱ",
        "subType": 1,
        "num": 1,
        "N1": 200,
        "N2": 180,
        "N3": 170,
        "AddRequired": 50,
        "MergeRequired": 20
    }),
    3105: _tools.RODict({
        "ID": 3105,
        "name": "回廊一层-历战Ⅲ",
        "subType": 1,
        "num": 1,
        "N1": 200,
        "N2": 180,
        "N3": 170,
        "AddRequired": 50,
        "MergeRequired": 20
    }),
    3110: _tools.RODict({
        "ID": 3110,
        "name": "回廊一层-俸禄Ⅰ",
        "subType": 1,
        "num": 1,
        "N1": 200,
        "N2": 180,
        "N3": 170,
        "AddRequired": 50,
        "MergeRequired": 20
    }),
    3111: _tools.RODict({
        "ID": 3111,
        "name": "回廊一层-俸禄Ⅱ",
        "subType": 1,
        "num": 1,
        "N1": 200,
        "N2": 180,
        "N3": 170,
        "AddRequired": 50,
        "MergeRequired": 20
    }),
    3112: _tools.RODict({
        "ID": 3112,
        "name": "回廊一层-赏金Ⅰ",
        "subType": 1,
        "num": 1,
        "N1": 200,
        "N2": 180,
        "N3": 170,
        "AddRequired": 50,
        "MergeRequired": 20
    }),
    3113: _tools.RODict({
        "ID": 3113,
        "name": "回廊一层-赏金Ⅱ",
        "subType": 1,
        "num": 1,
        "N1": 200,
        "N2": 180,
        "N3": 170,
        "AddRequired": 50,
        "MergeRequired": 20
    }),
    3114: _tools.RODict({
        "ID": 3114,
        "name": "回廊一层-赏金Ⅲ",
        "subType": 1,
        "num": 1,
        "N1": 200,
        "N2": 180,
        "N3": 170,
        "AddRequired": 50,
        "MergeRequired": 20
    }),
    3116: _tools.RODict({
        "ID": 3116,
        "name": "回廊一层-擂台",
        "subType": 1,
        "num": 1,
        "N1": 200,
        "N2": 180,
        "N3": 170,
        "AddRequired": 50,
        "MergeRequired": 20
    }),
    3118: _tools.RODict({
        "ID": 3118,
        "name": "回廊一层-锻体",
        "subType": 1,
        "num": 1,
        "N1": 200,
        "N2": 180,
        "N3": 170,
        "AddRequired": 50,
        "MergeRequired": 20
    }),
    3119: _tools.RODict({
        "ID": 3119,
        "name": "回廊一层-遗器",
        "subType": 1,
        "num": 1,
        "N1": 200,
        "N2": 180,
        "N3": 170,
        "AddRequired": 50,
        "MergeRequired": 20
    }),
    3120: _tools.RODict({
        "ID": 3120,
        "name": "回廊一层-狂潮",
        "subType": 1,
        "num": 1,
        "N1": 200,
        "N2": 180,
        "N3": 170,
        "AddRequired": 50,
        "MergeRequired": 20
    }),
    3121: _tools.RODict({
        "ID": 3121,
        "name": "回廊一层-混沌之境",
        "subType": 1,
        "num": 1,
        "N1": 200,
        "N2": 180,
        "N3": 170,
        "AddRequired": 50,
        "MergeRequired": 20
    }),
    3124: _tools.RODict({
        "ID": 3124,
        "name": "回廊一层-心魔试炼",
        "subType": 1,
        "num": 1,
        "N1": 200,
        "N2": 180,
        "N3": 170,
        "AddRequired": 50,
        "MergeRequired": 20
    }),
    5100: _tools.RODict({
        "ID": 5100,
        "name": "天劫崖一层",
        "subType": 1,
        "num": 1,
        "N1": 200,
        "N2": 180,
        "N3": 170,
        "AddRequired": 100,
        "MergeRequired": 50
    }),
    5201: _tools.RODict({
        "ID": 5201,
        "name": "归墟一层",
        "subType": 1,
        "num": 1,
        "N1": 200,
        "N2": 180,
        "N3": 170,
        "AddRequired": 100,
        "MergeRequired": 50
    }),
    9000: _tools.RODict({
        "ID": 9000,
        "name": "等待之境",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 200,
        "MergeRequired": 100
    })
})
minKey = 1001
maxKey = 9000