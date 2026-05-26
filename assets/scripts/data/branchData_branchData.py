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
        "num": 2,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    1002: _tools.RODict({
        "ID": 1002,
        "name": "同心谷",
        "subType": 1,
        "num": 2,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    1003: _tools.RODict({
        "ID": 1003,
        "name": "占坑大世界场景",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    1004: _tools.RODict({
        "ID": 1004,
        "name": "飞沙要塞",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    1005: _tools.RODict({
        "ID": 1005,
        "name": "精灵之村",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    1006: _tools.RODict({
        "ID": 1006,
        "name": "精灵宝殿",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    1010: _tools.RODict({
        "ID": 1010,
        "name": "石窟走廊",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    1011: _tools.RODict({
        "ID": 1011,
        "name": "新元城郊",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    1020: _tools.RODict({
        "ID": 1020,
        "name": "祖珂地堡一层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    1021: _tools.RODict({
        "ID": 1021,
        "name": "祖珂地堡二层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    1024: _tools.RODict({
        "ID": 1024,
        "name": "祖珂地堡三层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    1027: _tools.RODict({
        "ID": 1027,
        "name": "祖珂地堡四层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    1028: _tools.RODict({
        "ID": 1028,
        "name": "祖珂地堡五层",
        "subType": 2,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    1026: _tools.RODict({
        "ID": 1026,
        "name": "祖珂地堡六层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    1030: _tools.RODict({
        "ID": 1030,
        "name": "月光海港一层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    1031: _tools.RODict({
        "ID": 1031,
        "name": "月光海港二层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    1032: _tools.RODict({
        "ID": 1032,
        "name": "月光海港三层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    1035: _tools.RODict({
        "ID": 1035,
        "name": "月光海港四层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    1036: _tools.RODict({
        "ID": 1036,
        "name": "月光海港五层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    1101: _tools.RODict({
        "ID": 1101,
        "name": "杜格教廷一层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    1102: _tools.RODict({
        "ID": 1102,
        "name": "杜格教廷二层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    1103: _tools.RODict({
        "ID": 1103,
        "name": "杜格教廷三层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    1110: _tools.RODict({
        "ID": 1110,
        "name": "流沙故城一层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    1111: _tools.RODict({
        "ID": 1111,
        "name": "流沙故城二层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    1112: _tools.RODict({
        "ID": 1112,
        "name": "流沙故城三层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    1120: _tools.RODict({
        "ID": 1120,
        "name": "五毒石窟一层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    1121: _tools.RODict({
        "ID": 1121,
        "name": "五毒石窟二层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    1123: _tools.RODict({
        "ID": 1123,
        "name": "五毒石窟三层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    1124: _tools.RODict({
        "ID": 1124,
        "name": "五毒石窟四层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    1125: _tools.RODict({
        "ID": 1125,
        "name": "五毒石窟五层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    1126: _tools.RODict({
        "ID": 1126,
        "name": "五毒石窟六层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    7000: _tools.RODict({
        "ID": 7000,
        "name": "演武场",
        "subType": 2,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    3100: _tools.RODict({
        "ID": 3100,
        "name": "回廊大厅",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    3101: _tools.RODict({
        "ID": 3101,
        "name": "回廊一层-修行Ⅰ",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    3102: _tools.RODict({
        "ID": 3102,
        "name": "回廊一层-修行Ⅱ",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    3103: _tools.RODict({
        "ID": 3103,
        "name": "回廊一层-历战Ⅰ",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    3104: _tools.RODict({
        "ID": 3104,
        "name": "回廊一层-历战Ⅱ",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    3105: _tools.RODict({
        "ID": 3105,
        "name": "回廊一层-历战Ⅲ",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    3106: _tools.RODict({
        "ID": 3106,
        "name": "回廊一层-魔物",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    3107: _tools.RODict({
        "ID": 3107,
        "name": "回廊一层-首领Ⅰ",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    3108: _tools.RODict({
        "ID": 3108,
        "name": "回廊一层-首领Ⅱ",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    3109: _tools.RODict({
        "ID": 3109,
        "name": "回廊一层-首领Ⅲ",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    3110: _tools.RODict({
        "ID": 3110,
        "name": "回廊一层-俸禄Ⅰ",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    3111: _tools.RODict({
        "ID": 3111,
        "name": "回廊一层-俸禄Ⅱ",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    3112: _tools.RODict({
        "ID": 3112,
        "name": "回廊一层-赏金Ⅰ",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    3113: _tools.RODict({
        "ID": 3113,
        "name": "回廊一层-赏金Ⅱ",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    3114: _tools.RODict({
        "ID": 3114,
        "name": "回廊一层-赏金Ⅲ",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    3115: _tools.RODict({
        "ID": 3115,
        "name": "回廊一层-镇守",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    3116: _tools.RODict({
        "ID": 3116,
        "name": "回廊一层-擂台",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    3117: _tools.RODict({
        "ID": 3117,
        "name": "回廊一层-封印",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    3118: _tools.RODict({
        "ID": 3118,
        "name": "回廊一层-锻体",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    3119: _tools.RODict({
        "ID": 3119,
        "name": "回廊一层-遗器",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    3120: _tools.RODict({
        "ID": 3120,
        "name": "回廊一层-狂潮",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    3121: _tools.RODict({
        "ID": 3121,
        "name": "回廊一层-混沌之境",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    3122: _tools.RODict({
        "ID": 3122,
        "name": "回廊一层-隐匿",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    3123: _tools.RODict({
        "ID": 3123,
        "name": "回廊一层-祈福",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    3124: _tools.RODict({
        "ID": 3124,
        "name": "心魔·表",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    3125: _tools.RODict({
        "ID": 3125,
        "name": "心魔·里",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    5100: _tools.RODict({
        "ID": 5100,
        "name": "天劫崖一层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    5201: _tools.RODict({
        "ID": 5201,
        "name": "归墟一层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    })
})
minKey = 1001
maxKey = 7000