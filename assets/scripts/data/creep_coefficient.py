# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: creep/coefficient
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
        "notes": "普通怪",
        "adjFullHp": 1,
        "adjFullMp": 1,
        "adjMinPhysicalAtk": 1,
        "adjMaxPhysicalAtk": 1,
        "adjMinMagicAtk": 1,
        "adjMaxMagicAtk": 1,
        "adjAtkBless": 1,
        "adjMinPhysicalArmor": 1,
        "adjMaxPhysicalArmor": 1,
        "adjMinMagicArmor": 1,
        "adjMaxMagicArmor": 1,
        "adjHit": 1,
        "adjDodge": 1,
        "adjFatal": 1,
        "adjAntiFatal": 1,
        "adjIgnoreArmor": 1.0,
        "adjDmgArmor": 1,
        "adjMortal": 1.0,
        "adjAntiMortal": 1.0,
        "adjRealDmg": 1,
        "adjRealDmgDef": 1,
        "adjFinalDmg": 1.0,
        "adjFinalDmgAnti": 1.0,
        "adjStunEnh": 1,
        "adjStunAnti": 1,
        "adjSilentEnh": 1,
        "adjSilentAnti": 1,
        "adjKnockEnh": 1,
        "adjKnockAnti": 1,
        "adjFrozenEnh": 1,
        "adjFrozenAnti": 1,
        "adjSlowEnh": 1,
        "adjSlowAnti": 1
    }),
    2: _tools.RODict({
        "ID": 2,
        "notes": "幸运怪",
        "adjFullHp": 10,
        "adjFullMp": 1,
        "adjMinPhysicalAtk": 1,
        "adjMaxPhysicalAtk": 1,
        "adjMinMagicAtk": 1,
        "adjMaxMagicAtk": 1,
        "adjAtkBless": 1,
        "adjMinPhysicalArmor": 1,
        "adjMaxPhysicalArmor": 1,
        "adjMinMagicArmor": 1,
        "adjMaxMagicArmor": 1,
        "adjHit": 1,
        "adjDodge": 1,
        "adjFatal": 1,
        "adjAntiFatal": 1,
        "adjIgnoreArmor": 1.0,
        "adjDmgArmor": 1,
        "adjMortal": 1.0,
        "adjAntiMortal": 1.0,
        "adjRealDmg": 1,
        "adjRealDmgDef": 1,
        "adjFinalDmg": 1.0,
        "adjFinalDmgAnti": 1.0,
        "adjStunEnh": 1,
        "adjStunAnti": 1,
        "adjSilentEnh": 1,
        "adjSilentAnti": 1,
        "adjKnockEnh": 1,
        "adjKnockAnti": 1,
        "adjFrozenEnh": 1,
        "adjFrozenAnti": 1,
        "adjSlowEnh": 1,
        "adjSlowAnti": 1
    }),
    3: _tools.RODict({
        "ID": 3,
        "notes": "头目怪",
        "adjFullHp": None,
        "adjFullMp": 1,
        "adjMinPhysicalAtk": None,
        "adjMaxPhysicalAtk": None,
        "adjMinMagicAtk": None,
        "adjMaxMagicAtk": None,
        "adjAtkBless": 1,
        "adjMinPhysicalArmor": 1,
        "adjMaxPhysicalArmor": 1,
        "adjMinMagicArmor": 1,
        "adjMaxMagicArmor": 1,
        "adjHit": 1,
        "adjDodge": 1,
        "adjFatal": 1,
        "adjAntiFatal": 1,
        "adjIgnoreArmor": 1.0,
        "adjDmgArmor": 1,
        "adjMortal": 1.0,
        "adjAntiMortal": 1.0,
        "adjRealDmg": 1,
        "adjRealDmgDef": 1,
        "adjFinalDmg": 1.0,
        "adjFinalDmgAnti": 1.0,
        "adjStunEnh": 1,
        "adjStunAnti": 1,
        "adjSilentEnh": 1,
        "adjSilentAnti": 1,
        "adjKnockEnh": 1,
        "adjKnockAnti": 1,
        "adjFrozenEnh": 1,
        "adjFrozenAnti": 1,
        "adjSlowEnh": 1,
        "adjSlowAnti": 1
    })
})
minKey = 1
maxKey = 3