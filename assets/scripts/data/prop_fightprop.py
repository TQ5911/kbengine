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
        "propList": _tools.RODict({"adjFullHp":20000,"adjFullMp":10000,"adjMinPhysicalAtk":100,"adjMaxPhysicalAtk":200,"adjMinMagicAtk":100,"adjMaxMagicAtk":200,"mulFullHp":1})
    }),
    52001001: _tools.RODict({
        "propID": 52001001,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":42,"adjMinMagicAtk":22,"adjMaxMagicAtk":42,"adjHit":5})
    }),
    52001002: _tools.RODict({
        "propID": 52001002,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":28,"adjMaxPhysicalAtk":48,"adjMinMagicAtk":28,"adjMaxMagicAtk":48,"adjHit":7})
    }),
    52001003: _tools.RODict({
        "propID": 52001003,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":58,"adjMinMagicAtk":30,"adjMaxMagicAtk":58,"adjHit":9})
    }),
    52001004: _tools.RODict({
        "propID": 52001004,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":34,"adjMaxPhysicalAtk":64,"adjMinMagicAtk":34,"adjMaxMagicAtk":64,"adjHit":15})
    }),
    52001005: _tools.RODict({
        "propID": 52001005,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":42,"adjMaxPhysicalAtk":78,"adjMinMagicAtk":42,"adjMaxMagicAtk":78,"adjHit":18})
    }),
    52001006: _tools.RODict({
        "propID": 52001006,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":48,"adjMaxPhysicalAtk":90,"adjMinMagicAtk":48,"adjMaxMagicAtk":90,"adjHit":21})
    }),
    52001007: _tools.RODict({
        "propID": 52001007,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":54,"adjMaxPhysicalAtk":102,"adjMinMagicAtk":54,"adjMaxMagicAtk":102,"adjHit":24})
    }),
    52001008: _tools.RODict({
        "propID": 52001008,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":60,"adjMaxPhysicalAtk":114,"adjMinMagicAtk":60,"adjMaxMagicAtk":114,"adjHit":33,"adjFatal":10})
    }),
    52001009: _tools.RODict({
        "propID": 52001009,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":76,"adjMaxPhysicalAtk":142,"adjMinMagicAtk":76,"adjMaxMagicAtk":142,"adjHit":36,"adjFatal":15})
    }),
    52001010: _tools.RODict({
        "propID": 52001010,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":84,"adjMaxPhysicalAtk":160,"adjMinMagicAtk":84,"adjMaxMagicAtk":160,"adjHit":42,"adjFatal":20})
    }),
    52001011: _tools.RODict({
        "propID": 52001011,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":96,"adjMaxPhysicalAtk":180,"adjMinMagicAtk":96,"adjMaxMagicAtk":180,"adjHit":45,"adjFatal":25})
    }),
    52001012: _tools.RODict({
        "propID": 52001012,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":108,"adjMaxPhysicalAtk":204,"adjMinMagicAtk":108,"adjMaxMagicAtk":204,"adjHit":48,"adjFatal":30})
    }),
    52001013: _tools.RODict({
        "propID": 52001013,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":76,"adjMaxPhysicalAtk":142,"adjMinMagicAtk":76,"adjMaxMagicAtk":142,"adjHit":36,"adjIgnoreArmor":0.01})
    }),
    52001014: _tools.RODict({
        "propID": 52001014,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":84,"adjMaxPhysicalAtk":160,"adjMinMagicAtk":84,"adjMaxMagicAtk":160,"adjHit":42,"adjIgnoreArmor":0.014})
    }),
    52001015: _tools.RODict({
        "propID": 52001015,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":96,"adjMaxPhysicalAtk":180,"adjMinMagicAtk":96,"adjMaxMagicAtk":180,"adjHit":45,"adjIgnoreArmor":0.018})
    }),
    52001016: _tools.RODict({
        "propID": 52001016,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":108,"adjMaxPhysicalAtk":204,"adjMinMagicAtk":108,"adjMaxMagicAtk":204,"adjHit":48,"adjIgnoreArmor":0.021})
    }),
    52001017: _tools.RODict({
        "propID": 52001017,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":132,"adjMaxPhysicalAtk":246,"adjMinMagicAtk":132,"adjMaxMagicAtk":246,"adjHit":54,"adjFatal":40,"adjFinalDmg":0.01})
    }),
    52001018: _tools.RODict({
        "propID": 52001018,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":150,"adjMaxPhysicalAtk":280,"adjMinMagicAtk":150,"adjMaxMagicAtk":280,"adjHit":57,"adjFatal":50,"adjFinalDmg":0.015})
    }),
    52001019: _tools.RODict({
        "propID": 52001019,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":172,"adjMaxPhysicalAtk":318,"adjMinMagicAtk":172,"adjMaxMagicAtk":318,"adjHit":60,"adjFatal":60,"adjFinalDmg":0.02})
    }),
    52001020: _tools.RODict({
        "propID": 52001020,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":192,"adjMaxPhysicalAtk":360,"adjMinMagicAtk":192,"adjMaxMagicAtk":360,"adjHit":66,"adjFatal":80,"adjFinalDmg":0.03})
    }),
    52001021: _tools.RODict({
        "propID": 52001021,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":132,"adjMaxPhysicalAtk":246,"adjMinMagicAtk":132,"adjMaxMagicAtk":246,"adjHit":54,"adjIgnoreArmor":0.028,"adjRealDmg":2})
    }),
    52001022: _tools.RODict({
        "propID": 52001022,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":150,"adjMaxPhysicalAtk":280,"adjMinMagicAtk":150,"adjMaxMagicAtk":280,"adjHit":57,"adjIgnoreArmor":0.035,"adjRealDmg":3})
    }),
    52001023: _tools.RODict({
        "propID": 52001023,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":172,"adjMaxPhysicalAtk":318,"adjMinMagicAtk":172,"adjMaxMagicAtk":318,"adjHit":60,"adjIgnoreArmor":0.042,"adjRealDmg":4})
    }),
    52001024: _tools.RODict({
        "propID": 52001024,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":192,"adjMaxPhysicalAtk":360,"adjMinMagicAtk":192,"adjMaxMagicAtk":360,"adjHit":66,"adjIgnoreArmor":0.056,"adjRealDmg":6})
    }),
    52001025: _tools.RODict({
        "propID": 52001025,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":42,"adjMinMagicAtk":22,"adjMaxMagicAtk":42,"adjHit":5})
    }),
    52001026: _tools.RODict({
        "propID": 52001026,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":28,"adjMaxPhysicalAtk":48,"adjMinMagicAtk":28,"adjMaxMagicAtk":48,"adjHit":7})
    }),
    52001027: _tools.RODict({
        "propID": 52001027,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":58,"adjMinMagicAtk":30,"adjMaxMagicAtk":58,"adjHit":9})
    }),
    52001028: _tools.RODict({
        "propID": 52001028,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":34,"adjMaxPhysicalAtk":64,"adjMinMagicAtk":34,"adjMaxMagicAtk":64,"adjHit":15})
    }),
    52001029: _tools.RODict({
        "propID": 52001029,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":42,"adjMaxPhysicalAtk":78,"adjMinMagicAtk":42,"adjMaxMagicAtk":78,"adjHit":18})
    }),
    52001030: _tools.RODict({
        "propID": 52001030,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":48,"adjMaxPhysicalAtk":90,"adjMinMagicAtk":48,"adjMaxMagicAtk":90,"adjHit":21})
    }),
    52001031: _tools.RODict({
        "propID": 52001031,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":54,"adjMaxPhysicalAtk":102,"adjMinMagicAtk":54,"adjMaxMagicAtk":102,"adjHit":24})
    }),
    52001032: _tools.RODict({
        "propID": 52001032,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":60,"adjMaxPhysicalAtk":114,"adjMinMagicAtk":60,"adjMaxMagicAtk":114,"adjHit":33,"adjFatal":10})
    }),
    52001033: _tools.RODict({
        "propID": 52001033,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":76,"adjMaxPhysicalAtk":142,"adjMinMagicAtk":76,"adjMaxMagicAtk":142,"adjHit":36,"adjFatal":15})
    }),
    52001034: _tools.RODict({
        "propID": 52001034,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":84,"adjMaxPhysicalAtk":160,"adjMinMagicAtk":84,"adjMaxMagicAtk":160,"adjHit":42,"adjFatal":20})
    }),
    52001035: _tools.RODict({
        "propID": 52001035,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":96,"adjMaxPhysicalAtk":180,"adjMinMagicAtk":96,"adjMaxMagicAtk":180,"adjHit":45,"adjFatal":25})
    }),
    52001036: _tools.RODict({
        "propID": 52001036,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":108,"adjMaxPhysicalAtk":204,"adjMinMagicAtk":108,"adjMaxMagicAtk":204,"adjHit":48,"adjFatal":30})
    }),
    52001037: _tools.RODict({
        "propID": 52001037,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":76,"adjMaxPhysicalAtk":142,"adjMinMagicAtk":76,"adjMaxMagicAtk":142,"adjHit":36,"adjIgnoreArmor":0.01})
    }),
    52001038: _tools.RODict({
        "propID": 52001038,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":84,"adjMaxPhysicalAtk":160,"adjMinMagicAtk":84,"adjMaxMagicAtk":160,"adjHit":42,"adjIgnoreArmor":0.014})
    }),
    52001039: _tools.RODict({
        "propID": 52001039,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":96,"adjMaxPhysicalAtk":180,"adjMinMagicAtk":96,"adjMaxMagicAtk":180,"adjHit":45,"adjIgnoreArmor":0.018})
    }),
    52001040: _tools.RODict({
        "propID": 52001040,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":108,"adjMaxPhysicalAtk":204,"adjMinMagicAtk":108,"adjMaxMagicAtk":204,"adjHit":48,"adjIgnoreArmor":0.021})
    }),
    52001041: _tools.RODict({
        "propID": 52001041,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":132,"adjMaxPhysicalAtk":246,"adjMinMagicAtk":132,"adjMaxMagicAtk":246,"adjHit":54,"adjFatal":40,"adjFinalDmg":0.01})
    }),
    52001042: _tools.RODict({
        "propID": 52001042,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":150,"adjMaxPhysicalAtk":280,"adjMinMagicAtk":150,"adjMaxMagicAtk":280,"adjHit":57,"adjFatal":50,"adjFinalDmg":0.015})
    }),
    52001043: _tools.RODict({
        "propID": 52001043,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":172,"adjMaxPhysicalAtk":318,"adjMinMagicAtk":172,"adjMaxMagicAtk":318,"adjHit":60,"adjFatal":60,"adjFinalDmg":0.02})
    }),
    52001044: _tools.RODict({
        "propID": 52001044,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":192,"adjMaxPhysicalAtk":360,"adjMinMagicAtk":192,"adjMaxMagicAtk":360,"adjHit":66,"adjFatal":80,"adjFinalDmg":0.03})
    }),
    52001045: _tools.RODict({
        "propID": 52001045,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":132,"adjMaxPhysicalAtk":246,"adjMinMagicAtk":132,"adjMaxMagicAtk":246,"adjHit":54,"adjIgnoreArmor":0.028,"adjRealDmg":2})
    }),
    52001046: _tools.RODict({
        "propID": 52001046,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":150,"adjMaxPhysicalAtk":280,"adjMinMagicAtk":150,"adjMaxMagicAtk":280,"adjHit":57,"adjIgnoreArmor":0.035,"adjRealDmg":3})
    }),
    52001047: _tools.RODict({
        "propID": 52001047,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":172,"adjMaxPhysicalAtk":318,"adjMinMagicAtk":172,"adjMaxMagicAtk":318,"adjHit":60,"adjIgnoreArmor":0.042,"adjRealDmg":4})
    }),
    52001048: _tools.RODict({
        "propID": 52001048,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":192,"adjMaxPhysicalAtk":360,"adjMinMagicAtk":192,"adjMaxMagicAtk":360,"adjHit":66,"adjIgnoreArmor":0.056,"adjRealDmg":6})
    }),
    52001049: _tools.RODict({
        "propID": 52001049,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":42,"adjMinMagicAtk":22,"adjMaxMagicAtk":42,"adjHit":5})
    }),
    52001050: _tools.RODict({
        "propID": 52001050,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":28,"adjMaxPhysicalAtk":48,"adjMinMagicAtk":28,"adjMaxMagicAtk":48,"adjHit":7})
    }),
    52001051: _tools.RODict({
        "propID": 52001051,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":58,"adjMinMagicAtk":30,"adjMaxMagicAtk":58,"adjHit":9})
    }),
    52001052: _tools.RODict({
        "propID": 52001052,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":34,"adjMaxPhysicalAtk":64,"adjMinMagicAtk":34,"adjMaxMagicAtk":64,"adjHit":15})
    }),
    52001053: _tools.RODict({
        "propID": 52001053,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":42,"adjMaxPhysicalAtk":78,"adjMinMagicAtk":42,"adjMaxMagicAtk":78,"adjHit":18})
    }),
    52001054: _tools.RODict({
        "propID": 52001054,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":48,"adjMaxPhysicalAtk":90,"adjMinMagicAtk":48,"adjMaxMagicAtk":90,"adjHit":21})
    }),
    52001055: _tools.RODict({
        "propID": 52001055,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":54,"adjMaxPhysicalAtk":102,"adjMinMagicAtk":54,"adjMaxMagicAtk":102,"adjHit":24})
    }),
    52001056: _tools.RODict({
        "propID": 52001056,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":60,"adjMaxPhysicalAtk":114,"adjMinMagicAtk":60,"adjMaxMagicAtk":114,"adjHit":33,"adjFatal":10})
    }),
    52001057: _tools.RODict({
        "propID": 52001057,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":76,"adjMaxPhysicalAtk":142,"adjMinMagicAtk":76,"adjMaxMagicAtk":142,"adjHit":36,"adjFatal":15})
    }),
    52001058: _tools.RODict({
        "propID": 52001058,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":84,"adjMaxPhysicalAtk":160,"adjMinMagicAtk":84,"adjMaxMagicAtk":160,"adjHit":42,"adjFatal":20})
    }),
    52001059: _tools.RODict({
        "propID": 52001059,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":96,"adjMaxPhysicalAtk":180,"adjMinMagicAtk":96,"adjMaxMagicAtk":180,"adjHit":45,"adjFatal":25})
    }),
    52001060: _tools.RODict({
        "propID": 52001060,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":108,"adjMaxPhysicalAtk":204,"adjMinMagicAtk":108,"adjMaxMagicAtk":204,"adjHit":48,"adjFatal":30})
    }),
    52001061: _tools.RODict({
        "propID": 52001061,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":76,"adjMaxPhysicalAtk":142,"adjMinMagicAtk":76,"adjMaxMagicAtk":142,"adjHit":36,"adjIgnoreArmor":0.01})
    }),
    52001062: _tools.RODict({
        "propID": 52001062,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":84,"adjMaxPhysicalAtk":160,"adjMinMagicAtk":84,"adjMaxMagicAtk":160,"adjHit":42,"adjIgnoreArmor":0.014})
    }),
    52001063: _tools.RODict({
        "propID": 52001063,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":96,"adjMaxPhysicalAtk":180,"adjMinMagicAtk":96,"adjMaxMagicAtk":180,"adjHit":45,"adjIgnoreArmor":0.018})
    }),
    52001064: _tools.RODict({
        "propID": 52001064,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":108,"adjMaxPhysicalAtk":204,"adjMinMagicAtk":108,"adjMaxMagicAtk":204,"adjHit":48,"adjIgnoreArmor":0.021})
    }),
    52001065: _tools.RODict({
        "propID": 52001065,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":132,"adjMaxPhysicalAtk":246,"adjMinMagicAtk":132,"adjMaxMagicAtk":246,"adjHit":54,"adjFatal":40,"adjFinalDmg":0.01})
    }),
    52001066: _tools.RODict({
        "propID": 52001066,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":150,"adjMaxPhysicalAtk":280,"adjMinMagicAtk":150,"adjMaxMagicAtk":280,"adjHit":57,"adjFatal":50,"adjFinalDmg":0.015})
    }),
    52001067: _tools.RODict({
        "propID": 52001067,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":172,"adjMaxPhysicalAtk":318,"adjMinMagicAtk":172,"adjMaxMagicAtk":318,"adjHit":60,"adjFatal":60,"adjFinalDmg":0.02})
    }),
    52001068: _tools.RODict({
        "propID": 52001068,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":192,"adjMaxPhysicalAtk":360,"adjMinMagicAtk":192,"adjMaxMagicAtk":360,"adjHit":66,"adjFatal":80,"adjFinalDmg":0.03})
    }),
    52001069: _tools.RODict({
        "propID": 52001069,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":132,"adjMaxPhysicalAtk":246,"adjMinMagicAtk":132,"adjMaxMagicAtk":246,"adjHit":54,"adjIgnoreArmor":0.028,"adjRealDmg":2})
    }),
    52001070: _tools.RODict({
        "propID": 52001070,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":150,"adjMaxPhysicalAtk":280,"adjMinMagicAtk":150,"adjMaxMagicAtk":280,"adjHit":57,"adjIgnoreArmor":0.035,"adjRealDmg":3})
    }),
    52001071: _tools.RODict({
        "propID": 52001071,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":172,"adjMaxPhysicalAtk":318,"adjMinMagicAtk":172,"adjMaxMagicAtk":318,"adjHit":60,"adjIgnoreArmor":0.042,"adjRealDmg":4})
    }),
    52001072: _tools.RODict({
        "propID": 52001072,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":192,"adjMaxPhysicalAtk":360,"adjMinMagicAtk":192,"adjMaxMagicAtk":360,"adjHit":66,"adjIgnoreArmor":0.056,"adjRealDmg":6})
    }),
    52001073: _tools.RODict({
        "propID": 52001073,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":48,"adjMinPhysicalArmor":3,"adjMaxPhysicalArmor":3,"adjMinMagicArmor":3,"adjMaxMagicArmor":3})
    }),
    52001074: _tools.RODict({
        "propID": 52001074,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":56,"adjMinPhysicalArmor":4,"adjMaxPhysicalArmor":4,"adjMinMagicArmor":4,"adjMaxMagicArmor":4})
    }),
    52001075: _tools.RODict({
        "propID": 52001075,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":64,"adjMinPhysicalArmor":6,"adjMaxPhysicalArmor":6,"adjMinMagicArmor":6,"adjMaxMagicArmor":6})
    }),
    52001076: _tools.RODict({
        "propID": 52001076,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":80,"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10})
    }),
    52001077: _tools.RODict({
        "propID": 52001077,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":88,"adjMinPhysicalArmor":12,"adjMaxPhysicalArmor":12,"adjMinMagicArmor":12,"adjMaxMagicArmor":12})
    }),
    52001078: _tools.RODict({
        "propID": 52001078,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":96,"adjMinPhysicalArmor":12,"adjMaxPhysicalArmor":12,"adjMinMagicArmor":12,"adjMaxMagicArmor":12})
    }),
    52001079: _tools.RODict({
        "propID": 52001079,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":104,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16})
    }),
    52001080: _tools.RODict({
        "propID": 52001080,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":144,"adjMinPhysicalArmor":22,"adjMaxPhysicalArmor":22,"adjMinMagicArmor":22,"adjMaxMagicArmor":22,"adjAntiFatal":10})
    }),
    52001081: _tools.RODict({
        "propID": 52001081,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":168,"adjMinPhysicalArmor":25,"adjMaxPhysicalArmor":25,"adjMinMagicArmor":25,"adjMaxMagicArmor":25,"adjAntiFatal":15})
    }),
    52001082: _tools.RODict({
        "propID": 52001082,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":192,"adjMinPhysicalArmor":28,"adjMaxPhysicalArmor":28,"adjMinMagicArmor":28,"adjMaxMagicArmor":28,"adjAntiFatal":20})
    }),
    52001083: _tools.RODict({
        "propID": 52001083,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":240,"adjMinPhysicalArmor":31,"adjMaxPhysicalArmor":31,"adjMinMagicArmor":31,"adjMaxMagicArmor":31,"adjAntiFatal":25})
    }),
    52001084: _tools.RODict({
        "propID": 52001084,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":288,"adjMinPhysicalArmor":34,"adjMaxPhysicalArmor":34,"adjMinMagicArmor":34,"adjMaxMagicArmor":34,"adjAntiFatal":30})
    }),
    52001085: _tools.RODict({
        "propID": 52001085,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":192,"adjMinPhysicalArmor":28,"adjMaxPhysicalArmor":28,"adjMinMagicArmor":28,"adjMaxMagicArmor":28,"adjMonsterDmgAnti":0.01})
    }),
    52001086: _tools.RODict({
        "propID": 52001086,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":240,"adjMinPhysicalArmor":31,"adjMaxPhysicalArmor":31,"adjMinMagicArmor":31,"adjMaxMagicArmor":31,"adjMonsterDmgAnti":0.0125})
    }),
    52001087: _tools.RODict({
        "propID": 52001087,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":288,"adjMinPhysicalArmor":34,"adjMaxPhysicalArmor":34,"adjMinMagicArmor":34,"adjMaxMagicArmor":34,"adjMonsterDmgAnti":0.015})
    }),
    52001088: _tools.RODict({
        "propID": 52001088,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":384,"adjMinPhysicalArmor":43,"adjMaxPhysicalArmor":43,"adjMinMagicArmor":43,"adjMaxMagicArmor":43,"adjAntiFatal":40,"adjFinalDmgAnti":0.01})
    }),
    52001089: _tools.RODict({
        "propID": 52001089,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":432,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":50,"adjMaxMagicArmor":50,"adjAntiFatal":50,"adjFinalDmgAnti":0.015})
    }),
    52001090: _tools.RODict({
        "propID": 52001090,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":480,"adjMinPhysicalArmor":54,"adjMaxPhysicalArmor":54,"adjMinMagicArmor":54,"adjMaxMagicArmor":54,"adjAntiFatal":60,"adjFinalDmgAnti":0.02})
    }),
    52001091: _tools.RODict({
        "propID": 52001091,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":528,"adjMinPhysicalArmor":61,"adjMaxPhysicalArmor":61,"adjMinMagicArmor":61,"adjMaxMagicArmor":61,"adjAntiFatal":80,"adjFinalDmgAnti":0.03})
    }),
    52001092: _tools.RODict({
        "propID": 52001092,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":384,"adjMinPhysicalArmor":43,"adjMaxPhysicalArmor":43,"adjMinMagicArmor":43,"adjMaxMagicArmor":43,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.02})
    }),
    52001093: _tools.RODict({
        "propID": 52001093,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":432,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":50,"adjMaxMagicArmor":50,"adjRealDmgDef":3,"adjMonsterDmgAnti":0.025})
    }),
    52001094: _tools.RODict({
        "propID": 52001094,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":480,"adjMinPhysicalArmor":54,"adjMaxPhysicalArmor":54,"adjMinMagicArmor":54,"adjMaxMagicArmor":54,"adjRealDmgDef":4,"adjMonsterDmgAnti":0.03})
    }),
    52001095: _tools.RODict({
        "propID": 52001095,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":528,"adjMinPhysicalArmor":61,"adjMaxPhysicalArmor":61,"adjMinMagicArmor":61,"adjMaxMagicArmor":61,"adjRealDmgDef":6,"adjMonsterDmgAnti":0.04})
    }),
    52001096: _tools.RODict({
        "propID": 52001096,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":48,"adjMinPhysicalArmor":3,"adjMaxPhysicalArmor":3,"adjMinMagicArmor":3,"adjMaxMagicArmor":3})
    }),
    52001097: _tools.RODict({
        "propID": 52001097,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":56,"adjMinPhysicalArmor":4,"adjMaxPhysicalArmor":4,"adjMinMagicArmor":4,"adjMaxMagicArmor":4})
    }),
    52001098: _tools.RODict({
        "propID": 52001098,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":64,"adjMinPhysicalArmor":6,"adjMaxPhysicalArmor":6,"adjMinMagicArmor":6,"adjMaxMagicArmor":6})
    }),
    52001099: _tools.RODict({
        "propID": 52001099,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":80,"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10})
    }),
    52001100: _tools.RODict({
        "propID": 52001100,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":88,"adjMinPhysicalArmor":12,"adjMaxPhysicalArmor":12,"adjMinMagicArmor":12,"adjMaxMagicArmor":12})
    }),
    52001101: _tools.RODict({
        "propID": 52001101,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":96,"adjMinPhysicalArmor":12,"adjMaxPhysicalArmor":12,"adjMinMagicArmor":12,"adjMaxMagicArmor":12})
    }),
    52001102: _tools.RODict({
        "propID": 52001102,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":104,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16})
    }),
    52001103: _tools.RODict({
        "propID": 52001103,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":144,"adjMinPhysicalArmor":22,"adjMaxPhysicalArmor":22,"adjMinMagicArmor":22,"adjMaxMagicArmor":22,"adjAntiFatal":10})
    }),
    52001104: _tools.RODict({
        "propID": 52001104,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":168,"adjMinPhysicalArmor":25,"adjMaxPhysicalArmor":25,"adjMinMagicArmor":25,"adjMaxMagicArmor":25,"adjAntiFatal":15})
    }),
    52001105: _tools.RODict({
        "propID": 52001105,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":192,"adjMinPhysicalArmor":28,"adjMaxPhysicalArmor":28,"adjMinMagicArmor":28,"adjMaxMagicArmor":28,"adjAntiFatal":20})
    }),
    52001106: _tools.RODict({
        "propID": 52001106,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":240,"adjMinPhysicalArmor":31,"adjMaxPhysicalArmor":31,"adjMinMagicArmor":31,"adjMaxMagicArmor":31,"adjAntiFatal":25})
    }),
    52001107: _tools.RODict({
        "propID": 52001107,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":288,"adjMinPhysicalArmor":34,"adjMaxPhysicalArmor":34,"adjMinMagicArmor":34,"adjMaxMagicArmor":34,"adjAntiFatal":30})
    }),
    52001108: _tools.RODict({
        "propID": 52001108,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":192,"adjMinPhysicalArmor":28,"adjMaxPhysicalArmor":28,"adjMinMagicArmor":28,"adjMaxMagicArmor":28,"adjMonsterDmgAnti":0.01})
    }),
    52001109: _tools.RODict({
        "propID": 52001109,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":240,"adjMinPhysicalArmor":31,"adjMaxPhysicalArmor":31,"adjMinMagicArmor":31,"adjMaxMagicArmor":31,"adjMonsterDmgAnti":0.0125})
    }),
    52001110: _tools.RODict({
        "propID": 52001110,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":288,"adjMinPhysicalArmor":34,"adjMaxPhysicalArmor":34,"adjMinMagicArmor":34,"adjMaxMagicArmor":34,"adjMonsterDmgAnti":0.015})
    }),
    52001111: _tools.RODict({
        "propID": 52001111,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":384,"adjMinPhysicalArmor":43,"adjMaxPhysicalArmor":43,"adjMinMagicArmor":43,"adjMaxMagicArmor":43,"adjAntiFatal":40,"adjFinalDmgAnti":0.01})
    }),
    52001112: _tools.RODict({
        "propID": 52001112,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":432,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":50,"adjMaxMagicArmor":50,"adjAntiFatal":50,"adjFinalDmgAnti":0.015})
    }),
    52001113: _tools.RODict({
        "propID": 52001113,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":480,"adjMinPhysicalArmor":54,"adjMaxPhysicalArmor":54,"adjMinMagicArmor":54,"adjMaxMagicArmor":54,"adjAntiFatal":60,"adjFinalDmgAnti":0.02})
    }),
    52001114: _tools.RODict({
        "propID": 52001114,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":528,"adjMinPhysicalArmor":61,"adjMaxPhysicalArmor":61,"adjMinMagicArmor":61,"adjMaxMagicArmor":61,"adjAntiFatal":80,"adjFinalDmgAnti":0.03})
    }),
    52001115: _tools.RODict({
        "propID": 52001115,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":384,"adjMinPhysicalArmor":43,"adjMaxPhysicalArmor":43,"adjMinMagicArmor":43,"adjMaxMagicArmor":43,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.02})
    }),
    52001116: _tools.RODict({
        "propID": 52001116,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":432,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":50,"adjMaxMagicArmor":50,"adjRealDmgDef":3,"adjMonsterDmgAnti":0.025})
    }),
    52001117: _tools.RODict({
        "propID": 52001117,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":480,"adjMinPhysicalArmor":54,"adjMaxPhysicalArmor":54,"adjMinMagicArmor":54,"adjMaxMagicArmor":54,"adjRealDmgDef":4,"adjMonsterDmgAnti":0.03})
    }),
    52001118: _tools.RODict({
        "propID": 52001118,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":528,"adjMinPhysicalArmor":61,"adjMaxPhysicalArmor":61,"adjMinMagicArmor":61,"adjMaxMagicArmor":61,"adjRealDmgDef":6,"adjMonsterDmgAnti":0.04})
    }),
    52001119: _tools.RODict({
        "propID": 52001119,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":48,"adjMinPhysicalArmor":3,"adjMaxPhysicalArmor":3,"adjMinMagicArmor":3,"adjMaxMagicArmor":3})
    }),
    52001120: _tools.RODict({
        "propID": 52001120,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":56,"adjMinPhysicalArmor":4,"adjMaxPhysicalArmor":4,"adjMinMagicArmor":4,"adjMaxMagicArmor":4})
    }),
    52001121: _tools.RODict({
        "propID": 52001121,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":64,"adjMinPhysicalArmor":6,"adjMaxPhysicalArmor":6,"adjMinMagicArmor":6,"adjMaxMagicArmor":6})
    }),
    52001122: _tools.RODict({
        "propID": 52001122,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":80,"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10})
    }),
    52001123: _tools.RODict({
        "propID": 52001123,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":88,"adjMinPhysicalArmor":12,"adjMaxPhysicalArmor":12,"adjMinMagicArmor":12,"adjMaxMagicArmor":12})
    }),
    52001124: _tools.RODict({
        "propID": 52001124,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":96,"adjMinPhysicalArmor":12,"adjMaxPhysicalArmor":12,"adjMinMagicArmor":12,"adjMaxMagicArmor":12})
    }),
    52001125: _tools.RODict({
        "propID": 52001125,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":104,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16})
    }),
    52001126: _tools.RODict({
        "propID": 52001126,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":144,"adjMinPhysicalArmor":22,"adjMaxPhysicalArmor":22,"adjMinMagicArmor":22,"adjMaxMagicArmor":22,"adjAntiFatal":10})
    }),
    52001127: _tools.RODict({
        "propID": 52001127,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":168,"adjMinPhysicalArmor":25,"adjMaxPhysicalArmor":25,"adjMinMagicArmor":25,"adjMaxMagicArmor":25,"adjAntiFatal":15})
    }),
    52001128: _tools.RODict({
        "propID": 52001128,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":192,"adjMinPhysicalArmor":28,"adjMaxPhysicalArmor":28,"adjMinMagicArmor":28,"adjMaxMagicArmor":28,"adjAntiFatal":20})
    }),
    52001129: _tools.RODict({
        "propID": 52001129,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":240,"adjMinPhysicalArmor":31,"adjMaxPhysicalArmor":31,"adjMinMagicArmor":31,"adjMaxMagicArmor":31,"adjAntiFatal":25})
    }),
    52001130: _tools.RODict({
        "propID": 52001130,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":288,"adjMinPhysicalArmor":34,"adjMaxPhysicalArmor":34,"adjMinMagicArmor":34,"adjMaxMagicArmor":34,"adjAntiFatal":30})
    }),
    52001131: _tools.RODict({
        "propID": 52001131,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":192,"adjMinPhysicalArmor":28,"adjMaxPhysicalArmor":28,"adjMinMagicArmor":28,"adjMaxMagicArmor":28,"adjMonsterDmgAnti":0.01})
    }),
    52001132: _tools.RODict({
        "propID": 52001132,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":240,"adjMinPhysicalArmor":31,"adjMaxPhysicalArmor":31,"adjMinMagicArmor":31,"adjMaxMagicArmor":31,"adjMonsterDmgAnti":0.0125})
    }),
    52001133: _tools.RODict({
        "propID": 52001133,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":288,"adjMinPhysicalArmor":34,"adjMaxPhysicalArmor":34,"adjMinMagicArmor":34,"adjMaxMagicArmor":34,"adjMonsterDmgAnti":0.015})
    }),
    52001134: _tools.RODict({
        "propID": 52001134,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":384,"adjMinPhysicalArmor":43,"adjMaxPhysicalArmor":43,"adjMinMagicArmor":43,"adjMaxMagicArmor":43,"adjAntiFatal":40,"adjFinalDmgAnti":0.01})
    }),
    52001135: _tools.RODict({
        "propID": 52001135,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":432,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":50,"adjMaxMagicArmor":50,"adjAntiFatal":50,"adjFinalDmgAnti":0.015})
    }),
    52001136: _tools.RODict({
        "propID": 52001136,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":480,"adjMinPhysicalArmor":54,"adjMaxPhysicalArmor":54,"adjMinMagicArmor":54,"adjMaxMagicArmor":54,"adjAntiFatal":60,"adjFinalDmgAnti":0.02})
    }),
    52001137: _tools.RODict({
        "propID": 52001137,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":528,"adjMinPhysicalArmor":61,"adjMaxPhysicalArmor":61,"adjMinMagicArmor":61,"adjMaxMagicArmor":61,"adjAntiFatal":80,"adjFinalDmgAnti":0.03})
    }),
    52001138: _tools.RODict({
        "propID": 52001138,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":384,"adjMinPhysicalArmor":43,"adjMaxPhysicalArmor":43,"adjMinMagicArmor":43,"adjMaxMagicArmor":43,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.02})
    }),
    52001139: _tools.RODict({
        "propID": 52001139,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":432,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":50,"adjMaxMagicArmor":50,"adjRealDmgDef":3,"adjMonsterDmgAnti":0.025})
    }),
    52001140: _tools.RODict({
        "propID": 52001140,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":480,"adjMinPhysicalArmor":54,"adjMaxPhysicalArmor":54,"adjMinMagicArmor":54,"adjMaxMagicArmor":54,"adjRealDmgDef":4,"adjMonsterDmgAnti":0.03})
    }),
    52001141: _tools.RODict({
        "propID": 52001141,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":528,"adjMinPhysicalArmor":61,"adjMaxPhysicalArmor":61,"adjMinMagicArmor":61,"adjMaxMagicArmor":61,"adjRealDmgDef":6,"adjMonsterDmgAnti":0.04})
    }),
    52001142: _tools.RODict({
        "propID": 52001142,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":96,"adjMinPhysicalArmor":1,"adjMaxPhysicalArmor":1})
    }),
    52001143: _tools.RODict({
        "propID": 52001143,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":106,"adjMinPhysicalArmor":2,"adjMaxPhysicalArmor":2})
    }),
    52001144: _tools.RODict({
        "propID": 52001144,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":115,"adjMinPhysicalArmor":3,"adjMaxPhysicalArmor":3})
    }),
    52001145: _tools.RODict({
        "propID": 52001145,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":144,"adjMinPhysicalArmor":5,"adjMaxPhysicalArmor":5,"adjDebilityAnti":1})
    }),
    52001146: _tools.RODict({
        "propID": 52001146,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":163,"adjMinPhysicalArmor":6,"adjMaxPhysicalArmor":6,"adjDebilityAnti":2})
    }),
    52001147: _tools.RODict({
        "propID": 52001147,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":182,"adjMinPhysicalArmor":7,"adjMaxPhysicalArmor":7,"adjDebilityAnti":3})
    }),
    52001148: _tools.RODict({
        "propID": 52001148,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":202,"adjMinPhysicalArmor":8,"adjMaxPhysicalArmor":8,"adjDebilityAnti":4})
    }),
    52001149: _tools.RODict({
        "propID": 52001149,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":288,"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjDebilityAnti":5})
    }),
    52001150: _tools.RODict({
        "propID": 52001150,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":336,"adjMinPhysicalArmor":11,"adjMaxPhysicalArmor":11,"adjDebilityAnti":6})
    }),
    52001151: _tools.RODict({
        "propID": 52001151,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":384,"adjMinPhysicalArmor":12,"adjMaxPhysicalArmor":12,"adjDebilityAnti":7})
    }),
    52001152: _tools.RODict({
        "propID": 52001152,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":480,"adjMinPhysicalArmor":14,"adjMaxPhysicalArmor":14,"adjDebilityAnti":8})
    }),
    52001153: _tools.RODict({
        "propID": 52001153,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":576,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjDebilityAnti":9})
    }),
    52001154: _tools.RODict({
        "propID": 52001154,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":768,"adjMinPhysicalArmor":20,"adjMaxPhysicalArmor":20,"adjDebilityAnti":11})
    }),
    52001155: _tools.RODict({
        "propID": 52001155,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":864,"adjMinPhysicalArmor":23,"adjMaxPhysicalArmor":23,"adjDebilityAnti":12})
    }),
    52001156: _tools.RODict({
        "propID": 52001156,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":960,"adjMinPhysicalArmor":25,"adjMaxPhysicalArmor":25,"adjDebilityAnti":13})
    }),
    52001157: _tools.RODict({
        "propID": 52001157,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1056,"adjMinPhysicalArmor":28,"adjMaxPhysicalArmor":28,"adjDebilityAnti":15})
    }),
    52001158: _tools.RODict({
        "propID": 52001158,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":80,"adjMinMagicArmor":1,"adjMaxMagicArmor":1,"adjDodge":4})
    }),
    52001159: _tools.RODict({
        "propID": 52001159,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":88,"adjMinMagicArmor":2,"adjMaxMagicArmor":2,"adjDodge":5})
    }),
    52001160: _tools.RODict({
        "propID": 52001160,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":96,"adjMinMagicArmor":3,"adjMaxMagicArmor":3,"adjDodge":6})
    }),
    52001161: _tools.RODict({
        "propID": 52001161,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":120,"adjMinMagicArmor":5,"adjMaxMagicArmor":5,"adjDodge":10})
    }),
    52001162: _tools.RODict({
        "propID": 52001162,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":136,"adjMinMagicArmor":6,"adjMaxMagicArmor":6,"adjDodge":12})
    }),
    52001163: _tools.RODict({
        "propID": 52001163,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":152,"adjMinMagicArmor":7,"adjMaxMagicArmor":7,"adjDodge":14})
    }),
    52001164: _tools.RODict({
        "propID": 52001164,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":168,"adjMinMagicArmor":8,"adjMaxMagicArmor":8,"adjDodge":16})
    }),
    52001165: _tools.RODict({
        "propID": 52001165,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":240,"adjMinMagicArmor":10,"adjMaxMagicArmor":10,"adjDodge":22})
    }),
    52001166: _tools.RODict({
        "propID": 52001166,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":280,"adjMinMagicArmor":11,"adjMaxMagicArmor":11,"adjDodge":24})
    }),
    52001167: _tools.RODict({
        "propID": 52001167,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":320,"adjMinMagicArmor":12,"adjMaxMagicArmor":12,"adjDodge":26})
    }),
    52001168: _tools.RODict({
        "propID": 52001168,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":400,"adjMinMagicArmor":14,"adjMaxMagicArmor":14,"adjDodge":28})
    }),
    52001169: _tools.RODict({
        "propID": 52001169,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":480,"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjDodge":30})
    }),
    52001170: _tools.RODict({
        "propID": 52001170,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":640,"adjMinMagicArmor":20,"adjMaxMagicArmor":20,"adjDodge":36})
    }),
    52001171: _tools.RODict({
        "propID": 52001171,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":720,"adjMinMagicArmor":23,"adjMaxMagicArmor":23,"adjDodge":38})
    }),
    52001172: _tools.RODict({
        "propID": 52001172,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":800,"adjMinMagicArmor":25,"adjMaxMagicArmor":25,"adjDodge":40})
    }),
    52001173: _tools.RODict({
        "propID": 52001173,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":880,"adjMinMagicArmor":28,"adjMaxMagicArmor":28,"adjDodge":45})
    }),
    52001174: _tools.RODict({
        "propID": 52001174,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":20})
    }),
    52001175: _tools.RODict({
        "propID": 52001175,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":28})
    }),
    52001176: _tools.RODict({
        "propID": 52001176,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":36})
    }),
    52001177: _tools.RODict({
        "propID": 52001177,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":50})
    }),
    52001178: _tools.RODict({
        "propID": 52001178,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":60})
    }),
    52001179: _tools.RODict({
        "propID": 52001179,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":70})
    }),
    52001180: _tools.RODict({
        "propID": 52001180,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":80})
    }),
    52001181: _tools.RODict({
        "propID": 52001181,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":110,"adjDebilityEnh":5})
    }),
    52001182: _tools.RODict({
        "propID": 52001182,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":120,"adjDebilityEnh":6})
    }),
    52001183: _tools.RODict({
        "propID": 52001183,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":130,"adjDebilityEnh":7})
    }),
    52001184: _tools.RODict({
        "propID": 52001184,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":140,"adjDebilityEnh":8})
    }),
    52001185: _tools.RODict({
        "propID": 52001185,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":150,"adjDebilityEnh":9})
    }),
    52001186: _tools.RODict({
        "propID": 52001186,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":180,"adjDebilityEnh":11})
    }),
    52001187: _tools.RODict({
        "propID": 52001187,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":190,"adjDebilityEnh":12})
    }),
    52001188: _tools.RODict({
        "propID": 52001188,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":200,"adjDebilityEnh":13})
    }),
    52001189: _tools.RODict({
        "propID": 52001189,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":220,"adjDebilityEnh":15})
    }),
    52001190: _tools.RODict({
        "propID": 52001190,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":3,"adjMaxPhysicalArmor":3,"adjMinMagicArmor":3,"adjMaxMagicArmor":3,"adjFatal":18})
    }),
    52001191: _tools.RODict({
        "propID": 52001191,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":4,"adjMaxPhysicalArmor":4,"adjMinMagicArmor":4,"adjMaxMagicArmor":4,"adjFatal":22})
    }),
    52001192: _tools.RODict({
        "propID": 52001192,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":5,"adjMaxPhysicalArmor":5,"adjMinMagicArmor":5,"adjMaxMagicArmor":5,"adjFatal":25})
    }),
    52001193: _tools.RODict({
        "propID": 52001193,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":6,"adjMaxPhysicalArmor":6,"adjMinMagicArmor":6,"adjMaxMagicArmor":6,"adjFatal":28})
    }),
    52001194: _tools.RODict({
        "propID": 52001194,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjFatal":32})
    }),
    52001195: _tools.RODict({
        "propID": 52001195,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10,"adjFatal":39})
    }),
    52001196: _tools.RODict({
        "propID": 52001196,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":12,"adjMaxPhysicalArmor":12,"adjMinMagicArmor":12,"adjMaxMagicArmor":12,"adjFatal":44})
    }),
    52001197: _tools.RODict({
        "propID": 52001197,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":14,"adjMaxPhysicalArmor":14,"adjMinMagicArmor":14,"adjMaxMagicArmor":14,"adjFatal":50})
    }),
    52001198: _tools.RODict({
        "propID": 52001198,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjFatal":57})
    }),
    52001199: _tools.RODict({
        "propID": 52001199,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":19,"adjMaxPhysicalArmor":19,"adjMinMagicArmor":19,"adjMaxMagicArmor":19,"adjFatal":68})
    }),
    52001200: _tools.RODict({
        "propID": 52001200,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":21,"adjMaxPhysicalArmor":21,"adjMinMagicArmor":21,"adjMaxMagicArmor":21,"adjFatal":78})
    }),
    52001201: _tools.RODict({
        "propID": 52001201,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":23,"adjMaxPhysicalArmor":23,"adjMinMagicArmor":23,"adjMaxMagicArmor":23,"adjFatal":88})
    }),
    52001202: _tools.RODict({
        "propID": 52001202,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":26,"adjMaxPhysicalArmor":26,"adjMinMagicArmor":26,"adjMaxMagicArmor":26,"adjFatal":100})
    }),
    52001203: _tools.RODict({
        "propID": 52001203,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":3,"adjMaxPhysicalArmor":3,"adjMinMagicArmor":3,"adjMaxMagicArmor":3,"adjIgnoreArmor":0.0177777777777778})
    }),
    52001204: _tools.RODict({
        "propID": 52001204,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":4,"adjMaxPhysicalArmor":4,"adjMinMagicArmor":4,"adjMaxMagicArmor":4,"adjIgnoreArmor":0.0216666666666667})
    }),
    52001205: _tools.RODict({
        "propID": 52001205,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":5,"adjMaxPhysicalArmor":5,"adjMinMagicArmor":5,"adjMaxMagicArmor":5,"adjIgnoreArmor":0.025})
    }),
    52001206: _tools.RODict({
        "propID": 52001206,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":6,"adjMaxPhysicalArmor":6,"adjMinMagicArmor":6,"adjMaxMagicArmor":6,"adjIgnoreArmor":0.0283333333333333})
    }),
    52001207: _tools.RODict({
        "propID": 52001207,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjIgnoreArmor":0.0316666666666667})
    }),
    52001208: _tools.RODict({
        "propID": 52001208,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10,"adjIgnoreArmor":0.0394444444444444})
    }),
    52001209: _tools.RODict({
        "propID": 52001209,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":12,"adjMaxPhysicalArmor":12,"adjMinMagicArmor":12,"adjMaxMagicArmor":12,"adjIgnoreArmor":0.0444444444444444})
    }),
    52001210: _tools.RODict({
        "propID": 52001210,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":14,"adjMaxPhysicalArmor":14,"adjMinMagicArmor":14,"adjMaxMagicArmor":14,"adjIgnoreArmor":0.05})
    }),
    52001211: _tools.RODict({
        "propID": 52001211,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjIgnoreArmor":0.0566666666666667})
    }),
    52001212: _tools.RODict({
        "propID": 52001212,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":19,"adjMaxPhysicalArmor":19,"adjMinMagicArmor":19,"adjMaxMagicArmor":19,"adjIgnoreArmor":0.0683333333333333})
    }),
    52001213: _tools.RODict({
        "propID": 52001213,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":21,"adjMaxPhysicalArmor":21,"adjMinMagicArmor":21,"adjMaxMagicArmor":21,"adjIgnoreArmor":0.0777777777777778})
    }),
    52001214: _tools.RODict({
        "propID": 52001214,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":23,"adjMaxPhysicalArmor":23,"adjMinMagicArmor":23,"adjMaxMagicArmor":23,"adjIgnoreArmor":0.0883333333333333})
    }),
    52001215: _tools.RODict({
        "propID": 52001215,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":26,"adjMaxPhysicalArmor":26,"adjMinMagicArmor":26,"adjMaxMagicArmor":26,"adjIgnoreArmor":0.1})
    }),
    52001216: _tools.RODict({
        "propID": 52001216,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9})
    }),
    52001217: _tools.RODict({
        "propID": 52001217,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10})
    }),
    52001218: _tools.RODict({
        "propID": 52001218,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":12,"adjMaxPhysicalArmor":12,"adjMinMagicArmor":12,"adjMaxMagicArmor":12})
    }),
    52001219: _tools.RODict({
        "propID": 52001219,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":14,"adjMaxPhysicalArmor":14,"adjMinMagicArmor":14,"adjMaxMagicArmor":14})
    }),
    52001220: _tools.RODict({
        "propID": 52001220,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16})
    }),
    52001221: _tools.RODict({
        "propID": 52001221,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":19,"adjMaxPhysicalArmor":19,"adjMinMagicArmor":19,"adjMaxMagicArmor":19})
    }),
    52001222: _tools.RODict({
        "propID": 52001222,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":21,"adjMaxPhysicalArmor":21,"adjMinMagicArmor":21,"adjMaxMagicArmor":21})
    }),
    52001223: _tools.RODict({
        "propID": 52001223,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":23,"adjMaxPhysicalArmor":23,"adjMinMagicArmor":23,"adjMaxMagicArmor":23})
    }),
    52001224: _tools.RODict({
        "propID": 52001224,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":26,"adjMaxPhysicalArmor":26,"adjMinMagicArmor":26,"adjMaxMagicArmor":26})
    }),
    52001225: _tools.RODict({
        "propID": 52001225,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":1,"adjMaxPhysicalAtk":4})
    }),
    52001226: _tools.RODict({
        "propID": 52001226,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":2,"adjMaxPhysicalAtk":6})
    }),
    52001227: _tools.RODict({
        "propID": 52001227,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":3,"adjMaxPhysicalAtk":10})
    }),
    52001228: _tools.RODict({
        "propID": 52001228,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":4,"adjMaxPhysicalAtk":12})
    }),
    52001229: _tools.RODict({
        "propID": 52001229,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":5,"adjMaxPhysicalAtk":22})
    }),
    52001230: _tools.RODict({
        "propID": 52001230,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":6,"adjMaxPhysicalAtk":24})
    }),
    52001231: _tools.RODict({
        "propID": 52001231,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":7,"adjMaxPhysicalAtk":28})
    }),
    52001232: _tools.RODict({
        "propID": 52001232,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":8,"adjMaxPhysicalAtk":30})
    }),
    52001233: _tools.RODict({
        "propID": 52001233,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":9,"adjMaxPhysicalAtk":36})
    }),
    52001234: _tools.RODict({
        "propID": 52001234,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":12,"adjMaxPhysicalAtk":48})
    }),
    52001235: _tools.RODict({
        "propID": 52001235,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":13,"adjMaxPhysicalAtk":54})
    }),
    52001236: _tools.RODict({
        "propID": 52001236,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":14,"adjMaxPhysicalAtk":60})
    }),
    52001237: _tools.RODict({
        "propID": 52001237,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":16,"adjMaxPhysicalAtk":66})
    }),
    52001238: _tools.RODict({
        "propID": 52001238,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":1,"adjMaxMagicAtk":4})
    }),
    52001239: _tools.RODict({
        "propID": 52001239,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":2,"adjMaxMagicAtk":6})
    }),
    52001240: _tools.RODict({
        "propID": 52001240,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":3,"adjMaxMagicAtk":10})
    }),
    52001241: _tools.RODict({
        "propID": 52001241,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":4,"adjMaxMagicAtk":12})
    }),
    52001242: _tools.RODict({
        "propID": 52001242,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":5,"adjMaxMagicAtk":22})
    }),
    52001243: _tools.RODict({
        "propID": 52001243,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":6,"adjMaxMagicAtk":24})
    }),
    52001244: _tools.RODict({
        "propID": 52001244,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":7,"adjMaxMagicAtk":28})
    }),
    52001245: _tools.RODict({
        "propID": 52001245,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":8,"adjMaxMagicAtk":30})
    }),
    52001246: _tools.RODict({
        "propID": 52001246,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":9,"adjMaxMagicAtk":36})
    }),
    52001247: _tools.RODict({
        "propID": 52001247,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":12,"adjMaxMagicAtk":48})
    }),
    52001248: _tools.RODict({
        "propID": 52001248,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":13,"adjMaxMagicAtk":54})
    }),
    52001249: _tools.RODict({
        "propID": 52001249,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":14,"adjMaxMagicAtk":60})
    }),
    52001250: _tools.RODict({
        "propID": 52001250,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":16,"adjMaxMagicAtk":66})
    }),
    52001251: _tools.RODict({
        "propID": 52001251,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":162})
    }),
    52001252: _tools.RODict({
        "propID": 52001252,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":180})
    }),
    52001253: _tools.RODict({
        "propID": 52001253,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":210})
    }),
    52001254: _tools.RODict({
        "propID": 52001254,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":228})
    }),
    52001255: _tools.RODict({
        "propID": 52001255,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":270})
    }),
    52001256: _tools.RODict({
        "propID": 52001256,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":360})
    }),
    52001257: _tools.RODict({
        "propID": 52001257,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":402})
    }),
    52001258: _tools.RODict({
        "propID": 52001258,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":444})
    }),
    52001259: _tools.RODict({
        "propID": 52001259,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":492})
    }),
    52002001: _tools.RODict({
        "propID": 52002001,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":1,"adjMaxPhysicalAtk":1,"adjMinMagicAtk":1,"adjMaxMagicAtk":1})
    }),
    52002002: _tools.RODict({
        "propID": 52002002,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":3,"adjMaxPhysicalAtk":3,"adjMinMagicAtk":3,"adjMaxMagicAtk":3,"adjHit":1})
    }),
    52002003: _tools.RODict({
        "propID": 52002003,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":5,"adjMaxPhysicalAtk":6,"adjMinMagicAtk":5,"adjMaxMagicAtk":6,"adjHit":2})
    }),
    52002004: _tools.RODict({
        "propID": 52002004,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":7,"adjMaxPhysicalAtk":11,"adjMinMagicAtk":7,"adjMaxMagicAtk":11,"adjHit":4})
    }),
    52002005: _tools.RODict({
        "propID": 52002005,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":10,"adjMaxPhysicalAtk":17,"adjMinMagicAtk":10,"adjMaxMagicAtk":17,"adjHit":6})
    }),
    52002006: _tools.RODict({
        "propID": 52002006,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":14,"adjMaxPhysicalAtk":25,"adjMinMagicAtk":14,"adjMaxMagicAtk":25,"adjHit":9})
    }),
    52002007: _tools.RODict({
        "propID": 52002007,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":19,"adjMaxPhysicalAtk":34,"adjMinMagicAtk":19,"adjMaxMagicAtk":34,"adjHit":12})
    }),
    52002008: _tools.RODict({
        "propID": 52002008,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":44,"adjMinMagicAtk":25,"adjMaxMagicAtk":44,"adjHit":15})
    }),
    52002009: _tools.RODict({
        "propID": 52002009,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":33,"adjMaxPhysicalAtk":55,"adjMinMagicAtk":33,"adjMaxMagicAtk":55,"adjHit":18})
    }),
    52002010: _tools.RODict({
        "propID": 52002010,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":42,"adjMaxPhysicalAtk":70,"adjMinMagicAtk":42,"adjMaxMagicAtk":70,"adjHit":21,"adjFinalDmg":0.01})
    }),
    52002011: _tools.RODict({
        "propID": 52002011,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":53,"adjMaxPhysicalAtk":90,"adjMinMagicAtk":53,"adjMaxMagicAtk":90,"adjHit":24,"adjFinalDmg":0.03})
    }),
    52002012: _tools.RODict({
        "propID": 52002012,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":67,"adjMaxPhysicalAtk":115,"adjMinMagicAtk":67,"adjMaxMagicAtk":115,"adjHit":27,"adjFinalDmg":0.05})
    }),
    52002013: _tools.RODict({
        "propID": 52002013,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":82,"adjMaxPhysicalAtk":145,"adjMinMagicAtk":82,"adjMaxMagicAtk":145,"adjHit":30,"adjFinalDmg":0.08})
    }),
    52002014: _tools.RODict({
        "propID": 52002014,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":13})
    }),
    52002015: _tools.RODict({
        "propID": 52002015,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":39})
    }),
    52002016: _tools.RODict({
        "propID": 52002016,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":78,"adjRealDmg":1})
    }),
    52002017: _tools.RODict({
        "propID": 52002017,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":124,"adjRealDmg":2})
    }),
    52002018: _tools.RODict({
        "propID": 52002018,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":176,"adjRealDmg":3})
    }),
    52002019: _tools.RODict({
        "propID": 52002019,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":234,"adjRealDmg":5})
    }),
    52002020: _tools.RODict({
        "propID": 52002020,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":312,"adjRealDmg":7})
    }),
    52002021: _tools.RODict({
        "propID": 52002021,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":410,"adjRealDmg":9})
    }),
    52002022: _tools.RODict({
        "propID": 52002022,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":527,"adjRealDmg":12})
    }),
    52002023: _tools.RODict({
        "propID": 52002023,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":683,"adjRealDmg":15,"adjFinalDmgAnti":0.01})
    }),
    52002024: _tools.RODict({
        "propID": 52002024,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":878,"adjRealDmg":19,"adjFinalDmgAnti":0.03})
    }),
    52002025: _tools.RODict({
        "propID": 52002025,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1112,"adjRealDmg":24,"adjFinalDmgAnti":0.05})
    }),
    52002026: _tools.RODict({
        "propID": 52002026,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1385,"adjRealDmg":30,"adjFinalDmgAnti":0.08})
    }),
    52002027: _tools.RODict({
        "propID": 52002027,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":1,"adjMaxPhysicalArmor":1})
    }),
    52002028: _tools.RODict({
        "propID": 52002028,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":2,"adjMaxPhysicalArmor":2,"adjRealDmgDef":1})
    }),
    52002029: _tools.RODict({
        "propID": 52002029,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":4,"adjMaxPhysicalArmor":4,"adjRealDmgDef":2})
    }),
    52002030: _tools.RODict({
        "propID": 52002030,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":6,"adjMaxPhysicalArmor":6,"adjRealDmgDef":4})
    }),
    52002031: _tools.RODict({
        "propID": 52002031,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjRealDmgDef":6})
    }),
    52002032: _tools.RODict({
        "propID": 52002032,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":12,"adjMaxPhysicalArmor":12,"adjRealDmgDef":9})
    }),
    52002033: _tools.RODict({
        "propID": 52002033,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjRealDmgDef":12})
    }),
    52002034: _tools.RODict({
        "propID": 52002034,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":20,"adjMaxPhysicalArmor":20,"adjRealDmgDef":15})
    }),
    52002035: _tools.RODict({
        "propID": 52002035,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":25,"adjMaxPhysicalArmor":25,"adjRealDmgDef":18})
    }),
    52002036: _tools.RODict({
        "propID": 52002036,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":31,"adjMaxPhysicalArmor":31,"adjRealDmgDef":21,"adjDebilityAnti":7})
    }),
    52002037: _tools.RODict({
        "propID": 52002037,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":39,"adjMaxPhysicalArmor":39,"adjRealDmgDef":24,"adjDebilityAnti":14})
    }),
    52002038: _tools.RODict({
        "propID": 52002038,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":49,"adjMaxPhysicalArmor":49,"adjRealDmgDef":27,"adjDebilityAnti":24})
    }),
    52002039: _tools.RODict({
        "propID": 52002039,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":61,"adjMaxPhysicalArmor":61,"adjRealDmgDef":30,"adjDebilityAnti":44})
    }),
    52002040: _tools.RODict({
        "propID": 52002040,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":1,"adjMaxMagicArmor":1})
    }),
    52002041: _tools.RODict({
        "propID": 52002041,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":2,"adjMaxMagicArmor":2,"adjDodge":1})
    }),
    52002042: _tools.RODict({
        "propID": 52002042,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":4,"adjMaxMagicArmor":4,"adjDodge":2})
    }),
    52002043: _tools.RODict({
        "propID": 52002043,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":6,"adjMaxMagicArmor":6,"adjDodge":4})
    }),
    52002044: _tools.RODict({
        "propID": 52002044,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjDodge":6})
    }),
    52002045: _tools.RODict({
        "propID": 52002045,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":12,"adjMaxMagicArmor":12,"adjDodge":9})
    }),
    52002046: _tools.RODict({
        "propID": 52002046,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjDodge":12})
    }),
    52002047: _tools.RODict({
        "propID": 52002047,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":20,"adjMaxMagicArmor":20,"adjDodge":16})
    }),
    52002048: _tools.RODict({
        "propID": 52002048,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":25,"adjMaxMagicArmor":25,"adjDodge":20})
    }),
    52002049: _tools.RODict({
        "propID": 52002049,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":31,"adjMaxMagicArmor":31,"adjDodge":25,"adjDebilityEnh":7})
    }),
    52002050: _tools.RODict({
        "propID": 52002050,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":39,"adjMaxMagicArmor":39,"adjDodge":31,"adjDebilityEnh":7})
    }),
    52002051: _tools.RODict({
        "propID": 52002051,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":49,"adjMaxMagicArmor":49,"adjDodge":38,"adjDebilityEnh":10})
    }),
    52002052: _tools.RODict({
        "propID": 52002052,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":61,"adjMaxMagicArmor":61,"adjDodge":45,"adjDebilityEnh":20})
    }),
    51000001: _tools.RODict({
        "propID": 51000001,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":272,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":37,"adjMinMagicAtk":20,"adjMaxMagicAtk":37,"adjHit":1,"adjDodge":1})
    }),
    51000002: _tools.RODict({
        "propID": 51000002,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":285,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":38,"adjMinMagicAtk":21,"adjMaxMagicAtk":38,"adjHit":2,"adjDodge":2})
    }),
    51000003: _tools.RODict({
        "propID": 51000003,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":299,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":39,"adjMinMagicAtk":21,"adjMaxMagicAtk":39,"adjHit":3,"adjDodge":3})
    }),
    51000004: _tools.RODict({
        "propID": 51000004,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":312,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":40,"adjMinMagicAtk":22,"adjMaxMagicAtk":40,"adjHit":4,"adjDodge":4})
    }),
    51000005: _tools.RODict({
        "propID": 51000005,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":326,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":41,"adjMinMagicAtk":23,"adjMaxMagicAtk":41,"adjHit":5,"adjDodge":5})
    }),
    51000006: _tools.RODict({
        "propID": 51000006,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":339,"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":43,"adjMinMagicAtk":24,"adjMaxMagicAtk":43,"adjHit":6,"adjDodge":6})
    }),
    51000007: _tools.RODict({
        "propID": 51000007,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":353,"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":44,"adjMinMagicAtk":24,"adjMaxMagicAtk":44,"adjHit":7,"adjDodge":7})
    }),
    51000008: _tools.RODict({
        "propID": 51000008,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":367,"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":45,"adjMinMagicAtk":25,"adjMaxMagicAtk":45,"adjHit":8,"adjDodge":8})
    }),
    51000009: _tools.RODict({
        "propID": 51000009,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":380,"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":46,"adjMinMagicAtk":25,"adjMaxMagicAtk":46,"adjHit":9,"adjDodge":9})
    }),
    51000010: _tools.RODict({
        "propID": 51000010,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":394,"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":47,"adjMinMagicAtk":26,"adjMaxMagicAtk":47,"adjHit":10,"adjDodge":10})
    }),
    51000011: _tools.RODict({
        "propID": 51000011,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":295,"adjMinPhysicalAtk":10,"adjMaxPhysicalAtk":18,"adjMinMagicAtk":10,"adjMaxMagicAtk":18,"adjMinPhysicalArmor":1,"adjMaxPhysicalArmor":1,"adjMinMagicArmor":1,"adjMaxMagicArmor":1,"adjHit":4})
    }),
    51000012: _tools.RODict({
        "propID": 51000012,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":304,"adjMinPhysicalAtk":10,"adjMaxPhysicalAtk":19,"adjMinMagicAtk":10,"adjMaxMagicAtk":19,"adjMinPhysicalArmor":2,"adjMaxPhysicalArmor":2,"adjMinMagicArmor":2,"adjMaxMagicArmor":2,"adjHit":4})
    }),
    51000013: _tools.RODict({
        "propID": 51000013,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":319,"adjMinPhysicalAtk":11,"adjMaxPhysicalAtk":20,"adjMinMagicAtk":11,"adjMaxMagicAtk":20,"adjMinPhysicalArmor":3,"adjMaxPhysicalArmor":3,"adjMinMagicArmor":3,"adjMaxMagicArmor":3,"adjHit":5})
    }),
    51000014: _tools.RODict({
        "propID": 51000014,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":328,"adjMinPhysicalAtk":11,"adjMaxPhysicalAtk":20,"adjMinMagicAtk":11,"adjMaxMagicAtk":20,"adjMinPhysicalArmor":4,"adjMaxPhysicalArmor":4,"adjMinMagicArmor":4,"adjMaxMagicArmor":4,"adjHit":5})
    }),
    51000015: _tools.RODict({
        "propID": 51000015,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":396,"adjMinPhysicalAtk":12,"adjMaxPhysicalAtk":21,"adjMinMagicAtk":12,"adjMaxMagicAtk":21,"adjMinPhysicalArmor":5,"adjMaxPhysicalArmor":5,"adjMinMagicArmor":5,"adjMaxMagicArmor":5,"adjHit":5})
    }),
    51000016: _tools.RODict({
        "propID": 51000016,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":407,"adjMinPhysicalAtk":13,"adjMaxPhysicalAtk":23,"adjMinMagicAtk":13,"adjMaxMagicAtk":23,"adjMinPhysicalArmor":6,"adjMaxPhysicalArmor":6,"adjMinMagicArmor":6,"adjMaxMagicArmor":6,"adjHit":5})
    }),
    51000017: _tools.RODict({
        "propID": 51000017,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":424,"adjMinPhysicalAtk":14,"adjMaxPhysicalAtk":25,"adjMinMagicAtk":14,"adjMaxMagicAtk":25,"adjMinPhysicalArmor":8,"adjMaxPhysicalArmor":8,"adjMinMagicArmor":8,"adjMaxMagicArmor":8,"adjHit":5})
    }),
    51000018: _tools.RODict({
        "propID": 51000018,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":436,"adjMinPhysicalAtk":14,"adjMaxPhysicalAtk":25,"adjMinMagicAtk":14,"adjMaxMagicAtk":25,"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10,"adjHit":6})
    }),
    51000019: _tools.RODict({
        "propID": 51000019,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":453,"adjMinPhysicalAtk":14,"adjMaxPhysicalAtk":26,"adjMinMagicAtk":14,"adjMaxMagicAtk":26,"adjMinPhysicalArmor":14,"adjMaxPhysicalArmor":14,"adjMinMagicArmor":14,"adjMaxMagicArmor":14,"adjHit":6})
    }),
    51000020: _tools.RODict({
        "propID": 51000020,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":501,"adjMinPhysicalAtk":14,"adjMaxPhysicalAtk":26,"adjMinMagicAtk":14,"adjMaxMagicAtk":26,"adjMinPhysicalArmor":15,"adjMaxPhysicalArmor":15,"adjMinMagicArmor":15,"adjMaxMagicArmor":15,"adjHit":6})
    }),
    51000021: _tools.RODict({
        "propID": 51000021,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":526,"adjMinPhysicalAtk":18,"adjMaxPhysicalAtk":33,"adjMinMagicAtk":18,"adjMaxMagicAtk":33,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjHit":6,"adjDebilityAnti":1})
    }),
    51000022: _tools.RODict({
        "propID": 51000022,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":539,"adjMinPhysicalAtk":18,"adjMaxPhysicalAtk":33,"adjMinMagicAtk":18,"adjMaxMagicAtk":33,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjHit":10,"adjDebilityAnti":1})
    }),
    51000023: _tools.RODict({
        "propID": 51000023,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":584,"adjMinPhysicalAtk":19,"adjMaxPhysicalAtk":34,"adjMinMagicAtk":19,"adjMaxMagicAtk":34,"adjMinPhysicalArmor":17,"adjMaxPhysicalArmor":17,"adjMinMagicArmor":17,"adjMaxMagicArmor":17,"adjHit":10,"adjDebilityAnti":1})
    }),
    51000024: _tools.RODict({
        "propID": 51000024,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":624,"adjMinPhysicalAtk":19,"adjMaxPhysicalAtk":34,"adjMinMagicAtk":19,"adjMaxMagicAtk":34,"adjMinPhysicalArmor":18,"adjMaxPhysicalArmor":18,"adjMinMagicArmor":18,"adjMaxMagicArmor":18,"adjHit":10,"adjDebilityAnti":1})
    }),
    51000025: _tools.RODict({
        "propID": 51000025,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":740,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":39,"adjMinMagicAtk":21,"adjMaxMagicAtk":39,"adjMinPhysicalArmor":20,"adjMaxPhysicalArmor":20,"adjMinMagicArmor":20,"adjMaxMagicArmor":20,"adjHit":10,"adjDebilityAnti":2})
    }),
    51000026: _tools.RODict({
        "propID": 51000026,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":756,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":39,"adjMinMagicAtk":21,"adjMaxMagicAtk":39,"adjMinPhysicalArmor":21,"adjMaxPhysicalArmor":21,"adjMinMagicArmor":21,"adjMaxMagicArmor":21,"adjHit":12,"adjDebilityAnti":2})
    }),
    51000027: _tools.RODict({
        "propID": 51000027,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":780,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":40,"adjMinMagicAtk":22,"adjMaxMagicAtk":40,"adjMinPhysicalArmor":21,"adjMaxPhysicalArmor":21,"adjMinMagicArmor":21,"adjMaxMagicArmor":21,"adjHit":12,"adjDebilityAnti":2})
    }),
    51000028: _tools.RODict({
        "propID": 51000028,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":826,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":40,"adjMinMagicAtk":22,"adjMaxMagicAtk":40,"adjMinPhysicalArmor":22,"adjMaxPhysicalArmor":22,"adjMinMagicArmor":22,"adjMaxMagicArmor":22,"adjHit":12,"adjDebilityAnti":2})
    }),
    51000029: _tools.RODict({
        "propID": 51000029,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":946,"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":43,"adjMinMagicAtk":24,"adjMaxMagicAtk":43,"adjMinPhysicalArmor":23,"adjMaxPhysicalArmor":23,"adjMinMagicArmor":23,"adjMaxMagicArmor":23,"adjHit":12,"adjDebilityAnti":3})
    }),
    51000030: _tools.RODict({
        "propID": 51000030,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4111,"adjMinPhysicalAtk":247,"adjMaxPhysicalAtk":247,"adjMinMagicAtk":247,"adjMaxMagicAtk":247,"adjMinPhysicalArmor":62,"adjMaxPhysicalArmor":62,"adjMinMagicArmor":62,"adjMaxMagicArmor":62,"adjHit":14,"adjDodge":14,"adjDebilityAnti":3})
    }),
    51000031: _tools.RODict({
        "propID": 51000031,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4213,"adjMinPhysicalAtk":249,"adjMaxPhysicalAtk":249,"adjMinMagicAtk":249,"adjMaxMagicAtk":249,"adjMinPhysicalArmor":62,"adjMaxPhysicalArmor":62,"adjMinMagicArmor":62,"adjMaxMagicArmor":62,"adjHit":14,"adjDodge":14,"adjRealDmg":1,"adjDebilityAnti":3})
    }),
    51000032: _tools.RODict({
        "propID": 51000032,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4317,"adjMinPhysicalAtk":251,"adjMaxPhysicalAtk":251,"adjMinMagicAtk":251,"adjMaxMagicAtk":251,"adjMinPhysicalArmor":62,"adjMaxPhysicalArmor":62,"adjMinMagicArmor":62,"adjMaxMagicArmor":62,"adjHit":14,"adjDodge":14,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":3})
    }),
    51000033: _tools.RODict({
        "propID": 51000033,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4421,"adjMinPhysicalAtk":253,"adjMaxPhysicalAtk":253,"adjMinMagicAtk":253,"adjMaxMagicAtk":253,"adjMinPhysicalArmor":62,"adjMaxPhysicalArmor":62,"adjMinMagicArmor":62,"adjMaxMagicArmor":62,"adjHit":14,"adjDodge":14,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":4})
    }),
    51000034: _tools.RODict({
        "propID": 51000034,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4526,"adjMinPhysicalAtk":254,"adjMaxPhysicalAtk":254,"adjMinMagicAtk":254,"adjMaxMagicAtk":254,"adjMinPhysicalArmor":63,"adjMaxPhysicalArmor":63,"adjMinMagicArmor":63,"adjMaxMagicArmor":63,"adjHit":14,"adjDodge":14,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":4})
    }),
    51000035: _tools.RODict({
        "propID": 51000035,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4632,"adjMinPhysicalAtk":257,"adjMaxPhysicalAtk":257,"adjMinMagicAtk":257,"adjMaxMagicAtk":257,"adjMinPhysicalArmor":63,"adjMaxPhysicalArmor":63,"adjMinMagicArmor":63,"adjMaxMagicArmor":63,"adjHit":14,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":1,"adjDebilityAnti":4})
    }),
    51000036: _tools.RODict({
        "propID": 51000036,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4738,"adjMinPhysicalAtk":259,"adjMaxPhysicalAtk":259,"adjMinMagicAtk":259,"adjMaxMagicAtk":259,"adjMinPhysicalArmor":63,"adjMaxPhysicalArmor":63,"adjMinMagicArmor":63,"adjMaxMagicArmor":63,"adjHit":14,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":2,"adjDebilityAnti":4})
    }),
    51000037: _tools.RODict({
        "propID": 51000037,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4846,"adjMinPhysicalAtk":261,"adjMaxPhysicalAtk":261,"adjMinMagicAtk":261,"adjMaxMagicAtk":261,"adjMinPhysicalArmor":64,"adjMaxPhysicalArmor":64,"adjMinMagicArmor":64,"adjMaxMagicArmor":64,"adjHit":14,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":2,"adjDebilityAnti":4})
    }),
    51000038: _tools.RODict({
        "propID": 51000038,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4954,"adjMinPhysicalAtk":263,"adjMaxPhysicalAtk":263,"adjMinMagicAtk":263,"adjMaxMagicAtk":263,"adjMinPhysicalArmor":64,"adjMaxPhysicalArmor":64,"adjMinMagicArmor":64,"adjMaxMagicArmor":64,"adjHit":14,"adjDodge":14,"adjRealDmg":3,"adjRealDmgDef":2,"adjDebilityAnti":5})
    }),
    51000039: _tools.RODict({
        "propID": 51000039,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5063,"adjMinPhysicalAtk":265,"adjMaxPhysicalAtk":265,"adjMinMagicAtk":265,"adjMaxMagicAtk":265,"adjMinPhysicalArmor":64,"adjMaxPhysicalArmor":64,"adjMinMagicArmor":64,"adjMaxMagicArmor":64,"adjHit":14,"adjDodge":14,"adjRealDmg":3,"adjRealDmgDef":3,"adjDebilityEnh":5,"adjDebilityAnti":5})
    }),
    51000040: _tools.RODict({
        "propID": 51000040,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5173,"adjMinPhysicalAtk":267,"adjMaxPhysicalAtk":267,"adjMinMagicAtk":267,"adjMaxMagicAtk":267,"adjMinPhysicalArmor":65,"adjMaxPhysicalArmor":65,"adjMinMagicArmor":65,"adjMaxMagicArmor":65,"adjHit":14,"adjDodge":14,"adjRealDmg":3,"adjRealDmgDef":3,"adjDebilityEnh":5,"adjDebilityAnti":5})
    }),
    51000041: _tools.RODict({
        "propID": 51000041,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2117,"adjMinPhysicalAtk":38,"adjMaxPhysicalAtk":69,"adjMinMagicAtk":38,"adjMaxMagicAtk":69,"adjMinPhysicalArmor":38,"adjMaxPhysicalArmor":38,"adjMinMagicArmor":38,"adjMaxMagicArmor":38,"adjHit":23,"adjRealDmg":3,"adjRealDmgDef":3,"adjDebilityEnh":5,"adjDebilityAnti":5})
    }),
    51000042: _tools.RODict({
        "propID": 51000042,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2151,"adjMinPhysicalAtk":40,"adjMaxPhysicalAtk":72,"adjMinMagicAtk":40,"adjMaxMagicAtk":72,"adjMinPhysicalArmor":38,"adjMaxPhysicalArmor":38,"adjMinMagicArmor":38,"adjMaxMagicArmor":38,"adjHit":23,"adjRealDmg":4,"adjRealDmgDef":3,"adjDebilityEnh":5,"adjDebilityAnti":5})
    }),
    51000043: _tools.RODict({
        "propID": 51000043,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2195,"adjMinPhysicalAtk":42,"adjMaxPhysicalAtk":76,"adjMinMagicAtk":42,"adjMaxMagicAtk":76,"adjMinPhysicalArmor":38,"adjMaxPhysicalArmor":38,"adjMinMagicArmor":38,"adjMaxMagicArmor":38,"adjHit":25,"adjRealDmg":4,"adjRealDmgDef":4,"adjDebilityEnh":5,"adjDebilityAnti":6})
    }),
    51000044: _tools.RODict({
        "propID": 51000044,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2269,"adjMinPhysicalAtk":43,"adjMaxPhysicalAtk":78,"adjMinMagicAtk":43,"adjMaxMagicAtk":78,"adjMinPhysicalArmor":39,"adjMaxPhysicalArmor":39,"adjMinMagicArmor":39,"adjMaxMagicArmor":39,"adjHit":26,"adjRealDmg":4,"adjRealDmgDef":4,"adjDebilityEnh":6,"adjDebilityAnti":6})
    }),
    51000045: _tools.RODict({
        "propID": 51000045,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2353,"adjMinPhysicalAtk":45,"adjMaxPhysicalAtk":81,"adjMinMagicAtk":45,"adjMaxMagicAtk":81,"adjMinPhysicalArmor":39,"adjMaxPhysicalArmor":39,"adjMinMagicArmor":39,"adjMaxMagicArmor":39,"adjHit":26,"adjRealDmg":4,"adjRealDmgDef":4,"adjDebilityEnh":6,"adjDebilityAnti":6})
    }),
    51000046: _tools.RODict({
        "propID": 51000046,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2619,"adjMinPhysicalAtk":45,"adjMaxPhysicalAtk":81,"adjMinMagicAtk":45,"adjMaxMagicAtk":81,"adjMinPhysicalArmor":42,"adjMaxPhysicalArmor":42,"adjMinMagicArmor":42,"adjMaxMagicArmor":42,"adjHit":26,"adjRealDmg":4,"adjRealDmgDef":4,"adjDebilityEnh":6,"adjDebilityAnti":6})
    }),
    51000047: _tools.RODict({
        "propID": 51000047,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2668,"adjMinPhysicalAtk":48,"adjMaxPhysicalAtk":87,"adjMinMagicAtk":48,"adjMaxMagicAtk":87,"adjMinPhysicalArmor":42,"adjMaxPhysicalArmor":42,"adjMinMagicArmor":42,"adjMaxMagicArmor":42,"adjHit":26,"adjRealDmg":5,"adjRealDmgDef":4,"adjDebilityEnh":6,"adjDebilityAnti":6})
    }),
    51000048: _tools.RODict({
        "propID": 51000048,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2708,"adjMinPhysicalAtk":48,"adjMaxPhysicalAtk":88,"adjMinMagicAtk":48,"adjMaxMagicAtk":88,"adjMinPhysicalArmor":43,"adjMaxPhysicalArmor":43,"adjMinMagicArmor":43,"adjMaxMagicArmor":43,"adjHit":30,"adjRealDmg":5,"adjRealDmgDef":5,"adjDebilityEnh":6,"adjDebilityAnti":7})
    }),
    51000049: _tools.RODict({
        "propID": 51000049,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2894,"adjMinPhysicalAtk":50,"adjMaxPhysicalAtk":91,"adjMinMagicAtk":50,"adjMaxMagicAtk":91,"adjMinPhysicalArmor":44,"adjMaxPhysicalArmor":44,"adjMinMagicArmor":44,"adjMaxMagicArmor":44,"adjHit":30,"adjRealDmg":5,"adjRealDmgDef":5,"adjDebilityEnh":7,"adjDebilityAnti":7})
    }),
    51000050: _tools.RODict({
        "propID": 51000050,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3010,"adjMinPhysicalAtk":53,"adjMaxPhysicalAtk":96,"adjMinMagicAtk":53,"adjMaxMagicAtk":96,"adjMinPhysicalArmor":45,"adjMaxPhysicalArmor":45,"adjMinMagicArmor":45,"adjMaxMagicArmor":45,"adjHit":32,"adjRealDmg":5,"adjRealDmgDef":5,"adjDebilityEnh":7,"adjDebilityAnti":7})
    }),
    51000051: _tools.RODict({
        "propID": 51000051,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3278,"adjMinPhysicalAtk":53,"adjMaxPhysicalAtk":97,"adjMinMagicAtk":53,"adjMaxMagicAtk":97,"adjMinPhysicalArmor":49,"adjMaxPhysicalArmor":49,"adjMinMagicArmor":49,"adjMaxMagicArmor":49,"adjHit":32,"adjRealDmg":5,"adjRealDmgDef":5,"adjDebilityEnh":7,"adjDebilityAnti":7})
    }),
    51000052: _tools.RODict({
        "propID": 51000052,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3411,"adjMinPhysicalAtk":55,"adjMaxPhysicalAtk":100,"adjMinMagicAtk":55,"adjMaxMagicAtk":100,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":50,"adjMaxMagicArmor":50,"adjHit":32,"adjRealDmg":6,"adjRealDmgDef":5,"adjDebilityEnh":7,"adjDebilityAnti":7})
    }),
    51000053: _tools.RODict({
        "propID": 51000053,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3469,"adjMinPhysicalAtk":57,"adjMaxPhysicalAtk":103,"adjMinMagicAtk":57,"adjMaxMagicAtk":103,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":50,"adjMaxMagicArmor":50,"adjHit":34,"adjRealDmg":6,"adjRealDmgDef":6,"adjDebilityEnh":7,"adjDebilityAnti":8})
    }),
    51000054: _tools.RODict({
        "propID": 51000054,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3572,"adjMinPhysicalAtk":59,"adjMaxPhysicalAtk":108,"adjMinMagicAtk":59,"adjMaxMagicAtk":108,"adjMinPhysicalArmor":51,"adjMaxPhysicalArmor":51,"adjMinMagicArmor":51,"adjMaxMagicArmor":51,"adjHit":34,"adjRealDmg":6,"adjRealDmgDef":6,"adjDebilityEnh":8,"adjDebilityAnti":8})
    }),
    51000055: _tools.RODict({
        "propID": 51000055,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3689,"adjMinPhysicalAtk":62,"adjMaxPhysicalAtk":112,"adjMinMagicAtk":62,"adjMaxMagicAtk":112,"adjMinPhysicalArmor":52,"adjMaxPhysicalArmor":52,"adjMinMagicArmor":52,"adjMaxMagicArmor":52,"adjHit":37,"adjRealDmg":6,"adjRealDmgDef":6,"adjDebilityEnh":8,"adjDebilityAnti":8})
    }),
    51000056: _tools.RODict({
        "propID": 51000056,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4013,"adjMinPhysicalAtk":62,"adjMaxPhysicalAtk":112,"adjMinMagicAtk":62,"adjMaxMagicAtk":112,"adjMinPhysicalArmor":56,"adjMaxPhysicalArmor":56,"adjMinMagicArmor":56,"adjMaxMagicArmor":56,"adjHit":37,"adjRealDmg":6,"adjRealDmgDef":6,"adjDebilityEnh":8,"adjDebilityAnti":8})
    }),
    51000057: _tools.RODict({
        "propID": 51000057,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4182,"adjMinPhysicalAtk":64,"adjMaxPhysicalAtk":116,"adjMinMagicAtk":64,"adjMaxMagicAtk":116,"adjMinPhysicalArmor":57,"adjMaxPhysicalArmor":57,"adjMinMagicArmor":57,"adjMaxMagicArmor":57,"adjHit":37,"adjRealDmg":7,"adjRealDmgDef":6,"adjDebilityEnh":8,"adjDebilityAnti":8})
    }),
    51000058: _tools.RODict({
        "propID": 51000058,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4236,"adjMinPhysicalAtk":65,"adjMaxPhysicalAtk":118,"adjMinMagicAtk":65,"adjMaxMagicAtk":118,"adjMinPhysicalArmor":57,"adjMaxPhysicalArmor":57,"adjMinMagicArmor":57,"adjMaxMagicArmor":57,"adjHit":39,"adjRealDmg":7,"adjRealDmgDef":7,"adjDebilityEnh":8,"adjDebilityAnti":9})
    }),
    51000059: _tools.RODict({
        "propID": 51000059,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4422,"adjMinPhysicalAtk":69,"adjMaxPhysicalAtk":126,"adjMinMagicAtk":69,"adjMaxMagicAtk":126,"adjMinPhysicalArmor":58,"adjMaxPhysicalArmor":58,"adjMinMagicArmor":58,"adjMaxMagicArmor":58,"adjHit":39,"adjRealDmg":7,"adjRealDmgDef":7,"adjDebilityEnh":9,"adjDebilityAnti":9})
    }),
    51000060: _tools.RODict({
        "propID": 51000060,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4598,"adjMinPhysicalAtk":71,"adjMaxPhysicalAtk":129,"adjMinMagicAtk":71,"adjMaxMagicAtk":129,"adjMinPhysicalArmor":59,"adjMaxPhysicalArmor":59,"adjMinMagicArmor":59,"adjMaxMagicArmor":59,"adjHit":42,"adjRealDmg":7,"adjRealDmgDef":7,"adjDebilityEnh":9,"adjDebilityAnti":9})
    }),
    51000061: _tools.RODict({
        "propID": 51000061,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5181,"adjMinPhysicalAtk":72,"adjMaxPhysicalAtk":130,"adjMinMagicAtk":72,"adjMaxMagicAtk":130,"adjMinPhysicalArmor":66,"adjMaxPhysicalArmor":66,"adjMinMagicArmor":66,"adjMaxMagicArmor":66,"adjHit":42,"adjRealDmg":7,"adjRealDmgDef":7,"adjDebilityEnh":9,"adjDebilityAnti":9})
    }),
    51000062: _tools.RODict({
        "propID": 51000062,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5369,"adjMinPhysicalAtk":76,"adjMaxPhysicalAtk":139,"adjMinMagicAtk":76,"adjMaxMagicAtk":139,"adjMinPhysicalArmor":68,"adjMaxPhysicalArmor":68,"adjMinMagicArmor":68,"adjMaxMagicArmor":68,"adjHit":42,"adjRealDmg":9,"adjRealDmgDef":7,"adjDebilityEnh":9,"adjDebilityAnti":9})
    }),
    51000063: _tools.RODict({
        "propID": 51000063,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5447,"adjMinPhysicalAtk":79,"adjMaxPhysicalAtk":144,"adjMinMagicAtk":79,"adjMaxMagicAtk":144,"adjMinPhysicalArmor":68,"adjMaxPhysicalArmor":68,"adjMinMagicArmor":68,"adjMaxMagicArmor":68,"adjHit":48,"adjRealDmg":9,"adjRealDmgDef":9,"adjDebilityEnh":9,"adjDebilityAnti":11})
    }),
    51000064: _tools.RODict({
        "propID": 51000064,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5728,"adjMinPhysicalAtk":83,"adjMaxPhysicalAtk":151,"adjMinMagicAtk":83,"adjMaxMagicAtk":151,"adjMinPhysicalArmor":69,"adjMaxPhysicalArmor":69,"adjMinMagicArmor":69,"adjMaxMagicArmor":69,"adjHit":48,"adjRealDmg":9,"adjRealDmgDef":9,"adjDebilityEnh":11,"adjDebilityAnti":11})
    }),
    51000065: _tools.RODict({
        "propID": 51000065,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":6027,"adjMinPhysicalAtk":85,"adjMaxPhysicalAtk":155,"adjMinMagicAtk":85,"adjMaxMagicAtk":155,"adjMinPhysicalArmor":70,"adjMaxPhysicalArmor":70,"adjMinMagicArmor":70,"adjMaxMagicArmor":70,"adjHit":52,"adjRealDmg":9,"adjRealDmgDef":9,"adjDebilityEnh":11,"adjDebilityAnti":11})
    }),
    51000066: _tools.RODict({
        "propID": 51000066,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":6539,"adjMinPhysicalAtk":85,"adjMaxPhysicalAtk":155,"adjMinMagicAtk":85,"adjMaxMagicAtk":155,"adjMinPhysicalArmor":76,"adjMaxPhysicalArmor":76,"adjMinMagicArmor":76,"adjMaxMagicArmor":76,"adjHit":52,"adjRealDmg":9,"adjRealDmgDef":9,"adjDebilityEnh":11,"adjDebilityAnti":11})
    }),
    51000067: _tools.RODict({
        "propID": 51000067,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":6772,"adjMinPhysicalAtk":90,"adjMaxPhysicalAtk":163,"adjMinMagicAtk":90,"adjMaxMagicAtk":163,"adjMinPhysicalArmor":78,"adjMaxPhysicalArmor":78,"adjMinMagicArmor":78,"adjMaxMagicArmor":78,"adjHit":52,"adjRealDmg":11,"adjRealDmgDef":9,"adjDebilityEnh":11,"adjDebilityAnti":11})
    }),
    51000068: _tools.RODict({
        "propID": 51000068,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":6850,"adjMinPhysicalAtk":91,"adjMaxPhysicalAtk":166,"adjMinMagicAtk":91,"adjMaxMagicAtk":166,"adjMinPhysicalArmor":79,"adjMaxPhysicalArmor":79,"adjMinMagicArmor":79,"adjMaxMagicArmor":79,"adjHit":54,"adjRealDmg":11,"adjRealDmgDef":11,"adjDebilityEnh":11,"adjDebilityAnti":12})
    }),
    51000069: _tools.RODict({
        "propID": 51000069,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":7103,"adjMinPhysicalAtk":97,"adjMaxPhysicalAtk":176,"adjMinMagicAtk":97,"adjMaxMagicAtk":176,"adjMinPhysicalArmor":79,"adjMaxPhysicalArmor":79,"adjMinMagicArmor":79,"adjMaxMagicArmor":79,"adjHit":54,"adjRealDmg":11,"adjRealDmgDef":11,"adjDebilityEnh":12,"adjDebilityAnti":12})
    }),
    51000070: _tools.RODict({
        "propID": 51000070,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":7345,"adjMinPhysicalAtk":99,"adjMaxPhysicalAtk":180,"adjMinMagicAtk":99,"adjMaxMagicAtk":180,"adjMinPhysicalArmor":80,"adjMaxPhysicalArmor":80,"adjMinMagicArmor":80,"adjMaxMagicArmor":80,"adjHit":58,"adjRealDmg":11,"adjRealDmgDef":11,"adjDebilityEnh":12,"adjDebilityAnti":12})
    }),
    51001001: _tools.RODict({
        "propID": 51001001,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":90,"adjMinPhysicalAtk":5,"adjMaxPhysicalAtk":10,"adjMinMagicAtk":5,"adjMaxMagicAtk":10,"adjRealDmg":1,"adjDebilityAnti":2})
    }),
    51001002: _tools.RODict({
        "propID": 51001002,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":470,"adjMinPhysicalAtk":5,"adjMaxPhysicalAtk":10,"adjMinMagicAtk":5,"adjMaxMagicAtk":10,"adjRealDmg":1,"adjDebilityAnti":2})
    }),
    51001003: _tools.RODict({
        "propID": 51001003,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":480,"adjMinPhysicalAtk":6,"adjMaxPhysicalAtk":11,"adjMinMagicAtk":6,"adjMaxMagicAtk":11,"adjRealDmg":1,"adjDebilityAnti":2})
    }),
    51001004: _tools.RODict({
        "propID": 51001004,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":480,"adjMinPhysicalAtk":8,"adjMaxPhysicalAtk":14,"adjMinMagicAtk":8,"adjMaxMagicAtk":14,"adjRealDmg":1,"adjDebilityAnti":2})
    }),
    51001005: _tools.RODict({
        "propID": 51001005,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":488,"adjMinPhysicalAtk":8,"adjMaxPhysicalAtk":16,"adjMinMagicAtk":8,"adjMaxMagicAtk":16,"adjRealDmg":1,"adjDebilityAnti":2})
    }),
    51001006: _tools.RODict({
        "propID": 51001006,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":488,"adjMinPhysicalAtk":10,"adjMaxPhysicalAtk":17,"adjMinMagicAtk":10,"adjMaxMagicAtk":17,"adjRealDmg":1,"adjDebilityAnti":2})
    }),
    51001007: _tools.RODict({
        "propID": 51001007,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":498,"adjMinPhysicalAtk":10,"adjMaxPhysicalAtk":18,"adjMinMagicAtk":10,"adjMaxMagicAtk":18,"adjRealDmg":1,"adjDebilityAnti":2})
    }),
    51001008: _tools.RODict({
        "propID": 51001008,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":498,"adjMinPhysicalAtk":10,"adjMaxPhysicalAtk":18,"adjMinMagicAtk":10,"adjMaxMagicAtk":18,"adjHit":4,"adjRealDmg":1,"adjDebilityAnti":2})
    }),
    51001009: _tools.RODict({
        "propID": 51001009,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":506,"adjMinPhysicalAtk":11,"adjMaxPhysicalAtk":19,"adjMinMagicAtk":11,"adjMaxMagicAtk":19,"adjHit":4,"adjRealDmg":1,"adjDebilityAnti":2})
    }),
    51001010: _tools.RODict({
        "propID": 51001010,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":562,"adjMinPhysicalAtk":11,"adjMaxPhysicalAtk":19,"adjMinMagicAtk":11,"adjMaxMagicAtk":19,"adjHit":4,"adjRealDmg":1,"adjDebilityAnti":2})
    }),
    51001011: _tools.RODict({
        "propID": 51001011,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":590,"adjMinPhysicalAtk":12,"adjMaxPhysicalAtk":22,"adjMinMagicAtk":12,"adjMaxMagicAtk":22,"adjMinPhysicalArmor":1,"adjMaxPhysicalArmor":1,"adjMinMagicArmor":1,"adjMaxMagicArmor":1,"adjHit":4,"adjRealDmg":1,"adjDebilityAnti":2})
    }),
    51001012: _tools.RODict({
        "propID": 51001012,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":608,"adjMinPhysicalAtk":12,"adjMaxPhysicalAtk":23,"adjMinMagicAtk":12,"adjMaxMagicAtk":23,"adjMinPhysicalArmor":2,"adjMaxPhysicalArmor":2,"adjMinMagicArmor":2,"adjMaxMagicArmor":2,"adjHit":4,"adjRealDmg":1,"adjDebilityAnti":2})
    }),
    51001013: _tools.RODict({
        "propID": 51001013,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":638,"adjMinPhysicalAtk":13,"adjMaxPhysicalAtk":24,"adjMinMagicAtk":13,"adjMaxMagicAtk":24,"adjMinPhysicalArmor":3,"adjMaxPhysicalArmor":3,"adjMinMagicArmor":3,"adjMaxMagicArmor":3,"adjHit":5,"adjRealDmg":1,"adjDebilityAnti":2})
    }),
    51001014: _tools.RODict({
        "propID": 51001014,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":656,"adjMinPhysicalAtk":13,"adjMaxPhysicalAtk":24,"adjMinMagicAtk":13,"adjMaxMagicAtk":24,"adjMinPhysicalArmor":4,"adjMaxPhysicalArmor":4,"adjMinMagicArmor":4,"adjMaxMagicArmor":4,"adjHit":5,"adjRealDmg":1,"adjDebilityAnti":2})
    }),
    51001015: _tools.RODict({
        "propID": 51001015,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":792,"adjMinPhysicalAtk":14,"adjMaxPhysicalAtk":25,"adjMinMagicAtk":14,"adjMaxMagicAtk":25,"adjMinPhysicalArmor":5,"adjMaxPhysicalArmor":5,"adjMinMagicArmor":5,"adjMaxMagicArmor":5,"adjHit":5,"adjRealDmg":1,"adjDebilityAnti":2})
    }),
    51001016: _tools.RODict({
        "propID": 51001016,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":814,"adjMinPhysicalAtk":16,"adjMaxPhysicalAtk":28,"adjMinMagicAtk":16,"adjMaxMagicAtk":28,"adjMinPhysicalArmor":6,"adjMaxPhysicalArmor":6,"adjMinMagicArmor":6,"adjMaxMagicArmor":6,"adjHit":5,"adjRealDmg":1,"adjDebilityAnti":2})
    }),
    51001017: _tools.RODict({
        "propID": 51001017,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":848,"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":30,"adjMinMagicAtk":17,"adjMaxMagicAtk":30,"adjMinPhysicalArmor":8,"adjMaxPhysicalArmor":8,"adjMinMagicArmor":8,"adjMaxMagicArmor":8,"adjHit":5,"adjRealDmg":1,"adjDebilityAnti":2})
    }),
    51001018: _tools.RODict({
        "propID": 51001018,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":872,"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":30,"adjMinMagicAtk":17,"adjMaxMagicAtk":30,"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10,"adjHit":6,"adjRealDmg":1,"adjDebilityAnti":2})
    }),
    51001019: _tools.RODict({
        "propID": 51001019,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":906,"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":31,"adjMinMagicAtk":17,"adjMaxMagicAtk":31,"adjMinPhysicalArmor":14,"adjMaxPhysicalArmor":14,"adjMinMagicArmor":14,"adjMaxMagicArmor":14,"adjHit":6,"adjRealDmg":1,"adjDebilityAnti":2})
    }),
    51001020: _tools.RODict({
        "propID": 51001020,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1002,"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":31,"adjMinMagicAtk":17,"adjMaxMagicAtk":31,"adjMinPhysicalArmor":15,"adjMaxPhysicalArmor":15,"adjMinMagicArmor":15,"adjMaxMagicArmor":15,"adjHit":6,"adjRealDmg":1,"adjDebilityAnti":2})
    }),
    51001021: _tools.RODict({
        "propID": 51001021,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1052,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":40,"adjMinMagicAtk":22,"adjMaxMagicAtk":40,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjHit":6,"adjRealDmg":1,"adjDebilityAnti":3})
    }),
    51001022: _tools.RODict({
        "propID": 51001022,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1078,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":40,"adjMinMagicAtk":22,"adjMaxMagicAtk":40,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjHit":10,"adjRealDmg":1,"adjDebilityAnti":3})
    }),
    51001023: _tools.RODict({
        "propID": 51001023,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1168,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":41,"adjMinMagicAtk":23,"adjMaxMagicAtk":41,"adjMinPhysicalArmor":17,"adjMaxPhysicalArmor":17,"adjMinMagicArmor":17,"adjMaxMagicArmor":17,"adjHit":10,"adjRealDmg":1,"adjDebilityAnti":3})
    }),
    51001024: _tools.RODict({
        "propID": 51001024,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1248,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":41,"adjMinMagicAtk":23,"adjMaxMagicAtk":41,"adjMinPhysicalArmor":18,"adjMaxPhysicalArmor":18,"adjMinMagicArmor":18,"adjMaxMagicArmor":18,"adjHit":10,"adjRealDmg":1,"adjDebilityAnti":3})
    }),
    51001025: _tools.RODict({
        "propID": 51001025,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1480,"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":47,"adjMinMagicAtk":25,"adjMaxMagicAtk":47,"adjMinPhysicalArmor":20,"adjMaxPhysicalArmor":20,"adjMinMagicArmor":20,"adjMaxMagicArmor":20,"adjHit":10,"adjRealDmg":1,"adjDebilityAnti":4})
    }),
    51001026: _tools.RODict({
        "propID": 51001026,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1512,"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":47,"adjMinMagicAtk":25,"adjMaxMagicAtk":47,"adjMinPhysicalArmor":21,"adjMaxPhysicalArmor":21,"adjMinMagicArmor":21,"adjMaxMagicArmor":21,"adjHit":12,"adjRealDmg":1,"adjDebilityAnti":4})
    }),
    51001027: _tools.RODict({
        "propID": 51001027,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1560,"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":48,"adjMinMagicAtk":26,"adjMaxMagicAtk":48,"adjMinPhysicalArmor":21,"adjMaxPhysicalArmor":21,"adjMinMagicArmor":21,"adjMaxMagicArmor":21,"adjHit":12,"adjRealDmg":1,"adjDebilityAnti":4})
    }),
    51001028: _tools.RODict({
        "propID": 51001028,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1652,"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":48,"adjMinMagicAtk":26,"adjMaxMagicAtk":48,"adjMinPhysicalArmor":22,"adjMaxPhysicalArmor":22,"adjMinMagicArmor":22,"adjMaxMagicArmor":22,"adjHit":12,"adjRealDmg":1,"adjDebilityAnti":4})
    }),
    51001029: _tools.RODict({
        "propID": 51001029,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1892,"adjMinPhysicalAtk":29,"adjMaxPhysicalAtk":52,"adjMinMagicAtk":29,"adjMaxMagicAtk":52,"adjMinPhysicalArmor":23,"adjMaxPhysicalArmor":23,"adjMinMagicArmor":23,"adjMaxMagicArmor":23,"adjHit":12,"adjRealDmg":1,"adjDebilityAnti":5})
    }),
    51001030: _tools.RODict({
        "propID": 51001030,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1946,"adjMinPhysicalAtk":29,"adjMaxPhysicalAtk":53,"adjMinMagicAtk":29,"adjMaxMagicAtk":53,"adjMinPhysicalArmor":24,"adjMaxPhysicalArmor":24,"adjMinMagicArmor":24,"adjMaxMagicArmor":24,"adjHit":14,"adjRealDmg":1,"adjDebilityAnti":5})
    }),
    51001031: _tools.RODict({
        "propID": 51001031,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2062,"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":54,"adjMinMagicAtk":30,"adjMaxMagicAtk":54,"adjMinPhysicalArmor":24,"adjMaxPhysicalArmor":24,"adjMinMagicArmor":24,"adjMaxMagicArmor":24,"adjHit":14,"adjRealDmg":1,"adjDebilityAnti":5})
    }),
    51001032: _tools.RODict({
        "propID": 51001032,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2196,"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":54,"adjMinMagicAtk":30,"adjMaxMagicAtk":54,"adjMinPhysicalArmor":25,"adjMaxPhysicalArmor":25,"adjMinMagicArmor":25,"adjMaxMagicArmor":25,"adjHit":14,"adjRealDmg":1,"adjDebilityAnti":5})
    }),
    51001033: _tools.RODict({
        "propID": 51001033,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2446,"adjMinPhysicalAtk":34,"adjMaxPhysicalAtk":61,"adjMinMagicAtk":34,"adjMaxMagicAtk":61,"adjMinPhysicalArmor":27,"adjMaxPhysicalArmor":27,"adjMinMagicArmor":27,"adjMaxMagicArmor":27,"adjHit":14,"adjRealDmg":1,"adjDebilityAnti":6})
    }),
    51001034: _tools.RODict({
        "propID": 51001034,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2510,"adjMinPhysicalAtk":35,"adjMaxPhysicalAtk":64,"adjMinMagicAtk":35,"adjMaxMagicAtk":64,"adjMinPhysicalArmor":27,"adjMaxPhysicalArmor":27,"adjMinMagicArmor":27,"adjMaxMagicArmor":27,"adjHit":16,"adjRealDmg":1,"adjDebilityAnti":6})
    }),
    51001035: _tools.RODict({
        "propID": 51001035,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2622,"adjMinPhysicalAtk":37,"adjMaxPhysicalAtk":67,"adjMinMagicAtk":37,"adjMaxMagicAtk":67,"adjMinPhysicalArmor":28,"adjMaxPhysicalArmor":28,"adjMinMagicArmor":28,"adjMaxMagicArmor":28,"adjHit":16,"adjRealDmg":1,"adjDebilityAnti":6})
    }),
    51001036: _tools.RODict({
        "propID": 51001036,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2704,"adjMinPhysicalAtk":37,"adjMaxPhysicalAtk":67,"adjMinMagicAtk":37,"adjMaxMagicAtk":67,"adjMinPhysicalArmor":28,"adjMaxPhysicalArmor":28,"adjMinMagicArmor":28,"adjMaxMagicArmor":28,"adjHit":16,"adjRealDmg":1,"adjDebilityAnti":6})
    }),
    51001037: _tools.RODict({
        "propID": 51001037,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2976,"adjMinPhysicalAtk":37,"adjMaxPhysicalAtk":68,"adjMinMagicAtk":37,"adjMaxMagicAtk":68,"adjMinPhysicalArmor":30,"adjMaxPhysicalArmor":30,"adjMinMagicArmor":30,"adjMaxMagicArmor":30,"adjHit":17,"adjRealDmg":1,"adjDebilityAnti":6})
    }),
    51001038: _tools.RODict({
        "propID": 51001038,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3028,"adjMinPhysicalAtk":43,"adjMaxPhysicalAtk":78,"adjMinMagicAtk":43,"adjMaxMagicAtk":78,"adjMinPhysicalArmor":30,"adjMaxPhysicalArmor":30,"adjMinMagicArmor":30,"adjMaxMagicArmor":30,"adjHit":17,"adjRealDmg":1,"adjDebilityAnti":7})
    }),
    51001039: _tools.RODict({
        "propID": 51001039,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3134,"adjMinPhysicalAtk":44,"adjMaxPhysicalAtk":80,"adjMinMagicAtk":44,"adjMaxMagicAtk":80,"adjMinPhysicalArmor":30,"adjMaxPhysicalArmor":30,"adjMinMagicArmor":30,"adjMaxMagicArmor":30,"adjHit":23,"adjRealDmg":1,"adjDebilityEnh":5,"adjDebilityAnti":7})
    }),
    51001040: _tools.RODict({
        "propID": 51001040,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3584,"adjMinPhysicalAtk":44,"adjMaxPhysicalAtk":82,"adjMinMagicAtk":44,"adjMaxMagicAtk":82,"adjMinPhysicalArmor":32,"adjMaxPhysicalArmor":32,"adjMinMagicArmor":32,"adjMaxMagicArmor":32,"adjHit":23,"adjRealDmg":1,"adjDebilityEnh":5,"adjDebilityAnti":7})
    }),
    51001041: _tools.RODict({
        "propID": 51001041,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4234,"adjMinPhysicalAtk":46,"adjMaxPhysicalAtk":83,"adjMinMagicAtk":46,"adjMaxMagicAtk":83,"adjMinPhysicalArmor":38,"adjMaxPhysicalArmor":38,"adjMinMagicArmor":38,"adjMaxMagicArmor":38,"adjHit":23,"adjRealDmg":1,"adjDebilityEnh":5,"adjDebilityAnti":7})
    }),
    51001042: _tools.RODict({
        "propID": 51001042,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4302,"adjMinPhysicalAtk":48,"adjMaxPhysicalAtk":86,"adjMinMagicAtk":48,"adjMaxMagicAtk":86,"adjMinPhysicalArmor":38,"adjMaxPhysicalArmor":38,"adjMinMagicArmor":38,"adjMaxMagicArmor":38,"adjHit":23,"adjRealDmg":2,"adjDebilityEnh":5,"adjDebilityAnti":7})
    }),
    51001043: _tools.RODict({
        "propID": 51001043,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4390,"adjMinPhysicalAtk":50,"adjMaxPhysicalAtk":91,"adjMinMagicAtk":50,"adjMaxMagicAtk":91,"adjMinPhysicalArmor":38,"adjMaxPhysicalArmor":38,"adjMinMagicArmor":38,"adjMaxMagicArmor":38,"adjHit":25,"adjRealDmg":2,"adjRealDmgDef":1,"adjDebilityEnh":5,"adjDebilityAnti":8})
    }),
    51001044: _tools.RODict({
        "propID": 51001044,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4538,"adjMinPhysicalAtk":52,"adjMaxPhysicalAtk":94,"adjMinMagicAtk":52,"adjMaxMagicAtk":94,"adjMinPhysicalArmor":39,"adjMaxPhysicalArmor":39,"adjMinMagicArmor":39,"adjMaxMagicArmor":39,"adjHit":26,"adjRealDmg":2,"adjRealDmgDef":1,"adjDebilityEnh":6,"adjDebilityAnti":8})
    }),
    51001045: _tools.RODict({
        "propID": 51001045,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4706,"adjMinPhysicalAtk":54,"adjMaxPhysicalAtk":97,"adjMinMagicAtk":54,"adjMaxMagicAtk":97,"adjMinPhysicalArmor":39,"adjMaxPhysicalArmor":39,"adjMinMagicArmor":39,"adjMaxMagicArmor":39,"adjHit":26,"adjRealDmg":2,"adjRealDmgDef":1,"adjDebilityEnh":6,"adjDebilityAnti":8})
    }),
    51001046: _tools.RODict({
        "propID": 51001046,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5238,"adjMinPhysicalAtk":54,"adjMaxPhysicalAtk":97,"adjMinMagicAtk":54,"adjMaxMagicAtk":97,"adjMinPhysicalArmor":42,"adjMaxPhysicalArmor":42,"adjMinMagicArmor":42,"adjMaxMagicArmor":42,"adjHit":26,"adjRealDmg":3,"adjRealDmgDef":1,"adjDebilityEnh":6,"adjDebilityAnti":8})
    }),
    51001047: _tools.RODict({
        "propID": 51001047,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5336,"adjMinPhysicalAtk":58,"adjMaxPhysicalAtk":104,"adjMinMagicAtk":58,"adjMaxMagicAtk":104,"adjMinPhysicalArmor":42,"adjMaxPhysicalArmor":42,"adjMinMagicArmor":42,"adjMaxMagicArmor":42,"adjHit":26,"adjRealDmg":3,"adjRealDmgDef":2,"adjDebilityEnh":6,"adjDebilityAnti":8})
    }),
    51001048: _tools.RODict({
        "propID": 51001048,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5416,"adjMinPhysicalAtk":58,"adjMaxPhysicalAtk":106,"adjMinMagicAtk":58,"adjMaxMagicAtk":106,"adjMinPhysicalArmor":43,"adjMaxPhysicalArmor":43,"adjMinMagicArmor":43,"adjMaxMagicArmor":43,"adjHit":30,"adjRealDmg":3,"adjRealDmgDef":2,"adjDebilityEnh":6,"adjDebilityAnti":9})
    }),
    51001049: _tools.RODict({
        "propID": 51001049,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5788,"adjMinPhysicalAtk":60,"adjMaxPhysicalAtk":109,"adjMinMagicAtk":60,"adjMaxMagicAtk":109,"adjMinPhysicalArmor":44,"adjMaxPhysicalArmor":44,"adjMinMagicArmor":44,"adjMaxMagicArmor":44,"adjHit":30,"adjRealDmg":4,"adjRealDmgDef":2,"adjDebilityEnh":7,"adjDebilityAnti":9})
    }),
    51001050: _tools.RODict({
        "propID": 51001050,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":6020,"adjMinPhysicalAtk":64,"adjMaxPhysicalAtk":115,"adjMinMagicAtk":64,"adjMaxMagicAtk":115,"adjMinPhysicalArmor":45,"adjMaxPhysicalArmor":45,"adjMinMagicArmor":45,"adjMaxMagicArmor":45,"adjHit":32,"adjRealDmg":4,"adjRealDmgDef":3,"adjDebilityEnh":7,"adjDebilityAnti":9})
    }),
    51001051: _tools.RODict({
        "propID": 51001051,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":6556,"adjMinPhysicalAtk":64,"adjMaxPhysicalAtk":116,"adjMinMagicAtk":64,"adjMaxMagicAtk":116,"adjMinPhysicalArmor":49,"adjMaxPhysicalArmor":49,"adjMinMagicArmor":49,"adjMaxMagicArmor":49,"adjHit":32,"adjRealDmg":4,"adjRealDmgDef":3,"adjDebilityEnh":7,"adjDebilityAnti":9})
    }),
    51001052: _tools.RODict({
        "propID": 51001052,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":6822,"adjMinPhysicalAtk":66,"adjMaxPhysicalAtk":120,"adjMinMagicAtk":66,"adjMaxMagicAtk":120,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":50,"adjMaxMagicArmor":50,"adjHit":32,"adjRealDmg":4,"adjRealDmgDef":3,"adjDebilityEnh":7,"adjDebilityAnti":9})
    }),
    51001053: _tools.RODict({
        "propID": 51001053,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":6938,"adjMinPhysicalAtk":68,"adjMaxPhysicalAtk":124,"adjMinMagicAtk":68,"adjMaxMagicAtk":124,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":50,"adjMaxMagicArmor":50,"adjHit":34,"adjRealDmg":6,"adjRealDmgDef":3,"adjDebilityEnh":7,"adjDebilityAnti":10})
    }),
    51001054: _tools.RODict({
        "propID": 51001054,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":7144,"adjMinPhysicalAtk":71,"adjMaxPhysicalAtk":130,"adjMinMagicAtk":71,"adjMaxMagicAtk":130,"adjMinPhysicalArmor":51,"adjMaxPhysicalArmor":51,"adjMinMagicArmor":51,"adjMaxMagicArmor":51,"adjHit":34,"adjRealDmg":6,"adjRealDmgDef":5,"adjDebilityEnh":8,"adjDebilityAnti":10})
    }),
    51001055: _tools.RODict({
        "propID": 51001055,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":7378,"adjMinPhysicalAtk":74,"adjMaxPhysicalAtk":134,"adjMinMagicAtk":74,"adjMaxMagicAtk":134,"adjMinPhysicalArmor":52,"adjMaxPhysicalArmor":52,"adjMinMagicArmor":52,"adjMaxMagicArmor":52,"adjHit":37,"adjRealDmg":6,"adjRealDmgDef":5,"adjDebilityEnh":8,"adjDebilityAnti":10})
    }),
    51001056: _tools.RODict({
        "propID": 51001056,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":8026,"adjMinPhysicalAtk":74,"adjMaxPhysicalAtk":134,"adjMinMagicAtk":74,"adjMaxMagicAtk":134,"adjMinPhysicalArmor":56,"adjMaxPhysicalArmor":56,"adjMinMagicArmor":56,"adjMaxMagicArmor":56,"adjHit":37,"adjRealDmg":6,"adjRealDmgDef":5,"adjDebilityEnh":8,"adjDebilityAnti":10})
    }),
    51001057: _tools.RODict({
        "propID": 51001057,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":8364,"adjMinPhysicalAtk":77,"adjMaxPhysicalAtk":139,"adjMinMagicAtk":77,"adjMaxMagicAtk":139,"adjMinPhysicalArmor":57,"adjMaxPhysicalArmor":57,"adjMinMagicArmor":57,"adjMaxMagicArmor":57,"adjHit":37,"adjRealDmg":6,"adjRealDmgDef":5,"adjDebilityEnh":8,"adjDebilityAnti":10})
    }),
    51001058: _tools.RODict({
        "propID": 51001058,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":8472,"adjMinPhysicalAtk":78,"adjMaxPhysicalAtk":142,"adjMinMagicAtk":78,"adjMaxMagicAtk":142,"adjMinPhysicalArmor":57,"adjMaxPhysicalArmor":57,"adjMinMagicArmor":57,"adjMaxMagicArmor":57,"adjHit":39,"adjRealDmg":8,"adjRealDmgDef":5,"adjDebilityEnh":8,"adjDebilityAnti":11})
    }),
    51001059: _tools.RODict({
        "propID": 51001059,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":8844,"adjMinPhysicalAtk":83,"adjMaxPhysicalAtk":151,"adjMinMagicAtk":83,"adjMaxMagicAtk":151,"adjMinPhysicalArmor":58,"adjMaxPhysicalArmor":58,"adjMinMagicArmor":58,"adjMaxMagicArmor":58,"adjHit":39,"adjRealDmg":8,"adjRealDmgDef":7,"adjDebilityEnh":9,"adjDebilityAnti":11})
    }),
    51001060: _tools.RODict({
        "propID": 51001060,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":9196,"adjMinPhysicalAtk":85,"adjMaxPhysicalAtk":155,"adjMinMagicAtk":85,"adjMaxMagicAtk":155,"adjMinPhysicalArmor":59,"adjMaxPhysicalArmor":59,"adjMinMagicArmor":59,"adjMaxMagicArmor":59,"adjHit":42,"adjRealDmg":8,"adjRealDmgDef":7,"adjDebilityEnh":9,"adjDebilityAnti":11})
    }),
    51001061: _tools.RODict({
        "propID": 51001061,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":10362,"adjMinPhysicalAtk":86,"adjMaxPhysicalAtk":156,"adjMinMagicAtk":86,"adjMaxMagicAtk":156,"adjMinPhysicalArmor":66,"adjMaxPhysicalArmor":66,"adjMinMagicArmor":66,"adjMaxMagicArmor":66,"adjHit":42,"adjRealDmg":8,"adjRealDmgDef":7,"adjDebilityEnh":9,"adjDebilityAnti":11})
    }),
    51001062: _tools.RODict({
        "propID": 51001062,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":10738,"adjMinPhysicalAtk":91,"adjMaxPhysicalAtk":167,"adjMinMagicAtk":91,"adjMaxMagicAtk":167,"adjMinPhysicalArmor":68,"adjMaxPhysicalArmor":68,"adjMinMagicArmor":68,"adjMaxMagicArmor":68,"adjHit":42,"adjRealDmg":8,"adjRealDmgDef":7,"adjDebilityEnh":9,"adjDebilityAnti":11})
    }),
    51001063: _tools.RODict({
        "propID": 51001063,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":10894,"adjMinPhysicalAtk":95,"adjMaxPhysicalAtk":173,"adjMinMagicAtk":95,"adjMaxMagicAtk":173,"adjMinPhysicalArmor":68,"adjMaxPhysicalArmor":68,"adjMinMagicArmor":68,"adjMaxMagicArmor":68,"adjHit":48,"adjRealDmg":10,"adjRealDmgDef":7,"adjDebilityEnh":9,"adjDebilityAnti":13})
    }),
    51001064: _tools.RODict({
        "propID": 51001064,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":11456,"adjMinPhysicalAtk":100,"adjMaxPhysicalAtk":181,"adjMinMagicAtk":100,"adjMaxMagicAtk":181,"adjMinPhysicalArmor":69,"adjMaxPhysicalArmor":69,"adjMinMagicArmor":69,"adjMaxMagicArmor":69,"adjHit":48,"adjRealDmg":10,"adjRealDmgDef":9,"adjDebilityEnh":11,"adjDebilityAnti":13})
    }),
    51001065: _tools.RODict({
        "propID": 51001065,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":12054,"adjMinPhysicalAtk":102,"adjMaxPhysicalAtk":186,"adjMinMagicAtk":102,"adjMaxMagicAtk":186,"adjMinPhysicalArmor":70,"adjMaxPhysicalArmor":70,"adjMinMagicArmor":70,"adjMaxMagicArmor":70,"adjHit":52,"adjRealDmg":10,"adjRealDmgDef":9,"adjDebilityEnh":11,"adjDebilityAnti":13})
    }),
    51001066: _tools.RODict({
        "propID": 51001066,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":13078,"adjMinPhysicalAtk":102,"adjMaxPhysicalAtk":186,"adjMinMagicAtk":102,"adjMaxMagicAtk":186,"adjMinPhysicalArmor":76,"adjMaxPhysicalArmor":76,"adjMinMagicArmor":76,"adjMaxMagicArmor":76,"adjHit":52,"adjRealDmg":10,"adjRealDmgDef":9,"adjDebilityEnh":11,"adjDebilityAnti":13})
    }),
    51001067: _tools.RODict({
        "propID": 51001067,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":13544,"adjMinPhysicalAtk":108,"adjMaxPhysicalAtk":196,"adjMinMagicAtk":108,"adjMaxMagicAtk":196,"adjMinPhysicalArmor":78,"adjMaxPhysicalArmor":78,"adjMinMagicArmor":78,"adjMaxMagicArmor":78,"adjHit":52,"adjRealDmg":10,"adjRealDmgDef":9,"adjDebilityEnh":11,"adjDebilityAnti":13})
    }),
    51001068: _tools.RODict({
        "propID": 51001068,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":13700,"adjMinPhysicalAtk":109,"adjMaxPhysicalAtk":199,"adjMinMagicAtk":109,"adjMaxMagicAtk":199,"adjMinPhysicalArmor":79,"adjMaxPhysicalArmor":79,"adjMinMagicArmor":79,"adjMaxMagicArmor":79,"adjHit":54,"adjRealDmg":13,"adjRealDmgDef":9,"adjDebilityEnh":11,"adjDebilityAnti":14})
    }),
    51001069: _tools.RODict({
        "propID": 51001069,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":14206,"adjMinPhysicalAtk":116,"adjMaxPhysicalAtk":211,"adjMinMagicAtk":116,"adjMaxMagicAtk":211,"adjMinPhysicalArmor":79,"adjMaxPhysicalArmor":79,"adjMinMagicArmor":79,"adjMaxMagicArmor":79,"adjHit":54,"adjRealDmg":13,"adjRealDmgDef":12,"adjDebilityEnh":12,"adjDebilityAnti":14})
    }),
    51001070: _tools.RODict({
        "propID": 51001070,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":14690,"adjMinPhysicalAtk":119,"adjMaxPhysicalAtk":216,"adjMinMagicAtk":119,"adjMaxMagicAtk":216,"adjMinPhysicalArmor":80,"adjMaxPhysicalArmor":80,"adjMinMagicArmor":80,"adjMaxMagicArmor":80,"adjHit":58,"adjRealDmg":13,"adjRealDmgDef":12,"adjDebilityEnh":12,"adjDebilityAnti":14})
    }),
    51002001: _tools.RODict({
        "propID": 51002001,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":589,"adjMinPhysicalAtk":14,"adjMaxPhysicalAtk":18,"adjMinMagicAtk":14,"adjMaxMagicAtk":18,"adjMinPhysicalArmor":2,"adjMaxPhysicalArmor":2,"adjMinMagicArmor":2,"adjMaxMagicArmor":2,"adjHit":36,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":4})
    }),
    51002002: _tools.RODict({
        "propID": 51002002,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3125,"adjMinPhysicalAtk":14,"adjMaxPhysicalAtk":19,"adjMinMagicAtk":14,"adjMaxMagicAtk":19,"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjHit":36,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":4})
    }),
    51002003: _tools.RODict({
        "propID": 51002003,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3193,"adjMinPhysicalAtk":15,"adjMaxPhysicalAtk":20,"adjMinMagicAtk":15,"adjMaxMagicAtk":20,"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjHit":36,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":4})
    }),
    51002004: _tools.RODict({
        "propID": 51002004,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3193,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":28,"adjMinMagicAtk":21,"adjMaxMagicAtk":28,"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjHit":36,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":4})
    }),
    51002005: _tools.RODict({
        "propID": 51002005,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3261,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":30,"adjMinMagicAtk":23,"adjMaxMagicAtk":30,"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjHit":36,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":4})
    }),
    51002006: _tools.RODict({
        "propID": 51002006,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3216,"adjMinPhysicalAtk":29,"adjMaxPhysicalAtk":39,"adjMinMagicAtk":29,"adjMaxMagicAtk":39,"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10,"adjHit":36,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":4})
    }),
    51002007: _tools.RODict({
        "propID": 51002007,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3284,"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":40,"adjMinMagicAtk":30,"adjMaxMagicAtk":40,"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10,"adjHit":36,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":4})
    }),
    51002008: _tools.RODict({
        "propID": 51002008,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3284,"adjMinPhysicalAtk":36,"adjMaxPhysicalAtk":48,"adjMinMagicAtk":36,"adjMaxMagicAtk":48,"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10,"adjHit":40,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":4})
    }),
    51002009: _tools.RODict({
        "propID": 51002009,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3352,"adjMinPhysicalAtk":38,"adjMaxPhysicalAtk":50,"adjMinMagicAtk":38,"adjMaxMagicAtk":50,"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10,"adjHit":40,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":4})
    }),
    51002010: _tools.RODict({
        "propID": 51002010,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3669,"adjMinPhysicalAtk":38,"adjMaxPhysicalAtk":51,"adjMinMagicAtk":38,"adjMaxMagicAtk":51,"adjMinPhysicalArmor":12,"adjMaxPhysicalArmor":12,"adjMinMagicArmor":12,"adjMaxMagicArmor":12,"adjHit":40,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":4})
    }),
    51002011: _tools.RODict({
        "propID": 51002011,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3737,"adjMinPhysicalAtk":41,"adjMaxPhysicalAtk":54,"adjMinMagicAtk":41,"adjMaxMagicAtk":54,"adjMinPhysicalArmor":12,"adjMaxPhysicalArmor":12,"adjMinMagicArmor":12,"adjMaxMagicArmor":12,"adjHit":40,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":4})
    }),
    51002012: _tools.RODict({
        "propID": 51002012,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3737,"adjMinPhysicalAtk":43,"adjMaxPhysicalAtk":57,"adjMinMagicAtk":43,"adjMaxMagicAtk":57,"adjMinPhysicalArmor":12,"adjMaxPhysicalArmor":12,"adjMinMagicArmor":12,"adjMaxMagicArmor":12,"adjHit":40,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":4})
    }),
    51002013: _tools.RODict({
        "propID": 51002013,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3805,"adjMinPhysicalAtk":44,"adjMaxPhysicalAtk":59,"adjMinMagicAtk":44,"adjMaxMagicAtk":59,"adjMinPhysicalArmor":12,"adjMaxPhysicalArmor":12,"adjMinMagicArmor":12,"adjMaxMagicArmor":12,"adjHit":41,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":4})
    }),
    51002014: _tools.RODict({
        "propID": 51002014,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3760,"adjMinPhysicalAtk":45,"adjMaxPhysicalAtk":60,"adjMinMagicAtk":45,"adjMaxMagicAtk":60,"adjMinPhysicalArmor":13,"adjMaxPhysicalArmor":13,"adjMinMagicArmor":13,"adjMaxMagicArmor":13,"adjHit":41,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":4})
    }),
    51002015: _tools.RODict({
        "propID": 51002015,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4507,"adjMinPhysicalAtk":47,"adjMaxPhysicalAtk":62,"adjMinMagicAtk":47,"adjMaxMagicAtk":62,"adjMinPhysicalArmor":13,"adjMaxPhysicalArmor":13,"adjMinMagicArmor":13,"adjMaxMagicArmor":13,"adjHit":41,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":4})
    }),
    51002016: _tools.RODict({
        "propID": 51002016,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4462,"adjMinPhysicalAtk":49,"adjMaxPhysicalAtk":65,"adjMinMagicAtk":49,"adjMaxMagicAtk":65,"adjMinPhysicalArmor":14,"adjMaxPhysicalArmor":14,"adjMinMagicArmor":14,"adjMaxMagicArmor":14,"adjHit":41,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":4})
    }),
    51002017: _tools.RODict({
        "propID": 51002017,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4529,"adjMinPhysicalAtk":52,"adjMaxPhysicalAtk":69,"adjMinMagicAtk":52,"adjMaxMagicAtk":69,"adjMinPhysicalArmor":14,"adjMaxPhysicalArmor":14,"adjMinMagicArmor":14,"adjMaxMagicArmor":14,"adjHit":41,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":4})
    }),
    51002018: _tools.RODict({
        "propID": 51002018,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4529,"adjMinPhysicalAtk":53,"adjMaxPhysicalAtk":70,"adjMinMagicAtk":53,"adjMaxMagicAtk":70,"adjMinPhysicalArmor":14,"adjMaxPhysicalArmor":14,"adjMinMagicArmor":14,"adjMaxMagicArmor":14,"adjHit":42,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":4})
    }),
    51002019: _tools.RODict({
        "propID": 51002019,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4597,"adjMinPhysicalAtk":54,"adjMaxPhysicalAtk":72,"adjMinMagicAtk":54,"adjMaxMagicAtk":72,"adjMinPhysicalArmor":14,"adjMaxPhysicalArmor":14,"adjMinMagicArmor":14,"adjMaxMagicArmor":14,"adjHit":42,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":4})
    }),
    51002020: _tools.RODict({
        "propID": 51002020,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4960,"adjMinPhysicalAtk":55,"adjMaxPhysicalAtk":73,"adjMinMagicAtk":55,"adjMaxMagicAtk":73,"adjMinPhysicalArmor":15,"adjMaxPhysicalArmor":15,"adjMinMagicArmor":15,"adjMaxMagicArmor":15,"adjHit":42,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":4})
    }),
    51002021: _tools.RODict({
        "propID": 51002021,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5050,"adjMinPhysicalAtk":63,"adjMaxPhysicalAtk":84,"adjMinMagicAtk":63,"adjMaxMagicAtk":84,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjHit":42,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":5})
    }),
    51002022: _tools.RODict({
        "propID": 51002022,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5050,"adjMinPhysicalAtk":65,"adjMaxPhysicalAtk":87,"adjMinMagicAtk":65,"adjMaxMagicAtk":87,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjHit":46,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":5})
    }),
    51002023: _tools.RODict({
        "propID": 51002023,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5345,"adjMinPhysicalAtk":68,"adjMaxPhysicalAtk":90,"adjMinMagicAtk":68,"adjMaxMagicAtk":90,"adjMinPhysicalArmor":17,"adjMaxPhysicalArmor":17,"adjMinMagicArmor":17,"adjMaxMagicArmor":17,"adjHit":46,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":5})
    }),
    51002024: _tools.RODict({
        "propID": 51002024,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5571,"adjMinPhysicalAtk":68,"adjMaxPhysicalAtk":90,"adjMinMagicAtk":68,"adjMaxMagicAtk":90,"adjMinPhysicalArmor":18,"adjMaxPhysicalArmor":18,"adjMinMagicArmor":18,"adjMaxMagicArmor":18,"adjHit":46,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":5})
    }),
    51002025: _tools.RODict({
        "propID": 51002025,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":6500,"adjMinPhysicalAtk":74,"adjMaxPhysicalAtk":98,"adjMinMagicAtk":74,"adjMaxMagicAtk":98,"adjMinPhysicalArmor":20,"adjMaxPhysicalArmor":20,"adjMinMagicArmor":20,"adjMaxMagicArmor":20,"adjHit":46,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":6})
    }),
    51002026: _tools.RODict({
        "propID": 51002026,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":6455,"adjMinPhysicalAtk":75,"adjMaxPhysicalAtk":100,"adjMinMagicAtk":75,"adjMaxMagicAtk":100,"adjMinPhysicalArmor":21,"adjMaxPhysicalArmor":21,"adjMinMagicArmor":21,"adjMaxMagicArmor":21,"adjHit":48,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":6})
    }),
    51002027: _tools.RODict({
        "propID": 51002027,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":6523,"adjMinPhysicalAtk":77,"adjMaxPhysicalAtk":102,"adjMinMagicAtk":77,"adjMaxMagicAtk":102,"adjMinPhysicalArmor":21,"adjMaxPhysicalArmor":21,"adjMinMagicArmor":21,"adjMaxMagicArmor":21,"adjHit":48,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":6})
    }),
    51002028: _tools.RODict({
        "propID": 51002028,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":6749,"adjMinPhysicalAtk":77,"adjMaxPhysicalAtk":103,"adjMinMagicAtk":77,"adjMaxMagicAtk":103,"adjMinPhysicalArmor":22,"adjMaxPhysicalArmor":22,"adjMinMagicArmor":22,"adjMaxMagicArmor":22,"adjHit":48,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":6})
    }),
    51002029: _tools.RODict({
        "propID": 51002029,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":7655,"adjMinPhysicalAtk":82,"adjMaxPhysicalAtk":109,"adjMinMagicAtk":82,"adjMaxMagicAtk":109,"adjMinPhysicalArmor":23,"adjMaxPhysicalArmor":23,"adjMinMagicArmor":23,"adjMaxMagicArmor":23,"adjHit":48,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":7})
    }),
    51002030: _tools.RODict({
        "propID": 51002030,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":7677,"adjMinPhysicalAtk":84,"adjMaxPhysicalAtk":112,"adjMinMagicAtk":84,"adjMaxMagicAtk":112,"adjMinPhysicalArmor":24,"adjMaxPhysicalArmor":24,"adjMinMagicArmor":24,"adjMaxMagicArmor":24,"adjHit":50,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":7})
    }),
    51002031: _tools.RODict({
        "propID": 51002031,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":8017,"adjMinPhysicalAtk":86,"adjMaxPhysicalAtk":114,"adjMinMagicAtk":86,"adjMaxMagicAtk":114,"adjMinPhysicalArmor":24,"adjMaxPhysicalArmor":24,"adjMinMagicArmor":24,"adjMaxMagicArmor":24,"adjHit":50,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":7})
    }),
    51002032: _tools.RODict({
        "propID": 51002032,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":8379,"adjMinPhysicalAtk":86,"adjMaxPhysicalAtk":115,"adjMinMagicAtk":86,"adjMaxMagicAtk":115,"adjMinPhysicalArmor":25,"adjMaxPhysicalArmor":25,"adjMinMagicArmor":25,"adjMaxMagicArmor":25,"adjHit":50,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":7})
    }),
    51002033: _tools.RODict({
        "propID": 51002033,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":9172,"adjMinPhysicalAtk":94,"adjMaxPhysicalAtk":125,"adjMinMagicAtk":94,"adjMaxMagicAtk":125,"adjMinPhysicalArmor":27,"adjMaxPhysicalArmor":27,"adjMinMagicArmor":27,"adjMaxMagicArmor":27,"adjHit":50,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":8})
    }),
    51002034: _tools.RODict({
        "propID": 51002034,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":9240,"adjMinPhysicalAtk":96,"adjMaxPhysicalAtk":128,"adjMinMagicAtk":96,"adjMaxMagicAtk":128,"adjMinPhysicalArmor":27,"adjMaxPhysicalArmor":27,"adjMinMagicArmor":27,"adjMaxMagicArmor":27,"adjHit":52,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":8})
    }),
    51002035: _tools.RODict({
        "propID": 51002035,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":9466,"adjMinPhysicalAtk":99,"adjMaxPhysicalAtk":132,"adjMinMagicAtk":99,"adjMaxMagicAtk":132,"adjMinPhysicalArmor":28,"adjMaxPhysicalArmor":28,"adjMinMagicArmor":28,"adjMaxMagicArmor":28,"adjHit":52,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":8})
    }),
    51002036: _tools.RODict({
        "propID": 51002036,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":9602,"adjMinPhysicalAtk":100,"adjMaxPhysicalAtk":133,"adjMinMagicAtk":100,"adjMaxMagicAtk":133,"adjMinPhysicalArmor":28,"adjMaxPhysicalArmor":28,"adjMinMagicArmor":28,"adjMaxMagicArmor":28,"adjHit":52,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":8})
    }),
    51002037: _tools.RODict({
        "propID": 51002037,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":10394,"adjMinPhysicalAtk":101,"adjMaxPhysicalAtk":135,"adjMinMagicAtk":101,"adjMaxMagicAtk":135,"adjMinPhysicalArmor":30,"adjMaxPhysicalArmor":30,"adjMinMagicArmor":30,"adjMaxMagicArmor":30,"adjHit":53,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":8})
    }),
    51002038: _tools.RODict({
        "propID": 51002038,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":10394,"adjMinPhysicalAtk":115,"adjMaxPhysicalAtk":153,"adjMinMagicAtk":115,"adjMaxMagicAtk":153,"adjMinPhysicalArmor":30,"adjMaxPhysicalArmor":30,"adjMinMagicArmor":30,"adjMaxMagicArmor":30,"adjHit":53,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":9})
    }),
    51002039: _tools.RODict({
        "propID": 51002039,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":10598,"adjMinPhysicalAtk":122,"adjMaxPhysicalAtk":162,"adjMinMagicAtk":122,"adjMaxMagicAtk":162,"adjMinPhysicalArmor":30,"adjMaxPhysicalArmor":30,"adjMinMagicArmor":30,"adjMaxMagicArmor":30,"adjHit":59,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityEnh":5,"adjDebilityAnti":9})
    }),
    51002040: _tools.RODict({
        "propID": 51002040,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":12002,"adjMinPhysicalAtk":123,"adjMaxPhysicalAtk":164,"adjMinMagicAtk":123,"adjMaxMagicAtk":164,"adjMinPhysicalArmor":32,"adjMaxPhysicalArmor":32,"adjMinMagicArmor":32,"adjMaxMagicArmor":32,"adjHit":59,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityEnh":5,"adjDebilityAnti":9})
    }),
    51002041: _tools.RODict({
        "propID": 51002041,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":13904,"adjMinPhysicalAtk":125,"adjMaxPhysicalAtk":166,"adjMinMagicAtk":125,"adjMaxMagicAtk":166,"adjMinPhysicalArmor":38,"adjMaxPhysicalArmor":38,"adjMinMagicArmor":38,"adjMaxMagicArmor":38,"adjHit":59,"adjDodge":2,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityEnh":5,"adjDebilityAnti":9})
    }),
    51002042: _tools.RODict({
        "propID": 51002042,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":13904,"adjMinPhysicalAtk":131,"adjMaxPhysicalAtk":174,"adjMinMagicAtk":131,"adjMaxMagicAtk":174,"adjMinPhysicalArmor":38,"adjMaxPhysicalArmor":38,"adjMinMagicArmor":38,"adjMaxMagicArmor":38,"adjHit":59,"adjDodge":2,"adjRealDmg":2,"adjRealDmgDef":1,"adjDebilityEnh":5,"adjDebilityAnti":9})
    }),
    51002043: _tools.RODict({
        "propID": 51002043,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":13972,"adjMinPhysicalAtk":139,"adjMaxPhysicalAtk":185,"adjMinMagicAtk":139,"adjMaxMagicAtk":185,"adjMinPhysicalArmor":38,"adjMaxPhysicalArmor":38,"adjMinMagicArmor":38,"adjMaxMagicArmor":38,"adjHit":61,"adjDodge":2,"adjRealDmg":2,"adjRealDmgDef":2,"adjDebilityEnh":5,"adjDebilityAnti":10})
    }),
    51002044: _tools.RODict({
        "propID": 51002044,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":14198,"adjMinPhysicalAtk":141,"adjMaxPhysicalAtk":188,"adjMinMagicAtk":141,"adjMaxMagicAtk":188,"adjMinPhysicalArmor":39,"adjMaxPhysicalArmor":39,"adjMinMagicArmor":39,"adjMaxMagicArmor":39,"adjHit":62,"adjDodge":2,"adjRealDmg":2,"adjRealDmgDef":2,"adjDebilityEnh":6,"adjDebilityAnti":10})
    }),
    51002045: _tools.RODict({
        "propID": 51002045,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":14538,"adjMinPhysicalAtk":144,"adjMaxPhysicalAtk":192,"adjMinMagicAtk":144,"adjMaxMagicAtk":192,"adjMinPhysicalArmor":39,"adjMaxPhysicalArmor":39,"adjMinMagicArmor":39,"adjMaxMagicArmor":39,"adjHit":62,"adjDodge":2,"adjRealDmg":2,"adjRealDmgDef":2,"adjDebilityEnh":6,"adjDebilityAnti":10})
    }),
    51002046: _tools.RODict({
        "propID": 51002046,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":15964,"adjMinPhysicalAtk":147,"adjMaxPhysicalAtk":196,"adjMinMagicAtk":147,"adjMaxMagicAtk":196,"adjMinPhysicalArmor":42,"adjMaxPhysicalArmor":42,"adjMinMagicArmor":42,"adjMaxMagicArmor":42,"adjHit":62,"adjDodge":2,"adjRealDmg":3,"adjRealDmgDef":2,"adjDebilityEnh":6,"adjDebilityAnti":10})
    }),
    51002047: _tools.RODict({
        "propID": 51002047,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":16032,"adjMinPhysicalAtk":154,"adjMaxPhysicalAtk":205,"adjMinMagicAtk":154,"adjMaxMagicAtk":205,"adjMinPhysicalArmor":42,"adjMaxPhysicalArmor":42,"adjMinMagicArmor":42,"adjMaxMagicArmor":42,"adjHit":62,"adjDodge":2,"adjRealDmg":3,"adjRealDmgDef":3,"adjDebilityEnh":6,"adjDebilityAnti":10})
    }),
    51002048: _tools.RODict({
        "propID": 51002048,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":15987,"adjMinPhysicalAtk":160,"adjMaxPhysicalAtk":213,"adjMinMagicAtk":160,"adjMaxMagicAtk":213,"adjMinPhysicalArmor":43,"adjMaxPhysicalArmor":43,"adjMinMagicArmor":43,"adjMaxMagicArmor":43,"adjHit":66,"adjDodge":2,"adjRealDmg":3,"adjRealDmgDef":3,"adjDebilityEnh":6,"adjDebilityAnti":11})
    }),
    51002049: _tools.RODict({
        "propID": 51002049,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":16893,"adjMinPhysicalAtk":165,"adjMaxPhysicalAtk":220,"adjMinMagicAtk":165,"adjMaxMagicAtk":220,"adjMinPhysicalArmor":44,"adjMaxPhysicalArmor":44,"adjMinMagicArmor":44,"adjMaxMagicArmor":44,"adjHit":66,"adjDodge":2,"adjRealDmg":4,"adjRealDmgDef":3,"adjDebilityEnh":7,"adjDebilityAnti":11})
    }),
    51002050: _tools.RODict({
        "propID": 51002050,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":17323,"adjMinPhysicalAtk":170,"adjMaxPhysicalAtk":226,"adjMinMagicAtk":170,"adjMaxMagicAtk":226,"adjMinPhysicalArmor":45,"adjMaxPhysicalArmor":45,"adjMinMagicArmor":45,"adjMaxMagicArmor":45,"adjHit":68,"adjDodge":2,"adjRealDmg":4,"adjRealDmgDef":4,"adjDebilityEnh":7,"adjDebilityAnti":11})
    }),
    51002051: _tools.RODict({
        "propID": 51002051,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":18568,"adjMinPhysicalAtk":171,"adjMaxPhysicalAtk":228,"adjMinMagicAtk":171,"adjMaxMagicAtk":228,"adjMinPhysicalArmor":49,"adjMaxPhysicalArmor":49,"adjMinMagicArmor":49,"adjMaxMagicArmor":49,"adjHit":68,"adjDodge":2,"adjRealDmg":4,"adjRealDmgDef":4,"adjDebilityEnh":7,"adjDebilityAnti":11})
    }),
    51002052: _tools.RODict({
        "propID": 51002052,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":19067,"adjMinPhysicalAtk":177,"adjMaxPhysicalAtk":236,"adjMinMagicAtk":177,"adjMaxMagicAtk":236,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":50,"adjMaxMagicArmor":50,"adjHit":68,"adjDodge":2,"adjRealDmg":4,"adjRealDmgDef":4,"adjDebilityEnh":7,"adjDebilityAnti":11})
    }),
    51002053: _tools.RODict({
        "propID": 51002053,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":19134,"adjMinPhysicalAtk":193,"adjMaxPhysicalAtk":257,"adjMinMagicAtk":193,"adjMaxMagicAtk":257,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":50,"adjMaxMagicArmor":50,"adjHit":70,"adjDodge":2,"adjRealDmg":6,"adjRealDmgDef":4,"adjDebilityEnh":7,"adjDebilityAnti":12})
    }),
    51002054: _tools.RODict({
        "propID": 51002054,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":19429,"adjMinPhysicalAtk":197,"adjMaxPhysicalAtk":263,"adjMinMagicAtk":197,"adjMaxMagicAtk":263,"adjMinPhysicalArmor":51,"adjMaxPhysicalArmor":51,"adjMinMagicArmor":51,"adjMaxMagicArmor":51,"adjHit":70,"adjDodge":2,"adjRealDmg":6,"adjRealDmgDef":6,"adjDebilityEnh":8,"adjDebilityAnti":12})
    }),
    51002055: _tools.RODict({
        "propID": 51002055,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":19791,"adjMinPhysicalAtk":200,"adjMaxPhysicalAtk":266,"adjMinMagicAtk":200,"adjMaxMagicAtk":266,"adjMinPhysicalArmor":52,"adjMaxPhysicalArmor":52,"adjMinMagicArmor":52,"adjMaxMagicArmor":52,"adjHit":73,"adjDodge":2,"adjRealDmg":6,"adjRealDmgDef":6,"adjDebilityEnh":8,"adjDebilityAnti":12})
    }),
    51002056: _tools.RODict({
        "propID": 51002056,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":21240,"adjMinPhysicalAtk":200,"adjMaxPhysicalAtk":267,"adjMinMagicAtk":200,"adjMaxMagicAtk":267,"adjMinPhysicalArmor":56,"adjMaxPhysicalArmor":56,"adjMinMagicArmor":56,"adjMaxMagicArmor":56,"adjHit":73,"adjDodge":2,"adjRealDmg":6,"adjRealDmgDef":6,"adjDebilityEnh":8,"adjDebilityAnti":12})
    }),
    51002057: _tools.RODict({
        "propID": 51002057,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":21874,"adjMinPhysicalAtk":207,"adjMaxPhysicalAtk":276,"adjMinMagicAtk":207,"adjMaxMagicAtk":276,"adjMinPhysicalArmor":57,"adjMaxPhysicalArmor":57,"adjMinMagicArmor":57,"adjMaxMagicArmor":57,"adjHit":73,"adjDodge":2,"adjRealDmg":6,"adjRealDmgDef":6,"adjDebilityEnh":8,"adjDebilityAnti":12})
    }),
    51002058: _tools.RODict({
        "propID": 51002058,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":21874,"adjMinPhysicalAtk":223,"adjMaxPhysicalAtk":297,"adjMinMagicAtk":223,"adjMaxMagicAtk":297,"adjMinPhysicalArmor":57,"adjMaxPhysicalArmor":57,"adjMinMagicArmor":57,"adjMaxMagicArmor":57,"adjHit":75,"adjDodge":2,"adjRealDmg":8,"adjRealDmgDef":6,"adjDebilityEnh":8,"adjDebilityAnti":13})
    }),
    51002059: _tools.RODict({
        "propID": 51002059,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":22576,"adjMinPhysicalAtk":230,"adjMaxPhysicalAtk":306,"adjMinMagicAtk":230,"adjMaxMagicAtk":306,"adjMinPhysicalArmor":58,"adjMaxPhysicalArmor":58,"adjMinMagicArmor":58,"adjMaxMagicArmor":58,"adjHit":75,"adjDodge":2,"adjRealDmg":8,"adjRealDmgDef":8,"adjDebilityEnh":9,"adjDebilityAnti":13})
    }),
    51002060: _tools.RODict({
        "propID": 51002060,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":23210,"adjMinPhysicalAtk":233,"adjMaxPhysicalAtk":310,"adjMinMagicAtk":233,"adjMaxMagicAtk":310,"adjMinPhysicalArmor":59,"adjMaxPhysicalArmor":59,"adjMinMagicArmor":59,"adjMaxMagicArmor":59,"adjHit":78,"adjDodge":2,"adjRealDmg":8,"adjRealDmgDef":8,"adjDebilityEnh":9,"adjDebilityAnti":13})
    }),
    51002061: _tools.RODict({
        "propID": 51002061,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":25814,"adjMinPhysicalAtk":234,"adjMaxPhysicalAtk":312,"adjMinMagicAtk":234,"adjMaxMagicAtk":312,"adjMinPhysicalArmor":66,"adjMaxPhysicalArmor":66,"adjMinMagicArmor":66,"adjMaxMagicArmor":66,"adjHit":78,"adjDodge":2,"adjRealDmg":8,"adjRealDmgDef":8,"adjDebilityEnh":9,"adjDebilityAnti":13})
    }),
    51002062: _tools.RODict({
        "propID": 51002062,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":26403,"adjMinPhysicalAtk":248,"adjMaxPhysicalAtk":330,"adjMinMagicAtk":248,"adjMaxMagicAtk":330,"adjMinPhysicalArmor":68,"adjMaxPhysicalArmor":68,"adjMinMagicArmor":68,"adjMaxMagicArmor":68,"adjHit":78,"adjDodge":2,"adjRealDmg":8,"adjRealDmgDef":8,"adjDebilityEnh":9,"adjDebilityAnti":13})
    }),
    51002063: _tools.RODict({
        "propID": 51002063,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":26471,"adjMinPhysicalAtk":276,"adjMaxPhysicalAtk":368,"adjMinMagicAtk":276,"adjMaxMagicAtk":368,"adjMinPhysicalArmor":68,"adjMaxPhysicalArmor":68,"adjMinMagicArmor":68,"adjMaxMagicArmor":68,"adjHit":84,"adjDodge":2,"adjRealDmg":10,"adjRealDmgDef":8,"adjDebilityEnh":9,"adjDebilityAnti":15})
    }),
    51002064: _tools.RODict({
        "propID": 51002064,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":27580,"adjMinPhysicalAtk":282,"adjMaxPhysicalAtk":376,"adjMinMagicAtk":282,"adjMaxMagicAtk":376,"adjMinPhysicalArmor":69,"adjMaxPhysicalArmor":69,"adjMinMagicArmor":69,"adjMaxMagicArmor":69,"adjHit":84,"adjDodge":2,"adjRealDmg":10,"adjRealDmgDef":10,"adjDebilityEnh":11,"adjDebilityAnti":15})
    }),
    51002065: _tools.RODict({
        "propID": 51002065,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":28757,"adjMinPhysicalAtk":286,"adjMaxPhysicalAtk":381,"adjMinMagicAtk":286,"adjMaxMagicAtk":381,"adjMinPhysicalArmor":70,"adjMaxPhysicalArmor":70,"adjMinMagicArmor":70,"adjMaxMagicArmor":70,"adjHit":88,"adjDodge":2,"adjRealDmg":10,"adjRealDmgDef":10,"adjDebilityEnh":11,"adjDebilityAnti":15})
    }),
    51002066: _tools.RODict({
        "propID": 51002066,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":30795,"adjMinPhysicalAtk":287,"adjMaxPhysicalAtk":382,"adjMinMagicAtk":287,"adjMaxMagicAtk":382,"adjMinPhysicalArmor":76,"adjMaxPhysicalArmor":76,"adjMinMagicArmor":76,"adjMaxMagicArmor":76,"adjHit":88,"adjDodge":2,"adjRealDmg":10,"adjRealDmgDef":10,"adjDebilityEnh":11,"adjDebilityAnti":15})
    }),
    51002067: _tools.RODict({
        "propID": 51002067,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":31520,"adjMinPhysicalAtk":296,"adjMaxPhysicalAtk":395,"adjMinMagicAtk":296,"adjMaxMagicAtk":395,"adjMinPhysicalArmor":78,"adjMaxPhysicalArmor":78,"adjMinMagicArmor":78,"adjMaxMagicArmor":78,"adjHit":88,"adjDodge":2,"adjRealDmg":10,"adjRealDmgDef":10,"adjDebilityEnh":11,"adjDebilityAnti":15})
    }),
    51002068: _tools.RODict({
        "propID": 51002068,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":31475,"adjMinPhysicalAtk":314,"adjMaxPhysicalAtk":419,"adjMinMagicAtk":314,"adjMaxMagicAtk":419,"adjMinPhysicalArmor":79,"adjMaxPhysicalArmor":79,"adjMinMagicArmor":79,"adjMaxMagicArmor":79,"adjHit":90,"adjDodge":2,"adjRealDmg":13,"adjRealDmgDef":10,"adjDebilityEnh":11,"adjDebilityAnti":16})
    }),
    51002069: _tools.RODict({
        "propID": 51002069,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":32357,"adjMinPhysicalAtk":323,"adjMaxPhysicalAtk":430,"adjMinMagicAtk":323,"adjMaxMagicAtk":430,"adjMinPhysicalArmor":79,"adjMaxPhysicalArmor":79,"adjMinMagicArmor":79,"adjMaxMagicArmor":79,"adjHit":90,"adjDodge":2,"adjRealDmg":13,"adjRealDmgDef":13,"adjDebilityEnh":12,"adjDebilityAnti":16})
    }),
    51002070: _tools.RODict({
        "propID": 51002070,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":33127,"adjMinPhysicalAtk":327,"adjMaxPhysicalAtk":436,"adjMinMagicAtk":327,"adjMaxMagicAtk":436,"adjMinPhysicalArmor":80,"adjMaxPhysicalArmor":80,"adjMinMagicArmor":80,"adjMaxMagicArmor":80,"adjHit":94,"adjDodge":2,"adjRealDmg":13,"adjRealDmgDef":13,"adjDebilityEnh":12,"adjDebilityAnti":16})
    }),
    51003001: _tools.RODict({
        "propID": 51003001,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4907,"adjMinPhysicalAtk":27,"adjMaxPhysicalAtk":28,"adjMinMagicAtk":27,"adjMaxMagicAtk":28,"adjMinPhysicalArmor":2,"adjMaxPhysicalArmor":2,"adjMinMagicArmor":2,"adjMaxMagicArmor":2,"adjHit":76,"adjDodge":3,"adjRealDmg":1,"adjRealDmgDef":2,"adjDebilityAnti":6})
    }),
    51003002: _tools.RODict({
        "propID": 51003002,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":23418,"adjMinPhysicalAtk":28,"adjMaxPhysicalAtk":29,"adjMinMagicAtk":28,"adjMaxMagicAtk":29,"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjHit":76,"adjDodge":3,"adjRealDmg":1,"adjRealDmgDef":2,"adjDebilityAnti":6})
    }),
    51003003: _tools.RODict({
        "propID": 51003003,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":23983,"adjMinPhysicalAtk":29,"adjMaxPhysicalAtk":31,"adjMinMagicAtk":29,"adjMaxMagicAtk":31,"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjHit":76,"adjDodge":3,"adjRealDmg":1,"adjRealDmgDef":2,"adjDebilityAnti":6})
    }),
    51003004: _tools.RODict({
        "propID": 51003004,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":24733,"adjMinPhysicalAtk":40,"adjMaxPhysicalAtk":42,"adjMinMagicAtk":40,"adjMaxMagicAtk":42,"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjHit":76,"adjDodge":3,"adjRealDmg":1,"adjRealDmgDef":2,"adjDebilityAnti":6})
    }),
    51003005: _tools.RODict({
        "propID": 51003005,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":25299,"adjMinPhysicalAtk":42,"adjMaxPhysicalAtk":44,"adjMinMagicAtk":42,"adjMaxMagicAtk":44,"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjHit":76,"adjDodge":3,"adjRealDmg":1,"adjRealDmgDef":2,"adjDebilityAnti":6})
    }),
    51003006: _tools.RODict({
        "propID": 51003006,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":24549,"adjMinPhysicalAtk":54,"adjMaxPhysicalAtk":57,"adjMinMagicAtk":54,"adjMaxMagicAtk":57,"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10,"adjHit":76,"adjDodge":3,"adjRealDmg":1,"adjRealDmgDef":2,"adjDebilityAnti":6})
    }),
    51003007: _tools.RODict({
        "propID": 51003007,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":25865,"adjMinPhysicalAtk":56,"adjMaxPhysicalAtk":59,"adjMinMagicAtk":56,"adjMaxMagicAtk":59,"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10,"adjHit":76,"adjDodge":3,"adjRealDmg":1,"adjRealDmgDef":2,"adjDebilityAnti":6})
    }),
    51003008: _tools.RODict({
        "propID": 51003008,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":25865,"adjMinPhysicalAtk":67,"adjMaxPhysicalAtk":71,"adjMinMagicAtk":67,"adjMaxMagicAtk":71,"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10,"adjHit":80,"adjDodge":3,"adjRealDmg":1,"adjRealDmgDef":2,"adjDebilityAnti":6})
    }),
    51003009: _tools.RODict({
        "propID": 51003009,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":26431,"adjMinPhysicalAtk":70,"adjMaxPhysicalAtk":74,"adjMinMagicAtk":70,"adjMaxMagicAtk":74,"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10,"adjHit":80,"adjDodge":3,"adjRealDmg":1,"adjRealDmgDef":2,"adjDebilityAnti":6})
    }),
    51003010: _tools.RODict({
        "propID": 51003010,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":29075,"adjMinPhysicalAtk":71,"adjMaxPhysicalAtk":75,"adjMinMagicAtk":71,"adjMaxMagicAtk":75,"adjMinPhysicalArmor":12,"adjMaxPhysicalArmor":12,"adjMinMagicArmor":12,"adjMaxMagicArmor":12,"adjHit":80,"adjDodge":3,"adjRealDmg":1,"adjRealDmgDef":2,"adjDebilityAnti":6})
    }),
    51003011: _tools.RODict({
        "propID": 51003011,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":29907,"adjMinPhysicalAtk":75,"adjMaxPhysicalAtk":79,"adjMinMagicAtk":75,"adjMaxMagicAtk":79,"adjMinPhysicalArmor":12,"adjMaxPhysicalArmor":12,"adjMinMagicArmor":12,"adjMaxMagicArmor":12,"adjHit":80,"adjDodge":3,"adjRealDmg":1,"adjRealDmgDef":2,"adjDebilityAnti":6})
    }),
    51003012: _tools.RODict({
        "propID": 51003012,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":30923,"adjMinPhysicalAtk":79,"adjMaxPhysicalAtk":83,"adjMinMagicAtk":79,"adjMaxMagicAtk":83,"adjMinPhysicalArmor":12,"adjMaxPhysicalArmor":12,"adjMinMagicArmor":12,"adjMaxMagicArmor":12,"adjHit":80,"adjDodge":3,"adjRealDmg":1,"adjRealDmgDef":2,"adjDebilityAnti":6})
    }),
    51003013: _tools.RODict({
        "propID": 51003013,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":31773,"adjMinPhysicalAtk":82,"adjMaxPhysicalAtk":86,"adjMinMagicAtk":82,"adjMaxMagicAtk":86,"adjMinPhysicalArmor":12,"adjMaxPhysicalArmor":12,"adjMinMagicArmor":12,"adjMaxMagicArmor":12,"adjHit":81,"adjDodge":3,"adjRealDmg":1,"adjRealDmgDef":2,"adjDebilityAnti":6})
    }),
    51003014: _tools.RODict({
        "propID": 51003014,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":32015,"adjMinPhysicalAtk":84,"adjMaxPhysicalAtk":88,"adjMinMagicAtk":84,"adjMaxMagicAtk":88,"adjMinPhysicalArmor":13,"adjMaxPhysicalArmor":13,"adjMinMagicArmor":13,"adjMaxMagicArmor":13,"adjHit":81,"adjDodge":3,"adjRealDmg":1,"adjRealDmgDef":2,"adjDebilityAnti":6})
    }),
    51003015: _tools.RODict({
        "propID": 51003015,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":38813,"adjMinPhysicalAtk":86,"adjMaxPhysicalAtk":90,"adjMinMagicAtk":86,"adjMaxMagicAtk":90,"adjMinPhysicalArmor":13,"adjMaxPhysicalArmor":13,"adjMinMagicArmor":13,"adjMaxMagicArmor":13,"adjHit":81,"adjDodge":3,"adjRealDmg":1,"adjRealDmgDef":2,"adjDebilityAnti":6})
    }),
    51003016: _tools.RODict({
        "propID": 51003016,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":39095,"adjMinPhysicalAtk":89,"adjMaxPhysicalAtk":94,"adjMinMagicAtk":89,"adjMaxMagicAtk":94,"adjMinPhysicalArmor":14,"adjMaxPhysicalArmor":14,"adjMinMagicArmor":14,"adjMaxMagicArmor":14,"adjHit":81,"adjDodge":3,"adjRealDmg":1,"adjRealDmgDef":2,"adjDebilityAnti":6})
    }),
    51003017: _tools.RODict({
        "propID": 51003017,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":40020,"adjMinPhysicalAtk":94,"adjMaxPhysicalAtk":99,"adjMinMagicAtk":94,"adjMaxMagicAtk":99,"adjMinPhysicalArmor":14,"adjMaxPhysicalArmor":14,"adjMinMagicArmor":14,"adjMaxMagicArmor":14,"adjHit":81,"adjDodge":3,"adjRealDmg":1,"adjRealDmgDef":2,"adjDebilityAnti":6})
    }),
    51003018: _tools.RODict({
        "propID": 51003018,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":41095,"adjMinPhysicalAtk":96,"adjMaxPhysicalAtk":101,"adjMinMagicAtk":96,"adjMaxMagicAtk":101,"adjMinPhysicalArmor":14,"adjMaxPhysicalArmor":14,"adjMinMagicArmor":14,"adjMaxMagicArmor":14,"adjHit":82,"adjDodge":3,"adjRealDmg":1,"adjRealDmgDef":2,"adjDebilityAnti":6})
    }),
    51003019: _tools.RODict({
        "propID": 51003019,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":42036,"adjMinPhysicalAtk":98,"adjMaxPhysicalAtk":103,"adjMinMagicAtk":98,"adjMaxMagicAtk":103,"adjMinPhysicalArmor":14,"adjMaxPhysicalArmor":14,"adjMinMagicArmor":14,"adjMaxMagicArmor":14,"adjHit":82,"adjDodge":3,"adjRealDmg":1,"adjRealDmgDef":2,"adjDebilityAnti":6})
    }),
    51003020: _tools.RODict({
        "propID": 51003020,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":46026,"adjMinPhysicalAtk":100,"adjMaxPhysicalAtk":105,"adjMinMagicAtk":100,"adjMaxMagicAtk":105,"adjMinPhysicalArmor":15,"adjMaxPhysicalArmor":15,"adjMinMagicArmor":15,"adjMaxMagicArmor":15,"adjHit":82,"adjDodge":3,"adjRealDmg":1,"adjRealDmgDef":2,"adjDebilityAnti":6})
    }),
    51003021: _tools.RODict({
        "propID": 51003021,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":47556,"adjMinPhysicalAtk":112,"adjMaxPhysicalAtk":118,"adjMinMagicAtk":112,"adjMaxMagicAtk":118,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjHit":82,"adjDodge":3,"adjRealDmg":1,"adjRealDmgDef":2,"adjDebilityAnti":7})
    }),
    51003022: _tools.RODict({
        "propID": 51003022,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":48667,"adjMinPhysicalAtk":117,"adjMaxPhysicalAtk":123,"adjMinMagicAtk":117,"adjMaxMagicAtk":123,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjHit":86,"adjDodge":3,"adjRealDmg":1,"adjRealDmgDef":2,"adjDebilityAnti":7})
    }),
    51003023: _tools.RODict({
        "propID": 51003023,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":52127,"adjMinPhysicalAtk":120,"adjMaxPhysicalAtk":126,"adjMinMagicAtk":120,"adjMaxMagicAtk":126,"adjMinPhysicalArmor":17,"adjMaxPhysicalArmor":17,"adjMinMagicArmor":17,"adjMaxMagicArmor":17,"adjHit":86,"adjDodge":3,"adjRealDmg":1,"adjRealDmgDef":2,"adjDebilityAnti":7})
    }),
    51003024: _tools.RODict({
        "propID": 51003024,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":54983,"adjMinPhysicalAtk":122,"adjMaxPhysicalAtk":128,"adjMinMagicAtk":122,"adjMaxMagicAtk":128,"adjMinPhysicalArmor":18,"adjMaxPhysicalArmor":18,"adjMinMagicArmor":18,"adjMaxMagicArmor":18,"adjHit":86,"adjDodge":3,"adjRealDmg":1,"adjRealDmgDef":2,"adjDebilityAnti":7})
    }),
    51003025: _tools.RODict({
        "propID": 51003025,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":64164,"adjMinPhysicalAtk":130,"adjMaxPhysicalAtk":137,"adjMinMagicAtk":130,"adjMaxMagicAtk":137,"adjMinPhysicalArmor":20,"adjMaxPhysicalArmor":20,"adjMinMagicArmor":20,"adjMaxMagicArmor":20,"adjHit":86,"adjDodge":3,"adjRealDmg":1,"adjRealDmgDef":2,"adjDebilityAnti":8})
    }),
    51003026: _tools.RODict({
        "propID": 51003026,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":65260,"adjMinPhysicalAtk":135,"adjMaxPhysicalAtk":142,"adjMinMagicAtk":135,"adjMaxMagicAtk":142,"adjMinPhysicalArmor":21,"adjMaxPhysicalArmor":21,"adjMinMagicArmor":21,"adjMaxMagicArmor":21,"adjHit":88,"adjDodge":3,"adjRealDmg":1,"adjRealDmgDef":2,"adjDebilityAnti":8})
    }),
    51003027: _tools.RODict({
        "propID": 51003027,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":67881,"adjMinPhysicalAtk":138,"adjMaxPhysicalAtk":145,"adjMinMagicAtk":138,"adjMaxMagicAtk":145,"adjMinPhysicalArmor":21,"adjMaxPhysicalArmor":21,"adjMinMagicArmor":21,"adjMaxMagicArmor":21,"adjHit":88,"adjDodge":3,"adjRealDmg":1,"adjRealDmgDef":2,"adjDebilityAnti":8})
    }),
    51003028: _tools.RODict({
        "propID": 51003028,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":71631,"adjMinPhysicalAtk":141,"adjMaxPhysicalAtk":148,"adjMinMagicAtk":141,"adjMaxMagicAtk":148,"adjMinPhysicalArmor":22,"adjMaxPhysicalArmor":22,"adjMinMagicArmor":22,"adjMaxMagicArmor":22,"adjHit":88,"adjDodge":3,"adjRealDmg":1,"adjRealDmgDef":2,"adjDebilityAnti":8})
    }),
    51003029: _tools.RODict({
        "propID": 51003029,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":82144,"adjMinPhysicalAtk":149,"adjMaxPhysicalAtk":157,"adjMinMagicAtk":149,"adjMaxMagicAtk":157,"adjMinPhysicalArmor":23,"adjMaxPhysicalArmor":23,"adjMinMagicArmor":23,"adjMaxMagicArmor":23,"adjHit":88,"adjDodge":3,"adjRealDmg":1,"adjRealDmgDef":2,"adjDebilityAnti":9})
    }),
    51003030: _tools.RODict({
        "propID": 51003030,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":83974,"adjMinPhysicalAtk":155,"adjMaxPhysicalAtk":163,"adjMinMagicAtk":155,"adjMaxMagicAtk":163,"adjMinPhysicalArmor":24,"adjMaxPhysicalArmor":24,"adjMinMagicArmor":24,"adjMaxMagicArmor":24,"adjHit":90,"adjDodge":3,"adjRealDmg":1,"adjRealDmgDef":2,"adjDebilityAnti":9})
    }),
    51003031: _tools.RODict({
        "propID": 51003031,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":89447,"adjMinPhysicalAtk":158,"adjMaxPhysicalAtk":166,"adjMinMagicAtk":158,"adjMaxMagicAtk":166,"adjMinPhysicalArmor":24,"adjMaxPhysicalArmor":24,"adjMinMagicArmor":24,"adjMaxMagicArmor":24,"adjHit":90,"adjDodge":3,"adjRealDmg":2,"adjRealDmgDef":2,"adjDebilityAnti":9})
    }),
    51003032: _tools.RODict({
        "propID": 51003032,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":94751,"adjMinPhysicalAtk":161,"adjMaxPhysicalAtk":169,"adjMinMagicAtk":161,"adjMaxMagicAtk":169,"adjMinPhysicalArmor":25,"adjMaxPhysicalArmor":25,"adjMinMagicArmor":25,"adjMaxMagicArmor":25,"adjHit":90,"adjDodge":3,"adjRealDmg":2,"adjRealDmgDef":3,"adjDebilityAnti":9})
    }),
    51003033: _tools.RODict({
        "propID": 51003033,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":104056,"adjMinPhysicalAtk":175,"adjMaxPhysicalAtk":184,"adjMinMagicAtk":175,"adjMaxMagicAtk":184,"adjMinPhysicalArmor":27,"adjMaxPhysicalArmor":27,"adjMinMagicArmor":27,"adjMaxMagicArmor":27,"adjHit":90,"adjDodge":3,"adjRealDmg":2,"adjRealDmgDef":3,"adjDebilityAnti":10})
    }),
    51003034: _tools.RODict({
        "propID": 51003034,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":106921,"adjMinPhysicalAtk":181,"adjMaxPhysicalAtk":191,"adjMinMagicAtk":181,"adjMaxMagicAtk":191,"adjMinPhysicalArmor":27,"adjMaxPhysicalArmor":27,"adjMinMagicArmor":27,"adjMaxMagicArmor":27,"adjHit":92,"adjDodge":3,"adjRealDmg":2,"adjRealDmgDef":3,"adjDebilityAnti":10})
    }),
    51003035: _tools.RODict({
        "propID": 51003035,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":110981,"adjMinPhysicalAtk":187,"adjMaxPhysicalAtk":197,"adjMinMagicAtk":187,"adjMaxMagicAtk":197,"adjMinPhysicalArmor":28,"adjMaxPhysicalArmor":28,"adjMinMagicArmor":28,"adjMaxMagicArmor":28,"adjHit":92,"adjDodge":3,"adjRealDmg":3,"adjRealDmgDef":3,"adjDebilityAnti":10})
    }),
    51003036: _tools.RODict({
        "propID": 51003036,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":114590,"adjMinPhysicalAtk":190,"adjMaxPhysicalAtk":200,"adjMinMagicAtk":190,"adjMaxMagicAtk":200,"adjMinPhysicalArmor":28,"adjMaxPhysicalArmor":28,"adjMinMagicArmor":28,"adjMaxMagicArmor":28,"adjHit":92,"adjDodge":3,"adjRealDmg":3,"adjRealDmgDef":4,"adjDebilityAnti":10})
    }),
    51003037: _tools.RODict({
        "propID": 51003037,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":123470,"adjMinPhysicalAtk":194,"adjMaxPhysicalAtk":204,"adjMinMagicAtk":194,"adjMaxMagicAtk":204,"adjMinPhysicalArmor":30,"adjMaxPhysicalArmor":30,"adjMinMagicArmor":30,"adjMaxMagicArmor":30,"adjHit":93,"adjDodge":3,"adjRealDmg":3,"adjRealDmgDef":4,"adjDebilityAnti":10})
    }),
    51003038: _tools.RODict({
        "propID": 51003038,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":124974,"adjMinPhysicalAtk":221,"adjMaxPhysicalAtk":233,"adjMinMagicAtk":221,"adjMaxMagicAtk":233,"adjMinPhysicalArmor":30,"adjMaxPhysicalArmor":30,"adjMinMagicArmor":30,"adjMaxMagicArmor":30,"adjHit":93,"adjDodge":3,"adjRealDmg":4,"adjRealDmgDef":4,"adjDebilityAnti":11})
    }),
    51003039: _tools.RODict({
        "propID": 51003039,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":128667,"adjMinPhysicalAtk":237,"adjMaxPhysicalAtk":249,"adjMinMagicAtk":237,"adjMaxMagicAtk":249,"adjMinPhysicalArmor":30,"adjMaxPhysicalArmor":30,"adjMinMagicArmor":30,"adjMaxMagicArmor":30,"adjHit":99,"adjDodge":3,"adjRealDmg":4,"adjRealDmgDef":5,"adjDebilityEnh":5,"adjDebilityAnti":11})
    }),
    51003040: _tools.RODict({
        "propID": 51003040,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":144418,"adjMinPhysicalAtk":241,"adjMaxPhysicalAtk":254,"adjMinMagicAtk":241,"adjMaxMagicAtk":254,"adjMinPhysicalArmor":32,"adjMaxPhysicalArmor":32,"adjMinMagicArmor":32,"adjMaxMagicArmor":32,"adjHit":99,"adjDodge":3,"adjRealDmg":4,"adjRealDmgDef":5,"adjDebilityEnh":5,"adjDebilityAnti":11})
    }),
    51003041: _tools.RODict({
        "propID": 51003041,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":163868,"adjMinPhysicalAtk":246,"adjMaxPhysicalAtk":259,"adjMinMagicAtk":246,"adjMaxMagicAtk":259,"adjMinPhysicalArmor":38,"adjMaxPhysicalArmor":38,"adjMinMagicArmor":38,"adjMaxMagicArmor":38,"adjHit":99,"adjDodge":3,"adjRealDmg":4,"adjRealDmgDef":5,"adjDebilityEnh":5,"adjDebilityAnti":11})
    }),
    51003042: _tools.RODict({
        "propID": 51003042,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":165634,"adjMinPhysicalAtk":261,"adjMaxPhysicalAtk":275,"adjMinMagicAtk":261,"adjMaxMagicAtk":275,"adjMinPhysicalArmor":38,"adjMaxPhysicalArmor":38,"adjMinMagicArmor":38,"adjMaxMagicArmor":38,"adjHit":99,"adjDodge":3,"adjRealDmg":5,"adjRealDmgDef":5,"adjDebilityEnh":5,"adjDebilityAnti":11})
    }),
    51003043: _tools.RODict({
        "propID": 51003043,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":168153,"adjMinPhysicalAtk":281,"adjMaxPhysicalAtk":296,"adjMinMagicAtk":281,"adjMaxMagicAtk":296,"adjMinPhysicalArmor":38,"adjMaxPhysicalArmor":38,"adjMinMagicArmor":38,"adjMaxMagicArmor":38,"adjHit":101,"adjDodge":3,"adjRealDmg":5,"adjRealDmgDef":6,"adjDebilityEnh":5,"adjDebilityAnti":12})
    }),
    51003044: _tools.RODict({
        "propID": 51003044,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":171952,"adjMinPhysicalAtk":287,"adjMaxPhysicalAtk":302,"adjMinMagicAtk":287,"adjMaxMagicAtk":302,"adjMinPhysicalArmor":39,"adjMaxPhysicalArmor":39,"adjMinMagicArmor":39,"adjMaxMagicArmor":39,"adjHit":102,"adjDodge":3,"adjRealDmg":5,"adjRealDmgDef":6,"adjDebilityEnh":6,"adjDebilityAnti":12})
    }),
    51003045: _tools.RODict({
        "propID": 51003045,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":177557,"adjMinPhysicalAtk":295,"adjMaxPhysicalAtk":310,"adjMinMagicAtk":295,"adjMaxMagicAtk":310,"adjMinPhysicalArmor":39,"adjMaxPhysicalArmor":39,"adjMinMagicArmor":39,"adjMaxMagicArmor":39,"adjHit":102,"adjDodge":3,"adjRealDmg":5,"adjRealDmgDef":6,"adjDebilityEnh":6,"adjDebilityAnti":12})
    }),
    51003046: _tools.RODict({
        "propID": 51003046,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":194009,"adjMinPhysicalAtk":304,"adjMaxPhysicalAtk":320,"adjMinMagicAtk":304,"adjMaxMagicAtk":320,"adjMinPhysicalArmor":42,"adjMaxPhysicalArmor":42,"adjMinMagicArmor":42,"adjMaxMagicArmor":42,"adjHit":102,"adjDodge":3,"adjRealDmg":5,"adjRealDmgDef":6,"adjDebilityEnh":6,"adjDebilityAnti":12})
    }),
    51003047: _tools.RODict({
        "propID": 51003047,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":196706,"adjMinPhysicalAtk":318,"adjMaxPhysicalAtk":335,"adjMinMagicAtk":318,"adjMaxMagicAtk":335,"adjMinPhysicalArmor":42,"adjMaxPhysicalArmor":42,"adjMinMagicArmor":42,"adjMaxMagicArmor":42,"adjHit":102,"adjDodge":3,"adjRealDmg":6,"adjRealDmgDef":6,"adjDebilityEnh":6,"adjDebilityAnti":12})
    }),
    51003048: _tools.RODict({
        "propID": 51003048,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":197600,"adjMinPhysicalAtk":337,"adjMaxPhysicalAtk":355,"adjMinMagicAtk":337,"adjMaxMagicAtk":355,"adjMinPhysicalArmor":43,"adjMaxPhysicalArmor":43,"adjMinMagicArmor":43,"adjMaxMagicArmor":43,"adjHit":106,"adjDodge":3,"adjRealDmg":6,"adjRealDmgDef":7,"adjDebilityEnh":6,"adjDebilityAnti":13})
    }),
    51003049: _tools.RODict({
        "propID": 51003049,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":209487,"adjMinPhysicalAtk":352,"adjMaxPhysicalAtk":370,"adjMinMagicAtk":352,"adjMaxMagicAtk":370,"adjMinPhysicalArmor":44,"adjMaxPhysicalArmor":44,"adjMinMagicArmor":44,"adjMaxMagicArmor":44,"adjHit":106,"adjDodge":3,"adjRealDmg":6,"adjRealDmgDef":7,"adjDebilityEnh":7,"adjDebilityAnti":13})
    }),
    51003050: _tools.RODict({
        "propID": 51003050,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":215974,"adjMinPhysicalAtk":362,"adjMaxPhysicalAtk":381,"adjMinMagicAtk":362,"adjMaxMagicAtk":381,"adjMinPhysicalArmor":45,"adjMaxPhysicalArmor":45,"adjMinMagicArmor":45,"adjMaxMagicArmor":45,"adjHit":108,"adjDodge":3,"adjRealDmg":6,"adjRealDmgDef":7,"adjDebilityEnh":7,"adjDebilityAnti":13})
    }),
    51003051: _tools.RODict({
        "propID": 51003051,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":230520,"adjMinPhysicalAtk":369,"adjMaxPhysicalAtk":388,"adjMinMagicAtk":369,"adjMaxMagicAtk":388,"adjMinPhysicalArmor":49,"adjMaxPhysicalArmor":49,"adjMinMagicArmor":49,"adjMaxMagicArmor":49,"adjHit":108,"adjDodge":3,"adjRealDmg":6,"adjRealDmgDef":7,"adjDebilityEnh":7,"adjDebilityAnti":13})
    }),
    51003052: _tools.RODict({
        "propID": 51003052,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":237995,"adjMinPhysicalAtk":385,"adjMaxPhysicalAtk":405,"adjMinMagicAtk":385,"adjMaxMagicAtk":405,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":50,"adjMaxMagicArmor":50,"adjHit":108,"adjDodge":3,"adjRealDmg":7,"adjRealDmgDef":7,"adjDebilityEnh":7,"adjDebilityAnti":13})
    }),
    51003053: _tools.RODict({
        "propID": 51003053,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":240956,"adjMinPhysicalAtk":429,"adjMaxPhysicalAtk":452,"adjMinMagicAtk":429,"adjMaxMagicAtk":452,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":50,"adjMaxMagicArmor":50,"adjHit":110,"adjDodge":3,"adjRealDmg":7,"adjRealDmgDef":8,"adjDebilityEnh":7,"adjDebilityAnti":14})
    }),
    51003054: _tools.RODict({
        "propID": 51003054,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":246106,"adjMinPhysicalAtk":441,"adjMaxPhysicalAtk":464,"adjMinMagicAtk":441,"adjMaxMagicAtk":464,"adjMinPhysicalArmor":51,"adjMaxPhysicalArmor":51,"adjMinMagicArmor":51,"adjMaxMagicArmor":51,"adjHit":110,"adjDodge":3,"adjRealDmg":7,"adjRealDmgDef":8,"adjDebilityEnh":8,"adjDebilityAnti":14})
    }),
    51003055: _tools.RODict({
        "propID": 51003055,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":252118,"adjMinPhysicalAtk":450,"adjMaxPhysicalAtk":474,"adjMinMagicAtk":450,"adjMaxMagicAtk":474,"adjMinPhysicalArmor":52,"adjMaxPhysicalArmor":52,"adjMinMagicArmor":52,"adjMaxMagicArmor":52,"adjHit":113,"adjDodge":3,"adjRealDmg":7,"adjRealDmgDef":8,"adjDebilityEnh":8,"adjDebilityAnti":14})
    }),
    51003056: _tools.RODict({
        "propID": 51003056,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":269765,"adjMinPhysicalAtk":458,"adjMaxPhysicalAtk":482,"adjMinMagicAtk":458,"adjMaxMagicAtk":482,"adjMinPhysicalArmor":56,"adjMaxPhysicalArmor":56,"adjMinMagicArmor":56,"adjMaxMagicArmor":56,"adjHit":113,"adjDodge":3,"adjRealDmg":7,"adjRealDmgDef":8,"adjDebilityEnh":8,"adjDebilityAnti":14})
    }),
    51003057: _tools.RODict({
        "propID": 51003057,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":279289,"adjMinPhysicalAtk":477,"adjMaxPhysicalAtk":502,"adjMinMagicAtk":477,"adjMaxMagicAtk":502,"adjMinPhysicalArmor":57,"adjMaxPhysicalArmor":57,"adjMinMagicArmor":57,"adjMaxMagicArmor":57,"adjHit":113,"adjDodge":3,"adjRealDmg":8,"adjRealDmgDef":8,"adjDebilityEnh":8,"adjDebilityAnti":14})
    }),
    51003058: _tools.RODict({
        "propID": 51003058,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":281648,"adjMinPhysicalAtk":528,"adjMaxPhysicalAtk":556,"adjMinMagicAtk":528,"adjMaxMagicAtk":556,"adjMinPhysicalArmor":57,"adjMaxPhysicalArmor":57,"adjMinMagicArmor":57,"adjMaxMagicArmor":57,"adjHit":115,"adjDodge":3,"adjRealDmg":8,"adjRealDmgDef":9,"adjDebilityEnh":8,"adjDebilityAnti":15})
    }),
    51003059: _tools.RODict({
        "propID": 51003059,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":292162,"adjMinPhysicalAtk":544,"adjMaxPhysicalAtk":573,"adjMinMagicAtk":544,"adjMaxMagicAtk":573,"adjMinPhysicalArmor":58,"adjMaxPhysicalArmor":58,"adjMinMagicArmor":58,"adjMaxMagicArmor":58,"adjHit":115,"adjDodge":3,"adjRealDmg":8,"adjRealDmgDef":9,"adjDebilityEnh":9,"adjDebilityAnti":15})
    }),
    51003060: _tools.RODict({
        "propID": 51003060,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":301937,"adjMinPhysicalAtk":556,"adjMaxPhysicalAtk":585,"adjMinMagicAtk":556,"adjMaxMagicAtk":585,"adjMinPhysicalArmor":59,"adjMaxPhysicalArmor":59,"adjMinMagicArmor":59,"adjMaxMagicArmor":59,"adjHit":118,"adjDodge":3,"adjRealDmg":8,"adjRealDmgDef":9,"adjDebilityEnh":9,"adjDebilityAnti":15})
    }),
    51003061: _tools.RODict({
        "propID": 51003061,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":333205,"adjMinPhysicalAtk":565,"adjMaxPhysicalAtk":595,"adjMinMagicAtk":565,"adjMaxMagicAtk":595,"adjMinPhysicalArmor":66,"adjMaxPhysicalArmor":66,"adjMinMagicArmor":66,"adjMaxMagicArmor":66,"adjHit":118,"adjDodge":3,"adjRealDmg":8,"adjRealDmgDef":9,"adjDebilityEnh":9,"adjDebilityAnti":15})
    }),
    51003062: _tools.RODict({
        "propID": 51003062,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":342177,"adjMinPhysicalAtk":602,"adjMaxPhysicalAtk":634,"adjMinMagicAtk":602,"adjMaxMagicAtk":634,"adjMinPhysicalArmor":68,"adjMaxPhysicalArmor":68,"adjMinMagicArmor":68,"adjMaxMagicArmor":68,"adjHit":118,"adjDodge":3,"adjRealDmg":10,"adjRealDmgDef":9,"adjDebilityEnh":9,"adjDebilityAnti":15})
    }),
    51003063: _tools.RODict({
        "propID": 51003063,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":345738,"adjMinPhysicalAtk":697,"adjMaxPhysicalAtk":734,"adjMinMagicAtk":697,"adjMaxMagicAtk":734,"adjMinPhysicalArmor":68,"adjMaxPhysicalArmor":68,"adjMinMagicArmor":68,"adjMaxMagicArmor":68,"adjHit":124,"adjDodge":3,"adjRealDmg":10,"adjRealDmgDef":11,"adjDebilityEnh":9,"adjDebilityAnti":17})
    }),
    51003064: _tools.RODict({
        "propID": 51003064,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":362095,"adjMinPhysicalAtk":714,"adjMaxPhysicalAtk":752,"adjMinMagicAtk":714,"adjMaxMagicAtk":752,"adjMinPhysicalArmor":69,"adjMaxPhysicalArmor":69,"adjMinMagicArmor":69,"adjMaxMagicArmor":69,"adjHit":124,"adjDodge":3,"adjRealDmg":10,"adjRealDmgDef":11,"adjDebilityEnh":11,"adjDebilityAnti":17})
    }),
    51003065: _tools.RODict({
        "propID": 51003065,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":379506,"adjMinPhysicalAtk":731,"adjMaxPhysicalAtk":769,"adjMinMagicAtk":731,"adjMaxMagicAtk":769,"adjMinPhysicalArmor":70,"adjMaxPhysicalArmor":70,"adjMinMagicArmor":70,"adjMaxMagicArmor":70,"adjHit":128,"adjDodge":3,"adjRealDmg":10,"adjRealDmgDef":11,"adjDebilityEnh":11,"adjDebilityAnti":17})
    }),
    51003066: _tools.RODict({
        "propID": 51003066,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":405376,"adjMinPhysicalAtk":743,"adjMaxPhysicalAtk":782,"adjMinMagicAtk":743,"adjMaxMagicAtk":782,"adjMinPhysicalArmor":76,"adjMaxPhysicalArmor":76,"adjMinMagicArmor":76,"adjMaxMagicArmor":76,"adjHit":128,"adjDodge":3,"adjRealDmg":10,"adjRealDmgDef":11,"adjDebilityEnh":11,"adjDebilityAnti":17})
    }),
    51003067: _tools.RODict({
        "propID": 51003067,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":416710,"adjMinPhysicalAtk":773,"adjMaxPhysicalAtk":814,"adjMinMagicAtk":773,"adjMaxMagicAtk":814,"adjMinPhysicalArmor":78,"adjMaxPhysicalArmor":78,"adjMinMagicArmor":78,"adjMaxMagicArmor":78,"adjHit":128,"adjDodge":3,"adjRealDmg":12,"adjRealDmgDef":11,"adjDebilityEnh":11,"adjDebilityAnti":17})
    }),
    51003068: _tools.RODict({
        "propID": 51003068,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":418609,"adjMinPhysicalAtk":845,"adjMaxPhysicalAtk":889,"adjMinMagicAtk":845,"adjMaxMagicAtk":889,"adjMinPhysicalArmor":79,"adjMaxPhysicalArmor":79,"adjMinMagicArmor":79,"adjMaxMagicArmor":79,"adjHit":130,"adjDodge":3,"adjRealDmg":12,"adjRealDmgDef":13,"adjDebilityEnh":11,"adjDebilityAnti":18})
    }),
    51003069: _tools.RODict({
        "propID": 51003069,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":433379,"adjMinPhysicalAtk":868,"adjMaxPhysicalAtk":914,"adjMinMagicAtk":868,"adjMaxMagicAtk":914,"adjMinPhysicalArmor":79,"adjMaxPhysicalArmor":79,"adjMinMagicArmor":79,"adjMaxMagicArmor":79,"adjHit":130,"adjDodge":3,"adjRealDmg":12,"adjRealDmgDef":13,"adjDebilityEnh":12,"adjDebilityAnti":18})
    }),
    51003070: _tools.RODict({
        "propID": 51003070,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":446192,"adjMinPhysicalAtk":890,"adjMaxPhysicalAtk":937,"adjMinMagicAtk":890,"adjMaxMagicAtk":937,"adjMinPhysicalArmor":80,"adjMaxPhysicalArmor":80,"adjMinMagicArmor":80,"adjMaxMagicArmor":80,"adjHit":134,"adjDodge":3,"adjRealDmg":12,"adjRealDmgDef":13,"adjDebilityEnh":12,"adjDebilityAnti":18})
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
        "propList": _tools.RODict({"adjDebilityEnh":4})
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
        "propList": _tools.RODict({"adjDebilityEnh":7})
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
        "propList": _tools.RODict({"adjDebilityEnh":9})
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
        "propList": _tools.RODict({"adjDebilityAnti":5})
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
        "propList": _tools.RODict({"adjDebilityAnti":10})
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
        "propList": _tools.RODict({"adjDebilityAnti":15})
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
        "propList": _tools.RODict({"adjDropRate":0.01})
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
        "propList": _tools.RODict({"adjGatherRate":0.01})
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
        "propList": _tools.RODict({"adjDropRate":0.01})
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
        "propList": _tools.RODict({"adjGatherRate":0.01})
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
        "propList": _tools.RODict({"adjDropRate":0.01})
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
        "propList": _tools.RODict({"adjGatherRate":0.01})
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
        "propList": _tools.RODict({"adjDropRate":0.01})
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
        "propList": _tools.RODict({"adjGatherRate":0.01})
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
        "propList": _tools.RODict({"adjDropRate":0.01})
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
        "propList": _tools.RODict({"adjGatherRate":0.01})
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
        "propList": _tools.RODict({"adjDebilityEnh":5})
    }),
    52003221: _tools.RODict({
        "propID": 52003221,
        "type": 2,
        "propList": _tools.RODict({"adjDebilityEnh":8})
    }),
    52003222: _tools.RODict({
        "propID": 52003222,
        "type": 2,
        "propList": _tools.RODict({"adjDebilityEnh":11})
    }),
    52003223: _tools.RODict({
        "propID": 52003223,
        "type": 2,
        "propList": _tools.RODict({"adjDebilityEnh":14})
    }),
    52003224: _tools.RODict({
        "propID": 52003224,
        "type": 2,
        "propList": _tools.RODict({"adjDebilityAnti":5})
    }),
    52003225: _tools.RODict({
        "propID": 52003225,
        "type": 2,
        "propList": _tools.RODict({"adjDebilityAnti":8})
    }),
    52003226: _tools.RODict({
        "propID": 52003226,
        "type": 2,
        "propList": _tools.RODict({"adjDebilityAnti":11})
    }),
    52003227: _tools.RODict({
        "propID": 52003227,
        "type": 2,
        "propList": _tools.RODict({"adjDebilityAnti":14})
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
    52001260: _tools.RODict({
        "propID": 52001260,
        "type": 1,
        "propList": _tools.RODict({"adjMinPhysicalAtk":3,"adjMaxPhysicalAtk":6,"adjMinMagicAtk":3,"adjMaxMagicAtk":6})
    }),
    52001261: _tools.RODict({
        "propID": 52001261,
        "type": 1,
        "propList": _tools.RODict({"adjMinPhysicalAtk":1,"adjMaxPhysicalAtk":2,"adjMinMagicAtk":4,"adjMaxMagicAtk":8})
    }),
    52001262: _tools.RODict({
        "propID": 52001262,
        "type": 1,
        "propList": _tools.RODict({"adjMinPhysicalAtk":4,"adjMaxPhysicalAtk":8,"adjMinMagicAtk":1,"adjMaxMagicAtk":2})
    }),
    51009001: _tools.RODict({
        "propID": 51009001,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":200,"adjMinPhysicalAtk":2,"adjMaxPhysicalAtk":3,"adjMinMagicAtk":2,"adjMaxMagicAtk":3,"adjMinPhysicalArmor":1,"adjMaxPhysicalArmor":1,"adjMinMagicArmor":1,"adjMaxMagicArmor":1,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009002: _tools.RODict({
        "propID": 51009002,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":210,"adjMinPhysicalAtk":8,"adjMaxPhysicalAtk":13,"adjMinMagicAtk":8,"adjMaxMagicAtk":13,"adjMinPhysicalArmor":1,"adjMaxPhysicalArmor":1,"adjMinMagicArmor":1,"adjMaxMagicArmor":1,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009003: _tools.RODict({
        "propID": 51009003,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":220,"adjMinPhysicalAtk":8,"adjMaxPhysicalAtk":13,"adjMinMagicAtk":8,"adjMaxMagicAtk":13,"adjMinPhysicalArmor":1,"adjMaxPhysicalArmor":1,"adjMinMagicArmor":1,"adjMaxMagicArmor":1,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009004: _tools.RODict({
        "propID": 51009004,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":278,"adjMinPhysicalAtk":8,"adjMaxPhysicalAtk":13,"adjMinMagicAtk":8,"adjMaxMagicAtk":13,"adjMinPhysicalArmor":3,"adjMaxPhysicalArmor":3,"adjMinMagicArmor":3,"adjMaxMagicArmor":3,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009005: _tools.RODict({
        "propID": 51009005,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":288,"adjMinPhysicalAtk":8,"adjMaxPhysicalAtk":14,"adjMinMagicAtk":8,"adjMaxMagicAtk":14,"adjMinPhysicalArmor":3,"adjMaxPhysicalArmor":3,"adjMinMagicArmor":3,"adjMaxMagicArmor":3,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009006: _tools.RODict({
        "propID": 51009006,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":378,"adjMinPhysicalAtk":8,"adjMaxPhysicalAtk":14,"adjMinMagicAtk":8,"adjMaxMagicAtk":14,"adjMinPhysicalArmor":4,"adjMaxPhysicalArmor":4,"adjMinMagicArmor":4,"adjMaxMagicArmor":4,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009007: _tools.RODict({
        "propID": 51009007,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":388,"adjMinPhysicalAtk":8,"adjMaxPhysicalAtk":14,"adjMinMagicAtk":8,"adjMaxMagicAtk":14,"adjMinPhysicalArmor":4,"adjMaxPhysicalArmor":4,"adjMinMagicArmor":4,"adjMaxMagicArmor":4,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009008: _tools.RODict({
        "propID": 51009008,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":478,"adjMinPhysicalAtk":8,"adjMaxPhysicalAtk":14,"adjMinMagicAtk":8,"adjMaxMagicAtk":14,"adjMinPhysicalArmor":4,"adjMaxPhysicalArmor":4,"adjMinMagicArmor":4,"adjMaxMagicArmor":4,"adjHit":5,"adjDodge":4,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009009: _tools.RODict({
        "propID": 51009009,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":488,"adjMinPhysicalAtk":8,"adjMaxPhysicalAtk":14,"adjMinMagicAtk":8,"adjMaxMagicAtk":14,"adjMinPhysicalArmor":5,"adjMaxPhysicalArmor":5,"adjMinMagicArmor":5,"adjMaxMagicArmor":5,"adjHit":5,"adjDodge":4,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009010: _tools.RODict({
        "propID": 51009010,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":498,"adjMinPhysicalAtk":10,"adjMaxPhysicalAtk":16,"adjMinMagicAtk":10,"adjMaxMagicAtk":16,"adjMinPhysicalArmor":5,"adjMaxPhysicalArmor":5,"adjMinMagicArmor":5,"adjMaxMagicArmor":5,"adjHit":7,"adjDodge":4,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009011: _tools.RODict({
        "propID": 51009011,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":516,"adjMinPhysicalAtk":10,"adjMaxPhysicalAtk":16,"adjMinMagicAtk":10,"adjMaxMagicAtk":16,"adjMinPhysicalArmor":6,"adjMaxPhysicalArmor":6,"adjMinMagicArmor":6,"adjMaxMagicArmor":6,"adjHit":7,"adjDodge":4,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009012: _tools.RODict({
        "propID": 51009012,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":534,"adjMinPhysicalAtk":10,"adjMaxPhysicalAtk":16,"adjMinMagicAtk":10,"adjMaxMagicAtk":16,"adjMinPhysicalArmor":6,"adjMaxPhysicalArmor":6,"adjMinMagicArmor":6,"adjMaxMagicArmor":6,"adjHit":7,"adjDodge":4,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009013: _tools.RODict({
        "propID": 51009013,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":552,"adjMinPhysicalAtk":10,"adjMaxPhysicalAtk":16,"adjMinMagicAtk":10,"adjMaxMagicAtk":16,"adjMinPhysicalArmor":7,"adjMaxPhysicalArmor":7,"adjMinMagicArmor":7,"adjMaxMagicArmor":7,"adjHit":7,"adjDodge":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009014: _tools.RODict({
        "propID": 51009014,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":562,"adjMinPhysicalAtk":11,"adjMaxPhysicalAtk":16,"adjMinMagicAtk":11,"adjMaxMagicAtk":16,"adjMinPhysicalArmor":7,"adjMaxPhysicalArmor":7,"adjMinMagicArmor":7,"adjMaxMagicArmor":7,"adjHit":7,"adjDodge":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009015: _tools.RODict({
        "propID": 51009015,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":572,"adjMinPhysicalAtk":11,"adjMaxPhysicalAtk":19,"adjMinMagicAtk":11,"adjMaxMagicAtk":19,"adjMinPhysicalArmor":7,"adjMaxPhysicalArmor":7,"adjMinMagicArmor":7,"adjMaxMagicArmor":7,"adjHit":9,"adjDodge":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009016: _tools.RODict({
        "propID": 51009016,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":590,"adjMinPhysicalAtk":11,"adjMaxPhysicalAtk":19,"adjMinMagicAtk":11,"adjMaxMagicAtk":19,"adjMinPhysicalArmor":8,"adjMaxPhysicalArmor":8,"adjMinMagicArmor":8,"adjMaxMagicArmor":8,"adjHit":9,"adjDodge":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009017: _tools.RODict({
        "propID": 51009017,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":608,"adjMinPhysicalAtk":11,"adjMaxPhysicalAtk":19,"adjMinMagicAtk":11,"adjMaxMagicAtk":19,"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjHit":9,"adjDodge":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009018: _tools.RODict({
        "propID": 51009018,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":626,"adjMinPhysicalAtk":12,"adjMaxPhysicalAtk":19,"adjMinMagicAtk":12,"adjMaxMagicAtk":19,"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjHit":9,"adjDodge":6,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009019: _tools.RODict({
        "propID": 51009019,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":636,"adjMinPhysicalAtk":12,"adjMaxPhysicalAtk":19,"adjMinMagicAtk":12,"adjMaxMagicAtk":19,"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10,"adjHit":9,"adjDodge":6,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009020: _tools.RODict({
        "propID": 51009020,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":646,"adjMinPhysicalAtk":13,"adjMaxPhysicalAtk":21,"adjMinMagicAtk":13,"adjMaxMagicAtk":21,"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10,"adjHit":15,"adjDodge":6,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009021: _tools.RODict({
        "propID": 51009021,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":696,"adjMinPhysicalAtk":13,"adjMaxPhysicalAtk":21,"adjMinMagicAtk":13,"adjMaxMagicAtk":21,"adjMinPhysicalArmor":13,"adjMaxPhysicalArmor":13,"adjMinMagicArmor":13,"adjMaxMagicArmor":13,"adjHit":15,"adjDodge":6,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":7})
    }),
    51009022: _tools.RODict({
        "propID": 51009022,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":730,"adjMinPhysicalAtk":13,"adjMaxPhysicalAtk":21,"adjMinMagicAtk":13,"adjMaxMagicAtk":21,"adjMinPhysicalArmor":13,"adjMaxPhysicalArmor":13,"adjMinMagicArmor":13,"adjMaxMagicArmor":13,"adjHit":15,"adjDodge":10,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":7})
    }),
    51009023: _tools.RODict({
        "propID": 51009023,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":750,"adjMinPhysicalAtk":14,"adjMaxPhysicalAtk":23,"adjMinMagicAtk":14,"adjMaxMagicAtk":23,"adjMinPhysicalArmor":14,"adjMaxPhysicalArmor":14,"adjMinMagicArmor":14,"adjMaxMagicArmor":14,"adjHit":15,"adjDodge":10,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":7})
    }),
    51009024: _tools.RODict({
        "propID": 51009024,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":760,"adjMinPhysicalAtk":15,"adjMaxPhysicalAtk":24,"adjMinMagicAtk":15,"adjMaxMagicAtk":24,"adjMinPhysicalArmor":14,"adjMaxPhysicalArmor":14,"adjMinMagicArmor":14,"adjMaxMagicArmor":14,"adjHit":15,"adjDodge":10,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":7})
    }),
    51009025: _tools.RODict({
        "propID": 51009025,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":794,"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":27,"adjMinMagicAtk":17,"adjMaxMagicAtk":27,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjHit":18,"adjDodge":10,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":8})
    }),
    51009026: _tools.RODict({
        "propID": 51009026,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":820,"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":27,"adjMinMagicAtk":17,"adjMaxMagicAtk":27,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjHit":18,"adjDodge":12,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":8})
    }),
    51009027: _tools.RODict({
        "propID": 51009027,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":830,"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":28,"adjMinMagicAtk":17,"adjMaxMagicAtk":28,"adjMinPhysicalArmor":17,"adjMaxPhysicalArmor":17,"adjMinMagicArmor":17,"adjMaxMagicArmor":17,"adjHit":18,"adjDodge":12,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":8})
    }),
    51009028: _tools.RODict({
        "propID": 51009028,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":840,"adjMinPhysicalAtk":18,"adjMaxPhysicalAtk":29,"adjMinMagicAtk":18,"adjMaxMagicAtk":29,"adjMinPhysicalArmor":17,"adjMaxPhysicalArmor":17,"adjMinMagicArmor":17,"adjMaxMagicArmor":17,"adjHit":18,"adjDodge":12,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":8})
    }),
    51009029: _tools.RODict({
        "propID": 51009029,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":874,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":32,"adjMinMagicAtk":20,"adjMaxMagicAtk":32,"adjMinPhysicalArmor":18,"adjMaxPhysicalArmor":18,"adjMinMagicArmor":18,"adjMaxMagicArmor":18,"adjHit":21,"adjDodge":12,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":9})
    }),
    51009030: _tools.RODict({
        "propID": 51009030,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":900,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":32,"adjMinMagicAtk":20,"adjMaxMagicAtk":32,"adjMinPhysicalArmor":19,"adjMaxPhysicalArmor":19,"adjMinMagicArmor":19,"adjMaxMagicArmor":19,"adjHit":21,"adjDodge":14,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":9})
    }),
    51009031: _tools.RODict({
        "propID": 51009031,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":910,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":34,"adjMinMagicAtk":20,"adjMaxMagicAtk":34,"adjMinPhysicalArmor":19,"adjMaxPhysicalArmor":19,"adjMinMagicArmor":19,"adjMaxMagicArmor":19,"adjHit":21,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":9})
    }),
    51009032: _tools.RODict({
        "propID": 51009032,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":920,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":35,"adjMinMagicAtk":21,"adjMaxMagicAtk":35,"adjMinPhysicalArmor":19,"adjMaxPhysicalArmor":19,"adjMinMagicArmor":19,"adjMaxMagicArmor":19,"adjHit":22,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":3,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":9})
    }),
    51009033: _tools.RODict({
        "propID": 51009033,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":974,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":38,"adjMinMagicAtk":23,"adjMaxMagicAtk":38,"adjMinPhysicalArmor":22,"adjMaxPhysicalArmor":22,"adjMinMagicArmor":22,"adjMaxMagicArmor":22,"adjHit":25,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":3,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":10})
    }),
    51009034: _tools.RODict({
        "propID": 51009034,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1000,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":39,"adjMinMagicAtk":23,"adjMaxMagicAtk":39,"adjMinPhysicalArmor":23,"adjMaxPhysicalArmor":23,"adjMinMagicArmor":23,"adjMaxMagicArmor":23,"adjHit":25,"adjDodge":16,"adjRealDmg":2,"adjRealDmgDef":3,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":10})
    }),
    51009035: _tools.RODict({
        "propID": 51009035,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1010,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":40,"adjMinMagicAtk":23,"adjMaxMagicAtk":40,"adjMinPhysicalArmor":24,"adjMaxPhysicalArmor":24,"adjMinMagicArmor":24,"adjMaxMagicArmor":24,"adjHit":25,"adjDodge":16,"adjRealDmg":3,"adjRealDmgDef":3,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":10})
    }),
    51009036: _tools.RODict({
        "propID": 51009036,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1020,"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":40,"adjMinMagicAtk":24,"adjMaxMagicAtk":40,"adjMinPhysicalArmor":24,"adjMaxPhysicalArmor":24,"adjMinMagicArmor":24,"adjMaxMagicArmor":24,"adjHit":25,"adjDodge":16,"adjRealDmg":3,"adjRealDmgDef":4,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":10})
    }),
    51009037: _tools.RODict({
        "propID": 51009037,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1030,"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":43,"adjMinMagicAtk":25,"adjMaxMagicAtk":43,"adjMinPhysicalArmor":25,"adjMaxPhysicalArmor":25,"adjMinMagicArmor":25,"adjMaxMagicArmor":25,"adjHit":34,"adjDodge":17,"adjRealDmg":3,"adjRealDmgDef":4,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":10})
    }),
    51009038: _tools.RODict({
        "propID": 51009038,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1152,"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":43,"adjMinMagicAtk":25,"adjMaxMagicAtk":43,"adjMinPhysicalArmor":29,"adjMaxPhysicalArmor":29,"adjMinMagicArmor":29,"adjMaxMagicArmor":29,"adjHit":34,"adjDodge":17,"adjRealDmg":4,"adjRealDmgDef":4,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":11})
    }),
    51009039: _tools.RODict({
        "propID": 51009039,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1234,"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":44,"adjMinMagicAtk":25,"adjMaxMagicAtk":44,"adjMinPhysicalArmor":30,"adjMaxPhysicalArmor":30,"adjMinMagicArmor":30,"adjMaxMagicArmor":30,"adjHit":34,"adjDodge":23,"adjRealDmg":4,"adjRealDmgDef":5,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":5,"adjDebilityAnti":11})
    }),
    51009040: _tools.RODict({
        "propID": 51009040,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1244,"adjMinPhysicalAtk":27,"adjMaxPhysicalAtk":50,"adjMinMagicAtk":27,"adjMaxMagicAtk":50,"adjMinPhysicalArmor":30,"adjMaxPhysicalArmor":30,"adjMinMagicArmor":30,"adjMaxMagicArmor":30,"adjHit":34,"adjDodge":23,"adjRealDmg":4,"adjRealDmgDef":5,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":5,"adjDebilityAnti":11})
    }),
    51009041: _tools.RODict({
        "propID": 51009041,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1254,"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":58,"adjMinMagicAtk":32,"adjMaxMagicAtk":58,"adjMinPhysicalArmor":31,"adjMaxPhysicalArmor":31,"adjMinMagicArmor":31,"adjMaxMagicArmor":31,"adjHit":38,"adjDodge":23,"adjRealDmg":4,"adjRealDmgDef":5,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":5,"adjDebilityAnti":11})
    }),
    51009042: _tools.RODict({
        "propID": 51009042,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1318,"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":58,"adjMinMagicAtk":32,"adjMaxMagicAtk":58,"adjMinPhysicalArmor":32,"adjMaxPhysicalArmor":32,"adjMinMagicArmor":32,"adjMaxMagicArmor":32,"adjHit":38,"adjDodge":23,"adjRealDmg":5,"adjRealDmgDef":5,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":5,"adjDebilityAnti":11})
    }),
    51009043: _tools.RODict({
        "propID": 51009043,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1408,"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":58,"adjMinMagicAtk":32,"adjMaxMagicAtk":58,"adjMinPhysicalArmor":34,"adjMaxPhysicalArmor":34,"adjMinMagicArmor":34,"adjMaxMagicArmor":34,"adjHit":38,"adjDodge":25,"adjRealDmg":5,"adjRealDmgDef":6,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":5,"adjDebilityAnti":12})
    }),
    51009044: _tools.RODict({
        "propID": 51009044,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1418,"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":59,"adjMinMagicAtk":32,"adjMaxMagicAtk":59,"adjMinPhysicalArmor":35,"adjMaxPhysicalArmor":35,"adjMinMagicArmor":35,"adjMaxMagicArmor":35,"adjHit":38,"adjDodge":26,"adjRealDmg":5,"adjRealDmgDef":6,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":6,"adjDebilityAnti":12})
    }),
    51009045: _tools.RODict({
        "propID": 51009045,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1428,"adjMinPhysicalAtk":33,"adjMaxPhysicalAtk":60,"adjMinMagicAtk":33,"adjMaxMagicAtk":60,"adjMinPhysicalArmor":37,"adjMaxPhysicalArmor":37,"adjMinMagicArmor":37,"adjMaxMagicArmor":37,"adjHit":38,"adjDodge":26,"adjRealDmg":5,"adjRealDmgDef":6,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":6,"adjDebilityAnti":12})
    }),
    51009046: _tools.RODict({
        "propID": 51009046,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1473,"adjMinPhysicalAtk":35,"adjMaxPhysicalAtk":66,"adjMinMagicAtk":35,"adjMaxMagicAtk":66,"adjMinPhysicalArmor":37,"adjMaxPhysicalArmor":37,"adjMinMagicArmor":37,"adjMaxMagicArmor":37,"adjHit":43,"adjDodge":26,"adjRealDmg":5,"adjRealDmgDef":6,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":6,"adjDebilityAnti":12})
    }),
    51009047: _tools.RODict({
        "propID": 51009047,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1507,"adjMinPhysicalAtk":35,"adjMaxPhysicalAtk":66,"adjMinMagicAtk":35,"adjMaxMagicAtk":66,"adjMinPhysicalArmor":40,"adjMaxPhysicalArmor":40,"adjMinMagicArmor":40,"adjMaxMagicArmor":40,"adjHit":43,"adjDodge":26,"adjRealDmg":6,"adjRealDmgDef":6,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":6,"adjDebilityAnti":12})
    }),
    51009048: _tools.RODict({
        "propID": 51009048,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1597,"adjMinPhysicalAtk":36,"adjMaxPhysicalAtk":66,"adjMinMagicAtk":36,"adjMaxMagicAtk":66,"adjMinPhysicalArmor":40,"adjMaxPhysicalArmor":40,"adjMinMagicArmor":40,"adjMaxMagicArmor":40,"adjHit":43,"adjDodge":30,"adjRealDmg":6,"adjRealDmgDef":7,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":6,"adjDebilityAnti":13})
    }),
    51009049: _tools.RODict({
        "propID": 51009049,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1647,"adjMinPhysicalAtk":37,"adjMaxPhysicalAtk":70,"adjMinMagicAtk":37,"adjMaxMagicAtk":70,"adjMinPhysicalArmor":42,"adjMaxPhysicalArmor":42,"adjMinMagicArmor":42,"adjMaxMagicArmor":42,"adjHit":45,"adjDodge":30,"adjRealDmg":6,"adjRealDmgDef":7,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":7,"adjDebilityAnti":13})
    }),
    51009050: _tools.RODict({
        "propID": 51009050,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1657,"adjMinPhysicalAtk":38,"adjMaxPhysicalAtk":71,"adjMinMagicAtk":38,"adjMaxMagicAtk":71,"adjMinPhysicalArmor":44,"adjMaxPhysicalArmor":44,"adjMinMagicArmor":44,"adjMaxMagicArmor":44,"adjHit":45,"adjDodge":32,"adjRealDmg":6,"adjRealDmgDef":7,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":7,"adjDebilityAnti":13})
    }),
    51009051: _tools.RODict({
        "propID": 51009051,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1667,"adjMinPhysicalAtk":41,"adjMaxPhysicalAtk":77,"adjMinMagicAtk":41,"adjMaxMagicAtk":77,"adjMinPhysicalArmor":45,"adjMaxPhysicalArmor":45,"adjMinMagicArmor":45,"adjMaxMagicArmor":45,"adjHit":48,"adjDodge":32,"adjRealDmg":6,"adjRealDmgDef":7,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":7,"adjDebilityAnti":13})
    }),
    51009052: _tools.RODict({
        "propID": 51009052,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1725,"adjMinPhysicalAtk":42,"adjMaxPhysicalAtk":79,"adjMinMagicAtk":42,"adjMaxMagicAtk":79,"adjMinPhysicalArmor":46,"adjMaxPhysicalArmor":46,"adjMinMagicArmor":46,"adjMaxMagicArmor":46,"adjHit":51,"adjDodge":32,"adjRealDmg":7,"adjRealDmgDef":7,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":7,"adjDebilityAnti":13})
    }),
    51009053: _tools.RODict({
        "propID": 51009053,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1940,"adjMinPhysicalAtk":42,"adjMaxPhysicalAtk":79,"adjMinMagicAtk":42,"adjMaxMagicAtk":79,"adjMinPhysicalArmor":48,"adjMaxPhysicalArmor":48,"adjMinMagicArmor":48,"adjMaxMagicArmor":48,"adjHit":51,"adjDodge":34,"adjRealDmg":7,"adjRealDmgDef":8,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":7,"adjDebilityAnti":14})
    }),
    51009054: _tools.RODict({
        "propID": 51009054,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1950,"adjMinPhysicalAtk":43,"adjMaxPhysicalAtk":80,"adjMinMagicAtk":43,"adjMaxMagicAtk":80,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":50,"adjMaxMagicArmor":50,"adjHit":51,"adjDodge":34,"adjRealDmg":7,"adjRealDmgDef":8,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":8,"adjDebilityAnti":14})
    }),
    51009055: _tools.RODict({
        "propID": 51009055,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1960,"adjMinPhysicalAtk":43,"adjMaxPhysicalAtk":82,"adjMinMagicAtk":43,"adjMaxMagicAtk":82,"adjMinPhysicalArmor":52,"adjMaxPhysicalArmor":52,"adjMinMagicArmor":52,"adjMaxMagicArmor":52,"adjHit":51,"adjDodge":37,"adjRealDmg":7,"adjRealDmgDef":8,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":8,"adjDebilityAnti":14})
    }),
    51009056: _tools.RODict({
        "propID": 51009056,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1970,"adjMinPhysicalAtk":46,"adjMaxPhysicalAtk":88,"adjMinMagicAtk":46,"adjMaxMagicAtk":88,"adjMinPhysicalArmor":52,"adjMaxPhysicalArmor":52,"adjMinMagicArmor":52,"adjMaxMagicArmor":52,"adjHit":54,"adjDodge":37,"adjRealDmg":7,"adjRealDmgDef":8,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":8,"adjDebilityAnti":14})
    }),
    51009057: _tools.RODict({
        "propID": 51009057,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2028,"adjMinPhysicalAtk":48,"adjMaxPhysicalAtk":90,"adjMinMagicAtk":48,"adjMaxMagicAtk":90,"adjMinPhysicalArmor":54,"adjMaxPhysicalArmor":54,"adjMinMagicArmor":54,"adjMaxMagicArmor":54,"adjHit":57,"adjDodge":37,"adjRealDmg":8,"adjRealDmgDef":8,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":8,"adjDebilityAnti":14})
    }),
    51009058: _tools.RODict({
        "propID": 51009058,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2258,"adjMinPhysicalAtk":48,"adjMaxPhysicalAtk":90,"adjMinMagicAtk":48,"adjMaxMagicAtk":90,"adjMinPhysicalArmor":55,"adjMaxPhysicalArmor":55,"adjMinMagicArmor":55,"adjMaxMagicArmor":55,"adjHit":57,"adjDodge":39,"adjRealDmg":8,"adjRealDmgDef":9,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":8,"adjDebilityAnti":15})
    }),
    51009059: _tools.RODict({
        "propID": 51009059,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2268,"adjMinPhysicalAtk":48,"adjMaxPhysicalAtk":93,"adjMinMagicAtk":48,"adjMaxMagicAtk":93,"adjMinPhysicalArmor":59,"adjMaxPhysicalArmor":59,"adjMinMagicArmor":59,"adjMaxMagicArmor":59,"adjHit":57,"adjDodge":39,"adjRealDmg":8,"adjRealDmgDef":9,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":9,"adjDebilityAnti":15})
    }),
    51009060: _tools.RODict({
        "propID": 51009060,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2278,"adjMinPhysicalAtk":49,"adjMaxPhysicalAtk":95,"adjMinMagicAtk":49,"adjMaxMagicAtk":95,"adjMinPhysicalArmor":60,"adjMaxPhysicalArmor":60,"adjMinMagicArmor":60,"adjMaxMagicArmor":60,"adjHit":57,"adjDodge":42,"adjRealDmg":8,"adjRealDmgDef":9,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":9,"adjDebilityAnti":15})
    }),
    51009061: _tools.RODict({
        "propID": 51009061,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2288,"adjMinPhysicalAtk":55,"adjMaxPhysicalAtk":106,"adjMinMagicAtk":55,"adjMaxMagicAtk":106,"adjMinPhysicalArmor":61,"adjMaxPhysicalArmor":61,"adjMinMagicArmor":61,"adjMaxMagicArmor":61,"adjHit":66,"adjDodge":42,"adjRealDmg":8,"adjRealDmgDef":9,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":9,"adjDebilityAnti":15})
    }),
    51009062: _tools.RODict({
        "propID": 51009062,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2394,"adjMinPhysicalAtk":57,"adjMaxPhysicalAtk":109,"adjMinMagicAtk":57,"adjMaxMagicAtk":109,"adjMinPhysicalArmor":65,"adjMaxPhysicalArmor":65,"adjMinMagicArmor":65,"adjMaxMagicArmor":65,"adjHit":69,"adjDodge":42,"adjRealDmg":10,"adjRealDmgDef":9,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":9,"adjDebilityAnti":15})
    }),
    51009063: _tools.RODict({
        "propID": 51009063,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2799,"adjMinPhysicalAtk":57,"adjMaxPhysicalAtk":109,"adjMinMagicAtk":57,"adjMaxMagicAtk":109,"adjMinPhysicalArmor":68,"adjMaxPhysicalArmor":68,"adjMinMagicArmor":68,"adjMaxMagicArmor":68,"adjHit":69,"adjDodge":48,"adjRealDmg":10,"adjRealDmgDef":11,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":9,"adjDebilityAnti":17})
    }),
    51009064: _tools.RODict({
        "propID": 51009064,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2809,"adjMinPhysicalAtk":58,"adjMaxPhysicalAtk":113,"adjMinMagicAtk":58,"adjMaxMagicAtk":113,"adjMinPhysicalArmor":71,"adjMaxPhysicalArmor":71,"adjMinMagicArmor":71,"adjMaxMagicArmor":71,"adjHit":69,"adjDodge":48,"adjRealDmg":10,"adjRealDmgDef":11,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":11,"adjDebilityAnti":17})
    }),
    51009065: _tools.RODict({
        "propID": 51009065,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2819,"adjMinPhysicalAtk":59,"adjMaxPhysicalAtk":118,"adjMinMagicAtk":59,"adjMaxMagicAtk":118,"adjMinPhysicalArmor":73,"adjMaxPhysicalArmor":73,"adjMinMagicArmor":73,"adjMaxMagicArmor":73,"adjHit":69,"adjDodge":52,"adjRealDmg":10,"adjRealDmgDef":11,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":11,"adjDebilityAnti":17})
    }),
    51009066: _tools.RODict({
        "propID": 51009066,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2829,"adjMinPhysicalAtk":63,"adjMaxPhysicalAtk":126,"adjMinMagicAtk":63,"adjMaxMagicAtk":126,"adjMinPhysicalArmor":73,"adjMaxPhysicalArmor":73,"adjMinMagicArmor":73,"adjMaxMagicArmor":73,"adjHit":72,"adjDodge":52,"adjRealDmg":10,"adjRealDmgDef":11,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":11,"adjDebilityAnti":17})
    }),
    51009067: _tools.RODict({
        "propID": 51009067,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2887,"adjMinPhysicalAtk":65,"adjMaxPhysicalAtk":129,"adjMinMagicAtk":65,"adjMaxMagicAtk":129,"adjMinPhysicalArmor":77,"adjMaxPhysicalArmor":77,"adjMinMagicArmor":77,"adjMaxMagicArmor":77,"adjHit":75,"adjDodge":52,"adjRealDmg":12,"adjRealDmgDef":11,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":11,"adjDebilityAnti":17})
    }),
    51009068: _tools.RODict({
        "propID": 51009068,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3147,"adjMinPhysicalAtk":66,"adjMaxPhysicalAtk":129,"adjMinMagicAtk":66,"adjMaxMagicAtk":129,"adjMinPhysicalArmor":79,"adjMaxPhysicalArmor":79,"adjMinMagicArmor":79,"adjMaxMagicArmor":79,"adjHit":75,"adjDodge":54,"adjRealDmg":12,"adjRealDmgDef":13,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":11,"adjDebilityAnti":18})
    }),
    51009069: _tools.RODict({
        "propID": 51009069,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3157,"adjMinPhysicalAtk":66,"adjMaxPhysicalAtk":132,"adjMinMagicAtk":66,"adjMaxMagicAtk":132,"adjMinPhysicalArmor":84,"adjMaxPhysicalArmor":84,"adjMinMagicArmor":84,"adjMaxMagicArmor":84,"adjHit":75,"adjDodge":54,"adjRealDmg":12,"adjRealDmgDef":13,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":12,"adjDebilityAnti":18})
    }),
    51009070: _tools.RODict({
        "propID": 51009070,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3177,"adjMinPhysicalAtk":67,"adjMaxPhysicalAtk":135,"adjMinMagicAtk":67,"adjMaxMagicAtk":135,"adjMinPhysicalArmor":86,"adjMaxPhysicalArmor":86,"adjMinMagicArmor":86,"adjMaxMagicArmor":86,"adjHit":75,"adjDodge":58,"adjRealDmg":12,"adjRealDmgDef":13,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":12,"adjDebilityAnti":18})
    }),
    51009101: _tools.RODict({
        "propID": 51009101,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":100,"adjMinPhysicalAtk":7,"adjMaxPhysicalAtk":10,"adjMinMagicAtk":7,"adjMaxMagicAtk":10,"adjMinPhysicalArmor":1,"adjMaxPhysicalArmor":1,"adjMinMagicArmor":1,"adjMaxMagicArmor":1,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009102: _tools.RODict({
        "propID": 51009102,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":105,"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":52,"adjMinMagicAtk":30,"adjMaxMagicAtk":52,"adjMinPhysicalArmor":1,"adjMaxPhysicalArmor":1,"adjMinMagicArmor":1,"adjMaxMagicArmor":1,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009103: _tools.RODict({
        "propID": 51009103,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":110,"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":53,"adjMinMagicAtk":30,"adjMaxMagicAtk":53,"adjMinPhysicalArmor":1,"adjMaxPhysicalArmor":1,"adjMinMagicArmor":1,"adjMaxMagicArmor":1,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009104: _tools.RODict({
        "propID": 51009104,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":139,"adjMinPhysicalAtk":31,"adjMaxPhysicalAtk":53,"adjMinMagicAtk":31,"adjMaxMagicAtk":53,"adjMinPhysicalArmor":3,"adjMaxPhysicalArmor":3,"adjMinMagicArmor":3,"adjMaxMagicArmor":3,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009105: _tools.RODict({
        "propID": 51009105,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":144,"adjMinPhysicalAtk":31,"adjMaxPhysicalAtk":54,"adjMinMagicAtk":31,"adjMaxMagicAtk":54,"adjMinPhysicalArmor":3,"adjMaxPhysicalArmor":3,"adjMinMagicArmor":3,"adjMaxMagicArmor":3,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009106: _tools.RODict({
        "propID": 51009106,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":189,"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":54,"adjMinMagicAtk":32,"adjMaxMagicAtk":54,"adjMinPhysicalArmor":4,"adjMaxPhysicalArmor":4,"adjMinMagicArmor":4,"adjMaxMagicArmor":4,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009107: _tools.RODict({
        "propID": 51009107,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":194,"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":55,"adjMinMagicAtk":32,"adjMaxMagicAtk":55,"adjMinPhysicalArmor":4,"adjMaxPhysicalArmor":4,"adjMinMagicArmor":4,"adjMaxMagicArmor":4,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009108: _tools.RODict({
        "propID": 51009108,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":239,"adjMinPhysicalAtk":33,"adjMaxPhysicalAtk":55,"adjMinMagicAtk":33,"adjMaxMagicAtk":55,"adjMinPhysicalArmor":4,"adjMaxPhysicalArmor":4,"adjMinMagicArmor":4,"adjMaxMagicArmor":4,"adjHit":5,"adjDodge":4,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009109: _tools.RODict({
        "propID": 51009109,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":244,"adjMinPhysicalAtk":33,"adjMaxPhysicalAtk":56,"adjMinMagicAtk":33,"adjMaxMagicAtk":56,"adjMinPhysicalArmor":5,"adjMaxPhysicalArmor":5,"adjMinMagicArmor":5,"adjMaxMagicArmor":5,"adjHit":5,"adjDodge":4,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009110: _tools.RODict({
        "propID": 51009110,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":249,"adjMinPhysicalAtk":40,"adjMaxPhysicalAtk":62,"adjMinMagicAtk":40,"adjMaxMagicAtk":62,"adjMinPhysicalArmor":5,"adjMaxPhysicalArmor":5,"adjMinMagicArmor":5,"adjMaxMagicArmor":5,"adjHit":7,"adjDodge":4,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009111: _tools.RODict({
        "propID": 51009111,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":258,"adjMinPhysicalAtk":40,"adjMaxPhysicalAtk":63,"adjMinMagicAtk":40,"adjMaxMagicAtk":63,"adjMinPhysicalArmor":6,"adjMaxPhysicalArmor":6,"adjMinMagicArmor":6,"adjMaxMagicArmor":6,"adjHit":7,"adjDodge":4,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009112: _tools.RODict({
        "propID": 51009112,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":267,"adjMinPhysicalAtk":41,"adjMaxPhysicalAtk":63,"adjMinMagicAtk":41,"adjMaxMagicAtk":63,"adjMinPhysicalArmor":6,"adjMaxPhysicalArmor":6,"adjMinMagicArmor":6,"adjMaxMagicArmor":6,"adjHit":7,"adjDodge":4,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009113: _tools.RODict({
        "propID": 51009113,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":276,"adjMinPhysicalAtk":41,"adjMaxPhysicalAtk":64,"adjMinMagicAtk":41,"adjMaxMagicAtk":64,"adjMinPhysicalArmor":7,"adjMaxPhysicalArmor":7,"adjMinMagicArmor":7,"adjMaxMagicArmor":7,"adjHit":7,"adjDodge":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009114: _tools.RODict({
        "propID": 51009114,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":281,"adjMinPhysicalAtk":42,"adjMaxPhysicalAtk":64,"adjMinMagicAtk":42,"adjMaxMagicAtk":64,"adjMinPhysicalArmor":7,"adjMaxPhysicalArmor":7,"adjMinMagicArmor":7,"adjMaxMagicArmor":7,"adjHit":7,"adjDodge":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009115: _tools.RODict({
        "propID": 51009115,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":286,"adjMinPhysicalAtk":44,"adjMaxPhysicalAtk":75,"adjMinMagicAtk":44,"adjMaxMagicAtk":75,"adjMinPhysicalArmor":7,"adjMaxPhysicalArmor":7,"adjMinMagicArmor":7,"adjMaxMagicArmor":7,"adjHit":9,"adjDodge":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009116: _tools.RODict({
        "propID": 51009116,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":295,"adjMinPhysicalAtk":45,"adjMaxPhysicalAtk":75,"adjMinMagicAtk":45,"adjMaxMagicAtk":75,"adjMinPhysicalArmor":8,"adjMaxPhysicalArmor":8,"adjMinMagicArmor":8,"adjMaxMagicArmor":8,"adjHit":9,"adjDodge":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009117: _tools.RODict({
        "propID": 51009117,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":304,"adjMinPhysicalAtk":45,"adjMaxPhysicalAtk":76,"adjMinMagicAtk":45,"adjMaxMagicAtk":76,"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjHit":9,"adjDodge":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009118: _tools.RODict({
        "propID": 51009118,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":313,"adjMinPhysicalAtk":46,"adjMaxPhysicalAtk":76,"adjMinMagicAtk":46,"adjMaxMagicAtk":76,"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjHit":9,"adjDodge":6,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009119: _tools.RODict({
        "propID": 51009119,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":318,"adjMinPhysicalAtk":46,"adjMaxPhysicalAtk":77,"adjMinMagicAtk":46,"adjMaxMagicAtk":77,"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10,"adjHit":9,"adjDodge":6,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009120: _tools.RODict({
        "propID": 51009120,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":323,"adjMinPhysicalAtk":51,"adjMaxPhysicalAtk":83,"adjMinMagicAtk":51,"adjMaxMagicAtk":83,"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10,"adjHit":15,"adjDodge":6,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009121: _tools.RODict({
        "propID": 51009121,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":348,"adjMinPhysicalAtk":52,"adjMaxPhysicalAtk":85,"adjMinMagicAtk":52,"adjMaxMagicAtk":85,"adjMinPhysicalArmor":13,"adjMaxPhysicalArmor":13,"adjMinMagicArmor":13,"adjMaxMagicArmor":13,"adjHit":15,"adjDodge":6,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":7})
    }),
    51009122: _tools.RODict({
        "propID": 51009122,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":365,"adjMinPhysicalAtk":53,"adjMaxPhysicalAtk":85,"adjMinMagicAtk":53,"adjMaxMagicAtk":85,"adjMinPhysicalArmor":13,"adjMaxPhysicalArmor":13,"adjMinMagicArmor":13,"adjMaxMagicArmor":13,"adjHit":15,"adjDodge":10,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":7})
    }),
    51009123: _tools.RODict({
        "propID": 51009123,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":375,"adjMinPhysicalAtk":56,"adjMaxPhysicalAtk":90,"adjMinMagicAtk":56,"adjMaxMagicAtk":90,"adjMinPhysicalArmor":14,"adjMaxPhysicalArmor":14,"adjMinMagicArmor":14,"adjMaxMagicArmor":14,"adjHit":15,"adjDodge":10,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":7})
    }),
    51009124: _tools.RODict({
        "propID": 51009124,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":380,"adjMinPhysicalAtk":60,"adjMaxPhysicalAtk":94,"adjMinMagicAtk":60,"adjMaxMagicAtk":94,"adjMinPhysicalArmor":14,"adjMaxPhysicalArmor":14,"adjMinMagicArmor":14,"adjMaxMagicArmor":14,"adjHit":15,"adjDodge":10,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":7})
    }),
    51009125: _tools.RODict({
        "propID": 51009125,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":397,"adjMinPhysicalAtk":68,"adjMaxPhysicalAtk":109,"adjMinMagicAtk":68,"adjMaxMagicAtk":109,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjHit":18,"adjDodge":10,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":8})
    }),
    51009126: _tools.RODict({
        "propID": 51009126,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":410,"adjMinPhysicalAtk":69,"adjMaxPhysicalAtk":109,"adjMinMagicAtk":69,"adjMaxMagicAtk":109,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjHit":18,"adjDodge":12,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":8})
    }),
    51009127: _tools.RODict({
        "propID": 51009127,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":415,"adjMinPhysicalAtk":69,"adjMaxPhysicalAtk":110,"adjMinMagicAtk":69,"adjMaxMagicAtk":110,"adjMinPhysicalArmor":17,"adjMaxPhysicalArmor":17,"adjMinMagicArmor":17,"adjMaxMagicArmor":17,"adjHit":18,"adjDodge":12,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":8})
    }),
    51009128: _tools.RODict({
        "propID": 51009128,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":420,"adjMinPhysicalAtk":72,"adjMaxPhysicalAtk":114,"adjMinMagicAtk":72,"adjMaxMagicAtk":114,"adjMinPhysicalArmor":17,"adjMaxPhysicalArmor":17,"adjMinMagicArmor":17,"adjMaxMagicArmor":17,"adjHit":18,"adjDodge":12,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":8})
    }),
    51009129: _tools.RODict({
        "propID": 51009129,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":437,"adjMinPhysicalAtk":78,"adjMaxPhysicalAtk":128,"adjMinMagicAtk":78,"adjMaxMagicAtk":128,"adjMinPhysicalArmor":18,"adjMaxPhysicalArmor":18,"adjMinMagicArmor":18,"adjMaxMagicArmor":18,"adjHit":21,"adjDodge":12,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":9})
    }),
    51009130: _tools.RODict({
        "propID": 51009130,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":450,"adjMinPhysicalAtk":79,"adjMaxPhysicalAtk":129,"adjMinMagicAtk":79,"adjMaxMagicAtk":129,"adjMinPhysicalArmor":19,"adjMaxPhysicalArmor":19,"adjMinMagicArmor":19,"adjMaxMagicArmor":19,"adjHit":21,"adjDodge":14,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":9})
    }),
    51009131: _tools.RODict({
        "propID": 51009131,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":455,"adjMinPhysicalAtk":80,"adjMaxPhysicalAtk":134,"adjMinMagicAtk":80,"adjMaxMagicAtk":134,"adjMinPhysicalArmor":19,"adjMaxPhysicalArmor":19,"adjMinMagicArmor":19,"adjMaxMagicArmor":19,"adjHit":21,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":9})
    }),
    51009132: _tools.RODict({
        "propID": 51009132,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":460,"adjMinPhysicalAtk":84,"adjMaxPhysicalAtk":140,"adjMinMagicAtk":84,"adjMaxMagicAtk":140,"adjMinPhysicalArmor":19,"adjMaxPhysicalArmor":19,"adjMinMagicArmor":19,"adjMaxMagicArmor":19,"adjHit":22,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":3,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":9})
    }),
    51009133: _tools.RODict({
        "propID": 51009133,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":487,"adjMinPhysicalAtk":90,"adjMaxPhysicalAtk":153,"adjMinMagicAtk":90,"adjMaxMagicAtk":153,"adjMinPhysicalArmor":22,"adjMaxPhysicalArmor":22,"adjMinMagicArmor":22,"adjMaxMagicArmor":22,"adjHit":25,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":3,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":10})
    }),
    51009134: _tools.RODict({
        "propID": 51009134,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":500,"adjMinPhysicalAtk":91,"adjMaxPhysicalAtk":154,"adjMinMagicAtk":91,"adjMaxMagicAtk":154,"adjMinPhysicalArmor":23,"adjMaxPhysicalArmor":23,"adjMinMagicArmor":23,"adjMaxMagicArmor":23,"adjHit":25,"adjDodge":16,"adjRealDmg":2,"adjRealDmgDef":3,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":10})
    }),
    51009135: _tools.RODict({
        "propID": 51009135,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":505,"adjMinPhysicalAtk":92,"adjMaxPhysicalAtk":158,"adjMinMagicAtk":92,"adjMaxMagicAtk":158,"adjMinPhysicalArmor":24,"adjMaxPhysicalArmor":24,"adjMinMagicArmor":24,"adjMaxMagicArmor":24,"adjHit":25,"adjDodge":16,"adjRealDmg":3,"adjRealDmgDef":3,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":10})
    }),
    51009136: _tools.RODict({
        "propID": 51009136,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":510,"adjMinPhysicalAtk":94,"adjMaxPhysicalAtk":160,"adjMinMagicAtk":94,"adjMaxMagicAtk":160,"adjMinPhysicalArmor":24,"adjMaxPhysicalArmor":24,"adjMinMagicArmor":24,"adjMaxMagicArmor":24,"adjHit":25,"adjDodge":16,"adjRealDmg":3,"adjRealDmgDef":4,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":10})
    }),
    51009137: _tools.RODict({
        "propID": 51009137,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":515,"adjMinPhysicalAtk":100,"adjMaxPhysicalAtk":173,"adjMinMagicAtk":100,"adjMaxMagicAtk":173,"adjMinPhysicalArmor":25,"adjMaxPhysicalArmor":25,"adjMinMagicArmor":25,"adjMaxMagicArmor":25,"adjHit":34,"adjDodge":17,"adjRealDmg":3,"adjRealDmgDef":4,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":10})
    }),
    51009138: _tools.RODict({
        "propID": 51009138,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":576,"adjMinPhysicalAtk":101,"adjMaxPhysicalAtk":173,"adjMinMagicAtk":101,"adjMaxMagicAtk":173,"adjMinPhysicalArmor":29,"adjMaxPhysicalArmor":29,"adjMinMagicArmor":29,"adjMaxMagicArmor":29,"adjHit":34,"adjDodge":17,"adjRealDmg":4,"adjRealDmgDef":4,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":11})
    }),
    51009139: _tools.RODict({
        "propID": 51009139,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":617,"adjMinPhysicalAtk":101,"adjMaxPhysicalAtk":176,"adjMinMagicAtk":101,"adjMaxMagicAtk":176,"adjMinPhysicalArmor":30,"adjMaxPhysicalArmor":30,"adjMinMagicArmor":30,"adjMaxMagicArmor":30,"adjHit":34,"adjDodge":23,"adjRealDmg":4,"adjRealDmgDef":5,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":5,"adjDebilityAnti":11})
    }),
    51009140: _tools.RODict({
        "propID": 51009140,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":622,"adjMinPhysicalAtk":108,"adjMaxPhysicalAtk":198,"adjMinMagicAtk":108,"adjMaxMagicAtk":198,"adjMinPhysicalArmor":30,"adjMaxPhysicalArmor":30,"adjMinMagicArmor":30,"adjMaxMagicArmor":30,"adjHit":34,"adjDodge":23,"adjRealDmg":4,"adjRealDmgDef":5,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":5,"adjDebilityAnti":11})
    }),
    51009141: _tools.RODict({
        "propID": 51009141,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":627,"adjMinPhysicalAtk":126,"adjMaxPhysicalAtk":230,"adjMinMagicAtk":126,"adjMaxMagicAtk":230,"adjMinPhysicalArmor":31,"adjMaxPhysicalArmor":31,"adjMinMagicArmor":31,"adjMaxMagicArmor":31,"adjHit":38,"adjDodge":23,"adjRealDmg":4,"adjRealDmgDef":5,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":5,"adjDebilityAnti":11})
    }),
    51009142: _tools.RODict({
        "propID": 51009142,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":659,"adjMinPhysicalAtk":127,"adjMaxPhysicalAtk":230,"adjMinMagicAtk":127,"adjMaxMagicAtk":230,"adjMinPhysicalArmor":32,"adjMaxPhysicalArmor":32,"adjMinMagicArmor":32,"adjMaxMagicArmor":32,"adjHit":38,"adjDodge":23,"adjRealDmg":5,"adjRealDmgDef":5,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":5,"adjDebilityAnti":11})
    }),
    51009143: _tools.RODict({
        "propID": 51009143,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":704,"adjMinPhysicalAtk":127,"adjMaxPhysicalAtk":231,"adjMinMagicAtk":127,"adjMaxMagicAtk":231,"adjMinPhysicalArmor":34,"adjMaxPhysicalArmor":34,"adjMinMagicArmor":34,"adjMaxMagicArmor":34,"adjHit":38,"adjDodge":25,"adjRealDmg":5,"adjRealDmgDef":6,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":5,"adjDebilityAnti":12})
    }),
    51009144: _tools.RODict({
        "propID": 51009144,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":709,"adjMinPhysicalAtk":129,"adjMaxPhysicalAtk":235,"adjMinMagicAtk":129,"adjMaxMagicAtk":235,"adjMinPhysicalArmor":35,"adjMaxPhysicalArmor":35,"adjMinMagicArmor":35,"adjMaxMagicArmor":35,"adjHit":38,"adjDodge":26,"adjRealDmg":5,"adjRealDmgDef":6,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":6,"adjDebilityAnti":12})
    }),
    51009145: _tools.RODict({
        "propID": 51009145,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":714,"adjMinPhysicalAtk":130,"adjMaxPhysicalAtk":240,"adjMinMagicAtk":130,"adjMaxMagicAtk":240,"adjMinPhysicalArmor":37,"adjMaxPhysicalArmor":37,"adjMinMagicArmor":37,"adjMaxMagicArmor":37,"adjHit":38,"adjDodge":26,"adjRealDmg":5,"adjRealDmgDef":6,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":6,"adjDebilityAnti":12})
    }),
    51009146: _tools.RODict({
        "propID": 51009146,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":737,"adjMinPhysicalAtk":141,"adjMaxPhysicalAtk":263,"adjMinMagicAtk":141,"adjMaxMagicAtk":263,"adjMinPhysicalArmor":37,"adjMaxPhysicalArmor":37,"adjMinMagicArmor":37,"adjMaxMagicArmor":37,"adjHit":43,"adjDodge":26,"adjRealDmg":5,"adjRealDmgDef":6,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":6,"adjDebilityAnti":12})
    }),
    51009147: _tools.RODict({
        "propID": 51009147,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":754,"adjMinPhysicalAtk":141,"adjMaxPhysicalAtk":264,"adjMinMagicAtk":141,"adjMaxMagicAtk":264,"adjMinPhysicalArmor":40,"adjMaxPhysicalArmor":40,"adjMinMagicArmor":40,"adjMaxMagicArmor":40,"adjHit":43,"adjDodge":26,"adjRealDmg":6,"adjRealDmgDef":6,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":6,"adjDebilityAnti":12})
    }),
    51009148: _tools.RODict({
        "propID": 51009148,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":799,"adjMinPhysicalAtk":142,"adjMaxPhysicalAtk":264,"adjMinMagicAtk":142,"adjMaxMagicAtk":264,"adjMinPhysicalArmor":40,"adjMaxPhysicalArmor":40,"adjMinMagicArmor":40,"adjMaxMagicArmor":40,"adjHit":43,"adjDodge":30,"adjRealDmg":6,"adjRealDmgDef":7,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":6,"adjDebilityAnti":13})
    }),
    51009149: _tools.RODict({
        "propID": 51009149,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":824,"adjMinPhysicalAtk":147,"adjMaxPhysicalAtk":278,"adjMinMagicAtk":147,"adjMaxMagicAtk":278,"adjMinPhysicalArmor":42,"adjMaxPhysicalArmor":42,"adjMinMagicArmor":42,"adjMaxMagicArmor":42,"adjHit":45,"adjDodge":30,"adjRealDmg":6,"adjRealDmgDef":7,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":7,"adjDebilityAnti":13})
    }),
    51009150: _tools.RODict({
        "propID": 51009150,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":829,"adjMinPhysicalAtk":150,"adjMaxPhysicalAtk":285,"adjMinMagicAtk":150,"adjMaxMagicAtk":285,"adjMinPhysicalArmor":44,"adjMaxPhysicalArmor":44,"adjMinMagicArmor":44,"adjMaxMagicArmor":44,"adjHit":45,"adjDodge":32,"adjRealDmg":6,"adjRealDmgDef":7,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":7,"adjDebilityAnti":13})
    }),
    51009151: _tools.RODict({
        "propID": 51009151,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":834,"adjMinPhysicalAtk":162,"adjMaxPhysicalAtk":306,"adjMinMagicAtk":162,"adjMaxMagicAtk":306,"adjMinPhysicalArmor":45,"adjMaxPhysicalArmor":45,"adjMinMagicArmor":45,"adjMaxMagicArmor":45,"adjHit":48,"adjDodge":32,"adjRealDmg":6,"adjRealDmgDef":7,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":7,"adjDebilityAnti":13})
    }),
    51009152: _tools.RODict({
        "propID": 51009152,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":863,"adjMinPhysicalAtk":167,"adjMaxPhysicalAtk":314,"adjMinMagicAtk":167,"adjMaxMagicAtk":314,"adjMinPhysicalArmor":46,"adjMaxPhysicalArmor":46,"adjMinMagicArmor":46,"adjMaxMagicArmor":46,"adjHit":51,"adjDodge":32,"adjRealDmg":7,"adjRealDmgDef":7,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":7,"adjDebilityAnti":13})
    }),
    51009153: _tools.RODict({
        "propID": 51009153,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":970,"adjMinPhysicalAtk":167,"adjMaxPhysicalAtk":315,"adjMinMagicAtk":167,"adjMaxMagicAtk":315,"adjMinPhysicalArmor":48,"adjMaxPhysicalArmor":48,"adjMinMagicArmor":48,"adjMaxMagicArmor":48,"adjHit":51,"adjDodge":34,"adjRealDmg":7,"adjRealDmgDef":8,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":7,"adjDebilityAnti":14})
    }),
    51009154: _tools.RODict({
        "propID": 51009154,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":975,"adjMinPhysicalAtk":170,"adjMaxPhysicalAtk":320,"adjMinMagicAtk":170,"adjMaxMagicAtk":320,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":50,"adjMaxMagicArmor":50,"adjHit":51,"adjDodge":34,"adjRealDmg":7,"adjRealDmgDef":8,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":8,"adjDebilityAnti":14})
    }),
    51009155: _tools.RODict({
        "propID": 51009155,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":980,"adjMinPhysicalAtk":172,"adjMaxPhysicalAtk":326,"adjMinMagicAtk":172,"adjMaxMagicAtk":326,"adjMinPhysicalArmor":52,"adjMaxPhysicalArmor":52,"adjMinMagicArmor":52,"adjMaxMagicArmor":52,"adjHit":51,"adjDodge":37,"adjRealDmg":7,"adjRealDmgDef":8,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":8,"adjDebilityAnti":14})
    }),
    51009156: _tools.RODict({
        "propID": 51009156,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":985,"adjMinPhysicalAtk":185,"adjMaxPhysicalAtk":350,"adjMinMagicAtk":185,"adjMaxMagicAtk":350,"adjMinPhysicalArmor":52,"adjMaxPhysicalArmor":52,"adjMinMagicArmor":52,"adjMaxMagicArmor":52,"adjHit":54,"adjDodge":37,"adjRealDmg":7,"adjRealDmgDef":8,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":8,"adjDebilityAnti":14})
    }),
    51009157: _tools.RODict({
        "propID": 51009157,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1014,"adjMinPhysicalAtk":190,"adjMaxPhysicalAtk":360,"adjMinMagicAtk":190,"adjMaxMagicAtk":360,"adjMinPhysicalArmor":54,"adjMaxPhysicalArmor":54,"adjMinMagicArmor":54,"adjMaxMagicArmor":54,"adjHit":57,"adjDodge":37,"adjRealDmg":8,"adjRealDmgDef":8,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":8,"adjDebilityAnti":14})
    }),
    51009158: _tools.RODict({
        "propID": 51009158,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1129,"adjMinPhysicalAtk":191,"adjMaxPhysicalAtk":360,"adjMinMagicAtk":191,"adjMaxMagicAtk":360,"adjMinPhysicalArmor":55,"adjMaxPhysicalArmor":55,"adjMinMagicArmor":55,"adjMaxMagicArmor":55,"adjHit":57,"adjDodge":39,"adjRealDmg":8,"adjRealDmgDef":9,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":8,"adjDebilityAnti":15})
    }),
    51009159: _tools.RODict({
        "propID": 51009159,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1134,"adjMinPhysicalAtk":193,"adjMaxPhysicalAtk":371,"adjMinMagicAtk":193,"adjMaxMagicAtk":371,"adjMinPhysicalArmor":59,"adjMaxPhysicalArmor":59,"adjMinMagicArmor":59,"adjMaxMagicArmor":59,"adjHit":57,"adjDodge":39,"adjRealDmg":8,"adjRealDmgDef":9,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":9,"adjDebilityAnti":15})
    }),
    51009160: _tools.RODict({
        "propID": 51009160,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1139,"adjMinPhysicalAtk":196,"adjMaxPhysicalAtk":381,"adjMinMagicAtk":196,"adjMaxMagicAtk":381,"adjMinPhysicalArmor":60,"adjMaxPhysicalArmor":60,"adjMinMagicArmor":60,"adjMaxMagicArmor":60,"adjHit":57,"adjDodge":42,"adjRealDmg":8,"adjRealDmgDef":9,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":9,"adjDebilityAnti":15})
    }),
    51009161: _tools.RODict({
        "propID": 51009161,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1144,"adjMinPhysicalAtk":220,"adjMaxPhysicalAtk":424,"adjMinMagicAtk":220,"adjMaxMagicAtk":424,"adjMinPhysicalArmor":61,"adjMaxPhysicalArmor":61,"adjMinMagicArmor":61,"adjMaxMagicArmor":61,"adjHit":66,"adjDodge":42,"adjRealDmg":8,"adjRealDmgDef":9,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":9,"adjDebilityAnti":15})
    }),
    51009162: _tools.RODict({
        "propID": 51009162,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1197,"adjMinPhysicalAtk":227,"adjMaxPhysicalAtk":434,"adjMinMagicAtk":227,"adjMaxMagicAtk":434,"adjMinPhysicalArmor":65,"adjMaxPhysicalArmor":65,"adjMinMagicArmor":65,"adjMaxMagicArmor":65,"adjHit":69,"adjDodge":42,"adjRealDmg":10,"adjRealDmgDef":9,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":9,"adjDebilityAnti":15})
    }),
    51009163: _tools.RODict({
        "propID": 51009163,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1400,"adjMinPhysicalAtk":227,"adjMaxPhysicalAtk":435,"adjMinMagicAtk":227,"adjMaxMagicAtk":435,"adjMinPhysicalArmor":68,"adjMaxPhysicalArmor":68,"adjMinMagicArmor":68,"adjMaxMagicArmor":68,"adjHit":69,"adjDodge":48,"adjRealDmg":10,"adjRealDmgDef":11,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":9,"adjDebilityAnti":17})
    }),
    51009164: _tools.RODict({
        "propID": 51009164,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1405,"adjMinPhysicalAtk":231,"adjMaxPhysicalAtk":452,"adjMinMagicAtk":231,"adjMaxMagicAtk":452,"adjMinPhysicalArmor":71,"adjMaxPhysicalArmor":71,"adjMinMagicArmor":71,"adjMaxMagicArmor":71,"adjHit":69,"adjDodge":48,"adjRealDmg":10,"adjRealDmgDef":11,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":11,"adjDebilityAnti":17})
    }),
    51009165: _tools.RODict({
        "propID": 51009165,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1410,"adjMinPhysicalAtk":234,"adjMaxPhysicalAtk":470,"adjMinMagicAtk":234,"adjMaxMagicAtk":470,"adjMinPhysicalArmor":73,"adjMaxPhysicalArmor":73,"adjMinMagicArmor":73,"adjMaxMagicArmor":73,"adjHit":69,"adjDodge":52,"adjRealDmg":10,"adjRealDmgDef":11,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":11,"adjDebilityAnti":17})
    }),
    51009166: _tools.RODict({
        "propID": 51009166,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1415,"adjMinPhysicalAtk":253,"adjMaxPhysicalAtk":504,"adjMinMagicAtk":253,"adjMaxMagicAtk":504,"adjMinPhysicalArmor":73,"adjMaxPhysicalArmor":73,"adjMinMagicArmor":73,"adjMaxMagicArmor":73,"adjHit":72,"adjDodge":52,"adjRealDmg":10,"adjRealDmgDef":11,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":11,"adjDebilityAnti":17})
    }),
    51009167: _tools.RODict({
        "propID": 51009167,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1444,"adjMinPhysicalAtk":261,"adjMaxPhysicalAtk":516,"adjMinMagicAtk":261,"adjMaxMagicAtk":516,"adjMinPhysicalArmor":77,"adjMaxPhysicalArmor":77,"adjMinMagicArmor":77,"adjMaxMagicArmor":77,"adjHit":75,"adjDodge":52,"adjRealDmg":12,"adjRealDmgDef":11,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":11,"adjDebilityAnti":17})
    }),
    51009168: _tools.RODict({
        "propID": 51009168,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1574,"adjMinPhysicalAtk":262,"adjMaxPhysicalAtk":516,"adjMinMagicAtk":262,"adjMaxMagicAtk":516,"adjMinPhysicalArmor":79,"adjMaxPhysicalArmor":79,"adjMinMagicArmor":79,"adjMaxMagicArmor":79,"adjHit":75,"adjDodge":54,"adjRealDmg":12,"adjRealDmgDef":13,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":11,"adjDebilityAnti":18})
    }),
    51009169: _tools.RODict({
        "propID": 51009169,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1579,"adjMinPhysicalAtk":264,"adjMaxPhysicalAtk":529,"adjMinMagicAtk":264,"adjMaxMagicAtk":529,"adjMinPhysicalArmor":84,"adjMaxPhysicalArmor":84,"adjMinMagicArmor":84,"adjMaxMagicArmor":84,"adjHit":75,"adjDodge":54,"adjRealDmg":12,"adjRealDmgDef":13,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":12,"adjDebilityAnti":18})
    }),
    51009170: _tools.RODict({
        "propID": 51009170,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1589,"adjMinPhysicalAtk":267,"adjMaxPhysicalAtk":541,"adjMinMagicAtk":267,"adjMaxMagicAtk":541,"adjMinPhysicalArmor":86,"adjMaxPhysicalArmor":86,"adjMinMagicArmor":86,"adjMaxMagicArmor":86,"adjHit":75,"adjDodge":58,"adjRealDmg":12,"adjRealDmgDef":13,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":12,"adjDebilityAnti":18})
    }),
    51009201: _tools.RODict({
        "propID": 51009201,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":150,"adjMinPhysicalAtk":4,"adjMaxPhysicalAtk":5,"adjMinMagicAtk":4,"adjMaxMagicAtk":5,"adjMinPhysicalArmor":1,"adjMaxPhysicalArmor":1,"adjMinMagicArmor":1,"adjMaxMagicArmor":1,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009202: _tools.RODict({
        "propID": 51009202,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":158,"adjMinPhysicalAtk":15,"adjMaxPhysicalAtk":26,"adjMinMagicAtk":15,"adjMaxMagicAtk":26,"adjMinPhysicalArmor":1,"adjMaxPhysicalArmor":1,"adjMinMagicArmor":1,"adjMaxMagicArmor":1,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009203: _tools.RODict({
        "propID": 51009203,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":165,"adjMinPhysicalAtk":15,"adjMaxPhysicalAtk":27,"adjMinMagicAtk":15,"adjMaxMagicAtk":27,"adjMinPhysicalArmor":1,"adjMaxPhysicalArmor":1,"adjMinMagicArmor":1,"adjMaxMagicArmor":1,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009204: _tools.RODict({
        "propID": 51009204,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":209,"adjMinPhysicalAtk":16,"adjMaxPhysicalAtk":27,"adjMinMagicAtk":16,"adjMaxMagicAtk":27,"adjMinPhysicalArmor":3,"adjMaxPhysicalArmor":3,"adjMinMagicArmor":3,"adjMaxMagicArmor":3,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009205: _tools.RODict({
        "propID": 51009205,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":216,"adjMinPhysicalAtk":16,"adjMaxPhysicalAtk":27,"adjMinMagicAtk":16,"adjMaxMagicAtk":27,"adjMinPhysicalArmor":3,"adjMaxPhysicalArmor":3,"adjMinMagicArmor":3,"adjMaxMagicArmor":3,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009206: _tools.RODict({
        "propID": 51009206,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":284,"adjMinPhysicalAtk":16,"adjMaxPhysicalAtk":27,"adjMinMagicAtk":16,"adjMaxMagicAtk":27,"adjMinPhysicalArmor":4,"adjMaxPhysicalArmor":4,"adjMinMagicArmor":4,"adjMaxMagicArmor":4,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009207: _tools.RODict({
        "propID": 51009207,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":291,"adjMinPhysicalAtk":16,"adjMaxPhysicalAtk":28,"adjMinMagicAtk":16,"adjMaxMagicAtk":28,"adjMinPhysicalArmor":4,"adjMaxPhysicalArmor":4,"adjMinMagicArmor":4,"adjMaxMagicArmor":4,"adjHit":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009208: _tools.RODict({
        "propID": 51009208,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":359,"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":28,"adjMinMagicAtk":17,"adjMaxMagicAtk":28,"adjMinPhysicalArmor":4,"adjMaxPhysicalArmor":4,"adjMinMagicArmor":4,"adjMaxMagicArmor":4,"adjHit":5,"adjDodge":4,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009209: _tools.RODict({
        "propID": 51009209,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":366,"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":28,"adjMinMagicAtk":17,"adjMaxMagicAtk":28,"adjMinPhysicalArmor":5,"adjMaxPhysicalArmor":5,"adjMinMagicArmor":5,"adjMaxMagicArmor":5,"adjHit":5,"adjDodge":4,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009210: _tools.RODict({
        "propID": 51009210,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":374,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":31,"adjMinMagicAtk":20,"adjMaxMagicAtk":31,"adjMinPhysicalArmor":5,"adjMaxPhysicalArmor":5,"adjMinMagicArmor":5,"adjMaxMagicArmor":5,"adjHit":7,"adjDodge":4,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009211: _tools.RODict({
        "propID": 51009211,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":387,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":32,"adjMinMagicAtk":20,"adjMaxMagicAtk":32,"adjMinPhysicalArmor":6,"adjMaxPhysicalArmor":6,"adjMinMagicArmor":6,"adjMaxMagicArmor":6,"adjHit":7,"adjDodge":4,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009212: _tools.RODict({
        "propID": 51009212,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":401,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":32,"adjMinMagicAtk":21,"adjMaxMagicAtk":32,"adjMinPhysicalArmor":6,"adjMaxPhysicalArmor":6,"adjMinMagicArmor":6,"adjMaxMagicArmor":6,"adjHit":7,"adjDodge":4,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009213: _tools.RODict({
        "propID": 51009213,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":414,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":32,"adjMinMagicAtk":21,"adjMaxMagicAtk":32,"adjMinPhysicalArmor":7,"adjMaxPhysicalArmor":7,"adjMinMagicArmor":7,"adjMaxMagicArmor":7,"adjHit":7,"adjDodge":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009214: _tools.RODict({
        "propID": 51009214,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":422,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":32,"adjMinMagicAtk":21,"adjMaxMagicAtk":32,"adjMinPhysicalArmor":7,"adjMaxPhysicalArmor":7,"adjMinMagicArmor":7,"adjMaxMagicArmor":7,"adjHit":7,"adjDodge":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009215: _tools.RODict({
        "propID": 51009215,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":429,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":38,"adjMinMagicAtk":22,"adjMaxMagicAtk":38,"adjMinPhysicalArmor":7,"adjMaxPhysicalArmor":7,"adjMinMagicArmor":7,"adjMaxMagicArmor":7,"adjHit":9,"adjDodge":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009216: _tools.RODict({
        "propID": 51009216,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":443,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":38,"adjMinMagicAtk":23,"adjMaxMagicAtk":38,"adjMinPhysicalArmor":8,"adjMaxPhysicalArmor":8,"adjMinMagicArmor":8,"adjMaxMagicArmor":8,"adjHit":9,"adjDodge":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009217: _tools.RODict({
        "propID": 51009217,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":456,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":38,"adjMinMagicAtk":23,"adjMaxMagicAtk":38,"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjHit":9,"adjDodge":5,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009218: _tools.RODict({
        "propID": 51009218,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":470,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":38,"adjMinMagicAtk":23,"adjMaxMagicAtk":38,"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjHit":9,"adjDodge":6,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009219: _tools.RODict({
        "propID": 51009219,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":477,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":39,"adjMinMagicAtk":23,"adjMaxMagicAtk":39,"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10,"adjHit":9,"adjDodge":6,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009220: _tools.RODict({
        "propID": 51009220,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":485,"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":42,"adjMinMagicAtk":26,"adjMaxMagicAtk":42,"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10,"adjHit":15,"adjDodge":6,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":6})
    }),
    51009221: _tools.RODict({
        "propID": 51009221,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":522,"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":43,"adjMinMagicAtk":26,"adjMaxMagicAtk":43,"adjMinPhysicalArmor":13,"adjMaxPhysicalArmor":13,"adjMinMagicArmor":13,"adjMaxMagicArmor":13,"adjHit":15,"adjDodge":6,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":7})
    }),
    51009222: _tools.RODict({
        "propID": 51009222,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":548,"adjMinPhysicalAtk":27,"adjMaxPhysicalAtk":43,"adjMinMagicAtk":27,"adjMaxMagicAtk":43,"adjMinPhysicalArmor":13,"adjMaxPhysicalArmor":13,"adjMinMagicArmor":13,"adjMaxMagicArmor":13,"adjHit":15,"adjDodge":10,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":7})
    }),
    51009223: _tools.RODict({
        "propID": 51009223,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":563,"adjMinPhysicalAtk":28,"adjMaxPhysicalAtk":45,"adjMinMagicAtk":28,"adjMaxMagicAtk":45,"adjMinPhysicalArmor":14,"adjMaxPhysicalArmor":14,"adjMinMagicArmor":14,"adjMaxMagicArmor":14,"adjHit":15,"adjDodge":10,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":7})
    }),
    51009224: _tools.RODict({
        "propID": 51009224,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":570,"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":47,"adjMinMagicAtk":30,"adjMaxMagicAtk":47,"adjMinPhysicalArmor":14,"adjMaxPhysicalArmor":14,"adjMinMagicArmor":14,"adjMaxMagicArmor":14,"adjHit":15,"adjDodge":10,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":7})
    }),
    51009225: _tools.RODict({
        "propID": 51009225,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":596,"adjMinPhysicalAtk":34,"adjMaxPhysicalAtk":55,"adjMinMagicAtk":34,"adjMaxMagicAtk":55,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjHit":18,"adjDodge":10,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":8})
    }),
    51009226: _tools.RODict({
        "propID": 51009226,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":615,"adjMinPhysicalAtk":35,"adjMaxPhysicalAtk":55,"adjMinMagicAtk":35,"adjMaxMagicAtk":55,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjHit":18,"adjDodge":12,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":8})
    }),
    51009227: _tools.RODict({
        "propID": 51009227,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":623,"adjMinPhysicalAtk":35,"adjMaxPhysicalAtk":55,"adjMinMagicAtk":35,"adjMaxMagicAtk":55,"adjMinPhysicalArmor":17,"adjMaxPhysicalArmor":17,"adjMinMagicArmor":17,"adjMaxMagicArmor":17,"adjHit":18,"adjDodge":12,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":8})
    }),
    51009228: _tools.RODict({
        "propID": 51009228,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":630,"adjMinPhysicalAtk":36,"adjMaxPhysicalAtk":57,"adjMinMagicAtk":36,"adjMaxMagicAtk":57,"adjMinPhysicalArmor":17,"adjMaxPhysicalArmor":17,"adjMinMagicArmor":17,"adjMaxMagicArmor":17,"adjHit":18,"adjDodge":12,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":8})
    }),
    51009229: _tools.RODict({
        "propID": 51009229,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":656,"adjMinPhysicalAtk":39,"adjMaxPhysicalAtk":64,"adjMinMagicAtk":39,"adjMaxMagicAtk":64,"adjMinPhysicalArmor":18,"adjMaxPhysicalArmor":18,"adjMinMagicArmor":18,"adjMaxMagicArmor":18,"adjHit":21,"adjDodge":12,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":9})
    }),
    51009230: _tools.RODict({
        "propID": 51009230,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":675,"adjMinPhysicalAtk":40,"adjMaxPhysicalAtk":65,"adjMinMagicAtk":40,"adjMaxMagicAtk":65,"adjMinPhysicalArmor":19,"adjMaxPhysicalArmor":19,"adjMinMagicArmor":19,"adjMaxMagicArmor":19,"adjHit":21,"adjDodge":14,"adjRealDmg":1,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":9})
    }),
    51009231: _tools.RODict({
        "propID": 51009231,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":683,"adjMinPhysicalAtk":40,"adjMaxPhysicalAtk":67,"adjMinMagicAtk":40,"adjMaxMagicAtk":67,"adjMinPhysicalArmor":19,"adjMaxPhysicalArmor":19,"adjMinMagicArmor":19,"adjMaxMagicArmor":19,"adjHit":21,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":2,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":9})
    }),
    51009232: _tools.RODict({
        "propID": 51009232,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":690,"adjMinPhysicalAtk":42,"adjMaxPhysicalAtk":70,"adjMinMagicAtk":42,"adjMaxMagicAtk":70,"adjMinPhysicalArmor":19,"adjMaxPhysicalArmor":19,"adjMinMagicArmor":19,"adjMaxMagicArmor":19,"adjHit":22,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":3,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":9})
    }),
    51009233: _tools.RODict({
        "propID": 51009233,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":731,"adjMinPhysicalAtk":45,"adjMaxPhysicalAtk":77,"adjMinMagicAtk":45,"adjMaxMagicAtk":77,"adjMinPhysicalArmor":22,"adjMaxPhysicalArmor":22,"adjMinMagicArmor":22,"adjMaxMagicArmor":22,"adjHit":25,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":3,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":10})
    }),
    51009234: _tools.RODict({
        "propID": 51009234,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":750,"adjMinPhysicalAtk":46,"adjMaxPhysicalAtk":77,"adjMinMagicAtk":46,"adjMaxMagicAtk":77,"adjMinPhysicalArmor":23,"adjMaxPhysicalArmor":23,"adjMinMagicArmor":23,"adjMaxMagicArmor":23,"adjHit":25,"adjDodge":16,"adjRealDmg":2,"adjRealDmgDef":3,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":10})
    }),
    51009235: _tools.RODict({
        "propID": 51009235,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":758,"adjMinPhysicalAtk":46,"adjMaxPhysicalAtk":79,"adjMinMagicAtk":46,"adjMaxMagicAtk":79,"adjMinPhysicalArmor":24,"adjMaxPhysicalArmor":24,"adjMinMagicArmor":24,"adjMaxMagicArmor":24,"adjHit":25,"adjDodge":16,"adjRealDmg":3,"adjRealDmgDef":3,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":10})
    }),
    51009236: _tools.RODict({
        "propID": 51009236,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":765,"adjMinPhysicalAtk":47,"adjMaxPhysicalAtk":80,"adjMinMagicAtk":47,"adjMaxMagicAtk":80,"adjMinPhysicalArmor":24,"adjMaxPhysicalArmor":24,"adjMinMagicArmor":24,"adjMaxMagicArmor":24,"adjHit":25,"adjDodge":16,"adjRealDmg":3,"adjRealDmgDef":4,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":10})
    }),
    51009237: _tools.RODict({
        "propID": 51009237,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":773,"adjMinPhysicalAtk":50,"adjMaxPhysicalAtk":87,"adjMinMagicAtk":50,"adjMaxMagicAtk":87,"adjMinPhysicalArmor":25,"adjMaxPhysicalArmor":25,"adjMinMagicArmor":25,"adjMaxMagicArmor":25,"adjHit":34,"adjDodge":17,"adjRealDmg":3,"adjRealDmgDef":4,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":10})
    }),
    51009238: _tools.RODict({
        "propID": 51009238,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":864,"adjMinPhysicalAtk":51,"adjMaxPhysicalAtk":87,"adjMinMagicAtk":51,"adjMaxMagicAtk":87,"adjMinPhysicalArmor":29,"adjMaxPhysicalArmor":29,"adjMinMagicArmor":29,"adjMaxMagicArmor":29,"adjHit":34,"adjDodge":17,"adjRealDmg":4,"adjRealDmgDef":4,"adjMonsterDmgAnti":0.5,"adjDebilityAnti":11})
    }),
    51009239: _tools.RODict({
        "propID": 51009239,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":926,"adjMinPhysicalAtk":51,"adjMaxPhysicalAtk":88,"adjMinMagicAtk":51,"adjMaxMagicAtk":88,"adjMinPhysicalArmor":30,"adjMaxPhysicalArmor":30,"adjMinMagicArmor":30,"adjMaxMagicArmor":30,"adjHit":34,"adjDodge":23,"adjRealDmg":4,"adjRealDmgDef":5,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":5,"adjDebilityAnti":11})
    }),
    51009240: _tools.RODict({
        "propID": 51009240,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":933,"adjMinPhysicalAtk":54,"adjMaxPhysicalAtk":99,"adjMinMagicAtk":54,"adjMaxMagicAtk":99,"adjMinPhysicalArmor":30,"adjMaxPhysicalArmor":30,"adjMinMagicArmor":30,"adjMaxMagicArmor":30,"adjHit":34,"adjDodge":23,"adjRealDmg":4,"adjRealDmgDef":5,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":5,"adjDebilityAnti":11})
    }),
    51009241: _tools.RODict({
        "propID": 51009241,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":941,"adjMinPhysicalAtk":63,"adjMaxPhysicalAtk":115,"adjMinMagicAtk":63,"adjMaxMagicAtk":115,"adjMinPhysicalArmor":31,"adjMaxPhysicalArmor":31,"adjMinMagicArmor":31,"adjMaxMagicArmor":31,"adjHit":38,"adjDodge":23,"adjRealDmg":4,"adjRealDmgDef":5,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":5,"adjDebilityAnti":11})
    }),
    51009242: _tools.RODict({
        "propID": 51009242,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":989,"adjMinPhysicalAtk":64,"adjMaxPhysicalAtk":115,"adjMinMagicAtk":64,"adjMaxMagicAtk":115,"adjMinPhysicalArmor":32,"adjMaxPhysicalArmor":32,"adjMinMagicArmor":32,"adjMaxMagicArmor":32,"adjHit":38,"adjDodge":23,"adjRealDmg":5,"adjRealDmgDef":5,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":5,"adjDebilityAnti":11})
    }),
    51009243: _tools.RODict({
        "propID": 51009243,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1056,"adjMinPhysicalAtk":64,"adjMaxPhysicalAtk":116,"adjMinMagicAtk":64,"adjMaxMagicAtk":116,"adjMinPhysicalArmor":34,"adjMaxPhysicalArmor":34,"adjMinMagicArmor":34,"adjMaxMagicArmor":34,"adjHit":38,"adjDodge":25,"adjRealDmg":5,"adjRealDmgDef":6,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":5,"adjDebilityAnti":12})
    }),
    51009244: _tools.RODict({
        "propID": 51009244,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1064,"adjMinPhysicalAtk":65,"adjMaxPhysicalAtk":118,"adjMinMagicAtk":65,"adjMaxMagicAtk":118,"adjMinPhysicalArmor":35,"adjMaxPhysicalArmor":35,"adjMinMagicArmor":35,"adjMaxMagicArmor":35,"adjHit":38,"adjDodge":26,"adjRealDmg":5,"adjRealDmgDef":6,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":6,"adjDebilityAnti":12})
    }),
    51009245: _tools.RODict({
        "propID": 51009245,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1071,"adjMinPhysicalAtk":65,"adjMaxPhysicalAtk":120,"adjMinMagicAtk":65,"adjMaxMagicAtk":120,"adjMinPhysicalArmor":37,"adjMaxPhysicalArmor":37,"adjMinMagicArmor":37,"adjMaxMagicArmor":37,"adjHit":38,"adjDodge":26,"adjRealDmg":5,"adjRealDmgDef":6,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":6,"adjDebilityAnti":12})
    }),
    51009246: _tools.RODict({
        "propID": 51009246,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1105,"adjMinPhysicalAtk":71,"adjMaxPhysicalAtk":132,"adjMinMagicAtk":71,"adjMaxMagicAtk":132,"adjMinPhysicalArmor":37,"adjMaxPhysicalArmor":37,"adjMinMagicArmor":37,"adjMaxMagicArmor":37,"adjHit":43,"adjDodge":26,"adjRealDmg":5,"adjRealDmgDef":6,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":6,"adjDebilityAnti":12})
    }),
    51009247: _tools.RODict({
        "propID": 51009247,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1130,"adjMinPhysicalAtk":71,"adjMaxPhysicalAtk":132,"adjMinMagicAtk":71,"adjMaxMagicAtk":132,"adjMinPhysicalArmor":40,"adjMaxPhysicalArmor":40,"adjMinMagicArmor":40,"adjMaxMagicArmor":40,"adjHit":43,"adjDodge":26,"adjRealDmg":6,"adjRealDmgDef":6,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":6,"adjDebilityAnti":12})
    }),
    51009248: _tools.RODict({
        "propID": 51009248,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1198,"adjMinPhysicalAtk":71,"adjMaxPhysicalAtk":132,"adjMinMagicAtk":71,"adjMaxMagicAtk":132,"adjMinPhysicalArmor":40,"adjMaxPhysicalArmor":40,"adjMinMagicArmor":40,"adjMaxMagicArmor":40,"adjHit":43,"adjDodge":30,"adjRealDmg":6,"adjRealDmgDef":7,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":6,"adjDebilityAnti":13})
    }),
    51009249: _tools.RODict({
        "propID": 51009249,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1235,"adjMinPhysicalAtk":74,"adjMaxPhysicalAtk":139,"adjMinMagicAtk":74,"adjMaxMagicAtk":139,"adjMinPhysicalArmor":42,"adjMaxPhysicalArmor":42,"adjMinMagicArmor":42,"adjMaxMagicArmor":42,"adjHit":45,"adjDodge":30,"adjRealDmg":6,"adjRealDmgDef":7,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":7,"adjDebilityAnti":13})
    }),
    51009250: _tools.RODict({
        "propID": 51009250,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1243,"adjMinPhysicalAtk":75,"adjMaxPhysicalAtk":143,"adjMinMagicAtk":75,"adjMaxMagicAtk":143,"adjMinPhysicalArmor":44,"adjMaxPhysicalArmor":44,"adjMinMagicArmor":44,"adjMaxMagicArmor":44,"adjHit":45,"adjDodge":32,"adjRealDmg":6,"adjRealDmgDef":7,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":7,"adjDebilityAnti":13})
    }),
    51009251: _tools.RODict({
        "propID": 51009251,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1250,"adjMinPhysicalAtk":81,"adjMaxPhysicalAtk":153,"adjMinMagicAtk":81,"adjMaxMagicAtk":153,"adjMinPhysicalArmor":45,"adjMaxPhysicalArmor":45,"adjMinMagicArmor":45,"adjMaxMagicArmor":45,"adjHit":48,"adjDodge":32,"adjRealDmg":6,"adjRealDmgDef":7,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":7,"adjDebilityAnti":13})
    }),
    51009252: _tools.RODict({
        "propID": 51009252,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1294,"adjMinPhysicalAtk":84,"adjMaxPhysicalAtk":157,"adjMinMagicAtk":84,"adjMaxMagicAtk":157,"adjMinPhysicalArmor":46,"adjMaxPhysicalArmor":46,"adjMinMagicArmor":46,"adjMaxMagicArmor":46,"adjHit":51,"adjDodge":32,"adjRealDmg":7,"adjRealDmgDef":7,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":7,"adjDebilityAnti":13})
    }),
    51009253: _tools.RODict({
        "propID": 51009253,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1455,"adjMinPhysicalAtk":84,"adjMaxPhysicalAtk":158,"adjMinMagicAtk":84,"adjMaxMagicAtk":158,"adjMinPhysicalArmor":48,"adjMaxPhysicalArmor":48,"adjMinMagicArmor":48,"adjMaxMagicArmor":48,"adjHit":51,"adjDodge":34,"adjRealDmg":7,"adjRealDmgDef":8,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":7,"adjDebilityAnti":14})
    }),
    51009254: _tools.RODict({
        "propID": 51009254,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1463,"adjMinPhysicalAtk":85,"adjMaxPhysicalAtk":160,"adjMinMagicAtk":85,"adjMaxMagicAtk":160,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":50,"adjMaxMagicArmor":50,"adjHit":51,"adjDodge":34,"adjRealDmg":7,"adjRealDmgDef":8,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":8,"adjDebilityAnti":14})
    }),
    51009255: _tools.RODict({
        "propID": 51009255,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1470,"adjMinPhysicalAtk":86,"adjMaxPhysicalAtk":163,"adjMinMagicAtk":86,"adjMaxMagicAtk":163,"adjMinPhysicalArmor":52,"adjMaxPhysicalArmor":52,"adjMinMagicArmor":52,"adjMaxMagicArmor":52,"adjHit":51,"adjDodge":37,"adjRealDmg":7,"adjRealDmgDef":8,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":8,"adjDebilityAnti":14})
    }),
    51009256: _tools.RODict({
        "propID": 51009256,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1478,"adjMinPhysicalAtk":93,"adjMaxPhysicalAtk":175,"adjMinMagicAtk":93,"adjMaxMagicAtk":175,"adjMinPhysicalArmor":52,"adjMaxPhysicalArmor":52,"adjMinMagicArmor":52,"adjMaxMagicArmor":52,"adjHit":54,"adjDodge":37,"adjRealDmg":7,"adjRealDmgDef":8,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":8,"adjDebilityAnti":14})
    }),
    51009257: _tools.RODict({
        "propID": 51009257,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1521,"adjMinPhysicalAtk":95,"adjMaxPhysicalAtk":180,"adjMinMagicAtk":95,"adjMaxMagicAtk":180,"adjMinPhysicalArmor":54,"adjMaxPhysicalArmor":54,"adjMinMagicArmor":54,"adjMaxMagicArmor":54,"adjHit":57,"adjDodge":37,"adjRealDmg":8,"adjRealDmgDef":8,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":8,"adjDebilityAnti":14})
    }),
    51009258: _tools.RODict({
        "propID": 51009258,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1694,"adjMinPhysicalAtk":96,"adjMaxPhysicalAtk":180,"adjMinMagicAtk":96,"adjMaxMagicAtk":180,"adjMinPhysicalArmor":55,"adjMaxPhysicalArmor":55,"adjMinMagicArmor":55,"adjMaxMagicArmor":55,"adjHit":57,"adjDodge":39,"adjRealDmg":8,"adjRealDmgDef":9,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":8,"adjDebilityAnti":15})
    }),
    51009259: _tools.RODict({
        "propID": 51009259,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1701,"adjMinPhysicalAtk":97,"adjMaxPhysicalAtk":186,"adjMinMagicAtk":97,"adjMaxMagicAtk":186,"adjMinPhysicalArmor":59,"adjMaxPhysicalArmor":59,"adjMinMagicArmor":59,"adjMaxMagicArmor":59,"adjHit":57,"adjDodge":39,"adjRealDmg":8,"adjRealDmgDef":9,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":9,"adjDebilityAnti":15})
    }),
    51009260: _tools.RODict({
        "propID": 51009260,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1709,"adjMinPhysicalAtk":98,"adjMaxPhysicalAtk":191,"adjMinMagicAtk":98,"adjMaxMagicAtk":191,"adjMinPhysicalArmor":60,"adjMaxPhysicalArmor":60,"adjMinMagicArmor":60,"adjMaxMagicArmor":60,"adjHit":57,"adjDodge":42,"adjRealDmg":8,"adjRealDmgDef":9,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":9,"adjDebilityAnti":15})
    }),
    51009261: _tools.RODict({
        "propID": 51009261,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1716,"adjMinPhysicalAtk":110,"adjMaxPhysicalAtk":212,"adjMinMagicAtk":110,"adjMaxMagicAtk":212,"adjMinPhysicalArmor":61,"adjMaxPhysicalArmor":61,"adjMinMagicArmor":61,"adjMaxMagicArmor":61,"adjHit":66,"adjDodge":42,"adjRealDmg":8,"adjRealDmgDef":9,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":9,"adjDebilityAnti":15})
    }),
    51009262: _tools.RODict({
        "propID": 51009262,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1796,"adjMinPhysicalAtk":114,"adjMaxPhysicalAtk":217,"adjMinMagicAtk":114,"adjMaxMagicAtk":217,"adjMinPhysicalArmor":65,"adjMaxPhysicalArmor":65,"adjMinMagicArmor":65,"adjMaxMagicArmor":65,"adjHit":69,"adjDodge":42,"adjRealDmg":10,"adjRealDmgDef":9,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":9,"adjDebilityAnti":15})
    }),
    51009263: _tools.RODict({
        "propID": 51009263,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2099,"adjMinPhysicalAtk":114,"adjMaxPhysicalAtk":218,"adjMinMagicAtk":114,"adjMaxMagicAtk":218,"adjMinPhysicalArmor":68,"adjMaxPhysicalArmor":68,"adjMinMagicArmor":68,"adjMaxMagicArmor":68,"adjHit":69,"adjDodge":48,"adjRealDmg":10,"adjRealDmgDef":11,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":9,"adjDebilityAnti":17})
    }),
    51009264: _tools.RODict({
        "propID": 51009264,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2107,"adjMinPhysicalAtk":116,"adjMaxPhysicalAtk":226,"adjMinMagicAtk":116,"adjMaxMagicAtk":226,"adjMinPhysicalArmor":71,"adjMaxPhysicalArmor":71,"adjMinMagicArmor":71,"adjMaxMagicArmor":71,"adjHit":69,"adjDodge":48,"adjRealDmg":10,"adjRealDmgDef":11,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":11,"adjDebilityAnti":17})
    }),
    51009265: _tools.RODict({
        "propID": 51009265,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2114,"adjMinPhysicalAtk":117,"adjMaxPhysicalAtk":235,"adjMinMagicAtk":117,"adjMaxMagicAtk":235,"adjMinPhysicalArmor":73,"adjMaxPhysicalArmor":73,"adjMinMagicArmor":73,"adjMaxMagicArmor":73,"adjHit":69,"adjDodge":52,"adjRealDmg":10,"adjRealDmgDef":11,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":11,"adjDebilityAnti":17})
    }),
    51009266: _tools.RODict({
        "propID": 51009266,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2122,"adjMinPhysicalAtk":127,"adjMaxPhysicalAtk":252,"adjMinMagicAtk":127,"adjMaxMagicAtk":252,"adjMinPhysicalArmor":73,"adjMaxPhysicalArmor":73,"adjMinMagicArmor":73,"adjMaxMagicArmor":73,"adjHit":72,"adjDodge":52,"adjRealDmg":10,"adjRealDmgDef":11,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":11,"adjDebilityAnti":17})
    }),
    51009267: _tools.RODict({
        "propID": 51009267,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2165,"adjMinPhysicalAtk":131,"adjMaxPhysicalAtk":258,"adjMinMagicAtk":131,"adjMaxMagicAtk":258,"adjMinPhysicalArmor":77,"adjMaxPhysicalArmor":77,"adjMinMagicArmor":77,"adjMaxMagicArmor":77,"adjHit":75,"adjDodge":52,"adjRealDmg":12,"adjRealDmgDef":11,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":11,"adjDebilityAnti":17})
    }),
    51009268: _tools.RODict({
        "propID": 51009268,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2360,"adjMinPhysicalAtk":131,"adjMaxPhysicalAtk":258,"adjMinMagicAtk":131,"adjMaxMagicAtk":258,"adjMinPhysicalArmor":79,"adjMaxPhysicalArmor":79,"adjMinMagicArmor":79,"adjMaxMagicArmor":79,"adjHit":75,"adjDodge":54,"adjRealDmg":12,"adjRealDmgDef":13,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":11,"adjDebilityAnti":18})
    }),
    51009269: _tools.RODict({
        "propID": 51009269,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2368,"adjMinPhysicalAtk":132,"adjMaxPhysicalAtk":265,"adjMinMagicAtk":132,"adjMaxMagicAtk":265,"adjMinPhysicalArmor":84,"adjMaxPhysicalArmor":84,"adjMinMagicArmor":84,"adjMaxMagicArmor":84,"adjHit":75,"adjDodge":54,"adjRealDmg":12,"adjRealDmgDef":13,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":12,"adjDebilityAnti":18})
    }),
    51009270: _tools.RODict({
        "propID": 51009270,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2383,"adjMinPhysicalAtk":134,"adjMaxPhysicalAtk":271,"adjMinMagicAtk":134,"adjMaxMagicAtk":271,"adjMinPhysicalArmor":86,"adjMaxPhysicalArmor":86,"adjMinMagicArmor":86,"adjMaxMagicArmor":86,"adjHit":75,"adjDodge":58,"adjRealDmg":12,"adjRealDmgDef":13,"adjMonsterDmgAnti":0.5,"adjDebilityEnh":12,"adjDebilityAnti":18})
    }),
    51011001: _tools.RODict({
        "propID": 51011001,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2944350,"adjMinPhysicalAtk":37,"adjMaxPhysicalAtk":41,"adjMinMagicAtk":37,"adjMaxMagicAtk":41,"adjMinPhysicalArmor":2,"adjMaxPhysicalArmor":2,"adjMinMagicArmor":2,"adjMaxMagicArmor":2,"adjHit":73,"adjDodge":4,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011002: _tools.RODict({
        "propID": 51011002,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":14050620,"adjMinPhysicalAtk":39,"adjMaxPhysicalAtk":43,"adjMinMagicAtk":39,"adjMaxMagicAtk":43,"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjHit":73,"adjDodge":6,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011003: _tools.RODict({
        "propID": 51011003,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":14390055,"adjMinPhysicalAtk":41,"adjMaxPhysicalAtk":46,"adjMinMagicAtk":41,"adjMaxMagicAtk":46,"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjHit":73,"adjDodge":6,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011004: _tools.RODict({
        "propID": 51011004,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":14840055,"adjMinPhysicalAtk":55,"adjMaxPhysicalAtk":61,"adjMinMagicAtk":55,"adjMaxMagicAtk":61,"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjHit":73,"adjDodge":6,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011005: _tools.RODict({
        "propID": 51011005,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":15179490,"adjMinPhysicalAtk":58,"adjMaxPhysicalAtk":64,"adjMinMagicAtk":58,"adjMaxMagicAtk":64,"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjHit":73,"adjDodge":6,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011006: _tools.RODict({
        "propID": 51011006,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":14729490,"adjMinPhysicalAtk":75,"adjMaxPhysicalAtk":83,"adjMinMagicAtk":75,"adjMaxMagicAtk":83,"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10,"adjHit":73,"adjDodge":6,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011007: _tools.RODict({
        "propID": 51011007,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":15518925,"adjMinPhysicalAtk":77,"adjMaxPhysicalAtk":86,"adjMinMagicAtk":77,"adjMaxMagicAtk":86,"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10,"adjHit":73,"adjDodge":6,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011008: _tools.RODict({
        "propID": 51011008,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":15518925,"adjMinPhysicalAtk":94,"adjMaxPhysicalAtk":104,"adjMinMagicAtk":94,"adjMaxMagicAtk":104,"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10,"adjHit":77,"adjDodge":10,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011009: _tools.RODict({
        "propID": 51011009,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":15858360,"adjMinPhysicalAtk":96,"adjMaxPhysicalAtk":107,"adjMinMagicAtk":96,"adjMaxMagicAtk":107,"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10,"adjHit":77,"adjDodge":10,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011010: _tools.RODict({
        "propID": 51011010,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":17444970,"adjMinPhysicalAtk":98,"adjMaxPhysicalAtk":109,"adjMinMagicAtk":98,"adjMaxMagicAtk":109,"adjMinPhysicalArmor":12,"adjMaxPhysicalArmor":12,"adjMinMagicArmor":12,"adjMaxMagicArmor":12,"adjHit":77,"adjDodge":10,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011011: _tools.RODict({
        "propID": 51011011,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":17944249,"adjMinPhysicalAtk":103,"adjMaxPhysicalAtk":114,"adjMinMagicAtk":103,"adjMaxMagicAtk":114,"adjMinPhysicalArmor":12,"adjMaxPhysicalArmor":12,"adjMinMagicArmor":12,"adjMaxMagicArmor":12,"adjHit":77,"adjDodge":10,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011012: _tools.RODict({
        "propID": 51011012,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":18554093,"adjMinPhysicalAtk":107,"adjMaxPhysicalAtk":119,"adjMinMagicAtk":107,"adjMaxMagicAtk":119,"adjMinPhysicalArmor":12,"adjMaxPhysicalArmor":12,"adjMinMagicArmor":12,"adjMaxMagicArmor":12,"adjHit":77,"adjDodge":10,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011013: _tools.RODict({
        "propID": 51011013,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":19063555,"adjMinPhysicalAtk":111,"adjMaxPhysicalAtk":123,"adjMinMagicAtk":111,"adjMaxMagicAtk":123,"adjMinPhysicalArmor":12,"adjMaxPhysicalArmor":12,"adjMinMagicArmor":12,"adjMaxMagicArmor":12,"adjHit":78,"adjDodge":11,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011014: _tools.RODict({
        "propID": 51011014,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":19208794,"adjMinPhysicalAtk":113,"adjMaxPhysicalAtk":125,"adjMinMagicAtk":113,"adjMaxMagicAtk":125,"adjMinPhysicalArmor":13,"adjMaxPhysicalArmor":13,"adjMinMagicArmor":13,"adjMaxMagicArmor":13,"adjHit":78,"adjDodge":11,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011015: _tools.RODict({
        "propID": 51011015,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":23288006,"adjMinPhysicalAtk":115,"adjMaxPhysicalAtk":128,"adjMinMagicAtk":115,"adjMaxMagicAtk":128,"adjMinPhysicalArmor":13,"adjMaxPhysicalArmor":13,"adjMinMagicArmor":13,"adjMaxMagicArmor":13,"adjHit":78,"adjDodge":11,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011016: _tools.RODict({
        "propID": 51011016,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":23457083,"adjMinPhysicalAtk":121,"adjMaxPhysicalAtk":134,"adjMinMagicAtk":121,"adjMaxMagicAtk":134,"adjMinPhysicalArmor":14,"adjMaxPhysicalArmor":14,"adjMinMagicArmor":14,"adjMaxMagicArmor":14,"adjHit":78,"adjDodge":11,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011017: _tools.RODict({
        "propID": 51011017,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":24011854,"adjMinPhysicalAtk":126,"adjMaxPhysicalAtk":140,"adjMinMagicAtk":126,"adjMaxMagicAtk":140,"adjMinPhysicalArmor":14,"adjMaxPhysicalArmor":14,"adjMinMagicArmor":14,"adjMaxMagicArmor":14,"adjHit":78,"adjDodge":11,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011018: _tools.RODict({
        "propID": 51011018,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":24656825,"adjMinPhysicalAtk":129,"adjMaxPhysicalAtk":143,"adjMinMagicAtk":129,"adjMaxMagicAtk":143,"adjMinPhysicalArmor":14,"adjMaxPhysicalArmor":14,"adjMinMagicArmor":14,"adjMaxMagicArmor":14,"adjHit":79,"adjDodge":12,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011019: _tools.RODict({
        "propID": 51011019,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":25221780,"adjMinPhysicalAtk":131,"adjMaxPhysicalAtk":146,"adjMinMagicAtk":131,"adjMaxMagicAtk":146,"adjMinPhysicalArmor":14,"adjMaxPhysicalArmor":14,"adjMinMagicArmor":14,"adjMaxMagicArmor":14,"adjHit":79,"adjDodge":12,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011020: _tools.RODict({
        "propID": 51011020,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":27615416,"adjMinPhysicalAtk":133,"adjMaxPhysicalAtk":148,"adjMinMagicAtk":133,"adjMaxMagicAtk":148,"adjMinPhysicalArmor":15,"adjMaxPhysicalArmor":15,"adjMinMagicArmor":15,"adjMaxMagicArmor":15,"adjHit":79,"adjDodge":12,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011021: _tools.RODict({
        "propID": 51011021,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":28533692,"adjMinPhysicalAtk":149,"adjMaxPhysicalAtk":165,"adjMinMagicAtk":149,"adjMaxMagicAtk":165,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjHit":79,"adjDodge":12,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011022: _tools.RODict({
        "propID": 51011022,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":29200212,"adjMinPhysicalAtk":155,"adjMaxPhysicalAtk":172,"adjMinMagicAtk":155,"adjMaxMagicAtk":172,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjHit":83,"adjDodge":16,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011023: _tools.RODict({
        "propID": 51011023,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":31276040,"adjMinPhysicalAtk":159,"adjMaxPhysicalAtk":177,"adjMinMagicAtk":159,"adjMaxMagicAtk":177,"adjMinPhysicalArmor":17,"adjMaxPhysicalArmor":17,"adjMinMagicArmor":17,"adjMaxMagicArmor":17,"adjHit":83,"adjDodge":16,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011024: _tools.RODict({
        "propID": 51011024,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":32989855,"adjMinPhysicalAtk":161,"adjMaxPhysicalAtk":179,"adjMinMagicAtk":161,"adjMaxMagicAtk":179,"adjMinPhysicalArmor":18,"adjMaxPhysicalArmor":18,"adjMinMagicArmor":18,"adjMaxMagicArmor":18,"adjHit":83,"adjDodge":16,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011025: _tools.RODict({
        "propID": 51011025,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":38498177,"adjMinPhysicalAtk":172,"adjMaxPhysicalAtk":191,"adjMinMagicAtk":172,"adjMaxMagicAtk":191,"adjMinPhysicalArmor":20,"adjMaxPhysicalArmor":20,"adjMinMagicArmor":20,"adjMaxMagicArmor":20,"adjHit":83,"adjDodge":16,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011026: _tools.RODict({
        "propID": 51011026,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":39156161,"adjMinPhysicalAtk":176,"adjMaxPhysicalAtk":196,"adjMinMagicAtk":176,"adjMaxMagicAtk":196,"adjMinPhysicalArmor":21,"adjMaxPhysicalArmor":21,"adjMinMagicArmor":21,"adjMaxMagicArmor":21,"adjHit":85,"adjDodge":18,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011027: _tools.RODict({
        "propID": 51011027,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":40728785,"adjMinPhysicalAtk":179,"adjMaxPhysicalAtk":199,"adjMinMagicAtk":179,"adjMaxMagicAtk":199,"adjMinPhysicalArmor":21,"adjMaxPhysicalArmor":21,"adjMinMagicArmor":21,"adjMaxMagicArmor":21,"adjHit":85,"adjDodge":18,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011028: _tools.RODict({
        "propID": 51011028,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":42978796,"adjMinPhysicalAtk":181,"adjMaxPhysicalAtk":201,"adjMinMagicAtk":181,"adjMaxMagicAtk":201,"adjMinPhysicalArmor":22,"adjMaxPhysicalArmor":22,"adjMinMagicArmor":22,"adjMaxMagicArmor":22,"adjHit":85,"adjDodge":18,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011029: _tools.RODict({
        "propID": 51011029,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":49286239,"adjMinPhysicalAtk":190,"adjMaxPhysicalAtk":211,"adjMinMagicAtk":190,"adjMaxMagicAtk":211,"adjMinPhysicalArmor":23,"adjMaxPhysicalArmor":23,"adjMinMagicArmor":23,"adjMaxMagicArmor":23,"adjHit":85,"adjDodge":18,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011030: _tools.RODict({
        "propID": 51011030,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":50384538,"adjMinPhysicalAtk":195,"adjMaxPhysicalAtk":217,"adjMinMagicAtk":195,"adjMaxMagicAtk":217,"adjMinPhysicalArmor":24,"adjMaxPhysicalArmor":24,"adjMinMagicArmor":24,"adjMaxMagicArmor":24,"adjHit":87,"adjDodge":20,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011031: _tools.RODict({
        "propID": 51011031,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":53667991,"adjMinPhysicalAtk":198,"adjMaxPhysicalAtk":220,"adjMinMagicAtk":198,"adjMaxMagicAtk":220,"adjMinPhysicalArmor":24,"adjMaxPhysicalArmor":24,"adjMinMagicArmor":24,"adjMaxMagicArmor":24,"adjHit":87,"adjDodge":20,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011032: _tools.RODict({
        "propID": 51011032,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":56850498,"adjMinPhysicalAtk":200,"adjMaxPhysicalAtk":222,"adjMinMagicAtk":200,"adjMaxMagicAtk":222,"adjMinPhysicalArmor":25,"adjMaxPhysicalArmor":25,"adjMinMagicArmor":25,"adjMaxMagicArmor":25,"adjHit":87,"adjDodge":20,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011033: _tools.RODict({
        "propID": 51011033,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":62433773,"adjMinPhysicalAtk":215,"adjMaxPhysicalAtk":239,"adjMinMagicAtk":215,"adjMaxMagicAtk":239,"adjMinPhysicalArmor":27,"adjMaxPhysicalArmor":27,"adjMinMagicArmor":27,"adjMaxMagicArmor":27,"adjHit":87,"adjDodge":20,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011034: _tools.RODict({
        "propID": 51011034,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":64152508,"adjMinPhysicalAtk":221,"adjMaxPhysicalAtk":245,"adjMinMagicAtk":221,"adjMaxMagicAtk":245,"adjMinPhysicalArmor":27,"adjMaxPhysicalArmor":27,"adjMinMagicArmor":27,"adjMaxMagicArmor":27,"adjHit":89,"adjDodge":22,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011035: _tools.RODict({
        "propID": 51011035,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":66588413,"adjMinPhysicalAtk":225,"adjMaxPhysicalAtk":250,"adjMinMagicAtk":225,"adjMaxMagicAtk":250,"adjMinPhysicalArmor":28,"adjMaxPhysicalArmor":28,"adjMinMagicArmor":28,"adjMaxMagicArmor":28,"adjHit":89,"adjDodge":22,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011036: _tools.RODict({
        "propID": 51011036,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":68754096,"adjMinPhysicalAtk":227,"adjMaxPhysicalAtk":252,"adjMinMagicAtk":227,"adjMaxMagicAtk":252,"adjMinPhysicalArmor":28,"adjMaxPhysicalArmor":28,"adjMinMagicArmor":28,"adjMaxMagicArmor":28,"adjHit":89,"adjDodge":22,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011037: _tools.RODict({
        "propID": 51011037,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":74082264,"adjMinPhysicalAtk":230,"adjMaxPhysicalAtk":255,"adjMinMagicAtk":230,"adjMaxMagicAtk":255,"adjMinPhysicalArmor":30,"adjMaxPhysicalArmor":30,"adjMinMagicArmor":30,"adjMaxMagicArmor":30,"adjHit":90,"adjDodge":23,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011038: _tools.RODict({
        "propID": 51011038,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":74984486,"adjMinPhysicalAtk":258,"adjMaxPhysicalAtk":287,"adjMinMagicAtk":258,"adjMaxMagicAtk":287,"adjMinPhysicalArmor":30,"adjMaxPhysicalArmor":30,"adjMinMagicArmor":30,"adjMaxMagicArmor":30,"adjHit":90,"adjDodge":23,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011039: _tools.RODict({
        "propID": 51011039,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":77200322,"adjMinPhysicalAtk":275,"adjMaxPhysicalAtk":306,"adjMinMagicAtk":275,"adjMaxMagicAtk":306,"adjMinPhysicalArmor":30,"adjMaxPhysicalArmor":30,"adjMinMagicArmor":30,"adjMaxMagicArmor":30,"adjHit":96,"adjDodge":29,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011040: _tools.RODict({
        "propID": 51011040,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":86650569,"adjMinPhysicalAtk":278,"adjMaxPhysicalAtk":309,"adjMinMagicAtk":278,"adjMaxMagicAtk":309,"adjMinPhysicalArmor":32,"adjMaxPhysicalArmor":32,"adjMinMagicArmor":32,"adjMaxMagicArmor":32,"adjHit":96,"adjDodge":29,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011041: _tools.RODict({
        "propID": 51011041,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":98320766,"adjMinPhysicalAtk":281,"adjMaxPhysicalAtk":312,"adjMinMagicAtk":281,"adjMaxMagicAtk":312,"adjMinPhysicalArmor":38,"adjMaxPhysicalArmor":38,"adjMinMagicArmor":38,"adjMaxMagicArmor":38,"adjHit":96,"adjDodge":29,"adjRealDmg":1,"adjRealDmgDef":2})
    }),
    51011042: _tools.RODict({
        "propID": 51011042,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":99380466,"adjMinPhysicalAtk":295,"adjMaxPhysicalAtk":328,"adjMinMagicAtk":295,"adjMaxMagicAtk":328,"adjMinPhysicalArmor":38,"adjMaxPhysicalArmor":38,"adjMinMagicArmor":38,"adjMaxMagicArmor":38,"adjHit":96,"adjDodge":29,"adjRealDmg":2,"adjRealDmgDef":2})
    }),
    51011043: _tools.RODict({
        "propID": 51011043,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":100891615,"adjMinPhysicalAtk":315,"adjMaxPhysicalAtk":350,"adjMinMagicAtk":315,"adjMaxMagicAtk":350,"adjMinPhysicalArmor":38,"adjMaxPhysicalArmor":38,"adjMinMagicArmor":38,"adjMaxMagicArmor":38,"adjHit":98,"adjDodge":31,"adjRealDmg":2,"adjRealDmgDef":3})
    }),
    51011044: _tools.RODict({
        "propID": 51011044,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":103171082,"adjMinPhysicalAtk":319,"adjMaxPhysicalAtk":354,"adjMinMagicAtk":319,"adjMaxMagicAtk":354,"adjMinPhysicalArmor":39,"adjMaxPhysicalArmor":39,"adjMinMagicArmor":39,"adjMaxMagicArmor":39,"adjHit":99,"adjDodge":32,"adjRealDmg":2,"adjRealDmgDef":3})
    }),
    51011045: _tools.RODict({
        "propID": 51011045,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":106534440,"adjMinPhysicalAtk":323,"adjMaxPhysicalAtk":359,"adjMinMagicAtk":323,"adjMaxMagicAtk":359,"adjMinPhysicalArmor":39,"adjMaxPhysicalArmor":39,"adjMinMagicArmor":39,"adjMaxMagicArmor":39,"adjHit":99,"adjDodge":32,"adjRealDmg":2,"adjRealDmgDef":3})
    }),
    51011046: _tools.RODict({
        "propID": 51011046,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":116405111,"adjMinPhysicalAtk":331,"adjMaxPhysicalAtk":368,"adjMinMagicAtk":331,"adjMaxMagicAtk":368,"adjMinPhysicalArmor":42,"adjMaxPhysicalArmor":42,"adjMinMagicArmor":42,"adjMaxMagicArmor":42,"adjHit":99,"adjDodge":32,"adjRealDmg":3,"adjRealDmgDef":3})
    }),
    51011047: _tools.RODict({
        "propID": 51011047,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":118023851,"adjMinPhysicalAtk":342,"adjMaxPhysicalAtk":380,"adjMinMagicAtk":342,"adjMaxMagicAtk":380,"adjMinPhysicalArmor":42,"adjMaxPhysicalArmor":42,"adjMinMagicArmor":42,"adjMaxMagicArmor":42,"adjHit":99,"adjDodge":32,"adjRealDmg":3,"adjRealDmgDef":4})
    }),
    51011048: _tools.RODict({
        "propID": 51011048,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":118559959,"adjMinPhysicalAtk":359,"adjMaxPhysicalAtk":399,"adjMinMagicAtk":359,"adjMaxMagicAtk":399,"adjMinPhysicalArmor":43,"adjMaxPhysicalArmor":43,"adjMinMagicArmor":43,"adjMaxMagicArmor":43,"adjHit":103,"adjDodge":36,"adjRealDmg":3,"adjRealDmgDef":4})
    }),
    51011049: _tools.RODict({
        "propID": 51011049,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":125692473,"adjMinPhysicalAtk":371,"adjMaxPhysicalAtk":412,"adjMinMagicAtk":371,"adjMaxMagicAtk":412,"adjMinPhysicalArmor":44,"adjMaxPhysicalArmor":44,"adjMinMagicArmor":44,"adjMaxMagicArmor":44,"adjHit":103,"adjDodge":36,"adjRealDmg":4,"adjRealDmgDef":4})
    }),
    51011050: _tools.RODict({
        "propID": 51011050,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":129584565,"adjMinPhysicalAtk":377,"adjMaxPhysicalAtk":419,"adjMinMagicAtk":377,"adjMaxMagicAtk":419,"adjMinPhysicalArmor":45,"adjMaxPhysicalArmor":45,"adjMinMagicArmor":45,"adjMaxMagicArmor":45,"adjHit":105,"adjDodge":38,"adjRealDmg":4,"adjRealDmgDef":5})
    }),
    51011051: _tools.RODict({
        "propID": 51011051,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":138312125,"adjMinPhysicalAtk":380,"adjMaxPhysicalAtk":422,"adjMinMagicAtk":380,"adjMaxMagicAtk":422,"adjMinPhysicalArmor":49,"adjMaxPhysicalArmor":49,"adjMinMagicArmor":49,"adjMaxMagicArmor":49,"adjHit":105,"adjDodge":38,"adjRealDmg":4,"adjRealDmgDef":5})
    }),
    51011052: _tools.RODict({
        "propID": 51011052,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":142797278,"adjMinPhysicalAtk":393,"adjMaxPhysicalAtk":437,"adjMinMagicAtk":393,"adjMaxMagicAtk":437,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":50,"adjMaxMagicArmor":50,"adjHit":105,"adjDodge":38,"adjRealDmg":4,"adjRealDmgDef":5})
    }),
    51011053: _tools.RODict({
        "propID": 51011053,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":144573496,"adjMinPhysicalAtk":435,"adjMaxPhysicalAtk":483,"adjMinMagicAtk":435,"adjMaxMagicAtk":483,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":50,"adjMaxMagicArmor":50,"adjHit":107,"adjDodge":40,"adjRealDmg":5,"adjRealDmgDef":5})
    }),
    51011054: _tools.RODict({
        "propID": 51011054,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":147663648,"adjMinPhysicalAtk":441,"adjMaxPhysicalAtk":490,"adjMinMagicAtk":441,"adjMaxMagicAtk":490,"adjMinPhysicalArmor":51,"adjMaxPhysicalArmor":51,"adjMinMagicArmor":51,"adjMaxMagicArmor":51,"adjHit":107,"adjDodge":40,"adjRealDmg":5,"adjRealDmgDef":6})
    }),
    51011055: _tools.RODict({
        "propID": 51011055,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":151270925,"adjMinPhysicalAtk":446,"adjMaxPhysicalAtk":495,"adjMinMagicAtk":446,"adjMaxMagicAtk":495,"adjMinPhysicalArmor":52,"adjMaxPhysicalArmor":52,"adjMinMagicArmor":52,"adjMaxMagicArmor":52,"adjHit":110,"adjDodge":43,"adjRealDmg":5,"adjRealDmgDef":6})
    }),
    51011056: _tools.RODict({
        "propID": 51011056,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":161859285,"adjMinPhysicalAtk":447,"adjMaxPhysicalAtk":497,"adjMinMagicAtk":447,"adjMaxMagicAtk":497,"adjMinPhysicalArmor":56,"adjMaxPhysicalArmor":56,"adjMinMagicArmor":56,"adjMaxMagicArmor":56,"adjHit":110,"adjDodge":43,"adjRealDmg":5,"adjRealDmgDef":6})
    }),
    51011057: _tools.RODict({
        "propID": 51011057,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":167573502,"adjMinPhysicalAtk":462,"adjMaxPhysicalAtk":513,"adjMinMagicAtk":462,"adjMaxMagicAtk":513,"adjMinPhysicalArmor":57,"adjMaxPhysicalArmor":57,"adjMinMagicArmor":57,"adjMaxMagicArmor":57,"adjHit":110,"adjDodge":43,"adjRealDmg":5,"adjRealDmgDef":6})
    }),
    51011058: _tools.RODict({
        "propID": 51011058,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":168988968,"adjMinPhysicalAtk":505,"adjMaxPhysicalAtk":561,"adjMinMagicAtk":505,"adjMaxMagicAtk":561,"adjMinPhysicalArmor":57,"adjMaxPhysicalArmor":57,"adjMinMagicArmor":57,"adjMaxMagicArmor":57,"adjHit":112,"adjDodge":45,"adjRealDmg":6,"adjRealDmgDef":6})
    }),
    51011059: _tools.RODict({
        "propID": 51011059,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":175297274,"adjMinPhysicalAtk":514,"adjMaxPhysicalAtk":571,"adjMinMagicAtk":514,"adjMaxMagicAtk":571,"adjMinPhysicalArmor":58,"adjMaxPhysicalArmor":58,"adjMinMagicArmor":58,"adjMaxMagicArmor":58,"adjHit":112,"adjDodge":45,"adjRealDmg":6,"adjRealDmgDef":7})
    }),
    51011060: _tools.RODict({
        "propID": 51011060,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":181162103,"adjMinPhysicalAtk":518,"adjMaxPhysicalAtk":576,"adjMinMagicAtk":518,"adjMaxMagicAtk":576,"adjMinPhysicalArmor":59,"adjMaxPhysicalArmor":59,"adjMinMagicArmor":59,"adjMaxMagicArmor":59,"adjHit":115,"adjDodge":48,"adjRealDmg":6,"adjRealDmgDef":7})
    }),
    51011061: _tools.RODict({
        "propID": 51011061,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":199922864,"adjMinPhysicalAtk":521,"adjMaxPhysicalAtk":579,"adjMinMagicAtk":521,"adjMaxMagicAtk":579,"adjMinPhysicalArmor":66,"adjMaxPhysicalArmor":66,"adjMinMagicArmor":66,"adjMaxMagicArmor":66,"adjHit":115,"adjDodge":48,"adjRealDmg":6,"adjRealDmgDef":7})
    }),
    51011062: _tools.RODict({
        "propID": 51011062,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":205306481,"adjMinPhysicalAtk":548,"adjMaxPhysicalAtk":609,"adjMinMagicAtk":548,"adjMaxMagicAtk":609,"adjMinPhysicalArmor":68,"adjMaxPhysicalArmor":68,"adjMinMagicArmor":68,"adjMaxMagicArmor":68,"adjHit":115,"adjDodge":48,"adjRealDmg":6,"adjRealDmgDef":7})
    }),
    51011063: _tools.RODict({
        "propID": 51011063,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":207442964,"adjMinPhysicalAtk":626,"adjMaxPhysicalAtk":695,"adjMinMagicAtk":626,"adjMaxMagicAtk":695,"adjMinPhysicalArmor":68,"adjMaxPhysicalArmor":68,"adjMinMagicArmor":68,"adjMaxMagicArmor":68,"adjHit":121,"adjDodge":54,"adjRealDmg":7,"adjRealDmgDef":7})
    }),
    51011064: _tools.RODict({
        "propID": 51011064,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":217256915,"adjMinPhysicalAtk":634,"adjMaxPhysicalAtk":704,"adjMinMagicAtk":634,"adjMaxMagicAtk":704,"adjMinPhysicalArmor":69,"adjMaxPhysicalArmor":69,"adjMinMagicArmor":69,"adjMaxMagicArmor":69,"adjHit":121,"adjDodge":54,"adjRealDmg":7,"adjRealDmgDef":8})
    }),
    51011065: _tools.RODict({
        "propID": 51011065,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":227703398,"adjMinPhysicalAtk":639,"adjMaxPhysicalAtk":710,"adjMinMagicAtk":639,"adjMaxMagicAtk":710,"adjMinPhysicalArmor":70,"adjMaxPhysicalArmor":70,"adjMinMagicArmor":70,"adjMaxMagicArmor":70,"adjHit":125,"adjDodge":58,"adjRealDmg":7,"adjRealDmgDef":8})
    }),
    51011066: _tools.RODict({
        "propID": 51011066,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":243225374,"adjMinPhysicalAtk":641,"adjMaxPhysicalAtk":712,"adjMinMagicAtk":641,"adjMaxMagicAtk":712,"adjMinPhysicalArmor":76,"adjMaxPhysicalArmor":76,"adjMinMagicArmor":76,"adjMaxMagicArmor":76,"adjHit":125,"adjDodge":58,"adjRealDmg":7,"adjRealDmgDef":8})
    }),
    51011067: _tools.RODict({
        "propID": 51011067,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":250026082,"adjMinPhysicalAtk":658,"adjMaxPhysicalAtk":731,"adjMinMagicAtk":658,"adjMaxMagicAtk":731,"adjMinPhysicalArmor":78,"adjMaxPhysicalArmor":78,"adjMinMagicArmor":78,"adjMaxMagicArmor":78,"adjHit":125,"adjDodge":58,"adjRealDmg":7,"adjRealDmgDef":8})
    }),
    51011068: _tools.RODict({
        "propID": 51011068,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":251165567,"adjMinPhysicalAtk":707,"adjMaxPhysicalAtk":786,"adjMinMagicAtk":707,"adjMaxMagicAtk":786,"adjMinPhysicalArmor":79,"adjMaxPhysicalArmor":79,"adjMinMagicArmor":79,"adjMaxMagicArmor":79,"adjHit":127,"adjDodge":60,"adjRealDmg":8,"adjRealDmgDef":8})
    }),
    51011069: _tools.RODict({
        "propID": 51011069,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":260027673,"adjMinPhysicalAtk":718,"adjMaxPhysicalAtk":798,"adjMinMagicAtk":718,"adjMaxMagicAtk":798,"adjMinPhysicalArmor":79,"adjMaxPhysicalArmor":79,"adjMinMagicArmor":79,"adjMaxMagicArmor":79,"adjHit":127,"adjDodge":60,"adjRealDmg":8,"adjRealDmgDef":9})
    }),
    51011070: _tools.RODict({
        "propID": 51011070,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":267714936,"adjMinPhysicalAtk":725,"adjMaxPhysicalAtk":806,"adjMinMagicAtk":725,"adjMaxMagicAtk":806,"adjMinPhysicalArmor":80,"adjMaxPhysicalArmor":80,"adjMinMagicArmor":80,"adjMaxMagicArmor":80,"adjHit":131,"adjDodge":64,"adjRealDmg":8,"adjRealDmgDef":9})
    }),
    52009001: _tools.RODict({
        "propID": 52009001,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":200,"adjMinPhysicalAtk":4,"adjMaxPhysicalAtk":6,"adjMinMagicAtk":4,"adjMaxMagicAtk":6,"adjMinPhysicalArmor":2,"adjMaxPhysicalArmor":2,"adjMinMagicArmor":2,"adjMaxMagicArmor":2,"adjHit":68,"adjDodge":6,"adjRealDmgDef":2,"adjDebilityEnh":1})
    }),
    52009002: _tools.RODict({
        "propID": 52009002,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":10000,"adjMinPhysicalAtk":1,"adjMaxPhysicalAtk":1,"adjMinMagicAtk":1,"adjMaxMagicAtk":1,"adjMinPhysicalArmor":2,"adjMaxPhysicalArmor":2,"adjMinMagicArmor":2,"adjMaxMagicArmor":2,"adjHit":1,"adjDodge":1,"adjDebilityEnh":1})
    }),
    52009003: _tools.RODict({
        "propID": 52009003,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":240,"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":26,"adjMinMagicAtk":26,"adjMaxMagicAtk":26,"adjHit":1,"adjDodge":1})
    }),
    52009004: _tools.RODict({
        "propID": 52009004,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":252,"adjMinPhysicalAtk":27,"adjMaxPhysicalAtk":27,"adjMinMagicAtk":27,"adjMaxMagicAtk":27,"adjHit":1,"adjDodge":1})
    }),
    52009005: _tools.RODict({
        "propID": 52009005,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":160,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":21,"adjMinMagicAtk":21,"adjMaxMagicAtk":21,"adjHit":1,"adjDodge":1})
    }),
    52009006: _tools.RODict({
        "propID": 52009006,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1800,"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":30,"adjMinMagicAtk":30,"adjMaxMagicAtk":30,"adjHit":2,"adjDodge":2})
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
        "propList": _tools.RODict({"adjFullHp":2400,"adjMinPhysicalAtk":35,"adjMaxPhysicalAtk":35,"adjMinMagicAtk":35,"adjMaxMagicAtk":35,"adjMinPhysicalArmor":1,"adjMaxPhysicalArmor":1,"adjMinMagicArmor":1,"adjMaxMagicArmor":1,"adjHit":5,"adjDodge":5})
    }),
    52009011: _tools.RODict({
        "propID": 52009011,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1200,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":22,"adjMinMagicAtk":21,"adjMaxMagicAtk":22,"adjMinPhysicalArmor":2,"adjMaxPhysicalArmor":2,"adjMinMagicArmor":2,"adjMaxMagicArmor":2,"adjHit":10,"adjDodge":6,"adjRealDmgDef":4,"adjDebilityEnh":1,"adjDebilityAnti":1})
    }),
    51012001: _tools.RODict({
        "propID": 51012001,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":900,"adjMinPhysicalAtk":4,"adjMaxPhysicalAtk":6,"adjMinMagicAtk":4,"adjMaxMagicAtk":6,"adjMinPhysicalArmor":2,"adjMaxPhysicalArmor":2,"adjMinMagicArmor":2,"adjMaxMagicArmor":2,"adjHit":1,"adjDodge":1,"adjRealDmgDef":2,"adjDebilityEnh":1})
    }),
    51012002: _tools.RODict({
        "propID": 51012002,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4700,"adjMinPhysicalAtk":4,"adjMaxPhysicalAtk":7,"adjMinMagicAtk":4,"adjMaxMagicAtk":7,"adjMinPhysicalArmor":4,"adjMaxPhysicalArmor":4,"adjMinMagicArmor":4,"adjMaxMagicArmor":4,"adjHit":1,"adjDodge":1,"adjRealDmgDef":2,"adjDebilityEnh":1})
    }),
    51012003: _tools.RODict({
        "propID": 51012003,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4800,"adjMinPhysicalAtk":4,"adjMaxPhysicalAtk":7,"adjMinMagicAtk":4,"adjMaxMagicAtk":7,"adjMinPhysicalArmor":4,"adjMaxPhysicalArmor":4,"adjMinMagicArmor":4,"adjMaxMagicArmor":4,"adjHit":1,"adjDodge":1,"adjRealDmgDef":2,"adjDebilityEnh":1})
    }),
    51012004: _tools.RODict({
        "propID": 51012004,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4800,"adjMinPhysicalAtk":4,"adjMaxPhysicalAtk":7,"adjMinMagicAtk":4,"adjMaxMagicAtk":7,"adjMinPhysicalArmor":5,"adjMaxPhysicalArmor":5,"adjMinMagicArmor":5,"adjMaxMagicArmor":5,"adjHit":1,"adjDodge":1,"adjRealDmgDef":2,"adjDebilityEnh":1})
    }),
    51012005: _tools.RODict({
        "propID": 51012005,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4880,"adjMinPhysicalAtk":5,"adjMaxPhysicalAtk":8,"adjMinMagicAtk":5,"adjMaxMagicAtk":8,"adjMinPhysicalArmor":5,"adjMaxPhysicalArmor":5,"adjMinMagicArmor":5,"adjMaxMagicArmor":5,"adjHit":1,"adjDodge":1,"adjRealDmgDef":2,"adjDebilityEnh":1})
    }),
    51012006: _tools.RODict({
        "propID": 51012006,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4880,"adjMinPhysicalAtk":5,"adjMaxPhysicalAtk":8,"adjMinMagicAtk":5,"adjMaxMagicAtk":8,"adjMinPhysicalArmor":5,"adjMaxPhysicalArmor":5,"adjMinMagicArmor":5,"adjMaxMagicArmor":5,"adjHit":1,"adjDodge":1,"adjRealDmgDef":2,"adjDebilityEnh":1})
    }),
    51012007: _tools.RODict({
        "propID": 51012007,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4980,"adjMinPhysicalAtk":5,"adjMaxPhysicalAtk":8,"adjMinMagicAtk":5,"adjMaxMagicAtk":8,"adjMinPhysicalArmor":6,"adjMaxPhysicalArmor":6,"adjMinMagicArmor":6,"adjMaxMagicArmor":6,"adjHit":1,"adjDodge":1,"adjRealDmgDef":2,"adjDebilityEnh":1})
    }),
    51012008: _tools.RODict({
        "propID": 51012008,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4980,"adjMinPhysicalAtk":5,"adjMaxPhysicalAtk":8,"adjMinMagicAtk":5,"adjMaxMagicAtk":8,"adjMinPhysicalArmor":6,"adjMaxPhysicalArmor":6,"adjMinMagicArmor":6,"adjMaxMagicArmor":6,"adjHit":5,"adjDodge":5,"adjRealDmgDef":2,"adjDebilityEnh":1})
    }),
    51012009: _tools.RODict({
        "propID": 51012009,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5060,"adjMinPhysicalAtk":5,"adjMaxPhysicalAtk":8,"adjMinMagicAtk":5,"adjMaxMagicAtk":8,"adjMinPhysicalArmor":6,"adjMaxPhysicalArmor":6,"adjMinMagicArmor":6,"adjMaxMagicArmor":6,"adjHit":5,"adjDodge":5,"adjRealDmgDef":2,"adjDebilityEnh":1})
    }),
    51012010: _tools.RODict({
        "propID": 51012010,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5620,"adjMinPhysicalAtk":5,"adjMaxPhysicalAtk":8,"adjMinMagicAtk":5,"adjMaxMagicAtk":8,"adjMinPhysicalArmor":8,"adjMaxPhysicalArmor":8,"adjMinMagicArmor":8,"adjMaxMagicArmor":8,"adjHit":5,"adjDodge":5,"adjRealDmgDef":2,"adjDebilityEnh":1})
    }),
    51012011: _tools.RODict({
        "propID": 51012011,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5900,"adjMinPhysicalAtk":6,"adjMaxPhysicalAtk":11,"adjMinMagicAtk":6,"adjMaxMagicAtk":11,"adjMinPhysicalArmor":8,"adjMaxPhysicalArmor":8,"adjMinMagicArmor":8,"adjMaxMagicArmor":8,"adjHit":5,"adjDodge":5,"adjRealDmgDef":2,"adjDebilityEnh":1})
    }),
    51012012: _tools.RODict({
        "propID": 51012012,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":6080,"adjMinPhysicalAtk":6,"adjMaxPhysicalAtk":11,"adjMinMagicAtk":6,"adjMaxMagicAtk":11,"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjHit":5,"adjDodge":5,"adjRealDmgDef":2,"adjDebilityEnh":1})
    }),
    51012013: _tools.RODict({
        "propID": 51012013,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":6380,"adjMinPhysicalAtk":7,"adjMaxPhysicalAtk":12,"adjMinMagicAtk":7,"adjMaxMagicAtk":12,"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjHit":6,"adjDodge":6,"adjRealDmgDef":2,"adjDebilityEnh":1})
    }),
    51012014: _tools.RODict({
        "propID": 51012014,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":6560,"adjMinPhysicalAtk":7,"adjMaxPhysicalAtk":12,"adjMinMagicAtk":7,"adjMaxMagicAtk":12,"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10,"adjHit":6,"adjDodge":6,"adjRealDmgDef":2,"adjDebilityEnh":1})
    }),
    51012015: _tools.RODict({
        "propID": 51012015,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":7920,"adjMinPhysicalAtk":7,"adjMaxPhysicalAtk":13,"adjMinMagicAtk":7,"adjMaxMagicAtk":13,"adjMinPhysicalArmor":11,"adjMaxPhysicalArmor":11,"adjMinMagicArmor":11,"adjMaxMagicArmor":11,"adjHit":6,"adjDodge":6,"adjRealDmgDef":2,"adjDebilityEnh":1})
    }),
    51012016: _tools.RODict({
        "propID": 51012016,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":8140,"adjMinPhysicalAtk":7,"adjMaxPhysicalAtk":13,"adjMinMagicAtk":7,"adjMaxMagicAtk":13,"adjMinPhysicalArmor":12,"adjMaxPhysicalArmor":12,"adjMinMagicArmor":12,"adjMaxMagicArmor":12,"adjHit":6,"adjDodge":6,"adjRealDmgDef":2,"adjDebilityEnh":1})
    }),
    51012017: _tools.RODict({
        "propID": 51012017,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":8480,"adjMinPhysicalAtk":7,"adjMaxPhysicalAtk":13,"adjMinMagicAtk":7,"adjMaxMagicAtk":13,"adjMinPhysicalArmor":12,"adjMaxPhysicalArmor":12,"adjMinMagicArmor":12,"adjMaxMagicArmor":12,"adjHit":6,"adjDodge":6,"adjRealDmgDef":2,"adjDebilityEnh":1})
    }),
    51012018: _tools.RODict({
        "propID": 51012018,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":8720,"adjMinPhysicalAtk":8,"adjMaxPhysicalAtk":14,"adjMinMagicAtk":8,"adjMaxMagicAtk":14,"adjMinPhysicalArmor":13,"adjMaxPhysicalArmor":13,"adjMinMagicArmor":13,"adjMaxMagicArmor":13,"adjHit":7,"adjDodge":7,"adjRealDmgDef":2,"adjDebilityEnh":1})
    }),
    51012019: _tools.RODict({
        "propID": 51012019,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":9060,"adjMinPhysicalAtk":8,"adjMaxPhysicalAtk":14,"adjMinMagicAtk":8,"adjMaxMagicAtk":14,"adjMinPhysicalArmor":13,"adjMaxPhysicalArmor":13,"adjMinMagicArmor":13,"adjMaxMagicArmor":13,"adjHit":7,"adjDodge":7,"adjRealDmgDef":2,"adjDebilityEnh":1})
    }),
    51012020: _tools.RODict({
        "propID": 51012020,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":10020,"adjMinPhysicalAtk":8,"adjMaxPhysicalAtk":16,"adjMinMagicAtk":8,"adjMaxMagicAtk":16,"adjMinPhysicalArmor":17,"adjMaxPhysicalArmor":17,"adjMinMagicArmor":17,"adjMaxMagicArmor":17,"adjHit":7,"adjDodge":7,"adjRealDmgDef":2,"adjDebilityEnh":1})
    }),
    51012021: _tools.RODict({
        "propID": 51012021,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":10520,"adjMinPhysicalAtk":8,"adjMaxPhysicalAtk":16,"adjMinMagicAtk":8,"adjMaxMagicAtk":16,"adjMinPhysicalArmor":18,"adjMaxPhysicalArmor":18,"adjMinMagicArmor":18,"adjMaxMagicArmor":18,"adjHit":7,"adjDodge":7,"adjRealDmgDef":3,"adjDebilityEnh":1})
    }),
    51012022: _tools.RODict({
        "propID": 51012022,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":10780,"adjMinPhysicalAtk":10,"adjMaxPhysicalAtk":17,"adjMinMagicAtk":10,"adjMaxMagicAtk":17,"adjMinPhysicalArmor":19,"adjMaxPhysicalArmor":19,"adjMinMagicArmor":19,"adjMaxMagicArmor":19,"adjHit":11,"adjDodge":11,"adjRealDmgDef":3,"adjDebilityEnh":1})
    }),
    51012023: _tools.RODict({
        "propID": 51012023,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":11680,"adjMinPhysicalAtk":10,"adjMaxPhysicalAtk":18,"adjMinMagicAtk":10,"adjMaxMagicAtk":18,"adjMinPhysicalArmor":21,"adjMaxPhysicalArmor":21,"adjMinMagicArmor":21,"adjMaxMagicArmor":21,"adjHit":11,"adjDodge":11,"adjRealDmgDef":3,"adjDebilityEnh":1})
    }),
    51012024: _tools.RODict({
        "propID": 51012024,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":12480,"adjMinPhysicalAtk":10,"adjMaxPhysicalAtk":18,"adjMinMagicAtk":10,"adjMaxMagicAtk":18,"adjMinPhysicalArmor":23,"adjMaxPhysicalArmor":23,"adjMinMagicArmor":23,"adjMaxMagicArmor":23,"adjHit":11,"adjDodge":11,"adjRealDmgDef":3,"adjDebilityEnh":1})
    }),
    51012025: _tools.RODict({
        "propID": 51012025,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":14800,"adjMinPhysicalAtk":11,"adjMaxPhysicalAtk":19,"adjMinMagicAtk":11,"adjMaxMagicAtk":19,"adjMinPhysicalArmor":26,"adjMaxPhysicalArmor":26,"adjMinMagicArmor":26,"adjMaxMagicArmor":26,"adjHit":11,"adjDodge":11,"adjRealDmgDef":4,"adjDebilityEnh":1})
    }),
    51012026: _tools.RODict({
        "propID": 51012026,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":15120,"adjMinPhysicalAtk":11,"adjMaxPhysicalAtk":19,"adjMinMagicAtk":11,"adjMaxMagicAtk":19,"adjMinPhysicalArmor":28,"adjMaxPhysicalArmor":28,"adjMinMagicArmor":28,"adjMaxMagicArmor":28,"adjHit":14,"adjDodge":14,"adjRealDmgDef":4,"adjDebilityEnh":1})
    }),
    51012027: _tools.RODict({
        "propID": 51012027,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":15600,"adjMinPhysicalAtk":11,"adjMaxPhysicalAtk":20,"adjMinMagicAtk":11,"adjMaxMagicAtk":20,"adjMinPhysicalArmor":30,"adjMaxPhysicalArmor":30,"adjMinMagicArmor":30,"adjMaxMagicArmor":30,"adjHit":14,"adjDodge":14,"adjRealDmgDef":4,"adjDebilityEnh":1})
    }),
    51012028: _tools.RODict({
        "propID": 51012028,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":16520,"adjMinPhysicalAtk":11,"adjMaxPhysicalAtk":20,"adjMinMagicAtk":11,"adjMaxMagicAtk":20,"adjMinPhysicalArmor":34,"adjMaxPhysicalArmor":34,"adjMinMagicArmor":34,"adjMaxMagicArmor":34,"adjHit":14,"adjDodge":14,"adjRealDmgDef":4,"adjDebilityEnh":1})
    }),
    51012029: _tools.RODict({
        "propID": 51012029,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":18920,"adjMinPhysicalAtk":12,"adjMaxPhysicalAtk":22,"adjMinMagicAtk":12,"adjMaxMagicAtk":22,"adjMinPhysicalArmor":38,"adjMaxPhysicalArmor":38,"adjMinMagicArmor":38,"adjMaxMagicArmor":38,"adjHit":14,"adjDodge":14,"adjRealDmgDef":5,"adjDebilityEnh":1})
    }),
    51012030: _tools.RODict({
        "propID": 51012030,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":19460,"adjMinPhysicalAtk":12,"adjMaxPhysicalAtk":22,"adjMinMagicAtk":12,"adjMaxMagicAtk":22,"adjMinPhysicalArmor":41,"adjMaxPhysicalArmor":41,"adjMinMagicArmor":41,"adjMaxMagicArmor":41,"adjHit":16,"adjDodge":16,"adjRealDmgDef":5,"adjDebilityEnh":1})
    }),
    51012031: _tools.RODict({
        "propID": 51012031,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":20620,"adjMinPhysicalAtk":13,"adjMaxPhysicalAtk":24,"adjMinMagicAtk":13,"adjMaxMagicAtk":24,"adjMinPhysicalArmor":44,"adjMaxPhysicalArmor":44,"adjMinMagicArmor":44,"adjMaxMagicArmor":44,"adjHit":16,"adjDodge":16,"adjRealDmgDef":5,"adjDebilityEnh":2})
    }),
    51012032: _tools.RODict({
        "propID": 51012032,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":21960,"adjMinPhysicalAtk":13,"adjMaxPhysicalAtk":24,"adjMinMagicAtk":13,"adjMaxMagicAtk":24,"adjMinPhysicalArmor":47,"adjMaxPhysicalArmor":47,"adjMinMagicArmor":47,"adjMaxMagicArmor":47,"adjHit":16,"adjDodge":16,"adjRealDmgDef":5,"adjDebilityEnh":2,"adjDebilityAnti":1})
    }),
    51012033: _tools.RODict({
        "propID": 51012033,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":24460,"adjMinPhysicalAtk":14,"adjMaxPhysicalAtk":25,"adjMinMagicAtk":14,"adjMaxMagicAtk":25,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":50,"adjMaxMagicArmor":50,"adjHit":17,"adjDodge":17,"adjRealDmgDef":6,"adjDebilityEnh":2,"adjDebilityAnti":1})
    }),
    51012034: _tools.RODict({
        "propID": 51012034,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":25100,"adjMinPhysicalAtk":14,"adjMaxPhysicalAtk":26,"adjMinMagicAtk":14,"adjMaxMagicAtk":26,"adjMinPhysicalArmor":52,"adjMaxPhysicalArmor":52,"adjMinMagicArmor":52,"adjMaxMagicArmor":52,"adjHit":19,"adjDodge":19,"adjRealDmgDef":6,"adjDebilityEnh":2,"adjDebilityAnti":1})
    }),
    51012035: _tools.RODict({
        "propID": 51012035,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":26220,"adjMinPhysicalAtk":16,"adjMaxPhysicalAtk":28,"adjMinMagicAtk":16,"adjMaxMagicAtk":28,"adjMinPhysicalArmor":56,"adjMaxPhysicalArmor":56,"adjMinMagicArmor":56,"adjMaxMagicArmor":56,"adjHit":19,"adjDodge":19,"adjRealDmgDef":6,"adjDebilityEnh":3,"adjDebilityAnti":1})
    }),
    51012036: _tools.RODict({
        "propID": 51012036,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":27040,"adjMinPhysicalAtk":16,"adjMaxPhysicalAtk":28,"adjMinMagicAtk":16,"adjMaxMagicAtk":28,"adjMinPhysicalArmor":59,"adjMaxPhysicalArmor":59,"adjMinMagicArmor":59,"adjMaxMagicArmor":59,"adjHit":19,"adjDodge":19,"adjRealDmgDef":6,"adjDebilityEnh":3,"adjDebilityAnti":2})
    }),
    51012037: _tools.RODict({
        "propID": 51012037,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":29760,"adjMinPhysicalAtk":16,"adjMaxPhysicalAtk":29,"adjMinMagicAtk":16,"adjMaxMagicAtk":29,"adjMinPhysicalArmor":60,"adjMaxPhysicalArmor":60,"adjMinMagicArmor":60,"adjMaxMagicArmor":60,"adjHit":21,"adjDodge":21,"adjRealDmgDef":6,"adjDebilityEnh":3,"adjDebilityAnti":2})
    }),
    51012038: _tools.RODict({
        "propID": 51012038,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":30280,"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":31,"adjMinMagicAtk":17,"adjMaxMagicAtk":31,"adjMinPhysicalArmor":62,"adjMaxPhysicalArmor":62,"adjMinMagicArmor":62,"adjMaxMagicArmor":62,"adjHit":21,"adjDodge":21,"adjRealDmgDef":7,"adjDebilityEnh":4,"adjDebilityAnti":2})
    }),
    51012039: _tools.RODict({
        "propID": 51012039,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":31340,"adjMinPhysicalAtk":18,"adjMaxPhysicalAtk":32,"adjMinMagicAtk":18,"adjMaxMagicAtk":32,"adjMinPhysicalArmor":63,"adjMaxPhysicalArmor":63,"adjMinMagicArmor":63,"adjMaxMagicArmor":63,"adjHit":29,"adjDodge":29,"adjRealDmg":5,"adjRealDmgDef":7,"adjDebilityEnh":4,"adjDebilityAnti":3})
    }),
    51012040: _tools.RODict({
        "propID": 51012040,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":35840,"adjMinPhysicalAtk":18,"adjMaxPhysicalAtk":34,"adjMinMagicAtk":18,"adjMaxMagicAtk":34,"adjMinPhysicalArmor":70,"adjMaxPhysicalArmor":70,"adjMinMagicArmor":70,"adjMaxMagicArmor":70,"adjHit":29,"adjDodge":29,"adjRealDmg":5,"adjRealDmgDef":7,"adjDebilityEnh":4,"adjDebilityAnti":3})
    }),
    51012041: _tools.RODict({
        "propID": 51012041,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":42340,"adjMinPhysicalAtk":19,"adjMaxPhysicalAtk":35,"adjMinMagicAtk":19,"adjMaxMagicAtk":35,"adjMinPhysicalArmor":80,"adjMaxPhysicalArmor":80,"adjMinMagicArmor":80,"adjMaxMagicArmor":80,"adjHit":29,"adjDodge":29,"adjRealDmg":5,"adjRealDmgDef":7,"adjDebilityEnh":4,"adjDebilityAnti":3})
    }),
    51012042: _tools.RODict({
        "propID": 51012042,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":43020,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":36,"adjMinMagicAtk":20,"adjMaxMagicAtk":36,"adjMinPhysicalArmor":81,"adjMaxPhysicalArmor":81,"adjMinMagicArmor":81,"adjMaxMagicArmor":81,"adjHit":29,"adjDodge":29,"adjRealDmg":5,"adjRealDmgDef":7,"adjDebilityEnh":5,"adjDebilityAnti":3})
    }),
    51012043: _tools.RODict({
        "propID": 51012043,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":43900,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":38,"adjMinMagicAtk":22,"adjMaxMagicAtk":38,"adjMinPhysicalArmor":82,"adjMaxPhysicalArmor":82,"adjMinMagicArmor":82,"adjMaxMagicArmor":82,"adjHit":31,"adjDodge":31,"adjRealDmg":5,"adjRealDmgDef":8,"adjDebilityEnh":5,"adjDebilityAnti":4})
    }),
    51012044: _tools.RODict({
        "propID": 51012044,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":45380,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":40,"adjMinMagicAtk":22,"adjMaxMagicAtk":40,"adjMinPhysicalArmor":84,"adjMaxPhysicalArmor":84,"adjMinMagicArmor":84,"adjMaxMagicArmor":84,"adjHit":34,"adjDodge":34,"adjRealDmg":6,"adjRealDmgDef":8,"adjDebilityEnh":5,"adjDebilityAnti":4})
    }),
    51012045: _tools.RODict({
        "propID": 51012045,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":47060,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":40,"adjMinMagicAtk":22,"adjMaxMagicAtk":40,"adjMinPhysicalArmor":86,"adjMaxPhysicalArmor":86,"adjMinMagicArmor":86,"adjMaxMagicArmor":86,"adjHit":34,"adjDodge":34,"adjRealDmg":6,"adjRealDmgDef":8,"adjDebilityEnh":5,"adjDebilityAnti":4})
    }),
    51012046: _tools.RODict({
        "propID": 51012046,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":52380,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":41,"adjMinMagicAtk":23,"adjMaxMagicAtk":41,"adjMinPhysicalArmor":91,"adjMaxPhysicalArmor":91,"adjMinMagicArmor":91,"adjMaxMagicArmor":91,"adjHit":34,"adjDodge":34,"adjRealDmg":6,"adjRealDmgDef":8,"adjDebilityEnh":5,"adjDebilityAnti":4})
    }),
    51012047: _tools.RODict({
        "propID": 51012047,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":53360,"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":44,"adjMinMagicAtk":24,"adjMaxMagicAtk":44,"adjMinPhysicalArmor":92,"adjMaxPhysicalArmor":92,"adjMinMagicArmor":92,"adjMaxMagicArmor":92,"adjHit":34,"adjDodge":34,"adjRealDmg":6,"adjRealDmgDef":8,"adjDebilityEnh":6,"adjDebilityAnti":4})
    }),
    51012048: _tools.RODict({
        "propID": 51012048,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":54160,"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":46,"adjMinMagicAtk":25,"adjMaxMagicAtk":46,"adjMinPhysicalArmor":93,"adjMaxPhysicalArmor":93,"adjMinMagicArmor":93,"adjMaxMagicArmor":93,"adjHit":36,"adjDodge":36,"adjRealDmg":6,"adjRealDmgDef":9,"adjDebilityEnh":6,"adjDebilityAnti":5})
    }),
    51012049: _tools.RODict({
        "propID": 51012049,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":57880,"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":47,"adjMinMagicAtk":25,"adjMaxMagicAtk":47,"adjMinPhysicalArmor":95,"adjMaxPhysicalArmor":95,"adjMinMagicArmor":95,"adjMaxMagicArmor":95,"adjHit":39,"adjDodge":39,"adjRealDmg":7,"adjRealDmgDef":9,"adjDebilityEnh":6,"adjDebilityAnti":5})
    }),
    51012050: _tools.RODict({
        "propID": 51012050,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":60200,"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":48,"adjMinMagicAtk":26,"adjMaxMagicAtk":48,"adjMinPhysicalArmor":97,"adjMaxPhysicalArmor":97,"adjMinMagicArmor":97,"adjMaxMagicArmor":97,"adjHit":39,"adjDodge":39,"adjRealDmg":7,"adjRealDmgDef":9,"adjDebilityEnh":6,"adjDebilityAnti":5})
    }),
    51012051: _tools.RODict({
        "propID": 51012051,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":65560,"adjMinPhysicalAtk":28,"adjMaxPhysicalAtk":50,"adjMinMagicAtk":28,"adjMaxMagicAtk":50,"adjMinPhysicalArmor":103,"adjMaxPhysicalArmor":103,"adjMinMagicArmor":103,"adjMaxMagicArmor":103,"adjHit":39,"adjDodge":39,"adjRealDmg":7,"adjRealDmgDef":9,"adjDebilityEnh":6,"adjDebilityAnti":5})
    }),
    51012052: _tools.RODict({
        "propID": 51012052,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":68220,"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":54,"adjMinMagicAtk":30,"adjMaxMagicAtk":54,"adjMinPhysicalArmor":104,"adjMaxPhysicalArmor":104,"adjMinMagicArmor":104,"adjMaxMagicArmor":104,"adjHit":39,"adjDodge":39,"adjRealDmg":7,"adjRealDmgDef":9,"adjDebilityEnh":7,"adjDebilityAnti":5})
    }),
    51012053: _tools.RODict({
        "propID": 51012053,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":69380,"adjMinPhysicalAtk":31,"adjMaxPhysicalAtk":56,"adjMinMagicAtk":31,"adjMaxMagicAtk":56,"adjMinPhysicalArmor":105,"adjMaxPhysicalArmor":105,"adjMinMagicArmor":105,"adjMaxMagicArmor":105,"adjHit":41,"adjDodge":41,"adjRealDmg":7,"adjRealDmgDef":10,"adjDebilityEnh":7,"adjDebilityAnti":6})
    }),
    51012054: _tools.RODict({
        "propID": 51012054,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":71440,"adjMinPhysicalAtk":31,"adjMaxPhysicalAtk":58,"adjMinMagicAtk":31,"adjMaxMagicAtk":58,"adjMinPhysicalArmor":107,"adjMaxPhysicalArmor":107,"adjMinMagicArmor":107,"adjMaxMagicArmor":107,"adjHit":45,"adjDodge":45,"adjRealDmg":8,"adjRealDmgDef":10,"adjDebilityEnh":7,"adjDebilityAnti":6})
    }),
    51012055: _tools.RODict({
        "propID": 51012055,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":73780,"adjMinPhysicalAtk":34,"adjMaxPhysicalAtk":60,"adjMinMagicAtk":34,"adjMaxMagicAtk":60,"adjMinPhysicalArmor":109,"adjMaxPhysicalArmor":109,"adjMinMagicArmor":109,"adjMaxMagicArmor":109,"adjHit":45,"adjDodge":45,"adjRealDmg":8,"adjRealDmgDef":10,"adjDebilityEnh":7,"adjDebilityAnti":6})
    }),
    51012056: _tools.RODict({
        "propID": 51012056,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":80260,"adjMinPhysicalAtk":34,"adjMaxPhysicalAtk":61,"adjMinMagicAtk":34,"adjMaxMagicAtk":61,"adjMinPhysicalArmor":117,"adjMaxPhysicalArmor":117,"adjMinMagicArmor":117,"adjMaxMagicArmor":117,"adjHit":45,"adjDodge":45,"adjRealDmg":8,"adjRealDmgDef":10,"adjDebilityEnh":7,"adjDebilityAnti":6})
    }),
    51012057: _tools.RODict({
        "propID": 51012057,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":83640,"adjMinPhysicalAtk":36,"adjMaxPhysicalAtk":66,"adjMinMagicAtk":36,"adjMaxMagicAtk":66,"adjMinPhysicalArmor":118,"adjMaxPhysicalArmor":118,"adjMinMagicArmor":118,"adjMaxMagicArmor":118,"adjHit":45,"adjDodge":45,"adjRealDmg":8,"adjRealDmgDef":10,"adjDebilityEnh":8,"adjDebilityAnti":6})
    }),
    51012058: _tools.RODict({
        "propID": 51012058,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":84720,"adjMinPhysicalAtk":38,"adjMaxPhysicalAtk":70,"adjMinMagicAtk":38,"adjMaxMagicAtk":70,"adjMinPhysicalArmor":119,"adjMaxPhysicalArmor":119,"adjMinMagicArmor":119,"adjMaxMagicArmor":119,"adjHit":47,"adjDodge":47,"adjRealDmg":8,"adjRealDmgDef":11,"adjDebilityEnh":8,"adjDebilityAnti":7})
    }),
    51012059: _tools.RODict({
        "propID": 51012059,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":88440,"adjMinPhysicalAtk":38,"adjMaxPhysicalAtk":71,"adjMinMagicAtk":38,"adjMaxMagicAtk":71,"adjMinPhysicalArmor":122,"adjMaxPhysicalArmor":122,"adjMinMagicArmor":122,"adjMaxMagicArmor":122,"adjHit":51,"adjDodge":51,"adjRealDmg":9,"adjRealDmgDef":11,"adjDebilityEnh":8,"adjDebilityAnti":7})
    }),
    51012060: _tools.RODict({
        "propID": 51012060,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":91960,"adjMinPhysicalAtk":41,"adjMaxPhysicalAtk":73,"adjMinMagicAtk":41,"adjMaxMagicAtk":73,"adjMinPhysicalArmor":125,"adjMaxPhysicalArmor":125,"adjMinMagicArmor":125,"adjMaxMagicArmor":125,"adjHit":51,"adjDodge":51,"adjRealDmg":9,"adjRealDmgDef":11,"adjDebilityEnh":8,"adjDebilityAnti":7})
    }),
    51012061: _tools.RODict({
        "propID": 51012061,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":103620,"adjMinPhysicalAtk":42,"adjMaxPhysicalAtk":76,"adjMinMagicAtk":42,"adjMaxMagicAtk":76,"adjMinPhysicalArmor":135,"adjMaxPhysicalArmor":135,"adjMinMagicArmor":135,"adjMaxMagicArmor":135,"adjHit":51,"adjDodge":51,"adjRealDmg":9,"adjRealDmgDef":11,"adjDebilityEnh":8,"adjDebilityAnti":7})
    }),
    51012062: _tools.RODict({
        "propID": 51012062,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":107380,"adjMinPhysicalAtk":46,"adjMaxPhysicalAtk":83,"adjMinMagicAtk":46,"adjMaxMagicAtk":83,"adjMinPhysicalArmor":136,"adjMaxPhysicalArmor":136,"adjMinMagicArmor":136,"adjMaxMagicArmor":136,"adjHit":51,"adjDodge":51,"adjRealDmg":9,"adjRealDmgDef":11,"adjDebilityEnh":10,"adjDebilityAnti":7})
    }),
    51012063: _tools.RODict({
        "propID": 51012063,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":108940,"adjMinPhysicalAtk":48,"adjMaxPhysicalAtk":88,"adjMinMagicAtk":48,"adjMaxMagicAtk":88,"adjMinPhysicalArmor":137,"adjMaxPhysicalArmor":137,"adjMinMagicArmor":137,"adjMaxMagicArmor":137,"adjHit":57,"adjDodge":57,"adjRealDmg":9,"adjRealDmgDef":13,"adjDebilityEnh":10,"adjDebilityAnti":9})
    }),
    51012064: _tools.RODict({
        "propID": 51012064,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":114560,"adjMinPhysicalAtk":50,"adjMaxPhysicalAtk":91,"adjMinMagicAtk":50,"adjMaxMagicAtk":91,"adjMinPhysicalArmor":142,"adjMaxPhysicalArmor":142,"adjMinMagicArmor":142,"adjMaxMagicArmor":142,"adjHit":62,"adjDodge":62,"adjRealDmg":11,"adjRealDmgDef":13,"adjDebilityEnh":10,"adjDebilityAnti":9})
    }),
    51012065: _tools.RODict({
        "propID": 51012065,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":120540,"adjMinPhysicalAtk":52,"adjMaxPhysicalAtk":94,"adjMinMagicAtk":52,"adjMaxMagicAtk":94,"adjMinPhysicalArmor":147,"adjMaxPhysicalArmor":147,"adjMinMagicArmor":147,"adjMaxMagicArmor":147,"adjHit":62,"adjDodge":62,"adjRealDmg":11,"adjRealDmgDef":13,"adjDebilityEnh":10,"adjDebilityAnti":9})
    }),
    51012066: _tools.RODict({
        "propID": 51012066,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":130780,"adjMinPhysicalAtk":53,"adjMaxPhysicalAtk":96,"adjMinMagicAtk":53,"adjMaxMagicAtk":96,"adjMinPhysicalArmor":157,"adjMaxPhysicalArmor":157,"adjMinMagicArmor":157,"adjMaxMagicArmor":157,"adjHit":62,"adjDodge":62,"adjRealDmg":11,"adjRealDmgDef":13,"adjDebilityEnh":10,"adjDebilityAnti":9})
    }),
    51012067: _tools.RODict({
        "propID": 51012067,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":135440,"adjMinPhysicalAtk":58,"adjMaxPhysicalAtk":106,"adjMinMagicAtk":58,"adjMaxMagicAtk":106,"adjMinPhysicalArmor":158,"adjMaxPhysicalArmor":158,"adjMinMagicArmor":158,"adjMaxMagicArmor":158,"adjHit":62,"adjDodge":62,"adjRealDmg":11,"adjRealDmgDef":13,"adjDebilityEnh":12,"adjDebilityAnti":9})
    }),
    51012068: _tools.RODict({
        "propID": 51012068,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":137000,"adjMinPhysicalAtk":61,"adjMaxPhysicalAtk":110,"adjMinMagicAtk":61,"adjMaxMagicAtk":110,"adjMinPhysicalArmor":159,"adjMaxPhysicalArmor":159,"adjMinMagicArmor":159,"adjMaxMagicArmor":159,"adjHit":64,"adjDodge":64,"adjRealDmg":11,"adjRealDmgDef":14,"adjDebilityEnh":12,"adjDebilityAnti":11})
    }),
    51012069: _tools.RODict({
        "propID": 51012069,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":142060,"adjMinPhysicalAtk":62,"adjMaxPhysicalAtk":114,"adjMinMagicAtk":62,"adjMaxMagicAtk":114,"adjMinPhysicalArmor":162,"adjMaxPhysicalArmor":162,"adjMinMagicArmor":162,"adjMaxMagicArmor":162,"adjHit":70,"adjDodge":70,"adjRealDmg":12,"adjRealDmgDef":14,"adjDebilityEnh":12,"adjDebilityAnti":11})
    }),
    51012070: _tools.RODict({
        "propID": 51012070,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":146900,"adjMinPhysicalAtk":65,"adjMaxPhysicalAtk":119,"adjMinMagicAtk":65,"adjMaxMagicAtk":119,"adjMinPhysicalArmor":165,"adjMaxPhysicalArmor":165,"adjMinMagicArmor":165,"adjMaxMagicArmor":165,"adjHit":70,"adjDodge":70,"adjRealDmg":12,"adjRealDmgDef":14,"adjDebilityEnh":12,"adjDebilityAnti":11})
    }),
    52012071: _tools.RODict({
        "propID": 52012071,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":592800,"adjMinPhysicalAtk":277,"adjMaxPhysicalAtk":292,"adjMinMagicAtk":277,"adjMaxMagicAtk":292,"adjMinPhysicalArmor":73,"adjMaxPhysicalArmor":73,"adjMinMagicArmor":73,"adjMaxMagicArmor":73,"adjHit":41,"adjDodge":7,"adjRealDmg":5,"adjRealDmgDef":1,"adjDebilityEnh":15,"adjDebilityAnti":5})
    }),
    52012072: _tools.RODict({
        "propID": 52012072,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":58798,"adjMinPhysicalAtk":134,"adjMaxPhysicalAtk":164,"adjMinMagicAtk":134,"adjMaxMagicAtk":164,"adjMinPhysicalArmor":27,"adjMaxPhysicalArmor":27,"adjMinMagicArmor":27,"adjMaxMagicArmor":27,"adjHit":90,"adjDodge":13,"adjRealDmg":5,"adjRealDmgDef":1,"adjDebilityEnh":15,"adjDebilityAnti":5})
    }),
    51013001: _tools.RODict({
        "propID": 51013001,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5741,"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":39,"adjMinMagicAtk":32,"adjMaxMagicAtk":39,"adjMinPhysicalArmor":3,"adjMaxPhysicalArmor":3,"adjMinMagicArmor":3,"adjMaxMagicArmor":3,"adjHit":6,"adjDodge":2,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013002: _tools.RODict({
        "propID": 51013002,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5141,"adjMinPhysicalAtk":35,"adjMaxPhysicalAtk":43,"adjMinMagicAtk":35,"adjMaxMagicAtk":43,"adjMinPhysicalArmor":4,"adjMaxPhysicalArmor":4,"adjMinMagicArmor":4,"adjMaxMagicArmor":4,"adjHit":6,"adjDodge":2,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013003: _tools.RODict({
        "propID": 51013003,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5594,"adjMinPhysicalAtk":37,"adjMaxPhysicalAtk":46,"adjMinMagicAtk":37,"adjMaxMagicAtk":46,"adjMinPhysicalArmor":4,"adjMaxPhysicalArmor":4,"adjMinMagicArmor":4,"adjMaxMagicArmor":4,"adjHit":6,"adjDodge":2,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013004: _tools.RODict({
        "propID": 51013004,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5294,"adjMinPhysicalAtk":40,"adjMaxPhysicalAtk":48,"adjMinMagicAtk":40,"adjMaxMagicAtk":48,"adjMinPhysicalArmor":5,"adjMaxPhysicalArmor":5,"adjMinMagicArmor":5,"adjMaxMagicArmor":5,"adjHit":6,"adjDodge":2,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013005: _tools.RODict({
        "propID": 51013005,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5746,"adjMinPhysicalAtk":42,"adjMaxPhysicalAtk":51,"adjMinMagicAtk":42,"adjMaxMagicAtk":51,"adjMinPhysicalArmor":5,"adjMaxPhysicalArmor":5,"adjMinMagicArmor":5,"adjMaxMagicArmor":5,"adjHit":6,"adjDodge":2,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013006: _tools.RODict({
        "propID": 51013006,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":6652,"adjMinPhysicalAtk":43,"adjMaxPhysicalAtk":52,"adjMinMagicAtk":43,"adjMaxMagicAtk":52,"adjMinPhysicalArmor":5,"adjMaxPhysicalArmor":5,"adjMinMagicArmor":5,"adjMaxMagicArmor":5,"adjHit":6,"adjDodge":6,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013007: _tools.RODict({
        "propID": 51013007,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":7404,"adjMinPhysicalAtk":46,"adjMaxPhysicalAtk":56,"adjMinMagicAtk":46,"adjMaxMagicAtk":56,"adjMinPhysicalArmor":5,"adjMaxPhysicalArmor":5,"adjMinMagicArmor":5,"adjMaxMagicArmor":5,"adjHit":10,"adjDodge":6,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013008: _tools.RODict({
        "propID": 51013008,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":6804,"adjMinPhysicalAtk":48,"adjMaxPhysicalAtk":59,"adjMinMagicAtk":48,"adjMaxMagicAtk":59,"adjMinPhysicalArmor":6,"adjMaxPhysicalArmor":6,"adjMinMagicArmor":6,"adjMaxMagicArmor":6,"adjHit":10,"adjDodge":6,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013009: _tools.RODict({
        "propID": 51013009,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":7257,"adjMinPhysicalAtk":50,"adjMaxPhysicalAtk":61,"adjMinMagicAtk":50,"adjMaxMagicAtk":61,"adjMinPhysicalArmor":6,"adjMaxPhysicalArmor":6,"adjMinMagicArmor":6,"adjMaxMagicArmor":6,"adjHit":10,"adjDodge":6,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013010: _tools.RODict({
        "propID": 51013010,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":6957,"adjMinPhysicalAtk":51,"adjMaxPhysicalAtk":63,"adjMinMagicAtk":51,"adjMaxMagicAtk":63,"adjMinPhysicalArmor":7,"adjMaxPhysicalArmor":7,"adjMinMagicArmor":7,"adjMaxMagicArmor":7,"adjHit":10,"adjDodge":6,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013011: _tools.RODict({
        "propID": 51013011,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":8315,"adjMinPhysicalAtk":53,"adjMaxPhysicalAtk":65,"adjMinMagicAtk":53,"adjMaxMagicAtk":65,"adjMinPhysicalArmor":7,"adjMaxPhysicalArmor":7,"adjMinMagicArmor":7,"adjMaxMagicArmor":7,"adjHit":10,"adjDodge":7,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013012: _tools.RODict({
        "propID": 51013012,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":8615,"adjMinPhysicalAtk":56,"adjMaxPhysicalAtk":69,"adjMinMagicAtk":56,"adjMaxMagicAtk":69,"adjMinPhysicalArmor":7,"adjMaxPhysicalArmor":7,"adjMinMagicArmor":7,"adjMaxMagicArmor":7,"adjHit":11,"adjDodge":7,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013013: _tools.RODict({
        "propID": 51013013,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":9067,"adjMinPhysicalAtk":59,"adjMaxPhysicalAtk":72,"adjMinMagicAtk":59,"adjMaxMagicAtk":72,"adjMinPhysicalArmor":7,"adjMaxPhysicalArmor":7,"adjMinMagicArmor":7,"adjMaxMagicArmor":7,"adjHit":11,"adjDodge":7,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013014: _tools.RODict({
        "propID": 51013014,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":8767,"adjMinPhysicalAtk":61,"adjMaxPhysicalAtk":74,"adjMinMagicAtk":61,"adjMaxMagicAtk":74,"adjMinPhysicalArmor":8,"adjMaxPhysicalArmor":8,"adjMinMagicArmor":8,"adjMaxMagicArmor":8,"adjHit":11,"adjDodge":7,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013015: _tools.RODict({
        "propID": 51013015,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":9220,"adjMinPhysicalAtk":63,"adjMaxPhysicalAtk":76,"adjMinMagicAtk":63,"adjMaxMagicAtk":76,"adjMinPhysicalArmor":8,"adjMaxPhysicalArmor":8,"adjMinMagicArmor":8,"adjMaxMagicArmor":8,"adjHit":11,"adjDodge":7,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013016: _tools.RODict({
        "propID": 51013016,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":11635,"adjMinPhysicalAtk":64,"adjMaxPhysicalAtk":78,"adjMinMagicAtk":64,"adjMaxMagicAtk":78,"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjHit":11,"adjDodge":8,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013017: _tools.RODict({
        "propID": 51013017,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":12540,"adjMinPhysicalAtk":72,"adjMaxPhysicalAtk":88,"adjMinMagicAtk":72,"adjMaxMagicAtk":88,"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjHit":12,"adjDodge":8,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013018: _tools.RODict({
        "propID": 51013018,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":12840,"adjMinPhysicalAtk":73,"adjMaxPhysicalAtk":89,"adjMinMagicAtk":73,"adjMaxMagicAtk":89,"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjHit":12,"adjDodge":8,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013019: _tools.RODict({
        "propID": 51013019,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":13745,"adjMinPhysicalAtk":76,"adjMaxPhysicalAtk":93,"adjMinMagicAtk":76,"adjMaxMagicAtk":93,"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjHit":12,"adjDodge":8,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013020: _tools.RODict({
        "propID": 51013020,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":13298,"adjMinPhysicalAtk":77,"adjMaxPhysicalAtk":95,"adjMinMagicAtk":77,"adjMaxMagicAtk":95,"adjMinPhysicalArmor":11,"adjMaxPhysicalArmor":11,"adjMinMagicArmor":11,"adjMaxMagicArmor":11,"adjHit":12,"adjDodge":12,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013021: _tools.RODict({
        "propID": 51013021,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":14808,"adjMinPhysicalAtk":83,"adjMaxPhysicalAtk":102,"adjMinMagicAtk":83,"adjMaxMagicAtk":102,"adjMinPhysicalArmor":12,"adjMaxPhysicalArmor":12,"adjMinMagicArmor":12,"adjMaxMagicArmor":12,"adjHit":16,"adjDodge":12,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013022: _tools.RODict({
        "propID": 51013022,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":8508,"adjMinPhysicalAtk":85,"adjMaxPhysicalAtk":104,"adjMinMagicAtk":85,"adjMaxMagicAtk":104,"adjMinPhysicalArmor":23,"adjMaxPhysicalArmor":23,"adjMinMagicArmor":23,"adjMaxMagicArmor":23,"adjHit":16,"adjDodge":12,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013023: _tools.RODict({
        "propID": 51013023,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":15261,"adjMinPhysicalAtk":87,"adjMaxPhysicalAtk":106,"adjMinMagicAtk":87,"adjMaxMagicAtk":106,"adjMinPhysicalArmor":13,"adjMaxPhysicalArmor":13,"adjMinMagicArmor":13,"adjMaxMagicArmor":13,"adjHit":16,"adjDodge":12,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013024: _tools.RODict({
        "propID": 51013024,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":9266,"adjMinPhysicalAtk":88,"adjMaxPhysicalAtk":107,"adjMinMagicAtk":88,"adjMaxMagicAtk":107,"adjMinPhysicalArmor":25,"adjMaxPhysicalArmor":25,"adjMinMagicArmor":25,"adjMaxMagicArmor":25,"adjHit":16,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013025: _tools.RODict({
        "propID": 51013025,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":17376,"adjMinPhysicalAtk":93,"adjMaxPhysicalAtk":114,"adjMinMagicAtk":93,"adjMaxMagicAtk":114,"adjMinPhysicalArmor":15,"adjMaxPhysicalArmor":15,"adjMinMagicArmor":15,"adjMaxMagicArmor":15,"adjHit":18,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013026: _tools.RODict({
        "propID": 51013026,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":17976,"adjMinPhysicalAtk":94,"adjMaxPhysicalAtk":115,"adjMinMagicAtk":94,"adjMaxMagicAtk":115,"adjMinPhysicalArmor":15,"adjMaxPhysicalArmor":15,"adjMinMagicArmor":15,"adjMaxMagicArmor":15,"adjHit":18,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013027: _tools.RODict({
        "propID": 51013027,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":19482,"adjMinPhysicalAtk":96,"adjMaxPhysicalAtk":118,"adjMinMagicAtk":96,"adjMaxMagicAtk":118,"adjMinPhysicalArmor":15,"adjMaxPhysicalArmor":15,"adjMinMagicArmor":15,"adjMaxMagicArmor":15,"adjHit":18,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013028: _tools.RODict({
        "propID": 51013028,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":20239,"adjMinPhysicalAtk":97,"adjMaxPhysicalAtk":119,"adjMinMagicAtk":97,"adjMaxMagicAtk":119,"adjMinPhysicalArmor":17,"adjMaxPhysicalArmor":17,"adjMinMagicArmor":17,"adjMaxMagicArmor":17,"adjHit":18,"adjDodge":16,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013029: _tools.RODict({
        "propID": 51013029,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":22050,"adjMinPhysicalAtk":105,"adjMaxPhysicalAtk":128,"adjMinMagicAtk":105,"adjMaxMagicAtk":128,"adjMinPhysicalArmor":18,"adjMaxPhysicalArmor":18,"adjMinMagicArmor":18,"adjMaxMagicArmor":18,"adjHit":20,"adjDodge":16,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013030: _tools.RODict({
        "propID": 51013030,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":22650,"adjMinPhysicalAtk":106,"adjMaxPhysicalAtk":130,"adjMinMagicAtk":106,"adjMaxMagicAtk":130,"adjMinPhysicalArmor":18,"adjMaxPhysicalArmor":18,"adjMinMagicArmor":18,"adjMaxMagicArmor":18,"adjHit":20,"adjDodge":16,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013031: _tools.RODict({
        "propID": 51013031,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":23555,"adjMinPhysicalAtk":109,"adjMaxPhysicalAtk":133,"adjMinMagicAtk":109,"adjMaxMagicAtk":133,"adjMinPhysicalArmor":19,"adjMaxPhysicalArmor":19,"adjMinMagicArmor":19,"adjMaxMagicArmor":19,"adjHit":20,"adjDodge":16,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013032: _tools.RODict({
        "propID": 51013032,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":23407,"adjMinPhysicalAtk":110,"adjMaxPhysicalAtk":135,"adjMinMagicAtk":110,"adjMaxMagicAtk":135,"adjMinPhysicalArmor":21,"adjMaxPhysicalArmor":21,"adjMinMagicArmor":21,"adjMaxMagicArmor":21,"adjHit":20,"adjDodge":18,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013033: _tools.RODict({
        "propID": 51013033,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":28533,"adjMinPhysicalAtk":112,"adjMaxPhysicalAtk":137,"adjMinMagicAtk":112,"adjMaxMagicAtk":137,"adjMinPhysicalArmor":21,"adjMaxPhysicalArmor":21,"adjMinMagicArmor":21,"adjMaxMagicArmor":21,"adjHit":22,"adjDodge":18,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013034: _tools.RODict({
        "propID": 51013034,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":28533,"adjMinPhysicalAtk":121,"adjMaxPhysicalAtk":148,"adjMinMagicAtk":121,"adjMaxMagicAtk":148,"adjMinPhysicalArmor":22,"adjMaxPhysicalArmor":22,"adjMinMagicArmor":22,"adjMaxMagicArmor":22,"adjHit":22,"adjDodge":18,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013035: _tools.RODict({
        "propID": 51013035,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":29586,"adjMinPhysicalAtk":124,"adjMaxPhysicalAtk":152,"adjMinMagicAtk":124,"adjMaxMagicAtk":152,"adjMinPhysicalArmor":22,"adjMaxPhysicalArmor":22,"adjMinMagicArmor":22,"adjMaxMagicArmor":22,"adjHit":22,"adjDodge":19,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013036: _tools.RODict({
        "propID": 51013036,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":32301,"adjMinPhysicalAtk":125,"adjMaxPhysicalAtk":153,"adjMinMagicAtk":125,"adjMaxMagicAtk":153,"adjMinPhysicalArmor":23,"adjMaxPhysicalArmor":23,"adjMinMagicArmor":23,"adjMaxMagicArmor":23,"adjHit":23,"adjDodge":19,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013037: _tools.RODict({
        "propID": 51013037,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":36222,"adjMinPhysicalAtk":127,"adjMaxPhysicalAtk":156,"adjMinMagicAtk":127,"adjMaxMagicAtk":156,"adjMinPhysicalArmor":23,"adjMaxPhysicalArmor":23,"adjMinMagicArmor":23,"adjMaxMagicArmor":23,"adjHit":23,"adjDodge":25,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013038: _tools.RODict({
        "propID": 51013038,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":35922,"adjMinPhysicalAtk":135,"adjMaxPhysicalAtk":165,"adjMinMagicAtk":135,"adjMaxMagicAtk":165,"adjMinPhysicalArmor":24,"adjMaxPhysicalArmor":24,"adjMinMagicArmor":24,"adjMaxMagicArmor":24,"adjHit":29,"adjDodge":25,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013039: _tools.RODict({
        "propID": 51013039,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":36674,"adjMinPhysicalAtk":140,"adjMaxPhysicalAtk":171,"adjMinMagicAtk":140,"adjMaxMagicAtk":171,"adjMinPhysicalArmor":24,"adjMaxPhysicalArmor":24,"adjMinMagicArmor":24,"adjMaxMagicArmor":24,"adjHit":29,"adjDodge":25,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013040: _tools.RODict({
        "propID": 51013040,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":35627,"adjMinPhysicalAtk":141,"adjMaxPhysicalAtk":172,"adjMinMagicAtk":141,"adjMaxMagicAtk":172,"adjMinPhysicalArmor":27,"adjMaxPhysicalArmor":27,"adjMinMagicArmor":27,"adjMaxMagicArmor":27,"adjHit":29,"adjDodge":25,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013041: _tools.RODict({
        "propID": 51013041,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":33832,"adjMinPhysicalAtk":143,"adjMaxPhysicalAtk":175,"adjMinMagicAtk":143,"adjMaxMagicAtk":175,"adjMinPhysicalArmor":32,"adjMaxPhysicalArmor":32,"adjMinMagicArmor":32,"adjMaxMagicArmor":32,"adjHit":29,"adjDodge":27,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013042: _tools.RODict({
        "propID": 51013042,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":38205,"adjMinPhysicalAtk":148,"adjMaxPhysicalAtk":181,"adjMinMagicAtk":148,"adjMaxMagicAtk":181,"adjMinPhysicalArmor":32,"adjMaxPhysicalArmor":32,"adjMinMagicArmor":32,"adjMaxMagicArmor":32,"adjHit":31,"adjDodge":28,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013043: _tools.RODict({
        "propID": 51013043,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":38958,"adjMinPhysicalAtk":155,"adjMaxPhysicalAtk":189,"adjMinMagicAtk":155,"adjMaxMagicAtk":189,"adjMinPhysicalArmor":32,"adjMaxPhysicalArmor":32,"adjMinMagicArmor":32,"adjMaxMagicArmor":32,"adjHit":32,"adjDodge":28,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013044: _tools.RODict({
        "propID": 51013044,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":38658,"adjMinPhysicalAtk":158,"adjMaxPhysicalAtk":193,"adjMinMagicAtk":158,"adjMaxMagicAtk":193,"adjMinPhysicalArmor":33,"adjMaxPhysicalArmor":33,"adjMinMagicArmor":33,"adjMaxMagicArmor":33,"adjHit":32,"adjDodge":28,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013045: _tools.RODict({
        "propID": 51013045,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":41979,"adjMinPhysicalAtk":165,"adjMaxPhysicalAtk":201,"adjMinMagicAtk":165,"adjMaxMagicAtk":201,"adjMinPhysicalArmor":34,"adjMaxPhysicalArmor":34,"adjMinMagicArmor":34,"adjMaxMagicArmor":34,"adjHit":32,"adjDodge":28,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013046: _tools.RODict({
        "propID": 51013046,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":41531,"adjMinPhysicalAtk":168,"adjMaxPhysicalAtk":205,"adjMinMagicAtk":168,"adjMaxMagicAtk":205,"adjMinPhysicalArmor":36,"adjMaxPhysicalArmor":36,"adjMinMagicArmor":36,"adjMaxMagicArmor":36,"adjHit":32,"adjDodge":32,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013047: _tools.RODict({
        "propID": 51013047,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":44094,"adjMinPhysicalAtk":170,"adjMaxPhysicalAtk":207,"adjMinMagicAtk":170,"adjMaxMagicAtk":207,"adjMinPhysicalArmor":36,"adjMaxPhysicalArmor":36,"adjMinMagicArmor":36,"adjMaxMagicArmor":36,"adjHit":36,"adjDodge":32,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013048: _tools.RODict({
        "propID": 51013048,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":47415,"adjMinPhysicalAtk":174,"adjMaxPhysicalAtk":213,"adjMinMagicAtk":174,"adjMaxMagicAtk":213,"adjMinPhysicalArmor":37,"adjMaxPhysicalArmor":37,"adjMinMagicArmor":37,"adjMaxMagicArmor":37,"adjHit":36,"adjDodge":34,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013049: _tools.RODict({
        "propID": 51013049,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":46967,"adjMinPhysicalAtk":185,"adjMaxPhysicalAtk":226,"adjMinMagicAtk":185,"adjMaxMagicAtk":226,"adjMinPhysicalArmor":39,"adjMaxPhysicalArmor":39,"adjMinMagicArmor":39,"adjMaxMagicArmor":39,"adjHit":38,"adjDodge":34,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013050: _tools.RODict({
        "propID": 51013050,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":47120,"adjMinPhysicalAtk":188,"adjMaxPhysicalAtk":230,"adjMinMagicAtk":188,"adjMaxMagicAtk":230,"adjMinPhysicalArmor":40,"adjMaxPhysicalArmor":40,"adjMinMagicArmor":40,"adjMaxMagicArmor":40,"adjHit":38,"adjDodge":34,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013051: _tools.RODict({
        "propID": 51013051,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":47725,"adjMinPhysicalAtk":190,"adjMaxPhysicalAtk":232,"adjMinMagicAtk":190,"adjMaxMagicAtk":232,"adjMinPhysicalArmor":41,"adjMaxPhysicalArmor":41,"adjMinMagicArmor":41,"adjMaxMagicArmor":41,"adjHit":38,"adjDodge":36,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013052: _tools.RODict({
        "propID": 51013052,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":48635,"adjMinPhysicalAtk":191,"adjMaxPhysicalAtk":234,"adjMinMagicAtk":191,"adjMaxMagicAtk":234,"adjMinPhysicalArmor":43,"adjMaxPhysicalArmor":43,"adjMinMagicArmor":43,"adjMaxMagicArmor":43,"adjHit":40,"adjDodge":36,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013053: _tools.RODict({
        "propID": 51013053,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":53009,"adjMinPhysicalAtk":197,"adjMaxPhysicalAtk":240,"adjMinMagicAtk":197,"adjMaxMagicAtk":240,"adjMinPhysicalArmor":43,"adjMaxPhysicalArmor":43,"adjMinMagicArmor":43,"adjMaxMagicArmor":43,"adjHit":40,"adjDodge":39,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013054: _tools.RODict({
        "propID": 51013054,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":52709,"adjMinPhysicalAtk":209,"adjMaxPhysicalAtk":255,"adjMinMagicAtk":209,"adjMaxMagicAtk":255,"adjMinPhysicalArmor":44,"adjMaxPhysicalArmor":44,"adjMinMagicArmor":44,"adjMaxMagicArmor":44,"adjHit":43,"adjDodge":39,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013055: _tools.RODict({
        "propID": 51013055,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":54366,"adjMinPhysicalAtk":213,"adjMaxPhysicalAtk":261,"adjMinMagicAtk":213,"adjMaxMagicAtk":261,"adjMinPhysicalArmor":44,"adjMaxPhysicalArmor":44,"adjMinMagicArmor":44,"adjMaxMagicArmor":44,"adjHit":43,"adjDodge":39,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013056: _tools.RODict({
        "propID": 51013056,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":54372,"adjMinPhysicalAtk":214,"adjMaxPhysicalAtk":262,"adjMinMagicAtk":214,"adjMaxMagicAtk":262,"adjMinPhysicalArmor":46,"adjMaxPhysicalArmor":46,"adjMinMagicArmor":46,"adjMaxMagicArmor":46,"adjHit":43,"adjDodge":41,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013057: _tools.RODict({
        "propID": 51013057,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":57397,"adjMinPhysicalAtk":216,"adjMaxPhysicalAtk":265,"adjMinMagicAtk":216,"adjMaxMagicAtk":265,"adjMinPhysicalArmor":49,"adjMaxPhysicalArmor":49,"adjMinMagicArmor":49,"adjMaxMagicArmor":49,"adjHit":45,"adjDodge":41,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013058: _tools.RODict({
        "propID": 51013058,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":61771,"adjMinPhysicalAtk":226,"adjMaxPhysicalAtk":276,"adjMinMagicAtk":226,"adjMaxMagicAtk":276,"adjMinPhysicalArmor":49,"adjMaxPhysicalArmor":49,"adjMinMagicArmor":49,"adjMaxMagicArmor":49,"adjHit":45,"adjDodge":44,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013059: _tools.RODict({
        "propID": 51013059,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":61923,"adjMinPhysicalAtk":245,"adjMaxPhysicalAtk":299,"adjMinMagicAtk":245,"adjMaxMagicAtk":299,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":50,"adjMaxMagicArmor":50,"adjHit":48,"adjDodge":44,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013060: _tools.RODict({
        "propID": 51013060,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":62833,"adjMinPhysicalAtk":249,"adjMaxPhysicalAtk":304,"adjMinMagicAtk":249,"adjMaxMagicAtk":304,"adjMinPhysicalArmor":52,"adjMaxPhysicalArmor":52,"adjMinMagicArmor":52,"adjMaxMagicArmor":52,"adjHit":48,"adjDodge":44,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013061: _tools.RODict({
        "propID": 51013061,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":64196,"adjMinPhysicalAtk":251,"adjMaxPhysicalAtk":306,"adjMinMagicAtk":251,"adjMaxMagicAtk":306,"adjMinPhysicalArmor":54,"adjMaxPhysicalArmor":54,"adjMinMagicArmor":54,"adjMaxMagicArmor":54,"adjHit":48,"adjDodge":50,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013062: _tools.RODict({
        "propID": 51013062,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":64959,"adjMinPhysicalAtk":252,"adjMaxPhysicalAtk":308,"adjMinMagicAtk":252,"adjMaxMagicAtk":308,"adjMinPhysicalArmor":57,"adjMaxPhysicalArmor":57,"adjMinMagicArmor":57,"adjMaxMagicArmor":57,"adjHit":54,"adjDodge":50,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013063: _tools.RODict({
        "propID": 51013063,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":70690,"adjMinPhysicalAtk":260,"adjMaxPhysicalAtk":317,"adjMinMagicAtk":260,"adjMaxMagicAtk":317,"adjMinPhysicalArmor":57,"adjMaxPhysicalArmor":57,"adjMinMagicArmor":57,"adjMaxMagicArmor":57,"adjHit":54,"adjDodge":54,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013064: _tools.RODict({
        "propID": 51013064,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":71690,"adjMinPhysicalAtk":276,"adjMaxPhysicalAtk":337,"adjMinMagicAtk":276,"adjMaxMagicAtk":337,"adjMinPhysicalArmor":60,"adjMaxPhysicalArmor":60,"adjMinMagicArmor":60,"adjMaxMagicArmor":60,"adjHit":58,"adjDodge":54,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013065: _tools.RODict({
        "propID": 51013065,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":72690,"adjMinPhysicalAtk":282,"adjMaxPhysicalAtk":344,"adjMinMagicAtk":282,"adjMaxMagicAtk":344,"adjMinPhysicalArmor":62,"adjMaxPhysicalArmor":62,"adjMinMagicArmor":62,"adjMaxMagicArmor":62,"adjHit":58,"adjDodge":54,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013066: _tools.RODict({
        "propID": 51013066,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":73690,"adjMinPhysicalAtk":284,"adjMaxPhysicalAtk":347,"adjMinMagicAtk":284,"adjMaxMagicAtk":347,"adjMinPhysicalArmor":64,"adjMaxPhysicalArmor":64,"adjMinMagicArmor":64,"adjMaxMagicArmor":64,"adjHit":58,"adjDodge":56,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013067: _tools.RODict({
        "propID": 51013067,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":74690,"adjMinPhysicalAtk":294,"adjMaxPhysicalAtk":357,"adjMinMagicAtk":294,"adjMaxMagicAtk":357,"adjMinPhysicalArmor":68,"adjMaxPhysicalArmor":68,"adjMinMagicArmor":68,"adjMaxMagicArmor":68,"adjHit":60,"adjDodge":56,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013068: _tools.RODict({
        "propID": 51013068,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":75690,"adjMinPhysicalAtk":304,"adjMaxPhysicalAtk":367,"adjMinMagicAtk":304,"adjMaxMagicAtk":367,"adjMinPhysicalArmor":68,"adjMaxPhysicalArmor":68,"adjMinMagicArmor":68,"adjMaxMagicArmor":68,"adjHit":60,"adjDodge":60,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013069: _tools.RODict({
        "propID": 51013069,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":76690,"adjMinPhysicalAtk":314,"adjMaxPhysicalAtk":377,"adjMinMagicAtk":314,"adjMaxMagicAtk":377,"adjMinPhysicalArmor":69,"adjMaxPhysicalArmor":69,"adjMinMagicArmor":69,"adjMaxMagicArmor":69,"adjHit":64,"adjDodge":64,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51013070: _tools.RODict({
        "propID": 51013070,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":77690,"adjMinPhysicalAtk":324,"adjMaxPhysicalAtk":387,"adjMinMagicAtk":324,"adjMaxMagicAtk":387,"adjMinPhysicalArmor":71,"adjMaxPhysicalArmor":71,"adjMinMagicArmor":71,"adjMaxMagicArmor":71,"adjHit":64,"adjDodge":64,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014001: _tools.RODict({
        "propID": 51014001,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3445,"adjMinPhysicalAtk":18,"adjMaxPhysicalAtk":22,"adjMinMagicAtk":18,"adjMaxMagicAtk":22,"adjMinPhysicalArmor":3,"adjMaxPhysicalArmor":3,"adjMinMagicArmor":3,"adjMaxMagicArmor":3,"adjHit":6,"adjDodge":2,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014002: _tools.RODict({
        "propID": 51014002,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3085,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":25,"adjMinMagicAtk":20,"adjMaxMagicAtk":25,"adjMinPhysicalArmor":4,"adjMaxPhysicalArmor":4,"adjMinMagicArmor":4,"adjMaxMagicArmor":4,"adjHit":6,"adjDodge":2,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014003: _tools.RODict({
        "propID": 51014003,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3356,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":27,"adjMinMagicAtk":22,"adjMaxMagicAtk":27,"adjMinPhysicalArmor":4,"adjMaxPhysicalArmor":4,"adjMinMagicArmor":4,"adjMaxMagicArmor":4,"adjHit":6,"adjDodge":2,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014004: _tools.RODict({
        "propID": 51014004,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3176,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":28,"adjMinMagicAtk":23,"adjMaxMagicAtk":28,"adjMinPhysicalArmor":5,"adjMaxPhysicalArmor":5,"adjMinMagicArmor":5,"adjMaxMagicArmor":5,"adjHit":6,"adjDodge":2,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014005: _tools.RODict({
        "propID": 51014005,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3448,"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":30,"adjMinMagicAtk":24,"adjMaxMagicAtk":30,"adjMinPhysicalArmor":5,"adjMaxPhysicalArmor":5,"adjMinMagicArmor":5,"adjMaxMagicArmor":5,"adjHit":6,"adjDodge":2,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014006: _tools.RODict({
        "propID": 51014006,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3991,"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":31,"adjMinMagicAtk":25,"adjMaxMagicAtk":31,"adjMinPhysicalArmor":5,"adjMaxPhysicalArmor":5,"adjMinMagicArmor":5,"adjMaxMagicArmor":5,"adjHit":6,"adjDodge":6,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014007: _tools.RODict({
        "propID": 51014007,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4442,"adjMinPhysicalAtk":27,"adjMaxPhysicalAtk":33,"adjMinMagicAtk":27,"adjMaxMagicAtk":33,"adjMinPhysicalArmor":5,"adjMaxPhysicalArmor":5,"adjMinMagicArmor":5,"adjMaxMagicArmor":5,"adjHit":10,"adjDodge":6,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014008: _tools.RODict({
        "propID": 51014008,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4082,"adjMinPhysicalAtk":29,"adjMaxPhysicalAtk":35,"adjMinMagicAtk":29,"adjMaxMagicAtk":35,"adjMinPhysicalArmor":6,"adjMaxPhysicalArmor":6,"adjMinMagicArmor":6,"adjMaxMagicArmor":6,"adjHit":10,"adjDodge":6,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014009: _tools.RODict({
        "propID": 51014009,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4354,"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":37,"adjMinMagicAtk":30,"adjMaxMagicAtk":37,"adjMinPhysicalArmor":6,"adjMaxPhysicalArmor":6,"adjMinMagicArmor":6,"adjMaxMagicArmor":6,"adjHit":10,"adjDodge":6,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014010: _tools.RODict({
        "propID": 51014010,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4174,"adjMinPhysicalAtk":31,"adjMaxPhysicalAtk":38,"adjMinMagicAtk":31,"adjMaxMagicAtk":38,"adjMinPhysicalArmor":7,"adjMaxPhysicalArmor":7,"adjMinMagicArmor":7,"adjMaxMagicArmor":7,"adjHit":10,"adjDodge":6,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014011: _tools.RODict({
        "propID": 51014011,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4989,"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":40,"adjMinMagicAtk":32,"adjMaxMagicAtk":40,"adjMinPhysicalArmor":7,"adjMaxPhysicalArmor":7,"adjMinMagicArmor":7,"adjMaxMagicArmor":7,"adjHit":10,"adjDodge":7,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014012: _tools.RODict({
        "propID": 51014012,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5169,"adjMinPhysicalAtk":35,"adjMaxPhysicalAtk":43,"adjMinMagicAtk":35,"adjMaxMagicAtk":43,"adjMinPhysicalArmor":7,"adjMaxPhysicalArmor":7,"adjMinMagicArmor":7,"adjMaxMagicArmor":7,"adjHit":11,"adjDodge":7,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014013: _tools.RODict({
        "propID": 51014013,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5440,"adjMinPhysicalAtk":37,"adjMaxPhysicalAtk":46,"adjMinMagicAtk":37,"adjMaxMagicAtk":46,"adjMinPhysicalArmor":7,"adjMaxPhysicalArmor":7,"adjMinMagicArmor":7,"adjMaxMagicArmor":7,"adjHit":11,"adjDodge":7,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014014: _tools.RODict({
        "propID": 51014014,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5260,"adjMinPhysicalAtk":38,"adjMaxPhysicalAtk":46,"adjMinMagicAtk":38,"adjMaxMagicAtk":46,"adjMinPhysicalArmor":8,"adjMaxPhysicalArmor":8,"adjMinMagicArmor":8,"adjMaxMagicArmor":8,"adjHit":11,"adjDodge":7,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014015: _tools.RODict({
        "propID": 51014015,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5532,"adjMinPhysicalAtk":39,"adjMaxPhysicalAtk":48,"adjMinMagicAtk":39,"adjMaxMagicAtk":48,"adjMinPhysicalArmor":8,"adjMaxPhysicalArmor":8,"adjMinMagicArmor":8,"adjMaxMagicArmor":8,"adjHit":11,"adjDodge":7,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014016: _tools.RODict({
        "propID": 51014016,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":6981,"adjMinPhysicalAtk":40,"adjMaxPhysicalAtk":49,"adjMinMagicAtk":40,"adjMaxMagicAtk":49,"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjHit":11,"adjDodge":8,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014017: _tools.RODict({
        "propID": 51014017,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":7524,"adjMinPhysicalAtk":47,"adjMaxPhysicalAtk":58,"adjMinMagicAtk":47,"adjMaxMagicAtk":58,"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjHit":12,"adjDodge":8,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014018: _tools.RODict({
        "propID": 51014018,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":7704,"adjMinPhysicalAtk":48,"adjMaxPhysicalAtk":58,"adjMinMagicAtk":48,"adjMaxMagicAtk":58,"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjHit":12,"adjDodge":8,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014019: _tools.RODict({
        "propID": 51014019,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":8247,"adjMinPhysicalAtk":50,"adjMaxPhysicalAtk":61,"adjMinMagicAtk":50,"adjMaxMagicAtk":61,"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9,"adjHit":12,"adjDodge":8,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014020: _tools.RODict({
        "propID": 51014020,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":7979,"adjMinPhysicalAtk":50,"adjMaxPhysicalAtk":62,"adjMinMagicAtk":50,"adjMaxMagicAtk":62,"adjMinPhysicalArmor":11,"adjMaxPhysicalArmor":11,"adjMinMagicArmor":11,"adjMaxMagicArmor":11,"adjHit":12,"adjDodge":12,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014021: _tools.RODict({
        "propID": 51014021,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":8885,"adjMinPhysicalAtk":56,"adjMaxPhysicalAtk":68,"adjMinMagicAtk":56,"adjMaxMagicAtk":68,"adjMinPhysicalArmor":12,"adjMaxPhysicalArmor":12,"adjMinMagicArmor":12,"adjMaxMagicArmor":12,"adjHit":16,"adjDodge":12,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014022: _tools.RODict({
        "propID": 51014022,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5105,"adjMinPhysicalAtk":56,"adjMaxPhysicalAtk":69,"adjMinMagicAtk":56,"adjMaxMagicAtk":69,"adjMinPhysicalArmor":23,"adjMaxPhysicalArmor":23,"adjMinMagicArmor":23,"adjMaxMagicArmor":23,"adjHit":16,"adjDodge":12,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014023: _tools.RODict({
        "propID": 51014023,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":9157,"adjMinPhysicalAtk":58,"adjMaxPhysicalAtk":71,"adjMinMagicAtk":58,"adjMaxMagicAtk":71,"adjMinPhysicalArmor":13,"adjMaxPhysicalArmor":13,"adjMinMagicArmor":13,"adjMaxMagicArmor":13,"adjHit":16,"adjDodge":12,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014024: _tools.RODict({
        "propID": 51014024,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5560,"adjMinPhysicalAtk":58,"adjMaxPhysicalAtk":71,"adjMinMagicAtk":58,"adjMaxMagicAtk":71,"adjMinPhysicalArmor":25,"adjMaxPhysicalArmor":25,"adjMinMagicArmor":25,"adjMaxMagicArmor":25,"adjHit":16,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014025: _tools.RODict({
        "propID": 51014025,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":10426,"adjMinPhysicalAtk":63,"adjMaxPhysicalAtk":77,"adjMinMagicAtk":63,"adjMaxMagicAtk":77,"adjMinPhysicalArmor":15,"adjMaxPhysicalArmor":15,"adjMinMagicArmor":15,"adjMaxMagicArmor":15,"adjHit":18,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014026: _tools.RODict({
        "propID": 51014026,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":10786,"adjMinPhysicalAtk":63,"adjMaxPhysicalAtk":77,"adjMinMagicAtk":63,"adjMaxMagicAtk":77,"adjMinPhysicalArmor":15,"adjMaxPhysicalArmor":15,"adjMinMagicArmor":15,"adjMaxMagicArmor":15,"adjHit":18,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014027: _tools.RODict({
        "propID": 51014027,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":11689,"adjMinPhysicalAtk":65,"adjMaxPhysicalAtk":79,"adjMinMagicAtk":65,"adjMaxMagicAtk":79,"adjMinPhysicalArmor":15,"adjMaxPhysicalArmor":15,"adjMinMagicArmor":15,"adjMaxMagicArmor":15,"adjHit":18,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014028: _tools.RODict({
        "propID": 51014028,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":12143,"adjMinPhysicalAtk":65,"adjMaxPhysicalAtk":80,"adjMinMagicAtk":65,"adjMaxMagicAtk":80,"adjMinPhysicalArmor":17,"adjMaxPhysicalArmor":17,"adjMinMagicArmor":17,"adjMaxMagicArmor":17,"adjHit":18,"adjDodge":16,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014029: _tools.RODict({
        "propID": 51014029,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":13230,"adjMinPhysicalAtk":71,"adjMaxPhysicalAtk":87,"adjMinMagicAtk":71,"adjMaxMagicAtk":87,"adjMinPhysicalArmor":18,"adjMaxPhysicalArmor":18,"adjMinMagicArmor":18,"adjMaxMagicArmor":18,"adjHit":20,"adjDodge":16,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014030: _tools.RODict({
        "propID": 51014030,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":13590,"adjMinPhysicalAtk":71,"adjMaxPhysicalAtk":87,"adjMinMagicAtk":71,"adjMaxMagicAtk":87,"adjMinPhysicalArmor":18,"adjMaxPhysicalArmor":18,"adjMinMagicArmor":18,"adjMaxMagicArmor":18,"adjHit":20,"adjDodge":16,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014031: _tools.RODict({
        "propID": 51014031,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":14133,"adjMinPhysicalAtk":74,"adjMaxPhysicalAtk":90,"adjMinMagicAtk":74,"adjMaxMagicAtk":90,"adjMinPhysicalArmor":19,"adjMaxPhysicalArmor":19,"adjMinMagicArmor":19,"adjMaxMagicArmor":19,"adjHit":20,"adjDodge":16,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014032: _tools.RODict({
        "propID": 51014032,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":14044,"adjMinPhysicalAtk":74,"adjMaxPhysicalAtk":91,"adjMinMagicAtk":74,"adjMaxMagicAtk":91,"adjMinPhysicalArmor":21,"adjMaxPhysicalArmor":21,"adjMinMagicArmor":21,"adjMaxMagicArmor":21,"adjHit":20,"adjDodge":18,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014033: _tools.RODict({
        "propID": 51014033,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":17120,"adjMinPhysicalAtk":76,"adjMaxPhysicalAtk":93,"adjMinMagicAtk":76,"adjMaxMagicAtk":93,"adjMinPhysicalArmor":21,"adjMaxPhysicalArmor":21,"adjMinMagicArmor":21,"adjMaxMagicArmor":21,"adjHit":22,"adjDodge":18,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014034: _tools.RODict({
        "propID": 51014034,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":17120,"adjMinPhysicalAtk":84,"adjMaxPhysicalAtk":102,"adjMinMagicAtk":84,"adjMaxMagicAtk":102,"adjMinPhysicalArmor":22,"adjMaxPhysicalArmor":22,"adjMinMagicArmor":22,"adjMaxMagicArmor":22,"adjHit":22,"adjDodge":18,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014035: _tools.RODict({
        "propID": 51014035,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":17752,"adjMinPhysicalAtk":86,"adjMaxPhysicalAtk":105,"adjMinMagicAtk":86,"adjMaxMagicAtk":105,"adjMinPhysicalArmor":22,"adjMaxPhysicalArmor":22,"adjMinMagicArmor":22,"adjMaxMagicArmor":22,"adjHit":22,"adjDodge":19,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014036: _tools.RODict({
        "propID": 51014036,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":19381,"adjMinPhysicalAtk":86,"adjMaxPhysicalAtk":105,"adjMinMagicAtk":86,"adjMaxMagicAtk":105,"adjMinPhysicalArmor":23,"adjMaxPhysicalArmor":23,"adjMinMagicArmor":23,"adjMaxMagicArmor":23,"adjHit":23,"adjDodge":19,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014037: _tools.RODict({
        "propID": 51014037,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":21733,"adjMinPhysicalAtk":88,"adjMaxPhysicalAtk":107,"adjMinMagicAtk":88,"adjMaxMagicAtk":107,"adjMinPhysicalArmor":23,"adjMaxPhysicalArmor":23,"adjMinMagicArmor":23,"adjMaxMagicArmor":23,"adjHit":23,"adjDodge":25,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014038: _tools.RODict({
        "propID": 51014038,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":21553,"adjMinPhysicalAtk":93,"adjMaxPhysicalAtk":113,"adjMinMagicAtk":93,"adjMaxMagicAtk":113,"adjMinPhysicalArmor":24,"adjMaxPhysicalArmor":24,"adjMinMagicArmor":24,"adjMaxMagicArmor":24,"adjHit":29,"adjDodge":25,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014039: _tools.RODict({
        "propID": 51014039,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":22004,"adjMinPhysicalAtk":96,"adjMaxPhysicalAtk":118,"adjMinMagicAtk":96,"adjMaxMagicAtk":118,"adjMinPhysicalArmor":24,"adjMaxPhysicalArmor":24,"adjMinMagicArmor":24,"adjMaxMagicArmor":24,"adjHit":29,"adjDodge":25,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014040: _tools.RODict({
        "propID": 51014040,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":21376,"adjMinPhysicalAtk":97,"adjMaxPhysicalAtk":119,"adjMinMagicAtk":97,"adjMaxMagicAtk":119,"adjMinPhysicalArmor":27,"adjMaxPhysicalArmor":27,"adjMinMagicArmor":27,"adjMaxMagicArmor":27,"adjHit":29,"adjDodge":25,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014041: _tools.RODict({
        "propID": 51014041,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":20299,"adjMinPhysicalAtk":98,"adjMaxPhysicalAtk":120,"adjMinMagicAtk":98,"adjMaxMagicAtk":120,"adjMinPhysicalArmor":32,"adjMaxPhysicalArmor":32,"adjMinMagicArmor":32,"adjMaxMagicArmor":32,"adjHit":29,"adjDodge":27,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014042: _tools.RODict({
        "propID": 51014042,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":22923,"adjMinPhysicalAtk":101,"adjMaxPhysicalAtk":123,"adjMinMagicAtk":101,"adjMaxMagicAtk":123,"adjMinPhysicalArmor":32,"adjMaxPhysicalArmor":32,"adjMinMagicArmor":32,"adjMaxMagicArmor":32,"adjHit":31,"adjDodge":28,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014043: _tools.RODict({
        "propID": 51014043,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":23375,"adjMinPhysicalAtk":107,"adjMaxPhysicalAtk":131,"adjMinMagicAtk":107,"adjMaxMagicAtk":131,"adjMinPhysicalArmor":32,"adjMaxPhysicalArmor":32,"adjMinMagicArmor":32,"adjMaxMagicArmor":32,"adjHit":32,"adjDodge":28,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014044: _tools.RODict({
        "propID": 51014044,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":23195,"adjMinPhysicalAtk":109,"adjMaxPhysicalAtk":133,"adjMinMagicAtk":109,"adjMaxMagicAtk":133,"adjMinPhysicalArmor":33,"adjMaxPhysicalArmor":33,"adjMinMagicArmor":33,"adjMaxMagicArmor":33,"adjHit":32,"adjDodge":28,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014045: _tools.RODict({
        "propID": 51014045,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":25187,"adjMinPhysicalAtk":113,"adjMaxPhysicalAtk":138,"adjMinMagicAtk":113,"adjMaxMagicAtk":138,"adjMinPhysicalArmor":34,"adjMaxPhysicalArmor":34,"adjMinMagicArmor":34,"adjMaxMagicArmor":34,"adjHit":32,"adjDodge":28,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014046: _tools.RODict({
        "propID": 51014046,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":24919,"adjMinPhysicalAtk":115,"adjMaxPhysicalAtk":141,"adjMinMagicAtk":115,"adjMaxMagicAtk":141,"adjMinPhysicalArmor":36,"adjMaxPhysicalArmor":36,"adjMinMagicArmor":36,"adjMaxMagicArmor":36,"adjHit":32,"adjDodge":32,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014047: _tools.RODict({
        "propID": 51014047,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":26456,"adjMinPhysicalAtk":117,"adjMaxPhysicalAtk":143,"adjMinMagicAtk":117,"adjMaxMagicAtk":143,"adjMinPhysicalArmor":36,"adjMaxPhysicalArmor":36,"adjMinMagicArmor":36,"adjMaxMagicArmor":36,"adjHit":36,"adjDodge":32,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014048: _tools.RODict({
        "propID": 51014048,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":28449,"adjMinPhysicalAtk":120,"adjMaxPhysicalAtk":147,"adjMinMagicAtk":120,"adjMaxMagicAtk":147,"adjMinPhysicalArmor":37,"adjMaxPhysicalArmor":37,"adjMinMagicArmor":37,"adjMaxMagicArmor":37,"adjHit":36,"adjDodge":34,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014049: _tools.RODict({
        "propID": 51014049,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":28180,"adjMinPhysicalAtk":127,"adjMaxPhysicalAtk":156,"adjMinMagicAtk":127,"adjMaxMagicAtk":156,"adjMinPhysicalArmor":39,"adjMaxPhysicalArmor":39,"adjMinMagicArmor":39,"adjMaxMagicArmor":39,"adjHit":38,"adjDodge":34,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014050: _tools.RODict({
        "propID": 51014050,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":28272,"adjMinPhysicalAtk":130,"adjMaxPhysicalAtk":158,"adjMinMagicAtk":130,"adjMaxMagicAtk":158,"adjMinPhysicalArmor":40,"adjMaxPhysicalArmor":40,"adjMinMagicArmor":40,"adjMaxMagicArmor":40,"adjHit":38,"adjDodge":34,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014051: _tools.RODict({
        "propID": 51014051,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":28635,"adjMinPhysicalAtk":131,"adjMaxPhysicalAtk":160,"adjMinMagicAtk":131,"adjMaxMagicAtk":160,"adjMinPhysicalArmor":41,"adjMaxPhysicalArmor":41,"adjMinMagicArmor":41,"adjMaxMagicArmor":41,"adjHit":38,"adjDodge":36,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014052: _tools.RODict({
        "propID": 51014052,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":29181,"adjMinPhysicalAtk":132,"adjMaxPhysicalAtk":161,"adjMinMagicAtk":132,"adjMaxMagicAtk":161,"adjMinPhysicalArmor":43,"adjMaxPhysicalArmor":43,"adjMinMagicArmor":43,"adjMaxMagicArmor":43,"adjHit":40,"adjDodge":36,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014053: _tools.RODict({
        "propID": 51014053,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":31805,"adjMinPhysicalAtk":136,"adjMaxPhysicalAtk":166,"adjMinMagicAtk":136,"adjMaxMagicAtk":166,"adjMinPhysicalArmor":43,"adjMaxPhysicalArmor":43,"adjMinMagicArmor":43,"adjMaxMagicArmor":43,"adjHit":40,"adjDodge":39,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014054: _tools.RODict({
        "propID": 51014054,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":31625,"adjMinPhysicalAtk":143,"adjMaxPhysicalAtk":175,"adjMinMagicAtk":143,"adjMaxMagicAtk":175,"adjMinPhysicalArmor":44,"adjMaxPhysicalArmor":44,"adjMinMagicArmor":44,"adjMaxMagicArmor":44,"adjHit":43,"adjDodge":39,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014055: _tools.RODict({
        "propID": 51014055,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":32620,"adjMinPhysicalAtk":147,"adjMaxPhysicalAtk":180,"adjMinMagicAtk":147,"adjMaxMagicAtk":180,"adjMinPhysicalArmor":44,"adjMaxPhysicalArmor":44,"adjMinMagicArmor":44,"adjMaxMagicArmor":44,"adjHit":43,"adjDodge":39,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014056: _tools.RODict({
        "propID": 51014056,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":32623,"adjMinPhysicalAtk":148,"adjMaxPhysicalAtk":181,"adjMinMagicAtk":148,"adjMaxMagicAtk":181,"adjMinPhysicalArmor":46,"adjMaxPhysicalArmor":46,"adjMinMagicArmor":46,"adjMaxMagicArmor":46,"adjHit":43,"adjDodge":41,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014057: _tools.RODict({
        "propID": 51014057,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":34438,"adjMinPhysicalAtk":149,"adjMaxPhysicalAtk":182,"adjMinMagicAtk":149,"adjMaxMagicAtk":182,"adjMinPhysicalArmor":49,"adjMaxPhysicalArmor":49,"adjMinMagicArmor":49,"adjMaxMagicArmor":49,"adjHit":45,"adjDodge":41,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014058: _tools.RODict({
        "propID": 51014058,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":37063,"adjMinPhysicalAtk":158,"adjMaxPhysicalAtk":193,"adjMinMagicAtk":158,"adjMaxMagicAtk":193,"adjMinPhysicalArmor":49,"adjMaxPhysicalArmor":49,"adjMinMagicArmor":49,"adjMaxMagicArmor":49,"adjHit":45,"adjDodge":44,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014059: _tools.RODict({
        "propID": 51014059,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":37154,"adjMinPhysicalAtk":169,"adjMaxPhysicalAtk":207,"adjMinMagicAtk":169,"adjMaxMagicAtk":207,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":50,"adjMaxMagicArmor":50,"adjHit":48,"adjDodge":44,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014060: _tools.RODict({
        "propID": 51014060,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":37700,"adjMinPhysicalAtk":172,"adjMaxPhysicalAtk":211,"adjMinMagicAtk":172,"adjMaxMagicAtk":211,"adjMinPhysicalArmor":52,"adjMaxPhysicalArmor":52,"adjMinMagicArmor":52,"adjMaxMagicArmor":52,"adjHit":48,"adjDodge":44,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014061: _tools.RODict({
        "propID": 51014061,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":38518,"adjMinPhysicalAtk":174,"adjMaxPhysicalAtk":213,"adjMinMagicAtk":174,"adjMaxMagicAtk":213,"adjMinPhysicalArmor":54,"adjMaxPhysicalArmor":54,"adjMinMagicArmor":54,"adjMaxMagicArmor":54,"adjHit":48,"adjDodge":50,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014062: _tools.RODict({
        "propID": 51014062,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":38975,"adjMinPhysicalAtk":174,"adjMaxPhysicalAtk":213,"adjMinMagicAtk":174,"adjMaxMagicAtk":213,"adjMinPhysicalArmor":57,"adjMaxPhysicalArmor":57,"adjMinMagicArmor":57,"adjMaxMagicArmor":57,"adjHit":54,"adjDodge":50,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014063: _tools.RODict({
        "propID": 51014063,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":42414,"adjMinPhysicalAtk":182,"adjMaxPhysicalAtk":222,"adjMinMagicAtk":182,"adjMaxMagicAtk":222,"adjMinPhysicalArmor":57,"adjMaxPhysicalArmor":57,"adjMinMagicArmor":57,"adjMaxMagicArmor":57,"adjHit":54,"adjDodge":54,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014064: _tools.RODict({
        "propID": 51014064,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":43014,"adjMinPhysicalAtk":191,"adjMaxPhysicalAtk":234,"adjMinMagicAtk":191,"adjMaxMagicAtk":234,"adjMinPhysicalArmor":60,"adjMaxPhysicalArmor":60,"adjMinMagicArmor":60,"adjMaxMagicArmor":60,"adjHit":58,"adjDodge":54,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014065: _tools.RODict({
        "propID": 51014065,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":43614,"adjMinPhysicalAtk":196,"adjMaxPhysicalAtk":240,"adjMinMagicAtk":196,"adjMaxMagicAtk":240,"adjMinPhysicalArmor":62,"adjMaxPhysicalArmor":62,"adjMinMagicArmor":62,"adjMaxMagicArmor":62,"adjHit":58,"adjDodge":54,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014066: _tools.RODict({
        "propID": 51014066,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":44214,"adjMinPhysicalAtk":197,"adjMaxPhysicalAtk":241,"adjMinMagicAtk":197,"adjMaxMagicAtk":241,"adjMinPhysicalArmor":64,"adjMaxPhysicalArmor":64,"adjMinMagicArmor":64,"adjMaxMagicArmor":64,"adjHit":58,"adjDodge":56,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014067: _tools.RODict({
        "propID": 51014067,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":44814,"adjMinPhysicalAtk":207,"adjMaxPhysicalAtk":251,"adjMinMagicAtk":207,"adjMaxMagicAtk":251,"adjMinPhysicalArmor":68,"adjMaxPhysicalArmor":68,"adjMinMagicArmor":68,"adjMaxMagicArmor":68,"adjHit":60,"adjDodge":56,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014068: _tools.RODict({
        "propID": 51014068,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":45414,"adjMinPhysicalAtk":217,"adjMaxPhysicalAtk":261,"adjMinMagicAtk":217,"adjMaxMagicAtk":261,"adjMinPhysicalArmor":68,"adjMaxPhysicalArmor":68,"adjMinMagicArmor":68,"adjMaxMagicArmor":68,"adjHit":60,"adjDodge":60,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014069: _tools.RODict({
        "propID": 51014069,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":46014,"adjMinPhysicalAtk":227,"adjMaxPhysicalAtk":271,"adjMinMagicAtk":227,"adjMaxMagicAtk":271,"adjMinPhysicalArmor":69,"adjMaxPhysicalArmor":69,"adjMinMagicArmor":69,"adjMaxMagicArmor":69,"adjHit":64,"adjDodge":64,"adjRealDmg":2,"adjRealDmgDef":1})
    }),
    51014070: _tools.RODict({
        "propID": 51014070,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":46614,"adjMinPhysicalAtk":237,"adjMaxPhysicalAtk":281,"adjMinMagicAtk":237,"adjMaxMagicAtk":281,"adjMinPhysicalArmor":71,"adjMaxPhysicalArmor":71,"adjMinMagicArmor":71,"adjMaxMagicArmor":71,"adjHit":64,"adjDodge":64,"adjRealDmg":2,"adjRealDmgDef":1})
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
    52002053: _tools.RODict({
        "propID": 52002053,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":1,"adjMaxPhysicalArmor":1,"adjMinMagicArmor":1,"adjMaxMagicArmor":1})
    }),
    52002054: _tools.RODict({
        "propID": 52002054,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":2,"adjMaxPhysicalArmor":2,"adjMinMagicArmor":2,"adjMaxMagicArmor":2})
    }),
    52002055: _tools.RODict({
        "propID": 52002055,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":3,"adjMaxPhysicalArmor":3,"adjMinMagicArmor":3,"adjMaxMagicArmor":3})
    }),
    52002056: _tools.RODict({
        "propID": 52002056,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":5,"adjMaxPhysicalArmor":5,"adjMinMagicArmor":5,"adjMaxMagicArmor":5})
    }),
    52002057: _tools.RODict({
        "propID": 52002057,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":7,"adjMaxPhysicalArmor":7,"adjMinMagicArmor":7,"adjMaxMagicArmor":7})
    }),
    52002058: _tools.RODict({
        "propID": 52002058,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":9,"adjMaxPhysicalArmor":9,"adjMinMagicArmor":9,"adjMaxMagicArmor":9})
    }),
    52002059: _tools.RODict({
        "propID": 52002059,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":12,"adjMaxPhysicalArmor":12,"adjMinMagicArmor":12,"adjMaxMagicArmor":12})
    }),
    52002060: _tools.RODict({
        "propID": 52002060,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":15,"adjMaxPhysicalArmor":15,"adjMinMagicArmor":15,"adjMaxMagicArmor":15})
    }),
    52002061: _tools.RODict({
        "propID": 52002061,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":19,"adjMaxPhysicalArmor":19,"adjMinMagicArmor":19,"adjMaxMagicArmor":19})
    }),
    52002062: _tools.RODict({
        "propID": 52002062,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":23,"adjMaxPhysicalArmor":23,"adjMinMagicArmor":23,"adjMaxMagicArmor":23,"adjExtraDmgDef":0.02})
    }),
    52002063: _tools.RODict({
        "propID": 52002063,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":28,"adjMaxPhysicalArmor":28,"adjMinMagicArmor":28,"adjMaxMagicArmor":28,"adjExtraDmgDef":0.04})
    }),
    52002064: _tools.RODict({
        "propID": 52002064,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":34,"adjMaxPhysicalArmor":34,"adjMinMagicArmor":34,"adjMaxMagicArmor":34,"adjExtraDmgDef":0.07})
    }),
    52002065: _tools.RODict({
        "propID": 52002065,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":41,"adjMaxPhysicalArmor":41,"adjMinMagicArmor":41,"adjMaxMagicArmor":41,"adjExtraDmgDef":0.12})
    }),
    52002066: _tools.RODict({
        "propID": 52002066,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":1,"adjMaxMagicAtk":1})
    }),
    52002067: _tools.RODict({
        "propID": 52002067,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":2,"adjMaxMagicAtk":2})
    }),
    52002068: _tools.RODict({
        "propID": 52002068,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":4,"adjMaxMagicAtk":4})
    }),
    52002069: _tools.RODict({
        "propID": 52002069,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":6,"adjMaxMagicAtk":6})
    }),
    52002070: _tools.RODict({
        "propID": 52002070,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":9,"adjMaxMagicAtk":9})
    }),
    52002071: _tools.RODict({
        "propID": 52002071,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":12,"adjMaxMagicAtk":12})
    }),
    52002072: _tools.RODict({
        "propID": 52002072,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":16,"adjMaxMagicAtk":16})
    }),
    52002073: _tools.RODict({
        "propID": 52002073,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":21,"adjMaxMagicAtk":21})
    }),
    52002074: _tools.RODict({
        "propID": 52002074,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":27,"adjMaxMagicAtk":27})
    }),
    52002075: _tools.RODict({
        "propID": 52002075,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":35,"adjMaxMagicAtk":35,"adjExtraDmg":0.01})
    }),
    52002076: _tools.RODict({
        "propID": 52002076,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":45,"adjMaxMagicAtk":45,"adjExtraDmg":0.02})
    }),
    52002077: _tools.RODict({
        "propID": 52002077,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":57,"adjMaxMagicAtk":57,"adjExtraDmg":0.04})
    }),
    52002078: _tools.RODict({
        "propID": 52002078,
        "type": 2,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":72,"adjMaxMagicAtk":72,"adjExtraDmg":0.07})
    }),
    52002079: _tools.RODict({
        "propID": 52002079,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":5})
    }),
    52002080: _tools.RODict({
        "propID": 52002080,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":13})
    }),
    52002081: _tools.RODict({
        "propID": 52002081,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":23})
    }),
    52002082: _tools.RODict({
        "propID": 52002082,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":35})
    }),
    52002083: _tools.RODict({
        "propID": 52002083,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":49})
    }),
    52002084: _tools.RODict({
        "propID": 52002084,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":64})
    }),
    52002085: _tools.RODict({
        "propID": 52002085,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":80})
    }),
    52002086: _tools.RODict({
        "propID": 52002086,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":97})
    }),
    52002087: _tools.RODict({
        "propID": 52002087,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":115})
    }),
    52002088: _tools.RODict({
        "propID": 52002088,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":134,"mulMaxPhysicalAtk":0.01,"mulMaxMagicAtk":0.01})
    }),
    52002089: _tools.RODict({
        "propID": 52002089,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":154,"mulMaxPhysicalAtk":0.02,"mulMaxMagicAtk":0.02})
    }),
    52002090: _tools.RODict({
        "propID": 52002090,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":176,"mulMaxPhysicalAtk":0.04,"mulMaxMagicAtk":0.04})
    }),
    52002091: _tools.RODict({
        "propID": 52002091,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":200,"mulMaxPhysicalAtk":0.07,"mulMaxMagicAtk":0.07})
    }),
    52002092: _tools.RODict({
        "propID": 52002092,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":990000,"adjMinPhysicalAtk":170,"adjMaxPhysicalAtk":189,"adjMinMagicAtk":170,"adjMaxMagicAtk":189,"adjMinPhysicalArmor":15,"adjMaxPhysicalArmor":15,"adjMinMagicArmor":15,"adjMaxMagicArmor":15,"adjHit":109,"adjDodge":34,"adjRealDmg":3,"adjRealDmgDef":1,"adjDebilityEnh":13,"adjDebilityAnti":13})
    }),
    52002093: _tools.RODict({
        "propID": 52002093,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2800,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":41,"adjMinMagicAtk":23,"adjMaxMagicAtk":41,"adjMinPhysicalArmor":15,"adjMaxPhysicalArmor":15,"adjMinMagicArmor":15,"adjMaxMagicArmor":15})
    }),
    51015001: _tools.RODict({
        "propID": 51015001,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1360,"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":56,"adjMinMagicAtk":30,"adjMaxMagicAtk":56,"adjHit":1,"adjDodge":1})
    }),
    51015002: _tools.RODict({
        "propID": 51015002,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1425,"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":57,"adjMinMagicAtk":32,"adjMaxMagicAtk":57,"adjHit":2,"adjDodge":2})
    }),
    51015003: _tools.RODict({
        "propID": 51015003,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1495,"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":59,"adjMinMagicAtk":32,"adjMaxMagicAtk":59,"adjHit":3,"adjDodge":3})
    }),
    51015004: _tools.RODict({
        "propID": 51015004,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1560,"adjMinPhysicalAtk":33,"adjMaxPhysicalAtk":60,"adjMinMagicAtk":33,"adjMaxMagicAtk":60,"adjHit":4,"adjDodge":4})
    }),
    51015005: _tools.RODict({
        "propID": 51015005,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1630,"adjMinPhysicalAtk":35,"adjMaxPhysicalAtk":62,"adjMinMagicAtk":35,"adjMaxMagicAtk":62,"adjHit":5,"adjDodge":5})
    }),
    51015006: _tools.RODict({
        "propID": 51015006,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1695,"adjMinPhysicalAtk":36,"adjMaxPhysicalAtk":65,"adjMinMagicAtk":36,"adjMaxMagicAtk":65,"adjHit":6,"adjDodge":6})
    }),
    51015007: _tools.RODict({
        "propID": 51015007,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1765,"adjMinPhysicalAtk":36,"adjMaxPhysicalAtk":66,"adjMinMagicAtk":36,"adjMaxMagicAtk":66,"adjHit":7,"adjDodge":7})
    }),
    51015008: _tools.RODict({
        "propID": 51015008,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1835,"adjMinPhysicalAtk":38,"adjMaxPhysicalAtk":68,"adjMinMagicAtk":38,"adjMaxMagicAtk":68,"adjHit":8,"adjDodge":8})
    }),
    51015009: _tools.RODict({
        "propID": 51015009,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1900,"adjMinPhysicalAtk":38,"adjMaxPhysicalAtk":69,"adjMinMagicAtk":38,"adjMaxMagicAtk":69,"adjHit":9,"adjDodge":9})
    }),
    51015010: _tools.RODict({
        "propID": 51015010,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1970,"adjMinPhysicalAtk":39,"adjMaxPhysicalAtk":71,"adjMinMagicAtk":39,"adjMaxMagicAtk":71,"adjHit":10,"adjDodge":10})
    }),
    51015011: _tools.RODict({
        "propID": 51015011,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1475,"adjMinPhysicalAtk":15,"adjMaxPhysicalAtk":27,"adjMinMagicAtk":15,"adjMaxMagicAtk":27,"adjMinPhysicalArmor":1,"adjMaxPhysicalArmor":1,"adjMinMagicArmor":1,"adjMaxMagicArmor":1,"adjHit":4})
    }),
    51015012: _tools.RODict({
        "propID": 51015012,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1520,"adjMinPhysicalAtk":15,"adjMaxPhysicalAtk":29,"adjMinMagicAtk":15,"adjMaxMagicAtk":29,"adjMinPhysicalArmor":2,"adjMaxPhysicalArmor":2,"adjMinMagicArmor":2,"adjMaxMagicArmor":2,"adjHit":4})
    }),
    51015013: _tools.RODict({
        "propID": 51015013,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1595,"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":30,"adjMinMagicAtk":17,"adjMaxMagicAtk":30,"adjMinPhysicalArmor":3,"adjMaxPhysicalArmor":3,"adjMinMagicArmor":3,"adjMaxMagicArmor":3,"adjHit":5})
    }),
    51015014: _tools.RODict({
        "propID": 51015014,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1640,"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":30,"adjMinMagicAtk":17,"adjMaxMagicAtk":30,"adjMinPhysicalArmor":4,"adjMaxPhysicalArmor":4,"adjMinMagicArmor":4,"adjMaxMagicArmor":4,"adjHit":5})
    }),
    51015015: _tools.RODict({
        "propID": 51015015,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":1980,"adjMinPhysicalAtk":18,"adjMaxPhysicalAtk":32,"adjMinMagicAtk":18,"adjMaxMagicAtk":32,"adjMinPhysicalArmor":5,"adjMaxPhysicalArmor":5,"adjMinMagicArmor":5,"adjMaxMagicArmor":5,"adjHit":5})
    }),
    51015016: _tools.RODict({
        "propID": 51015016,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2035,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":35,"adjMinMagicAtk":20,"adjMaxMagicAtk":35,"adjMinPhysicalArmor":6,"adjMaxPhysicalArmor":6,"adjMinMagicArmor":6,"adjMaxMagicArmor":6,"adjHit":5})
    }),
    51015017: _tools.RODict({
        "propID": 51015017,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2120,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":38,"adjMinMagicAtk":21,"adjMaxMagicAtk":38,"adjMinPhysicalArmor":8,"adjMaxPhysicalArmor":8,"adjMinMagicArmor":8,"adjMaxMagicArmor":8,"adjHit":5})
    }),
    51015018: _tools.RODict({
        "propID": 51015018,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2180,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":38,"adjMinMagicAtk":21,"adjMaxMagicAtk":38,"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10,"adjHit":6})
    }),
    51015019: _tools.RODict({
        "propID": 51015019,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2265,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":39,"adjMinMagicAtk":21,"adjMaxMagicAtk":39,"adjMinPhysicalArmor":14,"adjMaxPhysicalArmor":14,"adjMinMagicArmor":14,"adjMaxMagicArmor":14,"adjHit":6})
    }),
    51015020: _tools.RODict({
        "propID": 51015020,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2505,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":39,"adjMinMagicAtk":21,"adjMaxMagicAtk":39,"adjMinPhysicalArmor":15,"adjMaxPhysicalArmor":15,"adjMinMagicArmor":15,"adjMaxMagicArmor":15,"adjHit":6})
    }),
    51015021: _tools.RODict({
        "propID": 51015021,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2630,"adjMinPhysicalAtk":27,"adjMaxPhysicalAtk":50,"adjMinMagicAtk":27,"adjMaxMagicAtk":50,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjHit":6,"adjDebilityAnti":1})
    }),
    51015022: _tools.RODict({
        "propID": 51015022,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2695,"adjMinPhysicalAtk":27,"adjMaxPhysicalAtk":50,"adjMinMagicAtk":27,"adjMaxMagicAtk":50,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjHit":10,"adjDebilityAnti":1})
    }),
    51015023: _tools.RODict({
        "propID": 51015023,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2920,"adjMinPhysicalAtk":29,"adjMaxPhysicalAtk":51,"adjMinMagicAtk":29,"adjMaxMagicAtk":51,"adjMinPhysicalArmor":17,"adjMaxPhysicalArmor":17,"adjMinMagicArmor":17,"adjMaxMagicArmor":17,"adjHit":10,"adjDebilityAnti":1})
    }),
    51015024: _tools.RODict({
        "propID": 51015024,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3120,"adjMinPhysicalAtk":29,"adjMaxPhysicalAtk":51,"adjMinMagicAtk":29,"adjMaxMagicAtk":51,"adjMinPhysicalArmor":18,"adjMaxPhysicalArmor":18,"adjMinMagicArmor":18,"adjMaxMagicArmor":18,"adjHit":10,"adjDebilityAnti":1})
    }),
    51015025: _tools.RODict({
        "propID": 51015025,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3700,"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":59,"adjMinMagicAtk":32,"adjMaxMagicAtk":59,"adjMinPhysicalArmor":20,"adjMaxPhysicalArmor":20,"adjMinMagicArmor":20,"adjMaxMagicArmor":20,"adjHit":10,"adjDebilityAnti":2})
    }),
    51015026: _tools.RODict({
        "propID": 51015026,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3780,"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":59,"adjMinMagicAtk":32,"adjMaxMagicAtk":59,"adjMinPhysicalArmor":21,"adjMaxPhysicalArmor":21,"adjMinMagicArmor":21,"adjMaxMagicArmor":21,"adjHit":12,"adjDebilityAnti":2})
    }),
    51015027: _tools.RODict({
        "propID": 51015027,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3900,"adjMinPhysicalAtk":33,"adjMaxPhysicalAtk":60,"adjMinMagicAtk":33,"adjMaxMagicAtk":60,"adjMinPhysicalArmor":21,"adjMaxPhysicalArmor":21,"adjMinMagicArmor":21,"adjMaxMagicArmor":21,"adjHit":12,"adjDebilityAnti":2})
    }),
    51015028: _tools.RODict({
        "propID": 51015028,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4130,"adjMinPhysicalAtk":33,"adjMaxPhysicalAtk":60,"adjMinMagicAtk":33,"adjMaxMagicAtk":60,"adjMinPhysicalArmor":22,"adjMaxPhysicalArmor":22,"adjMinMagicArmor":22,"adjMaxMagicArmor":22,"adjHit":12,"adjDebilityAnti":2})
    }),
    51015029: _tools.RODict({
        "propID": 51015029,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4730,"adjMinPhysicalAtk":36,"adjMaxPhysicalAtk":65,"adjMinMagicAtk":36,"adjMaxMagicAtk":65,"adjMinPhysicalArmor":23,"adjMaxPhysicalArmor":23,"adjMinMagicArmor":23,"adjMaxMagicArmor":23,"adjHit":12,"adjDebilityAnti":3})
    }),
    51015030: _tools.RODict({
        "propID": 51015030,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":20555,"adjMinPhysicalAtk":371,"adjMaxPhysicalAtk":371,"adjMinMagicAtk":371,"adjMaxMagicAtk":371,"adjMinPhysicalArmor":62,"adjMaxPhysicalArmor":62,"adjMinMagicArmor":62,"adjMaxMagicArmor":62,"adjHit":14,"adjDodge":14,"adjDebilityAnti":3})
    }),
    51015031: _tools.RODict({
        "propID": 51015031,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":21065,"adjMinPhysicalAtk":374,"adjMaxPhysicalAtk":374,"adjMinMagicAtk":374,"adjMaxMagicAtk":374,"adjMinPhysicalArmor":62,"adjMaxPhysicalArmor":62,"adjMinMagicArmor":62,"adjMaxMagicArmor":62,"adjHit":14,"adjDodge":14,"adjRealDmg":1,"adjDebilityAnti":3})
    }),
    51015032: _tools.RODict({
        "propID": 51015032,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":21585,"adjMinPhysicalAtk":377,"adjMaxPhysicalAtk":377,"adjMinMagicAtk":377,"adjMaxMagicAtk":377,"adjMinPhysicalArmor":62,"adjMaxPhysicalArmor":62,"adjMinMagicArmor":62,"adjMaxMagicArmor":62,"adjHit":14,"adjDodge":14,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":3})
    }),
    51015033: _tools.RODict({
        "propID": 51015033,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":22105,"adjMinPhysicalAtk":380,"adjMaxPhysicalAtk":380,"adjMinMagicAtk":380,"adjMaxMagicAtk":380,"adjMinPhysicalArmor":62,"adjMaxPhysicalArmor":62,"adjMinMagicArmor":62,"adjMaxMagicArmor":62,"adjHit":14,"adjDodge":14,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":4})
    }),
    51015034: _tools.RODict({
        "propID": 51015034,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":22630,"adjMinPhysicalAtk":381,"adjMaxPhysicalAtk":381,"adjMinMagicAtk":381,"adjMaxMagicAtk":381,"adjMinPhysicalArmor":63,"adjMaxPhysicalArmor":63,"adjMinMagicArmor":63,"adjMaxMagicArmor":63,"adjHit":14,"adjDodge":14,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":4})
    }),
    51015035: _tools.RODict({
        "propID": 51015035,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":23160,"adjMinPhysicalAtk":386,"adjMaxPhysicalAtk":386,"adjMinMagicAtk":386,"adjMaxMagicAtk":386,"adjMinPhysicalArmor":63,"adjMaxPhysicalArmor":63,"adjMinMagicArmor":63,"adjMaxMagicArmor":63,"adjHit":14,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":1,"adjDebilityAnti":4})
    }),
    51015036: _tools.RODict({
        "propID": 51015036,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":23690,"adjMinPhysicalAtk":389,"adjMaxPhysicalAtk":389,"adjMinMagicAtk":389,"adjMaxMagicAtk":389,"adjMinPhysicalArmor":63,"adjMaxPhysicalArmor":63,"adjMinMagicArmor":63,"adjMaxMagicArmor":63,"adjHit":14,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":2,"adjDebilityAnti":4})
    }),
    51015037: _tools.RODict({
        "propID": 51015037,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":24230,"adjMinPhysicalAtk":392,"adjMaxPhysicalAtk":392,"adjMinMagicAtk":392,"adjMaxMagicAtk":392,"adjMinPhysicalArmor":64,"adjMaxPhysicalArmor":64,"adjMinMagicArmor":64,"adjMaxMagicArmor":64,"adjHit":14,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":2,"adjDebilityAnti":4})
    }),
    51015038: _tools.RODict({
        "propID": 51015038,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":24770,"adjMinPhysicalAtk":395,"adjMaxPhysicalAtk":395,"adjMinMagicAtk":395,"adjMaxMagicAtk":395,"adjMinPhysicalArmor":64,"adjMaxPhysicalArmor":64,"adjMinMagicArmor":64,"adjMaxMagicArmor":64,"adjHit":14,"adjDodge":14,"adjRealDmg":3,"adjRealDmgDef":2,"adjDebilityAnti":5})
    }),
    51015039: _tools.RODict({
        "propID": 51015039,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":25315,"adjMinPhysicalAtk":398,"adjMaxPhysicalAtk":398,"adjMinMagicAtk":398,"adjMaxMagicAtk":398,"adjMinPhysicalArmor":64,"adjMaxPhysicalArmor":64,"adjMinMagicArmor":64,"adjMaxMagicArmor":64,"adjHit":14,"adjDodge":14,"adjRealDmg":3,"adjRealDmgDef":3,"adjDebilityEnh":5,"adjDebilityAnti":5})
    }),
    51015040: _tools.RODict({
        "propID": 51015040,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":25865,"adjMinPhysicalAtk":401,"adjMaxPhysicalAtk":401,"adjMinMagicAtk":401,"adjMaxMagicAtk":401,"adjMinPhysicalArmor":65,"adjMaxPhysicalArmor":65,"adjMinMagicArmor":65,"adjMaxMagicArmor":65,"adjHit":14,"adjDodge":14,"adjRealDmg":3,"adjRealDmgDef":3,"adjDebilityEnh":5,"adjDebilityAnti":5})
    }),
    51015041: _tools.RODict({
        "propID": 51015041,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":10585,"adjMinPhysicalAtk":57,"adjMaxPhysicalAtk":104,"adjMinMagicAtk":57,"adjMaxMagicAtk":104,"adjMinPhysicalArmor":38,"adjMaxPhysicalArmor":38,"adjMinMagicArmor":38,"adjMaxMagicArmor":38,"adjHit":23,"adjRealDmg":3,"adjRealDmgDef":3,"adjDebilityEnh":5,"adjDebilityAnti":5})
    }),
    51015042: _tools.RODict({
        "propID": 51015042,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":10755,"adjMinPhysicalAtk":60,"adjMaxPhysicalAtk":108,"adjMinMagicAtk":60,"adjMaxMagicAtk":108,"adjMinPhysicalArmor":38,"adjMaxPhysicalArmor":38,"adjMinMagicArmor":38,"adjMaxMagicArmor":38,"adjHit":23,"adjRealDmg":4,"adjRealDmgDef":3,"adjDebilityEnh":5,"adjDebilityAnti":5})
    }),
    51015043: _tools.RODict({
        "propID": 51015043,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":10975,"adjMinPhysicalAtk":63,"adjMaxPhysicalAtk":114,"adjMinMagicAtk":63,"adjMaxMagicAtk":114,"adjMinPhysicalArmor":38,"adjMaxPhysicalArmor":38,"adjMinMagicArmor":38,"adjMaxMagicArmor":38,"adjHit":25,"adjRealDmg":4,"adjRealDmgDef":4,"adjDebilityEnh":5,"adjDebilityAnti":6})
    }),
    51015044: _tools.RODict({
        "propID": 51015044,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":11345,"adjMinPhysicalAtk":65,"adjMaxPhysicalAtk":117,"adjMinMagicAtk":65,"adjMaxMagicAtk":117,"adjMinPhysicalArmor":39,"adjMaxPhysicalArmor":39,"adjMinMagicArmor":39,"adjMaxMagicArmor":39,"adjHit":26,"adjRealDmg":4,"adjRealDmgDef":4,"adjDebilityEnh":6,"adjDebilityAnti":6})
    }),
    51015045: _tools.RODict({
        "propID": 51015045,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":11765,"adjMinPhysicalAtk":68,"adjMaxPhysicalAtk":122,"adjMinMagicAtk":68,"adjMaxMagicAtk":122,"adjMinPhysicalArmor":39,"adjMaxPhysicalArmor":39,"adjMinMagicArmor":39,"adjMaxMagicArmor":39,"adjHit":26,"adjRealDmg":4,"adjRealDmgDef":4,"adjDebilityEnh":6,"adjDebilityAnti":6})
    }),
    51015046: _tools.RODict({
        "propID": 51015046,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":13095,"adjMinPhysicalAtk":68,"adjMaxPhysicalAtk":122,"adjMinMagicAtk":68,"adjMaxMagicAtk":122,"adjMinPhysicalArmor":42,"adjMaxPhysicalArmor":42,"adjMinMagicArmor":42,"adjMaxMagicArmor":42,"adjHit":26,"adjRealDmg":4,"adjRealDmgDef":4,"adjDebilityEnh":6,"adjDebilityAnti":6})
    }),
    51015047: _tools.RODict({
        "propID": 51015047,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":13340,"adjMinPhysicalAtk":72,"adjMaxPhysicalAtk":131,"adjMinMagicAtk":72,"adjMaxMagicAtk":131,"adjMinPhysicalArmor":42,"adjMaxPhysicalArmor":42,"adjMinMagicArmor":42,"adjMaxMagicArmor":42,"adjHit":26,"adjRealDmg":5,"adjRealDmgDef":4,"adjDebilityEnh":6,"adjDebilityAnti":6})
    }),
    51015048: _tools.RODict({
        "propID": 51015048,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":13540,"adjMinPhysicalAtk":72,"adjMaxPhysicalAtk":132,"adjMinMagicAtk":72,"adjMaxMagicAtk":132,"adjMinPhysicalArmor":43,"adjMaxPhysicalArmor":43,"adjMinMagicArmor":43,"adjMaxMagicArmor":43,"adjHit":30,"adjRealDmg":5,"adjRealDmgDef":5,"adjDebilityEnh":6,"adjDebilityAnti":7})
    }),
    51015049: _tools.RODict({
        "propID": 51015049,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":14470,"adjMinPhysicalAtk":75,"adjMaxPhysicalAtk":137,"adjMinMagicAtk":75,"adjMaxMagicAtk":137,"adjMinPhysicalArmor":44,"adjMaxPhysicalArmor":44,"adjMinMagicArmor":44,"adjMaxMagicArmor":44,"adjHit":30,"adjRealDmg":5,"adjRealDmgDef":5,"adjDebilityEnh":7,"adjDebilityAnti":7})
    }),
    51015050: _tools.RODict({
        "propID": 51015050,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":15050,"adjMinPhysicalAtk":80,"adjMaxPhysicalAtk":144,"adjMinMagicAtk":80,"adjMaxMagicAtk":144,"adjMinPhysicalArmor":45,"adjMaxPhysicalArmor":45,"adjMinMagicArmor":45,"adjMaxMagicArmor":45,"adjHit":32,"adjRealDmg":5,"adjRealDmgDef":5,"adjDebilityEnh":7,"adjDebilityAnti":7})
    }),
    51015051: _tools.RODict({
        "propID": 51015051,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":16390,"adjMinPhysicalAtk":80,"adjMaxPhysicalAtk":146,"adjMinMagicAtk":80,"adjMaxMagicAtk":146,"adjMinPhysicalArmor":49,"adjMaxPhysicalArmor":49,"adjMinMagicArmor":49,"adjMaxMagicArmor":49,"adjHit":32,"adjRealDmg":5,"adjRealDmgDef":5,"adjDebilityEnh":7,"adjDebilityAnti":7})
    }),
    51015052: _tools.RODict({
        "propID": 51015052,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":17055,"adjMinPhysicalAtk":83,"adjMaxPhysicalAtk":150,"adjMinMagicAtk":83,"adjMaxMagicAtk":150,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":50,"adjMaxMagicArmor":50,"adjHit":32,"adjRealDmg":6,"adjRealDmgDef":5,"adjDebilityEnh":7,"adjDebilityAnti":7})
    }),
    51015053: _tools.RODict({
        "propID": 51015053,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":17345,"adjMinPhysicalAtk":86,"adjMaxPhysicalAtk":155,"adjMinMagicAtk":86,"adjMaxMagicAtk":155,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":50,"adjMaxMagicArmor":50,"adjHit":34,"adjRealDmg":6,"adjRealDmgDef":6,"adjDebilityEnh":7,"adjDebilityAnti":8})
    }),
    51015054: _tools.RODict({
        "propID": 51015054,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":17860,"adjMinPhysicalAtk":89,"adjMaxPhysicalAtk":162,"adjMinMagicAtk":89,"adjMaxMagicAtk":162,"adjMinPhysicalArmor":51,"adjMaxPhysicalArmor":51,"adjMinMagicArmor":51,"adjMaxMagicArmor":51,"adjHit":34,"adjRealDmg":6,"adjRealDmgDef":6,"adjDebilityEnh":8,"adjDebilityAnti":8})
    }),
    51015055: _tools.RODict({
        "propID": 51015055,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":18445,"adjMinPhysicalAtk":93,"adjMaxPhysicalAtk":168,"adjMinMagicAtk":93,"adjMaxMagicAtk":168,"adjMinPhysicalArmor":52,"adjMaxPhysicalArmor":52,"adjMinMagicArmor":52,"adjMaxMagicArmor":52,"adjHit":37,"adjRealDmg":6,"adjRealDmgDef":6,"adjDebilityEnh":8,"adjDebilityAnti":8})
    }),
    51015056: _tools.RODict({
        "propID": 51015056,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":20065,"adjMinPhysicalAtk":93,"adjMaxPhysicalAtk":168,"adjMinMagicAtk":93,"adjMaxMagicAtk":168,"adjMinPhysicalArmor":56,"adjMaxPhysicalArmor":56,"adjMinMagicArmor":56,"adjMaxMagicArmor":56,"adjHit":37,"adjRealDmg":6,"adjRealDmgDef":6,"adjDebilityEnh":8,"adjDebilityAnti":8})
    }),
    51015057: _tools.RODict({
        "propID": 51015057,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":20910,"adjMinPhysicalAtk":96,"adjMaxPhysicalAtk":174,"adjMinMagicAtk":96,"adjMaxMagicAtk":174,"adjMinPhysicalArmor":57,"adjMaxPhysicalArmor":57,"adjMinMagicArmor":57,"adjMaxMagicArmor":57,"adjHit":37,"adjRealDmg":7,"adjRealDmgDef":6,"adjDebilityEnh":8,"adjDebilityAnti":8})
    }),
    51015058: _tools.RODict({
        "propID": 51015058,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":21180,"adjMinPhysicalAtk":98,"adjMaxPhysicalAtk":177,"adjMinMagicAtk":98,"adjMaxMagicAtk":177,"adjMinPhysicalArmor":57,"adjMaxPhysicalArmor":57,"adjMinMagicArmor":57,"adjMaxMagicArmor":57,"adjHit":39,"adjRealDmg":7,"adjRealDmgDef":7,"adjDebilityEnh":8,"adjDebilityAnti":9})
    }),
    51015059: _tools.RODict({
        "propID": 51015059,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":22110,"adjMinPhysicalAtk":104,"adjMaxPhysicalAtk":189,"adjMinMagicAtk":104,"adjMaxMagicAtk":189,"adjMinPhysicalArmor":58,"adjMaxPhysicalArmor":58,"adjMinMagicArmor":58,"adjMaxMagicArmor":58,"adjHit":39,"adjRealDmg":7,"adjRealDmgDef":7,"adjDebilityEnh":9,"adjDebilityAnti":9})
    }),
    51015060: _tools.RODict({
        "propID": 51015060,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":22990,"adjMinPhysicalAtk":107,"adjMaxPhysicalAtk":194,"adjMinMagicAtk":107,"adjMaxMagicAtk":194,"adjMinPhysicalArmor":59,"adjMaxPhysicalArmor":59,"adjMinMagicArmor":59,"adjMaxMagicArmor":59,"adjHit":42,"adjRealDmg":7,"adjRealDmgDef":7,"adjDebilityEnh":9,"adjDebilityAnti":9})
    }),
    51015061: _tools.RODict({
        "propID": 51015061,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":25905,"adjMinPhysicalAtk":108,"adjMaxPhysicalAtk":195,"adjMinMagicAtk":108,"adjMaxMagicAtk":195,"adjMinPhysicalArmor":66,"adjMaxPhysicalArmor":66,"adjMinMagicArmor":66,"adjMaxMagicArmor":66,"adjHit":42,"adjRealDmg":7,"adjRealDmgDef":7,"adjDebilityEnh":9,"adjDebilityAnti":9})
    }),
    51015062: _tools.RODict({
        "propID": 51015062,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":26845,"adjMinPhysicalAtk":114,"adjMaxPhysicalAtk":209,"adjMinMagicAtk":114,"adjMaxMagicAtk":209,"adjMinPhysicalArmor":68,"adjMaxPhysicalArmor":68,"adjMinMagicArmor":68,"adjMaxMagicArmor":68,"adjHit":42,"adjRealDmg":9,"adjRealDmgDef":7,"adjDebilityEnh":9,"adjDebilityAnti":9})
    }),
    51015063: _tools.RODict({
        "propID": 51015063,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":27235,"adjMinPhysicalAtk":119,"adjMaxPhysicalAtk":216,"adjMinMagicAtk":119,"adjMaxMagicAtk":216,"adjMinPhysicalArmor":68,"adjMaxPhysicalArmor":68,"adjMinMagicArmor":68,"adjMaxMagicArmor":68,"adjHit":48,"adjRealDmg":9,"adjRealDmgDef":9,"adjDebilityEnh":9,"adjDebilityAnti":11})
    }),
    51015064: _tools.RODict({
        "propID": 51015064,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":28640,"adjMinPhysicalAtk":125,"adjMaxPhysicalAtk":227,"adjMinMagicAtk":125,"adjMaxMagicAtk":227,"adjMinPhysicalArmor":69,"adjMaxPhysicalArmor":69,"adjMinMagicArmor":69,"adjMaxMagicArmor":69,"adjHit":48,"adjRealDmg":9,"adjRealDmgDef":9,"adjDebilityEnh":11,"adjDebilityAnti":11})
    }),
    51015065: _tools.RODict({
        "propID": 51015065,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":30135,"adjMinPhysicalAtk":128,"adjMaxPhysicalAtk":233,"adjMinMagicAtk":128,"adjMaxMagicAtk":233,"adjMinPhysicalArmor":70,"adjMaxPhysicalArmor":70,"adjMinMagicArmor":70,"adjMaxMagicArmor":70,"adjHit":52,"adjRealDmg":9,"adjRealDmgDef":9,"adjDebilityEnh":11,"adjDebilityAnti":11})
    }),
    51015066: _tools.RODict({
        "propID": 51015066,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":32695,"adjMinPhysicalAtk":128,"adjMaxPhysicalAtk":233,"adjMinMagicAtk":128,"adjMaxMagicAtk":233,"adjMinPhysicalArmor":76,"adjMaxPhysicalArmor":76,"adjMinMagicArmor":76,"adjMaxMagicArmor":76,"adjHit":52,"adjRealDmg":9,"adjRealDmgDef":9,"adjDebilityEnh":11,"adjDebilityAnti":11})
    }),
    51015067: _tools.RODict({
        "propID": 51015067,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":33860,"adjMinPhysicalAtk":135,"adjMaxPhysicalAtk":245,"adjMinMagicAtk":135,"adjMaxMagicAtk":245,"adjMinPhysicalArmor":78,"adjMaxPhysicalArmor":78,"adjMinMagicArmor":78,"adjMaxMagicArmor":78,"adjHit":52,"adjRealDmg":11,"adjRealDmgDef":9,"adjDebilityEnh":11,"adjDebilityAnti":11})
    }),
    51015068: _tools.RODict({
        "propID": 51015068,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":34250,"adjMinPhysicalAtk":137,"adjMaxPhysicalAtk":249,"adjMinMagicAtk":137,"adjMaxMagicAtk":249,"adjMinPhysicalArmor":79,"adjMaxPhysicalArmor":79,"adjMinMagicArmor":79,"adjMaxMagicArmor":79,"adjHit":54,"adjRealDmg":11,"adjRealDmgDef":11,"adjDebilityEnh":11,"adjDebilityAnti":12})
    }),
    51015069: _tools.RODict({
        "propID": 51015069,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":35515,"adjMinPhysicalAtk":146,"adjMaxPhysicalAtk":264,"adjMinMagicAtk":146,"adjMaxMagicAtk":264,"adjMinPhysicalArmor":79,"adjMaxPhysicalArmor":79,"adjMinMagicArmor":79,"adjMaxMagicArmor":79,"adjHit":54,"adjRealDmg":11,"adjRealDmgDef":11,"adjDebilityEnh":12,"adjDebilityAnti":12})
    }),
    51015070: _tools.RODict({
        "propID": 51015070,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":36725,"adjMinPhysicalAtk":149,"adjMaxPhysicalAtk":270,"adjMinMagicAtk":149,"adjMaxMagicAtk":270,"adjMinPhysicalArmor":80,"adjMaxPhysicalArmor":80,"adjMinMagicArmor":80,"adjMaxMagicArmor":80,"adjHit":58,"adjRealDmg":11,"adjRealDmgDef":11,"adjDebilityEnh":12,"adjDebilityAnti":12})
    }),
    51016001: _tools.RODict({
        "propID": 51016001,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":2992,"adjMinPhysicalAtk":36,"adjMaxPhysicalAtk":67,"adjMinMagicAtk":36,"adjMaxMagicAtk":67,"adjHit":1,"adjDodge":1})
    }),
    51016002: _tools.RODict({
        "propID": 51016002,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3135,"adjMinPhysicalAtk":38,"adjMaxPhysicalAtk":68,"adjMinMagicAtk":38,"adjMaxMagicAtk":68,"adjHit":2,"adjDodge":2})
    }),
    51016003: _tools.RODict({
        "propID": 51016003,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3289,"adjMinPhysicalAtk":38,"adjMaxPhysicalAtk":71,"adjMinMagicAtk":38,"adjMaxMagicAtk":71,"adjHit":3,"adjDodge":3})
    }),
    51016004: _tools.RODict({
        "propID": 51016004,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3432,"adjMinPhysicalAtk":40,"adjMaxPhysicalAtk":72,"adjMinMagicAtk":40,"adjMaxMagicAtk":72,"adjHit":4,"adjDodge":4})
    }),
    51016005: _tools.RODict({
        "propID": 51016005,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3586,"adjMinPhysicalAtk":42,"adjMaxPhysicalAtk":74,"adjMinMagicAtk":42,"adjMaxMagicAtk":74,"adjHit":5,"adjDodge":5})
    }),
    51016006: _tools.RODict({
        "propID": 51016006,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3729,"adjMinPhysicalAtk":43,"adjMaxPhysicalAtk":78,"adjMinMagicAtk":43,"adjMaxMagicAtk":78,"adjHit":6,"adjDodge":6})
    }),
    51016007: _tools.RODict({
        "propID": 51016007,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3883,"adjMinPhysicalAtk":43,"adjMaxPhysicalAtk":79,"adjMinMagicAtk":43,"adjMaxMagicAtk":79,"adjHit":7,"adjDodge":7})
    }),
    51016008: _tools.RODict({
        "propID": 51016008,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4037,"adjMinPhysicalAtk":46,"adjMaxPhysicalAtk":82,"adjMinMagicAtk":46,"adjMaxMagicAtk":82,"adjHit":8,"adjDodge":8})
    }),
    51016009: _tools.RODict({
        "propID": 51016009,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4180,"adjMinPhysicalAtk":46,"adjMaxPhysicalAtk":83,"adjMinMagicAtk":46,"adjMaxMagicAtk":83,"adjHit":9,"adjDodge":9})
    }),
    51016010: _tools.RODict({
        "propID": 51016010,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4334,"adjMinPhysicalAtk":47,"adjMaxPhysicalAtk":85,"adjMinMagicAtk":47,"adjMaxMagicAtk":85,"adjHit":10,"adjDodge":10})
    }),
    51016011: _tools.RODict({
        "propID": 51016011,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3245,"adjMinPhysicalAtk":18,"adjMaxPhysicalAtk":32,"adjMinMagicAtk":18,"adjMaxMagicAtk":32,"adjMinPhysicalArmor":1,"adjMaxPhysicalArmor":1,"adjMinMagicArmor":1,"adjMaxMagicArmor":1,"adjHit":4})
    }),
    51016012: _tools.RODict({
        "propID": 51016012,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3344,"adjMinPhysicalAtk":18,"adjMaxPhysicalAtk":35,"adjMinMagicAtk":18,"adjMaxMagicAtk":35,"adjMinPhysicalArmor":2,"adjMaxPhysicalArmor":2,"adjMinMagicArmor":2,"adjMaxMagicArmor":2,"adjHit":4})
    }),
    51016013: _tools.RODict({
        "propID": 51016013,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3509,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":36,"adjMinMagicAtk":20,"adjMaxMagicAtk":36,"adjMinPhysicalArmor":3,"adjMaxPhysicalArmor":3,"adjMinMagicArmor":3,"adjMaxMagicArmor":3,"adjHit":5})
    }),
    51016014: _tools.RODict({
        "propID": 51016014,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":3608,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":36,"adjMinMagicAtk":20,"adjMaxMagicAtk":36,"adjMinPhysicalArmor":4,"adjMaxPhysicalArmor":4,"adjMinMagicArmor":4,"adjMaxMagicArmor":4,"adjHit":5})
    }),
    51016015: _tools.RODict({
        "propID": 51016015,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4356,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":38,"adjMinMagicAtk":22,"adjMaxMagicAtk":38,"adjMinPhysicalArmor":5,"adjMaxPhysicalArmor":5,"adjMinMagicArmor":5,"adjMaxMagicArmor":5,"adjHit":5})
    }),
    51016016: _tools.RODict({
        "propID": 51016016,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4477,"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":42,"adjMinMagicAtk":24,"adjMaxMagicAtk":42,"adjMinPhysicalArmor":6,"adjMaxPhysicalArmor":6,"adjMinMagicArmor":6,"adjMaxMagicArmor":6,"adjHit":5})
    }),
    51016017: _tools.RODict({
        "propID": 51016017,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4664,"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":46,"adjMinMagicAtk":25,"adjMaxMagicAtk":46,"adjMinPhysicalArmor":8,"adjMaxPhysicalArmor":8,"adjMinMagicArmor":8,"adjMaxMagicArmor":8,"adjHit":5})
    }),
    51016018: _tools.RODict({
        "propID": 51016018,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4796,"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":46,"adjMinMagicAtk":25,"adjMaxMagicAtk":46,"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10,"adjHit":6})
    }),
    51016019: _tools.RODict({
        "propID": 51016019,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4983,"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":47,"adjMinMagicAtk":25,"adjMaxMagicAtk":47,"adjMinPhysicalArmor":14,"adjMaxPhysicalArmor":14,"adjMinMagicArmor":14,"adjMaxMagicArmor":14,"adjHit":6})
    }),
    51016020: _tools.RODict({
        "propID": 51016020,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5511,"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":47,"adjMinMagicAtk":25,"adjMaxMagicAtk":47,"adjMinPhysicalArmor":15,"adjMaxPhysicalArmor":15,"adjMinMagicArmor":15,"adjMaxMagicArmor":15,"adjHit":6})
    }),
    51016021: _tools.RODict({
        "propID": 51016021,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5786,"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":60,"adjMinMagicAtk":32,"adjMaxMagicAtk":60,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjHit":6,"adjDebilityAnti":1})
    }),
    51016022: _tools.RODict({
        "propID": 51016022,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5929,"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":60,"adjMinMagicAtk":32,"adjMaxMagicAtk":60,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjHit":10,"adjDebilityAnti":1})
    }),
    51016023: _tools.RODict({
        "propID": 51016023,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":6424,"adjMinPhysicalAtk":35,"adjMaxPhysicalAtk":61,"adjMinMagicAtk":35,"adjMaxMagicAtk":61,"adjMinPhysicalArmor":17,"adjMaxPhysicalArmor":17,"adjMinMagicArmor":17,"adjMaxMagicArmor":17,"adjHit":10,"adjDebilityAnti":1})
    }),
    51016024: _tools.RODict({
        "propID": 51016024,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":6864,"adjMinPhysicalAtk":35,"adjMaxPhysicalAtk":61,"adjMinMagicAtk":35,"adjMaxMagicAtk":61,"adjMinPhysicalArmor":18,"adjMaxPhysicalArmor":18,"adjMinMagicArmor":18,"adjMaxMagicArmor":18,"adjHit":10,"adjDebilityAnti":1})
    }),
    51016025: _tools.RODict({
        "propID": 51016025,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":8140,"adjMinPhysicalAtk":38,"adjMaxPhysicalAtk":71,"adjMinMagicAtk":38,"adjMaxMagicAtk":71,"adjMinPhysicalArmor":20,"adjMaxPhysicalArmor":20,"adjMinMagicArmor":20,"adjMaxMagicArmor":20,"adjHit":10,"adjDebilityAnti":2})
    }),
    51016026: _tools.RODict({
        "propID": 51016026,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":8316,"adjMinPhysicalAtk":38,"adjMaxPhysicalAtk":71,"adjMinMagicAtk":38,"adjMaxMagicAtk":71,"adjMinPhysicalArmor":21,"adjMaxPhysicalArmor":21,"adjMinMagicArmor":21,"adjMaxMagicArmor":21,"adjHit":12,"adjDebilityAnti":2})
    }),
    51016027: _tools.RODict({
        "propID": 51016027,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":8580,"adjMinPhysicalAtk":40,"adjMaxPhysicalAtk":72,"adjMinMagicAtk":40,"adjMaxMagicAtk":72,"adjMinPhysicalArmor":21,"adjMaxPhysicalArmor":21,"adjMinMagicArmor":21,"adjMaxMagicArmor":21,"adjHit":12,"adjDebilityAnti":2})
    }),
    51016028: _tools.RODict({
        "propID": 51016028,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":9086,"adjMinPhysicalAtk":40,"adjMaxPhysicalAtk":72,"adjMinMagicAtk":40,"adjMaxMagicAtk":72,"adjMinPhysicalArmor":22,"adjMaxPhysicalArmor":22,"adjMinMagicArmor":22,"adjMaxMagicArmor":22,"adjHit":12,"adjDebilityAnti":2})
    }),
    51016029: _tools.RODict({
        "propID": 51016029,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":10406,"adjMinPhysicalAtk":43,"adjMaxPhysicalAtk":78,"adjMinMagicAtk":43,"adjMaxMagicAtk":78,"adjMinPhysicalArmor":23,"adjMaxPhysicalArmor":23,"adjMinMagicArmor":23,"adjMaxMagicArmor":23,"adjHit":12,"adjDebilityAnti":3})
    }),
    51016030: _tools.RODict({
        "propID": 51016030,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":45221,"adjMinPhysicalAtk":445,"adjMaxPhysicalAtk":445,"adjMinMagicAtk":445,"adjMaxMagicAtk":445,"adjMinPhysicalArmor":62,"adjMaxPhysicalArmor":62,"adjMinMagicArmor":62,"adjMaxMagicArmor":62,"adjHit":14,"adjDodge":14,"adjDebilityAnti":3})
    }),
    51016031: _tools.RODict({
        "propID": 51016031,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":46343,"adjMinPhysicalAtk":449,"adjMaxPhysicalAtk":449,"adjMinMagicAtk":449,"adjMaxMagicAtk":449,"adjMinPhysicalArmor":62,"adjMaxPhysicalArmor":62,"adjMinMagicArmor":62,"adjMaxMagicArmor":62,"adjHit":14,"adjDodge":14,"adjRealDmg":1,"adjDebilityAnti":3})
    }),
    51016032: _tools.RODict({
        "propID": 51016032,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":47487,"adjMinPhysicalAtk":452,"adjMaxPhysicalAtk":452,"adjMinMagicAtk":452,"adjMaxMagicAtk":452,"adjMinPhysicalArmor":62,"adjMaxPhysicalArmor":62,"adjMinMagicArmor":62,"adjMaxMagicArmor":62,"adjHit":14,"adjDodge":14,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":3})
    }),
    51016033: _tools.RODict({
        "propID": 51016033,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":48631,"adjMinPhysicalAtk":456,"adjMaxPhysicalAtk":456,"adjMinMagicAtk":456,"adjMaxMagicAtk":456,"adjMinPhysicalArmor":62,"adjMaxPhysicalArmor":62,"adjMinMagicArmor":62,"adjMaxMagicArmor":62,"adjHit":14,"adjDodge":14,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":4})
    }),
    51016034: _tools.RODict({
        "propID": 51016034,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":49786,"adjMinPhysicalAtk":457,"adjMaxPhysicalAtk":457,"adjMinMagicAtk":457,"adjMaxMagicAtk":457,"adjMinPhysicalArmor":63,"adjMaxPhysicalArmor":63,"adjMinMagicArmor":63,"adjMaxMagicArmor":63,"adjHit":14,"adjDodge":14,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":4})
    }),
    51016035: _tools.RODict({
        "propID": 51016035,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":50952,"adjMinPhysicalAtk":463,"adjMaxPhysicalAtk":463,"adjMinMagicAtk":463,"adjMaxMagicAtk":463,"adjMinPhysicalArmor":63,"adjMaxPhysicalArmor":63,"adjMinMagicArmor":63,"adjMaxMagicArmor":63,"adjHit":14,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":1,"adjDebilityAnti":4})
    }),
    51016036: _tools.RODict({
        "propID": 51016036,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":52118,"adjMinPhysicalAtk":467,"adjMaxPhysicalAtk":467,"adjMinMagicAtk":467,"adjMaxMagicAtk":467,"adjMinPhysicalArmor":63,"adjMaxPhysicalArmor":63,"adjMinMagicArmor":63,"adjMaxMagicArmor":63,"adjHit":14,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":2,"adjDebilityAnti":4})
    }),
    51016037: _tools.RODict({
        "propID": 51016037,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":53306,"adjMinPhysicalAtk":470,"adjMaxPhysicalAtk":470,"adjMinMagicAtk":470,"adjMaxMagicAtk":470,"adjMinPhysicalArmor":64,"adjMaxPhysicalArmor":64,"adjMinMagicArmor":64,"adjMaxMagicArmor":64,"adjHit":14,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":2,"adjDebilityAnti":4})
    }),
    51016038: _tools.RODict({
        "propID": 51016038,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":54494,"adjMinPhysicalAtk":474,"adjMaxPhysicalAtk":474,"adjMinMagicAtk":474,"adjMaxMagicAtk":474,"adjMinPhysicalArmor":64,"adjMaxPhysicalArmor":64,"adjMinMagicArmor":64,"adjMaxMagicArmor":64,"adjHit":14,"adjDodge":14,"adjRealDmg":3,"adjRealDmgDef":2,"adjDebilityAnti":5})
    }),
    51016039: _tools.RODict({
        "propID": 51016039,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":55693,"adjMinPhysicalAtk":478,"adjMaxPhysicalAtk":478,"adjMinMagicAtk":478,"adjMaxMagicAtk":478,"adjMinPhysicalArmor":64,"adjMaxPhysicalArmor":64,"adjMinMagicArmor":64,"adjMaxMagicArmor":64,"adjHit":14,"adjDodge":14,"adjRealDmg":3,"adjRealDmgDef":3,"adjDebilityEnh":5,"adjDebilityAnti":5})
    }),
    51016040: _tools.RODict({
        "propID": 51016040,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":56903,"adjMinPhysicalAtk":481,"adjMaxPhysicalAtk":481,"adjMinMagicAtk":481,"adjMaxMagicAtk":481,"adjMinPhysicalArmor":65,"adjMaxPhysicalArmor":65,"adjMinMagicArmor":65,"adjMaxMagicArmor":65,"adjHit":14,"adjDodge":14,"adjRealDmg":3,"adjRealDmgDef":3,"adjDebilityEnh":5,"adjDebilityAnti":5})
    }),
    51016041: _tools.RODict({
        "propID": 51016041,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":23287,"adjMinPhysicalAtk":68,"adjMaxPhysicalAtk":125,"adjMinMagicAtk":68,"adjMaxMagicAtk":125,"adjMinPhysicalArmor":38,"adjMaxPhysicalArmor":38,"adjMinMagicArmor":38,"adjMaxMagicArmor":38,"adjHit":23,"adjRealDmg":3,"adjRealDmgDef":3,"adjDebilityEnh":5,"adjDebilityAnti":5})
    }),
    51016042: _tools.RODict({
        "propID": 51016042,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":23661,"adjMinPhysicalAtk":72,"adjMaxPhysicalAtk":130,"adjMinMagicAtk":72,"adjMaxMagicAtk":130,"adjMinPhysicalArmor":38,"adjMaxPhysicalArmor":38,"adjMinMagicArmor":38,"adjMaxMagicArmor":38,"adjHit":23,"adjRealDmg":4,"adjRealDmgDef":3,"adjDebilityEnh":5,"adjDebilityAnti":5})
    }),
    51016043: _tools.RODict({
        "propID": 51016043,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":24145,"adjMinPhysicalAtk":76,"adjMaxPhysicalAtk":137,"adjMinMagicAtk":76,"adjMaxMagicAtk":137,"adjMinPhysicalArmor":38,"adjMaxPhysicalArmor":38,"adjMinMagicArmor":38,"adjMaxMagicArmor":38,"adjHit":25,"adjRealDmg":4,"adjRealDmgDef":4,"adjDebilityEnh":5,"adjDebilityAnti":6})
    }),
    51016044: _tools.RODict({
        "propID": 51016044,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":24959,"adjMinPhysicalAtk":78,"adjMaxPhysicalAtk":140,"adjMinMagicAtk":78,"adjMaxMagicAtk":140,"adjMinPhysicalArmor":39,"adjMaxPhysicalArmor":39,"adjMinMagicArmor":39,"adjMaxMagicArmor":39,"adjHit":26,"adjRealDmg":4,"adjRealDmgDef":4,"adjDebilityEnh":6,"adjDebilityAnti":6})
    }),
    51016045: _tools.RODict({
        "propID": 51016045,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":25883,"adjMinPhysicalAtk":82,"adjMaxPhysicalAtk":146,"adjMinMagicAtk":82,"adjMaxMagicAtk":146,"adjMinPhysicalArmor":39,"adjMaxPhysicalArmor":39,"adjMinMagicArmor":39,"adjMaxMagicArmor":39,"adjHit":26,"adjRealDmg":4,"adjRealDmgDef":4,"adjDebilityEnh":6,"adjDebilityAnti":6})
    }),
    51016046: _tools.RODict({
        "propID": 51016046,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":28809,"adjMinPhysicalAtk":82,"adjMaxPhysicalAtk":146,"adjMinMagicAtk":82,"adjMaxMagicAtk":146,"adjMinPhysicalArmor":42,"adjMaxPhysicalArmor":42,"adjMinMagicArmor":42,"adjMaxMagicArmor":42,"adjHit":26,"adjRealDmg":4,"adjRealDmgDef":4,"adjDebilityEnh":6,"adjDebilityAnti":6})
    }),
    51016047: _tools.RODict({
        "propID": 51016047,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":29348,"adjMinPhysicalAtk":86,"adjMaxPhysicalAtk":157,"adjMinMagicAtk":86,"adjMaxMagicAtk":157,"adjMinPhysicalArmor":42,"adjMaxPhysicalArmor":42,"adjMinMagicArmor":42,"adjMaxMagicArmor":42,"adjHit":26,"adjRealDmg":5,"adjRealDmgDef":4,"adjDebilityEnh":6,"adjDebilityAnti":6})
    }),
    51016048: _tools.RODict({
        "propID": 51016048,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":29788,"adjMinPhysicalAtk":86,"adjMaxPhysicalAtk":158,"adjMinMagicAtk":86,"adjMaxMagicAtk":158,"adjMinPhysicalArmor":43,"adjMaxPhysicalArmor":43,"adjMinMagicArmor":43,"adjMaxMagicArmor":43,"adjHit":30,"adjRealDmg":5,"adjRealDmgDef":5,"adjDebilityEnh":6,"adjDebilityAnti":7})
    }),
    51016049: _tools.RODict({
        "propID": 51016049,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":31834,"adjMinPhysicalAtk":90,"adjMaxPhysicalAtk":164,"adjMinMagicAtk":90,"adjMaxMagicAtk":164,"adjMinPhysicalArmor":44,"adjMaxPhysicalArmor":44,"adjMinMagicArmor":44,"adjMaxMagicArmor":44,"adjHit":30,"adjRealDmg":5,"adjRealDmgDef":5,"adjDebilityEnh":7,"adjDebilityAnti":7})
    }),
    51016050: _tools.RODict({
        "propID": 51016050,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":33110,"adjMinPhysicalAtk":96,"adjMaxPhysicalAtk":173,"adjMinMagicAtk":96,"adjMaxMagicAtk":173,"adjMinPhysicalArmor":45,"adjMaxPhysicalArmor":45,"adjMinMagicArmor":45,"adjMaxMagicArmor":45,"adjHit":32,"adjRealDmg":5,"adjRealDmgDef":5,"adjDebilityEnh":7,"adjDebilityAnti":7})
    }),
    51016051: _tools.RODict({
        "propID": 51016051,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":36058,"adjMinPhysicalAtk":96,"adjMaxPhysicalAtk":175,"adjMinMagicAtk":96,"adjMaxMagicAtk":175,"adjMinPhysicalArmor":49,"adjMaxPhysicalArmor":49,"adjMinMagicArmor":49,"adjMaxMagicArmor":49,"adjHit":32,"adjRealDmg":5,"adjRealDmgDef":5,"adjDebilityEnh":7,"adjDebilityAnti":7})
    }),
    51016052: _tools.RODict({
        "propID": 51016052,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":37521,"adjMinPhysicalAtk":100,"adjMaxPhysicalAtk":180,"adjMinMagicAtk":100,"adjMaxMagicAtk":180,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":50,"adjMaxMagicArmor":50,"adjHit":32,"adjRealDmg":6,"adjRealDmgDef":5,"adjDebilityEnh":7,"adjDebilityAnti":7})
    }),
    51016053: _tools.RODict({
        "propID": 51016053,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":38159,"adjMinPhysicalAtk":103,"adjMaxPhysicalAtk":186,"adjMinMagicAtk":103,"adjMaxMagicAtk":186,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":50,"adjMaxMagicArmor":50,"adjHit":34,"adjRealDmg":6,"adjRealDmgDef":6,"adjDebilityEnh":7,"adjDebilityAnti":8})
    }),
    51016054: _tools.RODict({
        "propID": 51016054,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":39292,"adjMinPhysicalAtk":107,"adjMaxPhysicalAtk":194,"adjMinMagicAtk":107,"adjMaxMagicAtk":194,"adjMinPhysicalArmor":51,"adjMaxPhysicalArmor":51,"adjMinMagicArmor":51,"adjMaxMagicArmor":51,"adjHit":34,"adjRealDmg":6,"adjRealDmgDef":6,"adjDebilityEnh":8,"adjDebilityAnti":8})
    }),
    51016055: _tools.RODict({
        "propID": 51016055,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":40579,"adjMinPhysicalAtk":112,"adjMaxPhysicalAtk":202,"adjMinMagicAtk":112,"adjMaxMagicAtk":202,"adjMinPhysicalArmor":52,"adjMaxPhysicalArmor":52,"adjMinMagicArmor":52,"adjMaxMagicArmor":52,"adjHit":37,"adjRealDmg":6,"adjRealDmgDef":6,"adjDebilityEnh":8,"adjDebilityAnti":8})
    }),
    51016056: _tools.RODict({
        "propID": 51016056,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":44143,"adjMinPhysicalAtk":112,"adjMaxPhysicalAtk":202,"adjMinMagicAtk":112,"adjMaxMagicAtk":202,"adjMinPhysicalArmor":56,"adjMaxPhysicalArmor":56,"adjMinMagicArmor":56,"adjMaxMagicArmor":56,"adjHit":37,"adjRealDmg":6,"adjRealDmgDef":6,"adjDebilityEnh":8,"adjDebilityAnti":8})
    }),
    51016057: _tools.RODict({
        "propID": 51016057,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":46002,"adjMinPhysicalAtk":115,"adjMaxPhysicalAtk":209,"adjMinMagicAtk":115,"adjMaxMagicAtk":209,"adjMinPhysicalArmor":57,"adjMaxPhysicalArmor":57,"adjMinMagicArmor":57,"adjMaxMagicArmor":57,"adjHit":37,"adjRealDmg":7,"adjRealDmgDef":6,"adjDebilityEnh":8,"adjDebilityAnti":8})
    }),
    51016058: _tools.RODict({
        "propID": 51016058,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":46596,"adjMinPhysicalAtk":118,"adjMaxPhysicalAtk":212,"adjMinMagicAtk":118,"adjMaxMagicAtk":212,"adjMinPhysicalArmor":57,"adjMaxPhysicalArmor":57,"adjMinMagicArmor":57,"adjMaxMagicArmor":57,"adjHit":39,"adjRealDmg":7,"adjRealDmgDef":7,"adjDebilityEnh":8,"adjDebilityAnti":9})
    }),
    51016059: _tools.RODict({
        "propID": 51016059,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":48642,"adjMinPhysicalAtk":125,"adjMaxPhysicalAtk":227,"adjMinMagicAtk":125,"adjMaxMagicAtk":227,"adjMinPhysicalArmor":58,"adjMaxPhysicalArmor":58,"adjMinMagicArmor":58,"adjMaxMagicArmor":58,"adjHit":39,"adjRealDmg":7,"adjRealDmgDef":7,"adjDebilityEnh":9,"adjDebilityAnti":9})
    }),
    51016060: _tools.RODict({
        "propID": 51016060,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":50578,"adjMinPhysicalAtk":128,"adjMaxPhysicalAtk":233,"adjMinMagicAtk":128,"adjMaxMagicAtk":233,"adjMinPhysicalArmor":59,"adjMaxPhysicalArmor":59,"adjMinMagicArmor":59,"adjMaxMagicArmor":59,"adjHit":42,"adjRealDmg":7,"adjRealDmgDef":7,"adjDebilityEnh":9,"adjDebilityAnti":9})
    }),
    51016061: _tools.RODict({
        "propID": 51016061,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":56991,"adjMinPhysicalAtk":130,"adjMaxPhysicalAtk":234,"adjMinMagicAtk":130,"adjMaxMagicAtk":234,"adjMinPhysicalArmor":66,"adjMaxPhysicalArmor":66,"adjMinMagicArmor":66,"adjMaxMagicArmor":66,"adjHit":42,"adjRealDmg":7,"adjRealDmgDef":7,"adjDebilityEnh":9,"adjDebilityAnti":9})
    }),
    51016062: _tools.RODict({
        "propID": 51016062,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":59059,"adjMinPhysicalAtk":137,"adjMaxPhysicalAtk":251,"adjMinMagicAtk":137,"adjMaxMagicAtk":251,"adjMinPhysicalArmor":68,"adjMaxPhysicalArmor":68,"adjMinMagicArmor":68,"adjMaxMagicArmor":68,"adjHit":42,"adjRealDmg":9,"adjRealDmgDef":7,"adjDebilityEnh":9,"adjDebilityAnti":9})
    }),
    51016063: _tools.RODict({
        "propID": 51016063,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":59917,"adjMinPhysicalAtk":143,"adjMaxPhysicalAtk":259,"adjMinMagicAtk":143,"adjMaxMagicAtk":259,"adjMinPhysicalArmor":68,"adjMaxPhysicalArmor":68,"adjMinMagicArmor":68,"adjMaxMagicArmor":68,"adjHit":48,"adjRealDmg":9,"adjRealDmgDef":9,"adjDebilityEnh":9,"adjDebilityAnti":11})
    }),
    51016064: _tools.RODict({
        "propID": 51016064,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":63008,"adjMinPhysicalAtk":150,"adjMaxPhysicalAtk":272,"adjMinMagicAtk":150,"adjMaxMagicAtk":272,"adjMinPhysicalArmor":69,"adjMaxPhysicalArmor":69,"adjMinMagicArmor":69,"adjMaxMagicArmor":69,"adjHit":48,"adjRealDmg":9,"adjRealDmgDef":9,"adjDebilityEnh":11,"adjDebilityAnti":11})
    }),
    51016065: _tools.RODict({
        "propID": 51016065,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":66297,"adjMinPhysicalAtk":154,"adjMaxPhysicalAtk":280,"adjMinMagicAtk":154,"adjMaxMagicAtk":280,"adjMinPhysicalArmor":70,"adjMaxPhysicalArmor":70,"adjMinMagicArmor":70,"adjMaxMagicArmor":70,"adjHit":52,"adjRealDmg":9,"adjRealDmgDef":9,"adjDebilityEnh":11,"adjDebilityAnti":11})
    }),
    51016066: _tools.RODict({
        "propID": 51016066,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":71929,"adjMinPhysicalAtk":154,"adjMaxPhysicalAtk":280,"adjMinMagicAtk":154,"adjMaxMagicAtk":280,"adjMinPhysicalArmor":76,"adjMaxPhysicalArmor":76,"adjMinMagicArmor":76,"adjMaxMagicArmor":76,"adjHit":52,"adjRealDmg":9,"adjRealDmgDef":9,"adjDebilityEnh":11,"adjDebilityAnti":11})
    }),
    51016067: _tools.RODict({
        "propID": 51016067,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":74492,"adjMinPhysicalAtk":162,"adjMaxPhysicalAtk":294,"adjMinMagicAtk":162,"adjMaxMagicAtk":294,"adjMinPhysicalArmor":78,"adjMaxPhysicalArmor":78,"adjMinMagicArmor":78,"adjMaxMagicArmor":78,"adjHit":52,"adjRealDmg":11,"adjRealDmgDef":9,"adjDebilityEnh":11,"adjDebilityAnti":11})
    }),
    51016068: _tools.RODict({
        "propID": 51016068,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":75350,"adjMinPhysicalAtk":164,"adjMaxPhysicalAtk":299,"adjMinMagicAtk":164,"adjMaxMagicAtk":299,"adjMinPhysicalArmor":79,"adjMaxPhysicalArmor":79,"adjMinMagicArmor":79,"adjMaxMagicArmor":79,"adjHit":54,"adjRealDmg":11,"adjRealDmgDef":11,"adjDebilityEnh":11,"adjDebilityAnti":12})
    }),
    51016069: _tools.RODict({
        "propID": 51016069,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":78133,"adjMinPhysicalAtk":175,"adjMaxPhysicalAtk":317,"adjMinMagicAtk":175,"adjMaxMagicAtk":317,"adjMinPhysicalArmor":79,"adjMaxPhysicalArmor":79,"adjMinMagicArmor":79,"adjMaxMagicArmor":79,"adjHit":54,"adjRealDmg":11,"adjRealDmgDef":11,"adjDebilityEnh":12,"adjDebilityAnti":12})
    }),
    51016070: _tools.RODict({
        "propID": 51016070,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":80795,"adjMinPhysicalAtk":179,"adjMaxPhysicalAtk":324,"adjMinMagicAtk":179,"adjMaxMagicAtk":324,"adjMinPhysicalArmor":80,"adjMaxPhysicalArmor":80,"adjMinMagicArmor":80,"adjMaxMagicArmor":80,"adjHit":58,"adjRealDmg":11,"adjRealDmgDef":11,"adjDebilityEnh":12,"adjDebilityAnti":12})
    }),
    51017001: _tools.RODict({
        "propID": 51017001,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4488,"adjMinPhysicalAtk":75,"adjMaxPhysicalAtk":140,"adjMinMagicAtk":75,"adjMaxMagicAtk":140,"adjHit":1,"adjDodge":1})
    }),
    51017002: _tools.RODict({
        "propID": 51017002,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4703,"adjMinPhysicalAtk":80,"adjMaxPhysicalAtk":143,"adjMinMagicAtk":80,"adjMaxMagicAtk":143,"adjHit":2,"adjDodge":2})
    }),
    51017003: _tools.RODict({
        "propID": 51017003,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4934,"adjMinPhysicalAtk":80,"adjMaxPhysicalAtk":148,"adjMinMagicAtk":80,"adjMaxMagicAtk":148,"adjHit":3,"adjDodge":3})
    }),
    51017004: _tools.RODict({
        "propID": 51017004,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5148,"adjMinPhysicalAtk":83,"adjMaxPhysicalAtk":150,"adjMinMagicAtk":83,"adjMaxMagicAtk":150,"adjHit":4,"adjDodge":4})
    }),
    51017005: _tools.RODict({
        "propID": 51017005,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5379,"adjMinPhysicalAtk":88,"adjMaxPhysicalAtk":155,"adjMinMagicAtk":88,"adjMaxMagicAtk":155,"adjHit":5,"adjDodge":5})
    }),
    51017006: _tools.RODict({
        "propID": 51017006,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5594,"adjMinPhysicalAtk":90,"adjMaxPhysicalAtk":163,"adjMinMagicAtk":90,"adjMaxMagicAtk":163,"adjHit":6,"adjDodge":6})
    }),
    51017007: _tools.RODict({
        "propID": 51017007,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5825,"adjMinPhysicalAtk":90,"adjMaxPhysicalAtk":165,"adjMinMagicAtk":90,"adjMaxMagicAtk":165,"adjHit":7,"adjDodge":7})
    }),
    51017008: _tools.RODict({
        "propID": 51017008,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":6056,"adjMinPhysicalAtk":95,"adjMaxPhysicalAtk":170,"adjMinMagicAtk":95,"adjMaxMagicAtk":170,"adjHit":8,"adjDodge":8})
    }),
    51017009: _tools.RODict({
        "propID": 51017009,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":6270,"adjMinPhysicalAtk":95,"adjMaxPhysicalAtk":173,"adjMinMagicAtk":95,"adjMaxMagicAtk":173,"adjHit":9,"adjDodge":9})
    }),
    51017010: _tools.RODict({
        "propID": 51017010,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":6501,"adjMinPhysicalAtk":98,"adjMaxPhysicalAtk":178,"adjMinMagicAtk":98,"adjMaxMagicAtk":178,"adjHit":10,"adjDodge":10})
    }),
    51017011: _tools.RODict({
        "propID": 51017011,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":4868,"adjMinPhysicalAtk":38,"adjMaxPhysicalAtk":68,"adjMinMagicAtk":38,"adjMaxMagicAtk":68,"adjMinPhysicalArmor":1,"adjMaxPhysicalArmor":1,"adjMinMagicArmor":1,"adjMaxMagicArmor":1,"adjHit":4})
    }),
    51017012: _tools.RODict({
        "propID": 51017012,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5016,"adjMinPhysicalAtk":38,"adjMaxPhysicalAtk":73,"adjMinMagicAtk":38,"adjMaxMagicAtk":73,"adjMinPhysicalArmor":2,"adjMaxPhysicalArmor":2,"adjMinMagicArmor":2,"adjMaxMagicArmor":2,"adjHit":4})
    }),
    51017013: _tools.RODict({
        "propID": 51017013,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5264,"adjMinPhysicalAtk":43,"adjMaxPhysicalAtk":75,"adjMinMagicAtk":43,"adjMaxMagicAtk":75,"adjMinPhysicalArmor":3,"adjMaxPhysicalArmor":3,"adjMinMagicArmor":3,"adjMaxMagicArmor":3,"adjHit":5})
    }),
    51017014: _tools.RODict({
        "propID": 51017014,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":5412,"adjMinPhysicalAtk":43,"adjMaxPhysicalAtk":75,"adjMinMagicAtk":43,"adjMaxMagicAtk":75,"adjMinPhysicalArmor":4,"adjMaxPhysicalArmor":4,"adjMinMagicArmor":4,"adjMaxMagicArmor":4,"adjHit":5})
    }),
    51017015: _tools.RODict({
        "propID": 51017015,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":6534,"adjMinPhysicalAtk":45,"adjMaxPhysicalAtk":80,"adjMinMagicAtk":45,"adjMaxMagicAtk":80,"adjMinPhysicalArmor":5,"adjMaxPhysicalArmor":5,"adjMinMagicArmor":5,"adjMaxMagicArmor":5,"adjHit":5})
    }),
    51017016: _tools.RODict({
        "propID": 51017016,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":6716,"adjMinPhysicalAtk":50,"adjMaxPhysicalAtk":88,"adjMinMagicAtk":50,"adjMaxMagicAtk":88,"adjMinPhysicalArmor":6,"adjMaxPhysicalArmor":6,"adjMinMagicArmor":6,"adjMaxMagicArmor":6,"adjHit":5})
    }),
    51017017: _tools.RODict({
        "propID": 51017017,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":6996,"adjMinPhysicalAtk":53,"adjMaxPhysicalAtk":95,"adjMinMagicAtk":53,"adjMaxMagicAtk":95,"adjMinPhysicalArmor":8,"adjMaxPhysicalArmor":8,"adjMinMagicArmor":8,"adjMaxMagicArmor":8,"adjHit":5})
    }),
    51017018: _tools.RODict({
        "propID": 51017018,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":7194,"adjMinPhysicalAtk":53,"adjMaxPhysicalAtk":95,"adjMinMagicAtk":53,"adjMaxMagicAtk":95,"adjMinPhysicalArmor":10,"adjMaxPhysicalArmor":10,"adjMinMagicArmor":10,"adjMaxMagicArmor":10,"adjHit":6})
    }),
    51017019: _tools.RODict({
        "propID": 51017019,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":7475,"adjMinPhysicalAtk":53,"adjMaxPhysicalAtk":98,"adjMinMagicAtk":53,"adjMaxMagicAtk":98,"adjMinPhysicalArmor":14,"adjMaxPhysicalArmor":14,"adjMinMagicArmor":14,"adjMaxMagicArmor":14,"adjHit":6})
    }),
    51017020: _tools.RODict({
        "propID": 51017020,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":8267,"adjMinPhysicalAtk":53,"adjMaxPhysicalAtk":98,"adjMinMagicAtk":53,"adjMaxMagicAtk":98,"adjMinPhysicalArmor":15,"adjMaxPhysicalArmor":15,"adjMinMagicArmor":15,"adjMaxMagicArmor":15,"adjHit":6})
    }),
    51017021: _tools.RODict({
        "propID": 51017021,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":8679,"adjMinPhysicalAtk":68,"adjMaxPhysicalAtk":125,"adjMinMagicAtk":68,"adjMaxMagicAtk":125,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjHit":6,"adjDebilityAnti":1})
    }),
    51017022: _tools.RODict({
        "propID": 51017022,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":8894,"adjMinPhysicalAtk":68,"adjMaxPhysicalAtk":125,"adjMinMagicAtk":68,"adjMaxMagicAtk":125,"adjMinPhysicalArmor":16,"adjMaxPhysicalArmor":16,"adjMinMagicArmor":16,"adjMaxMagicArmor":16,"adjHit":10,"adjDebilityAnti":1})
    }),
    51017023: _tools.RODict({
        "propID": 51017023,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":9636,"adjMinPhysicalAtk":73,"adjMaxPhysicalAtk":128,"adjMinMagicAtk":73,"adjMaxMagicAtk":128,"adjMinPhysicalArmor":17,"adjMaxPhysicalArmor":17,"adjMinMagicArmor":17,"adjMaxMagicArmor":17,"adjHit":10,"adjDebilityAnti":1})
    }),
    51017024: _tools.RODict({
        "propID": 51017024,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":10296,"adjMinPhysicalAtk":73,"adjMaxPhysicalAtk":128,"adjMinMagicAtk":73,"adjMaxMagicAtk":128,"adjMinPhysicalArmor":18,"adjMaxPhysicalArmor":18,"adjMinMagicArmor":18,"adjMaxMagicArmor":18,"adjHit":10,"adjDebilityAnti":1})
    }),
    51017025: _tools.RODict({
        "propID": 51017025,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":12210,"adjMinPhysicalAtk":80,"adjMaxPhysicalAtk":148,"adjMinMagicAtk":80,"adjMaxMagicAtk":148,"adjMinPhysicalArmor":20,"adjMaxPhysicalArmor":20,"adjMinMagicArmor":20,"adjMaxMagicArmor":20,"adjHit":10,"adjDebilityAnti":2})
    }),
    51017026: _tools.RODict({
        "propID": 51017026,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":12474,"adjMinPhysicalAtk":80,"adjMaxPhysicalAtk":148,"adjMinMagicAtk":80,"adjMaxMagicAtk":148,"adjMinPhysicalArmor":21,"adjMaxPhysicalArmor":21,"adjMinMagicArmor":21,"adjMaxMagicArmor":21,"adjHit":12,"adjDebilityAnti":2})
    }),
    51017027: _tools.RODict({
        "propID": 51017027,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":12870,"adjMinPhysicalAtk":83,"adjMaxPhysicalAtk":150,"adjMinMagicAtk":83,"adjMaxMagicAtk":150,"adjMinPhysicalArmor":21,"adjMaxPhysicalArmor":21,"adjMinMagicArmor":21,"adjMaxMagicArmor":21,"adjHit":12,"adjDebilityAnti":2})
    }),
    51017028: _tools.RODict({
        "propID": 51017028,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":13629,"adjMinPhysicalAtk":83,"adjMaxPhysicalAtk":150,"adjMinMagicAtk":83,"adjMaxMagicAtk":150,"adjMinPhysicalArmor":22,"adjMaxPhysicalArmor":22,"adjMinMagicArmor":22,"adjMaxMagicArmor":22,"adjHit":12,"adjDebilityAnti":2})
    }),
    51017029: _tools.RODict({
        "propID": 51017029,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":15609,"adjMinPhysicalAtk":90,"adjMaxPhysicalAtk":163,"adjMinMagicAtk":90,"adjMaxMagicAtk":163,"adjMinPhysicalArmor":23,"adjMaxPhysicalArmor":23,"adjMinMagicArmor":23,"adjMaxMagicArmor":23,"adjHit":12,"adjDebilityAnti":3})
    }),
    51017030: _tools.RODict({
        "propID": 51017030,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":67832,"adjMinPhysicalAtk":928,"adjMaxPhysicalAtk":928,"adjMinMagicAtk":928,"adjMaxMagicAtk":928,"adjMinPhysicalArmor":62,"adjMaxPhysicalArmor":62,"adjMinMagicArmor":62,"adjMaxMagicArmor":62,"adjHit":14,"adjDodge":14,"adjDebilityAnti":3})
    }),
    51017031: _tools.RODict({
        "propID": 51017031,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":69515,"adjMinPhysicalAtk":935,"adjMaxPhysicalAtk":935,"adjMinMagicAtk":935,"adjMaxMagicAtk":935,"adjMinPhysicalArmor":62,"adjMaxPhysicalArmor":62,"adjMinMagicArmor":62,"adjMaxMagicArmor":62,"adjHit":14,"adjDodge":14,"adjRealDmg":1,"adjDebilityAnti":3})
    }),
    51017032: _tools.RODict({
        "propID": 51017032,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":71231,"adjMinPhysicalAtk":943,"adjMaxPhysicalAtk":943,"adjMinMagicAtk":943,"adjMaxMagicAtk":943,"adjMinPhysicalArmor":62,"adjMaxPhysicalArmor":62,"adjMinMagicArmor":62,"adjMaxMagicArmor":62,"adjHit":14,"adjDodge":14,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":3})
    }),
    51017033: _tools.RODict({
        "propID": 51017033,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":72947,"adjMinPhysicalAtk":950,"adjMaxPhysicalAtk":950,"adjMinMagicAtk":950,"adjMaxMagicAtk":950,"adjMinPhysicalArmor":62,"adjMaxPhysicalArmor":62,"adjMinMagicArmor":62,"adjMaxMagicArmor":62,"adjHit":14,"adjDodge":14,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":4})
    }),
    51017034: _tools.RODict({
        "propID": 51017034,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":74679,"adjMinPhysicalAtk":953,"adjMaxPhysicalAtk":953,"adjMinMagicAtk":953,"adjMaxMagicAtk":953,"adjMinPhysicalArmor":63,"adjMaxPhysicalArmor":63,"adjMinMagicArmor":63,"adjMaxMagicArmor":63,"adjHit":14,"adjDodge":14,"adjRealDmg":1,"adjRealDmgDef":1,"adjDebilityAnti":4})
    }),
    51017035: _tools.RODict({
        "propID": 51017035,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":76428,"adjMinPhysicalAtk":965,"adjMaxPhysicalAtk":965,"adjMinMagicAtk":965,"adjMaxMagicAtk":965,"adjMinPhysicalArmor":63,"adjMaxPhysicalArmor":63,"adjMinMagicArmor":63,"adjMaxMagicArmor":63,"adjHit":14,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":1,"adjDebilityAnti":4})
    }),
    51017036: _tools.RODict({
        "propID": 51017036,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":78177,"adjMinPhysicalAtk":973,"adjMaxPhysicalAtk":973,"adjMinMagicAtk":973,"adjMaxMagicAtk":973,"adjMinPhysicalArmor":63,"adjMaxPhysicalArmor":63,"adjMinMagicArmor":63,"adjMaxMagicArmor":63,"adjHit":14,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":2,"adjDebilityAnti":4})
    }),
    51017037: _tools.RODict({
        "propID": 51017037,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":79959,"adjMinPhysicalAtk":980,"adjMaxPhysicalAtk":980,"adjMinMagicAtk":980,"adjMaxMagicAtk":980,"adjMinPhysicalArmor":64,"adjMaxPhysicalArmor":64,"adjMinMagicArmor":64,"adjMaxMagicArmor":64,"adjHit":14,"adjDodge":14,"adjRealDmg":2,"adjRealDmgDef":2,"adjDebilityAnti":4})
    }),
    51017038: _tools.RODict({
        "propID": 51017038,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":81741,"adjMinPhysicalAtk":988,"adjMaxPhysicalAtk":988,"adjMinMagicAtk":988,"adjMaxMagicAtk":988,"adjMinPhysicalArmor":64,"adjMaxPhysicalArmor":64,"adjMinMagicArmor":64,"adjMaxMagicArmor":64,"adjHit":14,"adjDodge":14,"adjRealDmg":3,"adjRealDmgDef":2,"adjDebilityAnti":5})
    }),
    51017039: _tools.RODict({
        "propID": 51017039,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":83540,"adjMinPhysicalAtk":995,"adjMaxPhysicalAtk":995,"adjMinMagicAtk":995,"adjMaxMagicAtk":995,"adjMinPhysicalArmor":64,"adjMaxPhysicalArmor":64,"adjMinMagicArmor":64,"adjMaxMagicArmor":64,"adjHit":14,"adjDodge":14,"adjRealDmg":3,"adjRealDmgDef":3,"adjDebilityEnh":5,"adjDebilityAnti":5})
    }),
    51017040: _tools.RODict({
        "propID": 51017040,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":85355,"adjMinPhysicalAtk":1003,"adjMaxPhysicalAtk":1003,"adjMinMagicAtk":1003,"adjMaxMagicAtk":1003,"adjMinPhysicalArmor":65,"adjMaxPhysicalArmor":65,"adjMinMagicArmor":65,"adjMaxMagicArmor":65,"adjHit":14,"adjDodge":14,"adjRealDmg":3,"adjRealDmgDef":3,"adjDebilityEnh":5,"adjDebilityAnti":5})
    }),
    51017041: _tools.RODict({
        "propID": 51017041,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":34931,"adjMinPhysicalAtk":143,"adjMaxPhysicalAtk":260,"adjMinMagicAtk":143,"adjMaxMagicAtk":260,"adjMinPhysicalArmor":38,"adjMaxPhysicalArmor":38,"adjMinMagicArmor":38,"adjMaxMagicArmor":38,"adjHit":23,"adjRealDmg":3,"adjRealDmgDef":3,"adjDebilityEnh":5,"adjDebilityAnti":5})
    }),
    51017042: _tools.RODict({
        "propID": 51017042,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":35492,"adjMinPhysicalAtk":150,"adjMaxPhysicalAtk":270,"adjMinMagicAtk":150,"adjMaxMagicAtk":270,"adjMinPhysicalArmor":38,"adjMaxPhysicalArmor":38,"adjMinMagicArmor":38,"adjMaxMagicArmor":38,"adjHit":23,"adjRealDmg":4,"adjRealDmgDef":3,"adjDebilityEnh":5,"adjDebilityAnti":5})
    }),
    51017043: _tools.RODict({
        "propID": 51017043,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":36218,"adjMinPhysicalAtk":158,"adjMaxPhysicalAtk":285,"adjMinMagicAtk":158,"adjMaxMagicAtk":285,"adjMinPhysicalArmor":38,"adjMaxPhysicalArmor":38,"adjMinMagicArmor":38,"adjMaxMagicArmor":38,"adjHit":25,"adjRealDmg":4,"adjRealDmgDef":4,"adjDebilityEnh":5,"adjDebilityAnti":6})
    }),
    51017044: _tools.RODict({
        "propID": 51017044,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":37439,"adjMinPhysicalAtk":163,"adjMaxPhysicalAtk":293,"adjMinMagicAtk":163,"adjMaxMagicAtk":293,"adjMinPhysicalArmor":39,"adjMaxPhysicalArmor":39,"adjMinMagicArmor":39,"adjMaxMagicArmor":39,"adjHit":26,"adjRealDmg":4,"adjRealDmgDef":4,"adjDebilityEnh":6,"adjDebilityAnti":6})
    }),
    51017045: _tools.RODict({
        "propID": 51017045,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":38825,"adjMinPhysicalAtk":170,"adjMaxPhysicalAtk":305,"adjMinMagicAtk":170,"adjMaxMagicAtk":305,"adjMinPhysicalArmor":39,"adjMaxPhysicalArmor":39,"adjMinMagicArmor":39,"adjMaxMagicArmor":39,"adjHit":26,"adjRealDmg":4,"adjRealDmgDef":4,"adjDebilityEnh":6,"adjDebilityAnti":6})
    }),
    51017046: _tools.RODict({
        "propID": 51017046,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":43214,"adjMinPhysicalAtk":170,"adjMaxPhysicalAtk":305,"adjMinMagicAtk":170,"adjMaxMagicAtk":305,"adjMinPhysicalArmor":42,"adjMaxPhysicalArmor":42,"adjMinMagicArmor":42,"adjMaxMagicArmor":42,"adjHit":26,"adjRealDmg":4,"adjRealDmgDef":4,"adjDebilityEnh":6,"adjDebilityAnti":6})
    }),
    51017047: _tools.RODict({
        "propID": 51017047,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":44022,"adjMinPhysicalAtk":180,"adjMaxPhysicalAtk":328,"adjMinMagicAtk":180,"adjMaxMagicAtk":328,"adjMinPhysicalArmor":42,"adjMaxPhysicalArmor":42,"adjMinMagicArmor":42,"adjMaxMagicArmor":42,"adjHit":26,"adjRealDmg":5,"adjRealDmgDef":4,"adjDebilityEnh":6,"adjDebilityAnti":6})
    }),
    51017048: _tools.RODict({
        "propID": 51017048,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":44682,"adjMinPhysicalAtk":180,"adjMaxPhysicalAtk":330,"adjMinMagicAtk":180,"adjMaxMagicAtk":330,"adjMinPhysicalArmor":43,"adjMaxPhysicalArmor":43,"adjMinMagicArmor":43,"adjMaxMagicArmor":43,"adjHit":30,"adjRealDmg":5,"adjRealDmgDef":5,"adjDebilityEnh":6,"adjDebilityAnti":7})
    }),
    51017049: _tools.RODict({
        "propID": 51017049,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":47751,"adjMinPhysicalAtk":188,"adjMaxPhysicalAtk":343,"adjMinMagicAtk":188,"adjMaxMagicAtk":343,"adjMinPhysicalArmor":44,"adjMaxPhysicalArmor":44,"adjMinMagicArmor":44,"adjMaxMagicArmor":44,"adjHit":30,"adjRealDmg":5,"adjRealDmgDef":5,"adjDebilityEnh":7,"adjDebilityAnti":7})
    }),
    51017050: _tools.RODict({
        "propID": 51017050,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":49665,"adjMinPhysicalAtk":200,"adjMaxPhysicalAtk":360,"adjMinMagicAtk":200,"adjMaxMagicAtk":360,"adjMinPhysicalArmor":45,"adjMaxPhysicalArmor":45,"adjMinMagicArmor":45,"adjMaxMagicArmor":45,"adjHit":32,"adjRealDmg":5,"adjRealDmgDef":5,"adjDebilityEnh":7,"adjDebilityAnti":7})
    }),
    51017051: _tools.RODict({
        "propID": 51017051,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":54087,"adjMinPhysicalAtk":200,"adjMaxPhysicalAtk":365,"adjMinMagicAtk":200,"adjMaxMagicAtk":365,"adjMinPhysicalArmor":49,"adjMaxPhysicalArmor":49,"adjMinMagicArmor":49,"adjMaxMagicArmor":49,"adjHit":32,"adjRealDmg":5,"adjRealDmgDef":5,"adjDebilityEnh":7,"adjDebilityAnti":7})
    }),
    51017052: _tools.RODict({
        "propID": 51017052,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":56282,"adjMinPhysicalAtk":208,"adjMaxPhysicalAtk":375,"adjMinMagicAtk":208,"adjMaxMagicAtk":375,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":50,"adjMaxMagicArmor":50,"adjHit":32,"adjRealDmg":6,"adjRealDmgDef":5,"adjDebilityEnh":7,"adjDebilityAnti":7})
    }),
    51017053: _tools.RODict({
        "propID": 51017053,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":57239,"adjMinPhysicalAtk":215,"adjMaxPhysicalAtk":388,"adjMinMagicAtk":215,"adjMaxMagicAtk":388,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":50,"adjMaxMagicArmor":50,"adjHit":34,"adjRealDmg":6,"adjRealDmgDef":6,"adjDebilityEnh":7,"adjDebilityAnti":8})
    }),
    51017054: _tools.RODict({
        "propID": 51017054,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":58938,"adjMinPhysicalAtk":223,"adjMaxPhysicalAtk":405,"adjMinMagicAtk":223,"adjMaxMagicAtk":405,"adjMinPhysicalArmor":51,"adjMaxPhysicalArmor":51,"adjMinMagicArmor":51,"adjMaxMagicArmor":51,"adjHit":34,"adjRealDmg":6,"adjRealDmgDef":6,"adjDebilityEnh":8,"adjDebilityAnti":8})
    }),
    51017055: _tools.RODict({
        "propID": 51017055,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":60869,"adjMinPhysicalAtk":233,"adjMaxPhysicalAtk":420,"adjMinMagicAtk":233,"adjMaxMagicAtk":420,"adjMinPhysicalArmor":52,"adjMaxPhysicalArmor":52,"adjMinMagicArmor":52,"adjMaxMagicArmor":52,"adjHit":37,"adjRealDmg":6,"adjRealDmgDef":6,"adjDebilityEnh":8,"adjDebilityAnti":8})
    }),
    51017056: _tools.RODict({
        "propID": 51017056,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":66215,"adjMinPhysicalAtk":233,"adjMaxPhysicalAtk":420,"adjMinMagicAtk":233,"adjMaxMagicAtk":420,"adjMinPhysicalArmor":56,"adjMaxPhysicalArmor":56,"adjMinMagicArmor":56,"adjMaxMagicArmor":56,"adjHit":37,"adjRealDmg":6,"adjRealDmgDef":6,"adjDebilityEnh":8,"adjDebilityAnti":8})
    }),
    51017057: _tools.RODict({
        "propID": 51017057,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":69003,"adjMinPhysicalAtk":240,"adjMaxPhysicalAtk":435,"adjMinMagicAtk":240,"adjMaxMagicAtk":435,"adjMinPhysicalArmor":57,"adjMaxPhysicalArmor":57,"adjMinMagicArmor":57,"adjMaxMagicArmor":57,"adjHit":37,"adjRealDmg":7,"adjRealDmgDef":6,"adjDebilityEnh":8,"adjDebilityAnti":8})
    }),
    51017058: _tools.RODict({
        "propID": 51017058,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":69894,"adjMinPhysicalAtk":245,"adjMaxPhysicalAtk":443,"adjMinMagicAtk":245,"adjMaxMagicAtk":443,"adjMinPhysicalArmor":57,"adjMaxPhysicalArmor":57,"adjMinMagicArmor":57,"adjMaxMagicArmor":57,"adjHit":39,"adjRealDmg":7,"adjRealDmgDef":7,"adjDebilityEnh":8,"adjDebilityAnti":9})
    }),
    51017059: _tools.RODict({
        "propID": 51017059,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":72963,"adjMinPhysicalAtk":260,"adjMaxPhysicalAtk":473,"adjMinMagicAtk":260,"adjMaxMagicAtk":473,"adjMinPhysicalArmor":58,"adjMaxPhysicalArmor":58,"adjMinMagicArmor":58,"adjMaxMagicArmor":58,"adjHit":39,"adjRealDmg":7,"adjRealDmgDef":7,"adjDebilityEnh":9,"adjDebilityAnti":9})
    }),
    51017060: _tools.RODict({
        "propID": 51017060,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":75867,"adjMinPhysicalAtk":268,"adjMaxPhysicalAtk":485,"adjMinMagicAtk":268,"adjMaxMagicAtk":485,"adjMinPhysicalArmor":59,"adjMaxPhysicalArmor":59,"adjMinMagicArmor":59,"adjMaxMagicArmor":59,"adjHit":42,"adjRealDmg":7,"adjRealDmgDef":7,"adjDebilityEnh":9,"adjDebilityAnti":9})
    }),
    51017061: _tools.RODict({
        "propID": 51017061,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":85487,"adjMinPhysicalAtk":270,"adjMaxPhysicalAtk":488,"adjMinMagicAtk":270,"adjMaxMagicAtk":488,"adjMinPhysicalArmor":66,"adjMaxPhysicalArmor":66,"adjMinMagicArmor":66,"adjMaxMagicArmor":66,"adjHit":42,"adjRealDmg":7,"adjRealDmgDef":7,"adjDebilityEnh":9,"adjDebilityAnti":9})
    }),
    51017062: _tools.RODict({
        "propID": 51017062,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":88589,"adjMinPhysicalAtk":285,"adjMaxPhysicalAtk":523,"adjMinMagicAtk":285,"adjMaxMagicAtk":523,"adjMinPhysicalArmor":68,"adjMaxPhysicalArmor":68,"adjMinMagicArmor":68,"adjMaxMagicArmor":68,"adjHit":42,"adjRealDmg":9,"adjRealDmgDef":7,"adjDebilityEnh":9,"adjDebilityAnti":9})
    }),
    51017063: _tools.RODict({
        "propID": 51017063,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":89876,"adjMinPhysicalAtk":298,"adjMaxPhysicalAtk":540,"adjMinMagicAtk":298,"adjMaxMagicAtk":540,"adjMinPhysicalArmor":68,"adjMaxPhysicalArmor":68,"adjMinMagicArmor":68,"adjMaxMagicArmor":68,"adjHit":48,"adjRealDmg":9,"adjRealDmgDef":9,"adjDebilityEnh":9,"adjDebilityAnti":11})
    }),
    51017064: _tools.RODict({
        "propID": 51017064,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":94512,"adjMinPhysicalAtk":313,"adjMaxPhysicalAtk":568,"adjMinMagicAtk":313,"adjMaxMagicAtk":568,"adjMinPhysicalArmor":69,"adjMaxPhysicalArmor":69,"adjMinMagicArmor":69,"adjMaxMagicArmor":69,"adjHit":48,"adjRealDmg":9,"adjRealDmgDef":9,"adjDebilityEnh":11,"adjDebilityAnti":11})
    }),
    51017065: _tools.RODict({
        "propID": 51017065,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":99446,"adjMinPhysicalAtk":320,"adjMaxPhysicalAtk":583,"adjMinMagicAtk":320,"adjMaxMagicAtk":583,"adjMinPhysicalArmor":70,"adjMaxPhysicalArmor":70,"adjMinMagicArmor":70,"adjMaxMagicArmor":70,"adjHit":52,"adjRealDmg":9,"adjRealDmgDef":9,"adjDebilityEnh":11,"adjDebilityAnti":11})
    }),
    51017066: _tools.RODict({
        "propID": 51017066,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":107894,"adjMinPhysicalAtk":320,"adjMaxPhysicalAtk":583,"adjMinMagicAtk":320,"adjMaxMagicAtk":583,"adjMinPhysicalArmor":76,"adjMaxPhysicalArmor":76,"adjMinMagicArmor":76,"adjMaxMagicArmor":76,"adjHit":52,"adjRealDmg":9,"adjRealDmgDef":9,"adjDebilityEnh":11,"adjDebilityAnti":11})
    }),
    51017067: _tools.RODict({
        "propID": 51017067,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":111738,"adjMinPhysicalAtk":338,"adjMaxPhysicalAtk":613,"adjMinMagicAtk":338,"adjMaxMagicAtk":613,"adjMinPhysicalArmor":78,"adjMaxPhysicalArmor":78,"adjMinMagicArmor":78,"adjMaxMagicArmor":78,"adjHit":52,"adjRealDmg":11,"adjRealDmgDef":9,"adjDebilityEnh":11,"adjDebilityAnti":11})
    }),
    51017068: _tools.RODict({
        "propID": 51017068,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":113025,"adjMinPhysicalAtk":343,"adjMaxPhysicalAtk":623,"adjMinMagicAtk":343,"adjMaxMagicAtk":623,"adjMinPhysicalArmor":79,"adjMaxPhysicalArmor":79,"adjMinMagicArmor":79,"adjMaxMagicArmor":79,"adjHit":54,"adjRealDmg":11,"adjRealDmgDef":11,"adjDebilityEnh":11,"adjDebilityAnti":12})
    }),
    51017069: _tools.RODict({
        "propID": 51017069,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":117200,"adjMinPhysicalAtk":365,"adjMaxPhysicalAtk":660,"adjMinMagicAtk":365,"adjMaxMagicAtk":660,"adjMinPhysicalArmor":79,"adjMaxPhysicalArmor":79,"adjMinMagicArmor":79,"adjMaxMagicArmor":79,"adjHit":54,"adjRealDmg":11,"adjRealDmgDef":11,"adjDebilityEnh":12,"adjDebilityAnti":12})
    }),
    51017070: _tools.RODict({
        "propID": 51017070,
        "type": 1,
        "propList": _tools.RODict({"adjFullHp":121193,"adjMinPhysicalAtk":373,"adjMaxPhysicalAtk":675,"adjMinMagicAtk":373,"adjMaxMagicAtk":675,"adjMinPhysicalArmor":80,"adjMaxPhysicalArmor":80,"adjMinMagicArmor":80,"adjMaxMagicArmor":80,"adjHit":58,"adjRealDmg":11,"adjRealDmgDef":11,"adjDebilityEnh":12,"adjDebilityAnti":12})
    }),
    52012092: _tools.RODict({
        "propID": 52012092,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":30234,"adjMinPhysicalAtk":90,"adjMaxPhysicalAtk":168,"adjMinMagicAtk":90,"adjMaxMagicAtk":168,"adjHit":1,"adjDodge":1})
    }),
    52012093: _tools.RODict({
        "propID": 52012093,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":19445,"adjMinPhysicalAtk":100,"adjMaxPhysicalAtk":123,"adjMinMagicAtk":100,"adjMaxMagicAtk":123,"adjMinPhysicalArmor":19,"adjMaxPhysicalArmor":19,"adjMinMagicArmor":19,"adjMaxMagicArmor":19,"adjHit":90,"adjDodge":13,"adjRealDmg":1,"adjRealDmgDef":1})
    }),
    52012094: _tools.RODict({
        "propID": 52012094,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":76399,"adjMinPhysicalAtk":194,"adjMaxPhysicalAtk":237,"adjMinMagicAtk":194,"adjMaxMagicAtk":237,"adjMinPhysicalArmor":38,"adjMaxPhysicalArmor":38,"adjMinMagicArmor":38,"adjMaxMagicArmor":38,"adjHit":90,"adjDodge":15,"adjRealDmg":1,"adjRealDmgDef":1})
    }),
    52012095: _tools.RODict({
        "propID": 52012095,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":799094,"adjMinPhysicalAtk":116,"adjMaxPhysicalAtk":129,"adjMinMagicAtk":116,"adjMaxMagicAtk":129,"adjMinPhysicalArmor":22,"adjMaxPhysicalArmor":22,"adjMinMagicArmor":22,"adjMaxMagicArmor":22,"adjHit":90,"adjDodge":15,"adjRealDmg":3,"adjRealDmgDef":1})
    }),
    52012096: _tools.RODict({
        "propID": 52012096,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":10984406,"adjMinPhysicalAtk":248,"adjMaxPhysicalAtk":275,"adjMinMagicAtk":248,"adjMaxMagicAtk":275,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":50,"adjMaxMagicArmor":50,"adjHit":110,"adjDodge":20,"adjRealDmg":6,"adjRealDmgDef":1,"adjDebilityEnh":7,"adjDebilityAnti":15})
    }),
    52012097: _tools.RODict({
        "propID": 52012097,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":11843,"adjMinPhysicalAtk":248,"adjMaxPhysicalAtk":275,"adjMinMagicAtk":248,"adjMaxMagicAtk":275,"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":50,"adjMinMagicArmor":50,"adjMaxMagicArmor":50,"adjHit":110,"adjDodge":20,"adjRealDmg":6,"adjRealDmgDef":1,"adjDebilityEnh":7,"adjDebilityAnti":15})
    }),
    52012098: _tools.RODict({
        "propID": 52012098,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":40,"adjMaxMagicAtk":120})
    }),
    52012099: _tools.RODict({
        "propID": 52012099,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":56,"adjMaxMagicAtk":168,"adjHit":10,"adjFinalDmg":0.02})
    }),
    52012100: _tools.RODict({
        "propID": 52012100,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":78,"adjMaxMagicAtk":235,"adjHit":14,"adjFinalDmg":0.04})
    }),
    52012101: _tools.RODict({
        "propID": 52012101,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":116,"adjMaxMagicAtk":352,"adjHit":21,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012102: _tools.RODict({
        "propID": 52012102,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":40,"adjMaxMagicAtk":120})
    }),
    52012103: _tools.RODict({
        "propID": 52012103,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":56,"adjMaxMagicAtk":168,"adjHit":10,"adjFinalDmg":0.02})
    }),
    52012104: _tools.RODict({
        "propID": 52012104,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":78,"adjMaxMagicAtk":235,"adjHit":14,"adjFinalDmg":0.04})
    }),
    52012105: _tools.RODict({
        "propID": 52012105,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":116,"adjMaxMagicAtk":352,"adjHit":21,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012106: _tools.RODict({
        "propID": 52012106,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":40,"adjMaxPhysicalAtk":120})
    }),
    52012107: _tools.RODict({
        "propID": 52012107,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":56,"adjMaxPhysicalAtk":168,"adjHit":10,"adjFinalDmg":0.02})
    }),
    52012108: _tools.RODict({
        "propID": 52012108,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":78,"adjMaxPhysicalAtk":235,"adjHit":14,"adjFinalDmg":0.04})
    }),
    52012109: _tools.RODict({
        "propID": 52012109,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":116,"adjMaxPhysicalAtk":352,"adjHit":21,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012110: _tools.RODict({
        "propID": 52012110,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":10,"adjMaxPhysicalAtk":30})
    }),
    52012111: _tools.RODict({
        "propID": 52012111,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":14,"adjMaxPhysicalAtk":42,"adjFatal":10,"adjIgnoreArmor":0.04})
    }),
    52012112: _tools.RODict({
        "propID": 52012112,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":59,"adjFatal":14,"adjIgnoreArmor":0.08})
    }),
    52012113: _tools.RODict({
        "propID": 52012113,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":89,"adjFatal":21,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52012114: _tools.RODict({
        "propID": 52012114,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":10,"adjMaxMagicAtk":30})
    }),
    52012115: _tools.RODict({
        "propID": 52012115,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":14,"adjMaxMagicAtk":42,"adjFatal":10,"adjIgnoreArmor":0.04})
    }),
    52012116: _tools.RODict({
        "propID": 52012116,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":20,"adjMaxMagicAtk":59,"adjFatal":14,"adjIgnoreArmor":0.08})
    }),
    52012117: _tools.RODict({
        "propID": 52012117,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":30,"adjMaxMagicAtk":89,"adjFatal":21,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52012118: _tools.RODict({
        "propID": 52012118,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":400,"adjMinPhysicalAtk":8,"adjMaxPhysicalAtk":25})
    }),
    52012119: _tools.RODict({
        "propID": 52012119,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":560,"adjMinPhysicalAtk":11,"adjMaxPhysicalAtk":35,"adjMonsterDmg":0.025})
    }),
    52012120: _tools.RODict({
        "propID": 52012120,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":784,"adjMinPhysicalAtk":15,"adjMaxPhysicalAtk":49,"adjMonsterDmg":0.05})
    }),
    52012121: _tools.RODict({
        "propID": 52012121,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1172,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":74,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52012122: _tools.RODict({
        "propID": 52012122,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":400,"adjMinMagicAtk":8,"adjMaxMagicAtk":25})
    }),
    52012123: _tools.RODict({
        "propID": 52012123,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":560,"adjMinMagicAtk":11,"adjMaxMagicAtk":35,"adjMonsterDmg":0.025})
    }),
    52012124: _tools.RODict({
        "propID": 52012124,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":784,"adjMinMagicAtk":15,"adjMaxMagicAtk":49,"adjMonsterDmg":0.05})
    }),
    52012125: _tools.RODict({
        "propID": 52012125,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1172,"adjMinMagicAtk":23,"adjMaxMagicAtk":74,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52012126: _tools.RODict({
        "propID": 52012126,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":160,"adjMinPhysicalAtk":7,"adjMaxPhysicalAtk":20})
    }),
    52012127: _tools.RODict({
        "propID": 52012127,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":224,"adjMinPhysicalAtk":10,"adjMaxPhysicalAtk":28,"adjIgnoreArmor":0.02})
    }),
    52012128: _tools.RODict({
        "propID": 52012128,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":314,"adjMinPhysicalAtk":14,"adjMaxPhysicalAtk":39,"adjIgnoreArmor":0.04})
    }),
    52012129: _tools.RODict({
        "propID": 52012129,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":469,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":59,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52012130: _tools.RODict({
        "propID": 52012130,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":160,"adjMinMagicAtk":7,"adjMaxMagicAtk":20})
    }),
    52012131: _tools.RODict({
        "propID": 52012131,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":224,"adjMinMagicAtk":10,"adjMaxMagicAtk":28,"adjIgnoreArmor":0.02})
    }),
    52012132: _tools.RODict({
        "propID": 52012132,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":314,"adjMinMagicAtk":14,"adjMaxMagicAtk":39,"adjIgnoreArmor":0.04})
    }),
    52012133: _tools.RODict({
        "propID": 52012133,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":469,"adjMinMagicAtk":21,"adjMaxMagicAtk":59,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52012134: _tools.RODict({
        "propID": 52012134,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":24,"adjMaxPhysicalArmor":72,"adjMinMagicArmor":24,"adjMaxMagicArmor":72})
    }),
    52012135: _tools.RODict({
        "propID": 52012135,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":26,"adjMaxPhysicalArmor":75,"adjMinMagicArmor":26,"adjMaxMagicArmor":75,"adjMortal":0.05})
    }),
    52012136: _tools.RODict({
        "propID": 52012136,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":35,"adjMaxPhysicalArmor":105,"adjMinMagicArmor":35,"adjMaxMagicArmor":105,"adjMortal":0.1})
    }),
    52012137: _tools.RODict({
        "propID": 52012137,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":52,"adjMaxPhysicalArmor":156,"adjMinMagicArmor":52,"adjMaxMagicArmor":156,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012138: _tools.RODict({
        "propID": 52012138,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":8,"adjMaxPhysicalArmor":24})
    }),
    52012139: _tools.RODict({
        "propID": 52012139,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":15,"adjMaxPhysicalArmor":45,"adjDodge":10,"adjPVPDmg":0.02})
    }),
    52012140: _tools.RODict({
        "propID": 52012140,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":21,"adjMaxPhysicalArmor":64,"adjDodge":14,"adjPVPDmg":0.04})
    }),
    52012141: _tools.RODict({
        "propID": 52012141,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":32,"adjMaxPhysicalArmor":94,"adjDodge":21,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52012142: _tools.RODict({
        "propID": 52012142,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":400})
    }),
    52012143: _tools.RODict({
        "propID": 52012143,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":560,"adjDrugsQuantity":1,"adjFinalDmg":0.02})
    }),
    52012144: _tools.RODict({
        "propID": 52012144,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":784,"adjDrugsQuantity":3,"adjFinalDmg":0.04})
    }),
    52012145: _tools.RODict({
        "propID": 52012145,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1172,"adjDrugsQuantity":5,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012146: _tools.RODict({
        "propID": 52012146,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":8,"adjMaxMagicArmor":24})
    }),
    52012147: _tools.RODict({
        "propID": 52012147,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":15,"adjMaxMagicArmor":45,"adjAntiFatal":10,"adjMortal":0.05})
    }),
    52012148: _tools.RODict({
        "propID": 52012148,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":21,"adjMaxMagicArmor":64,"adjAntiFatal":14,"adjMortal":0.1})
    }),
    52012149: _tools.RODict({
        "propID": 52012149,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":32,"adjMaxMagicArmor":94,"adjAntiFatal":21,"adjMortal":0.1,"adjAntiMortal":0.1})
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
    52012166: _tools.RODict({
        "propID": 52012166,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":58,"adjMaxMagicAtk":126})
    }),
    52012167: _tools.RODict({
        "propID": 52012167,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":64,"adjMaxMagicAtk":139})
    }),
    52012168: _tools.RODict({
        "propID": 52012168,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":69,"adjMaxMagicAtk":151})
    }),
    52012169: _tools.RODict({
        "propID": 52012169,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":76,"adjMaxMagicAtk":164})
    }),
    52012170: _tools.RODict({
        "propID": 52012170,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":81,"adjMaxMagicAtk":176,"adjHit":11,"adjFinalDmg":0.02})
    }),
    52012171: _tools.RODict({
        "propID": 52012171,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":89,"adjMaxMagicAtk":194,"adjHit":12,"adjFinalDmg":0.02})
    }),
    52012172: _tools.RODict({
        "propID": 52012172,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":97,"adjMaxMagicAtk":212,"adjHit":13,"adjFinalDmg":0.02})
    }),
    52012173: _tools.RODict({
        "propID": 52012173,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":105,"adjMaxMagicAtk":229,"adjHit":14,"adjFinalDmg":0.02})
    }),
    52012174: _tools.RODict({
        "propID": 52012174,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":113,"adjMaxMagicAtk":247,"adjHit":15,"adjFinalDmg":0.04})
    }),
    52012175: _tools.RODict({
        "propID": 52012175,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":125,"adjMaxMagicAtk":272,"adjHit":16,"adjFinalDmg":0.04})
    }),
    52012176: _tools.RODict({
        "propID": 52012176,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":137,"adjMaxMagicAtk":296,"adjHit":18,"adjFinalDmg":0.04})
    }),
    52012177: _tools.RODict({
        "propID": 52012177,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":147,"adjMaxMagicAtk":321,"adjHit":19,"adjFinalDmg":0.04})
    }),
    52012178: _tools.RODict({
        "propID": 52012178,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":169,"adjMaxMagicAtk":370,"adjHit":22,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012179: _tools.RODict({
        "propID": 52012179,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":186,"adjMaxMagicAtk":406,"adjHit":24,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012180: _tools.RODict({
        "propID": 52012180,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":205,"adjMaxMagicAtk":447,"adjHit":26,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012181: _tools.RODict({
        "propID": 52012181,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":226,"adjMaxMagicAtk":492,"adjHit":29,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012182: _tools.RODict({
        "propID": 52012182,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":61,"adjMaxMagicAtk":132})
    }),
    52012183: _tools.RODict({
        "propID": 52012183,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":67,"adjMaxMagicAtk":146})
    }),
    52012184: _tools.RODict({
        "propID": 52012184,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":72,"adjMaxMagicAtk":159})
    }),
    52012185: _tools.RODict({
        "propID": 52012185,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":80,"adjMaxMagicAtk":172})
    }),
    52012186: _tools.RODict({
        "propID": 52012186,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":85,"adjMaxMagicAtk":185,"adjHit":12,"adjFinalDmg":0.02})
    }),
    52012187: _tools.RODict({
        "propID": 52012187,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":93,"adjMaxMagicAtk":204,"adjHit":13,"adjFinalDmg":0.02})
    }),
    52012188: _tools.RODict({
        "propID": 52012188,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":102,"adjMaxMagicAtk":223,"adjHit":14,"adjFinalDmg":0.02})
    }),
    52012189: _tools.RODict({
        "propID": 52012189,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":110,"adjMaxMagicAtk":240,"adjHit":15,"adjFinalDmg":0.02})
    }),
    52012190: _tools.RODict({
        "propID": 52012190,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":119,"adjMaxMagicAtk":259,"adjHit":16,"adjFinalDmg":0.04})
    }),
    52012191: _tools.RODict({
        "propID": 52012191,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":131,"adjMaxMagicAtk":286,"adjHit":17,"adjFinalDmg":0.04})
    }),
    52012192: _tools.RODict({
        "propID": 52012192,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":144,"adjMaxMagicAtk":311,"adjHit":19,"adjFinalDmg":0.04})
    }),
    52012193: _tools.RODict({
        "propID": 52012193,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":154,"adjMaxMagicAtk":337,"adjHit":20,"adjFinalDmg":0.04})
    }),
    52012194: _tools.RODict({
        "propID": 52012194,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":177,"adjMaxMagicAtk":389,"adjHit":23,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012195: _tools.RODict({
        "propID": 52012195,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":195,"adjMaxMagicAtk":426,"adjHit":25,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012196: _tools.RODict({
        "propID": 52012196,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":215,"adjMaxMagicAtk":469,"adjHit":27,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012197: _tools.RODict({
        "propID": 52012197,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":237,"adjMaxMagicAtk":517,"adjHit":30,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012198: _tools.RODict({
        "propID": 52012198,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":64,"adjMaxMagicAtk":139})
    }),
    52012199: _tools.RODict({
        "propID": 52012199,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":70,"adjMaxMagicAtk":153})
    }),
    52012200: _tools.RODict({
        "propID": 52012200,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":76,"adjMaxMagicAtk":167})
    }),
    52012201: _tools.RODict({
        "propID": 52012201,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":84,"adjMaxMagicAtk":181})
    }),
    52012202: _tools.RODict({
        "propID": 52012202,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":89,"adjMaxMagicAtk":194,"adjHit":13,"adjFinalDmg":0.02})
    }),
    52012203: _tools.RODict({
        "propID": 52012203,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":98,"adjMaxMagicAtk":214,"adjHit":14,"adjFinalDmg":0.02})
    }),
    52012204: _tools.RODict({
        "propID": 52012204,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":107,"adjMaxMagicAtk":234,"adjHit":15,"adjFinalDmg":0.02})
    }),
    52012205: _tools.RODict({
        "propID": 52012205,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":116,"adjMaxMagicAtk":252,"adjHit":16,"adjFinalDmg":0.02})
    }),
    52012206: _tools.RODict({
        "propID": 52012206,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":125,"adjMaxMagicAtk":272,"adjHit":17,"adjFinalDmg":0.04})
    }),
    52012207: _tools.RODict({
        "propID": 52012207,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":138,"adjMaxMagicAtk":300,"adjHit":18,"adjFinalDmg":0.04})
    }),
    52012208: _tools.RODict({
        "propID": 52012208,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":151,"adjMaxMagicAtk":327,"adjHit":20,"adjFinalDmg":0.04})
    }),
    52012209: _tools.RODict({
        "propID": 52012209,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":162,"adjMaxMagicAtk":354,"adjHit":21,"adjFinalDmg":0.04})
    }),
    52012210: _tools.RODict({
        "propID": 52012210,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":186,"adjMaxMagicAtk":408,"adjHit":24,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012211: _tools.RODict({
        "propID": 52012211,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":205,"adjMaxMagicAtk":447,"adjHit":26,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012212: _tools.RODict({
        "propID": 52012212,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":226,"adjMaxMagicAtk":492,"adjHit":28,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012213: _tools.RODict({
        "propID": 52012213,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":249,"adjMaxMagicAtk":543,"adjHit":32,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012214: _tools.RODict({
        "propID": 52012214,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":67,"adjMaxMagicAtk":146})
    }),
    52012215: _tools.RODict({
        "propID": 52012215,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":74,"adjMaxMagicAtk":161})
    }),
    52012216: _tools.RODict({
        "propID": 52012216,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":80,"adjMaxMagicAtk":175})
    }),
    52012217: _tools.RODict({
        "propID": 52012217,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":88,"adjMaxMagicAtk":190})
    }),
    52012218: _tools.RODict({
        "propID": 52012218,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":93,"adjMaxMagicAtk":204,"adjHit":14,"adjFinalDmg":0.02})
    }),
    52012219: _tools.RODict({
        "propID": 52012219,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":103,"adjMaxMagicAtk":225,"adjHit":15,"adjFinalDmg":0.02})
    }),
    52012220: _tools.RODict({
        "propID": 52012220,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":112,"adjMaxMagicAtk":246,"adjHit":16,"adjFinalDmg":0.02})
    }),
    52012221: _tools.RODict({
        "propID": 52012221,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":122,"adjMaxMagicAtk":265,"adjHit":17,"adjFinalDmg":0.02})
    }),
    52012222: _tools.RODict({
        "propID": 52012222,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":131,"adjMaxMagicAtk":286,"adjHit":18,"adjFinalDmg":0.04})
    }),
    52012223: _tools.RODict({
        "propID": 52012223,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":145,"adjMaxMagicAtk":315,"adjHit":19,"adjFinalDmg":0.04})
    }),
    52012224: _tools.RODict({
        "propID": 52012224,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":159,"adjMaxMagicAtk":343,"adjHit":21,"adjFinalDmg":0.04})
    }),
    52012225: _tools.RODict({
        "propID": 52012225,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":170,"adjMaxMagicAtk":372,"adjHit":22,"adjFinalDmg":0.04})
    }),
    52012226: _tools.RODict({
        "propID": 52012226,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":195,"adjMaxMagicAtk":428,"adjHit":25,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012227: _tools.RODict({
        "propID": 52012227,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":215,"adjMaxMagicAtk":469,"adjHit":27,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012228: _tools.RODict({
        "propID": 52012228,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":237,"adjMaxMagicAtk":517,"adjHit":29,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012229: _tools.RODict({
        "propID": 52012229,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":261,"adjMaxMagicAtk":570,"adjHit":34,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012230: _tools.RODict({
        "propID": 52012230,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":70,"adjMaxMagicAtk":153})
    }),
    52012231: _tools.RODict({
        "propID": 52012231,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":78,"adjMaxMagicAtk":169})
    }),
    52012232: _tools.RODict({
        "propID": 52012232,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":84,"adjMaxMagicAtk":184})
    }),
    52012233: _tools.RODict({
        "propID": 52012233,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":92,"adjMaxMagicAtk":200})
    }),
    52012234: _tools.RODict({
        "propID": 52012234,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":98,"adjMaxMagicAtk":214,"adjHit":15,"adjFinalDmg":0.02})
    }),
    52012235: _tools.RODict({
        "propID": 52012235,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":108,"adjMaxMagicAtk":236,"adjHit":16,"adjFinalDmg":0.02})
    }),
    52012236: _tools.RODict({
        "propID": 52012236,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":118,"adjMaxMagicAtk":258,"adjHit":17,"adjFinalDmg":0.02})
    }),
    52012237: _tools.RODict({
        "propID": 52012237,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":128,"adjMaxMagicAtk":278,"adjHit":18,"adjFinalDmg":0.02})
    }),
    52012238: _tools.RODict({
        "propID": 52012238,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":138,"adjMaxMagicAtk":300,"adjHit":19,"adjFinalDmg":0.04})
    }),
    52012239: _tools.RODict({
        "propID": 52012239,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":152,"adjMaxMagicAtk":331,"adjHit":20,"adjFinalDmg":0.04})
    }),
    52012240: _tools.RODict({
        "propID": 52012240,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":167,"adjMaxMagicAtk":360,"adjHit":22,"adjFinalDmg":0.04})
    }),
    52012241: _tools.RODict({
        "propID": 52012241,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":179,"adjMaxMagicAtk":391,"adjHit":23,"adjFinalDmg":0.04})
    }),
    52012242: _tools.RODict({
        "propID": 52012242,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":205,"adjMaxMagicAtk":449,"adjHit":26,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012243: _tools.RODict({
        "propID": 52012243,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":226,"adjMaxMagicAtk":492,"adjHit":28,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012244: _tools.RODict({
        "propID": 52012244,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":249,"adjMaxMagicAtk":543,"adjHit":30,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012245: _tools.RODict({
        "propID": 52012245,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":274,"adjMaxMagicAtk":599,"adjHit":36,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012246: _tools.RODict({
        "propID": 52012246,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":74,"adjMaxMagicAtk":161})
    }),
    52012247: _tools.RODict({
        "propID": 52012247,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":82,"adjMaxMagicAtk":177})
    }),
    52012248: _tools.RODict({
        "propID": 52012248,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":88,"adjMaxMagicAtk":193})
    }),
    52012249: _tools.RODict({
        "propID": 52012249,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":97,"adjMaxMagicAtk":210})
    }),
    52012250: _tools.RODict({
        "propID": 52012250,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":103,"adjMaxMagicAtk":225,"adjHit":16,"adjFinalDmg":0.02})
    }),
    52012251: _tools.RODict({
        "propID": 52012251,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":113,"adjMaxMagicAtk":248,"adjHit":17,"adjFinalDmg":0.02})
    }),
    52012252: _tools.RODict({
        "propID": 52012252,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":124,"adjMaxMagicAtk":271,"adjHit":18,"adjFinalDmg":0.02})
    }),
    52012253: _tools.RODict({
        "propID": 52012253,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":134,"adjMaxMagicAtk":292,"adjHit":19,"adjFinalDmg":0.02})
    }),
    52012254: _tools.RODict({
        "propID": 52012254,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":145,"adjMaxMagicAtk":315,"adjHit":20,"adjFinalDmg":0.04})
    }),
    52012255: _tools.RODict({
        "propID": 52012255,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":160,"adjMaxMagicAtk":348,"adjHit":21,"adjFinalDmg":0.04})
    }),
    52012256: _tools.RODict({
        "propID": 52012256,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":175,"adjMaxMagicAtk":378,"adjHit":23,"adjFinalDmg":0.04})
    }),
    52012257: _tools.RODict({
        "propID": 52012257,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":188,"adjMaxMagicAtk":411,"adjHit":24,"adjFinalDmg":0.04})
    }),
    52012258: _tools.RODict({
        "propID": 52012258,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":215,"adjMaxMagicAtk":471,"adjHit":27,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012259: _tools.RODict({
        "propID": 52012259,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":237,"adjMaxMagicAtk":517,"adjHit":29,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012260: _tools.RODict({
        "propID": 52012260,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":261,"adjMaxMagicAtk":570,"adjHit":32,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012261: _tools.RODict({
        "propID": 52012261,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":288,"adjMaxMagicAtk":629,"adjHit":38,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012262: _tools.RODict({
        "propID": 52012262,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":78,"adjMaxMagicAtk":169})
    }),
    52012263: _tools.RODict({
        "propID": 52012263,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":86,"adjMaxMagicAtk":186})
    }),
    52012264: _tools.RODict({
        "propID": 52012264,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":92,"adjMaxMagicAtk":203})
    }),
    52012265: _tools.RODict({
        "propID": 52012265,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":102,"adjMaxMagicAtk":221})
    }),
    52012266: _tools.RODict({
        "propID": 52012266,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":108,"adjMaxMagicAtk":236,"adjHit":17,"adjFinalDmg":0.02})
    }),
    52012267: _tools.RODict({
        "propID": 52012267,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":119,"adjMaxMagicAtk":260,"adjHit":18,"adjFinalDmg":0.02})
    }),
    52012268: _tools.RODict({
        "propID": 52012268,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":130,"adjMaxMagicAtk":285,"adjHit":19,"adjFinalDmg":0.02})
    }),
    52012269: _tools.RODict({
        "propID": 52012269,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":141,"adjMaxMagicAtk":307,"adjHit":20,"adjFinalDmg":0.02})
    }),
    52012270: _tools.RODict({
        "propID": 52012270,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":152,"adjMaxMagicAtk":331,"adjHit":21,"adjFinalDmg":0.04})
    }),
    52012271: _tools.RODict({
        "propID": 52012271,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":168,"adjMaxMagicAtk":365,"adjHit":22,"adjFinalDmg":0.04})
    }),
    52012272: _tools.RODict({
        "propID": 52012272,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":184,"adjMaxMagicAtk":397,"adjHit":24,"adjFinalDmg":0.04})
    }),
    52012273: _tools.RODict({
        "propID": 52012273,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":197,"adjMaxMagicAtk":432,"adjHit":25,"adjFinalDmg":0.04})
    }),
    52012274: _tools.RODict({
        "propID": 52012274,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":226,"adjMaxMagicAtk":495,"adjHit":28,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012275: _tools.RODict({
        "propID": 52012275,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":249,"adjMaxMagicAtk":543,"adjHit":30,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012276: _tools.RODict({
        "propID": 52012276,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":274,"adjMaxMagicAtk":599,"adjHit":34,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012277: _tools.RODict({
        "propID": 52012277,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":302,"adjMaxMagicAtk":660,"adjHit":40,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012278: _tools.RODict({
        "propID": 52012278,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":82,"adjMaxMagicAtk":177})
    }),
    52012279: _tools.RODict({
        "propID": 52012279,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":90,"adjMaxMagicAtk":195})
    }),
    52012280: _tools.RODict({
        "propID": 52012280,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":97,"adjMaxMagicAtk":213})
    }),
    52012281: _tools.RODict({
        "propID": 52012281,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":107,"adjMaxMagicAtk":232})
    }),
    52012282: _tools.RODict({
        "propID": 52012282,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":113,"adjMaxMagicAtk":248,"adjHit":18,"adjFinalDmg":0.02})
    }),
    52012283: _tools.RODict({
        "propID": 52012283,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":125,"adjMaxMagicAtk":273,"adjHit":19,"adjFinalDmg":0.02})
    }),
    52012284: _tools.RODict({
        "propID": 52012284,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":137,"adjMaxMagicAtk":299,"adjHit":20,"adjFinalDmg":0.02})
    }),
    52012285: _tools.RODict({
        "propID": 52012285,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":148,"adjMaxMagicAtk":322,"adjHit":21,"adjFinalDmg":0.02})
    }),
    52012286: _tools.RODict({
        "propID": 52012286,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":160,"adjMaxMagicAtk":348,"adjHit":22,"adjFinalDmg":0.04})
    }),
    52012287: _tools.RODict({
        "propID": 52012287,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":176,"adjMaxMagicAtk":383,"adjHit":23,"adjFinalDmg":0.04})
    }),
    52012288: _tools.RODict({
        "propID": 52012288,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":193,"adjMaxMagicAtk":417,"adjHit":25,"adjFinalDmg":0.04})
    }),
    52012289: _tools.RODict({
        "propID": 52012289,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":207,"adjMaxMagicAtk":454,"adjHit":26,"adjFinalDmg":0.04})
    }),
    52012290: _tools.RODict({
        "propID": 52012290,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":237,"adjMaxMagicAtk":520,"adjHit":29,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012291: _tools.RODict({
        "propID": 52012291,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":261,"adjMaxMagicAtk":570,"adjHit":32,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012292: _tools.RODict({
        "propID": 52012292,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":288,"adjMaxMagicAtk":629,"adjHit":36,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012293: _tools.RODict({
        "propID": 52012293,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":317,"adjMaxMagicAtk":693,"adjHit":42,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012294: _tools.RODict({
        "propID": 52012294,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":86,"adjMaxMagicAtk":186})
    }),
    52012295: _tools.RODict({
        "propID": 52012295,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":95,"adjMaxMagicAtk":205})
    }),
    52012296: _tools.RODict({
        "propID": 52012296,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":102,"adjMaxMagicAtk":224})
    }),
    52012297: _tools.RODict({
        "propID": 52012297,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":112,"adjMaxMagicAtk":244})
    }),
    52012298: _tools.RODict({
        "propID": 52012298,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":119,"adjMaxMagicAtk":260,"adjHit":19,"adjFinalDmg":0.02})
    }),
    52012299: _tools.RODict({
        "propID": 52012299,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":131,"adjMaxMagicAtk":287,"adjHit":20,"adjFinalDmg":0.02})
    }),
    52012300: _tools.RODict({
        "propID": 52012300,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":144,"adjMaxMagicAtk":314,"adjHit":21,"adjFinalDmg":0.02})
    }),
    52012301: _tools.RODict({
        "propID": 52012301,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":155,"adjMaxMagicAtk":338,"adjHit":22,"adjFinalDmg":0.02})
    }),
    52012302: _tools.RODict({
        "propID": 52012302,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":168,"adjMaxMagicAtk":365,"adjHit":23,"adjFinalDmg":0.04})
    }),
    52012303: _tools.RODict({
        "propID": 52012303,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":185,"adjMaxMagicAtk":402,"adjHit":24,"adjFinalDmg":0.04})
    }),
    52012304: _tools.RODict({
        "propID": 52012304,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":203,"adjMaxMagicAtk":438,"adjHit":26,"adjFinalDmg":0.04})
    }),
    52012305: _tools.RODict({
        "propID": 52012305,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":217,"adjMaxMagicAtk":477,"adjHit":27,"adjFinalDmg":0.04})
    }),
    52012306: _tools.RODict({
        "propID": 52012306,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":249,"adjMaxMagicAtk":546,"adjHit":30,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012307: _tools.RODict({
        "propID": 52012307,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":274,"adjMaxMagicAtk":599,"adjHit":34,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012308: _tools.RODict({
        "propID": 52012308,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":302,"adjMaxMagicAtk":660,"adjHit":38,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012309: _tools.RODict({
        "propID": 52012309,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":333,"adjMaxMagicAtk":728,"adjHit":44,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012310: _tools.RODict({
        "propID": 52012310,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":90,"adjMaxMagicAtk":195})
    }),
    52012311: _tools.RODict({
        "propID": 52012311,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":100,"adjMaxMagicAtk":215})
    }),
    52012312: _tools.RODict({
        "propID": 52012312,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":107,"adjMaxMagicAtk":235})
    }),
    52012313: _tools.RODict({
        "propID": 52012313,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":118,"adjMaxMagicAtk":256})
    }),
    52012314: _tools.RODict({
        "propID": 52012314,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":125,"adjMaxMagicAtk":273,"adjHit":20,"adjFinalDmg":0.02})
    }),
    52012315: _tools.RODict({
        "propID": 52012315,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":138,"adjMaxMagicAtk":301,"adjHit":21,"adjFinalDmg":0.02})
    }),
    52012316: _tools.RODict({
        "propID": 52012316,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":151,"adjMaxMagicAtk":330,"adjHit":22,"adjFinalDmg":0.02})
    }),
    52012317: _tools.RODict({
        "propID": 52012317,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":163,"adjMaxMagicAtk":355,"adjHit":23,"adjFinalDmg":0.02})
    }),
    52012318: _tools.RODict({
        "propID": 52012318,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":176,"adjMaxMagicAtk":383,"adjHit":24,"adjFinalDmg":0.04})
    }),
    52012319: _tools.RODict({
        "propID": 52012319,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":194,"adjMaxMagicAtk":422,"adjHit":25,"adjFinalDmg":0.04})
    }),
    52012320: _tools.RODict({
        "propID": 52012320,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":213,"adjMaxMagicAtk":460,"adjHit":27,"adjFinalDmg":0.04})
    }),
    52012321: _tools.RODict({
        "propID": 52012321,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":228,"adjMaxMagicAtk":501,"adjHit":28,"adjFinalDmg":0.04})
    }),
    52012322: _tools.RODict({
        "propID": 52012322,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":261,"adjMaxMagicAtk":573,"adjHit":32,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012323: _tools.RODict({
        "propID": 52012323,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":288,"adjMaxMagicAtk":629,"adjHit":36,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012324: _tools.RODict({
        "propID": 52012324,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":317,"adjMaxMagicAtk":693,"adjHit":40,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012325: _tools.RODict({
        "propID": 52012325,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":350,"adjMaxMagicAtk":764,"adjHit":46,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
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
    52012342: _tools.RODict({
        "propID": 52012342,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":58,"adjMaxMagicAtk":126})
    }),
    52012343: _tools.RODict({
        "propID": 52012343,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":64,"adjMaxMagicAtk":139})
    }),
    52012344: _tools.RODict({
        "propID": 52012344,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":69,"adjMaxMagicAtk":151})
    }),
    52012345: _tools.RODict({
        "propID": 52012345,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":76,"adjMaxMagicAtk":164})
    }),
    52012346: _tools.RODict({
        "propID": 52012346,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":81,"adjMaxMagicAtk":176,"adjHit":11,"adjFinalDmg":0.02})
    }),
    52012347: _tools.RODict({
        "propID": 52012347,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":89,"adjMaxMagicAtk":194,"adjHit":12,"adjFinalDmg":0.02})
    }),
    52012348: _tools.RODict({
        "propID": 52012348,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":97,"adjMaxMagicAtk":212,"adjHit":13,"adjFinalDmg":0.02})
    }),
    52012349: _tools.RODict({
        "propID": 52012349,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":105,"adjMaxMagicAtk":229,"adjHit":14,"adjFinalDmg":0.02})
    }),
    52012350: _tools.RODict({
        "propID": 52012350,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":113,"adjMaxMagicAtk":247,"adjHit":15,"adjFinalDmg":0.04})
    }),
    52012351: _tools.RODict({
        "propID": 52012351,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":125,"adjMaxMagicAtk":272,"adjHit":16,"adjFinalDmg":0.04})
    }),
    52012352: _tools.RODict({
        "propID": 52012352,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":137,"adjMaxMagicAtk":296,"adjHit":18,"adjFinalDmg":0.04})
    }),
    52012353: _tools.RODict({
        "propID": 52012353,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":147,"adjMaxMagicAtk":321,"adjHit":19,"adjFinalDmg":0.04})
    }),
    52012354: _tools.RODict({
        "propID": 52012354,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":169,"adjMaxMagicAtk":370,"adjHit":22,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012355: _tools.RODict({
        "propID": 52012355,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":186,"adjMaxMagicAtk":406,"adjHit":24,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012356: _tools.RODict({
        "propID": 52012356,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":205,"adjMaxMagicAtk":447,"adjHit":26,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012357: _tools.RODict({
        "propID": 52012357,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":226,"adjMaxMagicAtk":492,"adjHit":29,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012358: _tools.RODict({
        "propID": 52012358,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":61,"adjMaxMagicAtk":132})
    }),
    52012359: _tools.RODict({
        "propID": 52012359,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":67,"adjMaxMagicAtk":146})
    }),
    52012360: _tools.RODict({
        "propID": 52012360,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":72,"adjMaxMagicAtk":159})
    }),
    52012361: _tools.RODict({
        "propID": 52012361,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":80,"adjMaxMagicAtk":172})
    }),
    52012362: _tools.RODict({
        "propID": 52012362,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":85,"adjMaxMagicAtk":185,"adjHit":12,"adjFinalDmg":0.02})
    }),
    52012363: _tools.RODict({
        "propID": 52012363,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":93,"adjMaxMagicAtk":204,"adjHit":13,"adjFinalDmg":0.02})
    }),
    52012364: _tools.RODict({
        "propID": 52012364,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":102,"adjMaxMagicAtk":223,"adjHit":14,"adjFinalDmg":0.02})
    }),
    52012365: _tools.RODict({
        "propID": 52012365,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":110,"adjMaxMagicAtk":240,"adjHit":15,"adjFinalDmg":0.02})
    }),
    52012366: _tools.RODict({
        "propID": 52012366,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":119,"adjMaxMagicAtk":259,"adjHit":16,"adjFinalDmg":0.04})
    }),
    52012367: _tools.RODict({
        "propID": 52012367,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":131,"adjMaxMagicAtk":286,"adjHit":17,"adjFinalDmg":0.04})
    }),
    52012368: _tools.RODict({
        "propID": 52012368,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":144,"adjMaxMagicAtk":311,"adjHit":19,"adjFinalDmg":0.04})
    }),
    52012369: _tools.RODict({
        "propID": 52012369,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":154,"adjMaxMagicAtk":337,"adjHit":20,"adjFinalDmg":0.04})
    }),
    52012370: _tools.RODict({
        "propID": 52012370,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":177,"adjMaxMagicAtk":389,"adjHit":23,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012371: _tools.RODict({
        "propID": 52012371,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":195,"adjMaxMagicAtk":426,"adjHit":25,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012372: _tools.RODict({
        "propID": 52012372,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":215,"adjMaxMagicAtk":469,"adjHit":27,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012373: _tools.RODict({
        "propID": 52012373,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":237,"adjMaxMagicAtk":517,"adjHit":30,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012374: _tools.RODict({
        "propID": 52012374,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":64,"adjMaxMagicAtk":139})
    }),
    52012375: _tools.RODict({
        "propID": 52012375,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":70,"adjMaxMagicAtk":153})
    }),
    52012376: _tools.RODict({
        "propID": 52012376,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":76,"adjMaxMagicAtk":167})
    }),
    52012377: _tools.RODict({
        "propID": 52012377,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":84,"adjMaxMagicAtk":181})
    }),
    52012378: _tools.RODict({
        "propID": 52012378,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":89,"adjMaxMagicAtk":194,"adjHit":13,"adjFinalDmg":0.02})
    }),
    52012379: _tools.RODict({
        "propID": 52012379,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":98,"adjMaxMagicAtk":214,"adjHit":14,"adjFinalDmg":0.02})
    }),
    52012380: _tools.RODict({
        "propID": 52012380,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":107,"adjMaxMagicAtk":234,"adjHit":15,"adjFinalDmg":0.02})
    }),
    52012381: _tools.RODict({
        "propID": 52012381,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":116,"adjMaxMagicAtk":252,"adjHit":16,"adjFinalDmg":0.02})
    }),
    52012382: _tools.RODict({
        "propID": 52012382,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":125,"adjMaxMagicAtk":272,"adjHit":17,"adjFinalDmg":0.04})
    }),
    52012383: _tools.RODict({
        "propID": 52012383,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":138,"adjMaxMagicAtk":300,"adjHit":18,"adjFinalDmg":0.04})
    }),
    52012384: _tools.RODict({
        "propID": 52012384,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":151,"adjMaxMagicAtk":327,"adjHit":20,"adjFinalDmg":0.04})
    }),
    52012385: _tools.RODict({
        "propID": 52012385,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":162,"adjMaxMagicAtk":354,"adjHit":21,"adjFinalDmg":0.04})
    }),
    52012386: _tools.RODict({
        "propID": 52012386,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":186,"adjMaxMagicAtk":408,"adjHit":24,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012387: _tools.RODict({
        "propID": 52012387,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":205,"adjMaxMagicAtk":447,"adjHit":26,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012388: _tools.RODict({
        "propID": 52012388,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":226,"adjMaxMagicAtk":492,"adjHit":28,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012389: _tools.RODict({
        "propID": 52012389,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":249,"adjMaxMagicAtk":543,"adjHit":32,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012390: _tools.RODict({
        "propID": 52012390,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":67,"adjMaxMagicAtk":146})
    }),
    52012391: _tools.RODict({
        "propID": 52012391,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":74,"adjMaxMagicAtk":161})
    }),
    52012392: _tools.RODict({
        "propID": 52012392,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":80,"adjMaxMagicAtk":175})
    }),
    52012393: _tools.RODict({
        "propID": 52012393,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":88,"adjMaxMagicAtk":190})
    }),
    52012394: _tools.RODict({
        "propID": 52012394,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":93,"adjMaxMagicAtk":204,"adjHit":14,"adjFinalDmg":0.02})
    }),
    52012395: _tools.RODict({
        "propID": 52012395,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":103,"adjMaxMagicAtk":225,"adjHit":15,"adjFinalDmg":0.02})
    }),
    52012396: _tools.RODict({
        "propID": 52012396,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":112,"adjMaxMagicAtk":246,"adjHit":16,"adjFinalDmg":0.02})
    }),
    52012397: _tools.RODict({
        "propID": 52012397,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":122,"adjMaxMagicAtk":265,"adjHit":17,"adjFinalDmg":0.02})
    }),
    52012398: _tools.RODict({
        "propID": 52012398,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":131,"adjMaxMagicAtk":286,"adjHit":18,"adjFinalDmg":0.04})
    }),
    52012399: _tools.RODict({
        "propID": 52012399,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":145,"adjMaxMagicAtk":315,"adjHit":19,"adjFinalDmg":0.04})
    }),
    52012400: _tools.RODict({
        "propID": 52012400,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":159,"adjMaxMagicAtk":343,"adjHit":21,"adjFinalDmg":0.04})
    }),
    52012401: _tools.RODict({
        "propID": 52012401,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":170,"adjMaxMagicAtk":372,"adjHit":22,"adjFinalDmg":0.04})
    }),
    52012402: _tools.RODict({
        "propID": 52012402,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":195,"adjMaxMagicAtk":428,"adjHit":25,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012403: _tools.RODict({
        "propID": 52012403,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":215,"adjMaxMagicAtk":469,"adjHit":27,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012404: _tools.RODict({
        "propID": 52012404,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":237,"adjMaxMagicAtk":517,"adjHit":29,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012405: _tools.RODict({
        "propID": 52012405,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":261,"adjMaxMagicAtk":570,"adjHit":34,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012406: _tools.RODict({
        "propID": 52012406,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":70,"adjMaxMagicAtk":153})
    }),
    52012407: _tools.RODict({
        "propID": 52012407,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":78,"adjMaxMagicAtk":169})
    }),
    52012408: _tools.RODict({
        "propID": 52012408,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":84,"adjMaxMagicAtk":184})
    }),
    52012409: _tools.RODict({
        "propID": 52012409,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":92,"adjMaxMagicAtk":200})
    }),
    52012410: _tools.RODict({
        "propID": 52012410,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":98,"adjMaxMagicAtk":214,"adjHit":15,"adjFinalDmg":0.02})
    }),
    52012411: _tools.RODict({
        "propID": 52012411,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":108,"adjMaxMagicAtk":236,"adjHit":16,"adjFinalDmg":0.02})
    }),
    52012412: _tools.RODict({
        "propID": 52012412,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":118,"adjMaxMagicAtk":258,"adjHit":17,"adjFinalDmg":0.02})
    }),
    52012413: _tools.RODict({
        "propID": 52012413,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":128,"adjMaxMagicAtk":278,"adjHit":18,"adjFinalDmg":0.02})
    }),
    52012414: _tools.RODict({
        "propID": 52012414,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":138,"adjMaxMagicAtk":300,"adjHit":19,"adjFinalDmg":0.04})
    }),
    52012415: _tools.RODict({
        "propID": 52012415,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":152,"adjMaxMagicAtk":331,"adjHit":20,"adjFinalDmg":0.04})
    }),
    52012416: _tools.RODict({
        "propID": 52012416,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":167,"adjMaxMagicAtk":360,"adjHit":22,"adjFinalDmg":0.04})
    }),
    52012417: _tools.RODict({
        "propID": 52012417,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":179,"adjMaxMagicAtk":391,"adjHit":23,"adjFinalDmg":0.04})
    }),
    52012418: _tools.RODict({
        "propID": 52012418,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":205,"adjMaxMagicAtk":449,"adjHit":26,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012419: _tools.RODict({
        "propID": 52012419,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":226,"adjMaxMagicAtk":492,"adjHit":28,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012420: _tools.RODict({
        "propID": 52012420,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":249,"adjMaxMagicAtk":543,"adjHit":30,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012421: _tools.RODict({
        "propID": 52012421,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":274,"adjMaxMagicAtk":599,"adjHit":36,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012422: _tools.RODict({
        "propID": 52012422,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":74,"adjMaxMagicAtk":161})
    }),
    52012423: _tools.RODict({
        "propID": 52012423,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":82,"adjMaxMagicAtk":177})
    }),
    52012424: _tools.RODict({
        "propID": 52012424,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":88,"adjMaxMagicAtk":193})
    }),
    52012425: _tools.RODict({
        "propID": 52012425,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":97,"adjMaxMagicAtk":210})
    }),
    52012426: _tools.RODict({
        "propID": 52012426,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":103,"adjMaxMagicAtk":225,"adjHit":16,"adjFinalDmg":0.02})
    }),
    52012427: _tools.RODict({
        "propID": 52012427,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":113,"adjMaxMagicAtk":248,"adjHit":17,"adjFinalDmg":0.02})
    }),
    52012428: _tools.RODict({
        "propID": 52012428,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":124,"adjMaxMagicAtk":271,"adjHit":18,"adjFinalDmg":0.02})
    }),
    52012429: _tools.RODict({
        "propID": 52012429,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":134,"adjMaxMagicAtk":292,"adjHit":19,"adjFinalDmg":0.02})
    }),
    52012430: _tools.RODict({
        "propID": 52012430,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":145,"adjMaxMagicAtk":315,"adjHit":20,"adjFinalDmg":0.04})
    }),
    52012431: _tools.RODict({
        "propID": 52012431,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":160,"adjMaxMagicAtk":348,"adjHit":21,"adjFinalDmg":0.04})
    }),
    52012432: _tools.RODict({
        "propID": 52012432,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":175,"adjMaxMagicAtk":378,"adjHit":23,"adjFinalDmg":0.04})
    }),
    52012433: _tools.RODict({
        "propID": 52012433,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":188,"adjMaxMagicAtk":411,"adjHit":24,"adjFinalDmg":0.04})
    }),
    52012434: _tools.RODict({
        "propID": 52012434,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":215,"adjMaxMagicAtk":471,"adjHit":27,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012435: _tools.RODict({
        "propID": 52012435,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":237,"adjMaxMagicAtk":517,"adjHit":29,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012436: _tools.RODict({
        "propID": 52012436,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":261,"adjMaxMagicAtk":570,"adjHit":32,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012437: _tools.RODict({
        "propID": 52012437,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":288,"adjMaxMagicAtk":629,"adjHit":38,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012438: _tools.RODict({
        "propID": 52012438,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":78,"adjMaxMagicAtk":169})
    }),
    52012439: _tools.RODict({
        "propID": 52012439,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":86,"adjMaxMagicAtk":186})
    }),
    52012440: _tools.RODict({
        "propID": 52012440,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":92,"adjMaxMagicAtk":203})
    }),
    52012441: _tools.RODict({
        "propID": 52012441,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":102,"adjMaxMagicAtk":221})
    }),
    52012442: _tools.RODict({
        "propID": 52012442,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":108,"adjMaxMagicAtk":236,"adjHit":17,"adjFinalDmg":0.02})
    }),
    52012443: _tools.RODict({
        "propID": 52012443,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":119,"adjMaxMagicAtk":260,"adjHit":18,"adjFinalDmg":0.02})
    }),
    52012444: _tools.RODict({
        "propID": 52012444,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":130,"adjMaxMagicAtk":285,"adjHit":19,"adjFinalDmg":0.02})
    }),
    52012445: _tools.RODict({
        "propID": 52012445,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":141,"adjMaxMagicAtk":307,"adjHit":20,"adjFinalDmg":0.02})
    }),
    52012446: _tools.RODict({
        "propID": 52012446,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":152,"adjMaxMagicAtk":331,"adjHit":21,"adjFinalDmg":0.04})
    }),
    52012447: _tools.RODict({
        "propID": 52012447,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":168,"adjMaxMagicAtk":365,"adjHit":22,"adjFinalDmg":0.04})
    }),
    52012448: _tools.RODict({
        "propID": 52012448,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":184,"adjMaxMagicAtk":397,"adjHit":24,"adjFinalDmg":0.04})
    }),
    52012449: _tools.RODict({
        "propID": 52012449,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":197,"adjMaxMagicAtk":432,"adjHit":25,"adjFinalDmg":0.04})
    }),
    52012450: _tools.RODict({
        "propID": 52012450,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":226,"adjMaxMagicAtk":495,"adjHit":28,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012451: _tools.RODict({
        "propID": 52012451,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":249,"adjMaxMagicAtk":543,"adjHit":30,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012452: _tools.RODict({
        "propID": 52012452,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":274,"adjMaxMagicAtk":599,"adjHit":34,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012453: _tools.RODict({
        "propID": 52012453,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":302,"adjMaxMagicAtk":660,"adjHit":40,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012454: _tools.RODict({
        "propID": 52012454,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":82,"adjMaxMagicAtk":177})
    }),
    52012455: _tools.RODict({
        "propID": 52012455,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":90,"adjMaxMagicAtk":195})
    }),
    52012456: _tools.RODict({
        "propID": 52012456,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":97,"adjMaxMagicAtk":213})
    }),
    52012457: _tools.RODict({
        "propID": 52012457,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":107,"adjMaxMagicAtk":232})
    }),
    52012458: _tools.RODict({
        "propID": 52012458,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":113,"adjMaxMagicAtk":248,"adjHit":18,"adjFinalDmg":0.02})
    }),
    52012459: _tools.RODict({
        "propID": 52012459,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":125,"adjMaxMagicAtk":273,"adjHit":19,"adjFinalDmg":0.02})
    }),
    52012460: _tools.RODict({
        "propID": 52012460,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":137,"adjMaxMagicAtk":299,"adjHit":20,"adjFinalDmg":0.02})
    }),
    52012461: _tools.RODict({
        "propID": 52012461,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":148,"adjMaxMagicAtk":322,"adjHit":21,"adjFinalDmg":0.02})
    }),
    52012462: _tools.RODict({
        "propID": 52012462,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":160,"adjMaxMagicAtk":348,"adjHit":22,"adjFinalDmg":0.04})
    }),
    52012463: _tools.RODict({
        "propID": 52012463,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":176,"adjMaxMagicAtk":383,"adjHit":23,"adjFinalDmg":0.04})
    }),
    52012464: _tools.RODict({
        "propID": 52012464,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":193,"adjMaxMagicAtk":417,"adjHit":25,"adjFinalDmg":0.04})
    }),
    52012465: _tools.RODict({
        "propID": 52012465,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":207,"adjMaxMagicAtk":454,"adjHit":26,"adjFinalDmg":0.04})
    }),
    52012466: _tools.RODict({
        "propID": 52012466,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":237,"adjMaxMagicAtk":520,"adjHit":29,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012467: _tools.RODict({
        "propID": 52012467,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":261,"adjMaxMagicAtk":570,"adjHit":32,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012468: _tools.RODict({
        "propID": 52012468,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":288,"adjMaxMagicAtk":629,"adjHit":36,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012469: _tools.RODict({
        "propID": 52012469,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":317,"adjMaxMagicAtk":693,"adjHit":42,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012470: _tools.RODict({
        "propID": 52012470,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":86,"adjMaxMagicAtk":186})
    }),
    52012471: _tools.RODict({
        "propID": 52012471,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":95,"adjMaxMagicAtk":205})
    }),
    52012472: _tools.RODict({
        "propID": 52012472,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":102,"adjMaxMagicAtk":224})
    }),
    52012473: _tools.RODict({
        "propID": 52012473,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":112,"adjMaxMagicAtk":244})
    }),
    52012474: _tools.RODict({
        "propID": 52012474,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":119,"adjMaxMagicAtk":260,"adjHit":19,"adjFinalDmg":0.02})
    }),
    52012475: _tools.RODict({
        "propID": 52012475,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":131,"adjMaxMagicAtk":287,"adjHit":20,"adjFinalDmg":0.02})
    }),
    52012476: _tools.RODict({
        "propID": 52012476,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":144,"adjMaxMagicAtk":314,"adjHit":21,"adjFinalDmg":0.02})
    }),
    52012477: _tools.RODict({
        "propID": 52012477,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":155,"adjMaxMagicAtk":338,"adjHit":22,"adjFinalDmg":0.02})
    }),
    52012478: _tools.RODict({
        "propID": 52012478,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":168,"adjMaxMagicAtk":365,"adjHit":23,"adjFinalDmg":0.04})
    }),
    52012479: _tools.RODict({
        "propID": 52012479,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":185,"adjMaxMagicAtk":402,"adjHit":24,"adjFinalDmg":0.04})
    }),
    52012480: _tools.RODict({
        "propID": 52012480,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":203,"adjMaxMagicAtk":438,"adjHit":26,"adjFinalDmg":0.04})
    }),
    52012481: _tools.RODict({
        "propID": 52012481,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":217,"adjMaxMagicAtk":477,"adjHit":27,"adjFinalDmg":0.04})
    }),
    52012482: _tools.RODict({
        "propID": 52012482,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":249,"adjMaxMagicAtk":546,"adjHit":30,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012483: _tools.RODict({
        "propID": 52012483,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":274,"adjMaxMagicAtk":599,"adjHit":34,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012484: _tools.RODict({
        "propID": 52012484,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":302,"adjMaxMagicAtk":660,"adjHit":38,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012485: _tools.RODict({
        "propID": 52012485,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":333,"adjMaxMagicAtk":728,"adjHit":44,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012486: _tools.RODict({
        "propID": 52012486,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":90,"adjMaxMagicAtk":195})
    }),
    52012487: _tools.RODict({
        "propID": 52012487,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":100,"adjMaxMagicAtk":215})
    }),
    52012488: _tools.RODict({
        "propID": 52012488,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":107,"adjMaxMagicAtk":235})
    }),
    52012489: _tools.RODict({
        "propID": 52012489,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":118,"adjMaxMagicAtk":256})
    }),
    52012490: _tools.RODict({
        "propID": 52012490,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":125,"adjMaxMagicAtk":273,"adjHit":20,"adjFinalDmg":0.02})
    }),
    52012491: _tools.RODict({
        "propID": 52012491,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":138,"adjMaxMagicAtk":301,"adjHit":21,"adjFinalDmg":0.02})
    }),
    52012492: _tools.RODict({
        "propID": 52012492,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":151,"adjMaxMagicAtk":330,"adjHit":22,"adjFinalDmg":0.02})
    }),
    52012493: _tools.RODict({
        "propID": 52012493,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":163,"adjMaxMagicAtk":355,"adjHit":23,"adjFinalDmg":0.02})
    }),
    52012494: _tools.RODict({
        "propID": 52012494,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":176,"adjMaxMagicAtk":383,"adjHit":24,"adjFinalDmg":0.04})
    }),
    52012495: _tools.RODict({
        "propID": 52012495,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":194,"adjMaxMagicAtk":422,"adjHit":25,"adjFinalDmg":0.04})
    }),
    52012496: _tools.RODict({
        "propID": 52012496,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":213,"adjMaxMagicAtk":460,"adjHit":27,"adjFinalDmg":0.04})
    }),
    52012497: _tools.RODict({
        "propID": 52012497,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":228,"adjMaxMagicAtk":501,"adjHit":28,"adjFinalDmg":0.04})
    }),
    52012498: _tools.RODict({
        "propID": 52012498,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":261,"adjMaxMagicAtk":573,"adjHit":32,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012499: _tools.RODict({
        "propID": 52012499,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":288,"adjMaxMagicAtk":629,"adjHit":36,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012500: _tools.RODict({
        "propID": 52012500,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":317,"adjMaxMagicAtk":693,"adjHit":40,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012501: _tools.RODict({
        "propID": 52012501,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":350,"adjMaxMagicAtk":764,"adjHit":46,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
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
    52012518: _tools.RODict({
        "propID": 52012518,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":58,"adjMaxPhysicalAtk":126})
    }),
    52012519: _tools.RODict({
        "propID": 52012519,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":64,"adjMaxPhysicalAtk":139})
    }),
    52012520: _tools.RODict({
        "propID": 52012520,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":69,"adjMaxPhysicalAtk":151})
    }),
    52012521: _tools.RODict({
        "propID": 52012521,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":76,"adjMaxPhysicalAtk":164})
    }),
    52012522: _tools.RODict({
        "propID": 52012522,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":81,"adjMaxPhysicalAtk":176,"adjHit":11,"adjFinalDmg":0.02})
    }),
    52012523: _tools.RODict({
        "propID": 52012523,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":89,"adjMaxPhysicalAtk":194,"adjHit":12,"adjFinalDmg":0.02})
    }),
    52012524: _tools.RODict({
        "propID": 52012524,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":97,"adjMaxPhysicalAtk":212,"adjHit":13,"adjFinalDmg":0.02})
    }),
    52012525: _tools.RODict({
        "propID": 52012525,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":105,"adjMaxPhysicalAtk":229,"adjHit":14,"adjFinalDmg":0.02})
    }),
    52012526: _tools.RODict({
        "propID": 52012526,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":113,"adjMaxPhysicalAtk":247,"adjHit":15,"adjFinalDmg":0.04})
    }),
    52012527: _tools.RODict({
        "propID": 52012527,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":125,"adjMaxPhysicalAtk":272,"adjHit":16,"adjFinalDmg":0.04})
    }),
    52012528: _tools.RODict({
        "propID": 52012528,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":137,"adjMaxPhysicalAtk":296,"adjHit":18,"adjFinalDmg":0.04})
    }),
    52012529: _tools.RODict({
        "propID": 52012529,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":147,"adjMaxPhysicalAtk":321,"adjHit":19,"adjFinalDmg":0.04})
    }),
    52012530: _tools.RODict({
        "propID": 52012530,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":169,"adjMaxPhysicalAtk":370,"adjHit":22,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012531: _tools.RODict({
        "propID": 52012531,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":186,"adjMaxPhysicalAtk":406,"adjHit":24,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012532: _tools.RODict({
        "propID": 52012532,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":205,"adjMaxPhysicalAtk":447,"adjHit":26,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012533: _tools.RODict({
        "propID": 52012533,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":226,"adjMaxPhysicalAtk":492,"adjHit":29,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012534: _tools.RODict({
        "propID": 52012534,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":61,"adjMaxPhysicalAtk":132})
    }),
    52012535: _tools.RODict({
        "propID": 52012535,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":67,"adjMaxPhysicalAtk":146})
    }),
    52012536: _tools.RODict({
        "propID": 52012536,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":72,"adjMaxPhysicalAtk":159})
    }),
    52012537: _tools.RODict({
        "propID": 52012537,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":80,"adjMaxPhysicalAtk":172})
    }),
    52012538: _tools.RODict({
        "propID": 52012538,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":85,"adjMaxPhysicalAtk":185,"adjHit":12,"adjFinalDmg":0.02})
    }),
    52012539: _tools.RODict({
        "propID": 52012539,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":93,"adjMaxPhysicalAtk":204,"adjHit":13,"adjFinalDmg":0.02})
    }),
    52012540: _tools.RODict({
        "propID": 52012540,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":102,"adjMaxPhysicalAtk":223,"adjHit":14,"adjFinalDmg":0.02})
    }),
    52012541: _tools.RODict({
        "propID": 52012541,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":110,"adjMaxPhysicalAtk":240,"adjHit":15,"adjFinalDmg":0.02})
    }),
    52012542: _tools.RODict({
        "propID": 52012542,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":119,"adjMaxPhysicalAtk":259,"adjHit":16,"adjFinalDmg":0.04})
    }),
    52012543: _tools.RODict({
        "propID": 52012543,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":131,"adjMaxPhysicalAtk":286,"adjHit":17,"adjFinalDmg":0.04})
    }),
    52012544: _tools.RODict({
        "propID": 52012544,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":144,"adjMaxPhysicalAtk":311,"adjHit":19,"adjFinalDmg":0.04})
    }),
    52012545: _tools.RODict({
        "propID": 52012545,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":154,"adjMaxPhysicalAtk":337,"adjHit":20,"adjFinalDmg":0.04})
    }),
    52012546: _tools.RODict({
        "propID": 52012546,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":177,"adjMaxPhysicalAtk":389,"adjHit":23,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012547: _tools.RODict({
        "propID": 52012547,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":195,"adjMaxPhysicalAtk":426,"adjHit":25,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012548: _tools.RODict({
        "propID": 52012548,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":215,"adjMaxPhysicalAtk":469,"adjHit":27,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012549: _tools.RODict({
        "propID": 52012549,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":237,"adjMaxPhysicalAtk":517,"adjHit":30,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012550: _tools.RODict({
        "propID": 52012550,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":64,"adjMaxPhysicalAtk":139})
    }),
    52012551: _tools.RODict({
        "propID": 52012551,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":70,"adjMaxPhysicalAtk":153})
    }),
    52012552: _tools.RODict({
        "propID": 52012552,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":76,"adjMaxPhysicalAtk":167})
    }),
    52012553: _tools.RODict({
        "propID": 52012553,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":84,"adjMaxPhysicalAtk":181})
    }),
    52012554: _tools.RODict({
        "propID": 52012554,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":89,"adjMaxPhysicalAtk":194,"adjHit":13,"adjFinalDmg":0.02})
    }),
    52012555: _tools.RODict({
        "propID": 52012555,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":98,"adjMaxPhysicalAtk":214,"adjHit":14,"adjFinalDmg":0.02})
    }),
    52012556: _tools.RODict({
        "propID": 52012556,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":107,"adjMaxPhysicalAtk":234,"adjHit":15,"adjFinalDmg":0.02})
    }),
    52012557: _tools.RODict({
        "propID": 52012557,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":116,"adjMaxPhysicalAtk":252,"adjHit":16,"adjFinalDmg":0.02})
    }),
    52012558: _tools.RODict({
        "propID": 52012558,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":125,"adjMaxPhysicalAtk":272,"adjHit":17,"adjFinalDmg":0.04})
    }),
    52012559: _tools.RODict({
        "propID": 52012559,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":138,"adjMaxPhysicalAtk":300,"adjHit":18,"adjFinalDmg":0.04})
    }),
    52012560: _tools.RODict({
        "propID": 52012560,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":151,"adjMaxPhysicalAtk":327,"adjHit":20,"adjFinalDmg":0.04})
    }),
    52012561: _tools.RODict({
        "propID": 52012561,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":162,"adjMaxPhysicalAtk":354,"adjHit":21,"adjFinalDmg":0.04})
    }),
    52012562: _tools.RODict({
        "propID": 52012562,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":186,"adjMaxPhysicalAtk":408,"adjHit":24,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012563: _tools.RODict({
        "propID": 52012563,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":205,"adjMaxPhysicalAtk":447,"adjHit":26,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012564: _tools.RODict({
        "propID": 52012564,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":226,"adjMaxPhysicalAtk":492,"adjHit":28,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012565: _tools.RODict({
        "propID": 52012565,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":249,"adjMaxPhysicalAtk":543,"adjHit":32,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012566: _tools.RODict({
        "propID": 52012566,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":67,"adjMaxPhysicalAtk":146})
    }),
    52012567: _tools.RODict({
        "propID": 52012567,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":74,"adjMaxPhysicalAtk":161})
    }),
    52012568: _tools.RODict({
        "propID": 52012568,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":80,"adjMaxPhysicalAtk":175})
    }),
    52012569: _tools.RODict({
        "propID": 52012569,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":88,"adjMaxPhysicalAtk":190})
    }),
    52012570: _tools.RODict({
        "propID": 52012570,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":93,"adjMaxPhysicalAtk":204,"adjHit":14,"adjFinalDmg":0.02})
    }),
    52012571: _tools.RODict({
        "propID": 52012571,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":103,"adjMaxPhysicalAtk":225,"adjHit":15,"adjFinalDmg":0.02})
    }),
    52012572: _tools.RODict({
        "propID": 52012572,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":112,"adjMaxPhysicalAtk":246,"adjHit":16,"adjFinalDmg":0.02})
    }),
    52012573: _tools.RODict({
        "propID": 52012573,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":122,"adjMaxPhysicalAtk":265,"adjHit":17,"adjFinalDmg":0.02})
    }),
    52012574: _tools.RODict({
        "propID": 52012574,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":131,"adjMaxPhysicalAtk":286,"adjHit":18,"adjFinalDmg":0.04})
    }),
    52012575: _tools.RODict({
        "propID": 52012575,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":145,"adjMaxPhysicalAtk":315,"adjHit":19,"adjFinalDmg":0.04})
    }),
    52012576: _tools.RODict({
        "propID": 52012576,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":159,"adjMaxPhysicalAtk":343,"adjHit":21,"adjFinalDmg":0.04})
    }),
    52012577: _tools.RODict({
        "propID": 52012577,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":170,"adjMaxPhysicalAtk":372,"adjHit":22,"adjFinalDmg":0.04})
    }),
    52012578: _tools.RODict({
        "propID": 52012578,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":195,"adjMaxPhysicalAtk":428,"adjHit":25,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012579: _tools.RODict({
        "propID": 52012579,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":215,"adjMaxPhysicalAtk":469,"adjHit":27,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012580: _tools.RODict({
        "propID": 52012580,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":237,"adjMaxPhysicalAtk":517,"adjHit":29,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012581: _tools.RODict({
        "propID": 52012581,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":261,"adjMaxPhysicalAtk":570,"adjHit":34,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012582: _tools.RODict({
        "propID": 52012582,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":70,"adjMaxPhysicalAtk":153})
    }),
    52012583: _tools.RODict({
        "propID": 52012583,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":78,"adjMaxPhysicalAtk":169})
    }),
    52012584: _tools.RODict({
        "propID": 52012584,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":84,"adjMaxPhysicalAtk":184})
    }),
    52012585: _tools.RODict({
        "propID": 52012585,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":92,"adjMaxPhysicalAtk":200})
    }),
    52012586: _tools.RODict({
        "propID": 52012586,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":98,"adjMaxPhysicalAtk":214,"adjHit":15,"adjFinalDmg":0.02})
    }),
    52012587: _tools.RODict({
        "propID": 52012587,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":108,"adjMaxPhysicalAtk":236,"adjHit":16,"adjFinalDmg":0.02})
    }),
    52012588: _tools.RODict({
        "propID": 52012588,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":118,"adjMaxPhysicalAtk":258,"adjHit":17,"adjFinalDmg":0.02})
    }),
    52012589: _tools.RODict({
        "propID": 52012589,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":128,"adjMaxPhysicalAtk":278,"adjHit":18,"adjFinalDmg":0.02})
    }),
    52012590: _tools.RODict({
        "propID": 52012590,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":138,"adjMaxPhysicalAtk":300,"adjHit":19,"adjFinalDmg":0.04})
    }),
    52012591: _tools.RODict({
        "propID": 52012591,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":152,"adjMaxPhysicalAtk":331,"adjHit":20,"adjFinalDmg":0.04})
    }),
    52012592: _tools.RODict({
        "propID": 52012592,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":167,"adjMaxPhysicalAtk":360,"adjHit":22,"adjFinalDmg":0.04})
    }),
    52012593: _tools.RODict({
        "propID": 52012593,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":179,"adjMaxPhysicalAtk":391,"adjHit":23,"adjFinalDmg":0.04})
    }),
    52012594: _tools.RODict({
        "propID": 52012594,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":205,"adjMaxPhysicalAtk":449,"adjHit":26,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012595: _tools.RODict({
        "propID": 52012595,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":226,"adjMaxPhysicalAtk":492,"adjHit":28,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012596: _tools.RODict({
        "propID": 52012596,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":249,"adjMaxPhysicalAtk":543,"adjHit":30,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012597: _tools.RODict({
        "propID": 52012597,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":274,"adjMaxPhysicalAtk":599,"adjHit":36,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012598: _tools.RODict({
        "propID": 52012598,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":74,"adjMaxPhysicalAtk":161})
    }),
    52012599: _tools.RODict({
        "propID": 52012599,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":82,"adjMaxPhysicalAtk":177})
    }),
    52012600: _tools.RODict({
        "propID": 52012600,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":88,"adjMaxPhysicalAtk":193})
    }),
    52012601: _tools.RODict({
        "propID": 52012601,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":97,"adjMaxPhysicalAtk":210})
    }),
    52012602: _tools.RODict({
        "propID": 52012602,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":103,"adjMaxPhysicalAtk":225,"adjHit":16,"adjFinalDmg":0.02})
    }),
    52012603: _tools.RODict({
        "propID": 52012603,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":113,"adjMaxPhysicalAtk":248,"adjHit":17,"adjFinalDmg":0.02})
    }),
    52012604: _tools.RODict({
        "propID": 52012604,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":124,"adjMaxPhysicalAtk":271,"adjHit":18,"adjFinalDmg":0.02})
    }),
    52012605: _tools.RODict({
        "propID": 52012605,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":134,"adjMaxPhysicalAtk":292,"adjHit":19,"adjFinalDmg":0.02})
    }),
    52012606: _tools.RODict({
        "propID": 52012606,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":145,"adjMaxPhysicalAtk":315,"adjHit":20,"adjFinalDmg":0.04})
    }),
    52012607: _tools.RODict({
        "propID": 52012607,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":160,"adjMaxPhysicalAtk":348,"adjHit":21,"adjFinalDmg":0.04})
    }),
    52012608: _tools.RODict({
        "propID": 52012608,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":175,"adjMaxPhysicalAtk":378,"adjHit":23,"adjFinalDmg":0.04})
    }),
    52012609: _tools.RODict({
        "propID": 52012609,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":188,"adjMaxPhysicalAtk":411,"adjHit":24,"adjFinalDmg":0.04})
    }),
    52012610: _tools.RODict({
        "propID": 52012610,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":215,"adjMaxPhysicalAtk":471,"adjHit":27,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012611: _tools.RODict({
        "propID": 52012611,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":237,"adjMaxPhysicalAtk":517,"adjHit":29,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012612: _tools.RODict({
        "propID": 52012612,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":261,"adjMaxPhysicalAtk":570,"adjHit":32,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012613: _tools.RODict({
        "propID": 52012613,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":288,"adjMaxPhysicalAtk":629,"adjHit":38,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012614: _tools.RODict({
        "propID": 52012614,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":78,"adjMaxPhysicalAtk":169})
    }),
    52012615: _tools.RODict({
        "propID": 52012615,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":86,"adjMaxPhysicalAtk":186})
    }),
    52012616: _tools.RODict({
        "propID": 52012616,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":92,"adjMaxPhysicalAtk":203})
    }),
    52012617: _tools.RODict({
        "propID": 52012617,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":102,"adjMaxPhysicalAtk":221})
    }),
    52012618: _tools.RODict({
        "propID": 52012618,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":108,"adjMaxPhysicalAtk":236,"adjHit":17,"adjFinalDmg":0.02})
    }),
    52012619: _tools.RODict({
        "propID": 52012619,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":119,"adjMaxPhysicalAtk":260,"adjHit":18,"adjFinalDmg":0.02})
    }),
    52012620: _tools.RODict({
        "propID": 52012620,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":130,"adjMaxPhysicalAtk":285,"adjHit":19,"adjFinalDmg":0.02})
    }),
    52012621: _tools.RODict({
        "propID": 52012621,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":141,"adjMaxPhysicalAtk":307,"adjHit":20,"adjFinalDmg":0.02})
    }),
    52012622: _tools.RODict({
        "propID": 52012622,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":152,"adjMaxPhysicalAtk":331,"adjHit":21,"adjFinalDmg":0.04})
    }),
    52012623: _tools.RODict({
        "propID": 52012623,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":168,"adjMaxPhysicalAtk":365,"adjHit":22,"adjFinalDmg":0.04})
    }),
    52012624: _tools.RODict({
        "propID": 52012624,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":184,"adjMaxPhysicalAtk":397,"adjHit":24,"adjFinalDmg":0.04})
    }),
    52012625: _tools.RODict({
        "propID": 52012625,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":197,"adjMaxPhysicalAtk":432,"adjHit":25,"adjFinalDmg":0.04})
    }),
    52012626: _tools.RODict({
        "propID": 52012626,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":226,"adjMaxPhysicalAtk":495,"adjHit":28,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012627: _tools.RODict({
        "propID": 52012627,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":249,"adjMaxPhysicalAtk":543,"adjHit":30,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012628: _tools.RODict({
        "propID": 52012628,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":274,"adjMaxPhysicalAtk":599,"adjHit":34,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012629: _tools.RODict({
        "propID": 52012629,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":302,"adjMaxPhysicalAtk":660,"adjHit":40,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012630: _tools.RODict({
        "propID": 52012630,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":82,"adjMaxPhysicalAtk":177})
    }),
    52012631: _tools.RODict({
        "propID": 52012631,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":90,"adjMaxPhysicalAtk":195})
    }),
    52012632: _tools.RODict({
        "propID": 52012632,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":97,"adjMaxPhysicalAtk":213})
    }),
    52012633: _tools.RODict({
        "propID": 52012633,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":107,"adjMaxPhysicalAtk":232})
    }),
    52012634: _tools.RODict({
        "propID": 52012634,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":113,"adjMaxPhysicalAtk":248,"adjHit":18,"adjFinalDmg":0.02})
    }),
    52012635: _tools.RODict({
        "propID": 52012635,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":125,"adjMaxPhysicalAtk":273,"adjHit":19,"adjFinalDmg":0.02})
    }),
    52012636: _tools.RODict({
        "propID": 52012636,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":137,"adjMaxPhysicalAtk":299,"adjHit":20,"adjFinalDmg":0.02})
    }),
    52012637: _tools.RODict({
        "propID": 52012637,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":148,"adjMaxPhysicalAtk":322,"adjHit":21,"adjFinalDmg":0.02})
    }),
    52012638: _tools.RODict({
        "propID": 52012638,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":160,"adjMaxPhysicalAtk":348,"adjHit":22,"adjFinalDmg":0.04})
    }),
    52012639: _tools.RODict({
        "propID": 52012639,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":176,"adjMaxPhysicalAtk":383,"adjHit":23,"adjFinalDmg":0.04})
    }),
    52012640: _tools.RODict({
        "propID": 52012640,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":193,"adjMaxPhysicalAtk":417,"adjHit":25,"adjFinalDmg":0.04})
    }),
    52012641: _tools.RODict({
        "propID": 52012641,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":207,"adjMaxPhysicalAtk":454,"adjHit":26,"adjFinalDmg":0.04})
    }),
    52012642: _tools.RODict({
        "propID": 52012642,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":237,"adjMaxPhysicalAtk":520,"adjHit":29,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012643: _tools.RODict({
        "propID": 52012643,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":261,"adjMaxPhysicalAtk":570,"adjHit":32,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012644: _tools.RODict({
        "propID": 52012644,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":288,"adjMaxPhysicalAtk":629,"adjHit":36,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012645: _tools.RODict({
        "propID": 52012645,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":317,"adjMaxPhysicalAtk":693,"adjHit":42,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012646: _tools.RODict({
        "propID": 52012646,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":86,"adjMaxPhysicalAtk":186})
    }),
    52012647: _tools.RODict({
        "propID": 52012647,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":95,"adjMaxPhysicalAtk":205})
    }),
    52012648: _tools.RODict({
        "propID": 52012648,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":102,"adjMaxPhysicalAtk":224})
    }),
    52012649: _tools.RODict({
        "propID": 52012649,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":112,"adjMaxPhysicalAtk":244})
    }),
    52012650: _tools.RODict({
        "propID": 52012650,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":119,"adjMaxPhysicalAtk":260,"adjHit":19,"adjFinalDmg":0.02})
    }),
    52012651: _tools.RODict({
        "propID": 52012651,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":131,"adjMaxPhysicalAtk":287,"adjHit":20,"adjFinalDmg":0.02})
    }),
    52012652: _tools.RODict({
        "propID": 52012652,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":144,"adjMaxPhysicalAtk":314,"adjHit":21,"adjFinalDmg":0.02})
    }),
    52012653: _tools.RODict({
        "propID": 52012653,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":155,"adjMaxPhysicalAtk":338,"adjHit":22,"adjFinalDmg":0.02})
    }),
    52012654: _tools.RODict({
        "propID": 52012654,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":168,"adjMaxPhysicalAtk":365,"adjHit":23,"adjFinalDmg":0.04})
    }),
    52012655: _tools.RODict({
        "propID": 52012655,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":185,"adjMaxPhysicalAtk":402,"adjHit":24,"adjFinalDmg":0.04})
    }),
    52012656: _tools.RODict({
        "propID": 52012656,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":203,"adjMaxPhysicalAtk":438,"adjHit":26,"adjFinalDmg":0.04})
    }),
    52012657: _tools.RODict({
        "propID": 52012657,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":217,"adjMaxPhysicalAtk":477,"adjHit":27,"adjFinalDmg":0.04})
    }),
    52012658: _tools.RODict({
        "propID": 52012658,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":249,"adjMaxPhysicalAtk":546,"adjHit":30,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012659: _tools.RODict({
        "propID": 52012659,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":274,"adjMaxPhysicalAtk":599,"adjHit":34,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012660: _tools.RODict({
        "propID": 52012660,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":302,"adjMaxPhysicalAtk":660,"adjHit":38,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012661: _tools.RODict({
        "propID": 52012661,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":333,"adjMaxPhysicalAtk":728,"adjHit":44,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012662: _tools.RODict({
        "propID": 52012662,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":90,"adjMaxPhysicalAtk":195})
    }),
    52012663: _tools.RODict({
        "propID": 52012663,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":100,"adjMaxPhysicalAtk":215})
    }),
    52012664: _tools.RODict({
        "propID": 52012664,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":107,"adjMaxPhysicalAtk":235})
    }),
    52012665: _tools.RODict({
        "propID": 52012665,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":118,"adjMaxPhysicalAtk":256})
    }),
    52012666: _tools.RODict({
        "propID": 52012666,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":125,"adjMaxPhysicalAtk":273,"adjHit":20,"adjFinalDmg":0.02})
    }),
    52012667: _tools.RODict({
        "propID": 52012667,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":138,"adjMaxPhysicalAtk":301,"adjHit":21,"adjFinalDmg":0.02})
    }),
    52012668: _tools.RODict({
        "propID": 52012668,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":151,"adjMaxPhysicalAtk":330,"adjHit":22,"adjFinalDmg":0.02})
    }),
    52012669: _tools.RODict({
        "propID": 52012669,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":163,"adjMaxPhysicalAtk":355,"adjHit":23,"adjFinalDmg":0.02})
    }),
    52012670: _tools.RODict({
        "propID": 52012670,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":176,"adjMaxPhysicalAtk":383,"adjHit":24,"adjFinalDmg":0.04})
    }),
    52012671: _tools.RODict({
        "propID": 52012671,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":194,"adjMaxPhysicalAtk":422,"adjHit":25,"adjFinalDmg":0.04})
    }),
    52012672: _tools.RODict({
        "propID": 52012672,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":213,"adjMaxPhysicalAtk":460,"adjHit":27,"adjFinalDmg":0.04})
    }),
    52012673: _tools.RODict({
        "propID": 52012673,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":228,"adjMaxPhysicalAtk":501,"adjHit":28,"adjFinalDmg":0.04})
    }),
    52012674: _tools.RODict({
        "propID": 52012674,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":261,"adjMaxPhysicalAtk":573,"adjHit":32,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012675: _tools.RODict({
        "propID": 52012675,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":288,"adjMaxPhysicalAtk":629,"adjHit":36,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012676: _tools.RODict({
        "propID": 52012676,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":317,"adjMaxPhysicalAtk":693,"adjHit":40,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012677: _tools.RODict({
        "propID": 52012677,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":350,"adjMaxPhysicalAtk":764,"adjHit":46,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52012678: _tools.RODict({
        "propID": 52012678,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":65,"adjMaxPhysicalArmor":98,"adjMinMagicArmor":65,"adjMaxMagicArmor":98})
    }),
    52012679: _tools.RODict({
        "propID": 52012679,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":72,"adjMaxPhysicalArmor":108,"adjMinMagicArmor":72,"adjMaxMagicArmor":108})
    }),
    52012680: _tools.RODict({
        "propID": 52012680,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":78,"adjMaxPhysicalArmor":118,"adjMinMagicArmor":78,"adjMaxMagicArmor":118})
    }),
    52012681: _tools.RODict({
        "propID": 52012681,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":85,"adjMaxPhysicalArmor":127,"adjMinMagicArmor":85,"adjMaxMagicArmor":127})
    }),
    52012682: _tools.RODict({
        "propID": 52012682,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":91,"adjMaxPhysicalArmor":137,"adjMinMagicArmor":91,"adjMaxMagicArmor":137,"adjMortal":0.05})
    }),
    52012683: _tools.RODict({
        "propID": 52012683,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":100,"adjMaxPhysicalArmor":151,"adjMinMagicArmor":100,"adjMaxMagicArmor":151,"adjMortal":0.05})
    }),
    52012684: _tools.RODict({
        "propID": 52012684,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":109,"adjMaxPhysicalArmor":164,"adjMinMagicArmor":109,"adjMaxMagicArmor":164,"adjMortal":0.05})
    }),
    52012685: _tools.RODict({
        "propID": 52012685,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":118,"adjMaxPhysicalArmor":178,"adjMinMagicArmor":118,"adjMaxMagicArmor":178,"adjMortal":0.05})
    }),
    52012686: _tools.RODict({
        "propID": 52012686,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":127,"adjMaxPhysicalArmor":192,"adjMinMagicArmor":127,"adjMaxMagicArmor":192,"adjMortal":0.1})
    }),
    52012687: _tools.RODict({
        "propID": 52012687,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":140,"adjMaxPhysicalArmor":211,"adjMinMagicArmor":140,"adjMaxMagicArmor":211,"adjMortal":0.1})
    }),
    52012688: _tools.RODict({
        "propID": 52012688,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":152,"adjMaxPhysicalArmor":230,"adjMinMagicArmor":152,"adjMaxMagicArmor":230,"adjMortal":0.1})
    }),
    52012689: _tools.RODict({
        "propID": 52012689,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":165,"adjMaxPhysicalArmor":250,"adjMinMagicArmor":165,"adjMaxMagicArmor":250,"adjMortal":0.1})
    }),
    52012690: _tools.RODict({
        "propID": 52012690,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":190,"adjMaxPhysicalArmor":288,"adjMinMagicArmor":190,"adjMaxMagicArmor":288,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012691: _tools.RODict({
        "propID": 52012691,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":209,"adjMaxPhysicalArmor":317,"adjMinMagicArmor":209,"adjMaxMagicArmor":317,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012692: _tools.RODict({
        "propID": 52012692,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":230,"adjMaxPhysicalArmor":349,"adjMinMagicArmor":230,"adjMaxMagicArmor":349,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012693: _tools.RODict({
        "propID": 52012693,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":253,"adjMaxPhysicalArmor":384,"adjMinMagicArmor":253,"adjMaxMagicArmor":384,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012694: _tools.RODict({
        "propID": 52012694,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":68,"adjMaxPhysicalArmor":103,"adjMinMagicArmor":68,"adjMaxMagicArmor":103})
    }),
    52012695: _tools.RODict({
        "propID": 52012695,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":76,"adjMaxPhysicalArmor":113,"adjMinMagicArmor":76,"adjMaxMagicArmor":113})
    }),
    52012696: _tools.RODict({
        "propID": 52012696,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":82,"adjMaxPhysicalArmor":124,"adjMinMagicArmor":82,"adjMaxMagicArmor":124})
    }),
    52012697: _tools.RODict({
        "propID": 52012697,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":89,"adjMaxPhysicalArmor":133,"adjMinMagicArmor":89,"adjMaxMagicArmor":133})
    }),
    52012698: _tools.RODict({
        "propID": 52012698,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":96,"adjMaxPhysicalArmor":144,"adjMinMagicArmor":96,"adjMaxMagicArmor":144,"adjMortal":0.05})
    }),
    52012699: _tools.RODict({
        "propID": 52012699,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":105,"adjMaxPhysicalArmor":159,"adjMinMagicArmor":105,"adjMaxMagicArmor":159,"adjMortal":0.05})
    }),
    52012700: _tools.RODict({
        "propID": 52012700,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":114,"adjMaxPhysicalArmor":172,"adjMinMagicArmor":114,"adjMaxMagicArmor":172,"adjMortal":0.05})
    }),
    52012701: _tools.RODict({
        "propID": 52012701,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":124,"adjMaxPhysicalArmor":187,"adjMinMagicArmor":124,"adjMaxMagicArmor":187,"adjMortal":0.05})
    }),
    52012702: _tools.RODict({
        "propID": 52012702,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":133,"adjMaxPhysicalArmor":202,"adjMinMagicArmor":133,"adjMaxMagicArmor":202,"adjMortal":0.1})
    }),
    52012703: _tools.RODict({
        "propID": 52012703,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":147,"adjMaxPhysicalArmor":222,"adjMinMagicArmor":147,"adjMaxMagicArmor":222,"adjMortal":0.1})
    }),
    52012704: _tools.RODict({
        "propID": 52012704,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":160,"adjMaxPhysicalArmor":242,"adjMinMagicArmor":160,"adjMaxMagicArmor":242,"adjMortal":0.1})
    }),
    52012705: _tools.RODict({
        "propID": 52012705,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":173,"adjMaxPhysicalArmor":263,"adjMinMagicArmor":173,"adjMaxMagicArmor":263,"adjMortal":0.1})
    }),
    52012706: _tools.RODict({
        "propID": 52012706,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":200,"adjMaxPhysicalArmor":302,"adjMinMagicArmor":200,"adjMaxMagicArmor":302,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012707: _tools.RODict({
        "propID": 52012707,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":219,"adjMaxPhysicalArmor":333,"adjMinMagicArmor":219,"adjMaxMagicArmor":333,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012708: _tools.RODict({
        "propID": 52012708,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":242,"adjMaxPhysicalArmor":366,"adjMinMagicArmor":242,"adjMaxMagicArmor":366,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012709: _tools.RODict({
        "propID": 52012709,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":266,"adjMaxPhysicalArmor":403,"adjMinMagicArmor":266,"adjMaxMagicArmor":403,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012710: _tools.RODict({
        "propID": 52012710,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":71,"adjMaxPhysicalArmor":108,"adjMinMagicArmor":71,"adjMaxMagicArmor":108})
    }),
    52012711: _tools.RODict({
        "propID": 52012711,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":80,"adjMaxPhysicalArmor":119,"adjMinMagicArmor":80,"adjMaxMagicArmor":119})
    }),
    52012712: _tools.RODict({
        "propID": 52012712,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":86,"adjMaxPhysicalArmor":130,"adjMinMagicArmor":86,"adjMaxMagicArmor":130})
    }),
    52012713: _tools.RODict({
        "propID": 52012713,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":93,"adjMaxPhysicalArmor":140,"adjMinMagicArmor":93,"adjMaxMagicArmor":140})
    }),
    52012714: _tools.RODict({
        "propID": 52012714,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":101,"adjMaxPhysicalArmor":151,"adjMinMagicArmor":101,"adjMaxMagicArmor":151,"adjMortal":0.05})
    }),
    52012715: _tools.RODict({
        "propID": 52012715,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":110,"adjMaxPhysicalArmor":167,"adjMinMagicArmor":110,"adjMaxMagicArmor":167,"adjMortal":0.05})
    }),
    52012716: _tools.RODict({
        "propID": 52012716,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":120,"adjMaxPhysicalArmor":181,"adjMinMagicArmor":120,"adjMaxMagicArmor":181,"adjMortal":0.05})
    }),
    52012717: _tools.RODict({
        "propID": 52012717,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":130,"adjMaxPhysicalArmor":196,"adjMinMagicArmor":130,"adjMaxMagicArmor":196,"adjMortal":0.05})
    }),
    52012718: _tools.RODict({
        "propID": 52012718,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":140,"adjMaxPhysicalArmor":212,"adjMinMagicArmor":140,"adjMaxMagicArmor":212,"adjMortal":0.1})
    }),
    52012719: _tools.RODict({
        "propID": 52012719,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":154,"adjMaxPhysicalArmor":233,"adjMinMagicArmor":154,"adjMaxMagicArmor":233,"adjMortal":0.1})
    }),
    52012720: _tools.RODict({
        "propID": 52012720,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":168,"adjMaxPhysicalArmor":254,"adjMinMagicArmor":168,"adjMaxMagicArmor":254,"adjMortal":0.1})
    }),
    52012721: _tools.RODict({
        "propID": 52012721,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":182,"adjMaxPhysicalArmor":276,"adjMinMagicArmor":182,"adjMaxMagicArmor":276,"adjMortal":0.1})
    }),
    52012722: _tools.RODict({
        "propID": 52012722,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":210,"adjMaxPhysicalArmor":317,"adjMinMagicArmor":210,"adjMaxMagicArmor":317,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012723: _tools.RODict({
        "propID": 52012723,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":230,"adjMaxPhysicalArmor":350,"adjMinMagicArmor":230,"adjMaxMagicArmor":350,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012724: _tools.RODict({
        "propID": 52012724,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":254,"adjMaxPhysicalArmor":384,"adjMinMagicArmor":254,"adjMaxMagicArmor":384,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012725: _tools.RODict({
        "propID": 52012725,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":279,"adjMaxPhysicalArmor":423,"adjMinMagicArmor":279,"adjMaxMagicArmor":423,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012726: _tools.RODict({
        "propID": 52012726,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":75,"adjMaxPhysicalArmor":113,"adjMinMagicArmor":75,"adjMaxMagicArmor":113})
    }),
    52012727: _tools.RODict({
        "propID": 52012727,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":84,"adjMaxPhysicalArmor":125,"adjMinMagicArmor":84,"adjMaxMagicArmor":125})
    }),
    52012728: _tools.RODict({
        "propID": 52012728,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":90,"adjMaxPhysicalArmor":137,"adjMinMagicArmor":90,"adjMaxMagicArmor":137})
    }),
    52012729: _tools.RODict({
        "propID": 52012729,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":98,"adjMaxPhysicalArmor":147,"adjMinMagicArmor":98,"adjMaxMagicArmor":147})
    }),
    52012730: _tools.RODict({
        "propID": 52012730,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":106,"adjMaxPhysicalArmor":159,"adjMinMagicArmor":106,"adjMaxMagicArmor":159,"adjMortal":0.05})
    }),
    52012731: _tools.RODict({
        "propID": 52012731,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":116,"adjMaxPhysicalArmor":175,"adjMinMagicArmor":116,"adjMaxMagicArmor":175,"adjMortal":0.05})
    }),
    52012732: _tools.RODict({
        "propID": 52012732,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":126,"adjMaxPhysicalArmor":190,"adjMinMagicArmor":126,"adjMaxMagicArmor":190,"adjMortal":0.05})
    }),
    52012733: _tools.RODict({
        "propID": 52012733,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":137,"adjMaxPhysicalArmor":206,"adjMinMagicArmor":137,"adjMaxMagicArmor":206,"adjMortal":0.05})
    }),
    52012734: _tools.RODict({
        "propID": 52012734,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":147,"adjMaxPhysicalArmor":223,"adjMinMagicArmor":147,"adjMaxMagicArmor":223,"adjMortal":0.1})
    }),
    52012735: _tools.RODict({
        "propID": 52012735,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":162,"adjMaxPhysicalArmor":245,"adjMinMagicArmor":162,"adjMaxMagicArmor":245,"adjMortal":0.1})
    }),
    52012736: _tools.RODict({
        "propID": 52012736,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":176,"adjMaxPhysicalArmor":267,"adjMinMagicArmor":176,"adjMaxMagicArmor":267,"adjMortal":0.1})
    }),
    52012737: _tools.RODict({
        "propID": 52012737,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":191,"adjMaxPhysicalArmor":290,"adjMinMagicArmor":191,"adjMaxMagicArmor":290,"adjMortal":0.1})
    }),
    52012738: _tools.RODict({
        "propID": 52012738,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":221,"adjMaxPhysicalArmor":333,"adjMinMagicArmor":221,"adjMaxMagicArmor":333,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012739: _tools.RODict({
        "propID": 52012739,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":242,"adjMaxPhysicalArmor":368,"adjMinMagicArmor":242,"adjMaxMagicArmor":368,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012740: _tools.RODict({
        "propID": 52012740,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":267,"adjMaxPhysicalArmor":403,"adjMinMagicArmor":267,"adjMaxMagicArmor":403,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012741: _tools.RODict({
        "propID": 52012741,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":293,"adjMaxPhysicalArmor":444,"adjMinMagicArmor":293,"adjMaxMagicArmor":444,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012742: _tools.RODict({
        "propID": 52012742,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":79,"adjMaxPhysicalArmor":119,"adjMinMagicArmor":79,"adjMaxMagicArmor":119})
    }),
    52012743: _tools.RODict({
        "propID": 52012743,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":88,"adjMaxPhysicalArmor":131,"adjMinMagicArmor":88,"adjMaxMagicArmor":131})
    }),
    52012744: _tools.RODict({
        "propID": 52012744,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":95,"adjMaxPhysicalArmor":144,"adjMinMagicArmor":95,"adjMaxMagicArmor":144})
    }),
    52012745: _tools.RODict({
        "propID": 52012745,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":103,"adjMaxPhysicalArmor":154,"adjMinMagicArmor":103,"adjMaxMagicArmor":154})
    }),
    52012746: _tools.RODict({
        "propID": 52012746,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":111,"adjMaxPhysicalArmor":167,"adjMinMagicArmor":111,"adjMaxMagicArmor":167,"adjMortal":0.05})
    }),
    52012747: _tools.RODict({
        "propID": 52012747,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":122,"adjMaxPhysicalArmor":184,"adjMinMagicArmor":122,"adjMaxMagicArmor":184,"adjMortal":0.05})
    }),
    52012748: _tools.RODict({
        "propID": 52012748,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":132,"adjMaxPhysicalArmor":200,"adjMinMagicArmor":132,"adjMaxMagicArmor":200,"adjMortal":0.05})
    }),
    52012749: _tools.RODict({
        "propID": 52012749,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":144,"adjMaxPhysicalArmor":216,"adjMinMagicArmor":144,"adjMaxMagicArmor":216,"adjMortal":0.05})
    }),
    52012750: _tools.RODict({
        "propID": 52012750,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":154,"adjMaxPhysicalArmor":234,"adjMinMagicArmor":154,"adjMaxMagicArmor":234,"adjMortal":0.1})
    }),
    52012751: _tools.RODict({
        "propID": 52012751,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":170,"adjMaxPhysicalArmor":257,"adjMinMagicArmor":170,"adjMaxMagicArmor":257,"adjMortal":0.1})
    }),
    52012752: _tools.RODict({
        "propID": 52012752,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":185,"adjMaxPhysicalArmor":280,"adjMinMagicArmor":185,"adjMaxMagicArmor":280,"adjMortal":0.1})
    }),
    52012753: _tools.RODict({
        "propID": 52012753,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":201,"adjMaxPhysicalArmor":305,"adjMinMagicArmor":201,"adjMaxMagicArmor":305,"adjMortal":0.1})
    }),
    52012754: _tools.RODict({
        "propID": 52012754,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":232,"adjMaxPhysicalArmor":350,"adjMinMagicArmor":232,"adjMaxMagicArmor":350,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012755: _tools.RODict({
        "propID": 52012755,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":254,"adjMaxPhysicalArmor":386,"adjMinMagicArmor":254,"adjMaxMagicArmor":386,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012756: _tools.RODict({
        "propID": 52012756,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":280,"adjMaxPhysicalArmor":423,"adjMinMagicArmor":280,"adjMaxMagicArmor":423,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012757: _tools.RODict({
        "propID": 52012757,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":308,"adjMaxPhysicalArmor":466,"adjMinMagicArmor":308,"adjMaxMagicArmor":466,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012758: _tools.RODict({
        "propID": 52012758,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":83,"adjMaxPhysicalArmor":125,"adjMinMagicArmor":83,"adjMaxMagicArmor":125})
    }),
    52012759: _tools.RODict({
        "propID": 52012759,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":92,"adjMaxPhysicalArmor":138,"adjMinMagicArmor":92,"adjMaxMagicArmor":138})
    }),
    52012760: _tools.RODict({
        "propID": 52012760,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":100,"adjMaxPhysicalArmor":151,"adjMinMagicArmor":100,"adjMaxMagicArmor":151})
    }),
    52012761: _tools.RODict({
        "propID": 52012761,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":108,"adjMaxPhysicalArmor":162,"adjMinMagicArmor":108,"adjMaxMagicArmor":162})
    }),
    52012762: _tools.RODict({
        "propID": 52012762,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":117,"adjMaxPhysicalArmor":175,"adjMinMagicArmor":117,"adjMaxMagicArmor":175,"adjMortal":0.05})
    }),
    52012763: _tools.RODict({
        "propID": 52012763,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":128,"adjMaxPhysicalArmor":193,"adjMinMagicArmor":128,"adjMaxMagicArmor":193,"adjMortal":0.05})
    }),
    52012764: _tools.RODict({
        "propID": 52012764,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":139,"adjMaxPhysicalArmor":210,"adjMinMagicArmor":139,"adjMaxMagicArmor":210,"adjMortal":0.05})
    }),
    52012765: _tools.RODict({
        "propID": 52012765,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":151,"adjMaxPhysicalArmor":227,"adjMinMagicArmor":151,"adjMaxMagicArmor":227,"adjMortal":0.05})
    }),
    52012766: _tools.RODict({
        "propID": 52012766,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":162,"adjMaxPhysicalArmor":246,"adjMinMagicArmor":162,"adjMaxMagicArmor":246,"adjMortal":0.1})
    }),
    52012767: _tools.RODict({
        "propID": 52012767,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":179,"adjMaxPhysicalArmor":270,"adjMinMagicArmor":179,"adjMaxMagicArmor":270,"adjMortal":0.1})
    }),
    52012768: _tools.RODict({
        "propID": 52012768,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":194,"adjMaxPhysicalArmor":294,"adjMinMagicArmor":194,"adjMaxMagicArmor":294,"adjMortal":0.1})
    }),
    52012769: _tools.RODict({
        "propID": 52012769,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":211,"adjMaxPhysicalArmor":320,"adjMinMagicArmor":211,"adjMaxMagicArmor":320,"adjMortal":0.1})
    }),
    52012770: _tools.RODict({
        "propID": 52012770,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":244,"adjMaxPhysicalArmor":368,"adjMinMagicArmor":244,"adjMaxMagicArmor":368,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012771: _tools.RODict({
        "propID": 52012771,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":267,"adjMaxPhysicalArmor":405,"adjMinMagicArmor":267,"adjMaxMagicArmor":405,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012772: _tools.RODict({
        "propID": 52012772,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":294,"adjMaxPhysicalArmor":444,"adjMinMagicArmor":294,"adjMaxMagicArmor":444,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012773: _tools.RODict({
        "propID": 52012773,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":323,"adjMaxPhysicalArmor":489,"adjMinMagicArmor":323,"adjMaxMagicArmor":489,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012774: _tools.RODict({
        "propID": 52012774,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":87,"adjMaxPhysicalArmor":131,"adjMinMagicArmor":87,"adjMaxMagicArmor":131})
    }),
    52012775: _tools.RODict({
        "propID": 52012775,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":97,"adjMaxPhysicalArmor":145,"adjMinMagicArmor":97,"adjMaxMagicArmor":145})
    }),
    52012776: _tools.RODict({
        "propID": 52012776,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":105,"adjMaxPhysicalArmor":159,"adjMinMagicArmor":105,"adjMaxMagicArmor":159})
    }),
    52012777: _tools.RODict({
        "propID": 52012777,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":113,"adjMaxPhysicalArmor":170,"adjMinMagicArmor":113,"adjMaxMagicArmor":170})
    }),
    52012778: _tools.RODict({
        "propID": 52012778,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":123,"adjMaxPhysicalArmor":184,"adjMinMagicArmor":123,"adjMaxMagicArmor":184,"adjMortal":0.05})
    }),
    52012779: _tools.RODict({
        "propID": 52012779,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":134,"adjMaxPhysicalArmor":203,"adjMinMagicArmor":134,"adjMaxMagicArmor":203,"adjMortal":0.05})
    }),
    52012780: _tools.RODict({
        "propID": 52012780,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":146,"adjMaxPhysicalArmor":221,"adjMinMagicArmor":146,"adjMaxMagicArmor":221,"adjMortal":0.05})
    }),
    52012781: _tools.RODict({
        "propID": 52012781,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":159,"adjMaxPhysicalArmor":238,"adjMinMagicArmor":159,"adjMaxMagicArmor":238,"adjMortal":0.05})
    }),
    52012782: _tools.RODict({
        "propID": 52012782,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":170,"adjMaxPhysicalArmor":258,"adjMinMagicArmor":170,"adjMaxMagicArmor":258,"adjMortal":0.1})
    }),
    52012783: _tools.RODict({
        "propID": 52012783,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":188,"adjMaxPhysicalArmor":284,"adjMinMagicArmor":188,"adjMaxMagicArmor":284,"adjMortal":0.1})
    }),
    52012784: _tools.RODict({
        "propID": 52012784,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":204,"adjMaxPhysicalArmor":309,"adjMinMagicArmor":204,"adjMaxMagicArmor":309,"adjMortal":0.1})
    }),
    52012785: _tools.RODict({
        "propID": 52012785,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":222,"adjMaxPhysicalArmor":336,"adjMinMagicArmor":222,"adjMaxMagicArmor":336,"adjMortal":0.1})
    }),
    52012786: _tools.RODict({
        "propID": 52012786,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":256,"adjMaxPhysicalArmor":386,"adjMinMagicArmor":256,"adjMaxMagicArmor":386,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012787: _tools.RODict({
        "propID": 52012787,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":280,"adjMaxPhysicalArmor":425,"adjMinMagicArmor":280,"adjMaxMagicArmor":425,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012788: _tools.RODict({
        "propID": 52012788,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":309,"adjMaxPhysicalArmor":466,"adjMinMagicArmor":309,"adjMaxMagicArmor":466,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012789: _tools.RODict({
        "propID": 52012789,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":339,"adjMaxPhysicalArmor":513,"adjMinMagicArmor":339,"adjMaxMagicArmor":513,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012790: _tools.RODict({
        "propID": 52012790,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":91,"adjMaxPhysicalArmor":138,"adjMinMagicArmor":91,"adjMaxMagicArmor":138})
    }),
    52012791: _tools.RODict({
        "propID": 52012791,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":102,"adjMaxPhysicalArmor":152,"adjMinMagicArmor":102,"adjMaxMagicArmor":152})
    }),
    52012792: _tools.RODict({
        "propID": 52012792,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":110,"adjMaxPhysicalArmor":167,"adjMinMagicArmor":110,"adjMaxMagicArmor":167})
    }),
    52012793: _tools.RODict({
        "propID": 52012793,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":119,"adjMaxPhysicalArmor":179,"adjMinMagicArmor":119,"adjMaxMagicArmor":179})
    }),
    52012794: _tools.RODict({
        "propID": 52012794,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":129,"adjMaxPhysicalArmor":193,"adjMinMagicArmor":129,"adjMaxMagicArmor":193,"adjMortal":0.05})
    }),
    52012795: _tools.RODict({
        "propID": 52012795,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":141,"adjMaxPhysicalArmor":213,"adjMinMagicArmor":141,"adjMaxMagicArmor":213,"adjMortal":0.05})
    }),
    52012796: _tools.RODict({
        "propID": 52012796,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":153,"adjMaxPhysicalArmor":232,"adjMinMagicArmor":153,"adjMaxMagicArmor":232,"adjMortal":0.05})
    }),
    52012797: _tools.RODict({
        "propID": 52012797,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":167,"adjMaxPhysicalArmor":250,"adjMinMagicArmor":167,"adjMaxMagicArmor":250,"adjMortal":0.05})
    }),
    52012798: _tools.RODict({
        "propID": 52012798,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":179,"adjMaxPhysicalArmor":271,"adjMinMagicArmor":179,"adjMaxMagicArmor":271,"adjMortal":0.1})
    }),
    52012799: _tools.RODict({
        "propID": 52012799,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":197,"adjMaxPhysicalArmor":298,"adjMinMagicArmor":197,"adjMaxMagicArmor":298,"adjMortal":0.1})
    }),
    52012800: _tools.RODict({
        "propID": 52012800,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":214,"adjMaxPhysicalArmor":324,"adjMinMagicArmor":214,"adjMaxMagicArmor":324,"adjMortal":0.1})
    }),
    52012801: _tools.RODict({
        "propID": 52012801,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":233,"adjMaxPhysicalArmor":353,"adjMinMagicArmor":233,"adjMaxMagicArmor":353,"adjMortal":0.1})
    }),
    52012802: _tools.RODict({
        "propID": 52012802,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":269,"adjMaxPhysicalArmor":405,"adjMinMagicArmor":269,"adjMaxMagicArmor":405,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012803: _tools.RODict({
        "propID": 52012803,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":294,"adjMaxPhysicalArmor":446,"adjMinMagicArmor":294,"adjMaxMagicArmor":446,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012804: _tools.RODict({
        "propID": 52012804,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":324,"adjMaxPhysicalArmor":489,"adjMinMagicArmor":324,"adjMaxMagicArmor":489,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012805: _tools.RODict({
        "propID": 52012805,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":356,"adjMaxPhysicalArmor":539,"adjMinMagicArmor":356,"adjMaxMagicArmor":539,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012806: _tools.RODict({
        "propID": 52012806,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":96,"adjMaxPhysicalArmor":145,"adjMinMagicArmor":96,"adjMaxMagicArmor":145})
    }),
    52012807: _tools.RODict({
        "propID": 52012807,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":107,"adjMaxPhysicalArmor":160,"adjMinMagicArmor":107,"adjMaxMagicArmor":160})
    }),
    52012808: _tools.RODict({
        "propID": 52012808,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":116,"adjMaxPhysicalArmor":175,"adjMinMagicArmor":116,"adjMaxMagicArmor":175})
    }),
    52012809: _tools.RODict({
        "propID": 52012809,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":125,"adjMaxPhysicalArmor":188,"adjMinMagicArmor":125,"adjMaxMagicArmor":188})
    }),
    52012810: _tools.RODict({
        "propID": 52012810,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":135,"adjMaxPhysicalArmor":203,"adjMinMagicArmor":135,"adjMaxMagicArmor":203,"adjMortal":0.05})
    }),
    52012811: _tools.RODict({
        "propID": 52012811,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":148,"adjMaxPhysicalArmor":224,"adjMinMagicArmor":148,"adjMaxMagicArmor":224,"adjMortal":0.05})
    }),
    52012812: _tools.RODict({
        "propID": 52012812,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":161,"adjMaxPhysicalArmor":244,"adjMinMagicArmor":161,"adjMaxMagicArmor":244,"adjMortal":0.05})
    }),
    52012813: _tools.RODict({
        "propID": 52012813,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":175,"adjMaxPhysicalArmor":263,"adjMinMagicArmor":175,"adjMaxMagicArmor":263,"adjMortal":0.05})
    }),
    52012814: _tools.RODict({
        "propID": 52012814,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":188,"adjMaxPhysicalArmor":285,"adjMinMagicArmor":188,"adjMaxMagicArmor":285,"adjMortal":0.1})
    }),
    52012815: _tools.RODict({
        "propID": 52012815,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":207,"adjMaxPhysicalArmor":313,"adjMinMagicArmor":207,"adjMaxMagicArmor":313,"adjMortal":0.1})
    }),
    52012816: _tools.RODict({
        "propID": 52012816,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":225,"adjMaxPhysicalArmor":340,"adjMinMagicArmor":225,"adjMaxMagicArmor":340,"adjMortal":0.1})
    }),
    52012817: _tools.RODict({
        "propID": 52012817,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":245,"adjMaxPhysicalArmor":371,"adjMinMagicArmor":245,"adjMaxMagicArmor":371,"adjMortal":0.1})
    }),
    52012818: _tools.RODict({
        "propID": 52012818,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":282,"adjMaxPhysicalArmor":425,"adjMinMagicArmor":282,"adjMaxMagicArmor":425,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012819: _tools.RODict({
        "propID": 52012819,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":309,"adjMaxPhysicalArmor":468,"adjMinMagicArmor":309,"adjMaxMagicArmor":468,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012820: _tools.RODict({
        "propID": 52012820,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":340,"adjMaxPhysicalArmor":513,"adjMinMagicArmor":340,"adjMaxMagicArmor":513,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012821: _tools.RODict({
        "propID": 52012821,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":374,"adjMaxPhysicalArmor":566,"adjMinMagicArmor":374,"adjMaxMagicArmor":566,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012822: _tools.RODict({
        "propID": 52012822,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":101,"adjMaxPhysicalArmor":152,"adjMinMagicArmor":101,"adjMaxMagicArmor":152})
    }),
    52012823: _tools.RODict({
        "propID": 52012823,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":112,"adjMaxPhysicalArmor":168,"adjMinMagicArmor":112,"adjMaxMagicArmor":168})
    }),
    52012824: _tools.RODict({
        "propID": 52012824,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":122,"adjMaxPhysicalArmor":184,"adjMinMagicArmor":122,"adjMaxMagicArmor":184})
    }),
    52012825: _tools.RODict({
        "propID": 52012825,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":131,"adjMaxPhysicalArmor":197,"adjMinMagicArmor":131,"adjMaxMagicArmor":197})
    }),
    52012826: _tools.RODict({
        "propID": 52012826,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":142,"adjMaxPhysicalArmor":213,"adjMinMagicArmor":142,"adjMaxMagicArmor":213,"adjMortal":0.05})
    }),
    52012827: _tools.RODict({
        "propID": 52012827,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":155,"adjMaxPhysicalArmor":235,"adjMinMagicArmor":155,"adjMaxMagicArmor":235,"adjMortal":0.05})
    }),
    52012828: _tools.RODict({
        "propID": 52012828,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":169,"adjMaxPhysicalArmor":256,"adjMinMagicArmor":169,"adjMaxMagicArmor":256,"adjMortal":0.05})
    }),
    52012829: _tools.RODict({
        "propID": 52012829,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":184,"adjMaxPhysicalArmor":276,"adjMinMagicArmor":184,"adjMaxMagicArmor":276,"adjMortal":0.05})
    }),
    52012830: _tools.RODict({
        "propID": 52012830,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":197,"adjMaxPhysicalArmor":299,"adjMinMagicArmor":197,"adjMaxMagicArmor":299,"adjMortal":0.1})
    }),
    52012831: _tools.RODict({
        "propID": 52012831,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":217,"adjMaxPhysicalArmor":329,"adjMinMagicArmor":217,"adjMaxMagicArmor":329,"adjMortal":0.1})
    }),
    52012832: _tools.RODict({
        "propID": 52012832,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":236,"adjMaxPhysicalArmor":357,"adjMinMagicArmor":236,"adjMaxMagicArmor":357,"adjMortal":0.1})
    }),
    52012833: _tools.RODict({
        "propID": 52012833,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":257,"adjMaxPhysicalArmor":390,"adjMinMagicArmor":257,"adjMaxMagicArmor":390,"adjMortal":0.1})
    }),
    52012834: _tools.RODict({
        "propID": 52012834,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":296,"adjMaxPhysicalArmor":446,"adjMinMagicArmor":296,"adjMaxMagicArmor":446,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012835: _tools.RODict({
        "propID": 52012835,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":324,"adjMaxPhysicalArmor":491,"adjMinMagicArmor":324,"adjMaxMagicArmor":491,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012836: _tools.RODict({
        "propID": 52012836,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":357,"adjMaxPhysicalArmor":539,"adjMinMagicArmor":357,"adjMaxMagicArmor":539,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012837: _tools.RODict({
        "propID": 52012837,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":393,"adjMaxPhysicalArmor":594,"adjMinMagicArmor":393,"adjMaxMagicArmor":594,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012838: _tools.RODict({
        "propID": 52012838,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":106,"adjMaxPhysicalArmor":160,"adjMinMagicArmor":106,"adjMaxMagicArmor":160})
    }),
    52012839: _tools.RODict({
        "propID": 52012839,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":118,"adjMaxPhysicalArmor":176,"adjMinMagicArmor":118,"adjMaxMagicArmor":176})
    }),
    52012840: _tools.RODict({
        "propID": 52012840,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":128,"adjMaxPhysicalArmor":193,"adjMinMagicArmor":128,"adjMaxMagicArmor":193})
    }),
    52012841: _tools.RODict({
        "propID": 52012841,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":138,"adjMaxPhysicalArmor":207,"adjMinMagicArmor":138,"adjMaxMagicArmor":207})
    }),
    52012842: _tools.RODict({
        "propID": 52012842,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":149,"adjMaxPhysicalArmor":224,"adjMinMagicArmor":149,"adjMaxMagicArmor":224,"adjMortal":0.05})
    }),
    52012843: _tools.RODict({
        "propID": 52012843,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":163,"adjMaxPhysicalArmor":247,"adjMinMagicArmor":163,"adjMaxMagicArmor":247,"adjMortal":0.05})
    }),
    52012844: _tools.RODict({
        "propID": 52012844,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":177,"adjMaxPhysicalArmor":269,"adjMinMagicArmor":177,"adjMaxMagicArmor":269,"adjMortal":0.05})
    }),
    52012845: _tools.RODict({
        "propID": 52012845,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":193,"adjMaxPhysicalArmor":290,"adjMinMagicArmor":193,"adjMaxMagicArmor":290,"adjMortal":0.05})
    }),
    52012846: _tools.RODict({
        "propID": 52012846,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":207,"adjMaxPhysicalArmor":314,"adjMinMagicArmor":207,"adjMaxMagicArmor":314,"adjMortal":0.1})
    }),
    52012847: _tools.RODict({
        "propID": 52012847,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":228,"adjMaxPhysicalArmor":345,"adjMinMagicArmor":228,"adjMaxMagicArmor":345,"adjMortal":0.1})
    }),
    52012848: _tools.RODict({
        "propID": 52012848,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":248,"adjMaxPhysicalArmor":375,"adjMinMagicArmor":248,"adjMaxMagicArmor":375,"adjMortal":0.1})
    }),
    52012849: _tools.RODict({
        "propID": 52012849,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":270,"adjMaxPhysicalArmor":410,"adjMinMagicArmor":270,"adjMaxMagicArmor":410,"adjMortal":0.1})
    }),
    52012850: _tools.RODict({
        "propID": 52012850,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":311,"adjMaxPhysicalArmor":468,"adjMinMagicArmor":311,"adjMaxMagicArmor":468,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012851: _tools.RODict({
        "propID": 52012851,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":340,"adjMaxPhysicalArmor":516,"adjMinMagicArmor":340,"adjMaxMagicArmor":516,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012852: _tools.RODict({
        "propID": 52012852,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":375,"adjMaxPhysicalArmor":566,"adjMinMagicArmor":375,"adjMaxMagicArmor":566,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012853: _tools.RODict({
        "propID": 52012853,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":413,"adjMaxPhysicalArmor":624,"adjMinMagicArmor":413,"adjMaxMagicArmor":624,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012854: _tools.RODict({
        "propID": 52012854,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":22,"adjMaxMagicArmor":33})
    }),
    52012855: _tools.RODict({
        "propID": 52012855,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":24,"adjMaxMagicArmor":36})
    }),
    52012856: _tools.RODict({
        "propID": 52012856,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":26,"adjMaxMagicArmor":40})
    }),
    52012857: _tools.RODict({
        "propID": 52012857,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":29,"adjMaxMagicArmor":43})
    }),
    52012858: _tools.RODict({
        "propID": 52012858,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":31,"adjMaxMagicArmor":46,"adjAntiFatal":10,"adjMortal":0.05})
    }),
    52012859: _tools.RODict({
        "propID": 52012859,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":34,"adjMaxMagicArmor":51,"adjAntiFatal":11,"adjMortal":0.05})
    }),
    52012860: _tools.RODict({
        "propID": 52012860,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":37,"adjMaxMagicArmor":55,"adjAntiFatal":12,"adjMortal":0.05})
    }),
    52012861: _tools.RODict({
        "propID": 52012861,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":40,"adjMaxMagicArmor":60,"adjAntiFatal":13,"adjMortal":0.05})
    }),
    52012862: _tools.RODict({
        "propID": 52012862,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":43,"adjMaxMagicArmor":64,"adjAntiFatal":14,"adjMortal":0.1})
    }),
    52012863: _tools.RODict({
        "propID": 52012863,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":47,"adjMaxMagicArmor":70,"adjAntiFatal":15,"adjMortal":0.1})
    }),
    52012864: _tools.RODict({
        "propID": 52012864,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":52,"adjMaxMagicArmor":77,"adjAntiFatal":17,"adjMortal":0.1})
    }),
    52012865: _tools.RODict({
        "propID": 52012865,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":56,"adjMaxMagicArmor":83,"adjAntiFatal":18,"adjMortal":0.1})
    }),
    52012866: _tools.RODict({
        "propID": 52012866,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":64,"adjMaxMagicArmor":95,"adjAntiFatal":21,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012867: _tools.RODict({
        "propID": 52012867,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":70,"adjMaxMagicArmor":105,"adjAntiFatal":23,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012868: _tools.RODict({
        "propID": 52012868,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":77,"adjMaxMagicArmor":116,"adjAntiFatal":25,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012869: _tools.RODict({
        "propID": 52012869,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":85,"adjMaxMagicArmor":128,"adjAntiFatal":28,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012870: _tools.RODict({
        "propID": 52012870,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":23,"adjMaxMagicArmor":35})
    }),
    52012871: _tools.RODict({
        "propID": 52012871,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":25,"adjMaxMagicArmor":38})
    }),
    52012872: _tools.RODict({
        "propID": 52012872,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":27,"adjMaxMagicArmor":42})
    }),
    52012873: _tools.RODict({
        "propID": 52012873,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":30,"adjMaxMagicArmor":45})
    }),
    52012874: _tools.RODict({
        "propID": 52012874,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":33,"adjMaxMagicArmor":48,"adjAntiFatal":11,"adjMortal":0.05})
    }),
    52012875: _tools.RODict({
        "propID": 52012875,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":36,"adjMaxMagicArmor":54,"adjAntiFatal":12,"adjMortal":0.05})
    }),
    52012876: _tools.RODict({
        "propID": 52012876,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":39,"adjMaxMagicArmor":58,"adjAntiFatal":13,"adjMortal":0.05})
    }),
    52012877: _tools.RODict({
        "propID": 52012877,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":42,"adjMaxMagicArmor":63,"adjAntiFatal":14,"adjMortal":0.05})
    }),
    52012878: _tools.RODict({
        "propID": 52012878,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":45,"adjMaxMagicArmor":67,"adjAntiFatal":15,"adjMortal":0.1})
    }),
    52012879: _tools.RODict({
        "propID": 52012879,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":49,"adjMaxMagicArmor":74,"adjAntiFatal":16,"adjMortal":0.1})
    }),
    52012880: _tools.RODict({
        "propID": 52012880,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":55,"adjMaxMagicArmor":81,"adjAntiFatal":18,"adjMortal":0.1})
    }),
    52012881: _tools.RODict({
        "propID": 52012881,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":59,"adjMaxMagicArmor":87,"adjAntiFatal":19,"adjMortal":0.1})
    }),
    52012882: _tools.RODict({
        "propID": 52012882,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":67,"adjMaxMagicArmor":100,"adjAntiFatal":22,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012883: _tools.RODict({
        "propID": 52012883,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":74,"adjMaxMagicArmor":110,"adjAntiFatal":24,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012884: _tools.RODict({
        "propID": 52012884,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":81,"adjMaxMagicArmor":122,"adjAntiFatal":26,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012885: _tools.RODict({
        "propID": 52012885,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":89,"adjMaxMagicArmor":134,"adjAntiFatal":29,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012886: _tools.RODict({
        "propID": 52012886,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":24,"adjMaxMagicArmor":37})
    }),
    52012887: _tools.RODict({
        "propID": 52012887,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":26,"adjMaxMagicArmor":40})
    }),
    52012888: _tools.RODict({
        "propID": 52012888,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":28,"adjMaxMagicArmor":44})
    }),
    52012889: _tools.RODict({
        "propID": 52012889,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":32,"adjMaxMagicArmor":47})
    }),
    52012890: _tools.RODict({
        "propID": 52012890,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":35,"adjMaxMagicArmor":50,"adjAntiFatal":12,"adjMortal":0.05})
    }),
    52012891: _tools.RODict({
        "propID": 52012891,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":38,"adjMaxMagicArmor":57,"adjAntiFatal":13,"adjMortal":0.05})
    }),
    52012892: _tools.RODict({
        "propID": 52012892,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":41,"adjMaxMagicArmor":61,"adjAntiFatal":14,"adjMortal":0.05})
    }),
    52012893: _tools.RODict({
        "propID": 52012893,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":44,"adjMaxMagicArmor":66,"adjAntiFatal":15,"adjMortal":0.05})
    }),
    52012894: _tools.RODict({
        "propID": 52012894,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":47,"adjMaxMagicArmor":70,"adjAntiFatal":16,"adjMortal":0.1})
    }),
    52012895: _tools.RODict({
        "propID": 52012895,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":51,"adjMaxMagicArmor":78,"adjAntiFatal":17,"adjMortal":0.1})
    }),
    52012896: _tools.RODict({
        "propID": 52012896,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":58,"adjMaxMagicArmor":85,"adjAntiFatal":19,"adjMortal":0.1})
    }),
    52012897: _tools.RODict({
        "propID": 52012897,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":62,"adjMaxMagicArmor":91,"adjAntiFatal":20,"adjMortal":0.1})
    }),
    52012898: _tools.RODict({
        "propID": 52012898,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":70,"adjMaxMagicArmor":105,"adjAntiFatal":23,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012899: _tools.RODict({
        "propID": 52012899,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":78,"adjMaxMagicArmor":116,"adjAntiFatal":25,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012900: _tools.RODict({
        "propID": 52012900,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":85,"adjMaxMagicArmor":128,"adjAntiFatal":27,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012901: _tools.RODict({
        "propID": 52012901,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":93,"adjMaxMagicArmor":141,"adjAntiFatal":30,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012902: _tools.RODict({
        "propID": 52012902,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":25,"adjMaxMagicArmor":39})
    }),
    52012903: _tools.RODict({
        "propID": 52012903,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":27,"adjMaxMagicArmor":42})
    }),
    52012904: _tools.RODict({
        "propID": 52012904,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":29,"adjMaxMagicArmor":46})
    }),
    52012905: _tools.RODict({
        "propID": 52012905,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":34,"adjMaxMagicArmor":49})
    }),
    52012906: _tools.RODict({
        "propID": 52012906,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":37,"adjMaxMagicArmor":53,"adjAntiFatal":13,"adjMortal":0.05})
    }),
    52012907: _tools.RODict({
        "propID": 52012907,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":40,"adjMaxMagicArmor":60,"adjAntiFatal":14,"adjMortal":0.05})
    }),
    52012908: _tools.RODict({
        "propID": 52012908,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":43,"adjMaxMagicArmor":64,"adjAntiFatal":15,"adjMortal":0.05})
    }),
    52012909: _tools.RODict({
        "propID": 52012909,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":46,"adjMaxMagicArmor":69,"adjAntiFatal":16,"adjMortal":0.05})
    }),
    52012910: _tools.RODict({
        "propID": 52012910,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":49,"adjMaxMagicArmor":74,"adjAntiFatal":17,"adjMortal":0.1})
    }),
    52012911: _tools.RODict({
        "propID": 52012911,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":54,"adjMaxMagicArmor":82,"adjAntiFatal":18,"adjMortal":0.1})
    }),
    52012912: _tools.RODict({
        "propID": 52012912,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":61,"adjMaxMagicArmor":89,"adjAntiFatal":20,"adjMortal":0.1})
    }),
    52012913: _tools.RODict({
        "propID": 52012913,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":65,"adjMaxMagicArmor":96,"adjAntiFatal":21,"adjMortal":0.1})
    }),
    52012914: _tools.RODict({
        "propID": 52012914,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":74,"adjMaxMagicArmor":110,"adjAntiFatal":24,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012915: _tools.RODict({
        "propID": 52012915,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":82,"adjMaxMagicArmor":122,"adjAntiFatal":26,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012916: _tools.RODict({
        "propID": 52012916,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":89,"adjMaxMagicArmor":134,"adjAntiFatal":28,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012917: _tools.RODict({
        "propID": 52012917,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":98,"adjMaxMagicArmor":148,"adjAntiFatal":32,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012918: _tools.RODict({
        "propID": 52012918,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":26,"adjMaxMagicArmor":41})
    }),
    52012919: _tools.RODict({
        "propID": 52012919,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":28,"adjMaxMagicArmor":44})
    }),
    52012920: _tools.RODict({
        "propID": 52012920,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":30,"adjMaxMagicArmor":48})
    }),
    52012921: _tools.RODict({
        "propID": 52012921,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":36,"adjMaxMagicArmor":51})
    }),
    52012922: _tools.RODict({
        "propID": 52012922,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":39,"adjMaxMagicArmor":56,"adjAntiFatal":14,"adjMortal":0.05})
    }),
    52012923: _tools.RODict({
        "propID": 52012923,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":42,"adjMaxMagicArmor":63,"adjAntiFatal":15,"adjMortal":0.05})
    }),
    52012924: _tools.RODict({
        "propID": 52012924,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":45,"adjMaxMagicArmor":67,"adjAntiFatal":16,"adjMortal":0.05})
    }),
    52012925: _tools.RODict({
        "propID": 52012925,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":48,"adjMaxMagicArmor":72,"adjAntiFatal":17,"adjMortal":0.05})
    }),
    52012926: _tools.RODict({
        "propID": 52012926,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":51,"adjMaxMagicArmor":78,"adjAntiFatal":18,"adjMortal":0.1})
    }),
    52012927: _tools.RODict({
        "propID": 52012927,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":57,"adjMaxMagicArmor":86,"adjAntiFatal":19,"adjMortal":0.1})
    }),
    52012928: _tools.RODict({
        "propID": 52012928,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":64,"adjMaxMagicArmor":93,"adjAntiFatal":21,"adjMortal":0.1})
    }),
    52012929: _tools.RODict({
        "propID": 52012929,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":68,"adjMaxMagicArmor":101,"adjAntiFatal":22,"adjMortal":0.1})
    }),
    52012930: _tools.RODict({
        "propID": 52012930,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":78,"adjMaxMagicArmor":116,"adjAntiFatal":25,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012931: _tools.RODict({
        "propID": 52012931,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":86,"adjMaxMagicArmor":128,"adjAntiFatal":27,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012932: _tools.RODict({
        "propID": 52012932,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":93,"adjMaxMagicArmor":141,"adjAntiFatal":29,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012933: _tools.RODict({
        "propID": 52012933,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":103,"adjMaxMagicArmor":155,"adjAntiFatal":34,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012934: _tools.RODict({
        "propID": 52012934,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":27,"adjMaxMagicArmor":43})
    }),
    52012935: _tools.RODict({
        "propID": 52012935,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":29,"adjMaxMagicArmor":46})
    }),
    52012936: _tools.RODict({
        "propID": 52012936,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":32,"adjMaxMagicArmor":50})
    }),
    52012937: _tools.RODict({
        "propID": 52012937,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":38,"adjMaxMagicArmor":54})
    }),
    52012938: _tools.RODict({
        "propID": 52012938,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":41,"adjMaxMagicArmor":59,"adjAntiFatal":15,"adjMortal":0.05})
    }),
    52012939: _tools.RODict({
        "propID": 52012939,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":44,"adjMaxMagicArmor":66,"adjAntiFatal":16,"adjMortal":0.05})
    }),
    52012940: _tools.RODict({
        "propID": 52012940,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":47,"adjMaxMagicArmor":70,"adjAntiFatal":17,"adjMortal":0.05})
    }),
    52012941: _tools.RODict({
        "propID": 52012941,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":50,"adjMaxMagicArmor":76,"adjAntiFatal":18,"adjMortal":0.05})
    }),
    52012942: _tools.RODict({
        "propID": 52012942,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":54,"adjMaxMagicArmor":82,"adjAntiFatal":19,"adjMortal":0.1})
    }),
    52012943: _tools.RODict({
        "propID": 52012943,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":60,"adjMaxMagicArmor":90,"adjAntiFatal":20,"adjMortal":0.1})
    }),
    52012944: _tools.RODict({
        "propID": 52012944,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":67,"adjMaxMagicArmor":98,"adjAntiFatal":22,"adjMortal":0.1})
    }),
    52012945: _tools.RODict({
        "propID": 52012945,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":71,"adjMaxMagicArmor":106,"adjAntiFatal":23,"adjMortal":0.1})
    }),
    52012946: _tools.RODict({
        "propID": 52012946,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":82,"adjMaxMagicArmor":122,"adjAntiFatal":26,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012947: _tools.RODict({
        "propID": 52012947,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":90,"adjMaxMagicArmor":134,"adjAntiFatal":28,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012948: _tools.RODict({
        "propID": 52012948,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":98,"adjMaxMagicArmor":148,"adjAntiFatal":30,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012949: _tools.RODict({
        "propID": 52012949,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":108,"adjMaxMagicArmor":163,"adjAntiFatal":36,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012950: _tools.RODict({
        "propID": 52012950,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":28,"adjMaxMagicArmor":45})
    }),
    52012951: _tools.RODict({
        "propID": 52012951,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":30,"adjMaxMagicArmor":48})
    }),
    52012952: _tools.RODict({
        "propID": 52012952,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":34,"adjMaxMagicArmor":53})
    }),
    52012953: _tools.RODict({
        "propID": 52012953,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":40,"adjMaxMagicArmor":57})
    }),
    52012954: _tools.RODict({
        "propID": 52012954,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":43,"adjMaxMagicArmor":62,"adjAntiFatal":16,"adjMortal":0.05})
    }),
    52012955: _tools.RODict({
        "propID": 52012955,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":46,"adjMaxMagicArmor":69,"adjAntiFatal":17,"adjMortal":0.05})
    }),
    52012956: _tools.RODict({
        "propID": 52012956,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":49,"adjMaxMagicArmor":74,"adjAntiFatal":18,"adjMortal":0.05})
    }),
    52012957: _tools.RODict({
        "propID": 52012957,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":53,"adjMaxMagicArmor":80,"adjAntiFatal":19,"adjMortal":0.05})
    }),
    52012958: _tools.RODict({
        "propID": 52012958,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":57,"adjMaxMagicArmor":86,"adjAntiFatal":20,"adjMortal":0.1})
    }),
    52012959: _tools.RODict({
        "propID": 52012959,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":63,"adjMaxMagicArmor":95,"adjAntiFatal":21,"adjMortal":0.1})
    }),
    52012960: _tools.RODict({
        "propID": 52012960,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":70,"adjMaxMagicArmor":103,"adjAntiFatal":23,"adjMortal":0.1})
    }),
    52012961: _tools.RODict({
        "propID": 52012961,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":75,"adjMaxMagicArmor":111,"adjAntiFatal":24,"adjMortal":0.1})
    }),
    52012962: _tools.RODict({
        "propID": 52012962,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":86,"adjMaxMagicArmor":128,"adjAntiFatal":27,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012963: _tools.RODict({
        "propID": 52012963,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":95,"adjMaxMagicArmor":141,"adjAntiFatal":29,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012964: _tools.RODict({
        "propID": 52012964,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":103,"adjMaxMagicArmor":155,"adjAntiFatal":32,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012965: _tools.RODict({
        "propID": 52012965,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":113,"adjMaxMagicArmor":171,"adjAntiFatal":38,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012966: _tools.RODict({
        "propID": 52012966,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":29,"adjMaxMagicArmor":47})
    }),
    52012967: _tools.RODict({
        "propID": 52012967,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":32,"adjMaxMagicArmor":50})
    }),
    52012968: _tools.RODict({
        "propID": 52012968,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":36,"adjMaxMagicArmor":56})
    }),
    52012969: _tools.RODict({
        "propID": 52012969,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":42,"adjMaxMagicArmor":60})
    }),
    52012970: _tools.RODict({
        "propID": 52012970,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":45,"adjMaxMagicArmor":65,"adjAntiFatal":17,"adjMortal":0.05})
    }),
    52012971: _tools.RODict({
        "propID": 52012971,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":48,"adjMaxMagicArmor":72,"adjAntiFatal":18,"adjMortal":0.05})
    }),
    52012972: _tools.RODict({
        "propID": 52012972,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":51,"adjMaxMagicArmor":78,"adjAntiFatal":19,"adjMortal":0.05})
    }),
    52012973: _tools.RODict({
        "propID": 52012973,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":56,"adjMaxMagicArmor":84,"adjAntiFatal":20,"adjMortal":0.05})
    }),
    52012974: _tools.RODict({
        "propID": 52012974,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":60,"adjMaxMagicArmor":90,"adjAntiFatal":21,"adjMortal":0.1})
    }),
    52012975: _tools.RODict({
        "propID": 52012975,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":66,"adjMaxMagicArmor":100,"adjAntiFatal":22,"adjMortal":0.1})
    }),
    52012976: _tools.RODict({
        "propID": 52012976,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":74,"adjMaxMagicArmor":108,"adjAntiFatal":24,"adjMortal":0.1})
    }),
    52012977: _tools.RODict({
        "propID": 52012977,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":79,"adjMaxMagicArmor":117,"adjAntiFatal":25,"adjMortal":0.1})
    }),
    52012978: _tools.RODict({
        "propID": 52012978,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":90,"adjMaxMagicArmor":134,"adjAntiFatal":28,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012979: _tools.RODict({
        "propID": 52012979,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":100,"adjMaxMagicArmor":148,"adjAntiFatal":30,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012980: _tools.RODict({
        "propID": 52012980,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":108,"adjMaxMagicArmor":163,"adjAntiFatal":34,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012981: _tools.RODict({
        "propID": 52012981,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":119,"adjMaxMagicArmor":180,"adjAntiFatal":40,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012982: _tools.RODict({
        "propID": 52012982,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":30,"adjMaxMagicArmor":49})
    }),
    52012983: _tools.RODict({
        "propID": 52012983,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":34,"adjMaxMagicArmor":53})
    }),
    52012984: _tools.RODict({
        "propID": 52012984,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":38,"adjMaxMagicArmor":59})
    }),
    52012985: _tools.RODict({
        "propID": 52012985,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":44,"adjMaxMagicArmor":63})
    }),
    52012986: _tools.RODict({
        "propID": 52012986,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":47,"adjMaxMagicArmor":68,"adjAntiFatal":18,"adjMortal":0.05})
    }),
    52012987: _tools.RODict({
        "propID": 52012987,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":50,"adjMaxMagicArmor":76,"adjAntiFatal":19,"adjMortal":0.05})
    }),
    52012988: _tools.RODict({
        "propID": 52012988,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":54,"adjMaxMagicArmor":82,"adjAntiFatal":20,"adjMortal":0.05})
    }),
    52012989: _tools.RODict({
        "propID": 52012989,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":59,"adjMaxMagicArmor":88,"adjAntiFatal":21,"adjMortal":0.05})
    }),
    52012990: _tools.RODict({
        "propID": 52012990,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":63,"adjMaxMagicArmor":95,"adjAntiFatal":22,"adjMortal":0.1})
    }),
    52012991: _tools.RODict({
        "propID": 52012991,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":69,"adjMaxMagicArmor":105,"adjAntiFatal":23,"adjMortal":0.1})
    }),
    52012992: _tools.RODict({
        "propID": 52012992,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":78,"adjMaxMagicArmor":113,"adjAntiFatal":25,"adjMortal":0.1})
    }),
    52012993: _tools.RODict({
        "propID": 52012993,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":83,"adjMaxMagicArmor":123,"adjAntiFatal":26,"adjMortal":0.1})
    }),
    52012994: _tools.RODict({
        "propID": 52012994,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":95,"adjMaxMagicArmor":141,"adjAntiFatal":29,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012995: _tools.RODict({
        "propID": 52012995,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":105,"adjMaxMagicArmor":155,"adjAntiFatal":32,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012996: _tools.RODict({
        "propID": 52012996,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":113,"adjMaxMagicArmor":171,"adjAntiFatal":36,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012997: _tools.RODict({
        "propID": 52012997,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":125,"adjMaxMagicArmor":189,"adjAntiFatal":42,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52012998: _tools.RODict({
        "propID": 52012998,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":32,"adjMaxMagicArmor":51})
    }),
    52012999: _tools.RODict({
        "propID": 52012999,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":36,"adjMaxMagicArmor":56})
    }),
    52013000: _tools.RODict({
        "propID": 52013000,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":40,"adjMaxMagicArmor":62})
    }),
    52013001: _tools.RODict({
        "propID": 52013001,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":46,"adjMaxMagicArmor":66})
    }),
    52013002: _tools.RODict({
        "propID": 52013002,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":49,"adjMaxMagicArmor":71,"adjAntiFatal":19,"adjMortal":0.05})
    }),
    52013003: _tools.RODict({
        "propID": 52013003,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":53,"adjMaxMagicArmor":80,"adjAntiFatal":20,"adjMortal":0.05})
    }),
    52013004: _tools.RODict({
        "propID": 52013004,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":57,"adjMaxMagicArmor":86,"adjAntiFatal":21,"adjMortal":0.05})
    }),
    52013005: _tools.RODict({
        "propID": 52013005,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":62,"adjMaxMagicArmor":92,"adjAntiFatal":22,"adjMortal":0.05})
    }),
    52013006: _tools.RODict({
        "propID": 52013006,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":66,"adjMaxMagicArmor":100,"adjAntiFatal":23,"adjMortal":0.1})
    }),
    52013007: _tools.RODict({
        "propID": 52013007,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":72,"adjMaxMagicArmor":110,"adjAntiFatal":24,"adjMortal":0.1})
    }),
    52013008: _tools.RODict({
        "propID": 52013008,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":82,"adjMaxMagicArmor":119,"adjAntiFatal":26,"adjMortal":0.1})
    }),
    52013009: _tools.RODict({
        "propID": 52013009,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":87,"adjMaxMagicArmor":129,"adjAntiFatal":27,"adjMortal":0.1})
    }),
    52013010: _tools.RODict({
        "propID": 52013010,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":100,"adjMaxMagicArmor":148,"adjAntiFatal":30,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52013011: _tools.RODict({
        "propID": 52013011,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":110,"adjMaxMagicArmor":163,"adjAntiFatal":34,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52013012: _tools.RODict({
        "propID": 52013012,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":119,"adjMaxMagicArmor":180,"adjAntiFatal":38,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52013013: _tools.RODict({
        "propID": 52013013,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":131,"adjMaxMagicArmor":198,"adjAntiFatal":44,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52013014: _tools.RODict({
        "propID": 52013014,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":34,"adjMaxMagicArmor":54})
    }),
    52013015: _tools.RODict({
        "propID": 52013015,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":38,"adjMaxMagicArmor":59})
    }),
    52013016: _tools.RODict({
        "propID": 52013016,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":42,"adjMaxMagicArmor":65})
    }),
    52013017: _tools.RODict({
        "propID": 52013017,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":48,"adjMaxMagicArmor":69})
    }),
    52013018: _tools.RODict({
        "propID": 52013018,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":51,"adjMaxMagicArmor":75,"adjAntiFatal":20,"adjMortal":0.05})
    }),
    52013019: _tools.RODict({
        "propID": 52013019,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":56,"adjMaxMagicArmor":84,"adjAntiFatal":21,"adjMortal":0.05})
    }),
    52013020: _tools.RODict({
        "propID": 52013020,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":60,"adjMaxMagicArmor":90,"adjAntiFatal":22,"adjMortal":0.05})
    }),
    52013021: _tools.RODict({
        "propID": 52013021,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":65,"adjMaxMagicArmor":97,"adjAntiFatal":23,"adjMortal":0.05})
    }),
    52013022: _tools.RODict({
        "propID": 52013022,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":69,"adjMaxMagicArmor":105,"adjAntiFatal":24,"adjMortal":0.1})
    }),
    52013023: _tools.RODict({
        "propID": 52013023,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":76,"adjMaxMagicArmor":116,"adjAntiFatal":25,"adjMortal":0.1})
    }),
    52013024: _tools.RODict({
        "propID": 52013024,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":86,"adjMaxMagicArmor":125,"adjAntiFatal":27,"adjMortal":0.1})
    }),
    52013025: _tools.RODict({
        "propID": 52013025,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":91,"adjMaxMagicArmor":135,"adjAntiFatal":28,"adjMortal":0.1})
    }),
    52013026: _tools.RODict({
        "propID": 52013026,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":105,"adjMaxMagicArmor":155,"adjAntiFatal":32,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52013027: _tools.RODict({
        "propID": 52013027,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":116,"adjMaxMagicArmor":171,"adjAntiFatal":36,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52013028: _tools.RODict({
        "propID": 52013028,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":125,"adjMaxMagicArmor":189,"adjAntiFatal":40,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52013029: _tools.RODict({
        "propID": 52013029,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicArmor":138,"adjMaxMagicArmor":208,"adjAntiFatal":46,"adjMortal":0.1,"adjAntiMortal":0.1})
    }),
    52013030: _tools.RODict({
        "propID": 52013030,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":22,"adjMaxPhysicalArmor":33})
    }),
    52013031: _tools.RODict({
        "propID": 52013031,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":24,"adjMaxPhysicalArmor":36})
    }),
    52013032: _tools.RODict({
        "propID": 52013032,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":26,"adjMaxPhysicalArmor":40})
    }),
    52013033: _tools.RODict({
        "propID": 52013033,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":29,"adjMaxPhysicalArmor":43})
    }),
    52013034: _tools.RODict({
        "propID": 52013034,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":31,"adjMaxPhysicalArmor":46,"adjDodge":10,"adjPVPDmg":0.02})
    }),
    52013035: _tools.RODict({
        "propID": 52013035,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":34,"adjMaxPhysicalArmor":51,"adjDodge":11,"adjPVPDmg":0.02})
    }),
    52013036: _tools.RODict({
        "propID": 52013036,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":37,"adjMaxPhysicalArmor":55,"adjDodge":12,"adjPVPDmg":0.02})
    }),
    52013037: _tools.RODict({
        "propID": 52013037,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":40,"adjMaxPhysicalArmor":60,"adjDodge":13,"adjPVPDmg":0.02})
    }),
    52013038: _tools.RODict({
        "propID": 52013038,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":43,"adjMaxPhysicalArmor":64,"adjDodge":14,"adjPVPDmg":0.04})
    }),
    52013039: _tools.RODict({
        "propID": 52013039,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":47,"adjMaxPhysicalArmor":70,"adjDodge":15,"adjPVPDmg":0.04})
    }),
    52013040: _tools.RODict({
        "propID": 52013040,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":52,"adjMaxPhysicalArmor":77,"adjDodge":17,"adjPVPDmg":0.04})
    }),
    52013041: _tools.RODict({
        "propID": 52013041,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":56,"adjMaxPhysicalArmor":83,"adjDodge":18,"adjPVPDmg":0.04})
    }),
    52013042: _tools.RODict({
        "propID": 52013042,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":64,"adjMaxPhysicalArmor":95,"adjDodge":21,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013043: _tools.RODict({
        "propID": 52013043,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":70,"adjMaxPhysicalArmor":105,"adjDodge":23,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013044: _tools.RODict({
        "propID": 52013044,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":77,"adjMaxPhysicalArmor":116,"adjDodge":25,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013045: _tools.RODict({
        "propID": 52013045,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":85,"adjMaxPhysicalArmor":128,"adjDodge":28,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013046: _tools.RODict({
        "propID": 52013046,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":23,"adjMaxPhysicalArmor":35})
    }),
    52013047: _tools.RODict({
        "propID": 52013047,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":25,"adjMaxPhysicalArmor":38})
    }),
    52013048: _tools.RODict({
        "propID": 52013048,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":27,"adjMaxPhysicalArmor":42})
    }),
    52013049: _tools.RODict({
        "propID": 52013049,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":30,"adjMaxPhysicalArmor":45})
    }),
    52013050: _tools.RODict({
        "propID": 52013050,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":33,"adjMaxPhysicalArmor":48,"adjDodge":11,"adjPVPDmg":0.02})
    }),
    52013051: _tools.RODict({
        "propID": 52013051,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":36,"adjMaxPhysicalArmor":54,"adjDodge":12,"adjPVPDmg":0.02})
    }),
    52013052: _tools.RODict({
        "propID": 52013052,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":39,"adjMaxPhysicalArmor":58,"adjDodge":13,"adjPVPDmg":0.02})
    }),
    52013053: _tools.RODict({
        "propID": 52013053,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":42,"adjMaxPhysicalArmor":63,"adjDodge":14,"adjPVPDmg":0.02})
    }),
    52013054: _tools.RODict({
        "propID": 52013054,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":45,"adjMaxPhysicalArmor":67,"adjDodge":15,"adjPVPDmg":0.04})
    }),
    52013055: _tools.RODict({
        "propID": 52013055,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":49,"adjMaxPhysicalArmor":74,"adjDodge":16,"adjPVPDmg":0.04})
    }),
    52013056: _tools.RODict({
        "propID": 52013056,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":55,"adjMaxPhysicalArmor":81,"adjDodge":18,"adjPVPDmg":0.04})
    }),
    52013057: _tools.RODict({
        "propID": 52013057,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":59,"adjMaxPhysicalArmor":87,"adjDodge":19,"adjPVPDmg":0.04})
    }),
    52013058: _tools.RODict({
        "propID": 52013058,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":67,"adjMaxPhysicalArmor":100,"adjDodge":22,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013059: _tools.RODict({
        "propID": 52013059,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":74,"adjMaxPhysicalArmor":110,"adjDodge":24,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013060: _tools.RODict({
        "propID": 52013060,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":81,"adjMaxPhysicalArmor":122,"adjDodge":26,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013061: _tools.RODict({
        "propID": 52013061,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":89,"adjMaxPhysicalArmor":134,"adjDodge":29,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013062: _tools.RODict({
        "propID": 52013062,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":24,"adjMaxPhysicalArmor":37})
    }),
    52013063: _tools.RODict({
        "propID": 52013063,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":26,"adjMaxPhysicalArmor":40})
    }),
    52013064: _tools.RODict({
        "propID": 52013064,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":28,"adjMaxPhysicalArmor":44})
    }),
    52013065: _tools.RODict({
        "propID": 52013065,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":32,"adjMaxPhysicalArmor":47})
    }),
    52013066: _tools.RODict({
        "propID": 52013066,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":35,"adjMaxPhysicalArmor":50,"adjDodge":12,"adjPVPDmg":0.02})
    }),
    52013067: _tools.RODict({
        "propID": 52013067,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":38,"adjMaxPhysicalArmor":57,"adjDodge":13,"adjPVPDmg":0.02})
    }),
    52013068: _tools.RODict({
        "propID": 52013068,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":41,"adjMaxPhysicalArmor":61,"adjDodge":14,"adjPVPDmg":0.02})
    }),
    52013069: _tools.RODict({
        "propID": 52013069,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":44,"adjMaxPhysicalArmor":66,"adjDodge":15,"adjPVPDmg":0.02})
    }),
    52013070: _tools.RODict({
        "propID": 52013070,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":47,"adjMaxPhysicalArmor":70,"adjDodge":16,"adjPVPDmg":0.04})
    }),
    52013071: _tools.RODict({
        "propID": 52013071,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":51,"adjMaxPhysicalArmor":78,"adjDodge":17,"adjPVPDmg":0.04})
    }),
    52013072: _tools.RODict({
        "propID": 52013072,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":58,"adjMaxPhysicalArmor":85,"adjDodge":19,"adjPVPDmg":0.04})
    }),
    52013073: _tools.RODict({
        "propID": 52013073,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":62,"adjMaxPhysicalArmor":91,"adjDodge":20,"adjPVPDmg":0.04})
    }),
    52013074: _tools.RODict({
        "propID": 52013074,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":70,"adjMaxPhysicalArmor":105,"adjDodge":23,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013075: _tools.RODict({
        "propID": 52013075,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":78,"adjMaxPhysicalArmor":116,"adjDodge":25,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013076: _tools.RODict({
        "propID": 52013076,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":85,"adjMaxPhysicalArmor":128,"adjDodge":27,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013077: _tools.RODict({
        "propID": 52013077,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":93,"adjMaxPhysicalArmor":141,"adjDodge":30,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013078: _tools.RODict({
        "propID": 52013078,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":25,"adjMaxPhysicalArmor":39})
    }),
    52013079: _tools.RODict({
        "propID": 52013079,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":27,"adjMaxPhysicalArmor":42})
    }),
    52013080: _tools.RODict({
        "propID": 52013080,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":29,"adjMaxPhysicalArmor":46})
    }),
    52013081: _tools.RODict({
        "propID": 52013081,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":34,"adjMaxPhysicalArmor":49})
    }),
    52013082: _tools.RODict({
        "propID": 52013082,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":37,"adjMaxPhysicalArmor":53,"adjDodge":13,"adjPVPDmg":0.02})
    }),
    52013083: _tools.RODict({
        "propID": 52013083,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":40,"adjMaxPhysicalArmor":60,"adjDodge":14,"adjPVPDmg":0.02})
    }),
    52013084: _tools.RODict({
        "propID": 52013084,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":43,"adjMaxPhysicalArmor":64,"adjDodge":15,"adjPVPDmg":0.02})
    }),
    52013085: _tools.RODict({
        "propID": 52013085,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":46,"adjMaxPhysicalArmor":69,"adjDodge":16,"adjPVPDmg":0.02})
    }),
    52013086: _tools.RODict({
        "propID": 52013086,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":49,"adjMaxPhysicalArmor":74,"adjDodge":17,"adjPVPDmg":0.04})
    }),
    52013087: _tools.RODict({
        "propID": 52013087,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":54,"adjMaxPhysicalArmor":82,"adjDodge":18,"adjPVPDmg":0.04})
    }),
    52013088: _tools.RODict({
        "propID": 52013088,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":61,"adjMaxPhysicalArmor":89,"adjDodge":20,"adjPVPDmg":0.04})
    }),
    52013089: _tools.RODict({
        "propID": 52013089,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":65,"adjMaxPhysicalArmor":96,"adjDodge":21,"adjPVPDmg":0.04})
    }),
    52013090: _tools.RODict({
        "propID": 52013090,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":74,"adjMaxPhysicalArmor":110,"adjDodge":24,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013091: _tools.RODict({
        "propID": 52013091,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":82,"adjMaxPhysicalArmor":122,"adjDodge":26,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013092: _tools.RODict({
        "propID": 52013092,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":89,"adjMaxPhysicalArmor":134,"adjDodge":28,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013093: _tools.RODict({
        "propID": 52013093,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":98,"adjMaxPhysicalArmor":148,"adjDodge":32,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013094: _tools.RODict({
        "propID": 52013094,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":26,"adjMaxPhysicalArmor":41})
    }),
    52013095: _tools.RODict({
        "propID": 52013095,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":28,"adjMaxPhysicalArmor":44})
    }),
    52013096: _tools.RODict({
        "propID": 52013096,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":30,"adjMaxPhysicalArmor":48})
    }),
    52013097: _tools.RODict({
        "propID": 52013097,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":36,"adjMaxPhysicalArmor":51})
    }),
    52013098: _tools.RODict({
        "propID": 52013098,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":39,"adjMaxPhysicalArmor":56,"adjDodge":14,"adjPVPDmg":0.02})
    }),
    52013099: _tools.RODict({
        "propID": 52013099,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":42,"adjMaxPhysicalArmor":63,"adjDodge":15,"adjPVPDmg":0.02})
    }),
    52013100: _tools.RODict({
        "propID": 52013100,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":45,"adjMaxPhysicalArmor":67,"adjDodge":16,"adjPVPDmg":0.02})
    }),
    52013101: _tools.RODict({
        "propID": 52013101,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":48,"adjMaxPhysicalArmor":72,"adjDodge":17,"adjPVPDmg":0.02})
    }),
    52013102: _tools.RODict({
        "propID": 52013102,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":51,"adjMaxPhysicalArmor":78,"adjDodge":18,"adjPVPDmg":0.04})
    }),
    52013103: _tools.RODict({
        "propID": 52013103,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":57,"adjMaxPhysicalArmor":86,"adjDodge":19,"adjPVPDmg":0.04})
    }),
    52013104: _tools.RODict({
        "propID": 52013104,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":64,"adjMaxPhysicalArmor":93,"adjDodge":21,"adjPVPDmg":0.04})
    }),
    52013105: _tools.RODict({
        "propID": 52013105,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":68,"adjMaxPhysicalArmor":101,"adjDodge":22,"adjPVPDmg":0.04})
    }),
    52013106: _tools.RODict({
        "propID": 52013106,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":78,"adjMaxPhysicalArmor":116,"adjDodge":25,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013107: _tools.RODict({
        "propID": 52013107,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":86,"adjMaxPhysicalArmor":128,"adjDodge":27,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013108: _tools.RODict({
        "propID": 52013108,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":93,"adjMaxPhysicalArmor":141,"adjDodge":29,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013109: _tools.RODict({
        "propID": 52013109,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":103,"adjMaxPhysicalArmor":155,"adjDodge":34,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013110: _tools.RODict({
        "propID": 52013110,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":27,"adjMaxPhysicalArmor":43})
    }),
    52013111: _tools.RODict({
        "propID": 52013111,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":29,"adjMaxPhysicalArmor":46})
    }),
    52013112: _tools.RODict({
        "propID": 52013112,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":32,"adjMaxPhysicalArmor":50})
    }),
    52013113: _tools.RODict({
        "propID": 52013113,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":38,"adjMaxPhysicalArmor":54})
    }),
    52013114: _tools.RODict({
        "propID": 52013114,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":41,"adjMaxPhysicalArmor":59,"adjDodge":15,"adjPVPDmg":0.02})
    }),
    52013115: _tools.RODict({
        "propID": 52013115,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":44,"adjMaxPhysicalArmor":66,"adjDodge":16,"adjPVPDmg":0.02})
    }),
    52013116: _tools.RODict({
        "propID": 52013116,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":47,"adjMaxPhysicalArmor":70,"adjDodge":17,"adjPVPDmg":0.02})
    }),
    52013117: _tools.RODict({
        "propID": 52013117,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":76,"adjDodge":18,"adjPVPDmg":0.02})
    }),
    52013118: _tools.RODict({
        "propID": 52013118,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":54,"adjMaxPhysicalArmor":82,"adjDodge":19,"adjPVPDmg":0.04})
    }),
    52013119: _tools.RODict({
        "propID": 52013119,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":60,"adjMaxPhysicalArmor":90,"adjDodge":20,"adjPVPDmg":0.04})
    }),
    52013120: _tools.RODict({
        "propID": 52013120,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":67,"adjMaxPhysicalArmor":98,"adjDodge":22,"adjPVPDmg":0.04})
    }),
    52013121: _tools.RODict({
        "propID": 52013121,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":71,"adjMaxPhysicalArmor":106,"adjDodge":23,"adjPVPDmg":0.04})
    }),
    52013122: _tools.RODict({
        "propID": 52013122,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":82,"adjMaxPhysicalArmor":122,"adjDodge":26,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013123: _tools.RODict({
        "propID": 52013123,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":90,"adjMaxPhysicalArmor":134,"adjDodge":28,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013124: _tools.RODict({
        "propID": 52013124,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":98,"adjMaxPhysicalArmor":148,"adjDodge":30,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013125: _tools.RODict({
        "propID": 52013125,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":108,"adjMaxPhysicalArmor":163,"adjDodge":36,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013126: _tools.RODict({
        "propID": 52013126,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":28,"adjMaxPhysicalArmor":45})
    }),
    52013127: _tools.RODict({
        "propID": 52013127,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":30,"adjMaxPhysicalArmor":48})
    }),
    52013128: _tools.RODict({
        "propID": 52013128,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":34,"adjMaxPhysicalArmor":53})
    }),
    52013129: _tools.RODict({
        "propID": 52013129,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":40,"adjMaxPhysicalArmor":57})
    }),
    52013130: _tools.RODict({
        "propID": 52013130,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":43,"adjMaxPhysicalArmor":62,"adjDodge":16,"adjPVPDmg":0.02})
    }),
    52013131: _tools.RODict({
        "propID": 52013131,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":46,"adjMaxPhysicalArmor":69,"adjDodge":17,"adjPVPDmg":0.02})
    }),
    52013132: _tools.RODict({
        "propID": 52013132,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":49,"adjMaxPhysicalArmor":74,"adjDodge":18,"adjPVPDmg":0.02})
    }),
    52013133: _tools.RODict({
        "propID": 52013133,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":53,"adjMaxPhysicalArmor":80,"adjDodge":19,"adjPVPDmg":0.02})
    }),
    52013134: _tools.RODict({
        "propID": 52013134,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":57,"adjMaxPhysicalArmor":86,"adjDodge":20,"adjPVPDmg":0.04})
    }),
    52013135: _tools.RODict({
        "propID": 52013135,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":63,"adjMaxPhysicalArmor":95,"adjDodge":21,"adjPVPDmg":0.04})
    }),
    52013136: _tools.RODict({
        "propID": 52013136,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":70,"adjMaxPhysicalArmor":103,"adjDodge":23,"adjPVPDmg":0.04})
    }),
    52013137: _tools.RODict({
        "propID": 52013137,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":75,"adjMaxPhysicalArmor":111,"adjDodge":24,"adjPVPDmg":0.04})
    }),
    52013138: _tools.RODict({
        "propID": 52013138,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":86,"adjMaxPhysicalArmor":128,"adjDodge":27,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013139: _tools.RODict({
        "propID": 52013139,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":95,"adjMaxPhysicalArmor":141,"adjDodge":29,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013140: _tools.RODict({
        "propID": 52013140,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":103,"adjMaxPhysicalArmor":155,"adjDodge":32,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013141: _tools.RODict({
        "propID": 52013141,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":113,"adjMaxPhysicalArmor":171,"adjDodge":38,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013142: _tools.RODict({
        "propID": 52013142,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":29,"adjMaxPhysicalArmor":47})
    }),
    52013143: _tools.RODict({
        "propID": 52013143,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":32,"adjMaxPhysicalArmor":50})
    }),
    52013144: _tools.RODict({
        "propID": 52013144,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":36,"adjMaxPhysicalArmor":56})
    }),
    52013145: _tools.RODict({
        "propID": 52013145,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":42,"adjMaxPhysicalArmor":60})
    }),
    52013146: _tools.RODict({
        "propID": 52013146,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":45,"adjMaxPhysicalArmor":65,"adjDodge":17,"adjPVPDmg":0.02})
    }),
    52013147: _tools.RODict({
        "propID": 52013147,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":48,"adjMaxPhysicalArmor":72,"adjDodge":18,"adjPVPDmg":0.02})
    }),
    52013148: _tools.RODict({
        "propID": 52013148,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":51,"adjMaxPhysicalArmor":78,"adjDodge":19,"adjPVPDmg":0.02})
    }),
    52013149: _tools.RODict({
        "propID": 52013149,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":56,"adjMaxPhysicalArmor":84,"adjDodge":20,"adjPVPDmg":0.02})
    }),
    52013150: _tools.RODict({
        "propID": 52013150,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":60,"adjMaxPhysicalArmor":90,"adjDodge":21,"adjPVPDmg":0.04})
    }),
    52013151: _tools.RODict({
        "propID": 52013151,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":66,"adjMaxPhysicalArmor":100,"adjDodge":22,"adjPVPDmg":0.04})
    }),
    52013152: _tools.RODict({
        "propID": 52013152,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":74,"adjMaxPhysicalArmor":108,"adjDodge":24,"adjPVPDmg":0.04})
    }),
    52013153: _tools.RODict({
        "propID": 52013153,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":79,"adjMaxPhysicalArmor":117,"adjDodge":25,"adjPVPDmg":0.04})
    }),
    52013154: _tools.RODict({
        "propID": 52013154,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":90,"adjMaxPhysicalArmor":134,"adjDodge":28,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013155: _tools.RODict({
        "propID": 52013155,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":100,"adjMaxPhysicalArmor":148,"adjDodge":30,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013156: _tools.RODict({
        "propID": 52013156,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":108,"adjMaxPhysicalArmor":163,"adjDodge":34,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013157: _tools.RODict({
        "propID": 52013157,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":119,"adjMaxPhysicalArmor":180,"adjDodge":40,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013158: _tools.RODict({
        "propID": 52013158,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":30,"adjMaxPhysicalArmor":49})
    }),
    52013159: _tools.RODict({
        "propID": 52013159,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":34,"adjMaxPhysicalArmor":53})
    }),
    52013160: _tools.RODict({
        "propID": 52013160,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":38,"adjMaxPhysicalArmor":59})
    }),
    52013161: _tools.RODict({
        "propID": 52013161,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":44,"adjMaxPhysicalArmor":63})
    }),
    52013162: _tools.RODict({
        "propID": 52013162,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":47,"adjMaxPhysicalArmor":68,"adjDodge":18,"adjPVPDmg":0.02})
    }),
    52013163: _tools.RODict({
        "propID": 52013163,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":50,"adjMaxPhysicalArmor":76,"adjDodge":19,"adjPVPDmg":0.02})
    }),
    52013164: _tools.RODict({
        "propID": 52013164,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":54,"adjMaxPhysicalArmor":82,"adjDodge":20,"adjPVPDmg":0.02})
    }),
    52013165: _tools.RODict({
        "propID": 52013165,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":59,"adjMaxPhysicalArmor":88,"adjDodge":21,"adjPVPDmg":0.02})
    }),
    52013166: _tools.RODict({
        "propID": 52013166,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":63,"adjMaxPhysicalArmor":95,"adjDodge":22,"adjPVPDmg":0.04})
    }),
    52013167: _tools.RODict({
        "propID": 52013167,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":69,"adjMaxPhysicalArmor":105,"adjDodge":23,"adjPVPDmg":0.04})
    }),
    52013168: _tools.RODict({
        "propID": 52013168,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":78,"adjMaxPhysicalArmor":113,"adjDodge":25,"adjPVPDmg":0.04})
    }),
    52013169: _tools.RODict({
        "propID": 52013169,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":83,"adjMaxPhysicalArmor":123,"adjDodge":26,"adjPVPDmg":0.04})
    }),
    52013170: _tools.RODict({
        "propID": 52013170,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":95,"adjMaxPhysicalArmor":141,"adjDodge":29,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013171: _tools.RODict({
        "propID": 52013171,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":105,"adjMaxPhysicalArmor":155,"adjDodge":32,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013172: _tools.RODict({
        "propID": 52013172,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":113,"adjMaxPhysicalArmor":171,"adjDodge":36,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013173: _tools.RODict({
        "propID": 52013173,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":125,"adjMaxPhysicalArmor":189,"adjDodge":42,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013174: _tools.RODict({
        "propID": 52013174,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":32,"adjMaxPhysicalArmor":51})
    }),
    52013175: _tools.RODict({
        "propID": 52013175,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":36,"adjMaxPhysicalArmor":56})
    }),
    52013176: _tools.RODict({
        "propID": 52013176,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":40,"adjMaxPhysicalArmor":62})
    }),
    52013177: _tools.RODict({
        "propID": 52013177,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":46,"adjMaxPhysicalArmor":66})
    }),
    52013178: _tools.RODict({
        "propID": 52013178,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":49,"adjMaxPhysicalArmor":71,"adjDodge":19,"adjPVPDmg":0.02})
    }),
    52013179: _tools.RODict({
        "propID": 52013179,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":53,"adjMaxPhysicalArmor":80,"adjDodge":20,"adjPVPDmg":0.02})
    }),
    52013180: _tools.RODict({
        "propID": 52013180,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":57,"adjMaxPhysicalArmor":86,"adjDodge":21,"adjPVPDmg":0.02})
    }),
    52013181: _tools.RODict({
        "propID": 52013181,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":62,"adjMaxPhysicalArmor":92,"adjDodge":22,"adjPVPDmg":0.02})
    }),
    52013182: _tools.RODict({
        "propID": 52013182,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":66,"adjMaxPhysicalArmor":100,"adjDodge":23,"adjPVPDmg":0.04})
    }),
    52013183: _tools.RODict({
        "propID": 52013183,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":72,"adjMaxPhysicalArmor":110,"adjDodge":24,"adjPVPDmg":0.04})
    }),
    52013184: _tools.RODict({
        "propID": 52013184,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":82,"adjMaxPhysicalArmor":119,"adjDodge":26,"adjPVPDmg":0.04})
    }),
    52013185: _tools.RODict({
        "propID": 52013185,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":87,"adjMaxPhysicalArmor":129,"adjDodge":27,"adjPVPDmg":0.04})
    }),
    52013186: _tools.RODict({
        "propID": 52013186,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":100,"adjMaxPhysicalArmor":148,"adjDodge":30,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013187: _tools.RODict({
        "propID": 52013187,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":110,"adjMaxPhysicalArmor":163,"adjDodge":34,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013188: _tools.RODict({
        "propID": 52013188,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":119,"adjMaxPhysicalArmor":180,"adjDodge":38,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013189: _tools.RODict({
        "propID": 52013189,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":131,"adjMaxPhysicalArmor":198,"adjDodge":44,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013190: _tools.RODict({
        "propID": 52013190,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":34,"adjMaxPhysicalArmor":54})
    }),
    52013191: _tools.RODict({
        "propID": 52013191,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":38,"adjMaxPhysicalArmor":59})
    }),
    52013192: _tools.RODict({
        "propID": 52013192,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":42,"adjMaxPhysicalArmor":65})
    }),
    52013193: _tools.RODict({
        "propID": 52013193,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":48,"adjMaxPhysicalArmor":69})
    }),
    52013194: _tools.RODict({
        "propID": 52013194,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":51,"adjMaxPhysicalArmor":75,"adjDodge":20,"adjPVPDmg":0.02})
    }),
    52013195: _tools.RODict({
        "propID": 52013195,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":56,"adjMaxPhysicalArmor":84,"adjDodge":21,"adjPVPDmg":0.02})
    }),
    52013196: _tools.RODict({
        "propID": 52013196,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":60,"adjMaxPhysicalArmor":90,"adjDodge":22,"adjPVPDmg":0.02})
    }),
    52013197: _tools.RODict({
        "propID": 52013197,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":65,"adjMaxPhysicalArmor":97,"adjDodge":23,"adjPVPDmg":0.02})
    }),
    52013198: _tools.RODict({
        "propID": 52013198,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":69,"adjMaxPhysicalArmor":105,"adjDodge":24,"adjPVPDmg":0.04})
    }),
    52013199: _tools.RODict({
        "propID": 52013199,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":76,"adjMaxPhysicalArmor":116,"adjDodge":25,"adjPVPDmg":0.04})
    }),
    52013200: _tools.RODict({
        "propID": 52013200,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":86,"adjMaxPhysicalArmor":125,"adjDodge":27,"adjPVPDmg":0.04})
    }),
    52013201: _tools.RODict({
        "propID": 52013201,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":91,"adjMaxPhysicalArmor":135,"adjDodge":28,"adjPVPDmg":0.04})
    }),
    52013202: _tools.RODict({
        "propID": 52013202,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":105,"adjMaxPhysicalArmor":155,"adjDodge":32,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013203: _tools.RODict({
        "propID": 52013203,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":116,"adjMaxPhysicalArmor":171,"adjDodge":36,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013204: _tools.RODict({
        "propID": 52013204,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":125,"adjMaxPhysicalArmor":189,"adjDodge":40,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
    }),
    52013205: _tools.RODict({
        "propID": 52013205,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalArmor":138,"adjMaxPhysicalArmor":208,"adjDodge":46,"adjPVPDmg":0.04,"adjPVPDmgAnti":0.04})
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
    52013222: _tools.RODict({
        "propID": 52013222,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":15,"adjMaxPhysicalAtk":32})
    }),
    52013223: _tools.RODict({
        "propID": 52013223,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":16,"adjMaxPhysicalAtk":35})
    }),
    52013224: _tools.RODict({
        "propID": 52013224,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":18,"adjMaxPhysicalAtk":38})
    }),
    52013225: _tools.RODict({
        "propID": 52013225,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":19,"adjMaxPhysicalAtk":41})
    }),
    52013226: _tools.RODict({
        "propID": 52013226,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":44,"adjFatal":11,"adjIgnoreArmor":0.04})
    }),
    52013227: _tools.RODict({
        "propID": 52013227,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":48,"adjFatal":12,"adjIgnoreArmor":0.04})
    }),
    52013228: _tools.RODict({
        "propID": 52013228,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":53,"adjFatal":13,"adjIgnoreArmor":0.04})
    }),
    52013229: _tools.RODict({
        "propID": 52013229,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":27,"adjMaxPhysicalAtk":58,"adjFatal":14,"adjIgnoreArmor":0.04})
    }),
    52013230: _tools.RODict({
        "propID": 52013230,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":29,"adjMaxPhysicalAtk":62,"adjFatal":15,"adjIgnoreArmor":0.08})
    }),
    52013231: _tools.RODict({
        "propID": 52013231,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":33,"adjMaxPhysicalAtk":68,"adjFatal":16,"adjIgnoreArmor":0.08})
    }),
    52013232: _tools.RODict({
        "propID": 52013232,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":36,"adjMaxPhysicalAtk":75,"adjFatal":18,"adjIgnoreArmor":0.08})
    }),
    52013233: _tools.RODict({
        "propID": 52013233,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":38,"adjMaxPhysicalAtk":81,"adjFatal":19,"adjIgnoreArmor":0.08})
    }),
    52013234: _tools.RODict({
        "propID": 52013234,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":43,"adjMaxPhysicalAtk":93,"adjFatal":22,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013235: _tools.RODict({
        "propID": 52013235,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":47,"adjMaxPhysicalAtk":103,"adjFatal":24,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013236: _tools.RODict({
        "propID": 52013236,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":53,"adjMaxPhysicalAtk":113,"adjFatal":26,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013237: _tools.RODict({
        "propID": 52013237,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":58,"adjMaxPhysicalAtk":125,"adjFatal":29,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013238: _tools.RODict({
        "propID": 52013238,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":16,"adjMaxPhysicalAtk":34})
    }),
    52013239: _tools.RODict({
        "propID": 52013239,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":37})
    }),
    52013240: _tools.RODict({
        "propID": 52013240,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":19,"adjMaxPhysicalAtk":40})
    }),
    52013241: _tools.RODict({
        "propID": 52013241,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":43})
    }),
    52013242: _tools.RODict({
        "propID": 52013242,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":46,"adjFatal":12,"adjIgnoreArmor":0.04})
    }),
    52013243: _tools.RODict({
        "propID": 52013243,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":50,"adjFatal":13,"adjIgnoreArmor":0.04})
    }),
    52013244: _tools.RODict({
        "propID": 52013244,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":56,"adjFatal":14,"adjIgnoreArmor":0.04})
    }),
    52013245: _tools.RODict({
        "propID": 52013245,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":28,"adjMaxPhysicalAtk":61,"adjFatal":15,"adjIgnoreArmor":0.04})
    }),
    52013246: _tools.RODict({
        "propID": 52013246,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":65,"adjFatal":16,"adjIgnoreArmor":0.08})
    }),
    52013247: _tools.RODict({
        "propID": 52013247,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":35,"adjMaxPhysicalAtk":71,"adjFatal":17,"adjIgnoreArmor":0.08})
    }),
    52013248: _tools.RODict({
        "propID": 52013248,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":38,"adjMaxPhysicalAtk":79,"adjFatal":19,"adjIgnoreArmor":0.08})
    }),
    52013249: _tools.RODict({
        "propID": 52013249,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":40,"adjMaxPhysicalAtk":85,"adjFatal":20,"adjIgnoreArmor":0.08})
    }),
    52013250: _tools.RODict({
        "propID": 52013250,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":45,"adjMaxPhysicalAtk":98,"adjFatal":23,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013251: _tools.RODict({
        "propID": 52013251,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":49,"adjMaxPhysicalAtk":108,"adjFatal":25,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013252: _tools.RODict({
        "propID": 52013252,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":56,"adjMaxPhysicalAtk":119,"adjFatal":27,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013253: _tools.RODict({
        "propID": 52013253,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":61,"adjMaxPhysicalAtk":131,"adjFatal":30,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013254: _tools.RODict({
        "propID": 52013254,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":36})
    }),
    52013255: _tools.RODict({
        "propID": 52013255,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":18,"adjMaxPhysicalAtk":39})
    }),
    52013256: _tools.RODict({
        "propID": 52013256,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":42})
    }),
    52013257: _tools.RODict({
        "propID": 52013257,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":45})
    }),
    52013258: _tools.RODict({
        "propID": 52013258,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":48,"adjFatal":13,"adjIgnoreArmor":0.04})
    }),
    52013259: _tools.RODict({
        "propID": 52013259,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":53,"adjFatal":14,"adjIgnoreArmor":0.04})
    }),
    52013260: _tools.RODict({
        "propID": 52013260,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":27,"adjMaxPhysicalAtk":59,"adjFatal":15,"adjIgnoreArmor":0.04})
    }),
    52013261: _tools.RODict({
        "propID": 52013261,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":29,"adjMaxPhysicalAtk":64,"adjFatal":16,"adjIgnoreArmor":0.04})
    }),
    52013262: _tools.RODict({
        "propID": 52013262,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":68,"adjFatal":17,"adjIgnoreArmor":0.08})
    }),
    52013263: _tools.RODict({
        "propID": 52013263,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":37,"adjMaxPhysicalAtk":75,"adjFatal":18,"adjIgnoreArmor":0.08})
    }),
    52013264: _tools.RODict({
        "propID": 52013264,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":40,"adjMaxPhysicalAtk":83,"adjFatal":20,"adjIgnoreArmor":0.08})
    }),
    52013265: _tools.RODict({
        "propID": 52013265,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":42,"adjMaxPhysicalAtk":89,"adjFatal":21,"adjIgnoreArmor":0.08})
    }),
    52013266: _tools.RODict({
        "propID": 52013266,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":47,"adjMaxPhysicalAtk":103,"adjFatal":24,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013267: _tools.RODict({
        "propID": 52013267,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":51,"adjMaxPhysicalAtk":113,"adjFatal":26,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013268: _tools.RODict({
        "propID": 52013268,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":59,"adjMaxPhysicalAtk":125,"adjFatal":28,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013269: _tools.RODict({
        "propID": 52013269,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":64,"adjMaxPhysicalAtk":138,"adjFatal":32,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013270: _tools.RODict({
        "propID": 52013270,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":18,"adjMaxPhysicalAtk":38})
    }),
    52013271: _tools.RODict({
        "propID": 52013271,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":19,"adjMaxPhysicalAtk":41})
    }),
    52013272: _tools.RODict({
        "propID": 52013272,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":44})
    }),
    52013273: _tools.RODict({
        "propID": 52013273,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":47})
    }),
    52013274: _tools.RODict({
        "propID": 52013274,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":50,"adjFatal":14,"adjIgnoreArmor":0.04})
    }),
    52013275: _tools.RODict({
        "propID": 52013275,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":56,"adjFatal":15,"adjIgnoreArmor":0.04})
    }),
    52013276: _tools.RODict({
        "propID": 52013276,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":28,"adjMaxPhysicalAtk":62,"adjFatal":16,"adjIgnoreArmor":0.04})
    }),
    52013277: _tools.RODict({
        "propID": 52013277,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":67,"adjFatal":17,"adjIgnoreArmor":0.04})
    }),
    52013278: _tools.RODict({
        "propID": 52013278,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":34,"adjMaxPhysicalAtk":71,"adjFatal":18,"adjIgnoreArmor":0.08})
    }),
    52013279: _tools.RODict({
        "propID": 52013279,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":39,"adjMaxPhysicalAtk":79,"adjFatal":19,"adjIgnoreArmor":0.08})
    }),
    52013280: _tools.RODict({
        "propID": 52013280,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":42,"adjMaxPhysicalAtk":87,"adjFatal":21,"adjIgnoreArmor":0.08})
    }),
    52013281: _tools.RODict({
        "propID": 52013281,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":44,"adjMaxPhysicalAtk":93,"adjFatal":22,"adjIgnoreArmor":0.08})
    }),
    52013282: _tools.RODict({
        "propID": 52013282,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":49,"adjMaxPhysicalAtk":108,"adjFatal":25,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013283: _tools.RODict({
        "propID": 52013283,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":54,"adjMaxPhysicalAtk":119,"adjFatal":27,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013284: _tools.RODict({
        "propID": 52013284,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":62,"adjMaxPhysicalAtk":131,"adjFatal":29,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013285: _tools.RODict({
        "propID": 52013285,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":67,"adjMaxPhysicalAtk":145,"adjFatal":34,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013286: _tools.RODict({
        "propID": 52013286,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":19,"adjMaxPhysicalAtk":40})
    }),
    52013287: _tools.RODict({
        "propID": 52013287,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":43})
    }),
    52013288: _tools.RODict({
        "propID": 52013288,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":46})
    }),
    52013289: _tools.RODict({
        "propID": 52013289,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":49})
    }),
    52013290: _tools.RODict({
        "propID": 52013290,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":53,"adjFatal":15,"adjIgnoreArmor":0.04})
    }),
    52013291: _tools.RODict({
        "propID": 52013291,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":27,"adjMaxPhysicalAtk":59,"adjFatal":16,"adjIgnoreArmor":0.04})
    }),
    52013292: _tools.RODict({
        "propID": 52013292,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":29,"adjMaxPhysicalAtk":65,"adjFatal":17,"adjIgnoreArmor":0.04})
    }),
    52013293: _tools.RODict({
        "propID": 52013293,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":70,"adjFatal":18,"adjIgnoreArmor":0.04})
    }),
    52013294: _tools.RODict({
        "propID": 52013294,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":36,"adjMaxPhysicalAtk":75,"adjFatal":19,"adjIgnoreArmor":0.08})
    }),
    52013295: _tools.RODict({
        "propID": 52013295,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":41,"adjMaxPhysicalAtk":83,"adjFatal":20,"adjIgnoreArmor":0.08})
    }),
    52013296: _tools.RODict({
        "propID": 52013296,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":44,"adjMaxPhysicalAtk":91,"adjFatal":22,"adjIgnoreArmor":0.08})
    }),
    52013297: _tools.RODict({
        "propID": 52013297,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":46,"adjMaxPhysicalAtk":98,"adjFatal":23,"adjIgnoreArmor":0.08})
    }),
    52013298: _tools.RODict({
        "propID": 52013298,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":51,"adjMaxPhysicalAtk":113,"adjFatal":26,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013299: _tools.RODict({
        "propID": 52013299,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":57,"adjMaxPhysicalAtk":125,"adjFatal":28,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013300: _tools.RODict({
        "propID": 52013300,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":65,"adjMaxPhysicalAtk":138,"adjFatal":30,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013301: _tools.RODict({
        "propID": 52013301,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":70,"adjMaxPhysicalAtk":152,"adjFatal":36,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013302: _tools.RODict({
        "propID": 52013302,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":42})
    }),
    52013303: _tools.RODict({
        "propID": 52013303,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":45})
    }),
    52013304: _tools.RODict({
        "propID": 52013304,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":48})
    }),
    52013305: _tools.RODict({
        "propID": 52013305,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":51})
    }),
    52013306: _tools.RODict({
        "propID": 52013306,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":56,"adjFatal":16,"adjIgnoreArmor":0.04})
    }),
    52013307: _tools.RODict({
        "propID": 52013307,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":28,"adjMaxPhysicalAtk":62,"adjFatal":17,"adjIgnoreArmor":0.04})
    }),
    52013308: _tools.RODict({
        "propID": 52013308,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":68,"adjFatal":18,"adjIgnoreArmor":0.04})
    }),
    52013309: _tools.RODict({
        "propID": 52013309,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":34,"adjMaxPhysicalAtk":74,"adjFatal":19,"adjIgnoreArmor":0.04})
    }),
    52013310: _tools.RODict({
        "propID": 52013310,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":38,"adjMaxPhysicalAtk":79,"adjFatal":20,"adjIgnoreArmor":0.08})
    }),
    52013311: _tools.RODict({
        "propID": 52013311,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":43,"adjMaxPhysicalAtk":87,"adjFatal":21,"adjIgnoreArmor":0.08})
    }),
    52013312: _tools.RODict({
        "propID": 52013312,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":46,"adjMaxPhysicalAtk":96,"adjFatal":23,"adjIgnoreArmor":0.08})
    }),
    52013313: _tools.RODict({
        "propID": 52013313,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":48,"adjMaxPhysicalAtk":103,"adjFatal":24,"adjIgnoreArmor":0.08})
    }),
    52013314: _tools.RODict({
        "propID": 52013314,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":54,"adjMaxPhysicalAtk":119,"adjFatal":27,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013315: _tools.RODict({
        "propID": 52013315,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":60,"adjMaxPhysicalAtk":131,"adjFatal":29,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013316: _tools.RODict({
        "propID": 52013316,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":68,"adjMaxPhysicalAtk":145,"adjFatal":32,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013317: _tools.RODict({
        "propID": 52013317,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":74,"adjMaxPhysicalAtk":160,"adjFatal":38,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013318: _tools.RODict({
        "propID": 52013318,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":44})
    }),
    52013319: _tools.RODict({
        "propID": 52013319,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":47})
    }),
    52013320: _tools.RODict({
        "propID": 52013320,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":50})
    }),
    52013321: _tools.RODict({
        "propID": 52013321,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":54})
    }),
    52013322: _tools.RODict({
        "propID": 52013322,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":27,"adjMaxPhysicalAtk":59,"adjFatal":17,"adjIgnoreArmor":0.04})
    }),
    52013323: _tools.RODict({
        "propID": 52013323,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":29,"adjMaxPhysicalAtk":65,"adjFatal":18,"adjIgnoreArmor":0.04})
    }),
    52013324: _tools.RODict({
        "propID": 52013324,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":71,"adjFatal":19,"adjIgnoreArmor":0.04})
    }),
    52013325: _tools.RODict({
        "propID": 52013325,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":36,"adjMaxPhysicalAtk":78,"adjFatal":20,"adjIgnoreArmor":0.04})
    }),
    52013326: _tools.RODict({
        "propID": 52013326,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":40,"adjMaxPhysicalAtk":83,"adjFatal":21,"adjIgnoreArmor":0.08})
    }),
    52013327: _tools.RODict({
        "propID": 52013327,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":45,"adjMaxPhysicalAtk":91,"adjFatal":22,"adjIgnoreArmor":0.08})
    }),
    52013328: _tools.RODict({
        "propID": 52013328,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":48,"adjMaxPhysicalAtk":101,"adjFatal":24,"adjIgnoreArmor":0.08})
    }),
    52013329: _tools.RODict({
        "propID": 52013329,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":50,"adjMaxPhysicalAtk":108,"adjFatal":25,"adjIgnoreArmor":0.08})
    }),
    52013330: _tools.RODict({
        "propID": 52013330,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":57,"adjMaxPhysicalAtk":125,"adjFatal":28,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013331: _tools.RODict({
        "propID": 52013331,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":63,"adjMaxPhysicalAtk":138,"adjFatal":30,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013332: _tools.RODict({
        "propID": 52013332,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":71,"adjMaxPhysicalAtk":152,"adjFatal":34,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013333: _tools.RODict({
        "propID": 52013333,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":78,"adjMaxPhysicalAtk":168,"adjFatal":40,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013334: _tools.RODict({
        "propID": 52013334,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":46})
    }),
    52013335: _tools.RODict({
        "propID": 52013335,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":49})
    }),
    52013336: _tools.RODict({
        "propID": 52013336,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":53})
    }),
    52013337: _tools.RODict({
        "propID": 52013337,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":57})
    }),
    52013338: _tools.RODict({
        "propID": 52013338,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":28,"adjMaxPhysicalAtk":62,"adjFatal":18,"adjIgnoreArmor":0.04})
    }),
    52013339: _tools.RODict({
        "propID": 52013339,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":68,"adjFatal":19,"adjIgnoreArmor":0.04})
    }),
    52013340: _tools.RODict({
        "propID": 52013340,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":34,"adjMaxPhysicalAtk":75,"adjFatal":20,"adjIgnoreArmor":0.04})
    }),
    52013341: _tools.RODict({
        "propID": 52013341,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":38,"adjMaxPhysicalAtk":82,"adjFatal":21,"adjIgnoreArmor":0.04})
    }),
    52013342: _tools.RODict({
        "propID": 52013342,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":42,"adjMaxPhysicalAtk":87,"adjFatal":22,"adjIgnoreArmor":0.08})
    }),
    52013343: _tools.RODict({
        "propID": 52013343,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":47,"adjMaxPhysicalAtk":96,"adjFatal":23,"adjIgnoreArmor":0.08})
    }),
    52013344: _tools.RODict({
        "propID": 52013344,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":50,"adjMaxPhysicalAtk":106,"adjFatal":25,"adjIgnoreArmor":0.08})
    }),
    52013345: _tools.RODict({
        "propID": 52013345,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":53,"adjMaxPhysicalAtk":113,"adjFatal":26,"adjIgnoreArmor":0.08})
    }),
    52013346: _tools.RODict({
        "propID": 52013346,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":60,"adjMaxPhysicalAtk":131,"adjFatal":29,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013347: _tools.RODict({
        "propID": 52013347,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":66,"adjMaxPhysicalAtk":145,"adjFatal":32,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013348: _tools.RODict({
        "propID": 52013348,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":75,"adjMaxPhysicalAtk":160,"adjFatal":36,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013349: _tools.RODict({
        "propID": 52013349,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":82,"adjMaxPhysicalAtk":176,"adjFatal":42,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013350: _tools.RODict({
        "propID": 52013350,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":48})
    }),
    52013351: _tools.RODict({
        "propID": 52013351,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":51})
    }),
    52013352: _tools.RODict({
        "propID": 52013352,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":56})
    }),
    52013353: _tools.RODict({
        "propID": 52013353,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":27,"adjMaxPhysicalAtk":60})
    }),
    52013354: _tools.RODict({
        "propID": 52013354,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":29,"adjMaxPhysicalAtk":65,"adjFatal":19,"adjIgnoreArmor":0.04})
    }),
    52013355: _tools.RODict({
        "propID": 52013355,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":71,"adjFatal":20,"adjIgnoreArmor":0.04})
    }),
    52013356: _tools.RODict({
        "propID": 52013356,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":36,"adjMaxPhysicalAtk":79,"adjFatal":21,"adjIgnoreArmor":0.04})
    }),
    52013357: _tools.RODict({
        "propID": 52013357,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":40,"adjMaxPhysicalAtk":86,"adjFatal":22,"adjIgnoreArmor":0.04})
    }),
    52013358: _tools.RODict({
        "propID": 52013358,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":44,"adjMaxPhysicalAtk":91,"adjFatal":23,"adjIgnoreArmor":0.08})
    }),
    52013359: _tools.RODict({
        "propID": 52013359,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":49,"adjMaxPhysicalAtk":101,"adjFatal":24,"adjIgnoreArmor":0.08})
    }),
    52013360: _tools.RODict({
        "propID": 52013360,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":53,"adjMaxPhysicalAtk":111,"adjFatal":26,"adjIgnoreArmor":0.08})
    }),
    52013361: _tools.RODict({
        "propID": 52013361,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":56,"adjMaxPhysicalAtk":119,"adjFatal":27,"adjIgnoreArmor":0.08})
    }),
    52013362: _tools.RODict({
        "propID": 52013362,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":63,"adjMaxPhysicalAtk":138,"adjFatal":30,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013363: _tools.RODict({
        "propID": 52013363,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":69,"adjMaxPhysicalAtk":152,"adjFatal":34,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013364: _tools.RODict({
        "propID": 52013364,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":79,"adjMaxPhysicalAtk":168,"adjFatal":38,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013365: _tools.RODict({
        "propID": 52013365,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":86,"adjMaxPhysicalAtk":185,"adjFatal":44,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013366: _tools.RODict({
        "propID": 52013366,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":50})
    }),
    52013367: _tools.RODict({
        "propID": 52013367,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":54})
    }),
    52013368: _tools.RODict({
        "propID": 52013368,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":27,"adjMaxPhysicalAtk":59})
    }),
    52013369: _tools.RODict({
        "propID": 52013369,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":28,"adjMaxPhysicalAtk":63})
    }),
    52013370: _tools.RODict({
        "propID": 52013370,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":68,"adjFatal":20,"adjIgnoreArmor":0.04})
    }),
    52013371: _tools.RODict({
        "propID": 52013371,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":34,"adjMaxPhysicalAtk":75,"adjFatal":21,"adjIgnoreArmor":0.04})
    }),
    52013372: _tools.RODict({
        "propID": 52013372,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":38,"adjMaxPhysicalAtk":83,"adjFatal":22,"adjIgnoreArmor":0.04})
    }),
    52013373: _tools.RODict({
        "propID": 52013373,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":42,"adjMaxPhysicalAtk":90,"adjFatal":23,"adjIgnoreArmor":0.04})
    }),
    52013374: _tools.RODict({
        "propID": 52013374,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":46,"adjMaxPhysicalAtk":96,"adjFatal":24,"adjIgnoreArmor":0.08})
    }),
    52013375: _tools.RODict({
        "propID": 52013375,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":51,"adjMaxPhysicalAtk":106,"adjFatal":25,"adjIgnoreArmor":0.08})
    }),
    52013376: _tools.RODict({
        "propID": 52013376,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":56,"adjMaxPhysicalAtk":117,"adjFatal":27,"adjIgnoreArmor":0.08})
    }),
    52013377: _tools.RODict({
        "propID": 52013377,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":59,"adjMaxPhysicalAtk":125,"adjFatal":28,"adjIgnoreArmor":0.08})
    }),
    52013378: _tools.RODict({
        "propID": 52013378,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":66,"adjMaxPhysicalAtk":145,"adjFatal":32,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013379: _tools.RODict({
        "propID": 52013379,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":72,"adjMaxPhysicalAtk":160,"adjFatal":36,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013380: _tools.RODict({
        "propID": 52013380,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":83,"adjMaxPhysicalAtk":176,"adjFatal":40,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013381: _tools.RODict({
        "propID": 52013381,
        "type": 2,
        "propList": _tools.RODict({"adjMinPhysicalAtk":90,"adjMaxPhysicalAtk":194,"adjFatal":46,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
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
    52013398: _tools.RODict({
        "propID": 52013398,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":15,"adjMaxMagicAtk":32})
    }),
    52013399: _tools.RODict({
        "propID": 52013399,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":16,"adjMaxMagicAtk":35})
    }),
    52013400: _tools.RODict({
        "propID": 52013400,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":18,"adjMaxMagicAtk":38})
    }),
    52013401: _tools.RODict({
        "propID": 52013401,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":19,"adjMaxMagicAtk":41})
    }),
    52013402: _tools.RODict({
        "propID": 52013402,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":21,"adjMaxMagicAtk":44,"adjFatal":11,"adjIgnoreArmor":0.04})
    }),
    52013403: _tools.RODict({
        "propID": 52013403,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":23,"adjMaxMagicAtk":48,"adjFatal":12,"adjIgnoreArmor":0.04})
    }),
    52013404: _tools.RODict({
        "propID": 52013404,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":25,"adjMaxMagicAtk":53,"adjFatal":13,"adjIgnoreArmor":0.04})
    }),
    52013405: _tools.RODict({
        "propID": 52013405,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":27,"adjMaxMagicAtk":58,"adjFatal":14,"adjIgnoreArmor":0.04})
    }),
    52013406: _tools.RODict({
        "propID": 52013406,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":29,"adjMaxMagicAtk":62,"adjFatal":15,"adjIgnoreArmor":0.08})
    }),
    52013407: _tools.RODict({
        "propID": 52013407,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":33,"adjMaxMagicAtk":68,"adjFatal":16,"adjIgnoreArmor":0.08})
    }),
    52013408: _tools.RODict({
        "propID": 52013408,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":36,"adjMaxMagicAtk":75,"adjFatal":18,"adjIgnoreArmor":0.08})
    }),
    52013409: _tools.RODict({
        "propID": 52013409,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":38,"adjMaxMagicAtk":81,"adjFatal":19,"adjIgnoreArmor":0.08})
    }),
    52013410: _tools.RODict({
        "propID": 52013410,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":43,"adjMaxMagicAtk":93,"adjFatal":22,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013411: _tools.RODict({
        "propID": 52013411,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":47,"adjMaxMagicAtk":103,"adjFatal":24,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013412: _tools.RODict({
        "propID": 52013412,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":53,"adjMaxMagicAtk":113,"adjFatal":26,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013413: _tools.RODict({
        "propID": 52013413,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":58,"adjMaxMagicAtk":125,"adjFatal":29,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013414: _tools.RODict({
        "propID": 52013414,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":16,"adjMaxMagicAtk":34})
    }),
    52013415: _tools.RODict({
        "propID": 52013415,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":17,"adjMaxMagicAtk":37})
    }),
    52013416: _tools.RODict({
        "propID": 52013416,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":19,"adjMaxMagicAtk":40})
    }),
    52013417: _tools.RODict({
        "propID": 52013417,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":20,"adjMaxMagicAtk":43})
    }),
    52013418: _tools.RODict({
        "propID": 52013418,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":22,"adjMaxMagicAtk":46,"adjFatal":12,"adjIgnoreArmor":0.04})
    }),
    52013419: _tools.RODict({
        "propID": 52013419,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":24,"adjMaxMagicAtk":50,"adjFatal":13,"adjIgnoreArmor":0.04})
    }),
    52013420: _tools.RODict({
        "propID": 52013420,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":26,"adjMaxMagicAtk":56,"adjFatal":14,"adjIgnoreArmor":0.04})
    }),
    52013421: _tools.RODict({
        "propID": 52013421,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":28,"adjMaxMagicAtk":61,"adjFatal":15,"adjIgnoreArmor":0.04})
    }),
    52013422: _tools.RODict({
        "propID": 52013422,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":30,"adjMaxMagicAtk":65,"adjFatal":16,"adjIgnoreArmor":0.08})
    }),
    52013423: _tools.RODict({
        "propID": 52013423,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":35,"adjMaxMagicAtk":71,"adjFatal":17,"adjIgnoreArmor":0.08})
    }),
    52013424: _tools.RODict({
        "propID": 52013424,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":38,"adjMaxMagicAtk":79,"adjFatal":19,"adjIgnoreArmor":0.08})
    }),
    52013425: _tools.RODict({
        "propID": 52013425,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":40,"adjMaxMagicAtk":85,"adjFatal":20,"adjIgnoreArmor":0.08})
    }),
    52013426: _tools.RODict({
        "propID": 52013426,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":45,"adjMaxMagicAtk":98,"adjFatal":23,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013427: _tools.RODict({
        "propID": 52013427,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":49,"adjMaxMagicAtk":108,"adjFatal":25,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013428: _tools.RODict({
        "propID": 52013428,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":56,"adjMaxMagicAtk":119,"adjFatal":27,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013429: _tools.RODict({
        "propID": 52013429,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":61,"adjMaxMagicAtk":131,"adjFatal":30,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013430: _tools.RODict({
        "propID": 52013430,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":17,"adjMaxMagicAtk":36})
    }),
    52013431: _tools.RODict({
        "propID": 52013431,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":18,"adjMaxMagicAtk":39})
    }),
    52013432: _tools.RODict({
        "propID": 52013432,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":20,"adjMaxMagicAtk":42})
    }),
    52013433: _tools.RODict({
        "propID": 52013433,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":21,"adjMaxMagicAtk":45})
    }),
    52013434: _tools.RODict({
        "propID": 52013434,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":23,"adjMaxMagicAtk":48,"adjFatal":13,"adjIgnoreArmor":0.04})
    }),
    52013435: _tools.RODict({
        "propID": 52013435,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":25,"adjMaxMagicAtk":53,"adjFatal":14,"adjIgnoreArmor":0.04})
    }),
    52013436: _tools.RODict({
        "propID": 52013436,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":27,"adjMaxMagicAtk":59,"adjFatal":15,"adjIgnoreArmor":0.04})
    }),
    52013437: _tools.RODict({
        "propID": 52013437,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":29,"adjMaxMagicAtk":64,"adjFatal":16,"adjIgnoreArmor":0.04})
    }),
    52013438: _tools.RODict({
        "propID": 52013438,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":32,"adjMaxMagicAtk":68,"adjFatal":17,"adjIgnoreArmor":0.08})
    }),
    52013439: _tools.RODict({
        "propID": 52013439,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":37,"adjMaxMagicAtk":75,"adjFatal":18,"adjIgnoreArmor":0.08})
    }),
    52013440: _tools.RODict({
        "propID": 52013440,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":40,"adjMaxMagicAtk":83,"adjFatal":20,"adjIgnoreArmor":0.08})
    }),
    52013441: _tools.RODict({
        "propID": 52013441,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":42,"adjMaxMagicAtk":89,"adjFatal":21,"adjIgnoreArmor":0.08})
    }),
    52013442: _tools.RODict({
        "propID": 52013442,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":47,"adjMaxMagicAtk":103,"adjFatal":24,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013443: _tools.RODict({
        "propID": 52013443,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":51,"adjMaxMagicAtk":113,"adjFatal":26,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013444: _tools.RODict({
        "propID": 52013444,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":59,"adjMaxMagicAtk":125,"adjFatal":28,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013445: _tools.RODict({
        "propID": 52013445,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":64,"adjMaxMagicAtk":138,"adjFatal":32,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013446: _tools.RODict({
        "propID": 52013446,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":18,"adjMaxMagicAtk":38})
    }),
    52013447: _tools.RODict({
        "propID": 52013447,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":19,"adjMaxMagicAtk":41})
    }),
    52013448: _tools.RODict({
        "propID": 52013448,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":21,"adjMaxMagicAtk":44})
    }),
    52013449: _tools.RODict({
        "propID": 52013449,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":22,"adjMaxMagicAtk":47})
    }),
    52013450: _tools.RODict({
        "propID": 52013450,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":24,"adjMaxMagicAtk":50,"adjFatal":14,"adjIgnoreArmor":0.04})
    }),
    52013451: _tools.RODict({
        "propID": 52013451,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":26,"adjMaxMagicAtk":56,"adjFatal":15,"adjIgnoreArmor":0.04})
    }),
    52013452: _tools.RODict({
        "propID": 52013452,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":28,"adjMaxMagicAtk":62,"adjFatal":16,"adjIgnoreArmor":0.04})
    }),
    52013453: _tools.RODict({
        "propID": 52013453,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":30,"adjMaxMagicAtk":67,"adjFatal":17,"adjIgnoreArmor":0.04})
    }),
    52013454: _tools.RODict({
        "propID": 52013454,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":34,"adjMaxMagicAtk":71,"adjFatal":18,"adjIgnoreArmor":0.08})
    }),
    52013455: _tools.RODict({
        "propID": 52013455,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":39,"adjMaxMagicAtk":79,"adjFatal":19,"adjIgnoreArmor":0.08})
    }),
    52013456: _tools.RODict({
        "propID": 52013456,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":42,"adjMaxMagicAtk":87,"adjFatal":21,"adjIgnoreArmor":0.08})
    }),
    52013457: _tools.RODict({
        "propID": 52013457,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":44,"adjMaxMagicAtk":93,"adjFatal":22,"adjIgnoreArmor":0.08})
    }),
    52013458: _tools.RODict({
        "propID": 52013458,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":49,"adjMaxMagicAtk":108,"adjFatal":25,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013459: _tools.RODict({
        "propID": 52013459,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":54,"adjMaxMagicAtk":119,"adjFatal":27,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013460: _tools.RODict({
        "propID": 52013460,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":62,"adjMaxMagicAtk":131,"adjFatal":29,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013461: _tools.RODict({
        "propID": 52013461,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":67,"adjMaxMagicAtk":145,"adjFatal":34,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013462: _tools.RODict({
        "propID": 52013462,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":19,"adjMaxMagicAtk":40})
    }),
    52013463: _tools.RODict({
        "propID": 52013463,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":20,"adjMaxMagicAtk":43})
    }),
    52013464: _tools.RODict({
        "propID": 52013464,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":22,"adjMaxMagicAtk":46})
    }),
    52013465: _tools.RODict({
        "propID": 52013465,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":23,"adjMaxMagicAtk":49})
    }),
    52013466: _tools.RODict({
        "propID": 52013466,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":25,"adjMaxMagicAtk":53,"adjFatal":15,"adjIgnoreArmor":0.04})
    }),
    52013467: _tools.RODict({
        "propID": 52013467,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":27,"adjMaxMagicAtk":59,"adjFatal":16,"adjIgnoreArmor":0.04})
    }),
    52013468: _tools.RODict({
        "propID": 52013468,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":29,"adjMaxMagicAtk":65,"adjFatal":17,"adjIgnoreArmor":0.04})
    }),
    52013469: _tools.RODict({
        "propID": 52013469,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":32,"adjMaxMagicAtk":70,"adjFatal":18,"adjIgnoreArmor":0.04})
    }),
    52013470: _tools.RODict({
        "propID": 52013470,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":36,"adjMaxMagicAtk":75,"adjFatal":19,"adjIgnoreArmor":0.08})
    }),
    52013471: _tools.RODict({
        "propID": 52013471,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":41,"adjMaxMagicAtk":83,"adjFatal":20,"adjIgnoreArmor":0.08})
    }),
    52013472: _tools.RODict({
        "propID": 52013472,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":44,"adjMaxMagicAtk":91,"adjFatal":22,"adjIgnoreArmor":0.08})
    }),
    52013473: _tools.RODict({
        "propID": 52013473,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":46,"adjMaxMagicAtk":98,"adjFatal":23,"adjIgnoreArmor":0.08})
    }),
    52013474: _tools.RODict({
        "propID": 52013474,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":51,"adjMaxMagicAtk":113,"adjFatal":26,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013475: _tools.RODict({
        "propID": 52013475,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":57,"adjMaxMagicAtk":125,"adjFatal":28,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013476: _tools.RODict({
        "propID": 52013476,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":65,"adjMaxMagicAtk":138,"adjFatal":30,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013477: _tools.RODict({
        "propID": 52013477,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":70,"adjMaxMagicAtk":152,"adjFatal":36,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013478: _tools.RODict({
        "propID": 52013478,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":20,"adjMaxMagicAtk":42})
    }),
    52013479: _tools.RODict({
        "propID": 52013479,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":21,"adjMaxMagicAtk":45})
    }),
    52013480: _tools.RODict({
        "propID": 52013480,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":23,"adjMaxMagicAtk":48})
    }),
    52013481: _tools.RODict({
        "propID": 52013481,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":24,"adjMaxMagicAtk":51})
    }),
    52013482: _tools.RODict({
        "propID": 52013482,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":26,"adjMaxMagicAtk":56,"adjFatal":16,"adjIgnoreArmor":0.04})
    }),
    52013483: _tools.RODict({
        "propID": 52013483,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":28,"adjMaxMagicAtk":62,"adjFatal":17,"adjIgnoreArmor":0.04})
    }),
    52013484: _tools.RODict({
        "propID": 52013484,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":30,"adjMaxMagicAtk":68,"adjFatal":18,"adjIgnoreArmor":0.04})
    }),
    52013485: _tools.RODict({
        "propID": 52013485,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":34,"adjMaxMagicAtk":74,"adjFatal":19,"adjIgnoreArmor":0.04})
    }),
    52013486: _tools.RODict({
        "propID": 52013486,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":38,"adjMaxMagicAtk":79,"adjFatal":20,"adjIgnoreArmor":0.08})
    }),
    52013487: _tools.RODict({
        "propID": 52013487,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":43,"adjMaxMagicAtk":87,"adjFatal":21,"adjIgnoreArmor":0.08})
    }),
    52013488: _tools.RODict({
        "propID": 52013488,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":46,"adjMaxMagicAtk":96,"adjFatal":23,"adjIgnoreArmor":0.08})
    }),
    52013489: _tools.RODict({
        "propID": 52013489,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":48,"adjMaxMagicAtk":103,"adjFatal":24,"adjIgnoreArmor":0.08})
    }),
    52013490: _tools.RODict({
        "propID": 52013490,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":54,"adjMaxMagicAtk":119,"adjFatal":27,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013491: _tools.RODict({
        "propID": 52013491,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":60,"adjMaxMagicAtk":131,"adjFatal":29,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013492: _tools.RODict({
        "propID": 52013492,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":68,"adjMaxMagicAtk":145,"adjFatal":32,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013493: _tools.RODict({
        "propID": 52013493,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":74,"adjMaxMagicAtk":160,"adjFatal":38,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013494: _tools.RODict({
        "propID": 52013494,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":21,"adjMaxMagicAtk":44})
    }),
    52013495: _tools.RODict({
        "propID": 52013495,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":22,"adjMaxMagicAtk":47})
    }),
    52013496: _tools.RODict({
        "propID": 52013496,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":24,"adjMaxMagicAtk":50})
    }),
    52013497: _tools.RODict({
        "propID": 52013497,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":25,"adjMaxMagicAtk":54})
    }),
    52013498: _tools.RODict({
        "propID": 52013498,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":27,"adjMaxMagicAtk":59,"adjFatal":17,"adjIgnoreArmor":0.04})
    }),
    52013499: _tools.RODict({
        "propID": 52013499,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":29,"adjMaxMagicAtk":65,"adjFatal":18,"adjIgnoreArmor":0.04})
    }),
    52013500: _tools.RODict({
        "propID": 52013500,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":32,"adjMaxMagicAtk":71,"adjFatal":19,"adjIgnoreArmor":0.04})
    }),
    52013501: _tools.RODict({
        "propID": 52013501,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":36,"adjMaxMagicAtk":78,"adjFatal":20,"adjIgnoreArmor":0.04})
    }),
    52013502: _tools.RODict({
        "propID": 52013502,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":40,"adjMaxMagicAtk":83,"adjFatal":21,"adjIgnoreArmor":0.08})
    }),
    52013503: _tools.RODict({
        "propID": 52013503,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":45,"adjMaxMagicAtk":91,"adjFatal":22,"adjIgnoreArmor":0.08})
    }),
    52013504: _tools.RODict({
        "propID": 52013504,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":48,"adjMaxMagicAtk":101,"adjFatal":24,"adjIgnoreArmor":0.08})
    }),
    52013505: _tools.RODict({
        "propID": 52013505,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":50,"adjMaxMagicAtk":108,"adjFatal":25,"adjIgnoreArmor":0.08})
    }),
    52013506: _tools.RODict({
        "propID": 52013506,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":57,"adjMaxMagicAtk":125,"adjFatal":28,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013507: _tools.RODict({
        "propID": 52013507,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":63,"adjMaxMagicAtk":138,"adjFatal":30,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013508: _tools.RODict({
        "propID": 52013508,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":71,"adjMaxMagicAtk":152,"adjFatal":34,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013509: _tools.RODict({
        "propID": 52013509,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":78,"adjMaxMagicAtk":168,"adjFatal":40,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013510: _tools.RODict({
        "propID": 52013510,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":22,"adjMaxMagicAtk":46})
    }),
    52013511: _tools.RODict({
        "propID": 52013511,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":23,"adjMaxMagicAtk":49})
    }),
    52013512: _tools.RODict({
        "propID": 52013512,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":25,"adjMaxMagicAtk":53})
    }),
    52013513: _tools.RODict({
        "propID": 52013513,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":26,"adjMaxMagicAtk":57})
    }),
    52013514: _tools.RODict({
        "propID": 52013514,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":28,"adjMaxMagicAtk":62,"adjFatal":18,"adjIgnoreArmor":0.04})
    }),
    52013515: _tools.RODict({
        "propID": 52013515,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":30,"adjMaxMagicAtk":68,"adjFatal":19,"adjIgnoreArmor":0.04})
    }),
    52013516: _tools.RODict({
        "propID": 52013516,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":34,"adjMaxMagicAtk":75,"adjFatal":20,"adjIgnoreArmor":0.04})
    }),
    52013517: _tools.RODict({
        "propID": 52013517,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":38,"adjMaxMagicAtk":82,"adjFatal":21,"adjIgnoreArmor":0.04})
    }),
    52013518: _tools.RODict({
        "propID": 52013518,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":42,"adjMaxMagicAtk":87,"adjFatal":22,"adjIgnoreArmor":0.08})
    }),
    52013519: _tools.RODict({
        "propID": 52013519,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":47,"adjMaxMagicAtk":96,"adjFatal":23,"adjIgnoreArmor":0.08})
    }),
    52013520: _tools.RODict({
        "propID": 52013520,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":50,"adjMaxMagicAtk":106,"adjFatal":25,"adjIgnoreArmor":0.08})
    }),
    52013521: _tools.RODict({
        "propID": 52013521,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":53,"adjMaxMagicAtk":113,"adjFatal":26,"adjIgnoreArmor":0.08})
    }),
    52013522: _tools.RODict({
        "propID": 52013522,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":60,"adjMaxMagicAtk":131,"adjFatal":29,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013523: _tools.RODict({
        "propID": 52013523,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":66,"adjMaxMagicAtk":145,"adjFatal":32,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013524: _tools.RODict({
        "propID": 52013524,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":75,"adjMaxMagicAtk":160,"adjFatal":36,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013525: _tools.RODict({
        "propID": 52013525,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":82,"adjMaxMagicAtk":176,"adjFatal":42,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013526: _tools.RODict({
        "propID": 52013526,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":23,"adjMaxMagicAtk":48})
    }),
    52013527: _tools.RODict({
        "propID": 52013527,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":24,"adjMaxMagicAtk":51})
    }),
    52013528: _tools.RODict({
        "propID": 52013528,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":26,"adjMaxMagicAtk":56})
    }),
    52013529: _tools.RODict({
        "propID": 52013529,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":27,"adjMaxMagicAtk":60})
    }),
    52013530: _tools.RODict({
        "propID": 52013530,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":29,"adjMaxMagicAtk":65,"adjFatal":19,"adjIgnoreArmor":0.04})
    }),
    52013531: _tools.RODict({
        "propID": 52013531,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":32,"adjMaxMagicAtk":71,"adjFatal":20,"adjIgnoreArmor":0.04})
    }),
    52013532: _tools.RODict({
        "propID": 52013532,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":36,"adjMaxMagicAtk":79,"adjFatal":21,"adjIgnoreArmor":0.04})
    }),
    52013533: _tools.RODict({
        "propID": 52013533,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":40,"adjMaxMagicAtk":86,"adjFatal":22,"adjIgnoreArmor":0.04})
    }),
    52013534: _tools.RODict({
        "propID": 52013534,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":44,"adjMaxMagicAtk":91,"adjFatal":23,"adjIgnoreArmor":0.08})
    }),
    52013535: _tools.RODict({
        "propID": 52013535,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":49,"adjMaxMagicAtk":101,"adjFatal":24,"adjIgnoreArmor":0.08})
    }),
    52013536: _tools.RODict({
        "propID": 52013536,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":53,"adjMaxMagicAtk":111,"adjFatal":26,"adjIgnoreArmor":0.08})
    }),
    52013537: _tools.RODict({
        "propID": 52013537,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":56,"adjMaxMagicAtk":119,"adjFatal":27,"adjIgnoreArmor":0.08})
    }),
    52013538: _tools.RODict({
        "propID": 52013538,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":63,"adjMaxMagicAtk":138,"adjFatal":30,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013539: _tools.RODict({
        "propID": 52013539,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":69,"adjMaxMagicAtk":152,"adjFatal":34,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013540: _tools.RODict({
        "propID": 52013540,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":79,"adjMaxMagicAtk":168,"adjFatal":38,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013541: _tools.RODict({
        "propID": 52013541,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":86,"adjMaxMagicAtk":185,"adjFatal":44,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013542: _tools.RODict({
        "propID": 52013542,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":24,"adjMaxMagicAtk":50})
    }),
    52013543: _tools.RODict({
        "propID": 52013543,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":25,"adjMaxMagicAtk":54})
    }),
    52013544: _tools.RODict({
        "propID": 52013544,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":27,"adjMaxMagicAtk":59})
    }),
    52013545: _tools.RODict({
        "propID": 52013545,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":28,"adjMaxMagicAtk":63})
    }),
    52013546: _tools.RODict({
        "propID": 52013546,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":30,"adjMaxMagicAtk":68,"adjFatal":20,"adjIgnoreArmor":0.04})
    }),
    52013547: _tools.RODict({
        "propID": 52013547,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":34,"adjMaxMagicAtk":75,"adjFatal":21,"adjIgnoreArmor":0.04})
    }),
    52013548: _tools.RODict({
        "propID": 52013548,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":38,"adjMaxMagicAtk":83,"adjFatal":22,"adjIgnoreArmor":0.04})
    }),
    52013549: _tools.RODict({
        "propID": 52013549,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":42,"adjMaxMagicAtk":90,"adjFatal":23,"adjIgnoreArmor":0.04})
    }),
    52013550: _tools.RODict({
        "propID": 52013550,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":46,"adjMaxMagicAtk":96,"adjFatal":24,"adjIgnoreArmor":0.08})
    }),
    52013551: _tools.RODict({
        "propID": 52013551,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":51,"adjMaxMagicAtk":106,"adjFatal":25,"adjIgnoreArmor":0.08})
    }),
    52013552: _tools.RODict({
        "propID": 52013552,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":56,"adjMaxMagicAtk":117,"adjFatal":27,"adjIgnoreArmor":0.08})
    }),
    52013553: _tools.RODict({
        "propID": 52013553,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":59,"adjMaxMagicAtk":125,"adjFatal":28,"adjIgnoreArmor":0.08})
    }),
    52013554: _tools.RODict({
        "propID": 52013554,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":66,"adjMaxMagicAtk":145,"adjFatal":32,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013555: _tools.RODict({
        "propID": 52013555,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":72,"adjMaxMagicAtk":160,"adjFatal":36,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013556: _tools.RODict({
        "propID": 52013556,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":83,"adjMaxMagicAtk":176,"adjFatal":40,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
    }),
    52013557: _tools.RODict({
        "propID": 52013557,
        "type": 2,
        "propList": _tools.RODict({"adjMinMagicAtk":90,"adjMaxMagicAtk":194,"adjFatal":46,"adjIgnoreArmor":0.08,"adjDmgArmor":0.08})
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
    52013574: _tools.RODict({
        "propID": 52013574,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":168,"adjMinPhysicalAtk":9,"adjMaxPhysicalAtk":21})
    }),
    52013575: _tools.RODict({
        "propID": 52013575,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":185,"adjMinPhysicalAtk":11,"adjMaxPhysicalAtk":23})
    }),
    52013576: _tools.RODict({
        "propID": 52013576,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":202,"adjMinPhysicalAtk":12,"adjMaxPhysicalAtk":25})
    }),
    52013577: _tools.RODict({
        "propID": 52013577,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":218,"adjMinPhysicalAtk":13,"adjMaxPhysicalAtk":27})
    }),
    52013578: _tools.RODict({
        "propID": 52013578,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":235,"adjMinPhysicalAtk":14,"adjMaxPhysicalAtk":29,"adjIgnoreArmor":0.02})
    }),
    52013579: _tools.RODict({
        "propID": 52013579,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":258,"adjMinPhysicalAtk":15,"adjMaxPhysicalAtk":33,"adjIgnoreArmor":0.02})
    }),
    52013580: _tools.RODict({
        "propID": 52013580,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":282,"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":36,"adjIgnoreArmor":0.02})
    }),
    52013581: _tools.RODict({
        "propID": 52013581,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":306,"adjMinPhysicalAtk":18,"adjMaxPhysicalAtk":38,"adjIgnoreArmor":0.02})
    }),
    52013582: _tools.RODict({
        "propID": 52013582,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":330,"adjMinPhysicalAtk":19,"adjMaxPhysicalAtk":41,"adjIgnoreArmor":0.04})
    }),
    52013583: _tools.RODict({
        "propID": 52013583,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":362,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":45,"adjIgnoreArmor":0.04})
    }),
    52013584: _tools.RODict({
        "propID": 52013584,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":396,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":49,"adjIgnoreArmor":0.04})
    }),
    52013585: _tools.RODict({
        "propID": 52013585,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":428,"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":54,"adjIgnoreArmor":0.04})
    }),
    52013586: _tools.RODict({
        "propID": 52013586,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":492,"adjMinPhysicalAtk":27,"adjMaxPhysicalAtk":62,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013587: _tools.RODict({
        "propID": 52013587,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":542,"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":68,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013588: _tools.RODict({
        "propID": 52013588,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":596,"adjMinPhysicalAtk":34,"adjMaxPhysicalAtk":76,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013589: _tools.RODict({
        "propID": 52013589,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":656,"adjMinPhysicalAtk":37,"adjMaxPhysicalAtk":83,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013590: _tools.RODict({
        "propID": 52013590,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":176,"adjMinPhysicalAtk":9,"adjMaxPhysicalAtk":22})
    }),
    52013591: _tools.RODict({
        "propID": 52013591,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":194,"adjMinPhysicalAtk":12,"adjMaxPhysicalAtk":24})
    }),
    52013592: _tools.RODict({
        "propID": 52013592,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":212,"adjMinPhysicalAtk":13,"adjMaxPhysicalAtk":26})
    }),
    52013593: _tools.RODict({
        "propID": 52013593,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":229,"adjMinPhysicalAtk":14,"adjMaxPhysicalAtk":28})
    }),
    52013594: _tools.RODict({
        "propID": 52013594,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":247,"adjMinPhysicalAtk":15,"adjMaxPhysicalAtk":30,"adjIgnoreArmor":0.02})
    }),
    52013595: _tools.RODict({
        "propID": 52013595,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":271,"adjMinPhysicalAtk":16,"adjMaxPhysicalAtk":35,"adjIgnoreArmor":0.02})
    }),
    52013596: _tools.RODict({
        "propID": 52013596,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":296,"adjMinPhysicalAtk":18,"adjMaxPhysicalAtk":38,"adjIgnoreArmor":0.02})
    }),
    52013597: _tools.RODict({
        "propID": 52013597,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":321,"adjMinPhysicalAtk":19,"adjMaxPhysicalAtk":40,"adjIgnoreArmor":0.02})
    }),
    52013598: _tools.RODict({
        "propID": 52013598,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":347,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":43,"adjIgnoreArmor":0.04})
    }),
    52013599: _tools.RODict({
        "propID": 52013599,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":380,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":47,"adjIgnoreArmor":0.04})
    }),
    52013600: _tools.RODict({
        "propID": 52013600,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":416,"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":51,"adjIgnoreArmor":0.04})
    }),
    52013601: _tools.RODict({
        "propID": 52013601,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":449,"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":57,"adjIgnoreArmor":0.04})
    }),
    52013602: _tools.RODict({
        "propID": 52013602,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":517,"adjMinPhysicalAtk":28,"adjMaxPhysicalAtk":65,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013603: _tools.RODict({
        "propID": 52013603,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":569,"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":71,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013604: _tools.RODict({
        "propID": 52013604,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":626,"adjMinPhysicalAtk":36,"adjMaxPhysicalAtk":80,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013605: _tools.RODict({
        "propID": 52013605,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":689,"adjMinPhysicalAtk":39,"adjMaxPhysicalAtk":87,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013606: _tools.RODict({
        "propID": 52013606,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":185,"adjMinPhysicalAtk":9,"adjMaxPhysicalAtk":23})
    }),
    52013607: _tools.RODict({
        "propID": 52013607,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":204,"adjMinPhysicalAtk":13,"adjMaxPhysicalAtk":25})
    }),
    52013608: _tools.RODict({
        "propID": 52013608,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":223,"adjMinPhysicalAtk":14,"adjMaxPhysicalAtk":27})
    }),
    52013609: _tools.RODict({
        "propID": 52013609,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":240,"adjMinPhysicalAtk":15,"adjMaxPhysicalAtk":29})
    }),
    52013610: _tools.RODict({
        "propID": 52013610,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":259,"adjMinPhysicalAtk":16,"adjMaxPhysicalAtk":32,"adjIgnoreArmor":0.02})
    }),
    52013611: _tools.RODict({
        "propID": 52013611,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":285,"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":37,"adjIgnoreArmor":0.02})
    }),
    52013612: _tools.RODict({
        "propID": 52013612,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":311,"adjMinPhysicalAtk":19,"adjMaxPhysicalAtk":40,"adjIgnoreArmor":0.02})
    }),
    52013613: _tools.RODict({
        "propID": 52013613,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":337,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":42,"adjIgnoreArmor":0.02})
    }),
    52013614: _tools.RODict({
        "propID": 52013614,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":364,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":45,"adjIgnoreArmor":0.04})
    }),
    52013615: _tools.RODict({
        "propID": 52013615,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":399,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":49,"adjIgnoreArmor":0.04})
    }),
    52013616: _tools.RODict({
        "propID": 52013616,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":437,"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":54,"adjIgnoreArmor":0.04})
    }),
    52013617: _tools.RODict({
        "propID": 52013617,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":471,"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":60,"adjIgnoreArmor":0.04})
    }),
    52013618: _tools.RODict({
        "propID": 52013618,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":543,"adjMinPhysicalAtk":29,"adjMaxPhysicalAtk":68,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013619: _tools.RODict({
        "propID": 52013619,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":597,"adjMinPhysicalAtk":34,"adjMaxPhysicalAtk":75,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013620: _tools.RODict({
        "propID": 52013620,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":657,"adjMinPhysicalAtk":38,"adjMaxPhysicalAtk":84,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013621: _tools.RODict({
        "propID": 52013621,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":723,"adjMinPhysicalAtk":41,"adjMaxPhysicalAtk":91,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013622: _tools.RODict({
        "propID": 52013622,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":194,"adjMinPhysicalAtk":9,"adjMaxPhysicalAtk":24})
    }),
    52013623: _tools.RODict({
        "propID": 52013623,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":214,"adjMinPhysicalAtk":14,"adjMaxPhysicalAtk":26})
    }),
    52013624: _tools.RODict({
        "propID": 52013624,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":234,"adjMinPhysicalAtk":15,"adjMaxPhysicalAtk":28})
    }),
    52013625: _tools.RODict({
        "propID": 52013625,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":252,"adjMinPhysicalAtk":16,"adjMaxPhysicalAtk":30})
    }),
    52013626: _tools.RODict({
        "propID": 52013626,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":272,"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":34,"adjIgnoreArmor":0.02})
    }),
    52013627: _tools.RODict({
        "propID": 52013627,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":299,"adjMinPhysicalAtk":18,"adjMaxPhysicalAtk":39,"adjIgnoreArmor":0.02})
    }),
    52013628: _tools.RODict({
        "propID": 52013628,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":327,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":42,"adjIgnoreArmor":0.02})
    }),
    52013629: _tools.RODict({
        "propID": 52013629,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":354,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":44,"adjIgnoreArmor":0.02})
    }),
    52013630: _tools.RODict({
        "propID": 52013630,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":382,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":47,"adjIgnoreArmor":0.04})
    }),
    52013631: _tools.RODict({
        "propID": 52013631,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":419,"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":51,"adjIgnoreArmor":0.04})
    }),
    52013632: _tools.RODict({
        "propID": 52013632,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":459,"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":57,"adjIgnoreArmor":0.04})
    }),
    52013633: _tools.RODict({
        "propID": 52013633,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":495,"adjMinPhysicalAtk":27,"adjMaxPhysicalAtk":63,"adjIgnoreArmor":0.04})
    }),
    52013634: _tools.RODict({
        "propID": 52013634,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":570,"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":71,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013635: _tools.RODict({
        "propID": 52013635,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":627,"adjMinPhysicalAtk":36,"adjMaxPhysicalAtk":79,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013636: _tools.RODict({
        "propID": 52013636,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":690,"adjMinPhysicalAtk":40,"adjMaxPhysicalAtk":88,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013637: _tools.RODict({
        "propID": 52013637,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":759,"adjMinPhysicalAtk":43,"adjMaxPhysicalAtk":96,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013638: _tools.RODict({
        "propID": 52013638,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":204,"adjMinPhysicalAtk":9,"adjMaxPhysicalAtk":25})
    }),
    52013639: _tools.RODict({
        "propID": 52013639,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":225,"adjMinPhysicalAtk":15,"adjMaxPhysicalAtk":27})
    }),
    52013640: _tools.RODict({
        "propID": 52013640,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":246,"adjMinPhysicalAtk":16,"adjMaxPhysicalAtk":29})
    }),
    52013641: _tools.RODict({
        "propID": 52013641,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":265,"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":32})
    }),
    52013642: _tools.RODict({
        "propID": 52013642,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":286,"adjMinPhysicalAtk":18,"adjMaxPhysicalAtk":36,"adjIgnoreArmor":0.02})
    }),
    52013643: _tools.RODict({
        "propID": 52013643,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":314,"adjMinPhysicalAtk":19,"adjMaxPhysicalAtk":41,"adjIgnoreArmor":0.02})
    }),
    52013644: _tools.RODict({
        "propID": 52013644,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":343,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":44,"adjIgnoreArmor":0.02})
    }),
    52013645: _tools.RODict({
        "propID": 52013645,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":372,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":46,"adjIgnoreArmor":0.02})
    }),
    52013646: _tools.RODict({
        "propID": 52013646,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":401,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":49,"adjIgnoreArmor":0.04})
    }),
    52013647: _tools.RODict({
        "propID": 52013647,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":440,"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":54,"adjIgnoreArmor":0.04})
    }),
    52013648: _tools.RODict({
        "propID": 52013648,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":482,"adjMinPhysicalAtk":27,"adjMaxPhysicalAtk":60,"adjIgnoreArmor":0.04})
    }),
    52013649: _tools.RODict({
        "propID": 52013649,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":520,"adjMinPhysicalAtk":28,"adjMaxPhysicalAtk":66,"adjIgnoreArmor":0.04})
    }),
    52013650: _tools.RODict({
        "propID": 52013650,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":599,"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":75,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013651: _tools.RODict({
        "propID": 52013651,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":658,"adjMinPhysicalAtk":38,"adjMaxPhysicalAtk":83,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013652: _tools.RODict({
        "propID": 52013652,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":725,"adjMinPhysicalAtk":42,"adjMaxPhysicalAtk":92,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013653: _tools.RODict({
        "propID": 52013653,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":797,"adjMinPhysicalAtk":45,"adjMaxPhysicalAtk":101,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013654: _tools.RODict({
        "propID": 52013654,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":214,"adjMinPhysicalAtk":9,"adjMaxPhysicalAtk":26})
    }),
    52013655: _tools.RODict({
        "propID": 52013655,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":236,"adjMinPhysicalAtk":16,"adjMaxPhysicalAtk":28})
    }),
    52013656: _tools.RODict({
        "propID": 52013656,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":258,"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":30})
    }),
    52013657: _tools.RODict({
        "propID": 52013657,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":278,"adjMinPhysicalAtk":18,"adjMaxPhysicalAtk":34})
    }),
    52013658: _tools.RODict({
        "propID": 52013658,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":300,"adjMinPhysicalAtk":19,"adjMaxPhysicalAtk":38,"adjIgnoreArmor":0.02})
    }),
    52013659: _tools.RODict({
        "propID": 52013659,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":330,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":43,"adjIgnoreArmor":0.02})
    }),
    52013660: _tools.RODict({
        "propID": 52013660,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":360,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":46,"adjIgnoreArmor":0.02})
    }),
    52013661: _tools.RODict({
        "propID": 52013661,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":391,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":48,"adjIgnoreArmor":0.02})
    }),
    52013662: _tools.RODict({
        "propID": 52013662,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":421,"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":51,"adjIgnoreArmor":0.04})
    }),
    52013663: _tools.RODict({
        "propID": 52013663,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":462,"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":57,"adjIgnoreArmor":0.04})
    }),
    52013664: _tools.RODict({
        "propID": 52013664,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":506,"adjMinPhysicalAtk":28,"adjMaxPhysicalAtk":63,"adjIgnoreArmor":0.04})
    }),
    52013665: _tools.RODict({
        "propID": 52013665,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":546,"adjMinPhysicalAtk":29,"adjMaxPhysicalAtk":69,"adjIgnoreArmor":0.04})
    }),
    52013666: _tools.RODict({
        "propID": 52013666,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":629,"adjMinPhysicalAtk":34,"adjMaxPhysicalAtk":79,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013667: _tools.RODict({
        "propID": 52013667,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":691,"adjMinPhysicalAtk":40,"adjMaxPhysicalAtk":87,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013668: _tools.RODict({
        "propID": 52013668,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":761,"adjMinPhysicalAtk":44,"adjMaxPhysicalAtk":97,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013669: _tools.RODict({
        "propID": 52013669,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":837,"adjMinPhysicalAtk":47,"adjMaxPhysicalAtk":106,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013670: _tools.RODict({
        "propID": 52013670,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":225,"adjMinPhysicalAtk":9,"adjMaxPhysicalAtk":27})
    }),
    52013671: _tools.RODict({
        "propID": 52013671,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":248,"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":29})
    }),
    52013672: _tools.RODict({
        "propID": 52013672,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":271,"adjMinPhysicalAtk":18,"adjMaxPhysicalAtk":32})
    }),
    52013673: _tools.RODict({
        "propID": 52013673,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":292,"adjMinPhysicalAtk":19,"adjMaxPhysicalAtk":36})
    }),
    52013674: _tools.RODict({
        "propID": 52013674,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":315,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":40,"adjIgnoreArmor":0.02})
    }),
    52013675: _tools.RODict({
        "propID": 52013675,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":347,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":45,"adjIgnoreArmor":0.02})
    }),
    52013676: _tools.RODict({
        "propID": 52013676,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":378,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":48,"adjIgnoreArmor":0.02})
    }),
    52013677: _tools.RODict({
        "propID": 52013677,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":411,"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":50,"adjIgnoreArmor":0.02})
    }),
    52013678: _tools.RODict({
        "propID": 52013678,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":442,"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":54,"adjIgnoreArmor":0.04})
    }),
    52013679: _tools.RODict({
        "propID": 52013679,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":485,"adjMinPhysicalAtk":27,"adjMaxPhysicalAtk":60,"adjIgnoreArmor":0.04})
    }),
    52013680: _tools.RODict({
        "propID": 52013680,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":531,"adjMinPhysicalAtk":29,"adjMaxPhysicalAtk":66,"adjIgnoreArmor":0.04})
    }),
    52013681: _tools.RODict({
        "propID": 52013681,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":573,"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":72,"adjIgnoreArmor":0.04})
    }),
    52013682: _tools.RODict({
        "propID": 52013682,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":660,"adjMinPhysicalAtk":36,"adjMaxPhysicalAtk":83,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013683: _tools.RODict({
        "propID": 52013683,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":726,"adjMinPhysicalAtk":42,"adjMaxPhysicalAtk":91,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013684: _tools.RODict({
        "propID": 52013684,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":799,"adjMinPhysicalAtk":46,"adjMaxPhysicalAtk":102,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013685: _tools.RODict({
        "propID": 52013685,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":879,"adjMinPhysicalAtk":49,"adjMaxPhysicalAtk":111,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013686: _tools.RODict({
        "propID": 52013686,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":236,"adjMinPhysicalAtk":9,"adjMaxPhysicalAtk":28})
    }),
    52013687: _tools.RODict({
        "propID": 52013687,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":260,"adjMinPhysicalAtk":18,"adjMaxPhysicalAtk":30})
    }),
    52013688: _tools.RODict({
        "propID": 52013688,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":285,"adjMinPhysicalAtk":19,"adjMaxPhysicalAtk":34})
    }),
    52013689: _tools.RODict({
        "propID": 52013689,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":307,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":38})
    }),
    52013690: _tools.RODict({
        "propID": 52013690,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":331,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":42,"adjIgnoreArmor":0.02})
    }),
    52013691: _tools.RODict({
        "propID": 52013691,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":364,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":47,"adjIgnoreArmor":0.02})
    }),
    52013692: _tools.RODict({
        "propID": 52013692,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":397,"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":50,"adjIgnoreArmor":0.02})
    }),
    52013693: _tools.RODict({
        "propID": 52013693,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":432,"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":53,"adjIgnoreArmor":0.02})
    }),
    52013694: _tools.RODict({
        "propID": 52013694,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":464,"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":57,"adjIgnoreArmor":0.04})
    }),
    52013695: _tools.RODict({
        "propID": 52013695,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":509,"adjMinPhysicalAtk":28,"adjMaxPhysicalAtk":63,"adjIgnoreArmor":0.04})
    }),
    52013696: _tools.RODict({
        "propID": 52013696,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":558,"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":69,"adjIgnoreArmor":0.04})
    }),
    52013697: _tools.RODict({
        "propID": 52013697,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":602,"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":76,"adjIgnoreArmor":0.04})
    }),
    52013698: _tools.RODict({
        "propID": 52013698,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":693,"adjMinPhysicalAtk":38,"adjMaxPhysicalAtk":87,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013699: _tools.RODict({
        "propID": 52013699,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":762,"adjMinPhysicalAtk":44,"adjMaxPhysicalAtk":96,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013700: _tools.RODict({
        "propID": 52013700,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":839,"adjMinPhysicalAtk":48,"adjMaxPhysicalAtk":107,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013701: _tools.RODict({
        "propID": 52013701,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":923,"adjMinPhysicalAtk":51,"adjMaxPhysicalAtk":117,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013702: _tools.RODict({
        "propID": 52013702,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":248,"adjMinPhysicalAtk":9,"adjMaxPhysicalAtk":29})
    }),
    52013703: _tools.RODict({
        "propID": 52013703,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":273,"adjMinPhysicalAtk":19,"adjMaxPhysicalAtk":32})
    }),
    52013704: _tools.RODict({
        "propID": 52013704,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":299,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":36})
    }),
    52013705: _tools.RODict({
        "propID": 52013705,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":322,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":40})
    }),
    52013706: _tools.RODict({
        "propID": 52013706,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":348,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":44,"adjIgnoreArmor":0.02})
    }),
    52013707: _tools.RODict({
        "propID": 52013707,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":382,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":49,"adjIgnoreArmor":0.02})
    }),
    52013708: _tools.RODict({
        "propID": 52013708,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":417,"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":53,"adjIgnoreArmor":0.02})
    }),
    52013709: _tools.RODict({
        "propID": 52013709,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":454,"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":56,"adjIgnoreArmor":0.02})
    }),
    52013710: _tools.RODict({
        "propID": 52013710,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":487,"adjMinPhysicalAtk":27,"adjMaxPhysicalAtk":60,"adjIgnoreArmor":0.04})
    }),
    52013711: _tools.RODict({
        "propID": 52013711,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":534,"adjMinPhysicalAtk":29,"adjMaxPhysicalAtk":66,"adjIgnoreArmor":0.04})
    }),
    52013712: _tools.RODict({
        "propID": 52013712,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":586,"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":72,"adjIgnoreArmor":0.04})
    }),
    52013713: _tools.RODict({
        "propID": 52013713,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":632,"adjMinPhysicalAtk":34,"adjMaxPhysicalAtk":80,"adjIgnoreArmor":0.04})
    }),
    52013714: _tools.RODict({
        "propID": 52013714,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":728,"adjMinPhysicalAtk":40,"adjMaxPhysicalAtk":91,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013715: _tools.RODict({
        "propID": 52013715,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":800,"adjMinPhysicalAtk":46,"adjMaxPhysicalAtk":101,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013716: _tools.RODict({
        "propID": 52013716,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":881,"adjMinPhysicalAtk":50,"adjMaxPhysicalAtk":112,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013717: _tools.RODict({
        "propID": 52013717,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":969,"adjMinPhysicalAtk":54,"adjMaxPhysicalAtk":123,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013718: _tools.RODict({
        "propID": 52013718,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":260,"adjMinPhysicalAtk":9,"adjMaxPhysicalAtk":30})
    }),
    52013719: _tools.RODict({
        "propID": 52013719,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":287,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":34})
    }),
    52013720: _tools.RODict({
        "propID": 52013720,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":314,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":38})
    }),
    52013721: _tools.RODict({
        "propID": 52013721,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":338,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":42})
    }),
    52013722: _tools.RODict({
        "propID": 52013722,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":365,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":46,"adjIgnoreArmor":0.02})
    }),
    52013723: _tools.RODict({
        "propID": 52013723,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":401,"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":51,"adjIgnoreArmor":0.02})
    }),
    52013724: _tools.RODict({
        "propID": 52013724,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":438,"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":56,"adjIgnoreArmor":0.02})
    }),
    52013725: _tools.RODict({
        "propID": 52013725,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":477,"adjMinPhysicalAtk":27,"adjMaxPhysicalAtk":59,"adjIgnoreArmor":0.02})
    }),
    52013726: _tools.RODict({
        "propID": 52013726,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":511,"adjMinPhysicalAtk":28,"adjMaxPhysicalAtk":63,"adjIgnoreArmor":0.04})
    }),
    52013727: _tools.RODict({
        "propID": 52013727,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":561,"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":69,"adjIgnoreArmor":0.04})
    }),
    52013728: _tools.RODict({
        "propID": 52013728,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":615,"adjMinPhysicalAtk":34,"adjMaxPhysicalAtk":76,"adjIgnoreArmor":0.04})
    }),
    52013729: _tools.RODict({
        "propID": 52013729,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":664,"adjMinPhysicalAtk":36,"adjMaxPhysicalAtk":84,"adjIgnoreArmor":0.04})
    }),
    52013730: _tools.RODict({
        "propID": 52013730,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":764,"adjMinPhysicalAtk":42,"adjMaxPhysicalAtk":96,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013731: _tools.RODict({
        "propID": 52013731,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":840,"adjMinPhysicalAtk":48,"adjMaxPhysicalAtk":106,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013732: _tools.RODict({
        "propID": 52013732,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":925,"adjMinPhysicalAtk":53,"adjMaxPhysicalAtk":118,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013733: _tools.RODict({
        "propID": 52013733,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":1017,"adjMinPhysicalAtk":57,"adjMaxPhysicalAtk":129,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
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
    52013750: _tools.RODict({
        "propID": 52013750,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":168,"adjMinMagicAtk":9,"adjMaxMagicAtk":21})
    }),
    52013751: _tools.RODict({
        "propID": 52013751,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":185,"adjMinMagicAtk":11,"adjMaxMagicAtk":23})
    }),
    52013752: _tools.RODict({
        "propID": 52013752,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":202,"adjMinMagicAtk":12,"adjMaxMagicAtk":25})
    }),
    52013753: _tools.RODict({
        "propID": 52013753,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":218,"adjMinMagicAtk":13,"adjMaxMagicAtk":27})
    }),
    52013754: _tools.RODict({
        "propID": 52013754,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":235,"adjMinMagicAtk":14,"adjMaxMagicAtk":29,"adjIgnoreArmor":0.02})
    }),
    52013755: _tools.RODict({
        "propID": 52013755,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":258,"adjMinMagicAtk":15,"adjMaxMagicAtk":33,"adjIgnoreArmor":0.02})
    }),
    52013756: _tools.RODict({
        "propID": 52013756,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":282,"adjMinMagicAtk":17,"adjMaxMagicAtk":36,"adjIgnoreArmor":0.02})
    }),
    52013757: _tools.RODict({
        "propID": 52013757,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":306,"adjMinMagicAtk":18,"adjMaxMagicAtk":38,"adjIgnoreArmor":0.02})
    }),
    52013758: _tools.RODict({
        "propID": 52013758,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":330,"adjMinMagicAtk":19,"adjMaxMagicAtk":41,"adjIgnoreArmor":0.04})
    }),
    52013759: _tools.RODict({
        "propID": 52013759,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":362,"adjMinMagicAtk":21,"adjMaxMagicAtk":45,"adjIgnoreArmor":0.04})
    }),
    52013760: _tools.RODict({
        "propID": 52013760,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":396,"adjMinMagicAtk":23,"adjMaxMagicAtk":49,"adjIgnoreArmor":0.04})
    }),
    52013761: _tools.RODict({
        "propID": 52013761,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":428,"adjMinMagicAtk":24,"adjMaxMagicAtk":54,"adjIgnoreArmor":0.04})
    }),
    52013762: _tools.RODict({
        "propID": 52013762,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":492,"adjMinMagicAtk":27,"adjMaxMagicAtk":62,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013763: _tools.RODict({
        "propID": 52013763,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":542,"adjMinMagicAtk":30,"adjMaxMagicAtk":68,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013764: _tools.RODict({
        "propID": 52013764,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":596,"adjMinMagicAtk":34,"adjMaxMagicAtk":76,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013765: _tools.RODict({
        "propID": 52013765,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":656,"adjMinMagicAtk":37,"adjMaxMagicAtk":83,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013766: _tools.RODict({
        "propID": 52013766,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":176,"adjMinMagicAtk":9,"adjMaxMagicAtk":22})
    }),
    52013767: _tools.RODict({
        "propID": 52013767,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":194,"adjMinMagicAtk":12,"adjMaxMagicAtk":24})
    }),
    52013768: _tools.RODict({
        "propID": 52013768,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":212,"adjMinMagicAtk":13,"adjMaxMagicAtk":26})
    }),
    52013769: _tools.RODict({
        "propID": 52013769,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":229,"adjMinMagicAtk":14,"adjMaxMagicAtk":28})
    }),
    52013770: _tools.RODict({
        "propID": 52013770,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":247,"adjMinMagicAtk":15,"adjMaxMagicAtk":30,"adjIgnoreArmor":0.02})
    }),
    52013771: _tools.RODict({
        "propID": 52013771,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":271,"adjMinMagicAtk":16,"adjMaxMagicAtk":35,"adjIgnoreArmor":0.02})
    }),
    52013772: _tools.RODict({
        "propID": 52013772,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":296,"adjMinMagicAtk":18,"adjMaxMagicAtk":38,"adjIgnoreArmor":0.02})
    }),
    52013773: _tools.RODict({
        "propID": 52013773,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":321,"adjMinMagicAtk":19,"adjMaxMagicAtk":40,"adjIgnoreArmor":0.02})
    }),
    52013774: _tools.RODict({
        "propID": 52013774,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":347,"adjMinMagicAtk":20,"adjMaxMagicAtk":43,"adjIgnoreArmor":0.04})
    }),
    52013775: _tools.RODict({
        "propID": 52013775,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":380,"adjMinMagicAtk":22,"adjMaxMagicAtk":47,"adjIgnoreArmor":0.04})
    }),
    52013776: _tools.RODict({
        "propID": 52013776,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":416,"adjMinMagicAtk":24,"adjMaxMagicAtk":51,"adjIgnoreArmor":0.04})
    }),
    52013777: _tools.RODict({
        "propID": 52013777,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":449,"adjMinMagicAtk":25,"adjMaxMagicAtk":57,"adjIgnoreArmor":0.04})
    }),
    52013778: _tools.RODict({
        "propID": 52013778,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":517,"adjMinMagicAtk":28,"adjMaxMagicAtk":65,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013779: _tools.RODict({
        "propID": 52013779,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":569,"adjMinMagicAtk":32,"adjMaxMagicAtk":71,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013780: _tools.RODict({
        "propID": 52013780,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":626,"adjMinMagicAtk":36,"adjMaxMagicAtk":80,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013781: _tools.RODict({
        "propID": 52013781,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":689,"adjMinMagicAtk":39,"adjMaxMagicAtk":87,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013782: _tools.RODict({
        "propID": 52013782,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":185,"adjMinMagicAtk":9,"adjMaxMagicAtk":23})
    }),
    52013783: _tools.RODict({
        "propID": 52013783,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":204,"adjMinMagicAtk":13,"adjMaxMagicAtk":25})
    }),
    52013784: _tools.RODict({
        "propID": 52013784,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":223,"adjMinMagicAtk":14,"adjMaxMagicAtk":27})
    }),
    52013785: _tools.RODict({
        "propID": 52013785,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":240,"adjMinMagicAtk":15,"adjMaxMagicAtk":29})
    }),
    52013786: _tools.RODict({
        "propID": 52013786,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":259,"adjMinMagicAtk":16,"adjMaxMagicAtk":32,"adjIgnoreArmor":0.02})
    }),
    52013787: _tools.RODict({
        "propID": 52013787,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":285,"adjMinMagicAtk":17,"adjMaxMagicAtk":37,"adjIgnoreArmor":0.02})
    }),
    52013788: _tools.RODict({
        "propID": 52013788,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":311,"adjMinMagicAtk":19,"adjMaxMagicAtk":40,"adjIgnoreArmor":0.02})
    }),
    52013789: _tools.RODict({
        "propID": 52013789,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":337,"adjMinMagicAtk":20,"adjMaxMagicAtk":42,"adjIgnoreArmor":0.02})
    }),
    52013790: _tools.RODict({
        "propID": 52013790,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":364,"adjMinMagicAtk":21,"adjMaxMagicAtk":45,"adjIgnoreArmor":0.04})
    }),
    52013791: _tools.RODict({
        "propID": 52013791,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":399,"adjMinMagicAtk":23,"adjMaxMagicAtk":49,"adjIgnoreArmor":0.04})
    }),
    52013792: _tools.RODict({
        "propID": 52013792,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":437,"adjMinMagicAtk":25,"adjMaxMagicAtk":54,"adjIgnoreArmor":0.04})
    }),
    52013793: _tools.RODict({
        "propID": 52013793,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":471,"adjMinMagicAtk":26,"adjMaxMagicAtk":60,"adjIgnoreArmor":0.04})
    }),
    52013794: _tools.RODict({
        "propID": 52013794,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":543,"adjMinMagicAtk":29,"adjMaxMagicAtk":68,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013795: _tools.RODict({
        "propID": 52013795,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":597,"adjMinMagicAtk":34,"adjMaxMagicAtk":75,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013796: _tools.RODict({
        "propID": 52013796,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":657,"adjMinMagicAtk":38,"adjMaxMagicAtk":84,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013797: _tools.RODict({
        "propID": 52013797,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":723,"adjMinMagicAtk":41,"adjMaxMagicAtk":91,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013798: _tools.RODict({
        "propID": 52013798,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":194,"adjMinMagicAtk":9,"adjMaxMagicAtk":24})
    }),
    52013799: _tools.RODict({
        "propID": 52013799,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":214,"adjMinMagicAtk":14,"adjMaxMagicAtk":26})
    }),
    52013800: _tools.RODict({
        "propID": 52013800,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":234,"adjMinMagicAtk":15,"adjMaxMagicAtk":28})
    }),
    52013801: _tools.RODict({
        "propID": 52013801,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":252,"adjMinMagicAtk":16,"adjMaxMagicAtk":30})
    }),
    52013802: _tools.RODict({
        "propID": 52013802,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":272,"adjMinMagicAtk":17,"adjMaxMagicAtk":34,"adjIgnoreArmor":0.02})
    }),
    52013803: _tools.RODict({
        "propID": 52013803,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":299,"adjMinMagicAtk":18,"adjMaxMagicAtk":39,"adjIgnoreArmor":0.02})
    }),
    52013804: _tools.RODict({
        "propID": 52013804,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":327,"adjMinMagicAtk":20,"adjMaxMagicAtk":42,"adjIgnoreArmor":0.02})
    }),
    52013805: _tools.RODict({
        "propID": 52013805,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":354,"adjMinMagicAtk":21,"adjMaxMagicAtk":44,"adjIgnoreArmor":0.02})
    }),
    52013806: _tools.RODict({
        "propID": 52013806,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":382,"adjMinMagicAtk":22,"adjMaxMagicAtk":47,"adjIgnoreArmor":0.04})
    }),
    52013807: _tools.RODict({
        "propID": 52013807,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":419,"adjMinMagicAtk":24,"adjMaxMagicAtk":51,"adjIgnoreArmor":0.04})
    }),
    52013808: _tools.RODict({
        "propID": 52013808,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":459,"adjMinMagicAtk":26,"adjMaxMagicAtk":57,"adjIgnoreArmor":0.04})
    }),
    52013809: _tools.RODict({
        "propID": 52013809,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":495,"adjMinMagicAtk":27,"adjMaxMagicAtk":63,"adjIgnoreArmor":0.04})
    }),
    52013810: _tools.RODict({
        "propID": 52013810,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":570,"adjMinMagicAtk":30,"adjMaxMagicAtk":71,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013811: _tools.RODict({
        "propID": 52013811,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":627,"adjMinMagicAtk":36,"adjMaxMagicAtk":79,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013812: _tools.RODict({
        "propID": 52013812,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":690,"adjMinMagicAtk":40,"adjMaxMagicAtk":88,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013813: _tools.RODict({
        "propID": 52013813,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":759,"adjMinMagicAtk":43,"adjMaxMagicAtk":96,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013814: _tools.RODict({
        "propID": 52013814,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":204,"adjMinMagicAtk":9,"adjMaxMagicAtk":25})
    }),
    52013815: _tools.RODict({
        "propID": 52013815,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":225,"adjMinMagicAtk":15,"adjMaxMagicAtk":27})
    }),
    52013816: _tools.RODict({
        "propID": 52013816,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":246,"adjMinMagicAtk":16,"adjMaxMagicAtk":29})
    }),
    52013817: _tools.RODict({
        "propID": 52013817,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":265,"adjMinMagicAtk":17,"adjMaxMagicAtk":32})
    }),
    52013818: _tools.RODict({
        "propID": 52013818,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":286,"adjMinMagicAtk":18,"adjMaxMagicAtk":36,"adjIgnoreArmor":0.02})
    }),
    52013819: _tools.RODict({
        "propID": 52013819,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":314,"adjMinMagicAtk":19,"adjMaxMagicAtk":41,"adjIgnoreArmor":0.02})
    }),
    52013820: _tools.RODict({
        "propID": 52013820,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":343,"adjMinMagicAtk":21,"adjMaxMagicAtk":44,"adjIgnoreArmor":0.02})
    }),
    52013821: _tools.RODict({
        "propID": 52013821,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":372,"adjMinMagicAtk":22,"adjMaxMagicAtk":46,"adjIgnoreArmor":0.02})
    }),
    52013822: _tools.RODict({
        "propID": 52013822,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":401,"adjMinMagicAtk":23,"adjMaxMagicAtk":49,"adjIgnoreArmor":0.04})
    }),
    52013823: _tools.RODict({
        "propID": 52013823,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":440,"adjMinMagicAtk":25,"adjMaxMagicAtk":54,"adjIgnoreArmor":0.04})
    }),
    52013824: _tools.RODict({
        "propID": 52013824,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":482,"adjMinMagicAtk":27,"adjMaxMagicAtk":60,"adjIgnoreArmor":0.04})
    }),
    52013825: _tools.RODict({
        "propID": 52013825,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":520,"adjMinMagicAtk":28,"adjMaxMagicAtk":66,"adjIgnoreArmor":0.04})
    }),
    52013826: _tools.RODict({
        "propID": 52013826,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":599,"adjMinMagicAtk":32,"adjMaxMagicAtk":75,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013827: _tools.RODict({
        "propID": 52013827,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":658,"adjMinMagicAtk":38,"adjMaxMagicAtk":83,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013828: _tools.RODict({
        "propID": 52013828,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":725,"adjMinMagicAtk":42,"adjMaxMagicAtk":92,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013829: _tools.RODict({
        "propID": 52013829,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":797,"adjMinMagicAtk":45,"adjMaxMagicAtk":101,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013830: _tools.RODict({
        "propID": 52013830,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":214,"adjMinMagicAtk":9,"adjMaxMagicAtk":26})
    }),
    52013831: _tools.RODict({
        "propID": 52013831,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":236,"adjMinMagicAtk":16,"adjMaxMagicAtk":28})
    }),
    52013832: _tools.RODict({
        "propID": 52013832,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":258,"adjMinMagicAtk":17,"adjMaxMagicAtk":30})
    }),
    52013833: _tools.RODict({
        "propID": 52013833,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":278,"adjMinMagicAtk":18,"adjMaxMagicAtk":34})
    }),
    52013834: _tools.RODict({
        "propID": 52013834,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":300,"adjMinMagicAtk":19,"adjMaxMagicAtk":38,"adjIgnoreArmor":0.02})
    }),
    52013835: _tools.RODict({
        "propID": 52013835,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":330,"adjMinMagicAtk":20,"adjMaxMagicAtk":43,"adjIgnoreArmor":0.02})
    }),
    52013836: _tools.RODict({
        "propID": 52013836,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":360,"adjMinMagicAtk":22,"adjMaxMagicAtk":46,"adjIgnoreArmor":0.02})
    }),
    52013837: _tools.RODict({
        "propID": 52013837,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":391,"adjMinMagicAtk":23,"adjMaxMagicAtk":48,"adjIgnoreArmor":0.02})
    }),
    52013838: _tools.RODict({
        "propID": 52013838,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":421,"adjMinMagicAtk":24,"adjMaxMagicAtk":51,"adjIgnoreArmor":0.04})
    }),
    52013839: _tools.RODict({
        "propID": 52013839,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":462,"adjMinMagicAtk":26,"adjMaxMagicAtk":57,"adjIgnoreArmor":0.04})
    }),
    52013840: _tools.RODict({
        "propID": 52013840,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":506,"adjMinMagicAtk":28,"adjMaxMagicAtk":63,"adjIgnoreArmor":0.04})
    }),
    52013841: _tools.RODict({
        "propID": 52013841,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":546,"adjMinMagicAtk":29,"adjMaxMagicAtk":69,"adjIgnoreArmor":0.04})
    }),
    52013842: _tools.RODict({
        "propID": 52013842,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":629,"adjMinMagicAtk":34,"adjMaxMagicAtk":79,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013843: _tools.RODict({
        "propID": 52013843,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":691,"adjMinMagicAtk":40,"adjMaxMagicAtk":87,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013844: _tools.RODict({
        "propID": 52013844,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":761,"adjMinMagicAtk":44,"adjMaxMagicAtk":97,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013845: _tools.RODict({
        "propID": 52013845,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":837,"adjMinMagicAtk":47,"adjMaxMagicAtk":106,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013846: _tools.RODict({
        "propID": 52013846,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":225,"adjMinMagicAtk":9,"adjMaxMagicAtk":27})
    }),
    52013847: _tools.RODict({
        "propID": 52013847,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":248,"adjMinMagicAtk":17,"adjMaxMagicAtk":29})
    }),
    52013848: _tools.RODict({
        "propID": 52013848,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":271,"adjMinMagicAtk":18,"adjMaxMagicAtk":32})
    }),
    52013849: _tools.RODict({
        "propID": 52013849,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":292,"adjMinMagicAtk":19,"adjMaxMagicAtk":36})
    }),
    52013850: _tools.RODict({
        "propID": 52013850,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":315,"adjMinMagicAtk":20,"adjMaxMagicAtk":40,"adjIgnoreArmor":0.02})
    }),
    52013851: _tools.RODict({
        "propID": 52013851,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":347,"adjMinMagicAtk":21,"adjMaxMagicAtk":45,"adjIgnoreArmor":0.02})
    }),
    52013852: _tools.RODict({
        "propID": 52013852,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":378,"adjMinMagicAtk":23,"adjMaxMagicAtk":48,"adjIgnoreArmor":0.02})
    }),
    52013853: _tools.RODict({
        "propID": 52013853,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":411,"adjMinMagicAtk":24,"adjMaxMagicAtk":50,"adjIgnoreArmor":0.02})
    }),
    52013854: _tools.RODict({
        "propID": 52013854,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":442,"adjMinMagicAtk":25,"adjMaxMagicAtk":54,"adjIgnoreArmor":0.04})
    }),
    52013855: _tools.RODict({
        "propID": 52013855,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":485,"adjMinMagicAtk":27,"adjMaxMagicAtk":60,"adjIgnoreArmor":0.04})
    }),
    52013856: _tools.RODict({
        "propID": 52013856,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":531,"adjMinMagicAtk":29,"adjMaxMagicAtk":66,"adjIgnoreArmor":0.04})
    }),
    52013857: _tools.RODict({
        "propID": 52013857,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":573,"adjMinMagicAtk":30,"adjMaxMagicAtk":72,"adjIgnoreArmor":0.04})
    }),
    52013858: _tools.RODict({
        "propID": 52013858,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":660,"adjMinMagicAtk":36,"adjMaxMagicAtk":83,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013859: _tools.RODict({
        "propID": 52013859,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":726,"adjMinMagicAtk":42,"adjMaxMagicAtk":91,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013860: _tools.RODict({
        "propID": 52013860,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":799,"adjMinMagicAtk":46,"adjMaxMagicAtk":102,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013861: _tools.RODict({
        "propID": 52013861,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":879,"adjMinMagicAtk":49,"adjMaxMagicAtk":111,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013862: _tools.RODict({
        "propID": 52013862,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":236,"adjMinMagicAtk":9,"adjMaxMagicAtk":28})
    }),
    52013863: _tools.RODict({
        "propID": 52013863,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":260,"adjMinMagicAtk":18,"adjMaxMagicAtk":30})
    }),
    52013864: _tools.RODict({
        "propID": 52013864,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":285,"adjMinMagicAtk":19,"adjMaxMagicAtk":34})
    }),
    52013865: _tools.RODict({
        "propID": 52013865,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":307,"adjMinMagicAtk":20,"adjMaxMagicAtk":38})
    }),
    52013866: _tools.RODict({
        "propID": 52013866,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":331,"adjMinMagicAtk":21,"adjMaxMagicAtk":42,"adjIgnoreArmor":0.02})
    }),
    52013867: _tools.RODict({
        "propID": 52013867,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":364,"adjMinMagicAtk":22,"adjMaxMagicAtk":47,"adjIgnoreArmor":0.02})
    }),
    52013868: _tools.RODict({
        "propID": 52013868,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":397,"adjMinMagicAtk":24,"adjMaxMagicAtk":50,"adjIgnoreArmor":0.02})
    }),
    52013869: _tools.RODict({
        "propID": 52013869,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":432,"adjMinMagicAtk":25,"adjMaxMagicAtk":53,"adjIgnoreArmor":0.02})
    }),
    52013870: _tools.RODict({
        "propID": 52013870,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":464,"adjMinMagicAtk":26,"adjMaxMagicAtk":57,"adjIgnoreArmor":0.04})
    }),
    52013871: _tools.RODict({
        "propID": 52013871,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":509,"adjMinMagicAtk":28,"adjMaxMagicAtk":63,"adjIgnoreArmor":0.04})
    }),
    52013872: _tools.RODict({
        "propID": 52013872,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":558,"adjMinMagicAtk":30,"adjMaxMagicAtk":69,"adjIgnoreArmor":0.04})
    }),
    52013873: _tools.RODict({
        "propID": 52013873,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":602,"adjMinMagicAtk":32,"adjMaxMagicAtk":76,"adjIgnoreArmor":0.04})
    }),
    52013874: _tools.RODict({
        "propID": 52013874,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":693,"adjMinMagicAtk":38,"adjMaxMagicAtk":87,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013875: _tools.RODict({
        "propID": 52013875,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":762,"adjMinMagicAtk":44,"adjMaxMagicAtk":96,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013876: _tools.RODict({
        "propID": 52013876,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":839,"adjMinMagicAtk":48,"adjMaxMagicAtk":107,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013877: _tools.RODict({
        "propID": 52013877,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":923,"adjMinMagicAtk":51,"adjMaxMagicAtk":117,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013878: _tools.RODict({
        "propID": 52013878,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":248,"adjMinMagicAtk":9,"adjMaxMagicAtk":29})
    }),
    52013879: _tools.RODict({
        "propID": 52013879,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":273,"adjMinMagicAtk":19,"adjMaxMagicAtk":32})
    }),
    52013880: _tools.RODict({
        "propID": 52013880,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":299,"adjMinMagicAtk":20,"adjMaxMagicAtk":36})
    }),
    52013881: _tools.RODict({
        "propID": 52013881,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":322,"adjMinMagicAtk":21,"adjMaxMagicAtk":40})
    }),
    52013882: _tools.RODict({
        "propID": 52013882,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":348,"adjMinMagicAtk":22,"adjMaxMagicAtk":44,"adjIgnoreArmor":0.02})
    }),
    52013883: _tools.RODict({
        "propID": 52013883,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":382,"adjMinMagicAtk":23,"adjMaxMagicAtk":49,"adjIgnoreArmor":0.02})
    }),
    52013884: _tools.RODict({
        "propID": 52013884,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":417,"adjMinMagicAtk":25,"adjMaxMagicAtk":53,"adjIgnoreArmor":0.02})
    }),
    52013885: _tools.RODict({
        "propID": 52013885,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":454,"adjMinMagicAtk":26,"adjMaxMagicAtk":56,"adjIgnoreArmor":0.02})
    }),
    52013886: _tools.RODict({
        "propID": 52013886,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":487,"adjMinMagicAtk":27,"adjMaxMagicAtk":60,"adjIgnoreArmor":0.04})
    }),
    52013887: _tools.RODict({
        "propID": 52013887,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":534,"adjMinMagicAtk":29,"adjMaxMagicAtk":66,"adjIgnoreArmor":0.04})
    }),
    52013888: _tools.RODict({
        "propID": 52013888,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":586,"adjMinMagicAtk":32,"adjMaxMagicAtk":72,"adjIgnoreArmor":0.04})
    }),
    52013889: _tools.RODict({
        "propID": 52013889,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":632,"adjMinMagicAtk":34,"adjMaxMagicAtk":80,"adjIgnoreArmor":0.04})
    }),
    52013890: _tools.RODict({
        "propID": 52013890,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":728,"adjMinMagicAtk":40,"adjMaxMagicAtk":91,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013891: _tools.RODict({
        "propID": 52013891,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":800,"adjMinMagicAtk":46,"adjMaxMagicAtk":101,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013892: _tools.RODict({
        "propID": 52013892,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":881,"adjMinMagicAtk":50,"adjMaxMagicAtk":112,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013893: _tools.RODict({
        "propID": 52013893,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":969,"adjMinMagicAtk":54,"adjMaxMagicAtk":123,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013894: _tools.RODict({
        "propID": 52013894,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":260,"adjMinMagicAtk":9,"adjMaxMagicAtk":30})
    }),
    52013895: _tools.RODict({
        "propID": 52013895,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":287,"adjMinMagicAtk":20,"adjMaxMagicAtk":34})
    }),
    52013896: _tools.RODict({
        "propID": 52013896,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":314,"adjMinMagicAtk":21,"adjMaxMagicAtk":38})
    }),
    52013897: _tools.RODict({
        "propID": 52013897,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":338,"adjMinMagicAtk":22,"adjMaxMagicAtk":42})
    }),
    52013898: _tools.RODict({
        "propID": 52013898,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":365,"adjMinMagicAtk":23,"adjMaxMagicAtk":46,"adjIgnoreArmor":0.02})
    }),
    52013899: _tools.RODict({
        "propID": 52013899,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":401,"adjMinMagicAtk":24,"adjMaxMagicAtk":51,"adjIgnoreArmor":0.02})
    }),
    52013900: _tools.RODict({
        "propID": 52013900,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":438,"adjMinMagicAtk":26,"adjMaxMagicAtk":56,"adjIgnoreArmor":0.02})
    }),
    52013901: _tools.RODict({
        "propID": 52013901,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":477,"adjMinMagicAtk":27,"adjMaxMagicAtk":59,"adjIgnoreArmor":0.02})
    }),
    52013902: _tools.RODict({
        "propID": 52013902,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":511,"adjMinMagicAtk":28,"adjMaxMagicAtk":63,"adjIgnoreArmor":0.04})
    }),
    52013903: _tools.RODict({
        "propID": 52013903,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":561,"adjMinMagicAtk":30,"adjMaxMagicAtk":69,"adjIgnoreArmor":0.04})
    }),
    52013904: _tools.RODict({
        "propID": 52013904,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":615,"adjMinMagicAtk":34,"adjMaxMagicAtk":76,"adjIgnoreArmor":0.04})
    }),
    52013905: _tools.RODict({
        "propID": 52013905,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":664,"adjMinMagicAtk":36,"adjMaxMagicAtk":84,"adjIgnoreArmor":0.04})
    }),
    52013906: _tools.RODict({
        "propID": 52013906,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":764,"adjMinMagicAtk":42,"adjMaxMagicAtk":96,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013907: _tools.RODict({
        "propID": 52013907,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":840,"adjMinMagicAtk":48,"adjMaxMagicAtk":106,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013908: _tools.RODict({
        "propID": 52013908,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":925,"adjMinMagicAtk":53,"adjMaxMagicAtk":118,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
    }),
    52013909: _tools.RODict({
        "propID": 52013909,
        "type": 2,
        "propList": _tools.RODict({"adjFullMp":1017,"adjMinMagicAtk":57,"adjMaxMagicAtk":129,"adjIgnoreArmor":0.04,"adjDmgArmor":0.04})
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
    52013926: _tools.RODict({
        "propID": 52013926,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":916,"adjMinPhysicalAtk":12,"adjMaxPhysicalAtk":26})
    }),
    52013927: _tools.RODict({
        "propID": 52013927,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1007,"adjMinPhysicalAtk":13,"adjMaxPhysicalAtk":29})
    }),
    52013928: _tools.RODict({
        "propID": 52013928,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1098,"adjMinPhysicalAtk":14,"adjMaxPhysicalAtk":32})
    }),
    52013929: _tools.RODict({
        "propID": 52013929,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1191,"adjMinPhysicalAtk":15,"adjMaxPhysicalAtk":35})
    }),
    52013930: _tools.RODict({
        "propID": 52013930,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1282,"adjMinPhysicalAtk":16,"adjMaxPhysicalAtk":37,"adjMonsterDmg":0.025})
    }),
    52013931: _tools.RODict({
        "propID": 52013931,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1410,"adjMinPhysicalAtk":18,"adjMaxPhysicalAtk":41,"adjMonsterDmg":0.025})
    }),
    52013932: _tools.RODict({
        "propID": 52013932,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1538,"adjMinPhysicalAtk":19,"adjMaxPhysicalAtk":44,"adjMonsterDmg":0.025})
    }),
    52013933: _tools.RODict({
        "propID": 52013933,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1666,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":48,"adjMonsterDmg":0.025})
    }),
    52013934: _tools.RODict({
        "propID": 52013934,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1794,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":51,"adjMonsterDmg":0.05})
    }),
    52013935: _tools.RODict({
        "propID": 52013935,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1974,"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":57,"adjMonsterDmg":0.05})
    }),
    52013936: _tools.RODict({
        "propID": 52013936,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2154,"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":62,"adjMonsterDmg":0.05})
    }),
    52013937: _tools.RODict({
        "propID": 52013937,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2333,"adjMinPhysicalAtk":28,"adjMaxPhysicalAtk":67,"adjMonsterDmg":0.05})
    }),
    52013938: _tools.RODict({
        "propID": 52013938,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2683,"adjMinPhysicalAtk":33,"adjMaxPhysicalAtk":78,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52013939: _tools.RODict({
        "propID": 52013939,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2952,"adjMinPhysicalAtk":36,"adjMaxPhysicalAtk":85,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52013940: _tools.RODict({
        "propID": 52013940,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3247,"adjMinPhysicalAtk":39,"adjMaxPhysicalAtk":93,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52013941: _tools.RODict({
        "propID": 52013941,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3571,"adjMinPhysicalAtk":43,"adjMaxPhysicalAtk":103,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52013942: _tools.RODict({
        "propID": 52013942,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":962,"adjMinPhysicalAtk":13,"adjMaxPhysicalAtk":27})
    }),
    52013943: _tools.RODict({
        "propID": 52013943,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1057,"adjMinPhysicalAtk":14,"adjMaxPhysicalAtk":30})
    }),
    52013944: _tools.RODict({
        "propID": 52013944,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1153,"adjMinPhysicalAtk":15,"adjMaxPhysicalAtk":34})
    }),
    52013945: _tools.RODict({
        "propID": 52013945,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1251,"adjMinPhysicalAtk":16,"adjMaxPhysicalAtk":37})
    }),
    52013946: _tools.RODict({
        "propID": 52013946,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1346,"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":39,"adjMonsterDmg":0.025})
    }),
    52013947: _tools.RODict({
        "propID": 52013947,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1481,"adjMinPhysicalAtk":19,"adjMaxPhysicalAtk":43,"adjMonsterDmg":0.025})
    }),
    52013948: _tools.RODict({
        "propID": 52013948,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1615,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":46,"adjMonsterDmg":0.025})
    }),
    52013949: _tools.RODict({
        "propID": 52013949,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1749,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":50,"adjMonsterDmg":0.025})
    }),
    52013950: _tools.RODict({
        "propID": 52013950,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1884,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":54,"adjMonsterDmg":0.05})
    }),
    52013951: _tools.RODict({
        "propID": 52013951,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2073,"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":60,"adjMonsterDmg":0.05})
    }),
    52013952: _tools.RODict({
        "propID": 52013952,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2262,"adjMinPhysicalAtk":27,"adjMaxPhysicalAtk":65,"adjMonsterDmg":0.05})
    }),
    52013953: _tools.RODict({
        "propID": 52013953,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2450,"adjMinPhysicalAtk":29,"adjMaxPhysicalAtk":70,"adjMonsterDmg":0.05})
    }),
    52013954: _tools.RODict({
        "propID": 52013954,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2817,"adjMinPhysicalAtk":35,"adjMaxPhysicalAtk":82,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52013955: _tools.RODict({
        "propID": 52013955,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3100,"adjMinPhysicalAtk":38,"adjMaxPhysicalAtk":89,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52013956: _tools.RODict({
        "propID": 52013956,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3409,"adjMinPhysicalAtk":41,"adjMaxPhysicalAtk":98,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52013957: _tools.RODict({
        "propID": 52013957,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3750,"adjMinPhysicalAtk":45,"adjMaxPhysicalAtk":108,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52013958: _tools.RODict({
        "propID": 52013958,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1010,"adjMinPhysicalAtk":14,"adjMaxPhysicalAtk":28})
    }),
    52013959: _tools.RODict({
        "propID": 52013959,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1110,"adjMinPhysicalAtk":15,"adjMaxPhysicalAtk":32})
    }),
    52013960: _tools.RODict({
        "propID": 52013960,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1211,"adjMinPhysicalAtk":16,"adjMaxPhysicalAtk":36})
    }),
    52013961: _tools.RODict({
        "propID": 52013961,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1314,"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":39})
    }),
    52013962: _tools.RODict({
        "propID": 52013962,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1413,"adjMinPhysicalAtk":18,"adjMaxPhysicalAtk":41,"adjMonsterDmg":0.025})
    }),
    52013963: _tools.RODict({
        "propID": 52013963,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1555,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":45,"adjMonsterDmg":0.025})
    }),
    52013964: _tools.RODict({
        "propID": 52013964,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1696,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":48,"adjMonsterDmg":0.025})
    }),
    52013965: _tools.RODict({
        "propID": 52013965,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1836,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":53,"adjMonsterDmg":0.025})
    }),
    52013966: _tools.RODict({
        "propID": 52013966,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1978,"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":57,"adjMonsterDmg":0.05})
    }),
    52013967: _tools.RODict({
        "propID": 52013967,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2177,"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":63,"adjMonsterDmg":0.05})
    }),
    52013968: _tools.RODict({
        "propID": 52013968,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2375,"adjMinPhysicalAtk":28,"adjMaxPhysicalAtk":68,"adjMonsterDmg":0.05})
    }),
    52013969: _tools.RODict({
        "propID": 52013969,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2573,"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":74,"adjMonsterDmg":0.05})
    }),
    52013970: _tools.RODict({
        "propID": 52013970,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2958,"adjMinPhysicalAtk":37,"adjMaxPhysicalAtk":86,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52013971: _tools.RODict({
        "propID": 52013971,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3255,"adjMinPhysicalAtk":40,"adjMaxPhysicalAtk":93,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52013972: _tools.RODict({
        "propID": 52013972,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3579,"adjMinPhysicalAtk":43,"adjMaxPhysicalAtk":103,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52013973: _tools.RODict({
        "propID": 52013973,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3938,"adjMinPhysicalAtk":47,"adjMaxPhysicalAtk":113,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52013974: _tools.RODict({
        "propID": 52013974,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1061,"adjMinPhysicalAtk":15,"adjMaxPhysicalAtk":29})
    }),
    52013975: _tools.RODict({
        "propID": 52013975,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1166,"adjMinPhysicalAtk":16,"adjMaxPhysicalAtk":34})
    }),
    52013976: _tools.RODict({
        "propID": 52013976,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1272,"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":38})
    }),
    52013977: _tools.RODict({
        "propID": 52013977,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1380,"adjMinPhysicalAtk":18,"adjMaxPhysicalAtk":41})
    }),
    52013978: _tools.RODict({
        "propID": 52013978,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1484,"adjMinPhysicalAtk":19,"adjMaxPhysicalAtk":43,"adjMonsterDmg":0.025})
    }),
    52013979: _tools.RODict({
        "propID": 52013979,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1633,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":47,"adjMonsterDmg":0.025})
    }),
    52013980: _tools.RODict({
        "propID": 52013980,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1781,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":50,"adjMonsterDmg":0.025})
    }),
    52013981: _tools.RODict({
        "propID": 52013981,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1928,"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":56,"adjMonsterDmg":0.025})
    }),
    52013982: _tools.RODict({
        "propID": 52013982,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2077,"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":60,"adjMonsterDmg":0.05})
    }),
    52013983: _tools.RODict({
        "propID": 52013983,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2286,"adjMinPhysicalAtk":27,"adjMaxPhysicalAtk":66,"adjMonsterDmg":0.05})
    }),
    52013984: _tools.RODict({
        "propID": 52013984,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2494,"adjMinPhysicalAtk":29,"adjMaxPhysicalAtk":71,"adjMonsterDmg":0.05})
    }),
    52013985: _tools.RODict({
        "propID": 52013985,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2702,"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":78,"adjMonsterDmg":0.05})
    }),
    52013986: _tools.RODict({
        "propID": 52013986,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3106,"adjMinPhysicalAtk":39,"adjMaxPhysicalAtk":90,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52013987: _tools.RODict({
        "propID": 52013987,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3418,"adjMinPhysicalAtk":42,"adjMaxPhysicalAtk":98,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52013988: _tools.RODict({
        "propID": 52013988,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3758,"adjMinPhysicalAtk":45,"adjMaxPhysicalAtk":108,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52013989: _tools.RODict({
        "propID": 52013989,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4135,"adjMinPhysicalAtk":49,"adjMaxPhysicalAtk":119,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52013990: _tools.RODict({
        "propID": 52013990,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1114,"adjMinPhysicalAtk":16,"adjMaxPhysicalAtk":30})
    }),
    52013991: _tools.RODict({
        "propID": 52013991,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1224,"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":36})
    }),
    52013992: _tools.RODict({
        "propID": 52013992,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1336,"adjMinPhysicalAtk":18,"adjMaxPhysicalAtk":40})
    }),
    52013993: _tools.RODict({
        "propID": 52013993,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1449,"adjMinPhysicalAtk":19,"adjMaxPhysicalAtk":43})
    }),
    52013994: _tools.RODict({
        "propID": 52013994,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1558,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":45,"adjMonsterDmg":0.025})
    }),
    52013995: _tools.RODict({
        "propID": 52013995,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1715,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":49,"adjMonsterDmg":0.025})
    }),
    52013996: _tools.RODict({
        "propID": 52013996,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1870,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":53,"adjMonsterDmg":0.025})
    }),
    52013997: _tools.RODict({
        "propID": 52013997,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2024,"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":59,"adjMonsterDmg":0.025})
    }),
    52013998: _tools.RODict({
        "propID": 52013998,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2181,"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":63,"adjMonsterDmg":0.05})
    }),
    52013999: _tools.RODict({
        "propID": 52013999,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2400,"adjMinPhysicalAtk":28,"adjMaxPhysicalAtk":69,"adjMonsterDmg":0.05})
    }),
    52014000: _tools.RODict({
        "propID": 52014000,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2619,"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":75,"adjMonsterDmg":0.05})
    }),
    52014001: _tools.RODict({
        "propID": 52014001,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2837,"adjMinPhysicalAtk":34,"adjMaxPhysicalAtk":82,"adjMonsterDmg":0.05})
    }),
    52014002: _tools.RODict({
        "propID": 52014002,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3261,"adjMinPhysicalAtk":41,"adjMaxPhysicalAtk":95,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014003: _tools.RODict({
        "propID": 52014003,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3589,"adjMinPhysicalAtk":44,"adjMaxPhysicalAtk":103,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014004: _tools.RODict({
        "propID": 52014004,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3946,"adjMinPhysicalAtk":47,"adjMaxPhysicalAtk":113,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014005: _tools.RODict({
        "propID": 52014005,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4342,"adjMinPhysicalAtk":51,"adjMaxPhysicalAtk":125,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014006: _tools.RODict({
        "propID": 52014006,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1170,"adjMinPhysicalAtk":17,"adjMaxPhysicalAtk":32})
    }),
    52014007: _tools.RODict({
        "propID": 52014007,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1285,"adjMinPhysicalAtk":18,"adjMaxPhysicalAtk":38})
    }),
    52014008: _tools.RODict({
        "propID": 52014008,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1403,"adjMinPhysicalAtk":19,"adjMaxPhysicalAtk":42})
    }),
    52014009: _tools.RODict({
        "propID": 52014009,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1521,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":45})
    }),
    52014010: _tools.RODict({
        "propID": 52014010,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1636,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":47,"adjMonsterDmg":0.025})
    }),
    52014011: _tools.RODict({
        "propID": 52014011,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1801,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":51,"adjMonsterDmg":0.025})
    }),
    52014012: _tools.RODict({
        "propID": 52014012,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1964,"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":56,"adjMonsterDmg":0.025})
    }),
    52014013: _tools.RODict({
        "propID": 52014013,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2125,"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":62,"adjMonsterDmg":0.025})
    }),
    52014014: _tools.RODict({
        "propID": 52014014,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2290,"adjMinPhysicalAtk":27,"adjMaxPhysicalAtk":66,"adjMonsterDmg":0.05})
    }),
    52014015: _tools.RODict({
        "propID": 52014015,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2520,"adjMinPhysicalAtk":29,"adjMaxPhysicalAtk":72,"adjMonsterDmg":0.05})
    }),
    52014016: _tools.RODict({
        "propID": 52014016,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2750,"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":79,"adjMonsterDmg":0.05})
    }),
    52014017: _tools.RODict({
        "propID": 52014017,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2979,"adjMinPhysicalAtk":36,"adjMaxPhysicalAtk":86,"adjMonsterDmg":0.05})
    }),
    52014018: _tools.RODict({
        "propID": 52014018,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3424,"adjMinPhysicalAtk":43,"adjMaxPhysicalAtk":100,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014019: _tools.RODict({
        "propID": 52014019,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3768,"adjMinPhysicalAtk":46,"adjMaxPhysicalAtk":108,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014020: _tools.RODict({
        "propID": 52014020,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4143,"adjMinPhysicalAtk":49,"adjMaxPhysicalAtk":119,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014021: _tools.RODict({
        "propID": 52014021,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4559,"adjMinPhysicalAtk":54,"adjMaxPhysicalAtk":131,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014022: _tools.RODict({
        "propID": 52014022,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1229,"adjMinPhysicalAtk":18,"adjMaxPhysicalAtk":34})
    }),
    52014023: _tools.RODict({
        "propID": 52014023,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1349,"adjMinPhysicalAtk":19,"adjMaxPhysicalAtk":40})
    }),
    52014024: _tools.RODict({
        "propID": 52014024,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1473,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":44})
    }),
    52014025: _tools.RODict({
        "propID": 52014025,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1597,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":47})
    }),
    52014026: _tools.RODict({
        "propID": 52014026,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1718,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":49,"adjMonsterDmg":0.025})
    }),
    52014027: _tools.RODict({
        "propID": 52014027,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1891,"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":54,"adjMonsterDmg":0.025})
    }),
    52014028: _tools.RODict({
        "propID": 52014028,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2062,"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":59,"adjMonsterDmg":0.025})
    }),
    52014029: _tools.RODict({
        "propID": 52014029,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2231,"adjMinPhysicalAtk":27,"adjMaxPhysicalAtk":65,"adjMonsterDmg":0.025})
    }),
    52014030: _tools.RODict({
        "propID": 52014030,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2405,"adjMinPhysicalAtk":28,"adjMaxPhysicalAtk":69,"adjMonsterDmg":0.05})
    }),
    52014031: _tools.RODict({
        "propID": 52014031,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2646,"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":76,"adjMonsterDmg":0.05})
    }),
    52014032: _tools.RODict({
        "propID": 52014032,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2888,"adjMinPhysicalAtk":34,"adjMaxPhysicalAtk":83,"adjMonsterDmg":0.05})
    }),
    52014033: _tools.RODict({
        "propID": 52014033,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3128,"adjMinPhysicalAtk":38,"adjMaxPhysicalAtk":90,"adjMonsterDmg":0.05})
    }),
    52014034: _tools.RODict({
        "propID": 52014034,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3595,"adjMinPhysicalAtk":45,"adjMaxPhysicalAtk":105,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014035: _tools.RODict({
        "propID": 52014035,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3956,"adjMinPhysicalAtk":48,"adjMaxPhysicalAtk":113,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014036: _tools.RODict({
        "propID": 52014036,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4350,"adjMinPhysicalAtk":51,"adjMaxPhysicalAtk":125,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014037: _tools.RODict({
        "propID": 52014037,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4787,"adjMinPhysicalAtk":57,"adjMaxPhysicalAtk":138,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014038: _tools.RODict({
        "propID": 52014038,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1290,"adjMinPhysicalAtk":19,"adjMaxPhysicalAtk":36})
    }),
    52014039: _tools.RODict({
        "propID": 52014039,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1416,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":42})
    }),
    52014040: _tools.RODict({
        "propID": 52014040,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1547,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":46})
    }),
    52014041: _tools.RODict({
        "propID": 52014041,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1677,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":49})
    }),
    52014042: _tools.RODict({
        "propID": 52014042,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1804,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":51,"adjMonsterDmg":0.025})
    }),
    52014043: _tools.RODict({
        "propID": 52014043,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1986,"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":57,"adjMonsterDmg":0.025})
    }),
    52014044: _tools.RODict({
        "propID": 52014044,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2165,"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":62,"adjMonsterDmg":0.025})
    }),
    52014045: _tools.RODict({
        "propID": 52014045,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2343,"adjMinPhysicalAtk":28,"adjMaxPhysicalAtk":68,"adjMonsterDmg":0.025})
    }),
    52014046: _tools.RODict({
        "propID": 52014046,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2525,"adjMinPhysicalAtk":29,"adjMaxPhysicalAtk":72,"adjMonsterDmg":0.05})
    }),
    52014047: _tools.RODict({
        "propID": 52014047,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2778,"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":80,"adjMonsterDmg":0.05})
    }),
    52014048: _tools.RODict({
        "propID": 52014048,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3032,"adjMinPhysicalAtk":36,"adjMaxPhysicalAtk":87,"adjMonsterDmg":0.05})
    }),
    52014049: _tools.RODict({
        "propID": 52014049,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3284,"adjMinPhysicalAtk":40,"adjMaxPhysicalAtk":95,"adjMonsterDmg":0.05})
    }),
    52014050: _tools.RODict({
        "propID": 52014050,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3775,"adjMinPhysicalAtk":47,"adjMaxPhysicalAtk":110,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014051: _tools.RODict({
        "propID": 52014051,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4154,"adjMinPhysicalAtk":50,"adjMaxPhysicalAtk":119,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014052: _tools.RODict({
        "propID": 52014052,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4568,"adjMinPhysicalAtk":54,"adjMaxPhysicalAtk":131,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014053: _tools.RODict({
        "propID": 52014053,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5026,"adjMinPhysicalAtk":60,"adjMaxPhysicalAtk":145,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014054: _tools.RODict({
        "propID": 52014054,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1355,"adjMinPhysicalAtk":20,"adjMaxPhysicalAtk":38})
    }),
    52014055: _tools.RODict({
        "propID": 52014055,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1487,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":44})
    }),
    52014056: _tools.RODict({
        "propID": 52014056,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1624,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":48})
    }),
    52014057: _tools.RODict({
        "propID": 52014057,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1761,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":51})
    }),
    52014058: _tools.RODict({
        "propID": 52014058,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1894,"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":54,"adjMonsterDmg":0.025})
    }),
    52014059: _tools.RODict({
        "propID": 52014059,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2085,"adjMinPhysicalAtk":26,"adjMaxPhysicalAtk":60,"adjMonsterDmg":0.025})
    }),
    52014060: _tools.RODict({
        "propID": 52014060,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2273,"adjMinPhysicalAtk":27,"adjMaxPhysicalAtk":65,"adjMonsterDmg":0.025})
    }),
    52014061: _tools.RODict({
        "propID": 52014061,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2460,"adjMinPhysicalAtk":29,"adjMaxPhysicalAtk":71,"adjMonsterDmg":0.025})
    }),
    52014062: _tools.RODict({
        "propID": 52014062,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2651,"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":76,"adjMonsterDmg":0.05})
    }),
    52014063: _tools.RODict({
        "propID": 52014063,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2917,"adjMinPhysicalAtk":34,"adjMaxPhysicalAtk":84,"adjMonsterDmg":0.05})
    }),
    52014064: _tools.RODict({
        "propID": 52014064,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3184,"adjMinPhysicalAtk":38,"adjMaxPhysicalAtk":91,"adjMonsterDmg":0.05})
    }),
    52014065: _tools.RODict({
        "propID": 52014065,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3448,"adjMinPhysicalAtk":42,"adjMaxPhysicalAtk":100,"adjMonsterDmg":0.05})
    }),
    52014066: _tools.RODict({
        "propID": 52014066,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3964,"adjMinPhysicalAtk":49,"adjMaxPhysicalAtk":116,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014067: _tools.RODict({
        "propID": 52014067,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4362,"adjMinPhysicalAtk":53,"adjMaxPhysicalAtk":125,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014068: _tools.RODict({
        "propID": 52014068,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4796,"adjMinPhysicalAtk":57,"adjMaxPhysicalAtk":138,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014069: _tools.RODict({
        "propID": 52014069,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5277,"adjMinPhysicalAtk":63,"adjMaxPhysicalAtk":152,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014070: _tools.RODict({
        "propID": 52014070,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1423,"adjMinPhysicalAtk":21,"adjMaxPhysicalAtk":40})
    }),
    52014071: _tools.RODict({
        "propID": 52014071,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1561,"adjMinPhysicalAtk":22,"adjMaxPhysicalAtk":46})
    }),
    52014072: _tools.RODict({
        "propID": 52014072,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1705,"adjMinPhysicalAtk":23,"adjMaxPhysicalAtk":50})
    }),
    52014073: _tools.RODict({
        "propID": 52014073,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1849,"adjMinPhysicalAtk":24,"adjMaxPhysicalAtk":54})
    }),
    52014074: _tools.RODict({
        "propID": 52014074,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1989,"adjMinPhysicalAtk":25,"adjMaxPhysicalAtk":57,"adjMonsterDmg":0.025})
    }),
    52014075: _tools.RODict({
        "propID": 52014075,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2189,"adjMinPhysicalAtk":27,"adjMaxPhysicalAtk":63,"adjMonsterDmg":0.025})
    }),
    52014076: _tools.RODict({
        "propID": 52014076,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2387,"adjMinPhysicalAtk":28,"adjMaxPhysicalAtk":68,"adjMonsterDmg":0.025})
    }),
    52014077: _tools.RODict({
        "propID": 52014077,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2583,"adjMinPhysicalAtk":30,"adjMaxPhysicalAtk":75,"adjMonsterDmg":0.025})
    }),
    52014078: _tools.RODict({
        "propID": 52014078,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2784,"adjMinPhysicalAtk":32,"adjMaxPhysicalAtk":80,"adjMonsterDmg":0.05})
    }),
    52014079: _tools.RODict({
        "propID": 52014079,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3063,"adjMinPhysicalAtk":36,"adjMaxPhysicalAtk":88,"adjMonsterDmg":0.05})
    }),
    52014080: _tools.RODict({
        "propID": 52014080,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3343,"adjMinPhysicalAtk":40,"adjMaxPhysicalAtk":96,"adjMonsterDmg":0.05})
    }),
    52014081: _tools.RODict({
        "propID": 52014081,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3620,"adjMinPhysicalAtk":44,"adjMaxPhysicalAtk":105,"adjMonsterDmg":0.05})
    }),
    52014082: _tools.RODict({
        "propID": 52014082,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4162,"adjMinPhysicalAtk":51,"adjMaxPhysicalAtk":122,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014083: _tools.RODict({
        "propID": 52014083,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4580,"adjMinPhysicalAtk":56,"adjMaxPhysicalAtk":131,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014084: _tools.RODict({
        "propID": 52014084,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5036,"adjMinPhysicalAtk":60,"adjMaxPhysicalAtk":145,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014085: _tools.RODict({
        "propID": 52014085,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5541,"adjMinPhysicalAtk":66,"adjMaxPhysicalAtk":160,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
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
    52014102: _tools.RODict({
        "propID": 52014102,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":916,"adjMinMagicAtk":12,"adjMaxMagicAtk":26})
    }),
    52014103: _tools.RODict({
        "propID": 52014103,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1007,"adjMinMagicAtk":13,"adjMaxMagicAtk":29})
    }),
    52014104: _tools.RODict({
        "propID": 52014104,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1098,"adjMinMagicAtk":14,"adjMaxMagicAtk":32})
    }),
    52014105: _tools.RODict({
        "propID": 52014105,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1191,"adjMinMagicAtk":15,"adjMaxMagicAtk":35})
    }),
    52014106: _tools.RODict({
        "propID": 52014106,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1282,"adjMinMagicAtk":16,"adjMaxMagicAtk":37,"adjMonsterDmg":0.025})
    }),
    52014107: _tools.RODict({
        "propID": 52014107,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1410,"adjMinMagicAtk":18,"adjMaxMagicAtk":41,"adjMonsterDmg":0.025})
    }),
    52014108: _tools.RODict({
        "propID": 52014108,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1538,"adjMinMagicAtk":19,"adjMaxMagicAtk":44,"adjMonsterDmg":0.025})
    }),
    52014109: _tools.RODict({
        "propID": 52014109,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1666,"adjMinMagicAtk":21,"adjMaxMagicAtk":48,"adjMonsterDmg":0.025})
    }),
    52014110: _tools.RODict({
        "propID": 52014110,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1794,"adjMinMagicAtk":22,"adjMaxMagicAtk":51,"adjMonsterDmg":0.05})
    }),
    52014111: _tools.RODict({
        "propID": 52014111,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1974,"adjMinMagicAtk":24,"adjMaxMagicAtk":57,"adjMonsterDmg":0.05})
    }),
    52014112: _tools.RODict({
        "propID": 52014112,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2154,"adjMinMagicAtk":26,"adjMaxMagicAtk":62,"adjMonsterDmg":0.05})
    }),
    52014113: _tools.RODict({
        "propID": 52014113,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2333,"adjMinMagicAtk":28,"adjMaxMagicAtk":67,"adjMonsterDmg":0.05})
    }),
    52014114: _tools.RODict({
        "propID": 52014114,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2683,"adjMinMagicAtk":33,"adjMaxMagicAtk":78,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014115: _tools.RODict({
        "propID": 52014115,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2952,"adjMinMagicAtk":36,"adjMaxMagicAtk":85,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014116: _tools.RODict({
        "propID": 52014116,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3247,"adjMinMagicAtk":39,"adjMaxMagicAtk":93,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014117: _tools.RODict({
        "propID": 52014117,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3571,"adjMinMagicAtk":43,"adjMaxMagicAtk":103,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014118: _tools.RODict({
        "propID": 52014118,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":962,"adjMinMagicAtk":13,"adjMaxMagicAtk":27})
    }),
    52014119: _tools.RODict({
        "propID": 52014119,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1057,"adjMinMagicAtk":14,"adjMaxMagicAtk":30})
    }),
    52014120: _tools.RODict({
        "propID": 52014120,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1153,"adjMinMagicAtk":15,"adjMaxMagicAtk":34})
    }),
    52014121: _tools.RODict({
        "propID": 52014121,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1251,"adjMinMagicAtk":16,"adjMaxMagicAtk":37})
    }),
    52014122: _tools.RODict({
        "propID": 52014122,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1346,"adjMinMagicAtk":17,"adjMaxMagicAtk":39,"adjMonsterDmg":0.025})
    }),
    52014123: _tools.RODict({
        "propID": 52014123,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1481,"adjMinMagicAtk":19,"adjMaxMagicAtk":43,"adjMonsterDmg":0.025})
    }),
    52014124: _tools.RODict({
        "propID": 52014124,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1615,"adjMinMagicAtk":20,"adjMaxMagicAtk":46,"adjMonsterDmg":0.025})
    }),
    52014125: _tools.RODict({
        "propID": 52014125,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1749,"adjMinMagicAtk":22,"adjMaxMagicAtk":50,"adjMonsterDmg":0.025})
    }),
    52014126: _tools.RODict({
        "propID": 52014126,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1884,"adjMinMagicAtk":23,"adjMaxMagicAtk":54,"adjMonsterDmg":0.05})
    }),
    52014127: _tools.RODict({
        "propID": 52014127,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2073,"adjMinMagicAtk":25,"adjMaxMagicAtk":60,"adjMonsterDmg":0.05})
    }),
    52014128: _tools.RODict({
        "propID": 52014128,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2262,"adjMinMagicAtk":27,"adjMaxMagicAtk":65,"adjMonsterDmg":0.05})
    }),
    52014129: _tools.RODict({
        "propID": 52014129,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2450,"adjMinMagicAtk":29,"adjMaxMagicAtk":70,"adjMonsterDmg":0.05})
    }),
    52014130: _tools.RODict({
        "propID": 52014130,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2817,"adjMinMagicAtk":35,"adjMaxMagicAtk":82,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014131: _tools.RODict({
        "propID": 52014131,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3100,"adjMinMagicAtk":38,"adjMaxMagicAtk":89,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014132: _tools.RODict({
        "propID": 52014132,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3409,"adjMinMagicAtk":41,"adjMaxMagicAtk":98,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014133: _tools.RODict({
        "propID": 52014133,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3750,"adjMinMagicAtk":45,"adjMaxMagicAtk":108,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014134: _tools.RODict({
        "propID": 52014134,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1010,"adjMinMagicAtk":14,"adjMaxMagicAtk":28})
    }),
    52014135: _tools.RODict({
        "propID": 52014135,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1110,"adjMinMagicAtk":15,"adjMaxMagicAtk":32})
    }),
    52014136: _tools.RODict({
        "propID": 52014136,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1211,"adjMinMagicAtk":16,"adjMaxMagicAtk":36})
    }),
    52014137: _tools.RODict({
        "propID": 52014137,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1314,"adjMinMagicAtk":17,"adjMaxMagicAtk":39})
    }),
    52014138: _tools.RODict({
        "propID": 52014138,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1413,"adjMinMagicAtk":18,"adjMaxMagicAtk":41,"adjMonsterDmg":0.025})
    }),
    52014139: _tools.RODict({
        "propID": 52014139,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1555,"adjMinMagicAtk":20,"adjMaxMagicAtk":45,"adjMonsterDmg":0.025})
    }),
    52014140: _tools.RODict({
        "propID": 52014140,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1696,"adjMinMagicAtk":21,"adjMaxMagicAtk":48,"adjMonsterDmg":0.025})
    }),
    52014141: _tools.RODict({
        "propID": 52014141,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1836,"adjMinMagicAtk":23,"adjMaxMagicAtk":53,"adjMonsterDmg":0.025})
    }),
    52014142: _tools.RODict({
        "propID": 52014142,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1978,"adjMinMagicAtk":24,"adjMaxMagicAtk":57,"adjMonsterDmg":0.05})
    }),
    52014143: _tools.RODict({
        "propID": 52014143,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2177,"adjMinMagicAtk":26,"adjMaxMagicAtk":63,"adjMonsterDmg":0.05})
    }),
    52014144: _tools.RODict({
        "propID": 52014144,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2375,"adjMinMagicAtk":28,"adjMaxMagicAtk":68,"adjMonsterDmg":0.05})
    }),
    52014145: _tools.RODict({
        "propID": 52014145,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2573,"adjMinMagicAtk":30,"adjMaxMagicAtk":74,"adjMonsterDmg":0.05})
    }),
    52014146: _tools.RODict({
        "propID": 52014146,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2958,"adjMinMagicAtk":37,"adjMaxMagicAtk":86,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014147: _tools.RODict({
        "propID": 52014147,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3255,"adjMinMagicAtk":40,"adjMaxMagicAtk":93,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014148: _tools.RODict({
        "propID": 52014148,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3579,"adjMinMagicAtk":43,"adjMaxMagicAtk":103,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014149: _tools.RODict({
        "propID": 52014149,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3938,"adjMinMagicAtk":47,"adjMaxMagicAtk":113,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014150: _tools.RODict({
        "propID": 52014150,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1061,"adjMinMagicAtk":15,"adjMaxMagicAtk":29})
    }),
    52014151: _tools.RODict({
        "propID": 52014151,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1166,"adjMinMagicAtk":16,"adjMaxMagicAtk":34})
    }),
    52014152: _tools.RODict({
        "propID": 52014152,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1272,"adjMinMagicAtk":17,"adjMaxMagicAtk":38})
    }),
    52014153: _tools.RODict({
        "propID": 52014153,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1380,"adjMinMagicAtk":18,"adjMaxMagicAtk":41})
    }),
    52014154: _tools.RODict({
        "propID": 52014154,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1484,"adjMinMagicAtk":19,"adjMaxMagicAtk":43,"adjMonsterDmg":0.025})
    }),
    52014155: _tools.RODict({
        "propID": 52014155,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1633,"adjMinMagicAtk":21,"adjMaxMagicAtk":47,"adjMonsterDmg":0.025})
    }),
    52014156: _tools.RODict({
        "propID": 52014156,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1781,"adjMinMagicAtk":22,"adjMaxMagicAtk":50,"adjMonsterDmg":0.025})
    }),
    52014157: _tools.RODict({
        "propID": 52014157,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1928,"adjMinMagicAtk":24,"adjMaxMagicAtk":56,"adjMonsterDmg":0.025})
    }),
    52014158: _tools.RODict({
        "propID": 52014158,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2077,"adjMinMagicAtk":25,"adjMaxMagicAtk":60,"adjMonsterDmg":0.05})
    }),
    52014159: _tools.RODict({
        "propID": 52014159,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2286,"adjMinMagicAtk":27,"adjMaxMagicAtk":66,"adjMonsterDmg":0.05})
    }),
    52014160: _tools.RODict({
        "propID": 52014160,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2494,"adjMinMagicAtk":29,"adjMaxMagicAtk":71,"adjMonsterDmg":0.05})
    }),
    52014161: _tools.RODict({
        "propID": 52014161,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2702,"adjMinMagicAtk":32,"adjMaxMagicAtk":78,"adjMonsterDmg":0.05})
    }),
    52014162: _tools.RODict({
        "propID": 52014162,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3106,"adjMinMagicAtk":39,"adjMaxMagicAtk":90,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014163: _tools.RODict({
        "propID": 52014163,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3418,"adjMinMagicAtk":42,"adjMaxMagicAtk":98,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014164: _tools.RODict({
        "propID": 52014164,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3758,"adjMinMagicAtk":45,"adjMaxMagicAtk":108,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014165: _tools.RODict({
        "propID": 52014165,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4135,"adjMinMagicAtk":49,"adjMaxMagicAtk":119,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014166: _tools.RODict({
        "propID": 52014166,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1114,"adjMinMagicAtk":16,"adjMaxMagicAtk":30})
    }),
    52014167: _tools.RODict({
        "propID": 52014167,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1224,"adjMinMagicAtk":17,"adjMaxMagicAtk":36})
    }),
    52014168: _tools.RODict({
        "propID": 52014168,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1336,"adjMinMagicAtk":18,"adjMaxMagicAtk":40})
    }),
    52014169: _tools.RODict({
        "propID": 52014169,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1449,"adjMinMagicAtk":19,"adjMaxMagicAtk":43})
    }),
    52014170: _tools.RODict({
        "propID": 52014170,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1558,"adjMinMagicAtk":20,"adjMaxMagicAtk":45,"adjMonsterDmg":0.025})
    }),
    52014171: _tools.RODict({
        "propID": 52014171,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1715,"adjMinMagicAtk":22,"adjMaxMagicAtk":49,"adjMonsterDmg":0.025})
    }),
    52014172: _tools.RODict({
        "propID": 52014172,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1870,"adjMinMagicAtk":23,"adjMaxMagicAtk":53,"adjMonsterDmg":0.025})
    }),
    52014173: _tools.RODict({
        "propID": 52014173,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2024,"adjMinMagicAtk":25,"adjMaxMagicAtk":59,"adjMonsterDmg":0.025})
    }),
    52014174: _tools.RODict({
        "propID": 52014174,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2181,"adjMinMagicAtk":26,"adjMaxMagicAtk":63,"adjMonsterDmg":0.05})
    }),
    52014175: _tools.RODict({
        "propID": 52014175,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2400,"adjMinMagicAtk":28,"adjMaxMagicAtk":69,"adjMonsterDmg":0.05})
    }),
    52014176: _tools.RODict({
        "propID": 52014176,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2619,"adjMinMagicAtk":30,"adjMaxMagicAtk":75,"adjMonsterDmg":0.05})
    }),
    52014177: _tools.RODict({
        "propID": 52014177,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2837,"adjMinMagicAtk":34,"adjMaxMagicAtk":82,"adjMonsterDmg":0.05})
    }),
    52014178: _tools.RODict({
        "propID": 52014178,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3261,"adjMinMagicAtk":41,"adjMaxMagicAtk":95,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014179: _tools.RODict({
        "propID": 52014179,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3589,"adjMinMagicAtk":44,"adjMaxMagicAtk":103,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014180: _tools.RODict({
        "propID": 52014180,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3946,"adjMinMagicAtk":47,"adjMaxMagicAtk":113,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014181: _tools.RODict({
        "propID": 52014181,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4342,"adjMinMagicAtk":51,"adjMaxMagicAtk":125,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014182: _tools.RODict({
        "propID": 52014182,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1170,"adjMinMagicAtk":17,"adjMaxMagicAtk":32})
    }),
    52014183: _tools.RODict({
        "propID": 52014183,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1285,"adjMinMagicAtk":18,"adjMaxMagicAtk":38})
    }),
    52014184: _tools.RODict({
        "propID": 52014184,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1403,"adjMinMagicAtk":19,"adjMaxMagicAtk":42})
    }),
    52014185: _tools.RODict({
        "propID": 52014185,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1521,"adjMinMagicAtk":20,"adjMaxMagicAtk":45})
    }),
    52014186: _tools.RODict({
        "propID": 52014186,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1636,"adjMinMagicAtk":21,"adjMaxMagicAtk":47,"adjMonsterDmg":0.025})
    }),
    52014187: _tools.RODict({
        "propID": 52014187,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1801,"adjMinMagicAtk":23,"adjMaxMagicAtk":51,"adjMonsterDmg":0.025})
    }),
    52014188: _tools.RODict({
        "propID": 52014188,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1964,"adjMinMagicAtk":24,"adjMaxMagicAtk":56,"adjMonsterDmg":0.025})
    }),
    52014189: _tools.RODict({
        "propID": 52014189,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2125,"adjMinMagicAtk":26,"adjMaxMagicAtk":62,"adjMonsterDmg":0.025})
    }),
    52014190: _tools.RODict({
        "propID": 52014190,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2290,"adjMinMagicAtk":27,"adjMaxMagicAtk":66,"adjMonsterDmg":0.05})
    }),
    52014191: _tools.RODict({
        "propID": 52014191,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2520,"adjMinMagicAtk":29,"adjMaxMagicAtk":72,"adjMonsterDmg":0.05})
    }),
    52014192: _tools.RODict({
        "propID": 52014192,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2750,"adjMinMagicAtk":32,"adjMaxMagicAtk":79,"adjMonsterDmg":0.05})
    }),
    52014193: _tools.RODict({
        "propID": 52014193,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2979,"adjMinMagicAtk":36,"adjMaxMagicAtk":86,"adjMonsterDmg":0.05})
    }),
    52014194: _tools.RODict({
        "propID": 52014194,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3424,"adjMinMagicAtk":43,"adjMaxMagicAtk":100,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014195: _tools.RODict({
        "propID": 52014195,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3768,"adjMinMagicAtk":46,"adjMaxMagicAtk":108,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014196: _tools.RODict({
        "propID": 52014196,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4143,"adjMinMagicAtk":49,"adjMaxMagicAtk":119,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014197: _tools.RODict({
        "propID": 52014197,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4559,"adjMinMagicAtk":54,"adjMaxMagicAtk":131,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014198: _tools.RODict({
        "propID": 52014198,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1229,"adjMinMagicAtk":18,"adjMaxMagicAtk":34})
    }),
    52014199: _tools.RODict({
        "propID": 52014199,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1349,"adjMinMagicAtk":19,"adjMaxMagicAtk":40})
    }),
    52014200: _tools.RODict({
        "propID": 52014200,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1473,"adjMinMagicAtk":20,"adjMaxMagicAtk":44})
    }),
    52014201: _tools.RODict({
        "propID": 52014201,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1597,"adjMinMagicAtk":21,"adjMaxMagicAtk":47})
    }),
    52014202: _tools.RODict({
        "propID": 52014202,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1718,"adjMinMagicAtk":22,"adjMaxMagicAtk":49,"adjMonsterDmg":0.025})
    }),
    52014203: _tools.RODict({
        "propID": 52014203,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1891,"adjMinMagicAtk":24,"adjMaxMagicAtk":54,"adjMonsterDmg":0.025})
    }),
    52014204: _tools.RODict({
        "propID": 52014204,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2062,"adjMinMagicAtk":25,"adjMaxMagicAtk":59,"adjMonsterDmg":0.025})
    }),
    52014205: _tools.RODict({
        "propID": 52014205,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2231,"adjMinMagicAtk":27,"adjMaxMagicAtk":65,"adjMonsterDmg":0.025})
    }),
    52014206: _tools.RODict({
        "propID": 52014206,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2405,"adjMinMagicAtk":28,"adjMaxMagicAtk":69,"adjMonsterDmg":0.05})
    }),
    52014207: _tools.RODict({
        "propID": 52014207,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2646,"adjMinMagicAtk":30,"adjMaxMagicAtk":76,"adjMonsterDmg":0.05})
    }),
    52014208: _tools.RODict({
        "propID": 52014208,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2888,"adjMinMagicAtk":34,"adjMaxMagicAtk":83,"adjMonsterDmg":0.05})
    }),
    52014209: _tools.RODict({
        "propID": 52014209,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3128,"adjMinMagicAtk":38,"adjMaxMagicAtk":90,"adjMonsterDmg":0.05})
    }),
    52014210: _tools.RODict({
        "propID": 52014210,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3595,"adjMinMagicAtk":45,"adjMaxMagicAtk":105,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014211: _tools.RODict({
        "propID": 52014211,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3956,"adjMinMagicAtk":48,"adjMaxMagicAtk":113,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014212: _tools.RODict({
        "propID": 52014212,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4350,"adjMinMagicAtk":51,"adjMaxMagicAtk":125,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014213: _tools.RODict({
        "propID": 52014213,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4787,"adjMinMagicAtk":57,"adjMaxMagicAtk":138,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014214: _tools.RODict({
        "propID": 52014214,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1290,"adjMinMagicAtk":19,"adjMaxMagicAtk":36})
    }),
    52014215: _tools.RODict({
        "propID": 52014215,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1416,"adjMinMagicAtk":20,"adjMaxMagicAtk":42})
    }),
    52014216: _tools.RODict({
        "propID": 52014216,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1547,"adjMinMagicAtk":21,"adjMaxMagicAtk":46})
    }),
    52014217: _tools.RODict({
        "propID": 52014217,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1677,"adjMinMagicAtk":22,"adjMaxMagicAtk":49})
    }),
    52014218: _tools.RODict({
        "propID": 52014218,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1804,"adjMinMagicAtk":23,"adjMaxMagicAtk":51,"adjMonsterDmg":0.025})
    }),
    52014219: _tools.RODict({
        "propID": 52014219,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1986,"adjMinMagicAtk":25,"adjMaxMagicAtk":57,"adjMonsterDmg":0.025})
    }),
    52014220: _tools.RODict({
        "propID": 52014220,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2165,"adjMinMagicAtk":26,"adjMaxMagicAtk":62,"adjMonsterDmg":0.025})
    }),
    52014221: _tools.RODict({
        "propID": 52014221,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2343,"adjMinMagicAtk":28,"adjMaxMagicAtk":68,"adjMonsterDmg":0.025})
    }),
    52014222: _tools.RODict({
        "propID": 52014222,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2525,"adjMinMagicAtk":29,"adjMaxMagicAtk":72,"adjMonsterDmg":0.05})
    }),
    52014223: _tools.RODict({
        "propID": 52014223,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2778,"adjMinMagicAtk":32,"adjMaxMagicAtk":80,"adjMonsterDmg":0.05})
    }),
    52014224: _tools.RODict({
        "propID": 52014224,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3032,"adjMinMagicAtk":36,"adjMaxMagicAtk":87,"adjMonsterDmg":0.05})
    }),
    52014225: _tools.RODict({
        "propID": 52014225,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3284,"adjMinMagicAtk":40,"adjMaxMagicAtk":95,"adjMonsterDmg":0.05})
    }),
    52014226: _tools.RODict({
        "propID": 52014226,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3775,"adjMinMagicAtk":47,"adjMaxMagicAtk":110,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014227: _tools.RODict({
        "propID": 52014227,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4154,"adjMinMagicAtk":50,"adjMaxMagicAtk":119,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014228: _tools.RODict({
        "propID": 52014228,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4568,"adjMinMagicAtk":54,"adjMaxMagicAtk":131,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014229: _tools.RODict({
        "propID": 52014229,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5026,"adjMinMagicAtk":60,"adjMaxMagicAtk":145,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014230: _tools.RODict({
        "propID": 52014230,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1355,"adjMinMagicAtk":20,"adjMaxMagicAtk":38})
    }),
    52014231: _tools.RODict({
        "propID": 52014231,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1487,"adjMinMagicAtk":21,"adjMaxMagicAtk":44})
    }),
    52014232: _tools.RODict({
        "propID": 52014232,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1624,"adjMinMagicAtk":22,"adjMaxMagicAtk":48})
    }),
    52014233: _tools.RODict({
        "propID": 52014233,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1761,"adjMinMagicAtk":23,"adjMaxMagicAtk":51})
    }),
    52014234: _tools.RODict({
        "propID": 52014234,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1894,"adjMinMagicAtk":24,"adjMaxMagicAtk":54,"adjMonsterDmg":0.025})
    }),
    52014235: _tools.RODict({
        "propID": 52014235,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2085,"adjMinMagicAtk":26,"adjMaxMagicAtk":60,"adjMonsterDmg":0.025})
    }),
    52014236: _tools.RODict({
        "propID": 52014236,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2273,"adjMinMagicAtk":27,"adjMaxMagicAtk":65,"adjMonsterDmg":0.025})
    }),
    52014237: _tools.RODict({
        "propID": 52014237,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2460,"adjMinMagicAtk":29,"adjMaxMagicAtk":71,"adjMonsterDmg":0.025})
    }),
    52014238: _tools.RODict({
        "propID": 52014238,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2651,"adjMinMagicAtk":30,"adjMaxMagicAtk":76,"adjMonsterDmg":0.05})
    }),
    52014239: _tools.RODict({
        "propID": 52014239,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2917,"adjMinMagicAtk":34,"adjMaxMagicAtk":84,"adjMonsterDmg":0.05})
    }),
    52014240: _tools.RODict({
        "propID": 52014240,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3184,"adjMinMagicAtk":38,"adjMaxMagicAtk":91,"adjMonsterDmg":0.05})
    }),
    52014241: _tools.RODict({
        "propID": 52014241,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3448,"adjMinMagicAtk":42,"adjMaxMagicAtk":100,"adjMonsterDmg":0.05})
    }),
    52014242: _tools.RODict({
        "propID": 52014242,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3964,"adjMinMagicAtk":49,"adjMaxMagicAtk":116,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014243: _tools.RODict({
        "propID": 52014243,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4362,"adjMinMagicAtk":53,"adjMaxMagicAtk":125,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014244: _tools.RODict({
        "propID": 52014244,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4796,"adjMinMagicAtk":57,"adjMaxMagicAtk":138,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014245: _tools.RODict({
        "propID": 52014245,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5277,"adjMinMagicAtk":63,"adjMaxMagicAtk":152,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014246: _tools.RODict({
        "propID": 52014246,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1423,"adjMinMagicAtk":21,"adjMaxMagicAtk":40})
    }),
    52014247: _tools.RODict({
        "propID": 52014247,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1561,"adjMinMagicAtk":22,"adjMaxMagicAtk":46})
    }),
    52014248: _tools.RODict({
        "propID": 52014248,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1705,"adjMinMagicAtk":23,"adjMaxMagicAtk":50})
    }),
    52014249: _tools.RODict({
        "propID": 52014249,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1849,"adjMinMagicAtk":24,"adjMaxMagicAtk":54})
    }),
    52014250: _tools.RODict({
        "propID": 52014250,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1989,"adjMinMagicAtk":25,"adjMaxMagicAtk":57,"adjMonsterDmg":0.025})
    }),
    52014251: _tools.RODict({
        "propID": 52014251,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2189,"adjMinMagicAtk":27,"adjMaxMagicAtk":63,"adjMonsterDmg":0.025})
    }),
    52014252: _tools.RODict({
        "propID": 52014252,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2387,"adjMinMagicAtk":28,"adjMaxMagicAtk":68,"adjMonsterDmg":0.025})
    }),
    52014253: _tools.RODict({
        "propID": 52014253,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2583,"adjMinMagicAtk":30,"adjMaxMagicAtk":75,"adjMonsterDmg":0.025})
    }),
    52014254: _tools.RODict({
        "propID": 52014254,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2784,"adjMinMagicAtk":32,"adjMaxMagicAtk":80,"adjMonsterDmg":0.05})
    }),
    52014255: _tools.RODict({
        "propID": 52014255,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3063,"adjMinMagicAtk":36,"adjMaxMagicAtk":88,"adjMonsterDmg":0.05})
    }),
    52014256: _tools.RODict({
        "propID": 52014256,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3343,"adjMinMagicAtk":40,"adjMaxMagicAtk":96,"adjMonsterDmg":0.05})
    }),
    52014257: _tools.RODict({
        "propID": 52014257,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3620,"adjMinMagicAtk":44,"adjMaxMagicAtk":105,"adjMonsterDmg":0.05})
    }),
    52014258: _tools.RODict({
        "propID": 52014258,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4162,"adjMinMagicAtk":51,"adjMaxMagicAtk":122,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014259: _tools.RODict({
        "propID": 52014259,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4580,"adjMinMagicAtk":56,"adjMaxMagicAtk":131,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014260: _tools.RODict({
        "propID": 52014260,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5036,"adjMinMagicAtk":60,"adjMaxMagicAtk":145,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
    }),
    52014261: _tools.RODict({
        "propID": 52014261,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5541,"adjMinMagicAtk":66,"adjMaxMagicAtk":160,"adjMonsterDmg":0.05,"adjMonsterDmgAnti":0.05})
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
    52014278: _tools.RODict({
        "propID": 52014278,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":916})
    }),
    52014279: _tools.RODict({
        "propID": 52014279,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1007})
    }),
    52014280: _tools.RODict({
        "propID": 52014280,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1098})
    }),
    52014281: _tools.RODict({
        "propID": 52014281,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1191})
    }),
    52014282: _tools.RODict({
        "propID": 52014282,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1282,"adjDrugsQuantity":1,"adjFinalDmg":0.02})
    }),
    52014283: _tools.RODict({
        "propID": 52014283,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1410,"adjDrugsQuantity":1,"adjFinalDmg":0.02})
    }),
    52014284: _tools.RODict({
        "propID": 52014284,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1538,"adjDrugsQuantity":2,"adjFinalDmg":0.02})
    }),
    52014285: _tools.RODict({
        "propID": 52014285,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1666,"adjDrugsQuantity":2,"adjFinalDmg":0.02})
    }),
    52014286: _tools.RODict({
        "propID": 52014286,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1794,"adjDrugsQuantity":3,"adjFinalDmg":0.04})
    }),
    52014287: _tools.RODict({
        "propID": 52014287,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1974,"adjDrugsQuantity":3,"adjFinalDmg":0.04})
    }),
    52014288: _tools.RODict({
        "propID": 52014288,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2154,"adjDrugsQuantity":4,"adjFinalDmg":0.04})
    }),
    52014289: _tools.RODict({
        "propID": 52014289,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2333,"adjDrugsQuantity":4,"adjFinalDmg":0.04})
    }),
    52014290: _tools.RODict({
        "propID": 52014290,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2683,"adjDrugsQuantity":5,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014291: _tools.RODict({
        "propID": 52014291,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2952,"adjDrugsQuantity":5,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014292: _tools.RODict({
        "propID": 52014292,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3247,"adjDrugsQuantity":6,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014293: _tools.RODict({
        "propID": 52014293,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3571,"adjDrugsQuantity":6,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014294: _tools.RODict({
        "propID": 52014294,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":962})
    }),
    52014295: _tools.RODict({
        "propID": 52014295,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1057})
    }),
    52014296: _tools.RODict({
        "propID": 52014296,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1153})
    }),
    52014297: _tools.RODict({
        "propID": 52014297,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1251})
    }),
    52014298: _tools.RODict({
        "propID": 52014298,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1346,"adjDrugsQuantity":1,"adjFinalDmg":0.02})
    }),
    52014299: _tools.RODict({
        "propID": 52014299,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1481,"adjDrugsQuantity":1,"adjFinalDmg":0.02})
    }),
    52014300: _tools.RODict({
        "propID": 52014300,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1615,"adjDrugsQuantity":2,"adjFinalDmg":0.02})
    }),
    52014301: _tools.RODict({
        "propID": 52014301,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1749,"adjDrugsQuantity":2,"adjFinalDmg":0.02})
    }),
    52014302: _tools.RODict({
        "propID": 52014302,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1884,"adjDrugsQuantity":3,"adjFinalDmg":0.04})
    }),
    52014303: _tools.RODict({
        "propID": 52014303,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2073,"adjDrugsQuantity":3,"adjFinalDmg":0.04})
    }),
    52014304: _tools.RODict({
        "propID": 52014304,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2262,"adjDrugsQuantity":4,"adjFinalDmg":0.04})
    }),
    52014305: _tools.RODict({
        "propID": 52014305,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2450,"adjDrugsQuantity":4,"adjFinalDmg":0.04})
    }),
    52014306: _tools.RODict({
        "propID": 52014306,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2817,"adjDrugsQuantity":5,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014307: _tools.RODict({
        "propID": 52014307,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3100,"adjDrugsQuantity":5,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014308: _tools.RODict({
        "propID": 52014308,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3409,"adjDrugsQuantity":6,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014309: _tools.RODict({
        "propID": 52014309,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3750,"adjDrugsQuantity":6,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014310: _tools.RODict({
        "propID": 52014310,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1010})
    }),
    52014311: _tools.RODict({
        "propID": 52014311,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1110})
    }),
    52014312: _tools.RODict({
        "propID": 52014312,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1211})
    }),
    52014313: _tools.RODict({
        "propID": 52014313,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1314})
    }),
    52014314: _tools.RODict({
        "propID": 52014314,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1413,"adjDrugsQuantity":1,"adjFinalDmg":0.02})
    }),
    52014315: _tools.RODict({
        "propID": 52014315,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1555,"adjDrugsQuantity":1,"adjFinalDmg":0.02})
    }),
    52014316: _tools.RODict({
        "propID": 52014316,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1696,"adjDrugsQuantity":2,"adjFinalDmg":0.02})
    }),
    52014317: _tools.RODict({
        "propID": 52014317,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1836,"adjDrugsQuantity":2,"adjFinalDmg":0.02})
    }),
    52014318: _tools.RODict({
        "propID": 52014318,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1978,"adjDrugsQuantity":3,"adjFinalDmg":0.04})
    }),
    52014319: _tools.RODict({
        "propID": 52014319,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2177,"adjDrugsQuantity":3,"adjFinalDmg":0.04})
    }),
    52014320: _tools.RODict({
        "propID": 52014320,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2375,"adjDrugsQuantity":4,"adjFinalDmg":0.04})
    }),
    52014321: _tools.RODict({
        "propID": 52014321,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2573,"adjDrugsQuantity":4,"adjFinalDmg":0.04})
    }),
    52014322: _tools.RODict({
        "propID": 52014322,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2958,"adjDrugsQuantity":5,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014323: _tools.RODict({
        "propID": 52014323,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3255,"adjDrugsQuantity":5,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014324: _tools.RODict({
        "propID": 52014324,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3579,"adjDrugsQuantity":6,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014325: _tools.RODict({
        "propID": 52014325,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3938,"adjDrugsQuantity":6,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014326: _tools.RODict({
        "propID": 52014326,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1061})
    }),
    52014327: _tools.RODict({
        "propID": 52014327,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1166})
    }),
    52014328: _tools.RODict({
        "propID": 52014328,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1272})
    }),
    52014329: _tools.RODict({
        "propID": 52014329,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1380})
    }),
    52014330: _tools.RODict({
        "propID": 52014330,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1484,"adjDrugsQuantity":1,"adjFinalDmg":0.02})
    }),
    52014331: _tools.RODict({
        "propID": 52014331,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1633,"adjDrugsQuantity":1,"adjFinalDmg":0.02})
    }),
    52014332: _tools.RODict({
        "propID": 52014332,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1781,"adjDrugsQuantity":2,"adjFinalDmg":0.02})
    }),
    52014333: _tools.RODict({
        "propID": 52014333,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1928,"adjDrugsQuantity":2,"adjFinalDmg":0.02})
    }),
    52014334: _tools.RODict({
        "propID": 52014334,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2077,"adjDrugsQuantity":3,"adjFinalDmg":0.04})
    }),
    52014335: _tools.RODict({
        "propID": 52014335,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2286,"adjDrugsQuantity":3,"adjFinalDmg":0.04})
    }),
    52014336: _tools.RODict({
        "propID": 52014336,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2494,"adjDrugsQuantity":4,"adjFinalDmg":0.04})
    }),
    52014337: _tools.RODict({
        "propID": 52014337,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2702,"adjDrugsQuantity":4,"adjFinalDmg":0.04})
    }),
    52014338: _tools.RODict({
        "propID": 52014338,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3106,"adjDrugsQuantity":5,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014339: _tools.RODict({
        "propID": 52014339,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3418,"adjDrugsQuantity":5,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014340: _tools.RODict({
        "propID": 52014340,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3758,"adjDrugsQuantity":6,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014341: _tools.RODict({
        "propID": 52014341,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4135,"adjDrugsQuantity":6,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014342: _tools.RODict({
        "propID": 52014342,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1114})
    }),
    52014343: _tools.RODict({
        "propID": 52014343,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1224})
    }),
    52014344: _tools.RODict({
        "propID": 52014344,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1336})
    }),
    52014345: _tools.RODict({
        "propID": 52014345,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1449})
    }),
    52014346: _tools.RODict({
        "propID": 52014346,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1558,"adjDrugsQuantity":1,"adjFinalDmg":0.02})
    }),
    52014347: _tools.RODict({
        "propID": 52014347,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1715,"adjDrugsQuantity":1,"adjFinalDmg":0.02})
    }),
    52014348: _tools.RODict({
        "propID": 52014348,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1870,"adjDrugsQuantity":2,"adjFinalDmg":0.02})
    }),
    52014349: _tools.RODict({
        "propID": 52014349,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2024,"adjDrugsQuantity":2,"adjFinalDmg":0.02})
    }),
    52014350: _tools.RODict({
        "propID": 52014350,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2181,"adjDrugsQuantity":3,"adjFinalDmg":0.04})
    }),
    52014351: _tools.RODict({
        "propID": 52014351,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2400,"adjDrugsQuantity":3,"adjFinalDmg":0.04})
    }),
    52014352: _tools.RODict({
        "propID": 52014352,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2619,"adjDrugsQuantity":4,"adjFinalDmg":0.04})
    }),
    52014353: _tools.RODict({
        "propID": 52014353,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2837,"adjDrugsQuantity":4,"adjFinalDmg":0.04})
    }),
    52014354: _tools.RODict({
        "propID": 52014354,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3261,"adjDrugsQuantity":5,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014355: _tools.RODict({
        "propID": 52014355,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3589,"adjDrugsQuantity":5,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014356: _tools.RODict({
        "propID": 52014356,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3946,"adjDrugsQuantity":6,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014357: _tools.RODict({
        "propID": 52014357,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4342,"adjDrugsQuantity":6,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014358: _tools.RODict({
        "propID": 52014358,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1170})
    }),
    52014359: _tools.RODict({
        "propID": 52014359,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1285})
    }),
    52014360: _tools.RODict({
        "propID": 52014360,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1403})
    }),
    52014361: _tools.RODict({
        "propID": 52014361,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1521})
    }),
    52014362: _tools.RODict({
        "propID": 52014362,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1636,"adjDrugsQuantity":1,"adjFinalDmg":0.02})
    }),
    52014363: _tools.RODict({
        "propID": 52014363,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1801,"adjDrugsQuantity":1,"adjFinalDmg":0.02})
    }),
    52014364: _tools.RODict({
        "propID": 52014364,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1964,"adjDrugsQuantity":2,"adjFinalDmg":0.02})
    }),
    52014365: _tools.RODict({
        "propID": 52014365,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2125,"adjDrugsQuantity":2,"adjFinalDmg":0.02})
    }),
    52014366: _tools.RODict({
        "propID": 52014366,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2290,"adjDrugsQuantity":3,"adjFinalDmg":0.04})
    }),
    52014367: _tools.RODict({
        "propID": 52014367,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2520,"adjDrugsQuantity":3,"adjFinalDmg":0.04})
    }),
    52014368: _tools.RODict({
        "propID": 52014368,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2750,"adjDrugsQuantity":4,"adjFinalDmg":0.04})
    }),
    52014369: _tools.RODict({
        "propID": 52014369,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2979,"adjDrugsQuantity":4,"adjFinalDmg":0.04})
    }),
    52014370: _tools.RODict({
        "propID": 52014370,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3424,"adjDrugsQuantity":5,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014371: _tools.RODict({
        "propID": 52014371,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3768,"adjDrugsQuantity":5,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014372: _tools.RODict({
        "propID": 52014372,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4143,"adjDrugsQuantity":6,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014373: _tools.RODict({
        "propID": 52014373,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4559,"adjDrugsQuantity":6,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014374: _tools.RODict({
        "propID": 52014374,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1229})
    }),
    52014375: _tools.RODict({
        "propID": 52014375,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1349})
    }),
    52014376: _tools.RODict({
        "propID": 52014376,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1473})
    }),
    52014377: _tools.RODict({
        "propID": 52014377,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1597})
    }),
    52014378: _tools.RODict({
        "propID": 52014378,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1718,"adjDrugsQuantity":1,"adjFinalDmg":0.02})
    }),
    52014379: _tools.RODict({
        "propID": 52014379,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1891,"adjDrugsQuantity":1,"adjFinalDmg":0.02})
    }),
    52014380: _tools.RODict({
        "propID": 52014380,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2062,"adjDrugsQuantity":2,"adjFinalDmg":0.02})
    }),
    52014381: _tools.RODict({
        "propID": 52014381,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2231,"adjDrugsQuantity":2,"adjFinalDmg":0.02})
    }),
    52014382: _tools.RODict({
        "propID": 52014382,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2405,"adjDrugsQuantity":3,"adjFinalDmg":0.04})
    }),
    52014383: _tools.RODict({
        "propID": 52014383,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2646,"adjDrugsQuantity":3,"adjFinalDmg":0.04})
    }),
    52014384: _tools.RODict({
        "propID": 52014384,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2888,"adjDrugsQuantity":4,"adjFinalDmg":0.04})
    }),
    52014385: _tools.RODict({
        "propID": 52014385,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3128,"adjDrugsQuantity":4,"adjFinalDmg":0.04})
    }),
    52014386: _tools.RODict({
        "propID": 52014386,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3595,"adjDrugsQuantity":5,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014387: _tools.RODict({
        "propID": 52014387,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3956,"adjDrugsQuantity":5,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014388: _tools.RODict({
        "propID": 52014388,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4350,"adjDrugsQuantity":6,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014389: _tools.RODict({
        "propID": 52014389,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4787,"adjDrugsQuantity":6,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014390: _tools.RODict({
        "propID": 52014390,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1290})
    }),
    52014391: _tools.RODict({
        "propID": 52014391,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1416})
    }),
    52014392: _tools.RODict({
        "propID": 52014392,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1547})
    }),
    52014393: _tools.RODict({
        "propID": 52014393,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1677})
    }),
    52014394: _tools.RODict({
        "propID": 52014394,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1804,"adjDrugsQuantity":1,"adjFinalDmg":0.02})
    }),
    52014395: _tools.RODict({
        "propID": 52014395,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1986,"adjDrugsQuantity":1,"adjFinalDmg":0.02})
    }),
    52014396: _tools.RODict({
        "propID": 52014396,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2165,"adjDrugsQuantity":2,"adjFinalDmg":0.02})
    }),
    52014397: _tools.RODict({
        "propID": 52014397,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2343,"adjDrugsQuantity":2,"adjFinalDmg":0.02})
    }),
    52014398: _tools.RODict({
        "propID": 52014398,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2525,"adjDrugsQuantity":3,"adjFinalDmg":0.04})
    }),
    52014399: _tools.RODict({
        "propID": 52014399,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2778,"adjDrugsQuantity":3,"adjFinalDmg":0.04})
    }),
    52014400: _tools.RODict({
        "propID": 52014400,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3032,"adjDrugsQuantity":4,"adjFinalDmg":0.04})
    }),
    52014401: _tools.RODict({
        "propID": 52014401,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3284,"adjDrugsQuantity":4,"adjFinalDmg":0.04})
    }),
    52014402: _tools.RODict({
        "propID": 52014402,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3775,"adjDrugsQuantity":5,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014403: _tools.RODict({
        "propID": 52014403,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4154,"adjDrugsQuantity":5,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014404: _tools.RODict({
        "propID": 52014404,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4568,"adjDrugsQuantity":6,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014405: _tools.RODict({
        "propID": 52014405,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5026,"adjDrugsQuantity":6,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014406: _tools.RODict({
        "propID": 52014406,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1355})
    }),
    52014407: _tools.RODict({
        "propID": 52014407,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1487})
    }),
    52014408: _tools.RODict({
        "propID": 52014408,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1624})
    }),
    52014409: _tools.RODict({
        "propID": 52014409,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1761})
    }),
    52014410: _tools.RODict({
        "propID": 52014410,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1894,"adjDrugsQuantity":1,"adjFinalDmg":0.02})
    }),
    52014411: _tools.RODict({
        "propID": 52014411,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2085,"adjDrugsQuantity":1,"adjFinalDmg":0.02})
    }),
    52014412: _tools.RODict({
        "propID": 52014412,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2273,"adjDrugsQuantity":2,"adjFinalDmg":0.02})
    }),
    52014413: _tools.RODict({
        "propID": 52014413,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2460,"adjDrugsQuantity":2,"adjFinalDmg":0.02})
    }),
    52014414: _tools.RODict({
        "propID": 52014414,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2651,"adjDrugsQuantity":3,"adjFinalDmg":0.04})
    }),
    52014415: _tools.RODict({
        "propID": 52014415,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2917,"adjDrugsQuantity":3,"adjFinalDmg":0.04})
    }),
    52014416: _tools.RODict({
        "propID": 52014416,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3184,"adjDrugsQuantity":4,"adjFinalDmg":0.04})
    }),
    52014417: _tools.RODict({
        "propID": 52014417,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3448,"adjDrugsQuantity":4,"adjFinalDmg":0.04})
    }),
    52014418: _tools.RODict({
        "propID": 52014418,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3964,"adjDrugsQuantity":5,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014419: _tools.RODict({
        "propID": 52014419,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4362,"adjDrugsQuantity":5,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014420: _tools.RODict({
        "propID": 52014420,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4796,"adjDrugsQuantity":6,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014421: _tools.RODict({
        "propID": 52014421,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5277,"adjDrugsQuantity":6,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014422: _tools.RODict({
        "propID": 52014422,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1423})
    }),
    52014423: _tools.RODict({
        "propID": 52014423,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1561})
    }),
    52014424: _tools.RODict({
        "propID": 52014424,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1705})
    }),
    52014425: _tools.RODict({
        "propID": 52014425,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1849})
    }),
    52014426: _tools.RODict({
        "propID": 52014426,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":1989,"adjDrugsQuantity":1,"adjFinalDmg":0.02})
    }),
    52014427: _tools.RODict({
        "propID": 52014427,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2189,"adjDrugsQuantity":1,"adjFinalDmg":0.02})
    }),
    52014428: _tools.RODict({
        "propID": 52014428,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2387,"adjDrugsQuantity":2,"adjFinalDmg":0.02})
    }),
    52014429: _tools.RODict({
        "propID": 52014429,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2583,"adjDrugsQuantity":2,"adjFinalDmg":0.02})
    }),
    52014430: _tools.RODict({
        "propID": 52014430,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":2784,"adjDrugsQuantity":3,"adjFinalDmg":0.04})
    }),
    52014431: _tools.RODict({
        "propID": 52014431,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3063,"adjDrugsQuantity":3,"adjFinalDmg":0.04})
    }),
    52014432: _tools.RODict({
        "propID": 52014432,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3343,"adjDrugsQuantity":4,"adjFinalDmg":0.04})
    }),
    52014433: _tools.RODict({
        "propID": 52014433,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":3620,"adjDrugsQuantity":4,"adjFinalDmg":0.04})
    }),
    52014434: _tools.RODict({
        "propID": 52014434,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4162,"adjDrugsQuantity":5,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014435: _tools.RODict({
        "propID": 52014435,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":4580,"adjDrugsQuantity":5,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014436: _tools.RODict({
        "propID": 52014436,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5036,"adjDrugsQuantity":6,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    }),
    52014437: _tools.RODict({
        "propID": 52014437,
        "type": 2,
        "propList": _tools.RODict({"adjFullHp":5541,"adjDrugsQuantity":6,"adjFinalDmg":0.04,"adjFinalDmgAnti":0.04})
    })
})
minKey = 51000001
maxKey = 52014437