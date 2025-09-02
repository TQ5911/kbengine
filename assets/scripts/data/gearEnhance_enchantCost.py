# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: gearEnhance/enchantCost
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
        "quality": 1,
        "startLevel": 1,
        "endLevel": 60,
        "enchantScrollId": 30000001,
        "enchantScrollCount": 1,
        "enchantCost": 0
    }),
    1061: _tools.RODict({
        "ID": 1061,
        "quality": 1,
        "startLevel": 61,
        "endLevel": 90,
        "enchantScrollId": 30000001,
        "enchantScrollCount": 2,
        "enchantCost": 0
    }),
    1091: _tools.RODict({
        "ID": 1091,
        "quality": 1,
        "startLevel": 91,
        "endLevel": 120,
        "enchantScrollId": 30000001,
        "enchantScrollCount": 3,
        "enchantCost": 0
    }),
    1121: _tools.RODict({
        "ID": 1121,
        "quality": 1,
        "startLevel": 121,
        "endLevel": 150,
        "enchantScrollId": 30000001,
        "enchantScrollCount": 4,
        "enchantCost": 0
    }),
    1151: _tools.RODict({
        "ID": 1151,
        "quality": 1,
        "startLevel": 151,
        "endLevel": 200,
        "enchantScrollId": 30000001,
        "enchantScrollCount": 5,
        "enchantCost": 0
    }),
    2001: _tools.RODict({
        "ID": 2001,
        "quality": 2,
        "startLevel": 1,
        "endLevel": 60,
        "enchantScrollId": 30000001,
        "enchantScrollCount": 1,
        "enchantCost": 0
    }),
    2061: _tools.RODict({
        "ID": 2061,
        "quality": 2,
        "startLevel": 61,
        "endLevel": 90,
        "enchantScrollId": 30000001,
        "enchantScrollCount": 2,
        "enchantCost": 0
    }),
    2091: _tools.RODict({
        "ID": 2091,
        "quality": 2,
        "startLevel": 91,
        "endLevel": 120,
        "enchantScrollId": 30000001,
        "enchantScrollCount": 3,
        "enchantCost": 0
    }),
    2121: _tools.RODict({
        "ID": 2121,
        "quality": 2,
        "startLevel": 121,
        "endLevel": 150,
        "enchantScrollId": 30000001,
        "enchantScrollCount": 4,
        "enchantCost": 0
    }),
    2151: _tools.RODict({
        "ID": 2151,
        "quality": 2,
        "startLevel": 151,
        "endLevel": 200,
        "enchantScrollId": 30000001,
        "enchantScrollCount": 5,
        "enchantCost": 0
    }),
    3001: _tools.RODict({
        "ID": 3001,
        "quality": 3,
        "startLevel": 1,
        "endLevel": 60,
        "enchantScrollId": 30000001,
        "enchantScrollCount": 1,
        "enchantCost": 0
    }),
    3061: _tools.RODict({
        "ID": 3061,
        "quality": 3,
        "startLevel": 61,
        "endLevel": 90,
        "enchantScrollId": 30000001,
        "enchantScrollCount": 2,
        "enchantCost": 0
    }),
    3091: _tools.RODict({
        "ID": 3091,
        "quality": 3,
        "startLevel": 91,
        "endLevel": 120,
        "enchantScrollId": 30000001,
        "enchantScrollCount": 3,
        "enchantCost": 0
    }),
    3121: _tools.RODict({
        "ID": 3121,
        "quality": 3,
        "startLevel": 121,
        "endLevel": 150,
        "enchantScrollId": 30000001,
        "enchantScrollCount": 4,
        "enchantCost": 0
    }),
    3151: _tools.RODict({
        "ID": 3151,
        "quality": 3,
        "startLevel": 151,
        "endLevel": 200,
        "enchantScrollId": 30000001,
        "enchantScrollCount": 5,
        "enchantCost": 0
    }),
    4001: _tools.RODict({
        "ID": 4001,
        "quality": 4,
        "startLevel": 1,
        "endLevel": 60,
        "enchantScrollId": 30000001,
        "enchantScrollCount": 2,
        "enchantCost": 0
    }),
    4061: _tools.RODict({
        "ID": 4061,
        "quality": 4,
        "startLevel": 61,
        "endLevel": 90,
        "enchantScrollId": 30000001,
        "enchantScrollCount": 4,
        "enchantCost": 0
    }),
    4091: _tools.RODict({
        "ID": 4091,
        "quality": 4,
        "startLevel": 91,
        "endLevel": 120,
        "enchantScrollId": 30000001,
        "enchantScrollCount": 6,
        "enchantCost": 0
    }),
    4121: _tools.RODict({
        "ID": 4121,
        "quality": 4,
        "startLevel": 121,
        "endLevel": 150,
        "enchantScrollId": 30000001,
        "enchantScrollCount": 8,
        "enchantCost": 0
    }),
    4151: _tools.RODict({
        "ID": 4151,
        "quality": 4,
        "startLevel": 151,
        "endLevel": 200,
        "enchantScrollId": 30000001,
        "enchantScrollCount": 10,
        "enchantCost": 0
    })
})
minKey = 1001
maxKey = 4151