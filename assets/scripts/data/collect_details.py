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
        "unavailableClass": _tools.ROList([1001, 1002]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxMagicAtk":1}),
        "equipment": _tools.ROList([[80111001, 0, 1], [80121001, 0, 1], [80131001, 0, 1]]),
        "props": None
    }),
    100002: _tools.RODict({
        "ID": 100002,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxMagicAtk":1}),
        "equipment": _tools.ROList([[80111001, 1, 1], [80121001, 1, 1], [80131001, 1, 1]]),
        "props": None
    }),
    100003: _tools.RODict({
        "ID": 100003,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxMagicAtk":2}),
        "equipment": _tools.ROList([[80111001, 2, 1], [80121001, 2, 1], [80131001, 2, 1]]),
        "props": None
    }),
    100004: _tools.RODict({
        "ID": 100004,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxMagicAtk":2}),
        "equipment": _tools.ROList([[80111001, 3, 1], [80121001, 3, 1], [80131001, 3, 1]]),
        "props": None
    }),
    100005: _tools.RODict({
        "ID": 100005,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxMagicAtk":3}),
        "equipment": _tools.ROList([[80111001, 4, 1], [80121001, 4, 1], [80131001, 4, 1]]),
        "props": None
    }),
    100006: _tools.RODict({
        "ID": 100006,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxMagicAtk":3}),
        "equipment": _tools.ROList([[80111001, 5, 1], [80121001, 5, 1], [80131001, 5, 1]]),
        "props": None
    }),
    100007: _tools.RODict({
        "ID": 100007,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxMagicAtk":4}),
        "equipment": _tools.ROList([[80111001, 6, 1], [80121001, 6, 1], [80131001, 6, 1]]),
        "props": None
    }),
    100008: _tools.RODict({
        "ID": 100008,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxMagicAtk":4}),
        "equipment": _tools.ROList([[80111001, 7, 1], [80121001, 7, 1], [80131001, 7, 1]]),
        "props": None
    }),
    100009: _tools.RODict({
        "ID": 100009,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxMagicAtk":2}),
        "equipment": _tools.ROList([[80111001, 0, 2], [80121001, 0, 2], [80131001, 0, 2]]),
        "props": None
    }),
    100010: _tools.RODict({
        "ID": 100010,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxMagicAtk":2}),
        "equipment": _tools.ROList([[80111001, 1, 2], [80121001, 1, 2], [80131001, 1, 2]]),
        "props": None
    }),
    100011: _tools.RODict({
        "ID": 100011,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxMagicAtk":3}),
        "equipment": _tools.ROList([[80111001, 2, 2], [80121001, 2, 2], [80131001, 2, 2]]),
        "props": None
    }),
    100012: _tools.RODict({
        "ID": 100012,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxMagicAtk":3}),
        "equipment": _tools.ROList([[80111001, 3, 2], [80121001, 3, 2], [80131001, 3, 2]]),
        "props": None
    }),
    100013: _tools.RODict({
        "ID": 100013,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxMagicAtk":4}),
        "equipment": _tools.ROList([[80111001, 4, 2], [80121001, 4, 2], [80131001, 4, 2]]),
        "props": None
    }),
    100014: _tools.RODict({
        "ID": 100014,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxMagicAtk":4}),
        "equipment": _tools.ROList([[80111001, 5, 2], [80121001, 5, 2], [80131001, 5, 2]]),
        "props": None
    }),
    100015: _tools.RODict({
        "ID": 100015,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxMagicAtk":5}),
        "equipment": _tools.ROList([[80111001, 6, 2], [80121001, 6, 2], [80131001, 6, 2]]),
        "props": None
    }),
    100016: _tools.RODict({
        "ID": 100016,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxMagicAtk":5}),
        "equipment": _tools.ROList([[80111001, 7, 2], [80121001, 7, 2], [80131001, 7, 2]]),
        "props": None
    }),
    100017: _tools.RODict({
        "ID": 100017,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxMagicAtk":3}),
        "equipment": _tools.ROList([[80111001, 0, 3], [80121001, 0, 3], [80131001, 0, 3]]),
        "props": None
    }),
    100018: _tools.RODict({
        "ID": 100018,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxMagicAtk":3}),
        "equipment": _tools.ROList([[80111001, 1, 3], [80121001, 1, 3], [80131001, 1, 3]]),
        "props": None
    }),
    100019: _tools.RODict({
        "ID": 100019,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxMagicAtk":4}),
        "equipment": _tools.ROList([[80111001, 2, 3], [80121001, 2, 3], [80131001, 2, 3]]),
        "props": None
    }),
    100020: _tools.RODict({
        "ID": 100020,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxMagicAtk":4}),
        "equipment": _tools.ROList([[80111001, 3, 3], [80121001, 3, 3], [80131001, 3, 3]]),
        "props": None
    }),
    100021: _tools.RODict({
        "ID": 100021,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxMagicAtk":5}),
        "equipment": _tools.ROList([[80111001, 4, 3], [80121001, 4, 3], [80131001, 4, 3]]),
        "props": None
    }),
    100022: _tools.RODict({
        "ID": 100022,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxMagicAtk":5}),
        "equipment": _tools.ROList([[80111001, 5, 3], [80121001, 5, 3], [80131001, 5, 3]]),
        "props": None
    }),
    100023: _tools.RODict({
        "ID": 100023,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxMagicAtk":6}),
        "equipment": _tools.ROList([[80111001, 6, 3], [80121001, 6, 3], [80131001, 6, 3]]),
        "props": None
    }),
    100024: _tools.RODict({
        "ID": 100024,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxMagicAtk":6}),
        "equipment": _tools.ROList([[80111001, 7, 3], [80121001, 7, 3], [80131001, 7, 3]]),
        "props": None
    }),
    100025: _tools.RODict({
        "ID": 100025,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxMagicAtk":4}),
        "equipment": _tools.ROList([[80111001, 0, 4], [80121001, 0, 4], [80131001, 0, 4]]),
        "props": None
    }),
    100026: _tools.RODict({
        "ID": 100026,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxMagicAtk":4}),
        "equipment": _tools.ROList([[80111001, 1, 4], [80121001, 1, 4], [80131001, 1, 4]]),
        "props": None
    }),
    100027: _tools.RODict({
        "ID": 100027,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxMagicAtk":5}),
        "equipment": _tools.ROList([[80111001, 2, 4], [80121001, 2, 4], [80131001, 2, 4]]),
        "props": None
    }),
    100028: _tools.RODict({
        "ID": 100028,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxMagicAtk":5}),
        "equipment": _tools.ROList([[80111001, 3, 4], [80121001, 3, 4], [80131001, 3, 4]]),
        "props": None
    }),
    100029: _tools.RODict({
        "ID": 100029,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxMagicAtk":6}),
        "equipment": _tools.ROList([[80111001, 4, 4], [80121001, 4, 4], [80131001, 4, 4]]),
        "props": None
    }),
    100030: _tools.RODict({
        "ID": 100030,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxMagicAtk":6}),
        "equipment": _tools.ROList([[80111001, 5, 4], [80121001, 5, 4], [80131001, 5, 4]]),
        "props": None
    }),
    100031: _tools.RODict({
        "ID": 100031,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxMagicAtk":7}),
        "equipment": _tools.ROList([[80111001, 6, 4], [80121001, 6, 4], [80131001, 6, 4]]),
        "props": None
    }),
    100032: _tools.RODict({
        "ID": 100032,
        "unavailableClass": _tools.ROList([1001, 1002]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxMagicAtk":7}),
        "equipment": _tools.ROList([[80111001, 7, 4], [80121001, 7, 4], [80131001, 7, 4]]),
        "props": None
    }),
    100033: _tools.RODict({
        "ID": 100033,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjFullHp":26}),
        "equipment": _tools.ROList([[80211001, 0, 1], [80221001, 0, 1], [80231001, 0, 1]]),
        "props": None
    }),
    100034: _tools.RODict({
        "ID": 100034,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjFullHp":26}),
        "equipment": _tools.ROList([[80211001, 1, 1], [80221001, 1, 1], [80231001, 1, 1]]),
        "props": None
    }),
    100035: _tools.RODict({
        "ID": 100035,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjFullHp":66}),
        "equipment": _tools.ROList([[80211001, 2, 1], [80221001, 2, 1], [80231001, 2, 1]]),
        "props": None
    }),
    100036: _tools.RODict({
        "ID": 100036,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjFullHp":66}),
        "equipment": _tools.ROList([[80211001, 3, 1], [80221001, 3, 1], [80231001, 3, 1]]),
        "props": None
    }),
    100037: _tools.RODict({
        "ID": 100037,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjFullHp":106}),
        "equipment": _tools.ROList([[80211001, 4, 1], [80221001, 4, 1], [80231001, 4, 1]]),
        "props": None
    }),
    100038: _tools.RODict({
        "ID": 100038,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjFullHp":106}),
        "equipment": _tools.ROList([[80211001, 5, 1], [80221001, 5, 1], [80231001, 5, 1]]),
        "props": None
    }),
    100039: _tools.RODict({
        "ID": 100039,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjFullHp":146}),
        "equipment": _tools.ROList([[80211001, 6, 1], [80221001, 6, 1], [80231001, 6, 1]]),
        "props": None
    }),
    100040: _tools.RODict({
        "ID": 100040,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjFullHp":146}),
        "equipment": _tools.ROList([[80211001, 7, 1], [80221001, 7, 1], [80231001, 7, 1]]),
        "props": None
    }),
    100041: _tools.RODict({
        "ID": 100041,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjFullHp":66}),
        "equipment": _tools.ROList([[80211001, 0, 2], [80221001, 0, 2], [80231001, 0, 2]]),
        "props": None
    }),
    100042: _tools.RODict({
        "ID": 100042,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjFullHp":66}),
        "equipment": _tools.ROList([[80211001, 1, 2], [80221001, 1, 2], [80231001, 1, 2]]),
        "props": None
    }),
    100043: _tools.RODict({
        "ID": 100043,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjFullHp":106}),
        "equipment": _tools.ROList([[80211001, 2, 2], [80221001, 2, 2], [80231001, 2, 2]]),
        "props": None
    }),
    100044: _tools.RODict({
        "ID": 100044,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjFullHp":106}),
        "equipment": _tools.ROList([[80211001, 3, 2], [80221001, 3, 2], [80231001, 3, 2]]),
        "props": None
    }),
    100045: _tools.RODict({
        "ID": 100045,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjFullHp":146}),
        "equipment": _tools.ROList([[80211001, 4, 2], [80221001, 4, 2], [80231001, 4, 2]]),
        "props": None
    }),
    100046: _tools.RODict({
        "ID": 100046,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjFullHp":146}),
        "equipment": _tools.ROList([[80211001, 5, 2], [80221001, 5, 2], [80231001, 5, 2]]),
        "props": None
    }),
    100047: _tools.RODict({
        "ID": 100047,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjFullHp":186}),
        "equipment": _tools.ROList([[80211001, 6, 2], [80221001, 6, 2], [80231001, 6, 2]]),
        "props": None
    }),
    100048: _tools.RODict({
        "ID": 100048,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjFullHp":186}),
        "equipment": _tools.ROList([[80211001, 7, 2], [80221001, 7, 2], [80231001, 7, 2]]),
        "props": None
    }),
    100049: _tools.RODict({
        "ID": 100049,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjFullHp":106}),
        "equipment": _tools.ROList([[80211001, 0, 3], [80221001, 0, 3], [80231001, 0, 3]]),
        "props": None
    }),
    100050: _tools.RODict({
        "ID": 100050,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjFullHp":106}),
        "equipment": _tools.ROList([[80211001, 1, 3], [80221001, 1, 3], [80231001, 1, 3]]),
        "props": None
    }),
    100051: _tools.RODict({
        "ID": 100051,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjFullHp":146}),
        "equipment": _tools.ROList([[80211001, 2, 3], [80221001, 2, 3], [80231001, 2, 3]]),
        "props": None
    }),
    100052: _tools.RODict({
        "ID": 100052,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjFullHp":146}),
        "equipment": _tools.ROList([[80211001, 3, 3], [80221001, 3, 3], [80231001, 3, 3]]),
        "props": None
    }),
    100053: _tools.RODict({
        "ID": 100053,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjFullHp":186}),
        "equipment": _tools.ROList([[80211001, 4, 3], [80221001, 4, 3], [80231001, 4, 3]]),
        "props": None
    }),
    100054: _tools.RODict({
        "ID": 100054,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjFullHp":186}),
        "equipment": _tools.ROList([[80211001, 5, 3], [80221001, 5, 3], [80231001, 5, 3]]),
        "props": None
    }),
    100055: _tools.RODict({
        "ID": 100055,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjFullHp":226}),
        "equipment": _tools.ROList([[80211001, 6, 3], [80221001, 6, 3], [80231001, 6, 3]]),
        "props": None
    }),
    100056: _tools.RODict({
        "ID": 100056,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjFullHp":226}),
        "equipment": _tools.ROList([[80211001, 7, 3], [80221001, 7, 3], [80231001, 7, 3]]),
        "props": None
    }),
    100057: _tools.RODict({
        "ID": 100057,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjFullHp":146}),
        "equipment": _tools.ROList([[80211001, 0, 4], [80221001, 0, 4], [80231001, 0, 4]]),
        "props": None
    }),
    100058: _tools.RODict({
        "ID": 100058,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjFullHp":146}),
        "equipment": _tools.ROList([[80211001, 1, 4], [80221001, 1, 4], [80231001, 1, 4]]),
        "props": None
    }),
    100059: _tools.RODict({
        "ID": 100059,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjFullHp":186}),
        "equipment": _tools.ROList([[80211001, 2, 4], [80221001, 2, 4], [80231001, 2, 4]]),
        "props": None
    }),
    100060: _tools.RODict({
        "ID": 100060,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjFullHp":186}),
        "equipment": _tools.ROList([[80211001, 3, 4], [80221001, 3, 4], [80231001, 3, 4]]),
        "props": None
    }),
    100061: _tools.RODict({
        "ID": 100061,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjFullHp":226}),
        "equipment": _tools.ROList([[80211001, 4, 4], [80221001, 4, 4], [80231001, 4, 4]]),
        "props": None
    }),
    100062: _tools.RODict({
        "ID": 100062,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjFullHp":226}),
        "equipment": _tools.ROList([[80211001, 5, 4], [80221001, 5, 4], [80231001, 5, 4]]),
        "props": None
    }),
    100063: _tools.RODict({
        "ID": 100063,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjFullHp":266}),
        "equipment": _tools.ROList([[80211001, 6, 4], [80221001, 6, 4], [80231001, 6, 4]]),
        "props": None
    }),
    100064: _tools.RODict({
        "ID": 100064,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjFullHp":266}),
        "equipment": _tools.ROList([[80211001, 7, 4], [80221001, 7, 4], [80231001, 7, 4]]),
        "props": None
    }),
    100065: _tools.RODict({
        "ID": 100065,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmg":0.001}),
        "equipment": _tools.ROList([[80311001, 0, 1], [80321001, 0, 1], [80331001, 0, 1]]),
        "props": None
    }),
    100066: _tools.RODict({
        "ID": 100066,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmg":0.0012}),
        "equipment": _tools.ROList([[80311001, 1, 1], [80321001, 1, 1], [80331001, 1, 1]]),
        "props": None
    }),
    100067: _tools.RODict({
        "ID": 100067,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmg":0.0014}),
        "equipment": _tools.ROList([[80311001, 2, 1], [80321001, 2, 1], [80331001, 2, 1]]),
        "props": None
    }),
    100068: _tools.RODict({
        "ID": 100068,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmg":0.0016}),
        "equipment": _tools.ROList([[80311001, 3, 1], [80321001, 3, 1], [80331001, 3, 1]]),
        "props": None
    }),
    100069: _tools.RODict({
        "ID": 100069,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmg":0.0018}),
        "equipment": _tools.ROList([[80311001, 4, 1], [80321001, 4, 1], [80331001, 4, 1]]),
        "props": None
    }),
    100070: _tools.RODict({
        "ID": 100070,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmg":0.002}),
        "equipment": _tools.ROList([[80311001, 5, 1], [80321001, 5, 1], [80331001, 5, 1]]),
        "props": None
    }),
    100071: _tools.RODict({
        "ID": 100071,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmg":0.0022}),
        "equipment": _tools.ROList([[80311001, 6, 1], [80321001, 6, 1], [80331001, 6, 1]]),
        "props": None
    }),
    100072: _tools.RODict({
        "ID": 100072,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmg":0.0024}),
        "equipment": _tools.ROList([[80311001, 7, 1], [80321001, 7, 1], [80331001, 7, 1]]),
        "props": None
    }),
    100073: _tools.RODict({
        "ID": 100073,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmg":0.0014}),
        "equipment": _tools.ROList([[80311001, 0, 2], [80321001, 0, 2], [80331001, 0, 2]]),
        "props": None
    }),
    100074: _tools.RODict({
        "ID": 100074,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmg":0.0016}),
        "equipment": _tools.ROList([[80311001, 1, 2], [80321001, 1, 2], [80331001, 1, 2]]),
        "props": None
    }),
    100075: _tools.RODict({
        "ID": 100075,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmg":0.0018}),
        "equipment": _tools.ROList([[80311001, 2, 2], [80321001, 2, 2], [80331001, 2, 2]]),
        "props": None
    }),
    100076: _tools.RODict({
        "ID": 100076,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmg":0.002}),
        "equipment": _tools.ROList([[80311001, 3, 2], [80321001, 3, 2], [80331001, 3, 2]]),
        "props": None
    }),
    100077: _tools.RODict({
        "ID": 100077,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmg":0.0022}),
        "equipment": _tools.ROList([[80311001, 4, 2], [80321001, 4, 2], [80331001, 4, 2]]),
        "props": None
    }),
    100078: _tools.RODict({
        "ID": 100078,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmg":0.0024}),
        "equipment": _tools.ROList([[80311001, 5, 2], [80321001, 5, 2], [80331001, 5, 2]]),
        "props": None
    }),
    100079: _tools.RODict({
        "ID": 100079,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmg":0.0026}),
        "equipment": _tools.ROList([[80311001, 6, 2], [80321001, 6, 2], [80331001, 6, 2]]),
        "props": None
    }),
    100080: _tools.RODict({
        "ID": 100080,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmg":0.0028}),
        "equipment": _tools.ROList([[80311001, 7, 2], [80321001, 7, 2], [80331001, 7, 2]]),
        "props": None
    }),
    100081: _tools.RODict({
        "ID": 100081,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmg":0.0018}),
        "equipment": _tools.ROList([[80311001, 0, 3], [80321001, 0, 3], [80331001, 0, 3]]),
        "props": None
    }),
    100082: _tools.RODict({
        "ID": 100082,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmg":0.002}),
        "equipment": _tools.ROList([[80311001, 1, 3], [80321001, 1, 3], [80331001, 1, 3]]),
        "props": None
    }),
    100083: _tools.RODict({
        "ID": 100083,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmg":0.0022}),
        "equipment": _tools.ROList([[80311001, 2, 3], [80321001, 2, 3], [80331001, 2, 3]]),
        "props": None
    }),
    100084: _tools.RODict({
        "ID": 100084,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmg":0.0024}),
        "equipment": _tools.ROList([[80311001, 3, 3], [80321001, 3, 3], [80331001, 3, 3]]),
        "props": None
    }),
    100085: _tools.RODict({
        "ID": 100085,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmg":0.0026}),
        "equipment": _tools.ROList([[80311001, 4, 3], [80321001, 4, 3], [80331001, 4, 3]]),
        "props": None
    }),
    100086: _tools.RODict({
        "ID": 100086,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmg":0.0028}),
        "equipment": _tools.ROList([[80311001, 5, 3], [80321001, 5, 3], [80331001, 5, 3]]),
        "props": None
    }),
    100087: _tools.RODict({
        "ID": 100087,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmg":0.003}),
        "equipment": _tools.ROList([[80311001, 6, 3], [80321001, 6, 3], [80331001, 6, 3]]),
        "props": None
    }),
    100088: _tools.RODict({
        "ID": 100088,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmg":0.0032}),
        "equipment": _tools.ROList([[80311001, 7, 3], [80321001, 7, 3], [80331001, 7, 3]]),
        "props": None
    }),
    100089: _tools.RODict({
        "ID": 100089,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmg":0.0022}),
        "equipment": _tools.ROList([[80311001, 0, 4], [80321001, 0, 4], [80331001, 0, 4]]),
        "props": None
    }),
    100090: _tools.RODict({
        "ID": 100090,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmg":0.0024}),
        "equipment": _tools.ROList([[80311001, 1, 4], [80321001, 1, 4], [80331001, 1, 4]]),
        "props": None
    }),
    100091: _tools.RODict({
        "ID": 100091,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmg":0.0026}),
        "equipment": _tools.ROList([[80311001, 2, 4], [80321001, 2, 4], [80331001, 2, 4]]),
        "props": None
    }),
    100092: _tools.RODict({
        "ID": 100092,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmg":0.0028}),
        "equipment": _tools.ROList([[80311001, 3, 4], [80321001, 3, 4], [80331001, 3, 4]]),
        "props": None
    }),
    100093: _tools.RODict({
        "ID": 100093,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmg":0.003}),
        "equipment": _tools.ROList([[80311001, 4, 4], [80321001, 4, 4], [80331001, 4, 4]]),
        "props": None
    }),
    100094: _tools.RODict({
        "ID": 100094,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmg":0.0032}),
        "equipment": _tools.ROList([[80311001, 5, 4], [80321001, 5, 4], [80331001, 5, 4]]),
        "props": None
    }),
    100095: _tools.RODict({
        "ID": 100095,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmg":0.0034}),
        "equipment": _tools.ROList([[80311001, 6, 4], [80321001, 6, 4], [80331001, 6, 4]]),
        "props": None
    }),
    100096: _tools.RODict({
        "ID": 100096,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmg":0.0036}),
        "equipment": _tools.ROList([[80311001, 7, 4], [80321001, 7, 4], [80331001, 7, 4]]),
        "props": None
    }),
    100097: _tools.RODict({
        "ID": 100097,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.001}),
        "equipment": _tools.ROList([[80411001, 0, 1], [80421001, 0, 1], [80431001, 0, 1]]),
        "props": None
    }),
    100098: _tools.RODict({
        "ID": 100098,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0012}),
        "equipment": _tools.ROList([[80411001, 1, 1], [80421001, 1, 1], [80431001, 1, 1]]),
        "props": None
    }),
    100099: _tools.RODict({
        "ID": 100099,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0014}),
        "equipment": _tools.ROList([[80411001, 2, 1], [80421001, 2, 1], [80431001, 2, 1]]),
        "props": None
    }),
    100100: _tools.RODict({
        "ID": 100100,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0016}),
        "equipment": _tools.ROList([[80411001, 3, 1], [80421001, 3, 1], [80431001, 3, 1]]),
        "props": None
    }),
    100101: _tools.RODict({
        "ID": 100101,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0018}),
        "equipment": _tools.ROList([[80411001, 4, 1], [80421001, 4, 1], [80431001, 4, 1]]),
        "props": None
    }),
    100102: _tools.RODict({
        "ID": 100102,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.002}),
        "equipment": _tools.ROList([[80411001, 5, 1], [80421001, 5, 1], [80431001, 5, 1]]),
        "props": None
    }),
    100103: _tools.RODict({
        "ID": 100103,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0022}),
        "equipment": _tools.ROList([[80411001, 6, 1], [80421001, 6, 1], [80431001, 6, 1]]),
        "props": None
    }),
    100104: _tools.RODict({
        "ID": 100104,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0024}),
        "equipment": _tools.ROList([[80411001, 7, 1], [80421001, 7, 1], [80431001, 7, 1]]),
        "props": None
    }),
    100105: _tools.RODict({
        "ID": 100105,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0014}),
        "equipment": _tools.ROList([[80411001, 0, 2], [80421001, 0, 2], [80431001, 0, 2]]),
        "props": None
    }),
    100106: _tools.RODict({
        "ID": 100106,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0016}),
        "equipment": _tools.ROList([[80411001, 1, 2], [80421001, 1, 2], [80431001, 1, 2]]),
        "props": None
    }),
    100107: _tools.RODict({
        "ID": 100107,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0018}),
        "equipment": _tools.ROList([[80411001, 2, 2], [80421001, 2, 2], [80431001, 2, 2]]),
        "props": None
    }),
    100108: _tools.RODict({
        "ID": 100108,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.002}),
        "equipment": _tools.ROList([[80411001, 3, 2], [80421001, 3, 2], [80431001, 3, 2]]),
        "props": None
    }),
    100109: _tools.RODict({
        "ID": 100109,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0022}),
        "equipment": _tools.ROList([[80411001, 4, 2], [80421001, 4, 2], [80431001, 4, 2]]),
        "props": None
    }),
    100110: _tools.RODict({
        "ID": 100110,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0024}),
        "equipment": _tools.ROList([[80411001, 5, 2], [80421001, 5, 2], [80431001, 5, 2]]),
        "props": None
    }),
    100111: _tools.RODict({
        "ID": 100111,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0026}),
        "equipment": _tools.ROList([[80411001, 6, 2], [80421001, 6, 2], [80431001, 6, 2]]),
        "props": None
    }),
    100112: _tools.RODict({
        "ID": 100112,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0028}),
        "equipment": _tools.ROList([[80411001, 7, 2], [80421001, 7, 2], [80431001, 7, 2]]),
        "props": None
    }),
    100113: _tools.RODict({
        "ID": 100113,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0018}),
        "equipment": _tools.ROList([[80411001, 0, 3], [80421001, 0, 3], [80431001, 0, 3]]),
        "props": None
    }),
    100114: _tools.RODict({
        "ID": 100114,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.002}),
        "equipment": _tools.ROList([[80411001, 1, 3], [80421001, 1, 3], [80431001, 1, 3]]),
        "props": None
    }),
    100115: _tools.RODict({
        "ID": 100115,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0022}),
        "equipment": _tools.ROList([[80411001, 2, 3], [80421001, 2, 3], [80431001, 2, 3]]),
        "props": None
    }),
    100116: _tools.RODict({
        "ID": 100116,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0024}),
        "equipment": _tools.ROList([[80411001, 3, 3], [80421001, 3, 3], [80431001, 3, 3]]),
        "props": None
    }),
    100117: _tools.RODict({
        "ID": 100117,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0026}),
        "equipment": _tools.ROList([[80411001, 4, 3], [80421001, 4, 3], [80431001, 4, 3]]),
        "props": None
    }),
    100118: _tools.RODict({
        "ID": 100118,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0028}),
        "equipment": _tools.ROList([[80411001, 5, 3], [80421001, 5, 3], [80431001, 5, 3]]),
        "props": None
    }),
    100119: _tools.RODict({
        "ID": 100119,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.003}),
        "equipment": _tools.ROList([[80411001, 6, 3], [80421001, 6, 3], [80431001, 6, 3]]),
        "props": None
    }),
    100120: _tools.RODict({
        "ID": 100120,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0032}),
        "equipment": _tools.ROList([[80411001, 7, 3], [80421001, 7, 3], [80431001, 7, 3]]),
        "props": None
    }),
    100121: _tools.RODict({
        "ID": 100121,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0022}),
        "equipment": _tools.ROList([[80411001, 0, 4], [80421001, 0, 4], [80431001, 0, 4]]),
        "props": None
    }),
    100122: _tools.RODict({
        "ID": 100122,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0024}),
        "equipment": _tools.ROList([[80411001, 1, 4], [80421001, 1, 4], [80431001, 1, 4]]),
        "props": None
    }),
    100123: _tools.RODict({
        "ID": 100123,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0026}),
        "equipment": _tools.ROList([[80411001, 2, 4], [80421001, 2, 4], [80431001, 2, 4]]),
        "props": None
    }),
    100124: _tools.RODict({
        "ID": 100124,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0028}),
        "equipment": _tools.ROList([[80411001, 3, 4], [80421001, 3, 4], [80431001, 3, 4]]),
        "props": None
    }),
    100125: _tools.RODict({
        "ID": 100125,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.003}),
        "equipment": _tools.ROList([[80411001, 4, 4], [80421001, 4, 4], [80431001, 4, 4]]),
        "props": None
    }),
    100126: _tools.RODict({
        "ID": 100126,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0032}),
        "equipment": _tools.ROList([[80411001, 5, 4], [80421001, 5, 4], [80431001, 5, 4]]),
        "props": None
    }),
    100127: _tools.RODict({
        "ID": 100127,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0034}),
        "equipment": _tools.ROList([[80411001, 6, 4], [80421001, 6, 4], [80431001, 6, 4]]),
        "props": None
    }),
    100128: _tools.RODict({
        "ID": 100128,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjPVPDmgAnti":0.0036}),
        "equipment": _tools.ROList([[80411001, 7, 4], [80421001, 7, 4], [80431001, 7, 4]]),
        "props": None
    }),
    100129: _tools.RODict({
        "ID": 100129,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.001}),
        "equipment": _tools.ROList([[80811001, 0, 1], [80821001, 0, 1], [80831001, 0, 1]]),
        "props": None
    }),
    100130: _tools.RODict({
        "ID": 100130,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0012}),
        "equipment": _tools.ROList([[80811001, 1, 1], [80821001, 1, 1], [80831001, 1, 1]]),
        "props": None
    }),
    100131: _tools.RODict({
        "ID": 100131,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0014}),
        "equipment": _tools.ROList([[80811001, 2, 1], [80821001, 2, 1], [80831001, 2, 1]]),
        "props": None
    }),
    100132: _tools.RODict({
        "ID": 100132,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0016}),
        "equipment": _tools.ROList([[80811001, 3, 1], [80821001, 3, 1], [80831001, 3, 1]]),
        "props": None
    }),
    100133: _tools.RODict({
        "ID": 100133,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0018}),
        "equipment": _tools.ROList([[80811001, 4, 1], [80821001, 4, 1], [80831001, 4, 1]]),
        "props": None
    }),
    100134: _tools.RODict({
        "ID": 100134,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.002}),
        "equipment": _tools.ROList([[80811001, 5, 1], [80821001, 5, 1], [80831001, 5, 1]]),
        "props": None
    }),
    100135: _tools.RODict({
        "ID": 100135,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0022}),
        "equipment": _tools.ROList([[80811001, 6, 1], [80821001, 6, 1], [80831001, 6, 1]]),
        "props": None
    }),
    100136: _tools.RODict({
        "ID": 100136,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0024}),
        "equipment": _tools.ROList([[80811001, 7, 1], [80821001, 7, 1], [80831001, 7, 1]]),
        "props": None
    }),
    100137: _tools.RODict({
        "ID": 100137,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0014}),
        "equipment": _tools.ROList([[80811001, 0, 2], [80821001, 0, 2], [80831001, 0, 2]]),
        "props": None
    }),
    100138: _tools.RODict({
        "ID": 100138,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0016}),
        "equipment": _tools.ROList([[80811001, 1, 2], [80821001, 1, 2], [80831001, 1, 2]]),
        "props": None
    }),
    100139: _tools.RODict({
        "ID": 100139,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0018}),
        "equipment": _tools.ROList([[80811001, 2, 2], [80821001, 2, 2], [80831001, 2, 2]]),
        "props": None
    }),
    100140: _tools.RODict({
        "ID": 100140,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.002}),
        "equipment": _tools.ROList([[80811001, 3, 2], [80821001, 3, 2], [80831001, 3, 2]]),
        "props": None
    }),
    100141: _tools.RODict({
        "ID": 100141,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0022}),
        "equipment": _tools.ROList([[80811001, 4, 2], [80821001, 4, 2], [80831001, 4, 2]]),
        "props": None
    }),
    100142: _tools.RODict({
        "ID": 100142,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0024}),
        "equipment": _tools.ROList([[80811001, 5, 2], [80821001, 5, 2], [80831001, 5, 2]]),
        "props": None
    }),
    100143: _tools.RODict({
        "ID": 100143,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0026}),
        "equipment": _tools.ROList([[80811001, 6, 2], [80821001, 6, 2], [80831001, 6, 2]]),
        "props": None
    }),
    100144: _tools.RODict({
        "ID": 100144,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0028}),
        "equipment": _tools.ROList([[80811001, 7, 2], [80821001, 7, 2], [80831001, 7, 2]]),
        "props": None
    }),
    100145: _tools.RODict({
        "ID": 100145,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0018}),
        "equipment": _tools.ROList([[80811001, 0, 3], [80821001, 0, 3], [80831001, 0, 3]]),
        "props": None
    }),
    100146: _tools.RODict({
        "ID": 100146,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.002}),
        "equipment": _tools.ROList([[80811001, 1, 3], [80821001, 1, 3], [80831001, 1, 3]]),
        "props": None
    }),
    100147: _tools.RODict({
        "ID": 100147,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0022}),
        "equipment": _tools.ROList([[80811001, 2, 3], [80821001, 2, 3], [80831001, 2, 3]]),
        "props": None
    }),
    100148: _tools.RODict({
        "ID": 100148,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0024}),
        "equipment": _tools.ROList([[80811001, 3, 3], [80821001, 3, 3], [80831001, 3, 3]]),
        "props": None
    }),
    100149: _tools.RODict({
        "ID": 100149,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0026}),
        "equipment": _tools.ROList([[80811001, 4, 3], [80821001, 4, 3], [80831001, 4, 3]]),
        "props": None
    }),
    100150: _tools.RODict({
        "ID": 100150,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0028}),
        "equipment": _tools.ROList([[80811001, 5, 3], [80821001, 5, 3], [80831001, 5, 3]]),
        "props": None
    }),
    100151: _tools.RODict({
        "ID": 100151,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.003}),
        "equipment": _tools.ROList([[80811001, 6, 3], [80821001, 6, 3], [80831001, 6, 3]]),
        "props": None
    }),
    100152: _tools.RODict({
        "ID": 100152,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0032}),
        "equipment": _tools.ROList([[80811001, 7, 3], [80821001, 7, 3], [80831001, 7, 3]]),
        "props": None
    }),
    100153: _tools.RODict({
        "ID": 100153,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0022}),
        "equipment": _tools.ROList([[80811001, 0, 4], [80821001, 0, 4], [80831001, 0, 4]]),
        "props": None
    }),
    100154: _tools.RODict({
        "ID": 100154,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0024}),
        "equipment": _tools.ROList([[80811001, 1, 4], [80821001, 1, 4], [80831001, 1, 4]]),
        "props": None
    }),
    100155: _tools.RODict({
        "ID": 100155,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0026}),
        "equipment": _tools.ROList([[80811001, 2, 4], [80821001, 2, 4], [80831001, 2, 4]]),
        "props": None
    }),
    100156: _tools.RODict({
        "ID": 100156,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0028}),
        "equipment": _tools.ROList([[80811001, 3, 4], [80821001, 3, 4], [80831001, 3, 4]]),
        "props": None
    }),
    100157: _tools.RODict({
        "ID": 100157,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.003}),
        "equipment": _tools.ROList([[80811001, 4, 4], [80821001, 4, 4], [80831001, 4, 4]]),
        "props": None
    }),
    100158: _tools.RODict({
        "ID": 100158,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0032}),
        "equipment": _tools.ROList([[80811001, 5, 4], [80821001, 5, 4], [80831001, 5, 4]]),
        "props": None
    }),
    100159: _tools.RODict({
        "ID": 100159,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0034}),
        "equipment": _tools.ROList([[80811001, 6, 4], [80821001, 6, 4], [80831001, 6, 4]]),
        "props": None
    }),
    100160: _tools.RODict({
        "ID": 100160,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmgAnti":0.0036}),
        "equipment": _tools.ROList([[80811001, 7, 4], [80821001, 7, 4], [80831001, 7, 4]]),
        "props": None
    }),
    100161: _tools.RODict({
        "ID": 100161,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmg":0.001}),
        "equipment": _tools.ROList([[80581001, 0, 1], [80591001, 0, 1]]),
        "props": None
    }),
    100162: _tools.RODict({
        "ID": 100162,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmg":0.0012}),
        "equipment": _tools.ROList([[80581001, 1, 1], [80591001, 1, 1]]),
        "props": None
    }),
    100163: _tools.RODict({
        "ID": 100163,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmg":0.0014}),
        "equipment": _tools.ROList([[80581001, 2, 1], [80591001, 2, 1]]),
        "props": None
    }),
    100164: _tools.RODict({
        "ID": 100164,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmg":0.0016}),
        "equipment": _tools.ROList([[80581001, 3, 1], [80591001, 3, 1]]),
        "props": None
    }),
    100165: _tools.RODict({
        "ID": 100165,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmg":0.0018}),
        "equipment": _tools.ROList([[80581001, 4, 1], [80591001, 4, 1]]),
        "props": None
    }),
    100166: _tools.RODict({
        "ID": 100166,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmg":0.002}),
        "equipment": _tools.ROList([[80581001, 5, 1], [80591001, 5, 1]]),
        "props": None
    }),
    100167: _tools.RODict({
        "ID": 100167,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmg":0.0022}),
        "equipment": _tools.ROList([[80581001, 6, 1], [80591001, 6, 1]]),
        "props": None
    }),
    100168: _tools.RODict({
        "ID": 100168,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmg":0.0024}),
        "equipment": _tools.ROList([[80581001, 7, 1], [80591001, 7, 1]]),
        "props": None
    }),
    100169: _tools.RODict({
        "ID": 100169,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmg":0.0014}),
        "equipment": _tools.ROList([[80581001, 0, 2], [80591001, 0, 2]]),
        "props": None
    }),
    100170: _tools.RODict({
        "ID": 100170,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmg":0.0016}),
        "equipment": _tools.ROList([[80581001, 1, 2], [80591001, 1, 2]]),
        "props": None
    }),
    100171: _tools.RODict({
        "ID": 100171,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmg":0.0018}),
        "equipment": _tools.ROList([[80581001, 2, 2], [80591001, 2, 2]]),
        "props": None
    }),
    100172: _tools.RODict({
        "ID": 100172,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmg":0.002}),
        "equipment": _tools.ROList([[80581001, 3, 2], [80591001, 3, 2]]),
        "props": None
    }),
    100173: _tools.RODict({
        "ID": 100173,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmg":0.0022}),
        "equipment": _tools.ROList([[80581001, 4, 2], [80591001, 4, 2]]),
        "props": None
    }),
    100174: _tools.RODict({
        "ID": 100174,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmg":0.0024}),
        "equipment": _tools.ROList([[80581001, 5, 2], [80591001, 5, 2]]),
        "props": None
    }),
    100175: _tools.RODict({
        "ID": 100175,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmg":0.0026}),
        "equipment": _tools.ROList([[80581001, 6, 2], [80591001, 6, 2]]),
        "props": None
    }),
    100176: _tools.RODict({
        "ID": 100176,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmg":0.0028}),
        "equipment": _tools.ROList([[80581001, 7, 2], [80591001, 7, 2]]),
        "props": None
    }),
    100177: _tools.RODict({
        "ID": 100177,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmg":0.0018}),
        "equipment": _tools.ROList([[80581001, 0, 3], [80591001, 0, 3]]),
        "props": None
    }),
    100178: _tools.RODict({
        "ID": 100178,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmg":0.002}),
        "equipment": _tools.ROList([[80581001, 1, 3], [80591001, 1, 3]]),
        "props": None
    }),
    100179: _tools.RODict({
        "ID": 100179,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmg":0.0022}),
        "equipment": _tools.ROList([[80581001, 2, 3], [80591001, 2, 3]]),
        "props": None
    }),
    100180: _tools.RODict({
        "ID": 100180,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmg":0.0024}),
        "equipment": _tools.ROList([[80581001, 3, 3], [80591001, 3, 3]]),
        "props": None
    }),
    100181: _tools.RODict({
        "ID": 100181,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmg":0.0026}),
        "equipment": _tools.ROList([[80581001, 4, 3], [80591001, 4, 3]]),
        "props": None
    }),
    100182: _tools.RODict({
        "ID": 100182,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmg":0.0028}),
        "equipment": _tools.ROList([[80581001, 5, 3], [80591001, 5, 3]]),
        "props": None
    }),
    100183: _tools.RODict({
        "ID": 100183,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmg":0.003}),
        "equipment": _tools.ROList([[80581001, 6, 3], [80591001, 6, 3]]),
        "props": None
    }),
    100184: _tools.RODict({
        "ID": 100184,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmg":0.0032}),
        "equipment": _tools.ROList([[80581001, 7, 3], [80591001, 7, 3]]),
        "props": None
    }),
    100185: _tools.RODict({
        "ID": 100185,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmg":0.0022}),
        "equipment": _tools.ROList([[80581001, 0, 4], [80591001, 0, 4]]),
        "props": None
    }),
    100186: _tools.RODict({
        "ID": 100186,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmg":0.0024}),
        "equipment": _tools.ROList([[80581001, 1, 4], [80591001, 1, 4]]),
        "props": None
    }),
    100187: _tools.RODict({
        "ID": 100187,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmg":0.0026}),
        "equipment": _tools.ROList([[80581001, 2, 4], [80591001, 2, 4]]),
        "props": None
    }),
    100188: _tools.RODict({
        "ID": 100188,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmg":0.0028}),
        "equipment": _tools.ROList([[80581001, 3, 4], [80591001, 3, 4]]),
        "props": None
    }),
    100189: _tools.RODict({
        "ID": 100189,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmg":0.003}),
        "equipment": _tools.ROList([[80581001, 4, 4], [80591001, 4, 4]]),
        "props": None
    }),
    100190: _tools.RODict({
        "ID": 100190,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmg":0.0032}),
        "equipment": _tools.ROList([[80581001, 5, 4], [80591001, 5, 4]]),
        "props": None
    }),
    100191: _tools.RODict({
        "ID": 100191,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmg":0.0034}),
        "equipment": _tools.ROList([[80581001, 6, 4], [80591001, 6, 4]]),
        "props": None
    }),
    100192: _tools.RODict({
        "ID": 100192,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMonsterDmg":0.0036}),
        "equipment": _tools.ROList([[80581001, 7, 4], [80591001, 7, 4]]),
        "props": None
    }),
    100193: _tools.RODict({
        "ID": 100193,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinMagicArmor":1}),
        "equipment": _tools.ROList([[80681001, 0, 1], [80691001, 0, 1]]),
        "props": None
    }),
    100194: _tools.RODict({
        "ID": 100194,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinMagicArmor":1}),
        "equipment": _tools.ROList([[80681001, 1, 1], [80691001, 1, 1]]),
        "props": None
    }),
    100195: _tools.RODict({
        "ID": 100195,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinMagicArmor":1}),
        "equipment": _tools.ROList([[80681001, 2, 1], [80691001, 2, 1]]),
        "props": None
    }),
    100196: _tools.RODict({
        "ID": 100196,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinMagicArmor":1}),
        "equipment": _tools.ROList([[80681001, 3, 1], [80691001, 3, 1]]),
        "props": None
    }),
    100197: _tools.RODict({
        "ID": 100197,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinMagicArmor":1}),
        "equipment": _tools.ROList([[80681001, 4, 1], [80691001, 4, 1]]),
        "props": None
    }),
    100198: _tools.RODict({
        "ID": 100198,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinMagicArmor":2}),
        "equipment": _tools.ROList([[80681001, 5, 1], [80691001, 5, 1]]),
        "props": None
    }),
    100199: _tools.RODict({
        "ID": 100199,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinMagicArmor":2}),
        "equipment": _tools.ROList([[80681001, 6, 1], [80691001, 6, 1]]),
        "props": None
    }),
    100200: _tools.RODict({
        "ID": 100200,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinMagicArmor":2}),
        "equipment": _tools.ROList([[80681001, 7, 1], [80691001, 7, 1]]),
        "props": None
    }),
    100201: _tools.RODict({
        "ID": 100201,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinMagicArmor":2}),
        "equipment": _tools.ROList([[80681001, 0, 2], [80691001, 0, 2]]),
        "props": None
    }),
    100202: _tools.RODict({
        "ID": 100202,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinMagicArmor":2}),
        "equipment": _tools.ROList([[80681001, 1, 2], [80691001, 1, 2]]),
        "props": None
    }),
    100203: _tools.RODict({
        "ID": 100203,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinMagicArmor":2}),
        "equipment": _tools.ROList([[80681001, 2, 2], [80691001, 2, 2]]),
        "props": None
    }),
    100204: _tools.RODict({
        "ID": 100204,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinMagicArmor":2}),
        "equipment": _tools.ROList([[80681001, 3, 2], [80691001, 3, 2]]),
        "props": None
    }),
    100205: _tools.RODict({
        "ID": 100205,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinMagicArmor":2}),
        "equipment": _tools.ROList([[80681001, 4, 2], [80691001, 4, 2]]),
        "props": None
    }),
    100206: _tools.RODict({
        "ID": 100206,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinMagicArmor":3}),
        "equipment": _tools.ROList([[80681001, 5, 2], [80691001, 5, 2]]),
        "props": None
    }),
    100207: _tools.RODict({
        "ID": 100207,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinMagicArmor":3}),
        "equipment": _tools.ROList([[80681001, 6, 2], [80691001, 6, 2]]),
        "props": None
    }),
    100208: _tools.RODict({
        "ID": 100208,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinMagicArmor":3}),
        "equipment": _tools.ROList([[80681001, 7, 2], [80691001, 7, 2]]),
        "props": None
    }),
    100209: _tools.RODict({
        "ID": 100209,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinMagicArmor":3}),
        "equipment": _tools.ROList([[80681001, 0, 3], [80691001, 0, 3]]),
        "props": None
    }),
    100210: _tools.RODict({
        "ID": 100210,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinMagicArmor":3}),
        "equipment": _tools.ROList([[80681001, 1, 3], [80691001, 1, 3]]),
        "props": None
    }),
    100211: _tools.RODict({
        "ID": 100211,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinMagicArmor":3}),
        "equipment": _tools.ROList([[80681001, 2, 3], [80691001, 2, 3]]),
        "props": None
    }),
    100212: _tools.RODict({
        "ID": 100212,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinMagicArmor":3}),
        "equipment": _tools.ROList([[80681001, 3, 3], [80691001, 3, 3]]),
        "props": None
    }),
    100213: _tools.RODict({
        "ID": 100213,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinMagicArmor":3}),
        "equipment": _tools.ROList([[80681001, 4, 3], [80691001, 4, 3]]),
        "props": None
    }),
    100214: _tools.RODict({
        "ID": 100214,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinMagicArmor":4}),
        "equipment": _tools.ROList([[80681001, 5, 3], [80691001, 5, 3]]),
        "props": None
    }),
    100215: _tools.RODict({
        "ID": 100215,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinMagicArmor":4}),
        "equipment": _tools.ROList([[80681001, 6, 3], [80691001, 6, 3]]),
        "props": None
    }),
    100216: _tools.RODict({
        "ID": 100216,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinMagicArmor":4}),
        "equipment": _tools.ROList([[80681001, 7, 3], [80691001, 7, 3]]),
        "props": None
    }),
    100217: _tools.RODict({
        "ID": 100217,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinMagicArmor":4}),
        "equipment": _tools.ROList([[80681001, 0, 4], [80691001, 0, 4]]),
        "props": None
    }),
    100218: _tools.RODict({
        "ID": 100218,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinMagicArmor":4}),
        "equipment": _tools.ROList([[80681001, 1, 4], [80691001, 1, 4]]),
        "props": None
    }),
    100219: _tools.RODict({
        "ID": 100219,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinMagicArmor":4}),
        "equipment": _tools.ROList([[80681001, 2, 4], [80691001, 2, 4]]),
        "props": None
    }),
    100220: _tools.RODict({
        "ID": 100220,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinMagicArmor":4}),
        "equipment": _tools.ROList([[80681001, 3, 4], [80691001, 3, 4]]),
        "props": None
    }),
    100221: _tools.RODict({
        "ID": 100221,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinMagicArmor":4}),
        "equipment": _tools.ROList([[80681001, 4, 4], [80691001, 4, 4]]),
        "props": None
    }),
    100222: _tools.RODict({
        "ID": 100222,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinMagicArmor":5}),
        "equipment": _tools.ROList([[80681001, 5, 4], [80691001, 5, 4]]),
        "props": None
    }),
    100223: _tools.RODict({
        "ID": 100223,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinMagicArmor":5}),
        "equipment": _tools.ROList([[80681001, 6, 4], [80691001, 6, 4]]),
        "props": None
    }),
    100224: _tools.RODict({
        "ID": 100224,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinMagicArmor":5}),
        "equipment": _tools.ROList([[80681001, 7, 4], [80691001, 7, 4]]),
        "props": None
    }),
    100225: _tools.RODict({
        "ID": 100225,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinPhysicalArmor":1}),
        "equipment": _tools.ROList([[80781001, 0, 1], [80791001, 0, 1]]),
        "props": None
    }),
    100226: _tools.RODict({
        "ID": 100226,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinPhysicalArmor":1}),
        "equipment": _tools.ROList([[80781001, 1, 1], [80791001, 1, 1]]),
        "props": None
    }),
    100227: _tools.RODict({
        "ID": 100227,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinPhysicalArmor":1}),
        "equipment": _tools.ROList([[80781001, 2, 1], [80791001, 2, 1]]),
        "props": None
    }),
    100228: _tools.RODict({
        "ID": 100228,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinPhysicalArmor":1}),
        "equipment": _tools.ROList([[80781001, 3, 1], [80791001, 3, 1]]),
        "props": None
    }),
    100229: _tools.RODict({
        "ID": 100229,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinPhysicalArmor":1}),
        "equipment": _tools.ROList([[80781001, 4, 1], [80791001, 4, 1]]),
        "props": None
    }),
    100230: _tools.RODict({
        "ID": 100230,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinPhysicalArmor":2}),
        "equipment": _tools.ROList([[80781001, 5, 1], [80791001, 5, 1]]),
        "props": None
    }),
    100231: _tools.RODict({
        "ID": 100231,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinPhysicalArmor":2}),
        "equipment": _tools.ROList([[80781001, 6, 1], [80791001, 6, 1]]),
        "props": None
    }),
    100232: _tools.RODict({
        "ID": 100232,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinPhysicalArmor":2}),
        "equipment": _tools.ROList([[80781001, 7, 1], [80791001, 7, 1]]),
        "props": None
    }),
    100233: _tools.RODict({
        "ID": 100233,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinPhysicalArmor":2}),
        "equipment": _tools.ROList([[80781001, 0, 2], [80791001, 0, 2]]),
        "props": None
    }),
    100234: _tools.RODict({
        "ID": 100234,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinPhysicalArmor":2}),
        "equipment": _tools.ROList([[80781001, 1, 2], [80791001, 1, 2]]),
        "props": None
    }),
    100235: _tools.RODict({
        "ID": 100235,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinPhysicalArmor":2}),
        "equipment": _tools.ROList([[80781001, 2, 2], [80791001, 2, 2]]),
        "props": None
    }),
    100236: _tools.RODict({
        "ID": 100236,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinPhysicalArmor":2}),
        "equipment": _tools.ROList([[80781001, 3, 2], [80791001, 3, 2]]),
        "props": None
    }),
    100237: _tools.RODict({
        "ID": 100237,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinPhysicalArmor":2}),
        "equipment": _tools.ROList([[80781001, 4, 2], [80791001, 4, 2]]),
        "props": None
    }),
    100238: _tools.RODict({
        "ID": 100238,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinPhysicalArmor":3}),
        "equipment": _tools.ROList([[80781001, 5, 2], [80791001, 5, 2]]),
        "props": None
    }),
    100239: _tools.RODict({
        "ID": 100239,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinPhysicalArmor":3}),
        "equipment": _tools.ROList([[80781001, 6, 2], [80791001, 6, 2]]),
        "props": None
    }),
    100240: _tools.RODict({
        "ID": 100240,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinPhysicalArmor":3}),
        "equipment": _tools.ROList([[80781001, 7, 2], [80791001, 7, 2]]),
        "props": None
    }),
    100241: _tools.RODict({
        "ID": 100241,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinPhysicalArmor":3}),
        "equipment": _tools.ROList([[80781001, 0, 3], [80791001, 0, 3]]),
        "props": None
    }),
    100242: _tools.RODict({
        "ID": 100242,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinPhysicalArmor":3}),
        "equipment": _tools.ROList([[80781001, 1, 3], [80791001, 1, 3]]),
        "props": None
    }),
    100243: _tools.RODict({
        "ID": 100243,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinPhysicalArmor":3}),
        "equipment": _tools.ROList([[80781001, 2, 3], [80791001, 2, 3]]),
        "props": None
    }),
    100244: _tools.RODict({
        "ID": 100244,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinPhysicalArmor":3}),
        "equipment": _tools.ROList([[80781001, 3, 3], [80791001, 3, 3]]),
        "props": None
    }),
    100245: _tools.RODict({
        "ID": 100245,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinPhysicalArmor":3}),
        "equipment": _tools.ROList([[80781001, 4, 3], [80791001, 4, 3]]),
        "props": None
    }),
    100246: _tools.RODict({
        "ID": 100246,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinPhysicalArmor":4}),
        "equipment": _tools.ROList([[80781001, 5, 3], [80791001, 5, 3]]),
        "props": None
    }),
    100247: _tools.RODict({
        "ID": 100247,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinPhysicalArmor":4}),
        "equipment": _tools.ROList([[80781001, 6, 3], [80791001, 6, 3]]),
        "props": None
    }),
    100248: _tools.RODict({
        "ID": 100248,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinPhysicalArmor":4}),
        "equipment": _tools.ROList([[80781001, 7, 3], [80791001, 7, 3]]),
        "props": None
    }),
    100249: _tools.RODict({
        "ID": 100249,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinPhysicalArmor":4}),
        "equipment": _tools.ROList([[80781001, 0, 4], [80791001, 0, 4]]),
        "props": None
    }),
    100250: _tools.RODict({
        "ID": 100250,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinPhysicalArmor":4}),
        "equipment": _tools.ROList([[80781001, 1, 4], [80791001, 1, 4]]),
        "props": None
    }),
    100251: _tools.RODict({
        "ID": 100251,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinPhysicalArmor":4}),
        "equipment": _tools.ROList([[80781001, 2, 4], [80791001, 2, 4]]),
        "props": None
    }),
    100252: _tools.RODict({
        "ID": 100252,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinPhysicalArmor":4}),
        "equipment": _tools.ROList([[80781001, 3, 4], [80791001, 3, 4]]),
        "props": None
    }),
    100253: _tools.RODict({
        "ID": 100253,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinPhysicalArmor":4}),
        "equipment": _tools.ROList([[80781001, 4, 4], [80791001, 4, 4]]),
        "props": None
    }),
    100254: _tools.RODict({
        "ID": 100254,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinPhysicalArmor":5}),
        "equipment": _tools.ROList([[80781001, 5, 4], [80791001, 5, 4]]),
        "props": None
    }),
    100255: _tools.RODict({
        "ID": 100255,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinPhysicalArmor":5}),
        "equipment": _tools.ROList([[80781001, 6, 4], [80791001, 6, 4]]),
        "props": None
    }),
    100256: _tools.RODict({
        "ID": 100256,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjMinPhysicalArmor":5}),
        "equipment": _tools.ROList([[80781001, 7, 4], [80791001, 7, 4]]),
        "props": None
    }),
    100257: _tools.RODict({
        "ID": 100257,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":1}),
        "equipment": _tools.ROList([[80111001, 0, 1], [80121001, 0, 1], [80131001, 0, 1]]),
        "props": None
    }),
    100258: _tools.RODict({
        "ID": 100258,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":1}),
        "equipment": _tools.ROList([[80111001, 1, 1], [80121001, 1, 1], [80131001, 1, 1]]),
        "props": None
    }),
    100259: _tools.RODict({
        "ID": 100259,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":2}),
        "equipment": _tools.ROList([[80111001, 2, 1], [80121001, 2, 1], [80131001, 2, 1]]),
        "props": None
    }),
    100260: _tools.RODict({
        "ID": 100260,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":2}),
        "equipment": _tools.ROList([[80111001, 3, 1], [80121001, 3, 1], [80131001, 3, 1]]),
        "props": None
    }),
    100261: _tools.RODict({
        "ID": 100261,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":3}),
        "equipment": _tools.ROList([[80111001, 4, 1], [80121001, 4, 1], [80131001, 4, 1]]),
        "props": None
    }),
    100262: _tools.RODict({
        "ID": 100262,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":3}),
        "equipment": _tools.ROList([[80111001, 5, 1], [80121001, 5, 1], [80131001, 5, 1]]),
        "props": None
    }),
    100263: _tools.RODict({
        "ID": 100263,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":4}),
        "equipment": _tools.ROList([[80111001, 6, 1], [80121001, 6, 1], [80131001, 6, 1]]),
        "props": None
    }),
    100264: _tools.RODict({
        "ID": 100264,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":4}),
        "equipment": _tools.ROList([[80111001, 7, 1], [80121001, 7, 1], [80131001, 7, 1]]),
        "props": None
    }),
    100265: _tools.RODict({
        "ID": 100265,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":2}),
        "equipment": _tools.ROList([[80111001, 0, 2], [80121001, 0, 2], [80131001, 0, 2]]),
        "props": None
    }),
    100266: _tools.RODict({
        "ID": 100266,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":2}),
        "equipment": _tools.ROList([[80111001, 1, 2], [80121001, 1, 2], [80131001, 1, 2]]),
        "props": None
    }),
    100267: _tools.RODict({
        "ID": 100267,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":3}),
        "equipment": _tools.ROList([[80111001, 2, 2], [80121001, 2, 2], [80131001, 2, 2]]),
        "props": None
    }),
    100268: _tools.RODict({
        "ID": 100268,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":3}),
        "equipment": _tools.ROList([[80111001, 3, 2], [80121001, 3, 2], [80131001, 3, 2]]),
        "props": None
    }),
    100269: _tools.RODict({
        "ID": 100269,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":4}),
        "equipment": _tools.ROList([[80111001, 4, 2], [80121001, 4, 2], [80131001, 4, 2]]),
        "props": None
    }),
    100270: _tools.RODict({
        "ID": 100270,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":4}),
        "equipment": _tools.ROList([[80111001, 5, 2], [80121001, 5, 2], [80131001, 5, 2]]),
        "props": None
    }),
    100271: _tools.RODict({
        "ID": 100271,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":5}),
        "equipment": _tools.ROList([[80111001, 6, 2], [80121001, 6, 2], [80131001, 6, 2]]),
        "props": None
    }),
    100272: _tools.RODict({
        "ID": 100272,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":5}),
        "equipment": _tools.ROList([[80111001, 7, 2], [80121001, 7, 2], [80131001, 7, 2]]),
        "props": None
    }),
    100273: _tools.RODict({
        "ID": 100273,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":3}),
        "equipment": _tools.ROList([[80111001, 0, 3], [80121001, 0, 3], [80131001, 0, 3]]),
        "props": None
    }),
    100274: _tools.RODict({
        "ID": 100274,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":3}),
        "equipment": _tools.ROList([[80111001, 1, 3], [80121001, 1, 3], [80131001, 1, 3]]),
        "props": None
    }),
    100275: _tools.RODict({
        "ID": 100275,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":4}),
        "equipment": _tools.ROList([[80111001, 2, 3], [80121001, 2, 3], [80131001, 2, 3]]),
        "props": None
    }),
    100276: _tools.RODict({
        "ID": 100276,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":4}),
        "equipment": _tools.ROList([[80111001, 3, 3], [80121001, 3, 3], [80131001, 3, 3]]),
        "props": None
    }),
    100277: _tools.RODict({
        "ID": 100277,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":5}),
        "equipment": _tools.ROList([[80111001, 4, 3], [80121001, 4, 3], [80131001, 4, 3]]),
        "props": None
    }),
    100278: _tools.RODict({
        "ID": 100278,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":5}),
        "equipment": _tools.ROList([[80111001, 5, 3], [80121001, 5, 3], [80131001, 5, 3]]),
        "props": None
    }),
    100279: _tools.RODict({
        "ID": 100279,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":6}),
        "equipment": _tools.ROList([[80111001, 6, 3], [80121001, 6, 3], [80131001, 6, 3]]),
        "props": None
    }),
    100280: _tools.RODict({
        "ID": 100280,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":6}),
        "equipment": _tools.ROList([[80111001, 7, 3], [80121001, 7, 3], [80131001, 7, 3]]),
        "props": None
    }),
    100281: _tools.RODict({
        "ID": 100281,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":4}),
        "equipment": _tools.ROList([[80111001, 0, 4], [80121001, 0, 4], [80131001, 0, 4]]),
        "props": None
    }),
    100282: _tools.RODict({
        "ID": 100282,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":4}),
        "equipment": _tools.ROList([[80111001, 1, 4], [80121001, 1, 4], [80131001, 1, 4]]),
        "props": None
    }),
    100283: _tools.RODict({
        "ID": 100283,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":5}),
        "equipment": _tools.ROList([[80111001, 2, 4], [80121001, 2, 4], [80131001, 2, 4]]),
        "props": None
    }),
    100284: _tools.RODict({
        "ID": 100284,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":5}),
        "equipment": _tools.ROList([[80111001, 3, 4], [80121001, 3, 4], [80131001, 3, 4]]),
        "props": None
    }),
    100285: _tools.RODict({
        "ID": 100285,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":6}),
        "equipment": _tools.ROList([[80111001, 4, 4], [80121001, 4, 4], [80131001, 4, 4]]),
        "props": None
    }),
    100286: _tools.RODict({
        "ID": 100286,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":6}),
        "equipment": _tools.ROList([[80111001, 5, 4], [80121001, 5, 4], [80131001, 5, 4]]),
        "props": None
    }),
    100287: _tools.RODict({
        "ID": 100287,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":7}),
        "equipment": _tools.ROList([[80111001, 6, 4], [80121001, 6, 4], [80131001, 6, 4]]),
        "props": None
    }),
    100288: _tools.RODict({
        "ID": 100288,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52014262,
        "propList": _tools.RODict({"adjMaxPhysicalAtk":7}),
        "equipment": _tools.ROList([[80111001, 7, 4], [80121001, 7, 4], [80131001, 7, 4]]),
        "props": None
    }),
    100289: _tools.RODict({
        "ID": 100289,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjCopper":0.02}),
        "equipment": None,
        "props": _tools.ROList([30001001, 30001002, 30001003, 30001004, 30001005])
    }),
    100290: _tools.RODict({
        "ID": 100290,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjCopper":0.02}),
        "equipment": None,
        "props": _tools.ROList([30001006, 30001007, 30001008, 30001009, 30001010])
    }),
    100291: _tools.RODict({
        "ID": 100291,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjCopper":0.02}),
        "equipment": None,
        "props": _tools.ROList([30001001, 30001002, 30001003, 30001004])
    }),
    100292: _tools.RODict({
        "ID": 100292,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjCopper":0.02}),
        "equipment": None,
        "props": _tools.ROList([30001003, 30001004, 30001005, 30001006])
    }),
    100293: _tools.RODict({
        "ID": 100293,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjCopper":0.02}),
        "equipment": None,
        "props": _tools.ROList([30001005, 30001006, 30001007, 30001008])
    }),
    100294: _tools.RODict({
        "ID": 100294,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjCopper":0.02}),
        "equipment": None,
        "props": _tools.ROList([30001007, 30001008, 30001009, 30001010])
    }),
    100295: _tools.RODict({
        "ID": 100295,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjCopper":0.02}),
        "equipment": None,
        "props": _tools.ROList([30001001, 30001008, 30001009, 30001010])
    }),
    100296: _tools.RODict({
        "ID": 100296,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjIgnoreArmor":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001011, 30001012, 30001013, 30001014, 30001015])
    }),
    100297: _tools.RODict({
        "ID": 100297,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjDmgArmor":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001016, 30001017, 30001018, 30001019, 30001020])
    }),
    100298: _tools.RODict({
        "ID": 100298,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjIgnoreArmor":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001011, 30001012, 30001013, 30001014])
    }),
    100299: _tools.RODict({
        "ID": 100299,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjDmgArmor":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001013, 30001014, 30001015, 30001016])
    }),
    100300: _tools.RODict({
        "ID": 100300,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjIgnoreArmor":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001015, 30001016, 30001017, 30001018])
    }),
    100301: _tools.RODict({
        "ID": 100301,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjDmgArmor":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001017, 30001018, 30001019, 30001020])
    }),
    100302: _tools.RODict({
        "ID": 100302,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjFullMp":24}),
        "equipment": None,
        "props": _tools.ROList([30001011, 30001012, 30001019, 30001020])
    }),
    100303: _tools.RODict({
        "ID": 100303,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjCopper":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001001, 30001002, 30001003])
    }),
    100304: _tools.RODict({
        "ID": 100304,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjCopper":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001002, 30001003, 30001004])
    }),
    100305: _tools.RODict({
        "ID": 100305,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjCopper":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001003, 30001004, 30001005])
    }),
    100306: _tools.RODict({
        "ID": 100306,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjCopper":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001004, 30001005, 30001006])
    }),
    100307: _tools.RODict({
        "ID": 100307,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjCopper":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001005, 30001006, 30001007])
    }),
    100308: _tools.RODict({
        "ID": 100308,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjCopper":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001006, 30001007, 30001008])
    }),
    100309: _tools.RODict({
        "ID": 100309,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjCopper":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001007, 30001008, 30001009])
    }),
    100310: _tools.RODict({
        "ID": 100310,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjCopper":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001008, 30001009, 30001010])
    }),
    100311: _tools.RODict({
        "ID": 100311,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjCopper":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001011, 30001012, 30001001])
    }),
    100312: _tools.RODict({
        "ID": 100312,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjCopper":0.03}),
        "equipment": None,
        "props": _tools.ROList([30001004, 30001001, 30001014, 30001011])
    }),
    100313: _tools.RODict({
        "ID": 100313,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjCopper":0.03}),
        "equipment": None,
        "props": _tools.ROList([30001005, 30001002, 30001015, 30001012])
    }),
    100314: _tools.RODict({
        "ID": 100314,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjCopper":0.03}),
        "equipment": None,
        "props": _tools.ROList([30001006, 30001003, 30001016, 30001013])
    }),
    100315: _tools.RODict({
        "ID": 100315,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjCopper":0.03}),
        "equipment": None,
        "props": _tools.ROList([30001007, 30001004, 30001017, 30001014])
    }),
    100316: _tools.RODict({
        "ID": 100316,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjCopper":0.03}),
        "equipment": None,
        "props": _tools.ROList([30001008, 30001005, 30001018, 30001015])
    }),
    100317: _tools.RODict({
        "ID": 100317,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjExpGrow":0.01}),
        "equipment": None,
        "props": _tools.ROList([30003008, 30003010, 30003012, 30003013])
    }),
    100318: _tools.RODict({
        "ID": 100318,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjExpGrow":0.01}),
        "equipment": None,
        "props": _tools.ROList([30003007, 30003009, 30003011])
    }),
    100319: _tools.RODict({
        "ID": 100319,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjExpGrow":0.01}),
        "equipment": None,
        "props": _tools.ROList([30003002, 30003004, 30003006])
    }),
    100320: _tools.RODict({
        "ID": 100320,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjExpGrow":0.01}),
        "equipment": None,
        "props": _tools.ROList([30003001, 30003003, 30003005])
    }),
    100321: _tools.RODict({
        "ID": 100321,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjExpGrow":0.01}),
        "equipment": None,
        "props": _tools.ROList([30003001, 30003002, 30003003, 30003004])
    }),
    100322: _tools.RODict({
        "ID": 100322,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjExpGrow":0.01}),
        "equipment": None,
        "props": _tools.ROList([30003005, 30003006, 30003007, 30003008])
    }),
    100323: _tools.RODict({
        "ID": 100323,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjExpGrow":0.01}),
        "equipment": None,
        "props": _tools.ROList([30003009, 30003010, 30003011, 30003012, 30003013])
    }),
    100324: _tools.RODict({
        "ID": 100324,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjExpGrow":0.02}),
        "equipment": None,
        "props": _tools.ROList([30003014, 30003015, 30003016, 30003017])
    }),
    100325: _tools.RODict({
        "ID": 100325,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjExpGrow":0.02}),
        "equipment": None,
        "props": _tools.ROList([30003018, 30003019, 30003020, 30003021])
    }),
    100326: _tools.RODict({
        "ID": 100326,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjExpGrow":0.02}),
        "equipment": None,
        "props": _tools.ROList([30003022, 30003023, 30003024, 30003025])
    }),
    100327: _tools.RODict({
        "ID": 100327,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjExpGrow":0.02}),
        "equipment": None,
        "props": _tools.ROList([30003026, 30003027, 30003028, 30003029, 30003030])
    }),
    100328: _tools.RODict({
        "ID": 100328,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjExpGrow":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001001, 30001002, 30003001, 30003002, 30003011])
    }),
    100329: _tools.RODict({
        "ID": 100329,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjExpGrow":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001003, 30001004, 30003003, 30003004, 30003012])
    }),
    100330: _tools.RODict({
        "ID": 100330,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjExpGrow":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001005, 30001006, 30003005, 30003006, 30003013])
    }),
    100331: _tools.RODict({
        "ID": 100331,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjExpGrow":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001007, 30001008, 30003007, 30003008])
    }),
    100332: _tools.RODict({
        "ID": 100332,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjExpGrow":0.01}),
        "equipment": None,
        "props": _tools.ROList([30001009, 30001010, 30003009, 30003010])
    }),
    100333: _tools.RODict({
        "ID": 100333,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjExpGrow":0.02}),
        "equipment": None,
        "props": _tools.ROList([30001011, 30001012, 30003014, 30003015, 30003024, 30003029])
    }),
    100334: _tools.RODict({
        "ID": 100334,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjExpGrow":0.03}),
        "equipment": None,
        "props": _tools.ROList([30001013, 30001014, 30003016, 30003017, 30003025, 30003030])
    }),
    100335: _tools.RODict({
        "ID": 100335,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjExpGrow":0.02}),
        "equipment": None,
        "props": _tools.ROList([30001015, 30001016, 30003018, 30003019, 30003026])
    }),
    100336: _tools.RODict({
        "ID": 100336,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjExpGrow":0.02}),
        "equipment": None,
        "props": _tools.ROList([30001017, 30001018, 30003020, 30003021, 30003027])
    }),
    100337: _tools.RODict({
        "ID": 100337,
        "unavailableClass": None,
        "prop": 52014262,
        "propList": _tools.RODict({"adjCopper":0.02}),
        "equipment": None,
        "props": _tools.ROList([30001019, 30001020, 30003022, 30003023, 30003027])
    })
})
minKey = 100001
maxKey = 100337