# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: NPC/pickTimes
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    16000002: _tools.RODict({
        "ID": 16000002,
        "pickTimes": 1
    }),
    16000003: _tools.RODict({
        "ID": 16000003,
        "pickTimes": 1
    }),
    16000004: _tools.RODict({
        "ID": 16000004,
        "pickTimes": 1
    }),
    16000005: _tools.RODict({
        "ID": 16000005,
        "pickTimes": 1
    }),
    16000027: _tools.RODict({
        "ID": 16000027,
        "pickTimes": 1
    }),
    16000028: _tools.RODict({
        "ID": 16000028,
        "pickTimes": 1
    }),
    16000029: _tools.RODict({
        "ID": 16000029,
        "pickTimes": 0
    }),
    16000040: _tools.RODict({
        "ID": 16000040,
        "pickTimes": 1
    }),
    16000041: _tools.RODict({
        "ID": 16000041,
        "pickTimes": 1
    }),
    16000042: _tools.RODict({
        "ID": 16000042,
        "pickTimes": 1
    }),
    16000043: _tools.RODict({
        "ID": 16000043,
        "pickTimes": 1
    }),
    16000044: _tools.RODict({
        "ID": 16000044,
        "pickTimes": 1
    }),
    16000045: _tools.RODict({
        "ID": 16000045,
        "pickTimes": 1
    }),
    16000046: _tools.RODict({
        "ID": 16000046,
        "pickTimes": 1
    }),
    16000047: _tools.RODict({
        "ID": 16000047,
        "pickTimes": 1
    }),
    16000048: _tools.RODict({
        "ID": 16000048,
        "pickTimes": 5
    }),
    16000049: _tools.RODict({
        "ID": 16000049,
        "pickTimes": 10
    }),
    16000050: _tools.RODict({
        "ID": 16000050,
        "pickTimes": 15
    }),
    16000051: _tools.RODict({
        "ID": 16000051,
        "pickTimes": 20
    }),
    16000052: _tools.RODict({
        "ID": 16000052,
        "pickTimes": 20
    }),
    16000053: _tools.RODict({
        "ID": 16000053,
        "pickTimes": 10
    }),
    16000054: _tools.RODict({
        "ID": 16000054,
        "pickTimes": 15
    }),
    16000055: _tools.RODict({
        "ID": 16000055,
        "pickTimes": 20
    }),
    16000056: _tools.RODict({
        "ID": 16000056,
        "pickTimes": 1
    }),
    16000057: _tools.RODict({
        "ID": 16000057,
        "pickTimes": 1
    }),
    16000058: _tools.RODict({
        "ID": 16000058,
        "pickTimes": 1
    }),
    16000059: _tools.RODict({
        "ID": 16000059,
        "pickTimes": 1
    }),
    16000060: _tools.RODict({
        "ID": 16000060,
        "pickTimes": 1
    }),
    16000061: _tools.RODict({
        "ID": 16000061,
        "pickTimes": 1
    }),
    16000063: _tools.RODict({
        "ID": 16000063,
        "pickTimes": 1
    }),
    16000064: _tools.RODict({
        "ID": 16000064,
        "pickTimes": 1
    }),
    16000065: _tools.RODict({
        "ID": 16000065,
        "pickTimes": 1
    }),
    16000066: _tools.RODict({
        "ID": 16000066,
        "pickTimes": 1
    }),
    16000067: _tools.RODict({
        "ID": 16000067,
        "pickTimes": 1
    }),
    16000068: _tools.RODict({
        "ID": 16000068,
        "pickTimes": 1
    }),
    16000069: _tools.RODict({
        "ID": 16000069,
        "pickTimes": 1
    }),
    16000070: _tools.RODict({
        "ID": 16000070,
        "pickTimes": 1
    }),
    16000071: _tools.RODict({
        "ID": 16000071,
        "pickTimes": 1
    }),
    16000072: _tools.RODict({
        "ID": 16000072,
        "pickTimes": 1
    }),
    16000073: _tools.RODict({
        "ID": 16000073,
        "pickTimes": 1
    }),
    16000074: _tools.RODict({
        "ID": 16000074,
        "pickTimes": 1
    }),
    16000075: _tools.RODict({
        "ID": 16000075,
        "pickTimes": 1
    }),
    16000076: _tools.RODict({
        "ID": 16000076,
        "pickTimes": 1
    }),
    16000077: _tools.RODict({
        "ID": 16000077,
        "pickTimes": 1
    }),
    16000078: _tools.RODict({
        "ID": 16000078,
        "pickTimes": 1
    }),
    16000079: _tools.RODict({
        "ID": 16000079,
        "pickTimes": 1
    }),
    16000080: _tools.RODict({
        "ID": 16000080,
        "pickTimes": 1
    }),
    16000081: _tools.RODict({
        "ID": 16000081,
        "pickTimes": 1
    }),
    16000082: _tools.RODict({
        "ID": 16000082,
        "pickTimes": 1
    }),
    16000083: _tools.RODict({
        "ID": 16000083,
        "pickTimes": 1
    }),
    16000084: _tools.RODict({
        "ID": 16000084,
        "pickTimes": 1
    }),
    16000085: _tools.RODict({
        "ID": 16000085,
        "pickTimes": 1
    }),
    16000086: _tools.RODict({
        "ID": 16000086,
        "pickTimes": 1
    }),
    16000087: _tools.RODict({
        "ID": 16000087,
        "pickTimes": 1
    }),
    16000088: _tools.RODict({
        "ID": 16000088,
        "pickTimes": 1
    }),
    16000089: _tools.RODict({
        "ID": 16000089,
        "pickTimes": 1
    }),
    16000090: _tools.RODict({
        "ID": 16000090,
        "pickTimes": 1
    }),
    16000091: _tools.RODict({
        "ID": 16000091,
        "pickTimes": 1
    }),
    16000092: _tools.RODict({
        "ID": 16000092,
        "pickTimes": 1
    }),
    16000093: _tools.RODict({
        "ID": 16000093,
        "pickTimes": 1
    }),
    16000094: _tools.RODict({
        "ID": 16000094,
        "pickTimes": 1
    }),
    16000095: _tools.RODict({
        "ID": 16000095,
        "pickTimes": 1
    }),
    16000096: _tools.RODict({
        "ID": 16000096,
        "pickTimes": 1
    }),
    16000097: _tools.RODict({
        "ID": 16000097,
        "pickTimes": 1
    }),
    16000098: _tools.RODict({
        "ID": 16000098,
        "pickTimes": 1
    }),
    16000099: _tools.RODict({
        "ID": 16000099,
        "pickTimes": 1
    }),
    16000100: _tools.RODict({
        "ID": 16000100,
        "pickTimes": 1
    }),
    16000101: _tools.RODict({
        "ID": 16000101,
        "pickTimes": 1
    }),
    16000102: _tools.RODict({
        "ID": 16000102,
        "pickTimes": 1
    }),
    16000103: _tools.RODict({
        "ID": 16000103,
        "pickTimes": 1
    }),
    16000104: _tools.RODict({
        "ID": 16000104,
        "pickTimes": 1
    }),
    16000105: _tools.RODict({
        "ID": 16000105,
        "pickTimes": 1
    }),
    16000106: _tools.RODict({
        "ID": 16000106,
        "pickTimes": 1
    }),
    16000107: _tools.RODict({
        "ID": 16000107,
        "pickTimes": 1
    }),
    16000108: _tools.RODict({
        "ID": 16000108,
        "pickTimes": 1
    }),
    16000109: _tools.RODict({
        "ID": 16000109,
        "pickTimes": 1
    }),
    16000110: _tools.RODict({
        "ID": 16000110,
        "pickTimes": 1
    }),
    16000111: _tools.RODict({
        "ID": 16000111,
        "pickTimes": 1
    }),
    16000112: _tools.RODict({
        "ID": 16000112,
        "pickTimes": 1
    }),
    16000113: _tools.RODict({
        "ID": 16000113,
        "pickTimes": 1
    }),
    16000114: _tools.RODict({
        "ID": 16000114,
        "pickTimes": 1
    }),
    16000115: _tools.RODict({
        "ID": 16000115,
        "pickTimes": 1
    }),
    16000116: _tools.RODict({
        "ID": 16000116,
        "pickTimes": 1
    }),
    16000117: _tools.RODict({
        "ID": 16000117,
        "pickTimes": 1
    }),
    16000118: _tools.RODict({
        "ID": 16000118,
        "pickTimes": 1
    }),
    16000119: _tools.RODict({
        "ID": 16000119,
        "pickTimes": 1
    }),
    16001001: _tools.RODict({
        "ID": 16001001,
        "pickTimes": 20
    }),
    16001002: _tools.RODict({
        "ID": 16001002,
        "pickTimes": 30
    }),
    16001003: _tools.RODict({
        "ID": 16001003,
        "pickTimes": 45
    }),
    16001004: _tools.RODict({
        "ID": 16001004,
        "pickTimes": 60
    }),
    16001005: _tools.RODict({
        "ID": 16001005,
        "pickTimes": 20
    }),
    16001006: _tools.RODict({
        "ID": 16001006,
        "pickTimes": 30
    }),
    16001007: _tools.RODict({
        "ID": 16001007,
        "pickTimes": 45
    }),
    16001008: _tools.RODict({
        "ID": 16001008,
        "pickTimes": 60
    }),
    16001009: _tools.RODict({
        "ID": 16001009,
        "pickTimes": 25
    }),
    16001010: _tools.RODict({
        "ID": 16001010,
        "pickTimes": 80
    }),
    16001011: _tools.RODict({
        "ID": 16001011,
        "pickTimes": 100
    }),
    16001012: _tools.RODict({
        "ID": 16001012,
        "pickTimes": 150
    }),
    16001013: _tools.RODict({
        "ID": 16001013,
        "pickTimes": 25
    }),
    16001014: _tools.RODict({
        "ID": 16001014,
        "pickTimes": 80
    }),
    16001015: _tools.RODict({
        "ID": 16001015,
        "pickTimes": 100
    }),
    16001016: _tools.RODict({
        "ID": 16001016,
        "pickTimes": 150
    }),
    16001017: _tools.RODict({
        "ID": 16001017,
        "pickTimes": 25
    }),
    16001018: _tools.RODict({
        "ID": 16001018,
        "pickTimes": 80
    }),
    16001019: _tools.RODict({
        "ID": 16001019,
        "pickTimes": 100
    }),
    16001020: _tools.RODict({
        "ID": 16001020,
        "pickTimes": 150
    }),
    16001021: _tools.RODict({
        "ID": 16001021,
        "pickTimes": 25
    }),
    16001022: _tools.RODict({
        "ID": 16001022,
        "pickTimes": 80
    }),
    16001023: _tools.RODict({
        "ID": 16001023,
        "pickTimes": 100
    }),
    16001024: _tools.RODict({
        "ID": 16001024,
        "pickTimes": 150
    }),
    16001025: _tools.RODict({
        "ID": 16001025,
        "pickTimes": 25
    }),
    16001026: _tools.RODict({
        "ID": 16001026,
        "pickTimes": 80
    }),
    16001027: _tools.RODict({
        "ID": 16001027,
        "pickTimes": 100
    }),
    16001028: _tools.RODict({
        "ID": 16001028,
        "pickTimes": 150
    }),
    16001029: _tools.RODict({
        "ID": 16001029,
        "pickTimes": 25
    }),
    16001030: _tools.RODict({
        "ID": 16001030,
        "pickTimes": 80
    }),
    16001031: _tools.RODict({
        "ID": 16001031,
        "pickTimes": 100
    }),
    16001032: _tools.RODict({
        "ID": 16001032,
        "pickTimes": 150
    }),
    16001033: _tools.RODict({
        "ID": 16001033,
        "pickTimes": 25
    }),
    16001034: _tools.RODict({
        "ID": 16001034,
        "pickTimes": 80
    }),
    16001035: _tools.RODict({
        "ID": 16001035,
        "pickTimes": 100
    }),
    16001036: _tools.RODict({
        "ID": 16001036,
        "pickTimes": 150
    }),
    16001037: _tools.RODict({
        "ID": 16001037,
        "pickTimes": 25
    }),
    16001038: _tools.RODict({
        "ID": 16001038,
        "pickTimes": 80
    }),
    16001039: _tools.RODict({
        "ID": 16001039,
        "pickTimes": 100
    }),
    16001040: _tools.RODict({
        "ID": 16001040,
        "pickTimes": 150
    }),
    16001041: _tools.RODict({
        "ID": 16001041,
        "pickTimes": 25
    }),
    16001042: _tools.RODict({
        "ID": 16001042,
        "pickTimes": 80
    }),
    16001043: _tools.RODict({
        "ID": 16001043,
        "pickTimes": 100
    }),
    16001044: _tools.RODict({
        "ID": 16001044,
        "pickTimes": 150
    }),
    16001045: _tools.RODict({
        "ID": 16001045,
        "pickTimes": 25
    }),
    16001046: _tools.RODict({
        "ID": 16001046,
        "pickTimes": 80
    }),
    16001047: _tools.RODict({
        "ID": 16001047,
        "pickTimes": 100
    }),
    16001048: _tools.RODict({
        "ID": 16001048,
        "pickTimes": 150
    }),
    16001049: _tools.RODict({
        "ID": 16001049,
        "pickTimes": 25
    }),
    16001050: _tools.RODict({
        "ID": 16001050,
        "pickTimes": 80
    }),
    16001051: _tools.RODict({
        "ID": 16001051,
        "pickTimes": 100
    }),
    16001052: _tools.RODict({
        "ID": 16001052,
        "pickTimes": 150
    }),
    16001053: _tools.RODict({
        "ID": 16001053,
        "pickTimes": 25
    }),
    16001054: _tools.RODict({
        "ID": 16001054,
        "pickTimes": 80
    }),
    16001055: _tools.RODict({
        "ID": 16001055,
        "pickTimes": 100
    }),
    16001056: _tools.RODict({
        "ID": 16001056,
        "pickTimes": 150
    }),
    16001057: _tools.RODict({
        "ID": 16001057,
        "pickTimes": 25
    }),
    16001058: _tools.RODict({
        "ID": 16001058,
        "pickTimes": 80
    }),
    16001059: _tools.RODict({
        "ID": 16001059,
        "pickTimes": 100
    }),
    16001060: _tools.RODict({
        "ID": 16001060,
        "pickTimes": 150
    }),
    16001061: _tools.RODict({
        "ID": 16001061,
        "pickTimes": 25
    }),
    16001062: _tools.RODict({
        "ID": 16001062,
        "pickTimes": 80
    }),
    16001063: _tools.RODict({
        "ID": 16001063,
        "pickTimes": 100
    }),
    16001064: _tools.RODict({
        "ID": 16001064,
        "pickTimes": 150
    }),
    16002001: _tools.RODict({
        "ID": 16002001,
        "pickTimes": 1
    }),
    16002002: _tools.RODict({
        "ID": 16002002,
        "pickTimes": 1
    }),
    16002003: _tools.RODict({
        "ID": 16002003,
        "pickTimes": 1
    }),
    16002004: _tools.RODict({
        "ID": 16002004,
        "pickTimes": 1
    }),
    16002005: _tools.RODict({
        "ID": 16002005,
        "pickTimes": 1
    }),
    16002006: _tools.RODict({
        "ID": 16002006,
        "pickTimes": 60
    }),
    16002007: _tools.RODict({
        "ID": 16002007,
        "pickTimes": 90
    }),
    16002008: _tools.RODict({
        "ID": 16002008,
        "pickTimes": 150
    }),
    16002009: _tools.RODict({
        "ID": 16002009,
        "pickTimes": 1
    }),
    16002010: _tools.RODict({
        "ID": 16002010,
        "pickTimes": 1
    }),
    16002101: _tools.RODict({
        "ID": 16002101,
        "pickTimes": 1
    }),
    16002102: _tools.RODict({
        "ID": 16002102,
        "pickTimes": 1
    }),
    16002103: _tools.RODict({
        "ID": 16002103,
        "pickTimes": 1
    }),
    16002104: _tools.RODict({
        "ID": 16002104,
        "pickTimes": 1
    }),
    16002105: _tools.RODict({
        "ID": 16002105,
        "pickTimes": 1
    }),
    16002106: _tools.RODict({
        "ID": 16002106,
        "pickTimes": 60
    }),
    16002107: _tools.RODict({
        "ID": 16002107,
        "pickTimes": 90
    }),
    16002108: _tools.RODict({
        "ID": 16002108,
        "pickTimes": 150
    }),
    16002109: _tools.RODict({
        "ID": 16002109,
        "pickTimes": 1
    }),
    16002110: _tools.RODict({
        "ID": 16002110,
        "pickTimes": 1
    }),
    16002201: _tools.RODict({
        "ID": 16002201,
        "pickTimes": 1
    }),
    16002202: _tools.RODict({
        "ID": 16002202,
        "pickTimes": 1
    }),
    16002203: _tools.RODict({
        "ID": 16002203,
        "pickTimes": 1
    }),
    16002204: _tools.RODict({
        "ID": 16002204,
        "pickTimes": 1
    }),
    16002205: _tools.RODict({
        "ID": 16002205,
        "pickTimes": 1
    }),
    16002206: _tools.RODict({
        "ID": 16002206,
        "pickTimes": 60
    }),
    16002207: _tools.RODict({
        "ID": 16002207,
        "pickTimes": 90
    }),
    16002208: _tools.RODict({
        "ID": 16002208,
        "pickTimes": 150
    }),
    16002209: _tools.RODict({
        "ID": 16002209,
        "pickTimes": 1
    }),
    16002210: _tools.RODict({
        "ID": 16002210,
        "pickTimes": 1
    }),
    16002301: _tools.RODict({
        "ID": 16002301,
        "pickTimes": 1
    }),
    16002302: _tools.RODict({
        "ID": 16002302,
        "pickTimes": 1
    }),
    16002303: _tools.RODict({
        "ID": 16002303,
        "pickTimes": 1
    }),
    16002304: _tools.RODict({
        "ID": 16002304,
        "pickTimes": 1
    }),
    16002401: _tools.RODict({
        "ID": 16002401,
        "pickTimes": 1
    }),
    16002402: _tools.RODict({
        "ID": 16002402,
        "pickTimes": 1
    }),
    16002403: _tools.RODict({
        "ID": 16002403,
        "pickTimes": 1
    }),
    16002404: _tools.RODict({
        "ID": 16002404,
        "pickTimes": 1
    }),
    16003101: _tools.RODict({
        "ID": 16003101,
        "pickTimes": 1
    }),
    16003102: _tools.RODict({
        "ID": 16003102,
        "pickTimes": 1
    }),
    16003103: _tools.RODict({
        "ID": 16003103,
        "pickTimes": 1
    }),
    16003104: _tools.RODict({
        "ID": 16003104,
        "pickTimes": 1
    }),
    16003105: _tools.RODict({
        "ID": 16003105,
        "pickTimes": 1
    }),
    16003106: _tools.RODict({
        "ID": 16003106,
        "pickTimes": 1
    }),
    16003107: _tools.RODict({
        "ID": 16003107,
        "pickTimes": 1
    }),
    16003108: _tools.RODict({
        "ID": 16003108,
        "pickTimes": 1
    }),
    16003201: _tools.RODict({
        "ID": 16003201,
        "pickTimes": 1
    }),
    16003202: _tools.RODict({
        "ID": 16003202,
        "pickTimes": 1
    }),
    16003203: _tools.RODict({
        "ID": 16003203,
        "pickTimes": 1
    }),
    16003204: _tools.RODict({
        "ID": 16003204,
        "pickTimes": 1
    }),
    16003205: _tools.RODict({
        "ID": 16003205,
        "pickTimes": 1
    }),
    16003206: _tools.RODict({
        "ID": 16003206,
        "pickTimes": 1
    }),
    16003207: _tools.RODict({
        "ID": 16003207,
        "pickTimes": 1
    }),
    16003208: _tools.RODict({
        "ID": 16003208,
        "pickTimes": 1
    }),
    16003301: _tools.RODict({
        "ID": 16003301,
        "pickTimes": 1
    }),
    16003302: _tools.RODict({
        "ID": 16003302,
        "pickTimes": 1
    }),
    16003303: _tools.RODict({
        "ID": 16003303,
        "pickTimes": 1
    }),
    16003304: _tools.RODict({
        "ID": 16003304,
        "pickTimes": 1
    }),
    16003305: _tools.RODict({
        "ID": 16003305,
        "pickTimes": 1
    }),
    16003306: _tools.RODict({
        "ID": 16003306,
        "pickTimes": 1
    }),
    16003307: _tools.RODict({
        "ID": 16003307,
        "pickTimes": 1
    }),
    16003308: _tools.RODict({
        "ID": 16003308,
        "pickTimes": 1
    }),
    16006068: _tools.RODict({
        "ID": 16006068,
        "pickTimes": 1
    }),
    16006069: _tools.RODict({
        "ID": 16006069,
        "pickTimes": 1
    }),
    16006070: _tools.RODict({
        "ID": 16006070,
        "pickTimes": 1
    }),
    16006071: _tools.RODict({
        "ID": 16006071,
        "pickTimes": 1
    }),
    16006072: _tools.RODict({
        "ID": 16006072,
        "pickTimes": 1
    }),
    16006073: _tools.RODict({
        "ID": 16006073,
        "pickTimes": 1
    }),
    16006074: _tools.RODict({
        "ID": 16006074,
        "pickTimes": 1
    }),
    16006075: _tools.RODict({
        "ID": 16006075,
        "pickTimes": 1
    }),
    16006076: _tools.RODict({
        "ID": 16006076,
        "pickTimes": 1
    }),
    16006077: _tools.RODict({
        "ID": 16006077,
        "pickTimes": 1
    }),
    16006078: _tools.RODict({
        "ID": 16006078,
        "pickTimes": 1
    }),
    16006079: _tools.RODict({
        "ID": 16006079,
        "pickTimes": 1
    }),
    16006080: _tools.RODict({
        "ID": 16006080,
        "pickTimes": 1
    }),
    16006081: _tools.RODict({
        "ID": 16006081,
        "pickTimes": 1
    }),
    16006082: _tools.RODict({
        "ID": 16006082,
        "pickTimes": 1
    }),
    16006083: _tools.RODict({
        "ID": 16006083,
        "pickTimes": 1
    }),
    16006084: _tools.RODict({
        "ID": 16006084,
        "pickTimes": 1
    }),
    16006085: _tools.RODict({
        "ID": 16006085,
        "pickTimes": 1
    }),
    16006086: _tools.RODict({
        "ID": 16006086,
        "pickTimes": 1
    }),
    16006087: _tools.RODict({
        "ID": 16006087,
        "pickTimes": 1
    }),
    16006088: _tools.RODict({
        "ID": 16006088,
        "pickTimes": 1
    }),
    16006089: _tools.RODict({
        "ID": 16006089,
        "pickTimes": 1
    }),
    16006090: _tools.RODict({
        "ID": 16006090,
        "pickTimes": 1
    }),
    16006091: _tools.RODict({
        "ID": 16006091,
        "pickTimes": 1
    }),
    16006092: _tools.RODict({
        "ID": 16006092,
        "pickTimes": 1
    }),
    16006093: _tools.RODict({
        "ID": 16006093,
        "pickTimes": 1
    }),
    16006094: _tools.RODict({
        "ID": 16006094,
        "pickTimes": 1
    }),
    16006095: _tools.RODict({
        "ID": 16006095,
        "pickTimes": 1
    }),
    16006096: _tools.RODict({
        "ID": 16006096,
        "pickTimes": 1
    }),
    16006097: _tools.RODict({
        "ID": 16006097,
        "pickTimes": 1
    }),
    16006098: _tools.RODict({
        "ID": 16006098,
        "pickTimes": 1
    }),
    16006099: _tools.RODict({
        "ID": 16006099,
        "pickTimes": 1
    }),
    16006100: _tools.RODict({
        "ID": 16006100,
        "pickTimes": 1
    }),
    16006101: _tools.RODict({
        "ID": 16006101,
        "pickTimes": 1
    }),
    16006102: _tools.RODict({
        "ID": 16006102,
        "pickTimes": 1
    }),
    16006103: _tools.RODict({
        "ID": 16006103,
        "pickTimes": 1
    }),
    16006104: _tools.RODict({
        "ID": 16006104,
        "pickTimes": 1
    }),
    16006105: _tools.RODict({
        "ID": 16006105,
        "pickTimes": 1
    }),
    16006106: _tools.RODict({
        "ID": 16006106,
        "pickTimes": 1
    })
})
minKey = 16000002
maxKey = 16006106