# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: formula/generalFormula
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab


# import grow_grow1


def _34000003(qua, lv):
    rate = 0
    if qua == 1:
        rate = 0.04
    elif qua == 2:
        rate = 0.03
    elif qua == 3:
        rate = 0.02
    elif qua == 4:
        rate = 0.015
    sum = 0
    for i in range(0, lv):
        if (i + 1) % 5 == 0:
            sum += (i // 5 + 0.5) * rate * 1.2
        else:
            sum += (i // 5 + 0.5) * rate
    return sum
def _34000004(qua, grade):
    factor1 = 1
    factor2 = 1
    factor3 = ((qua - 1) * 4 + grade )* 0.25
    factor4 = ((qua - 1) * 4 + grade )* 0.25
    return [factor1,factor2,factor3,factor4]
def _34000007(cnt):
    if cnt < 5:
        wt = cnt * 5
    elif cnt < 11:
        wt = (cnt-4) * 10 + 20
    else:
        wt = 90

    return wt
def _34000010(lv):
    sum = 0
    for i in range(1, lv+1):
        a = i*2
        sum = a
    return sum
def _34000011(lv):
    sum = 0
    for i in range(1, lv+1):
        a = i*0.002
        sum = a
    return sum
def _34000012(lv):
    sum = 0
    for i in range(1, lv+1):
        a = i*0.001
        sum = a
    return sum
def _34000013(e):
    if e >-500:
        result = 0.05
    else:
        result = 0.1
    return result
def _34000014(e):
    result = int(e.score * 2 * 0.1) + e.quality**2 * 10 + e.grade * 10
    return result
def _34000015(e):
    if e >5000:
        result = 50
    elif 2000 < e <= 5000:
        result = 100
    else:
        result = 200

    return result
def _34000016(lv):
    sum = 0
    for i in range(1, lv+1):
        a = i*0.002
        sum = a
    return sum
def _34000017(lv):
    sum = 0
    for i in range(1, lv+1):
        a = i*3
        sum = a
    return sum
def _34000018(lv):
    sum = 0
    for i in range(1, lv+1):
        a = i*150
        sum = a
    return sum
def _34000019(lv):
    sum = 0
    for i in range(1, lv+1):
        a = i*6
        sum = a
    return sum
def _34000020(lv):
    sum = 0
    for i in range(1, lv+1):
        a = i*0.005
        sum = a
    return sum
def _34010001(e):
    return int(e.level*60+340)
def _34010002(e):
    return int(e.level*60+340)
def _34010003(e):
    return int(e.level*60+340)
def _34010004(e):
    return int(e.level*6+28)
def _34010005(e):
    return int(e.level*6+28)
def _34010006(e):
    return int(e.level*6+28)
def _34010007(e):
    return 7
def _34010008(e):
    return 7
def _34010009(e):
    return int(e.level*3+57)
def _34010010(e):
    return 6
def _34010011(e):
    return 6
def _34010012(e):
    return int(e.level+ 26)
def _34010013(e):
    return int(e.level*3 + 57)
def _34010014(e):
    return int(e.level*3 + 57)
def _34010015(e):
    return 7
def _34010016(e):
     return int(e.level + 26)
def _34010017(e):
    return int(e.level + 26)
def _34010018(e):
    return 6
def _34010019(e):
    return int(e.level*0.6 + 8)
def _34010020(e):
    return int(e.level*0.6 + 8)
def _34010021(e):
    return int(e.level*0.6 + 8)
def _34010022(e):
    return int(e.level*0.6 + 8)
def _34010023(e):
    return int(e.level*0.6 + 8)
def _34010024(e):
     return int(e.level*0.6 + 8)
def _34010025(e):
    return int(e.level/2*1+1)
def _34010026(e):
    return int(e.level/2*1+1)
def _34010027(e):
     return int(e.level/2*1+1)
def _34010028(e):
     return int(e.level/2*1+1)
def _34010029(e):
     return int(e.level/2*1+1)
def _34010030(e):
    return int(e.level/2*1+1)
def _34010031(e):
    return int(e.level*1.2 + 23)
def _34010032(e):
    return int(e.level*1.2 + 23)
def _34010033(e):
    return int(e.level*1.2 + 23)
def _34010034(e):
    return int(e.level*1.2 + 23)
def _34010035(e):
    return int(e.level*1.2 + 23)
def _34010036(e):
     return int(e.level*1.2 + 23)
def _34010037(e):
    return int(e.level*1)
def _34010038(e):
     return int(e.level*1)
def _34010039(e):
    return min(int(e*1), 180)
def _34990001(e):
    return 1
datas = _tools.RODict({ 
    34000001: _tools.RODict({
        "ID": 34000001,
        'serverFormula':lambda e: int((e['level'] *44+ 192)*e['rarityCoefficient']),
    }),
    34000002: _tools.RODict({
        "ID": 34000002,
        'serverFormula':lambda grade: grade*2,
    }),
    34000003: _tools.RODict({
        "ID": 34000003,
        'serverFormula':_34000003,
    }),
    34000004: _tools.RODict({
        "ID": 34000004,
        'serverFormula':_34000004,
    }),
    34000005: _tools.RODict({
        "ID": 34000005,
        'serverFormula':lambda lv: 2 + lv * 0.1,
    }),
    34000006: _tools.RODict({
        "ID": 34000006,
        'serverFormula':lambda lv: lv * 1250,
    }),
    34000007: _tools.RODict({
        "ID": 34000007,
        'serverFormula':_34000007,
    }),
    34000008: _tools.RODict({
        "ID": 34000008,
        'serverFormula':lambda exp: int(exp/500+2000),
    }),
    34000009: _tools.RODict({
        "ID": 34000009,
        'serverFormula':lambda exp: int(exp/580000+2),
    }),
    34000010: _tools.RODict({
        "ID": 34000010,
        'serverFormula':_34000010,
    }),
    34000011: _tools.RODict({
        "ID": 34000011,
        'serverFormula':_34000011,
    }),
    34000012: _tools.RODict({
        "ID": 34000012,
        'serverFormula':_34000012,
    }),
    34000013: _tools.RODict({
        "ID": 34000013,
        'serverFormula':_34000013,
    }),
    34000014: _tools.RODict({
        "ID": 34000014,
        'serverFormula':_34000014,
    }),
    34000015: _tools.RODict({
        "ID": 34000015,
        'serverFormula':_34000015,
    }),
    34000016: _tools.RODict({
        "ID": 34000016,
        'serverFormula':_34000016,
    }),
    34000017: _tools.RODict({
        "ID": 34000017,
        'serverFormula':_34000017,
    }),
    34000018: _tools.RODict({
        "ID": 34000018,
        'serverFormula':_34000018,
    }),
    34000019: _tools.RODict({
        "ID": 34000019,
        'serverFormula':_34000019,
    }),
    34000020: _tools.RODict({
        "ID": 34000020,
        'serverFormula':_34000020,
    }),
    34900000: _tools.RODict({
        "ID": 34900000,
        'serverFormula':lambda :0,
    }),
    34900001: _tools.RODict({
        "ID": 34900001,
        'serverFormula':lambda :1,
    }),
    34900002: _tools.RODict({
        "ID": 34900002,
        'serverFormula':lambda a1:a1+1,
    }),
    34900003: _tools.RODict({
        "ID": 34900003,
        'serverFormula':lambda a1:a1==1,
    }),
    34900004: _tools.RODict({
        "ID": 34900004,
        'serverFormula':lambda a1,a2:a1==a2,
    }),
    34900005: _tools.RODict({
        "ID": 34900005,
        'serverFormula':lambda v: v<15,
    }),
    34010001: _tools.RODict({
        "ID": 34010001,
        'serverFormula':_34010001,
    }),
    34010002: _tools.RODict({
        "ID": 34010002,
        'serverFormula':_34010002,
    }),
    34010003: _tools.RODict({
        "ID": 34010003,
        'serverFormula':_34010003,
    }),
    34010004: _tools.RODict({
        "ID": 34010004,
        'serverFormula':_34010004,
    }),
    34010005: _tools.RODict({
        "ID": 34010005,
        'serverFormula':_34010005,
    }),
    34010006: _tools.RODict({
        "ID": 34010006,
        'serverFormula':_34010006,
    }),
    34010007: _tools.RODict({
        "ID": 34010007,
        'serverFormula':_34010007,
    }),
    34010008: _tools.RODict({
        "ID": 34010008,
        'serverFormula':_34010008,
    }),
    34010009: _tools.RODict({
        "ID": 34010009,
        'serverFormula':_34010009,
    }),
    34010010: _tools.RODict({
        "ID": 34010010,
        'serverFormula':_34010010,
    }),
    34010011: _tools.RODict({
        "ID": 34010011,
        'serverFormula':_34010011,
    }),
    34010012: _tools.RODict({
        "ID": 34010012,
        'serverFormula':_34010012,
    }),
    34010013: _tools.RODict({
        "ID": 34010013,
        'serverFormula':_34010013,
    }),
    34010014: _tools.RODict({
        "ID": 34010014,
        'serverFormula':_34010014,
    }),
    34010015: _tools.RODict({
        "ID": 34010015,
        'serverFormula':_34010015,
    }),
    34010016: _tools.RODict({
        "ID": 34010016,
        'serverFormula':_34010016,
    }),
    34010017: _tools.RODict({
        "ID": 34010017,
        'serverFormula':_34010017,
    }),
    34010018: _tools.RODict({
        "ID": 34010018,
        'serverFormula':_34010018,
    }),
    34010019: _tools.RODict({
        "ID": 34010019,
        'serverFormula':_34010019,
    }),
    34010020: _tools.RODict({
        "ID": 34010020,
        'serverFormula':_34010020,
    }),
    34010021: _tools.RODict({
        "ID": 34010021,
        'serverFormula':_34010021,
    }),
    34010022: _tools.RODict({
        "ID": 34010022,
        'serverFormula':_34010022,
    }),
    34010023: _tools.RODict({
        "ID": 34010023,
        'serverFormula':_34010023,
    }),
    34010024: _tools.RODict({
        "ID": 34010024,
        'serverFormula':_34010024,
    }),
    34010025: _tools.RODict({
        "ID": 34010025,
        'serverFormula':_34010025,
    }),
    34010026: _tools.RODict({
        "ID": 34010026,
        'serverFormula':_34010026,
    }),
    34010027: _tools.RODict({
        "ID": 34010027,
        'serverFormula':_34010027,
    }),
    34010028: _tools.RODict({
        "ID": 34010028,
        'serverFormula':_34010028,
    }),
    34010029: _tools.RODict({
        "ID": 34010029,
        'serverFormula':_34010029,
    }),
    34010030: _tools.RODict({
        "ID": 34010030,
        'serverFormula':_34010030,
    }),
    34010031: _tools.RODict({
        "ID": 34010031,
        'serverFormula':_34010031,
    }),
    34010032: _tools.RODict({
        "ID": 34010032,
        'serverFormula':_34010032,
    }),
    34010033: _tools.RODict({
        "ID": 34010033,
        'serverFormula':_34010033,
    }),
    34010034: _tools.RODict({
        "ID": 34010034,
        'serverFormula':_34010034,
    }),
    34010035: _tools.RODict({
        "ID": 34010035,
        'serverFormula':_34010035,
    }),
    34010036: _tools.RODict({
        "ID": 34010036,
        'serverFormula':_34010036,
    }),
    34010037: _tools.RODict({
        "ID": 34010037,
        'serverFormula':_34010037,
    }),
    34010038: _tools.RODict({
        "ID": 34010038,
        'serverFormula':_34010038,
    }),
    34010039: _tools.RODict({
        "ID": 34010039,
        'serverFormula':_34010039,
    }),
    34990001: _tools.RODict({
        "ID": 34990001,
        'serverFormula':_34990001,
    })
})
minKey = 34000001
maxKey = 34990001