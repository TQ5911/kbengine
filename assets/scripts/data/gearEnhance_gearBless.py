# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: gearEnhance/gearBless
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    120: _tools.RODict({
        "ID": 120,
        "gearBlessGoldCost": ((30000013, 2000),),
        "gearBlessItem": ((30000220, 1),),
        "result": _tools.ROList([[-2, -1, 0, 1], [0, 0, 50, 50]]),
        "backtrack": 5,
        "guaranteedCount": 0
    }),
    121: _tools.RODict({
        "ID": 121,
        "gearBlessGoldCost": ((30000013, 2000),),
        "gearBlessItem": ((30000220, 1),),
        "result": _tools.ROList([[-2, -1, 0, 1], [0, 20, 45, 35]]),
        "backtrack": 5,
        "guaranteedCount": 0
    }),
    122: _tools.RODict({
        "ID": 122,
        "gearBlessGoldCost": ((30000013, 2000),),
        "gearBlessItem": ((30000220, 1),),
        "result": _tools.ROList([[-2, -1, 0, 1], [0, 20, 60, 20]]),
        "backtrack": 7,
        "guaranteedCount": 0
    }),
    123: _tools.RODict({
        "ID": 123,
        "gearBlessGoldCost": ((30000013, 2000),),
        "gearBlessItem": ((30000220, 1),),
        "result": _tools.ROList([[-2, -1, 0, 1], [0, 15, 75, 10]]),
        "backtrack": 15,
        "guaranteedCount": 0
    }),
    124: _tools.RODict({
        "ID": 124,
        "gearBlessGoldCost": ((30000013, 2000),),
        "gearBlessItem": ((30000220, 1),),
        "result": _tools.ROList([[-2, -1, 0, 1], [0, 10, 85, 5]]),
        "backtrack": 30,
        "guaranteedCount": 0
    }),
    125: _tools.RODict({
        "ID": 125,
        "gearBlessGoldCost": ((30000013, 2000),),
        "gearBlessItem": ((30000220, 1),),
        "result": _tools.ROList([[-2, -1, 0, 1], [0, 10, 85, 5]]),
        "backtrack": 100,
        "guaranteedCount": 0
    }),
    126: _tools.RODict({
        "ID": 126,
        "gearBlessGoldCost": ((30000013, 2000),),
        "gearBlessItem": ((30000220, 1),),
        "result": _tools.ROList([[-2, -1, 0, 1], [0, 20, 79, 1]]),
        "backtrack": 200,
        "guaranteedCount": 15
    }),
    127: _tools.RODict({
        "ID": 127,
        "gearBlessGoldCost": 0,
        "gearBlessItem": 0,
        "result": 0,
        "backtrack": 2500,
        "guaranteedCount": 0
    }),
    130: _tools.RODict({
        "ID": 130,
        "gearBlessGoldCost": ((30000013, 5000),),
        "gearBlessItem": ((30000220, 1),),
        "result": _tools.ROList([[-2, -1, 0, 1], [0, 0, 50, 50]]),
        "backtrack": 5,
        "guaranteedCount": 0
    }),
    131: _tools.RODict({
        "ID": 131,
        "gearBlessGoldCost": ((30000013, 5000),),
        "gearBlessItem": ((30000220, 1),),
        "result": _tools.ROList([[-2, -1, 0, 1], [0, 20, 45, 35]]),
        "backtrack": 5,
        "guaranteedCount": 0
    }),
    132: _tools.RODict({
        "ID": 132,
        "gearBlessGoldCost": ((30000013, 5000),),
        "gearBlessItem": ((30000220, 1),),
        "result": _tools.ROList([[-2, -1, 0, 1], [0, 20, 60, 20]]),
        "backtrack": 7,
        "guaranteedCount": 0
    }),
    133: _tools.RODict({
        "ID": 133,
        "gearBlessGoldCost": ((30000013, 5000),),
        "gearBlessItem": ((30000220, 1),),
        "result": _tools.ROList([[-2, -1, 0, 1], [0, 15, 75, 10]]),
        "backtrack": 15,
        "guaranteedCount": 0
    }),
    134: _tools.RODict({
        "ID": 134,
        "gearBlessGoldCost": ((30000013, 5000),),
        "gearBlessItem": ((30000220, 1),),
        "result": _tools.ROList([[-2, -1, 0, 1], [0, 10, 85, 5]]),
        "backtrack": 30,
        "guaranteedCount": 0
    }),
    135: _tools.RODict({
        "ID": 135,
        "gearBlessGoldCost": ((30000013, 5000),),
        "gearBlessItem": ((30000220, 1),),
        "result": _tools.ROList([[-2, -1, 0, 1], [0, 10, 85, 5]]),
        "backtrack": 100,
        "guaranteedCount": 0
    }),
    136: _tools.RODict({
        "ID": 136,
        "gearBlessGoldCost": ((30000013, 5000),),
        "gearBlessItem": ((30000220, 1),),
        "result": _tools.ROList([[-2, -1, 0, 1], [0, 20, 79, 1]]),
        "backtrack": 200,
        "guaranteedCount": 30
    }),
    137: _tools.RODict({
        "ID": 137,
        "gearBlessGoldCost": 0,
        "gearBlessItem": 0,
        "result": 0,
        "backtrack": 2500,
        "guaranteedCount": 0
    }),
    140: _tools.RODict({
        "ID": 140,
        "gearBlessGoldCost": ((30000013, 10000),),
        "gearBlessItem": ((30000220, 2),),
        "result": _tools.ROList([[-2, -1, 0, 1], [0, 0, 50, 50]]),
        "backtrack": 5,
        "guaranteedCount": 0
    }),
    141: _tools.RODict({
        "ID": 141,
        "gearBlessGoldCost": ((30000013, 10000),),
        "gearBlessItem": ((30000220, 2),),
        "result": _tools.ROList([[-2, -1, 0, 1], [0, 20, 45, 35]]),
        "backtrack": 5,
        "guaranteedCount": 0
    }),
    142: _tools.RODict({
        "ID": 142,
        "gearBlessGoldCost": ((30000013, 10000),),
        "gearBlessItem": ((30000220, 2),),
        "result": _tools.ROList([[-2, -1, 0, 1], [0, 20, 60, 20]]),
        "backtrack": 7,
        "guaranteedCount": 0
    }),
    143: _tools.RODict({
        "ID": 143,
        "gearBlessGoldCost": ((30000013, 10000),),
        "gearBlessItem": ((30000220, 2),),
        "result": _tools.ROList([[-2, -1, 0, 1], [0, 15, 75, 10]]),
        "backtrack": 15,
        "guaranteedCount": 0
    }),
    144: _tools.RODict({
        "ID": 144,
        "gearBlessGoldCost": ((30000013, 10000),),
        "gearBlessItem": ((30000220, 2),),
        "result": _tools.ROList([[-2, -1, 0, 1], [0, 10, 85, 5]]),
        "backtrack": 30,
        "guaranteedCount": 0
    }),
    145: _tools.RODict({
        "ID": 145,
        "gearBlessGoldCost": ((30000013, 10000),),
        "gearBlessItem": ((30000220, 2),),
        "result": _tools.ROList([[-2, -1, 0, 1], [0, 10, 85, 5]]),
        "backtrack": 100,
        "guaranteedCount": 0
    }),
    146: _tools.RODict({
        "ID": 146,
        "gearBlessGoldCost": ((30000013, 10000),),
        "gearBlessItem": ((30000220, 2),),
        "result": _tools.ROList([[-2, -1, 0, 1], [0, 20, 79, 1]]),
        "backtrack": 200,
        "guaranteedCount": 30
    }),
    147: _tools.RODict({
        "ID": 147,
        "gearBlessGoldCost": 0,
        "gearBlessItem": 0,
        "result": 0,
        "backtrack": 2500,
        "guaranteedCount": 0
    })
})
minKey = 120
maxKey = 147