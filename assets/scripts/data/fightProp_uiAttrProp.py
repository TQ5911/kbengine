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
        "hideInAttrUI": 0,
        "showType": 1,
        "sort": 1
    }),
    "fullMp": _tools.RODict({
        "ID": "fullMp",
        "hideInAttrUI": 0,
        "showType": 1,
        "sort": 2
    }),
    "minPhysicalAtk": _tools.RODict({
        "ID": "minPhysicalAtk",
        "hideInAttrUI": 0,
        "showType": 1,
        "sort": 3
    }),
    "maxPhysicalAtk": _tools.RODict({
        "ID": "maxPhysicalAtk",
        "hideInAttrUI": 0,
        "showType": 1,
        "sort": 4
    }),
    "minPhysicalArmor": _tools.RODict({
        "ID": "minPhysicalArmor",
        "hideInAttrUI": 0,
        "showType": 1,
        "sort": 5
    }),
    "maxPhysicalArmor": _tools.RODict({
        "ID": "maxPhysicalArmor",
        "hideInAttrUI": 0,
        "showType": 1,
        "sort": 6
    }),
    "minMagicAtk": _tools.RODict({
        "ID": "minMagicAtk",
        "hideInAttrUI": 0,
        "showType": 1,
        "sort": 7
    }),
    "maxMagicAtk": _tools.RODict({
        "ID": "maxMagicAtk",
        "hideInAttrUI": 0,
        "showType": 1,
        "sort": 8
    }),
    "minMagicArmor": _tools.RODict({
        "ID": "minMagicArmor",
        "hideInAttrUI": 0,
        "showType": 1,
        "sort": 9
    }),
    "maxMagicArmor": _tools.RODict({
        "ID": "maxMagicArmor",
        "hideInAttrUI": 0,
        "showType": 1,
        "sort": 10
    }),
    "hit": _tools.RODict({
        "ID": "hit",
        "hideInAttrUI": 0,
        "showType": 1,
        "sort": 13
    }),
    "dodge": _tools.RODict({
        "ID": "dodge",
        "hideInAttrUI": 0,
        "showType": 1,
        "sort": 14
    }),
    "accuracy": _tools.RODict({
        "ID": "accuracy",
        "hideInAttrUI": 0,
        "showType": 1,
        "sort": 15
    }),
    "evasion": _tools.RODict({
        "ID": "evasion",
        "hideInAttrUI": 0,
        "showType": 1,
        "sort": 16
    }),
    "fatal": _tools.RODict({
        "ID": "fatal",
        "hideInAttrUI": 0,
        "showType": 1,
        "sort": 17
    }),
    "antiFatal": _tools.RODict({
        "ID": "antiFatal",
        "hideInAttrUI": 0,
        "showType": 1,
        "sort": 18
    }),
    "drugsQuantity": _tools.RODict({
        "ID": "drugsQuantity",
        "hideInAttrUI": 0,
        "showType": 1,
        "sort": 19
    }),
    "atkBless": _tools.RODict({
        "ID": "atkBless",
        "hideInAttrUI": 0,
        "showType": 1,
        "sort": 20
    }),
    "minAllArmor": _tools.RODict({
        "ID": "minAllArmor",
        "hideInAttrUI": 0,
        "showType": 1,
        "sort": 11
    }),
    "maxAllArmor": _tools.RODict({
        "ID": "maxAllArmor",
        "hideInAttrUI": 0,
        "showType": 1,
        "sort": 12
    }),
    "mortal": _tools.RODict({
        "ID": "mortal",
        "hideInAttrUI": 0,
        "showType": 2,
        "sort": 1
    }),
    "antiMortal": _tools.RODict({
        "ID": "antiMortal",
        "hideInAttrUI": 0,
        "showType": 2,
        "sort": 2
    }),
    "ignoreArmor": _tools.RODict({
        "ID": "ignoreArmor",
        "hideInAttrUI": 0,
        "showType": 2,
        "sort": 3
    }),
    "dmgArmor": _tools.RODict({
        "ID": "dmgArmor",
        "hideInAttrUI": 0,
        "showType": 2,
        "sort": 4
    }),
    "finalDmg": _tools.RODict({
        "ID": "finalDmg",
        "hideInAttrUI": 0,
        "showType": 2,
        "sort": 5
    }),
    "finalDmgAnti": _tools.RODict({
        "ID": "finalDmgAnti",
        "hideInAttrUI": 0,
        "showType": 2,
        "sort": 6
    }),
    "realDmg": _tools.RODict({
        "ID": "realDmg",
        "hideInAttrUI": 0,
        "showType": 2,
        "sort": 7
    }),
    "realDmgDef": _tools.RODict({
        "ID": "realDmgDef",
        "hideInAttrUI": 0,
        "showType": 2,
        "sort": 8
    }),
    "monsterDmg": _tools.RODict({
        "ID": "monsterDmg",
        "hideInAttrUI": 0,
        "showType": 2,
        "sort": 9
    }),
    "monsterDmgAnti": _tools.RODict({
        "ID": "monsterDmgAnti",
        "hideInAttrUI": 0,
        "showType": 2,
        "sort": 10
    }),
    "PVPDmg": _tools.RODict({
        "ID": "PVPDmg",
        "hideInAttrUI": 0,
        "showType": 2,
        "sort": 11
    }),
    "PVPDmgAnti": _tools.RODict({
        "ID": "PVPDmgAnti",
        "hideInAttrUI": 0,
        "showType": 2,
        "sort": 12
    }),
    "mulSpeed": _tools.RODict({
        "ID": "mulSpeed",
        "hideInAttrUI": 0,
        "showType": 2,
        "sort": 13
    }),
    "skillCD": _tools.RODict({
        "ID": "skillCD",
        "hideInAttrUI": 0,
        "showType": 2,
        "sort": 14
    }),
    "stunEnh": _tools.RODict({
        "ID": "stunEnh",
        "hideInAttrUI": 0,
        "showType": 3,
        "sort": 1
    }),
    "stunAnti": _tools.RODict({
        "ID": "stunAnti",
        "hideInAttrUI": 0,
        "showType": 3,
        "sort": 2
    }),
    "silentEnh": _tools.RODict({
        "ID": "silentEnh",
        "hideInAttrUI": 0,
        "showType": 3,
        "sort": 3
    }),
    "silentAnti": _tools.RODict({
        "ID": "silentAnti",
        "hideInAttrUI": 0,
        "showType": 3,
        "sort": 4
    }),
    "knockEnh": _tools.RODict({
        "ID": "knockEnh",
        "hideInAttrUI": 0,
        "showType": 3,
        "sort": 5
    }),
    "knockAnti": _tools.RODict({
        "ID": "knockAnti",
        "hideInAttrUI": 0,
        "showType": 3,
        "sort": 6
    }),
    "frozenEnh": _tools.RODict({
        "ID": "frozenEnh",
        "hideInAttrUI": 0,
        "showType": 3,
        "sort": 7
    }),
    "frozenAnti": _tools.RODict({
        "ID": "frozenAnti",
        "hideInAttrUI": 0,
        "showType": 3,
        "sort": 8
    }),
    "slowEnh": _tools.RODict({
        "ID": "slowEnh",
        "hideInAttrUI": 0,
        "showType": 3,
        "sort": 9
    }),
    "slowAnti": _tools.RODict({
        "ID": "slowAnti",
        "hideInAttrUI": 0,
        "showType": 3,
        "sort": 10
    }),
    "pushEnh": _tools.RODict({
        "ID": "pushEnh",
        "hideInAttrUI": 0,
        "showType": 3,
        "sort": 11
    }),
    "pushAnti": _tools.RODict({
        "ID": "pushAnti",
        "hideInAttrUI": 0,
        "showType": 3,
        "sort": 12
    }),
    "uniEnh": _tools.RODict({
        "ID": "uniEnh",
        "hideInAttrUI": 0,
        "showType": 3,
        "sort": 13
    }),
    "uniAnti": _tools.RODict({
        "ID": "uniAnti",
        "hideInAttrUI": 0,
        "showType": 3,
        "sort": 14
    }),
    "copper": _tools.RODict({
        "ID": "copper",
        "hideInAttrUI": 0,
        "showType": 4,
        "sort": 1
    }),
    "expGrow": _tools.RODict({
        "ID": "expGrow",
        "hideInAttrUI": 0,
        "showType": 4,
        "sort": 2
    }),
    "medicineRate": _tools.RODict({
        "ID": "medicineRate",
        "hideInAttrUI": 0,
        "showType": 4,
        "sort": 3
    }),
    "miningRate": _tools.RODict({
        "ID": "miningRate",
        "hideInAttrUI": 1,
        "showType": 4,
        "sort": 4
    }),
    "gatherRate": _tools.RODict({
        "ID": "gatherRate",
        "hideInAttrUI": 1,
        "showType": 4,
        "sort": 4
    })
})