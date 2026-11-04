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
        "propList": _tools.RODict({"adjFullHp":50,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":22,"adjMinMagicAtk":22,"adjMaxMagicAtk":22,"adjMinPhysicalArmor":18,"adjMaxPhysicalArmor":18,"adjMinMagicArmor":18,"adjMaxMagicArmor":18,"adjAccuracy":1,"adjEvasion":5,"adjFatal":5})
    }),
    51000002: _tools.RODict({
        "propID": 51000002,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":53,"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":24,"adjMinMagicAtk":24,"adjMaxMagicAtk":24,"adjMinPhysicalArmor":19,"adjMaxPhysicalArmor":19,"adjMinMagicArmor":19,"adjMaxMagicArmor":19,"adjAccuracy":1,"adjEvasion":5,"adjFatal":5})
    }),
    51000003: _tools.RODict({
        "propID": 51000003,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":56,"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":26,"adjMinMagicAtk":26,"adjMaxMagicAtk":26,"adjMinPhysicalArmor":20,"adjMaxPhysicalArmor":20,"adjMinMagicArmor":20,"adjMaxMagicArmor":20,"adjAccuracy":1,"adjEvasion":5,"adjFatal":5})
    }),
    51000004: _tools.RODict({
        "propID": 51000004,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":59,"adjMinPhysicalAtk":29,"adjMaxPhysicalAtk":29,"adjMinMagicAtk":29,"adjMaxMagicAtk":29,"adjMinPhysicalArmor":22,"adjMaxPhysicalArmor":22,"adjMinMagicArmor":22,"adjMaxMagicArmor":22,"adjAccuracy":1,"adjEvasion":5,"adjFatal":5})
    }),
    51000005: _tools.RODict({
        "propID": 51000005,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":62,"adjMinPhysicalAtk":37,"adjMaxPhysicalAtk":37,"adjMinMagicAtk":37,"adjMaxMagicAtk":37,"adjMinPhysicalArmor":23,"adjMaxPhysicalArmor":23,"adjMinMagicArmor":23,"adjMaxMagicArmor":23,"adjAccuracy":1,"adjEvasion":5,"adjFatal":5})
    }),
    51000006: _tools.RODict({
        "propID": 51000006,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":65,"adjMinPhysicalAtk":66,"adjMaxPhysicalAtk":66,"adjMinMagicAtk":66,"adjMaxMagicAtk":66,"adjMinPhysicalArmor":24,"adjMaxPhysicalArmor":24,"adjMinMagicArmor":24,"adjMaxMagicArmor":24,"adjAccuracy":1,"adjEvasion":5,"adjFatal":5})
    }),
    51000007: _tools.RODict({
        "propID": 51000007,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":70,"adjMinPhysicalAtk":103,"adjMaxPhysicalAtk":103,"adjMinMagicAtk":103,"adjMaxMagicAtk":103,"adjMinPhysicalArmor":25,"adjMaxPhysicalArmor":25,"adjMinMagicArmor":25,"adjMaxMagicArmor":25,"adjAccuracy":1,"adjEvasion":5,"adjFatal":5})
    }),
    51000008: _tools.RODict({
        "propID": 51000008,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":80,"adjMinPhysicalAtk":125,"adjMaxPhysicalAtk":125,"adjMinMagicAtk":125,"adjMaxMagicAtk":125,"adjMinPhysicalArmor":30,"adjMaxPhysicalArmor":30,"adjMinMagicArmor":30,"adjMaxMagicArmor":30,"adjAccuracy":1,"adjEvasion":5,"adjFatal":5})
    }),
    51000009: _tools.RODict({
        "propID": 51000009,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":90,"adjMinPhysicalAtk":136,"adjMaxPhysicalAtk":136,"adjMinMagicAtk":136,"adjMaxMagicAtk":136,"adjMinPhysicalArmor":123,"adjMaxPhysicalArmor":123,"adjMinMagicArmor":123,"adjMaxMagicArmor":123,"adjAccuracy":1,"adjEvasion":5,"adjFatal":5})
    }),
    51000010: _tools.RODict({
        "propID": 51000010,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":100,"adjMinPhysicalAtk":147,"adjMaxPhysicalAtk":147,"adjMinMagicAtk":147,"adjMaxMagicAtk":147,"adjMinPhysicalArmor":126,"adjMaxPhysicalArmor":126,"adjMinMagicArmor":126,"adjMaxMagicArmor":126,"adjAccuracy":2,"adjEvasion":5,"adjFatal":5})
    }),
    51000011: _tools.RODict({
        "propID": 51000011,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":110,"adjMinPhysicalAtk":166,"adjMaxPhysicalAtk":166,"adjMinMagicAtk":166,"adjMaxMagicAtk":166,"adjMinPhysicalArmor":129,"adjMaxPhysicalArmor":129,"adjMinMagicArmor":129,"adjMaxMagicArmor":129,"adjAccuracy":2,"adjEvasion":5,"adjFatal":5})
    }),
    51000012: _tools.RODict({
        "propID": 51000012,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":120,"adjMinPhysicalAtk":191,"adjMaxPhysicalAtk":191,"adjMinMagicAtk":191,"adjMaxMagicAtk":191,"adjMinPhysicalArmor":133,"adjMaxPhysicalArmor":133,"adjMinMagicArmor":133,"adjMaxMagicArmor":133,"adjAccuracy":2,"adjEvasion":5,"adjFatal":5})
    }),
    51000013: _tools.RODict({
        "propID": 51000013,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":135,"adjMinPhysicalAtk":220,"adjMaxPhysicalAtk":220,"adjMinMagicAtk":220,"adjMaxMagicAtk":220,"adjMinPhysicalArmor":137,"adjMaxPhysicalArmor":137,"adjMinMagicArmor":137,"adjMaxMagicArmor":137,"adjAccuracy":2,"adjEvasion":5,"adjFatal":5})
    }),
    51000014: _tools.RODict({
        "propID": 51000014,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":150,"adjMinPhysicalAtk":242,"adjMaxPhysicalAtk":242,"adjMinMagicAtk":242,"adjMaxMagicAtk":242,"adjMinPhysicalArmor":141,"adjMaxPhysicalArmor":141,"adjMinMagicArmor":141,"adjMaxMagicArmor":141,"adjAccuracy":2,"adjEvasion":5,"adjFatal":5})
    }),
    51000015: _tools.RODict({
        "propID": 51000015,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":175,"adjMinPhysicalAtk":253,"adjMaxPhysicalAtk":253,"adjMinMagicAtk":253,"adjMaxMagicAtk":253,"adjMinPhysicalArmor":145,"adjMaxPhysicalArmor":145,"adjMinMagicArmor":145,"adjMaxMagicArmor":145,"adjAccuracy":2,"adjEvasion":5,"adjFatal":5})
    }),
    51000016: _tools.RODict({
        "propID": 51000016,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":200,"adjMinPhysicalAtk":262,"adjMaxPhysicalAtk":262,"adjMinMagicAtk":262,"adjMaxMagicAtk":262,"adjMinPhysicalArmor":149,"adjMaxPhysicalArmor":149,"adjMinMagicArmor":149,"adjMaxMagicArmor":149,"adjAccuracy":2,"adjEvasion":5,"adjFatal":5})
    }),
    51000017: _tools.RODict({
        "propID": 51000017,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":225,"adjMinPhysicalAtk":267,"adjMaxPhysicalAtk":267,"adjMinMagicAtk":267,"adjMaxMagicAtk":267,"adjMinPhysicalArmor":153,"adjMaxPhysicalArmor":153,"adjMinMagicArmor":153,"adjMaxMagicArmor":153,"adjAccuracy":2,"adjEvasion":5,"adjFatal":5})
    }),
    51000018: _tools.RODict({
        "propID": 51000018,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":250,"adjMinPhysicalAtk":279,"adjMaxPhysicalAtk":279,"adjMinMagicAtk":279,"adjMaxMagicAtk":279,"adjMinPhysicalArmor":156,"adjMaxPhysicalArmor":156,"adjMinMagicArmor":156,"adjMaxMagicArmor":156,"adjAccuracy":2,"adjEvasion":5,"adjFatal":6,"adjAntiFatal":1,"adjMonsterDmg":0.0065})
    }),
    51000019: _tools.RODict({
        "propID": 51000019,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":275,"adjMinPhysicalAtk":295,"adjMaxPhysicalAtk":295,"adjMinMagicAtk":295,"adjMaxMagicAtk":295,"adjMinPhysicalArmor":160,"adjMaxPhysicalArmor":160,"adjMinMagicArmor":160,"adjMaxMagicArmor":160,"adjAccuracy":2,"adjEvasion":5,"adjFatal":6,"adjAntiFatal":1,"adjIgnoreArmor":0.0045,"adjDmgArmor":0.0045,"adjMortal":0.018,"adjAntiMortal":0.018,"adjMonsterDmg":0.0155,"adjMonsterDmgAnti":0.009,"adjFinalDmg":0.0045,"adjFinalDmgAnti":0.0045})
    }),
    51000020: _tools.RODict({
        "propID": 51000020,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":300,"adjMinPhysicalAtk":315,"adjMaxPhysicalAtk":315,"adjMinMagicAtk":315,"adjMaxMagicAtk":315,"adjMinPhysicalArmor":164,"adjMaxPhysicalArmor":164,"adjMinMagicArmor":164,"adjMaxMagicArmor":164,"adjAccuracy":4,"adjEvasion":6,"adjFatal":7,"adjAntiFatal":1,"adjIgnoreArmor":0.006,"adjDmgArmor":0.006,"adjMortal":0.0282,"adjAntiMortal":0.0282,"adjMonsterDmg":0.0306,"adjMonsterDmgAnti":0.0141,"adjFinalDmg":0.0065,"adjFinalDmgAnti":0.0065})
    }),
    51000021: _tools.RODict({
        "propID": 51000021,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":319,"adjMinPhysicalAtk":363,"adjMaxPhysicalAtk":363,"adjMinMagicAtk":363,"adjMaxMagicAtk":363,"adjMinPhysicalArmor":172,"adjMaxPhysicalArmor":172,"adjMinMagicArmor":172,"adjMaxMagicArmor":172,"adjAccuracy":4,"adjEvasion":6,"adjFatal":7,"adjAntiFatal":1,"adjIgnoreArmor":0.006,"adjDmgArmor":0.006,"adjMortal":0.0282,"adjAntiMortal":0.0282,"adjMonsterDmg":0.0306,"adjMonsterDmgAnti":0.0141,"adjFinalDmg":0.0065,"adjFinalDmgAnti":0.0065})
    }),
    51000022: _tools.RODict({
        "propID": 51000022,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":339,"adjMinPhysicalAtk":380,"adjMaxPhysicalAtk":380,"adjMinMagicAtk":380,"adjMaxMagicAtk":380,"adjMinPhysicalArmor":180,"adjMaxPhysicalArmor":180,"adjMinMagicArmor":180,"adjMaxMagicArmor":180,"adjAccuracy":4,"adjEvasion":6,"adjFatal":7,"adjAntiFatal":1,"adjIgnoreArmor":0.006,"adjDmgArmor":0.006,"adjMortal":0.0282,"adjAntiMortal":0.0282,"adjMonsterDmg":0.0306,"adjMonsterDmgAnti":0.0141,"adjFinalDmg":0.0065,"adjFinalDmgAnti":0.0065})
    }),
    51000023: _tools.RODict({
        "propID": 51000023,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":359,"adjMinPhysicalAtk":404,"adjMaxPhysicalAtk":404,"adjMinMagicAtk":404,"adjMaxMagicAtk":404,"adjMinPhysicalArmor":188,"adjMaxPhysicalArmor":188,"adjMinMagicArmor":188,"adjMaxMagicArmor":188,"adjAccuracy":4,"adjEvasion":6,"adjFatal":7,"adjAntiFatal":1,"adjIgnoreArmor":0.006,"adjDmgArmor":0.006,"adjMortal":0.0282,"adjAntiMortal":0.0282,"adjMonsterDmg":0.0306,"adjMonsterDmgAnti":0.0641,"adjFinalDmg":0.0065,"adjFinalDmgAnti":0.0065})
    }),
    51000024: _tools.RODict({
        "propID": 51000024,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":379,"adjMinPhysicalAtk":407,"adjMaxPhysicalAtk":407,"adjMinMagicAtk":407,"adjMaxMagicAtk":407,"adjMinPhysicalArmor":195,"adjMaxPhysicalArmor":195,"adjMinMagicArmor":195,"adjMaxMagicArmor":195,"adjAccuracy":4,"adjEvasion":6,"adjFatal":7,"adjAntiFatal":1,"adjIgnoreArmor":0.006,"adjDmgArmor":0.006,"adjMortal":0.0282,"adjAntiMortal":0.0282,"adjMonsterDmg":0.0306,"adjMonsterDmgAnti":0.0641,"adjFinalDmg":0.0065,"adjFinalDmgAnti":0.0065})
    }),
    51000025: _tools.RODict({
        "propID": 51000025,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":399,"adjMinPhysicalAtk":435,"adjMaxPhysicalAtk":435,"adjMinMagicAtk":435,"adjMaxMagicAtk":435,"adjMinPhysicalArmor":203,"adjMaxPhysicalArmor":203,"adjMinMagicArmor":203,"adjMaxMagicArmor":203,"adjAccuracy":5,"adjEvasion":8,"adjFatal":8,"adjAntiFatal":1,"adjIgnoreArmor":0.0075,"adjDmgArmor":0.01,"adjMortal":0.0342,"adjAntiMortal":0.0342,"adjMonsterDmg":0.0436,"adjMonsterDmgAnti":0.0671,"adjFinalDmg":0.008,"adjFinalDmgAnti":0.008,"adjStunEnh":1,"adjStunAnti":1,"adjSilentEnh":1,"adjSilentAnti":1,"adjKnockEnh":1,"adjKnockAnti":1,"adjFrozenEnh":1,"adjFrozenAnti":1,"adjSlowEnh":1,"adjSlowAnti":1,"adjPushEnh":1,"adjPushAnti":1})
    }),
    51000026: _tools.RODict({
        "propID": 51000026,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":447,"adjMinPhysicalAtk":453,"adjMaxPhysicalAtk":453,"adjMinMagicAtk":453,"adjMaxMagicAtk":453,"adjMinPhysicalArmor":211,"adjMaxPhysicalArmor":211,"adjMinMagicArmor":211,"adjMaxMagicArmor":211,"adjAccuracy":6,"adjEvasion":8,"adjFatal":8,"adjAntiFatal":1,"adjIgnoreArmor":0.0075,"adjDmgArmor":0.01,"adjMortal":0.0383,"adjAntiMortal":0.0383,"adjMonsterDmg":0.0457,"adjMonsterDmgAnti":0.0692,"adjFinalDmg":0.0085,"adjFinalDmgAnti":0.0085,"adjStunEnh":2,"adjStunAnti":2,"adjSilentEnh":2,"adjSilentAnti":2,"adjKnockEnh":2,"adjKnockAnti":2,"adjFrozenEnh":2,"adjFrozenAnti":2,"adjSlowEnh":2,"adjSlowAnti":2,"adjPushEnh":2,"adjPushAnti":2})
    }),
    51000027: _tools.RODict({
        "propID": 51000027,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":495,"adjMinPhysicalAtk":476,"adjMaxPhysicalAtk":476,"adjMinMagicAtk":476,"adjMaxMagicAtk":476,"adjMinPhysicalArmor":219,"adjMaxPhysicalArmor":219,"adjMinMagicArmor":219,"adjMaxMagicArmor":219,"adjAccuracy":6,"adjEvasion":8,"adjFatal":8,"adjAntiFatal":1,"adjIgnoreArmor":0.0075,"adjDmgArmor":0.01,"adjMortal":0.0383,"adjAntiMortal":0.0383,"adjMonsterDmg":0.0457,"adjMonsterDmgAnti":0.0692,"adjFinalDmg":0.0085,"adjFinalDmgAnti":0.0085,"adjStunEnh":2,"adjStunAnti":2,"adjSilentEnh":2,"adjSilentAnti":2,"adjKnockEnh":2,"adjKnockAnti":2,"adjFrozenEnh":2,"adjFrozenAnti":2,"adjSlowEnh":2,"adjSlowAnti":2,"adjPushEnh":2,"adjPushAnti":2})
    }),
    51000028: _tools.RODict({
        "propID": 51000028,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":543,"adjMinPhysicalAtk":489,"adjMaxPhysicalAtk":489,"adjMinMagicAtk":489,"adjMaxMagicAtk":489,"adjMinPhysicalArmor":227,"adjMaxPhysicalArmor":227,"adjMinMagicArmor":227,"adjMaxMagicArmor":227,"adjAccuracy":6,"adjEvasion":8,"adjFatal":8,"adjAntiFatal":1,"adjIgnoreArmor":0.0075,"adjDmgArmor":0.01,"adjMortal":0.0425,"adjAntiMortal":0.0425,"adjMonsterDmg":0.0478,"adjMonsterDmgAnti":0.0713,"adjFinalDmg":0.009,"adjFinalDmgAnti":0.009,"adjStunEnh":2,"adjStunAnti":2,"adjSilentEnh":2,"adjSilentAnti":2,"adjKnockEnh":2,"adjKnockAnti":2,"adjFrozenEnh":2,"adjFrozenAnti":2,"adjSlowEnh":2,"adjSlowAnti":2,"adjPushEnh":2,"adjPushAnti":2})
    }),
    51000029: _tools.RODict({
        "propID": 51000029,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":591,"adjMinPhysicalAtk":500,"adjMaxPhysicalAtk":500,"adjMinMagicAtk":500,"adjMaxMagicAtk":500,"adjMinPhysicalArmor":235,"adjMaxPhysicalArmor":235,"adjMinMagicArmor":235,"adjMaxMagicArmor":235,"adjAccuracy":6,"adjEvasion":8,"adjFatal":8,"adjAntiFatal":1,"adjIgnoreArmor":0.0075,"adjDmgArmor":0.01,"adjMortal":0.0425,"adjAntiMortal":0.0425,"adjMonsterDmg":0.0478,"adjMonsterDmgAnti":0.0713,"adjFinalDmg":0.009,"adjFinalDmgAnti":0.009,"adjStunEnh":2,"adjStunAnti":2,"adjSilentEnh":2,"adjSilentAnti":2,"adjKnockEnh":2,"adjKnockAnti":2,"adjFrozenEnh":2,"adjFrozenAnti":2,"adjSlowEnh":2,"adjSlowAnti":2,"adjPushEnh":2,"adjPushAnti":2})
    }),
    51000030: _tools.RODict({
        "propID": 51000030,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":639,"adjMinPhysicalAtk":505,"adjMaxPhysicalAtk":505,"adjMinMagicAtk":505,"adjMaxMagicAtk":505,"adjMinPhysicalArmor":242,"adjMaxPhysicalArmor":242,"adjMinMagicArmor":242,"adjMaxMagicArmor":242,"adjAccuracy":8,"adjEvasion":9,"adjFatal":24,"adjAntiFatal":2,"adjIgnoreArmor":0.029,"adjDmgArmor":0.0115,"adjMortal":0.0652,"adjAntiMortal":0.0527,"adjMonsterDmg":0.0628,"adjMonsterDmgAnti":0.0763,"adjFinalDmg":0.011,"adjFinalDmgAnti":0.011,"adjStunEnh":2,"adjStunAnti":2,"adjSilentEnh":2,"adjSilentAnti":2,"adjKnockEnh":2,"adjKnockAnti":2,"adjFrozenEnh":2,"adjFrozenAnti":2,"adjSlowEnh":2,"adjSlowAnti":2,"adjPushEnh":2,"adjPushAnti":2})
    }),
    51000031: _tools.RODict({
        "propID": 51000031,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":681,"adjMinPhysicalAtk":521,"adjMaxPhysicalAtk":521,"adjMinMagicAtk":521,"adjMaxMagicAtk":521,"adjMinPhysicalArmor":248,"adjMaxPhysicalArmor":248,"adjMinMagicArmor":248,"adjMaxMagicArmor":248,"adjAccuracy":9,"adjEvasion":10,"adjFatal":25,"adjAntiFatal":3,"adjIgnoreArmor":0.0361,"adjDmgArmor":0.0134,"adjMortal":0.0872,"adjAntiMortal":0.0609,"adjMonsterDmg":0.0803,"adjMonsterDmgAnti":0.0834,"adjFinalDmg":0.0181,"adjFinalDmgAnti":0.0126,"adjStunEnh":2,"adjStunAnti":2,"adjSilentEnh":2,"adjSilentAnti":2,"adjKnockEnh":2,"adjKnockAnti":2,"adjFrozenEnh":2,"adjFrozenAnti":2,"adjSlowEnh":2,"adjSlowAnti":2,"adjPushEnh":2,"adjPushAnti":2})
    }),
    51000032: _tools.RODict({
        "propID": 51000032,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":706,"adjMinPhysicalAtk":531,"adjMaxPhysicalAtk":531,"adjMinMagicAtk":531,"adjMaxMagicAtk":531,"adjMinPhysicalArmor":253,"adjMaxPhysicalArmor":253,"adjMinMagicArmor":253,"adjMaxMagicArmor":253,"adjAccuracy":9,"adjEvasion":10,"adjFatal":26,"adjAntiFatal":5,"adjIgnoreArmor":0.0432,"adjDmgArmor":0.0152,"adjMortal":0.1092,"adjAntiMortal":0.0692,"adjMonsterDmg":0.0978,"adjMonsterDmgAnti":0.0906,"adjFinalDmg":0.0252,"adjFinalDmgAnti":0.0142,"adjStunEnh":2,"adjStunAnti":2,"adjSilentEnh":2,"adjSilentAnti":2,"adjKnockEnh":2,"adjKnockAnti":2,"adjFrozenEnh":2,"adjFrozenAnti":2,"adjSlowEnh":2,"adjSlowAnti":2,"adjPushEnh":2,"adjPushAnti":2})
    }),
    51000033: _tools.RODict({
        "propID": 51000033,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":731,"adjMinPhysicalAtk":548,"adjMaxPhysicalAtk":548,"adjMinMagicAtk":548,"adjMaxMagicAtk":548,"adjMinPhysicalArmor":258,"adjMaxPhysicalArmor":258,"adjMinMagicArmor":258,"adjMaxMagicArmor":258,"adjAccuracy":10,"adjEvasion":11,"adjFatal":27,"adjAntiFatal":7,"adjIgnoreArmor":0.0504,"adjDmgArmor":0.0171,"adjMortal":0.1312,"adjAntiMortal":0.0774,"adjMonsterDmg":0.1152,"adjMonsterDmgAnti":0.0977,"adjFinalDmg":0.0324,"adjFinalDmgAnti":0.0158,"adjStunEnh":3,"adjStunAnti":3,"adjSilentEnh":3,"adjSilentAnti":3,"adjKnockEnh":3,"adjKnockAnti":3,"adjFrozenEnh":3,"adjFrozenAnti":3,"adjSlowEnh":3,"adjSlowAnti":3,"adjPushEnh":3,"adjPushAnti":3})
    }),
    51000034: _tools.RODict({
        "propID": 51000034,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":757,"adjMinPhysicalAtk":558,"adjMaxPhysicalAtk":558,"adjMinMagicAtk":558,"adjMaxMagicAtk":558,"adjMinPhysicalArmor":263,"adjMaxPhysicalArmor":263,"adjMinMagicArmor":263,"adjMaxMagicArmor":263,"adjAccuracy":11,"adjEvasion":11,"adjFatal":28,"adjAntiFatal":9,"adjIgnoreArmor":0.0575,"adjDmgArmor":0.019,"adjMortal":0.1532,"adjAntiMortal":0.0857,"adjMonsterDmg":0.1327,"adjMonsterDmgAnti":0.1048,"adjFinalDmg":0.0395,"adjFinalDmgAnti":0.0175,"adjStunEnh":3,"adjStunAnti":3,"adjSilentEnh":3,"adjSilentAnti":3,"adjKnockEnh":3,"adjKnockAnti":3,"adjFrozenEnh":3,"adjFrozenAnti":3,"adjSlowEnh":3,"adjSlowAnti":3,"adjPushEnh":3,"adjPushAnti":3})
    }),
    51000035: _tools.RODict({
        "propID": 51000035,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":782,"adjMinPhysicalAtk":562,"adjMaxPhysicalAtk":562,"adjMinMagicAtk":562,"adjMaxMagicAtk":562,"adjMinPhysicalArmor":269,"adjMaxPhysicalArmor":269,"adjMinMagicArmor":269,"adjMaxMagicArmor":269,"adjAccuracy":11,"adjEvasion":12,"adjFatal":29,"adjAntiFatal":11,"adjIgnoreArmor":0.0646,"adjDmgArmor":0.0208,"adjMortal":0.1752,"adjAntiMortal":0.094,"adjMonsterDmg":0.1502,"adjMonsterDmgAnti":0.1119,"adjFinalDmg":0.0466,"adjFinalDmgAnti":0.0191,"adjStunEnh":4,"adjStunAnti":4,"adjSilentEnh":4,"adjSilentAnti":4,"adjKnockEnh":4,"adjKnockAnti":4,"adjFrozenEnh":4,"adjFrozenAnti":4,"adjSlowEnh":4,"adjSlowAnti":4,"adjPushEnh":4,"adjPushAnti":4})
    }),
    51000036: _tools.RODict({
        "propID": 51000036,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":830,"adjMinPhysicalAtk":566,"adjMaxPhysicalAtk":566,"adjMinMagicAtk":566,"adjMaxMagicAtk":566,"adjMinPhysicalArmor":274,"adjMaxPhysicalArmor":274,"adjMinMagicArmor":274,"adjMaxMagicArmor":274,"adjAccuracy":12,"adjEvasion":12,"adjFatal":30,"adjAntiFatal":13,"adjIgnoreArmor":0.0717,"adjDmgArmor":0.0227,"adjMortal":0.1972,"adjAntiMortal":0.1022,"adjMonsterDmg":0.1676,"adjMonsterDmgAnti":0.119,"adjFinalDmg":0.0537,"adjFinalDmgAnti":0.0207,"adjStunEnh":4,"adjStunAnti":4,"adjSilentEnh":4,"adjSilentAnti":4,"adjKnockEnh":4,"adjKnockAnti":4,"adjFrozenEnh":4,"adjFrozenAnti":4,"adjSlowEnh":4,"adjSlowAnti":4,"adjPushEnh":4,"adjPushAnti":4})
    }),
    51000037: _tools.RODict({
        "propID": 51000037,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":857,"adjMinPhysicalAtk":576,"adjMaxPhysicalAtk":576,"adjMinMagicAtk":576,"adjMaxMagicAtk":576,"adjMinPhysicalArmor":279,"adjMaxPhysicalArmor":279,"adjMinMagicArmor":279,"adjMaxMagicArmor":279,"adjAccuracy":12,"adjEvasion":13,"adjFatal":31,"adjAntiFatal":15,"adjIgnoreArmor":0.0788,"adjDmgArmor":0.0246,"adjMortal":0.2192,"adjAntiMortal":0.1105,"adjMonsterDmg":0.1851,"adjMonsterDmgAnti":0.1261,"adjFinalDmg":0.0608,"adjFinalDmgAnti":0.0223,"adjStunEnh":4,"adjStunAnti":4,"adjSilentEnh":4,"adjSilentAnti":4,"adjKnockEnh":4,"adjKnockAnti":4,"adjFrozenEnh":4,"adjFrozenAnti":4,"adjSlowEnh":4,"adjSlowAnti":4,"adjPushEnh":4,"adjPushAnti":4})
    }),
    51000038: _tools.RODict({
        "propID": 51000038,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":884,"adjMinPhysicalAtk":580,"adjMaxPhysicalAtk":580,"adjMinMagicAtk":580,"adjMaxMagicAtk":580,"adjMinPhysicalArmor":284,"adjMaxPhysicalArmor":284,"adjMinMagicArmor":284,"adjMaxMagicArmor":284,"adjAccuracy":13,"adjEvasion":13,"adjFatal":32,"adjAntiFatal":17,"adjIgnoreArmor":0.0859,"adjDmgArmor":0.0264,"adjMortal":0.2412,"adjAntiMortal":0.1187,"adjMonsterDmg":0.2026,"adjMonsterDmgAnti":0.1332,"adjFinalDmg":0.0679,"adjFinalDmgAnti":0.0239,"adjStunEnh":5,"adjStunAnti":5,"adjSilentEnh":5,"adjSilentAnti":5,"adjKnockEnh":5,"adjKnockAnti":5,"adjFrozenEnh":5,"adjFrozenAnti":5,"adjSlowEnh":5,"adjSlowAnti":5,"adjPushEnh":5,"adjPushAnti":5})
    }),
    51000039: _tools.RODict({
        "propID": 51000039,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":911,"adjMinPhysicalAtk":583,"adjMaxPhysicalAtk":583,"adjMinMagicAtk":583,"adjMaxMagicAtk":583,"adjMinPhysicalArmor":290,"adjMaxPhysicalArmor":290,"adjMinMagicArmor":290,"adjMaxMagicArmor":290,"adjAccuracy":13,"adjEvasion":14,"adjFatal":33,"adjAntiFatal":18,"adjIgnoreArmor":0.0931,"adjDmgArmor":0.0283,"adjMortal":0.2632,"adjAntiMortal":0.127,"adjMonsterDmg":0.22,"adjMonsterDmgAnti":0.1403,"adjFinalDmg":0.0751,"adjFinalDmgAnti":0.0255,"adjStunEnh":5,"adjStunAnti":5,"adjSilentEnh":5,"adjSilentAnti":5,"adjKnockEnh":5,"adjKnockAnti":5,"adjFrozenEnh":5,"adjFrozenAnti":5,"adjSlowEnh":5,"adjSlowAnti":5,"adjPushEnh":5,"adjPushAnti":5})
    }),
    51000040: _tools.RODict({
        "propID": 51000040,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":939,"adjMinPhysicalAtk":593,"adjMaxPhysicalAtk":593,"adjMinMagicAtk":593,"adjMaxMagicAtk":593,"adjMinPhysicalArmor":295,"adjMaxPhysicalArmor":295,"adjMinMagicArmor":295,"adjMaxMagicArmor":295,"adjAccuracy":15,"adjEvasion":15,"adjFatal":33,"adjAntiFatal":20,"adjIgnoreArmor":0.1002,"adjDmgArmor":0.0302,"adjMortal":0.2853,"adjAntiMortal":0.1353,"adjMonsterDmg":0.2375,"adjMonsterDmgAnti":0.1474,"adjFinalDmg":0.0822,"adjFinalDmgAnti":0.0272,"adjStunEnh":5,"adjStunAnti":5,"adjSilentEnh":5,"adjSilentAnti":5,"adjKnockEnh":5,"adjKnockAnti":5,"adjFrozenEnh":5,"adjFrozenAnti":5,"adjSlowEnh":5,"adjSlowAnti":5,"adjPushEnh":5,"adjPushAnti":5})
    }),
    51000041: _tools.RODict({
        "propID": 51000041,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":995,"adjMinPhysicalAtk":606,"adjMaxPhysicalAtk":606,"adjMinMagicAtk":606,"adjMaxMagicAtk":606,"adjMinPhysicalArmor":302,"adjMaxPhysicalArmor":302,"adjMinMagicArmor":302,"adjMaxMagicArmor":302,"adjAccuracy":16,"adjEvasion":15,"adjFatal":35,"adjAntiFatal":21,"adjIgnoreArmor":0.1023,"adjDmgArmor":0.032,"adjMortal":0.3106,"adjAntiMortal":0.1443,"adjMonsterDmg":0.2486,"adjMonsterDmgAnti":0.1559,"adjFinalDmg":0.0848,"adjFinalDmgAnti":0.0298,"adjStunEnh":5,"adjStunAnti":5,"adjSilentEnh":5,"adjSilentAnti":5,"adjKnockEnh":5,"adjKnockAnti":5,"adjFrozenEnh":5,"adjFrozenAnti":5,"adjSlowEnh":5,"adjSlowAnti":5,"adjPushEnh":5,"adjPushAnti":5})
    }),
    51000042: _tools.RODict({
        "propID": 51000042,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1028,"adjMinPhysicalAtk":619,"adjMaxPhysicalAtk":619,"adjMinMagicAtk":619,"adjMaxMagicAtk":619,"adjMinPhysicalArmor":310,"adjMaxPhysicalArmor":310,"adjMinMagicArmor":310,"adjMaxMagicArmor":310,"adjAccuracy":16,"adjEvasion":16,"adjFatal":36,"adjAntiFatal":22,"adjIgnoreArmor":0.1044,"adjDmgArmor":0.0339,"adjMortal":0.3359,"adjAntiMortal":0.1534,"adjMonsterDmg":0.2598,"adjMonsterDmgAnti":0.1644,"adjFinalDmg":0.0874,"adjFinalDmgAnti":0.0324,"adjStunEnh":6,"adjStunAnti":6,"adjSilentEnh":6,"adjSilentAnti":6,"adjKnockEnh":6,"adjKnockAnti":6,"adjFrozenEnh":6,"adjFrozenAnti":6,"adjSlowEnh":6,"adjSlowAnti":6,"adjPushEnh":6,"adjPushAnti":6})
    }),
    51000043: _tools.RODict({
        "propID": 51000043,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1062,"adjMinPhysicalAtk":633,"adjMaxPhysicalAtk":633,"adjMinMagicAtk":633,"adjMaxMagicAtk":633,"adjMinPhysicalArmor":317,"adjMaxPhysicalArmor":317,"adjMinMagicArmor":317,"adjMaxMagicArmor":317,"adjAccuracy":17,"adjEvasion":16,"adjFatal":37,"adjAntiFatal":22,"adjIgnoreArmor":0.1065,"adjDmgArmor":0.0358,"adjMortal":0.3613,"adjAntiMortal":0.1625,"adjMonsterDmg":0.2709,"adjMonsterDmgAnti":0.1729,"adjFinalDmg":0.0901,"adjFinalDmgAnti":0.0351,"adjStunEnh":6,"adjStunAnti":6,"adjSilentEnh":6,"adjSilentAnti":6,"adjKnockEnh":6,"adjKnockAnti":6,"adjFrozenEnh":6,"adjFrozenAnti":6,"adjSlowEnh":6,"adjSlowAnti":6,"adjPushEnh":6,"adjPushAnti":6})
    }),
    51000044: _tools.RODict({
        "propID": 51000044,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1096,"adjMinPhysicalAtk":646,"adjMaxPhysicalAtk":646,"adjMinMagicAtk":646,"adjMaxMagicAtk":646,"adjMinPhysicalArmor":324,"adjMaxPhysicalArmor":324,"adjMinMagicArmor":324,"adjMaxMagicArmor":324,"adjAccuracy":18,"adjEvasion":17,"adjFatal":38,"adjAntiFatal":23,"adjIgnoreArmor":0.1086,"adjDmgArmor":0.0376,"adjMortal":0.3866,"adjAntiMortal":0.1716,"adjMonsterDmg":0.282,"adjMonsterDmgAnti":0.1814,"adjFinalDmg":0.0927,"adjFinalDmgAnti":0.0377,"adjStunEnh":7,"adjStunAnti":7,"adjSilentEnh":7,"adjSilentAnti":7,"adjKnockEnh":7,"adjKnockAnti":7,"adjFrozenEnh":7,"adjFrozenAnti":7,"adjSlowEnh":7,"adjSlowAnti":7,"adjPushEnh":7,"adjPushAnti":7})
    }),
    51000045: _tools.RODict({
        "propID": 51000045,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1132,"adjMinPhysicalAtk":659,"adjMaxPhysicalAtk":659,"adjMinMagicAtk":659,"adjMaxMagicAtk":659,"adjMinPhysicalArmor":332,"adjMaxPhysicalArmor":332,"adjMinMagicArmor":332,"adjMaxMagicArmor":332,"adjAccuracy":18,"adjEvasion":18,"adjFatal":40,"adjAntiFatal":25,"adjIgnoreArmor":0.1108,"adjDmgArmor":0.0395,"adjMortal":0.412,"adjAntiMortal":0.1807,"adjMonsterDmg":0.2932,"adjMonsterDmgAnti":0.1899,"adjFinalDmg":0.0954,"adjFinalDmgAnti":0.0404,"adjStunEnh":8,"adjStunAnti":8,"adjSilentEnh":8,"adjSilentAnti":8,"adjKnockEnh":8,"adjKnockAnti":8,"adjFrozenEnh":8,"adjFrozenAnti":8,"adjSlowEnh":8,"adjSlowAnti":8,"adjPushEnh":8,"adjPushAnti":8})
    }),
    51000046: _tools.RODict({
        "propID": 51000046,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1198,"adjMinPhysicalAtk":672,"adjMaxPhysicalAtk":672,"adjMinMagicAtk":672,"adjMaxMagicAtk":672,"adjMinPhysicalArmor":339,"adjMaxPhysicalArmor":339,"adjMinMagicArmor":339,"adjMaxMagicArmor":339,"adjAccuracy":19,"adjEvasion":18,"adjFatal":41,"adjAntiFatal":25,"adjIgnoreArmor":0.1129,"adjDmgArmor":0.0414,"adjMortal":0.4373,"adjAntiMortal":0.1898,"adjMonsterDmg":0.3043,"adjMonsterDmgAnti":0.1984,"adjFinalDmg":0.098,"adjFinalDmgAnti":0.043,"adjStunEnh":9,"adjStunAnti":9,"adjSilentEnh":9,"adjSilentAnti":9,"adjKnockEnh":9,"adjKnockAnti":9,"adjFrozenEnh":9,"adjFrozenAnti":9,"adjSlowEnh":9,"adjSlowAnti":9,"adjPushEnh":9,"adjPushAnti":9})
    }),
    51000047: _tools.RODict({
        "propID": 51000047,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1236,"adjMinPhysicalAtk":686,"adjMaxPhysicalAtk":686,"adjMinMagicAtk":686,"adjMaxMagicAtk":686,"adjMinPhysicalArmor":347,"adjMaxPhysicalArmor":347,"adjMinMagicArmor":347,"adjMaxMagicArmor":347,"adjAccuracy":20,"adjEvasion":19,"adjFatal":42,"adjAntiFatal":26,"adjIgnoreArmor":0.115,"adjDmgArmor":0.0432,"adjMortal":0.4626,"adjAntiMortal":0.1989,"adjMonsterDmg":0.3154,"adjMonsterDmgAnti":0.2069,"adjFinalDmg":0.1007,"adjFinalDmgAnti":0.0457,"adjStunEnh":9,"adjStunAnti":9,"adjSilentEnh":9,"adjSilentAnti":9,"adjKnockEnh":9,"adjKnockAnti":9,"adjFrozenEnh":9,"adjFrozenAnti":9,"adjSlowEnh":9,"adjSlowAnti":9,"adjPushEnh":9,"adjPushAnti":9})
    }),
    51000048: _tools.RODict({
        "propID": 51000048,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1275,"adjMinPhysicalAtk":699,"adjMaxPhysicalAtk":699,"adjMinMagicAtk":699,"adjMaxMagicAtk":699,"adjMinPhysicalArmor":354,"adjMaxPhysicalArmor":354,"adjMinMagicArmor":354,"adjMaxMagicArmor":354,"adjAccuracy":20,"adjEvasion":20,"adjFatal":43,"adjAntiFatal":27,"adjIgnoreArmor":0.1171,"adjDmgArmor":0.0451,"adjMortal":0.488,"adjAntiMortal":0.208,"adjMonsterDmg":0.3266,"adjMonsterDmgAnti":0.2154,"adjFinalDmg":0.1033,"adjFinalDmgAnti":0.0483,"adjStunEnh":10,"adjStunAnti":10,"adjSilentEnh":10,"adjSilentAnti":10,"adjKnockEnh":10,"adjKnockAnti":10,"adjFrozenEnh":10,"adjFrozenAnti":10,"adjSlowEnh":10,"adjSlowAnti":10,"adjPushEnh":10,"adjPushAnti":10})
    }),
    51000049: _tools.RODict({
        "propID": 51000049,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1315,"adjMinPhysicalAtk":712,"adjMaxPhysicalAtk":712,"adjMinMagicAtk":712,"adjMaxMagicAtk":712,"adjMinPhysicalArmor":362,"adjMaxPhysicalArmor":362,"adjMinMagicArmor":362,"adjMaxMagicArmor":362,"adjAccuracy":21,"adjEvasion":20,"adjFatal":45,"adjAntiFatal":27,"adjIgnoreArmor":0.1192,"adjDmgArmor":0.047,"adjMortal":0.5133,"adjAntiMortal":0.2171,"adjMonsterDmg":0.3377,"adjMonsterDmgAnti":0.2239,"adjFinalDmg":0.1059,"adjFinalDmgAnti":0.0509,"adjStunEnh":10,"adjStunAnti":10,"adjSilentEnh":10,"adjSilentAnti":10,"adjKnockEnh":10,"adjKnockAnti":10,"adjFrozenEnh":10,"adjFrozenAnti":10,"adjSlowEnh":10,"adjSlowAnti":10,"adjPushEnh":10,"adjPushAnti":10})
    }),
    51000050: _tools.RODict({
        "propID": 51000050,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1356,"adjMinPhysicalAtk":725,"adjMaxPhysicalAtk":725,"adjMinMagicAtk":725,"adjMaxMagicAtk":725,"adjAtkBless":1,"adjMinPhysicalArmor":369,"adjMaxPhysicalArmor":369,"adjMinMagicArmor":369,"adjMaxMagicArmor":369,"adjAccuracy":22,"adjEvasion":21,"adjFatal":46,"adjAntiFatal":28,"adjIgnoreArmor":0.1213,"adjDmgArmor":0.0488,"adjMortal":0.5387,"adjAntiMortal":0.2262,"adjMonsterDmg":0.3488,"adjMonsterDmgAnti":0.2324,"adjFinalDmg":0.1086,"adjFinalDmgAnti":0.0536,"adjStunEnh":11,"adjStunAnti":11,"adjSilentEnh":11,"adjSilentAnti":11,"adjKnockEnh":11,"adjKnockAnti":11,"adjFrozenEnh":11,"adjFrozenAnti":11,"adjSlowEnh":11,"adjSlowAnti":11,"adjPushEnh":11,"adjPushAnti":11})
    }),
    51000051: _tools.RODict({
        "propID": 51000051,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1396,"adjMinPhysicalAtk":742,"adjMaxPhysicalAtk":742,"adjMinMagicAtk":742,"adjMaxMagicAtk":742,"adjAtkBless":1,"adjMinPhysicalArmor":379,"adjMaxPhysicalArmor":379,"adjMinMagicArmor":379,"adjMaxMagicArmor":379,"adjAccuracy":22,"adjEvasion":21,"adjFatal":47,"adjAntiFatal":29,"adjIgnoreArmor":0.1254,"adjDmgArmor":0.0512,"adjMortal":0.5471,"adjAntiMortal":0.2346,"adjMonsterDmg":0.3589,"adjMonsterDmgAnti":0.2402,"adjFinalDmg":0.1112,"adjFinalDmgAnti":0.0562,"adjStunEnh":11,"adjStunAnti":11,"adjSilentEnh":11,"adjSilentAnti":11,"adjKnockEnh":11,"adjKnockAnti":11,"adjFrozenEnh":11,"adjFrozenAnti":11,"adjSlowEnh":11,"adjSlowAnti":11,"adjPushEnh":11,"adjPushAnti":11})
    }),
    51000052: _tools.RODict({
        "propID": 51000052,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1436,"adjMinPhysicalAtk":759,"adjMaxPhysicalAtk":759,"adjMinMagicAtk":759,"adjMaxMagicAtk":759,"adjAtkBless":1,"adjMinPhysicalArmor":389,"adjMaxPhysicalArmor":389,"adjMinMagicArmor":389,"adjMaxMagicArmor":389,"adjAccuracy":23,"adjEvasion":22,"adjFatal":48,"adjAntiFatal":29,"adjIgnoreArmor":0.1295,"adjDmgArmor":0.0535,"adjMortal":0.5555,"adjAntiMortal":0.243,"adjMonsterDmg":0.369,"adjMonsterDmgAnti":0.248,"adjFinalDmg":0.1138,"adjFinalDmgAnti":0.0588,"adjStunEnh":12,"adjStunAnti":12,"adjSilentEnh":12,"adjSilentAnti":12,"adjKnockEnh":12,"adjKnockAnti":12,"adjFrozenEnh":12,"adjFrozenAnti":12,"adjSlowEnh":12,"adjSlowAnti":12,"adjPushEnh":12,"adjPushAnti":12})
    }),
    51000053: _tools.RODict({
        "propID": 51000053,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1477,"adjMinPhysicalAtk":776,"adjMaxPhysicalAtk":776,"adjMinMagicAtk":776,"adjMaxMagicAtk":776,"adjAtkBless":1,"adjMinPhysicalArmor":400,"adjMaxPhysicalArmor":400,"adjMinMagicArmor":400,"adjMaxMagicArmor":400,"adjAccuracy":24,"adjEvasion":23,"adjFatal":49,"adjAntiFatal":30,"adjIgnoreArmor":0.1336,"adjDmgArmor":0.0558,"adjMortal":0.5639,"adjAntiMortal":0.2514,"adjMonsterDmg":0.3792,"adjMonsterDmgAnti":0.2557,"adjFinalDmg":0.1164,"adjFinalDmgAnti":0.0614,"adjStunEnh":12,"adjStunAnti":12,"adjSilentEnh":12,"adjSilentAnti":12,"adjKnockEnh":12,"adjKnockAnti":12,"adjFrozenEnh":12,"adjFrozenAnti":12,"adjSlowEnh":12,"adjSlowAnti":12,"adjPushEnh":12,"adjPushAnti":12})
    }),
    51000054: _tools.RODict({
        "propID": 51000054,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1519,"adjMinPhysicalAtk":792,"adjMaxPhysicalAtk":792,"adjMinMagicAtk":792,"adjMaxMagicAtk":792,"adjAtkBless":1,"adjMinPhysicalArmor":410,"adjMaxPhysicalArmor":410,"adjMinMagicArmor":410,"adjMaxMagicArmor":410,"adjAccuracy":24,"adjEvasion":24,"adjFatal":50,"adjAntiFatal":31,"adjIgnoreArmor":0.1377,"adjDmgArmor":0.0582,"adjMortal":0.5723,"adjAntiMortal":0.2598,"adjMonsterDmg":0.3893,"adjMonsterDmgAnti":0.2635,"adjFinalDmg":0.119,"adjFinalDmgAnti":0.064,"adjStunEnh":13,"adjStunAnti":13,"adjSilentEnh":13,"adjSilentAnti":13,"adjKnockEnh":13,"adjKnockAnti":13,"adjFrozenEnh":13,"adjFrozenAnti":13,"adjSlowEnh":13,"adjSlowAnti":13,"adjPushEnh":13,"adjPushAnti":13})
    }),
    51000055: _tools.RODict({
        "propID": 51000055,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1561,"adjMinPhysicalAtk":819,"adjMaxPhysicalAtk":819,"adjMinMagicAtk":819,"adjMaxMagicAtk":819,"adjAtkBless":1,"adjMinPhysicalArmor":420,"adjMaxPhysicalArmor":420,"adjMinMagicArmor":420,"adjMaxMagicArmor":420,"adjAccuracy":25,"adjEvasion":24,"adjFatal":52,"adjAntiFatal":32,"adjIgnoreArmor":0.1417,"adjDmgArmor":0.0605,"adjMortal":0.5807,"adjAntiMortal":0.2683,"adjMonsterDmg":0.3994,"adjMonsterDmgAnti":0.2712,"adjFinalDmg":0.1216,"adjFinalDmgAnti":0.0666,"adjStunEnh":14,"adjStunAnti":14,"adjSilentEnh":14,"adjSilentAnti":14,"adjKnockEnh":14,"adjKnockAnti":14,"adjFrozenEnh":14,"adjFrozenAnti":14,"adjSlowEnh":14,"adjSlowAnti":14,"adjPushEnh":14,"adjPushAnti":14})
    }),
    51000056: _tools.RODict({
        "propID": 51000056,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1604,"adjMinPhysicalAtk":836,"adjMaxPhysicalAtk":836,"adjMinMagicAtk":836,"adjMaxMagicAtk":836,"adjAtkBless":1,"adjMinPhysicalArmor":430,"adjMaxPhysicalArmor":430,"adjMinMagicArmor":430,"adjMaxMagicArmor":430,"adjAccuracy":26,"adjEvasion":25,"adjFatal":53,"adjAntiFatal":33,"adjIgnoreArmor":0.1458,"adjDmgArmor":0.0628,"adjMortal":0.5892,"adjAntiMortal":0.2767,"adjMonsterDmg":0.4095,"adjMonsterDmgAnti":0.279,"adjFinalDmg":0.1242,"adjFinalDmgAnti":0.0692,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15,"adjPushEnh":15,"adjPushAnti":15})
    }),
    51000057: _tools.RODict({
        "propID": 51000057,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1648,"adjMinPhysicalAtk":853,"adjMaxPhysicalAtk":853,"adjMinMagicAtk":853,"adjMaxMagicAtk":853,"adjAtkBless":1,"adjMinPhysicalArmor":441,"adjMaxPhysicalArmor":441,"adjMinMagicArmor":441,"adjMaxMagicArmor":441,"adjAccuracy":26,"adjEvasion":26,"adjFatal":54,"adjAntiFatal":33,"adjIgnoreArmor":0.1499,"adjDmgArmor":0.0652,"adjMortal":0.5976,"adjAntiMortal":0.2851,"adjMonsterDmg":0.4196,"adjMonsterDmgAnti":0.2868,"adjFinalDmg":0.1268,"adjFinalDmgAnti":0.0718,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15,"adjPushEnh":15,"adjPushAnti":15})
    }),
    51000058: _tools.RODict({
        "propID": 51000058,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1692,"adjMinPhysicalAtk":870,"adjMaxPhysicalAtk":870,"adjMinMagicAtk":870,"adjMaxMagicAtk":870,"adjAtkBless":1,"adjMinPhysicalArmor":451,"adjMaxPhysicalArmor":451,"adjMinMagicArmor":451,"adjMaxMagicArmor":451,"adjAccuracy":27,"adjEvasion":26,"adjFatal":55,"adjAntiFatal":34,"adjIgnoreArmor":0.154,"adjDmgArmor":0.0675,"adjMortal":0.606,"adjAntiMortal":0.2935,"adjMonsterDmg":0.4297,"adjMonsterDmgAnti":0.2945,"adjFinalDmg":0.1295,"adjFinalDmgAnti":0.0745,"adjStunEnh":16,"adjStunAnti":16,"adjSilentEnh":16,"adjSilentAnti":16,"adjKnockEnh":16,"adjKnockAnti":16,"adjFrozenEnh":16,"adjFrozenAnti":16,"adjSlowEnh":16,"adjSlowAnti":16,"adjPushEnh":16,"adjPushAnti":16})
    }),
    51000059: _tools.RODict({
        "propID": 51000059,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1737,"adjMinPhysicalAtk":887,"adjMaxPhysicalAtk":887,"adjMinMagicAtk":887,"adjMaxMagicAtk":887,"adjAtkBless":1,"adjMinPhysicalArmor":461,"adjMaxPhysicalArmor":461,"adjMinMagicArmor":461,"adjMaxMagicArmor":461,"adjAccuracy":28,"adjEvasion":27,"adjFatal":56,"adjAntiFatal":35,"adjIgnoreArmor":0.1581,"adjDmgArmor":0.0698,"adjMortal":0.6144,"adjAntiMortal":0.3019,"adjMonsterDmg":0.4398,"adjMonsterDmgAnti":0.3023,"adjFinalDmg":0.1321,"adjFinalDmgAnti":0.0771,"adjStunEnh":16,"adjStunAnti":16,"adjSilentEnh":16,"adjSilentAnti":16,"adjKnockEnh":16,"adjKnockAnti":16,"adjFrozenEnh":16,"adjFrozenAnti":16,"adjSlowEnh":16,"adjSlowAnti":16,"adjPushEnh":16,"adjPushAnti":16})
    }),
    51000060: _tools.RODict({
        "propID": 51000060,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1782,"adjMinPhysicalAtk":903,"adjMaxPhysicalAtk":903,"adjMinMagicAtk":903,"adjMaxMagicAtk":903,"adjAtkBless":2,"adjMinPhysicalArmor":471,"adjMaxPhysicalArmor":471,"adjMinMagicArmor":471,"adjMaxMagicArmor":471,"adjAccuracy":29,"adjEvasion":28,"adjFatal":57,"adjAntiFatal":35,"adjIgnoreArmor":0.1622,"adjDmgArmor":0.0722,"adjMortal":0.6228,"adjAntiMortal":0.3103,"adjMonsterDmg":0.4499,"adjMonsterDmgAnti":0.3101,"adjFinalDmg":0.1347,"adjFinalDmgAnti":0.0797,"adjStunEnh":17,"adjStunAnti":17,"adjSilentEnh":17,"adjSilentAnti":17,"adjKnockEnh":17,"adjKnockAnti":17,"adjFrozenEnh":17,"adjFrozenAnti":17,"adjSlowEnh":17,"adjSlowAnti":17,"adjPushEnh":17,"adjPushAnti":17})
    }),
    51000061: _tools.RODict({
        "propID": 51000061,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1830,"adjMinPhysicalAtk":920,"adjMaxPhysicalAtk":920,"adjMinMagicAtk":920,"adjMaxMagicAtk":920,"adjAtkBless":2,"adjMinPhysicalArmor":481,"adjMaxPhysicalArmor":481,"adjMinMagicArmor":481,"adjMaxMagicArmor":481,"adjAccuracy":29,"adjEvasion":28,"adjFatal":58,"adjAntiFatal":36,"adjIgnoreArmor":0.1664,"adjDmgArmor":0.0739,"adjMortal":0.6462,"adjAntiMortal":0.3212,"adjMonsterDmg":0.463,"adjMonsterDmgAnti":0.3228,"adjFinalDmg":0.1394,"adjFinalDmgAnti":0.0829,"adjStunEnh":17,"adjStunAnti":17,"adjSilentEnh":17,"adjSilentAnti":17,"adjKnockEnh":17,"adjKnockAnti":17,"adjFrozenEnh":17,"adjFrozenAnti":17,"adjSlowEnh":17,"adjSlowAnti":17,"adjPushEnh":17,"adjPushAnti":17})
    }),
    51000062: _tools.RODict({
        "propID": 51000062,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1880,"adjMinPhysicalAtk":936,"adjMaxPhysicalAtk":936,"adjMinMagicAtk":936,"adjMaxMagicAtk":936,"adjAtkBless":2,"adjMinPhysicalArmor":492,"adjMaxPhysicalArmor":492,"adjMinMagicArmor":492,"adjMaxMagicArmor":492,"adjAccuracy":29,"adjEvasion":29,"adjFatal":58,"adjAntiFatal":37,"adjIgnoreArmor":0.1706,"adjDmgArmor":0.0756,"adjMortal":0.6696,"adjAntiMortal":0.3321,"adjMonsterDmg":0.476,"adjMonsterDmgAnti":0.3355,"adjFinalDmg":0.1441,"adjFinalDmgAnti":0.0861,"adjStunEnh":18,"adjStunAnti":18,"adjSilentEnh":18,"adjSilentAnti":18,"adjKnockEnh":18,"adjKnockAnti":18,"adjFrozenEnh":18,"adjFrozenAnti":18,"adjSlowEnh":18,"adjSlowAnti":18,"adjPushEnh":18,"adjPushAnti":18})
    }),
    51000063: _tools.RODict({
        "propID": 51000063,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1929,"adjMinPhysicalAtk":953,"adjMaxPhysicalAtk":953,"adjMinMagicAtk":953,"adjMaxMagicAtk":953,"adjAtkBless":2,"adjMinPhysicalArmor":502,"adjMaxPhysicalArmor":502,"adjMinMagicArmor":502,"adjMaxMagicArmor":502,"adjAccuracy":30,"adjEvasion":29,"adjFatal":59,"adjAntiFatal":37,"adjIgnoreArmor":0.1749,"adjDmgArmor":0.0774,"adjMortal":0.693,"adjAntiMortal":0.343,"adjMonsterDmg":0.489,"adjMonsterDmgAnti":0.3482,"adjFinalDmg":0.1489,"adjFinalDmgAnti":0.0894,"adjStunEnh":18,"adjStunAnti":18,"adjSilentEnh":18,"adjSilentAnti":18,"adjKnockEnh":18,"adjKnockAnti":18,"adjFrozenEnh":18,"adjFrozenAnti":18,"adjSlowEnh":18,"adjSlowAnti":18,"adjPushEnh":18,"adjPushAnti":18})
    }),
    51000064: _tools.RODict({
        "propID": 51000064,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1980,"adjMinPhysicalAtk":969,"adjMaxPhysicalAtk":969,"adjMinMagicAtk":969,"adjMaxMagicAtk":969,"adjAtkBless":2,"adjMinPhysicalArmor":512,"adjMaxPhysicalArmor":512,"adjMinMagicArmor":512,"adjMaxMagicArmor":512,"adjAccuracy":30,"adjEvasion":30,"adjFatal":59,"adjAntiFatal":38,"adjIgnoreArmor":0.1791,"adjDmgArmor":0.0791,"adjMortal":0.7164,"adjAntiMortal":0.3539,"adjMonsterDmg":0.502,"adjMonsterDmgAnti":0.3608,"adjFinalDmg":0.1536,"adjFinalDmgAnti":0.0926,"adjStunEnh":19,"adjStunAnti":19,"adjSilentEnh":19,"adjSilentAnti":19,"adjKnockEnh":19,"adjKnockAnti":19,"adjFrozenEnh":19,"adjFrozenAnti":19,"adjSlowEnh":19,"adjSlowAnti":19,"adjPushEnh":19,"adjPushAnti":19})
    }),
    51000065: _tools.RODict({
        "propID": 51000065,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2032,"adjMinPhysicalAtk":974,"adjMaxPhysicalAtk":974,"adjMinMagicAtk":974,"adjMaxMagicAtk":974,"adjAtkBless":2,"adjMinPhysicalArmor":522,"adjMaxPhysicalArmor":522,"adjMinMagicArmor":522,"adjMaxMagicArmor":522,"adjAccuracy":31,"adjEvasion":30,"adjFatal":60,"adjAntiFatal":40,"adjIgnoreArmor":0.1833,"adjDmgArmor":0.0808,"adjMortal":0.7398,"adjAntiMortal":0.3648,"adjMonsterDmg":0.5151,"adjMonsterDmgAnti":0.3735,"adjFinalDmg":0.1583,"adjFinalDmgAnti":0.0958,"adjStunEnh":20,"adjStunAnti":20,"adjSilentEnh":20,"adjSilentAnti":20,"adjKnockEnh":20,"adjKnockAnti":20,"adjFrozenEnh":20,"adjFrozenAnti":20,"adjSlowEnh":20,"adjSlowAnti":20,"adjPushEnh":20,"adjPushAnti":20})
    }),
    51000066: _tools.RODict({
        "propID": 51000066,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2084,"adjMinPhysicalAtk":991,"adjMaxPhysicalAtk":991,"adjMinMagicAtk":991,"adjMaxMagicAtk":991,"adjAtkBless":2,"adjMinPhysicalArmor":532,"adjMaxPhysicalArmor":532,"adjMinMagicArmor":532,"adjMaxMagicArmor":532,"adjAccuracy":31,"adjEvasion":30,"adjFatal":60,"adjAntiFatal":40,"adjIgnoreArmor":0.1876,"adjDmgArmor":0.0826,"adjMortal":0.7632,"adjAntiMortal":0.3757,"adjMonsterDmg":0.5281,"adjMonsterDmgAnti":0.3862,"adjFinalDmg":0.1631,"adjFinalDmgAnti":0.0991,"adjStunEnh":20,"adjStunAnti":20,"adjSilentEnh":20,"adjSilentAnti":20,"adjKnockEnh":20,"adjKnockAnti":20,"adjFrozenEnh":20,"adjFrozenAnti":20,"adjSlowEnh":20,"adjSlowAnti":20,"adjPushEnh":20,"adjPushAnti":20})
    }),
    51000067: _tools.RODict({
        "propID": 51000067,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2137,"adjMinPhysicalAtk":1007,"adjMaxPhysicalAtk":1007,"adjMinMagicAtk":1007,"adjMaxMagicAtk":1007,"adjAtkBless":2,"adjMinPhysicalArmor":542,"adjMaxPhysicalArmor":542,"adjMinMagicArmor":542,"adjMaxMagicArmor":542,"adjAccuracy":32,"adjEvasion":31,"adjFatal":61,"adjAntiFatal":41,"adjIgnoreArmor":0.1918,"adjDmgArmor":0.0843,"adjMortal":0.7866,"adjAntiMortal":0.3866,"adjMonsterDmg":0.5412,"adjMonsterDmgAnti":0.3989,"adjFinalDmg":0.1678,"adjFinalDmgAnti":0.1023,"adjStunEnh":21,"adjStunAnti":21,"adjSilentEnh":21,"adjSilentAnti":21,"adjKnockEnh":21,"adjKnockAnti":21,"adjFrozenEnh":21,"adjFrozenAnti":21,"adjSlowEnh":21,"adjSlowAnti":21,"adjPushEnh":21,"adjPushAnti":21})
    }),
    51000068: _tools.RODict({
        "propID": 51000068,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2191,"adjMinPhysicalAtk":1023,"adjMaxPhysicalAtk":1023,"adjMinMagicAtk":1023,"adjMaxMagicAtk":1023,"adjAtkBless":2,"adjMinPhysicalArmor":552,"adjMaxPhysicalArmor":552,"adjMinMagicArmor":552,"adjMaxMagicArmor":552,"adjAccuracy":32,"adjEvasion":31,"adjFatal":61,"adjAntiFatal":42,"adjIgnoreArmor":0.196,"adjDmgArmor":0.086,"adjMortal":0.81,"adjAntiMortal":0.3975,"adjMonsterDmg":0.5542,"adjMonsterDmgAnti":0.4116,"adjFinalDmg":0.1725,"adjFinalDmgAnti":0.1055,"adjStunEnh":21,"adjStunAnti":21,"adjSilentEnh":21,"adjSilentAnti":21,"adjKnockEnh":21,"adjKnockAnti":21,"adjFrozenEnh":21,"adjFrozenAnti":21,"adjSlowEnh":21,"adjSlowAnti":21,"adjPushEnh":21,"adjPushAnti":21})
    }),
    51000069: _tools.RODict({
        "propID": 51000069,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2246,"adjMinPhysicalAtk":1039,"adjMaxPhysicalAtk":1039,"adjMinMagicAtk":1039,"adjMaxMagicAtk":1039,"adjAtkBless":2,"adjMinPhysicalArmor":563,"adjMaxPhysicalArmor":563,"adjMinMagicArmor":563,"adjMaxMagicArmor":563,"adjAccuracy":33,"adjEvasion":32,"adjFatal":62,"adjAntiFatal":42,"adjIgnoreArmor":0.2003,"adjDmgArmor":0.0878,"adjMortal":0.8334,"adjAntiMortal":0.4084,"adjMonsterDmg":0.5672,"adjMonsterDmgAnti":0.4243,"adjFinalDmg":0.1773,"adjFinalDmgAnti":0.1088,"adjStunEnh":22,"adjStunAnti":22,"adjSilentEnh":22,"adjSilentAnti":22,"adjKnockEnh":22,"adjKnockAnti":22,"adjFrozenEnh":22,"adjFrozenAnti":22,"adjSlowEnh":22,"adjSlowAnti":22,"adjPushEnh":22,"adjPushAnti":22})
    }),
    51000070: _tools.RODict({
        "propID": 51000070,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2302,"adjMinPhysicalAtk":1056,"adjMaxPhysicalAtk":1056,"adjMinMagicAtk":1056,"adjMaxMagicAtk":1056,"adjAtkBless":3,"adjMinPhysicalArmor":573,"adjMaxPhysicalArmor":573,"adjMinMagicArmor":573,"adjMaxMagicArmor":573,"adjAccuracy":33,"adjEvasion":32,"adjFatal":62,"adjAntiFatal":43,"adjIgnoreArmor":0.2045,"adjDmgArmor":0.0895,"adjMortal":0.8568,"adjAntiMortal":0.4193,"adjMonsterDmg":0.5802,"adjMonsterDmgAnti":0.437,"adjFinalDmg":0.182,"adjFinalDmgAnti":0.112,"adjStunEnh":22,"adjStunAnti":22,"adjSilentEnh":22,"adjSilentAnti":22,"adjKnockEnh":22,"adjKnockAnti":22,"adjFrozenEnh":22,"adjFrozenAnti":22,"adjSlowEnh":22,"adjSlowAnti":22,"adjPushEnh":22,"adjPushAnti":22})
    }),
    51000071: _tools.RODict({
        "propID": 51000071,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2372,"adjMinPhysicalAtk":1074,"adjMaxPhysicalAtk":1074,"adjMinMagicAtk":1074,"adjMaxMagicAtk":1074,"adjAtkBless":3,"adjMinPhysicalArmor":583,"adjMaxPhysicalArmor":583,"adjMinMagicArmor":583,"adjMaxMagicArmor":583,"adjAccuracy":34,"adjEvasion":33,"adjFatal":63,"adjAntiFatal":44,"adjIgnoreArmor":0.2093,"adjDmgArmor":0.0918,"adjMortal":0.884,"adjAntiMortal":0.4315,"adjMonsterDmg":0.5947,"adjMonsterDmgAnti":0.4446,"adjFinalDmg":0.189,"adjFinalDmgAnti":0.115,"adjStunEnh":23,"adjStunAnti":23,"adjSilentEnh":23,"adjSilentAnti":23,"adjKnockEnh":23,"adjKnockAnti":23,"adjFrozenEnh":23,"adjFrozenAnti":23,"adjSlowEnh":23,"adjSlowAnti":23,"adjPushEnh":23,"adjPushAnti":23})
    }),
    51000072: _tools.RODict({
        "propID": 51000072,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2443,"adjMinPhysicalAtk":1092,"adjMaxPhysicalAtk":1092,"adjMinMagicAtk":1092,"adjMaxMagicAtk":1092,"adjAtkBless":3,"adjMinPhysicalArmor":594,"adjMaxPhysicalArmor":594,"adjMinMagicArmor":594,"adjMaxMagicArmor":594,"adjAccuracy":34,"adjEvasion":34,"adjFatal":63,"adjAntiFatal":44,"adjIgnoreArmor":0.2142,"adjDmgArmor":0.0942,"adjMortal":0.9113,"adjAntiMortal":0.4437,"adjMonsterDmg":0.6091,"adjMonsterDmgAnti":0.4522,"adjFinalDmg":0.1959,"adjFinalDmgAnti":0.1179,"adjStunEnh":23,"adjStunAnti":23,"adjSilentEnh":23,"adjSilentAnti":23,"adjKnockEnh":23,"adjKnockAnti":23,"adjFrozenEnh":23,"adjFrozenAnti":23,"adjSlowEnh":23,"adjSlowAnti":23,"adjPushEnh":23,"adjPushAnti":23})
    }),
    51000073: _tools.RODict({
        "propID": 51000073,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2516,"adjMinPhysicalAtk":1110,"adjMaxPhysicalAtk":1110,"adjMinMagicAtk":1110,"adjMaxMagicAtk":1110,"adjAtkBless":3,"adjMinPhysicalArmor":605,"adjMaxPhysicalArmor":605,"adjMinMagicArmor":605,"adjMaxMagicArmor":605,"adjAccuracy":35,"adjEvasion":34,"adjFatal":64,"adjAntiFatal":45,"adjIgnoreArmor":0.219,"adjDmgArmor":0.0965,"adjMortal":0.9385,"adjAntiMortal":0.456,"adjMonsterDmg":0.6235,"adjMonsterDmgAnti":0.4598,"adjFinalDmg":0.2029,"adjFinalDmgAnti":0.1209,"adjStunEnh":23,"adjStunAnti":23,"adjSilentEnh":23,"adjSilentAnti":23,"adjKnockEnh":23,"adjKnockAnti":23,"adjFrozenEnh":23,"adjFrozenAnti":23,"adjSlowEnh":23,"adjSlowAnti":23,"adjPushEnh":23,"adjPushAnti":23})
    }),
    51000074: _tools.RODict({
        "propID": 51000074,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2591,"adjMinPhysicalAtk":1128,"adjMaxPhysicalAtk":1128,"adjMinMagicAtk":1128,"adjMaxMagicAtk":1128,"adjAtkBless":3,"adjMinPhysicalArmor":615,"adjMaxPhysicalArmor":615,"adjMinMagicArmor":615,"adjMaxMagicArmor":615,"adjAccuracy":36,"adjEvasion":35,"adjFatal":65,"adjAntiFatal":45,"adjIgnoreArmor":0.2238,"adjDmgArmor":0.0988,"adjMortal":0.9657,"adjAntiMortal":0.4682,"adjMonsterDmg":0.638,"adjMonsterDmgAnti":0.4673,"adjFinalDmg":0.2098,"adjFinalDmgAnti":0.1238,"adjStunEnh":24,"adjStunAnti":24,"adjSilentEnh":24,"adjSilentAnti":24,"adjKnockEnh":24,"adjKnockAnti":24,"adjFrozenEnh":24,"adjFrozenAnti":24,"adjSlowEnh":24,"adjSlowAnti":24,"adjPushEnh":24,"adjPushAnti":24})
    }),
    51000075: _tools.RODict({
        "propID": 51000075,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2667,"adjMinPhysicalAtk":1146,"adjMaxPhysicalAtk":1146,"adjMinMagicAtk":1146,"adjMaxMagicAtk":1146,"adjAtkBless":3,"adjMinPhysicalArmor":626,"adjMaxPhysicalArmor":626,"adjMinMagicArmor":626,"adjMaxMagicArmor":626,"adjAccuracy":36,"adjEvasion":36,"adjFatal":65,"adjAntiFatal":47,"adjIgnoreArmor":0.2287,"adjDmgArmor":0.1012,"adjMortal":0.993,"adjAntiMortal":0.4805,"adjMonsterDmg":0.6524,"adjMonsterDmgAnti":0.4749,"adjFinalDmg":0.2168,"adjFinalDmgAnti":0.1268,"adjStunEnh":25,"adjStunAnti":25,"adjSilentEnh":25,"adjSilentAnti":25,"adjKnockEnh":25,"adjKnockAnti":25,"adjFrozenEnh":25,"adjFrozenAnti":25,"adjSlowEnh":25,"adjSlowAnti":25,"adjPushEnh":25,"adjPushAnti":25})
    }),
    51000076: _tools.RODict({
        "propID": 51000076,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2744,"adjMinPhysicalAtk":1164,"adjMaxPhysicalAtk":1164,"adjMinMagicAtk":1164,"adjMaxMagicAtk":1164,"adjAtkBless":3,"adjMinPhysicalArmor":637,"adjMaxPhysicalArmor":637,"adjMinMagicArmor":637,"adjMaxMagicArmor":637,"adjAccuracy":37,"adjEvasion":36,"adjFatal":66,"adjAntiFatal":47,"adjIgnoreArmor":0.2335,"adjDmgArmor":0.1035,"adjMortal":1.0203,"adjAntiMortal":0.4927,"adjMonsterDmg":0.6668,"adjMonsterDmgAnti":0.4825,"adjFinalDmg":0.2238,"adjFinalDmgAnti":0.1298,"adjStunEnh":26,"adjStunAnti":26,"adjSilentEnh":26,"adjSilentAnti":26,"adjKnockEnh":26,"adjKnockAnti":26,"adjFrozenEnh":26,"adjFrozenAnti":26,"adjSlowEnh":26,"adjSlowAnti":26,"adjPushEnh":26,"adjPushAnti":26})
    }),
    51000077: _tools.RODict({
        "propID": 51000077,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2824,"adjMinPhysicalAtk":1182,"adjMaxPhysicalAtk":1182,"adjMinMagicAtk":1182,"adjMaxMagicAtk":1182,"adjAtkBless":3,"adjMinPhysicalArmor":647,"adjMaxPhysicalArmor":647,"adjMinMagicArmor":647,"adjMaxMagicArmor":647,"adjAccuracy":38,"adjEvasion":37,"adjFatal":66,"adjAntiFatal":48,"adjIgnoreArmor":0.2383,"adjDmgArmor":0.1058,"adjMortal":1.0475,"adjAntiMortal":0.505,"adjMonsterDmg":0.6812,"adjMonsterDmgAnti":0.4901,"adjFinalDmg":0.2307,"adjFinalDmgAnti":0.1327,"adjStunEnh":26,"adjStunAnti":26,"adjSilentEnh":26,"adjSilentAnti":26,"adjKnockEnh":26,"adjKnockAnti":26,"adjFrozenEnh":26,"adjFrozenAnti":26,"adjSlowEnh":26,"adjSlowAnti":26,"adjPushEnh":26,"adjPushAnti":26})
    }),
    51000078: _tools.RODict({
        "propID": 51000078,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2904,"adjMinPhysicalAtk":1200,"adjMaxPhysicalAtk":1200,"adjMinMagicAtk":1200,"adjMaxMagicAtk":1200,"adjAtkBless":3,"adjMinPhysicalArmor":658,"adjMaxPhysicalArmor":658,"adjMinMagicArmor":658,"adjMaxMagicArmor":658,"adjAccuracy":38,"adjEvasion":38,"adjFatal":67,"adjAntiFatal":49,"adjIgnoreArmor":0.2432,"adjDmgArmor":0.1082,"adjMortal":1.0748,"adjAntiMortal":0.5172,"adjMonsterDmg":0.6957,"adjMonsterDmgAnti":0.4977,"adjFinalDmg":0.2377,"adjFinalDmgAnti":0.1357,"adjStunEnh":26,"adjStunAnti":26,"adjSilentEnh":26,"adjSilentAnti":26,"adjKnockEnh":26,"adjKnockAnti":26,"adjFrozenEnh":26,"adjFrozenAnti":26,"adjSlowEnh":26,"adjSlowAnti":26,"adjPushEnh":26,"adjPushAnti":26})
    }),
    51000079: _tools.RODict({
        "propID": 51000079,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2986,"adjMinPhysicalAtk":1218,"adjMaxPhysicalAtk":1218,"adjMinMagicAtk":1218,"adjMaxMagicAtk":1218,"adjAtkBless":3,"adjMinPhysicalArmor":669,"adjMaxPhysicalArmor":669,"adjMinMagicArmor":669,"adjMaxMagicArmor":669,"adjAccuracy":39,"adjEvasion":38,"adjFatal":68,"adjAntiFatal":49,"adjIgnoreArmor":0.248,"adjDmgArmor":0.1105,"adjMortal":1.102,"adjAntiMortal":0.5295,"adjMonsterDmg":0.7101,"adjMonsterDmgAnti":0.5052,"adjFinalDmg":0.2446,"adjFinalDmgAnti":0.1386,"adjStunEnh":27,"adjStunAnti":27,"adjSilentEnh":27,"adjSilentAnti":27,"adjKnockEnh":27,"adjKnockAnti":27,"adjFrozenEnh":27,"adjFrozenAnti":27,"adjSlowEnh":27,"adjSlowAnti":27,"adjPushEnh":27,"adjPushAnti":27})
    }),
    51000080: _tools.RODict({
        "propID": 51000080,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3070,"adjMinPhysicalAtk":1236,"adjMaxPhysicalAtk":1236,"adjMinMagicAtk":1236,"adjMaxMagicAtk":1236,"adjAtkBless":3,"adjMinPhysicalArmor":680,"adjMaxPhysicalArmor":680,"adjMinMagicArmor":680,"adjMaxMagicArmor":680,"adjAccuracy":40,"adjEvasion":39,"adjFatal":68,"adjAntiFatal":50,"adjIgnoreArmor":0.2528,"adjDmgArmor":0.1128,"adjMortal":1.1293,"adjAntiMortal":0.5417,"adjMonsterDmg":0.7245,"adjMonsterDmgAnti":0.5128,"adjFinalDmg":0.2516,"adjFinalDmgAnti":0.1416,"adjStunEnh":27,"adjStunAnti":27,"adjSilentEnh":27,"adjSilentAnti":27,"adjKnockEnh":27,"adjKnockAnti":27,"adjFrozenEnh":27,"adjFrozenAnti":27,"adjSlowEnh":27,"adjSlowAnti":27,"adjPushEnh":27,"adjPushAnti":27})
    }),
    51000081: _tools.RODict({
        "propID": 51000081,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3137,"adjMinPhysicalAtk":1261,"adjMaxPhysicalAtk":1261,"adjMinMagicAtk":1261,"adjMaxMagicAtk":1261,"adjAtkBless":3,"adjMinPhysicalArmor":692,"adjMaxPhysicalArmor":692,"adjMinMagicArmor":692,"adjMaxMagicArmor":692,"adjAccuracy":40,"adjEvasion":39,"adjFatal":68,"adjAntiFatal":50,"adjIgnoreArmor":0.2555,"adjDmgArmor":0.1155,"adjMortal":1.1335,"adjAntiMortal":0.5459,"adjMonsterDmg":0.7312,"adjMonsterDmgAnti":0.519,"adjFinalDmg":0.2545,"adjFinalDmgAnti":0.1446,"adjStunEnh":27,"adjStunAnti":27,"adjSilentEnh":27,"adjSilentAnti":27,"adjKnockEnh":27,"adjKnockAnti":27,"adjFrozenEnh":27,"adjFrozenAnti":27,"adjSlowEnh":27,"adjSlowAnti":27,"adjPushEnh":27,"adjPushAnti":27})
    }),
    51000082: _tools.RODict({
        "propID": 51000082,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3205,"adjMinPhysicalAtk":1286,"adjMaxPhysicalAtk":1286,"adjMinMagicAtk":1286,"adjMaxMagicAtk":1286,"adjAtkBless":3,"adjMinPhysicalArmor":705,"adjMaxPhysicalArmor":705,"adjMinMagicArmor":705,"adjMaxMagicArmor":705,"adjAccuracy":41,"adjEvasion":40,"adjFatal":69,"adjAntiFatal":50,"adjIgnoreArmor":0.2583,"adjDmgArmor":0.1183,"adjMortal":1.1377,"adjAntiMortal":0.5501,"adjMonsterDmg":0.7379,"adjMonsterDmgAnti":0.5251,"adjFinalDmg":0.2575,"adjFinalDmgAnti":0.1475,"adjStunEnh":27,"adjStunAnti":27,"adjSilentEnh":27,"adjSilentAnti":27,"adjKnockEnh":27,"adjKnockAnti":27,"adjFrozenEnh":27,"adjFrozenAnti":27,"adjSlowEnh":27,"adjSlowAnti":27,"adjPushEnh":27,"adjPushAnti":27})
    }),
    51000083: _tools.RODict({
        "propID": 51000083,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3273,"adjMinPhysicalAtk":1311,"adjMaxPhysicalAtk":1311,"adjMinMagicAtk":1311,"adjMaxMagicAtk":1311,"adjAtkBless":3,"adjMinPhysicalArmor":717,"adjMaxPhysicalArmor":717,"adjMinMagicArmor":717,"adjMaxMagicArmor":717,"adjAccuracy":41,"adjEvasion":40,"adjFatal":69,"adjAntiFatal":50,"adjIgnoreArmor":0.261,"adjDmgArmor":0.121,"adjMortal":1.1419,"adjAntiMortal":0.5543,"adjMonsterDmg":0.7446,"adjMonsterDmgAnti":0.5312,"adjFinalDmg":0.2605,"adjFinalDmgAnti":0.1505,"adjStunEnh":28,"adjStunAnti":28,"adjSilentEnh":28,"adjSilentAnti":28,"adjKnockEnh":28,"adjKnockAnti":28,"adjFrozenEnh":28,"adjFrozenAnti":28,"adjSlowEnh":28,"adjSlowAnti":28,"adjPushEnh":28,"adjPushAnti":28})
    }),
    51000084: _tools.RODict({
        "propID": 51000084,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3341,"adjMinPhysicalAtk":1335,"adjMaxPhysicalAtk":1335,"adjMinMagicAtk":1335,"adjMaxMagicAtk":1335,"adjAtkBless":3,"adjMinPhysicalArmor":730,"adjMaxPhysicalArmor":730,"adjMinMagicArmor":730,"adjMaxMagicArmor":730,"adjAccuracy":41,"adjEvasion":41,"adjFatal":69,"adjAntiFatal":51,"adjIgnoreArmor":0.2637,"adjDmgArmor":0.1237,"adjMortal":1.1461,"adjAntiMortal":0.5585,"adjMonsterDmg":0.7513,"adjMonsterDmgAnti":0.5373,"adjFinalDmg":0.2635,"adjFinalDmgAnti":0.1535,"adjStunEnh":28,"adjStunAnti":28,"adjSilentEnh":28,"adjSilentAnti":28,"adjKnockEnh":28,"adjKnockAnti":28,"adjFrozenEnh":28,"adjFrozenAnti":28,"adjSlowEnh":28,"adjSlowAnti":28,"adjPushEnh":28,"adjPushAnti":28})
    }),
    51000085: _tools.RODict({
        "propID": 51000085,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3409,"adjMinPhysicalAtk":1360,"adjMaxPhysicalAtk":1360,"adjMinMagicAtk":1360,"adjMaxMagicAtk":1360,"adjAtkBless":3,"adjMinPhysicalArmor":742,"adjMaxPhysicalArmor":742,"adjMinMagicArmor":742,"adjMaxMagicArmor":742,"adjAccuracy":42,"adjEvasion":41,"adjFatal":69,"adjAntiFatal":51,"adjIgnoreArmor":0.2664,"adjDmgArmor":0.1264,"adjMortal":1.1502,"adjAntiMortal":0.5627,"adjMonsterDmg":0.758,"adjMonsterDmgAnti":0.5434,"adjFinalDmg":0.2664,"adjFinalDmgAnti":0.1564,"adjStunEnh":29,"adjStunAnti":29,"adjSilentEnh":29,"adjSilentAnti":29,"adjKnockEnh":29,"adjKnockAnti":29,"adjFrozenEnh":29,"adjFrozenAnti":29,"adjSlowEnh":29,"adjSlowAnti":29,"adjPushEnh":29,"adjPushAnti":29})
    }),
    51000086: _tools.RODict({
        "propID": 51000086,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3478,"adjMinPhysicalAtk":1385,"adjMaxPhysicalAtk":1385,"adjMinMagicAtk":1385,"adjMaxMagicAtk":1385,"adjAtkBless":3,"adjMinPhysicalArmor":755,"adjMaxPhysicalArmor":755,"adjMinMagicArmor":755,"adjMaxMagicArmor":755,"adjAccuracy":42,"adjEvasion":41,"adjFatal":69,"adjAntiFatal":51,"adjIgnoreArmor":0.2691,"adjDmgArmor":0.1291,"adjMortal":1.1544,"adjAntiMortal":0.5669,"adjMonsterDmg":0.7647,"adjMonsterDmgAnti":0.5495,"adjFinalDmg":0.2694,"adjFinalDmgAnti":0.1594,"adjStunEnh":29,"adjStunAnti":29,"adjSilentEnh":29,"adjSilentAnti":29,"adjKnockEnh":29,"adjKnockAnti":29,"adjFrozenEnh":29,"adjFrozenAnti":29,"adjSlowEnh":29,"adjSlowAnti":29,"adjPushEnh":29,"adjPushAnti":29})
    }),
    51000087: _tools.RODict({
        "propID": 51000087,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3547,"adjMinPhysicalAtk":1410,"adjMaxPhysicalAtk":1410,"adjMinMagicAtk":1410,"adjMaxMagicAtk":1410,"adjAtkBless":3,"adjMinPhysicalArmor":767,"adjMaxPhysicalArmor":767,"adjMinMagicArmor":767,"adjMaxMagicArmor":767,"adjAccuracy":43,"adjEvasion":42,"adjFatal":70,"adjAntiFatal":51,"adjIgnoreArmor":0.2718,"adjDmgArmor":0.1319,"adjMortal":1.1586,"adjAntiMortal":0.5711,"adjMonsterDmg":0.7714,"adjMonsterDmgAnti":0.5556,"adjFinalDmg":0.2724,"adjFinalDmgAnti":0.1624,"adjStunEnh":29,"adjStunAnti":29,"adjSilentEnh":29,"adjSilentAnti":29,"adjKnockEnh":29,"adjKnockAnti":29,"adjFrozenEnh":29,"adjFrozenAnti":29,"adjSlowEnh":29,"adjSlowAnti":29,"adjPushEnh":29,"adjPushAnti":29})
    }),
    51000088: _tools.RODict({
        "propID": 51000088,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3616,"adjMinPhysicalAtk":1435,"adjMaxPhysicalAtk":1435,"adjMinMagicAtk":1435,"adjMaxMagicAtk":1435,"adjAtkBless":3,"adjMinPhysicalArmor":780,"adjMaxPhysicalArmor":780,"adjMinMagicArmor":780,"adjMaxMagicArmor":780,"adjAccuracy":43,"adjEvasion":42,"adjFatal":70,"adjAntiFatal":51,"adjIgnoreArmor":0.2746,"adjDmgArmor":0.1346,"adjMortal":1.1628,"adjAntiMortal":0.5753,"adjMonsterDmg":0.7781,"adjMonsterDmgAnti":0.5618,"adjFinalDmg":0.2753,"adjFinalDmgAnti":0.1653,"adjStunEnh":30,"adjStunAnti":30,"adjSilentEnh":30,"adjSilentAnti":30,"adjKnockEnh":30,"adjKnockAnti":30,"adjFrozenEnh":30,"adjFrozenAnti":30,"adjSlowEnh":30,"adjSlowAnti":30,"adjPushEnh":30,"adjPushAnti":30})
    }),
    51000089: _tools.RODict({
        "propID": 51000089,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3686,"adjMinPhysicalAtk":1460,"adjMaxPhysicalAtk":1460,"adjMinMagicAtk":1460,"adjMaxMagicAtk":1460,"adjAtkBless":3,"adjMinPhysicalArmor":792,"adjMaxPhysicalArmor":792,"adjMinMagicArmor":792,"adjMaxMagicArmor":792,"adjAccuracy":43,"adjEvasion":43,"adjFatal":70,"adjAntiFatal":52,"adjIgnoreArmor":0.2773,"adjDmgArmor":0.1373,"adjMortal":1.167,"adjAntiMortal":0.5795,"adjMonsterDmg":0.7848,"adjMonsterDmgAnti":0.5679,"adjFinalDmg":0.2783,"adjFinalDmgAnti":0.1683,"adjStunEnh":30,"adjStunAnti":30,"adjSilentEnh":30,"adjSilentAnti":30,"adjKnockEnh":30,"adjKnockAnti":30,"adjFrozenEnh":30,"adjFrozenAnti":30,"adjSlowEnh":30,"adjSlowAnti":30,"adjPushEnh":30,"adjPushAnti":30})
    }),
    51000090: _tools.RODict({
        "propID": 51000090,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3756,"adjMinPhysicalAtk":1485,"adjMaxPhysicalAtk":1485,"adjMinMagicAtk":1485,"adjMaxMagicAtk":1485,"adjAtkBless":3,"adjMinPhysicalArmor":805,"adjMaxPhysicalArmor":805,"adjMinMagicArmor":805,"adjMaxMagicArmor":805,"adjAccuracy":44,"adjEvasion":43,"adjFatal":70,"adjAntiFatal":52,"adjIgnoreArmor":0.28,"adjDmgArmor":0.14,"adjMortal":1.1713,"adjAntiMortal":0.5837,"adjMonsterDmg":0.7915,"adjMonsterDmgAnti":0.574,"adjFinalDmg":0.2812,"adjFinalDmgAnti":0.1713,"adjStunEnh":30,"adjStunAnti":30,"adjSilentEnh":30,"adjSilentAnti":30,"adjKnockEnh":30,"adjKnockAnti":30,"adjFrozenEnh":30,"adjFrozenAnti":30,"adjSlowEnh":30,"adjSlowAnti":30,"adjPushEnh":30,"adjPushAnti":30})
    }),
    52004001: _tools.RODict({
        "propID": 52004001,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3500000,"adjMinPhysicalArmor":300,"adjMaxPhysicalArmor":300,"adjMinMagicArmor":300,"adjMaxMagicArmor":300})
    }),
    52004002: _tools.RODict({
        "propID": 52004002,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":6000000,"adjMinPhysicalArmor":400,"adjMaxPhysicalArmor":400,"adjMinMagicArmor":400,"adjMaxMagicArmor":400})
    }),
    52004003: _tools.RODict({
        "propID": 52004003,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":9000000,"adjMinPhysicalArmor":500,"adjMaxPhysicalArmor":500,"adjMinMagicArmor":500,"adjMaxMagicArmor":500})
    }),
    52004004: _tools.RODict({
        "propID": 52004004,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":18000000,"adjMinPhysicalArmor":700,"adjMaxPhysicalArmor":700,"adjMinMagicArmor":700,"adjMaxMagicArmor":700})
    }),
    52004005: _tools.RODict({
        "propID": 52004005,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":30000000,"adjMinPhysicalArmor":900,"adjMaxPhysicalArmor":900,"adjMinMagicArmor":900,"adjMaxMagicArmor":900})
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
        "propList": _tools.RODict({"adjFullHp":875000,"adjMinPhysicalArmor":300,"adjMaxPhysicalArmor":300,"adjMinMagicArmor":300,"adjMaxMagicArmor":300})
    }),
    52004012: _tools.RODict({
        "propID": 52004012,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1500000,"adjMinPhysicalArmor":400,"adjMaxPhysicalArmor":400,"adjMinMagicArmor":400,"adjMaxMagicArmor":400})
    }),
    52004013: _tools.RODict({
        "propID": 52004013,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2250000,"adjMinPhysicalArmor":500,"adjMaxPhysicalArmor":500,"adjMinMagicArmor":500,"adjMaxMagicArmor":500})
    }),
    52004014: _tools.RODict({
        "propID": 52004014,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4500000,"adjMinPhysicalArmor":700,"adjMaxPhysicalArmor":700,"adjMinMagicArmor":700,"adjMaxMagicArmor":700})
    }),
    52004015: _tools.RODict({
        "propID": 52004015,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":7500000,"adjMinPhysicalArmor":900,"adjMaxPhysicalArmor":900,"adjMinMagicArmor":900,"adjMaxMagicArmor":900})
    }),
    52004016: _tools.RODict({
        "propID": 52004016,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":437500,"adjMinPhysicalAtk":1000,"adjMaxPhysicalAtk":1000,"adjMinMagicAtk":1000,"adjMaxMagicAtk":1000,"adjMinPhysicalArmor":300,"adjMaxPhysicalArmor":300,"adjMinMagicArmor":300,"adjMaxMagicArmor":300})
    }),
    52004017: _tools.RODict({
        "propID": 52004017,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":750000,"adjMinPhysicalAtk":1500,"adjMaxPhysicalAtk":1500,"adjMinMagicAtk":1500,"adjMaxMagicAtk":1500,"adjMinPhysicalArmor":400,"adjMaxPhysicalArmor":400,"adjMinMagicArmor":400,"adjMaxMagicArmor":400})
    }),
    52004018: _tools.RODict({
        "propID": 52004018,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1125000,"adjMinPhysicalAtk":2000,"adjMaxPhysicalAtk":2000,"adjMinMagicAtk":2000,"adjMaxMagicAtk":2000,"adjMinPhysicalArmor":500,"adjMaxPhysicalArmor":500,"adjMinMagicArmor":500,"adjMaxMagicArmor":500})
    }),
    52004019: _tools.RODict({
        "propID": 52004019,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2250000,"adjMinPhysicalAtk":2500,"adjMaxPhysicalAtk":2500,"adjMinMagicAtk":2500,"adjMaxMagicAtk":2500,"adjMinPhysicalArmor":700,"adjMaxPhysicalArmor":700,"adjMinMagicArmor":700,"adjMaxMagicArmor":700})
    }),
    52004020: _tools.RODict({
        "propID": 52004020,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3750000,"adjMinPhysicalAtk":3000,"adjMaxPhysicalAtk":3000,"adjMinMagicAtk":3000,"adjMaxMagicAtk":3000,"adjMinPhysicalArmor":900,"adjMaxPhysicalArmor":900,"adjMinMagicArmor":900,"adjMaxMagicArmor":900})
    }),
    52004021: _tools.RODict({
        "propID": 52004021,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1750000,"adjMinPhysicalArmor":300,"adjMaxPhysicalArmor":300,"adjMinMagicArmor":300,"adjMaxMagicArmor":300})
    }),
    52004022: _tools.RODict({
        "propID": 52004022,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3000000,"adjMinPhysicalArmor":400,"adjMaxPhysicalArmor":400,"adjMinMagicArmor":400,"adjMaxMagicArmor":400})
    }),
    52004023: _tools.RODict({
        "propID": 52004023,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4500000,"adjMinPhysicalArmor":500,"adjMaxPhysicalArmor":500,"adjMinMagicArmor":500,"adjMaxMagicArmor":500})
    }),
    52004024: _tools.RODict({
        "propID": 52004024,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":9000000,"adjMinPhysicalArmor":600,"adjMaxPhysicalArmor":600,"adjMinMagicArmor":600,"adjMaxMagicArmor":600})
    }),
    52004025: _tools.RODict({
        "propID": 52004025,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":15000000,"adjMinPhysicalArmor":800,"adjMaxPhysicalArmor":800,"adjMinMagicArmor":800,"adjMaxMagicArmor":800})
    }),
    52004026: _tools.RODict({
        "propID": 52004026,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1750000,"adjMinPhysicalArmor":300,"adjMaxPhysicalArmor":300,"adjMinMagicArmor":300,"adjMaxMagicArmor":300})
    }),
    52004027: _tools.RODict({
        "propID": 52004027,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3000000,"adjMinPhysicalArmor":400,"adjMaxPhysicalArmor":400,"adjMinMagicArmor":400,"adjMaxMagicArmor":400})
    }),
    52004028: _tools.RODict({
        "propID": 52004028,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4500000,"adjMinPhysicalArmor":500,"adjMaxPhysicalArmor":500,"adjMinMagicArmor":500,"adjMaxMagicArmor":500})
    }),
    52004029: _tools.RODict({
        "propID": 52004029,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":9000000,"adjMinPhysicalArmor":600,"adjMaxPhysicalArmor":600,"adjMinMagicArmor":600,"adjMaxMagicArmor":600})
    }),
    52004030: _tools.RODict({
        "propID": 52004030,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":15000000,"adjMinPhysicalArmor":800,"adjMaxPhysicalArmor":800,"adjMinMagicArmor":800,"adjMaxMagicArmor":800})
    }),
    52004031: _tools.RODict({
        "propID": 52004031,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1750000,"adjMinPhysicalArmor":300,"adjMaxPhysicalArmor":300,"adjMinMagicArmor":300,"adjMaxMagicArmor":300})
    }),
    52004032: _tools.RODict({
        "propID": 52004032,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3000000,"adjMinPhysicalArmor":400,"adjMaxPhysicalArmor":400,"adjMinMagicArmor":400,"adjMaxMagicArmor":400})
    }),
    52004033: _tools.RODict({
        "propID": 52004033,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4500000,"adjMinPhysicalArmor":500,"adjMaxPhysicalArmor":500,"adjMinMagicArmor":500,"adjMaxMagicArmor":500})
    }),
    52004034: _tools.RODict({
        "propID": 52004034,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":9000000,"adjMinPhysicalArmor":600,"adjMaxPhysicalArmor":600,"adjMinMagicArmor":600,"adjMaxMagicArmor":600})
    }),
    52004035: _tools.RODict({
        "propID": 52004035,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":15000000,"adjMinPhysicalArmor":800,"adjMaxPhysicalArmor":800,"adjMinMagicArmor":800,"adjMaxMagicArmor":800})
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
        "propList": _tools.RODict({"adjMinMagicAtk":60,"adjMaxMagicAtk":125})
    }),
    52012151: _tools.RODict({
        "propID": 52012151,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":66,"adjMaxMagicAtk":137})
    }),
    52012152: _tools.RODict({
        "propID": 52012152,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":72,"adjMaxMagicAtk":150})
    }),
    52012153: _tools.RODict({
        "propID": 52012153,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":78,"adjMaxMagicAtk":163})
    }),
    52012154: _tools.RODict({
        "propID": 52012154,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":86,"adjMaxMagicAtk":179,"adjHit":13,"adjFinalDmg":0.04})
    }),
    52012155: _tools.RODict({
        "propID": 52012155,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":94,"adjMaxMagicAtk":197,"adjHit":14,"adjFinalDmg":0.04})
    }),
    52012156: _tools.RODict({
        "propID": 52012156,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":103,"adjMaxMagicAtk":215,"adjHit":15,"adjFinalDmg":0.04})
    }),
    52012157: _tools.RODict({
        "propID": 52012157,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":112,"adjMaxMagicAtk":233,"adjHit":16,"adjFinalDmg":0.04})
    }),
    52012158: _tools.RODict({
        "propID": 52012158,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":123,"adjMaxMagicAtk":256,"adjHit":18,"adjFinalDmg":0.08})
    }),
    52012159: _tools.RODict({
        "propID": 52012159,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":135,"adjMaxMagicAtk":281,"adjHit":19,"adjFinalDmg":0.08})
    }),
    52012160: _tools.RODict({
        "propID": 52012160,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":147,"adjMaxMagicAtk":307,"adjHit":20,"adjFinalDmg":0.08})
    }),
    52012161: _tools.RODict({
        "propID": 52012161,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":160,"adjMaxMagicAtk":333,"adjHit":22,"adjFinalDmg":0.08})
    }),
    52012162: _tools.RODict({
        "propID": 52012162,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":176,"adjMaxMagicAtk":366,"adjHit":25,"adjFinalDmg":0.08,"adjFinalDmgAnti":0.08})
    }),
    52012163: _tools.RODict({
        "propID": 52012163,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":194,"adjMaxMagicAtk":403,"adjHit":27,"adjFinalDmg":0.08,"adjFinalDmgAnti":0.08})
    }),
    52012164: _tools.RODict({
        "propID": 52012164,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":213,"adjMaxMagicAtk":443,"adjHit":29,"adjFinalDmg":0.08,"adjFinalDmgAnti":0.08})
    }),
    52012165: _tools.RODict({
        "propID": 52012165,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":234,"adjMaxMagicAtk":487,"adjHit":32,"adjFinalDmg":0.08,"adjFinalDmgAnti":0.08})
    }),
    52012326: _tools.RODict({
        "propID": 52012326,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":60,"adjMaxMagicAtk":125})
    }),
    52012327: _tools.RODict({
        "propID": 52012327,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":66,"adjMaxMagicAtk":137})
    }),
    52012328: _tools.RODict({
        "propID": 52012328,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":72,"adjMaxMagicAtk":150})
    }),
    52012329: _tools.RODict({
        "propID": 52012329,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":78,"adjMaxMagicAtk":163})
    }),
    52012330: _tools.RODict({
        "propID": 52012330,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":86,"adjMaxMagicAtk":179,"adjHit":13,"adjFinalDmg":0.04})
    }),
    52012331: _tools.RODict({
        "propID": 52012331,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":94,"adjMaxMagicAtk":197,"adjHit":14,"adjFinalDmg":0.04})
    }),
    52012332: _tools.RODict({
        "propID": 52012332,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":103,"adjMaxMagicAtk":215,"adjHit":15,"adjFinalDmg":0.04})
    }),
    52012333: _tools.RODict({
        "propID": 52012333,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":112,"adjMaxMagicAtk":233,"adjHit":16,"adjFinalDmg":0.04})
    }),
    52012334: _tools.RODict({
        "propID": 52012334,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":123,"adjMaxMagicAtk":256,"adjHit":18,"adjFinalDmg":0.08})
    }),
    52012335: _tools.RODict({
        "propID": 52012335,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":135,"adjMaxMagicAtk":281,"adjHit":19,"adjFinalDmg":0.08})
    }),
    52012336: _tools.RODict({
        "propID": 52012336,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":147,"adjMaxMagicAtk":307,"adjHit":20,"adjFinalDmg":0.08})
    }),
    52012337: _tools.RODict({
        "propID": 52012337,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":160,"adjMaxMagicAtk":333,"adjHit":22,"adjFinalDmg":0.08})
    }),
    52012338: _tools.RODict({
        "propID": 52012338,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":176,"adjMaxMagicAtk":366,"adjHit":25,"adjFinalDmg":0.08,"adjFinalDmgAnti":0.08})
    }),
    52012339: _tools.RODict({
        "propID": 52012339,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":194,"adjMaxMagicAtk":403,"adjHit":27,"adjFinalDmg":0.08,"adjFinalDmgAnti":0.08})
    }),
    52012340: _tools.RODict({
        "propID": 52012340,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":213,"adjMaxMagicAtk":443,"adjHit":29,"adjFinalDmg":0.08,"adjFinalDmgAnti":0.08})
    }),
    52012341: _tools.RODict({
        "propID": 52012341,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":234,"adjMaxMagicAtk":487,"adjHit":32,"adjFinalDmg":0.08,"adjFinalDmgAnti":0.08})
    }),
    52012502: _tools.RODict({
        "propID": 52012502,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":60,"adjMaxPhysicalAtk":125})
    }),
    52012503: _tools.RODict({
        "propID": 52012503,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":66,"adjMaxPhysicalAtk":137})
    }),
    52012504: _tools.RODict({
        "propID": 52012504,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":72,"adjMaxPhysicalAtk":150})
    }),
    52012505: _tools.RODict({
        "propID": 52012505,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":78,"adjMaxPhysicalAtk":163})
    }),
    52012506: _tools.RODict({
        "propID": 52012506,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":86,"adjMaxPhysicalAtk":179,"adjHit":13,"adjFinalDmg":0.04})
    }),
    52012507: _tools.RODict({
        "propID": 52012507,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":94,"adjMaxPhysicalAtk":197,"adjHit":14,"adjFinalDmg":0.04})
    }),
    52012508: _tools.RODict({
        "propID": 52012508,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":103,"adjMaxPhysicalAtk":215,"adjHit":15,"adjFinalDmg":0.04})
    }),
    52012509: _tools.RODict({
        "propID": 52012509,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":112,"adjMaxPhysicalAtk":233,"adjHit":16,"adjFinalDmg":0.04})
    }),
    52012510: _tools.RODict({
        "propID": 52012510,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":123,"adjMaxPhysicalAtk":256,"adjHit":18,"adjFinalDmg":0.08})
    }),
    52012511: _tools.RODict({
        "propID": 52012511,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":135,"adjMaxPhysicalAtk":281,"adjHit":19,"adjFinalDmg":0.08})
    }),
    52012512: _tools.RODict({
        "propID": 52012512,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":147,"adjMaxPhysicalAtk":307,"adjHit":20,"adjFinalDmg":0.08})
    }),
    52012513: _tools.RODict({
        "propID": 52012513,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":160,"adjMaxPhysicalAtk":333,"adjHit":22,"adjFinalDmg":0.08})
    }),
    52012514: _tools.RODict({
        "propID": 52012514,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":176,"adjMaxPhysicalAtk":366,"adjHit":25,"adjFinalDmg":0.08,"adjFinalDmgAnti":0.08})
    }),
    52012515: _tools.RODict({
        "propID": 52012515,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":194,"adjMaxPhysicalAtk":403,"adjHit":27,"adjFinalDmg":0.08,"adjFinalDmgAnti":0.08})
    }),
    52012516: _tools.RODict({
        "propID": 52012516,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":213,"adjMaxPhysicalAtk":443,"adjHit":29,"adjFinalDmg":0.08,"adjFinalDmgAnti":0.08})
    }),
    52012517: _tools.RODict({
        "propID": 52012517,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":234,"adjMaxPhysicalAtk":487,"adjHit":32,"adjFinalDmg":0.08,"adjFinalDmgAnti":0.08})
    }),
    52012678: _tools.RODict({
        "propID": 52012678,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":62,"adjMaxPhysicalArmor":71,"adjMinMagicArmor":62,"adjMaxMagicArmor":71})
    }),
    52012679: _tools.RODict({
        "propID": 52012679,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":68,"adjMaxPhysicalArmor":78,"adjMinMagicArmor":68,"adjMaxMagicArmor":78})
    }),
    52012680: _tools.RODict({
        "propID": 52012680,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":74,"adjMaxPhysicalArmor":85,"adjMinMagicArmor":74,"adjMaxMagicArmor":85})
    }),
    52012681: _tools.RODict({
        "propID": 52012681,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":81,"adjMaxPhysicalArmor":92,"adjMinMagicArmor":81,"adjMaxMagicArmor":92})
    }),
    52012682: _tools.RODict({
        "propID": 52012682,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":89,"adjMaxPhysicalArmor":101,"adjMinMagicArmor":89,"adjMaxMagicArmor":101,"adjMortal":0.15})
    }),
    52012683: _tools.RODict({
        "propID": 52012683,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":98,"adjMaxPhysicalArmor":111,"adjMinMagicArmor":98,"adjMaxMagicArmor":111,"adjMortal":0.15})
    }),
    52012684: _tools.RODict({
        "propID": 52012684,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":107,"adjMaxPhysicalArmor":121,"adjMinMagicArmor":107,"adjMaxMagicArmor":121,"adjMortal":0.15})
    }),
    52012685: _tools.RODict({
        "propID": 52012685,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":116,"adjMaxPhysicalArmor":131,"adjMinMagicArmor":116,"adjMaxMagicArmor":131,"adjMortal":0.15})
    }),
    52012686: _tools.RODict({
        "propID": 52012686,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":128,"adjMaxPhysicalArmor":144,"adjMinMagicArmor":128,"adjMaxMagicArmor":144,"adjMortal":0.3})
    }),
    52012687: _tools.RODict({
        "propID": 52012687,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":140,"adjMaxPhysicalArmor":157,"adjMinMagicArmor":140,"adjMaxMagicArmor":157,"adjMortal":0.3})
    }),
    52012688: _tools.RODict({
        "propID": 52012688,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":153,"adjMaxPhysicalArmor":172,"adjMinMagicArmor":153,"adjMaxMagicArmor":172,"adjMortal":0.3})
    }),
    52012689: _tools.RODict({
        "propID": 52012689,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":166,"adjMaxPhysicalArmor":187,"adjMinMagicArmor":166,"adjMaxMagicArmor":187,"adjMortal":0.3})
    }),
    52012690: _tools.RODict({
        "propID": 52012690,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":183,"adjMaxPhysicalArmor":206,"adjMinMagicArmor":183,"adjMaxMagicArmor":206,"adjMortal":0.3,"adjAntiMortal":0.3})
    }),
    52012691: _tools.RODict({
        "propID": 52012691,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":201,"adjMaxPhysicalArmor":227,"adjMinMagicArmor":201,"adjMaxMagicArmor":227,"adjMortal":0.3,"adjAntiMortal":0.3})
    }),
    52012692: _tools.RODict({
        "propID": 52012692,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":221,"adjMaxPhysicalArmor":250,"adjMinMagicArmor":221,"adjMaxMagicArmor":250,"adjMortal":0.3,"adjAntiMortal":0.3})
    }),
    52012693: _tools.RODict({
        "propID": 52012693,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":243,"adjMaxPhysicalArmor":275,"adjMinMagicArmor":243,"adjMaxMagicArmor":275,"adjMortal":0.3,"adjAntiMortal":0.3})
    }),
    52012854: _tools.RODict({
        "propID": 52012854,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":28,"adjMaxMagicArmor":30})
    }),
    52012855: _tools.RODict({
        "propID": 52012855,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":31,"adjMaxMagicArmor":33})
    }),
    52012856: _tools.RODict({
        "propID": 52012856,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":34,"adjMaxMagicArmor":36})
    }),
    52012857: _tools.RODict({
        "propID": 52012857,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":37,"adjMaxMagicArmor":39})
    }),
    52012858: _tools.RODict({
        "propID": 52012858,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":40,"adjMaxMagicArmor":43,"adjAntiFatal":12,"adjMortal":0.125})
    }),
    52012859: _tools.RODict({
        "propID": 52012859,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":44,"adjMaxMagicArmor":47,"adjAntiFatal":13,"adjMortal":0.125})
    }),
    52012860: _tools.RODict({
        "propID": 52012860,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":48,"adjMaxMagicArmor":51,"adjAntiFatal":14,"adjMortal":0.125})
    }),
    52012861: _tools.RODict({
        "propID": 52012861,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":52,"adjMaxMagicArmor":56,"adjAntiFatal":15,"adjMortal":0.125})
    }),
    52012862: _tools.RODict({
        "propID": 52012862,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":57,"adjMaxMagicArmor":62,"adjAntiFatal":17,"adjMortal":0.25})
    }),
    52012863: _tools.RODict({
        "propID": 52012863,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":62,"adjMaxMagicArmor":68,"adjAntiFatal":18,"adjMortal":0.25})
    }),
    52012864: _tools.RODict({
        "propID": 52012864,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":68,"adjMaxMagicArmor":74,"adjAntiFatal":19,"adjMortal":0.25})
    }),
    52012865: _tools.RODict({
        "propID": 52012865,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":74,"adjMaxMagicArmor":81,"adjAntiFatal":21,"adjMortal":0.25})
    }),
    52012866: _tools.RODict({
        "propID": 52012866,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":81,"adjMaxMagicArmor":89,"adjAntiFatal":24,"adjMortal":0.25,"adjAntiMortal":0.25})
    }),
    52012867: _tools.RODict({
        "propID": 52012867,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":89,"adjMaxMagicArmor":98,"adjAntiFatal":26,"adjMortal":0.25,"adjAntiMortal":0.25})
    }),
    52012868: _tools.RODict({
        "propID": 52012868,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":98,"adjMaxMagicArmor":108,"adjAntiFatal":28,"adjMortal":0.25,"adjAntiMortal":0.25})
    }),
    52012869: _tools.RODict({
        "propID": 52012869,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":108,"adjMaxMagicArmor":119,"adjAntiFatal":31,"adjMortal":0.25,"adjAntiMortal":0.25})
    }),
    52013030: _tools.RODict({
        "propID": 52013030,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":28,"adjMaxPhysicalArmor":30})
    }),
    52013031: _tools.RODict({
        "propID": 52013031,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":31,"adjMaxPhysicalArmor":33})
    }),
    52013032: _tools.RODict({
        "propID": 52013032,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":34,"adjMaxPhysicalArmor":36})
    }),
    52013033: _tools.RODict({
        "propID": 52013033,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":37,"adjMaxPhysicalArmor":39})
    }),
    52013034: _tools.RODict({
        "propID": 52013034,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":40,"adjMaxPhysicalArmor":43,"adjDodge":12,"adjPVPDmg":0.05})
    }),
    52013035: _tools.RODict({
        "propID": 52013035,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":44,"adjMaxPhysicalArmor":47,"adjDodge":13,"adjPVPDmg":0.05})
    }),
    52013036: _tools.RODict({
        "propID": 52013036,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":48,"adjMaxPhysicalArmor":51,"adjDodge":14,"adjPVPDmg":0.05})
    }),
    52013037: _tools.RODict({
        "propID": 52013037,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":52,"adjMaxPhysicalArmor":56,"adjDodge":15,"adjPVPDmg":0.05})
    }),
    52013038: _tools.RODict({
        "propID": 52013038,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":57,"adjMaxPhysicalArmor":62,"adjDodge":17,"adjPVPDmg":0.1})
    }),
    52013039: _tools.RODict({
        "propID": 52013039,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":62,"adjMaxPhysicalArmor":68,"adjDodge":18,"adjPVPDmg":0.1})
    }),
    52013040: _tools.RODict({
        "propID": 52013040,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":68,"adjMaxPhysicalArmor":74,"adjDodge":19,"adjPVPDmg":0.1})
    }),
    52013041: _tools.RODict({
        "propID": 52013041,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":74,"adjMaxPhysicalArmor":81,"adjDodge":21,"adjPVPDmg":0.1})
    }),
    52013042: _tools.RODict({
        "propID": 52013042,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":81,"adjMaxPhysicalArmor":89,"adjDodge":24,"adjPVPDmg":0.1,"adjPVPDmgAnti":0.1})
    }),
    52013043: _tools.RODict({
        "propID": 52013043,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":89,"adjMaxPhysicalArmor":98,"adjDodge":26,"adjPVPDmg":0.1,"adjPVPDmgAnti":0.1})
    }),
    52013044: _tools.RODict({
        "propID": 52013044,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":98,"adjMaxPhysicalArmor":108,"adjDodge":28,"adjPVPDmg":0.1,"adjPVPDmgAnti":0.1})
    }),
    52013045: _tools.RODict({
        "propID": 52013045,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":108,"adjMaxPhysicalArmor":119,"adjDodge":31,"adjPVPDmg":0.1,"adjPVPDmgAnti":0.1})
    }),
    52013206: _tools.RODict({
        "propID": 52013206,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":50})
    }),
    52013207: _tools.RODict({
        "propID": 52013207,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":33,"adjMaxPhysicalAtk":55})
    }),
    52013208: _tools.RODict({
        "propID": 52013208,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":36,"adjMaxPhysicalAtk":60})
    }),
    52013209: _tools.RODict({
        "propID": 52013209,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":39,"adjMaxPhysicalAtk":65})
    }),
    52013210: _tools.RODict({
        "propID": 52013210,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":43,"adjMaxPhysicalAtk":72,"adjFatal":12,"adjIgnoreArmor":0.02})
    }),
    52013211: _tools.RODict({
        "propID": 52013211,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":47,"adjMaxPhysicalAtk":79,"adjFatal":13,"adjIgnoreArmor":0.02})
    }),
    52013212: _tools.RODict({
        "propID": 52013212,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":51,"adjMaxPhysicalAtk":86,"adjFatal":14,"adjIgnoreArmor":0.02})
    }),
    52013213: _tools.RODict({
        "propID": 52013213,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":56,"adjMaxPhysicalAtk":94,"adjFatal":15,"adjIgnoreArmor":0.02})
    }),
    52013214: _tools.RODict({
        "propID": 52013214,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":62,"adjMaxPhysicalAtk":103,"adjFatal":17,"adjIgnoreArmor":0.04})
    }),
    52013215: _tools.RODict({
        "propID": 52013215,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":68,"adjMaxPhysicalAtk":113,"adjFatal":18,"adjIgnoreArmor":0.04})
    }),
    52013216: _tools.RODict({
        "propID": 52013216,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":74,"adjMaxPhysicalAtk":123,"adjFatal":19,"adjIgnoreArmor":0.04})
    }),
    52013217: _tools.RODict({
        "propID": 52013217,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":81,"adjMaxPhysicalAtk":134,"adjFatal":21,"adjIgnoreArmor":0.04})
    }),
    52013218: _tools.RODict({
        "propID": 52013218,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":89,"adjMaxPhysicalAtk":147,"adjFatal":24,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013219: _tools.RODict({
        "propID": 52013219,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":98,"adjMaxPhysicalAtk":162,"adjFatal":26,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013220: _tools.RODict({
        "propID": 52013220,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":108,"adjMaxPhysicalAtk":178,"adjFatal":28,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013221: _tools.RODict({
        "propID": 52013221,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":119,"adjMaxPhysicalAtk":196,"adjFatal":31,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013382: _tools.RODict({
        "propID": 52013382,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":30,"adjMaxMagicAtk":50})
    }),
    52013383: _tools.RODict({
        "propID": 52013383,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":33,"adjMaxMagicAtk":55})
    }),
    52013384: _tools.RODict({
        "propID": 52013384,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":36,"adjMaxMagicAtk":60})
    }),
    52013385: _tools.RODict({
        "propID": 52013385,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":39,"adjMaxMagicAtk":65})
    }),
    52013386: _tools.RODict({
        "propID": 52013386,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":43,"adjMaxMagicAtk":72,"adjFatal":12,"adjIgnoreArmor":0.02})
    }),
    52013387: _tools.RODict({
        "propID": 52013387,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":47,"adjMaxMagicAtk":79,"adjFatal":13,"adjIgnoreArmor":0.02})
    }),
    52013388: _tools.RODict({
        "propID": 52013388,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":51,"adjMaxMagicAtk":86,"adjFatal":14,"adjIgnoreArmor":0.02})
    }),
    52013389: _tools.RODict({
        "propID": 52013389,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":56,"adjMaxMagicAtk":94,"adjFatal":15,"adjIgnoreArmor":0.02})
    }),
    52013390: _tools.RODict({
        "propID": 52013390,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":62,"adjMaxMagicAtk":103,"adjFatal":17,"adjIgnoreArmor":0.04})
    }),
    52013391: _tools.RODict({
        "propID": 52013391,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":68,"adjMaxMagicAtk":113,"adjFatal":18,"adjIgnoreArmor":0.04})
    }),
    52013392: _tools.RODict({
        "propID": 52013392,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":74,"adjMaxMagicAtk":123,"adjFatal":19,"adjIgnoreArmor":0.04})
    }),
    52013393: _tools.RODict({
        "propID": 52013393,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":81,"adjMaxMagicAtk":134,"adjFatal":21,"adjIgnoreArmor":0.04})
    }),
    52013394: _tools.RODict({
        "propID": 52013394,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":89,"adjMaxMagicAtk":147,"adjFatal":24,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013395: _tools.RODict({
        "propID": 52013395,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":98,"adjMaxMagicAtk":162,"adjFatal":26,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013396: _tools.RODict({
        "propID": 52013396,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":108,"adjMaxMagicAtk":178,"adjFatal":28,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013397: _tools.RODict({
        "propID": 52013397,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":119,"adjMaxMagicAtk":196,"adjFatal":31,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013558: _tools.RODict({
        "propID": 52013558,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":170,"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":46})
    }),
    52013559: _tools.RODict({
        "propID": 52013559,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":187,"adjMinPhysicalAtk":33,"adjMaxPhysicalAtk":50})
    }),
    52013560: _tools.RODict({
        "propID": 52013560,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":204,"adjMinPhysicalAtk":36,"adjMaxPhysicalAtk":54})
    }),
    52013561: _tools.RODict({
        "propID": 52013561,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":221,"adjMinPhysicalAtk":39,"adjMaxPhysicalAtk":59})
    }),
    52013562: _tools.RODict({
        "propID": 52013562,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":243,"adjMinPhysicalAtk":43,"adjMaxPhysicalAtk":65,"adjIgnoreArmor":0.025})
    }),
    52013563: _tools.RODict({
        "propID": 52013563,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":267,"adjMinPhysicalAtk":47,"adjMaxPhysicalAtk":71,"adjIgnoreArmor":0.025})
    }),
    52013564: _tools.RODict({
        "propID": 52013564,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":291,"adjMinPhysicalAtk":51,"adjMaxPhysicalAtk":78,"adjIgnoreArmor":0.025})
    }),
    52013565: _tools.RODict({
        "propID": 52013565,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":316,"adjMinPhysicalAtk":56,"adjMaxPhysicalAtk":85,"adjIgnoreArmor":0.025})
    }),
    52013566: _tools.RODict({
        "propID": 52013566,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":348,"adjMinPhysicalAtk":62,"adjMaxPhysicalAtk":94,"adjIgnoreArmor":0.05})
    }),
    52013567: _tools.RODict({
        "propID": 52013567,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":382,"adjMinPhysicalAtk":68,"adjMaxPhysicalAtk":103,"adjIgnoreArmor":0.05})
    }),
    52013568: _tools.RODict({
        "propID": 52013568,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":417,"adjMinPhysicalAtk":74,"adjMaxPhysicalAtk":112,"adjIgnoreArmor":0.05})
    }),
    52013569: _tools.RODict({
        "propID": 52013569,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":452,"adjMinPhysicalAtk":81,"adjMaxPhysicalAtk":122,"adjIgnoreArmor":0.05})
    }),
    52013570: _tools.RODict({
        "propID": 52013570,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":497,"adjMinPhysicalAtk":89,"adjMaxPhysicalAtk":134,"adjIgnoreArmor":0.05,"adjDmgArmor":0.05})
    }),
    52013571: _tools.RODict({
        "propID": 52013571,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":547,"adjMinPhysicalAtk":98,"adjMaxPhysicalAtk":147,"adjIgnoreArmor":0.05,"adjDmgArmor":0.05})
    }),
    52013572: _tools.RODict({
        "propID": 52013572,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":602,"adjMinPhysicalAtk":108,"adjMaxPhysicalAtk":162,"adjIgnoreArmor":0.05,"adjDmgArmor":0.05})
    }),
    52013573: _tools.RODict({
        "propID": 52013573,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":662,"adjMinPhysicalAtk":119,"adjMaxPhysicalAtk":178,"adjIgnoreArmor":0.05,"adjDmgArmor":0.05})
    }),
    52013734: _tools.RODict({
        "propID": 52013734,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":170,"adjMinMagicAtk":30,"adjMaxMagicAtk":46})
    }),
    52013735: _tools.RODict({
        "propID": 52013735,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":187,"adjMinMagicAtk":33,"adjMaxMagicAtk":50})
    }),
    52013736: _tools.RODict({
        "propID": 52013736,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":204,"adjMinMagicAtk":36,"adjMaxMagicAtk":54})
    }),
    52013737: _tools.RODict({
        "propID": 52013737,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":221,"adjMinMagicAtk":39,"adjMaxMagicAtk":59})
    }),
    52013738: _tools.RODict({
        "propID": 52013738,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":243,"adjMinMagicAtk":43,"adjMaxMagicAtk":65,"adjIgnoreArmor":0.025})
    }),
    52013739: _tools.RODict({
        "propID": 52013739,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":267,"adjMinMagicAtk":47,"adjMaxMagicAtk":71,"adjIgnoreArmor":0.025})
    }),
    52013740: _tools.RODict({
        "propID": 52013740,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":291,"adjMinMagicAtk":51,"adjMaxMagicAtk":78,"adjIgnoreArmor":0.025})
    }),
    52013741: _tools.RODict({
        "propID": 52013741,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":316,"adjMinMagicAtk":56,"adjMaxMagicAtk":85,"adjIgnoreArmor":0.025})
    }),
    52013742: _tools.RODict({
        "propID": 52013742,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":348,"adjMinMagicAtk":62,"adjMaxMagicAtk":94,"adjIgnoreArmor":0.05})
    }),
    52013743: _tools.RODict({
        "propID": 52013743,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":382,"adjMinMagicAtk":68,"adjMaxMagicAtk":103,"adjIgnoreArmor":0.05})
    }),
    52013744: _tools.RODict({
        "propID": 52013744,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":417,"adjMinMagicAtk":74,"adjMaxMagicAtk":112,"adjIgnoreArmor":0.05})
    }),
    52013745: _tools.RODict({
        "propID": 52013745,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":452,"adjMinMagicAtk":81,"adjMaxMagicAtk":122,"adjIgnoreArmor":0.05})
    }),
    52013746: _tools.RODict({
        "propID": 52013746,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":497,"adjMinMagicAtk":89,"adjMaxMagicAtk":134,"adjIgnoreArmor":0.05,"adjDmgArmor":0.05})
    }),
    52013747: _tools.RODict({
        "propID": 52013747,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":547,"adjMinMagicAtk":98,"adjMaxMagicAtk":147,"adjIgnoreArmor":0.05,"adjDmgArmor":0.05})
    }),
    52013748: _tools.RODict({
        "propID": 52013748,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":602,"adjMinMagicAtk":108,"adjMaxMagicAtk":162,"adjIgnoreArmor":0.05,"adjDmgArmor":0.05})
    }),
    52013749: _tools.RODict({
        "propID": 52013749,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":662,"adjMinMagicAtk":119,"adjMaxMagicAtk":178,"adjIgnoreArmor":0.05,"adjDmgArmor":0.05})
    }),
    52013910: _tools.RODict({
        "propID": 52013910,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1800,"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":36})
    }),
    52013911: _tools.RODict({
        "propID": 52013911,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1980,"adjMinPhysicalAtk":18,"adjMaxPhysicalAtk":39})
    }),
    52013912: _tools.RODict({
        "propID": 52013912,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2160,"adjMinPhysicalAtk":19,"adjMaxPhysicalAtk":42})
    }),
    52013913: _tools.RODict({
        "propID": 52013913,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2340,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":46})
    }),
    52013914: _tools.RODict({
        "propID": 52013914,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2574,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":51,"adjMonsterDmg":0.04})
    }),
    52013915: _tools.RODict({
        "propID": 52013915,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2831,"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":56,"adjMonsterDmg":0.04})
    }),
    52013916: _tools.RODict({
        "propID": 52013916,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3088,"adjMinPhysicalAtk":27,"adjMaxPhysicalAtk":61,"adjMonsterDmg":0.04})
    }),
    52013917: _tools.RODict({
        "propID": 52013917,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3346,"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":66,"adjMonsterDmg":0.04})
    }),
    52013918: _tools.RODict({
        "propID": 52013918,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4015,"adjMinPhysicalAtk":33,"adjMaxPhysicalAtk":73,"adjMonsterDmg":0.08})
    }),
    52013919: _tools.RODict({
        "propID": 52013919,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4416,"adjMinPhysicalAtk":36,"adjMaxPhysicalAtk":80,"adjMonsterDmg":0.08})
    }),
    52013920: _tools.RODict({
        "propID": 52013920,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4818,"adjMinPhysicalAtk":39,"adjMaxPhysicalAtk":87,"adjMonsterDmg":0.08})
    }),
    52013921: _tools.RODict({
        "propID": 52013921,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5220,"adjMinPhysicalAtk":43,"adjMaxPhysicalAtk":95,"adjMonsterDmg":0.08})
    }),
    52013922: _tools.RODict({
        "propID": 52013922,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5742,"adjMinPhysicalAtk":47,"adjMaxPhysicalAtk":105,"adjMonsterDmg":0.08,"adjMonsterDmgAnti":0.08})
    }),
    52013923: _tools.RODict({
        "propID": 52013923,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":6316,"adjMinPhysicalAtk":52,"adjMaxPhysicalAtk":116,"adjMonsterDmg":0.08,"adjMonsterDmgAnti":0.08})
    }),
    52013924: _tools.RODict({
        "propID": 52013924,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":6948,"adjMinPhysicalAtk":57,"adjMaxPhysicalAtk":128,"adjMonsterDmg":0.08,"adjMonsterDmgAnti":0.08})
    }),
    52013925: _tools.RODict({
        "propID": 52013925,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":7643,"adjMinPhysicalAtk":63,"adjMaxPhysicalAtk":141,"adjMonsterDmg":0.08,"adjMonsterDmgAnti":0.08})
    }),
    52014086: _tools.RODict({
        "propID": 52014086,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1800,"adjMinMagicAtk":17,"adjMaxMagicAtk":36})
    }),
    52014087: _tools.RODict({
        "propID": 52014087,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1980,"adjMinMagicAtk":18,"adjMaxMagicAtk":39})
    }),
    52014088: _tools.RODict({
        "propID": 52014088,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2160,"adjMinMagicAtk":19,"adjMaxMagicAtk":42})
    }),
    52014089: _tools.RODict({
        "propID": 52014089,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2340,"adjMinMagicAtk":21,"adjMaxMagicAtk":46})
    }),
    52014090: _tools.RODict({
        "propID": 52014090,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2574,"adjMinMagicAtk":23,"adjMaxMagicAtk":51,"adjMonsterDmg":0.04})
    }),
    52014091: _tools.RODict({
        "propID": 52014091,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2831,"adjMinMagicAtk":25,"adjMaxMagicAtk":56,"adjMonsterDmg":0.04})
    }),
    52014092: _tools.RODict({
        "propID": 52014092,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3088,"adjMinMagicAtk":27,"adjMaxMagicAtk":61,"adjMonsterDmg":0.04})
    }),
    52014093: _tools.RODict({
        "propID": 52014093,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3346,"adjMinMagicAtk":30,"adjMaxMagicAtk":66,"adjMonsterDmg":0.04})
    }),
    52014094: _tools.RODict({
        "propID": 52014094,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4015,"adjMinMagicAtk":33,"adjMaxMagicAtk":73,"adjMonsterDmg":0.08})
    }),
    52014095: _tools.RODict({
        "propID": 52014095,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4416,"adjMinMagicAtk":36,"adjMaxMagicAtk":80,"adjMonsterDmg":0.08})
    }),
    52014096: _tools.RODict({
        "propID": 52014096,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4818,"adjMinMagicAtk":39,"adjMaxMagicAtk":87,"adjMonsterDmg":0.08})
    }),
    52014097: _tools.RODict({
        "propID": 52014097,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5220,"adjMinMagicAtk":43,"adjMaxMagicAtk":95,"adjMonsterDmg":0.08})
    }),
    52014098: _tools.RODict({
        "propID": 52014098,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5742,"adjMinMagicAtk":47,"adjMaxMagicAtk":105,"adjMonsterDmg":0.08,"adjMonsterDmgAnti":0.08})
    }),
    52014099: _tools.RODict({
        "propID": 52014099,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":6316,"adjMinMagicAtk":52,"adjMaxMagicAtk":116,"adjMonsterDmg":0.08,"adjMonsterDmgAnti":0.08})
    }),
    52014100: _tools.RODict({
        "propID": 52014100,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":6948,"adjMinMagicAtk":57,"adjMaxMagicAtk":128,"adjMonsterDmg":0.08,"adjMonsterDmgAnti":0.08})
    }),
    52014101: _tools.RODict({
        "propID": 52014101,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":7643,"adjMinMagicAtk":63,"adjMaxMagicAtk":141,"adjMonsterDmg":0.08,"adjMonsterDmgAnti":0.08})
    }),
    52014262: _tools.RODict({
        "propID": 52014262,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4000,"adjDrugsQuantity":5})
    }),
    52014263: _tools.RODict({
        "propID": 52014263,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4400,"adjDrugsQuantity":6})
    }),
    52014264: _tools.RODict({
        "propID": 52014264,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4800,"adjDrugsQuantity":7})
    }),
    52014265: _tools.RODict({
        "propID": 52014265,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5200,"adjDrugsQuantity":8})
    }),
    52014266: _tools.RODict({
        "propID": 52014266,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5720,"adjDrugsQuantity":10,"adjFinalDmg":0.015})
    }),
    52014267: _tools.RODict({
        "propID": 52014267,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":6292,"adjDrugsQuantity":11,"adjFinalDmg":0.015})
    }),
    52014268: _tools.RODict({
        "propID": 52014268,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":6864,"adjDrugsQuantity":12,"adjFinalDmg":0.015})
    }),
    52014269: _tools.RODict({
        "propID": 52014269,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":7436,"adjDrugsQuantity":14,"adjFinalDmg":0.015})
    }),
    52014270: _tools.RODict({
        "propID": 52014270,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":8923,"adjDrugsQuantity":16,"adjFinalDmg":0.03})
    }),
    52014271: _tools.RODict({
        "propID": 52014271,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":9815,"adjDrugsQuantity":18,"adjFinalDmg":0.03})
    }),
    52014272: _tools.RODict({
        "propID": 52014272,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":10707,"adjDrugsQuantity":20,"adjFinalDmg":0.03})
    }),
    52014273: _tools.RODict({
        "propID": 52014273,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":11600,"adjDrugsQuantity":22,"adjFinalDmg":0.03})
    }),
    52014274: _tools.RODict({
        "propID": 52014274,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":12760,"adjDrugsQuantity":24,"adjFinalDmg":0.03,"adjFinalDmgAnti":0.03})
    }),
    52014275: _tools.RODict({
        "propID": 52014275,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":14036,"adjDrugsQuantity":26,"adjFinalDmg":0.03,"adjFinalDmgAnti":0.03})
    }),
    52014276: _tools.RODict({
        "propID": 52014276,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":15440,"adjDrugsQuantity":28,"adjFinalDmg":0.03,"adjFinalDmgAnti":0.03})
    }),
    52014277: _tools.RODict({
        "propID": 52014277,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":16984,"adjDrugsQuantity":31,"adjFinalDmg":0.03,"adjFinalDmgAnti":0.03})
    })
})
minKey = 51000001
maxKey = 52014277