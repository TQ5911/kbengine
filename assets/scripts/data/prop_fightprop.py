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
        "propList": _tools.RODict({"adjFullHp":50,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":22,"adjMinMagicAtk":22,"adjMaxMagicAtk":22,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjAccuracy":3,"adjFatal":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000002: _tools.RODict({
        "propID": 51000002,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":53,"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":24,"adjMinMagicAtk":24,"adjMaxMagicAtk":24,"adjMinPhysicalArmor":17,"adjMaxPhysicalArmor":17,"adjMinMagicArmor":17,"adjMaxMagicArmor":17,"adjAccuracy":3,"adjFatal":2,"adjRealDmg":2,"adjRealDmgDef":2,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000003: _tools.RODict({
        "propID": 51000003,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":56,"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":26,"adjMinMagicAtk":26,"adjMaxMagicAtk":26,"adjMinPhysicalArmor":18,"adjMaxPhysicalArmor":18,"adjMinMagicArmor":18,"adjMaxMagicArmor":18,"adjAccuracy":3,"adjFatal":2,"adjRealDmg":3,"adjRealDmgDef":3,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000004: _tools.RODict({
        "propID": 51000004,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":59,"adjMinPhysicalAtk":28,"adjMaxPhysicalAtk":28,"adjMinMagicAtk":28,"adjMaxMagicAtk":28,"adjMinPhysicalArmor":18,"adjMaxPhysicalArmor":18,"adjMinMagicArmor":18,"adjMaxMagicArmor":18,"adjAccuracy":3,"adjFatal":2,"adjRealDmg":4,"adjRealDmgDef":4,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000005: _tools.RODict({
        "propID": 51000005,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":62,"adjMinPhysicalAtk":36,"adjMaxPhysicalAtk":36,"adjMinMagicAtk":36,"adjMaxMagicAtk":36,"adjMinPhysicalArmor":19,"adjMaxPhysicalArmor":19,"adjMinMagicArmor":19,"adjMaxMagicArmor":19,"adjAccuracy":3,"adjFatal":2,"adjRealDmg":5,"adjRealDmgDef":5,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000006: _tools.RODict({
        "propID": 51000006,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":65,"adjMinPhysicalAtk":65,"adjMaxPhysicalAtk":65,"adjMinMagicAtk":65,"adjMaxMagicAtk":65,"adjMinPhysicalArmor":20,"adjMaxPhysicalArmor":20,"adjMinMagicArmor":20,"adjMaxMagicArmor":20,"adjAccuracy":3,"adjFatal":2,"adjRealDmg":6,"adjRealDmgDef":6,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000007: _tools.RODict({
        "propID": 51000007,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":68,"adjMinPhysicalAtk":102,"adjMaxPhysicalAtk":102,"adjMinMagicAtk":102,"adjMaxMagicAtk":102,"adjMinPhysicalArmor":30,"adjMaxPhysicalArmor":30,"adjMinMagicArmor":30,"adjMaxMagicArmor":30,"adjAccuracy":3,"adjFatal":2,"adjRealDmg":7,"adjRealDmgDef":7,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000008: _tools.RODict({
        "propID": 51000008,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":70,"adjMinPhysicalAtk":124,"adjMaxPhysicalAtk":124,"adjMinMagicAtk":124,"adjMaxMagicAtk":124,"adjMinPhysicalArmor":40,"adjMaxPhysicalArmor":40,"adjMinMagicArmor":40,"adjMaxMagicArmor":40,"adjAccuracy":3,"adjFatal":2,"adjRealDmg":8,"adjRealDmgDef":8,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000009: _tools.RODict({
        "propID": 51000009,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":75,"adjMinPhysicalAtk":135,"adjMaxPhysicalAtk":135,"adjMinMagicAtk":135,"adjMaxMagicAtk":135,"adjMinPhysicalArmor":125,"adjMaxPhysicalArmor":125,"adjMinMagicArmor":125,"adjMaxMagicArmor":125,"adjAccuracy":3,"adjFatal":2,"adjRealDmg":9,"adjRealDmgDef":9,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000010: _tools.RODict({
        "propID": 51000010,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":80,"adjMinPhysicalAtk":145,"adjMaxPhysicalAtk":145,"adjMinMagicAtk":145,"adjMaxMagicAtk":145,"adjMinPhysicalArmor":134,"adjMaxPhysicalArmor":134,"adjMinMagicArmor":134,"adjMaxMagicArmor":134,"adjAccuracy":3,"adjFatal":2,"adjRealDmg":10,"adjRealDmgDef":10,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000011: _tools.RODict({
        "propID": 51000011,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":85,"adjMinPhysicalAtk":168,"adjMaxPhysicalAtk":168,"adjMinMagicAtk":168,"adjMaxMagicAtk":168,"adjMinPhysicalArmor":139,"adjMaxPhysicalArmor":139,"adjMinMagicArmor":139,"adjMaxMagicArmor":139,"adjAccuracy":3,"adjEvasion":1,"adjFatal":2,"adjRealDmg":11,"adjRealDmgDef":11,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000012: _tools.RODict({
        "propID": 51000012,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":105,"adjMinPhysicalAtk":190,"adjMaxPhysicalAtk":190,"adjMinMagicAtk":190,"adjMaxMagicAtk":190,"adjMinPhysicalArmor":140,"adjMaxPhysicalArmor":140,"adjMinMagicArmor":140,"adjMaxMagicArmor":140,"adjAccuracy":3,"adjEvasion":1,"adjFatal":2,"adjRealDmg":12,"adjRealDmgDef":12,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000013: _tools.RODict({
        "propID": 51000013,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":120,"adjMinPhysicalAtk":202,"adjMaxPhysicalAtk":202,"adjMinMagicAtk":202,"adjMaxMagicAtk":202,"adjMinPhysicalArmor":141,"adjMaxPhysicalArmor":141,"adjMinMagicArmor":141,"adjMaxMagicArmor":141,"adjAccuracy":3,"adjEvasion":1,"adjFatal":2,"adjRealDmg":13,"adjRealDmgDef":13,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000014: _tools.RODict({
        "propID": 51000014,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":135,"adjMinPhysicalAtk":210,"adjMaxPhysicalAtk":210,"adjMinMagicAtk":210,"adjMaxMagicAtk":210,"adjMinPhysicalArmor":143,"adjMaxPhysicalArmor":143,"adjMinMagicArmor":143,"adjMaxMagicArmor":143,"adjAccuracy":3,"adjEvasion":1,"adjFatal":2,"adjRealDmg":14,"adjRealDmgDef":14,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000015: _tools.RODict({
        "propID": 51000015,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":155,"adjMinPhysicalAtk":222,"adjMaxPhysicalAtk":222,"adjMinMagicAtk":222,"adjMaxMagicAtk":222,"adjMinPhysicalArmor":144,"adjMaxPhysicalArmor":144,"adjMinMagicArmor":144,"adjMaxMagicArmor":144,"adjAccuracy":3,"adjEvasion":1,"adjFatal":2,"adjRealDmg":15,"adjRealDmgDef":15,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000016: _tools.RODict({
        "propID": 51000016,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":175,"adjMinPhysicalAtk":236,"adjMaxPhysicalAtk":236,"adjMinMagicAtk":236,"adjMaxMagicAtk":236,"adjMinPhysicalArmor":145,"adjMaxPhysicalArmor":145,"adjMinMagicArmor":145,"adjMaxMagicArmor":145,"adjAccuracy":3,"adjEvasion":2,"adjFatal":2,"adjRealDmg":16,"adjRealDmgDef":16,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000017: _tools.RODict({
        "propID": 51000017,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":195,"adjMinPhysicalAtk":244,"adjMaxPhysicalAtk":244,"adjMinMagicAtk":244,"adjMaxMagicAtk":244,"adjMinPhysicalArmor":146,"adjMaxPhysicalArmor":146,"adjMinMagicArmor":146,"adjMaxMagicArmor":146,"adjAccuracy":3,"adjEvasion":2,"adjFatal":2,"adjRealDmg":17,"adjRealDmgDef":17,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000018: _tools.RODict({
        "propID": 51000018,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":215,"adjMinPhysicalAtk":256,"adjMaxPhysicalAtk":256,"adjMinMagicAtk":256,"adjMaxMagicAtk":256,"adjMinPhysicalArmor":154,"adjMaxPhysicalArmor":154,"adjMinMagicArmor":154,"adjMaxMagicArmor":154,"adjAccuracy":3,"adjEvasion":2,"adjFatal":2,"adjRealDmg":18,"adjRealDmgDef":18,"adjMonsterDmg":0.0045,"adjMonsterDmgAnti":0.0037,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000019: _tools.RODict({
        "propID": 51000019,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":235,"adjMinPhysicalAtk":295,"adjMaxPhysicalAtk":295,"adjMinMagicAtk":295,"adjMaxMagicAtk":295,"adjMinPhysicalArmor":164,"adjMaxPhysicalArmor":164,"adjMinMagicArmor":164,"adjMaxMagicArmor":164,"adjAccuracy":3,"adjEvasion":2,"adjFatal":2,"adjIgnoreArmor":0.0045,"adjDmgArmor":0.0045,"adjMortal":0.018,"adjAntiMortal":0.018,"adjRealDmg":19,"adjRealDmgDef":19,"adjMonsterDmg":0.0135,"adjMonsterDmgAnti":0.0128,"adjFinalDmg":0.0045,"adjFinalDmgAnti":0.0045,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000020: _tools.RODict({
        "propID": 51000020,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":240,"adjMinPhysicalAtk":310,"adjMaxPhysicalAtk":310,"adjMinMagicAtk":310,"adjMaxMagicAtk":310,"adjMinPhysicalArmor":173,"adjMaxPhysicalArmor":173,"adjMinMagicArmor":173,"adjMaxMagicArmor":173,"adjAccuracy":3,"adjEvasion":2,"adjFatal":3,"adjAntiFatal":1,"adjIgnoreArmor":0.006,"adjDmgArmor":0.006,"adjMortal":0.0282,"adjAntiMortal":0.0282,"adjRealDmg":20,"adjRealDmgDef":20,"adjMonsterDmg":0.0286,"adjMonsterDmgAnti":0.0278,"adjFinalDmg":0.0067,"adjFinalDmgAnti":0.0067,"adjStunEnh":2,"adjStunAnti":2,"adjSilentEnh":2,"adjSilentAnti":2,"adjKnockEnh":2,"adjKnockAnti":2,"adjFrozenEnh":2,"adjFrozenAnti":2,"adjSlowEnh":2,"adjSlowAnti":2,"adjPushEnh":2,"adjPushAnti":2})
    }),
    51000021: _tools.RODict({
        "propID": 51000021,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":266,"adjMinPhysicalAtk":332,"adjMaxPhysicalAtk":332,"adjMinMagicAtk":332,"adjMaxMagicAtk":332,"adjMinPhysicalArmor":179,"adjMaxPhysicalArmor":179,"adjMinMagicArmor":179,"adjMaxMagicArmor":179,"adjAccuracy":3,"adjEvasion":2,"adjFatal":4,"adjAntiFatal":1,"adjIgnoreArmor":0.006,"adjDmgArmor":0.006,"adjMortal":0.0282,"adjAntiMortal":0.0282,"adjRealDmg":21,"adjRealDmgDef":21,"adjMonsterDmg":0.0286,"adjMonsterDmgAnti":0.0278,"adjFinalDmg":0.0067,"adjFinalDmgAnti":0.0067,"adjStunEnh":2,"adjStunAnti":2,"adjSilentEnh":2,"adjSilentAnti":2,"adjKnockEnh":2,"adjKnockAnti":2,"adjFrozenEnh":2,"adjFrozenAnti":2,"adjSlowEnh":2,"adjSlowAnti":2,"adjPushEnh":2,"adjPushAnti":2})
    }),
    51000022: _tools.RODict({
        "propID": 51000022,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":292,"adjMinPhysicalAtk":347,"adjMaxPhysicalAtk":347,"adjMinMagicAtk":347,"adjMaxMagicAtk":347,"adjMinPhysicalArmor":187,"adjMaxPhysicalArmor":187,"adjMinMagicArmor":187,"adjMaxMagicArmor":187,"adjAccuracy":3,"adjEvasion":2,"adjFatal":5,"adjAntiFatal":1,"adjIgnoreArmor":0.006,"adjDmgArmor":0.006,"adjMortal":0.0282,"adjAntiMortal":0.0282,"adjRealDmg":22,"adjRealDmgDef":22,"adjMonsterDmg":0.0286,"adjMonsterDmgAnti":0.0278,"adjFinalDmg":0.0067,"adjFinalDmgAnti":0.0067,"adjStunEnh":2,"adjStunAnti":2,"adjSilentEnh":2,"adjSilentAnti":2,"adjKnockEnh":2,"adjKnockAnti":2,"adjFrozenEnh":2,"adjFrozenAnti":2,"adjSlowEnh":2,"adjSlowAnti":2,"adjPushEnh":2,"adjPushAnti":2})
    }),
    51000023: _tools.RODict({
        "propID": 51000023,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":319,"adjMinPhysicalAtk":371,"adjMaxPhysicalAtk":371,"adjMinMagicAtk":371,"adjMaxMagicAtk":371,"adjMinPhysicalArmor":204,"adjMaxPhysicalArmor":204,"adjMinMagicArmor":204,"adjMaxMagicArmor":204,"adjAccuracy":3,"adjEvasion":2,"adjFatal":6,"adjAntiFatal":1,"adjIgnoreArmor":0.006,"adjDmgArmor":0.006,"adjMortal":0.0282,"adjAntiMortal":0.0282,"adjRealDmg":23,"adjRealDmgDef":23,"adjMonsterDmg":0.0286,"adjMonsterDmgAnti":0.0278,"adjFinalDmg":0.0067,"adjFinalDmgAnti":0.0067,"adjStunEnh":2,"adjStunAnti":2,"adjSilentEnh":2,"adjSilentAnti":2,"adjKnockEnh":2,"adjKnockAnti":2,"adjFrozenEnh":2,"adjFrozenAnti":2,"adjSlowEnh":2,"adjSlowAnti":2,"adjPushEnh":2,"adjPushAnti":2})
    }),
    51000024: _tools.RODict({
        "propID": 51000024,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":345,"adjMinPhysicalAtk":383,"adjMaxPhysicalAtk":383,"adjMinMagicAtk":383,"adjMaxMagicAtk":383,"adjMinPhysicalArmor":210,"adjMaxPhysicalArmor":210,"adjMinMagicArmor":210,"adjMaxMagicArmor":210,"adjAccuracy":3,"adjEvasion":2,"adjFatal":7,"adjAntiFatal":1,"adjIgnoreArmor":0.006,"adjDmgArmor":0.006,"adjMortal":0.0282,"adjAntiMortal":0.0282,"adjRealDmg":24,"adjRealDmgDef":24,"adjMonsterDmg":0.0286,"adjMonsterDmgAnti":0.0278,"adjFinalDmg":0.0067,"adjFinalDmgAnti":0.0067,"adjStunEnh":2,"adjStunAnti":2,"adjSilentEnh":2,"adjSilentAnti":2,"adjKnockEnh":2,"adjKnockAnti":2,"adjFrozenEnh":2,"adjFrozenAnti":2,"adjSlowEnh":2,"adjSlowAnti":2,"adjPushEnh":2,"adjPushAnti":2})
    }),
    51000025: _tools.RODict({
        "propID": 51000025,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":372,"adjMinPhysicalAtk":428,"adjMaxPhysicalAtk":428,"adjMinMagicAtk":428,"adjMaxMagicAtk":428,"adjMinPhysicalArmor":229,"adjMaxPhysicalArmor":229,"adjMinMagicArmor":229,"adjMaxMagicArmor":229,"adjAccuracy":3,"adjEvasion":3,"adjFatal":8,"adjAntiFatal":1,"adjIgnoreArmor":0.0075,"adjDmgArmor":0.01,"adjMortal":0.0342,"adjAntiMortal":0.0342,"adjRealDmg":25,"adjRealDmgDef":25,"adjMonsterDmg":0.0416,"adjMonsterDmgAnti":0.0458,"adjFinalDmg":0.0083,"adjFinalDmgAnti":0.0083,"adjStunEnh":2,"adjStunAnti":2,"adjSilentEnh":2,"adjSilentAnti":2,"adjKnockEnh":2,"adjKnockAnti":2,"adjFrozenEnh":2,"adjFrozenAnti":2,"adjSlowEnh":2,"adjSlowAnti":2,"adjPushEnh":2,"adjPushAnti":2})
    }),
    51000026: _tools.RODict({
        "propID": 51000026,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":412,"adjMinPhysicalAtk":431,"adjMaxPhysicalAtk":431,"adjMinMagicAtk":431,"adjMaxMagicAtk":431,"adjMinPhysicalArmor":229,"adjMaxPhysicalArmor":229,"adjMinMagicArmor":229,"adjMaxMagicArmor":229,"adjAccuracy":4,"adjEvasion":3,"adjFatal":9,"adjAntiFatal":1,"adjIgnoreArmor":0.0075,"adjDmgArmor":0.01,"adjMortal":0.0383,"adjAntiMortal":0.0383,"adjRealDmg":26,"adjRealDmgDef":26,"adjMonsterDmg":0.0437,"adjMonsterDmgAnti":0.0479,"adjFinalDmg":0.009,"adjFinalDmgAnti":0.009,"adjStunEnh":3,"adjStunAnti":3,"adjSilentEnh":3,"adjSilentAnti":3,"adjKnockEnh":3,"adjKnockAnti":3,"adjFrozenEnh":3,"adjFrozenAnti":3,"adjSlowEnh":3,"adjSlowAnti":3,"adjPushEnh":3,"adjPushAnti":3})
    }),
    51000027: _tools.RODict({
        "propID": 51000027,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":453,"adjMinPhysicalAtk":454,"adjMaxPhysicalAtk":454,"adjMinMagicAtk":454,"adjMaxMagicAtk":454,"adjMinPhysicalArmor":239,"adjMaxPhysicalArmor":239,"adjMinMagicArmor":239,"adjMaxMagicArmor":239,"adjAccuracy":4,"adjEvasion":3,"adjFatal":10,"adjAntiFatal":1,"adjIgnoreArmor":0.0075,"adjDmgArmor":0.01,"adjMortal":0.0383,"adjAntiMortal":0.0383,"adjRealDmg":27,"adjRealDmgDef":27,"adjMonsterDmg":0.0437,"adjMonsterDmgAnti":0.0479,"adjFinalDmg":0.009,"adjFinalDmgAnti":0.009,"adjStunEnh":3,"adjStunAnti":3,"adjSilentEnh":3,"adjSilentAnti":3,"adjKnockEnh":3,"adjKnockAnti":3,"adjFrozenEnh":3,"adjFrozenAnti":3,"adjSlowEnh":3,"adjSlowAnti":3,"adjPushEnh":3,"adjPushAnti":3})
    }),
    51000028: _tools.RODict({
        "propID": 51000028,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":494,"adjMinPhysicalAtk":458,"adjMaxPhysicalAtk":458,"adjMinMagicAtk":458,"adjMaxMagicAtk":458,"adjMinPhysicalArmor":242,"adjMaxPhysicalArmor":242,"adjMinMagicArmor":242,"adjMaxMagicArmor":242,"adjAccuracy":4,"adjEvasion":3,"adjFatal":11,"adjAntiFatal":1,"adjIgnoreArmor":0.0075,"adjDmgArmor":0.01,"adjMortal":0.0425,"adjAntiMortal":0.0425,"adjRealDmg":28,"adjRealDmgDef":28,"adjMonsterDmg":0.0457,"adjMonsterDmgAnti":0.05,"adjFinalDmg":0.0097,"adjFinalDmgAnti":0.0097,"adjStunEnh":3,"adjStunAnti":3,"adjSilentEnh":3,"adjSilentAnti":3,"adjKnockEnh":3,"adjKnockAnti":3,"adjFrozenEnh":3,"adjFrozenAnti":3,"adjSlowEnh":3,"adjSlowAnti":3,"adjPushEnh":3,"adjPushAnti":3})
    }),
    51000029: _tools.RODict({
        "propID": 51000029,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":535,"adjMinPhysicalAtk":470,"adjMaxPhysicalAtk":470,"adjMinMagicAtk":470,"adjMaxMagicAtk":470,"adjMinPhysicalArmor":248,"adjMaxPhysicalArmor":248,"adjMinMagicArmor":248,"adjMaxMagicArmor":248,"adjAccuracy":4,"adjEvasion":3,"adjFatal":12,"adjAntiFatal":1,"adjIgnoreArmor":0.0075,"adjDmgArmor":0.01,"adjMortal":0.0425,"adjAntiMortal":0.0425,"adjRealDmg":29,"adjRealDmgDef":29,"adjMonsterDmg":0.0457,"adjMonsterDmgAnti":0.05,"adjFinalDmg":0.0097,"adjFinalDmgAnti":0.0097,"adjStunEnh":3,"adjStunAnti":3,"adjSilentEnh":3,"adjSilentAnti":3,"adjKnockEnh":3,"adjKnockAnti":3,"adjFrozenEnh":3,"adjFrozenAnti":3,"adjSlowEnh":3,"adjSlowAnti":3,"adjPushEnh":3,"adjPushAnti":3})
    }),
    51000030: _tools.RODict({
        "propID": 51000030,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":576,"adjMinPhysicalAtk":479,"adjMaxPhysicalAtk":479,"adjMinMagicAtk":479,"adjMaxMagicAtk":479,"adjMinPhysicalArmor":258,"adjMaxPhysicalArmor":258,"adjMinMagicArmor":258,"adjMaxMagicArmor":258,"adjAccuracy":4,"adjEvasion":3,"adjFatal":14,"adjAntiFatal":1,"adjIgnoreArmor":0.029,"adjDmgArmor":0.0115,"adjMortal":0.0627,"adjAntiMortal":0.0527,"adjRealDmg":30,"adjRealDmgDef":30,"adjMonsterDmg":0.0608,"adjMonsterDmgAnti":0.0651,"adjFinalDmg":0.012,"adjFinalDmgAnti":0.012,"adjStunEnh":4,"adjStunAnti":4,"adjSilentEnh":4,"adjSilentAnti":4,"adjKnockEnh":4,"adjKnockAnti":4,"adjFrozenEnh":4,"adjFrozenAnti":4,"adjSlowEnh":4,"adjSlowAnti":4,"adjPushEnh":4,"adjPushAnti":4})
    }),
    51000031: _tools.RODict({
        "propID": 51000031,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":590,"adjMinPhysicalAtk":490,"adjMaxPhysicalAtk":490,"adjMinMagicAtk":490,"adjMaxMagicAtk":490,"adjMinPhysicalArmor":264,"adjMaxPhysicalArmor":264,"adjMinMagicArmor":264,"adjMaxMagicArmor":264,"adjAccuracy":5,"adjEvasion":4,"adjFatal":15,"adjAntiFatal":3,"adjIgnoreArmor":0.033,"adjDmgArmor":0.0132,"adjMortal":0.0785,"adjAntiMortal":0.0595,"adjRealDmg":31,"adjRealDmgDef":31,"adjMonsterDmg":0.0777,"adjMonsterDmgAnti":0.0734,"adjFinalDmg":0.0155,"adjFinalDmgAnti":0.0135,"adjStunEnh":4,"adjStunAnti":4,"adjSilentEnh":4,"adjSilentAnti":4,"adjKnockEnh":4,"adjKnockAnti":4,"adjFrozenEnh":4,"adjFrozenAnti":4,"adjSlowEnh":4,"adjSlowAnti":4,"adjPushEnh":4,"adjPushAnti":4})
    }),
    51000032: _tools.RODict({
        "propID": 51000032,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":604,"adjMinPhysicalAtk":498,"adjMaxPhysicalAtk":498,"adjMinMagicAtk":498,"adjMaxMagicAtk":498,"adjMinPhysicalArmor":269,"adjMaxPhysicalArmor":269,"adjMinMagicArmor":269,"adjMaxMagicArmor":269,"adjAccuracy":5,"adjEvasion":4,"adjFatal":15,"adjAntiFatal":4,"adjIgnoreArmor":0.0369,"adjDmgArmor":0.0149,"adjMortal":0.0943,"adjAntiMortal":0.0663,"adjRealDmg":32,"adjRealDmgDef":32,"adjMonsterDmg":0.0945,"adjMonsterDmgAnti":0.0816,"adjFinalDmg":0.0191,"adjFinalDmgAnti":0.0151,"adjStunEnh":4,"adjStunAnti":4,"adjSilentEnh":4,"adjSilentAnti":4,"adjKnockEnh":4,"adjKnockAnti":4,"adjFrozenEnh":4,"adjFrozenAnti":4,"adjSlowEnh":4,"adjSlowAnti":4,"adjPushEnh":4,"adjPushAnti":4})
    }),
    51000033: _tools.RODict({
        "propID": 51000033,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":617,"adjMinPhysicalAtk":512,"adjMaxPhysicalAtk":512,"adjMinMagicAtk":512,"adjMaxMagicAtk":512,"adjMinPhysicalArmor":275,"adjMaxPhysicalArmor":275,"adjMinMagicArmor":275,"adjMaxMagicArmor":275,"adjAccuracy":5,"adjEvasion":4,"adjFatal":16,"adjAntiFatal":6,"adjIgnoreArmor":0.0409,"adjDmgArmor":0.0166,"adjMortal":0.1101,"adjAntiMortal":0.0731,"adjRealDmg":33,"adjRealDmgDef":33,"adjMonsterDmg":0.1114,"adjMonsterDmgAnti":0.0899,"adjFinalDmg":0.0226,"adjFinalDmgAnti":0.0166,"adjStunEnh":4,"adjStunAnti":4,"adjSilentEnh":4,"adjSilentAnti":4,"adjKnockEnh":4,"adjKnockAnti":4,"adjFrozenEnh":4,"adjFrozenAnti":4,"adjSlowEnh":4,"adjSlowAnti":4,"adjPushEnh":4,"adjPushAnti":4})
    }),
    51000034: _tools.RODict({
        "propID": 51000034,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":631,"adjMinPhysicalAtk":520,"adjMaxPhysicalAtk":520,"adjMinMagicAtk":520,"adjMaxMagicAtk":520,"adjMinPhysicalArmor":280,"adjMaxPhysicalArmor":280,"adjMinMagicArmor":280,"adjMaxMagicArmor":280,"adjAccuracy":6,"adjEvasion":4,"adjFatal":17,"adjAntiFatal":7,"adjIgnoreArmor":0.0448,"adjDmgArmor":0.0183,"adjMortal":0.1259,"adjAntiMortal":0.0799,"adjRealDmg":34,"adjRealDmgDef":34,"adjMonsterDmg":0.1282,"adjMonsterDmgAnti":0.0982,"adjFinalDmg":0.0261,"adjFinalDmgAnti":0.0181,"adjStunEnh":5,"adjStunAnti":5,"adjSilentEnh":5,"adjSilentAnti":5,"adjKnockEnh":5,"adjKnockAnti":5,"adjFrozenEnh":5,"adjFrozenAnti":5,"adjSlowEnh":5,"adjSlowAnti":5,"adjPushEnh":5,"adjPushAnti":5})
    }),
    51000035: _tools.RODict({
        "propID": 51000035,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":645,"adjMinPhysicalAtk":528,"adjMaxPhysicalAtk":528,"adjMinMagicAtk":528,"adjMaxMagicAtk":528,"adjMinPhysicalArmor":286,"adjMaxPhysicalArmor":286,"adjMinMagicArmor":286,"adjMaxMagicArmor":286,"adjAccuracy":6,"adjEvasion":5,"adjFatal":17,"adjAntiFatal":9,"adjIgnoreArmor":0.0488,"adjDmgArmor":0.02,"adjMortal":0.1417,"adjAntiMortal":0.0867,"adjRealDmg":35,"adjRealDmgDef":35,"adjMonsterDmg":0.1451,"adjMonsterDmgAnti":0.1065,"adjFinalDmg":0.0296,"adjFinalDmgAnti":0.0196,"adjStunEnh":5,"adjStunAnti":5,"adjSilentEnh":5,"adjSilentAnti":5,"adjKnockEnh":5,"adjKnockAnti":5,"adjFrozenEnh":5,"adjFrozenAnti":5,"adjSlowEnh":5,"adjSlowAnti":5,"adjPushEnh":5,"adjPushAnti":5})
    }),
    51000036: _tools.RODict({
        "propID": 51000036,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":658,"adjMinPhysicalAtk":542,"adjMaxPhysicalAtk":542,"adjMinMagicAtk":542,"adjMaxMagicAtk":542,"adjMinPhysicalArmor":292,"adjMaxPhysicalArmor":292,"adjMinMagicArmor":292,"adjMaxMagicArmor":292,"adjAccuracy":6,"adjEvasion":5,"adjFatal":18,"adjAntiFatal":10,"adjIgnoreArmor":0.0527,"adjDmgArmor":0.0217,"adjMortal":0.1575,"adjAntiMortal":0.0935,"adjRealDmg":36,"adjRealDmgDef":36,"adjMonsterDmg":0.1619,"adjMonsterDmgAnti":0.1147,"adjFinalDmg":0.0331,"adjFinalDmgAnti":0.0211,"adjStunEnh":5,"adjStunAnti":5,"adjSilentEnh":5,"adjSilentAnti":5,"adjKnockEnh":5,"adjKnockAnti":5,"adjFrozenEnh":5,"adjFrozenAnti":5,"adjSlowEnh":5,"adjSlowAnti":5,"adjPushEnh":5,"adjPushAnti":5})
    }),
    51000037: _tools.RODict({
        "propID": 51000037,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":672,"adjMinPhysicalAtk":551,"adjMaxPhysicalAtk":551,"adjMinMagicAtk":551,"adjMaxMagicAtk":551,"adjMinPhysicalArmor":297,"adjMaxPhysicalArmor":297,"adjMinMagicArmor":297,"adjMaxMagicArmor":297,"adjAccuracy":7,"adjEvasion":5,"adjFatal":19,"adjAntiFatal":12,"adjIgnoreArmor":0.0567,"adjDmgArmor":0.0234,"adjMortal":0.1733,"adjAntiMortal":0.1003,"adjRealDmg":37,"adjRealDmgDef":37,"adjMonsterDmg":0.1788,"adjMonsterDmgAnti":0.123,"adjFinalDmg":0.0367,"adjFinalDmgAnti":0.0227,"adjStunEnh":5,"adjStunAnti":5,"adjSilentEnh":5,"adjSilentAnti":5,"adjKnockEnh":5,"adjKnockAnti":5,"adjFrozenEnh":5,"adjFrozenAnti":5,"adjSlowEnh":5,"adjSlowAnti":5,"adjPushEnh":5,"adjPushAnti":5})
    }),
    51000038: _tools.RODict({
        "propID": 51000038,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":685,"adjMinPhysicalAtk":559,"adjMaxPhysicalAtk":559,"adjMinMagicAtk":559,"adjMaxMagicAtk":559,"adjMinPhysicalArmor":303,"adjMaxPhysicalArmor":303,"adjMinMagicArmor":303,"adjMaxMagicArmor":303,"adjAccuracy":7,"adjEvasion":5,"adjFatal":19,"adjAntiFatal":14,"adjIgnoreArmor":0.0606,"adjDmgArmor":0.0251,"adjMortal":0.1891,"adjAntiMortal":0.1071,"adjRealDmg":38,"adjRealDmgDef":38,"adjMonsterDmg":0.1956,"adjMonsterDmgAnti":0.1313,"adjFinalDmg":0.0402,"adjFinalDmgAnti":0.0242,"adjStunEnh":5,"adjStunAnti":5,"adjSilentEnh":5,"adjSilentAnti":5,"adjKnockEnh":5,"adjKnockAnti":5,"adjFrozenEnh":5,"adjFrozenAnti":5,"adjSlowEnh":5,"adjSlowAnti":5,"adjPushEnh":5,"adjPushAnti":5})
    }),
    51000039: _tools.RODict({
        "propID": 51000039,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":698,"adjMinPhysicalAtk":567,"adjMaxPhysicalAtk":567,"adjMinMagicAtk":567,"adjMaxMagicAtk":567,"adjMinPhysicalArmor":309,"adjMaxPhysicalArmor":309,"adjMinMagicArmor":309,"adjMaxMagicArmor":309,"adjAccuracy":7,"adjEvasion":6,"adjFatal":20,"adjAntiFatal":15,"adjIgnoreArmor":0.0646,"adjDmgArmor":0.0268,"adjMortal":0.2049,"adjAntiMortal":0.1139,"adjRealDmg":39,"adjRealDmgDef":39,"adjMonsterDmg":0.2125,"adjMonsterDmgAnti":0.1396,"adjFinalDmg":0.0437,"adjFinalDmgAnti":0.0257,"adjStunEnh":5,"adjStunAnti":5,"adjSilentEnh":5,"adjSilentAnti":5,"adjKnockEnh":5,"adjKnockAnti":5,"adjFrozenEnh":5,"adjFrozenAnti":5,"adjSlowEnh":5,"adjSlowAnti":5,"adjPushEnh":5,"adjPushAnti":5})
    }),
    51000040: _tools.RODict({
        "propID": 51000040,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":711,"adjMinPhysicalAtk":582,"adjMaxPhysicalAtk":582,"adjMinMagicAtk":582,"adjMaxMagicAtk":582,"adjMinPhysicalArmor":314,"adjMaxPhysicalArmor":314,"adjMinMagicArmor":314,"adjMaxMagicArmor":314,"adjAccuracy":8,"adjEvasion":6,"adjFatal":21,"adjAntiFatal":17,"adjIgnoreArmor":0.0685,"adjDmgArmor":0.0285,"adjMortal":0.2207,"adjAntiMortal":0.1207,"adjRealDmg":40,"adjRealDmgDef":40,"adjMonsterDmg":0.2293,"adjMonsterDmgAnti":0.1478,"adjFinalDmg":0.0473,"adjFinalDmgAnti":0.0272,"adjStunEnh":7,"adjStunAnti":7,"adjSilentEnh":7,"adjSilentAnti":7,"adjKnockEnh":7,"adjKnockAnti":7,"adjFrozenEnh":7,"adjFrozenAnti":7,"adjSlowEnh":7,"adjSlowAnti":7,"adjPushEnh":7,"adjPushAnti":7})
    }),
    51000041: _tools.RODict({
        "propID": 51000041,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":729,"adjMinPhysicalAtk":596,"adjMaxPhysicalAtk":596,"adjMinMagicAtk":596,"adjMaxMagicAtk":596,"adjMinPhysicalArmor":322,"adjMaxPhysicalArmor":322,"adjMinMagicArmor":322,"adjMaxMagicArmor":322,"adjAccuracy":9,"adjEvasion":7,"adjFatal":22,"adjAntiFatal":17,"adjIgnoreArmor":0.0715,"adjDmgArmor":0.0295,"adjMortal":0.2391,"adjAntiMortal":0.1294,"adjRealDmg":41,"adjRealDmgDef":41,"adjMonsterDmg":0.2376,"adjMonsterDmgAnti":0.1561,"adjFinalDmg":0.0524,"adjFinalDmgAnti":0.0294,"adjStunEnh":7,"adjStunAnti":7,"adjSilentEnh":7,"adjSilentAnti":7,"adjKnockEnh":7,"adjKnockAnti":7,"adjFrozenEnh":7,"adjFrozenAnti":7,"adjSlowEnh":7,"adjSlowAnti":7,"adjPushEnh":7,"adjPushAnti":7})
    }),
    51000042: _tools.RODict({
        "propID": 51000042,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":747,"adjMinPhysicalAtk":611,"adjMaxPhysicalAtk":611,"adjMinMagicAtk":611,"adjMaxMagicAtk":611,"adjMinPhysicalArmor":330,"adjMaxPhysicalArmor":330,"adjMinMagicArmor":330,"adjMaxMagicArmor":330,"adjAccuracy":9,"adjEvasion":8,"adjFatal":22,"adjAntiFatal":18,"adjIgnoreArmor":0.0744,"adjDmgArmor":0.0304,"adjMortal":0.2576,"adjAntiMortal":0.1382,"adjRealDmg":42,"adjRealDmgDef":42,"adjMonsterDmg":0.2459,"adjMonsterDmgAnti":0.1644,"adjFinalDmg":0.0575,"adjFinalDmgAnti":0.0315,"adjStunEnh":7,"adjStunAnti":7,"adjSilentEnh":7,"adjSilentAnti":7,"adjKnockEnh":7,"adjKnockAnti":7,"adjFrozenEnh":7,"adjFrozenAnti":7,"adjSlowEnh":7,"adjSlowAnti":7,"adjPushEnh":7,"adjPushAnti":7})
    }),
    51000043: _tools.RODict({
        "propID": 51000043,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":765,"adjMinPhysicalAtk":625,"adjMaxPhysicalAtk":625,"adjMinMagicAtk":625,"adjMaxMagicAtk":625,"adjMinPhysicalArmor":339,"adjMaxPhysicalArmor":339,"adjMinMagicArmor":339,"adjMaxMagicArmor":339,"adjAccuracy":9,"adjEvasion":8,"adjFatal":23,"adjAntiFatal":18,"adjIgnoreArmor":0.0774,"adjDmgArmor":0.0314,"adjMortal":0.2761,"adjAntiMortal":0.147,"adjRealDmg":43,"adjRealDmgDef":43,"adjMonsterDmg":0.2542,"adjMonsterDmgAnti":0.1726,"adjFinalDmg":0.0626,"adjFinalDmgAnti":0.0336,"adjStunEnh":7,"adjStunAnti":7,"adjSilentEnh":7,"adjSilentAnti":7,"adjKnockEnh":7,"adjKnockAnti":7,"adjFrozenEnh":7,"adjFrozenAnti":7,"adjSlowEnh":7,"adjSlowAnti":7,"adjPushEnh":7,"adjPushAnti":7})
    }),
    51000044: _tools.RODict({
        "propID": 51000044,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":784,"adjMinPhysicalAtk":640,"adjMaxPhysicalAtk":640,"adjMinMagicAtk":640,"adjMaxMagicAtk":640,"adjMinPhysicalArmor":347,"adjMaxPhysicalArmor":347,"adjMinMagicArmor":347,"adjMaxMagicArmor":347,"adjAccuracy":10,"adjEvasion":8,"adjFatal":24,"adjAntiFatal":19,"adjIgnoreArmor":0.0803,"adjDmgArmor":0.0323,"adjMortal":0.2945,"adjAntiMortal":0.1557,"adjRealDmg":44,"adjRealDmgDef":44,"adjMonsterDmg":0.2625,"adjMonsterDmgAnti":0.1809,"adjFinalDmg":0.0678,"adjFinalDmgAnti":0.0358,"adjStunEnh":8,"adjStunAnti":8,"adjSilentEnh":8,"adjSilentAnti":8,"adjKnockEnh":8,"adjKnockAnti":8,"adjFrozenEnh":8,"adjFrozenAnti":8,"adjSlowEnh":8,"adjSlowAnti":8,"adjPushEnh":8,"adjPushAnti":8})
    }),
    51000045: _tools.RODict({
        "propID": 51000045,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":803,"adjMinPhysicalAtk":651,"adjMaxPhysicalAtk":651,"adjMinMagicAtk":651,"adjMaxMagicAtk":651,"adjMinPhysicalArmor":355,"adjMaxPhysicalArmor":355,"adjMinMagicArmor":355,"adjMaxMagicArmor":355,"adjAccuracy":10,"adjEvasion":9,"adjFatal":25,"adjAntiFatal":20,"adjIgnoreArmor":0.0833,"adjDmgArmor":0.0333,"adjMortal":0.313,"adjAntiMortal":0.1645,"adjRealDmg":45,"adjRealDmgDef":45,"adjMonsterDmg":0.2707,"adjMonsterDmgAnti":0.1891,"adjFinalDmg":0.0729,"adjFinalDmgAnti":0.0379,"adjStunEnh":8,"adjStunAnti":8,"adjSilentEnh":8,"adjSilentAnti":8,"adjKnockEnh":8,"adjKnockAnti":8,"adjFrozenEnh":8,"adjFrozenAnti":8,"adjSlowEnh":8,"adjSlowAnti":8,"adjPushEnh":8,"adjPushAnti":8})
    }),
    51000046: _tools.RODict({
        "propID": 51000046,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":822,"adjMinPhysicalAtk":666,"adjMaxPhysicalAtk":666,"adjMinMagicAtk":666,"adjMaxMagicAtk":666,"adjMinPhysicalArmor":363,"adjMaxPhysicalArmor":363,"adjMinMagicArmor":363,"adjMaxMagicArmor":363,"adjAccuracy":10,"adjEvasion":9,"adjFatal":25,"adjAntiFatal":20,"adjIgnoreArmor":0.0862,"adjDmgArmor":0.0342,"adjMortal":0.3315,"adjAntiMortal":0.1733,"adjRealDmg":46,"adjRealDmgDef":46,"adjMonsterDmg":0.279,"adjMonsterDmgAnti":0.1974,"adjFinalDmg":0.078,"adjFinalDmgAnti":0.04,"adjStunEnh":8,"adjStunAnti":8,"adjSilentEnh":8,"adjSilentAnti":8,"adjKnockEnh":8,"adjKnockAnti":8,"adjFrozenEnh":8,"adjFrozenAnti":8,"adjSlowEnh":8,"adjSlowAnti":8,"adjPushEnh":8,"adjPushAnti":8})
    }),
    51000047: _tools.RODict({
        "propID": 51000047,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":842,"adjMinPhysicalAtk":681,"adjMaxPhysicalAtk":681,"adjMinMagicAtk":681,"adjMaxMagicAtk":681,"adjMinPhysicalArmor":371,"adjMaxPhysicalArmor":371,"adjMinMagicArmor":371,"adjMaxMagicArmor":371,"adjAccuracy":11,"adjEvasion":9,"adjFatal":26,"adjAntiFatal":21,"adjIgnoreArmor":0.0892,"adjDmgArmor":0.0352,"adjMortal":0.3499,"adjAntiMortal":0.182,"adjRealDmg":47,"adjRealDmgDef":47,"adjMonsterDmg":0.2873,"adjMonsterDmgAnti":0.2056,"adjFinalDmg":0.0831,"adjFinalDmgAnti":0.0421,"adjStunEnh":8,"adjStunAnti":8,"adjSilentEnh":8,"adjSilentAnti":8,"adjKnockEnh":8,"adjKnockAnti":8,"adjFrozenEnh":8,"adjFrozenAnti":8,"adjSlowEnh":8,"adjSlowAnti":8,"adjPushEnh":8,"adjPushAnti":8})
    }),
    51000048: _tools.RODict({
        "propID": 51000048,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":862,"adjMinPhysicalAtk":693,"adjMaxPhysicalAtk":693,"adjMinMagicAtk":693,"adjMaxMagicAtk":693,"adjMinPhysicalArmor":379,"adjMaxPhysicalArmor":379,"adjMinMagicArmor":379,"adjMaxMagicArmor":379,"adjAccuracy":11,"adjEvasion":9,"adjFatal":27,"adjAntiFatal":21,"adjIgnoreArmor":0.0921,"adjDmgArmor":0.0361,"adjMortal":0.3684,"adjAntiMortal":0.1908,"adjRealDmg":48,"adjRealDmgDef":48,"adjMonsterDmg":0.2956,"adjMonsterDmgAnti":0.2139,"adjFinalDmg":0.0883,"adjFinalDmgAnti":0.0443,"adjStunEnh":9,"adjStunAnti":9,"adjSilentEnh":9,"adjSilentAnti":9,"adjKnockEnh":9,"adjKnockAnti":9,"adjFrozenEnh":9,"adjFrozenAnti":9,"adjSlowEnh":9,"adjSlowAnti":9,"adjPushEnh":9,"adjPushAnti":9})
    }),
    51000049: _tools.RODict({
        "propID": 51000049,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":882,"adjMinPhysicalAtk":704,"adjMaxPhysicalAtk":704,"adjMinMagicAtk":704,"adjMaxMagicAtk":704,"adjMinPhysicalArmor":387,"adjMaxPhysicalArmor":387,"adjMinMagicArmor":387,"adjMaxMagicArmor":387,"adjAccuracy":11,"adjEvasion":10,"adjFatal":28,"adjAntiFatal":22,"adjIgnoreArmor":0.0951,"adjDmgArmor":0.037,"adjMortal":0.3869,"adjAntiMortal":0.1996,"adjRealDmg":49,"adjRealDmgDef":49,"adjMonsterDmg":0.3039,"adjMonsterDmgAnti":0.2222,"adjFinalDmg":0.0934,"adjFinalDmgAnti":0.0464,"adjStunEnh":9,"adjStunAnti":9,"adjSilentEnh":9,"adjSilentAnti":9,"adjKnockEnh":9,"adjKnockAnti":9,"adjFrozenEnh":9,"adjFrozenAnti":9,"adjSlowEnh":9,"adjSlowAnti":9,"adjPushEnh":9,"adjPushAnti":9})
    }),
    51000050: _tools.RODict({
        "propID": 51000050,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":903,"adjMinPhysicalAtk":720,"adjMaxPhysicalAtk":720,"adjMinMagicAtk":720,"adjMaxMagicAtk":720,"adjAtkBless":1,"adjMinPhysicalArmor":395,"adjMaxPhysicalArmor":395,"adjMinMagicArmor":395,"adjMaxMagicArmor":395,"adjAccuracy":12,"adjEvasion":10,"adjFatal":28,"adjAntiFatal":23,"adjIgnoreArmor":0.098,"adjDmgArmor":0.038,"adjMortal":0.4053,"adjAntiMortal":0.2083,"adjRealDmg":50,"adjRealDmgDef":50,"adjMonsterDmg":0.3122,"adjMonsterDmgAnti":0.2304,"adjFinalDmg":0.0985,"adjFinalDmgAnti":0.0485,"adjStunEnh":10,"adjStunAnti":10,"adjSilentEnh":10,"adjSilentAnti":10,"adjKnockEnh":10,"adjKnockAnti":10,"adjFrozenEnh":10,"adjFrozenAnti":10,"adjSlowEnh":10,"adjSlowAnti":10,"adjPushEnh":10,"adjPushAnti":10})
    }),
    51000051: _tools.RODict({
        "propID": 51000051,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":919,"adjMinPhysicalAtk":742,"adjMaxPhysicalAtk":742,"adjMinMagicAtk":742,"adjMaxMagicAtk":742,"adjAtkBless":1,"adjMinPhysicalArmor":408,"adjMaxPhysicalArmor":408,"adjMinMagicArmor":408,"adjMaxMagicArmor":408,"adjAccuracy":12,"adjEvasion":10,"adjFatal":29,"adjAntiFatal":23,"adjIgnoreArmor":0.0998,"adjDmgArmor":0.0398,"adjMortal":0.4135,"adjAntiMortal":0.2158,"adjRealDmg":51,"adjRealDmgDef":51,"adjMonsterDmg":0.3223,"adjMonsterDmgAnti":0.2404,"adjFinalDmg":0.1003,"adjFinalDmgAnti":0.0503,"adjStunEnh":10,"adjStunAnti":10,"adjSilentEnh":10,"adjSilentAnti":10,"adjKnockEnh":10,"adjKnockAnti":10,"adjFrozenEnh":10,"adjFrozenAnti":10,"adjSlowEnh":10,"adjSlowAnti":10,"adjPushEnh":10,"adjPushAnti":10})
    }),
    51000052: _tools.RODict({
        "propID": 51000052,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":935,"adjMinPhysicalAtk":764,"adjMaxPhysicalAtk":764,"adjMinMagicAtk":764,"adjMaxMagicAtk":764,"adjAtkBless":1,"adjMinPhysicalArmor":420,"adjMaxPhysicalArmor":420,"adjMinMagicArmor":420,"adjMaxMagicArmor":420,"adjAccuracy":12,"adjEvasion":11,"adjFatal":30,"adjAntiFatal":24,"adjIgnoreArmor":0.1015,"adjDmgArmor":0.0415,"adjMortal":0.4217,"adjAntiMortal":0.2233,"adjRealDmg":52,"adjRealDmgDef":52,"adjMonsterDmg":0.3323,"adjMonsterDmgAnti":0.2504,"adjFinalDmg":0.1021,"adjFinalDmgAnti":0.0521,"adjStunEnh":11,"adjStunAnti":11,"adjSilentEnh":11,"adjSilentAnti":11,"adjKnockEnh":11,"adjKnockAnti":11,"adjFrozenEnh":11,"adjFrozenAnti":11,"adjSlowEnh":11,"adjSlowAnti":11,"adjPushEnh":11,"adjPushAnti":11})
    }),
    51000053: _tools.RODict({
        "propID": 51000053,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":951,"adjMinPhysicalAtk":786,"adjMaxPhysicalAtk":786,"adjMinMagicAtk":786,"adjMaxMagicAtk":786,"adjAtkBless":1,"adjMinPhysicalArmor":433,"adjMaxPhysicalArmor":433,"adjMinMagicArmor":433,"adjMaxMagicArmor":433,"adjAccuracy":13,"adjEvasion":11,"adjFatal":31,"adjAntiFatal":24,"adjIgnoreArmor":0.1033,"adjDmgArmor":0.0433,"adjMortal":0.4298,"adjAntiMortal":0.2307,"adjRealDmg":53,"adjRealDmgDef":53,"adjMonsterDmg":0.3424,"adjMonsterDmgAnti":0.2604,"adjFinalDmg":0.1039,"adjFinalDmgAnti":0.0539,"adjStunEnh":11,"adjStunAnti":11,"adjSilentEnh":11,"adjSilentAnti":11,"adjKnockEnh":11,"adjKnockAnti":11,"adjFrozenEnh":11,"adjFrozenAnti":11,"adjSlowEnh":11,"adjSlowAnti":11,"adjPushEnh":11,"adjPushAnti":11})
    }),
    51000054: _tools.RODict({
        "propID": 51000054,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":968,"adjMinPhysicalAtk":809,"adjMaxPhysicalAtk":809,"adjMinMagicAtk":809,"adjMaxMagicAtk":809,"adjAtkBless":1,"adjMinPhysicalArmor":446,"adjMaxPhysicalArmor":446,"adjMinMagicArmor":446,"adjMaxMagicArmor":446,"adjAccuracy":13,"adjEvasion":11,"adjFatal":32,"adjAntiFatal":25,"adjIgnoreArmor":0.105,"adjDmgArmor":0.045,"adjMortal":0.438,"adjAntiMortal":0.2382,"adjRealDmg":54,"adjRealDmgDef":54,"adjMonsterDmg":0.3525,"adjMonsterDmgAnti":0.2704,"adjFinalDmg":0.1057,"adjFinalDmgAnti":0.0557,"adjStunEnh":11,"adjStunAnti":11,"adjSilentEnh":11,"adjSilentAnti":11,"adjKnockEnh":11,"adjKnockAnti":11,"adjFrozenEnh":11,"adjFrozenAnti":11,"adjSlowEnh":11,"adjSlowAnti":11,"adjPushEnh":11,"adjPushAnti":11})
    }),
    51000055: _tools.RODict({
        "propID": 51000055,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":984,"adjMinPhysicalAtk":832,"adjMaxPhysicalAtk":832,"adjMinMagicAtk":832,"adjMaxMagicAtk":832,"adjAtkBless":1,"adjMinPhysicalArmor":458,"adjMaxPhysicalArmor":458,"adjMinMagicArmor":458,"adjMaxMagicArmor":458,"adjAccuracy":13,"adjEvasion":12,"adjFatal":32,"adjAntiFatal":25,"adjIgnoreArmor":0.1068,"adjDmgArmor":0.0468,"adjMortal":0.4462,"adjAntiMortal":0.2457,"adjRealDmg":55,"adjRealDmgDef":55,"adjMonsterDmg":0.3626,"adjMonsterDmgAnti":0.2803,"adjFinalDmg":0.1075,"adjFinalDmgAnti":0.0575,"adjStunEnh":11,"adjStunAnti":11,"adjSilentEnh":11,"adjSilentAnti":11,"adjKnockEnh":11,"adjKnockAnti":11,"adjFrozenEnh":11,"adjFrozenAnti":11,"adjSlowEnh":11,"adjSlowAnti":11,"adjPushEnh":11,"adjPushAnti":11})
    }),
    51000056: _tools.RODict({
        "propID": 51000056,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1001,"adjMinPhysicalAtk":856,"adjMaxPhysicalAtk":856,"adjMinMagicAtk":856,"adjMaxMagicAtk":856,"adjAtkBless":1,"adjMinPhysicalArmor":471,"adjMaxPhysicalArmor":471,"adjMinMagicArmor":471,"adjMaxMagicArmor":471,"adjAccuracy":14,"adjEvasion":12,"adjFatal":33,"adjAntiFatal":26,"adjIgnoreArmor":0.1085,"adjDmgArmor":0.0485,"adjMortal":0.4543,"adjAntiMortal":0.2531,"adjRealDmg":56,"adjRealDmgDef":56,"adjMonsterDmg":0.3727,"adjMonsterDmgAnti":0.2903,"adjFinalDmg":0.1093,"adjFinalDmgAnti":0.0593,"adjStunEnh":12,"adjStunAnti":12,"adjSilentEnh":12,"adjSilentAnti":12,"adjKnockEnh":12,"adjKnockAnti":12,"adjFrozenEnh":12,"adjFrozenAnti":12,"adjSlowEnh":12,"adjSlowAnti":12,"adjPushEnh":12,"adjPushAnti":12})
    }),
    51000057: _tools.RODict({
        "propID": 51000057,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1019,"adjMinPhysicalAtk":871,"adjMaxPhysicalAtk":871,"adjMinMagicAtk":871,"adjMaxMagicAtk":871,"adjAtkBless":1,"adjMinPhysicalArmor":483,"adjMaxPhysicalArmor":483,"adjMinMagicArmor":483,"adjMaxMagicArmor":483,"adjAccuracy":14,"adjEvasion":12,"adjFatal":34,"adjAntiFatal":26,"adjIgnoreArmor":0.1103,"adjDmgArmor":0.0503,"adjMortal":0.4625,"adjAntiMortal":0.2606,"adjRealDmg":57,"adjRealDmgDef":57,"adjMonsterDmg":0.3828,"adjMonsterDmgAnti":0.3003,"adjFinalDmg":0.1111,"adjFinalDmgAnti":0.0611,"adjStunEnh":12,"adjStunAnti":12,"adjSilentEnh":12,"adjSilentAnti":12,"adjKnockEnh":12,"adjKnockAnti":12,"adjFrozenEnh":12,"adjFrozenAnti":12,"adjSlowEnh":12,"adjSlowAnti":12,"adjPushEnh":12,"adjPushAnti":12})
    }),
    51000058: _tools.RODict({
        "propID": 51000058,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1036,"adjMinPhysicalAtk":895,"adjMaxPhysicalAtk":895,"adjMinMagicAtk":895,"adjMaxMagicAtk":895,"adjAtkBless":1,"adjMinPhysicalArmor":496,"adjMaxPhysicalArmor":496,"adjMinMagicArmor":496,"adjMaxMagicArmor":496,"adjAccuracy":15,"adjEvasion":13,"adjFatal":35,"adjAntiFatal":27,"adjIgnoreArmor":0.112,"adjDmgArmor":0.052,"adjMortal":0.4707,"adjAntiMortal":0.2681,"adjRealDmg":58,"adjRealDmgDef":58,"adjMonsterDmg":0.3928,"adjMonsterDmgAnti":0.3103,"adjFinalDmg":0.1129,"adjFinalDmgAnti":0.0629,"adjStunEnh":12,"adjStunAnti":12,"adjSilentEnh":12,"adjSilentAnti":12,"adjKnockEnh":12,"adjKnockAnti":12,"adjFrozenEnh":12,"adjFrozenAnti":12,"adjSlowEnh":12,"adjSlowAnti":12,"adjPushEnh":12,"adjPushAnti":12})
    }),
    51000059: _tools.RODict({
        "propID": 51000059,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1054,"adjMinPhysicalAtk":919,"adjMaxPhysicalAtk":919,"adjMinMagicAtk":919,"adjMaxMagicAtk":919,"adjAtkBless":1,"adjMinPhysicalArmor":509,"adjMaxPhysicalArmor":509,"adjMinMagicArmor":509,"adjMaxMagicArmor":509,"adjAccuracy":15,"adjEvasion":13,"adjFatal":36,"adjAntiFatal":27,"adjIgnoreArmor":0.1138,"adjDmgArmor":0.0538,"adjMortal":0.4788,"adjAntiMortal":0.2755,"adjRealDmg":59,"adjRealDmgDef":59,"adjMonsterDmg":0.4029,"adjMonsterDmgAnti":0.3203,"adjFinalDmg":0.1147,"adjFinalDmgAnti":0.0647,"adjStunEnh":12,"adjStunAnti":12,"adjSilentEnh":12,"adjSilentAnti":12,"adjKnockEnh":12,"adjKnockAnti":12,"adjFrozenEnh":12,"adjFrozenAnti":12,"adjSlowEnh":12,"adjSlowAnti":12,"adjPushEnh":12,"adjPushAnti":12})
    }),
    51000060: _tools.RODict({
        "propID": 51000060,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1071,"adjMinPhysicalAtk":939,"adjMaxPhysicalAtk":939,"adjMinMagicAtk":939,"adjMaxMagicAtk":939,"adjAtkBless":2,"adjMinPhysicalArmor":521,"adjMaxPhysicalArmor":521,"adjMinMagicArmor":521,"adjMaxMagicArmor":521,"adjAccuracy":16,"adjEvasion":15,"adjFatal":37,"adjAntiFatal":28,"adjIgnoreArmor":0.1155,"adjDmgArmor":0.0555,"adjMortal":0.487,"adjAntiMortal":0.283,"adjRealDmg":60,"adjRealDmgDef":60,"adjMonsterDmg":0.413,"adjMonsterDmgAnti":0.3302,"adjFinalDmg":0.1165,"adjFinalDmgAnti":0.0665,"adjStunEnh":13,"adjStunAnti":13,"adjSilentEnh":13,"adjSilentAnti":13,"adjKnockEnh":13,"adjKnockAnti":13,"adjFrozenEnh":13,"adjFrozenAnti":13,"adjSlowEnh":13,"adjSlowAnti":13,"adjPushEnh":13,"adjPushAnti":13})
    }),
    51000061: _tools.RODict({
        "propID": 51000061,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1087,"adjMinPhysicalAtk":965,"adjMaxPhysicalAtk":965,"adjMinMagicAtk":965,"adjMaxMagicAtk":965,"adjAtkBless":2,"adjMinPhysicalArmor":535,"adjMaxPhysicalArmor":535,"adjMinMagicArmor":535,"adjMaxMagicArmor":535,"adjAccuracy":17,"adjEvasion":15,"adjFatal":37,"adjAntiFatal":28,"adjIgnoreArmor":0.1164,"adjDmgArmor":0.0564,"adjMortal":0.4948,"adjAntiMortal":0.2911,"adjRealDmg":61,"adjRealDmgDef":61,"adjMonsterDmg":0.4214,"adjMonsterDmgAnti":0.3385,"adjFinalDmg":0.1184,"adjFinalDmgAnti":0.0684,"adjStunEnh":13,"adjStunAnti":13,"adjSilentEnh":13,"adjSilentAnti":13,"adjKnockEnh":13,"adjKnockAnti":13,"adjFrozenEnh":13,"adjFrozenAnti":13,"adjSlowEnh":13,"adjSlowAnti":13,"adjPushEnh":13,"adjPushAnti":13})
    }),
    51000062: _tools.RODict({
        "propID": 51000062,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1103,"adjMinPhysicalAtk":982,"adjMaxPhysicalAtk":982,"adjMinMagicAtk":982,"adjMaxMagicAtk":982,"adjAtkBless":2,"adjMinPhysicalArmor":548,"adjMaxPhysicalArmor":548,"adjMinMagicArmor":548,"adjMaxMagicArmor":548,"adjAccuracy":17,"adjEvasion":16,"adjFatal":38,"adjAntiFatal":29,"adjIgnoreArmor":0.1173,"adjDmgArmor":0.0573,"adjMortal":0.5025,"adjAntiMortal":0.2991,"adjRealDmg":62,"adjRealDmgDef":62,"adjMonsterDmg":0.4298,"adjMonsterDmgAnti":0.3468,"adjFinalDmg":0.1204,"adjFinalDmgAnti":0.0704,"adjStunEnh":13,"adjStunAnti":13,"adjSilentEnh":13,"adjSilentAnti":13,"adjKnockEnh":13,"adjKnockAnti":13,"adjFrozenEnh":13,"adjFrozenAnti":13,"adjSlowEnh":13,"adjSlowAnti":13,"adjPushEnh":13,"adjPushAnti":13})
    }),
    51000063: _tools.RODict({
        "propID": 51000063,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1119,"adjMinPhysicalAtk":1008,"adjMaxPhysicalAtk":1008,"adjMinMagicAtk":1008,"adjMaxMagicAtk":1008,"adjAtkBless":2,"adjMinPhysicalArmor":562,"adjMaxPhysicalArmor":562,"adjMinMagicArmor":562,"adjMaxMagicArmor":562,"adjAccuracy":17,"adjEvasion":16,"adjFatal":38,"adjAntiFatal":29,"adjIgnoreArmor":0.1182,"adjDmgArmor":0.0582,"adjMortal":0.5103,"adjAntiMortal":0.3072,"adjRealDmg":63,"adjRealDmgDef":63,"adjMonsterDmg":0.4382,"adjMonsterDmgAnti":0.3551,"adjFinalDmg":0.1224,"adjFinalDmgAnti":0.0723,"adjStunEnh":13,"adjStunAnti":13,"adjSilentEnh":13,"adjSilentAnti":13,"adjKnockEnh":13,"adjKnockAnti":13,"adjFrozenEnh":13,"adjFrozenAnti":13,"adjSlowEnh":13,"adjSlowAnti":13,"adjPushEnh":13,"adjPushAnti":13})
    }),
    51000064: _tools.RODict({
        "propID": 51000064,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1135,"adjMinPhysicalAtk":1030,"adjMaxPhysicalAtk":1030,"adjMinMagicAtk":1030,"adjMaxMagicAtk":1030,"adjAtkBless":2,"adjMinPhysicalArmor":575,"adjMaxPhysicalArmor":575,"adjMinMagicArmor":575,"adjMaxMagicArmor":575,"adjAccuracy":17,"adjEvasion":17,"adjFatal":39,"adjAntiFatal":30,"adjIgnoreArmor":0.1191,"adjDmgArmor":0.0591,"adjMortal":0.5181,"adjAntiMortal":0.3153,"adjRealDmg":64,"adjRealDmgDef":64,"adjMonsterDmg":0.4465,"adjMonsterDmgAnti":0.3634,"adjFinalDmg":0.1243,"adjFinalDmgAnti":0.0743,"adjStunEnh":14,"adjStunAnti":14,"adjSilentEnh":14,"adjSilentAnti":14,"adjKnockEnh":14,"adjKnockAnti":14,"adjFrozenEnh":14,"adjFrozenAnti":14,"adjSlowEnh":14,"adjSlowAnti":14,"adjPushEnh":14,"adjPushAnti":14})
    }),
    51000065: _tools.RODict({
        "propID": 51000065,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1151,"adjMinPhysicalAtk":1057,"adjMaxPhysicalAtk":1057,"adjMinMagicAtk":1057,"adjMaxMagicAtk":1057,"adjAtkBless":2,"adjMinPhysicalArmor":589,"adjMaxPhysicalArmor":589,"adjMinMagicArmor":589,"adjMaxMagicArmor":589,"adjAccuracy":18,"adjEvasion":17,"adjFatal":39,"adjAntiFatal":30,"adjIgnoreArmor":0.12,"adjDmgArmor":0.06,"adjMortal":0.5258,"adjAntiMortal":0.3233,"adjRealDmg":65,"adjRealDmgDef":65,"adjMonsterDmg":0.4549,"adjMonsterDmgAnti":0.3717,"adjFinalDmg":0.1263,"adjFinalDmgAnti":0.0762,"adjStunEnh":14,"adjStunAnti":14,"adjSilentEnh":14,"adjSilentAnti":14,"adjKnockEnh":14,"adjKnockAnti":14,"adjFrozenEnh":14,"adjFrozenAnti":14,"adjSlowEnh":14,"adjSlowAnti":14,"adjPushEnh":14,"adjPushAnti":14})
    }),
    51000066: _tools.RODict({
        "propID": 51000066,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1168,"adjMinPhysicalAtk":1080,"adjMaxPhysicalAtk":1080,"adjMinMagicAtk":1080,"adjMaxMagicAtk":1080,"adjAtkBless":2,"adjMinPhysicalArmor":602,"adjMaxPhysicalArmor":602,"adjMinMagicArmor":602,"adjMaxMagicArmor":602,"adjAccuracy":18,"adjEvasion":18,"adjFatal":39,"adjAntiFatal":31,"adjIgnoreArmor":0.1209,"adjDmgArmor":0.0609,"adjMortal":0.5336,"adjAntiMortal":0.3314,"adjRealDmg":66,"adjRealDmgDef":66,"adjMonsterDmg":0.4633,"adjMonsterDmgAnti":0.3799,"adjFinalDmg":0.1282,"adjFinalDmgAnti":0.0782,"adjStunEnh":14,"adjStunAnti":14,"adjSilentEnh":14,"adjSilentAnti":14,"adjKnockEnh":14,"adjKnockAnti":14,"adjFrozenEnh":14,"adjFrozenAnti":14,"adjSlowEnh":14,"adjSlowAnti":14,"adjPushEnh":14,"adjPushAnti":14})
    }),
    51000067: _tools.RODict({
        "propID": 51000067,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1184,"adjMinPhysicalAtk":1102,"adjMaxPhysicalAtk":1102,"adjMinMagicAtk":1102,"adjMaxMagicAtk":1102,"adjAtkBless":2,"adjMinPhysicalArmor":616,"adjMaxPhysicalArmor":616,"adjMinMagicArmor":616,"adjMaxMagicArmor":616,"adjAccuracy":18,"adjEvasion":18,"adjFatal":40,"adjAntiFatal":31,"adjIgnoreArmor":0.1218,"adjDmgArmor":0.0618,"adjMortal":0.5414,"adjAntiMortal":0.3395,"adjRealDmg":67,"adjRealDmgDef":67,"adjMonsterDmg":0.4717,"adjMonsterDmgAnti":0.3882,"adjFinalDmg":0.1302,"adjFinalDmgAnti":0.0801,"adjStunEnh":14,"adjStunAnti":14,"adjSilentEnh":14,"adjSilentAnti":14,"adjKnockEnh":14,"adjKnockAnti":14,"adjFrozenEnh":14,"adjFrozenAnti":14,"adjSlowEnh":14,"adjSlowAnti":14,"adjPushEnh":14,"adjPushAnti":14})
    }),
    51000068: _tools.RODict({
        "propID": 51000068,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1201,"adjMinPhysicalAtk":1125,"adjMaxPhysicalAtk":1125,"adjMinMagicAtk":1125,"adjMaxMagicAtk":1125,"adjAtkBless":2,"adjMinPhysicalArmor":629,"adjMaxPhysicalArmor":629,"adjMinMagicArmor":629,"adjMaxMagicArmor":629,"adjAccuracy":18,"adjEvasion":19,"adjFatal":40,"adjAntiFatal":31,"adjIgnoreArmor":0.1227,"adjDmgArmor":0.0627,"adjMortal":0.5491,"adjAntiMortal":0.3475,"adjRealDmg":68,"adjRealDmgDef":68,"adjMonsterDmg":0.4801,"adjMonsterDmgAnti":0.3965,"adjFinalDmg":0.1321,"adjFinalDmgAnti":0.0821,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15,"adjPushEnh":15,"adjPushAnti":15})
    }),
    51000069: _tools.RODict({
        "propID": 51000069,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1218,"adjMinPhysicalAtk":1148,"adjMaxPhysicalAtk":1148,"adjMinMagicAtk":1148,"adjMaxMagicAtk":1148,"adjAtkBless":2,"adjMinPhysicalArmor":643,"adjMaxPhysicalArmor":643,"adjMinMagicArmor":643,"adjMaxMagicArmor":643,"adjAccuracy":19,"adjEvasion":19,"adjFatal":41,"adjAntiFatal":32,"adjIgnoreArmor":0.1236,"adjDmgArmor":0.0636,"adjMortal":0.5569,"adjAntiMortal":0.3556,"adjRealDmg":69,"adjRealDmgDef":69,"adjMonsterDmg":0.4885,"adjMonsterDmgAnti":0.4048,"adjFinalDmg":0.1341,"adjFinalDmgAnti":0.084,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15,"adjPushEnh":15,"adjPushAnti":15})
    }),
    51000070: _tools.RODict({
        "propID": 51000070,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1235,"adjMinPhysicalAtk":1166,"adjMaxPhysicalAtk":1166,"adjMinMagicAtk":1166,"adjMaxMagicAtk":1166,"adjAtkBless":3,"adjMinPhysicalArmor":656,"adjMaxPhysicalArmor":656,"adjMinMagicArmor":656,"adjMaxMagicArmor":656,"adjAccuracy":19,"adjEvasion":20,"adjFatal":41,"adjAntiFatal":32,"adjIgnoreArmor":0.1245,"adjDmgArmor":0.0645,"adjMortal":0.5647,"adjAntiMortal":0.3637,"adjRealDmg":70,"adjRealDmgDef":70,"adjMonsterDmg":0.4968,"adjMonsterDmgAnti":0.4131,"adjFinalDmg":0.136,"adjFinalDmgAnti":0.086,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15,"adjPushEnh":15,"adjPushAnti":15})
    }),
    51000071: _tools.RODict({
        "propID": 51000071,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1273,"adjMinPhysicalAtk":1181,"adjMaxPhysicalAtk":1181,"adjMinMagicAtk":1181,"adjMaxMagicAtk":1181,"adjAtkBless":3,"adjMinPhysicalArmor":669,"adjMaxPhysicalArmor":669,"adjMinMagicArmor":669,"adjMaxMagicArmor":669,"adjAccuracy":19,"adjEvasion":20,"adjFatal":42,"adjAntiFatal":33,"adjIgnoreArmor":0.132,"adjDmgArmor":0.066,"adjMortal":0.5928,"adjAntiMortal":0.3738,"adjRealDmg":71,"adjRealDmgDef":71,"adjMonsterDmg":0.5143,"adjMonsterDmgAnti":0.4223,"adjFinalDmg":0.1433,"adjFinalDmgAnti":0.0882,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15,"adjPushEnh":15,"adjPushAnti":15})
    }),
    51000072: _tools.RODict({
        "propID": 51000072,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1311,"adjMinPhysicalAtk":1197,"adjMaxPhysicalAtk":1197,"adjMinMagicAtk":1197,"adjMaxMagicAtk":1197,"adjAtkBless":3,"adjMinPhysicalArmor":682,"adjMaxPhysicalArmor":682,"adjMinMagicArmor":682,"adjMaxMagicArmor":682,"adjAccuracy":19,"adjEvasion":21,"adjFatal":43,"adjAntiFatal":33,"adjIgnoreArmor":0.1395,"adjDmgArmor":0.0675,"adjMortal":0.621,"adjAntiMortal":0.384,"adjRealDmg":72,"adjRealDmgDef":72,"adjMonsterDmg":0.5317,"adjMonsterDmgAnti":0.4315,"adjFinalDmg":0.1505,"adjFinalDmgAnti":0.0905,"adjStunEnh":16,"adjStunAnti":16,"adjSilentEnh":16,"adjSilentAnti":16,"adjKnockEnh":16,"adjKnockAnti":16,"adjFrozenEnh":16,"adjFrozenAnti":16,"adjSlowEnh":16,"adjSlowAnti":16,"adjPushEnh":16,"adjPushAnti":16})
    }),
    51000073: _tools.RODict({
        "propID": 51000073,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1351,"adjMinPhysicalAtk":1213,"adjMaxPhysicalAtk":1213,"adjMinMagicAtk":1213,"adjMaxMagicAtk":1213,"adjAtkBless":3,"adjMinPhysicalArmor":695,"adjMaxPhysicalArmor":695,"adjMinMagicArmor":695,"adjMaxMagicArmor":695,"adjAccuracy":20,"adjEvasion":21,"adjFatal":43,"adjAntiFatal":34,"adjIgnoreArmor":0.147,"adjDmgArmor":0.069,"adjMortal":0.6492,"adjAntiMortal":0.3942,"adjRealDmg":73,"adjRealDmgDef":73,"adjMonsterDmg":0.5491,"adjMonsterDmgAnti":0.4407,"adjFinalDmg":0.1578,"adjFinalDmgAnti":0.0927,"adjStunEnh":16,"adjStunAnti":16,"adjSilentEnh":16,"adjSilentAnti":16,"adjKnockEnh":16,"adjKnockAnti":16,"adjFrozenEnh":16,"adjFrozenAnti":16,"adjSlowEnh":16,"adjSlowAnti":16,"adjPushEnh":16,"adjPushAnti":16})
    }),
    51000074: _tools.RODict({
        "propID": 51000074,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1391,"adjMinPhysicalAtk":1229,"adjMaxPhysicalAtk":1229,"adjMinMagicAtk":1229,"adjMaxMagicAtk":1229,"adjAtkBless":3,"adjMinPhysicalArmor":708,"adjMaxPhysicalArmor":708,"adjMinMagicArmor":708,"adjMaxMagicArmor":708,"adjAccuracy":20,"adjEvasion":21,"adjFatal":44,"adjAntiFatal":35,"adjIgnoreArmor":0.1545,"adjDmgArmor":0.0705,"adjMortal":0.6773,"adjAntiMortal":0.4043,"adjRealDmg":74,"adjRealDmgDef":74,"adjMonsterDmg":0.5666,"adjMonsterDmgAnti":0.4499,"adjFinalDmg":0.165,"adjFinalDmgAnti":0.095,"adjStunEnh":16,"adjStunAnti":16,"adjSilentEnh":16,"adjSilentAnti":16,"adjKnockEnh":16,"adjKnockAnti":16,"adjFrozenEnh":16,"adjFrozenAnti":16,"adjSlowEnh":16,"adjSlowAnti":16,"adjPushEnh":16,"adjPushAnti":16})
    }),
    51000075: _tools.RODict({
        "propID": 51000075,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1433,"adjMinPhysicalAtk":1239,"adjMaxPhysicalAtk":1239,"adjMinMagicAtk":1239,"adjMaxMagicAtk":1239,"adjAtkBless":3,"adjMinPhysicalArmor":721,"adjMaxPhysicalArmor":721,"adjMinMagicArmor":721,"adjMaxMagicArmor":721,"adjAccuracy":20,"adjEvasion":21,"adjFatal":44,"adjAntiFatal":35,"adjIgnoreArmor":0.162,"adjDmgArmor":0.072,"adjMortal":0.7055,"adjAntiMortal":0.4145,"adjRealDmg":75,"adjRealDmgDef":75,"adjMonsterDmg":0.584,"adjMonsterDmgAnti":0.4591,"adjFinalDmg":0.1723,"adjFinalDmgAnti":0.0973,"adjStunEnh":16,"adjStunAnti":16,"adjSilentEnh":16,"adjSilentAnti":16,"adjKnockEnh":16,"adjKnockAnti":16,"adjFrozenEnh":16,"adjFrozenAnti":16,"adjSlowEnh":16,"adjSlowAnti":16,"adjPushEnh":16,"adjPushAnti":16})
    }),
    51000076: _tools.RODict({
        "propID": 51000076,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1476,"adjMinPhysicalAtk":1249,"adjMaxPhysicalAtk":1249,"adjMinMagicAtk":1249,"adjMaxMagicAtk":1249,"adjAtkBless":3,"adjMinPhysicalArmor":734,"adjMaxPhysicalArmor":734,"adjMinMagicArmor":734,"adjMaxMagicArmor":734,"adjAccuracy":20,"adjEvasion":22,"adjFatal":45,"adjAntiFatal":36,"adjIgnoreArmor":0.1695,"adjDmgArmor":0.0735,"adjMortal":0.7337,"adjAntiMortal":0.4247,"adjRealDmg":76,"adjRealDmgDef":76,"adjMonsterDmg":0.6014,"adjMonsterDmgAnti":0.4683,"adjFinalDmg":0.1795,"adjFinalDmgAnti":0.0995,"adjStunEnh":17,"adjStunAnti":17,"adjSilentEnh":17,"adjSilentAnti":17,"adjKnockEnh":17,"adjKnockAnti":17,"adjFrozenEnh":17,"adjFrozenAnti":17,"adjSlowEnh":17,"adjSlowAnti":17,"adjPushEnh":17,"adjPushAnti":17})
    }),
    51000077: _tools.RODict({
        "propID": 51000077,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1520,"adjMinPhysicalAtk":1259,"adjMaxPhysicalAtk":1259,"adjMinMagicAtk":1259,"adjMaxMagicAtk":1259,"adjAtkBless":3,"adjMinPhysicalArmor":746,"adjMaxPhysicalArmor":746,"adjMinMagicArmor":746,"adjMaxMagicArmor":746,"adjAccuracy":21,"adjEvasion":22,"adjFatal":46,"adjAntiFatal":36,"adjIgnoreArmor":0.177,"adjDmgArmor":0.075,"adjMortal":0.7618,"adjAntiMortal":0.4348,"adjRealDmg":77,"adjRealDmgDef":77,"adjMonsterDmg":0.6189,"adjMonsterDmgAnti":0.4775,"adjFinalDmg":0.1868,"adjFinalDmgAnti":0.1018,"adjStunEnh":17,"adjStunAnti":17,"adjSilentEnh":17,"adjSilentAnti":17,"adjKnockEnh":17,"adjKnockAnti":17,"adjFrozenEnh":17,"adjFrozenAnti":17,"adjSlowEnh":17,"adjSlowAnti":17,"adjPushEnh":17,"adjPushAnti":17})
    }),
    51000078: _tools.RODict({
        "propID": 51000078,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1566,"adjMinPhysicalAtk":1268,"adjMaxPhysicalAtk":1268,"adjMinMagicAtk":1268,"adjMaxMagicAtk":1268,"adjAtkBless":3,"adjMinPhysicalArmor":759,"adjMaxPhysicalArmor":759,"adjMinMagicArmor":759,"adjMaxMagicArmor":759,"adjAccuracy":21,"adjEvasion":22,"adjFatal":46,"adjAntiFatal":37,"adjIgnoreArmor":0.1845,"adjDmgArmor":0.0765,"adjMortal":0.79,"adjAntiMortal":0.445,"adjRealDmg":78,"adjRealDmgDef":78,"adjMonsterDmg":0.6363,"adjMonsterDmgAnti":0.4868,"adjFinalDmg":0.194,"adjFinalDmgAnti":0.104,"adjStunEnh":17,"adjStunAnti":17,"adjSilentEnh":17,"adjSilentAnti":17,"adjKnockEnh":17,"adjKnockAnti":17,"adjFrozenEnh":17,"adjFrozenAnti":17,"adjSlowEnh":17,"adjSlowAnti":17,"adjPushEnh":17,"adjPushAnti":17})
    }),
    51000079: _tools.RODict({
        "propID": 51000079,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1612,"adjMinPhysicalAtk":1284,"adjMaxPhysicalAtk":1284,"adjMinMagicAtk":1284,"adjMaxMagicAtk":1284,"adjAtkBless":3,"adjMinPhysicalArmor":772,"adjMaxPhysicalArmor":772,"adjMinMagicArmor":772,"adjMaxMagicArmor":772,"adjAccuracy":21,"adjEvasion":22,"adjFatal":47,"adjAntiFatal":37,"adjIgnoreArmor":0.192,"adjDmgArmor":0.078,"adjMortal":0.8182,"adjAntiMortal":0.4552,"adjRealDmg":79,"adjRealDmgDef":79,"adjMonsterDmg":0.6537,"adjMonsterDmgAnti":0.496,"adjFinalDmg":0.2013,"adjFinalDmgAnti":0.1063,"adjStunEnh":17,"adjStunAnti":17,"adjSilentEnh":17,"adjSilentAnti":17,"adjKnockEnh":17,"adjKnockAnti":17,"adjFrozenEnh":17,"adjFrozenAnti":17,"adjSlowEnh":17,"adjSlowAnti":17,"adjPushEnh":17,"adjPushAnti":17})
    }),
    51000080: _tools.RODict({
        "propID": 51000080,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1660,"adjMinPhysicalAtk":1299,"adjMaxPhysicalAtk":1299,"adjMinMagicAtk":1299,"adjMaxMagicAtk":1299,"adjAtkBless":3,"adjMinPhysicalArmor":785,"adjMaxPhysicalArmor":785,"adjMinMagicArmor":785,"adjMaxMagicArmor":785,"adjAccuracy":21,"adjEvasion":23,"adjFatal":47,"adjAntiFatal":38,"adjIgnoreArmor":0.1995,"adjDmgArmor":0.0795,"adjMortal":0.8463,"adjAntiMortal":0.4653,"adjRealDmg":80,"adjRealDmgDef":80,"adjMonsterDmg":0.6712,"adjMonsterDmgAnti":0.5052,"adjFinalDmg":0.2085,"adjFinalDmgAnti":0.1085,"adjStunEnh":18,"adjStunAnti":18,"adjSilentEnh":18,"adjSilentAnti":18,"adjKnockEnh":18,"adjKnockAnti":18,"adjFrozenEnh":18,"adjFrozenAnti":18,"adjSlowEnh":18,"adjSlowAnti":18,"adjPushEnh":18,"adjPushAnti":18})
    }),
    51000081: _tools.RODict({
        "propID": 51000081,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1680,"adjMinPhysicalAtk":1314,"adjMaxPhysicalAtk":1314,"adjMinMagicAtk":1314,"adjMaxMagicAtk":1314,"adjAtkBless":3,"adjMinPhysicalArmor":796,"adjMaxPhysicalArmor":796,"adjMinMagicArmor":796,"adjMaxMagicArmor":796,"adjAccuracy":22,"adjEvasion":23,"adjFatal":48,"adjAntiFatal":38,"adjIgnoreArmor":0.2006,"adjDmgArmor":0.0805,"adjMortal":0.8572,"adjAntiMortal":0.4765,"adjRealDmg":81,"adjRealDmgDef":81,"adjMonsterDmg":0.6802,"adjMonsterDmgAnti":0.5143,"adjFinalDmg":0.2112,"adjFinalDmgAnti":0.1112,"adjStunEnh":18,"adjStunAnti":18,"adjSilentEnh":18,"adjSilentAnti":18,"adjKnockEnh":18,"adjKnockAnti":18,"adjFrozenEnh":18,"adjFrozenAnti":18,"adjSlowEnh":18,"adjSlowAnti":18,"adjPushEnh":18,"adjPushAnti":18})
    }),
    51000082: _tools.RODict({
        "propID": 51000082,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1700,"adjMinPhysicalAtk":1335,"adjMaxPhysicalAtk":1335,"adjMinMagicAtk":1335,"adjMaxMagicAtk":1335,"adjAtkBless":3,"adjMinPhysicalArmor":806,"adjMaxPhysicalArmor":806,"adjMinMagicArmor":806,"adjMaxMagicArmor":806,"adjAccuracy":23,"adjEvasion":23,"adjFatal":48,"adjAntiFatal":39,"adjIgnoreArmor":0.2016,"adjDmgArmor":0.0816,"adjMortal":0.8681,"adjAntiMortal":0.4877,"adjRealDmg":82,"adjRealDmgDef":82,"adjMonsterDmg":0.6892,"adjMonsterDmgAnti":0.5233,"adjFinalDmg":0.214,"adjFinalDmgAnti":0.1139,"adjStunEnh":18,"adjStunAnti":18,"adjSilentEnh":18,"adjSilentAnti":18,"adjKnockEnh":18,"adjKnockAnti":18,"adjFrozenEnh":18,"adjFrozenAnti":18,"adjSlowEnh":18,"adjSlowAnti":18,"adjPushEnh":18,"adjPushAnti":18})
    }),
    51000083: _tools.RODict({
        "propID": 51000083,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1720,"adjMinPhysicalAtk":1349,"adjMaxPhysicalAtk":1349,"adjMinMagicAtk":1349,"adjMaxMagicAtk":1349,"adjAtkBless":3,"adjMinPhysicalArmor":816,"adjMaxPhysicalArmor":816,"adjMinMagicArmor":816,"adjMaxMagicArmor":816,"adjAccuracy":24,"adjEvasion":23,"adjFatal":49,"adjAntiFatal":39,"adjIgnoreArmor":0.2026,"adjDmgArmor":0.0826,"adjMortal":0.8789,"adjAntiMortal":0.4988,"adjRealDmg":83,"adjRealDmgDef":83,"adjMonsterDmg":0.6983,"adjMonsterDmgAnti":0.5324,"adjFinalDmg":0.2167,"adjFinalDmgAnti":0.1167,"adjStunEnh":18,"adjStunAnti":18,"adjSilentEnh":18,"adjSilentAnti":18,"adjKnockEnh":18,"adjKnockAnti":18,"adjFrozenEnh":18,"adjFrozenAnti":18,"adjSlowEnh":18,"adjSlowAnti":18,"adjPushEnh":18,"adjPushAnti":18})
    }),
    51000084: _tools.RODict({
        "propID": 51000084,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1741,"adjMinPhysicalAtk":1377,"adjMaxPhysicalAtk":1377,"adjMinMagicAtk":1377,"adjMaxMagicAtk":1377,"adjAtkBless":3,"adjMinPhysicalArmor":826,"adjMaxPhysicalArmor":826,"adjMinMagicArmor":826,"adjMaxMagicArmor":826,"adjAccuracy":24,"adjEvasion":24,"adjFatal":49,"adjAntiFatal":40,"adjIgnoreArmor":0.2037,"adjDmgArmor":0.0837,"adjMortal":0.8898,"adjAntiMortal":0.51,"adjRealDmg":84,"adjRealDmgDef":84,"adjMonsterDmg":0.7073,"adjMonsterDmgAnti":0.5415,"adjFinalDmg":0.2194,"adjFinalDmgAnti":0.1194,"adjStunEnh":19,"adjStunAnti":19,"adjSilentEnh":19,"adjSilentAnti":19,"adjKnockEnh":19,"adjKnockAnti":19,"adjFrozenEnh":19,"adjFrozenAnti":19,"adjSlowEnh":19,"adjSlowAnti":19,"adjPushEnh":19,"adjPushAnti":19})
    }),
    51000085: _tools.RODict({
        "propID": 51000085,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1761,"adjMinPhysicalAtk":1391,"adjMaxPhysicalAtk":1391,"adjMinMagicAtk":1391,"adjMaxMagicAtk":1391,"adjAtkBless":3,"adjMinPhysicalArmor":837,"adjMaxPhysicalArmor":837,"adjMinMagicArmor":837,"adjMaxMagicArmor":837,"adjAccuracy":25,"adjEvasion":24,"adjFatal":50,"adjAntiFatal":40,"adjIgnoreArmor":0.2047,"adjDmgArmor":0.0847,"adjMortal":0.9007,"adjAntiMortal":0.5212,"adjRealDmg":85,"adjRealDmgDef":85,"adjMonsterDmg":0.7163,"adjMonsterDmgAnti":0.5506,"adjFinalDmg":0.2221,"adjFinalDmgAnti":0.1221,"adjStunEnh":19,"adjStunAnti":19,"adjSilentEnh":19,"adjSilentAnti":19,"adjKnockEnh":19,"adjKnockAnti":19,"adjFrozenEnh":19,"adjFrozenAnti":19,"adjSlowEnh":19,"adjSlowAnti":19,"adjPushEnh":19,"adjPushAnti":19})
    }),
    51000086: _tools.RODict({
        "propID": 51000086,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1781,"adjMinPhysicalAtk":1413,"adjMaxPhysicalAtk":1413,"adjMinMagicAtk":1413,"adjMaxMagicAtk":1413,"adjAtkBless":3,"adjMinPhysicalArmor":847,"adjMaxPhysicalArmor":847,"adjMinMagicArmor":847,"adjMaxMagicArmor":847,"adjAccuracy":26,"adjEvasion":24,"adjFatal":50,"adjAntiFatal":41,"adjIgnoreArmor":0.2058,"adjDmgArmor":0.0858,"adjMortal":0.9115,"adjAntiMortal":0.5323,"adjRealDmg":86,"adjRealDmgDef":86,"adjMonsterDmg":0.7254,"adjMonsterDmgAnti":0.5597,"adjFinalDmg":0.2249,"adjFinalDmgAnti":0.1249,"adjStunEnh":19,"adjStunAnti":19,"adjSilentEnh":19,"adjSilentAnti":19,"adjKnockEnh":19,"adjKnockAnti":19,"adjFrozenEnh":19,"adjFrozenAnti":19,"adjSlowEnh":19,"adjSlowAnti":19,"adjPushEnh":19,"adjPushAnti":19})
    }),
    51000087: _tools.RODict({
        "propID": 51000087,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1802,"adjMinPhysicalAtk":1434,"adjMaxPhysicalAtk":1434,"adjMinMagicAtk":1434,"adjMaxMagicAtk":1434,"adjAtkBless":3,"adjMinPhysicalArmor":857,"adjMaxPhysicalArmor":857,"adjMinMagicArmor":857,"adjMaxMagicArmor":857,"adjAccuracy":27,"adjEvasion":24,"adjFatal":51,"adjAntiFatal":41,"adjIgnoreArmor":0.2068,"adjDmgArmor":0.0868,"adjMortal":0.9224,"adjAntiMortal":0.5435,"adjRealDmg":87,"adjRealDmgDef":87,"adjMonsterDmg":0.7344,"adjMonsterDmgAnti":0.5688,"adjFinalDmg":0.2276,"adjFinalDmgAnti":0.1276,"adjStunEnh":19,"adjStunAnti":19,"adjSilentEnh":19,"adjSilentAnti":19,"adjKnockEnh":19,"adjKnockAnti":19,"adjFrozenEnh":19,"adjFrozenAnti":19,"adjSlowEnh":19,"adjSlowAnti":19,"adjPushEnh":19,"adjPushAnti":19})
    }),
    51000088: _tools.RODict({
        "propID": 51000088,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1823,"adjMinPhysicalAtk":1456,"adjMaxPhysicalAtk":1456,"adjMinMagicAtk":1456,"adjMaxMagicAtk":1456,"adjAtkBless":3,"adjMinPhysicalArmor":868,"adjMaxPhysicalArmor":868,"adjMinMagicArmor":868,"adjMaxMagicArmor":868,"adjAccuracy":27,"adjEvasion":25,"adjFatal":51,"adjAntiFatal":42,"adjIgnoreArmor":0.2079,"adjDmgArmor":0.0879,"adjMortal":0.9333,"adjAntiMortal":0.5547,"adjRealDmg":88,"adjRealDmgDef":88,"adjMonsterDmg":0.7434,"adjMonsterDmgAnti":0.5778,"adjFinalDmg":0.2303,"adjFinalDmgAnti":0.1303,"adjStunEnh":20,"adjStunAnti":20,"adjSilentEnh":20,"adjSilentAnti":20,"adjKnockEnh":20,"adjKnockAnti":20,"adjFrozenEnh":20,"adjFrozenAnti":20,"adjSlowEnh":20,"adjSlowAnti":20,"adjPushEnh":20,"adjPushAnti":20})
    }),
    51000089: _tools.RODict({
        "propID": 51000089,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1843,"adjMinPhysicalAtk":1477,"adjMaxPhysicalAtk":1477,"adjMinMagicAtk":1477,"adjMaxMagicAtk":1477,"adjAtkBless":3,"adjMinPhysicalArmor":878,"adjMaxPhysicalArmor":878,"adjMinMagicArmor":878,"adjMaxMagicArmor":878,"adjAccuracy":28,"adjEvasion":25,"adjFatal":52,"adjAntiFatal":42,"adjIgnoreArmor":0.2089,"adjDmgArmor":0.0889,"adjMortal":0.9441,"adjAntiMortal":0.5658,"adjRealDmg":89,"adjRealDmgDef":89,"adjMonsterDmg":0.7525,"adjMonsterDmgAnti":0.5869,"adjFinalDmg":0.233,"adjFinalDmgAnti":0.133,"adjStunEnh":20,"adjStunAnti":20,"adjSilentEnh":20,"adjSilentAnti":20,"adjKnockEnh":20,"adjKnockAnti":20,"adjFrozenEnh":20,"adjFrozenAnti":20,"adjSlowEnh":20,"adjSlowAnti":20,"adjPushEnh":20,"adjPushAnti":20})
    }),
    51000090: _tools.RODict({
        "propID": 51000090,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1864,"adjMinPhysicalAtk":1499,"adjMaxPhysicalAtk":1499,"adjMinMagicAtk":1499,"adjMaxMagicAtk":1499,"adjAtkBless":3,"adjMinPhysicalArmor":888,"adjMaxPhysicalArmor":888,"adjMinMagicArmor":888,"adjMaxMagicArmor":888,"adjAccuracy":29,"adjEvasion":25,"adjFatal":52,"adjAntiFatal":43,"adjIgnoreArmor":0.21,"adjDmgArmor":0.09,"adjMortal":0.955,"adjAntiMortal":0.577,"adjRealDmg":90,"adjRealDmgDef":90,"adjMonsterDmg":0.7615,"adjMonsterDmgAnti":0.596,"adjFinalDmg":0.2358,"adjFinalDmgAnti":0.1357,"adjStunEnh":20,"adjStunAnti":20,"adjSilentEnh":20,"adjSilentAnti":20,"adjKnockEnh":20,"adjKnockAnti":20,"adjFrozenEnh":20,"adjFrozenAnti":20,"adjSlowEnh":20,"adjSlowAnti":20,"adjPushEnh":20,"adjPushAnti":20})
    }),
    52004001: _tools.RODict({
        "propID": 52004001,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2400000,"adjMinPhysicalArmor":300,"adjMaxPhysicalArmor":300,"adjMinMagicArmor":300,"adjMaxMagicArmor":300})
    }),
    52004002: _tools.RODict({
        "propID": 52004002,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3000000,"adjMinPhysicalArmor":400,"adjMaxPhysicalArmor":400,"adjMinMagicArmor":400,"adjMaxMagicArmor":400})
    }),
    52004003: _tools.RODict({
        "propID": 52004003,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4000000,"adjMinPhysicalArmor":500,"adjMaxPhysicalArmor":500,"adjMinMagicArmor":500,"adjMaxMagicArmor":500})
    }),
    52004004: _tools.RODict({
        "propID": 52004004,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5000000,"adjMinPhysicalArmor":700,"adjMaxPhysicalArmor":700,"adjMinMagicArmor":700,"adjMaxMagicArmor":700})
    }),
    52004005: _tools.RODict({
        "propID": 52004005,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":7000000,"adjMinPhysicalArmor":900,"adjMaxPhysicalArmor":900,"adjMinMagicArmor":900,"adjMaxMagicArmor":900})
    }),
    52004006: _tools.RODict({
        "propID": 52004006,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1200000,"adjMinPhysicalArmor":300,"adjMaxPhysicalArmor":300,"adjMinMagicArmor":300,"adjMaxMagicArmor":300})
    }),
    52004007: _tools.RODict({
        "propID": 52004007,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1500000,"adjMinPhysicalArmor":400,"adjMaxPhysicalArmor":400,"adjMinMagicArmor":400,"adjMaxMagicArmor":400})
    }),
    52004008: _tools.RODict({
        "propID": 52004008,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2000000,"adjMinPhysicalArmor":500,"adjMaxPhysicalArmor":500,"adjMinMagicArmor":500,"adjMaxMagicArmor":500})
    }),
    52004009: _tools.RODict({
        "propID": 52004009,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2500000,"adjMinPhysicalArmor":700,"adjMaxPhysicalArmor":700,"adjMinMagicArmor":700,"adjMaxMagicArmor":700})
    }),
    52004010: _tools.RODict({
        "propID": 52004010,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3500000,"adjMinPhysicalArmor":900,"adjMaxPhysicalArmor":900,"adjMinMagicArmor":900,"adjMaxMagicArmor":900})
    }),
    52004011: _tools.RODict({
        "propID": 52004011,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":600000,"adjMinPhysicalArmor":300,"adjMaxPhysicalArmor":300,"adjMinMagicArmor":300,"adjMaxMagicArmor":300})
    }),
    52004012: _tools.RODict({
        "propID": 52004012,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":750000,"adjMinPhysicalArmor":400,"adjMaxPhysicalArmor":400,"adjMinMagicArmor":400,"adjMaxMagicArmor":400})
    }),
    52004013: _tools.RODict({
        "propID": 52004013,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1000000,"adjMinPhysicalArmor":500,"adjMaxPhysicalArmor":500,"adjMinMagicArmor":500,"adjMaxMagicArmor":500})
    }),
    52004014: _tools.RODict({
        "propID": 52004014,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1250000,"adjMinPhysicalArmor":700,"adjMaxPhysicalArmor":700,"adjMinMagicArmor":700,"adjMaxMagicArmor":700})
    }),
    52004015: _tools.RODict({
        "propID": 52004015,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1750000,"adjMinPhysicalArmor":900,"adjMaxPhysicalArmor":900,"adjMinMagicArmor":900,"adjMaxMagicArmor":900})
    }),
    52004016: _tools.RODict({
        "propID": 52004016,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":300000,"adjMinPhysicalAtk":1000,"adjMaxPhysicalAtk":1000,"adjMinMagicAtk":1000,"adjMaxMagicAtk":1000,"adjMinPhysicalArmor":300,"adjMaxPhysicalArmor":300,"adjMinMagicArmor":300,"adjMaxMagicArmor":300})
    }),
    52004017: _tools.RODict({
        "propID": 52004017,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":375000,"adjMinPhysicalAtk":1500,"adjMaxPhysicalAtk":1500,"adjMinMagicAtk":1500,"adjMaxMagicAtk":1500,"adjMinPhysicalArmor":400,"adjMaxPhysicalArmor":400,"adjMinMagicArmor":400,"adjMaxMagicArmor":400})
    }),
    52004018: _tools.RODict({
        "propID": 52004018,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":500000,"adjMinPhysicalAtk":2000,"adjMaxPhysicalAtk":2000,"adjMinMagicAtk":2000,"adjMaxMagicAtk":2000,"adjMinPhysicalArmor":500,"adjMaxPhysicalArmor":500,"adjMinMagicArmor":500,"adjMaxMagicArmor":500})
    }),
    52004019: _tools.RODict({
        "propID": 52004019,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":625000,"adjMinPhysicalAtk":2500,"adjMaxPhysicalAtk":2500,"adjMinMagicAtk":2500,"adjMaxMagicAtk":2500,"adjMinPhysicalArmor":700,"adjMaxPhysicalArmor":700,"adjMinMagicArmor":700,"adjMaxMagicArmor":700})
    }),
    52004020: _tools.RODict({
        "propID": 52004020,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":875000,"adjMinPhysicalAtk":3000,"adjMaxPhysicalAtk":3000,"adjMinMagicAtk":3000,"adjMaxMagicAtk":3000,"adjMinPhysicalArmor":900,"adjMaxPhysicalArmor":900,"adjMinMagicArmor":900,"adjMaxMagicArmor":900})
    }),
    52004021: _tools.RODict({
        "propID": 52004021,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1200000,"adjMinPhysicalArmor":300,"adjMaxPhysicalArmor":300,"adjMinMagicArmor":300,"adjMaxMagicArmor":300})
    }),
    52004022: _tools.RODict({
        "propID": 52004022,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1500000,"adjMinPhysicalArmor":400,"adjMaxPhysicalArmor":400,"adjMinMagicArmor":400,"adjMaxMagicArmor":400})
    }),
    52004023: _tools.RODict({
        "propID": 52004023,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2000000,"adjMinPhysicalArmor":500,"adjMaxPhysicalArmor":500,"adjMinMagicArmor":500,"adjMaxMagicArmor":500})
    }),
    52004024: _tools.RODict({
        "propID": 52004024,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2500000,"adjMinPhysicalArmor":700,"adjMaxPhysicalArmor":700,"adjMinMagicArmor":700,"adjMaxMagicArmor":700})
    }),
    52004025: _tools.RODict({
        "propID": 52004025,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3500000,"adjMinPhysicalArmor":900,"adjMaxPhysicalArmor":900,"adjMinMagicArmor":900,"adjMaxMagicArmor":900})
    }),
    52004026: _tools.RODict({
        "propID": 52004026,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1200000,"adjMinPhysicalArmor":300,"adjMaxPhysicalArmor":300,"adjMinMagicArmor":300,"adjMaxMagicArmor":300})
    }),
    52004027: _tools.RODict({
        "propID": 52004027,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1500000,"adjMinPhysicalArmor":400,"adjMaxPhysicalArmor":400,"adjMinMagicArmor":400,"adjMaxMagicArmor":400})
    }),
    52004028: _tools.RODict({
        "propID": 52004028,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2000000,"adjMinPhysicalArmor":500,"adjMaxPhysicalArmor":500,"adjMinMagicArmor":500,"adjMaxMagicArmor":500})
    }),
    52004029: _tools.RODict({
        "propID": 52004029,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2500000,"adjMinPhysicalArmor":700,"adjMaxPhysicalArmor":700,"adjMinMagicArmor":700,"adjMaxMagicArmor":700})
    }),
    52004030: _tools.RODict({
        "propID": 52004030,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3500000,"adjMinPhysicalArmor":900,"adjMaxPhysicalArmor":900,"adjMinMagicArmor":900,"adjMaxMagicArmor":900})
    }),
    52004031: _tools.RODict({
        "propID": 52004031,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1200000,"adjMinPhysicalArmor":300,"adjMaxPhysicalArmor":300,"adjMinMagicArmor":300,"adjMaxMagicArmor":300})
    }),
    52004032: _tools.RODict({
        "propID": 52004032,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1500000,"adjMinPhysicalArmor":400,"adjMaxPhysicalArmor":400,"adjMinMagicArmor":400,"adjMaxMagicArmor":400})
    }),
    52004033: _tools.RODict({
        "propID": 52004033,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2000000,"adjMinPhysicalArmor":500,"adjMaxPhysicalArmor":500,"adjMinMagicArmor":500,"adjMaxMagicArmor":500})
    }),
    52004034: _tools.RODict({
        "propID": 52004034,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2500000,"adjMinPhysicalArmor":700,"adjMaxPhysicalArmor":700,"adjMinMagicArmor":700,"adjMaxMagicArmor":700})
    }),
    52004035: _tools.RODict({
        "propID": 52004035,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3500000,"adjMinPhysicalArmor":900,"adjMaxPhysicalArmor":900,"adjMinMagicArmor":900,"adjMaxMagicArmor":900})
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
        "propList": _tools.RODict({"adjMinMagicAtk":49,"adjMaxMagicAtk":132})
    }),
    52012151: _tools.RODict({
        "propID": 52012151,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":54,"adjMaxMagicAtk":145})
    }),
    52012152: _tools.RODict({
        "propID": 52012152,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":59,"adjMaxMagicAtk":158})
    }),
    52012153: _tools.RODict({
        "propID": 52012153,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":64,"adjMaxMagicAtk":172})
    }),
    52012154: _tools.RODict({
        "propID": 52012154,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":70,"adjMaxMagicAtk":189,"adjHit":10,"adjFinalDmg":0.03})
    }),
    52012155: _tools.RODict({
        "propID": 52012155,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":77,"adjMaxMagicAtk":208,"adjHit":11,"adjFinalDmg":0.03})
    }),
    52012156: _tools.RODict({
        "propID": 52012156,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":84,"adjMaxMagicAtk":227,"adjHit":12,"adjFinalDmg":0.03})
    }),
    52012157: _tools.RODict({
        "propID": 52012157,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":91,"adjMaxMagicAtk":246,"adjHit":13,"adjFinalDmg":0.03})
    }),
    52012158: _tools.RODict({
        "propID": 52012158,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":100,"adjMaxMagicAtk":271,"adjHit":15,"adjFinalDmg":0.06})
    }),
    52012159: _tools.RODict({
        "propID": 52012159,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":110,"adjMaxMagicAtk":298,"adjHit":16,"adjFinalDmg":0.06})
    }),
    52012160: _tools.RODict({
        "propID": 52012160,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":120,"adjMaxMagicAtk":325,"adjHit":17,"adjFinalDmg":0.06})
    }),
    52012161: _tools.RODict({
        "propID": 52012161,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":130,"adjMaxMagicAtk":352,"adjHit":19,"adjFinalDmg":0.06})
    }),
    52012162: _tools.RODict({
        "propID": 52012162,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":143,"adjMaxMagicAtk":387,"adjHit":22,"adjFinalDmg":0.06,"adjFinalDmgAnti":0.06})
    }),
    52012163: _tools.RODict({
        "propID": 52012163,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":157,"adjMaxMagicAtk":426,"adjHit":24,"adjFinalDmg":0.06,"adjFinalDmgAnti":0.06})
    }),
    52012164: _tools.RODict({
        "propID": 52012164,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":173,"adjMaxMagicAtk":469,"adjHit":26,"adjFinalDmg":0.06,"adjFinalDmgAnti":0.06})
    }),
    52012165: _tools.RODict({
        "propID": 52012165,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":190,"adjMaxMagicAtk":516,"adjHit":28,"adjFinalDmg":0.06,"adjFinalDmgAnti":0.06})
    }),
    52012326: _tools.RODict({
        "propID": 52012326,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":49,"adjMaxMagicAtk":132})
    }),
    52012327: _tools.RODict({
        "propID": 52012327,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":54,"adjMaxMagicAtk":145})
    }),
    52012328: _tools.RODict({
        "propID": 52012328,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":59,"adjMaxMagicAtk":158})
    }),
    52012329: _tools.RODict({
        "propID": 52012329,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":64,"adjMaxMagicAtk":172})
    }),
    52012330: _tools.RODict({
        "propID": 52012330,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":70,"adjMaxMagicAtk":189,"adjHit":10,"adjFinalDmg":0.03})
    }),
    52012331: _tools.RODict({
        "propID": 52012331,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":77,"adjMaxMagicAtk":208,"adjHit":11,"adjFinalDmg":0.03})
    }),
    52012332: _tools.RODict({
        "propID": 52012332,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":84,"adjMaxMagicAtk":227,"adjHit":12,"adjFinalDmg":0.03})
    }),
    52012333: _tools.RODict({
        "propID": 52012333,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":91,"adjMaxMagicAtk":246,"adjHit":13,"adjFinalDmg":0.03})
    }),
    52012334: _tools.RODict({
        "propID": 52012334,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":100,"adjMaxMagicAtk":271,"adjHit":15,"adjFinalDmg":0.06})
    }),
    52012335: _tools.RODict({
        "propID": 52012335,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":110,"adjMaxMagicAtk":298,"adjHit":16,"adjFinalDmg":0.06})
    }),
    52012336: _tools.RODict({
        "propID": 52012336,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":120,"adjMaxMagicAtk":325,"adjHit":17,"adjFinalDmg":0.06})
    }),
    52012337: _tools.RODict({
        "propID": 52012337,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":130,"adjMaxMagicAtk":352,"adjHit":19,"adjFinalDmg":0.06})
    }),
    52012338: _tools.RODict({
        "propID": 52012338,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":143,"adjMaxMagicAtk":387,"adjHit":22,"adjFinalDmg":0.06,"adjFinalDmgAnti":0.06})
    }),
    52012339: _tools.RODict({
        "propID": 52012339,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":157,"adjMaxMagicAtk":426,"adjHit":24,"adjFinalDmg":0.06,"adjFinalDmgAnti":0.06})
    }),
    52012340: _tools.RODict({
        "propID": 52012340,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":173,"adjMaxMagicAtk":469,"adjHit":26,"adjFinalDmg":0.06,"adjFinalDmgAnti":0.06})
    }),
    52012341: _tools.RODict({
        "propID": 52012341,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":190,"adjMaxMagicAtk":516,"adjHit":28,"adjFinalDmg":0.06,"adjFinalDmgAnti":0.06})
    }),
    52012502: _tools.RODict({
        "propID": 52012502,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":49,"adjMaxPhysicalAtk":132})
    }),
    52012503: _tools.RODict({
        "propID": 52012503,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":54,"adjMaxPhysicalAtk":145})
    }),
    52012504: _tools.RODict({
        "propID": 52012504,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":59,"adjMaxPhysicalAtk":158})
    }),
    52012505: _tools.RODict({
        "propID": 52012505,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":64,"adjMaxPhysicalAtk":172})
    }),
    52012506: _tools.RODict({
        "propID": 52012506,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":70,"adjMaxPhysicalAtk":189,"adjHit":10,"adjFinalDmg":0.03})
    }),
    52012507: _tools.RODict({
        "propID": 52012507,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":77,"adjMaxPhysicalAtk":208,"adjHit":11,"adjFinalDmg":0.03})
    }),
    52012508: _tools.RODict({
        "propID": 52012508,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":84,"adjMaxPhysicalAtk":227,"adjHit":12,"adjFinalDmg":0.03})
    }),
    52012509: _tools.RODict({
        "propID": 52012509,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":91,"adjMaxPhysicalAtk":246,"adjHit":13,"adjFinalDmg":0.03})
    }),
    52012510: _tools.RODict({
        "propID": 52012510,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":100,"adjMaxPhysicalAtk":271,"adjHit":15,"adjFinalDmg":0.06})
    }),
    52012511: _tools.RODict({
        "propID": 52012511,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":110,"adjMaxPhysicalAtk":298,"adjHit":16,"adjFinalDmg":0.06})
    }),
    52012512: _tools.RODict({
        "propID": 52012512,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":120,"adjMaxPhysicalAtk":325,"adjHit":17,"adjFinalDmg":0.06})
    }),
    52012513: _tools.RODict({
        "propID": 52012513,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":130,"adjMaxPhysicalAtk":352,"adjHit":19,"adjFinalDmg":0.06})
    }),
    52012514: _tools.RODict({
        "propID": 52012514,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":143,"adjMaxPhysicalAtk":387,"adjHit":22,"adjFinalDmg":0.06,"adjFinalDmgAnti":0.06})
    }),
    52012515: _tools.RODict({
        "propID": 52012515,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":157,"adjMaxPhysicalAtk":426,"adjHit":24,"adjFinalDmg":0.06,"adjFinalDmgAnti":0.06})
    }),
    52012516: _tools.RODict({
        "propID": 52012516,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":173,"adjMaxPhysicalAtk":469,"adjHit":26,"adjFinalDmg":0.06,"adjFinalDmgAnti":0.06})
    }),
    52012517: _tools.RODict({
        "propID": 52012517,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":190,"adjMaxPhysicalAtk":516,"adjHit":28,"adjFinalDmg":0.06,"adjFinalDmgAnti":0.06})
    }),
    52012678: _tools.RODict({
        "propID": 52012678,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":66,"adjMaxPhysicalArmor":95,"adjMinMagicArmor":66,"adjMaxMagicArmor":95})
    }),
    52012679: _tools.RODict({
        "propID": 52012679,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":73,"adjMaxPhysicalArmor":105,"adjMinMagicArmor":73,"adjMaxMagicArmor":105})
    }),
    52012680: _tools.RODict({
        "propID": 52012680,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":79,"adjMaxPhysicalArmor":114,"adjMinMagicArmor":79,"adjMaxMagicArmor":114})
    }),
    52012681: _tools.RODict({
        "propID": 52012681,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":86,"adjMaxPhysicalArmor":124,"adjMinMagicArmor":86,"adjMaxMagicArmor":124})
    }),
    52012682: _tools.RODict({
        "propID": 52012682,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":95,"adjMaxPhysicalArmor":136,"adjMinMagicArmor":95,"adjMaxMagicArmor":136,"adjMortal":0.1})
    }),
    52012683: _tools.RODict({
        "propID": 52012683,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":105,"adjMaxPhysicalArmor":150,"adjMinMagicArmor":105,"adjMaxMagicArmor":150,"adjMortal":0.1})
    }),
    52012684: _tools.RODict({
        "propID": 52012684,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":114,"adjMaxPhysicalArmor":163,"adjMinMagicArmor":114,"adjMaxMagicArmor":163,"adjMortal":0.1})
    }),
    52012685: _tools.RODict({
        "propID": 52012685,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":124,"adjMaxPhysicalArmor":177,"adjMinMagicArmor":124,"adjMaxMagicArmor":177,"adjMortal":0.1})
    }),
    52012686: _tools.RODict({
        "propID": 52012686,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":136,"adjMaxPhysicalArmor":195,"adjMinMagicArmor":136,"adjMaxMagicArmor":195,"adjMortal":0.2})
    }),
    52012687: _tools.RODict({
        "propID": 52012687,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":150,"adjMaxPhysicalArmor":215,"adjMinMagicArmor":150,"adjMaxMagicArmor":215,"adjMortal":0.2})
    }),
    52012688: _tools.RODict({
        "propID": 52012688,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":163,"adjMaxPhysicalArmor":234,"adjMinMagicArmor":163,"adjMaxMagicArmor":234,"adjMortal":0.2})
    }),
    52012689: _tools.RODict({
        "propID": 52012689,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":177,"adjMaxPhysicalArmor":254,"adjMinMagicArmor":177,"adjMaxMagicArmor":254,"adjMortal":0.2})
    }),
    52012690: _tools.RODict({
        "propID": 52012690,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":195,"adjMaxPhysicalArmor":279,"adjMinMagicArmor":195,"adjMaxMagicArmor":279,"adjMortal":0.2,"adjAntiMortal":0.2})
    }),
    52012691: _tools.RODict({
        "propID": 52012691,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":215,"adjMaxPhysicalArmor":307,"adjMinMagicArmor":215,"adjMaxMagicArmor":307,"adjMortal":0.2,"adjAntiMortal":0.2})
    }),
    52012692: _tools.RODict({
        "propID": 52012692,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":237,"adjMaxPhysicalArmor":338,"adjMinMagicArmor":237,"adjMaxMagicArmor":338,"adjMortal":0.2,"adjAntiMortal":0.2})
    }),
    52012693: _tools.RODict({
        "propID": 52012693,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":261,"adjMaxPhysicalArmor":372,"adjMinMagicArmor":261,"adjMaxMagicArmor":372,"adjMortal":0.2,"adjAntiMortal":0.2})
    }),
    52012854: _tools.RODict({
        "propID": 52012854,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":25,"adjMaxMagicArmor":35})
    }),
    52012855: _tools.RODict({
        "propID": 52012855,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":28,"adjMaxMagicArmor":39})
    }),
    52012856: _tools.RODict({
        "propID": 52012856,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":30,"adjMaxMagicArmor":42})
    }),
    52012857: _tools.RODict({
        "propID": 52012857,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":33,"adjMaxMagicArmor":46})
    }),
    52012858: _tools.RODict({
        "propID": 52012858,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":36,"adjMaxMagicArmor":51,"adjAntiFatal":10,"adjMortal":0.08})
    }),
    52012859: _tools.RODict({
        "propID": 52012859,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":40,"adjMaxMagicArmor":56,"adjAntiFatal":11,"adjMortal":0.08})
    }),
    52012860: _tools.RODict({
        "propID": 52012860,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":43,"adjMaxMagicArmor":61,"adjAntiFatal":12,"adjMortal":0.08})
    }),
    52012861: _tools.RODict({
        "propID": 52012861,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":47,"adjMaxMagicArmor":66,"adjAntiFatal":13,"adjMortal":0.08})
    }),
    52012862: _tools.RODict({
        "propID": 52012862,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":52,"adjMaxMagicArmor":73,"adjAntiFatal":15,"adjMortal":0.16})
    }),
    52012863: _tools.RODict({
        "propID": 52012863,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":57,"adjMaxMagicArmor":80,"adjAntiFatal":16,"adjMortal":0.16})
    }),
    52012864: _tools.RODict({
        "propID": 52012864,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":62,"adjMaxMagicArmor":88,"adjAntiFatal":17,"adjMortal":0.16})
    }),
    52012865: _tools.RODict({
        "propID": 52012865,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":68,"adjMaxMagicArmor":95,"adjAntiFatal":19,"adjMortal":0.16})
    }),
    52012866: _tools.RODict({
        "propID": 52012866,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":75,"adjMaxMagicArmor":105,"adjAntiFatal":22,"adjMortal":0.16,"adjAntiMortal":0.16})
    }),
    52012867: _tools.RODict({
        "propID": 52012867,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":83,"adjMaxMagicArmor":116,"adjAntiFatal":24,"adjMortal":0.16,"adjAntiMortal":0.16})
    }),
    52012868: _tools.RODict({
        "propID": 52012868,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":91,"adjMaxMagicArmor":128,"adjAntiFatal":26,"adjMortal":0.16,"adjAntiMortal":0.16})
    }),
    52012869: _tools.RODict({
        "propID": 52012869,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":100,"adjMaxMagicArmor":141,"adjAntiFatal":28,"adjMortal":0.16,"adjAntiMortal":0.16})
    }),
    52013030: _tools.RODict({
        "propID": 52013030,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":25,"adjMaxPhysicalArmor":35})
    }),
    52013031: _tools.RODict({
        "propID": 52013031,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":28,"adjMaxPhysicalArmor":39})
    }),
    52013032: _tools.RODict({
        "propID": 52013032,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":30,"adjMaxPhysicalArmor":42})
    }),
    52013033: _tools.RODict({
        "propID": 52013033,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":33,"adjMaxPhysicalArmor":46})
    }),
    52013034: _tools.RODict({
        "propID": 52013034,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":36,"adjMaxPhysicalArmor":51,"adjDodge":10,"adjPVPDmg":0.04})
    }),
    52013035: _tools.RODict({
        "propID": 52013035,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":40,"adjMaxPhysicalArmor":56,"adjDodge":11,"adjPVPDmg":0.04})
    }),
    52013036: _tools.RODict({
        "propID": 52013036,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":43,"adjMaxPhysicalArmor":61,"adjDodge":12,"adjPVPDmg":0.04})
    }),
    52013037: _tools.RODict({
        "propID": 52013037,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":47,"adjMaxPhysicalArmor":66,"adjDodge":13,"adjPVPDmg":0.04})
    }),
    52013038: _tools.RODict({
        "propID": 52013038,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":52,"adjMaxPhysicalArmor":73,"adjDodge":15,"adjPVPDmg":0.08})
    }),
    52013039: _tools.RODict({
        "propID": 52013039,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":57,"adjMaxPhysicalArmor":80,"adjDodge":16,"adjPVPDmg":0.08})
    }),
    52013040: _tools.RODict({
        "propID": 52013040,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":62,"adjMaxPhysicalArmor":88,"adjDodge":17,"adjPVPDmg":0.08})
    }),
    52013041: _tools.RODict({
        "propID": 52013041,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":68,"adjMaxPhysicalArmor":95,"adjDodge":19,"adjPVPDmg":0.08})
    }),
    52013042: _tools.RODict({
        "propID": 52013042,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":75,"adjMaxPhysicalArmor":105,"adjDodge":22,"adjPVPDmg":0.08,"adjPVPDmgAnti":0.08})
    }),
    52013043: _tools.RODict({
        "propID": 52013043,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":83,"adjMaxPhysicalArmor":116,"adjDodge":24,"adjPVPDmg":0.08,"adjPVPDmgAnti":0.08})
    }),
    52013044: _tools.RODict({
        "propID": 52013044,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":91,"adjMaxPhysicalArmor":128,"adjDodge":26,"adjPVPDmg":0.08,"adjPVPDmgAnti":0.08})
    }),
    52013045: _tools.RODict({
        "propID": 52013045,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":100,"adjMaxPhysicalArmor":141,"adjDodge":28,"adjPVPDmg":0.08,"adjPVPDmgAnti":0.08})
    }),
    52013206: _tools.RODict({
        "propID": 52013206,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":50})
    }),
    52013207: _tools.RODict({
        "propID": 52013207,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":55})
    }),
    52013208: _tools.RODict({
        "propID": 52013208,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":60})
    }),
    52013209: _tools.RODict({
        "propID": 52013209,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":65})
    }),
    52013210: _tools.RODict({
        "propID": 52013210,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":29,"adjMaxPhysicalAtk":72,"adjFatal":10,"adjIgnoreArmor":0.02})
    }),
    52013211: _tools.RODict({
        "propID": 52013211,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":79,"adjFatal":11,"adjIgnoreArmor":0.02})
    }),
    52013212: _tools.RODict({
        "propID": 52013212,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":35,"adjMaxPhysicalAtk":86,"adjFatal":12,"adjIgnoreArmor":0.02})
    }),
    52013213: _tools.RODict({
        "propID": 52013213,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":38,"adjMaxPhysicalAtk":94,"adjFatal":13,"adjIgnoreArmor":0.02})
    }),
    52013214: _tools.RODict({
        "propID": 52013214,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":42,"adjMaxPhysicalAtk":103,"adjFatal":15,"adjIgnoreArmor":0.04})
    }),
    52013215: _tools.RODict({
        "propID": 52013215,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":46,"adjMaxPhysicalAtk":113,"adjFatal":16,"adjIgnoreArmor":0.04})
    }),
    52013216: _tools.RODict({
        "propID": 52013216,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":50,"adjMaxPhysicalAtk":124,"adjFatal":17,"adjIgnoreArmor":0.04})
    }),
    52013217: _tools.RODict({
        "propID": 52013217,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":55,"adjMaxPhysicalAtk":134,"adjFatal":19,"adjIgnoreArmor":0.04})
    }),
    52013218: _tools.RODict({
        "propID": 52013218,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":61,"adjMaxPhysicalAtk":147,"adjFatal":22,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013219: _tools.RODict({
        "propID": 52013219,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":67,"adjMaxPhysicalAtk":162,"adjFatal":24,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013220: _tools.RODict({
        "propID": 52013220,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":74,"adjMaxPhysicalAtk":178,"adjFatal":26,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013221: _tools.RODict({
        "propID": 52013221,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":81,"adjMaxPhysicalAtk":196,"adjFatal":28,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013382: _tools.RODict({
        "propID": 52013382,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":20,"adjMaxMagicAtk":50})
    }),
    52013383: _tools.RODict({
        "propID": 52013383,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":22,"adjMaxMagicAtk":55})
    }),
    52013384: _tools.RODict({
        "propID": 52013384,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":24,"adjMaxMagicAtk":60})
    }),
    52013385: _tools.RODict({
        "propID": 52013385,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":26,"adjMaxMagicAtk":65})
    }),
    52013386: _tools.RODict({
        "propID": 52013386,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":29,"adjMaxMagicAtk":72,"adjFatal":10,"adjIgnoreArmor":0.02})
    }),
    52013387: _tools.RODict({
        "propID": 52013387,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":32,"adjMaxMagicAtk":79,"adjFatal":11,"adjIgnoreArmor":0.02})
    }),
    52013388: _tools.RODict({
        "propID": 52013388,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":35,"adjMaxMagicAtk":86,"adjFatal":12,"adjIgnoreArmor":0.02})
    }),
    52013389: _tools.RODict({
        "propID": 52013389,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":38,"adjMaxMagicAtk":94,"adjFatal":13,"adjIgnoreArmor":0.02})
    }),
    52013390: _tools.RODict({
        "propID": 52013390,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":42,"adjMaxMagicAtk":103,"adjFatal":15,"adjIgnoreArmor":0.04})
    }),
    52013391: _tools.RODict({
        "propID": 52013391,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":46,"adjMaxMagicAtk":113,"adjFatal":16,"adjIgnoreArmor":0.04})
    }),
    52013392: _tools.RODict({
        "propID": 52013392,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":50,"adjMaxMagicAtk":124,"adjFatal":17,"adjIgnoreArmor":0.04})
    }),
    52013393: _tools.RODict({
        "propID": 52013393,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":55,"adjMaxMagicAtk":134,"adjFatal":19,"adjIgnoreArmor":0.04})
    }),
    52013394: _tools.RODict({
        "propID": 52013394,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":61,"adjMaxMagicAtk":147,"adjFatal":22,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013395: _tools.RODict({
        "propID": 52013395,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":67,"adjMaxMagicAtk":162,"adjFatal":24,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013396: _tools.RODict({
        "propID": 52013396,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":74,"adjMaxMagicAtk":178,"adjFatal":26,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013397: _tools.RODict({
        "propID": 52013397,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":81,"adjMaxMagicAtk":196,"adjFatal":28,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013558: _tools.RODict({
        "propID": 52013558,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":155,"adjMinPhysicalAtk":18,"adjMaxPhysicalAtk":43})
    }),
    52013559: _tools.RODict({
        "propID": 52013559,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":171,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":47})
    }),
    52013560: _tools.RODict({
        "propID": 52013560,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":186,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":52})
    }),
    52013561: _tools.RODict({
        "propID": 52013561,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":202,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":56})
    }),
    52013562: _tools.RODict({
        "propID": 52013562,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":222,"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":62,"adjIgnoreArmor":0.02})
    }),
    52013563: _tools.RODict({
        "propID": 52013563,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":244,"adjMinPhysicalAtk":28,"adjMaxPhysicalAtk":68,"adjIgnoreArmor":0.02})
    }),
    52013564: _tools.RODict({
        "propID": 52013564,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":266,"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":74,"adjIgnoreArmor":0.02})
    }),
    52013565: _tools.RODict({
        "propID": 52013565,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":289,"adjMinPhysicalAtk":33,"adjMaxPhysicalAtk":81,"adjIgnoreArmor":0.02})
    }),
    52013566: _tools.RODict({
        "propID": 52013566,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":318,"adjMinPhysicalAtk":36,"adjMaxPhysicalAtk":89,"adjIgnoreArmor":0.04})
    }),
    52013567: _tools.RODict({
        "propID": 52013567,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":350,"adjMinPhysicalAtk":40,"adjMaxPhysicalAtk":98,"adjIgnoreArmor":0.04})
    }),
    52013568: _tools.RODict({
        "propID": 52013568,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":382,"adjMinPhysicalAtk":43,"adjMaxPhysicalAtk":107,"adjIgnoreArmor":0.04})
    }),
    52013569: _tools.RODict({
        "propID": 52013569,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":413,"adjMinPhysicalAtk":47,"adjMaxPhysicalAtk":116,"adjIgnoreArmor":0.04})
    }),
    52013570: _tools.RODict({
        "propID": 52013570,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":454,"adjMinPhysicalAtk":52,"adjMaxPhysicalAtk":128,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013571: _tools.RODict({
        "propID": 52013571,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":499,"adjMinPhysicalAtk":57,"adjMaxPhysicalAtk":141,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013572: _tools.RODict({
        "propID": 52013572,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":549,"adjMinPhysicalAtk":63,"adjMaxPhysicalAtk":155,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013573: _tools.RODict({
        "propID": 52013573,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":604,"adjMinPhysicalAtk":69,"adjMaxPhysicalAtk":171,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013734: _tools.RODict({
        "propID": 52013734,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":155,"adjMinMagicAtk":18,"adjMaxMagicAtk":43})
    }),
    52013735: _tools.RODict({
        "propID": 52013735,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":171,"adjMinMagicAtk":20,"adjMaxMagicAtk":47})
    }),
    52013736: _tools.RODict({
        "propID": 52013736,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":186,"adjMinMagicAtk":22,"adjMaxMagicAtk":52})
    }),
    52013737: _tools.RODict({
        "propID": 52013737,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":202,"adjMinMagicAtk":23,"adjMaxMagicAtk":56})
    }),
    52013738: _tools.RODict({
        "propID": 52013738,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":222,"adjMinMagicAtk":25,"adjMaxMagicAtk":62,"adjIgnoreArmor":0.02})
    }),
    52013739: _tools.RODict({
        "propID": 52013739,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":244,"adjMinMagicAtk":28,"adjMaxMagicAtk":68,"adjIgnoreArmor":0.02})
    }),
    52013740: _tools.RODict({
        "propID": 52013740,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":266,"adjMinMagicAtk":30,"adjMaxMagicAtk":74,"adjIgnoreArmor":0.02})
    }),
    52013741: _tools.RODict({
        "propID": 52013741,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":289,"adjMinMagicAtk":33,"adjMaxMagicAtk":81,"adjIgnoreArmor":0.02})
    }),
    52013742: _tools.RODict({
        "propID": 52013742,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":318,"adjMinMagicAtk":36,"adjMaxMagicAtk":89,"adjIgnoreArmor":0.04})
    }),
    52013743: _tools.RODict({
        "propID": 52013743,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":350,"adjMinMagicAtk":40,"adjMaxMagicAtk":98,"adjIgnoreArmor":0.04})
    }),
    52013744: _tools.RODict({
        "propID": 52013744,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":382,"adjMinMagicAtk":43,"adjMaxMagicAtk":107,"adjIgnoreArmor":0.04})
    }),
    52013745: _tools.RODict({
        "propID": 52013745,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":413,"adjMinMagicAtk":47,"adjMaxMagicAtk":116,"adjIgnoreArmor":0.04})
    }),
    52013746: _tools.RODict({
        "propID": 52013746,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":454,"adjMinMagicAtk":52,"adjMaxMagicAtk":128,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013747: _tools.RODict({
        "propID": 52013747,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":499,"adjMinMagicAtk":57,"adjMaxMagicAtk":141,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013748: _tools.RODict({
        "propID": 52013748,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":549,"adjMinMagicAtk":63,"adjMaxMagicAtk":155,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013749: _tools.RODict({
        "propID": 52013749,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":604,"adjMinMagicAtk":69,"adjMaxMagicAtk":171,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013910: _tools.RODict({
        "propID": 52013910,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1200,"adjMinPhysicalAtk":18,"adjMaxPhysicalAtk":43})
    }),
    52013911: _tools.RODict({
        "propID": 52013911,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1320,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":47})
    }),
    52013912: _tools.RODict({
        "propID": 52013912,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1440,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":52})
    }),
    52013913: _tools.RODict({
        "propID": 52013913,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1560,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":56})
    }),
    52013914: _tools.RODict({
        "propID": 52013914,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1716,"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":62,"adjMonsterDmg":0.04})
    }),
    52013915: _tools.RODict({
        "propID": 52013915,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1888,"adjMinPhysicalAtk":28,"adjMaxPhysicalAtk":68,"adjMonsterDmg":0.04})
    }),
    52013916: _tools.RODict({
        "propID": 52013916,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2059,"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":74,"adjMonsterDmg":0.04})
    }),
    52013917: _tools.RODict({
        "propID": 52013917,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2231,"adjMinPhysicalAtk":33,"adjMaxPhysicalAtk":81,"adjMonsterDmg":0.04})
    }),
    52013918: _tools.RODict({
        "propID": 52013918,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2454,"adjMinPhysicalAtk":36,"adjMaxPhysicalAtk":89,"adjMonsterDmg":0.08})
    }),
    52013919: _tools.RODict({
        "propID": 52013919,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2699,"adjMinPhysicalAtk":40,"adjMaxPhysicalAtk":98,"adjMonsterDmg":0.08})
    }),
    52013920: _tools.RODict({
        "propID": 52013920,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2945,"adjMinPhysicalAtk":43,"adjMaxPhysicalAtk":107,"adjMonsterDmg":0.08})
    }),
    52013921: _tools.RODict({
        "propID": 52013921,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3190,"adjMinPhysicalAtk":47,"adjMaxPhysicalAtk":116,"adjMonsterDmg":0.08})
    }),
    52013922: _tools.RODict({
        "propID": 52013922,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3509,"adjMinPhysicalAtk":52,"adjMaxPhysicalAtk":128,"adjMonsterDmg":0.08,"adjMonsterDmgAnti":0.08})
    }),
    52013923: _tools.RODict({
        "propID": 52013923,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3860,"adjMinPhysicalAtk":57,"adjMaxPhysicalAtk":141,"adjMonsterDmg":0.08,"adjMonsterDmgAnti":0.08})
    }),
    52013924: _tools.RODict({
        "propID": 52013924,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4246,"adjMinPhysicalAtk":63,"adjMaxPhysicalAtk":155,"adjMonsterDmg":0.08,"adjMonsterDmgAnti":0.08})
    }),
    52013925: _tools.RODict({
        "propID": 52013925,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4671,"adjMinPhysicalAtk":69,"adjMaxPhysicalAtk":171,"adjMonsterDmg":0.08,"adjMonsterDmgAnti":0.08})
    }),
    52014086: _tools.RODict({
        "propID": 52014086,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1200,"adjMinMagicAtk":18,"adjMaxMagicAtk":43})
    }),
    52014087: _tools.RODict({
        "propID": 52014087,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1320,"adjMinMagicAtk":20,"adjMaxMagicAtk":47})
    }),
    52014088: _tools.RODict({
        "propID": 52014088,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1440,"adjMinMagicAtk":22,"adjMaxMagicAtk":52})
    }),
    52014089: _tools.RODict({
        "propID": 52014089,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1560,"adjMinMagicAtk":23,"adjMaxMagicAtk":56})
    }),
    52014090: _tools.RODict({
        "propID": 52014090,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1716,"adjMinMagicAtk":25,"adjMaxMagicAtk":62,"adjMonsterDmg":0.04})
    }),
    52014091: _tools.RODict({
        "propID": 52014091,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1888,"adjMinMagicAtk":28,"adjMaxMagicAtk":68,"adjMonsterDmg":0.04})
    }),
    52014092: _tools.RODict({
        "propID": 52014092,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2059,"adjMinMagicAtk":30,"adjMaxMagicAtk":74,"adjMonsterDmg":0.04})
    }),
    52014093: _tools.RODict({
        "propID": 52014093,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2231,"adjMinMagicAtk":33,"adjMaxMagicAtk":81,"adjMonsterDmg":0.04})
    }),
    52014094: _tools.RODict({
        "propID": 52014094,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2454,"adjMinMagicAtk":36,"adjMaxMagicAtk":89,"adjMonsterDmg":0.08})
    }),
    52014095: _tools.RODict({
        "propID": 52014095,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2699,"adjMinMagicAtk":40,"adjMaxMagicAtk":98,"adjMonsterDmg":0.08})
    }),
    52014096: _tools.RODict({
        "propID": 52014096,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2945,"adjMinMagicAtk":43,"adjMaxMagicAtk":107,"adjMonsterDmg":0.08})
    }),
    52014097: _tools.RODict({
        "propID": 52014097,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3190,"adjMinMagicAtk":47,"adjMaxMagicAtk":116,"adjMonsterDmg":0.08})
    }),
    52014098: _tools.RODict({
        "propID": 52014098,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3509,"adjMinMagicAtk":52,"adjMaxMagicAtk":128,"adjMonsterDmg":0.08,"adjMonsterDmgAnti":0.08})
    }),
    52014099: _tools.RODict({
        "propID": 52014099,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3860,"adjMinMagicAtk":57,"adjMaxMagicAtk":141,"adjMonsterDmg":0.08,"adjMonsterDmgAnti":0.08})
    }),
    52014100: _tools.RODict({
        "propID": 52014100,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4246,"adjMinMagicAtk":63,"adjMaxMagicAtk":155,"adjMonsterDmg":0.08,"adjMonsterDmgAnti":0.08})
    }),
    52014101: _tools.RODict({
        "propID": 52014101,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4671,"adjMinMagicAtk":69,"adjMaxMagicAtk":171,"adjMonsterDmg":0.08,"adjMonsterDmgAnti":0.08})
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