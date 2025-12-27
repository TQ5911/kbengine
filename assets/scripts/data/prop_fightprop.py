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
        "propList": _tools.RODict({"adjFullHp":20000,"adjFullMp":10000,"adjMinPhysicalAtk":100,"adjMaxPhysicalAtk":200,"adjMinMagicAtk":100,"adjMaxMagicAtk":200,"mulFullHp":1.0,"adjRealDmgDef":50})
    }),
    51000001: _tools.RODict({
        "propID": 51000001,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":50,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":21,"adjMinMagicAtk":21,"adjMaxMagicAtk":21,"adjMinPhysicalArmor":15,"adjMaxPhysicalArmor":15,"adjMinMagicArmor":15,"adjMaxMagicArmor":15,"adjHit":1,"adjDodge":1,"adjRealDmg":1,"adjRealDmgDef":1,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000002: _tools.RODict({
        "propID": 51000002,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":52,"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":24,"adjMinMagicAtk":24,"adjMaxMagicAtk":24,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjHit":1,"adjDodge":1,"adjRealDmg":2,"adjRealDmgDef":2,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000003: _tools.RODict({
        "propID": 51000003,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":54,"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":26,"adjMinMagicAtk":26,"adjMaxMagicAtk":26,"adjMinPhysicalArmor":17,"adjMaxPhysicalArmor":17,"adjMinMagicArmor":17,"adjMaxMagicArmor":17,"adjHit":2,"adjDodge":2,"adjRealDmg":3,"adjRealDmgDef":3,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000004: _tools.RODict({
        "propID": 51000004,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":56,"adjMinPhysicalAtk":28,"adjMaxPhysicalAtk":28,"adjMinMagicAtk":28,"adjMaxMagicAtk":28,"adjMinPhysicalArmor":18,"adjMaxPhysicalArmor":18,"adjMinMagicArmor":18,"adjMaxMagicArmor":18,"adjHit":2,"adjDodge":2,"adjRealDmg":4,"adjRealDmgDef":4,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000005: _tools.RODict({
        "propID": 51000005,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":58,"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":32,"adjMinMagicAtk":32,"adjMaxMagicAtk":32,"adjMinPhysicalArmor":19,"adjMaxPhysicalArmor":19,"adjMinMagicArmor":19,"adjMaxMagicArmor":19,"adjHit":3,"adjDodge":3,"adjRealDmg":5,"adjRealDmgDef":5,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000006: _tools.RODict({
        "propID": 51000006,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":60,"adjMinPhysicalAtk":65,"adjMaxPhysicalAtk":65,"adjMinMagicAtk":65,"adjMaxMagicAtk":65,"adjMinPhysicalArmor":20,"adjMaxPhysicalArmor":20,"adjMinMagicArmor":20,"adjMaxMagicArmor":20,"adjHit":3,"adjDodge":3,"adjRealDmg":6,"adjRealDmgDef":6,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000007: _tools.RODict({
        "propID": 51000007,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":62,"adjMinPhysicalAtk":80,"adjMaxPhysicalAtk":80,"adjMinMagicAtk":80,"adjMaxMagicAtk":80,"adjMinPhysicalArmor":21,"adjMaxPhysicalArmor":21,"adjMinMagicArmor":21,"adjMaxMagicArmor":21,"adjHit":4,"adjDodge":4,"adjRealDmg":7,"adjRealDmgDef":7,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000008: _tools.RODict({
        "propID": 51000008,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":64,"adjMinPhysicalAtk":98,"adjMaxPhysicalAtk":98,"adjMinMagicAtk":98,"adjMaxMagicAtk":98,"adjMinPhysicalArmor":32,"adjMaxPhysicalArmor":32,"adjMinMagicArmor":32,"adjMaxMagicArmor":32,"adjHit":4,"adjDodge":4,"adjRealDmg":8,"adjRealDmgDef":8,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000009: _tools.RODict({
        "propID": 51000009,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":66,"adjMinPhysicalAtk":105,"adjMaxPhysicalAtk":105,"adjMinMagicAtk":105,"adjMaxMagicAtk":105,"adjMinPhysicalArmor":122,"adjMaxPhysicalArmor":122,"adjMinMagicArmor":122,"adjMaxMagicArmor":122,"adjHit":5,"adjDodge":5,"adjRealDmg":9,"adjRealDmgDef":9,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000010: _tools.RODict({
        "propID": 51000010,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":68,"adjMinPhysicalAtk":112,"adjMaxPhysicalAtk":112,"adjMinMagicAtk":112,"adjMaxMagicAtk":112,"adjMinPhysicalArmor":124,"adjMaxPhysicalArmor":124,"adjMinMagicArmor":124,"adjMaxMagicArmor":124,"adjHit":5,"adjDodge":5,"adjRealDmg":10,"adjRealDmgDef":10,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000011: _tools.RODict({
        "propID": 51000011,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":70,"adjMinPhysicalAtk":120,"adjMaxPhysicalAtk":120,"adjMinMagicAtk":120,"adjMaxMagicAtk":120,"adjMinPhysicalArmor":132,"adjMaxPhysicalArmor":132,"adjMinMagicArmor":132,"adjMaxMagicArmor":132,"adjHit":6,"adjDodge":6,"adjRealDmg":11,"adjRealDmgDef":11,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000012: _tools.RODict({
        "propID": 51000012,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":75,"adjMinPhysicalAtk":127,"adjMaxPhysicalAtk":127,"adjMinMagicAtk":127,"adjMaxMagicAtk":127,"adjMinPhysicalArmor":134,"adjMaxPhysicalArmor":134,"adjMinMagicArmor":134,"adjMaxMagicArmor":134,"adjHit":6,"adjDodge":6,"adjRealDmg":12,"adjRealDmgDef":12,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000013: _tools.RODict({
        "propID": 51000013,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":80,"adjMinPhysicalAtk":134,"adjMaxPhysicalAtk":134,"adjMinMagicAtk":134,"adjMaxMagicAtk":134,"adjMinPhysicalArmor":135,"adjMaxPhysicalArmor":135,"adjMinMagicArmor":135,"adjMaxMagicArmor":135,"adjHit":7,"adjDodge":7,"adjRealDmg":13,"adjRealDmgDef":13,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000014: _tools.RODict({
        "propID": 51000014,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":90,"adjMinPhysicalAtk":141,"adjMaxPhysicalAtk":141,"adjMinMagicAtk":141,"adjMaxMagicAtk":141,"adjMinPhysicalArmor":136,"adjMaxPhysicalArmor":136,"adjMinMagicArmor":136,"adjMaxMagicArmor":136,"adjHit":7,"adjDodge":7,"adjRealDmg":14,"adjRealDmgDef":14,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000015: _tools.RODict({
        "propID": 51000015,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":110,"adjMinPhysicalAtk":152,"adjMaxPhysicalAtk":152,"adjMinMagicAtk":152,"adjMaxMagicAtk":152,"adjMinPhysicalArmor":138,"adjMaxPhysicalArmor":138,"adjMinMagicArmor":138,"adjMaxMagicArmor":138,"adjHit":8,"adjDodge":8,"adjRealDmg":15,"adjRealDmgDef":15,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000016: _tools.RODict({
        "propID": 51000016,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":120,"adjMinPhysicalAtk":163,"adjMaxPhysicalAtk":163,"adjMinMagicAtk":163,"adjMaxMagicAtk":163,"adjMinPhysicalArmor":158,"adjMaxPhysicalArmor":158,"adjMinMagicArmor":158,"adjMaxMagicArmor":158,"adjHit":8,"adjDodge":9,"adjRealDmg":16,"adjRealDmgDef":16,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000017: _tools.RODict({
        "propID": 51000017,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":129,"adjMinPhysicalAtk":174,"adjMaxPhysicalAtk":174,"adjMinMagicAtk":174,"adjMaxMagicAtk":174,"adjMinPhysicalArmor":159,"adjMaxPhysicalArmor":159,"adjMinMagicArmor":159,"adjMaxMagicArmor":159,"adjHit":9,"adjDodge":10,"adjRealDmg":17,"adjRealDmgDef":17,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000018: _tools.RODict({
        "propID": 51000018,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":131,"adjMinPhysicalAtk":196,"adjMaxPhysicalAtk":196,"adjMinMagicAtk":196,"adjMaxMagicAtk":196,"adjMinPhysicalArmor":161,"adjMaxPhysicalArmor":161,"adjMinMagicArmor":161,"adjMaxMagicArmor":161,"adjHit":9,"adjDodge":10,"adjRealDmg":18,"adjRealDmgDef":18,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000019: _tools.RODict({
        "propID": 51000019,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":135,"adjMinPhysicalAtk":210,"adjMaxPhysicalAtk":210,"adjMinMagicAtk":210,"adjMaxMagicAtk":210,"adjMinPhysicalArmor":169,"adjMaxPhysicalArmor":169,"adjMinMagicArmor":169,"adjMaxMagicArmor":169,"adjHit":10,"adjDodge":11,"adjRealDmg":19,"adjRealDmgDef":19,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000020: _tools.RODict({
        "propID": 51000020,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":165,"adjMinPhysicalAtk":254,"adjMaxPhysicalAtk":254,"adjMinMagicAtk":254,"adjMaxMagicAtk":254,"adjMinPhysicalArmor":178,"adjMaxPhysicalArmor":178,"adjMinMagicArmor":178,"adjMaxMagicArmor":178,"adjHit":10,"adjDodge":11,"adjRealDmg":20,"adjRealDmgDef":20,"adjFinalDmg":0.005,"adjFinalDmgAnti":0.005,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000021: _tools.RODict({
        "propID": 51000021,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":172,"adjMinPhysicalAtk":259,"adjMaxPhysicalAtk":259,"adjMinMagicAtk":259,"adjMaxMagicAtk":259,"adjMinPhysicalArmor":180,"adjMaxPhysicalArmor":180,"adjMinMagicArmor":180,"adjMaxMagicArmor":180,"adjHit":11,"adjDodge":12,"adjRealDmg":21,"adjRealDmgDef":21,"adjFinalDmg":0.005,"adjFinalDmgAnti":0.005,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000022: _tools.RODict({
        "propID": 51000022,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":174,"adjMinPhysicalAtk":264,"adjMaxPhysicalAtk":264,"adjMinMagicAtk":264,"adjMaxMagicAtk":264,"adjMinPhysicalArmor":184,"adjMaxPhysicalArmor":184,"adjMinMagicArmor":184,"adjMaxMagicArmor":184,"adjHit":11,"adjDodge":12,"adjRealDmg":22,"adjRealDmgDef":22,"adjFinalDmg":0.006,"adjFinalDmgAnti":0.006,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000023: _tools.RODict({
        "propID": 51000023,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":179,"adjMinPhysicalAtk":267,"adjMaxPhysicalAtk":267,"adjMinMagicAtk":267,"adjMaxMagicAtk":267,"adjMinPhysicalArmor":185,"adjMaxPhysicalArmor":185,"adjMinMagicArmor":185,"adjMaxMagicArmor":185,"adjHit":12,"adjDodge":13,"adjRealDmg":23,"adjRealDmgDef":23,"adjFinalDmg":0.006,"adjFinalDmgAnti":0.006,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000024: _tools.RODict({
        "propID": 51000024,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":187,"adjMinPhysicalAtk":274,"adjMaxPhysicalAtk":274,"adjMinMagicAtk":274,"adjMaxMagicAtk":274,"adjMinPhysicalArmor":190,"adjMaxPhysicalArmor":190,"adjMinMagicArmor":190,"adjMaxMagicArmor":190,"adjHit":12,"adjDodge":13,"adjRealDmg":24,"adjRealDmgDef":24,"adjFinalDmg":0.007,"adjFinalDmgAnti":0.007,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000025: _tools.RODict({
        "propID": 51000025,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":274,"adjMinPhysicalAtk":332,"adjMaxPhysicalAtk":332,"adjMinMagicAtk":332,"adjMaxMagicAtk":332,"adjMinPhysicalArmor":193,"adjMaxPhysicalArmor":193,"adjMinMagicArmor":193,"adjMaxMagicArmor":193,"adjHit":13,"adjDodge":15,"adjRealDmg":25,"adjRealDmgDef":25,"adjFinalDmg":0.007,"adjFinalDmgAnti":0.007,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000026: _tools.RODict({
        "propID": 51000026,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":293,"adjMinPhysicalAtk":336,"adjMaxPhysicalAtk":336,"adjMinMagicAtk":336,"adjMaxMagicAtk":336,"adjMinPhysicalArmor":198,"adjMaxPhysicalArmor":198,"adjMinMagicArmor":198,"adjMaxMagicArmor":198,"adjHit":13,"adjDodge":15,"adjFatal":3,"adjIgnoreArmor":0.021,"adjRealDmg":26,"adjRealDmgDef":26,"adjFinalDmg":0.029,"adjFinalDmgAnti":0.008,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000027: _tools.RODict({
        "propID": 51000027,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":301,"adjMinPhysicalAtk":341,"adjMaxPhysicalAtk":341,"adjMinMagicAtk":341,"adjMaxMagicAtk":341,"adjMinPhysicalArmor":200,"adjMaxPhysicalArmor":200,"adjMinMagicArmor":200,"adjMaxMagicArmor":200,"adjHit":14,"adjDodge":16,"adjFatal":3,"adjIgnoreArmor":0.021,"adjRealDmg":27,"adjRealDmgDef":27,"adjFinalDmg":0.029,"adjFinalDmgAnti":0.008,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000028: _tools.RODict({
        "propID": 51000028,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":310,"adjMinPhysicalAtk":348,"adjMaxPhysicalAtk":348,"adjMinMagicAtk":348,"adjMaxMagicAtk":348,"adjMinPhysicalArmor":202,"adjMaxPhysicalArmor":202,"adjMinMagicArmor":202,"adjMaxMagicArmor":202,"adjHit":14,"adjDodge":16,"adjFatal":3,"adjIgnoreArmor":0.021,"adjRealDmg":28,"adjRealDmgDef":28,"adjFinalDmg":0.03,"adjFinalDmgAnti":0.009,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000029: _tools.RODict({
        "propID": 51000029,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":315,"adjMinPhysicalAtk":350,"adjMaxPhysicalAtk":350,"adjMinMagicAtk":350,"adjMaxMagicAtk":350,"adjMinPhysicalArmor":203,"adjMaxPhysicalArmor":203,"adjMinMagicArmor":203,"adjMaxMagicArmor":203,"adjHit":15,"adjDodge":17,"adjFatal":3,"adjIgnoreArmor":0.021,"adjRealDmg":29,"adjRealDmgDef":29,"adjFinalDmg":0.03,"adjFinalDmgAnti":0.009,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000030: _tools.RODict({
        "propID": 51000030,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":433,"adjMinPhysicalAtk":438,"adjMaxPhysicalAtk":438,"adjMinMagicAtk":438,"adjMaxMagicAtk":438,"adjMinPhysicalArmor":233,"adjMaxPhysicalArmor":233,"adjMinMagicArmor":233,"adjMaxMagicArmor":233,"adjHit":29,"adjDodge":18,"adjFatal":3,"adjIgnoreArmor":0.041,"adjRealDmg":30,"adjRealDmgDef":30,"adjFinalDmg":0.051,"adjFinalDmgAnti":0.01,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000031: _tools.RODict({
        "propID": 51000031,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":444,"adjMinPhysicalAtk":446,"adjMaxPhysicalAtk":446,"adjMinMagicAtk":446,"adjMaxMagicAtk":446,"adjMinPhysicalArmor":242,"adjMaxPhysicalArmor":242,"adjMinMagicArmor":242,"adjMaxMagicArmor":242,"adjHit":29,"adjDodge":19,"adjFatal":4,"adjAntiFatal":1,"adjIgnoreArmor":0.0471,"adjMortal":0.01,"adjRealDmg":31,"adjRealDmgDef":31,"adjFinalDmg":0.0566,"adjFinalDmgAnti":0.0105,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000032: _tools.RODict({
        "propID": 51000032,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":458,"adjMinPhysicalAtk":455,"adjMaxPhysicalAtk":455,"adjMinMagicAtk":455,"adjMaxMagicAtk":455,"adjMinPhysicalArmor":250,"adjMaxPhysicalArmor":250,"adjMinMagicArmor":250,"adjMaxMagicArmor":250,"adjHit":30,"adjDodge":20,"adjFatal":6,"adjAntiFatal":3,"adjIgnoreArmor":0.0532,"adjMortal":0.02,"adjRealDmg":32,"adjRealDmgDef":32,"adjFinalDmg":0.0622,"adjFinalDmgAnti":0.011,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000033: _tools.RODict({
        "propID": 51000033,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":472,"adjMinPhysicalAtk":464,"adjMaxPhysicalAtk":464,"adjMinMagicAtk":464,"adjMaxMagicAtk":464,"adjMinPhysicalArmor":259,"adjMaxPhysicalArmor":259,"adjMinMagicArmor":259,"adjMaxMagicArmor":259,"adjHit":31,"adjDodge":21,"adjFatal":8,"adjAntiFatal":4,"adjIgnoreArmor":0.0593,"adjMortal":0.03,"adjRealDmg":33,"adjRealDmgDef":33,"adjFinalDmg":0.0678,"adjFinalDmgAnti":0.0115,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000034: _tools.RODict({
        "propID": 51000034,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":487,"adjMinPhysicalAtk":472,"adjMaxPhysicalAtk":472,"adjMinMagicAtk":472,"adjMaxMagicAtk":472,"adjMinPhysicalArmor":267,"adjMaxPhysicalArmor":267,"adjMinMagicArmor":267,"adjMaxMagicArmor":267,"adjHit":31,"adjDodge":23,"adjFatal":10,"adjAntiFatal":6,"adjIgnoreArmor":0.0654,"adjMortal":0.04,"adjRealDmg":34,"adjRealDmgDef":34,"adjFinalDmg":0.0734,"adjFinalDmgAnti":0.012,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000035: _tools.RODict({
        "propID": 51000035,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":500,"adjMinPhysicalAtk":481,"adjMaxPhysicalAtk":481,"adjMinMagicAtk":481,"adjMaxMagicAtk":481,"adjMinPhysicalArmor":276,"adjMaxPhysicalArmor":276,"adjMinMagicArmor":276,"adjMaxMagicArmor":276,"adjHit":32,"adjDodge":24,"adjFatal":12,"adjAntiFatal":7,"adjIgnoreArmor":0.0715,"adjMortal":0.05,"adjRealDmg":35,"adjRealDmgDef":35,"adjFinalDmg":0.079,"adjFinalDmgAnti":0.0125,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000036: _tools.RODict({
        "propID": 51000036,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":516,"adjMinPhysicalAtk":489,"adjMaxPhysicalAtk":489,"adjMinMagicAtk":489,"adjMaxMagicAtk":489,"adjMinPhysicalArmor":284,"adjMaxPhysicalArmor":284,"adjMinMagicArmor":284,"adjMaxMagicArmor":284,"adjHit":33,"adjDodge":25,"adjFatal":13,"adjAntiFatal":9,"adjIgnoreArmor":0.0776,"adjMortal":0.06,"adjRealDmg":36,"adjRealDmgDef":36,"adjFinalDmg":0.0846,"adjFinalDmgAnti":0.013,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000037: _tools.RODict({
        "propID": 51000037,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":532,"adjMinPhysicalAtk":498,"adjMaxPhysicalAtk":498,"adjMinMagicAtk":498,"adjMaxMagicAtk":498,"adjMinPhysicalArmor":293,"adjMaxPhysicalArmor":293,"adjMinMagicArmor":293,"adjMaxMagicArmor":293,"adjHit":33,"adjDodge":27,"adjFatal":15,"adjAntiFatal":10,"adjIgnoreArmor":0.0837,"adjMortal":0.07,"adjRealDmg":37,"adjRealDmgDef":37,"adjFinalDmg":0.0902,"adjFinalDmgAnti":0.0135,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000038: _tools.RODict({
        "propID": 51000038,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":549,"adjMinPhysicalAtk":507,"adjMaxPhysicalAtk":507,"adjMinMagicAtk":507,"adjMaxMagicAtk":507,"adjMinPhysicalArmor":301,"adjMaxPhysicalArmor":301,"adjMinMagicArmor":301,"adjMaxMagicArmor":301,"adjHit":34,"adjDodge":28,"adjFatal":17,"adjAntiFatal":12,"adjIgnoreArmor":0.0898,"adjMortal":0.08,"adjRealDmg":38,"adjRealDmgDef":38,"adjFinalDmg":0.0958,"adjFinalDmgAnti":0.014,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000039: _tools.RODict({
        "propID": 51000039,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":567,"adjMinPhysicalAtk":515,"adjMaxPhysicalAtk":515,"adjMinMagicAtk":515,"adjMaxMagicAtk":515,"adjMinPhysicalArmor":310,"adjMaxPhysicalArmor":310,"adjMinMagicArmor":310,"adjMaxMagicArmor":310,"adjHit":35,"adjDodge":29,"adjFatal":19,"adjAntiFatal":13,"adjIgnoreArmor":0.0959,"adjMortal":0.09,"adjRealDmg":39,"adjRealDmgDef":39,"adjFinalDmg":0.1014,"adjFinalDmgAnti":0.0145,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000040: _tools.RODict({
        "propID": 51000040,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":583,"adjMinPhysicalAtk":524,"adjMaxPhysicalAtk":524,"adjMinMagicAtk":524,"adjMaxMagicAtk":524,"adjMinPhysicalArmor":318,"adjMaxPhysicalArmor":318,"adjMinMagicArmor":318,"adjMaxMagicArmor":318,"adjHit":35,"adjDodge":31,"adjFatal":21,"adjAntiFatal":15,"adjIgnoreArmor":0.102,"adjMortal":0.1,"adjRealDmg":40,"adjRealDmgDef":40,"adjFinalDmg":0.107,"adjFinalDmgAnti":0.015,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000041: _tools.RODict({
        "propID": 51000041,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":601,"adjMinPhysicalAtk":535,"adjMaxPhysicalAtk":535,"adjMinMagicAtk":535,"adjMaxMagicAtk":535,"adjMinPhysicalArmor":326,"adjMaxPhysicalArmor":326,"adjMinMagicArmor":326,"adjMaxMagicArmor":326,"adjHit":36,"adjDodge":31,"adjFatal":21,"adjAntiFatal":15,"adjIgnoreArmor":0.104,"adjMortal":0.1,"adjRealDmg":41,"adjRealDmgDef":41,"adjFinalDmg":0.1095,"adjFinalDmgAnti":0.0155,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000042: _tools.RODict({
        "propID": 51000042,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":618,"adjMinPhysicalAtk":546,"adjMaxPhysicalAtk":546,"adjMinMagicAtk":546,"adjMaxMagicAtk":546,"adjMinPhysicalArmor":333,"adjMaxPhysicalArmor":333,"adjMinMagicArmor":333,"adjMaxMagicArmor":333,"adjHit":37,"adjDodge":32,"adjFatal":21,"adjAntiFatal":15,"adjIgnoreArmor":0.106,"adjMortal":0.1,"adjRealDmg":42,"adjRealDmgDef":42,"adjFinalDmg":0.112,"adjFinalDmgAnti":0.016,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000043: _tools.RODict({
        "propID": 51000043,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":637,"adjMinPhysicalAtk":558,"adjMaxPhysicalAtk":558,"adjMinMagicAtk":558,"adjMaxMagicAtk":558,"adjMinPhysicalArmor":340,"adjMaxPhysicalArmor":340,"adjMinMagicArmor":340,"adjMaxMagicArmor":340,"adjHit":37,"adjDodge":33,"adjFatal":21,"adjAntiFatal":15,"adjIgnoreArmor":0.108,"adjMortal":0.1,"adjRealDmg":43,"adjRealDmgDef":43,"adjFinalDmg":0.1145,"adjFinalDmgAnti":0.0165,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000044: _tools.RODict({
        "propID": 51000044,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":653,"adjMinPhysicalAtk":569,"adjMaxPhysicalAtk":569,"adjMinMagicAtk":569,"adjMaxMagicAtk":569,"adjMinPhysicalArmor":348,"adjMaxPhysicalArmor":348,"adjMinMagicArmor":348,"adjMaxMagicArmor":348,"adjHit":38,"adjDodge":34,"adjFatal":21,"adjAntiFatal":15,"adjIgnoreArmor":0.11,"adjMortal":0.1,"adjRealDmg":44,"adjRealDmgDef":44,"adjFinalDmg":0.117,"adjFinalDmgAnti":0.017,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000045: _tools.RODict({
        "propID": 51000045,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":672,"adjMinPhysicalAtk":580,"adjMaxPhysicalAtk":580,"adjMinMagicAtk":580,"adjMaxMagicAtk":580,"adjMinPhysicalArmor":355,"adjMaxPhysicalArmor":355,"adjMinMagicArmor":355,"adjMaxMagicArmor":355,"adjHit":39,"adjDodge":35,"adjFatal":21,"adjAntiFatal":15,"adjIgnoreArmor":0.112,"adjMortal":0.1,"adjRealDmg":45,"adjRealDmgDef":45,"adjFinalDmg":0.1195,"adjFinalDmgAnti":0.0175,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000046: _tools.RODict({
        "propID": 51000046,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":691,"adjMinPhysicalAtk":591,"adjMaxPhysicalAtk":591,"adjMinMagicAtk":591,"adjMaxMagicAtk":591,"adjMinPhysicalArmor":363,"adjMaxPhysicalArmor":363,"adjMinMagicArmor":363,"adjMaxMagicArmor":363,"adjHit":39,"adjDodge":35,"adjFatal":21,"adjAntiFatal":15,"adjIgnoreArmor":0.114,"adjMortal":0.1,"adjRealDmg":46,"adjRealDmgDef":46,"adjFinalDmg":0.122,"adjFinalDmgAnti":0.018,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000047: _tools.RODict({
        "propID": 51000047,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":710,"adjMinPhysicalAtk":603,"adjMaxPhysicalAtk":603,"adjMinMagicAtk":603,"adjMaxMagicAtk":603,"adjMinPhysicalArmor":370,"adjMaxPhysicalArmor":370,"adjMinMagicArmor":370,"adjMaxMagicArmor":370,"adjHit":40,"adjDodge":36,"adjFatal":21,"adjAntiFatal":15,"adjIgnoreArmor":0.116,"adjMortal":0.1,"adjRealDmg":47,"adjRealDmgDef":47,"adjFinalDmg":0.1245,"adjFinalDmgAnti":0.0185,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000048: _tools.RODict({
        "propID": 51000048,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":727,"adjMinPhysicalAtk":614,"adjMaxPhysicalAtk":614,"adjMinMagicAtk":614,"adjMaxMagicAtk":614,"adjMinPhysicalArmor":377,"adjMaxPhysicalArmor":377,"adjMinMagicArmor":377,"adjMaxMagicArmor":377,"adjHit":41,"adjDodge":37,"adjFatal":21,"adjAntiFatal":15,"adjIgnoreArmor":0.118,"adjMortal":0.1,"adjRealDmg":48,"adjRealDmgDef":48,"adjFinalDmg":0.127,"adjFinalDmgAnti":0.019,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000049: _tools.RODict({
        "propID": 51000049,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":747,"adjMinPhysicalAtk":625,"adjMaxPhysicalAtk":625,"adjMinMagicAtk":625,"adjMaxMagicAtk":625,"adjMinPhysicalArmor":385,"adjMaxPhysicalArmor":385,"adjMinMagicArmor":385,"adjMaxMagicArmor":385,"adjHit":41,"adjDodge":38,"adjFatal":21,"adjAntiFatal":15,"adjIgnoreArmor":0.12,"adjMortal":0.1,"adjRealDmg":49,"adjRealDmgDef":49,"adjFinalDmg":0.1295,"adjFinalDmgAnti":0.0195,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000050: _tools.RODict({
        "propID": 51000050,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":767,"adjMinPhysicalAtk":637,"adjMaxPhysicalAtk":637,"adjMinMagicAtk":637,"adjMaxMagicAtk":637,"adjMinPhysicalArmor":392,"adjMaxPhysicalArmor":392,"adjMinMagicArmor":392,"adjMaxMagicArmor":392,"adjHit":42,"adjDodge":39,"adjFatal":22,"adjAntiFatal":16,"adjIgnoreArmor":0.122,"adjMortal":0.1,"adjRealDmg":50,"adjRealDmgDef":50,"adjFinalDmg":0.132,"adjFinalDmgAnti":0.02,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000051: _tools.RODict({
        "propID": 51000051,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":798,"adjMinPhysicalAtk":651,"adjMaxPhysicalAtk":651,"adjMinMagicAtk":651,"adjMaxMagicAtk":651,"adjMinPhysicalArmor":401,"adjMaxPhysicalArmor":401,"adjMinMagicArmor":401,"adjMaxMagicArmor":401,"adjHit":43,"adjDodge":39,"adjFatal":22,"adjAntiFatal":16,"adjIgnoreArmor":0.1281,"adjMortal":0.105,"adjRealDmg":51,"adjRealDmgDef":51,"adjFinalDmg":0.1346,"adjFinalDmgAnti":0.0205,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000052: _tools.RODict({
        "propID": 51000052,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":829,"adjMinPhysicalAtk":666,"adjMaxPhysicalAtk":666,"adjMinMagicAtk":666,"adjMaxMagicAtk":666,"adjMinPhysicalArmor":411,"adjMaxPhysicalArmor":411,"adjMinMagicArmor":411,"adjMaxMagicArmor":411,"adjHit":44,"adjDodge":40,"adjFatal":23,"adjAntiFatal":16,"adjIgnoreArmor":0.1342,"adjMortal":0.11,"adjRealDmg":52,"adjRealDmgDef":52,"adjFinalDmg":0.1372,"adjFinalDmgAnti":0.021,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000053: _tools.RODict({
        "propID": 51000053,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":859,"adjMinPhysicalAtk":681,"adjMaxPhysicalAtk":681,"adjMinMagicAtk":681,"adjMaxMagicAtk":681,"adjMinPhysicalArmor":420,"adjMaxPhysicalArmor":420,"adjMinMagicArmor":420,"adjMaxMagicArmor":420,"adjHit":44,"adjDodge":41,"adjFatal":23,"adjAntiFatal":16,"adjIgnoreArmor":0.1403,"adjMortal":0.115,"adjRealDmg":53,"adjRealDmgDef":53,"adjFinalDmg":0.1398,"adjFinalDmgAnti":0.0215,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000054: _tools.RODict({
        "propID": 51000054,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":892,"adjMinPhysicalAtk":696,"adjMaxPhysicalAtk":696,"adjMinMagicAtk":696,"adjMaxMagicAtk":696,"adjMinPhysicalArmor":429,"adjMaxPhysicalArmor":429,"adjMinMagicArmor":429,"adjMaxMagicArmor":429,"adjHit":45,"adjDodge":42,"adjFatal":24,"adjAntiFatal":16,"adjIgnoreArmor":0.1464,"adjMortal":0.12,"adjRealDmg":54,"adjRealDmgDef":54,"adjFinalDmg":0.1424,"adjFinalDmgAnti":0.022,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000055: _tools.RODict({
        "propID": 51000055,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":925,"adjMinPhysicalAtk":711,"adjMaxPhysicalAtk":711,"adjMinMagicAtk":711,"adjMaxMagicAtk":711,"adjMinPhysicalArmor":438,"adjMaxPhysicalArmor":438,"adjMinMagicArmor":438,"adjMaxMagicArmor":438,"adjHit":46,"adjDodge":43,"adjFatal":24,"adjAntiFatal":17,"adjIgnoreArmor":0.1525,"adjMortal":0.125,"adjRealDmg":55,"adjRealDmgDef":55,"adjFinalDmg":0.145,"adjFinalDmgAnti":0.0225,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000056: _tools.RODict({
        "propID": 51000056,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":960,"adjMinPhysicalAtk":726,"adjMaxPhysicalAtk":726,"adjMinMagicAtk":726,"adjMaxMagicAtk":726,"adjMinPhysicalArmor":448,"adjMaxPhysicalArmor":448,"adjMinMagicArmor":448,"adjMaxMagicArmor":448,"adjHit":47,"adjDodge":43,"adjFatal":25,"adjAntiFatal":17,"adjIgnoreArmor":0.1586,"adjMortal":0.13,"adjRealDmg":56,"adjRealDmgDef":56,"adjFinalDmg":0.1476,"adjFinalDmgAnti":0.023,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000057: _tools.RODict({
        "propID": 51000057,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":993,"adjMinPhysicalAtk":741,"adjMaxPhysicalAtk":741,"adjMinMagicAtk":741,"adjMaxMagicAtk":741,"adjMinPhysicalArmor":457,"adjMaxPhysicalArmor":457,"adjMinMagicArmor":457,"adjMaxMagicArmor":457,"adjHit":48,"adjDodge":44,"adjFatal":25,"adjAntiFatal":17,"adjIgnoreArmor":0.1647,"adjMortal":0.135,"adjRealDmg":57,"adjRealDmgDef":57,"adjFinalDmg":0.1502,"adjFinalDmgAnti":0.0235,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000058: _tools.RODict({
        "propID": 51000058,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1029,"adjMinPhysicalAtk":756,"adjMaxPhysicalAtk":756,"adjMinMagicAtk":756,"adjMaxMagicAtk":756,"adjMinPhysicalArmor":466,"adjMaxPhysicalArmor":466,"adjMinMagicArmor":466,"adjMaxMagicArmor":466,"adjHit":49,"adjDodge":45,"adjFatal":26,"adjAntiFatal":17,"adjIgnoreArmor":0.1708,"adjMortal":0.14,"adjRealDmg":58,"adjRealDmgDef":58,"adjFinalDmg":0.1528,"adjFinalDmgAnti":0.024,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000059: _tools.RODict({
        "propID": 51000059,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1066,"adjMinPhysicalAtk":771,"adjMaxPhysicalAtk":771,"adjMinMagicAtk":771,"adjMaxMagicAtk":771,"adjMinPhysicalArmor":475,"adjMaxPhysicalArmor":475,"adjMinMagicArmor":475,"adjMaxMagicArmor":475,"adjHit":50,"adjDodge":46,"adjFatal":26,"adjAntiFatal":17,"adjIgnoreArmor":0.1769,"adjMortal":0.145,"adjRealDmg":59,"adjRealDmgDef":59,"adjFinalDmg":0.1554,"adjFinalDmgAnti":0.0245,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000060: _tools.RODict({
        "propID": 51000060,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1104,"adjMinPhysicalAtk":786,"adjMaxPhysicalAtk":786,"adjMinMagicAtk":786,"adjMaxMagicAtk":786,"adjMinPhysicalArmor":485,"adjMaxPhysicalArmor":485,"adjMinMagicArmor":485,"adjMaxMagicArmor":485,"adjHit":51,"adjDodge":47,"adjFatal":27,"adjAntiFatal":18,"adjIgnoreArmor":0.183,"adjMortal":0.15,"adjRealDmg":60,"adjRealDmgDef":60,"adjFinalDmg":0.158,"adjFinalDmgAnti":0.025,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000061: _tools.RODict({
        "propID": 51000061,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1123,"adjMinPhysicalAtk":797,"adjMaxPhysicalAtk":797,"adjMinMagicAtk":797,"adjMaxMagicAtk":797,"adjMinPhysicalArmor":493,"adjMaxPhysicalArmor":493,"adjMinMagicArmor":493,"adjMaxMagicArmor":493,"adjHit":51,"adjDodge":47,"adjFatal":27,"adjAntiFatal":18,"adjIgnoreArmor":0.183,"adjMortal":0.15,"adjRealDmg":61,"adjRealDmgDef":61,"adjFinalDmg":0.1585,"adjFinalDmgAnti":0.0255,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000062: _tools.RODict({
        "propID": 51000062,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1144,"adjMinPhysicalAtk":809,"adjMaxPhysicalAtk":809,"adjMinMagicAtk":809,"adjMaxMagicAtk":809,"adjMinPhysicalArmor":501,"adjMaxPhysicalArmor":501,"adjMinMagicArmor":501,"adjMaxMagicArmor":501,"adjHit":52,"adjDodge":48,"adjFatal":27,"adjAntiFatal":18,"adjIgnoreArmor":0.183,"adjMortal":0.15,"adjRealDmg":62,"adjRealDmgDef":62,"adjFinalDmg":0.159,"adjFinalDmgAnti":0.026,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000063: _tools.RODict({
        "propID": 51000063,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1166,"adjMinPhysicalAtk":820,"adjMaxPhysicalAtk":820,"adjMinMagicAtk":820,"adjMaxMagicAtk":820,"adjMinPhysicalArmor":509,"adjMaxPhysicalArmor":509,"adjMinMagicArmor":509,"adjMaxMagicArmor":509,"adjHit":52,"adjDodge":49,"adjFatal":27,"adjAntiFatal":18,"adjIgnoreArmor":0.183,"adjMortal":0.15,"adjRealDmg":63,"adjRealDmgDef":63,"adjFinalDmg":0.1595,"adjFinalDmgAnti":0.0265,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000064: _tools.RODict({
        "propID": 51000064,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1188,"adjMinPhysicalAtk":832,"adjMaxPhysicalAtk":832,"adjMinMagicAtk":832,"adjMaxMagicAtk":832,"adjMinPhysicalArmor":517,"adjMaxPhysicalArmor":517,"adjMinMagicArmor":517,"adjMaxMagicArmor":517,"adjHit":53,"adjDodge":50,"adjFatal":27,"adjAntiFatal":18,"adjIgnoreArmor":0.183,"adjMortal":0.15,"adjRealDmg":64,"adjRealDmgDef":64,"adjFinalDmg":0.16,"adjFinalDmgAnti":0.027,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000065: _tools.RODict({
        "propID": 51000065,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1210,"adjMinPhysicalAtk":843,"adjMaxPhysicalAtk":843,"adjMinMagicAtk":843,"adjMaxMagicAtk":843,"adjMinPhysicalArmor":525,"adjMaxPhysicalArmor":525,"adjMinMagicArmor":525,"adjMaxMagicArmor":525,"adjHit":53,"adjDodge":51,"adjFatal":27,"adjAntiFatal":18,"adjIgnoreArmor":0.183,"adjMortal":0.15,"adjRealDmg":65,"adjRealDmgDef":65,"adjFinalDmg":0.1605,"adjFinalDmgAnti":0.0275,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000066: _tools.RODict({
        "propID": 51000066,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1230,"adjMinPhysicalAtk":854,"adjMaxPhysicalAtk":854,"adjMinMagicAtk":854,"adjMaxMagicAtk":854,"adjMinPhysicalArmor":533,"adjMaxPhysicalArmor":533,"adjMinMagicArmor":533,"adjMaxMagicArmor":533,"adjHit":54,"adjDodge":51,"adjFatal":27,"adjAntiFatal":18,"adjIgnoreArmor":0.183,"adjMortal":0.15,"adjRealDmg":66,"adjRealDmgDef":66,"adjFinalDmg":0.161,"adjFinalDmgAnti":0.028,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000067: _tools.RODict({
        "propID": 51000067,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1252,"adjMinPhysicalAtk":866,"adjMaxPhysicalAtk":866,"adjMinMagicAtk":866,"adjMaxMagicAtk":866,"adjMinPhysicalArmor":541,"adjMaxPhysicalArmor":541,"adjMinMagicArmor":541,"adjMaxMagicArmor":541,"adjHit":54,"adjDodge":52,"adjFatal":27,"adjAntiFatal":18,"adjIgnoreArmor":0.183,"adjMortal":0.15,"adjRealDmg":67,"adjRealDmgDef":67,"adjFinalDmg":0.1615,"adjFinalDmgAnti":0.0285,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000068: _tools.RODict({
        "propID": 51000068,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1275,"adjMinPhysicalAtk":877,"adjMaxPhysicalAtk":877,"adjMinMagicAtk":877,"adjMaxMagicAtk":877,"adjMinPhysicalArmor":549,"adjMaxPhysicalArmor":549,"adjMinMagicArmor":549,"adjMaxMagicArmor":549,"adjHit":55,"adjDodge":53,"adjFatal":27,"adjAntiFatal":18,"adjIgnoreArmor":0.183,"adjMortal":0.15,"adjRealDmg":68,"adjRealDmgDef":68,"adjFinalDmg":0.162,"adjFinalDmgAnti":0.029,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000069: _tools.RODict({
        "propID": 51000069,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1298,"adjMinPhysicalAtk":889,"adjMaxPhysicalAtk":889,"adjMinMagicAtk":889,"adjMaxMagicAtk":889,"adjMinPhysicalArmor":557,"adjMaxPhysicalArmor":557,"adjMinMagicArmor":557,"adjMaxMagicArmor":557,"adjHit":56,"adjDodge":54,"adjFatal":27,"adjAntiFatal":18,"adjIgnoreArmor":0.183,"adjMortal":0.15,"adjRealDmg":69,"adjRealDmgDef":69,"adjFinalDmg":0.1625,"adjFinalDmgAnti":0.0295,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000070: _tools.RODict({
        "propID": 51000070,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1318,"adjMinPhysicalAtk":900,"adjMaxPhysicalAtk":900,"adjMinMagicAtk":900,"adjMaxMagicAtk":900,"adjMinPhysicalArmor":565,"adjMaxPhysicalArmor":565,"adjMinMagicArmor":565,"adjMaxMagicArmor":565,"adjHit":56,"adjDodge":55,"adjFatal":28,"adjAntiFatal":19,"adjIgnoreArmor":0.183,"adjMortal":0.15,"adjRealDmg":70,"adjRealDmgDef":70,"adjFinalDmg":0.163,"adjFinalDmgAnti":0.03,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000071: _tools.RODict({
        "propID": 51000071,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1350,"adjMinPhysicalAtk":913,"adjMaxPhysicalAtk":913,"adjMinMagicAtk":913,"adjMaxMagicAtk":913,"adjMinPhysicalArmor":574,"adjMaxPhysicalArmor":574,"adjMinMagicArmor":574,"adjMaxMagicArmor":574,"adjHit":57,"adjDodge":55,"adjFatal":28,"adjAntiFatal":19,"adjIgnoreArmor":0.183,"adjMortal":0.15,"adjRealDmg":71,"adjRealDmgDef":71,"adjFinalDmg":0.1655,"adjFinalDmgAnti":0.0305,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000072: _tools.RODict({
        "propID": 51000072,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1383,"adjMinPhysicalAtk":926,"adjMaxPhysicalAtk":926,"adjMinMagicAtk":926,"adjMaxMagicAtk":926,"adjMinPhysicalArmor":583,"adjMaxPhysicalArmor":583,"adjMinMagicArmor":583,"adjMaxMagicArmor":583,"adjHit":57,"adjDodge":56,"adjFatal":28,"adjAntiFatal":19,"adjIgnoreArmor":0.183,"adjMortal":0.15,"adjRealDmg":72,"adjRealDmgDef":72,"adjFinalDmg":0.168,"adjFinalDmgAnti":0.031,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000073: _tools.RODict({
        "propID": 51000073,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1416,"adjMinPhysicalAtk":939,"adjMaxPhysicalAtk":939,"adjMinMagicAtk":939,"adjMaxMagicAtk":939,"adjMinPhysicalArmor":592,"adjMaxPhysicalArmor":592,"adjMinMagicArmor":592,"adjMaxMagicArmor":592,"adjHit":58,"adjDodge":57,"adjFatal":28,"adjAntiFatal":19,"adjIgnoreArmor":0.183,"adjMortal":0.15,"adjRealDmg":73,"adjRealDmgDef":73,"adjFinalDmg":0.1705,"adjFinalDmgAnti":0.0315,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000074: _tools.RODict({
        "propID": 51000074,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1450,"adjMinPhysicalAtk":952,"adjMaxPhysicalAtk":952,"adjMinMagicAtk":952,"adjMaxMagicAtk":952,"adjMinPhysicalArmor":602,"adjMaxPhysicalArmor":602,"adjMinMagicArmor":602,"adjMaxMagicArmor":602,"adjHit":58,"adjDodge":58,"adjFatal":28,"adjAntiFatal":19,"adjIgnoreArmor":0.183,"adjMortal":0.15,"adjRealDmg":74,"adjRealDmgDef":74,"adjFinalDmg":0.173,"adjFinalDmgAnti":0.032,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000075: _tools.RODict({
        "propID": 51000075,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1484,"adjMinPhysicalAtk":965,"adjMaxPhysicalAtk":965,"adjMinMagicAtk":965,"adjMaxMagicAtk":965,"adjMinPhysicalArmor":611,"adjMaxPhysicalArmor":611,"adjMinMagicArmor":611,"adjMaxMagicArmor":611,"adjHit":59,"adjDodge":59,"adjFatal":28,"adjAntiFatal":19,"adjIgnoreArmor":0.183,"adjMortal":0.15,"adjRealDmg":75,"adjRealDmgDef":75,"adjFinalDmg":0.1755,"adjFinalDmgAnti":0.0325,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000076: _tools.RODict({
        "propID": 51000076,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1519,"adjMinPhysicalAtk":978,"adjMaxPhysicalAtk":978,"adjMinMagicAtk":978,"adjMaxMagicAtk":978,"adjMinPhysicalArmor":620,"adjMaxPhysicalArmor":620,"adjMinMagicArmor":620,"adjMaxMagicArmor":620,"adjHit":60,"adjDodge":59,"adjFatal":28,"adjAntiFatal":19,"adjIgnoreArmor":0.183,"adjMortal":0.15,"adjRealDmg":76,"adjRealDmgDef":76,"adjFinalDmg":0.178,"adjFinalDmgAnti":0.033,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000077: _tools.RODict({
        "propID": 51000077,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1554,"adjMinPhysicalAtk":991,"adjMaxPhysicalAtk":991,"adjMinMagicAtk":991,"adjMaxMagicAtk":991,"adjMinPhysicalArmor":629,"adjMaxPhysicalArmor":629,"adjMinMagicArmor":629,"adjMaxMagicArmor":629,"adjHit":60,"adjDodge":60,"adjFatal":28,"adjAntiFatal":19,"adjIgnoreArmor":0.183,"adjMortal":0.15,"adjRealDmg":77,"adjRealDmgDef":77,"adjFinalDmg":0.1805,"adjFinalDmgAnti":0.0335,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000078: _tools.RODict({
        "propID": 51000078,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1590,"adjMinPhysicalAtk":1005,"adjMaxPhysicalAtk":1005,"adjMinMagicAtk":1005,"adjMaxMagicAtk":1005,"adjMinPhysicalArmor":638,"adjMaxPhysicalArmor":638,"adjMinMagicArmor":638,"adjMaxMagicArmor":638,"adjHit":61,"adjDodge":61,"adjFatal":28,"adjAntiFatal":19,"adjIgnoreArmor":0.183,"adjMortal":0.15,"adjRealDmg":78,"adjRealDmgDef":78,"adjFinalDmg":0.183,"adjFinalDmgAnti":0.034,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000079: _tools.RODict({
        "propID": 51000079,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1627,"adjMinPhysicalAtk":1018,"adjMaxPhysicalAtk":1018,"adjMinMagicAtk":1018,"adjMaxMagicAtk":1018,"adjMinPhysicalArmor":647,"adjMaxPhysicalArmor":647,"adjMinMagicArmor":647,"adjMaxMagicArmor":647,"adjHit":61,"adjDodge":62,"adjFatal":28,"adjAntiFatal":19,"adjIgnoreArmor":0.183,"adjMortal":0.15,"adjRealDmg":79,"adjRealDmgDef":79,"adjFinalDmg":0.1855,"adjFinalDmgAnti":0.0345,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000080: _tools.RODict({
        "propID": 51000080,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1664,"adjMinPhysicalAtk":1031,"adjMaxPhysicalAtk":1031,"adjMinMagicAtk":1031,"adjMaxMagicAtk":1031,"adjMinPhysicalArmor":657,"adjMaxPhysicalArmor":657,"adjMinMagicArmor":657,"adjMaxMagicArmor":657,"adjHit":62,"adjDodge":63,"adjFatal":28,"adjAntiFatal":19,"adjIgnoreArmor":0.183,"adjMortal":0.15,"adjRealDmg":80,"adjRealDmgDef":80,"adjFinalDmg":0.188,"adjFinalDmgAnti":0.035,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000081: _tools.RODict({
        "propID": 51000081,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1732,"adjMinPhysicalAtk":1054,"adjMaxPhysicalAtk":1054,"adjMinMagicAtk":1054,"adjMaxMagicAtk":1054,"adjMinPhysicalArmor":673,"adjMaxPhysicalArmor":673,"adjMinMagicArmor":673,"adjMaxMagicArmor":673,"adjHit":63,"adjDodge":64,"adjFatal":28,"adjAntiFatal":19,"adjIgnoreArmor":0.187,"adjMortal":0.155,"adjRealDmg":81,"adjRealDmgDef":81,"adjFinalDmg":0.1965,"adjFinalDmgAnti":0.0355,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000082: _tools.RODict({
        "propID": 51000082,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1803,"adjMinPhysicalAtk":1077,"adjMaxPhysicalAtk":1077,"adjMinMagicAtk":1077,"adjMaxMagicAtk":1077,"adjMinPhysicalArmor":690,"adjMaxPhysicalArmor":690,"adjMinMagicArmor":690,"adjMaxMagicArmor":690,"adjHit":63,"adjDodge":66,"adjFatal":28,"adjAntiFatal":19,"adjIgnoreArmor":0.191,"adjMortal":0.16,"adjRealDmg":82,"adjRealDmgDef":82,"adjFinalDmg":0.205,"adjFinalDmgAnti":0.036,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000083: _tools.RODict({
        "propID": 51000083,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1876,"adjMinPhysicalAtk":1101,"adjMaxPhysicalAtk":1101,"adjMinMagicAtk":1101,"adjMaxMagicAtk":1101,"adjMinPhysicalArmor":706,"adjMaxPhysicalArmor":706,"adjMinMagicArmor":706,"adjMaxMagicArmor":706,"adjHit":64,"adjDodge":68,"adjFatal":28,"adjAntiFatal":19,"adjIgnoreArmor":0.195,"adjMortal":0.165,"adjRealDmg":83,"adjRealDmgDef":83,"adjFinalDmg":0.2135,"adjFinalDmgAnti":0.0365,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000084: _tools.RODict({
        "propID": 51000084,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1951,"adjMinPhysicalAtk":1124,"adjMaxPhysicalAtk":1124,"adjMinMagicAtk":1124,"adjMaxMagicAtk":1124,"adjMinPhysicalArmor":723,"adjMaxPhysicalArmor":723,"adjMinMagicArmor":723,"adjMaxMagicArmor":723,"adjHit":65,"adjDodge":70,"adjFatal":28,"adjAntiFatal":19,"adjIgnoreArmor":0.199,"adjMortal":0.17,"adjRealDmg":84,"adjRealDmgDef":84,"adjFinalDmg":0.222,"adjFinalDmgAnti":0.037,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000085: _tools.RODict({
        "propID": 51000085,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2028,"adjMinPhysicalAtk":1148,"adjMaxPhysicalAtk":1148,"adjMinMagicAtk":1148,"adjMaxMagicAtk":1148,"adjMinPhysicalArmor":739,"adjMaxPhysicalArmor":739,"adjMinMagicArmor":739,"adjMaxMagicArmor":739,"adjHit":65,"adjDodge":72,"adjFatal":28,"adjAntiFatal":19,"adjIgnoreArmor":0.203,"adjMortal":0.175,"adjRealDmg":85,"adjRealDmgDef":85,"adjFinalDmg":0.2305,"adjFinalDmgAnti":0.0375,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000086: _tools.RODict({
        "propID": 51000086,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2107,"adjMinPhysicalAtk":1171,"adjMaxPhysicalAtk":1171,"adjMinMagicAtk":1171,"adjMaxMagicAtk":1171,"adjMinPhysicalArmor":756,"adjMaxPhysicalArmor":756,"adjMinMagicArmor":756,"adjMaxMagicArmor":756,"adjHit":66,"adjDodge":74,"adjFatal":28,"adjAntiFatal":19,"adjIgnoreArmor":0.207,"adjMortal":0.18,"adjRealDmg":86,"adjRealDmgDef":86,"adjFinalDmg":0.239,"adjFinalDmgAnti":0.038,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000087: _tools.RODict({
        "propID": 51000087,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2188,"adjMinPhysicalAtk":1194,"adjMaxPhysicalAtk":1194,"adjMinMagicAtk":1194,"adjMaxMagicAtk":1194,"adjMinPhysicalArmor":772,"adjMaxPhysicalArmor":772,"adjMinMagicArmor":772,"adjMaxMagicArmor":772,"adjHit":67,"adjDodge":76,"adjFatal":28,"adjAntiFatal":19,"adjIgnoreArmor":0.211,"adjMortal":0.185,"adjRealDmg":87,"adjRealDmgDef":87,"adjFinalDmg":0.2475,"adjFinalDmgAnti":0.0385,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000088: _tools.RODict({
        "propID": 51000088,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2272,"adjMinPhysicalAtk":1218,"adjMaxPhysicalAtk":1218,"adjMinMagicAtk":1218,"adjMaxMagicAtk":1218,"adjMinPhysicalArmor":789,"adjMaxPhysicalArmor":789,"adjMinMagicArmor":789,"adjMaxMagicArmor":789,"adjHit":67,"adjDodge":78,"adjFatal":28,"adjAntiFatal":19,"adjIgnoreArmor":0.215,"adjMortal":0.19,"adjRealDmg":88,"adjRealDmgDef":88,"adjFinalDmg":0.256,"adjFinalDmgAnti":0.039,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000089: _tools.RODict({
        "propID": 51000089,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2358,"adjMinPhysicalAtk":1241,"adjMaxPhysicalAtk":1241,"adjMinMagicAtk":1241,"adjMaxMagicAtk":1241,"adjMinPhysicalArmor":805,"adjMaxPhysicalArmor":805,"adjMinMagicArmor":805,"adjMaxMagicArmor":805,"adjHit":68,"adjDodge":80,"adjFatal":28,"adjAntiFatal":19,"adjIgnoreArmor":0.219,"adjMortal":0.195,"adjRealDmg":89,"adjRealDmgDef":89,"adjFinalDmg":0.2645,"adjFinalDmgAnti":0.0395,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
    }),
    51000090: _tools.RODict({
        "propID": 51000090,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2447,"adjMinPhysicalAtk":1265,"adjMaxPhysicalAtk":1265,"adjMinMagicAtk":1265,"adjMaxMagicAtk":1265,"adjMinPhysicalArmor":822,"adjMaxPhysicalArmor":822,"adjMinMagicArmor":822,"adjMaxMagicArmor":822,"adjHit":69,"adjDodge":82,"adjFatal":29,"adjAntiFatal":20,"adjIgnoreArmor":0.223,"adjMortal":0.2,"adjRealDmg":90,"adjRealDmgDef":90,"adjFinalDmg":0.273,"adjFinalDmgAnti":0.04,"adjStunEnh":15,"adjStunAnti":15,"adjSilentEnh":15,"adjSilentAnti":15,"adjKnockEnh":15,"adjKnockAnti":15,"adjFrozenEnh":15,"adjFrozenAnti":15,"adjSlowEnh":15,"adjSlowAnti":15})
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
        "propList": _tools.RODict({"adjFullHp":1100000,"adjMinPhysicalArmor":320,"adjMaxPhysicalArmor":320,"adjMinMagicArmor":320,"adjMaxMagicArmor":320})
    }),
    52004022: _tools.RODict({
        "propID": 52004022,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1500000,"adjMinPhysicalArmor":390,"adjMaxPhysicalArmor":390,"adjMinMagicArmor":390,"adjMaxMagicArmor":390})
    }),
    52004023: _tools.RODict({
        "propID": 52004023,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2200000,"adjMinPhysicalArmor":500,"adjMaxPhysicalArmor":500,"adjMinMagicArmor":500,"adjMaxMagicArmor":500})
    }),
    52004024: _tools.RODict({
        "propID": 52004024,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3400000,"adjMinPhysicalArmor":690,"adjMaxPhysicalArmor":690,"adjMinMagicArmor":690,"adjMaxMagicArmor":690})
    }),
    52004025: _tools.RODict({
        "propID": 52004025,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4450000,"adjMinPhysicalArmor":820,"adjMaxPhysicalArmor":820,"adjMinMagicArmor":820,"adjMaxMagicArmor":820})
    }),
    52004026: _tools.RODict({
        "propID": 52004026,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1200000,"adjMinPhysicalArmor":350,"adjMaxPhysicalArmor":350,"adjMinMagicArmor":350,"adjMaxMagicArmor":350})
    }),
    52004027: _tools.RODict({
        "propID": 52004027,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1650000,"adjMinPhysicalArmor":430,"adjMaxPhysicalArmor":430,"adjMinMagicArmor":430,"adjMaxMagicArmor":430})
    }),
    52004028: _tools.RODict({
        "propID": 52004028,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2450000,"adjMinPhysicalArmor":550,"adjMaxPhysicalArmor":550,"adjMinMagicArmor":550,"adjMaxMagicArmor":550})
    }),
    52004029: _tools.RODict({
        "propID": 52004029,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3750000,"adjMinPhysicalArmor":760,"adjMaxPhysicalArmor":760,"adjMinMagicArmor":760,"adjMaxMagicArmor":760})
    }),
    52004030: _tools.RODict({
        "propID": 52004030,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4900000,"adjMinPhysicalArmor":900,"adjMaxPhysicalArmor":900,"adjMinMagicArmor":900,"adjMaxMagicArmor":900})
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
        "propList": _tools.RODict({"adjMinMagicAtk":55,"adjMaxMagicAtk":120})
    }),
    52012151: _tools.RODict({
        "propID": 52012151,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":61,"adjMaxMagicAtk":132})
    }),
    52012152: _tools.RODict({
        "propID": 52012152,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":66,"adjMaxMagicAtk":144})
    }),
    52012153: _tools.RODict({
        "propID": 52012153,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":72,"adjMaxMagicAtk":156})
    }),
    52012154: _tools.RODict({
        "propID": 52012154,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":77,"adjMaxMagicAtk":168,"adjHit":10,"adjFinalDmg":0.02})
    }),
    52012155: _tools.RODict({
        "propID": 52012155,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":85,"adjMaxMagicAtk":185,"adjHit":11,"adjFinalDmg":0.02})
    }),
    52012156: _tools.RODict({
        "propID": 52012156,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":92,"adjMaxMagicAtk":202,"adjHit":12,"adjFinalDmg":0.02})
    }),
    52012157: _tools.RODict({
        "propID": 52012157,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":100,"adjMaxMagicAtk":218,"adjHit":13,"adjFinalDmg":0.02})
    }),
    52012158: _tools.RODict({
        "propID": 52012158,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":108,"adjMaxMagicAtk":235,"adjHit":14,"adjFinalDmg":0.04})
    }),
    52012159: _tools.RODict({
        "propID": 52012159,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":119,"adjMaxMagicAtk":259,"adjHit":15,"adjFinalDmg":0.04})
    }),
    52012160: _tools.RODict({
        "propID": 52012160,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":130,"adjMaxMagicAtk":282,"adjHit":17,"adjFinalDmg":0.04})
    }),
    52012161: _tools.RODict({
        "propID": 52012161,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":140,"adjMaxMagicAtk":306,"adjHit":18,"adjFinalDmg":0.04})
    }),
    52012162: _tools.RODict({
        "propID": 52012162,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":161,"adjMaxMagicAtk":352,"adjHit":21,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012163: _tools.RODict({
        "propID": 52012163,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":177,"adjMaxMagicAtk":387,"adjHit":23,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012164: _tools.RODict({
        "propID": 52012164,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":195,"adjMaxMagicAtk":426,"adjHit":25,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012165: _tools.RODict({
        "propID": 52012165,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":215,"adjMaxMagicAtk":469,"adjHit":28,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012326: _tools.RODict({
        "propID": 52012326,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":55,"adjMaxMagicAtk":120})
    }),
    52012327: _tools.RODict({
        "propID": 52012327,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":61,"adjMaxMagicAtk":132})
    }),
    52012328: _tools.RODict({
        "propID": 52012328,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":66,"adjMaxMagicAtk":144})
    }),
    52012329: _tools.RODict({
        "propID": 52012329,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":72,"adjMaxMagicAtk":156})
    }),
    52012330: _tools.RODict({
        "propID": 52012330,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":77,"adjMaxMagicAtk":168,"adjHit":10,"adjFinalDmg":0.02})
    }),
    52012331: _tools.RODict({
        "propID": 52012331,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":85,"adjMaxMagicAtk":185,"adjHit":11,"adjFinalDmg":0.02})
    }),
    52012332: _tools.RODict({
        "propID": 52012332,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":92,"adjMaxMagicAtk":202,"adjHit":12,"adjFinalDmg":0.02})
    }),
    52012333: _tools.RODict({
        "propID": 52012333,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":100,"adjMaxMagicAtk":218,"adjHit":13,"adjFinalDmg":0.02})
    }),
    52012334: _tools.RODict({
        "propID": 52012334,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":108,"adjMaxMagicAtk":235,"adjHit":14,"adjFinalDmg":0.04})
    }),
    52012335: _tools.RODict({
        "propID": 52012335,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":119,"adjMaxMagicAtk":259,"adjHit":15,"adjFinalDmg":0.04})
    }),
    52012336: _tools.RODict({
        "propID": 52012336,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":130,"adjMaxMagicAtk":282,"adjHit":17,"adjFinalDmg":0.04})
    }),
    52012337: _tools.RODict({
        "propID": 52012337,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":140,"adjMaxMagicAtk":306,"adjHit":18,"adjFinalDmg":0.04})
    }),
    52012338: _tools.RODict({
        "propID": 52012338,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":161,"adjMaxMagicAtk":352,"adjHit":21,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012339: _tools.RODict({
        "propID": 52012339,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":177,"adjMaxMagicAtk":387,"adjHit":23,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012340: _tools.RODict({
        "propID": 52012340,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":195,"adjMaxMagicAtk":426,"adjHit":25,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012341: _tools.RODict({
        "propID": 52012341,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":215,"adjMaxMagicAtk":469,"adjHit":28,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012502: _tools.RODict({
        "propID": 52012502,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":55,"adjMaxPhysicalAtk":120})
    }),
    52012503: _tools.RODict({
        "propID": 52012503,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":61,"adjMaxPhysicalAtk":132})
    }),
    52012504: _tools.RODict({
        "propID": 52012504,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":66,"adjMaxPhysicalAtk":144})
    }),
    52012505: _tools.RODict({
        "propID": 52012505,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":72,"adjMaxPhysicalAtk":156})
    }),
    52012506: _tools.RODict({
        "propID": 52012506,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":77,"adjMaxPhysicalAtk":168,"adjHit":10,"adjFinalDmg":0.02})
    }),
    52012507: _tools.RODict({
        "propID": 52012507,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":85,"adjMaxPhysicalAtk":185,"adjHit":11,"adjFinalDmg":0.02})
    }),
    52012508: _tools.RODict({
        "propID": 52012508,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":92,"adjMaxPhysicalAtk":202,"adjHit":12,"adjFinalDmg":0.02})
    }),
    52012509: _tools.RODict({
        "propID": 52012509,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":100,"adjMaxPhysicalAtk":218,"adjHit":13,"adjFinalDmg":0.02})
    }),
    52012510: _tools.RODict({
        "propID": 52012510,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":108,"adjMaxPhysicalAtk":235,"adjHit":14,"adjFinalDmg":0.04})
    }),
    52012511: _tools.RODict({
        "propID": 52012511,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":119,"adjMaxPhysicalAtk":259,"adjHit":15,"adjFinalDmg":0.04})
    }),
    52012512: _tools.RODict({
        "propID": 52012512,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":130,"adjMaxPhysicalAtk":282,"adjHit":17,"adjFinalDmg":0.04})
    }),
    52012513: _tools.RODict({
        "propID": 52012513,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":140,"adjMaxPhysicalAtk":306,"adjHit":18,"adjFinalDmg":0.04})
    }),
    52012514: _tools.RODict({
        "propID": 52012514,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":161,"adjMaxPhysicalAtk":352,"adjHit":21,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012515: _tools.RODict({
        "propID": 52012515,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":177,"adjMaxPhysicalAtk":387,"adjHit":23,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012516: _tools.RODict({
        "propID": 52012516,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":195,"adjMaxPhysicalAtk":426,"adjHit":25,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012517: _tools.RODict({
        "propID": 52012517,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":215,"adjMaxPhysicalAtk":469,"adjHit":28,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012678: _tools.RODict({
        "propID": 52012678,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":60,"adjMaxPhysicalArmor":90,"adjMinMagicArmor":60,"adjMaxMagicArmor":90})
    }),
    52012679: _tools.RODict({
        "propID": 52012679,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":66,"adjMaxPhysicalArmor":99,"adjMinMagicArmor":66,"adjMaxMagicArmor":99})
    }),
    52012680: _tools.RODict({
        "propID": 52012680,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":72,"adjMaxPhysicalArmor":108,"adjMinMagicArmor":72,"adjMaxMagicArmor":108})
    }),
    52012681: _tools.RODict({
        "propID": 52012681,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":78,"adjMaxPhysicalArmor":117,"adjMinMagicArmor":78,"adjMaxMagicArmor":117})
    }),
    52012682: _tools.RODict({
        "propID": 52012682,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":84,"adjMaxPhysicalArmor":126,"adjMinMagicArmor":84,"adjMaxMagicArmor":126,"adjMortal":0.05})
    }),
    52012683: _tools.RODict({
        "propID": 52012683,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":92,"adjMaxPhysicalArmor":139,"adjMinMagicArmor":92,"adjMaxMagicArmor":139,"adjMortal":0.05})
    }),
    52012684: _tools.RODict({
        "propID": 52012684,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":101,"adjMaxPhysicalArmor":151,"adjMinMagicArmor":101,"adjMaxMagicArmor":151,"adjMortal":0.05})
    }),
    52012685: _tools.RODict({
        "propID": 52012685,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":109,"adjMaxPhysicalArmor":164,"adjMinMagicArmor":109,"adjMaxMagicArmor":164,"adjMortal":0.05})
    }),
    52012686: _tools.RODict({
        "propID": 52012686,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":118,"adjMaxPhysicalArmor":176,"adjMinMagicArmor":118,"adjMaxMagicArmor":176,"adjMortal":0.1})
    }),
    52012687: _tools.RODict({
        "propID": 52012687,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":130,"adjMaxPhysicalArmor":194,"adjMinMagicArmor":130,"adjMaxMagicArmor":194,"adjMortal":0.1})
    }),
    52012688: _tools.RODict({
        "propID": 52012688,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":142,"adjMaxPhysicalArmor":211,"adjMinMagicArmor":142,"adjMaxMagicArmor":211,"adjMortal":0.1})
    }),
    52012689: _tools.RODict({
        "propID": 52012689,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":153,"adjMaxPhysicalArmor":229,"adjMinMagicArmor":153,"adjMaxMagicArmor":229,"adjMortal":0.1})
    }),
    52012690: _tools.RODict({
        "propID": 52012690,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":176,"adjMaxPhysicalArmor":263,"adjMinMagicArmor":176,"adjMaxMagicArmor":263,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012691: _tools.RODict({
        "propID": 52012691,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":194,"adjMaxPhysicalArmor":289,"adjMinMagicArmor":194,"adjMaxMagicArmor":289,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012692: _tools.RODict({
        "propID": 52012692,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":213,"adjMaxPhysicalArmor":318,"adjMinMagicArmor":213,"adjMaxMagicArmor":318,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012693: _tools.RODict({
        "propID": 52012693,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":234,"adjMaxPhysicalArmor":350,"adjMinMagicArmor":234,"adjMaxMagicArmor":350,"adjMortal":0.1,"adjAntiMortal":0.1})
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
        "propList": _tools.RODict({"adjMinMagicArmor":28,"adjMaxMagicArmor":42,"adjAntiFatal":10,"adjMortal":0.05})
    }),
    52012859: _tools.RODict({
        "propID": 52012859,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":31,"adjMaxMagicArmor":46,"adjAntiFatal":11,"adjMortal":0.05})
    }),
    52012860: _tools.RODict({
        "propID": 52012860,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":34,"adjMaxMagicArmor":50,"adjAntiFatal":12,"adjMortal":0.05})
    }),
    52012861: _tools.RODict({
        "propID": 52012861,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":36,"adjMaxMagicArmor":55,"adjAntiFatal":13,"adjMortal":0.05})
    }),
    52012862: _tools.RODict({
        "propID": 52012862,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":39,"adjMaxMagicArmor":59,"adjAntiFatal":14,"adjMortal":0.1})
    }),
    52012863: _tools.RODict({
        "propID": 52012863,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":43,"adjMaxMagicArmor":65,"adjAntiFatal":15,"adjMortal":0.1})
    }),
    52012864: _tools.RODict({
        "propID": 52012864,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":47,"adjMaxMagicArmor":71,"adjAntiFatal":17,"adjMortal":0.1})
    }),
    52012865: _tools.RODict({
        "propID": 52012865,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":51,"adjMaxMagicArmor":77,"adjAntiFatal":18,"adjMortal":0.1})
    }),
    52012866: _tools.RODict({
        "propID": 52012866,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":59,"adjMaxMagicArmor":89,"adjAntiFatal":21,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012867: _tools.RODict({
        "propID": 52012867,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":65,"adjMaxMagicArmor":98,"adjAntiFatal":23,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012868: _tools.RODict({
        "propID": 52012868,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":72,"adjMaxMagicArmor":108,"adjAntiFatal":25,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012869: _tools.RODict({
        "propID": 52012869,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":79,"adjMaxMagicArmor":119,"adjAntiFatal":28,"adjMortal":0.1,"adjAntiMortal":0.1})
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
        "propList": _tools.RODict({"adjMinPhysicalArmor":28,"adjMaxPhysicalArmor":42,"adjDodge":10,"adjPVPDmg":0.02})
    }),
    52013035: _tools.RODict({
        "propID": 52013035,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":31,"adjMaxPhysicalArmor":46,"adjDodge":11,"adjPVPDmg":0.02})
    }),
    52013036: _tools.RODict({
        "propID": 52013036,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":34,"adjMaxPhysicalArmor":50,"adjDodge":12,"adjPVPDmg":0.02})
    }),
    52013037: _tools.RODict({
        "propID": 52013037,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":36,"adjMaxPhysicalArmor":55,"adjDodge":13,"adjPVPDmg":0.02})
    }),
    52013038: _tools.RODict({
        "propID": 52013038,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":39,"adjMaxPhysicalArmor":59,"adjDodge":14,"adjPVPDmg":0.04})
    }),
    52013039: _tools.RODict({
        "propID": 52013039,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":43,"adjMaxPhysicalArmor":65,"adjDodge":15,"adjPVPDmg":0.04})
    }),
    52013040: _tools.RODict({
        "propID": 52013040,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":47,"adjMaxPhysicalArmor":71,"adjDodge":17,"adjPVPDmg":0.04})
    }),
    52013041: _tools.RODict({
        "propID": 52013041,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":51,"adjMaxPhysicalArmor":77,"adjDodge":18,"adjPVPDmg":0.04})
    }),
    52013042: _tools.RODict({
        "propID": 52013042,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":59,"adjMaxPhysicalArmor":89,"adjDodge":21,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013043: _tools.RODict({
        "propID": 52013043,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":65,"adjMaxPhysicalArmor":98,"adjDodge":23,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013044: _tools.RODict({
        "propID": 52013044,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":72,"adjMaxPhysicalArmor":108,"adjDodge":25,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013045: _tools.RODict({
        "propID": 52013045,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":79,"adjMaxPhysicalArmor":119,"adjDodge":28,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013206: _tools.RODict({
        "propID": 52013206,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":14,"adjMaxPhysicalAtk":30})
    }),
    52013207: _tools.RODict({
        "propID": 52013207,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":15,"adjMaxPhysicalAtk":33})
    }),
    52013208: _tools.RODict({
        "propID": 52013208,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":36})
    }),
    52013209: _tools.RODict({
        "propID": 52013209,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":18,"adjMaxPhysicalAtk":39})
    }),
    52013210: _tools.RODict({
        "propID": 52013210,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":42,"adjFatal":10,"adjIgnoreArmor":0.04})
    }),
    52013211: _tools.RODict({
        "propID": 52013211,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":46,"adjFatal":11,"adjIgnoreArmor":0.04})
    }),
    52013212: _tools.RODict({
        "propID": 52013212,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":50,"adjFatal":12,"adjIgnoreArmor":0.04})
    }),
    52013213: _tools.RODict({
        "propID": 52013213,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":55,"adjFatal":13,"adjIgnoreArmor":0.04})
    }),
    52013214: _tools.RODict({
        "propID": 52013214,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":28,"adjMaxPhysicalAtk":59,"adjFatal":14,"adjIgnoreArmor":0.08})
    }),
    52013215: _tools.RODict({
        "propID": 52013215,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":31,"adjMaxPhysicalAtk":65,"adjFatal":15,"adjIgnoreArmor":0.08})
    }),
    52013216: _tools.RODict({
        "propID": 52013216,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":34,"adjMaxPhysicalAtk":71,"adjFatal":17,"adjIgnoreArmor":0.08})
    }),
    52013217: _tools.RODict({
        "propID": 52013217,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":36,"adjMaxPhysicalAtk":77,"adjFatal":18,"adjIgnoreArmor":0.08})
    }),
    52013218: _tools.RODict({
        "propID": 52013218,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":41,"adjMaxPhysicalAtk":89,"adjFatal":21,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013219: _tools.RODict({
        "propID": 52013219,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":45,"adjMaxPhysicalAtk":98,"adjFatal":23,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013220: _tools.RODict({
        "propID": 52013220,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":50,"adjMaxPhysicalAtk":108,"adjFatal":25,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013221: _tools.RODict({
        "propID": 52013221,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":55,"adjMaxPhysicalAtk":119,"adjFatal":28,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013382: _tools.RODict({
        "propID": 52013382,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":14,"adjMaxMagicAtk":30})
    }),
    52013383: _tools.RODict({
        "propID": 52013383,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":15,"adjMaxMagicAtk":33})
    }),
    52013384: _tools.RODict({
        "propID": 52013384,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":17,"adjMaxMagicAtk":36})
    }),
    52013385: _tools.RODict({
        "propID": 52013385,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":18,"adjMaxMagicAtk":39})
    }),
    52013386: _tools.RODict({
        "propID": 52013386,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":20,"adjMaxMagicAtk":42,"adjFatal":10,"adjIgnoreArmor":0.04})
    }),
    52013387: _tools.RODict({
        "propID": 52013387,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":22,"adjMaxMagicAtk":46,"adjFatal":11,"adjIgnoreArmor":0.04})
    }),
    52013388: _tools.RODict({
        "propID": 52013388,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":24,"adjMaxMagicAtk":50,"adjFatal":12,"adjIgnoreArmor":0.04})
    }),
    52013389: _tools.RODict({
        "propID": 52013389,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":26,"adjMaxMagicAtk":55,"adjFatal":13,"adjIgnoreArmor":0.04})
    }),
    52013390: _tools.RODict({
        "propID": 52013390,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":28,"adjMaxMagicAtk":59,"adjFatal":14,"adjIgnoreArmor":0.08})
    }),
    52013391: _tools.RODict({
        "propID": 52013391,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":31,"adjMaxMagicAtk":65,"adjFatal":15,"adjIgnoreArmor":0.08})
    }),
    52013392: _tools.RODict({
        "propID": 52013392,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":34,"adjMaxMagicAtk":71,"adjFatal":17,"adjIgnoreArmor":0.08})
    }),
    52013393: _tools.RODict({
        "propID": 52013393,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":36,"adjMaxMagicAtk":77,"adjFatal":18,"adjIgnoreArmor":0.08})
    }),
    52013394: _tools.RODict({
        "propID": 52013394,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":41,"adjMaxMagicAtk":89,"adjFatal":21,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013395: _tools.RODict({
        "propID": 52013395,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":45,"adjMaxMagicAtk":98,"adjFatal":23,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013396: _tools.RODict({
        "propID": 52013396,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":50,"adjMaxMagicAtk":108,"adjFatal":25,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013397: _tools.RODict({
        "propID": 52013397,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":55,"adjMaxMagicAtk":119,"adjFatal":28,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013558: _tools.RODict({
        "propID": 52013558,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":160,"adjMinPhysicalAtk":9,"adjMaxPhysicalAtk":20})
    }),
    52013559: _tools.RODict({
        "propID": 52013559,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":176,"adjMinPhysicalAtk":10,"adjMaxPhysicalAtk":22})
    }),
    52013560: _tools.RODict({
        "propID": 52013560,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":192,"adjMinPhysicalAtk":11,"adjMaxPhysicalAtk":24})
    }),
    52013561: _tools.RODict({
        "propID": 52013561,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":208,"adjMinPhysicalAtk":12,"adjMaxPhysicalAtk":26})
    }),
    52013562: _tools.RODict({
        "propID": 52013562,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":224,"adjMinPhysicalAtk":13,"adjMaxPhysicalAtk":28,"adjIgnoreArmor":0.02})
    }),
    52013563: _tools.RODict({
        "propID": 52013563,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":246,"adjMinPhysicalAtk":14,"adjMaxPhysicalAtk":31,"adjIgnoreArmor":0.02})
    }),
    52013564: _tools.RODict({
        "propID": 52013564,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":269,"adjMinPhysicalAtk":16,"adjMaxPhysicalAtk":34,"adjIgnoreArmor":0.02})
    }),
    52013565: _tools.RODict({
        "propID": 52013565,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":291,"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":36,"adjIgnoreArmor":0.02})
    }),
    52013566: _tools.RODict({
        "propID": 52013566,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":314,"adjMinPhysicalAtk":18,"adjMaxPhysicalAtk":39,"adjIgnoreArmor":0.04})
    }),
    52013567: _tools.RODict({
        "propID": 52013567,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":345,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":43,"adjIgnoreArmor":0.04})
    }),
    52013568: _tools.RODict({
        "propID": 52013568,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":377,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":47,"adjIgnoreArmor":0.04})
    }),
    52013569: _tools.RODict({
        "propID": 52013569,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":408,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":51,"adjIgnoreArmor":0.04})
    }),
    52013570: _tools.RODict({
        "propID": 52013570,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":469,"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":59,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013571: _tools.RODict({
        "propID": 52013571,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":516,"adjMinPhysicalAtk":29,"adjMaxPhysicalAtk":65,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013572: _tools.RODict({
        "propID": 52013572,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":568,"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":72,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013573: _tools.RODict({
        "propID": 52013573,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":625,"adjMinPhysicalAtk":35,"adjMaxPhysicalAtk":79,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013734: _tools.RODict({
        "propID": 52013734,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":160,"adjMinMagicAtk":9,"adjMaxMagicAtk":20})
    }),
    52013735: _tools.RODict({
        "propID": 52013735,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":176,"adjMinMagicAtk":10,"adjMaxMagicAtk":22})
    }),
    52013736: _tools.RODict({
        "propID": 52013736,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":192,"adjMinMagicAtk":11,"adjMaxMagicAtk":24})
    }),
    52013737: _tools.RODict({
        "propID": 52013737,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":208,"adjMinMagicAtk":12,"adjMaxMagicAtk":26})
    }),
    52013738: _tools.RODict({
        "propID": 52013738,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":224,"adjMinMagicAtk":13,"adjMaxMagicAtk":28,"adjIgnoreArmor":0.02})
    }),
    52013739: _tools.RODict({
        "propID": 52013739,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":246,"adjMinMagicAtk":14,"adjMaxMagicAtk":31,"adjIgnoreArmor":0.02})
    }),
    52013740: _tools.RODict({
        "propID": 52013740,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":269,"adjMinMagicAtk":16,"adjMaxMagicAtk":34,"adjIgnoreArmor":0.02})
    }),
    52013741: _tools.RODict({
        "propID": 52013741,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":291,"adjMinMagicAtk":17,"adjMaxMagicAtk":36,"adjIgnoreArmor":0.02})
    }),
    52013742: _tools.RODict({
        "propID": 52013742,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":314,"adjMinMagicAtk":18,"adjMaxMagicAtk":39,"adjIgnoreArmor":0.04})
    }),
    52013743: _tools.RODict({
        "propID": 52013743,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":345,"adjMinMagicAtk":20,"adjMaxMagicAtk":43,"adjIgnoreArmor":0.04})
    }),
    52013744: _tools.RODict({
        "propID": 52013744,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":377,"adjMinMagicAtk":22,"adjMaxMagicAtk":47,"adjIgnoreArmor":0.04})
    }),
    52013745: _tools.RODict({
        "propID": 52013745,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":408,"adjMinMagicAtk":23,"adjMaxMagicAtk":51,"adjIgnoreArmor":0.04})
    }),
    52013746: _tools.RODict({
        "propID": 52013746,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":469,"adjMinMagicAtk":26,"adjMaxMagicAtk":59,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013747: _tools.RODict({
        "propID": 52013747,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":516,"adjMinMagicAtk":29,"adjMaxMagicAtk":65,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013748: _tools.RODict({
        "propID": 52013748,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":568,"adjMinMagicAtk":32,"adjMaxMagicAtk":72,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013749: _tools.RODict({
        "propID": 52013749,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":625,"adjMinMagicAtk":35,"adjMaxMagicAtk":79,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013910: _tools.RODict({
        "propID": 52013910,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":872,"adjMinPhysicalAtk":11,"adjMaxPhysicalAtk":25})
    }),
    52013911: _tools.RODict({
        "propID": 52013911,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":959,"adjMinPhysicalAtk":12,"adjMaxPhysicalAtk":28})
    }),
    52013912: _tools.RODict({
        "propID": 52013912,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1046,"adjMinPhysicalAtk":13,"adjMaxPhysicalAtk":30})
    }),
    52013913: _tools.RODict({
        "propID": 52013913,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1134,"adjMinPhysicalAtk":14,"adjMaxPhysicalAtk":33})
    }),
    52013914: _tools.RODict({
        "propID": 52013914,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1221,"adjMinPhysicalAtk":15,"adjMaxPhysicalAtk":35,"adjMonsterDmg":0.025})
    }),
    52013915: _tools.RODict({
        "propID": 52013915,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1343,"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":39,"adjMonsterDmg":0.025})
    }),
    52013916: _tools.RODict({
        "propID": 52013916,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1465,"adjMinPhysicalAtk":18,"adjMaxPhysicalAtk":42,"adjMonsterDmg":0.025})
    }),
    52013917: _tools.RODict({
        "propID": 52013917,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1587,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":46,"adjMonsterDmg":0.025})
    }),
    52013918: _tools.RODict({
        "propID": 52013918,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1709,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":49,"adjMonsterDmg":0.05})
    }),
    52013919: _tools.RODict({
        "propID": 52013919,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1880,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":54,"adjMonsterDmg":0.05})
    }),
    52013920: _tools.RODict({
        "propID": 52013920,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2051,"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":59,"adjMonsterDmg":0.05})
    }),
    52013921: _tools.RODict({
        "propID": 52013921,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2222,"adjMinPhysicalAtk":27,"adjMaxPhysicalAtk":64,"adjMonsterDmg":0.05})
    }),
    52013922: _tools.RODict({
        "propID": 52013922,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2555,"adjMinPhysicalAtk":31,"adjMaxPhysicalAtk":74,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52013923: _tools.RODict({
        "propID": 52013923,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2811,"adjMinPhysicalAtk":34,"adjMaxPhysicalAtk":81,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52013924: _tools.RODict({
        "propID": 52013924,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3092,"adjMinPhysicalAtk":37,"adjMaxPhysicalAtk":89,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52013925: _tools.RODict({
        "propID": 52013925,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3401,"adjMinPhysicalAtk":41,"adjMaxPhysicalAtk":98,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014086: _tools.RODict({
        "propID": 52014086,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":872,"adjMinMagicAtk":11,"adjMaxMagicAtk":25})
    }),
    52014087: _tools.RODict({
        "propID": 52014087,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":959,"adjMinMagicAtk":12,"adjMaxMagicAtk":28})
    }),
    52014088: _tools.RODict({
        "propID": 52014088,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1046,"adjMinMagicAtk":13,"adjMaxMagicAtk":30})
    }),
    52014089: _tools.RODict({
        "propID": 52014089,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1134,"adjMinMagicAtk":14,"adjMaxMagicAtk":33})
    }),
    52014090: _tools.RODict({
        "propID": 52014090,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1221,"adjMinMagicAtk":15,"adjMaxMagicAtk":35,"adjMonsterDmg":0.025})
    }),
    52014091: _tools.RODict({
        "propID": 52014091,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1343,"adjMinMagicAtk":17,"adjMaxMagicAtk":39,"adjMonsterDmg":0.025})
    }),
    52014092: _tools.RODict({
        "propID": 52014092,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1465,"adjMinMagicAtk":18,"adjMaxMagicAtk":42,"adjMonsterDmg":0.025})
    }),
    52014093: _tools.RODict({
        "propID": 52014093,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1587,"adjMinMagicAtk":20,"adjMaxMagicAtk":46,"adjMonsterDmg":0.025})
    }),
    52014094: _tools.RODict({
        "propID": 52014094,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1709,"adjMinMagicAtk":21,"adjMaxMagicAtk":49,"adjMonsterDmg":0.05})
    }),
    52014095: _tools.RODict({
        "propID": 52014095,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1880,"adjMinMagicAtk":23,"adjMaxMagicAtk":54,"adjMonsterDmg":0.05})
    }),
    52014096: _tools.RODict({
        "propID": 52014096,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2051,"adjMinMagicAtk":25,"adjMaxMagicAtk":59,"adjMonsterDmg":0.05})
    }),
    52014097: _tools.RODict({
        "propID": 52014097,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2222,"adjMinMagicAtk":27,"adjMaxMagicAtk":64,"adjMonsterDmg":0.05})
    }),
    52014098: _tools.RODict({
        "propID": 52014098,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2555,"adjMinMagicAtk":31,"adjMaxMagicAtk":74,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014099: _tools.RODict({
        "propID": 52014099,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2811,"adjMinMagicAtk":34,"adjMaxMagicAtk":81,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014100: _tools.RODict({
        "propID": 52014100,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3092,"adjMinMagicAtk":37,"adjMaxMagicAtk":89,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014101: _tools.RODict({
        "propID": 52014101,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3401,"adjMinMagicAtk":41,"adjMaxMagicAtk":98,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014262: _tools.RODict({
        "propID": 52014262,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":872,"adjDrugsQuantity":3})
    }),
    52014263: _tools.RODict({
        "propID": 52014263,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":959,"adjDrugsQuantity":3})
    }),
    52014264: _tools.RODict({
        "propID": 52014264,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1046,"adjDrugsQuantity":3})
    }),
    52014265: _tools.RODict({
        "propID": 52014265,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1134,"adjDrugsQuantity":3})
    }),
    52014266: _tools.RODict({
        "propID": 52014266,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1221,"adjDrugsQuantity":10,"adjFinalDmg":0.02})
    }),
    52014267: _tools.RODict({
        "propID": 52014267,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1343,"adjDrugsQuantity":10,"adjFinalDmg":0.02})
    }),
    52014268: _tools.RODict({
        "propID": 52014268,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1465,"adjDrugsQuantity":10,"adjFinalDmg":0.02})
    }),
    52014269: _tools.RODict({
        "propID": 52014269,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1587,"adjDrugsQuantity":10,"adjFinalDmg":0.02})
    }),
    52014270: _tools.RODict({
        "propID": 52014270,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1709,"adjDrugsQuantity":20,"adjFinalDmg":0.04})
    }),
    52014271: _tools.RODict({
        "propID": 52014271,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1880,"adjDrugsQuantity":20,"adjFinalDmg":0.04})
    }),
    52014272: _tools.RODict({
        "propID": 52014272,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2051,"adjDrugsQuantity":20,"adjFinalDmg":0.04})
    }),
    52014273: _tools.RODict({
        "propID": 52014273,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2222,"adjDrugsQuantity":20,"adjFinalDmg":0.04})
    }),
    52014274: _tools.RODict({
        "propID": 52014274,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2555,"adjDrugsQuantity":30,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014275: _tools.RODict({
        "propID": 52014275,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2811,"adjDrugsQuantity":30,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014276: _tools.RODict({
        "propID": 52014276,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3092,"adjDrugsQuantity":30,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014277: _tools.RODict({
        "propID": 52014277,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3401,"adjDrugsQuantity":30,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    })
})
minKey = 51000001
maxKey = 52014277