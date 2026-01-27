# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: creep/countRefresh
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    310301: _tools.RODict({
        "ID": 310301,
        "mapID": 3103,
        "combatAreaID": 31038004,
        "refreshMonsterID": _tools.ROList([31030088]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11011004, 11011005, 11011006]),
        "countResetTime": 60
    }),
    310302: _tools.RODict({
        "ID": 310302,
        "mapID": 3103,
        "combatAreaID": 31038005,
        "refreshMonsterID": _tools.ROList([31030129]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11011004, 11011005, 11011006]),
        "countResetTime": 60
    }),
    310303: _tools.RODict({
        "ID": 310303,
        "mapID": 3103,
        "combatAreaID": 31038006,
        "refreshMonsterID": _tools.ROList([31030170]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11011004, 11011005, 11011006]),
        "countResetTime": 60
    }),
    310401: _tools.RODict({
        "ID": 310401,
        "mapID": 3104,
        "combatAreaID": 31048004,
        "refreshMonsterID": _tools.ROList([31040088]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11011004, 11011005, 11011006]),
        "countResetTime": 60
    }),
    310402: _tools.RODict({
        "ID": 310402,
        "mapID": 3104,
        "combatAreaID": 31048005,
        "refreshMonsterID": _tools.ROList([31040129]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11011004, 11011005, 11011006]),
        "countResetTime": 60
    }),
    310403: _tools.RODict({
        "ID": 310403,
        "mapID": 3104,
        "combatAreaID": 31048006,
        "refreshMonsterID": _tools.ROList([31040170]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11011004, 11011005, 11011006]),
        "countResetTime": 60
    }),
    310501: _tools.RODict({
        "ID": 310501,
        "mapID": 3105,
        "combatAreaID": 31058004,
        "refreshMonsterID": _tools.ROList([31050088]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11011004, 11011005, 11011006]),
        "countResetTime": 60
    }),
    310502: _tools.RODict({
        "ID": 310502,
        "mapID": 3105,
        "combatAreaID": 31058005,
        "refreshMonsterID": _tools.ROList([31050129]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11011004, 11011005, 11011006]),
        "countResetTime": 60
    }),
    310503: _tools.RODict({
        "ID": 310503,
        "mapID": 3105,
        "combatAreaID": 31058006,
        "refreshMonsterID": _tools.ROList([31050170]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11011004, 11011005, 11011006]),
        "countResetTime": 60
    }),
    311201: _tools.RODict({
        "ID": 311201,
        "mapID": 3112,
        "combatAreaID": 31128004,
        "refreshMonsterID": _tools.ROList([31120088]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11011011, 11011012, 11011013]),
        "countResetTime": 60
    }),
    311202: _tools.RODict({
        "ID": 311202,
        "mapID": 3112,
        "combatAreaID": 31128005,
        "refreshMonsterID": _tools.ROList([31120129]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11011011, 11011012, 11011013]),
        "countResetTime": 60
    }),
    311203: _tools.RODict({
        "ID": 311203,
        "mapID": 3112,
        "combatAreaID": 31128006,
        "refreshMonsterID": _tools.ROList([31120170]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11011011, 11011012, 11011013]),
        "countResetTime": 60
    }),
    311301: _tools.RODict({
        "ID": 311301,
        "mapID": 3113,
        "combatAreaID": 31138004,
        "refreshMonsterID": _tools.ROList([31130088]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11011011, 11011012, 11011013]),
        "countResetTime": 60
    }),
    311302: _tools.RODict({
        "ID": 311302,
        "mapID": 3113,
        "combatAreaID": 31138005,
        "refreshMonsterID": _tools.ROList([31130129]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11011011, 11011012, 11011013]),
        "countResetTime": 60
    }),
    311303: _tools.RODict({
        "ID": 311303,
        "mapID": 3113,
        "combatAreaID": 31138006,
        "refreshMonsterID": _tools.ROList([31130170]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11011011, 11011012, 11011013]),
        "countResetTime": 60
    }),
    311401: _tools.RODict({
        "ID": 311401,
        "mapID": 3114,
        "combatAreaID": 31148004,
        "refreshMonsterID": _tools.ROList([31140088]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11011011, 11011012, 11011013]),
        "countResetTime": 60
    }),
    311402: _tools.RODict({
        "ID": 311402,
        "mapID": 3114,
        "combatAreaID": 31148005,
        "refreshMonsterID": _tools.ROList([31140129]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11011011, 11011012, 11011013]),
        "countResetTime": 60
    }),
    311403: _tools.RODict({
        "ID": 311403,
        "mapID": 3114,
        "combatAreaID": 31148006,
        "refreshMonsterID": _tools.ROList([31140170]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11011011, 11011012, 11011013]),
        "countResetTime": 60
    }),
    311801: _tools.RODict({
        "ID": 311801,
        "mapID": 3118,
        "combatAreaID": 31188004,
        "refreshMonsterID": _tools.ROList([31180088]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11011046, 11011047, 11011048]),
        "countResetTime": 60
    }),
    311802: _tools.RODict({
        "ID": 311802,
        "mapID": 3118,
        "combatAreaID": 31188005,
        "refreshMonsterID": _tools.ROList([31180129]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11011046, 11011047, 11011048]),
        "countResetTime": 60
    }),
    311803: _tools.RODict({
        "ID": 311803,
        "mapID": 3118,
        "combatAreaID": 31188006,
        "refreshMonsterID": _tools.ROList([31180170]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11011046, 11011047, 11011048]),
        "countResetTime": 60
    }),
    311901: _tools.RODict({
        "ID": 311901,
        "mapID": 3119,
        "combatAreaID": 31198004,
        "refreshMonsterID": _tools.ROList([31190088]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11011050, 11011051, 11011052]),
        "countResetTime": 60
    }),
    311902: _tools.RODict({
        "ID": 311902,
        "mapID": 3119,
        "combatAreaID": 31198005,
        "refreshMonsterID": _tools.ROList([31190129]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11011050, 11011051, 11011052]),
        "countResetTime": 60
    }),
    311903: _tools.RODict({
        "ID": 311903,
        "mapID": 3119,
        "combatAreaID": 31198006,
        "refreshMonsterID": _tools.ROList([31190170]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11011050, 11011051, 11011052]),
        "countResetTime": 60
    }),
    312001: _tools.RODict({
        "ID": 312001,
        "mapID": 3120,
        "combatAreaID": 31208008,
        "refreshMonsterID": _tools.ROList([31200096, 31200104]),
        "countLimit": 100,
        "countMonsterID": _tools.ROList([11011030, 11011031, 11011032]),
        "countResetTime": 60
    }),
    312002: _tools.RODict({
        "ID": 312002,
        "mapID": 3120,
        "combatAreaID": 31208008,
        "refreshMonsterID": _tools.ROList([31200112, 31200120]),
        "countLimit": 100,
        "countMonsterID": _tools.ROList([11011035, 11011036, 11011037]),
        "countResetTime": 60
    }),
    312003: _tools.RODict({
        "ID": 312003,
        "mapID": 3120,
        "combatAreaID": 31208008,
        "refreshMonsterID": _tools.ROList([31200129, 31200137]),
        "countLimit": 100,
        "countMonsterID": _tools.ROList([11011040, 11011041, 11011042]),
        "countResetTime": 60
    }),
    312004: _tools.RODict({
        "ID": 312004,
        "mapID": 3120,
        "combatAreaID": 31208008,
        "refreshMonsterID": _tools.ROList([31200168]),
        "countLimit": 60,
        "countMonsterID": _tools.ROList([11011033, 11011034, 11011038, 11011039, 11011043, 11011044]),
        "countResetTime": 150
    }),
    320301: _tools.RODict({
        "ID": 320301,
        "mapID": 3203,
        "combatAreaID": 32038004,
        "refreshMonsterID": _tools.ROList([32030088]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11012004, 11012005, 11012006]),
        "countResetTime": 60
    }),
    320302: _tools.RODict({
        "ID": 320302,
        "mapID": 3203,
        "combatAreaID": 32038005,
        "refreshMonsterID": _tools.ROList([32030129]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11012004, 11012005, 11012006]),
        "countResetTime": 60
    }),
    320303: _tools.RODict({
        "ID": 320303,
        "mapID": 3203,
        "combatAreaID": 32038006,
        "refreshMonsterID": _tools.ROList([32030170]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11012004, 11012005, 11012006]),
        "countResetTime": 60
    }),
    320401: _tools.RODict({
        "ID": 320401,
        "mapID": 3204,
        "combatAreaID": 32048004,
        "refreshMonsterID": _tools.ROList([32040088]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11012004, 11012005, 11012006]),
        "countResetTime": 60
    }),
    320402: _tools.RODict({
        "ID": 320402,
        "mapID": 3204,
        "combatAreaID": 32048005,
        "refreshMonsterID": _tools.ROList([32040129]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11012004, 11012005, 11012006]),
        "countResetTime": 60
    }),
    320403: _tools.RODict({
        "ID": 320403,
        "mapID": 3204,
        "combatAreaID": 32048006,
        "refreshMonsterID": _tools.ROList([32040170]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11012004, 11012005, 11012006]),
        "countResetTime": 60
    }),
    320501: _tools.RODict({
        "ID": 320501,
        "mapID": 3205,
        "combatAreaID": 32058004,
        "refreshMonsterID": _tools.ROList([32050088]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11012004, 11012005, 11012006]),
        "countResetTime": 60
    }),
    320502: _tools.RODict({
        "ID": 320502,
        "mapID": 3205,
        "combatAreaID": 32058005,
        "refreshMonsterID": _tools.ROList([32050129]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11012004, 11012005, 11012006]),
        "countResetTime": 60
    }),
    320503: _tools.RODict({
        "ID": 320503,
        "mapID": 3205,
        "combatAreaID": 32058006,
        "refreshMonsterID": _tools.ROList([32050170]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11012004, 11012005, 11012006]),
        "countResetTime": 60
    }),
    321201: _tools.RODict({
        "ID": 321201,
        "mapID": 3212,
        "combatAreaID": 32128004,
        "refreshMonsterID": _tools.ROList([32120088]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11012011, 11012012, 11012013]),
        "countResetTime": 60
    }),
    321202: _tools.RODict({
        "ID": 321202,
        "mapID": 3212,
        "combatAreaID": 32128005,
        "refreshMonsterID": _tools.ROList([32120129]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11012011, 11012012, 11012013]),
        "countResetTime": 60
    }),
    321203: _tools.RODict({
        "ID": 321203,
        "mapID": 3212,
        "combatAreaID": 32128006,
        "refreshMonsterID": _tools.ROList([32120170]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11012011, 11012012, 11012013]),
        "countResetTime": 60
    }),
    321301: _tools.RODict({
        "ID": 321301,
        "mapID": 3213,
        "combatAreaID": 32138004,
        "refreshMonsterID": _tools.ROList([32130088]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11012011, 11012012, 11012013]),
        "countResetTime": 60
    }),
    321302: _tools.RODict({
        "ID": 321302,
        "mapID": 3213,
        "combatAreaID": 32138005,
        "refreshMonsterID": _tools.ROList([32130129]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11012011, 11012012, 11012013]),
        "countResetTime": 60
    }),
    321303: _tools.RODict({
        "ID": 321303,
        "mapID": 3213,
        "combatAreaID": 32138006,
        "refreshMonsterID": _tools.ROList([32130170]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11012011, 11012012, 11012013]),
        "countResetTime": 60
    }),
    321401: _tools.RODict({
        "ID": 321401,
        "mapID": 3214,
        "combatAreaID": 32148004,
        "refreshMonsterID": _tools.ROList([32140088]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11012011, 11012012, 11012013]),
        "countResetTime": 60
    }),
    321402: _tools.RODict({
        "ID": 321402,
        "mapID": 3214,
        "combatAreaID": 32148005,
        "refreshMonsterID": _tools.ROList([32140129]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11012011, 11012012, 11012013]),
        "countResetTime": 60
    }),
    321403: _tools.RODict({
        "ID": 321403,
        "mapID": 3214,
        "combatAreaID": 32148006,
        "refreshMonsterID": _tools.ROList([32140170]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11012011, 11012012, 11012013]),
        "countResetTime": 60
    }),
    321801: _tools.RODict({
        "ID": 321801,
        "mapID": 3218,
        "combatAreaID": 32188004,
        "refreshMonsterID": _tools.ROList([32180088]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11012046, 11012047, 11012048]),
        "countResetTime": 60
    }),
    321802: _tools.RODict({
        "ID": 321802,
        "mapID": 3218,
        "combatAreaID": 32188005,
        "refreshMonsterID": _tools.ROList([32180129]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11012046, 11012047, 11012048]),
        "countResetTime": 60
    }),
    321803: _tools.RODict({
        "ID": 321803,
        "mapID": 3218,
        "combatAreaID": 32188006,
        "refreshMonsterID": _tools.ROList([32180170]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11012046, 11012047, 11012048]),
        "countResetTime": 60
    }),
    321901: _tools.RODict({
        "ID": 321901,
        "mapID": 3219,
        "combatAreaID": 32198004,
        "refreshMonsterID": _tools.ROList([32190088]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11012050, 11012051, 11012052]),
        "countResetTime": 60
    }),
    321902: _tools.RODict({
        "ID": 321902,
        "mapID": 3219,
        "combatAreaID": 32198005,
        "refreshMonsterID": _tools.ROList([32190129]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11012050, 11012051, 11012052]),
        "countResetTime": 60
    }),
    321903: _tools.RODict({
        "ID": 321903,
        "mapID": 3219,
        "combatAreaID": 32198006,
        "refreshMonsterID": _tools.ROList([32190170]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11012050, 11012051, 11012052]),
        "countResetTime": 60
    }),
    322001: _tools.RODict({
        "ID": 322001,
        "mapID": 3220,
        "combatAreaID": 32208008,
        "refreshMonsterID": _tools.ROList([32200096, 32200104]),
        "countLimit": 100,
        "countMonsterID": _tools.ROList([11012030, 11012032, 11012032]),
        "countResetTime": 60
    }),
    322002: _tools.RODict({
        "ID": 322002,
        "mapID": 3220,
        "combatAreaID": 32208008,
        "refreshMonsterID": _tools.ROList([32200112, 32200120]),
        "countLimit": 100,
        "countMonsterID": _tools.ROList([11012035, 11012036, 11012037]),
        "countResetTime": 60
    }),
    322003: _tools.RODict({
        "ID": 322003,
        "mapID": 3220,
        "combatAreaID": 32208008,
        "refreshMonsterID": _tools.ROList([32200129, 32200137]),
        "countLimit": 100,
        "countMonsterID": _tools.ROList([11012040, 11012041, 11012042]),
        "countResetTime": 60
    }),
    322004: _tools.RODict({
        "ID": 322004,
        "mapID": 3220,
        "combatAreaID": 32208008,
        "refreshMonsterID": _tools.ROList([32200168]),
        "countLimit": 60,
        "countMonsterID": _tools.ROList([11012033, 11012034, 11012038, 11012039, 11012043, 11012044]),
        "countResetTime": 150
    }),
    330301: _tools.RODict({
        "ID": 330301,
        "mapID": 3303,
        "combatAreaID": 33038004,
        "refreshMonsterID": _tools.ROList([33030088]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11013004, 11013005, 11013006]),
        "countResetTime": 60
    }),
    330302: _tools.RODict({
        "ID": 330302,
        "mapID": 3303,
        "combatAreaID": 33038005,
        "refreshMonsterID": _tools.ROList([33030129]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11013004, 11013005, 11013006]),
        "countResetTime": 60
    }),
    330303: _tools.RODict({
        "ID": 330303,
        "mapID": 3303,
        "combatAreaID": 33038006,
        "refreshMonsterID": _tools.ROList([33030170]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11013004, 11013005, 11013006]),
        "countResetTime": 60
    }),
    330401: _tools.RODict({
        "ID": 330401,
        "mapID": 3304,
        "combatAreaID": 33048004,
        "refreshMonsterID": _tools.ROList([33040088]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11013004, 11013005, 11013006]),
        "countResetTime": 60
    }),
    330402: _tools.RODict({
        "ID": 330402,
        "mapID": 3304,
        "combatAreaID": 33048005,
        "refreshMonsterID": _tools.ROList([33040129]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11013004, 11013005, 11013006]),
        "countResetTime": 60
    }),
    330403: _tools.RODict({
        "ID": 330403,
        "mapID": 3304,
        "combatAreaID": 33048006,
        "refreshMonsterID": _tools.ROList([33040170]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11013004, 11013005, 11013006]),
        "countResetTime": 60
    }),
    330501: _tools.RODict({
        "ID": 330501,
        "mapID": 3305,
        "combatAreaID": 33058004,
        "refreshMonsterID": _tools.ROList([33050088]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11013004, 11013005, 11013006]),
        "countResetTime": 60
    }),
    330502: _tools.RODict({
        "ID": 330502,
        "mapID": 3305,
        "combatAreaID": 33058005,
        "refreshMonsterID": _tools.ROList([33050129]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11013004, 11013005, 11013006]),
        "countResetTime": 60
    }),
    330503: _tools.RODict({
        "ID": 330503,
        "mapID": 3305,
        "combatAreaID": 33058006,
        "refreshMonsterID": _tools.ROList([33050170]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11013004, 11013005, 11013006]),
        "countResetTime": 60
    }),
    331201: _tools.RODict({
        "ID": 331201,
        "mapID": 3312,
        "combatAreaID": 33128004,
        "refreshMonsterID": _tools.ROList([33120088]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11013011, 11013012, 11013013]),
        "countResetTime": 60
    }),
    331202: _tools.RODict({
        "ID": 331202,
        "mapID": 3312,
        "combatAreaID": 33128005,
        "refreshMonsterID": _tools.ROList([33120129]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11013011, 11013012, 11013013]),
        "countResetTime": 60
    }),
    331203: _tools.RODict({
        "ID": 331203,
        "mapID": 3312,
        "combatAreaID": 33128006,
        "refreshMonsterID": _tools.ROList([33120170]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11013011, 11013012, 11013013]),
        "countResetTime": 60
    }),
    331301: _tools.RODict({
        "ID": 331301,
        "mapID": 3313,
        "combatAreaID": 33138004,
        "refreshMonsterID": _tools.ROList([33130088]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11013011, 11013012, 11013013]),
        "countResetTime": 60
    }),
    331302: _tools.RODict({
        "ID": 331302,
        "mapID": 3313,
        "combatAreaID": 33138005,
        "refreshMonsterID": _tools.ROList([33130129]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11013011, 11013012, 11013013]),
        "countResetTime": 60
    }),
    331303: _tools.RODict({
        "ID": 331303,
        "mapID": 3313,
        "combatAreaID": 33138006,
        "refreshMonsterID": _tools.ROList([33130170]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11013011, 11013012, 11013013]),
        "countResetTime": 60
    }),
    331401: _tools.RODict({
        "ID": 331401,
        "mapID": 3314,
        "combatAreaID": 33148004,
        "refreshMonsterID": _tools.ROList([33140088]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11013011, 11013012, 11013013]),
        "countResetTime": 60
    }),
    331402: _tools.RODict({
        "ID": 331402,
        "mapID": 3314,
        "combatAreaID": 33148005,
        "refreshMonsterID": _tools.ROList([33140129]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11013011, 11013012, 11013013]),
        "countResetTime": 60
    }),
    331403: _tools.RODict({
        "ID": 331403,
        "mapID": 3314,
        "combatAreaID": 33148006,
        "refreshMonsterID": _tools.ROList([33140170]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11013011, 11013012, 11013013]),
        "countResetTime": 60
    }),
    331801: _tools.RODict({
        "ID": 331801,
        "mapID": 3318,
        "combatAreaID": 33188004,
        "refreshMonsterID": _tools.ROList([33180088]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11013046, 11013047, 11013048]),
        "countResetTime": 60
    }),
    331802: _tools.RODict({
        "ID": 331802,
        "mapID": 3318,
        "combatAreaID": 33188005,
        "refreshMonsterID": _tools.ROList([33180129]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11013046, 11013047, 11013048]),
        "countResetTime": 60
    }),
    331803: _tools.RODict({
        "ID": 331803,
        "mapID": 3318,
        "combatAreaID": 33188006,
        "refreshMonsterID": _tools.ROList([33180170]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11013046, 11013047, 11013048]),
        "countResetTime": 60
    }),
    331901: _tools.RODict({
        "ID": 331901,
        "mapID": 3319,
        "combatAreaID": 33198004,
        "refreshMonsterID": _tools.ROList([33190088]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11013050, 11013051, 11013052]),
        "countResetTime": 60
    }),
    331902: _tools.RODict({
        "ID": 331902,
        "mapID": 3319,
        "combatAreaID": 33198005,
        "refreshMonsterID": _tools.ROList([33190129]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11013050, 11013051, 11013052]),
        "countResetTime": 60
    }),
    331903: _tools.RODict({
        "ID": 331903,
        "mapID": 3319,
        "combatAreaID": 33198006,
        "refreshMonsterID": _tools.ROList([33190170]),
        "countLimit": 1000,
        "countMonsterID": _tools.ROList([11013050, 11013051, 11013052]),
        "countResetTime": 60
    }),
    332001: _tools.RODict({
        "ID": 332001,
        "mapID": 3320,
        "combatAreaID": 33208008,
        "refreshMonsterID": _tools.ROList([33200096, 33200104]),
        "countLimit": 100,
        "countMonsterID": _tools.ROList([11013030, 11013033, 11013032]),
        "countResetTime": 60
    }),
    332002: _tools.RODict({
        "ID": 332002,
        "mapID": 3320,
        "combatAreaID": 33208008,
        "refreshMonsterID": _tools.ROList([33200112, 33200120]),
        "countLimit": 100,
        "countMonsterID": _tools.ROList([11013035, 11013036, 11013037]),
        "countResetTime": 60
    }),
    332003: _tools.RODict({
        "ID": 332003,
        "mapID": 3320,
        "combatAreaID": 33208008,
        "refreshMonsterID": _tools.ROList([33200129, 33200137]),
        "countLimit": 100,
        "countMonsterID": _tools.ROList([11013040, 11013041, 11013042]),
        "countResetTime": 60
    }),
    332004: _tools.RODict({
        "ID": 332004,
        "mapID": 3320,
        "combatAreaID": 33208008,
        "refreshMonsterID": _tools.ROList([33200168]),
        "countLimit": 60,
        "countMonsterID": _tools.ROList([11013033, 11013034, 11013038, 11013039, 11013043, 11013044]),
        "countResetTime": 150
    })
})
minKey = 310301
maxKey = 332004

