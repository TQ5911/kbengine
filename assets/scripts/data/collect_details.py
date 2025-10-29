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
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003181,
        "progress": 10,
        "equipment": _tools.ROList([[80111001, 0, 1], [80121001, 0, 1], [80131001, 0, 1]]),
        "props": None
    }),
    100002: _tools.RODict({
        "ID": 100002,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003185,
        "progress": 10,
        "equipment": _tools.ROList([[80211001, 0, 1], [80221001, 0, 1], [80231001, 0, 1]]),
        "props": None
    }),
    100003: _tools.RODict({
        "ID": 100003,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003189,
        "progress": 10,
        "equipment": _tools.ROList([[80311001, 0, 1], [80321001, 0, 1], [80331001, 0, 1]]),
        "props": None
    }),
    100004: _tools.RODict({
        "ID": 100004,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003193,
        "progress": 10,
        "equipment": _tools.ROList([[80411001, 0, 1], [80421001, 0, 1], [80431001, 0, 1]]),
        "props": None
    }),
    100005: _tools.RODict({
        "ID": 100005,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003197,
        "progress": 10,
        "equipment": _tools.ROList([[80581001, 0, 1]]),
        "props": _tools.ROList([30000287, 30000288, 30000289])
    }),
    100006: _tools.RODict({
        "ID": 100006,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003201,
        "progress": 12,
        "equipment": _tools.ROList([[80111002, 0, 1], [80121002, 0, 1], [80131002, 0, 1]]),
        "props": None
    }),
    100007: _tools.RODict({
        "ID": 100007,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003205,
        "progress": 12,
        "equipment": _tools.ROList([[80211002, 0, 1], [80221002, 0, 1], [80231002, 0, 1]]),
        "props": None
    }),
    100008: _tools.RODict({
        "ID": 100008,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003209,
        "progress": 12,
        "equipment": _tools.ROList([[80311002, 0, 1], [80321002, 0, 1], [80331002, 0, 1]]),
        "props": None
    }),
    100009: _tools.RODict({
        "ID": 100009,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003211,
        "progress": 12,
        "equipment": _tools.ROList([[80411002, 0, 1], [80421002, 0, 1], [80431002, 0, 1]]),
        "props": None
    }),
    100010: _tools.RODict({
        "ID": 100010,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003212,
        "progress": 12,
        "equipment": _tools.ROList([[80581002, 0, 1]]),
        "props": _tools.ROList([30000287, 30000288, 30000289])
    }),
    100011: _tools.RODict({
        "ID": 100011,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003213,
        "progress": 14,
        "equipment": _tools.ROList([[80111003, 0, 1], [80121003, 0, 1], [80131003, 0, 1]]),
        "props": None
    }),
    100012: _tools.RODict({
        "ID": 100012,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003214,
        "progress": 14,
        "equipment": _tools.ROList([[80211003, 0, 1], [80221003, 0, 1], [80231003, 0, 1]]),
        "props": None
    }),
    100013: _tools.RODict({
        "ID": 100013,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003215,
        "progress": 14,
        "equipment": _tools.ROList([[80311003, 0, 1], [80321003, 0, 1], [80331003, 0, 1]]),
        "props": None
    }),
    100014: _tools.RODict({
        "ID": 100014,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003216,
        "progress": 14,
        "equipment": _tools.ROList([[80411003, 0, 1], [80421003, 0, 1], [80431003, 0, 1]]),
        "props": None
    }),
    100015: _tools.RODict({
        "ID": 100015,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003218,
        "progress": 14,
        "equipment": _tools.ROList([[80581003, 0, 1]]),
        "props": _tools.ROList([30000287, 30000288, 30000289])
    }),
    100016: _tools.RODict({
        "ID": 100016,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003220,
        "progress": 20,
        "equipment": _tools.ROList([[80112001, 0, 2], [80122001, 0, 2], [80132001, 0, 2]]),
        "props": None
    }),
    100017: _tools.RODict({
        "ID": 100017,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003224,
        "progress": 20,
        "equipment": _tools.ROList([[80212001, 0, 2], [80222001, 0, 2], [80232001, 0, 2]]),
        "props": None
    }),
    100018: _tools.RODict({
        "ID": 100018,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003228,
        "progress": 20,
        "equipment": _tools.ROList([[80312001, 0, 2], [80322001, 0, 2], [80332001, 0, 2]]),
        "props": None
    }),
    100019: _tools.RODict({
        "ID": 100019,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003232,
        "progress": 20,
        "equipment": _tools.ROList([[80412001, 0, 2], [80422001, 0, 2], [80432001, 0, 2]]),
        "props": None
    }),
    100020: _tools.RODict({
        "ID": 100020,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003236,
        "progress": 20,
        "equipment": _tools.ROList([[80582001, 0, 2]]),
        "props": _tools.ROList([30000290, 30000291, 30000292])
    }),
    100021: _tools.RODict({
        "ID": 100021,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003238,
        "progress": 20,
        "equipment": _tools.ROList([[80682001, 0, 2], [80782001, 0, 2]]),
        "props": None
    }),
    100022: _tools.RODict({
        "ID": 100022,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003181,
        "progress": 20,
        "equipment": _tools.ROList([[80692001, 0, 2], [80792001, 0, 2]]),
        "props": None
    }),
    100023: _tools.RODict({
        "ID": 100023,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003205,
        "progress": 20,
        "equipment": None,
        "props": _tools.ROList([30990121, 30990126, 30990127])
    }),
    100024: _tools.RODict({
        "ID": 100024,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003209,
        "progress": 20,
        "equipment": None,
        "props": _tools.ROList([30990122, 30990123, 30990124, 30990125])
    }),
    100025: _tools.RODict({
        "ID": 100025,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003185,
        "progress": 24,
        "equipment": _tools.ROList([[80112002, 1, 2], [80122002, 1, 2], [80132002, 1, 2]]),
        "props": None
    }),
    100026: _tools.RODict({
        "ID": 100026,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003189,
        "progress": 24,
        "equipment": _tools.ROList([[80212002, 1, 2], [80222002, 1, 2], [80232002, 1, 2]]),
        "props": None
    }),
    100027: _tools.RODict({
        "ID": 100027,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003193,
        "progress": 24,
        "equipment": _tools.ROList([[80312002, 1, 2], [80322002, 1, 2], [80332002, 1, 2]]),
        "props": None
    }),
    100028: _tools.RODict({
        "ID": 100028,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003197,
        "progress": 24,
        "equipment": _tools.ROList([[80412002, 1, 2], [80422002, 1, 2], [80432002, 1, 2]]),
        "props": None
    }),
    100029: _tools.RODict({
        "ID": 100029,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003201,
        "progress": 24,
        "equipment": _tools.ROList([[80582002, 1, 2]]),
        "props": _tools.ROList([30000290, 30000291, 30000292])
    }),
    100030: _tools.RODict({
        "ID": 100030,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003205,
        "progress": 24,
        "equipment": _tools.ROList([[80682002, 1, 2], [80782002, 1, 2]]),
        "props": None
    }),
    100031: _tools.RODict({
        "ID": 100031,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003209,
        "progress": 24,
        "equipment": _tools.ROList([[80692002, 1, 2], [80792002, 1, 2]]),
        "props": None
    }),
    100032: _tools.RODict({
        "ID": 100032,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003211,
        "progress": 28,
        "equipment": _tools.ROList([[80112003, 1, 2], [80122003, 1, 2], [80132003, 1, 2]]),
        "props": None
    }),
    100033: _tools.RODict({
        "ID": 100033,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003212,
        "progress": 28,
        "equipment": _tools.ROList([[80212003, 1, 2], [80222003, 1, 2], [80232003, 1, 2]]),
        "props": None
    }),
    100034: _tools.RODict({
        "ID": 100034,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003213,
        "progress": 28,
        "equipment": _tools.ROList([[80312003, 1, 2], [80322003, 1, 2], [80332003, 1, 2]]),
        "props": None
    }),
    100035: _tools.RODict({
        "ID": 100035,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003214,
        "progress": 28,
        "equipment": _tools.ROList([[80412003, 1, 2], [80422003, 1, 2], [80432003, 1, 2]]),
        "props": None
    }),
    100036: _tools.RODict({
        "ID": 100036,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003215,
        "progress": 28,
        "equipment": _tools.ROList([[80582003, 1, 2]]),
        "props": _tools.ROList([30000290, 30000291, 30000292])
    }),
    100037: _tools.RODict({
        "ID": 100037,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003216,
        "progress": 28,
        "equipment": _tools.ROList([[80682003, 1, 2], [80782003, 1, 2]]),
        "props": None
    }),
    100038: _tools.RODict({
        "ID": 100038,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003218,
        "progress": 28,
        "equipment": _tools.ROList([[80692003, 1, 2], [80792003, 1, 2]]),
        "props": None
    }),
    100039: _tools.RODict({
        "ID": 100039,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003220,
        "progress": 32,
        "equipment": _tools.ROList([[80112004, 2, 2], [80122004, 2, 2], [80132004, 2, 2]]),
        "props": None
    }),
    100040: _tools.RODict({
        "ID": 100040,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003224,
        "progress": 32,
        "equipment": _tools.ROList([[80212004, 2, 2], [80222004, 2, 2], [80232004, 2, 2]]),
        "props": None
    }),
    100041: _tools.RODict({
        "ID": 100041,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003228,
        "progress": 32,
        "equipment": _tools.ROList([[80312004, 2, 2], [80322004, 2, 2], [80332004, 2, 2]]),
        "props": None
    }),
    100042: _tools.RODict({
        "ID": 100042,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003232,
        "progress": 32,
        "equipment": _tools.ROList([[80412004, 2, 2], [80422004, 2, 2], [80432004, 2, 2]]),
        "props": None
    }),
    100043: _tools.RODict({
        "ID": 100043,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003236,
        "progress": 32,
        "equipment": _tools.ROList([[80582004, 2, 2]]),
        "props": _tools.ROList([30000290, 30000291, 30000292])
    }),
    100044: _tools.RODict({
        "ID": 100044,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003238,
        "progress": 32,
        "equipment": _tools.ROList([[80682004, 2, 2], [80782004, 2, 2]]),
        "props": None
    }),
    100045: _tools.RODict({
        "ID": 100045,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003181,
        "progress": 32,
        "equipment": _tools.ROList([[80692004, 2, 2], [80792004, 2, 2]]),
        "props": None
    }),
    100046: _tools.RODict({
        "ID": 100046,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003182,
        "progress": 60,
        "equipment": _tools.ROList([[80113001, 2, 3], [80123001, 2, 3], [80133001, 2, 3]]),
        "props": None
    }),
    100047: _tools.RODict({
        "ID": 100047,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003186,
        "progress": 60,
        "equipment": _tools.ROList([[80213001, 2, 3], [80223001, 2, 3], [80233001, 2, 3]]),
        "props": None
    }),
    100048: _tools.RODict({
        "ID": 100048,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003190,
        "progress": 60,
        "equipment": _tools.ROList([[80313001, 2, 3], [80323001, 2, 3], [80333001, 2, 3]]),
        "props": None
    }),
    100049: _tools.RODict({
        "ID": 100049,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003194,
        "progress": 60,
        "equipment": _tools.ROList([[80413001, 2, 3], [80423001, 2, 3], [80433001, 2, 3]]),
        "props": None
    }),
    100050: _tools.RODict({
        "ID": 100050,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003198,
        "progress": 60,
        "equipment": _tools.ROList([[80583001, 2, 3]]),
        "props": _tools.ROList([30000293, 30000294, 30000295])
    }),
    100051: _tools.RODict({
        "ID": 100051,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003202,
        "progress": 60,
        "equipment": _tools.ROList([[80683001, 2, 3], [80783001, 2, 3]]),
        "props": None
    }),
    100052: _tools.RODict({
        "ID": 100052,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003206,
        "progress": 60,
        "equipment": _tools.ROList([[80693001, 2, 3], [80793001, 2, 3]]),
        "props": None
    }),
    100053: _tools.RODict({
        "ID": 100053,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003206,
        "progress": 60,
        "equipment": None,
        "props": _tools.ROList([30990128, 30990133, 30990134])
    }),
    100054: _tools.RODict({
        "ID": 100054,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003209,
        "progress": 60,
        "equipment": None,
        "props": _tools.ROList([30990129, 30990130, 30990131, 30990132])
    }),
    100055: _tools.RODict({
        "ID": 100055,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003221,
        "progress": 66,
        "equipment": _tools.ROList([[80113002, 3, 3], [80123002, 3, 3], [80133002, 3, 3]]),
        "props": None
    }),
    100056: _tools.RODict({
        "ID": 100056,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003225,
        "progress": 66,
        "equipment": _tools.ROList([[80213002, 3, 3], [80223002, 3, 3], [80233002, 3, 3]]),
        "props": None
    }),
    100057: _tools.RODict({
        "ID": 100057,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003229,
        "progress": 66,
        "equipment": _tools.ROList([[80313002, 3, 3], [80323002, 3, 3], [80333002, 3, 3]]),
        "props": None
    }),
    100058: _tools.RODict({
        "ID": 100058,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003233,
        "progress": 66,
        "equipment": _tools.ROList([[80413002, 3, 3], [80423002, 3, 3], [80433002, 3, 3]]),
        "props": None
    }),
    100059: _tools.RODict({
        "ID": 100059,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003183,
        "progress": 66,
        "equipment": _tools.ROList([[80583002, 3, 3]]),
        "props": _tools.ROList([30000293, 30000294, 30000295])
    }),
    100060: _tools.RODict({
        "ID": 100060,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003187,
        "progress": 66,
        "equipment": _tools.ROList([[80683002, 3, 3], [80783002, 3, 3]]),
        "props": None
    }),
    100061: _tools.RODict({
        "ID": 100061,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003191,
        "progress": 66,
        "equipment": _tools.ROList([[80693002, 3, 3], [80793002, 3, 3]]),
        "props": None
    }),
    100062: _tools.RODict({
        "ID": 100062,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003195,
        "progress": 72,
        "equipment": _tools.ROList([[80113003, 3, 3], [80123003, 3, 3], [80133003, 3, 3]]),
        "props": None
    }),
    100063: _tools.RODict({
        "ID": 100063,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003199,
        "progress": 72,
        "equipment": _tools.ROList([[80213003, 3, 3], [80223003, 3, 3], [80233003, 3, 3]]),
        "props": None
    }),
    100064: _tools.RODict({
        "ID": 100064,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003203,
        "progress": 72,
        "equipment": _tools.ROList([[80313003, 3, 3], [80323003, 3, 3], [80333003, 3, 3]]),
        "props": None
    }),
    100065: _tools.RODict({
        "ID": 100065,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003207,
        "progress": 72,
        "equipment": _tools.ROList([[80413003, 3, 3], [80423003, 3, 3], [80433003, 3, 3]]),
        "props": None
    }),
    100066: _tools.RODict({
        "ID": 100066,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003210,
        "progress": 72,
        "equipment": _tools.ROList([[80583003, 3, 3]]),
        "props": _tools.ROList([30000293, 30000294, 30000295])
    }),
    100067: _tools.RODict({
        "ID": 100067,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003217,
        "progress": 72,
        "equipment": _tools.ROList([[80683003, 3, 3], [80783003, 3, 3]]),
        "props": None
    }),
    100068: _tools.RODict({
        "ID": 100068,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003219,
        "progress": 72,
        "equipment": _tools.ROList([[80693003, 3, 3], [80793003, 3, 3]]),
        "props": None
    }),
    100069: _tools.RODict({
        "ID": 100069,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003222,
        "progress": 78,
        "equipment": _tools.ROList([[80113004, 3, 3], [80123004, 3, 3], [80133004, 3, 3]]),
        "props": None
    }),
    100070: _tools.RODict({
        "ID": 100070,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003226,
        "progress": 78,
        "equipment": _tools.ROList([[80213004, 3, 3], [80223004, 3, 3], [80233004, 3, 3]]),
        "props": None
    }),
    100071: _tools.RODict({
        "ID": 100071,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003230,
        "progress": 78,
        "equipment": _tools.ROList([[80313004, 3, 3], [80323004, 3, 3], [80333004, 3, 3]]),
        "props": None
    }),
    100072: _tools.RODict({
        "ID": 100072,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003234,
        "progress": 78,
        "equipment": _tools.ROList([[80413004, 3, 3], [80423004, 3, 3], [80433004, 3, 3]]),
        "props": None
    }),
    100073: _tools.RODict({
        "ID": 100073,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003209,
        "progress": 78,
        "equipment": _tools.ROList([[80583004, 3, 3]]),
        "props": _tools.ROList([30000293, 30000294, 30000295])
    }),
    100074: _tools.RODict({
        "ID": 100074,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003211,
        "progress": 78,
        "equipment": _tools.ROList([[80683004, 4, 3], [80783004, 4, 3]]),
        "props": None
    }),
    100075: _tools.RODict({
        "ID": 100075,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003212,
        "progress": 78,
        "equipment": _tools.ROList([[80693004, 4, 3], [80793004, 4, 3]]),
        "props": None
    }),
    100076: _tools.RODict({
        "ID": 100076,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003213,
        "progress": 84,
        "equipment": _tools.ROList([[80113005, 4, 3], [80123005, 4, 3], [80133005, 4, 3]]),
        "props": None
    }),
    100077: _tools.RODict({
        "ID": 100077,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003214,
        "progress": 84,
        "equipment": _tools.ROList([[80213005, 4, 3], [80223005, 4, 3], [80233005, 4, 3]]),
        "props": None
    }),
    100078: _tools.RODict({
        "ID": 100078,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003215,
        "progress": 84,
        "equipment": _tools.ROList([[80313005, 4, 3], [80323005, 4, 3], [80333005, 4, 3]]),
        "props": None
    }),
    100079: _tools.RODict({
        "ID": 100079,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003211,
        "progress": 84,
        "equipment": _tools.ROList([[80413005, 4, 3], [80423005, 4, 3], [80433005, 4, 3]]),
        "props": None
    }),
    100080: _tools.RODict({
        "ID": 100080,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003212,
        "progress": 84,
        "equipment": _tools.ROList([[80583005, 4, 3]]),
        "props": _tools.ROList([30000293, 30000294, 30000295])
    }),
    100081: _tools.RODict({
        "ID": 100081,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003237,
        "progress": 84,
        "equipment": _tools.ROList([[80683005, 4, 3], [80783005, 4, 3]]),
        "props": None
    }),
    100082: _tools.RODict({
        "ID": 100082,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003239,
        "progress": 84,
        "equipment": _tools.ROList([[80693005, 4, 3], [80793005, 4, 3]]),
        "props": None
    }),
    100083: _tools.RODict({
        "ID": 100083,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003213,
        "progress": 180,
        "equipment": _tools.ROList([[80114001, 4, 4], [80124001, 4, 4], [80134001, 4, 4]]),
        "props": None
    }),
    100084: _tools.RODict({
        "ID": 100084,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003214,
        "progress": 180,
        "equipment": _tools.ROList([[80214005, 4, 4], [80224005, 4, 4], [80234005, 4, 4]]),
        "props": None
    }),
    100085: _tools.RODict({
        "ID": 100085,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003217,
        "progress": 180,
        "equipment": _tools.ROList([[80214001, 4, 4], [80224001, 4, 4], [80234001, 4, 4]]),
        "props": None
    }),
    100086: _tools.RODict({
        "ID": 100086,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003219,
        "progress": 180,
        "equipment": _tools.ROList([[80214005, 4, 4], [80224005, 4, 4], [80234005, 4, 4]]),
        "props": None
    }),
    100087: _tools.RODict({
        "ID": 100087,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003237,
        "progress": 180,
        "equipment": _tools.ROList([[80314001, 4, 4], [80324001, 4, 4], [80334001, 4, 4]]),
        "props": None
    }),
    100088: _tools.RODict({
        "ID": 100088,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003239,
        "progress": 180,
        "equipment": _tools.ROList([[80414001, 4, 4], [80424001, 4, 4], [80434001, 4, 4]]),
        "props": None
    }),
    100089: _tools.RODict({
        "ID": 100089,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003183,
        "progress": 180,
        "equipment": _tools.ROList([[80584001, 4, 4]]),
        "props": _tools.ROList([30000296, 30000297, 30000298])
    }),
    100090: _tools.RODict({
        "ID": 100090,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003187,
        "progress": 180,
        "equipment": _tools.ROList([[80684001, 4, 4], [80784001, 4, 4]]),
        "props": None
    }),
    100091: _tools.RODict({
        "ID": 100091,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003191,
        "progress": 180,
        "equipment": _tools.ROList([[80694001, 4, 4], [80794001, 4, 4]]),
        "props": None
    }),
    100092: _tools.RODict({
        "ID": 100092,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003195,
        "progress": 180,
        "equipment": _tools.ROList([[80704001, 4, 4], [80804001, 4, 4]]),
        "props": None
    }),
    100093: _tools.RODict({
        "ID": 100093,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003207,
        "progress": 180,
        "equipment": None,
        "props": _tools.ROList([30990135, 30990140, 30990141])
    }),
    100094: _tools.RODict({
        "ID": 100094,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003210,
        "progress": 180,
        "equipment": None,
        "props": _tools.ROList([30990136, 30990137, 30990138, 30990139])
    }),
    100095: _tools.RODict({
        "ID": 100095,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003199,
        "progress": 188,
        "equipment": _tools.ROList([[80114002, 5, 4], [80124002, 5, 4], [80134002, 5, 4]]),
        "props": None
    }),
    100096: _tools.RODict({
        "ID": 100096,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003203,
        "progress": 188,
        "equipment": _tools.ROList([[80114006, 5, 4], [80124006, 5, 4], [80134006, 5, 4]]),
        "props": None
    }),
    100097: _tools.RODict({
        "ID": 100097,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003207,
        "progress": 188,
        "equipment": _tools.ROList([[80214002, 5, 4], [80224002, 5, 4], [80234002, 5, 4]]),
        "props": None
    }),
    100098: _tools.RODict({
        "ID": 100098,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003210,
        "progress": 188,
        "equipment": _tools.ROList([[80214006, 5, 4], [80224006, 5, 4], [80234006, 5, 4]]),
        "props": None
    }),
    100099: _tools.RODict({
        "ID": 100099,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003217,
        "progress": 188,
        "equipment": _tools.ROList([[80314002, 5, 4], [80324002, 5, 4], [80334002, 5, 4]]),
        "props": None
    }),
    100100: _tools.RODict({
        "ID": 100100,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003219,
        "progress": 188,
        "equipment": _tools.ROList([[80414002, 5, 4], [80424002, 5, 4], [80434002, 5, 4]]),
        "props": None
    }),
    100101: _tools.RODict({
        "ID": 100101,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003222,
        "progress": 188,
        "equipment": _tools.ROList([[80584002, 5, 4]]),
        "props": _tools.ROList([30000296, 30000297, 30000298])
    }),
    100102: _tools.RODict({
        "ID": 100102,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003226,
        "progress": 188,
        "equipment": _tools.ROList([[80684002, 5, 4], [80784002, 5, 4]]),
        "props": None
    }),
    100103: _tools.RODict({
        "ID": 100103,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003230,
        "progress": 188,
        "equipment": _tools.ROList([[80693002, 5, 4], [80793002, 5, 4]]),
        "props": None
    }),
    100104: _tools.RODict({
        "ID": 100104,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003234,
        "progress": 188,
        "equipment": _tools.ROList([[80703002, 5, 4], [80803002, 5, 4]]),
        "props": None
    }),
    100105: _tools.RODict({
        "ID": 100105,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003237,
        "progress": 196,
        "equipment": _tools.ROList([[80114003, 5, 4], [80124003, 5, 4], [80134003, 5, 4]]),
        "props": None
    }),
    100106: _tools.RODict({
        "ID": 100106,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003239,
        "progress": 196,
        "equipment": _tools.ROList([[80114007, 5, 4], [80124007, 5, 4], [80134007, 5, 4]]),
        "props": None
    }),
    100107: _tools.RODict({
        "ID": 100107,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003184,
        "progress": 196,
        "equipment": _tools.ROList([[80214003, 5, 4], [80224003, 5, 4], [80234003, 5, 4]]),
        "props": None
    }),
    100108: _tools.RODict({
        "ID": 100108,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003188,
        "progress": 196,
        "equipment": _tools.ROList([[80214007, 5, 4], [80224007, 5, 4], [80234007, 5, 4]]),
        "props": None
    }),
    100109: _tools.RODict({
        "ID": 100109,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003192,
        "progress": 196,
        "equipment": _tools.ROList([[80314003, 5, 4], [80324003, 5, 4], [80334003, 5, 4]]),
        "props": None
    }),
    100110: _tools.RODict({
        "ID": 100110,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003196,
        "progress": 196,
        "equipment": _tools.ROList([[80414003, 5, 4], [80424003, 5, 4], [80434003, 5, 4]]),
        "props": None
    }),
    100111: _tools.RODict({
        "ID": 100111,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003200,
        "progress": 196,
        "equipment": _tools.ROList([[80584003, 5, 4]]),
        "props": _tools.ROList([30000296, 30000297, 30000298])
    }),
    100112: _tools.RODict({
        "ID": 100112,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003204,
        "progress": 196,
        "equipment": _tools.ROList([[80684003, 5, 4], [80784003, 5, 4]]),
        "props": None
    }),
    100113: _tools.RODict({
        "ID": 100113,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003208,
        "progress": 196,
        "equipment": _tools.ROList([[80694003, 5, 4], [80794003, 5, 4]]),
        "props": None
    }),
    100114: _tools.RODict({
        "ID": 100114,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003223,
        "progress": 196,
        "equipment": _tools.ROList([[80704003, 5, 4], [80804003, 5, 4]]),
        "props": None
    }),
    100115: _tools.RODict({
        "ID": 100115,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003227,
        "progress": 300,
        "equipment": _tools.ROList([[80115001, 6, 5], [80125001, 6, 5], [80135001, 6, 5]]),
        "props": None
    }),
    100116: _tools.RODict({
        "ID": 100116,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003231,
        "progress": 300,
        "equipment": _tools.ROList([[80115002, 6, 5], [80125002, 6, 5], [80135002, 6, 5]]),
        "props": None
    }),
    100117: _tools.RODict({
        "ID": 100117,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003235,
        "progress": 300,
        "equipment": _tools.ROList([[80215001, 6, 5], [80225001, 6, 5], [80235001, 6, 5]]),
        "props": None
    }),
    100118: _tools.RODict({
        "ID": 100118,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003211,
        "progress": 300,
        "equipment": _tools.ROList([[80215002, 6, 5], [80225002, 6, 5], [80235002, 6, 5]]),
        "props": None
    }),
    100119: _tools.RODict({
        "ID": 100119,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003212,
        "progress": 300,
        "equipment": _tools.ROList([[80315001, 6, 5], [80325001, 6, 5], [80335001, 6, 5]]),
        "props": None
    }),
    100120: _tools.RODict({
        "ID": 100120,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003213,
        "progress": 300,
        "equipment": _tools.ROList([[80415001, 6, 5], [80425001, 6, 5], [80435001, 6, 5]]),
        "props": None
    }),
    100121: _tools.RODict({
        "ID": 100121,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003214,
        "progress": 300,
        "equipment": _tools.ROList([[80585001, 6, 5]]),
        "props": _tools.ROList([30000296, 30000297, 30000298])
    }),
    100122: _tools.RODict({
        "ID": 100122,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003215,
        "progress": 300,
        "equipment": _tools.ROList([[80685001, 6, 5], [80785001, 6, 5]]),
        "props": None
    }),
    100123: _tools.RODict({
        "ID": 100123,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003237,
        "progress": 300,
        "equipment": _tools.ROList([[80695001, 6, 5], [80795001, 6, 5]]),
        "props": None
    }),
    100124: _tools.RODict({
        "ID": 100124,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003239,
        "progress": 300,
        "equipment": _tools.ROList([[80705002, 6, 5], [80805001, 6, 5]]),
        "props": None
    }),
    100125: _tools.RODict({
        "ID": 100125,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003208,
        "progress": 300,
        "equipment": None,
        "props": _tools.ROList([30990142, 30990147, 30990148])
    }),
    100126: _tools.RODict({
        "ID": 100126,
        "type1": 0,
        "unavailableClass": _tools.ROList([1001]),
        "prop": 52003210,
        "progress": 300,
        "equipment": None,
        "props": _tools.ROList([30990143, 30990144, 30990145, 30990146])
    }),
    100127: _tools.RODict({
        "ID": 100127,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003181,
        "progress": 10,
        "equipment": _tools.ROList([[80111001, 0, 1], [80121001, 0, 1], [80131001, 0, 1]]),
        "props": None
    }),
    100128: _tools.RODict({
        "ID": 100128,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003185,
        "progress": 10,
        "equipment": _tools.ROList([[80211001, 0, 1], [80221001, 0, 1], [80231001, 0, 1]]),
        "props": None
    }),
    100129: _tools.RODict({
        "ID": 100129,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003189,
        "progress": 10,
        "equipment": _tools.ROList([[80311001, 0, 1], [80321001, 0, 1], [80331001, 0, 1]]),
        "props": None
    }),
    100130: _tools.RODict({
        "ID": 100130,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003193,
        "progress": 10,
        "equipment": _tools.ROList([[80411001, 0, 1], [80421001, 0, 1], [80431001, 0, 1]]),
        "props": None
    }),
    100131: _tools.RODict({
        "ID": 100131,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003197,
        "progress": 10,
        "equipment": _tools.ROList([[80581001, 0, 1]]),
        "props": _tools.ROList([30000287, 30000288, 30000289])
    }),
    100132: _tools.RODict({
        "ID": 100132,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003201,
        "progress": 12,
        "equipment": _tools.ROList([[80111002, 0, 1], [80121002, 0, 1], [80131002, 0, 1]]),
        "props": None
    }),
    100133: _tools.RODict({
        "ID": 100133,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003205,
        "progress": 12,
        "equipment": _tools.ROList([[80211002, 0, 1], [80221002, 0, 1], [80231002, 0, 1]]),
        "props": None
    }),
    100134: _tools.RODict({
        "ID": 100134,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003209,
        "progress": 12,
        "equipment": _tools.ROList([[80311002, 0, 1], [80321002, 0, 1], [80331002, 0, 1]]),
        "props": None
    }),
    100135: _tools.RODict({
        "ID": 100135,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003211,
        "progress": 12,
        "equipment": _tools.ROList([[80411002, 0, 1], [80421002, 0, 1], [80431002, 0, 1]]),
        "props": None
    }),
    100136: _tools.RODict({
        "ID": 100136,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003212,
        "progress": 12,
        "equipment": _tools.ROList([[80581002, 0, 1]]),
        "props": _tools.ROList([30000287, 30000288, 30000289])
    }),
    100137: _tools.RODict({
        "ID": 100137,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003213,
        "progress": 14,
        "equipment": _tools.ROList([[80111003, 0, 1], [80121003, 0, 1], [80131003, 0, 1]]),
        "props": None
    }),
    100138: _tools.RODict({
        "ID": 100138,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003214,
        "progress": 14,
        "equipment": _tools.ROList([[80211003, 0, 1], [80221003, 0, 1], [80231003, 0, 1]]),
        "props": None
    }),
    100139: _tools.RODict({
        "ID": 100139,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003215,
        "progress": 14,
        "equipment": _tools.ROList([[80311003, 0, 1], [80321003, 0, 1], [80331003, 0, 1]]),
        "props": None
    }),
    100140: _tools.RODict({
        "ID": 100140,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003216,
        "progress": 14,
        "equipment": _tools.ROList([[80411003, 0, 1], [80421003, 0, 1], [80431003, 0, 1]]),
        "props": None
    }),
    100141: _tools.RODict({
        "ID": 100141,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003218,
        "progress": 14,
        "equipment": _tools.ROList([[80581003, 0, 1]]),
        "props": _tools.ROList([30000287, 30000288, 30000289])
    }),
    100142: _tools.RODict({
        "ID": 100142,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003220,
        "progress": 20,
        "equipment": _tools.ROList([[80112001, 0, 2], [80122001, 0, 2], [80132001, 0, 2]]),
        "props": None
    }),
    100143: _tools.RODict({
        "ID": 100143,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003224,
        "progress": 20,
        "equipment": _tools.ROList([[80212001, 0, 2], [80222001, 0, 2], [80232001, 0, 2]]),
        "props": None
    }),
    100144: _tools.RODict({
        "ID": 100144,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003228,
        "progress": 20,
        "equipment": _tools.ROList([[80312001, 0, 2], [80322001, 0, 2], [80332001, 0, 2]]),
        "props": None
    }),
    100145: _tools.RODict({
        "ID": 100145,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003232,
        "progress": 20,
        "equipment": _tools.ROList([[80412001, 0, 2], [80422001, 0, 2], [80432001, 0, 2]]),
        "props": None
    }),
    100146: _tools.RODict({
        "ID": 100146,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003236,
        "progress": 20,
        "equipment": _tools.ROList([[80582001, 0, 2]]),
        "props": _tools.ROList([30000290, 30000291, 30000292])
    }),
    100147: _tools.RODict({
        "ID": 100147,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003238,
        "progress": 20,
        "equipment": _tools.ROList([[80682001, 0, 2], [80782001, 0, 2]]),
        "props": None
    }),
    100148: _tools.RODict({
        "ID": 100148,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003181,
        "progress": 20,
        "equipment": _tools.ROList([[80692001, 0, 2], [80792001, 0, 2]]),
        "props": None
    }),
    100149: _tools.RODict({
        "ID": 100149,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003205,
        "progress": 20,
        "equipment": None,
        "props": _tools.ROList([30990121, 30990126, 30990127])
    }),
    100150: _tools.RODict({
        "ID": 100150,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003209,
        "progress": 20,
        "equipment": None,
        "props": _tools.ROList([30990122, 30990123, 30990124, 30990125])
    }),
    100151: _tools.RODict({
        "ID": 100151,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003185,
        "progress": 24,
        "equipment": _tools.ROList([[80112002, 1, 2], [80122002, 1, 2], [80132002, 1, 2]]),
        "props": None
    }),
    100152: _tools.RODict({
        "ID": 100152,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003189,
        "progress": 24,
        "equipment": _tools.ROList([[80212002, 1, 2], [80222002, 1, 2], [80232002, 1, 2]]),
        "props": None
    }),
    100153: _tools.RODict({
        "ID": 100153,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003193,
        "progress": 24,
        "equipment": _tools.ROList([[80312002, 1, 2], [80322002, 1, 2], [80332002, 1, 2]]),
        "props": None
    }),
    100154: _tools.RODict({
        "ID": 100154,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003197,
        "progress": 24,
        "equipment": _tools.ROList([[80412002, 1, 2], [80422002, 1, 2], [80432002, 1, 2]]),
        "props": None
    }),
    100155: _tools.RODict({
        "ID": 100155,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003201,
        "progress": 24,
        "equipment": _tools.ROList([[80582002, 1, 2]]),
        "props": _tools.ROList([30000290, 30000291, 30000292])
    }),
    100156: _tools.RODict({
        "ID": 100156,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003205,
        "progress": 24,
        "equipment": _tools.ROList([[80682002, 1, 2], [80782002, 1, 2]]),
        "props": None
    }),
    100157: _tools.RODict({
        "ID": 100157,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003209,
        "progress": 24,
        "equipment": _tools.ROList([[80692002, 1, 2], [80792002, 1, 2]]),
        "props": None
    }),
    100158: _tools.RODict({
        "ID": 100158,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003211,
        "progress": 28,
        "equipment": _tools.ROList([[80112003, 1, 2], [80122003, 1, 2], [80132003, 1, 2]]),
        "props": None
    }),
    100159: _tools.RODict({
        "ID": 100159,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003212,
        "progress": 28,
        "equipment": _tools.ROList([[80212003, 1, 2], [80222003, 1, 2], [80232003, 1, 2]]),
        "props": None
    }),
    100160: _tools.RODict({
        "ID": 100160,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003213,
        "progress": 28,
        "equipment": _tools.ROList([[80312003, 1, 2], [80322003, 1, 2], [80332003, 1, 2]]),
        "props": None
    }),
    100161: _tools.RODict({
        "ID": 100161,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003214,
        "progress": 28,
        "equipment": _tools.ROList([[80412003, 1, 2], [80422003, 1, 2], [80432003, 1, 2]]),
        "props": None
    }),
    100162: _tools.RODict({
        "ID": 100162,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003215,
        "progress": 28,
        "equipment": _tools.ROList([[80582003, 1, 2]]),
        "props": _tools.ROList([30000290, 30000291, 30000292])
    }),
    100163: _tools.RODict({
        "ID": 100163,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003216,
        "progress": 28,
        "equipment": _tools.ROList([[80682003, 1, 2], [80782003, 1, 2]]),
        "props": None
    }),
    100164: _tools.RODict({
        "ID": 100164,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003218,
        "progress": 28,
        "equipment": _tools.ROList([[80692003, 1, 2], [80792003, 1, 2]]),
        "props": None
    }),
    100165: _tools.RODict({
        "ID": 100165,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003220,
        "progress": 32,
        "equipment": _tools.ROList([[80112004, 2, 2], [80122004, 2, 2], [80132004, 2, 2]]),
        "props": None
    }),
    100166: _tools.RODict({
        "ID": 100166,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003224,
        "progress": 32,
        "equipment": _tools.ROList([[80212004, 2, 2], [80222004, 2, 2], [80232004, 2, 2]]),
        "props": None
    }),
    100167: _tools.RODict({
        "ID": 100167,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003228,
        "progress": 32,
        "equipment": _tools.ROList([[80312004, 2, 2], [80322004, 2, 2], [80332004, 2, 2]]),
        "props": None
    }),
    100168: _tools.RODict({
        "ID": 100168,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003232,
        "progress": 32,
        "equipment": _tools.ROList([[80412004, 2, 2], [80422004, 2, 2], [80432004, 2, 2]]),
        "props": None
    }),
    100169: _tools.RODict({
        "ID": 100169,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003236,
        "progress": 32,
        "equipment": _tools.ROList([[80582004, 2, 2]]),
        "props": _tools.ROList([30000290, 30000291, 30000292])
    }),
    100170: _tools.RODict({
        "ID": 100170,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003238,
        "progress": 32,
        "equipment": _tools.ROList([[80682004, 2, 2], [80782004, 2, 2]]),
        "props": None
    }),
    100171: _tools.RODict({
        "ID": 100171,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003181,
        "progress": 32,
        "equipment": _tools.ROList([[80692004, 2, 2], [80792004, 2, 2]]),
        "props": None
    }),
    100172: _tools.RODict({
        "ID": 100172,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003182,
        "progress": 60,
        "equipment": _tools.ROList([[80113001, 2, 3], [80123001, 2, 3], [80133001, 2, 3]]),
        "props": None
    }),
    100173: _tools.RODict({
        "ID": 100173,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003186,
        "progress": 60,
        "equipment": _tools.ROList([[80213001, 2, 3], [80223001, 2, 3], [80233001, 2, 3]]),
        "props": None
    }),
    100174: _tools.RODict({
        "ID": 100174,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003190,
        "progress": 60,
        "equipment": _tools.ROList([[80313001, 2, 3], [80323001, 2, 3], [80333001, 2, 3]]),
        "props": None
    }),
    100175: _tools.RODict({
        "ID": 100175,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003194,
        "progress": 60,
        "equipment": _tools.ROList([[80413001, 2, 3], [80423001, 2, 3], [80433001, 2, 3]]),
        "props": None
    }),
    100176: _tools.RODict({
        "ID": 100176,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003198,
        "progress": 60,
        "equipment": _tools.ROList([[80583001, 2, 3]]),
        "props": _tools.ROList([30000293, 30000294, 30000295])
    }),
    100177: _tools.RODict({
        "ID": 100177,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003202,
        "progress": 60,
        "equipment": _tools.ROList([[80683001, 2, 3], [80783001, 2, 3]]),
        "props": None
    }),
    100178: _tools.RODict({
        "ID": 100178,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003206,
        "progress": 60,
        "equipment": _tools.ROList([[80693001, 2, 3], [80793001, 2, 3]]),
        "props": None
    }),
    100179: _tools.RODict({
        "ID": 100179,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003206,
        "progress": 60,
        "equipment": None,
        "props": _tools.ROList([30990128, 30990133, 30990134])
    }),
    100180: _tools.RODict({
        "ID": 100180,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003209,
        "progress": 60,
        "equipment": None,
        "props": _tools.ROList([30990129, 30990130, 30990131, 30990132])
    }),
    100181: _tools.RODict({
        "ID": 100181,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003221,
        "progress": 66,
        "equipment": _tools.ROList([[80113002, 3, 3], [80123002, 3, 3], [80133002, 3, 3]]),
        "props": None
    }),
    100182: _tools.RODict({
        "ID": 100182,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003225,
        "progress": 66,
        "equipment": _tools.ROList([[80213002, 3, 3], [80223002, 3, 3], [80233002, 3, 3]]),
        "props": None
    }),
    100183: _tools.RODict({
        "ID": 100183,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003229,
        "progress": 66,
        "equipment": _tools.ROList([[80313002, 3, 3], [80323002, 3, 3], [80333002, 3, 3]]),
        "props": None
    }),
    100184: _tools.RODict({
        "ID": 100184,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003233,
        "progress": 66,
        "equipment": _tools.ROList([[80413002, 3, 3], [80423002, 3, 3], [80433002, 3, 3]]),
        "props": None
    }),
    100185: _tools.RODict({
        "ID": 100185,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003183,
        "progress": 66,
        "equipment": _tools.ROList([[80583002, 3, 3]]),
        "props": _tools.ROList([30000293, 30000294, 30000295])
    }),
    100186: _tools.RODict({
        "ID": 100186,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003187,
        "progress": 66,
        "equipment": _tools.ROList([[80683002, 3, 3], [80783002, 3, 3]]),
        "props": None
    }),
    100187: _tools.RODict({
        "ID": 100187,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003191,
        "progress": 66,
        "equipment": _tools.ROList([[80693002, 3, 3], [80793002, 3, 3]]),
        "props": None
    }),
    100188: _tools.RODict({
        "ID": 100188,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003195,
        "progress": 72,
        "equipment": _tools.ROList([[80113003, 3, 3], [80123003, 3, 3], [80133003, 3, 3]]),
        "props": None
    }),
    100189: _tools.RODict({
        "ID": 100189,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003199,
        "progress": 72,
        "equipment": _tools.ROList([[80213003, 3, 3], [80223003, 3, 3], [80233003, 3, 3]]),
        "props": None
    }),
    100190: _tools.RODict({
        "ID": 100190,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003203,
        "progress": 72,
        "equipment": _tools.ROList([[80313003, 3, 3], [80323003, 3, 3], [80333003, 3, 3]]),
        "props": None
    }),
    100191: _tools.RODict({
        "ID": 100191,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003207,
        "progress": 72,
        "equipment": _tools.ROList([[80413003, 3, 3], [80423003, 3, 3], [80433003, 3, 3]]),
        "props": None
    }),
    100192: _tools.RODict({
        "ID": 100192,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003210,
        "progress": 72,
        "equipment": _tools.ROList([[80583003, 3, 3]]),
        "props": _tools.ROList([30000293, 30000294, 30000295])
    }),
    100193: _tools.RODict({
        "ID": 100193,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003217,
        "progress": 72,
        "equipment": _tools.ROList([[80683003, 3, 3], [80783003, 3, 3]]),
        "props": None
    }),
    100194: _tools.RODict({
        "ID": 100194,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003219,
        "progress": 72,
        "equipment": _tools.ROList([[80693003, 3, 3], [80793003, 3, 3]]),
        "props": None
    }),
    100195: _tools.RODict({
        "ID": 100195,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003222,
        "progress": 78,
        "equipment": _tools.ROList([[80113004, 3, 3], [80123004, 3, 3], [80133004, 3, 3]]),
        "props": None
    }),
    100196: _tools.RODict({
        "ID": 100196,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003226,
        "progress": 78,
        "equipment": _tools.ROList([[80213004, 3, 3], [80223004, 3, 3], [80233004, 3, 3]]),
        "props": None
    }),
    100197: _tools.RODict({
        "ID": 100197,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003230,
        "progress": 78,
        "equipment": _tools.ROList([[80313004, 3, 3], [80323004, 3, 3], [80333004, 3, 3]]),
        "props": None
    }),
    100198: _tools.RODict({
        "ID": 100198,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003234,
        "progress": 78,
        "equipment": _tools.ROList([[80413004, 3, 3], [80423004, 3, 3], [80433004, 3, 3]]),
        "props": None
    }),
    100199: _tools.RODict({
        "ID": 100199,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003209,
        "progress": 78,
        "equipment": _tools.ROList([[80583004, 3, 3]]),
        "props": _tools.ROList([30000293, 30000294, 30000295])
    }),
    100200: _tools.RODict({
        "ID": 100200,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003211,
        "progress": 78,
        "equipment": _tools.ROList([[80683004, 4, 3], [80783004, 4, 3]]),
        "props": None
    }),
    100201: _tools.RODict({
        "ID": 100201,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003212,
        "progress": 78,
        "equipment": _tools.ROList([[80693004, 4, 3], [80793004, 4, 3]]),
        "props": None
    }),
    100202: _tools.RODict({
        "ID": 100202,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003213,
        "progress": 84,
        "equipment": _tools.ROList([[80113005, 4, 3], [80123005, 4, 3], [80133005, 4, 3]]),
        "props": None
    }),
    100203: _tools.RODict({
        "ID": 100203,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003214,
        "progress": 84,
        "equipment": _tools.ROList([[80213005, 4, 3], [80223005, 4, 3], [80233005, 4, 3]]),
        "props": None
    }),
    100204: _tools.RODict({
        "ID": 100204,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003215,
        "progress": 84,
        "equipment": _tools.ROList([[80313005, 4, 3], [80323005, 4, 3], [80333005, 4, 3]]),
        "props": None
    }),
    100205: _tools.RODict({
        "ID": 100205,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003211,
        "progress": 84,
        "equipment": _tools.ROList([[80413005, 4, 3], [80423005, 4, 3], [80433005, 4, 3]]),
        "props": None
    }),
    100206: _tools.RODict({
        "ID": 100206,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003212,
        "progress": 84,
        "equipment": _tools.ROList([[80583005, 4, 3]]),
        "props": _tools.ROList([30000293, 30000294, 30000295])
    }),
    100207: _tools.RODict({
        "ID": 100207,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003237,
        "progress": 84,
        "equipment": _tools.ROList([[80683005, 4, 3], [80783005, 4, 3]]),
        "props": None
    }),
    100208: _tools.RODict({
        "ID": 100208,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003239,
        "progress": 84,
        "equipment": _tools.ROList([[80693005, 4, 3], [80793005, 4, 3]]),
        "props": None
    }),
    100209: _tools.RODict({
        "ID": 100209,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003213,
        "progress": 180,
        "equipment": _tools.ROList([[80114001, 4, 4], [80124001, 4, 4], [80134001, 4, 4]]),
        "props": None
    }),
    100210: _tools.RODict({
        "ID": 100210,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003214,
        "progress": 180,
        "equipment": _tools.ROList([[80214005, 4, 4], [80224005, 4, 4], [80234005, 4, 4]]),
        "props": None
    }),
    100211: _tools.RODict({
        "ID": 100211,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003217,
        "progress": 180,
        "equipment": _tools.ROList([[80214001, 4, 4], [80224001, 4, 4], [80234001, 4, 4]]),
        "props": None
    }),
    100212: _tools.RODict({
        "ID": 100212,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003219,
        "progress": 180,
        "equipment": _tools.ROList([[80214005, 4, 4], [80224005, 4, 4], [80234005, 4, 4]]),
        "props": None
    }),
    100213: _tools.RODict({
        "ID": 100213,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003237,
        "progress": 180,
        "equipment": _tools.ROList([[80314001, 4, 4], [80324001, 4, 4], [80334001, 4, 4]]),
        "props": None
    }),
    100214: _tools.RODict({
        "ID": 100214,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003239,
        "progress": 180,
        "equipment": _tools.ROList([[80414001, 4, 4], [80424001, 4, 4], [80434001, 4, 4]]),
        "props": None
    }),
    100215: _tools.RODict({
        "ID": 100215,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003183,
        "progress": 180,
        "equipment": _tools.ROList([[80584001, 4, 4]]),
        "props": _tools.ROList([30000296, 30000297, 30000298])
    }),
    100216: _tools.RODict({
        "ID": 100216,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003187,
        "progress": 180,
        "equipment": _tools.ROList([[80684001, 4, 4], [80784001, 4, 4]]),
        "props": None
    }),
    100217: _tools.RODict({
        "ID": 100217,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003191,
        "progress": 180,
        "equipment": _tools.ROList([[80694001, 4, 4], [80794001, 4, 4]]),
        "props": None
    }),
    100218: _tools.RODict({
        "ID": 100218,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003195,
        "progress": 180,
        "equipment": _tools.ROList([[80704001, 4, 4], [80804001, 4, 4]]),
        "props": None
    }),
    100219: _tools.RODict({
        "ID": 100219,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003207,
        "progress": 180,
        "equipment": None,
        "props": _tools.ROList([30990135, 30990140, 30990141])
    }),
    100220: _tools.RODict({
        "ID": 100220,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003210,
        "progress": 180,
        "equipment": None,
        "props": _tools.ROList([30990136, 30990137, 30990138, 30990139])
    }),
    100221: _tools.RODict({
        "ID": 100221,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003199,
        "progress": 188,
        "equipment": _tools.ROList([[80114002, 5, 4], [80124002, 5, 4], [80134002, 5, 4]]),
        "props": None
    }),
    100222: _tools.RODict({
        "ID": 100222,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003203,
        "progress": 188,
        "equipment": _tools.ROList([[80114006, 5, 4], [80124006, 5, 4], [80134006, 5, 4]]),
        "props": None
    }),
    100223: _tools.RODict({
        "ID": 100223,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003207,
        "progress": 188,
        "equipment": _tools.ROList([[80214002, 5, 4], [80224002, 5, 4], [80234002, 5, 4]]),
        "props": None
    }),
    100224: _tools.RODict({
        "ID": 100224,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003210,
        "progress": 188,
        "equipment": _tools.ROList([[80214006, 5, 4], [80224006, 5, 4], [80234006, 5, 4]]),
        "props": None
    }),
    100225: _tools.RODict({
        "ID": 100225,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003217,
        "progress": 188,
        "equipment": _tools.ROList([[80314002, 5, 4], [80324002, 5, 4], [80334002, 5, 4]]),
        "props": None
    }),
    100226: _tools.RODict({
        "ID": 100226,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003219,
        "progress": 188,
        "equipment": _tools.ROList([[80414002, 5, 4], [80424002, 5, 4], [80434002, 5, 4]]),
        "props": None
    }),
    100227: _tools.RODict({
        "ID": 100227,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003222,
        "progress": 188,
        "equipment": _tools.ROList([[80584002, 5, 4]]),
        "props": _tools.ROList([30000296, 30000297, 30000298])
    }),
    100228: _tools.RODict({
        "ID": 100228,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003226,
        "progress": 188,
        "equipment": _tools.ROList([[80684002, 5, 4], [80784002, 5, 4]]),
        "props": None
    }),
    100229: _tools.RODict({
        "ID": 100229,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003230,
        "progress": 188,
        "equipment": _tools.ROList([[80693002, 5, 4], [80793002, 5, 4]]),
        "props": None
    }),
    100230: _tools.RODict({
        "ID": 100230,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003234,
        "progress": 188,
        "equipment": _tools.ROList([[80703002, 5, 4], [80803002, 5, 4]]),
        "props": None
    }),
    100231: _tools.RODict({
        "ID": 100231,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003237,
        "progress": 196,
        "equipment": _tools.ROList([[80114003, 5, 4], [80124003, 5, 4], [80134003, 5, 4]]),
        "props": None
    }),
    100232: _tools.RODict({
        "ID": 100232,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003239,
        "progress": 196,
        "equipment": _tools.ROList([[80114007, 5, 4], [80124007, 5, 4], [80134007, 5, 4]]),
        "props": None
    }),
    100233: _tools.RODict({
        "ID": 100233,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003184,
        "progress": 196,
        "equipment": _tools.ROList([[80214003, 5, 4], [80224003, 5, 4], [80234003, 5, 4]]),
        "props": None
    }),
    100234: _tools.RODict({
        "ID": 100234,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003188,
        "progress": 196,
        "equipment": _tools.ROList([[80214007, 5, 4], [80224007, 5, 4], [80234007, 5, 4]]),
        "props": None
    }),
    100235: _tools.RODict({
        "ID": 100235,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003192,
        "progress": 196,
        "equipment": _tools.ROList([[80314003, 5, 4], [80324003, 5, 4], [80334003, 5, 4]]),
        "props": None
    }),
    100236: _tools.RODict({
        "ID": 100236,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003196,
        "progress": 196,
        "equipment": _tools.ROList([[80414003, 5, 4], [80424003, 5, 4], [80434003, 5, 4]]),
        "props": None
    }),
    100237: _tools.RODict({
        "ID": 100237,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003200,
        "progress": 196,
        "equipment": _tools.ROList([[80584003, 5, 4]]),
        "props": _tools.ROList([30000296, 30000297, 30000298])
    }),
    100238: _tools.RODict({
        "ID": 100238,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003204,
        "progress": 196,
        "equipment": _tools.ROList([[80684003, 5, 4], [80784003, 5, 4]]),
        "props": None
    }),
    100239: _tools.RODict({
        "ID": 100239,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003208,
        "progress": 196,
        "equipment": _tools.ROList([[80694003, 5, 4], [80794003, 5, 4]]),
        "props": None
    }),
    100240: _tools.RODict({
        "ID": 100240,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003223,
        "progress": 196,
        "equipment": _tools.ROList([[80704003, 5, 4], [80804003, 5, 4]]),
        "props": None
    }),
    100241: _tools.RODict({
        "ID": 100241,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003227,
        "progress": 300,
        "equipment": _tools.ROList([[80115001, 6, 5], [80125001, 6, 5], [80135001, 6, 5]]),
        "props": None
    }),
    100242: _tools.RODict({
        "ID": 100242,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003231,
        "progress": 300,
        "equipment": _tools.ROList([[80115002, 6, 5], [80125002, 6, 5], [80135002, 6, 5]]),
        "props": None
    }),
    100243: _tools.RODict({
        "ID": 100243,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003235,
        "progress": 300,
        "equipment": _tools.ROList([[80215001, 6, 5], [80225001, 6, 5], [80235001, 6, 5]]),
        "props": None
    }),
    100244: _tools.RODict({
        "ID": 100244,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003211,
        "progress": 300,
        "equipment": _tools.ROList([[80215002, 6, 5], [80225002, 6, 5], [80235002, 6, 5]]),
        "props": None
    }),
    100245: _tools.RODict({
        "ID": 100245,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003212,
        "progress": 300,
        "equipment": _tools.ROList([[80315001, 6, 5], [80325001, 6, 5], [80335001, 6, 5]]),
        "props": None
    }),
    100246: _tools.RODict({
        "ID": 100246,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003213,
        "progress": 300,
        "equipment": _tools.ROList([[80415001, 6, 5], [80425001, 6, 5], [80435001, 6, 5]]),
        "props": None
    }),
    100247: _tools.RODict({
        "ID": 100247,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003214,
        "progress": 300,
        "equipment": _tools.ROList([[80585001, 6, 5]]),
        "props": _tools.ROList([30000296, 30000297, 30000298])
    }),
    100248: _tools.RODict({
        "ID": 100248,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003215,
        "progress": 300,
        "equipment": _tools.ROList([[80685001, 6, 5], [80785001, 6, 5]]),
        "props": None
    }),
    100249: _tools.RODict({
        "ID": 100249,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003237,
        "progress": 300,
        "equipment": _tools.ROList([[80695001, 6, 5], [80795001, 6, 5]]),
        "props": None
    }),
    100250: _tools.RODict({
        "ID": 100250,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003239,
        "progress": 300,
        "equipment": _tools.ROList([[80705002, 6, 5], [80805001, 6, 5]]),
        "props": None
    }),
    100251: _tools.RODict({
        "ID": 100251,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003208,
        "progress": 300,
        "equipment": None,
        "props": _tools.ROList([30990142, 30990147, 30990148])
    }),
    100252: _tools.RODict({
        "ID": 100252,
        "type1": 1,
        "unavailableClass": _tools.ROList([1002]),
        "prop": 52003210,
        "progress": 300,
        "equipment": None,
        "props": _tools.ROList([30990143, 30990144, 30990145, 30990146])
    }),
    100253: _tools.RODict({
        "ID": 100253,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003181,
        "progress": 10,
        "equipment": _tools.ROList([[80111001, 0, 1], [80121001, 0, 1], [80131001, 0, 1]]),
        "props": None
    }),
    100254: _tools.RODict({
        "ID": 100254,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003185,
        "progress": 10,
        "equipment": _tools.ROList([[80211001, 0, 1], [80221001, 0, 1], [80231001, 0, 1]]),
        "props": None
    }),
    100255: _tools.RODict({
        "ID": 100255,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003189,
        "progress": 10,
        "equipment": _tools.ROList([[80311001, 0, 1], [80321001, 0, 1], [80331001, 0, 1]]),
        "props": None
    }),
    100256: _tools.RODict({
        "ID": 100256,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003193,
        "progress": 10,
        "equipment": _tools.ROList([[80411001, 0, 1], [80421001, 0, 1], [80431001, 0, 1]]),
        "props": None
    }),
    100257: _tools.RODict({
        "ID": 100257,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003197,
        "progress": 10,
        "equipment": _tools.ROList([[80581001, 0, 1]]),
        "props": _tools.ROList([30000287, 30000288, 30000289])
    }),
    100258: _tools.RODict({
        "ID": 100258,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003201,
        "progress": 12,
        "equipment": _tools.ROList([[80111002, 0, 1], [80121002, 0, 1], [80131002, 0, 1]]),
        "props": None
    }),
    100259: _tools.RODict({
        "ID": 100259,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003205,
        "progress": 12,
        "equipment": _tools.ROList([[80211002, 0, 1], [80221002, 0, 1], [80231002, 0, 1]]),
        "props": None
    }),
    100260: _tools.RODict({
        "ID": 100260,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003209,
        "progress": 12,
        "equipment": _tools.ROList([[80311002, 0, 1], [80321002, 0, 1], [80331002, 0, 1]]),
        "props": None
    }),
    100261: _tools.RODict({
        "ID": 100261,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003211,
        "progress": 12,
        "equipment": _tools.ROList([[80411002, 0, 1], [80421002, 0, 1], [80431002, 0, 1]]),
        "props": None
    }),
    100262: _tools.RODict({
        "ID": 100262,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003212,
        "progress": 12,
        "equipment": _tools.ROList([[80581002, 0, 1]]),
        "props": _tools.ROList([30000287, 30000288, 30000289])
    }),
    100263: _tools.RODict({
        "ID": 100263,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003213,
        "progress": 14,
        "equipment": _tools.ROList([[80111003, 0, 1], [80121003, 0, 1], [80131003, 0, 1]]),
        "props": None
    }),
    100264: _tools.RODict({
        "ID": 100264,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003214,
        "progress": 14,
        "equipment": _tools.ROList([[80211003, 0, 1], [80221003, 0, 1], [80231003, 0, 1]]),
        "props": None
    }),
    100265: _tools.RODict({
        "ID": 100265,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003215,
        "progress": 14,
        "equipment": _tools.ROList([[80311003, 0, 1], [80321003, 0, 1], [80331003, 0, 1]]),
        "props": None
    }),
    100266: _tools.RODict({
        "ID": 100266,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003216,
        "progress": 14,
        "equipment": _tools.ROList([[80411003, 0, 1], [80421003, 0, 1], [80431003, 0, 1]]),
        "props": None
    }),
    100267: _tools.RODict({
        "ID": 100267,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003218,
        "progress": 14,
        "equipment": _tools.ROList([[80581003, 0, 1]]),
        "props": _tools.ROList([30000287, 30000288, 30000289])
    }),
    100268: _tools.RODict({
        "ID": 100268,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003220,
        "progress": 20,
        "equipment": _tools.ROList([[80112001, 0, 2], [80122001, 0, 2], [80132001, 0, 2]]),
        "props": None
    }),
    100269: _tools.RODict({
        "ID": 100269,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003224,
        "progress": 20,
        "equipment": _tools.ROList([[80212001, 0, 2], [80222001, 0, 2], [80232001, 0, 2]]),
        "props": None
    }),
    100270: _tools.RODict({
        "ID": 100270,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003228,
        "progress": 20,
        "equipment": _tools.ROList([[80312001, 0, 2], [80322001, 0, 2], [80332001, 0, 2]]),
        "props": None
    }),
    100271: _tools.RODict({
        "ID": 100271,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003232,
        "progress": 20,
        "equipment": _tools.ROList([[80412001, 0, 2], [80422001, 0, 2], [80432001, 0, 2]]),
        "props": None
    }),
    100272: _tools.RODict({
        "ID": 100272,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003236,
        "progress": 20,
        "equipment": _tools.ROList([[80582001, 0, 2]]),
        "props": _tools.ROList([30000290, 30000291, 30000292])
    }),
    100273: _tools.RODict({
        "ID": 100273,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003238,
        "progress": 20,
        "equipment": _tools.ROList([[80682001, 0, 2], [80782001, 0, 2]]),
        "props": None
    }),
    100274: _tools.RODict({
        "ID": 100274,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003181,
        "progress": 20,
        "equipment": _tools.ROList([[80692001, 0, 2], [80792001, 0, 2]]),
        "props": None
    }),
    100275: _tools.RODict({
        "ID": 100275,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003205,
        "progress": 20,
        "equipment": None,
        "props": _tools.ROList([30990121, 30990126, 30990127])
    }),
    100276: _tools.RODict({
        "ID": 100276,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003209,
        "progress": 20,
        "equipment": None,
        "props": _tools.ROList([30990122, 30990123, 30990124, 30990125])
    }),
    100277: _tools.RODict({
        "ID": 100277,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003185,
        "progress": 24,
        "equipment": _tools.ROList([[80112002, 1, 2], [80122002, 1, 2], [80132002, 1, 2]]),
        "props": None
    }),
    100278: _tools.RODict({
        "ID": 100278,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003189,
        "progress": 24,
        "equipment": _tools.ROList([[80212002, 1, 2], [80222002, 1, 2], [80232002, 1, 2]]),
        "props": None
    }),
    100279: _tools.RODict({
        "ID": 100279,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003193,
        "progress": 24,
        "equipment": _tools.ROList([[80312002, 1, 2], [80322002, 1, 2], [80332002, 1, 2]]),
        "props": None
    }),
    100280: _tools.RODict({
        "ID": 100280,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003197,
        "progress": 24,
        "equipment": _tools.ROList([[80412002, 1, 2], [80422002, 1, 2], [80432002, 1, 2]]),
        "props": None
    }),
    100281: _tools.RODict({
        "ID": 100281,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003201,
        "progress": 24,
        "equipment": _tools.ROList([[80582002, 1, 2]]),
        "props": _tools.ROList([30000290, 30000291, 30000292])
    }),
    100282: _tools.RODict({
        "ID": 100282,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003205,
        "progress": 24,
        "equipment": _tools.ROList([[80682002, 1, 2], [80782002, 1, 2]]),
        "props": None
    }),
    100283: _tools.RODict({
        "ID": 100283,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003209,
        "progress": 24,
        "equipment": _tools.ROList([[80692002, 1, 2], [80792002, 1, 2]]),
        "props": None
    }),
    100284: _tools.RODict({
        "ID": 100284,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003211,
        "progress": 28,
        "equipment": _tools.ROList([[80112003, 1, 2], [80122003, 1, 2], [80132003, 1, 2]]),
        "props": None
    }),
    100285: _tools.RODict({
        "ID": 100285,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003212,
        "progress": 28,
        "equipment": _tools.ROList([[80212003, 1, 2], [80222003, 1, 2], [80232003, 1, 2]]),
        "props": None
    }),
    100286: _tools.RODict({
        "ID": 100286,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003213,
        "progress": 28,
        "equipment": _tools.ROList([[80312003, 1, 2], [80322003, 1, 2], [80332003, 1, 2]]),
        "props": None
    }),
    100287: _tools.RODict({
        "ID": 100287,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003214,
        "progress": 28,
        "equipment": _tools.ROList([[80412003, 1, 2], [80422003, 1, 2], [80432003, 1, 2]]),
        "props": None
    }),
    100288: _tools.RODict({
        "ID": 100288,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003215,
        "progress": 28,
        "equipment": _tools.ROList([[80582003, 1, 2]]),
        "props": _tools.ROList([30000290, 30000291, 30000292])
    }),
    100289: _tools.RODict({
        "ID": 100289,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003216,
        "progress": 28,
        "equipment": _tools.ROList([[80682003, 1, 2], [80782003, 1, 2]]),
        "props": None
    }),
    100290: _tools.RODict({
        "ID": 100290,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003218,
        "progress": 28,
        "equipment": _tools.ROList([[80692003, 1, 2], [80792003, 1, 2]]),
        "props": None
    }),
    100291: _tools.RODict({
        "ID": 100291,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003220,
        "progress": 32,
        "equipment": _tools.ROList([[80112004, 2, 2], [80122004, 2, 2], [80132004, 2, 2]]),
        "props": None
    }),
    100292: _tools.RODict({
        "ID": 100292,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003224,
        "progress": 32,
        "equipment": _tools.ROList([[80212004, 2, 2], [80222004, 2, 2], [80232004, 2, 2]]),
        "props": None
    }),
    100293: _tools.RODict({
        "ID": 100293,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003228,
        "progress": 32,
        "equipment": _tools.ROList([[80312004, 2, 2], [80322004, 2, 2], [80332004, 2, 2]]),
        "props": None
    }),
    100294: _tools.RODict({
        "ID": 100294,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003232,
        "progress": 32,
        "equipment": _tools.ROList([[80412004, 2, 2], [80422004, 2, 2], [80432004, 2, 2]]),
        "props": None
    }),
    100295: _tools.RODict({
        "ID": 100295,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003236,
        "progress": 32,
        "equipment": _tools.ROList([[80582004, 2, 2]]),
        "props": _tools.ROList([30000290, 30000291, 30000292])
    }),
    100296: _tools.RODict({
        "ID": 100296,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003238,
        "progress": 32,
        "equipment": _tools.ROList([[80682004, 2, 2], [80782004, 2, 2]]),
        "props": None
    }),
    100297: _tools.RODict({
        "ID": 100297,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003181,
        "progress": 32,
        "equipment": _tools.ROList([[80692004, 2, 2], [80792004, 2, 2]]),
        "props": None
    }),
    100298: _tools.RODict({
        "ID": 100298,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003182,
        "progress": 60,
        "equipment": _tools.ROList([[80113001, 2, 3], [80123001, 2, 3], [80133001, 2, 3]]),
        "props": None
    }),
    100299: _tools.RODict({
        "ID": 100299,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003186,
        "progress": 60,
        "equipment": _tools.ROList([[80213001, 2, 3], [80223001, 2, 3], [80233001, 2, 3]]),
        "props": None
    }),
    100300: _tools.RODict({
        "ID": 100300,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003190,
        "progress": 60,
        "equipment": _tools.ROList([[80313001, 2, 3], [80323001, 2, 3], [80333001, 2, 3]]),
        "props": None
    }),
    100301: _tools.RODict({
        "ID": 100301,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003194,
        "progress": 60,
        "equipment": _tools.ROList([[80413001, 2, 3], [80423001, 2, 3], [80433001, 2, 3]]),
        "props": None
    }),
    100302: _tools.RODict({
        "ID": 100302,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003198,
        "progress": 60,
        "equipment": _tools.ROList([[80583001, 2, 3]]),
        "props": _tools.ROList([30000293, 30000294, 30000295])
    }),
    100303: _tools.RODict({
        "ID": 100303,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003202,
        "progress": 60,
        "equipment": _tools.ROList([[80683001, 2, 3], [80783001, 2, 3]]),
        "props": None
    }),
    100304: _tools.RODict({
        "ID": 100304,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003206,
        "progress": 60,
        "equipment": _tools.ROList([[80693001, 2, 3], [80793001, 2, 3]]),
        "props": None
    }),
    100305: _tools.RODict({
        "ID": 100305,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003206,
        "progress": 60,
        "equipment": None,
        "props": _tools.ROList([30990128, 30990133, 30990134])
    }),
    100306: _tools.RODict({
        "ID": 100306,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003209,
        "progress": 60,
        "equipment": None,
        "props": _tools.ROList([30990129, 30990130, 30990131, 30990132])
    }),
    100307: _tools.RODict({
        "ID": 100307,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003221,
        "progress": 66,
        "equipment": _tools.ROList([[80113002, 3, 3], [80123002, 3, 3], [80133002, 3, 3]]),
        "props": None
    }),
    100308: _tools.RODict({
        "ID": 100308,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003225,
        "progress": 66,
        "equipment": _tools.ROList([[80213002, 3, 3], [80223002, 3, 3], [80233002, 3, 3]]),
        "props": None
    }),
    100309: _tools.RODict({
        "ID": 100309,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003229,
        "progress": 66,
        "equipment": _tools.ROList([[80313002, 3, 3], [80323002, 3, 3], [80333002, 3, 3]]),
        "props": None
    }),
    100310: _tools.RODict({
        "ID": 100310,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003233,
        "progress": 66,
        "equipment": _tools.ROList([[80413002, 3, 3], [80423002, 3, 3], [80433002, 3, 3]]),
        "props": None
    }),
    100311: _tools.RODict({
        "ID": 100311,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003183,
        "progress": 66,
        "equipment": _tools.ROList([[80583002, 3, 3]]),
        "props": _tools.ROList([30000293, 30000294, 30000295])
    }),
    100312: _tools.RODict({
        "ID": 100312,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003187,
        "progress": 66,
        "equipment": _tools.ROList([[80683002, 3, 3], [80783002, 3, 3]]),
        "props": None
    }),
    100313: _tools.RODict({
        "ID": 100313,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003191,
        "progress": 66,
        "equipment": _tools.ROList([[80693002, 3, 3], [80793002, 3, 3]]),
        "props": None
    }),
    100314: _tools.RODict({
        "ID": 100314,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003195,
        "progress": 72,
        "equipment": _tools.ROList([[80113003, 3, 3], [80123003, 3, 3], [80133003, 3, 3]]),
        "props": None
    }),
    100315: _tools.RODict({
        "ID": 100315,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003199,
        "progress": 72,
        "equipment": _tools.ROList([[80213003, 3, 3], [80223003, 3, 3], [80233003, 3, 3]]),
        "props": None
    }),
    100316: _tools.RODict({
        "ID": 100316,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003203,
        "progress": 72,
        "equipment": _tools.ROList([[80313003, 3, 3], [80323003, 3, 3], [80333003, 3, 3]]),
        "props": None
    }),
    100317: _tools.RODict({
        "ID": 100317,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003207,
        "progress": 72,
        "equipment": _tools.ROList([[80413003, 3, 3], [80423003, 3, 3], [80433003, 3, 3]]),
        "props": None
    }),
    100318: _tools.RODict({
        "ID": 100318,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003210,
        "progress": 72,
        "equipment": _tools.ROList([[80583003, 3, 3]]),
        "props": _tools.ROList([30000293, 30000294, 30000295])
    }),
    100319: _tools.RODict({
        "ID": 100319,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003217,
        "progress": 72,
        "equipment": _tools.ROList([[80683003, 3, 3], [80783003, 3, 3]]),
        "props": None
    }),
    100320: _tools.RODict({
        "ID": 100320,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003219,
        "progress": 72,
        "equipment": _tools.ROList([[80693003, 3, 3], [80793003, 3, 3]]),
        "props": None
    }),
    100321: _tools.RODict({
        "ID": 100321,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003222,
        "progress": 78,
        "equipment": _tools.ROList([[80113004, 3, 3], [80123004, 3, 3], [80133004, 3, 3]]),
        "props": None
    }),
    100322: _tools.RODict({
        "ID": 100322,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003226,
        "progress": 78,
        "equipment": _tools.ROList([[80213004, 3, 3], [80223004, 3, 3], [80233004, 3, 3]]),
        "props": None
    }),
    100323: _tools.RODict({
        "ID": 100323,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003230,
        "progress": 78,
        "equipment": _tools.ROList([[80313004, 3, 3], [80323004, 3, 3], [80333004, 3, 3]]),
        "props": None
    }),
    100324: _tools.RODict({
        "ID": 100324,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003234,
        "progress": 78,
        "equipment": _tools.ROList([[80413004, 3, 3], [80423004, 3, 3], [80433004, 3, 3]]),
        "props": None
    }),
    100325: _tools.RODict({
        "ID": 100325,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003209,
        "progress": 78,
        "equipment": _tools.ROList([[80583004, 3, 3]]),
        "props": _tools.ROList([30000293, 30000294, 30000295])
    }),
    100326: _tools.RODict({
        "ID": 100326,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003211,
        "progress": 78,
        "equipment": _tools.ROList([[80683004, 4, 3], [80783004, 4, 3]]),
        "props": None
    }),
    100327: _tools.RODict({
        "ID": 100327,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003212,
        "progress": 78,
        "equipment": _tools.ROList([[80693004, 4, 3], [80793004, 4, 3]]),
        "props": None
    }),
    100328: _tools.RODict({
        "ID": 100328,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003213,
        "progress": 84,
        "equipment": _tools.ROList([[80113005, 4, 3], [80123005, 4, 3], [80133005, 4, 3]]),
        "props": None
    }),
    100329: _tools.RODict({
        "ID": 100329,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003214,
        "progress": 84,
        "equipment": _tools.ROList([[80213005, 4, 3], [80223005, 4, 3], [80233005, 4, 3]]),
        "props": None
    }),
    100330: _tools.RODict({
        "ID": 100330,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003215,
        "progress": 84,
        "equipment": _tools.ROList([[80313005, 4, 3], [80323005, 4, 3], [80333005, 4, 3]]),
        "props": None
    }),
    100331: _tools.RODict({
        "ID": 100331,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003211,
        "progress": 84,
        "equipment": _tools.ROList([[80413005, 4, 3], [80423005, 4, 3], [80433005, 4, 3]]),
        "props": None
    }),
    100332: _tools.RODict({
        "ID": 100332,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003212,
        "progress": 84,
        "equipment": _tools.ROList([[80583005, 4, 3]]),
        "props": _tools.ROList([30000293, 30000294, 30000295])
    }),
    100333: _tools.RODict({
        "ID": 100333,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003237,
        "progress": 84,
        "equipment": _tools.ROList([[80683005, 4, 3], [80783005, 4, 3]]),
        "props": None
    }),
    100334: _tools.RODict({
        "ID": 100334,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003239,
        "progress": 84,
        "equipment": _tools.ROList([[80693005, 4, 3], [80793005, 4, 3]]),
        "props": None
    }),
    100335: _tools.RODict({
        "ID": 100335,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003213,
        "progress": 180,
        "equipment": _tools.ROList([[80114001, 4, 4], [80124001, 4, 4], [80134001, 4, 4]]),
        "props": None
    }),
    100336: _tools.RODict({
        "ID": 100336,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003214,
        "progress": 180,
        "equipment": _tools.ROList([[80214005, 4, 4], [80224005, 4, 4], [80234005, 4, 4]]),
        "props": None
    }),
    100337: _tools.RODict({
        "ID": 100337,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003217,
        "progress": 180,
        "equipment": _tools.ROList([[80214001, 4, 4], [80224001, 4, 4], [80234001, 4, 4]]),
        "props": None
    }),
    100338: _tools.RODict({
        "ID": 100338,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003219,
        "progress": 180,
        "equipment": _tools.ROList([[80214005, 4, 4], [80224005, 4, 4], [80234005, 4, 4]]),
        "props": None
    }),
    100339: _tools.RODict({
        "ID": 100339,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003237,
        "progress": 180,
        "equipment": _tools.ROList([[80314001, 4, 4], [80324001, 4, 4], [80334001, 4, 4]]),
        "props": None
    }),
    100340: _tools.RODict({
        "ID": 100340,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003239,
        "progress": 180,
        "equipment": _tools.ROList([[80414001, 4, 4], [80424001, 4, 4], [80434001, 4, 4]]),
        "props": None
    }),
    100341: _tools.RODict({
        "ID": 100341,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003183,
        "progress": 180,
        "equipment": _tools.ROList([[80584001, 4, 4]]),
        "props": _tools.ROList([30000296, 30000297, 30000298])
    }),
    100342: _tools.RODict({
        "ID": 100342,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003187,
        "progress": 180,
        "equipment": _tools.ROList([[80684001, 4, 4], [80784001, 4, 4]]),
        "props": None
    }),
    100343: _tools.RODict({
        "ID": 100343,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003191,
        "progress": 180,
        "equipment": _tools.ROList([[80694001, 4, 4], [80794001, 4, 4]]),
        "props": None
    }),
    100344: _tools.RODict({
        "ID": 100344,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003195,
        "progress": 180,
        "equipment": _tools.ROList([[80704001, 4, 4], [80804001, 4, 4]]),
        "props": None
    }),
    100345: _tools.RODict({
        "ID": 100345,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003207,
        "progress": 180,
        "equipment": None,
        "props": _tools.ROList([30990135, 30990140, 30990141])
    }),
    100346: _tools.RODict({
        "ID": 100346,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003210,
        "progress": 180,
        "equipment": None,
        "props": _tools.ROList([30990136, 30990137, 30990138, 30990139])
    }),
    100347: _tools.RODict({
        "ID": 100347,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003199,
        "progress": 188,
        "equipment": _tools.ROList([[80114002, 5, 4], [80124002, 5, 4], [80134002, 5, 4]]),
        "props": None
    }),
    100348: _tools.RODict({
        "ID": 100348,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003203,
        "progress": 188,
        "equipment": _tools.ROList([[80114006, 5, 4], [80124006, 5, 4], [80134006, 5, 4]]),
        "props": None
    }),
    100349: _tools.RODict({
        "ID": 100349,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003207,
        "progress": 188,
        "equipment": _tools.ROList([[80214002, 5, 4], [80224002, 5, 4], [80234002, 5, 4]]),
        "props": None
    }),
    100350: _tools.RODict({
        "ID": 100350,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003210,
        "progress": 188,
        "equipment": _tools.ROList([[80214006, 5, 4], [80224006, 5, 4], [80234006, 5, 4]]),
        "props": None
    }),
    100351: _tools.RODict({
        "ID": 100351,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003217,
        "progress": 188,
        "equipment": _tools.ROList([[80314002, 5, 4], [80324002, 5, 4], [80334002, 5, 4]]),
        "props": None
    }),
    100352: _tools.RODict({
        "ID": 100352,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003219,
        "progress": 188,
        "equipment": _tools.ROList([[80414002, 5, 4], [80424002, 5, 4], [80434002, 5, 4]]),
        "props": None
    }),
    100353: _tools.RODict({
        "ID": 100353,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003222,
        "progress": 188,
        "equipment": _tools.ROList([[80584002, 5, 4]]),
        "props": _tools.ROList([30000296, 30000297, 30000298])
    }),
    100354: _tools.RODict({
        "ID": 100354,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003226,
        "progress": 188,
        "equipment": _tools.ROList([[80684002, 5, 4], [80784002, 5, 4]]),
        "props": None
    }),
    100355: _tools.RODict({
        "ID": 100355,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003230,
        "progress": 188,
        "equipment": _tools.ROList([[80693002, 5, 4], [80793002, 5, 4]]),
        "props": None
    }),
    100356: _tools.RODict({
        "ID": 100356,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003234,
        "progress": 188,
        "equipment": _tools.ROList([[80703002, 5, 4], [80803002, 5, 4]]),
        "props": None
    }),
    100357: _tools.RODict({
        "ID": 100357,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003237,
        "progress": 196,
        "equipment": _tools.ROList([[80114003, 5, 4], [80124003, 5, 4], [80134003, 5, 4]]),
        "props": None
    }),
    100358: _tools.RODict({
        "ID": 100358,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003239,
        "progress": 196,
        "equipment": _tools.ROList([[80114007, 5, 4], [80124007, 5, 4], [80134007, 5, 4]]),
        "props": None
    }),
    100359: _tools.RODict({
        "ID": 100359,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003184,
        "progress": 196,
        "equipment": _tools.ROList([[80214003, 5, 4], [80224003, 5, 4], [80234003, 5, 4]]),
        "props": None
    }),
    100360: _tools.RODict({
        "ID": 100360,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003188,
        "progress": 196,
        "equipment": _tools.ROList([[80214007, 5, 4], [80224007, 5, 4], [80234007, 5, 4]]),
        "props": None
    }),
    100361: _tools.RODict({
        "ID": 100361,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003192,
        "progress": 196,
        "equipment": _tools.ROList([[80314003, 5, 4], [80324003, 5, 4], [80334003, 5, 4]]),
        "props": None
    }),
    100362: _tools.RODict({
        "ID": 100362,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003196,
        "progress": 196,
        "equipment": _tools.ROList([[80414003, 5, 4], [80424003, 5, 4], [80434003, 5, 4]]),
        "props": None
    }),
    100363: _tools.RODict({
        "ID": 100363,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003200,
        "progress": 196,
        "equipment": _tools.ROList([[80584003, 5, 4]]),
        "props": _tools.ROList([30000296, 30000297, 30000298])
    }),
    100364: _tools.RODict({
        "ID": 100364,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003204,
        "progress": 196,
        "equipment": _tools.ROList([[80684003, 5, 4], [80784003, 5, 4]]),
        "props": None
    }),
    100365: _tools.RODict({
        "ID": 100365,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003208,
        "progress": 196,
        "equipment": _tools.ROList([[80694003, 5, 4], [80794003, 5, 4]]),
        "props": None
    }),
    100366: _tools.RODict({
        "ID": 100366,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003223,
        "progress": 196,
        "equipment": _tools.ROList([[80704003, 5, 4], [80804003, 5, 4]]),
        "props": None
    }),
    100367: _tools.RODict({
        "ID": 100367,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003227,
        "progress": 300,
        "equipment": _tools.ROList([[80115001, 6, 5], [80125001, 6, 5], [80135001, 6, 5]]),
        "props": None
    }),
    100368: _tools.RODict({
        "ID": 100368,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003231,
        "progress": 300,
        "equipment": _tools.ROList([[80115002, 6, 5], [80125002, 6, 5], [80135002, 6, 5]]),
        "props": None
    }),
    100369: _tools.RODict({
        "ID": 100369,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003235,
        "progress": 300,
        "equipment": _tools.ROList([[80215001, 6, 5], [80225001, 6, 5], [80235001, 6, 5]]),
        "props": None
    }),
    100370: _tools.RODict({
        "ID": 100370,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003211,
        "progress": 300,
        "equipment": _tools.ROList([[80215002, 6, 5], [80225002, 6, 5], [80235002, 6, 5]]),
        "props": None
    }),
    100371: _tools.RODict({
        "ID": 100371,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003212,
        "progress": 300,
        "equipment": _tools.ROList([[80315001, 6, 5], [80325001, 6, 5], [80335001, 6, 5]]),
        "props": None
    }),
    100372: _tools.RODict({
        "ID": 100372,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003213,
        "progress": 300,
        "equipment": _tools.ROList([[80415001, 6, 5], [80425001, 6, 5], [80435001, 6, 5]]),
        "props": None
    }),
    100373: _tools.RODict({
        "ID": 100373,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003214,
        "progress": 300,
        "equipment": _tools.ROList([[80585001, 6, 5]]),
        "props": _tools.ROList([30000296, 30000297, 30000298])
    }),
    100374: _tools.RODict({
        "ID": 100374,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003215,
        "progress": 300,
        "equipment": _tools.ROList([[80685001, 6, 5], [80785001, 6, 5]]),
        "props": None
    }),
    100375: _tools.RODict({
        "ID": 100375,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003237,
        "progress": 300,
        "equipment": _tools.ROList([[80695001, 6, 5], [80795001, 6, 5]]),
        "props": None
    }),
    100376: _tools.RODict({
        "ID": 100376,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003239,
        "progress": 300,
        "equipment": _tools.ROList([[80705002, 6, 5], [80805001, 6, 5]]),
        "props": None
    }),
    100377: _tools.RODict({
        "ID": 100377,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003208,
        "progress": 300,
        "equipment": None,
        "props": _tools.ROList([30990142, 30990147, 30990148])
    }),
    100378: _tools.RODict({
        "ID": 100378,
        "type1": 2,
        "unavailableClass": _tools.ROList([1003]),
        "prop": 52003210,
        "progress": 300,
        "equipment": None,
        "props": _tools.ROList([30990143, 30990144, 30990145, 30990146])
    })
})
minKey = 100001
maxKey = 100378