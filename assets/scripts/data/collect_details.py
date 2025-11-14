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
        "unavailableClass": None,
        "prop": 52003181,
        "equipment": _tools.ROList([[80111001, 0, 1], [80121001, 0, 1], [80131001, 0, 1]]),
        "props": None
    }),
    100002: _tools.RODict({
        "ID": 100002,
        "unavailableClass": None,
        "prop": 52003185,
        "equipment": _tools.ROList([[80211001, 0, 1], [80221001, 0, 1], [80231001, 0, 1]]),
        "props": None
    }),
    100003: _tools.RODict({
        "ID": 100003,
        "unavailableClass": None,
        "prop": 52003189,
        "equipment": _tools.ROList([[80311001, 0, 1], [80321001, 0, 1], [80331001, 0, 1]]),
        "props": None
    }),
    100004: _tools.RODict({
        "ID": 100004,
        "unavailableClass": None,
        "prop": 52003193,
        "equipment": _tools.ROList([[80411001, 0, 1], [80421001, 0, 1], [80431001, 0, 1]]),
        "props": None
    }),
    100005: _tools.RODict({
        "ID": 100005,
        "unavailableClass": None,
        "prop": 52003197,
        "equipment": _tools.ROList([[80581001, 0, 1]]),
        "props": _tools.ROList([30000287, 30000288, 30000289])
    }),
    100006: _tools.RODict({
        "ID": 100006,
        "unavailableClass": None,
        "prop": 52003201,
        "equipment": _tools.ROList([[80111001, 0, 2], [80121001, 0, 2], [80131001, 0, 2]]),
        "props": None
    }),
    100007: _tools.RODict({
        "ID": 100007,
        "unavailableClass": None,
        "prop": 52003205,
        "equipment": _tools.ROList([[80211001, 0, 2], [80221001, 0, 2], [80231001, 0, 2]]),
        "props": None
    }),
    100008: _tools.RODict({
        "ID": 100008,
        "unavailableClass": None,
        "prop": 52003209,
        "equipment": _tools.ROList([[80311001, 0, 2], [80321001, 0, 2], [80331001, 0, 2]]),
        "props": None
    }),
    100009: _tools.RODict({
        "ID": 100009,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003211,
        "equipment": _tools.ROList([[80411001, 0, 2], [80421001, 0, 2], [80431001, 0, 2]]),
        "props": None
    }),
    100010: _tools.RODict({
        "ID": 100010,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003212,
        "equipment": _tools.ROList([[80581001, 0, 2]]),
        "props": _tools.ROList([30000287, 30000288, 30000289])
    }),
    100011: _tools.RODict({
        "ID": 100011,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003213,
        "equipment": _tools.ROList([[80111001, 0, 3], [80121001, 0, 3], [80131001, 0, 3]]),
        "props": None
    }),
    100012: _tools.RODict({
        "ID": 100012,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003214,
        "equipment": _tools.ROList([[80211001, 0, 3], [80221001, 0, 3], [80231001, 0, 3]]),
        "props": None
    }),
    100013: _tools.RODict({
        "ID": 100013,
        "unavailableClass": None,
        "prop": 52003215,
        "equipment": _tools.ROList([[80311001, 0, 3], [80321001, 0, 3], [80331001, 0, 3]]),
        "props": None
    }),
    100014: _tools.RODict({
        "ID": 100014,
        "unavailableClass": None,
        "prop": 52003216,
        "equipment": _tools.ROList([[80411001, 0, 3], [80421001, 0, 3], [80431001, 0, 3]]),
        "props": None
    }),
    100015: _tools.RODict({
        "ID": 100015,
        "unavailableClass": None,
        "prop": 52003218,
        "equipment": _tools.ROList([[80581001, 0, 3]]),
        "props": _tools.ROList([30000287, 30000288, 30000289])
    }),
    100016: _tools.RODict({
        "ID": 100016,
        "unavailableClass": None,
        "prop": 52003181,
        "equipment": _tools.ROList([[80112001, 0, 1], [80122001, 0, 1], [80132001, 0, 1]]),
        "props": None
    }),
    100017: _tools.RODict({
        "ID": 100017,
        "unavailableClass": None,
        "prop": 52003185,
        "equipment": _tools.ROList([[80212001, 0, 1], [80222001, 0, 1], [80232001, 0, 1]]),
        "props": None
    }),
    100018: _tools.RODict({
        "ID": 100018,
        "unavailableClass": None,
        "prop": 52003189,
        "equipment": _tools.ROList([[80312001, 0, 1], [80322001, 0, 1], [80332001, 0, 1]]),
        "props": None
    }),
    100019: _tools.RODict({
        "ID": 100019,
        "unavailableClass": None,
        "prop": 52003193,
        "equipment": _tools.ROList([[80412001, 0, 1], [80422001, 0, 1], [80432001, 0, 1]]),
        "props": None
    }),
    100020: _tools.RODict({
        "ID": 100020,
        "unavailableClass": None,
        "prop": 52003197,
        "equipment": _tools.ROList([[80582001, 0, 1]]),
        "props": _tools.ROList([30000290, 30000291, 30000292])
    }),
    100021: _tools.RODict({
        "ID": 100021,
        "unavailableClass": None,
        "prop": 52003201,
        "equipment": _tools.ROList([[80682001, 0, 1], [80782001, 0, 1]]),
        "props": None
    }),
    100022: _tools.RODict({
        "ID": 100022,
        "unavailableClass": None,
        "prop": 52003205,
        "equipment": _tools.ROList([[80692001, 0, 1], [80794001, 0, 1]]),
        "props": None
    }),
    100023: _tools.RODict({
        "ID": 100023,
        "unavailableClass": None,
        "prop": 52003209,
        "equipment": None,
        "props": _tools.ROList([30990121, 30990126, 30990127])
    }),
    100024: _tools.RODict({
        "ID": 100024,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003211,
        "equipment": None,
        "props": _tools.ROList([30990122, 30990123, 30990124, 30990125])
    }),
    100025: _tools.RODict({
        "ID": 100025,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003212,
        "equipment": _tools.ROList([[80112001, 1, 2], [80122001, 1, 2], [80132001, 1, 2]]),
        "props": None
    }),
    100026: _tools.RODict({
        "ID": 100026,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003213,
        "equipment": _tools.ROList([[80212001, 1, 2], [80222001, 1, 2], [80232001, 1, 2]]),
        "props": None
    }),
    100027: _tools.RODict({
        "ID": 100027,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003214,
        "equipment": _tools.ROList([[80312001, 1, 2], [80322001, 1, 2], [80332001, 1, 2]]),
        "props": None
    }),
    100028: _tools.RODict({
        "ID": 100028,
        "unavailableClass": None,
        "prop": 52003215,
        "equipment": _tools.ROList([[80412001, 1, 2], [80422001, 1, 2], [80432001, 1, 2]]),
        "props": None
    }),
    100029: _tools.RODict({
        "ID": 100029,
        "unavailableClass": None,
        "prop": 52003216,
        "equipment": _tools.ROList([[80582001, 1, 2]]),
        "props": _tools.ROList([30000290, 30000291, 30000292])
    }),
    100030: _tools.RODict({
        "ID": 100030,
        "unavailableClass": None,
        "prop": 52003218,
        "equipment": _tools.ROList([[80682001, 1, 2], [80782001, 1, 2]]),
        "props": None
    }),
    100031: _tools.RODict({
        "ID": 100031,
        "unavailableClass": None,
        "prop": 52003181,
        "equipment": _tools.ROList([[80692001, 1, 2], [80794001, 1, 2]]),
        "props": None
    }),
    100032: _tools.RODict({
        "ID": 100032,
        "unavailableClass": None,
        "prop": 52003185,
        "equipment": _tools.ROList([[80112001, 1, 3], [80122001, 1, 3], [80132001, 1, 3]]),
        "props": None
    }),
    100033: _tools.RODict({
        "ID": 100033,
        "unavailableClass": None,
        "prop": 52003189,
        "equipment": _tools.ROList([[80212001, 1, 3], [80222001, 1, 3], [80232001, 1, 3]]),
        "props": None
    }),
    100034: _tools.RODict({
        "ID": 100034,
        "unavailableClass": None,
        "prop": 52003193,
        "equipment": _tools.ROList([[80312001, 1, 3], [80322001, 1, 3], [80332001, 1, 3]]),
        "props": None
    }),
    100035: _tools.RODict({
        "ID": 100035,
        "unavailableClass": None,
        "prop": 52003197,
        "equipment": _tools.ROList([[80412001, 1, 3], [80422001, 1, 3], [80432001, 1, 3]]),
        "props": None
    }),
    100036: _tools.RODict({
        "ID": 100036,
        "unavailableClass": None,
        "prop": 52003201,
        "equipment": _tools.ROList([[80582001, 1, 3]]),
        "props": _tools.ROList([30000290, 30000291, 30000292])
    }),
    100037: _tools.RODict({
        "ID": 100037,
        "unavailableClass": None,
        "prop": 52003205,
        "equipment": _tools.ROList([[80682001, 1, 3], [80782001, 1, 3]]),
        "props": None
    }),
    100038: _tools.RODict({
        "ID": 100038,
        "unavailableClass": None,
        "prop": 52003209,
        "equipment": _tools.ROList([[80692001, 1, 3], [80794001, 1, 3]]),
        "props": None
    }),
    100039: _tools.RODict({
        "ID": 100039,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003211,
        "equipment": _tools.ROList([[80112001, 2, 4], [80122001, 2, 4], [80132001, 2, 4]]),
        "props": None
    }),
    100040: _tools.RODict({
        "ID": 100040,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003212,
        "equipment": _tools.ROList([[80212001, 2, 4], [80222001, 2, 4], [80232001, 2, 4]]),
        "props": None
    }),
    100041: _tools.RODict({
        "ID": 100041,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003213,
        "equipment": _tools.ROList([[80312001, 2, 4], [80322001, 2, 4], [80332001, 2, 4]]),
        "props": None
    }),
    100042: _tools.RODict({
        "ID": 100042,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003214,
        "equipment": _tools.ROList([[80412001, 2, 4], [80422001, 2, 4], [80432001, 2, 4]]),
        "props": None
    }),
    100043: _tools.RODict({
        "ID": 100043,
        "unavailableClass": None,
        "prop": 52003215,
        "equipment": _tools.ROList([[80582001, 2, 4]]),
        "props": _tools.ROList([30000290, 30000291, 30000292])
    }),
    100044: _tools.RODict({
        "ID": 100044,
        "unavailableClass": None,
        "prop": 52003216,
        "equipment": _tools.ROList([[80682001, 2, 4], [80782001, 2, 4]]),
        "props": None
    }),
    100045: _tools.RODict({
        "ID": 100045,
        "unavailableClass": None,
        "prop": 52003218,
        "equipment": _tools.ROList([[80692001, 2, 4], [80794001, 2, 4]]),
        "props": None
    }),
    100046: _tools.RODict({
        "ID": 100046,
        "unavailableClass": None,
        "prop": 52003181,
        "equipment": _tools.ROList([[80113001, 2, 1], [80123001, 2, 1], [80133001, 2, 1]]),
        "props": None
    }),
    100047: _tools.RODict({
        "ID": 100047,
        "unavailableClass": None,
        "prop": 52003185,
        "equipment": _tools.ROList([[80213001, 2, 1], [80223001, 2, 1], [80233001, 2, 1]]),
        "props": None
    }),
    100048: _tools.RODict({
        "ID": 100048,
        "unavailableClass": None,
        "prop": 52003189,
        "equipment": _tools.ROList([[80313001, 2, 1], [80323001, 2, 1], [80333001, 2, 1]]),
        "props": None
    }),
    100049: _tools.RODict({
        "ID": 100049,
        "unavailableClass": None,
        "prop": 52003193,
        "equipment": _tools.ROList([[80413001, 2, 1], [80423001, 2, 1], [80433001, 2, 1]]),
        "props": None
    }),
    100050: _tools.RODict({
        "ID": 100050,
        "unavailableClass": None,
        "prop": 52003197,
        "equipment": _tools.ROList([[80583001, 2, 1]]),
        "props": _tools.ROList([30000293, 30000294, 30000295])
    }),
    100051: _tools.RODict({
        "ID": 100051,
        "unavailableClass": None,
        "prop": 52003201,
        "equipment": _tools.ROList([[80683001, 2, 1], [80783001, 2, 1]]),
        "props": None
    }),
    100052: _tools.RODict({
        "ID": 100052,
        "unavailableClass": None,
        "prop": 52003205,
        "equipment": _tools.ROList([[80693001, 2, 1], [80793001, 2, 1]]),
        "props": None
    }),
    100053: _tools.RODict({
        "ID": 100053,
        "unavailableClass": None,
        "prop": 52003209,
        "equipment": None,
        "props": _tools.ROList([30990128, 30990133, 30990134])
    }),
    100054: _tools.RODict({
        "ID": 100054,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003211,
        "equipment": None,
        "props": _tools.ROList([30990129, 30990130, 30990131, 30990132])
    }),
    100055: _tools.RODict({
        "ID": 100055,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003212,
        "equipment": _tools.ROList([[80113001, 3, 2], [80123001, 3, 2], [80133001, 3, 2]]),
        "props": None
    }),
    100056: _tools.RODict({
        "ID": 100056,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003213,
        "equipment": _tools.ROList([[80213001, 3, 2], [80223001, 3, 2], [80233001, 3, 2]]),
        "props": None
    }),
    100057: _tools.RODict({
        "ID": 100057,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003214,
        "equipment": _tools.ROList([[80313001, 3, 2], [80323001, 3, 2], [80333001, 3, 2]]),
        "props": None
    }),
    100058: _tools.RODict({
        "ID": 100058,
        "unavailableClass": None,
        "prop": 52003215,
        "equipment": _tools.ROList([[80413001, 3, 2], [80423001, 3, 2], [80433001, 3, 2]]),
        "props": None
    }),
    100059: _tools.RODict({
        "ID": 100059,
        "unavailableClass": None,
        "prop": 52003216,
        "equipment": _tools.ROList([[80583001, 3, 2]]),
        "props": _tools.ROList([30000293, 30000294, 30000295])
    }),
    100060: _tools.RODict({
        "ID": 100060,
        "unavailableClass": None,
        "prop": 52003218,
        "equipment": _tools.ROList([[80683001, 3, 2], [80783001, 3, 2]]),
        "props": None
    }),
    100061: _tools.RODict({
        "ID": 100061,
        "unavailableClass": None,
        "prop": 52003181,
        "equipment": _tools.ROList([[80693001, 3, 2], [80793001, 3, 2]]),
        "props": None
    }),
    100062: _tools.RODict({
        "ID": 100062,
        "unavailableClass": None,
        "prop": 52003185,
        "equipment": _tools.ROList([[80113001, 3, 3], [80123001, 3, 3], [80133001, 3, 3]]),
        "props": None
    }),
    100063: _tools.RODict({
        "ID": 100063,
        "unavailableClass": None,
        "prop": 52003189,
        "equipment": _tools.ROList([[80213001, 3, 3], [80223001, 3, 3], [80233001, 3, 3]]),
        "props": None
    }),
    100064: _tools.RODict({
        "ID": 100064,
        "unavailableClass": None,
        "prop": 52003193,
        "equipment": _tools.ROList([[80313001, 3, 3], [80323001, 3, 3], [80333001, 3, 3]]),
        "props": None
    }),
    100065: _tools.RODict({
        "ID": 100065,
        "unavailableClass": None,
        "prop": 52003197,
        "equipment": _tools.ROList([[80413001, 3, 3], [80423001, 3, 3], [80433001, 3, 3]]),
        "props": None
    }),
    100066: _tools.RODict({
        "ID": 100066,
        "unavailableClass": None,
        "prop": 52003201,
        "equipment": _tools.ROList([[80583001, 3, 3]]),
        "props": _tools.ROList([30000293, 30000294, 30000295])
    }),
    100067: _tools.RODict({
        "ID": 100067,
        "unavailableClass": None,
        "prop": 52003205,
        "equipment": _tools.ROList([[80683001, 3, 3], [80783001, 3, 3]]),
        "props": None
    }),
    100068: _tools.RODict({
        "ID": 100068,
        "unavailableClass": None,
        "prop": 52003209,
        "equipment": _tools.ROList([[80693001, 3, 3], [80793001, 3, 3]]),
        "props": None
    }),
    100069: _tools.RODict({
        "ID": 100069,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003211,
        "equipment": _tools.ROList([[80113001, 3, 4], [80123001, 3, 4], [80133001, 3, 4]]),
        "props": None
    }),
    100070: _tools.RODict({
        "ID": 100070,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003212,
        "equipment": _tools.ROList([[80213001, 3, 4], [80223001, 3, 4], [80233001, 3, 4]]),
        "props": None
    }),
    100071: _tools.RODict({
        "ID": 100071,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003213,
        "equipment": _tools.ROList([[80313001, 3, 4], [80323001, 3, 4], [80333001, 3, 4]]),
        "props": None
    }),
    100072: _tools.RODict({
        "ID": 100072,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003214,
        "equipment": _tools.ROList([[80413001, 3, 4], [80423001, 3, 4], [80433001, 3, 4]]),
        "props": None
    }),
    100073: _tools.RODict({
        "ID": 100073,
        "unavailableClass": None,
        "prop": 52003215,
        "equipment": _tools.ROList([[80583001, 3, 4]]),
        "props": _tools.ROList([30000293, 30000294, 30000295])
    }),
    100074: _tools.RODict({
        "ID": 100074,
        "unavailableClass": None,
        "prop": 52003216,
        "equipment": _tools.ROList([[80683001, 4, 4], [80783001, 4, 4]]),
        "props": None
    }),
    100075: _tools.RODict({
        "ID": 100075,
        "unavailableClass": None,
        "prop": 52003218,
        "equipment": _tools.ROList([[80693001, 4, 4], [80793001, 4, 4]]),
        "props": None
    }),
    100076: _tools.RODict({
        "ID": 100076,
        "unavailableClass": None,
        "prop": 52003181,
        "equipment": _tools.ROList([[80113001, 4, 5], [80123001, 4, 5], [80133001, 4, 5]]),
        "props": None
    }),
    100077: _tools.RODict({
        "ID": 100077,
        "unavailableClass": None,
        "prop": 52003185,
        "equipment": _tools.ROList([[80213001, 4, 5], [80223001, 4, 5], [80233001, 4, 5]]),
        "props": None
    }),
    100078: _tools.RODict({
        "ID": 100078,
        "unavailableClass": None,
        "prop": 52003189,
        "equipment": _tools.ROList([[80313001, 4, 5], [80323001, 4, 5], [80333001, 4, 5]]),
        "props": None
    }),
    100079: _tools.RODict({
        "ID": 100079,
        "unavailableClass": None,
        "prop": 52003193,
        "equipment": _tools.ROList([[80413001, 4, 5], [80423001, 4, 5], [80433001, 4, 5]]),
        "props": None
    }),
    100080: _tools.RODict({
        "ID": 100080,
        "unavailableClass": None,
        "prop": 52003197,
        "equipment": _tools.ROList([[80583001, 4, 5]]),
        "props": _tools.ROList([30000293, 30000294, 30000295])
    }),
    100081: _tools.RODict({
        "ID": 100081,
        "unavailableClass": None,
        "prop": 52003201,
        "equipment": _tools.ROList([[80683001, 4, 5], [80783001, 4, 5]]),
        "props": None
    }),
    100082: _tools.RODict({
        "ID": 100082,
        "unavailableClass": None,
        "prop": 52003205,
        "equipment": _tools.ROList([[80693001, 4, 5], [80793001, 4, 5]]),
        "props": None
    }),
    100083: _tools.RODict({
        "ID": 100083,
        "unavailableClass": None,
        "prop": 52003209,
        "equipment": _tools.ROList([[80114001, 4, 1], [80124001, 4, 1], [80134001, 4, 1]]),
        "props": None
    }),
    100084: _tools.RODict({
        "ID": 100084,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003211,
        "equipment": _tools.ROList([[80214001, 4, 5], [80224001, 4, 5], [80234001, 4, 5]]),
        "props": None
    }),
    100085: _tools.RODict({
        "ID": 100085,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003212,
        "equipment": _tools.ROList([[80214001, 4, 1], [80224001, 4, 1], [80234001, 4, 1]]),
        "props": None
    }),
    100086: _tools.RODict({
        "ID": 100086,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003213,
        "equipment": _tools.ROList([[80214001, 4, 5], [80224001, 4, 5], [80234001, 4, 5]]),
        "props": None
    }),
    100087: _tools.RODict({
        "ID": 100087,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003214,
        "equipment": _tools.ROList([[80314001, 4, 1], [80324001, 4, 1], [80334001, 4, 1]]),
        "props": None
    }),
    100088: _tools.RODict({
        "ID": 100088,
        "unavailableClass": None,
        "prop": 52003215,
        "equipment": _tools.ROList([[80414001, 4, 1], [80424001, 4, 1], [80434001, 4, 1]]),
        "props": None
    }),
    100089: _tools.RODict({
        "ID": 100089,
        "unavailableClass": None,
        "prop": 52003216,
        "equipment": _tools.ROList([[80584001, 4, 1]]),
        "props": _tools.ROList([30000296, 30000297, 30000298])
    }),
    100090: _tools.RODict({
        "ID": 100090,
        "unavailableClass": None,
        "prop": 52003218,
        "equipment": _tools.ROList([[80684001, 4, 1], [80784001, 4, 1]]),
        "props": None
    }),
    100091: _tools.RODict({
        "ID": 100091,
        "unavailableClass": None,
        "prop": 52003181,
        "equipment": _tools.ROList([[80694001, 4, 1], [80794001, 4, 1]]),
        "props": None
    }),
    100092: _tools.RODict({
        "ID": 100092,
        "unavailableClass": None,
        "prop": 52003185,
        "equipment": _tools.ROList([[80694001, 4, 1], [80794001, 4, 1]]),
        "props": None
    }),
    100093: _tools.RODict({
        "ID": 100093,
        "unavailableClass": None,
        "prop": 52003189,
        "equipment": None,
        "props": _tools.ROList([30990135, 30990140, 30990141])
    }),
    100094: _tools.RODict({
        "ID": 100094,
        "unavailableClass": None,
        "prop": 52003193,
        "equipment": None,
        "props": _tools.ROList([30990136, 30990137, 30990138, 30990139])
    }),
    100095: _tools.RODict({
        "ID": 100095,
        "unavailableClass": None,
        "prop": 52003197,
        "equipment": _tools.ROList([[80114001, 5, 2], [80124001, 5, 2], [80134001, 5, 2]]),
        "props": None
    }),
    100096: _tools.RODict({
        "ID": 100096,
        "unavailableClass": None,
        "prop": 52003201,
        "equipment": _tools.ROList([[80114001, 5, 6], [80124001, 5, 6], [80134001, 5, 6]]),
        "props": None
    }),
    100097: _tools.RODict({
        "ID": 100097,
        "unavailableClass": None,
        "prop": 52003205,
        "equipment": _tools.ROList([[80214001, 5, 2], [80224001, 5, 2], [80234001, 5, 2]]),
        "props": None
    }),
    100098: _tools.RODict({
        "ID": 100098,
        "unavailableClass": None,
        "prop": 52003209,
        "equipment": _tools.ROList([[80214001, 5, 6], [80224001, 5, 6], [80234001, 5, 6]]),
        "props": None
    }),
    100099: _tools.RODict({
        "ID": 100099,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003211,
        "equipment": _tools.ROList([[80314001, 5, 2], [80324001, 5, 2], [80334001, 5, 2]]),
        "props": None
    }),
    100100: _tools.RODict({
        "ID": 100100,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003212,
        "equipment": _tools.ROList([[80414001, 5, 2], [80424001, 5, 2], [80434001, 5, 2]]),
        "props": None
    }),
    100101: _tools.RODict({
        "ID": 100101,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003213,
        "equipment": _tools.ROList([[80584001, 5, 2]]),
        "props": _tools.ROList([30000296, 30000297, 30000298])
    }),
    100102: _tools.RODict({
        "ID": 100102,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003214,
        "equipment": _tools.ROList([[80684001, 5, 2], [80784001, 5, 2]]),
        "props": None
    }),
    100103: _tools.RODict({
        "ID": 100103,
        "unavailableClass": None,
        "prop": 52003215,
        "equipment": _tools.ROList([[80693001, 5, 2], [80793001, 5, 2]]),
        "props": None
    }),
    100104: _tools.RODict({
        "ID": 100104,
        "unavailableClass": None,
        "prop": 52003216,
        "equipment": _tools.ROList([[80693001, 5, 2], [80793001, 5, 2]]),
        "props": None
    }),
    100105: _tools.RODict({
        "ID": 100105,
        "unavailableClass": None,
        "prop": 52003218,
        "equipment": _tools.ROList([[80114001, 5, 3], [80124001, 5, 3], [80134001, 5, 3]]),
        "props": None
    }),
    100106: _tools.RODict({
        "ID": 100106,
        "unavailableClass": None,
        "prop": 52003181,
        "equipment": _tools.ROList([[80114001, 5, 7], [80124001, 5, 7], [80134001, 5, 7]]),
        "props": None
    }),
    100107: _tools.RODict({
        "ID": 100107,
        "unavailableClass": None,
        "prop": 52003185,
        "equipment": _tools.ROList([[80214001, 5, 3], [80224001, 5, 3], [80234001, 5, 3]]),
        "props": None
    }),
    100108: _tools.RODict({
        "ID": 100108,
        "unavailableClass": None,
        "prop": 52003189,
        "equipment": _tools.ROList([[80214001, 5, 7], [80224001, 5, 7], [80234001, 5, 7]]),
        "props": None
    }),
    100109: _tools.RODict({
        "ID": 100109,
        "unavailableClass": None,
        "prop": 52003193,
        "equipment": _tools.ROList([[80314001, 5, 3], [80324001, 5, 3], [80334001, 5, 3]]),
        "props": None
    }),
    100110: _tools.RODict({
        "ID": 100110,
        "unavailableClass": None,
        "prop": 52003197,
        "equipment": _tools.ROList([[80414001, 5, 3], [80424001, 5, 3], [80434001, 5, 3]]),
        "props": None
    }),
    100111: _tools.RODict({
        "ID": 100111,
        "unavailableClass": None,
        "prop": 52003201,
        "equipment": _tools.ROList([[80584001, 5, 3]]),
        "props": _tools.ROList([30000296, 30000297, 30000298])
    }),
    100112: _tools.RODict({
        "ID": 100112,
        "unavailableClass": None,
        "prop": 52003205,
        "equipment": _tools.ROList([[80684001, 5, 3], [80784001, 5, 3]]),
        "props": None
    }),
    100113: _tools.RODict({
        "ID": 100113,
        "unavailableClass": None,
        "prop": 52003209,
        "equipment": _tools.ROList([[80694001, 5, 3], [80794001, 5, 3]]),
        "props": None
    }),
    100114: _tools.RODict({
        "ID": 100114,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003211,
        "equipment": _tools.ROList([[80694001, 5, 3], [80794001, 5, 3]]),
        "props": None
    }),
    100115: _tools.RODict({
        "ID": 100115,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003212,
        "equipment": _tools.ROList([[80114001, 6, 1], [80124001, 6, 1], [80134001, 6, 1]]),
        "props": None
    }),
    100116: _tools.RODict({
        "ID": 100116,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003213,
        "equipment": _tools.ROList([[80114001, 6, 2], [80124001, 6, 2], [80134001, 6, 2]]),
        "props": None
    }),
    100117: _tools.RODict({
        "ID": 100117,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003214,
        "equipment": _tools.ROList([[80214001, 6, 1], [80224001, 6, 1], [80234001, 6, 1]]),
        "props": None
    }),
    100118: _tools.RODict({
        "ID": 100118,
        "unavailableClass": None,
        "prop": 52003215,
        "equipment": _tools.ROList([[80214001, 6, 2], [80224001, 6, 2], [80234001, 6, 2]]),
        "props": None
    }),
    100119: _tools.RODict({
        "ID": 100119,
        "unavailableClass": None,
        "prop": 52003216,
        "equipment": _tools.ROList([[80314001, 6, 1], [80324001, 6, 1], [80334001, 6, 1]]),
        "props": None
    }),
    100120: _tools.RODict({
        "ID": 100120,
        "unavailableClass": None,
        "prop": 52003218,
        "equipment": _tools.ROList([[80414001, 6, 1], [80424001, 6, 1], [80434001, 6, 1]]),
        "props": None
    }),
    100121: _tools.RODict({
        "ID": 100121,
        "unavailableClass": None,
        "prop": 52003181,
        "equipment": _tools.ROList([[80781001, 6, 1]]),
        "props": _tools.ROList([30000296, 30000297, 30000298])
    }),
    100122: _tools.RODict({
        "ID": 100122,
        "unavailableClass": None,
        "prop": 52003185,
        "equipment": _tools.ROList([[80782001, 6, 1], [80792001, 6, 1]]),
        "props": None
    }),
    100123: _tools.RODict({
        "ID": 100123,
        "unavailableClass": None,
        "prop": 52003189,
        "equipment": _tools.ROList([[80783001, 6, 1], [80793001, 6, 1]]),
        "props": None
    }),
    100124: _tools.RODict({
        "ID": 100124,
        "unavailableClass": None,
        "prop": 52003193,
        "equipment": _tools.ROList([[80784001, 6, 2], [80794001, 6, 1]]),
        "props": None
    }),
    100125: _tools.RODict({
        "ID": 100125,
        "unavailableClass": None,
        "prop": 52003197,
        "equipment": None,
        "props": _tools.ROList([30990142, 30990147, 30990148])
    }),
    100126: _tools.RODict({
        "ID": 100126,
        "unavailableClass": None,
        "prop": 52003201,
        "equipment": None,
        "props": _tools.ROList([30990143, 30990144, 30990145, 30990146])
    })
})
minKey = 100001
maxKey = 100126