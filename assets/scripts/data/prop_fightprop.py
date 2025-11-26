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
    52003001: _tools.RODict({
        "propID": 52003001,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmg":0.01})
    }),
    52003002: _tools.RODict({
        "propID": 52003002,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.01})
    }),
    52003003: _tools.RODict({
        "propID": 52003003,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1})
    }),
    52003004: _tools.RODict({
        "propID": 52003004,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmg":0.01})
    }),
    52003005: _tools.RODict({
        "propID": 52003005,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.01})
    }),
    52003006: _tools.RODict({
        "propID": 52003006,
        "type": 2,
        "propList": _tools.RODict({})
    }),
    52003007: _tools.RODict({
        "propID": 52003007,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmg":0.01})
    }),
    52003008: _tools.RODict({
        "propID": 52003008,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.01})
    }),
    52003009: _tools.RODict({
        "propID": 52003009,
        "type": 2,
        "propList": _tools.RODict({"mulMaxPhysicalAtk":0.01})
    }),
    52003010: _tools.RODict({
        "propID": 52003010,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmg":0.01})
    }),
    52003011: _tools.RODict({
        "propID": 52003011,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.01})
    }),
    52003012: _tools.RODict({
        "propID": 52003012,
        "type": 2,
        "propList": _tools.RODict({"mulMaxMagicAtk":0.01})
    }),
    52003013: _tools.RODict({
        "propID": 52003013,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmg":0.01})
    }),
    52003014: _tools.RODict({
        "propID": 52003014,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.01})
    }),
    52003015: _tools.RODict({
        "propID": 52003015,
        "type": 2,
        "propList": _tools.RODict({"adjFatal":5})
    }),
    52003016: _tools.RODict({
        "propID": 52003016,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmg":0.01})
    }),
    52003017: _tools.RODict({
        "propID": 52003017,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.01})
    }),
    52003018: _tools.RODict({
        "propID": 52003018,
        "type": 2,
        "propList": _tools.RODict({"mulMaxPhysicalAtk":0.01})
    }),
    52003019: _tools.RODict({
        "propID": 52003019,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmg":0.01})
    }),
    52003020: _tools.RODict({
        "propID": 52003020,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.01})
    }),
    52003021: _tools.RODict({
        "propID": 52003021,
        "type": 2,
        "propList": _tools.RODict({"mulMaxMagicAtk":0.01})
    }),
    52003022: _tools.RODict({
        "propID": 52003022,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmg":0.01})
    }),
    52003023: _tools.RODict({
        "propID": 52003023,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.01})
    }),
    52003024: _tools.RODict({
        "propID": 52003024,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1})
    }),
    52003025: _tools.RODict({
        "propID": 52003025,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmg":0.01})
    }),
    52003026: _tools.RODict({
        "propID": 52003026,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.01})
    }),
    52003027: _tools.RODict({
        "propID": 52003027,
        "type": 2,
        "propList": _tools.RODict({})
    }),
    52003028: _tools.RODict({
        "propID": 52003028,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmg":0.01})
    }),
    52003029: _tools.RODict({
        "propID": 52003029,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.01})
    }),
    52003030: _tools.RODict({
        "propID": 52003030,
        "type": 2,
        "propList": _tools.RODict({"mulMaxPhysicalAtk":0.01})
    }),
    52003031: _tools.RODict({
        "propID": 52003031,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmg":0.01})
    }),
    52003032: _tools.RODict({
        "propID": 52003032,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.01})
    }),
    52003033: _tools.RODict({
        "propID": 52003033,
        "type": 2,
        "propList": _tools.RODict({"mulMaxMagicAtk":0.01})
    }),
    52003034: _tools.RODict({
        "propID": 52003034,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmg":0.01})
    }),
    52003035: _tools.RODict({
        "propID": 52003035,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.01})
    }),
    52003036: _tools.RODict({
        "propID": 52003036,
        "type": 2,
        "propList": _tools.RODict({"adjFatal":5})
    }),
    52003037: _tools.RODict({
        "propID": 52003037,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmg":0.01})
    }),
    52003038: _tools.RODict({
        "propID": 52003038,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.01})
    }),
    52003039: _tools.RODict({
        "propID": 52003039,
        "type": 2,
        "propList": _tools.RODict({"mulMaxPhysicalAtk":0.01})
    }),
    52003040: _tools.RODict({
        "propID": 52003040,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmg":0.01})
    }),
    52003041: _tools.RODict({
        "propID": 52003041,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.01})
    }),
    52003042: _tools.RODict({
        "propID": 52003042,
        "type": 2,
        "propList": _tools.RODict({"mulMaxMagicAtk":0.01})
    }),
    52003043: _tools.RODict({
        "propID": 52003043,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmg":0.01})
    }),
    52003044: _tools.RODict({
        "propID": 52003044,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.01})
    }),
    52003045: _tools.RODict({
        "propID": 52003045,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1})
    }),
    52003046: _tools.RODict({
        "propID": 52003046,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmg":0.01})
    }),
    52003047: _tools.RODict({
        "propID": 52003047,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.01})
    }),
    52003048: _tools.RODict({
        "propID": 52003048,
        "type": 2,
        "propList": _tools.RODict({})
    }),
    52003049: _tools.RODict({
        "propID": 52003049,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmg":0.01})
    }),
    52003050: _tools.RODict({
        "propID": 52003050,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.01})
    }),
    52003051: _tools.RODict({
        "propID": 52003051,
        "type": 2,
        "propList": _tools.RODict({"mulMaxPhysicalAtk":0.02})
    }),
    52003052: _tools.RODict({
        "propID": 52003052,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmg":0.01})
    }),
    52003053: _tools.RODict({
        "propID": 52003053,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.01})
    }),
    52003054: _tools.RODict({
        "propID": 52003054,
        "type": 2,
        "propList": _tools.RODict({"mulMaxMagicAtk":0.02})
    }),
    52003055: _tools.RODict({
        "propID": 52003055,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmg":0.01})
    }),
    52003056: _tools.RODict({
        "propID": 52003056,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.01})
    }),
    52003057: _tools.RODict({
        "propID": 52003057,
        "type": 2,
        "propList": _tools.RODict({"adjFatal":10})
    }),
    52003058: _tools.RODict({
        "propID": 52003058,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmg":0.01})
    }),
    52003059: _tools.RODict({
        "propID": 52003059,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.01})
    }),
    52003060: _tools.RODict({
        "propID": 52003060,
        "type": 2,
        "propList": _tools.RODict({"adjIgnoreArmor":0.03})
    }),
    52003061: _tools.RODict({
        "propID": 52003061,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmg":0.01})
    }),
    52003062: _tools.RODict({
        "propID": 52003062,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.01})
    }),
    52003063: _tools.RODict({
        "propID": 52003063,
        "type": 2,
        "propList": _tools.RODict({})
    }),
    52003064: _tools.RODict({
        "propID": 52003064,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmg":0.01})
    }),
    52003065: _tools.RODict({
        "propID": 52003065,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.01})
    }),
    52003066: _tools.RODict({
        "propID": 52003066,
        "type": 2,
        "propList": _tools.RODict({"adjStunAnti":5})
    }),
    52003067: _tools.RODict({
        "propID": 52003067,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmg":0.01})
    }),
    52003068: _tools.RODict({
        "propID": 52003068,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.01})
    }),
    52003069: _tools.RODict({
        "propID": 52003069,
        "type": 2,
        "propList": _tools.RODict({"adjSilentEnh":5})
    }),
    52003070: _tools.RODict({
        "propID": 52003070,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmg":0.01})
    }),
    52003071: _tools.RODict({
        "propID": 52003071,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.01})
    }),
    52003072: _tools.RODict({
        "propID": 52003072,
        "type": 2,
        "propList": _tools.RODict({"adjFrozenAnti":5})
    }),
    52003073: _tools.RODict({
        "propID": 52003073,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmg":0.01})
    }),
    52003074: _tools.RODict({
        "propID": 52003074,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.01})
    }),
    52003075: _tools.RODict({
        "propID": 52003075,
        "type": 2,
        "propList": _tools.RODict({"adjAntiFatal":5})
    }),
    52003076: _tools.RODict({
        "propID": 52003076,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmg":0.01})
    }),
    52003077: _tools.RODict({
        "propID": 52003077,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.01})
    }),
    52003078: _tools.RODict({
        "propID": 52003078,
        "type": 2,
        "propList": _tools.RODict({"adjKnockAnti":5})
    }),
    52003079: _tools.RODict({
        "propID": 52003079,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmg":0.01})
    }),
    52003080: _tools.RODict({
        "propID": 52003080,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.01})
    }),
    52003081: _tools.RODict({
        "propID": 52003081,
        "type": 2,
        "propList": _tools.RODict({})
    }),
    52003082: _tools.RODict({
        "propID": 52003082,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmg":0.01})
    }),
    52003083: _tools.RODict({
        "propID": 52003083,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.01})
    }),
    52003084: _tools.RODict({
        "propID": 52003084,
        "type": 2,
        "propList": _tools.RODict({"adjStunAnti":10})
    }),
    52003085: _tools.RODict({
        "propID": 52003085,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmg":0.01})
    }),
    52003086: _tools.RODict({
        "propID": 52003086,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.01})
    }),
    52003087: _tools.RODict({
        "propID": 52003087,
        "type": 2,
        "propList": _tools.RODict({"adjSilentEnh":10})
    }),
    52003088: _tools.RODict({
        "propID": 52003088,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmg":0.01})
    }),
    52003089: _tools.RODict({
        "propID": 52003089,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.01})
    }),
    52003090: _tools.RODict({
        "propID": 52003090,
        "type": 2,
        "propList": _tools.RODict({"adjFrozenAnti":10})
    }),
    52003091: _tools.RODict({
        "propID": 52003091,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmg":0.01})
    }),
    52003092: _tools.RODict({
        "propID": 52003092,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.01})
    }),
    52003093: _tools.RODict({
        "propID": 52003093,
        "type": 2,
        "propList": _tools.RODict({"adjKnockAnti":10})
    }),
    52003094: _tools.RODict({
        "propID": 52003094,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmg":0.01})
    }),
    52003095: _tools.RODict({
        "propID": 52003095,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.01})
    }),
    52003096: _tools.RODict({
        "propID": 52003096,
        "type": 2,
        "propList": _tools.RODict({"adjAntiFatal":5})
    }),
    52003097: _tools.RODict({
        "propID": 52003097,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmg":0.01})
    }),
    52003098: _tools.RODict({
        "propID": 52003098,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.01})
    }),
    52003099: _tools.RODict({
        "propID": 52003099,
        "type": 2,
        "propList": _tools.RODict({})
    }),
    52003100: _tools.RODict({
        "propID": 52003100,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmg":0.01})
    }),
    52003101: _tools.RODict({
        "propID": 52003101,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.01})
    }),
    52003102: _tools.RODict({
        "propID": 52003102,
        "type": 2,
        "propList": _tools.RODict({"adjStunAnti":15})
    }),
    52003103: _tools.RODict({
        "propID": 52003103,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmg":0.01})
    }),
    52003104: _tools.RODict({
        "propID": 52003104,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.01})
    }),
    52003105: _tools.RODict({
        "propID": 52003105,
        "type": 2,
        "propList": _tools.RODict({"adjSilentEnh":15})
    }),
    52003106: _tools.RODict({
        "propID": 52003106,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmg":0.01})
    }),
    52003107: _tools.RODict({
        "propID": 52003107,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.01})
    }),
    52003108: _tools.RODict({
        "propID": 52003108,
        "type": 2,
        "propList": _tools.RODict({"adjFrozenAnti":15})
    }),
    52003109: _tools.RODict({
        "propID": 52003109,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmg":0.01})
    }),
    52003110: _tools.RODict({
        "propID": 52003110,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.01})
    }),
    52003111: _tools.RODict({
        "propID": 52003111,
        "type": 2,
        "propList": _tools.RODict({"adjKnockAnti":15})
    }),
    52003112: _tools.RODict({
        "propID": 52003112,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmg":0.01})
    }),
    52003113: _tools.RODict({
        "propID": 52003113,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.01})
    }),
    52003114: _tools.RODict({
        "propID": 52003114,
        "type": 2,
        "propList": _tools.RODict({"mulFullHp":0.02})
    }),
    52003115: _tools.RODict({
        "propID": 52003115,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmg":0.01})
    }),
    52003116: _tools.RODict({
        "propID": 52003116,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.01})
    }),
    52003117: _tools.RODict({
        "propID": 52003117,
        "type": 2,
        "propList": _tools.RODict({"adjAntiFatal":10})
    }),
    52003118: _tools.RODict({
        "propID": 52003118,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmg":0.01})
    }),
    52003119: _tools.RODict({
        "propID": 52003119,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.01})
    }),
    52003120: _tools.RODict({
        "propID": 52003120,
        "type": 2,
        "propList": _tools.RODict({"mulFullHp":0.03})
    }),
    52003121: _tools.RODict({
        "propID": 52003121,
        "type": 2,
        "propList": _tools.RODict({"adjCopper":0.01})
    }),
    52003122: _tools.RODict({
        "propID": 52003122,
        "type": 2,
        "propList": _tools.RODict({"adjExpGrow":0.01})
    }),
    52003123: _tools.RODict({
        "propID": 52003123,
        "type": 2,
        "propList": _tools.RODict({})
    }),
    52003124: _tools.RODict({
        "propID": 52003124,
        "type": 2,
        "propList": _tools.RODict({"adjCopper":0.01})
    }),
    52003125: _tools.RODict({
        "propID": 52003125,
        "type": 2,
        "propList": _tools.RODict({"adjExpGrow":0.01})
    }),
    52003126: _tools.RODict({
        "propID": 52003126,
        "type": 2,
        "propList": _tools.RODict({"adjMedicineRate":0.01})
    }),
    52003127: _tools.RODict({
        "propID": 52003127,
        "type": 2,
        "propList": _tools.RODict({"adjCopper":0.01})
    }),
    52003128: _tools.RODict({
        "propID": 52003128,
        "type": 2,
        "propList": _tools.RODict({"adjExpGrow":0.01})
    }),
    52003129: _tools.RODict({
        "propID": 52003129,
        "type": 2,
        "propList": _tools.RODict({"adjMiningRate":0.01})
    }),
    52003130: _tools.RODict({
        "propID": 52003130,
        "type": 2,
        "propList": _tools.RODict({"adjCopper":0.01})
    }),
    52003131: _tools.RODict({
        "propID": 52003131,
        "type": 2,
        "propList": _tools.RODict({"adjExpGrow":0.01})
    }),
    52003132: _tools.RODict({
        "propID": 52003132,
        "type": 2,
        "propList": _tools.RODict({})
    }),
    52003133: _tools.RODict({
        "propID": 52003133,
        "type": 2,
        "propList": _tools.RODict({"adjCopper":0.01})
    }),
    52003134: _tools.RODict({
        "propID": 52003134,
        "type": 2,
        "propList": _tools.RODict({"adjExpGrow":0.01})
    }),
    52003135: _tools.RODict({
        "propID": 52003135,
        "type": 2,
        "propList": _tools.RODict({})
    }),
    52003136: _tools.RODict({
        "propID": 52003136,
        "type": 2,
        "propList": _tools.RODict({"adjCopper":0.01})
    }),
    52003137: _tools.RODict({
        "propID": 52003137,
        "type": 2,
        "propList": _tools.RODict({"adjExpGrow":0.01})
    }),
    52003138: _tools.RODict({
        "propID": 52003138,
        "type": 2,
        "propList": _tools.RODict({"adjMedicineRate":0.01})
    }),
    52003139: _tools.RODict({
        "propID": 52003139,
        "type": 2,
        "propList": _tools.RODict({"adjCopper":0.01})
    }),
    52003140: _tools.RODict({
        "propID": 52003140,
        "type": 2,
        "propList": _tools.RODict({"adjExpGrow":0.01})
    }),
    52003141: _tools.RODict({
        "propID": 52003141,
        "type": 2,
        "propList": _tools.RODict({"adjMiningRate":0.01})
    }),
    52003142: _tools.RODict({
        "propID": 52003142,
        "type": 2,
        "propList": _tools.RODict({"adjCopper":0.01})
    }),
    52003143: _tools.RODict({
        "propID": 52003143,
        "type": 2,
        "propList": _tools.RODict({"adjExpGrow":0.01})
    }),
    52003144: _tools.RODict({
        "propID": 52003144,
        "type": 2,
        "propList": _tools.RODict({})
    }),
    52003145: _tools.RODict({
        "propID": 52003145,
        "type": 2,
        "propList": _tools.RODict({"adjCopper":0.01})
    }),
    52003146: _tools.RODict({
        "propID": 52003146,
        "type": 2,
        "propList": _tools.RODict({"adjExpGrow":0.01})
    }),
    52003147: _tools.RODict({
        "propID": 52003147,
        "type": 2,
        "propList": _tools.RODict({})
    }),
    52003148: _tools.RODict({
        "propID": 52003148,
        "type": 2,
        "propList": _tools.RODict({"adjCopper":0.01})
    }),
    52003149: _tools.RODict({
        "propID": 52003149,
        "type": 2,
        "propList": _tools.RODict({"adjExpGrow":0.01})
    }),
    52003150: _tools.RODict({
        "propID": 52003150,
        "type": 2,
        "propList": _tools.RODict({"adjMedicineRate":0.01})
    }),
    52003151: _tools.RODict({
        "propID": 52003151,
        "type": 2,
        "propList": _tools.RODict({"adjCopper":0.01})
    }),
    52003152: _tools.RODict({
        "propID": 52003152,
        "type": 2,
        "propList": _tools.RODict({"adjExpGrow":0.01})
    }),
    52003153: _tools.RODict({
        "propID": 52003153,
        "type": 2,
        "propList": _tools.RODict({"adjMiningRate":0.01})
    }),
    52003154: _tools.RODict({
        "propID": 52003154,
        "type": 2,
        "propList": _tools.RODict({"adjCopper":0.01})
    }),
    52003155: _tools.RODict({
        "propID": 52003155,
        "type": 2,
        "propList": _tools.RODict({"adjExpGrow":0.01})
    }),
    52003156: _tools.RODict({
        "propID": 52003156,
        "type": 2,
        "propList": _tools.RODict({})
    }),
    52003157: _tools.RODict({
        "propID": 52003157,
        "type": 2,
        "propList": _tools.RODict({"adjCopper":0.01})
    }),
    52003158: _tools.RODict({
        "propID": 52003158,
        "type": 2,
        "propList": _tools.RODict({"adjExpGrow":0.01})
    }),
    52003159: _tools.RODict({
        "propID": 52003159,
        "type": 2,
        "propList": _tools.RODict({})
    }),
    52003160: _tools.RODict({
        "propID": 52003160,
        "type": 2,
        "propList": _tools.RODict({"adjCopper":0.01})
    }),
    52003161: _tools.RODict({
        "propID": 52003161,
        "type": 2,
        "propList": _tools.RODict({"adjExpGrow":0.01})
    }),
    52003162: _tools.RODict({
        "propID": 52003162,
        "type": 2,
        "propList": _tools.RODict({"adjMedicineRate":0.01})
    }),
    52003163: _tools.RODict({
        "propID": 52003163,
        "type": 2,
        "propList": _tools.RODict({"adjCopper":0.01})
    }),
    52003164: _tools.RODict({
        "propID": 52003164,
        "type": 2,
        "propList": _tools.RODict({"adjExpGrow":0.01})
    }),
    52003165: _tools.RODict({
        "propID": 52003165,
        "type": 2,
        "propList": _tools.RODict({"adjMiningRate":0.01})
    }),
    52003166: _tools.RODict({
        "propID": 52003166,
        "type": 2,
        "propList": _tools.RODict({"adjCopper":0.01})
    }),
    52003167: _tools.RODict({
        "propID": 52003167,
        "type": 2,
        "propList": _tools.RODict({"adjExpGrow":0.01})
    }),
    52003168: _tools.RODict({
        "propID": 52003168,
        "type": 2,
        "propList": _tools.RODict({})
    }),
    52003169: _tools.RODict({
        "propID": 52003169,
        "type": 2,
        "propList": _tools.RODict({"adjCopper":0.01})
    }),
    52003170: _tools.RODict({
        "propID": 52003170,
        "type": 2,
        "propList": _tools.RODict({"adjExpGrow":0.01})
    }),
    52003171: _tools.RODict({
        "propID": 52003171,
        "type": 2,
        "propList": _tools.RODict({})
    }),
    52003172: _tools.RODict({
        "propID": 52003172,
        "type": 2,
        "propList": _tools.RODict({"adjCopper":0.01})
    }),
    52003173: _tools.RODict({
        "propID": 52003173,
        "type": 2,
        "propList": _tools.RODict({"adjExpGrow":0.01})
    }),
    52003174: _tools.RODict({
        "propID": 52003174,
        "type": 2,
        "propList": _tools.RODict({"adjMedicineRate":0.01})
    }),
    52003175: _tools.RODict({
        "propID": 52003175,
        "type": 2,
        "propList": _tools.RODict({"adjCopper":0.01})
    }),
    52003176: _tools.RODict({
        "propID": 52003176,
        "type": 2,
        "propList": _tools.RODict({"adjExpGrow":0.01})
    }),
    52003177: _tools.RODict({
        "propID": 52003177,
        "type": 2,
        "propList": _tools.RODict({"adjMiningRate":0.01})
    }),
    52003178: _tools.RODict({
        "propID": 52003178,
        "type": 2,
        "propList": _tools.RODict({"adjCopper":0.01})
    }),
    52003179: _tools.RODict({
        "propID": 52003179,
        "type": 2,
        "propList": _tools.RODict({"adjExpGrow":0.01})
    }),
    52003180: _tools.RODict({
        "propID": 52003180,
        "type": 2,
        "propList": _tools.RODict({})
    }),
    52003181: _tools.RODict({
        "propID": 52003181,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmg":0.005})
    }),
    52003182: _tools.RODict({
        "propID": 52003182,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmg":0.008})
    }),
    52003183: _tools.RODict({
        "propID": 52003183,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmg":0.011})
    }),
    52003184: _tools.RODict({
        "propID": 52003184,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmg":0.014})
    }),
    52003185: _tools.RODict({
        "propID": 52003185,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.005})
    }),
    52003186: _tools.RODict({
        "propID": 52003186,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.008})
    }),
    52003187: _tools.RODict({
        "propID": 52003187,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.011})
    }),
    52003188: _tools.RODict({
        "propID": 52003188,
        "type": 2,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.014})
    }),
    52003189: _tools.RODict({
        "propID": 52003189,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmg":0.005})
    }),
    52003190: _tools.RODict({
        "propID": 52003190,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmg":0.008})
    }),
    52003191: _tools.RODict({
        "propID": 52003191,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmg":0.011})
    }),
    52003192: _tools.RODict({
        "propID": 52003192,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmg":0.014})
    }),
    52003193: _tools.RODict({
        "propID": 52003193,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.005})
    }),
    52003194: _tools.RODict({
        "propID": 52003194,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.008})
    }),
    52003195: _tools.RODict({
        "propID": 52003195,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.011})
    }),
    52003196: _tools.RODict({
        "propID": 52003196,
        "type": 2,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.014})
    }),
    52003197: _tools.RODict({
        "propID": 52003197,
        "type": 2,
        "propList": _tools.RODict({"adjCopper":0.005})
    }),
    52003198: _tools.RODict({
        "propID": 52003198,
        "type": 2,
        "propList": _tools.RODict({"adjCopper":0.008})
    }),
    52003199: _tools.RODict({
        "propID": 52003199,
        "type": 2,
        "propList": _tools.RODict({"adjCopper":0.011})
    }),
    52003200: _tools.RODict({
        "propID": 52003200,
        "type": 2,
        "propList": _tools.RODict({"adjCopper":0.014})
    }),
    52003201: _tools.RODict({
        "propID": 52003201,
        "type": 2,
        "propList": _tools.RODict({"adjExpGrow":0.005})
    }),
    52003202: _tools.RODict({
        "propID": 52003202,
        "type": 2,
        "propList": _tools.RODict({"adjExpGrow":0.008})
    }),
    52003203: _tools.RODict({
        "propID": 52003203,
        "type": 2,
        "propList": _tools.RODict({"adjExpGrow":0.011})
    }),
    52003204: _tools.RODict({
        "propID": 52003204,
        "type": 2,
        "propList": _tools.RODict({"adjExpGrow":0.014})
    }),
    52003205: _tools.RODict({
        "propID": 52003205,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5})
    }),
    52003206: _tools.RODict({
        "propID": 52003206,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":8})
    }),
    52003207: _tools.RODict({
        "propID": 52003207,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":11})
    }),
    52003208: _tools.RODict({
        "propID": 52003208,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":14})
    }),
    52003209: _tools.RODict({
        "propID": 52003209,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":2})
    }),
    52003210: _tools.RODict({
        "propID": 52003210,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":3})
    }),
    52003211: _tools.RODict({
        "propID": 52003211,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":1})
    }),
    52003212: _tools.RODict({
        "propID": 52003212,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":2})
    }),
    52003213: _tools.RODict({
        "propID": 52003213,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":1})
    }),
    52003214: _tools.RODict({
        "propID": 52003214,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":2})
    }),
    52003215: _tools.RODict({
        "propID": 52003215,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1})
    }),
    52003216: _tools.RODict({
        "propID": 52003216,
        "type": 2,
        "propList": _tools.RODict({"adjHit":1})
    }),
    52003217: _tools.RODict({
        "propID": 52003217,
        "type": 2,
        "propList": _tools.RODict({"adjHit":2})
    }),
    52003218: _tools.RODict({
        "propID": 52003218,
        "type": 2,
        "propList": _tools.RODict({"adjDodge":1})
    }),
    52003219: _tools.RODict({
        "propID": 52003219,
        "type": 2,
        "propList": _tools.RODict({"adjDodge":2})
    }),
    52003220: _tools.RODict({
        "propID": 52003220,
        "type": 2,
        "propList": _tools.RODict({})
    }),
    52003221: _tools.RODict({
        "propID": 52003221,
        "type": 2,
        "propList": _tools.RODict({})
    }),
    52003222: _tools.RODict({
        "propID": 52003222,
        "type": 2,
        "propList": _tools.RODict({})
    }),
    52003223: _tools.RODict({
        "propID": 52003223,
        "type": 2,
        "propList": _tools.RODict({})
    }),
    52003224: _tools.RODict({
        "propID": 52003224,
        "type": 2,
        "propList": _tools.RODict({})
    }),
    52003225: _tools.RODict({
        "propID": 52003225,
        "type": 2,
        "propList": _tools.RODict({})
    }),
    52003226: _tools.RODict({
        "propID": 52003226,
        "type": 2,
        "propList": _tools.RODict({})
    }),
    52003227: _tools.RODict({
        "propID": 52003227,
        "type": 2,
        "propList": _tools.RODict({})
    }),
    52003228: _tools.RODict({
        "propID": 52003228,
        "type": 2,
        "propList": _tools.RODict({"adjFatal":5})
    }),
    52003229: _tools.RODict({
        "propID": 52003229,
        "type": 2,
        "propList": _tools.RODict({"adjFatal":8})
    }),
    52003230: _tools.RODict({
        "propID": 52003230,
        "type": 2,
        "propList": _tools.RODict({"adjFatal":11})
    }),
    52003231: _tools.RODict({
        "propID": 52003231,
        "type": 2,
        "propList": _tools.RODict({"adjFatal":14})
    }),
    52003232: _tools.RODict({
        "propID": 52003232,
        "type": 2,
        "propList": _tools.RODict({"adjAntiFatal":5})
    }),
    52003233: _tools.RODict({
        "propID": 52003233,
        "type": 2,
        "propList": _tools.RODict({"adjAntiFatal":8})
    }),
    52003234: _tools.RODict({
        "propID": 52003234,
        "type": 2,
        "propList": _tools.RODict({"adjAntiFatal":11})
    }),
    52003235: _tools.RODict({
        "propID": 52003235,
        "type": 2,
        "propList": _tools.RODict({"adjAntiFatal":14})
    }),
    52003236: _tools.RODict({
        "propID": 52003236,
        "type": 2,
        "propList": _tools.RODict({"adjFinalDmg":0.03})
    }),
    52003237: _tools.RODict({
        "propID": 52003237,
        "type": 2,
        "propList": _tools.RODict({"adjFinalDmg":0.06})
    }),
    52003238: _tools.RODict({
        "propID": 52003238,
        "type": 2,
        "propList": _tools.RODict({"adjFinalDmgAnti":0.03})
    }),
    52003239: _tools.RODict({
        "propID": 52003239,
        "type": 2,
        "propList": _tools.RODict({"adjFinalDmgAnti":0.06})
    }),
    51004001: _tools.RODict({
        "propID": 51004001,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":718200})
    }),
    51004002: _tools.RODict({
        "propID": 51004002,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":825900})
    }),
    51004003: _tools.RODict({
        "propID": 51004003,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":949800})
    }),
    51004004: _tools.RODict({
        "propID": 51004004,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1092300})
    }),
    51004005: _tools.RODict({
        "propID": 51004005,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1256100})
    }),
    51004006: _tools.RODict({
        "propID": 51004006,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1444500})
    }),
    51004007: _tools.RODict({
        "propID": 51004007,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1661200})
    }),
    51005001: _tools.RODict({
        "propID": 51005001,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":247680})
    }),
    51005002: _tools.RODict({
        "propID": 51005002,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":288000})
    }),
    51005003: _tools.RODict({
        "propID": 51005003,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":328000})
    }),
    51005004: _tools.RODict({
        "propID": 51005004,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":368000})
    }),
    51005005: _tools.RODict({
        "propID": 51005005,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":408000})
    }),
    51005006: _tools.RODict({
        "propID": 51005006,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":448000})
    }),
    51005007: _tools.RODict({
        "propID": 51005007,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":488000})
    }),
    51006001: _tools.RODict({
        "propID": 51006001,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":12384})
    }),
    51006002: _tools.RODict({
        "propID": 51006002,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":14200})
    }),
    51006003: _tools.RODict({
        "propID": 51006003,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":16300})
    }),
    51006004: _tools.RODict({
        "propID": 51006004,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":18700})
    }),
    51006005: _tools.RODict({
        "propID": 51006005,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":21500})
    }),
    51006006: _tools.RODict({
        "propID": 51006006,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":24700})
    }),
    51006007: _tools.RODict({
        "propID": 51006007,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":28400})
    }),
    51007001: _tools.RODict({
        "propID": 51007001,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":73000})
    }),
    51007002: _tools.RODict({
        "propID": 51007002,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":84000})
    }),
    51007003: _tools.RODict({
        "propID": 51007003,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":96600})
    }),
    51007004: _tools.RODict({
        "propID": 51007004,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":111100})
    }),
    51007005: _tools.RODict({
        "propID": 51007005,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":127800})
    }),
    51007006: _tools.RODict({
        "propID": 51007006,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":147000})
    }),
    51007007: _tools.RODict({
        "propID": 51007007,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":169100})
    }),
    51008001: _tools.RODict({
        "propID": 51008001,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2100,"adjMinPhysicalAtk":70,"adjMaxPhysicalAtk":70,"adjMinMagicAtk":70,"adjMaxMagicAtk":70})
    }),
    51008002: _tools.RODict({
        "propID": 51008002,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2700,"adjMinPhysicalAtk":82,"adjMaxPhysicalAtk":82,"adjMinMagicAtk":82,"adjMaxMagicAtk":82})
    }),
    51008003: _tools.RODict({
        "propID": 51008003,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3300,"adjMinPhysicalAtk":94,"adjMaxPhysicalAtk":94,"adjMinMagicAtk":94,"adjMaxMagicAtk":94})
    }),
    51008004: _tools.RODict({
        "propID": 51008004,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3900,"adjMinPhysicalAtk":106,"adjMaxPhysicalAtk":106,"adjMinMagicAtk":106,"adjMaxMagicAtk":106})
    }),
    51008005: _tools.RODict({
        "propID": 51008005,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4500,"adjMinPhysicalAtk":118,"adjMaxPhysicalAtk":118,"adjMinMagicAtk":118,"adjMaxMagicAtk":118})
    }),
    51008006: _tools.RODict({
        "propID": 51008006,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5100,"adjMinPhysicalAtk":130,"adjMaxPhysicalAtk":130,"adjMinMagicAtk":130,"adjMaxMagicAtk":130})
    }),
    51008007: _tools.RODict({
        "propID": 51008007,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5700,"adjMinPhysicalAtk":142,"adjMaxPhysicalAtk":142,"adjMinMagicAtk":142,"adjMaxMagicAtk":142})
    }),
    51009001: _tools.RODict({
        "propID": 51009001,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":200,"adjMinPhysicalAtk":2,"adjMaxPhysicalAtk":3,"adjMinMagicAtk":2,"adjMaxMagicAtk":3,"adjMinPhysicalArmor":1,"adjMaxPhysicalArmor":1,"adjMinMagicArmor":1,"adjMaxMagicArmor":1,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009002: _tools.RODict({
        "propID": 51009002,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":210,"adjMinPhysicalAtk":8,"adjMaxPhysicalAtk":13,"adjMinMagicAtk":8,"adjMaxMagicAtk":13,"adjMinPhysicalArmor":1,"adjMaxPhysicalArmor":1,"adjMinMagicArmor":1,"adjMaxMagicArmor":1,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009003: _tools.RODict({
        "propID": 51009003,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":220,"adjMinPhysicalAtk":8,"adjMaxPhysicalAtk":13,"adjMinMagicAtk":8,"adjMaxMagicAtk":13,"adjMinPhysicalArmor":1,"adjMaxPhysicalArmor":1,"adjMinMagicArmor":1,"adjMaxMagicArmor":1,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009004: _tools.RODict({
        "propID": 51009004,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":278,"adjMinPhysicalAtk":8,"adjMaxPhysicalAtk":13,"adjMinMagicAtk":8,"adjMaxMagicAtk":13,"adjMinPhysicalArmor":3,"adjMaxPhysicalArmor":3,"adjMinMagicArmor":3,"adjMaxMagicArmor":3,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009005: _tools.RODict({
        "propID": 51009005,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":288,"adjMinPhysicalAtk":8,"adjMaxPhysicalAtk":14,"adjMinMagicAtk":8,"adjMaxMagicAtk":14,"adjMinPhysicalArmor":3,"adjMaxPhysicalArmor":3,"adjMinMagicArmor":3,"adjMaxMagicArmor":3,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009006: _tools.RODict({
        "propID": 51009006,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":378,"adjMinPhysicalAtk":8,"adjMaxPhysicalAtk":14,"adjMinMagicAtk":8,"adjMaxMagicAtk":14,"adjMinPhysicalArmor":4,"adjMaxPhysicalArmor":4,"adjMinMagicArmor":4,"adjMaxMagicArmor":4,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009007: _tools.RODict({
        "propID": 51009007,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":388,"adjMinPhysicalAtk":8,"adjMaxPhysicalAtk":14,"adjMinMagicAtk":8,"adjMaxMagicAtk":14,"adjMinPhysicalArmor":4,"adjMaxPhysicalArmor":4,"adjMinMagicArmor":4,"adjMaxMagicArmor":4,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009008: _tools.RODict({
        "propID": 51009008,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":478,"adjMinPhysicalAtk":8,"adjMaxPhysicalAtk":14,"adjMinMagicAtk":8,"adjMaxMagicAtk":14,"adjMinPhysicalArmor":4,"adjMaxPhysicalArmor":4,"adjMinMagicArmor":4,"adjMaxMagicArmor":4,"adjHit":5,"adjDodge":4,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009009: _tools.RODict({
        "propID": 51009009,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":488,"adjMinPhysicalAtk":8,"adjMaxPhysicalAtk":14,"adjMinMagicAtk":8,"adjMaxMagicAtk":14,"adjMinPhysicalArmor":5,"adjMaxPhysicalArmor":5,"adjMinMagicArmor":5,"adjMaxMagicArmor":5,"adjHit":5,"adjDodge":4,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009010: _tools.RODict({
        "propID": 51009010,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":498,"adjMinPhysicalAtk":10,"adjMaxPhysicalAtk":16,"adjMinMagicAtk":10,"adjMaxMagicAtk":16,"adjMinPhysicalArmor":5,"adjMaxPhysicalArmor":5,"adjMinMagicArmor":5,"adjMaxMagicArmor":5,"adjHit":7,"adjDodge":4,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009011: _tools.RODict({
        "propID": 51009011,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":516,"adjMinPhysicalAtk":10,"adjMaxPhysicalAtk":16,"adjMinMagicAtk":10,"adjMaxMagicAtk":16,"adjMinPhysicalArmor":6,"adjMaxPhysicalArmor":6,"adjMinMagicArmor":6,"adjMaxMagicArmor":6,"adjHit":7,"adjDodge":4,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009012: _tools.RODict({
        "propID": 51009012,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":534,"adjMinPhysicalAtk":10,"adjMaxPhysicalAtk":16,"adjMinMagicAtk":10,"adjMaxMagicAtk":16,"adjMinPhysicalArmor":6,"adjMaxPhysicalArmor":6,"adjMinMagicArmor":6,"adjMaxMagicArmor":6,"adjHit":7,"adjDodge":4,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009013: _tools.RODict({
        "propID": 51009013,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":552,"adjMinPhysicalAtk":10,"adjMaxPhysicalAtk":16,"adjMinMagicAtk":10,"adjMaxMagicAtk":16,"adjMinPhysicalArmor":7,"adjMaxPhysicalArmor":7,"adjMinMagicArmor":7,"adjMaxMagicArmor":7,"adjHit":7,"adjDodge":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009014: _tools.RODict({
        "propID": 51009014,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":562,"adjMinPhysicalAtk":11,"adjMaxPhysicalAtk":16,"adjMinMagicAtk":11,"adjMaxMagicAtk":16,"adjMinPhysicalArmor":7,"adjMaxPhysicalArmor":7,"adjMinMagicArmor":7,"adjMaxMagicArmor":7,"adjHit":7,"adjDodge":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009015: _tools.RODict({
        "propID": 51009015,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":572,"adjMinPhysicalAtk":11,"adjMaxPhysicalAtk":19,"adjMinMagicAtk":11,"adjMaxMagicAtk":19,"adjMinPhysicalArmor":7,"adjMaxPhysicalArmor":7,"adjMinMagicArmor":7,"adjMaxMagicArmor":7,"adjHit":9,"adjDodge":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009016: _tools.RODict({
        "propID": 51009016,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":590,"adjMinPhysicalAtk":11,"adjMaxPhysicalAtk":19,"adjMinMagicAtk":11,"adjMaxMagicAtk":19,"adjMinPhysicalArmor":8,"adjMaxPhysicalArmor":8,"adjMinMagicArmor":8,"adjMaxMagicArmor":8,"adjHit":9,"adjDodge":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009017: _tools.RODict({
        "propID": 51009017,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":608,"adjMinPhysicalAtk":11,"adjMaxPhysicalAtk":19,"adjMinMagicAtk":11,"adjMaxMagicAtk":19,"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjHit":9,"adjDodge":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009018: _tools.RODict({
        "propID": 51009018,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":626,"adjMinPhysicalAtk":12,"adjMaxPhysicalAtk":19,"adjMinMagicAtk":12,"adjMaxMagicAtk":19,"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjHit":9,"adjDodge":6,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009019: _tools.RODict({
        "propID": 51009019,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":636,"adjMinPhysicalAtk":12,"adjMaxPhysicalAtk":19,"adjMinMagicAtk":12,"adjMaxMagicAtk":19,"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10,"adjHit":9,"adjDodge":6,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009020: _tools.RODict({
        "propID": 51009020,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":646,"adjMinPhysicalAtk":13,"adjMaxPhysicalAtk":21,"adjMinMagicAtk":13,"adjMaxMagicAtk":21,"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10,"adjHit":15,"adjDodge":6,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009021: _tools.RODict({
        "propID": 51009021,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":696,"adjMinPhysicalAtk":13,"adjMaxPhysicalAtk":21,"adjMinMagicAtk":13,"adjMaxMagicAtk":21,"adjMinPhysicalArmor":13,"adjMaxPhysicalArmor":13,"adjMinMagicArmor":13,"adjMaxMagicArmor":13,"adjHit":15,"adjDodge":6,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009022: _tools.RODict({
        "propID": 51009022,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":730,"adjMinPhysicalAtk":13,"adjMaxPhysicalAtk":21,"adjMinMagicAtk":13,"adjMaxMagicAtk":21,"adjMinPhysicalArmor":13,"adjMaxPhysicalArmor":13,"adjMinMagicArmor":13,"adjMaxMagicArmor":13,"adjHit":15,"adjDodge":10,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009023: _tools.RODict({
        "propID": 51009023,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":750,"adjMinPhysicalAtk":14,"adjMaxPhysicalAtk":23,"adjMinMagicAtk":14,"adjMaxMagicAtk":23,"adjMinPhysicalArmor":14,"adjMaxPhysicalArmor":14,"adjMinMagicArmor":14,"adjMaxMagicArmor":14,"adjHit":15,"adjDodge":10,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009024: _tools.RODict({
        "propID": 51009024,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":760,"adjMinPhysicalAtk":15,"adjMaxPhysicalAtk":24,"adjMinMagicAtk":15,"adjMaxMagicAtk":24,"adjMinPhysicalArmor":14,"adjMaxPhysicalArmor":14,"adjMinMagicArmor":14,"adjMaxMagicArmor":14,"adjHit":15,"adjDodge":10,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009025: _tools.RODict({
        "propID": 51009025,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":794,"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":27,"adjMinMagicAtk":17,"adjMaxMagicAtk":27,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjHit":18,"adjDodge":10,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009026: _tools.RODict({
        "propID": 51009026,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":820,"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":27,"adjMinMagicAtk":17,"adjMaxMagicAtk":27,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjHit":18,"adjDodge":12,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009027: _tools.RODict({
        "propID": 51009027,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":830,"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":28,"adjMinMagicAtk":17,"adjMaxMagicAtk":28,"adjMinPhysicalArmor":17,"adjMaxPhysicalArmor":17,"adjMinMagicArmor":17,"adjMaxMagicArmor":17,"adjHit":18,"adjDodge":12,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009028: _tools.RODict({
        "propID": 51009028,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":840,"adjMinPhysicalAtk":18,"adjMaxPhysicalAtk":29,"adjMinMagicAtk":18,"adjMaxMagicAtk":29,"adjMinPhysicalArmor":17,"adjMaxPhysicalArmor":17,"adjMinMagicArmor":17,"adjMaxMagicArmor":17,"adjHit":18,"adjDodge":12,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009029: _tools.RODict({
        "propID": 51009029,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":874,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":32,"adjMinMagicAtk":20,"adjMaxMagicAtk":32,"adjMinPhysicalArmor":18,"adjMaxPhysicalArmor":18,"adjMinMagicArmor":18,"adjMaxMagicArmor":18,"adjHit":21,"adjDodge":12,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009030: _tools.RODict({
        "propID": 51009030,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":900,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":32,"adjMinMagicAtk":20,"adjMaxMagicAtk":32,"adjMinPhysicalArmor":19,"adjMaxPhysicalArmor":19,"adjMinMagicArmor":19,"adjMaxMagicArmor":19,"adjHit":21,"adjDodge":14,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009031: _tools.RODict({
        "propID": 51009031,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":910,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":34,"adjMinMagicAtk":20,"adjMaxMagicAtk":34,"adjMinPhysicalArmor":19,"adjMaxPhysicalArmor":19,"adjMinMagicArmor":19,"adjMaxMagicArmor":19,"adjHit":21,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009032: _tools.RODict({
        "propID": 51009032,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":920,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":35,"adjMinMagicAtk":21,"adjMaxMagicAtk":35,"adjMinPhysicalArmor":19,"adjMaxPhysicalArmor":19,"adjMinMagicArmor":19,"adjMaxMagicArmor":19,"adjHit":22,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":3,"adjMonsterDmgAnti":0.5})
    }),
    51009033: _tools.RODict({
        "propID": 51009033,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":974,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":38,"adjMinMagicAtk":23,"adjMaxMagicAtk":38,"adjMinPhysicalArmor":22,"adjMaxPhysicalArmor":22,"adjMinMagicArmor":22,"adjMaxMagicArmor":22,"adjHit":25,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":3,"adjMonsterDmgAnti":0.5})
    }),
    51009034: _tools.RODict({
        "propID": 51009034,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1000,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":39,"adjMinMagicAtk":23,"adjMaxMagicAtk":39,"adjMinPhysicalArmor":23,"adjMaxPhysicalArmor":23,"adjMinMagicArmor":23,"adjMaxMagicArmor":23,"adjHit":25,"adjDodge":16,"adjRealDmg":2,"adjRealDmgDef":3,"adjMonsterDmgAnti":0.5})
    }),
    51009035: _tools.RODict({
        "propID": 51009035,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1010,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":40,"adjMinMagicAtk":23,"adjMaxMagicAtk":40,"adjMinPhysicalArmor":24,"adjMaxPhysicalArmor":24,"adjMinMagicArmor":24,"adjMaxMagicArmor":24,"adjHit":25,"adjDodge":16,"adjRealDmg":3,"adjRealDmgDef":3,"adjMonsterDmgAnti":0.5})
    }),
    51009036: _tools.RODict({
        "propID": 51009036,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1020,"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":40,"adjMinMagicAtk":24,"adjMaxMagicAtk":40,"adjMinPhysicalArmor":24,"adjMaxPhysicalArmor":24,"adjMinMagicArmor":24,"adjMaxMagicArmor":24,"adjHit":25,"adjDodge":16,"adjRealDmg":3,"adjRealDmgDef":4,"adjMonsterDmgAnti":0.5})
    }),
    51009037: _tools.RODict({
        "propID": 51009037,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1030,"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":43,"adjMinMagicAtk":25,"adjMaxMagicAtk":43,"adjMinPhysicalArmor":25,"adjMaxPhysicalArmor":25,"adjMinMagicArmor":25,"adjMaxMagicArmor":25,"adjHit":34,"adjDodge":17,"adjRealDmg":3,"adjRealDmgDef":4,"adjMonsterDmgAnti":0.5})
    }),
    51009038: _tools.RODict({
        "propID": 51009038,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1152,"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":43,"adjMinMagicAtk":25,"adjMaxMagicAtk":43,"adjMinPhysicalArmor":29,"adjMaxPhysicalArmor":29,"adjMinMagicArmor":29,"adjMaxMagicArmor":29,"adjHit":34,"adjDodge":17,"adjRealDmg":4,"adjRealDmgDef":4,"adjMonsterDmgAnti":0.5})
    }),
    51009039: _tools.RODict({
        "propID": 51009039,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1234,"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":44,"adjMinMagicAtk":25,"adjMaxMagicAtk":44,"adjMinPhysicalArmor":30,"adjMaxPhysicalArmor":30,"adjMinMagicArmor":30,"adjMaxMagicArmor":30,"adjHit":34,"adjDodge":23,"adjRealDmg":4,"adjRealDmgDef":5,"adjMonsterDmgAnti":0.5})
    }),
    51009040: _tools.RODict({
        "propID": 51009040,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1244,"adjMinPhysicalAtk":27,"adjMaxPhysicalAtk":50,"adjMinMagicAtk":27,"adjMaxMagicAtk":50,"adjMinPhysicalArmor":30,"adjMaxPhysicalArmor":30,"adjMinMagicArmor":30,"adjMaxMagicArmor":30,"adjHit":34,"adjDodge":23,"adjRealDmg":4,"adjRealDmgDef":5,"adjMonsterDmgAnti":0.5})
    }),
    51009041: _tools.RODict({
        "propID": 51009041,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1254,"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":58,"adjMinMagicAtk":32,"adjMaxMagicAtk":58,"adjMinPhysicalArmor":31,"adjMaxPhysicalArmor":31,"adjMinMagicArmor":31,"adjMaxMagicArmor":31,"adjHit":38,"adjDodge":23,"adjRealDmg":4,"adjRealDmgDef":5,"adjMonsterDmgAnti":0.5})
    }),
    51009042: _tools.RODict({
        "propID": 51009042,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1318,"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":58,"adjMinMagicAtk":32,"adjMaxMagicAtk":58,"adjMinPhysicalArmor":32,"adjMaxPhysicalArmor":32,"adjMinMagicArmor":32,"adjMaxMagicArmor":32,"adjHit":38,"adjDodge":23,"adjRealDmg":5,"adjRealDmgDef":5,"adjMonsterDmgAnti":0.5})
    }),
    51009043: _tools.RODict({
        "propID": 51009043,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1408,"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":58,"adjMinMagicAtk":32,"adjMaxMagicAtk":58,"adjMinPhysicalArmor":34,"adjMaxPhysicalArmor":34,"adjMinMagicArmor":34,"adjMaxMagicArmor":34,"adjHit":38,"adjDodge":25,"adjRealDmg":5,"adjRealDmgDef":6,"adjMonsterDmgAnti":0.5})
    }),
    51009044: _tools.RODict({
        "propID": 51009044,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1418,"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":59,"adjMinMagicAtk":32,"adjMaxMagicAtk":59,"adjMinPhysicalArmor":35,"adjMaxPhysicalArmor":35,"adjMinMagicArmor":35,"adjMaxMagicArmor":35,"adjHit":38,"adjDodge":26,"adjRealDmg":5,"adjRealDmgDef":6,"adjMonsterDmgAnti":0.5})
    }),
    51009045: _tools.RODict({
        "propID": 51009045,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1428,"adjMinPhysicalAtk":33,"adjMaxPhysicalAtk":60,"adjMinMagicAtk":33,"adjMaxMagicAtk":60,"adjMinPhysicalArmor":37,"adjMaxPhysicalArmor":37,"adjMinMagicArmor":37,"adjMaxMagicArmor":37,"adjHit":38,"adjDodge":26,"adjRealDmg":5,"adjRealDmgDef":6,"adjMonsterDmgAnti":0.5})
    }),
    51009046: _tools.RODict({
        "propID": 51009046,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1473,"adjMinPhysicalAtk":35,"adjMaxPhysicalAtk":66,"adjMinMagicAtk":35,"adjMaxMagicAtk":66,"adjMinPhysicalArmor":37,"adjMaxPhysicalArmor":37,"adjMinMagicArmor":37,"adjMaxMagicArmor":37,"adjHit":43,"adjDodge":26,"adjRealDmg":5,"adjRealDmgDef":6,"adjMonsterDmgAnti":0.5})
    }),
    51009047: _tools.RODict({
        "propID": 51009047,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1507,"adjMinPhysicalAtk":35,"adjMaxPhysicalAtk":66,"adjMinMagicAtk":35,"adjMaxMagicAtk":66,"adjMinPhysicalArmor":40,"adjMaxPhysicalArmor":40,"adjMinMagicArmor":40,"adjMaxMagicArmor":40,"adjHit":43,"adjDodge":26,"adjRealDmg":6,"adjRealDmgDef":6,"adjMonsterDmgAnti":0.5})
    }),
    51009048: _tools.RODict({
        "propID": 51009048,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1597,"adjMinPhysicalAtk":36,"adjMaxPhysicalAtk":66,"adjMinMagicAtk":36,"adjMaxMagicAtk":66,"adjMinPhysicalArmor":40,"adjMaxPhysicalArmor":40,"adjMinMagicArmor":40,"adjMaxMagicArmor":40,"adjHit":43,"adjDodge":30,"adjRealDmg":6,"adjRealDmgDef":7,"adjMonsterDmgAnti":0.5})
    }),
    51009049: _tools.RODict({
        "propID": 51009049,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1647,"adjMinPhysicalAtk":37,"adjMaxPhysicalAtk":70,"adjMinMagicAtk":37,"adjMaxMagicAtk":70,"adjMinPhysicalArmor":42,"adjMaxPhysicalArmor":42,"adjMinMagicArmor":42,"adjMaxMagicArmor":42,"adjHit":45,"adjDodge":30,"adjRealDmg":6,"adjRealDmgDef":7,"adjMonsterDmgAnti":0.5})
    }),
    51009050: _tools.RODict({
        "propID": 51009050,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1657,"adjMinPhysicalAtk":38,"adjMaxPhysicalAtk":71,"adjMinMagicAtk":38,"adjMaxMagicAtk":71,"adjMinPhysicalArmor":44,"adjMaxPhysicalArmor":44,"adjMinMagicArmor":44,"adjMaxMagicArmor":44,"adjHit":45,"adjDodge":32,"adjRealDmg":6,"adjRealDmgDef":7,"adjMonsterDmgAnti":0.5})
    }),
    51009051: _tools.RODict({
        "propID": 51009051,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1667,"adjMinPhysicalAtk":41,"adjMaxPhysicalAtk":77,"adjMinMagicAtk":41,"adjMaxMagicAtk":77,"adjMinPhysicalArmor":45,"adjMaxPhysicalArmor":45,"adjMinMagicArmor":45,"adjMaxMagicArmor":45,"adjHit":48,"adjDodge":32,"adjRealDmg":6,"adjRealDmgDef":7,"adjMonsterDmgAnti":0.5})
    }),
    51009052: _tools.RODict({
        "propID": 51009052,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1725,"adjMinPhysicalAtk":42,"adjMaxPhysicalAtk":79,"adjMinMagicAtk":42,"adjMaxMagicAtk":79,"adjMinPhysicalArmor":46,"adjMaxPhysicalArmor":46,"adjMinMagicArmor":46,"adjMaxMagicArmor":46,"adjHit":51,"adjDodge":32,"adjRealDmg":7,"adjRealDmgDef":7,"adjMonsterDmgAnti":0.5})
    }),
    51009053: _tools.RODict({
        "propID": 51009053,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1940,"adjMinPhysicalAtk":42,"adjMaxPhysicalAtk":79,"adjMinMagicAtk":42,"adjMaxMagicAtk":79,"adjMinPhysicalArmor":48,"adjMaxPhysicalArmor":48,"adjMinMagicArmor":48,"adjMaxMagicArmor":48,"adjHit":51,"adjDodge":34,"adjRealDmg":7,"adjRealDmgDef":8,"adjMonsterDmgAnti":0.5})
    }),
    51009054: _tools.RODict({
        "propID": 51009054,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1950,"adjMinPhysicalAtk":43,"adjMaxPhysicalAtk":80,"adjMinMagicAtk":43,"adjMaxMagicAtk":80,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":50,"adjMaxMagicArmor":50,"adjHit":51,"adjDodge":34,"adjRealDmg":7,"adjRealDmgDef":8,"adjMonsterDmgAnti":0.5})
    }),
    51009055: _tools.RODict({
        "propID": 51009055,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1960,"adjMinPhysicalAtk":43,"adjMaxPhysicalAtk":82,"adjMinMagicAtk":43,"adjMaxMagicAtk":82,"adjMinPhysicalArmor":52,"adjMaxPhysicalArmor":52,"adjMinMagicArmor":52,"adjMaxMagicArmor":52,"adjHit":51,"adjDodge":37,"adjRealDmg":7,"adjRealDmgDef":8,"adjMonsterDmgAnti":0.5})
    }),
    51009056: _tools.RODict({
        "propID": 51009056,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1970,"adjMinPhysicalAtk":46,"adjMaxPhysicalAtk":88,"adjMinMagicAtk":46,"adjMaxMagicAtk":88,"adjMinPhysicalArmor":52,"adjMaxPhysicalArmor":52,"adjMinMagicArmor":52,"adjMaxMagicArmor":52,"adjHit":54,"adjDodge":37,"adjRealDmg":7,"adjRealDmgDef":8,"adjMonsterDmgAnti":0.5})
    }),
    51009057: _tools.RODict({
        "propID": 51009057,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2028,"adjMinPhysicalAtk":48,"adjMaxPhysicalAtk":90,"adjMinMagicAtk":48,"adjMaxMagicAtk":90,"adjMinPhysicalArmor":54,"adjMaxPhysicalArmor":54,"adjMinMagicArmor":54,"adjMaxMagicArmor":54,"adjHit":57,"adjDodge":37,"adjRealDmg":8,"adjRealDmgDef":8,"adjMonsterDmgAnti":0.5})
    }),
    51009058: _tools.RODict({
        "propID": 51009058,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2258,"adjMinPhysicalAtk":48,"adjMaxPhysicalAtk":90,"adjMinMagicAtk":48,"adjMaxMagicAtk":90,"adjMinPhysicalArmor":55,"adjMaxPhysicalArmor":55,"adjMinMagicArmor":55,"adjMaxMagicArmor":55,"adjHit":57,"adjDodge":39,"adjRealDmg":8,"adjRealDmgDef":9,"adjMonsterDmgAnti":0.5})
    }),
    51009059: _tools.RODict({
        "propID": 51009059,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2268,"adjMinPhysicalAtk":48,"adjMaxPhysicalAtk":93,"adjMinMagicAtk":48,"adjMaxMagicAtk":93,"adjMinPhysicalArmor":59,"adjMaxPhysicalArmor":59,"adjMinMagicArmor":59,"adjMaxMagicArmor":59,"adjHit":57,"adjDodge":39,"adjRealDmg":8,"adjRealDmgDef":9,"adjMonsterDmgAnti":0.5})
    }),
    51009060: _tools.RODict({
        "propID": 51009060,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2278,"adjMinPhysicalAtk":49,"adjMaxPhysicalAtk":95,"adjMinMagicAtk":49,"adjMaxMagicAtk":95,"adjMinPhysicalArmor":60,"adjMaxPhysicalArmor":60,"adjMinMagicArmor":60,"adjMaxMagicArmor":60,"adjHit":57,"adjDodge":42,"adjRealDmg":8,"adjRealDmgDef":9,"adjMonsterDmgAnti":0.5})
    }),
    51009061: _tools.RODict({
        "propID": 51009061,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2288,"adjMinPhysicalAtk":55,"adjMaxPhysicalAtk":106,"adjMinMagicAtk":55,"adjMaxMagicAtk":106,"adjMinPhysicalArmor":61,"adjMaxPhysicalArmor":61,"adjMinMagicArmor":61,"adjMaxMagicArmor":61,"adjHit":66,"adjDodge":42,"adjRealDmg":8,"adjRealDmgDef":9,"adjMonsterDmgAnti":0.5})
    }),
    51009062: _tools.RODict({
        "propID": 51009062,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2394,"adjMinPhysicalAtk":57,"adjMaxPhysicalAtk":109,"adjMinMagicAtk":57,"adjMaxMagicAtk":109,"adjMinPhysicalArmor":65,"adjMaxPhysicalArmor":65,"adjMinMagicArmor":65,"adjMaxMagicArmor":65,"adjHit":69,"adjDodge":42,"adjRealDmg":10,"adjRealDmgDef":9,"adjMonsterDmgAnti":0.5})
    }),
    51009063: _tools.RODict({
        "propID": 51009063,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2799,"adjMinPhysicalAtk":57,"adjMaxPhysicalAtk":109,"adjMinMagicAtk":57,"adjMaxMagicAtk":109,"adjMinPhysicalArmor":68,"adjMaxPhysicalArmor":68,"adjMinMagicArmor":68,"adjMaxMagicArmor":68,"adjHit":69,"adjDodge":48,"adjRealDmg":10,"adjRealDmgDef":11,"adjMonsterDmgAnti":0.5})
    }),
    51009064: _tools.RODict({
        "propID": 51009064,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2809,"adjMinPhysicalAtk":58,"adjMaxPhysicalAtk":113,"adjMinMagicAtk":58,"adjMaxMagicAtk":113,"adjMinPhysicalArmor":71,"adjMaxPhysicalArmor":71,"adjMinMagicArmor":71,"adjMaxMagicArmor":71,"adjHit":69,"adjDodge":48,"adjRealDmg":10,"adjRealDmgDef":11,"adjMonsterDmgAnti":0.5})
    }),
    51009065: _tools.RODict({
        "propID": 51009065,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2819,"adjMinPhysicalAtk":59,"adjMaxPhysicalAtk":118,"adjMinMagicAtk":59,"adjMaxMagicAtk":118,"adjMinPhysicalArmor":73,"adjMaxPhysicalArmor":73,"adjMinMagicArmor":73,"adjMaxMagicArmor":73,"adjHit":69,"adjDodge":52,"adjRealDmg":10,"adjRealDmgDef":11,"adjMonsterDmgAnti":0.5})
    }),
    51009066: _tools.RODict({
        "propID": 51009066,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2829,"adjMinPhysicalAtk":63,"adjMaxPhysicalAtk":126,"adjMinMagicAtk":63,"adjMaxMagicAtk":126,"adjMinPhysicalArmor":73,"adjMaxPhysicalArmor":73,"adjMinMagicArmor":73,"adjMaxMagicArmor":73,"adjHit":72,"adjDodge":52,"adjRealDmg":10,"adjRealDmgDef":11,"adjMonsterDmgAnti":0.5})
    }),
    51009067: _tools.RODict({
        "propID": 51009067,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2887,"adjMinPhysicalAtk":65,"adjMaxPhysicalAtk":129,"adjMinMagicAtk":65,"adjMaxMagicAtk":129,"adjMinPhysicalArmor":77,"adjMaxPhysicalArmor":77,"adjMinMagicArmor":77,"adjMaxMagicArmor":77,"adjHit":75,"adjDodge":52,"adjRealDmg":12,"adjRealDmgDef":11,"adjMonsterDmgAnti":0.5})
    }),
    51009068: _tools.RODict({
        "propID": 51009068,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3147,"adjMinPhysicalAtk":66,"adjMaxPhysicalAtk":129,"adjMinMagicAtk":66,"adjMaxMagicAtk":129,"adjMinPhysicalArmor":79,"adjMaxPhysicalArmor":79,"adjMinMagicArmor":79,"adjMaxMagicArmor":79,"adjHit":75,"adjDodge":54,"adjRealDmg":12,"adjRealDmgDef":13,"adjMonsterDmgAnti":0.5})
    }),
    51009069: _tools.RODict({
        "propID": 51009069,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3157,"adjMinPhysicalAtk":66,"adjMaxPhysicalAtk":132,"adjMinMagicAtk":66,"adjMaxMagicAtk":132,"adjMinPhysicalArmor":84,"adjMaxPhysicalArmor":84,"adjMinMagicArmor":84,"adjMaxMagicArmor":84,"adjHit":75,"adjDodge":54,"adjRealDmg":12,"adjRealDmgDef":13,"adjMonsterDmgAnti":0.5})
    }),
    51009070: _tools.RODict({
        "propID": 51009070,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3177,"adjMinPhysicalAtk":67,"adjMaxPhysicalAtk":135,"adjMinMagicAtk":67,"adjMaxMagicAtk":135,"adjMinPhysicalArmor":86,"adjMaxPhysicalArmor":86,"adjMinMagicArmor":86,"adjMaxMagicArmor":86,"adjHit":75,"adjDodge":58,"adjRealDmg":12,"adjRealDmgDef":13,"adjMonsterDmgAnti":0.5})
    }),
    51009101: _tools.RODict({
        "propID": 51009101,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":100,"adjMinPhysicalAtk":7,"adjMaxPhysicalAtk":10,"adjMinMagicAtk":7,"adjMaxMagicAtk":10,"adjMinPhysicalArmor":1,"adjMaxPhysicalArmor":1,"adjMinMagicArmor":1,"adjMaxMagicArmor":1,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009102: _tools.RODict({
        "propID": 51009102,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":105,"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":52,"adjMinMagicAtk":30,"adjMaxMagicAtk":52,"adjMinPhysicalArmor":1,"adjMaxPhysicalArmor":1,"adjMinMagicArmor":1,"adjMaxMagicArmor":1,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009103: _tools.RODict({
        "propID": 51009103,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":110,"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":53,"adjMinMagicAtk":30,"adjMaxMagicAtk":53,"adjMinPhysicalArmor":1,"adjMaxPhysicalArmor":1,"adjMinMagicArmor":1,"adjMaxMagicArmor":1,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009104: _tools.RODict({
        "propID": 51009104,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":139,"adjMinPhysicalAtk":31,"adjMaxPhysicalAtk":53,"adjMinMagicAtk":31,"adjMaxMagicAtk":53,"adjMinPhysicalArmor":3,"adjMaxPhysicalArmor":3,"adjMinMagicArmor":3,"adjMaxMagicArmor":3,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009105: _tools.RODict({
        "propID": 51009105,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":144,"adjMinPhysicalAtk":31,"adjMaxPhysicalAtk":54,"adjMinMagicAtk":31,"adjMaxMagicAtk":54,"adjMinPhysicalArmor":3,"adjMaxPhysicalArmor":3,"adjMinMagicArmor":3,"adjMaxMagicArmor":3,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009106: _tools.RODict({
        "propID": 51009106,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":189,"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":54,"adjMinMagicAtk":32,"adjMaxMagicAtk":54,"adjMinPhysicalArmor":4,"adjMaxPhysicalArmor":4,"adjMinMagicArmor":4,"adjMaxMagicArmor":4,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009107: _tools.RODict({
        "propID": 51009107,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":194,"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":55,"adjMinMagicAtk":32,"adjMaxMagicAtk":55,"adjMinPhysicalArmor":4,"adjMaxPhysicalArmor":4,"adjMinMagicArmor":4,"adjMaxMagicArmor":4,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009108: _tools.RODict({
        "propID": 51009108,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":239,"adjMinPhysicalAtk":33,"adjMaxPhysicalAtk":55,"adjMinMagicAtk":33,"adjMaxMagicAtk":55,"adjMinPhysicalArmor":4,"adjMaxPhysicalArmor":4,"adjMinMagicArmor":4,"adjMaxMagicArmor":4,"adjHit":5,"adjDodge":4,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009109: _tools.RODict({
        "propID": 51009109,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":244,"adjMinPhysicalAtk":33,"adjMaxPhysicalAtk":56,"adjMinMagicAtk":33,"adjMaxMagicAtk":56,"adjMinPhysicalArmor":5,"adjMaxPhysicalArmor":5,"adjMinMagicArmor":5,"adjMaxMagicArmor":5,"adjHit":5,"adjDodge":4,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009110: _tools.RODict({
        "propID": 51009110,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":249,"adjMinPhysicalAtk":40,"adjMaxPhysicalAtk":62,"adjMinMagicAtk":40,"adjMaxMagicAtk":62,"adjMinPhysicalArmor":5,"adjMaxPhysicalArmor":5,"adjMinMagicArmor":5,"adjMaxMagicArmor":5,"adjHit":7,"adjDodge":4,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009111: _tools.RODict({
        "propID": 51009111,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":258,"adjMinPhysicalAtk":40,"adjMaxPhysicalAtk":63,"adjMinMagicAtk":40,"adjMaxMagicAtk":63,"adjMinPhysicalArmor":6,"adjMaxPhysicalArmor":6,"adjMinMagicArmor":6,"adjMaxMagicArmor":6,"adjHit":7,"adjDodge":4,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009112: _tools.RODict({
        "propID": 51009112,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":267,"adjMinPhysicalAtk":41,"adjMaxPhysicalAtk":63,"adjMinMagicAtk":41,"adjMaxMagicAtk":63,"adjMinPhysicalArmor":6,"adjMaxPhysicalArmor":6,"adjMinMagicArmor":6,"adjMaxMagicArmor":6,"adjHit":7,"adjDodge":4,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009113: _tools.RODict({
        "propID": 51009113,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":276,"adjMinPhysicalAtk":41,"adjMaxPhysicalAtk":64,"adjMinMagicAtk":41,"adjMaxMagicAtk":64,"adjMinPhysicalArmor":7,"adjMaxPhysicalArmor":7,"adjMinMagicArmor":7,"adjMaxMagicArmor":7,"adjHit":7,"adjDodge":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009114: _tools.RODict({
        "propID": 51009114,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":281,"adjMinPhysicalAtk":42,"adjMaxPhysicalAtk":64,"adjMinMagicAtk":42,"adjMaxMagicAtk":64,"adjMinPhysicalArmor":7,"adjMaxPhysicalArmor":7,"adjMinMagicArmor":7,"adjMaxMagicArmor":7,"adjHit":7,"adjDodge":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009115: _tools.RODict({
        "propID": 51009115,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":286,"adjMinPhysicalAtk":44,"adjMaxPhysicalAtk":75,"adjMinMagicAtk":44,"adjMaxMagicAtk":75,"adjMinPhysicalArmor":7,"adjMaxPhysicalArmor":7,"adjMinMagicArmor":7,"adjMaxMagicArmor":7,"adjHit":9,"adjDodge":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009116: _tools.RODict({
        "propID": 51009116,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":295,"adjMinPhysicalAtk":45,"adjMaxPhysicalAtk":75,"adjMinMagicAtk":45,"adjMaxMagicAtk":75,"adjMinPhysicalArmor":8,"adjMaxPhysicalArmor":8,"adjMinMagicArmor":8,"adjMaxMagicArmor":8,"adjHit":9,"adjDodge":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009117: _tools.RODict({
        "propID": 51009117,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":304,"adjMinPhysicalAtk":45,"adjMaxPhysicalAtk":76,"adjMinMagicAtk":45,"adjMaxMagicAtk":76,"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjHit":9,"adjDodge":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009118: _tools.RODict({
        "propID": 51009118,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":313,"adjMinPhysicalAtk":46,"adjMaxPhysicalAtk":76,"adjMinMagicAtk":46,"adjMaxMagicAtk":76,"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjHit":9,"adjDodge":6,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009119: _tools.RODict({
        "propID": 51009119,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":318,"adjMinPhysicalAtk":46,"adjMaxPhysicalAtk":77,"adjMinMagicAtk":46,"adjMaxMagicAtk":77,"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10,"adjHit":9,"adjDodge":6,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009120: _tools.RODict({
        "propID": 51009120,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":323,"adjMinPhysicalAtk":51,"adjMaxPhysicalAtk":83,"adjMinMagicAtk":51,"adjMaxMagicAtk":83,"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10,"adjHit":15,"adjDodge":6,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009121: _tools.RODict({
        "propID": 51009121,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":348,"adjMinPhysicalAtk":52,"adjMaxPhysicalAtk":85,"adjMinMagicAtk":52,"adjMaxMagicAtk":85,"adjMinPhysicalArmor":13,"adjMaxPhysicalArmor":13,"adjMinMagicArmor":13,"adjMaxMagicArmor":13,"adjHit":15,"adjDodge":6,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009122: _tools.RODict({
        "propID": 51009122,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":365,"adjMinPhysicalAtk":53,"adjMaxPhysicalAtk":85,"adjMinMagicAtk":53,"adjMaxMagicAtk":85,"adjMinPhysicalArmor":13,"adjMaxPhysicalArmor":13,"adjMinMagicArmor":13,"adjMaxMagicArmor":13,"adjHit":15,"adjDodge":10,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009123: _tools.RODict({
        "propID": 51009123,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":375,"adjMinPhysicalAtk":56,"adjMaxPhysicalAtk":90,"adjMinMagicAtk":56,"adjMaxMagicAtk":90,"adjMinPhysicalArmor":14,"adjMaxPhysicalArmor":14,"adjMinMagicArmor":14,"adjMaxMagicArmor":14,"adjHit":15,"adjDodge":10,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009124: _tools.RODict({
        "propID": 51009124,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":380,"adjMinPhysicalAtk":60,"adjMaxPhysicalAtk":94,"adjMinMagicAtk":60,"adjMaxMagicAtk":94,"adjMinPhysicalArmor":14,"adjMaxPhysicalArmor":14,"adjMinMagicArmor":14,"adjMaxMagicArmor":14,"adjHit":15,"adjDodge":10,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009125: _tools.RODict({
        "propID": 51009125,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":397,"adjMinPhysicalAtk":68,"adjMaxPhysicalAtk":109,"adjMinMagicAtk":68,"adjMaxMagicAtk":109,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjHit":18,"adjDodge":10,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009126: _tools.RODict({
        "propID": 51009126,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":410,"adjMinPhysicalAtk":69,"adjMaxPhysicalAtk":109,"adjMinMagicAtk":69,"adjMaxMagicAtk":109,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjHit":18,"adjDodge":12,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009127: _tools.RODict({
        "propID": 51009127,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":415,"adjMinPhysicalAtk":69,"adjMaxPhysicalAtk":110,"adjMinMagicAtk":69,"adjMaxMagicAtk":110,"adjMinPhysicalArmor":17,"adjMaxPhysicalArmor":17,"adjMinMagicArmor":17,"adjMaxMagicArmor":17,"adjHit":18,"adjDodge":12,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009128: _tools.RODict({
        "propID": 51009128,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":420,"adjMinPhysicalAtk":72,"adjMaxPhysicalAtk":114,"adjMinMagicAtk":72,"adjMaxMagicAtk":114,"adjMinPhysicalArmor":17,"adjMaxPhysicalArmor":17,"adjMinMagicArmor":17,"adjMaxMagicArmor":17,"adjHit":18,"adjDodge":12,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009129: _tools.RODict({
        "propID": 51009129,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":437,"adjMinPhysicalAtk":78,"adjMaxPhysicalAtk":128,"adjMinMagicAtk":78,"adjMaxMagicAtk":128,"adjMinPhysicalArmor":18,"adjMaxPhysicalArmor":18,"adjMinMagicArmor":18,"adjMaxMagicArmor":18,"adjHit":21,"adjDodge":12,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009130: _tools.RODict({
        "propID": 51009130,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":450,"adjMinPhysicalAtk":79,"adjMaxPhysicalAtk":129,"adjMinMagicAtk":79,"adjMaxMagicAtk":129,"adjMinPhysicalArmor":19,"adjMaxPhysicalArmor":19,"adjMinMagicArmor":19,"adjMaxMagicArmor":19,"adjHit":21,"adjDodge":14,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009131: _tools.RODict({
        "propID": 51009131,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":455,"adjMinPhysicalAtk":80,"adjMaxPhysicalAtk":134,"adjMinMagicAtk":80,"adjMaxMagicAtk":134,"adjMinPhysicalArmor":19,"adjMaxPhysicalArmor":19,"adjMinMagicArmor":19,"adjMaxMagicArmor":19,"adjHit":21,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009132: _tools.RODict({
        "propID": 51009132,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":460,"adjMinPhysicalAtk":84,"adjMaxPhysicalAtk":140,"adjMinMagicAtk":84,"adjMaxMagicAtk":140,"adjMinPhysicalArmor":19,"adjMaxPhysicalArmor":19,"adjMinMagicArmor":19,"adjMaxMagicArmor":19,"adjHit":22,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":3,"adjMonsterDmgAnti":0.5})
    }),
    51009133: _tools.RODict({
        "propID": 51009133,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":487,"adjMinPhysicalAtk":90,"adjMaxPhysicalAtk":153,"adjMinMagicAtk":90,"adjMaxMagicAtk":153,"adjMinPhysicalArmor":22,"adjMaxPhysicalArmor":22,"adjMinMagicArmor":22,"adjMaxMagicArmor":22,"adjHit":25,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":3,"adjMonsterDmgAnti":0.5})
    }),
    51009134: _tools.RODict({
        "propID": 51009134,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":500,"adjMinPhysicalAtk":91,"adjMaxPhysicalAtk":154,"adjMinMagicAtk":91,"adjMaxMagicAtk":154,"adjMinPhysicalArmor":23,"adjMaxPhysicalArmor":23,"adjMinMagicArmor":23,"adjMaxMagicArmor":23,"adjHit":25,"adjDodge":16,"adjRealDmg":2,"adjRealDmgDef":3,"adjMonsterDmgAnti":0.5})
    }),
    51009135: _tools.RODict({
        "propID": 51009135,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":505,"adjMinPhysicalAtk":92,"adjMaxPhysicalAtk":158,"adjMinMagicAtk":92,"adjMaxMagicAtk":158,"adjMinPhysicalArmor":24,"adjMaxPhysicalArmor":24,"adjMinMagicArmor":24,"adjMaxMagicArmor":24,"adjHit":25,"adjDodge":16,"adjRealDmg":3,"adjRealDmgDef":3,"adjMonsterDmgAnti":0.5})
    }),
    51009136: _tools.RODict({
        "propID": 51009136,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":510,"adjMinPhysicalAtk":94,"adjMaxPhysicalAtk":160,"adjMinMagicAtk":94,"adjMaxMagicAtk":160,"adjMinPhysicalArmor":24,"adjMaxPhysicalArmor":24,"adjMinMagicArmor":24,"adjMaxMagicArmor":24,"adjHit":25,"adjDodge":16,"adjRealDmg":3,"adjRealDmgDef":4,"adjMonsterDmgAnti":0.5})
    }),
    51009137: _tools.RODict({
        "propID": 51009137,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":515,"adjMinPhysicalAtk":100,"adjMaxPhysicalAtk":173,"adjMinMagicAtk":100,"adjMaxMagicAtk":173,"adjMinPhysicalArmor":25,"adjMaxPhysicalArmor":25,"adjMinMagicArmor":25,"adjMaxMagicArmor":25,"adjHit":34,"adjDodge":17,"adjRealDmg":3,"adjRealDmgDef":4,"adjMonsterDmgAnti":0.5})
    }),
    51009138: _tools.RODict({
        "propID": 51009138,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":576,"adjMinPhysicalAtk":101,"adjMaxPhysicalAtk":173,"adjMinMagicAtk":101,"adjMaxMagicAtk":173,"adjMinPhysicalArmor":29,"adjMaxPhysicalArmor":29,"adjMinMagicArmor":29,"adjMaxMagicArmor":29,"adjHit":34,"adjDodge":17,"adjRealDmg":4,"adjRealDmgDef":4,"adjMonsterDmgAnti":0.5})
    }),
    51009139: _tools.RODict({
        "propID": 51009139,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":617,"adjMinPhysicalAtk":101,"adjMaxPhysicalAtk":176,"adjMinMagicAtk":101,"adjMaxMagicAtk":176,"adjMinPhysicalArmor":30,"adjMaxPhysicalArmor":30,"adjMinMagicArmor":30,"adjMaxMagicArmor":30,"adjHit":34,"adjDodge":23,"adjRealDmg":4,"adjRealDmgDef":5,"adjMonsterDmgAnti":0.5})
    }),
    51009140: _tools.RODict({
        "propID": 51009140,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":622,"adjMinPhysicalAtk":108,"adjMaxPhysicalAtk":198,"adjMinMagicAtk":108,"adjMaxMagicAtk":198,"adjMinPhysicalArmor":30,"adjMaxPhysicalArmor":30,"adjMinMagicArmor":30,"adjMaxMagicArmor":30,"adjHit":34,"adjDodge":23,"adjRealDmg":4,"adjRealDmgDef":5,"adjMonsterDmgAnti":0.5})
    }),
    51009141: _tools.RODict({
        "propID": 51009141,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":627,"adjMinPhysicalAtk":126,"adjMaxPhysicalAtk":230,"adjMinMagicAtk":126,"adjMaxMagicAtk":230,"adjMinPhysicalArmor":31,"adjMaxPhysicalArmor":31,"adjMinMagicArmor":31,"adjMaxMagicArmor":31,"adjHit":38,"adjDodge":23,"adjRealDmg":4,"adjRealDmgDef":5,"adjMonsterDmgAnti":0.5})
    }),
    51009142: _tools.RODict({
        "propID": 51009142,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":659,"adjMinPhysicalAtk":127,"adjMaxPhysicalAtk":230,"adjMinMagicAtk":127,"adjMaxMagicAtk":230,"adjMinPhysicalArmor":32,"adjMaxPhysicalArmor":32,"adjMinMagicArmor":32,"adjMaxMagicArmor":32,"adjHit":38,"adjDodge":23,"adjRealDmg":5,"adjRealDmgDef":5,"adjMonsterDmgAnti":0.5})
    }),
    51009143: _tools.RODict({
        "propID": 51009143,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":704,"adjMinPhysicalAtk":127,"adjMaxPhysicalAtk":231,"adjMinMagicAtk":127,"adjMaxMagicAtk":231,"adjMinPhysicalArmor":34,"adjMaxPhysicalArmor":34,"adjMinMagicArmor":34,"adjMaxMagicArmor":34,"adjHit":38,"adjDodge":25,"adjRealDmg":5,"adjRealDmgDef":6,"adjMonsterDmgAnti":0.5})
    }),
    51009144: _tools.RODict({
        "propID": 51009144,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":709,"adjMinPhysicalAtk":129,"adjMaxPhysicalAtk":235,"adjMinMagicAtk":129,"adjMaxMagicAtk":235,"adjMinPhysicalArmor":35,"adjMaxPhysicalArmor":35,"adjMinMagicArmor":35,"adjMaxMagicArmor":35,"adjHit":38,"adjDodge":26,"adjRealDmg":5,"adjRealDmgDef":6,"adjMonsterDmgAnti":0.5})
    }),
    51009145: _tools.RODict({
        "propID": 51009145,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":714,"adjMinPhysicalAtk":130,"adjMaxPhysicalAtk":240,"adjMinMagicAtk":130,"adjMaxMagicAtk":240,"adjMinPhysicalArmor":37,"adjMaxPhysicalArmor":37,"adjMinMagicArmor":37,"adjMaxMagicArmor":37,"adjHit":38,"adjDodge":26,"adjRealDmg":5,"adjRealDmgDef":6,"adjMonsterDmgAnti":0.5})
    }),
    51009146: _tools.RODict({
        "propID": 51009146,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":737,"adjMinPhysicalAtk":141,"adjMaxPhysicalAtk":263,"adjMinMagicAtk":141,"adjMaxMagicAtk":263,"adjMinPhysicalArmor":37,"adjMaxPhysicalArmor":37,"adjMinMagicArmor":37,"adjMaxMagicArmor":37,"adjHit":43,"adjDodge":26,"adjRealDmg":5,"adjRealDmgDef":6,"adjMonsterDmgAnti":0.5})
    }),
    51009147: _tools.RODict({
        "propID": 51009147,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":754,"adjMinPhysicalAtk":141,"adjMaxPhysicalAtk":264,"adjMinMagicAtk":141,"adjMaxMagicAtk":264,"adjMinPhysicalArmor":40,"adjMaxPhysicalArmor":40,"adjMinMagicArmor":40,"adjMaxMagicArmor":40,"adjHit":43,"adjDodge":26,"adjRealDmg":6,"adjRealDmgDef":6,"adjMonsterDmgAnti":0.5})
    }),
    51009148: _tools.RODict({
        "propID": 51009148,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":799,"adjMinPhysicalAtk":142,"adjMaxPhysicalAtk":264,"adjMinMagicAtk":142,"adjMaxMagicAtk":264,"adjMinPhysicalArmor":40,"adjMaxPhysicalArmor":40,"adjMinMagicArmor":40,"adjMaxMagicArmor":40,"adjHit":43,"adjDodge":30,"adjRealDmg":6,"adjRealDmgDef":7,"adjMonsterDmgAnti":0.5})
    }),
    51009149: _tools.RODict({
        "propID": 51009149,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":824,"adjMinPhysicalAtk":147,"adjMaxPhysicalAtk":278,"adjMinMagicAtk":147,"adjMaxMagicAtk":278,"adjMinPhysicalArmor":42,"adjMaxPhysicalArmor":42,"adjMinMagicArmor":42,"adjMaxMagicArmor":42,"adjHit":45,"adjDodge":30,"adjRealDmg":6,"adjRealDmgDef":7,"adjMonsterDmgAnti":0.5})
    }),
    51009150: _tools.RODict({
        "propID": 51009150,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":829,"adjMinPhysicalAtk":150,"adjMaxPhysicalAtk":285,"adjMinMagicAtk":150,"adjMaxMagicAtk":285,"adjMinPhysicalArmor":44,"adjMaxPhysicalArmor":44,"adjMinMagicArmor":44,"adjMaxMagicArmor":44,"adjHit":45,"adjDodge":32,"adjRealDmg":6,"adjRealDmgDef":7,"adjMonsterDmgAnti":0.5})
    }),
    51009151: _tools.RODict({
        "propID": 51009151,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":834,"adjMinPhysicalAtk":162,"adjMaxPhysicalAtk":306,"adjMinMagicAtk":162,"adjMaxMagicAtk":306,"adjMinPhysicalArmor":45,"adjMaxPhysicalArmor":45,"adjMinMagicArmor":45,"adjMaxMagicArmor":45,"adjHit":48,"adjDodge":32,"adjRealDmg":6,"adjRealDmgDef":7,"adjMonsterDmgAnti":0.5})
    }),
    51009152: _tools.RODict({
        "propID": 51009152,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":863,"adjMinPhysicalAtk":167,"adjMaxPhysicalAtk":314,"adjMinMagicAtk":167,"adjMaxMagicAtk":314,"adjMinPhysicalArmor":46,"adjMaxPhysicalArmor":46,"adjMinMagicArmor":46,"adjMaxMagicArmor":46,"adjHit":51,"adjDodge":32,"adjRealDmg":7,"adjRealDmgDef":7,"adjMonsterDmgAnti":0.5})
    }),
    51009153: _tools.RODict({
        "propID": 51009153,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":970,"adjMinPhysicalAtk":167,"adjMaxPhysicalAtk":315,"adjMinMagicAtk":167,"adjMaxMagicAtk":315,"adjMinPhysicalArmor":48,"adjMaxPhysicalArmor":48,"adjMinMagicArmor":48,"adjMaxMagicArmor":48,"adjHit":51,"adjDodge":34,"adjRealDmg":7,"adjRealDmgDef":8,"adjMonsterDmgAnti":0.5})
    }),
    51009154: _tools.RODict({
        "propID": 51009154,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":975,"adjMinPhysicalAtk":170,"adjMaxPhysicalAtk":320,"adjMinMagicAtk":170,"adjMaxMagicAtk":320,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":50,"adjMaxMagicArmor":50,"adjHit":51,"adjDodge":34,"adjRealDmg":7,"adjRealDmgDef":8,"adjMonsterDmgAnti":0.5})
    }),
    51009155: _tools.RODict({
        "propID": 51009155,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":980,"adjMinPhysicalAtk":172,"adjMaxPhysicalAtk":326,"adjMinMagicAtk":172,"adjMaxMagicAtk":326,"adjMinPhysicalArmor":52,"adjMaxPhysicalArmor":52,"adjMinMagicArmor":52,"adjMaxMagicArmor":52,"adjHit":51,"adjDodge":37,"adjRealDmg":7,"adjRealDmgDef":8,"adjMonsterDmgAnti":0.5})
    }),
    51009156: _tools.RODict({
        "propID": 51009156,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":985,"adjMinPhysicalAtk":185,"adjMaxPhysicalAtk":350,"adjMinMagicAtk":185,"adjMaxMagicAtk":350,"adjMinPhysicalArmor":52,"adjMaxPhysicalArmor":52,"adjMinMagicArmor":52,"adjMaxMagicArmor":52,"adjHit":54,"adjDodge":37,"adjRealDmg":7,"adjRealDmgDef":8,"adjMonsterDmgAnti":0.5})
    }),
    51009157: _tools.RODict({
        "propID": 51009157,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1014,"adjMinPhysicalAtk":190,"adjMaxPhysicalAtk":360,"adjMinMagicAtk":190,"adjMaxMagicAtk":360,"adjMinPhysicalArmor":54,"adjMaxPhysicalArmor":54,"adjMinMagicArmor":54,"adjMaxMagicArmor":54,"adjHit":57,"adjDodge":37,"adjRealDmg":8,"adjRealDmgDef":8,"adjMonsterDmgAnti":0.5})
    }),
    51009158: _tools.RODict({
        "propID": 51009158,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1129,"adjMinPhysicalAtk":191,"adjMaxPhysicalAtk":360,"adjMinMagicAtk":191,"adjMaxMagicAtk":360,"adjMinPhysicalArmor":55,"adjMaxPhysicalArmor":55,"adjMinMagicArmor":55,"adjMaxMagicArmor":55,"adjHit":57,"adjDodge":39,"adjRealDmg":8,"adjRealDmgDef":9,"adjMonsterDmgAnti":0.5})
    }),
    51009159: _tools.RODict({
        "propID": 51009159,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1134,"adjMinPhysicalAtk":193,"adjMaxPhysicalAtk":371,"adjMinMagicAtk":193,"adjMaxMagicAtk":371,"adjMinPhysicalArmor":59,"adjMaxPhysicalArmor":59,"adjMinMagicArmor":59,"adjMaxMagicArmor":59,"adjHit":57,"adjDodge":39,"adjRealDmg":8,"adjRealDmgDef":9,"adjMonsterDmgAnti":0.5})
    }),
    51009160: _tools.RODict({
        "propID": 51009160,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1139,"adjMinPhysicalAtk":196,"adjMaxPhysicalAtk":381,"adjMinMagicAtk":196,"adjMaxMagicAtk":381,"adjMinPhysicalArmor":60,"adjMaxPhysicalArmor":60,"adjMinMagicArmor":60,"adjMaxMagicArmor":60,"adjHit":57,"adjDodge":42,"adjRealDmg":8,"adjRealDmgDef":9,"adjMonsterDmgAnti":0.5})
    }),
    51009161: _tools.RODict({
        "propID": 51009161,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1144,"adjMinPhysicalAtk":220,"adjMaxPhysicalAtk":424,"adjMinMagicAtk":220,"adjMaxMagicAtk":424,"adjMinPhysicalArmor":61,"adjMaxPhysicalArmor":61,"adjMinMagicArmor":61,"adjMaxMagicArmor":61,"adjHit":66,"adjDodge":42,"adjRealDmg":8,"adjRealDmgDef":9,"adjMonsterDmgAnti":0.5})
    }),
    51009162: _tools.RODict({
        "propID": 51009162,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1197,"adjMinPhysicalAtk":227,"adjMaxPhysicalAtk":434,"adjMinMagicAtk":227,"adjMaxMagicAtk":434,"adjMinPhysicalArmor":65,"adjMaxPhysicalArmor":65,"adjMinMagicArmor":65,"adjMaxMagicArmor":65,"adjHit":69,"adjDodge":42,"adjRealDmg":10,"adjRealDmgDef":9,"adjMonsterDmgAnti":0.5})
    }),
    51009163: _tools.RODict({
        "propID": 51009163,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1400,"adjMinPhysicalAtk":227,"adjMaxPhysicalAtk":435,"adjMinMagicAtk":227,"adjMaxMagicAtk":435,"adjMinPhysicalArmor":68,"adjMaxPhysicalArmor":68,"adjMinMagicArmor":68,"adjMaxMagicArmor":68,"adjHit":69,"adjDodge":48,"adjRealDmg":10,"adjRealDmgDef":11,"adjMonsterDmgAnti":0.5})
    }),
    51009164: _tools.RODict({
        "propID": 51009164,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1405,"adjMinPhysicalAtk":231,"adjMaxPhysicalAtk":452,"adjMinMagicAtk":231,"adjMaxMagicAtk":452,"adjMinPhysicalArmor":71,"adjMaxPhysicalArmor":71,"adjMinMagicArmor":71,"adjMaxMagicArmor":71,"adjHit":69,"adjDodge":48,"adjRealDmg":10,"adjRealDmgDef":11,"adjMonsterDmgAnti":0.5})
    }),
    51009165: _tools.RODict({
        "propID": 51009165,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1410,"adjMinPhysicalAtk":234,"adjMaxPhysicalAtk":470,"adjMinMagicAtk":234,"adjMaxMagicAtk":470,"adjMinPhysicalArmor":73,"adjMaxPhysicalArmor":73,"adjMinMagicArmor":73,"adjMaxMagicArmor":73,"adjHit":69,"adjDodge":52,"adjRealDmg":10,"adjRealDmgDef":11,"adjMonsterDmgAnti":0.5})
    }),
    51009166: _tools.RODict({
        "propID": 51009166,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1415,"adjMinPhysicalAtk":253,"adjMaxPhysicalAtk":504,"adjMinMagicAtk":253,"adjMaxMagicAtk":504,"adjMinPhysicalArmor":73,"adjMaxPhysicalArmor":73,"adjMinMagicArmor":73,"adjMaxMagicArmor":73,"adjHit":72,"adjDodge":52,"adjRealDmg":10,"adjRealDmgDef":11,"adjMonsterDmgAnti":0.5})
    }),
    51009167: _tools.RODict({
        "propID": 51009167,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1444,"adjMinPhysicalAtk":261,"adjMaxPhysicalAtk":516,"adjMinMagicAtk":261,"adjMaxMagicAtk":516,"adjMinPhysicalArmor":77,"adjMaxPhysicalArmor":77,"adjMinMagicArmor":77,"adjMaxMagicArmor":77,"adjHit":75,"adjDodge":52,"adjRealDmg":12,"adjRealDmgDef":11,"adjMonsterDmgAnti":0.5})
    }),
    51009168: _tools.RODict({
        "propID": 51009168,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1574,"adjMinPhysicalAtk":262,"adjMaxPhysicalAtk":516,"adjMinMagicAtk":262,"adjMaxMagicAtk":516,"adjMinPhysicalArmor":79,"adjMaxPhysicalArmor":79,"adjMinMagicArmor":79,"adjMaxMagicArmor":79,"adjHit":75,"adjDodge":54,"adjRealDmg":12,"adjRealDmgDef":13,"adjMonsterDmgAnti":0.5})
    }),
    51009169: _tools.RODict({
        "propID": 51009169,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1579,"adjMinPhysicalAtk":264,"adjMaxPhysicalAtk":529,"adjMinMagicAtk":264,"adjMaxMagicAtk":529,"adjMinPhysicalArmor":84,"adjMaxPhysicalArmor":84,"adjMinMagicArmor":84,"adjMaxMagicArmor":84,"adjHit":75,"adjDodge":54,"adjRealDmg":12,"adjRealDmgDef":13,"adjMonsterDmgAnti":0.5})
    }),
    51009170: _tools.RODict({
        "propID": 51009170,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1589,"adjMinPhysicalAtk":267,"adjMaxPhysicalAtk":541,"adjMinMagicAtk":267,"adjMaxMagicAtk":541,"adjMinPhysicalArmor":86,"adjMaxPhysicalArmor":86,"adjMinMagicArmor":86,"adjMaxMagicArmor":86,"adjHit":75,"adjDodge":58,"adjRealDmg":12,"adjRealDmgDef":13,"adjMonsterDmgAnti":0.5})
    }),
    51009201: _tools.RODict({
        "propID": 51009201,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":150,"adjMinPhysicalAtk":4,"adjMaxPhysicalAtk":5,"adjMinMagicAtk":4,"adjMaxMagicAtk":5,"adjMinPhysicalArmor":1,"adjMaxPhysicalArmor":1,"adjMinMagicArmor":1,"adjMaxMagicArmor":1,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009202: _tools.RODict({
        "propID": 51009202,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":158,"adjMinPhysicalAtk":15,"adjMaxPhysicalAtk":26,"adjMinMagicAtk":15,"adjMaxMagicAtk":26,"adjMinPhysicalArmor":1,"adjMaxPhysicalArmor":1,"adjMinMagicArmor":1,"adjMaxMagicArmor":1,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009203: _tools.RODict({
        "propID": 51009203,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":165,"adjMinPhysicalAtk":15,"adjMaxPhysicalAtk":27,"adjMinMagicAtk":15,"adjMaxMagicAtk":27,"adjMinPhysicalArmor":1,"adjMaxPhysicalArmor":1,"adjMinMagicArmor":1,"adjMaxMagicArmor":1,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009204: _tools.RODict({
        "propID": 51009204,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":209,"adjMinPhysicalAtk":16,"adjMaxPhysicalAtk":27,"adjMinMagicAtk":16,"adjMaxMagicAtk":27,"adjMinPhysicalArmor":3,"adjMaxPhysicalArmor":3,"adjMinMagicArmor":3,"adjMaxMagicArmor":3,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009205: _tools.RODict({
        "propID": 51009205,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":216,"adjMinPhysicalAtk":16,"adjMaxPhysicalAtk":27,"adjMinMagicAtk":16,"adjMaxMagicAtk":27,"adjMinPhysicalArmor":3,"adjMaxPhysicalArmor":3,"adjMinMagicArmor":3,"adjMaxMagicArmor":3,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009206: _tools.RODict({
        "propID": 51009206,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":284,"adjMinPhysicalAtk":16,"adjMaxPhysicalAtk":27,"adjMinMagicAtk":16,"adjMaxMagicAtk":27,"adjMinPhysicalArmor":4,"adjMaxPhysicalArmor":4,"adjMinMagicArmor":4,"adjMaxMagicArmor":4,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009207: _tools.RODict({
        "propID": 51009207,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":291,"adjMinPhysicalAtk":16,"adjMaxPhysicalAtk":28,"adjMinMagicAtk":16,"adjMaxMagicAtk":28,"adjMinPhysicalArmor":4,"adjMaxPhysicalArmor":4,"adjMinMagicArmor":4,"adjMaxMagicArmor":4,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009208: _tools.RODict({
        "propID": 51009208,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":359,"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":28,"adjMinMagicAtk":17,"adjMaxMagicAtk":28,"adjMinPhysicalArmor":4,"adjMaxPhysicalArmor":4,"adjMinMagicArmor":4,"adjMaxMagicArmor":4,"adjHit":5,"adjDodge":4,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009209: _tools.RODict({
        "propID": 51009209,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":366,"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":28,"adjMinMagicAtk":17,"adjMaxMagicAtk":28,"adjMinPhysicalArmor":5,"adjMaxPhysicalArmor":5,"adjMinMagicArmor":5,"adjMaxMagicArmor":5,"adjHit":5,"adjDodge":4,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009210: _tools.RODict({
        "propID": 51009210,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":374,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":31,"adjMinMagicAtk":20,"adjMaxMagicAtk":31,"adjMinPhysicalArmor":5,"adjMaxPhysicalArmor":5,"adjMinMagicArmor":5,"adjMaxMagicArmor":5,"adjHit":7,"adjDodge":4,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009211: _tools.RODict({
        "propID": 51009211,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":387,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":32,"adjMinMagicAtk":20,"adjMaxMagicAtk":32,"adjMinPhysicalArmor":6,"adjMaxPhysicalArmor":6,"adjMinMagicArmor":6,"adjMaxMagicArmor":6,"adjHit":7,"adjDodge":4,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009212: _tools.RODict({
        "propID": 51009212,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":401,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":32,"adjMinMagicAtk":21,"adjMaxMagicAtk":32,"adjMinPhysicalArmor":6,"adjMaxPhysicalArmor":6,"adjMinMagicArmor":6,"adjMaxMagicArmor":6,"adjHit":7,"adjDodge":4,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009213: _tools.RODict({
        "propID": 51009213,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":414,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":32,"adjMinMagicAtk":21,"adjMaxMagicAtk":32,"adjMinPhysicalArmor":7,"adjMaxPhysicalArmor":7,"adjMinMagicArmor":7,"adjMaxMagicArmor":7,"adjHit":7,"adjDodge":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009214: _tools.RODict({
        "propID": 51009214,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":422,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":32,"adjMinMagicAtk":21,"adjMaxMagicAtk":32,"adjMinPhysicalArmor":7,"adjMaxPhysicalArmor":7,"adjMinMagicArmor":7,"adjMaxMagicArmor":7,"adjHit":7,"adjDodge":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009215: _tools.RODict({
        "propID": 51009215,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":429,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":38,"adjMinMagicAtk":22,"adjMaxMagicAtk":38,"adjMinPhysicalArmor":7,"adjMaxPhysicalArmor":7,"adjMinMagicArmor":7,"adjMaxMagicArmor":7,"adjHit":9,"adjDodge":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009216: _tools.RODict({
        "propID": 51009216,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":443,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":38,"adjMinMagicAtk":23,"adjMaxMagicAtk":38,"adjMinPhysicalArmor":8,"adjMaxPhysicalArmor":8,"adjMinMagicArmor":8,"adjMaxMagicArmor":8,"adjHit":9,"adjDodge":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009217: _tools.RODict({
        "propID": 51009217,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":456,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":38,"adjMinMagicAtk":23,"adjMaxMagicAtk":38,"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjHit":9,"adjDodge":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009218: _tools.RODict({
        "propID": 51009218,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":470,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":38,"adjMinMagicAtk":23,"adjMaxMagicAtk":38,"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjHit":9,"adjDodge":6,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009219: _tools.RODict({
        "propID": 51009219,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":477,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":39,"adjMinMagicAtk":23,"adjMaxMagicAtk":39,"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10,"adjHit":9,"adjDodge":6,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009220: _tools.RODict({
        "propID": 51009220,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":485,"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":42,"adjMinMagicAtk":26,"adjMaxMagicAtk":42,"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10,"adjHit":15,"adjDodge":6,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009221: _tools.RODict({
        "propID": 51009221,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":522,"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":43,"adjMinMagicAtk":26,"adjMaxMagicAtk":43,"adjMinPhysicalArmor":13,"adjMaxPhysicalArmor":13,"adjMinMagicArmor":13,"adjMaxMagicArmor":13,"adjHit":15,"adjDodge":6,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009222: _tools.RODict({
        "propID": 51009222,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":548,"adjMinPhysicalAtk":27,"adjMaxPhysicalAtk":43,"adjMinMagicAtk":27,"adjMaxMagicAtk":43,"adjMinPhysicalArmor":13,"adjMaxPhysicalArmor":13,"adjMinMagicArmor":13,"adjMaxMagicArmor":13,"adjHit":15,"adjDodge":10,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009223: _tools.RODict({
        "propID": 51009223,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":563,"adjMinPhysicalAtk":28,"adjMaxPhysicalAtk":45,"adjMinMagicAtk":28,"adjMaxMagicAtk":45,"adjMinPhysicalArmor":14,"adjMaxPhysicalArmor":14,"adjMinMagicArmor":14,"adjMaxMagicArmor":14,"adjHit":15,"adjDodge":10,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009224: _tools.RODict({
        "propID": 51009224,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":570,"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":47,"adjMinMagicAtk":30,"adjMaxMagicAtk":47,"adjMinPhysicalArmor":14,"adjMaxPhysicalArmor":14,"adjMinMagicArmor":14,"adjMaxMagicArmor":14,"adjHit":15,"adjDodge":10,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009225: _tools.RODict({
        "propID": 51009225,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":596,"adjMinPhysicalAtk":34,"adjMaxPhysicalAtk":55,"adjMinMagicAtk":34,"adjMaxMagicAtk":55,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjHit":18,"adjDodge":10,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009226: _tools.RODict({
        "propID": 51009226,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":615,"adjMinPhysicalAtk":35,"adjMaxPhysicalAtk":55,"adjMinMagicAtk":35,"adjMaxMagicAtk":55,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjHit":18,"adjDodge":12,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009227: _tools.RODict({
        "propID": 51009227,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":623,"adjMinPhysicalAtk":35,"adjMaxPhysicalAtk":55,"adjMinMagicAtk":35,"adjMaxMagicAtk":55,"adjMinPhysicalArmor":17,"adjMaxPhysicalArmor":17,"adjMinMagicArmor":17,"adjMaxMagicArmor":17,"adjHit":18,"adjDodge":12,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009228: _tools.RODict({
        "propID": 51009228,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":630,"adjMinPhysicalAtk":36,"adjMaxPhysicalAtk":57,"adjMinMagicAtk":36,"adjMaxMagicAtk":57,"adjMinPhysicalArmor":17,"adjMaxPhysicalArmor":17,"adjMinMagicArmor":17,"adjMaxMagicArmor":17,"adjHit":18,"adjDodge":12,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009229: _tools.RODict({
        "propID": 51009229,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":656,"adjMinPhysicalAtk":39,"adjMaxPhysicalAtk":64,"adjMinMagicAtk":39,"adjMaxMagicAtk":64,"adjMinPhysicalArmor":18,"adjMaxPhysicalArmor":18,"adjMinMagicArmor":18,"adjMaxMagicArmor":18,"adjHit":21,"adjDodge":12,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009230: _tools.RODict({
        "propID": 51009230,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":675,"adjMinPhysicalAtk":40,"adjMaxPhysicalAtk":65,"adjMinMagicAtk":40,"adjMaxMagicAtk":65,"adjMinPhysicalArmor":19,"adjMaxPhysicalArmor":19,"adjMinMagicArmor":19,"adjMaxMagicArmor":19,"adjHit":21,"adjDodge":14,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009231: _tools.RODict({
        "propID": 51009231,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":683,"adjMinPhysicalAtk":40,"adjMaxPhysicalAtk":67,"adjMinMagicAtk":40,"adjMaxMagicAtk":67,"adjMinPhysicalArmor":19,"adjMaxPhysicalArmor":19,"adjMinMagicArmor":19,"adjMaxMagicArmor":19,"adjHit":21,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5})
    }),
    51009232: _tools.RODict({
        "propID": 51009232,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":690,"adjMinPhysicalAtk":42,"adjMaxPhysicalAtk":70,"adjMinMagicAtk":42,"adjMaxMagicAtk":70,"adjMinPhysicalArmor":19,"adjMaxPhysicalArmor":19,"adjMinMagicArmor":19,"adjMaxMagicArmor":19,"adjHit":22,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":3,"adjMonsterDmgAnti":0.5})
    }),
    51009233: _tools.RODict({
        "propID": 51009233,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":731,"adjMinPhysicalAtk":45,"adjMaxPhysicalAtk":77,"adjMinMagicAtk":45,"adjMaxMagicAtk":77,"adjMinPhysicalArmor":22,"adjMaxPhysicalArmor":22,"adjMinMagicArmor":22,"adjMaxMagicArmor":22,"adjHit":25,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":3,"adjMonsterDmgAnti":0.5})
    }),
    51009234: _tools.RODict({
        "propID": 51009234,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":750,"adjMinPhysicalAtk":46,"adjMaxPhysicalAtk":77,"adjMinMagicAtk":46,"adjMaxMagicAtk":77,"adjMinPhysicalArmor":23,"adjMaxPhysicalArmor":23,"adjMinMagicArmor":23,"adjMaxMagicArmor":23,"adjHit":25,"adjDodge":16,"adjRealDmg":2,"adjRealDmgDef":3,"adjMonsterDmgAnti":0.5})
    }),
    51009235: _tools.RODict({
        "propID": 51009235,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":758,"adjMinPhysicalAtk":46,"adjMaxPhysicalAtk":79,"adjMinMagicAtk":46,"adjMaxMagicAtk":79,"adjMinPhysicalArmor":24,"adjMaxPhysicalArmor":24,"adjMinMagicArmor":24,"adjMaxMagicArmor":24,"adjHit":25,"adjDodge":16,"adjRealDmg":3,"adjRealDmgDef":3,"adjMonsterDmgAnti":0.5})
    }),
    51009236: _tools.RODict({
        "propID": 51009236,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":765,"adjMinPhysicalAtk":47,"adjMaxPhysicalAtk":80,"adjMinMagicAtk":47,"adjMaxMagicAtk":80,"adjMinPhysicalArmor":24,"adjMaxPhysicalArmor":24,"adjMinMagicArmor":24,"adjMaxMagicArmor":24,"adjHit":25,"adjDodge":16,"adjRealDmg":3,"adjRealDmgDef":4,"adjMonsterDmgAnti":0.5})
    }),
    51009237: _tools.RODict({
        "propID": 51009237,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":773,"adjMinPhysicalAtk":50,"adjMaxPhysicalAtk":87,"adjMinMagicAtk":50,"adjMaxMagicAtk":87,"adjMinPhysicalArmor":25,"adjMaxPhysicalArmor":25,"adjMinMagicArmor":25,"adjMaxMagicArmor":25,"adjHit":34,"adjDodge":17,"adjRealDmg":3,"adjRealDmgDef":4,"adjMonsterDmgAnti":0.5})
    }),
    51009238: _tools.RODict({
        "propID": 51009238,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":864,"adjMinPhysicalAtk":51,"adjMaxPhysicalAtk":87,"adjMinMagicAtk":51,"adjMaxMagicAtk":87,"adjMinPhysicalArmor":29,"adjMaxPhysicalArmor":29,"adjMinMagicArmor":29,"adjMaxMagicArmor":29,"adjHit":34,"adjDodge":17,"adjRealDmg":4,"adjRealDmgDef":4,"adjMonsterDmgAnti":0.5})
    }),
    51009239: _tools.RODict({
        "propID": 51009239,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":926,"adjMinPhysicalAtk":51,"adjMaxPhysicalAtk":88,"adjMinMagicAtk":51,"adjMaxMagicAtk":88,"adjMinPhysicalArmor":30,"adjMaxPhysicalArmor":30,"adjMinMagicArmor":30,"adjMaxMagicArmor":30,"adjHit":34,"adjDodge":23,"adjRealDmg":4,"adjRealDmgDef":5,"adjMonsterDmgAnti":0.5})
    }),
    51009240: _tools.RODict({
        "propID": 51009240,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":933,"adjMinPhysicalAtk":54,"adjMaxPhysicalAtk":99,"adjMinMagicAtk":54,"adjMaxMagicAtk":99,"adjMinPhysicalArmor":30,"adjMaxPhysicalArmor":30,"adjMinMagicArmor":30,"adjMaxMagicArmor":30,"adjHit":34,"adjDodge":23,"adjRealDmg":4,"adjRealDmgDef":5,"adjMonsterDmgAnti":0.5})
    }),
    51009241: _tools.RODict({
        "propID": 51009241,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":941,"adjMinPhysicalAtk":63,"adjMaxPhysicalAtk":115,"adjMinMagicAtk":63,"adjMaxMagicAtk":115,"adjMinPhysicalArmor":31,"adjMaxPhysicalArmor":31,"adjMinMagicArmor":31,"adjMaxMagicArmor":31,"adjHit":38,"adjDodge":23,"adjRealDmg":4,"adjRealDmgDef":5,"adjMonsterDmgAnti":0.5})
    }),
    51009242: _tools.RODict({
        "propID": 51009242,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":989,"adjMinPhysicalAtk":64,"adjMaxPhysicalAtk":115,"adjMinMagicAtk":64,"adjMaxMagicAtk":115,"adjMinPhysicalArmor":32,"adjMaxPhysicalArmor":32,"adjMinMagicArmor":32,"adjMaxMagicArmor":32,"adjHit":38,"adjDodge":23,"adjRealDmg":5,"adjRealDmgDef":5,"adjMonsterDmgAnti":0.5})
    }),
    51009243: _tools.RODict({
        "propID": 51009243,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1056,"adjMinPhysicalAtk":64,"adjMaxPhysicalAtk":116,"adjMinMagicAtk":64,"adjMaxMagicAtk":116,"adjMinPhysicalArmor":34,"adjMaxPhysicalArmor":34,"adjMinMagicArmor":34,"adjMaxMagicArmor":34,"adjHit":38,"adjDodge":25,"adjRealDmg":5,"adjRealDmgDef":6,"adjMonsterDmgAnti":0.5})
    }),
    51009244: _tools.RODict({
        "propID": 51009244,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1064,"adjMinPhysicalAtk":65,"adjMaxPhysicalAtk":118,"adjMinMagicAtk":65,"adjMaxMagicAtk":118,"adjMinPhysicalArmor":35,"adjMaxPhysicalArmor":35,"adjMinMagicArmor":35,"adjMaxMagicArmor":35,"adjHit":38,"adjDodge":26,"adjRealDmg":5,"adjRealDmgDef":6,"adjMonsterDmgAnti":0.5})
    }),
    51009245: _tools.RODict({
        "propID": 51009245,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1071,"adjMinPhysicalAtk":65,"adjMaxPhysicalAtk":120,"adjMinMagicAtk":65,"adjMaxMagicAtk":120,"adjMinPhysicalArmor":37,"adjMaxPhysicalArmor":37,"adjMinMagicArmor":37,"adjMaxMagicArmor":37,"adjHit":38,"adjDodge":26,"adjRealDmg":5,"adjRealDmgDef":6,"adjMonsterDmgAnti":0.5})
    }),
    51009246: _tools.RODict({
        "propID": 51009246,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1105,"adjMinPhysicalAtk":71,"adjMaxPhysicalAtk":132,"adjMinMagicAtk":71,"adjMaxMagicAtk":132,"adjMinPhysicalArmor":37,"adjMaxPhysicalArmor":37,"adjMinMagicArmor":37,"adjMaxMagicArmor":37,"adjHit":43,"adjDodge":26,"adjRealDmg":5,"adjRealDmgDef":6,"adjMonsterDmgAnti":0.5})
    }),
    51009247: _tools.RODict({
        "propID": 51009247,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1130,"adjMinPhysicalAtk":71,"adjMaxPhysicalAtk":132,"adjMinMagicAtk":71,"adjMaxMagicAtk":132,"adjMinPhysicalArmor":40,"adjMaxPhysicalArmor":40,"adjMinMagicArmor":40,"adjMaxMagicArmor":40,"adjHit":43,"adjDodge":26,"adjRealDmg":6,"adjRealDmgDef":6,"adjMonsterDmgAnti":0.5})
    }),
    51009248: _tools.RODict({
        "propID": 51009248,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1198,"adjMinPhysicalAtk":71,"adjMaxPhysicalAtk":132,"adjMinMagicAtk":71,"adjMaxMagicAtk":132,"adjMinPhysicalArmor":40,"adjMaxPhysicalArmor":40,"adjMinMagicArmor":40,"adjMaxMagicArmor":40,"adjHit":43,"adjDodge":30,"adjRealDmg":6,"adjRealDmgDef":7,"adjMonsterDmgAnti":0.5})
    }),
    51009249: _tools.RODict({
        "propID": 51009249,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1235,"adjMinPhysicalAtk":74,"adjMaxPhysicalAtk":139,"adjMinMagicAtk":74,"adjMaxMagicAtk":139,"adjMinPhysicalArmor":42,"adjMaxPhysicalArmor":42,"adjMinMagicArmor":42,"adjMaxMagicArmor":42,"adjHit":45,"adjDodge":30,"adjRealDmg":6,"adjRealDmgDef":7,"adjMonsterDmgAnti":0.5})
    }),
    51009250: _tools.RODict({
        "propID": 51009250,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1243,"adjMinPhysicalAtk":75,"adjMaxPhysicalAtk":143,"adjMinMagicAtk":75,"adjMaxMagicAtk":143,"adjMinPhysicalArmor":44,"adjMaxPhysicalArmor":44,"adjMinMagicArmor":44,"adjMaxMagicArmor":44,"adjHit":45,"adjDodge":32,"adjRealDmg":6,"adjRealDmgDef":7,"adjMonsterDmgAnti":0.5})
    }),
    51009251: _tools.RODict({
        "propID": 51009251,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1250,"adjMinPhysicalAtk":81,"adjMaxPhysicalAtk":153,"adjMinMagicAtk":81,"adjMaxMagicAtk":153,"adjMinPhysicalArmor":45,"adjMaxPhysicalArmor":45,"adjMinMagicArmor":45,"adjMaxMagicArmor":45,"adjHit":48,"adjDodge":32,"adjRealDmg":6,"adjRealDmgDef":7,"adjMonsterDmgAnti":0.5})
    }),
    51009252: _tools.RODict({
        "propID": 51009252,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1294,"adjMinPhysicalAtk":84,"adjMaxPhysicalAtk":157,"adjMinMagicAtk":84,"adjMaxMagicAtk":157,"adjMinPhysicalArmor":46,"adjMaxPhysicalArmor":46,"adjMinMagicArmor":46,"adjMaxMagicArmor":46,"adjHit":51,"adjDodge":32,"adjRealDmg":7,"adjRealDmgDef":7,"adjMonsterDmgAnti":0.5})
    }),
    51009253: _tools.RODict({
        "propID": 51009253,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1455,"adjMinPhysicalAtk":84,"adjMaxPhysicalAtk":158,"adjMinMagicAtk":84,"adjMaxMagicAtk":158,"adjMinPhysicalArmor":48,"adjMaxPhysicalArmor":48,"adjMinMagicArmor":48,"adjMaxMagicArmor":48,"adjHit":51,"adjDodge":34,"adjRealDmg":7,"adjRealDmgDef":8,"adjMonsterDmgAnti":0.5})
    }),
    51009254: _tools.RODict({
        "propID": 51009254,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1463,"adjMinPhysicalAtk":85,"adjMaxPhysicalAtk":160,"adjMinMagicAtk":85,"adjMaxMagicAtk":160,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":50,"adjMaxMagicArmor":50,"adjHit":51,"adjDodge":34,"adjRealDmg":7,"adjRealDmgDef":8,"adjMonsterDmgAnti":0.5})
    }),
    51009255: _tools.RODict({
        "propID": 51009255,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1470,"adjMinPhysicalAtk":86,"adjMaxPhysicalAtk":163,"adjMinMagicAtk":86,"adjMaxMagicAtk":163,"adjMinPhysicalArmor":52,"adjMaxPhysicalArmor":52,"adjMinMagicArmor":52,"adjMaxMagicArmor":52,"adjHit":51,"adjDodge":37,"adjRealDmg":7,"adjRealDmgDef":8,"adjMonsterDmgAnti":0.5})
    }),
    51009256: _tools.RODict({
        "propID": 51009256,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1478,"adjMinPhysicalAtk":93,"adjMaxPhysicalAtk":175,"adjMinMagicAtk":93,"adjMaxMagicAtk":175,"adjMinPhysicalArmor":52,"adjMaxPhysicalArmor":52,"adjMinMagicArmor":52,"adjMaxMagicArmor":52,"adjHit":54,"adjDodge":37,"adjRealDmg":7,"adjRealDmgDef":8,"adjMonsterDmgAnti":0.5})
    }),
    51009257: _tools.RODict({
        "propID": 51009257,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1521,"adjMinPhysicalAtk":95,"adjMaxPhysicalAtk":180,"adjMinMagicAtk":95,"adjMaxMagicAtk":180,"adjMinPhysicalArmor":54,"adjMaxPhysicalArmor":54,"adjMinMagicArmor":54,"adjMaxMagicArmor":54,"adjHit":57,"adjDodge":37,"adjRealDmg":8,"adjRealDmgDef":8,"adjMonsterDmgAnti":0.5})
    }),
    51009258: _tools.RODict({
        "propID": 51009258,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1694,"adjMinPhysicalAtk":96,"adjMaxPhysicalAtk":180,"adjMinMagicAtk":96,"adjMaxMagicAtk":180,"adjMinPhysicalArmor":55,"adjMaxPhysicalArmor":55,"adjMinMagicArmor":55,"adjMaxMagicArmor":55,"adjHit":57,"adjDodge":39,"adjRealDmg":8,"adjRealDmgDef":9,"adjMonsterDmgAnti":0.5})
    }),
    51009259: _tools.RODict({
        "propID": 51009259,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1701,"adjMinPhysicalAtk":97,"adjMaxPhysicalAtk":186,"adjMinMagicAtk":97,"adjMaxMagicAtk":186,"adjMinPhysicalArmor":59,"adjMaxPhysicalArmor":59,"adjMinMagicArmor":59,"adjMaxMagicArmor":59,"adjHit":57,"adjDodge":39,"adjRealDmg":8,"adjRealDmgDef":9,"adjMonsterDmgAnti":0.5})
    }),
    51009260: _tools.RODict({
        "propID": 51009260,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1709,"adjMinPhysicalAtk":98,"adjMaxPhysicalAtk":191,"adjMinMagicAtk":98,"adjMaxMagicAtk":191,"adjMinPhysicalArmor":60,"adjMaxPhysicalArmor":60,"adjMinMagicArmor":60,"adjMaxMagicArmor":60,"adjHit":57,"adjDodge":42,"adjRealDmg":8,"adjRealDmgDef":9,"adjMonsterDmgAnti":0.5})
    }),
    51009261: _tools.RODict({
        "propID": 51009261,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1716,"adjMinPhysicalAtk":110,"adjMaxPhysicalAtk":212,"adjMinMagicAtk":110,"adjMaxMagicAtk":212,"adjMinPhysicalArmor":61,"adjMaxPhysicalArmor":61,"adjMinMagicArmor":61,"adjMaxMagicArmor":61,"adjHit":66,"adjDodge":42,"adjRealDmg":8,"adjRealDmgDef":9,"adjMonsterDmgAnti":0.5})
    }),
    51009262: _tools.RODict({
        "propID": 51009262,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1796,"adjMinPhysicalAtk":114,"adjMaxPhysicalAtk":217,"adjMinMagicAtk":114,"adjMaxMagicAtk":217,"adjMinPhysicalArmor":65,"adjMaxPhysicalArmor":65,"adjMinMagicArmor":65,"adjMaxMagicArmor":65,"adjHit":69,"adjDodge":42,"adjRealDmg":10,"adjRealDmgDef":9,"adjMonsterDmgAnti":0.5})
    }),
    51009263: _tools.RODict({
        "propID": 51009263,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2099,"adjMinPhysicalAtk":114,"adjMaxPhysicalAtk":218,"adjMinMagicAtk":114,"adjMaxMagicAtk":218,"adjMinPhysicalArmor":68,"adjMaxPhysicalArmor":68,"adjMinMagicArmor":68,"adjMaxMagicArmor":68,"adjHit":69,"adjDodge":48,"adjRealDmg":10,"adjRealDmgDef":11,"adjMonsterDmgAnti":0.5})
    }),
    51009264: _tools.RODict({
        "propID": 51009264,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2107,"adjMinPhysicalAtk":116,"adjMaxPhysicalAtk":226,"adjMinMagicAtk":116,"adjMaxMagicAtk":226,"adjMinPhysicalArmor":71,"adjMaxPhysicalArmor":71,"adjMinMagicArmor":71,"adjMaxMagicArmor":71,"adjHit":69,"adjDodge":48,"adjRealDmg":10,"adjRealDmgDef":11,"adjMonsterDmgAnti":0.5})
    }),
    51009265: _tools.RODict({
        "propID": 51009265,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2114,"adjMinPhysicalAtk":117,"adjMaxPhysicalAtk":235,"adjMinMagicAtk":117,"adjMaxMagicAtk":235,"adjMinPhysicalArmor":73,"adjMaxPhysicalArmor":73,"adjMinMagicArmor":73,"adjMaxMagicArmor":73,"adjHit":69,"adjDodge":52,"adjRealDmg":10,"adjRealDmgDef":11,"adjMonsterDmgAnti":0.5})
    }),
    51009266: _tools.RODict({
        "propID": 51009266,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2122,"adjMinPhysicalAtk":127,"adjMaxPhysicalAtk":252,"adjMinMagicAtk":127,"adjMaxMagicAtk":252,"adjMinPhysicalArmor":73,"adjMaxPhysicalArmor":73,"adjMinMagicArmor":73,"adjMaxMagicArmor":73,"adjHit":72,"adjDodge":52,"adjRealDmg":10,"adjRealDmgDef":11,"adjMonsterDmgAnti":0.5})
    }),
    51009267: _tools.RODict({
        "propID": 51009267,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2165,"adjMinPhysicalAtk":131,"adjMaxPhysicalAtk":258,"adjMinMagicAtk":131,"adjMaxMagicAtk":258,"adjMinPhysicalArmor":77,"adjMaxPhysicalArmor":77,"adjMinMagicArmor":77,"adjMaxMagicArmor":77,"adjHit":75,"adjDodge":52,"adjRealDmg":12,"adjRealDmgDef":11,"adjMonsterDmgAnti":0.5})
    }),
    51009268: _tools.RODict({
        "propID": 51009268,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2360,"adjMinPhysicalAtk":131,"adjMaxPhysicalAtk":258,"adjMinMagicAtk":131,"adjMaxMagicAtk":258,"adjMinPhysicalArmor":79,"adjMaxPhysicalArmor":79,"adjMinMagicArmor":79,"adjMaxMagicArmor":79,"adjHit":75,"adjDodge":54,"adjRealDmg":12,"adjRealDmgDef":13,"adjMonsterDmgAnti":0.5})
    }),
    51009269: _tools.RODict({
        "propID": 51009269,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2368,"adjMinPhysicalAtk":132,"adjMaxPhysicalAtk":265,"adjMinMagicAtk":132,"adjMaxMagicAtk":265,"adjMinPhysicalArmor":84,"adjMaxPhysicalArmor":84,"adjMinMagicArmor":84,"adjMaxMagicArmor":84,"adjHit":75,"adjDodge":54,"adjRealDmg":12,"adjRealDmgDef":13,"adjMonsterDmgAnti":0.5})
    }),
    51009270: _tools.RODict({
        "propID": 51009270,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2383,"adjMinPhysicalAtk":134,"adjMaxPhysicalAtk":271,"adjMinMagicAtk":134,"adjMaxMagicAtk":271,"adjMinPhysicalArmor":86,"adjMaxPhysicalArmor":86,"adjMinMagicArmor":86,"adjMaxMagicArmor":86,"adjHit":75,"adjDodge":58,"adjRealDmg":12,"adjRealDmgDef":13,"adjMonsterDmgAnti":0.5})
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
    }),
    52120001: _tools.RODict({
        "propID": 52120001,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":32})
    }),
    52120002: _tools.RODict({
        "propID": 52120002,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":64})
    }),
    52120003: _tools.RODict({
        "propID": 52120003,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":96})
    }),
    52120004: _tools.RODict({
        "propID": 52120004,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":128})
    }),
    52120005: _tools.RODict({
        "propID": 52120005,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":160})
    }),
    52120006: _tools.RODict({
        "propID": 52120006,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":192})
    }),
    52120007: _tools.RODict({
        "propID": 52120007,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":224})
    }),
    52120008: _tools.RODict({
        "propID": 52120008,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":256})
    }),
    52120009: _tools.RODict({
        "propID": 52120009,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":288})
    }),
    52120010: _tools.RODict({
        "propID": 52120010,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":320})
    }),
    52120011: _tools.RODict({
        "propID": 52120011,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":352})
    }),
    52120012: _tools.RODict({
        "propID": 52120012,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":384})
    }),
    52120013: _tools.RODict({
        "propID": 52120013,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":416})
    }),
    52120014: _tools.RODict({
        "propID": 52120014,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":448})
    }),
    52120015: _tools.RODict({
        "propID": 52120015,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":480})
    }),
    52120016: _tools.RODict({
        "propID": 52120016,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":528})
    }),
    52120017: _tools.RODict({
        "propID": 52120017,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":576})
    }),
    52120018: _tools.RODict({
        "propID": 52120018,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":624})
    }),
    52120019: _tools.RODict({
        "propID": 52120019,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":672})
    }),
    52120020: _tools.RODict({
        "propID": 52120020,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":720})
    }),
    52120021: _tools.RODict({
        "propID": 52120021,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":768})
    }),
    52120022: _tools.RODict({
        "propID": 52120022,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":816})
    }),
    52120023: _tools.RODict({
        "propID": 52120023,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":864})
    }),
    52120024: _tools.RODict({
        "propID": 52120024,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":912})
    }),
    52120025: _tools.RODict({
        "propID": 52120025,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":960})
    }),
    52120026: _tools.RODict({
        "propID": 52120026,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1008})
    }),
    52120027: _tools.RODict({
        "propID": 52120027,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1056})
    }),
    52120028: _tools.RODict({
        "propID": 52120028,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1104})
    }),
    52120029: _tools.RODict({
        "propID": 52120029,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1152})
    }),
    52120030: _tools.RODict({
        "propID": 52120030,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1200})
    }),
    52120031: _tools.RODict({
        "propID": 52120031,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1264})
    }),
    52120032: _tools.RODict({
        "propID": 52120032,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1328})
    }),
    52120033: _tools.RODict({
        "propID": 52120033,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1392})
    }),
    52120034: _tools.RODict({
        "propID": 52120034,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1456})
    }),
    52120035: _tools.RODict({
        "propID": 52120035,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1520})
    }),
    52120036: _tools.RODict({
        "propID": 52120036,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1584})
    }),
    52120037: _tools.RODict({
        "propID": 52120037,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1648})
    }),
    52120038: _tools.RODict({
        "propID": 52120038,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1712})
    }),
    52120039: _tools.RODict({
        "propID": 52120039,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1776})
    }),
    52120040: _tools.RODict({
        "propID": 52120040,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1840})
    }),
    52120041: _tools.RODict({
        "propID": 52120041,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1904})
    }),
    52120042: _tools.RODict({
        "propID": 52120042,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1968})
    }),
    52120043: _tools.RODict({
        "propID": 52120043,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2032})
    }),
    52120044: _tools.RODict({
        "propID": 52120044,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2096})
    }),
    52120045: _tools.RODict({
        "propID": 52120045,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2160})
    }),
    52120046: _tools.RODict({
        "propID": 52120046,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2240})
    }),
    52120047: _tools.RODict({
        "propID": 52120047,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2320})
    }),
    52120048: _tools.RODict({
        "propID": 52120048,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2400})
    }),
    52120049: _tools.RODict({
        "propID": 52120049,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2480})
    }),
    52120050: _tools.RODict({
        "propID": 52120050,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2560})
    }),
    52120051: _tools.RODict({
        "propID": 52120051,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2640})
    }),
    52120052: _tools.RODict({
        "propID": 52120052,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2720})
    }),
    52120053: _tools.RODict({
        "propID": 52120053,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2800})
    }),
    52120054: _tools.RODict({
        "propID": 52120054,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2880})
    }),
    52120055: _tools.RODict({
        "propID": 52120055,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2960})
    }),
    52120056: _tools.RODict({
        "propID": 52120056,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3040})
    }),
    52120057: _tools.RODict({
        "propID": 52120057,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3120})
    }),
    52120058: _tools.RODict({
        "propID": 52120058,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3200})
    }),
    52120059: _tools.RODict({
        "propID": 52120059,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3280})
    }),
    52120060: _tools.RODict({
        "propID": 52120060,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3360})
    }),
    52120061: _tools.RODict({
        "propID": 52120061,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3456})
    }),
    52120062: _tools.RODict({
        "propID": 52120062,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3552})
    }),
    52120063: _tools.RODict({
        "propID": 52120063,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3648})
    }),
    52120064: _tools.RODict({
        "propID": 52120064,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3744})
    }),
    52120065: _tools.RODict({
        "propID": 52120065,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3840})
    }),
    52120066: _tools.RODict({
        "propID": 52120066,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3936})
    }),
    52120067: _tools.RODict({
        "propID": 52120067,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4032})
    }),
    52120068: _tools.RODict({
        "propID": 52120068,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4128})
    }),
    52120069: _tools.RODict({
        "propID": 52120069,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4224})
    }),
    52120070: _tools.RODict({
        "propID": 52120070,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4320})
    }),
    52120071: _tools.RODict({
        "propID": 52120071,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4416})
    }),
    52120072: _tools.RODict({
        "propID": 52120072,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4512})
    }),
    52120073: _tools.RODict({
        "propID": 52120073,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4608})
    }),
    52120074: _tools.RODict({
        "propID": 52120074,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4704})
    }),
    52120075: _tools.RODict({
        "propID": 52120075,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4800})
    }),
    52120076: _tools.RODict({
        "propID": 52120076,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4912})
    }),
    52120077: _tools.RODict({
        "propID": 52120077,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5024})
    }),
    52120078: _tools.RODict({
        "propID": 52120078,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5136})
    }),
    52120079: _tools.RODict({
        "propID": 52120079,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5248})
    }),
    52120080: _tools.RODict({
        "propID": 52120080,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5360})
    }),
    52120081: _tools.RODict({
        "propID": 52120081,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5472})
    }),
    52120082: _tools.RODict({
        "propID": 52120082,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5584})
    }),
    52120083: _tools.RODict({
        "propID": 52120083,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5696})
    }),
    52120084: _tools.RODict({
        "propID": 52120084,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5808})
    }),
    52120085: _tools.RODict({
        "propID": 52120085,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5920})
    }),
    52120086: _tools.RODict({
        "propID": 52120086,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":6048})
    }),
    52120087: _tools.RODict({
        "propID": 52120087,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":6176})
    }),
    52120088: _tools.RODict({
        "propID": 52120088,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":6304})
    }),
    52120089: _tools.RODict({
        "propID": 52120089,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":6432})
    }),
    52120090: _tools.RODict({
        "propID": 52120090,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":6560})
    }),
    52120091: _tools.RODict({
        "propID": 52120091,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":6704})
    }),
    52120092: _tools.RODict({
        "propID": 52120092,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":6848})
    }),
    52120093: _tools.RODict({
        "propID": 52120093,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":6992})
    }),
    52120094: _tools.RODict({
        "propID": 52120094,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":7136})
    }),
    52120095: _tools.RODict({
        "propID": 52120095,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":7280})
    }),
    52120096: _tools.RODict({
        "propID": 52120096,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":7424})
    }),
    52120097: _tools.RODict({
        "propID": 52120097,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":7568})
    }),
    52120098: _tools.RODict({
        "propID": 52120098,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":7712})
    }),
    52120099: _tools.RODict({
        "propID": 52120099,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":7856})
    }),
    52120100: _tools.RODict({
        "propID": 52120100,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":8000})
    }),
    52120101: _tools.RODict({
        "propID": 52120101,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":5})
    }),
    52120102: _tools.RODict({
        "propID": 52120102,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":10})
    }),
    52120103: _tools.RODict({
        "propID": 52120103,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":15})
    }),
    52120104: _tools.RODict({
        "propID": 52120104,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":20})
    }),
    52120105: _tools.RODict({
        "propID": 52120105,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":26})
    }),
    52120106: _tools.RODict({
        "propID": 52120106,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":31})
    }),
    52120107: _tools.RODict({
        "propID": 52120107,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":36})
    }),
    52120108: _tools.RODict({
        "propID": 52120108,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":41})
    }),
    52120109: _tools.RODict({
        "propID": 52120109,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":46})
    }),
    52120110: _tools.RODict({
        "propID": 52120110,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":51})
    }),
    52120111: _tools.RODict({
        "propID": 52120111,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":56})
    }),
    52120112: _tools.RODict({
        "propID": 52120112,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":61})
    }),
    52120113: _tools.RODict({
        "propID": 52120113,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":67})
    }),
    52120114: _tools.RODict({
        "propID": 52120114,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":72})
    }),
    52120115: _tools.RODict({
        "propID": 52120115,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":77})
    }),
    52120116: _tools.RODict({
        "propID": 52120116,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":84})
    }),
    52120117: _tools.RODict({
        "propID": 52120117,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":92})
    }),
    52120118: _tools.RODict({
        "propID": 52120118,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":100})
    }),
    52120119: _tools.RODict({
        "propID": 52120119,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":108})
    }),
    52120120: _tools.RODict({
        "propID": 52120120,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":115})
    }),
    52120121: _tools.RODict({
        "propID": 52120121,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":123})
    }),
    52120122: _tools.RODict({
        "propID": 52120122,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":131})
    }),
    52120123: _tools.RODict({
        "propID": 52120123,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":138})
    }),
    52120124: _tools.RODict({
        "propID": 52120124,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":146})
    }),
    52120125: _tools.RODict({
        "propID": 52120125,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":154})
    }),
    52120126: _tools.RODict({
        "propID": 52120126,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":161})
    }),
    52120127: _tools.RODict({
        "propID": 52120127,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":169})
    }),
    52120128: _tools.RODict({
        "propID": 52120128,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":177})
    }),
    52120129: _tools.RODict({
        "propID": 52120129,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":184})
    }),
    52120130: _tools.RODict({
        "propID": 52120130,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":192})
    }),
    52120131: _tools.RODict({
        "propID": 52120131,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":202})
    }),
    52120132: _tools.RODict({
        "propID": 52120132,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":212})
    }),
    52120133: _tools.RODict({
        "propID": 52120133,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":223})
    }),
    52120134: _tools.RODict({
        "propID": 52120134,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":233})
    }),
    52120135: _tools.RODict({
        "propID": 52120135,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":243})
    }),
    52120136: _tools.RODict({
        "propID": 52120136,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":253})
    }),
    52120137: _tools.RODict({
        "propID": 52120137,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":264})
    }),
    52120138: _tools.RODict({
        "propID": 52120138,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":274})
    }),
    52120139: _tools.RODict({
        "propID": 52120139,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":284})
    }),
    52120140: _tools.RODict({
        "propID": 52120140,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":294})
    }),
    52120141: _tools.RODict({
        "propID": 52120141,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":305})
    }),
    52120142: _tools.RODict({
        "propID": 52120142,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":315})
    }),
    52120143: _tools.RODict({
        "propID": 52120143,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":325})
    }),
    52120144: _tools.RODict({
        "propID": 52120144,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":335})
    }),
    52120145: _tools.RODict({
        "propID": 52120145,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":346})
    }),
    52120146: _tools.RODict({
        "propID": 52120146,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":358})
    }),
    52120147: _tools.RODict({
        "propID": 52120147,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":371})
    }),
    52120148: _tools.RODict({
        "propID": 52120148,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":384})
    }),
    52120149: _tools.RODict({
        "propID": 52120149,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":397})
    }),
    52120150: _tools.RODict({
        "propID": 52120150,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":410})
    }),
    52120151: _tools.RODict({
        "propID": 52120151,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":422})
    }),
    52120152: _tools.RODict({
        "propID": 52120152,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":435})
    }),
    52120153: _tools.RODict({
        "propID": 52120153,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":448})
    }),
    52120154: _tools.RODict({
        "propID": 52120154,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":461})
    }),
    52120155: _tools.RODict({
        "propID": 52120155,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":474})
    }),
    52120156: _tools.RODict({
        "propID": 52120156,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":486})
    }),
    52120157: _tools.RODict({
        "propID": 52120157,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":499})
    }),
    52120158: _tools.RODict({
        "propID": 52120158,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":512})
    }),
    52120159: _tools.RODict({
        "propID": 52120159,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":525})
    }),
    52120160: _tools.RODict({
        "propID": 52120160,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":538})
    }),
    52120161: _tools.RODict({
        "propID": 52120161,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":553})
    }),
    52120162: _tools.RODict({
        "propID": 52120162,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":568})
    }),
    52120163: _tools.RODict({
        "propID": 52120163,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":584})
    }),
    52120164: _tools.RODict({
        "propID": 52120164,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":599})
    }),
    52120165: _tools.RODict({
        "propID": 52120165,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":614})
    }),
    52120166: _tools.RODict({
        "propID": 52120166,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":630})
    }),
    52120167: _tools.RODict({
        "propID": 52120167,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":645})
    }),
    52120168: _tools.RODict({
        "propID": 52120168,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":660})
    }),
    52120169: _tools.RODict({
        "propID": 52120169,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":676})
    }),
    52120170: _tools.RODict({
        "propID": 52120170,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":691})
    }),
    52120171: _tools.RODict({
        "propID": 52120171,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":707})
    }),
    52120172: _tools.RODict({
        "propID": 52120172,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":722})
    }),
    52120173: _tools.RODict({
        "propID": 52120173,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":737})
    }),
    52120174: _tools.RODict({
        "propID": 52120174,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":753})
    }),
    52120175: _tools.RODict({
        "propID": 52120175,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":768})
    }),
    52120176: _tools.RODict({
        "propID": 52120176,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":786})
    }),
    52120177: _tools.RODict({
        "propID": 52120177,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":804})
    }),
    52120178: _tools.RODict({
        "propID": 52120178,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":822})
    }),
    52120179: _tools.RODict({
        "propID": 52120179,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":840})
    }),
    52120180: _tools.RODict({
        "propID": 52120180,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":858})
    }),
    52120181: _tools.RODict({
        "propID": 52120181,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":876})
    }),
    52120182: _tools.RODict({
        "propID": 52120182,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":893})
    }),
    52120183: _tools.RODict({
        "propID": 52120183,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":911})
    }),
    52120184: _tools.RODict({
        "propID": 52120184,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":929})
    }),
    52120185: _tools.RODict({
        "propID": 52120185,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":947})
    }),
    52120186: _tools.RODict({
        "propID": 52120186,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":968})
    }),
    52120187: _tools.RODict({
        "propID": 52120187,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":988})
    }),
    52120188: _tools.RODict({
        "propID": 52120188,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":1009})
    }),
    52120189: _tools.RODict({
        "propID": 52120189,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":1029})
    }),
    52120190: _tools.RODict({
        "propID": 52120190,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":1050})
    }),
    52120191: _tools.RODict({
        "propID": 52120191,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":1073})
    }),
    52120192: _tools.RODict({
        "propID": 52120192,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":1096})
    }),
    52120193: _tools.RODict({
        "propID": 52120193,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":1119})
    }),
    52120194: _tools.RODict({
        "propID": 52120194,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":1142})
    }),
    52120195: _tools.RODict({
        "propID": 52120195,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":1165})
    }),
    52120196: _tools.RODict({
        "propID": 52120196,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":1188})
    }),
    52120197: _tools.RODict({
        "propID": 52120197,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":1211})
    }),
    52120198: _tools.RODict({
        "propID": 52120198,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":1234})
    }),
    52120199: _tools.RODict({
        "propID": 52120199,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":1257})
    }),
    52120200: _tools.RODict({
        "propID": 52120200,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":1280})
    }),
    52120201: _tools.RODict({
        "propID": 52120201,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":2})
    }),
    52120202: _tools.RODict({
        "propID": 52120202,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":4})
    }),
    52120203: _tools.RODict({
        "propID": 52120203,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":6})
    }),
    52120204: _tools.RODict({
        "propID": 52120204,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":9})
    }),
    52120205: _tools.RODict({
        "propID": 52120205,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":12})
    }),
    52120206: _tools.RODict({
        "propID": 52120206,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":13})
    }),
    52120207: _tools.RODict({
        "propID": 52120207,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":15})
    }),
    52120208: _tools.RODict({
        "propID": 52120208,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":17})
    }),
    52120209: _tools.RODict({
        "propID": 52120209,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":20})
    }),
    52120210: _tools.RODict({
        "propID": 52120210,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":23})
    }),
    52120211: _tools.RODict({
        "propID": 52120211,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":24})
    }),
    52120212: _tools.RODict({
        "propID": 52120212,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":26})
    }),
    52120213: _tools.RODict({
        "propID": 52120213,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":28})
    }),
    52120214: _tools.RODict({
        "propID": 52120214,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":31})
    }),
    52120215: _tools.RODict({
        "propID": 52120215,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":34})
    }),
    52120216: _tools.RODict({
        "propID": 52120216,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":35})
    }),
    52120217: _tools.RODict({
        "propID": 52120217,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":37})
    }),
    52120218: _tools.RODict({
        "propID": 52120218,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":39})
    }),
    52120219: _tools.RODict({
        "propID": 52120219,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":42})
    }),
    52120220: _tools.RODict({
        "propID": 52120220,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":45})
    }),
    52120221: _tools.RODict({
        "propID": 52120221,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":46})
    }),
    52120222: _tools.RODict({
        "propID": 52120222,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":48})
    }),
    52120223: _tools.RODict({
        "propID": 52120223,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":50})
    }),
    52120224: _tools.RODict({
        "propID": 52120224,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":53})
    }),
    52120225: _tools.RODict({
        "propID": 52120225,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":56})
    }),
    52120226: _tools.RODict({
        "propID": 52120226,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":57})
    }),
    52120227: _tools.RODict({
        "propID": 52120227,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":59})
    }),
    52120228: _tools.RODict({
        "propID": 52120228,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":61})
    }),
    52120229: _tools.RODict({
        "propID": 52120229,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":64})
    }),
    52120230: _tools.RODict({
        "propID": 52120230,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":67})
    }),
    52120231: _tools.RODict({
        "propID": 52120231,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":68})
    }),
    52120232: _tools.RODict({
        "propID": 52120232,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":70})
    }),
    52120233: _tools.RODict({
        "propID": 52120233,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":72})
    }),
    52120234: _tools.RODict({
        "propID": 52120234,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":75})
    }),
    52120235: _tools.RODict({
        "propID": 52120235,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":78})
    }),
    52120236: _tools.RODict({
        "propID": 52120236,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":79})
    }),
    52120237: _tools.RODict({
        "propID": 52120237,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":81})
    }),
    52120238: _tools.RODict({
        "propID": 52120238,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":83})
    }),
    52120239: _tools.RODict({
        "propID": 52120239,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":86})
    }),
    52120240: _tools.RODict({
        "propID": 52120240,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":89})
    }),
    52120241: _tools.RODict({
        "propID": 52120241,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":90})
    }),
    52120242: _tools.RODict({
        "propID": 52120242,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":92})
    }),
    52120243: _tools.RODict({
        "propID": 52120243,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":94})
    }),
    52120244: _tools.RODict({
        "propID": 52120244,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":97})
    }),
    52120245: _tools.RODict({
        "propID": 52120245,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":100})
    }),
    52120246: _tools.RODict({
        "propID": 52120246,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":101})
    }),
    52120247: _tools.RODict({
        "propID": 52120247,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":103})
    }),
    52120248: _tools.RODict({
        "propID": 52120248,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":105})
    }),
    52120249: _tools.RODict({
        "propID": 52120249,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":108})
    }),
    52120250: _tools.RODict({
        "propID": 52120250,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":111})
    }),
    52120251: _tools.RODict({
        "propID": 52120251,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":112})
    }),
    52120252: _tools.RODict({
        "propID": 52120252,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":114})
    }),
    52120253: _tools.RODict({
        "propID": 52120253,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":116})
    }),
    52120254: _tools.RODict({
        "propID": 52120254,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":119})
    }),
    52120255: _tools.RODict({
        "propID": 52120255,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":122})
    }),
    52120256: _tools.RODict({
        "propID": 52120256,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":123})
    }),
    52120257: _tools.RODict({
        "propID": 52120257,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":125})
    }),
    52120258: _tools.RODict({
        "propID": 52120258,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":127})
    }),
    52120259: _tools.RODict({
        "propID": 52120259,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":130})
    }),
    52120260: _tools.RODict({
        "propID": 52120260,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":133})
    }),
    52120261: _tools.RODict({
        "propID": 52120261,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":134})
    }),
    52120262: _tools.RODict({
        "propID": 52120262,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":136})
    }),
    52120263: _tools.RODict({
        "propID": 52120263,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":138})
    }),
    52120264: _tools.RODict({
        "propID": 52120264,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":141})
    }),
    52120265: _tools.RODict({
        "propID": 52120265,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":144})
    }),
    52120266: _tools.RODict({
        "propID": 52120266,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":145})
    }),
    52120267: _tools.RODict({
        "propID": 52120267,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":147})
    }),
    52120268: _tools.RODict({
        "propID": 52120268,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":149})
    }),
    52120269: _tools.RODict({
        "propID": 52120269,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":152})
    }),
    52120270: _tools.RODict({
        "propID": 52120270,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":155})
    }),
    52120271: _tools.RODict({
        "propID": 52120271,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":156})
    }),
    52120272: _tools.RODict({
        "propID": 52120272,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":158})
    }),
    52120273: _tools.RODict({
        "propID": 52120273,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":160})
    }),
    52120274: _tools.RODict({
        "propID": 52120274,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":163})
    }),
    52120275: _tools.RODict({
        "propID": 52120275,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":166})
    }),
    52120276: _tools.RODict({
        "propID": 52120276,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":167})
    }),
    52120277: _tools.RODict({
        "propID": 52120277,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":169})
    }),
    52120278: _tools.RODict({
        "propID": 52120278,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":171})
    }),
    52120279: _tools.RODict({
        "propID": 52120279,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":174})
    }),
    52120280: _tools.RODict({
        "propID": 52120280,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":177})
    }),
    52120281: _tools.RODict({
        "propID": 52120281,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":178})
    }),
    52120282: _tools.RODict({
        "propID": 52120282,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":180})
    }),
    52120283: _tools.RODict({
        "propID": 52120283,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":182})
    }),
    52120284: _tools.RODict({
        "propID": 52120284,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":185})
    }),
    52120285: _tools.RODict({
        "propID": 52120285,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":188})
    }),
    52120286: _tools.RODict({
        "propID": 52120286,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":189})
    }),
    52120287: _tools.RODict({
        "propID": 52120287,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":191})
    }),
    52120288: _tools.RODict({
        "propID": 52120288,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":193})
    }),
    52120289: _tools.RODict({
        "propID": 52120289,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":196})
    }),
    52120290: _tools.RODict({
        "propID": 52120290,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":199})
    }),
    52120291: _tools.RODict({
        "propID": 52120291,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":200})
    }),
    52120292: _tools.RODict({
        "propID": 52120292,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":202})
    }),
    52120293: _tools.RODict({
        "propID": 52120293,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":204})
    }),
    52120294: _tools.RODict({
        "propID": 52120294,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":207})
    }),
    52120295: _tools.RODict({
        "propID": 52120295,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":210})
    }),
    52120296: _tools.RODict({
        "propID": 52120296,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":211})
    }),
    52120297: _tools.RODict({
        "propID": 52120297,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":213})
    }),
    52120298: _tools.RODict({
        "propID": 52120298,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":215})
    }),
    52120299: _tools.RODict({
        "propID": 52120299,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":218})
    }),
    52120300: _tools.RODict({
        "propID": 52120300,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":221})
    }),
    52120301: _tools.RODict({
        "propID": 52120301,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":2})
    }),
    52120302: _tools.RODict({
        "propID": 52120302,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":4})
    }),
    52120303: _tools.RODict({
        "propID": 52120303,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":6})
    }),
    52120304: _tools.RODict({
        "propID": 52120304,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":9})
    }),
    52120305: _tools.RODict({
        "propID": 52120305,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":12})
    }),
    52120306: _tools.RODict({
        "propID": 52120306,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":13})
    }),
    52120307: _tools.RODict({
        "propID": 52120307,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":15})
    }),
    52120308: _tools.RODict({
        "propID": 52120308,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":17})
    }),
    52120309: _tools.RODict({
        "propID": 52120309,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":20})
    }),
    52120310: _tools.RODict({
        "propID": 52120310,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":23})
    }),
    52120311: _tools.RODict({
        "propID": 52120311,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":24})
    }),
    52120312: _tools.RODict({
        "propID": 52120312,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":26})
    }),
    52120313: _tools.RODict({
        "propID": 52120313,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":28})
    }),
    52120314: _tools.RODict({
        "propID": 52120314,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":31})
    }),
    52120315: _tools.RODict({
        "propID": 52120315,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":34})
    }),
    52120316: _tools.RODict({
        "propID": 52120316,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":35})
    }),
    52120317: _tools.RODict({
        "propID": 52120317,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":37})
    }),
    52120318: _tools.RODict({
        "propID": 52120318,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":39})
    }),
    52120319: _tools.RODict({
        "propID": 52120319,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":42})
    }),
    52120320: _tools.RODict({
        "propID": 52120320,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":45})
    }),
    52120321: _tools.RODict({
        "propID": 52120321,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":46})
    }),
    52120322: _tools.RODict({
        "propID": 52120322,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":48})
    }),
    52120323: _tools.RODict({
        "propID": 52120323,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":50})
    }),
    52120324: _tools.RODict({
        "propID": 52120324,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":53})
    }),
    52120325: _tools.RODict({
        "propID": 52120325,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":56})
    }),
    52120326: _tools.RODict({
        "propID": 52120326,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":57})
    }),
    52120327: _tools.RODict({
        "propID": 52120327,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":59})
    }),
    52120328: _tools.RODict({
        "propID": 52120328,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":61})
    }),
    52120329: _tools.RODict({
        "propID": 52120329,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":64})
    }),
    52120330: _tools.RODict({
        "propID": 52120330,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":67})
    }),
    52120331: _tools.RODict({
        "propID": 52120331,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":68})
    }),
    52120332: _tools.RODict({
        "propID": 52120332,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":70})
    }),
    52120333: _tools.RODict({
        "propID": 52120333,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":72})
    }),
    52120334: _tools.RODict({
        "propID": 52120334,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":75})
    }),
    52120335: _tools.RODict({
        "propID": 52120335,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":78})
    }),
    52120336: _tools.RODict({
        "propID": 52120336,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":79})
    }),
    52120337: _tools.RODict({
        "propID": 52120337,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":81})
    }),
    52120338: _tools.RODict({
        "propID": 52120338,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":83})
    }),
    52120339: _tools.RODict({
        "propID": 52120339,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":86})
    }),
    52120340: _tools.RODict({
        "propID": 52120340,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":89})
    }),
    52120341: _tools.RODict({
        "propID": 52120341,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":90})
    }),
    52120342: _tools.RODict({
        "propID": 52120342,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":92})
    }),
    52120343: _tools.RODict({
        "propID": 52120343,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":94})
    }),
    52120344: _tools.RODict({
        "propID": 52120344,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":97})
    }),
    52120345: _tools.RODict({
        "propID": 52120345,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":100})
    }),
    52120346: _tools.RODict({
        "propID": 52120346,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":101})
    }),
    52120347: _tools.RODict({
        "propID": 52120347,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":103})
    }),
    52120348: _tools.RODict({
        "propID": 52120348,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":105})
    }),
    52120349: _tools.RODict({
        "propID": 52120349,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":108})
    }),
    52120350: _tools.RODict({
        "propID": 52120350,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":111})
    }),
    52120351: _tools.RODict({
        "propID": 52120351,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":112})
    }),
    52120352: _tools.RODict({
        "propID": 52120352,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":114})
    }),
    52120353: _tools.RODict({
        "propID": 52120353,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":116})
    }),
    52120354: _tools.RODict({
        "propID": 52120354,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":119})
    }),
    52120355: _tools.RODict({
        "propID": 52120355,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":122})
    }),
    52120356: _tools.RODict({
        "propID": 52120356,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":123})
    }),
    52120357: _tools.RODict({
        "propID": 52120357,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":125})
    }),
    52120358: _tools.RODict({
        "propID": 52120358,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":127})
    }),
    52120359: _tools.RODict({
        "propID": 52120359,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":130})
    }),
    52120360: _tools.RODict({
        "propID": 52120360,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":133})
    }),
    52120361: _tools.RODict({
        "propID": 52120361,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":134})
    }),
    52120362: _tools.RODict({
        "propID": 52120362,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":136})
    }),
    52120363: _tools.RODict({
        "propID": 52120363,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":138})
    }),
    52120364: _tools.RODict({
        "propID": 52120364,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":141})
    }),
    52120365: _tools.RODict({
        "propID": 52120365,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":144})
    }),
    52120366: _tools.RODict({
        "propID": 52120366,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":145})
    }),
    52120367: _tools.RODict({
        "propID": 52120367,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":147})
    }),
    52120368: _tools.RODict({
        "propID": 52120368,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":149})
    }),
    52120369: _tools.RODict({
        "propID": 52120369,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":152})
    }),
    52120370: _tools.RODict({
        "propID": 52120370,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":155})
    }),
    52120371: _tools.RODict({
        "propID": 52120371,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":156})
    }),
    52120372: _tools.RODict({
        "propID": 52120372,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":158})
    }),
    52120373: _tools.RODict({
        "propID": 52120373,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":160})
    }),
    52120374: _tools.RODict({
        "propID": 52120374,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":163})
    }),
    52120375: _tools.RODict({
        "propID": 52120375,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":166})
    }),
    52120376: _tools.RODict({
        "propID": 52120376,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":167})
    }),
    52120377: _tools.RODict({
        "propID": 52120377,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":169})
    }),
    52120378: _tools.RODict({
        "propID": 52120378,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":171})
    }),
    52120379: _tools.RODict({
        "propID": 52120379,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":174})
    }),
    52120380: _tools.RODict({
        "propID": 52120380,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":177})
    }),
    52120381: _tools.RODict({
        "propID": 52120381,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":178})
    }),
    52120382: _tools.RODict({
        "propID": 52120382,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":180})
    }),
    52120383: _tools.RODict({
        "propID": 52120383,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":182})
    }),
    52120384: _tools.RODict({
        "propID": 52120384,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":185})
    }),
    52120385: _tools.RODict({
        "propID": 52120385,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":188})
    }),
    52120386: _tools.RODict({
        "propID": 52120386,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":189})
    }),
    52120387: _tools.RODict({
        "propID": 52120387,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":191})
    }),
    52120388: _tools.RODict({
        "propID": 52120388,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":193})
    }),
    52120389: _tools.RODict({
        "propID": 52120389,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":196})
    }),
    52120390: _tools.RODict({
        "propID": 52120390,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":199})
    }),
    52120391: _tools.RODict({
        "propID": 52120391,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":200})
    }),
    52120392: _tools.RODict({
        "propID": 52120392,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":202})
    }),
    52120393: _tools.RODict({
        "propID": 52120393,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":204})
    }),
    52120394: _tools.RODict({
        "propID": 52120394,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":207})
    }),
    52120395: _tools.RODict({
        "propID": 52120395,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":210})
    }),
    52120396: _tools.RODict({
        "propID": 52120396,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":211})
    }),
    52120397: _tools.RODict({
        "propID": 52120397,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":213})
    }),
    52120398: _tools.RODict({
        "propID": 52120398,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":215})
    }),
    52120399: _tools.RODict({
        "propID": 52120399,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":218})
    }),
    52120400: _tools.RODict({
        "propID": 52120400,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicAtk":221})
    }),
    52120401: _tools.RODict({
        "propID": 52120401,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":1})
    }),
    52120402: _tools.RODict({
        "propID": 52120402,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":2})
    }),
    52120403: _tools.RODict({
        "propID": 52120403,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":3})
    }),
    52120404: _tools.RODict({
        "propID": 52120404,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":4})
    }),
    52120405: _tools.RODict({
        "propID": 52120405,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":5})
    }),
    52120406: _tools.RODict({
        "propID": 52120406,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":6})
    }),
    52120407: _tools.RODict({
        "propID": 52120407,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":7})
    }),
    52120408: _tools.RODict({
        "propID": 52120408,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":8})
    }),
    52120409: _tools.RODict({
        "propID": 52120409,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":9})
    }),
    52120410: _tools.RODict({
        "propID": 52120410,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":10})
    }),
    52120411: _tools.RODict({
        "propID": 52120411,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":11})
    }),
    52120412: _tools.RODict({
        "propID": 52120412,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":12})
    }),
    52120413: _tools.RODict({
        "propID": 52120413,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":13})
    }),
    52120414: _tools.RODict({
        "propID": 52120414,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":14})
    }),
    52120415: _tools.RODict({
        "propID": 52120415,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":15})
    }),
    52120416: _tools.RODict({
        "propID": 52120416,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":16})
    }),
    52120417: _tools.RODict({
        "propID": 52120417,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":17})
    }),
    52120418: _tools.RODict({
        "propID": 52120418,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":18})
    }),
    52120419: _tools.RODict({
        "propID": 52120419,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":19})
    }),
    52120420: _tools.RODict({
        "propID": 52120420,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":20})
    }),
    52120421: _tools.RODict({
        "propID": 52120421,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":21})
    }),
    52120422: _tools.RODict({
        "propID": 52120422,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":22})
    }),
    52120423: _tools.RODict({
        "propID": 52120423,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":23})
    }),
    52120424: _tools.RODict({
        "propID": 52120424,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":24})
    }),
    52120425: _tools.RODict({
        "propID": 52120425,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":25})
    }),
    52120426: _tools.RODict({
        "propID": 52120426,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":26})
    }),
    52120427: _tools.RODict({
        "propID": 52120427,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":27})
    }),
    52120428: _tools.RODict({
        "propID": 52120428,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":28})
    }),
    52120429: _tools.RODict({
        "propID": 52120429,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":29})
    }),
    52120430: _tools.RODict({
        "propID": 52120430,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":30})
    }),
    52120431: _tools.RODict({
        "propID": 52120431,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":31})
    }),
    52120432: _tools.RODict({
        "propID": 52120432,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":32})
    }),
    52120433: _tools.RODict({
        "propID": 52120433,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":33})
    }),
    52120434: _tools.RODict({
        "propID": 52120434,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":34})
    }),
    52120435: _tools.RODict({
        "propID": 52120435,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":35})
    }),
    52120436: _tools.RODict({
        "propID": 52120436,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":36})
    }),
    52120437: _tools.RODict({
        "propID": 52120437,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":37})
    }),
    52120438: _tools.RODict({
        "propID": 52120438,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":38})
    }),
    52120439: _tools.RODict({
        "propID": 52120439,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":39})
    }),
    52120440: _tools.RODict({
        "propID": 52120440,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":40})
    }),
    52120441: _tools.RODict({
        "propID": 52120441,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":41})
    }),
    52120442: _tools.RODict({
        "propID": 52120442,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":42})
    }),
    52120443: _tools.RODict({
        "propID": 52120443,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":43})
    }),
    52120444: _tools.RODict({
        "propID": 52120444,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":44})
    }),
    52120445: _tools.RODict({
        "propID": 52120445,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":45})
    }),
    52120446: _tools.RODict({
        "propID": 52120446,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":46})
    }),
    52120447: _tools.RODict({
        "propID": 52120447,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":47})
    }),
    52120448: _tools.RODict({
        "propID": 52120448,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":48})
    }),
    52120449: _tools.RODict({
        "propID": 52120449,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":49})
    }),
    52120450: _tools.RODict({
        "propID": 52120450,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":50})
    }),
    52120451: _tools.RODict({
        "propID": 52120451,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":51})
    }),
    52120452: _tools.RODict({
        "propID": 52120452,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":52})
    }),
    52120453: _tools.RODict({
        "propID": 52120453,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":53})
    }),
    52120454: _tools.RODict({
        "propID": 52120454,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":54})
    }),
    52120455: _tools.RODict({
        "propID": 52120455,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":55})
    }),
    52120456: _tools.RODict({
        "propID": 52120456,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":56})
    }),
    52120457: _tools.RODict({
        "propID": 52120457,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":57})
    }),
    52120458: _tools.RODict({
        "propID": 52120458,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":58})
    }),
    52120459: _tools.RODict({
        "propID": 52120459,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":59})
    }),
    52120460: _tools.RODict({
        "propID": 52120460,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":60})
    }),
    52120461: _tools.RODict({
        "propID": 52120461,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":61})
    }),
    52120462: _tools.RODict({
        "propID": 52120462,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":62})
    }),
    52120463: _tools.RODict({
        "propID": 52120463,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":63})
    }),
    52120464: _tools.RODict({
        "propID": 52120464,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":64})
    }),
    52120465: _tools.RODict({
        "propID": 52120465,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":65})
    }),
    52120466: _tools.RODict({
        "propID": 52120466,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":66})
    }),
    52120467: _tools.RODict({
        "propID": 52120467,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":67})
    }),
    52120468: _tools.RODict({
        "propID": 52120468,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":68})
    }),
    52120469: _tools.RODict({
        "propID": 52120469,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":69})
    }),
    52120470: _tools.RODict({
        "propID": 52120470,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":70})
    }),
    52120471: _tools.RODict({
        "propID": 52120471,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":71})
    }),
    52120472: _tools.RODict({
        "propID": 52120472,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":72})
    }),
    52120473: _tools.RODict({
        "propID": 52120473,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":73})
    }),
    52120474: _tools.RODict({
        "propID": 52120474,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":74})
    }),
    52120475: _tools.RODict({
        "propID": 52120475,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":75})
    }),
    52120476: _tools.RODict({
        "propID": 52120476,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":76})
    }),
    52120477: _tools.RODict({
        "propID": 52120477,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":77})
    }),
    52120478: _tools.RODict({
        "propID": 52120478,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":78})
    }),
    52120479: _tools.RODict({
        "propID": 52120479,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":79})
    }),
    52120480: _tools.RODict({
        "propID": 52120480,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":80})
    }),
    52120481: _tools.RODict({
        "propID": 52120481,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":81})
    }),
    52120482: _tools.RODict({
        "propID": 52120482,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":82})
    }),
    52120483: _tools.RODict({
        "propID": 52120483,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":83})
    }),
    52120484: _tools.RODict({
        "propID": 52120484,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":84})
    }),
    52120485: _tools.RODict({
        "propID": 52120485,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":85})
    }),
    52120486: _tools.RODict({
        "propID": 52120486,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":86})
    }),
    52120487: _tools.RODict({
        "propID": 52120487,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":87})
    }),
    52120488: _tools.RODict({
        "propID": 52120488,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":88})
    }),
    52120489: _tools.RODict({
        "propID": 52120489,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":89})
    }),
    52120490: _tools.RODict({
        "propID": 52120490,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":90})
    }),
    52120491: _tools.RODict({
        "propID": 52120491,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":91})
    }),
    52120492: _tools.RODict({
        "propID": 52120492,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":92})
    }),
    52120493: _tools.RODict({
        "propID": 52120493,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":93})
    }),
    52120494: _tools.RODict({
        "propID": 52120494,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":94})
    }),
    52120495: _tools.RODict({
        "propID": 52120495,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":95})
    }),
    52120496: _tools.RODict({
        "propID": 52120496,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":96})
    }),
    52120497: _tools.RODict({
        "propID": 52120497,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":97})
    }),
    52120498: _tools.RODict({
        "propID": 52120498,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":98})
    }),
    52120499: _tools.RODict({
        "propID": 52120499,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":99})
    }),
    52120500: _tools.RODict({
        "propID": 52120500,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":100})
    }),
    52120501: _tools.RODict({
        "propID": 52120501,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":1})
    }),
    52120502: _tools.RODict({
        "propID": 52120502,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":2})
    }),
    52120503: _tools.RODict({
        "propID": 52120503,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":3})
    }),
    52120504: _tools.RODict({
        "propID": 52120504,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":4})
    }),
    52120505: _tools.RODict({
        "propID": 52120505,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":5})
    }),
    52120506: _tools.RODict({
        "propID": 52120506,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":6})
    }),
    52120507: _tools.RODict({
        "propID": 52120507,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":7})
    }),
    52120508: _tools.RODict({
        "propID": 52120508,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":8})
    }),
    52120509: _tools.RODict({
        "propID": 52120509,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":9})
    }),
    52120510: _tools.RODict({
        "propID": 52120510,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":10})
    }),
    52120511: _tools.RODict({
        "propID": 52120511,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":11})
    }),
    52120512: _tools.RODict({
        "propID": 52120512,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":12})
    }),
    52120513: _tools.RODict({
        "propID": 52120513,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":13})
    }),
    52120514: _tools.RODict({
        "propID": 52120514,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":14})
    }),
    52120515: _tools.RODict({
        "propID": 52120515,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":15})
    }),
    52120516: _tools.RODict({
        "propID": 52120516,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":16})
    }),
    52120517: _tools.RODict({
        "propID": 52120517,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":17})
    }),
    52120518: _tools.RODict({
        "propID": 52120518,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":18})
    }),
    52120519: _tools.RODict({
        "propID": 52120519,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":19})
    }),
    52120520: _tools.RODict({
        "propID": 52120520,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":20})
    }),
    52120521: _tools.RODict({
        "propID": 52120521,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":21})
    }),
    52120522: _tools.RODict({
        "propID": 52120522,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":22})
    }),
    52120523: _tools.RODict({
        "propID": 52120523,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":23})
    }),
    52120524: _tools.RODict({
        "propID": 52120524,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":24})
    }),
    52120525: _tools.RODict({
        "propID": 52120525,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":25})
    }),
    52120526: _tools.RODict({
        "propID": 52120526,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":26})
    }),
    52120527: _tools.RODict({
        "propID": 52120527,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":27})
    }),
    52120528: _tools.RODict({
        "propID": 52120528,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":28})
    }),
    52120529: _tools.RODict({
        "propID": 52120529,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":29})
    }),
    52120530: _tools.RODict({
        "propID": 52120530,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":30})
    }),
    52120531: _tools.RODict({
        "propID": 52120531,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":31})
    }),
    52120532: _tools.RODict({
        "propID": 52120532,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":32})
    }),
    52120533: _tools.RODict({
        "propID": 52120533,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":33})
    }),
    52120534: _tools.RODict({
        "propID": 52120534,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":34})
    }),
    52120535: _tools.RODict({
        "propID": 52120535,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":35})
    }),
    52120536: _tools.RODict({
        "propID": 52120536,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":36})
    }),
    52120537: _tools.RODict({
        "propID": 52120537,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":37})
    }),
    52120538: _tools.RODict({
        "propID": 52120538,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":38})
    }),
    52120539: _tools.RODict({
        "propID": 52120539,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":39})
    }),
    52120540: _tools.RODict({
        "propID": 52120540,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":40})
    }),
    52120541: _tools.RODict({
        "propID": 52120541,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":41})
    }),
    52120542: _tools.RODict({
        "propID": 52120542,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":42})
    }),
    52120543: _tools.RODict({
        "propID": 52120543,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":43})
    }),
    52120544: _tools.RODict({
        "propID": 52120544,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":44})
    }),
    52120545: _tools.RODict({
        "propID": 52120545,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":45})
    }),
    52120546: _tools.RODict({
        "propID": 52120546,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":46})
    }),
    52120547: _tools.RODict({
        "propID": 52120547,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":47})
    }),
    52120548: _tools.RODict({
        "propID": 52120548,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":48})
    }),
    52120549: _tools.RODict({
        "propID": 52120549,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":49})
    }),
    52120550: _tools.RODict({
        "propID": 52120550,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":50})
    }),
    52120551: _tools.RODict({
        "propID": 52120551,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":51})
    }),
    52120552: _tools.RODict({
        "propID": 52120552,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":52})
    }),
    52120553: _tools.RODict({
        "propID": 52120553,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":53})
    }),
    52120554: _tools.RODict({
        "propID": 52120554,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":54})
    }),
    52120555: _tools.RODict({
        "propID": 52120555,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":55})
    }),
    52120556: _tools.RODict({
        "propID": 52120556,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":56})
    }),
    52120557: _tools.RODict({
        "propID": 52120557,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":57})
    }),
    52120558: _tools.RODict({
        "propID": 52120558,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":58})
    }),
    52120559: _tools.RODict({
        "propID": 52120559,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":59})
    }),
    52120560: _tools.RODict({
        "propID": 52120560,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":60})
    }),
    52120561: _tools.RODict({
        "propID": 52120561,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":61})
    }),
    52120562: _tools.RODict({
        "propID": 52120562,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":62})
    }),
    52120563: _tools.RODict({
        "propID": 52120563,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":63})
    }),
    52120564: _tools.RODict({
        "propID": 52120564,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":64})
    }),
    52120565: _tools.RODict({
        "propID": 52120565,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":65})
    }),
    52120566: _tools.RODict({
        "propID": 52120566,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":66})
    }),
    52120567: _tools.RODict({
        "propID": 52120567,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":67})
    }),
    52120568: _tools.RODict({
        "propID": 52120568,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":68})
    }),
    52120569: _tools.RODict({
        "propID": 52120569,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":69})
    }),
    52120570: _tools.RODict({
        "propID": 52120570,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":70})
    }),
    52120571: _tools.RODict({
        "propID": 52120571,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":71})
    }),
    52120572: _tools.RODict({
        "propID": 52120572,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":72})
    }),
    52120573: _tools.RODict({
        "propID": 52120573,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":73})
    }),
    52120574: _tools.RODict({
        "propID": 52120574,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":74})
    }),
    52120575: _tools.RODict({
        "propID": 52120575,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":75})
    }),
    52120576: _tools.RODict({
        "propID": 52120576,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":76})
    }),
    52120577: _tools.RODict({
        "propID": 52120577,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":77})
    }),
    52120578: _tools.RODict({
        "propID": 52120578,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":78})
    }),
    52120579: _tools.RODict({
        "propID": 52120579,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":79})
    }),
    52120580: _tools.RODict({
        "propID": 52120580,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":80})
    }),
    52120581: _tools.RODict({
        "propID": 52120581,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":81})
    }),
    52120582: _tools.RODict({
        "propID": 52120582,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":82})
    }),
    52120583: _tools.RODict({
        "propID": 52120583,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":83})
    }),
    52120584: _tools.RODict({
        "propID": 52120584,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":84})
    }),
    52120585: _tools.RODict({
        "propID": 52120585,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":85})
    }),
    52120586: _tools.RODict({
        "propID": 52120586,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":86})
    }),
    52120587: _tools.RODict({
        "propID": 52120587,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":87})
    }),
    52120588: _tools.RODict({
        "propID": 52120588,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":88})
    }),
    52120589: _tools.RODict({
        "propID": 52120589,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":89})
    }),
    52120590: _tools.RODict({
        "propID": 52120590,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":90})
    }),
    52120591: _tools.RODict({
        "propID": 52120591,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":91})
    }),
    52120592: _tools.RODict({
        "propID": 52120592,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":92})
    }),
    52120593: _tools.RODict({
        "propID": 52120593,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":93})
    }),
    52120594: _tools.RODict({
        "propID": 52120594,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":94})
    }),
    52120595: _tools.RODict({
        "propID": 52120595,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":95})
    }),
    52120596: _tools.RODict({
        "propID": 52120596,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":96})
    }),
    52120597: _tools.RODict({
        "propID": 52120597,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":97})
    }),
    52120598: _tools.RODict({
        "propID": 52120598,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":98})
    }),
    52120599: _tools.RODict({
        "propID": 52120599,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":99})
    }),
    52120600: _tools.RODict({
        "propID": 52120600,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":100})
    }),
    52120601: _tools.RODict({
        "propID": 52120601,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":2})
    }),
    52120602: _tools.RODict({
        "propID": 52120602,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":5})
    }),
    52120603: _tools.RODict({
        "propID": 52120603,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":8})
    }),
    52120604: _tools.RODict({
        "propID": 52120604,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":11})
    }),
    52120605: _tools.RODict({
        "propID": 52120605,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":14})
    }),
    52120606: _tools.RODict({
        "propID": 52120606,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":17})
    }),
    52120607: _tools.RODict({
        "propID": 52120607,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":20})
    }),
    52120608: _tools.RODict({
        "propID": 52120608,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":23})
    }),
    52120609: _tools.RODict({
        "propID": 52120609,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":26})
    }),
    52120610: _tools.RODict({
        "propID": 52120610,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":29})
    }),
    52120611: _tools.RODict({
        "propID": 52120611,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":32})
    }),
    52120612: _tools.RODict({
        "propID": 52120612,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":35})
    }),
    52120613: _tools.RODict({
        "propID": 52120613,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":38})
    }),
    52120614: _tools.RODict({
        "propID": 52120614,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":41})
    }),
    52120615: _tools.RODict({
        "propID": 52120615,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":44})
    }),
    52120616: _tools.RODict({
        "propID": 52120616,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":47})
    }),
    52120617: _tools.RODict({
        "propID": 52120617,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":50})
    }),
    52120618: _tools.RODict({
        "propID": 52120618,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":53})
    }),
    52120619: _tools.RODict({
        "propID": 52120619,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":56})
    }),
    52120620: _tools.RODict({
        "propID": 52120620,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":59})
    }),
    52120621: _tools.RODict({
        "propID": 52120621,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":62})
    }),
    52120622: _tools.RODict({
        "propID": 52120622,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":65})
    }),
    52120623: _tools.RODict({
        "propID": 52120623,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":68})
    }),
    52120624: _tools.RODict({
        "propID": 52120624,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":71})
    }),
    52120625: _tools.RODict({
        "propID": 52120625,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":74})
    }),
    52120626: _tools.RODict({
        "propID": 52120626,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":77})
    }),
    52120627: _tools.RODict({
        "propID": 52120627,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":80})
    }),
    52120628: _tools.RODict({
        "propID": 52120628,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":83})
    }),
    52120629: _tools.RODict({
        "propID": 52120629,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":86})
    }),
    52120630: _tools.RODict({
        "propID": 52120630,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":89})
    }),
    52120631: _tools.RODict({
        "propID": 52120631,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":92})
    }),
    52120632: _tools.RODict({
        "propID": 52120632,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":95})
    }),
    52120633: _tools.RODict({
        "propID": 52120633,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":98})
    }),
    52120634: _tools.RODict({
        "propID": 52120634,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":101})
    }),
    52120635: _tools.RODict({
        "propID": 52120635,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":104})
    }),
    52120636: _tools.RODict({
        "propID": 52120636,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":107})
    }),
    52120637: _tools.RODict({
        "propID": 52120637,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":110})
    }),
    52120638: _tools.RODict({
        "propID": 52120638,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":113})
    }),
    52120639: _tools.RODict({
        "propID": 52120639,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":116})
    }),
    52120640: _tools.RODict({
        "propID": 52120640,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":119})
    }),
    52120641: _tools.RODict({
        "propID": 52120641,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":122})
    }),
    52120642: _tools.RODict({
        "propID": 52120642,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":125})
    }),
    52120643: _tools.RODict({
        "propID": 52120643,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":128})
    }),
    52120644: _tools.RODict({
        "propID": 52120644,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":131})
    }),
    52120645: _tools.RODict({
        "propID": 52120645,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":134})
    }),
    52120646: _tools.RODict({
        "propID": 52120646,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":137})
    }),
    52120647: _tools.RODict({
        "propID": 52120647,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":140})
    }),
    52120648: _tools.RODict({
        "propID": 52120648,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":143})
    }),
    52120649: _tools.RODict({
        "propID": 52120649,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":146})
    }),
    52120650: _tools.RODict({
        "propID": 52120650,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":149})
    }),
    52120651: _tools.RODict({
        "propID": 52120651,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":152})
    }),
    52120652: _tools.RODict({
        "propID": 52120652,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":155})
    }),
    52120653: _tools.RODict({
        "propID": 52120653,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":158})
    }),
    52120654: _tools.RODict({
        "propID": 52120654,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":161})
    }),
    52120655: _tools.RODict({
        "propID": 52120655,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":164})
    }),
    52120656: _tools.RODict({
        "propID": 52120656,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":167})
    }),
    52120657: _tools.RODict({
        "propID": 52120657,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":170})
    }),
    52120658: _tools.RODict({
        "propID": 52120658,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":173})
    }),
    52120659: _tools.RODict({
        "propID": 52120659,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":176})
    }),
    52120660: _tools.RODict({
        "propID": 52120660,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":179})
    }),
    52120661: _tools.RODict({
        "propID": 52120661,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":182})
    }),
    52120662: _tools.RODict({
        "propID": 52120662,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":185})
    }),
    52120663: _tools.RODict({
        "propID": 52120663,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":188})
    }),
    52120664: _tools.RODict({
        "propID": 52120664,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":191})
    }),
    52120665: _tools.RODict({
        "propID": 52120665,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":194})
    }),
    52120666: _tools.RODict({
        "propID": 52120666,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":197})
    }),
    52120667: _tools.RODict({
        "propID": 52120667,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":200})
    }),
    52120668: _tools.RODict({
        "propID": 52120668,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":203})
    }),
    52120669: _tools.RODict({
        "propID": 52120669,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":206})
    }),
    52120670: _tools.RODict({
        "propID": 52120670,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":209})
    }),
    52120671: _tools.RODict({
        "propID": 52120671,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":212})
    }),
    52120672: _tools.RODict({
        "propID": 52120672,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":215})
    }),
    52120673: _tools.RODict({
        "propID": 52120673,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":218})
    }),
    52120674: _tools.RODict({
        "propID": 52120674,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":221})
    }),
    52120675: _tools.RODict({
        "propID": 52120675,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":224})
    }),
    52120676: _tools.RODict({
        "propID": 52120676,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":227})
    }),
    52120677: _tools.RODict({
        "propID": 52120677,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":230})
    }),
    52120678: _tools.RODict({
        "propID": 52120678,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":233})
    }),
    52120679: _tools.RODict({
        "propID": 52120679,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":236})
    }),
    52120680: _tools.RODict({
        "propID": 52120680,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":239})
    }),
    52120681: _tools.RODict({
        "propID": 52120681,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":242})
    }),
    52120682: _tools.RODict({
        "propID": 52120682,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":245})
    }),
    52120683: _tools.RODict({
        "propID": 52120683,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":248})
    }),
    52120684: _tools.RODict({
        "propID": 52120684,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":251})
    }),
    52120685: _tools.RODict({
        "propID": 52120685,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":254})
    }),
    52120686: _tools.RODict({
        "propID": 52120686,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":257})
    }),
    52120687: _tools.RODict({
        "propID": 52120687,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":260})
    }),
    52120688: _tools.RODict({
        "propID": 52120688,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":263})
    }),
    52120689: _tools.RODict({
        "propID": 52120689,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":266})
    }),
    52120690: _tools.RODict({
        "propID": 52120690,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":269})
    }),
    52120691: _tools.RODict({
        "propID": 52120691,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":272})
    }),
    52120692: _tools.RODict({
        "propID": 52120692,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":275})
    }),
    52120693: _tools.RODict({
        "propID": 52120693,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":278})
    }),
    52120694: _tools.RODict({
        "propID": 52120694,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":281})
    }),
    52120695: _tools.RODict({
        "propID": 52120695,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":284})
    }),
    52120696: _tools.RODict({
        "propID": 52120696,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":287})
    }),
    52120697: _tools.RODict({
        "propID": 52120697,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":290})
    }),
    52120698: _tools.RODict({
        "propID": 52120698,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":293})
    }),
    52120699: _tools.RODict({
        "propID": 52120699,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":296})
    }),
    52120700: _tools.RODict({
        "propID": 52120700,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalArmor":299})
    }),
    52120701: _tools.RODict({
        "propID": 52120701,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":1})
    }),
    52120702: _tools.RODict({
        "propID": 52120702,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":2})
    }),
    52120703: _tools.RODict({
        "propID": 52120703,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":3})
    }),
    52120704: _tools.RODict({
        "propID": 52120704,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":5})
    }),
    52120705: _tools.RODict({
        "propID": 52120705,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":7})
    }),
    52120706: _tools.RODict({
        "propID": 52120706,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":8})
    }),
    52120707: _tools.RODict({
        "propID": 52120707,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":9})
    }),
    52120708: _tools.RODict({
        "propID": 52120708,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":10})
    }),
    52120709: _tools.RODict({
        "propID": 52120709,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":12})
    }),
    52120710: _tools.RODict({
        "propID": 52120710,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":14})
    }),
    52120711: _tools.RODict({
        "propID": 52120711,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":15})
    }),
    52120712: _tools.RODict({
        "propID": 52120712,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":16})
    }),
    52120713: _tools.RODict({
        "propID": 52120713,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":17})
    }),
    52120714: _tools.RODict({
        "propID": 52120714,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":19})
    }),
    52120715: _tools.RODict({
        "propID": 52120715,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":21})
    }),
    52120716: _tools.RODict({
        "propID": 52120716,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":22})
    }),
    52120717: _tools.RODict({
        "propID": 52120717,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":23})
    }),
    52120718: _tools.RODict({
        "propID": 52120718,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":24})
    }),
    52120719: _tools.RODict({
        "propID": 52120719,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":26})
    }),
    52120720: _tools.RODict({
        "propID": 52120720,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":28})
    }),
    52120721: _tools.RODict({
        "propID": 52120721,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":29})
    }),
    52120722: _tools.RODict({
        "propID": 52120722,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":30})
    }),
    52120723: _tools.RODict({
        "propID": 52120723,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":31})
    }),
    52120724: _tools.RODict({
        "propID": 52120724,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":33})
    }),
    52120725: _tools.RODict({
        "propID": 52120725,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":35})
    }),
    52120726: _tools.RODict({
        "propID": 52120726,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":36})
    }),
    52120727: _tools.RODict({
        "propID": 52120727,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":37})
    }),
    52120728: _tools.RODict({
        "propID": 52120728,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":38})
    }),
    52120729: _tools.RODict({
        "propID": 52120729,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":40})
    }),
    52120730: _tools.RODict({
        "propID": 52120730,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":42})
    }),
    52120731: _tools.RODict({
        "propID": 52120731,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":43})
    }),
    52120732: _tools.RODict({
        "propID": 52120732,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":44})
    }),
    52120733: _tools.RODict({
        "propID": 52120733,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":45})
    }),
    52120734: _tools.RODict({
        "propID": 52120734,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":47})
    }),
    52120735: _tools.RODict({
        "propID": 52120735,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":49})
    }),
    52120736: _tools.RODict({
        "propID": 52120736,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":50})
    }),
    52120737: _tools.RODict({
        "propID": 52120737,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":51})
    }),
    52120738: _tools.RODict({
        "propID": 52120738,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":52})
    }),
    52120739: _tools.RODict({
        "propID": 52120739,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":54})
    }),
    52120740: _tools.RODict({
        "propID": 52120740,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":56})
    }),
    52120741: _tools.RODict({
        "propID": 52120741,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":57})
    }),
    52120742: _tools.RODict({
        "propID": 52120742,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":58})
    }),
    52120743: _tools.RODict({
        "propID": 52120743,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":59})
    }),
    52120744: _tools.RODict({
        "propID": 52120744,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":61})
    }),
    52120745: _tools.RODict({
        "propID": 52120745,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":63})
    }),
    52120746: _tools.RODict({
        "propID": 52120746,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":64})
    }),
    52120747: _tools.RODict({
        "propID": 52120747,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":65})
    }),
    52120748: _tools.RODict({
        "propID": 52120748,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":66})
    }),
    52120749: _tools.RODict({
        "propID": 52120749,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":68})
    }),
    52120750: _tools.RODict({
        "propID": 52120750,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":70})
    }),
    52120751: _tools.RODict({
        "propID": 52120751,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":71})
    }),
    52120752: _tools.RODict({
        "propID": 52120752,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":72})
    }),
    52120753: _tools.RODict({
        "propID": 52120753,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":73})
    }),
    52120754: _tools.RODict({
        "propID": 52120754,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":75})
    }),
    52120755: _tools.RODict({
        "propID": 52120755,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":77})
    }),
    52120756: _tools.RODict({
        "propID": 52120756,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":78})
    }),
    52120757: _tools.RODict({
        "propID": 52120757,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":79})
    }),
    52120758: _tools.RODict({
        "propID": 52120758,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":80})
    }),
    52120759: _tools.RODict({
        "propID": 52120759,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":82})
    }),
    52120760: _tools.RODict({
        "propID": 52120760,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":84})
    }),
    52120761: _tools.RODict({
        "propID": 52120761,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":85})
    }),
    52120762: _tools.RODict({
        "propID": 52120762,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":86})
    }),
    52120763: _tools.RODict({
        "propID": 52120763,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":87})
    }),
    52120764: _tools.RODict({
        "propID": 52120764,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":89})
    }),
    52120765: _tools.RODict({
        "propID": 52120765,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":91})
    }),
    52120766: _tools.RODict({
        "propID": 52120766,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":92})
    }),
    52120767: _tools.RODict({
        "propID": 52120767,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":93})
    }),
    52120768: _tools.RODict({
        "propID": 52120768,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":94})
    }),
    52120769: _tools.RODict({
        "propID": 52120769,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":96})
    }),
    52120770: _tools.RODict({
        "propID": 52120770,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":98})
    }),
    52120771: _tools.RODict({
        "propID": 52120771,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":99})
    }),
    52120772: _tools.RODict({
        "propID": 52120772,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":100})
    }),
    52120773: _tools.RODict({
        "propID": 52120773,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":101})
    }),
    52120774: _tools.RODict({
        "propID": 52120774,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":103})
    }),
    52120775: _tools.RODict({
        "propID": 52120775,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":105})
    }),
    52120776: _tools.RODict({
        "propID": 52120776,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":106})
    }),
    52120777: _tools.RODict({
        "propID": 52120777,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":107})
    }),
    52120778: _tools.RODict({
        "propID": 52120778,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":108})
    }),
    52120779: _tools.RODict({
        "propID": 52120779,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":110})
    }),
    52120780: _tools.RODict({
        "propID": 52120780,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":112})
    }),
    52120781: _tools.RODict({
        "propID": 52120781,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":113})
    }),
    52120782: _tools.RODict({
        "propID": 52120782,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":114})
    }),
    52120783: _tools.RODict({
        "propID": 52120783,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":115})
    }),
    52120784: _tools.RODict({
        "propID": 52120784,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":117})
    }),
    52120785: _tools.RODict({
        "propID": 52120785,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":119})
    }),
    52120786: _tools.RODict({
        "propID": 52120786,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":120})
    }),
    52120787: _tools.RODict({
        "propID": 52120787,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":121})
    }),
    52120788: _tools.RODict({
        "propID": 52120788,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":122})
    }),
    52120789: _tools.RODict({
        "propID": 52120789,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":124})
    }),
    52120790: _tools.RODict({
        "propID": 52120790,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":126})
    }),
    52120791: _tools.RODict({
        "propID": 52120791,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":127})
    }),
    52120792: _tools.RODict({
        "propID": 52120792,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":128})
    }),
    52120793: _tools.RODict({
        "propID": 52120793,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":129})
    }),
    52120794: _tools.RODict({
        "propID": 52120794,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":131})
    }),
    52120795: _tools.RODict({
        "propID": 52120795,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":133})
    }),
    52120796: _tools.RODict({
        "propID": 52120796,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":134})
    }),
    52120797: _tools.RODict({
        "propID": 52120797,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":135})
    }),
    52120798: _tools.RODict({
        "propID": 52120798,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":136})
    }),
    52120799: _tools.RODict({
        "propID": 52120799,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":138})
    }),
    52120800: _tools.RODict({
        "propID": 52120800,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":140})
    }),
    52120801: _tools.RODict({
        "propID": 52120801,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":2})
    }),
    52120802: _tools.RODict({
        "propID": 52120802,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":5})
    }),
    52120803: _tools.RODict({
        "propID": 52120803,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":8})
    }),
    52120804: _tools.RODict({
        "propID": 52120804,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":11})
    }),
    52120805: _tools.RODict({
        "propID": 52120805,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":14})
    }),
    52120806: _tools.RODict({
        "propID": 52120806,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":17})
    }),
    52120807: _tools.RODict({
        "propID": 52120807,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":20})
    }),
    52120808: _tools.RODict({
        "propID": 52120808,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":23})
    }),
    52120809: _tools.RODict({
        "propID": 52120809,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":26})
    }),
    52120810: _tools.RODict({
        "propID": 52120810,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":29})
    }),
    52120811: _tools.RODict({
        "propID": 52120811,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":32})
    }),
    52120812: _tools.RODict({
        "propID": 52120812,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":35})
    }),
    52120813: _tools.RODict({
        "propID": 52120813,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":38})
    }),
    52120814: _tools.RODict({
        "propID": 52120814,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":41})
    }),
    52120815: _tools.RODict({
        "propID": 52120815,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":44})
    }),
    52120816: _tools.RODict({
        "propID": 52120816,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":47})
    }),
    52120817: _tools.RODict({
        "propID": 52120817,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":50})
    }),
    52120818: _tools.RODict({
        "propID": 52120818,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":53})
    }),
    52120819: _tools.RODict({
        "propID": 52120819,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":56})
    }),
    52120820: _tools.RODict({
        "propID": 52120820,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":59})
    }),
    52120821: _tools.RODict({
        "propID": 52120821,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":62})
    }),
    52120822: _tools.RODict({
        "propID": 52120822,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":65})
    }),
    52120823: _tools.RODict({
        "propID": 52120823,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":68})
    }),
    52120824: _tools.RODict({
        "propID": 52120824,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":71})
    }),
    52120825: _tools.RODict({
        "propID": 52120825,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":74})
    }),
    52120826: _tools.RODict({
        "propID": 52120826,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":77})
    }),
    52120827: _tools.RODict({
        "propID": 52120827,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":80})
    }),
    52120828: _tools.RODict({
        "propID": 52120828,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":83})
    }),
    52120829: _tools.RODict({
        "propID": 52120829,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":86})
    }),
    52120830: _tools.RODict({
        "propID": 52120830,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":89})
    }),
    52120831: _tools.RODict({
        "propID": 52120831,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":92})
    }),
    52120832: _tools.RODict({
        "propID": 52120832,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":95})
    }),
    52120833: _tools.RODict({
        "propID": 52120833,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":98})
    }),
    52120834: _tools.RODict({
        "propID": 52120834,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":101})
    }),
    52120835: _tools.RODict({
        "propID": 52120835,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":104})
    }),
    52120836: _tools.RODict({
        "propID": 52120836,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":107})
    }),
    52120837: _tools.RODict({
        "propID": 52120837,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":110})
    }),
    52120838: _tools.RODict({
        "propID": 52120838,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":113})
    }),
    52120839: _tools.RODict({
        "propID": 52120839,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":116})
    }),
    52120840: _tools.RODict({
        "propID": 52120840,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":119})
    }),
    52120841: _tools.RODict({
        "propID": 52120841,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":122})
    }),
    52120842: _tools.RODict({
        "propID": 52120842,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":125})
    }),
    52120843: _tools.RODict({
        "propID": 52120843,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":128})
    }),
    52120844: _tools.RODict({
        "propID": 52120844,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":131})
    }),
    52120845: _tools.RODict({
        "propID": 52120845,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":134})
    }),
    52120846: _tools.RODict({
        "propID": 52120846,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":137})
    }),
    52120847: _tools.RODict({
        "propID": 52120847,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":140})
    }),
    52120848: _tools.RODict({
        "propID": 52120848,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":143})
    }),
    52120849: _tools.RODict({
        "propID": 52120849,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":146})
    }),
    52120850: _tools.RODict({
        "propID": 52120850,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":149})
    }),
    52120851: _tools.RODict({
        "propID": 52120851,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":152})
    }),
    52120852: _tools.RODict({
        "propID": 52120852,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":155})
    }),
    52120853: _tools.RODict({
        "propID": 52120853,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":158})
    }),
    52120854: _tools.RODict({
        "propID": 52120854,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":161})
    }),
    52120855: _tools.RODict({
        "propID": 52120855,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":164})
    }),
    52120856: _tools.RODict({
        "propID": 52120856,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":167})
    }),
    52120857: _tools.RODict({
        "propID": 52120857,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":170})
    }),
    52120858: _tools.RODict({
        "propID": 52120858,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":173})
    }),
    52120859: _tools.RODict({
        "propID": 52120859,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":176})
    }),
    52120860: _tools.RODict({
        "propID": 52120860,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":179})
    }),
    52120861: _tools.RODict({
        "propID": 52120861,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":182})
    }),
    52120862: _tools.RODict({
        "propID": 52120862,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":185})
    }),
    52120863: _tools.RODict({
        "propID": 52120863,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":188})
    }),
    52120864: _tools.RODict({
        "propID": 52120864,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":191})
    }),
    52120865: _tools.RODict({
        "propID": 52120865,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":194})
    }),
    52120866: _tools.RODict({
        "propID": 52120866,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":197})
    }),
    52120867: _tools.RODict({
        "propID": 52120867,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":200})
    }),
    52120868: _tools.RODict({
        "propID": 52120868,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":203})
    }),
    52120869: _tools.RODict({
        "propID": 52120869,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":206})
    }),
    52120870: _tools.RODict({
        "propID": 52120870,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":209})
    }),
    52120871: _tools.RODict({
        "propID": 52120871,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":212})
    }),
    52120872: _tools.RODict({
        "propID": 52120872,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":215})
    }),
    52120873: _tools.RODict({
        "propID": 52120873,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":218})
    }),
    52120874: _tools.RODict({
        "propID": 52120874,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":221})
    }),
    52120875: _tools.RODict({
        "propID": 52120875,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":224})
    }),
    52120876: _tools.RODict({
        "propID": 52120876,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":227})
    }),
    52120877: _tools.RODict({
        "propID": 52120877,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":230})
    }),
    52120878: _tools.RODict({
        "propID": 52120878,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":233})
    }),
    52120879: _tools.RODict({
        "propID": 52120879,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":236})
    }),
    52120880: _tools.RODict({
        "propID": 52120880,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":239})
    }),
    52120881: _tools.RODict({
        "propID": 52120881,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":242})
    }),
    52120882: _tools.RODict({
        "propID": 52120882,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":245})
    }),
    52120883: _tools.RODict({
        "propID": 52120883,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":248})
    }),
    52120884: _tools.RODict({
        "propID": 52120884,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":251})
    }),
    52120885: _tools.RODict({
        "propID": 52120885,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":254})
    }),
    52120886: _tools.RODict({
        "propID": 52120886,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":257})
    }),
    52120887: _tools.RODict({
        "propID": 52120887,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":260})
    }),
    52120888: _tools.RODict({
        "propID": 52120888,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":263})
    }),
    52120889: _tools.RODict({
        "propID": 52120889,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":266})
    }),
    52120890: _tools.RODict({
        "propID": 52120890,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":269})
    }),
    52120891: _tools.RODict({
        "propID": 52120891,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":272})
    }),
    52120892: _tools.RODict({
        "propID": 52120892,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":275})
    }),
    52120893: _tools.RODict({
        "propID": 52120893,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":278})
    }),
    52120894: _tools.RODict({
        "propID": 52120894,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":281})
    }),
    52120895: _tools.RODict({
        "propID": 52120895,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":284})
    }),
    52120896: _tools.RODict({
        "propID": 52120896,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":287})
    }),
    52120897: _tools.RODict({
        "propID": 52120897,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":290})
    }),
    52120898: _tools.RODict({
        "propID": 52120898,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":293})
    }),
    52120899: _tools.RODict({
        "propID": 52120899,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":296})
    }),
    52120900: _tools.RODict({
        "propID": 52120900,
        "type": 2,
        "propList": _tools.RODict({"adjMaxMagicArmor":299})
    }),
    52120901: _tools.RODict({
        "propID": 52120901,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":1})
    }),
    52120902: _tools.RODict({
        "propID": 52120902,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":2})
    }),
    52120903: _tools.RODict({
        "propID": 52120903,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":3})
    }),
    52120904: _tools.RODict({
        "propID": 52120904,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":5})
    }),
    52120905: _tools.RODict({
        "propID": 52120905,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":7})
    }),
    52120906: _tools.RODict({
        "propID": 52120906,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":8})
    }),
    52120907: _tools.RODict({
        "propID": 52120907,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":9})
    }),
    52120908: _tools.RODict({
        "propID": 52120908,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":10})
    }),
    52120909: _tools.RODict({
        "propID": 52120909,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":12})
    }),
    52120910: _tools.RODict({
        "propID": 52120910,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":14})
    }),
    52120911: _tools.RODict({
        "propID": 52120911,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":15})
    }),
    52120912: _tools.RODict({
        "propID": 52120912,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":16})
    }),
    52120913: _tools.RODict({
        "propID": 52120913,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":17})
    }),
    52120914: _tools.RODict({
        "propID": 52120914,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":19})
    }),
    52120915: _tools.RODict({
        "propID": 52120915,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":21})
    }),
    52120916: _tools.RODict({
        "propID": 52120916,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":22})
    }),
    52120917: _tools.RODict({
        "propID": 52120917,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":23})
    }),
    52120918: _tools.RODict({
        "propID": 52120918,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":24})
    }),
    52120919: _tools.RODict({
        "propID": 52120919,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":26})
    }),
    52120920: _tools.RODict({
        "propID": 52120920,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":28})
    }),
    52120921: _tools.RODict({
        "propID": 52120921,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":29})
    }),
    52120922: _tools.RODict({
        "propID": 52120922,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":30})
    }),
    52120923: _tools.RODict({
        "propID": 52120923,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":31})
    }),
    52120924: _tools.RODict({
        "propID": 52120924,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":33})
    }),
    52120925: _tools.RODict({
        "propID": 52120925,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":35})
    }),
    52120926: _tools.RODict({
        "propID": 52120926,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":36})
    }),
    52120927: _tools.RODict({
        "propID": 52120927,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":37})
    }),
    52120928: _tools.RODict({
        "propID": 52120928,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":38})
    }),
    52120929: _tools.RODict({
        "propID": 52120929,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":40})
    }),
    52120930: _tools.RODict({
        "propID": 52120930,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":42})
    }),
    52120931: _tools.RODict({
        "propID": 52120931,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":43})
    }),
    52120932: _tools.RODict({
        "propID": 52120932,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":44})
    }),
    52120933: _tools.RODict({
        "propID": 52120933,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":45})
    }),
    52120934: _tools.RODict({
        "propID": 52120934,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":47})
    }),
    52120935: _tools.RODict({
        "propID": 52120935,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":49})
    }),
    52120936: _tools.RODict({
        "propID": 52120936,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":50})
    }),
    52120937: _tools.RODict({
        "propID": 52120937,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":51})
    }),
    52120938: _tools.RODict({
        "propID": 52120938,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":52})
    }),
    52120939: _tools.RODict({
        "propID": 52120939,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":54})
    }),
    52120940: _tools.RODict({
        "propID": 52120940,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":56})
    }),
    52120941: _tools.RODict({
        "propID": 52120941,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":57})
    }),
    52120942: _tools.RODict({
        "propID": 52120942,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":58})
    }),
    52120943: _tools.RODict({
        "propID": 52120943,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":59})
    }),
    52120944: _tools.RODict({
        "propID": 52120944,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":61})
    }),
    52120945: _tools.RODict({
        "propID": 52120945,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":63})
    }),
    52120946: _tools.RODict({
        "propID": 52120946,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":64})
    }),
    52120947: _tools.RODict({
        "propID": 52120947,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":65})
    }),
    52120948: _tools.RODict({
        "propID": 52120948,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":66})
    }),
    52120949: _tools.RODict({
        "propID": 52120949,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":68})
    }),
    52120950: _tools.RODict({
        "propID": 52120950,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":70})
    }),
    52120951: _tools.RODict({
        "propID": 52120951,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":71})
    }),
    52120952: _tools.RODict({
        "propID": 52120952,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":72})
    }),
    52120953: _tools.RODict({
        "propID": 52120953,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":73})
    }),
    52120954: _tools.RODict({
        "propID": 52120954,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":75})
    }),
    52120955: _tools.RODict({
        "propID": 52120955,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":77})
    }),
    52120956: _tools.RODict({
        "propID": 52120956,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":78})
    }),
    52120957: _tools.RODict({
        "propID": 52120957,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":79})
    }),
    52120958: _tools.RODict({
        "propID": 52120958,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":80})
    }),
    52120959: _tools.RODict({
        "propID": 52120959,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":82})
    }),
    52120960: _tools.RODict({
        "propID": 52120960,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":84})
    }),
    52120961: _tools.RODict({
        "propID": 52120961,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":85})
    }),
    52120962: _tools.RODict({
        "propID": 52120962,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":86})
    }),
    52120963: _tools.RODict({
        "propID": 52120963,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":87})
    }),
    52120964: _tools.RODict({
        "propID": 52120964,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":89})
    }),
    52120965: _tools.RODict({
        "propID": 52120965,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":91})
    }),
    52120966: _tools.RODict({
        "propID": 52120966,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":92})
    }),
    52120967: _tools.RODict({
        "propID": 52120967,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":93})
    }),
    52120968: _tools.RODict({
        "propID": 52120968,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":94})
    }),
    52120969: _tools.RODict({
        "propID": 52120969,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":96})
    }),
    52120970: _tools.RODict({
        "propID": 52120970,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":98})
    }),
    52120971: _tools.RODict({
        "propID": 52120971,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":99})
    }),
    52120972: _tools.RODict({
        "propID": 52120972,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":100})
    }),
    52120973: _tools.RODict({
        "propID": 52120973,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":101})
    }),
    52120974: _tools.RODict({
        "propID": 52120974,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":103})
    }),
    52120975: _tools.RODict({
        "propID": 52120975,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":105})
    }),
    52120976: _tools.RODict({
        "propID": 52120976,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":106})
    }),
    52120977: _tools.RODict({
        "propID": 52120977,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":107})
    }),
    52120978: _tools.RODict({
        "propID": 52120978,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":108})
    }),
    52120979: _tools.RODict({
        "propID": 52120979,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":110})
    }),
    52120980: _tools.RODict({
        "propID": 52120980,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":112})
    }),
    52120981: _tools.RODict({
        "propID": 52120981,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":113})
    }),
    52120982: _tools.RODict({
        "propID": 52120982,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":114})
    }),
    52120983: _tools.RODict({
        "propID": 52120983,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":115})
    }),
    52120984: _tools.RODict({
        "propID": 52120984,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":117})
    }),
    52120985: _tools.RODict({
        "propID": 52120985,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":119})
    }),
    52120986: _tools.RODict({
        "propID": 52120986,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":120})
    }),
    52120987: _tools.RODict({
        "propID": 52120987,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":121})
    }),
    52120988: _tools.RODict({
        "propID": 52120988,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":122})
    }),
    52120989: _tools.RODict({
        "propID": 52120989,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":124})
    }),
    52120990: _tools.RODict({
        "propID": 52120990,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":126})
    }),
    52120991: _tools.RODict({
        "propID": 52120991,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":127})
    }),
    52120992: _tools.RODict({
        "propID": 52120992,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":128})
    }),
    52120993: _tools.RODict({
        "propID": 52120993,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":129})
    }),
    52120994: _tools.RODict({
        "propID": 52120994,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":131})
    }),
    52120995: _tools.RODict({
        "propID": 52120995,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":133})
    }),
    52120996: _tools.RODict({
        "propID": 52120996,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":134})
    }),
    52120997: _tools.RODict({
        "propID": 52120997,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":135})
    }),
    52120998: _tools.RODict({
        "propID": 52120998,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":136})
    }),
    52120999: _tools.RODict({
        "propID": 52120999,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":138})
    }),
    52121000: _tools.RODict({
        "propID": 52121000,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":140})
    }),
    52121001: _tools.RODict({
        "propID": 52121001,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":160,"adjMinPhysicalAtk":7,"adjMaxPhysicalAtk":15,"adjHit":2,"adjDodge":2,"adjMonsterDmg":0.01,"adjMonsterDmgAnti":0.01})
    }),
    52121002: _tools.RODict({
        "propID": 52121002,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":320,"adjMinPhysicalAtk":14,"adjMaxPhysicalAtk":30,"adjHit":4,"adjDodge":4,"adjMonsterDmg":0.01,"adjMonsterDmgAnti":0.01})
    }),
    52121003: _tools.RODict({
        "propID": 52121003,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":480,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":45,"adjHit":6,"adjDodge":6,"adjMonsterDmg":0.02,"adjMonsterDmgAnti":0.02})
    }),
    52121004: _tools.RODict({
        "propID": 52121004,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":720,"adjMinPhysicalAtk":28,"adjMaxPhysicalAtk":60,"adjHit":8,"adjDodge":8,"adjMonsterDmg":0.02,"adjMonsterDmgAnti":0.02})
    }),
    52121005: _tools.RODict({
        "propID": 52121005,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":960,"adjMinPhysicalAtk":35,"adjMaxPhysicalAtk":75,"adjHit":10,"adjDodge":10,"adjMonsterDmg":0.03,"adjMonsterDmgAnti":0.03})
    }),
    52121006: _tools.RODict({
        "propID": 52121006,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1200,"adjMinPhysicalAtk":42,"adjMaxPhysicalAtk":90,"adjHit":12,"adjDodge":12,"adjMonsterDmg":0.03,"adjMonsterDmgAnti":0.03})
    }),
    52121007: _tools.RODict({
        "propID": 52121007,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1520,"adjMinPhysicalAtk":49,"adjMaxPhysicalAtk":105,"adjHit":14,"adjDodge":14,"adjMonsterDmg":0.04,"adjMonsterDmgAnti":0.04})
    }),
    52121008: _tools.RODict({
        "propID": 52121008,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1840,"adjMinPhysicalAtk":56,"adjMaxPhysicalAtk":120,"adjHit":16,"adjDodge":16,"adjMonsterDmg":0.04,"adjMonsterDmgAnti":0.04})
    }),
    52121009: _tools.RODict({
        "propID": 52121009,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2160,"adjMinPhysicalAtk":63,"adjMaxPhysicalAtk":135,"adjHit":18,"adjDodge":18,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52121010: _tools.RODict({
        "propID": 52121010,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2560,"adjMinPhysicalAtk":70,"adjMaxPhysicalAtk":150,"adjHit":20,"adjDodge":20,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52121011: _tools.RODict({
        "propID": 52121011,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2960,"adjMinPhysicalAtk":77,"adjMaxPhysicalAtk":165,"adjHit":22,"adjDodge":22,"adjMonsterDmg":0.06,"adjMonsterDmgAnti":0.06})
    }),
    52121012: _tools.RODict({
        "propID": 52121012,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3360,"adjMinPhysicalAtk":84,"adjMaxPhysicalAtk":180,"adjHit":24,"adjDodge":24,"adjMonsterDmg":0.06,"adjMonsterDmgAnti":0.06})
    }),
    52121013: _tools.RODict({
        "propID": 52121013,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3840,"adjMinPhysicalAtk":91,"adjMaxPhysicalAtk":195,"adjHit":26,"adjDodge":26,"adjMonsterDmg":0.07,"adjMonsterDmgAnti":0.07})
    }),
    52121014: _tools.RODict({
        "propID": 52121014,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4320,"adjMinPhysicalAtk":98,"adjMaxPhysicalAtk":210,"adjHit":28,"adjDodge":28,"adjMonsterDmg":0.07,"adjMonsterDmgAnti":0.07})
    }),
    52121015: _tools.RODict({
        "propID": 52121015,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4800,"adjMinPhysicalAtk":105,"adjMaxPhysicalAtk":225,"adjHit":30,"adjDodge":30,"adjMonsterDmg":0.08,"adjMonsterDmgAnti":0.08})
    }),
    52121016: _tools.RODict({
        "propID": 52121016,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5360,"adjMinPhysicalAtk":112,"adjMaxPhysicalAtk":240,"adjHit":32,"adjDodge":32,"adjMonsterDmg":0.08,"adjMonsterDmgAnti":0.08})
    }),
    52121017: _tools.RODict({
        "propID": 52121017,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5920,"adjMinPhysicalAtk":119,"adjMaxPhysicalAtk":255,"adjHit":34,"adjDodge":34,"adjMonsterDmg":0.09,"adjMonsterDmgAnti":0.09})
    }),
    52121018: _tools.RODict({
        "propID": 52121018,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":6560,"adjMinPhysicalAtk":126,"adjMaxPhysicalAtk":270,"adjHit":36,"adjDodge":36,"adjMonsterDmg":0.09,"adjMonsterDmgAnti":0.09})
    }),
    52121019: _tools.RODict({
        "propID": 52121019,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":7280,"adjMinPhysicalAtk":133,"adjMaxPhysicalAtk":285,"adjHit":38,"adjDodge":38,"adjMonsterDmg":0.1,"adjMonsterDmgAnti":0.1})
    }),
    52121020: _tools.RODict({
        "propID": 52121020,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":8000,"adjMinPhysicalAtk":140,"adjMaxPhysicalAtk":300,"adjHit":40,"adjDodge":40,"adjMonsterDmg":0.1,"adjMonsterDmgAnti":0.1})
    }),
    52121021: _tools.RODict({
        "propID": 52121021,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":160,"adjMinMagicAtk":7,"adjMaxMagicAtk":15,"adjHit":2,"adjDodge":2,"adjMonsterDmg":0.01,"adjMonsterDmgAnti":0.01})
    }),
    52121022: _tools.RODict({
        "propID": 52121022,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":320,"adjMinMagicAtk":14,"adjMaxMagicAtk":30,"adjHit":4,"adjDodge":4,"adjMonsterDmg":0.01,"adjMonsterDmgAnti":0.01})
    }),
    52121023: _tools.RODict({
        "propID": 52121023,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":480,"adjMinMagicAtk":21,"adjMaxMagicAtk":45,"adjHit":6,"adjDodge":6,"adjMonsterDmg":0.02,"adjMonsterDmgAnti":0.02})
    }),
    52121024: _tools.RODict({
        "propID": 52121024,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":720,"adjMinMagicAtk":28,"adjMaxMagicAtk":60,"adjHit":8,"adjDodge":8,"adjMonsterDmg":0.02,"adjMonsterDmgAnti":0.02})
    }),
    52121025: _tools.RODict({
        "propID": 52121025,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":960,"adjMinMagicAtk":35,"adjMaxMagicAtk":75,"adjHit":10,"adjDodge":10,"adjMonsterDmg":0.03,"adjMonsterDmgAnti":0.03})
    }),
    52121026: _tools.RODict({
        "propID": 52121026,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1200,"adjMinMagicAtk":42,"adjMaxMagicAtk":90,"adjHit":12,"adjDodge":12,"adjMonsterDmg":0.03,"adjMonsterDmgAnti":0.03})
    }),
    52121027: _tools.RODict({
        "propID": 52121027,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1520,"adjMinMagicAtk":49,"adjMaxMagicAtk":105,"adjHit":14,"adjDodge":14,"adjMonsterDmg":0.04,"adjMonsterDmgAnti":0.04})
    }),
    52121028: _tools.RODict({
        "propID": 52121028,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1840,"adjMinMagicAtk":56,"adjMaxMagicAtk":120,"adjHit":16,"adjDodge":16,"adjMonsterDmg":0.04,"adjMonsterDmgAnti":0.04})
    }),
    52121029: _tools.RODict({
        "propID": 52121029,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2160,"adjMinMagicAtk":63,"adjMaxMagicAtk":135,"adjHit":18,"adjDodge":18,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52121030: _tools.RODict({
        "propID": 52121030,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2560,"adjMinMagicAtk":70,"adjMaxMagicAtk":150,"adjHit":20,"adjDodge":20,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52121031: _tools.RODict({
        "propID": 52121031,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2960,"adjMinMagicAtk":77,"adjMaxMagicAtk":165,"adjHit":22,"adjDodge":22,"adjMonsterDmg":0.06,"adjMonsterDmgAnti":0.06})
    }),
    52121032: _tools.RODict({
        "propID": 52121032,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3360,"adjMinMagicAtk":84,"adjMaxMagicAtk":180,"adjHit":24,"adjDodge":24,"adjMonsterDmg":0.06,"adjMonsterDmgAnti":0.06})
    }),
    52121033: _tools.RODict({
        "propID": 52121033,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3840,"adjMinMagicAtk":91,"adjMaxMagicAtk":195,"adjHit":26,"adjDodge":26,"adjMonsterDmg":0.07,"adjMonsterDmgAnti":0.07})
    }),
    52121034: _tools.RODict({
        "propID": 52121034,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4320,"adjMinMagicAtk":98,"adjMaxMagicAtk":210,"adjHit":28,"adjDodge":28,"adjMonsterDmg":0.07,"adjMonsterDmgAnti":0.07})
    }),
    52121035: _tools.RODict({
        "propID": 52121035,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4800,"adjMinMagicAtk":105,"adjMaxMagicAtk":225,"adjHit":30,"adjDodge":30,"adjMonsterDmg":0.08,"adjMonsterDmgAnti":0.08})
    }),
    52121036: _tools.RODict({
        "propID": 52121036,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5360,"adjMinMagicAtk":112,"adjMaxMagicAtk":240,"adjHit":32,"adjDodge":32,"adjMonsterDmg":0.08,"adjMonsterDmgAnti":0.08})
    }),
    52121037: _tools.RODict({
        "propID": 52121037,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5920,"adjMinMagicAtk":119,"adjMaxMagicAtk":255,"adjHit":34,"adjDodge":34,"adjMonsterDmg":0.09,"adjMonsterDmgAnti":0.09})
    }),
    52121038: _tools.RODict({
        "propID": 52121038,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":6560,"adjMinMagicAtk":126,"adjMaxMagicAtk":270,"adjHit":36,"adjDodge":36,"adjMonsterDmg":0.09,"adjMonsterDmgAnti":0.09})
    }),
    52121039: _tools.RODict({
        "propID": 52121039,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":7280,"adjMinMagicAtk":133,"adjMaxMagicAtk":285,"adjHit":38,"adjDodge":38,"adjMonsterDmg":0.1,"adjMonsterDmgAnti":0.1})
    }),
    52121040: _tools.RODict({
        "propID": 52121040,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":8000,"adjMinMagicAtk":140,"adjMaxMagicAtk":300,"adjHit":40,"adjDodge":40,"adjMonsterDmg":0.1,"adjMonsterDmgAnti":0.1})
    })
})
minKey = 51000001
maxKey = 52121040