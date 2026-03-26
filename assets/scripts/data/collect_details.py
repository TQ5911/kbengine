# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: collect/details
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    100001: _tools.RODict({
        "ID": 100001,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":1}),
        "equipment": _tools.ROList([[80111001, 0, 1], [80591001, 0, 1], [80691001, 0, 1]]),
        "props": None
    }),
    100002: _tools.RODict({
        "ID": 100002,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":1}),
        "equipment": _tools.ROList([[80111001, 1, 1], [80591001, 1, 1], [80691001, 1, 1]]),
        "props": None
    }),
    100003: _tools.RODict({
        "ID": 100003,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":2}),
        "equipment": _tools.ROList([[80111001, 2, 1], [80591001, 2, 1], [80691001, 2, 1]]),
        "props": None
    }),
    100004: _tools.RODict({
        "ID": 100004,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":2}),
        "equipment": _tools.ROList([[80111001, 3, 1], [80591001, 3, 1], [80691001, 3, 1]]),
        "props": None
    }),
    100005: _tools.RODict({
        "ID": 100005,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":3}),
        "equipment": _tools.ROList([[80111001, 4, 1], [80591001, 4, 1], [80691001, 4, 1]]),
        "props": None
    }),
    100006: _tools.RODict({
        "ID": 100006,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":3}),
        "equipment": _tools.ROList([[80111001, 5, 1], [80591001, 5, 1], [80691001, 5, 1]]),
        "props": None
    }),
    100007: _tools.RODict({
        "ID": 100007,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":4}),
        "equipment": _tools.ROList([[80111001, 6, 1], [80591001, 6, 1], [80691001, 6, 1]]),
        "props": None
    }),
    100008: _tools.RODict({
        "ID": 100008,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":4}),
        "equipment": _tools.ROList([[80111001, 7, 1], [80591001, 7, 1], [80691001, 7, 1]]),
        "props": None
    }),
    100009: _tools.RODict({
        "ID": 100009,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":1}),
        "equipment": _tools.ROList([[80111001, 0, 2], [80591001, 0, 2], [80691001, 0, 2]]),
        "props": None
    }),
    100010: _tools.RODict({
        "ID": 100010,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":1}),
        "equipment": _tools.ROList([[80111001, 1, 2], [80591001, 1, 2], [80691001, 1, 2]]),
        "props": None
    }),
    100011: _tools.RODict({
        "ID": 100011,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":2}),
        "equipment": _tools.ROList([[80111001, 2, 2], [80591001, 2, 2], [80691001, 2, 2]]),
        "props": None
    }),
    100012: _tools.RODict({
        "ID": 100012,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":2}),
        "equipment": _tools.ROList([[80111001, 3, 2], [80591001, 3, 2], [80691001, 3, 2]]),
        "props": None
    }),
    100013: _tools.RODict({
        "ID": 100013,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":3}),
        "equipment": _tools.ROList([[80111001, 4, 2], [80591001, 4, 2], [80691001, 4, 2]]),
        "props": None
    }),
    100014: _tools.RODict({
        "ID": 100014,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":3}),
        "equipment": _tools.ROList([[80111001, 5, 2], [80591001, 5, 2], [80691001, 5, 2]]),
        "props": None
    }),
    100015: _tools.RODict({
        "ID": 100015,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":4}),
        "equipment": _tools.ROList([[80111001, 6, 2], [80591001, 6, 2], [80691001, 6, 2]]),
        "props": None
    }),
    100016: _tools.RODict({
        "ID": 100016,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":4}),
        "equipment": _tools.ROList([[80111001, 7, 2], [80591001, 7, 2], [80691001, 7, 2]]),
        "props": None
    }),
    100017: _tools.RODict({
        "ID": 100017,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":1}),
        "equipment": _tools.ROList([[80111001, 0, 3], [80591001, 0, 3], [80691001, 0, 3]]),
        "props": None
    }),
    100018: _tools.RODict({
        "ID": 100018,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":1}),
        "equipment": _tools.ROList([[80111001, 1, 3], [80591001, 1, 3], [80691001, 1, 3]]),
        "props": None
    }),
    100019: _tools.RODict({
        "ID": 100019,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":2}),
        "equipment": _tools.ROList([[80111001, 2, 3], [80591001, 2, 3], [80691001, 2, 3]]),
        "props": None
    }),
    100020: _tools.RODict({
        "ID": 100020,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":2}),
        "equipment": _tools.ROList([[80111001, 3, 3], [80591001, 3, 3], [80691001, 3, 3]]),
        "props": None
    }),
    100021: _tools.RODict({
        "ID": 100021,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":3}),
        "equipment": _tools.ROList([[80111001, 4, 3], [80591001, 4, 3], [80691001, 4, 3]]),
        "props": None
    }),
    100022: _tools.RODict({
        "ID": 100022,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":3}),
        "equipment": _tools.ROList([[80111001, 5, 3], [80591001, 5, 3], [80691001, 5, 3]]),
        "props": None
    }),
    100023: _tools.RODict({
        "ID": 100023,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":4}),
        "equipment": _tools.ROList([[80111001, 6, 3], [80591001, 6, 3], [80691001, 6, 3]]),
        "props": None
    }),
    100024: _tools.RODict({
        "ID": 100024,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":4}),
        "equipment": _tools.ROList([[80111001, 7, 3], [80591001, 7, 3], [80691001, 7, 3]]),
        "props": None
    }),
    100025: _tools.RODict({
        "ID": 100025,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":1}),
        "equipment": _tools.ROList([[80111001, 0, 4], [80591001, 0, 4], [80691001, 0, 4]]),
        "props": None
    }),
    100026: _tools.RODict({
        "ID": 100026,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":1}),
        "equipment": _tools.ROList([[80111001, 1, 4], [80591001, 1, 4], [80691001, 1, 4]]),
        "props": None
    }),
    100027: _tools.RODict({
        "ID": 100027,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":2}),
        "equipment": _tools.ROList([[80111001, 2, 4], [80591001, 2, 4], [80691001, 2, 4]]),
        "props": None
    }),
    100028: _tools.RODict({
        "ID": 100028,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":2}),
        "equipment": _tools.ROList([[80111001, 3, 4], [80591001, 3, 4], [80691001, 3, 4]]),
        "props": None
    }),
    100029: _tools.RODict({
        "ID": 100029,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":3}),
        "equipment": _tools.ROList([[80111001, 4, 4], [80591001, 4, 4], [80691001, 4, 4]]),
        "props": None
    }),
    100030: _tools.RODict({
        "ID": 100030,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":3}),
        "equipment": _tools.ROList([[80111001, 5, 4], [80591001, 5, 4], [80691001, 5, 4]]),
        "props": None
    }),
    100031: _tools.RODict({
        "ID": 100031,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":4}),
        "equipment": _tools.ROList([[80111001, 6, 4], [80591001, 6, 4], [80691001, 6, 4]]),
        "props": None
    }),
    100032: _tools.RODict({
        "ID": 100032,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":4}),
        "equipment": _tools.ROList([[80111001, 7, 4], [80591001, 7, 4], [80691001, 7, 4]]),
        "props": None
    }),
    100033: _tools.RODict({
        "ID": 100033,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":1}),
        "equipment": _tools.ROList([[80121001, 0, 1], [80591001, 0, 1], [80691001, 0, 1]]),
        "props": None
    }),
    100034: _tools.RODict({
        "ID": 100034,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":1}),
        "equipment": _tools.ROList([[80121001, 1, 1], [80591001, 1, 1], [80691001, 1, 1]]),
        "props": None
    }),
    100035: _tools.RODict({
        "ID": 100035,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":2}),
        "equipment": _tools.ROList([[80121001, 2, 1], [80591001, 2, 1], [80691001, 2, 1]]),
        "props": None
    }),
    100036: _tools.RODict({
        "ID": 100036,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":2}),
        "equipment": _tools.ROList([[80121001, 3, 1], [80591001, 3, 1], [80691001, 3, 1]]),
        "props": None
    }),
    100037: _tools.RODict({
        "ID": 100037,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":3}),
        "equipment": _tools.ROList([[80121001, 4, 1], [80591001, 4, 1], [80691001, 4, 1]]),
        "props": None
    }),
    100038: _tools.RODict({
        "ID": 100038,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":3}),
        "equipment": _tools.ROList([[80121001, 5, 1], [80591001, 5, 1], [80691001, 5, 1]]),
        "props": None
    }),
    100039: _tools.RODict({
        "ID": 100039,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":4}),
        "equipment": _tools.ROList([[80121001, 6, 1], [80591001, 6, 1], [80691001, 6, 1]]),
        "props": None
    }),
    100040: _tools.RODict({
        "ID": 100040,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":4}),
        "equipment": _tools.ROList([[80121001, 7, 1], [80591001, 7, 1], [80691001, 7, 1]]),
        "props": None
    }),
    100041: _tools.RODict({
        "ID": 100041,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":1}),
        "equipment": _tools.ROList([[80121001, 0, 2], [80591001, 0, 2], [80691001, 0, 2]]),
        "props": None
    }),
    100042: _tools.RODict({
        "ID": 100042,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":1}),
        "equipment": _tools.ROList([[80121001, 1, 2], [80591001, 1, 2], [80691001, 1, 2]]),
        "props": None
    }),
    100043: _tools.RODict({
        "ID": 100043,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":2}),
        "equipment": _tools.ROList([[80121001, 2, 2], [80591001, 2, 2], [80691001, 2, 2]]),
        "props": None
    }),
    100044: _tools.RODict({
        "ID": 100044,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":2}),
        "equipment": _tools.ROList([[80121001, 3, 2], [80591001, 3, 2], [80691001, 3, 2]]),
        "props": None
    }),
    100045: _tools.RODict({
        "ID": 100045,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":3}),
        "equipment": _tools.ROList([[80121001, 4, 2], [80591001, 4, 2], [80691001, 4, 2]]),
        "props": None
    }),
    100046: _tools.RODict({
        "ID": 100046,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":3}),
        "equipment": _tools.ROList([[80121001, 5, 2], [80591001, 5, 2], [80691001, 5, 2]]),
        "props": None
    }),
    100047: _tools.RODict({
        "ID": 100047,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":4}),
        "equipment": _tools.ROList([[80121001, 6, 2], [80591001, 6, 2], [80691001, 6, 2]]),
        "props": None
    }),
    100048: _tools.RODict({
        "ID": 100048,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":4}),
        "equipment": _tools.ROList([[80121001, 7, 2], [80591001, 7, 2], [80691001, 7, 2]]),
        "props": None
    }),
    100049: _tools.RODict({
        "ID": 100049,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":1}),
        "equipment": _tools.ROList([[80121001, 0, 3], [80591001, 0, 3], [80691001, 0, 3]]),
        "props": None
    }),
    100050: _tools.RODict({
        "ID": 100050,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":1}),
        "equipment": _tools.ROList([[80121001, 1, 3], [80591001, 1, 3], [80691001, 1, 3]]),
        "props": None
    }),
    100051: _tools.RODict({
        "ID": 100051,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":2}),
        "equipment": _tools.ROList([[80121001, 2, 3], [80591001, 2, 3], [80691001, 2, 3]]),
        "props": None
    }),
    100052: _tools.RODict({
        "ID": 100052,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":2}),
        "equipment": _tools.ROList([[80121001, 3, 3], [80591001, 3, 3], [80691001, 3, 3]]),
        "props": None
    }),
    100053: _tools.RODict({
        "ID": 100053,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":3}),
        "equipment": _tools.ROList([[80121001, 4, 3], [80591001, 4, 3], [80691001, 4, 3]]),
        "props": None
    }),
    100054: _tools.RODict({
        "ID": 100054,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":3}),
        "equipment": _tools.ROList([[80121001, 5, 3], [80591001, 5, 3], [80691001, 5, 3]]),
        "props": None
    }),
    100055: _tools.RODict({
        "ID": 100055,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":4}),
        "equipment": _tools.ROList([[80121001, 6, 3], [80591001, 6, 3], [80691001, 6, 3]]),
        "props": None
    }),
    100056: _tools.RODict({
        "ID": 100056,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":4}),
        "equipment": _tools.ROList([[80121001, 7, 3], [80591001, 7, 3], [80691001, 7, 3]]),
        "props": None
    }),
    100057: _tools.RODict({
        "ID": 100057,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":1}),
        "equipment": _tools.ROList([[80121001, 0, 4], [80591001, 0, 4], [80691001, 0, 4]]),
        "props": None
    }),
    100058: _tools.RODict({
        "ID": 100058,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":1}),
        "equipment": _tools.ROList([[80121001, 1, 4], [80591001, 1, 4], [80691001, 1, 4]]),
        "props": None
    }),
    100059: _tools.RODict({
        "ID": 100059,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":2}),
        "equipment": _tools.ROList([[80121001, 2, 4], [80591001, 2, 4], [80691001, 2, 4]]),
        "props": None
    }),
    100060: _tools.RODict({
        "ID": 100060,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":2}),
        "equipment": _tools.ROList([[80121001, 3, 4], [80591001, 3, 4], [80691001, 3, 4]]),
        "props": None
    }),
    100061: _tools.RODict({
        "ID": 100061,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":3}),
        "equipment": _tools.ROList([[80121001, 4, 4], [80591001, 4, 4], [80691001, 4, 4]]),
        "props": None
    }),
    100062: _tools.RODict({
        "ID": 100062,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":3}),
        "equipment": _tools.ROList([[80121001, 5, 4], [80591001, 5, 4], [80691001, 5, 4]]),
        "props": None
    }),
    100063: _tools.RODict({
        "ID": 100063,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":4}),
        "equipment": _tools.ROList([[80121001, 6, 4], [80591001, 6, 4], [80691001, 6, 4]]),
        "props": None
    }),
    100064: _tools.RODict({
        "ID": 100064,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":4}),
        "equipment": _tools.ROList([[80121001, 7, 4], [80591001, 7, 4], [80691001, 7, 4]]),
        "props": None
    }),
    100065: _tools.RODict({
        "ID": 100065,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":1}),
        "equipment": _tools.ROList([[80131001, 0, 1], [80581001, 0, 1], [80681001, 0, 1]]),
        "props": None
    }),
    100066: _tools.RODict({
        "ID": 100066,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":1}),
        "equipment": _tools.ROList([[80131001, 1, 1], [80581001, 1, 1], [80681001, 1, 1]]),
        "props": None
    }),
    100067: _tools.RODict({
        "ID": 100067,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":2}),
        "equipment": _tools.ROList([[80131001, 2, 1], [80581001, 2, 1], [80681001, 2, 1]]),
        "props": None
    }),
    100068: _tools.RODict({
        "ID": 100068,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":2}),
        "equipment": _tools.ROList([[80131001, 3, 1], [80581001, 3, 1], [80681001, 3, 1]]),
        "props": None
    }),
    100069: _tools.RODict({
        "ID": 100069,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":3}),
        "equipment": _tools.ROList([[80131001, 4, 1], [80581001, 4, 1], [80681001, 4, 1]]),
        "props": None
    }),
    100070: _tools.RODict({
        "ID": 100070,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":3}),
        "equipment": _tools.ROList([[80131001, 5, 1], [80581001, 5, 1], [80681001, 5, 1]]),
        "props": None
    }),
    100071: _tools.RODict({
        "ID": 100071,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":4}),
        "equipment": _tools.ROList([[80131001, 6, 1], [80581001, 6, 1], [80681001, 6, 1]]),
        "props": None
    }),
    100072: _tools.RODict({
        "ID": 100072,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":4}),
        "equipment": _tools.ROList([[80131001, 7, 1], [80581001, 7, 1], [80681001, 7, 1]]),
        "props": None
    }),
    100073: _tools.RODict({
        "ID": 100073,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":1}),
        "equipment": _tools.ROList([[80131001, 0, 2], [80581001, 0, 2], [80681001, 0, 2]]),
        "props": None
    }),
    100074: _tools.RODict({
        "ID": 100074,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":1}),
        "equipment": _tools.ROList([[80131001, 1, 2], [80581001, 1, 2], [80681001, 1, 2]]),
        "props": None
    }),
    100075: _tools.RODict({
        "ID": 100075,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":2}),
        "equipment": _tools.ROList([[80131001, 2, 2], [80581001, 2, 2], [80681001, 2, 2]]),
        "props": None
    }),
    100076: _tools.RODict({
        "ID": 100076,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":2}),
        "equipment": _tools.ROList([[80131001, 3, 2], [80581001, 3, 2], [80681001, 3, 2]]),
        "props": None
    }),
    100077: _tools.RODict({
        "ID": 100077,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":3}),
        "equipment": _tools.ROList([[80131001, 4, 2], [80581001, 4, 2], [80681001, 4, 2]]),
        "props": None
    }),
    100078: _tools.RODict({
        "ID": 100078,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":3}),
        "equipment": _tools.ROList([[80131001, 5, 2], [80581001, 5, 2], [80681001, 5, 2]]),
        "props": None
    }),
    100079: _tools.RODict({
        "ID": 100079,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":4}),
        "equipment": _tools.ROList([[80131001, 6, 2], [80581001, 6, 2], [80681001, 6, 2]]),
        "props": None
    }),
    100080: _tools.RODict({
        "ID": 100080,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":4}),
        "equipment": _tools.ROList([[80131001, 7, 2], [80581001, 7, 2], [80681001, 7, 2]]),
        "props": None
    }),
    100081: _tools.RODict({
        "ID": 100081,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":1}),
        "equipment": _tools.ROList([[80131001, 0, 3], [80581001, 0, 3], [80681001, 0, 3]]),
        "props": None
    }),
    100082: _tools.RODict({
        "ID": 100082,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":1}),
        "equipment": _tools.ROList([[80131001, 1, 3], [80581001, 1, 3], [80681001, 1, 3]]),
        "props": None
    }),
    100083: _tools.RODict({
        "ID": 100083,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":2}),
        "equipment": _tools.ROList([[80131001, 2, 3], [80581001, 2, 3], [80681001, 2, 3]]),
        "props": None
    }),
    100084: _tools.RODict({
        "ID": 100084,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":2}),
        "equipment": _tools.ROList([[80131001, 3, 3], [80581001, 3, 3], [80681001, 3, 3]]),
        "props": None
    }),
    100085: _tools.RODict({
        "ID": 100085,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":3}),
        "equipment": _tools.ROList([[80131001, 4, 3], [80581001, 4, 3], [80681001, 4, 3]]),
        "props": None
    }),
    100086: _tools.RODict({
        "ID": 100086,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":3}),
        "equipment": _tools.ROList([[80131001, 5, 3], [80581001, 5, 3], [80681001, 5, 3]]),
        "props": None
    }),
    100087: _tools.RODict({
        "ID": 100087,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":4}),
        "equipment": _tools.ROList([[80131001, 6, 3], [80581001, 6, 3], [80681001, 6, 3]]),
        "props": None
    }),
    100088: _tools.RODict({
        "ID": 100088,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":4}),
        "equipment": _tools.ROList([[80131001, 7, 3], [80581001, 7, 3], [80681001, 7, 3]]),
        "props": None
    }),
    100089: _tools.RODict({
        "ID": 100089,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":1}),
        "equipment": _tools.ROList([[80131001, 0, 4], [80581001, 0, 4], [80681001, 0, 4]]),
        "props": None
    }),
    100090: _tools.RODict({
        "ID": 100090,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":1}),
        "equipment": _tools.ROList([[80131001, 1, 4], [80581001, 1, 4], [80681001, 1, 4]]),
        "props": None
    }),
    100091: _tools.RODict({
        "ID": 100091,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":2}),
        "equipment": _tools.ROList([[80131001, 2, 4], [80581001, 2, 4], [80681001, 2, 4]]),
        "props": None
    }),
    100092: _tools.RODict({
        "ID": 100092,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":2}),
        "equipment": _tools.ROList([[80131001, 3, 4], [80581001, 3, 4], [80681001, 3, 4]]),
        "props": None
    }),
    100093: _tools.RODict({
        "ID": 100093,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":3}),
        "equipment": _tools.ROList([[80131001, 4, 4], [80581001, 4, 4], [80681001, 4, 4]]),
        "props": None
    }),
    100094: _tools.RODict({
        "ID": 100094,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":3}),
        "equipment": _tools.ROList([[80131001, 5, 4], [80581001, 5, 4], [80681001, 5, 4]]),
        "props": None
    }),
    100095: _tools.RODict({
        "ID": 100095,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":4}),
        "equipment": _tools.ROList([[80131001, 6, 4], [80581001, 6, 4], [80681001, 6, 4]]),
        "props": None
    }),
    100096: _tools.RODict({
        "ID": 100096,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":4}),
        "equipment": _tools.ROList([[80131001, 7, 4], [80581001, 7, 4], [80681001, 7, 4]]),
        "props": None
    }),
    100097: _tools.RODict({
        "ID": 100097,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":30}),
        "equipment": _tools.ROList([[80211001, 0, 1], [80791001, 0, 1], [80311001, 0, 1]]),
        "props": None
    }),
    100098: _tools.RODict({
        "ID": 100098,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":45}),
        "equipment": _tools.ROList([[80211001, 1, 1], [80791001, 1, 1], [80311001, 1, 1]]),
        "props": None
    }),
    100099: _tools.RODict({
        "ID": 100099,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":60}),
        "equipment": _tools.ROList([[80211001, 2, 1], [80791001, 2, 1], [80311001, 2, 1]]),
        "props": None
    }),
    100100: _tools.RODict({
        "ID": 100100,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":60}),
        "equipment": _tools.ROList([[80211001, 3, 1], [80791001, 3, 1], [80311001, 3, 1]]),
        "props": None
    }),
    100101: _tools.RODict({
        "ID": 100101,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":90}),
        "equipment": _tools.ROList([[80211001, 4, 1], [80791001, 4, 1], [80311001, 4, 1]]),
        "props": None
    }),
    100102: _tools.RODict({
        "ID": 100102,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":120}),
        "equipment": _tools.ROList([[80211001, 5, 1], [80791001, 5, 1], [80311001, 5, 1]]),
        "props": None
    }),
    100103: _tools.RODict({
        "ID": 100103,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":150}),
        "equipment": _tools.ROList([[80211001, 6, 1], [80791001, 6, 1], [80311001, 6, 1]]),
        "props": None
    }),
    100104: _tools.RODict({
        "ID": 100104,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":240}),
        "equipment": _tools.ROList([[80211001, 7, 1], [80791001, 7, 1], [80311001, 7, 1]]),
        "props": None
    }),
    100105: _tools.RODict({
        "ID": 100105,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":60}),
        "equipment": _tools.ROList([[80211001, 0, 2], [80791001, 0, 2], [80311001, 0, 2]]),
        "props": None
    }),
    100106: _tools.RODict({
        "ID": 100106,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":75}),
        "equipment": _tools.ROList([[80211001, 1, 2], [80791001, 1, 2], [80311001, 1, 2]]),
        "props": None
    }),
    100107: _tools.RODict({
        "ID": 100107,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":90}),
        "equipment": _tools.ROList([[80211001, 2, 2], [80791001, 2, 2], [80311001, 2, 2]]),
        "props": None
    }),
    100108: _tools.RODict({
        "ID": 100108,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":90}),
        "equipment": _tools.ROList([[80211001, 3, 2], [80791001, 3, 2], [80311001, 3, 2]]),
        "props": None
    }),
    100109: _tools.RODict({
        "ID": 100109,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":120}),
        "equipment": _tools.ROList([[80211001, 4, 2], [80791001, 4, 2], [80311001, 4, 2]]),
        "props": None
    }),
    100110: _tools.RODict({
        "ID": 100110,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":150}),
        "equipment": _tools.ROList([[80211001, 5, 2], [80791001, 5, 2], [80311001, 5, 2]]),
        "props": None
    }),
    100111: _tools.RODict({
        "ID": 100111,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":180}),
        "equipment": _tools.ROList([[80211001, 6, 2], [80791001, 6, 2], [80311001, 6, 2]]),
        "props": None
    }),
    100112: _tools.RODict({
        "ID": 100112,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":270}),
        "equipment": _tools.ROList([[80211001, 7, 2], [80791001, 7, 2], [80311001, 7, 2]]),
        "props": None
    }),
    100113: _tools.RODict({
        "ID": 100113,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":90}),
        "equipment": _tools.ROList([[80211001, 0, 3], [80791001, 0, 3], [80311001, 0, 3]]),
        "props": None
    }),
    100114: _tools.RODict({
        "ID": 100114,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":105}),
        "equipment": _tools.ROList([[80211001, 1, 3], [80791001, 1, 3], [80311001, 1, 3]]),
        "props": None
    }),
    100115: _tools.RODict({
        "ID": 100115,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":120}),
        "equipment": _tools.ROList([[80211001, 2, 3], [80791001, 2, 3], [80311001, 2, 3]]),
        "props": None
    }),
    100116: _tools.RODict({
        "ID": 100116,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":120}),
        "equipment": _tools.ROList([[80211001, 3, 3], [80791001, 3, 3], [80311001, 3, 3]]),
        "props": None
    }),
    100117: _tools.RODict({
        "ID": 100117,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":150}),
        "equipment": _tools.ROList([[80211001, 4, 3], [80791001, 4, 3], [80311001, 4, 3]]),
        "props": None
    }),
    100118: _tools.RODict({
        "ID": 100118,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":180}),
        "equipment": _tools.ROList([[80211001, 5, 3], [80791001, 5, 3], [80311001, 5, 3]]),
        "props": None
    }),
    100119: _tools.RODict({
        "ID": 100119,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":210}),
        "equipment": _tools.ROList([[80211001, 6, 3], [80791001, 6, 3], [80311001, 6, 3]]),
        "props": None
    }),
    100120: _tools.RODict({
        "ID": 100120,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":300}),
        "equipment": _tools.ROList([[80211001, 7, 3], [80791001, 7, 3], [80311001, 7, 3]]),
        "props": None
    }),
    100121: _tools.RODict({
        "ID": 100121,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":120}),
        "equipment": _tools.ROList([[80211001, 0, 4], [80791001, 0, 4], [80311001, 0, 4]]),
        "props": None
    }),
    100122: _tools.RODict({
        "ID": 100122,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":135}),
        "equipment": _tools.ROList([[80211001, 1, 4], [80791001, 1, 4], [80311001, 1, 4]]),
        "props": None
    }),
    100123: _tools.RODict({
        "ID": 100123,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":150}),
        "equipment": _tools.ROList([[80211001, 2, 4], [80791001, 2, 4], [80311001, 2, 4]]),
        "props": None
    }),
    100124: _tools.RODict({
        "ID": 100124,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":150}),
        "equipment": _tools.ROList([[80211001, 3, 4], [80791001, 3, 4], [80311001, 3, 4]]),
        "props": None
    }),
    100125: _tools.RODict({
        "ID": 100125,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":180}),
        "equipment": _tools.ROList([[80211001, 4, 4], [80791001, 4, 4], [80311001, 4, 4]]),
        "props": None
    }),
    100126: _tools.RODict({
        "ID": 100126,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":210}),
        "equipment": _tools.ROList([[80211001, 5, 4], [80791001, 5, 4], [80311001, 5, 4]]),
        "props": None
    }),
    100127: _tools.RODict({
        "ID": 100127,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":240}),
        "equipment": _tools.ROList([[80211001, 6, 4], [80791001, 6, 4], [80311001, 6, 4]]),
        "props": None
    }),
    100128: _tools.RODict({
        "ID": 100128,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":330}),
        "equipment": _tools.ROList([[80211001, 7, 4], [80791001, 7, 4], [80311001, 7, 4]]),
        "props": None
    }),
    100129: _tools.RODict({
        "ID": 100129,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":30}),
        "equipment": _tools.ROList([[80221001, 0, 1], [80791001, 0, 1], [80321001, 0, 1]]),
        "props": None
    }),
    100130: _tools.RODict({
        "ID": 100130,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":45}),
        "equipment": _tools.ROList([[80221001, 1, 1], [80791001, 1, 1], [80321001, 1, 1]]),
        "props": None
    }),
    100131: _tools.RODict({
        "ID": 100131,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":60}),
        "equipment": _tools.ROList([[80221001, 2, 1], [80791001, 2, 1], [80321001, 2, 1]]),
        "props": None
    }),
    100132: _tools.RODict({
        "ID": 100132,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":60}),
        "equipment": _tools.ROList([[80221001, 3, 1], [80791001, 3, 1], [80321001, 3, 1]]),
        "props": None
    }),
    100133: _tools.RODict({
        "ID": 100133,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":90}),
        "equipment": _tools.ROList([[80221001, 4, 1], [80791001, 4, 1], [80321001, 4, 1]]),
        "props": None
    }),
    100134: _tools.RODict({
        "ID": 100134,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":120}),
        "equipment": _tools.ROList([[80221001, 5, 1], [80791001, 5, 1], [80321001, 5, 1]]),
        "props": None
    }),
    100135: _tools.RODict({
        "ID": 100135,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":150}),
        "equipment": _tools.ROList([[80221001, 6, 1], [80791001, 6, 1], [80321001, 6, 1]]),
        "props": None
    }),
    100136: _tools.RODict({
        "ID": 100136,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":240}),
        "equipment": _tools.ROList([[80221001, 7, 1], [80791001, 7, 1], [80321001, 7, 1]]),
        "props": None
    }),
    100137: _tools.RODict({
        "ID": 100137,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":60}),
        "equipment": _tools.ROList([[80221001, 0, 2], [80791001, 0, 2], [80321001, 0, 2]]),
        "props": None
    }),
    100138: _tools.RODict({
        "ID": 100138,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":75}),
        "equipment": _tools.ROList([[80221001, 1, 2], [80791001, 1, 2], [80321001, 1, 2]]),
        "props": None
    }),
    100139: _tools.RODict({
        "ID": 100139,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":90}),
        "equipment": _tools.ROList([[80221001, 2, 2], [80791001, 2, 2], [80321001, 2, 2]]),
        "props": None
    }),
    100140: _tools.RODict({
        "ID": 100140,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":90}),
        "equipment": _tools.ROList([[80221001, 3, 2], [80791001, 3, 2], [80321001, 3, 2]]),
        "props": None
    }),
    100141: _tools.RODict({
        "ID": 100141,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":120}),
        "equipment": _tools.ROList([[80221001, 4, 2], [80791001, 4, 2], [80321001, 4, 2]]),
        "props": None
    }),
    100142: _tools.RODict({
        "ID": 100142,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":150}),
        "equipment": _tools.ROList([[80221001, 5, 2], [80791001, 5, 2], [80321001, 5, 2]]),
        "props": None
    }),
    100143: _tools.RODict({
        "ID": 100143,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":180}),
        "equipment": _tools.ROList([[80221001, 6, 2], [80791001, 6, 2], [80321001, 6, 2]]),
        "props": None
    }),
    100144: _tools.RODict({
        "ID": 100144,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":270}),
        "equipment": _tools.ROList([[80221001, 7, 2], [80791001, 7, 2], [80321001, 7, 2]]),
        "props": None
    }),
    100145: _tools.RODict({
        "ID": 100145,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":90}),
        "equipment": _tools.ROList([[80221001, 0, 3], [80791001, 0, 3], [80321001, 0, 3]]),
        "props": None
    }),
    100146: _tools.RODict({
        "ID": 100146,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":105}),
        "equipment": _tools.ROList([[80221001, 1, 3], [80791001, 1, 3], [80321001, 1, 3]]),
        "props": None
    }),
    100147: _tools.RODict({
        "ID": 100147,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":120}),
        "equipment": _tools.ROList([[80221001, 2, 3], [80791001, 2, 3], [80321001, 2, 3]]),
        "props": None
    }),
    100148: _tools.RODict({
        "ID": 100148,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":120}),
        "equipment": _tools.ROList([[80221001, 3, 3], [80791001, 3, 3], [80321001, 3, 3]]),
        "props": None
    }),
    100149: _tools.RODict({
        "ID": 100149,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":150}),
        "equipment": _tools.ROList([[80221001, 4, 3], [80791001, 4, 3], [80321001, 4, 3]]),
        "props": None
    }),
    100150: _tools.RODict({
        "ID": 100150,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":180}),
        "equipment": _tools.ROList([[80221001, 5, 3], [80791001, 5, 3], [80321001, 5, 3]]),
        "props": None
    }),
    100151: _tools.RODict({
        "ID": 100151,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":210}),
        "equipment": _tools.ROList([[80221001, 6, 3], [80791001, 6, 3], [80321001, 6, 3]]),
        "props": None
    }),
    100152: _tools.RODict({
        "ID": 100152,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":300}),
        "equipment": _tools.ROList([[80221001, 7, 3], [80791001, 7, 3], [80321001, 7, 3]]),
        "props": None
    }),
    100153: _tools.RODict({
        "ID": 100153,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":120}),
        "equipment": _tools.ROList([[80221001, 0, 4], [80791001, 0, 4], [80321001, 0, 4]]),
        "props": None
    }),
    100154: _tools.RODict({
        "ID": 100154,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":135}),
        "equipment": _tools.ROList([[80221001, 1, 4], [80791001, 1, 4], [80321001, 1, 4]]),
        "props": None
    }),
    100155: _tools.RODict({
        "ID": 100155,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":150}),
        "equipment": _tools.ROList([[80221001, 2, 4], [80791001, 2, 4], [80321001, 2, 4]]),
        "props": None
    }),
    100156: _tools.RODict({
        "ID": 100156,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":150}),
        "equipment": _tools.ROList([[80221001, 3, 4], [80791001, 3, 4], [80321001, 3, 4]]),
        "props": None
    }),
    100157: _tools.RODict({
        "ID": 100157,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":180}),
        "equipment": _tools.ROList([[80221001, 4, 4], [80791001, 4, 4], [80321001, 4, 4]]),
        "props": None
    }),
    100158: _tools.RODict({
        "ID": 100158,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":210}),
        "equipment": _tools.ROList([[80221001, 5, 4], [80791001, 5, 4], [80321001, 5, 4]]),
        "props": None
    }),
    100159: _tools.RODict({
        "ID": 100159,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":240}),
        "equipment": _tools.ROList([[80221001, 6, 4], [80791001, 6, 4], [80321001, 6, 4]]),
        "props": None
    }),
    100160: _tools.RODict({
        "ID": 100160,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":330}),
        "equipment": _tools.ROList([[80221001, 7, 4], [80791001, 7, 4], [80321001, 7, 4]]),
        "props": None
    }),
    100161: _tools.RODict({
        "ID": 100161,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":30}),
        "equipment": _tools.ROList([[80231001, 0, 1], [80781001, 0, 1], [80331001, 0, 1]]),
        "props": None
    }),
    100162: _tools.RODict({
        "ID": 100162,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":45}),
        "equipment": _tools.ROList([[80231001, 1, 1], [80781001, 1, 1], [80331001, 1, 1]]),
        "props": None
    }),
    100163: _tools.RODict({
        "ID": 100163,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":60}),
        "equipment": _tools.ROList([[80231001, 2, 1], [80781001, 2, 1], [80331001, 2, 1]]),
        "props": None
    }),
    100164: _tools.RODict({
        "ID": 100164,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":60}),
        "equipment": _tools.ROList([[80231001, 3, 1], [80781001, 3, 1], [80331001, 3, 1]]),
        "props": None
    }),
    100165: _tools.RODict({
        "ID": 100165,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":90}),
        "equipment": _tools.ROList([[80231001, 4, 1], [80781001, 4, 1], [80331001, 4, 1]]),
        "props": None
    }),
    100166: _tools.RODict({
        "ID": 100166,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":120}),
        "equipment": _tools.ROList([[80231001, 5, 1], [80781001, 5, 1], [80331001, 5, 1]]),
        "props": None
    }),
    100167: _tools.RODict({
        "ID": 100167,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":150}),
        "equipment": _tools.ROList([[80231001, 6, 1], [80781001, 6, 1], [80331001, 6, 1]]),
        "props": None
    }),
    100168: _tools.RODict({
        "ID": 100168,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":240}),
        "equipment": _tools.ROList([[80231001, 7, 1], [80781001, 7, 1], [80331001, 7, 1]]),
        "props": None
    }),
    100169: _tools.RODict({
        "ID": 100169,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":60}),
        "equipment": _tools.ROList([[80231001, 0, 2], [80781001, 0, 2], [80331001, 0, 2]]),
        "props": None
    }),
    100170: _tools.RODict({
        "ID": 100170,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":75}),
        "equipment": _tools.ROList([[80231001, 1, 2], [80781001, 1, 2], [80331001, 1, 2]]),
        "props": None
    }),
    100171: _tools.RODict({
        "ID": 100171,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":90}),
        "equipment": _tools.ROList([[80231001, 2, 2], [80781001, 2, 2], [80331001, 2, 2]]),
        "props": None
    }),
    100172: _tools.RODict({
        "ID": 100172,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":90}),
        "equipment": _tools.ROList([[80231001, 3, 2], [80781001, 3, 2], [80331001, 3, 2]]),
        "props": None
    }),
    100173: _tools.RODict({
        "ID": 100173,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":120}),
        "equipment": _tools.ROList([[80231001, 4, 2], [80781001, 4, 2], [80331001, 4, 2]]),
        "props": None
    }),
    100174: _tools.RODict({
        "ID": 100174,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":150}),
        "equipment": _tools.ROList([[80231001, 5, 2], [80781001, 5, 2], [80331001, 5, 2]]),
        "props": None
    }),
    100175: _tools.RODict({
        "ID": 100175,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":180}),
        "equipment": _tools.ROList([[80231001, 6, 2], [80781001, 6, 2], [80331001, 6, 2]]),
        "props": None
    }),
    100176: _tools.RODict({
        "ID": 100176,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":270}),
        "equipment": _tools.ROList([[80231001, 7, 2], [80781001, 7, 2], [80331001, 7, 2]]),
        "props": None
    }),
    100177: _tools.RODict({
        "ID": 100177,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":90}),
        "equipment": _tools.ROList([[80231001, 0, 3], [80781001, 0, 3], [80331001, 0, 3]]),
        "props": None
    }),
    100178: _tools.RODict({
        "ID": 100178,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":105}),
        "equipment": _tools.ROList([[80231001, 1, 3], [80781001, 1, 3], [80331001, 1, 3]]),
        "props": None
    }),
    100179: _tools.RODict({
        "ID": 100179,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":120}),
        "equipment": _tools.ROList([[80231001, 2, 3], [80781001, 2, 3], [80331001, 2, 3]]),
        "props": None
    }),
    100180: _tools.RODict({
        "ID": 100180,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":120}),
        "equipment": _tools.ROList([[80231001, 3, 3], [80781001, 3, 3], [80331001, 3, 3]]),
        "props": None
    }),
    100181: _tools.RODict({
        "ID": 100181,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":150}),
        "equipment": _tools.ROList([[80231001, 4, 3], [80781001, 4, 3], [80331001, 4, 3]]),
        "props": None
    }),
    100182: _tools.RODict({
        "ID": 100182,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":180}),
        "equipment": _tools.ROList([[80231001, 5, 3], [80781001, 5, 3], [80331001, 5, 3]]),
        "props": None
    }),
    100183: _tools.RODict({
        "ID": 100183,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":210}),
        "equipment": _tools.ROList([[80231001, 6, 3], [80781001, 6, 3], [80331001, 6, 3]]),
        "props": None
    }),
    100184: _tools.RODict({
        "ID": 100184,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":300}),
        "equipment": _tools.ROList([[80231001, 7, 3], [80781001, 7, 3], [80331001, 7, 3]]),
        "props": None
    }),
    100185: _tools.RODict({
        "ID": 100185,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":120}),
        "equipment": _tools.ROList([[80231001, 0, 4], [80781001, 0, 4], [80331001, 0, 4]]),
        "props": None
    }),
    100186: _tools.RODict({
        "ID": 100186,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":135}),
        "equipment": _tools.ROList([[80231001, 1, 4], [80781001, 1, 4], [80331001, 1, 4]]),
        "props": None
    }),
    100187: _tools.RODict({
        "ID": 100187,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":150}),
        "equipment": _tools.ROList([[80231001, 2, 4], [80781001, 2, 4], [80331001, 2, 4]]),
        "props": None
    }),
    100188: _tools.RODict({
        "ID": 100188,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":150}),
        "equipment": _tools.ROList([[80231001, 3, 4], [80781001, 3, 4], [80331001, 3, 4]]),
        "props": None
    }),
    100189: _tools.RODict({
        "ID": 100189,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":180}),
        "equipment": _tools.ROList([[80231001, 4, 4], [80781001, 4, 4], [80331001, 4, 4]]),
        "props": None
    }),
    100190: _tools.RODict({
        "ID": 100190,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":210}),
        "equipment": _tools.ROList([[80231001, 5, 4], [80781001, 5, 4], [80331001, 5, 4]]),
        "props": None
    }),
    100191: _tools.RODict({
        "ID": 100191,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":240}),
        "equipment": _tools.ROList([[80231001, 6, 4], [80781001, 6, 4], [80331001, 6, 4]]),
        "props": None
    }),
    100192: _tools.RODict({
        "ID": 100192,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":330}),
        "equipment": _tools.ROList([[80231001, 7, 4], [80781001, 7, 4], [80331001, 7, 4]]),
        "props": None
    }),
    100193: _tools.RODict({
        "ID": 100193,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.001}),
        "equipment": _tools.ROList([[80311001, 0, 1], [80411001, 0, 1], [80811001, 0, 1]]),
        "props": None
    }),
    100194: _tools.RODict({
        "ID": 100194,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.001}),
        "equipment": _tools.ROList([[80311001, 1, 1], [80411001, 1, 1], [80811001, 1, 1]]),
        "props": None
    }),
    100195: _tools.RODict({
        "ID": 100195,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0015}),
        "equipment": _tools.ROList([[80311001, 2, 1], [80411001, 2, 1], [80811001, 2, 1]]),
        "props": None
    }),
    100196: _tools.RODict({
        "ID": 100196,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.002}),
        "equipment": _tools.ROList([[80311001, 3, 1], [80411001, 3, 1], [80811001, 3, 1]]),
        "props": None
    }),
    100197: _tools.RODict({
        "ID": 100197,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.003}),
        "equipment": _tools.ROList([[80311001, 4, 1], [80411001, 4, 1], [80811001, 4, 1]]),
        "props": None
    }),
    100198: _tools.RODict({
        "ID": 100198,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.004}),
        "equipment": _tools.ROList([[80311001, 5, 1], [80411001, 5, 1], [80811001, 5, 1]]),
        "props": None
    }),
    100199: _tools.RODict({
        "ID": 100199,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.005}),
        "equipment": _tools.ROList([[80311001, 6, 1], [80411001, 6, 1], [80811001, 6, 1]]),
        "props": None
    }),
    100200: _tools.RODict({
        "ID": 100200,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0075}),
        "equipment": _tools.ROList([[80311001, 7, 1], [80411001, 7, 1], [80811001, 7, 1]]),
        "props": None
    }),
    100201: _tools.RODict({
        "ID": 100201,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0015}),
        "equipment": _tools.ROList([[80311001, 0, 2], [80411001, 0, 2], [80811001, 0, 2]]),
        "props": None
    }),
    100202: _tools.RODict({
        "ID": 100202,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0015}),
        "equipment": _tools.ROList([[80311001, 1, 2], [80411001, 1, 2], [80811001, 1, 2]]),
        "props": None
    }),
    100203: _tools.RODict({
        "ID": 100203,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.002}),
        "equipment": _tools.ROList([[80311001, 2, 2], [80411001, 2, 2], [80811001, 2, 2]]),
        "props": None
    }),
    100204: _tools.RODict({
        "ID": 100204,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0025}),
        "equipment": _tools.ROList([[80311001, 3, 2], [80411001, 3, 2], [80811001, 3, 2]]),
        "props": None
    }),
    100205: _tools.RODict({
        "ID": 100205,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0035}),
        "equipment": _tools.ROList([[80311001, 4, 2], [80411001, 4, 2], [80811001, 4, 2]]),
        "props": None
    }),
    100206: _tools.RODict({
        "ID": 100206,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0045}),
        "equipment": _tools.ROList([[80311001, 5, 2], [80411001, 5, 2], [80811001, 5, 2]]),
        "props": None
    }),
    100207: _tools.RODict({
        "ID": 100207,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0055}),
        "equipment": _tools.ROList([[80311001, 6, 2], [80411001, 6, 2], [80811001, 6, 2]]),
        "props": None
    }),
    100208: _tools.RODict({
        "ID": 100208,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.008}),
        "equipment": _tools.ROList([[80311001, 7, 2], [80411001, 7, 2], [80811001, 7, 2]]),
        "props": None
    }),
    100209: _tools.RODict({
        "ID": 100209,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.002}),
        "equipment": _tools.ROList([[80311001, 0, 3], [80411001, 0, 3], [80811001, 0, 3]]),
        "props": None
    }),
    100210: _tools.RODict({
        "ID": 100210,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0025}),
        "equipment": _tools.ROList([[80311001, 1, 3], [80411001, 1, 3], [80811001, 1, 3]]),
        "props": None
    }),
    100211: _tools.RODict({
        "ID": 100211,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0025}),
        "equipment": _tools.ROList([[80311001, 2, 3], [80411001, 2, 3], [80811001, 2, 3]]),
        "props": None
    }),
    100212: _tools.RODict({
        "ID": 100212,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.003}),
        "equipment": _tools.ROList([[80311001, 3, 3], [80411001, 3, 3], [80811001, 3, 3]]),
        "props": None
    }),
    100213: _tools.RODict({
        "ID": 100213,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.004}),
        "equipment": _tools.ROList([[80311001, 4, 3], [80411001, 4, 3], [80811001, 4, 3]]),
        "props": None
    }),
    100214: _tools.RODict({
        "ID": 100214,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.005}),
        "equipment": _tools.ROList([[80311001, 5, 3], [80411001, 5, 3], [80811001, 5, 3]]),
        "props": None
    }),
    100215: _tools.RODict({
        "ID": 100215,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.006}),
        "equipment": _tools.ROList([[80311001, 6, 3], [80411001, 6, 3], [80811001, 6, 3]]),
        "props": None
    }),
    100216: _tools.RODict({
        "ID": 100216,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0085}),
        "equipment": _tools.ROList([[80311001, 7, 3], [80411001, 7, 3], [80811001, 7, 3]]),
        "props": None
    }),
    100217: _tools.RODict({
        "ID": 100217,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0025}),
        "equipment": _tools.ROList([[80311001, 0, 4], [80411001, 0, 4], [80811001, 0, 4]]),
        "props": None
    }),
    100218: _tools.RODict({
        "ID": 100218,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.003}),
        "equipment": _tools.ROList([[80311001, 1, 4], [80411001, 1, 4], [80811001, 1, 4]]),
        "props": None
    }),
    100219: _tools.RODict({
        "ID": 100219,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.003}),
        "equipment": _tools.ROList([[80311001, 2, 4], [80411001, 2, 4], [80811001, 2, 4]]),
        "props": None
    }),
    100220: _tools.RODict({
        "ID": 100220,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0035}),
        "equipment": _tools.ROList([[80311001, 3, 4], [80411001, 3, 4], [80811001, 3, 4]]),
        "props": None
    }),
    100221: _tools.RODict({
        "ID": 100221,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0045}),
        "equipment": _tools.ROList([[80311001, 4, 4], [80411001, 4, 4], [80811001, 4, 4]]),
        "props": None
    }),
    100222: _tools.RODict({
        "ID": 100222,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0055}),
        "equipment": _tools.ROList([[80311001, 5, 4], [80411001, 5, 4], [80811001, 5, 4]]),
        "props": None
    }),
    100223: _tools.RODict({
        "ID": 100223,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0065}),
        "equipment": _tools.ROList([[80311001, 6, 4], [80411001, 6, 4], [80811001, 6, 4]]),
        "props": None
    }),
    100224: _tools.RODict({
        "ID": 100224,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.009}),
        "equipment": _tools.ROList([[80311001, 7, 4], [80411001, 7, 4], [80811001, 7, 4]]),
        "props": None
    }),
    100225: _tools.RODict({
        "ID": 100225,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.001}),
        "equipment": _tools.ROList([[80321001, 0, 1], [80421001, 0, 1], [80821001, 0, 1]]),
        "props": None
    }),
    100226: _tools.RODict({
        "ID": 100226,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.001}),
        "equipment": _tools.ROList([[80321001, 1, 1], [80421001, 1, 1], [80821001, 1, 1]]),
        "props": None
    }),
    100227: _tools.RODict({
        "ID": 100227,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0015}),
        "equipment": _tools.ROList([[80321001, 2, 1], [80421001, 2, 1], [80821001, 2, 1]]),
        "props": None
    }),
    100228: _tools.RODict({
        "ID": 100228,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.002}),
        "equipment": _tools.ROList([[80321001, 3, 1], [80421001, 3, 1], [80821001, 3, 1]]),
        "props": None
    }),
    100229: _tools.RODict({
        "ID": 100229,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.003}),
        "equipment": _tools.ROList([[80321001, 4, 1], [80421001, 4, 1], [80821001, 4, 1]]),
        "props": None
    }),
    100230: _tools.RODict({
        "ID": 100230,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.004}),
        "equipment": _tools.ROList([[80321001, 5, 1], [80421001, 5, 1], [80821001, 5, 1]]),
        "props": None
    }),
    100231: _tools.RODict({
        "ID": 100231,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.005}),
        "equipment": _tools.ROList([[80321001, 6, 1], [80421001, 6, 1], [80821001, 6, 1]]),
        "props": None
    }),
    100232: _tools.RODict({
        "ID": 100232,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0075}),
        "equipment": _tools.ROList([[80321001, 7, 1], [80421001, 7, 1], [80821001, 7, 1]]),
        "props": None
    }),
    100233: _tools.RODict({
        "ID": 100233,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0015}),
        "equipment": _tools.ROList([[80321001, 0, 2], [80421001, 0, 2], [80821001, 0, 2]]),
        "props": None
    }),
    100234: _tools.RODict({
        "ID": 100234,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0015}),
        "equipment": _tools.ROList([[80321001, 1, 2], [80421001, 1, 2], [80821001, 1, 2]]),
        "props": None
    }),
    100235: _tools.RODict({
        "ID": 100235,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.002}),
        "equipment": _tools.ROList([[80321001, 2, 2], [80421001, 2, 2], [80821001, 2, 2]]),
        "props": None
    }),
    100236: _tools.RODict({
        "ID": 100236,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0025}),
        "equipment": _tools.ROList([[80321001, 3, 2], [80421001, 3, 2], [80821001, 3, 2]]),
        "props": None
    }),
    100237: _tools.RODict({
        "ID": 100237,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0035}),
        "equipment": _tools.ROList([[80321001, 4, 2], [80421001, 4, 2], [80821001, 4, 2]]),
        "props": None
    }),
    100238: _tools.RODict({
        "ID": 100238,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0045}),
        "equipment": _tools.ROList([[80321001, 5, 2], [80421001, 5, 2], [80821001, 5, 2]]),
        "props": None
    }),
    100239: _tools.RODict({
        "ID": 100239,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0055}),
        "equipment": _tools.ROList([[80321001, 6, 2], [80421001, 6, 2], [80821001, 6, 2]]),
        "props": None
    }),
    100240: _tools.RODict({
        "ID": 100240,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.008}),
        "equipment": _tools.ROList([[80321001, 7, 2], [80421001, 7, 2], [80821001, 7, 2]]),
        "props": None
    }),
    100241: _tools.RODict({
        "ID": 100241,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.002}),
        "equipment": _tools.ROList([[80321001, 0, 3], [80421001, 0, 3], [80821001, 0, 3]]),
        "props": None
    }),
    100242: _tools.RODict({
        "ID": 100242,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0025}),
        "equipment": _tools.ROList([[80321001, 1, 3], [80421001, 1, 3], [80821001, 1, 3]]),
        "props": None
    }),
    100243: _tools.RODict({
        "ID": 100243,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0025}),
        "equipment": _tools.ROList([[80321001, 2, 3], [80421001, 2, 3], [80821001, 2, 3]]),
        "props": None
    }),
    100244: _tools.RODict({
        "ID": 100244,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.003}),
        "equipment": _tools.ROList([[80321001, 3, 3], [80421001, 3, 3], [80821001, 3, 3]]),
        "props": None
    }),
    100245: _tools.RODict({
        "ID": 100245,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.004}),
        "equipment": _tools.ROList([[80321001, 4, 3], [80421001, 4, 3], [80821001, 4, 3]]),
        "props": None
    }),
    100246: _tools.RODict({
        "ID": 100246,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.005}),
        "equipment": _tools.ROList([[80321001, 5, 3], [80421001, 5, 3], [80821001, 5, 3]]),
        "props": None
    }),
    100247: _tools.RODict({
        "ID": 100247,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.006}),
        "equipment": _tools.ROList([[80321001, 6, 3], [80421001, 6, 3], [80821001, 6, 3]]),
        "props": None
    }),
    100248: _tools.RODict({
        "ID": 100248,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0085}),
        "equipment": _tools.ROList([[80321001, 7, 3], [80421001, 7, 3], [80821001, 7, 3]]),
        "props": None
    }),
    100249: _tools.RODict({
        "ID": 100249,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0025}),
        "equipment": _tools.ROList([[80321001, 0, 4], [80421001, 0, 4], [80821001, 0, 4]]),
        "props": None
    }),
    100250: _tools.RODict({
        "ID": 100250,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.003}),
        "equipment": _tools.ROList([[80321001, 1, 4], [80421001, 1, 4], [80821001, 1, 4]]),
        "props": None
    }),
    100251: _tools.RODict({
        "ID": 100251,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.003}),
        "equipment": _tools.ROList([[80321001, 2, 4], [80421001, 2, 4], [80821001, 2, 4]]),
        "props": None
    }),
    100252: _tools.RODict({
        "ID": 100252,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0035}),
        "equipment": _tools.ROList([[80321001, 3, 4], [80421001, 3, 4], [80821001, 3, 4]]),
        "props": None
    }),
    100253: _tools.RODict({
        "ID": 100253,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0045}),
        "equipment": _tools.ROList([[80321001, 4, 4], [80421001, 4, 4], [80821001, 4, 4]]),
        "props": None
    }),
    100254: _tools.RODict({
        "ID": 100254,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0055}),
        "equipment": _tools.ROList([[80321001, 5, 4], [80421001, 5, 4], [80821001, 5, 4]]),
        "props": None
    }),
    100255: _tools.RODict({
        "ID": 100255,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0065}),
        "equipment": _tools.ROList([[80321001, 6, 4], [80421001, 6, 4], [80821001, 6, 4]]),
        "props": None
    }),
    100256: _tools.RODict({
        "ID": 100256,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.009}),
        "equipment": _tools.ROList([[80321001, 7, 4], [80421001, 7, 4], [80821001, 7, 4]]),
        "props": None
    }),
    100257: _tools.RODict({
        "ID": 100257,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.001}),
        "equipment": _tools.ROList([[80831001, 0, 1], [80431001, 0, 1], [80331001, 0, 1]]),
        "props": None
    }),
    100258: _tools.RODict({
        "ID": 100258,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.001}),
        "equipment": _tools.ROList([[80831001, 1, 1], [80431001, 1, 1], [80331001, 1, 1]]),
        "props": None
    }),
    100259: _tools.RODict({
        "ID": 100259,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.0015}),
        "equipment": _tools.ROList([[80831001, 2, 1], [80431001, 2, 1], [80331001, 2, 1]]),
        "props": None
    }),
    100260: _tools.RODict({
        "ID": 100260,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.002}),
        "equipment": _tools.ROList([[80831001, 3, 1], [80431001, 3, 1], [80331001, 3, 1]]),
        "props": None
    }),
    100261: _tools.RODict({
        "ID": 100261,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.003}),
        "equipment": _tools.ROList([[80831001, 4, 1], [80431001, 4, 1], [80331001, 4, 1]]),
        "props": None
    }),
    100262: _tools.RODict({
        "ID": 100262,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.004}),
        "equipment": _tools.ROList([[80831001, 5, 1], [80431001, 5, 1], [80331001, 5, 1]]),
        "props": None
    }),
    100263: _tools.RODict({
        "ID": 100263,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.005}),
        "equipment": _tools.ROList([[80831001, 6, 1], [80431001, 6, 1], [80331001, 6, 1]]),
        "props": None
    }),
    100264: _tools.RODict({
        "ID": 100264,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.0075}),
        "equipment": _tools.ROList([[80831001, 7, 1], [80431001, 7, 1], [80331001, 7, 1]]),
        "props": None
    }),
    100265: _tools.RODict({
        "ID": 100265,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.0015}),
        "equipment": _tools.ROList([[80831001, 0, 2], [80431001, 0, 2], [80331001, 0, 2]]),
        "props": None
    }),
    100266: _tools.RODict({
        "ID": 100266,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.0015}),
        "equipment": _tools.ROList([[80831001, 1, 2], [80431001, 1, 2], [80331001, 1, 2]]),
        "props": None
    }),
    100267: _tools.RODict({
        "ID": 100267,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.002}),
        "equipment": _tools.ROList([[80831001, 2, 2], [80431001, 2, 2], [80331001, 2, 2]]),
        "props": None
    }),
    100268: _tools.RODict({
        "ID": 100268,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.0025}),
        "equipment": _tools.ROList([[80831001, 3, 2], [80431001, 3, 2], [80331001, 3, 2]]),
        "props": None
    }),
    100269: _tools.RODict({
        "ID": 100269,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.0035}),
        "equipment": _tools.ROList([[80831001, 4, 2], [80431001, 4, 2], [80331001, 4, 2]]),
        "props": None
    }),
    100270: _tools.RODict({
        "ID": 100270,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.0045}),
        "equipment": _tools.ROList([[80831001, 5, 2], [80431001, 5, 2], [80331001, 5, 2]]),
        "props": None
    }),
    100271: _tools.RODict({
        "ID": 100271,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.0055}),
        "equipment": _tools.ROList([[80831001, 6, 2], [80431001, 6, 2], [80331001, 6, 2]]),
        "props": None
    }),
    100272: _tools.RODict({
        "ID": 100272,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.008}),
        "equipment": _tools.ROList([[80831001, 7, 2], [80431001, 7, 2], [80331001, 7, 2]]),
        "props": None
    }),
    100273: _tools.RODict({
        "ID": 100273,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.002}),
        "equipment": _tools.ROList([[80831001, 0, 3], [80431001, 0, 3], [80331001, 0, 3]]),
        "props": None
    }),
    100274: _tools.RODict({
        "ID": 100274,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.0025}),
        "equipment": _tools.ROList([[80831001, 1, 3], [80431001, 1, 3], [80331001, 1, 3]]),
        "props": None
    }),
    100275: _tools.RODict({
        "ID": 100275,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.0025}),
        "equipment": _tools.ROList([[80831001, 2, 3], [80431001, 2, 3], [80331001, 2, 3]]),
        "props": None
    }),
    100276: _tools.RODict({
        "ID": 100276,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.003}),
        "equipment": _tools.ROList([[80831001, 3, 3], [80431001, 3, 3], [80331001, 3, 3]]),
        "props": None
    }),
    100277: _tools.RODict({
        "ID": 100277,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.004}),
        "equipment": _tools.ROList([[80831001, 4, 3], [80431001, 4, 3], [80331001, 4, 3]]),
        "props": None
    }),
    100278: _tools.RODict({
        "ID": 100278,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.005}),
        "equipment": _tools.ROList([[80831001, 5, 3], [80431001, 5, 3], [80331001, 5, 3]]),
        "props": None
    }),
    100279: _tools.RODict({
        "ID": 100279,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.006}),
        "equipment": _tools.ROList([[80831001, 6, 3], [80431001, 6, 3], [80331001, 6, 3]]),
        "props": None
    }),
    100280: _tools.RODict({
        "ID": 100280,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.0085}),
        "equipment": _tools.ROList([[80831001, 7, 3], [80431001, 7, 3], [80331001, 7, 3]]),
        "props": None
    }),
    100281: _tools.RODict({
        "ID": 100281,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.0025}),
        "equipment": _tools.ROList([[80831001, 0, 4], [80431001, 0, 4], [80331001, 0, 4]]),
        "props": None
    }),
    100282: _tools.RODict({
        "ID": 100282,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.003}),
        "equipment": _tools.ROList([[80831001, 1, 4], [80431001, 1, 4], [80331001, 1, 4]]),
        "props": None
    }),
    100283: _tools.RODict({
        "ID": 100283,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.003}),
        "equipment": _tools.ROList([[80831001, 2, 4], [80431001, 2, 4], [80331001, 2, 4]]),
        "props": None
    }),
    100284: _tools.RODict({
        "ID": 100284,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.0035}),
        "equipment": _tools.ROList([[80831001, 3, 4], [80431001, 3, 4], [80331001, 3, 4]]),
        "props": None
    }),
    100285: _tools.RODict({
        "ID": 100285,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.0045}),
        "equipment": _tools.ROList([[80831001, 4, 4], [80431001, 4, 4], [80331001, 4, 4]]),
        "props": None
    }),
    100286: _tools.RODict({
        "ID": 100286,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.0055}),
        "equipment": _tools.ROList([[80831001, 5, 4], [80431001, 5, 4], [80331001, 5, 4]]),
        "props": None
    }),
    100287: _tools.RODict({
        "ID": 100287,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.0065}),
        "equipment": _tools.ROList([[80831001, 6, 4], [80431001, 6, 4], [80331001, 6, 4]]),
        "props": None
    }),
    100288: _tools.RODict({
        "ID": 100288,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.009}),
        "equipment": _tools.ROList([[80831001, 7, 4], [80431001, 7, 4], [80331001, 7, 4]]),
        "props": None
    }),
    100289: _tools.RODict({
        "ID": 100289,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.001}),
        "equipment": _tools.ROList([[80411001, 0, 1], [80811001, 0, 1], [80211001, 0, 1]]),
        "props": None
    }),
    100290: _tools.RODict({
        "ID": 100290,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.001}),
        "equipment": _tools.ROList([[80411001, 1, 1], [80811001, 1, 1], [80211001, 1, 1]]),
        "props": None
    }),
    100291: _tools.RODict({
        "ID": 100291,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80411001, 2, 1], [80811001, 2, 1], [80211001, 2, 1]]),
        "props": None
    }),
    100292: _tools.RODict({
        "ID": 100292,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.002}),
        "equipment": _tools.ROList([[80411001, 3, 1], [80811001, 3, 1], [80211001, 3, 1]]),
        "props": None
    }),
    100293: _tools.RODict({
        "ID": 100293,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.003}),
        "equipment": _tools.ROList([[80411001, 4, 1], [80811001, 4, 1], [80211001, 4, 1]]),
        "props": None
    }),
    100294: _tools.RODict({
        "ID": 100294,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.004}),
        "equipment": _tools.ROList([[80411001, 5, 1], [80811001, 5, 1], [80211001, 5, 1]]),
        "props": None
    }),
    100295: _tools.RODict({
        "ID": 100295,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.005}),
        "equipment": _tools.ROList([[80411001, 6, 1], [80811001, 6, 1], [80211001, 6, 1]]),
        "props": None
    }),
    100296: _tools.RODict({
        "ID": 100296,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0075}),
        "equipment": _tools.ROList([[80411001, 7, 1], [80811001, 7, 1], [80211001, 7, 1]]),
        "props": None
    }),
    100297: _tools.RODict({
        "ID": 100297,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80411001, 0, 2], [80811001, 0, 2], [80211001, 0, 2]]),
        "props": None
    }),
    100298: _tools.RODict({
        "ID": 100298,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80411001, 1, 2], [80811001, 1, 2], [80211001, 1, 2]]),
        "props": None
    }),
    100299: _tools.RODict({
        "ID": 100299,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.002}),
        "equipment": _tools.ROList([[80411001, 2, 2], [80811001, 2, 2], [80211001, 2, 2]]),
        "props": None
    }),
    100300: _tools.RODict({
        "ID": 100300,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80411001, 3, 2], [80811001, 3, 2], [80211001, 3, 2]]),
        "props": None
    }),
    100301: _tools.RODict({
        "ID": 100301,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0035}),
        "equipment": _tools.ROList([[80411001, 4, 2], [80811001, 4, 2], [80211001, 4, 2]]),
        "props": None
    }),
    100302: _tools.RODict({
        "ID": 100302,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0045}),
        "equipment": _tools.ROList([[80411001, 5, 2], [80811001, 5, 2], [80211001, 5, 2]]),
        "props": None
    }),
    100303: _tools.RODict({
        "ID": 100303,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0055}),
        "equipment": _tools.ROList([[80411001, 6, 2], [80811001, 6, 2], [80211001, 6, 2]]),
        "props": None
    }),
    100304: _tools.RODict({
        "ID": 100304,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.008}),
        "equipment": _tools.ROList([[80411001, 7, 2], [80811001, 7, 2], [80211001, 7, 2]]),
        "props": None
    }),
    100305: _tools.RODict({
        "ID": 100305,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.002}),
        "equipment": _tools.ROList([[80411001, 0, 3], [80811001, 0, 3], [80211001, 0, 3]]),
        "props": None
    }),
    100306: _tools.RODict({
        "ID": 100306,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80411001, 1, 3], [80811001, 1, 3], [80211001, 1, 3]]),
        "props": None
    }),
    100307: _tools.RODict({
        "ID": 100307,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80411001, 2, 3], [80811001, 2, 3], [80211001, 2, 3]]),
        "props": None
    }),
    100308: _tools.RODict({
        "ID": 100308,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.003}),
        "equipment": _tools.ROList([[80411001, 3, 3], [80811001, 3, 3], [80211001, 3, 3]]),
        "props": None
    }),
    100309: _tools.RODict({
        "ID": 100309,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.004}),
        "equipment": _tools.ROList([[80411001, 4, 3], [80811001, 4, 3], [80211001, 4, 3]]),
        "props": None
    }),
    100310: _tools.RODict({
        "ID": 100310,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.005}),
        "equipment": _tools.ROList([[80411001, 5, 3], [80811001, 5, 3], [80211001, 5, 3]]),
        "props": None
    }),
    100311: _tools.RODict({
        "ID": 100311,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.006}),
        "equipment": _tools.ROList([[80411001, 6, 3], [80811001, 6, 3], [80211001, 6, 3]]),
        "props": None
    }),
    100312: _tools.RODict({
        "ID": 100312,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0085}),
        "equipment": _tools.ROList([[80411001, 7, 3], [80811001, 7, 3], [80211001, 7, 3]]),
        "props": None
    }),
    100313: _tools.RODict({
        "ID": 100313,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80411001, 0, 4], [80811001, 0, 4], [80211001, 0, 4]]),
        "props": None
    }),
    100314: _tools.RODict({
        "ID": 100314,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.003}),
        "equipment": _tools.ROList([[80411001, 1, 4], [80811001, 1, 4], [80211001, 1, 4]]),
        "props": None
    }),
    100315: _tools.RODict({
        "ID": 100315,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.003}),
        "equipment": _tools.ROList([[80411001, 2, 4], [80811001, 2, 4], [80211001, 2, 4]]),
        "props": None
    }),
    100316: _tools.RODict({
        "ID": 100316,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0035}),
        "equipment": _tools.ROList([[80411001, 3, 4], [80811001, 3, 4], [80211001, 3, 4]]),
        "props": None
    }),
    100317: _tools.RODict({
        "ID": 100317,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0045}),
        "equipment": _tools.ROList([[80411001, 4, 4], [80811001, 4, 4], [80211001, 4, 4]]),
        "props": None
    }),
    100318: _tools.RODict({
        "ID": 100318,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0055}),
        "equipment": _tools.ROList([[80411001, 5, 4], [80811001, 5, 4], [80211001, 5, 4]]),
        "props": None
    }),
    100319: _tools.RODict({
        "ID": 100319,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0065}),
        "equipment": _tools.ROList([[80411001, 6, 4], [80811001, 6, 4], [80211001, 6, 4]]),
        "props": None
    }),
    100320: _tools.RODict({
        "ID": 100320,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.009}),
        "equipment": _tools.ROList([[80411001, 7, 4], [80811001, 7, 4], [80211001, 7, 4]]),
        "props": None
    }),
    100321: _tools.RODict({
        "ID": 100321,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.001}),
        "equipment": _tools.ROList([[80421001, 0, 1], [80821001, 0, 1], [80221001, 0, 1]]),
        "props": None
    }),
    100322: _tools.RODict({
        "ID": 100322,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.001}),
        "equipment": _tools.ROList([[80421001, 1, 1], [80821001, 1, 1], [80221001, 1, 1]]),
        "props": None
    }),
    100323: _tools.RODict({
        "ID": 100323,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80421001, 2, 1], [80821001, 2, 1], [80221001, 2, 1]]),
        "props": None
    }),
    100324: _tools.RODict({
        "ID": 100324,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.002}),
        "equipment": _tools.ROList([[80421001, 3, 1], [80821001, 3, 1], [80221001, 3, 1]]),
        "props": None
    }),
    100325: _tools.RODict({
        "ID": 100325,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.003}),
        "equipment": _tools.ROList([[80421001, 4, 1], [80821001, 4, 1], [80221001, 4, 1]]),
        "props": None
    }),
    100326: _tools.RODict({
        "ID": 100326,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.004}),
        "equipment": _tools.ROList([[80421001, 5, 1], [80821001, 5, 1], [80221001, 5, 1]]),
        "props": None
    }),
    100327: _tools.RODict({
        "ID": 100327,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.005}),
        "equipment": _tools.ROList([[80421001, 6, 1], [80821001, 6, 1], [80221001, 6, 1]]),
        "props": None
    }),
    100328: _tools.RODict({
        "ID": 100328,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0075}),
        "equipment": _tools.ROList([[80421001, 7, 1], [80821001, 7, 1], [80221001, 7, 1]]),
        "props": None
    }),
    100329: _tools.RODict({
        "ID": 100329,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80421001, 0, 2], [80821001, 0, 2], [80221001, 0, 2]]),
        "props": None
    }),
    100330: _tools.RODict({
        "ID": 100330,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80421001, 1, 2], [80821001, 1, 2], [80221001, 1, 2]]),
        "props": None
    }),
    100331: _tools.RODict({
        "ID": 100331,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.002}),
        "equipment": _tools.ROList([[80421001, 2, 2], [80821001, 2, 2], [80221001, 2, 2]]),
        "props": None
    }),
    100332: _tools.RODict({
        "ID": 100332,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80421001, 3, 2], [80821001, 3, 2], [80221001, 3, 2]]),
        "props": None
    }),
    100333: _tools.RODict({
        "ID": 100333,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0035}),
        "equipment": _tools.ROList([[80421001, 4, 2], [80821001, 4, 2], [80221001, 4, 2]]),
        "props": None
    }),
    100334: _tools.RODict({
        "ID": 100334,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0045}),
        "equipment": _tools.ROList([[80421001, 5, 2], [80821001, 5, 2], [80221001, 5, 2]]),
        "props": None
    }),
    100335: _tools.RODict({
        "ID": 100335,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0055}),
        "equipment": _tools.ROList([[80421001, 6, 2], [80821001, 6, 2], [80221001, 6, 2]]),
        "props": None
    }),
    100336: _tools.RODict({
        "ID": 100336,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.008}),
        "equipment": _tools.ROList([[80421001, 7, 2], [80821001, 7, 2], [80221001, 7, 2]]),
        "props": None
    }),
    100337: _tools.RODict({
        "ID": 100337,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.002}),
        "equipment": _tools.ROList([[80421001, 0, 3], [80821001, 0, 3], [80221001, 0, 3]]),
        "props": None
    }),
    100338: _tools.RODict({
        "ID": 100338,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80421001, 1, 3], [80821001, 1, 3], [80221001, 1, 3]]),
        "props": None
    }),
    100339: _tools.RODict({
        "ID": 100339,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80421001, 2, 3], [80821001, 2, 3], [80221001, 2, 3]]),
        "props": None
    }),
    100340: _tools.RODict({
        "ID": 100340,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.003}),
        "equipment": _tools.ROList([[80421001, 3, 3], [80821001, 3, 3], [80221001, 3, 3]]),
        "props": None
    }),
    100341: _tools.RODict({
        "ID": 100341,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.004}),
        "equipment": _tools.ROList([[80421001, 4, 3], [80821001, 4, 3], [80221001, 4, 3]]),
        "props": None
    }),
    100342: _tools.RODict({
        "ID": 100342,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.005}),
        "equipment": _tools.ROList([[80421001, 5, 3], [80821001, 5, 3], [80221001, 5, 3]]),
        "props": None
    }),
    100343: _tools.RODict({
        "ID": 100343,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.006}),
        "equipment": _tools.ROList([[80421001, 6, 3], [80821001, 6, 3], [80221001, 6, 3]]),
        "props": None
    }),
    100344: _tools.RODict({
        "ID": 100344,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0085}),
        "equipment": _tools.ROList([[80421001, 7, 3], [80821001, 7, 3], [80221001, 7, 3]]),
        "props": None
    }),
    100345: _tools.RODict({
        "ID": 100345,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80421001, 0, 4], [80821001, 0, 4], [80221001, 0, 4]]),
        "props": None
    }),
    100346: _tools.RODict({
        "ID": 100346,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.003}),
        "equipment": _tools.ROList([[80421001, 1, 4], [80821001, 1, 4], [80221001, 1, 4]]),
        "props": None
    }),
    100347: _tools.RODict({
        "ID": 100347,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.003}),
        "equipment": _tools.ROList([[80421001, 2, 4], [80821001, 2, 4], [80221001, 2, 4]]),
        "props": None
    }),
    100348: _tools.RODict({
        "ID": 100348,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0035}),
        "equipment": _tools.ROList([[80421001, 3, 4], [80821001, 3, 4], [80221001, 3, 4]]),
        "props": None
    }),
    100349: _tools.RODict({
        "ID": 100349,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0045}),
        "equipment": _tools.ROList([[80421001, 4, 4], [80821001, 4, 4], [80221001, 4, 4]]),
        "props": None
    }),
    100350: _tools.RODict({
        "ID": 100350,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0055}),
        "equipment": _tools.ROList([[80421001, 5, 4], [80821001, 5, 4], [80221001, 5, 4]]),
        "props": None
    }),
    100351: _tools.RODict({
        "ID": 100351,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0065}),
        "equipment": _tools.ROList([[80421001, 6, 4], [80821001, 6, 4], [80221001, 6, 4]]),
        "props": None
    }),
    100352: _tools.RODict({
        "ID": 100352,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.009}),
        "equipment": _tools.ROList([[80421001, 7, 4], [80821001, 7, 4], [80221001, 7, 4]]),
        "props": None
    }),
    100353: _tools.RODict({
        "ID": 100353,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.001}),
        "equipment": _tools.ROList([[80431001, 0, 1], [80831001, 0, 1], [80231001, 0, 1]]),
        "props": None
    }),
    100354: _tools.RODict({
        "ID": 100354,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.001}),
        "equipment": _tools.ROList([[80431001, 1, 1], [80831001, 1, 1], [80231001, 1, 1]]),
        "props": None
    }),
    100355: _tools.RODict({
        "ID": 100355,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80431001, 2, 1], [80831001, 2, 1], [80231001, 2, 1]]),
        "props": None
    }),
    100356: _tools.RODict({
        "ID": 100356,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.002}),
        "equipment": _tools.ROList([[80431001, 3, 1], [80831001, 3, 1], [80231001, 3, 1]]),
        "props": None
    }),
    100357: _tools.RODict({
        "ID": 100357,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.003}),
        "equipment": _tools.ROList([[80431001, 4, 1], [80831001, 4, 1], [80231001, 4, 1]]),
        "props": None
    }),
    100358: _tools.RODict({
        "ID": 100358,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.004}),
        "equipment": _tools.ROList([[80431001, 5, 1], [80831001, 5, 1], [80231001, 5, 1]]),
        "props": None
    }),
    100359: _tools.RODict({
        "ID": 100359,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.005}),
        "equipment": _tools.ROList([[80431001, 6, 1], [80831001, 6, 1], [80231001, 6, 1]]),
        "props": None
    }),
    100360: _tools.RODict({
        "ID": 100360,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0075}),
        "equipment": _tools.ROList([[80431001, 7, 1], [80831001, 7, 1], [80231001, 7, 1]]),
        "props": None
    }),
    100361: _tools.RODict({
        "ID": 100361,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80431001, 0, 2], [80831001, 0, 2], [80231001, 0, 2]]),
        "props": None
    }),
    100362: _tools.RODict({
        "ID": 100362,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80431001, 1, 2], [80831001, 1, 2], [80231001, 1, 2]]),
        "props": None
    }),
    100363: _tools.RODict({
        "ID": 100363,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.002}),
        "equipment": _tools.ROList([[80431001, 2, 2], [80831001, 2, 2], [80231001, 2, 2]]),
        "props": None
    }),
    100364: _tools.RODict({
        "ID": 100364,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80431001, 3, 2], [80831001, 3, 2], [80231001, 3, 2]]),
        "props": None
    }),
    100365: _tools.RODict({
        "ID": 100365,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0035}),
        "equipment": _tools.ROList([[80431001, 4, 2], [80831001, 4, 2], [80231001, 4, 2]]),
        "props": None
    }),
    100366: _tools.RODict({
        "ID": 100366,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0045}),
        "equipment": _tools.ROList([[80431001, 5, 2], [80831001, 5, 2], [80231001, 5, 2]]),
        "props": None
    }),
    100367: _tools.RODict({
        "ID": 100367,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0055}),
        "equipment": _tools.ROList([[80431001, 6, 2], [80831001, 6, 2], [80231001, 6, 2]]),
        "props": None
    }),
    100368: _tools.RODict({
        "ID": 100368,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.008}),
        "equipment": _tools.ROList([[80431001, 7, 2], [80831001, 7, 2], [80231001, 7, 2]]),
        "props": None
    }),
    100369: _tools.RODict({
        "ID": 100369,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.002}),
        "equipment": _tools.ROList([[80431001, 0, 3], [80831001, 0, 3], [80231001, 0, 3]]),
        "props": None
    }),
    100370: _tools.RODict({
        "ID": 100370,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80431001, 1, 3], [80831001, 1, 3], [80231001, 1, 3]]),
        "props": None
    }),
    100371: _tools.RODict({
        "ID": 100371,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80431001, 2, 3], [80831001, 2, 3], [80231001, 2, 3]]),
        "props": None
    }),
    100372: _tools.RODict({
        "ID": 100372,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.003}),
        "equipment": _tools.ROList([[80431001, 3, 3], [80831001, 3, 3], [80231001, 3, 3]]),
        "props": None
    }),
    100373: _tools.RODict({
        "ID": 100373,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.004}),
        "equipment": _tools.ROList([[80431001, 4, 3], [80831001, 4, 3], [80231001, 4, 3]]),
        "props": None
    }),
    100374: _tools.RODict({
        "ID": 100374,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.005}),
        "equipment": _tools.ROList([[80431001, 5, 3], [80831001, 5, 3], [80231001, 5, 3]]),
        "props": None
    }),
    100375: _tools.RODict({
        "ID": 100375,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.006}),
        "equipment": _tools.ROList([[80431001, 6, 3], [80831001, 6, 3], [80231001, 6, 3]]),
        "props": None
    }),
    100376: _tools.RODict({
        "ID": 100376,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0085}),
        "equipment": _tools.ROList([[80431001, 7, 3], [80831001, 7, 3], [80231001, 7, 3]]),
        "props": None
    }),
    100377: _tools.RODict({
        "ID": 100377,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80431001, 0, 4], [80831001, 0, 4], [80231001, 0, 4]]),
        "props": None
    }),
    100378: _tools.RODict({
        "ID": 100378,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.003}),
        "equipment": _tools.ROList([[80431001, 1, 4], [80831001, 1, 4], [80231001, 1, 4]]),
        "props": None
    }),
    100379: _tools.RODict({
        "ID": 100379,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.003}),
        "equipment": _tools.ROList([[80431001, 2, 4], [80831001, 2, 4], [80231001, 2, 4]]),
        "props": None
    }),
    100380: _tools.RODict({
        "ID": 100380,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0035}),
        "equipment": _tools.ROList([[80431001, 3, 4], [80831001, 3, 4], [80231001, 3, 4]]),
        "props": None
    }),
    100381: _tools.RODict({
        "ID": 100381,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0045}),
        "equipment": _tools.ROList([[80431001, 4, 4], [80831001, 4, 4], [80231001, 4, 4]]),
        "props": None
    }),
    100382: _tools.RODict({
        "ID": 100382,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0055}),
        "equipment": _tools.ROList([[80431001, 5, 4], [80831001, 5, 4], [80231001, 5, 4]]),
        "props": None
    }),
    100383: _tools.RODict({
        "ID": 100383,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0065}),
        "equipment": _tools.ROList([[80431001, 6, 4], [80831001, 6, 4], [80231001, 6, 4]]),
        "props": None
    }),
    100384: _tools.RODict({
        "ID": 100384,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.009}),
        "equipment": _tools.ROList([[80431001, 7, 4], [80831001, 7, 4], [80231001, 7, 4]]),
        "props": None
    }),
    100385: _tools.RODict({
        "ID": 100385,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.001}),
        "equipment": _tools.ROList([[80811001, 0, 1], [80211001, 0, 1], [80311001, 0, 1]]),
        "props": None
    }),
    100386: _tools.RODict({
        "ID": 100386,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.001}),
        "equipment": _tools.ROList([[80811001, 1, 1], [80211001, 1, 1], [80311001, 1, 1]]),
        "props": None
    }),
    100387: _tools.RODict({
        "ID": 100387,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80811001, 2, 1], [80211001, 2, 1], [80311001, 2, 1]]),
        "props": None
    }),
    100388: _tools.RODict({
        "ID": 100388,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.002}),
        "equipment": _tools.ROList([[80811001, 3, 1], [80211001, 3, 1], [80311001, 3, 1]]),
        "props": None
    }),
    100389: _tools.RODict({
        "ID": 100389,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.003}),
        "equipment": _tools.ROList([[80811001, 4, 1], [80211001, 4, 1], [80311001, 4, 1]]),
        "props": None
    }),
    100390: _tools.RODict({
        "ID": 100390,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.004}),
        "equipment": _tools.ROList([[80811001, 5, 1], [80211001, 5, 1], [80311001, 5, 1]]),
        "props": None
    }),
    100391: _tools.RODict({
        "ID": 100391,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.005}),
        "equipment": _tools.ROList([[80811001, 6, 1], [80211001, 6, 1], [80311001, 6, 1]]),
        "props": None
    }),
    100392: _tools.RODict({
        "ID": 100392,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0075}),
        "equipment": _tools.ROList([[80811001, 7, 1], [80211001, 7, 1], [80311001, 7, 1]]),
        "props": None
    }),
    100393: _tools.RODict({
        "ID": 100393,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80811001, 0, 2], [80211001, 0, 2], [80311001, 0, 2]]),
        "props": None
    }),
    100394: _tools.RODict({
        "ID": 100394,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80811001, 1, 2], [80211001, 1, 2], [80311001, 1, 2]]),
        "props": None
    }),
    100395: _tools.RODict({
        "ID": 100395,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.002}),
        "equipment": _tools.ROList([[80811001, 2, 2], [80211001, 2, 2], [80311001, 2, 2]]),
        "props": None
    }),
    100396: _tools.RODict({
        "ID": 100396,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80811001, 3, 2], [80211001, 3, 2], [80311001, 3, 2]]),
        "props": None
    }),
    100397: _tools.RODict({
        "ID": 100397,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0035}),
        "equipment": _tools.ROList([[80811001, 4, 2], [80211001, 4, 2], [80311001, 4, 2]]),
        "props": None
    }),
    100398: _tools.RODict({
        "ID": 100398,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0045}),
        "equipment": _tools.ROList([[80811001, 5, 2], [80211001, 5, 2], [80311001, 5, 2]]),
        "props": None
    }),
    100399: _tools.RODict({
        "ID": 100399,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0055}),
        "equipment": _tools.ROList([[80811001, 6, 2], [80211001, 6, 2], [80311001, 6, 2]]),
        "props": None
    }),
    100400: _tools.RODict({
        "ID": 100400,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.008}),
        "equipment": _tools.ROList([[80811001, 7, 2], [80211001, 7, 2], [80311001, 7, 2]]),
        "props": None
    }),
    100401: _tools.RODict({
        "ID": 100401,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.002}),
        "equipment": _tools.ROList([[80811001, 0, 3], [80211001, 0, 3], [80311001, 0, 3]]),
        "props": None
    }),
    100402: _tools.RODict({
        "ID": 100402,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80811001, 1, 3], [80211001, 1, 3], [80311001, 1, 3]]),
        "props": None
    }),
    100403: _tools.RODict({
        "ID": 100403,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80811001, 2, 3], [80211001, 2, 3], [80311001, 2, 3]]),
        "props": None
    }),
    100404: _tools.RODict({
        "ID": 100404,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.003}),
        "equipment": _tools.ROList([[80811001, 3, 3], [80211001, 3, 3], [80311001, 3, 3]]),
        "props": None
    }),
    100405: _tools.RODict({
        "ID": 100405,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.004}),
        "equipment": _tools.ROList([[80811001, 4, 3], [80211001, 4, 3], [80311001, 4, 3]]),
        "props": None
    }),
    100406: _tools.RODict({
        "ID": 100406,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.005}),
        "equipment": _tools.ROList([[80811001, 5, 3], [80211001, 5, 3], [80311001, 5, 3]]),
        "props": None
    }),
    100407: _tools.RODict({
        "ID": 100407,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.006}),
        "equipment": _tools.ROList([[80811001, 6, 3], [80211001, 6, 3], [80311001, 6, 3]]),
        "props": None
    }),
    100408: _tools.RODict({
        "ID": 100408,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0085}),
        "equipment": _tools.ROList([[80811001, 7, 3], [80211001, 7, 3], [80311001, 7, 3]]),
        "props": None
    }),
    100409: _tools.RODict({
        "ID": 100409,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80811001, 0, 4], [80211001, 0, 4], [80311001, 0, 4]]),
        "props": None
    }),
    100410: _tools.RODict({
        "ID": 100410,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.003}),
        "equipment": _tools.ROList([[80811001, 1, 4], [80211001, 1, 4], [80311001, 1, 4]]),
        "props": None
    }),
    100411: _tools.RODict({
        "ID": 100411,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.003}),
        "equipment": _tools.ROList([[80811001, 2, 4], [80211001, 2, 4], [80311001, 2, 4]]),
        "props": None
    }),
    100412: _tools.RODict({
        "ID": 100412,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0035}),
        "equipment": _tools.ROList([[80811001, 3, 4], [80211001, 3, 4], [80311001, 3, 4]]),
        "props": None
    }),
    100413: _tools.RODict({
        "ID": 100413,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0045}),
        "equipment": _tools.ROList([[80811001, 4, 4], [80211001, 4, 4], [80311001, 4, 4]]),
        "props": None
    }),
    100414: _tools.RODict({
        "ID": 100414,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0055}),
        "equipment": _tools.ROList([[80811001, 5, 4], [80211001, 5, 4], [80311001, 5, 4]]),
        "props": None
    }),
    100415: _tools.RODict({
        "ID": 100415,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0065}),
        "equipment": _tools.ROList([[80811001, 6, 4], [80211001, 6, 4], [80311001, 6, 4]]),
        "props": None
    }),
    100416: _tools.RODict({
        "ID": 100416,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.009}),
        "equipment": _tools.ROList([[80811001, 7, 4], [80211001, 7, 4], [80311001, 7, 4]]),
        "props": None
    }),
    100417: _tools.RODict({
        "ID": 100417,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.001}),
        "equipment": _tools.ROList([[80821001, 0, 1], [80221001, 0, 1], [80321001, 0, 1]]),
        "props": None
    }),
    100418: _tools.RODict({
        "ID": 100418,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.001}),
        "equipment": _tools.ROList([[80821001, 1, 1], [80221001, 1, 1], [80321001, 1, 1]]),
        "props": None
    }),
    100419: _tools.RODict({
        "ID": 100419,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80821001, 2, 1], [80221001, 2, 1], [80321001, 2, 1]]),
        "props": None
    }),
    100420: _tools.RODict({
        "ID": 100420,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.002}),
        "equipment": _tools.ROList([[80821001, 3, 1], [80221001, 3, 1], [80321001, 3, 1]]),
        "props": None
    }),
    100421: _tools.RODict({
        "ID": 100421,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.003}),
        "equipment": _tools.ROList([[80821001, 4, 1], [80221001, 4, 1], [80321001, 4, 1]]),
        "props": None
    }),
    100422: _tools.RODict({
        "ID": 100422,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.004}),
        "equipment": _tools.ROList([[80821001, 5, 1], [80221001, 5, 1], [80321001, 5, 1]]),
        "props": None
    }),
    100423: _tools.RODict({
        "ID": 100423,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.005}),
        "equipment": _tools.ROList([[80821001, 6, 1], [80221001, 6, 1], [80321001, 6, 1]]),
        "props": None
    }),
    100424: _tools.RODict({
        "ID": 100424,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0075}),
        "equipment": _tools.ROList([[80821001, 7, 1], [80221001, 7, 1], [80321001, 7, 1]]),
        "props": None
    }),
    100425: _tools.RODict({
        "ID": 100425,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80821001, 0, 2], [80221001, 0, 2], [80321001, 0, 2]]),
        "props": None
    }),
    100426: _tools.RODict({
        "ID": 100426,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80821001, 1, 2], [80221001, 1, 2], [80321001, 1, 2]]),
        "props": None
    }),
    100427: _tools.RODict({
        "ID": 100427,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.002}),
        "equipment": _tools.ROList([[80821001, 2, 2], [80221001, 2, 2], [80321001, 2, 2]]),
        "props": None
    }),
    100428: _tools.RODict({
        "ID": 100428,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80821001, 3, 2], [80221001, 3, 2], [80321001, 3, 2]]),
        "props": None
    }),
    100429: _tools.RODict({
        "ID": 100429,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0035}),
        "equipment": _tools.ROList([[80821001, 4, 2], [80221001, 4, 2], [80321001, 4, 2]]),
        "props": None
    }),
    100430: _tools.RODict({
        "ID": 100430,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0045}),
        "equipment": _tools.ROList([[80821001, 5, 2], [80221001, 5, 2], [80321001, 5, 2]]),
        "props": None
    }),
    100431: _tools.RODict({
        "ID": 100431,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0055}),
        "equipment": _tools.ROList([[80821001, 6, 2], [80221001, 6, 2], [80321001, 6, 2]]),
        "props": None
    }),
    100432: _tools.RODict({
        "ID": 100432,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.008}),
        "equipment": _tools.ROList([[80821001, 7, 2], [80221001, 7, 2], [80321001, 7, 2]]),
        "props": None
    }),
    100433: _tools.RODict({
        "ID": 100433,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.002}),
        "equipment": _tools.ROList([[80821001, 0, 3], [80221001, 0, 3], [80321001, 0, 3]]),
        "props": None
    }),
    100434: _tools.RODict({
        "ID": 100434,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80821001, 1, 3], [80221001, 1, 3], [80321001, 1, 3]]),
        "props": None
    }),
    100435: _tools.RODict({
        "ID": 100435,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80821001, 2, 3], [80221001, 2, 3], [80321001, 2, 3]]),
        "props": None
    }),
    100436: _tools.RODict({
        "ID": 100436,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.003}),
        "equipment": _tools.ROList([[80821001, 3, 3], [80221001, 3, 3], [80321001, 3, 3]]),
        "props": None
    }),
    100437: _tools.RODict({
        "ID": 100437,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.004}),
        "equipment": _tools.ROList([[80821001, 4, 3], [80221001, 4, 3], [80321001, 4, 3]]),
        "props": None
    }),
    100438: _tools.RODict({
        "ID": 100438,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.005}),
        "equipment": _tools.ROList([[80821001, 5, 3], [80221001, 5, 3], [80321001, 5, 3]]),
        "props": None
    }),
    100439: _tools.RODict({
        "ID": 100439,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.006}),
        "equipment": _tools.ROList([[80821001, 6, 3], [80221001, 6, 3], [80321001, 6, 3]]),
        "props": None
    }),
    100440: _tools.RODict({
        "ID": 100440,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0085}),
        "equipment": _tools.ROList([[80821001, 7, 3], [80221001, 7, 3], [80321001, 7, 3]]),
        "props": None
    }),
    100441: _tools.RODict({
        "ID": 100441,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80821001, 0, 4], [80221001, 0, 4], [80321001, 0, 4]]),
        "props": None
    }),
    100442: _tools.RODict({
        "ID": 100442,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.003}),
        "equipment": _tools.ROList([[80821001, 1, 4], [80221001, 1, 4], [80321001, 1, 4]]),
        "props": None
    }),
    100443: _tools.RODict({
        "ID": 100443,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.003}),
        "equipment": _tools.ROList([[80821001, 2, 4], [80221001, 2, 4], [80321001, 2, 4]]),
        "props": None
    }),
    100444: _tools.RODict({
        "ID": 100444,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0035}),
        "equipment": _tools.ROList([[80821001, 3, 4], [80221001, 3, 4], [80321001, 3, 4]]),
        "props": None
    }),
    100445: _tools.RODict({
        "ID": 100445,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0045}),
        "equipment": _tools.ROList([[80821001, 4, 4], [80221001, 4, 4], [80321001, 4, 4]]),
        "props": None
    }),
    100446: _tools.RODict({
        "ID": 100446,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0055}),
        "equipment": _tools.ROList([[80821001, 5, 4], [80221001, 5, 4], [80321001, 5, 4]]),
        "props": None
    }),
    100447: _tools.RODict({
        "ID": 100447,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0065}),
        "equipment": _tools.ROList([[80821001, 6, 4], [80221001, 6, 4], [80321001, 6, 4]]),
        "props": None
    }),
    100448: _tools.RODict({
        "ID": 100448,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.009}),
        "equipment": _tools.ROList([[80821001, 7, 4], [80221001, 7, 4], [80321001, 7, 4]]),
        "props": None
    }),
    100449: _tools.RODict({
        "ID": 100449,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.001}),
        "equipment": _tools.ROList([[80831001, 0, 1], [80231001, 0, 1], [80331001, 0, 1]]),
        "props": None
    }),
    100450: _tools.RODict({
        "ID": 100450,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.001}),
        "equipment": _tools.ROList([[80831001, 1, 1], [80231001, 1, 1], [80331001, 1, 1]]),
        "props": None
    }),
    100451: _tools.RODict({
        "ID": 100451,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80831001, 2, 1], [80231001, 2, 1], [80331001, 2, 1]]),
        "props": None
    }),
    100452: _tools.RODict({
        "ID": 100452,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.002}),
        "equipment": _tools.ROList([[80831001, 3, 1], [80231001, 3, 1], [80331001, 3, 1]]),
        "props": None
    }),
    100453: _tools.RODict({
        "ID": 100453,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.003}),
        "equipment": _tools.ROList([[80831001, 4, 1], [80231001, 4, 1], [80331001, 4, 1]]),
        "props": None
    }),
    100454: _tools.RODict({
        "ID": 100454,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.004}),
        "equipment": _tools.ROList([[80831001, 5, 1], [80231001, 5, 1], [80331001, 5, 1]]),
        "props": None
    }),
    100455: _tools.RODict({
        "ID": 100455,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.005}),
        "equipment": _tools.ROList([[80831001, 6, 1], [80231001, 6, 1], [80331001, 6, 1]]),
        "props": None
    }),
    100456: _tools.RODict({
        "ID": 100456,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0075}),
        "equipment": _tools.ROList([[80831001, 7, 1], [80231001, 7, 1], [80331001, 7, 1]]),
        "props": None
    }),
    100457: _tools.RODict({
        "ID": 100457,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80831001, 0, 2], [80231001, 0, 2], [80331001, 0, 2]]),
        "props": None
    }),
    100458: _tools.RODict({
        "ID": 100458,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80831001, 1, 2], [80231001, 1, 2], [80331001, 1, 2]]),
        "props": None
    }),
    100459: _tools.RODict({
        "ID": 100459,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.002}),
        "equipment": _tools.ROList([[80831001, 2, 2], [80231001, 2, 2], [80331001, 2, 2]]),
        "props": None
    }),
    100460: _tools.RODict({
        "ID": 100460,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80831001, 3, 2], [80231001, 3, 2], [80331001, 3, 2]]),
        "props": None
    }),
    100461: _tools.RODict({
        "ID": 100461,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0035}),
        "equipment": _tools.ROList([[80831001, 4, 2], [80231001, 4, 2], [80331001, 4, 2]]),
        "props": None
    }),
    100462: _tools.RODict({
        "ID": 100462,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0045}),
        "equipment": _tools.ROList([[80831001, 5, 2], [80231001, 5, 2], [80331001, 5, 2]]),
        "props": None
    }),
    100463: _tools.RODict({
        "ID": 100463,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0055}),
        "equipment": _tools.ROList([[80831001, 6, 2], [80231001, 6, 2], [80331001, 6, 2]]),
        "props": None
    }),
    100464: _tools.RODict({
        "ID": 100464,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.008}),
        "equipment": _tools.ROList([[80831001, 7, 2], [80231001, 7, 2], [80331001, 7, 2]]),
        "props": None
    }),
    100465: _tools.RODict({
        "ID": 100465,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.002}),
        "equipment": _tools.ROList([[80831001, 0, 3], [80231001, 0, 3], [80331001, 0, 3]]),
        "props": None
    }),
    100466: _tools.RODict({
        "ID": 100466,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80831001, 1, 3], [80231001, 1, 3], [80331001, 1, 3]]),
        "props": None
    }),
    100467: _tools.RODict({
        "ID": 100467,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80831001, 2, 3], [80231001, 2, 3], [80331001, 2, 3]]),
        "props": None
    }),
    100468: _tools.RODict({
        "ID": 100468,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.003}),
        "equipment": _tools.ROList([[80831001, 3, 3], [80231001, 3, 3], [80331001, 3, 3]]),
        "props": None
    }),
    100469: _tools.RODict({
        "ID": 100469,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.004}),
        "equipment": _tools.ROList([[80831001, 4, 3], [80231001, 4, 3], [80331001, 4, 3]]),
        "props": None
    }),
    100470: _tools.RODict({
        "ID": 100470,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.005}),
        "equipment": _tools.ROList([[80831001, 5, 3], [80231001, 5, 3], [80331001, 5, 3]]),
        "props": None
    }),
    100471: _tools.RODict({
        "ID": 100471,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.006}),
        "equipment": _tools.ROList([[80831001, 6, 3], [80231001, 6, 3], [80331001, 6, 3]]),
        "props": None
    }),
    100472: _tools.RODict({
        "ID": 100472,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0085}),
        "equipment": _tools.ROList([[80831001, 7, 3], [80231001, 7, 3], [80331001, 7, 3]]),
        "props": None
    }),
    100473: _tools.RODict({
        "ID": 100473,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80831001, 0, 4], [80231001, 0, 4], [80331001, 0, 4]]),
        "props": None
    }),
    100474: _tools.RODict({
        "ID": 100474,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.003}),
        "equipment": _tools.ROList([[80831001, 1, 4], [80231001, 1, 4], [80331001, 1, 4]]),
        "props": None
    }),
    100475: _tools.RODict({
        "ID": 100475,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.003}),
        "equipment": _tools.ROList([[80831001, 2, 4], [80231001, 2, 4], [80331001, 2, 4]]),
        "props": None
    }),
    100476: _tools.RODict({
        "ID": 100476,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0035}),
        "equipment": _tools.ROList([[80831001, 3, 4], [80231001, 3, 4], [80331001, 3, 4]]),
        "props": None
    }),
    100477: _tools.RODict({
        "ID": 100477,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0045}),
        "equipment": _tools.ROList([[80831001, 4, 4], [80231001, 4, 4], [80331001, 4, 4]]),
        "props": None
    }),
    100478: _tools.RODict({
        "ID": 100478,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0055}),
        "equipment": _tools.ROList([[80831001, 5, 4], [80231001, 5, 4], [80331001, 5, 4]]),
        "props": None
    }),
    100479: _tools.RODict({
        "ID": 100479,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0065}),
        "equipment": _tools.ROList([[80831001, 6, 4], [80231001, 6, 4], [80331001, 6, 4]]),
        "props": None
    }),
    100480: _tools.RODict({
        "ID": 100480,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.009}),
        "equipment": _tools.ROList([[80831001, 7, 4], [80231001, 7, 4], [80331001, 7, 4]]),
        "props": None
    }),
    100481: _tools.RODict({
        "ID": 100481,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.001}),
        "equipment": _tools.ROList([[80691001, 0, 1], [80591001, 0, 1]]),
        "props": None
    }),
    100482: _tools.RODict({
        "ID": 100482,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.001}),
        "equipment": _tools.ROList([[80691001, 1, 1], [80591001, 1, 1]]),
        "props": None
    }),
    100483: _tools.RODict({
        "ID": 100483,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0015}),
        "equipment": _tools.ROList([[80691001, 2, 1], [80591001, 2, 1]]),
        "props": None
    }),
    100484: _tools.RODict({
        "ID": 100484,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.002}),
        "equipment": _tools.ROList([[80691001, 3, 1], [80591001, 3, 1]]),
        "props": None
    }),
    100485: _tools.RODict({
        "ID": 100485,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.003}),
        "equipment": _tools.ROList([[80691001, 4, 1], [80591001, 4, 1]]),
        "props": None
    }),
    100486: _tools.RODict({
        "ID": 100486,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.004}),
        "equipment": _tools.ROList([[80691001, 5, 1], [80591001, 5, 1]]),
        "props": None
    }),
    100487: _tools.RODict({
        "ID": 100487,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.005}),
        "equipment": _tools.ROList([[80691001, 6, 1], [80591001, 6, 1]]),
        "props": None
    }),
    100488: _tools.RODict({
        "ID": 100488,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0075}),
        "equipment": _tools.ROList([[80691001, 7, 1], [80591001, 7, 1]]),
        "props": None
    }),
    100489: _tools.RODict({
        "ID": 100489,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0015}),
        "equipment": _tools.ROList([[80691001, 0, 2], [80591001, 0, 2]]),
        "props": None
    }),
    100490: _tools.RODict({
        "ID": 100490,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0015}),
        "equipment": _tools.ROList([[80691001, 1, 2], [80591001, 1, 2]]),
        "props": None
    }),
    100491: _tools.RODict({
        "ID": 100491,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.002}),
        "equipment": _tools.ROList([[80691001, 2, 2], [80591001, 2, 2]]),
        "props": None
    }),
    100492: _tools.RODict({
        "ID": 100492,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0025}),
        "equipment": _tools.ROList([[80691001, 3, 2], [80591001, 3, 2]]),
        "props": None
    }),
    100493: _tools.RODict({
        "ID": 100493,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0035}),
        "equipment": _tools.ROList([[80691001, 4, 2], [80591001, 4, 2]]),
        "props": None
    }),
    100494: _tools.RODict({
        "ID": 100494,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0045}),
        "equipment": _tools.ROList([[80691001, 5, 2], [80591001, 5, 2]]),
        "props": None
    }),
    100495: _tools.RODict({
        "ID": 100495,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0055}),
        "equipment": _tools.ROList([[80691001, 6, 2], [80591001, 6, 2]]),
        "props": None
    }),
    100496: _tools.RODict({
        "ID": 100496,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.008}),
        "equipment": _tools.ROList([[80691001, 7, 2], [80591001, 7, 2]]),
        "props": None
    }),
    100497: _tools.RODict({
        "ID": 100497,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.002}),
        "equipment": _tools.ROList([[80691001, 0, 3], [80591001, 0, 3]]),
        "props": None
    }),
    100498: _tools.RODict({
        "ID": 100498,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0025}),
        "equipment": _tools.ROList([[80691001, 1, 3], [80591001, 1, 3]]),
        "props": None
    }),
    100499: _tools.RODict({
        "ID": 100499,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0025}),
        "equipment": _tools.ROList([[80691001, 2, 3], [80591001, 2, 3]]),
        "props": None
    }),
    100500: _tools.RODict({
        "ID": 100500,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.003}),
        "equipment": _tools.ROList([[80691001, 3, 3], [80591001, 3, 3]]),
        "props": None
    }),
    100501: _tools.RODict({
        "ID": 100501,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.004}),
        "equipment": _tools.ROList([[80691001, 4, 3], [80591001, 4, 3]]),
        "props": None
    }),
    100502: _tools.RODict({
        "ID": 100502,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.005}),
        "equipment": _tools.ROList([[80691001, 5, 3], [80591001, 5, 3]]),
        "props": None
    }),
    100503: _tools.RODict({
        "ID": 100503,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.006}),
        "equipment": _tools.ROList([[80691001, 6, 3], [80591001, 6, 3]]),
        "props": None
    }),
    100504: _tools.RODict({
        "ID": 100504,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0085}),
        "equipment": _tools.ROList([[80691001, 7, 3], [80591001, 7, 3]]),
        "props": None
    }),
    100505: _tools.RODict({
        "ID": 100505,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0025}),
        "equipment": _tools.ROList([[80691001, 0, 4], [80591001, 0, 4]]),
        "props": None
    }),
    100506: _tools.RODict({
        "ID": 100506,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.003}),
        "equipment": _tools.ROList([[80691001, 1, 4], [80591001, 1, 4]]),
        "props": None
    }),
    100507: _tools.RODict({
        "ID": 100507,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.003}),
        "equipment": _tools.ROList([[80691001, 2, 4], [80591001, 2, 4]]),
        "props": None
    }),
    100508: _tools.RODict({
        "ID": 100508,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0035}),
        "equipment": _tools.ROList([[80691001, 3, 4], [80591001, 3, 4]]),
        "props": None
    }),
    100509: _tools.RODict({
        "ID": 100509,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0045}),
        "equipment": _tools.ROList([[80691001, 4, 4], [80591001, 4, 4]]),
        "props": None
    }),
    100510: _tools.RODict({
        "ID": 100510,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0055}),
        "equipment": _tools.ROList([[80691001, 5, 4], [80591001, 5, 4]]),
        "props": None
    }),
    100511: _tools.RODict({
        "ID": 100511,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0065}),
        "equipment": _tools.ROList([[80691001, 6, 4], [80591001, 6, 4]]),
        "props": None
    }),
    100512: _tools.RODict({
        "ID": 100512,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.009}),
        "equipment": _tools.ROList([[80691001, 7, 4], [80591001, 7, 4]]),
        "props": None
    }),
    100513: _tools.RODict({
        "ID": 100513,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.001}),
        "equipment": _tools.ROList([[80581001, 0, 1], [80681001, 0, 1]]),
        "props": None
    }),
    100514: _tools.RODict({
        "ID": 100514,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.001}),
        "equipment": _tools.ROList([[80581001, 1, 1], [80681001, 1, 1]]),
        "props": None
    }),
    100515: _tools.RODict({
        "ID": 100515,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0015}),
        "equipment": _tools.ROList([[80581001, 2, 1], [80681001, 2, 1]]),
        "props": None
    }),
    100516: _tools.RODict({
        "ID": 100516,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.002}),
        "equipment": _tools.ROList([[80581001, 3, 1], [80681001, 3, 1]]),
        "props": None
    }),
    100517: _tools.RODict({
        "ID": 100517,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.003}),
        "equipment": _tools.ROList([[80581001, 4, 1], [80681001, 4, 1]]),
        "props": None
    }),
    100518: _tools.RODict({
        "ID": 100518,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.004}),
        "equipment": _tools.ROList([[80581001, 5, 1], [80681001, 5, 1]]),
        "props": None
    }),
    100519: _tools.RODict({
        "ID": 100519,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.005}),
        "equipment": _tools.ROList([[80581001, 6, 1], [80681001, 6, 1]]),
        "props": None
    }),
    100520: _tools.RODict({
        "ID": 100520,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0075}),
        "equipment": _tools.ROList([[80581001, 7, 1], [80681001, 7, 1]]),
        "props": None
    }),
    100521: _tools.RODict({
        "ID": 100521,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0015}),
        "equipment": _tools.ROList([[80581001, 0, 2], [80681001, 0, 2]]),
        "props": None
    }),
    100522: _tools.RODict({
        "ID": 100522,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0015}),
        "equipment": _tools.ROList([[80581001, 1, 2], [80681001, 1, 2]]),
        "props": None
    }),
    100523: _tools.RODict({
        "ID": 100523,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.002}),
        "equipment": _tools.ROList([[80581001, 2, 2], [80681001, 2, 2]]),
        "props": None
    }),
    100524: _tools.RODict({
        "ID": 100524,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0025}),
        "equipment": _tools.ROList([[80581001, 3, 2], [80681001, 3, 2]]),
        "props": None
    }),
    100525: _tools.RODict({
        "ID": 100525,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0035}),
        "equipment": _tools.ROList([[80581001, 4, 2], [80681001, 4, 2]]),
        "props": None
    }),
    100526: _tools.RODict({
        "ID": 100526,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0045}),
        "equipment": _tools.ROList([[80581001, 5, 2], [80681001, 5, 2]]),
        "props": None
    }),
    100527: _tools.RODict({
        "ID": 100527,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0055}),
        "equipment": _tools.ROList([[80581001, 6, 2], [80681001, 6, 2]]),
        "props": None
    }),
    100528: _tools.RODict({
        "ID": 100528,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.008}),
        "equipment": _tools.ROList([[80581001, 7, 2], [80681001, 7, 2]]),
        "props": None
    }),
    100529: _tools.RODict({
        "ID": 100529,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.002}),
        "equipment": _tools.ROList([[80581001, 0, 3], [80681001, 0, 3]]),
        "props": None
    }),
    100530: _tools.RODict({
        "ID": 100530,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0025}),
        "equipment": _tools.ROList([[80581001, 1, 3], [80681001, 1, 3]]),
        "props": None
    }),
    100531: _tools.RODict({
        "ID": 100531,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0025}),
        "equipment": _tools.ROList([[80581001, 2, 3], [80681001, 2, 3]]),
        "props": None
    }),
    100532: _tools.RODict({
        "ID": 100532,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.003}),
        "equipment": _tools.ROList([[80581001, 3, 3], [80681001, 3, 3]]),
        "props": None
    }),
    100533: _tools.RODict({
        "ID": 100533,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.004}),
        "equipment": _tools.ROList([[80581001, 4, 3], [80681001, 4, 3]]),
        "props": None
    }),
    100534: _tools.RODict({
        "ID": 100534,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.005}),
        "equipment": _tools.ROList([[80581001, 5, 3], [80681001, 5, 3]]),
        "props": None
    }),
    100535: _tools.RODict({
        "ID": 100535,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.006}),
        "equipment": _tools.ROList([[80581001, 6, 3], [80681001, 6, 3]]),
        "props": None
    }),
    100536: _tools.RODict({
        "ID": 100536,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0085}),
        "equipment": _tools.ROList([[80581001, 7, 3], [80681001, 7, 3]]),
        "props": None
    }),
    100537: _tools.RODict({
        "ID": 100537,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0025}),
        "equipment": _tools.ROList([[80581001, 0, 4], [80681001, 0, 4]]),
        "props": None
    }),
    100538: _tools.RODict({
        "ID": 100538,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.003}),
        "equipment": _tools.ROList([[80581001, 1, 4], [80681001, 1, 4]]),
        "props": None
    }),
    100539: _tools.RODict({
        "ID": 100539,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.003}),
        "equipment": _tools.ROList([[80581001, 2, 4], [80681001, 2, 4]]),
        "props": None
    }),
    100540: _tools.RODict({
        "ID": 100540,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0035}),
        "equipment": _tools.ROList([[80581001, 3, 4], [80681001, 3, 4]]),
        "props": None
    }),
    100541: _tools.RODict({
        "ID": 100541,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0045}),
        "equipment": _tools.ROList([[80581001, 4, 4], [80681001, 4, 4]]),
        "props": None
    }),
    100542: _tools.RODict({
        "ID": 100542,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0055}),
        "equipment": _tools.ROList([[80581001, 5, 4], [80681001, 5, 4]]),
        "props": None
    }),
    100543: _tools.RODict({
        "ID": 100543,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0065}),
        "equipment": _tools.ROList([[80581001, 6, 4], [80681001, 6, 4]]),
        "props": None
    }),
    100544: _tools.RODict({
        "ID": 100544,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.009}),
        "equipment": _tools.ROList([[80581001, 7, 4], [80681001, 7, 4]]),
        "props": None
    }),
    100545: _tools.RODict({
        "ID": 100545,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80681001, 0, 1], [80781001, 0, 1]]),
        "props": None
    }),
    100546: _tools.RODict({
        "ID": 100546,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80681001, 1, 1], [80781001, 1, 1]]),
        "props": None
    }),
    100547: _tools.RODict({
        "ID": 100547,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenEnh":2}),
        "equipment": _tools.ROList([[80681001, 2, 1], [80781001, 2, 1]]),
        "props": None
    }),
    100548: _tools.RODict({
        "ID": 100548,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowEnh":2}),
        "equipment": _tools.ROList([[80681001, 3, 1], [80781001, 3, 1]]),
        "props": None
    }),
    100549: _tools.RODict({
        "ID": 100549,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushEnh":3}),
        "equipment": _tools.ROList([[80681001, 4, 1], [80781001, 4, 1]]),
        "props": None
    }),
    100550: _tools.RODict({
        "ID": 100550,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockEnh":4}),
        "equipment": _tools.ROList([[80681001, 5, 1], [80781001, 5, 1]]),
        "props": None
    }),
    100551: _tools.RODict({
        "ID": 100551,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80681001, 3, 1], [80781001, 3, 1]]),
        "props": None
    }),
    100552: _tools.RODict({
        "ID": 100552,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80681001, 4, 1], [80781001, 4, 1]]),
        "props": None
    }),
    100553: _tools.RODict({
        "ID": 100553,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockEnh":2}),
        "equipment": _tools.ROList([[80681001, 0, 2], [80781001, 0, 2]]),
        "props": None
    }),
    100554: _tools.RODict({
        "ID": 100554,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushEnh":2}),
        "equipment": _tools.ROList([[80681001, 1, 2], [80781001, 1, 2]]),
        "props": None
    }),
    100555: _tools.RODict({
        "ID": 100555,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowEnh":3}),
        "equipment": _tools.ROList([[80681001, 2, 2], [80781001, 2, 2]]),
        "props": None
    }),
    100556: _tools.RODict({
        "ID": 100556,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenEnh":3}),
        "equipment": _tools.ROList([[80681001, 3, 2], [80781001, 3, 2]]),
        "props": None
    }),
    100557: _tools.RODict({
        "ID": 100557,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentEnh":4}),
        "equipment": _tools.ROList([[80681001, 4, 2], [80781001, 4, 2]]),
        "props": None
    }),
    100558: _tools.RODict({
        "ID": 100558,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunEnh":5}),
        "equipment": _tools.ROList([[80681001, 5, 2], [80781001, 5, 2]]),
        "props": None
    }),
    100559: _tools.RODict({
        "ID": 100559,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80681001, 3, 2], [80781001, 3, 2]]),
        "props": None
    }),
    100560: _tools.RODict({
        "ID": 100560,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80681001, 4, 2], [80781001, 4, 2]]),
        "props": None
    }),
    100561: _tools.RODict({
        "ID": 100561,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunEnh":2}),
        "equipment": _tools.ROList([[80681001, 0, 3], [80781001, 0, 3]]),
        "props": None
    }),
    100562: _tools.RODict({
        "ID": 100562,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentEnh":4}),
        "equipment": _tools.ROList([[80681001, 1, 3], [80781001, 1, 3]]),
        "props": None
    }),
    100563: _tools.RODict({
        "ID": 100563,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenEnh":5}),
        "equipment": _tools.ROList([[80681001, 2, 3], [80781001, 2, 3]]),
        "props": None
    }),
    100564: _tools.RODict({
        "ID": 100564,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowEnh":5}),
        "equipment": _tools.ROList([[80681001, 3, 3], [80781001, 3, 3]]),
        "props": None
    }),
    100565: _tools.RODict({
        "ID": 100565,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushEnh":6}),
        "equipment": _tools.ROList([[80681001, 4, 3], [80781001, 4, 3]]),
        "props": None
    }),
    100566: _tools.RODict({
        "ID": 100566,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockEnh":6}),
        "equipment": _tools.ROList([[80681001, 5, 3], [80781001, 5, 3]]),
        "props": None
    }),
    100567: _tools.RODict({
        "ID": 100567,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80681001, 4, 3], [80781001, 4, 3]]),
        "props": None
    }),
    100568: _tools.RODict({
        "ID": 100568,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80681001, 5, 3], [80781001, 5, 3]]),
        "props": None
    }),
    100569: _tools.RODict({
        "ID": 100569,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockEnh":3}),
        "equipment": _tools.ROList([[80681001, 0, 4], [80781001, 0, 4]]),
        "props": None
    }),
    100570: _tools.RODict({
        "ID": 100570,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushEnh":4}),
        "equipment": _tools.ROList([[80681001, 1, 4], [80781001, 1, 4]]),
        "props": None
    }),
    100571: _tools.RODict({
        "ID": 100571,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowEnh":5}),
        "equipment": _tools.ROList([[80681001, 2, 4], [80781001, 2, 4]]),
        "props": None
    }),
    100572: _tools.RODict({
        "ID": 100572,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenEnh":5}),
        "equipment": _tools.ROList([[80681001, 3, 4], [80781001, 3, 4]]),
        "props": None
    }),
    100573: _tools.RODict({
        "ID": 100573,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentEnh":6}),
        "equipment": _tools.ROList([[80681001, 4, 4], [80781001, 4, 4]]),
        "props": None
    }),
    100574: _tools.RODict({
        "ID": 100574,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunEnh":7}),
        "equipment": _tools.ROList([[80681001, 5, 4], [80781001, 5, 4]]),
        "props": None
    }),
    100575: _tools.RODict({
        "ID": 100575,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80681001, 5, 4], [80781001, 5, 4]]),
        "props": None
    }),
    100576: _tools.RODict({
        "ID": 100576,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80681001, 6, 4], [80781001, 6, 4]]),
        "props": None
    }),
    100577: _tools.RODict({
        "ID": 100577,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80791001, 0, 1], [80691001, 0, 1]]),
        "props": None
    }),
    100578: _tools.RODict({
        "ID": 100578,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80791001, 1, 1], [80691001, 1, 1]]),
        "props": None
    }),
    100579: _tools.RODict({
        "ID": 100579,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjFrozenEnh":2}),
        "equipment": _tools.ROList([[80791001, 2, 1], [80691001, 2, 1]]),
        "props": None
    }),
    100580: _tools.RODict({
        "ID": 100580,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjSlowEnh":2}),
        "equipment": _tools.ROList([[80791001, 3, 1], [80691001, 3, 1]]),
        "props": None
    }),
    100581: _tools.RODict({
        "ID": 100581,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjPushEnh":3}),
        "equipment": _tools.ROList([[80791001, 4, 1], [80691001, 4, 1]]),
        "props": None
    }),
    100582: _tools.RODict({
        "ID": 100582,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjKnockEnh":4}),
        "equipment": _tools.ROList([[80791001, 5, 1], [80691001, 5, 1]]),
        "props": None
    }),
    100583: _tools.RODict({
        "ID": 100583,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80791001, 3, 1], [80691001, 3, 1]]),
        "props": None
    }),
    100584: _tools.RODict({
        "ID": 100584,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80791001, 4, 1], [80691001, 4, 1]]),
        "props": None
    }),
    100585: _tools.RODict({
        "ID": 100585,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjKnockEnh":2}),
        "equipment": _tools.ROList([[80791001, 0, 2], [80691001, 0, 2]]),
        "props": None
    }),
    100586: _tools.RODict({
        "ID": 100586,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjPushEnh":2}),
        "equipment": _tools.ROList([[80791001, 1, 2], [80691001, 1, 2]]),
        "props": None
    }),
    100587: _tools.RODict({
        "ID": 100587,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjSlowEnh":3}),
        "equipment": _tools.ROList([[80791001, 2, 2], [80691001, 2, 2]]),
        "props": None
    }),
    100588: _tools.RODict({
        "ID": 100588,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjFrozenEnh":3}),
        "equipment": _tools.ROList([[80791001, 3, 2], [80691001, 3, 2]]),
        "props": None
    }),
    100589: _tools.RODict({
        "ID": 100589,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjSilentEnh":4}),
        "equipment": _tools.ROList([[80791001, 4, 2], [80691001, 4, 2]]),
        "props": None
    }),
    100590: _tools.RODict({
        "ID": 100590,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjStunEnh":5}),
        "equipment": _tools.ROList([[80791001, 5, 2], [80691001, 5, 2]]),
        "props": None
    }),
    100591: _tools.RODict({
        "ID": 100591,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80791001, 3, 2], [80691001, 3, 2]]),
        "props": None
    }),
    100592: _tools.RODict({
        "ID": 100592,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80791001, 4, 2], [80691001, 4, 2]]),
        "props": None
    }),
    100593: _tools.RODict({
        "ID": 100593,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjStunEnh":2}),
        "equipment": _tools.ROList([[80791001, 0, 3], [80691001, 0, 3]]),
        "props": None
    }),
    100594: _tools.RODict({
        "ID": 100594,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjSilentEnh":4}),
        "equipment": _tools.ROList([[80791001, 1, 3], [80691001, 1, 3]]),
        "props": None
    }),
    100595: _tools.RODict({
        "ID": 100595,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjFrozenEnh":5}),
        "equipment": _tools.ROList([[80791001, 2, 3], [80691001, 2, 3]]),
        "props": None
    }),
    100596: _tools.RODict({
        "ID": 100596,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjSlowEnh":5}),
        "equipment": _tools.ROList([[80791001, 3, 3], [80691001, 3, 3]]),
        "props": None
    }),
    100597: _tools.RODict({
        "ID": 100597,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjPushEnh":6}),
        "equipment": _tools.ROList([[80791001, 4, 3], [80691001, 4, 3]]),
        "props": None
    }),
    100598: _tools.RODict({
        "ID": 100598,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjKnockEnh":6}),
        "equipment": _tools.ROList([[80791001, 5, 3], [80691001, 5, 3]]),
        "props": None
    }),
    100599: _tools.RODict({
        "ID": 100599,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80791001, 4, 3], [80691001, 4, 3]]),
        "props": None
    }),
    100600: _tools.RODict({
        "ID": 100600,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80791001, 5, 3], [80691001, 5, 3]]),
        "props": None
    }),
    100601: _tools.RODict({
        "ID": 100601,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjKnockEnh":3}),
        "equipment": _tools.ROList([[80791001, 0, 4], [80691001, 0, 4]]),
        "props": None
    }),
    100602: _tools.RODict({
        "ID": 100602,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjPushEnh":4}),
        "equipment": _tools.ROList([[80791001, 1, 4], [80691001, 1, 4]]),
        "props": None
    }),
    100603: _tools.RODict({
        "ID": 100603,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjSlowEnh":5}),
        "equipment": _tools.ROList([[80791001, 2, 4], [80691001, 2, 4]]),
        "props": None
    }),
    100604: _tools.RODict({
        "ID": 100604,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjFrozenEnh":5}),
        "equipment": _tools.ROList([[80791001, 3, 4], [80691001, 3, 4]]),
        "props": None
    }),
    100605: _tools.RODict({
        "ID": 100605,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjSilentEnh":6}),
        "equipment": _tools.ROList([[80791001, 4, 4], [80691001, 4, 4]]),
        "props": None
    }),
    100606: _tools.RODict({
        "ID": 100606,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjStunEnh":7}),
        "equipment": _tools.ROList([[80791001, 5, 4], [80691001, 5, 4]]),
        "props": None
    }),
    100607: _tools.RODict({
        "ID": 100607,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80791001, 5, 4], [80691001, 5, 4]]),
        "props": None
    }),
    100608: _tools.RODict({
        "ID": 100608,
        "unavailableClass": _tools.ROList([1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80791001, 6, 4], [80691001, 6, 4]]),
        "props": None
    }),
    100609: _tools.RODict({
        "ID": 100609,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80781001, 0, 1], [80131001, 0, 1]]),
        "props": None
    }),
    100610: _tools.RODict({
        "ID": 100610,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80781001, 1, 1], [80131001, 1, 1]]),
        "props": None
    }),
    100611: _tools.RODict({
        "ID": 100611,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenAnti":2}),
        "equipment": _tools.ROList([[80781001, 2, 1], [80131001, 2, 1]]),
        "props": None
    }),
    100612: _tools.RODict({
        "ID": 100612,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowAnti":2}),
        "equipment": _tools.ROList([[80781001, 3, 1], [80131001, 3, 1]]),
        "props": None
    }),
    100613: _tools.RODict({
        "ID": 100613,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushAnti":3}),
        "equipment": _tools.ROList([[80781001, 4, 1], [80131001, 4, 1]]),
        "props": None
    }),
    100614: _tools.RODict({
        "ID": 100614,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockAnti":4}),
        "equipment": _tools.ROList([[80781001, 5, 1], [80131001, 5, 1]]),
        "props": None
    }),
    100615: _tools.RODict({
        "ID": 100615,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80781001, 3, 1], [80131001, 3, 1]]),
        "props": None
    }),
    100616: _tools.RODict({
        "ID": 100616,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80781001, 4, 1], [80131001, 4, 1]]),
        "props": None
    }),
    100617: _tools.RODict({
        "ID": 100617,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockAnti":2}),
        "equipment": _tools.ROList([[80781001, 0, 2], [80131001, 0, 2]]),
        "props": None
    }),
    100618: _tools.RODict({
        "ID": 100618,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushAnti":2}),
        "equipment": _tools.ROList([[80781001, 1, 2], [80131001, 1, 2]]),
        "props": None
    }),
    100619: _tools.RODict({
        "ID": 100619,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowAnti":3}),
        "equipment": _tools.ROList([[80781001, 2, 2], [80131001, 2, 2]]),
        "props": None
    }),
    100620: _tools.RODict({
        "ID": 100620,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenAnti":3}),
        "equipment": _tools.ROList([[80781001, 3, 2], [80131001, 3, 2]]),
        "props": None
    }),
    100621: _tools.RODict({
        "ID": 100621,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentAnti":4}),
        "equipment": _tools.ROList([[80781001, 4, 2], [80131001, 4, 2]]),
        "props": None
    }),
    100622: _tools.RODict({
        "ID": 100622,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunAnti":5}),
        "equipment": _tools.ROList([[80781001, 5, 2], [80131001, 5, 2]]),
        "props": None
    }),
    100623: _tools.RODict({
        "ID": 100623,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80781001, 3, 2], [80131001, 3, 2]]),
        "props": None
    }),
    100624: _tools.RODict({
        "ID": 100624,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80781001, 4, 2], [80131001, 4, 2]]),
        "props": None
    }),
    100625: _tools.RODict({
        "ID": 100625,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunAnti":2}),
        "equipment": _tools.ROList([[80781001, 0, 3], [80131001, 0, 3]]),
        "props": None
    }),
    100626: _tools.RODict({
        "ID": 100626,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentAnti":4}),
        "equipment": _tools.ROList([[80781001, 1, 3], [80131001, 1, 3]]),
        "props": None
    }),
    100627: _tools.RODict({
        "ID": 100627,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenAnti":5}),
        "equipment": _tools.ROList([[80781001, 2, 3], [80131001, 2, 3]]),
        "props": None
    }),
    100628: _tools.RODict({
        "ID": 100628,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowAnti":5}),
        "equipment": _tools.ROList([[80781001, 3, 3], [80131001, 3, 3]]),
        "props": None
    }),
    100629: _tools.RODict({
        "ID": 100629,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushAnti":6}),
        "equipment": _tools.ROList([[80781001, 4, 3], [80131001, 4, 3]]),
        "props": None
    }),
    100630: _tools.RODict({
        "ID": 100630,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockAnti":6}),
        "equipment": _tools.ROList([[80781001, 5, 3], [80131001, 5, 3]]),
        "props": None
    }),
    100631: _tools.RODict({
        "ID": 100631,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80781001, 4, 3], [80131001, 4, 3]]),
        "props": None
    }),
    100632: _tools.RODict({
        "ID": 100632,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80781001, 5, 3], [80131001, 5, 3]]),
        "props": None
    }),
    100633: _tools.RODict({
        "ID": 100633,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockAnti":3}),
        "equipment": _tools.ROList([[80781001, 0, 4], [80131001, 0, 4]]),
        "props": None
    }),
    100634: _tools.RODict({
        "ID": 100634,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushAnti":4}),
        "equipment": _tools.ROList([[80781001, 1, 4], [80131001, 1, 4]]),
        "props": None
    }),
    100635: _tools.RODict({
        "ID": 100635,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowAnti":5}),
        "equipment": _tools.ROList([[80781001, 2, 4], [80131001, 2, 4]]),
        "props": None
    }),
    100636: _tools.RODict({
        "ID": 100636,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenAnti":5}),
        "equipment": _tools.ROList([[80781001, 3, 4], [80131001, 3, 4]]),
        "props": None
    }),
    100637: _tools.RODict({
        "ID": 100637,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentAnti":6}),
        "equipment": _tools.ROList([[80781001, 4, 4], [80131001, 4, 4]]),
        "props": None
    }),
    100638: _tools.RODict({
        "ID": 100638,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunAnti":7}),
        "equipment": _tools.ROList([[80781001, 5, 4], [80131001, 5, 4]]),
        "props": None
    }),
    100639: _tools.RODict({
        "ID": 100639,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80781001, 5, 4], [80131001, 5, 4]]),
        "props": None
    }),
    100640: _tools.RODict({
        "ID": 100640,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80781001, 6, 4], [80131001, 6, 4]]),
        "props": None
    }),
    100641: _tools.RODict({
        "ID": 100641,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80121001, 0, 1], [80791001, 0, 1]]),
        "props": None
    }),
    100642: _tools.RODict({
        "ID": 100642,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80121001, 1, 1], [80791001, 1, 1]]),
        "props": None
    }),
    100643: _tools.RODict({
        "ID": 100643,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":2}),
        "equipment": _tools.ROList([[80121001, 2, 1], [80791001, 2, 1]]),
        "props": None
    }),
    100644: _tools.RODict({
        "ID": 100644,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":2}),
        "equipment": _tools.ROList([[80121001, 3, 1], [80791001, 3, 1]]),
        "props": None
    }),
    100645: _tools.RODict({
        "ID": 100645,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPushAnti":3}),
        "equipment": _tools.ROList([[80121001, 4, 1], [80791001, 4, 1]]),
        "props": None
    }),
    100646: _tools.RODict({
        "ID": 100646,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":4}),
        "equipment": _tools.ROList([[80121001, 5, 1], [80791001, 5, 1]]),
        "props": None
    }),
    100647: _tools.RODict({
        "ID": 100647,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80121001, 3, 1], [80791001, 3, 1]]),
        "props": None
    }),
    100648: _tools.RODict({
        "ID": 100648,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80121001, 4, 1], [80791001, 4, 1]]),
        "props": None
    }),
    100649: _tools.RODict({
        "ID": 100649,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":2}),
        "equipment": _tools.ROList([[80121001, 0, 2], [80791001, 0, 2]]),
        "props": None
    }),
    100650: _tools.RODict({
        "ID": 100650,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPushAnti":2}),
        "equipment": _tools.ROList([[80121001, 1, 2], [80791001, 1, 2]]),
        "props": None
    }),
    100651: _tools.RODict({
        "ID": 100651,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":3}),
        "equipment": _tools.ROList([[80121001, 2, 2], [80791001, 2, 2]]),
        "props": None
    }),
    100652: _tools.RODict({
        "ID": 100652,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":3}),
        "equipment": _tools.ROList([[80121001, 3, 2], [80791001, 3, 2]]),
        "props": None
    }),
    100653: _tools.RODict({
        "ID": 100653,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":4}),
        "equipment": _tools.ROList([[80121001, 4, 2], [80791001, 4, 2]]),
        "props": None
    }),
    100654: _tools.RODict({
        "ID": 100654,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjStunAnti":5}),
        "equipment": _tools.ROList([[80121001, 5, 2], [80791001, 5, 2]]),
        "props": None
    }),
    100655: _tools.RODict({
        "ID": 100655,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80121001, 3, 2], [80791001, 3, 2]]),
        "props": None
    }),
    100656: _tools.RODict({
        "ID": 100656,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80121001, 4, 2], [80791001, 4, 2]]),
        "props": None
    }),
    100657: _tools.RODict({
        "ID": 100657,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjStunAnti":2}),
        "equipment": _tools.ROList([[80121001, 0, 3], [80791001, 0, 3]]),
        "props": None
    }),
    100658: _tools.RODict({
        "ID": 100658,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":4}),
        "equipment": _tools.ROList([[80121001, 1, 3], [80791001, 1, 3]]),
        "props": None
    }),
    100659: _tools.RODict({
        "ID": 100659,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":5}),
        "equipment": _tools.ROList([[80121001, 2, 3], [80791001, 2, 3]]),
        "props": None
    }),
    100660: _tools.RODict({
        "ID": 100660,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":5}),
        "equipment": _tools.ROList([[80121001, 3, 3], [80791001, 3, 3]]),
        "props": None
    }),
    100661: _tools.RODict({
        "ID": 100661,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPushAnti":6}),
        "equipment": _tools.ROList([[80121001, 4, 3], [80791001, 4, 3]]),
        "props": None
    }),
    100662: _tools.RODict({
        "ID": 100662,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":6}),
        "equipment": _tools.ROList([[80121001, 5, 3], [80791001, 5, 3]]),
        "props": None
    }),
    100663: _tools.RODict({
        "ID": 100663,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80121001, 4, 3], [80791001, 4, 3]]),
        "props": None
    }),
    100664: _tools.RODict({
        "ID": 100664,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80121001, 5, 3], [80791001, 5, 3]]),
        "props": None
    }),
    100665: _tools.RODict({
        "ID": 100665,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":3}),
        "equipment": _tools.ROList([[80121001, 0, 4], [80791001, 0, 4]]),
        "props": None
    }),
    100666: _tools.RODict({
        "ID": 100666,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPushAnti":4}),
        "equipment": _tools.ROList([[80121001, 1, 4], [80791001, 1, 4]]),
        "props": None
    }),
    100667: _tools.RODict({
        "ID": 100667,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":5}),
        "equipment": _tools.ROList([[80121001, 2, 4], [80791001, 2, 4]]),
        "props": None
    }),
    100668: _tools.RODict({
        "ID": 100668,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":5}),
        "equipment": _tools.ROList([[80121001, 3, 4], [80791001, 3, 4]]),
        "props": None
    }),
    100669: _tools.RODict({
        "ID": 100669,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":6}),
        "equipment": _tools.ROList([[80121001, 4, 4], [80791001, 4, 4]]),
        "props": None
    }),
    100670: _tools.RODict({
        "ID": 100670,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjStunAnti":7}),
        "equipment": _tools.ROList([[80121001, 5, 4], [80791001, 5, 4]]),
        "props": None
    }),
    100671: _tools.RODict({
        "ID": 100671,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80121001, 5, 4], [80791001, 5, 4]]),
        "props": None
    }),
    100672: _tools.RODict({
        "ID": 100672,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80121001, 6, 4], [80791001, 6, 4]]),
        "props": None
    }),
    100673: _tools.RODict({
        "ID": 100673,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80111001, 0, 1], [80791001, 0, 1]]),
        "props": None
    }),
    100674: _tools.RODict({
        "ID": 100674,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80111001, 1, 1], [80791001, 1, 1]]),
        "props": None
    }),
    100675: _tools.RODict({
        "ID": 100675,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":2}),
        "equipment": _tools.ROList([[80111001, 2, 1], [80791001, 2, 1]]),
        "props": None
    }),
    100676: _tools.RODict({
        "ID": 100676,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":2}),
        "equipment": _tools.ROList([[80111001, 3, 1], [80791001, 3, 1]]),
        "props": None
    }),
    100677: _tools.RODict({
        "ID": 100677,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPushAnti":3}),
        "equipment": _tools.ROList([[80111001, 4, 1], [80791001, 4, 1]]),
        "props": None
    }),
    100678: _tools.RODict({
        "ID": 100678,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":4}),
        "equipment": _tools.ROList([[80111001, 5, 1], [80791001, 5, 1]]),
        "props": None
    }),
    100679: _tools.RODict({
        "ID": 100679,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80111001, 3, 1], [80791001, 3, 1]]),
        "props": None
    }),
    100680: _tools.RODict({
        "ID": 100680,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80111001, 4, 1], [80791001, 4, 1]]),
        "props": None
    }),
    100681: _tools.RODict({
        "ID": 100681,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":2}),
        "equipment": _tools.ROList([[80111001, 0, 2], [80791001, 0, 2]]),
        "props": None
    }),
    100682: _tools.RODict({
        "ID": 100682,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPushAnti":2}),
        "equipment": _tools.ROList([[80111001, 1, 2], [80791001, 1, 2]]),
        "props": None
    }),
    100683: _tools.RODict({
        "ID": 100683,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":3}),
        "equipment": _tools.ROList([[80111001, 2, 2], [80791001, 2, 2]]),
        "props": None
    }),
    100684: _tools.RODict({
        "ID": 100684,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":3}),
        "equipment": _tools.ROList([[80111001, 3, 2], [80791001, 3, 2]]),
        "props": None
    }),
    100685: _tools.RODict({
        "ID": 100685,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":4}),
        "equipment": _tools.ROList([[80111001, 4, 2], [80791001, 4, 2]]),
        "props": None
    }),
    100686: _tools.RODict({
        "ID": 100686,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjStunAnti":5}),
        "equipment": _tools.ROList([[80111001, 5, 2], [80791001, 5, 2]]),
        "props": None
    }),
    100687: _tools.RODict({
        "ID": 100687,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80111001, 3, 2], [80791001, 3, 2]]),
        "props": None
    }),
    100688: _tools.RODict({
        "ID": 100688,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80111001, 4, 2], [80791001, 4, 2]]),
        "props": None
    }),
    100689: _tools.RODict({
        "ID": 100689,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjStunAnti":2}),
        "equipment": _tools.ROList([[80111001, 0, 3], [80791001, 0, 3]]),
        "props": None
    }),
    100690: _tools.RODict({
        "ID": 100690,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":4}),
        "equipment": _tools.ROList([[80111001, 1, 3], [80791001, 1, 3]]),
        "props": None
    }),
    100691: _tools.RODict({
        "ID": 100691,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":5}),
        "equipment": _tools.ROList([[80111001, 2, 3], [80791001, 2, 3]]),
        "props": None
    }),
    100692: _tools.RODict({
        "ID": 100692,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":5}),
        "equipment": _tools.ROList([[80111001, 3, 3], [80791001, 3, 3]]),
        "props": None
    }),
    100693: _tools.RODict({
        "ID": 100693,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPushAnti":6}),
        "equipment": _tools.ROList([[80111001, 4, 3], [80791001, 4, 3]]),
        "props": None
    }),
    100694: _tools.RODict({
        "ID": 100694,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":6}),
        "equipment": _tools.ROList([[80111001, 5, 3], [80791001, 5, 3]]),
        "props": None
    }),
    100695: _tools.RODict({
        "ID": 100695,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80111001, 4, 3], [80791001, 4, 3]]),
        "props": None
    }),
    100696: _tools.RODict({
        "ID": 100696,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80111001, 5, 3], [80791001, 5, 3]]),
        "props": None
    }),
    100697: _tools.RODict({
        "ID": 100697,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":3}),
        "equipment": _tools.ROList([[80111001, 0, 4], [80791001, 0, 4]]),
        "props": None
    }),
    100698: _tools.RODict({
        "ID": 100698,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPushAnti":4}),
        "equipment": _tools.ROList([[80111001, 1, 4], [80791001, 1, 4]]),
        "props": None
    }),
    100699: _tools.RODict({
        "ID": 100699,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":5}),
        "equipment": _tools.ROList([[80111001, 2, 4], [80791001, 2, 4]]),
        "props": None
    }),
    100700: _tools.RODict({
        "ID": 100700,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":5}),
        "equipment": _tools.ROList([[80111001, 3, 4], [80791001, 3, 4]]),
        "props": None
    }),
    100701: _tools.RODict({
        "ID": 100701,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":6}),
        "equipment": _tools.ROList([[80111001, 4, 4], [80791001, 4, 4]]),
        "props": None
    }),
    100702: _tools.RODict({
        "ID": 100702,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjStunAnti":7}),
        "equipment": _tools.ROList([[80111001, 5, 4], [80791001, 5, 4]]),
        "props": None
    }),
    100703: _tools.RODict({
        "ID": 100703,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80111001, 5, 4], [80791001, 5, 4]]),
        "props": None
    }),
    100704: _tools.RODict({
        "ID": 100704,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80111001, 6, 4], [80791001, 6, 4]]),
        "props": None
    }),
    100705: _tools.RODict({
        "ID": 100705,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.015}),
        "equipment": None,
        "props": _tools.ROList([30001001, 30001002, 30001003, 30001004, 30001005])
    }),
    100706: _tools.RODict({
        "ID": 100706,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.015}),
        "equipment": None,
        "props": _tools.ROList([30001006, 30001007, 30001008, 30001009, 30001010])
    }),
    100707: _tools.RODict({
        "ID": 100707,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.015}),
        "equipment": None,
        "props": _tools.ROList([30001001, 30001002, 30001003, 30001004, 30001010])
    }),
    100708: _tools.RODict({
        "ID": 100708,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001003, 30001004, 30001005, 30001006])
    }),
    100709: _tools.RODict({
        "ID": 100709,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001005, 30001006, 30001007, 30001008])
    }),
    100710: _tools.RODict({
        "ID": 100710,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001007, 30001008, 30001009, 30001010])
    }),
    100711: _tools.RODict({
        "ID": 100711,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001001, 30001002, 30001009, 30001010])
    }),
    100712: _tools.RODict({
        "ID": 100712,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjAccuracy":3}),
        "equipment": None,
        "props": _tools.ROList([30001011, 30001012, 30001013, 30001014, 30001015])
    }),
    100713: _tools.RODict({
        "ID": 100713,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjAccuracy":3}),
        "equipment": None,
        "props": _tools.ROList([30001016, 30001017, 30001018, 30001019, 30001020])
    }),
    100714: _tools.RODict({
        "ID": 100714,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": None,
        "props": _tools.ROList([30001007, 30001008, 30001009, 30001005])
    }),
    100715: _tools.RODict({
        "ID": 100715,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": None,
        "props": _tools.ROList([30001006, 30001007, 30001003, 30001004])
    }),
    100716: _tools.RODict({
        "ID": 100716,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjAccuracy":2}),
        "equipment": None,
        "props": _tools.ROList([30001015, 30001016, 30001017, 30001018])
    }),
    100717: _tools.RODict({
        "ID": 100717,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjAccuracy":2}),
        "equipment": None,
        "props": _tools.ROList([30001017, 30001018, 30001019, 30001020])
    }),
    100718: _tools.RODict({
        "ID": 100718,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjAccuracy":3}),
        "equipment": None,
        "props": _tools.ROList([30001011, 30001012, 30001019, 30001020, 30001015])
    }),
    100719: _tools.RODict({
        "ID": 100719,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001001, 30001002, 30001003])
    }),
    100720: _tools.RODict({
        "ID": 100720,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001002, 30001003, 30001004])
    }),
    100721: _tools.RODict({
        "ID": 100721,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001003, 30001004, 30001005])
    }),
    100722: _tools.RODict({
        "ID": 100722,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001004, 30001005, 30001006])
    }),
    100723: _tools.RODict({
        "ID": 100723,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001005, 30001006, 30001007])
    }),
    100724: _tools.RODict({
        "ID": 100724,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001006, 30001007, 30001008])
    }),
    100725: _tools.RODict({
        "ID": 100725,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001007, 30001008, 30001009])
    }),
    100726: _tools.RODict({
        "ID": 100726,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001008, 30001009, 30001010])
    }),
    100727: _tools.RODict({
        "ID": 100727,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001009, 30001010, 30001001])
    }),
    100728: _tools.RODict({
        "ID": 100728,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.02}),
        "equipment": None,
        "props": _tools.ROList([30001004, 30001001, 30001014, 30001011])
    }),
    100729: _tools.RODict({
        "ID": 100729,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.02}),
        "equipment": None,
        "props": _tools.ROList([30001005, 30001002, 30001015, 30001012])
    }),
    100730: _tools.RODict({
        "ID": 100730,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.02}),
        "equipment": None,
        "props": _tools.ROList([30001006, 30001003, 30001016, 30001013])
    }),
    100731: _tools.RODict({
        "ID": 100731,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.02}),
        "equipment": None,
        "props": _tools.ROList([30001007, 30001009, 30001017, 30001019])
    }),
    100732: _tools.RODict({
        "ID": 100732,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.02}),
        "equipment": None,
        "props": _tools.ROList([30001008, 30001010, 30001018, 30001020])
    }),
    100733: _tools.RODict({
        "ID": 100733,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.045}),
        "equipment": None,
        "props": _tools.ROList([30001018, 30001015, 30001019, 30001012, 30001016])
    }),
    100734: _tools.RODict({
        "ID": 100734,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.045}),
        "equipment": None,
        "props": _tools.ROList([30001012, 30001016, 30001020, 30001013, 30001017])
    }),
    100735: _tools.RODict({
        "ID": 100735,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.045}),
        "equipment": None,
        "props": _tools.ROList([30001013, 30001017, 30001011, 30001014, 30001020])
    }),
    100736: _tools.RODict({
        "ID": 100736,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.045}),
        "equipment": None,
        "props": _tools.ROList([30001014, 30001018, 30001019, 30001011, 30001017])
    }),
    100737: _tools.RODict({
        "ID": 100737,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.015}),
        "equipment": None,
        "props": _tools.ROList([30003008, 30003010, 30003012, 30003013, 30003004])
    }),
    100738: _tools.RODict({
        "ID": 100738,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.01}),
        "equipment": None,
        "props": _tools.ROList([30003007, 30003009, 30003011])
    }),
    100739: _tools.RODict({
        "ID": 100739,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.01}),
        "equipment": None,
        "props": _tools.ROList([30003002, 30003004, 30003006])
    }),
    100740: _tools.RODict({
        "ID": 100740,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.01}),
        "equipment": None,
        "props": _tools.ROList([30003001, 30003003, 30003005])
    }),
    100741: _tools.RODict({
        "ID": 100741,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.01}),
        "equipment": None,
        "props": _tools.ROList([30003001, 30003002, 30003003, 30003004])
    }),
    100742: _tools.RODict({
        "ID": 100742,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.01}),
        "equipment": None,
        "props": _tools.ROList([30003005, 30003006, 30003007, 30003008])
    }),
    100743: _tools.RODict({
        "ID": 100743,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.015}),
        "equipment": None,
        "props": _tools.ROList([30003009, 30003010, 30003011, 30003012, 30003013])
    }),
    100744: _tools.RODict({
        "ID": 100744,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.035}),
        "equipment": None,
        "props": _tools.ROList([30003014, 30003015, 30003016, 30003017])
    }),
    100745: _tools.RODict({
        "ID": 100745,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.035}),
        "equipment": None,
        "props": _tools.ROList([30003018, 30003019, 30003020, 30003021])
    }),
    100746: _tools.RODict({
        "ID": 100746,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.035}),
        "equipment": None,
        "props": _tools.ROList([30003022, 30003023, 30003024, 30003025])
    }),
    100747: _tools.RODict({
        "ID": 100747,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.035}),
        "equipment": None,
        "props": _tools.ROList([30003026, 30003027, 30003028, 30003029, 30003030])
    }),
    100748: _tools.RODict({
        "ID": 100748,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001001, 30001002, 30003001, 30003002, 30003011])
    }),
    100749: _tools.RODict({
        "ID": 100749,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001003, 30001004, 30003003, 30003004, 30003012])
    }),
    100750: _tools.RODict({
        "ID": 100750,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001005, 30001006, 30003005, 30003006, 30003013])
    }),
    100751: _tools.RODict({
        "ID": 100751,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001007, 30001008, 30003007, 30003008])
    }),
    100752: _tools.RODict({
        "ID": 100752,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001009, 30001010, 30003009, 30003010])
    }),
    100753: _tools.RODict({
        "ID": 100753,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.03}),
        "equipment": None,
        "props": _tools.ROList([30001011, 30001012, 30003014, 30003015, 30003024, 30003029])
    }),
    100754: _tools.RODict({
        "ID": 100754,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.03}),
        "equipment": None,
        "props": _tools.ROList([30001013, 30001014, 30003016, 30003017, 30003025, 30003030])
    }),
    100755: _tools.RODict({
        "ID": 100755,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.02}),
        "equipment": None,
        "props": _tools.ROList([30001015, 30001016, 30003018, 30003019, 30003026])
    }),
    100756: _tools.RODict({
        "ID": 100756,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.02}),
        "equipment": None,
        "props": _tools.ROList([30001017, 30001018, 30003020, 30003021, 30003027])
    }),
    100757: _tools.RODict({
        "ID": 100757,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.02}),
        "equipment": None,
        "props": _tools.ROList([30001019, 30001020, 30003022, 30003023, 30003028])
    }),
    100758: _tools.RODict({
        "ID": 100758,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjEvasion":2}),
        "equipment": None,
        "props": _tools.ROList([30003014, 30003018, 30003022, 30003026, 30003030])
    }),
    100759: _tools.RODict({
        "ID": 100759,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": None,
        "props": _tools.ROList([30003009, 30003010, 30003011, 30003005, 30003006])
    }),
    100760: _tools.RODict({
        "ID": 100760,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjEvasion":2}),
        "equipment": None,
        "props": _tools.ROList([30003030, 30003020, 30003024, 30003028, 30003017])
    }),
    100761: _tools.RODict({
        "ID": 100761,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": None,
        "props": _tools.ROList([30003001, 30003003, 30003005, 30003004, 30003006])
    }),
    100762: _tools.RODict({
        "ID": 100762,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjEvasion":2}),
        "equipment": None,
        "props": _tools.ROList([30003030, 30003018, 30003026, 30003028, 30003027])
    }),
    100763: _tools.RODict({
        "ID": 100763,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjEvasion":2}),
        "equipment": None,
        "props": _tools.ROList([30003014, 30003019, 30003024, 30003029, 30003021])
    })
})
minKey = 100001
maxKey = 100763