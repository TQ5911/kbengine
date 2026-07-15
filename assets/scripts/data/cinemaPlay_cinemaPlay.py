# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: cinemaPlay/cinemaPlay
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    98000001: _tools.RODict({
        "ID": 98000001,
        "cinemaTime": 5,
        "event": "",
        "parm": "",
    }),
    98000002: _tools.RODict({
        "ID": 98000002,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98000035: _tools.RODict({
        "ID": 98000035,
        "cinemaTime": 5,
        "event": "",
        "parm": "",
    }),
    98000036: _tools.RODict({
        "ID": 98000036,
        "cinemaTime": 5,
        "event": "",
        "parm": "1",
    }),
    98000037: _tools.RODict({
        "ID": 98000037,
        "cinemaTime": 5,
        "event": "",
        "parm": "1",
    }),
    98000056: _tools.RODict({
        "ID": 98000056,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98000057: _tools.RODict({
        "ID": 98000057,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98000063: _tools.RODict({
        "ID": 98000063,
        "cinemaTime": 12,
        "event": "setPositionByTag",
        "parm": "1",
    }),
    98000076: _tools.RODict({
        "ID": 98000076,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98010001: _tools.RODict({
        "ID": 98010001,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98010002: _tools.RODict({
        "ID": 98010002,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98010003: _tools.RODict({
        "ID": 98010003,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98010004: _tools.RODict({
        "ID": 98010004,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98010005: _tools.RODict({
        "ID": 98010005,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98010006: _tools.RODict({
        "ID": 98010006,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98010008: _tools.RODict({
        "ID": 98010008,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98010010: _tools.RODict({
        "ID": 98010010,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98010011: _tools.RODict({
        "ID": 98010011,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98010012: _tools.RODict({
        "ID": 98010012,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98010013: _tools.RODict({
        "ID": 98010013,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98010014: _tools.RODict({
        "ID": 98010014,
        "cinemaTime": 12,
        "event": "setPositionByTag",
        "parm": "3",
    }),
    98010015: _tools.RODict({
        "ID": 98010015,
        "cinemaTime": 12,
        "event": "setPositionByTag",
        "parm": "2",
    }),
    98010016: _tools.RODict({
        "ID": 98010016,
        "cinemaTime": 12,
        "event": "setPositionByTag",
        "parm": "4",
    }),
    98010018: _tools.RODict({
        "ID": 98010018,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98010019: _tools.RODict({
        "ID": 98010019,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98010020: _tools.RODict({
        "ID": 98010020,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98010021: _tools.RODict({
        "ID": 98010021,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98010022: _tools.RODict({
        "ID": 98010022,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98010023: _tools.RODict({
        "ID": 98010023,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98010024: _tools.RODict({
        "ID": 98010024,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98010025: _tools.RODict({
        "ID": 98010025,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98010026: _tools.RODict({
        "ID": 98010026,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98010027: _tools.RODict({
        "ID": 98010027,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98010028: _tools.RODict({
        "ID": 98010028,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040001: _tools.RODict({
        "ID": 98040001,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040002: _tools.RODict({
        "ID": 98040002,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040003: _tools.RODict({
        "ID": 98040003,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040004: _tools.RODict({
        "ID": 98040004,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040005: _tools.RODict({
        "ID": 98040005,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040006: _tools.RODict({
        "ID": 98040006,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040007: _tools.RODict({
        "ID": 98040007,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040008: _tools.RODict({
        "ID": 98040008,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040009: _tools.RODict({
        "ID": 98040009,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040010: _tools.RODict({
        "ID": 98040010,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040011: _tools.RODict({
        "ID": 98040011,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040012: _tools.RODict({
        "ID": 98040012,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040013: _tools.RODict({
        "ID": 98040013,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040014: _tools.RODict({
        "ID": 98040014,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040015: _tools.RODict({
        "ID": 98040015,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040016: _tools.RODict({
        "ID": 98040016,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040017: _tools.RODict({
        "ID": 98040017,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040018: _tools.RODict({
        "ID": 98040018,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040019: _tools.RODict({
        "ID": 98040019,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040020: _tools.RODict({
        "ID": 98040020,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040021: _tools.RODict({
        "ID": 98040021,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040022: _tools.RODict({
        "ID": 98040022,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040023: _tools.RODict({
        "ID": 98040023,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040024: _tools.RODict({
        "ID": 98040024,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040025: _tools.RODict({
        "ID": 98040025,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040026: _tools.RODict({
        "ID": 98040026,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040027: _tools.RODict({
        "ID": 98040027,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040028: _tools.RODict({
        "ID": 98040028,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040029: _tools.RODict({
        "ID": 98040029,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040030: _tools.RODict({
        "ID": 98040030,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040031: _tools.RODict({
        "ID": 98040031,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040032: _tools.RODict({
        "ID": 98040032,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040033: _tools.RODict({
        "ID": 98040033,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040034: _tools.RODict({
        "ID": 98040034,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040035: _tools.RODict({
        "ID": 98040035,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040036: _tools.RODict({
        "ID": 98040036,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040037: _tools.RODict({
        "ID": 98040037,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040038: _tools.RODict({
        "ID": 98040038,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040039: _tools.RODict({
        "ID": 98040039,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040040: _tools.RODict({
        "ID": 98040040,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040041: _tools.RODict({
        "ID": 98040041,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040042: _tools.RODict({
        "ID": 98040042,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040043: _tools.RODict({
        "ID": 98040043,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040044: _tools.RODict({
        "ID": 98040044,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040045: _tools.RODict({
        "ID": 98040045,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040046: _tools.RODict({
        "ID": 98040046,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040047: _tools.RODict({
        "ID": 98040047,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040048: _tools.RODict({
        "ID": 98040048,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040049: _tools.RODict({
        "ID": 98040049,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040050: _tools.RODict({
        "ID": 98040050,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040051: _tools.RODict({
        "ID": 98040051,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040052: _tools.RODict({
        "ID": 98040052,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040053: _tools.RODict({
        "ID": 98040053,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98040054: _tools.RODict({
        "ID": 98040054,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    }),
    98090001: _tools.RODict({
        "ID": 98090001,
        "cinemaTime": 12,
        "event": "",
        "parm": "",
    })
})
minKey = 98000001
maxKey = 98090001