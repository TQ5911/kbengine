# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: fightProp/uiAttrProp
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "fullHp": _tools.RODict({
        "ID": "fullHp",
        "showType": 1,
        "sort": 1
    }),
    "fullMp": _tools.RODict({
        "ID": "fullMp",
        "showType": 1,
        "sort": 2
    }),
    "minPhysicalAtk": _tools.RODict({
        "ID": "minPhysicalAtk",
        "showType": 1,
        "sort": 3
    }),
    "maxPhysicalAtk": _tools.RODict({
        "ID": "maxPhysicalAtk",
        "showType": 1,
        "sort": 4
    }),
    "minPhysicalArmor": _tools.RODict({
        "ID": "minPhysicalArmor",
        "showType": 1,
        "sort": 5
    }),
    "maxPhysicalArmor": _tools.RODict({
        "ID": "maxPhysicalArmor",
        "showType": 1,
        "sort": 6
    }),
    "minMagicAtk": _tools.RODict({
        "ID": "minMagicAtk",
        "showType": 1,
        "sort": 7
    }),
    "maxMagicAtk": _tools.RODict({
        "ID": "maxMagicAtk",
        "showType": 1,
        "sort": 8
    }),
    "minMagicArmor": _tools.RODict({
        "ID": "minMagicArmor",
        "showType": 1,
        "sort": 9
    }),
    "maxMagicArmor": _tools.RODict({
        "ID": "maxMagicArmor",
        "showType": 1,
        "sort": 10
    }),
    "hit": _tools.RODict({
        "ID": "hit",
        "showType": 1,
        "sort": 11
    }),
    "dodge": _tools.RODict({
        "ID": "dodge",
        "showType": 1,
        "sort": 12
    }),
    "accuracy": _tools.RODict({
        "ID": "accuracy",
        "showType": 1,
        "sort": 13
    }),
    "evasion": _tools.RODict({
        "ID": "evasion",
        "showType": 1,
        "sort": 14
    }),
    "fatal": _tools.RODict({
        "ID": "fatal",
        "showType": 1,
        "sort": 15
    }),
    "antiFatal": _tools.RODict({
        "ID": "antiFatal",
        "showType": 1,
        "sort": 16
    }),
    "drugsQuantity": _tools.RODict({
        "ID": "drugsQuantity",
        "showType": 1,
        "sort": 17
    }),
    "atkBless": _tools.RODict({
        "ID": "atkBless",
        "showType": 1,
        "sort": 18
    }),
    "mortal": _tools.RODict({
        "ID": "mortal",
        "showType": 2,
        "sort": 1
    }),
    "antiMortal": _tools.RODict({
        "ID": "antiMortal",
        "showType": 2,
        "sort": 2
    }),
    "ignoreArmor": _tools.RODict({
        "ID": "ignoreArmor",
        "showType": 2,
        "sort": 3
    }),
    "dmgArmor": _tools.RODict({
        "ID": "dmgArmor",
        "showType": 2,
        "sort": 4
    }),
    "finalDmg": _tools.RODict({
        "ID": "finalDmg",
        "showType": 2,
        "sort": 5
    }),
    "finalDmgAnti": _tools.RODict({
        "ID": "finalDmgAnti",
        "showType": 2,
        "sort": 6
    }),
    "realDmg": _tools.RODict({
        "ID": "realDmg",
        "showType": 2,
        "sort": 7
    }),
    "realDmgDef": _tools.RODict({
        "ID": "realDmgDef",
        "showType": 2,
        "sort": 8
    }),
    "monsterDmg": _tools.RODict({
        "ID": "monsterDmg",
        "showType": 2,
        "sort": 9
    }),
    "monsterDmgAnti": _tools.RODict({
        "ID": "monsterDmgAnti",
        "showType": 2,
        "sort": 10
    }),
    "PVPDmg": _tools.RODict({
        "ID": "PVPDmg",
        "showType": 2,
        "sort": 11
    }),
    "PVPDmgAnti": _tools.RODict({
        "ID": "PVPDmgAnti",
        "showType": 2,
        "sort": 12
    }),
    "mulSpeed": _tools.RODict({
        "ID": "mulSpeed",
        "showType": 2,
        "sort": 13
    }),
    "skillCD": _tools.RODict({
        "ID": "skillCD",
        "showType": 2,
        "sort": 14
    }),
    "stunEnh": _tools.RODict({
        "ID": "stunEnh",
        "showType": 3,
        "sort": 1
    }),
    "stunAnti": _tools.RODict({
        "ID": "stunAnti",
        "showType": 3,
        "sort": 2
    }),
    "silentEnh": _tools.RODict({
        "ID": "silentEnh",
        "showType": 3,
        "sort": 3
    }),
    "silentAnti": _tools.RODict({
        "ID": "silentAnti",
        "showType": 3,
        "sort": 4
    }),
    "knockEnh": _tools.RODict({
        "ID": "knockEnh",
        "showType": 3,
        "sort": 5
    }),
    "knockAnti": _tools.RODict({
        "ID": "knockAnti",
        "showType": 3,
        "sort": 6
    }),
    "frozenEnh": _tools.RODict({
        "ID": "frozenEnh",
        "showType": 3,
        "sort": 7
    }),
    "frozenAnti": _tools.RODict({
        "ID": "frozenAnti",
        "showType": 3,
        "sort": 8
    }),
    "slowEnh": _tools.RODict({
        "ID": "slowEnh",
        "showType": 3,
        "sort": 9
    }),
    "slowAnti": _tools.RODict({
        "ID": "slowAnti",
        "showType": 3,
        "sort": 10
    }),
    "pushEnh": _tools.RODict({
        "ID": "pushEnh",
        "showType": 3,
        "sort": 11
    }),
    "pushAnti": _tools.RODict({
        "ID": "pushAnti",
        "showType": 3,
        "sort": 12
    }),
    "copper": _tools.RODict({
        "ID": "copper",
        "showType": 4,
        "sort": 1
    }),
    "expGrow": _tools.RODict({
        "ID": "expGrow",
        "showType": 4,
        "sort": 2
    }),
    "medicineRate": _tools.RODict({
        "ID": "medicineRate",
        "showType": 4,
        "sort": 3
    })
})