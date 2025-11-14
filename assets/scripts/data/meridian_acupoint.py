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
        "prop": _tools.RODict({0:52014262}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10102: _tools.RODict({
        "ID": 10102,
        "meridian": 1,
        "acupoint": 1,
        "level": 2,
        "prop": _tools.RODict({0:52014263}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10103: _tools.RODict({
        "ID": 10103,
        "meridian": 1,
        "acupoint": 1,
        "level": 3,
        "prop": _tools.RODict({0:52014264}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10104: _tools.RODict({
        "ID": 10104,
        "meridian": 1,
        "acupoint": 1,
        "level": 4,
        "prop": _tools.RODict({0:52014265}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10105: _tools.RODict({
        "ID": 10105,
        "meridian": 1,
        "acupoint": 1,
        "level": 5,
        "prop": _tools.RODict({0:52014266}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10201: _tools.RODict({
        "ID": 10201,
        "meridian": 1,
        "acupoint": 2,
        "level": 1,
        "prop": _tools.RODict({0:52014267}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10202: _tools.RODict({
        "ID": 10202,
        "meridian": 1,
        "acupoint": 2,
        "level": 2,
        "prop": _tools.RODict({0:52014268}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10203: _tools.RODict({
        "ID": 10203,
        "meridian": 1,
        "acupoint": 2,
        "level": 3,
        "prop": _tools.RODict({0:52014269}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10204: _tools.RODict({
        "ID": 10204,
        "meridian": 1,
        "acupoint": 2,
        "level": 4,
        "prop": _tools.RODict({0:52014270}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10205: _tools.RODict({
        "ID": 10205,
        "meridian": 1,
        "acupoint": 2,
        "level": 5,
        "prop": _tools.RODict({0:52014271}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10301: _tools.RODict({
        "ID": 10301,
        "meridian": 1,
        "acupoint": 3,
        "level": 1,
        "prop": _tools.RODict({1001:52014272,1002:52014272,1003:52014272}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10302: _tools.RODict({
        "ID": 10302,
        "meridian": 1,
        "acupoint": 3,
        "level": 2,
        "prop": _tools.RODict({1001:52014273,1002:52014273,1003:52014273}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10303: _tools.RODict({
        "ID": 10303,
        "meridian": 1,
        "acupoint": 3,
        "level": 3,
        "prop": _tools.RODict({1001:52014274,1002:52014274,1003:52014274}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10304: _tools.RODict({
        "ID": 10304,
        "meridian": 1,
        "acupoint": 3,
        "level": 4,
        "prop": _tools.RODict({1001:52014275,1002:52014275,1003:52014275}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10305: _tools.RODict({
        "ID": 10305,
        "meridian": 1,
        "acupoint": 3,
        "level": 5,
        "prop": _tools.RODict({1001:52014276,1002:52014276,1003:52014276}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10401: _tools.RODict({
        "ID": 10401,
        "meridian": 1,
        "acupoint": 4,
        "level": 1,
        "prop": _tools.RODict({1001:52014277,1002:52014277,1003:52014277}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10402: _tools.RODict({
        "ID": 10402,
        "meridian": 1,
        "acupoint": 4,
        "level": 2,
        "prop": _tools.RODict({1001:52014278,1002:52014278,1003:52014278}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10403: _tools.RODict({
        "ID": 10403,
        "meridian": 1,
        "acupoint": 4,
        "level": 3,
        "prop": _tools.RODict({1001:52014279,1002:52014279,1003:52014279}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10404: _tools.RODict({
        "ID": 10404,
        "meridian": 1,
        "acupoint": 4,
        "level": 4,
        "prop": _tools.RODict({1001:52014280,1002:52014280,1003:52014280}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10405: _tools.RODict({
        "ID": 10405,
        "meridian": 1,
        "acupoint": 4,
        "level": 5,
        "prop": _tools.RODict({1001:52014281,1002:52014281,1003:52014281}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10501: _tools.RODict({
        "ID": 10501,
        "meridian": 1,
        "acupoint": 5,
        "level": 1,
        "prop": _tools.RODict({0:52014282}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10502: _tools.RODict({
        "ID": 10502,
        "meridian": 1,
        "acupoint": 5,
        "level": 2,
        "prop": _tools.RODict({0:52014283}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10503: _tools.RODict({
        "ID": 10503,
        "meridian": 1,
        "acupoint": 5,
        "level": 3,
        "prop": _tools.RODict({0:52014284}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10504: _tools.RODict({
        "ID": 10504,
        "meridian": 1,
        "acupoint": 5,
        "level": 4,
        "prop": _tools.RODict({0:52014285}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10505: _tools.RODict({
        "ID": 10505,
        "meridian": 1,
        "acupoint": 5,
        "level": 5,
        "prop": _tools.RODict({0:52014286}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10601: _tools.RODict({
        "ID": 10601,
        "meridian": 1,
        "acupoint": 6,
        "level": 1,
        "prop": _tools.RODict({0:52014287}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10602: _tools.RODict({
        "ID": 10602,
        "meridian": 1,
        "acupoint": 6,
        "level": 2,
        "prop": _tools.RODict({0:52014288}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10603: _tools.RODict({
        "ID": 10603,
        "meridian": 1,
        "acupoint": 6,
        "level": 3,
        "prop": _tools.RODict({0:52014289}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10604: _tools.RODict({
        "ID": 10604,
        "meridian": 1,
        "acupoint": 6,
        "level": 4,
        "prop": _tools.RODict({0:52014290}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10605: _tools.RODict({
        "ID": 10605,
        "meridian": 1,
        "acupoint": 6,
        "level": 5,
        "prop": _tools.RODict({0:52014291}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10701: _tools.RODict({
        "ID": 10701,
        "meridian": 1,
        "acupoint": 7,
        "level": 1,
        "prop": _tools.RODict({0:52014292}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10702: _tools.RODict({
        "ID": 10702,
        "meridian": 1,
        "acupoint": 7,
        "level": 2,
        "prop": _tools.RODict({0:52014293}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10703: _tools.RODict({
        "ID": 10703,
        "meridian": 1,
        "acupoint": 7,
        "level": 3,
        "prop": _tools.RODict({0:52014294}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10704: _tools.RODict({
        "ID": 10704,
        "meridian": 1,
        "acupoint": 7,
        "level": 4,
        "prop": _tools.RODict({0:52014295}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10705: _tools.RODict({
        "ID": 10705,
        "meridian": 1,
        "acupoint": 7,
        "level": 5,
        "prop": _tools.RODict({0:52014296}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10801: _tools.RODict({
        "ID": 10801,
        "meridian": 1,
        "acupoint": 8,
        "level": 1,
        "prop": _tools.RODict({0:52014297}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10802: _tools.RODict({
        "ID": 10802,
        "meridian": 1,
        "acupoint": 8,
        "level": 2,
        "prop": _tools.RODict({0:52014298}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10803: _tools.RODict({
        "ID": 10803,
        "meridian": 1,
        "acupoint": 8,
        "level": 3,
        "prop": _tools.RODict({0:52014299}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10804: _tools.RODict({
        "ID": 10804,
        "meridian": 1,
        "acupoint": 8,
        "level": 4,
        "prop": _tools.RODict({0:52014300}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    10805: _tools.RODict({
        "ID": 10805,
        "meridian": 1,
        "acupoint": 8,
        "level": 5,
        "prop": _tools.RODict({0:52014301}),
        "needItems": _tools.ROList([[30000223, 20], [30000227, 5]]),
        "needCoins": _tools.ROList([30000002, 1000])
    }),
    20101: _tools.RODict({
        "ID": 20101,
        "meridian": 2,
        "acupoint": 1,
        "level": 1,
        "prop": _tools.RODict({0:52014262}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20102: _tools.RODict({
        "ID": 20102,
        "meridian": 2,
        "acupoint": 1,
        "level": 2,
        "prop": _tools.RODict({0:52014263}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20103: _tools.RODict({
        "ID": 20103,
        "meridian": 2,
        "acupoint": 1,
        "level": 3,
        "prop": _tools.RODict({0:52014264}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20104: _tools.RODict({
        "ID": 20104,
        "meridian": 2,
        "acupoint": 1,
        "level": 4,
        "prop": _tools.RODict({0:52014265}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20105: _tools.RODict({
        "ID": 20105,
        "meridian": 2,
        "acupoint": 1,
        "level": 5,
        "prop": _tools.RODict({0:52014266}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20201: _tools.RODict({
        "ID": 20201,
        "meridian": 2,
        "acupoint": 2,
        "level": 1,
        "prop": _tools.RODict({0:52014267}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20202: _tools.RODict({
        "ID": 20202,
        "meridian": 2,
        "acupoint": 2,
        "level": 2,
        "prop": _tools.RODict({0:52014268}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20203: _tools.RODict({
        "ID": 20203,
        "meridian": 2,
        "acupoint": 2,
        "level": 3,
        "prop": _tools.RODict({0:52014269}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20204: _tools.RODict({
        "ID": 20204,
        "meridian": 2,
        "acupoint": 2,
        "level": 4,
        "prop": _tools.RODict({0:52014270}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20205: _tools.RODict({
        "ID": 20205,
        "meridian": 2,
        "acupoint": 2,
        "level": 5,
        "prop": _tools.RODict({0:52014271}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20301: _tools.RODict({
        "ID": 20301,
        "meridian": 2,
        "acupoint": 3,
        "level": 1,
        "prop": _tools.RODict({0:52014272}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20302: _tools.RODict({
        "ID": 20302,
        "meridian": 2,
        "acupoint": 3,
        "level": 2,
        "prop": _tools.RODict({0:52014273}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20303: _tools.RODict({
        "ID": 20303,
        "meridian": 2,
        "acupoint": 3,
        "level": 3,
        "prop": _tools.RODict({0:52014274}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20304: _tools.RODict({
        "ID": 20304,
        "meridian": 2,
        "acupoint": 3,
        "level": 4,
        "prop": _tools.RODict({0:52014275}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20305: _tools.RODict({
        "ID": 20305,
        "meridian": 2,
        "acupoint": 3,
        "level": 5,
        "prop": _tools.RODict({0:52014276}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20401: _tools.RODict({
        "ID": 20401,
        "meridian": 2,
        "acupoint": 4,
        "level": 1,
        "prop": _tools.RODict({0:52014277}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20402: _tools.RODict({
        "ID": 20402,
        "meridian": 2,
        "acupoint": 4,
        "level": 2,
        "prop": _tools.RODict({0:52014278}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20403: _tools.RODict({
        "ID": 20403,
        "meridian": 2,
        "acupoint": 4,
        "level": 3,
        "prop": _tools.RODict({0:52014279}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20404: _tools.RODict({
        "ID": 20404,
        "meridian": 2,
        "acupoint": 4,
        "level": 4,
        "prop": _tools.RODict({0:52014280}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20405: _tools.RODict({
        "ID": 20405,
        "meridian": 2,
        "acupoint": 4,
        "level": 5,
        "prop": _tools.RODict({0:52014281}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20501: _tools.RODict({
        "ID": 20501,
        "meridian": 2,
        "acupoint": 5,
        "level": 1,
        "prop": _tools.RODict({0:52014282}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20502: _tools.RODict({
        "ID": 20502,
        "meridian": 2,
        "acupoint": 5,
        "level": 2,
        "prop": _tools.RODict({0:52014283}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20503: _tools.RODict({
        "ID": 20503,
        "meridian": 2,
        "acupoint": 5,
        "level": 3,
        "prop": _tools.RODict({0:52014284}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20504: _tools.RODict({
        "ID": 20504,
        "meridian": 2,
        "acupoint": 5,
        "level": 4,
        "prop": _tools.RODict({0:52014285}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20505: _tools.RODict({
        "ID": 20505,
        "meridian": 2,
        "acupoint": 5,
        "level": 5,
        "prop": _tools.RODict({0:52014286}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20601: _tools.RODict({
        "ID": 20601,
        "meridian": 2,
        "acupoint": 6,
        "level": 1,
        "prop": _tools.RODict({0:52014287}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20602: _tools.RODict({
        "ID": 20602,
        "meridian": 2,
        "acupoint": 6,
        "level": 2,
        "prop": _tools.RODict({0:52014288}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20603: _tools.RODict({
        "ID": 20603,
        "meridian": 2,
        "acupoint": 6,
        "level": 3,
        "prop": _tools.RODict({0:52014289}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20604: _tools.RODict({
        "ID": 20604,
        "meridian": 2,
        "acupoint": 6,
        "level": 4,
        "prop": _tools.RODict({0:52014290}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20605: _tools.RODict({
        "ID": 20605,
        "meridian": 2,
        "acupoint": 6,
        "level": 5,
        "prop": _tools.RODict({0:52014291}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20701: _tools.RODict({
        "ID": 20701,
        "meridian": 2,
        "acupoint": 7,
        "level": 1,
        "prop": _tools.RODict({0:52014292}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20702: _tools.RODict({
        "ID": 20702,
        "meridian": 2,
        "acupoint": 7,
        "level": 2,
        "prop": _tools.RODict({0:52014293}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20703: _tools.RODict({
        "ID": 20703,
        "meridian": 2,
        "acupoint": 7,
        "level": 3,
        "prop": _tools.RODict({0:52014294}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20704: _tools.RODict({
        "ID": 20704,
        "meridian": 2,
        "acupoint": 7,
        "level": 4,
        "prop": _tools.RODict({0:52014295}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20705: _tools.RODict({
        "ID": 20705,
        "meridian": 2,
        "acupoint": 7,
        "level": 5,
        "prop": _tools.RODict({0:52014296}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20801: _tools.RODict({
        "ID": 20801,
        "meridian": 2,
        "acupoint": 8,
        "level": 1,
        "prop": _tools.RODict({0:52014297}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20802: _tools.RODict({
        "ID": 20802,
        "meridian": 2,
        "acupoint": 8,
        "level": 2,
        "prop": _tools.RODict({0:52014298}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20803: _tools.RODict({
        "ID": 20803,
        "meridian": 2,
        "acupoint": 8,
        "level": 3,
        "prop": _tools.RODict({0:52014299}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20804: _tools.RODict({
        "ID": 20804,
        "meridian": 2,
        "acupoint": 8,
        "level": 4,
        "prop": _tools.RODict({0:52014300}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    20805: _tools.RODict({
        "ID": 20805,
        "meridian": 2,
        "acupoint": 8,
        "level": 5,
        "prop": _tools.RODict({0:52014301}),
        "needItems": _tools.ROList([[30000224, 20], [30000228, 5]]),
        "needCoins": _tools.ROList([30000002, 1500])
    }),
    30101: _tools.RODict({
        "ID": 30101,
        "meridian": 3,
        "acupoint": 1,
        "level": 1,
        "prop": _tools.RODict({0:52014262}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30102: _tools.RODict({
        "ID": 30102,
        "meridian": 3,
        "acupoint": 1,
        "level": 2,
        "prop": _tools.RODict({0:52014263}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30103: _tools.RODict({
        "ID": 30103,
        "meridian": 3,
        "acupoint": 1,
        "level": 3,
        "prop": _tools.RODict({0:52014264}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30104: _tools.RODict({
        "ID": 30104,
        "meridian": 3,
        "acupoint": 1,
        "level": 4,
        "prop": _tools.RODict({0:52014265}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30105: _tools.RODict({
        "ID": 30105,
        "meridian": 3,
        "acupoint": 1,
        "level": 5,
        "prop": _tools.RODict({0:52014266}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30201: _tools.RODict({
        "ID": 30201,
        "meridian": 3,
        "acupoint": 2,
        "level": 1,
        "prop": _tools.RODict({0:52014267}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30202: _tools.RODict({
        "ID": 30202,
        "meridian": 3,
        "acupoint": 2,
        "level": 2,
        "prop": _tools.RODict({0:52014268}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30203: _tools.RODict({
        "ID": 30203,
        "meridian": 3,
        "acupoint": 2,
        "level": 3,
        "prop": _tools.RODict({0:52014269}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30204: _tools.RODict({
        "ID": 30204,
        "meridian": 3,
        "acupoint": 2,
        "level": 4,
        "prop": _tools.RODict({0:52014270}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30205: _tools.RODict({
        "ID": 30205,
        "meridian": 3,
        "acupoint": 2,
        "level": 5,
        "prop": _tools.RODict({0:52014271}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30301: _tools.RODict({
        "ID": 30301,
        "meridian": 3,
        "acupoint": 3,
        "level": 1,
        "prop": _tools.RODict({0:52014272}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30302: _tools.RODict({
        "ID": 30302,
        "meridian": 3,
        "acupoint": 3,
        "level": 2,
        "prop": _tools.RODict({0:52014273}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30303: _tools.RODict({
        "ID": 30303,
        "meridian": 3,
        "acupoint": 3,
        "level": 3,
        "prop": _tools.RODict({0:52014274}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30304: _tools.RODict({
        "ID": 30304,
        "meridian": 3,
        "acupoint": 3,
        "level": 4,
        "prop": _tools.RODict({0:52014275}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30305: _tools.RODict({
        "ID": 30305,
        "meridian": 3,
        "acupoint": 3,
        "level": 5,
        "prop": _tools.RODict({0:52014276}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30401: _tools.RODict({
        "ID": 30401,
        "meridian": 3,
        "acupoint": 4,
        "level": 1,
        "prop": _tools.RODict({0:52014277}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30402: _tools.RODict({
        "ID": 30402,
        "meridian": 3,
        "acupoint": 4,
        "level": 2,
        "prop": _tools.RODict({0:52014278}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30403: _tools.RODict({
        "ID": 30403,
        "meridian": 3,
        "acupoint": 4,
        "level": 3,
        "prop": _tools.RODict({0:52014279}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30404: _tools.RODict({
        "ID": 30404,
        "meridian": 3,
        "acupoint": 4,
        "level": 4,
        "prop": _tools.RODict({0:52014280}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30405: _tools.RODict({
        "ID": 30405,
        "meridian": 3,
        "acupoint": 4,
        "level": 5,
        "prop": _tools.RODict({0:52014281}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30501: _tools.RODict({
        "ID": 30501,
        "meridian": 3,
        "acupoint": 5,
        "level": 1,
        "prop": _tools.RODict({0:52014282}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30502: _tools.RODict({
        "ID": 30502,
        "meridian": 3,
        "acupoint": 5,
        "level": 2,
        "prop": _tools.RODict({0:52014283}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30503: _tools.RODict({
        "ID": 30503,
        "meridian": 3,
        "acupoint": 5,
        "level": 3,
        "prop": _tools.RODict({0:52014284}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30504: _tools.RODict({
        "ID": 30504,
        "meridian": 3,
        "acupoint": 5,
        "level": 4,
        "prop": _tools.RODict({0:52014285}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30505: _tools.RODict({
        "ID": 30505,
        "meridian": 3,
        "acupoint": 5,
        "level": 5,
        "prop": _tools.RODict({0:52014286}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30601: _tools.RODict({
        "ID": 30601,
        "meridian": 3,
        "acupoint": 6,
        "level": 1,
        "prop": _tools.RODict({0:52014287}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30602: _tools.RODict({
        "ID": 30602,
        "meridian": 3,
        "acupoint": 6,
        "level": 2,
        "prop": _tools.RODict({0:52014288}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30603: _tools.RODict({
        "ID": 30603,
        "meridian": 3,
        "acupoint": 6,
        "level": 3,
        "prop": _tools.RODict({0:52014289}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30604: _tools.RODict({
        "ID": 30604,
        "meridian": 3,
        "acupoint": 6,
        "level": 4,
        "prop": _tools.RODict({0:52014290}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30605: _tools.RODict({
        "ID": 30605,
        "meridian": 3,
        "acupoint": 6,
        "level": 5,
        "prop": _tools.RODict({0:52014291}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30701: _tools.RODict({
        "ID": 30701,
        "meridian": 3,
        "acupoint": 7,
        "level": 1,
        "prop": _tools.RODict({0:52014292}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30702: _tools.RODict({
        "ID": 30702,
        "meridian": 3,
        "acupoint": 7,
        "level": 2,
        "prop": _tools.RODict({0:52014293}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30703: _tools.RODict({
        "ID": 30703,
        "meridian": 3,
        "acupoint": 7,
        "level": 3,
        "prop": _tools.RODict({0:52014294}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30704: _tools.RODict({
        "ID": 30704,
        "meridian": 3,
        "acupoint": 7,
        "level": 4,
        "prop": _tools.RODict({0:52014295}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30705: _tools.RODict({
        "ID": 30705,
        "meridian": 3,
        "acupoint": 7,
        "level": 5,
        "prop": _tools.RODict({0:52014296}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30801: _tools.RODict({
        "ID": 30801,
        "meridian": 3,
        "acupoint": 8,
        "level": 1,
        "prop": _tools.RODict({0:52014297}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30802: _tools.RODict({
        "ID": 30802,
        "meridian": 3,
        "acupoint": 8,
        "level": 2,
        "prop": _tools.RODict({0:52014298}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30803: _tools.RODict({
        "ID": 30803,
        "meridian": 3,
        "acupoint": 8,
        "level": 3,
        "prop": _tools.RODict({0:52014299}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30804: _tools.RODict({
        "ID": 30804,
        "meridian": 3,
        "acupoint": 8,
        "level": 4,
        "prop": _tools.RODict({0:52014300}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    30805: _tools.RODict({
        "ID": 30805,
        "meridian": 3,
        "acupoint": 8,
        "level": 5,
        "prop": _tools.RODict({0:52014301}),
        "needItems": _tools.ROList([[30000225, 20], [30000229, 5]]),
        "needCoins": _tools.ROList([30000002, 2000])
    }),
    40101: _tools.RODict({
        "ID": 40101,
        "meridian": 4,
        "acupoint": 1,
        "level": 1,
        "prop": _tools.RODict({0:52014262}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40102: _tools.RODict({
        "ID": 40102,
        "meridian": 4,
        "acupoint": 1,
        "level": 2,
        "prop": _tools.RODict({0:52014263}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40103: _tools.RODict({
        "ID": 40103,
        "meridian": 4,
        "acupoint": 1,
        "level": 3,
        "prop": _tools.RODict({0:52014264}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40104: _tools.RODict({
        "ID": 40104,
        "meridian": 4,
        "acupoint": 1,
        "level": 4,
        "prop": _tools.RODict({0:52014265}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40105: _tools.RODict({
        "ID": 40105,
        "meridian": 4,
        "acupoint": 1,
        "level": 5,
        "prop": _tools.RODict({0:52014266}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40201: _tools.RODict({
        "ID": 40201,
        "meridian": 4,
        "acupoint": 2,
        "level": 1,
        "prop": _tools.RODict({0:52014267}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40202: _tools.RODict({
        "ID": 40202,
        "meridian": 4,
        "acupoint": 2,
        "level": 2,
        "prop": _tools.RODict({0:52014268}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40203: _tools.RODict({
        "ID": 40203,
        "meridian": 4,
        "acupoint": 2,
        "level": 3,
        "prop": _tools.RODict({0:52014269}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40204: _tools.RODict({
        "ID": 40204,
        "meridian": 4,
        "acupoint": 2,
        "level": 4,
        "prop": _tools.RODict({0:52014270}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40205: _tools.RODict({
        "ID": 40205,
        "meridian": 4,
        "acupoint": 2,
        "level": 5,
        "prop": _tools.RODict({0:52014271}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40301: _tools.RODict({
        "ID": 40301,
        "meridian": 4,
        "acupoint": 3,
        "level": 1,
        "prop": _tools.RODict({0:52014272}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40302: _tools.RODict({
        "ID": 40302,
        "meridian": 4,
        "acupoint": 3,
        "level": 2,
        "prop": _tools.RODict({0:52014273}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40303: _tools.RODict({
        "ID": 40303,
        "meridian": 4,
        "acupoint": 3,
        "level": 3,
        "prop": _tools.RODict({0:52014274}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40304: _tools.RODict({
        "ID": 40304,
        "meridian": 4,
        "acupoint": 3,
        "level": 4,
        "prop": _tools.RODict({0:52014275}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40305: _tools.RODict({
        "ID": 40305,
        "meridian": 4,
        "acupoint": 3,
        "level": 5,
        "prop": _tools.RODict({0:52014276}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40401: _tools.RODict({
        "ID": 40401,
        "meridian": 4,
        "acupoint": 4,
        "level": 1,
        "prop": _tools.RODict({0:52014277}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40402: _tools.RODict({
        "ID": 40402,
        "meridian": 4,
        "acupoint": 4,
        "level": 2,
        "prop": _tools.RODict({0:52014278}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40403: _tools.RODict({
        "ID": 40403,
        "meridian": 4,
        "acupoint": 4,
        "level": 3,
        "prop": _tools.RODict({0:52014279}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40404: _tools.RODict({
        "ID": 40404,
        "meridian": 4,
        "acupoint": 4,
        "level": 4,
        "prop": _tools.RODict({0:52014280}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40405: _tools.RODict({
        "ID": 40405,
        "meridian": 4,
        "acupoint": 4,
        "level": 5,
        "prop": _tools.RODict({0:52014281}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40501: _tools.RODict({
        "ID": 40501,
        "meridian": 4,
        "acupoint": 5,
        "level": 1,
        "prop": _tools.RODict({0:52014282}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40502: _tools.RODict({
        "ID": 40502,
        "meridian": 4,
        "acupoint": 5,
        "level": 2,
        "prop": _tools.RODict({0:52014283}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40503: _tools.RODict({
        "ID": 40503,
        "meridian": 4,
        "acupoint": 5,
        "level": 3,
        "prop": _tools.RODict({0:52014284}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40504: _tools.RODict({
        "ID": 40504,
        "meridian": 4,
        "acupoint": 5,
        "level": 4,
        "prop": _tools.RODict({0:52014285}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40505: _tools.RODict({
        "ID": 40505,
        "meridian": 4,
        "acupoint": 5,
        "level": 5,
        "prop": _tools.RODict({0:52014286}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40601: _tools.RODict({
        "ID": 40601,
        "meridian": 4,
        "acupoint": 6,
        "level": 1,
        "prop": _tools.RODict({0:52014287}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40602: _tools.RODict({
        "ID": 40602,
        "meridian": 4,
        "acupoint": 6,
        "level": 2,
        "prop": _tools.RODict({0:52014288}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40603: _tools.RODict({
        "ID": 40603,
        "meridian": 4,
        "acupoint": 6,
        "level": 3,
        "prop": _tools.RODict({0:52014289}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40604: _tools.RODict({
        "ID": 40604,
        "meridian": 4,
        "acupoint": 6,
        "level": 4,
        "prop": _tools.RODict({0:52014290}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40605: _tools.RODict({
        "ID": 40605,
        "meridian": 4,
        "acupoint": 6,
        "level": 5,
        "prop": _tools.RODict({0:52014291}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40701: _tools.RODict({
        "ID": 40701,
        "meridian": 4,
        "acupoint": 7,
        "level": 1,
        "prop": _tools.RODict({0:52014292}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40702: _tools.RODict({
        "ID": 40702,
        "meridian": 4,
        "acupoint": 7,
        "level": 2,
        "prop": _tools.RODict({0:52014293}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40703: _tools.RODict({
        "ID": 40703,
        "meridian": 4,
        "acupoint": 7,
        "level": 3,
        "prop": _tools.RODict({0:52014294}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40704: _tools.RODict({
        "ID": 40704,
        "meridian": 4,
        "acupoint": 7,
        "level": 4,
        "prop": _tools.RODict({0:52014295}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40705: _tools.RODict({
        "ID": 40705,
        "meridian": 4,
        "acupoint": 7,
        "level": 5,
        "prop": _tools.RODict({0:52014296}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40801: _tools.RODict({
        "ID": 40801,
        "meridian": 4,
        "acupoint": 8,
        "level": 1,
        "prop": _tools.RODict({0:52014297}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40802: _tools.RODict({
        "ID": 40802,
        "meridian": 4,
        "acupoint": 8,
        "level": 2,
        "prop": _tools.RODict({0:52014298}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40803: _tools.RODict({
        "ID": 40803,
        "meridian": 4,
        "acupoint": 8,
        "level": 3,
        "prop": _tools.RODict({0:52014299}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40804: _tools.RODict({
        "ID": 40804,
        "meridian": 4,
        "acupoint": 8,
        "level": 4,
        "prop": _tools.RODict({0:52014300}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    }),
    40805: _tools.RODict({
        "ID": 40805,
        "meridian": 4,
        "acupoint": 8,
        "level": 5,
        "prop": _tools.RODict({0:52014301}),
        "needItems": _tools.ROList([[30000226, 20], [30000230, 5]]),
        "needCoins": _tools.ROList([30000002, 2500])
    })
})
minKey = 10101
maxKey = 40805