refreshMonsterIDIndex = {310331030088: 310301, 310331030129: 310302, 310331030170: 310303, 310431040088: 310401, 310431040129: 310402, 310431040170: 310403, 310531050088: 310501, 310531050129: 310502, 310531050170: 310503, 311231120088: 311201, 311231120129: 311202, 311231120170: 311203, 311331130088: 311301, 311331130129: 311302, 311331130170: 311303, 311431140088: 311401, 311431140129: 311402, 311431140170: 311403, 311831180088: 311801, 311831180129: 311802, 311831180170: 311803, 311931190088: 311901, 311931190129: 311902, 311931190170: 311903, 312031200096: 312001, 312031200104: 312001, 312031200112: 312002, 312031200120: 312002, 312031200129: 312003, 312031200137: 312003, 312031200168: 312004, 320332030088: 320301, 320332030129: 320302, 320332030170: 320303, 320432040088: 320401, 320432040129: 320402, 320432040170: 320403, 320532050088: 320501, 320532050129: 320502, 320532050170: 320503, 321232120088: 321201, 321232120129: 321202, 321232120170: 321203, 321332130088: 321301, 321332130129: 321302, 321332130170: 321303, 321432140088: 321401, 321432140129: 321402, 321432140170: 321403, 321832180088: 321801, 321832180129: 321802, 321832180170: 321803, 321932190088: 321901, 321932190129: 321902, 321932190170: 321903, 322032200096: 322001, 322032200104: 322001, 322032200112: 322002, 322032200120: 322002, 322032200129: 322003, 322032200137: 322003, 322032200168: 322004, 330333030088: 330301, 330333030129: 330302, 330333030170: 330303, 330433040088: 330401, 330433040129: 330402, 330433040170: 330403, 330533050088: 330501, 330533050129: 330502, 330533050170: 330503, 331233120088: 331201, 331233120129: 331202, 331233120170: 331203, 331333130088: 331301, 331333130129: 331302, 331333130170: 331303, 331433140088: 331401, 331433140129: 331402, 331433140170: 331403, 331833180088: 331801, 331833180129: 331802, 331833180170: 331803, 331933190088: 331901, 331933190129: 331902, 331933190170: 331903, 332033200096: 332001, 332033200104: 332001, 332033200112: 332002, 332033200120: 332002, 332033200129: 332003, 332033200137: 332003, 332033200168: 332004}


