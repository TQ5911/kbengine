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
        "needItems": _tools.ROList([[30000279, 15]]),
        "needCoins": _tools.ROList([30000002, 100000]),
        "needLevel": 0
    }),
    3: _tools.RODict({
        "ID": 3,
        "prop0": None,
        "prop1001": _tools.ROList([['adjMaxMagicAtk', 5], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1002": _tools.ROList([['adjMaxMagicAtk', 5], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1003": _tools.ROList([['adjMaxPhysicalAtk', 5], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "needItems": _tools.ROList([[30000279, 25]]),
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
        "needCoins": _tools.ROList([30000002, 300000]),
        "needLevel": 30
    }),
    5: _tools.RODict({
        "ID": 5,
        "prop0": None,
        "prop1001": _tools.ROList([['adjMaxMagicAtk', 6], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1002": _tools.ROList([['adjMaxMagicAtk', 6], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1003": _tools.ROList([['adjMaxPhysicalAtk', 6], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "needItems": _tools.ROList([[30000279, 120]]),
        "needCoins": _tools.ROList([30000002, 600000]),
        "needLevel": 33
    }),
    6: _tools.RODict({
        "ID": 6,
        "prop0": None,
        "prop1001": _tools.ROList([['adjMaxMagicAtk', 6], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1002": _tools.ROList([['adjMaxMagicAtk', 6], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1003": _tools.ROList([['adjMaxPhysicalAtk', 6], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "needItems": _tools.ROList([[30000280, 18]]),
        "needCoins": _tools.ROList([30000002, 1000000]),
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
        "needLevel": 43
    }),
    10: _tools.RODict({
        "ID": 10,
        "prop0": None,
        "prop1001": _tools.ROList([['adjMaxMagicAtk', 8], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1002": _tools.ROList([['adjMaxMagicAtk', 8], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1003": _tools.ROList([['adjMaxPhysicalAtk', 8], ['adjFatal', 1], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "needItems": _tools.ROList([[30000280, 150]]),
        "needCoins": _tools.ROList([30000002, 10000000]),
        "needLevel": 45
    }),
    11: _tools.RODict({
        "ID": 11,
        "prop0": None,
        "prop1001": _tools.ROList([['adjMaxMagicAtk', 9], ['adjFullHp', 250], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1002": _tools.ROList([['adjMaxMagicAtk', 9], ['adjFullHp', 250], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1003": _tools.ROList([['adjMaxPhysicalAtk', 9], ['adjFullHp', 250], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "needItems": _tools.ROList([[30000281, 20]]),
        "needCoins": _tools.ROList([30000002, 15000000]),
        "needLevel": 47
    }),
    12: _tools.RODict({
        "ID": 12,
        "prop0": None,
        "prop1001": _tools.ROList([['adjMaxMagicAtk', 9], ['adjFullHp', 300], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1002": _tools.ROList([['adjMaxMagicAtk', 9], ['adjFullHp', 300], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1003": _tools.ROList([['adjMaxPhysicalAtk', 9], ['adjFullHp', 300], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "needItems": _tools.ROList([[30000281, 30]]),
        "needCoins": _tools.ROList([30000002, 20000000]),
        "needLevel": 50
    }),
    13: _tools.RODict({
        "ID": 13,
        "prop0": None,
        "prop1001": _tools.ROList([['adjMaxMagicAtk', 10], ['adjFullHp', 350], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1002": _tools.ROList([['adjMaxMagicAtk', 10], ['adjFullHp', 350], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1003": _tools.ROList([['adjMaxPhysicalAtk', 10], ['adjFullHp', 350], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "needItems": _tools.ROList([[30000281, 35]]),
        "needCoins": _tools.ROList([30000002, 30000000]),
        "needLevel": 53
    }),
    14: _tools.RODict({
        "ID": 14,
        "prop0": None,
        "prop1001": _tools.ROList([['adjMaxMagicAtk', 10], ['adjFullHp', 400], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1002": _tools.ROList([['adjMaxMagicAtk', 10], ['adjFullHp', 400], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1003": _tools.ROList([['adjMaxPhysicalAtk', 10], ['adjFullHp', 400], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "needItems": _tools.ROList([[30000281, 40]]),
        "needCoins": _tools.ROList([30000002, 40000000]),
        "needLevel": 55
    }),
    15: _tools.RODict({
        "ID": 15,
        "prop0": None,
        "prop1001": _tools.ROList([['adjMaxMagicAtk', 10], ['adjFullHp', 450], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1002": _tools.ROList([['adjMaxMagicAtk', 10], ['adjFullHp', 450], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1003": _tools.ROList([['adjMaxPhysicalAtk', 10], ['adjFullHp', 450], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "needItems": _tools.ROList([[30000281, 55]]),
        "needCoins": _tools.ROList([30000002, 50000000]),
        "needLevel": 60
    }),
    16: _tools.RODict({
        "ID": 16,
        "prop0": None,
        "prop1001": _tools.ROList([['adjMaxMagicAtk', 10], ['adjFullHp', 500], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1002": _tools.ROList([['adjMaxMagicAtk', 10], ['adjFullHp', 500], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1003": _tools.ROList([['adjMaxPhysicalAtk', 10], ['adjFullHp', 500], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "needItems": _tools.ROList([[30000282, 7]]),
        "needCoins": _tools.ROList([30000002, 60000000]),
        "needLevel": 62
    }),
    17: _tools.RODict({
        "ID": 17,
        "prop0": None,
        "prop1001": _tools.ROList([['adjMaxMagicAtk', 10], ['adjFullHp', 550], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1002": _tools.ROList([['adjMaxMagicAtk', 10], ['adjFullHp', 550], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1003": _tools.ROList([['adjMaxPhysicalAtk', 10], ['adjFullHp', 550], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "needItems": _tools.ROList([[30000282, 8]]),
        "needCoins": _tools.ROList([30000002, 75000000]),
        "needLevel": 65
    }),
    18: _tools.RODict({
        "ID": 18,
        "prop0": None,
        "prop1001": _tools.ROList([['adjMaxMagicAtk', 10], ['adjFullHp', 600], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1002": _tools.ROList([['adjMaxMagicAtk', 10], ['adjFullHp', 600], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1003": _tools.ROList([['adjMaxPhysicalAtk', 10], ['adjFullHp', 600], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "needItems": _tools.ROList([[30000282, 9]]),
        "needCoins": _tools.ROList([30000002, 90000000]),
        "needLevel": 67
    }),
    19: _tools.RODict({
        "ID": 19,
        "prop0": None,
        "prop1001": _tools.ROList([['adjMaxMagicAtk', 10], ['adjFullHp', 650], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1002": _tools.ROList([['adjMaxMagicAtk', 10], ['adjFullHp', 650], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1003": _tools.ROList([['adjMaxPhysicalAtk', 10], ['adjFullHp', 650], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "needItems": _tools.ROList([[30000282, 10]]),
        "needCoins": _tools.ROList([30000002, 110000000]),
        "needLevel": 70
    }),
    20: _tools.RODict({
        "ID": 20,
        "prop0": None,
        "prop1001": _tools.ROList([['adjMaxMagicAtk', 10], ['adjFullHp', 700], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1002": _tools.ROList([['adjMaxMagicAtk', 10], ['adjFullHp', 700], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "prop1003": _tools.ROList([['adjMaxPhysicalAtk', 10], ['adjFullHp', 700], ['adjAccuracy', 1], ['adjEvasion', 1], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01], ['adjCopper', 0.015], ['adjExpGrow', 0.015]]),
        "needItems": _tools.ROList([[30000282, 12]]),
        "needCoins": _tools.ROList([30000002, 130000000]),
        "needLevel": 72
    })
})
minKey = 1
maxKey = 20