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
        "name": "同心村",
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
        "name": "占坑场景",
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
        "name": "精灵村外",
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
    1022: _tools.RODict({
        "ID": 1022,
        "name": "祖珂地堡六层",
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
    1026: _tools.RODict({
        "ID": 1026,
        "name": "祖珂地堡七层",
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
        "name": "月光海港六层",
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
        "name": "月光海港七层",
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
        "name": "猪洞一层",
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
        "name": "猪洞二层",
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
        "name": "猪洞三层",
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
        "name": "蜈蚣洞一层",
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
        "name": "蜈蚣洞二层",
        "subType": 1,
        "num": 1,
        "N1": 400,
        "N2": 380,
        "N3": 370,
        "AddRequired": 350,
        "MergeRequired": 200
    }),
    1122: _tools.RODict({
        "ID": 1122,
        "name": "蜈蚣洞三层",
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
        "name": "五毒石窟四层",
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