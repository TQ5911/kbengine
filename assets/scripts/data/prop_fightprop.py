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
        "propList": _tools.RODict({"adjFullHp":100,"adjMinPhysicalAtk":6,"adjMaxPhysicalAtk":15,"adjMinMagicAtk":13,"adjMaxMagicAtk":20,"adjMinPhysicalArmor":6,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":6,"adjMaxMagicArmor":10,"adjHit":1,"adjDodge":1})
    }),
    51000002: _tools.RODict({
        "propID": 51000002,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":120,"adjMinPhysicalAtk":9,"adjMaxPhysicalAtk":20,"adjMinMagicAtk":14,"adjMaxMagicAtk":30,"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":15,"adjMinMagicArmor":10,"adjMaxMagicArmor":15,"adjHit":1,"adjDodge":1})
    }),
    51000003: _tools.RODict({
        "propID": 51000003,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":140,"adjMinPhysicalAtk":13,"adjMaxPhysicalAtk":30,"adjMinMagicAtk":15,"adjMaxMagicAtk":40,"adjMinPhysicalArmor":13,"adjMaxPhysicalArmor":20,"adjMinMagicArmor":13,"adjMaxMagicArmor":20,"adjHit":2,"adjDodge":2})
    }),
    51000004: _tools.RODict({
        "propID": 51000004,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":160,"adjMinPhysicalAtk":18,"adjMaxPhysicalAtk":40,"adjMinMagicAtk":67,"adjMaxMagicAtk":50,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":25,"adjMinMagicArmor":16,"adjMaxMagicArmor":25,"adjHit":2,"adjDodge":2})
    }),
    51000005: _tools.RODict({
        "propID": 51000005,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":180,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":50,"adjMinMagicAtk":68,"adjMaxMagicAtk":60,"adjMinPhysicalArmor":20,"adjMaxPhysicalArmor":30,"adjMinMagicArmor":20,"adjMaxMagicArmor":30,"adjHit":3,"adjDodge":3})
    }),
    51000006: _tools.RODict({
        "propID": 51000006,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":200,"adjMinPhysicalAtk":27,"adjMaxPhysicalAtk":60,"adjMinMagicAtk":69,"adjMaxMagicAtk":70,"adjMinPhysicalArmor":23,"adjMaxPhysicalArmor":35,"adjMinMagicArmor":23,"adjMaxMagicArmor":35,"adjHit":3,"adjDodge":3})
    }),
    51000007: _tools.RODict({
        "propID": 51000007,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":220,"adjMinPhysicalAtk":31,"adjMaxPhysicalAtk":70,"adjMinMagicAtk":78,"adjMaxMagicAtk":80,"adjMinPhysicalArmor":26,"adjMaxPhysicalArmor":40,"adjMinMagicArmor":26,"adjMaxMagicArmor":40,"adjHit":4,"adjDodge":4})
    }),
    51000008: _tools.RODict({
        "propID": 51000008,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":240,"adjMinPhysicalAtk":36,"adjMaxPhysicalAtk":80,"adjMinMagicAtk":79,"adjMaxMagicAtk":90,"adjMinPhysicalArmor":30,"adjMaxPhysicalArmor":45,"adjMinMagicArmor":30,"adjMaxMagicArmor":45,"adjHit":4,"adjDodge":4})
    }),
    51000009: _tools.RODict({
        "propID": 51000009,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":260,"adjMinPhysicalAtk":40,"adjMaxPhysicalAtk":90,"adjMinMagicAtk":79,"adjMaxMagicAtk":100,"adjMinPhysicalArmor":33,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":33,"adjMaxMagicArmor":50,"adjHit":5,"adjDodge":5})
    }),
    51000010: _tools.RODict({
        "propID": 51000010,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":280,"adjMinPhysicalAtk":45,"adjMaxPhysicalAtk":100,"adjMinMagicAtk":98,"adjMaxMagicAtk":110,"adjMinPhysicalArmor":36,"adjMaxPhysicalArmor":55,"adjMinMagicArmor":36,"adjMaxMagicArmor":55,"adjHit":5,"adjDodge":5})
    }),
    51000011: _tools.RODict({
        "propID": 51000011,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":300,"adjMinPhysicalAtk":50,"adjMaxPhysicalAtk":110,"adjMinMagicAtk":104,"adjMaxMagicAtk":120,"adjMinPhysicalArmor":40,"adjMaxPhysicalArmor":60,"adjMinMagicArmor":40,"adjMaxMagicArmor":60,"adjHit":6,"adjDodge":6})
    }),
    51000012: _tools.RODict({
        "propID": 51000012,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":320,"adjMinPhysicalAtk":54,"adjMaxPhysicalAtk":120,"adjMinMagicAtk":105,"adjMaxMagicAtk":130,"adjMinPhysicalArmor":43,"adjMaxPhysicalArmor":65,"adjMinMagicArmor":43,"adjMaxMagicArmor":65,"adjHit":6,"adjDodge":6})
    }),
    51000013: _tools.RODict({
        "propID": 51000013,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":340,"adjMinPhysicalAtk":59,"adjMaxPhysicalAtk":130,"adjMinMagicAtk":106,"adjMaxMagicAtk":140,"adjMinPhysicalArmor":46,"adjMaxPhysicalArmor":70,"adjMinMagicArmor":46,"adjMaxMagicArmor":70,"adjHit":7,"adjDodge":7})
    }),
    51000014: _tools.RODict({
        "propID": 51000014,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":360,"adjMinPhysicalAtk":63,"adjMaxPhysicalAtk":140,"adjMinMagicAtk":106,"adjMaxMagicAtk":150,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":75,"adjMinMagicArmor":50,"adjMaxMagicArmor":75,"adjHit":7,"adjDodge":7})
    }),
    51000015: _tools.RODict({
        "propID": 51000015,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":380,"adjMinPhysicalAtk":68,"adjMaxPhysicalAtk":150,"adjMinMagicAtk":109,"adjMaxMagicAtk":160,"adjMinPhysicalArmor":53,"adjMaxPhysicalArmor":80,"adjMinMagicArmor":53,"adjMaxMagicArmor":80,"adjHit":8,"adjDodge":8})
    }),
    51000016: _tools.RODict({
        "propID": 51000016,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":400,"adjMinPhysicalAtk":72,"adjMaxPhysicalAtk":160,"adjMinMagicAtk":123,"adjMaxMagicAtk":170,"adjMinPhysicalArmor":60,"adjMaxPhysicalArmor":90,"adjMinMagicArmor":60,"adjMaxMagicArmor":90,"adjHit":8,"adjDodge":8})
    }),
    51000017: _tools.RODict({
        "propID": 51000017,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":420,"adjMinPhysicalAtk":77,"adjMaxPhysicalAtk":170,"adjMinMagicAtk":124,"adjMaxMagicAtk":180,"adjMinPhysicalArmor":66,"adjMaxPhysicalArmor":100,"adjMinMagicArmor":66,"adjMaxMagicArmor":100,"adjHit":9,"adjDodge":9})
    }),
    51000018: _tools.RODict({
        "propID": 51000018,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":440,"adjMinPhysicalAtk":81,"adjMaxPhysicalAtk":180,"adjMinMagicAtk":126,"adjMaxMagicAtk":190,"adjMinPhysicalArmor":73,"adjMaxPhysicalArmor":110,"adjMinMagicArmor":73,"adjMaxMagicArmor":110,"adjHit":9,"adjDodge":9})
    }),
    51000019: _tools.RODict({
        "propID": 51000019,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":460,"adjMinPhysicalAtk":90,"adjMaxPhysicalAtk":200,"adjMinMagicAtk":127,"adjMaxMagicAtk":210,"adjMinPhysicalArmor":80,"adjMaxPhysicalArmor":120,"adjMinMagicArmor":80,"adjMaxMagicArmor":120,"adjHit":10,"adjDodge":10})
    }),
    51000020: _tools.RODict({
        "propID": 51000020,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":480,"adjMinPhysicalAtk":100,"adjMaxPhysicalAtk":220,"adjMinMagicAtk":128,"adjMaxMagicAtk":230,"adjMinPhysicalArmor":86,"adjMaxPhysicalArmor":130,"adjMinMagicArmor":86,"adjMaxMagicArmor":130,"adjHit":10,"adjDodge":10})
    }),
    51000021: _tools.RODict({
        "propID": 51000021,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":500,"adjMinPhysicalAtk":109,"adjMaxPhysicalAtk":240,"adjMinMagicAtk":130,"adjMaxMagicAtk":250,"adjMinPhysicalArmor":93,"adjMaxPhysicalArmor":140,"adjMinMagicArmor":93,"adjMaxMagicArmor":140,"adjHit":11,"adjDodge":11,"adjMortal":0.003,"adjAntiMortal":0.003})
    }),
    51000022: _tools.RODict({
        "propID": 51000022,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":520,"adjMinPhysicalAtk":118,"adjMaxPhysicalAtk":260,"adjMinMagicAtk":131,"adjMaxMagicAtk":270,"adjMinPhysicalArmor":100,"adjMaxPhysicalArmor":150,"adjMinMagicArmor":100,"adjMaxMagicArmor":150,"adjHit":11,"adjDodge":11,"adjMortal":0.003,"adjAntiMortal":0.003})
    }),
    51000023: _tools.RODict({
        "propID": 51000023,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":540,"adjMinPhysicalAtk":127,"adjMaxPhysicalAtk":280,"adjMinMagicAtk":142,"adjMaxMagicAtk":290,"adjMinPhysicalArmor":113,"adjMaxPhysicalArmor":170,"adjMinMagicArmor":113,"adjMaxMagicArmor":170,"adjHit":12,"adjDodge":12,"adjMortal":0.006,"adjAntiMortal":0.006})
    }),
    51000024: _tools.RODict({
        "propID": 51000024,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":560,"adjMinPhysicalAtk":136,"adjMaxPhysicalAtk":300,"adjMinMagicAtk":144,"adjMaxMagicAtk":310,"adjMinPhysicalArmor":126,"adjMaxPhysicalArmor":190,"adjMinMagicArmor":126,"adjMaxMagicArmor":190,"adjHit":12,"adjDodge":12,"adjMortal":0.006,"adjAntiMortal":0.006})
    }),
    51000025: _tools.RODict({
        "propID": 51000025,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":579,"adjMinPhysicalAtk":157,"adjMaxPhysicalAtk":345,"adjMinMagicAtk":157,"adjMaxMagicAtk":345,"adjMinPhysicalArmor":146,"adjMaxPhysicalArmor":219,"adjMinMagicArmor":146,"adjMaxMagicArmor":219,"adjHit":15,"adjDodge":15,"adjFatal":1,"adjAntiFatal":1,"adjMortal":0.009,"adjAntiMortal":0.009})
    }),
    51000026: _tools.RODict({
        "propID": 51000026,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":680,"adjMinPhysicalAtk":163,"adjMaxPhysicalAtk":359,"adjMinMagicAtk":163,"adjMaxMagicAtk":359,"adjMinPhysicalArmor":150,"adjMaxPhysicalArmor":226,"adjMinMagicArmor":150,"adjMaxMagicArmor":226,"adjHit":20,"adjDodge":20,"adjFatal":7,"adjAntiFatal":7,"adjMortal":0.009,"adjAntiMortal":0.009})
    }),
    51000027: _tools.RODict({
        "propID": 51000027,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":699,"adjMinPhysicalAtk":164,"adjMaxPhysicalAtk":361,"adjMinMagicAtk":164,"adjMaxMagicAtk":361,"adjMinPhysicalArmor":151,"adjMaxPhysicalArmor":227,"adjMinMagicArmor":151,"adjMaxMagicArmor":227,"adjHit":21,"adjDodge":21,"adjFatal":7,"adjAntiFatal":7,"adjMortal":0.012,"adjAntiMortal":0.012})
    }),
    51000028: _tools.RODict({
        "propID": 51000028,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":795,"adjMinPhysicalAtk":165,"adjMaxPhysicalAtk":364,"adjMinMagicAtk":165,"adjMaxMagicAtk":364,"adjMinPhysicalArmor":152,"adjMaxPhysicalArmor":228,"adjMinMagicArmor":152,"adjMaxMagicArmor":228,"adjHit":21,"adjDodge":21,"adjFatal":7,"adjAntiFatal":7,"adjMortal":0.012,"adjAntiMortal":0.012})
    }),
    51000029: _tools.RODict({
        "propID": 51000029,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":811,"adjMinPhysicalAtk":166,"adjMaxPhysicalAtk":366,"adjMinMagicAtk":166,"adjMaxMagicAtk":366,"adjMinPhysicalArmor":152,"adjMaxPhysicalArmor":229,"adjMinMagicArmor":152,"adjMaxMagicArmor":229,"adjHit":22,"adjDodge":22,"adjFatal":7,"adjAntiFatal":7,"adjMortal":0.015,"adjAntiMortal":0.015})
    }),
    51000030: _tools.RODict({
        "propID": 51000030,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":914,"adjMinPhysicalAtk":183,"adjMaxPhysicalAtk":402,"adjMinMagicAtk":183,"adjMaxMagicAtk":402,"adjMinPhysicalArmor":168,"adjMaxPhysicalArmor":252,"adjMinMagicArmor":168,"adjMaxMagicArmor":252,"adjHit":22,"adjDodge":22,"adjFatal":7,"adjAntiFatal":7,"adjMortal":0.015,"adjAntiMortal":0.015})
    }),
    51000031: _tools.RODict({
        "propID": 51000031,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":966,"adjMinPhysicalAtk":184,"adjMaxPhysicalAtk":406,"adjMinMagicAtk":184,"adjMaxMagicAtk":406,"adjMinPhysicalArmor":169,"adjMaxPhysicalArmor":254,"adjMinMagicArmor":169,"adjMaxMagicArmor":254,"adjHit":23,"adjDodge":23,"adjFatal":10,"adjAntiFatal":7,"adjMortal":0.018,"adjAntiMortal":0.018})
    }),
    51000032: _tools.RODict({
        "propID": 51000032,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":972,"adjMinPhysicalAtk":185,"adjMaxPhysicalAtk":407,"adjMinMagicAtk":185,"adjMaxMagicAtk":407,"adjMinPhysicalArmor":170,"adjMaxPhysicalArmor":255,"adjMinMagicArmor":170,"adjMaxMagicArmor":255,"adjHit":23,"adjDodge":23,"adjFatal":10,"adjAntiFatal":7,"adjMortal":0.018,"adjAntiMortal":0.018})
    }),
    51000033: _tools.RODict({
        "propID": 51000033,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1215,"adjMinPhysicalAtk":225,"adjMaxPhysicalAtk":496,"adjMinMagicAtk":225,"adjMaxMagicAtk":496,"adjMinPhysicalArmor":206,"adjMaxPhysicalArmor":310,"adjMinMagicArmor":206,"adjMaxMagicArmor":310,"adjHit":38,"adjDodge":38,"adjFatal":24,"adjAntiFatal":21,"adjMortal":0.121,"adjAntiMortal":0.021})
    }),
    51000034: _tools.RODict({
        "propID": 51000034,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1221,"adjMinPhysicalAtk":226,"adjMaxPhysicalAtk":498,"adjMinMagicAtk":226,"adjMaxMagicAtk":498,"adjMinPhysicalArmor":207,"adjMaxPhysicalArmor":311,"adjMinMagicArmor":207,"adjMaxMagicArmor":311,"adjHit":38,"adjDodge":38,"adjFatal":24,"adjAntiFatal":21,"adjMortal":0.121,"adjAntiMortal":0.021})
    }),
    51000035: _tools.RODict({
        "propID": 51000035,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1361,"adjMinPhysicalAtk":235,"adjMaxPhysicalAtk":517,"adjMinMagicAtk":235,"adjMaxMagicAtk":517,"adjMinPhysicalArmor":212,"adjMaxPhysicalArmor":318,"adjMinMagicArmor":212,"adjMaxMagicArmor":318,"adjHit":41,"adjDodge":41,"adjFatal":26,"adjAntiFatal":22,"adjMortal":0.124,"adjAntiMortal":0.024})
    }),
    51000036: _tools.RODict({
        "propID": 51000036,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1365,"adjMinPhysicalAtk":236,"adjMaxPhysicalAtk":520,"adjMinMagicAtk":236,"adjMaxMagicAtk":520,"adjMinPhysicalArmor":213,"adjMaxPhysicalArmor":320,"adjMinMagicArmor":213,"adjMaxMagicArmor":320,"adjHit":41,"adjDodge":41,"adjFatal":26,"adjAntiFatal":22,"adjMortal":0.124,"adjAntiMortal":0.024})
    }),
    51000037: _tools.RODict({
        "propID": 51000037,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1398,"adjMinPhysicalAtk":242,"adjMaxPhysicalAtk":532,"adjMinMagicAtk":242,"adjMaxMagicAtk":532,"adjMinPhysicalArmor":218,"adjMaxPhysicalArmor":328,"adjMinMagicArmor":218,"adjMaxMagicArmor":328,"adjHit":42,"adjDodge":43,"adjFatal":26,"adjAntiFatal":23,"adjMortal":0.127,"adjAntiMortal":0.027})
    }),
    51000038: _tools.RODict({
        "propID": 51000038,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1405,"adjMinPhysicalAtk":243,"adjMaxPhysicalAtk":535,"adjMinMagicAtk":243,"adjMaxMagicAtk":535,"adjMinPhysicalArmor":219,"adjMaxPhysicalArmor":329,"adjMinMagicArmor":219,"adjMaxMagicArmor":329,"adjHit":42,"adjDodge":43,"adjFatal":26,"adjAntiFatal":23,"adjMortal":0.127,"adjAntiMortal":0.027})
    }),
    51000039: _tools.RODict({
        "propID": 51000039,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1515,"adjMinPhysicalAtk":255,"adjMaxPhysicalAtk":561,"adjMinMagicAtk":255,"adjMaxMagicAtk":561,"adjMinPhysicalArmor":228,"adjMaxPhysicalArmor":342,"adjMinMagicArmor":228,"adjMaxMagicArmor":342,"adjHit":45,"adjDodge":46,"adjFatal":26,"adjAntiFatal":24,"adjMortal":0.13,"adjAntiMortal":0.03})
    }),
    51000040: _tools.RODict({
        "propID": 51000040,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1525,"adjMinPhysicalAtk":256,"adjMaxPhysicalAtk":563,"adjMinMagicAtk":256,"adjMaxMagicAtk":563,"adjMinPhysicalArmor":228,"adjMaxPhysicalArmor":343,"adjMinMagicArmor":228,"adjMaxMagicArmor":343,"adjHit":45,"adjDodge":46,"adjFatal":26,"adjAntiFatal":24,"adjMortal":0.13,"adjAntiMortal":0.03})
    }),
    51000041: _tools.RODict({
        "propID": 51000041,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1578,"adjMinPhysicalAtk":258,"adjMaxPhysicalAtk":568,"adjMinMagicAtk":258,"adjMaxMagicAtk":568,"adjMinPhysicalArmor":230,"adjMaxPhysicalArmor":345,"adjMinMagicArmor":230,"adjMaxMagicArmor":345,"adjHit":46,"adjDodge":47,"adjFatal":28,"adjAntiFatal":24,"adjMortal":0.133,"adjAntiMortal":0.033})
    }),
    51000042: _tools.RODict({
        "propID": 51000042,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1587,"adjMinPhysicalAtk":261,"adjMaxPhysicalAtk":576,"adjMinMagicAtk":261,"adjMaxMagicAtk":576,"adjMinPhysicalArmor":233,"adjMaxPhysicalArmor":350,"adjMinMagicArmor":233,"adjMaxMagicArmor":350,"adjHit":46,"adjDodge":47,"adjFatal":28,"adjAntiFatal":24,"adjMortal":0.133,"adjAntiMortal":0.033})
    }),
    51000043: _tools.RODict({
        "propID": 51000043,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1608,"adjMinPhysicalAtk":263,"adjMaxPhysicalAtk":579,"adjMinMagicAtk":263,"adjMaxMagicAtk":579,"adjMinPhysicalArmor":234,"adjMaxPhysicalArmor":351,"adjMinMagicArmor":234,"adjMaxMagicArmor":351,"adjHit":47,"adjDodge":48,"adjFatal":28,"adjAntiFatal":24,"adjMortal":0.136,"adjAntiMortal":0.036})
    }),
    51000044: _tools.RODict({
        "propID": 51000044,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1618,"adjMinPhysicalAtk":263,"adjMaxPhysicalAtk":580,"adjMinMagicAtk":263,"adjMaxMagicAtk":580,"adjMinPhysicalArmor":234,"adjMaxPhysicalArmor":352,"adjMinMagicArmor":234,"adjMaxMagicArmor":352,"adjHit":47,"adjDodge":48,"adjFatal":28,"adjAntiFatal":24,"adjMortal":0.136,"adjAntiMortal":0.036})
    }),
    51000045: _tools.RODict({
        "propID": 51000045,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1668,"adjMinPhysicalAtk":270,"adjMaxPhysicalAtk":595,"adjMinMagicAtk":270,"adjMaxMagicAtk":595,"adjMinPhysicalArmor":238,"adjMaxPhysicalArmor":358,"adjMinMagicArmor":238,"adjMaxMagicArmor":358,"adjHit":49,"adjDodge":50,"adjFatal":29,"adjAntiFatal":25,"adjMortal":0.139,"adjAntiMortal":0.039})
    }),
    51000046: _tools.RODict({
        "propID": 51000046,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1683,"adjMinPhysicalAtk":272,"adjMaxPhysicalAtk":600,"adjMinMagicAtk":272,"adjMaxMagicAtk":600,"adjMinPhysicalArmor":240,"adjMaxPhysicalArmor":360,"adjMinMagicArmor":240,"adjMaxMagicArmor":360,"adjHit":54,"adjDodge":55,"adjFatal":34,"adjAntiFatal":30,"adjMortal":0.149,"adjAntiMortal":0.049})
    }),
    51000047: _tools.RODict({
        "propID": 51000047,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1780,"adjMinPhysicalAtk":278,"adjMaxPhysicalAtk":612,"adjMinMagicAtk":278,"adjMaxMagicAtk":612,"adjMinPhysicalArmor":242,"adjMaxPhysicalArmor":364,"adjMinMagicArmor":242,"adjMaxMagicArmor":364,"adjHit":57,"adjDodge":57,"adjFatal":35,"adjAntiFatal":30,"adjMortal":0.152,"adjAntiMortal":0.052})
    }),
    51000048: _tools.RODict({
        "propID": 51000048,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1857,"adjMinPhysicalAtk":290,"adjMaxPhysicalAtk":638,"adjMinMagicAtk":290,"adjMaxMagicAtk":638,"adjMinPhysicalArmor":250,"adjMaxPhysicalArmor":375,"adjMinMagicArmor":250,"adjMaxMagicArmor":375,"adjHit":59,"adjDodge":59,"adjFatal":36,"adjAntiFatal":31,"adjMortal":0.152,"adjAntiMortal":0.052})
    }),
    51000049: _tools.RODict({
        "propID": 51000049,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1883,"adjMinPhysicalAtk":291,"adjMaxPhysicalAtk":640,"adjMinMagicAtk":291,"adjMaxMagicAtk":640,"adjMinPhysicalArmor":250,"adjMaxPhysicalArmor":376,"adjMinMagicArmor":250,"adjMaxMagicArmor":376,"adjHit":60,"adjDodge":60,"adjFatal":36,"adjAntiFatal":31,"adjMortal":0.155,"adjAntiMortal":0.055})
    }),
    51000050: _tools.RODict({
        "propID": 51000050,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1885,"adjMinPhysicalAtk":292,"adjMaxPhysicalAtk":643,"adjMinMagicAtk":292,"adjMaxMagicAtk":643,"adjMinPhysicalArmor":252,"adjMaxPhysicalArmor":378,"adjMinMagicArmor":252,"adjMaxMagicArmor":378,"adjHit":60,"adjDodge":60,"adjFatal":36,"adjAntiFatal":31,"adjMortal":0.155,"adjAntiMortal":0.055})
    }),
    51000051: _tools.RODict({
        "propID": 51000051,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2104,"adjMinPhysicalAtk":326,"adjMaxPhysicalAtk":718,"adjMinMagicAtk":326,"adjMaxMagicAtk":718,"adjMinPhysicalArmor":280,"adjMaxPhysicalArmor":420,"adjMinMagicArmor":280,"adjMaxMagicArmor":420,"adjHit":64,"adjDodge":64,"adjFatal":38,"adjAntiFatal":33,"adjMortal":0.158,"adjAntiMortal":0.058})
    }),
    51000052: _tools.RODict({
        "propID": 51000052,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2211,"adjMinPhysicalAtk":339,"adjMaxPhysicalAtk":747,"adjMinMagicAtk":339,"adjMaxMagicAtk":747,"adjMinPhysicalArmor":287,"adjMaxPhysicalArmor":431,"adjMinMagicArmor":287,"adjMaxMagicArmor":431,"adjHit":66,"adjDodge":66,"adjFatal":39,"adjAntiFatal":34,"adjMortal":0.158,"adjAntiMortal":0.058})
    }),
    51000053: _tools.RODict({
        "propID": 51000053,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2356,"adjMinPhysicalAtk":363,"adjMaxPhysicalAtk":798,"adjMinMagicAtk":363,"adjMaxMagicAtk":798,"adjMinPhysicalArmor":308,"adjMaxPhysicalArmor":462,"adjMinMagicArmor":308,"adjMaxMagicArmor":462,"adjHit":69,"adjDodge":68,"adjFatal":41,"adjAntiFatal":35,"adjMortal":0.161,"adjAntiMortal":0.061})
    }),
    51000054: _tools.RODict({
        "propID": 51000054,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2397,"adjMinPhysicalAtk":365,"adjMaxPhysicalAtk":804,"adjMinMagicAtk":365,"adjMaxMagicAtk":804,"adjMinPhysicalArmor":308,"adjMaxPhysicalArmor":463,"adjMinMagicArmor":308,"adjMaxMagicArmor":463,"adjHit":69,"adjDodge":68,"adjFatal":41,"adjAntiFatal":35,"adjMortal":0.161,"adjAntiMortal":0.061})
    }),
    51000055: _tools.RODict({
        "propID": 51000055,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2493,"adjMinPhysicalAtk":367,"adjMaxPhysicalAtk":807,"adjMinMagicAtk":367,"adjMaxMagicAtk":807,"adjMinPhysicalArmor":309,"adjMaxPhysicalArmor":464,"adjMinMagicArmor":309,"adjMaxMagicArmor":464,"adjHit":70,"adjDodge":69,"adjFatal":41,"adjAntiFatal":35,"adjMortal":0.164,"adjAntiMortal":0.064})
    }),
    51000056: _tools.RODict({
        "propID": 51000056,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2562,"adjMinPhysicalAtk":382,"adjMaxPhysicalAtk":842,"adjMinMagicAtk":382,"adjMaxMagicAtk":842,"adjMinPhysicalArmor":319,"adjMaxPhysicalArmor":479,"adjMinMagicArmor":319,"adjMaxMagicArmor":479,"adjHit":72,"adjDodge":72,"adjFatal":42,"adjAntiFatal":37,"adjMortal":0.164,"adjAntiMortal":0.064})
    }),
    51000057: _tools.RODict({
        "propID": 51000057,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2728,"adjMinPhysicalAtk":413,"adjMaxPhysicalAtk":908,"adjMinMagicAtk":413,"adjMaxMagicAtk":908,"adjMinPhysicalArmor":347,"adjMaxPhysicalArmor":521,"adjMinMagicArmor":347,"adjMaxMagicArmor":521,"adjHit":75,"adjDodge":74,"adjFatal":44,"adjAntiFatal":39,"adjMortal":0.167,"adjAntiMortal":0.067})
    }),
    51000058: _tools.RODict({
        "propID": 51000058,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2760,"adjMinPhysicalAtk":414,"adjMaxPhysicalAtk":911,"adjMinMagicAtk":414,"adjMaxMagicAtk":911,"adjMinPhysicalArmor":348,"adjMaxPhysicalArmor":522,"adjMinMagicArmor":348,"adjMaxMagicArmor":522,"adjHit":75,"adjDodge":74,"adjFatal":45,"adjAntiFatal":39,"adjMortal":0.167,"adjAntiMortal":0.067})
    }),
    51000059: _tools.RODict({
        "propID": 51000059,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2793,"adjMinPhysicalAtk":416,"adjMaxPhysicalAtk":916,"adjMinMagicAtk":416,"adjMaxMagicAtk":916,"adjMinPhysicalArmor":348,"adjMaxPhysicalArmor":523,"adjMinMagicArmor":348,"adjMaxMagicArmor":523,"adjHit":76,"adjDodge":75,"adjFatal":45,"adjAntiFatal":39,"adjMortal":0.17,"adjAntiMortal":0.07})
    }),
    51000060: _tools.RODict({
        "propID": 51000060,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3303,"adjMinPhysicalAtk":455,"adjMaxPhysicalAtk":1001,"adjMinMagicAtk":455,"adjMaxMagicAtk":1001,"adjMinPhysicalArmor":376,"adjMaxPhysicalArmor":564,"adjMinMagicArmor":376,"adjMaxMagicArmor":564,"adjHit":79,"adjDodge":79,"adjFatal":49,"adjAntiFatal":42,"adjMortal":0.27,"adjAntiMortal":0.07})
    }),
    51000061: _tools.RODict({
        "propID": 51000061,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3334,"adjMinPhysicalAtk":457,"adjMaxPhysicalAtk":1005,"adjMinMagicAtk":457,"adjMaxMagicAtk":1005,"adjMinPhysicalArmor":377,"adjMaxPhysicalArmor":566,"adjMinMagicArmor":377,"adjMaxMagicArmor":566,"adjHit":80,"adjDodge":80,"adjFatal":49,"adjAntiFatal":42,"adjMortal":0.273,"adjAntiMortal":0.073})
    }),
    51000062: _tools.RODict({
        "propID": 51000062,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3344,"adjMinPhysicalAtk":457,"adjMaxPhysicalAtk":1007,"adjMinMagicAtk":457,"adjMaxMagicAtk":1007,"adjMinPhysicalArmor":378,"adjMaxPhysicalArmor":567,"adjMinMagicArmor":378,"adjMaxMagicArmor":567,"adjHit":80,"adjDodge":80,"adjFatal":49,"adjAntiFatal":42,"adjMortal":0.273,"adjAntiMortal":0.073})
    }),
    51000063: _tools.RODict({
        "propID": 51000063,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3414,"adjMinPhysicalAtk":464,"adjMaxPhysicalAtk":1021,"adjMinMagicAtk":464,"adjMaxMagicAtk":1021,"adjMinPhysicalArmor":382,"adjMaxPhysicalArmor":573,"adjMinMagicArmor":382,"adjMaxMagicArmor":573,"adjHit":82,"adjDodge":82,"adjFatal":49,"adjAntiFatal":42,"adjMortal":0.276,"adjAntiMortal":0.076})
    }),
    51000064: _tools.RODict({
        "propID": 51000064,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3520,"adjMinPhysicalAtk":479,"adjMaxPhysicalAtk":1054,"adjMinMagicAtk":479,"adjMaxMagicAtk":1054,"adjMinPhysicalArmor":389,"adjMaxPhysicalArmor":584,"adjMinMagicArmor":389,"adjMaxMagicArmor":584,"adjHit":84,"adjDodge":84,"adjFatal":50,"adjAntiFatal":43,"adjMortal":0.276,"adjAntiMortal":0.076})
    }),
    51000065: _tools.RODict({
        "propID": 51000065,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3556,"adjMinPhysicalAtk":482,"adjMaxPhysicalAtk":1060,"adjMinMagicAtk":482,"adjMaxMagicAtk":1060,"adjMinPhysicalArmor":390,"adjMaxPhysicalArmor":585,"adjMinMagicArmor":390,"adjMaxMagicArmor":585,"adjHit":85,"adjDodge":85,"adjFatal":50,"adjAntiFatal":43,"adjMortal":0.279,"adjAntiMortal":0.079})
    }),
    51000066: _tools.RODict({
        "propID": 51000066,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3562,"adjMinPhysicalAtk":483,"adjMaxPhysicalAtk":1064,"adjMinMagicAtk":483,"adjMaxMagicAtk":1064,"adjMinPhysicalArmor":391,"adjMaxPhysicalArmor":587,"adjMinMagicArmor":391,"adjMaxMagicArmor":587,"adjHit":85,"adjDodge":85,"adjFatal":50,"adjAntiFatal":43,"adjMortal":0.279,"adjAntiMortal":0.079})
    }),
    51000067: _tools.RODict({
        "propID": 51000067,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3599,"adjMinPhysicalAtk":484,"adjMaxPhysicalAtk":1066,"adjMinMagicAtk":484,"adjMaxMagicAtk":1066,"adjMinPhysicalArmor":392,"adjMaxPhysicalArmor":588,"adjMinMagicArmor":392,"adjMaxMagicArmor":588,"adjHit":86,"adjDodge":86,"adjFatal":50,"adjAntiFatal":43,"adjMortal":0.282,"adjAntiMortal":0.082})
    }),
    51000068: _tools.RODict({
        "propID": 51000068,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3612,"adjMinPhysicalAtk":485,"adjMaxPhysicalAtk":1069,"adjMinMagicAtk":485,"adjMaxMagicAtk":1069,"adjMinPhysicalArmor":392,"adjMaxPhysicalArmor":589,"adjMinMagicArmor":392,"adjMaxMagicArmor":589,"adjHit":86,"adjDodge":86,"adjFatal":50,"adjAntiFatal":43,"adjMortal":0.282,"adjAntiMortal":0.082})
    }),
    51000069: _tools.RODict({
        "propID": 51000069,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3678,"adjMinPhysicalAtk":492,"adjMaxPhysicalAtk":1083,"adjMinMagicAtk":492,"adjMaxMagicAtk":1083,"adjMinPhysicalArmor":397,"adjMaxPhysicalArmor":596,"adjMinMagicArmor":397,"adjMaxMagicArmor":596,"adjHit":87,"adjDodge":87,"adjFatal":51,"adjAntiFatal":44,"adjMortal":0.285,"adjAntiMortal":0.085})
    }),
    51000070: _tools.RODict({
        "propID": 51000070,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3688,"adjMinPhysicalAtk":493,"adjMaxPhysicalAtk":1085,"adjMinMagicAtk":493,"adjMaxMagicAtk":1085,"adjMinPhysicalArmor":398,"adjMaxPhysicalArmor":597,"adjMinMagicArmor":398,"adjMaxMagicArmor":597,"adjHit":87,"adjDodge":87,"adjFatal":51,"adjAntiFatal":44,"adjMortal":0.285,"adjAntiMortal":0.085})
    }),
    52004001: _tools.RODict({
        "propID": 52004001,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":718200})
    }),
    52004002: _tools.RODict({
        "propID": 52004002,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":825900})
    }),
    52004003: _tools.RODict({
        "propID": 52004003,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":949800})
    }),
    52004004: _tools.RODict({
        "propID": 52004004,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1092300})
    }),
    52004005: _tools.RODict({
        "propID": 52004005,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1256100})
    }),
    52004006: _tools.RODict({
        "propID": 52004006,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1444500})
    }),
    52004007: _tools.RODict({
        "propID": 52004007,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1661200})
    }),
    52005001: _tools.RODict({
        "propID": 52005001,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":247680})
    }),
    52005002: _tools.RODict({
        "propID": 52005002,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":288000})
    }),
    52005003: _tools.RODict({
        "propID": 52005003,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":328000})
    }),
    52005004: _tools.RODict({
        "propID": 52005004,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":368000})
    }),
    52005005: _tools.RODict({
        "propID": 52005005,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":408000})
    }),
    52005006: _tools.RODict({
        "propID": 52005006,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":448000})
    }),
    52005007: _tools.RODict({
        "propID": 52005007,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":488000})
    }),
    52006001: _tools.RODict({
        "propID": 52006001,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":12384})
    }),
    52006002: _tools.RODict({
        "propID": 52006002,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":14200})
    }),
    52006003: _tools.RODict({
        "propID": 52006003,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":16300})
    }),
    52006004: _tools.RODict({
        "propID": 52006004,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":18700})
    }),
    52006005: _tools.RODict({
        "propID": 52006005,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":21500})
    }),
    52006006: _tools.RODict({
        "propID": 52006006,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":24700})
    }),
    52006007: _tools.RODict({
        "propID": 52006007,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":28400})
    }),
    52007001: _tools.RODict({
        "propID": 52007001,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":73000})
    }),
    52007002: _tools.RODict({
        "propID": 52007002,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":84000})
    }),
    52007003: _tools.RODict({
        "propID": 52007003,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":96600})
    }),
    52007004: _tools.RODict({
        "propID": 52007004,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":111100})
    }),
    52007005: _tools.RODict({
        "propID": 52007005,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":127800})
    }),
    52007006: _tools.RODict({
        "propID": 52007006,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":147000})
    }),
    52007007: _tools.RODict({
        "propID": 52007007,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":169100})
    }),
    52008001: _tools.RODict({
        "propID": 52008001,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2100,"adjMinPhysicalAtk":70,"adjMaxPhysicalAtk":70,"adjMinMagicAtk":70,"adjMaxMagicAtk":70})
    }),
    52008002: _tools.RODict({
        "propID": 52008002,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2700,"adjMinPhysicalAtk":82,"adjMaxPhysicalAtk":82,"adjMinMagicAtk":82,"adjMaxMagicAtk":82})
    }),
    52008003: _tools.RODict({
        "propID": 52008003,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3300,"adjMinPhysicalAtk":94,"adjMaxPhysicalAtk":94,"adjMinMagicAtk":94,"adjMaxMagicAtk":94})
    }),
    52008004: _tools.RODict({
        "propID": 52008004,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3900,"adjMinPhysicalAtk":106,"adjMaxPhysicalAtk":106,"adjMinMagicAtk":106,"adjMaxMagicAtk":106})
    }),
    52008005: _tools.RODict({
        "propID": 52008005,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4500,"adjMinPhysicalAtk":118,"adjMaxPhysicalAtk":118,"adjMinMagicAtk":118,"adjMaxMagicAtk":118})
    }),
    52008006: _tools.RODict({
        "propID": 52008006,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5100,"adjMinPhysicalAtk":130,"adjMaxPhysicalAtk":130,"adjMinMagicAtk":130,"adjMaxMagicAtk":130})
    }),
    52008007: _tools.RODict({
        "propID": 52008007,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5700,"adjMinPhysicalAtk":142,"adjMaxPhysicalAtk":142,"adjMinMagicAtk":142,"adjMaxMagicAtk":142})
    }),
    52009001: _tools.RODict({
        "propID": 52009001,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":200,"adjMinPhysicalAtk":4,"adjMaxPhysicalAtk":6,"adjMinMagicAtk":4,"adjMaxMagicAtk":6,"adjMinPhysicalArmor":2,"adjMaxPhysicalArmor":2,"adjMinMagicArmor":2,"adjMaxMagicArmor":2,"adjHit":68,"adjDodge":6,"adjRealDmgDef":2})
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
        "propList": _tools.RODict({"adjFullHp":872})
    }),
    52014263: _tools.RODict({
        "propID": 52014263,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":959})
    }),
    52014264: _tools.RODict({
        "propID": 52014264,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1046})
    }),
    52014265: _tools.RODict({
        "propID": 52014265,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1134})
    }),
    52014266: _tools.RODict({
        "propID": 52014266,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1221,"adjDrugsQuantity":1,"adjFinalDmg":0.02})
    }),
    52014267: _tools.RODict({
        "propID": 52014267,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1343,"adjDrugsQuantity":1,"adjFinalDmg":0.02})
    }),
    52014268: _tools.RODict({
        "propID": 52014268,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1465,"adjDrugsQuantity":2,"adjFinalDmg":0.02})
    }),
    52014269: _tools.RODict({
        "propID": 52014269,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1587,"adjDrugsQuantity":2,"adjFinalDmg":0.02})
    }),
    52014270: _tools.RODict({
        "propID": 52014270,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1709,"adjDrugsQuantity":3,"adjFinalDmg":0.04})
    }),
    52014271: _tools.RODict({
        "propID": 52014271,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1880,"adjDrugsQuantity":3,"adjFinalDmg":0.04})
    }),
    52014272: _tools.RODict({
        "propID": 52014272,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2051,"adjDrugsQuantity":4,"adjFinalDmg":0.04})
    }),
    52014273: _tools.RODict({
        "propID": 52014273,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2222,"adjDrugsQuantity":4,"adjFinalDmg":0.04})
    }),
    52014274: _tools.RODict({
        "propID": 52014274,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2555,"adjDrugsQuantity":5,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014275: _tools.RODict({
        "propID": 52014275,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2811,"adjDrugsQuantity":5,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014276: _tools.RODict({
        "propID": 52014276,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3092,"adjDrugsQuantity":6,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014277: _tools.RODict({
        "propID": 52014277,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3401,"adjDrugsQuantity":6,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    })
})
minKey = 51000001
maxKey = 52014277