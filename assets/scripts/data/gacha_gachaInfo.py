# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: gacha/gachaInfo
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    10101: _tools.RODict({
        "ID": 10101,
        "title": "<color=#967100>传说品质精灵</color><color=#9e9886>召唤获得概率2%</color>",
        "percentage": "召唤获得概率2%",
        "petList": (15000030, 15000031, 15000032, 15000033)
    }),
    10102: _tools.RODict({
        "ID": 10102,
        "title": "<color=#763e9b>史诗品质精灵</color><color=#9e9886>召唤获得概率4%</color>",
        "percentage": "召唤获得概率4%",
        "petList": (15000021, 15000022, 15000023, 15000024, 15000025, 15000026, 15000027, 15000028)
    }),
    10103: _tools.RODict({
        "ID": 10103,
        "title": "<color=#2f6caf>精良品质精灵</color><color=#9e9886>召唤获得概率24%</color>",
        "percentage": "召唤获得概率24%",
        "petList": (15000011, 15000012, 15000013, 15000014, 15000015, 15000016, 15000017, 15000018, 15000019, 15000020)
    }),
    10104: _tools.RODict({
        "ID": 10104,
        "title": "<color=#266914>优秀品质精灵</color><color=#9e9886>召唤获得概率70%</color>",
        "percentage": "召唤获得概率70%",
        "petList": (15000001, 15000002, 15000003, 15000004, 15000005, 15000006, 15000007, 15000008, 15000009, 15000010)
    }),
    10201: _tools.RODict({
        "ID": 10201,
        "title": "<color=#967100>传说品质精灵</color><color=#9e9886>召唤获得概率2%</color>",
        "percentage": "召唤获得概率2%",
        "petList": (15000030, 15000031, 15000032, 15000033)
    }),
    10202: _tools.RODict({
        "ID": 10202,
        "title": "<color=#763e9b>史诗品质精灵</color><color=#9e9886>召唤获得概率4%</color>",
        "percentage": "召唤获得概率4%",
        "petList": (15000021, 15000022, 15000023, 15000024, 15000025, 15000026, 15000027, 15000028)
    }),
    10203: _tools.RODict({
        "ID": 10203,
        "title": "<color=#2f6caf>精良品质精灵</color><color=#9e9886>召唤获得概率24%</color>",
        "percentage": "召唤获得概率24%",
        "petList": (15000011, 15000012, 15000013, 15000014, 15000015, 15000016, 15000017, 15000018, 15000019, 15000020)
    }),
    10204: _tools.RODict({
        "ID": 10204,
        "title": "<color=#266914>优秀品质精灵</color><color=#9e9886>召唤获得概率70%</color>",
        "percentage": "召唤获得概率70%",
        "petList": (15000001, 15000002, 15000003, 15000004, 15000005, 15000006, 15000007, 15000008, 15000009, 15000010)
    })
})
minKey = 10101
maxKey = 10204