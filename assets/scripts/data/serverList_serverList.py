# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: serverList/serverList
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    10001: _tools.RODict({
        "ID": 10001,
        "serverName": "公共服",
        "groupID": 1,
        "zoneID": 2000,
        "startTime": "1742160600",
        "serverState": 4,
        "serverFlagState": 1
    }),
    10002: _tools.RODict({
        "ID": 10002,
        "serverName": "alphaTest9",
        "groupID": 9,
        "zoneID": 2000,
        "startTime": "1735680600",
        "serverState": 4,
        "serverFlagState": 1
    }),
    10003: _tools.RODict({
        "ID": 10003,
        "serverName": "alpha跨服9",
        "groupID": 9,
        "zoneID": 2000,
        "startTime": "1735680600",
        "serverState": 4,
        "serverFlagState": 1
    }),
    20002: _tools.RODict({
        "ID": 20002,
        "serverName": "苹果审核服",
        "groupID": 1,
        "zoneID": 2000,
        "startTime": "1742160600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20003: _tools.RODict({
        "ID": 20003,
        "serverName": "压测LT服",
        "groupID": 1,
        "zoneID": 2000,
        "startTime": "1742160600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20004: _tools.RODict({
        "ID": 20004,
        "serverName": "预发布",
        "groupID": 1,
        "zoneID": 2000,
        "startTime": "1742160600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20005: _tools.RODict({
        "ID": 20005,
        "serverName": "预发布1",
        "groupID": 1,
        "zoneID": 2000,
        "startTime": "1742160600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20088: _tools.RODict({
        "ID": 20088,
        "serverName": "MYH",
        "groupID": 3,
        "zoneID": 2003,
        "startTime": "1742160600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20101: _tools.RODict({
        "ID": 20101,
        "serverName": "WZW",
        "groupID": 2,
        "zoneID": 2002,
        "startTime": "1742160600",
        "serverState": 1,
        "serverFlagState": (1, 2)
    }),
    20102: _tools.RODict({
        "ID": 20102,
        "serverName": "LZY",
        "groupID": 2,
        "zoneID": 2002,
        "startTime": "1742160600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20103: _tools.RODict({
        "ID": 20103,
        "serverName": "YY",
        "groupID": 2,
        "zoneID": 2002,
        "startTime": "1742160600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20104: _tools.RODict({
        "ID": 20104,
        "serverName": "LY",
        "groupID": 2,
        "zoneID": 2002,
        "startTime": "1742160600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20105: _tools.RODict({
        "ID": 20105,
        "serverName": "ZXH",
        "groupID": 8,
        "zoneID": 2003,
        "startTime": "1742160600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20107: _tools.RODict({
        "ID": 20107,
        "serverName": "TJY",
        "groupID": 2,
        "zoneID": 2002,
        "startTime": "1742160600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20108: _tools.RODict({
        "ID": 20108,
        "serverName": "WP",
        "groupID": 8,
        "zoneID": 2003,
        "startTime": "1742160600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20109: _tools.RODict({
        "ID": 20109,
        "serverName": "WZW2",
        "groupID": 2,
        "zoneID": 2002,
        "startTime": "1742160600",
        "serverState": 0,
        "serverFlagState": (1, 2)
    }),
    20110: _tools.RODict({
        "ID": 20110,
        "serverName": "YWM",
        "groupID": 2,
        "zoneID": 2003,
        "startTime": "1750663800",
        "serverState": 2,
        "serverFlagState": None
    }),
    20201: _tools.RODict({
        "ID": 20201,
        "serverName": "WYL",
        "groupID": 30,
        "zoneID": 2003,
        "startTime": "1742160600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20202: _tools.RODict({
        "ID": 20202,
        "serverName": "WYL2",
        "groupID": 30,
        "zoneID": 2003,
        "startTime": "1742160600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20212: _tools.RODict({
        "ID": 20212,
        "serverName": "XFL",
        "groupID": 3,
        "zoneID": 2003,
        "startTime": "1742160600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20216: _tools.RODict({
        "ID": 20216,
        "serverName": "WYB",
        "groupID": 2,
        "zoneID": 2003,
        "startTime": "1750663800",
        "serverState": 2,
        "serverFlagState": None
    }),
    20222: _tools.RODict({
        "ID": 20222,
        "serverName": "SiYiH",
        "groupID": 2,
        "zoneID": 2003,
        "startTime": "1742160600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20223: _tools.RODict({
        "ID": 20223,
        "serverName": "ckz",
        "groupID": 2,
        "zoneID": 2003,
        "startTime": "1742160600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20224: _tools.RODict({
        "ID": 20224,
        "serverName": "公共2服",
        "groupID": 1,
        "zoneID": 2000,
        "startTime": "1742196600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20225: _tools.RODict({
        "ID": 20225,
        "serverName": "ckz2",
        "groupID": 2,
        "zoneID": 2003,
        "startTime": "1742196600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20226: _tools.RODict({
        "ID": 20226,
        "serverName": "lh",
        "groupID": 2,
        "zoneID": 2002,
        "startTime": "1742196600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20227: _tools.RODict({
        "ID": 20227,
        "serverName": "ZTQ",
        "groupID": 3,
        "zoneID": 2003,
        "startTime": "1742196600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20228: _tools.RODict({
        "ID": 20228,
        "serverName": "LJ",
        "groupID": 4,
        "zoneID": 2003,
        "startTime": "1742196600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20229: _tools.RODict({
        "ID": 20229,
        "serverName": "WZY",
        "groupID": 5,
        "zoneID": 2003,
        "startTime": "1742196600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20230: _tools.RODict({
        "ID": 20230,
        "serverName": "clys",
        "groupID": 2,
        "zoneID": 2003,
        "startTime": "1742160600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20231: _tools.RODict({
        "ID": 20231,
        "serverName": "QW",
        "groupID": 3,
        "zoneID": 2003,
        "startTime": "1743494400",
        "serverState": 2,
        "serverFlagState": None
    }),
    20232: _tools.RODict({
        "ID": 20232,
        "serverName": "GJQ",
        "groupID": 3,
        "zoneID": 2003,
        "startTime": "1744009200",
        "serverState": 2,
        "serverFlagState": None
    }),
    20233: _tools.RODict({
        "ID": 20233,
        "serverName": "zww",
        "groupID": 12,
        "zoneID": 2003,
        "startTime": "1744009200",
        "serverState": 2,
        "serverFlagState": None
    }),
    20234: _tools.RODict({
        "ID": 20234,
        "serverName": "DCL",
        "groupID": 3,
        "zoneID": 2003,
        "startTime": "1742160600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20235: _tools.RODict({
        "ID": 20235,
        "serverName": "CYF",
        "groupID": 2,
        "zoneID": 2003,
        "startTime": "1745812800",
        "serverState": 2,
        "serverFlagState": None
    }),
    20236: _tools.RODict({
        "ID": 20236,
        "serverName": "LM",
        "groupID": 3,
        "zoneID": 2003,
        "startTime": "1745812800",
        "serverState": 2,
        "serverFlagState": None
    }),
    20237: _tools.RODict({
        "ID": 20237,
        "serverName": "YL",
        "groupID": 2,
        "zoneID": 2002,
        "startTime": "1747638000",
        "serverState": 2,
        "serverFlagState": None
    }),
    20238: _tools.RODict({
        "ID": 20238,
        "serverName": "LJCS",
        "groupID": 4,
        "zoneID": 2003,
        "startTime": "1742196600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20239: _tools.RODict({
        "ID": 20239,
        "serverName": "LZJ",
        "groupID": 2,
        "zoneID": 2003,
        "startTime": "1742196600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20240: _tools.RODict({
        "ID": 20240,
        "serverName": "XGT",
        "groupID": 2,
        "zoneID": 2002,
        "startTime": "1742196600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20241: _tools.RODict({
        "ID": 20241,
        "serverName": "ZC",
        "groupID": 6,
        "zoneID": 2002,
        "startTime": "1742160600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20242: _tools.RODict({
        "ID": 20242,
        "serverName": "WY",
        "groupID": 2,
        "zoneID": 2002,
        "startTime": "1743494400",
        "serverState": 2,
        "serverFlagState": None
    }),
    20250: _tools.RODict({
        "ID": 20250,
        "serverName": "SXS",
        "groupID": 2,
        "zoneID": 2003,
        "startTime": "1742196600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20251: _tools.RODict({
        "ID": 20251,
        "serverName": "ZCCS",
        "groupID": 6,
        "zoneID": 2002,
        "startTime": "1742160600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20256: _tools.RODict({
        "ID": 20256,
        "serverName": "LQY",
        "groupID": 3,
        "zoneID": 2003,
        "startTime": "1742196600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20257: _tools.RODict({
        "ID": 20257,
        "serverName": "LH",
        "groupID": 3,
        "zoneID": 2003,
        "startTime": "1742196600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20258: _tools.RODict({
        "ID": 20258,
        "serverName": "TT",
        "groupID": 3,
        "zoneID": 2003,
        "startTime": "1742196600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20259: _tools.RODict({
        "ID": 20259,
        "serverName": "MJJ",
        "groupID": 2,
        "zoneID": 2002,
        "startTime": "1742196600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20298: _tools.RODict({
        "ID": 20298,
        "serverName": "ZR",
        "groupID": 2,
        "zoneID": 2002,
        "startTime": "1742196600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20806: _tools.RODict({
        "ID": 20806,
        "serverName": "跨服ZXH",
        "groupID": 8,
        "zoneID": 2003,
        "startTime": "1742160600",
        "serverState": 2,
        "serverFlagState": None
    }),
    20807: _tools.RODict({
        "ID": 20807,
        "serverName": "zww跨服",
        "groupID": 12,
        "zoneID": 2003,
        "startTime": "1744009200",
        "serverState": 2,
        "serverFlagState": None
    })
})
minKey = 10001
maxKey = 20807

group2ServerIds = _tools.RODict({
    1: _tools.ROList(['10001', '20002', '20003', '20004', '20005', '20224']),
    9: _tools.ROList(['10002', '10003']),
    3: _tools.ROList(['20088', '20212', '20227', '20231', '20232', '20234', '20236', '20256', '20257', '20258']),
    2: _tools.ROList(['20101', '20102', '20103', '20104', '20107', '20109', '20110', '20216', '20222', '20223', '20225', '20226', '20230', '20235', '20237', '20239', '20240', '20242', '20250', '20259', '20298']),
    8: _tools.ROList(['20105', '20108', '20806']),
    30: _tools.ROList(['20201', '20202']),
    4: _tools.ROList(['20228', '20238']),
    5: _tools.ROList(['20229']),
    12: _tools.ROList(['20233', '20807']),
    6: _tools.ROList(['20241', '20251']),
})