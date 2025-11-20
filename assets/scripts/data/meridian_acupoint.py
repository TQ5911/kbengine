# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: meridian/acupoint
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    10101: _tools.RODict({
        "ID": 10101,
        "meridian": 1,
        "acupoint": 1,
        "level": 1,
        "prop": _tools.RODict({0:52120001}),
        "needItems": _tools.ROList([[30000263, 10], [30000264, 10]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    10102: _tools.RODict({
        "ID": 10102,
        "meridian": 1,
        "acupoint": 1,
        "level": 2,
        "prop": _tools.RODict({0:52120002}),
        "needItems": _tools.ROList([[30000263, 12], [30000264, 12]]),
        "needCoins": _tools.ROList([30000002, 2200])
    }),
    10103: _tools.RODict({
        "ID": 10103,
        "meridian": 1,
        "acupoint": 1,
        "level": 3,
        "prop": _tools.RODict({0:52120003}),
        "needItems": _tools.ROList([[30000263, 14], [30000264, 14]]),
        "needCoins": _tools.ROList([30000002, 2400])
    }),
    10104: _tools.RODict({
        "ID": 10104,
        "meridian": 1,
        "acupoint": 1,
        "level": 4,
        "prop": _tools.RODict({0:52120004}),
        "needItems": _tools.ROList([[30000263, 16], [30000264, 16]]),
        "needCoins": _tools.ROList([30000002, 2600])
    }),
    10105: _tools.RODict({
        "ID": 10105,
        "meridian": 1,
        "acupoint": 1,
        "level": 5,
        "prop": _tools.RODict({0:52120005}),
        "needItems": _tools.ROList([[30000263, 18], [30000264, 18]]),
        "needCoins": _tools.ROList([30000002, 2900])
    }),
    10201: _tools.RODict({
        "ID": 10201,
        "meridian": 1,
        "acupoint": 2,
        "level": 1,
        "prop": _tools.RODict({0:52120101}),
        "needItems": _tools.ROList([[30000264, 10], [30000265, 10]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    10202: _tools.RODict({
        "ID": 10202,
        "meridian": 1,
        "acupoint": 2,
        "level": 2,
        "prop": _tools.RODict({0:52120102}),
        "needItems": _tools.ROList([[30000264, 12], [30000265, 12]]),
        "needCoins": _tools.ROList([30000002, 2200])
    }),
    10203: _tools.RODict({
        "ID": 10203,
        "meridian": 1,
        "acupoint": 2,
        "level": 3,
        "prop": _tools.RODict({0:52120103}),
        "needItems": _tools.ROList([[30000264, 14], [30000265, 14]]),
        "needCoins": _tools.ROList([30000002, 2400])
    }),
    10204: _tools.RODict({
        "ID": 10204,
        "meridian": 1,
        "acupoint": 2,
        "level": 4,
        "prop": _tools.RODict({0:52120104}),
        "needItems": _tools.ROList([[30000264, 16], [30000265, 16]]),
        "needCoins": _tools.ROList([30000002, 2600])
    }),
    10205: _tools.RODict({
        "ID": 10205,
        "meridian": 1,
        "acupoint": 2,
        "level": 5,
        "prop": _tools.RODict({0:52120105}),
        "needItems": _tools.ROList([[30000264, 18], [30000265, 18]]),
        "needCoins": _tools.ROList([30000002, 2900])
    }),
    10301: _tools.RODict({
        "ID": 10301,
        "meridian": 1,
        "acupoint": 3,
        "level": 1,
        "prop": _tools.RODict({1001:52120301,1002:52120301,1003:52120201}),
        "needItems": _tools.ROList([[30000265, 10], [30000266, 10]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    10302: _tools.RODict({
        "ID": 10302,
        "meridian": 1,
        "acupoint": 3,
        "level": 2,
        "prop": _tools.RODict({1001:52120302,1002:52120302,1003:52120202}),
        "needItems": _tools.ROList([[30000265, 12], [30000266, 12]]),
        "needCoins": _tools.ROList([30000002, 2200])
    }),
    10303: _tools.RODict({
        "ID": 10303,
        "meridian": 1,
        "acupoint": 3,
        "level": 3,
        "prop": _tools.RODict({1001:52120303,1002:52120303,1003:52120203}),
        "needItems": _tools.ROList([[30000265, 14], [30000266, 14]]),
        "needCoins": _tools.ROList([30000002, 2400])
    }),
    10304: _tools.RODict({
        "ID": 10304,
        "meridian": 1,
        "acupoint": 3,
        "level": 4,
        "prop": _tools.RODict({1001:52120304,1002:52120304,1003:52120204}),
        "needItems": _tools.ROList([[30000265, 16], [30000266, 16]]),
        "needCoins": _tools.ROList([30000002, 2600])
    }),
    10305: _tools.RODict({
        "ID": 10305,
        "meridian": 1,
        "acupoint": 3,
        "level": 5,
        "prop": _tools.RODict({1001:52120305,1002:52120305,1003:52120205}),
        "needItems": _tools.ROList([[30000265, 18], [30000266, 18]]),
        "needCoins": _tools.ROList([30000002, 2900])
    }),
    10401: _tools.RODict({
        "ID": 10401,
        "meridian": 1,
        "acupoint": 4,
        "level": 1,
        "prop": _tools.RODict({1001:52120501,1002:52120501,1003:52120401}),
        "needItems": _tools.ROList([[30000266, 10], [30000263, 10]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    10402: _tools.RODict({
        "ID": 10402,
        "meridian": 1,
        "acupoint": 4,
        "level": 2,
        "prop": _tools.RODict({1001:52120502,1002:52120502,1003:52120402}),
        "needItems": _tools.ROList([[30000266, 12], [30000263, 12]]),
        "needCoins": _tools.ROList([30000002, 2200])
    }),
    10403: _tools.RODict({
        "ID": 10403,
        "meridian": 1,
        "acupoint": 4,
        "level": 3,
        "prop": _tools.RODict({1001:52120503,1002:52120503,1003:52120403}),
        "needItems": _tools.ROList([[30000266, 14], [30000263, 14]]),
        "needCoins": _tools.ROList([30000002, 2400])
    }),
    10404: _tools.RODict({
        "ID": 10404,
        "meridian": 1,
        "acupoint": 4,
        "level": 4,
        "prop": _tools.RODict({1001:52120504,1002:52120504,1003:52120404}),
        "needItems": _tools.ROList([[30000266, 16], [30000263, 16]]),
        "needCoins": _tools.ROList([30000002, 2600])
    }),
    10405: _tools.RODict({
        "ID": 10405,
        "meridian": 1,
        "acupoint": 4,
        "level": 5,
        "prop": _tools.RODict({1001:52120505,1002:52120505,1003:52120405}),
        "needItems": _tools.ROList([[30000266, 18], [30000263, 18]]),
        "needCoins": _tools.ROList([30000002, 2900])
    }),
    10501: _tools.RODict({
        "ID": 10501,
        "meridian": 1,
        "acupoint": 5,
        "level": 1,
        "prop": _tools.RODict({0:52120601}),
        "needItems": _tools.ROList([[30000263, 10], [30000265, 10]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    10502: _tools.RODict({
        "ID": 10502,
        "meridian": 1,
        "acupoint": 5,
        "level": 2,
        "prop": _tools.RODict({0:52120602}),
        "needItems": _tools.ROList([[30000263, 12], [30000265, 12]]),
        "needCoins": _tools.ROList([30000002, 2200])
    }),
    10503: _tools.RODict({
        "ID": 10503,
        "meridian": 1,
        "acupoint": 5,
        "level": 3,
        "prop": _tools.RODict({0:52120603}),
        "needItems": _tools.ROList([[30000263, 14], [30000265, 14]]),
        "needCoins": _tools.ROList([30000002, 2400])
    }),
    10504: _tools.RODict({
        "ID": 10504,
        "meridian": 1,
        "acupoint": 5,
        "level": 4,
        "prop": _tools.RODict({0:52120604}),
        "needItems": _tools.ROList([[30000263, 16], [30000265, 16]]),
        "needCoins": _tools.ROList([30000002, 2600])
    }),
    10505: _tools.RODict({
        "ID": 10505,
        "meridian": 1,
        "acupoint": 5,
        "level": 5,
        "prop": _tools.RODict({0:52120605}),
        "needItems": _tools.ROList([[30000263, 18], [30000265, 18]]),
        "needCoins": _tools.ROList([30000002, 2900])
    }),
    10601: _tools.RODict({
        "ID": 10601,
        "meridian": 1,
        "acupoint": 6,
        "level": 1,
        "prop": _tools.RODict({0:52120701}),
        "needItems": _tools.ROList([[30000264, 10], [30000266, 10]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    10602: _tools.RODict({
        "ID": 10602,
        "meridian": 1,
        "acupoint": 6,
        "level": 2,
        "prop": _tools.RODict({0:52120702}),
        "needItems": _tools.ROList([[30000264, 12], [30000266, 12]]),
        "needCoins": _tools.ROList([30000002, 2200])
    }),
    10603: _tools.RODict({
        "ID": 10603,
        "meridian": 1,
        "acupoint": 6,
        "level": 3,
        "prop": _tools.RODict({0:52120703}),
        "needItems": _tools.ROList([[30000264, 14], [30000266, 14]]),
        "needCoins": _tools.ROList([30000002, 2400])
    }),
    10604: _tools.RODict({
        "ID": 10604,
        "meridian": 1,
        "acupoint": 6,
        "level": 4,
        "prop": _tools.RODict({0:52120704}),
        "needItems": _tools.ROList([[30000264, 16], [30000266, 16]]),
        "needCoins": _tools.ROList([30000002, 2600])
    }),
    10605: _tools.RODict({
        "ID": 10605,
        "meridian": 1,
        "acupoint": 6,
        "level": 5,
        "prop": _tools.RODict({0:52120705}),
        "needItems": _tools.ROList([[30000264, 18], [30000266, 18]]),
        "needCoins": _tools.ROList([30000002, 2900])
    }),
    10701: _tools.RODict({
        "ID": 10701,
        "meridian": 1,
        "acupoint": 7,
        "level": 1,
        "prop": _tools.RODict({0:52120801}),
        "needItems": _tools.ROList([[30000265, 10], [30000264, 10]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    10702: _tools.RODict({
        "ID": 10702,
        "meridian": 1,
        "acupoint": 7,
        "level": 2,
        "prop": _tools.RODict({0:52120802}),
        "needItems": _tools.ROList([[30000265, 12], [30000264, 12]]),
        "needCoins": _tools.ROList([30000002, 2200])
    }),
    10703: _tools.RODict({
        "ID": 10703,
        "meridian": 1,
        "acupoint": 7,
        "level": 3,
        "prop": _tools.RODict({0:52120803}),
        "needItems": _tools.ROList([[30000265, 14], [30000264, 14]]),
        "needCoins": _tools.ROList([30000002, 2400])
    }),
    10704: _tools.RODict({
        "ID": 10704,
        "meridian": 1,
        "acupoint": 7,
        "level": 4,
        "prop": _tools.RODict({0:52120804}),
        "needItems": _tools.ROList([[30000265, 16], [30000264, 16]]),
        "needCoins": _tools.ROList([30000002, 2600])
    }),
    10705: _tools.RODict({
        "ID": 10705,
        "meridian": 1,
        "acupoint": 7,
        "level": 5,
        "prop": _tools.RODict({0:52120805}),
        "needItems": _tools.ROList([[30000265, 18], [30000264, 18]]),
        "needCoins": _tools.ROList([30000002, 2900])
    }),
    10801: _tools.RODict({
        "ID": 10801,
        "meridian": 1,
        "acupoint": 8,
        "level": 1,
        "prop": _tools.RODict({0:52120901}),
        "needItems": _tools.ROList([[30000266, 10], [30000263, 10]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    10802: _tools.RODict({
        "ID": 10802,
        "meridian": 1,
        "acupoint": 8,
        "level": 2,
        "prop": _tools.RODict({0:52120902}),
        "needItems": _tools.ROList([[30000266, 12], [30000263, 12]]),
        "needCoins": _tools.ROList([30000002, 2200])
    }),
    10803: _tools.RODict({
        "ID": 10803,
        "meridian": 1,
        "acupoint": 8,
        "level": 3,
        "prop": _tools.RODict({0:52120903}),
        "needItems": _tools.ROList([[30000266, 14], [30000263, 14]]),
        "needCoins": _tools.ROList([30000002, 2400])
    }),
    10804: _tools.RODict({
        "ID": 10804,
        "meridian": 1,
        "acupoint": 8,
        "level": 4,
        "prop": _tools.RODict({0:52120904}),
        "needItems": _tools.ROList([[30000266, 16], [30000263, 16]]),
        "needCoins": _tools.ROList([30000002, 2600])
    }),
    10805: _tools.RODict({
        "ID": 10805,
        "meridian": 1,
        "acupoint": 8,
        "level": 5,
        "prop": _tools.RODict({0:52120905}),
        "needItems": _tools.ROList([[30000266, 18], [30000263, 18]]),
        "needCoins": _tools.ROList([30000002, 2900])
    }),
    20101: _tools.RODict({
        "ID": 20101,
        "meridian": 2,
        "acupoint": 1,
        "level": 1,
        "prop": _tools.RODict({0:52120006}),
        "needItems": _tools.ROList([[30000263, 20], [30000264, 20]]),
        "needCoins": _tools.ROList([30000002, 3200])
    }),
    20102: _tools.RODict({
        "ID": 20102,
        "meridian": 2,
        "acupoint": 1,
        "level": 2,
        "prop": _tools.RODict({0:52120007}),
        "needItems": _tools.ROList([[30000263, 22], [30000264, 22]]),
        "needCoins": _tools.ROList([30000002, 3500])
    }),
    20103: _tools.RODict({
        "ID": 20103,
        "meridian": 2,
        "acupoint": 1,
        "level": 3,
        "prop": _tools.RODict({0:52120008}),
        "needItems": _tools.ROList([[30000263, 24], [30000264, 24]]),
        "needCoins": _tools.ROList([30000002, 3900])
    }),
    20104: _tools.RODict({
        "ID": 20104,
        "meridian": 2,
        "acupoint": 1,
        "level": 4,
        "prop": _tools.RODict({0:52120009}),
        "needItems": _tools.ROList([[30000263, 26], [30000264, 26]]),
        "needCoins": _tools.ROList([30000002, 4300])
    }),
    20105: _tools.RODict({
        "ID": 20105,
        "meridian": 2,
        "acupoint": 1,
        "level": 5,
        "prop": _tools.RODict({0:52120010}),
        "needItems": _tools.ROList([[30000263, 28], [30000264, 28]]),
        "needCoins": _tools.ROList([30000002, 4700])
    }),
    20201: _tools.RODict({
        "ID": 20201,
        "meridian": 2,
        "acupoint": 2,
        "level": 1,
        "prop": _tools.RODict({0:52120106}),
        "needItems": _tools.ROList([[30000264, 20], [30000265, 20]]),
        "needCoins": _tools.ROList([30000002, 3200])
    }),
    20202: _tools.RODict({
        "ID": 20202,
        "meridian": 2,
        "acupoint": 2,
        "level": 2,
        "prop": _tools.RODict({0:52120107}),
        "needItems": _tools.ROList([[30000264, 22], [30000265, 22]]),
        "needCoins": _tools.ROList([30000002, 3500])
    }),
    20203: _tools.RODict({
        "ID": 20203,
        "meridian": 2,
        "acupoint": 2,
        "level": 3,
        "prop": _tools.RODict({0:52120108}),
        "needItems": _tools.ROList([[30000264, 24], [30000265, 24]]),
        "needCoins": _tools.ROList([30000002, 3900])
    }),
    20204: _tools.RODict({
        "ID": 20204,
        "meridian": 2,
        "acupoint": 2,
        "level": 4,
        "prop": _tools.RODict({0:52120109}),
        "needItems": _tools.ROList([[30000264, 26], [30000265, 26]]),
        "needCoins": _tools.ROList([30000002, 4300])
    }),
    20205: _tools.RODict({
        "ID": 20205,
        "meridian": 2,
        "acupoint": 2,
        "level": 5,
        "prop": _tools.RODict({0:52120110}),
        "needItems": _tools.ROList([[30000264, 28], [30000265, 28]]),
        "needCoins": _tools.ROList([30000002, 4700])
    }),
    20301: _tools.RODict({
        "ID": 20301,
        "meridian": 2,
        "acupoint": 3,
        "level": 1,
        "prop": _tools.RODict({1001:52120306,1002:52120306,1003:52120206}),
        "needItems": _tools.ROList([[30000265, 20], [30000266, 20]]),
        "needCoins": _tools.ROList([30000002, 3200])
    }),
    20302: _tools.RODict({
        "ID": 20302,
        "meridian": 2,
        "acupoint": 3,
        "level": 2,
        "prop": _tools.RODict({1001:52120307,1002:52120307,1003:52120207}),
        "needItems": _tools.ROList([[30000265, 22], [30000266, 22]]),
        "needCoins": _tools.ROList([30000002, 3500])
    }),
    20303: _tools.RODict({
        "ID": 20303,
        "meridian": 2,
        "acupoint": 3,
        "level": 3,
        "prop": _tools.RODict({1001:52120308,1002:52120308,1003:52120208}),
        "needItems": _tools.ROList([[30000265, 24], [30000266, 24]]),
        "needCoins": _tools.ROList([30000002, 3900])
    }),
    20304: _tools.RODict({
        "ID": 20304,
        "meridian": 2,
        "acupoint": 3,
        "level": 4,
        "prop": _tools.RODict({1001:52120309,1002:52120309,1003:52120209}),
        "needItems": _tools.ROList([[30000265, 26], [30000266, 26]]),
        "needCoins": _tools.ROList([30000002, 4300])
    }),
    20305: _tools.RODict({
        "ID": 20305,
        "meridian": 2,
        "acupoint": 3,
        "level": 5,
        "prop": _tools.RODict({1001:52120310,1002:52120310,1003:52120210}),
        "needItems": _tools.ROList([[30000265, 28], [30000266, 28]]),
        "needCoins": _tools.ROList([30000002, 4700])
    }),
    20401: _tools.RODict({
        "ID": 20401,
        "meridian": 2,
        "acupoint": 4,
        "level": 1,
        "prop": _tools.RODict({1001:52120506,1002:52120506,1003:52120406}),
        "needItems": _tools.ROList([[30000266, 20], [30000263, 20]]),
        "needCoins": _tools.ROList([30000002, 3200])
    }),
    20402: _tools.RODict({
        "ID": 20402,
        "meridian": 2,
        "acupoint": 4,
        "level": 2,
        "prop": _tools.RODict({1001:52120507,1002:52120507,1003:52120407}),
        "needItems": _tools.ROList([[30000266, 22], [30000263, 22]]),
        "needCoins": _tools.ROList([30000002, 3500])
    }),
    20403: _tools.RODict({
        "ID": 20403,
        "meridian": 2,
        "acupoint": 4,
        "level": 3,
        "prop": _tools.RODict({1001:52120508,1002:52120508,1003:52120408}),
        "needItems": _tools.ROList([[30000266, 24], [30000263, 24]]),
        "needCoins": _tools.ROList([30000002, 3900])
    }),
    20404: _tools.RODict({
        "ID": 20404,
        "meridian": 2,
        "acupoint": 4,
        "level": 4,
        "prop": _tools.RODict({1001:52120509,1002:52120509,1003:52120409}),
        "needItems": _tools.ROList([[30000266, 26], [30000263, 26]]),
        "needCoins": _tools.ROList([30000002, 4300])
    }),
    20405: _tools.RODict({
        "ID": 20405,
        "meridian": 2,
        "acupoint": 4,
        "level": 5,
        "prop": _tools.RODict({1001:52120510,1002:52120510,1003:52120410}),
        "needItems": _tools.ROList([[30000266, 28], [30000263, 28]]),
        "needCoins": _tools.ROList([30000002, 4700])
    }),
    20501: _tools.RODict({
        "ID": 20501,
        "meridian": 2,
        "acupoint": 5,
        "level": 1,
        "prop": _tools.RODict({0:52120606}),
        "needItems": _tools.ROList([[30000263, 20], [30000265, 20]]),
        "needCoins": _tools.ROList([30000002, 3200])
    }),
    20502: _tools.RODict({
        "ID": 20502,
        "meridian": 2,
        "acupoint": 5,
        "level": 2,
        "prop": _tools.RODict({0:52120607}),
        "needItems": _tools.ROList([[30000263, 22], [30000265, 22]]),
        "needCoins": _tools.ROList([30000002, 3500])
    }),
    20503: _tools.RODict({
        "ID": 20503,
        "meridian": 2,
        "acupoint": 5,
        "level": 3,
        "prop": _tools.RODict({0:52120608}),
        "needItems": _tools.ROList([[30000263, 24], [30000265, 24]]),
        "needCoins": _tools.ROList([30000002, 3900])
    }),
    20504: _tools.RODict({
        "ID": 20504,
        "meridian": 2,
        "acupoint": 5,
        "level": 4,
        "prop": _tools.RODict({0:52120609}),
        "needItems": _tools.ROList([[30000263, 26], [30000265, 26]]),
        "needCoins": _tools.ROList([30000002, 4300])
    }),
    20505: _tools.RODict({
        "ID": 20505,
        "meridian": 2,
        "acupoint": 5,
        "level": 5,
        "prop": _tools.RODict({0:52120610}),
        "needItems": _tools.ROList([[30000263, 28], [30000265, 28]]),
        "needCoins": _tools.ROList([30000002, 4700])
    }),
    20601: _tools.RODict({
        "ID": 20601,
        "meridian": 2,
        "acupoint": 6,
        "level": 1,
        "prop": _tools.RODict({0:52120706}),
        "needItems": _tools.ROList([[30000264, 20], [30000266, 20]]),
        "needCoins": _tools.ROList([30000002, 3200])
    }),
    20602: _tools.RODict({
        "ID": 20602,
        "meridian": 2,
        "acupoint": 6,
        "level": 2,
        "prop": _tools.RODict({0:52120707}),
        "needItems": _tools.ROList([[30000264, 22], [30000266, 22]]),
        "needCoins": _tools.ROList([30000002, 3500])
    }),
    20603: _tools.RODict({
        "ID": 20603,
        "meridian": 2,
        "acupoint": 6,
        "level": 3,
        "prop": _tools.RODict({0:52120708}),
        "needItems": _tools.ROList([[30000264, 24], [30000266, 24]]),
        "needCoins": _tools.ROList([30000002, 3900])
    }),
    20604: _tools.RODict({
        "ID": 20604,
        "meridian": 2,
        "acupoint": 6,
        "level": 4,
        "prop": _tools.RODict({0:52120709}),
        "needItems": _tools.ROList([[30000264, 26], [30000266, 26]]),
        "needCoins": _tools.ROList([30000002, 4300])
    }),
    20605: _tools.RODict({
        "ID": 20605,
        "meridian": 2,
        "acupoint": 6,
        "level": 5,
        "prop": _tools.RODict({0:52120710}),
        "needItems": _tools.ROList([[30000264, 28], [30000266, 28]]),
        "needCoins": _tools.ROList([30000002, 4700])
    }),
    20701: _tools.RODict({
        "ID": 20701,
        "meridian": 2,
        "acupoint": 7,
        "level": 1,
        "prop": _tools.RODict({0:52120806}),
        "needItems": _tools.ROList([[30000265, 20], [30000264, 20]]),
        "needCoins": _tools.ROList([30000002, 3200])
    }),
    20702: _tools.RODict({
        "ID": 20702,
        "meridian": 2,
        "acupoint": 7,
        "level": 2,
        "prop": _tools.RODict({0:52120807}),
        "needItems": _tools.ROList([[30000265, 22], [30000264, 22]]),
        "needCoins": _tools.ROList([30000002, 3500])
    }),
    20703: _tools.RODict({
        "ID": 20703,
        "meridian": 2,
        "acupoint": 7,
        "level": 3,
        "prop": _tools.RODict({0:52120808}),
        "needItems": _tools.ROList([[30000265, 24], [30000264, 24]]),
        "needCoins": _tools.ROList([30000002, 3900])
    }),
    20704: _tools.RODict({
        "ID": 20704,
        "meridian": 2,
        "acupoint": 7,
        "level": 4,
        "prop": _tools.RODict({0:52120809}),
        "needItems": _tools.ROList([[30000265, 26], [30000264, 26]]),
        "needCoins": _tools.ROList([30000002, 4300])
    }),
    20705: _tools.RODict({
        "ID": 20705,
        "meridian": 2,
        "acupoint": 7,
        "level": 5,
        "prop": _tools.RODict({0:52120810}),
        "needItems": _tools.ROList([[30000265, 28], [30000264, 28]]),
        "needCoins": _tools.ROList([30000002, 4700])
    }),
    20801: _tools.RODict({
        "ID": 20801,
        "meridian": 2,
        "acupoint": 8,
        "level": 1,
        "prop": _tools.RODict({0:52120906}),
        "needItems": _tools.ROList([[30000266, 20], [30000263, 20]]),
        "needCoins": _tools.ROList([30000002, 3200])
    }),
    20802: _tools.RODict({
        "ID": 20802,
        "meridian": 2,
        "acupoint": 8,
        "level": 2,
        "prop": _tools.RODict({0:52120907}),
        "needItems": _tools.ROList([[30000266, 22], [30000263, 22]]),
        "needCoins": _tools.ROList([30000002, 3500])
    }),
    20803: _tools.RODict({
        "ID": 20803,
        "meridian": 2,
        "acupoint": 8,
        "level": 3,
        "prop": _tools.RODict({0:52120908}),
        "needItems": _tools.ROList([[30000266, 24], [30000263, 24]]),
        "needCoins": _tools.ROList([30000002, 3900])
    }),
    20804: _tools.RODict({
        "ID": 20804,
        "meridian": 2,
        "acupoint": 8,
        "level": 4,
        "prop": _tools.RODict({0:52120909}),
        "needItems": _tools.ROList([[30000266, 26], [30000263, 26]]),
        "needCoins": _tools.ROList([30000002, 4300])
    }),
    20805: _tools.RODict({
        "ID": 20805,
        "meridian": 2,
        "acupoint": 8,
        "level": 5,
        "prop": _tools.RODict({0:52120910}),
        "needItems": _tools.ROList([[30000266, 28], [30000263, 28]]),
        "needCoins": _tools.ROList([30000002, 4700])
    }),
    30101: _tools.RODict({
        "ID": 30101,
        "meridian": 3,
        "acupoint": 1,
        "level": 1,
        "prop": _tools.RODict({0:52120011}),
        "needItems": _tools.ROList([[30000263, 30], [30000264, 30]]),
        "needCoins": _tools.ROList([30000002, 5200])
    }),
    30102: _tools.RODict({
        "ID": 30102,
        "meridian": 3,
        "acupoint": 1,
        "level": 2,
        "prop": _tools.RODict({0:52120012}),
        "needItems": _tools.ROList([[30000263, 32], [30000264, 32]]),
        "needCoins": _tools.ROList([30000002, 5700])
    }),
    30103: _tools.RODict({
        "ID": 30103,
        "meridian": 3,
        "acupoint": 1,
        "level": 3,
        "prop": _tools.RODict({0:52120013}),
        "needItems": _tools.ROList([[30000263, 34], [30000264, 34]]),
        "needCoins": _tools.ROList([30000002, 6300])
    }),
    30104: _tools.RODict({
        "ID": 30104,
        "meridian": 3,
        "acupoint": 1,
        "level": 4,
        "prop": _tools.RODict({0:52120014}),
        "needItems": _tools.ROList([[30000263, 36], [30000264, 36]]),
        "needCoins": _tools.ROList([30000002, 6900])
    }),
    30105: _tools.RODict({
        "ID": 30105,
        "meridian": 3,
        "acupoint": 1,
        "level": 5,
        "prop": _tools.RODict({0:52120015}),
        "needItems": _tools.ROList([[30000263, 38], [30000264, 38]]),
        "needCoins": _tools.ROList([30000002, 7600])
    }),
    30201: _tools.RODict({
        "ID": 30201,
        "meridian": 3,
        "acupoint": 2,
        "level": 1,
        "prop": _tools.RODict({0:52120111}),
        "needItems": _tools.ROList([[30000264, 30], [30000265, 30]]),
        "needCoins": _tools.ROList([30000002, 5200])
    }),
    30202: _tools.RODict({
        "ID": 30202,
        "meridian": 3,
        "acupoint": 2,
        "level": 2,
        "prop": _tools.RODict({0:52120112}),
        "needItems": _tools.ROList([[30000264, 32], [30000265, 32]]),
        "needCoins": _tools.ROList([30000002, 5700])
    }),
    30203: _tools.RODict({
        "ID": 30203,
        "meridian": 3,
        "acupoint": 2,
        "level": 3,
        "prop": _tools.RODict({0:52120113}),
        "needItems": _tools.ROList([[30000264, 34], [30000265, 34]]),
        "needCoins": _tools.ROList([30000002, 6300])
    }),
    30204: _tools.RODict({
        "ID": 30204,
        "meridian": 3,
        "acupoint": 2,
        "level": 4,
        "prop": _tools.RODict({0:52120114}),
        "needItems": _tools.ROList([[30000264, 36], [30000265, 36]]),
        "needCoins": _tools.ROList([30000002, 6900])
    }),
    30205: _tools.RODict({
        "ID": 30205,
        "meridian": 3,
        "acupoint": 2,
        "level": 5,
        "prop": _tools.RODict({0:52120115}),
        "needItems": _tools.ROList([[30000264, 38], [30000265, 38]]),
        "needCoins": _tools.ROList([30000002, 7600])
    }),
    30301: _tools.RODict({
        "ID": 30301,
        "meridian": 3,
        "acupoint": 3,
        "level": 1,
        "prop": _tools.RODict({1001:52120311,1002:52120311,1003:52120211}),
        "needItems": _tools.ROList([[30000265, 30], [30000266, 30]]),
        "needCoins": _tools.ROList([30000002, 5200])
    }),
    30302: _tools.RODict({
        "ID": 30302,
        "meridian": 3,
        "acupoint": 3,
        "level": 2,
        "prop": _tools.RODict({1001:52120312,1002:52120312,1003:52120212}),
        "needItems": _tools.ROList([[30000265, 32], [30000266, 32]]),
        "needCoins": _tools.ROList([30000002, 5700])
    }),
    30303: _tools.RODict({
        "ID": 30303,
        "meridian": 3,
        "acupoint": 3,
        "level": 3,
        "prop": _tools.RODict({1001:52120313,1002:52120313,1003:52120213}),
        "needItems": _tools.ROList([[30000265, 34], [30000266, 34]]),
        "needCoins": _tools.ROList([30000002, 6300])
    }),
    30304: _tools.RODict({
        "ID": 30304,
        "meridian": 3,
        "acupoint": 3,
        "level": 4,
        "prop": _tools.RODict({1001:52120314,1002:52120314,1003:52120214}),
        "needItems": _tools.ROList([[30000265, 36], [30000266, 36]]),
        "needCoins": _tools.ROList([30000002, 6900])
    }),
    30305: _tools.RODict({
        "ID": 30305,
        "meridian": 3,
        "acupoint": 3,
        "level": 5,
        "prop": _tools.RODict({1001:52120315,1002:52120315,1003:52120215}),
        "needItems": _tools.ROList([[30000265, 38], [30000266, 38]]),
        "needCoins": _tools.ROList([30000002, 7600])
    }),
    30401: _tools.RODict({
        "ID": 30401,
        "meridian": 3,
        "acupoint": 4,
        "level": 1,
        "prop": _tools.RODict({1001:52120511,1002:52120511,1003:52120411}),
        "needItems": _tools.ROList([[30000266, 30], [30000263, 30]]),
        "needCoins": _tools.ROList([30000002, 5200])
    }),
    30402: _tools.RODict({
        "ID": 30402,
        "meridian": 3,
        "acupoint": 4,
        "level": 2,
        "prop": _tools.RODict({1001:52120512,1002:52120512,1003:52120412}),
        "needItems": _tools.ROList([[30000266, 32], [30000263, 32]]),
        "needCoins": _tools.ROList([30000002, 5700])
    }),
    30403: _tools.RODict({
        "ID": 30403,
        "meridian": 3,
        "acupoint": 4,
        "level": 3,
        "prop": _tools.RODict({1001:52120513,1002:52120513,1003:52120413}),
        "needItems": _tools.ROList([[30000266, 34], [30000263, 34]]),
        "needCoins": _tools.ROList([30000002, 6300])
    }),
    30404: _tools.RODict({
        "ID": 30404,
        "meridian": 3,
        "acupoint": 4,
        "level": 4,
        "prop": _tools.RODict({1001:52120514,1002:52120514,1003:52120414}),
        "needItems": _tools.ROList([[30000266, 36], [30000263, 36]]),
        "needCoins": _tools.ROList([30000002, 6900])
    }),
    30405: _tools.RODict({
        "ID": 30405,
        "meridian": 3,
        "acupoint": 4,
        "level": 5,
        "prop": _tools.RODict({1001:52120515,1002:52120515,1003:52120415}),
        "needItems": _tools.ROList([[30000266, 38], [30000263, 38]]),
        "needCoins": _tools.ROList([30000002, 7600])
    }),
    30501: _tools.RODict({
        "ID": 30501,
        "meridian": 3,
        "acupoint": 5,
        "level": 1,
        "prop": _tools.RODict({0:52120611}),
        "needItems": _tools.ROList([[30000263, 30], [30000265, 30]]),
        "needCoins": _tools.ROList([30000002, 5200])
    }),
    30502: _tools.RODict({
        "ID": 30502,
        "meridian": 3,
        "acupoint": 5,
        "level": 2,
        "prop": _tools.RODict({0:52120612}),
        "needItems": _tools.ROList([[30000263, 32], [30000265, 32]]),
        "needCoins": _tools.ROList([30000002, 5700])
    }),
    30503: _tools.RODict({
        "ID": 30503,
        "meridian": 3,
        "acupoint": 5,
        "level": 3,
        "prop": _tools.RODict({0:52120613}),
        "needItems": _tools.ROList([[30000263, 34], [30000265, 34]]),
        "needCoins": _tools.ROList([30000002, 6300])
    }),
    30504: _tools.RODict({
        "ID": 30504,
        "meridian": 3,
        "acupoint": 5,
        "level": 4,
        "prop": _tools.RODict({0:52120614}),
        "needItems": _tools.ROList([[30000263, 36], [30000265, 36]]),
        "needCoins": _tools.ROList([30000002, 6900])
    }),
    30505: _tools.RODict({
        "ID": 30505,
        "meridian": 3,
        "acupoint": 5,
        "level": 5,
        "prop": _tools.RODict({0:52120615}),
        "needItems": _tools.ROList([[30000263, 38], [30000265, 38]]),
        "needCoins": _tools.ROList([30000002, 7600])
    }),
    30601: _tools.RODict({
        "ID": 30601,
        "meridian": 3,
        "acupoint": 6,
        "level": 1,
        "prop": _tools.RODict({0:52120711}),
        "needItems": _tools.ROList([[30000264, 30], [30000266, 30]]),
        "needCoins": _tools.ROList([30000002, 5200])
    }),
    30602: _tools.RODict({
        "ID": 30602,
        "meridian": 3,
        "acupoint": 6,
        "level": 2,
        "prop": _tools.RODict({0:52120712}),
        "needItems": _tools.ROList([[30000264, 32], [30000266, 32]]),
        "needCoins": _tools.ROList([30000002, 5700])
    }),
    30603: _tools.RODict({
        "ID": 30603,
        "meridian": 3,
        "acupoint": 6,
        "level": 3,
        "prop": _tools.RODict({0:52120713}),
        "needItems": _tools.ROList([[30000264, 34], [30000266, 34]]),
        "needCoins": _tools.ROList([30000002, 6300])
    }),
    30604: _tools.RODict({
        "ID": 30604,
        "meridian": 3,
        "acupoint": 6,
        "level": 4,
        "prop": _tools.RODict({0:52120714}),
        "needItems": _tools.ROList([[30000264, 36], [30000266, 36]]),
        "needCoins": _tools.ROList([30000002, 6900])
    }),
    30605: _tools.RODict({
        "ID": 30605,
        "meridian": 3,
        "acupoint": 6,
        "level": 5,
        "prop": _tools.RODict({0:52120715}),
        "needItems": _tools.ROList([[30000264, 38], [30000266, 38]]),
        "needCoins": _tools.ROList([30000002, 7600])
    }),
    30701: _tools.RODict({
        "ID": 30701,
        "meridian": 3,
        "acupoint": 7,
        "level": 1,
        "prop": _tools.RODict({0:52120811}),
        "needItems": _tools.ROList([[30000265, 30], [30000264, 30]]),
        "needCoins": _tools.ROList([30000002, 5200])
    }),
    30702: _tools.RODict({
        "ID": 30702,
        "meridian": 3,
        "acupoint": 7,
        "level": 2,
        "prop": _tools.RODict({0:52120812}),
        "needItems": _tools.ROList([[30000265, 32], [30000264, 32]]),
        "needCoins": _tools.ROList([30000002, 5700])
    }),
    30703: _tools.RODict({
        "ID": 30703,
        "meridian": 3,
        "acupoint": 7,
        "level": 3,
        "prop": _tools.RODict({0:52120813}),
        "needItems": _tools.ROList([[30000265, 34], [30000264, 34]]),
        "needCoins": _tools.ROList([30000002, 6300])
    }),
    30704: _tools.RODict({
        "ID": 30704,
        "meridian": 3,
        "acupoint": 7,
        "level": 4,
        "prop": _tools.RODict({0:52120814}),
        "needItems": _tools.ROList([[30000265, 36], [30000264, 36]]),
        "needCoins": _tools.ROList([30000002, 6900])
    }),
    30705: _tools.RODict({
        "ID": 30705,
        "meridian": 3,
        "acupoint": 7,
        "level": 5,
        "prop": _tools.RODict({0:52120815}),
        "needItems": _tools.ROList([[30000265, 38], [30000264, 38]]),
        "needCoins": _tools.ROList([30000002, 7600])
    }),
    30801: _tools.RODict({
        "ID": 30801,
        "meridian": 3,
        "acupoint": 8,
        "level": 1,
        "prop": _tools.RODict({0:52120911}),
        "needItems": _tools.ROList([[30000266, 30], [30000263, 30]]),
        "needCoins": _tools.ROList([30000002, 5200])
    }),
    30802: _tools.RODict({
        "ID": 30802,
        "meridian": 3,
        "acupoint": 8,
        "level": 2,
        "prop": _tools.RODict({0:52120912}),
        "needItems": _tools.ROList([[30000266, 32], [30000263, 32]]),
        "needCoins": _tools.ROList([30000002, 5700])
    }),
    30803: _tools.RODict({
        "ID": 30803,
        "meridian": 3,
        "acupoint": 8,
        "level": 3,
        "prop": _tools.RODict({0:52120913}),
        "needItems": _tools.ROList([[30000266, 34], [30000263, 34]]),
        "needCoins": _tools.ROList([30000002, 6300])
    }),
    30804: _tools.RODict({
        "ID": 30804,
        "meridian": 3,
        "acupoint": 8,
        "level": 4,
        "prop": _tools.RODict({0:52120914}),
        "needItems": _tools.ROList([[30000266, 36], [30000263, 36]]),
        "needCoins": _tools.ROList([30000002, 6900])
    }),
    30805: _tools.RODict({
        "ID": 30805,
        "meridian": 3,
        "acupoint": 8,
        "level": 5,
        "prop": _tools.RODict({0:52120915}),
        "needItems": _tools.ROList([[30000266, 38], [30000263, 38]]),
        "needCoins": _tools.ROList([30000002, 7600])
    }),
    40101: _tools.RODict({
        "ID": 40101,
        "meridian": 4,
        "acupoint": 1,
        "level": 1,
        "prop": _tools.RODict({0:52120016}),
        "needItems": _tools.ROList([[30000263, 40], [30000264, 40]]),
        "needCoins": _tools.ROList([30000002, 8400])
    }),
    40102: _tools.RODict({
        "ID": 40102,
        "meridian": 4,
        "acupoint": 1,
        "level": 2,
        "prop": _tools.RODict({0:52120017}),
        "needItems": _tools.ROList([[30000263, 42], [30000264, 42]]),
        "needCoins": _tools.ROList([30000002, 9200])
    }),
    40103: _tools.RODict({
        "ID": 40103,
        "meridian": 4,
        "acupoint": 1,
        "level": 3,
        "prop": _tools.RODict({0:52120018}),
        "needItems": _tools.ROList([[30000263, 44], [30000264, 44]]),
        "needCoins": _tools.ROList([30000002, 10100])
    }),
    40104: _tools.RODict({
        "ID": 40104,
        "meridian": 4,
        "acupoint": 1,
        "level": 4,
        "prop": _tools.RODict({0:52120019}),
        "needItems": _tools.ROList([[30000263, 46], [30000264, 46]]),
        "needCoins": _tools.ROList([30000002, 11100])
    }),
    40105: _tools.RODict({
        "ID": 40105,
        "meridian": 4,
        "acupoint": 1,
        "level": 5,
        "prop": _tools.RODict({0:52120020}),
        "needItems": _tools.ROList([[30000263, 48], [30000264, 48]]),
        "needCoins": _tools.ROList([30000002, 12200])
    }),
    40201: _tools.RODict({
        "ID": 40201,
        "meridian": 4,
        "acupoint": 2,
        "level": 1,
        "prop": _tools.RODict({0:52120116}),
        "needItems": _tools.ROList([[30000264, 40], [30000265, 40]]),
        "needCoins": _tools.ROList([30000002, 8400])
    }),
    40202: _tools.RODict({
        "ID": 40202,
        "meridian": 4,
        "acupoint": 2,
        "level": 2,
        "prop": _tools.RODict({0:52120117}),
        "needItems": _tools.ROList([[30000264, 42], [30000265, 42]]),
        "needCoins": _tools.ROList([30000002, 9200])
    }),
    40203: _tools.RODict({
        "ID": 40203,
        "meridian": 4,
        "acupoint": 2,
        "level": 3,
        "prop": _tools.RODict({0:52120118}),
        "needItems": _tools.ROList([[30000264, 44], [30000265, 44]]),
        "needCoins": _tools.ROList([30000002, 10100])
    }),
    40204: _tools.RODict({
        "ID": 40204,
        "meridian": 4,
        "acupoint": 2,
        "level": 4,
        "prop": _tools.RODict({0:52120119}),
        "needItems": _tools.ROList([[30000264, 46], [30000265, 46]]),
        "needCoins": _tools.ROList([30000002, 11100])
    }),
    40205: _tools.RODict({
        "ID": 40205,
        "meridian": 4,
        "acupoint": 2,
        "level": 5,
        "prop": _tools.RODict({0:52120120}),
        "needItems": _tools.ROList([[30000264, 48], [30000265, 48]]),
        "needCoins": _tools.ROList([30000002, 12200])
    }),
    40301: _tools.RODict({
        "ID": 40301,
        "meridian": 4,
        "acupoint": 3,
        "level": 1,
        "prop": _tools.RODict({1001:52120316,1002:52120316,1003:52120216}),
        "needItems": _tools.ROList([[30000265, 40], [30000266, 40]]),
        "needCoins": _tools.ROList([30000002, 8400])
    }),
    40302: _tools.RODict({
        "ID": 40302,
        "meridian": 4,
        "acupoint": 3,
        "level": 2,
        "prop": _tools.RODict({1001:52120317,1002:52120317,1003:52120217}),
        "needItems": _tools.ROList([[30000265, 42], [30000266, 42]]),
        "needCoins": _tools.ROList([30000002, 9200])
    }),
    40303: _tools.RODict({
        "ID": 40303,
        "meridian": 4,
        "acupoint": 3,
        "level": 3,
        "prop": _tools.RODict({1001:52120318,1002:52120318,1003:52120218}),
        "needItems": _tools.ROList([[30000265, 44], [30000266, 44]]),
        "needCoins": _tools.ROList([30000002, 10100])
    }),
    40304: _tools.RODict({
        "ID": 40304,
        "meridian": 4,
        "acupoint": 3,
        "level": 4,
        "prop": _tools.RODict({1001:52120319,1002:52120319,1003:52120219}),
        "needItems": _tools.ROList([[30000265, 46], [30000266, 46]]),
        "needCoins": _tools.ROList([30000002, 11100])
    }),
    40305: _tools.RODict({
        "ID": 40305,
        "meridian": 4,
        "acupoint": 3,
        "level": 5,
        "prop": _tools.RODict({1001:52120320,1002:52120320,1003:52120220}),
        "needItems": _tools.ROList([[30000265, 48], [30000266, 48]]),
        "needCoins": _tools.ROList([30000002, 12200])
    }),
    40401: _tools.RODict({
        "ID": 40401,
        "meridian": 4,
        "acupoint": 4,
        "level": 1,
        "prop": _tools.RODict({1001:52120516,1002:52120516,1003:52120416}),
        "needItems": _tools.ROList([[30000266, 40], [30000263, 40]]),
        "needCoins": _tools.ROList([30000002, 8400])
    }),
    40402: _tools.RODict({
        "ID": 40402,
        "meridian": 4,
        "acupoint": 4,
        "level": 2,
        "prop": _tools.RODict({1001:52120517,1002:52120517,1003:52120417}),
        "needItems": _tools.ROList([[30000266, 42], [30000263, 42]]),
        "needCoins": _tools.ROList([30000002, 9200])
    }),
    40403: _tools.RODict({
        "ID": 40403,
        "meridian": 4,
        "acupoint": 4,
        "level": 3,
        "prop": _tools.RODict({1001:52120518,1002:52120518,1003:52120418}),
        "needItems": _tools.ROList([[30000266, 44], [30000263, 44]]),
        "needCoins": _tools.ROList([30000002, 10100])
    }),
    40404: _tools.RODict({
        "ID": 40404,
        "meridian": 4,
        "acupoint": 4,
        "level": 4,
        "prop": _tools.RODict({1001:52120519,1002:52120519,1003:52120419}),
        "needItems": _tools.ROList([[30000266, 46], [30000263, 46]]),
        "needCoins": _tools.ROList([30000002, 11100])
    }),
    40405: _tools.RODict({
        "ID": 40405,
        "meridian": 4,
        "acupoint": 4,
        "level": 5,
        "prop": _tools.RODict({1001:52120520,1002:52120520,1003:52120420}),
        "needItems": _tools.ROList([[30000266, 48], [30000263, 48]]),
        "needCoins": _tools.ROList([30000002, 12200])
    }),
    40501: _tools.RODict({
        "ID": 40501,
        "meridian": 4,
        "acupoint": 5,
        "level": 1,
        "prop": _tools.RODict({0:52120616}),
        "needItems": _tools.ROList([[30000263, 40], [30000265, 40]]),
        "needCoins": _tools.ROList([30000002, 8400])
    }),
    40502: _tools.RODict({
        "ID": 40502,
        "meridian": 4,
        "acupoint": 5,
        "level": 2,
        "prop": _tools.RODict({0:52120617}),
        "needItems": _tools.ROList([[30000263, 42], [30000265, 42]]),
        "needCoins": _tools.ROList([30000002, 9200])
    }),
    40503: _tools.RODict({
        "ID": 40503,
        "meridian": 4,
        "acupoint": 5,
        "level": 3,
        "prop": _tools.RODict({0:52120618}),
        "needItems": _tools.ROList([[30000263, 44], [30000265, 44]]),
        "needCoins": _tools.ROList([30000002, 10100])
    }),
    40504: _tools.RODict({
        "ID": 40504,
        "meridian": 4,
        "acupoint": 5,
        "level": 4,
        "prop": _tools.RODict({0:52120619}),
        "needItems": _tools.ROList([[30000263, 46], [30000265, 46]]),
        "needCoins": _tools.ROList([30000002, 11100])
    }),
    40505: _tools.RODict({
        "ID": 40505,
        "meridian": 4,
        "acupoint": 5,
        "level": 5,
        "prop": _tools.RODict({0:52120620}),
        "needItems": _tools.ROList([[30000263, 48], [30000265, 48]]),
        "needCoins": _tools.ROList([30000002, 12200])
    }),
    40601: _tools.RODict({
        "ID": 40601,
        "meridian": 4,
        "acupoint": 6,
        "level": 1,
        "prop": _tools.RODict({0:52120716}),
        "needItems": _tools.ROList([[30000264, 40], [30000266, 40]]),
        "needCoins": _tools.ROList([30000002, 8400])
    }),
    40602: _tools.RODict({
        "ID": 40602,
        "meridian": 4,
        "acupoint": 6,
        "level": 2,
        "prop": _tools.RODict({0:52120717}),
        "needItems": _tools.ROList([[30000264, 42], [30000266, 42]]),
        "needCoins": _tools.ROList([30000002, 9200])
    }),
    40603: _tools.RODict({
        "ID": 40603,
        "meridian": 4,
        "acupoint": 6,
        "level": 3,
        "prop": _tools.RODict({0:52120718}),
        "needItems": _tools.ROList([[30000264, 44], [30000266, 44]]),
        "needCoins": _tools.ROList([30000002, 10100])
    }),
    40604: _tools.RODict({
        "ID": 40604,
        "meridian": 4,
        "acupoint": 6,
        "level": 4,
        "prop": _tools.RODict({0:52120719}),
        "needItems": _tools.ROList([[30000264, 46], [30000266, 46]]),
        "needCoins": _tools.ROList([30000002, 11100])
    }),
    40605: _tools.RODict({
        "ID": 40605,
        "meridian": 4,
        "acupoint": 6,
        "level": 5,
        "prop": _tools.RODict({0:52120720}),
        "needItems": _tools.ROList([[30000264, 48], [30000266, 48]]),
        "needCoins": _tools.ROList([30000002, 12200])
    }),
    40701: _tools.RODict({
        "ID": 40701,
        "meridian": 4,
        "acupoint": 7,
        "level": 1,
        "prop": _tools.RODict({0:52120816}),
        "needItems": _tools.ROList([[30000265, 40], [30000264, 40]]),
        "needCoins": _tools.ROList([30000002, 8400])
    }),
    40702: _tools.RODict({
        "ID": 40702,
        "meridian": 4,
        "acupoint": 7,
        "level": 2,
        "prop": _tools.RODict({0:52120817}),
        "needItems": _tools.ROList([[30000265, 42], [30000264, 42]]),
        "needCoins": _tools.ROList([30000002, 9200])
    }),
    40703: _tools.RODict({
        "ID": 40703,
        "meridian": 4,
        "acupoint": 7,
        "level": 3,
        "prop": _tools.RODict({0:52120818}),
        "needItems": _tools.ROList([[30000265, 44], [30000264, 44]]),
        "needCoins": _tools.ROList([30000002, 10100])
    }),
    40704: _tools.RODict({
        "ID": 40704,
        "meridian": 4,
        "acupoint": 7,
        "level": 4,
        "prop": _tools.RODict({0:52120819}),
        "needItems": _tools.ROList([[30000265, 46], [30000264, 46]]),
        "needCoins": _tools.ROList([30000002, 11100])
    }),
    40705: _tools.RODict({
        "ID": 40705,
        "meridian": 4,
        "acupoint": 7,
        "level": 5,
        "prop": _tools.RODict({0:52120820}),
        "needItems": _tools.ROList([[30000265, 48], [30000264, 48]]),
        "needCoins": _tools.ROList([30000002, 12200])
    }),
    40801: _tools.RODict({
        "ID": 40801,
        "meridian": 4,
        "acupoint": 8,
        "level": 1,
        "prop": _tools.RODict({0:52120916}),
        "needItems": _tools.ROList([[30000266, 40], [30000263, 40]]),
        "needCoins": _tools.ROList([30000002, 8400])
    }),
    40802: _tools.RODict({
        "ID": 40802,
        "meridian": 4,
        "acupoint": 8,
        "level": 2,
        "prop": _tools.RODict({0:52120917}),
        "needItems": _tools.ROList([[30000266, 42], [30000263, 42]]),
        "needCoins": _tools.ROList([30000002, 9200])
    }),
    40803: _tools.RODict({
        "ID": 40803,
        "meridian": 4,
        "acupoint": 8,
        "level": 3,
        "prop": _tools.RODict({0:52120918}),
        "needItems": _tools.ROList([[30000266, 44], [30000263, 44]]),
        "needCoins": _tools.ROList([30000002, 10100])
    }),
    40804: _tools.RODict({
        "ID": 40804,
        "meridian": 4,
        "acupoint": 8,
        "level": 4,
        "prop": _tools.RODict({0:52120919}),
        "needItems": _tools.ROList([[30000266, 46], [30000263, 46]]),
        "needCoins": _tools.ROList([30000002, 11100])
    }),
    40805: _tools.RODict({
        "ID": 40805,
        "meridian": 4,
        "acupoint": 8,
        "level": 5,
        "prop": _tools.RODict({0:52120920}),
        "needItems": _tools.ROList([[30000266, 48], [30000263, 48]]),
        "needCoins": _tools.ROList([30000002, 12200])
    }),
    50101: _tools.RODict({
        "ID": 50101,
        "meridian": 5,
        "acupoint": 1,
        "level": 1,
        "prop": _tools.RODict({0:52120021}),
        "needItems": _tools.ROList([[30000263, 50], [30000264, 50]]),
        "needCoins": _tools.ROList([30000002, 13400])
    }),
    50102: _tools.RODict({
        "ID": 50102,
        "meridian": 5,
        "acupoint": 1,
        "level": 2,
        "prop": _tools.RODict({0:52120022}),
        "needItems": _tools.ROList([[30000263, 52], [30000264, 52]]),
        "needCoins": _tools.ROList([30000002, 14700])
    }),
    50103: _tools.RODict({
        "ID": 50103,
        "meridian": 5,
        "acupoint": 1,
        "level": 3,
        "prop": _tools.RODict({0:52120023}),
        "needItems": _tools.ROList([[30000263, 54], [30000264, 54]]),
        "needCoins": _tools.ROList([30000002, 16200])
    }),
    50104: _tools.RODict({
        "ID": 50104,
        "meridian": 5,
        "acupoint": 1,
        "level": 4,
        "prop": _tools.RODict({0:52120024}),
        "needItems": _tools.ROList([[30000263, 56], [30000264, 56]]),
        "needCoins": _tools.ROList([30000002, 17800])
    }),
    50105: _tools.RODict({
        "ID": 50105,
        "meridian": 5,
        "acupoint": 1,
        "level": 5,
        "prop": _tools.RODict({0:52120025}),
        "needItems": _tools.ROList([[30000263, 58], [30000264, 58]]),
        "needCoins": _tools.ROList([30000002, 19600])
    }),
    50201: _tools.RODict({
        "ID": 50201,
        "meridian": 5,
        "acupoint": 2,
        "level": 1,
        "prop": _tools.RODict({0:52120121}),
        "needItems": _tools.ROList([[30000264, 50], [30000265, 50]]),
        "needCoins": _tools.ROList([30000002, 13400])
    }),
    50202: _tools.RODict({
        "ID": 50202,
        "meridian": 5,
        "acupoint": 2,
        "level": 2,
        "prop": _tools.RODict({0:52120122}),
        "needItems": _tools.ROList([[30000264, 52], [30000265, 52]]),
        "needCoins": _tools.ROList([30000002, 14700])
    }),
    50203: _tools.RODict({
        "ID": 50203,
        "meridian": 5,
        "acupoint": 2,
        "level": 3,
        "prop": _tools.RODict({0:52120123}),
        "needItems": _tools.ROList([[30000264, 54], [30000265, 54]]),
        "needCoins": _tools.ROList([30000002, 16200])
    }),
    50204: _tools.RODict({
        "ID": 50204,
        "meridian": 5,
        "acupoint": 2,
        "level": 4,
        "prop": _tools.RODict({0:52120124}),
        "needItems": _tools.ROList([[30000264, 56], [30000265, 56]]),
        "needCoins": _tools.ROList([30000002, 17800])
    }),
    50205: _tools.RODict({
        "ID": 50205,
        "meridian": 5,
        "acupoint": 2,
        "level": 5,
        "prop": _tools.RODict({0:52120125}),
        "needItems": _tools.ROList([[30000264, 58], [30000265, 58]]),
        "needCoins": _tools.ROList([30000002, 19600])
    }),
    50301: _tools.RODict({
        "ID": 50301,
        "meridian": 5,
        "acupoint": 3,
        "level": 1,
        "prop": _tools.RODict({1001:52120321,1002:52120321,1003:52120221}),
        "needItems": _tools.ROList([[30000265, 50], [30000266, 50]]),
        "needCoins": _tools.ROList([30000002, 13400])
    }),
    50302: _tools.RODict({
        "ID": 50302,
        "meridian": 5,
        "acupoint": 3,
        "level": 2,
        "prop": _tools.RODict({1001:52120322,1002:52120322,1003:52120222}),
        "needItems": _tools.ROList([[30000265, 52], [30000266, 52]]),
        "needCoins": _tools.ROList([30000002, 14700])
    }),
    50303: _tools.RODict({
        "ID": 50303,
        "meridian": 5,
        "acupoint": 3,
        "level": 3,
        "prop": _tools.RODict({1001:52120323,1002:52120323,1003:52120223}),
        "needItems": _tools.ROList([[30000265, 54], [30000266, 54]]),
        "needCoins": _tools.ROList([30000002, 16200])
    }),
    50304: _tools.RODict({
        "ID": 50304,
        "meridian": 5,
        "acupoint": 3,
        "level": 4,
        "prop": _tools.RODict({1001:52120324,1002:52120324,1003:52120224}),
        "needItems": _tools.ROList([[30000265, 56], [30000266, 56]]),
        "needCoins": _tools.ROList([30000002, 17800])
    }),
    50305: _tools.RODict({
        "ID": 50305,
        "meridian": 5,
        "acupoint": 3,
        "level": 5,
        "prop": _tools.RODict({1001:52120325,1002:52120325,1003:52120225}),
        "needItems": _tools.ROList([[30000265, 58], [30000266, 58]]),
        "needCoins": _tools.ROList([30000002, 19600])
    }),
    50401: _tools.RODict({
        "ID": 50401,
        "meridian": 5,
        "acupoint": 4,
        "level": 1,
        "prop": _tools.RODict({1001:52120521,1002:52120521,1003:52120421}),
        "needItems": _tools.ROList([[30000266, 50], [30000263, 50]]),
        "needCoins": _tools.ROList([30000002, 13400])
    }),
    50402: _tools.RODict({
        "ID": 50402,
        "meridian": 5,
        "acupoint": 4,
        "level": 2,
        "prop": _tools.RODict({1001:52120522,1002:52120522,1003:52120422}),
        "needItems": _tools.ROList([[30000266, 52], [30000263, 52]]),
        "needCoins": _tools.ROList([30000002, 14700])
    }),
    50403: _tools.RODict({
        "ID": 50403,
        "meridian": 5,
        "acupoint": 4,
        "level": 3,
        "prop": _tools.RODict({1001:52120523,1002:52120523,1003:52120423}),
        "needItems": _tools.ROList([[30000266, 54], [30000263, 54]]),
        "needCoins": _tools.ROList([30000002, 16200])
    }),
    50404: _tools.RODict({
        "ID": 50404,
        "meridian": 5,
        "acupoint": 4,
        "level": 4,
        "prop": _tools.RODict({1001:52120524,1002:52120524,1003:52120424}),
        "needItems": _tools.ROList([[30000266, 56], [30000263, 56]]),
        "needCoins": _tools.ROList([30000002, 17800])
    }),
    50405: _tools.RODict({
        "ID": 50405,
        "meridian": 5,
        "acupoint": 4,
        "level": 5,
        "prop": _tools.RODict({1001:52120525,1002:52120525,1003:52120425}),
        "needItems": _tools.ROList([[30000266, 58], [30000263, 58]]),
        "needCoins": _tools.ROList([30000002, 19600])
    }),
    50501: _tools.RODict({
        "ID": 50501,
        "meridian": 5,
        "acupoint": 5,
        "level": 1,
        "prop": _tools.RODict({0:52120621}),
        "needItems": _tools.ROList([[30000263, 50], [30000265, 50]]),
        "needCoins": _tools.ROList([30000002, 13400])
    }),
    50502: _tools.RODict({
        "ID": 50502,
        "meridian": 5,
        "acupoint": 5,
        "level": 2,
        "prop": _tools.RODict({0:52120622}),
        "needItems": _tools.ROList([[30000263, 52], [30000265, 52]]),
        "needCoins": _tools.ROList([30000002, 14700])
    }),
    50503: _tools.RODict({
        "ID": 50503,
        "meridian": 5,
        "acupoint": 5,
        "level": 3,
        "prop": _tools.RODict({0:52120623}),
        "needItems": _tools.ROList([[30000263, 54], [30000265, 54]]),
        "needCoins": _tools.ROList([30000002, 16200])
    }),
    50504: _tools.RODict({
        "ID": 50504,
        "meridian": 5,
        "acupoint": 5,
        "level": 4,
        "prop": _tools.RODict({0:52120624}),
        "needItems": _tools.ROList([[30000263, 56], [30000265, 56]]),
        "needCoins": _tools.ROList([30000002, 17800])
    }),
    50505: _tools.RODict({
        "ID": 50505,
        "meridian": 5,
        "acupoint": 5,
        "level": 5,
        "prop": _tools.RODict({0:52120625}),
        "needItems": _tools.ROList([[30000263, 58], [30000265, 58]]),
        "needCoins": _tools.ROList([30000002, 19600])
    }),
    50601: _tools.RODict({
        "ID": 50601,
        "meridian": 5,
        "acupoint": 6,
        "level": 1,
        "prop": _tools.RODict({0:52120721}),
        "needItems": _tools.ROList([[30000264, 50], [30000266, 50]]),
        "needCoins": _tools.ROList([30000002, 13400])
    }),
    50602: _tools.RODict({
        "ID": 50602,
        "meridian": 5,
        "acupoint": 6,
        "level": 2,
        "prop": _tools.RODict({0:52120722}),
        "needItems": _tools.ROList([[30000264, 52], [30000266, 52]]),
        "needCoins": _tools.ROList([30000002, 14700])
    }),
    50603: _tools.RODict({
        "ID": 50603,
        "meridian": 5,
        "acupoint": 6,
        "level": 3,
        "prop": _tools.RODict({0:52120723}),
        "needItems": _tools.ROList([[30000264, 54], [30000266, 54]]),
        "needCoins": _tools.ROList([30000002, 16200])
    }),
    50604: _tools.RODict({
        "ID": 50604,
        "meridian": 5,
        "acupoint": 6,
        "level": 4,
        "prop": _tools.RODict({0:52120724}),
        "needItems": _tools.ROList([[30000264, 56], [30000266, 56]]),
        "needCoins": _tools.ROList([30000002, 17800])
    }),
    50605: _tools.RODict({
        "ID": 50605,
        "meridian": 5,
        "acupoint": 6,
        "level": 5,
        "prop": _tools.RODict({0:52120725}),
        "needItems": _tools.ROList([[30000264, 58], [30000266, 58]]),
        "needCoins": _tools.ROList([30000002, 19600])
    }),
    50701: _tools.RODict({
        "ID": 50701,
        "meridian": 5,
        "acupoint": 7,
        "level": 1,
        "prop": _tools.RODict({0:52120821}),
        "needItems": _tools.ROList([[30000265, 50], [30000264, 50]]),
        "needCoins": _tools.ROList([30000002, 13400])
    }),
    50702: _tools.RODict({
        "ID": 50702,
        "meridian": 5,
        "acupoint": 7,
        "level": 2,
        "prop": _tools.RODict({0:52120822}),
        "needItems": _tools.ROList([[30000265, 52], [30000264, 52]]),
        "needCoins": _tools.ROList([30000002, 14700])
    }),
    50703: _tools.RODict({
        "ID": 50703,
        "meridian": 5,
        "acupoint": 7,
        "level": 3,
        "prop": _tools.RODict({0:52120823}),
        "needItems": _tools.ROList([[30000265, 54], [30000264, 54]]),
        "needCoins": _tools.ROList([30000002, 16200])
    }),
    50704: _tools.RODict({
        "ID": 50704,
        "meridian": 5,
        "acupoint": 7,
        "level": 4,
        "prop": _tools.RODict({0:52120824}),
        "needItems": _tools.ROList([[30000265, 56], [30000264, 56]]),
        "needCoins": _tools.ROList([30000002, 17800])
    }),
    50705: _tools.RODict({
        "ID": 50705,
        "meridian": 5,
        "acupoint": 7,
        "level": 5,
        "prop": _tools.RODict({0:52120825}),
        "needItems": _tools.ROList([[30000265, 58], [30000264, 58]]),
        "needCoins": _tools.ROList([30000002, 19600])
    }),
    50801: _tools.RODict({
        "ID": 50801,
        "meridian": 5,
        "acupoint": 8,
        "level": 1,
        "prop": _tools.RODict({0:52120921}),
        "needItems": _tools.ROList([[30000266, 50], [30000263, 50]]),
        "needCoins": _tools.ROList([30000002, 13400])
    }),
    50802: _tools.RODict({
        "ID": 50802,
        "meridian": 5,
        "acupoint": 8,
        "level": 2,
        "prop": _tools.RODict({0:52120922}),
        "needItems": _tools.ROList([[30000266, 52], [30000263, 52]]),
        "needCoins": _tools.ROList([30000002, 14700])
    }),
    50803: _tools.RODict({
        "ID": 50803,
        "meridian": 5,
        "acupoint": 8,
        "level": 3,
        "prop": _tools.RODict({0:52120923}),
        "needItems": _tools.ROList([[30000266, 54], [30000263, 54]]),
        "needCoins": _tools.ROList([30000002, 16200])
    }),
    50804: _tools.RODict({
        "ID": 50804,
        "meridian": 5,
        "acupoint": 8,
        "level": 4,
        "prop": _tools.RODict({0:52120924}),
        "needItems": _tools.ROList([[30000266, 56], [30000263, 56]]),
        "needCoins": _tools.ROList([30000002, 17800])
    }),
    50805: _tools.RODict({
        "ID": 50805,
        "meridian": 5,
        "acupoint": 8,
        "level": 5,
        "prop": _tools.RODict({0:52120925}),
        "needItems": _tools.ROList([[30000266, 58], [30000263, 58]]),
        "needCoins": _tools.ROList([30000002, 19600])
    }),
    60101: _tools.RODict({
        "ID": 60101,
        "meridian": 6,
        "acupoint": 1,
        "level": 1,
        "prop": _tools.RODict({0:52120026}),
        "needItems": _tools.ROList([[30000267, 10], [30000268, 10]]),
        "needCoins": _tools.ROList([30000002, 21600])
    }),
    60102: _tools.RODict({
        "ID": 60102,
        "meridian": 6,
        "acupoint": 1,
        "level": 2,
        "prop": _tools.RODict({0:52120027}),
        "needItems": _tools.ROList([[30000267, 12], [30000268, 12]]),
        "needCoins": _tools.ROList([30000002, 23800])
    }),
    60103: _tools.RODict({
        "ID": 60103,
        "meridian": 6,
        "acupoint": 1,
        "level": 3,
        "prop": _tools.RODict({0:52120028}),
        "needItems": _tools.ROList([[30000267, 14], [30000268, 14]]),
        "needCoins": _tools.ROList([30000002, 26200])
    }),
    60104: _tools.RODict({
        "ID": 60104,
        "meridian": 6,
        "acupoint": 1,
        "level": 4,
        "prop": _tools.RODict({0:52120029}),
        "needItems": _tools.ROList([[30000267, 16], [30000268, 16]]),
        "needCoins": _tools.ROList([30000002, 28800])
    }),
    60105: _tools.RODict({
        "ID": 60105,
        "meridian": 6,
        "acupoint": 1,
        "level": 5,
        "prop": _tools.RODict({0:52120030}),
        "needItems": _tools.ROList([[30000267, 18], [30000268, 18]]),
        "needCoins": _tools.ROList([30000002, 31700])
    }),
    60201: _tools.RODict({
        "ID": 60201,
        "meridian": 6,
        "acupoint": 2,
        "level": 1,
        "prop": _tools.RODict({0:52120126}),
        "needItems": _tools.ROList([[30000267, 10], [30000268, 10]]),
        "needCoins": _tools.ROList([30000002, 21600])
    }),
    60202: _tools.RODict({
        "ID": 60202,
        "meridian": 6,
        "acupoint": 2,
        "level": 2,
        "prop": _tools.RODict({0:52120127}),
        "needItems": _tools.ROList([[30000267, 12], [30000268, 12]]),
        "needCoins": _tools.ROList([30000002, 23800])
    }),
    60203: _tools.RODict({
        "ID": 60203,
        "meridian": 6,
        "acupoint": 2,
        "level": 3,
        "prop": _tools.RODict({0:52120128}),
        "needItems": _tools.ROList([[30000267, 14], [30000268, 14]]),
        "needCoins": _tools.ROList([30000002, 26200])
    }),
    60204: _tools.RODict({
        "ID": 60204,
        "meridian": 6,
        "acupoint": 2,
        "level": 4,
        "prop": _tools.RODict({0:52120129}),
        "needItems": _tools.ROList([[30000267, 16], [30000268, 16]]),
        "needCoins": _tools.ROList([30000002, 28800])
    }),
    60205: _tools.RODict({
        "ID": 60205,
        "meridian": 6,
        "acupoint": 2,
        "level": 5,
        "prop": _tools.RODict({0:52120130}),
        "needItems": _tools.ROList([[30000267, 18], [30000268, 18]]),
        "needCoins": _tools.ROList([30000002, 31700])
    }),
    60301: _tools.RODict({
        "ID": 60301,
        "meridian": 6,
        "acupoint": 3,
        "level": 1,
        "prop": _tools.RODict({1001:52120326,1002:52120326,1003:52120226}),
        "needItems": _tools.ROList([[30000267, 10], [30000268, 10]]),
        "needCoins": _tools.ROList([30000002, 21600])
    }),
    60302: _tools.RODict({
        "ID": 60302,
        "meridian": 6,
        "acupoint": 3,
        "level": 2,
        "prop": _tools.RODict({1001:52120327,1002:52120327,1003:52120227}),
        "needItems": _tools.ROList([[30000267, 12], [30000268, 12]]),
        "needCoins": _tools.ROList([30000002, 23800])
    }),
    60303: _tools.RODict({
        "ID": 60303,
        "meridian": 6,
        "acupoint": 3,
        "level": 3,
        "prop": _tools.RODict({1001:52120328,1002:52120328,1003:52120228}),
        "needItems": _tools.ROList([[30000267, 14], [30000268, 14]]),
        "needCoins": _tools.ROList([30000002, 26200])
    }),
    60304: _tools.RODict({
        "ID": 60304,
        "meridian": 6,
        "acupoint": 3,
        "level": 4,
        "prop": _tools.RODict({1001:52120329,1002:52120329,1003:52120229}),
        "needItems": _tools.ROList([[30000267, 16], [30000268, 16]]),
        "needCoins": _tools.ROList([30000002, 28800])
    }),
    60305: _tools.RODict({
        "ID": 60305,
        "meridian": 6,
        "acupoint": 3,
        "level": 5,
        "prop": _tools.RODict({1001:52120330,1002:52120330,1003:52120230}),
        "needItems": _tools.ROList([[30000267, 18], [30000268, 18]]),
        "needCoins": _tools.ROList([30000002, 31700])
    }),
    60401: _tools.RODict({
        "ID": 60401,
        "meridian": 6,
        "acupoint": 4,
        "level": 1,
        "prop": _tools.RODict({1001:52120526,1002:52120526,1003:52120426}),
        "needItems": _tools.ROList([[30000267, 10], [30000268, 10]]),
        "needCoins": _tools.ROList([30000002, 21600])
    }),
    60402: _tools.RODict({
        "ID": 60402,
        "meridian": 6,
        "acupoint": 4,
        "level": 2,
        "prop": _tools.RODict({1001:52120527,1002:52120527,1003:52120427}),
        "needItems": _tools.ROList([[30000267, 12], [30000268, 12]]),
        "needCoins": _tools.ROList([30000002, 23800])
    }),
    60403: _tools.RODict({
        "ID": 60403,
        "meridian": 6,
        "acupoint": 4,
        "level": 3,
        "prop": _tools.RODict({1001:52120528,1002:52120528,1003:52120428}),
        "needItems": _tools.ROList([[30000267, 14], [30000268, 14]]),
        "needCoins": _tools.ROList([30000002, 26200])
    }),
    60404: _tools.RODict({
        "ID": 60404,
        "meridian": 6,
        "acupoint": 4,
        "level": 4,
        "prop": _tools.RODict({1001:52120529,1002:52120529,1003:52120429}),
        "needItems": _tools.ROList([[30000267, 16], [30000268, 16]]),
        "needCoins": _tools.ROList([30000002, 28800])
    }),
    60405: _tools.RODict({
        "ID": 60405,
        "meridian": 6,
        "acupoint": 4,
        "level": 5,
        "prop": _tools.RODict({1001:52120530,1002:52120530,1003:52120430}),
        "needItems": _tools.ROList([[30000267, 18], [30000268, 18]]),
        "needCoins": _tools.ROList([30000002, 31700])
    }),
    60501: _tools.RODict({
        "ID": 60501,
        "meridian": 6,
        "acupoint": 5,
        "level": 1,
        "prop": _tools.RODict({0:52120626}),
        "needItems": _tools.ROList([[30000267, 10], [30000268, 10]]),
        "needCoins": _tools.ROList([30000002, 21600])
    }),
    60502: _tools.RODict({
        "ID": 60502,
        "meridian": 6,
        "acupoint": 5,
        "level": 2,
        "prop": _tools.RODict({0:52120627}),
        "needItems": _tools.ROList([[30000267, 12], [30000268, 12]]),
        "needCoins": _tools.ROList([30000002, 23800])
    }),
    60503: _tools.RODict({
        "ID": 60503,
        "meridian": 6,
        "acupoint": 5,
        "level": 3,
        "prop": _tools.RODict({0:52120628}),
        "needItems": _tools.ROList([[30000267, 14], [30000268, 14]]),
        "needCoins": _tools.ROList([30000002, 26200])
    }),
    60504: _tools.RODict({
        "ID": 60504,
        "meridian": 6,
        "acupoint": 5,
        "level": 4,
        "prop": _tools.RODict({0:52120629}),
        "needItems": _tools.ROList([[30000267, 16], [30000268, 16]]),
        "needCoins": _tools.ROList([30000002, 28800])
    }),
    60505: _tools.RODict({
        "ID": 60505,
        "meridian": 6,
        "acupoint": 5,
        "level": 5,
        "prop": _tools.RODict({0:52120630}),
        "needItems": _tools.ROList([[30000267, 18], [30000268, 18]]),
        "needCoins": _tools.ROList([30000002, 31700])
    }),
    60601: _tools.RODict({
        "ID": 60601,
        "meridian": 6,
        "acupoint": 6,
        "level": 1,
        "prop": _tools.RODict({0:52120726}),
        "needItems": _tools.ROList([[30000267, 10], [30000268, 10]]),
        "needCoins": _tools.ROList([30000002, 21600])
    }),
    60602: _tools.RODict({
        "ID": 60602,
        "meridian": 6,
        "acupoint": 6,
        "level": 2,
        "prop": _tools.RODict({0:52120727}),
        "needItems": _tools.ROList([[30000267, 12], [30000268, 12]]),
        "needCoins": _tools.ROList([30000002, 23800])
    }),
    60603: _tools.RODict({
        "ID": 60603,
        "meridian": 6,
        "acupoint": 6,
        "level": 3,
        "prop": _tools.RODict({0:52120728}),
        "needItems": _tools.ROList([[30000267, 14], [30000268, 14]]),
        "needCoins": _tools.ROList([30000002, 26200])
    }),
    60604: _tools.RODict({
        "ID": 60604,
        "meridian": 6,
        "acupoint": 6,
        "level": 4,
        "prop": _tools.RODict({0:52120729}),
        "needItems": _tools.ROList([[30000267, 16], [30000268, 16]]),
        "needCoins": _tools.ROList([30000002, 28800])
    }),
    60605: _tools.RODict({
        "ID": 60605,
        "meridian": 6,
        "acupoint": 6,
        "level": 5,
        "prop": _tools.RODict({0:52120730}),
        "needItems": _tools.ROList([[30000267, 18], [30000268, 18]]),
        "needCoins": _tools.ROList([30000002, 31700])
    }),
    60701: _tools.RODict({
        "ID": 60701,
        "meridian": 6,
        "acupoint": 7,
        "level": 1,
        "prop": _tools.RODict({0:52120826}),
        "needItems": _tools.ROList([[30000267, 10], [30000268, 10]]),
        "needCoins": _tools.ROList([30000002, 21600])
    }),
    60702: _tools.RODict({
        "ID": 60702,
        "meridian": 6,
        "acupoint": 7,
        "level": 2,
        "prop": _tools.RODict({0:52120827}),
        "needItems": _tools.ROList([[30000267, 12], [30000268, 12]]),
        "needCoins": _tools.ROList([30000002, 23800])
    }),
    60703: _tools.RODict({
        "ID": 60703,
        "meridian": 6,
        "acupoint": 7,
        "level": 3,
        "prop": _tools.RODict({0:52120828}),
        "needItems": _tools.ROList([[30000267, 14], [30000268, 14]]),
        "needCoins": _tools.ROList([30000002, 26200])
    }),
    60704: _tools.RODict({
        "ID": 60704,
        "meridian": 6,
        "acupoint": 7,
        "level": 4,
        "prop": _tools.RODict({0:52120829}),
        "needItems": _tools.ROList([[30000267, 16], [30000268, 16]]),
        "needCoins": _tools.ROList([30000002, 28800])
    }),
    60705: _tools.RODict({
        "ID": 60705,
        "meridian": 6,
        "acupoint": 7,
        "level": 5,
        "prop": _tools.RODict({0:52120830}),
        "needItems": _tools.ROList([[30000267, 18], [30000268, 18]]),
        "needCoins": _tools.ROList([30000002, 31700])
    }),
    60801: _tools.RODict({
        "ID": 60801,
        "meridian": 6,
        "acupoint": 8,
        "level": 1,
        "prop": _tools.RODict({0:52120926}),
        "needItems": _tools.ROList([[30000267, 10], [30000268, 10]]),
        "needCoins": _tools.ROList([30000002, 21600])
    }),
    60802: _tools.RODict({
        "ID": 60802,
        "meridian": 6,
        "acupoint": 8,
        "level": 2,
        "prop": _tools.RODict({0:52120927}),
        "needItems": _tools.ROList([[30000267, 12], [30000268, 12]]),
        "needCoins": _tools.ROList([30000002, 23800])
    }),
    60803: _tools.RODict({
        "ID": 60803,
        "meridian": 6,
        "acupoint": 8,
        "level": 3,
        "prop": _tools.RODict({0:52120928}),
        "needItems": _tools.ROList([[30000267, 14], [30000268, 14]]),
        "needCoins": _tools.ROList([30000002, 26200])
    }),
    60804: _tools.RODict({
        "ID": 60804,
        "meridian": 6,
        "acupoint": 8,
        "level": 4,
        "prop": _tools.RODict({0:52120929}),
        "needItems": _tools.ROList([[30000267, 16], [30000268, 16]]),
        "needCoins": _tools.ROList([30000002, 28800])
    }),
    60805: _tools.RODict({
        "ID": 60805,
        "meridian": 6,
        "acupoint": 8,
        "level": 5,
        "prop": _tools.RODict({0:52120930}),
        "needItems": _tools.ROList([[30000267, 18], [30000268, 18]]),
        "needCoins": _tools.ROList([30000002, 31700])
    }),
    70101: _tools.RODict({
        "ID": 70101,
        "meridian": 7,
        "acupoint": 1,
        "level": 1,
        "prop": _tools.RODict({0:52120031}),
        "needItems": _tools.ROList([[30000267, 20], [30000268, 20]]),
        "needCoins": _tools.ROList([30000002, 34900])
    }),
    70102: _tools.RODict({
        "ID": 70102,
        "meridian": 7,
        "acupoint": 1,
        "level": 2,
        "prop": _tools.RODict({0:52120032}),
        "needItems": _tools.ROList([[30000267, 22], [30000268, 22]]),
        "needCoins": _tools.ROList([30000002, 38400])
    }),
    70103: _tools.RODict({
        "ID": 70103,
        "meridian": 7,
        "acupoint": 1,
        "level": 3,
        "prop": _tools.RODict({0:52120033}),
        "needItems": _tools.ROList([[30000267, 24], [30000268, 24]]),
        "needCoins": _tools.ROList([30000002, 42200])
    }),
    70104: _tools.RODict({
        "ID": 70104,
        "meridian": 7,
        "acupoint": 1,
        "level": 4,
        "prop": _tools.RODict({0:52120034}),
        "needItems": _tools.ROList([[30000267, 26], [30000268, 26]]),
        "needCoins": _tools.ROList([30000002, 46400])
    }),
    70105: _tools.RODict({
        "ID": 70105,
        "meridian": 7,
        "acupoint": 1,
        "level": 5,
        "prop": _tools.RODict({0:52120035}),
        "needItems": _tools.ROList([[30000267, 28], [30000268, 28]]),
        "needCoins": _tools.ROList([30000002, 51000])
    }),
    70201: _tools.RODict({
        "ID": 70201,
        "meridian": 7,
        "acupoint": 2,
        "level": 1,
        "prop": _tools.RODict({0:52120131}),
        "needItems": _tools.ROList([[30000267, 20], [30000268, 20]]),
        "needCoins": _tools.ROList([30000002, 34900])
    }),
    70202: _tools.RODict({
        "ID": 70202,
        "meridian": 7,
        "acupoint": 2,
        "level": 2,
        "prop": _tools.RODict({0:52120132}),
        "needItems": _tools.ROList([[30000267, 22], [30000268, 22]]),
        "needCoins": _tools.ROList([30000002, 38400])
    }),
    70203: _tools.RODict({
        "ID": 70203,
        "meridian": 7,
        "acupoint": 2,
        "level": 3,
        "prop": _tools.RODict({0:52120133}),
        "needItems": _tools.ROList([[30000267, 24], [30000268, 24]]),
        "needCoins": _tools.ROList([30000002, 42200])
    }),
    70204: _tools.RODict({
        "ID": 70204,
        "meridian": 7,
        "acupoint": 2,
        "level": 4,
        "prop": _tools.RODict({0:52120134}),
        "needItems": _tools.ROList([[30000267, 26], [30000268, 26]]),
        "needCoins": _tools.ROList([30000002, 46400])
    }),
    70205: _tools.RODict({
        "ID": 70205,
        "meridian": 7,
        "acupoint": 2,
        "level": 5,
        "prop": _tools.RODict({0:52120135}),
        "needItems": _tools.ROList([[30000267, 28], [30000268, 28]]),
        "needCoins": _tools.ROList([30000002, 51000])
    }),
    70301: _tools.RODict({
        "ID": 70301,
        "meridian": 7,
        "acupoint": 3,
        "level": 1,
        "prop": _tools.RODict({1001:52120331,1002:52120331,1003:52120231}),
        "needItems": _tools.ROList([[30000267, 20], [30000268, 20]]),
        "needCoins": _tools.ROList([30000002, 34900])
    }),
    70302: _tools.RODict({
        "ID": 70302,
        "meridian": 7,
        "acupoint": 3,
        "level": 2,
        "prop": _tools.RODict({1001:52120332,1002:52120332,1003:52120232}),
        "needItems": _tools.ROList([[30000267, 22], [30000268, 22]]),
        "needCoins": _tools.ROList([30000002, 38400])
    }),
    70303: _tools.RODict({
        "ID": 70303,
        "meridian": 7,
        "acupoint": 3,
        "level": 3,
        "prop": _tools.RODict({1001:52120333,1002:52120333,1003:52120233}),
        "needItems": _tools.ROList([[30000267, 24], [30000268, 24]]),
        "needCoins": _tools.ROList([30000002, 42200])
    }),
    70304: _tools.RODict({
        "ID": 70304,
        "meridian": 7,
        "acupoint": 3,
        "level": 4,
        "prop": _tools.RODict({1001:52120334,1002:52120334,1003:52120234}),
        "needItems": _tools.ROList([[30000267, 26], [30000268, 26]]),
        "needCoins": _tools.ROList([30000002, 46400])
    }),
    70305: _tools.RODict({
        "ID": 70305,
        "meridian": 7,
        "acupoint": 3,
        "level": 5,
        "prop": _tools.RODict({1001:52120335,1002:52120335,1003:52120235}),
        "needItems": _tools.ROList([[30000267, 28], [30000268, 28]]),
        "needCoins": _tools.ROList([30000002, 51000])
    }),
    70401: _tools.RODict({
        "ID": 70401,
        "meridian": 7,
        "acupoint": 4,
        "level": 1,
        "prop": _tools.RODict({1001:52120531,1002:52120531,1003:52120431}),
        "needItems": _tools.ROList([[30000267, 20], [30000268, 20]]),
        "needCoins": _tools.ROList([30000002, 34900])
    }),
    70402: _tools.RODict({
        "ID": 70402,
        "meridian": 7,
        "acupoint": 4,
        "level": 2,
        "prop": _tools.RODict({1001:52120532,1002:52120532,1003:52120432}),
        "needItems": _tools.ROList([[30000267, 22], [30000268, 22]]),
        "needCoins": _tools.ROList([30000002, 38400])
    }),
    70403: _tools.RODict({
        "ID": 70403,
        "meridian": 7,
        "acupoint": 4,
        "level": 3,
        "prop": _tools.RODict({1001:52120533,1002:52120533,1003:52120433}),
        "needItems": _tools.ROList([[30000267, 24], [30000268, 24]]),
        "needCoins": _tools.ROList([30000002, 42200])
    }),
    70404: _tools.RODict({
        "ID": 70404,
        "meridian": 7,
        "acupoint": 4,
        "level": 4,
        "prop": _tools.RODict({1001:52120534,1002:52120534,1003:52120434}),
        "needItems": _tools.ROList([[30000267, 26], [30000268, 26]]),
        "needCoins": _tools.ROList([30000002, 46400])
    }),
    70405: _tools.RODict({
        "ID": 70405,
        "meridian": 7,
        "acupoint": 4,
        "level": 5,
        "prop": _tools.RODict({1001:52120535,1002:52120535,1003:52120435}),
        "needItems": _tools.ROList([[30000267, 28], [30000268, 28]]),
        "needCoins": _tools.ROList([30000002, 51000])
    }),
    70501: _tools.RODict({
        "ID": 70501,
        "meridian": 7,
        "acupoint": 5,
        "level": 1,
        "prop": _tools.RODict({0:52120631}),
        "needItems": _tools.ROList([[30000267, 20], [30000268, 20]]),
        "needCoins": _tools.ROList([30000002, 34900])
    }),
    70502: _tools.RODict({
        "ID": 70502,
        "meridian": 7,
        "acupoint": 5,
        "level": 2,
        "prop": _tools.RODict({0:52120632}),
        "needItems": _tools.ROList([[30000267, 22], [30000268, 22]]),
        "needCoins": _tools.ROList([30000002, 38400])
    }),
    70503: _tools.RODict({
        "ID": 70503,
        "meridian": 7,
        "acupoint": 5,
        "level": 3,
        "prop": _tools.RODict({0:52120633}),
        "needItems": _tools.ROList([[30000267, 24], [30000268, 24]]),
        "needCoins": _tools.ROList([30000002, 42200])
    }),
    70504: _tools.RODict({
        "ID": 70504,
        "meridian": 7,
        "acupoint": 5,
        "level": 4,
        "prop": _tools.RODict({0:52120634}),
        "needItems": _tools.ROList([[30000267, 26], [30000268, 26]]),
        "needCoins": _tools.ROList([30000002, 46400])
    }),
    70505: _tools.RODict({
        "ID": 70505,
        "meridian": 7,
        "acupoint": 5,
        "level": 5,
        "prop": _tools.RODict({0:52120635}),
        "needItems": _tools.ROList([[30000267, 28], [30000268, 28]]),
        "needCoins": _tools.ROList([30000002, 51000])
    }),
    70601: _tools.RODict({
        "ID": 70601,
        "meridian": 7,
        "acupoint": 6,
        "level": 1,
        "prop": _tools.RODict({0:52120731}),
        "needItems": _tools.ROList([[30000267, 20], [30000268, 20]]),
        "needCoins": _tools.ROList([30000002, 34900])
    }),
    70602: _tools.RODict({
        "ID": 70602,
        "meridian": 7,
        "acupoint": 6,
        "level": 2,
        "prop": _tools.RODict({0:52120732}),
        "needItems": _tools.ROList([[30000267, 22], [30000268, 22]]),
        "needCoins": _tools.ROList([30000002, 38400])
    }),
    70603: _tools.RODict({
        "ID": 70603,
        "meridian": 7,
        "acupoint": 6,
        "level": 3,
        "prop": _tools.RODict({0:52120733}),
        "needItems": _tools.ROList([[30000267, 24], [30000268, 24]]),
        "needCoins": _tools.ROList([30000002, 42200])
    }),
    70604: _tools.RODict({
        "ID": 70604,
        "meridian": 7,
        "acupoint": 6,
        "level": 4,
        "prop": _tools.RODict({0:52120734}),
        "needItems": _tools.ROList([[30000267, 26], [30000268, 26]]),
        "needCoins": _tools.ROList([30000002, 46400])
    }),
    70605: _tools.RODict({
        "ID": 70605,
        "meridian": 7,
        "acupoint": 6,
        "level": 5,
        "prop": _tools.RODict({0:52120735}),
        "needItems": _tools.ROList([[30000267, 28], [30000268, 28]]),
        "needCoins": _tools.ROList([30000002, 51000])
    }),
    70701: _tools.RODict({
        "ID": 70701,
        "meridian": 7,
        "acupoint": 7,
        "level": 1,
        "prop": _tools.RODict({0:52120831}),
        "needItems": _tools.ROList([[30000267, 20], [30000268, 20]]),
        "needCoins": _tools.ROList([30000002, 34900])
    }),
    70702: _tools.RODict({
        "ID": 70702,
        "meridian": 7,
        "acupoint": 7,
        "level": 2,
        "prop": _tools.RODict({0:52120832}),
        "needItems": _tools.ROList([[30000267, 22], [30000268, 22]]),
        "needCoins": _tools.ROList([30000002, 38400])
    }),
    70703: _tools.RODict({
        "ID": 70703,
        "meridian": 7,
        "acupoint": 7,
        "level": 3,
        "prop": _tools.RODict({0:52120833}),
        "needItems": _tools.ROList([[30000267, 24], [30000268, 24]]),
        "needCoins": _tools.ROList([30000002, 42200])
    }),
    70704: _tools.RODict({
        "ID": 70704,
        "meridian": 7,
        "acupoint": 7,
        "level": 4,
        "prop": _tools.RODict({0:52120834}),
        "needItems": _tools.ROList([[30000267, 26], [30000268, 26]]),
        "needCoins": _tools.ROList([30000002, 46400])
    }),
    70705: _tools.RODict({
        "ID": 70705,
        "meridian": 7,
        "acupoint": 7,
        "level": 5,
        "prop": _tools.RODict({0:52120835}),
        "needItems": _tools.ROList([[30000267, 28], [30000268, 28]]),
        "needCoins": _tools.ROList([30000002, 51000])
    }),
    70801: _tools.RODict({
        "ID": 70801,
        "meridian": 7,
        "acupoint": 8,
        "level": 1,
        "prop": _tools.RODict({0:52120931}),
        "needItems": _tools.ROList([[30000267, 20], [30000268, 20]]),
        "needCoins": _tools.ROList([30000002, 34900])
    }),
    70802: _tools.RODict({
        "ID": 70802,
        "meridian": 7,
        "acupoint": 8,
        "level": 2,
        "prop": _tools.RODict({0:52120932}),
        "needItems": _tools.ROList([[30000267, 22], [30000268, 22]]),
        "needCoins": _tools.ROList([30000002, 38400])
    }),
    70803: _tools.RODict({
        "ID": 70803,
        "meridian": 7,
        "acupoint": 8,
        "level": 3,
        "prop": _tools.RODict({0:52120933}),
        "needItems": _tools.ROList([[30000267, 24], [30000268, 24]]),
        "needCoins": _tools.ROList([30000002, 42200])
    }),
    70804: _tools.RODict({
        "ID": 70804,
        "meridian": 7,
        "acupoint": 8,
        "level": 4,
        "prop": _tools.RODict({0:52120934}),
        "needItems": _tools.ROList([[30000267, 26], [30000268, 26]]),
        "needCoins": _tools.ROList([30000002, 46400])
    }),
    70805: _tools.RODict({
        "ID": 70805,
        "meridian": 7,
        "acupoint": 8,
        "level": 5,
        "prop": _tools.RODict({0:52120935}),
        "needItems": _tools.ROList([[30000267, 28], [30000268, 28]]),
        "needCoins": _tools.ROList([30000002, 51000])
    }),
    80101: _tools.RODict({
        "ID": 80101,
        "meridian": 8,
        "acupoint": 1,
        "level": 1,
        "prop": _tools.RODict({0:52120036}),
        "needItems": _tools.ROList([[30000267, 30], [30000268, 30]]),
        "needCoins": _tools.ROList([30000002, 56100])
    }),
    80102: _tools.RODict({
        "ID": 80102,
        "meridian": 8,
        "acupoint": 1,
        "level": 2,
        "prop": _tools.RODict({0:52120037}),
        "needItems": _tools.ROList([[30000267, 32], [30000268, 32]]),
        "needCoins": _tools.ROList([30000002, 61700])
    }),
    80103: _tools.RODict({
        "ID": 80103,
        "meridian": 8,
        "acupoint": 1,
        "level": 3,
        "prop": _tools.RODict({0:52120038}),
        "needItems": _tools.ROList([[30000267, 34], [30000268, 34]]),
        "needCoins": _tools.ROList([30000002, 67900])
    }),
    80104: _tools.RODict({
        "ID": 80104,
        "meridian": 8,
        "acupoint": 1,
        "level": 4,
        "prop": _tools.RODict({0:52120039}),
        "needItems": _tools.ROList([[30000267, 36], [30000268, 36]]),
        "needCoins": _tools.ROList([30000002, 74700])
    }),
    80105: _tools.RODict({
        "ID": 80105,
        "meridian": 8,
        "acupoint": 1,
        "level": 5,
        "prop": _tools.RODict({0:52120040}),
        "needItems": _tools.ROList([[30000267, 38], [30000268, 38]]),
        "needCoins": _tools.ROList([30000002, 82200])
    }),
    80201: _tools.RODict({
        "ID": 80201,
        "meridian": 8,
        "acupoint": 2,
        "level": 1,
        "prop": _tools.RODict({0:52120136}),
        "needItems": _tools.ROList([[30000267, 30], [30000268, 30]]),
        "needCoins": _tools.ROList([30000002, 56100])
    }),
    80202: _tools.RODict({
        "ID": 80202,
        "meridian": 8,
        "acupoint": 2,
        "level": 2,
        "prop": _tools.RODict({0:52120137}),
        "needItems": _tools.ROList([[30000267, 32], [30000268, 32]]),
        "needCoins": _tools.ROList([30000002, 61700])
    }),
    80203: _tools.RODict({
        "ID": 80203,
        "meridian": 8,
        "acupoint": 2,
        "level": 3,
        "prop": _tools.RODict({0:52120138}),
        "needItems": _tools.ROList([[30000267, 34], [30000268, 34]]),
        "needCoins": _tools.ROList([30000002, 67900])
    }),
    80204: _tools.RODict({
        "ID": 80204,
        "meridian": 8,
        "acupoint": 2,
        "level": 4,
        "prop": _tools.RODict({0:52120139}),
        "needItems": _tools.ROList([[30000267, 36], [30000268, 36]]),
        "needCoins": _tools.ROList([30000002, 74700])
    }),
    80205: _tools.RODict({
        "ID": 80205,
        "meridian": 8,
        "acupoint": 2,
        "level": 5,
        "prop": _tools.RODict({0:52120140}),
        "needItems": _tools.ROList([[30000267, 38], [30000268, 38]]),
        "needCoins": _tools.ROList([30000002, 82200])
    }),
    80301: _tools.RODict({
        "ID": 80301,
        "meridian": 8,
        "acupoint": 3,
        "level": 1,
        "prop": _tools.RODict({1001:52120336,1002:52120336,1003:52120236}),
        "needItems": _tools.ROList([[30000267, 30], [30000268, 30]]),
        "needCoins": _tools.ROList([30000002, 56100])
    }),
    80302: _tools.RODict({
        "ID": 80302,
        "meridian": 8,
        "acupoint": 3,
        "level": 2,
        "prop": _tools.RODict({1001:52120337,1002:52120337,1003:52120237}),
        "needItems": _tools.ROList([[30000267, 32], [30000268, 32]]),
        "needCoins": _tools.ROList([30000002, 61700])
    }),
    80303: _tools.RODict({
        "ID": 80303,
        "meridian": 8,
        "acupoint": 3,
        "level": 3,
        "prop": _tools.RODict({1001:52120338,1002:52120338,1003:52120238}),
        "needItems": _tools.ROList([[30000267, 34], [30000268, 34]]),
        "needCoins": _tools.ROList([30000002, 67900])
    }),
    80304: _tools.RODict({
        "ID": 80304,
        "meridian": 8,
        "acupoint": 3,
        "level": 4,
        "prop": _tools.RODict({1001:52120339,1002:52120339,1003:52120239}),
        "needItems": _tools.ROList([[30000267, 36], [30000268, 36]]),
        "needCoins": _tools.ROList([30000002, 74700])
    }),
    80305: _tools.RODict({
        "ID": 80305,
        "meridian": 8,
        "acupoint": 3,
        "level": 5,
        "prop": _tools.RODict({1001:52120340,1002:52120340,1003:52120240}),
        "needItems": _tools.ROList([[30000267, 38], [30000268, 38]]),
        "needCoins": _tools.ROList([30000002, 82200])
    }),
    80401: _tools.RODict({
        "ID": 80401,
        "meridian": 8,
        "acupoint": 4,
        "level": 1,
        "prop": _tools.RODict({1001:52120536,1002:52120536,1003:52120436}),
        "needItems": _tools.ROList([[30000267, 30], [30000268, 30]]),
        "needCoins": _tools.ROList([30000002, 56100])
    }),
    80402: _tools.RODict({
        "ID": 80402,
        "meridian": 8,
        "acupoint": 4,
        "level": 2,
        "prop": _tools.RODict({1001:52120537,1002:52120537,1003:52120437}),
        "needItems": _tools.ROList([[30000267, 32], [30000268, 32]]),
        "needCoins": _tools.ROList([30000002, 61700])
    }),
    80403: _tools.RODict({
        "ID": 80403,
        "meridian": 8,
        "acupoint": 4,
        "level": 3,
        "prop": _tools.RODict({1001:52120538,1002:52120538,1003:52120438}),
        "needItems": _tools.ROList([[30000267, 34], [30000268, 34]]),
        "needCoins": _tools.ROList([30000002, 67900])
    }),
    80404: _tools.RODict({
        "ID": 80404,
        "meridian": 8,
        "acupoint": 4,
        "level": 4,
        "prop": _tools.RODict({1001:52120539,1002:52120539,1003:52120439}),
        "needItems": _tools.ROList([[30000267, 36], [30000268, 36]]),
        "needCoins": _tools.ROList([30000002, 74700])
    }),
    80405: _tools.RODict({
        "ID": 80405,
        "meridian": 8,
        "acupoint": 4,
        "level": 5,
        "prop": _tools.RODict({1001:52120540,1002:52120540,1003:52120440}),
        "needItems": _tools.ROList([[30000267, 38], [30000268, 38]]),
        "needCoins": _tools.ROList([30000002, 82200])
    }),
    80501: _tools.RODict({
        "ID": 80501,
        "meridian": 8,
        "acupoint": 5,
        "level": 1,
        "prop": _tools.RODict({0:52120636}),
        "needItems": _tools.ROList([[30000267, 30], [30000268, 30]]),
        "needCoins": _tools.ROList([30000002, 56100])
    }),
    80502: _tools.RODict({
        "ID": 80502,
        "meridian": 8,
        "acupoint": 5,
        "level": 2,
        "prop": _tools.RODict({0:52120637}),
        "needItems": _tools.ROList([[30000267, 32], [30000268, 32]]),
        "needCoins": _tools.ROList([30000002, 61700])
    }),
    80503: _tools.RODict({
        "ID": 80503,
        "meridian": 8,
        "acupoint": 5,
        "level": 3,
        "prop": _tools.RODict({0:52120638}),
        "needItems": _tools.ROList([[30000267, 34], [30000268, 34]]),
        "needCoins": _tools.ROList([30000002, 67900])
    }),
    80504: _tools.RODict({
        "ID": 80504,
        "meridian": 8,
        "acupoint": 5,
        "level": 4,
        "prop": _tools.RODict({0:52120639}),
        "needItems": _tools.ROList([[30000267, 36], [30000268, 36]]),
        "needCoins": _tools.ROList([30000002, 74700])
    }),
    80505: _tools.RODict({
        "ID": 80505,
        "meridian": 8,
        "acupoint": 5,
        "level": 5,
        "prop": _tools.RODict({0:52120640}),
        "needItems": _tools.ROList([[30000267, 38], [30000268, 38]]),
        "needCoins": _tools.ROList([30000002, 82200])
    }),
    80601: _tools.RODict({
        "ID": 80601,
        "meridian": 8,
        "acupoint": 6,
        "level": 1,
        "prop": _tools.RODict({0:52120736}),
        "needItems": _tools.ROList([[30000267, 30], [30000268, 30]]),
        "needCoins": _tools.ROList([30000002, 56100])
    }),
    80602: _tools.RODict({
        "ID": 80602,
        "meridian": 8,
        "acupoint": 6,
        "level": 2,
        "prop": _tools.RODict({0:52120737}),
        "needItems": _tools.ROList([[30000267, 32], [30000268, 32]]),
        "needCoins": _tools.ROList([30000002, 61700])
    }),
    80603: _tools.RODict({
        "ID": 80603,
        "meridian": 8,
        "acupoint": 6,
        "level": 3,
        "prop": _tools.RODict({0:52120738}),
        "needItems": _tools.ROList([[30000267, 34], [30000268, 34]]),
        "needCoins": _tools.ROList([30000002, 67900])
    }),
    80604: _tools.RODict({
        "ID": 80604,
        "meridian": 8,
        "acupoint": 6,
        "level": 4,
        "prop": _tools.RODict({0:52120739}),
        "needItems": _tools.ROList([[30000267, 36], [30000268, 36]]),
        "needCoins": _tools.ROList([30000002, 74700])
    }),
    80605: _tools.RODict({
        "ID": 80605,
        "meridian": 8,
        "acupoint": 6,
        "level": 5,
        "prop": _tools.RODict({0:52120740}),
        "needItems": _tools.ROList([[30000267, 38], [30000268, 38]]),
        "needCoins": _tools.ROList([30000002, 82200])
    }),
    80701: _tools.RODict({
        "ID": 80701,
        "meridian": 8,
        "acupoint": 7,
        "level": 1,
        "prop": _tools.RODict({0:52120836}),
        "needItems": _tools.ROList([[30000267, 30], [30000268, 30]]),
        "needCoins": _tools.ROList([30000002, 56100])
    }),
    80702: _tools.RODict({
        "ID": 80702,
        "meridian": 8,
        "acupoint": 7,
        "level": 2,
        "prop": _tools.RODict({0:52120837}),
        "needItems": _tools.ROList([[30000267, 32], [30000268, 32]]),
        "needCoins": _tools.ROList([30000002, 61700])
    }),
    80703: _tools.RODict({
        "ID": 80703,
        "meridian": 8,
        "acupoint": 7,
        "level": 3,
        "prop": _tools.RODict({0:52120838}),
        "needItems": _tools.ROList([[30000267, 34], [30000268, 34]]),
        "needCoins": _tools.ROList([30000002, 67900])
    }),
    80704: _tools.RODict({
        "ID": 80704,
        "meridian": 8,
        "acupoint": 7,
        "level": 4,
        "prop": _tools.RODict({0:52120839}),
        "needItems": _tools.ROList([[30000267, 36], [30000268, 36]]),
        "needCoins": _tools.ROList([30000002, 74700])
    }),
    80705: _tools.RODict({
        "ID": 80705,
        "meridian": 8,
        "acupoint": 7,
        "level": 5,
        "prop": _tools.RODict({0:52120840}),
        "needItems": _tools.ROList([[30000267, 38], [30000268, 38]]),
        "needCoins": _tools.ROList([30000002, 82200])
    }),
    80801: _tools.RODict({
        "ID": 80801,
        "meridian": 8,
        "acupoint": 8,
        "level": 1,
        "prop": _tools.RODict({0:52120936}),
        "needItems": _tools.ROList([[30000267, 30], [30000268, 30]]),
        "needCoins": _tools.ROList([30000002, 56100])
    }),
    80802: _tools.RODict({
        "ID": 80802,
        "meridian": 8,
        "acupoint": 8,
        "level": 2,
        "prop": _tools.RODict({0:52120937}),
        "needItems": _tools.ROList([[30000267, 32], [30000268, 32]]),
        "needCoins": _tools.ROList([30000002, 61700])
    }),
    80803: _tools.RODict({
        "ID": 80803,
        "meridian": 8,
        "acupoint": 8,
        "level": 3,
        "prop": _tools.RODict({0:52120938}),
        "needItems": _tools.ROList([[30000267, 34], [30000268, 34]]),
        "needCoins": _tools.ROList([30000002, 67900])
    }),
    80804: _tools.RODict({
        "ID": 80804,
        "meridian": 8,
        "acupoint": 8,
        "level": 4,
        "prop": _tools.RODict({0:52120939}),
        "needItems": _tools.ROList([[30000267, 36], [30000268, 36]]),
        "needCoins": _tools.ROList([30000002, 74700])
    }),
    80805: _tools.RODict({
        "ID": 80805,
        "meridian": 8,
        "acupoint": 8,
        "level": 5,
        "prop": _tools.RODict({0:52120940}),
        "needItems": _tools.ROList([[30000267, 38], [30000268, 38]]),
        "needCoins": _tools.ROList([30000002, 82200])
    }),
    90101: _tools.RODict({
        "ID": 90101,
        "meridian": 9,
        "acupoint": 1,
        "level": 1,
        "prop": _tools.RODict({0:52120041}),
        "needItems": _tools.ROList([[30000267, 40], [30000268, 40]]),
        "needCoins": _tools.ROList([30000002, 90400])
    }),
    90102: _tools.RODict({
        "ID": 90102,
        "meridian": 9,
        "acupoint": 1,
        "level": 2,
        "prop": _tools.RODict({0:52120042}),
        "needItems": _tools.ROList([[30000267, 42], [30000268, 42]]),
        "needCoins": _tools.ROList([30000002, 99400])
    }),
    90103: _tools.RODict({
        "ID": 90103,
        "meridian": 9,
        "acupoint": 1,
        "level": 3,
        "prop": _tools.RODict({0:52120043}),
        "needItems": _tools.ROList([[30000267, 44], [30000268, 44]]),
        "needCoins": _tools.ROList([30000002, 109300])
    }),
    90104: _tools.RODict({
        "ID": 90104,
        "meridian": 9,
        "acupoint": 1,
        "level": 4,
        "prop": _tools.RODict({0:52120044}),
        "needItems": _tools.ROList([[30000267, 46], [30000268, 46]]),
        "needCoins": _tools.ROList([30000002, 120000])
    }),
    90105: _tools.RODict({
        "ID": 90105,
        "meridian": 9,
        "acupoint": 1,
        "level": 5,
        "prop": _tools.RODict({0:52120045}),
        "needItems": _tools.ROList([[30000267, 48], [30000268, 48]]),
        "needCoins": _tools.ROList([30000002, 130000])
    }),
    90201: _tools.RODict({
        "ID": 90201,
        "meridian": 9,
        "acupoint": 2,
        "level": 1,
        "prop": _tools.RODict({0:52120141}),
        "needItems": _tools.ROList([[30000267, 40], [30000268, 40]]),
        "needCoins": _tools.ROList([30000002, 90400])
    }),
    90202: _tools.RODict({
        "ID": 90202,
        "meridian": 9,
        "acupoint": 2,
        "level": 2,
        "prop": _tools.RODict({0:52120142}),
        "needItems": _tools.ROList([[30000267, 42], [30000268, 42]]),
        "needCoins": _tools.ROList([30000002, 99400])
    }),
    90203: _tools.RODict({
        "ID": 90203,
        "meridian": 9,
        "acupoint": 2,
        "level": 3,
        "prop": _tools.RODict({0:52120143}),
        "needItems": _tools.ROList([[30000267, 44], [30000268, 44]]),
        "needCoins": _tools.ROList([30000002, 109300])
    }),
    90204: _tools.RODict({
        "ID": 90204,
        "meridian": 9,
        "acupoint": 2,
        "level": 4,
        "prop": _tools.RODict({0:52120144}),
        "needItems": _tools.ROList([[30000267, 46], [30000268, 46]]),
        "needCoins": _tools.ROList([30000002, 120000])
    }),
    90205: _tools.RODict({
        "ID": 90205,
        "meridian": 9,
        "acupoint": 2,
        "level": 5,
        "prop": _tools.RODict({0:52120145}),
        "needItems": _tools.ROList([[30000267, 48], [30000268, 48]]),
        "needCoins": _tools.ROList([30000002, 130000])
    }),
    90301: _tools.RODict({
        "ID": 90301,
        "meridian": 9,
        "acupoint": 3,
        "level": 1,
        "prop": _tools.RODict({1001:52120341,1002:52120341,1003:52120241}),
        "needItems": _tools.ROList([[30000267, 40], [30000268, 40]]),
        "needCoins": _tools.ROList([30000002, 90400])
    }),
    90302: _tools.RODict({
        "ID": 90302,
        "meridian": 9,
        "acupoint": 3,
        "level": 2,
        "prop": _tools.RODict({1001:52120342,1002:52120342,1003:52120242}),
        "needItems": _tools.ROList([[30000267, 42], [30000268, 42]]),
        "needCoins": _tools.ROList([30000002, 99400])
    }),
    90303: _tools.RODict({
        "ID": 90303,
        "meridian": 9,
        "acupoint": 3,
        "level": 3,
        "prop": _tools.RODict({1001:52120343,1002:52120343,1003:52120243}),
        "needItems": _tools.ROList([[30000267, 44], [30000268, 44]]),
        "needCoins": _tools.ROList([30000002, 109300])
    }),
    90304: _tools.RODict({
        "ID": 90304,
        "meridian": 9,
        "acupoint": 3,
        "level": 4,
        "prop": _tools.RODict({1001:52120344,1002:52120344,1003:52120244}),
        "needItems": _tools.ROList([[30000267, 46], [30000268, 46]]),
        "needCoins": _tools.ROList([30000002, 120000])
    }),
    90305: _tools.RODict({
        "ID": 90305,
        "meridian": 9,
        "acupoint": 3,
        "level": 5,
        "prop": _tools.RODict({1001:52120345,1002:52120345,1003:52120245}),
        "needItems": _tools.ROList([[30000267, 48], [30000268, 48]]),
        "needCoins": _tools.ROList([30000002, 130000])
    }),
    90401: _tools.RODict({
        "ID": 90401,
        "meridian": 9,
        "acupoint": 4,
        "level": 1,
        "prop": _tools.RODict({1001:52120541,1002:52120541,1003:52120441}),
        "needItems": _tools.ROList([[30000267, 40], [30000268, 40]]),
        "needCoins": _tools.ROList([30000002, 90400])
    }),
    90402: _tools.RODict({
        "ID": 90402,
        "meridian": 9,
        "acupoint": 4,
        "level": 2,
        "prop": _tools.RODict({1001:52120542,1002:52120542,1003:52120442}),
        "needItems": _tools.ROList([[30000267, 42], [30000268, 42]]),
        "needCoins": _tools.ROList([30000002, 99400])
    }),
    90403: _tools.RODict({
        "ID": 90403,
        "meridian": 9,
        "acupoint": 4,
        "level": 3,
        "prop": _tools.RODict({1001:52120543,1002:52120543,1003:52120443}),
        "needItems": _tools.ROList([[30000267, 44], [30000268, 44]]),
        "needCoins": _tools.ROList([30000002, 109300])
    }),
    90404: _tools.RODict({
        "ID": 90404,
        "meridian": 9,
        "acupoint": 4,
        "level": 4,
        "prop": _tools.RODict({1001:52120544,1002:52120544,1003:52120444}),
        "needItems": _tools.ROList([[30000267, 46], [30000268, 46]]),
        "needCoins": _tools.ROList([30000002, 120000])
    }),
    90405: _tools.RODict({
        "ID": 90405,
        "meridian": 9,
        "acupoint": 4,
        "level": 5,
        "prop": _tools.RODict({1001:52120545,1002:52120545,1003:52120445}),
        "needItems": _tools.ROList([[30000267, 48], [30000268, 48]]),
        "needCoins": _tools.ROList([30000002, 130000])
    }),
    90501: _tools.RODict({
        "ID": 90501,
        "meridian": 9,
        "acupoint": 5,
        "level": 1,
        "prop": _tools.RODict({0:52120641}),
        "needItems": _tools.ROList([[30000267, 40], [30000268, 40]]),
        "needCoins": _tools.ROList([30000002, 90400])
    }),
    90502: _tools.RODict({
        "ID": 90502,
        "meridian": 9,
        "acupoint": 5,
        "level": 2,
        "prop": _tools.RODict({0:52120642}),
        "needItems": _tools.ROList([[30000267, 42], [30000268, 42]]),
        "needCoins": _tools.ROList([30000002, 99400])
    }),
    90503: _tools.RODict({
        "ID": 90503,
        "meridian": 9,
        "acupoint": 5,
        "level": 3,
        "prop": _tools.RODict({0:52120643}),
        "needItems": _tools.ROList([[30000267, 44], [30000268, 44]]),
        "needCoins": _tools.ROList([30000002, 109300])
    }),
    90504: _tools.RODict({
        "ID": 90504,
        "meridian": 9,
        "acupoint": 5,
        "level": 4,
        "prop": _tools.RODict({0:52120644}),
        "needItems": _tools.ROList([[30000267, 46], [30000268, 46]]),
        "needCoins": _tools.ROList([30000002, 120000])
    }),
    90505: _tools.RODict({
        "ID": 90505,
        "meridian": 9,
        "acupoint": 5,
        "level": 5,
        "prop": _tools.RODict({0:52120645}),
        "needItems": _tools.ROList([[30000267, 48], [30000268, 48]]),
        "needCoins": _tools.ROList([30000002, 130000])
    }),
    90601: _tools.RODict({
        "ID": 90601,
        "meridian": 9,
        "acupoint": 6,
        "level": 1,
        "prop": _tools.RODict({0:52120741}),
        "needItems": _tools.ROList([[30000267, 40], [30000268, 40]]),
        "needCoins": _tools.ROList([30000002, 90400])
    }),
    90602: _tools.RODict({
        "ID": 90602,
        "meridian": 9,
        "acupoint": 6,
        "level": 2,
        "prop": _tools.RODict({0:52120742}),
        "needItems": _tools.ROList([[30000267, 42], [30000268, 42]]),
        "needCoins": _tools.ROList([30000002, 99400])
    }),
    90603: _tools.RODict({
        "ID": 90603,
        "meridian": 9,
        "acupoint": 6,
        "level": 3,
        "prop": _tools.RODict({0:52120743}),
        "needItems": _tools.ROList([[30000267, 44], [30000268, 44]]),
        "needCoins": _tools.ROList([30000002, 109300])
    }),
    90604: _tools.RODict({
        "ID": 90604,
        "meridian": 9,
        "acupoint": 6,
        "level": 4,
        "prop": _tools.RODict({0:52120744}),
        "needItems": _tools.ROList([[30000267, 46], [30000268, 46]]),
        "needCoins": _tools.ROList([30000002, 120000])
    }),
    90605: _tools.RODict({
        "ID": 90605,
        "meridian": 9,
        "acupoint": 6,
        "level": 5,
        "prop": _tools.RODict({0:52120745}),
        "needItems": _tools.ROList([[30000267, 48], [30000268, 48]]),
        "needCoins": _tools.ROList([30000002, 130000])
    }),
    90701: _tools.RODict({
        "ID": 90701,
        "meridian": 9,
        "acupoint": 7,
        "level": 1,
        "prop": _tools.RODict({0:52120841}),
        "needItems": _tools.ROList([[30000267, 40], [30000268, 40]]),
        "needCoins": _tools.ROList([30000002, 90400])
    }),
    90702: _tools.RODict({
        "ID": 90702,
        "meridian": 9,
        "acupoint": 7,
        "level": 2,
        "prop": _tools.RODict({0:52120842}),
        "needItems": _tools.ROList([[30000267, 42], [30000268, 42]]),
        "needCoins": _tools.ROList([30000002, 99400])
    }),
    90703: _tools.RODict({
        "ID": 90703,
        "meridian": 9,
        "acupoint": 7,
        "level": 3,
        "prop": _tools.RODict({0:52120843}),
        "needItems": _tools.ROList([[30000267, 44], [30000268, 44]]),
        "needCoins": _tools.ROList([30000002, 109300])
    }),
    90704: _tools.RODict({
        "ID": 90704,
        "meridian": 9,
        "acupoint": 7,
        "level": 4,
        "prop": _tools.RODict({0:52120844}),
        "needItems": _tools.ROList([[30000267, 46], [30000268, 46]]),
        "needCoins": _tools.ROList([30000002, 120000])
    }),
    90705: _tools.RODict({
        "ID": 90705,
        "meridian": 9,
        "acupoint": 7,
        "level": 5,
        "prop": _tools.RODict({0:52120845}),
        "needItems": _tools.ROList([[30000267, 48], [30000268, 48]]),
        "needCoins": _tools.ROList([30000002, 130000])
    }),
    90801: _tools.RODict({
        "ID": 90801,
        "meridian": 9,
        "acupoint": 8,
        "level": 1,
        "prop": _tools.RODict({0:52120941}),
        "needItems": _tools.ROList([[30000267, 40], [30000268, 40]]),
        "needCoins": _tools.ROList([30000002, 90400])
    }),
    90802: _tools.RODict({
        "ID": 90802,
        "meridian": 9,
        "acupoint": 8,
        "level": 2,
        "prop": _tools.RODict({0:52120942}),
        "needItems": _tools.ROList([[30000267, 42], [30000268, 42]]),
        "needCoins": _tools.ROList([30000002, 99400])
    }),
    90803: _tools.RODict({
        "ID": 90803,
        "meridian": 9,
        "acupoint": 8,
        "level": 3,
        "prop": _tools.RODict({0:52120943}),
        "needItems": _tools.ROList([[30000267, 44], [30000268, 44]]),
        "needCoins": _tools.ROList([30000002, 109300])
    }),
    90804: _tools.RODict({
        "ID": 90804,
        "meridian": 9,
        "acupoint": 8,
        "level": 4,
        "prop": _tools.RODict({0:52120944}),
        "needItems": _tools.ROList([[30000267, 46], [30000268, 46]]),
        "needCoins": _tools.ROList([30000002, 120000])
    }),
    90805: _tools.RODict({
        "ID": 90805,
        "meridian": 9,
        "acupoint": 8,
        "level": 5,
        "prop": _tools.RODict({0:52120945}),
        "needItems": _tools.ROList([[30000267, 48], [30000268, 48]]),
        "needCoins": _tools.ROList([30000002, 130000])
    }),
    100101: _tools.RODict({
        "ID": 100101,
        "meridian": 10,
        "acupoint": 1,
        "level": 1,
        "prop": _tools.RODict({0:52120046}),
        "needItems": _tools.ROList([[30000267, 50], [30000268, 50]]),
        "needCoins": _tools.ROList([30000002, 140000])
    }),
    100102: _tools.RODict({
        "ID": 100102,
        "meridian": 10,
        "acupoint": 1,
        "level": 2,
        "prop": _tools.RODict({0:52120047}),
        "needItems": _tools.ROList([[30000267, 52], [30000268, 52]]),
        "needCoins": _tools.ROList([30000002, 150000])
    }),
    100103: _tools.RODict({
        "ID": 100103,
        "meridian": 10,
        "acupoint": 1,
        "level": 3,
        "prop": _tools.RODict({0:52120048}),
        "needItems": _tools.ROList([[30000267, 54], [30000268, 54]]),
        "needCoins": _tools.ROList([30000002, 160000])
    }),
    100104: _tools.RODict({
        "ID": 100104,
        "meridian": 10,
        "acupoint": 1,
        "level": 4,
        "prop": _tools.RODict({0:52120049}),
        "needItems": _tools.ROList([[30000267, 56], [30000268, 56]]),
        "needCoins": _tools.ROList([30000002, 170000])
    }),
    100105: _tools.RODict({
        "ID": 100105,
        "meridian": 10,
        "acupoint": 1,
        "level": 5,
        "prop": _tools.RODict({0:52120050}),
        "needItems": _tools.ROList([[30000267, 58], [30000268, 58]]),
        "needCoins": _tools.ROList([30000002, 180000])
    }),
    100201: _tools.RODict({
        "ID": 100201,
        "meridian": 10,
        "acupoint": 2,
        "level": 1,
        "prop": _tools.RODict({0:52120146}),
        "needItems": _tools.ROList([[30000267, 50], [30000268, 50]]),
        "needCoins": _tools.ROList([30000002, 140000])
    }),
    100202: _tools.RODict({
        "ID": 100202,
        "meridian": 10,
        "acupoint": 2,
        "level": 2,
        "prop": _tools.RODict({0:52120147}),
        "needItems": _tools.ROList([[30000267, 52], [30000268, 52]]),
        "needCoins": _tools.ROList([30000002, 150000])
    }),
    100203: _tools.RODict({
        "ID": 100203,
        "meridian": 10,
        "acupoint": 2,
        "level": 3,
        "prop": _tools.RODict({0:52120148}),
        "needItems": _tools.ROList([[30000267, 54], [30000268, 54]]),
        "needCoins": _tools.ROList([30000002, 160000])
    }),
    100204: _tools.RODict({
        "ID": 100204,
        "meridian": 10,
        "acupoint": 2,
        "level": 4,
        "prop": _tools.RODict({0:52120149}),
        "needItems": _tools.ROList([[30000267, 56], [30000268, 56]]),
        "needCoins": _tools.ROList([30000002, 170000])
    }),
    100205: _tools.RODict({
        "ID": 100205,
        "meridian": 10,
        "acupoint": 2,
        "level": 5,
        "prop": _tools.RODict({0:52120150}),
        "needItems": _tools.ROList([[30000267, 58], [30000268, 58]]),
        "needCoins": _tools.ROList([30000002, 180000])
    }),
    100301: _tools.RODict({
        "ID": 100301,
        "meridian": 10,
        "acupoint": 3,
        "level": 1,
        "prop": _tools.RODict({1001:52120346,1002:52120346,1003:52120246}),
        "needItems": _tools.ROList([[30000267, 50], [30000268, 50]]),
        "needCoins": _tools.ROList([30000002, 140000])
    }),
    100302: _tools.RODict({
        "ID": 100302,
        "meridian": 10,
        "acupoint": 3,
        "level": 2,
        "prop": _tools.RODict({1001:52120347,1002:52120347,1003:52120247}),
        "needItems": _tools.ROList([[30000267, 52], [30000268, 52]]),
        "needCoins": _tools.ROList([30000002, 150000])
    }),
    100303: _tools.RODict({
        "ID": 100303,
        "meridian": 10,
        "acupoint": 3,
        "level": 3,
        "prop": _tools.RODict({1001:52120348,1002:52120348,1003:52120248}),
        "needItems": _tools.ROList([[30000267, 54], [30000268, 54]]),
        "needCoins": _tools.ROList([30000002, 160000])
    }),
    100304: _tools.RODict({
        "ID": 100304,
        "meridian": 10,
        "acupoint": 3,
        "level": 4,
        "prop": _tools.RODict({1001:52120349,1002:52120349,1003:52120249}),
        "needItems": _tools.ROList([[30000267, 56], [30000268, 56]]),
        "needCoins": _tools.ROList([30000002, 170000])
    }),
    100305: _tools.RODict({
        "ID": 100305,
        "meridian": 10,
        "acupoint": 3,
        "level": 5,
        "prop": _tools.RODict({1001:52120350,1002:52120350,1003:52120250}),
        "needItems": _tools.ROList([[30000267, 58], [30000268, 58]]),
        "needCoins": _tools.ROList([30000002, 180000])
    }),
    100401: _tools.RODict({
        "ID": 100401,
        "meridian": 10,
        "acupoint": 4,
        "level": 1,
        "prop": _tools.RODict({1001:52120546,1002:52120546,1003:52120446}),
        "needItems": _tools.ROList([[30000267, 50], [30000268, 50]]),
        "needCoins": _tools.ROList([30000002, 140000])
    }),
    100402: _tools.RODict({
        "ID": 100402,
        "meridian": 10,
        "acupoint": 4,
        "level": 2,
        "prop": _tools.RODict({1001:52120547,1002:52120547,1003:52120447}),
        "needItems": _tools.ROList([[30000267, 52], [30000268, 52]]),
        "needCoins": _tools.ROList([30000002, 150000])
    }),
    100403: _tools.RODict({
        "ID": 100403,
        "meridian": 10,
        "acupoint": 4,
        "level": 3,
        "prop": _tools.RODict({1001:52120548,1002:52120548,1003:52120448}),
        "needItems": _tools.ROList([[30000267, 54], [30000268, 54]]),
        "needCoins": _tools.ROList([30000002, 160000])
    }),
    100404: _tools.RODict({
        "ID": 100404,
        "meridian": 10,
        "acupoint": 4,
        "level": 4,
        "prop": _tools.RODict({1001:52120549,1002:52120549,1003:52120449}),
        "needItems": _tools.ROList([[30000267, 56], [30000268, 56]]),
        "needCoins": _tools.ROList([30000002, 170000])
    }),
    100405: _tools.RODict({
        "ID": 100405,
        "meridian": 10,
        "acupoint": 4,
        "level": 5,
        "prop": _tools.RODict({1001:52120550,1002:52120550,1003:52120450}),
        "needItems": _tools.ROList([[30000267, 58], [30000268, 58]]),
        "needCoins": _tools.ROList([30000002, 180000])
    }),
    100501: _tools.RODict({
        "ID": 100501,
        "meridian": 10,
        "acupoint": 5,
        "level": 1,
        "prop": _tools.RODict({0:52120646}),
        "needItems": _tools.ROList([[30000267, 50], [30000268, 50]]),
        "needCoins": _tools.ROList([30000002, 140000])
    }),
    100502: _tools.RODict({
        "ID": 100502,
        "meridian": 10,
        "acupoint": 5,
        "level": 2,
        "prop": _tools.RODict({0:52120647}),
        "needItems": _tools.ROList([[30000267, 52], [30000268, 52]]),
        "needCoins": _tools.ROList([30000002, 150000])
    }),
    100503: _tools.RODict({
        "ID": 100503,
        "meridian": 10,
        "acupoint": 5,
        "level": 3,
        "prop": _tools.RODict({0:52120648}),
        "needItems": _tools.ROList([[30000267, 54], [30000268, 54]]),
        "needCoins": _tools.ROList([30000002, 160000])
    }),
    100504: _tools.RODict({
        "ID": 100504,
        "meridian": 10,
        "acupoint": 5,
        "level": 4,
        "prop": _tools.RODict({0:52120649}),
        "needItems": _tools.ROList([[30000267, 56], [30000268, 56]]),
        "needCoins": _tools.ROList([30000002, 170000])
    }),
    100505: _tools.RODict({
        "ID": 100505,
        "meridian": 10,
        "acupoint": 5,
        "level": 5,
        "prop": _tools.RODict({0:52120650}),
        "needItems": _tools.ROList([[30000267, 58], [30000268, 58]]),
        "needCoins": _tools.ROList([30000002, 180000])
    }),
    100601: _tools.RODict({
        "ID": 100601,
        "meridian": 10,
        "acupoint": 6,
        "level": 1,
        "prop": _tools.RODict({0:52120746}),
        "needItems": _tools.ROList([[30000267, 50], [30000268, 50]]),
        "needCoins": _tools.ROList([30000002, 140000])
    }),
    100602: _tools.RODict({
        "ID": 100602,
        "meridian": 10,
        "acupoint": 6,
        "level": 2,
        "prop": _tools.RODict({0:52120747}),
        "needItems": _tools.ROList([[30000267, 52], [30000268, 52]]),
        "needCoins": _tools.ROList([30000002, 150000])
    }),
    100603: _tools.RODict({
        "ID": 100603,
        "meridian": 10,
        "acupoint": 6,
        "level": 3,
        "prop": _tools.RODict({0:52120748}),
        "needItems": _tools.ROList([[30000267, 54], [30000268, 54]]),
        "needCoins": _tools.ROList([30000002, 160000])
    }),
    100604: _tools.RODict({
        "ID": 100604,
        "meridian": 10,
        "acupoint": 6,
        "level": 4,
        "prop": _tools.RODict({0:52120749}),
        "needItems": _tools.ROList([[30000267, 56], [30000268, 56]]),
        "needCoins": _tools.ROList([30000002, 170000])
    }),
    100605: _tools.RODict({
        "ID": 100605,
        "meridian": 10,
        "acupoint": 6,
        "level": 5,
        "prop": _tools.RODict({0:52120750}),
        "needItems": _tools.ROList([[30000267, 58], [30000268, 58]]),
        "needCoins": _tools.ROList([30000002, 180000])
    }),
    100701: _tools.RODict({
        "ID": 100701,
        "meridian": 10,
        "acupoint": 7,
        "level": 1,
        "prop": _tools.RODict({0:52120846}),
        "needItems": _tools.ROList([[30000267, 50], [30000268, 50]]),
        "needCoins": _tools.ROList([30000002, 140000])
    }),
    100702: _tools.RODict({
        "ID": 100702,
        "meridian": 10,
        "acupoint": 7,
        "level": 2,
        "prop": _tools.RODict({0:52120847}),
        "needItems": _tools.ROList([[30000267, 52], [30000268, 52]]),
        "needCoins": _tools.ROList([30000002, 150000])
    }),
    100703: _tools.RODict({
        "ID": 100703,
        "meridian": 10,
        "acupoint": 7,
        "level": 3,
        "prop": _tools.RODict({0:52120848}),
        "needItems": _tools.ROList([[30000267, 54], [30000268, 54]]),
        "needCoins": _tools.ROList([30000002, 160000])
    }),
    100704: _tools.RODict({
        "ID": 100704,
        "meridian": 10,
        "acupoint": 7,
        "level": 4,
        "prop": _tools.RODict({0:52120849}),
        "needItems": _tools.ROList([[30000267, 56], [30000268, 56]]),
        "needCoins": _tools.ROList([30000002, 170000])
    }),
    100705: _tools.RODict({
        "ID": 100705,
        "meridian": 10,
        "acupoint": 7,
        "level": 5,
        "prop": _tools.RODict({0:52120850}),
        "needItems": _tools.ROList([[30000267, 58], [30000268, 58]]),
        "needCoins": _tools.ROList([30000002, 180000])
    }),
    100801: _tools.RODict({
        "ID": 100801,
        "meridian": 10,
        "acupoint": 8,
        "level": 1,
        "prop": _tools.RODict({0:52120946}),
        "needItems": _tools.ROList([[30000267, 50], [30000268, 50]]),
        "needCoins": _tools.ROList([30000002, 140000])
    }),
    100802: _tools.RODict({
        "ID": 100802,
        "meridian": 10,
        "acupoint": 8,
        "level": 2,
        "prop": _tools.RODict({0:52120947}),
        "needItems": _tools.ROList([[30000267, 52], [30000268, 52]]),
        "needCoins": _tools.ROList([30000002, 150000])
    }),
    100803: _tools.RODict({
        "ID": 100803,
        "meridian": 10,
        "acupoint": 8,
        "level": 3,
        "prop": _tools.RODict({0:52120948}),
        "needItems": _tools.ROList([[30000267, 54], [30000268, 54]]),
        "needCoins": _tools.ROList([30000002, 160000])
    }),
    100804: _tools.RODict({
        "ID": 100804,
        "meridian": 10,
        "acupoint": 8,
        "level": 4,
        "prop": _tools.RODict({0:52120949}),
        "needItems": _tools.ROList([[30000267, 56], [30000268, 56]]),
        "needCoins": _tools.ROList([30000002, 170000])
    }),
    100805: _tools.RODict({
        "ID": 100805,
        "meridian": 10,
        "acupoint": 8,
        "level": 5,
        "prop": _tools.RODict({0:52120950}),
        "needItems": _tools.ROList([[30000267, 58], [30000268, 58]]),
        "needCoins": _tools.ROList([30000002, 180000])
    }),
    110101: _tools.RODict({
        "ID": 110101,
        "meridian": 11,
        "acupoint": 1,
        "level": 1,
        "prop": _tools.RODict({0:52120051}),
        "needItems": _tools.ROList([[30000271, 10], [30000272, 10]]),
        "needCoins": _tools.ROList([30000002, 190000])
    }),
    110102: _tools.RODict({
        "ID": 110102,
        "meridian": 11,
        "acupoint": 1,
        "level": 2,
        "prop": _tools.RODict({0:52120052}),
        "needItems": _tools.ROList([[30000271, 12], [30000272, 12]]),
        "needCoins": _tools.ROList([30000002, 200000])
    }),
    110103: _tools.RODict({
        "ID": 110103,
        "meridian": 11,
        "acupoint": 1,
        "level": 3,
        "prop": _tools.RODict({0:52120053}),
        "needItems": _tools.ROList([[30000271, 14], [30000272, 14]]),
        "needCoins": _tools.ROList([30000002, 210000])
    }),
    110104: _tools.RODict({
        "ID": 110104,
        "meridian": 11,
        "acupoint": 1,
        "level": 4,
        "prop": _tools.RODict({0:52120054}),
        "needItems": _tools.ROList([[30000271, 16], [30000272, 16]]),
        "needCoins": _tools.ROList([30000002, 220000])
    }),
    110105: _tools.RODict({
        "ID": 110105,
        "meridian": 11,
        "acupoint": 1,
        "level": 5,
        "prop": _tools.RODict({0:52120055}),
        "needItems": _tools.ROList([[30000271, 18], [30000272, 18]]),
        "needCoins": _tools.ROList([30000002, 230000])
    }),
    110201: _tools.RODict({
        "ID": 110201,
        "meridian": 11,
        "acupoint": 2,
        "level": 1,
        "prop": _tools.RODict({0:52120151}),
        "needItems": _tools.ROList([[30000271, 10], [30000272, 10]]),
        "needCoins": _tools.ROList([30000002, 190000])
    }),
    110202: _tools.RODict({
        "ID": 110202,
        "meridian": 11,
        "acupoint": 2,
        "level": 2,
        "prop": _tools.RODict({0:52120152}),
        "needItems": _tools.ROList([[30000271, 12], [30000272, 12]]),
        "needCoins": _tools.ROList([30000002, 200000])
    }),
    110203: _tools.RODict({
        "ID": 110203,
        "meridian": 11,
        "acupoint": 2,
        "level": 3,
        "prop": _tools.RODict({0:52120153}),
        "needItems": _tools.ROList([[30000271, 14], [30000272, 14]]),
        "needCoins": _tools.ROList([30000002, 210000])
    }),
    110204: _tools.RODict({
        "ID": 110204,
        "meridian": 11,
        "acupoint": 2,
        "level": 4,
        "prop": _tools.RODict({0:52120154}),
        "needItems": _tools.ROList([[30000271, 16], [30000272, 16]]),
        "needCoins": _tools.ROList([30000002, 220000])
    }),
    110205: _tools.RODict({
        "ID": 110205,
        "meridian": 11,
        "acupoint": 2,
        "level": 5,
        "prop": _tools.RODict({0:52120155}),
        "needItems": _tools.ROList([[30000271, 18], [30000272, 18]]),
        "needCoins": _tools.ROList([30000002, 230000])
    }),
    110301: _tools.RODict({
        "ID": 110301,
        "meridian": 11,
        "acupoint": 3,
        "level": 1,
        "prop": _tools.RODict({1001:52120351,1002:52120351,1003:52120251}),
        "needItems": _tools.ROList([[30000271, 10], [30000272, 10]]),
        "needCoins": _tools.ROList([30000002, 190000])
    }),
    110302: _tools.RODict({
        "ID": 110302,
        "meridian": 11,
        "acupoint": 3,
        "level": 2,
        "prop": _tools.RODict({1001:52120352,1002:52120352,1003:52120252}),
        "needItems": _tools.ROList([[30000271, 12], [30000272, 12]]),
        "needCoins": _tools.ROList([30000002, 200000])
    }),
    110303: _tools.RODict({
        "ID": 110303,
        "meridian": 11,
        "acupoint": 3,
        "level": 3,
        "prop": _tools.RODict({1001:52120353,1002:52120353,1003:52120253}),
        "needItems": _tools.ROList([[30000271, 14], [30000272, 14]]),
        "needCoins": _tools.ROList([30000002, 210000])
    }),
    110304: _tools.RODict({
        "ID": 110304,
        "meridian": 11,
        "acupoint": 3,
        "level": 4,
        "prop": _tools.RODict({1001:52120354,1002:52120354,1003:52120254}),
        "needItems": _tools.ROList([[30000271, 16], [30000272, 16]]),
        "needCoins": _tools.ROList([30000002, 220000])
    }),
    110305: _tools.RODict({
        "ID": 110305,
        "meridian": 11,
        "acupoint": 3,
        "level": 5,
        "prop": _tools.RODict({1001:52120355,1002:52120355,1003:52120255}),
        "needItems": _tools.ROList([[30000271, 18], [30000272, 18]]),
        "needCoins": _tools.ROList([30000002, 230000])
    }),
    110401: _tools.RODict({
        "ID": 110401,
        "meridian": 11,
        "acupoint": 4,
        "level": 1,
        "prop": _tools.RODict({1001:52120551,1002:52120551,1003:52120451}),
        "needItems": _tools.ROList([[30000271, 10], [30000272, 10]]),
        "needCoins": _tools.ROList([30000002, 190000])
    }),
    110402: _tools.RODict({
        "ID": 110402,
        "meridian": 11,
        "acupoint": 4,
        "level": 2,
        "prop": _tools.RODict({1001:52120552,1002:52120552,1003:52120452}),
        "needItems": _tools.ROList([[30000271, 12], [30000272, 12]]),
        "needCoins": _tools.ROList([30000002, 200000])
    }),
    110403: _tools.RODict({
        "ID": 110403,
        "meridian": 11,
        "acupoint": 4,
        "level": 3,
        "prop": _tools.RODict({1001:52120553,1002:52120553,1003:52120453}),
        "needItems": _tools.ROList([[30000271, 14], [30000272, 14]]),
        "needCoins": _tools.ROList([30000002, 210000])
    }),
    110404: _tools.RODict({
        "ID": 110404,
        "meridian": 11,
        "acupoint": 4,
        "level": 4,
        "prop": _tools.RODict({1001:52120554,1002:52120554,1003:52120454}),
        "needItems": _tools.ROList([[30000271, 16], [30000272, 16]]),
        "needCoins": _tools.ROList([30000002, 220000])
    }),
    110405: _tools.RODict({
        "ID": 110405,
        "meridian": 11,
        "acupoint": 4,
        "level": 5,
        "prop": _tools.RODict({1001:52120555,1002:52120555,1003:52120455}),
        "needItems": _tools.ROList([[30000271, 18], [30000272, 18]]),
        "needCoins": _tools.ROList([30000002, 230000])
    }),
    110501: _tools.RODict({
        "ID": 110501,
        "meridian": 11,
        "acupoint": 5,
        "level": 1,
        "prop": _tools.RODict({0:52120651}),
        "needItems": _tools.ROList([[30000271, 10], [30000272, 10]]),
        "needCoins": _tools.ROList([30000002, 190000])
    }),
    110502: _tools.RODict({
        "ID": 110502,
        "meridian": 11,
        "acupoint": 5,
        "level": 2,
        "prop": _tools.RODict({0:52120652}),
        "needItems": _tools.ROList([[30000271, 12], [30000272, 12]]),
        "needCoins": _tools.ROList([30000002, 200000])
    }),
    110503: _tools.RODict({
        "ID": 110503,
        "meridian": 11,
        "acupoint": 5,
        "level": 3,
        "prop": _tools.RODict({0:52120653}),
        "needItems": _tools.ROList([[30000271, 14], [30000272, 14]]),
        "needCoins": _tools.ROList([30000002, 210000])
    }),
    110504: _tools.RODict({
        "ID": 110504,
        "meridian": 11,
        "acupoint": 5,
        "level": 4,
        "prop": _tools.RODict({0:52120654}),
        "needItems": _tools.ROList([[30000271, 16], [30000272, 16]]),
        "needCoins": _tools.ROList([30000002, 220000])
    }),
    110505: _tools.RODict({
        "ID": 110505,
        "meridian": 11,
        "acupoint": 5,
        "level": 5,
        "prop": _tools.RODict({0:52120655}),
        "needItems": _tools.ROList([[30000271, 18], [30000272, 18]]),
        "needCoins": _tools.ROList([30000002, 230000])
    }),
    110601: _tools.RODict({
        "ID": 110601,
        "meridian": 11,
        "acupoint": 6,
        "level": 1,
        "prop": _tools.RODict({0:52120751}),
        "needItems": _tools.ROList([[30000271, 10], [30000272, 10]]),
        "needCoins": _tools.ROList([30000002, 190000])
    }),
    110602: _tools.RODict({
        "ID": 110602,
        "meridian": 11,
        "acupoint": 6,
        "level": 2,
        "prop": _tools.RODict({0:52120752}),
        "needItems": _tools.ROList([[30000271, 12], [30000272, 12]]),
        "needCoins": _tools.ROList([30000002, 200000])
    }),
    110603: _tools.RODict({
        "ID": 110603,
        "meridian": 11,
        "acupoint": 6,
        "level": 3,
        "prop": _tools.RODict({0:52120753}),
        "needItems": _tools.ROList([[30000271, 14], [30000272, 14]]),
        "needCoins": _tools.ROList([30000002, 210000])
    }),
    110604: _tools.RODict({
        "ID": 110604,
        "meridian": 11,
        "acupoint": 6,
        "level": 4,
        "prop": _tools.RODict({0:52120754}),
        "needItems": _tools.ROList([[30000271, 16], [30000272, 16]]),
        "needCoins": _tools.ROList([30000002, 220000])
    }),
    110605: _tools.RODict({
        "ID": 110605,
        "meridian": 11,
        "acupoint": 6,
        "level": 5,
        "prop": _tools.RODict({0:52120755}),
        "needItems": _tools.ROList([[30000271, 18], [30000272, 18]]),
        "needCoins": _tools.ROList([30000002, 230000])
    }),
    110701: _tools.RODict({
        "ID": 110701,
        "meridian": 11,
        "acupoint": 7,
        "level": 1,
        "prop": _tools.RODict({0:52120851}),
        "needItems": _tools.ROList([[30000271, 10], [30000272, 10]]),
        "needCoins": _tools.ROList([30000002, 190000])
    }),
    110702: _tools.RODict({
        "ID": 110702,
        "meridian": 11,
        "acupoint": 7,
        "level": 2,
        "prop": _tools.RODict({0:52120852}),
        "needItems": _tools.ROList([[30000271, 12], [30000272, 12]]),
        "needCoins": _tools.ROList([30000002, 200000])
    }),
    110703: _tools.RODict({
        "ID": 110703,
        "meridian": 11,
        "acupoint": 7,
        "level": 3,
        "prop": _tools.RODict({0:52120853}),
        "needItems": _tools.ROList([[30000271, 14], [30000272, 14]]),
        "needCoins": _tools.ROList([30000002, 210000])
    }),
    110704: _tools.RODict({
        "ID": 110704,
        "meridian": 11,
        "acupoint": 7,
        "level": 4,
        "prop": _tools.RODict({0:52120854}),
        "needItems": _tools.ROList([[30000271, 16], [30000272, 16]]),
        "needCoins": _tools.ROList([30000002, 220000])
    }),
    110705: _tools.RODict({
        "ID": 110705,
        "meridian": 11,
        "acupoint": 7,
        "level": 5,
        "prop": _tools.RODict({0:52120855}),
        "needItems": _tools.ROList([[30000271, 18], [30000272, 18]]),
        "needCoins": _tools.ROList([30000002, 230000])
    }),
    110801: _tools.RODict({
        "ID": 110801,
        "meridian": 11,
        "acupoint": 8,
        "level": 1,
        "prop": _tools.RODict({0:52120951}),
        "needItems": _tools.ROList([[30000271, 10], [30000272, 10]]),
        "needCoins": _tools.ROList([30000002, 190000])
    }),
    110802: _tools.RODict({
        "ID": 110802,
        "meridian": 11,
        "acupoint": 8,
        "level": 2,
        "prop": _tools.RODict({0:52120952}),
        "needItems": _tools.ROList([[30000271, 12], [30000272, 12]]),
        "needCoins": _tools.ROList([30000002, 200000])
    }),
    110803: _tools.RODict({
        "ID": 110803,
        "meridian": 11,
        "acupoint": 8,
        "level": 3,
        "prop": _tools.RODict({0:52120953}),
        "needItems": _tools.ROList([[30000271, 14], [30000272, 14]]),
        "needCoins": _tools.ROList([30000002, 210000])
    }),
    110804: _tools.RODict({
        "ID": 110804,
        "meridian": 11,
        "acupoint": 8,
        "level": 4,
        "prop": _tools.RODict({0:52120954}),
        "needItems": _tools.ROList([[30000271, 16], [30000272, 16]]),
        "needCoins": _tools.ROList([30000002, 220000])
    }),
    110805: _tools.RODict({
        "ID": 110805,
        "meridian": 11,
        "acupoint": 8,
        "level": 5,
        "prop": _tools.RODict({0:52120955}),
        "needItems": _tools.ROList([[30000271, 18], [30000272, 18]]),
        "needCoins": _tools.ROList([30000002, 230000])
    }),
    120101: _tools.RODict({
        "ID": 120101,
        "meridian": 12,
        "acupoint": 1,
        "level": 1,
        "prop": _tools.RODict({0:52120056}),
        "needItems": _tools.ROList([[30000271, 20], [30000272, 20]]),
        "needCoins": _tools.ROList([30000002, 240000])
    }),
    120102: _tools.RODict({
        "ID": 120102,
        "meridian": 12,
        "acupoint": 1,
        "level": 2,
        "prop": _tools.RODict({0:52120057}),
        "needItems": _tools.ROList([[30000271, 22], [30000272, 22]]),
        "needCoins": _tools.ROList([30000002, 250000])
    }),
    120103: _tools.RODict({
        "ID": 120103,
        "meridian": 12,
        "acupoint": 1,
        "level": 3,
        "prop": _tools.RODict({0:52120058}),
        "needItems": _tools.ROList([[30000271, 24], [30000272, 24]]),
        "needCoins": _tools.ROList([30000002, 260000])
    }),
    120104: _tools.RODict({
        "ID": 120104,
        "meridian": 12,
        "acupoint": 1,
        "level": 4,
        "prop": _tools.RODict({0:52120059}),
        "needItems": _tools.ROList([[30000271, 26], [30000272, 26]]),
        "needCoins": _tools.ROList([30000002, 270000])
    }),
    120105: _tools.RODict({
        "ID": 120105,
        "meridian": 12,
        "acupoint": 1,
        "level": 5,
        "prop": _tools.RODict({0:52120060}),
        "needItems": _tools.ROList([[30000271, 28], [30000272, 28]]),
        "needCoins": _tools.ROList([30000002, 280000])
    }),
    120201: _tools.RODict({
        "ID": 120201,
        "meridian": 12,
        "acupoint": 2,
        "level": 1,
        "prop": _tools.RODict({0:52120156}),
        "needItems": _tools.ROList([[30000271, 20], [30000272, 20]]),
        "needCoins": _tools.ROList([30000002, 240000])
    }),
    120202: _tools.RODict({
        "ID": 120202,
        "meridian": 12,
        "acupoint": 2,
        "level": 2,
        "prop": _tools.RODict({0:52120157}),
        "needItems": _tools.ROList([[30000271, 22], [30000272, 22]]),
        "needCoins": _tools.ROList([30000002, 250000])
    }),
    120203: _tools.RODict({
        "ID": 120203,
        "meridian": 12,
        "acupoint": 2,
        "level": 3,
        "prop": _tools.RODict({0:52120158}),
        "needItems": _tools.ROList([[30000271, 24], [30000272, 24]]),
        "needCoins": _tools.ROList([30000002, 260000])
    }),
    120204: _tools.RODict({
        "ID": 120204,
        "meridian": 12,
        "acupoint": 2,
        "level": 4,
        "prop": _tools.RODict({0:52120159}),
        "needItems": _tools.ROList([[30000271, 26], [30000272, 26]]),
        "needCoins": _tools.ROList([30000002, 270000])
    }),
    120205: _tools.RODict({
        "ID": 120205,
        "meridian": 12,
        "acupoint": 2,
        "level": 5,
        "prop": _tools.RODict({0:52120160}),
        "needItems": _tools.ROList([[30000271, 28], [30000272, 28]]),
        "needCoins": _tools.ROList([30000002, 280000])
    }),
    120301: _tools.RODict({
        "ID": 120301,
        "meridian": 12,
        "acupoint": 3,
        "level": 1,
        "prop": _tools.RODict({1001:52120356,1002:52120356,1003:52120256}),
        "needItems": _tools.ROList([[30000271, 20], [30000272, 20]]),
        "needCoins": _tools.ROList([30000002, 240000])
    }),
    120302: _tools.RODict({
        "ID": 120302,
        "meridian": 12,
        "acupoint": 3,
        "level": 2,
        "prop": _tools.RODict({1001:52120357,1002:52120357,1003:52120257}),
        "needItems": _tools.ROList([[30000271, 22], [30000272, 22]]),
        "needCoins": _tools.ROList([30000002, 250000])
    }),
    120303: _tools.RODict({
        "ID": 120303,
        "meridian": 12,
        "acupoint": 3,
        "level": 3,
        "prop": _tools.RODict({1001:52120358,1002:52120358,1003:52120258}),
        "needItems": _tools.ROList([[30000271, 24], [30000272, 24]]),
        "needCoins": _tools.ROList([30000002, 260000])
    }),
    120304: _tools.RODict({
        "ID": 120304,
        "meridian": 12,
        "acupoint": 3,
        "level": 4,
        "prop": _tools.RODict({1001:52120359,1002:52120359,1003:52120259}),
        "needItems": _tools.ROList([[30000271, 26], [30000272, 26]]),
        "needCoins": _tools.ROList([30000002, 270000])
    }),
    120305: _tools.RODict({
        "ID": 120305,
        "meridian": 12,
        "acupoint": 3,
        "level": 5,
        "prop": _tools.RODict({1001:52120360,1002:52120360,1003:52120260}),
        "needItems": _tools.ROList([[30000271, 28], [30000272, 28]]),
        "needCoins": _tools.ROList([30000002, 280000])
    }),
    120401: _tools.RODict({
        "ID": 120401,
        "meridian": 12,
        "acupoint": 4,
        "level": 1,
        "prop": _tools.RODict({1001:52120556,1002:52120556,1003:52120456}),
        "needItems": _tools.ROList([[30000271, 20], [30000272, 20]]),
        "needCoins": _tools.ROList([30000002, 240000])
    }),
    120402: _tools.RODict({
        "ID": 120402,
        "meridian": 12,
        "acupoint": 4,
        "level": 2,
        "prop": _tools.RODict({1001:52120557,1002:52120557,1003:52120457}),
        "needItems": _tools.ROList([[30000271, 22], [30000272, 22]]),
        "needCoins": _tools.ROList([30000002, 250000])
    }),
    120403: _tools.RODict({
        "ID": 120403,
        "meridian": 12,
        "acupoint": 4,
        "level": 3,
        "prop": _tools.RODict({1001:52120558,1002:52120558,1003:52120458}),
        "needItems": _tools.ROList([[30000271, 24], [30000272, 24]]),
        "needCoins": _tools.ROList([30000002, 260000])
    }),
    120404: _tools.RODict({
        "ID": 120404,
        "meridian": 12,
        "acupoint": 4,
        "level": 4,
        "prop": _tools.RODict({1001:52120559,1002:52120559,1003:52120459}),
        "needItems": _tools.ROList([[30000271, 26], [30000272, 26]]),
        "needCoins": _tools.ROList([30000002, 270000])
    }),
    120405: _tools.RODict({
        "ID": 120405,
        "meridian": 12,
        "acupoint": 4,
        "level": 5,
        "prop": _tools.RODict({1001:52120560,1002:52120560,1003:52120460}),
        "needItems": _tools.ROList([[30000271, 28], [30000272, 28]]),
        "needCoins": _tools.ROList([30000002, 280000])
    }),
    120501: _tools.RODict({
        "ID": 120501,
        "meridian": 12,
        "acupoint": 5,
        "level": 1,
        "prop": _tools.RODict({0:52120656}),
        "needItems": _tools.ROList([[30000271, 20], [30000272, 20]]),
        "needCoins": _tools.ROList([30000002, 240000])
    }),
    120502: _tools.RODict({
        "ID": 120502,
        "meridian": 12,
        "acupoint": 5,
        "level": 2,
        "prop": _tools.RODict({0:52120657}),
        "needItems": _tools.ROList([[30000271, 22], [30000272, 22]]),
        "needCoins": _tools.ROList([30000002, 250000])
    }),
    120503: _tools.RODict({
        "ID": 120503,
        "meridian": 12,
        "acupoint": 5,
        "level": 3,
        "prop": _tools.RODict({0:52120658}),
        "needItems": _tools.ROList([[30000271, 24], [30000272, 24]]),
        "needCoins": _tools.ROList([30000002, 260000])
    }),
    120504: _tools.RODict({
        "ID": 120504,
        "meridian": 12,
        "acupoint": 5,
        "level": 4,
        "prop": _tools.RODict({0:52120659}),
        "needItems": _tools.ROList([[30000271, 26], [30000272, 26]]),
        "needCoins": _tools.ROList([30000002, 270000])
    }),
    120505: _tools.RODict({
        "ID": 120505,
        "meridian": 12,
        "acupoint": 5,
        "level": 5,
        "prop": _tools.RODict({0:52120660}),
        "needItems": _tools.ROList([[30000271, 28], [30000272, 28]]),
        "needCoins": _tools.ROList([30000002, 280000])
    }),
    120601: _tools.RODict({
        "ID": 120601,
        "meridian": 12,
        "acupoint": 6,
        "level": 1,
        "prop": _tools.RODict({0:52120756}),
        "needItems": _tools.ROList([[30000271, 20], [30000272, 20]]),
        "needCoins": _tools.ROList([30000002, 240000])
    }),
    120602: _tools.RODict({
        "ID": 120602,
        "meridian": 12,
        "acupoint": 6,
        "level": 2,
        "prop": _tools.RODict({0:52120757}),
        "needItems": _tools.ROList([[30000271, 22], [30000272, 22]]),
        "needCoins": _tools.ROList([30000002, 250000])
    }),
    120603: _tools.RODict({
        "ID": 120603,
        "meridian": 12,
        "acupoint": 6,
        "level": 3,
        "prop": _tools.RODict({0:52120758}),
        "needItems": _tools.ROList([[30000271, 24], [30000272, 24]]),
        "needCoins": _tools.ROList([30000002, 260000])
    }),
    120604: _tools.RODict({
        "ID": 120604,
        "meridian": 12,
        "acupoint": 6,
        "level": 4,
        "prop": _tools.RODict({0:52120759}),
        "needItems": _tools.ROList([[30000271, 26], [30000272, 26]]),
        "needCoins": _tools.ROList([30000002, 270000])
    }),
    120605: _tools.RODict({
        "ID": 120605,
        "meridian": 12,
        "acupoint": 6,
        "level": 5,
        "prop": _tools.RODict({0:52120760}),
        "needItems": _tools.ROList([[30000271, 28], [30000272, 28]]),
        "needCoins": _tools.ROList([30000002, 280000])
    }),
    120701: _tools.RODict({
        "ID": 120701,
        "meridian": 12,
        "acupoint": 7,
        "level": 1,
        "prop": _tools.RODict({0:52120856}),
        "needItems": _tools.ROList([[30000271, 20], [30000272, 20]]),
        "needCoins": _tools.ROList([30000002, 240000])
    }),
    120702: _tools.RODict({
        "ID": 120702,
        "meridian": 12,
        "acupoint": 7,
        "level": 2,
        "prop": _tools.RODict({0:52120857}),
        "needItems": _tools.ROList([[30000271, 22], [30000272, 22]]),
        "needCoins": _tools.ROList([30000002, 250000])
    }),
    120703: _tools.RODict({
        "ID": 120703,
        "meridian": 12,
        "acupoint": 7,
        "level": 3,
        "prop": _tools.RODict({0:52120858}),
        "needItems": _tools.ROList([[30000271, 24], [30000272, 24]]),
        "needCoins": _tools.ROList([30000002, 260000])
    }),
    120704: _tools.RODict({
        "ID": 120704,
        "meridian": 12,
        "acupoint": 7,
        "level": 4,
        "prop": _tools.RODict({0:52120859}),
        "needItems": _tools.ROList([[30000271, 26], [30000272, 26]]),
        "needCoins": _tools.ROList([30000002, 270000])
    }),
    120705: _tools.RODict({
        "ID": 120705,
        "meridian": 12,
        "acupoint": 7,
        "level": 5,
        "prop": _tools.RODict({0:52120860}),
        "needItems": _tools.ROList([[30000271, 28], [30000272, 28]]),
        "needCoins": _tools.ROList([30000002, 280000])
    }),
    120801: _tools.RODict({
        "ID": 120801,
        "meridian": 12,
        "acupoint": 8,
        "level": 1,
        "prop": _tools.RODict({0:52120956}),
        "needItems": _tools.ROList([[30000271, 20], [30000272, 20]]),
        "needCoins": _tools.ROList([30000002, 240000])
    }),
    120802: _tools.RODict({
        "ID": 120802,
        "meridian": 12,
        "acupoint": 8,
        "level": 2,
        "prop": _tools.RODict({0:52120957}),
        "needItems": _tools.ROList([[30000271, 22], [30000272, 22]]),
        "needCoins": _tools.ROList([30000002, 250000])
    }),
    120803: _tools.RODict({
        "ID": 120803,
        "meridian": 12,
        "acupoint": 8,
        "level": 3,
        "prop": _tools.RODict({0:52120958}),
        "needItems": _tools.ROList([[30000271, 24], [30000272, 24]]),
        "needCoins": _tools.ROList([30000002, 260000])
    }),
    120804: _tools.RODict({
        "ID": 120804,
        "meridian": 12,
        "acupoint": 8,
        "level": 4,
        "prop": _tools.RODict({0:52120959}),
        "needItems": _tools.ROList([[30000271, 26], [30000272, 26]]),
        "needCoins": _tools.ROList([30000002, 270000])
    }),
    120805: _tools.RODict({
        "ID": 120805,
        "meridian": 12,
        "acupoint": 8,
        "level": 5,
        "prop": _tools.RODict({0:52120960}),
        "needItems": _tools.ROList([[30000271, 28], [30000272, 28]]),
        "needCoins": _tools.ROList([30000002, 280000])
    }),
    130101: _tools.RODict({
        "ID": 130101,
        "meridian": 13,
        "acupoint": 1,
        "level": 1,
        "prop": _tools.RODict({0:52120061}),
        "needItems": _tools.ROList([[30000271, 30], [30000272, 30]]),
        "needCoins": _tools.ROList([30000002, 290000])
    }),
    130102: _tools.RODict({
        "ID": 130102,
        "meridian": 13,
        "acupoint": 1,
        "level": 2,
        "prop": _tools.RODict({0:52120062}),
        "needItems": _tools.ROList([[30000271, 32], [30000272, 32]]),
        "needCoins": _tools.ROList([30000002, 300000])
    }),
    130103: _tools.RODict({
        "ID": 130103,
        "meridian": 13,
        "acupoint": 1,
        "level": 3,
        "prop": _tools.RODict({0:52120063}),
        "needItems": _tools.ROList([[30000271, 34], [30000272, 34]]),
        "needCoins": _tools.ROList([30000002, 310000])
    }),
    130104: _tools.RODict({
        "ID": 130104,
        "meridian": 13,
        "acupoint": 1,
        "level": 4,
        "prop": _tools.RODict({0:52120064}),
        "needItems": _tools.ROList([[30000271, 36], [30000272, 36]]),
        "needCoins": _tools.ROList([30000002, 320000])
    }),
    130105: _tools.RODict({
        "ID": 130105,
        "meridian": 13,
        "acupoint": 1,
        "level": 5,
        "prop": _tools.RODict({0:52120065}),
        "needItems": _tools.ROList([[30000271, 38], [30000272, 38]]),
        "needCoins": _tools.ROList([30000002, 330000])
    }),
    130201: _tools.RODict({
        "ID": 130201,
        "meridian": 13,
        "acupoint": 2,
        "level": 1,
        "prop": _tools.RODict({0:52120161}),
        "needItems": _tools.ROList([[30000271, 30], [30000272, 30]]),
        "needCoins": _tools.ROList([30000002, 290000])
    }),
    130202: _tools.RODict({
        "ID": 130202,
        "meridian": 13,
        "acupoint": 2,
        "level": 2,
        "prop": _tools.RODict({0:52120162}),
        "needItems": _tools.ROList([[30000271, 32], [30000272, 32]]),
        "needCoins": _tools.ROList([30000002, 300000])
    }),
    130203: _tools.RODict({
        "ID": 130203,
        "meridian": 13,
        "acupoint": 2,
        "level": 3,
        "prop": _tools.RODict({0:52120163}),
        "needItems": _tools.ROList([[30000271, 34], [30000272, 34]]),
        "needCoins": _tools.ROList([30000002, 310000])
    }),
    130204: _tools.RODict({
        "ID": 130204,
        "meridian": 13,
        "acupoint": 2,
        "level": 4,
        "prop": _tools.RODict({0:52120164}),
        "needItems": _tools.ROList([[30000271, 36], [30000272, 36]]),
        "needCoins": _tools.ROList([30000002, 320000])
    }),
    130205: _tools.RODict({
        "ID": 130205,
        "meridian": 13,
        "acupoint": 2,
        "level": 5,
        "prop": _tools.RODict({0:52120165}),
        "needItems": _tools.ROList([[30000271, 38], [30000272, 38]]),
        "needCoins": _tools.ROList([30000002, 330000])
    }),
    130301: _tools.RODict({
        "ID": 130301,
        "meridian": 13,
        "acupoint": 3,
        "level": 1,
        "prop": _tools.RODict({1001:52120361,1002:52120361,1003:52120261}),
        "needItems": _tools.ROList([[30000271, 30], [30000272, 30]]),
        "needCoins": _tools.ROList([30000002, 290000])
    }),
    130302: _tools.RODict({
        "ID": 130302,
        "meridian": 13,
        "acupoint": 3,
        "level": 2,
        "prop": _tools.RODict({1001:52120362,1002:52120362,1003:52120262}),
        "needItems": _tools.ROList([[30000271, 32], [30000272, 32]]),
        "needCoins": _tools.ROList([30000002, 300000])
    }),
    130303: _tools.RODict({
        "ID": 130303,
        "meridian": 13,
        "acupoint": 3,
        "level": 3,
        "prop": _tools.RODict({1001:52120363,1002:52120363,1003:52120263}),
        "needItems": _tools.ROList([[30000271, 34], [30000272, 34]]),
        "needCoins": _tools.ROList([30000002, 310000])
    }),
    130304: _tools.RODict({
        "ID": 130304,
        "meridian": 13,
        "acupoint": 3,
        "level": 4,
        "prop": _tools.RODict({1001:52120364,1002:52120364,1003:52120264}),
        "needItems": _tools.ROList([[30000271, 36], [30000272, 36]]),
        "needCoins": _tools.ROList([30000002, 320000])
    }),
    130305: _tools.RODict({
        "ID": 130305,
        "meridian": 13,
        "acupoint": 3,
        "level": 5,
        "prop": _tools.RODict({1001:52120365,1002:52120365,1003:52120265}),
        "needItems": _tools.ROList([[30000271, 38], [30000272, 38]]),
        "needCoins": _tools.ROList([30000002, 330000])
    }),
    130401: _tools.RODict({
        "ID": 130401,
        "meridian": 13,
        "acupoint": 4,
        "level": 1,
        "prop": _tools.RODict({1001:52120561,1002:52120561,1003:52120461}),
        "needItems": _tools.ROList([[30000271, 30], [30000272, 30]]),
        "needCoins": _tools.ROList([30000002, 290000])
    }),
    130402: _tools.RODict({
        "ID": 130402,
        "meridian": 13,
        "acupoint": 4,
        "level": 2,
        "prop": _tools.RODict({1001:52120562,1002:52120562,1003:52120462}),
        "needItems": _tools.ROList([[30000271, 32], [30000272, 32]]),
        "needCoins": _tools.ROList([30000002, 300000])
    }),
    130403: _tools.RODict({
        "ID": 130403,
        "meridian": 13,
        "acupoint": 4,
        "level": 3,
        "prop": _tools.RODict({1001:52120563,1002:52120563,1003:52120463}),
        "needItems": _tools.ROList([[30000271, 34], [30000272, 34]]),
        "needCoins": _tools.ROList([30000002, 310000])
    }),
    130404: _tools.RODict({
        "ID": 130404,
        "meridian": 13,
        "acupoint": 4,
        "level": 4,
        "prop": _tools.RODict({1001:52120564,1002:52120564,1003:52120464}),
        "needItems": _tools.ROList([[30000271, 36], [30000272, 36]]),
        "needCoins": _tools.ROList([30000002, 320000])
    }),
    130405: _tools.RODict({
        "ID": 130405,
        "meridian": 13,
        "acupoint": 4,
        "level": 5,
        "prop": _tools.RODict({1001:52120565,1002:52120565,1003:52120465}),
        "needItems": _tools.ROList([[30000271, 38], [30000272, 38]]),
        "needCoins": _tools.ROList([30000002, 330000])
    }),
    130501: _tools.RODict({
        "ID": 130501,
        "meridian": 13,
        "acupoint": 5,
        "level": 1,
        "prop": _tools.RODict({0:52120661}),
        "needItems": _tools.ROList([[30000271, 30], [30000272, 30]]),
        "needCoins": _tools.ROList([30000002, 290000])
    }),
    130502: _tools.RODict({
        "ID": 130502,
        "meridian": 13,
        "acupoint": 5,
        "level": 2,
        "prop": _tools.RODict({0:52120662}),
        "needItems": _tools.ROList([[30000271, 32], [30000272, 32]]),
        "needCoins": _tools.ROList([30000002, 300000])
    }),
    130503: _tools.RODict({
        "ID": 130503,
        "meridian": 13,
        "acupoint": 5,
        "level": 3,
        "prop": _tools.RODict({0:52120663}),
        "needItems": _tools.ROList([[30000271, 34], [30000272, 34]]),
        "needCoins": _tools.ROList([30000002, 310000])
    }),
    130504: _tools.RODict({
        "ID": 130504,
        "meridian": 13,
        "acupoint": 5,
        "level": 4,
        "prop": _tools.RODict({0:52120664}),
        "needItems": _tools.ROList([[30000271, 36], [30000272, 36]]),
        "needCoins": _tools.ROList([30000002, 320000])
    }),
    130505: _tools.RODict({
        "ID": 130505,
        "meridian": 13,
        "acupoint": 5,
        "level": 5,
        "prop": _tools.RODict({0:52120665}),
        "needItems": _tools.ROList([[30000271, 38], [30000272, 38]]),
        "needCoins": _tools.ROList([30000002, 330000])
    }),
    130601: _tools.RODict({
        "ID": 130601,
        "meridian": 13,
        "acupoint": 6,
        "level": 1,
        "prop": _tools.RODict({0:52120761}),
        "needItems": _tools.ROList([[30000271, 30], [30000272, 30]]),
        "needCoins": _tools.ROList([30000002, 290000])
    }),
    130602: _tools.RODict({
        "ID": 130602,
        "meridian": 13,
        "acupoint": 6,
        "level": 2,
        "prop": _tools.RODict({0:52120762}),
        "needItems": _tools.ROList([[30000271, 32], [30000272, 32]]),
        "needCoins": _tools.ROList([30000002, 300000])
    }),
    130603: _tools.RODict({
        "ID": 130603,
        "meridian": 13,
        "acupoint": 6,
        "level": 3,
        "prop": _tools.RODict({0:52120763}),
        "needItems": _tools.ROList([[30000271, 34], [30000272, 34]]),
        "needCoins": _tools.ROList([30000002, 310000])
    }),
    130604: _tools.RODict({
        "ID": 130604,
        "meridian": 13,
        "acupoint": 6,
        "level": 4,
        "prop": _tools.RODict({0:52120764}),
        "needItems": _tools.ROList([[30000271, 36], [30000272, 36]]),
        "needCoins": _tools.ROList([30000002, 320000])
    }),
    130605: _tools.RODict({
        "ID": 130605,
        "meridian": 13,
        "acupoint": 6,
        "level": 5,
        "prop": _tools.RODict({0:52120765}),
        "needItems": _tools.ROList([[30000271, 38], [30000272, 38]]),
        "needCoins": _tools.ROList([30000002, 330000])
    }),
    130701: _tools.RODict({
        "ID": 130701,
        "meridian": 13,
        "acupoint": 7,
        "level": 1,
        "prop": _tools.RODict({0:52120861}),
        "needItems": _tools.ROList([[30000271, 30], [30000272, 30]]),
        "needCoins": _tools.ROList([30000002, 290000])
    }),
    130702: _tools.RODict({
        "ID": 130702,
        "meridian": 13,
        "acupoint": 7,
        "level": 2,
        "prop": _tools.RODict({0:52120862}),
        "needItems": _tools.ROList([[30000271, 32], [30000272, 32]]),
        "needCoins": _tools.ROList([30000002, 300000])
    }),
    130703: _tools.RODict({
        "ID": 130703,
        "meridian": 13,
        "acupoint": 7,
        "level": 3,
        "prop": _tools.RODict({0:52120863}),
        "needItems": _tools.ROList([[30000271, 34], [30000272, 34]]),
        "needCoins": _tools.ROList([30000002, 310000])
    }),
    130704: _tools.RODict({
        "ID": 130704,
        "meridian": 13,
        "acupoint": 7,
        "level": 4,
        "prop": _tools.RODict({0:52120864}),
        "needItems": _tools.ROList([[30000271, 36], [30000272, 36]]),
        "needCoins": _tools.ROList([30000002, 320000])
    }),
    130705: _tools.RODict({
        "ID": 130705,
        "meridian": 13,
        "acupoint": 7,
        "level": 5,
        "prop": _tools.RODict({0:52120865}),
        "needItems": _tools.ROList([[30000271, 38], [30000272, 38]]),
        "needCoins": _tools.ROList([30000002, 330000])
    }),
    130801: _tools.RODict({
        "ID": 130801,
        "meridian": 13,
        "acupoint": 8,
        "level": 1,
        "prop": _tools.RODict({0:52120961}),
        "needItems": _tools.ROList([[30000271, 30], [30000272, 30]]),
        "needCoins": _tools.ROList([30000002, 290000])
    }),
    130802: _tools.RODict({
        "ID": 130802,
        "meridian": 13,
        "acupoint": 8,
        "level": 2,
        "prop": _tools.RODict({0:52120962}),
        "needItems": _tools.ROList([[30000271, 32], [30000272, 32]]),
        "needCoins": _tools.ROList([30000002, 300000])
    }),
    130803: _tools.RODict({
        "ID": 130803,
        "meridian": 13,
        "acupoint": 8,
        "level": 3,
        "prop": _tools.RODict({0:52120963}),
        "needItems": _tools.ROList([[30000271, 34], [30000272, 34]]),
        "needCoins": _tools.ROList([30000002, 310000])
    }),
    130804: _tools.RODict({
        "ID": 130804,
        "meridian": 13,
        "acupoint": 8,
        "level": 4,
        "prop": _tools.RODict({0:52120964}),
        "needItems": _tools.ROList([[30000271, 36], [30000272, 36]]),
        "needCoins": _tools.ROList([30000002, 320000])
    }),
    130805: _tools.RODict({
        "ID": 130805,
        "meridian": 13,
        "acupoint": 8,
        "level": 5,
        "prop": _tools.RODict({0:52120965}),
        "needItems": _tools.ROList([[30000271, 38], [30000272, 38]]),
        "needCoins": _tools.ROList([30000002, 330000])
    }),
    140101: _tools.RODict({
        "ID": 140101,
        "meridian": 14,
        "acupoint": 1,
        "level": 1,
        "prop": _tools.RODict({0:52120066}),
        "needItems": _tools.ROList([[30000271, 40], [30000272, 40]]),
        "needCoins": _tools.ROList([30000002, 340000])
    }),
    140102: _tools.RODict({
        "ID": 140102,
        "meridian": 14,
        "acupoint": 1,
        "level": 2,
        "prop": _tools.RODict({0:52120067}),
        "needItems": _tools.ROList([[30000271, 42], [30000272, 42]]),
        "needCoins": _tools.ROList([30000002, 350000])
    }),
    140103: _tools.RODict({
        "ID": 140103,
        "meridian": 14,
        "acupoint": 1,
        "level": 3,
        "prop": _tools.RODict({0:52120068}),
        "needItems": _tools.ROList([[30000271, 44], [30000272, 44]]),
        "needCoins": _tools.ROList([30000002, 360000])
    }),
    140104: _tools.RODict({
        "ID": 140104,
        "meridian": 14,
        "acupoint": 1,
        "level": 4,
        "prop": _tools.RODict({0:52120069}),
        "needItems": _tools.ROList([[30000271, 46], [30000272, 46]]),
        "needCoins": _tools.ROList([30000002, 370000])
    }),
    140105: _tools.RODict({
        "ID": 140105,
        "meridian": 14,
        "acupoint": 1,
        "level": 5,
        "prop": _tools.RODict({0:52120070}),
        "needItems": _tools.ROList([[30000271, 48], [30000272, 48]]),
        "needCoins": _tools.ROList([30000002, 380000])
    }),
    140201: _tools.RODict({
        "ID": 140201,
        "meridian": 14,
        "acupoint": 2,
        "level": 1,
        "prop": _tools.RODict({0:52120166}),
        "needItems": _tools.ROList([[30000271, 40], [30000272, 40]]),
        "needCoins": _tools.ROList([30000002, 340000])
    }),
    140202: _tools.RODict({
        "ID": 140202,
        "meridian": 14,
        "acupoint": 2,
        "level": 2,
        "prop": _tools.RODict({0:52120167}),
        "needItems": _tools.ROList([[30000271, 42], [30000272, 42]]),
        "needCoins": _tools.ROList([30000002, 350000])
    }),
    140203: _tools.RODict({
        "ID": 140203,
        "meridian": 14,
        "acupoint": 2,
        "level": 3,
        "prop": _tools.RODict({0:52120168}),
        "needItems": _tools.ROList([[30000271, 44], [30000272, 44]]),
        "needCoins": _tools.ROList([30000002, 360000])
    }),
    140204: _tools.RODict({
        "ID": 140204,
        "meridian": 14,
        "acupoint": 2,
        "level": 4,
        "prop": _tools.RODict({0:52120169}),
        "needItems": _tools.ROList([[30000271, 46], [30000272, 46]]),
        "needCoins": _tools.ROList([30000002, 370000])
    }),
    140205: _tools.RODict({
        "ID": 140205,
        "meridian": 14,
        "acupoint": 2,
        "level": 5,
        "prop": _tools.RODict({0:52120170}),
        "needItems": _tools.ROList([[30000271, 48], [30000272, 48]]),
        "needCoins": _tools.ROList([30000002, 380000])
    }),
    140301: _tools.RODict({
        "ID": 140301,
        "meridian": 14,
        "acupoint": 3,
        "level": 1,
        "prop": _tools.RODict({1001:52120366,1002:52120366,1003:52120266}),
        "needItems": _tools.ROList([[30000271, 40], [30000272, 40]]),
        "needCoins": _tools.ROList([30000002, 340000])
    }),
    140302: _tools.RODict({
        "ID": 140302,
        "meridian": 14,
        "acupoint": 3,
        "level": 2,
        "prop": _tools.RODict({1001:52120367,1002:52120367,1003:52120267}),
        "needItems": _tools.ROList([[30000271, 42], [30000272, 42]]),
        "needCoins": _tools.ROList([30000002, 350000])
    }),
    140303: _tools.RODict({
        "ID": 140303,
        "meridian": 14,
        "acupoint": 3,
        "level": 3,
        "prop": _tools.RODict({1001:52120368,1002:52120368,1003:52120268}),
        "needItems": _tools.ROList([[30000271, 44], [30000272, 44]]),
        "needCoins": _tools.ROList([30000002, 360000])
    }),
    140304: _tools.RODict({
        "ID": 140304,
        "meridian": 14,
        "acupoint": 3,
        "level": 4,
        "prop": _tools.RODict({1001:52120369,1002:52120369,1003:52120269}),
        "needItems": _tools.ROList([[30000271, 46], [30000272, 46]]),
        "needCoins": _tools.ROList([30000002, 370000])
    }),
    140305: _tools.RODict({
        "ID": 140305,
        "meridian": 14,
        "acupoint": 3,
        "level": 5,
        "prop": _tools.RODict({1001:52120370,1002:52120370,1003:52120270}),
        "needItems": _tools.ROList([[30000271, 48], [30000272, 48]]),
        "needCoins": _tools.ROList([30000002, 380000])
    }),
    140401: _tools.RODict({
        "ID": 140401,
        "meridian": 14,
        "acupoint": 4,
        "level": 1,
        "prop": _tools.RODict({1001:52120566,1002:52120566,1003:52120466}),
        "needItems": _tools.ROList([[30000271, 40], [30000272, 40]]),
        "needCoins": _tools.ROList([30000002, 340000])
    }),
    140402: _tools.RODict({
        "ID": 140402,
        "meridian": 14,
        "acupoint": 4,
        "level": 2,
        "prop": _tools.RODict({1001:52120567,1002:52120567,1003:52120467}),
        "needItems": _tools.ROList([[30000271, 42], [30000272, 42]]),
        "needCoins": _tools.ROList([30000002, 350000])
    }),
    140403: _tools.RODict({
        "ID": 140403,
        "meridian": 14,
        "acupoint": 4,
        "level": 3,
        "prop": _tools.RODict({1001:52120568,1002:52120568,1003:52120468}),
        "needItems": _tools.ROList([[30000271, 44], [30000272, 44]]),
        "needCoins": _tools.ROList([30000002, 360000])
    }),
    140404: _tools.RODict({
        "ID": 140404,
        "meridian": 14,
        "acupoint": 4,
        "level": 4,
        "prop": _tools.RODict({1001:52120569,1002:52120569,1003:52120469}),
        "needItems": _tools.ROList([[30000271, 46], [30000272, 46]]),
        "needCoins": _tools.ROList([30000002, 370000])
    }),
    140405: _tools.RODict({
        "ID": 140405,
        "meridian": 14,
        "acupoint": 4,
        "level": 5,
        "prop": _tools.RODict({1001:52120570,1002:52120570,1003:52120470}),
        "needItems": _tools.ROList([[30000271, 48], [30000272, 48]]),
        "needCoins": _tools.ROList([30000002, 380000])
    }),
    140501: _tools.RODict({
        "ID": 140501,
        "meridian": 14,
        "acupoint": 5,
        "level": 1,
        "prop": _tools.RODict({0:52120666}),
        "needItems": _tools.ROList([[30000271, 40], [30000272, 40]]),
        "needCoins": _tools.ROList([30000002, 340000])
    }),
    140502: _tools.RODict({
        "ID": 140502,
        "meridian": 14,
        "acupoint": 5,
        "level": 2,
        "prop": _tools.RODict({0:52120667}),
        "needItems": _tools.ROList([[30000271, 42], [30000272, 42]]),
        "needCoins": _tools.ROList([30000002, 350000])
    }),
    140503: _tools.RODict({
        "ID": 140503,
        "meridian": 14,
        "acupoint": 5,
        "level": 3,
        "prop": _tools.RODict({0:52120668}),
        "needItems": _tools.ROList([[30000271, 44], [30000272, 44]]),
        "needCoins": _tools.ROList([30000002, 360000])
    }),
    140504: _tools.RODict({
        "ID": 140504,
        "meridian": 14,
        "acupoint": 5,
        "level": 4,
        "prop": _tools.RODict({0:52120669}),
        "needItems": _tools.ROList([[30000271, 46], [30000272, 46]]),
        "needCoins": _tools.ROList([30000002, 370000])
    }),
    140505: _tools.RODict({
        "ID": 140505,
        "meridian": 14,
        "acupoint": 5,
        "level": 5,
        "prop": _tools.RODict({0:52120670}),
        "needItems": _tools.ROList([[30000271, 48], [30000272, 48]]),
        "needCoins": _tools.ROList([30000002, 380000])
    }),
    140601: _tools.RODict({
        "ID": 140601,
        "meridian": 14,
        "acupoint": 6,
        "level": 1,
        "prop": _tools.RODict({0:52120766}),
        "needItems": _tools.ROList([[30000271, 40], [30000272, 40]]),
        "needCoins": _tools.ROList([30000002, 340000])
    }),
    140602: _tools.RODict({
        "ID": 140602,
        "meridian": 14,
        "acupoint": 6,
        "level": 2,
        "prop": _tools.RODict({0:52120767}),
        "needItems": _tools.ROList([[30000271, 42], [30000272, 42]]),
        "needCoins": _tools.ROList([30000002, 350000])
    }),
    140603: _tools.RODict({
        "ID": 140603,
        "meridian": 14,
        "acupoint": 6,
        "level": 3,
        "prop": _tools.RODict({0:52120768}),
        "needItems": _tools.ROList([[30000271, 44], [30000272, 44]]),
        "needCoins": _tools.ROList([30000002, 360000])
    }),
    140604: _tools.RODict({
        "ID": 140604,
        "meridian": 14,
        "acupoint": 6,
        "level": 4,
        "prop": _tools.RODict({0:52120769}),
        "needItems": _tools.ROList([[30000271, 46], [30000272, 46]]),
        "needCoins": _tools.ROList([30000002, 370000])
    }),
    140605: _tools.RODict({
        "ID": 140605,
        "meridian": 14,
        "acupoint": 6,
        "level": 5,
        "prop": _tools.RODict({0:52120770}),
        "needItems": _tools.ROList([[30000271, 48], [30000272, 48]]),
        "needCoins": _tools.ROList([30000002, 380000])
    }),
    140701: _tools.RODict({
        "ID": 140701,
        "meridian": 14,
        "acupoint": 7,
        "level": 1,
        "prop": _tools.RODict({0:52120866}),
        "needItems": _tools.ROList([[30000271, 40], [30000272, 40]]),
        "needCoins": _tools.ROList([30000002, 340000])
    }),
    140702: _tools.RODict({
        "ID": 140702,
        "meridian": 14,
        "acupoint": 7,
        "level": 2,
        "prop": _tools.RODict({0:52120867}),
        "needItems": _tools.ROList([[30000271, 42], [30000272, 42]]),
        "needCoins": _tools.ROList([30000002, 350000])
    }),
    140703: _tools.RODict({
        "ID": 140703,
        "meridian": 14,
        "acupoint": 7,
        "level": 3,
        "prop": _tools.RODict({0:52120868}),
        "needItems": _tools.ROList([[30000271, 44], [30000272, 44]]),
        "needCoins": _tools.ROList([30000002, 360000])
    }),
    140704: _tools.RODict({
        "ID": 140704,
        "meridian": 14,
        "acupoint": 7,
        "level": 4,
        "prop": _tools.RODict({0:52120869}),
        "needItems": _tools.ROList([[30000271, 46], [30000272, 46]]),
        "needCoins": _tools.ROList([30000002, 370000])
    }),
    140705: _tools.RODict({
        "ID": 140705,
        "meridian": 14,
        "acupoint": 7,
        "level": 5,
        "prop": _tools.RODict({0:52120870}),
        "needItems": _tools.ROList([[30000271, 48], [30000272, 48]]),
        "needCoins": _tools.ROList([30000002, 380000])
    }),
    140801: _tools.RODict({
        "ID": 140801,
        "meridian": 14,
        "acupoint": 8,
        "level": 1,
        "prop": _tools.RODict({0:52120966}),
        "needItems": _tools.ROList([[30000271, 40], [30000272, 40]]),
        "needCoins": _tools.ROList([30000002, 340000])
    }),
    140802: _tools.RODict({
        "ID": 140802,
        "meridian": 14,
        "acupoint": 8,
        "level": 2,
        "prop": _tools.RODict({0:52120967}),
        "needItems": _tools.ROList([[30000271, 42], [30000272, 42]]),
        "needCoins": _tools.ROList([30000002, 350000])
    }),
    140803: _tools.RODict({
        "ID": 140803,
        "meridian": 14,
        "acupoint": 8,
        "level": 3,
        "prop": _tools.RODict({0:52120968}),
        "needItems": _tools.ROList([[30000271, 44], [30000272, 44]]),
        "needCoins": _tools.ROList([30000002, 360000])
    }),
    140804: _tools.RODict({
        "ID": 140804,
        "meridian": 14,
        "acupoint": 8,
        "level": 4,
        "prop": _tools.RODict({0:52120969}),
        "needItems": _tools.ROList([[30000271, 46], [30000272, 46]]),
        "needCoins": _tools.ROList([30000002, 370000])
    }),
    140805: _tools.RODict({
        "ID": 140805,
        "meridian": 14,
        "acupoint": 8,
        "level": 5,
        "prop": _tools.RODict({0:52120970}),
        "needItems": _tools.ROList([[30000271, 48], [30000272, 48]]),
        "needCoins": _tools.ROList([30000002, 380000])
    }),
    150101: _tools.RODict({
        "ID": 150101,
        "meridian": 15,
        "acupoint": 1,
        "level": 1,
        "prop": _tools.RODict({0:52120071}),
        "needItems": _tools.ROList([[30000271, 50], [30000272, 50]]),
        "needCoins": _tools.ROList([30000002, 390000])
    }),
    150102: _tools.RODict({
        "ID": 150102,
        "meridian": 15,
        "acupoint": 1,
        "level": 2,
        "prop": _tools.RODict({0:52120072}),
        "needItems": _tools.ROList([[30000271, 52], [30000272, 52]]),
        "needCoins": _tools.ROList([30000002, 400000])
    }),
    150103: _tools.RODict({
        "ID": 150103,
        "meridian": 15,
        "acupoint": 1,
        "level": 3,
        "prop": _tools.RODict({0:52120073}),
        "needItems": _tools.ROList([[30000271, 54], [30000272, 54]]),
        "needCoins": _tools.ROList([30000002, 410000])
    }),
    150104: _tools.RODict({
        "ID": 150104,
        "meridian": 15,
        "acupoint": 1,
        "level": 4,
        "prop": _tools.RODict({0:52120074}),
        "needItems": _tools.ROList([[30000271, 56], [30000272, 56]]),
        "needCoins": _tools.ROList([30000002, 420000])
    }),
    150105: _tools.RODict({
        "ID": 150105,
        "meridian": 15,
        "acupoint": 1,
        "level": 5,
        "prop": _tools.RODict({0:52120075}),
        "needItems": _tools.ROList([[30000271, 58], [30000272, 58]]),
        "needCoins": _tools.ROList([30000002, 430000])
    }),
    150201: _tools.RODict({
        "ID": 150201,
        "meridian": 15,
        "acupoint": 2,
        "level": 1,
        "prop": _tools.RODict({0:52120171}),
        "needItems": _tools.ROList([[30000271, 50], [30000272, 50]]),
        "needCoins": _tools.ROList([30000002, 390000])
    }),
    150202: _tools.RODict({
        "ID": 150202,
        "meridian": 15,
        "acupoint": 2,
        "level": 2,
        "prop": _tools.RODict({0:52120172}),
        "needItems": _tools.ROList([[30000271, 52], [30000272, 52]]),
        "needCoins": _tools.ROList([30000002, 400000])
    }),
    150203: _tools.RODict({
        "ID": 150203,
        "meridian": 15,
        "acupoint": 2,
        "level": 3,
        "prop": _tools.RODict({0:52120173}),
        "needItems": _tools.ROList([[30000271, 54], [30000272, 54]]),
        "needCoins": _tools.ROList([30000002, 410000])
    }),
    150204: _tools.RODict({
        "ID": 150204,
        "meridian": 15,
        "acupoint": 2,
        "level": 4,
        "prop": _tools.RODict({0:52120174}),
        "needItems": _tools.ROList([[30000271, 56], [30000272, 56]]),
        "needCoins": _tools.ROList([30000002, 420000])
    }),
    150205: _tools.RODict({
        "ID": 150205,
        "meridian": 15,
        "acupoint": 2,
        "level": 5,
        "prop": _tools.RODict({0:52120175}),
        "needItems": _tools.ROList([[30000271, 58], [30000272, 58]]),
        "needCoins": _tools.ROList([30000002, 430000])
    }),
    150301: _tools.RODict({
        "ID": 150301,
        "meridian": 15,
        "acupoint": 3,
        "level": 1,
        "prop": _tools.RODict({1001:52120371,1002:52120371,1003:52120271}),
        "needItems": _tools.ROList([[30000271, 50], [30000272, 50]]),
        "needCoins": _tools.ROList([30000002, 390000])
    }),
    150302: _tools.RODict({
        "ID": 150302,
        "meridian": 15,
        "acupoint": 3,
        "level": 2,
        "prop": _tools.RODict({1001:52120372,1002:52120372,1003:52120272}),
        "needItems": _tools.ROList([[30000271, 52], [30000272, 52]]),
        "needCoins": _tools.ROList([30000002, 400000])
    }),
    150303: _tools.RODict({
        "ID": 150303,
        "meridian": 15,
        "acupoint": 3,
        "level": 3,
        "prop": _tools.RODict({1001:52120373,1002:52120373,1003:52120273}),
        "needItems": _tools.ROList([[30000271, 54], [30000272, 54]]),
        "needCoins": _tools.ROList([30000002, 410000])
    }),
    150304: _tools.RODict({
        "ID": 150304,
        "meridian": 15,
        "acupoint": 3,
        "level": 4,
        "prop": _tools.RODict({1001:52120374,1002:52120374,1003:52120274}),
        "needItems": _tools.ROList([[30000271, 56], [30000272, 56]]),
        "needCoins": _tools.ROList([30000002, 420000])
    }),
    150305: _tools.RODict({
        "ID": 150305,
        "meridian": 15,
        "acupoint": 3,
        "level": 5,
        "prop": _tools.RODict({1001:52120375,1002:52120375,1003:52120275}),
        "needItems": _tools.ROList([[30000271, 58], [30000272, 58]]),
        "needCoins": _tools.ROList([30000002, 430000])
    }),
    150401: _tools.RODict({
        "ID": 150401,
        "meridian": 15,
        "acupoint": 4,
        "level": 1,
        "prop": _tools.RODict({1001:52120571,1002:52120571,1003:52120471}),
        "needItems": _tools.ROList([[30000271, 50], [30000272, 50]]),
        "needCoins": _tools.ROList([30000002, 390000])
    }),
    150402: _tools.RODict({
        "ID": 150402,
        "meridian": 15,
        "acupoint": 4,
        "level": 2,
        "prop": _tools.RODict({1001:52120572,1002:52120572,1003:52120472}),
        "needItems": _tools.ROList([[30000271, 52], [30000272, 52]]),
        "needCoins": _tools.ROList([30000002, 400000])
    }),
    150403: _tools.RODict({
        "ID": 150403,
        "meridian": 15,
        "acupoint": 4,
        "level": 3,
        "prop": _tools.RODict({1001:52120573,1002:52120573,1003:52120473}),
        "needItems": _tools.ROList([[30000271, 54], [30000272, 54]]),
        "needCoins": _tools.ROList([30000002, 410000])
    }),
    150404: _tools.RODict({
        "ID": 150404,
        "meridian": 15,
        "acupoint": 4,
        "level": 4,
        "prop": _tools.RODict({1001:52120574,1002:52120574,1003:52120474}),
        "needItems": _tools.ROList([[30000271, 56], [30000272, 56]]),
        "needCoins": _tools.ROList([30000002, 420000])
    }),
    150405: _tools.RODict({
        "ID": 150405,
        "meridian": 15,
        "acupoint": 4,
        "level": 5,
        "prop": _tools.RODict({1001:52120575,1002:52120575,1003:52120475}),
        "needItems": _tools.ROList([[30000271, 58], [30000272, 58]]),
        "needCoins": _tools.ROList([30000002, 430000])
    }),
    150501: _tools.RODict({
        "ID": 150501,
        "meridian": 15,
        "acupoint": 5,
        "level": 1,
        "prop": _tools.RODict({0:52120671}),
        "needItems": _tools.ROList([[30000271, 50], [30000272, 50]]),
        "needCoins": _tools.ROList([30000002, 390000])
    }),
    150502: _tools.RODict({
        "ID": 150502,
        "meridian": 15,
        "acupoint": 5,
        "level": 2,
        "prop": _tools.RODict({0:52120672}),
        "needItems": _tools.ROList([[30000271, 52], [30000272, 52]]),
        "needCoins": _tools.ROList([30000002, 400000])
    }),
    150503: _tools.RODict({
        "ID": 150503,
        "meridian": 15,
        "acupoint": 5,
        "level": 3,
        "prop": _tools.RODict({0:52120673}),
        "needItems": _tools.ROList([[30000271, 54], [30000272, 54]]),
        "needCoins": _tools.ROList([30000002, 410000])
    }),
    150504: _tools.RODict({
        "ID": 150504,
        "meridian": 15,
        "acupoint": 5,
        "level": 4,
        "prop": _tools.RODict({0:52120674}),
        "needItems": _tools.ROList([[30000271, 56], [30000272, 56]]),
        "needCoins": _tools.ROList([30000002, 420000])
    }),
    150505: _tools.RODict({
        "ID": 150505,
        "meridian": 15,
        "acupoint": 5,
        "level": 5,
        "prop": _tools.RODict({0:52120675}),
        "needItems": _tools.ROList([[30000271, 58], [30000272, 58]]),
        "needCoins": _tools.ROList([30000002, 430000])
    }),
    150601: _tools.RODict({
        "ID": 150601,
        "meridian": 15,
        "acupoint": 6,
        "level": 1,
        "prop": _tools.RODict({0:52120771}),
        "needItems": _tools.ROList([[30000271, 50], [30000272, 50]]),
        "needCoins": _tools.ROList([30000002, 390000])
    }),
    150602: _tools.RODict({
        "ID": 150602,
        "meridian": 15,
        "acupoint": 6,
        "level": 2,
        "prop": _tools.RODict({0:52120772}),
        "needItems": _tools.ROList([[30000271, 52], [30000272, 52]]),
        "needCoins": _tools.ROList([30000002, 400000])
    }),
    150603: _tools.RODict({
        "ID": 150603,
        "meridian": 15,
        "acupoint": 6,
        "level": 3,
        "prop": _tools.RODict({0:52120773}),
        "needItems": _tools.ROList([[30000271, 54], [30000272, 54]]),
        "needCoins": _tools.ROList([30000002, 410000])
    }),
    150604: _tools.RODict({
        "ID": 150604,
        "meridian": 15,
        "acupoint": 6,
        "level": 4,
        "prop": _tools.RODict({0:52120774}),
        "needItems": _tools.ROList([[30000271, 56], [30000272, 56]]),
        "needCoins": _tools.ROList([30000002, 420000])
    }),
    150605: _tools.RODict({
        "ID": 150605,
        "meridian": 15,
        "acupoint": 6,
        "level": 5,
        "prop": _tools.RODict({0:52120775}),
        "needItems": _tools.ROList([[30000271, 58], [30000272, 58]]),
        "needCoins": _tools.ROList([30000002, 430000])
    }),
    150701: _tools.RODict({
        "ID": 150701,
        "meridian": 15,
        "acupoint": 7,
        "level": 1,
        "prop": _tools.RODict({0:52120871}),
        "needItems": _tools.ROList([[30000271, 50], [30000272, 50]]),
        "needCoins": _tools.ROList([30000002, 390000])
    }),
    150702: _tools.RODict({
        "ID": 150702,
        "meridian": 15,
        "acupoint": 7,
        "level": 2,
        "prop": _tools.RODict({0:52120872}),
        "needItems": _tools.ROList([[30000271, 52], [30000272, 52]]),
        "needCoins": _tools.ROList([30000002, 400000])
    }),
    150703: _tools.RODict({
        "ID": 150703,
        "meridian": 15,
        "acupoint": 7,
        "level": 3,
        "prop": _tools.RODict({0:52120873}),
        "needItems": _tools.ROList([[30000271, 54], [30000272, 54]]),
        "needCoins": _tools.ROList([30000002, 410000])
    }),
    150704: _tools.RODict({
        "ID": 150704,
        "meridian": 15,
        "acupoint": 7,
        "level": 4,
        "prop": _tools.RODict({0:52120874}),
        "needItems": _tools.ROList([[30000271, 56], [30000272, 56]]),
        "needCoins": _tools.ROList([30000002, 420000])
    }),
    150705: _tools.RODict({
        "ID": 150705,
        "meridian": 15,
        "acupoint": 7,
        "level": 5,
        "prop": _tools.RODict({0:52120875}),
        "needItems": _tools.ROList([[30000271, 58], [30000272, 58]]),
        "needCoins": _tools.ROList([30000002, 430000])
    }),
    150801: _tools.RODict({
        "ID": 150801,
        "meridian": 15,
        "acupoint": 8,
        "level": 1,
        "prop": _tools.RODict({0:52120971}),
        "needItems": _tools.ROList([[30000271, 50], [30000272, 50]]),
        "needCoins": _tools.ROList([30000002, 390000])
    }),
    150802: _tools.RODict({
        "ID": 150802,
        "meridian": 15,
        "acupoint": 8,
        "level": 2,
        "prop": _tools.RODict({0:52120972}),
        "needItems": _tools.ROList([[30000271, 52], [30000272, 52]]),
        "needCoins": _tools.ROList([30000002, 400000])
    }),
    150803: _tools.RODict({
        "ID": 150803,
        "meridian": 15,
        "acupoint": 8,
        "level": 3,
        "prop": _tools.RODict({0:52120973}),
        "needItems": _tools.ROList([[30000271, 54], [30000272, 54]]),
        "needCoins": _tools.ROList([30000002, 410000])
    }),
    150804: _tools.RODict({
        "ID": 150804,
        "meridian": 15,
        "acupoint": 8,
        "level": 4,
        "prop": _tools.RODict({0:52120974}),
        "needItems": _tools.ROList([[30000271, 56], [30000272, 56]]),
        "needCoins": _tools.ROList([30000002, 420000])
    }),
    150805: _tools.RODict({
        "ID": 150805,
        "meridian": 15,
        "acupoint": 8,
        "level": 5,
        "prop": _tools.RODict({0:52120975}),
        "needItems": _tools.ROList([[30000271, 58], [30000272, 58]]),
        "needCoins": _tools.ROList([30000002, 430000])
    }),
    160101: _tools.RODict({
        "ID": 160101,
        "meridian": 16,
        "acupoint": 1,
        "level": 1,
        "prop": _tools.RODict({0:52120076}),
        "needItems": _tools.ROList([[30000275, 10], [30000276, 10]]),
        "needCoins": _tools.ROList([30000002, 440000])
    }),
    160102: _tools.RODict({
        "ID": 160102,
        "meridian": 16,
        "acupoint": 1,
        "level": 2,
        "prop": _tools.RODict({0:52120077}),
        "needItems": _tools.ROList([[30000275, 12], [30000276, 12]]),
        "needCoins": _tools.ROList([30000002, 450000])
    }),
    160103: _tools.RODict({
        "ID": 160103,
        "meridian": 16,
        "acupoint": 1,
        "level": 3,
        "prop": _tools.RODict({0:52120078}),
        "needItems": _tools.ROList([[30000275, 14], [30000276, 14]]),
        "needCoins": _tools.ROList([30000002, 460000])
    }),
    160104: _tools.RODict({
        "ID": 160104,
        "meridian": 16,
        "acupoint": 1,
        "level": 4,
        "prop": _tools.RODict({0:52120079}),
        "needItems": _tools.ROList([[30000275, 16], [30000276, 16]]),
        "needCoins": _tools.ROList([30000002, 470000])
    }),
    160105: _tools.RODict({
        "ID": 160105,
        "meridian": 16,
        "acupoint": 1,
        "level": 5,
        "prop": _tools.RODict({0:52120080}),
        "needItems": _tools.ROList([[30000275, 18], [30000276, 18]]),
        "needCoins": _tools.ROList([30000002, 480000])
    }),
    160201: _tools.RODict({
        "ID": 160201,
        "meridian": 16,
        "acupoint": 2,
        "level": 1,
        "prop": _tools.RODict({0:52120176}),
        "needItems": _tools.ROList([[30000275, 10], [30000276, 10]]),
        "needCoins": _tools.ROList([30000002, 440000])
    }),
    160202: _tools.RODict({
        "ID": 160202,
        "meridian": 16,
        "acupoint": 2,
        "level": 2,
        "prop": _tools.RODict({0:52120177}),
        "needItems": _tools.ROList([[30000275, 12], [30000276, 12]]),
        "needCoins": _tools.ROList([30000002, 450000])
    }),
    160203: _tools.RODict({
        "ID": 160203,
        "meridian": 16,
        "acupoint": 2,
        "level": 3,
        "prop": _tools.RODict({0:52120178}),
        "needItems": _tools.ROList([[30000275, 14], [30000276, 14]]),
        "needCoins": _tools.ROList([30000002, 460000])
    }),
    160204: _tools.RODict({
        "ID": 160204,
        "meridian": 16,
        "acupoint": 2,
        "level": 4,
        "prop": _tools.RODict({0:52120179}),
        "needItems": _tools.ROList([[30000275, 16], [30000276, 16]]),
        "needCoins": _tools.ROList([30000002, 470000])
    }),
    160205: _tools.RODict({
        "ID": 160205,
        "meridian": 16,
        "acupoint": 2,
        "level": 5,
        "prop": _tools.RODict({0:52120180}),
        "needItems": _tools.ROList([[30000275, 18], [30000276, 18]]),
        "needCoins": _tools.ROList([30000002, 480000])
    }),
    160301: _tools.RODict({
        "ID": 160301,
        "meridian": 16,
        "acupoint": 3,
        "level": 1,
        "prop": _tools.RODict({1001:52120376,1002:52120376,1003:52120276}),
        "needItems": _tools.ROList([[30000275, 10], [30000276, 10]]),
        "needCoins": _tools.ROList([30000002, 440000])
    }),
    160302: _tools.RODict({
        "ID": 160302,
        "meridian": 16,
        "acupoint": 3,
        "level": 2,
        "prop": _tools.RODict({1001:52120377,1002:52120377,1003:52120277}),
        "needItems": _tools.ROList([[30000275, 12], [30000276, 12]]),
        "needCoins": _tools.ROList([30000002, 450000])
    }),
    160303: _tools.RODict({
        "ID": 160303,
        "meridian": 16,
        "acupoint": 3,
        "level": 3,
        "prop": _tools.RODict({1001:52120378,1002:52120378,1003:52120278}),
        "needItems": _tools.ROList([[30000275, 14], [30000276, 14]]),
        "needCoins": _tools.ROList([30000002, 460000])
    }),
    160304: _tools.RODict({
        "ID": 160304,
        "meridian": 16,
        "acupoint": 3,
        "level": 4,
        "prop": _tools.RODict({1001:52120379,1002:52120379,1003:52120279}),
        "needItems": _tools.ROList([[30000275, 16], [30000276, 16]]),
        "needCoins": _tools.ROList([30000002, 470000])
    }),
    160305: _tools.RODict({
        "ID": 160305,
        "meridian": 16,
        "acupoint": 3,
        "level": 5,
        "prop": _tools.RODict({1001:52120380,1002:52120380,1003:52120280}),
        "needItems": _tools.ROList([[30000275, 18], [30000276, 18]]),
        "needCoins": _tools.ROList([30000002, 480000])
    }),
    160401: _tools.RODict({
        "ID": 160401,
        "meridian": 16,
        "acupoint": 4,
        "level": 1,
        "prop": _tools.RODict({1001:52120576,1002:52120576,1003:52120476}),
        "needItems": _tools.ROList([[30000275, 10], [30000276, 10]]),
        "needCoins": _tools.ROList([30000002, 440000])
    }),
    160402: _tools.RODict({
        "ID": 160402,
        "meridian": 16,
        "acupoint": 4,
        "level": 2,
        "prop": _tools.RODict({1001:52120577,1002:52120577,1003:52120477}),
        "needItems": _tools.ROList([[30000275, 12], [30000276, 12]]),
        "needCoins": _tools.ROList([30000002, 450000])
    }),
    160403: _tools.RODict({
        "ID": 160403,
        "meridian": 16,
        "acupoint": 4,
        "level": 3,
        "prop": _tools.RODict({1001:52120578,1002:52120578,1003:52120478}),
        "needItems": _tools.ROList([[30000275, 14], [30000276, 14]]),
        "needCoins": _tools.ROList([30000002, 460000])
    }),
    160404: _tools.RODict({
        "ID": 160404,
        "meridian": 16,
        "acupoint": 4,
        "level": 4,
        "prop": _tools.RODict({1001:52120579,1002:52120579,1003:52120479}),
        "needItems": _tools.ROList([[30000275, 16], [30000276, 16]]),
        "needCoins": _tools.ROList([30000002, 470000])
    }),
    160405: _tools.RODict({
        "ID": 160405,
        "meridian": 16,
        "acupoint": 4,
        "level": 5,
        "prop": _tools.RODict({1001:52120580,1002:52120580,1003:52120480}),
        "needItems": _tools.ROList([[30000275, 18], [30000276, 18]]),
        "needCoins": _tools.ROList([30000002, 480000])
    }),
    160501: _tools.RODict({
        "ID": 160501,
        "meridian": 16,
        "acupoint": 5,
        "level": 1,
        "prop": _tools.RODict({0:52120676}),
        "needItems": _tools.ROList([[30000275, 10], [30000276, 10]]),
        "needCoins": _tools.ROList([30000002, 440000])
    }),
    160502: _tools.RODict({
        "ID": 160502,
        "meridian": 16,
        "acupoint": 5,
        "level": 2,
        "prop": _tools.RODict({0:52120677}),
        "needItems": _tools.ROList([[30000275, 12], [30000276, 12]]),
        "needCoins": _tools.ROList([30000002, 450000])
    }),
    160503: _tools.RODict({
        "ID": 160503,
        "meridian": 16,
        "acupoint": 5,
        "level": 3,
        "prop": _tools.RODict({0:52120678}),
        "needItems": _tools.ROList([[30000275, 14], [30000276, 14]]),
        "needCoins": _tools.ROList([30000002, 460000])
    }),
    160504: _tools.RODict({
        "ID": 160504,
        "meridian": 16,
        "acupoint": 5,
        "level": 4,
        "prop": _tools.RODict({0:52120679}),
        "needItems": _tools.ROList([[30000275, 16], [30000276, 16]]),
        "needCoins": _tools.ROList([30000002, 470000])
    }),
    160505: _tools.RODict({
        "ID": 160505,
        "meridian": 16,
        "acupoint": 5,
        "level": 5,
        "prop": _tools.RODict({0:52120680}),
        "needItems": _tools.ROList([[30000275, 18], [30000276, 18]]),
        "needCoins": _tools.ROList([30000002, 480000])
    }),
    160601: _tools.RODict({
        "ID": 160601,
        "meridian": 16,
        "acupoint": 6,
        "level": 1,
        "prop": _tools.RODict({0:52120776}),
        "needItems": _tools.ROList([[30000275, 10], [30000276, 10]]),
        "needCoins": _tools.ROList([30000002, 440000])
    }),
    160602: _tools.RODict({
        "ID": 160602,
        "meridian": 16,
        "acupoint": 6,
        "level": 2,
        "prop": _tools.RODict({0:52120777}),
        "needItems": _tools.ROList([[30000275, 12], [30000276, 12]]),
        "needCoins": _tools.ROList([30000002, 450000])
    }),
    160603: _tools.RODict({
        "ID": 160603,
        "meridian": 16,
        "acupoint": 6,
        "level": 3,
        "prop": _tools.RODict({0:52120778}),
        "needItems": _tools.ROList([[30000275, 14], [30000276, 14]]),
        "needCoins": _tools.ROList([30000002, 460000])
    }),
    160604: _tools.RODict({
        "ID": 160604,
        "meridian": 16,
        "acupoint": 6,
        "level": 4,
        "prop": _tools.RODict({0:52120779}),
        "needItems": _tools.ROList([[30000275, 16], [30000276, 16]]),
        "needCoins": _tools.ROList([30000002, 470000])
    }),
    160605: _tools.RODict({
        "ID": 160605,
        "meridian": 16,
        "acupoint": 6,
        "level": 5,
        "prop": _tools.RODict({0:52120780}),
        "needItems": _tools.ROList([[30000275, 18], [30000276, 18]]),
        "needCoins": _tools.ROList([30000002, 480000])
    }),
    160701: _tools.RODict({
        "ID": 160701,
        "meridian": 16,
        "acupoint": 7,
        "level": 1,
        "prop": _tools.RODict({0:52120876}),
        "needItems": _tools.ROList([[30000275, 10], [30000276, 10]]),
        "needCoins": _tools.ROList([30000002, 440000])
    }),
    160702: _tools.RODict({
        "ID": 160702,
        "meridian": 16,
        "acupoint": 7,
        "level": 2,
        "prop": _tools.RODict({0:52120877}),
        "needItems": _tools.ROList([[30000275, 12], [30000276, 12]]),
        "needCoins": _tools.ROList([30000002, 450000])
    }),
    160703: _tools.RODict({
        "ID": 160703,
        "meridian": 16,
        "acupoint": 7,
        "level": 3,
        "prop": _tools.RODict({0:52120878}),
        "needItems": _tools.ROList([[30000275, 14], [30000276, 14]]),
        "needCoins": _tools.ROList([30000002, 460000])
    }),
    160704: _tools.RODict({
        "ID": 160704,
        "meridian": 16,
        "acupoint": 7,
        "level": 4,
        "prop": _tools.RODict({0:52120879}),
        "needItems": _tools.ROList([[30000275, 16], [30000276, 16]]),
        "needCoins": _tools.ROList([30000002, 470000])
    }),
    160705: _tools.RODict({
        "ID": 160705,
        "meridian": 16,
        "acupoint": 7,
        "level": 5,
        "prop": _tools.RODict({0:52120880}),
        "needItems": _tools.ROList([[30000275, 18], [30000276, 18]]),
        "needCoins": _tools.ROList([30000002, 480000])
    }),
    160801: _tools.RODict({
        "ID": 160801,
        "meridian": 16,
        "acupoint": 8,
        "level": 1,
        "prop": _tools.RODict({0:52120976}),
        "needItems": _tools.ROList([[30000275, 10], [30000276, 10]]),
        "needCoins": _tools.ROList([30000002, 440000])
    }),
    160802: _tools.RODict({
        "ID": 160802,
        "meridian": 16,
        "acupoint": 8,
        "level": 2,
        "prop": _tools.RODict({0:52120977}),
        "needItems": _tools.ROList([[30000275, 12], [30000276, 12]]),
        "needCoins": _tools.ROList([30000002, 450000])
    }),
    160803: _tools.RODict({
        "ID": 160803,
        "meridian": 16,
        "acupoint": 8,
        "level": 3,
        "prop": _tools.RODict({0:52120978}),
        "needItems": _tools.ROList([[30000275, 14], [30000276, 14]]),
        "needCoins": _tools.ROList([30000002, 460000])
    }),
    160804: _tools.RODict({
        "ID": 160804,
        "meridian": 16,
        "acupoint": 8,
        "level": 4,
        "prop": _tools.RODict({0:52120979}),
        "needItems": _tools.ROList([[30000275, 16], [30000276, 16]]),
        "needCoins": _tools.ROList([30000002, 470000])
    }),
    160805: _tools.RODict({
        "ID": 160805,
        "meridian": 16,
        "acupoint": 8,
        "level": 5,
        "prop": _tools.RODict({0:52120980}),
        "needItems": _tools.ROList([[30000275, 18], [30000276, 18]]),
        "needCoins": _tools.ROList([30000002, 480000])
    }),
    170101: _tools.RODict({
        "ID": 170101,
        "meridian": 17,
        "acupoint": 1,
        "level": 1,
        "prop": _tools.RODict({0:52120081}),
        "needItems": _tools.ROList([[30000275, 20], [30000276, 20]]),
        "needCoins": _tools.ROList([30000002, 490000])
    }),
    170102: _tools.RODict({
        "ID": 170102,
        "meridian": 17,
        "acupoint": 1,
        "level": 2,
        "prop": _tools.RODict({0:52120082}),
        "needItems": _tools.ROList([[30000275, 22], [30000276, 22]]),
        "needCoins": _tools.ROList([30000002, 500000])
    }),
    170103: _tools.RODict({
        "ID": 170103,
        "meridian": 17,
        "acupoint": 1,
        "level": 3,
        "prop": _tools.RODict({0:52120083}),
        "needItems": _tools.ROList([[30000275, 24], [30000276, 24]]),
        "needCoins": _tools.ROList([30000002, 510000])
    }),
    170104: _tools.RODict({
        "ID": 170104,
        "meridian": 17,
        "acupoint": 1,
        "level": 4,
        "prop": _tools.RODict({0:52120084}),
        "needItems": _tools.ROList([[30000275, 26], [30000276, 26]]),
        "needCoins": _tools.ROList([30000002, 520000])
    }),
    170105: _tools.RODict({
        "ID": 170105,
        "meridian": 17,
        "acupoint": 1,
        "level": 5,
        "prop": _tools.RODict({0:52120085}),
        "needItems": _tools.ROList([[30000275, 28], [30000276, 28]]),
        "needCoins": _tools.ROList([30000002, 530000])
    }),
    170201: _tools.RODict({
        "ID": 170201,
        "meridian": 17,
        "acupoint": 2,
        "level": 1,
        "prop": _tools.RODict({0:52120181}),
        "needItems": _tools.ROList([[30000275, 20], [30000276, 20]]),
        "needCoins": _tools.ROList([30000002, 490000])
    }),
    170202: _tools.RODict({
        "ID": 170202,
        "meridian": 17,
        "acupoint": 2,
        "level": 2,
        "prop": _tools.RODict({0:52120182}),
        "needItems": _tools.ROList([[30000275, 22], [30000276, 22]]),
        "needCoins": _tools.ROList([30000002, 500000])
    }),
    170203: _tools.RODict({
        "ID": 170203,
        "meridian": 17,
        "acupoint": 2,
        "level": 3,
        "prop": _tools.RODict({0:52120183}),
        "needItems": _tools.ROList([[30000275, 24], [30000276, 24]]),
        "needCoins": _tools.ROList([30000002, 510000])
    }),
    170204: _tools.RODict({
        "ID": 170204,
        "meridian": 17,
        "acupoint": 2,
        "level": 4,
        "prop": _tools.RODict({0:52120184}),
        "needItems": _tools.ROList([[30000275, 26], [30000276, 26]]),
        "needCoins": _tools.ROList([30000002, 520000])
    }),
    170205: _tools.RODict({
        "ID": 170205,
        "meridian": 17,
        "acupoint": 2,
        "level": 5,
        "prop": _tools.RODict({0:52120185}),
        "needItems": _tools.ROList([[30000275, 28], [30000276, 28]]),
        "needCoins": _tools.ROList([30000002, 530000])
    }),
    170301: _tools.RODict({
        "ID": 170301,
        "meridian": 17,
        "acupoint": 3,
        "level": 1,
        "prop": _tools.RODict({1001:52120381,1002:52120381,1003:52120281}),
        "needItems": _tools.ROList([[30000275, 20], [30000276, 20]]),
        "needCoins": _tools.ROList([30000002, 490000])
    }),
    170302: _tools.RODict({
        "ID": 170302,
        "meridian": 17,
        "acupoint": 3,
        "level": 2,
        "prop": _tools.RODict({1001:52120382,1002:52120382,1003:52120282}),
        "needItems": _tools.ROList([[30000275, 22], [30000276, 22]]),
        "needCoins": _tools.ROList([30000002, 500000])
    }),
    170303: _tools.RODict({
        "ID": 170303,
        "meridian": 17,
        "acupoint": 3,
        "level": 3,
        "prop": _tools.RODict({1001:52120383,1002:52120383,1003:52120283}),
        "needItems": _tools.ROList([[30000275, 24], [30000276, 24]]),
        "needCoins": _tools.ROList([30000002, 510000])
    }),
    170304: _tools.RODict({
        "ID": 170304,
        "meridian": 17,
        "acupoint": 3,
        "level": 4,
        "prop": _tools.RODict({1001:52120384,1002:52120384,1003:52120284}),
        "needItems": _tools.ROList([[30000275, 26], [30000276, 26]]),
        "needCoins": _tools.ROList([30000002, 520000])
    }),
    170305: _tools.RODict({
        "ID": 170305,
        "meridian": 17,
        "acupoint": 3,
        "level": 5,
        "prop": _tools.RODict({1001:52120385,1002:52120385,1003:52120285}),
        "needItems": _tools.ROList([[30000275, 28], [30000276, 28]]),
        "needCoins": _tools.ROList([30000002, 530000])
    }),
    170401: _tools.RODict({
        "ID": 170401,
        "meridian": 17,
        "acupoint": 4,
        "level": 1,
        "prop": _tools.RODict({1001:52120581,1002:52120581,1003:52120481}),
        "needItems": _tools.ROList([[30000275, 20], [30000276, 20]]),
        "needCoins": _tools.ROList([30000002, 490000])
    }),
    170402: _tools.RODict({
        "ID": 170402,
        "meridian": 17,
        "acupoint": 4,
        "level": 2,
        "prop": _tools.RODict({1001:52120582,1002:52120582,1003:52120482}),
        "needItems": _tools.ROList([[30000275, 22], [30000276, 22]]),
        "needCoins": _tools.ROList([30000002, 500000])
    }),
    170403: _tools.RODict({
        "ID": 170403,
        "meridian": 17,
        "acupoint": 4,
        "level": 3,
        "prop": _tools.RODict({1001:52120583,1002:52120583,1003:52120483}),
        "needItems": _tools.ROList([[30000275, 24], [30000276, 24]]),
        "needCoins": _tools.ROList([30000002, 510000])
    }),
    170404: _tools.RODict({
        "ID": 170404,
        "meridian": 17,
        "acupoint": 4,
        "level": 4,
        "prop": _tools.RODict({1001:52120584,1002:52120584,1003:52120484}),
        "needItems": _tools.ROList([[30000275, 26], [30000276, 26]]),
        "needCoins": _tools.ROList([30000002, 520000])
    }),
    170405: _tools.RODict({
        "ID": 170405,
        "meridian": 17,
        "acupoint": 4,
        "level": 5,
        "prop": _tools.RODict({1001:52120585,1002:52120585,1003:52120485}),
        "needItems": _tools.ROList([[30000275, 28], [30000276, 28]]),
        "needCoins": _tools.ROList([30000002, 530000])
    }),
    170501: _tools.RODict({
        "ID": 170501,
        "meridian": 17,
        "acupoint": 5,
        "level": 1,
        "prop": _tools.RODict({0:52120681}),
        "needItems": _tools.ROList([[30000275, 20], [30000276, 20]]),
        "needCoins": _tools.ROList([30000002, 490000])
    }),
    170502: _tools.RODict({
        "ID": 170502,
        "meridian": 17,
        "acupoint": 5,
        "level": 2,
        "prop": _tools.RODict({0:52120682}),
        "needItems": _tools.ROList([[30000275, 22], [30000276, 22]]),
        "needCoins": _tools.ROList([30000002, 500000])
    }),
    170503: _tools.RODict({
        "ID": 170503,
        "meridian": 17,
        "acupoint": 5,
        "level": 3,
        "prop": _tools.RODict({0:52120683}),
        "needItems": _tools.ROList([[30000275, 24], [30000276, 24]]),
        "needCoins": _tools.ROList([30000002, 510000])
    }),
    170504: _tools.RODict({
        "ID": 170504,
        "meridian": 17,
        "acupoint": 5,
        "level": 4,
        "prop": _tools.RODict({0:52120684}),
        "needItems": _tools.ROList([[30000275, 26], [30000276, 26]]),
        "needCoins": _tools.ROList([30000002, 520000])
    }),
    170505: _tools.RODict({
        "ID": 170505,
        "meridian": 17,
        "acupoint": 5,
        "level": 5,
        "prop": _tools.RODict({0:52120685}),
        "needItems": _tools.ROList([[30000275, 28], [30000276, 28]]),
        "needCoins": _tools.ROList([30000002, 530000])
    }),
    170601: _tools.RODict({
        "ID": 170601,
        "meridian": 17,
        "acupoint": 6,
        "level": 1,
        "prop": _tools.RODict({0:52120781}),
        "needItems": _tools.ROList([[30000275, 20], [30000276, 20]]),
        "needCoins": _tools.ROList([30000002, 490000])
    }),
    170602: _tools.RODict({
        "ID": 170602,
        "meridian": 17,
        "acupoint": 6,
        "level": 2,
        "prop": _tools.RODict({0:52120782}),
        "needItems": _tools.ROList([[30000275, 22], [30000276, 22]]),
        "needCoins": _tools.ROList([30000002, 500000])
    }),
    170603: _tools.RODict({
        "ID": 170603,
        "meridian": 17,
        "acupoint": 6,
        "level": 3,
        "prop": _tools.RODict({0:52120783}),
        "needItems": _tools.ROList([[30000275, 24], [30000276, 24]]),
        "needCoins": _tools.ROList([30000002, 510000])
    }),
    170604: _tools.RODict({
        "ID": 170604,
        "meridian": 17,
        "acupoint": 6,
        "level": 4,
        "prop": _tools.RODict({0:52120784}),
        "needItems": _tools.ROList([[30000275, 26], [30000276, 26]]),
        "needCoins": _tools.ROList([30000002, 520000])
    }),
    170605: _tools.RODict({
        "ID": 170605,
        "meridian": 17,
        "acupoint": 6,
        "level": 5,
        "prop": _tools.RODict({0:52120785}),
        "needItems": _tools.ROList([[30000275, 28], [30000276, 28]]),
        "needCoins": _tools.ROList([30000002, 530000])
    }),
    170701: _tools.RODict({
        "ID": 170701,
        "meridian": 17,
        "acupoint": 7,
        "level": 1,
        "prop": _tools.RODict({0:52120881}),
        "needItems": _tools.ROList([[30000275, 20], [30000276, 20]]),
        "needCoins": _tools.ROList([30000002, 490000])
    }),
    170702: _tools.RODict({
        "ID": 170702,
        "meridian": 17,
        "acupoint": 7,
        "level": 2,
        "prop": _tools.RODict({0:52120882}),
        "needItems": _tools.ROList([[30000275, 22], [30000276, 22]]),
        "needCoins": _tools.ROList([30000002, 500000])
    }),
    170703: _tools.RODict({
        "ID": 170703,
        "meridian": 17,
        "acupoint": 7,
        "level": 3,
        "prop": _tools.RODict({0:52120883}),
        "needItems": _tools.ROList([[30000275, 24], [30000276, 24]]),
        "needCoins": _tools.ROList([30000002, 510000])
    }),
    170704: _tools.RODict({
        "ID": 170704,
        "meridian": 17,
        "acupoint": 7,
        "level": 4,
        "prop": _tools.RODict({0:52120884}),
        "needItems": _tools.ROList([[30000275, 26], [30000276, 26]]),
        "needCoins": _tools.ROList([30000002, 520000])
    }),
    170705: _tools.RODict({
        "ID": 170705,
        "meridian": 17,
        "acupoint": 7,
        "level": 5,
        "prop": _tools.RODict({0:52120885}),
        "needItems": _tools.ROList([[30000275, 28], [30000276, 28]]),
        "needCoins": _tools.ROList([30000002, 530000])
    }),
    170801: _tools.RODict({
        "ID": 170801,
        "meridian": 17,
        "acupoint": 8,
        "level": 1,
        "prop": _tools.RODict({0:52120981}),
        "needItems": _tools.ROList([[30000275, 20], [30000276, 20]]),
        "needCoins": _tools.ROList([30000002, 490000])
    }),
    170802: _tools.RODict({
        "ID": 170802,
        "meridian": 17,
        "acupoint": 8,
        "level": 2,
        "prop": _tools.RODict({0:52120982}),
        "needItems": _tools.ROList([[30000275, 22], [30000276, 22]]),
        "needCoins": _tools.ROList([30000002, 500000])
    }),
    170803: _tools.RODict({
        "ID": 170803,
        "meridian": 17,
        "acupoint": 8,
        "level": 3,
        "prop": _tools.RODict({0:52120983}),
        "needItems": _tools.ROList([[30000275, 24], [30000276, 24]]),
        "needCoins": _tools.ROList([30000002, 510000])
    }),
    170804: _tools.RODict({
        "ID": 170804,
        "meridian": 17,
        "acupoint": 8,
        "level": 4,
        "prop": _tools.RODict({0:52120984}),
        "needItems": _tools.ROList([[30000275, 26], [30000276, 26]]),
        "needCoins": _tools.ROList([30000002, 520000])
    }),
    170805: _tools.RODict({
        "ID": 170805,
        "meridian": 17,
        "acupoint": 8,
        "level": 5,
        "prop": _tools.RODict({0:52120985}),
        "needItems": _tools.ROList([[30000275, 28], [30000276, 28]]),
        "needCoins": _tools.ROList([30000002, 530000])
    }),
    180101: _tools.RODict({
        "ID": 180101,
        "meridian": 18,
        "acupoint": 1,
        "level": 1,
        "prop": _tools.RODict({0:52120086}),
        "needItems": _tools.ROList([[30000275, 30], [30000276, 30]]),
        "needCoins": _tools.ROList([30000002, 540000])
    }),
    180102: _tools.RODict({
        "ID": 180102,
        "meridian": 18,
        "acupoint": 1,
        "level": 2,
        "prop": _tools.RODict({0:52120087}),
        "needItems": _tools.ROList([[30000275, 32], [30000276, 32]]),
        "needCoins": _tools.ROList([30000002, 550000])
    }),
    180103: _tools.RODict({
        "ID": 180103,
        "meridian": 18,
        "acupoint": 1,
        "level": 3,
        "prop": _tools.RODict({0:52120088}),
        "needItems": _tools.ROList([[30000275, 34], [30000276, 34]]),
        "needCoins": _tools.ROList([30000002, 560000])
    }),
    180104: _tools.RODict({
        "ID": 180104,
        "meridian": 18,
        "acupoint": 1,
        "level": 4,
        "prop": _tools.RODict({0:52120089}),
        "needItems": _tools.ROList([[30000275, 36], [30000276, 36]]),
        "needCoins": _tools.ROList([30000002, 570000])
    }),
    180105: _tools.RODict({
        "ID": 180105,
        "meridian": 18,
        "acupoint": 1,
        "level": 5,
        "prop": _tools.RODict({0:52120090}),
        "needItems": _tools.ROList([[30000275, 38], [30000276, 38]]),
        "needCoins": _tools.ROList([30000002, 580000])
    }),
    180201: _tools.RODict({
        "ID": 180201,
        "meridian": 18,
        "acupoint": 2,
        "level": 1,
        "prop": _tools.RODict({0:52120186}),
        "needItems": _tools.ROList([[30000275, 30], [30000276, 30]]),
        "needCoins": _tools.ROList([30000002, 540000])
    }),
    180202: _tools.RODict({
        "ID": 180202,
        "meridian": 18,
        "acupoint": 2,
        "level": 2,
        "prop": _tools.RODict({0:52120187}),
        "needItems": _tools.ROList([[30000275, 32], [30000276, 32]]),
        "needCoins": _tools.ROList([30000002, 550000])
    }),
    180203: _tools.RODict({
        "ID": 180203,
        "meridian": 18,
        "acupoint": 2,
        "level": 3,
        "prop": _tools.RODict({0:52120188}),
        "needItems": _tools.ROList([[30000275, 34], [30000276, 34]]),
        "needCoins": _tools.ROList([30000002, 560000])
    }),
    180204: _tools.RODict({
        "ID": 180204,
        "meridian": 18,
        "acupoint": 2,
        "level": 4,
        "prop": _tools.RODict({0:52120189}),
        "needItems": _tools.ROList([[30000275, 36], [30000276, 36]]),
        "needCoins": _tools.ROList([30000002, 570000])
    }),
    180205: _tools.RODict({
        "ID": 180205,
        "meridian": 18,
        "acupoint": 2,
        "level": 5,
        "prop": _tools.RODict({0:52120190}),
        "needItems": _tools.ROList([[30000275, 38], [30000276, 38]]),
        "needCoins": _tools.ROList([30000002, 580000])
    }),
    180301: _tools.RODict({
        "ID": 180301,
        "meridian": 18,
        "acupoint": 3,
        "level": 1,
        "prop": _tools.RODict({1001:52120386,1002:52120386,1003:52120286}),
        "needItems": _tools.ROList([[30000275, 30], [30000276, 30]]),
        "needCoins": _tools.ROList([30000002, 540000])
    }),
    180302: _tools.RODict({
        "ID": 180302,
        "meridian": 18,
        "acupoint": 3,
        "level": 2,
        "prop": _tools.RODict({1001:52120387,1002:52120387,1003:52120287}),
        "needItems": _tools.ROList([[30000275, 32], [30000276, 32]]),
        "needCoins": _tools.ROList([30000002, 550000])
    }),
    180303: _tools.RODict({
        "ID": 180303,
        "meridian": 18,
        "acupoint": 3,
        "level": 3,
        "prop": _tools.RODict({1001:52120388,1002:52120388,1003:52120288}),
        "needItems": _tools.ROList([[30000275, 34], [30000276, 34]]),
        "needCoins": _tools.ROList([30000002, 560000])
    }),
    180304: _tools.RODict({
        "ID": 180304,
        "meridian": 18,
        "acupoint": 3,
        "level": 4,
        "prop": _tools.RODict({1001:52120389,1002:52120389,1003:52120289}),
        "needItems": _tools.ROList([[30000275, 36], [30000276, 36]]),
        "needCoins": _tools.ROList([30000002, 570000])
    }),
    180305: _tools.RODict({
        "ID": 180305,
        "meridian": 18,
        "acupoint": 3,
        "level": 5,
        "prop": _tools.RODict({1001:52120390,1002:52120390,1003:52120290}),
        "needItems": _tools.ROList([[30000275, 38], [30000276, 38]]),
        "needCoins": _tools.ROList([30000002, 580000])
    }),
    180401: _tools.RODict({
        "ID": 180401,
        "meridian": 18,
        "acupoint": 4,
        "level": 1,
        "prop": _tools.RODict({1001:52120586,1002:52120586,1003:52120486}),
        "needItems": _tools.ROList([[30000275, 30], [30000276, 30]]),
        "needCoins": _tools.ROList([30000002, 540000])
    }),
    180402: _tools.RODict({
        "ID": 180402,
        "meridian": 18,
        "acupoint": 4,
        "level": 2,
        "prop": _tools.RODict({1001:52120587,1002:52120587,1003:52120487}),
        "needItems": _tools.ROList([[30000275, 32], [30000276, 32]]),
        "needCoins": _tools.ROList([30000002, 550000])
    }),
    180403: _tools.RODict({
        "ID": 180403,
        "meridian": 18,
        "acupoint": 4,
        "level": 3,
        "prop": _tools.RODict({1001:52120588,1002:52120588,1003:52120488}),
        "needItems": _tools.ROList([[30000275, 34], [30000276, 34]]),
        "needCoins": _tools.ROList([30000002, 560000])
    }),
    180404: _tools.RODict({
        "ID": 180404,
        "meridian": 18,
        "acupoint": 4,
        "level": 4,
        "prop": _tools.RODict({1001:52120589,1002:52120589,1003:52120489}),
        "needItems": _tools.ROList([[30000275, 36], [30000276, 36]]),
        "needCoins": _tools.ROList([30000002, 570000])
    }),
    180405: _tools.RODict({
        "ID": 180405,
        "meridian": 18,
        "acupoint": 4,
        "level": 5,
        "prop": _tools.RODict({1001:52120590,1002:52120590,1003:52120490}),
        "needItems": _tools.ROList([[30000275, 38], [30000276, 38]]),
        "needCoins": _tools.ROList([30000002, 580000])
    }),
    180501: _tools.RODict({
        "ID": 180501,
        "meridian": 18,
        "acupoint": 5,
        "level": 1,
        "prop": _tools.RODict({0:52120686}),
        "needItems": _tools.ROList([[30000275, 30], [30000276, 30]]),
        "needCoins": _tools.ROList([30000002, 540000])
    }),
    180502: _tools.RODict({
        "ID": 180502,
        "meridian": 18,
        "acupoint": 5,
        "level": 2,
        "prop": _tools.RODict({0:52120687}),
        "needItems": _tools.ROList([[30000275, 32], [30000276, 32]]),
        "needCoins": _tools.ROList([30000002, 550000])
    }),
    180503: _tools.RODict({
        "ID": 180503,
        "meridian": 18,
        "acupoint": 5,
        "level": 3,
        "prop": _tools.RODict({0:52120688}),
        "needItems": _tools.ROList([[30000275, 34], [30000276, 34]]),
        "needCoins": _tools.ROList([30000002, 560000])
    }),
    180504: _tools.RODict({
        "ID": 180504,
        "meridian": 18,
        "acupoint": 5,
        "level": 4,
        "prop": _tools.RODict({0:52120689}),
        "needItems": _tools.ROList([[30000275, 36], [30000276, 36]]),
        "needCoins": _tools.ROList([30000002, 570000])
    }),
    180505: _tools.RODict({
        "ID": 180505,
        "meridian": 18,
        "acupoint": 5,
        "level": 5,
        "prop": _tools.RODict({0:52120690}),
        "needItems": _tools.ROList([[30000275, 38], [30000276, 38]]),
        "needCoins": _tools.ROList([30000002, 580000])
    }),
    180601: _tools.RODict({
        "ID": 180601,
        "meridian": 18,
        "acupoint": 6,
        "level": 1,
        "prop": _tools.RODict({0:52120786}),
        "needItems": _tools.ROList([[30000275, 30], [30000276, 30]]),
        "needCoins": _tools.ROList([30000002, 540000])
    }),
    180602: _tools.RODict({
        "ID": 180602,
        "meridian": 18,
        "acupoint": 6,
        "level": 2,
        "prop": _tools.RODict({0:52120787}),
        "needItems": _tools.ROList([[30000275, 32], [30000276, 32]]),
        "needCoins": _tools.ROList([30000002, 550000])
    }),
    180603: _tools.RODict({
        "ID": 180603,
        "meridian": 18,
        "acupoint": 6,
        "level": 3,
        "prop": _tools.RODict({0:52120788}),
        "needItems": _tools.ROList([[30000275, 34], [30000276, 34]]),
        "needCoins": _tools.ROList([30000002, 560000])
    }),
    180604: _tools.RODict({
        "ID": 180604,
        "meridian": 18,
        "acupoint": 6,
        "level": 4,
        "prop": _tools.RODict({0:52120789}),
        "needItems": _tools.ROList([[30000275, 36], [30000276, 36]]),
        "needCoins": _tools.ROList([30000002, 570000])
    }),
    180605: _tools.RODict({
        "ID": 180605,
        "meridian": 18,
        "acupoint": 6,
        "level": 5,
        "prop": _tools.RODict({0:52120790}),
        "needItems": _tools.ROList([[30000275, 38], [30000276, 38]]),
        "needCoins": _tools.ROList([30000002, 580000])
    }),
    180701: _tools.RODict({
        "ID": 180701,
        "meridian": 18,
        "acupoint": 7,
        "level": 1,
        "prop": _tools.RODict({0:52120886}),
        "needItems": _tools.ROList([[30000275, 30], [30000276, 30]]),
        "needCoins": _tools.ROList([30000002, 540000])
    }),
    180702: _tools.RODict({
        "ID": 180702,
        "meridian": 18,
        "acupoint": 7,
        "level": 2,
        "prop": _tools.RODict({0:52120887}),
        "needItems": _tools.ROList([[30000275, 32], [30000276, 32]]),
        "needCoins": _tools.ROList([30000002, 550000])
    }),
    180703: _tools.RODict({
        "ID": 180703,
        "meridian": 18,
        "acupoint": 7,
        "level": 3,
        "prop": _tools.RODict({0:52120888}),
        "needItems": _tools.ROList([[30000275, 34], [30000276, 34]]),
        "needCoins": _tools.ROList([30000002, 560000])
    }),
    180704: _tools.RODict({
        "ID": 180704,
        "meridian": 18,
        "acupoint": 7,
        "level": 4,
        "prop": _tools.RODict({0:52120889}),
        "needItems": _tools.ROList([[30000275, 36], [30000276, 36]]),
        "needCoins": _tools.ROList([30000002, 570000])
    }),
    180705: _tools.RODict({
        "ID": 180705,
        "meridian": 18,
        "acupoint": 7,
        "level": 5,
        "prop": _tools.RODict({0:52120890}),
        "needItems": _tools.ROList([[30000275, 38], [30000276, 38]]),
        "needCoins": _tools.ROList([30000002, 580000])
    }),
    180801: _tools.RODict({
        "ID": 180801,
        "meridian": 18,
        "acupoint": 8,
        "level": 1,
        "prop": _tools.RODict({0:52120986}),
        "needItems": _tools.ROList([[30000275, 30], [30000276, 30]]),
        "needCoins": _tools.ROList([30000002, 540000])
    }),
    180802: _tools.RODict({
        "ID": 180802,
        "meridian": 18,
        "acupoint": 8,
        "level": 2,
        "prop": _tools.RODict({0:52120987}),
        "needItems": _tools.ROList([[30000275, 32], [30000276, 32]]),
        "needCoins": _tools.ROList([30000002, 550000])
    }),
    180803: _tools.RODict({
        "ID": 180803,
        "meridian": 18,
        "acupoint": 8,
        "level": 3,
        "prop": _tools.RODict({0:52120988}),
        "needItems": _tools.ROList([[30000275, 34], [30000276, 34]]),
        "needCoins": _tools.ROList([30000002, 560000])
    }),
    180804: _tools.RODict({
        "ID": 180804,
        "meridian": 18,
        "acupoint": 8,
        "level": 4,
        "prop": _tools.RODict({0:52120989}),
        "needItems": _tools.ROList([[30000275, 36], [30000276, 36]]),
        "needCoins": _tools.ROList([30000002, 570000])
    }),
    180805: _tools.RODict({
        "ID": 180805,
        "meridian": 18,
        "acupoint": 8,
        "level": 5,
        "prop": _tools.RODict({0:52120990}),
        "needItems": _tools.ROList([[30000275, 38], [30000276, 38]]),
        "needCoins": _tools.ROList([30000002, 580000])
    }),
    190101: _tools.RODict({
        "ID": 190101,
        "meridian": 19,
        "acupoint": 1,
        "level": 1,
        "prop": _tools.RODict({0:52120091}),
        "needItems": _tools.ROList([[30000275, 40], [30000276, 40]]),
        "needCoins": _tools.ROList([30000002, 590000])
    }),
    190102: _tools.RODict({
        "ID": 190102,
        "meridian": 19,
        "acupoint": 1,
        "level": 2,
        "prop": _tools.RODict({0:52120092}),
        "needItems": _tools.ROList([[30000275, 42], [30000276, 42]]),
        "needCoins": _tools.ROList([30000002, 600000])
    }),
    190103: _tools.RODict({
        "ID": 190103,
        "meridian": 19,
        "acupoint": 1,
        "level": 3,
        "prop": _tools.RODict({0:52120093}),
        "needItems": _tools.ROList([[30000275, 44], [30000276, 44]]),
        "needCoins": _tools.ROList([30000002, 610000])
    }),
    190104: _tools.RODict({
        "ID": 190104,
        "meridian": 19,
        "acupoint": 1,
        "level": 4,
        "prop": _tools.RODict({0:52120094}),
        "needItems": _tools.ROList([[30000275, 46], [30000276, 46]]),
        "needCoins": _tools.ROList([30000002, 620000])
    }),
    190105: _tools.RODict({
        "ID": 190105,
        "meridian": 19,
        "acupoint": 1,
        "level": 5,
        "prop": _tools.RODict({0:52120095}),
        "needItems": _tools.ROList([[30000275, 48], [30000276, 48]]),
        "needCoins": _tools.ROList([30000002, 630000])
    }),
    190201: _tools.RODict({
        "ID": 190201,
        "meridian": 19,
        "acupoint": 2,
        "level": 1,
        "prop": _tools.RODict({0:52120191}),
        "needItems": _tools.ROList([[30000275, 40], [30000276, 40]]),
        "needCoins": _tools.ROList([30000002, 590000])
    }),
    190202: _tools.RODict({
        "ID": 190202,
        "meridian": 19,
        "acupoint": 2,
        "level": 2,
        "prop": _tools.RODict({0:52120192}),
        "needItems": _tools.ROList([[30000275, 42], [30000276, 42]]),
        "needCoins": _tools.ROList([30000002, 600000])
    }),
    190203: _tools.RODict({
        "ID": 190203,
        "meridian": 19,
        "acupoint": 2,
        "level": 3,
        "prop": _tools.RODict({0:52120193}),
        "needItems": _tools.ROList([[30000275, 44], [30000276, 44]]),
        "needCoins": _tools.ROList([30000002, 610000])
    }),
    190204: _tools.RODict({
        "ID": 190204,
        "meridian": 19,
        "acupoint": 2,
        "level": 4,
        "prop": _tools.RODict({0:52120194}),
        "needItems": _tools.ROList([[30000275, 46], [30000276, 46]]),
        "needCoins": _tools.ROList([30000002, 620000])
    }),
    190205: _tools.RODict({
        "ID": 190205,
        "meridian": 19,
        "acupoint": 2,
        "level": 5,
        "prop": _tools.RODict({0:52120195}),
        "needItems": _tools.ROList([[30000275, 48], [30000276, 48]]),
        "needCoins": _tools.ROList([30000002, 630000])
    }),
    190301: _tools.RODict({
        "ID": 190301,
        "meridian": 19,
        "acupoint": 3,
        "level": 1,
        "prop": _tools.RODict({1001:52120391,1002:52120391,1003:52120291}),
        "needItems": _tools.ROList([[30000275, 40], [30000276, 40]]),
        "needCoins": _tools.ROList([30000002, 590000])
    }),
    190302: _tools.RODict({
        "ID": 190302,
        "meridian": 19,
        "acupoint": 3,
        "level": 2,
        "prop": _tools.RODict({1001:52120392,1002:52120392,1003:52120292}),
        "needItems": _tools.ROList([[30000275, 42], [30000276, 42]]),
        "needCoins": _tools.ROList([30000002, 600000])
    }),
    190303: _tools.RODict({
        "ID": 190303,
        "meridian": 19,
        "acupoint": 3,
        "level": 3,
        "prop": _tools.RODict({1001:52120393,1002:52120393,1003:52120293}),
        "needItems": _tools.ROList([[30000275, 44], [30000276, 44]]),
        "needCoins": _tools.ROList([30000002, 610000])
    }),
    190304: _tools.RODict({
        "ID": 190304,
        "meridian": 19,
        "acupoint": 3,
        "level": 4,
        "prop": _tools.RODict({1001:52120394,1002:52120394,1003:52120294}),
        "needItems": _tools.ROList([[30000275, 46], [30000276, 46]]),
        "needCoins": _tools.ROList([30000002, 620000])
    }),
    190305: _tools.RODict({
        "ID": 190305,
        "meridian": 19,
        "acupoint": 3,
        "level": 5,
        "prop": _tools.RODict({1001:52120395,1002:52120395,1003:52120295}),
        "needItems": _tools.ROList([[30000275, 48], [30000276, 48]]),
        "needCoins": _tools.ROList([30000002, 630000])
    }),
    190401: _tools.RODict({
        "ID": 190401,
        "meridian": 19,
        "acupoint": 4,
        "level": 1,
        "prop": _tools.RODict({1001:52120591,1002:52120591,1003:52120491}),
        "needItems": _tools.ROList([[30000275, 40], [30000276, 40]]),
        "needCoins": _tools.ROList([30000002, 590000])
    }),
    190402: _tools.RODict({
        "ID": 190402,
        "meridian": 19,
        "acupoint": 4,
        "level": 2,
        "prop": _tools.RODict({1001:52120592,1002:52120592,1003:52120492}),
        "needItems": _tools.ROList([[30000275, 42], [30000276, 42]]),
        "needCoins": _tools.ROList([30000002, 600000])
    }),
    190403: _tools.RODict({
        "ID": 190403,
        "meridian": 19,
        "acupoint": 4,
        "level": 3,
        "prop": _tools.RODict({1001:52120593,1002:52120593,1003:52120493}),
        "needItems": _tools.ROList([[30000275, 44], [30000276, 44]]),
        "needCoins": _tools.ROList([30000002, 610000])
    }),
    190404: _tools.RODict({
        "ID": 190404,
        "meridian": 19,
        "acupoint": 4,
        "level": 4,
        "prop": _tools.RODict({1001:52120594,1002:52120594,1003:52120494}),
        "needItems": _tools.ROList([[30000275, 46], [30000276, 46]]),
        "needCoins": _tools.ROList([30000002, 620000])
    }),
    190405: _tools.RODict({
        "ID": 190405,
        "meridian": 19,
        "acupoint": 4,
        "level": 5,
        "prop": _tools.RODict({1001:52120595,1002:52120595,1003:52120495}),
        "needItems": _tools.ROList([[30000275, 48], [30000276, 48]]),
        "needCoins": _tools.ROList([30000002, 630000])
    }),
    190501: _tools.RODict({
        "ID": 190501,
        "meridian": 19,
        "acupoint": 5,
        "level": 1,
        "prop": _tools.RODict({0:52120691}),
        "needItems": _tools.ROList([[30000275, 40], [30000276, 40]]),
        "needCoins": _tools.ROList([30000002, 590000])
    }),
    190502: _tools.RODict({
        "ID": 190502,
        "meridian": 19,
        "acupoint": 5,
        "level": 2,
        "prop": _tools.RODict({0:52120692}),
        "needItems": _tools.ROList([[30000275, 42], [30000276, 42]]),
        "needCoins": _tools.ROList([30000002, 600000])
    }),
    190503: _tools.RODict({
        "ID": 190503,
        "meridian": 19,
        "acupoint": 5,
        "level": 3,
        "prop": _tools.RODict({0:52120693}),
        "needItems": _tools.ROList([[30000275, 44], [30000276, 44]]),
        "needCoins": _tools.ROList([30000002, 610000])
    }),
    190504: _tools.RODict({
        "ID": 190504,
        "meridian": 19,
        "acupoint": 5,
        "level": 4,
        "prop": _tools.RODict({0:52120694}),
        "needItems": _tools.ROList([[30000275, 46], [30000276, 46]]),
        "needCoins": _tools.ROList([30000002, 620000])
    }),
    190505: _tools.RODict({
        "ID": 190505,
        "meridian": 19,
        "acupoint": 5,
        "level": 5,
        "prop": _tools.RODict({0:52120695}),
        "needItems": _tools.ROList([[30000275, 48], [30000276, 48]]),
        "needCoins": _tools.ROList([30000002, 630000])
    }),
    190601: _tools.RODict({
        "ID": 190601,
        "meridian": 19,
        "acupoint": 6,
        "level": 1,
        "prop": _tools.RODict({0:52120791}),
        "needItems": _tools.ROList([[30000275, 40], [30000276, 40]]),
        "needCoins": _tools.ROList([30000002, 590000])
    }),
    190602: _tools.RODict({
        "ID": 190602,
        "meridian": 19,
        "acupoint": 6,
        "level": 2,
        "prop": _tools.RODict({0:52120792}),
        "needItems": _tools.ROList([[30000275, 42], [30000276, 42]]),
        "needCoins": _tools.ROList([30000002, 600000])
    }),
    190603: _tools.RODict({
        "ID": 190603,
        "meridian": 19,
        "acupoint": 6,
        "level": 3,
        "prop": _tools.RODict({0:52120793}),
        "needItems": _tools.ROList([[30000275, 44], [30000276, 44]]),
        "needCoins": _tools.ROList([30000002, 610000])
    }),
    190604: _tools.RODict({
        "ID": 190604,
        "meridian": 19,
        "acupoint": 6,
        "level": 4,
        "prop": _tools.RODict({0:52120794}),
        "needItems": _tools.ROList([[30000275, 46], [30000276, 46]]),
        "needCoins": _tools.ROList([30000002, 620000])
    }),
    190605: _tools.RODict({
        "ID": 190605,
        "meridian": 19,
        "acupoint": 6,
        "level": 5,
        "prop": _tools.RODict({0:52120795}),
        "needItems": _tools.ROList([[30000275, 48], [30000276, 48]]),
        "needCoins": _tools.ROList([30000002, 630000])
    }),
    190701: _tools.RODict({
        "ID": 190701,
        "meridian": 19,
        "acupoint": 7,
        "level": 1,
        "prop": _tools.RODict({0:52120891}),
        "needItems": _tools.ROList([[30000275, 40], [30000276, 40]]),
        "needCoins": _tools.ROList([30000002, 590000])
    }),
    190702: _tools.RODict({
        "ID": 190702,
        "meridian": 19,
        "acupoint": 7,
        "level": 2,
        "prop": _tools.RODict({0:52120892}),
        "needItems": _tools.ROList([[30000275, 42], [30000276, 42]]),
        "needCoins": _tools.ROList([30000002, 600000])
    }),
    190703: _tools.RODict({
        "ID": 190703,
        "meridian": 19,
        "acupoint": 7,
        "level": 3,
        "prop": _tools.RODict({0:52120893}),
        "needItems": _tools.ROList([[30000275, 44], [30000276, 44]]),
        "needCoins": _tools.ROList([30000002, 610000])
    }),
    190704: _tools.RODict({
        "ID": 190704,
        "meridian": 19,
        "acupoint": 7,
        "level": 4,
        "prop": _tools.RODict({0:52120894}),
        "needItems": _tools.ROList([[30000275, 46], [30000276, 46]]),
        "needCoins": _tools.ROList([30000002, 620000])
    }),
    190705: _tools.RODict({
        "ID": 190705,
        "meridian": 19,
        "acupoint": 7,
        "level": 5,
        "prop": _tools.RODict({0:52120895}),
        "needItems": _tools.ROList([[30000275, 48], [30000276, 48]]),
        "needCoins": _tools.ROList([30000002, 630000])
    }),
    190801: _tools.RODict({
        "ID": 190801,
        "meridian": 19,
        "acupoint": 8,
        "level": 1,
        "prop": _tools.RODict({0:52120991}),
        "needItems": _tools.ROList([[30000275, 40], [30000276, 40]]),
        "needCoins": _tools.ROList([30000002, 590000])
    }),
    190802: _tools.RODict({
        "ID": 190802,
        "meridian": 19,
        "acupoint": 8,
        "level": 2,
        "prop": _tools.RODict({0:52120992}),
        "needItems": _tools.ROList([[30000275, 42], [30000276, 42]]),
        "needCoins": _tools.ROList([30000002, 600000])
    }),
    190803: _tools.RODict({
        "ID": 190803,
        "meridian": 19,
        "acupoint": 8,
        "level": 3,
        "prop": _tools.RODict({0:52120993}),
        "needItems": _tools.ROList([[30000275, 44], [30000276, 44]]),
        "needCoins": _tools.ROList([30000002, 610000])
    }),
    190804: _tools.RODict({
        "ID": 190804,
        "meridian": 19,
        "acupoint": 8,
        "level": 4,
        "prop": _tools.RODict({0:52120994}),
        "needItems": _tools.ROList([[30000275, 46], [30000276, 46]]),
        "needCoins": _tools.ROList([30000002, 620000])
    }),
    190805: _tools.RODict({
        "ID": 190805,
        "meridian": 19,
        "acupoint": 8,
        "level": 5,
        "prop": _tools.RODict({0:52120995}),
        "needItems": _tools.ROList([[30000275, 48], [30000276, 48]]),
        "needCoins": _tools.ROList([30000002, 630000])
    }),
    200101: _tools.RODict({
        "ID": 200101,
        "meridian": 20,
        "acupoint": 1,
        "level": 1,
        "prop": _tools.RODict({0:52120096}),
        "needItems": _tools.ROList([[30000275, 50], [30000276, 50]]),
        "needCoins": _tools.ROList([30000002, 640000])
    }),
    200102: _tools.RODict({
        "ID": 200102,
        "meridian": 20,
        "acupoint": 1,
        "level": 2,
        "prop": _tools.RODict({0:52120097}),
        "needItems": _tools.ROList([[30000275, 52], [30000276, 52]]),
        "needCoins": _tools.ROList([30000002, 650000])
    }),
    200103: _tools.RODict({
        "ID": 200103,
        "meridian": 20,
        "acupoint": 1,
        "level": 3,
        "prop": _tools.RODict({0:52120098}),
        "needItems": _tools.ROList([[30000275, 54], [30000276, 54]]),
        "needCoins": _tools.ROList([30000002, 660000])
    }),
    200104: _tools.RODict({
        "ID": 200104,
        "meridian": 20,
        "acupoint": 1,
        "level": 4,
        "prop": _tools.RODict({0:52120099}),
        "needItems": _tools.ROList([[30000275, 56], [30000276, 56]]),
        "needCoins": _tools.ROList([30000002, 670000])
    }),
    200105: _tools.RODict({
        "ID": 200105,
        "meridian": 20,
        "acupoint": 1,
        "level": 5,
        "prop": _tools.RODict({0:52120100}),
        "needItems": _tools.ROList([[30000275, 58], [30000276, 58]]),
        "needCoins": _tools.ROList([30000002, 680000])
    }),
    200201: _tools.RODict({
        "ID": 200201,
        "meridian": 20,
        "acupoint": 2,
        "level": 1,
        "prop": _tools.RODict({0:52120196}),
        "needItems": _tools.ROList([[30000275, 50], [30000276, 50]]),
        "needCoins": _tools.ROList([30000002, 640000])
    }),
    200202: _tools.RODict({
        "ID": 200202,
        "meridian": 20,
        "acupoint": 2,
        "level": 2,
        "prop": _tools.RODict({0:52120197}),
        "needItems": _tools.ROList([[30000275, 52], [30000276, 52]]),
        "needCoins": _tools.ROList([30000002, 650000])
    }),
    200203: _tools.RODict({
        "ID": 200203,
        "meridian": 20,
        "acupoint": 2,
        "level": 3,
        "prop": _tools.RODict({0:52120198}),
        "needItems": _tools.ROList([[30000275, 54], [30000276, 54]]),
        "needCoins": _tools.ROList([30000002, 660000])
    }),
    200204: _tools.RODict({
        "ID": 200204,
        "meridian": 20,
        "acupoint": 2,
        "level": 4,
        "prop": _tools.RODict({0:52120199}),
        "needItems": _tools.ROList([[30000275, 56], [30000276, 56]]),
        "needCoins": _tools.ROList([30000002, 670000])
    }),
    200205: _tools.RODict({
        "ID": 200205,
        "meridian": 20,
        "acupoint": 2,
        "level": 5,
        "prop": _tools.RODict({0:52120200}),
        "needItems": _tools.ROList([[30000275, 58], [30000276, 58]]),
        "needCoins": _tools.ROList([30000002, 680000])
    }),
    200301: _tools.RODict({
        "ID": 200301,
        "meridian": 20,
        "acupoint": 3,
        "level": 1,
        "prop": _tools.RODict({1001:52120396,1002:52120396,1003:52120296}),
        "needItems": _tools.ROList([[30000275, 50], [30000276, 50]]),
        "needCoins": _tools.ROList([30000002, 640000])
    }),
    200302: _tools.RODict({
        "ID": 200302,
        "meridian": 20,
        "acupoint": 3,
        "level": 2,
        "prop": _tools.RODict({1001:52120397,1002:52120397,1003:52120297}),
        "needItems": _tools.ROList([[30000275, 52], [30000276, 52]]),
        "needCoins": _tools.ROList([30000002, 650000])
    }),
    200303: _tools.RODict({
        "ID": 200303,
        "meridian": 20,
        "acupoint": 3,
        "level": 3,
        "prop": _tools.RODict({1001:52120398,1002:52120398,1003:52120298}),
        "needItems": _tools.ROList([[30000275, 54], [30000276, 54]]),
        "needCoins": _tools.ROList([30000002, 660000])
    }),
    200304: _tools.RODict({
        "ID": 200304,
        "meridian": 20,
        "acupoint": 3,
        "level": 4,
        "prop": _tools.RODict({1001:52120399,1002:52120399,1003:52120299}),
        "needItems": _tools.ROList([[30000275, 56], [30000276, 56]]),
        "needCoins": _tools.ROList([30000002, 670000])
    }),
    200305: _tools.RODict({
        "ID": 200305,
        "meridian": 20,
        "acupoint": 3,
        "level": 5,
        "prop": _tools.RODict({1001:52120400,1002:52120400,1003:52120300}),
        "needItems": _tools.ROList([[30000275, 58], [30000276, 58]]),
        "needCoins": _tools.ROList([30000002, 680000])
    }),
    200401: _tools.RODict({
        "ID": 200401,
        "meridian": 20,
        "acupoint": 4,
        "level": 1,
        "prop": _tools.RODict({1001:52120596,1002:52120596,1003:52120496}),
        "needItems": _tools.ROList([[30000275, 50], [30000276, 50]]),
        "needCoins": _tools.ROList([30000002, 640000])
    }),
    200402: _tools.RODict({
        "ID": 200402,
        "meridian": 20,
        "acupoint": 4,
        "level": 2,
        "prop": _tools.RODict({1001:52120597,1002:52120597,1003:52120497}),
        "needItems": _tools.ROList([[30000275, 52], [30000276, 52]]),
        "needCoins": _tools.ROList([30000002, 650000])
    }),
    200403: _tools.RODict({
        "ID": 200403,
        "meridian": 20,
        "acupoint": 4,
        "level": 3,
        "prop": _tools.RODict({1001:52120598,1002:52120598,1003:52120498}),
        "needItems": _tools.ROList([[30000275, 54], [30000276, 54]]),
        "needCoins": _tools.ROList([30000002, 660000])
    }),
    200404: _tools.RODict({
        "ID": 200404,
        "meridian": 20,
        "acupoint": 4,
        "level": 4,
        "prop": _tools.RODict({1001:52120599,1002:52120599,1003:52120499}),
        "needItems": _tools.ROList([[30000275, 56], [30000276, 56]]),
        "needCoins": _tools.ROList([30000002, 670000])
    }),
    200405: _tools.RODict({
        "ID": 200405,
        "meridian": 20,
        "acupoint": 4,
        "level": 5,
        "prop": _tools.RODict({1001:52120600,1002:52120600,1003:52120500}),
        "needItems": _tools.ROList([[30000275, 58], [30000276, 58]]),
        "needCoins": _tools.ROList([30000002, 680000])
    }),
    200501: _tools.RODict({
        "ID": 200501,
        "meridian": 20,
        "acupoint": 5,
        "level": 1,
        "prop": _tools.RODict({0:52120696}),
        "needItems": _tools.ROList([[30000275, 50], [30000276, 50]]),
        "needCoins": _tools.ROList([30000002, 640000])
    }),
    200502: _tools.RODict({
        "ID": 200502,
        "meridian": 20,
        "acupoint": 5,
        "level": 2,
        "prop": _tools.RODict({0:52120697}),
        "needItems": _tools.ROList([[30000275, 52], [30000276, 52]]),
        "needCoins": _tools.ROList([30000002, 650000])
    }),
    200503: _tools.RODict({
        "ID": 200503,
        "meridian": 20,
        "acupoint": 5,
        "level": 3,
        "prop": _tools.RODict({0:52120698}),
        "needItems": _tools.ROList([[30000275, 54], [30000276, 54]]),
        "needCoins": _tools.ROList([30000002, 660000])
    }),
    200504: _tools.RODict({
        "ID": 200504,
        "meridian": 20,
        "acupoint": 5,
        "level": 4,
        "prop": _tools.RODict({0:52120699}),
        "needItems": _tools.ROList([[30000275, 56], [30000276, 56]]),
        "needCoins": _tools.ROList([30000002, 670000])
    }),
    200505: _tools.RODict({
        "ID": 200505,
        "meridian": 20,
        "acupoint": 5,
        "level": 5,
        "prop": _tools.RODict({0:52120700}),
        "needItems": _tools.ROList([[30000275, 58], [30000276, 58]]),
        "needCoins": _tools.ROList([30000002, 680000])
    }),
    200601: _tools.RODict({
        "ID": 200601,
        "meridian": 20,
        "acupoint": 6,
        "level": 1,
        "prop": _tools.RODict({0:52120796}),
        "needItems": _tools.ROList([[30000275, 50], [30000276, 50]]),
        "needCoins": _tools.ROList([30000002, 640000])
    }),
    200602: _tools.RODict({
        "ID": 200602,
        "meridian": 20,
        "acupoint": 6,
        "level": 2,
        "prop": _tools.RODict({0:52120797}),
        "needItems": _tools.ROList([[30000275, 52], [30000276, 52]]),
        "needCoins": _tools.ROList([30000002, 650000])
    }),
    200603: _tools.RODict({
        "ID": 200603,
        "meridian": 20,
        "acupoint": 6,
        "level": 3,
        "prop": _tools.RODict({0:52120798}),
        "needItems": _tools.ROList([[30000275, 54], [30000276, 54]]),
        "needCoins": _tools.ROList([30000002, 660000])
    }),
    200604: _tools.RODict({
        "ID": 200604,
        "meridian": 20,
        "acupoint": 6,
        "level": 4,
        "prop": _tools.RODict({0:52120799}),
        "needItems": _tools.ROList([[30000275, 56], [30000276, 56]]),
        "needCoins": _tools.ROList([30000002, 670000])
    }),
    200605: _tools.RODict({
        "ID": 200605,
        "meridian": 20,
        "acupoint": 6,
        "level": 5,
        "prop": _tools.RODict({0:52120800}),
        "needItems": _tools.ROList([[30000275, 58], [30000276, 58]]),
        "needCoins": _tools.ROList([30000002, 680000])
    }),
    200701: _tools.RODict({
        "ID": 200701,
        "meridian": 20,
        "acupoint": 7,
        "level": 1,
        "prop": _tools.RODict({0:52120896}),
        "needItems": _tools.ROList([[30000275, 50], [30000276, 50]]),
        "needCoins": _tools.ROList([30000002, 640000])
    }),
    200702: _tools.RODict({
        "ID": 200702,
        "meridian": 20,
        "acupoint": 7,
        "level": 2,
        "prop": _tools.RODict({0:52120897}),
        "needItems": _tools.ROList([[30000275, 52], [30000276, 52]]),
        "needCoins": _tools.ROList([30000002, 650000])
    }),
    200703: _tools.RODict({
        "ID": 200703,
        "meridian": 20,
        "acupoint": 7,
        "level": 3,
        "prop": _tools.RODict({0:52120898}),
        "needItems": _tools.ROList([[30000275, 54], [30000276, 54]]),
        "needCoins": _tools.ROList([30000002, 660000])
    }),
    200704: _tools.RODict({
        "ID": 200704,
        "meridian": 20,
        "acupoint": 7,
        "level": 4,
        "prop": _tools.RODict({0:52120899}),
        "needItems": _tools.ROList([[30000275, 56], [30000276, 56]]),
        "needCoins": _tools.ROList([30000002, 670000])
    }),
    200705: _tools.RODict({
        "ID": 200705,
        "meridian": 20,
        "acupoint": 7,
        "level": 5,
        "prop": _tools.RODict({0:52120900}),
        "needItems": _tools.ROList([[30000275, 58], [30000276, 58]]),
        "needCoins": _tools.ROList([30000002, 680000])
    }),
    200801: _tools.RODict({
        "ID": 200801,
        "meridian": 20,
        "acupoint": 8,
        "level": 1,
        "prop": _tools.RODict({0:52120996}),
        "needItems": _tools.ROList([[30000275, 50], [30000276, 50]]),
        "needCoins": _tools.ROList([30000002, 640000])
    }),
    200802: _tools.RODict({
        "ID": 200802,
        "meridian": 20,
        "acupoint": 8,
        "level": 2,
        "prop": _tools.RODict({0:52120997}),
        "needItems": _tools.ROList([[30000275, 52], [30000276, 52]]),
        "needCoins": _tools.ROList([30000002, 650000])
    }),
    200803: _tools.RODict({
        "ID": 200803,
        "meridian": 20,
        "acupoint": 8,
        "level": 3,
        "prop": _tools.RODict({0:52120998}),
        "needItems": _tools.ROList([[30000275, 54], [30000276, 54]]),
        "needCoins": _tools.ROList([30000002, 660000])
    }),
    200804: _tools.RODict({
        "ID": 200804,
        "meridian": 20,
        "acupoint": 8,
        "level": 4,
        "prop": _tools.RODict({0:52120999}),
        "needItems": _tools.ROList([[30000275, 56], [30000276, 56]]),
        "needCoins": _tools.ROList([30000002, 670000])
    }),
    200805: _tools.RODict({
        "ID": 200805,
        "meridian": 20,
        "acupoint": 8,
        "level": 5,
        "prop": _tools.RODict({0:52121000}),
        "needItems": _tools.ROList([[30000275, 58], [30000276, 58]]),
        "needCoins": _tools.ROList([30000002, 680000])
    })
})
minKey = 10101
maxKey = 200805