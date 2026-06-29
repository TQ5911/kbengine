# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: prop/fightprop
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    52000001: _tools.RODict({
        "propID": 52000001,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":20000,"adjFullMp":10000,"adjMinPhysicalAtk":100,"adjMaxPhysicalAtk":200,"adjMinMagicAtk":100,"adjMaxMagicAtk":200,"mulFullHp":1.0})
    }),
    51000001: _tools.RODict({
        "propID": 51000001,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":50,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":22,"adjMinMagicAtk":22,"adjMaxMagicAtk":22,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjAccuracy":5,"adjFatal":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000002: _tools.RODict({
        "propID": 51000002,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":53,"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":24,"adjMinMagicAtk":24,"adjMaxMagicAtk":24,"adjMinPhysicalArmor":17,"adjMaxPhysicalArmor":17,"adjMinMagicArmor":17,"adjMaxMagicArmor":17,"adjAccuracy":5,"adjFatal":2,"adjRealDmg":2,"adjRealDmgDef":2,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000003: _tools.RODict({
        "propID": 51000003,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":56,"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":26,"adjMinMagicAtk":26,"adjMaxMagicAtk":26,"adjMinPhysicalArmor":18,"adjMaxPhysicalArmor":18,"adjMinMagicArmor":18,"adjMaxMagicArmor":18,"adjAccuracy":5,"adjFatal":2,"adjRealDmg":3,"adjRealDmgDef":3,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000004: _tools.RODict({
        "propID": 51000004,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":59,"adjMinPhysicalAtk":28,"adjMaxPhysicalAtk":28,"adjMinMagicAtk":28,"adjMaxMagicAtk":28,"adjMinPhysicalArmor":18,"adjMaxPhysicalArmor":18,"adjMinMagicArmor":18,"adjMaxMagicArmor":18,"adjAccuracy":5,"adjFatal":2,"adjRealDmg":4,"adjRealDmgDef":4,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000005: _tools.RODict({
        "propID": 51000005,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":62,"adjMinPhysicalAtk":36,"adjMaxPhysicalAtk":36,"adjMinMagicAtk":36,"adjMaxMagicAtk":36,"adjMinPhysicalArmor":19,"adjMaxPhysicalArmor":19,"adjMinMagicArmor":19,"adjMaxMagicArmor":19,"adjAccuracy":5,"adjFatal":2,"adjRealDmg":5,"adjRealDmgDef":5,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000006: _tools.RODict({
        "propID": 51000006,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":65,"adjMinPhysicalAtk":65,"adjMaxPhysicalAtk":65,"adjMinMagicAtk":65,"adjMaxMagicAtk":65,"adjMinPhysicalArmor":21,"adjMaxPhysicalArmor":21,"adjMinMagicArmor":21,"adjMaxMagicArmor":21,"adjAccuracy":5,"adjFatal":2,"adjRealDmg":6,"adjRealDmgDef":6,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000007: _tools.RODict({
        "propID": 51000007,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":68,"adjMinPhysicalAtk":102,"adjMaxPhysicalAtk":102,"adjMinMagicAtk":102,"adjMaxMagicAtk":102,"adjMinPhysicalArmor":30,"adjMaxPhysicalArmor":30,"adjMinMagicArmor":30,"adjMaxMagicArmor":30,"adjAccuracy":5,"adjFatal":2,"adjRealDmg":7,"adjRealDmgDef":7,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000008: _tools.RODict({
        "propID": 51000008,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":71,"adjMinPhysicalAtk":124,"adjMaxPhysicalAtk":124,"adjMinMagicAtk":124,"adjMaxMagicAtk":124,"adjMinPhysicalArmor":45,"adjMaxPhysicalArmor":45,"adjMinMagicArmor":45,"adjMaxMagicArmor":45,"adjAccuracy":6,"adjEvasion":1,"adjFatal":2,"adjRealDmg":8,"adjRealDmgDef":8,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000009: _tools.RODict({
        "propID": 51000009,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":75,"adjMinPhysicalAtk":135,"adjMaxPhysicalAtk":135,"adjMinMagicAtk":135,"adjMaxMagicAtk":135,"adjMinPhysicalArmor":118,"adjMaxPhysicalArmor":118,"adjMinMagicArmor":118,"adjMaxMagicArmor":118,"adjAccuracy":6,"adjEvasion":1,"adjFatal":2,"adjRealDmg":9,"adjRealDmgDef":9,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000010: _tools.RODict({
        "propID": 51000010,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":80,"adjMinPhysicalAtk":145,"adjMaxPhysicalAtk":145,"adjMinMagicAtk":145,"adjMaxMagicAtk":145,"adjMinPhysicalArmor":120,"adjMaxPhysicalArmor":120,"adjMinMagicArmor":120,"adjMaxMagicArmor":120,"adjAccuracy":6,"adjEvasion":1,"adjFatal":2,"adjRealDmg":10,"adjRealDmgDef":10,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000011: _tools.RODict({
        "propID": 51000011,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":90,"adjMinPhysicalAtk":168,"adjMaxPhysicalAtk":168,"adjMinMagicAtk":168,"adjMaxMagicAtk":168,"adjMinPhysicalArmor":125,"adjMaxPhysicalArmor":125,"adjMinMagicArmor":125,"adjMaxMagicArmor":125,"adjAccuracy":6,"adjEvasion":1,"adjFatal":2,"adjRealDmg":11,"adjRealDmgDef":11,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000012: _tools.RODict({
        "propID": 51000012,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":100,"adjMinPhysicalAtk":190,"adjMaxPhysicalAtk":190,"adjMinMagicAtk":190,"adjMaxMagicAtk":190,"adjMinPhysicalArmor":126,"adjMaxPhysicalArmor":126,"adjMinMagicArmor":126,"adjMaxMagicArmor":126,"adjAccuracy":6,"adjEvasion":1,"adjFatal":2,"adjRealDmg":12,"adjRealDmgDef":12,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000013: _tools.RODict({
        "propID": 51000013,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":110,"adjMinPhysicalAtk":202,"adjMaxPhysicalAtk":202,"adjMinMagicAtk":202,"adjMaxMagicAtk":202,"adjMinPhysicalArmor":127,"adjMaxPhysicalArmor":127,"adjMinMagicArmor":127,"adjMaxMagicArmor":127,"adjAccuracy":6,"adjEvasion":1,"adjFatal":2,"adjRealDmg":13,"adjRealDmgDef":13,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000014: _tools.RODict({
        "propID": 51000014,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":120,"adjMinPhysicalAtk":210,"adjMaxPhysicalAtk":210,"adjMinMagicAtk":210,"adjMaxMagicAtk":210,"adjMinPhysicalArmor":129,"adjMaxPhysicalArmor":129,"adjMinMagicArmor":129,"adjMaxMagicArmor":129,"adjAccuracy":6,"adjEvasion":1,"adjFatal":2,"adjRealDmg":14,"adjRealDmgDef":14,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000015: _tools.RODict({
        "propID": 51000015,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":135,"adjMinPhysicalAtk":220,"adjMaxPhysicalAtk":220,"adjMinMagicAtk":220,"adjMaxMagicAtk":220,"adjMinPhysicalArmor":130,"adjMaxPhysicalArmor":130,"adjMinMagicArmor":130,"adjMaxMagicArmor":130,"adjAccuracy":6,"adjEvasion":1,"adjFatal":2,"adjRealDmg":15,"adjRealDmgDef":15,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000016: _tools.RODict({
        "propID": 51000016,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":150,"adjMinPhysicalAtk":236,"adjMaxPhysicalAtk":236,"adjMinMagicAtk":236,"adjMaxMagicAtk":236,"adjMinPhysicalArmor":132,"adjMaxPhysicalArmor":132,"adjMinMagicArmor":132,"adjMaxMagicArmor":132,"adjAccuracy":6,"adjEvasion":1,"adjFatal":2,"adjRealDmg":16,"adjRealDmgDef":16,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000017: _tools.RODict({
        "propID": 51000017,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":160,"adjMinPhysicalAtk":255,"adjMaxPhysicalAtk":255,"adjMinMagicAtk":255,"adjMaxMagicAtk":255,"adjMinPhysicalArmor":133,"adjMaxPhysicalArmor":133,"adjMinMagicArmor":133,"adjMaxMagicArmor":133,"adjAccuracy":6,"adjEvasion":1,"adjFatal":2,"adjRealDmg":17,"adjRealDmgDef":17,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000018: _tools.RODict({
        "propID": 51000018,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":170,"adjMinPhysicalAtk":269,"adjMaxPhysicalAtk":269,"adjMinMagicAtk":269,"adjMaxMagicAtk":269,"adjMinPhysicalArmor":141,"adjMaxPhysicalArmor":141,"adjMinMagicArmor":141,"adjMaxMagicArmor":141,"adjAccuracy":6,"adjEvasion":1,"adjFatal":2,"adjRealDmg":18,"adjRealDmgDef":18,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000019: _tools.RODict({
        "propID": 51000019,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":180,"adjMinPhysicalAtk":284,"adjMaxPhysicalAtk":284,"adjMinMagicAtk":284,"adjMaxMagicAtk":284,"adjMinPhysicalArmor":151,"adjMaxPhysicalArmor":151,"adjMinMagicArmor":151,"adjMaxMagicArmor":151,"adjAccuracy":6,"adjEvasion":1,"adjFatal":2,"adjIgnoreArmor":0.0045,"adjDmgArmor":0.0045,"adjMortal":0.018,"adjAntiMortal":0.018,"adjRealDmg":19,"adjRealDmgDef":19,"adjMonsterDmg":0.0135,"adjMonsterDmgAnti":0.0128,"adjFinalDmg":0.0045,"adjFinalDmgAnti":0.0045,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000020: _tools.RODict({
        "propID": 51000020,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":190,"adjMinPhysicalAtk":304,"adjMaxPhysicalAtk":304,"adjMinMagicAtk":304,"adjMaxMagicAtk":304,"adjMinPhysicalArmor":160,"adjMaxPhysicalArmor":160,"adjMinMagicArmor":160,"adjMaxMagicArmor":160,"adjAccuracy":7,"adjEvasion":2,"adjFatal":3,"adjAntiFatal":1,"adjIgnoreArmor":0.006,"adjDmgArmor":0.006,"adjMortal":0.0282,"adjAntiMortal":0.0282,"adjRealDmg":20,"adjRealDmgDef":20,"adjMonsterDmg":0.0286,"adjMonsterDmgAnti":0.0278,"adjFinalDmg":0.0067,"adjFinalDmgAnti":0.0067,"adjStunEnh":2,"adjStunAnti":2,"adjSilentEnh":2,"adjSilentAnti":2,"adjKnockEnh":2,"adjKnockAnti":2,"adjFrozenEnh":2,"adjFrozenAnti":2,"adjSlowEnh":2,"adjSlowAnti":2,"adjPushEnh":2,"adjPushAnti":2})
    }),
    51000021: _tools.RODict({
        "propID": 51000021,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":221,"adjMinPhysicalAtk":317,"adjMaxPhysicalAtk":317,"adjMinMagicAtk":317,"adjMaxMagicAtk":317,"adjMinPhysicalArmor":166,"adjMaxPhysicalArmor":166,"adjMinMagicArmor":166,"adjMaxMagicArmor":166,"adjAccuracy":7,"adjEvasion":2,"adjFatal":4,"adjAntiFatal":1,"adjIgnoreArmor":0.006,"adjDmgArmor":0.006,"adjMortal":0.0282,"adjAntiMortal":0.0282,"adjRealDmg":21,"adjRealDmgDef":21,"adjMonsterDmg":0.0286,"adjMonsterDmgAnti":0.0278,"adjFinalDmg":0.0067,"adjFinalDmgAnti":0.0067,"adjStunEnh":2,"adjStunAnti":2,"adjSilentEnh":2,"adjSilentAnti":2,"adjKnockEnh":2,"adjKnockAnti":2,"adjFrozenEnh":2,"adjFrozenAnti":2,"adjSlowEnh":2,"adjSlowAnti":2,"adjPushEnh":2,"adjPushAnti":2})
    }),
    51000022: _tools.RODict({
        "propID": 51000022,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":252,"adjMinPhysicalAtk":336,"adjMaxPhysicalAtk":336,"adjMinMagicAtk":336,"adjMaxMagicAtk":336,"adjMinPhysicalArmor":173,"adjMaxPhysicalArmor":173,"adjMinMagicArmor":173,"adjMaxMagicArmor":173,"adjAccuracy":7,"adjEvasion":2,"adjFatal":5,"adjAntiFatal":1,"adjIgnoreArmor":0.006,"adjDmgArmor":0.006,"adjMortal":0.0282,"adjAntiMortal":0.0282,"adjRealDmg":22,"adjRealDmgDef":22,"adjMonsterDmg":0.0286,"adjMonsterDmgAnti":0.0278,"adjFinalDmg":0.0067,"adjFinalDmgAnti":0.0067,"adjStunEnh":2,"adjStunAnti":2,"adjSilentEnh":2,"adjSilentAnti":2,"adjKnockEnh":2,"adjKnockAnti":2,"adjFrozenEnh":2,"adjFrozenAnti":2,"adjSlowEnh":2,"adjSlowAnti":2,"adjPushEnh":2,"adjPushAnti":2})
    }),
    51000023: _tools.RODict({
        "propID": 51000023,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":284,"adjMinPhysicalAtk":355,"adjMaxPhysicalAtk":355,"adjMinMagicAtk":355,"adjMaxMagicAtk":355,"adjMinPhysicalArmor":187,"adjMaxPhysicalArmor":187,"adjMinMagicArmor":187,"adjMaxMagicArmor":187,"adjAccuracy":7,"adjEvasion":2,"adjFatal":6,"adjAntiFatal":1,"adjIgnoreArmor":0.006,"adjDmgArmor":0.006,"adjMortal":0.0282,"adjAntiMortal":0.0282,"adjRealDmg":23,"adjRealDmgDef":23,"adjMonsterDmg":0.0286,"adjMonsterDmgAnti":0.0278,"adjFinalDmg":0.0067,"adjFinalDmgAnti":0.0067,"adjStunEnh":2,"adjStunAnti":2,"adjSilentEnh":2,"adjSilentAnti":2,"adjKnockEnh":2,"adjKnockAnti":2,"adjFrozenEnh":2,"adjFrozenAnti":2,"adjSlowEnh":2,"adjSlowAnti":2,"adjPushEnh":2,"adjPushAnti":2})
    }),
    51000024: _tools.RODict({
        "propID": 51000024,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":315,"adjMinPhysicalAtk":367,"adjMaxPhysicalAtk":367,"adjMinMagicAtk":367,"adjMaxMagicAtk":367,"adjMinPhysicalArmor":192,"adjMaxPhysicalArmor":192,"adjMinMagicArmor":192,"adjMaxMagicArmor":192,"adjAccuracy":7,"adjEvasion":2,"adjFatal":7,"adjAntiFatal":1,"adjIgnoreArmor":0.006,"adjDmgArmor":0.006,"adjMortal":0.0282,"adjAntiMortal":0.0282,"adjRealDmg":24,"adjRealDmgDef":24,"adjMonsterDmg":0.0286,"adjMonsterDmgAnti":0.0278,"adjFinalDmg":0.0067,"adjFinalDmgAnti":0.0067,"adjStunEnh":2,"adjStunAnti":2,"adjSilentEnh":2,"adjSilentAnti":2,"adjKnockEnh":2,"adjKnockAnti":2,"adjFrozenEnh":2,"adjFrozenAnti":2,"adjSlowEnh":2,"adjSlowAnti":2,"adjPushEnh":2,"adjPushAnti":2})
    }),
    51000025: _tools.RODict({
        "propID": 51000025,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":347,"adjMinPhysicalAtk":409,"adjMaxPhysicalAtk":409,"adjMinMagicAtk":409,"adjMaxMagicAtk":409,"adjMinPhysicalArmor":209,"adjMaxPhysicalArmor":209,"adjMinMagicArmor":209,"adjMaxMagicArmor":209,"adjAccuracy":7,"adjEvasion":2,"adjFatal":8,"adjAntiFatal":1,"adjIgnoreArmor":0.0075,"adjDmgArmor":0.01,"adjMortal":0.0342,"adjAntiMortal":0.0342,"adjRealDmg":25,"adjRealDmgDef":25,"adjMonsterDmg":0.0416,"adjMonsterDmgAnti":0.0458,"adjFinalDmg":0.0083,"adjFinalDmgAnti":0.0083,"adjStunEnh":2,"adjStunAnti":2,"adjSilentEnh":2,"adjSilentAnti":2,"adjKnockEnh":2,"adjKnockAnti":2,"adjFrozenEnh":2,"adjFrozenAnti":2,"adjSlowEnh":2,"adjSlowAnti":2,"adjPushEnh":2,"adjPushAnti":2})
    }),
    51000026: _tools.RODict({
        "propID": 51000026,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":379,"adjMinPhysicalAtk":413,"adjMaxPhysicalAtk":413,"adjMinMagicAtk":413,"adjMaxMagicAtk":413,"adjMinPhysicalArmor":211,"adjMaxPhysicalArmor":211,"adjMinMagicArmor":211,"adjMaxMagicArmor":211,"adjAccuracy":8,"adjEvasion":3,"adjFatal":9,"adjAntiFatal":1,"adjIgnoreArmor":0.0075,"adjDmgArmor":0.01,"adjMortal":0.0383,"adjAntiMortal":0.0383,"adjRealDmg":26,"adjRealDmgDef":26,"adjMonsterDmg":0.0437,"adjMonsterDmgAnti":0.0479,"adjFinalDmg":0.009,"adjFinalDmgAnti":0.009,"adjStunEnh":3,"adjStunAnti":3,"adjSilentEnh":3,"adjSilentAnti":3,"adjKnockEnh":3,"adjKnockAnti":3,"adjFrozenEnh":3,"adjFrozenAnti":3,"adjSlowEnh":3,"adjSlowAnti":3,"adjPushEnh":3,"adjPushAnti":3})
    }),
    51000027: _tools.RODict({
        "propID": 51000027,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":411,"adjMinPhysicalAtk":432,"adjMaxPhysicalAtk":432,"adjMinMagicAtk":432,"adjMaxMagicAtk":432,"adjMinPhysicalArmor":219,"adjMaxPhysicalArmor":219,"adjMinMagicArmor":219,"adjMaxMagicArmor":219,"adjAccuracy":8,"adjEvasion":3,"adjFatal":10,"adjAntiFatal":1,"adjIgnoreArmor":0.0075,"adjDmgArmor":0.01,"adjMortal":0.0383,"adjAntiMortal":0.0383,"adjRealDmg":27,"adjRealDmgDef":27,"adjMonsterDmg":0.0437,"adjMonsterDmgAnti":0.0479,"adjFinalDmg":0.009,"adjFinalDmgAnti":0.009,"adjStunEnh":3,"adjStunAnti":3,"adjSilentEnh":3,"adjSilentAnti":3,"adjKnockEnh":3,"adjKnockAnti":3,"adjFrozenEnh":3,"adjFrozenAnti":3,"adjSlowEnh":3,"adjSlowAnti":3,"adjPushEnh":3,"adjPushAnti":3})
    }),
    51000028: _tools.RODict({
        "propID": 51000028,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":444,"adjMinPhysicalAtk":442,"adjMaxPhysicalAtk":442,"adjMinMagicAtk":442,"adjMaxMagicAtk":442,"adjMinPhysicalArmor":222,"adjMaxPhysicalArmor":222,"adjMinMagicArmor":222,"adjMaxMagicArmor":222,"adjAccuracy":8,"adjEvasion":3,"adjFatal":11,"adjAntiFatal":1,"adjIgnoreArmor":0.0075,"adjDmgArmor":0.01,"adjMortal":0.0425,"adjAntiMortal":0.0425,"adjRealDmg":28,"adjRealDmgDef":28,"adjMonsterDmg":0.0457,"adjMonsterDmgAnti":0.05,"adjFinalDmg":0.0097,"adjFinalDmgAnti":0.0097,"adjStunEnh":3,"adjStunAnti":3,"adjSilentEnh":3,"adjSilentAnti":3,"adjKnockEnh":3,"adjKnockAnti":3,"adjFrozenEnh":3,"adjFrozenAnti":3,"adjSlowEnh":3,"adjSlowAnti":3,"adjPushEnh":3,"adjPushAnti":3})
    }),
    51000029: _tools.RODict({
        "propID": 51000029,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":476,"adjMinPhysicalAtk":451,"adjMaxPhysicalAtk":451,"adjMinMagicAtk":451,"adjMaxMagicAtk":451,"adjMinPhysicalArmor":227,"adjMaxPhysicalArmor":227,"adjMinMagicArmor":227,"adjMaxMagicArmor":227,"adjAccuracy":8,"adjEvasion":3,"adjFatal":12,"adjAntiFatal":1,"adjIgnoreArmor":0.0075,"adjDmgArmor":0.01,"adjMortal":0.0425,"adjAntiMortal":0.0425,"adjRealDmg":29,"adjRealDmgDef":29,"adjMonsterDmg":0.0457,"adjMonsterDmgAnti":0.05,"adjFinalDmg":0.0097,"adjFinalDmgAnti":0.0097,"adjStunEnh":3,"adjStunAnti":3,"adjSilentEnh":3,"adjSilentAnti":3,"adjKnockEnh":3,"adjKnockAnti":3,"adjFrozenEnh":3,"adjFrozenAnti":3,"adjSlowEnh":3,"adjSlowAnti":3,"adjPushEnh":3,"adjPushAnti":3})
    }),
    51000030: _tools.RODict({
        "propID": 51000030,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":509,"adjMinPhysicalAtk":460,"adjMaxPhysicalAtk":460,"adjMinMagicAtk":460,"adjMaxMagicAtk":460,"adjMinPhysicalArmor":238,"adjMaxPhysicalArmor":238,"adjMinMagicArmor":238,"adjMaxMagicArmor":238,"adjAccuracy":9,"adjEvasion":4,"adjFatal":14,"adjAntiFatal":1,"adjIgnoreArmor":0.029,"adjDmgArmor":0.0115,"adjMortal":0.0627,"adjAntiMortal":0.0527,"adjRealDmg":30,"adjRealDmgDef":30,"adjMonsterDmg":0.0608,"adjMonsterDmgAnti":0.0651,"adjFinalDmg":0.012,"adjFinalDmgAnti":0.012,"adjStunEnh":4,"adjStunAnti":4,"adjSilentEnh":4,"adjSilentAnti":4,"adjKnockEnh":4,"adjKnockAnti":4,"adjFrozenEnh":4,"adjFrozenAnti":4,"adjSlowEnh":4,"adjSlowAnti":4,"adjPushEnh":4,"adjPushAnti":4})
    }),
    51000031: _tools.RODict({
        "propID": 51000031,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":538,"adjMinPhysicalAtk":474,"adjMaxPhysicalAtk":474,"adjMinMagicAtk":474,"adjMaxMagicAtk":474,"adjMinPhysicalArmor":244,"adjMaxPhysicalArmor":244,"adjMinMagicArmor":244,"adjMaxMagicArmor":244,"adjAccuracy":9,"adjEvasion":4,"adjFatal":15,"adjAntiFatal":3,"adjIgnoreArmor":0.033,"adjDmgArmor":0.0132,"adjMortal":0.0785,"adjAntiMortal":0.0595,"adjRealDmg":31,"adjRealDmgDef":31,"adjMonsterDmg":0.0777,"adjMonsterDmgAnti":0.0734,"adjFinalDmg":0.0155,"adjFinalDmgAnti":0.0135,"adjStunEnh":4,"adjStunAnti":4,"adjSilentEnh":4,"adjSilentAnti":4,"adjKnockEnh":4,"adjKnockAnti":4,"adjFrozenEnh":4,"adjFrozenAnti":4,"adjSlowEnh":4,"adjSlowAnti":4,"adjPushEnh":4,"adjPushAnti":4})
    }),
    51000032: _tools.RODict({
        "propID": 51000032,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":551,"adjMinPhysicalAtk":483,"adjMaxPhysicalAtk":483,"adjMinMagicAtk":483,"adjMaxMagicAtk":483,"adjMinPhysicalArmor":250,"adjMaxPhysicalArmor":250,"adjMinMagicArmor":250,"adjMaxMagicArmor":250,"adjAccuracy":9,"adjEvasion":4,"adjFatal":15,"adjAntiFatal":4,"adjIgnoreArmor":0.0369,"adjDmgArmor":0.0149,"adjMortal":0.0943,"adjAntiMortal":0.0663,"adjRealDmg":32,"adjRealDmgDef":32,"adjMonsterDmg":0.0945,"adjMonsterDmgAnti":0.0816,"adjFinalDmg":0.0191,"adjFinalDmgAnti":0.0151,"adjStunEnh":4,"adjStunAnti":4,"adjSilentEnh":4,"adjSilentAnti":4,"adjKnockEnh":4,"adjKnockAnti":4,"adjFrozenEnh":4,"adjFrozenAnti":4,"adjSlowEnh":4,"adjSlowAnti":4,"adjPushEnh":4,"adjPushAnti":4})
    }),
    51000033: _tools.RODict({
        "propID": 51000033,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":565,"adjMinPhysicalAtk":492,"adjMaxPhysicalAtk":492,"adjMinMagicAtk":492,"adjMaxMagicAtk":492,"adjMinPhysicalArmor":256,"adjMaxPhysicalArmor":256,"adjMinMagicArmor":256,"adjMaxMagicArmor":256,"adjAccuracy":9,"adjEvasion":4,"adjFatal":16,"adjAntiFatal":6,"adjIgnoreArmor":0.0409,"adjDmgArmor":0.0166,"adjMortal":0.1101,"adjAntiMortal":0.0731,"adjRealDmg":33,"adjRealDmgDef":33,"adjMonsterDmg":0.1114,"adjMonsterDmgAnti":0.0899,"adjFinalDmg":0.0226,"adjFinalDmgAnti":0.0166,"adjStunEnh":4,"adjStunAnti":4,"adjSilentEnh":4,"adjSilentAnti":4,"adjKnockEnh":4,"adjKnockAnti":4,"adjFrozenEnh":4,"adjFrozenAnti":4,"adjSlowEnh":4,"adjSlowAnti":4,"adjPushEnh":4,"adjPushAnti":4})
    }),
    51000034: _tools.RODict({
        "propID": 51000034,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":578,"adjMinPhysicalAtk":501,"adjMaxPhysicalAtk":501,"adjMinMagicAtk":501,"adjMaxMagicAtk":501,"adjMinPhysicalArmor":262,"adjMaxPhysicalArmor":262,"adjMinMagicArmor":262,"adjMaxMagicArmor":262,"adjAccuracy":10,"adjEvasion":5,"adjFatal":17,"adjAntiFatal":7,"adjIgnoreArmor":0.0448,"adjDmgArmor":0.0183,"adjMortal":0.1259,"adjAntiMortal":0.0799,"adjRealDmg":34,"adjRealDmgDef":34,"adjMonsterDmg":0.1282,"adjMonsterDmgAnti":0.0982,"adjFinalDmg":0.0261,"adjFinalDmgAnti":0.0181,"adjStunEnh":5,"adjStunAnti":5,"adjSilentEnh":5,"adjSilentAnti":5,"adjKnockEnh":5,"adjKnockAnti":5,"adjFrozenEnh":5,"adjFrozenAnti":5,"adjSlowEnh":5,"adjSlowAnti":5,"adjPushEnh":5,"adjPushAnti":5})
    }),
    51000035: _tools.RODict({
        "propID": 51000035,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":592,"adjMinPhysicalAtk":516,"adjMaxPhysicalAtk":516,"adjMinMagicAtk":516,"adjMaxMagicAtk":516,"adjMinPhysicalArmor":268,"adjMaxPhysicalArmor":268,"adjMinMagicArmor":268,"adjMaxMagicArmor":268,"adjAccuracy":10,"adjEvasion":5,"adjFatal":17,"adjAntiFatal":9,"adjIgnoreArmor":0.0488,"adjDmgArmor":0.02,"adjMortal":0.1417,"adjAntiMortal":0.0867,"adjRealDmg":35,"adjRealDmgDef":35,"adjMonsterDmg":0.1451,"adjMonsterDmgAnti":0.1065,"adjFinalDmg":0.0296,"adjFinalDmgAnti":0.0196,"adjStunEnh":5,"adjStunAnti":5,"adjSilentEnh":5,"adjSilentAnti":5,"adjKnockEnh":5,"adjKnockAnti":5,"adjFrozenEnh":5,"adjFrozenAnti":5,"adjSlowEnh":5,"adjSlowAnti":5,"adjPushEnh":5,"adjPushAnti":5})
    }),
    51000036: _tools.RODict({
        "propID": 51000036,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":605,"adjMinPhysicalAtk":528,"adjMaxPhysicalAtk":528,"adjMinMagicAtk":528,"adjMaxMagicAtk":528,"adjMinPhysicalArmor":274,"adjMaxPhysicalArmor":274,"adjMinMagicArmor":274,"adjMaxMagicArmor":274,"adjAccuracy":10,"adjEvasion":5,"adjFatal":18,"adjAntiFatal":10,"adjIgnoreArmor":0.0527,"adjDmgArmor":0.0217,"adjMortal":0.1575,"adjAntiMortal":0.0935,"adjRealDmg":36,"adjRealDmgDef":36,"adjMonsterDmg":0.1619,"adjMonsterDmgAnti":0.1147,"adjFinalDmg":0.0331,"adjFinalDmgAnti":0.0211,"adjStunEnh":5,"adjStunAnti":5,"adjSilentEnh":5,"adjSilentAnti":5,"adjKnockEnh":5,"adjKnockAnti":5,"adjFrozenEnh":5,"adjFrozenAnti":5,"adjSlowEnh":5,"adjSlowAnti":5,"adjPushEnh":5,"adjPushAnti":5})
    }),
    51000037: _tools.RODict({
        "propID": 51000037,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":619,"adjMinPhysicalAtk":538,"adjMaxPhysicalAtk":538,"adjMinMagicAtk":538,"adjMaxMagicAtk":538,"adjMinPhysicalArmor":280,"adjMaxPhysicalArmor":280,"adjMinMagicArmor":280,"adjMaxMagicArmor":280,"adjAccuracy":10,"adjEvasion":5,"adjFatal":19,"adjAntiFatal":12,"adjIgnoreArmor":0.0567,"adjDmgArmor":0.0234,"adjMortal":0.1733,"adjAntiMortal":0.1003,"adjRealDmg":37,"adjRealDmgDef":37,"adjMonsterDmg":0.1788,"adjMonsterDmgAnti":0.123,"adjFinalDmg":0.0367,"adjFinalDmgAnti":0.0227,"adjStunEnh":5,"adjStunAnti":5,"adjSilentEnh":5,"adjSilentAnti":5,"adjKnockEnh":5,"adjKnockAnti":5,"adjFrozenEnh":5,"adjFrozenAnti":5,"adjSlowEnh":5,"adjSlowAnti":5,"adjPushEnh":5,"adjPushAnti":5})
    }),
    51000038: _tools.RODict({
        "propID": 51000038,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":632,"adjMinPhysicalAtk":547,"adjMaxPhysicalAtk":547,"adjMinMagicAtk":547,"adjMaxMagicAtk":547,"adjMinPhysicalArmor":286,"adjMaxPhysicalArmor":286,"adjMinMagicArmor":286,"adjMaxMagicArmor":286,"adjAccuracy":10,"adjEvasion":5,"adjFatal":19,"adjAntiFatal":14,"adjIgnoreArmor":0.0606,"adjDmgArmor":0.0251,"adjMortal":0.1891,"adjAntiMortal":0.1071,"adjRealDmg":38,"adjRealDmgDef":38,"adjMonsterDmg":0.1956,"adjMonsterDmgAnti":0.1313,"adjFinalDmg":0.0402,"adjFinalDmgAnti":0.0242,"adjStunEnh":5,"adjStunAnti":5,"adjSilentEnh":5,"adjSilentAnti":5,"adjKnockEnh":5,"adjKnockAnti":5,"adjFrozenEnh":5,"adjFrozenAnti":5,"adjSlowEnh":5,"adjSlowAnti":5,"adjPushEnh":5,"adjPushAnti":5})
    }),
    51000039: _tools.RODict({
        "propID": 51000039,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":645,"adjMinPhysicalAtk":557,"adjMaxPhysicalAtk":557,"adjMinMagicAtk":557,"adjMaxMagicAtk":557,"adjMinPhysicalArmor":292,"adjMaxPhysicalArmor":292,"adjMinMagicArmor":292,"adjMaxMagicArmor":292,"adjAccuracy":10,"adjEvasion":5,"adjFatal":20,"adjAntiFatal":15,"adjIgnoreArmor":0.0646,"adjDmgArmor":0.0268,"adjMortal":0.2049,"adjAntiMortal":0.1139,"adjRealDmg":39,"adjRealDmgDef":39,"adjMonsterDmg":0.2125,"adjMonsterDmgAnti":0.1396,"adjFinalDmg":0.0437,"adjFinalDmgAnti":0.0257,"adjStunEnh":5,"adjStunAnti":5,"adjSilentEnh":5,"adjSilentAnti":5,"adjKnockEnh":5,"adjKnockAnti":5,"adjFrozenEnh":5,"adjFrozenAnti":5,"adjSlowEnh":5,"adjSlowAnti":5,"adjPushEnh":5,"adjPushAnti":5})
    }),
    51000040: _tools.RODict({
        "propID": 51000040,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":658,"adjMinPhysicalAtk":568,"adjMaxPhysicalAtk":568,"adjMinMagicAtk":568,"adjMaxMagicAtk":568,"adjMinPhysicalArmor":297,"adjMaxPhysicalArmor":297,"adjMinMagicArmor":297,"adjMaxMagicArmor":297,"adjAccuracy":12,"adjEvasion":7,"adjFatal":21,"adjAntiFatal":17,"adjIgnoreArmor":0.0685,"adjDmgArmor":0.0285,"adjMortal":0.2207,"adjAntiMortal":0.1207,"adjRealDmg":40,"adjRealDmgDef":40,"adjMonsterDmg":0.2293,"adjMonsterDmgAnti":0.1478,"adjFinalDmg":0.0473,"adjFinalDmgAnti":0.0272,"adjStunEnh":7,"adjStunAnti":7,"adjSilentEnh":7,"adjSilentAnti":7,"adjKnockEnh":7,"adjKnockAnti":7,"adjFrozenEnh":7,"adjFrozenAnti":7,"adjSlowEnh":7,"adjSlowAnti":7,"adjPushEnh":7,"adjPushAnti":7})
    }),
    51000041: _tools.RODict({
        "propID": 51000041,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":675,"adjMinPhysicalAtk":583,"adjMaxPhysicalAtk":583,"adjMinMagicAtk":583,"adjMaxMagicAtk":583,"adjMinPhysicalArmor":305,"adjMaxPhysicalArmor":305,"adjMinMagicArmor":305,"adjMaxMagicArmor":305,"adjAccuracy":12,"adjEvasion":7,"adjFatal":22,"adjAntiFatal":17,"adjIgnoreArmor":0.0715,"adjDmgArmor":0.0295,"adjMortal":0.2371,"adjAntiMortal":0.1294,"adjRealDmg":41,"adjRealDmgDef":41,"adjMonsterDmg":0.2376,"adjMonsterDmgAnti":0.1561,"adjFinalDmg":0.0524,"adjFinalDmgAnti":0.0294,"adjStunEnh":7,"adjStunAnti":7,"adjSilentEnh":7,"adjSilentAnti":7,"adjKnockEnh":7,"adjKnockAnti":7,"adjFrozenEnh":7,"adjFrozenAnti":7,"adjSlowEnh":7,"adjSlowAnti":7,"adjPushEnh":7,"adjPushAnti":7})
    }),
    51000042: _tools.RODict({
        "propID": 51000042,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":692,"adjMinPhysicalAtk":599,"adjMaxPhysicalAtk":599,"adjMinMagicAtk":599,"adjMaxMagicAtk":599,"adjMinPhysicalArmor":313,"adjMaxPhysicalArmor":313,"adjMinMagicArmor":313,"adjMaxMagicArmor":313,"adjAccuracy":12,"adjEvasion":7,"adjFatal":22,"adjAntiFatal":18,"adjIgnoreArmor":0.0744,"adjDmgArmor":0.0304,"adjMortal":0.2536,"adjAntiMortal":0.1382,"adjRealDmg":42,"adjRealDmgDef":42,"adjMonsterDmg":0.2459,"adjMonsterDmgAnti":0.1644,"adjFinalDmg":0.0575,"adjFinalDmgAnti":0.0315,"adjStunEnh":7,"adjStunAnti":7,"adjSilentEnh":7,"adjSilentAnti":7,"adjKnockEnh":7,"adjKnockAnti":7,"adjFrozenEnh":7,"adjFrozenAnti":7,"adjSlowEnh":7,"adjSlowAnti":7,"adjPushEnh":7,"adjPushAnti":7})
    }),
    51000043: _tools.RODict({
        "propID": 51000043,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":710,"adjMinPhysicalAtk":614,"adjMaxPhysicalAtk":614,"adjMinMagicAtk":614,"adjMaxMagicAtk":614,"adjMinPhysicalArmor":322,"adjMaxPhysicalArmor":322,"adjMinMagicArmor":322,"adjMaxMagicArmor":322,"adjAccuracy":12,"adjEvasion":7,"adjFatal":23,"adjAntiFatal":18,"adjIgnoreArmor":0.0774,"adjDmgArmor":0.0314,"adjMortal":0.2701,"adjAntiMortal":0.147,"adjRealDmg":43,"adjRealDmgDef":43,"adjMonsterDmg":0.2542,"adjMonsterDmgAnti":0.1726,"adjFinalDmg":0.0626,"adjFinalDmgAnti":0.0336,"adjStunEnh":7,"adjStunAnti":7,"adjSilentEnh":7,"adjSilentAnti":7,"adjKnockEnh":7,"adjKnockAnti":7,"adjFrozenEnh":7,"adjFrozenAnti":7,"adjSlowEnh":7,"adjSlowAnti":7,"adjPushEnh":7,"adjPushAnti":7})
    }),
    51000044: _tools.RODict({
        "propID": 51000044,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":728,"adjMinPhysicalAtk":630,"adjMaxPhysicalAtk":630,"adjMinMagicAtk":630,"adjMaxMagicAtk":630,"adjMinPhysicalArmor":330,"adjMaxPhysicalArmor":330,"adjMinMagicArmor":330,"adjMaxMagicArmor":330,"adjAccuracy":13,"adjEvasion":8,"adjFatal":24,"adjAntiFatal":19,"adjIgnoreArmor":0.0803,"adjDmgArmor":0.0323,"adjMortal":0.2865,"adjAntiMortal":0.1557,"adjRealDmg":44,"adjRealDmgDef":44,"adjMonsterDmg":0.2625,"adjMonsterDmgAnti":0.1809,"adjFinalDmg":0.0678,"adjFinalDmgAnti":0.0358,"adjStunEnh":8,"adjStunAnti":8,"adjSilentEnh":8,"adjSilentAnti":8,"adjKnockEnh":8,"adjKnockAnti":8,"adjFrozenEnh":8,"adjFrozenAnti":8,"adjSlowEnh":8,"adjSlowAnti":8,"adjPushEnh":8,"adjPushAnti":8})
    }),
    51000045: _tools.RODict({
        "propID": 51000045,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":746,"adjMinPhysicalAtk":642,"adjMaxPhysicalAtk":642,"adjMinMagicAtk":642,"adjMaxMagicAtk":642,"adjMinPhysicalArmor":338,"adjMaxPhysicalArmor":338,"adjMinMagicArmor":338,"adjMaxMagicArmor":338,"adjAccuracy":13,"adjEvasion":8,"adjFatal":25,"adjAntiFatal":20,"adjIgnoreArmor":0.0833,"adjDmgArmor":0.0333,"adjMortal":0.303,"adjAntiMortal":0.1645,"adjRealDmg":45,"adjRealDmgDef":45,"adjMonsterDmg":0.2707,"adjMonsterDmgAnti":0.1891,"adjFinalDmg":0.0729,"adjFinalDmgAnti":0.0379,"adjStunEnh":8,"adjStunAnti":8,"adjSilentEnh":8,"adjSilentAnti":8,"adjKnockEnh":8,"adjKnockAnti":8,"adjFrozenEnh":8,"adjFrozenAnti":8,"adjSlowEnh":8,"adjSlowAnti":8,"adjPushEnh":8,"adjPushAnti":8})
    }),
    51000046: _tools.RODict({
        "propID": 51000046,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":765,"adjMinPhysicalAtk":655,"adjMaxPhysicalAtk":655,"adjMinMagicAtk":655,"adjMaxMagicAtk":655,"adjMinPhysicalArmor":346,"adjMaxPhysicalArmor":346,"adjMinMagicArmor":346,"adjMaxMagicArmor":346,"adjAccuracy":13,"adjEvasion":8,"adjFatal":25,"adjAntiFatal":20,"adjIgnoreArmor":0.0862,"adjDmgArmor":0.0342,"adjMortal":0.3195,"adjAntiMortal":0.1733,"adjRealDmg":46,"adjRealDmgDef":46,"adjMonsterDmg":0.279,"adjMonsterDmgAnti":0.1974,"adjFinalDmg":0.078,"adjFinalDmgAnti":0.04,"adjStunEnh":8,"adjStunAnti":8,"adjSilentEnh":8,"adjSilentAnti":8,"adjKnockEnh":8,"adjKnockAnti":8,"adjFrozenEnh":8,"adjFrozenAnti":8,"adjSlowEnh":8,"adjSlowAnti":8,"adjPushEnh":8,"adjPushAnti":8})
    }),
    51000047: _tools.RODict({
        "propID": 51000047,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":784,"adjMinPhysicalAtk":667,"adjMaxPhysicalAtk":667,"adjMinMagicAtk":667,"adjMaxMagicAtk":667,"adjMinPhysicalArmor":354,"adjMaxPhysicalArmor":354,"adjMinMagicArmor":354,"adjMaxMagicArmor":354,"adjAccuracy":13,"adjEvasion":8,"adjFatal":26,"adjAntiFatal":21,"adjIgnoreArmor":0.0892,"adjDmgArmor":0.0352,"adjMortal":0.3359,"adjAntiMortal":0.182,"adjRealDmg":47,"adjRealDmgDef":47,"adjMonsterDmg":0.2873,"adjMonsterDmgAnti":0.2056,"adjFinalDmg":0.0831,"adjFinalDmgAnti":0.0421,"adjStunEnh":8,"adjStunAnti":8,"adjSilentEnh":8,"adjSilentAnti":8,"adjKnockEnh":8,"adjKnockAnti":8,"adjFrozenEnh":8,"adjFrozenAnti":8,"adjSlowEnh":8,"adjSlowAnti":8,"adjPushEnh":8,"adjPushAnti":8})
    }),
    51000048: _tools.RODict({
        "propID": 51000048,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":803,"adjMinPhysicalAtk":686,"adjMaxPhysicalAtk":686,"adjMinMagicAtk":686,"adjMaxMagicAtk":686,"adjMinPhysicalArmor":362,"adjMaxPhysicalArmor":362,"adjMinMagicArmor":362,"adjMaxMagicArmor":362,"adjAccuracy":14,"adjEvasion":9,"adjFatal":27,"adjAntiFatal":21,"adjIgnoreArmor":0.0921,"adjDmgArmor":0.0361,"adjMortal":0.3524,"adjAntiMortal":0.1908,"adjRealDmg":48,"adjRealDmgDef":48,"adjMonsterDmg":0.2956,"adjMonsterDmgAnti":0.2139,"adjFinalDmg":0.0883,"adjFinalDmgAnti":0.0443,"adjStunEnh":9,"adjStunAnti":9,"adjSilentEnh":9,"adjSilentAnti":9,"adjKnockEnh":9,"adjKnockAnti":9,"adjFrozenEnh":9,"adjFrozenAnti":9,"adjSlowEnh":9,"adjSlowAnti":9,"adjPushEnh":9,"adjPushAnti":9})
    }),
    51000049: _tools.RODict({
        "propID": 51000049,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":823,"adjMinPhysicalAtk":699,"adjMaxPhysicalAtk":699,"adjMinMagicAtk":699,"adjMaxMagicAtk":699,"adjMinPhysicalArmor":370,"adjMaxPhysicalArmor":370,"adjMinMagicArmor":370,"adjMaxMagicArmor":370,"adjAccuracy":14,"adjEvasion":9,"adjFatal":28,"adjAntiFatal":22,"adjIgnoreArmor":0.0951,"adjDmgArmor":0.037,"adjMortal":0.3689,"adjAntiMortal":0.1996,"adjRealDmg":49,"adjRealDmgDef":49,"adjMonsterDmg":0.3039,"adjMonsterDmgAnti":0.2222,"adjFinalDmg":0.0934,"adjFinalDmgAnti":0.0464,"adjStunEnh":9,"adjStunAnti":9,"adjSilentEnh":9,"adjSilentAnti":9,"adjKnockEnh":9,"adjKnockAnti":9,"adjFrozenEnh":9,"adjFrozenAnti":9,"adjSlowEnh":9,"adjSlowAnti":9,"adjPushEnh":9,"adjPushAnti":9})
    }),
    51000050: _tools.RODict({
        "propID": 51000050,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":853,"adjMinPhysicalAtk":711,"adjMaxPhysicalAtk":711,"adjMinMagicAtk":711,"adjMaxMagicAtk":711,"adjMinPhysicalArmor":378,"adjMaxPhysicalArmor":378,"adjMinMagicArmor":378,"adjMaxMagicArmor":378,"adjAccuracy":15,"adjEvasion":10,"adjFatal":28,"adjAntiFatal":23,"adjIgnoreArmor":0.098,"adjDmgArmor":0.038,"adjMortal":0.3853,"adjAntiMortal":0.2083,"adjRealDmg":50,"adjRealDmgDef":50,"adjMonsterDmg":0.3122,"adjMonsterDmgAnti":0.2304,"adjFinalDmg":0.0985,"adjFinalDmgAnti":0.0485,"adjStunEnh":10,"adjStunAnti":10,"adjSilentEnh":10,"adjSilentAnti":10,"adjKnockEnh":10,"adjKnockAnti":10,"adjFrozenEnh":10,"adjFrozenAnti":10,"adjSlowEnh":10,"adjSlowAnti":10,"adjPushEnh":10,"adjPushAnti":10})
    }),
    51000051: _tools.RODict({
        "propID": 51000051,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":869,"adjMinPhysicalAtk":734,"adjMaxPhysicalAtk":734,"adjMinMagicAtk":734,"adjMaxMagicAtk":734,"adjMinPhysicalArmor":390,"adjMaxPhysicalArmor":390,"adjMinMagicArmor":390,"adjMaxMagicArmor":390,"adjAccuracy":15,"adjEvasion":10,"adjFatal":29,"adjAntiFatal":23,"adjIgnoreArmor":0.0998,"adjDmgArmor":0.0398,"adjMortal":0.3935,"adjAntiMortal":0.2158,"adjRealDmg":51,"adjRealDmgDef":51,"adjMonsterDmg":0.3223,"adjMonsterDmgAnti":0.2404,"adjFinalDmg":0.1003,"adjFinalDmgAnti":0.0503,"adjStunEnh":10,"adjStunAnti":10,"adjSilentEnh":10,"adjSilentAnti":10,"adjKnockEnh":10,"adjKnockAnti":10,"adjFrozenEnh":10,"adjFrozenAnti":10,"adjSlowEnh":10,"adjSlowAnti":10,"adjPushEnh":10,"adjPushAnti":10})
    }),
    51000052: _tools.RODict({
        "propID": 51000052,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":885,"adjMinPhysicalAtk":758,"adjMaxPhysicalAtk":758,"adjMinMagicAtk":758,"adjMaxMagicAtk":758,"adjMinPhysicalArmor":403,"adjMaxPhysicalArmor":403,"adjMinMagicArmor":403,"adjMaxMagicArmor":403,"adjAccuracy":16,"adjEvasion":11,"adjFatal":30,"adjAntiFatal":24,"adjIgnoreArmor":0.1015,"adjDmgArmor":0.0415,"adjMortal":0.4017,"adjAntiMortal":0.2233,"adjRealDmg":52,"adjRealDmgDef":52,"adjMonsterDmg":0.3323,"adjMonsterDmgAnti":0.2504,"adjFinalDmg":0.1021,"adjFinalDmgAnti":0.0521,"adjStunEnh":11,"adjStunAnti":11,"adjSilentEnh":11,"adjSilentAnti":11,"adjKnockEnh":11,"adjKnockAnti":11,"adjFrozenEnh":11,"adjFrozenAnti":11,"adjSlowEnh":11,"adjSlowAnti":11,"adjPushEnh":11,"adjPushAnti":11})
    }),
    51000053: _tools.RODict({
        "propID": 51000053,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":901,"adjMinPhysicalAtk":781,"adjMaxPhysicalAtk":781,"adjMinMagicAtk":781,"adjMaxMagicAtk":781,"adjMinPhysicalArmor":416,"adjMaxPhysicalArmor":416,"adjMinMagicArmor":416,"adjMaxMagicArmor":416,"adjAccuracy":16,"adjEvasion":11,"adjFatal":31,"adjAntiFatal":24,"adjIgnoreArmor":0.1033,"adjDmgArmor":0.0433,"adjMortal":0.4098,"adjAntiMortal":0.2307,"adjRealDmg":53,"adjRealDmgDef":53,"adjMonsterDmg":0.3424,"adjMonsterDmgAnti":0.2604,"adjFinalDmg":0.1039,"adjFinalDmgAnti":0.0539,"adjStunEnh":11,"adjStunAnti":11,"adjSilentEnh":11,"adjSilentAnti":11,"adjKnockEnh":11,"adjKnockAnti":11,"adjFrozenEnh":11,"adjFrozenAnti":11,"adjSlowEnh":11,"adjSlowAnti":11,"adjPushEnh":11,"adjPushAnti":11})
    }),
    51000054: _tools.RODict({
        "propID": 51000054,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":917,"adjMinPhysicalAtk":805,"adjMaxPhysicalAtk":805,"adjMinMagicAtk":805,"adjMaxMagicAtk":805,"adjMinPhysicalArmor":428,"adjMaxPhysicalArmor":428,"adjMinMagicArmor":428,"adjMaxMagicArmor":428,"adjAccuracy":16,"adjEvasion":11,"adjFatal":32,"adjAntiFatal":25,"adjIgnoreArmor":0.105,"adjDmgArmor":0.045,"adjMortal":0.418,"adjAntiMortal":0.2382,"adjRealDmg":54,"adjRealDmgDef":54,"adjMonsterDmg":0.3525,"adjMonsterDmgAnti":0.2704,"adjFinalDmg":0.1057,"adjFinalDmgAnti":0.0557,"adjStunEnh":11,"adjStunAnti":11,"adjSilentEnh":11,"adjSilentAnti":11,"adjKnockEnh":11,"adjKnockAnti":11,"adjFrozenEnh":11,"adjFrozenAnti":11,"adjSlowEnh":11,"adjSlowAnti":11,"adjPushEnh":11,"adjPushAnti":11})
    }),
    51000055: _tools.RODict({
        "propID": 51000055,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":933,"adjMinPhysicalAtk":821,"adjMaxPhysicalAtk":821,"adjMinMagicAtk":821,"adjMaxMagicAtk":821,"adjMinPhysicalArmor":441,"adjMaxPhysicalArmor":441,"adjMinMagicArmor":441,"adjMaxMagicArmor":441,"adjAccuracy":16,"adjEvasion":11,"adjFatal":32,"adjAntiFatal":25,"adjIgnoreArmor":0.1068,"adjDmgArmor":0.0468,"adjMortal":0.4262,"adjAntiMortal":0.2457,"adjRealDmg":55,"adjRealDmgDef":55,"adjMonsterDmg":0.3626,"adjMonsterDmgAnti":0.2803,"adjFinalDmg":0.1075,"adjFinalDmgAnti":0.0575,"adjStunEnh":11,"adjStunAnti":11,"adjSilentEnh":11,"adjSilentAnti":11,"adjKnockEnh":11,"adjKnockAnti":11,"adjFrozenEnh":11,"adjFrozenAnti":11,"adjSlowEnh":11,"adjSlowAnti":11,"adjPushEnh":11,"adjPushAnti":11})
    }),
    51000056: _tools.RODict({
        "propID": 51000056,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":950,"adjMinPhysicalAtk":846,"adjMaxPhysicalAtk":846,"adjMinMagicAtk":846,"adjMaxMagicAtk":846,"adjMinPhysicalArmor":454,"adjMaxPhysicalArmor":454,"adjMinMagicArmor":454,"adjMaxMagicArmor":454,"adjAccuracy":17,"adjEvasion":12,"adjFatal":33,"adjAntiFatal":26,"adjIgnoreArmor":0.1085,"adjDmgArmor":0.0485,"adjMortal":0.4343,"adjAntiMortal":0.2531,"adjRealDmg":56,"adjRealDmgDef":56,"adjMonsterDmg":0.3727,"adjMonsterDmgAnti":0.2903,"adjFinalDmg":0.1093,"adjFinalDmgAnti":0.0593,"adjStunEnh":12,"adjStunAnti":12,"adjSilentEnh":12,"adjSilentAnti":12,"adjKnockEnh":12,"adjKnockAnti":12,"adjFrozenEnh":12,"adjFrozenAnti":12,"adjSlowEnh":12,"adjSlowAnti":12,"adjPushEnh":12,"adjPushAnti":12})
    }),
    51000057: _tools.RODict({
        "propID": 51000057,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":967,"adjMinPhysicalAtk":870,"adjMaxPhysicalAtk":870,"adjMinMagicAtk":870,"adjMaxMagicAtk":870,"adjMinPhysicalArmor":466,"adjMaxPhysicalArmor":466,"adjMinMagicArmor":466,"adjMaxMagicArmor":466,"adjAccuracy":17,"adjEvasion":12,"adjFatal":34,"adjAntiFatal":26,"adjIgnoreArmor":0.1103,"adjDmgArmor":0.0503,"adjMortal":0.4425,"adjAntiMortal":0.2606,"adjRealDmg":57,"adjRealDmgDef":57,"adjMonsterDmg":0.3828,"adjMonsterDmgAnti":0.3003,"adjFinalDmg":0.1111,"adjFinalDmgAnti":0.0611,"adjStunEnh":12,"adjStunAnti":12,"adjSilentEnh":12,"adjSilentAnti":12,"adjKnockEnh":12,"adjKnockAnti":12,"adjFrozenEnh":12,"adjFrozenAnti":12,"adjSlowEnh":12,"adjSlowAnti":12,"adjPushEnh":12,"adjPushAnti":12})
    }),
    51000058: _tools.RODict({
        "propID": 51000058,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":983,"adjMinPhysicalAtk":891,"adjMaxPhysicalAtk":891,"adjMinMagicAtk":891,"adjMaxMagicAtk":891,"adjMinPhysicalArmor":479,"adjMaxPhysicalArmor":479,"adjMinMagicArmor":479,"adjMaxMagicArmor":479,"adjAccuracy":17,"adjEvasion":12,"adjFatal":35,"adjAntiFatal":27,"adjIgnoreArmor":0.112,"adjDmgArmor":0.052,"adjMortal":0.4507,"adjAntiMortal":0.2681,"adjRealDmg":58,"adjRealDmgDef":58,"adjMonsterDmg":0.3928,"adjMonsterDmgAnti":0.3103,"adjFinalDmg":0.1129,"adjFinalDmgAnti":0.0629,"adjStunEnh":12,"adjStunAnti":12,"adjSilentEnh":12,"adjSilentAnti":12,"adjKnockEnh":12,"adjKnockAnti":12,"adjFrozenEnh":12,"adjFrozenAnti":12,"adjSlowEnh":12,"adjSlowAnti":12,"adjPushEnh":12,"adjPushAnti":12})
    }),
    51000059: _tools.RODict({
        "propID": 51000059,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1000,"adjMinPhysicalAtk":912,"adjMaxPhysicalAtk":912,"adjMinMagicAtk":912,"adjMaxMagicAtk":912,"adjMinPhysicalArmor":491,"adjMaxPhysicalArmor":491,"adjMinMagicArmor":491,"adjMaxMagicArmor":491,"adjAccuracy":17,"adjEvasion":12,"adjFatal":36,"adjAntiFatal":27,"adjIgnoreArmor":0.1138,"adjDmgArmor":0.0538,"adjMortal":0.4588,"adjAntiMortal":0.2755,"adjRealDmg":59,"adjRealDmgDef":59,"adjMonsterDmg":0.4029,"adjMonsterDmgAnti":0.3203,"adjFinalDmg":0.1147,"adjFinalDmgAnti":0.0647,"adjStunEnh":12,"adjStunAnti":12,"adjSilentEnh":12,"adjSilentAnti":12,"adjKnockEnh":12,"adjKnockAnti":12,"adjFrozenEnh":12,"adjFrozenAnti":12,"adjSlowEnh":12,"adjSlowAnti":12,"adjPushEnh":12,"adjPushAnti":12})
    }),
    51000060: _tools.RODict({
        "propID": 51000060,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1032,"adjMinPhysicalAtk":933,"adjMaxPhysicalAtk":933,"adjMinMagicAtk":933,"adjMaxMagicAtk":933,"adjMinPhysicalArmor":504,"adjMaxPhysicalArmor":504,"adjMinMagicArmor":504,"adjMaxMagicArmor":504,"adjAccuracy":18,"adjEvasion":13,"adjFatal":37,"adjAntiFatal":28,"adjIgnoreArmor":0.1155,"adjDmgArmor":0.0555,"adjMortal":0.467,"adjAntiMortal":0.283,"adjRealDmg":60,"adjRealDmgDef":60,"adjMonsterDmg":0.413,"adjMonsterDmgAnti":0.3302,"adjFinalDmg":0.1165,"adjFinalDmgAnti":0.0665,"adjStunEnh":13,"adjStunAnti":13,"adjSilentEnh":13,"adjSilentAnti":13,"adjKnockEnh":13,"adjKnockAnti":13,"adjFrozenEnh":13,"adjFrozenAnti":13,"adjSlowEnh":13,"adjSlowAnti":13,"adjPushEnh":13,"adjPushAnti":13})
    }),
    51000061: _tools.RODict({
        "propID": 51000061,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1046,"adjMinPhysicalAtk":955,"adjMaxPhysicalAtk":955,"adjMinMagicAtk":955,"adjMaxMagicAtk":955,"adjMinPhysicalArmor":517,"adjMaxPhysicalArmor":517,"adjMinMagicArmor":517,"adjMaxMagicArmor":517,"adjAccuracy":18,"adjEvasion":13,"adjFatal":37,"adjAntiFatal":28,"adjIgnoreArmor":0.1164,"adjDmgArmor":0.0564,"adjMortal":0.4748,"adjAntiMortal":0.2911,"adjRealDmg":61,"adjRealDmgDef":61,"adjMonsterDmg":0.4214,"adjMonsterDmgAnti":0.3385,"adjFinalDmg":0.1184,"adjFinalDmgAnti":0.0684,"adjStunEnh":13,"adjStunAnti":13,"adjSilentEnh":13,"adjSilentAnti":13,"adjKnockEnh":13,"adjKnockAnti":13,"adjFrozenEnh":13,"adjFrozenAnti":13,"adjSlowEnh":13,"adjSlowAnti":13,"adjPushEnh":13,"adjPushAnti":13})
    }),
    51000062: _tools.RODict({
        "propID": 51000062,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1061,"adjMinPhysicalAtk":977,"adjMaxPhysicalAtk":977,"adjMinMagicAtk":977,"adjMaxMagicAtk":977,"adjMinPhysicalArmor":531,"adjMaxPhysicalArmor":531,"adjMinMagicArmor":531,"adjMaxMagicArmor":531,"adjAccuracy":18,"adjEvasion":13,"adjFatal":38,"adjAntiFatal":29,"adjIgnoreArmor":0.1173,"adjDmgArmor":0.0573,"adjMortal":0.4825,"adjAntiMortal":0.2991,"adjRealDmg":62,"adjRealDmgDef":62,"adjMonsterDmg":0.4298,"adjMonsterDmgAnti":0.3468,"adjFinalDmg":0.1204,"adjFinalDmgAnti":0.0704,"adjStunEnh":13,"adjStunAnti":13,"adjSilentEnh":13,"adjSilentAnti":13,"adjKnockEnh":13,"adjKnockAnti":13,"adjFrozenEnh":13,"adjFrozenAnti":13,"adjSlowEnh":13,"adjSlowAnti":13,"adjPushEnh":13,"adjPushAnti":13})
    }),
    51000063: _tools.RODict({
        "propID": 51000063,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1075,"adjMinPhysicalAtk":1000,"adjMaxPhysicalAtk":1000,"adjMinMagicAtk":1000,"adjMaxMagicAtk":1000,"adjMinPhysicalArmor":544,"adjMaxPhysicalArmor":544,"adjMinMagicArmor":544,"adjMaxMagicArmor":544,"adjAccuracy":19,"adjEvasion":14,"adjFatal":38,"adjAntiFatal":29,"adjIgnoreArmor":0.1182,"adjDmgArmor":0.0582,"adjMortal":0.4903,"adjAntiMortal":0.3072,"adjRealDmg":63,"adjRealDmgDef":63,"adjMonsterDmg":0.4382,"adjMonsterDmgAnti":0.3551,"adjFinalDmg":0.1224,"adjFinalDmgAnti":0.0723,"adjStunEnh":13,"adjStunAnti":13,"adjSilentEnh":13,"adjSilentAnti":13,"adjKnockEnh":13,"adjKnockAnti":13,"adjFrozenEnh":13,"adjFrozenAnti":13,"adjSlowEnh":13,"adjSlowAnti":13,"adjPushEnh":13,"adjPushAnti":13})
    }),
    51000064: _tools.RODict({
        "propID": 51000064,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1090,"adjMinPhysicalAtk":1027,"adjMaxPhysicalAtk":1027,"adjMinMagicAtk":1027,"adjMaxMagicAtk":1027,"adjMinPhysicalArmor":557,"adjMaxPhysicalArmor":557,"adjMinMagicArmor":557,"adjMaxMagicArmor":557,"adjAccuracy":19,"adjEvasion":14,"adjFatal":39,"adjAntiFatal":30,"adjIgnoreArmor":0.1191,"adjDmgArmor":0.0591,"adjMortal":0.4981,"adjAntiMortal":0.3153,"adjRealDmg":64,"adjRealDmgDef":64,"adjMonsterDmg":0.4465,"adjMonsterDmgAnti":0.3634,"adjFinalDmg":0.1243,"adjFinalDmgAnti":0.0743,"adjStunEnh":14,"adjStunAnti":14,"adjSilentEnh":14,"adjSilentAnti":14,"adjKnockEnh":14,"adjKnockAnti":14,"adjFrozenEnh":14,"adjFrozenAnti":14,"adjSlowEnh":14,"adjSlowAnti":14,"adjPushEnh":14,"adjPushAnti":14})
    }),
    51000065: _tools.RODict({
        "propID": 51000065,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1105,"adjMinPhysicalAtk":1050,"adjMaxPhysicalAtk":1050,"adjMinMagicAtk":1050,"adjMaxMagicAtk":1050,"adjMinPhysicalArmor":570,"adjMaxPhysicalArmor":570,"adjMinMagicArmor":570,"adjMaxMagicArmor":570,"adjAccuracy":20,"adjEvasion":15,"adjFatal":39,"adjAntiFatal":30,"adjIgnoreArmor":0.12,"adjDmgArmor":0.06,"adjMortal":0.5058,"adjAntiMortal":0.3233,"adjRealDmg":65,"adjRealDmgDef":65,"adjMonsterDmg":0.4549,"adjMonsterDmgAnti":0.3717,"adjFinalDmg":0.1263,"adjFinalDmgAnti":0.0762,"adjStunEnh":14,"adjStunAnti":14,"adjSilentEnh":14,"adjSilentAnti":14,"adjKnockEnh":14,"adjKnockAnti":14,"adjFrozenEnh":14,"adjFrozenAnti":14,"adjSlowEnh":14,"adjSlowAnti":14,"adjPushEnh":14,"adjPushAnti":14})
    }),
    51000066: _tools.RODict({
        "propID": 51000066,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1120,"adjMinPhysicalAtk":1072,"adjMaxPhysicalAtk":1072,"adjMinMagicAtk":1072,"adjMaxMagicAtk":1072,"adjMinPhysicalArmor":584,"adjMaxPhysicalArmor":584,"adjMinMagicArmor":584,"adjMaxMagicArmor":584,"adjAccuracy":20,"adjEvasion":15,"adjFatal":39,"adjAntiFatal":31,"adjIgnoreArmor":0.1209,"adjDmgArmor":0.0609,"adjMortal":0.5136,"adjAntiMortal":0.3314,"adjRealDmg":66,"adjRealDmgDef":66,"adjMonsterDmg":0.4633,"adjMonsterDmgAnti":0.3799,"adjFinalDmg":0.1282,"adjFinalDmgAnti":0.0782,"adjStunEnh":14,"adjStunAnti":14,"adjSilentEnh":14,"adjSilentAnti":14,"adjKnockEnh":14,"adjKnockAnti":14,"adjFrozenEnh":14,"adjFrozenAnti":14,"adjSlowEnh":14,"adjSlowAnti":14,"adjPushEnh":14,"adjPushAnti":14})
    }),
    51000067: _tools.RODict({
        "propID": 51000067,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1135,"adjMinPhysicalAtk":1095,"adjMaxPhysicalAtk":1095,"adjMinMagicAtk":1095,"adjMaxMagicAtk":1095,"adjMinPhysicalArmor":597,"adjMaxPhysicalArmor":597,"adjMinMagicArmor":597,"adjMaxMagicArmor":597,"adjAccuracy":21,"adjEvasion":16,"adjFatal":40,"adjAntiFatal":31,"adjIgnoreArmor":0.1218,"adjDmgArmor":0.0618,"adjMortal":0.5214,"adjAntiMortal":0.3395,"adjRealDmg":67,"adjRealDmgDef":67,"adjMonsterDmg":0.4717,"adjMonsterDmgAnti":0.3882,"adjFinalDmg":0.1302,"adjFinalDmgAnti":0.0801,"adjStunEnh":14,"adjStunAnti":14,"adjSilentEnh":14,"adjSilentAnti":14,"adjKnockEnh":14,"adjKnockAnti":14,"adjFrozenEnh":14,"adjFrozenAnti":14,"adjSlowEnh":14,"adjSlowAnti":14,"adjPushEnh":14,"adjPushAnti":14})
    }),
    51000068: _tools.RODict({
        "propID": 51000068,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1150,"adjMinPhysicalAtk":1119,"adjMaxPhysicalAtk":1119,"adjMinMagicAtk":1119,"adjMaxMagicAtk":1119,"adjMinPhysicalArmor":610,"adjMaxPhysicalArmor":610,"adjMinMagicArmor":610,"adjMaxMagicArmor":610,"adjAccuracy":21,"adjEvasion":16,"adjFatal":40,"adjAntiFatal":31,"adjIgnoreArmor":0.1227,"adjDmgArmor":0.0627,"adjMortal":0.5291,"adjAntiMortal":0.3475,"adjRealDmg":68,"adjRealDmgDef":68,"adjMonsterDmg":0.4801,"adjMonsterDmgAnti":0.3965,"adjFinalDmg":0.1321,"adjFinalDmgAnti":0.0821,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15,"adjPushEnh":15,"adjPushAnti":15})
    }),
    51000069: _tools.RODict({
        "propID": 51000069,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1165,"adjMinPhysicalAtk":1142,"adjMaxPhysicalAtk":1142,"adjMinMagicAtk":1142,"adjMaxMagicAtk":1142,"adjMinPhysicalArmor":624,"adjMaxPhysicalArmor":624,"adjMinMagicArmor":624,"adjMaxMagicArmor":624,"adjAccuracy":22,"adjEvasion":17,"adjFatal":41,"adjAntiFatal":32,"adjIgnoreArmor":0.1236,"adjDmgArmor":0.0636,"adjMortal":0.5369,"adjAntiMortal":0.3556,"adjRealDmg":69,"adjRealDmgDef":69,"adjMonsterDmg":0.4885,"adjMonsterDmgAnti":0.4048,"adjFinalDmg":0.1341,"adjFinalDmgAnti":0.084,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15,"adjPushEnh":15,"adjPushAnti":15})
    }),
    51000070: _tools.RODict({
        "propID": 51000070,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1199,"adjMinPhysicalAtk":1160,"adjMaxPhysicalAtk":1160,"adjMinMagicAtk":1160,"adjMaxMagicAtk":1160,"adjMinPhysicalArmor":637,"adjMaxPhysicalArmor":637,"adjMinMagicArmor":637,"adjMaxMagicArmor":637,"adjAccuracy":22,"adjEvasion":17,"adjFatal":41,"adjAntiFatal":32,"adjIgnoreArmor":0.1245,"adjDmgArmor":0.0645,"adjMortal":0.5447,"adjAntiMortal":0.3637,"adjRealDmg":70,"adjRealDmgDef":70,"adjMonsterDmg":0.4968,"adjMonsterDmgAnti":0.4131,"adjFinalDmg":0.136,"adjFinalDmgAnti":0.086,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15,"adjPushEnh":15,"adjPushAnti":15})
    }),
    51000071: _tools.RODict({
        "propID": 51000071,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1236,"adjMinPhysicalAtk":1177,"adjMaxPhysicalAtk":1177,"adjMinMagicAtk":1177,"adjMaxMagicAtk":1177,"adjMinPhysicalArmor":650,"adjMaxPhysicalArmor":650,"adjMinMagicArmor":650,"adjMaxMagicArmor":650,"adjAccuracy":22,"adjEvasion":17,"adjFatal":42,"adjAntiFatal":33,"adjIgnoreArmor":0.132,"adjDmgArmor":0.066,"adjMortal":0.5708,"adjAntiMortal":0.3738,"adjRealDmg":71,"adjRealDmgDef":71,"adjMonsterDmg":0.5143,"adjMonsterDmgAnti":0.4223,"adjFinalDmg":0.1433,"adjFinalDmgAnti":0.0882,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15,"adjPushEnh":15,"adjPushAnti":15})
    }),
    51000072: _tools.RODict({
        "propID": 51000072,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1275,"adjMinPhysicalAtk":1194,"adjMaxPhysicalAtk":1194,"adjMinMagicAtk":1194,"adjMaxMagicAtk":1194,"adjMinPhysicalArmor":663,"adjMaxPhysicalArmor":663,"adjMinMagicArmor":663,"adjMaxMagicArmor":663,"adjAccuracy":23,"adjEvasion":18,"adjFatal":43,"adjAntiFatal":33,"adjIgnoreArmor":0.1395,"adjDmgArmor":0.0675,"adjMortal":0.597,"adjAntiMortal":0.384,"adjRealDmg":72,"adjRealDmgDef":72,"adjMonsterDmg":0.5317,"adjMonsterDmgAnti":0.4315,"adjFinalDmg":0.1505,"adjFinalDmgAnti":0.0905,"adjStunEnh":16,"adjStunAnti":16,"adjSilentEnh":16,"adjSilentAnti":16,"adjKnockEnh":16,"adjKnockAnti":16,"adjFrozenEnh":16,"adjFrozenAnti":16,"adjSlowEnh":16,"adjSlowAnti":16,"adjPushEnh":16,"adjPushAnti":16})
    }),
    51000073: _tools.RODict({
        "propID": 51000073,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1314,"adjMinPhysicalAtk":1211,"adjMaxPhysicalAtk":1211,"adjMinMagicAtk":1211,"adjMaxMagicAtk":1211,"adjMinPhysicalArmor":676,"adjMaxPhysicalArmor":676,"adjMinMagicArmor":676,"adjMaxMagicArmor":676,"adjAccuracy":23,"adjEvasion":18,"adjFatal":43,"adjAntiFatal":34,"adjIgnoreArmor":0.147,"adjDmgArmor":0.069,"adjMortal":0.6232,"adjAntiMortal":0.3942,"adjRealDmg":73,"adjRealDmgDef":73,"adjMonsterDmg":0.5491,"adjMonsterDmgAnti":0.4407,"adjFinalDmg":0.1578,"adjFinalDmgAnti":0.0927,"adjStunEnh":16,"adjStunAnti":16,"adjSilentEnh":16,"adjSilentAnti":16,"adjKnockEnh":16,"adjKnockAnti":16,"adjFrozenEnh":16,"adjFrozenAnti":16,"adjSlowEnh":16,"adjSlowAnti":16,"adjPushEnh":16,"adjPushAnti":16})
    }),
    51000074: _tools.RODict({
        "propID": 51000074,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1354,"adjMinPhysicalAtk":1222,"adjMaxPhysicalAtk":1222,"adjMinMagicAtk":1222,"adjMaxMagicAtk":1222,"adjMinPhysicalArmor":689,"adjMaxPhysicalArmor":689,"adjMinMagicArmor":689,"adjMaxMagicArmor":689,"adjAccuracy":23,"adjEvasion":18,"adjFatal":44,"adjAntiFatal":35,"adjIgnoreArmor":0.1545,"adjDmgArmor":0.0705,"adjMortal":0.6493,"adjAntiMortal":0.4043,"adjRealDmg":74,"adjRealDmgDef":74,"adjMonsterDmg":0.5666,"adjMonsterDmgAnti":0.4499,"adjFinalDmg":0.165,"adjFinalDmgAnti":0.095,"adjStunEnh":16,"adjStunAnti":16,"adjSilentEnh":16,"adjSilentAnti":16,"adjKnockEnh":16,"adjKnockAnti":16,"adjFrozenEnh":16,"adjFrozenAnti":16,"adjSlowEnh":16,"adjSlowAnti":16,"adjPushEnh":16,"adjPushAnti":16})
    }),
    51000075: _tools.RODict({
        "propID": 51000075,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1396,"adjMinPhysicalAtk":1239,"adjMaxPhysicalAtk":1239,"adjMinMagicAtk":1239,"adjMaxMagicAtk":1239,"adjMinPhysicalArmor":702,"adjMaxPhysicalArmor":702,"adjMinMagicArmor":702,"adjMaxMagicArmor":702,"adjAccuracy":23,"adjEvasion":18,"adjFatal":44,"adjAntiFatal":35,"adjIgnoreArmor":0.162,"adjDmgArmor":0.072,"adjMortal":0.6755,"adjAntiMortal":0.4145,"adjRealDmg":75,"adjRealDmgDef":75,"adjMonsterDmg":0.584,"adjMonsterDmgAnti":0.4591,"adjFinalDmg":0.1723,"adjFinalDmgAnti":0.0973,"adjStunEnh":16,"adjStunAnti":16,"adjSilentEnh":16,"adjSilentAnti":16,"adjKnockEnh":16,"adjKnockAnti":16,"adjFrozenEnh":16,"adjFrozenAnti":16,"adjSlowEnh":16,"adjSlowAnti":16,"adjPushEnh":16,"adjPushAnti":16})
    }),
    51000076: _tools.RODict({
        "propID": 51000076,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1439,"adjMinPhysicalAtk":1256,"adjMaxPhysicalAtk":1256,"adjMinMagicAtk":1256,"adjMaxMagicAtk":1256,"adjMinPhysicalArmor":715,"adjMaxPhysicalArmor":715,"adjMinMagicArmor":715,"adjMaxMagicArmor":715,"adjAccuracy":24,"adjEvasion":19,"adjFatal":45,"adjAntiFatal":36,"adjIgnoreArmor":0.1695,"adjDmgArmor":0.0735,"adjMortal":0.7017,"adjAntiMortal":0.4247,"adjRealDmg":76,"adjRealDmgDef":76,"adjMonsterDmg":0.6014,"adjMonsterDmgAnti":0.4683,"adjFinalDmg":0.1795,"adjFinalDmgAnti":0.0995,"adjStunEnh":17,"adjStunAnti":17,"adjSilentEnh":17,"adjSilentAnti":17,"adjKnockEnh":17,"adjKnockAnti":17,"adjFrozenEnh":17,"adjFrozenAnti":17,"adjSlowEnh":17,"adjSlowAnti":17,"adjPushEnh":17,"adjPushAnti":17})
    }),
    51000077: _tools.RODict({
        "propID": 51000077,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1483,"adjMinPhysicalAtk":1273,"adjMaxPhysicalAtk":1273,"adjMinMagicAtk":1273,"adjMaxMagicAtk":1273,"adjMinPhysicalArmor":728,"adjMaxPhysicalArmor":728,"adjMinMagicArmor":728,"adjMaxMagicArmor":728,"adjAccuracy":24,"adjEvasion":19,"adjFatal":46,"adjAntiFatal":36,"adjIgnoreArmor":0.177,"adjDmgArmor":0.075,"adjMortal":0.7278,"adjAntiMortal":0.4348,"adjRealDmg":77,"adjRealDmgDef":77,"adjMonsterDmg":0.6189,"adjMonsterDmgAnti":0.4775,"adjFinalDmg":0.1868,"adjFinalDmgAnti":0.1018,"adjStunEnh":17,"adjStunAnti":17,"adjSilentEnh":17,"adjSilentAnti":17,"adjKnockEnh":17,"adjKnockAnti":17,"adjFrozenEnh":17,"adjFrozenAnti":17,"adjSlowEnh":17,"adjSlowAnti":17,"adjPushEnh":17,"adjPushAnti":17})
    }),
    51000078: _tools.RODict({
        "propID": 51000078,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1528,"adjMinPhysicalAtk":1278,"adjMaxPhysicalAtk":1278,"adjMinMagicAtk":1278,"adjMaxMagicAtk":1278,"adjMinPhysicalArmor":741,"adjMaxPhysicalArmor":741,"adjMinMagicArmor":741,"adjMaxMagicArmor":741,"adjAccuracy":24,"adjEvasion":19,"adjFatal":46,"adjAntiFatal":37,"adjIgnoreArmor":0.1845,"adjDmgArmor":0.0765,"adjMortal":0.754,"adjAntiMortal":0.445,"adjRealDmg":78,"adjRealDmgDef":78,"adjMonsterDmg":0.6363,"adjMonsterDmgAnti":0.4868,"adjFinalDmg":0.194,"adjFinalDmgAnti":0.104,"adjStunEnh":17,"adjStunAnti":17,"adjSilentEnh":17,"adjSilentAnti":17,"adjKnockEnh":17,"adjKnockAnti":17,"adjFrozenEnh":17,"adjFrozenAnti":17,"adjSlowEnh":17,"adjSlowAnti":17,"adjPushEnh":17,"adjPushAnti":17})
    }),
    51000079: _tools.RODict({
        "propID": 51000079,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1574,"adjMinPhysicalAtk":1295,"adjMaxPhysicalAtk":1295,"adjMinMagicAtk":1295,"adjMaxMagicAtk":1295,"adjMinPhysicalArmor":754,"adjMaxPhysicalArmor":754,"adjMinMagicArmor":754,"adjMaxMagicArmor":754,"adjAccuracy":24,"adjEvasion":19,"adjFatal":47,"adjAntiFatal":37,"adjIgnoreArmor":0.192,"adjDmgArmor":0.078,"adjMortal":0.7802,"adjAntiMortal":0.4552,"adjRealDmg":79,"adjRealDmgDef":79,"adjMonsterDmg":0.6537,"adjMonsterDmgAnti":0.496,"adjFinalDmg":0.2013,"adjFinalDmgAnti":0.1063,"adjStunEnh":17,"adjStunAnti":17,"adjSilentEnh":17,"adjSilentAnti":17,"adjKnockEnh":17,"adjKnockAnti":17,"adjFrozenEnh":17,"adjFrozenAnti":17,"adjSlowEnh":17,"adjSlowAnti":17,"adjPushEnh":17,"adjPushAnti":17})
    }),
    51000080: _tools.RODict({
        "propID": 51000080,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1622,"adjMinPhysicalAtk":1311,"adjMaxPhysicalAtk":1311,"adjMinMagicAtk":1311,"adjMaxMagicAtk":1311,"adjMinPhysicalArmor":767,"adjMaxPhysicalArmor":767,"adjMinMagicArmor":767,"adjMaxMagicArmor":767,"adjAccuracy":25,"adjEvasion":20,"adjFatal":47,"adjAntiFatal":38,"adjIgnoreArmor":0.1995,"adjDmgArmor":0.0795,"adjMortal":0.8063,"adjAntiMortal":0.4653,"adjRealDmg":80,"adjRealDmgDef":80,"adjMonsterDmg":0.6712,"adjMonsterDmgAnti":0.5052,"adjFinalDmg":0.2085,"adjFinalDmgAnti":0.1085,"adjStunEnh":18,"adjStunAnti":18,"adjSilentEnh":18,"adjSilentAnti":18,"adjKnockEnh":18,"adjKnockAnti":18,"adjFrozenEnh":18,"adjFrozenAnti":18,"adjSlowEnh":18,"adjSlowAnti":18,"adjPushEnh":18,"adjPushAnti":18})
    }),
    51000081: _tools.RODict({
        "propID": 51000081,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1644,"adjMinPhysicalAtk":1327,"adjMaxPhysicalAtk":1327,"adjMinMagicAtk":1327,"adjMaxMagicAtk":1327,"adjMinPhysicalArmor":777,"adjMaxPhysicalArmor":777,"adjMinMagicArmor":777,"adjMaxMagicArmor":777,"adjAccuracy":25,"adjEvasion":20,"adjFatal":48,"adjAntiFatal":38,"adjIgnoreArmor":0.2006,"adjDmgArmor":0.0805,"adjMortal":0.8172,"adjAntiMortal":0.4765,"adjRealDmg":81,"adjRealDmgDef":81,"adjMonsterDmg":0.6802,"adjMonsterDmgAnti":0.5143,"adjFinalDmg":0.2112,"adjFinalDmgAnti":0.1112,"adjStunEnh":18,"adjStunAnti":18,"adjSilentEnh":18,"adjSilentAnti":18,"adjKnockEnh":18,"adjKnockAnti":18,"adjFrozenEnh":18,"adjFrozenAnti":18,"adjSlowEnh":18,"adjSlowAnti":18,"adjPushEnh":18,"adjPushAnti":18})
    }),
    51000082: _tools.RODict({
        "propID": 51000082,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1665,"adjMinPhysicalAtk":1343,"adjMaxPhysicalAtk":1343,"adjMinMagicAtk":1343,"adjMaxMagicAtk":1343,"adjMinPhysicalArmor":788,"adjMaxPhysicalArmor":788,"adjMinMagicArmor":788,"adjMaxMagicArmor":788,"adjAccuracy":25,"adjEvasion":20,"adjFatal":48,"adjAntiFatal":39,"adjIgnoreArmor":0.2016,"adjDmgArmor":0.0816,"adjMortal":0.8281,"adjAntiMortal":0.4877,"adjRealDmg":82,"adjRealDmgDef":82,"adjMonsterDmg":0.6892,"adjMonsterDmgAnti":0.5233,"adjFinalDmg":0.214,"adjFinalDmgAnti":0.1139,"adjStunEnh":18,"adjStunAnti":18,"adjSilentEnh":18,"adjSilentAnti":18,"adjKnockEnh":18,"adjKnockAnti":18,"adjFrozenEnh":18,"adjFrozenAnti":18,"adjSlowEnh":18,"adjSlowAnti":18,"adjPushEnh":18,"adjPushAnti":18})
    }),
    51000083: _tools.RODict({
        "propID": 51000083,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1687,"adjMinPhysicalAtk":1359,"adjMaxPhysicalAtk":1359,"adjMinMagicAtk":1359,"adjMaxMagicAtk":1359,"adjMinPhysicalArmor":798,"adjMaxPhysicalArmor":798,"adjMinMagicArmor":798,"adjMaxMagicArmor":798,"adjAccuracy":25,"adjEvasion":20,"adjFatal":49,"adjAntiFatal":39,"adjIgnoreArmor":0.2026,"adjDmgArmor":0.0826,"adjMortal":0.8389,"adjAntiMortal":0.4988,"adjRealDmg":83,"adjRealDmgDef":83,"adjMonsterDmg":0.6983,"adjMonsterDmgAnti":0.5324,"adjFinalDmg":0.2167,"adjFinalDmgAnti":0.1167,"adjStunEnh":18,"adjStunAnti":18,"adjSilentEnh":18,"adjSilentAnti":18,"adjKnockEnh":18,"adjKnockAnti":18,"adjFrozenEnh":18,"adjFrozenAnti":18,"adjSlowEnh":18,"adjSlowAnti":18,"adjPushEnh":18,"adjPushAnti":18})
    }),
    51000084: _tools.RODict({
        "propID": 51000084,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1708,"adjMinPhysicalAtk":1374,"adjMaxPhysicalAtk":1374,"adjMinMagicAtk":1374,"adjMaxMagicAtk":1374,"adjMinPhysicalArmor":808,"adjMaxPhysicalArmor":808,"adjMinMagicArmor":808,"adjMaxMagicArmor":808,"adjAccuracy":26,"adjEvasion":21,"adjFatal":49,"adjAntiFatal":40,"adjIgnoreArmor":0.2037,"adjDmgArmor":0.0837,"adjMortal":0.8498,"adjAntiMortal":0.51,"adjRealDmg":84,"adjRealDmgDef":84,"adjMonsterDmg":0.7073,"adjMonsterDmgAnti":0.5415,"adjFinalDmg":0.2194,"adjFinalDmgAnti":0.1194,"adjStunEnh":19,"adjStunAnti":19,"adjSilentEnh":19,"adjSilentAnti":19,"adjKnockEnh":19,"adjKnockAnti":19,"adjFrozenEnh":19,"adjFrozenAnti":19,"adjSlowEnh":19,"adjSlowAnti":19,"adjPushEnh":19,"adjPushAnti":19})
    }),
    51000085: _tools.RODict({
        "propID": 51000085,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1730,"adjMinPhysicalAtk":1390,"adjMaxPhysicalAtk":1390,"adjMinMagicAtk":1390,"adjMaxMagicAtk":1390,"adjMinPhysicalArmor":818,"adjMaxPhysicalArmor":818,"adjMinMagicArmor":818,"adjMaxMagicArmor":818,"adjAccuracy":26,"adjEvasion":21,"adjFatal":50,"adjAntiFatal":40,"adjIgnoreArmor":0.2047,"adjDmgArmor":0.0847,"adjMortal":0.8607,"adjAntiMortal":0.5212,"adjRealDmg":85,"adjRealDmgDef":85,"adjMonsterDmg":0.7163,"adjMonsterDmgAnti":0.5506,"adjFinalDmg":0.2221,"adjFinalDmgAnti":0.1221,"adjStunEnh":19,"adjStunAnti":19,"adjSilentEnh":19,"adjSilentAnti":19,"adjKnockEnh":19,"adjKnockAnti":19,"adjFrozenEnh":19,"adjFrozenAnti":19,"adjSlowEnh":19,"adjSlowAnti":19,"adjPushEnh":19,"adjPushAnti":19})
    }),
    51000086: _tools.RODict({
        "propID": 51000086,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1752,"adjMinPhysicalAtk":1419,"adjMaxPhysicalAtk":1419,"adjMinMagicAtk":1419,"adjMaxMagicAtk":1419,"adjMinPhysicalArmor":829,"adjMaxPhysicalArmor":829,"adjMinMagicArmor":829,"adjMaxMagicArmor":829,"adjAccuracy":26,"adjEvasion":21,"adjFatal":50,"adjAntiFatal":41,"adjIgnoreArmor":0.2058,"adjDmgArmor":0.0858,"adjMortal":0.8715,"adjAntiMortal":0.5323,"adjRealDmg":86,"adjRealDmgDef":86,"adjMonsterDmg":0.7254,"adjMonsterDmgAnti":0.5597,"adjFinalDmg":0.2249,"adjFinalDmgAnti":0.1249,"adjStunEnh":19,"adjStunAnti":19,"adjSilentEnh":19,"adjSilentAnti":19,"adjKnockEnh":19,"adjKnockAnti":19,"adjFrozenEnh":19,"adjFrozenAnti":19,"adjSlowEnh":19,"adjSlowAnti":19,"adjPushEnh":19,"adjPushAnti":19})
    }),
    51000087: _tools.RODict({
        "propID": 51000087,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1774,"adjMinPhysicalAtk":1447,"adjMaxPhysicalAtk":1447,"adjMinMagicAtk":1447,"adjMaxMagicAtk":1447,"adjMinPhysicalArmor":839,"adjMaxPhysicalArmor":839,"adjMinMagicArmor":839,"adjMaxMagicArmor":839,"adjAccuracy":26,"adjEvasion":21,"adjFatal":51,"adjAntiFatal":41,"adjIgnoreArmor":0.2068,"adjDmgArmor":0.0868,"adjMortal":0.8824,"adjAntiMortal":0.5435,"adjRealDmg":87,"adjRealDmgDef":87,"adjMonsterDmg":0.7344,"adjMonsterDmgAnti":0.5688,"adjFinalDmg":0.2276,"adjFinalDmgAnti":0.1276,"adjStunEnh":19,"adjStunAnti":19,"adjSilentEnh":19,"adjSilentAnti":19,"adjKnockEnh":19,"adjKnockAnti":19,"adjFrozenEnh":19,"adjFrozenAnti":19,"adjSlowEnh":19,"adjSlowAnti":19,"adjPushEnh":19,"adjPushAnti":19})
    }),
    51000088: _tools.RODict({
        "propID": 51000088,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1796,"adjMinPhysicalAtk":1464,"adjMaxPhysicalAtk":1464,"adjMinMagicAtk":1464,"adjMaxMagicAtk":1464,"adjMinPhysicalArmor":849,"adjMaxPhysicalArmor":849,"adjMinMagicArmor":849,"adjMaxMagicArmor":849,"adjAccuracy":27,"adjEvasion":22,"adjFatal":51,"adjAntiFatal":42,"adjIgnoreArmor":0.2079,"adjDmgArmor":0.0879,"adjMortal":0.8933,"adjAntiMortal":0.5547,"adjRealDmg":88,"adjRealDmgDef":88,"adjMonsterDmg":0.7434,"adjMonsterDmgAnti":0.5778,"adjFinalDmg":0.2303,"adjFinalDmgAnti":0.1303,"adjStunEnh":20,"adjStunAnti":20,"adjSilentEnh":20,"adjSilentAnti":20,"adjKnockEnh":20,"adjKnockAnti":20,"adjFrozenEnh":20,"adjFrozenAnti":20,"adjSlowEnh":20,"adjSlowAnti":20,"adjPushEnh":20,"adjPushAnti":20})
    }),
    51000089: _tools.RODict({
        "propID": 51000089,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1818,"adjMinPhysicalAtk":1480,"adjMaxPhysicalAtk":1480,"adjMinMagicAtk":1480,"adjMaxMagicAtk":1480,"adjMinPhysicalArmor":859,"adjMaxPhysicalArmor":859,"adjMinMagicArmor":859,"adjMaxMagicArmor":859,"adjAccuracy":27,"adjEvasion":22,"adjFatal":52,"adjAntiFatal":42,"adjIgnoreArmor":0.2089,"adjDmgArmor":0.0889,"adjMortal":0.9041,"adjAntiMortal":0.5658,"adjRealDmg":89,"adjRealDmgDef":89,"adjMonsterDmg":0.7525,"adjMonsterDmgAnti":0.5869,"adjFinalDmg":0.233,"adjFinalDmgAnti":0.133,"adjStunEnh":20,"adjStunAnti":20,"adjSilentEnh":20,"adjSilentAnti":20,"adjKnockEnh":20,"adjKnockAnti":20,"adjFrozenEnh":20,"adjFrozenAnti":20,"adjSlowEnh":20,"adjSlowAnti":20,"adjPushEnh":20,"adjPushAnti":20})
    }),
    51000090: _tools.RODict({
        "propID": 51000090,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1840,"adjMinPhysicalAtk":1496,"adjMaxPhysicalAtk":1496,"adjMinMagicAtk":1496,"adjMaxMagicAtk":1496,"adjMinPhysicalArmor":870,"adjMaxPhysicalArmor":870,"adjMinMagicArmor":870,"adjMaxMagicArmor":870,"adjAccuracy":27,"adjEvasion":22,"adjFatal":52,"adjAntiFatal":43,"adjIgnoreArmor":0.21,"adjDmgArmor":0.09,"adjMortal":0.915,"adjAntiMortal":0.577,"adjRealDmg":90,"adjRealDmgDef":90,"adjMonsterDmg":0.7615,"adjMonsterDmgAnti":0.596,"adjFinalDmg":0.2358,"adjFinalDmgAnti":0.1357,"adjStunEnh":20,"adjStunAnti":20,"adjSilentEnh":20,"adjSilentAnti":20,"adjKnockEnh":20,"adjKnockAnti":20,"adjFrozenEnh":20,"adjFrozenAnti":20,"adjSlowEnh":20,"adjSlowAnti":20,"adjPushEnh":20,"adjPushAnti":20})
    }),
    52004001: _tools.RODict({
        "propID": 52004001,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2200000,"adjMinPhysicalArmor":350,"adjMaxPhysicalArmor":350,"adjMinMagicArmor":350,"adjMaxMagicArmor":350})
    }),
    52004002: _tools.RODict({
        "propID": 52004002,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3000000,"adjMinPhysicalArmor":430,"adjMaxPhysicalArmor":430,"adjMinMagicArmor":430,"adjMaxMagicArmor":430})
    }),
    52004003: _tools.RODict({
        "propID": 52004003,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4450000,"adjMinPhysicalArmor":550,"adjMaxPhysicalArmor":550,"adjMinMagicArmor":550,"adjMaxMagicArmor":550})
    }),
    52004004: _tools.RODict({
        "propID": 52004004,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":6850000,"adjMinPhysicalArmor":760,"adjMaxPhysicalArmor":760,"adjMinMagicArmor":760,"adjMaxMagicArmor":760})
    }),
    52004005: _tools.RODict({
        "propID": 52004005,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":8900000,"adjMinPhysicalArmor":900,"adjMaxPhysicalArmor":900,"adjMinMagicArmor":900,"adjMaxMagicArmor":900})
    }),
    52004006: _tools.RODict({
        "propID": 52004006,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1100000,"adjMinPhysicalArmor":320,"adjMaxPhysicalArmor":320,"adjMinMagicArmor":320,"adjMaxMagicArmor":320})
    }),
    52004007: _tools.RODict({
        "propID": 52004007,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1500000,"adjMinPhysicalArmor":390,"adjMaxPhysicalArmor":390,"adjMinMagicArmor":390,"adjMaxMagicArmor":390})
    }),
    52004008: _tools.RODict({
        "propID": 52004008,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2200000,"adjMinPhysicalArmor":500,"adjMaxPhysicalArmor":500,"adjMinMagicArmor":500,"adjMaxMagicArmor":500})
    }),
    52004009: _tools.RODict({
        "propID": 52004009,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3400000,"adjMinPhysicalArmor":690,"adjMaxPhysicalArmor":690,"adjMinMagicArmor":690,"adjMaxMagicArmor":690})
    }),
    52004010: _tools.RODict({
        "propID": 52004010,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4450000,"adjMinPhysicalArmor":820,"adjMaxPhysicalArmor":820,"adjMinMagicArmor":820,"adjMaxMagicArmor":820})
    }),
    52004011: _tools.RODict({
        "propID": 52004011,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":363600,"adjMinPhysicalArmor":320,"adjMaxPhysicalArmor":320,"adjMinMagicArmor":320,"adjMaxMagicArmor":320})
    }),
    52004012: _tools.RODict({
        "propID": 52004012,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":498000,"adjMinPhysicalArmor":390,"adjMaxPhysicalArmor":390,"adjMinMagicArmor":390,"adjMaxMagicArmor":390})
    }),
    52004013: _tools.RODict({
        "propID": 52004013,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":741600,"adjMinPhysicalArmor":500,"adjMaxPhysicalArmor":500,"adjMinMagicArmor":500,"adjMaxMagicArmor":500})
    }),
    52004014: _tools.RODict({
        "propID": 52004014,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1138200,"adjMinPhysicalArmor":690,"adjMaxPhysicalArmor":690,"adjMinMagicArmor":690,"adjMaxMagicArmor":690})
    }),
    52004015: _tools.RODict({
        "propID": 52004015,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1485000,"adjMinPhysicalArmor":820,"adjMaxPhysicalArmor":820,"adjMinMagicArmor":820,"adjMaxMagicArmor":820})
    }),
    52004016: _tools.RODict({
        "propID": 52004016,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":181800,"adjMinPhysicalAtk":1600,"adjMaxPhysicalAtk":1600,"adjMinMagicAtk":1600,"adjMaxMagicAtk":1600,"adjMinPhysicalArmor":290,"adjMaxPhysicalArmor":290,"adjMinMagicArmor":290,"adjMaxMagicArmor":290})
    }),
    52004017: _tools.RODict({
        "propID": 52004017,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":249000,"adjMinPhysicalAtk":1950,"adjMaxPhysicalAtk":1950,"adjMinMagicAtk":1950,"adjMaxMagicAtk":1950,"adjMinPhysicalArmor":350,"adjMaxPhysicalArmor":350,"adjMinMagicArmor":350,"adjMaxMagicArmor":350})
    }),
    52004018: _tools.RODict({
        "propID": 52004018,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":370800,"adjMinPhysicalAtk":2500,"adjMaxPhysicalAtk":2500,"adjMinMagicAtk":2500,"adjMaxMagicAtk":2500,"adjMinPhysicalArmor":450,"adjMaxPhysicalArmor":450,"adjMinMagicArmor":450,"adjMaxMagicArmor":450})
    }),
    52004019: _tools.RODict({
        "propID": 52004019,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":569100,"adjMinPhysicalAtk":3300,"adjMaxPhysicalAtk":3300,"adjMinMagicAtk":3300,"adjMaxMagicAtk":3300,"adjMinPhysicalArmor":620,"adjMaxPhysicalArmor":620,"adjMinMagicArmor":620,"adjMaxMagicArmor":620})
    }),
    52004020: _tools.RODict({
        "propID": 52004020,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":742500,"adjMinPhysicalAtk":3800,"adjMaxPhysicalAtk":3800,"adjMinMagicAtk":3800,"adjMaxMagicAtk":3800,"adjMinPhysicalArmor":740,"adjMaxPhysicalArmor":740,"adjMinMagicArmor":740,"adjMaxMagicArmor":740})
    }),
    52004021: _tools.RODict({
        "propID": 52004021,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1250000,"adjMinPhysicalArmor":320,"adjMaxPhysicalArmor":320,"adjMinMagicArmor":320,"adjMaxMagicArmor":320})
    }),
    52004022: _tools.RODict({
        "propID": 52004022,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1500000,"adjMinPhysicalArmor":390,"adjMaxPhysicalArmor":390,"adjMinMagicArmor":390,"adjMaxMagicArmor":390})
    }),
    52004023: _tools.RODict({
        "propID": 52004023,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2000000,"adjMinPhysicalArmor":500,"adjMaxPhysicalArmor":500,"adjMinMagicArmor":500,"adjMaxMagicArmor":500})
    }),
    52004024: _tools.RODict({
        "propID": 52004024,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3000000,"adjMinPhysicalArmor":690,"adjMaxPhysicalArmor":690,"adjMinMagicArmor":690,"adjMaxMagicArmor":690})
    }),
    52004025: _tools.RODict({
        "propID": 52004025,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3600000,"adjMinPhysicalArmor":820,"adjMaxPhysicalArmor":820,"adjMinMagicArmor":820,"adjMaxMagicArmor":820})
    }),
    52004026: _tools.RODict({
        "propID": 52004026,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1350000,"adjMinPhysicalArmor":320,"adjMaxPhysicalArmor":320,"adjMinMagicArmor":320,"adjMaxMagicArmor":320})
    }),
    52004027: _tools.RODict({
        "propID": 52004027,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1650000,"adjMinPhysicalArmor":390,"adjMaxPhysicalArmor":390,"adjMinMagicArmor":390,"adjMaxMagicArmor":390})
    }),
    52004028: _tools.RODict({
        "propID": 52004028,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2450000,"adjMinPhysicalArmor":500,"adjMaxPhysicalArmor":500,"adjMinMagicArmor":500,"adjMaxMagicArmor":500})
    }),
    52004029: _tools.RODict({
        "propID": 52004029,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3750000,"adjMinPhysicalArmor":690,"adjMaxPhysicalArmor":690,"adjMinMagicArmor":690,"adjMaxMagicArmor":690})
    }),
    52004030: _tools.RODict({
        "propID": 52004030,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4900000,"adjMinPhysicalArmor":820,"adjMaxPhysicalArmor":820,"adjMinMagicArmor":820,"adjMaxMagicArmor":820})
    }),
    52004031: _tools.RODict({
        "propID": 52004031,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1125000,"adjMinPhysicalArmor":320,"adjMaxPhysicalArmor":320,"adjMinMagicArmor":320,"adjMaxMagicArmor":320})
    }),
    52004032: _tools.RODict({
        "propID": 52004032,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1350000,"adjMinPhysicalArmor":390,"adjMaxPhysicalArmor":390,"adjMinMagicArmor":390,"adjMaxMagicArmor":390})
    }),
    52004033: _tools.RODict({
        "propID": 52004033,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1800000,"adjMinPhysicalArmor":500,"adjMaxPhysicalArmor":500,"adjMinMagicArmor":500,"adjMaxMagicArmor":500})
    }),
    52004034: _tools.RODict({
        "propID": 52004034,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2700000,"adjMinPhysicalArmor":690,"adjMaxPhysicalArmor":690,"adjMinMagicArmor":690,"adjMaxMagicArmor":690})
    }),
    52004035: _tools.RODict({
        "propID": 52004035,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3250000,"adjMinPhysicalArmor":820,"adjMaxPhysicalArmor":820,"adjMinMagicArmor":820,"adjMaxMagicArmor":820})
    }),
    52009001: _tools.RODict({
        "propID": 52009001,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":400,"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":26,"adjMinMagicAtk":26,"adjMaxMagicAtk":26,"adjHit":1,"adjDodge":1})
    }),
    52009002: _tools.RODict({
        "propID": 52009002,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":10000,"adjMinPhysicalAtk":1,"adjMaxPhysicalAtk":1,"adjMinMagicAtk":1,"adjMaxMagicAtk":1,"adjMinPhysicalArmor":2,"adjMaxPhysicalArmor":2,"adjMinMagicArmor":2,"adjMaxMagicArmor":2,"adjHit":1,"adjDodge":1})
    }),
    52009003: _tools.RODict({
        "propID": 52009003,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":100,"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":26,"adjMinMagicAtk":26,"adjMaxMagicAtk":26,"adjHit":1,"adjDodge":1})
    }),
    52009004: _tools.RODict({
        "propID": 52009004,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":200,"adjMinPhysicalAtk":27,"adjMaxPhysicalAtk":27,"adjMinMagicAtk":27,"adjMaxMagicAtk":27,"adjHit":1,"adjDodge":1})
    }),
    52009005: _tools.RODict({
        "propID": 52009005,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":160,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":21,"adjMinMagicAtk":21,"adjMaxMagicAtk":21,"adjHit":1,"adjDodge":1})
    }),
    52009006: _tools.RODict({
        "propID": 52009006,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1200,"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":30,"adjMinMagicAtk":30,"adjMaxMagicAtk":30,"adjHit":2,"adjDodge":2})
    }),
    52009007: _tools.RODict({
        "propID": 52009007,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":276,"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":30,"adjMinMagicAtk":30,"adjMaxMagicAtk":30,"adjHit":3,"adjDodge":3})
    }),
    52009008: _tools.RODict({
        "propID": 52009008,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":144,"adjMinPhysicalAtk":3,"adjMaxPhysicalAtk":6,"adjMinMagicAtk":3,"adjMaxMagicAtk":6,"adjHit":4,"adjDodge":4})
    }),
    52009009: _tools.RODict({
        "propID": 52009009,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":168,"adjMinPhysicalAtk":4,"adjMaxPhysicalAtk":7,"adjMinMagicAtk":4,"adjMaxMagicAtk":7,"adjHit":4,"adjDodge":4})
    }),
    52009010: _tools.RODict({
        "propID": 52009010,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2000,"adjMinPhysicalAtk":35,"adjMaxPhysicalAtk":35,"adjMinMagicAtk":35,"adjMaxMagicAtk":35,"adjMinPhysicalArmor":1,"adjMaxPhysicalArmor":1,"adjMinMagicArmor":1,"adjMaxMagicArmor":1,"adjHit":5,"adjDodge":5})
    }),
    52009011: _tools.RODict({
        "propID": 52009011,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1200,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":22,"adjMinMagicAtk":21,"adjMaxMagicAtk":22,"adjMinPhysicalArmor":2,"adjMaxPhysicalArmor":2,"adjMinMagicArmor":2,"adjMaxMagicArmor":2,"adjHit":10,"adjDodge":6,"adjRealDmgDef":4})
    }),
    52012071: _tools.RODict({
        "propID": 52012071,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":592800,"adjMinPhysicalAtk":277,"adjMaxPhysicalAtk":292,"adjMinMagicAtk":277,"adjMaxMagicAtk":292,"adjMinPhysicalArmor":73,"adjMaxPhysicalArmor":73,"adjMinMagicArmor":73,"adjMaxMagicArmor":73,"adjHit":41,"adjDodge":7,"adjRealDmg":5,"adjRealDmgDef":1})
    }),
    52012072: _tools.RODict({
        "propID": 52012072,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":58798,"adjMinPhysicalAtk":134,"adjMaxPhysicalAtk":164,"adjMinMagicAtk":134,"adjMaxMagicAtk":164,"adjMinPhysicalArmor":27,"adjMaxPhysicalArmor":27,"adjMinMagicArmor":27,"adjMaxMagicArmor":27,"adjHit":90,"adjDodge":13,"adjRealDmg":5,"adjRealDmgDef":1})
    }),
    52012073: _tools.RODict({
        "propID": 52012073,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":103097,"adjMinPhysicalAtk":139,"adjMaxPhysicalAtk":170,"adjMinMagicAtk":139,"adjMaxMagicAtk":170,"adjMinPhysicalArmor":27,"adjMaxPhysicalArmor":27,"adjMinMagicArmor":27,"adjMaxMagicArmor":27,"adjHit":90,"adjDodge":13,"adjRealDmg":1,"adjRealDmgDef":1})
    }),
    52012074: _tools.RODict({
        "propID": 52012074,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":466983,"adjMinPhysicalAtk":120,"adjMaxPhysicalAtk":143,"adjMinMagicAtk":120,"adjMaxMagicAtk":143,"adjMinPhysicalArmor":18,"adjMaxPhysicalArmor":18,"adjMinMagicArmor":18,"adjMaxMagicArmor":18,"adjHit":23,"adjDodge":1,"adjRealDmg":3,"adjRealDmgDef":3})
    }),
    52012075: _tools.RODict({
        "propID": 52012075,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":285330,"adjMinPhysicalAtk":106,"adjMaxPhysicalAtk":130,"adjMinMagicAtk":106,"adjMaxMagicAtk":130,"adjMinPhysicalArmor":25,"adjMaxPhysicalArmor":25,"adjMinMagicArmor":25,"adjMaxMagicArmor":25,"adjHit":34,"adjDodge":1,"adjRealDmg":3,"adjRealDmgDef":3})
    }),
    52012076: _tools.RODict({
        "propID": 52012076,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1059962,"adjMinPhysicalAtk":602,"adjMaxPhysicalAtk":602,"adjMinMagicAtk":602,"adjMaxMagicAtk":602,"adjMinPhysicalArmor":161,"adjMaxPhysicalArmor":161,"adjMinMagicArmor":161,"adjMaxMagicArmor":161,"adjHit":29,"adjDodge":27,"adjRealDmg":1,"adjRealDmgDef":1})
    }),
    52012077: _tools.RODict({
        "propID": 52012077,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":829846,"adjMinPhysicalAtk":589,"adjMaxPhysicalAtk":589,"adjMinMagicAtk":589,"adjMaxMagicAtk":589,"adjMinPhysicalArmor":157,"adjMaxPhysicalArmor":157,"adjMinMagicArmor":157,"adjMaxMagicArmor":157,"adjHit":22,"adjDodge":18,"adjRealDmg":1,"adjRealDmgDef":1})
    }),
    52012078: _tools.RODict({
        "propID": 52012078,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":600218,"adjMinPhysicalAtk":573,"adjMaxPhysicalAtk":573,"adjMinMagicAtk":573,"adjMaxMagicAtk":573,"adjMinPhysicalArmor":153,"adjMaxPhysicalArmor":153,"adjMinMagicArmor":153,"adjMaxMagicArmor":153,"adjHit":22,"adjDodge":18,"adjRealDmg":1,"adjRealDmgDef":1})
    }),
    52012079: _tools.RODict({
        "propID": 52012079,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":529981,"adjMinPhysicalAtk":602,"adjMaxPhysicalAtk":602,"adjMinMagicAtk":602,"adjMaxMagicAtk":602,"adjMinPhysicalArmor":161,"adjMaxPhysicalArmor":161,"adjMinMagicArmor":161,"adjMaxMagicArmor":161,"adjHit":20,"adjDodge":16,"adjRealDmg":1,"adjRealDmgDef":1})
    }),
    52012080: _tools.RODict({
        "propID": 52012080,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":311192,"adjMinPhysicalAtk":589,"adjMaxPhysicalAtk":589,"adjMinMagicAtk":589,"adjMaxMagicAtk":589,"adjMinPhysicalArmor":157,"adjMaxPhysicalArmor":157,"adjMinMagicArmor":157,"adjMaxMagicArmor":157,"adjHit":20,"adjDodge":16,"adjRealDmg":1,"adjRealDmgDef":1})
    }),
    52012081: _tools.RODict({
        "propID": 52012081,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":200073,"adjMinPhysicalAtk":573,"adjMaxPhysicalAtk":573,"adjMinMagicAtk":573,"adjMaxMagicAtk":573,"adjMinPhysicalArmor":153,"adjMaxPhysicalArmor":153,"adjMinMagicArmor":153,"adjMaxMagicArmor":153,"adjHit":20,"adjDodge":16,"adjRealDmg":1,"adjRealDmgDef":1})
    }),
    52012082: _tools.RODict({
        "propID": 52012082,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":200073,"adjMinPhysicalAtk":573,"adjMaxPhysicalAtk":573,"adjMinMagicAtk":573,"adjMaxMagicAtk":573,"adjMinPhysicalArmor":153,"adjMaxPhysicalArmor":153,"adjMinMagicArmor":153,"adjMaxMagicArmor":153,"adjHit":20,"adjDodge":16,"adjRealDmg":1,"adjRealDmgDef":1})
    }),
    52012083: _tools.RODict({
        "propID": 52012083,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":30786,"adjMinPhysicalAtk":124,"adjMaxPhysicalAtk":152,"adjMinMagicAtk":124,"adjMaxMagicAtk":152,"adjMinPhysicalArmor":20,"adjMaxPhysicalArmor":20,"adjMinMagicArmor":20,"adjMaxMagicArmor":20,"adjHit":20,"adjDodge":16,"adjRealDmg":1,"adjRealDmgDef":1})
    }),
    52012084: _tools.RODict({
        "propID": 52012084,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":62435,"adjMinPhysicalAtk":191,"adjMaxPhysicalAtk":234,"adjMinMagicAtk":191,"adjMaxMagicAtk":234,"adjMinPhysicalArmor":20,"adjMaxPhysicalArmor":20,"adjMinMagicArmor":20,"adjMaxMagicArmor":20,"adjHit":20,"adjDodge":16,"adjRealDmg":1,"adjRealDmgDef":1})
    }),
    52012085: _tools.RODict({
        "propID": 52012085,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":57615,"adjMinPhysicalAtk":174,"adjMaxPhysicalAtk":213,"adjMinMagicAtk":174,"adjMaxMagicAtk":213,"adjMinPhysicalArmor":20,"adjMaxPhysicalArmor":20,"adjMinMagicArmor":20,"adjMaxMagicArmor":20,"adjHit":20,"adjDodge":16,"adjRealDmg":1,"adjRealDmgDef":1})
    }),
    52012086: _tools.RODict({
        "propID": 52012086,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":46458,"adjMinPhysicalAtk":158,"adjMaxPhysicalAtk":193,"adjMinMagicAtk":158,"adjMaxMagicAtk":193,"adjMinPhysicalArmor":20,"adjMaxPhysicalArmor":20,"adjMinMagicArmor":20,"adjMaxMagicArmor":20,"adjHit":20,"adjDodge":16,"adjRealDmg":1,"adjRealDmgDef":1})
    }),
    52012087: _tools.RODict({
        "propID": 52012087,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":39827,"adjMinPhysicalAtk":141,"adjMaxPhysicalAtk":172,"adjMinMagicAtk":141,"adjMaxMagicAtk":172,"adjMinPhysicalArmor":20,"adjMaxPhysicalArmor":20,"adjMinMagicArmor":20,"adjMaxMagicArmor":20,"adjHit":29,"adjDodge":25,"adjRealDmg":1,"adjRealDmgDef":1})
    }),
    52012088: _tools.RODict({
        "propID": 52012088,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":31598,"adjMinPhysicalAtk":100,"adjMaxPhysicalAtk":123,"adjMinMagicAtk":100,"adjMaxMagicAtk":123,"adjMinPhysicalArmor":19,"adjMaxPhysicalArmor":19,"adjMinMagicArmor":19,"adjMaxMagicArmor":19,"adjHit":90,"adjDodge":13,"adjRealDmg":1,"adjRealDmgDef":1})
    }),
    52012089: _tools.RODict({
        "propID": 52012089,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":52664,"adjMinPhysicalAtk":100,"adjMaxPhysicalAtk":123,"adjMinMagicAtk":100,"adjMaxMagicAtk":123,"adjMinPhysicalArmor":19,"adjMaxPhysicalArmor":19,"adjMinMagicArmor":19,"adjMaxMagicArmor":19,"adjHit":90,"adjDodge":13,"adjRealDmg":1,"adjRealDmgDef":1})
    }),
    52012090: _tools.RODict({
        "propID": 52012090,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":248298,"adjMinPhysicalAtk":194,"adjMaxPhysicalAtk":237,"adjMinMagicAtk":194,"adjMaxMagicAtk":237,"adjMinPhysicalArmor":38,"adjMaxPhysicalArmor":38,"adjMinMagicArmor":38,"adjMaxMagicArmor":38,"adjHit":90,"adjDodge":15,"adjRealDmg":1,"adjRealDmgDef":1})
    }),
    52012091: _tools.RODict({
        "propID": 52012091,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":148979,"adjMinPhysicalAtk":194,"adjMaxPhysicalAtk":237,"adjMinMagicAtk":194,"adjMaxMagicAtk":237,"adjMinPhysicalArmor":38,"adjMaxPhysicalArmor":38,"adjMinMagicArmor":38,"adjMaxMagicArmor":38,"adjHit":90,"adjDodge":15,"adjRealDmg":1,"adjRealDmgDef":1})
    }),
    52002092: _tools.RODict({
        "propID": 52002092,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":990000,"adjMinPhysicalAtk":170,"adjMaxPhysicalAtk":189,"adjMinMagicAtk":170,"adjMaxMagicAtk":189,"adjMinPhysicalArmor":15,"adjMaxPhysicalArmor":15,"adjMinMagicArmor":15,"adjMaxMagicArmor":15,"adjHit":109,"adjDodge":34,"adjRealDmg":3,"adjRealDmgDef":1})
    }),
    52002093: _tools.RODict({
        "propID": 52002093,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2800,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":41,"adjMinMagicAtk":23,"adjMaxMagicAtk":41,"adjMinPhysicalArmor":15,"adjMaxPhysicalArmor":15,"adjMinMagicArmor":15,"adjMaxMagicArmor":15})
    }),
    52012095: _tools.RODict({
        "propID": 52012095,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":799094,"adjMinPhysicalAtk":116,"adjMaxPhysicalAtk":129,"adjMinMagicAtk":116,"adjMaxMagicAtk":129,"adjMinPhysicalArmor":22,"adjMaxPhysicalArmor":22,"adjMinMagicArmor":22,"adjMaxMagicArmor":22,"adjHit":90,"adjDodge":15,"adjRealDmg":3,"adjRealDmgDef":1})
    }),
    52012096: _tools.RODict({
        "propID": 52012096,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":10984406,"adjMinPhysicalAtk":248,"adjMaxPhysicalAtk":275,"adjMinMagicAtk":248,"adjMaxMagicAtk":275,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":50,"adjMaxMagicArmor":50,"adjHit":110,"adjDodge":20,"adjRealDmg":6,"adjRealDmgDef":1})
    }),
    52012097: _tools.RODict({
        "propID": 52012097,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":11843,"adjMinPhysicalAtk":248,"adjMaxPhysicalAtk":275,"adjMinMagicAtk":248,"adjMaxMagicAtk":275,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":50,"adjMaxMagicArmor":50,"adjHit":110,"adjDodge":20,"adjRealDmg":6,"adjRealDmgDef":1})
    }),
    52012150: _tools.RODict({
        "propID": 52012150,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":40,"adjMaxMagicAtk":115})
    }),
    52012151: _tools.RODict({
        "propID": 52012151,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":44,"adjMaxMagicAtk":127})
    }),
    52012152: _tools.RODict({
        "propID": 52012152,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":48,"adjMaxMagicAtk":138})
    }),
    52012153: _tools.RODict({
        "propID": 52012153,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":52,"adjMaxMagicAtk":150})
    }),
    52012154: _tools.RODict({
        "propID": 52012154,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":57,"adjMaxMagicAtk":165,"adjHit":10,"adjFinalDmg":0.03})
    }),
    52012155: _tools.RODict({
        "propID": 52012155,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":63,"adjMaxMagicAtk":182,"adjHit":11,"adjFinalDmg":0.03})
    }),
    52012156: _tools.RODict({
        "propID": 52012156,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":68,"adjMaxMagicAtk":198,"adjHit":12,"adjFinalDmg":0.03})
    }),
    52012157: _tools.RODict({
        "propID": 52012157,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":74,"adjMaxMagicAtk":215,"adjHit":13,"adjFinalDmg":0.03})
    }),
    52012158: _tools.RODict({
        "propID": 52012158,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":81,"adjMaxMagicAtk":237,"adjHit":15,"adjFinalDmg":0.06})
    }),
    52012159: _tools.RODict({
        "propID": 52012159,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":89,"adjMaxMagicAtk":261,"adjHit":16,"adjFinalDmg":0.06})
    }),
    52012160: _tools.RODict({
        "propID": 52012160,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":97,"adjMaxMagicAtk":284,"adjHit":17,"adjFinalDmg":0.06})
    }),
    52012161: _tools.RODict({
        "propID": 52012161,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":105,"adjMaxMagicAtk":308,"adjHit":19,"adjFinalDmg":0.06})
    }),
    52012162: _tools.RODict({
        "propID": 52012162,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":116,"adjMaxMagicAtk":339,"adjHit":22,"adjFinalDmg":0.06,"adjFinalDmgAnti":0.06})
    }),
    52012163: _tools.RODict({
        "propID": 52012163,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":128,"adjMaxMagicAtk":373,"adjHit":24,"adjFinalDmg":0.06,"adjFinalDmgAnti":0.06})
    }),
    52012164: _tools.RODict({
        "propID": 52012164,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":141,"adjMaxMagicAtk":410,"adjHit":26,"adjFinalDmg":0.06,"adjFinalDmgAnti":0.06})
    }),
    52012165: _tools.RODict({
        "propID": 52012165,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":155,"adjMaxMagicAtk":451,"adjHit":28,"adjFinalDmg":0.06,"adjFinalDmgAnti":0.06})
    }),
    52012326: _tools.RODict({
        "propID": 52012326,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":40,"adjMaxMagicAtk":115})
    }),
    52012327: _tools.RODict({
        "propID": 52012327,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":44,"adjMaxMagicAtk":127})
    }),
    52012328: _tools.RODict({
        "propID": 52012328,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":48,"adjMaxMagicAtk":138})
    }),
    52012329: _tools.RODict({
        "propID": 52012329,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":52,"adjMaxMagicAtk":150})
    }),
    52012330: _tools.RODict({
        "propID": 52012330,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":57,"adjMaxMagicAtk":165,"adjHit":10,"adjFinalDmg":0.03})
    }),
    52012331: _tools.RODict({
        "propID": 52012331,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":63,"adjMaxMagicAtk":182,"adjHit":11,"adjFinalDmg":0.03})
    }),
    52012332: _tools.RODict({
        "propID": 52012332,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":68,"adjMaxMagicAtk":198,"adjHit":12,"adjFinalDmg":0.03})
    }),
    52012333: _tools.RODict({
        "propID": 52012333,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":74,"adjMaxMagicAtk":215,"adjHit":13,"adjFinalDmg":0.03})
    }),
    52012334: _tools.RODict({
        "propID": 52012334,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":81,"adjMaxMagicAtk":237,"adjHit":15,"adjFinalDmg":0.06})
    }),
    52012335: _tools.RODict({
        "propID": 52012335,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":89,"adjMaxMagicAtk":261,"adjHit":16,"adjFinalDmg":0.06})
    }),
    52012336: _tools.RODict({
        "propID": 52012336,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":97,"adjMaxMagicAtk":284,"adjHit":17,"adjFinalDmg":0.06})
    }),
    52012337: _tools.RODict({
        "propID": 52012337,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":105,"adjMaxMagicAtk":308,"adjHit":19,"adjFinalDmg":0.06})
    }),
    52012338: _tools.RODict({
        "propID": 52012338,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":116,"adjMaxMagicAtk":339,"adjHit":22,"adjFinalDmg":0.06,"adjFinalDmgAnti":0.06})
    }),
    52012339: _tools.RODict({
        "propID": 52012339,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":128,"adjMaxMagicAtk":373,"adjHit":24,"adjFinalDmg":0.06,"adjFinalDmgAnti":0.06})
    }),
    52012340: _tools.RODict({
        "propID": 52012340,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":141,"adjMaxMagicAtk":410,"adjHit":26,"adjFinalDmg":0.06,"adjFinalDmgAnti":0.06})
    }),
    52012341: _tools.RODict({
        "propID": 52012341,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":155,"adjMaxMagicAtk":451,"adjHit":28,"adjFinalDmg":0.06,"adjFinalDmgAnti":0.06})
    }),
    52012502: _tools.RODict({
        "propID": 52012502,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":40,"adjMaxPhysicalAtk":115})
    }),
    52012503: _tools.RODict({
        "propID": 52012503,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":44,"adjMaxPhysicalAtk":127})
    }),
    52012504: _tools.RODict({
        "propID": 52012504,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":48,"adjMaxPhysicalAtk":138})
    }),
    52012505: _tools.RODict({
        "propID": 52012505,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":52,"adjMaxPhysicalAtk":150})
    }),
    52012506: _tools.RODict({
        "propID": 52012506,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":57,"adjMaxPhysicalAtk":165,"adjHit":10,"adjFinalDmg":0.03})
    }),
    52012507: _tools.RODict({
        "propID": 52012507,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":63,"adjMaxPhysicalAtk":182,"adjHit":11,"adjFinalDmg":0.03})
    }),
    52012508: _tools.RODict({
        "propID": 52012508,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":68,"adjMaxPhysicalAtk":198,"adjHit":12,"adjFinalDmg":0.03})
    }),
    52012509: _tools.RODict({
        "propID": 52012509,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":74,"adjMaxPhysicalAtk":215,"adjHit":13,"adjFinalDmg":0.03})
    }),
    52012510: _tools.RODict({
        "propID": 52012510,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":81,"adjMaxPhysicalAtk":237,"adjHit":15,"adjFinalDmg":0.06})
    }),
    52012511: _tools.RODict({
        "propID": 52012511,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":89,"adjMaxPhysicalAtk":261,"adjHit":16,"adjFinalDmg":0.06})
    }),
    52012512: _tools.RODict({
        "propID": 52012512,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":97,"adjMaxPhysicalAtk":284,"adjHit":17,"adjFinalDmg":0.06})
    }),
    52012513: _tools.RODict({
        "propID": 52012513,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":105,"adjMaxPhysicalAtk":308,"adjHit":19,"adjFinalDmg":0.06})
    }),
    52012514: _tools.RODict({
        "propID": 52012514,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":116,"adjMaxPhysicalAtk":339,"adjHit":22,"adjFinalDmg":0.06,"adjFinalDmgAnti":0.06})
    }),
    52012515: _tools.RODict({
        "propID": 52012515,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":128,"adjMaxPhysicalAtk":373,"adjHit":24,"adjFinalDmg":0.06,"adjFinalDmgAnti":0.06})
    }),
    52012516: _tools.RODict({
        "propID": 52012516,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":141,"adjMaxPhysicalAtk":410,"adjHit":26,"adjFinalDmg":0.06,"adjFinalDmgAnti":0.06})
    }),
    52012517: _tools.RODict({
        "propID": 52012517,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":155,"adjMaxPhysicalAtk":451,"adjHit":28,"adjFinalDmg":0.06,"adjFinalDmgAnti":0.06})
    }),
    52012678: _tools.RODict({
        "propID": 52012678,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":55,"adjMaxPhysicalArmor":85,"adjMinMagicArmor":55,"adjMaxMagicArmor":85})
    }),
    52012679: _tools.RODict({
        "propID": 52012679,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":61,"adjMaxPhysicalArmor":94,"adjMinMagicArmor":61,"adjMaxMagicArmor":94})
    }),
    52012680: _tools.RODict({
        "propID": 52012680,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":66,"adjMaxPhysicalArmor":102,"adjMinMagicArmor":66,"adjMaxMagicArmor":102})
    }),
    52012681: _tools.RODict({
        "propID": 52012681,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":72,"adjMaxPhysicalArmor":111,"adjMinMagicArmor":72,"adjMaxMagicArmor":111})
    }),
    52012682: _tools.RODict({
        "propID": 52012682,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":79,"adjMaxPhysicalArmor":122,"adjMinMagicArmor":79,"adjMaxMagicArmor":122,"adjMortal":0.08})
    }),
    52012683: _tools.RODict({
        "propID": 52012683,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":87,"adjMaxPhysicalArmor":134,"adjMinMagicArmor":87,"adjMaxMagicArmor":134,"adjMortal":0.08})
    }),
    52012684: _tools.RODict({
        "propID": 52012684,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":95,"adjMaxPhysicalArmor":146,"adjMinMagicArmor":95,"adjMaxMagicArmor":146,"adjMortal":0.08})
    }),
    52012685: _tools.RODict({
        "propID": 52012685,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":103,"adjMaxPhysicalArmor":159,"adjMinMagicArmor":103,"adjMaxMagicArmor":159,"adjMortal":0.08})
    }),
    52012686: _tools.RODict({
        "propID": 52012686,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":113,"adjMaxPhysicalArmor":175,"adjMinMagicArmor":113,"adjMaxMagicArmor":175,"adjMortal":0.16})
    }),
    52012687: _tools.RODict({
        "propID": 52012687,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":124,"adjMaxPhysicalArmor":193,"adjMinMagicArmor":124,"adjMaxMagicArmor":193,"adjMortal":0.16})
    }),
    52012688: _tools.RODict({
        "propID": 52012688,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":136,"adjMaxPhysicalArmor":210,"adjMinMagicArmor":136,"adjMaxMagicArmor":210,"adjMortal":0.16})
    }),
    52012689: _tools.RODict({
        "propID": 52012689,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":147,"adjMaxPhysicalArmor":228,"adjMinMagicArmor":147,"adjMaxMagicArmor":228,"adjMortal":0.16})
    }),
    52012690: _tools.RODict({
        "propID": 52012690,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":162,"adjMaxPhysicalArmor":251,"adjMinMagicArmor":162,"adjMaxMagicArmor":251,"adjMortal":0.16,"adjAntiMortal":0.16})
    }),
    52012691: _tools.RODict({
        "propID": 52012691,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":178,"adjMaxPhysicalArmor":276,"adjMinMagicArmor":178,"adjMaxMagicArmor":276,"adjMortal":0.16,"adjAntiMortal":0.16})
    }),
    52012692: _tools.RODict({
        "propID": 52012692,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":196,"adjMaxPhysicalArmor":304,"adjMinMagicArmor":196,"adjMaxMagicArmor":304,"adjMortal":0.16,"adjAntiMortal":0.16})
    }),
    52012693: _tools.RODict({
        "propID": 52012693,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":216,"adjMaxPhysicalArmor":334,"adjMinMagicArmor":216,"adjMaxMagicArmor":334,"adjMortal":0.16,"adjAntiMortal":0.16})
    }),
    52012854: _tools.RODict({
        "propID": 52012854,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":20,"adjMaxMagicArmor":30})
    }),
    52012855: _tools.RODict({
        "propID": 52012855,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":22,"adjMaxMagicArmor":33})
    }),
    52012856: _tools.RODict({
        "propID": 52012856,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":24,"adjMaxMagicArmor":36})
    }),
    52012857: _tools.RODict({
        "propID": 52012857,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":26,"adjMaxMagicArmor":39})
    }),
    52012858: _tools.RODict({
        "propID": 52012858,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":29,"adjMaxMagicArmor":43,"adjAntiFatal":10,"adjMortal":0.08})
    }),
    52012859: _tools.RODict({
        "propID": 52012859,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":32,"adjMaxMagicArmor":47,"adjAntiFatal":11,"adjMortal":0.08})
    }),
    52012860: _tools.RODict({
        "propID": 52012860,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":35,"adjMaxMagicArmor":52,"adjAntiFatal":12,"adjMortal":0.08})
    }),
    52012861: _tools.RODict({
        "propID": 52012861,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":38,"adjMaxMagicArmor":56,"adjAntiFatal":13,"adjMortal":0.08})
    }),
    52012862: _tools.RODict({
        "propID": 52012862,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":42,"adjMaxMagicArmor":62,"adjAntiFatal":15,"adjMortal":0.16})
    }),
    52012863: _tools.RODict({
        "propID": 52012863,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":46,"adjMaxMagicArmor":68,"adjAntiFatal":16,"adjMortal":0.16})
    }),
    52012864: _tools.RODict({
        "propID": 52012864,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":50,"adjMaxMagicArmor":74,"adjAntiFatal":17,"adjMortal":0.16})
    }),
    52012865: _tools.RODict({
        "propID": 52012865,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":55,"adjMaxMagicArmor":81,"adjAntiFatal":19,"adjMortal":0.16})
    }),
    52012866: _tools.RODict({
        "propID": 52012866,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":61,"adjMaxMagicArmor":89,"adjAntiFatal":22,"adjMortal":0.16,"adjAntiMortal":0.16})
    }),
    52012867: _tools.RODict({
        "propID": 52012867,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":67,"adjMaxMagicArmor":98,"adjAntiFatal":24,"adjMortal":0.16,"adjAntiMortal":0.16})
    }),
    52012868: _tools.RODict({
        "propID": 52012868,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":74,"adjMaxMagicArmor":108,"adjAntiFatal":26,"adjMortal":0.16,"adjAntiMortal":0.16})
    }),
    52012869: _tools.RODict({
        "propID": 52012869,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":81,"adjMaxMagicArmor":119,"adjAntiFatal":28,"adjMortal":0.16,"adjAntiMortal":0.16})
    }),
    52013030: _tools.RODict({
        "propID": 52013030,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":20,"adjMaxPhysicalArmor":30})
    }),
    52013031: _tools.RODict({
        "propID": 52013031,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":22,"adjMaxPhysicalArmor":33})
    }),
    52013032: _tools.RODict({
        "propID": 52013032,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":24,"adjMaxPhysicalArmor":36})
    }),
    52013033: _tools.RODict({
        "propID": 52013033,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":26,"adjMaxPhysicalArmor":39})
    }),
    52013034: _tools.RODict({
        "propID": 52013034,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":29,"adjMaxPhysicalArmor":43,"adjDodge":10,"adjPVPDmg":0.04})
    }),
    52013035: _tools.RODict({
        "propID": 52013035,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":32,"adjMaxPhysicalArmor":47,"adjDodge":11,"adjPVPDmg":0.04})
    }),
    52013036: _tools.RODict({
        "propID": 52013036,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":35,"adjMaxPhysicalArmor":52,"adjDodge":12,"adjPVPDmg":0.04})
    }),
    52013037: _tools.RODict({
        "propID": 52013037,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":38,"adjMaxPhysicalArmor":56,"adjDodge":13,"adjPVPDmg":0.04})
    }),
    52013038: _tools.RODict({
        "propID": 52013038,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":42,"adjMaxPhysicalArmor":62,"adjDodge":15,"adjPVPDmg":0.08})
    }),
    52013039: _tools.RODict({
        "propID": 52013039,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":46,"adjMaxPhysicalArmor":68,"adjDodge":16,"adjPVPDmg":0.08})
    }),
    52013040: _tools.RODict({
        "propID": 52013040,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":74,"adjDodge":17,"adjPVPDmg":0.08})
    }),
    52013041: _tools.RODict({
        "propID": 52013041,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":55,"adjMaxPhysicalArmor":81,"adjDodge":19,"adjPVPDmg":0.08})
    }),
    52013042: _tools.RODict({
        "propID": 52013042,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":61,"adjMaxPhysicalArmor":89,"adjDodge":22,"adjPVPDmg":0.08,"adjPVPDmgAnti":0.08})
    }),
    52013043: _tools.RODict({
        "propID": 52013043,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":67,"adjMaxPhysicalArmor":98,"adjDodge":24,"adjPVPDmg":0.08,"adjPVPDmgAnti":0.08})
    }),
    52013044: _tools.RODict({
        "propID": 52013044,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":74,"adjMaxPhysicalArmor":108,"adjDodge":26,"adjPVPDmg":0.08,"adjPVPDmgAnti":0.08})
    }),
    52013045: _tools.RODict({
        "propID": 52013045,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":81,"adjMaxPhysicalArmor":119,"adjDodge":28,"adjPVPDmg":0.08,"adjPVPDmgAnti":0.08})
    }),
    52013206: _tools.RODict({
        "propID": 52013206,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":14,"adjMaxPhysicalAtk":43})
    }),
    52013207: _tools.RODict({
        "propID": 52013207,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":15,"adjMaxPhysicalAtk":47})
    }),
    52013208: _tools.RODict({
        "propID": 52013208,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":52})
    }),
    52013209: _tools.RODict({
        "propID": 52013209,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":18,"adjMaxPhysicalAtk":56})
    }),
    52013210: _tools.RODict({
        "propID": 52013210,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":62,"adjFatal":10,"adjIgnoreArmor":0.02})
    }),
    52013211: _tools.RODict({
        "propID": 52013211,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":68,"adjFatal":11,"adjIgnoreArmor":0.02})
    }),
    52013212: _tools.RODict({
        "propID": 52013212,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":74,"adjFatal":12,"adjIgnoreArmor":0.02})
    }),
    52013213: _tools.RODict({
        "propID": 52013213,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":81,"adjFatal":13,"adjIgnoreArmor":0.02})
    }),
    52013214: _tools.RODict({
        "propID": 52013214,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":29,"adjMaxPhysicalAtk":89,"adjFatal":15,"adjIgnoreArmor":0.04})
    }),
    52013215: _tools.RODict({
        "propID": 52013215,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":98,"adjFatal":16,"adjIgnoreArmor":0.04})
    }),
    52013216: _tools.RODict({
        "propID": 52013216,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":35,"adjMaxPhysicalAtk":107,"adjFatal":17,"adjIgnoreArmor":0.04})
    }),
    52013217: _tools.RODict({
        "propID": 52013217,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":38,"adjMaxPhysicalAtk":116,"adjFatal":19,"adjIgnoreArmor":0.04})
    }),
    52013218: _tools.RODict({
        "propID": 52013218,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":42,"adjMaxPhysicalAtk":128,"adjFatal":22,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013219: _tools.RODict({
        "propID": 52013219,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":46,"adjMaxPhysicalAtk":141,"adjFatal":24,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013220: _tools.RODict({
        "propID": 52013220,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":51,"adjMaxPhysicalAtk":155,"adjFatal":26,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013221: _tools.RODict({
        "propID": 52013221,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":56,"adjMaxPhysicalAtk":171,"adjFatal":28,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013382: _tools.RODict({
        "propID": 52013382,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":14,"adjMaxMagicAtk":43})
    }),
    52013383: _tools.RODict({
        "propID": 52013383,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":15,"adjMaxMagicAtk":47})
    }),
    52013384: _tools.RODict({
        "propID": 52013384,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":17,"adjMaxMagicAtk":52})
    }),
    52013385: _tools.RODict({
        "propID": 52013385,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":18,"adjMaxMagicAtk":56})
    }),
    52013386: _tools.RODict({
        "propID": 52013386,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":20,"adjMaxMagicAtk":62,"adjFatal":10,"adjIgnoreArmor":0.02})
    }),
    52013387: _tools.RODict({
        "propID": 52013387,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":22,"adjMaxMagicAtk":68,"adjFatal":11,"adjIgnoreArmor":0.02})
    }),
    52013388: _tools.RODict({
        "propID": 52013388,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":24,"adjMaxMagicAtk":74,"adjFatal":12,"adjIgnoreArmor":0.02})
    }),
    52013389: _tools.RODict({
        "propID": 52013389,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":26,"adjMaxMagicAtk":81,"adjFatal":13,"adjIgnoreArmor":0.02})
    }),
    52013390: _tools.RODict({
        "propID": 52013390,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":29,"adjMaxMagicAtk":89,"adjFatal":15,"adjIgnoreArmor":0.04})
    }),
    52013391: _tools.RODict({
        "propID": 52013391,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":32,"adjMaxMagicAtk":98,"adjFatal":16,"adjIgnoreArmor":0.04})
    }),
    52013392: _tools.RODict({
        "propID": 52013392,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":35,"adjMaxMagicAtk":107,"adjFatal":17,"adjIgnoreArmor":0.04})
    }),
    52013393: _tools.RODict({
        "propID": 52013393,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":38,"adjMaxMagicAtk":116,"adjFatal":19,"adjIgnoreArmor":0.04})
    }),
    52013394: _tools.RODict({
        "propID": 52013394,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":42,"adjMaxMagicAtk":128,"adjFatal":22,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013395: _tools.RODict({
        "propID": 52013395,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":46,"adjMaxMagicAtk":141,"adjFatal":24,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013396: _tools.RODict({
        "propID": 52013396,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":51,"adjMaxMagicAtk":155,"adjFatal":26,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013397: _tools.RODict({
        "propID": 52013397,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":56,"adjMaxMagicAtk":171,"adjFatal":28,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013558: _tools.RODict({
        "propID": 52013558,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":160,"adjMinPhysicalAtk":13,"adjMaxPhysicalAtk":40})
    }),
    52013559: _tools.RODict({
        "propID": 52013559,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":176,"adjMinPhysicalAtk":14,"adjMaxPhysicalAtk":44})
    }),
    52013560: _tools.RODict({
        "propID": 52013560,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":192,"adjMinPhysicalAtk":16,"adjMaxPhysicalAtk":48})
    }),
    52013561: _tools.RODict({
        "propID": 52013561,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":208,"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":52})
    }),
    52013562: _tools.RODict({
        "propID": 52013562,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":229,"adjMinPhysicalAtk":19,"adjMaxPhysicalAtk":57,"adjIgnoreArmor":0.02})
    }),
    52013563: _tools.RODict({
        "propID": 52013563,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":252,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":63,"adjIgnoreArmor":0.02})
    }),
    52013564: _tools.RODict({
        "propID": 52013564,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":275,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":68,"adjIgnoreArmor":0.02})
    }),
    52013565: _tools.RODict({
        "propID": 52013565,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":298,"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":74,"adjIgnoreArmor":0.02})
    }),
    52013566: _tools.RODict({
        "propID": 52013566,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":328,"adjMinPhysicalAtk":28,"adjMaxPhysicalAtk":81,"adjIgnoreArmor":0.04})
    }),
    52013567: _tools.RODict({
        "propID": 52013567,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":361,"adjMinPhysicalAtk":31,"adjMaxPhysicalAtk":89,"adjIgnoreArmor":0.04})
    }),
    52013568: _tools.RODict({
        "propID": 52013568,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":394,"adjMinPhysicalAtk":34,"adjMaxPhysicalAtk":97,"adjIgnoreArmor":0.04})
    }),
    52013569: _tools.RODict({
        "propID": 52013569,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":426,"adjMinPhysicalAtk":36,"adjMaxPhysicalAtk":105,"adjIgnoreArmor":0.04})
    }),
    52013570: _tools.RODict({
        "propID": 52013570,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":469,"adjMinPhysicalAtk":40,"adjMaxPhysicalAtk":116,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013571: _tools.RODict({
        "propID": 52013571,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":516,"adjMinPhysicalAtk":44,"adjMaxPhysicalAtk":128,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013572: _tools.RODict({
        "propID": 52013572,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":568,"adjMinPhysicalAtk":48,"adjMaxPhysicalAtk":141,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013573: _tools.RODict({
        "propID": 52013573,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":625,"adjMinPhysicalAtk":53,"adjMaxPhysicalAtk":155,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013734: _tools.RODict({
        "propID": 52013734,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":160,"adjMinMagicAtk":13,"adjMaxMagicAtk":40})
    }),
    52013735: _tools.RODict({
        "propID": 52013735,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":176,"adjMinMagicAtk":14,"adjMaxMagicAtk":44})
    }),
    52013736: _tools.RODict({
        "propID": 52013736,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":192,"adjMinMagicAtk":16,"adjMaxMagicAtk":48})
    }),
    52013737: _tools.RODict({
        "propID": 52013737,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":208,"adjMinMagicAtk":17,"adjMaxMagicAtk":52})
    }),
    52013738: _tools.RODict({
        "propID": 52013738,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":229,"adjMinMagicAtk":19,"adjMaxMagicAtk":57,"adjIgnoreArmor":0.02})
    }),
    52013739: _tools.RODict({
        "propID": 52013739,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":252,"adjMinMagicAtk":21,"adjMaxMagicAtk":63,"adjIgnoreArmor":0.02})
    }),
    52013740: _tools.RODict({
        "propID": 52013740,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":275,"adjMinMagicAtk":23,"adjMaxMagicAtk":68,"adjIgnoreArmor":0.02})
    }),
    52013741: _tools.RODict({
        "propID": 52013741,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":298,"adjMinMagicAtk":25,"adjMaxMagicAtk":74,"adjIgnoreArmor":0.02})
    }),
    52013742: _tools.RODict({
        "propID": 52013742,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":328,"adjMinMagicAtk":28,"adjMaxMagicAtk":81,"adjIgnoreArmor":0.04})
    }),
    52013743: _tools.RODict({
        "propID": 52013743,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":361,"adjMinMagicAtk":31,"adjMaxMagicAtk":89,"adjIgnoreArmor":0.04})
    }),
    52013744: _tools.RODict({
        "propID": 52013744,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":394,"adjMinMagicAtk":34,"adjMaxMagicAtk":97,"adjIgnoreArmor":0.04})
    }),
    52013745: _tools.RODict({
        "propID": 52013745,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":426,"adjMinMagicAtk":36,"adjMaxMagicAtk":105,"adjIgnoreArmor":0.04})
    }),
    52013746: _tools.RODict({
        "propID": 52013746,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":469,"adjMinMagicAtk":40,"adjMaxMagicAtk":116,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013747: _tools.RODict({
        "propID": 52013747,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":516,"adjMinMagicAtk":44,"adjMaxMagicAtk":128,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013748: _tools.RODict({
        "propID": 52013748,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":568,"adjMinMagicAtk":48,"adjMaxMagicAtk":141,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013749: _tools.RODict({
        "propID": 52013749,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":625,"adjMinMagicAtk":53,"adjMaxMagicAtk":155,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013910: _tools.RODict({
        "propID": 52013910,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1200,"adjMinPhysicalAtk":14,"adjMaxPhysicalAtk":38})
    }),
    52013911: _tools.RODict({
        "propID": 52013911,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1320,"adjMinPhysicalAtk":15,"adjMaxPhysicalAtk":42})
    }),
    52013912: _tools.RODict({
        "propID": 52013912,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1440,"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":46})
    }),
    52013913: _tools.RODict({
        "propID": 52013913,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1560,"adjMinPhysicalAtk":18,"adjMaxPhysicalAtk":49})
    }),
    52013914: _tools.RODict({
        "propID": 52013914,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1716,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":54,"adjMonsterDmg":0.04})
    }),
    52013915: _tools.RODict({
        "propID": 52013915,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1888,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":59,"adjMonsterDmg":0.04})
    }),
    52013916: _tools.RODict({
        "propID": 52013916,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2059,"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":65,"adjMonsterDmg":0.04})
    }),
    52013917: _tools.RODict({
        "propID": 52013917,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2231,"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":70,"adjMonsterDmg":0.04})
    }),
    52013918: _tools.RODict({
        "propID": 52013918,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2454,"adjMinPhysicalAtk":29,"adjMaxPhysicalAtk":77,"adjMonsterDmg":0.08})
    }),
    52013919: _tools.RODict({
        "propID": 52013919,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2699,"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":85,"adjMonsterDmg":0.08})
    }),
    52013920: _tools.RODict({
        "propID": 52013920,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2945,"adjMinPhysicalAtk":35,"adjMaxPhysicalAtk":92,"adjMonsterDmg":0.08})
    }),
    52013921: _tools.RODict({
        "propID": 52013921,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3190,"adjMinPhysicalAtk":38,"adjMaxPhysicalAtk":100,"adjMonsterDmg":0.08})
    }),
    52013922: _tools.RODict({
        "propID": 52013922,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3509,"adjMinPhysicalAtk":42,"adjMaxPhysicalAtk":110,"adjMonsterDmg":0.08,"adjMonsterDmgAnti":0.08})
    }),
    52013923: _tools.RODict({
        "propID": 52013923,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3860,"adjMinPhysicalAtk":46,"adjMaxPhysicalAtk":121,"adjMonsterDmg":0.08,"adjMonsterDmgAnti":0.08})
    }),
    52013924: _tools.RODict({
        "propID": 52013924,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4246,"adjMinPhysicalAtk":51,"adjMaxPhysicalAtk":133,"adjMonsterDmg":0.08,"adjMonsterDmgAnti":0.08})
    }),
    52013925: _tools.RODict({
        "propID": 52013925,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4671,"adjMinPhysicalAtk":56,"adjMaxPhysicalAtk":146,"adjMonsterDmg":0.08,"adjMonsterDmgAnti":0.08})
    }),
    52014086: _tools.RODict({
        "propID": 52014086,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1200,"adjMinMagicAtk":14,"adjMaxMagicAtk":38})
    }),
    52014087: _tools.RODict({
        "propID": 52014087,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1320,"adjMinMagicAtk":15,"adjMaxMagicAtk":42})
    }),
    52014088: _tools.RODict({
        "propID": 52014088,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1440,"adjMinMagicAtk":17,"adjMaxMagicAtk":46})
    }),
    52014089: _tools.RODict({
        "propID": 52014089,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1560,"adjMinMagicAtk":18,"adjMaxMagicAtk":49})
    }),
    52014090: _tools.RODict({
        "propID": 52014090,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1716,"adjMinMagicAtk":20,"adjMaxMagicAtk":54,"adjMonsterDmg":0.04})
    }),
    52014091: _tools.RODict({
        "propID": 52014091,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1888,"adjMinMagicAtk":22,"adjMaxMagicAtk":59,"adjMonsterDmg":0.04})
    }),
    52014092: _tools.RODict({
        "propID": 52014092,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2059,"adjMinMagicAtk":24,"adjMaxMagicAtk":65,"adjMonsterDmg":0.04})
    }),
    52014093: _tools.RODict({
        "propID": 52014093,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2231,"adjMinMagicAtk":26,"adjMaxMagicAtk":70,"adjMonsterDmg":0.04})
    }),
    52014094: _tools.RODict({
        "propID": 52014094,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2454,"adjMinMagicAtk":29,"adjMaxMagicAtk":77,"adjMonsterDmg":0.08})
    }),
    52014095: _tools.RODict({
        "propID": 52014095,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2699,"adjMinMagicAtk":32,"adjMaxMagicAtk":85,"adjMonsterDmg":0.08})
    }),
    52014096: _tools.RODict({
        "propID": 52014096,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2945,"adjMinMagicAtk":35,"adjMaxMagicAtk":92,"adjMonsterDmg":0.08})
    }),
    52014097: _tools.RODict({
        "propID": 52014097,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3190,"adjMinMagicAtk":38,"adjMaxMagicAtk":100,"adjMonsterDmg":0.08})
    }),
    52014098: _tools.RODict({
        "propID": 52014098,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3509,"adjMinMagicAtk":42,"adjMaxMagicAtk":110,"adjMonsterDmg":0.08,"adjMonsterDmgAnti":0.08})
    }),
    52014099: _tools.RODict({
        "propID": 52014099,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3860,"adjMinMagicAtk":46,"adjMaxMagicAtk":121,"adjMonsterDmg":0.08,"adjMonsterDmgAnti":0.08})
    }),
    52014100: _tools.RODict({
        "propID": 52014100,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4246,"adjMinMagicAtk":51,"adjMaxMagicAtk":133,"adjMonsterDmg":0.08,"adjMonsterDmgAnti":0.08})
    }),
    52014101: _tools.RODict({
        "propID": 52014101,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4671,"adjMinMagicAtk":56,"adjMaxMagicAtk":146,"adjMonsterDmg":0.08,"adjMonsterDmgAnti":0.08})
    }),
    52014262: _tools.RODict({
        "propID": 52014262,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2000,"adjDrugsQuantity":4})
    }),
    52014263: _tools.RODict({
        "propID": 52014263,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2200,"adjDrugsQuantity":5})
    }),
    52014264: _tools.RODict({
        "propID": 52014264,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2400,"adjDrugsQuantity":6})
    }),
    52014265: _tools.RODict({
        "propID": 52014265,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2600,"adjDrugsQuantity":7})
    }),
    52014266: _tools.RODict({
        "propID": 52014266,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2860,"adjDrugsQuantity":9,"adjFinalDmg":0.02})
    }),
    52014267: _tools.RODict({
        "propID": 52014267,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3146,"adjDrugsQuantity":10,"adjFinalDmg":0.02})
    }),
    52014268: _tools.RODict({
        "propID": 52014268,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3432,"adjDrugsQuantity":11,"adjFinalDmg":0.02})
    }),
    52014269: _tools.RODict({
        "propID": 52014269,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3718,"adjDrugsQuantity":13,"adjFinalDmg":0.02})
    }),
    52014270: _tools.RODict({
        "propID": 52014270,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4090,"adjDrugsQuantity":16,"adjFinalDmg":0.04})
    }),
    52014271: _tools.RODict({
        "propID": 52014271,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4499,"adjDrugsQuantity":18,"adjFinalDmg":0.04})
    }),
    52014272: _tools.RODict({
        "propID": 52014272,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4908,"adjDrugsQuantity":20,"adjFinalDmg":0.04})
    }),
    52014273: _tools.RODict({
        "propID": 52014273,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5317,"adjDrugsQuantity":22,"adjFinalDmg":0.04})
    }),
    52014274: _tools.RODict({
        "propID": 52014274,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5849,"adjDrugsQuantity":26,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014275: _tools.RODict({
        "propID": 52014275,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":6434,"adjDrugsQuantity":28,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014276: _tools.RODict({
        "propID": 52014276,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":7077,"adjDrugsQuantity":30,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014277: _tools.RODict({
        "propID": 52014277,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":7785,"adjDrugsQuantity":32,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    })
})
minKey = 51000001
maxKey = 52014277