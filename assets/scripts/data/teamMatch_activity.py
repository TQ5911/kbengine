# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: teamMatch/activity
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    0: _tools.RODict({
        "ID": 0,
        "value": "未设定目标",
        "pareActivity": 0,
        "minScore": 0,
        "minLevel": 0,
        "enterDunID": 0,
        "isCrossServer": 0,
    }),
    1: _tools.RODict({
        "ID": 1,
        "value": "自设目标",
        "pareActivity": 1,
        "minScore": 0,
        "minLevel": 0,
        "enterDunID": 0,
        "isCrossServer": 0,
    }),
    2: _tools.RODict({
        "ID": 2,
        "value": "新元城战",
        "pareActivity": 2,
        "minScore": 0,
        "minLevel": 0,
        "enterDunID": 0,
        "isCrossServer": 0,
    }),
    3: _tools.RODict({
        "ID": 3,
        "value": "帮会副本",
        "pareActivity": 0,
        "minScore": 0,
        "minLevel": 0,
        "enterDunID": 0,
        "isCrossServer": 0,
    }),
    101: _tools.RODict({
        "ID": 101,
        "value": "深海禁地",
        "pareActivity": 32000004,
        "minScore": 7500,
        "minLevel": 16,
        "enterDunID": 2101,
        "isCrossServer": 0,
    }),
    102: _tools.RODict({
        "ID": 102,
        "value": "祖珂祭坛",
        "pareActivity": 32000004,
        "minScore": 15000,
        "minLevel": 30,
        "enterDunID": 2102,
        "isCrossServer": 0,
    }),
    103: _tools.RODict({
        "ID": 103,
        "value": "亡者之村",
        "pareActivity": 32000004,
        "minScore": 25000,
        "minLevel": 40,
        "enterDunID": 2104,
        "isCrossServer": 0,
    }),
    104: _tools.RODict({
        "ID": 104,
        "value": "五毒石窟",
        "pareActivity": 32000004,
        "minScore": 25000,
        "minLevel": 50,
        "enterDunID": 2103,
        "isCrossServer": 0,
    }),
    151: _tools.RODict({
        "ID": 151,
        "value": "驭沙军候",
        "pareActivity": 32000001,
        "minScore": 10000,
        "minLevel": 25,
        "enterDunID": 2204,
        "isCrossServer": 0,
    }),
    152: _tools.RODict({
        "ID": 152,
        "value": "阴阳鬼判",
        "pareActivity": 32000001,
        "minScore": 20000,
        "minLevel": 35,
        "enterDunID": 2201,
        "isCrossServer": 0,
    }),
    153: _tools.RODict({
        "ID": 153,
        "value": "双生海妖",
        "pareActivity": 32000001,
        "minScore": 30000,
        "minLevel": 45,
        "enterDunID": 2202,
        "isCrossServer": 0,
    }),
    154: _tools.RODict({
        "ID": 154,
        "value": "熔岩三头蛟",
        "pareActivity": 32000001,
        "minScore": 40000,
        "minLevel": 55,
        "enterDunID": 2203,
        "isCrossServer": 0,
    }),
    155: _tools.RODict({
        "ID": 155,
        "value": "弃天战狂",
        "pareActivity": 32000001,
        "minScore": 45000,
        "minLevel": 65,
        "enterDunID": 2204,
        "isCrossServer": 0,
    })
})
minKey = 0
maxKey = 155