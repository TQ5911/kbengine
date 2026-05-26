# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: soul/soulProp
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    1: _tools.RODict({
        "ID": 1,
        "propType": "adjMinPhysicalArmor",
        "occupation": (1001, 1002, 1003),
        "qualityValue": ((1, 5), (10, 15), (20, 25), (32, 40))
    }),
    2: _tools.RODict({
        "ID": 2,
        "propType": "adjMaxPhysicalArmor",
        "occupation": (1001, 1002, 1003),
        "qualityValue": ((3, 8), (16, 24), (32, 40), (52, 64))
    }),
    3: _tools.RODict({
        "ID": 3,
        "propType": "adjMinMagicArmor",
        "occupation": (1001, 1002, 1003),
        "qualityValue": ((1, 5), (10, 15), (20, 25), (32, 40))
    }),
    4: _tools.RODict({
        "ID": 4,
        "propType": "adjMaxMagicArmor",
        "occupation": (1001, 1002, 1003),
        "qualityValue": ((3, 8), (16, 24), (32, 40), (52, 64))
    }),
    5: _tools.RODict({
        "ID": 5,
        "propType": "adjDodge",
        "occupation": (1001, 1002, 1003),
        "qualityValue": ((1, 1), (2, 3), (4, 5), (6, 8))
    }),
    6: _tools.RODict({
        "ID": 6,
        "propType": "adjAntiFatal",
        "occupation": (1001, 1002, 1003),
        "qualityValue": ((1, 1), (2, 3), (4, 5), (6, 8))
    }),
    7: _tools.RODict({
        "ID": 7,
        "propType": "adjMinPhysicalAtk",
        "occupation": (1003,),
        "qualityValue": ((2, 3), (6, 9), (12, 15), (20, 24))
    }),
    8: _tools.RODict({
        "ID": 8,
        "propType": "adjMaxPhysicalAtk",
        "occupation": (1003,),
        "qualityValue": ((4, 5), (10, 15), (20, 25), (32, 40))
    }),
    9: _tools.RODict({
        "ID": 9,
        "propType": "adjMinMagicAtk",
        "occupation": (1001, 1002),
        "qualityValue": ((2, 3), (6, 9), (12, 15), (20, 24))
    }),
    10: _tools.RODict({
        "ID": 10,
        "propType": "adjMaxMagicAtk",
        "occupation": (1001, 1002),
        "qualityValue": ((4, 5), (10, 15), (20, 25), (32, 40))
    }),
    11: _tools.RODict({
        "ID": 11,
        "propType": "adjHit",
        "occupation": (1001, 1002, 1003),
        "qualityValue": ((1, 1), (2, 3), (4, 5), (6, 8))
    }),
    12: _tools.RODict({
        "ID": 12,
        "propType": "adjFatal",
        "occupation": (1001, 1002, 1003),
        "qualityValue": ((1, 1), (2, 3), (4, 5), (6, 8))
    }),
    13: _tools.RODict({
        "ID": 13,
        "propType": "adjMinPhysicalArmor",
        "occupation": (1001, 1002, 1003),
        "qualityValue": ((1, 5), (10, 15), (20, 25), (32, 40))
    }),
    14: _tools.RODict({
        "ID": 14,
        "propType": "adjMaxPhysicalArmor",
        "occupation": (1001, 1002, 1003),
        "qualityValue": ((3, 8), (16, 24), (32, 40), (52, 64))
    }),
    15: _tools.RODict({
        "ID": 15,
        "propType": "adjMinMagicArmor",
        "occupation": (1001, 1002, 1003),
        "qualityValue": ((1, 5), (10, 15), (20, 25), (32, 40))
    }),
    16: _tools.RODict({
        "ID": 16,
        "propType": "adjMaxMagicArmor",
        "occupation": (1001, 1002, 1003),
        "qualityValue": ((3, 8), (16, 24), (32, 40), (52, 64))
    }),
    17: _tools.RODict({
        "ID": 17,
        "propType": "adjDodge",
        "occupation": (1001, 1002, 1003),
        "qualityValue": ((1, 1), (2, 3), (4, 5), (6, 8))
    }),
    18: _tools.RODict({
        "ID": 18,
        "propType": "adjMinPhysicalArmor",
        "occupation": (1001, 1002, 1003),
        "qualityValue": ((1, 5), (10, 15), (20, 25), (32, 40))
    }),
    19: _tools.RODict({
        "ID": 19,
        "propType": "adjMaxPhysicalArmor",
        "occupation": (1001, 1002, 1003),
        "qualityValue": ((3, 8), (16, 24), (32, 40), (52, 64))
    }),
    20: _tools.RODict({
        "ID": 20,
        "propType": "adjMinMagicArmor",
        "occupation": (1001, 1002, 1003),
        "qualityValue": ((1, 5), (10, 15), (20, 25), (32, 40))
    }),
    21: _tools.RODict({
        "ID": 21,
        "propType": "adjMaxMagicArmor",
        "occupation": (1001, 1002, 1003),
        "qualityValue": ((3, 8), (16, 24), (32, 40), (52, 64))
    }),
    22: _tools.RODict({
        "ID": 22,
        "propType": "adjEvasion",
        "occupation": (1001, 1002, 1003),
        "qualityValue": ((1, 1), (2, 3), (4, 5), (6, 8))
    }),
    23: _tools.RODict({
        "ID": 23,
        "propType": "adjMinPhysicalArmor",
        "occupation": (1001, 1002, 1003),
        "qualityValue": ((1, 5), (10, 15), (20, 25), (32, 40))
    }),
    24: _tools.RODict({
        "ID": 24,
        "propType": "adjMaxPhysicalArmor",
        "occupation": (1001, 1002, 1003),
        "qualityValue": ((3, 8), (16, 24), (32, 40), (52, 64))
    }),
    25: _tools.RODict({
        "ID": 25,
        "propType": "adjMinMagicArmor",
        "occupation": (1001, 1002, 1003),
        "qualityValue": ((1, 5), (10, 15), (20, 25), (32, 40))
    }),
    26: _tools.RODict({
        "ID": 26,
        "propType": "adjMaxMagicArmor",
        "occupation": (1001, 1002, 1003),
        "qualityValue": ((3, 8), (16, 24), (32, 40), (52, 64))
    }),
    27: _tools.RODict({
        "ID": 27,
        "propType": "adjDodge",
        "occupation": (1001, 1002, 1003),
        "qualityValue": ((1, 1), (2, 3), (4, 5), (6, 8))
    }),
    28: _tools.RODict({
        "ID": 28,
        "propType": "adjMinPhysicalAtk",
        "occupation": (1003,),
        "qualityValue": ((2, 3), (6, 9), (12, 15), (20, 24))
    }),
    29: _tools.RODict({
        "ID": 29,
        "propType": "adjMaxPhysicalAtk",
        "occupation": (1003,),
        "qualityValue": ((4, 5), (10, 15), (20, 25), (32, 40))
    }),
    30: _tools.RODict({
        "ID": 30,
        "propType": "adjMinMagicAtk",
        "occupation": (1001, 1002),
        "qualityValue": ((2, 3), (6, 9), (12, 15), (20, 24))
    }),
    31: _tools.RODict({
        "ID": 31,
        "propType": "adjMaxMagicAtk",
        "occupation": (1001, 1002),
        "qualityValue": ((4, 5), (10, 15), (20, 25), (32, 40))
    }),
    32: _tools.RODict({
        "ID": 32,
        "propType": "adjAccuracy",
        "occupation": (1001, 1002, 1003),
        "qualityValue": ((1, 5), (6, 15), (20, 25), (30, 40))
    }),
    33: _tools.RODict({
        "ID": 33,
        "propType": "adjMinPhysicalAtk",
        "occupation": (1003,),
        "qualityValue": ((2, 3), (6, 9), (12, 15), (20, 24))
    }),
    34: _tools.RODict({
        "ID": 34,
        "propType": "adjMaxPhysicalAtk",
        "occupation": (1003,),
        "qualityValue": ((4, 5), (10, 15), (20, 25), (32, 40))
    }),
    35: _tools.RODict({
        "ID": 35,
        "propType": "adjMinMagicAtk",
        "occupation": (1001, 1002),
        "qualityValue": ((2, 3), (6, 9), (12, 15), (20, 24))
    }),
    36: _tools.RODict({
        "ID": 36,
        "propType": "adjMaxMagicAtk",
        "occupation": (1001, 1002),
        "qualityValue": ((4, 5), (10, 15), (20, 25), (32, 40))
    }),
    37: _tools.RODict({
        "ID": 37,
        "propType": "adjHit",
        "occupation": (1001, 1002, 1003),
        "qualityValue": ((1, 5), (6, 15), (20, 25), (30, 40))
    }),
    38: _tools.RODict({
        "ID": 38,
        "propType": "adjAtkBless",
        "occupation": (1001, 1002, 1003),
        "qualityValue": ((0, 0), (0, 0), (1, 1), (2, 2))
    }),
    39: _tools.RODict({
        "ID": 39,
        "propType": "adjMinPhysicalAtk",
        "occupation": (1003,),
        "qualityValue": ((2, 3), (6, 9), (12, 15), (20, 24))
    }),
    40: _tools.RODict({
        "ID": 40,
        "propType": "adjMaxPhysicalAtk",
        "occupation": (1003,),
        "qualityValue": ((4, 5), (10, 15), (20, 25), (32, 40))
    }),
    41: _tools.RODict({
        "ID": 41,
        "propType": "adjMinMagicAtk",
        "occupation": (1001, 1002),
        "qualityValue": ((2, 3), (6, 9), (12, 15), (20, 24))
    }),
    42: _tools.RODict({
        "ID": 42,
        "propType": "adjMaxMagicAtk",
        "occupation": (1001, 1002),
        "qualityValue": ((4, 5), (10, 15), (20, 25), (32, 40))
    }),
    43: _tools.RODict({
        "ID": 43,
        "propType": "adjHit",
        "occupation": (1001, 1002, 1003),
        "qualityValue": ((1, 5), (6, 15), (20, 25), (30, 40))
    })
})
minKey = 1
maxKey = 43