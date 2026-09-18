# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: meridian/meridian
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
        "prop0": None,
        "prop1001": _tools.ROList([['adjMaxMagicAtk', 4], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1002": _tools.ROList([['adjMaxMagicAtk', 4], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1003": _tools.ROList([['adjMaxPhysicalAtk', 4], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "needItems": _tools.ROList([[30000279, 10]]),
        "needCoins": _tools.ROList([30000002, 50000]),
        "needLevel": 0
    }),
    2: _tools.RODict({
        "ID": 2,
        "prop0": None,
        "prop1001": _tools.ROList([['adjMaxMagicAtk', 4], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1002": _tools.ROList([['adjMaxMagicAtk', 4], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1003": _tools.ROList([['adjMaxPhysicalAtk', 4], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "needItems": _tools.ROList([[30000279, 20]]),
        "needCoins": _tools.ROList([30000002, 100000]),
        "needLevel": 0
    }),
    3: _tools.RODict({
        "ID": 3,
        "prop0": None,
        "prop1001": _tools.ROList([['adjMaxMagicAtk', 5], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1002": _tools.ROList([['adjMaxMagicAtk', 5], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1003": _tools.ROList([['adjMaxPhysicalAtk', 5], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "needItems": _tools.ROList([[30000279, 40]]),
        "needCoins": _tools.ROList([30000002, 150000]),
        "needLevel": 25
    }),
    4: _tools.RODict({
        "ID": 4,
        "prop0": None,
        "prop1001": _tools.ROList([['adjMaxMagicAtk', 5], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1002": _tools.ROList([['adjMaxMagicAtk', 5], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1003": _tools.ROList([['adjMaxPhysicalAtk', 5], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "needItems": _tools.ROList([[30000279, 60]]),
        "needCoins": _tools.ROList([30000002, 200000]),
        "needLevel": 30
    }),
    5: _tools.RODict({
        "ID": 5,
        "prop0": None,
        "prop1001": _tools.ROList([['adjMaxMagicAtk', 6], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1002": _tools.ROList([['adjMaxMagicAtk', 6], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1003": _tools.ROList([['adjMaxPhysicalAtk', 6], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "needItems": _tools.ROList([[30000279, 120]]),
        "needCoins": _tools.ROList([30000002, 500000]),
        "needLevel": 33
    }),
    6: _tools.RODict({
        "ID": 6,
        "prop0": None,
        "prop1001": _tools.ROList([['adjMaxMagicAtk', 6], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1002": _tools.ROList([['adjMaxMagicAtk', 6], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1003": _tools.ROList([['adjMaxPhysicalAtk', 6], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "needItems": _tools.ROList([[30000280, 15]]),
        "needCoins": _tools.ROList([30000002, 900000]),
        "needLevel": 35
    }),
    7: _tools.RODict({
        "ID": 7,
        "prop0": None,
        "prop1001": _tools.ROList([['adjMaxMagicAtk', 7], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1002": _tools.ROList([['adjMaxMagicAtk', 7], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1003": _tools.ROList([['adjMaxPhysicalAtk', 7], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "needItems": _tools.ROList([[30000280, 35]]),
        "needCoins": _tools.ROList([30000002, 1600000]),
        "needLevel": 37
    }),
    8: _tools.RODict({
        "ID": 8,
        "prop0": None,
        "prop1001": _tools.ROList([['adjMaxMagicAtk', 7], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1002": _tools.ROList([['adjMaxMagicAtk', 7], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1003": _tools.ROList([['adjMaxPhysicalAtk', 7], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "needItems": _tools.ROList([[30000280, 55]]),
        "needCoins": _tools.ROList([30000002, 3000000]),
        "needLevel": 40
    }),
    9: _tools.RODict({
        "ID": 9,
        "prop0": None,
        "prop1001": _tools.ROList([['adjMaxMagicAtk', 8], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1002": _tools.ROList([['adjMaxMagicAtk', 8], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1003": _tools.ROList([['adjMaxPhysicalAtk', 8], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "needItems": _tools.ROList([[30000280, 115]]),
        "needCoins": _tools.ROList([30000002, 5000000]),
        "needLevel": 42
    }),
    10: _tools.RODict({
        "ID": 10,
        "prop0": None,
        "prop1001": _tools.ROList([['adjMaxMagicAtk', 8], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1002": _tools.ROList([['adjMaxMagicAtk', 8], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1003": _tools.ROList([['adjMaxPhysicalAtk', 8], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "needItems": _tools.ROList([[30000280, 150]]),
        "needCoins": _tools.ROList([30000002, 9000000]),
        "needLevel": 45
    }),
    11: _tools.RODict({
        "ID": 11,
        "prop0": None,
        "prop1001": _tools.ROList([['adjMaxMagicAtk', 9], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1002": _tools.ROList([['adjMaxMagicAtk', 9], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1003": _tools.ROList([['adjMaxPhysicalAtk', 9], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "needItems": _tools.ROList([[30000281, 20]]),
        "needCoins": _tools.ROList([30000002, 13000000]),
        "needLevel": 47
    }),
    12: _tools.RODict({
        "ID": 12,
        "prop0": None,
        "prop1001": _tools.ROList([['adjMaxMagicAtk', 9], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1002": _tools.ROList([['adjMaxMagicAtk', 9], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1003": _tools.ROList([['adjMaxPhysicalAtk', 9], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "needItems": _tools.ROList([[30000281, 30]]),
        "needCoins": _tools.ROList([30000002, 18000000]),
        "needLevel": 49
    }),
    13: _tools.RODict({
        "ID": 13,
        "prop0": None,
        "prop1001": _tools.ROList([['adjMaxMagicAtk', 10], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1002": _tools.ROList([['adjMaxMagicAtk', 10], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1003": _tools.ROList([['adjMaxPhysicalAtk', 10], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "needItems": _tools.ROList([[30000281, 35]]),
        "needCoins": _tools.ROList([30000002, 24000000]),
        "needLevel": 51
    }),
    14: _tools.RODict({
        "ID": 14,
        "prop0": None,
        "prop1001": _tools.ROList([['adjMaxMagicAtk', 10], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1002": _tools.ROList([['adjMaxMagicAtk', 10], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1003": _tools.ROList([['adjMaxPhysicalAtk', 10], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "needItems": _tools.ROList([[30000281, 40]]),
        "needCoins": _tools.ROList([30000002, 30000000]),
        "needLevel": 55
    }),
    15: _tools.RODict({
        "ID": 15,
        "prop0": None,
        "prop1001": _tools.ROList([['adjMaxMagicAtk', 10], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1002": _tools.ROList([['adjMaxMagicAtk', 10], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1003": _tools.ROList([['adjMaxPhysicalAtk', 10], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "needItems": _tools.ROList([[30000281, 55]]),
        "needCoins": _tools.ROList([30000002, 36000000]),
        "needLevel": 60
    }),
    16: _tools.RODict({
        "ID": 16,
        "prop0": None,
        "prop1001": _tools.ROList([['adjMaxMagicAtk', 10], ['adjMortal', 0.04], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1002": _tools.ROList([['adjMaxMagicAtk', 10], ['adjMortal', 0.04], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1003": _tools.ROList([['adjMaxPhysicalAtk', 10], ['adjMortal', 0.04], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "needItems": _tools.ROList([[30000282, 7]]),
        "needCoins": _tools.ROList([30000002, 45000000]),
        "needLevel": 62
    }),
    17: _tools.RODict({
        "ID": 17,
        "prop0": None,
        "prop1001": _tools.ROList([['adjMaxMagicAtk', 10], ['adjMortal', 0.04], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1002": _tools.ROList([['adjMaxMagicAtk', 10], ['adjMortal', 0.04], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1003": _tools.ROList([['adjMaxPhysicalAtk', 10], ['adjMortal', 0.04], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "needItems": _tools.ROList([[30000282, 8]]),
        "needCoins": _tools.ROList([30000002, 55000000]),
        "needLevel": 64
    }),
    18: _tools.RODict({
        "ID": 18,
        "prop0": None,
        "prop1001": _tools.ROList([['adjMaxMagicAtk', 10], ['adjMortal', 0.04], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1002": _tools.ROList([['adjMaxMagicAtk', 10], ['adjMortal', 0.04], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1003": _tools.ROList([['adjMaxPhysicalAtk', 10], ['adjMortal', 0.04], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "needItems": _tools.ROList([[30000282, 9]]),
        "needCoins": _tools.ROList([30000002, 65000000]),
        "needLevel": 66
    }),
    19: _tools.RODict({
        "ID": 19,
        "prop0": None,
        "prop1001": _tools.ROList([['adjMaxMagicAtk', 10], ['adjMortal', 0.04], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1002": _tools.ROList([['adjMaxMagicAtk', 10], ['adjMortal', 0.04], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1003": _tools.ROList([['adjMaxPhysicalAtk', 10], ['adjMortal', 0.04], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "needItems": _tools.ROList([[30000282, 10]]),
        "needCoins": _tools.ROList([30000002, 80000000]),
        "needLevel": 68
    }),
    20: _tools.RODict({
        "ID": 20,
        "prop0": None,
        "prop1001": _tools.ROList([['adjMaxMagicAtk', 10], ['adjMortal', 0.04], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1002": _tools.ROList([['adjMaxMagicAtk', 10], ['adjMortal', 0.04], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1003": _tools.ROList([['adjMaxPhysicalAtk', 10], ['adjMortal', 0.04], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "needItems": _tools.ROList([[30000282, 12]]),
        "needCoins": _tools.ROList([30000002, 100000000]),
        "needLevel": 70
    })
})
minKey = 1
maxKey = 20