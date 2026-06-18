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
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":1}),
        "equipment": _tools.ROList([[80111001, 0, 1], [80591001, 0, 1], [80791001, 0, 1]]),
        "props": None
    }),
    100034: _tools.RODict({
        "ID": 100034,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":1}),
        "equipment": _tools.ROList([[80111001, 1, 1], [80591001, 1, 1], [80791001, 1, 1]]),
        "props": None
    }),
    100035: _tools.RODict({
        "ID": 100035,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":2}),
        "equipment": _tools.ROList([[80111001, 2, 1], [80591001, 2, 1], [80791001, 2, 1]]),
        "props": None
    }),
    100036: _tools.RODict({
        "ID": 100036,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":2}),
        "equipment": _tools.ROList([[80111001, 3, 1], [80591001, 3, 1], [80791001, 3, 1]]),
        "props": None
    }),
    100037: _tools.RODict({
        "ID": 100037,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":3}),
        "equipment": _tools.ROList([[80111001, 4, 1], [80591001, 4, 1], [80791001, 4, 1]]),
        "props": None
    }),
    100038: _tools.RODict({
        "ID": 100038,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":3}),
        "equipment": _tools.ROList([[80111001, 5, 1], [80591001, 5, 1], [80791001, 5, 1]]),
        "props": None
    }),
    100039: _tools.RODict({
        "ID": 100039,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":4}),
        "equipment": _tools.ROList([[80111001, 6, 1], [80591001, 6, 1], [80791001, 6, 1]]),
        "props": None
    }),
    100040: _tools.RODict({
        "ID": 100040,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":4}),
        "equipment": _tools.ROList([[80111001, 7, 1], [80591001, 7, 1], [80791001, 7, 1]]),
        "props": None
    }),
    100041: _tools.RODict({
        "ID": 100041,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":1}),
        "equipment": _tools.ROList([[80111001, 0, 2], [80591001, 0, 2], [80791001, 0, 2]]),
        "props": None
    }),
    100042: _tools.RODict({
        "ID": 100042,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":1}),
        "equipment": _tools.ROList([[80111001, 1, 2], [80591001, 1, 2], [80791001, 1, 2]]),
        "props": None
    }),
    100043: _tools.RODict({
        "ID": 100043,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":2}),
        "equipment": _tools.ROList([[80111001, 2, 2], [80591001, 2, 2], [80791001, 2, 2]]),
        "props": None
    }),
    100044: _tools.RODict({
        "ID": 100044,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":2}),
        "equipment": _tools.ROList([[80111001, 3, 2], [80591001, 3, 2], [80791001, 3, 2]]),
        "props": None
    }),
    100045: _tools.RODict({
        "ID": 100045,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":3}),
        "equipment": _tools.ROList([[80111001, 4, 2], [80591001, 4, 2], [80791001, 4, 2]]),
        "props": None
    }),
    100046: _tools.RODict({
        "ID": 100046,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":3}),
        "equipment": _tools.ROList([[80111001, 5, 2], [80591001, 5, 2], [80791001, 5, 2]]),
        "props": None
    }),
    100047: _tools.RODict({
        "ID": 100047,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":4}),
        "equipment": _tools.ROList([[80111001, 6, 2], [80591001, 6, 2], [80791001, 6, 2]]),
        "props": None
    }),
    100048: _tools.RODict({
        "ID": 100048,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":4}),
        "equipment": _tools.ROList([[80111001, 7, 2], [80591001, 7, 2], [80791001, 7, 2]]),
        "props": None
    }),
    100049: _tools.RODict({
        "ID": 100049,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":1}),
        "equipment": _tools.ROList([[80111001, 0, 3], [80591001, 0, 3], [80791001, 0, 3]]),
        "props": None
    }),
    100050: _tools.RODict({
        "ID": 100050,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":1}),
        "equipment": _tools.ROList([[80111001, 1, 3], [80591001, 1, 3], [80791001, 1, 3]]),
        "props": None
    }),
    100051: _tools.RODict({
        "ID": 100051,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":2}),
        "equipment": _tools.ROList([[80111001, 2, 3], [80591001, 2, 3], [80791001, 2, 3]]),
        "props": None
    }),
    100052: _tools.RODict({
        "ID": 100052,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":2}),
        "equipment": _tools.ROList([[80111001, 3, 3], [80591001, 3, 3], [80791001, 3, 3]]),
        "props": None
    }),
    100053: _tools.RODict({
        "ID": 100053,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":3}),
        "equipment": _tools.ROList([[80111001, 4, 3], [80591001, 4, 3], [80791001, 4, 3]]),
        "props": None
    }),
    100054: _tools.RODict({
        "ID": 100054,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":3}),
        "equipment": _tools.ROList([[80111001, 5, 3], [80591001, 5, 3], [80791001, 5, 3]]),
        "props": None
    }),
    100055: _tools.RODict({
        "ID": 100055,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":4}),
        "equipment": _tools.ROList([[80111001, 6, 3], [80591001, 6, 3], [80791001, 6, 3]]),
        "props": None
    }),
    100056: _tools.RODict({
        "ID": 100056,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":4}),
        "equipment": _tools.ROList([[80111001, 7, 3], [80591001, 7, 3], [80791001, 7, 3]]),
        "props": None
    }),
    100057: _tools.RODict({
        "ID": 100057,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":1}),
        "equipment": _tools.ROList([[80111001, 0, 4], [80591001, 0, 4], [80791001, 0, 4]]),
        "props": None
    }),
    100058: _tools.RODict({
        "ID": 100058,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":1}),
        "equipment": _tools.ROList([[80111001, 1, 4], [80591001, 1, 4], [80791001, 1, 4]]),
        "props": None
    }),
    100059: _tools.RODict({
        "ID": 100059,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":2}),
        "equipment": _tools.ROList([[80111001, 2, 4], [80591001, 2, 4], [80791001, 2, 4]]),
        "props": None
    }),
    100060: _tools.RODict({
        "ID": 100060,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":2}),
        "equipment": _tools.ROList([[80111001, 3, 4], [80591001, 3, 4], [80791001, 3, 4]]),
        "props": None
    }),
    100061: _tools.RODict({
        "ID": 100061,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":3}),
        "equipment": _tools.ROList([[80111001, 4, 4], [80591001, 4, 4], [80791001, 4, 4]]),
        "props": None
    }),
    100062: _tools.RODict({
        "ID": 100062,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":3}),
        "equipment": _tools.ROList([[80111001, 5, 4], [80591001, 5, 4], [80791001, 5, 4]]),
        "props": None
    }),
    100063: _tools.RODict({
        "ID": 100063,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":4}),
        "equipment": _tools.ROList([[80111001, 6, 4], [80591001, 6, 4], [80791001, 6, 4]]),
        "props": None
    }),
    100064: _tools.RODict({
        "ID": 100064,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":4}),
        "equipment": _tools.ROList([[80111001, 7, 4], [80591001, 7, 4], [80791001, 7, 4]]),
        "props": None
    }),
    100065: _tools.RODict({
        "ID": 100065,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":30}),
        "equipment": _tools.ROList([[80211001, 0, 1], [80811001, 0, 1], [80791001, 0, 1]]),
        "props": None
    }),
    100066: _tools.RODict({
        "ID": 100066,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":45}),
        "equipment": _tools.ROList([[80211001, 1, 1], [80811001, 1, 1], [80791001, 1, 1]]),
        "props": None
    }),
    100067: _tools.RODict({
        "ID": 100067,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":60}),
        "equipment": _tools.ROList([[80211001, 2, 1], [80811001, 2, 1], [80791001, 2, 1]]),
        "props": None
    }),
    100068: _tools.RODict({
        "ID": 100068,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":75}),
        "equipment": _tools.ROList([[80211001, 3, 1], [80811001, 3, 1], [80791001, 3, 1]]),
        "props": None
    }),
    100069: _tools.RODict({
        "ID": 100069,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":90}),
        "equipment": _tools.ROList([[80211001, 4, 1], [80811001, 4, 1], [80791001, 4, 1]]),
        "props": None
    }),
    100070: _tools.RODict({
        "ID": 100070,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":120}),
        "equipment": _tools.ROList([[80211001, 5, 1], [80811001, 5, 1], [80791001, 5, 1]]),
        "props": None
    }),
    100071: _tools.RODict({
        "ID": 100071,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":160}),
        "equipment": _tools.ROList([[80211001, 6, 1], [80811001, 6, 1], [80791001, 6, 1]]),
        "props": None
    }),
    100072: _tools.RODict({
        "ID": 100072,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":250}),
        "equipment": _tools.ROList([[80211001, 7, 1], [80811001, 7, 1], [80791001, 7, 1]]),
        "props": None
    }),
    100073: _tools.RODict({
        "ID": 100073,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":60}),
        "equipment": _tools.ROList([[80211001, 0, 2], [80811001, 0, 2], [80791001, 0, 2]]),
        "props": None
    }),
    100074: _tools.RODict({
        "ID": 100074,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":75}),
        "equipment": _tools.ROList([[80211001, 1, 2], [80811001, 1, 2], [80791001, 1, 2]]),
        "props": None
    }),
    100075: _tools.RODict({
        "ID": 100075,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":90}),
        "equipment": _tools.ROList([[80211001, 2, 2], [80811001, 2, 2], [80791001, 2, 2]]),
        "props": None
    }),
    100076: _tools.RODict({
        "ID": 100076,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":105}),
        "equipment": _tools.ROList([[80211001, 3, 2], [80811001, 3, 2], [80791001, 3, 2]]),
        "props": None
    }),
    100077: _tools.RODict({
        "ID": 100077,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":120}),
        "equipment": _tools.ROList([[80211001, 4, 2], [80811001, 4, 2], [80791001, 4, 2]]),
        "props": None
    }),
    100078: _tools.RODict({
        "ID": 100078,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":150}),
        "equipment": _tools.ROList([[80211001, 5, 2], [80811001, 5, 2], [80791001, 5, 2]]),
        "props": None
    }),
    100079: _tools.RODict({
        "ID": 100079,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":190}),
        "equipment": _tools.ROList([[80211001, 6, 2], [80811001, 6, 2], [80791001, 6, 2]]),
        "props": None
    }),
    100080: _tools.RODict({
        "ID": 100080,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":300}),
        "equipment": _tools.ROList([[80211001, 7, 2], [80811001, 7, 2], [80791001, 7, 2]]),
        "props": None
    }),
    100081: _tools.RODict({
        "ID": 100081,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":90}),
        "equipment": _tools.ROList([[80211001, 0, 3], [80811001, 0, 3], [80791001, 0, 3]]),
        "props": None
    }),
    100082: _tools.RODict({
        "ID": 100082,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":105}),
        "equipment": _tools.ROList([[80211001, 1, 3], [80811001, 1, 3], [80791001, 1, 3]]),
        "props": None
    }),
    100083: _tools.RODict({
        "ID": 100083,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":120}),
        "equipment": _tools.ROList([[80211001, 2, 3], [80811001, 2, 3], [80791001, 2, 3]]),
        "props": None
    }),
    100084: _tools.RODict({
        "ID": 100084,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":140}),
        "equipment": _tools.ROList([[80211001, 3, 3], [80811001, 3, 3], [80791001, 3, 3]]),
        "props": None
    }),
    100085: _tools.RODict({
        "ID": 100085,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":155}),
        "equipment": _tools.ROList([[80211001, 4, 3], [80811001, 4, 3], [80791001, 4, 3]]),
        "props": None
    }),
    100086: _tools.RODict({
        "ID": 100086,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":185}),
        "equipment": _tools.ROList([[80211001, 5, 3], [80811001, 5, 3], [80791001, 5, 3]]),
        "props": None
    }),
    100087: _tools.RODict({
        "ID": 100087,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":225}),
        "equipment": _tools.ROList([[80211001, 6, 3], [80811001, 6, 3], [80791001, 6, 3]]),
        "props": None
    }),
    100088: _tools.RODict({
        "ID": 100088,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":350}),
        "equipment": _tools.ROList([[80211001, 7, 3], [80811001, 7, 3], [80791001, 7, 3]]),
        "props": None
    }),
    100089: _tools.RODict({
        "ID": 100089,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":130}),
        "equipment": _tools.ROList([[80211001, 0, 4], [80811001, 0, 4], [80791001, 0, 4]]),
        "props": None
    }),
    100090: _tools.RODict({
        "ID": 100090,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":145}),
        "equipment": _tools.ROList([[80211001, 1, 4], [80811001, 1, 4], [80791001, 1, 4]]),
        "props": None
    }),
    100091: _tools.RODict({
        "ID": 100091,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":160}),
        "equipment": _tools.ROList([[80211001, 2, 4], [80811001, 2, 4], [80791001, 2, 4]]),
        "props": None
    }),
    100092: _tools.RODict({
        "ID": 100092,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":180}),
        "equipment": _tools.ROList([[80211001, 3, 4], [80811001, 3, 4], [80791001, 3, 4]]),
        "props": None
    }),
    100093: _tools.RODict({
        "ID": 100093,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":200}),
        "equipment": _tools.ROList([[80211001, 4, 4], [80811001, 4, 4], [80791001, 4, 4]]),
        "props": None
    }),
    100094: _tools.RODict({
        "ID": 100094,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":225}),
        "equipment": _tools.ROList([[80211001, 5, 4], [80811001, 5, 4], [80791001, 5, 4]]),
        "props": None
    }),
    100095: _tools.RODict({
        "ID": 100095,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":270}),
        "equipment": _tools.ROList([[80211001, 6, 4], [80811001, 6, 4], [80791001, 6, 4]]),
        "props": None
    }),
    100096: _tools.RODict({
        "ID": 100096,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullHp":400}),
        "equipment": _tools.ROList([[80211001, 7, 4], [80811001, 7, 4], [80791001, 7, 4]]),
        "props": None
    }),
    100097: _tools.RODict({
        "ID": 100097,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullMp":3}),
        "equipment": _tools.ROList([[80211001, 0, 1], [80591001, 0, 1], [80691001, 0, 1]]),
        "props": None
    }),
    100098: _tools.RODict({
        "ID": 100098,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullMp":4}),
        "equipment": _tools.ROList([[80211001, 1, 1], [80591001, 1, 1], [80691001, 1, 1]]),
        "props": None
    }),
    100099: _tools.RODict({
        "ID": 100099,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullMp":6}),
        "equipment": _tools.ROList([[80211001, 2, 1], [80591001, 2, 1], [80691001, 2, 1]]),
        "props": None
    }),
    100100: _tools.RODict({
        "ID": 100100,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullMp":8}),
        "equipment": _tools.ROList([[80211001, 3, 1], [80591001, 3, 1], [80691001, 3, 1]]),
        "props": None
    }),
    100101: _tools.RODict({
        "ID": 100101,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullMp":9}),
        "equipment": _tools.ROList([[80211001, 4, 1], [80591001, 4, 1], [80691001, 4, 1]]),
        "props": None
    }),
    100102: _tools.RODict({
        "ID": 100102,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullMp":13}),
        "equipment": _tools.ROList([[80211001, 5, 1], [80591001, 5, 1], [80691001, 5, 1]]),
        "props": None
    }),
    100103: _tools.RODict({
        "ID": 100103,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullMp":17}),
        "equipment": _tools.ROList([[80211001, 6, 1], [80591001, 6, 1], [80691001, 6, 1]]),
        "props": None
    }),
    100104: _tools.RODict({
        "ID": 100104,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullMp":26}),
        "equipment": _tools.ROList([[80211001, 7, 1], [80591001, 7, 1], [80691001, 7, 1]]),
        "props": None
    }),
    100105: _tools.RODict({
        "ID": 100105,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullMp":6}),
        "equipment": _tools.ROList([[80211001, 0, 2], [80591001, 0, 2], [80691001, 0, 2]]),
        "props": None
    }),
    100106: _tools.RODict({
        "ID": 100106,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullMp":8}),
        "equipment": _tools.ROList([[80211001, 1, 2], [80591001, 1, 2], [80691001, 1, 2]]),
        "props": None
    }),
    100107: _tools.RODict({
        "ID": 100107,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullMp":9}),
        "equipment": _tools.ROList([[80211001, 2, 2], [80591001, 2, 2], [80691001, 2, 2]]),
        "props": None
    }),
    100108: _tools.RODict({
        "ID": 100108,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullMp":12}),
        "equipment": _tools.ROList([[80211001, 3, 2], [80591001, 3, 2], [80691001, 3, 2]]),
        "props": None
    }),
    100109: _tools.RODict({
        "ID": 100109,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullMp":13}),
        "equipment": _tools.ROList([[80211001, 4, 2], [80591001, 4, 2], [80691001, 4, 2]]),
        "props": None
    }),
    100110: _tools.RODict({
        "ID": 100110,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullMp":16}),
        "equipment": _tools.ROList([[80211001, 5, 2], [80591001, 5, 2], [80691001, 5, 2]]),
        "props": None
    }),
    100111: _tools.RODict({
        "ID": 100111,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullMp":19}),
        "equipment": _tools.ROList([[80211001, 6, 2], [80591001, 6, 2], [80691001, 6, 2]]),
        "props": None
    }),
    100112: _tools.RODict({
        "ID": 100112,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullMp":28}),
        "equipment": _tools.ROList([[80211001, 7, 2], [80591001, 7, 2], [80691001, 7, 2]]),
        "props": None
    }),
    100113: _tools.RODict({
        "ID": 100113,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullMp":9}),
        "equipment": _tools.ROList([[80211001, 0, 3], [80591001, 0, 3], [80691001, 0, 3]]),
        "props": None
    }),
    100114: _tools.RODict({
        "ID": 100114,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullMp":11}),
        "equipment": _tools.ROList([[80211001, 1, 3], [80591001, 1, 3], [80691001, 1, 3]]),
        "props": None
    }),
    100115: _tools.RODict({
        "ID": 100115,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullMp":13}),
        "equipment": _tools.ROList([[80211001, 2, 3], [80591001, 2, 3], [80691001, 2, 3]]),
        "props": None
    }),
    100116: _tools.RODict({
        "ID": 100116,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullMp":14}),
        "equipment": _tools.ROList([[80211001, 3, 3], [80591001, 3, 3], [80691001, 3, 3]]),
        "props": None
    }),
    100117: _tools.RODict({
        "ID": 100117,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullMp":16}),
        "equipment": _tools.ROList([[80211001, 4, 3], [80591001, 4, 3], [80691001, 4, 3]]),
        "props": None
    }),
    100118: _tools.RODict({
        "ID": 100118,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullMp":19}),
        "equipment": _tools.ROList([[80211001, 5, 3], [80591001, 5, 3], [80691001, 5, 3]]),
        "props": None
    }),
    100119: _tools.RODict({
        "ID": 100119,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullMp":23}),
        "equipment": _tools.ROList([[80211001, 6, 3], [80591001, 6, 3], [80691001, 6, 3]]),
        "props": None
    }),
    100120: _tools.RODict({
        "ID": 100120,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullMp":32}),
        "equipment": _tools.ROList([[80211001, 7, 3], [80591001, 7, 3], [80691001, 7, 3]]),
        "props": None
    }),
    100121: _tools.RODict({
        "ID": 100121,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullMp":13}),
        "equipment": _tools.ROList([[80211001, 0, 4], [80591001, 0, 4], [80691001, 0, 4]]),
        "props": None
    }),
    100122: _tools.RODict({
        "ID": 100122,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullMp":14}),
        "equipment": _tools.ROList([[80211001, 1, 4], [80591001, 1, 4], [80691001, 1, 4]]),
        "props": None
    }),
    100123: _tools.RODict({
        "ID": 100123,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullMp":16}),
        "equipment": _tools.ROList([[80211001, 2, 4], [80591001, 2, 4], [80691001, 2, 4]]),
        "props": None
    }),
    100124: _tools.RODict({
        "ID": 100124,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullMp":18}),
        "equipment": _tools.ROList([[80211001, 3, 4], [80591001, 3, 4], [80691001, 3, 4]]),
        "props": None
    }),
    100125: _tools.RODict({
        "ID": 100125,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullMp":19}),
        "equipment": _tools.ROList([[80211001, 4, 4], [80591001, 4, 4], [80691001, 4, 4]]),
        "props": None
    }),
    100126: _tools.RODict({
        "ID": 100126,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullMp":23}),
        "equipment": _tools.ROList([[80211001, 5, 4], [80591001, 5, 4], [80691001, 5, 4]]),
        "props": None
    }),
    100127: _tools.RODict({
        "ID": 100127,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullMp":25}),
        "equipment": _tools.ROList([[80211001, 6, 4], [80591001, 6, 4], [80691001, 6, 4]]),
        "props": None
    }),
    100128: _tools.RODict({
        "ID": 100128,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFullMp":38}),
        "equipment": _tools.ROList([[80211001, 7, 4], [80591001, 7, 4], [80691001, 7, 4]]),
        "props": None
    }),
    100129: _tools.RODict({
        "ID": 100129,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.001}),
        "equipment": _tools.ROList([[80111001, 0, 1], [80411001, 0, 1], [80691001, 0, 1]]),
        "props": None
    }),
    100130: _tools.RODict({
        "ID": 100130,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.001}),
        "equipment": _tools.ROList([[80111001, 1, 1], [80411001, 1, 1], [80691001, 1, 1]]),
        "props": None
    }),
    100131: _tools.RODict({
        "ID": 100131,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0015}),
        "equipment": _tools.ROList([[80111001, 2, 1], [80411001, 2, 1], [80691001, 2, 1]]),
        "props": None
    }),
    100132: _tools.RODict({
        "ID": 100132,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.002}),
        "equipment": _tools.ROList([[80111001, 3, 1], [80411001, 3, 1], [80691001, 3, 1]]),
        "props": None
    }),
    100133: _tools.RODict({
        "ID": 100133,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.003}),
        "equipment": _tools.ROList([[80111001, 4, 1], [80411001, 4, 1], [80691001, 4, 1]]),
        "props": None
    }),
    100134: _tools.RODict({
        "ID": 100134,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.004}),
        "equipment": _tools.ROList([[80111001, 5, 1], [80411001, 5, 1], [80691001, 5, 1]]),
        "props": None
    }),
    100135: _tools.RODict({
        "ID": 100135,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.005}),
        "equipment": _tools.ROList([[80111001, 6, 1], [80411001, 6, 1], [80691001, 6, 1]]),
        "props": None
    }),
    100136: _tools.RODict({
        "ID": 100136,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0075}),
        "equipment": _tools.ROList([[80111001, 7, 1], [80411001, 7, 1], [80691001, 7, 1]]),
        "props": None
    }),
    100137: _tools.RODict({
        "ID": 100137,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0015}),
        "equipment": _tools.ROList([[80111001, 0, 2], [80411001, 0, 2], [80691001, 0, 2]]),
        "props": None
    }),
    100138: _tools.RODict({
        "ID": 100138,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0015}),
        "equipment": _tools.ROList([[80111001, 1, 2], [80411001, 1, 2], [80691001, 1, 2]]),
        "props": None
    }),
    100139: _tools.RODict({
        "ID": 100139,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.002}),
        "equipment": _tools.ROList([[80111001, 2, 2], [80411001, 2, 2], [80691001, 2, 2]]),
        "props": None
    }),
    100140: _tools.RODict({
        "ID": 100140,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0025}),
        "equipment": _tools.ROList([[80111001, 3, 2], [80411001, 3, 2], [80691001, 3, 2]]),
        "props": None
    }),
    100141: _tools.RODict({
        "ID": 100141,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0035}),
        "equipment": _tools.ROList([[80111001, 4, 2], [80411001, 4, 2], [80691001, 4, 2]]),
        "props": None
    }),
    100142: _tools.RODict({
        "ID": 100142,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0045}),
        "equipment": _tools.ROList([[80111001, 5, 2], [80411001, 5, 2], [80691001, 5, 2]]),
        "props": None
    }),
    100143: _tools.RODict({
        "ID": 100143,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0055}),
        "equipment": _tools.ROList([[80111001, 6, 2], [80411001, 6, 2], [80691001, 6, 2]]),
        "props": None
    }),
    100144: _tools.RODict({
        "ID": 100144,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.008}),
        "equipment": _tools.ROList([[80111001, 7, 2], [80411001, 7, 2], [80691001, 7, 2]]),
        "props": None
    }),
    100145: _tools.RODict({
        "ID": 100145,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.002}),
        "equipment": _tools.ROList([[80111001, 0, 3], [80411001, 0, 3], [80691001, 0, 3]]),
        "props": None
    }),
    100146: _tools.RODict({
        "ID": 100146,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0025}),
        "equipment": _tools.ROList([[80111001, 1, 3], [80411001, 1, 3], [80691001, 1, 3]]),
        "props": None
    }),
    100147: _tools.RODict({
        "ID": 100147,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0025}),
        "equipment": _tools.ROList([[80111001, 2, 3], [80411001, 2, 3], [80691001, 2, 3]]),
        "props": None
    }),
    100148: _tools.RODict({
        "ID": 100148,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.003}),
        "equipment": _tools.ROList([[80111001, 3, 3], [80411001, 3, 3], [80691001, 3, 3]]),
        "props": None
    }),
    100149: _tools.RODict({
        "ID": 100149,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.004}),
        "equipment": _tools.ROList([[80111001, 4, 3], [80411001, 4, 3], [80691001, 4, 3]]),
        "props": None
    }),
    100150: _tools.RODict({
        "ID": 100150,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.005}),
        "equipment": _tools.ROList([[80111001, 5, 3], [80411001, 5, 3], [80691001, 5, 3]]),
        "props": None
    }),
    100151: _tools.RODict({
        "ID": 100151,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.006}),
        "equipment": _tools.ROList([[80111001, 6, 3], [80411001, 6, 3], [80691001, 6, 3]]),
        "props": None
    }),
    100152: _tools.RODict({
        "ID": 100152,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0085}),
        "equipment": _tools.ROList([[80111001, 7, 3], [80411001, 7, 3], [80691001, 7, 3]]),
        "props": None
    }),
    100153: _tools.RODict({
        "ID": 100153,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0025}),
        "equipment": _tools.ROList([[80111001, 0, 4], [80411001, 0, 4], [80691001, 0, 4]]),
        "props": None
    }),
    100154: _tools.RODict({
        "ID": 100154,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.003}),
        "equipment": _tools.ROList([[80111001, 1, 4], [80411001, 1, 4], [80691001, 1, 4]]),
        "props": None
    }),
    100155: _tools.RODict({
        "ID": 100155,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.003}),
        "equipment": _tools.ROList([[80111001, 2, 4], [80411001, 2, 4], [80691001, 2, 4]]),
        "props": None
    }),
    100156: _tools.RODict({
        "ID": 100156,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0035}),
        "equipment": _tools.ROList([[80111001, 3, 4], [80411001, 3, 4], [80691001, 3, 4]]),
        "props": None
    }),
    100157: _tools.RODict({
        "ID": 100157,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0045}),
        "equipment": _tools.ROList([[80111001, 4, 4], [80411001, 4, 4], [80691001, 4, 4]]),
        "props": None
    }),
    100158: _tools.RODict({
        "ID": 100158,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0055}),
        "equipment": _tools.ROList([[80111001, 5, 4], [80411001, 5, 4], [80691001, 5, 4]]),
        "props": None
    }),
    100159: _tools.RODict({
        "ID": 100159,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0065}),
        "equipment": _tools.ROList([[80111001, 6, 4], [80411001, 6, 4], [80691001, 6, 4]]),
        "props": None
    }),
    100160: _tools.RODict({
        "ID": 100160,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.009}),
        "equipment": _tools.ROList([[80111001, 7, 4], [80411001, 7, 4], [80691001, 7, 4]]),
        "props": None
    }),
    100161: _tools.RODict({
        "ID": 100161,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.001}),
        "equipment": _tools.ROList([[80211001, 0, 1], [80811001, 0, 1], [80411001, 0, 1]]),
        "props": None
    }),
    100162: _tools.RODict({
        "ID": 100162,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.001}),
        "equipment": _tools.ROList([[80211001, 1, 1], [80811001, 1, 1], [80411001, 1, 1]]),
        "props": None
    }),
    100163: _tools.RODict({
        "ID": 100163,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80211001, 2, 1], [80811001, 2, 1], [80411001, 2, 1]]),
        "props": None
    }),
    100164: _tools.RODict({
        "ID": 100164,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.002}),
        "equipment": _tools.ROList([[80211001, 3, 1], [80811001, 3, 1], [80411001, 3, 1]]),
        "props": None
    }),
    100165: _tools.RODict({
        "ID": 100165,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.003}),
        "equipment": _tools.ROList([[80211001, 4, 1], [80811001, 4, 1], [80411001, 4, 1]]),
        "props": None
    }),
    100166: _tools.RODict({
        "ID": 100166,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.004}),
        "equipment": _tools.ROList([[80211001, 5, 1], [80811001, 5, 1], [80411001, 5, 1]]),
        "props": None
    }),
    100167: _tools.RODict({
        "ID": 100167,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.005}),
        "equipment": _tools.ROList([[80211001, 6, 1], [80811001, 6, 1], [80411001, 6, 1]]),
        "props": None
    }),
    100168: _tools.RODict({
        "ID": 100168,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0075}),
        "equipment": _tools.ROList([[80211001, 7, 1], [80811001, 7, 1], [80411001, 7, 1]]),
        "props": None
    }),
    100169: _tools.RODict({
        "ID": 100169,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80211001, 0, 2], [80811001, 0, 2], [80411001, 0, 2]]),
        "props": None
    }),
    100170: _tools.RODict({
        "ID": 100170,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80211001, 1, 2], [80811001, 1, 2], [80411001, 1, 2]]),
        "props": None
    }),
    100171: _tools.RODict({
        "ID": 100171,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.002}),
        "equipment": _tools.ROList([[80211001, 2, 2], [80811001, 2, 2], [80411001, 2, 2]]),
        "props": None
    }),
    100172: _tools.RODict({
        "ID": 100172,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80211001, 3, 2], [80811001, 3, 2], [80411001, 3, 2]]),
        "props": None
    }),
    100173: _tools.RODict({
        "ID": 100173,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0035}),
        "equipment": _tools.ROList([[80211001, 4, 2], [80811001, 4, 2], [80411001, 4, 2]]),
        "props": None
    }),
    100174: _tools.RODict({
        "ID": 100174,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0045}),
        "equipment": _tools.ROList([[80211001, 5, 2], [80811001, 5, 2], [80411001, 5, 2]]),
        "props": None
    }),
    100175: _tools.RODict({
        "ID": 100175,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0055}),
        "equipment": _tools.ROList([[80211001, 6, 2], [80811001, 6, 2], [80411001, 6, 2]]),
        "props": None
    }),
    100176: _tools.RODict({
        "ID": 100176,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.008}),
        "equipment": _tools.ROList([[80211001, 7, 2], [80811001, 7, 2], [80411001, 7, 2]]),
        "props": None
    }),
    100177: _tools.RODict({
        "ID": 100177,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.002}),
        "equipment": _tools.ROList([[80211001, 0, 3], [80811001, 0, 3], [80411001, 0, 3]]),
        "props": None
    }),
    100178: _tools.RODict({
        "ID": 100178,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80211001, 1, 3], [80811001, 1, 3], [80411001, 1, 3]]),
        "props": None
    }),
    100179: _tools.RODict({
        "ID": 100179,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80211001, 2, 3], [80811001, 2, 3], [80411001, 2, 3]]),
        "props": None
    }),
    100180: _tools.RODict({
        "ID": 100180,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.003}),
        "equipment": _tools.ROList([[80211001, 3, 3], [80811001, 3, 3], [80411001, 3, 3]]),
        "props": None
    }),
    100181: _tools.RODict({
        "ID": 100181,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.004}),
        "equipment": _tools.ROList([[80211001, 4, 3], [80811001, 4, 3], [80411001, 4, 3]]),
        "props": None
    }),
    100182: _tools.RODict({
        "ID": 100182,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.005}),
        "equipment": _tools.ROList([[80211001, 5, 3], [80811001, 5, 3], [80411001, 5, 3]]),
        "props": None
    }),
    100183: _tools.RODict({
        "ID": 100183,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.006}),
        "equipment": _tools.ROList([[80211001, 6, 3], [80811001, 6, 3], [80411001, 6, 3]]),
        "props": None
    }),
    100184: _tools.RODict({
        "ID": 100184,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0085}),
        "equipment": _tools.ROList([[80211001, 7, 3], [80811001, 7, 3], [80411001, 7, 3]]),
        "props": None
    }),
    100185: _tools.RODict({
        "ID": 100185,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80211001, 0, 4], [80811001, 0, 4], [80411001, 0, 4]]),
        "props": None
    }),
    100186: _tools.RODict({
        "ID": 100186,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.003}),
        "equipment": _tools.ROList([[80211001, 1, 4], [80811001, 1, 4], [80411001, 1, 4]]),
        "props": None
    }),
    100187: _tools.RODict({
        "ID": 100187,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.003}),
        "equipment": _tools.ROList([[80211001, 2, 4], [80811001, 2, 4], [80411001, 2, 4]]),
        "props": None
    }),
    100188: _tools.RODict({
        "ID": 100188,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0035}),
        "equipment": _tools.ROList([[80211001, 3, 4], [80811001, 3, 4], [80411001, 3, 4]]),
        "props": None
    }),
    100189: _tools.RODict({
        "ID": 100189,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0045}),
        "equipment": _tools.ROList([[80211001, 4, 4], [80811001, 4, 4], [80411001, 4, 4]]),
        "props": None
    }),
    100190: _tools.RODict({
        "ID": 100190,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0055}),
        "equipment": _tools.ROList([[80211001, 5, 4], [80811001, 5, 4], [80411001, 5, 4]]),
        "props": None
    }),
    100191: _tools.RODict({
        "ID": 100191,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0065}),
        "equipment": _tools.ROList([[80211001, 6, 4], [80811001, 6, 4], [80411001, 6, 4]]),
        "props": None
    }),
    100192: _tools.RODict({
        "ID": 100192,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.009}),
        "equipment": _tools.ROList([[80211001, 7, 4], [80811001, 7, 4], [80411001, 7, 4]]),
        "props": None
    }),
    100193: _tools.RODict({
        "ID": 100193,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.001}),
        "equipment": _tools.ROList([[80311001, 0, 1], [80811001, 0, 1], [80411001, 0, 1]]),
        "props": None
    }),
    100194: _tools.RODict({
        "ID": 100194,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.001}),
        "equipment": _tools.ROList([[80311001, 1, 1], [80811001, 1, 1], [80411001, 1, 1]]),
        "props": None
    }),
    100195: _tools.RODict({
        "ID": 100195,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80311001, 2, 1], [80811001, 2, 1], [80411001, 2, 1]]),
        "props": None
    }),
    100196: _tools.RODict({
        "ID": 100196,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.002}),
        "equipment": _tools.ROList([[80311001, 3, 1], [80811001, 3, 1], [80411001, 3, 1]]),
        "props": None
    }),
    100197: _tools.RODict({
        "ID": 100197,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.003}),
        "equipment": _tools.ROList([[80311001, 4, 1], [80811001, 4, 1], [80411001, 4, 1]]),
        "props": None
    }),
    100198: _tools.RODict({
        "ID": 100198,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.004}),
        "equipment": _tools.ROList([[80311001, 5, 1], [80811001, 5, 1], [80411001, 5, 1]]),
        "props": None
    }),
    100199: _tools.RODict({
        "ID": 100199,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.005}),
        "equipment": _tools.ROList([[80311001, 6, 1], [80811001, 6, 1], [80411001, 6, 1]]),
        "props": None
    }),
    100200: _tools.RODict({
        "ID": 100200,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0075}),
        "equipment": _tools.ROList([[80311001, 7, 1], [80811001, 7, 1], [80411001, 7, 1]]),
        "props": None
    }),
    100201: _tools.RODict({
        "ID": 100201,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80311001, 0, 2], [80811001, 0, 2], [80411001, 0, 2]]),
        "props": None
    }),
    100202: _tools.RODict({
        "ID": 100202,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80311001, 1, 2], [80811001, 1, 2], [80411001, 1, 2]]),
        "props": None
    }),
    100203: _tools.RODict({
        "ID": 100203,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.002}),
        "equipment": _tools.ROList([[80311001, 2, 2], [80811001, 2, 2], [80411001, 2, 2]]),
        "props": None
    }),
    100204: _tools.RODict({
        "ID": 100204,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80311001, 3, 2], [80811001, 3, 2], [80411001, 3, 2]]),
        "props": None
    }),
    100205: _tools.RODict({
        "ID": 100205,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0035}),
        "equipment": _tools.ROList([[80311001, 4, 2], [80811001, 4, 2], [80411001, 4, 2]]),
        "props": None
    }),
    100206: _tools.RODict({
        "ID": 100206,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0045}),
        "equipment": _tools.ROList([[80311001, 5, 2], [80811001, 5, 2], [80411001, 5, 2]]),
        "props": None
    }),
    100207: _tools.RODict({
        "ID": 100207,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0055}),
        "equipment": _tools.ROList([[80311001, 6, 2], [80811001, 6, 2], [80411001, 6, 2]]),
        "props": None
    }),
    100208: _tools.RODict({
        "ID": 100208,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.008}),
        "equipment": _tools.ROList([[80311001, 7, 2], [80811001, 7, 2], [80411001, 7, 2]]),
        "props": None
    }),
    100209: _tools.RODict({
        "ID": 100209,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.002}),
        "equipment": _tools.ROList([[80311001, 0, 3], [80811001, 0, 3], [80411001, 0, 3]]),
        "props": None
    }),
    100210: _tools.RODict({
        "ID": 100210,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80311001, 1, 3], [80811001, 1, 3], [80411001, 1, 3]]),
        "props": None
    }),
    100211: _tools.RODict({
        "ID": 100211,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80311001, 2, 3], [80811001, 2, 3], [80411001, 2, 3]]),
        "props": None
    }),
    100212: _tools.RODict({
        "ID": 100212,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.003}),
        "equipment": _tools.ROList([[80311001, 3, 3], [80811001, 3, 3], [80411001, 3, 3]]),
        "props": None
    }),
    100213: _tools.RODict({
        "ID": 100213,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.004}),
        "equipment": _tools.ROList([[80311001, 4, 3], [80811001, 4, 3], [80411001, 4, 3]]),
        "props": None
    }),
    100214: _tools.RODict({
        "ID": 100214,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.005}),
        "equipment": _tools.ROList([[80311001, 5, 3], [80811001, 5, 3], [80411001, 5, 3]]),
        "props": None
    }),
    100215: _tools.RODict({
        "ID": 100215,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.006}),
        "equipment": _tools.ROList([[80311001, 6, 3], [80811001, 6, 3], [80411001, 6, 3]]),
        "props": None
    }),
    100216: _tools.RODict({
        "ID": 100216,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0085}),
        "equipment": _tools.ROList([[80311001, 7, 3], [80811001, 7, 3], [80411001, 7, 3]]),
        "props": None
    }),
    100217: _tools.RODict({
        "ID": 100217,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80311001, 0, 4], [80811001, 0, 4], [80411001, 0, 4]]),
        "props": None
    }),
    100218: _tools.RODict({
        "ID": 100218,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.003}),
        "equipment": _tools.ROList([[80311001, 1, 4], [80811001, 1, 4], [80411001, 1, 4]]),
        "props": None
    }),
    100219: _tools.RODict({
        "ID": 100219,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.003}),
        "equipment": _tools.ROList([[80311001, 2, 4], [80811001, 2, 4], [80411001, 2, 4]]),
        "props": None
    }),
    100220: _tools.RODict({
        "ID": 100220,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0035}),
        "equipment": _tools.ROList([[80311001, 3, 4], [80811001, 3, 4], [80411001, 3, 4]]),
        "props": None
    }),
    100221: _tools.RODict({
        "ID": 100221,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0045}),
        "equipment": _tools.ROList([[80311001, 4, 4], [80811001, 4, 4], [80411001, 4, 4]]),
        "props": None
    }),
    100222: _tools.RODict({
        "ID": 100222,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0055}),
        "equipment": _tools.ROList([[80311001, 5, 4], [80811001, 5, 4], [80411001, 5, 4]]),
        "props": None
    }),
    100223: _tools.RODict({
        "ID": 100223,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0065}),
        "equipment": _tools.ROList([[80311001, 6, 4], [80811001, 6, 4], [80411001, 6, 4]]),
        "props": None
    }),
    100224: _tools.RODict({
        "ID": 100224,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.009}),
        "equipment": _tools.ROList([[80311001, 7, 4], [80811001, 7, 4], [80411001, 7, 4]]),
        "props": None
    }),
    100225: _tools.RODict({
        "ID": 100225,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.001}),
        "equipment": _tools.ROList([[80811001, 0, 1], [80591001, 0, 1], [80791001, 0, 1]]),
        "props": None
    }),
    100226: _tools.RODict({
        "ID": 100226,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.001}),
        "equipment": _tools.ROList([[80811001, 1, 1], [80591001, 1, 1], [80791001, 1, 1]]),
        "props": None
    }),
    100227: _tools.RODict({
        "ID": 100227,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0015}),
        "equipment": _tools.ROList([[80811001, 2, 1], [80591001, 2, 1], [80791001, 2, 1]]),
        "props": None
    }),
    100228: _tools.RODict({
        "ID": 100228,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.002}),
        "equipment": _tools.ROList([[80811001, 3, 1], [80591001, 3, 1], [80791001, 3, 1]]),
        "props": None
    }),
    100229: _tools.RODict({
        "ID": 100229,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.003}),
        "equipment": _tools.ROList([[80811001, 4, 1], [80591001, 4, 1], [80791001, 4, 1]]),
        "props": None
    }),
    100230: _tools.RODict({
        "ID": 100230,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.004}),
        "equipment": _tools.ROList([[80811001, 5, 1], [80591001, 5, 1], [80791001, 5, 1]]),
        "props": None
    }),
    100231: _tools.RODict({
        "ID": 100231,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.005}),
        "equipment": _tools.ROList([[80811001, 6, 1], [80591001, 6, 1], [80791001, 6, 1]]),
        "props": None
    }),
    100232: _tools.RODict({
        "ID": 100232,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0075}),
        "equipment": _tools.ROList([[80811001, 7, 1], [80591001, 7, 1], [80791001, 7, 1]]),
        "props": None
    }),
    100233: _tools.RODict({
        "ID": 100233,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0015}),
        "equipment": _tools.ROList([[80811001, 0, 2], [80591001, 0, 2], [80791001, 0, 2]]),
        "props": None
    }),
    100234: _tools.RODict({
        "ID": 100234,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0015}),
        "equipment": _tools.ROList([[80811001, 1, 2], [80591001, 1, 2], [80791001, 1, 2]]),
        "props": None
    }),
    100235: _tools.RODict({
        "ID": 100235,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.002}),
        "equipment": _tools.ROList([[80811001, 2, 2], [80591001, 2, 2], [80791001, 2, 2]]),
        "props": None
    }),
    100236: _tools.RODict({
        "ID": 100236,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0025}),
        "equipment": _tools.ROList([[80811001, 3, 2], [80591001, 3, 2], [80791001, 3, 2]]),
        "props": None
    }),
    100237: _tools.RODict({
        "ID": 100237,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0035}),
        "equipment": _tools.ROList([[80811001, 4, 2], [80591001, 4, 2], [80791001, 4, 2]]),
        "props": None
    }),
    100238: _tools.RODict({
        "ID": 100238,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0045}),
        "equipment": _tools.ROList([[80811001, 5, 2], [80591001, 5, 2], [80791001, 5, 2]]),
        "props": None
    }),
    100239: _tools.RODict({
        "ID": 100239,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0055}),
        "equipment": _tools.ROList([[80811001, 6, 2], [80591001, 6, 2], [80791001, 6, 2]]),
        "props": None
    }),
    100240: _tools.RODict({
        "ID": 100240,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.008}),
        "equipment": _tools.ROList([[80811001, 7, 2], [80591001, 7, 2], [80791001, 7, 2]]),
        "props": None
    }),
    100241: _tools.RODict({
        "ID": 100241,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.002}),
        "equipment": _tools.ROList([[80811001, 0, 3], [80591001, 0, 3], [80791001, 0, 3]]),
        "props": None
    }),
    100242: _tools.RODict({
        "ID": 100242,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0025}),
        "equipment": _tools.ROList([[80811001, 1, 3], [80591001, 1, 3], [80791001, 1, 3]]),
        "props": None
    }),
    100243: _tools.RODict({
        "ID": 100243,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0025}),
        "equipment": _tools.ROList([[80811001, 2, 3], [80591001, 2, 3], [80791001, 2, 3]]),
        "props": None
    }),
    100244: _tools.RODict({
        "ID": 100244,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.003}),
        "equipment": _tools.ROList([[80811001, 3, 3], [80591001, 3, 3], [80791001, 3, 3]]),
        "props": None
    }),
    100245: _tools.RODict({
        "ID": 100245,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.004}),
        "equipment": _tools.ROList([[80811001, 4, 3], [80591001, 4, 3], [80791001, 4, 3]]),
        "props": None
    }),
    100246: _tools.RODict({
        "ID": 100246,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.005}),
        "equipment": _tools.ROList([[80811001, 5, 3], [80591001, 5, 3], [80791001, 5, 3]]),
        "props": None
    }),
    100247: _tools.RODict({
        "ID": 100247,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.006}),
        "equipment": _tools.ROList([[80811001, 6, 3], [80591001, 6, 3], [80791001, 6, 3]]),
        "props": None
    }),
    100248: _tools.RODict({
        "ID": 100248,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0085}),
        "equipment": _tools.ROList([[80811001, 7, 3], [80591001, 7, 3], [80791001, 7, 3]]),
        "props": None
    }),
    100249: _tools.RODict({
        "ID": 100249,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0025}),
        "equipment": _tools.ROList([[80811001, 0, 4], [80591001, 0, 4], [80791001, 0, 4]]),
        "props": None
    }),
    100250: _tools.RODict({
        "ID": 100250,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.003}),
        "equipment": _tools.ROList([[80811001, 1, 4], [80591001, 1, 4], [80791001, 1, 4]]),
        "props": None
    }),
    100251: _tools.RODict({
        "ID": 100251,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.003}),
        "equipment": _tools.ROList([[80811001, 2, 4], [80591001, 2, 4], [80791001, 2, 4]]),
        "props": None
    }),
    100252: _tools.RODict({
        "ID": 100252,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0035}),
        "equipment": _tools.ROList([[80811001, 3, 4], [80591001, 3, 4], [80791001, 3, 4]]),
        "props": None
    }),
    100253: _tools.RODict({
        "ID": 100253,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0045}),
        "equipment": _tools.ROList([[80811001, 4, 4], [80591001, 4, 4], [80791001, 4, 4]]),
        "props": None
    }),
    100254: _tools.RODict({
        "ID": 100254,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0055}),
        "equipment": _tools.ROList([[80811001, 5, 4], [80591001, 5, 4], [80791001, 5, 4]]),
        "props": None
    }),
    100255: _tools.RODict({
        "ID": 100255,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0065}),
        "equipment": _tools.ROList([[80811001, 6, 4], [80591001, 6, 4], [80791001, 6, 4]]),
        "props": None
    }),
    100256: _tools.RODict({
        "ID": 100256,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.009}),
        "equipment": _tools.ROList([[80811001, 7, 4], [80591001, 7, 4], [80791001, 7, 4]]),
        "props": None
    }),
    100257: _tools.RODict({
        "ID": 100257,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMortal":0.002}),
        "equipment": _tools.ROList([[80311001, 0, 1], [80811001, 0, 1], [80411001, 0, 1]]),
        "props": None
    }),
    100258: _tools.RODict({
        "ID": 100258,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMortal":0.002}),
        "equipment": _tools.ROList([[80311001, 1, 1], [80811001, 1, 1], [80411001, 1, 1]]),
        "props": None
    }),
    100259: _tools.RODict({
        "ID": 100259,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMortal":0.003}),
        "equipment": _tools.ROList([[80311001, 2, 1], [80811001, 2, 1], [80411001, 2, 1]]),
        "props": None
    }),
    100260: _tools.RODict({
        "ID": 100260,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMortal":0.004}),
        "equipment": _tools.ROList([[80311001, 3, 1], [80811001, 3, 1], [80411001, 3, 1]]),
        "props": None
    }),
    100261: _tools.RODict({
        "ID": 100261,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMortal":0.006}),
        "equipment": _tools.ROList([[80311001, 4, 1], [80811001, 4, 1], [80411001, 4, 1]]),
        "props": None
    }),
    100262: _tools.RODict({
        "ID": 100262,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMortal":0.008}),
        "equipment": _tools.ROList([[80311001, 5, 1], [80811001, 5, 1], [80411001, 5, 1]]),
        "props": None
    }),
    100263: _tools.RODict({
        "ID": 100263,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMortal":0.01}),
        "equipment": _tools.ROList([[80311001, 6, 1], [80811001, 6, 1], [80411001, 6, 1]]),
        "props": None
    }),
    100264: _tools.RODict({
        "ID": 100264,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMortal":0.015}),
        "equipment": _tools.ROList([[80311001, 7, 1], [80811001, 7, 1], [80411001, 7, 1]]),
        "props": None
    }),
    100265: _tools.RODict({
        "ID": 100265,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMortal":0.003}),
        "equipment": _tools.ROList([[80311001, 0, 2], [80811001, 0, 2], [80411001, 0, 2]]),
        "props": None
    }),
    100266: _tools.RODict({
        "ID": 100266,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMortal":0.003}),
        "equipment": _tools.ROList([[80311001, 1, 2], [80811001, 1, 2], [80411001, 1, 2]]),
        "props": None
    }),
    100267: _tools.RODict({
        "ID": 100267,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMortal":0.004}),
        "equipment": _tools.ROList([[80311001, 2, 2], [80811001, 2, 2], [80411001, 2, 2]]),
        "props": None
    }),
    100268: _tools.RODict({
        "ID": 100268,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMortal":0.005}),
        "equipment": _tools.ROList([[80311001, 3, 2], [80811001, 3, 2], [80411001, 3, 2]]),
        "props": None
    }),
    100269: _tools.RODict({
        "ID": 100269,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMortal":0.007}),
        "equipment": _tools.ROList([[80311001, 4, 2], [80811001, 4, 2], [80411001, 4, 2]]),
        "props": None
    }),
    100270: _tools.RODict({
        "ID": 100270,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMortal":0.009}),
        "equipment": _tools.ROList([[80311001, 5, 2], [80811001, 5, 2], [80411001, 5, 2]]),
        "props": None
    }),
    100271: _tools.RODict({
        "ID": 100271,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMortal":0.011}),
        "equipment": _tools.ROList([[80311001, 6, 2], [80811001, 6, 2], [80411001, 6, 2]]),
        "props": None
    }),
    100272: _tools.RODict({
        "ID": 100272,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMortal":0.016}),
        "equipment": _tools.ROList([[80311001, 7, 2], [80811001, 7, 2], [80411001, 7, 2]]),
        "props": None
    }),
    100273: _tools.RODict({
        "ID": 100273,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMortal":0.004}),
        "equipment": _tools.ROList([[80311001, 0, 3], [80811001, 0, 3], [80411001, 0, 3]]),
        "props": None
    }),
    100274: _tools.RODict({
        "ID": 100274,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMortal":0.005}),
        "equipment": _tools.ROList([[80311001, 1, 3], [80811001, 1, 3], [80411001, 1, 3]]),
        "props": None
    }),
    100275: _tools.RODict({
        "ID": 100275,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMortal":0.005}),
        "equipment": _tools.ROList([[80311001, 2, 3], [80811001, 2, 3], [80411001, 2, 3]]),
        "props": None
    }),
    100276: _tools.RODict({
        "ID": 100276,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMortal":0.006}),
        "equipment": _tools.ROList([[80311001, 3, 3], [80811001, 3, 3], [80411001, 3, 3]]),
        "props": None
    }),
    100277: _tools.RODict({
        "ID": 100277,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMortal":0.008}),
        "equipment": _tools.ROList([[80311001, 4, 3], [80811001, 4, 3], [80411001, 4, 3]]),
        "props": None
    }),
    100278: _tools.RODict({
        "ID": 100278,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMortal":0.01}),
        "equipment": _tools.ROList([[80311001, 5, 3], [80811001, 5, 3], [80411001, 5, 3]]),
        "props": None
    }),
    100279: _tools.RODict({
        "ID": 100279,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMortal":0.012}),
        "equipment": _tools.ROList([[80311001, 6, 3], [80811001, 6, 3], [80411001, 6, 3]]),
        "props": None
    }),
    100280: _tools.RODict({
        "ID": 100280,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMortal":0.017}),
        "equipment": _tools.ROList([[80311001, 7, 3], [80811001, 7, 3], [80411001, 7, 3]]),
        "props": None
    }),
    100281: _tools.RODict({
        "ID": 100281,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMortal":0.005}),
        "equipment": _tools.ROList([[80311001, 0, 4], [80811001, 0, 4], [80411001, 0, 4]]),
        "props": None
    }),
    100282: _tools.RODict({
        "ID": 100282,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMortal":0.006}),
        "equipment": _tools.ROList([[80311001, 1, 4], [80811001, 1, 4], [80411001, 1, 4]]),
        "props": None
    }),
    100283: _tools.RODict({
        "ID": 100283,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMortal":0.006}),
        "equipment": _tools.ROList([[80311001, 2, 4], [80811001, 2, 4], [80411001, 2, 4]]),
        "props": None
    }),
    100284: _tools.RODict({
        "ID": 100284,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMortal":0.007}),
        "equipment": _tools.ROList([[80311001, 3, 4], [80811001, 3, 4], [80411001, 3, 4]]),
        "props": None
    }),
    100285: _tools.RODict({
        "ID": 100285,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMortal":0.009}),
        "equipment": _tools.ROList([[80311001, 4, 4], [80811001, 4, 4], [80411001, 4, 4]]),
        "props": None
    }),
    100286: _tools.RODict({
        "ID": 100286,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMortal":0.011}),
        "equipment": _tools.ROList([[80311001, 5, 4], [80811001, 5, 4], [80411001, 5, 4]]),
        "props": None
    }),
    100287: _tools.RODict({
        "ID": 100287,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMortal":0.013}),
        "equipment": _tools.ROList([[80311001, 6, 4], [80811001, 6, 4], [80411001, 6, 4]]),
        "props": None
    }),
    100288: _tools.RODict({
        "ID": 100288,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjMortal":0.018}),
        "equipment": _tools.ROList([[80311001, 7, 4], [80811001, 7, 4], [80411001, 7, 4]]),
        "props": None
    }),
    100289: _tools.RODict({
        "ID": 100289,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.002}),
        "equipment": _tools.ROList([[80811001, 0, 1], [80591001, 0, 1], [80791001, 0, 1]]),
        "props": None
    }),
    100290: _tools.RODict({
        "ID": 100290,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.002}),
        "equipment": _tools.ROList([[80811001, 1, 1], [80591001, 1, 1], [80791001, 1, 1]]),
        "props": None
    }),
    100291: _tools.RODict({
        "ID": 100291,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.003}),
        "equipment": _tools.ROList([[80811001, 2, 1], [80591001, 2, 1], [80791001, 2, 1]]),
        "props": None
    }),
    100292: _tools.RODict({
        "ID": 100292,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.004}),
        "equipment": _tools.ROList([[80811001, 3, 1], [80591001, 3, 1], [80791001, 3, 1]]),
        "props": None
    }),
    100293: _tools.RODict({
        "ID": 100293,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.006}),
        "equipment": _tools.ROList([[80811001, 4, 1], [80591001, 4, 1], [80791001, 4, 1]]),
        "props": None
    }),
    100294: _tools.RODict({
        "ID": 100294,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.008}),
        "equipment": _tools.ROList([[80811001, 5, 1], [80591001, 5, 1], [80791001, 5, 1]]),
        "props": None
    }),
    100295: _tools.RODict({
        "ID": 100295,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.01}),
        "equipment": _tools.ROList([[80811001, 6, 1], [80591001, 6, 1], [80791001, 6, 1]]),
        "props": None
    }),
    100296: _tools.RODict({
        "ID": 100296,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.015}),
        "equipment": _tools.ROList([[80811001, 7, 1], [80591001, 7, 1], [80791001, 7, 1]]),
        "props": None
    }),
    100297: _tools.RODict({
        "ID": 100297,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.003}),
        "equipment": _tools.ROList([[80811001, 0, 2], [80591001, 0, 2], [80791001, 0, 2]]),
        "props": None
    }),
    100298: _tools.RODict({
        "ID": 100298,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.003}),
        "equipment": _tools.ROList([[80811001, 1, 2], [80591001, 1, 2], [80791001, 1, 2]]),
        "props": None
    }),
    100299: _tools.RODict({
        "ID": 100299,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.004}),
        "equipment": _tools.ROList([[80811001, 2, 2], [80591001, 2, 2], [80791001, 2, 2]]),
        "props": None
    }),
    100300: _tools.RODict({
        "ID": 100300,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.005}),
        "equipment": _tools.ROList([[80811001, 3, 2], [80591001, 3, 2], [80791001, 3, 2]]),
        "props": None
    }),
    100301: _tools.RODict({
        "ID": 100301,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.007}),
        "equipment": _tools.ROList([[80811001, 4, 2], [80591001, 4, 2], [80791001, 4, 2]]),
        "props": None
    }),
    100302: _tools.RODict({
        "ID": 100302,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.009}),
        "equipment": _tools.ROList([[80811001, 5, 2], [80591001, 5, 2], [80791001, 5, 2]]),
        "props": None
    }),
    100303: _tools.RODict({
        "ID": 100303,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.011}),
        "equipment": _tools.ROList([[80811001, 6, 2], [80591001, 6, 2], [80791001, 6, 2]]),
        "props": None
    }),
    100304: _tools.RODict({
        "ID": 100304,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.016}),
        "equipment": _tools.ROList([[80811001, 7, 2], [80591001, 7, 2], [80791001, 7, 2]]),
        "props": None
    }),
    100305: _tools.RODict({
        "ID": 100305,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.004}),
        "equipment": _tools.ROList([[80811001, 0, 3], [80591001, 0, 3], [80791001, 0, 3]]),
        "props": None
    }),
    100306: _tools.RODict({
        "ID": 100306,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.005}),
        "equipment": _tools.ROList([[80811001, 1, 3], [80591001, 1, 3], [80791001, 1, 3]]),
        "props": None
    }),
    100307: _tools.RODict({
        "ID": 100307,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.005}),
        "equipment": _tools.ROList([[80811001, 2, 3], [80591001, 2, 3], [80791001, 2, 3]]),
        "props": None
    }),
    100308: _tools.RODict({
        "ID": 100308,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.006}),
        "equipment": _tools.ROList([[80811001, 3, 3], [80591001, 3, 3], [80791001, 3, 3]]),
        "props": None
    }),
    100309: _tools.RODict({
        "ID": 100309,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.008}),
        "equipment": _tools.ROList([[80811001, 4, 3], [80591001, 4, 3], [80791001, 4, 3]]),
        "props": None
    }),
    100310: _tools.RODict({
        "ID": 100310,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.01}),
        "equipment": _tools.ROList([[80811001, 5, 3], [80591001, 5, 3], [80791001, 5, 3]]),
        "props": None
    }),
    100311: _tools.RODict({
        "ID": 100311,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.012}),
        "equipment": _tools.ROList([[80811001, 6, 3], [80591001, 6, 3], [80791001, 6, 3]]),
        "props": None
    }),
    100312: _tools.RODict({
        "ID": 100312,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.017}),
        "equipment": _tools.ROList([[80811001, 7, 3], [80591001, 7, 3], [80791001, 7, 3]]),
        "props": None
    }),
    100313: _tools.RODict({
        "ID": 100313,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.005}),
        "equipment": _tools.ROList([[80811001, 0, 4], [80591001, 0, 4], [80791001, 0, 4]]),
        "props": None
    }),
    100314: _tools.RODict({
        "ID": 100314,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.006}),
        "equipment": _tools.ROList([[80811001, 1, 4], [80591001, 1, 4], [80791001, 1, 4]]),
        "props": None
    }),
    100315: _tools.RODict({
        "ID": 100315,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.006}),
        "equipment": _tools.ROList([[80811001, 2, 4], [80591001, 2, 4], [80791001, 2, 4]]),
        "props": None
    }),
    100316: _tools.RODict({
        "ID": 100316,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.007}),
        "equipment": _tools.ROList([[80811001, 3, 4], [80591001, 3, 4], [80791001, 3, 4]]),
        "props": None
    }),
    100317: _tools.RODict({
        "ID": 100317,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.009}),
        "equipment": _tools.ROList([[80811001, 4, 4], [80591001, 4, 4], [80791001, 4, 4]]),
        "props": None
    }),
    100318: _tools.RODict({
        "ID": 100318,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.011}),
        "equipment": _tools.ROList([[80811001, 5, 4], [80591001, 5, 4], [80791001, 5, 4]]),
        "props": None
    }),
    100319: _tools.RODict({
        "ID": 100319,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.013}),
        "equipment": _tools.ROList([[80811001, 6, 4], [80591001, 6, 4], [80791001, 6, 4]]),
        "props": None
    }),
    100320: _tools.RODict({
        "ID": 100320,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.018}),
        "equipment": _tools.ROList([[80811001, 7, 4], [80591001, 7, 4], [80791001, 7, 4]]),
        "props": None
    }),
    100321: _tools.RODict({
        "ID": 100321,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80111001, 4, 1], [80311001, 4, 1], [80591001, 4, 1]]),
        "props": None
    }),
    100322: _tools.RODict({
        "ID": 100322,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80111001, 5, 1], [80311001, 5, 1], [80591001, 5, 1]]),
        "props": None
    }),
    100323: _tools.RODict({
        "ID": 100323,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80111001, 6, 1], [80311001, 6, 1], [80591001, 6, 1]]),
        "props": None
    }),
    100324: _tools.RODict({
        "ID": 100324,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80111001, 4, 2], [80311001, 4, 2], [80591001, 4, 2]]),
        "props": None
    }),
    100325: _tools.RODict({
        "ID": 100325,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80111001, 5, 2], [80311001, 5, 2], [80591001, 5, 2]]),
        "props": None
    }),
    100326: _tools.RODict({
        "ID": 100326,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80111001, 6, 2], [80311001, 6, 2], [80591001, 6, 2]]),
        "props": None
    }),
    100327: _tools.RODict({
        "ID": 100327,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80111001, 7, 2], [80311001, 7, 2], [80591001, 7, 2]]),
        "props": None
    }),
    100328: _tools.RODict({
        "ID": 100328,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80111001, 4, 3], [80311001, 4, 3], [80591001, 4, 3]]),
        "props": None
    }),
    100329: _tools.RODict({
        "ID": 100329,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80111001, 5, 3], [80311001, 5, 3], [80591001, 5, 3]]),
        "props": None
    }),
    100330: _tools.RODict({
        "ID": 100330,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80111001, 6, 3], [80311001, 6, 3], [80591001, 6, 3]]),
        "props": None
    }),
    100331: _tools.RODict({
        "ID": 100331,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80111001, 7, 3], [80311001, 7, 3], [80591001, 7, 3]]),
        "props": None
    }),
    100332: _tools.RODict({
        "ID": 100332,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80111001, 4, 4], [80311001, 4, 4], [80591001, 4, 4]]),
        "props": None
    }),
    100333: _tools.RODict({
        "ID": 100333,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80111001, 5, 4], [80311001, 5, 4], [80591001, 5, 4]]),
        "props": None
    }),
    100334: _tools.RODict({
        "ID": 100334,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80111001, 6, 4], [80311001, 6, 4], [80591001, 6, 4]]),
        "props": None
    }),
    100335: _tools.RODict({
        "ID": 100335,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80111001, 7, 4], [80311001, 7, 4], [80591001, 7, 4]]),
        "props": None
    }),
    100336: _tools.RODict({
        "ID": 100336,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80211001, 4, 1], [80311001, 4, 1], [80411001, 4, 1]]),
        "props": None
    }),
    100337: _tools.RODict({
        "ID": 100337,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80211001, 5, 1], [80311001, 5, 1], [80411001, 5, 1]]),
        "props": None
    }),
    100338: _tools.RODict({
        "ID": 100338,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80211001, 6, 1], [80311001, 6, 1], [80411001, 6, 1]]),
        "props": None
    }),
    100339: _tools.RODict({
        "ID": 100339,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80211001, 4, 2], [80311001, 4, 2], [80411001, 4, 2]]),
        "props": None
    }),
    100340: _tools.RODict({
        "ID": 100340,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80211001, 5, 2], [80311001, 5, 2], [80411001, 5, 2]]),
        "props": None
    }),
    100341: _tools.RODict({
        "ID": 100341,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80211001, 6, 2], [80311001, 6, 2], [80411001, 6, 2]]),
        "props": None
    }),
    100342: _tools.RODict({
        "ID": 100342,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80211001, 7, 2], [80311001, 7, 2], [80411001, 7, 2]]),
        "props": None
    }),
    100343: _tools.RODict({
        "ID": 100343,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80211001, 4, 3], [80311001, 4, 3], [80411001, 4, 3]]),
        "props": None
    }),
    100344: _tools.RODict({
        "ID": 100344,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80211001, 5, 3], [80311001, 5, 3], [80411001, 5, 3]]),
        "props": None
    }),
    100345: _tools.RODict({
        "ID": 100345,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80211001, 6, 3], [80311001, 6, 3], [80411001, 6, 3]]),
        "props": None
    }),
    100346: _tools.RODict({
        "ID": 100346,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80211001, 7, 3], [80311001, 7, 3], [80411001, 7, 3]]),
        "props": None
    }),
    100347: _tools.RODict({
        "ID": 100347,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80211001, 4, 4], [80311001, 4, 4], [80411001, 4, 4]]),
        "props": None
    }),
    100348: _tools.RODict({
        "ID": 100348,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80211001, 5, 4], [80311001, 5, 4], [80411001, 5, 4]]),
        "props": None
    }),
    100349: _tools.RODict({
        "ID": 100349,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80211001, 6, 4], [80311001, 6, 4], [80411001, 6, 4]]),
        "props": None
    }),
    100350: _tools.RODict({
        "ID": 100350,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80211001, 7, 4], [80311001, 7, 4], [80411001, 7, 4]]),
        "props": None
    }),
    100351: _tools.RODict({
        "ID": 100351,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80311001, 4, 1], [80691001, 4, 1], [80791001, 4, 1]]),
        "props": None
    }),
    100352: _tools.RODict({
        "ID": 100352,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80311001, 5, 1], [80691001, 5, 1], [80791001, 5, 1]]),
        "props": None
    }),
    100353: _tools.RODict({
        "ID": 100353,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80311001, 6, 1], [80691001, 6, 1], [80791001, 6, 1]]),
        "props": None
    }),
    100354: _tools.RODict({
        "ID": 100354,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80311001, 4, 2], [80691001, 4, 2], [80791001, 4, 2]]),
        "props": None
    }),
    100355: _tools.RODict({
        "ID": 100355,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80311001, 5, 2], [80691001, 5, 2], [80791001, 5, 2]]),
        "props": None
    }),
    100356: _tools.RODict({
        "ID": 100356,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80311001, 6, 2], [80691001, 6, 2], [80791001, 6, 2]]),
        "props": None
    }),
    100357: _tools.RODict({
        "ID": 100357,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80311001, 7, 2], [80691001, 7, 2], [80791001, 7, 2]]),
        "props": None
    }),
    100358: _tools.RODict({
        "ID": 100358,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80311001, 4, 3], [80691001, 4, 3], [80791001, 4, 3]]),
        "props": None
    }),
    100359: _tools.RODict({
        "ID": 100359,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80311001, 5, 3], [80691001, 5, 3], [80791001, 5, 3]]),
        "props": None
    }),
    100360: _tools.RODict({
        "ID": 100360,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80311001, 6, 3], [80691001, 6, 3], [80791001, 6, 3]]),
        "props": None
    }),
    100361: _tools.RODict({
        "ID": 100361,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80311001, 7, 3], [80691001, 7, 3], [80791001, 7, 3]]),
        "props": None
    }),
    100362: _tools.RODict({
        "ID": 100362,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80311001, 4, 4], [80691001, 4, 4], [80791001, 4, 4]]),
        "props": None
    }),
    100363: _tools.RODict({
        "ID": 100363,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80311001, 5, 4], [80691001, 5, 4], [80791001, 5, 4]]),
        "props": None
    }),
    100364: _tools.RODict({
        "ID": 100364,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80311001, 6, 4], [80691001, 6, 4], [80791001, 6, 4]]),
        "props": None
    }),
    100365: _tools.RODict({
        "ID": 100365,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80311001, 7, 4], [80691001, 7, 4], [80791001, 7, 4]]),
        "props": None
    }),
    100366: _tools.RODict({
        "ID": 100366,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80211001, 4, 1], [80411001, 4, 1], [80691001, 4, 1]]),
        "props": None
    }),
    100367: _tools.RODict({
        "ID": 100367,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80211001, 5, 1], [80411001, 5, 1], [80691001, 5, 1]]),
        "props": None
    }),
    100368: _tools.RODict({
        "ID": 100368,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80211001, 6, 1], [80411001, 6, 1], [80691001, 6, 1]]),
        "props": None
    }),
    100369: _tools.RODict({
        "ID": 100369,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80211001, 4, 2], [80411001, 4, 2], [80691001, 4, 2]]),
        "props": None
    }),
    100370: _tools.RODict({
        "ID": 100370,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80211001, 5, 2], [80411001, 5, 2], [80691001, 5, 2]]),
        "props": None
    }),
    100371: _tools.RODict({
        "ID": 100371,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80211001, 6, 2], [80411001, 6, 2], [80691001, 6, 2]]),
        "props": None
    }),
    100372: _tools.RODict({
        "ID": 100372,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80211001, 7, 2], [80411001, 7, 2], [80691001, 7, 2]]),
        "props": None
    }),
    100373: _tools.RODict({
        "ID": 100373,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80211001, 4, 3], [80411001, 4, 3], [80691001, 4, 3]]),
        "props": None
    }),
    100374: _tools.RODict({
        "ID": 100374,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80211001, 5, 3], [80411001, 5, 3], [80691001, 5, 3]]),
        "props": None
    }),
    100375: _tools.RODict({
        "ID": 100375,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80211001, 6, 3], [80411001, 6, 3], [80691001, 6, 3]]),
        "props": None
    }),
    100376: _tools.RODict({
        "ID": 100376,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80211001, 7, 3], [80411001, 7, 3], [80691001, 7, 3]]),
        "props": None
    }),
    100377: _tools.RODict({
        "ID": 100377,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80211001, 4, 4], [80411001, 4, 4], [80691001, 4, 4]]),
        "props": None
    }),
    100378: _tools.RODict({
        "ID": 100378,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80211001, 5, 4], [80411001, 5, 4], [80691001, 5, 4]]),
        "props": None
    }),
    100379: _tools.RODict({
        "ID": 100379,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80211001, 6, 4], [80411001, 6, 4], [80691001, 6, 4]]),
        "props": None
    }),
    100380: _tools.RODict({
        "ID": 100380,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80211001, 7, 4], [80411001, 7, 4], [80691001, 7, 4]]),
        "props": None
    }),
    100381: _tools.RODict({
        "ID": 100381,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80111001, 4, 1], [80411001, 4, 1], [80791001, 4, 1]]),
        "props": None
    }),
    100382: _tools.RODict({
        "ID": 100382,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80111001, 5, 1], [80411001, 5, 1], [80791001, 5, 1]]),
        "props": None
    }),
    100383: _tools.RODict({
        "ID": 100383,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80111001, 6, 1], [80411001, 6, 1], [80791001, 6, 1]]),
        "props": None
    }),
    100384: _tools.RODict({
        "ID": 100384,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80111001, 4, 2], [80411001, 4, 2], [80791001, 4, 2]]),
        "props": None
    }),
    100385: _tools.RODict({
        "ID": 100385,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80111001, 5, 2], [80411001, 5, 2], [80791001, 5, 2]]),
        "props": None
    }),
    100386: _tools.RODict({
        "ID": 100386,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80111001, 6, 2], [80411001, 6, 2], [80791001, 6, 2]]),
        "props": None
    }),
    100387: _tools.RODict({
        "ID": 100387,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80111001, 7, 2], [80411001, 7, 2], [80791001, 7, 2]]),
        "props": None
    }),
    100388: _tools.RODict({
        "ID": 100388,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80111001, 4, 3], [80411001, 4, 3], [80791001, 4, 3]]),
        "props": None
    }),
    100389: _tools.RODict({
        "ID": 100389,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80111001, 5, 3], [80411001, 5, 3], [80791001, 5, 3]]),
        "props": None
    }),
    100390: _tools.RODict({
        "ID": 100390,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80111001, 6, 3], [80411001, 6, 3], [80791001, 6, 3]]),
        "props": None
    }),
    100391: _tools.RODict({
        "ID": 100391,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80111001, 7, 3], [80411001, 7, 3], [80791001, 7, 3]]),
        "props": None
    }),
    100392: _tools.RODict({
        "ID": 100392,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80111001, 4, 4], [80411001, 4, 4], [80791001, 4, 4]]),
        "props": None
    }),
    100393: _tools.RODict({
        "ID": 100393,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80111001, 5, 4], [80411001, 5, 4], [80791001, 5, 4]]),
        "props": None
    }),
    100394: _tools.RODict({
        "ID": 100394,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80111001, 6, 4], [80411001, 6, 4], [80791001, 6, 4]]),
        "props": None
    }),
    100395: _tools.RODict({
        "ID": 100395,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80111001, 7, 4], [80411001, 7, 4], [80791001, 7, 4]]),
        "props": None
    }),
    100396: _tools.RODict({
        "ID": 100396,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80311001, 4, 1], [80811001, 4, 1], [80591001, 4, 1]]),
        "props": None
    }),
    100397: _tools.RODict({
        "ID": 100397,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80311001, 5, 1], [80811001, 5, 1], [80591001, 5, 1]]),
        "props": None
    }),
    100398: _tools.RODict({
        "ID": 100398,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80311001, 6, 1], [80811001, 6, 1], [80591001, 6, 1]]),
        "props": None
    }),
    100399: _tools.RODict({
        "ID": 100399,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80311001, 4, 2], [80811001, 4, 2], [80591001, 4, 2]]),
        "props": None
    }),
    100400: _tools.RODict({
        "ID": 100400,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80311001, 5, 2], [80811001, 5, 2], [80591001, 5, 2]]),
        "props": None
    }),
    100401: _tools.RODict({
        "ID": 100401,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80311001, 6, 2], [80811001, 6, 2], [80591001, 6, 2]]),
        "props": None
    }),
    100402: _tools.RODict({
        "ID": 100402,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80311001, 7, 2], [80811001, 7, 2], [80591001, 7, 2]]),
        "props": None
    }),
    100403: _tools.RODict({
        "ID": 100403,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80311001, 4, 3], [80811001, 4, 3], [80591001, 4, 3]]),
        "props": None
    }),
    100404: _tools.RODict({
        "ID": 100404,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80311001, 5, 3], [80811001, 5, 3], [80591001, 5, 3]]),
        "props": None
    }),
    100405: _tools.RODict({
        "ID": 100405,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80311001, 6, 3], [80811001, 6, 3], [80591001, 6, 3]]),
        "props": None
    }),
    100406: _tools.RODict({
        "ID": 100406,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80311001, 7, 3], [80811001, 7, 3], [80591001, 7, 3]]),
        "props": None
    }),
    100407: _tools.RODict({
        "ID": 100407,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80311001, 4, 4], [80811001, 4, 4], [80591001, 4, 4]]),
        "props": None
    }),
    100408: _tools.RODict({
        "ID": 100408,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80311001, 5, 4], [80811001, 5, 4], [80591001, 5, 4]]),
        "props": None
    }),
    100409: _tools.RODict({
        "ID": 100409,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80311001, 6, 4], [80811001, 6, 4], [80591001, 6, 4]]),
        "props": None
    }),
    100410: _tools.RODict({
        "ID": 100410,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80311001, 7, 4], [80811001, 7, 4], [80591001, 7, 4]]),
        "props": None
    }),
    100411: _tools.RODict({
        "ID": 100411,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80111001, 3, 1], [80591001, 3, 1]]),
        "props": None
    }),
    100412: _tools.RODict({
        "ID": 100412,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80111001, 4, 1], [80591001, 4, 1]]),
        "props": None
    }),
    100413: _tools.RODict({
        "ID": 100413,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80111001, 5, 1], [80591001, 5, 1]]),
        "props": None
    }),
    100414: _tools.RODict({
        "ID": 100414,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80111001, 3, 2], [80591001, 3, 2]]),
        "props": None
    }),
    100415: _tools.RODict({
        "ID": 100415,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80111001, 4, 2], [80591001, 4, 2]]),
        "props": None
    }),
    100416: _tools.RODict({
        "ID": 100416,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80111001, 5, 2], [80591001, 5, 2]]),
        "props": None
    }),
    100417: _tools.RODict({
        "ID": 100417,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80111001, 6, 2], [80591001, 6, 2]]),
        "props": None
    }),
    100418: _tools.RODict({
        "ID": 100418,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80111001, 3, 3], [80591001, 3, 3]]),
        "props": None
    }),
    100419: _tools.RODict({
        "ID": 100419,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80111001, 4, 3], [80591001, 4, 3]]),
        "props": None
    }),
    100420: _tools.RODict({
        "ID": 100420,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80111001, 5, 3], [80591001, 5, 3]]),
        "props": None
    }),
    100421: _tools.RODict({
        "ID": 100421,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80111001, 6, 3], [80591001, 6, 3]]),
        "props": None
    }),
    100422: _tools.RODict({
        "ID": 100422,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80111001, 3, 4], [80591001, 3, 4]]),
        "props": None
    }),
    100423: _tools.RODict({
        "ID": 100423,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80111001, 4, 4], [80591001, 4, 4]]),
        "props": None
    }),
    100424: _tools.RODict({
        "ID": 100424,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80111001, 5, 4], [80591001, 5, 4]]),
        "props": None
    }),
    100425: _tools.RODict({
        "ID": 100425,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80111001, 6, 4], [80591001, 6, 4]]),
        "props": None
    }),
    100426: _tools.RODict({
        "ID": 100426,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80211001, 3, 1], [80311001, 3, 1]]),
        "props": None
    }),
    100427: _tools.RODict({
        "ID": 100427,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80211001, 4, 1], [80311001, 4, 1]]),
        "props": None
    }),
    100428: _tools.RODict({
        "ID": 100428,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80211001, 5, 1], [80311001, 5, 1]]),
        "props": None
    }),
    100429: _tools.RODict({
        "ID": 100429,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80211001, 3, 2], [80311001, 3, 2]]),
        "props": None
    }),
    100430: _tools.RODict({
        "ID": 100430,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80211001, 4, 2], [80311001, 4, 2]]),
        "props": None
    }),
    100431: _tools.RODict({
        "ID": 100431,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80211001, 5, 2], [80311001, 5, 2]]),
        "props": None
    }),
    100432: _tools.RODict({
        "ID": 100432,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80211001, 6, 2], [80311001, 6, 2]]),
        "props": None
    }),
    100433: _tools.RODict({
        "ID": 100433,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80211001, 3, 3], [80311001, 3, 3]]),
        "props": None
    }),
    100434: _tools.RODict({
        "ID": 100434,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80211001, 4, 3], [80311001, 4, 3]]),
        "props": None
    }),
    100435: _tools.RODict({
        "ID": 100435,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80211001, 5, 3], [80311001, 5, 3]]),
        "props": None
    }),
    100436: _tools.RODict({
        "ID": 100436,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80211001, 6, 3], [80311001, 6, 3]]),
        "props": None
    }),
    100437: _tools.RODict({
        "ID": 100437,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80211001, 3, 4], [80311001, 3, 4]]),
        "props": None
    }),
    100438: _tools.RODict({
        "ID": 100438,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80211001, 4, 4], [80311001, 4, 4]]),
        "props": None
    }),
    100439: _tools.RODict({
        "ID": 100439,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80211001, 5, 4], [80311001, 5, 4]]),
        "props": None
    }),
    100440: _tools.RODict({
        "ID": 100440,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80211001, 6, 4], [80311001, 6, 4]]),
        "props": None
    }),
    100441: _tools.RODict({
        "ID": 100441,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80691001, 3, 1], [80791001, 3, 1]]),
        "props": None
    }),
    100442: _tools.RODict({
        "ID": 100442,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80691001, 4, 1], [80791001, 4, 1]]),
        "props": None
    }),
    100443: _tools.RODict({
        "ID": 100443,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80691001, 5, 1], [80791001, 5, 1]]),
        "props": None
    }),
    100444: _tools.RODict({
        "ID": 100444,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80691001, 3, 2], [80791001, 3, 2]]),
        "props": None
    }),
    100445: _tools.RODict({
        "ID": 100445,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80691001, 4, 2], [80791001, 4, 2]]),
        "props": None
    }),
    100446: _tools.RODict({
        "ID": 100446,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80691001, 5, 2], [80791001, 5, 2]]),
        "props": None
    }),
    100447: _tools.RODict({
        "ID": 100447,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80691001, 6, 2], [80791001, 6, 2]]),
        "props": None
    }),
    100448: _tools.RODict({
        "ID": 100448,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80691001, 3, 3], [80791001, 3, 3]]),
        "props": None
    }),
    100449: _tools.RODict({
        "ID": 100449,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80691001, 4, 3], [80791001, 4, 3]]),
        "props": None
    }),
    100450: _tools.RODict({
        "ID": 100450,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80691001, 5, 3], [80791001, 5, 3]]),
        "props": None
    }),
    100451: _tools.RODict({
        "ID": 100451,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80691001, 6, 3], [80791001, 6, 3]]),
        "props": None
    }),
    100452: _tools.RODict({
        "ID": 100452,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80691001, 3, 4], [80791001, 3, 4]]),
        "props": None
    }),
    100453: _tools.RODict({
        "ID": 100453,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80691001, 4, 4], [80791001, 4, 4]]),
        "props": None
    }),
    100454: _tools.RODict({
        "ID": 100454,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80691001, 5, 4], [80791001, 5, 4]]),
        "props": None
    }),
    100455: _tools.RODict({
        "ID": 100455,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80691001, 6, 4], [80791001, 6, 4]]),
        "props": None
    }),
    100456: _tools.RODict({
        "ID": 100456,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80811001, 3, 1], [80411001, 3, 1]]),
        "props": None
    }),
    100457: _tools.RODict({
        "ID": 100457,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80811001, 4, 1], [80411001, 4, 1]]),
        "props": None
    }),
    100458: _tools.RODict({
        "ID": 100458,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80811001, 5, 1], [80411001, 5, 1]]),
        "props": None
    }),
    100459: _tools.RODict({
        "ID": 100459,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80811001, 3, 2], [80411001, 3, 2]]),
        "props": None
    }),
    100460: _tools.RODict({
        "ID": 100460,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80811001, 4, 2], [80411001, 4, 2]]),
        "props": None
    }),
    100461: _tools.RODict({
        "ID": 100461,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80811001, 5, 2], [80411001, 5, 2]]),
        "props": None
    }),
    100462: _tools.RODict({
        "ID": 100462,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80811001, 6, 2], [80411001, 6, 2]]),
        "props": None
    }),
    100463: _tools.RODict({
        "ID": 100463,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80811001, 3, 3], [80411001, 3, 3]]),
        "props": None
    }),
    100464: _tools.RODict({
        "ID": 100464,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80811001, 4, 3], [80411001, 4, 3]]),
        "props": None
    }),
    100465: _tools.RODict({
        "ID": 100465,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80811001, 5, 3], [80411001, 5, 3]]),
        "props": None
    }),
    100466: _tools.RODict({
        "ID": 100466,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80811001, 6, 3], [80411001, 6, 3]]),
        "props": None
    }),
    100467: _tools.RODict({
        "ID": 100467,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80811001, 3, 4], [80411001, 3, 4]]),
        "props": None
    }),
    100468: _tools.RODict({
        "ID": 100468,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80811001, 4, 4], [80411001, 4, 4]]),
        "props": None
    }),
    100469: _tools.RODict({
        "ID": 100469,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80811001, 5, 4], [80411001, 5, 4]]),
        "props": None
    }),
    100470: _tools.RODict({
        "ID": 100470,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80811001, 6, 4], [80411001, 6, 4]]),
        "props": None
    }),
    100471: _tools.RODict({
        "ID": 100471,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80111001, 3, 1], [80691001, 3, 1]]),
        "props": None
    }),
    100472: _tools.RODict({
        "ID": 100472,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80111001, 4, 1], [80691001, 4, 1]]),
        "props": None
    }),
    100473: _tools.RODict({
        "ID": 100473,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80111001, 5, 1], [80691001, 5, 1]]),
        "props": None
    }),
    100474: _tools.RODict({
        "ID": 100474,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80111001, 3, 2], [80691001, 3, 2]]),
        "props": None
    }),
    100475: _tools.RODict({
        "ID": 100475,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80111001, 4, 2], [80691001, 4, 2]]),
        "props": None
    }),
    100476: _tools.RODict({
        "ID": 100476,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80111001, 5, 2], [80691001, 5, 2]]),
        "props": None
    }),
    100477: _tools.RODict({
        "ID": 100477,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80111001, 6, 2], [80691001, 6, 2]]),
        "props": None
    }),
    100478: _tools.RODict({
        "ID": 100478,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80111001, 3, 3], [80691001, 3, 3]]),
        "props": None
    }),
    100479: _tools.RODict({
        "ID": 100479,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80111001, 4, 3], [80691001, 4, 3]]),
        "props": None
    }),
    100480: _tools.RODict({
        "ID": 100480,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80111001, 5, 3], [80691001, 5, 3]]),
        "props": None
    }),
    100481: _tools.RODict({
        "ID": 100481,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80111001, 6, 3], [80691001, 6, 3]]),
        "props": None
    }),
    100482: _tools.RODict({
        "ID": 100482,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80111001, 3, 4], [80691001, 3, 4]]),
        "props": None
    }),
    100483: _tools.RODict({
        "ID": 100483,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80111001, 4, 4], [80691001, 4, 4]]),
        "props": None
    }),
    100484: _tools.RODict({
        "ID": 100484,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80111001, 5, 4], [80691001, 5, 4]]),
        "props": None
    }),
    100485: _tools.RODict({
        "ID": 100485,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80111001, 6, 4], [80691001, 6, 4]]),
        "props": None
    }),
    100486: _tools.RODict({
        "ID": 100486,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80211001, 3, 1], [80811001, 3, 1]]),
        "props": None
    }),
    100487: _tools.RODict({
        "ID": 100487,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80211001, 4, 1], [80811001, 4, 1]]),
        "props": None
    }),
    100488: _tools.RODict({
        "ID": 100488,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80211001, 5, 1], [80811001, 5, 1]]),
        "props": None
    }),
    100489: _tools.RODict({
        "ID": 100489,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80211001, 3, 2], [80811001, 3, 2]]),
        "props": None
    }),
    100490: _tools.RODict({
        "ID": 100490,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80211001, 4, 2], [80811001, 4, 2]]),
        "props": None
    }),
    100491: _tools.RODict({
        "ID": 100491,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80211001, 5, 2], [80811001, 5, 2]]),
        "props": None
    }),
    100492: _tools.RODict({
        "ID": 100492,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80211001, 6, 2], [80811001, 6, 2]]),
        "props": None
    }),
    100493: _tools.RODict({
        "ID": 100493,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80211001, 3, 3], [80811001, 3, 3]]),
        "props": None
    }),
    100494: _tools.RODict({
        "ID": 100494,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80211001, 4, 3], [80811001, 4, 3]]),
        "props": None
    }),
    100495: _tools.RODict({
        "ID": 100495,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80211001, 5, 3], [80811001, 5, 3]]),
        "props": None
    }),
    100496: _tools.RODict({
        "ID": 100496,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80211001, 6, 3], [80811001, 6, 3]]),
        "props": None
    }),
    100497: _tools.RODict({
        "ID": 100497,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80211001, 3, 4], [80811001, 3, 4]]),
        "props": None
    }),
    100498: _tools.RODict({
        "ID": 100498,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80211001, 4, 4], [80811001, 4, 4]]),
        "props": None
    }),
    100499: _tools.RODict({
        "ID": 100499,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80211001, 5, 4], [80811001, 5, 4]]),
        "props": None
    }),
    100500: _tools.RODict({
        "ID": 100500,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80211001, 6, 4], [80811001, 6, 4]]),
        "props": None
    }),
    100501: _tools.RODict({
        "ID": 100501,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80591001, 3, 1], [80791001, 3, 1]]),
        "props": None
    }),
    100502: _tools.RODict({
        "ID": 100502,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80591001, 4, 1], [80791001, 4, 1]]),
        "props": None
    }),
    100503: _tools.RODict({
        "ID": 100503,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80591001, 5, 1], [80791001, 5, 1]]),
        "props": None
    }),
    100504: _tools.RODict({
        "ID": 100504,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80591001, 3, 2], [80791001, 3, 2]]),
        "props": None
    }),
    100505: _tools.RODict({
        "ID": 100505,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80591001, 4, 2], [80791001, 4, 2]]),
        "props": None
    }),
    100506: _tools.RODict({
        "ID": 100506,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80591001, 5, 2], [80791001, 5, 2]]),
        "props": None
    }),
    100507: _tools.RODict({
        "ID": 100507,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80591001, 6, 2], [80791001, 6, 2]]),
        "props": None
    }),
    100508: _tools.RODict({
        "ID": 100508,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80591001, 3, 3], [80791001, 3, 3]]),
        "props": None
    }),
    100509: _tools.RODict({
        "ID": 100509,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80591001, 4, 3], [80791001, 4, 3]]),
        "props": None
    }),
    100510: _tools.RODict({
        "ID": 100510,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80591001, 5, 3], [80791001, 5, 3]]),
        "props": None
    }),
    100511: _tools.RODict({
        "ID": 100511,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80591001, 6, 3], [80791001, 6, 3]]),
        "props": None
    }),
    100512: _tools.RODict({
        "ID": 100512,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80591001, 3, 4], [80791001, 3, 4]]),
        "props": None
    }),
    100513: _tools.RODict({
        "ID": 100513,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80591001, 4, 4], [80791001, 4, 4]]),
        "props": None
    }),
    100514: _tools.RODict({
        "ID": 100514,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80591001, 5, 4], [80791001, 5, 4]]),
        "props": None
    }),
    100515: _tools.RODict({
        "ID": 100515,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80591001, 6, 4], [80791001, 6, 4]]),
        "props": None
    }),
    100516: _tools.RODict({
        "ID": 100516,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80311001, 3, 1], [80411001, 3, 1]]),
        "props": None
    }),
    100517: _tools.RODict({
        "ID": 100517,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80311001, 4, 1], [80411001, 4, 1]]),
        "props": None
    }),
    100518: _tools.RODict({
        "ID": 100518,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80311001, 5, 1], [80411001, 5, 1]]),
        "props": None
    }),
    100519: _tools.RODict({
        "ID": 100519,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80311001, 3, 2], [80411001, 3, 2]]),
        "props": None
    }),
    100520: _tools.RODict({
        "ID": 100520,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80311001, 4, 2], [80411001, 4, 2]]),
        "props": None
    }),
    100521: _tools.RODict({
        "ID": 100521,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80311001, 5, 2], [80411001, 5, 2]]),
        "props": None
    }),
    100522: _tools.RODict({
        "ID": 100522,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80311001, 6, 2], [80411001, 6, 2]]),
        "props": None
    }),
    100523: _tools.RODict({
        "ID": 100523,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80311001, 3, 3], [80411001, 3, 3]]),
        "props": None
    }),
    100524: _tools.RODict({
        "ID": 100524,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80311001, 4, 3], [80411001, 4, 3]]),
        "props": None
    }),
    100525: _tools.RODict({
        "ID": 100525,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80311001, 5, 3], [80411001, 5, 3]]),
        "props": None
    }),
    100526: _tools.RODict({
        "ID": 100526,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80311001, 6, 3], [80411001, 6, 3]]),
        "props": None
    }),
    100527: _tools.RODict({
        "ID": 100527,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80311001, 3, 4], [80411001, 3, 4]]),
        "props": None
    }),
    100528: _tools.RODict({
        "ID": 100528,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80311001, 4, 4], [80411001, 4, 4]]),
        "props": None
    }),
    100529: _tools.RODict({
        "ID": 100529,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80311001, 5, 4], [80411001, 5, 4]]),
        "props": None
    }),
    100530: _tools.RODict({
        "ID": 100530,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80311001, 6, 4], [80411001, 6, 4]]),
        "props": None
    }),
    100531: _tools.RODict({
        "ID": 100531,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80111001, 3, 1], [80791001, 3, 1]]),
        "props": None
    }),
    100532: _tools.RODict({
        "ID": 100532,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80111001, 4, 1], [80791001, 4, 1]]),
        "props": None
    }),
    100533: _tools.RODict({
        "ID": 100533,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80111001, 5, 1], [80791001, 5, 1]]),
        "props": None
    }),
    100534: _tools.RODict({
        "ID": 100534,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80111001, 3, 2], [80791001, 3, 2]]),
        "props": None
    }),
    100535: _tools.RODict({
        "ID": 100535,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80111001, 4, 2], [80791001, 4, 2]]),
        "props": None
    }),
    100536: _tools.RODict({
        "ID": 100536,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80111001, 5, 2], [80791001, 5, 2]]),
        "props": None
    }),
    100537: _tools.RODict({
        "ID": 100537,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80111001, 6, 2], [80791001, 6, 2]]),
        "props": None
    }),
    100538: _tools.RODict({
        "ID": 100538,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80111001, 3, 3], [80791001, 3, 3]]),
        "props": None
    }),
    100539: _tools.RODict({
        "ID": 100539,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80111001, 4, 3], [80791001, 4, 3]]),
        "props": None
    }),
    100540: _tools.RODict({
        "ID": 100540,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80111001, 5, 3], [80791001, 5, 3]]),
        "props": None
    }),
    100541: _tools.RODict({
        "ID": 100541,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80111001, 6, 3], [80791001, 6, 3]]),
        "props": None
    }),
    100542: _tools.RODict({
        "ID": 100542,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80111001, 3, 4], [80791001, 3, 4]]),
        "props": None
    }),
    100543: _tools.RODict({
        "ID": 100543,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80111001, 4, 4], [80791001, 4, 4]]),
        "props": None
    }),
    100544: _tools.RODict({
        "ID": 100544,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80111001, 5, 4], [80791001, 5, 4]]),
        "props": None
    }),
    100545: _tools.RODict({
        "ID": 100545,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80111001, 6, 4], [80791001, 6, 4]]),
        "props": None
    }),
    100546: _tools.RODict({
        "ID": 100546,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80211001, 3, 1], [80411001, 3, 1]]),
        "props": None
    }),
    100547: _tools.RODict({
        "ID": 100547,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80211001, 4, 1], [80411001, 4, 1]]),
        "props": None
    }),
    100548: _tools.RODict({
        "ID": 100548,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80211001, 5, 1], [80411001, 5, 1]]),
        "props": None
    }),
    100549: _tools.RODict({
        "ID": 100549,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80211001, 3, 2], [80411001, 3, 2]]),
        "props": None
    }),
    100550: _tools.RODict({
        "ID": 100550,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80211001, 4, 2], [80411001, 4, 2]]),
        "props": None
    }),
    100551: _tools.RODict({
        "ID": 100551,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80211001, 5, 2], [80411001, 5, 2]]),
        "props": None
    }),
    100552: _tools.RODict({
        "ID": 100552,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80211001, 6, 2], [80411001, 6, 2]]),
        "props": None
    }),
    100553: _tools.RODict({
        "ID": 100553,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80211001, 3, 3], [80411001, 3, 3]]),
        "props": None
    }),
    100554: _tools.RODict({
        "ID": 100554,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80211001, 4, 3], [80411001, 4, 3]]),
        "props": None
    }),
    100555: _tools.RODict({
        "ID": 100555,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80211001, 5, 3], [80411001, 5, 3]]),
        "props": None
    }),
    100556: _tools.RODict({
        "ID": 100556,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80211001, 6, 3], [80411001, 6, 3]]),
        "props": None
    }),
    100557: _tools.RODict({
        "ID": 100557,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80211001, 3, 4], [80411001, 3, 4]]),
        "props": None
    }),
    100558: _tools.RODict({
        "ID": 100558,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80211001, 4, 4], [80411001, 4, 4]]),
        "props": None
    }),
    100559: _tools.RODict({
        "ID": 100559,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80211001, 5, 4], [80411001, 5, 4]]),
        "props": None
    }),
    100560: _tools.RODict({
        "ID": 100560,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80211001, 6, 4], [80411001, 6, 4]]),
        "props": None
    }),
    100561: _tools.RODict({
        "ID": 100561,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80591001, 3, 1], [80691001, 3, 1]]),
        "props": None
    }),
    100562: _tools.RODict({
        "ID": 100562,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80591001, 4, 1], [80691001, 4, 1]]),
        "props": None
    }),
    100563: _tools.RODict({
        "ID": 100563,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80591001, 5, 1], [80691001, 5, 1]]),
        "props": None
    }),
    100564: _tools.RODict({
        "ID": 100564,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80591001, 3, 2], [80691001, 3, 2]]),
        "props": None
    }),
    100565: _tools.RODict({
        "ID": 100565,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80591001, 4, 2], [80691001, 4, 2]]),
        "props": None
    }),
    100566: _tools.RODict({
        "ID": 100566,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80591001, 5, 2], [80691001, 5, 2]]),
        "props": None
    }),
    100567: _tools.RODict({
        "ID": 100567,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80591001, 6, 2], [80691001, 6, 2]]),
        "props": None
    }),
    100568: _tools.RODict({
        "ID": 100568,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80591001, 3, 3], [80691001, 3, 3]]),
        "props": None
    }),
    100569: _tools.RODict({
        "ID": 100569,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80591001, 4, 3], [80691001, 4, 3]]),
        "props": None
    }),
    100570: _tools.RODict({
        "ID": 100570,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80591001, 5, 3], [80691001, 5, 3]]),
        "props": None
    }),
    100571: _tools.RODict({
        "ID": 100571,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80591001, 6, 3], [80691001, 6, 3]]),
        "props": None
    }),
    100572: _tools.RODict({
        "ID": 100572,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80591001, 3, 4], [80691001, 3, 4]]),
        "props": None
    }),
    100573: _tools.RODict({
        "ID": 100573,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80591001, 4, 4], [80691001, 4, 4]]),
        "props": None
    }),
    100574: _tools.RODict({
        "ID": 100574,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80591001, 5, 4], [80691001, 5, 4]]),
        "props": None
    }),
    100575: _tools.RODict({
        "ID": 100575,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80591001, 6, 4], [80691001, 6, 4]]),
        "props": None
    }),
    100576: _tools.RODict({
        "ID": 100576,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80811001, 3, 1], [80311001, 3, 1]]),
        "props": None
    }),
    100577: _tools.RODict({
        "ID": 100577,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80811001, 4, 1], [80311001, 4, 1]]),
        "props": None
    }),
    100578: _tools.RODict({
        "ID": 100578,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80811001, 5, 1], [80311001, 5, 1]]),
        "props": None
    }),
    100579: _tools.RODict({
        "ID": 100579,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80811001, 3, 2], [80311001, 3, 2]]),
        "props": None
    }),
    100580: _tools.RODict({
        "ID": 100580,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80811001, 4, 2], [80311001, 4, 2]]),
        "props": None
    }),
    100581: _tools.RODict({
        "ID": 100581,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80811001, 5, 2], [80311001, 5, 2]]),
        "props": None
    }),
    100582: _tools.RODict({
        "ID": 100582,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80811001, 6, 2], [80311001, 6, 2]]),
        "props": None
    }),
    100583: _tools.RODict({
        "ID": 100583,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80811001, 3, 3], [80311001, 3, 3]]),
        "props": None
    }),
    100584: _tools.RODict({
        "ID": 100584,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80811001, 4, 3], [80311001, 4, 3]]),
        "props": None
    }),
    100585: _tools.RODict({
        "ID": 100585,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80811001, 5, 3], [80311001, 5, 3]]),
        "props": None
    }),
    100586: _tools.RODict({
        "ID": 100586,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80811001, 6, 3], [80311001, 6, 3]]),
        "props": None
    }),
    100587: _tools.RODict({
        "ID": 100587,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80811001, 3, 4], [80311001, 3, 4]]),
        "props": None
    }),
    100588: _tools.RODict({
        "ID": 100588,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80811001, 4, 4], [80311001, 4, 4]]),
        "props": None
    }),
    100589: _tools.RODict({
        "ID": 100589,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80811001, 5, 4], [80311001, 5, 4]]),
        "props": None
    }),
    100590: _tools.RODict({
        "ID": 100590,
        "unavailableClass": _tools.ROList([1002, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80811001, 6, 4], [80311001, 6, 4]]),
        "props": None
    }),
    100591: _tools.RODict({
        "ID": 100591,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":1}),
        "equipment": _tools.ROList([[80121001, 0, 1], [80591001, 0, 1], [80691001, 0, 1]]),
        "props": None
    }),
    100592: _tools.RODict({
        "ID": 100592,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":1}),
        "equipment": _tools.ROList([[80121001, 1, 1], [80591001, 1, 1], [80691001, 1, 1]]),
        "props": None
    }),
    100593: _tools.RODict({
        "ID": 100593,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":2}),
        "equipment": _tools.ROList([[80121001, 2, 1], [80591001, 2, 1], [80691001, 2, 1]]),
        "props": None
    }),
    100594: _tools.RODict({
        "ID": 100594,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":2}),
        "equipment": _tools.ROList([[80121001, 3, 1], [80591001, 3, 1], [80691001, 3, 1]]),
        "props": None
    }),
    100595: _tools.RODict({
        "ID": 100595,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":3}),
        "equipment": _tools.ROList([[80121001, 4, 1], [80591001, 4, 1], [80691001, 4, 1]]),
        "props": None
    }),
    100596: _tools.RODict({
        "ID": 100596,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":3}),
        "equipment": _tools.ROList([[80121001, 5, 1], [80591001, 5, 1], [80691001, 5, 1]]),
        "props": None
    }),
    100597: _tools.RODict({
        "ID": 100597,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":4}),
        "equipment": _tools.ROList([[80121001, 6, 1], [80591001, 6, 1], [80691001, 6, 1]]),
        "props": None
    }),
    100598: _tools.RODict({
        "ID": 100598,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":4}),
        "equipment": _tools.ROList([[80121001, 7, 1], [80591001, 7, 1], [80691001, 7, 1]]),
        "props": None
    }),
    100599: _tools.RODict({
        "ID": 100599,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":1}),
        "equipment": _tools.ROList([[80121001, 0, 2], [80591001, 0, 2], [80691001, 0, 2]]),
        "props": None
    }),
    100600: _tools.RODict({
        "ID": 100600,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":1}),
        "equipment": _tools.ROList([[80121001, 1, 2], [80591001, 1, 2], [80691001, 1, 2]]),
        "props": None
    }),
    100601: _tools.RODict({
        "ID": 100601,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":2}),
        "equipment": _tools.ROList([[80121001, 2, 2], [80591001, 2, 2], [80691001, 2, 2]]),
        "props": None
    }),
    100602: _tools.RODict({
        "ID": 100602,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":2}),
        "equipment": _tools.ROList([[80121001, 3, 2], [80591001, 3, 2], [80691001, 3, 2]]),
        "props": None
    }),
    100603: _tools.RODict({
        "ID": 100603,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":3}),
        "equipment": _tools.ROList([[80121001, 4, 2], [80591001, 4, 2], [80691001, 4, 2]]),
        "props": None
    }),
    100604: _tools.RODict({
        "ID": 100604,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":3}),
        "equipment": _tools.ROList([[80121001, 5, 2], [80591001, 5, 2], [80691001, 5, 2]]),
        "props": None
    }),
    100605: _tools.RODict({
        "ID": 100605,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":4}),
        "equipment": _tools.ROList([[80121001, 6, 2], [80591001, 6, 2], [80691001, 6, 2]]),
        "props": None
    }),
    100606: _tools.RODict({
        "ID": 100606,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":4}),
        "equipment": _tools.ROList([[80121001, 7, 2], [80591001, 7, 2], [80691001, 7, 2]]),
        "props": None
    }),
    100607: _tools.RODict({
        "ID": 100607,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":1}),
        "equipment": _tools.ROList([[80121001, 0, 3], [80591001, 0, 3], [80691001, 0, 3]]),
        "props": None
    }),
    100608: _tools.RODict({
        "ID": 100608,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":1}),
        "equipment": _tools.ROList([[80121001, 1, 3], [80591001, 1, 3], [80691001, 1, 3]]),
        "props": None
    }),
    100609: _tools.RODict({
        "ID": 100609,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":2}),
        "equipment": _tools.ROList([[80121001, 2, 3], [80591001, 2, 3], [80691001, 2, 3]]),
        "props": None
    }),
    100610: _tools.RODict({
        "ID": 100610,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":2}),
        "equipment": _tools.ROList([[80121001, 3, 3], [80591001, 3, 3], [80691001, 3, 3]]),
        "props": None
    }),
    100611: _tools.RODict({
        "ID": 100611,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":3}),
        "equipment": _tools.ROList([[80121001, 4, 3], [80591001, 4, 3], [80691001, 4, 3]]),
        "props": None
    }),
    100612: _tools.RODict({
        "ID": 100612,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":3}),
        "equipment": _tools.ROList([[80121001, 5, 3], [80591001, 5, 3], [80691001, 5, 3]]),
        "props": None
    }),
    100613: _tools.RODict({
        "ID": 100613,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":4}),
        "equipment": _tools.ROList([[80121001, 6, 3], [80591001, 6, 3], [80691001, 6, 3]]),
        "props": None
    }),
    100614: _tools.RODict({
        "ID": 100614,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":4}),
        "equipment": _tools.ROList([[80121001, 7, 3], [80591001, 7, 3], [80691001, 7, 3]]),
        "props": None
    }),
    100615: _tools.RODict({
        "ID": 100615,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":1}),
        "equipment": _tools.ROList([[80121001, 0, 4], [80591001, 0, 4], [80691001, 0, 4]]),
        "props": None
    }),
    100616: _tools.RODict({
        "ID": 100616,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":1}),
        "equipment": _tools.ROList([[80121001, 1, 4], [80591001, 1, 4], [80691001, 1, 4]]),
        "props": None
    }),
    100617: _tools.RODict({
        "ID": 100617,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":2}),
        "equipment": _tools.ROList([[80121001, 2, 4], [80591001, 2, 4], [80691001, 2, 4]]),
        "props": None
    }),
    100618: _tools.RODict({
        "ID": 100618,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":2}),
        "equipment": _tools.ROList([[80121001, 3, 4], [80591001, 3, 4], [80691001, 3, 4]]),
        "props": None
    }),
    100619: _tools.RODict({
        "ID": 100619,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":3}),
        "equipment": _tools.ROList([[80121001, 4, 4], [80591001, 4, 4], [80691001, 4, 4]]),
        "props": None
    }),
    100620: _tools.RODict({
        "ID": 100620,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":3}),
        "equipment": _tools.ROList([[80121001, 5, 4], [80591001, 5, 4], [80691001, 5, 4]]),
        "props": None
    }),
    100621: _tools.RODict({
        "ID": 100621,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":4}),
        "equipment": _tools.ROList([[80121001, 6, 4], [80591001, 6, 4], [80691001, 6, 4]]),
        "props": None
    }),
    100622: _tools.RODict({
        "ID": 100622,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMaxMagicAtk":4}),
        "equipment": _tools.ROList([[80121001, 7, 4], [80591001, 7, 4], [80691001, 7, 4]]),
        "props": None
    }),
    100623: _tools.RODict({
        "ID": 100623,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":1}),
        "equipment": _tools.ROList([[80121001, 0, 1], [80591001, 0, 1], [80791001, 0, 1]]),
        "props": None
    }),
    100624: _tools.RODict({
        "ID": 100624,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":1}),
        "equipment": _tools.ROList([[80121001, 1, 1], [80591001, 1, 1], [80791001, 1, 1]]),
        "props": None
    }),
    100625: _tools.RODict({
        "ID": 100625,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":2}),
        "equipment": _tools.ROList([[80121001, 2, 1], [80591001, 2, 1], [80791001, 2, 1]]),
        "props": None
    }),
    100626: _tools.RODict({
        "ID": 100626,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":2}),
        "equipment": _tools.ROList([[80121001, 3, 1], [80591001, 3, 1], [80791001, 3, 1]]),
        "props": None
    }),
    100627: _tools.RODict({
        "ID": 100627,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":3}),
        "equipment": _tools.ROList([[80121001, 4, 1], [80591001, 4, 1], [80791001, 4, 1]]),
        "props": None
    }),
    100628: _tools.RODict({
        "ID": 100628,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":3}),
        "equipment": _tools.ROList([[80121001, 5, 1], [80591001, 5, 1], [80791001, 5, 1]]),
        "props": None
    }),
    100629: _tools.RODict({
        "ID": 100629,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":4}),
        "equipment": _tools.ROList([[80121001, 6, 1], [80591001, 6, 1], [80791001, 6, 1]]),
        "props": None
    }),
    100630: _tools.RODict({
        "ID": 100630,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":4}),
        "equipment": _tools.ROList([[80121001, 7, 1], [80591001, 7, 1], [80791001, 7, 1]]),
        "props": None
    }),
    100631: _tools.RODict({
        "ID": 100631,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":1}),
        "equipment": _tools.ROList([[80121001, 0, 2], [80591001, 0, 2], [80791001, 0, 2]]),
        "props": None
    }),
    100632: _tools.RODict({
        "ID": 100632,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":1}),
        "equipment": _tools.ROList([[80121001, 1, 2], [80591001, 1, 2], [80791001, 1, 2]]),
        "props": None
    }),
    100633: _tools.RODict({
        "ID": 100633,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":2}),
        "equipment": _tools.ROList([[80121001, 2, 2], [80591001, 2, 2], [80791001, 2, 2]]),
        "props": None
    }),
    100634: _tools.RODict({
        "ID": 100634,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":2}),
        "equipment": _tools.ROList([[80121001, 3, 2], [80591001, 3, 2], [80791001, 3, 2]]),
        "props": None
    }),
    100635: _tools.RODict({
        "ID": 100635,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":3}),
        "equipment": _tools.ROList([[80121001, 4, 2], [80591001, 4, 2], [80791001, 4, 2]]),
        "props": None
    }),
    100636: _tools.RODict({
        "ID": 100636,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":3}),
        "equipment": _tools.ROList([[80121001, 5, 2], [80591001, 5, 2], [80791001, 5, 2]]),
        "props": None
    }),
    100637: _tools.RODict({
        "ID": 100637,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":4}),
        "equipment": _tools.ROList([[80121001, 6, 2], [80591001, 6, 2], [80791001, 6, 2]]),
        "props": None
    }),
    100638: _tools.RODict({
        "ID": 100638,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":4}),
        "equipment": _tools.ROList([[80121001, 7, 2], [80591001, 7, 2], [80791001, 7, 2]]),
        "props": None
    }),
    100639: _tools.RODict({
        "ID": 100639,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":1}),
        "equipment": _tools.ROList([[80121001, 0, 3], [80591001, 0, 3], [80791001, 0, 3]]),
        "props": None
    }),
    100640: _tools.RODict({
        "ID": 100640,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":1}),
        "equipment": _tools.ROList([[80121001, 1, 3], [80591001, 1, 3], [80791001, 1, 3]]),
        "props": None
    }),
    100641: _tools.RODict({
        "ID": 100641,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":2}),
        "equipment": _tools.ROList([[80121001, 2, 3], [80591001, 2, 3], [80791001, 2, 3]]),
        "props": None
    }),
    100642: _tools.RODict({
        "ID": 100642,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":2}),
        "equipment": _tools.ROList([[80121001, 3, 3], [80591001, 3, 3], [80791001, 3, 3]]),
        "props": None
    }),
    100643: _tools.RODict({
        "ID": 100643,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":3}),
        "equipment": _tools.ROList([[80121001, 4, 3], [80591001, 4, 3], [80791001, 4, 3]]),
        "props": None
    }),
    100644: _tools.RODict({
        "ID": 100644,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":3}),
        "equipment": _tools.ROList([[80121001, 5, 3], [80591001, 5, 3], [80791001, 5, 3]]),
        "props": None
    }),
    100645: _tools.RODict({
        "ID": 100645,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":4}),
        "equipment": _tools.ROList([[80121001, 6, 3], [80591001, 6, 3], [80791001, 6, 3]]),
        "props": None
    }),
    100646: _tools.RODict({
        "ID": 100646,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":4}),
        "equipment": _tools.ROList([[80121001, 7, 3], [80591001, 7, 3], [80791001, 7, 3]]),
        "props": None
    }),
    100647: _tools.RODict({
        "ID": 100647,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":1}),
        "equipment": _tools.ROList([[80121001, 0, 4], [80591001, 0, 4], [80791001, 0, 4]]),
        "props": None
    }),
    100648: _tools.RODict({
        "ID": 100648,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":1}),
        "equipment": _tools.ROList([[80121001, 1, 4], [80591001, 1, 4], [80791001, 1, 4]]),
        "props": None
    }),
    100649: _tools.RODict({
        "ID": 100649,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":2}),
        "equipment": _tools.ROList([[80121001, 2, 4], [80591001, 2, 4], [80791001, 2, 4]]),
        "props": None
    }),
    100650: _tools.RODict({
        "ID": 100650,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":2}),
        "equipment": _tools.ROList([[80121001, 3, 4], [80591001, 3, 4], [80791001, 3, 4]]),
        "props": None
    }),
    100651: _tools.RODict({
        "ID": 100651,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":3}),
        "equipment": _tools.ROList([[80121001, 4, 4], [80591001, 4, 4], [80791001, 4, 4]]),
        "props": None
    }),
    100652: _tools.RODict({
        "ID": 100652,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":3}),
        "equipment": _tools.ROList([[80121001, 5, 4], [80591001, 5, 4], [80791001, 5, 4]]),
        "props": None
    }),
    100653: _tools.RODict({
        "ID": 100653,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":4}),
        "equipment": _tools.ROList([[80121001, 6, 4], [80591001, 6, 4], [80791001, 6, 4]]),
        "props": None
    }),
    100654: _tools.RODict({
        "ID": 100654,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMinMagicAtk":4}),
        "equipment": _tools.ROList([[80121001, 7, 4], [80591001, 7, 4], [80791001, 7, 4]]),
        "props": None
    }),
    100655: _tools.RODict({
        "ID": 100655,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":30}),
        "equipment": _tools.ROList([[80221001, 0, 1], [80821001, 0, 1], [80791001, 0, 1]]),
        "props": None
    }),
    100656: _tools.RODict({
        "ID": 100656,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":45}),
        "equipment": _tools.ROList([[80221001, 1, 1], [80821001, 1, 1], [80791001, 1, 1]]),
        "props": None
    }),
    100657: _tools.RODict({
        "ID": 100657,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":60}),
        "equipment": _tools.ROList([[80221001, 2, 1], [80821001, 2, 1], [80791001, 2, 1]]),
        "props": None
    }),
    100658: _tools.RODict({
        "ID": 100658,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":75}),
        "equipment": _tools.ROList([[80221001, 3, 1], [80821001, 3, 1], [80791001, 3, 1]]),
        "props": None
    }),
    100659: _tools.RODict({
        "ID": 100659,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":90}),
        "equipment": _tools.ROList([[80221001, 4, 1], [80821001, 4, 1], [80791001, 4, 1]]),
        "props": None
    }),
    100660: _tools.RODict({
        "ID": 100660,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":120}),
        "equipment": _tools.ROList([[80221001, 5, 1], [80821001, 5, 1], [80791001, 5, 1]]),
        "props": None
    }),
    100661: _tools.RODict({
        "ID": 100661,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":160}),
        "equipment": _tools.ROList([[80221001, 6, 1], [80821001, 6, 1], [80791001, 6, 1]]),
        "props": None
    }),
    100662: _tools.RODict({
        "ID": 100662,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":250}),
        "equipment": _tools.ROList([[80221001, 7, 1], [80821001, 7, 1], [80791001, 7, 1]]),
        "props": None
    }),
    100663: _tools.RODict({
        "ID": 100663,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":60}),
        "equipment": _tools.ROList([[80221001, 0, 2], [80821001, 0, 2], [80791001, 0, 2]]),
        "props": None
    }),
    100664: _tools.RODict({
        "ID": 100664,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":75}),
        "equipment": _tools.ROList([[80221001, 1, 2], [80821001, 1, 2], [80791001, 1, 2]]),
        "props": None
    }),
    100665: _tools.RODict({
        "ID": 100665,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":90}),
        "equipment": _tools.ROList([[80221001, 2, 2], [80821001, 2, 2], [80791001, 2, 2]]),
        "props": None
    }),
    100666: _tools.RODict({
        "ID": 100666,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":105}),
        "equipment": _tools.ROList([[80221001, 3, 2], [80821001, 3, 2], [80791001, 3, 2]]),
        "props": None
    }),
    100667: _tools.RODict({
        "ID": 100667,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":120}),
        "equipment": _tools.ROList([[80221001, 4, 2], [80821001, 4, 2], [80791001, 4, 2]]),
        "props": None
    }),
    100668: _tools.RODict({
        "ID": 100668,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":150}),
        "equipment": _tools.ROList([[80221001, 5, 2], [80821001, 5, 2], [80791001, 5, 2]]),
        "props": None
    }),
    100669: _tools.RODict({
        "ID": 100669,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":190}),
        "equipment": _tools.ROList([[80221001, 6, 2], [80821001, 6, 2], [80791001, 6, 2]]),
        "props": None
    }),
    100670: _tools.RODict({
        "ID": 100670,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":300}),
        "equipment": _tools.ROList([[80221001, 7, 2], [80821001, 7, 2], [80791001, 7, 2]]),
        "props": None
    }),
    100671: _tools.RODict({
        "ID": 100671,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":90}),
        "equipment": _tools.ROList([[80221001, 0, 3], [80821001, 0, 3], [80791001, 0, 3]]),
        "props": None
    }),
    100672: _tools.RODict({
        "ID": 100672,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":105}),
        "equipment": _tools.ROList([[80221001, 1, 3], [80821001, 1, 3], [80791001, 1, 3]]),
        "props": None
    }),
    100673: _tools.RODict({
        "ID": 100673,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":120}),
        "equipment": _tools.ROList([[80221001, 2, 3], [80821001, 2, 3], [80791001, 2, 3]]),
        "props": None
    }),
    100674: _tools.RODict({
        "ID": 100674,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":140}),
        "equipment": _tools.ROList([[80221001, 3, 3], [80821001, 3, 3], [80791001, 3, 3]]),
        "props": None
    }),
    100675: _tools.RODict({
        "ID": 100675,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":155}),
        "equipment": _tools.ROList([[80221001, 4, 3], [80821001, 4, 3], [80791001, 4, 3]]),
        "props": None
    }),
    100676: _tools.RODict({
        "ID": 100676,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":185}),
        "equipment": _tools.ROList([[80221001, 5, 3], [80821001, 5, 3], [80791001, 5, 3]]),
        "props": None
    }),
    100677: _tools.RODict({
        "ID": 100677,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":225}),
        "equipment": _tools.ROList([[80221001, 6, 3], [80821001, 6, 3], [80791001, 6, 3]]),
        "props": None
    }),
    100678: _tools.RODict({
        "ID": 100678,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":350}),
        "equipment": _tools.ROList([[80221001, 7, 3], [80821001, 7, 3], [80791001, 7, 3]]),
        "props": None
    }),
    100679: _tools.RODict({
        "ID": 100679,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":130}),
        "equipment": _tools.ROList([[80221001, 0, 4], [80821001, 0, 4], [80791001, 0, 4]]),
        "props": None
    }),
    100680: _tools.RODict({
        "ID": 100680,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":145}),
        "equipment": _tools.ROList([[80221001, 1, 4], [80821001, 1, 4], [80791001, 1, 4]]),
        "props": None
    }),
    100681: _tools.RODict({
        "ID": 100681,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":160}),
        "equipment": _tools.ROList([[80221001, 2, 4], [80821001, 2, 4], [80791001, 2, 4]]),
        "props": None
    }),
    100682: _tools.RODict({
        "ID": 100682,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":180}),
        "equipment": _tools.ROList([[80221001, 3, 4], [80821001, 3, 4], [80791001, 3, 4]]),
        "props": None
    }),
    100683: _tools.RODict({
        "ID": 100683,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":200}),
        "equipment": _tools.ROList([[80221001, 4, 4], [80821001, 4, 4], [80791001, 4, 4]]),
        "props": None
    }),
    100684: _tools.RODict({
        "ID": 100684,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":225}),
        "equipment": _tools.ROList([[80221001, 5, 4], [80821001, 5, 4], [80791001, 5, 4]]),
        "props": None
    }),
    100685: _tools.RODict({
        "ID": 100685,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":270}),
        "equipment": _tools.ROList([[80221001, 6, 4], [80821001, 6, 4], [80791001, 6, 4]]),
        "props": None
    }),
    100686: _tools.RODict({
        "ID": 100686,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullHp":400}),
        "equipment": _tools.ROList([[80221001, 7, 4], [80821001, 7, 4], [80791001, 7, 4]]),
        "props": None
    }),
    100687: _tools.RODict({
        "ID": 100687,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullMp":3}),
        "equipment": _tools.ROList([[80221001, 0, 1], [80591001, 0, 1], [80691001, 0, 1]]),
        "props": None
    }),
    100688: _tools.RODict({
        "ID": 100688,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullMp":4}),
        "equipment": _tools.ROList([[80221001, 1, 1], [80591001, 1, 1], [80691001, 1, 1]]),
        "props": None
    }),
    100689: _tools.RODict({
        "ID": 100689,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullMp":6}),
        "equipment": _tools.ROList([[80221001, 2, 1], [80591001, 2, 1], [80691001, 2, 1]]),
        "props": None
    }),
    100690: _tools.RODict({
        "ID": 100690,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullMp":8}),
        "equipment": _tools.ROList([[80221001, 3, 1], [80591001, 3, 1], [80691001, 3, 1]]),
        "props": None
    }),
    100691: _tools.RODict({
        "ID": 100691,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullMp":9}),
        "equipment": _tools.ROList([[80221001, 4, 1], [80591001, 4, 1], [80691001, 4, 1]]),
        "props": None
    }),
    100692: _tools.RODict({
        "ID": 100692,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullMp":13}),
        "equipment": _tools.ROList([[80221001, 5, 1], [80591001, 5, 1], [80691001, 5, 1]]),
        "props": None
    }),
    100693: _tools.RODict({
        "ID": 100693,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullMp":17}),
        "equipment": _tools.ROList([[80221001, 6, 1], [80591001, 6, 1], [80691001, 6, 1]]),
        "props": None
    }),
    100694: _tools.RODict({
        "ID": 100694,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullMp":26}),
        "equipment": _tools.ROList([[80221001, 7, 1], [80591001, 7, 1], [80691001, 7, 1]]),
        "props": None
    }),
    100695: _tools.RODict({
        "ID": 100695,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullMp":6}),
        "equipment": _tools.ROList([[80221001, 0, 2], [80591001, 0, 2], [80691001, 0, 2]]),
        "props": None
    }),
    100696: _tools.RODict({
        "ID": 100696,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullMp":8}),
        "equipment": _tools.ROList([[80221001, 1, 2], [80591001, 1, 2], [80691001, 1, 2]]),
        "props": None
    }),
    100697: _tools.RODict({
        "ID": 100697,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullMp":9}),
        "equipment": _tools.ROList([[80221001, 2, 2], [80591001, 2, 2], [80691001, 2, 2]]),
        "props": None
    }),
    100698: _tools.RODict({
        "ID": 100698,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullMp":12}),
        "equipment": _tools.ROList([[80221001, 3, 2], [80591001, 3, 2], [80691001, 3, 2]]),
        "props": None
    }),
    100699: _tools.RODict({
        "ID": 100699,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullMp":13}),
        "equipment": _tools.ROList([[80221001, 4, 2], [80591001, 4, 2], [80691001, 4, 2]]),
        "props": None
    }),
    100700: _tools.RODict({
        "ID": 100700,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullMp":16}),
        "equipment": _tools.ROList([[80221001, 5, 2], [80591001, 5, 2], [80691001, 5, 2]]),
        "props": None
    }),
    100701: _tools.RODict({
        "ID": 100701,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullMp":19}),
        "equipment": _tools.ROList([[80221001, 6, 2], [80591001, 6, 2], [80691001, 6, 2]]),
        "props": None
    }),
    100702: _tools.RODict({
        "ID": 100702,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullMp":28}),
        "equipment": _tools.ROList([[80221001, 7, 2], [80591001, 7, 2], [80691001, 7, 2]]),
        "props": None
    }),
    100703: _tools.RODict({
        "ID": 100703,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullMp":9}),
        "equipment": _tools.ROList([[80221001, 0, 3], [80591001, 0, 3], [80691001, 0, 3]]),
        "props": None
    }),
    100704: _tools.RODict({
        "ID": 100704,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullMp":11}),
        "equipment": _tools.ROList([[80221001, 1, 3], [80591001, 1, 3], [80691001, 1, 3]]),
        "props": None
    }),
    100705: _tools.RODict({
        "ID": 100705,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullMp":13}),
        "equipment": _tools.ROList([[80221001, 2, 3], [80591001, 2, 3], [80691001, 2, 3]]),
        "props": None
    }),
    100706: _tools.RODict({
        "ID": 100706,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullMp":14}),
        "equipment": _tools.ROList([[80221001, 3, 3], [80591001, 3, 3], [80691001, 3, 3]]),
        "props": None
    }),
    100707: _tools.RODict({
        "ID": 100707,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullMp":16}),
        "equipment": _tools.ROList([[80221001, 4, 3], [80591001, 4, 3], [80691001, 4, 3]]),
        "props": None
    }),
    100708: _tools.RODict({
        "ID": 100708,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullMp":19}),
        "equipment": _tools.ROList([[80221001, 5, 3], [80591001, 5, 3], [80691001, 5, 3]]),
        "props": None
    }),
    100709: _tools.RODict({
        "ID": 100709,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullMp":23}),
        "equipment": _tools.ROList([[80221001, 6, 3], [80591001, 6, 3], [80691001, 6, 3]]),
        "props": None
    }),
    100710: _tools.RODict({
        "ID": 100710,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullMp":32}),
        "equipment": _tools.ROList([[80221001, 7, 3], [80591001, 7, 3], [80691001, 7, 3]]),
        "props": None
    }),
    100711: _tools.RODict({
        "ID": 100711,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullMp":13}),
        "equipment": _tools.ROList([[80221001, 0, 4], [80591001, 0, 4], [80691001, 0, 4]]),
        "props": None
    }),
    100712: _tools.RODict({
        "ID": 100712,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullMp":14}),
        "equipment": _tools.ROList([[80221001, 1, 4], [80591001, 1, 4], [80691001, 1, 4]]),
        "props": None
    }),
    100713: _tools.RODict({
        "ID": 100713,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullMp":16}),
        "equipment": _tools.ROList([[80221001, 2, 4], [80591001, 2, 4], [80691001, 2, 4]]),
        "props": None
    }),
    100714: _tools.RODict({
        "ID": 100714,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullMp":18}),
        "equipment": _tools.ROList([[80221001, 3, 4], [80591001, 3, 4], [80691001, 3, 4]]),
        "props": None
    }),
    100715: _tools.RODict({
        "ID": 100715,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullMp":19}),
        "equipment": _tools.ROList([[80221001, 4, 4], [80591001, 4, 4], [80691001, 4, 4]]),
        "props": None
    }),
    100716: _tools.RODict({
        "ID": 100716,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullMp":23}),
        "equipment": _tools.ROList([[80221001, 5, 4], [80591001, 5, 4], [80691001, 5, 4]]),
        "props": None
    }),
    100717: _tools.RODict({
        "ID": 100717,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullMp":25}),
        "equipment": _tools.ROList([[80221001, 6, 4], [80591001, 6, 4], [80691001, 6, 4]]),
        "props": None
    }),
    100718: _tools.RODict({
        "ID": 100718,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFullMp":38}),
        "equipment": _tools.ROList([[80221001, 7, 4], [80591001, 7, 4], [80691001, 7, 4]]),
        "props": None
    }),
    100719: _tools.RODict({
        "ID": 100719,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.001}),
        "equipment": _tools.ROList([[80121001, 0, 1], [80421001, 0, 1], [80691001, 0, 1]]),
        "props": None
    }),
    100720: _tools.RODict({
        "ID": 100720,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.001}),
        "equipment": _tools.ROList([[80121001, 1, 1], [80421001, 1, 1], [80691001, 1, 1]]),
        "props": None
    }),
    100721: _tools.RODict({
        "ID": 100721,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0015}),
        "equipment": _tools.ROList([[80121001, 2, 1], [80421001, 2, 1], [80691001, 2, 1]]),
        "props": None
    }),
    100722: _tools.RODict({
        "ID": 100722,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.002}),
        "equipment": _tools.ROList([[80121001, 3, 1], [80421001, 3, 1], [80691001, 3, 1]]),
        "props": None
    }),
    100723: _tools.RODict({
        "ID": 100723,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.003}),
        "equipment": _tools.ROList([[80121001, 4, 1], [80421001, 4, 1], [80691001, 4, 1]]),
        "props": None
    }),
    100724: _tools.RODict({
        "ID": 100724,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.004}),
        "equipment": _tools.ROList([[80121001, 5, 1], [80421001, 5, 1], [80691001, 5, 1]]),
        "props": None
    }),
    100725: _tools.RODict({
        "ID": 100725,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.005}),
        "equipment": _tools.ROList([[80121001, 6, 1], [80421001, 6, 1], [80691001, 6, 1]]),
        "props": None
    }),
    100726: _tools.RODict({
        "ID": 100726,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0075}),
        "equipment": _tools.ROList([[80121001, 7, 1], [80421001, 7, 1], [80691001, 7, 1]]),
        "props": None
    }),
    100727: _tools.RODict({
        "ID": 100727,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0015}),
        "equipment": _tools.ROList([[80121001, 0, 2], [80421001, 0, 2], [80691001, 0, 2]]),
        "props": None
    }),
    100728: _tools.RODict({
        "ID": 100728,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0015}),
        "equipment": _tools.ROList([[80121001, 1, 2], [80421001, 1, 2], [80691001, 1, 2]]),
        "props": None
    }),
    100729: _tools.RODict({
        "ID": 100729,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.002}),
        "equipment": _tools.ROList([[80121001, 2, 2], [80421001, 2, 2], [80691001, 2, 2]]),
        "props": None
    }),
    100730: _tools.RODict({
        "ID": 100730,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0025}),
        "equipment": _tools.ROList([[80121001, 3, 2], [80421001, 3, 2], [80691001, 3, 2]]),
        "props": None
    }),
    100731: _tools.RODict({
        "ID": 100731,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0035}),
        "equipment": _tools.ROList([[80121001, 4, 2], [80421001, 4, 2], [80691001, 4, 2]]),
        "props": None
    }),
    100732: _tools.RODict({
        "ID": 100732,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0045}),
        "equipment": _tools.ROList([[80121001, 5, 2], [80421001, 5, 2], [80691001, 5, 2]]),
        "props": None
    }),
    100733: _tools.RODict({
        "ID": 100733,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0055}),
        "equipment": _tools.ROList([[80121001, 6, 2], [80421001, 6, 2], [80691001, 6, 2]]),
        "props": None
    }),
    100734: _tools.RODict({
        "ID": 100734,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.008}),
        "equipment": _tools.ROList([[80121001, 7, 2], [80421001, 7, 2], [80691001, 7, 2]]),
        "props": None
    }),
    100735: _tools.RODict({
        "ID": 100735,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.002}),
        "equipment": _tools.ROList([[80121001, 0, 3], [80421001, 0, 3], [80691001, 0, 3]]),
        "props": None
    }),
    100736: _tools.RODict({
        "ID": 100736,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0025}),
        "equipment": _tools.ROList([[80121001, 1, 3], [80421001, 1, 3], [80691001, 1, 3]]),
        "props": None
    }),
    100737: _tools.RODict({
        "ID": 100737,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0025}),
        "equipment": _tools.ROList([[80121001, 2, 3], [80421001, 2, 3], [80691001, 2, 3]]),
        "props": None
    }),
    100738: _tools.RODict({
        "ID": 100738,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.003}),
        "equipment": _tools.ROList([[80121001, 3, 3], [80421001, 3, 3], [80691001, 3, 3]]),
        "props": None
    }),
    100739: _tools.RODict({
        "ID": 100739,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.004}),
        "equipment": _tools.ROList([[80121001, 4, 3], [80421001, 4, 3], [80691001, 4, 3]]),
        "props": None
    }),
    100740: _tools.RODict({
        "ID": 100740,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.005}),
        "equipment": _tools.ROList([[80121001, 5, 3], [80421001, 5, 3], [80691001, 5, 3]]),
        "props": None
    }),
    100741: _tools.RODict({
        "ID": 100741,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.006}),
        "equipment": _tools.ROList([[80121001, 6, 3], [80421001, 6, 3], [80691001, 6, 3]]),
        "props": None
    }),
    100742: _tools.RODict({
        "ID": 100742,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0085}),
        "equipment": _tools.ROList([[80121001, 7, 3], [80421001, 7, 3], [80691001, 7, 3]]),
        "props": None
    }),
    100743: _tools.RODict({
        "ID": 100743,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0025}),
        "equipment": _tools.ROList([[80121001, 0, 4], [80421001, 0, 4], [80691001, 0, 4]]),
        "props": None
    }),
    100744: _tools.RODict({
        "ID": 100744,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.003}),
        "equipment": _tools.ROList([[80121001, 1, 4], [80421001, 1, 4], [80691001, 1, 4]]),
        "props": None
    }),
    100745: _tools.RODict({
        "ID": 100745,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.003}),
        "equipment": _tools.ROList([[80121001, 2, 4], [80421001, 2, 4], [80691001, 2, 4]]),
        "props": None
    }),
    100746: _tools.RODict({
        "ID": 100746,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0035}),
        "equipment": _tools.ROList([[80121001, 3, 4], [80421001, 3, 4], [80691001, 3, 4]]),
        "props": None
    }),
    100747: _tools.RODict({
        "ID": 100747,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0045}),
        "equipment": _tools.ROList([[80121001, 4, 4], [80421001, 4, 4], [80691001, 4, 4]]),
        "props": None
    }),
    100748: _tools.RODict({
        "ID": 100748,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0055}),
        "equipment": _tools.ROList([[80121001, 5, 4], [80421001, 5, 4], [80691001, 5, 4]]),
        "props": None
    }),
    100749: _tools.RODict({
        "ID": 100749,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.0065}),
        "equipment": _tools.ROList([[80121001, 6, 4], [80421001, 6, 4], [80691001, 6, 4]]),
        "props": None
    }),
    100750: _tools.RODict({
        "ID": 100750,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmg":0.009}),
        "equipment": _tools.ROList([[80121001, 7, 4], [80421001, 7, 4], [80691001, 7, 4]]),
        "props": None
    }),
    100751: _tools.RODict({
        "ID": 100751,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.001}),
        "equipment": _tools.ROList([[80221001, 0, 1], [80821001, 0, 1], [80421001, 0, 1]]),
        "props": None
    }),
    100752: _tools.RODict({
        "ID": 100752,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.001}),
        "equipment": _tools.ROList([[80221001, 1, 1], [80821001, 1, 1], [80421001, 1, 1]]),
        "props": None
    }),
    100753: _tools.RODict({
        "ID": 100753,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80221001, 2, 1], [80821001, 2, 1], [80421001, 2, 1]]),
        "props": None
    }),
    100754: _tools.RODict({
        "ID": 100754,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.002}),
        "equipment": _tools.ROList([[80221001, 3, 1], [80821001, 3, 1], [80421001, 3, 1]]),
        "props": None
    }),
    100755: _tools.RODict({
        "ID": 100755,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.003}),
        "equipment": _tools.ROList([[80221001, 4, 1], [80821001, 4, 1], [80421001, 4, 1]]),
        "props": None
    }),
    100756: _tools.RODict({
        "ID": 100756,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.004}),
        "equipment": _tools.ROList([[80221001, 5, 1], [80821001, 5, 1], [80421001, 5, 1]]),
        "props": None
    }),
    100757: _tools.RODict({
        "ID": 100757,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.005}),
        "equipment": _tools.ROList([[80221001, 6, 1], [80821001, 6, 1], [80421001, 6, 1]]),
        "props": None
    }),
    100758: _tools.RODict({
        "ID": 100758,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0075}),
        "equipment": _tools.ROList([[80221001, 7, 1], [80821001, 7, 1], [80421001, 7, 1]]),
        "props": None
    }),
    100759: _tools.RODict({
        "ID": 100759,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80221001, 0, 2], [80821001, 0, 2], [80421001, 0, 2]]),
        "props": None
    }),
    100760: _tools.RODict({
        "ID": 100760,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80221001, 1, 2], [80821001, 1, 2], [80421001, 1, 2]]),
        "props": None
    }),
    100761: _tools.RODict({
        "ID": 100761,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.002}),
        "equipment": _tools.ROList([[80221001, 2, 2], [80821001, 2, 2], [80421001, 2, 2]]),
        "props": None
    }),
    100762: _tools.RODict({
        "ID": 100762,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80221001, 3, 2], [80821001, 3, 2], [80421001, 3, 2]]),
        "props": None
    }),
    100763: _tools.RODict({
        "ID": 100763,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0035}),
        "equipment": _tools.ROList([[80221001, 4, 2], [80821001, 4, 2], [80421001, 4, 2]]),
        "props": None
    }),
    100764: _tools.RODict({
        "ID": 100764,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0045}),
        "equipment": _tools.ROList([[80221001, 5, 2], [80821001, 5, 2], [80421001, 5, 2]]),
        "props": None
    }),
    100765: _tools.RODict({
        "ID": 100765,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0055}),
        "equipment": _tools.ROList([[80221001, 6, 2], [80821001, 6, 2], [80421001, 6, 2]]),
        "props": None
    }),
    100766: _tools.RODict({
        "ID": 100766,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.008}),
        "equipment": _tools.ROList([[80221001, 7, 2], [80821001, 7, 2], [80421001, 7, 2]]),
        "props": None
    }),
    100767: _tools.RODict({
        "ID": 100767,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.002}),
        "equipment": _tools.ROList([[80221001, 0, 3], [80821001, 0, 3], [80421001, 0, 3]]),
        "props": None
    }),
    100768: _tools.RODict({
        "ID": 100768,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80221001, 1, 3], [80821001, 1, 3], [80421001, 1, 3]]),
        "props": None
    }),
    100769: _tools.RODict({
        "ID": 100769,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80221001, 2, 3], [80821001, 2, 3], [80421001, 2, 3]]),
        "props": None
    }),
    100770: _tools.RODict({
        "ID": 100770,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.003}),
        "equipment": _tools.ROList([[80221001, 3, 3], [80821001, 3, 3], [80421001, 3, 3]]),
        "props": None
    }),
    100771: _tools.RODict({
        "ID": 100771,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.004}),
        "equipment": _tools.ROList([[80221001, 4, 3], [80821001, 4, 3], [80421001, 4, 3]]),
        "props": None
    }),
    100772: _tools.RODict({
        "ID": 100772,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.005}),
        "equipment": _tools.ROList([[80221001, 5, 3], [80821001, 5, 3], [80421001, 5, 3]]),
        "props": None
    }),
    100773: _tools.RODict({
        "ID": 100773,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.006}),
        "equipment": _tools.ROList([[80221001, 6, 3], [80821001, 6, 3], [80421001, 6, 3]]),
        "props": None
    }),
    100774: _tools.RODict({
        "ID": 100774,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0085}),
        "equipment": _tools.ROList([[80221001, 7, 3], [80821001, 7, 3], [80421001, 7, 3]]),
        "props": None
    }),
    100775: _tools.RODict({
        "ID": 100775,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80221001, 0, 4], [80821001, 0, 4], [80421001, 0, 4]]),
        "props": None
    }),
    100776: _tools.RODict({
        "ID": 100776,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.003}),
        "equipment": _tools.ROList([[80221001, 1, 4], [80821001, 1, 4], [80421001, 1, 4]]),
        "props": None
    }),
    100777: _tools.RODict({
        "ID": 100777,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.003}),
        "equipment": _tools.ROList([[80221001, 2, 4], [80821001, 2, 4], [80421001, 2, 4]]),
        "props": None
    }),
    100778: _tools.RODict({
        "ID": 100778,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0035}),
        "equipment": _tools.ROList([[80221001, 3, 4], [80821001, 3, 4], [80421001, 3, 4]]),
        "props": None
    }),
    100779: _tools.RODict({
        "ID": 100779,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0045}),
        "equipment": _tools.ROList([[80221001, 4, 4], [80821001, 4, 4], [80421001, 4, 4]]),
        "props": None
    }),
    100780: _tools.RODict({
        "ID": 100780,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0055}),
        "equipment": _tools.ROList([[80221001, 5, 4], [80821001, 5, 4], [80421001, 5, 4]]),
        "props": None
    }),
    100781: _tools.RODict({
        "ID": 100781,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0065}),
        "equipment": _tools.ROList([[80221001, 6, 4], [80821001, 6, 4], [80421001, 6, 4]]),
        "props": None
    }),
    100782: _tools.RODict({
        "ID": 100782,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.009}),
        "equipment": _tools.ROList([[80221001, 7, 4], [80821001, 7, 4], [80421001, 7, 4]]),
        "props": None
    }),
    100783: _tools.RODict({
        "ID": 100783,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.001}),
        "equipment": _tools.ROList([[80321001, 0, 1], [80821001, 0, 1], [80421001, 0, 1]]),
        "props": None
    }),
    100784: _tools.RODict({
        "ID": 100784,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.001}),
        "equipment": _tools.ROList([[80321001, 1, 1], [80821001, 1, 1], [80421001, 1, 1]]),
        "props": None
    }),
    100785: _tools.RODict({
        "ID": 100785,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80321001, 2, 1], [80821001, 2, 1], [80421001, 2, 1]]),
        "props": None
    }),
    100786: _tools.RODict({
        "ID": 100786,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.002}),
        "equipment": _tools.ROList([[80321001, 3, 1], [80821001, 3, 1], [80421001, 3, 1]]),
        "props": None
    }),
    100787: _tools.RODict({
        "ID": 100787,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.003}),
        "equipment": _tools.ROList([[80321001, 4, 1], [80821001, 4, 1], [80421001, 4, 1]]),
        "props": None
    }),
    100788: _tools.RODict({
        "ID": 100788,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.004}),
        "equipment": _tools.ROList([[80321001, 5, 1], [80821001, 5, 1], [80421001, 5, 1]]),
        "props": None
    }),
    100789: _tools.RODict({
        "ID": 100789,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.005}),
        "equipment": _tools.ROList([[80321001, 6, 1], [80821001, 6, 1], [80421001, 6, 1]]),
        "props": None
    }),
    100790: _tools.RODict({
        "ID": 100790,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0075}),
        "equipment": _tools.ROList([[80321001, 7, 1], [80821001, 7, 1], [80421001, 7, 1]]),
        "props": None
    }),
    100791: _tools.RODict({
        "ID": 100791,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80321001, 0, 2], [80821001, 0, 2], [80421001, 0, 2]]),
        "props": None
    }),
    100792: _tools.RODict({
        "ID": 100792,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80321001, 1, 2], [80821001, 1, 2], [80421001, 1, 2]]),
        "props": None
    }),
    100793: _tools.RODict({
        "ID": 100793,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.002}),
        "equipment": _tools.ROList([[80321001, 2, 2], [80821001, 2, 2], [80421001, 2, 2]]),
        "props": None
    }),
    100794: _tools.RODict({
        "ID": 100794,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80321001, 3, 2], [80821001, 3, 2], [80421001, 3, 2]]),
        "props": None
    }),
    100795: _tools.RODict({
        "ID": 100795,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0035}),
        "equipment": _tools.ROList([[80321001, 4, 2], [80821001, 4, 2], [80421001, 4, 2]]),
        "props": None
    }),
    100796: _tools.RODict({
        "ID": 100796,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0045}),
        "equipment": _tools.ROList([[80321001, 5, 2], [80821001, 5, 2], [80421001, 5, 2]]),
        "props": None
    }),
    100797: _tools.RODict({
        "ID": 100797,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0055}),
        "equipment": _tools.ROList([[80321001, 6, 2], [80821001, 6, 2], [80421001, 6, 2]]),
        "props": None
    }),
    100798: _tools.RODict({
        "ID": 100798,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.008}),
        "equipment": _tools.ROList([[80321001, 7, 2], [80821001, 7, 2], [80421001, 7, 2]]),
        "props": None
    }),
    100799: _tools.RODict({
        "ID": 100799,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.002}),
        "equipment": _tools.ROList([[80321001, 0, 3], [80821001, 0, 3], [80421001, 0, 3]]),
        "props": None
    }),
    100800: _tools.RODict({
        "ID": 100800,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80321001, 1, 3], [80821001, 1, 3], [80421001, 1, 3]]),
        "props": None
    }),
    100801: _tools.RODict({
        "ID": 100801,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80321001, 2, 3], [80821001, 2, 3], [80421001, 2, 3]]),
        "props": None
    }),
    100802: _tools.RODict({
        "ID": 100802,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.003}),
        "equipment": _tools.ROList([[80321001, 3, 3], [80821001, 3, 3], [80421001, 3, 3]]),
        "props": None
    }),
    100803: _tools.RODict({
        "ID": 100803,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.004}),
        "equipment": _tools.ROList([[80321001, 4, 3], [80821001, 4, 3], [80421001, 4, 3]]),
        "props": None
    }),
    100804: _tools.RODict({
        "ID": 100804,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.005}),
        "equipment": _tools.ROList([[80321001, 5, 3], [80821001, 5, 3], [80421001, 5, 3]]),
        "props": None
    }),
    100805: _tools.RODict({
        "ID": 100805,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.006}),
        "equipment": _tools.ROList([[80321001, 6, 3], [80821001, 6, 3], [80421001, 6, 3]]),
        "props": None
    }),
    100806: _tools.RODict({
        "ID": 100806,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0085}),
        "equipment": _tools.ROList([[80321001, 7, 3], [80821001, 7, 3], [80421001, 7, 3]]),
        "props": None
    }),
    100807: _tools.RODict({
        "ID": 100807,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80321001, 0, 4], [80821001, 0, 4], [80421001, 0, 4]]),
        "props": None
    }),
    100808: _tools.RODict({
        "ID": 100808,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.003}),
        "equipment": _tools.ROList([[80321001, 1, 4], [80821001, 1, 4], [80421001, 1, 4]]),
        "props": None
    }),
    100809: _tools.RODict({
        "ID": 100809,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.003}),
        "equipment": _tools.ROList([[80321001, 2, 4], [80821001, 2, 4], [80421001, 2, 4]]),
        "props": None
    }),
    100810: _tools.RODict({
        "ID": 100810,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0035}),
        "equipment": _tools.ROList([[80321001, 3, 4], [80821001, 3, 4], [80421001, 3, 4]]),
        "props": None
    }),
    100811: _tools.RODict({
        "ID": 100811,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0045}),
        "equipment": _tools.ROList([[80321001, 4, 4], [80821001, 4, 4], [80421001, 4, 4]]),
        "props": None
    }),
    100812: _tools.RODict({
        "ID": 100812,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0055}),
        "equipment": _tools.ROList([[80321001, 5, 4], [80821001, 5, 4], [80421001, 5, 4]]),
        "props": None
    }),
    100813: _tools.RODict({
        "ID": 100813,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0065}),
        "equipment": _tools.ROList([[80321001, 6, 4], [80821001, 6, 4], [80421001, 6, 4]]),
        "props": None
    }),
    100814: _tools.RODict({
        "ID": 100814,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.009}),
        "equipment": _tools.ROList([[80321001, 7, 4], [80821001, 7, 4], [80421001, 7, 4]]),
        "props": None
    }),
    100815: _tools.RODict({
        "ID": 100815,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.001}),
        "equipment": _tools.ROList([[80821001, 0, 1], [80591001, 0, 1], [80791001, 0, 1]]),
        "props": None
    }),
    100816: _tools.RODict({
        "ID": 100816,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.001}),
        "equipment": _tools.ROList([[80821001, 1, 1], [80591001, 1, 1], [80791001, 1, 1]]),
        "props": None
    }),
    100817: _tools.RODict({
        "ID": 100817,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0015}),
        "equipment": _tools.ROList([[80821001, 2, 1], [80591001, 2, 1], [80791001, 2, 1]]),
        "props": None
    }),
    100818: _tools.RODict({
        "ID": 100818,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.002}),
        "equipment": _tools.ROList([[80821001, 3, 1], [80591001, 3, 1], [80791001, 3, 1]]),
        "props": None
    }),
    100819: _tools.RODict({
        "ID": 100819,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.003}),
        "equipment": _tools.ROList([[80821001, 4, 1], [80591001, 4, 1], [80791001, 4, 1]]),
        "props": None
    }),
    100820: _tools.RODict({
        "ID": 100820,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.004}),
        "equipment": _tools.ROList([[80821001, 5, 1], [80591001, 5, 1], [80791001, 5, 1]]),
        "props": None
    }),
    100821: _tools.RODict({
        "ID": 100821,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.005}),
        "equipment": _tools.ROList([[80821001, 6, 1], [80591001, 6, 1], [80791001, 6, 1]]),
        "props": None
    }),
    100822: _tools.RODict({
        "ID": 100822,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0075}),
        "equipment": _tools.ROList([[80821001, 7, 1], [80591001, 7, 1], [80791001, 7, 1]]),
        "props": None
    }),
    100823: _tools.RODict({
        "ID": 100823,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0015}),
        "equipment": _tools.ROList([[80821001, 0, 2], [80591001, 0, 2], [80791001, 0, 2]]),
        "props": None
    }),
    100824: _tools.RODict({
        "ID": 100824,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0015}),
        "equipment": _tools.ROList([[80821001, 1, 2], [80591001, 1, 2], [80791001, 1, 2]]),
        "props": None
    }),
    100825: _tools.RODict({
        "ID": 100825,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.002}),
        "equipment": _tools.ROList([[80821001, 2, 2], [80591001, 2, 2], [80791001, 2, 2]]),
        "props": None
    }),
    100826: _tools.RODict({
        "ID": 100826,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0025}),
        "equipment": _tools.ROList([[80821001, 3, 2], [80591001, 3, 2], [80791001, 3, 2]]),
        "props": None
    }),
    100827: _tools.RODict({
        "ID": 100827,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0035}),
        "equipment": _tools.ROList([[80821001, 4, 2], [80591001, 4, 2], [80791001, 4, 2]]),
        "props": None
    }),
    100828: _tools.RODict({
        "ID": 100828,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0045}),
        "equipment": _tools.ROList([[80821001, 5, 2], [80591001, 5, 2], [80791001, 5, 2]]),
        "props": None
    }),
    100829: _tools.RODict({
        "ID": 100829,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0055}),
        "equipment": _tools.ROList([[80821001, 6, 2], [80591001, 6, 2], [80791001, 6, 2]]),
        "props": None
    }),
    100830: _tools.RODict({
        "ID": 100830,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.008}),
        "equipment": _tools.ROList([[80821001, 7, 2], [80591001, 7, 2], [80791001, 7, 2]]),
        "props": None
    }),
    100831: _tools.RODict({
        "ID": 100831,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.002}),
        "equipment": _tools.ROList([[80821001, 0, 3], [80591001, 0, 3], [80791001, 0, 3]]),
        "props": None
    }),
    100832: _tools.RODict({
        "ID": 100832,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0025}),
        "equipment": _tools.ROList([[80821001, 1, 3], [80591001, 1, 3], [80791001, 1, 3]]),
        "props": None
    }),
    100833: _tools.RODict({
        "ID": 100833,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0025}),
        "equipment": _tools.ROList([[80821001, 2, 3], [80591001, 2, 3], [80791001, 2, 3]]),
        "props": None
    }),
    100834: _tools.RODict({
        "ID": 100834,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.003}),
        "equipment": _tools.ROList([[80821001, 3, 3], [80591001, 3, 3], [80791001, 3, 3]]),
        "props": None
    }),
    100835: _tools.RODict({
        "ID": 100835,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.004}),
        "equipment": _tools.ROList([[80821001, 4, 3], [80591001, 4, 3], [80791001, 4, 3]]),
        "props": None
    }),
    100836: _tools.RODict({
        "ID": 100836,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.005}),
        "equipment": _tools.ROList([[80821001, 5, 3], [80591001, 5, 3], [80791001, 5, 3]]),
        "props": None
    }),
    100837: _tools.RODict({
        "ID": 100837,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.006}),
        "equipment": _tools.ROList([[80821001, 6, 3], [80591001, 6, 3], [80791001, 6, 3]]),
        "props": None
    }),
    100838: _tools.RODict({
        "ID": 100838,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0085}),
        "equipment": _tools.ROList([[80821001, 7, 3], [80591001, 7, 3], [80791001, 7, 3]]),
        "props": None
    }),
    100839: _tools.RODict({
        "ID": 100839,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0025}),
        "equipment": _tools.ROList([[80821001, 0, 4], [80591001, 0, 4], [80791001, 0, 4]]),
        "props": None
    }),
    100840: _tools.RODict({
        "ID": 100840,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.003}),
        "equipment": _tools.ROList([[80821001, 1, 4], [80591001, 1, 4], [80791001, 1, 4]]),
        "props": None
    }),
    100841: _tools.RODict({
        "ID": 100841,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.003}),
        "equipment": _tools.ROList([[80821001, 2, 4], [80591001, 2, 4], [80791001, 2, 4]]),
        "props": None
    }),
    100842: _tools.RODict({
        "ID": 100842,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0035}),
        "equipment": _tools.ROList([[80821001, 3, 4], [80591001, 3, 4], [80791001, 3, 4]]),
        "props": None
    }),
    100843: _tools.RODict({
        "ID": 100843,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0045}),
        "equipment": _tools.ROList([[80821001, 4, 4], [80591001, 4, 4], [80791001, 4, 4]]),
        "props": None
    }),
    100844: _tools.RODict({
        "ID": 100844,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0055}),
        "equipment": _tools.ROList([[80821001, 5, 4], [80591001, 5, 4], [80791001, 5, 4]]),
        "props": None
    }),
    100845: _tools.RODict({
        "ID": 100845,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0065}),
        "equipment": _tools.ROList([[80821001, 6, 4], [80591001, 6, 4], [80791001, 6, 4]]),
        "props": None
    }),
    100846: _tools.RODict({
        "ID": 100846,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMonsterDmg":0.009}),
        "equipment": _tools.ROList([[80821001, 7, 4], [80591001, 7, 4], [80791001, 7, 4]]),
        "props": None
    }),
    100847: _tools.RODict({
        "ID": 100847,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMortal":0.002}),
        "equipment": _tools.ROList([[80321001, 0, 1], [80821001, 0, 1], [80421001, 0, 1]]),
        "props": None
    }),
    100848: _tools.RODict({
        "ID": 100848,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMortal":0.002}),
        "equipment": _tools.ROList([[80321001, 1, 1], [80821001, 1, 1], [80421001, 1, 1]]),
        "props": None
    }),
    100849: _tools.RODict({
        "ID": 100849,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMortal":0.003}),
        "equipment": _tools.ROList([[80321001, 2, 1], [80821001, 2, 1], [80421001, 2, 1]]),
        "props": None
    }),
    100850: _tools.RODict({
        "ID": 100850,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMortal":0.004}),
        "equipment": _tools.ROList([[80321001, 3, 1], [80821001, 3, 1], [80421001, 3, 1]]),
        "props": None
    }),
    100851: _tools.RODict({
        "ID": 100851,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMortal":0.006}),
        "equipment": _tools.ROList([[80321001, 4, 1], [80821001, 4, 1], [80421001, 4, 1]]),
        "props": None
    }),
    100852: _tools.RODict({
        "ID": 100852,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMortal":0.008}),
        "equipment": _tools.ROList([[80321001, 5, 1], [80821001, 5, 1], [80421001, 5, 1]]),
        "props": None
    }),
    100853: _tools.RODict({
        "ID": 100853,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMortal":0.01}),
        "equipment": _tools.ROList([[80321001, 6, 1], [80821001, 6, 1], [80421001, 6, 1]]),
        "props": None
    }),
    100854: _tools.RODict({
        "ID": 100854,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMortal":0.015}),
        "equipment": _tools.ROList([[80321001, 7, 1], [80821001, 7, 1], [80421001, 7, 1]]),
        "props": None
    }),
    100855: _tools.RODict({
        "ID": 100855,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMortal":0.003}),
        "equipment": _tools.ROList([[80321001, 0, 2], [80821001, 0, 2], [80421001, 0, 2]]),
        "props": None
    }),
    100856: _tools.RODict({
        "ID": 100856,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMortal":0.003}),
        "equipment": _tools.ROList([[80321001, 1, 2], [80821001, 1, 2], [80421001, 1, 2]]),
        "props": None
    }),
    100857: _tools.RODict({
        "ID": 100857,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMortal":0.004}),
        "equipment": _tools.ROList([[80321001, 2, 2], [80821001, 2, 2], [80421001, 2, 2]]),
        "props": None
    }),
    100858: _tools.RODict({
        "ID": 100858,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMortal":0.005}),
        "equipment": _tools.ROList([[80321001, 3, 2], [80821001, 3, 2], [80421001, 3, 2]]),
        "props": None
    }),
    100859: _tools.RODict({
        "ID": 100859,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMortal":0.007}),
        "equipment": _tools.ROList([[80321001, 4, 2], [80821001, 4, 2], [80421001, 4, 2]]),
        "props": None
    }),
    100860: _tools.RODict({
        "ID": 100860,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMortal":0.009}),
        "equipment": _tools.ROList([[80321001, 5, 2], [80821001, 5, 2], [80421001, 5, 2]]),
        "props": None
    }),
    100861: _tools.RODict({
        "ID": 100861,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMortal":0.011}),
        "equipment": _tools.ROList([[80321001, 6, 2], [80821001, 6, 2], [80421001, 6, 2]]),
        "props": None
    }),
    100862: _tools.RODict({
        "ID": 100862,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMortal":0.016}),
        "equipment": _tools.ROList([[80321001, 7, 2], [80821001, 7, 2], [80421001, 7, 2]]),
        "props": None
    }),
    100863: _tools.RODict({
        "ID": 100863,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMortal":0.004}),
        "equipment": _tools.ROList([[80321001, 0, 3], [80821001, 0, 3], [80421001, 0, 3]]),
        "props": None
    }),
    100864: _tools.RODict({
        "ID": 100864,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMortal":0.005}),
        "equipment": _tools.ROList([[80321001, 1, 3], [80821001, 1, 3], [80421001, 1, 3]]),
        "props": None
    }),
    100865: _tools.RODict({
        "ID": 100865,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMortal":0.005}),
        "equipment": _tools.ROList([[80321001, 2, 3], [80821001, 2, 3], [80421001, 2, 3]]),
        "props": None
    }),
    100866: _tools.RODict({
        "ID": 100866,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMortal":0.006}),
        "equipment": _tools.ROList([[80321001, 3, 3], [80821001, 3, 3], [80421001, 3, 3]]),
        "props": None
    }),
    100867: _tools.RODict({
        "ID": 100867,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMortal":0.008}),
        "equipment": _tools.ROList([[80321001, 4, 3], [80821001, 4, 3], [80421001, 4, 3]]),
        "props": None
    }),
    100868: _tools.RODict({
        "ID": 100868,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMortal":0.01}),
        "equipment": _tools.ROList([[80321001, 5, 3], [80821001, 5, 3], [80421001, 5, 3]]),
        "props": None
    }),
    100869: _tools.RODict({
        "ID": 100869,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMortal":0.012}),
        "equipment": _tools.ROList([[80321001, 6, 3], [80821001, 6, 3], [80421001, 6, 3]]),
        "props": None
    }),
    100870: _tools.RODict({
        "ID": 100870,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMortal":0.017}),
        "equipment": _tools.ROList([[80321001, 7, 3], [80821001, 7, 3], [80421001, 7, 3]]),
        "props": None
    }),
    100871: _tools.RODict({
        "ID": 100871,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMortal":0.005}),
        "equipment": _tools.ROList([[80321001, 0, 4], [80821001, 0, 4], [80421001, 0, 4]]),
        "props": None
    }),
    100872: _tools.RODict({
        "ID": 100872,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMortal":0.006}),
        "equipment": _tools.ROList([[80321001, 1, 4], [80821001, 1, 4], [80421001, 1, 4]]),
        "props": None
    }),
    100873: _tools.RODict({
        "ID": 100873,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMortal":0.006}),
        "equipment": _tools.ROList([[80321001, 2, 4], [80821001, 2, 4], [80421001, 2, 4]]),
        "props": None
    }),
    100874: _tools.RODict({
        "ID": 100874,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMortal":0.007}),
        "equipment": _tools.ROList([[80321001, 3, 4], [80821001, 3, 4], [80421001, 3, 4]]),
        "props": None
    }),
    100875: _tools.RODict({
        "ID": 100875,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMortal":0.009}),
        "equipment": _tools.ROList([[80321001, 4, 4], [80821001, 4, 4], [80421001, 4, 4]]),
        "props": None
    }),
    100876: _tools.RODict({
        "ID": 100876,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMortal":0.011}),
        "equipment": _tools.ROList([[80321001, 5, 4], [80821001, 5, 4], [80421001, 5, 4]]),
        "props": None
    }),
    100877: _tools.RODict({
        "ID": 100877,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMortal":0.013}),
        "equipment": _tools.ROList([[80321001, 6, 4], [80821001, 6, 4], [80421001, 6, 4]]),
        "props": None
    }),
    100878: _tools.RODict({
        "ID": 100878,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjMortal":0.018}),
        "equipment": _tools.ROList([[80321001, 7, 4], [80821001, 7, 4], [80421001, 7, 4]]),
        "props": None
    }),
    100879: _tools.RODict({
        "ID": 100879,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.002}),
        "equipment": _tools.ROList([[80821001, 0, 1], [80591001, 0, 1], [80791001, 0, 1]]),
        "props": None
    }),
    100880: _tools.RODict({
        "ID": 100880,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.002}),
        "equipment": _tools.ROList([[80821001, 1, 1], [80591001, 1, 1], [80791001, 1, 1]]),
        "props": None
    }),
    100881: _tools.RODict({
        "ID": 100881,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.003}),
        "equipment": _tools.ROList([[80821001, 2, 1], [80591001, 2, 1], [80791001, 2, 1]]),
        "props": None
    }),
    100882: _tools.RODict({
        "ID": 100882,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.004}),
        "equipment": _tools.ROList([[80821001, 3, 1], [80591001, 3, 1], [80791001, 3, 1]]),
        "props": None
    }),
    100883: _tools.RODict({
        "ID": 100883,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.006}),
        "equipment": _tools.ROList([[80821001, 4, 1], [80591001, 4, 1], [80791001, 4, 1]]),
        "props": None
    }),
    100884: _tools.RODict({
        "ID": 100884,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.008}),
        "equipment": _tools.ROList([[80821001, 5, 1], [80591001, 5, 1], [80791001, 5, 1]]),
        "props": None
    }),
    100885: _tools.RODict({
        "ID": 100885,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.01}),
        "equipment": _tools.ROList([[80821001, 6, 1], [80591001, 6, 1], [80791001, 6, 1]]),
        "props": None
    }),
    100886: _tools.RODict({
        "ID": 100886,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.015}),
        "equipment": _tools.ROList([[80821001, 7, 1], [80591001, 7, 1], [80791001, 7, 1]]),
        "props": None
    }),
    100887: _tools.RODict({
        "ID": 100887,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.003}),
        "equipment": _tools.ROList([[80821001, 0, 2], [80591001, 0, 2], [80791001, 0, 2]]),
        "props": None
    }),
    100888: _tools.RODict({
        "ID": 100888,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.003}),
        "equipment": _tools.ROList([[80821001, 1, 2], [80591001, 1, 2], [80791001, 1, 2]]),
        "props": None
    }),
    100889: _tools.RODict({
        "ID": 100889,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.004}),
        "equipment": _tools.ROList([[80821001, 2, 2], [80591001, 2, 2], [80791001, 2, 2]]),
        "props": None
    }),
    100890: _tools.RODict({
        "ID": 100890,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.005}),
        "equipment": _tools.ROList([[80821001, 3, 2], [80591001, 3, 2], [80791001, 3, 2]]),
        "props": None
    }),
    100891: _tools.RODict({
        "ID": 100891,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.007}),
        "equipment": _tools.ROList([[80821001, 4, 2], [80591001, 4, 2], [80791001, 4, 2]]),
        "props": None
    }),
    100892: _tools.RODict({
        "ID": 100892,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.009}),
        "equipment": _tools.ROList([[80821001, 5, 2], [80591001, 5, 2], [80791001, 5, 2]]),
        "props": None
    }),
    100893: _tools.RODict({
        "ID": 100893,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.011}),
        "equipment": _tools.ROList([[80821001, 6, 2], [80591001, 6, 2], [80791001, 6, 2]]),
        "props": None
    }),
    100894: _tools.RODict({
        "ID": 100894,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.016}),
        "equipment": _tools.ROList([[80821001, 7, 2], [80591001, 7, 2], [80791001, 7, 2]]),
        "props": None
    }),
    100895: _tools.RODict({
        "ID": 100895,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.004}),
        "equipment": _tools.ROList([[80821001, 0, 3], [80591001, 0, 3], [80791001, 0, 3]]),
        "props": None
    }),
    100896: _tools.RODict({
        "ID": 100896,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.005}),
        "equipment": _tools.ROList([[80821001, 1, 3], [80591001, 1, 3], [80791001, 1, 3]]),
        "props": None
    }),
    100897: _tools.RODict({
        "ID": 100897,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.005}),
        "equipment": _tools.ROList([[80821001, 2, 3], [80591001, 2, 3], [80791001, 2, 3]]),
        "props": None
    }),
    100898: _tools.RODict({
        "ID": 100898,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.006}),
        "equipment": _tools.ROList([[80821001, 3, 3], [80591001, 3, 3], [80791001, 3, 3]]),
        "props": None
    }),
    100899: _tools.RODict({
        "ID": 100899,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.008}),
        "equipment": _tools.ROList([[80821001, 4, 3], [80591001, 4, 3], [80791001, 4, 3]]),
        "props": None
    }),
    100900: _tools.RODict({
        "ID": 100900,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.01}),
        "equipment": _tools.ROList([[80821001, 5, 3], [80591001, 5, 3], [80791001, 5, 3]]),
        "props": None
    }),
    100901: _tools.RODict({
        "ID": 100901,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.012}),
        "equipment": _tools.ROList([[80821001, 6, 3], [80591001, 6, 3], [80791001, 6, 3]]),
        "props": None
    }),
    100902: _tools.RODict({
        "ID": 100902,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.017}),
        "equipment": _tools.ROList([[80821001, 7, 3], [80591001, 7, 3], [80791001, 7, 3]]),
        "props": None
    }),
    100903: _tools.RODict({
        "ID": 100903,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.005}),
        "equipment": _tools.ROList([[80821001, 0, 4], [80591001, 0, 4], [80791001, 0, 4]]),
        "props": None
    }),
    100904: _tools.RODict({
        "ID": 100904,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.006}),
        "equipment": _tools.ROList([[80821001, 1, 4], [80591001, 1, 4], [80791001, 1, 4]]),
        "props": None
    }),
    100905: _tools.RODict({
        "ID": 100905,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.006}),
        "equipment": _tools.ROList([[80821001, 2, 4], [80591001, 2, 4], [80791001, 2, 4]]),
        "props": None
    }),
    100906: _tools.RODict({
        "ID": 100906,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.007}),
        "equipment": _tools.ROList([[80821001, 3, 4], [80591001, 3, 4], [80791001, 3, 4]]),
        "props": None
    }),
    100907: _tools.RODict({
        "ID": 100907,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.009}),
        "equipment": _tools.ROList([[80821001, 4, 4], [80591001, 4, 4], [80791001, 4, 4]]),
        "props": None
    }),
    100908: _tools.RODict({
        "ID": 100908,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.011}),
        "equipment": _tools.ROList([[80821001, 5, 4], [80591001, 5, 4], [80791001, 5, 4]]),
        "props": None
    }),
    100909: _tools.RODict({
        "ID": 100909,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.013}),
        "equipment": _tools.ROList([[80821001, 6, 4], [80591001, 6, 4], [80791001, 6, 4]]),
        "props": None
    }),
    100910: _tools.RODict({
        "ID": 100910,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiMortal":0.018}),
        "equipment": _tools.ROList([[80821001, 7, 4], [80591001, 7, 4], [80791001, 7, 4]]),
        "props": None
    }),
    100911: _tools.RODict({
        "ID": 100911,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80121001, 4, 1], [80321001, 4, 1], [80591001, 4, 1]]),
        "props": None
    }),
    100912: _tools.RODict({
        "ID": 100912,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80121001, 5, 1], [80321001, 5, 1], [80591001, 5, 1]]),
        "props": None
    }),
    100913: _tools.RODict({
        "ID": 100913,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80121001, 6, 1], [80321001, 6, 1], [80591001, 6, 1]]),
        "props": None
    }),
    100914: _tools.RODict({
        "ID": 100914,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80121001, 4, 2], [80321001, 4, 2], [80591001, 4, 2]]),
        "props": None
    }),
    100915: _tools.RODict({
        "ID": 100915,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80121001, 5, 2], [80321001, 5, 2], [80591001, 5, 2]]),
        "props": None
    }),
    100916: _tools.RODict({
        "ID": 100916,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80121001, 6, 2], [80321001, 6, 2], [80591001, 6, 2]]),
        "props": None
    }),
    100917: _tools.RODict({
        "ID": 100917,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80121001, 7, 2], [80321001, 7, 2], [80591001, 7, 2]]),
        "props": None
    }),
    100918: _tools.RODict({
        "ID": 100918,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80121001, 4, 3], [80321001, 4, 3], [80591001, 4, 3]]),
        "props": None
    }),
    100919: _tools.RODict({
        "ID": 100919,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80121001, 5, 3], [80321001, 5, 3], [80591001, 5, 3]]),
        "props": None
    }),
    100920: _tools.RODict({
        "ID": 100920,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80121001, 6, 3], [80321001, 6, 3], [80591001, 6, 3]]),
        "props": None
    }),
    100921: _tools.RODict({
        "ID": 100921,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80121001, 7, 3], [80321001, 7, 3], [80591001, 7, 3]]),
        "props": None
    }),
    100922: _tools.RODict({
        "ID": 100922,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80121001, 4, 4], [80321001, 4, 4], [80591001, 4, 4]]),
        "props": None
    }),
    100923: _tools.RODict({
        "ID": 100923,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80121001, 5, 4], [80321001, 5, 4], [80591001, 5, 4]]),
        "props": None
    }),
    100924: _tools.RODict({
        "ID": 100924,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80121001, 6, 4], [80321001, 6, 4], [80591001, 6, 4]]),
        "props": None
    }),
    100925: _tools.RODict({
        "ID": 100925,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80121001, 7, 4], [80321001, 7, 4], [80591001, 7, 4]]),
        "props": None
    }),
    100926: _tools.RODict({
        "ID": 100926,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80221001, 4, 1], [80321001, 4, 1], [80421001, 4, 1]]),
        "props": None
    }),
    100927: _tools.RODict({
        "ID": 100927,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80221001, 5, 1], [80321001, 5, 1], [80421001, 5, 1]]),
        "props": None
    }),
    100928: _tools.RODict({
        "ID": 100928,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80221001, 6, 1], [80321001, 6, 1], [80421001, 6, 1]]),
        "props": None
    }),
    100929: _tools.RODict({
        "ID": 100929,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80221001, 4, 2], [80321001, 4, 2], [80421001, 4, 2]]),
        "props": None
    }),
    100930: _tools.RODict({
        "ID": 100930,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80221001, 5, 2], [80321001, 5, 2], [80421001, 5, 2]]),
        "props": None
    }),
    100931: _tools.RODict({
        "ID": 100931,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80221001, 6, 2], [80321001, 6, 2], [80421001, 6, 2]]),
        "props": None
    }),
    100932: _tools.RODict({
        "ID": 100932,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80221001, 7, 2], [80321001, 7, 2], [80421001, 7, 2]]),
        "props": None
    }),
    100933: _tools.RODict({
        "ID": 100933,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80221001, 4, 3], [80321001, 4, 3], [80421001, 4, 3]]),
        "props": None
    }),
    100934: _tools.RODict({
        "ID": 100934,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80221001, 5, 3], [80321001, 5, 3], [80421001, 5, 3]]),
        "props": None
    }),
    100935: _tools.RODict({
        "ID": 100935,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80221001, 6, 3], [80321001, 6, 3], [80421001, 6, 3]]),
        "props": None
    }),
    100936: _tools.RODict({
        "ID": 100936,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80221001, 7, 3], [80321001, 7, 3], [80421001, 7, 3]]),
        "props": None
    }),
    100937: _tools.RODict({
        "ID": 100937,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80221001, 4, 4], [80321001, 4, 4], [80421001, 4, 4]]),
        "props": None
    }),
    100938: _tools.RODict({
        "ID": 100938,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80221001, 5, 4], [80321001, 5, 4], [80421001, 5, 4]]),
        "props": None
    }),
    100939: _tools.RODict({
        "ID": 100939,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80221001, 6, 4], [80321001, 6, 4], [80421001, 6, 4]]),
        "props": None
    }),
    100940: _tools.RODict({
        "ID": 100940,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80221001, 7, 4], [80321001, 7, 4], [80421001, 7, 4]]),
        "props": None
    }),
    100941: _tools.RODict({
        "ID": 100941,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80321001, 4, 1], [80691001, 4, 1], [80791001, 4, 1]]),
        "props": None
    }),
    100942: _tools.RODict({
        "ID": 100942,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80321001, 5, 1], [80691001, 5, 1], [80791001, 5, 1]]),
        "props": None
    }),
    100943: _tools.RODict({
        "ID": 100943,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80321001, 6, 1], [80691001, 6, 1], [80791001, 6, 1]]),
        "props": None
    }),
    100944: _tools.RODict({
        "ID": 100944,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80321001, 4, 2], [80691001, 4, 2], [80791001, 4, 2]]),
        "props": None
    }),
    100945: _tools.RODict({
        "ID": 100945,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80321001, 5, 2], [80691001, 5, 2], [80791001, 5, 2]]),
        "props": None
    }),
    100946: _tools.RODict({
        "ID": 100946,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80321001, 6, 2], [80691001, 6, 2], [80791001, 6, 2]]),
        "props": None
    }),
    100947: _tools.RODict({
        "ID": 100947,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80321001, 7, 2], [80691001, 7, 2], [80791001, 7, 2]]),
        "props": None
    }),
    100948: _tools.RODict({
        "ID": 100948,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80321001, 4, 3], [80691001, 4, 3], [80791001, 4, 3]]),
        "props": None
    }),
    100949: _tools.RODict({
        "ID": 100949,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80321001, 5, 3], [80691001, 5, 3], [80791001, 5, 3]]),
        "props": None
    }),
    100950: _tools.RODict({
        "ID": 100950,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80321001, 6, 3], [80691001, 6, 3], [80791001, 6, 3]]),
        "props": None
    }),
    100951: _tools.RODict({
        "ID": 100951,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80321001, 7, 3], [80691001, 7, 3], [80791001, 7, 3]]),
        "props": None
    }),
    100952: _tools.RODict({
        "ID": 100952,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80321001, 4, 4], [80691001, 4, 4], [80791001, 4, 4]]),
        "props": None
    }),
    100953: _tools.RODict({
        "ID": 100953,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80321001, 5, 4], [80691001, 5, 4], [80791001, 5, 4]]),
        "props": None
    }),
    100954: _tools.RODict({
        "ID": 100954,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80321001, 6, 4], [80691001, 6, 4], [80791001, 6, 4]]),
        "props": None
    }),
    100955: _tools.RODict({
        "ID": 100955,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80321001, 7, 4], [80691001, 7, 4], [80791001, 7, 4]]),
        "props": None
    }),
    100956: _tools.RODict({
        "ID": 100956,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80221001, 4, 1], [80421001, 4, 1], [80691001, 4, 1]]),
        "props": None
    }),
    100957: _tools.RODict({
        "ID": 100957,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80221001, 5, 1], [80421001, 5, 1], [80691001, 5, 1]]),
        "props": None
    }),
    100958: _tools.RODict({
        "ID": 100958,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80221001, 6, 1], [80421001, 6, 1], [80691001, 6, 1]]),
        "props": None
    }),
    100959: _tools.RODict({
        "ID": 100959,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80221001, 4, 2], [80421001, 4, 2], [80691001, 4, 2]]),
        "props": None
    }),
    100960: _tools.RODict({
        "ID": 100960,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80221001, 5, 2], [80421001, 5, 2], [80691001, 5, 2]]),
        "props": None
    }),
    100961: _tools.RODict({
        "ID": 100961,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80221001, 6, 2], [80421001, 6, 2], [80691001, 6, 2]]),
        "props": None
    }),
    100962: _tools.RODict({
        "ID": 100962,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80221001, 7, 2], [80421001, 7, 2], [80691001, 7, 2]]),
        "props": None
    }),
    100963: _tools.RODict({
        "ID": 100963,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80221001, 4, 3], [80421001, 4, 3], [80691001, 4, 3]]),
        "props": None
    }),
    100964: _tools.RODict({
        "ID": 100964,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80221001, 5, 3], [80421001, 5, 3], [80691001, 5, 3]]),
        "props": None
    }),
    100965: _tools.RODict({
        "ID": 100965,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80221001, 6, 3], [80421001, 6, 3], [80691001, 6, 3]]),
        "props": None
    }),
    100966: _tools.RODict({
        "ID": 100966,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80221001, 7, 3], [80421001, 7, 3], [80691001, 7, 3]]),
        "props": None
    }),
    100967: _tools.RODict({
        "ID": 100967,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80221001, 4, 4], [80421001, 4, 4], [80691001, 4, 4]]),
        "props": None
    }),
    100968: _tools.RODict({
        "ID": 100968,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80221001, 5, 4], [80421001, 5, 4], [80691001, 5, 4]]),
        "props": None
    }),
    100969: _tools.RODict({
        "ID": 100969,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80221001, 6, 4], [80421001, 6, 4], [80691001, 6, 4]]),
        "props": None
    }),
    100970: _tools.RODict({
        "ID": 100970,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80221001, 7, 4], [80421001, 7, 4], [80691001, 7, 4]]),
        "props": None
    }),
    100971: _tools.RODict({
        "ID": 100971,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80121001, 4, 1], [80421001, 4, 1], [80791001, 4, 1]]),
        "props": None
    }),
    100972: _tools.RODict({
        "ID": 100972,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80121001, 5, 1], [80421001, 5, 1], [80791001, 5, 1]]),
        "props": None
    }),
    100973: _tools.RODict({
        "ID": 100973,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80121001, 6, 1], [80421001, 6, 1], [80791001, 6, 1]]),
        "props": None
    }),
    100974: _tools.RODict({
        "ID": 100974,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80121001, 4, 2], [80421001, 4, 2], [80791001, 4, 2]]),
        "props": None
    }),
    100975: _tools.RODict({
        "ID": 100975,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80121001, 5, 2], [80421001, 5, 2], [80791001, 5, 2]]),
        "props": None
    }),
    100976: _tools.RODict({
        "ID": 100976,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80121001, 6, 2], [80421001, 6, 2], [80791001, 6, 2]]),
        "props": None
    }),
    100977: _tools.RODict({
        "ID": 100977,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80121001, 7, 2], [80421001, 7, 2], [80791001, 7, 2]]),
        "props": None
    }),
    100978: _tools.RODict({
        "ID": 100978,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80121001, 4, 3], [80421001, 4, 3], [80791001, 4, 3]]),
        "props": None
    }),
    100979: _tools.RODict({
        "ID": 100979,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80121001, 5, 3], [80421001, 5, 3], [80791001, 5, 3]]),
        "props": None
    }),
    100980: _tools.RODict({
        "ID": 100980,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80121001, 6, 3], [80421001, 6, 3], [80791001, 6, 3]]),
        "props": None
    }),
    100981: _tools.RODict({
        "ID": 100981,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80121001, 7, 3], [80421001, 7, 3], [80791001, 7, 3]]),
        "props": None
    }),
    100982: _tools.RODict({
        "ID": 100982,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80121001, 4, 4], [80421001, 4, 4], [80791001, 4, 4]]),
        "props": None
    }),
    100983: _tools.RODict({
        "ID": 100983,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80121001, 5, 4], [80421001, 5, 4], [80791001, 5, 4]]),
        "props": None
    }),
    100984: _tools.RODict({
        "ID": 100984,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80121001, 6, 4], [80421001, 6, 4], [80791001, 6, 4]]),
        "props": None
    }),
    100985: _tools.RODict({
        "ID": 100985,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80121001, 7, 4], [80421001, 7, 4], [80791001, 7, 4]]),
        "props": None
    }),
    100986: _tools.RODict({
        "ID": 100986,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80321001, 4, 1], [80821001, 4, 1], [80591001, 4, 1]]),
        "props": None
    }),
    100987: _tools.RODict({
        "ID": 100987,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80321001, 5, 1], [80821001, 5, 1], [80591001, 5, 1]]),
        "props": None
    }),
    100988: _tools.RODict({
        "ID": 100988,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80321001, 6, 1], [80821001, 6, 1], [80591001, 6, 1]]),
        "props": None
    }),
    100989: _tools.RODict({
        "ID": 100989,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80321001, 4, 2], [80821001, 4, 2], [80591001, 4, 2]]),
        "props": None
    }),
    100990: _tools.RODict({
        "ID": 100990,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80321001, 5, 2], [80821001, 5, 2], [80591001, 5, 2]]),
        "props": None
    }),
    100991: _tools.RODict({
        "ID": 100991,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80321001, 6, 2], [80821001, 6, 2], [80591001, 6, 2]]),
        "props": None
    }),
    100992: _tools.RODict({
        "ID": 100992,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80321001, 7, 2], [80821001, 7, 2], [80591001, 7, 2]]),
        "props": None
    }),
    100993: _tools.RODict({
        "ID": 100993,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80321001, 4, 3], [80821001, 4, 3], [80591001, 4, 3]]),
        "props": None
    }),
    100994: _tools.RODict({
        "ID": 100994,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80321001, 5, 3], [80821001, 5, 3], [80591001, 5, 3]]),
        "props": None
    }),
    100995: _tools.RODict({
        "ID": 100995,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80321001, 6, 3], [80821001, 6, 3], [80591001, 6, 3]]),
        "props": None
    }),
    100996: _tools.RODict({
        "ID": 100996,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80321001, 7, 3], [80821001, 7, 3], [80591001, 7, 3]]),
        "props": None
    }),
    100997: _tools.RODict({
        "ID": 100997,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80321001, 4, 4], [80821001, 4, 4], [80591001, 4, 4]]),
        "props": None
    }),
    100998: _tools.RODict({
        "ID": 100998,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80321001, 5, 4], [80821001, 5, 4], [80591001, 5, 4]]),
        "props": None
    }),
    100999: _tools.RODict({
        "ID": 100999,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80321001, 6, 4], [80821001, 6, 4], [80591001, 6, 4]]),
        "props": None
    }),
    101000: _tools.RODict({
        "ID": 101000,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80321001, 7, 4], [80821001, 7, 4], [80591001, 7, 4]]),
        "props": None
    }),
    101001: _tools.RODict({
        "ID": 101001,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80121001, 3, 1], [80591001, 3, 1]]),
        "props": None
    }),
    101002: _tools.RODict({
        "ID": 101002,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80121001, 4, 1], [80591001, 4, 1]]),
        "props": None
    }),
    101003: _tools.RODict({
        "ID": 101003,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80121001, 5, 1], [80591001, 5, 1]]),
        "props": None
    }),
    101004: _tools.RODict({
        "ID": 101004,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80121001, 3, 2], [80591001, 3, 2]]),
        "props": None
    }),
    101005: _tools.RODict({
        "ID": 101005,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80121001, 4, 2], [80591001, 4, 2]]),
        "props": None
    }),
    101006: _tools.RODict({
        "ID": 101006,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80121001, 5, 2], [80591001, 5, 2]]),
        "props": None
    }),
    101007: _tools.RODict({
        "ID": 101007,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80121001, 6, 2], [80591001, 6, 2]]),
        "props": None
    }),
    101008: _tools.RODict({
        "ID": 101008,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80121001, 3, 3], [80591001, 3, 3]]),
        "props": None
    }),
    101009: _tools.RODict({
        "ID": 101009,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80121001, 4, 3], [80591001, 4, 3]]),
        "props": None
    }),
    101010: _tools.RODict({
        "ID": 101010,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80121001, 5, 3], [80591001, 5, 3]]),
        "props": None
    }),
    101011: _tools.RODict({
        "ID": 101011,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80121001, 6, 3], [80591001, 6, 3]]),
        "props": None
    }),
    101012: _tools.RODict({
        "ID": 101012,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80121001, 3, 4], [80591001, 3, 4]]),
        "props": None
    }),
    101013: _tools.RODict({
        "ID": 101013,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80121001, 4, 4], [80591001, 4, 4]]),
        "props": None
    }),
    101014: _tools.RODict({
        "ID": 101014,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80121001, 5, 4], [80591001, 5, 4]]),
        "props": None
    }),
    101015: _tools.RODict({
        "ID": 101015,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80121001, 6, 4], [80591001, 6, 4]]),
        "props": None
    }),
    101016: _tools.RODict({
        "ID": 101016,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80221001, 3, 1], [80321001, 3, 1]]),
        "props": None
    }),
    101017: _tools.RODict({
        "ID": 101017,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80221001, 4, 1], [80321001, 4, 1]]),
        "props": None
    }),
    101018: _tools.RODict({
        "ID": 101018,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80221001, 5, 1], [80321001, 5, 1]]),
        "props": None
    }),
    101019: _tools.RODict({
        "ID": 101019,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80221001, 3, 2], [80321001, 3, 2]]),
        "props": None
    }),
    101020: _tools.RODict({
        "ID": 101020,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80221001, 4, 2], [80321001, 4, 2]]),
        "props": None
    }),
    101021: _tools.RODict({
        "ID": 101021,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80221001, 5, 2], [80321001, 5, 2]]),
        "props": None
    }),
    101022: _tools.RODict({
        "ID": 101022,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80221001, 6, 2], [80321001, 6, 2]]),
        "props": None
    }),
    101023: _tools.RODict({
        "ID": 101023,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80221001, 3, 3], [80321001, 3, 3]]),
        "props": None
    }),
    101024: _tools.RODict({
        "ID": 101024,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80221001, 4, 3], [80321001, 4, 3]]),
        "props": None
    }),
    101025: _tools.RODict({
        "ID": 101025,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80221001, 5, 3], [80321001, 5, 3]]),
        "props": None
    }),
    101026: _tools.RODict({
        "ID": 101026,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80221001, 6, 3], [80321001, 6, 3]]),
        "props": None
    }),
    101027: _tools.RODict({
        "ID": 101027,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80221001, 3, 4], [80321001, 3, 4]]),
        "props": None
    }),
    101028: _tools.RODict({
        "ID": 101028,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80221001, 4, 4], [80321001, 4, 4]]),
        "props": None
    }),
    101029: _tools.RODict({
        "ID": 101029,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80221001, 5, 4], [80321001, 5, 4]]),
        "props": None
    }),
    101030: _tools.RODict({
        "ID": 101030,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80221001, 6, 4], [80321001, 6, 4]]),
        "props": None
    }),
    101031: _tools.RODict({
        "ID": 101031,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80691001, 3, 1], [80791001, 3, 1]]),
        "props": None
    }),
    101032: _tools.RODict({
        "ID": 101032,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80691001, 4, 1], [80791001, 4, 1]]),
        "props": None
    }),
    101033: _tools.RODict({
        "ID": 101033,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80691001, 5, 1], [80791001, 5, 1]]),
        "props": None
    }),
    101034: _tools.RODict({
        "ID": 101034,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80691001, 3, 2], [80791001, 3, 2]]),
        "props": None
    }),
    101035: _tools.RODict({
        "ID": 101035,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80691001, 4, 2], [80791001, 4, 2]]),
        "props": None
    }),
    101036: _tools.RODict({
        "ID": 101036,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80691001, 5, 2], [80791001, 5, 2]]),
        "props": None
    }),
    101037: _tools.RODict({
        "ID": 101037,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80691001, 6, 2], [80791001, 6, 2]]),
        "props": None
    }),
    101038: _tools.RODict({
        "ID": 101038,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80691001, 3, 3], [80791001, 3, 3]]),
        "props": None
    }),
    101039: _tools.RODict({
        "ID": 101039,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80691001, 4, 3], [80791001, 4, 3]]),
        "props": None
    }),
    101040: _tools.RODict({
        "ID": 101040,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80691001, 5, 3], [80791001, 5, 3]]),
        "props": None
    }),
    101041: _tools.RODict({
        "ID": 101041,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80691001, 6, 3], [80791001, 6, 3]]),
        "props": None
    }),
    101042: _tools.RODict({
        "ID": 101042,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80691001, 3, 4], [80791001, 3, 4]]),
        "props": None
    }),
    101043: _tools.RODict({
        "ID": 101043,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80691001, 4, 4], [80791001, 4, 4]]),
        "props": None
    }),
    101044: _tools.RODict({
        "ID": 101044,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80691001, 5, 4], [80791001, 5, 4]]),
        "props": None
    }),
    101045: _tools.RODict({
        "ID": 101045,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80691001, 6, 4], [80791001, 6, 4]]),
        "props": None
    }),
    101046: _tools.RODict({
        "ID": 101046,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80821001, 3, 1], [80421001, 3, 1]]),
        "props": None
    }),
    101047: _tools.RODict({
        "ID": 101047,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80821001, 4, 1], [80421001, 4, 1]]),
        "props": None
    }),
    101048: _tools.RODict({
        "ID": 101048,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80821001, 5, 1], [80421001, 5, 1]]),
        "props": None
    }),
    101049: _tools.RODict({
        "ID": 101049,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80821001, 3, 2], [80421001, 3, 2]]),
        "props": None
    }),
    101050: _tools.RODict({
        "ID": 101050,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80821001, 4, 2], [80421001, 4, 2]]),
        "props": None
    }),
    101051: _tools.RODict({
        "ID": 101051,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80821001, 5, 2], [80421001, 5, 2]]),
        "props": None
    }),
    101052: _tools.RODict({
        "ID": 101052,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80821001, 6, 2], [80421001, 6, 2]]),
        "props": None
    }),
    101053: _tools.RODict({
        "ID": 101053,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80821001, 3, 3], [80421001, 3, 3]]),
        "props": None
    }),
    101054: _tools.RODict({
        "ID": 101054,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80821001, 4, 3], [80421001, 4, 3]]),
        "props": None
    }),
    101055: _tools.RODict({
        "ID": 101055,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80821001, 5, 3], [80421001, 5, 3]]),
        "props": None
    }),
    101056: _tools.RODict({
        "ID": 101056,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80821001, 6, 3], [80421001, 6, 3]]),
        "props": None
    }),
    101057: _tools.RODict({
        "ID": 101057,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80821001, 3, 4], [80421001, 3, 4]]),
        "props": None
    }),
    101058: _tools.RODict({
        "ID": 101058,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80821001, 4, 4], [80421001, 4, 4]]),
        "props": None
    }),
    101059: _tools.RODict({
        "ID": 101059,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80821001, 5, 4], [80421001, 5, 4]]),
        "props": None
    }),
    101060: _tools.RODict({
        "ID": 101060,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80821001, 6, 4], [80421001, 6, 4]]),
        "props": None
    }),
    101061: _tools.RODict({
        "ID": 101061,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80121001, 3, 1], [80691001, 3, 1]]),
        "props": None
    }),
    101062: _tools.RODict({
        "ID": 101062,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80121001, 4, 1], [80691001, 4, 1]]),
        "props": None
    }),
    101063: _tools.RODict({
        "ID": 101063,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80121001, 5, 1], [80691001, 5, 1]]),
        "props": None
    }),
    101064: _tools.RODict({
        "ID": 101064,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80121001, 3, 2], [80691001, 3, 2]]),
        "props": None
    }),
    101065: _tools.RODict({
        "ID": 101065,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80121001, 4, 2], [80691001, 4, 2]]),
        "props": None
    }),
    101066: _tools.RODict({
        "ID": 101066,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80121001, 5, 2], [80691001, 5, 2]]),
        "props": None
    }),
    101067: _tools.RODict({
        "ID": 101067,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80121001, 6, 2], [80691001, 6, 2]]),
        "props": None
    }),
    101068: _tools.RODict({
        "ID": 101068,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80121001, 3, 3], [80691001, 3, 3]]),
        "props": None
    }),
    101069: _tools.RODict({
        "ID": 101069,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80121001, 4, 3], [80691001, 4, 3]]),
        "props": None
    }),
    101070: _tools.RODict({
        "ID": 101070,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80121001, 5, 3], [80691001, 5, 3]]),
        "props": None
    }),
    101071: _tools.RODict({
        "ID": 101071,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80121001, 6, 3], [80691001, 6, 3]]),
        "props": None
    }),
    101072: _tools.RODict({
        "ID": 101072,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80121001, 3, 4], [80691001, 3, 4]]),
        "props": None
    }),
    101073: _tools.RODict({
        "ID": 101073,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80121001, 4, 4], [80691001, 4, 4]]),
        "props": None
    }),
    101074: _tools.RODict({
        "ID": 101074,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80121001, 5, 4], [80691001, 5, 4]]),
        "props": None
    }),
    101075: _tools.RODict({
        "ID": 101075,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80121001, 6, 4], [80691001, 6, 4]]),
        "props": None
    }),
    101076: _tools.RODict({
        "ID": 101076,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80221001, 3, 1], [80821001, 3, 1]]),
        "props": None
    }),
    101077: _tools.RODict({
        "ID": 101077,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80221001, 4, 1], [80821001, 4, 1]]),
        "props": None
    }),
    101078: _tools.RODict({
        "ID": 101078,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80221001, 5, 1], [80821001, 5, 1]]),
        "props": None
    }),
    101079: _tools.RODict({
        "ID": 101079,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80221001, 3, 2], [80821001, 3, 2]]),
        "props": None
    }),
    101080: _tools.RODict({
        "ID": 101080,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80221001, 4, 2], [80821001, 4, 2]]),
        "props": None
    }),
    101081: _tools.RODict({
        "ID": 101081,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80221001, 5, 2], [80821001, 5, 2]]),
        "props": None
    }),
    101082: _tools.RODict({
        "ID": 101082,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80221001, 6, 2], [80821001, 6, 2]]),
        "props": None
    }),
    101083: _tools.RODict({
        "ID": 101083,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80221001, 3, 3], [80821001, 3, 3]]),
        "props": None
    }),
    101084: _tools.RODict({
        "ID": 101084,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80221001, 4, 3], [80821001, 4, 3]]),
        "props": None
    }),
    101085: _tools.RODict({
        "ID": 101085,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80221001, 5, 3], [80821001, 5, 3]]),
        "props": None
    }),
    101086: _tools.RODict({
        "ID": 101086,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80221001, 6, 3], [80821001, 6, 3]]),
        "props": None
    }),
    101087: _tools.RODict({
        "ID": 101087,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80221001, 3, 4], [80821001, 3, 4]]),
        "props": None
    }),
    101088: _tools.RODict({
        "ID": 101088,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80221001, 4, 4], [80821001, 4, 4]]),
        "props": None
    }),
    101089: _tools.RODict({
        "ID": 101089,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80221001, 5, 4], [80821001, 5, 4]]),
        "props": None
    }),
    101090: _tools.RODict({
        "ID": 101090,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80221001, 6, 4], [80821001, 6, 4]]),
        "props": None
    }),
    101091: _tools.RODict({
        "ID": 101091,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80591001, 3, 1], [80791001, 3, 1]]),
        "props": None
    }),
    101092: _tools.RODict({
        "ID": 101092,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80591001, 4, 1], [80791001, 4, 1]]),
        "props": None
    }),
    101093: _tools.RODict({
        "ID": 101093,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80591001, 5, 1], [80791001, 5, 1]]),
        "props": None
    }),
    101094: _tools.RODict({
        "ID": 101094,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80591001, 3, 2], [80791001, 3, 2]]),
        "props": None
    }),
    101095: _tools.RODict({
        "ID": 101095,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80591001, 4, 2], [80791001, 4, 2]]),
        "props": None
    }),
    101096: _tools.RODict({
        "ID": 101096,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80591001, 5, 2], [80791001, 5, 2]]),
        "props": None
    }),
    101097: _tools.RODict({
        "ID": 101097,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80591001, 6, 2], [80791001, 6, 2]]),
        "props": None
    }),
    101098: _tools.RODict({
        "ID": 101098,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80591001, 3, 3], [80791001, 3, 3]]),
        "props": None
    }),
    101099: _tools.RODict({
        "ID": 101099,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80591001, 4, 3], [80791001, 4, 3]]),
        "props": None
    }),
    101100: _tools.RODict({
        "ID": 101100,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80591001, 5, 3], [80791001, 5, 3]]),
        "props": None
    }),
    101101: _tools.RODict({
        "ID": 101101,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80591001, 6, 3], [80791001, 6, 3]]),
        "props": None
    }),
    101102: _tools.RODict({
        "ID": 101102,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80591001, 3, 4], [80791001, 3, 4]]),
        "props": None
    }),
    101103: _tools.RODict({
        "ID": 101103,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80591001, 4, 4], [80791001, 4, 4]]),
        "props": None
    }),
    101104: _tools.RODict({
        "ID": 101104,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80591001, 5, 4], [80791001, 5, 4]]),
        "props": None
    }),
    101105: _tools.RODict({
        "ID": 101105,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80591001, 6, 4], [80791001, 6, 4]]),
        "props": None
    }),
    101106: _tools.RODict({
        "ID": 101106,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80321001, 3, 1], [80421001, 3, 1]]),
        "props": None
    }),
    101107: _tools.RODict({
        "ID": 101107,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80321001, 4, 1], [80421001, 4, 1]]),
        "props": None
    }),
    101108: _tools.RODict({
        "ID": 101108,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80321001, 5, 1], [80421001, 5, 1]]),
        "props": None
    }),
    101109: _tools.RODict({
        "ID": 101109,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80321001, 3, 2], [80421001, 3, 2]]),
        "props": None
    }),
    101110: _tools.RODict({
        "ID": 101110,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80321001, 4, 2], [80421001, 4, 2]]),
        "props": None
    }),
    101111: _tools.RODict({
        "ID": 101111,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80321001, 5, 2], [80421001, 5, 2]]),
        "props": None
    }),
    101112: _tools.RODict({
        "ID": 101112,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80321001, 6, 2], [80421001, 6, 2]]),
        "props": None
    }),
    101113: _tools.RODict({
        "ID": 101113,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80321001, 3, 3], [80421001, 3, 3]]),
        "props": None
    }),
    101114: _tools.RODict({
        "ID": 101114,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80321001, 4, 3], [80421001, 4, 3]]),
        "props": None
    }),
    101115: _tools.RODict({
        "ID": 101115,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80321001, 5, 3], [80421001, 5, 3]]),
        "props": None
    }),
    101116: _tools.RODict({
        "ID": 101116,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80321001, 6, 3], [80421001, 6, 3]]),
        "props": None
    }),
    101117: _tools.RODict({
        "ID": 101117,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80321001, 3, 4], [80421001, 3, 4]]),
        "props": None
    }),
    101118: _tools.RODict({
        "ID": 101118,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80321001, 4, 4], [80421001, 4, 4]]),
        "props": None
    }),
    101119: _tools.RODict({
        "ID": 101119,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80321001, 5, 4], [80421001, 5, 4]]),
        "props": None
    }),
    101120: _tools.RODict({
        "ID": 101120,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80321001, 6, 4], [80421001, 6, 4]]),
        "props": None
    }),
    101121: _tools.RODict({
        "ID": 101121,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80121001, 3, 1], [80791001, 3, 1]]),
        "props": None
    }),
    101122: _tools.RODict({
        "ID": 101122,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80121001, 4, 1], [80791001, 4, 1]]),
        "props": None
    }),
    101123: _tools.RODict({
        "ID": 101123,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80121001, 5, 1], [80791001, 5, 1]]),
        "props": None
    }),
    101124: _tools.RODict({
        "ID": 101124,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80121001, 3, 2], [80791001, 3, 2]]),
        "props": None
    }),
    101125: _tools.RODict({
        "ID": 101125,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80121001, 4, 2], [80791001, 4, 2]]),
        "props": None
    }),
    101126: _tools.RODict({
        "ID": 101126,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80121001, 5, 2], [80791001, 5, 2]]),
        "props": None
    }),
    101127: _tools.RODict({
        "ID": 101127,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80121001, 6, 2], [80791001, 6, 2]]),
        "props": None
    }),
    101128: _tools.RODict({
        "ID": 101128,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80121001, 3, 3], [80791001, 3, 3]]),
        "props": None
    }),
    101129: _tools.RODict({
        "ID": 101129,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80121001, 4, 3], [80791001, 4, 3]]),
        "props": None
    }),
    101130: _tools.RODict({
        "ID": 101130,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80121001, 5, 3], [80791001, 5, 3]]),
        "props": None
    }),
    101131: _tools.RODict({
        "ID": 101131,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80121001, 6, 3], [80791001, 6, 3]]),
        "props": None
    }),
    101132: _tools.RODict({
        "ID": 101132,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80121001, 3, 4], [80791001, 3, 4]]),
        "props": None
    }),
    101133: _tools.RODict({
        "ID": 101133,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80121001, 4, 4], [80791001, 4, 4]]),
        "props": None
    }),
    101134: _tools.RODict({
        "ID": 101134,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80121001, 5, 4], [80791001, 5, 4]]),
        "props": None
    }),
    101135: _tools.RODict({
        "ID": 101135,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80121001, 6, 4], [80791001, 6, 4]]),
        "props": None
    }),
    101136: _tools.RODict({
        "ID": 101136,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80221001, 3, 1], [80421001, 3, 1]]),
        "props": None
    }),
    101137: _tools.RODict({
        "ID": 101137,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80221001, 4, 1], [80421001, 4, 1]]),
        "props": None
    }),
    101138: _tools.RODict({
        "ID": 101138,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80221001, 5, 1], [80421001, 5, 1]]),
        "props": None
    }),
    101139: _tools.RODict({
        "ID": 101139,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80221001, 3, 2], [80421001, 3, 2]]),
        "props": None
    }),
    101140: _tools.RODict({
        "ID": 101140,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80221001, 4, 2], [80421001, 4, 2]]),
        "props": None
    }),
    101141: _tools.RODict({
        "ID": 101141,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80221001, 5, 2], [80421001, 5, 2]]),
        "props": None
    }),
    101142: _tools.RODict({
        "ID": 101142,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80221001, 6, 2], [80421001, 6, 2]]),
        "props": None
    }),
    101143: _tools.RODict({
        "ID": 101143,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80221001, 3, 3], [80421001, 3, 3]]),
        "props": None
    }),
    101144: _tools.RODict({
        "ID": 101144,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80221001, 4, 3], [80421001, 4, 3]]),
        "props": None
    }),
    101145: _tools.RODict({
        "ID": 101145,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80221001, 5, 3], [80421001, 5, 3]]),
        "props": None
    }),
    101146: _tools.RODict({
        "ID": 101146,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80221001, 6, 3], [80421001, 6, 3]]),
        "props": None
    }),
    101147: _tools.RODict({
        "ID": 101147,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80221001, 3, 4], [80421001, 3, 4]]),
        "props": None
    }),
    101148: _tools.RODict({
        "ID": 101148,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80221001, 4, 4], [80421001, 4, 4]]),
        "props": None
    }),
    101149: _tools.RODict({
        "ID": 101149,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80221001, 5, 4], [80421001, 5, 4]]),
        "props": None
    }),
    101150: _tools.RODict({
        "ID": 101150,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80221001, 6, 4], [80421001, 6, 4]]),
        "props": None
    }),
    101151: _tools.RODict({
        "ID": 101151,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80591001, 3, 1], [80691001, 3, 1]]),
        "props": None
    }),
    101152: _tools.RODict({
        "ID": 101152,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80591001, 4, 1], [80691001, 4, 1]]),
        "props": None
    }),
    101153: _tools.RODict({
        "ID": 101153,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80591001, 5, 1], [80691001, 5, 1]]),
        "props": None
    }),
    101154: _tools.RODict({
        "ID": 101154,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80591001, 3, 2], [80691001, 3, 2]]),
        "props": None
    }),
    101155: _tools.RODict({
        "ID": 101155,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80591001, 4, 2], [80691001, 4, 2]]),
        "props": None
    }),
    101156: _tools.RODict({
        "ID": 101156,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80591001, 5, 2], [80691001, 5, 2]]),
        "props": None
    }),
    101157: _tools.RODict({
        "ID": 101157,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80591001, 6, 2], [80691001, 6, 2]]),
        "props": None
    }),
    101158: _tools.RODict({
        "ID": 101158,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80591001, 3, 3], [80691001, 3, 3]]),
        "props": None
    }),
    101159: _tools.RODict({
        "ID": 101159,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80591001, 4, 3], [80691001, 4, 3]]),
        "props": None
    }),
    101160: _tools.RODict({
        "ID": 101160,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80591001, 5, 3], [80691001, 5, 3]]),
        "props": None
    }),
    101161: _tools.RODict({
        "ID": 101161,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80591001, 6, 3], [80691001, 6, 3]]),
        "props": None
    }),
    101162: _tools.RODict({
        "ID": 101162,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80591001, 3, 4], [80691001, 3, 4]]),
        "props": None
    }),
    101163: _tools.RODict({
        "ID": 101163,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80591001, 4, 4], [80691001, 4, 4]]),
        "props": None
    }),
    101164: _tools.RODict({
        "ID": 101164,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80591001, 5, 4], [80691001, 5, 4]]),
        "props": None
    }),
    101165: _tools.RODict({
        "ID": 101165,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80591001, 6, 4], [80691001, 6, 4]]),
        "props": None
    }),
    101166: _tools.RODict({
        "ID": 101166,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80821001, 3, 1], [80321001, 3, 1]]),
        "props": None
    }),
    101167: _tools.RODict({
        "ID": 101167,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80821001, 4, 1], [80321001, 4, 1]]),
        "props": None
    }),
    101168: _tools.RODict({
        "ID": 101168,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80821001, 5, 1], [80321001, 5, 1]]),
        "props": None
    }),
    101169: _tools.RODict({
        "ID": 101169,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80821001, 3, 2], [80321001, 3, 2]]),
        "props": None
    }),
    101170: _tools.RODict({
        "ID": 101170,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80821001, 4, 2], [80321001, 4, 2]]),
        "props": None
    }),
    101171: _tools.RODict({
        "ID": 101171,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80821001, 5, 2], [80321001, 5, 2]]),
        "props": None
    }),
    101172: _tools.RODict({
        "ID": 101172,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80821001, 6, 2], [80321001, 6, 2]]),
        "props": None
    }),
    101173: _tools.RODict({
        "ID": 101173,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80821001, 3, 3], [80321001, 3, 3]]),
        "props": None
    }),
    101174: _tools.RODict({
        "ID": 101174,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80821001, 4, 3], [80321001, 4, 3]]),
        "props": None
    }),
    101175: _tools.RODict({
        "ID": 101175,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80821001, 5, 3], [80321001, 5, 3]]),
        "props": None
    }),
    101176: _tools.RODict({
        "ID": 101176,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80821001, 6, 3], [80321001, 6, 3]]),
        "props": None
    }),
    101177: _tools.RODict({
        "ID": 101177,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80821001, 3, 4], [80321001, 3, 4]]),
        "props": None
    }),
    101178: _tools.RODict({
        "ID": 101178,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80821001, 4, 4], [80321001, 4, 4]]),
        "props": None
    }),
    101179: _tools.RODict({
        "ID": 101179,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80821001, 5, 4], [80321001, 5, 4]]),
        "props": None
    }),
    101180: _tools.RODict({
        "ID": 101180,
        "unavailableClass": _tools.ROList([1001, 1003]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80821001, 6, 4], [80321001, 6, 4]]),
        "props": None
    }),
    101181: _tools.RODict({
        "ID": 101181,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":1}),
        "equipment": _tools.ROList([[80131001, 0, 1], [80581001, 0, 1], [80681001, 0, 1]]),
        "props": None
    }),
    101182: _tools.RODict({
        "ID": 101182,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":1}),
        "equipment": _tools.ROList([[80131001, 1, 1], [80581001, 1, 1], [80681001, 1, 1]]),
        "props": None
    }),
    101183: _tools.RODict({
        "ID": 101183,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":2}),
        "equipment": _tools.ROList([[80131001, 2, 1], [80581001, 2, 1], [80681001, 2, 1]]),
        "props": None
    }),
    101184: _tools.RODict({
        "ID": 101184,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":2}),
        "equipment": _tools.ROList([[80131001, 3, 1], [80581001, 3, 1], [80681001, 3, 1]]),
        "props": None
    }),
    101185: _tools.RODict({
        "ID": 101185,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":3}),
        "equipment": _tools.ROList([[80131001, 4, 1], [80581001, 4, 1], [80681001, 4, 1]]),
        "props": None
    }),
    101186: _tools.RODict({
        "ID": 101186,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":3}),
        "equipment": _tools.ROList([[80131001, 5, 1], [80581001, 5, 1], [80681001, 5, 1]]),
        "props": None
    }),
    101187: _tools.RODict({
        "ID": 101187,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":4}),
        "equipment": _tools.ROList([[80131001, 6, 1], [80581001, 6, 1], [80681001, 6, 1]]),
        "props": None
    }),
    101188: _tools.RODict({
        "ID": 101188,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":4}),
        "equipment": _tools.ROList([[80131001, 7, 1], [80581001, 7, 1], [80681001, 7, 1]]),
        "props": None
    }),
    101189: _tools.RODict({
        "ID": 101189,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":1}),
        "equipment": _tools.ROList([[80131001, 0, 2], [80581001, 0, 2], [80681001, 0, 2]]),
        "props": None
    }),
    101190: _tools.RODict({
        "ID": 101190,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":1}),
        "equipment": _tools.ROList([[80131001, 1, 2], [80581001, 1, 2], [80681001, 1, 2]]),
        "props": None
    }),
    101191: _tools.RODict({
        "ID": 101191,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":2}),
        "equipment": _tools.ROList([[80131001, 2, 2], [80581001, 2, 2], [80681001, 2, 2]]),
        "props": None
    }),
    101192: _tools.RODict({
        "ID": 101192,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":2}),
        "equipment": _tools.ROList([[80131001, 3, 2], [80581001, 3, 2], [80681001, 3, 2]]),
        "props": None
    }),
    101193: _tools.RODict({
        "ID": 101193,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":3}),
        "equipment": _tools.ROList([[80131001, 4, 2], [80581001, 4, 2], [80681001, 4, 2]]),
        "props": None
    }),
    101194: _tools.RODict({
        "ID": 101194,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":3}),
        "equipment": _tools.ROList([[80131001, 5, 2], [80581001, 5, 2], [80681001, 5, 2]]),
        "props": None
    }),
    101195: _tools.RODict({
        "ID": 101195,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":4}),
        "equipment": _tools.ROList([[80131001, 6, 2], [80581001, 6, 2], [80681001, 6, 2]]),
        "props": None
    }),
    101196: _tools.RODict({
        "ID": 101196,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":4}),
        "equipment": _tools.ROList([[80131001, 7, 2], [80581001, 7, 2], [80681001, 7, 2]]),
        "props": None
    }),
    101197: _tools.RODict({
        "ID": 101197,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":1}),
        "equipment": _tools.ROList([[80131001, 0, 3], [80581001, 0, 3], [80681001, 0, 3]]),
        "props": None
    }),
    101198: _tools.RODict({
        "ID": 101198,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":1}),
        "equipment": _tools.ROList([[80131001, 1, 3], [80581001, 1, 3], [80681001, 1, 3]]),
        "props": None
    }),
    101199: _tools.RODict({
        "ID": 101199,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":2}),
        "equipment": _tools.ROList([[80131001, 2, 3], [80581001, 2, 3], [80681001, 2, 3]]),
        "props": None
    }),
    101200: _tools.RODict({
        "ID": 101200,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":2}),
        "equipment": _tools.ROList([[80131001, 3, 3], [80581001, 3, 3], [80681001, 3, 3]]),
        "props": None
    }),
    101201: _tools.RODict({
        "ID": 101201,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":3}),
        "equipment": _tools.ROList([[80131001, 4, 3], [80581001, 4, 3], [80681001, 4, 3]]),
        "props": None
    }),
    101202: _tools.RODict({
        "ID": 101202,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":3}),
        "equipment": _tools.ROList([[80131001, 5, 3], [80581001, 5, 3], [80681001, 5, 3]]),
        "props": None
    }),
    101203: _tools.RODict({
        "ID": 101203,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":4}),
        "equipment": _tools.ROList([[80131001, 6, 3], [80581001, 6, 3], [80681001, 6, 3]]),
        "props": None
    }),
    101204: _tools.RODict({
        "ID": 101204,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":4}),
        "equipment": _tools.ROList([[80131001, 7, 3], [80581001, 7, 3], [80681001, 7, 3]]),
        "props": None
    }),
    101205: _tools.RODict({
        "ID": 101205,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":1}),
        "equipment": _tools.ROList([[80131001, 0, 4], [80581001, 0, 4], [80681001, 0, 4]]),
        "props": None
    }),
    101206: _tools.RODict({
        "ID": 101206,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":1}),
        "equipment": _tools.ROList([[80131001, 1, 4], [80581001, 1, 4], [80681001, 1, 4]]),
        "props": None
    }),
    101207: _tools.RODict({
        "ID": 101207,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":2}),
        "equipment": _tools.ROList([[80131001, 2, 4], [80581001, 2, 4], [80681001, 2, 4]]),
        "props": None
    }),
    101208: _tools.RODict({
        "ID": 101208,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":2}),
        "equipment": _tools.ROList([[80131001, 3, 4], [80581001, 3, 4], [80681001, 3, 4]]),
        "props": None
    }),
    101209: _tools.RODict({
        "ID": 101209,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":3}),
        "equipment": _tools.ROList([[80131001, 4, 4], [80581001, 4, 4], [80681001, 4, 4]]),
        "props": None
    }),
    101210: _tools.RODict({
        "ID": 101210,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":3}),
        "equipment": _tools.ROList([[80131001, 5, 4], [80581001, 5, 4], [80681001, 5, 4]]),
        "props": None
    }),
    101211: _tools.RODict({
        "ID": 101211,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":4}),
        "equipment": _tools.ROList([[80131001, 6, 4], [80581001, 6, 4], [80681001, 6, 4]]),
        "props": None
    }),
    101212: _tools.RODict({
        "ID": 101212,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMaxPhysicalAtk":4}),
        "equipment": _tools.ROList([[80131001, 7, 4], [80581001, 7, 4], [80681001, 7, 4]]),
        "props": None
    }),
    101213: _tools.RODict({
        "ID": 101213,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMinPhysicalAtk":1}),
        "equipment": _tools.ROList([[80131001, 0, 1], [80581001, 0, 1], [80781001, 0, 1]]),
        "props": None
    }),
    101214: _tools.RODict({
        "ID": 101214,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMinPhysicalAtk":1}),
        "equipment": _tools.ROList([[80131001, 1, 1], [80581001, 1, 1], [80781001, 1, 1]]),
        "props": None
    }),
    101215: _tools.RODict({
        "ID": 101215,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMinPhysicalAtk":2}),
        "equipment": _tools.ROList([[80131001, 2, 1], [80581001, 2, 1], [80781001, 2, 1]]),
        "props": None
    }),
    101216: _tools.RODict({
        "ID": 101216,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMinPhysicalAtk":2}),
        "equipment": _tools.ROList([[80131001, 3, 1], [80581001, 3, 1], [80781001, 3, 1]]),
        "props": None
    }),
    101217: _tools.RODict({
        "ID": 101217,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMinPhysicalAtk":3}),
        "equipment": _tools.ROList([[80131001, 4, 1], [80581001, 4, 1], [80781001, 4, 1]]),
        "props": None
    }),
    101218: _tools.RODict({
        "ID": 101218,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMinPhysicalAtk":3}),
        "equipment": _tools.ROList([[80131001, 5, 1], [80581001, 5, 1], [80781001, 5, 1]]),
        "props": None
    }),
    101219: _tools.RODict({
        "ID": 101219,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMinPhysicalAtk":4}),
        "equipment": _tools.ROList([[80131001, 6, 1], [80581001, 6, 1], [80781001, 6, 1]]),
        "props": None
    }),
    101220: _tools.RODict({
        "ID": 101220,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMinPhysicalAtk":4}),
        "equipment": _tools.ROList([[80131001, 7, 1], [80581001, 7, 1], [80781001, 7, 1]]),
        "props": None
    }),
    101221: _tools.RODict({
        "ID": 101221,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMinPhysicalAtk":1}),
        "equipment": _tools.ROList([[80131001, 0, 2], [80581001, 0, 2], [80781001, 0, 2]]),
        "props": None
    }),
    101222: _tools.RODict({
        "ID": 101222,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMinPhysicalAtk":1}),
        "equipment": _tools.ROList([[80131001, 1, 2], [80581001, 1, 2], [80781001, 1, 2]]),
        "props": None
    }),
    101223: _tools.RODict({
        "ID": 101223,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMinPhysicalAtk":2}),
        "equipment": _tools.ROList([[80131001, 2, 2], [80581001, 2, 2], [80781001, 2, 2]]),
        "props": None
    }),
    101224: _tools.RODict({
        "ID": 101224,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMinPhysicalAtk":2}),
        "equipment": _tools.ROList([[80131001, 3, 2], [80581001, 3, 2], [80781001, 3, 2]]),
        "props": None
    }),
    101225: _tools.RODict({
        "ID": 101225,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMinPhysicalAtk":3}),
        "equipment": _tools.ROList([[80131001, 4, 2], [80581001, 4, 2], [80781001, 4, 2]]),
        "props": None
    }),
    101226: _tools.RODict({
        "ID": 101226,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMinPhysicalAtk":3}),
        "equipment": _tools.ROList([[80131001, 5, 2], [80581001, 5, 2], [80781001, 5, 2]]),
        "props": None
    }),
    101227: _tools.RODict({
        "ID": 101227,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMinPhysicalAtk":4}),
        "equipment": _tools.ROList([[80131001, 6, 2], [80581001, 6, 2], [80781001, 6, 2]]),
        "props": None
    }),
    101228: _tools.RODict({
        "ID": 101228,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMinPhysicalAtk":4}),
        "equipment": _tools.ROList([[80131001, 7, 2], [80581001, 7, 2], [80781001, 7, 2]]),
        "props": None
    }),
    101229: _tools.RODict({
        "ID": 101229,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMinPhysicalAtk":1}),
        "equipment": _tools.ROList([[80131001, 0, 3], [80581001, 0, 3], [80781001, 0, 3]]),
        "props": None
    }),
    101230: _tools.RODict({
        "ID": 101230,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMinPhysicalAtk":1}),
        "equipment": _tools.ROList([[80131001, 1, 3], [80581001, 1, 3], [80781001, 1, 3]]),
        "props": None
    }),
    101231: _tools.RODict({
        "ID": 101231,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMinPhysicalAtk":2}),
        "equipment": _tools.ROList([[80131001, 2, 3], [80581001, 2, 3], [80781001, 2, 3]]),
        "props": None
    }),
    101232: _tools.RODict({
        "ID": 101232,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMinPhysicalAtk":2}),
        "equipment": _tools.ROList([[80131001, 3, 3], [80581001, 3, 3], [80781001, 3, 3]]),
        "props": None
    }),
    101233: _tools.RODict({
        "ID": 101233,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMinPhysicalAtk":3}),
        "equipment": _tools.ROList([[80131001, 4, 3], [80581001, 4, 3], [80781001, 4, 3]]),
        "props": None
    }),
    101234: _tools.RODict({
        "ID": 101234,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMinPhysicalAtk":3}),
        "equipment": _tools.ROList([[80131001, 5, 3], [80581001, 5, 3], [80781001, 5, 3]]),
        "props": None
    }),
    101235: _tools.RODict({
        "ID": 101235,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMinPhysicalAtk":4}),
        "equipment": _tools.ROList([[80131001, 6, 3], [80581001, 6, 3], [80781001, 6, 3]]),
        "props": None
    }),
    101236: _tools.RODict({
        "ID": 101236,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMinPhysicalAtk":4}),
        "equipment": _tools.ROList([[80131001, 7, 3], [80581001, 7, 3], [80781001, 7, 3]]),
        "props": None
    }),
    101237: _tools.RODict({
        "ID": 101237,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMinPhysicalAtk":1}),
        "equipment": _tools.ROList([[80131001, 0, 4], [80581001, 0, 4], [80781001, 0, 4]]),
        "props": None
    }),
    101238: _tools.RODict({
        "ID": 101238,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMinPhysicalAtk":1}),
        "equipment": _tools.ROList([[80131001, 1, 4], [80581001, 1, 4], [80781001, 1, 4]]),
        "props": None
    }),
    101239: _tools.RODict({
        "ID": 101239,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMinPhysicalAtk":2}),
        "equipment": _tools.ROList([[80131001, 2, 4], [80581001, 2, 4], [80781001, 2, 4]]),
        "props": None
    }),
    101240: _tools.RODict({
        "ID": 101240,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMinPhysicalAtk":2}),
        "equipment": _tools.ROList([[80131001, 3, 4], [80581001, 3, 4], [80781001, 3, 4]]),
        "props": None
    }),
    101241: _tools.RODict({
        "ID": 101241,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMinPhysicalAtk":3}),
        "equipment": _tools.ROList([[80131001, 4, 4], [80581001, 4, 4], [80781001, 4, 4]]),
        "props": None
    }),
    101242: _tools.RODict({
        "ID": 101242,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMinPhysicalAtk":3}),
        "equipment": _tools.ROList([[80131001, 5, 4], [80581001, 5, 4], [80781001, 5, 4]]),
        "props": None
    }),
    101243: _tools.RODict({
        "ID": 101243,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMinPhysicalAtk":4}),
        "equipment": _tools.ROList([[80131001, 6, 4], [80581001, 6, 4], [80781001, 6, 4]]),
        "props": None
    }),
    101244: _tools.RODict({
        "ID": 101244,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMinPhysicalAtk":4}),
        "equipment": _tools.ROList([[80131001, 7, 4], [80581001, 7, 4], [80781001, 7, 4]]),
        "props": None
    }),
    101245: _tools.RODict({
        "ID": 101245,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":30}),
        "equipment": _tools.ROList([[80131001, 0, 1], [80831001, 0, 1], [80781001, 0, 1]]),
        "props": None
    }),
    101246: _tools.RODict({
        "ID": 101246,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":45}),
        "equipment": _tools.ROList([[80131001, 1, 1], [80831001, 1, 1], [80781001, 1, 1]]),
        "props": None
    }),
    101247: _tools.RODict({
        "ID": 101247,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":60}),
        "equipment": _tools.ROList([[80131001, 2, 1], [80831001, 2, 1], [80781001, 2, 1]]),
        "props": None
    }),
    101248: _tools.RODict({
        "ID": 101248,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":75}),
        "equipment": _tools.ROList([[80131001, 3, 1], [80831001, 3, 1], [80781001, 3, 1]]),
        "props": None
    }),
    101249: _tools.RODict({
        "ID": 101249,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":90}),
        "equipment": _tools.ROList([[80131001, 4, 1], [80831001, 4, 1], [80781001, 4, 1]]),
        "props": None
    }),
    101250: _tools.RODict({
        "ID": 101250,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":120}),
        "equipment": _tools.ROList([[80131001, 5, 1], [80831001, 5, 1], [80781001, 5, 1]]),
        "props": None
    }),
    101251: _tools.RODict({
        "ID": 101251,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":160}),
        "equipment": _tools.ROList([[80131001, 6, 1], [80831001, 6, 1], [80781001, 6, 1]]),
        "props": None
    }),
    101252: _tools.RODict({
        "ID": 101252,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":250}),
        "equipment": _tools.ROList([[80131001, 7, 1], [80831001, 7, 1], [80781001, 7, 1]]),
        "props": None
    }),
    101253: _tools.RODict({
        "ID": 101253,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":60}),
        "equipment": _tools.ROList([[80131001, 0, 2], [80831001, 0, 2], [80781001, 0, 2]]),
        "props": None
    }),
    101254: _tools.RODict({
        "ID": 101254,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":75}),
        "equipment": _tools.ROList([[80131001, 1, 2], [80831001, 1, 2], [80781001, 1, 2]]),
        "props": None
    }),
    101255: _tools.RODict({
        "ID": 101255,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":90}),
        "equipment": _tools.ROList([[80131001, 2, 2], [80831001, 2, 2], [80781001, 2, 2]]),
        "props": None
    }),
    101256: _tools.RODict({
        "ID": 101256,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":105}),
        "equipment": _tools.ROList([[80131001, 3, 2], [80831001, 3, 2], [80781001, 3, 2]]),
        "props": None
    }),
    101257: _tools.RODict({
        "ID": 101257,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":120}),
        "equipment": _tools.ROList([[80131001, 4, 2], [80831001, 4, 2], [80781001, 4, 2]]),
        "props": None
    }),
    101258: _tools.RODict({
        "ID": 101258,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":150}),
        "equipment": _tools.ROList([[80131001, 5, 2], [80831001, 5, 2], [80781001, 5, 2]]),
        "props": None
    }),
    101259: _tools.RODict({
        "ID": 101259,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":190}),
        "equipment": _tools.ROList([[80131001, 6, 2], [80831001, 6, 2], [80781001, 6, 2]]),
        "props": None
    }),
    101260: _tools.RODict({
        "ID": 101260,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":300}),
        "equipment": _tools.ROList([[80131001, 7, 2], [80831001, 7, 2], [80781001, 7, 2]]),
        "props": None
    }),
    101261: _tools.RODict({
        "ID": 101261,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":90}),
        "equipment": _tools.ROList([[80131001, 0, 3], [80831001, 0, 3], [80781001, 0, 3]]),
        "props": None
    }),
    101262: _tools.RODict({
        "ID": 101262,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":105}),
        "equipment": _tools.ROList([[80131001, 1, 3], [80831001, 1, 3], [80781001, 1, 3]]),
        "props": None
    }),
    101263: _tools.RODict({
        "ID": 101263,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":120}),
        "equipment": _tools.ROList([[80131001, 2, 3], [80831001, 2, 3], [80781001, 2, 3]]),
        "props": None
    }),
    101264: _tools.RODict({
        "ID": 101264,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":140}),
        "equipment": _tools.ROList([[80131001, 3, 3], [80831001, 3, 3], [80781001, 3, 3]]),
        "props": None
    }),
    101265: _tools.RODict({
        "ID": 101265,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":155}),
        "equipment": _tools.ROList([[80131001, 4, 3], [80831001, 4, 3], [80781001, 4, 3]]),
        "props": None
    }),
    101266: _tools.RODict({
        "ID": 101266,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":185}),
        "equipment": _tools.ROList([[80131001, 5, 3], [80831001, 5, 3], [80781001, 5, 3]]),
        "props": None
    }),
    101267: _tools.RODict({
        "ID": 101267,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":225}),
        "equipment": _tools.ROList([[80131001, 6, 3], [80831001, 6, 3], [80781001, 6, 3]]),
        "props": None
    }),
    101268: _tools.RODict({
        "ID": 101268,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":350}),
        "equipment": _tools.ROList([[80131001, 7, 3], [80831001, 7, 3], [80781001, 7, 3]]),
        "props": None
    }),
    101269: _tools.RODict({
        "ID": 101269,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":130}),
        "equipment": _tools.ROList([[80131001, 0, 4], [80831001, 0, 4], [80781001, 0, 4]]),
        "props": None
    }),
    101270: _tools.RODict({
        "ID": 101270,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":145}),
        "equipment": _tools.ROList([[80131001, 1, 4], [80831001, 1, 4], [80781001, 1, 4]]),
        "props": None
    }),
    101271: _tools.RODict({
        "ID": 101271,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":160}),
        "equipment": _tools.ROList([[80131001, 2, 4], [80831001, 2, 4], [80781001, 2, 4]]),
        "props": None
    }),
    101272: _tools.RODict({
        "ID": 101272,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":180}),
        "equipment": _tools.ROList([[80131001, 3, 4], [80831001, 3, 4], [80781001, 3, 4]]),
        "props": None
    }),
    101273: _tools.RODict({
        "ID": 101273,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":200}),
        "equipment": _tools.ROList([[80131001, 4, 4], [80831001, 4, 4], [80781001, 4, 4]]),
        "props": None
    }),
    101274: _tools.RODict({
        "ID": 101274,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":225}),
        "equipment": _tools.ROList([[80131001, 5, 4], [80831001, 5, 4], [80781001, 5, 4]]),
        "props": None
    }),
    101275: _tools.RODict({
        "ID": 101275,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":270}),
        "equipment": _tools.ROList([[80131001, 6, 4], [80831001, 6, 4], [80781001, 6, 4]]),
        "props": None
    }),
    101276: _tools.RODict({
        "ID": 101276,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullHp":400}),
        "equipment": _tools.ROList([[80131001, 7, 4], [80831001, 7, 4], [80781001, 7, 4]]),
        "props": None
    }),
    101277: _tools.RODict({
        "ID": 101277,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullMp":3}),
        "equipment": _tools.ROList([[80131001, 0, 1], [80581001, 0, 1], [80681001, 0, 1]]),
        "props": None
    }),
    101278: _tools.RODict({
        "ID": 101278,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullMp":4}),
        "equipment": _tools.ROList([[80131001, 1, 1], [80581001, 1, 1], [80681001, 1, 1]]),
        "props": None
    }),
    101279: _tools.RODict({
        "ID": 101279,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullMp":6}),
        "equipment": _tools.ROList([[80131001, 2, 1], [80581001, 2, 1], [80681001, 2, 1]]),
        "props": None
    }),
    101280: _tools.RODict({
        "ID": 101280,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullMp":8}),
        "equipment": _tools.ROList([[80131001, 3, 1], [80581001, 3, 1], [80681001, 3, 1]]),
        "props": None
    }),
    101281: _tools.RODict({
        "ID": 101281,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullMp":9}),
        "equipment": _tools.ROList([[80131001, 4, 1], [80581001, 4, 1], [80681001, 4, 1]]),
        "props": None
    }),
    101282: _tools.RODict({
        "ID": 101282,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullMp":13}),
        "equipment": _tools.ROList([[80131001, 5, 1], [80581001, 5, 1], [80681001, 5, 1]]),
        "props": None
    }),
    101283: _tools.RODict({
        "ID": 101283,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullMp":17}),
        "equipment": _tools.ROList([[80131001, 6, 1], [80581001, 6, 1], [80681001, 6, 1]]),
        "props": None
    }),
    101284: _tools.RODict({
        "ID": 101284,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullMp":26}),
        "equipment": _tools.ROList([[80131001, 7, 1], [80581001, 7, 1], [80681001, 7, 1]]),
        "props": None
    }),
    101285: _tools.RODict({
        "ID": 101285,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullMp":6}),
        "equipment": _tools.ROList([[80131001, 0, 2], [80581001, 0, 2], [80681001, 0, 2]]),
        "props": None
    }),
    101286: _tools.RODict({
        "ID": 101286,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullMp":8}),
        "equipment": _tools.ROList([[80131001, 1, 2], [80581001, 1, 2], [80681001, 1, 2]]),
        "props": None
    }),
    101287: _tools.RODict({
        "ID": 101287,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullMp":9}),
        "equipment": _tools.ROList([[80131001, 2, 2], [80581001, 2, 2], [80681001, 2, 2]]),
        "props": None
    }),
    101288: _tools.RODict({
        "ID": 101288,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullMp":12}),
        "equipment": _tools.ROList([[80131001, 3, 2], [80581001, 3, 2], [80681001, 3, 2]]),
        "props": None
    }),
    101289: _tools.RODict({
        "ID": 101289,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullMp":13}),
        "equipment": _tools.ROList([[80131001, 4, 2], [80581001, 4, 2], [80681001, 4, 2]]),
        "props": None
    }),
    101290: _tools.RODict({
        "ID": 101290,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullMp":16}),
        "equipment": _tools.ROList([[80131001, 5, 2], [80581001, 5, 2], [80681001, 5, 2]]),
        "props": None
    }),
    101291: _tools.RODict({
        "ID": 101291,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullMp":19}),
        "equipment": _tools.ROList([[80131001, 6, 2], [80581001, 6, 2], [80681001, 6, 2]]),
        "props": None
    }),
    101292: _tools.RODict({
        "ID": 101292,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullMp":28}),
        "equipment": _tools.ROList([[80131001, 7, 2], [80581001, 7, 2], [80681001, 7, 2]]),
        "props": None
    }),
    101293: _tools.RODict({
        "ID": 101293,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullMp":9}),
        "equipment": _tools.ROList([[80131001, 0, 3], [80581001, 0, 3], [80681001, 0, 3]]),
        "props": None
    }),
    101294: _tools.RODict({
        "ID": 101294,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullMp":11}),
        "equipment": _tools.ROList([[80131001, 1, 3], [80581001, 1, 3], [80681001, 1, 3]]),
        "props": None
    }),
    101295: _tools.RODict({
        "ID": 101295,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullMp":13}),
        "equipment": _tools.ROList([[80131001, 2, 3], [80581001, 2, 3], [80681001, 2, 3]]),
        "props": None
    }),
    101296: _tools.RODict({
        "ID": 101296,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullMp":14}),
        "equipment": _tools.ROList([[80131001, 3, 3], [80581001, 3, 3], [80681001, 3, 3]]),
        "props": None
    }),
    101297: _tools.RODict({
        "ID": 101297,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullMp":16}),
        "equipment": _tools.ROList([[80131001, 4, 3], [80581001, 4, 3], [80681001, 4, 3]]),
        "props": None
    }),
    101298: _tools.RODict({
        "ID": 101298,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullMp":19}),
        "equipment": _tools.ROList([[80131001, 5, 3], [80581001, 5, 3], [80681001, 5, 3]]),
        "props": None
    }),
    101299: _tools.RODict({
        "ID": 101299,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullMp":23}),
        "equipment": _tools.ROList([[80131001, 6, 3], [80581001, 6, 3], [80681001, 6, 3]]),
        "props": None
    }),
    101300: _tools.RODict({
        "ID": 101300,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullMp":32}),
        "equipment": _tools.ROList([[80131001, 7, 3], [80581001, 7, 3], [80681001, 7, 3]]),
        "props": None
    }),
    101301: _tools.RODict({
        "ID": 101301,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullMp":13}),
        "equipment": _tools.ROList([[80131001, 0, 4], [80581001, 0, 4], [80681001, 0, 4]]),
        "props": None
    }),
    101302: _tools.RODict({
        "ID": 101302,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullMp":14}),
        "equipment": _tools.ROList([[80131001, 1, 4], [80581001, 1, 4], [80681001, 1, 4]]),
        "props": None
    }),
    101303: _tools.RODict({
        "ID": 101303,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullMp":16}),
        "equipment": _tools.ROList([[80131001, 2, 4], [80581001, 2, 4], [80681001, 2, 4]]),
        "props": None
    }),
    101304: _tools.RODict({
        "ID": 101304,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullMp":18}),
        "equipment": _tools.ROList([[80131001, 3, 4], [80581001, 3, 4], [80681001, 3, 4]]),
        "props": None
    }),
    101305: _tools.RODict({
        "ID": 101305,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullMp":19}),
        "equipment": _tools.ROList([[80131001, 4, 4], [80581001, 4, 4], [80681001, 4, 4]]),
        "props": None
    }),
    101306: _tools.RODict({
        "ID": 101306,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullMp":23}),
        "equipment": _tools.ROList([[80131001, 5, 4], [80581001, 5, 4], [80681001, 5, 4]]),
        "props": None
    }),
    101307: _tools.RODict({
        "ID": 101307,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullMp":25}),
        "equipment": _tools.ROList([[80131001, 6, 4], [80581001, 6, 4], [80681001, 6, 4]]),
        "props": None
    }),
    101308: _tools.RODict({
        "ID": 101308,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFullMp":38}),
        "equipment": _tools.ROList([[80131001, 7, 4], [80581001, 7, 4], [80681001, 7, 4]]),
        "props": None
    }),
    101309: _tools.RODict({
        "ID": 101309,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.001}),
        "equipment": _tools.ROList([[80131001, 0, 1], [80431001, 0, 1], [80681001, 0, 1]]),
        "props": None
    }),
    101310: _tools.RODict({
        "ID": 101310,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.001}),
        "equipment": _tools.ROList([[80131001, 1, 1], [80431001, 1, 1], [80681001, 1, 1]]),
        "props": None
    }),
    101311: _tools.RODict({
        "ID": 101311,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.0015}),
        "equipment": _tools.ROList([[80131001, 2, 1], [80431001, 2, 1], [80681001, 2, 1]]),
        "props": None
    }),
    101312: _tools.RODict({
        "ID": 101312,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.002}),
        "equipment": _tools.ROList([[80131001, 3, 1], [80431001, 3, 1], [80681001, 3, 1]]),
        "props": None
    }),
    101313: _tools.RODict({
        "ID": 101313,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.003}),
        "equipment": _tools.ROList([[80131001, 4, 1], [80431001, 4, 1], [80681001, 4, 1]]),
        "props": None
    }),
    101314: _tools.RODict({
        "ID": 101314,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.004}),
        "equipment": _tools.ROList([[80131001, 5, 1], [80431001, 5, 1], [80681001, 5, 1]]),
        "props": None
    }),
    101315: _tools.RODict({
        "ID": 101315,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.005}),
        "equipment": _tools.ROList([[80131001, 6, 1], [80431001, 6, 1], [80681001, 6, 1]]),
        "props": None
    }),
    101316: _tools.RODict({
        "ID": 101316,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.0075}),
        "equipment": _tools.ROList([[80131001, 7, 1], [80431001, 7, 1], [80681001, 7, 1]]),
        "props": None
    }),
    101317: _tools.RODict({
        "ID": 101317,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.0015}),
        "equipment": _tools.ROList([[80131001, 0, 2], [80431001, 0, 2], [80681001, 0, 2]]),
        "props": None
    }),
    101318: _tools.RODict({
        "ID": 101318,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.0015}),
        "equipment": _tools.ROList([[80131001, 1, 2], [80431001, 1, 2], [80681001, 1, 2]]),
        "props": None
    }),
    101319: _tools.RODict({
        "ID": 101319,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.002}),
        "equipment": _tools.ROList([[80131001, 2, 2], [80431001, 2, 2], [80681001, 2, 2]]),
        "props": None
    }),
    101320: _tools.RODict({
        "ID": 101320,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.0025}),
        "equipment": _tools.ROList([[80131001, 3, 2], [80431001, 3, 2], [80681001, 3, 2]]),
        "props": None
    }),
    101321: _tools.RODict({
        "ID": 101321,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.0035}),
        "equipment": _tools.ROList([[80131001, 4, 2], [80431001, 4, 2], [80681001, 4, 2]]),
        "props": None
    }),
    101322: _tools.RODict({
        "ID": 101322,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.0045}),
        "equipment": _tools.ROList([[80131001, 5, 2], [80431001, 5, 2], [80681001, 5, 2]]),
        "props": None
    }),
    101323: _tools.RODict({
        "ID": 101323,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.0055}),
        "equipment": _tools.ROList([[80131001, 6, 2], [80431001, 6, 2], [80681001, 6, 2]]),
        "props": None
    }),
    101324: _tools.RODict({
        "ID": 101324,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.008}),
        "equipment": _tools.ROList([[80131001, 7, 2], [80431001, 7, 2], [80681001, 7, 2]]),
        "props": None
    }),
    101325: _tools.RODict({
        "ID": 101325,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.002}),
        "equipment": _tools.ROList([[80131001, 0, 3], [80431001, 0, 3], [80681001, 0, 3]]),
        "props": None
    }),
    101326: _tools.RODict({
        "ID": 101326,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.0025}),
        "equipment": _tools.ROList([[80131001, 1, 3], [80431001, 1, 3], [80681001, 1, 3]]),
        "props": None
    }),
    101327: _tools.RODict({
        "ID": 101327,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.0025}),
        "equipment": _tools.ROList([[80131001, 2, 3], [80431001, 2, 3], [80681001, 2, 3]]),
        "props": None
    }),
    101328: _tools.RODict({
        "ID": 101328,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.003}),
        "equipment": _tools.ROList([[80131001, 3, 3], [80431001, 3, 3], [80681001, 3, 3]]),
        "props": None
    }),
    101329: _tools.RODict({
        "ID": 101329,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.004}),
        "equipment": _tools.ROList([[80131001, 4, 3], [80431001, 4, 3], [80681001, 4, 3]]),
        "props": None
    }),
    101330: _tools.RODict({
        "ID": 101330,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.005}),
        "equipment": _tools.ROList([[80131001, 5, 3], [80431001, 5, 3], [80681001, 5, 3]]),
        "props": None
    }),
    101331: _tools.RODict({
        "ID": 101331,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.006}),
        "equipment": _tools.ROList([[80131001, 6, 3], [80431001, 6, 3], [80681001, 6, 3]]),
        "props": None
    }),
    101332: _tools.RODict({
        "ID": 101332,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.0085}),
        "equipment": _tools.ROList([[80131001, 7, 3], [80431001, 7, 3], [80681001, 7, 3]]),
        "props": None
    }),
    101333: _tools.RODict({
        "ID": 101333,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.0025}),
        "equipment": _tools.ROList([[80131001, 0, 4], [80431001, 0, 4], [80681001, 0, 4]]),
        "props": None
    }),
    101334: _tools.RODict({
        "ID": 101334,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.003}),
        "equipment": _tools.ROList([[80131001, 1, 4], [80431001, 1, 4], [80681001, 1, 4]]),
        "props": None
    }),
    101335: _tools.RODict({
        "ID": 101335,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.003}),
        "equipment": _tools.ROList([[80131001, 2, 4], [80431001, 2, 4], [80681001, 2, 4]]),
        "props": None
    }),
    101336: _tools.RODict({
        "ID": 101336,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.0035}),
        "equipment": _tools.ROList([[80131001, 3, 4], [80431001, 3, 4], [80681001, 3, 4]]),
        "props": None
    }),
    101337: _tools.RODict({
        "ID": 101337,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.0045}),
        "equipment": _tools.ROList([[80131001, 4, 4], [80431001, 4, 4], [80681001, 4, 4]]),
        "props": None
    }),
    101338: _tools.RODict({
        "ID": 101338,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.0055}),
        "equipment": _tools.ROList([[80131001, 5, 4], [80431001, 5, 4], [80681001, 5, 4]]),
        "props": None
    }),
    101339: _tools.RODict({
        "ID": 101339,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.0065}),
        "equipment": _tools.ROList([[80131001, 6, 4], [80431001, 6, 4], [80681001, 6, 4]]),
        "props": None
    }),
    101340: _tools.RODict({
        "ID": 101340,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmg":0.009}),
        "equipment": _tools.ROList([[80131001, 7, 4], [80431001, 7, 4], [80681001, 7, 4]]),
        "props": None
    }),
    101341: _tools.RODict({
        "ID": 101341,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.001}),
        "equipment": _tools.ROList([[80131001, 0, 1], [80831001, 0, 1], [80431001, 0, 1]]),
        "props": None
    }),
    101342: _tools.RODict({
        "ID": 101342,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.001}),
        "equipment": _tools.ROList([[80131001, 1, 1], [80831001, 1, 1], [80431001, 1, 1]]),
        "props": None
    }),
    101343: _tools.RODict({
        "ID": 101343,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80131001, 2, 1], [80831001, 2, 1], [80431001, 2, 1]]),
        "props": None
    }),
    101344: _tools.RODict({
        "ID": 101344,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.002}),
        "equipment": _tools.ROList([[80131001, 3, 1], [80831001, 3, 1], [80431001, 3, 1]]),
        "props": None
    }),
    101345: _tools.RODict({
        "ID": 101345,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.003}),
        "equipment": _tools.ROList([[80131001, 4, 1], [80831001, 4, 1], [80431001, 4, 1]]),
        "props": None
    }),
    101346: _tools.RODict({
        "ID": 101346,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.004}),
        "equipment": _tools.ROList([[80131001, 5, 1], [80831001, 5, 1], [80431001, 5, 1]]),
        "props": None
    }),
    101347: _tools.RODict({
        "ID": 101347,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.005}),
        "equipment": _tools.ROList([[80131001, 6, 1], [80831001, 6, 1], [80431001, 6, 1]]),
        "props": None
    }),
    101348: _tools.RODict({
        "ID": 101348,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0075}),
        "equipment": _tools.ROList([[80131001, 7, 1], [80831001, 7, 1], [80431001, 7, 1]]),
        "props": None
    }),
    101349: _tools.RODict({
        "ID": 101349,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80131001, 0, 2], [80831001, 0, 2], [80431001, 0, 2]]),
        "props": None
    }),
    101350: _tools.RODict({
        "ID": 101350,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80131001, 1, 2], [80831001, 1, 2], [80431001, 1, 2]]),
        "props": None
    }),
    101351: _tools.RODict({
        "ID": 101351,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.002}),
        "equipment": _tools.ROList([[80131001, 2, 2], [80831001, 2, 2], [80431001, 2, 2]]),
        "props": None
    }),
    101352: _tools.RODict({
        "ID": 101352,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80131001, 3, 2], [80831001, 3, 2], [80431001, 3, 2]]),
        "props": None
    }),
    101353: _tools.RODict({
        "ID": 101353,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0035}),
        "equipment": _tools.ROList([[80131001, 4, 2], [80831001, 4, 2], [80431001, 4, 2]]),
        "props": None
    }),
    101354: _tools.RODict({
        "ID": 101354,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0045}),
        "equipment": _tools.ROList([[80131001, 5, 2], [80831001, 5, 2], [80431001, 5, 2]]),
        "props": None
    }),
    101355: _tools.RODict({
        "ID": 101355,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0055}),
        "equipment": _tools.ROList([[80131001, 6, 2], [80831001, 6, 2], [80431001, 6, 2]]),
        "props": None
    }),
    101356: _tools.RODict({
        "ID": 101356,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.008}),
        "equipment": _tools.ROList([[80131001, 7, 2], [80831001, 7, 2], [80431001, 7, 2]]),
        "props": None
    }),
    101357: _tools.RODict({
        "ID": 101357,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.002}),
        "equipment": _tools.ROList([[80131001, 0, 3], [80831001, 0, 3], [80431001, 0, 3]]),
        "props": None
    }),
    101358: _tools.RODict({
        "ID": 101358,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80131001, 1, 3], [80831001, 1, 3], [80431001, 1, 3]]),
        "props": None
    }),
    101359: _tools.RODict({
        "ID": 101359,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80131001, 2, 3], [80831001, 2, 3], [80431001, 2, 3]]),
        "props": None
    }),
    101360: _tools.RODict({
        "ID": 101360,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.003}),
        "equipment": _tools.ROList([[80131001, 3, 3], [80831001, 3, 3], [80431001, 3, 3]]),
        "props": None
    }),
    101361: _tools.RODict({
        "ID": 101361,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.004}),
        "equipment": _tools.ROList([[80131001, 4, 3], [80831001, 4, 3], [80431001, 4, 3]]),
        "props": None
    }),
    101362: _tools.RODict({
        "ID": 101362,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.005}),
        "equipment": _tools.ROList([[80131001, 5, 3], [80831001, 5, 3], [80431001, 5, 3]]),
        "props": None
    }),
    101363: _tools.RODict({
        "ID": 101363,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.006}),
        "equipment": _tools.ROList([[80131001, 6, 3], [80831001, 6, 3], [80431001, 6, 3]]),
        "props": None
    }),
    101364: _tools.RODict({
        "ID": 101364,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0085}),
        "equipment": _tools.ROList([[80131001, 7, 3], [80831001, 7, 3], [80431001, 7, 3]]),
        "props": None
    }),
    101365: _tools.RODict({
        "ID": 101365,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80131001, 0, 4], [80831001, 0, 4], [80431001, 0, 4]]),
        "props": None
    }),
    101366: _tools.RODict({
        "ID": 101366,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.003}),
        "equipment": _tools.ROList([[80131001, 1, 4], [80831001, 1, 4], [80431001, 1, 4]]),
        "props": None
    }),
    101367: _tools.RODict({
        "ID": 101367,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.003}),
        "equipment": _tools.ROList([[80131001, 2, 4], [80831001, 2, 4], [80431001, 2, 4]]),
        "props": None
    }),
    101368: _tools.RODict({
        "ID": 101368,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0035}),
        "equipment": _tools.ROList([[80131001, 3, 4], [80831001, 3, 4], [80431001, 3, 4]]),
        "props": None
    }),
    101369: _tools.RODict({
        "ID": 101369,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0045}),
        "equipment": _tools.ROList([[80131001, 4, 4], [80831001, 4, 4], [80431001, 4, 4]]),
        "props": None
    }),
    101370: _tools.RODict({
        "ID": 101370,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0055}),
        "equipment": _tools.ROList([[80131001, 5, 4], [80831001, 5, 4], [80431001, 5, 4]]),
        "props": None
    }),
    101371: _tools.RODict({
        "ID": 101371,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0065}),
        "equipment": _tools.ROList([[80131001, 6, 4], [80831001, 6, 4], [80431001, 6, 4]]),
        "props": None
    }),
    101372: _tools.RODict({
        "ID": 101372,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPVPDmgAnti":0.009}),
        "equipment": _tools.ROList([[80131001, 7, 4], [80831001, 7, 4], [80431001, 7, 4]]),
        "props": None
    }),
    101373: _tools.RODict({
        "ID": 101373,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.001}),
        "equipment": _tools.ROList([[80331001, 0, 1], [80831001, 0, 1], [80431001, 0, 1]]),
        "props": None
    }),
    101374: _tools.RODict({
        "ID": 101374,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.001}),
        "equipment": _tools.ROList([[80331001, 1, 1], [80831001, 1, 1], [80431001, 1, 1]]),
        "props": None
    }),
    101375: _tools.RODict({
        "ID": 101375,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80331001, 2, 1], [80831001, 2, 1], [80431001, 2, 1]]),
        "props": None
    }),
    101376: _tools.RODict({
        "ID": 101376,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.002}),
        "equipment": _tools.ROList([[80331001, 3, 1], [80831001, 3, 1], [80431001, 3, 1]]),
        "props": None
    }),
    101377: _tools.RODict({
        "ID": 101377,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.003}),
        "equipment": _tools.ROList([[80331001, 4, 1], [80831001, 4, 1], [80431001, 4, 1]]),
        "props": None
    }),
    101378: _tools.RODict({
        "ID": 101378,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.004}),
        "equipment": _tools.ROList([[80331001, 5, 1], [80831001, 5, 1], [80431001, 5, 1]]),
        "props": None
    }),
    101379: _tools.RODict({
        "ID": 101379,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.005}),
        "equipment": _tools.ROList([[80331001, 6, 1], [80831001, 6, 1], [80431001, 6, 1]]),
        "props": None
    }),
    101380: _tools.RODict({
        "ID": 101380,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0075}),
        "equipment": _tools.ROList([[80331001, 7, 1], [80831001, 7, 1], [80431001, 7, 1]]),
        "props": None
    }),
    101381: _tools.RODict({
        "ID": 101381,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80331001, 0, 2], [80831001, 0, 2], [80431001, 0, 2]]),
        "props": None
    }),
    101382: _tools.RODict({
        "ID": 101382,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0015}),
        "equipment": _tools.ROList([[80331001, 1, 2], [80831001, 1, 2], [80431001, 1, 2]]),
        "props": None
    }),
    101383: _tools.RODict({
        "ID": 101383,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.002}),
        "equipment": _tools.ROList([[80331001, 2, 2], [80831001, 2, 2], [80431001, 2, 2]]),
        "props": None
    }),
    101384: _tools.RODict({
        "ID": 101384,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80331001, 3, 2], [80831001, 3, 2], [80431001, 3, 2]]),
        "props": None
    }),
    101385: _tools.RODict({
        "ID": 101385,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0035}),
        "equipment": _tools.ROList([[80331001, 4, 2], [80831001, 4, 2], [80431001, 4, 2]]),
        "props": None
    }),
    101386: _tools.RODict({
        "ID": 101386,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0045}),
        "equipment": _tools.ROList([[80331001, 5, 2], [80831001, 5, 2], [80431001, 5, 2]]),
        "props": None
    }),
    101387: _tools.RODict({
        "ID": 101387,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0055}),
        "equipment": _tools.ROList([[80331001, 6, 2], [80831001, 6, 2], [80431001, 6, 2]]),
        "props": None
    }),
    101388: _tools.RODict({
        "ID": 101388,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.008}),
        "equipment": _tools.ROList([[80331001, 7, 2], [80831001, 7, 2], [80431001, 7, 2]]),
        "props": None
    }),
    101389: _tools.RODict({
        "ID": 101389,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.002}),
        "equipment": _tools.ROList([[80331001, 0, 3], [80831001, 0, 3], [80431001, 0, 3]]),
        "props": None
    }),
    101390: _tools.RODict({
        "ID": 101390,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80331001, 1, 3], [80831001, 1, 3], [80431001, 1, 3]]),
        "props": None
    }),
    101391: _tools.RODict({
        "ID": 101391,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80331001, 2, 3], [80831001, 2, 3], [80431001, 2, 3]]),
        "props": None
    }),
    101392: _tools.RODict({
        "ID": 101392,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.003}),
        "equipment": _tools.ROList([[80331001, 3, 3], [80831001, 3, 3], [80431001, 3, 3]]),
        "props": None
    }),
    101393: _tools.RODict({
        "ID": 101393,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.004}),
        "equipment": _tools.ROList([[80331001, 4, 3], [80831001, 4, 3], [80431001, 4, 3]]),
        "props": None
    }),
    101394: _tools.RODict({
        "ID": 101394,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.005}),
        "equipment": _tools.ROList([[80331001, 5, 3], [80831001, 5, 3], [80431001, 5, 3]]),
        "props": None
    }),
    101395: _tools.RODict({
        "ID": 101395,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.006}),
        "equipment": _tools.ROList([[80331001, 6, 3], [80831001, 6, 3], [80431001, 6, 3]]),
        "props": None
    }),
    101396: _tools.RODict({
        "ID": 101396,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0085}),
        "equipment": _tools.ROList([[80331001, 7, 3], [80831001, 7, 3], [80431001, 7, 3]]),
        "props": None
    }),
    101397: _tools.RODict({
        "ID": 101397,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0025}),
        "equipment": _tools.ROList([[80331001, 0, 4], [80831001, 0, 4], [80431001, 0, 4]]),
        "props": None
    }),
    101398: _tools.RODict({
        "ID": 101398,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.003}),
        "equipment": _tools.ROList([[80331001, 1, 4], [80831001, 1, 4], [80431001, 1, 4]]),
        "props": None
    }),
    101399: _tools.RODict({
        "ID": 101399,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.003}),
        "equipment": _tools.ROList([[80331001, 2, 4], [80831001, 2, 4], [80431001, 2, 4]]),
        "props": None
    }),
    101400: _tools.RODict({
        "ID": 101400,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0035}),
        "equipment": _tools.ROList([[80331001, 3, 4], [80831001, 3, 4], [80431001, 3, 4]]),
        "props": None
    }),
    101401: _tools.RODict({
        "ID": 101401,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0045}),
        "equipment": _tools.ROList([[80331001, 4, 4], [80831001, 4, 4], [80431001, 4, 4]]),
        "props": None
    }),
    101402: _tools.RODict({
        "ID": 101402,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0055}),
        "equipment": _tools.ROList([[80331001, 5, 4], [80831001, 5, 4], [80431001, 5, 4]]),
        "props": None
    }),
    101403: _tools.RODict({
        "ID": 101403,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0065}),
        "equipment": _tools.ROList([[80331001, 6, 4], [80831001, 6, 4], [80431001, 6, 4]]),
        "props": None
    }),
    101404: _tools.RODict({
        "ID": 101404,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.009}),
        "equipment": _tools.ROList([[80331001, 7, 4], [80831001, 7, 4], [80431001, 7, 4]]),
        "props": None
    }),
    101405: _tools.RODict({
        "ID": 101405,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.001}),
        "equipment": _tools.ROList([[80831001, 0, 1], [80581001, 0, 1], [80781001, 0, 1]]),
        "props": None
    }),
    101406: _tools.RODict({
        "ID": 101406,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.001}),
        "equipment": _tools.ROList([[80831001, 1, 1], [80581001, 1, 1], [80781001, 1, 1]]),
        "props": None
    }),
    101407: _tools.RODict({
        "ID": 101407,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0015}),
        "equipment": _tools.ROList([[80831001, 2, 1], [80581001, 2, 1], [80781001, 2, 1]]),
        "props": None
    }),
    101408: _tools.RODict({
        "ID": 101408,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.002}),
        "equipment": _tools.ROList([[80831001, 3, 1], [80581001, 3, 1], [80781001, 3, 1]]),
        "props": None
    }),
    101409: _tools.RODict({
        "ID": 101409,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.003}),
        "equipment": _tools.ROList([[80831001, 4, 1], [80581001, 4, 1], [80781001, 4, 1]]),
        "props": None
    }),
    101410: _tools.RODict({
        "ID": 101410,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.004}),
        "equipment": _tools.ROList([[80831001, 5, 1], [80581001, 5, 1], [80781001, 5, 1]]),
        "props": None
    }),
    101411: _tools.RODict({
        "ID": 101411,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.005}),
        "equipment": _tools.ROList([[80831001, 6, 1], [80581001, 6, 1], [80781001, 6, 1]]),
        "props": None
    }),
    101412: _tools.RODict({
        "ID": 101412,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0075}),
        "equipment": _tools.ROList([[80831001, 7, 1], [80581001, 7, 1], [80781001, 7, 1]]),
        "props": None
    }),
    101413: _tools.RODict({
        "ID": 101413,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0015}),
        "equipment": _tools.ROList([[80831001, 0, 2], [80581001, 0, 2], [80781001, 0, 2]]),
        "props": None
    }),
    101414: _tools.RODict({
        "ID": 101414,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0015}),
        "equipment": _tools.ROList([[80831001, 1, 2], [80581001, 1, 2], [80781001, 1, 2]]),
        "props": None
    }),
    101415: _tools.RODict({
        "ID": 101415,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.002}),
        "equipment": _tools.ROList([[80831001, 2, 2], [80581001, 2, 2], [80781001, 2, 2]]),
        "props": None
    }),
    101416: _tools.RODict({
        "ID": 101416,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0025}),
        "equipment": _tools.ROList([[80831001, 3, 2], [80581001, 3, 2], [80781001, 3, 2]]),
        "props": None
    }),
    101417: _tools.RODict({
        "ID": 101417,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0035}),
        "equipment": _tools.ROList([[80831001, 4, 2], [80581001, 4, 2], [80781001, 4, 2]]),
        "props": None
    }),
    101418: _tools.RODict({
        "ID": 101418,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0045}),
        "equipment": _tools.ROList([[80831001, 5, 2], [80581001, 5, 2], [80781001, 5, 2]]),
        "props": None
    }),
    101419: _tools.RODict({
        "ID": 101419,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0055}),
        "equipment": _tools.ROList([[80831001, 6, 2], [80581001, 6, 2], [80781001, 6, 2]]),
        "props": None
    }),
    101420: _tools.RODict({
        "ID": 101420,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.008}),
        "equipment": _tools.ROList([[80831001, 7, 2], [80581001, 7, 2], [80781001, 7, 2]]),
        "props": None
    }),
    101421: _tools.RODict({
        "ID": 101421,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.002}),
        "equipment": _tools.ROList([[80831001, 0, 3], [80581001, 0, 3], [80781001, 0, 3]]),
        "props": None
    }),
    101422: _tools.RODict({
        "ID": 101422,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0025}),
        "equipment": _tools.ROList([[80831001, 1, 3], [80581001, 1, 3], [80781001, 1, 3]]),
        "props": None
    }),
    101423: _tools.RODict({
        "ID": 101423,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0025}),
        "equipment": _tools.ROList([[80831001, 2, 3], [80581001, 2, 3], [80781001, 2, 3]]),
        "props": None
    }),
    101424: _tools.RODict({
        "ID": 101424,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.003}),
        "equipment": _tools.ROList([[80831001, 3, 3], [80581001, 3, 3], [80781001, 3, 3]]),
        "props": None
    }),
    101425: _tools.RODict({
        "ID": 101425,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.004}),
        "equipment": _tools.ROList([[80831001, 4, 3], [80581001, 4, 3], [80781001, 4, 3]]),
        "props": None
    }),
    101426: _tools.RODict({
        "ID": 101426,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.005}),
        "equipment": _tools.ROList([[80831001, 5, 3], [80581001, 5, 3], [80781001, 5, 3]]),
        "props": None
    }),
    101427: _tools.RODict({
        "ID": 101427,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.006}),
        "equipment": _tools.ROList([[80831001, 6, 3], [80581001, 6, 3], [80781001, 6, 3]]),
        "props": None
    }),
    101428: _tools.RODict({
        "ID": 101428,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0085}),
        "equipment": _tools.ROList([[80831001, 7, 3], [80581001, 7, 3], [80781001, 7, 3]]),
        "props": None
    }),
    101429: _tools.RODict({
        "ID": 101429,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0025}),
        "equipment": _tools.ROList([[80831001, 0, 4], [80581001, 0, 4], [80781001, 0, 4]]),
        "props": None
    }),
    101430: _tools.RODict({
        "ID": 101430,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.003}),
        "equipment": _tools.ROList([[80831001, 1, 4], [80581001, 1, 4], [80781001, 1, 4]]),
        "props": None
    }),
    101431: _tools.RODict({
        "ID": 101431,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.003}),
        "equipment": _tools.ROList([[80831001, 2, 4], [80581001, 2, 4], [80781001, 2, 4]]),
        "props": None
    }),
    101432: _tools.RODict({
        "ID": 101432,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0035}),
        "equipment": _tools.ROList([[80831001, 3, 4], [80581001, 3, 4], [80781001, 3, 4]]),
        "props": None
    }),
    101433: _tools.RODict({
        "ID": 101433,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0045}),
        "equipment": _tools.ROList([[80831001, 4, 4], [80581001, 4, 4], [80781001, 4, 4]]),
        "props": None
    }),
    101434: _tools.RODict({
        "ID": 101434,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0055}),
        "equipment": _tools.ROList([[80831001, 5, 4], [80581001, 5, 4], [80781001, 5, 4]]),
        "props": None
    }),
    101435: _tools.RODict({
        "ID": 101435,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.0065}),
        "equipment": _tools.ROList([[80831001, 6, 4], [80581001, 6, 4], [80781001, 6, 4]]),
        "props": None
    }),
    101436: _tools.RODict({
        "ID": 101436,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMonsterDmg":0.009}),
        "equipment": _tools.ROList([[80831001, 7, 4], [80581001, 7, 4], [80781001, 7, 4]]),
        "props": None
    }),
    101437: _tools.RODict({
        "ID": 101437,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMortal":0.002}),
        "equipment": _tools.ROList([[80331001, 0, 1], [80831001, 0, 1], [80431001, 0, 1]]),
        "props": None
    }),
    101438: _tools.RODict({
        "ID": 101438,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMortal":0.002}),
        "equipment": _tools.ROList([[80331001, 1, 1], [80831001, 1, 1], [80431001, 1, 1]]),
        "props": None
    }),
    101439: _tools.RODict({
        "ID": 101439,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMortal":0.003}),
        "equipment": _tools.ROList([[80331001, 2, 1], [80831001, 2, 1], [80431001, 2, 1]]),
        "props": None
    }),
    101440: _tools.RODict({
        "ID": 101440,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMortal":0.004}),
        "equipment": _tools.ROList([[80331001, 3, 1], [80831001, 3, 1], [80431001, 3, 1]]),
        "props": None
    }),
    101441: _tools.RODict({
        "ID": 101441,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMortal":0.006}),
        "equipment": _tools.ROList([[80331001, 4, 1], [80831001, 4, 1], [80431001, 4, 1]]),
        "props": None
    }),
    101442: _tools.RODict({
        "ID": 101442,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMortal":0.008}),
        "equipment": _tools.ROList([[80331001, 5, 1], [80831001, 5, 1], [80431001, 5, 1]]),
        "props": None
    }),
    101443: _tools.RODict({
        "ID": 101443,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMortal":0.01}),
        "equipment": _tools.ROList([[80331001, 6, 1], [80831001, 6, 1], [80431001, 6, 1]]),
        "props": None
    }),
    101444: _tools.RODict({
        "ID": 101444,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMortal":0.015}),
        "equipment": _tools.ROList([[80331001, 7, 1], [80831001, 7, 1], [80431001, 7, 1]]),
        "props": None
    }),
    101445: _tools.RODict({
        "ID": 101445,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMortal":0.003}),
        "equipment": _tools.ROList([[80331001, 0, 2], [80831001, 0, 2], [80431001, 0, 2]]),
        "props": None
    }),
    101446: _tools.RODict({
        "ID": 101446,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMortal":0.003}),
        "equipment": _tools.ROList([[80331001, 1, 2], [80831001, 1, 2], [80431001, 1, 2]]),
        "props": None
    }),
    101447: _tools.RODict({
        "ID": 101447,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMortal":0.004}),
        "equipment": _tools.ROList([[80331001, 2, 2], [80831001, 2, 2], [80431001, 2, 2]]),
        "props": None
    }),
    101448: _tools.RODict({
        "ID": 101448,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMortal":0.005}),
        "equipment": _tools.ROList([[80331001, 3, 2], [80831001, 3, 2], [80431001, 3, 2]]),
        "props": None
    }),
    101449: _tools.RODict({
        "ID": 101449,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMortal":0.007}),
        "equipment": _tools.ROList([[80331001, 4, 2], [80831001, 4, 2], [80431001, 4, 2]]),
        "props": None
    }),
    101450: _tools.RODict({
        "ID": 101450,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMortal":0.009}),
        "equipment": _tools.ROList([[80331001, 5, 2], [80831001, 5, 2], [80431001, 5, 2]]),
        "props": None
    }),
    101451: _tools.RODict({
        "ID": 101451,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMortal":0.011}),
        "equipment": _tools.ROList([[80331001, 6, 2], [80831001, 6, 2], [80431001, 6, 2]]),
        "props": None
    }),
    101452: _tools.RODict({
        "ID": 101452,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMortal":0.016}),
        "equipment": _tools.ROList([[80331001, 7, 2], [80831001, 7, 2], [80431001, 7, 2]]),
        "props": None
    }),
    101453: _tools.RODict({
        "ID": 101453,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMortal":0.004}),
        "equipment": _tools.ROList([[80331001, 0, 3], [80831001, 0, 3], [80431001, 0, 3]]),
        "props": None
    }),
    101454: _tools.RODict({
        "ID": 101454,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMortal":0.005}),
        "equipment": _tools.ROList([[80331001, 1, 3], [80831001, 1, 3], [80431001, 1, 3]]),
        "props": None
    }),
    101455: _tools.RODict({
        "ID": 101455,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMortal":0.005}),
        "equipment": _tools.ROList([[80331001, 2, 3], [80831001, 2, 3], [80431001, 2, 3]]),
        "props": None
    }),
    101456: _tools.RODict({
        "ID": 101456,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMortal":0.006}),
        "equipment": _tools.ROList([[80331001, 3, 3], [80831001, 3, 3], [80431001, 3, 3]]),
        "props": None
    }),
    101457: _tools.RODict({
        "ID": 101457,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMortal":0.008}),
        "equipment": _tools.ROList([[80331001, 4, 3], [80831001, 4, 3], [80431001, 4, 3]]),
        "props": None
    }),
    101458: _tools.RODict({
        "ID": 101458,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMortal":0.01}),
        "equipment": _tools.ROList([[80331001, 5, 3], [80831001, 5, 3], [80431001, 5, 3]]),
        "props": None
    }),
    101459: _tools.RODict({
        "ID": 101459,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMortal":0.012}),
        "equipment": _tools.ROList([[80331001, 6, 3], [80831001, 6, 3], [80431001, 6, 3]]),
        "props": None
    }),
    101460: _tools.RODict({
        "ID": 101460,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMortal":0.017}),
        "equipment": _tools.ROList([[80331001, 7, 3], [80831001, 7, 3], [80431001, 7, 3]]),
        "props": None
    }),
    101461: _tools.RODict({
        "ID": 101461,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMortal":0.005}),
        "equipment": _tools.ROList([[80331001, 0, 4], [80831001, 0, 4], [80431001, 0, 4]]),
        "props": None
    }),
    101462: _tools.RODict({
        "ID": 101462,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMortal":0.006}),
        "equipment": _tools.ROList([[80331001, 1, 4], [80831001, 1, 4], [80431001, 1, 4]]),
        "props": None
    }),
    101463: _tools.RODict({
        "ID": 101463,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMortal":0.006}),
        "equipment": _tools.ROList([[80331001, 2, 4], [80831001, 2, 4], [80431001, 2, 4]]),
        "props": None
    }),
    101464: _tools.RODict({
        "ID": 101464,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMortal":0.007}),
        "equipment": _tools.ROList([[80331001, 3, 4], [80831001, 3, 4], [80431001, 3, 4]]),
        "props": None
    }),
    101465: _tools.RODict({
        "ID": 101465,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMortal":0.009}),
        "equipment": _tools.ROList([[80331001, 4, 4], [80831001, 4, 4], [80431001, 4, 4]]),
        "props": None
    }),
    101466: _tools.RODict({
        "ID": 101466,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMortal":0.011}),
        "equipment": _tools.ROList([[80331001, 5, 4], [80831001, 5, 4], [80431001, 5, 4]]),
        "props": None
    }),
    101467: _tools.RODict({
        "ID": 101467,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMortal":0.013}),
        "equipment": _tools.ROList([[80331001, 6, 4], [80831001, 6, 4], [80431001, 6, 4]]),
        "props": None
    }),
    101468: _tools.RODict({
        "ID": 101468,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjMortal":0.018}),
        "equipment": _tools.ROList([[80331001, 7, 4], [80831001, 7, 4], [80431001, 7, 4]]),
        "props": None
    }),
    101469: _tools.RODict({
        "ID": 101469,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiMortal":0.002}),
        "equipment": _tools.ROList([[80831001, 0, 1], [80581001, 0, 1], [80781001, 0, 1]]),
        "props": None
    }),
    101470: _tools.RODict({
        "ID": 101470,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiMortal":0.002}),
        "equipment": _tools.ROList([[80831001, 1, 1], [80581001, 1, 1], [80781001, 1, 1]]),
        "props": None
    }),
    101471: _tools.RODict({
        "ID": 101471,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiMortal":0.003}),
        "equipment": _tools.ROList([[80831001, 2, 1], [80581001, 2, 1], [80781001, 2, 1]]),
        "props": None
    }),
    101472: _tools.RODict({
        "ID": 101472,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiMortal":0.004}),
        "equipment": _tools.ROList([[80831001, 3, 1], [80581001, 3, 1], [80781001, 3, 1]]),
        "props": None
    }),
    101473: _tools.RODict({
        "ID": 101473,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiMortal":0.006}),
        "equipment": _tools.ROList([[80831001, 4, 1], [80581001, 4, 1], [80781001, 4, 1]]),
        "props": None
    }),
    101474: _tools.RODict({
        "ID": 101474,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiMortal":0.008}),
        "equipment": _tools.ROList([[80831001, 5, 1], [80581001, 5, 1], [80781001, 5, 1]]),
        "props": None
    }),
    101475: _tools.RODict({
        "ID": 101475,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiMortal":0.01}),
        "equipment": _tools.ROList([[80831001, 6, 1], [80581001, 6, 1], [80781001, 6, 1]]),
        "props": None
    }),
    101476: _tools.RODict({
        "ID": 101476,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiMortal":0.015}),
        "equipment": _tools.ROList([[80831001, 7, 1], [80581001, 7, 1], [80781001, 7, 1]]),
        "props": None
    }),
    101477: _tools.RODict({
        "ID": 101477,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiMortal":0.003}),
        "equipment": _tools.ROList([[80831001, 0, 2], [80581001, 0, 2], [80781001, 0, 2]]),
        "props": None
    }),
    101478: _tools.RODict({
        "ID": 101478,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiMortal":0.003}),
        "equipment": _tools.ROList([[80831001, 1, 2], [80581001, 1, 2], [80781001, 1, 2]]),
        "props": None
    }),
    101479: _tools.RODict({
        "ID": 101479,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiMortal":0.004}),
        "equipment": _tools.ROList([[80831001, 2, 2], [80581001, 2, 2], [80781001, 2, 2]]),
        "props": None
    }),
    101480: _tools.RODict({
        "ID": 101480,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiMortal":0.005}),
        "equipment": _tools.ROList([[80831001, 3, 2], [80581001, 3, 2], [80781001, 3, 2]]),
        "props": None
    }),
    101481: _tools.RODict({
        "ID": 101481,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiMortal":0.007}),
        "equipment": _tools.ROList([[80831001, 4, 2], [80581001, 4, 2], [80781001, 4, 2]]),
        "props": None
    }),
    101482: _tools.RODict({
        "ID": 101482,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiMortal":0.009}),
        "equipment": _tools.ROList([[80831001, 5, 2], [80581001, 5, 2], [80781001, 5, 2]]),
        "props": None
    }),
    101483: _tools.RODict({
        "ID": 101483,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiMortal":0.011}),
        "equipment": _tools.ROList([[80831001, 6, 2], [80581001, 6, 2], [80781001, 6, 2]]),
        "props": None
    }),
    101484: _tools.RODict({
        "ID": 101484,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiMortal":0.016}),
        "equipment": _tools.ROList([[80831001, 7, 2], [80581001, 7, 2], [80781001, 7, 2]]),
        "props": None
    }),
    101485: _tools.RODict({
        "ID": 101485,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiMortal":0.004}),
        "equipment": _tools.ROList([[80831001, 0, 3], [80581001, 0, 3], [80781001, 0, 3]]),
        "props": None
    }),
    101486: _tools.RODict({
        "ID": 101486,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiMortal":0.005}),
        "equipment": _tools.ROList([[80831001, 1, 3], [80581001, 1, 3], [80781001, 1, 3]]),
        "props": None
    }),
    101487: _tools.RODict({
        "ID": 101487,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiMortal":0.005}),
        "equipment": _tools.ROList([[80831001, 2, 3], [80581001, 2, 3], [80781001, 2, 3]]),
        "props": None
    }),
    101488: _tools.RODict({
        "ID": 101488,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiMortal":0.006}),
        "equipment": _tools.ROList([[80831001, 3, 3], [80581001, 3, 3], [80781001, 3, 3]]),
        "props": None
    }),
    101489: _tools.RODict({
        "ID": 101489,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiMortal":0.008}),
        "equipment": _tools.ROList([[80831001, 4, 3], [80581001, 4, 3], [80781001, 4, 3]]),
        "props": None
    }),
    101490: _tools.RODict({
        "ID": 101490,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiMortal":0.01}),
        "equipment": _tools.ROList([[80831001, 5, 3], [80581001, 5, 3], [80781001, 5, 3]]),
        "props": None
    }),
    101491: _tools.RODict({
        "ID": 101491,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiMortal":0.012}),
        "equipment": _tools.ROList([[80831001, 6, 3], [80581001, 6, 3], [80781001, 6, 3]]),
        "props": None
    }),
    101492: _tools.RODict({
        "ID": 101492,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiMortal":0.017}),
        "equipment": _tools.ROList([[80831001, 7, 3], [80581001, 7, 3], [80781001, 7, 3]]),
        "props": None
    }),
    101493: _tools.RODict({
        "ID": 101493,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiMortal":0.005}),
        "equipment": _tools.ROList([[80831001, 0, 4], [80581001, 0, 4], [80781001, 0, 4]]),
        "props": None
    }),
    101494: _tools.RODict({
        "ID": 101494,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiMortal":0.006}),
        "equipment": _tools.ROList([[80831001, 1, 4], [80581001, 1, 4], [80781001, 1, 4]]),
        "props": None
    }),
    101495: _tools.RODict({
        "ID": 101495,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiMortal":0.006}),
        "equipment": _tools.ROList([[80831001, 2, 4], [80581001, 2, 4], [80781001, 2, 4]]),
        "props": None
    }),
    101496: _tools.RODict({
        "ID": 101496,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiMortal":0.007}),
        "equipment": _tools.ROList([[80831001, 3, 4], [80581001, 3, 4], [80781001, 3, 4]]),
        "props": None
    }),
    101497: _tools.RODict({
        "ID": 101497,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiMortal":0.009}),
        "equipment": _tools.ROList([[80831001, 4, 4], [80581001, 4, 4], [80781001, 4, 4]]),
        "props": None
    }),
    101498: _tools.RODict({
        "ID": 101498,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiMortal":0.011}),
        "equipment": _tools.ROList([[80831001, 5, 4], [80581001, 5, 4], [80781001, 5, 4]]),
        "props": None
    }),
    101499: _tools.RODict({
        "ID": 101499,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiMortal":0.013}),
        "equipment": _tools.ROList([[80831001, 6, 4], [80581001, 6, 4], [80781001, 6, 4]]),
        "props": None
    }),
    101500: _tools.RODict({
        "ID": 101500,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiMortal":0.018}),
        "equipment": _tools.ROList([[80831001, 7, 4], [80581001, 7, 4], [80781001, 7, 4]]),
        "props": None
    }),
    101501: _tools.RODict({
        "ID": 101501,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80131001, 4, 1], [80331001, 4, 1], [80581001, 4, 1]]),
        "props": None
    }),
    101502: _tools.RODict({
        "ID": 101502,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80131001, 5, 1], [80331001, 5, 1], [80581001, 5, 1]]),
        "props": None
    }),
    101503: _tools.RODict({
        "ID": 101503,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80131001, 6, 1], [80331001, 6, 1], [80581001, 6, 1]]),
        "props": None
    }),
    101504: _tools.RODict({
        "ID": 101504,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80131001, 4, 2], [80331001, 4, 2], [80581001, 4, 2]]),
        "props": None
    }),
    101505: _tools.RODict({
        "ID": 101505,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80131001, 5, 2], [80331001, 5, 2], [80581001, 5, 2]]),
        "props": None
    }),
    101506: _tools.RODict({
        "ID": 101506,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80131001, 6, 2], [80331001, 6, 2], [80581001, 6, 2]]),
        "props": None
    }),
    101507: _tools.RODict({
        "ID": 101507,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80131001, 7, 2], [80331001, 7, 2], [80581001, 7, 2]]),
        "props": None
    }),
    101508: _tools.RODict({
        "ID": 101508,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80131001, 4, 3], [80331001, 4, 3], [80581001, 4, 3]]),
        "props": None
    }),
    101509: _tools.RODict({
        "ID": 101509,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80131001, 5, 3], [80331001, 5, 3], [80581001, 5, 3]]),
        "props": None
    }),
    101510: _tools.RODict({
        "ID": 101510,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80131001, 6, 3], [80331001, 6, 3], [80581001, 6, 3]]),
        "props": None
    }),
    101511: _tools.RODict({
        "ID": 101511,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80131001, 7, 3], [80331001, 7, 3], [80581001, 7, 3]]),
        "props": None
    }),
    101512: _tools.RODict({
        "ID": 101512,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80131001, 4, 4], [80331001, 4, 4], [80581001, 4, 4]]),
        "props": None
    }),
    101513: _tools.RODict({
        "ID": 101513,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80131001, 5, 4], [80331001, 5, 4], [80581001, 5, 4]]),
        "props": None
    }),
    101514: _tools.RODict({
        "ID": 101514,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80131001, 6, 4], [80331001, 6, 4], [80581001, 6, 4]]),
        "props": None
    }),
    101515: _tools.RODict({
        "ID": 101515,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFatal":1}),
        "equipment": _tools.ROList([[80131001, 7, 4], [80331001, 7, 4], [80581001, 7, 4]]),
        "props": None
    }),
    101516: _tools.RODict({
        "ID": 101516,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80131001, 4, 1], [80331001, 4, 1], [80431001, 4, 1]]),
        "props": None
    }),
    101517: _tools.RODict({
        "ID": 101517,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80131001, 5, 1], [80331001, 5, 1], [80431001, 5, 1]]),
        "props": None
    }),
    101518: _tools.RODict({
        "ID": 101518,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80131001, 6, 1], [80331001, 6, 1], [80431001, 6, 1]]),
        "props": None
    }),
    101519: _tools.RODict({
        "ID": 101519,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80131001, 4, 2], [80331001, 4, 2], [80431001, 4, 2]]),
        "props": None
    }),
    101520: _tools.RODict({
        "ID": 101520,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80131001, 5, 2], [80331001, 5, 2], [80431001, 5, 2]]),
        "props": None
    }),
    101521: _tools.RODict({
        "ID": 101521,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80131001, 6, 2], [80331001, 6, 2], [80431001, 6, 2]]),
        "props": None
    }),
    101522: _tools.RODict({
        "ID": 101522,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80131001, 7, 2], [80331001, 7, 2], [80431001, 7, 2]]),
        "props": None
    }),
    101523: _tools.RODict({
        "ID": 101523,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80131001, 4, 3], [80331001, 4, 3], [80431001, 4, 3]]),
        "props": None
    }),
    101524: _tools.RODict({
        "ID": 101524,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80131001, 5, 3], [80331001, 5, 3], [80431001, 5, 3]]),
        "props": None
    }),
    101525: _tools.RODict({
        "ID": 101525,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80131001, 6, 3], [80331001, 6, 3], [80431001, 6, 3]]),
        "props": None
    }),
    101526: _tools.RODict({
        "ID": 101526,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80131001, 7, 3], [80331001, 7, 3], [80431001, 7, 3]]),
        "props": None
    }),
    101527: _tools.RODict({
        "ID": 101527,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80131001, 4, 4], [80331001, 4, 4], [80431001, 4, 4]]),
        "props": None
    }),
    101528: _tools.RODict({
        "ID": 101528,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80131001, 5, 4], [80331001, 5, 4], [80431001, 5, 4]]),
        "props": None
    }),
    101529: _tools.RODict({
        "ID": 101529,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80131001, 6, 4], [80331001, 6, 4], [80431001, 6, 4]]),
        "props": None
    }),
    101530: _tools.RODict({
        "ID": 101530,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAntiFatal":1}),
        "equipment": _tools.ROList([[80131001, 7, 4], [80331001, 7, 4], [80431001, 7, 4]]),
        "props": None
    }),
    101531: _tools.RODict({
        "ID": 101531,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80331001, 4, 1], [80681001, 4, 1], [80781001, 4, 1]]),
        "props": None
    }),
    101532: _tools.RODict({
        "ID": 101532,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80331001, 5, 1], [80681001, 5, 1], [80781001, 5, 1]]),
        "props": None
    }),
    101533: _tools.RODict({
        "ID": 101533,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80331001, 6, 1], [80681001, 6, 1], [80781001, 6, 1]]),
        "props": None
    }),
    101534: _tools.RODict({
        "ID": 101534,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80331001, 4, 2], [80681001, 4, 2], [80781001, 4, 2]]),
        "props": None
    }),
    101535: _tools.RODict({
        "ID": 101535,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80331001, 5, 2], [80681001, 5, 2], [80781001, 5, 2]]),
        "props": None
    }),
    101536: _tools.RODict({
        "ID": 101536,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80331001, 6, 2], [80681001, 6, 2], [80781001, 6, 2]]),
        "props": None
    }),
    101537: _tools.RODict({
        "ID": 101537,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80331001, 7, 2], [80681001, 7, 2], [80781001, 7, 2]]),
        "props": None
    }),
    101538: _tools.RODict({
        "ID": 101538,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80331001, 4, 3], [80681001, 4, 3], [80781001, 4, 3]]),
        "props": None
    }),
    101539: _tools.RODict({
        "ID": 101539,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80331001, 5, 3], [80681001, 5, 3], [80781001, 5, 3]]),
        "props": None
    }),
    101540: _tools.RODict({
        "ID": 101540,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80331001, 6, 3], [80681001, 6, 3], [80781001, 6, 3]]),
        "props": None
    }),
    101541: _tools.RODict({
        "ID": 101541,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80331001, 7, 3], [80681001, 7, 3], [80781001, 7, 3]]),
        "props": None
    }),
    101542: _tools.RODict({
        "ID": 101542,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80331001, 4, 4], [80681001, 4, 4], [80781001, 4, 4]]),
        "props": None
    }),
    101543: _tools.RODict({
        "ID": 101543,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80331001, 5, 4], [80681001, 5, 4], [80781001, 5, 4]]),
        "props": None
    }),
    101544: _tools.RODict({
        "ID": 101544,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80331001, 6, 4], [80681001, 6, 4], [80781001, 6, 4]]),
        "props": None
    }),
    101545: _tools.RODict({
        "ID": 101545,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjAccuracy":1}),
        "equipment": _tools.ROList([[80331001, 7, 4], [80681001, 7, 4], [80781001, 7, 4]]),
        "props": None
    }),
    101546: _tools.RODict({
        "ID": 101546,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80131001, 4, 1], [80431001, 4, 1], [80681001, 4, 1]]),
        "props": None
    }),
    101547: _tools.RODict({
        "ID": 101547,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80131001, 5, 1], [80431001, 5, 1], [80681001, 5, 1]]),
        "props": None
    }),
    101548: _tools.RODict({
        "ID": 101548,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80131001, 6, 1], [80431001, 6, 1], [80681001, 6, 1]]),
        "props": None
    }),
    101549: _tools.RODict({
        "ID": 101549,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80131001, 4, 2], [80431001, 4, 2], [80681001, 4, 2]]),
        "props": None
    }),
    101550: _tools.RODict({
        "ID": 101550,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80131001, 5, 2], [80431001, 5, 2], [80681001, 5, 2]]),
        "props": None
    }),
    101551: _tools.RODict({
        "ID": 101551,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80131001, 6, 2], [80431001, 6, 2], [80681001, 6, 2]]),
        "props": None
    }),
    101552: _tools.RODict({
        "ID": 101552,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80131001, 7, 2], [80431001, 7, 2], [80681001, 7, 2]]),
        "props": None
    }),
    101553: _tools.RODict({
        "ID": 101553,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80131001, 4, 3], [80431001, 4, 3], [80681001, 4, 3]]),
        "props": None
    }),
    101554: _tools.RODict({
        "ID": 101554,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80131001, 5, 3], [80431001, 5, 3], [80681001, 5, 3]]),
        "props": None
    }),
    101555: _tools.RODict({
        "ID": 101555,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80131001, 6, 3], [80431001, 6, 3], [80681001, 6, 3]]),
        "props": None
    }),
    101556: _tools.RODict({
        "ID": 101556,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80131001, 7, 3], [80431001, 7, 3], [80681001, 7, 3]]),
        "props": None
    }),
    101557: _tools.RODict({
        "ID": 101557,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80131001, 4, 4], [80431001, 4, 4], [80681001, 4, 4]]),
        "props": None
    }),
    101558: _tools.RODict({
        "ID": 101558,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80131001, 5, 4], [80431001, 5, 4], [80681001, 5, 4]]),
        "props": None
    }),
    101559: _tools.RODict({
        "ID": 101559,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80131001, 6, 4], [80431001, 6, 4], [80681001, 6, 4]]),
        "props": None
    }),
    101560: _tools.RODict({
        "ID": 101560,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjEvasion":1}),
        "equipment": _tools.ROList([[80131001, 7, 4], [80431001, 7, 4], [80681001, 7, 4]]),
        "props": None
    }),
    101561: _tools.RODict({
        "ID": 101561,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80131001, 4, 1], [80431001, 4, 1], [80781001, 4, 1]]),
        "props": None
    }),
    101562: _tools.RODict({
        "ID": 101562,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80131001, 5, 1], [80431001, 5, 1], [80781001, 5, 1]]),
        "props": None
    }),
    101563: _tools.RODict({
        "ID": 101563,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80131001, 6, 1], [80431001, 6, 1], [80781001, 6, 1]]),
        "props": None
    }),
    101564: _tools.RODict({
        "ID": 101564,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80131001, 4, 2], [80431001, 4, 2], [80781001, 4, 2]]),
        "props": None
    }),
    101565: _tools.RODict({
        "ID": 101565,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80131001, 5, 2], [80431001, 5, 2], [80781001, 5, 2]]),
        "props": None
    }),
    101566: _tools.RODict({
        "ID": 101566,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80131001, 6, 2], [80431001, 6, 2], [80781001, 6, 2]]),
        "props": None
    }),
    101567: _tools.RODict({
        "ID": 101567,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80131001, 7, 2], [80431001, 7, 2], [80781001, 7, 2]]),
        "props": None
    }),
    101568: _tools.RODict({
        "ID": 101568,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80131001, 4, 3], [80431001, 4, 3], [80781001, 4, 3]]),
        "props": None
    }),
    101569: _tools.RODict({
        "ID": 101569,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80131001, 5, 3], [80431001, 5, 3], [80781001, 5, 3]]),
        "props": None
    }),
    101570: _tools.RODict({
        "ID": 101570,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80131001, 6, 3], [80431001, 6, 3], [80781001, 6, 3]]),
        "props": None
    }),
    101571: _tools.RODict({
        "ID": 101571,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80131001, 7, 3], [80431001, 7, 3], [80781001, 7, 3]]),
        "props": None
    }),
    101572: _tools.RODict({
        "ID": 101572,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80131001, 4, 4], [80431001, 4, 4], [80781001, 4, 4]]),
        "props": None
    }),
    101573: _tools.RODict({
        "ID": 101573,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80131001, 5, 4], [80431001, 5, 4], [80781001, 5, 4]]),
        "props": None
    }),
    101574: _tools.RODict({
        "ID": 101574,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80131001, 6, 4], [80431001, 6, 4], [80781001, 6, 4]]),
        "props": None
    }),
    101575: _tools.RODict({
        "ID": 101575,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjHit":1}),
        "equipment": _tools.ROList([[80131001, 7, 4], [80431001, 7, 4], [80781001, 7, 4]]),
        "props": None
    }),
    101576: _tools.RODict({
        "ID": 101576,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80331001, 4, 1], [80831001, 4, 1], [80581001, 4, 1]]),
        "props": None
    }),
    101577: _tools.RODict({
        "ID": 101577,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80331001, 5, 1], [80831001, 5, 1], [80581001, 5, 1]]),
        "props": None
    }),
    101578: _tools.RODict({
        "ID": 101578,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80331001, 6, 1], [80831001, 6, 1], [80581001, 6, 1]]),
        "props": None
    }),
    101579: _tools.RODict({
        "ID": 101579,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80331001, 4, 2], [80831001, 4, 2], [80581001, 4, 2]]),
        "props": None
    }),
    101580: _tools.RODict({
        "ID": 101580,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80331001, 5, 2], [80831001, 5, 2], [80581001, 5, 2]]),
        "props": None
    }),
    101581: _tools.RODict({
        "ID": 101581,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80331001, 6, 2], [80831001, 6, 2], [80581001, 6, 2]]),
        "props": None
    }),
    101582: _tools.RODict({
        "ID": 101582,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80331001, 7, 2], [80831001, 7, 2], [80581001, 7, 2]]),
        "props": None
    }),
    101583: _tools.RODict({
        "ID": 101583,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80331001, 4, 3], [80831001, 4, 3], [80581001, 4, 3]]),
        "props": None
    }),
    101584: _tools.RODict({
        "ID": 101584,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80331001, 5, 3], [80831001, 5, 3], [80581001, 5, 3]]),
        "props": None
    }),
    101585: _tools.RODict({
        "ID": 101585,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80331001, 6, 3], [80831001, 6, 3], [80581001, 6, 3]]),
        "props": None
    }),
    101586: _tools.RODict({
        "ID": 101586,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80331001, 7, 3], [80831001, 7, 3], [80581001, 7, 3]]),
        "props": None
    }),
    101587: _tools.RODict({
        "ID": 101587,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80331001, 4, 4], [80831001, 4, 4], [80581001, 4, 4]]),
        "props": None
    }),
    101588: _tools.RODict({
        "ID": 101588,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80331001, 5, 4], [80831001, 5, 4], [80581001, 5, 4]]),
        "props": None
    }),
    101589: _tools.RODict({
        "ID": 101589,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80331001, 6, 4], [80831001, 6, 4], [80581001, 6, 4]]),
        "props": None
    }),
    101590: _tools.RODict({
        "ID": 101590,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjDodge":1}),
        "equipment": _tools.ROList([[80331001, 7, 4], [80831001, 7, 4], [80581001, 7, 4]]),
        "props": None
    }),
    101591: _tools.RODict({
        "ID": 101591,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80131001, 3, 1], [80581001, 3, 1]]),
        "props": None
    }),
    101592: _tools.RODict({
        "ID": 101592,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80131001, 4, 1], [80581001, 4, 1]]),
        "props": None
    }),
    101593: _tools.RODict({
        "ID": 101593,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80131001, 5, 1], [80581001, 5, 1]]),
        "props": None
    }),
    101594: _tools.RODict({
        "ID": 101594,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80131001, 3, 2], [80581001, 3, 2]]),
        "props": None
    }),
    101595: _tools.RODict({
        "ID": 101595,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80131001, 4, 2], [80581001, 4, 2]]),
        "props": None
    }),
    101596: _tools.RODict({
        "ID": 101596,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80131001, 5, 2], [80581001, 5, 2]]),
        "props": None
    }),
    101597: _tools.RODict({
        "ID": 101597,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80131001, 6, 2], [80581001, 6, 2]]),
        "props": None
    }),
    101598: _tools.RODict({
        "ID": 101598,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80131001, 3, 3], [80581001, 3, 3]]),
        "props": None
    }),
    101599: _tools.RODict({
        "ID": 101599,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80131001, 4, 3], [80581001, 4, 3]]),
        "props": None
    }),
    101600: _tools.RODict({
        "ID": 101600,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80131001, 5, 3], [80581001, 5, 3]]),
        "props": None
    }),
    101601: _tools.RODict({
        "ID": 101601,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80131001, 6, 3], [80581001, 6, 3]]),
        "props": None
    }),
    101602: _tools.RODict({
        "ID": 101602,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80131001, 3, 4], [80581001, 3, 4]]),
        "props": None
    }),
    101603: _tools.RODict({
        "ID": 101603,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80131001, 4, 4], [80581001, 4, 4]]),
        "props": None
    }),
    101604: _tools.RODict({
        "ID": 101604,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80131001, 5, 4], [80581001, 5, 4]]),
        "props": None
    }),
    101605: _tools.RODict({
        "ID": 101605,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunEnh":1}),
        "equipment": _tools.ROList([[80131001, 6, 4], [80581001, 6, 4]]),
        "props": None
    }),
    101606: _tools.RODict({
        "ID": 101606,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80131001, 3, 1], [80331001, 3, 1]]),
        "props": None
    }),
    101607: _tools.RODict({
        "ID": 101607,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80131001, 4, 1], [80331001, 4, 1]]),
        "props": None
    }),
    101608: _tools.RODict({
        "ID": 101608,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80131001, 5, 1], [80331001, 5, 1]]),
        "props": None
    }),
    101609: _tools.RODict({
        "ID": 101609,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80131001, 3, 2], [80331001, 3, 2]]),
        "props": None
    }),
    101610: _tools.RODict({
        "ID": 101610,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80131001, 4, 2], [80331001, 4, 2]]),
        "props": None
    }),
    101611: _tools.RODict({
        "ID": 101611,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80131001, 5, 2], [80331001, 5, 2]]),
        "props": None
    }),
    101612: _tools.RODict({
        "ID": 101612,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80131001, 6, 2], [80331001, 6, 2]]),
        "props": None
    }),
    101613: _tools.RODict({
        "ID": 101613,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80131001, 3, 3], [80331001, 3, 3]]),
        "props": None
    }),
    101614: _tools.RODict({
        "ID": 101614,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80131001, 4, 3], [80331001, 4, 3]]),
        "props": None
    }),
    101615: _tools.RODict({
        "ID": 101615,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80131001, 5, 3], [80331001, 5, 3]]),
        "props": None
    }),
    101616: _tools.RODict({
        "ID": 101616,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80131001, 6, 3], [80331001, 6, 3]]),
        "props": None
    }),
    101617: _tools.RODict({
        "ID": 101617,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80131001, 3, 4], [80331001, 3, 4]]),
        "props": None
    }),
    101618: _tools.RODict({
        "ID": 101618,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80131001, 4, 4], [80331001, 4, 4]]),
        "props": None
    }),
    101619: _tools.RODict({
        "ID": 101619,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80131001, 5, 4], [80331001, 5, 4]]),
        "props": None
    }),
    101620: _tools.RODict({
        "ID": 101620,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjStunAnti":1}),
        "equipment": _tools.ROList([[80131001, 6, 4], [80331001, 6, 4]]),
        "props": None
    }),
    101621: _tools.RODict({
        "ID": 101621,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80681001, 3, 1], [80781001, 3, 1]]),
        "props": None
    }),
    101622: _tools.RODict({
        "ID": 101622,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80681001, 4, 1], [80781001, 4, 1]]),
        "props": None
    }),
    101623: _tools.RODict({
        "ID": 101623,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80681001, 5, 1], [80781001, 5, 1]]),
        "props": None
    }),
    101624: _tools.RODict({
        "ID": 101624,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80681001, 3, 2], [80781001, 3, 2]]),
        "props": None
    }),
    101625: _tools.RODict({
        "ID": 101625,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80681001, 4, 2], [80781001, 4, 2]]),
        "props": None
    }),
    101626: _tools.RODict({
        "ID": 101626,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80681001, 5, 2], [80781001, 5, 2]]),
        "props": None
    }),
    101627: _tools.RODict({
        "ID": 101627,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80681001, 6, 2], [80781001, 6, 2]]),
        "props": None
    }),
    101628: _tools.RODict({
        "ID": 101628,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80681001, 3, 3], [80781001, 3, 3]]),
        "props": None
    }),
    101629: _tools.RODict({
        "ID": 101629,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80681001, 4, 3], [80781001, 4, 3]]),
        "props": None
    }),
    101630: _tools.RODict({
        "ID": 101630,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80681001, 5, 3], [80781001, 5, 3]]),
        "props": None
    }),
    101631: _tools.RODict({
        "ID": 101631,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80681001, 6, 3], [80781001, 6, 3]]),
        "props": None
    }),
    101632: _tools.RODict({
        "ID": 101632,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80681001, 3, 4], [80781001, 3, 4]]),
        "props": None
    }),
    101633: _tools.RODict({
        "ID": 101633,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80681001, 4, 4], [80781001, 4, 4]]),
        "props": None
    }),
    101634: _tools.RODict({
        "ID": 101634,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80681001, 5, 4], [80781001, 5, 4]]),
        "props": None
    }),
    101635: _tools.RODict({
        "ID": 101635,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentEnh":1}),
        "equipment": _tools.ROList([[80681001, 6, 4], [80781001, 6, 4]]),
        "props": None
    }),
    101636: _tools.RODict({
        "ID": 101636,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80831001, 3, 1], [80431001, 3, 1]]),
        "props": None
    }),
    101637: _tools.RODict({
        "ID": 101637,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80831001, 4, 1], [80431001, 4, 1]]),
        "props": None
    }),
    101638: _tools.RODict({
        "ID": 101638,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80831001, 5, 1], [80431001, 5, 1]]),
        "props": None
    }),
    101639: _tools.RODict({
        "ID": 101639,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80831001, 3, 2], [80431001, 3, 2]]),
        "props": None
    }),
    101640: _tools.RODict({
        "ID": 101640,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80831001, 4, 2], [80431001, 4, 2]]),
        "props": None
    }),
    101641: _tools.RODict({
        "ID": 101641,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80831001, 5, 2], [80431001, 5, 2]]),
        "props": None
    }),
    101642: _tools.RODict({
        "ID": 101642,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80831001, 6, 2], [80431001, 6, 2]]),
        "props": None
    }),
    101643: _tools.RODict({
        "ID": 101643,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80831001, 3, 3], [80431001, 3, 3]]),
        "props": None
    }),
    101644: _tools.RODict({
        "ID": 101644,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80831001, 4, 3], [80431001, 4, 3]]),
        "props": None
    }),
    101645: _tools.RODict({
        "ID": 101645,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80831001, 5, 3], [80431001, 5, 3]]),
        "props": None
    }),
    101646: _tools.RODict({
        "ID": 101646,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80831001, 6, 3], [80431001, 6, 3]]),
        "props": None
    }),
    101647: _tools.RODict({
        "ID": 101647,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80831001, 3, 4], [80431001, 3, 4]]),
        "props": None
    }),
    101648: _tools.RODict({
        "ID": 101648,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80831001, 4, 4], [80431001, 4, 4]]),
        "props": None
    }),
    101649: _tools.RODict({
        "ID": 101649,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80831001, 5, 4], [80431001, 5, 4]]),
        "props": None
    }),
    101650: _tools.RODict({
        "ID": 101650,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSilentAnti":1}),
        "equipment": _tools.ROList([[80831001, 6, 4], [80431001, 6, 4]]),
        "props": None
    }),
    101651: _tools.RODict({
        "ID": 101651,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80131001, 3, 1], [80681001, 3, 1]]),
        "props": None
    }),
    101652: _tools.RODict({
        "ID": 101652,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80131001, 4, 1], [80681001, 4, 1]]),
        "props": None
    }),
    101653: _tools.RODict({
        "ID": 101653,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80131001, 5, 1], [80681001, 5, 1]]),
        "props": None
    }),
    101654: _tools.RODict({
        "ID": 101654,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80131001, 3, 2], [80681001, 3, 2]]),
        "props": None
    }),
    101655: _tools.RODict({
        "ID": 101655,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80131001, 4, 2], [80681001, 4, 2]]),
        "props": None
    }),
    101656: _tools.RODict({
        "ID": 101656,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80131001, 5, 2], [80681001, 5, 2]]),
        "props": None
    }),
    101657: _tools.RODict({
        "ID": 101657,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80131001, 6, 2], [80681001, 6, 2]]),
        "props": None
    }),
    101658: _tools.RODict({
        "ID": 101658,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80131001, 3, 3], [80681001, 3, 3]]),
        "props": None
    }),
    101659: _tools.RODict({
        "ID": 101659,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80131001, 4, 3], [80681001, 4, 3]]),
        "props": None
    }),
    101660: _tools.RODict({
        "ID": 101660,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80131001, 5, 3], [80681001, 5, 3]]),
        "props": None
    }),
    101661: _tools.RODict({
        "ID": 101661,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80131001, 6, 3], [80681001, 6, 3]]),
        "props": None
    }),
    101662: _tools.RODict({
        "ID": 101662,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80131001, 3, 4], [80681001, 3, 4]]),
        "props": None
    }),
    101663: _tools.RODict({
        "ID": 101663,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80131001, 4, 4], [80681001, 4, 4]]),
        "props": None
    }),
    101664: _tools.RODict({
        "ID": 101664,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80131001, 5, 4], [80681001, 5, 4]]),
        "props": None
    }),
    101665: _tools.RODict({
        "ID": 101665,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenEnh":1}),
        "equipment": _tools.ROList([[80131001, 6, 4], [80681001, 6, 4]]),
        "props": None
    }),
    101666: _tools.RODict({
        "ID": 101666,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80131001, 3, 1], [80831001, 3, 1]]),
        "props": None
    }),
    101667: _tools.RODict({
        "ID": 101667,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80131001, 4, 1], [80831001, 4, 1]]),
        "props": None
    }),
    101668: _tools.RODict({
        "ID": 101668,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80131001, 5, 1], [80831001, 5, 1]]),
        "props": None
    }),
    101669: _tools.RODict({
        "ID": 101669,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80131001, 3, 2], [80831001, 3, 2]]),
        "props": None
    }),
    101670: _tools.RODict({
        "ID": 101670,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80131001, 4, 2], [80831001, 4, 2]]),
        "props": None
    }),
    101671: _tools.RODict({
        "ID": 101671,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80131001, 5, 2], [80831001, 5, 2]]),
        "props": None
    }),
    101672: _tools.RODict({
        "ID": 101672,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80131001, 6, 2], [80831001, 6, 2]]),
        "props": None
    }),
    101673: _tools.RODict({
        "ID": 101673,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80131001, 3, 3], [80831001, 3, 3]]),
        "props": None
    }),
    101674: _tools.RODict({
        "ID": 101674,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80131001, 4, 3], [80831001, 4, 3]]),
        "props": None
    }),
    101675: _tools.RODict({
        "ID": 101675,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80131001, 5, 3], [80831001, 5, 3]]),
        "props": None
    }),
    101676: _tools.RODict({
        "ID": 101676,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80131001, 6, 3], [80831001, 6, 3]]),
        "props": None
    }),
    101677: _tools.RODict({
        "ID": 101677,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80131001, 3, 4], [80831001, 3, 4]]),
        "props": None
    }),
    101678: _tools.RODict({
        "ID": 101678,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80131001, 4, 4], [80831001, 4, 4]]),
        "props": None
    }),
    101679: _tools.RODict({
        "ID": 101679,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80131001, 5, 4], [80831001, 5, 4]]),
        "props": None
    }),
    101680: _tools.RODict({
        "ID": 101680,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjFrozenAnti":1}),
        "equipment": _tools.ROList([[80131001, 6, 4], [80831001, 6, 4]]),
        "props": None
    }),
    101681: _tools.RODict({
        "ID": 101681,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80581001, 3, 1], [80781001, 3, 1]]),
        "props": None
    }),
    101682: _tools.RODict({
        "ID": 101682,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80581001, 4, 1], [80781001, 4, 1]]),
        "props": None
    }),
    101683: _tools.RODict({
        "ID": 101683,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80581001, 5, 1], [80781001, 5, 1]]),
        "props": None
    }),
    101684: _tools.RODict({
        "ID": 101684,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80581001, 3, 2], [80781001, 3, 2]]),
        "props": None
    }),
    101685: _tools.RODict({
        "ID": 101685,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80581001, 4, 2], [80781001, 4, 2]]),
        "props": None
    }),
    101686: _tools.RODict({
        "ID": 101686,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80581001, 5, 2], [80781001, 5, 2]]),
        "props": None
    }),
    101687: _tools.RODict({
        "ID": 101687,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80581001, 6, 2], [80781001, 6, 2]]),
        "props": None
    }),
    101688: _tools.RODict({
        "ID": 101688,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80581001, 3, 3], [80781001, 3, 3]]),
        "props": None
    }),
    101689: _tools.RODict({
        "ID": 101689,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80581001, 4, 3], [80781001, 4, 3]]),
        "props": None
    }),
    101690: _tools.RODict({
        "ID": 101690,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80581001, 5, 3], [80781001, 5, 3]]),
        "props": None
    }),
    101691: _tools.RODict({
        "ID": 101691,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80581001, 6, 3], [80781001, 6, 3]]),
        "props": None
    }),
    101692: _tools.RODict({
        "ID": 101692,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80581001, 3, 4], [80781001, 3, 4]]),
        "props": None
    }),
    101693: _tools.RODict({
        "ID": 101693,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80581001, 4, 4], [80781001, 4, 4]]),
        "props": None
    }),
    101694: _tools.RODict({
        "ID": 101694,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80581001, 5, 4], [80781001, 5, 4]]),
        "props": None
    }),
    101695: _tools.RODict({
        "ID": 101695,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowEnh":1}),
        "equipment": _tools.ROList([[80581001, 6, 4], [80781001, 6, 4]]),
        "props": None
    }),
    101696: _tools.RODict({
        "ID": 101696,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80331001, 3, 1], [80431001, 3, 1]]),
        "props": None
    }),
    101697: _tools.RODict({
        "ID": 101697,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80331001, 4, 1], [80431001, 4, 1]]),
        "props": None
    }),
    101698: _tools.RODict({
        "ID": 101698,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80331001, 5, 1], [80431001, 5, 1]]),
        "props": None
    }),
    101699: _tools.RODict({
        "ID": 101699,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80331001, 3, 2], [80431001, 3, 2]]),
        "props": None
    }),
    101700: _tools.RODict({
        "ID": 101700,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80331001, 4, 2], [80431001, 4, 2]]),
        "props": None
    }),
    101701: _tools.RODict({
        "ID": 101701,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80331001, 5, 2], [80431001, 5, 2]]),
        "props": None
    }),
    101702: _tools.RODict({
        "ID": 101702,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80331001, 6, 2], [80431001, 6, 2]]),
        "props": None
    }),
    101703: _tools.RODict({
        "ID": 101703,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80331001, 3, 3], [80431001, 3, 3]]),
        "props": None
    }),
    101704: _tools.RODict({
        "ID": 101704,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80331001, 4, 3], [80431001, 4, 3]]),
        "props": None
    }),
    101705: _tools.RODict({
        "ID": 101705,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80331001, 5, 3], [80431001, 5, 3]]),
        "props": None
    }),
    101706: _tools.RODict({
        "ID": 101706,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80331001, 6, 3], [80431001, 6, 3]]),
        "props": None
    }),
    101707: _tools.RODict({
        "ID": 101707,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80331001, 3, 4], [80431001, 3, 4]]),
        "props": None
    }),
    101708: _tools.RODict({
        "ID": 101708,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80331001, 4, 4], [80431001, 4, 4]]),
        "props": None
    }),
    101709: _tools.RODict({
        "ID": 101709,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80331001, 5, 4], [80431001, 5, 4]]),
        "props": None
    }),
    101710: _tools.RODict({
        "ID": 101710,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjSlowAnti":1}),
        "equipment": _tools.ROList([[80331001, 6, 4], [80431001, 6, 4]]),
        "props": None
    }),
    101711: _tools.RODict({
        "ID": 101711,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80131001, 3, 1], [80781001, 3, 1]]),
        "props": None
    }),
    101712: _tools.RODict({
        "ID": 101712,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80131001, 4, 1], [80781001, 4, 1]]),
        "props": None
    }),
    101713: _tools.RODict({
        "ID": 101713,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80131001, 5, 1], [80781001, 5, 1]]),
        "props": None
    }),
    101714: _tools.RODict({
        "ID": 101714,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80131001, 3, 2], [80781001, 3, 2]]),
        "props": None
    }),
    101715: _tools.RODict({
        "ID": 101715,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80131001, 4, 2], [80781001, 4, 2]]),
        "props": None
    }),
    101716: _tools.RODict({
        "ID": 101716,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80131001, 5, 2], [80781001, 5, 2]]),
        "props": None
    }),
    101717: _tools.RODict({
        "ID": 101717,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80131001, 6, 2], [80781001, 6, 2]]),
        "props": None
    }),
    101718: _tools.RODict({
        "ID": 101718,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80131001, 3, 3], [80781001, 3, 3]]),
        "props": None
    }),
    101719: _tools.RODict({
        "ID": 101719,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80131001, 4, 3], [80781001, 4, 3]]),
        "props": None
    }),
    101720: _tools.RODict({
        "ID": 101720,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80131001, 5, 3], [80781001, 5, 3]]),
        "props": None
    }),
    101721: _tools.RODict({
        "ID": 101721,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80131001, 6, 3], [80781001, 6, 3]]),
        "props": None
    }),
    101722: _tools.RODict({
        "ID": 101722,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80131001, 3, 4], [80781001, 3, 4]]),
        "props": None
    }),
    101723: _tools.RODict({
        "ID": 101723,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80131001, 4, 4], [80781001, 4, 4]]),
        "props": None
    }),
    101724: _tools.RODict({
        "ID": 101724,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80131001, 5, 4], [80781001, 5, 4]]),
        "props": None
    }),
    101725: _tools.RODict({
        "ID": 101725,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushEnh":1}),
        "equipment": _tools.ROList([[80131001, 6, 4], [80781001, 6, 4]]),
        "props": None
    }),
    101726: _tools.RODict({
        "ID": 101726,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80131001, 3, 1], [80431001, 3, 1]]),
        "props": None
    }),
    101727: _tools.RODict({
        "ID": 101727,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80131001, 4, 1], [80431001, 4, 1]]),
        "props": None
    }),
    101728: _tools.RODict({
        "ID": 101728,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80131001, 5, 1], [80431001, 5, 1]]),
        "props": None
    }),
    101729: _tools.RODict({
        "ID": 101729,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80131001, 3, 2], [80431001, 3, 2]]),
        "props": None
    }),
    101730: _tools.RODict({
        "ID": 101730,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80131001, 4, 2], [80431001, 4, 2]]),
        "props": None
    }),
    101731: _tools.RODict({
        "ID": 101731,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80131001, 5, 2], [80431001, 5, 2]]),
        "props": None
    }),
    101732: _tools.RODict({
        "ID": 101732,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80131001, 6, 2], [80431001, 6, 2]]),
        "props": None
    }),
    101733: _tools.RODict({
        "ID": 101733,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80131001, 3, 3], [80431001, 3, 3]]),
        "props": None
    }),
    101734: _tools.RODict({
        "ID": 101734,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80131001, 4, 3], [80431001, 4, 3]]),
        "props": None
    }),
    101735: _tools.RODict({
        "ID": 101735,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80131001, 5, 3], [80431001, 5, 3]]),
        "props": None
    }),
    101736: _tools.RODict({
        "ID": 101736,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80131001, 6, 3], [80431001, 6, 3]]),
        "props": None
    }),
    101737: _tools.RODict({
        "ID": 101737,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80131001, 3, 4], [80431001, 3, 4]]),
        "props": None
    }),
    101738: _tools.RODict({
        "ID": 101738,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80131001, 4, 4], [80431001, 4, 4]]),
        "props": None
    }),
    101739: _tools.RODict({
        "ID": 101739,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80131001, 5, 4], [80431001, 5, 4]]),
        "props": None
    }),
    101740: _tools.RODict({
        "ID": 101740,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjPushAnti":1}),
        "equipment": _tools.ROList([[80131001, 6, 4], [80431001, 6, 4]]),
        "props": None
    }),
    101741: _tools.RODict({
        "ID": 101741,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80581001, 3, 1], [80681001, 3, 1]]),
        "props": None
    }),
    101742: _tools.RODict({
        "ID": 101742,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80581001, 4, 1], [80681001, 4, 1]]),
        "props": None
    }),
    101743: _tools.RODict({
        "ID": 101743,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80581001, 5, 1], [80681001, 5, 1]]),
        "props": None
    }),
    101744: _tools.RODict({
        "ID": 101744,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80581001, 3, 2], [80681001, 3, 2]]),
        "props": None
    }),
    101745: _tools.RODict({
        "ID": 101745,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80581001, 4, 2], [80681001, 4, 2]]),
        "props": None
    }),
    101746: _tools.RODict({
        "ID": 101746,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80581001, 5, 2], [80681001, 5, 2]]),
        "props": None
    }),
    101747: _tools.RODict({
        "ID": 101747,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80581001, 6, 2], [80681001, 6, 2]]),
        "props": None
    }),
    101748: _tools.RODict({
        "ID": 101748,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80581001, 3, 3], [80681001, 3, 3]]),
        "props": None
    }),
    101749: _tools.RODict({
        "ID": 101749,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80581001, 4, 3], [80681001, 4, 3]]),
        "props": None
    }),
    101750: _tools.RODict({
        "ID": 101750,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80581001, 5, 3], [80681001, 5, 3]]),
        "props": None
    }),
    101751: _tools.RODict({
        "ID": 101751,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80581001, 6, 3], [80681001, 6, 3]]),
        "props": None
    }),
    101752: _tools.RODict({
        "ID": 101752,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80581001, 3, 4], [80681001, 3, 4]]),
        "props": None
    }),
    101753: _tools.RODict({
        "ID": 101753,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80581001, 4, 4], [80681001, 4, 4]]),
        "props": None
    }),
    101754: _tools.RODict({
        "ID": 101754,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80581001, 5, 4], [80681001, 5, 4]]),
        "props": None
    }),
    101755: _tools.RODict({
        "ID": 101755,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockEnh":1}),
        "equipment": _tools.ROList([[80581001, 6, 4], [80681001, 6, 4]]),
        "props": None
    }),
    101756: _tools.RODict({
        "ID": 101756,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80831001, 3, 1], [80331001, 3, 1]]),
        "props": None
    }),
    101757: _tools.RODict({
        "ID": 101757,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80831001, 4, 1], [80331001, 4, 1]]),
        "props": None
    }),
    101758: _tools.RODict({
        "ID": 101758,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80831001, 5, 1], [80331001, 5, 1]]),
        "props": None
    }),
    101759: _tools.RODict({
        "ID": 101759,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80831001, 3, 2], [80331001, 3, 2]]),
        "props": None
    }),
    101760: _tools.RODict({
        "ID": 101760,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80831001, 4, 2], [80331001, 4, 2]]),
        "props": None
    }),
    101761: _tools.RODict({
        "ID": 101761,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80831001, 5, 2], [80331001, 5, 2]]),
        "props": None
    }),
    101762: _tools.RODict({
        "ID": 101762,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80831001, 6, 2], [80331001, 6, 2]]),
        "props": None
    }),
    101763: _tools.RODict({
        "ID": 101763,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80831001, 3, 3], [80331001, 3, 3]]),
        "props": None
    }),
    101764: _tools.RODict({
        "ID": 101764,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80831001, 4, 3], [80331001, 4, 3]]),
        "props": None
    }),
    101765: _tools.RODict({
        "ID": 101765,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80831001, 5, 3], [80331001, 5, 3]]),
        "props": None
    }),
    101766: _tools.RODict({
        "ID": 101766,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80831001, 6, 3], [80331001, 6, 3]]),
        "props": None
    }),
    101767: _tools.RODict({
        "ID": 101767,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80831001, 3, 4], [80331001, 3, 4]]),
        "props": None
    }),
    101768: _tools.RODict({
        "ID": 101768,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80831001, 4, 4], [80331001, 4, 4]]),
        "props": None
    }),
    101769: _tools.RODict({
        "ID": 101769,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80831001, 5, 4], [80331001, 5, 4]]),
        "props": None
    }),
    101770: _tools.RODict({
        "ID": 101770,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "propList": _tools.RODict({"adjKnockAnti":1}),
        "equipment": _tools.ROList([[80831001, 6, 4], [80331001, 6, 4]]),
        "props": None
    }),
    101771: _tools.RODict({
        "ID": 101771,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.005}),
        "equipment": None,
        "props": _tools.ROList([30001001, 30001002, 30001007])
    }),
    101772: _tools.RODict({
        "ID": 101772,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.005}),
        "equipment": None,
        "props": _tools.ROList([30001003, 30001004, 30001010])
    }),
    101773: _tools.RODict({
        "ID": 101773,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.005}),
        "equipment": None,
        "props": _tools.ROList([30001005, 30001006, 30001036])
    }),
    101774: _tools.RODict({
        "ID": 101774,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.005}),
        "equipment": None,
        "props": _tools.ROList([30001007, 30001008, 30001001])
    }),
    101775: _tools.RODict({
        "ID": 101775,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.005}),
        "equipment": None,
        "props": _tools.ROList([30001009, 30001010, 30001004])
    }),
    101776: _tools.RODict({
        "ID": 101776,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.005}),
        "equipment": None,
        "props": _tools.ROList([30001034, 30001035, 30001037])
    }),
    101777: _tools.RODict({
        "ID": 101777,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.005}),
        "equipment": None,
        "props": _tools.ROList([30001036, 30001037, 30001008])
    }),
    101778: _tools.RODict({
        "ID": 101778,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.005}),
        "equipment": None,
        "props": _tools.ROList([30001038, 30001001, 30001034])
    }),
    101779: _tools.RODict({
        "ID": 101779,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.005}),
        "equipment": None,
        "props": _tools.ROList([30001001, 30001002, 30001003])
    }),
    101780: _tools.RODict({
        "ID": 101780,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.005}),
        "equipment": None,
        "props": _tools.ROList([30001004, 30001005, 30001006])
    }),
    101781: _tools.RODict({
        "ID": 101781,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.005}),
        "equipment": None,
        "props": _tools.ROList([30001007, 30001008, 30001009])
    }),
    101782: _tools.RODict({
        "ID": 101782,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.005}),
        "equipment": None,
        "props": _tools.ROList([30001010, 30001034, 30001035])
    }),
    101783: _tools.RODict({
        "ID": 101783,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.005}),
        "equipment": None,
        "props": _tools.ROList([30001036, 30001037, 30001038])
    }),
    101784: _tools.RODict({
        "ID": 101784,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.005}),
        "equipment": None,
        "props": _tools.ROList([30001002, 30001005, 30001009])
    }),
    101785: _tools.RODict({
        "ID": 101785,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.005}),
        "equipment": None,
        "props": _tools.ROList([30001001, 30001002, 30001003, 30001004, 30001005])
    }),
    101786: _tools.RODict({
        "ID": 101786,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.005}),
        "equipment": None,
        "props": _tools.ROList([30001006, 30001007, 30001008, 30001009, 30001010])
    }),
    101787: _tools.RODict({
        "ID": 101787,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.005}),
        "equipment": None,
        "props": _tools.ROList([30001034, 30001035, 30001036, 30001037, 30001038])
    }),
    101788: _tools.RODict({
        "ID": 101788,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30001011, 30001002, 30001003])
    }),
    101789: _tools.RODict({
        "ID": 101789,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30001012, 30001004, 30001005])
    }),
    101790: _tools.RODict({
        "ID": 101790,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30001013, 30001006, 30001007])
    }),
    101791: _tools.RODict({
        "ID": 101791,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30001014, 30001008, 30001009])
    }),
    101792: _tools.RODict({
        "ID": 101792,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30001015, 30001010, 30001034])
    }),
    101793: _tools.RODict({
        "ID": 101793,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30001016, 30001035, 30001036])
    }),
    101794: _tools.RODict({
        "ID": 101794,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30001017, 30001037, 30001038])
    }),
    101795: _tools.RODict({
        "ID": 101795,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30001018, 30001003, 30001004])
    }),
    101796: _tools.RODict({
        "ID": 101796,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30001019, 30001005, 30001006])
    }),
    101797: _tools.RODict({
        "ID": 101797,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30001020, 30001007, 30001008])
    }),
    101798: _tools.RODict({
        "ID": 101798,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30001039, 30001009, 30001010])
    }),
    101799: _tools.RODict({
        "ID": 101799,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30001040, 30001034, 30001035])
    }),
    101800: _tools.RODict({
        "ID": 101800,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30001041, 30001036, 30001037])
    }),
    101801: _tools.RODict({
        "ID": 101801,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30001042, 30001038, 30001001])
    }),
    101802: _tools.RODict({
        "ID": 101802,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30001043, 30001002, 30001005])
    }),
    101803: _tools.RODict({
        "ID": 101803,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.015}),
        "equipment": None,
        "props": _tools.ROList([30001011, 30001012, 30001006, 30001007, 30001008])
    }),
    101804: _tools.RODict({
        "ID": 101804,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.015}),
        "equipment": None,
        "props": _tools.ROList([30001013, 30001014, 30001009, 30001010, 30001034])
    }),
    101805: _tools.RODict({
        "ID": 101805,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.015}),
        "equipment": None,
        "props": _tools.ROList([30001015, 30001016, 30001035, 30001036, 30001037])
    }),
    101806: _tools.RODict({
        "ID": 101806,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.015}),
        "equipment": None,
        "props": _tools.ROList([30001017, 30001018, 30001038, 30001001, 30001002])
    }),
    101807: _tools.RODict({
        "ID": 101807,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.015}),
        "equipment": None,
        "props": _tools.ROList([30001019, 30001020, 30001003, 30001004, 30001005])
    }),
    101808: _tools.RODict({
        "ID": 101808,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.015}),
        "equipment": None,
        "props": _tools.ROList([30001039, 30001040, 30001010, 30001034, 30001035])
    }),
    101809: _tools.RODict({
        "ID": 101809,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.015}),
        "equipment": None,
        "props": _tools.ROList([30001041, 30001042, 30001007, 30001008, 30001009])
    }),
    101810: _tools.RODict({
        "ID": 101810,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.015}),
        "equipment": None,
        "props": _tools.ROList([30001043, 30001017, 30001036, 30001037, 30001038])
    }),
    101811: _tools.RODict({
        "ID": 101811,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.015}),
        "equipment": None,
        "props": _tools.ROList([30001011, 30001012, 30001013])
    }),
    101812: _tools.RODict({
        "ID": 101812,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.015}),
        "equipment": None,
        "props": _tools.ROList([30001014, 30001015, 30001016])
    }),
    101813: _tools.RODict({
        "ID": 101813,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.015}),
        "equipment": None,
        "props": _tools.ROList([30001017, 30001018, 30001019])
    }),
    101814: _tools.RODict({
        "ID": 101814,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.015}),
        "equipment": None,
        "props": _tools.ROList([30001020, 30001039, 30001040])
    }),
    101815: _tools.RODict({
        "ID": 101815,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.015}),
        "equipment": None,
        "props": _tools.ROList([30001041, 30001042, 30001043])
    }),
    101816: _tools.RODict({
        "ID": 101816,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.005}),
        "equipment": None,
        "props": _tools.ROList([30003002, 30003003, 30003004])
    }),
    101817: _tools.RODict({
        "ID": 101817,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.005}),
        "equipment": None,
        "props": _tools.ROList([30003005, 30003006, 30003007])
    }),
    101818: _tools.RODict({
        "ID": 101818,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.005}),
        "equipment": None,
        "props": _tools.ROList([30003008, 30003009, 30003010])
    }),
    101819: _tools.RODict({
        "ID": 101819,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.005}),
        "equipment": None,
        "props": _tools.ROList([30003011, 30003012, 30003013])
    }),
    101820: _tools.RODict({
        "ID": 101820,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.005}),
        "equipment": None,
        "props": _tools.ROList([30003014, 30003015, 30003016])
    }),
    101821: _tools.RODict({
        "ID": 101821,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.005}),
        "equipment": None,
        "props": _tools.ROList([30003017, 30003018, 30003019])
    }),
    101822: _tools.RODict({
        "ID": 101822,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.005}),
        "equipment": None,
        "props": _tools.ROList([30003020, 30003021, 30003022])
    }),
    101823: _tools.RODict({
        "ID": 101823,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.005}),
        "equipment": None,
        "props": _tools.ROList([30003023, 30003024, 30003025])
    }),
    101824: _tools.RODict({
        "ID": 101824,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.005}),
        "equipment": None,
        "props": _tools.ROList([30003026, 30003027, 30003001])
    }),
    101825: _tools.RODict({
        "ID": 101825,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.005}),
        "equipment": None,
        "props": _tools.ROList([30003001, 30003002, 30003003, 30003004, 30003005])
    }),
    101826: _tools.RODict({
        "ID": 101826,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.005}),
        "equipment": None,
        "props": _tools.ROList([30003006, 30003007, 30003008, 30003009, 30003010])
    }),
    101827: _tools.RODict({
        "ID": 101827,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.005}),
        "equipment": None,
        "props": _tools.ROList([30003011, 30003012, 30003013, 30003014, 30003015])
    }),
    101828: _tools.RODict({
        "ID": 101828,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.005}),
        "equipment": None,
        "props": _tools.ROList([30003016, 30003017, 30003018, 30003019, 30003020])
    }),
    101829: _tools.RODict({
        "ID": 101829,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.005}),
        "equipment": None,
        "props": _tools.ROList([30003021, 30003022, 30003023, 30003024, 30003025])
    }),
    101830: _tools.RODict({
        "ID": 101830,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.005}),
        "equipment": None,
        "props": _tools.ROList([30003026, 30003027, 30003001, 30003002, 30003003])
    }),
    101831: _tools.RODict({
        "ID": 101831,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30003103, 30003104, 30003019, 30003020, 30003021])
    }),
    101832: _tools.RODict({
        "ID": 101832,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30003105, 30003106, 30003022, 30003023, 30003024])
    }),
    101833: _tools.RODict({
        "ID": 101833,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30003107, 30003108, 30003025, 30003026, 30003027])
    }),
    101834: _tools.RODict({
        "ID": 101834,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30003109, 30003110, 30003001, 30003002, 30003003])
    }),
    101835: _tools.RODict({
        "ID": 101835,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30003113, 30003114, 30003004, 30003005, 30003006])
    }),
    101836: _tools.RODict({
        "ID": 101836,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30003111, 30003112, 30003007, 30003008, 30003009])
    }),
    101837: _tools.RODict({
        "ID": 101837,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30003115, 30003116, 30003010, 30003011, 30003012])
    }),
    101838: _tools.RODict({
        "ID": 101838,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30003117, 30003118, 30003013, 30003014, 30003015])
    }),
    101839: _tools.RODict({
        "ID": 101839,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30003119, 30003120, 30003016, 30003017, 30003018])
    }),
    101840: _tools.RODict({
        "ID": 101840,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30003121, 30003122, 30003019, 30003020, 30003021])
    }),
    101841: _tools.RODict({
        "ID": 101841,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30003123, 30003124, 30003022, 30003023, 30003024])
    }),
    101842: _tools.RODict({
        "ID": 101842,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30003125, 30003126, 30003025, 30003026, 30003027])
    }),
    101843: _tools.RODict({
        "ID": 101843,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30003127, 30003101, 30003003, 30003004, 30003005])
    }),
    101844: _tools.RODict({
        "ID": 101844,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjExpGrow":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30003102, 30003103, 30003006, 30003007, 30003008])
    }),
    101845: _tools.RODict({
        "ID": 101845,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30003101, 30003102, 30003103, 30003001, 30003002])
    }),
    101846: _tools.RODict({
        "ID": 101846,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30003104, 30003105, 30003106, 30003003, 30003004])
    }),
    101847: _tools.RODict({
        "ID": 101847,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30003110, 30003111, 30003112, 30003005, 30003006])
    }),
    101848: _tools.RODict({
        "ID": 101848,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30003107, 30003108, 30003109, 30003007, 30003008])
    }),
    101849: _tools.RODict({
        "ID": 101849,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30003113, 30003114, 30003115, 30003009, 30003010])
    }),
    101850: _tools.RODict({
        "ID": 101850,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30003116, 30003117, 30003118, 30003011, 30003012])
    }),
    101851: _tools.RODict({
        "ID": 101851,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30003119, 30003120, 30003121, 30003013, 30003014])
    }),
    101852: _tools.RODict({
        "ID": 101852,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30003122, 30003123, 30003124, 30003015, 30003016])
    }),
    101853: _tools.RODict({
        "ID": 101853,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30003125, 30003126, 30003127, 30003017, 30003018])
    }),
    101854: _tools.RODict({
        "ID": 101854,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30003105, 30003106, 30003107, 30003108])
    }),
    101855: _tools.RODict({
        "ID": 101855,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30003109, 30003110, 30003111, 30003112])
    }),
    101856: _tools.RODict({
        "ID": 101856,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30003113, 30003114, 30003115, 30003116])
    }),
    101857: _tools.RODict({
        "ID": 101857,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.0075}),
        "equipment": None,
        "props": _tools.ROList([30003117, 30003118, 30003119, 30003120])
    }),
    101858: _tools.RODict({
        "ID": 101858,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.01}),
        "equipment": None,
        "props": _tools.ROList([30003121, 30003122, 30003123, 30003124])
    }),
    101859: _tools.RODict({
        "ID": 101859,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.01}),
        "equipment": None,
        "props": _tools.ROList([30003125, 30003126, 30003127, 30003101])
    }),
    101860: _tools.RODict({
        "ID": 101860,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjCopper":0.01}),
        "equipment": None,
        "props": _tools.ROList([30003102, 30003103, 30003104, 30003105])
    }),
    101861: _tools.RODict({
        "ID": 101861,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjFinalDmgAnti":0.015}),
        "equipment": None,
        "props": _tools.ROList([30990198, 30990190, 30990174, 30990191])
    }),
    101862: _tools.RODict({
        "ID": 101862,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjFinalDmgAnti":0.015}),
        "equipment": None,
        "props": _tools.ROList([30990192, 30990193, 30990175, 30990194])
    }),
    101863: _tools.RODict({
        "ID": 101863,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjFinalDmg":0.015}),
        "equipment": None,
        "props": _tools.ROList([30990163, 30990164, 30990165, 30990173, 30990162])
    }),
    101864: _tools.RODict({
        "ID": 101864,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjFinalDmg":0.015}),
        "equipment": None,
        "props": _tools.ROList([30990195, 30990196, 30990188])
    }),
    101865: _tools.RODict({
        "ID": 101865,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjFinalDmg":0.015}),
        "equipment": None,
        "props": _tools.ROList([30990176, 30990177, 30990178, 30990179, 30990180, 30990181])
    }),
    101866: _tools.RODict({
        "ID": 101866,
        "unavailableClass": None,
        "propList": _tools.RODict({"adjFinalDmgAnti":0.015}),
        "equipment": None,
        "props": _tools.ROList([30990183, 30990184, 30990185, 30990186, 30990187])
    })
})
minKey = 100001
maxKey = 101866