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
        "prop1001": _tools.ROList([['adjFullHp', 125], ['adjMaxMagicAtk', 2], ['adjMaxPhysicalArmor', 2], ['adjMaxMagicArmor', 2], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1002": _tools.ROList([['adjFullHp', 125], ['adjMaxMagicAtk', 2], ['adjMaxPhysicalArmor', 2], ['adjMaxMagicArmor', 2], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1003": _tools.ROList([['adjFullHp', 125], ['adjMaxPhysicalAtk', 2], ['adjMaxPhysicalArmor', 2], ['adjMaxMagicArmor', 2], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "needItems": _tools.ROList([[30000279, 10]]),
        "needCoins": _tools.ROList([30000002, 10000])
    }),
    2: _tools.RODict({
        "ID": 2,
        "prop0": None,
        "prop1001": _tools.ROList([['adjFullHp', 150], ['adjMaxMagicAtk', 2], ['adjMaxPhysicalArmor', 2], ['adjMaxMagicArmor', 2], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1002": _tools.ROList([['adjFullHp', 150], ['adjMaxMagicAtk', 2], ['adjMaxPhysicalArmor', 2], ['adjMaxMagicArmor', 2], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1003": _tools.ROList([['adjFullHp', 150], ['adjMaxPhysicalAtk', 2], ['adjMaxPhysicalArmor', 2], ['adjMaxMagicArmor', 2], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "needItems": _tools.ROList([[30000279, 15]]),
        "needCoins": _tools.ROList([30000002, 25000])
    }),
    3: _tools.RODict({
        "ID": 3,
        "prop0": None,
        "prop1001": _tools.ROList([['adjFullHp', 175], ['adjMaxMagicAtk', 3], ['adjMaxPhysicalArmor', 3], ['adjMaxMagicArmor', 3], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1002": _tools.ROList([['adjFullHp', 175], ['adjMaxMagicAtk', 3], ['adjMaxPhysicalArmor', 3], ['adjMaxMagicArmor', 3], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1003": _tools.ROList([['adjFullHp', 175], ['adjMaxPhysicalAtk', 3], ['adjMaxPhysicalArmor', 3], ['adjMaxMagicArmor', 3], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "needItems": _tools.ROList([[30000279, 20]]),
        "needCoins": _tools.ROList([30000002, 50000])
    }),
    4: _tools.RODict({
        "ID": 4,
        "prop0": None,
        "prop1001": _tools.ROList([['adjFullHp', 200], ['adjMaxMagicAtk', 3], ['adjMaxPhysicalArmor', 3], ['adjMaxMagicArmor', 3], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1002": _tools.ROList([['adjFullHp', 200], ['adjMaxMagicAtk', 3], ['adjMaxPhysicalArmor', 3], ['adjMaxMagicArmor', 3], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1003": _tools.ROList([['adjFullHp', 200], ['adjMaxPhysicalAtk', 3], ['adjMaxPhysicalArmor', 3], ['adjMaxMagicArmor', 3], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "needItems": _tools.ROList([[30000280, 8]]),
        "needCoins": _tools.ROList([30000002, 120000])
    }),
    5: _tools.RODict({
        "ID": 5,
        "prop0": None,
        "prop1001": _tools.ROList([['adjFullHp', 225], ['adjMaxMagicAtk', 4], ['adjMaxPhysicalArmor', 4], ['adjMaxMagicArmor', 4], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1002": _tools.ROList([['adjFullHp', 225], ['adjMaxMagicAtk', 4], ['adjMaxPhysicalArmor', 4], ['adjMaxMagicArmor', 4], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1003": _tools.ROList([['adjFullHp', 225], ['adjMaxPhysicalAtk', 4], ['adjMaxPhysicalArmor', 4], ['adjMaxMagicArmor', 4], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "needItems": _tools.ROList([[30000280, 15]]),
        "needCoins": _tools.ROList([30000002, 210000])
    }),
    6: _tools.RODict({
        "ID": 6,
        "prop0": None,
        "prop1001": _tools.ROList([['adjFullHp', 250], ['adjMaxMagicAtk', 4], ['adjMaxPhysicalArmor', 4], ['adjMaxMagicArmor', 4], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1002": _tools.ROList([['adjFullHp', 250], ['adjMaxMagicAtk', 4], ['adjMaxPhysicalArmor', 4], ['adjMaxMagicArmor', 4], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1003": _tools.ROList([['adjFullHp', 250], ['adjMaxPhysicalAtk', 4], ['adjMaxPhysicalArmor', 4], ['adjMaxMagicArmor', 4], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "needItems": _tools.ROList([[30000280, 20]]),
        "needCoins": _tools.ROList([30000002, 450000])
    }),
    7: _tools.RODict({
        "ID": 7,
        "prop0": None,
        "prop1001": _tools.ROList([['adjFullHp', 275], ['adjMaxMagicAtk', 5], ['adjMaxPhysicalArmor', 5], ['adjMaxMagicArmor', 5], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1002": _tools.ROList([['adjFullHp', 275], ['adjMaxMagicAtk', 5], ['adjMaxPhysicalArmor', 5], ['adjMaxMagicArmor', 5], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1003": _tools.ROList([['adjFullHp', 275], ['adjMaxPhysicalAtk', 5], ['adjMaxPhysicalArmor', 5], ['adjMaxMagicArmor', 5], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "needItems": _tools.ROList([[30000280, 30]]),
        "needCoins": _tools.ROList([30000002, 700000])
    }),
    8: _tools.RODict({
        "ID": 8,
        "prop0": None,
        "prop1001": _tools.ROList([['adjFullHp', 300], ['adjMaxMagicAtk', 5], ['adjMaxPhysicalArmor', 5], ['adjMaxMagicArmor', 5], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1002": _tools.ROList([['adjFullHp', 300], ['adjMaxMagicAtk', 5], ['adjMaxPhysicalArmor', 5], ['adjMaxMagicArmor', 5], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1003": _tools.ROList([['adjFullHp', 300], ['adjMaxPhysicalAtk', 5], ['adjMaxPhysicalArmor', 5], ['adjMaxMagicArmor', 5], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "needItems": _tools.ROList([[30000280, 50]]),
        "needCoins": _tools.ROList([30000002, 1300000])
    }),
    9: _tools.RODict({
        "ID": 9,
        "prop0": None,
        "prop1001": _tools.ROList([['adjFullHp', 325], ['adjMaxMagicAtk', 6], ['adjMaxPhysicalArmor', 6], ['adjMaxMagicArmor', 6], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1002": _tools.ROList([['adjFullHp', 325], ['adjMaxMagicAtk', 6], ['adjMaxPhysicalArmor', 6], ['adjMaxMagicArmor', 6], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1003": _tools.ROList([['adjFullHp', 325], ['adjMaxPhysicalAtk', 6], ['adjMaxPhysicalArmor', 6], ['adjMaxMagicArmor', 6], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "needItems": _tools.ROList([[30000281, 10]]),
        "needCoins": _tools.ROList([30000002, 2500000])
    }),
    10: _tools.RODict({
        "ID": 10,
        "prop0": None,
        "prop1001": _tools.ROList([['adjFullHp', 350], ['adjMaxMagicAtk', 6], ['adjMaxPhysicalArmor', 6], ['adjMaxMagicArmor', 6], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1002": _tools.ROList([['adjFullHp', 350], ['adjMaxMagicAtk', 6], ['adjMaxPhysicalArmor', 6], ['adjMaxMagicArmor', 6], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1003": _tools.ROList([['adjFullHp', 350], ['adjMaxPhysicalAtk', 6], ['adjMaxPhysicalArmor', 6], ['adjMaxMagicArmor', 6], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "needItems": _tools.ROList([[30000281, 15]]),
        "needCoins": _tools.ROList([30000002, 4000000])
    }),
    11: _tools.RODict({
        "ID": 11,
        "prop0": None,
        "prop1001": _tools.ROList([['adjFullHp', 375], ['adjMaxMagicAtk', 7], ['adjMaxPhysicalArmor', 7], ['adjMaxMagicArmor', 7], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1002": _tools.ROList([['adjFullHp', 375], ['adjMaxMagicAtk', 7], ['adjMaxPhysicalArmor', 7], ['adjMaxMagicArmor', 7], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1003": _tools.ROList([['adjFullHp', 375], ['adjMaxPhysicalAtk', 7], ['adjMaxPhysicalArmor', 7], ['adjMaxMagicArmor', 7], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "needItems": _tools.ROList([[30000281, 20]]),
        "needCoins": _tools.ROList([30000002, 5000000])
    }),
    12: _tools.RODict({
        "ID": 12,
        "prop0": None,
        "prop1001": _tools.ROList([['adjFullHp', 400], ['adjMaxMagicAtk', 7], ['adjMaxPhysicalArmor', 7], ['adjMaxMagicArmor', 7], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1002": _tools.ROList([['adjFullHp', 400], ['adjMaxMagicAtk', 7], ['adjMaxPhysicalArmor', 7], ['adjMaxMagicArmor', 7], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1003": _tools.ROList([['adjFullHp', 400], ['adjMaxPhysicalAtk', 7], ['adjMaxPhysicalArmor', 7], ['adjMaxMagicArmor', 7], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "needItems": _tools.ROList([[30000282, 2]]),
        "needCoins": _tools.ROList([30000002, 10000000])
    }),
    13: _tools.RODict({
        "ID": 13,
        "prop0": None,
        "prop1001": _tools.ROList([['adjFullHp', 425], ['adjMaxMagicAtk', 8], ['adjMaxPhysicalArmor', 8], ['adjMaxMagicArmor', 8], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1002": _tools.ROList([['adjFullHp', 425], ['adjMaxMagicAtk', 8], ['adjMaxPhysicalArmor', 8], ['adjMaxMagicArmor', 8], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1003": _tools.ROList([['adjFullHp', 425], ['adjMaxPhysicalAtk', 8], ['adjMaxPhysicalArmor', 8], ['adjMaxMagicArmor', 8], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "needItems": _tools.ROList([[30000282, 2]]),
        "needCoins": _tools.ROList([30000002, 10000000])
    }),
    14: _tools.RODict({
        "ID": 14,
        "prop0": None,
        "prop1001": _tools.ROList([['adjFullHp', 450], ['adjMaxMagicAtk', 8], ['adjMaxPhysicalArmor', 8], ['adjMaxMagicArmor', 8], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1002": _tools.ROList([['adjFullHp', 450], ['adjMaxMagicAtk', 8], ['adjMaxPhysicalArmor', 8], ['adjMaxMagicArmor', 8], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1003": _tools.ROList([['adjFullHp', 450], ['adjMaxPhysicalAtk', 8], ['adjMaxPhysicalArmor', 8], ['adjMaxMagicArmor', 8], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "needItems": _tools.ROList([[30000282, 3]]),
        "needCoins": _tools.ROList([30000002, 15000000])
    }),
    15: _tools.RODict({
        "ID": 15,
        "prop0": None,
        "prop1001": _tools.ROList([['adjFullHp', 475], ['adjMaxMagicAtk', 9], ['adjMaxPhysicalArmor', 9], ['adjMaxMagicArmor', 9], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1002": _tools.ROList([['adjFullHp', 475], ['adjMaxMagicAtk', 9], ['adjMaxPhysicalArmor', 9], ['adjMaxMagicArmor', 9], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1003": _tools.ROList([['adjFullHp', 475], ['adjMaxPhysicalAtk', 9], ['adjMaxPhysicalArmor', 9], ['adjMaxMagicArmor', 9], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "needItems": _tools.ROList([[30000282, 3]]),
        "needCoins": _tools.ROList([30000002, 15000000])
    }),
    16: _tools.RODict({
        "ID": 16,
        "prop0": None,
        "prop1001": _tools.ROList([['adjFullHp', 500], ['adjMaxMagicAtk', 9], ['adjMaxPhysicalArmor', 9], ['adjMaxMagicArmor', 9], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1002": _tools.ROList([['adjFullHp', 500], ['adjMaxMagicAtk', 9], ['adjMaxPhysicalArmor', 9], ['adjMaxMagicArmor', 9], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1003": _tools.ROList([['adjFullHp', 500], ['adjMaxPhysicalAtk', 9], ['adjMaxPhysicalArmor', 9], ['adjMaxMagicArmor', 9], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "needItems": _tools.ROList([[30000282, 4]]),
        "needCoins": _tools.ROList([30000002, 20000000])
    }),
    17: _tools.RODict({
        "ID": 17,
        "prop0": None,
        "prop1001": _tools.ROList([['adjFullHp', 525], ['adjMaxMagicAtk', 10], ['adjMaxPhysicalArmor', 10], ['adjMaxMagicArmor', 10], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1002": _tools.ROList([['adjFullHp', 525], ['adjMaxMagicAtk', 10], ['adjMaxPhysicalArmor', 10], ['adjMaxMagicArmor', 10], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1003": _tools.ROList([['adjFullHp', 525], ['adjMaxPhysicalAtk', 10], ['adjMaxPhysicalArmor', 10], ['adjMaxMagicArmor', 10], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "needItems": _tools.ROList([[30000282, 5]]),
        "needCoins": _tools.ROList([30000002, 25000000])
    }),
    18: _tools.RODict({
        "ID": 18,
        "prop0": None,
        "prop1001": _tools.ROList([['adjFullHp', 550], ['adjMaxMagicAtk', 10], ['adjMaxPhysicalArmor', 10], ['adjMaxMagicArmor', 10], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1002": _tools.ROList([['adjFullHp', 550], ['adjMaxMagicAtk', 10], ['adjMaxPhysicalArmor', 10], ['adjMaxMagicArmor', 10], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1003": _tools.ROList([['adjFullHp', 550], ['adjMaxPhysicalAtk', 10], ['adjMaxPhysicalArmor', 10], ['adjMaxMagicArmor', 10], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "needItems": _tools.ROList([[30000282, 6]]),
        "needCoins": _tools.ROList([30000002, 30000000])
    }),
    19: _tools.RODict({
        "ID": 19,
        "prop0": None,
        "prop1001": _tools.ROList([['adjFullHp', 575], ['adjMaxMagicAtk', 12], ['adjMaxPhysicalArmor', 12], ['adjMaxMagicArmor', 12], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1002": _tools.ROList([['adjFullHp', 575], ['adjMaxMagicAtk', 12], ['adjMaxPhysicalArmor', 12], ['adjMaxMagicArmor', 12], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1003": _tools.ROList([['adjFullHp', 575], ['adjMaxPhysicalAtk', 12], ['adjMaxPhysicalArmor', 12], ['adjMaxMagicArmor', 12], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "needItems": _tools.ROList([[30000282, 7]]),
        "needCoins": _tools.ROList([30000002, 35000000])
    }),
    20: _tools.RODict({
        "ID": 20,
        "prop0": None,
        "prop1001": _tools.ROList([['adjFullHp', 600], ['adjMaxMagicAtk', 12], ['adjMaxPhysicalArmor', 12], ['adjMaxMagicArmor', 12], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1002": _tools.ROList([['adjFullHp', 600], ['adjMaxMagicAtk', 12], ['adjMaxPhysicalArmor', 12], ['adjMaxMagicArmor', 12], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "prop1003": _tools.ROList([['adjFullHp', 600], ['adjMaxPhysicalAtk', 12], ['adjMaxPhysicalArmor', 12], ['adjMaxMagicArmor', 12], ['adjDodge', 1], ['adjMonsterDmg', 0.005], ['adjMonsterDmgAnti', 0.005]]),
        "needItems": _tools.ROList([[30000282, 8]]),
        "needCoins": _tools.ROList([30000002, 40000000])
    })
})
minKey = 1
maxKey = 20