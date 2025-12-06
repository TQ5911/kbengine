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
        "prop": _tools.RODict({1001:51004001,1002:51004001,1003:51004001}),
        "prop0": None,
        "prop1001": _tools.ROList([['adjMinMagicArmor', 160], ['adjMaxMagicAtk', 15], ['adjMinMagicAtk', 7], ['adjHit', 2], ['adjDodge', 2], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01]]),
        "prop1002": _tools.ROList([['adjMinMagicArmor', 160], ['adjMaxMagicAtk', 15], ['adjMinMagicAtk', 7], ['adjHit', 2], ['adjDodge', 2], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01]]),
        "prop1003": _tools.ROList([['adjMinMagicArmor', 160], ['adjMaxPhysicalAtk', 15], ['adjMinPhysicalAtk', 7], ['adjHit', 2], ['adjDodge', 2], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01]]),
        "needItems": _tools.ROList([[30000279, 10]]),
        "needCoins": _tools.ROList([30000002, 10000])
    }),
    2: _tools.RODict({
        "ID": 2,
        "prop": _tools.RODict({1001:51004001,1002:51004001,1003:51004001}),
        "prop0": None,
        "prop1001": _tools.ROList([['adjMinMagicArmor', 320], ['adjMaxMagicAtk', 30], ['adjMinMagicAtk', 14], ['adjHit', 4], ['adjDodge', 4], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01]]),
        "prop1002": _tools.ROList([['adjMinMagicArmor', 320], ['adjMaxMagicAtk', 30], ['adjMinMagicAtk', 14], ['adjHit', 4], ['adjDodge', 4], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01]]),
        "prop1003": _tools.ROList([['adjMinMagicArmor', 320], ['adjMaxPhysicalAtk', 30], ['adjMinPhysicalAtk', 14], ['adjHit', 4], ['adjDodge', 4], ['adjMonsterDmg', 0.01], ['adjMonsterDmgAnti', 0.01]]),
        "needItems": _tools.ROList([[30000279, 15]]),
        "needCoins": _tools.ROList([30000002, 20000])
    }),
    3: _tools.RODict({
        "ID": 3,
        "prop": _tools.RODict({1001:51004001,1002:51004001,1003:51004001}),
        "prop0": None,
        "prop1001": _tools.ROList([['adjMinMagicArmor', 480], ['adjMaxMagicAtk', 45], ['adjMinMagicAtk', 21], ['adjHit', 6], ['adjDodge', 6], ['adjMonsterDmg', 0.02], ['adjMonsterDmgAnti', 0.02]]),
        "prop1002": _tools.ROList([['adjMinMagicArmor', 480], ['adjMaxMagicAtk', 45], ['adjMinMagicAtk', 21], ['adjHit', 6], ['adjDodge', 6], ['adjMonsterDmg', 0.02], ['adjMonsterDmgAnti', 0.02]]),
        "prop1003": _tools.ROList([['adjMinMagicArmor', 480], ['adjMaxPhysicalAtk', 45], ['adjMinPhysicalAtk', 21], ['adjHit', 6], ['adjDodge', 6], ['adjMonsterDmg', 0.02], ['adjMonsterDmgAnti', 0.02]]),
        "needItems": _tools.ROList([[30000279, 20]]),
        "needCoins": _tools.ROList([30000002, 30000])
    }),
    4: _tools.RODict({
        "ID": 4,
        "prop": _tools.RODict({1001:51004001,1002:51004001,1003:51004001}),
        "prop0": None,
        "prop1001": _tools.ROList([['adjMinMagicArmor', 720], ['adjMaxMagicAtk', 60], ['adjMinMagicAtk', 28], ['adjHit', 8], ['adjDodge', 8], ['adjMonsterDmg', 0.02], ['adjMonsterDmgAnti', 0.02]]),
        "prop1002": _tools.ROList([['adjMinMagicArmor', 720], ['adjMaxMagicAtk', 60], ['adjMinMagicAtk', 28], ['adjHit', 8], ['adjDodge', 8], ['adjMonsterDmg', 0.02], ['adjMonsterDmgAnti', 0.02]]),
        "prop1003": _tools.ROList([['adjMinMagicArmor', 720], ['adjMaxPhysicalAtk', 60], ['adjMinPhysicalAtk', 28], ['adjHit', 8], ['adjDodge', 8], ['adjMonsterDmg', 0.02], ['adjMonsterDmgAnti', 0.02]]),
        "needItems": _tools.ROList([[30000280, 5]]),
        "needCoins": _tools.ROList([30000002, 75000])
    }),
    5: _tools.RODict({
        "ID": 5,
        "prop": _tools.RODict({1001:51004001,1002:51004001,1003:51004001}),
        "prop0": None,
        "prop1001": _tools.ROList([['adjMinMagicArmor', 960], ['adjMaxMagicAtk', 75], ['adjMinMagicAtk', 35], ['adjHit', 10], ['adjDodge', 10], ['adjMonsterDmg', 0.03], ['adjMonsterDmgAnti', 0.03]]),
        "prop1002": _tools.ROList([['adjMinMagicArmor', 960], ['adjMaxMagicAtk', 75], ['adjMinMagicAtk', 35], ['adjHit', 10], ['adjDodge', 10], ['adjMonsterDmg', 0.03], ['adjMonsterDmgAnti', 0.03]]),
        "prop1003": _tools.ROList([['adjMinMagicArmor', 960], ['adjMaxPhysicalAtk', 75], ['adjMinPhysicalAtk', 35], ['adjHit', 10], ['adjDodge', 10], ['adjMonsterDmg', 0.03], ['adjMonsterDmgAnti', 0.03]]),
        "needItems": _tools.ROList([[30000280, 15]]),
        "needCoins": _tools.ROList([30000002, 100000])
    }),
    6: _tools.RODict({
        "ID": 6,
        "prop": _tools.RODict({1001:51004001,1002:51004001,1003:51004001}),
        "prop0": None,
        "prop1001": _tools.ROList([['adjMinMagicArmor', 1200], ['adjMaxMagicAtk', 90], ['adjMinMagicAtk', 42], ['adjHit', 12], ['adjDodge', 12], ['adjMonsterDmg', 0.03], ['adjMonsterDmgAnti', 0.03]]),
        "prop1002": _tools.ROList([['adjMinMagicArmor', 1200], ['adjMaxMagicAtk', 90], ['adjMinMagicAtk', 42], ['adjHit', 12], ['adjDodge', 12], ['adjMonsterDmg', 0.03], ['adjMonsterDmgAnti', 0.03]]),
        "prop1003": _tools.ROList([['adjMinMagicArmor', 1200], ['adjMaxPhysicalAtk', 90], ['adjMinPhysicalAtk', 42], ['adjHit', 12], ['adjDodge', 12], ['adjMonsterDmg', 0.03], ['adjMonsterDmgAnti', 0.03]]),
        "needItems": _tools.ROList([[30000280, 25]]),
        "needCoins": _tools.ROList([30000002, 300000])
    }),
    7: _tools.RODict({
        "ID": 7,
        "prop": _tools.RODict({1001:51004001,1002:51004001,1003:51004001}),
        "prop0": None,
        "prop1001": _tools.ROList([['adjMinMagicArmor', 1520], ['adjMaxMagicAtk', 105], ['adjMinMagicAtk', 49], ['adjHit', 14], ['adjDodge', 14], ['adjMonsterDmg', 0.04], ['adjMonsterDmgAnti', 0.04]]),
        "prop1002": _tools.ROList([['adjMinMagicArmor', 1520], ['adjMaxMagicAtk', 105], ['adjMinMagicAtk', 49], ['adjHit', 14], ['adjDodge', 14], ['adjMonsterDmg', 0.04], ['adjMonsterDmgAnti', 0.04]]),
        "prop1003": _tools.ROList([['adjMinMagicArmor', 1520], ['adjMaxPhysicalAtk', 105], ['adjMinPhysicalAtk', 49], ['adjHit', 14], ['adjDodge', 14], ['adjMonsterDmg', 0.04], ['adjMonsterDmgAnti', 0.04]]),
        "needItems": _tools.ROList([[30000280, 35]]),
        "needCoins": _tools.ROList([30000002, 500000])
    }),
    8: _tools.RODict({
        "ID": 8,
        "prop": _tools.RODict({1001:51004001,1002:51004001,1003:51004001}),
        "prop0": None,
        "prop1001": _tools.ROList([['adjMinMagicArmor', 1840], ['adjMaxMagicAtk', 120], ['adjMinMagicAtk', 56], ['adjHit', 16], ['adjDodge', 16], ['adjMonsterDmg', 0.04], ['adjMonsterDmgAnti', 0.04]]),
        "prop1002": _tools.ROList([['adjMinMagicArmor', 1840], ['adjMaxMagicAtk', 120], ['adjMinMagicAtk', 56], ['adjHit', 16], ['adjDodge', 16], ['adjMonsterDmg', 0.04], ['adjMonsterDmgAnti', 0.04]]),
        "prop1003": _tools.ROList([['adjMinMagicArmor', 1840], ['adjMaxPhysicalAtk', 120], ['adjMinPhysicalAtk', 56], ['adjHit', 16], ['adjDodge', 16], ['adjMonsterDmg', 0.04], ['adjMonsterDmgAnti', 0.04]]),
        "needItems": _tools.ROList([[30000281, 10]]),
        "needCoins": _tools.ROList([30000002, 1750000])
    }),
    9: _tools.RODict({
        "ID": 9,
        "prop": _tools.RODict({1001:51004001,1002:51004001,1003:51004001}),
        "prop0": None,
        "prop1001": _tools.ROList([['adjMinMagicArmor', 2160], ['adjMaxMagicAtk', 135], ['adjMinMagicAtk', 63], ['adjHit', 18], ['adjDodge', 18], ['adjMonsterDmg', 0.05], ['adjMonsterDmgAnti', 0.05]]),
        "prop1002": _tools.ROList([['adjMinMagicArmor', 2160], ['adjMaxMagicAtk', 135], ['adjMinMagicAtk', 63], ['adjHit', 18], ['adjDodge', 18], ['adjMonsterDmg', 0.05], ['adjMonsterDmgAnti', 0.05]]),
        "prop1003": _tools.ROList([['adjMinMagicArmor', 2160], ['adjMaxPhysicalAtk', 135], ['adjMinPhysicalAtk', 63], ['adjHit', 18], ['adjDodge', 18], ['adjMonsterDmg', 0.05], ['adjMonsterDmgAnti', 0.05]]),
        "needItems": _tools.ROList([[30000281, 20]]),
        "needCoins": _tools.ROList([30000002, 2500000])
    }),
    10: _tools.RODict({
        "ID": 10,
        "prop": _tools.RODict({1001:51004001,1002:51004001,1003:51004001}),
        "prop0": None,
        "prop1001": _tools.ROList([['adjMinMagicArmor', 2560], ['adjMaxMagicAtk', 150], ['adjMinMagicAtk', 70], ['adjHit', 20], ['adjDodge', 20], ['adjMonsterDmg', 0.05], ['adjMonsterDmgAnti', 0.05]]),
        "prop1002": _tools.ROList([['adjMinMagicArmor', 2560], ['adjMaxMagicAtk', 150], ['adjMinMagicAtk', 70], ['adjHit', 20], ['adjDodge', 20], ['adjMonsterDmg', 0.05], ['adjMonsterDmgAnti', 0.05]]),
        "prop1003": _tools.ROList([['adjMinMagicArmor', 2560], ['adjMaxPhysicalAtk', 150], ['adjMinPhysicalAtk', 70], ['adjHit', 20], ['adjDodge', 20], ['adjMonsterDmg', 0.05], ['adjMonsterDmgAnti', 0.05]]),
        "needItems": _tools.ROList([[30000281, 35]]),
        "needCoins": _tools.ROList([30000002, 3000000])
    }),
    11: _tools.RODict({
        "ID": 11,
        "prop": _tools.RODict({1001:51004001,1002:51004001,1003:51004001}),
        "prop0": None,
        "prop1001": _tools.ROList([['adjMinMagicArmor', 2960], ['adjMaxMagicAtk', 165], ['adjMinMagicAtk', 77], ['adjHit', 22], ['adjDodge', 22], ['adjMonsterDmg', 0.06], ['adjMonsterDmgAnti', 0.06]]),
        "prop1002": _tools.ROList([['adjMinMagicArmor', 2960], ['adjMaxMagicAtk', 165], ['adjMinMagicAtk', 77], ['adjHit', 22], ['adjDodge', 22], ['adjMonsterDmg', 0.06], ['adjMonsterDmgAnti', 0.06]]),
        "prop1003": _tools.ROList([['adjMinMagicArmor', 2960], ['adjMaxPhysicalAtk', 165], ['adjMinPhysicalAtk', 77], ['adjHit', 22], ['adjDodge', 22], ['adjMonsterDmg', 0.06], ['adjMonsterDmgAnti', 0.06]]),
        "needItems": _tools.ROList([[30000282, 3]]),
        "needCoins": _tools.ROList([30000002, 4000000])
    }),
    12: _tools.RODict({
        "ID": 12,
        "prop": _tools.RODict({1001:51004001,1002:51004001,1003:51004001}),
        "prop0": None,
        "prop1001": _tools.ROList([['adjMinMagicArmor', 3360], ['adjMaxMagicAtk', 180], ['adjMinMagicAtk', 84], ['adjHit', 24], ['adjDodge', 24], ['adjMonsterDmg', 0.06], ['adjMonsterDmgAnti', 0.06]]),
        "prop1002": _tools.ROList([['adjMinMagicArmor', 3360], ['adjMaxMagicAtk', 180], ['adjMinMagicAtk', 84], ['adjHit', 24], ['adjDodge', 24], ['adjMonsterDmg', 0.06], ['adjMonsterDmgAnti', 0.06]]),
        "prop1003": _tools.ROList([['adjMinMagicArmor', 3360], ['adjMaxPhysicalAtk', 180], ['adjMinPhysicalAtk', 84], ['adjHit', 24], ['adjDodge', 24], ['adjMonsterDmg', 0.06], ['adjMonsterDmgAnti', 0.06]]),
        "needItems": _tools.ROList([[30000282, 5]]),
        "needCoins": _tools.ROList([30000002, 5000000])
    }),
    13: _tools.RODict({
        "ID": 13,
        "prop": _tools.RODict({1001:51004001,1002:51004001,1003:51004001}),
        "prop0": None,
        "prop1001": _tools.ROList([['adjMinMagicArmor', 3840], ['adjMaxMagicAtk', 195], ['adjMinMagicAtk', 91], ['adjHit', 26], ['adjDodge', 26], ['adjMonsterDmg', 0.07], ['adjMonsterDmgAnti', 0.07]]),
        "prop1002": _tools.ROList([['adjMinMagicArmor', 3840], ['adjMaxMagicAtk', 195], ['adjMinMagicAtk', 91], ['adjHit', 26], ['adjDodge', 26], ['adjMonsterDmg', 0.07], ['adjMonsterDmgAnti', 0.07]]),
        "prop1003": _tools.ROList([['adjMinMagicArmor', 3840], ['adjMaxPhysicalAtk', 195], ['adjMinPhysicalAtk', 91], ['adjHit', 26], ['adjDodge', 26], ['adjMonsterDmg', 0.07], ['adjMonsterDmgAnti', 0.07]]),
        "needItems": _tools.ROList([[30000282, 6]]),
        "needCoins": _tools.ROList([30000002, 6000000])
    }),
    14: _tools.RODict({
        "ID": 14,
        "prop": _tools.RODict({1001:51004001,1002:51004001,1003:51004001}),
        "prop0": None,
        "prop1001": _tools.ROList([['adjMinMagicArmor', 4320], ['adjMaxMagicAtk', 210], ['adjMinMagicAtk', 98], ['adjHit', 28], ['adjDodge', 28], ['adjMonsterDmg', 0.07], ['adjMonsterDmgAnti', 0.07]]),
        "prop1002": _tools.ROList([['adjMinMagicArmor', 4320], ['adjMaxMagicAtk', 210], ['adjMinMagicAtk', 98], ['adjHit', 28], ['adjDodge', 28], ['adjMonsterDmg', 0.07], ['adjMonsterDmgAnti', 0.07]]),
        "prop1003": _tools.ROList([['adjMinMagicArmor', 4320], ['adjMaxPhysicalAtk', 210], ['adjMinPhysicalAtk', 98], ['adjHit', 28], ['adjDodge', 28], ['adjMonsterDmg', 0.07], ['adjMonsterDmgAnti', 0.07]]),
        "needItems": _tools.ROList([[30000282, 7]]),
        "needCoins": _tools.ROList([30000002, 7500000])
    }),
    15: _tools.RODict({
        "ID": 15,
        "prop": _tools.RODict({1001:51004001,1002:51004001,1003:51004001}),
        "prop0": None,
        "prop1001": _tools.ROList([['adjMinMagicArmor', 4800], ['adjMaxMagicAtk', 225], ['adjMinMagicAtk', 105], ['adjHit', 30], ['adjDodge', 30], ['adjMonsterDmg', 0.08], ['adjMonsterDmgAnti', 0.08]]),
        "prop1002": _tools.ROList([['adjMinMagicArmor', 4800], ['adjMaxMagicAtk', 225], ['adjMinMagicAtk', 105], ['adjHit', 30], ['adjDodge', 30], ['adjMonsterDmg', 0.08], ['adjMonsterDmgAnti', 0.08]]),
        "prop1003": _tools.ROList([['adjMinMagicArmor', 4800], ['adjMaxPhysicalAtk', 225], ['adjMinPhysicalAtk', 105], ['adjHit', 30], ['adjDodge', 30], ['adjMonsterDmg', 0.08], ['adjMonsterDmgAnti', 0.08]]),
        "needItems": _tools.ROList([[30000282, 8]]),
        "needCoins": _tools.ROList([30000002, 9000000])
    }),
    16: _tools.RODict({
        "ID": 16,
        "prop": _tools.RODict({1001:51004001,1002:51004001,1003:51004001}),
        "prop0": None,
        "prop1001": _tools.ROList([['adjMinMagicArmor', 5360], ['adjMaxMagicAtk', 240], ['adjMinMagicAtk', 112], ['adjHit', 32], ['adjDodge', 32], ['adjMonsterDmg', 0.08], ['adjMonsterDmgAnti', 0.08]]),
        "prop1002": _tools.ROList([['adjMinMagicArmor', 5360], ['adjMaxMagicAtk', 240], ['adjMinMagicAtk', 112], ['adjHit', 32], ['adjDodge', 32], ['adjMonsterDmg', 0.08], ['adjMonsterDmgAnti', 0.08]]),
        "prop1003": _tools.ROList([['adjMinMagicArmor', 5360], ['adjMaxPhysicalAtk', 240], ['adjMinPhysicalAtk', 112], ['adjHit', 32], ['adjDodge', 32], ['adjMonsterDmg', 0.08], ['adjMonsterDmgAnti', 0.08]]),
        "needItems": _tools.ROList([[30000282, 10]]),
        "needCoins": _tools.ROList([30000002, 10000000])
    }),
    17: _tools.RODict({
        "ID": 17,
        "prop": _tools.RODict({1001:51004001,1002:51004001,1003:51004001}),
        "prop0": None,
        "prop1001": _tools.ROList([['adjMinMagicArmor', 5920], ['adjMaxMagicAtk', 255], ['adjMinMagicAtk', 119], ['adjHit', 34], ['adjDodge', 34], ['adjMonsterDmg', 0.09], ['adjMonsterDmgAnti', 0.09]]),
        "prop1002": _tools.ROList([['adjMinMagicArmor', 5920], ['adjMaxMagicAtk', 255], ['adjMinMagicAtk', 119], ['adjHit', 34], ['adjDodge', 34], ['adjMonsterDmg', 0.09], ['adjMonsterDmgAnti', 0.09]]),
        "prop1003": _tools.ROList([['adjMinMagicArmor', 5920], ['adjMaxPhysicalAtk', 255], ['adjMinPhysicalAtk', 119], ['adjHit', 34], ['adjDodge', 34], ['adjMonsterDmg', 0.09], ['adjMonsterDmgAnti', 0.09]]),
        "needItems": _tools.ROList([[30000282, 12]]),
        "needCoins": _tools.ROList([30000002, 15000000])
    }),
    18: _tools.RODict({
        "ID": 18,
        "prop": _tools.RODict({1001:51004001,1002:51004001,1003:51004001}),
        "prop0": None,
        "prop1001": _tools.ROList([['adjMinMagicArmor', 6560], ['adjMaxMagicAtk', 270], ['adjMinMagicAtk', 126], ['adjHit', 36], ['adjDodge', 36], ['adjMonsterDmg', 0.09], ['adjMonsterDmgAnti', 0.09]]),
        "prop1002": _tools.ROList([['adjMinMagicArmor', 6560], ['adjMaxMagicAtk', 270], ['adjMinMagicAtk', 126], ['adjHit', 36], ['adjDodge', 36], ['adjMonsterDmg', 0.09], ['adjMonsterDmgAnti', 0.09]]),
        "prop1003": _tools.ROList([['adjMinMagicArmor', 6560], ['adjMaxPhysicalAtk', 270], ['adjMinPhysicalAtk', 126], ['adjHit', 36], ['adjDodge', 36], ['adjMonsterDmg', 0.09], ['adjMonsterDmgAnti', 0.09]]),
        "needItems": _tools.ROList([[30000282, 14]]),
        "needCoins": _tools.ROList([30000002, 20000000])
    }),
    19: _tools.RODict({
        "ID": 19,
        "prop": _tools.RODict({1001:51004001,1002:51004001,1003:51004001}),
        "prop0": None,
        "prop1001": _tools.ROList([['adjMinMagicArmor', 7280], ['adjMaxMagicAtk', 285], ['adjMinMagicAtk', 133], ['adjHit', 38], ['adjDodge', 38], ['adjMonsterDmg', 0.1], ['adjMonsterDmgAnti', 0.1]]),
        "prop1002": _tools.ROList([['adjMinMagicArmor', 7280], ['adjMaxMagicAtk', 285], ['adjMinMagicAtk', 133], ['adjHit', 38], ['adjDodge', 38], ['adjMonsterDmg', 0.1], ['adjMonsterDmgAnti', 0.1]]),
        "prop1003": _tools.ROList([['adjMinMagicArmor', 7280], ['adjMaxPhysicalAtk', 285], ['adjMinPhysicalAtk', 133], ['adjHit', 38], ['adjDodge', 38], ['adjMonsterDmg', 0.1], ['adjMonsterDmgAnti', 0.1]]),
        "needItems": _tools.ROList([[30000282, 16]]),
        "needCoins": _tools.ROList([30000002, 25000000])
    }),
    20: _tools.RODict({
        "ID": 20,
        "prop": _tools.RODict({1001:51004001,1002:51004001,1003:51004001}),
        "prop0": None,
        "prop1001": _tools.ROList([['adjMinMagicArmor', 8000], ['adjMaxMagicAtk', 300], ['adjMinMagicAtk', 140], ['adjHit', 40], ['adjDodge', 40], ['adjMonsterDmg', 0.1], ['adjMonsterDmgAnti', 0.1]]),
        "prop1002": _tools.ROList([['adjMinMagicArmor', 8000], ['adjMaxMagicAtk', 300], ['adjMinMagicAtk', 140], ['adjHit', 40], ['adjDodge', 40], ['adjMonsterDmg', 0.1], ['adjMonsterDmgAnti', 0.1]]),
        "prop1003": _tools.ROList([['adjMinMagicArmor', 8000], ['adjMaxPhysicalAtk', 300], ['adjMinPhysicalAtk', 140], ['adjHit', 40], ['adjDodge', 40], ['adjMonsterDmg', 0.1], ['adjMonsterDmgAnti', 0.1]]),
        "needItems": _tools.ROList([[30000282, 18]]),
        "needCoins": _tools.ROList([30000002, 30000000])
    })
})
minKey = 1
maxKey = 20