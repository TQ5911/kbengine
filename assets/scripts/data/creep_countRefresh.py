# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: creep/countRefresh
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
        "mapID": 3103,
        "combatAreaID": 31038004,
        "refreshMonsterID": _tools.ROList([31030088]),
        "countLimit": 30,
        "countMonsterID": _tools.ROList([11011004, 11011005, 11011006]),
        "countResetTime": 60
    }),
    2: _tools.RODict({
        "ID": 2,
        "mapID": 3103,
        "combatAreaID": 31038005,
        "refreshMonsterID": _tools.ROList([31030129]),
        "countLimit": 30,
        "countMonsterID": _tools.ROList([11011004, 11011005, 11011006]),
        "countResetTime": 60
    }),
    3: _tools.RODict({
        "ID": 3,
        "mapID": 3103,
        "combatAreaID": 31038006,
        "refreshMonsterID": _tools.ROList([31030170]),
        "countLimit": 30,
        "countMonsterID": _tools.ROList([11011004, 11011005, 11011006]),
        "countResetTime": 60
    }),
    4: _tools.RODict({
        "ID": 4,
        "mapID": 3104,
        "combatAreaID": 31048004,
        "refreshMonsterID": _tools.ROList([31040088]),
        "countLimit": 30,
        "countMonsterID": _tools.ROList([11011004, 11011005, 11011006]),
        "countResetTime": 60
    }),
    5: _tools.RODict({
        "ID": 5,
        "mapID": 3104,
        "combatAreaID": 31048005,
        "refreshMonsterID": _tools.ROList([31040129]),
        "countLimit": 30,
        "countMonsterID": _tools.ROList([11011004, 11011005, 11011006]),
        "countResetTime": 60
    }),
    6: _tools.RODict({
        "ID": 6,
        "mapID": 3104,
        "combatAreaID": 31048006,
        "refreshMonsterID": _tools.ROList([31040170]),
        "countLimit": 30,
        "countMonsterID": _tools.ROList([11011004, 11011005, 11011006]),
        "countResetTime": 60
    }),
    7: _tools.RODict({
        "ID": 7,
        "mapID": 3105,
        "combatAreaID": 31058004,
        "refreshMonsterID": _tools.ROList([31050088]),
        "countLimit": 30,
        "countMonsterID": _tools.ROList([11011004, 11011005, 11011006]),
        "countResetTime": 60
    }),
    8: _tools.RODict({
        "ID": 8,
        "mapID": 3105,
        "combatAreaID": 31058005,
        "refreshMonsterID": _tools.ROList([31050129]),
        "countLimit": 30,
        "countMonsterID": _tools.ROList([11011004, 11011005, 11011006]),
        "countResetTime": 60
    }),
    9: _tools.RODict({
        "ID": 9,
        "mapID": 3105,
        "combatAreaID": 31058006,
        "refreshMonsterID": _tools.ROList([31050170]),
        "countLimit": 30,
        "countMonsterID": _tools.ROList([11011004, 11011005, 11011006]),
        "countResetTime": 60
    }),
    10: _tools.RODict({
        "ID": 10,
        "mapID": 3112,
        "combatAreaID": 31128004,
        "refreshMonsterID": _tools.ROList([31120088]),
        "countLimit": 30,
        "countMonsterID": _tools.ROList([11011011, 11011012, 11011013]),
        "countResetTime": 60
    }),
    11: _tools.RODict({
        "ID": 11,
        "mapID": 3112,
        "combatAreaID": 31128005,
        "refreshMonsterID": _tools.ROList([31120129]),
        "countLimit": 30,
        "countMonsterID": _tools.ROList([11011011, 11011012, 11011013]),
        "countResetTime": 60
    }),
    12: _tools.RODict({
        "ID": 12,
        "mapID": 3112,
        "combatAreaID": 31128006,
        "refreshMonsterID": _tools.ROList([31120170]),
        "countLimit": 30,
        "countMonsterID": _tools.ROList([11011011, 11011012, 11011013]),
        "countResetTime": 60
    }),
    13: _tools.RODict({
        "ID": 13,
        "mapID": 3113,
        "combatAreaID": 31138004,
        "refreshMonsterID": _tools.ROList([31130088]),
        "countLimit": 30,
        "countMonsterID": _tools.ROList([11011011, 11011012, 11011013]),
        "countResetTime": 60
    }),
    14: _tools.RODict({
        "ID": 14,
        "mapID": 3113,
        "combatAreaID": 31138005,
        "refreshMonsterID": _tools.ROList([31130129]),
        "countLimit": 30,
        "countMonsterID": _tools.ROList([11011011, 11011012, 11011013]),
        "countResetTime": 60
    }),
    15: _tools.RODict({
        "ID": 15,
        "mapID": 3113,
        "combatAreaID": 31138006,
        "refreshMonsterID": _tools.ROList([31130170]),
        "countLimit": 30,
        "countMonsterID": _tools.ROList([11011011, 11011012, 11011013]),
        "countResetTime": 60
    }),
    16: _tools.RODict({
        "ID": 16,
        "mapID": 3114,
        "combatAreaID": 31148004,
        "refreshMonsterID": _tools.ROList([31140088]),
        "countLimit": 30,
        "countMonsterID": _tools.ROList([11011011, 11011012, 11011013]),
        "countResetTime": 60
    }),
    17: _tools.RODict({
        "ID": 17,
        "mapID": 3114,
        "combatAreaID": 31148005,
        "refreshMonsterID": _tools.ROList([31140129]),
        "countLimit": 30,
        "countMonsterID": _tools.ROList([11011011, 11011012, 11011013]),
        "countResetTime": 60
    }),
    18: _tools.RODict({
        "ID": 18,
        "mapID": 3114,
        "combatAreaID": 31148006,
        "refreshMonsterID": _tools.ROList([31140170]),
        "countLimit": 30,
        "countMonsterID": _tools.ROList([11011011, 11011012, 11011013]),
        "countResetTime": 60
    }),
    19: _tools.RODict({
        "ID": 19,
        "mapID": 3118,
        "combatAreaID": 31188004,
        "refreshMonsterID": _tools.ROList([31180088]),
        "countLimit": 30,
        "countMonsterID": _tools.ROList([11011046, 11011047, 11011048]),
        "countResetTime": 60
    }),
    20: _tools.RODict({
        "ID": 20,
        "mapID": 3118,
        "combatAreaID": 31188005,
        "refreshMonsterID": _tools.ROList([31180129]),
        "countLimit": 30,
        "countMonsterID": _tools.ROList([11011046, 11011047, 11011048]),
        "countResetTime": 60
    }),
    21: _tools.RODict({
        "ID": 21,
        "mapID": 3118,
        "combatAreaID": 31188006,
        "refreshMonsterID": _tools.ROList([31180170]),
        "countLimit": 30,
        "countMonsterID": _tools.ROList([11011046, 11011047, 11011048]),
        "countResetTime": 60
    }),
    22: _tools.RODict({
        "ID": 22,
        "mapID": 3119,
        "combatAreaID": 31198004,
        "refreshMonsterID": _tools.ROList([31190088]),
        "countLimit": 30,
        "countMonsterID": _tools.ROList([11011050, 11011051, 11011052]),
        "countResetTime": 60
    }),
    23: _tools.RODict({
        "ID": 23,
        "mapID": 3119,
        "combatAreaID": 31198005,
        "refreshMonsterID": _tools.ROList([31190129]),
        "countLimit": 30,
        "countMonsterID": _tools.ROList([11011050, 11011051, 11011052]),
        "countResetTime": 60
    }),
    24: _tools.RODict({
        "ID": 24,
        "mapID": 3119,
        "combatAreaID": 31198006,
        "refreshMonsterID": _tools.ROList([31190170]),
        "countLimit": 30,
        "countMonsterID": _tools.ROList([11011050, 11011051, 11011052]),
        "countResetTime": 60
    }),
    25: _tools.RODict({
        "ID": 25,
        "mapID": 3120,
        "combatAreaID": 31208008,
        "refreshMonsterID": _tools.ROList([31200096, 31200104]),
        "countLimit": 30,
        "countMonsterID": _tools.ROList([11011030, 11011031, 11011032]),
        "countResetTime": 60
    }),
    26: _tools.RODict({
        "ID": 26,
        "mapID": 3120,
        "combatAreaID": 31208008,
        "refreshMonsterID": _tools.ROList([31200112, 31200120]),
        "countLimit": 30,
        "countMonsterID": _tools.ROList([11011035, 11011036, 11011037]),
        "countResetTime": 60
    }),
    27: _tools.RODict({
        "ID": 27,
        "mapID": 3120,
        "combatAreaID": 31208008,
        "refreshMonsterID": _tools.ROList([31200129, 31200137]),
        "countLimit": 30,
        "countMonsterID": _tools.ROList([11011040, 11011041, 11011042]),
        "countResetTime": 60
    }),
    28: _tools.RODict({
        "ID": 28,
        "mapID": 3120,
        "combatAreaID": 31208008,
        "refreshMonsterID": _tools.ROList([31200168]),
        "countLimit": 12,
        "countMonsterID": _tools.ROList([11011033, 11011034, 11011038, 11011039, 11011043, 11011044]),
        "countResetTime": 60
    })
})
minKey = 1
maxKey = 28

refreshMonsterIDIndex = {310331030088: 1, 310331030129: 2, 310331030170: 3, 310431040088: 4, 310431040129: 5, 310431040170: 6, 310531050088: 7, 310531050129: 8, 310531050170: 9, 311231120088: 10, 311231120129: 11, 311231120170: 12, 311331130088: 13, 311331130129: 14, 311331130170: 15, 311431140088: 16, 311431140129: 17, 311431140170: 18, 311831180088: 19, 311831180129: 20, 311831180170: 21, 311931190088: 22, 311931190129: 23, 311931190170: 24, 312031200096: 25, 312031200104: 25, 312031200112: 26, 312031200120: 26, 312031200129: 27, 312031200137: 27, 312031200168: 28}


mapIDIndex = {3103: [1, 2, 3], 3104: [4, 5, 6], 3105: [7, 8, 9], 3112: [10, 11, 12], 3113: [13, 14, 15], 3114: [16, 17, 18], 3118: [19, 20, 21], 3119: [22, 23, 24], 3120: [25, 26, 27, 28]}
