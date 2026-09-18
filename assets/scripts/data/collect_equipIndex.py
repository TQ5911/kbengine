# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: collect/equipIndex
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    101: _tools.RODict({
        "indexId": 101,
        "propList": _tools.ROList([80111001, 80121001, 80131001])
    }),
    102: _tools.RODict({
        "indexId": 102,
        "propList": _tools.ROList([80112001, 80122001, 80132001])
    }),
    103: _tools.RODict({
        "indexId": 103,
        "propList": _tools.ROList([80113001, 80123001, 80133001])
    }),
    104: _tools.RODict({
        "indexId": 104,
        "propList": _tools.ROList([80114001, 80124001, 80134001])
    }),
    201: _tools.RODict({
        "indexId": 201,
        "propList": _tools.ROList([80211001, 80221001, 80231001])
    }),
    202: _tools.RODict({
        "indexId": 202,
        "propList": _tools.ROList([80212001, 80222001, 80232001])
    }),
    203: _tools.RODict({
        "indexId": 203,
        "propList": _tools.ROList([80213001, 80223001, 80233001])
    }),
    204: _tools.RODict({
        "indexId": 204,
        "propList": _tools.ROList([80214001, 80224001, 80234001])
    }),
    301: _tools.RODict({
        "indexId": 301,
        "propList": _tools.ROList([80311001, 80321001, 80331001])
    }),
    302: _tools.RODict({
        "indexId": 302,
        "propList": _tools.ROList([80312001, 80322001, 80332001])
    }),
    303: _tools.RODict({
        "indexId": 303,
        "propList": _tools.ROList([80313001, 80323001, 80333001])
    }),
    304: _tools.RODict({
        "indexId": 304,
        "propList": _tools.ROList([80314001, 80324001, 80334001])
    }),
    401: _tools.RODict({
        "indexId": 401,
        "propList": _tools.ROList([80411001, 80421001, 80431001])
    }),
    402: _tools.RODict({
        "indexId": 402,
        "propList": _tools.ROList([80412001, 80422001, 80432001])
    }),
    403: _tools.RODict({
        "indexId": 403,
        "propList": _tools.ROList([80413001, 80423001, 80433001])
    }),
    404: _tools.RODict({
        "indexId": 404,
        "propList": _tools.ROList([80414001, 80424001, 80434001])
    }),
    501: _tools.RODict({
        "indexId": 501,
        "propList": _tools.ROList([80591001, 80591001, 80581001])
    }),
    502: _tools.RODict({
        "indexId": 502,
        "propList": _tools.ROList([80592001, 80592001, 80582001])
    }),
    503: _tools.RODict({
        "indexId": 503,
        "propList": _tools.ROList([80593001, 80593001, 80583001])
    }),
    504: _tools.RODict({
        "indexId": 504,
        "propList": _tools.ROList([80594001, 80594001, 80584001])
    }),
    601: _tools.RODict({
        "indexId": 601,
        "propList": _tools.ROList([80691001, 80691001, 80681001])
    }),
    602: _tools.RODict({
        "indexId": 602,
        "propList": _tools.ROList([80692001, 80692001, 80682001])
    }),
    603: _tools.RODict({
        "indexId": 603,
        "propList": _tools.ROList([80693001, 80693001, 80683001])
    }),
    604: _tools.RODict({
        "indexId": 604,
        "propList": _tools.ROList([80694001, 80694001, 80684001])
    }),
    701: _tools.RODict({
        "indexId": 701,
        "propList": _tools.ROList([80791001, 80791001, 80781001])
    }),
    702: _tools.RODict({
        "indexId": 702,
        "propList": _tools.ROList([80792001, 80792001, 80782001])
    }),
    703: _tools.RODict({
        "indexId": 703,
        "propList": _tools.ROList([80793001, 80793001, 80783001])
    }),
    704: _tools.RODict({
        "indexId": 704,
        "propList": _tools.ROList([80794001, 80794001, 80784001])
    }),
    801: _tools.RODict({
        "indexId": 801,
        "propList": _tools.ROList([80811001, 80821001, 80831001])
    }),
    802: _tools.RODict({
        "indexId": 802,
        "propList": _tools.ROList([80812001, 80822001, 80832001])
    }),
    803: _tools.RODict({
        "indexId": 803,
        "propList": _tools.ROList([80813001, 80823001, 80833001])
    }),
    804: _tools.RODict({
        "indexId": 804,
        "propList": _tools.ROList([80814001, 80824001, 80834001])
    })
})
minKey = 101
maxKey = 804