mapIDIndex = {3103: [310301, 310302, 310303], 3104: [310401, 310402, 310403], 3105: [310501, 310502, 310503], 3112: [311201, 311202, 311203], 3113: [311301, 311302, 311303], 3114: [311401, 311402, 311403], 3118: [311801, 311802, 311803], 3119: [311901, 311902, 311903], 3120: [312001, 312002, 312003, 312004], 3203: [320301, 320302, 320303], 3204: [320401, 320402, 320403], 3205: [320501, 320502, 320503], 3212: [321201, 321202, 321203], 3213: [321301, 321302, 321303], 3214: [321401, 321402, 321403], 3218: [321801, 321802, 321803], 3219: [321901, 321902, 321903], 3220: [322001, 322002, 322003, 322004], 3303: [330301, 330302, 330303], 3304: [330401, 330402, 330403], 3305: [330501, 330502, 330503], 3312: [331201, 331202, 331203], 3313: [331301, 331302, 331303], 3314: [331401, 331402, 331403], 3318: [331801, 331802, 331803], 3319: [331901, 331902, 331903], 3320: [332001, 332002, 332003, 332004]}


combatAreaIdxDic = {31038004: [310301], 31038005: [310302], 31038006: [310303], 31048004: [310401], 31048005: [310402], 31048006: [310403], 31058004: [310501], 31058005: [310502], 31058006: [310503], 31128004: [311201], 31128005: [311202], 31128006: [311203], 31138004: [311301], 31138005: [311302], 31138006: [311303], 31148004: [311401], 31148005: [311402], 31148006: [311403], 31188004: [311801], 31188005: [311802], 31188006: [311803], 31198004: [311901], 31198005: [311902], 31198006: [311903], 31208008: [312001, 312002, 312003, 312004], 32038004: [320301], 32038005: [320302], 32038006: [320303], 32048004: [320401], 32048005: [320402], 32048006: [320403], 32058004: [320501], 32058005: [320502], 32058006: [320503], 32128004: [321201], 32128005: [321202], 32128006: [321203], 32138004: [321301], 32138005: [321302], 32138006: [321303], 32148004: [321401], 32148005: [321402], 32148006: [321403], 32188004: [321801], 32188005: [321802], 32188006: [321803], 32198004: [321901], 32198005: [321902], 32198006: [321903], 32208008: [322001, 322002, 322003, 322004], 33038004: [330301], 33038005: [330302], 33038006: [330303], 33048004: [330401], 33048005: [330402], 33048006: [330403], 33058004: [330501], 33058005: [330502], 33058006: [330503], 33128004: [331201], 33128005: [331202], 33128006: [331203], 33138004: [331301], 33138005: [331302], 33138006: [331303], 33148004: [331401], 33148005: [331402], 33148006: [331403], 33188004: [331801], 33188005: [331802], 33188006: [331803], 33198004: [331901], 33198005: [331902], 33198006: [331903], 33208008: [332001, 332002, 332003, 332004]}
