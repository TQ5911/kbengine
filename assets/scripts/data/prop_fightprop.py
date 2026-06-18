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
        "propList": _tools.RODict({"adjFullHp":50,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":22,"adjMinMagicAtk":22,"adjMaxMagicAtk":22,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjAccuracy":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjMonsterDmg":0.01})
    }),
    51000002: _tools.RODict({
        "propID": 51000002,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":53,"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":24,"adjMinMagicAtk":24,"adjMaxMagicAtk":24,"adjMinPhysicalArmor":17,"adjMaxPhysicalArmor":17,"adjMinMagicArmor":17,"adjMaxMagicArmor":17,"adjAccuracy":2,"adjRealDmg":2,"adjRealDmgDef":2,"adjMonsterDmg":0.01})
    }),
    51000003: _tools.RODict({
        "propID": 51000003,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":56,"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":26,"adjMinMagicAtk":26,"adjMaxMagicAtk":26,"adjMinPhysicalArmor":18,"adjMaxPhysicalArmor":18,"adjMinMagicArmor":18,"adjMaxMagicArmor":18,"adjAccuracy":2,"adjRealDmg":3,"adjRealDmgDef":3,"adjMonsterDmg":0.01})
    }),
    51000004: _tools.RODict({
        "propID": 51000004,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":59,"adjMinPhysicalAtk":28,"adjMaxPhysicalAtk":28,"adjMinMagicAtk":28,"adjMaxMagicAtk":28,"adjMinPhysicalArmor":19,"adjMaxPhysicalArmor":19,"adjMinMagicArmor":19,"adjMaxMagicArmor":19,"adjAccuracy":2,"adjRealDmg":4,"adjRealDmgDef":4,"adjMonsterDmg":0.01})
    }),
    51000005: _tools.RODict({
        "propID": 51000005,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":62,"adjMinPhysicalAtk":36,"adjMaxPhysicalAtk":36,"adjMinMagicAtk":36,"adjMaxMagicAtk":36,"adjMinPhysicalArmor":20,"adjMaxPhysicalArmor":20,"adjMinMagicArmor":20,"adjMaxMagicArmor":20,"adjAccuracy":2,"adjRealDmg":5,"adjRealDmgDef":5,"adjMonsterDmg":0.01})
    }),
    51000006: _tools.RODict({
        "propID": 51000006,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":65,"adjMinPhysicalAtk":65,"adjMaxPhysicalAtk":65,"adjMinMagicAtk":65,"adjMaxMagicAtk":65,"adjMinPhysicalArmor":22,"adjMaxPhysicalArmor":22,"adjMinMagicArmor":22,"adjMaxMagicArmor":22,"adjAccuracy":2,"adjRealDmg":6,"adjRealDmgDef":6,"adjMonsterDmg":0.01})
    }),
    51000007: _tools.RODict({
        "propID": 51000007,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":68,"adjMinPhysicalAtk":102,"adjMaxPhysicalAtk":102,"adjMinMagicAtk":102,"adjMaxMagicAtk":102,"adjMinPhysicalArmor":25,"adjMaxPhysicalArmor":25,"adjMinMagicArmor":25,"adjMaxMagicArmor":25,"adjAccuracy":2,"adjRealDmg":7,"adjRealDmgDef":7,"adjMonsterDmg":0.01})
    }),
    51000008: _tools.RODict({
        "propID": 51000008,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":71,"adjMinPhysicalAtk":124,"adjMaxPhysicalAtk":124,"adjMinMagicAtk":124,"adjMaxMagicAtk":124,"adjMinPhysicalArmor":35,"adjMaxPhysicalArmor":35,"adjMinMagicArmor":35,"adjMaxMagicArmor":35,"adjAccuracy":2,"adjRealDmg":8,"adjRealDmgDef":8,"adjMonsterDmg":0.01})
    }),
    51000009: _tools.RODict({
        "propID": 51000009,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":75,"adjMinPhysicalAtk":135,"adjMaxPhysicalAtk":135,"adjMinMagicAtk":135,"adjMaxMagicAtk":135,"adjMinPhysicalArmor":120,"adjMaxPhysicalArmor":120,"adjMinMagicArmor":120,"adjMaxMagicArmor":120,"adjAccuracy":2,"adjRealDmg":9,"adjRealDmgDef":9,"adjMonsterDmg":0.01})
    }),
    51000010: _tools.RODict({
        "propID": 51000010,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":80,"adjMinPhysicalAtk":145,"adjMaxPhysicalAtk":145,"adjMinMagicAtk":145,"adjMaxMagicAtk":145,"adjMinPhysicalArmor":125,"adjMaxPhysicalArmor":125,"adjMinMagicArmor":125,"adjMaxMagicArmor":125,"adjAccuracy":2,"adjRealDmg":10,"adjRealDmgDef":10,"adjMonsterDmg":0.01})
    }),
    51000011: _tools.RODict({
        "propID": 51000011,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":90,"adjMinPhysicalAtk":168,"adjMaxPhysicalAtk":168,"adjMinMagicAtk":168,"adjMaxMagicAtk":168,"adjMinPhysicalArmor":131,"adjMaxPhysicalArmor":131,"adjMinMagicArmor":131,"adjMaxMagicArmor":131,"adjAccuracy":2,"adjFatal":1,"adjAntiMortal":0.003,"adjRealDmg":11,"adjRealDmgDef":11,"adjMonsterDmg":0.01,"adjFinalDmg":0.003,"adjFinalDmgAnti":0.003})
    }),
    51000012: _tools.RODict({
        "propID": 51000012,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":100,"adjMinPhysicalAtk":190,"adjMaxPhysicalAtk":190,"adjMinMagicAtk":190,"adjMaxMagicAtk":190,"adjMinPhysicalArmor":137,"adjMaxPhysicalArmor":137,"adjMinMagicArmor":137,"adjMaxMagicArmor":137,"adjAccuracy":2,"adjFatal":1,"adjAntiMortal":0.003,"adjRealDmg":12,"adjRealDmgDef":12,"adjMonsterDmg":0.01,"adjFinalDmg":0.003,"adjFinalDmgAnti":0.003})
    }),
    51000013: _tools.RODict({
        "propID": 51000013,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":110,"adjMinPhysicalAtk":202,"adjMaxPhysicalAtk":202,"adjMinMagicAtk":202,"adjMaxMagicAtk":202,"adjMinPhysicalArmor":143,"adjMaxPhysicalArmor":143,"adjMinMagicArmor":143,"adjMaxMagicArmor":143,"adjAccuracy":2,"adjFatal":1,"adjAntiMortal":0.003,"adjRealDmg":13,"adjRealDmgDef":13,"adjMonsterDmg":0.01,"adjFinalDmg":0.003,"adjFinalDmgAnti":0.003})
    }),
    51000014: _tools.RODict({
        "propID": 51000014,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":120,"adjMinPhysicalAtk":210,"adjMaxPhysicalAtk":210,"adjMinMagicAtk":210,"adjMaxMagicAtk":210,"adjMinPhysicalArmor":150,"adjMaxPhysicalArmor":150,"adjMinMagicArmor":150,"adjMaxMagicArmor":150,"adjAccuracy":2,"adjFatal":1,"adjAntiMortal":0.003,"adjRealDmg":14,"adjRealDmgDef":14,"adjMonsterDmg":0.01,"adjFinalDmg":0.003,"adjFinalDmgAnti":0.003})
    }),
    51000015: _tools.RODict({
        "propID": 51000015,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":135,"adjMinPhysicalAtk":220,"adjMaxPhysicalAtk":220,"adjMinMagicAtk":220,"adjMaxMagicAtk":220,"adjMinPhysicalArmor":156,"adjMaxPhysicalArmor":156,"adjMinMagicArmor":156,"adjMaxMagicArmor":156,"adjAccuracy":2,"adjFatal":1,"adjAntiMortal":0.003,"adjRealDmg":15,"adjRealDmgDef":15,"adjMonsterDmg":0.01,"adjFinalDmg":0.003,"adjFinalDmgAnti":0.003})
    }),
    51000016: _tools.RODict({
        "propID": 51000016,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":150,"adjMinPhysicalAtk":225,"adjMaxPhysicalAtk":225,"adjMinMagicAtk":225,"adjMaxMagicAtk":225,"adjMinPhysicalArmor":162,"adjMaxPhysicalArmor":162,"adjMinMagicArmor":162,"adjMaxMagicArmor":162,"adjAccuracy":2,"adjFatal":1,"adjAntiMortal":0.003,"adjRealDmg":16,"adjRealDmgDef":16,"adjMonsterDmg":0.01,"adjFinalDmg":0.006,"adjFinalDmgAnti":0.006})
    }),
    51000017: _tools.RODict({
        "propID": 51000017,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":160,"adjMinPhysicalAtk":242,"adjMaxPhysicalAtk":242,"adjMinMagicAtk":242,"adjMaxMagicAtk":242,"adjMinPhysicalArmor":168,"adjMaxPhysicalArmor":168,"adjMinMagicArmor":168,"adjMaxMagicArmor":168,"adjAccuracy":2,"adjFatal":1,"adjAntiMortal":0.003,"adjRealDmg":17,"adjRealDmgDef":17,"adjMonsterDmg":0.01,"adjFinalDmg":0.006,"adjFinalDmgAnti":0.006})
    }),
    51000018: _tools.RODict({
        "propID": 51000018,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":170,"adjMinPhysicalAtk":256,"adjMaxPhysicalAtk":256,"adjMinMagicAtk":256,"adjMaxMagicAtk":256,"adjMinPhysicalArmor":175,"adjMaxPhysicalArmor":175,"adjMinMagicArmor":175,"adjMaxMagicArmor":175,"adjAccuracy":2,"adjFatal":1,"adjAntiMortal":0.003,"adjRealDmg":18,"adjRealDmgDef":18,"adjMonsterDmg":0.01,"adjFinalDmg":0.006,"adjFinalDmgAnti":0.006})
    }),
    51000019: _tools.RODict({
        "propID": 51000019,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":180,"adjMinPhysicalAtk":269,"adjMaxPhysicalAtk":269,"adjMinMagicAtk":269,"adjMaxMagicAtk":269,"adjMinPhysicalArmor":181,"adjMaxPhysicalArmor":181,"adjMinMagicArmor":181,"adjMaxMagicArmor":181,"adjAccuracy":2,"adjFatal":1,"adjAntiMortal":0.003,"adjRealDmg":19,"adjRealDmgDef":19,"adjMonsterDmg":0.01,"adjFinalDmg":0.006,"adjFinalDmgAnti":0.006})
    }),
    51000020: _tools.RODict({
        "propID": 51000020,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":190,"adjMinPhysicalAtk":280,"adjMaxPhysicalAtk":280,"adjMinMagicAtk":280,"adjMaxMagicAtk":280,"adjMinPhysicalArmor":187,"adjMaxPhysicalArmor":187,"adjMinMagicArmor":187,"adjMaxMagicArmor":187,"adjAccuracy":3,"adjEvasion":1,"adjFatal":1,"adjAntiMortal":0.003,"adjRealDmg":20,"adjRealDmgDef":20,"adjMonsterDmg":0.01,"adjFinalDmg":0.007,"adjFinalDmgAnti":0.007,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1})
    }),
    51000021: _tools.RODict({
        "propID": 51000021,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":220,"adjMinPhysicalAtk":305,"adjMaxPhysicalAtk":305,"adjMinMagicAtk":305,"adjMaxMagicAtk":305,"adjMinPhysicalArmor":194,"adjMaxPhysicalArmor":194,"adjMinMagicArmor":194,"adjMaxMagicArmor":194,"adjAccuracy":3,"adjEvasion":1,"adjFatal":1,"adjAntiMortal":0.003,"adjRealDmg":21,"adjRealDmgDef":21,"adjMonsterDmg":0.01,"adjFinalDmg":0.007,"adjFinalDmgAnti":0.007,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1})
    }),
    51000022: _tools.RODict({
        "propID": 51000022,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":250,"adjMinPhysicalAtk":320,"adjMaxPhysicalAtk":320,"adjMinMagicAtk":320,"adjMaxMagicAtk":320,"adjMinPhysicalArmor":202,"adjMaxPhysicalArmor":202,"adjMinMagicArmor":202,"adjMaxMagicArmor":202,"adjAccuracy":3,"adjEvasion":1,"adjFatal":1,"adjAntiMortal":0.003,"adjRealDmg":22,"adjRealDmgDef":22,"adjMonsterDmg":0.01,"adjFinalDmg":0.007,"adjFinalDmgAnti":0.007,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1})
    }),
    51000023: _tools.RODict({
        "propID": 51000023,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":280,"adjMinPhysicalAtk":340,"adjMaxPhysicalAtk":340,"adjMinMagicAtk":340,"adjMaxMagicAtk":340,"adjMinPhysicalArmor":209,"adjMaxPhysicalArmor":209,"adjMinMagicArmor":209,"adjMaxMagicArmor":209,"adjAccuracy":3,"adjEvasion":1,"adjFatal":1,"adjAntiMortal":0.003,"adjRealDmg":23,"adjRealDmgDef":23,"adjMonsterDmg":0.01,"adjFinalDmg":0.007,"adjFinalDmgAnti":0.007,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1})
    }),
    51000024: _tools.RODict({
        "propID": 51000024,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":310,"adjMinPhysicalAtk":365,"adjMaxPhysicalAtk":365,"adjMinMagicAtk":365,"adjMaxMagicAtk":365,"adjMinPhysicalArmor":216,"adjMaxPhysicalArmor":216,"adjMinMagicArmor":216,"adjMaxMagicArmor":216,"adjAccuracy":3,"adjEvasion":1,"adjFatal":1,"adjAntiMortal":0.003,"adjRealDmg":24,"adjRealDmgDef":24,"adjMonsterDmg":0.01,"adjFinalDmg":0.007,"adjFinalDmgAnti":0.007,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1})
    }),
    51000025: _tools.RODict({
        "propID": 51000025,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":341,"adjMinPhysicalAtk":390,"adjMaxPhysicalAtk":390,"adjMinMagicAtk":390,"adjMaxMagicAtk":390,"adjMinPhysicalArmor":223,"adjMaxPhysicalArmor":223,"adjMinMagicArmor":223,"adjMaxMagicArmor":223,"adjAccuracy":5,"adjEvasion":2,"adjFatal":2,"adjIgnoreArmor":0.004,"adjMortal":0.06,"adjAntiMortal":0.003,"adjRealDmg":25,"adjRealDmgDef":25,"adjMonsterDmg":0.01,"adjFinalDmg":0.0113,"adjFinalDmgAnti":0.008,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1})
    }),
    51000026: _tools.RODict({
        "propID": 51000026,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":377,"adjMinPhysicalAtk":403,"adjMaxPhysicalAtk":403,"adjMinMagicAtk":403,"adjMaxMagicAtk":403,"adjMinPhysicalArmor":230,"adjMaxPhysicalArmor":230,"adjMinMagicArmor":230,"adjMaxMagicArmor":230,"adjAccuracy":5,"adjEvasion":2,"adjFatal":2,"adjIgnoreArmor":0.004,"adjMortal":0.06,"adjAntiMortal":0.003,"adjRealDmg":26,"adjRealDmgDef":26,"adjMonsterDmg":0.01,"adjFinalDmg":0.0113,"adjFinalDmgAnti":0.008,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1})
    }),
    51000027: _tools.RODict({
        "propID": 51000027,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":413,"adjMinPhysicalAtk":415,"adjMaxPhysicalAtk":415,"adjMinMagicAtk":415,"adjMaxMagicAtk":415,"adjMinPhysicalArmor":238,"adjMaxPhysicalArmor":238,"adjMinMagicArmor":238,"adjMaxMagicArmor":238,"adjAccuracy":6,"adjEvasion":2,"adjFatal":2,"adjIgnoreArmor":0.004,"adjMortal":0.06,"adjAntiMortal":0.003,"adjRealDmg":27,"adjRealDmgDef":27,"adjMonsterDmg":0.01,"adjFinalDmg":0.0113,"adjFinalDmgAnti":0.008,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1})
    }),
    51000028: _tools.RODict({
        "propID": 51000028,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":449,"adjMinPhysicalAtk":421,"adjMaxPhysicalAtk":421,"adjMinMagicAtk":421,"adjMaxMagicAtk":421,"adjMinPhysicalArmor":245,"adjMaxPhysicalArmor":245,"adjMinMagicArmor":245,"adjMaxMagicArmor":245,"adjAccuracy":6,"adjEvasion":2,"adjFatal":3,"adjIgnoreArmor":0.004,"adjMortal":0.06,"adjAntiMortal":0.003,"adjRealDmg":28,"adjRealDmgDef":28,"adjMonsterDmg":0.01,"adjFinalDmg":0.0113,"adjFinalDmgAnti":0.008,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1})
    }),
    51000029: _tools.RODict({
        "propID": 51000029,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":485,"adjMinPhysicalAtk":430,"adjMaxPhysicalAtk":430,"adjMinMagicAtk":430,"adjMaxMagicAtk":430,"adjMinPhysicalArmor":252,"adjMaxPhysicalArmor":252,"adjMinMagicArmor":252,"adjMaxMagicArmor":252,"adjAccuracy":6,"adjEvasion":2,"adjFatal":5,"adjIgnoreArmor":0.004,"adjMortal":0.06,"adjAntiMortal":0.003,"adjRealDmg":29,"adjRealDmgDef":29,"adjMonsterDmg":0.01,"adjFinalDmg":0.0113,"adjFinalDmgAnti":0.008,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1})
    }),
    51000030: _tools.RODict({
        "propID": 51000030,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":521,"adjMinPhysicalAtk":441,"adjMaxPhysicalAtk":441,"adjMinMagicAtk":441,"adjMaxMagicAtk":441,"adjMinPhysicalArmor":259,"adjMaxPhysicalArmor":259,"adjMinMagicArmor":259,"adjMaxMagicArmor":259,"adjAccuracy":7,"adjEvasion":4,"adjFatal":10,"adjAntiFatal":1,"adjIgnoreArmor":0.028,"adjDmgArmor":0.008,"adjMortal":0.06,"adjAntiMortal":0.003,"adjRealDmg":30,"adjRealDmgDef":30,"adjMonsterDmg":0.01,"adjFinalDmg":0.0633,"adjFinalDmgAnti":0.0133,"adjStunEnh":2,"adjStunAnti":2,"adjSilentEnh":2,"adjSilentAnti":2,"adjKnockEnh":2,"adjKnockAnti":2,"adjFrozenEnh":2,"adjFrozenAnti":2,"adjSlowEnh":2,"adjSlowAnti":2})
    }),
    51000031: _tools.RODict({
        "propID": 51000031,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":550,"adjMinPhysicalAtk":453,"adjMaxPhysicalAtk":453,"adjMinMagicAtk":453,"adjMaxMagicAtk":453,"adjMinPhysicalArmor":265,"adjMaxPhysicalArmor":265,"adjMinMagicArmor":265,"adjMaxMagicArmor":265,"adjAccuracy":7,"adjEvasion":5,"adjFatal":15,"adjAntiFatal":3,"adjIgnoreArmor":0.0303,"adjDmgArmor":0.0088,"adjMortal":0.0685,"adjAntiMortal":0.0055,"adjRealDmg":31,"adjRealDmgDef":31,"adjMonsterDmg":0.01,"adjFinalDmg":0.0641,"adjFinalDmgAnti":0.0141,"adjStunEnh":2,"adjStunAnti":2,"adjSilentEnh":2,"adjSilentAnti":2,"adjKnockEnh":2,"adjKnockAnti":2,"adjFrozenEnh":2,"adjFrozenAnti":2,"adjSlowEnh":2,"adjSlowAnti":2})
    }),
    51000032: _tools.RODict({
        "propID": 51000032,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":564,"adjMinPhysicalAtk":469,"adjMaxPhysicalAtk":469,"adjMinMagicAtk":469,"adjMaxMagicAtk":469,"adjMinPhysicalArmor":271,"adjMaxPhysicalArmor":271,"adjMinMagicArmor":271,"adjMaxMagicArmor":271,"adjAccuracy":8,"adjEvasion":5,"adjFatal":16,"adjAntiFatal":5,"adjIgnoreArmor":0.0326,"adjDmgArmor":0.0096,"adjMortal":0.077,"adjAntiMortal":0.008,"adjRealDmg":32,"adjRealDmgDef":32,"adjMonsterDmg":0.01,"adjFinalDmg":0.0648,"adjFinalDmgAnti":0.0148,"adjStunEnh":2,"adjStunAnti":2,"adjSilentEnh":2,"adjSilentAnti":2,"adjKnockEnh":2,"adjKnockAnti":2,"adjFrozenEnh":2,"adjFrozenAnti":2,"adjSlowEnh":2,"adjSlowAnti":2})
    }),
    51000033: _tools.RODict({
        "propID": 51000033,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":577,"adjMinPhysicalAtk":481,"adjMaxPhysicalAtk":481,"adjMinMagicAtk":481,"adjMaxMagicAtk":481,"adjMinPhysicalArmor":276,"adjMaxPhysicalArmor":276,"adjMinMagicArmor":276,"adjMaxMagicArmor":276,"adjAccuracy":8,"adjEvasion":6,"adjFatal":17,"adjAntiFatal":6,"adjIgnoreArmor":0.0349,"adjDmgArmor":0.0104,"adjMortal":0.0855,"adjAntiMortal":0.0105,"adjRealDmg":33,"adjRealDmgDef":33,"adjMonsterDmg":0.01,"adjFinalDmg":0.0655,"adjFinalDmgAnti":0.0155,"adjStunEnh":2,"adjStunAnti":2,"adjSilentEnh":2,"adjSilentAnti":2,"adjKnockEnh":2,"adjKnockAnti":2,"adjFrozenEnh":2,"adjFrozenAnti":2,"adjSlowEnh":2,"adjSlowAnti":2})
    }),
    51000034: _tools.RODict({
        "propID": 51000034,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":590,"adjMinPhysicalAtk":494,"adjMaxPhysicalAtk":494,"adjMinMagicAtk":494,"adjMaxMagicAtk":494,"adjMinPhysicalArmor":282,"adjMaxPhysicalArmor":282,"adjMinMagicArmor":282,"adjMaxMagicArmor":282,"adjAccuracy":9,"adjEvasion":6,"adjFatal":17,"adjAntiFatal":8,"adjIgnoreArmor":0.0372,"adjDmgArmor":0.0112,"adjMortal":0.094,"adjAntiMortal":0.013,"adjRealDmg":34,"adjRealDmgDef":34,"adjMonsterDmg":0.01,"adjFinalDmg":0.0663,"adjFinalDmgAnti":0.0163,"adjStunEnh":2,"adjStunAnti":2,"adjSilentEnh":2,"adjSilentAnti":2,"adjKnockEnh":2,"adjKnockAnti":2,"adjFrozenEnh":2,"adjFrozenAnti":2,"adjSlowEnh":2,"adjSlowAnti":2})
    }),
    51000035: _tools.RODict({
        "propID": 51000035,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":611,"adjMinPhysicalAtk":513,"adjMaxPhysicalAtk":513,"adjMinMagicAtk":513,"adjMaxMagicAtk":513,"adjMinPhysicalArmor":288,"adjMaxPhysicalArmor":288,"adjMinMagicArmor":288,"adjMaxMagicArmor":288,"adjAccuracy":9,"adjEvasion":7,"adjFatal":17,"adjAntiFatal":10,"adjIgnoreArmor":0.0395,"adjDmgArmor":0.012,"adjMortal":0.1025,"adjAntiMortal":0.0155,"adjRealDmg":35,"adjRealDmgDef":35,"adjMonsterDmg":0.01,"adjFinalDmg":0.067,"adjFinalDmgAnti":0.017,"adjStunEnh":2,"adjStunAnti":2,"adjSilentEnh":2,"adjSilentAnti":2,"adjKnockEnh":2,"adjKnockAnti":2,"adjFrozenEnh":2,"adjFrozenAnti":2,"adjSlowEnh":2,"adjSlowAnti":2})
    }),
    51000036: _tools.RODict({
        "propID": 51000036,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":624,"adjMinPhysicalAtk":526,"adjMaxPhysicalAtk":526,"adjMinMagicAtk":526,"adjMaxMagicAtk":526,"adjMinPhysicalArmor":294,"adjMaxPhysicalArmor":294,"adjMinMagicArmor":294,"adjMaxMagicArmor":294,"adjAccuracy":10,"adjEvasion":7,"adjFatal":18,"adjAntiFatal":11,"adjIgnoreArmor":0.0418,"adjDmgArmor":0.0128,"adjMortal":0.111,"adjAntiMortal":0.018,"adjRealDmg":36,"adjRealDmgDef":36,"adjMonsterDmg":0.01,"adjFinalDmg":0.0677,"adjFinalDmgAnti":0.0177,"adjStunEnh":3,"adjStunAnti":3,"adjSilentEnh":3,"adjSilentAnti":3,"adjKnockEnh":3,"adjKnockAnti":3,"adjFrozenEnh":3,"adjFrozenAnti":3,"adjSlowEnh":3,"adjSlowAnti":3})
    }),
    51000037: _tools.RODict({
        "propID": 51000037,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":636,"adjMinPhysicalAtk":537,"adjMaxPhysicalAtk":537,"adjMinMagicAtk":537,"adjMaxMagicAtk":537,"adjMinPhysicalArmor":299,"adjMaxPhysicalArmor":299,"adjMinMagicArmor":299,"adjMaxMagicArmor":299,"adjAccuracy":10,"adjEvasion":7,"adjFatal":18,"adjAntiFatal":13,"adjIgnoreArmor":0.0441,"adjDmgArmor":0.0136,"adjMortal":0.1195,"adjAntiMortal":0.0205,"adjRealDmg":37,"adjRealDmgDef":37,"adjMonsterDmg":0.01,"adjFinalDmg":0.0685,"adjFinalDmgAnti":0.0185,"adjStunEnh":3,"adjStunAnti":3,"adjSilentEnh":3,"adjSilentAnti":3,"adjKnockEnh":3,"adjKnockAnti":3,"adjFrozenEnh":3,"adjFrozenAnti":3,"adjSlowEnh":3,"adjSlowAnti":3})
    }),
    51000038: _tools.RODict({
        "propID": 51000038,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":648,"adjMinPhysicalAtk":553,"adjMaxPhysicalAtk":553,"adjMinMagicAtk":553,"adjMaxMagicAtk":553,"adjMinPhysicalArmor":305,"adjMaxPhysicalArmor":305,"adjMinMagicArmor":305,"adjMaxMagicArmor":305,"adjAccuracy":11,"adjEvasion":8,"adjFatal":18,"adjAntiFatal":14,"adjIgnoreArmor":0.0464,"adjDmgArmor":0.0144,"adjMortal":0.128,"adjAntiMortal":0.023,"adjRealDmg":38,"adjRealDmgDef":38,"adjMonsterDmg":0.01,"adjFinalDmg":0.0692,"adjFinalDmgAnti":0.0192,"adjStunEnh":3,"adjStunAnti":3,"adjSilentEnh":3,"adjSilentAnti":3,"adjKnockEnh":3,"adjKnockAnti":3,"adjFrozenEnh":3,"adjFrozenAnti":3,"adjSlowEnh":3,"adjSlowAnti":3})
    }),
    51000039: _tools.RODict({
        "propID": 51000039,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":660,"adjMinPhysicalAtk":569,"adjMaxPhysicalAtk":569,"adjMinMagicAtk":569,"adjMaxMagicAtk":569,"adjMinPhysicalArmor":311,"adjMaxPhysicalArmor":311,"adjMinMagicArmor":311,"adjMaxMagicArmor":311,"adjAccuracy":11,"adjEvasion":8,"adjFatal":19,"adjAntiFatal":16,"adjIgnoreArmor":0.0487,"adjDmgArmor":0.0152,"adjMortal":0.1365,"adjAntiMortal":0.0255,"adjRealDmg":39,"adjRealDmgDef":39,"adjMonsterDmg":0.01,"adjFinalDmg":0.0699,"adjFinalDmgAnti":0.0199,"adjStunEnh":3,"adjStunAnti":3,"adjSilentEnh":3,"adjSilentAnti":3,"adjKnockEnh":3,"adjKnockAnti":3,"adjFrozenEnh":3,"adjFrozenAnti":3,"adjSlowEnh":3,"adjSlowAnti":3})
    }),
    51000040: _tools.RODict({
        "propID": 51000040,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":671,"adjMinPhysicalAtk":586,"adjMaxPhysicalAtk":586,"adjMinMagicAtk":586,"adjMaxMagicAtk":586,"adjMinPhysicalArmor":316,"adjMaxPhysicalArmor":316,"adjMinMagicArmor":316,"adjMaxMagicArmor":316,"adjAccuracy":12,"adjEvasion":9,"adjFatal":19,"adjAntiFatal":18,"adjIgnoreArmor":0.051,"adjDmgArmor":0.016,"adjMortal":0.145,"adjAntiMortal":0.028,"adjRealDmg":40,"adjRealDmgDef":40,"adjMonsterDmg":0.01,"adjFinalDmg":0.0707,"adjFinalDmgAnti":0.0207,"adjStunEnh":3,"adjStunAnti":3,"adjSilentEnh":3,"adjSilentAnti":3,"adjKnockEnh":3,"adjKnockAnti":3,"adjFrozenEnh":3,"adjFrozenAnti":3,"adjSlowEnh":3,"adjSlowAnti":3})
    }),
    51000041: _tools.RODict({
        "propID": 51000041,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":687,"adjMinPhysicalAtk":607,"adjMaxPhysicalAtk":607,"adjMinMagicAtk":607,"adjMaxMagicAtk":607,"adjMinPhysicalArmor":325,"adjMaxPhysicalArmor":325,"adjMinMagicArmor":325,"adjMaxMagicArmor":325,"adjAccuracy":13,"adjEvasion":9,"adjFatal":20,"adjAntiFatal":18,"adjIgnoreArmor":0.0525,"adjDmgArmor":0.016,"adjMortal":0.1475,"adjAntiMortal":0.0308,"adjRealDmg":41,"adjRealDmgDef":41,"adjMonsterDmg":0.01,"adjFinalDmg":0.0713,"adjFinalDmgAnti":0.0213,"adjStunEnh":4,"adjStunAnti":4,"adjSilentEnh":4,"adjSilentAnti":4,"adjKnockEnh":4,"adjKnockAnti":4,"adjFrozenEnh":4,"adjFrozenAnti":4,"adjSlowEnh":4,"adjSlowAnti":4})
    }),
    51000042: _tools.RODict({
        "propID": 51000042,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":704,"adjMinPhysicalAtk":625,"adjMaxPhysicalAtk":625,"adjMinMagicAtk":625,"adjMaxMagicAtk":625,"adjMinPhysicalArmor":334,"adjMaxPhysicalArmor":334,"adjMinMagicArmor":334,"adjMaxMagicArmor":334,"adjAccuracy":13,"adjEvasion":10,"adjFatal":20,"adjAntiFatal":18,"adjIgnoreArmor":0.054,"adjDmgArmor":0.016,"adjMortal":0.15,"adjAntiMortal":0.0336,"adjRealDmg":42,"adjRealDmgDef":42,"adjMonsterDmg":0.01,"adjFinalDmg":0.0719,"adjFinalDmgAnti":0.0219,"adjStunEnh":4,"adjStunAnti":4,"adjSilentEnh":4,"adjSilentAnti":4,"adjKnockEnh":4,"adjKnockAnti":4,"adjFrozenEnh":4,"adjFrozenAnti":4,"adjSlowEnh":4,"adjSlowAnti":4})
    }),
    51000043: _tools.RODict({
        "propID": 51000043,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":720,"adjMinPhysicalAtk":643,"adjMaxPhysicalAtk":643,"adjMinMagicAtk":643,"adjMaxMagicAtk":643,"adjMinPhysicalArmor":343,"adjMaxPhysicalArmor":343,"adjMinMagicArmor":343,"adjMaxMagicArmor":343,"adjAccuracy":14,"adjEvasion":10,"adjFatal":20,"adjAntiFatal":19,"adjIgnoreArmor":0.0555,"adjDmgArmor":0.016,"adjMortal":0.1525,"adjAntiMortal":0.0364,"adjRealDmg":43,"adjRealDmgDef":43,"adjMonsterDmg":0.01,"adjFinalDmg":0.0725,"adjFinalDmgAnti":0.0225,"adjStunEnh":4,"adjStunAnti":4,"adjSilentEnh":4,"adjSilentAnti":4,"adjKnockEnh":4,"adjKnockAnti":4,"adjFrozenEnh":4,"adjFrozenAnti":4,"adjSlowEnh":4,"adjSlowAnti":4})
    }),
    51000044: _tools.RODict({
        "propID": 51000044,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":737,"adjMinPhysicalAtk":661,"adjMaxPhysicalAtk":661,"adjMinMagicAtk":661,"adjMaxMagicAtk":661,"adjMinPhysicalArmor":352,"adjMaxPhysicalArmor":352,"adjMinMagicArmor":352,"adjMaxMagicArmor":352,"adjAccuracy":15,"adjEvasion":11,"adjFatal":21,"adjAntiFatal":19,"adjIgnoreArmor":0.057,"adjDmgArmor":0.016,"adjMortal":0.155,"adjAntiMortal":0.0392,"adjRealDmg":44,"adjRealDmgDef":44,"adjMonsterDmg":0.01,"adjFinalDmg":0.0731,"adjFinalDmgAnti":0.0231,"adjStunEnh":4,"adjStunAnti":4,"adjSilentEnh":4,"adjSilentAnti":4,"adjKnockEnh":4,"adjKnockAnti":4,"adjFrozenEnh":4,"adjFrozenAnti":4,"adjSlowEnh":4,"adjSlowAnti":4})
    }),
    51000045: _tools.RODict({
        "propID": 51000045,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":754,"adjMinPhysicalAtk":679,"adjMaxPhysicalAtk":679,"adjMinMagicAtk":679,"adjMaxMagicAtk":679,"adjMinPhysicalArmor":361,"adjMaxPhysicalArmor":361,"adjMinMagicArmor":361,"adjMaxMagicArmor":361,"adjAccuracy":16,"adjEvasion":12,"adjFatal":21,"adjAntiFatal":19,"adjIgnoreArmor":0.0585,"adjDmgArmor":0.016,"adjMortal":0.1575,"adjAntiMortal":0.042,"adjRealDmg":45,"adjRealDmgDef":45,"adjMonsterDmg":0.01,"adjFinalDmg":0.0737,"adjFinalDmgAnti":0.0237,"adjStunEnh":4,"adjStunAnti":4,"adjSilentEnh":4,"adjSilentAnti":4,"adjKnockEnh":4,"adjKnockAnti":4,"adjFrozenEnh":4,"adjFrozenAnti":4,"adjSlowEnh":4,"adjSlowAnti":4})
    }),
    51000046: _tools.RODict({
        "propID": 51000046,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":771,"adjMinPhysicalAtk":700,"adjMaxPhysicalAtk":700,"adjMinMagicAtk":700,"adjMaxMagicAtk":700,"adjMinPhysicalArmor":370,"adjMaxPhysicalArmor":370,"adjMinMagicArmor":370,"adjMaxMagicArmor":370,"adjAccuracy":16,"adjEvasion":12,"adjFatal":22,"adjAntiFatal":20,"adjIgnoreArmor":0.06,"adjDmgArmor":0.016,"adjMortal":0.16,"adjAntiMortal":0.0448,"adjRealDmg":46,"adjRealDmgDef":46,"adjMonsterDmg":0.01,"adjFinalDmg":0.0743,"adjFinalDmgAnti":0.0243,"adjStunEnh":5,"adjStunAnti":5,"adjSilentEnh":5,"adjSilentAnti":5,"adjKnockEnh":5,"adjKnockAnti":5,"adjFrozenEnh":5,"adjFrozenAnti":5,"adjSlowEnh":5,"adjSlowAnti":5})
    }),
    51000047: _tools.RODict({
        "propID": 51000047,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":789,"adjMinPhysicalAtk":714,"adjMaxPhysicalAtk":714,"adjMinMagicAtk":714,"adjMaxMagicAtk":714,"adjMinPhysicalArmor":379,"adjMaxPhysicalArmor":379,"adjMinMagicArmor":379,"adjMaxMagicArmor":379,"adjAccuracy":17,"adjEvasion":13,"adjFatal":22,"adjAntiFatal":20,"adjIgnoreArmor":0.0615,"adjDmgArmor":0.016,"adjMortal":0.1625,"adjAntiMortal":0.0476,"adjRealDmg":47,"adjRealDmgDef":47,"adjMonsterDmg":0.01,"adjFinalDmg":0.0749,"adjFinalDmgAnti":0.0249,"adjStunEnh":5,"adjStunAnti":5,"adjSilentEnh":5,"adjSilentAnti":5,"adjKnockEnh":5,"adjKnockAnti":5,"adjFrozenEnh":5,"adjFrozenAnti":5,"adjSlowEnh":5,"adjSlowAnti":5})
    }),
    51000048: _tools.RODict({
        "propID": 51000048,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":807,"adjMinPhysicalAtk":733,"adjMaxPhysicalAtk":733,"adjMinMagicAtk":733,"adjMaxMagicAtk":733,"adjMinPhysicalArmor":388,"adjMaxPhysicalArmor":388,"adjMinMagicArmor":388,"adjMaxMagicArmor":388,"adjAccuracy":18,"adjEvasion":13,"adjFatal":22,"adjAntiFatal":21,"adjIgnoreArmor":0.063,"adjDmgArmor":0.016,"adjMortal":0.165,"adjAntiMortal":0.0504,"adjRealDmg":48,"adjRealDmgDef":48,"adjMonsterDmg":0.01,"adjFinalDmg":0.0755,"adjFinalDmgAnti":0.0255,"adjStunEnh":5,"adjStunAnti":5,"adjSilentEnh":5,"adjSilentAnti":5,"adjKnockEnh":5,"adjKnockAnti":5,"adjFrozenEnh":5,"adjFrozenAnti":5,"adjSlowEnh":5,"adjSlowAnti":5})
    }),
    51000049: _tools.RODict({
        "propID": 51000049,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":825,"adjMinPhysicalAtk":752,"adjMaxPhysicalAtk":752,"adjMinMagicAtk":752,"adjMaxMagicAtk":752,"adjMinPhysicalArmor":397,"adjMaxPhysicalArmor":397,"adjMinMagicArmor":397,"adjMaxMagicArmor":397,"adjAccuracy":18,"adjEvasion":14,"adjFatal":23,"adjAntiFatal":21,"adjIgnoreArmor":0.0645,"adjDmgArmor":0.016,"adjMortal":0.1675,"adjAntiMortal":0.0532,"adjRealDmg":49,"adjRealDmgDef":49,"adjMonsterDmg":0.01,"adjFinalDmg":0.0761,"adjFinalDmgAnti":0.0261,"adjStunEnh":5,"adjStunAnti":5,"adjSilentEnh":5,"adjSilentAnti":5,"adjKnockEnh":5,"adjKnockAnti":5,"adjFrozenEnh":5,"adjFrozenAnti":5,"adjSlowEnh":5,"adjSlowAnti":5})
    }),
    51000050: _tools.RODict({
        "propID": 51000050,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":844,"adjMinPhysicalAtk":771,"adjMaxPhysicalAtk":771,"adjMinMagicAtk":771,"adjMaxMagicAtk":771,"adjMinPhysicalArmor":406,"adjMaxPhysicalArmor":406,"adjMinMagicArmor":406,"adjMaxMagicArmor":406,"adjAccuracy":19,"adjEvasion":15,"adjFatal":23,"adjAntiFatal":21,"adjIgnoreArmor":0.066,"adjDmgArmor":0.016,"adjMortal":0.17,"adjAntiMortal":0.056,"adjRealDmg":50,"adjRealDmgDef":50,"adjMonsterDmg":0.01,"adjFinalDmg":0.0767,"adjFinalDmgAnti":0.0267,"adjStunEnh":5,"adjStunAnti":5,"adjSilentEnh":5,"adjSilentAnti":5,"adjKnockEnh":5,"adjKnockAnti":5,"adjFrozenEnh":5,"adjFrozenAnti":5,"adjSlowEnh":5,"adjSlowAnti":5})
    }),
    51000051: _tools.RODict({
        "propID": 51000051,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":862,"adjMinPhysicalAtk":800,"adjMaxPhysicalAtk":800,"adjMinMagicAtk":800,"adjMaxMagicAtk":800,"adjMinPhysicalArmor":418,"adjMaxPhysicalArmor":418,"adjMinMagicArmor":418,"adjMaxMagicArmor":418,"adjAccuracy":20,"adjEvasion":15,"adjFatal":24,"adjAntiFatal":22,"adjIgnoreArmor":0.0668,"adjDmgArmor":0.0168,"adjMortal":0.176,"adjAntiMortal":0.056,"adjRealDmg":51,"adjRealDmgDef":51,"adjMonsterDmg":0.01,"adjFinalDmg":0.0776,"adjFinalDmgAnti":0.0276,"adjStunEnh":6,"adjStunAnti":6,"adjSilentEnh":6,"adjSilentAnti":6,"adjKnockEnh":6,"adjKnockAnti":6,"adjFrozenEnh":6,"adjFrozenAnti":6,"adjSlowEnh":6,"adjSlowAnti":6})
    }),
    51000052: _tools.RODict({
        "propID": 51000052,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":881,"adjMinPhysicalAtk":831,"adjMaxPhysicalAtk":831,"adjMinMagicAtk":831,"adjMaxMagicAtk":831,"adjMinPhysicalArmor":430,"adjMaxPhysicalArmor":430,"adjMinMagicArmor":430,"adjMaxMagicArmor":430,"adjAccuracy":21,"adjEvasion":16,"adjFatal":24,"adjAntiFatal":22,"adjIgnoreArmor":0.0676,"adjDmgArmor":0.0176,"adjMortal":0.182,"adjAntiMortal":0.056,"adjRealDmg":52,"adjRealDmgDef":52,"adjMonsterDmg":0.01,"adjFinalDmg":0.0785,"adjFinalDmgAnti":0.0285,"adjStunEnh":6,"adjStunAnti":6,"adjSilentEnh":6,"adjSilentAnti":6,"adjKnockEnh":6,"adjKnockAnti":6,"adjFrozenEnh":6,"adjFrozenAnti":6,"adjSlowEnh":6,"adjSlowAnti":6})
    }),
    51000053: _tools.RODict({
        "propID": 51000053,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":899,"adjMinPhysicalAtk":855,"adjMaxPhysicalAtk":855,"adjMinMagicAtk":855,"adjMaxMagicAtk":855,"adjMinPhysicalArmor":442,"adjMaxPhysicalArmor":442,"adjMinMagicArmor":442,"adjMaxMagicArmor":442,"adjAccuracy":22,"adjEvasion":17,"adjFatal":24,"adjAntiFatal":22,"adjIgnoreArmor":0.0684,"adjDmgArmor":0.0184,"adjMortal":0.188,"adjAntiMortal":0.056,"adjRealDmg":53,"adjRealDmgDef":53,"adjMonsterDmg":0.01,"adjFinalDmg":0.0795,"adjFinalDmgAnti":0.0295,"adjStunEnh":6,"adjStunAnti":6,"adjSilentEnh":6,"adjSilentAnti":6,"adjKnockEnh":6,"adjKnockAnti":6,"adjFrozenEnh":6,"adjFrozenAnti":6,"adjSlowEnh":6,"adjSlowAnti":6})
    }),
    51000054: _tools.RODict({
        "propID": 51000054,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":918,"adjMinPhysicalAtk":886,"adjMaxPhysicalAtk":886,"adjMinMagicAtk":886,"adjMaxMagicAtk":886,"adjMinPhysicalArmor":454,"adjMaxPhysicalArmor":454,"adjMinMagicArmor":454,"adjMaxMagicArmor":454,"adjAccuracy":23,"adjEvasion":18,"adjFatal":25,"adjAntiFatal":23,"adjIgnoreArmor":0.0692,"adjDmgArmor":0.0192,"adjMortal":0.194,"adjAntiMortal":0.056,"adjRealDmg":54,"adjRealDmgDef":54,"adjMonsterDmg":0.01,"adjFinalDmg":0.0804,"adjFinalDmgAnti":0.0304,"adjStunEnh":6,"adjStunAnti":6,"adjSilentEnh":6,"adjSilentAnti":6,"adjKnockEnh":6,"adjKnockAnti":6,"adjFrozenEnh":6,"adjFrozenAnti":6,"adjSlowEnh":6,"adjSlowAnti":6})
    }),
    51000055: _tools.RODict({
        "propID": 51000055,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":938,"adjMinPhysicalAtk":911,"adjMaxPhysicalAtk":911,"adjMinMagicAtk":911,"adjMaxMagicAtk":911,"adjMinPhysicalArmor":466,"adjMaxPhysicalArmor":466,"adjMinMagicArmor":466,"adjMaxMagicArmor":466,"adjAccuracy":23,"adjEvasion":18,"adjFatal":25,"adjAntiFatal":23,"adjIgnoreArmor":0.07,"adjDmgArmor":0.02,"adjMortal":0.2,"adjAntiMortal":0.056,"adjRealDmg":55,"adjRealDmgDef":55,"adjMonsterDmg":0.01,"adjFinalDmg":0.0813,"adjFinalDmgAnti":0.0313,"adjStunEnh":7,"adjStunAnti":7,"adjSilentEnh":7,"adjSilentAnti":7,"adjKnockEnh":7,"adjKnockAnti":7,"adjFrozenEnh":7,"adjFrozenAnti":7,"adjSlowEnh":7,"adjSlowAnti":7})
    }),
    51000056: _tools.RODict({
        "propID": 51000056,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":957,"adjMinPhysicalAtk":943,"adjMaxPhysicalAtk":943,"adjMinMagicAtk":943,"adjMaxMagicAtk":943,"adjMinPhysicalArmor":478,"adjMaxPhysicalArmor":478,"adjMinMagicArmor":478,"adjMaxMagicArmor":478,"adjAccuracy":24,"adjEvasion":19,"adjFatal":25,"adjAntiFatal":23,"adjIgnoreArmor":0.0708,"adjDmgArmor":0.0208,"adjMortal":0.206,"adjAntiMortal":0.056,"adjRealDmg":56,"adjRealDmgDef":56,"adjMonsterDmg":0.01,"adjFinalDmg":0.0823,"adjFinalDmgAnti":0.0323,"adjStunEnh":7,"adjStunAnti":7,"adjSilentEnh":7,"adjSilentAnti":7,"adjKnockEnh":7,"adjKnockAnti":7,"adjFrozenEnh":7,"adjFrozenAnti":7,"adjSlowEnh":7,"adjSlowAnti":7})
    }),
    51000057: _tools.RODict({
        "propID": 51000057,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":977,"adjMinPhysicalAtk":969,"adjMaxPhysicalAtk":969,"adjMinMagicAtk":969,"adjMaxMagicAtk":969,"adjMinPhysicalArmor":490,"adjMaxPhysicalArmor":490,"adjMinMagicArmor":490,"adjMaxMagicArmor":490,"adjAccuracy":25,"adjEvasion":20,"adjFatal":26,"adjAntiFatal":23,"adjIgnoreArmor":0.0716,"adjDmgArmor":0.0216,"adjMortal":0.212,"adjAntiMortal":0.056,"adjRealDmg":57,"adjRealDmgDef":57,"adjMonsterDmg":0.01,"adjFinalDmg":0.0832,"adjFinalDmgAnti":0.0332,"adjStunEnh":7,"adjStunAnti":7,"adjSilentEnh":7,"adjSilentAnti":7,"adjKnockEnh":7,"adjKnockAnti":7,"adjFrozenEnh":7,"adjFrozenAnti":7,"adjSlowEnh":7,"adjSlowAnti":7})
    }),
    51000058: _tools.RODict({
        "propID": 51000058,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":997,"adjMinPhysicalAtk":994,"adjMaxPhysicalAtk":994,"adjMinMagicAtk":994,"adjMaxMagicAtk":994,"adjMinPhysicalArmor":502,"adjMaxPhysicalArmor":502,"adjMinMagicArmor":502,"adjMaxMagicArmor":502,"adjAccuracy":26,"adjEvasion":21,"adjFatal":26,"adjAntiFatal":24,"adjIgnoreArmor":0.0724,"adjDmgArmor":0.0224,"adjMortal":0.218,"adjAntiMortal":0.056,"adjRealDmg":58,"adjRealDmgDef":58,"adjMonsterDmg":0.01,"adjFinalDmg":0.0841,"adjFinalDmgAnti":0.0341,"adjStunEnh":7,"adjStunAnti":7,"adjSilentEnh":7,"adjSilentAnti":7,"adjKnockEnh":7,"adjKnockAnti":7,"adjFrozenEnh":7,"adjFrozenAnti":7,"adjSlowEnh":7,"adjSlowAnti":7})
    }),
    51000059: _tools.RODict({
        "propID": 51000059,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1017,"adjMinPhysicalAtk":1020,"adjMaxPhysicalAtk":1020,"adjMinMagicAtk":1020,"adjMaxMagicAtk":1020,"adjMinPhysicalArmor":514,"adjMaxPhysicalArmor":514,"adjMinMagicArmor":514,"adjMaxMagicArmor":514,"adjAccuracy":27,"adjEvasion":21,"adjFatal":27,"adjAntiFatal":24,"adjIgnoreArmor":0.0732,"adjDmgArmor":0.0232,"adjMortal":0.224,"adjAntiMortal":0.056,"adjRealDmg":59,"adjRealDmgDef":59,"adjMonsterDmg":0.01,"adjFinalDmg":0.0851,"adjFinalDmgAnti":0.0351,"adjStunEnh":7,"adjStunAnti":7,"adjSilentEnh":7,"adjSilentAnti":7,"adjKnockEnh":7,"adjKnockAnti":7,"adjFrozenEnh":7,"adjFrozenAnti":7,"adjSlowEnh":7,"adjSlowAnti":7})
    }),
    51000060: _tools.RODict({
        "propID": 51000060,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1037,"adjMinPhysicalAtk":1054,"adjMaxPhysicalAtk":1054,"adjMinMagicAtk":1054,"adjMaxMagicAtk":1054,"adjMinPhysicalArmor":526,"adjMaxPhysicalArmor":526,"adjMinMagicArmor":526,"adjMaxMagicArmor":526,"adjAccuracy":28,"adjEvasion":22,"adjFatal":27,"adjAntiFatal":24,"adjIgnoreArmor":0.074,"adjDmgArmor":0.024,"adjMortal":0.23,"adjAntiMortal":0.056,"adjRealDmg":60,"adjRealDmgDef":60,"adjMonsterDmg":0.01,"adjFinalDmg":0.086,"adjFinalDmgAnti":0.036,"adjStunEnh":8,"adjStunAnti":8,"adjSilentEnh":8,"adjSilentAnti":8,"adjKnockEnh":8,"adjKnockAnti":8,"adjFrozenEnh":8,"adjFrozenAnti":8,"adjSlowEnh":8,"adjSlowAnti":8})
    }),
    51000061: _tools.RODict({
        "propID": 51000061,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1057,"adjMinPhysicalAtk":1077,"adjMaxPhysicalAtk":1077,"adjMinMagicAtk":1077,"adjMaxMagicAtk":1077,"adjMinPhysicalArmor":537,"adjMaxPhysicalArmor":537,"adjMinMagicArmor":537,"adjMaxMagicArmor":537,"adjAccuracy":28,"adjEvasion":23,"adjFatal":27,"adjAntiFatal":24,"adjIgnoreArmor":0.074,"adjDmgArmor":0.024,"adjMortal":0.23,"adjAntiMortal":0.0563,"adjRealDmg":61,"adjRealDmgDef":61,"adjMonsterDmg":0.01,"adjFinalDmg":0.087,"adjFinalDmgAnti":0.037,"adjStunEnh":8,"adjStunAnti":8,"adjSilentEnh":8,"adjSilentAnti":8,"adjKnockEnh":8,"adjKnockAnti":8,"adjFrozenEnh":8,"adjFrozenAnti":8,"adjSlowEnh":8,"adjSlowAnti":8})
    }),
    51000062: _tools.RODict({
        "propID": 51000062,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1077,"adjMinPhysicalAtk":1107,"adjMaxPhysicalAtk":1107,"adjMinMagicAtk":1107,"adjMaxMagicAtk":1107,"adjMinPhysicalArmor":548,"adjMaxPhysicalArmor":548,"adjMinMagicArmor":548,"adjMaxMagicArmor":548,"adjAccuracy":29,"adjEvasion":23,"adjFatal":27,"adjAntiFatal":25,"adjIgnoreArmor":0.074,"adjDmgArmor":0.024,"adjMortal":0.23,"adjAntiMortal":0.0566,"adjRealDmg":62,"adjRealDmgDef":62,"adjMonsterDmg":0.01,"adjFinalDmg":0.088,"adjFinalDmgAnti":0.038,"adjStunEnh":8,"adjStunAnti":8,"adjSilentEnh":8,"adjSilentAnti":8,"adjKnockEnh":8,"adjKnockAnti":8,"adjFrozenEnh":8,"adjFrozenAnti":8,"adjSlowEnh":8,"adjSlowAnti":8})
    }),
    51000063: _tools.RODict({
        "propID": 51000063,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1097,"adjMinPhysicalAtk":1138,"adjMaxPhysicalAtk":1138,"adjMinMagicAtk":1138,"adjMaxMagicAtk":1138,"adjMinPhysicalArmor":559,"adjMaxPhysicalArmor":559,"adjMinMagicArmor":559,"adjMaxMagicArmor":559,"adjAccuracy":30,"adjEvasion":24,"adjFatal":27,"adjAntiFatal":25,"adjIgnoreArmor":0.074,"adjDmgArmor":0.024,"adjMortal":0.23,"adjAntiMortal":0.0569,"adjRealDmg":63,"adjRealDmgDef":63,"adjMonsterDmg":0.01,"adjFinalDmg":0.089,"adjFinalDmgAnti":0.039,"adjStunEnh":9,"adjStunAnti":9,"adjSilentEnh":9,"adjSilentAnti":9,"adjKnockEnh":9,"adjKnockAnti":9,"adjFrozenEnh":9,"adjFrozenAnti":9,"adjSlowEnh":9,"adjSlowAnti":9})
    }),
    51000064: _tools.RODict({
        "propID": 51000064,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1117,"adjMinPhysicalAtk":1169,"adjMaxPhysicalAtk":1169,"adjMinMagicAtk":1169,"adjMaxMagicAtk":1169,"adjMinPhysicalArmor":570,"adjMaxPhysicalArmor":570,"adjMinMagicArmor":570,"adjMaxMagicArmor":570,"adjAccuracy":31,"adjEvasion":24,"adjFatal":28,"adjAntiFatal":25,"adjIgnoreArmor":0.074,"adjDmgArmor":0.024,"adjMortal":0.23,"adjAntiMortal":0.0572,"adjRealDmg":64,"adjRealDmgDef":64,"adjMonsterDmg":0.01,"adjFinalDmg":0.09,"adjFinalDmgAnti":0.04,"adjStunEnh":9,"adjStunAnti":9,"adjSilentEnh":9,"adjSilentAnti":9,"adjKnockEnh":9,"adjKnockAnti":9,"adjFrozenEnh":9,"adjFrozenAnti":9,"adjSlowEnh":9,"adjSlowAnti":9})
    }),
    51000065: _tools.RODict({
        "propID": 51000065,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1138,"adjMinPhysicalAtk":1200,"adjMaxPhysicalAtk":1200,"adjMinMagicAtk":1200,"adjMaxMagicAtk":1200,"adjMinPhysicalArmor":582,"adjMaxPhysicalArmor":582,"adjMinMagicArmor":582,"adjMaxMagicArmor":582,"adjAccuracy":31,"adjEvasion":25,"adjFatal":28,"adjAntiFatal":25,"adjIgnoreArmor":0.074,"adjDmgArmor":0.024,"adjMortal":0.23,"adjAntiMortal":0.0575,"adjRealDmg":65,"adjRealDmgDef":65,"adjMonsterDmg":0.01,"adjFinalDmg":0.091,"adjFinalDmgAnti":0.041,"adjStunEnh":9,"adjStunAnti":9,"adjSilentEnh":9,"adjSilentAnti":9,"adjKnockEnh":9,"adjKnockAnti":9,"adjFrozenEnh":9,"adjFrozenAnti":9,"adjSlowEnh":9,"adjSlowAnti":9})
    }),
    51000066: _tools.RODict({
        "propID": 51000066,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1159,"adjMinPhysicalAtk":1231,"adjMaxPhysicalAtk":1231,"adjMinMagicAtk":1231,"adjMaxMagicAtk":1231,"adjMinPhysicalArmor":593,"adjMaxPhysicalArmor":593,"adjMinMagicArmor":593,"adjMaxMagicArmor":593,"adjAccuracy":32,"adjEvasion":26,"adjFatal":28,"adjAntiFatal":25,"adjIgnoreArmor":0.074,"adjDmgArmor":0.024,"adjMortal":0.23,"adjAntiMortal":0.0578,"adjRealDmg":66,"adjRealDmgDef":66,"adjMonsterDmg":0.01,"adjFinalDmg":0.092,"adjFinalDmgAnti":0.042,"adjStunEnh":9,"adjStunAnti":9,"adjSilentEnh":9,"adjSilentAnti":9,"adjKnockEnh":9,"adjKnockAnti":9,"adjFrozenEnh":9,"adjFrozenAnti":9,"adjSlowEnh":9,"adjSlowAnti":9})
    }),
    51000067: _tools.RODict({
        "propID": 51000067,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1180,"adjMinPhysicalAtk":1263,"adjMaxPhysicalAtk":1263,"adjMinMagicAtk":1263,"adjMaxMagicAtk":1263,"adjMinPhysicalArmor":604,"adjMaxPhysicalArmor":604,"adjMinMagicArmor":604,"adjMaxMagicArmor":604,"adjAccuracy":33,"adjEvasion":26,"adjFatal":28,"adjAntiFatal":25,"adjIgnoreArmor":0.074,"adjDmgArmor":0.024,"adjMortal":0.23,"adjAntiMortal":0.0581,"adjRealDmg":67,"adjRealDmgDef":67,"adjMonsterDmg":0.01,"adjFinalDmg":0.093,"adjFinalDmgAnti":0.043,"adjStunEnh":10,"adjStunAnti":10,"adjSilentEnh":10,"adjSilentAnti":10,"adjKnockEnh":10,"adjKnockAnti":10,"adjFrozenEnh":10,"adjFrozenAnti":10,"adjSlowEnh":10,"adjSlowAnti":10})
    }),
    51000068: _tools.RODict({
        "propID": 51000068,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1201,"adjMinPhysicalAtk":1296,"adjMaxPhysicalAtk":1296,"adjMinMagicAtk":1296,"adjMaxMagicAtk":1296,"adjMinPhysicalArmor":615,"adjMaxPhysicalArmor":615,"adjMinMagicArmor":615,"adjMaxMagicArmor":615,"adjAccuracy":34,"adjEvasion":27,"adjFatal":28,"adjAntiFatal":25,"adjIgnoreArmor":0.074,"adjDmgArmor":0.024,"adjMortal":0.23,"adjAntiMortal":0.0584,"adjRealDmg":68,"adjRealDmgDef":68,"adjMonsterDmg":0.01,"adjFinalDmg":0.094,"adjFinalDmgAnti":0.044,"adjStunEnh":10,"adjStunAnti":10,"adjSilentEnh":10,"adjSilentAnti":10,"adjKnockEnh":10,"adjKnockAnti":10,"adjFrozenEnh":10,"adjFrozenAnti":10,"adjSlowEnh":10,"adjSlowAnti":10})
    }),
    51000069: _tools.RODict({
        "propID": 51000069,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1222,"adjMinPhysicalAtk":1328,"adjMaxPhysicalAtk":1328,"adjMinMagicAtk":1328,"adjMaxMagicAtk":1328,"adjMinPhysicalArmor":627,"adjMaxPhysicalArmor":627,"adjMinMagicArmor":627,"adjMaxMagicArmor":627,"adjAccuracy":34,"adjEvasion":27,"adjFatal":28,"adjAntiFatal":26,"adjIgnoreArmor":0.074,"adjDmgArmor":0.024,"adjMortal":0.23,"adjAntiMortal":0.0587,"adjRealDmg":69,"adjRealDmgDef":69,"adjMonsterDmg":0.01,"adjFinalDmg":0.095,"adjFinalDmgAnti":0.045,"adjStunEnh":10,"adjStunAnti":10,"adjSilentEnh":10,"adjSilentAnti":10,"adjKnockEnh":10,"adjKnockAnti":10,"adjFrozenEnh":10,"adjFrozenAnti":10,"adjSlowEnh":10,"adjSlowAnti":10})
    }),
    51000070: _tools.RODict({
        "propID": 51000070,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1244,"adjMinPhysicalAtk":1362,"adjMaxPhysicalAtk":1362,"adjMinMagicAtk":1362,"adjMaxMagicAtk":1362,"adjMinPhysicalArmor":638,"adjMaxPhysicalArmor":638,"adjMinMagicArmor":638,"adjMaxMagicArmor":638,"adjAccuracy":35,"adjEvasion":28,"adjFatal":29,"adjAntiFatal":26,"adjIgnoreArmor":0.074,"adjDmgArmor":0.024,"adjMortal":0.23,"adjAntiMortal":0.059,"adjRealDmg":70,"adjRealDmgDef":70,"adjMonsterDmg":0.01,"adjFinalDmg":0.096,"adjFinalDmgAnti":0.046,"adjStunEnh":10,"adjStunAnti":10,"adjSilentEnh":10,"adjSilentAnti":10,"adjKnockEnh":10,"adjKnockAnti":10,"adjFrozenEnh":10,"adjFrozenAnti":10,"adjSlowEnh":10,"adjSlowAnti":10})
    }),
    51000071: _tools.RODict({
        "propID": 51000071,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1270,"adjMinPhysicalAtk":1382,"adjMaxPhysicalAtk":1382,"adjMinMagicAtk":1382,"adjMaxMagicAtk":1382,"adjMinPhysicalArmor":649,"adjMaxPhysicalArmor":649,"adjMinMagicArmor":649,"adjMaxMagicArmor":649,"adjAccuracy":35,"adjEvasion":28,"adjFatal":29,"adjAntiFatal":26,"adjIgnoreArmor":0.076,"adjDmgArmor":0.024,"adjMortal":0.23,"adjAntiMortal":0.059,"adjRealDmg":71,"adjRealDmgDef":71,"adjMonsterDmg":0.01,"adjFinalDmg":0.1003,"adjFinalDmgAnti":0.0473,"adjStunEnh":11,"adjStunAnti":11,"adjSilentEnh":11,"adjSilentAnti":11,"adjKnockEnh":11,"adjKnockAnti":11,"adjFrozenEnh":11,"adjFrozenAnti":11,"adjSlowEnh":11,"adjSlowAnti":11})
    }),
    51000072: _tools.RODict({
        "propID": 51000072,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1297,"adjMinPhysicalAtk":1413,"adjMaxPhysicalAtk":1413,"adjMinMagicAtk":1413,"adjMaxMagicAtk":1413,"adjMinPhysicalArmor":660,"adjMaxPhysicalArmor":660,"adjMinMagicArmor":660,"adjMaxMagicArmor":660,"adjAccuracy":35,"adjEvasion":28,"adjFatal":29,"adjAntiFatal":26,"adjIgnoreArmor":0.078,"adjDmgArmor":0.024,"adjMortal":0.23,"adjAntiMortal":0.059,"adjRealDmg":72,"adjRealDmgDef":72,"adjMonsterDmg":0.01,"adjFinalDmg":0.1046,"adjFinalDmgAnti":0.0486,"adjStunEnh":11,"adjStunAnti":11,"adjSilentEnh":11,"adjSilentAnti":11,"adjKnockEnh":11,"adjKnockAnti":11,"adjFrozenEnh":11,"adjFrozenAnti":11,"adjSlowEnh":11,"adjSlowAnti":11})
    }),
    51000073: _tools.RODict({
        "propID": 51000073,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1325,"adjMinPhysicalAtk":1444,"adjMaxPhysicalAtk":1444,"adjMinMagicAtk":1444,"adjMaxMagicAtk":1444,"adjMinPhysicalArmor":672,"adjMaxPhysicalArmor":672,"adjMinMagicArmor":672,"adjMaxMagicArmor":672,"adjAccuracy":35,"adjEvasion":28,"adjFatal":29,"adjAntiFatal":26,"adjIgnoreArmor":0.08,"adjDmgArmor":0.024,"adjMortal":0.23,"adjAntiMortal":0.059,"adjRealDmg":73,"adjRealDmgDef":73,"adjMonsterDmg":0.01,"adjFinalDmg":0.1089,"adjFinalDmgAnti":0.0499,"adjStunEnh":11,"adjStunAnti":11,"adjSilentEnh":11,"adjSilentAnti":11,"adjKnockEnh":11,"adjKnockAnti":11,"adjFrozenEnh":11,"adjFrozenAnti":11,"adjSlowEnh":11,"adjSlowAnti":11})
    }),
    51000074: _tools.RODict({
        "propID": 51000074,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1353,"adjMinPhysicalAtk":1476,"adjMaxPhysicalAtk":1476,"adjMinMagicAtk":1476,"adjMaxMagicAtk":1476,"adjMinPhysicalArmor":683,"adjMaxPhysicalArmor":683,"adjMinMagicArmor":683,"adjMaxMagicArmor":683,"adjAccuracy":35,"adjEvasion":28,"adjFatal":29,"adjAntiFatal":26,"adjIgnoreArmor":0.082,"adjDmgArmor":0.024,"adjMortal":0.23,"adjAntiMortal":0.059,"adjRealDmg":74,"adjRealDmgDef":74,"adjMonsterDmg":0.01,"adjFinalDmg":0.1132,"adjFinalDmgAnti":0.0512,"adjStunEnh":11,"adjStunAnti":11,"adjSilentEnh":11,"adjSilentAnti":11,"adjKnockEnh":11,"adjKnockAnti":11,"adjFrozenEnh":11,"adjFrozenAnti":11,"adjSlowEnh":11,"adjSlowAnti":11})
    }),
    51000075: _tools.RODict({
        "propID": 51000075,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1381,"adjMinPhysicalAtk":1508,"adjMaxPhysicalAtk":1508,"adjMinMagicAtk":1508,"adjMaxMagicAtk":1508,"adjMinPhysicalArmor":694,"adjMaxPhysicalArmor":694,"adjMinMagicArmor":694,"adjMaxMagicArmor":694,"adjAccuracy":35,"adjEvasion":28,"adjFatal":29,"adjAntiFatal":26,"adjIgnoreArmor":0.084,"adjDmgArmor":0.024,"adjMortal":0.23,"adjAntiMortal":0.059,"adjRealDmg":75,"adjRealDmgDef":75,"adjMonsterDmg":0.01,"adjFinalDmg":0.1175,"adjFinalDmgAnti":0.0525,"adjStunEnh":12,"adjStunAnti":12,"adjSilentEnh":12,"adjSilentAnti":12,"adjKnockEnh":12,"adjKnockAnti":12,"adjFrozenEnh":12,"adjFrozenAnti":12,"adjSlowEnh":12,"adjSlowAnti":12})
    }),
    51000076: _tools.RODict({
        "propID": 51000076,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1410,"adjMinPhysicalAtk":1536,"adjMaxPhysicalAtk":1536,"adjMinMagicAtk":1536,"adjMaxMagicAtk":1536,"adjMinPhysicalArmor":706,"adjMaxPhysicalArmor":706,"adjMinMagicArmor":706,"adjMaxMagicArmor":706,"adjAccuracy":35,"adjEvasion":28,"adjFatal":29,"adjAntiFatal":26,"adjIgnoreArmor":0.086,"adjDmgArmor":0.024,"adjMortal":0.23,"adjAntiMortal":0.059,"adjRealDmg":76,"adjRealDmgDef":76,"adjMonsterDmg":0.01,"adjFinalDmg":0.1218,"adjFinalDmgAnti":0.0538,"adjStunEnh":12,"adjStunAnti":12,"adjSilentEnh":12,"adjSilentAnti":12,"adjKnockEnh":12,"adjKnockAnti":12,"adjFrozenEnh":12,"adjFrozenAnti":12,"adjSlowEnh":12,"adjSlowAnti":12})
    }),
    51000077: _tools.RODict({
        "propID": 51000077,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1440,"adjMinPhysicalAtk":1564,"adjMaxPhysicalAtk":1564,"adjMinMagicAtk":1564,"adjMaxMagicAtk":1564,"adjMinPhysicalArmor":717,"adjMaxPhysicalArmor":717,"adjMinMagicArmor":717,"adjMaxMagicArmor":717,"adjAccuracy":35,"adjEvasion":28,"adjFatal":29,"adjAntiFatal":26,"adjIgnoreArmor":0.088,"adjDmgArmor":0.024,"adjMortal":0.23,"adjAntiMortal":0.059,"adjRealDmg":77,"adjRealDmgDef":77,"adjMonsterDmg":0.01,"adjFinalDmg":0.1261,"adjFinalDmgAnti":0.0551,"adjStunEnh":12,"adjStunAnti":12,"adjSilentEnh":12,"adjSilentAnti":12,"adjKnockEnh":12,"adjKnockAnti":12,"adjFrozenEnh":12,"adjFrozenAnti":12,"adjSlowEnh":12,"adjSlowAnti":12})
    }),
    51000078: _tools.RODict({
        "propID": 51000078,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1470,"adjMinPhysicalAtk":1592,"adjMaxPhysicalAtk":1592,"adjMinMagicAtk":1592,"adjMaxMagicAtk":1592,"adjMinPhysicalArmor":728,"adjMaxPhysicalArmor":728,"adjMinMagicArmor":728,"adjMaxMagicArmor":728,"adjAccuracy":35,"adjEvasion":28,"adjFatal":29,"adjAntiFatal":26,"adjIgnoreArmor":0.09,"adjDmgArmor":0.024,"adjMortal":0.23,"adjAntiMortal":0.059,"adjRealDmg":78,"adjRealDmgDef":78,"adjMonsterDmg":0.01,"adjFinalDmg":0.1304,"adjFinalDmgAnti":0.0564,"adjStunEnh":12,"adjStunAnti":12,"adjSilentEnh":12,"adjSilentAnti":12,"adjKnockEnh":12,"adjKnockAnti":12,"adjFrozenEnh":12,"adjFrozenAnti":12,"adjSlowEnh":12,"adjSlowAnti":12})
    }),
    51000079: _tools.RODict({
        "propID": 51000079,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1500,"adjMinPhysicalAtk":1621,"adjMaxPhysicalAtk":1621,"adjMinMagicAtk":1621,"adjMaxMagicAtk":1621,"adjMinPhysicalArmor":740,"adjMaxPhysicalArmor":740,"adjMinMagicArmor":740,"adjMaxMagicArmor":740,"adjAccuracy":35,"adjEvasion":28,"adjFatal":29,"adjAntiFatal":26,"adjIgnoreArmor":0.092,"adjDmgArmor":0.024,"adjMortal":0.23,"adjAntiMortal":0.059,"adjRealDmg":79,"adjRealDmgDef":79,"adjMonsterDmg":0.01,"adjFinalDmg":0.1347,"adjFinalDmgAnti":0.0577,"adjStunEnh":13,"adjStunAnti":13,"adjSilentEnh":13,"adjSilentAnti":13,"adjKnockEnh":13,"adjKnockAnti":13,"adjFrozenEnh":13,"adjFrozenAnti":13,"adjSlowEnh":13,"adjSlowAnti":13})
    }),
    51000080: _tools.RODict({
        "propID": 51000080,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1559,"adjMinPhysicalAtk":1653,"adjMaxPhysicalAtk":1653,"adjMinMagicAtk":1653,"adjMaxMagicAtk":1653,"adjMinPhysicalArmor":751,"adjMaxPhysicalArmor":751,"adjMinMagicArmor":751,"adjMaxMagicArmor":751,"adjAccuracy":35,"adjEvasion":28,"adjFatal":29,"adjAntiFatal":26,"adjIgnoreArmor":0.094,"adjDmgArmor":0.024,"adjMortal":0.23,"adjAntiMortal":0.059,"adjRealDmg":80,"adjRealDmgDef":80,"adjMonsterDmg":0.01,"adjFinalDmg":0.139,"adjFinalDmgAnti":0.059,"adjStunEnh":13,"adjStunAnti":13,"adjSilentEnh":13,"adjSilentAnti":13,"adjKnockEnh":13,"adjKnockAnti":13,"adjFrozenEnh":13,"adjFrozenAnti":13,"adjSlowEnh":13,"adjSlowAnti":13})
    }),
    51000081: _tools.RODict({
        "propID": 51000081,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1598,"adjMinPhysicalAtk":1689,"adjMaxPhysicalAtk":1689,"adjMinMagicAtk":1689,"adjMaxMagicAtk":1689,"adjMinPhysicalArmor":762,"adjMaxPhysicalArmor":762,"adjMinMagicArmor":762,"adjMaxMagicArmor":762,"adjAccuracy":35,"adjEvasion":28,"adjFatal":29,"adjAntiFatal":26,"adjIgnoreArmor":0.097,"adjDmgArmor":0.024,"adjMortal":0.2385,"adjAntiMortal":0.0618,"adjRealDmg":81,"adjRealDmgDef":81,"adjMonsterDmg":0.01,"adjFinalDmg":0.1419,"adjFinalDmgAnti":0.0599,"adjStunEnh":13,"adjStunAnti":13,"adjSilentEnh":13,"adjSilentAnti":13,"adjKnockEnh":13,"adjKnockAnti":13,"adjFrozenEnh":13,"adjFrozenAnti":13,"adjSlowEnh":13,"adjSlowAnti":13})
    }),
    51000082: _tools.RODict({
        "propID": 51000082,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1638,"adjMinPhysicalAtk":1724,"adjMaxPhysicalAtk":1724,"adjMinMagicAtk":1724,"adjMaxMagicAtk":1724,"adjMinPhysicalArmor":772,"adjMaxPhysicalArmor":772,"adjMinMagicArmor":772,"adjMaxMagicArmor":772,"adjAccuracy":35,"adjEvasion":28,"adjFatal":29,"adjAntiFatal":26,"adjIgnoreArmor":0.1,"adjDmgArmor":0.024,"adjMortal":0.247,"adjAntiMortal":0.0646,"adjRealDmg":82,"adjRealDmgDef":82,"adjMonsterDmg":0.01,"adjFinalDmg":0.1448,"adjFinalDmgAnti":0.0608,"adjStunEnh":13,"adjStunAnti":13,"adjSilentEnh":13,"adjSilentAnti":13,"adjKnockEnh":13,"adjKnockAnti":13,"adjFrozenEnh":13,"adjFrozenAnti":13,"adjSlowEnh":13,"adjSlowAnti":13})
    }),
    51000083: _tools.RODict({
        "propID": 51000083,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1678,"adjMinPhysicalAtk":1760,"adjMaxPhysicalAtk":1760,"adjMinMagicAtk":1760,"adjMaxMagicAtk":1760,"adjMinPhysicalArmor":783,"adjMaxPhysicalArmor":783,"adjMinMagicArmor":783,"adjMaxMagicArmor":783,"adjAccuracy":35,"adjEvasion":28,"adjFatal":29,"adjAntiFatal":26,"adjIgnoreArmor":0.103,"adjDmgArmor":0.024,"adjMortal":0.2555,"adjAntiMortal":0.0674,"adjRealDmg":83,"adjRealDmgDef":83,"adjMonsterDmg":0.01,"adjFinalDmg":0.1477,"adjFinalDmgAnti":0.0617,"adjStunEnh":14,"adjStunAnti":14,"adjSilentEnh":14,"adjSilentAnti":14,"adjKnockEnh":14,"adjKnockAnti":14,"adjFrozenEnh":14,"adjFrozenAnti":14,"adjSlowEnh":14,"adjSlowAnti":14})
    }),
    51000084: _tools.RODict({
        "propID": 51000084,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1720,"adjMinPhysicalAtk":1796,"adjMaxPhysicalAtk":1796,"adjMinMagicAtk":1796,"adjMaxMagicAtk":1796,"adjMinPhysicalArmor":793,"adjMaxPhysicalArmor":793,"adjMinMagicArmor":793,"adjMaxMagicArmor":793,"adjAccuracy":35,"adjEvasion":28,"adjFatal":30,"adjAntiFatal":27,"adjIgnoreArmor":0.106,"adjDmgArmor":0.024,"adjMortal":0.264,"adjAntiMortal":0.0702,"adjRealDmg":84,"adjRealDmgDef":84,"adjMonsterDmg":0.01,"adjFinalDmg":0.1506,"adjFinalDmgAnti":0.0626,"adjStunEnh":14,"adjStunAnti":14,"adjSilentEnh":14,"adjSilentAnti":14,"adjKnockEnh":14,"adjKnockAnti":14,"adjFrozenEnh":14,"adjFrozenAnti":14,"adjSlowEnh":14,"adjSlowAnti":14})
    }),
    51000085: _tools.RODict({
        "propID": 51000085,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1762,"adjMinPhysicalAtk":1833,"adjMaxPhysicalAtk":1833,"adjMinMagicAtk":1833,"adjMaxMagicAtk":1833,"adjMinPhysicalArmor":804,"adjMaxPhysicalArmor":804,"adjMinMagicArmor":804,"adjMaxMagicArmor":804,"adjAccuracy":35,"adjEvasion":28,"adjFatal":30,"adjAntiFatal":27,"adjIgnoreArmor":0.109,"adjDmgArmor":0.024,"adjMortal":0.2725,"adjAntiMortal":0.073,"adjRealDmg":85,"adjRealDmgDef":85,"adjMonsterDmg":0.01,"adjFinalDmg":0.1535,"adjFinalDmgAnti":0.0635,"adjStunEnh":14,"adjStunAnti":14,"adjSilentEnh":14,"adjSilentAnti":14,"adjKnockEnh":14,"adjKnockAnti":14,"adjFrozenEnh":14,"adjFrozenAnti":14,"adjSlowEnh":14,"adjSlowAnti":14})
    }),
    51000086: _tools.RODict({
        "propID": 51000086,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1804,"adjMinPhysicalAtk":1866,"adjMaxPhysicalAtk":1866,"adjMinMagicAtk":1866,"adjMaxMagicAtk":1866,"adjMinPhysicalArmor":815,"adjMaxPhysicalArmor":815,"adjMinMagicArmor":815,"adjMaxMagicArmor":815,"adjAccuracy":35,"adjEvasion":28,"adjFatal":30,"adjAntiFatal":27,"adjIgnoreArmor":0.112,"adjDmgArmor":0.024,"adjMortal":0.281,"adjAntiMortal":0.0758,"adjRealDmg":86,"adjRealDmgDef":86,"adjMonsterDmg":0.01,"adjFinalDmg":0.1564,"adjFinalDmgAnti":0.0644,"adjStunEnh":14,"adjStunAnti":14,"adjSilentEnh":14,"adjSilentAnti":14,"adjKnockEnh":14,"adjKnockAnti":14,"adjFrozenEnh":14,"adjFrozenAnti":14,"adjSlowEnh":14,"adjSlowAnti":14})
    }),
    51000087: _tools.RODict({
        "propID": 51000087,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1848,"adjMinPhysicalAtk":1899,"adjMaxPhysicalAtk":1899,"adjMinMagicAtk":1899,"adjMaxMagicAtk":1899,"adjMinPhysicalArmor":825,"adjMaxPhysicalArmor":825,"adjMinMagicArmor":825,"adjMaxMagicArmor":825,"adjAccuracy":35,"adjEvasion":28,"adjFatal":31,"adjAntiFatal":28,"adjIgnoreArmor":0.115,"adjDmgArmor":0.024,"adjMortal":0.2895,"adjAntiMortal":0.0786,"adjRealDmg":87,"adjRealDmgDef":87,"adjMonsterDmg":0.01,"adjFinalDmg":0.1593,"adjFinalDmgAnti":0.0653,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000088: _tools.RODict({
        "propID": 51000088,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1892,"adjMinPhysicalAtk":1932,"adjMaxPhysicalAtk":1932,"adjMinMagicAtk":1932,"adjMaxMagicAtk":1932,"adjMinPhysicalArmor":836,"adjMaxPhysicalArmor":836,"adjMinMagicArmor":836,"adjMaxMagicArmor":836,"adjAccuracy":35,"adjEvasion":28,"adjFatal":31,"adjAntiFatal":28,"adjIgnoreArmor":0.118,"adjDmgArmor":0.024,"adjMortal":0.298,"adjAntiMortal":0.0814,"adjRealDmg":88,"adjRealDmgDef":88,"adjMonsterDmg":0.01,"adjFinalDmg":0.1622,"adjFinalDmgAnti":0.0662,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000089: _tools.RODict({
        "propID": 51000089,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1937,"adjMinPhysicalAtk":1965,"adjMaxPhysicalAtk":1965,"adjMinMagicAtk":1965,"adjMaxMagicAtk":1965,"adjMinPhysicalArmor":846,"adjMaxPhysicalArmor":846,"adjMinMagicArmor":846,"adjMaxMagicArmor":846,"adjAccuracy":35,"adjEvasion":28,"adjFatal":31,"adjAntiFatal":28,"adjIgnoreArmor":0.121,"adjDmgArmor":0.024,"adjMortal":0.3065,"adjAntiMortal":0.0842,"adjRealDmg":89,"adjRealDmgDef":89,"adjMonsterDmg":0.01,"adjFinalDmg":0.1651,"adjFinalDmgAnti":0.0671,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000090: _tools.RODict({
        "propID": 51000090,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2023,"adjMinPhysicalAtk":1999,"adjMaxPhysicalAtk":1999,"adjMinMagicAtk":1999,"adjMaxMagicAtk":1999,"adjMinPhysicalArmor":857,"adjMaxPhysicalArmor":857,"adjMinMagicArmor":857,"adjMaxMagicArmor":857,"adjAccuracy":35,"adjEvasion":28,"adjFatal":32,"adjAntiFatal":28,"adjIgnoreArmor":0.124,"adjDmgArmor":0.024,"adjMortal":0.315,"adjAntiMortal":0.087,"adjRealDmg":90,"adjRealDmgDef":90,"adjMonsterDmg":0.01,"adjFinalDmg":0.168,"adjFinalDmgAnti":0.068,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
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