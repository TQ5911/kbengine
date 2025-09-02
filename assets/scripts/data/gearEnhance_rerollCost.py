# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: gearEnhance/rerollCost
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
        "baseAttStoneId": 30000001,
        "baseAttStoneCount": 2,
        "baseAttGoldCost": 400,
        "reforgeStoneId": 30000001,
        "reforgeStoneCount": 3,
        "reforgeGoldCost": 400,
        "reforgeCredit": 3
    }),
    1061: _tools.RODict({
        "ID": 1061,
        "quality": 1,
        "startLevel": 61,
        "endLevel": 90,
        "baseAttStoneId": 30000001,
        "baseAttStoneCount": 4,
        "baseAttGoldCost": 600,
        "reforgeStoneId": 30000001,
        "reforgeStoneCount": 6,
        "reforgeGoldCost": 600,
        "reforgeCredit": 6
    }),
    1091: _tools.RODict({
        "ID": 1091,
        "quality": 1,
        "startLevel": 91,
        "endLevel": 120,
        "baseAttStoneId": 30000001,
        "baseAttStoneCount": 6,
        "baseAttGoldCost": 800,
        "reforgeStoneId": 30000001,
        "reforgeStoneCount": 9,
        "reforgeGoldCost": 800,
        "reforgeCredit": 9
    }),
    1121: _tools.RODict({
        "ID": 1121,
        "quality": 1,
        "startLevel": 121,
        "endLevel": 150,
        "baseAttStoneId": 30000001,
        "baseAttStoneCount": 8,
        "baseAttGoldCost": 1000,
        "reforgeStoneId": 30000001,
        "reforgeStoneCount": 12,
        "reforgeGoldCost": 1000,
        "reforgeCredit": 12
    }),
    1151: _tools.RODict({
        "ID": 1151,
        "quality": 1,
        "startLevel": 151,
        "endLevel": 200,
        "baseAttStoneId": 30000001,
        "baseAttStoneCount": 10,
        "baseAttGoldCost": 1200,
        "reforgeStoneId": 30000001,
        "reforgeStoneCount": 15,
        "reforgeGoldCost": 1200,
        "reforgeCredit": 15
    }),
    2001: _tools.RODict({
        "ID": 2001,
        "quality": 2,
        "startLevel": 1,
        "endLevel": 60,
        "baseAttStoneId": 30000001,
        "baseAttStoneCount": 3,
        "baseAttGoldCost": 400,
        "reforgeStoneId": 30000001,
        "reforgeStoneCount": 3,
        "reforgeGoldCost": 400,
        "reforgeCredit": 3
    }),
    2061: _tools.RODict({
        "ID": 2061,
        "quality": 2,
        "startLevel": 61,
        "endLevel": 90,
        "baseAttStoneId": 30000001,
        "baseAttStoneCount": 6,
        "baseAttGoldCost": 600,
        "reforgeStoneId": 30000001,
        "reforgeStoneCount": 6,
        "reforgeGoldCost": 600,
        "reforgeCredit": 6
    }),
    2091: _tools.RODict({
        "ID": 2091,
        "quality": 2,
        "startLevel": 91,
        "endLevel": 120,
        "baseAttStoneId": 30000001,
        "baseAttStoneCount": 9,
        "baseAttGoldCost": 800,
        "reforgeStoneId": 30000001,
        "reforgeStoneCount": 9,
        "reforgeGoldCost": 800,
        "reforgeCredit": 9
    }),
    2121: _tools.RODict({
        "ID": 2121,
        "quality": 2,
        "startLevel": 121,
        "endLevel": 150,
        "baseAttStoneId": 30000001,
        "baseAttStoneCount": 12,
        "baseAttGoldCost": 1000,
        "reforgeStoneId": 30000001,
        "reforgeStoneCount": 12,
        "reforgeGoldCost": 1000,
        "reforgeCredit": 12
    }),
    2151: _tools.RODict({
        "ID": 2151,
        "quality": 2,
        "startLevel": 151,
        "endLevel": 200,
        "baseAttStoneId": 30000001,
        "baseAttStoneCount": 15,
        "baseAttGoldCost": 1200,
        "reforgeStoneId": 30000001,
        "reforgeStoneCount": 15,
        "reforgeGoldCost": 1200,
        "reforgeCredit": 15
    }),
    3001: _tools.RODict({
        "ID": 3001,
        "quality": 3,
        "startLevel": 1,
        "endLevel": 60,
        "baseAttStoneId": 30000001,
        "baseAttStoneCount": 6,
        "baseAttGoldCost": 400,
        "reforgeStoneId": 30000001,
        "reforgeStoneCount": 6,
        "reforgeGoldCost": 400,
        "reforgeCredit": 6
    }),
    3061: _tools.RODict({
        "ID": 3061,
        "quality": 3,
        "startLevel": 61,
        "endLevel": 90,
        "baseAttStoneId": 30000001,
        "baseAttStoneCount": 12,
        "baseAttGoldCost": 600,
        "reforgeStoneId": 30000001,
        "reforgeStoneCount": 12,
        "reforgeGoldCost": 600,
        "reforgeCredit": 12
    }),
    3091: _tools.RODict({
        "ID": 3091,
        "quality": 3,
        "startLevel": 91,
        "endLevel": 120,
        "baseAttStoneId": 30000001,
        "baseAttStoneCount": 18,
        "baseAttGoldCost": 800,
        "reforgeStoneId": 30000001,
        "reforgeStoneCount": 18,
        "reforgeGoldCost": 800,
        "reforgeCredit": 18
    }),
    3121: _tools.RODict({
        "ID": 3121,
        "quality": 3,
        "startLevel": 121,
        "endLevel": 150,
        "baseAttStoneId": 30000001,
        "baseAttStoneCount": 24,
        "baseAttGoldCost": 1000,
        "reforgeStoneId": 30000001,
        "reforgeStoneCount": 24,
        "reforgeGoldCost": 1000,
        "reforgeCredit": 24
    }),
    3151: _tools.RODict({
        "ID": 3151,
        "quality": 3,
        "startLevel": 151,
        "endLevel": 200,
        "baseAttStoneId": 30000001,
        "baseAttStoneCount": 30,
        "baseAttGoldCost": 1200,
        "reforgeStoneId": 30000001,
        "reforgeStoneCount": 30,
        "reforgeGoldCost": 1200,
        "reforgeCredit": 30
    }),
    4001: _tools.RODict({
        "ID": 4001,
        "quality": 4,
        "startLevel": 1,
        "endLevel": 60,
        "baseAttStoneId": 30000001,
        "baseAttStoneCount": 7,
        "baseAttGoldCost": 400,
        "reforgeStoneId": 30000001,
        "reforgeStoneCount": 6,
        "reforgeGoldCost": 400,
        "reforgeCredit": 6
    }),
    4061: _tools.RODict({
        "ID": 4061,
        "quality": 4,
        "startLevel": 61,
        "endLevel": 90,
        "baseAttStoneId": 30000001,
        "baseAttStoneCount": 14,
        "baseAttGoldCost": 600,
        "reforgeStoneId": 30000001,
        "reforgeStoneCount": 12,
        "reforgeGoldCost": 600,
        "reforgeCredit": 12
    }),
    4091: _tools.RODict({
        "ID": 4091,
        "quality": 4,
        "startLevel": 91,
        "endLevel": 120,
        "baseAttStoneId": 30000001,
        "baseAttStoneCount": 21,
        "baseAttGoldCost": 800,
        "reforgeStoneId": 30000001,
        "reforgeStoneCount": 18,
        "reforgeGoldCost": 800,
        "reforgeCredit": 18
    }),
    4121: _tools.RODict({
        "ID": 4121,
        "quality": 4,
        "startLevel": 121,
        "endLevel": 150,
        "baseAttStoneId": 30000001,
        "baseAttStoneCount": 28,
        "baseAttGoldCost": 1000,
        "reforgeStoneId": 30000001,
        "reforgeStoneCount": 24,
        "reforgeGoldCost": 1000,
        "reforgeCredit": 24
    }),
    4151: _tools.RODict({
        "ID": 4151,
        "quality": 4,
        "startLevel": 151,
        "endLevel": 200,
        "baseAttStoneId": 30000001,
        "baseAttStoneCount": 35,
        "baseAttGoldCost": 1200,
        "reforgeStoneId": 30000001,
        "reforgeStoneCount": 30,
        "reforgeGoldCost": 1200,
        "reforgeCredit": 30
    })
})
minKey = 1001
maxKey = 4151