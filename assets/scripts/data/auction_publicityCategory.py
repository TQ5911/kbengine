# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: auction/publicityCategory
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    99: _tools.RODict({
        "ID": 99,
        "qualityAbove": None,
        "soulQualityAbove": None,
        "itemQualityAbove": None,
        "itemList": None
    }),
    1: _tools.RODict({
        "ID": 1,
        "qualityAbove": None,
        "soulQualityAbove": None,
        "itemQualityAbove": None,
        "itemList": None
    }),
    2: _tools.RODict({
        "ID": 2,
        "qualityAbove": (1, 2),
        "soulQualityAbove": None,
        "itemQualityAbove": None,
        "itemList": None
    }),
    3: _tools.RODict({
        "ID": 3,
        "qualityAbove": None,
        "soulQualityAbove": None,
        "itemQualityAbove": None,
        "itemList": None
    }),
    301: _tools.RODict({
        "ID": 301,
        "qualityAbove": (2, 2),
        "soulQualityAbove": None,
        "itemQualityAbove": None,
        "itemList": None
    }),
    302: _tools.RODict({
        "ID": 302,
        "qualityAbove": (3, 2),
        "soulQualityAbove": None,
        "itemQualityAbove": None,
        "itemList": None
    }),
    303: _tools.RODict({
        "ID": 303,
        "qualityAbove": (4, 2),
        "soulQualityAbove": None,
        "itemQualityAbove": None,
        "itemList": None
    }),
    304: _tools.RODict({
        "ID": 304,
        "qualityAbove": (8, 2),
        "soulQualityAbove": None,
        "itemQualityAbove": None,
        "itemList": None
    }),
    4: _tools.RODict({
        "ID": 4,
        "qualityAbove": None,
        "soulQualityAbove": None,
        "itemQualityAbove": None,
        "itemList": None
    }),
    401: _tools.RODict({
        "ID": 401,
        "qualityAbove": (5, 2),
        "soulQualityAbove": None,
        "itemQualityAbove": None,
        "itemList": None
    }),
    402: _tools.RODict({
        "ID": 402,
        "qualityAbove": (6, 2),
        "soulQualityAbove": None,
        "itemQualityAbove": None,
        "itemList": None
    }),
    403: _tools.RODict({
        "ID": 403,
        "qualityAbove": (7, 2),
        "soulQualityAbove": None,
        "itemQualityAbove": None,
        "itemList": None
    }),
    5: _tools.RODict({
        "ID": 5,
        "qualityAbove": None,
        "soulQualityAbove": None,
        "itemQualityAbove": (0, 11, 2),
        "itemList": None
    }),
    6: _tools.RODict({
        "ID": 6,
        "qualityAbove": None,
        "soulQualityAbove": None,
        "itemQualityAbove": None,
        "itemList": (30000220, 30000224, 30000225, 30000226, 30000231)
    }),
    7: _tools.RODict({
        "ID": 7,
        "qualityAbove": None,
        "soulQualityAbove": None,
        "itemQualityAbove": None,
        "itemList": (30990128, 30990129, 30990130, 30990131, 30990135, 30990136, 30990137, 30990138, 30990142, 30990143, 30990144, 30990145)
    }),
    8: _tools.RODict({
        "ID": 8,
        "qualityAbove": None,
        "soulQualityAbove": None,
        "itemQualityAbove": (0, 20, 3),
        "itemList": None
    }),
    9: _tools.RODict({
        "ID": 9,
        "qualityAbove": None,
        "soulQualityAbove": None,
        "itemQualityAbove": (1, 1, 3),
        "itemList": None
    }),
    10: _tools.RODict({
        "ID": 10,
        "qualityAbove": None,
        "soulQualityAbove": None,
        "itemQualityAbove": None,
        "itemList": None
    }),
    1001: _tools.RODict({
        "ID": 1001,
        "qualityAbove": None,
        "soulQualityAbove": (1, 1),
        "itemQualityAbove": None,
        "itemList": None
    }),
    1002: _tools.RODict({
        "ID": 1002,
        "qualityAbove": None,
        "soulQualityAbove": (2, 1),
        "itemQualityAbove": None,
        "itemList": None
    }),
    1003: _tools.RODict({
        "ID": 1003,
        "qualityAbove": None,
        "soulQualityAbove": (3, 1),
        "itemQualityAbove": None,
        "itemList": None
    }),
    1004: _tools.RODict({
        "ID": 1004,
        "qualityAbove": None,
        "soulQualityAbove": (4, 1),
        "itemQualityAbove": None,
        "itemList": None
    }),
    1005: _tools.RODict({
        "ID": 1005,
        "qualityAbove": None,
        "soulQualityAbove": (5, 1),
        "itemQualityAbove": None,
        "itemList": None
    }),
    1006: _tools.RODict({
        "ID": 1006,
        "qualityAbove": None,
        "soulQualityAbove": (6, 1),
        "itemQualityAbove": None,
        "itemList": None
    }),
    1007: _tools.RODict({
        "ID": 1007,
        "qualityAbove": None,
        "soulQualityAbove": (7, 1),
        "itemQualityAbove": None,
        "itemList": None
    }),
    1008: _tools.RODict({
        "ID": 1008,
        "qualityAbove": None,
        "soulQualityAbove": (8, 1),
        "itemQualityAbove": None,
        "itemList": None
    })
})
minKey = 1
maxKey = 1008

itemDataDic = {30000220: True, 30000224: True, 30000225: True, 30000226: True, 30000231: True, 30990128: True, 30990129: True, 30990130: True, 30990131: True, 30990135: True, 30990136: True, 30990137: True, 30990138: True, 30990142: True, 30990143: True, 30990144: True, 30990145: True}


itemQualityDataDic = {'0_11': 2, '0_20': 3, '1_1': 3}


equipQualityDataDic = {1: 2, 2: 2, 3: 2, 4: 2, 8: 2, 5: 2, 6: 2, 7: 2}
