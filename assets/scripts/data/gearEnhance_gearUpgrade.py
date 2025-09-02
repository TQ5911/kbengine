# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: gearEnhance/gearUpgrade
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    11: _tools.RODict({
        "ID": 11,
        "enhanceGoldCost": ((30000002, 100),),
        "enhanceItem": ((30000223, 1),),
        "class1": _tools.ROList([[0, 30, 60, 90], [10, 10, 10, 10]]),
        "class2": None,
        "class3": None,
        "class4": None,
        "advanceGoldCost": ((30000002, 200),),
        "advancedItem": ((30000227, 1),),
        "progressionSuccessRate": _tools.ROList([0.2]),
        "levelCap": 5
    }),
    12: _tools.RODict({
        "ID": 12,
        "enhanceGoldCost": ((30000002, 100),),
        "enhanceItem": ((30000223, 2),),
        "class1": _tools.ROList([[0, 30, 60, 90], [10, 10, 10, 10]]),
        "class2": None,
        "class3": None,
        "class4": None,
        "advanceGoldCost": ((30000002, 200),),
        "advancedItem": ((30000227, 2),),
        "progressionSuccessRate": _tools.ROList([0.2]),
        "levelCap": 5
    }),
    13: _tools.RODict({
        "ID": 13,
        "enhanceGoldCost": ((30000002, 100),),
        "enhanceItem": ((30000223, 3),),
        "class1": _tools.ROList([[0, 30, 60, 90], [10, 10, 10, 10]]),
        "class2": None,
        "class3": None,
        "class4": None,
        "advanceGoldCost": ((30000002, 200),),
        "advancedItem": ((30000227, 3),),
        "progressionSuccessRate": _tools.ROList([0.2]),
        "levelCap": 5
    }),
    14: _tools.RODict({
        "ID": 14,
        "enhanceGoldCost": ((30000002, 100),),
        "enhanceItem": ((30000223, 4),),
        "class1": _tools.ROList([[0, 30, 60, 90], [10, 10, 10, 10]]),
        "class2": None,
        "class3": None,
        "class4": None,
        "advanceGoldCost": ((30000002, 200),),
        "advancedItem": ((30000227, 4),),
        "progressionSuccessRate": _tools.ROList([0.2]),
        "levelCap": 5
    }),
    21: _tools.RODict({
        "ID": 21,
        "enhanceGoldCost": ((30000002, 200),),
        "enhanceItem": ((30000224, 1),),
        "class1": _tools.ROList([[0, 30, 60, 90], [10, 10, 10, 10]]),
        "class2": _tools.ROList([[0, 20, 40, 60], [10, 10, 10, 10]]),
        "class3": None,
        "class4": None,
        "advanceGoldCost": ((30000002, 400),),
        "advancedItem": ((30000228, 1),),
        "progressionSuccessRate": _tools.ROList([0.3, 0.2]),
        "levelCap": 10
    }),
    22: _tools.RODict({
        "ID": 22,
        "enhanceGoldCost": ((30000002, 200),),
        "enhanceItem": ((30000224, 2),),
        "class1": _tools.ROList([[0, 30, 60, 90], [10, 10, 10, 10]]),
        "class2": _tools.ROList([[0, 20, 40, 60], [10, 10, 10, 10]]),
        "class3": None,
        "class4": None,
        "advanceGoldCost": ((30000002, 400),),
        "advancedItem": ((30000228, 2),),
        "progressionSuccessRate": _tools.ROList([0.3, 0.2]),
        "levelCap": 10
    }),
    23: _tools.RODict({
        "ID": 23,
        "enhanceGoldCost": ((30000002, 200),),
        "enhanceItem": ((30000224, 3),),
        "class1": _tools.ROList([[0, 30, 60, 90], [10, 10, 10, 10]]),
        "class2": _tools.ROList([[0, 20, 40, 60], [10, 10, 10, 10]]),
        "class3": None,
        "class4": None,
        "advanceGoldCost": ((30000002, 400),),
        "advancedItem": ((30000228, 3),),
        "progressionSuccessRate": _tools.ROList([0.3, 0.2]),
        "levelCap": 10
    }),
    24: _tools.RODict({
        "ID": 24,
        "enhanceGoldCost": ((30000002, 200),),
        "enhanceItem": ((30000224, 4),),
        "class1": _tools.ROList([[0, 30, 60, 90], [10, 10, 10, 10]]),
        "class2": _tools.ROList([[0, 20, 40, 60], [10, 10, 10, 10]]),
        "class3": None,
        "class4": None,
        "advanceGoldCost": ((30000002, 400),),
        "advancedItem": ((30000228, 4),),
        "progressionSuccessRate": _tools.ROList([0.3, 0.2]),
        "levelCap": 10
    }),
    31: _tools.RODict({
        "ID": 31,
        "enhanceGoldCost": ((30000002, 300),),
        "enhanceItem": ((30000225, 1),),
        "class1": _tools.ROList([[0, 30, 60, 90], [10, 10, 10, 10]]),
        "class2": _tools.ROList([[0, 20, 40, 60], [10, 10, 10, 10]]),
        "class3": _tools.ROList([[0, 15, 30, 45], [10, 10, 10, 10]]),
        "class4": None,
        "advanceGoldCost": ((30000002, 600),),
        "advancedItem": ((30000229, 1),),
        "progressionSuccessRate": _tools.ROList([0.3, 0.3, 0.2]),
        "levelCap": 15
    }),
    32: _tools.RODict({
        "ID": 32,
        "enhanceGoldCost": ((30000002, 300),),
        "enhanceItem": ((30000225, 2),),
        "class1": _tools.ROList([[0, 30, 60, 90], [10, 10, 10, 10]]),
        "class2": _tools.ROList([[0, 20, 40, 60], [10, 10, 10, 10]]),
        "class3": _tools.ROList([[0, 15, 30, 45], [10, 10, 10, 10]]),
        "class4": None,
        "advanceGoldCost": ((30000002, 600),),
        "advancedItem": ((30000229, 2),),
        "progressionSuccessRate": _tools.ROList([0.3, 0.3, 0.2]),
        "levelCap": 15
    }),
    33: _tools.RODict({
        "ID": 33,
        "enhanceGoldCost": ((30000002, 300),),
        "enhanceItem": ((30000225, 3),),
        "class1": _tools.ROList([[0, 30, 60, 90], [10, 10, 10, 10]]),
        "class2": _tools.ROList([[0, 20, 40, 60], [10, 10, 10, 10]]),
        "class3": _tools.ROList([[0, 15, 30, 45], [10, 10, 10, 10]]),
        "class4": None,
        "advanceGoldCost": ((30000002, 600),),
        "advancedItem": ((30000229, 3),),
        "progressionSuccessRate": _tools.ROList([0.3, 0.3, 0.2]),
        "levelCap": 15
    }),
    34: _tools.RODict({
        "ID": 34,
        "enhanceGoldCost": ((30000002, 300),),
        "enhanceItem": ((30000225, 4),),
        "class1": _tools.ROList([[0, 30, 60, 90], [10, 10, 10, 10]]),
        "class2": _tools.ROList([[0, 20, 40, 60], [10, 10, 10, 10]]),
        "class3": _tools.ROList([[0, 15, 30, 45], [10, 10, 10, 10]]),
        "class4": None,
        "advanceGoldCost": ((30000002, 600),),
        "advancedItem": ((30000229, 4),),
        "progressionSuccessRate": _tools.ROList([0.3, 0.3, 0.2]),
        "levelCap": 15
    }),
    41: _tools.RODict({
        "ID": 41,
        "enhanceGoldCost": ((30000002, 400),),
        "enhanceItem": ((30000226, 1),),
        "class1": _tools.ROList([[10, 30, 60, 90], [10, 10, 10, 10]]),
        "class2": _tools.ROList([[0, 20, 40, 60], [10, 10, 10, 10]]),
        "class3": _tools.ROList([[0, 15, 30, 45], [10, 10, 10, 10]]),
        "class4": _tools.ROList([[0, 10, 20, 30], [10, 10, 10, 10]]),
        "advanceGoldCost": ((30000002, 800),),
        "advancedItem": ((30000230, 1),),
        "progressionSuccessRate": _tools.ROList([0.4, 0.4, 0.3, 0.2]),
        "levelCap": 20
    }),
    42: _tools.RODict({
        "ID": 42,
        "enhanceGoldCost": ((30000002, 400),),
        "enhanceItem": ((30000226, 2),),
        "class1": _tools.ROList([[10, 30, 60, 90], [10, 10, 10, 10]]),
        "class2": _tools.ROList([[0, 20, 40, 60], [10, 10, 10, 10]]),
        "class3": _tools.ROList([[0, 15, 30, 45], [10, 10, 10, 10]]),
        "class4": _tools.ROList([[0, 10, 20, 30], [10, 10, 10, 10]]),
        "advanceGoldCost": ((30000002, 800),),
        "advancedItem": ((30000230, 2),),
        "progressionSuccessRate": _tools.ROList([0.4, 0.4, 0.3, 0.2]),
        "levelCap": 20
    }),
    43: _tools.RODict({
        "ID": 43,
        "enhanceGoldCost": ((30000002, 400),),
        "enhanceItem": ((30000226, 3),),
        "class1": _tools.ROList([[10, 30, 60, 90], [10, 10, 10, 10]]),
        "class2": _tools.ROList([[0, 20, 40, 60], [10, 10, 10, 10]]),
        "class3": _tools.ROList([[0, 15, 30, 45], [10, 10, 10, 10]]),
        "class4": _tools.ROList([[0, 10, 20, 30], [10, 10, 10, 10]]),
        "advanceGoldCost": ((30000002, 800),),
        "advancedItem": ((30000230, 3),),
        "progressionSuccessRate": _tools.ROList([0.4, 0.4, 0.3, 0.2]),
        "levelCap": 20
    }),
    44: _tools.RODict({
        "ID": 44,
        "enhanceGoldCost": ((30000002, 400),),
        "enhanceItem": ((30000226, 4),),
        "class1": _tools.ROList([[10, 30, 60, 90], [10, 10, 10, 10]]),
        "class2": _tools.ROList([[0, 20, 40, 60], [10, 10, 10, 10]]),
        "class3": _tools.ROList([[0, 15, 30, 45], [10, 10, 10, 10]]),
        "class4": _tools.ROList([[0, 10, 20, 30], [10, 10, 10, 10]]),
        "advanceGoldCost": ((30000002, 800),),
        "advancedItem": ((30000230, 4),),
        "progressionSuccessRate": _tools.ROList([0.4, 0.4, 0.3, 0.2]),
        "levelCap": 20
    })
})
minKey = 11
maxKey = 44